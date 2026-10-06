"""contract_probe.py - Cognitive Contract readiness probe (v3.6).

Before any slide is written, the Agent must know four things (Q1~Q4) plus a few
scenario-specific facts (a QBR needs the variance, an RFC needs the migration plan).
This module reads the user's prompt (and optional reference document), classifies the
scenario, and reports which of those are still unknown, as consultant-style questions.

It is a heuristic: it detects whether a fact is *mentioned*, not whether it is *right*.
Its job is to stop the Agent from generating a deck out of an under-specified request.
"""

import re
from typing import Any, Dict, List, Optional

from core.cognitive_planner import CognitivePlanner

MONEY = r"\d+(?:\.\d+)?\s*(?:万|亿|元|百万|千万|[kKmM])"
PCT = r"\d+(?:\.\d+)?\s*(?:%|％|倍|[xX])"
TIME = r"(?:Q[1-4]|[1-4]\s*季度|\d+\s*个?\s*(?:月|周|天|年)|\d{4}\s*年|H[12]|上半年|下半年)"
HEADCOUNT = r"\d+\s*(?:个|名|位)?\s*(?:人头|HC|hc|编制|名额)"

UNIVERSAL = [
    {
        "key": "Q1",
        "name": "核心主旨",
        "pattern": r"(?:提升|降低|增长|下降|节省|缩短|推荐|建议|证明|目标|预期|实现|突破|选型|迁移|重构|优于|超过|转型|对齐)",
        "question": "抛开枝节，这份材料最想让对方记住的一句话是什么？（一个明确的判断，而不只是主题）",
        "blocking": False,
    },
    {
        "key": "Q2",
        "name": "受众与立场",
        "pattern": r"(?:领导|高管|管理层|委员会|评委|评审|客户|CTO|CEO|VP|总监|老板|投资人|董事|全员|同事|学员|团队|架构师|PMO|财务|HR|部门|甲方|面试)",
        "question": "谁在听？他们的立场和最担心的事是什么？（例如：CTO 担心迁移风险，财务担心 ROI）",
        "blocking": True,
    },
    {
        "key": "Q3",
        "name": "认知差与痛点",
        "pattern": r"(?:痛点|问题|瓶颈|风险|挑战|故障|不足|落后|成本高|流失|下滑|压力|缺口|低效|延期|承压|盲区|担心|质疑|饱和|超负荷)",
        "question": "对方现在已经知道什么？他们不知道、但必须知道的痛点或盲区是什么？",
        "blocking": False,
    },
    {
        "key": "Q4",
        "name": "终局行动",
        "pattern": r"(?:批准|决策|拍板|审批|预算|人头|立项|选型|采纳|签字|同意|授权|晋升|申请|通过|表决|签约|中标|启动|落地|对齐)",
        "question": "讲完之后，你希望对方当场做出什么决定或动作？（批预算、选方案、签字、改变做法……）",
        "blocking": True,
    },
]

SCENARIOS: Dict[str, Dict[str, Any]] = {
    "project_charter": {
        "label": "项目立项答辩与投资评审",
        "facts": [
            ("investment", "首期需要多少预算和人力？", MONEY + r"|" + HEADCOUNT),
            ("return", "预期回报是什么？（ROI、成本节降、收入增量，越量化越好）", PCT + r"|ROI|回报|收益|节降"),
            ("timeline", "里程碑和时间窗口是什么？", TIME),
            ("alternatives", "有哪些备选方案？不做的代价是什么？", r"备选|方案\s*[ABC]|替代|对比|不做|维持现状"),
        ],
    },
    "annual_strategy_okr": {
        "label": "年度战略规划与 OKR",
        "facts": [
            ("north_star", "年度北极星指标是什么，目标值多少？", r"北极星|核心指标|增长目标|" + PCT),
            ("resources", "资源如何在现有业务和新业务之间分配？", r"资源|配比|预算|人力|\d+\s*:\s*\d+"),
            ("cascade", "OKR 拆到哪一层（公司/部门/团队）？", r"OKR|部门|团队|拆解|对齐"),
            ("bets", "今年最关键的几场必赢战役是什么？", r"战役|必赢|重点|攻坚|优先级"),
        ],
    },
    "qbr_business_review": {
        "label": "季度业务复盘 QBR",
        "facts": [
            ("metrics", "本期核心指标和达成情况（附同比/环比）？", r"同比|环比|达成|完成率|" + PCT),
            ("variance", "哪些指标偏离了目标，原因是什么？", r"偏差|未达|未达成|下滑|承压|缺口|原因|归因"),
            ("actions", "下个周期的纠偏动作是什么？", r"措施|行动|下季度|纠偏|整改|计划"),
            ("period", "复盘的是哪个周期？", TIME + r"|季度|月度"),
        ],
    },
    "cross_team_alignment": {
        "label": "跨部门协同与共识拉通",
        "facts": [
            ("parties", "涉及哪几个团队？各自的角色是什么？", r"(?:产品|研发|运营|销售|财务|市场|测试|客服|数据|法务)[\s\S]*(?:产品|研发|运营|销售|财务|市场|测试|客服|数据|法务)"),
            ("dependencies", "关键依赖和接口约定是什么？", r"依赖|接口|SLA|联调|交付|对接"),
            ("conflict", "目前卡在哪里？分歧或延期点是什么？", r"冲突|分歧|瓶颈|延期|推诿|优先级|卡点|阻塞"),
            ("deadline", "对齐的截止时间是什么？", TIME),
        ],
    },
    "team_headcount_review": {
        "label": "团队述职与 HC 编制申请",
        "facts": [
            ("ask", "具体申请多少编制或预算？", HEADCOUNT + r"|" + MONEY),
            ("load", "现有团队的负载和业务增量证据？", r"人效|负载|饱和|业务量|产出|增长|" + PCT),
            ("roi", "每个新增编制对应什么产出？", r"ROI|产出|对应|产能|回报"),
            ("rollout", "是否分批释放、如何设置门禁？", r"分批|分期|阶梯|释放|门禁|两期"),
        ],
    },
    "tech_rfc_review": {
        "label": "技术方案选型与架构 RFC 评审",
        "facts": [
            ("options", "对比哪几个方案？（含维持现状）", r"对比|方案\s*[ABC]|自研|开源|云厂商|托管|选型"),
            ("nfr", "非功能性指标要求是什么？（延迟、吞吐、可用性）", r"延迟|QPS|TPS|吞吐|可用性|SLA|\d+\s*ms|99\.?\d*"),
            ("migration", "迁移、灰度和回滚方案？", r"迁移|回滚|灰度|双写|双读|平滑"),
            ("current", "现状瓶颈是什么？规模多大？", r"现状|瓶颈|规模|单体|扩展|" + PCT),
        ],
    },
    "post_mortem_review": {
        "label": "生产故障复盘与根因分析",
        "facts": [
            ("timeline", "故障时间线：何时发生、何时发现、何时止血、何时恢复？", r"\d{1,2}\s*[:：]\s*\d{2}|\d+\s*分钟|时间线|持续|宕机|历时"),
            ("impact", "影响了多少用户、订单或资金？", r"影响|订单|用户|资损|笔|客户|" + MONEY),
            ("root_cause", "根因是什么？（连问五个为什么）", r"根因|原因|配置|变更|发布|5\s*Whys|Why"),
            ("fixes", "整改项有哪些？谁负责、何时完成？", r"整改|防呆|行动项|改进|复盘措施|红线"),
        ],
    },
    "product_launch_gtm": {
        "label": "新产品发布与 GTM 上市",
        "facts": [
            ("icp", "首批目标客群是谁？", r"客群|目标客户|ICP|用户画像|中大型|KA|SMB|企业"),
            ("differentiator", "最强的差异化卖点是什么？", r"特性|差异化|卖点|优势|领先|杀手"),
            ("pricing", "怎么定价？单客经济如何？", r"定价|价格|付费|收费|毛利|客单|" + MONEY),
            ("gtm_goal", "上市目标和渠道节奏？", r"目标|营收|获客|转化|渠道|" + MONEY),
        ],
    },
    "enterprise_rfp_pitch": {
        "label": "大客户商务提案与竞标",
        "facts": [
            ("client", "客户是谁、处在什么行业和阶段？", r"客户|银行|甲方|行业|政企|央企|保险|医院"),
            ("requirements", "客户的核心需求和合规要求是什么？", r"需求|合规|等保|性能|SLA|要求|招标"),
            ("proof", "有哪些同类标杆案例可以佐证？", r"案例|标杆|已交付|成功|服务过"),
            ("commercials", "报价、TCO 和交付周期？", r"报价|TCO|周期|交付|" + MONEY),
        ],
    },
    "promotion_assessment": {
        "label": "晋升答辩与职级评审",
        "facts": [
            ("level", "申请晋升到什么职级？", r"晋升|P\d|M\d|职级|高级|资深|专家|级"),
            ("star", "最能代表你的 2~3 个项目，你具体做了什么？", r"主导|负责|项目|重构|攻坚|STAR"),
            ("net_impact", "结果的量化指标是什么？", PCT + r"|节省|降低|提升|" + MONEY),
            ("baseline", "团队或大盘本身的增长是多少？你的净增量是多少？", r"净|相比|对比|基线|大盘|团队整体|扣除"),
        ],
    },
    "internal_tech_talk": {
        "label": "内部技术分享与赋能培训",
        "facts": [
            ("learners", "听众是谁，现有水平如何？", r"新人|资深|学员|工程师|后端|前端|同学|开发者|团队"),
            ("takeaway", "听完后他们应该学会或改掉什么？", r"学会|收获|原则|反模式|最佳实践|方法|避免|改掉"),
            ("example", "有哪个真实案例或代码可以做反例/对照？", r"案例|代码|线上|事故|示例|实战|对照"),
            ("duration", "时长多久？", r"\d+\s*(?:分钟|小时)|一场|半天"),
        ],
    },
    "all_hands_rally": {
        "label": "全员大会与战略动员",
        "facts": [
            ("goal", "年度或阶段的硬目标是什么？", r"目标|营收|亿|冲刺|" + PCT),
            ("context", "外部大势和我们的窗口期是什么？", r"大势|窗口|周期|对手|环境|行业"),
            ("culture", "要强化哪些价值观或行为公约？", r"文化|价值观|公约|奋斗|使命|愿景"),
            ("incentive", "对奋斗者有什么激励和机制？", r"激励|奖励|机制|分红|晋升|奖金"),
        ],
    },
}


def _grounded_text(planner: CognitivePlanner, prompt: str, context: Optional[str], doc_path: Optional[str]) -> Dict[str, Any]:
    import os

    source = doc_path if (doc_path and os.path.exists(doc_path)) else context
    return planner.ingestor.ingest(source)


def probe(prompt: str, context: Optional[str] = None, doc_path: Optional[str] = None) -> Dict[str, Any]:
    """Return which contract slots and scenario facts are still unknown for this request."""
    planner = CognitivePlanner()
    grounded = _grounded_text(planner, prompt, context, doc_path)
    meta = planner._classify_scenario(prompt.strip(), grounded)
    stype = meta["scenario_type"]
    text = f"{prompt} {grounded.get('raw_text', '')}"

    slots: List[Dict[str, Any]] = []
    for u in UNIVERSAL:
        slots.append({
            "key": u["key"], "name": u["name"], "kind": "contract",
            "satisfied": bool(re.search(u["pattern"], text, re.IGNORECASE)),
            "question": u["question"], "blocking": u["blocking"],
        })
    spec = SCENARIOS.get(stype)
    for key, question, pattern in (spec["facts"] if spec else []):
        slots.append({
            "key": key, "name": key, "kind": "fact",
            "satisfied": bool(re.search(pattern, text, re.IGNORECASE)),
            "question": question, "blocking": False,
        })

    satisfied = sum(1 for s in slots if s["satisfied"])
    readiness = round(satisfied / len(slots), 2)
    blocking_missing = [s for s in slots if s["blocking"] and not s["satisfied"]]
    ready = readiness >= 0.7 and not blocking_missing
    missing = [s for s in slots if not s["satisfied"]]
    # Ask blocking questions first, then contract, then facts.
    missing.sort(key=lambda s: (not s["blocking"], s["kind"] != "contract"))

    return {
        "scenario": stype,
        "scenario_label": spec["label"] if spec else "通用汇报",
        "subject": meta.get("subject"),
        "readiness": readiness,
        "ready": ready,
        "slots": slots,
        "questions": [s["question"] for s in missing],
        "blocking": [s["key"] for s in blocking_missing],
        "note": "启发式检测：只判断是否提及，不判断是否正确。信息不足时先向用户提问，不要直接生成。",
    }
