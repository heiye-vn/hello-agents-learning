# Hello-Agents 智能体学习与实践仓库 🤖

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Upstream Repo](https://img.shields.io/badge/Source-Datawhale%2Fhello--agents-orange.svg)](https://github.com/datawhalechina/hello-agents)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

本仓库是基于 Datawhale 开源项目 **[Hello-Agents](https://github.com/datawhalechina/hello-agents)** 的学习与实践记录项目。采用 **Python** 语言，深入剖析大语言模型智能体（LLM Agent）的核心概念、设计模式、组件实现与多智能体协作实战。

---

## 📌 项目简介

随着大语言模型（LLM）的快速发展，Agent（智能体）已成为连接 LLM 与真实世界的关键桥梁。本项目旨在通过手写代码与动手实践，循序渐进地掌握 Agent 的底层工作原理与高级应用范式。

### 🎯 学习目标

- **原理透视**：理解 Agent 的核心要素（LLM 大脑、记忆 Memory、工具 Tool、规划 Planning）。
- **组件手撸**：从零构建 ReAct 框架、Function Calling 解析器、Vector DB 记忆检索等核心模块。
- **架构设计**：掌握单智能体（Single-Agent）与多智能体（Multi-Agent）协作系统的设计范式。
- **项目实战**：结合现实场景打造具备自我迭代、工具调用与任务拆解能力的智能体应用。

---

## 📚 目录结构与学习路线

本仓库按功能模块规划学习路径如下：

```plaintext
hello-agents-learning/
├── code/
│   ├── section01/        # 01. Agent 简介与大模型基础
│   ├── section02/        # 02. Prompt 工程与结构化输出
│   ├── section03/        # 03. 纯 Python 手写 ReAct 智能体
│   ├── section04/        # 04. 工具调用机制 (Function Calling / Tool Use)
│   ├── section05/        # 05. 自定义工具与 API 集成扩展
│   ├── section06/        # 06. 智能体短期与长期记忆机制
│   ├── section07/        # 07. 结合向量数据库的 RAG 记忆增强
│   ├── section08/        # 08. 思维链与推理规划 (CoT / ToT)
│   ├── section09/        # 09. 复杂任务拆解与子任务调度
│   ├── section10/        # 10. 智能体评估与自我修正 (Self-Reflection)
│   ├── section11/        # 11. 多智能体基础与通信机制
│   ├── section12/        # 12. 多智能体协作范式 (GroupChat / Router)
│   ├── section13/        # 13. 开源 Agent 框架实战应用
│   ├── section14/        # 14. Agent 部署与 API 服务化 (FastAPI/Streamlit)
│   ├── section15/        # 15. 综合项目实战 (智能代码解释器 / 研报助手)
│   └── section16/        # 16. 前沿探索与生态演进 (MCP / Agentic Workflow)
├── docs/                 # 学习笔记与章节内容
├── .env.example          # 环境变量配置模板
├── .gitignore            # Git 忽略规则
├── requirements.txt      # 全局通用依赖清单
└── README.md             # 项目说明文档
```

---

## 🚀 快速开始

### 1. 环境准备

确保已安装 Python 3.10 或更高版本。建议使用 `venv` 或 `conda` 创建隔离虚拟环境：

```bash
# 创建并激活虚拟环境 (Windows PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 2. 安装依赖

您既可以一次性安装项目根目录的**全局通用依赖**，也可以按需进入各章节目录单独安装**章节独立依赖**：

```bash
# 方式 A：安装全局通用依赖（推荐）
pip install -r requirements.txt

# 方式 B：单独安装具体章节的依赖 (例如 section01)
pip install -r code/section01/requirements.txt
```

### 3. 配置 API Key

拷贝环境变量模板文件并配置相应的大模型 API Key：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填充对应服务商的 Key（如 OpenAI、DeepSeek、智谱 AI 或 DashScope 等）：

```ini
# .env 示例
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# 可选：其他模型 API Key
DEEPSEEK_API_KEY=your_deepseek_api_key
ZHIPUAI_API_KEY=your_zhipu_api_key
```

---

## 🛠️ 技术栈

| 类别                | 技术 / 库                          |
| :------------------ | :--------------------------------- |
| **编程语言**        | Python 3.10+                       |
| **LLM 接口**        | OpenAI SDK, LangChain / LlamaIndex |
| **数据校验 & 配置** | Pydantic v2, python-dotenv         |
| **向量存储 & 检索** | ChromaDB / FAISS                   |
| **工具与部署**      | FastAPI, Streamlit (可选 UI 展示)  |

---

## 📖 学习日志

| 日期       | 模块       | 学习内容 / 产出                    |   状态    |
| :--------- | :--------- | :--------------------------------- | :-------: |
| 2026-07-23 | 项目初始化 | 创建仓库与架构规划 README.md       |  已完成   |
| -          | section01  | Agent 基础与 Prompt 工程实践       | 🔲 计划中 |
| -          | section02  | ReAct 模式原理与纯 Python 手写实现 | 🔲 计划中 |

> [!TIP]
> 建议在学习过程中同步在 `docs/` 目录下记录思考与踩坑经验。

---

## 🙏 致谢与参考

- **上游 GitHub 仓库**：[datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)
- **Datawhale 开源社区**：感谢 Datawhale 社区贡献的高质量开源 Agent 教程！

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 协议。
