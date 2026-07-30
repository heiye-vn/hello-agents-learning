### 一、 专业技能栏（Skill Set）写法示例

在简历的“专业技能”部分，不要只写“了解 Agent”，而是体现出**底层原理 + 生产框架**的深度：

> - **大模型与 Agent 架构**：深入理解大语言模型（LLM） Agent 核心设计范式，熟悉 **ReAct**（Thought-Action-Observation）、**Plan-and-Solve** 及 **Self-Reflection** 自我修正机制；
> - **底层引擎与手撸能力**：具备**从零手写 Agent 引擎**能力，掌握纯 Python 实现 Function Calling 参数解析、结构化 Prompt 约束及工具注册表（Tool Registry）设计；
> - **Memory 与 RAG 增强**：掌握 Agent 短期与长期记忆机制，熟悉基于向量数据库（Chroma/FAISS）的 RAG 上下文增强、历史对话摘要压缩与滑动窗口策略；
> - **主流框架与工程化**：熟练掌握 **LangGraph / LangChain** 的状态管理（StateGraph）与节点调度，具备多智能体（Multi-Agent）路由分发与协同通信的工程落地能力。

---

### 二、 项目经历栏（Project Experience）包装示例

你可以结合 `code/section15` 的综合实战（如智能代码解释器/研报助手/客服 Agent），将项目包装为具备含金量的项目：

#### 📝 项目名称：**基于自研轻量 Agent 引擎的智能研发/研报助手系统**

- **项目描述**：针对复杂多步骤任务处理场景，基于 LLM 与 ReAct 范式搭建的一款高灵活性 Agent 系统。支持动态工具调用、RAG 记忆检索与复杂任务拆解。
- **核心职责与技术实现**：
  1. **底层 Agent 引擎设计**：放弃重型框架依赖，使用纯 Python 手写核心 **ReAct 调度引擎**，实现低延迟的 Thought-Action 循环与流式（Streaming）状态响应；
  2. **工具链与 Function Calling 增强**：设计标准 Tool 注册接口与 JSON Schema 解析器，实现沙箱代码执行、Web 搜索等工具的动态绑定与异常重试（Retry）机制；
  3. **长期记忆与上下文管理**：结合 **Chroma 向量数据库** 实现 Agent 的长期记忆检索（RAG），采用滑动窗口与大模型摘要结合策略，降低 40% 的 Token 消耗并解决长文本遗忘问题；
  4. **任务拆解与多智能体协作**：引入 Router 分发节点与 Sub-Agent 模式，实现复杂大任务向子任务的自动拆解与结果汇聚。

---

### 三、 面试防坑指南（面试官怎么问？你怎么答？）

当你把这些写上简历后，面试官通常会问以下几个深度问题，你可以这样回答：

#### ❓ 面试官问：“你为什么选择自己手写 Agent 引擎，而不是直接用 LangChain？”

>**💡 高分回答**： “LangChain 封装层次很深，在轻量场景或特定定制化业务中存在性能开销和 Debug 困难的问题。我通过手撸 ReAct 循环、Tool 解析与 Memory 机制，彻底搞懂了 Agent 的底层数据流转。在实际生产中，我会根据业务复杂度进行选择——简单低延迟场景使用自研/轻量引擎，复杂图状态流转则使用 LangGraph。”

#### ❓ 面试官问：“Agent 在调用 Tool 时，如果 LLM 返回的 JSON 格式不对/报错了，你怎么处理？”

>**💡 高分回答**： “在手写引擎时我专门设计了**容错与自我修正机制（Self-Correction）**。当工具解析失败时，系统不会直接 Crash，而是把报错信息（Error Traceback）作为 Observation 重新喂给 LLM，触发 LLM 的自我修复重新生成正确的参数，最多重试 3 次；同时在 Prompt 层增加 JSON Schema 严格校验。”

### 💡 总结建议

1. **先手撸完核心代码**：把 `section03`（ReAct）、`section04`（Tool Call）、`section07`（RAG）这几章的代码打通、理解透。
2. **做一个属于你自己的 Agent 小应用**：基于所学知识，改造成一个你自己感兴趣的工具（比如：自动分析 Git Commit 的 Agent、命令行天气与新闻 Agent）。
3. **自信地写上简历**：你不仅懂框架，更懂底层原理，这在当前市场上是非常抢手的 Agent 研发人才！
