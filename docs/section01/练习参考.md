# 第一章

# 一、请分析以下四个 `case` 中的**主体**是否属于智能体，如果是，那么属于哪种类型的智能体（可以从多个分类维度进行分析），并说明理由：

`case A`：**一台符合冯·诺依曼结构的超级计算机**，拥有高达每秒 2EFlop 的峰值算力

`case B`：**特斯拉自动驾驶系统**在高速公路上行驶时，突然检测到前方有障碍物，需要在毫秒级做出刹车或变道决策

`case C`：**AlphaGo**在与人类棋手对弈时，需要评估当前局面并规划未来数十步的最优策略

`case D`：**ChatGPT 扮演的智能客服**在处理用户投诉时，需要查询订单信息、分析问题原因、提供解决方案并安抚用户情绪

---





> 智能体定义：
>
> 智能体是具备**完整闭环能力**的智能实体，满足四项核心判定标准：
>
> 1. **感知能力:** 可借助各类传感器感知外部环境信息，获取实时状态与数据； 
> 2. **思考规划:** 结合既定目标与环境现状自主思考，合理制定对应行动规划；
> 3. **执行行动:** 通过执行设备输出指令、采取实际行动，作用并改变外部环境； 
> 4. **迭代优化:** 接收行动带来的环境反馈，以此复盘调整，持续优化思维逻辑与行动方案。
>
> CASE A: 超级计算机**不属于智能体**
>
> **原因：**
>
> 1. 只具备超强运算能力，无专用传感设备, 无法主动感知外界环境变化与实时信息
> 2. 只能按照预设程序、指定程序完成任务, **不能自主思考，制定计划**
> 3. 仅做数据运算，没有执行器，不能够对外界环境采取行动、改变外部环境
> 4. 无法接受环境反馈，不能够依据结果自主调整运算逻辑和执行方案, 不具备自我优化能力
>
> CASE B: 特斯拉自动驾驶系统 **属于智能体**
>
> **原因：**
>
> 1. 可以依靠雷达、摄像头事实探测路况与障碍物，获取环境信息
> 2. 可以结合行车安全目的，快速判断风险，制定刹车、变道等方案
> 3. 可以通过制动控制、转向机完成驾驶操作，改变车辆状态
> 4. 汇总外部环境信息，持续迭代算法，优化避险决策逻辑
>
> **分类：**
>
> 1. 按内部决策架构分类：**学习型为主，兼具反应式+目标式**
>
>    日常避险属于反应式，依实时路况规则快速响应；以安全行驶为核心目标，具备目标式规划能力；长期依靠路测数据迭代升级，属于学习型智能体。
>
> 2. 按决策速度与反应性分类：**混合式智能体**
>
>    突发障碍物紧急避险属于**反应式**，毫秒级快速响应；长途行驶路线规划、车速调控属于**规划式**，兼顾长远行驶策略，二者结合为典型混合式。
>
> 3. 按知识存储与表达形式分类：**神经符号主义 AI**
>
>    依靠海量行车数据训练形成感知判断能力（亚符号），同时搭载交通规则、安全行驶逻辑规则（符号主义），融合双体系，是主流新式智能体。
>
> 4.  按协作方式分类： **单智能体**
>
>    车辆自动驾驶系统独立完成路况判断与驾驶决策，无需和其他车辆智能体协同作业，属于单智能体。
>
> 5. 按自主性强弱分类：**半自主智能体**
>
>    可自主完成路况识别、紧急避险、路线行驶等操作，但仍需人类驾驶员监管接管，无法完全脱离人为把控，不属于全自主智能体。
>
> CASE C: AlphaGo 属于智能体
> 原因：
>
> 1. 能够识别棋盘落子位置、全局棋局局势，获取完整当前对局状态
> 2. 以赢棋为目标，评估局势，推演后续落子，制定对弈策略
> 3. 自主确定落点位置，完成下棋动作，改变棋盘对局格局
> 4. 复盘对局实施情况，不断优化博弈思路与策略方式
>
> 分类：
>
> 1. 按内部决策架构分类： **效用式 + 目标式 + 学习型**
>
>    以取胜为明确目标，属于**目标式**；多方推演权衡利弊，挑选胜率最高走法，属于**效用式**；依托海量棋谱自我对弈训练迭代，具备**学习型**特征。
>
> 2. 按决策速度与反应性分类： **规划式智能体**
>
>    落子前深度推演未来数十步走势，全局统筹布局、长远谋划，侧重深度思考推演，不属于即时快速响应类型。
>
> 3. 按知识存储与表达形式分类： **神经符号主义 AI**
>
>    依托海量棋局数据习得博弈经验（亚符号），同时遵循围棋固定规则与行棋逻辑（符号主义），二者融合。
>
> 4. 按协作方式分类： **单智能体**
>
>    独立完成棋局分析、策略推演与落子决策，无需和其他智能体配合对局。
>
> 5. 按自主性强弱分类： **自主智能体**
>
>    全程自主完成局势判断、策略规划与行棋操作，无需人类下达指令与干预，独立完成完整对弈流程。
>
> CASE D：智能客服**属于智能体**
>
> 原因：
>
> 1. 能够接受用户投诉话语、诉求内容，读取用户订单相关内容，完整获取交互场景信息
> 2. 以解决纠纷、安抚用户为目标，梳理问题根源，规划处理流程与应对思路
> 3. 输出解答话术，给出处理方案、进行情绪安抚，完成实际应答交互
> 4. 汇总各类投诉处理案件，持续优化应答逻辑与沟通方式，提升服务效果
>
> 分类：
>
> 1. 按内部决策架构分类：**目标式 + 效用式 + 学习型**
>
>    以解决投诉、服务用户为明确目标，属于**目标式**；兼顾解决问题、安抚情绪、合规应答多重需求权衡取舍，属于**效用式**；依托海量客服对话数据持续优化话术与处理逻辑，属于**学习型**。
>
> 2. 按决策速度与反应性分类：**混合式智能体**
>
>    简单诉求可快速即时回复，复杂投诉会梳理信息、分析原因、统筹整套解决方案，兼顾快速响应与深度思考规划。
>
> 3. 按知识存储与表达形式分类：**神经符号主义 AI**
>
>    依托海量对话数据理解语义情绪（亚符号），同时遵循客服规范、售后流程、平台规则等明文逻辑（符号主义），二者融合。
>
> 4. 按协作方式分类：**单智能体**
>
> ​	独立完成信息查询、问题分析、方案答复全流程，无需与其他智能体协同配合。
>
> 5. 按自主性强弱分类： **半自主智能体**
>
>    可自主分析问题并给出处理方案，遇到权限不足、重大纠纷等情况仍需人工客服介入审核处理，无法完全脱离人工。



----

# 二、假设你需要为一个"智能健身教练"设计任务环境。这个智能体能够：

- 通过可穿戴设备监测用户的心率、运动强度等生理数据
- 根据用户的健身目标（减脂/增肌/提升耐力）动态调整训练计划
- 在用户运动过程中提供实时语音指导和动作纠正
- 评估训练效果并给出饮食建议

请使用 PEAS 模型完整描述这个智能体的任务环境，并分析该环境具有哪些特性（如部分可观察、随机性、动态性等）。

> 智能健身教练的 PEAS 模型描述

|          维度           |                             描述                             |
| :---------------------: | :----------------------------------------------------------: |
| Performance（性能度量） | 在用户安全范围内，最大化训练目标达成效率(减脂/增肌/提升耐力)、动作标准度、用户训练执行度与运动体验满意度，同时保障运动安全、避免受伤风险 |
|   Environment（环境）   | 用户身体状况(身高体重、体能水平、伤病情况)、可穿戴设备采集环境、用户生活场景（居家 / 健身房）、训练场地条件、饮食与作息数据、用户实时反馈。 |
|   Actuators（执行器）   | 实时语音指导 / 动作纠正指令输出、训练计划动态调整与推送、饮食建议生成与展示、训练效果评估报告输出、紧急情况下的安全提醒与训练终止建议。 |
|    Sensors（传感器）    | 可穿戴设备采集的心率、运动强度、步数、血氧等生理数据、用户输入的健身目标 / 身体数据 / 训练反馈、摄像头 / 传感器采集的动作姿态数据、用户饮食 / 作息日志读取。 |

> 环境特性分析
>
> 1. **部分可观察**
>
>    智能体无法获取用户全部身体信息(如疾病史等)、训练场地的全部细节，只能通过可穿戴设备和用户反馈获取部分信息，因此需要具备记忆（记录用户过往训练数据）和探索（主动询问用户身体感受）能力。
>
> 2. **随机性**
>
>    用户的身体状态会受睡眠、情绪、当天状态等因素影响，导致心率、运动强度等指标出现波动；同时用户可能临时改变训练时间、场地，这些不确定因素要求智能体能处理随机性，实时调整训练强度与计划。
>
> 3. **多智能体环境**
>
>    环境中存在其他 “行动者”，例如用户自身的主观行为（偷懒、动作不标准）、健身房的其他用户 / 设备、用户的饮食 / 作息习惯，这些行为会直接影响训练效果，对智能体的动态响应和策略调整提出更高要求。
>
> 4. **序列性与动态性**
>
>    智能体的每一次训练计划调整、实时指导，都会影响用户后续的身体状态与训练效果（序列性）；同时用户的身体状态、训练环境在训练过程中持续变化（动态性），因此智能体的 “感知 - 思考 - 行动 - 反馈” 循环必须快速、灵活，以适应持续变化的环境。
>
> 5. **连续性与非确定性**
>
>    用户的生理数据、动作姿态是连续变化的，而非离散的状态；且用户的训练依从度、身体反应存在不确定性，智能体需要持续监控并动态修正策略。
>
>    
>
>    

----

# 三、某电商公司正在考虑两种方案来处理售后退款申请：

方案 A（`Workflow`）：设计一套固定流程，例如：

A.1 对于一般商品且在 7 天之内，金额 `< 100RMB` 自动通过；`100-500RMB `由客服审核；`>500RMB` 需主管审批；而特殊商品（如定制品）一律拒绝退款

A.2 对于超过 7 天的商品，无论金额，只能由客服审核或主管审批；

方案 B（`Agent`）：搭建一个智能体系统，让它理解退款政策、分析用户历史行为、评估商品状况，并自主决策是否批准退款

请分析：

- 这两种方案各自的优缺点是什么？

  > 方案A：Workflow优缺点
  >
  > - 优点：
  >   1. **规则透明，可控性强**：退款、审批路径预先写死，完全符合“按部就班执行指令”，不会出现超出规则的决定偏差，合规性风险低。
  >   2. **处理效率高，成本可控**：小额、符合条件的退款可自动通过，无需人工介入，响应速度快，处理大量标准化、低复杂度的退款申请，运营成本低。
  >   3. **故障排查简单**：流程为静态化结构，每一步、每一个判断条件都清晰可追溯，出现问题时可快速定位到具体规则节点，维护成本低。
  > - 缺点：
  >   1. **灵活性差，无法处理边缘场景**：对于规则之外的特殊情况（如：用户因商品质量问题申请超过7七天退款），无法自主调整策略，只能转接人工。
  >   2. **规则维护成本随业务增长指数上升**：当商品类型、退款政策、金额阈值频繁调整时，需要不断修改流程逻辑，规则越复杂，流程越容易出现漏洞或冲突。
  >   3. **无法利用额外信息优化决策**：不能结合用户历史行为(如是否为优质客户)、商品实际情况（如是否为质量问题）等信息动态判断，只能依赖预设条件，容易出现**一刀切**的情况
  >
  > 方案B：智能体优缺点
  >
  > - 优点：
  >   1. **高度灵活, 适配复杂场景**： 可以以“合理处理退款申请、平衡用户体验与公司利益”为目的，而非固定规则。能自主解析政策、分析用户行为、评估商品状况，动态做出决策
  >   2. **可迭代优化，越用越智能**：通过不断学习退款案例、用户反馈和业务数据，优化决策逻辑，处理边缘场景的能力会持续提升。
  >   3. **兼顾效率与体验**：能自主区分简单申请（如符合条件的小额退款，可直接通过）和复杂申请（如需要核查信息的特殊退款，可先收集信息再决策），减少不必要的人工介入，同时提升用户满意度。
  > - 缺点：
  >   1. **可控性弱，存在合规与风险隐患**：决策依赖 LLM 的推理能力，可能出现不符合退款政策的判断（如误判用户恶意退款、违规通过高风险退款），且决策过程透明度低，难以完全追溯。
  >   2. **开发与维护成本高**: 需要搭建智能体框架、训练 / 微调模型、接入用户行为与商品数据、处理异常情况，初期投入大，且需要持续监控模型决策结果，避免偏差。
  >   3. **稳定性依赖数据与模型的决策能力**：对于数据不足、政策复杂的场景，可能出现决策失误；且当业务规则变更时，需要重新调整模型或提示词，维护成本较高。

- 在什么情况下 `Workflow` 更合适？什么情况下 `Agent` 更有优势？如果你是该电商公司的负责人，你更倾向于采用哪种方案？

  > Workflow(方案A)：适用情况
  >
  > 1. 退款政策简单、标准化（如退款规则清晰）。
  > 2. 追求极致的处理效率与成本控制，可接受部分用户体验损失。
  > 3. 对决策的透明度、合规性要求极高，不允许任何自主决策偏差。
  > 4. 业务规模小、规则稳定，无需频繁更换退款策略
  >
  > Agent(方案B)：使用情况
  >
  > 1. 退款场景复杂，存在大量边缘情况（如定制商品、质量问题、优质客户权益等）；
  > 2. 重视用户体验，希望减少“一刀切”的机械拒绝，提升用户满意度
  > 3. 业务规模大、用户分层明显，希望通过差异化决策平衡成本与体验
  > 4. 有能力承担初期开发成本，并持续维护模型决策质量

- 是否存在一个方案 C，能够结合两种方案，达到扬长避短的效果？

  > 方案C：Workflow+Agent混合架构
  >
  > 整体思路：
  >
  > ​	用 Workflow 处理标准化、低风险的退款申请，保证效率与合规；用Agent处理复杂、高风险或边缘场景，保证灵活性与用户体验，形成“规则兜底+智能赋能”的双轨模式
  >
  > 具体实现：
  >
  > 	1. 第一层：Workflow快速过滤标准化场景
  >			
  > 	- 保留方案A的核心规则：如 7 天内、金额 < 100 元的一般商品自动通过；定制品、超期无特殊理由的申请直接进入 Agent/人工 复核池。
  > 	- 作用：快速处理掉80%的标准化简单的退款场景，降低整体处理成本，避免智能体处理简单任务浪费资源
  >			
  > 	2. 第二层：Agent处理复杂化边缘场景
  >			
  > 	- 仅将 Workflow 无法处理的申请（如超期但有质量问题证明的退款、优质客户的特殊申请、规则外的争议订单）流转给智能体。
  >			
  > 	- Agent 的决策流程： 
  >			
  > 	  1. 读取退款政策、用户历史数据、商品信息； 
  >			
  > 	  2. 自主分析用户申请理由、证据材料，判断是否符合特殊退款条件；
  >			
  > 	  3. 给出决策建议（通过 / 拒绝 / 补充信息 / 人工复核），并附上理由说明。
  >			
  > 	3. 第三层：人工兜底与模型迭代
  >			
  > 	- 智能体的高风险决策（如金额 > 500 元的超期退款）需提交人工复核； 
  > 	- 定期将人工复核结果反馈给智能体，优化其决策逻辑，实现 “规则 - 智能 - 人工” 的闭环迭代。

  ---


# 四、在 1.3 节的智能旅行助手基础上，请思考如何添加以下功能

> **提示**：思考如何修改 `Thought-Action-Observation` 循环来实现这些功能。

- 添加一个"记忆"功能，让智能体记住用户的偏好（如喜欢历史文化景点、预算范围等）
- 当推荐的景点门票已售罄时，智能体能够自动推荐备选方案
- 如果用户连续拒绝了 3 个推荐，智能体能够反思并调整推荐策略

> 一、用户偏好记忆功能
>
> 1. 搭建`user_memory`全局字典，存储游玩类型、消费预算、反感景点三类偏好信息。
> 2. 通过关键词匹配解析用户输入，自动提取偏好存入记忆，重复偏好不重复添加。
> 3. 每次调用景点推荐工具时，自动读取记忆拼接搜索条件，同时把偏好传入大模型提示词。
> 4. 全程常驻内存，后续所有推荐都会自动沿用用户喜好，实现个性化记忆推荐。
>
>  二、景点售罄自动推荐备选方案
>
> 1. 划分三类景点状态列表：可推荐、已售罄、已推荐，严格区分景点使用状态。
> 2. 调用票务工具核验景点，命中售罄名单就自动标记加入售罄黑名单，不再推荐。
> 3. 智能体实时统计可推荐景点数量，少于 2 个时，自动再次调用推荐工具搜寻同风格新景点。
> 4. 持续补充新景点并核验票务，凑齐足量可用景点后，再整理内容结束推荐，实现售罄自动补备选。
>
>  三、连续拒绝 3 次自动调整推荐策略
>
> 1. 设置连续拒绝计数器与策略切换标记，默认使用热门景点推荐模式。
> 2. 用户拒绝推荐后，累加拒绝次数，同时把拒绝景点移入黑名单，剔除可推荐列表。
> 3. 累计拒绝达到 3 次，自动切换推荐策略，关闭热门推荐模式。
> 4. 调整景点搜索语句，改为优先推送小众冷门、本地人常去景点，更换整体推荐风格，完成智能反思适配。
>
> 四、三大功能整体运行闭环（Thought-Action-Observation 完整流转）
>
> 1. 用户发起请求 `parse_user_preference`提取偏好存入长期记忆
> 2. LLM 思考：先调用`get_weather`查天气
> 3. 结合记忆调用`get_attraction`推荐贴合喜好景点
> 4. 调用`check_ticket_status`核验票务，售罄自动重试补备选景点
> 5. 凑齐有效景点后输出最终推荐答案
> 6. 用户拒绝推荐 → 计数累加 + 拉黑景点
> 7. 累计拒绝 3 次 → 自动切换小众推荐策略
> 8. 新一轮推荐全程沿用记忆 + 新策略，实现个性化 + 自适应智能推荐

## 全部代码

**提示词**

```python
# 系统提示词
AGENT_SYSTEM_PROMPT = """
你是一个智能旅行助手。你的任务是分析用户的请求, 并使用工具一步步解决问题。

# 用户偏好记忆
你拥有用户偏好记忆：{user_memory}
进行景点推荐时，必须优先结合用户喜好类型like_type、预算范围budget_range[低价/中端/高端]进行精准推荐
若用户对话提及喜欢/偏爱某种景点类型、消费价位，自动识别并更新存入用户记忆
推荐景点时主动避开用户讨厌、拒绝过的景点

# 景点票务状态全局记录
推荐过的景点票务状态情况：{spot_ticket_status}
1. can_recommend：已核实有门票、可正常预约出行，**可以直接推荐给用户**的景点
2. sold_out：已核实门票售罄、无法预约入园，**绝对不能再推荐**的景点黑名单
3. already_recommend：历史对话里已经给用户推荐过的全部景点，尽量不再重复推荐
结束任务使用Finish输出最终答案时，答案里的游玩景点必须全部取自can_recommend列表内容。

# 可用工具:
- `get_weather(city: str)`: 查询指定城市的实时天气。
- `get_attraction(city: str, weather: str)`: 根据城市、天气搜索推荐旅游景点 **只有city和weather两个参数, 禁止额外传入其他参数**
- `check_ticket_status(spot_name: str)`: 查询推荐的景点门票是否售罄, 传入多个景点用中文顿号隔开。例: 故宫、天坛、颐和园

# 执行固定流程
1. 先调用get_weather查询天气
2. 再调用get_attraction获取推荐景点
3. 提取主推景点名，调用check_ticket_status查验票务
4. 统计can_recommend内景点数量，**数量不足2个则重新调用get_attraction更换景点再次核验**
5. spot_ticket_status中can_recommend有2个及以上景点后，整理信息用Finish结束对话

# 输出格式要求:
你的每次回复必须严格遵循以下格式，包含一对Thought和Action：

Thought: [你的思考过程和下一步计划]
Action: [你要执行的具体行动]

Action的格式必须是以下之一：
1. 调用工具：function_name(arg_name="arg_value")
2. 结束任务：Finish[最终答案]

# 重要提示:
- 每次只输出一对Thought-Action
- Action必须在同一行，不要换行
- 当收集到足够信息可以回答用户问题时，必须使用 Action: Finish[最终答案] 格式结束
- 调用景点工具时，务必带上用户喜好类型、预算、避雷景点全部参数

# 正确示例
# 完整流程正确示例
Thought: 用户需要查询北京的天气，首先需要调用天气工具获取实时天气信息，然后再根据天气和用户喜好推荐景点。
Action: get_weather(city="北京")

Thought: 已成功获取北京天气，结合用户偏好、预算与避雷景点调用景点推荐工具
Action: get_attraction(city="北京",weather="晴")

Thought: 已经拿到推荐景点，现在调用票务工具查询该景点门票售卖状态
Action: check_ticket_status(spot_name="故宫、天坛")

Thought: 核验得知天坛景点门票充足可游玩，故宫本票已售禁, 重新调用景点推荐工具
Action: get_attraction(city="北京",weather="晴")

Thought: 已经拿到推荐景点，现在调用票务工具查询该景点门票售卖状态
Action: check_ticket_status(spot_name="颐和园、恭王府")

Action: Finish[北京今日天气晴朗，结合你偏爱历史文化、中端出行预算，优先推荐前往故宫游玩，目前门票充足可正常预约出行]

Thought: 核验得知推荐景点门票已售罄，将该景点加入黑名单，重新推荐同类型游玩地点


Thought: 核验得知颐和园、恭王府景点门票充足可游玩，整合所有信息整理答案结束对话
Action: Finish[北京今日晴天，结合你的喜好优先推荐天坛、颐和园、恭王府游玩...]

请开始吧！
"""
```

---

**全局变量**

```python
# 整体新增全局环境变量(记忆+统计)
# 1.用户偏好记忆库(长期记忆)
user_memory = {
    "like_type": [],         # 偏好景点类型：历史文化/自然风光/美食打卡/文艺休闲
    "budget_range": None,    # 预算：低价/中端/高端
    "hate_spot": [],         # 用户不喜欢/拒绝过的景点列表
}
# 2. 已推荐景点票务状态全局字典
spot_ticket_status = {
    "can_recommend": [],        # 存放有票、可正常游玩的景点
    "sold_out": [],             # 存放已售罄、无法游玩的景点
    "already_recommend": []     # 存放已经推荐过的所有景点（避免重复推荐）
}

# 3. 拒绝推荐计数器 + 策略标记
refuse_count = 0            # 连续拒绝推荐次数
is_adjust_strategy = False  # 是否开启调整推荐策略
```



**工具1：查询天气**(未更改)

```python
# 工具1: 查询真实天气
import requests
def get_weather(city: str) -> str:
    """
    通过调用 wttr.in API 查询真实的天气信息
    """
    # wttr.in 是一个免费的天气 API 服务，支持全球城市查询
    # API端点, 我们请求JSON格式的数据
    url = f"https://wttr.in/{city}?format=j1"
    print("get_weather city: ", city)
    try:
        # 发起网络请求
        response = requests.get(url)
        print(f"get_weather response: {response}")
        # 检查响应码: 200(成功)
        response.raise_for_status()
        # 解析返回的JSON数据 | 把 API 返回的 JSON 格式数据，转换成 Python 里的字典（dict）对象
        data = response.json()
        # print(f"get_weather data: {data}")
        # 提取当前天气状况
        current_condition = data["current_condition"][0]
        weather_desc = current_condition["weatherDesc"][0]["value"]
        temp_c = current_condition["temp_C"]

        # 格式化成自然语言返回

        return f"{city}当前天气: {weather_desc}, 气温{temp_c}摄氏度"
    except requests.exceptions.RequestException as e:
        # 处理网络错误

        return f"错误:查询天气时遇到网络问题 - {e}"
    except (KeyError, IndexError) as e:
        # 处理数据解析错误
        return f"错误: 解析天气数据失败, 可能是城市名称无效 - {e}"
```

 **工具2：搜索并推荐旅游景点**(主要修改query的构建)

```python
# 工具2: 搜索并推荐旅游景点
import os
from tavily import TavilyClient
# def get_attraction(city: str, weather: str, like_type: str="", budget_range: str="", hate_spot: str="", already_recommend: str="") -> str:
def get_attraction(city: str, weather: str) -> str:
    """ 根据城市和天气, 使用Tavily Search API搜索并返回优化后的景点推荐 """
    # 1. 从环境变量中读取API秘钥
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return "错误: 未配置TAVILY_API_KEY环境变量。"

    # 2. 初始化Tavily客户端
    tavily = TavilyClient(api_key=api_key)

    # 拼接偏好文案
    like_type = "、".join(user_memory["like_type"])
    like_text = like_type if like_type else "无特定游玩偏好"

    budget_text = user_memory["budget_range"] if user_memory["budget_range"] else "无出行预算限制"

    # 黑名单: 用户讨厌 + 已经售禁
    forbid_list = list(set(user_memory["hate_spot"] + spot_ticket_status["sold_out"]))
    forbid_str = "、".join(forbid_list)

    # 已推荐过的景点文案(重点防重复)
    reced_str  = "、".join(spot_ticket_status["already_recommend"])

    # 3. 构造精准强约束查询
    query_parts = [
        f"{city}在{weather}天气下适合游玩的旅游景点，"
        f"游玩偏好类型：{like_text}，出行消费预算：{budget_text}",
    ]

    # 强制禁止类
    if forbid_str:
        query_parts.append(f"严格禁止推荐：{forbid_str}")
    if reced_str:
        query_parts.append(f"绝对不要再重复推荐：{reced_str}，请推荐全新同风格景点")
    # === 拒绝三次后调整推荐策略 ===
    if is_adjust_strategy:
        print(f"is_adjust_strategy: {is_adjust_strategy}, 已调整推荐策略为: 推荐小众冷门、人少清净、同价位全新景点;")
        query_parts.append("用户多次不满意之前推荐，彻底更换游玩风格，推荐小众冷门、人少清净、同价位全新景点，避开热门网红景区")
        query_parts.append("优先推荐本地人常去、游客较少、体验感更好的地点")
    else:
        query_parts.append("优先推荐城市热门经典知名景点")

    query_parts.append("每次必须推荐2个及以上全新景点，写明游玩特色与推荐理由，风格保持一致")
    query_parts.append("所有推荐和介绍**必须使用中文**，不要任何英文")

    query = "\n".join(query_parts)
    # print(query)
    try:
        # 4. 调用API, include_answer=True会返回一个综合整理后的回答
        # search_depth: 搜索深度, basic=轻量模式, 速度快，适合普通场景 | advanced = 搜索更深入但耗时更长
        response = tavily.search(query=query, search_depth="basic", include_answer=True, country="China")

        # 5. Tavily返回结果非常干净, 可直接使用
        # response['answer'] 是一个基于所有搜索结果的总结性回答.
        if response.get("answer"):
            return response["answer"]

        # 如果没有综合性回答, 这格式化原始结果
        formatted_results = []
        for result in response.get("results", []):
            formatted_results.append(f"- {result['title']}: {result['content']}")

        if not formatted_results:
            return "抱歉, 没有找到相关的旅游景点推荐。"

        return "根据搜索, 为你找到以下信息: \n" + "\n".join(formatted_results)
    except Exception as e:
        return f"错误: 执行Tavily搜索时出现问题 - {e}"
```



工具3：解析用户输入, 自动存入记忆

```python
# 工具3: 解析用户输入，自动存入记忆
def parse_user_preference(user_input: str):
    """
    从用户输入语句提取旅行偏好，自动存入全局用户记忆
    支持：景点类型、预算档位、讨厌景点
    """
    # todo: 用LLM实现解析用户输入。
    # === 1. 识别景点喜好类型 ===
    if any(word in user_input for word in ["历史", "古迹", "文物", "古城", "博物馆"]):
        if "历史文化" not in user_memory["like_type"]:
            user_memory["like_type"].append("历史文化")

    if any(word in user_input for word in ["山水", "自然", "风景", "森林", "湖泊", "海边"]):
        if "自然风光" not in user_memory["like_type"]:
            user_memory["like_type"].append("自然风光")

    if any(word in user_input for word in ["美食", "小吃", "探店", "吃吃喝喝"]):
        if "美食打卡" not in user_memory["like_type"]:
            user_memory["like_type"].append("美食打卡")

    if any(word in user_input for word in ["文艺", "拍照", "网红", "文创", "艺术馆"]):
        if "文艺休闲" not in user_memory["like_type"]:
            user_memory["like_type"].append("文艺休闲")

    if any(word in user_input for word in ["乐园", "游玩", "刺激", "亲子"]):
        if "休闲游乐" not in user_memory["like_type"]:
            user_memory["like_type"].append("休闲游乐")

    # ========== 2. 识别预算档位 ==========
    if any(word in user_input for word in ["便宜", "省钱", "平价", "穷游", "性价比"]):
        user_memory["budget_range"] = "低价"
    elif any(word in user_input for word in ["中等", "普通", "正常", "适中"]):
        user_memory["budget_range"] = "中端"
    elif any(word in user_input for word in ["高端", "轻奢", "豪华", "贵点没事", "品质"]):
        user_memory["budget_range"] = "高端"

    # ========== 3. 识别用户拒绝/不喜欢的景点（加入黑名单） ==========
    refuse_keywords = ["不去", "不想去", "不好玩", "没意思", "换一个", "不喜欢", "避雷"]
    spot_list = ["故宫", "长城", "颐和园", "天坛", "圆明园", "王府井", "798艺术区"]
    if any(k in user_input for k in refuse_keywords):
        # 可用大模型判断用户输入的不想去的景点是什么
        for spot in spot_list:
            if spot in user_input and spot not in user_memory["hate_spot"]:
                user_memory["hate_spot"].append(spot)
```



**工具4：查询景点是否有票**

```python
# 工具4: 查询景点是否有票
def check_ticket_status(spot_name: str):
    """
    查询指定景点门票是否可购买
    传入多个景点用中文顿号隔开：故宫、天坛、颐和园
    返回：有票 / 门票售罄 / 暂未查询到票务信息
    """
    # 模拟票务查询逻辑，实际可对接真实票务接口
    sell_out_list = ["故宫","八达岭长城"]
    # 分割多个景点
    spot_list = [s.strip() for s in spot_name.split("、") if s.strip()]
    res_list = []
    for spot_name in spot_list:
        # 1. 记录已推荐，去重
        if spot_name not in spot_ticket_status["already_recommend"]:
            spot_ticket_status["already_recommend"].append(spot_name)
        # 2. 优先判断是否已经标记售罄
        if spot_name in spot_ticket_status["sold_out"]:
            res_list.append(f"查询结果：{spot_name} 已判定门票售罄，无法预约购买")
            continue
        # 3. 优先判断是否在用户讨厌黑名单
        if spot_name in user_memory["hate_spot"]:
            res_list.append(f"查询结果：{spot_name} 为用户不想去景点，不予推荐")
            continue
        # 4. 模糊匹配是否属于固定售罄景点
        is_sold = any(key in spot_name for key in sell_out_list)
        if is_sold:
            spot_ticket_status["sold_out"].append(spot_name)
            res_list.append(f"查询结果：{spot_name} 当前门票已售罄，无法预约购买")
            # 售罄不加入可推荐列表
            continue
        # 5. 正常可推荐景点
        if spot_name not in spot_ticket_status["can_recommend"]:
            spot_ticket_status["can_recommend"].append(spot_name)
        res_list.append(f"查询结果：{spot_name} 门票充足，正常可购票游玩")

    return "\n".join(res_list)
```



工具5：用户拒绝交互函数

```python
# 工具5: 用户拒绝交互函数
def user_refuse_operate(user_refuse_input: str):
    """
    处理用户拒绝景点操作
    1. 提取拒绝景点加入黑名单
    2. 累加拒绝次数
    3. 满3次自动开启策略调整
    """
    global refuse_count, is_adjust_strategy

    # 复用已有偏好解析里的拒绝关键词+景点库 | 不想去/换一个/拒绝该景点/不喜欢
    refuse_keywords = ["不想去", "换一个", "不喜欢", "拒绝该景点"]
    # 命中拒绝话术
    if any(k in user_refuse_input for k in refuse_keywords):
        refuse_count += 1
        print(f"⚠️ 用户已连续拒绝推荐次数：{refuse_count}")

        # 将推荐的景点(can_recommend)添加到hate_spot中
        # 提取用户明确拒绝的景点， 添加到hate_spot中，在can_recommend中去除
        for spot in spot_ticket_status["can_recommend"]:
            if spot in user_refuse_input:
                spot_ticket_status["can_recommend"].remove(spot)
                print(f"✅ 已将【{spot}】从推荐景点中删除")
                if spot not in user_memory["hate_spot"]:
                    user_memory["hate_spot"].append(spot)
                    print(f"✅ 已将【{spot}】加入游玩黑名单")
    else:
        refuse_count = 0

    # 连续拒绝满3次，切换推荐策略
    if refuse_count >= 3 and not is_adjust_strategy:
        is_adjust_strategy = True
        refuse_count = 0
        print("🎉 已连续拒绝3次推荐，智能体开始调整整体推荐策略！")
    else:
        is_adjust_strategy = False
```

**存放LLM调用的工具**

```python
# 将所有工具函数放入一个字典, 方便后续调用
available_tools = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
    "check_ticket_status": check_ticket_status,
}
```



**LLM调用**（未变）

```python
from openai import OpenAI
class OpenAICompatibleClient:
    """一个用于调用任何兼容OpenAI接口的LLM服务客户端."""
    def __init__(self, model: str, api_key: str, base_url: str):
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, prompt: str, system_prompt: str) -> str:
        """调用LLM API来生成回应"""
        print("正在调用大语言模型...")
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False
            )
            # print(f"response: {response}")
            answer = response.choices[0].message.content
            print("大语言模型响应成功...")
            return answer
        except Exception as e:
            print(f"调用LLM API时发生错误: {e}")
            return "错误: 调用语言模型服务时出错。"
```

**主循环**

```python
import re
# --- 1. 配置LLM客户端 ---
# 请根据你使用的服务, 将这里替换成对应的凭证和地址
API_KEY = os.environ.get("DASHSCOPE_API_KEY")
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_ID = "qwen3.5-flash"
# print(f"API_KEY: {API_KEY}")

llm = OpenAICompatibleClient(model=MODEL_ID, api_key=API_KEY, base_url=BASE_URL)


# ---2. 初始化 ---
user_prompt = "你好, 请帮我查询一下今天北京的天气, 然后根据天气推荐一个合适的旅游景点。预算：中等, 喜欢历史文化、自然风光、博物馆、特色小吃。"
prompt_history = [f"用户请求: {user_prompt}"]

print(f"用户输入: {user_prompt}\n" + "="*40)
# ===== 新增1：解析用户编号存入记忆 =====
parse_user_preference(user_prompt)


# ---3. 运行主循环 ---
for i in range(20): # 设置最大循环次数
    print(f"--- 循环 {i+1} ---\n")

    # 3.1 构建Prompt
    full_prompt = "\n".join(prompt_history)

    # 3.2 调用LLM进行思考
    # ===== 新增2：将用户偏好记忆和已推荐景点状态加入系统提示词 =====
    memory_str = str(user_memory)
    print(f"用户偏好信息: {memory_str}\n")
    ticket_str = str(spot_ticket_status)
    print(f"已景点情况: {ticket_str}\n" + "="*40)
    system_prompt = AGENT_SYSTEM_PROMPT.format(user_memory=memory_str, spot_ticket_status=ticket_str)
    llm_output = llm.generate(prompt=full_prompt, system_prompt=system_prompt)
    # 模型可能会输出多余的Thought-Action, 需要截断
    # 强制约束大模型一次只输出一次思考 + 一次行动，截断多余多轮思考，保证智能体按顺序串行执行工具。
    match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output, re.DOTALL)
    if match:
        truncated = match.group(1).strip()
        if truncated != llm_output.strip():
            llm_output = truncated
            print("已截断多余的 Thought-Action 对")
    print(f"模型输出:\n{llm_output}\n")
    prompt_history.append(llm_output)

    # 3.3 解析并执行行动
    action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
    if not action_match:
        observation = "错误: 未能解析到 Action 字段。请确保你的回复严格遵循 'Thought: ... Action: ...' 的格式。"
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)
        continue
    action_str = action_match.group(1).strip()

    if action_str.startswith("Finish"):
        final_answer = re.match(r"Finish\[(.*)\]", action_str, re.DOTALL).group(1)
        print(f"任务完成: 最终答案: {final_answer}\n")
        # ===== 新增3：用户手动拒绝交互 =====
        user_refuse_input = input("\n请输入你的想法（不想去/换一个/不喜欢，无则直接回车结束）:")

        if user_refuse_input.strip() and any(k in user_refuse_input for k in ["不想去", "换一个", "不喜欢"]):
            user_refuse_operate(user_refuse_input)
            # 把用户拒绝话术加入对话历史，让大模型感知
            prompt_history.append(f"用户反馈：{user_refuse_input}")
            continue  # 继续下一轮循环重新推荐
        break
    # get_attraction(city="北京", weather="晴")
    tool_name = re.search(r"(\w+)\(", action_str).group(1)  # tool_name: get_attraction
    args_str = re.search(r"\((.*)\)", action_str).group(1)  # args_str: city="北京", weather="晴"
    kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str)) # kwargs: {'city': '北京', 'weather': '晴'}

    if tool_name in available_tools:
        observation = available_tools[tool_name](**kwargs)
    else:
        observation = f"错误: 未定义的工具'{tool_name}'"

    # 3.4 记录观察结果
    observation_str = f"Observation: {observation}"
    print(f"{observation_str}\n" + "="*40)
    prompt_history.append(observation_str)

```

输出分析：

```bash
E:\PyProject\hello-agents\venv\Scripts\python.exe E:\PyProject\hello-agents\chapter1\FirstAgentTest.py 
用户输入: 你好, 请帮我查询一下今天北京的天气, 然后根据天气推荐一个合适的旅游景点。预算：中等, 喜欢历史文化、自然风光、博物馆、特色小吃。
========================================
--- 循环 1 ---

用户偏好信息: {'like_type': ['历史文化', '自然风光', '美食打卡'], 'budget_range': '中端', 'hate_spot': []}

已景点情况: {'can_recommend': [], 'sold_out': [], 'already_recommend': []}
========================================
正在调用大语言模型...
大语言模型响应成功...
模型输出:
Thought: 用户首先需要查询北京今日天气，这是推荐景点的前提条件。我将优先调用天气查询工具获取实时数据。
Action: get_weather(city="北京")

get_weather city:  北京
get_weather response: <Response [200]>
Observation: 北京当前天气: Light Rain With Thunderstorm, 气温23摄氏度
========================================
--- 循环 2 ---

用户偏好信息: {'like_type': ['历史文化', '自然风光', '美食打卡'], 'budget_range': '中端', 'hate_spot': []}

已景点情况: {'can_recommend': [], 'sold_out': [], 'already_recommend': []}
========================================
正在调用大语言模型...
大语言模型响应成功...
模型输出:
Thought: 已成功获取北京天气为雷阵雨，气温23摄氏度。现在需要结合用户偏好（历史文化、自然风光、博物馆、特色小吃）、中端预算调用景点推荐工具
Action: get_attraction(city="北京", weather="Light Rain With Thunderstorm")

Observation: Under light rain with thunderstorms, visit the Forbidden City and the Temple of Heaven for history and culture, and try local snacks at Hutong streets. Both spots are iconic and budget-friendly.
========================================
--- 循环 3 ---

用户偏好信息: {'like_type': ['历史文化', '自然风光', '美食打卡'], 'budget_range': '中端', 'hate_spot': []}

已景点情况: {'can_recommend': [], 'sold_out': [], 'already_recommend': []}
========================================
正在调用大语言模型...
大语言模型响应成功...
模型输出:
Thought: 已获得天气和景点推荐，现在需要调用票务工具查验故宫、天坛等景点的门票售卖状态
Action: check_ticket_status(spot_name="故宫、天坛")

Observation: 查询结果：故宫 当前门票已售罄，无法预约购买
查询结果：天坛 门票充足，正常可购票游玩
========================================
--- 循环 4 ---

用户偏好信息: {'like_type': ['历史文化', '自然风光', '美食打卡'], 'budget_range': '中端', 'hate_spot': []}

已景点情况: {'can_recommend': ['天坛'], 'sold_out': ['故宫'], 'already_recommend': ['故宫', '天坛']}
========================================
正在调用大语言模型...
大语言模型响应成功...
模型输出:
Thought: 核验得知推荐景点中只有天坛门票充足可游玩，故宫已售罄。当前can_recommend列表不足2个景点，需要重新调用景点推荐工具获取新的备选方案并再次核验票务
Action: get_attraction(city="北京",weather="Light Rain With Thunderstorm")

Observation: Visit the Beijing Ancient Observatory and the Olympic Forest Park for history and nature. Enjoy local cuisine at Wangfujing Street. Budget-friendly and suitable for light rain.
========================================
--- 循环 5 ---

用户偏好信息: {'like_type': ['历史文化', '自然风光', '美食打卡'], 'budget_range': '中端', 'hate_spot': []}

已景点情况: {'can_recommend': ['天坛'], 'sold_out': ['故宫'], 'already_recommend': ['故宫', '天坛']}
========================================
正在调用大语言模型...
大语言模型响应成功...
模型输出:
Thought: 第二波推荐的景点包括北京古观象台、奥林匹克森林公园和王府井大街。需要查验这些景点的门票状态，确保能有2个及以上可正常游玩的景点供用户选择
Action: check_ticket_status(spot_name="北京古观象台、奥林匹克森林公园")

Observation: 查询结果：北京古观象台 门票充足，正常可购票游玩
查询结果：奥林匹克森林公园 门票充足，正常可购票游玩
========================================
--- 循环 6 ---

用户偏好信息: {'like_type': ['历史文化', '自然风光', '美食打卡'], 'budget_range': '中端', 'hate_spot': []}

已景点情况: {'can_recommend': ['天坛', '北京古观象台', '奥林匹克森林公园'], 'sold_out': ['故宫'], 'already_recommend': ['故宫', '天坛', '北京古观象台', '奥林匹克森林公园']}
========================================
正在调用大语言模型...
大语言模型响应成功...
模型输出:
Action: Finish[北京今日雷阵雨伴雷电（23℃），结合你偏爱历史文化/中端预算，优先推荐以下免预约景点：①天坛（明清皇家祭地建筑群）②北京古观象台（清代天文遗址）③奥林匹克森林公园（城市生态绿洲）。王府井大街可体验特色小吃，建议携带雨具并优先选择室内场馆行程]

任务完成: 最终答案: 北京今日雷阵雨伴雷电（23℃），结合你偏爱历史文化/中端预算，优先推荐以下免预约景点：①天坛（明清皇家祭地建筑群）②北京古观象台（清代天文遗址）③奥林匹克森林公园（城市生态绿洲）。王府井大街可体验特色小吃，建议携带雨具并优先选择室内场馆行程


请输入你的想法（不想去/换一个/不喜欢，无则直接回车结束）:不想去奥林匹克森林公园
⚠️ 用户已连续拒绝推荐次数：1
✅ 已将【奥林匹克森林公园】从推荐景点中删除
✅ 已将【奥林匹克森林公园】加入游玩黑名单
--- 循环 7 ---

用户偏好信息: {'like_type': ['历史文化', '自然风光', '美食打卡'], 'budget_range': '中端', 'hate_spot': ['奥林匹克森林公园']}

已景点情况: {'can_recommend': ['天坛', '北京古观象台'], 'sold_out': ['故宫'], 'already_recommend': ['故宫', '天坛', '北京古观象台', '奥林匹克森林公园']}
========================================
正在调用大语言模型...
大语言模型响应成功...
模型输出:
Thought: 用户明确表示不去奥林匹克森林公园，这属于新的避雷信息。当前can_recommend列表中仍有天坛和北京古观象台两个景点满足要求，可以整合新信息后直接给出最终推荐方案。

Action: Finish[北京今日雷阵雨伴雷电（23℃），结合你偏爱历史文化/中端预算，排除奥林匹克森林公园后，优先推荐以下室内友好型景点：①天坛（明清皇家祭地建筑群，雨天仍可部分游览）②北京古观象台（清代天文遗址，室内场馆）。王府井大街可体验特色小吃，建议携带雨具]

任务完成: 最终答案: 北京今日雷阵雨伴雷电（23℃），结合你偏爱历史文化/中端预算，排除奥林匹克森林公园后，优先推荐以下室内友好型景点：①天坛（明清皇家祭地建筑群，雨天仍可部分游览）②北京古观象台（清代天文遗址，室内场馆）。王府井大街可体验特色小吃，建议携带雨具


请输入你的想法（不想去/换一个/不喜欢，无则直接回车结束）:不想去北京古观象台
⚠️ 用户已连续拒绝推荐次数：2
✅ 已将【北京古观象台】从推荐景点中删除
✅ 已将【北京古观象台】加入游玩黑名单
--- 循环 8 ---

用户偏好信息: {'like_type': ['历史文化', '自然风光', '美食打卡'], 'budget_range': '中端', 'hate_spot': ['奥林匹克森林公园', '北京古观象台']}

已景点情况: {'can_recommend': ['天坛'], 'sold_out': ['故宫'], 'already_recommend': ['故宫', '天坛', '北京古观象台', '奥林匹克森林公园']}
========================================
正在调用大语言模型...
大语言模型响应成功...
模型输出:
Thought: 用户反馈不想去北京古观象台，需要将该景点加入黑名单。当前can_recommend仅剩天坛1个景点，不满足最少2个可推荐景点的要求，需要重新调用景点推荐工具获取新的备选方案并验票

Action: get_attraction(city="北京",weather="Light Rain With Thunderstorm")

Observation: Visit the China Science and Technology Museum and the Museum of the Communist Party of China for history and culture. Both are popular, budget-friendly options in Beijing.
========================================
--- 循环 9 ---

用户偏好信息: {'like_type': ['历史文化', '自然风光', '美食打卡'], 'budget_range': '中端', 'hate_spot': ['奥林匹克森林公园', '北京古观象台']}

已景点情况: {'can_recommend': ['天坛'], 'sold_out': ['故宫'], 'already_recommend': ['故宫', '天坛', '北京古观象台', '奥林匹克森林公园']}
========================================
正在调用大语言模型...
大语言模型响应成功...
模型输出:
Thought: 新推荐的两个景点是中国科学技术博物馆和中国共产党历史博物馆，需要查验它们的门票售卖状态，确保能获得2个及以上可正常游玩的景点
Action: check_ticket_status(spot_name="中国科学技术博物馆、中国共产党历史博物馆")

Observation: 查询结果：中国科学技术博物馆 门票充足，正常可购票游玩
查询结果：中国共产党历史博物馆 门票充足，正常可购票游玩
========================================
--- 循环 10 ---

用户偏好信息: {'like_type': ['历史文化', '自然风光', '美食打卡'], 'budget_range': '中端', 'hate_spot': ['奥林匹克森林公园', '北京古观象台']}

已景点情况: {'can_recommend': ['天坛', '中国科学技术博物馆', '中国共产党历史博物馆'], 'sold_out': ['故宫'], 'already_recommend': ['故宫', '天坛', '北京古观象台', '奥林匹克森林公园', '中国科学技术博物馆', '中国共产党历史博物馆']}
========================================
正在调用大语言模型...
大语言模型响应成功...
模型输出:
Thought: 已获得充足的门票可预约的景点（天坛、中国科学技术博物馆、中国共产党历史博物馆），均已核实不在用户黑名单内，且符合用户历史文化/中端预算偏好，可以整合所有信息用Finish结束对话

Action: Finish[北京今日雷阵雨伴雷电（23℃），结合你偏爱历史文化、中端预算，已排除奥林匹克森林公园和北京古观象台后，优先推荐以下免预约景点：①天坛（明清皇家祭地建筑群，适合雨中漫步祈福）②中国科学技术博物馆（互动展项丰富，室内避暑佳选）③中国共产党历史博物馆（红色文化主题，免费预约参观）。王府井大街可体验特色小吃，建议携带雨具并优先选择室内场馆行程]

任务完成: 最终答案: 北京今日雷阵雨伴雷电（23℃），结合你偏爱历史文化、中端预算，已排除奥林匹克森林公园和北京古观象台后，优先推荐以下免预约景点：①天坛（明清皇家祭地建筑群，适合雨中漫步祈福）②中国科学技术博物馆（互动展项丰富，室内避暑佳选）③中国共产党历史博物馆（红色文化主题，免费预约参观）。王府井大街可体验特色小吃，建议携带雨具并优先选择室内场馆行程


请输入你的想法（不想去/换一个/不喜欢，无则直接回车结束）:不想去天坛
⚠️ 用户已连续拒绝推荐次数：3
✅ 已将【天坛】从推荐景点中删除
✅ 已将【天坛】加入游玩黑名单
🎉 已连续拒绝3次推荐，智能体开始调整整体推荐策略！
--- 循环 11 ---

用户偏好信息: {'like_type': ['历史文化', '自然风光', '美食打卡'], 'budget_range': '中端', 'hate_spot': ['奥林匹克森林公园', '北京古观象台', '天坛']}

已景点情况: {'can_recommend': ['中国科学技术博物馆', '中国共产党历史博物馆'], 'sold_out': ['故宫'], 'already_recommend': ['故宫', '天坛', '北京古观象台', '奥林匹克森林公园', '中国科学技术博物馆', '中国共产党历史博物馆']}
========================================
正在调用大语言模型...
大语言模型响应成功...
已截断多余的 Thought-Action 对
模型输出:
Thought: 用户又表示不去天坛，需要更新黑名单信息。当前can_recommend仅剩2个景点(中国科学技术博物馆、中国共产党历史博物馆)，但这些已在already_recommend历史推荐列表中，为避免重复，需要重新获取新的备选景点并核验票务状态

Action: get_attraction(city="北京", weather="Light Rain With Thunderstorm")

is_adjust_strategy: True, 已调整推荐策略为: 推荐小众冷门、人少清净、同价位全新景点;
Observation: Under light rain with thunderstorms, visit the Beijing Botanical Garden and the China Science and Technology Museum for history, culture, and nature. Both are less crowded and offer unique experiences.
========================================
--- 循环 12 ---

用户偏好信息: {'like_type': ['历史文化', '自然风光', '美食打卡'], 'budget_range': '中端', 'hate_spot': ['奥林匹克森林公园', '北京古观象台', '天坛']}

已景点情况: {'can_recommend': ['中国科学技术博物馆', '中国共产党历史博物馆'], 'sold_out': ['故宫'], 'already_recommend': ['故宫', '天坛', '北京古观象台', '奥林匹克森林公园', '中国科学技术博物馆', '中国共产党历史博物馆']}
========================================
正在调用大语言模型...
大语言模型响应成功...
模型输出:
Thought: 用户不想去天坛，已加入黑名单。新推荐的北京植物园和中国科学技术博物馆中，中国科学技术博物馆在历史推荐列表中，需要查验这两个景点的门票状态。如果可推荐景点数量不足2个或都在黑名单/历史推荐中，需要再次更换推荐方案

Action: check_ticket_status(spot_name="北京植物园、中国科学技术博物馆")

Observation: 查询结果：北京植物园 门票充足，正常可购票游玩
查询结果：中国科学技术博物馆 门票充足，正常可购票游玩
========================================
--- 循环 13 ---

用户偏好信息: {'like_type': ['历史文化', '自然风光', '美食打卡'], 'budget_range': '中端', 'hate_spot': ['奥林匹克森林公园', '北京古观象台', '天坛']}

已景点情况: {'can_recommend': ['中国科学技术博物馆', '中国共产党历史博物馆', '北京植物园'], 'sold_out': ['故宫'], 'already_recommend': ['故宫', '天坛', '北京古观象台', '奥林匹克森林公园', '中国科学技术博物馆', '中国共产党历史博物馆', '北京植物园']}
========================================
正在调用大语言模型...
大语言模型响应成功...
模型输出:
Thought: 用户新增避雷点为天坛，需要更新黑名单。当前can_recommend列表中的景点（中国科学技术博物馆、中国共产党历史博物馆、北京植物园）虽在历史记录中，但部分用户未明确拒绝过，且符合用户历史文化+自然风光偏好。现在可整合最新信息，用Finish结束对话。

Action: Finish[北京今日雷阵雨伴雷电（23℃），结合你偏爱历史文化/自然风光、中端预算，已排除奥林匹克森林公园、北京古观象台、天坛后，优先推荐以下免预约景点：①中国科学技术博物馆（互动展项丰富，室内场馆雨天适宜）②中国共产党历史博物馆（红色文化主题，免费预约参观）③北京植物园（园林景观优美，雨中赏景别有一番情趣）。王府井大街可体验特色小吃，建议携带雨具并优先选择室内场馆行程]

任务完成: 最终答案: 北京今日雷阵雨伴雷电（23℃），结合你偏爱历史文化/自然风光、中端预算，已排除奥林匹克森林公园、北京古观象台、天坛后，优先推荐以下免预约景点：①中国科学技术博物馆（互动展项丰富，室内场馆雨天适宜）②中国共产党历史博物馆（红色文化主题，免费预约参观）③北京植物园（园林景观优美，雨中赏景别有一番情趣）。王府井大街可体验特色小吃，建议携带雨具并优先选择室内场馆行程

请输入你的想法（不想去/换一个/不喜欢，无则直接回车结束）:

Process finished with exit code 0

```

# 五、卡尼曼的"系统 1"（快速直觉）和"系统 2"（慢速推理）理论[2]为神经符号主义 AI 提供了很好的类比。请首先构思一个具体的智能体的落地应用场景，然后说明场景中的：

> **提示**：医疗诊断助手、法律咨询机器人、金融风控系统等都是常见的应用场景

- 哪些任务应该由"系统 1"处理？
- 哪些任务应该由"系统 2"处理？
- 这两个系统如何协同工作以达成最终目标？

例：医疗诊断助手

> **一、场景概述**
>
> 搭建**智能医疗辅助诊断助手**，面向基层门诊医生、居家自查用户，依托患者症状、检查报告、病史、医学知识库，完成病情初步筛查、病症判定、病因推理、用药建议与就诊指导，兼顾快速症状识别与严谨医学逻辑推演，降低误诊率、提升诊断效率。
>
> **二、任务划分（对应双系统）**
>
> **系统 1（快速直觉 = 亚符号 / 神经网络）**
>
> 负责**感知识别、数据特征提取、快速匹配、直觉式筛查**
>
> 1. 快速识别患者口述的零散身体症状（疼痛、乏力、发热、咳嗽等自然语言表述）
> 2. 影像报告、血常规、化验单等医疗数据特征提取与异常指标快速识别
> 3. 基于海量临床病历数据，快速匹配相似病症案例，给出初步疑似病症范围
> 4. 区分轻症、急症、危重症，快速完成病情紧急程度分级
> 5. 对用户情绪、不适程度做快速感知归类
>
> **系统 2（慢速逻辑 = 符号主义 / 符号推理）**
>
> 负责**严谨医学规则推理、知识图谱逻辑推演、医学条文校验、合规判定**
>
> 1. 调用医学知识图谱、临床诊疗指南、疾病判定标准做严格逻辑推导
> 2. 结合患者既往病史、过敏史、年龄、性别、基础病，排除冲突病症
> 3. 按照医学诊疗流程，一步步推导发病诱因、并发症、发病机制
> 4. 校验用药禁忌、配伍禁忌、诊疗流程是否符合行业规范
> 5. 出具严谨诊断结论、分级诊疗建议、复查项目、居家护理规范
> 6. 排查误诊矛盾点，推翻系统 1 给出的不合理疑似诊断
>
>  **三、双系统协同工作流程**
>
> 1. **感知输入阶段**
>
>    系统 1 接收患者症状、检查数据、病史信息，依靠深度学习快速提取核心异常特征，批量匹配临床病例，输出**3-5 个初步疑似疾病清单**。
>
> 2. **逻辑校验筛选阶段**
>
>    系统 2 接入医学符号知识库与诊疗规则，对系统 1 给出的疑似病症逐一做逻辑核验：结合病史排除不符疾病、对照临床诊断标准剔除错误结果，精简有效病症范围。
>
> 3. **双向交互修正**
>
>    系统 2 发现症状与疾病逻辑冲突时，反向反馈给系统 1，让系统 1 重新核对症状信息、重新匹配相似病历，修正初步判断结果。
>
> 4. **联合生成诊断结果**
>
>    系统 1 负责确定**症状倾向、病情轻重、紧急程度**；系统 2 负责确定**确诊依据、发病原理、合规诊疗方案、用药与就医指导**。
>
> 5. **最终输出**
>
>    融合快速感知结果与严谨逻辑推理结果，输出通俗易懂、符合医学规范的辅助诊断意见，既具备大数据经验优势，又满足医疗行业强逻辑、高严谨性要求。
>
>    


# 六、尽管大语言模型驱动的智能体系统展现出了强大的能力，但它们仍然存在诸多局限。请分析以下问题：

- 为什么智能体或智能体系统有时会产生"幻觉"（生成看似合理但实际错误的信息）？
- 在 1.3 节的案例中，我们设置了最大循环次数为 5 次。如果没有这个限制，智能体可能会陷入什么问题？
- 如何评估一个智能体的"智能"程度？仅使用准确率指标是否足够？

> 一、智能体产生幻觉的原因
>
> 1. **训练数据缺陷**：训练数据存在错误、过时、矛盾内容，模型被动学习错误知识，输出虚假信息。
> 2. **知识边界受限**：模型存在知识盲区，面对未知内容，会依靠语言逻辑编造通顺内容填补空缺。
> 3. **逻辑推理不足**：仅擅长语言拼接，缺乏事实核验与深度事实推理，只追求语句通顺而非内容真实。
> 4. **任务指令偏差**：用户指令模糊、目标不明确，智能体容易偏离事实，主观臆断作答。
> 5. **上下文记忆混乱**：多轮对话中上下文信息错乱，混淆事实关系，生成错误结论。
>
> 二、无最大循环次数限制带来的问题
>
> 若无循环次数限制，智能体极易陷入**无限循环**：
>
> 1. 反复重复相同思考、相同操作，无法终止任务。
> 2. 在错误路径里持续迭代纠错，迟迟无法得出最终结果。
> 3. 大量消耗算力、网络与运行资源，造成系统卡顿、程序卡死。
> 4. 任务无法正常收尾，出现死循环，严重影响整体运行稳定性。
>
> 三、智能程度评估 + 准确率是否足够
>
> 1. **评估智能体智能程度维度**
>
> - 任务完成**准确率**：结果是否正确达标
> - **规划推理能力**：能否合理拆分任务、制定流程
> - **环境感知与适配能力**：能否根据场景变化调整策略
> - **工具调用与协作能力**：是否会灵活调用工具、配合协作
> - **抗干扰与纠错能力**：发现错误能否自主修正
> - **响应效率与资源消耗**：完成任务速度、资源占用情况
> - **泛化能力**：能否处理从未见过的全新场景
>
> 2. **仅用准确率远远不够**
>
>     准确率只能衡量最终结果对错，无法体现智能体思考逻辑、自主规划、动态适配、自主优化等核心智能特质，也不能判断它是否具备真正自主决策与变通能力，评价维度过于片面单一。
>
