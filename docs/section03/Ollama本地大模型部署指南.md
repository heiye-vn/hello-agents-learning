# Ollama 本地大模型部署与使用指南

本指南旨在帮助开发者在本地快速安装、部署与调用大语言模型（LLM）。通过 Ollama，你可以轻松在个人电脑上运行开源大模型（如 Qwen2.5、DeepSeek-R1 等），实现零成本、离线且隐私安全的本地 LLM 开发环境。

---

## 一、 Ollama 的安装

Ollama 是一个轻量级、开箱即用的本地大模型运行框架。它为各种操作系统提供了便捷的安装程序。

### 1.1 Windows 环境安装
1. 访问 Ollama 官方网站：[https://ollama.com](https://ollama.com)
2. 点击 **Download for Windows** 下载 `OllamaSetup.exe` 安装包。
3. 双击运行安装包，点击 **Install** 进行一键安装。
4. 安装完成后，Ollama 会在后台自动启动（任务栏右下角会出现 Ollama 图标）。

> [!WARNING]
> **常见报错排查**：若在命令行输入 `ollama` 提示 `'ollama' 不是内部或外部命令`：
> - **原因**：安装完成后旧的终端窗口未刷新系统环境变量。
> - **解决**：关闭当前所有的 PowerShell / CMD 窗口，重新打开一个新的终端窗口即可。

### 1.2 macOS / Linux 环境安装
* **macOS**：在官网下载 `.zip` 压缩包，解压后拖入 `Applications` 应用程序文件夹即可。
* **Linux**：使用官方一键脚本在终端中安装：
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

---

## 二、 模型选择与硬件配置推荐

大语言模型运行时对电脑的 **显存 (VRAM)** 或 **系统内存 (RAM)** 有较严格的要求。选择模型时需特别关注模型的 **`Size / Usage`** 参数：
* **Size**：模型下载保存在本地磁盘的空间大小。
* **Usage**：模型加载并运行推理所需的最低显存/内存空间。

### 2.1 硬件配置与模型匹配表

| 硬件配置类型 | 推荐模型规模 | 典型代表模型 | 运行体验 |
| :--- | :--- | :--- | :--- |
| **轻薄本 / 集显**<br/>(16GB 内存, 无独显) | **1.5B ~ 3B** | `qwen2.5:1.5b`<br/>`qwen2.5:3b` | ⚡ 极其流畅，响应飞快（推荐 3B 作为日常首选） |
| **轻薄本 / 尝试高质**<br/>(16GB 内存, 无独显) | **7B ~ 8B** | `qwen2.5:7b`<br/>`deepseek-r1:7b` | 🐢 纯 CPU/核显计算，吐字偏慢（约 2~5 字/秒），但能力更强 |
| **主流游戏本 / 工作站**<br/>(16GB~32GB 内存 + 8G~12G 显存) | **7B ~ 14B** | `qwen2.5:7b`<br/>`qwen2.5:14b` | 🚀 显卡全加速，响应迅速，逻辑思维能力强 |
| **高端工作站 / Mac 统一内存**<br/>(32GB+ 内存/显存) | **32B ~ 70B** | `qwen2.5:32b`<br/>`qwen2.5:72b` | 💎 接近商业级 API 能力，支持复杂代码与逻辑推理 |

---

## 三、 命令行 (CLI) 部署与模型管理

安装好 Ollama 后，可以使用标准 CLI 命令完成模型的下载、运行、查看与卸载。

### 3.1 运行/部署模型
使用 `ollama run` 命令，若本地不存在该模型，Ollama 会自动从云端 Pull 并直接启动对话：

```bash
# 部署并运行通义千问 3B 模型（强烈推荐 16G 内存电脑使用）
ollama run qwen2.5:3b

# 部署并运行 DeepSeek-R1 7B 思考模型
ollama run deepseek-r1:7b
```

### 3.2 下载模型（不立即运行）
```bash
ollama pull qwen2.5:7b
```

### 3.3 查看本地已下载的模型
```bash
ollama list
```

### 3.4 删除模型（释放磁盘空间）
当某个模型不再使用时，使用 `ollama rm` 进行清理：
```bash
ollama rm qwen2.5:7b
```

---

## 四、 代码中调用与参数调试

Ollama 启动后会在本地后台建立 REST API 服务，默认监听端口为 `http://localhost:11434`。

### 4.1 Python 代码调用 (通过官方 SDK)

首先安装 Ollama 的 Python 客户端：
```bash
pip install ollama
```

在 Python 代码中进行调用并调节参数（以验证和提高回答的准确性）：

```python
import ollama

def generate_answer(prompt: str):
    response = ollama.chat(
        model='qwen2.5:3b',  # 指定本地部署的模型名称
        messages=[
            {
                'role': 'system', 
                'content': '你是一个严谨的 AI 助手。请基于事实回答问题，如果不确定请直说。'
            },
            {
                'role': 'user', 
                'content': prompt
            }
        ],
        # ⚙️ 调参控制区：验证与调优回答的准确性与稳定性
        options={
            'temperature': 0.1,   # 采样温度：0.0~0.2 适合事实/代码回答，降低幻觉；0.7+ 提高创造力
            'seed': 42,           # 固定随机种子：确保相同输入时输出完全可复现
            'top_p': 0.9,         # 核采样阈值
            'num_ctx': 4096,      # 上下文窗口 Token 大小
        }
    )
    return response['message']['content']

if __name__ == '__main__':
    result = generate_answer("请说明大模型采样参数 Temperature 的作用。")
    print(result)
```

### 4.2 Web 前端 / Node.js HTTP 调用

通过标准 `fetch` 接口异步请求本地 Ollama 服务：

```javascript
async function callLocalLLM(prompt) {
  const response = await fetch('http://localhost:11434/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'qwen2.5:3b',
      messages: [
        { role: 'user', content: prompt }
      ],
      stream: false,
      options: {
        temperature: 0.1 // 降温以提高生成准确性
      }
    })
  });
  
  const data = await response.json();
  console.log('AI 回复：', data.message.content);
}
```

---

## 五、 提高模型回答准确性的调参指南

当需要利用本地大模型进行高准确度任务（如代码编写、文档问答、数据提取）时，建议通过 `options` 调整以下参数：

| 参数名 | 参数范围 | 准确性测试建议 | 作用说明 |
| :--- | :--- | :--- | :--- |
| **`temperature`** | `0.0 ~ 2.0` | **`0.0 ~ 0.1`** | 采样温度。值越低越倾向选择高概率词，输出越确定、严谨、事实性高。 |
| **`seed`** | 任意整数 | **固定值（如 `42`）** | 随机种子。固定后每次输入相同的提示词，产生的输出完全一致，适合对比测试。 |
| **`num_ctx`** | `2048 ~ 32768` | **`4096` 或 `8192`** | 模型的上下文窗口大小。过大加重显存负担，过小会导致长对话遗忘。 |
| **`system`** | 文本字符串 | **指定严谨规则** | 设置系统指令（System Prompt），明确限制“禁止捏造，未知需明说”。 |

---

## 六、 进阶配置：修改模型默认存储位置

默认情况下，Ollama 会将模型下载至 C 盘 (`C:\Users\<用户名>\.ollama\models`)。若 C 盘空间紧张，可通过设置环境变量更改存储路径：

1. **Windows 更改路径**：
   - 右键“此电脑” ➔ “属性” ➔ “高级系统设置” ➔ “环境变量”。
   - 在“系统变量”中新建：
     - **变量名**：`OLLAMA_MODELS`
     - **变量值**：`D:\OllamaModels`（你希望存放大模型的目标路径）
   - 确定保存后重新启动 Ollama 软件即可。
