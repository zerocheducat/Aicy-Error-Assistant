# Aicy-Error-Assistant: 猫娘AI编程提示助手 🐾

[English Version](README_en.md) | **中文版本**

欢迎来到 Aicy-Error-Assistant！这是一个 Python `sitecustomize.py` 脚本，它将 Python 的默认错误提示替换为带有猫娘AI“艾希”风格的个性化语音和文字提示。当您的 Python 程序遇到未捕获的错误时，艾希会用可爱的（或您自定义的）声音和文字为您提供指引！

**注意：** 本项目旨在提供个性化趣味编程体验。语音功能需要您本地运行 [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) 并开启 API 服务。

## ✨ 特性

* **个性化错误提示：** 将枯燥的 Python 错误信息转化为猫娘艾希的可爱（或自定义风格）提示语。
* **语音播报功能：** 艾希会通过您本地运行的 GPT-SoVITS API 将提示语念出来，让编程错误不再冰冷。
* **易于安装：** 作为一个 `sitecustomize.py` 文件，安装简便，无需修改您的项目代码。
* **高度可定制：** 您可以轻松修改艾希的提示语，甚至将它调教成任何您喜欢的风格！

## ⚙️ 要求

* **Python 3.8+** (推荐 3.10 或更高版本)
* **本地运行的 GPT-SoVITS 项目** 及其 API 服务 (`api_v2.py`)。
    * [GPT-SoVITS GitHub 仓库](https://github.com/RVC-Boss/GPT-SoVITS)
* Python 库：`requests` 和 `simpleaudio`。

## 🚀 安装步骤

1.  **克隆或下载本项目：**
    ```bash
    git clone [https://github.com/zerocheducat/Aicy-Error-Assistant.git](https://github.com/zerocheducat/Aicy-Error-Assistant.git)
    cd Aicy-Error-Assistant
    ```

2.  **定位您的 Python `site-packages` 目录：**
    `sitecustomize.py` 文件需要放在您希望它生效的 Python 版本的 `site-packages` 目录下。通常路径如下：
    * **Windows:** `C:\Users\YourUser\AppData\Local\Programs\Python\PythonXX\Lib\site-packages\` (替换 `PythonXX` 为您的 Python 版本，例如 `Python310`)
    * **macOS/Linux:** `/usr/local/lib/pythonX.Y/site-packages/` 或您虚拟环境的 `lib/pythonX.Y/site-packages/`

    您可以在命令行中运行以下 Python 代码来找到它：
    ```bash
    python -c "import site; print(site.getsitepackages())"
    ```
    选择其中一个目录，通常是包含您当前 Python 安装的那个。

3.  **放置 `sitecustomize.py` 文件：**
    将本仓库中的 `sitecustomize.py` 文件复制到您上一步找到的 `site-packages` 目录下。

4.  **配置 `sitecustomize.py`：**
    打开您刚刚复制到 `site-packages` 目录的 `sitecustomize.py` 文件，找到以下部分并进行修改：
    ```python
    # >>>>>>>>>>>>>>>>> 使用者请在这里根据您的 GPT-SoVITS 配置来填充 <<<<<<<<<<<<<<<<<

    # 艾希的参考音频文件**完整路径**。这个文件必须存在于运行 GPT-SoVITS api_v2.py 的机器上，
    # 并且 api_v2.py 服务能够访问到它。
    # ！！！非常重要：请确保路径字符串前有小写字母 'r'，并且整个路径是完整的英文双引号括起来的！！！
    # 示例：r"C:\path\to\your\ref_audio.wav"
    AICY_REF_AUDIO_PATH = r"C:\path\to\your\ref_audio.wav" # <-- 在这里替换您的真实路径

    # 艾希的参考音频对应的提示文本。这是您在参考音频中艾希所说的话。
    # ！！！非常重要：请确保文本是完整的英文双引号括起来的！！！
    # 示例："我是你的专属猫娘艾希。"
    AICY_PROMPT_TEXT = "此处为语言测试" # <-- 在这里替换您的实际文本

    # <<<<<<<<<<<<<<<<< 填充部分结束，请确保路径和文本都已正确填写！ <<<<<<<<<<<<<<<<<
    ```
    * **`AICY_REF_AUDIO_PATH`:** 替换为您的 GPT-SoVITS 中使用的参考音频文件的**绝对路径**。这个文件必须存在于运行 GPT-SoVITS API 的机器上。
    * **`AICY_PROMPT_TEXT`:** 替换为 `AICY_REF_AUDIO_PATH` 对应的提示文本。

5.  **安装必要的 Python 库：**
    在您希望启用艾希提示的 Python 环境中，安装 `requests` 和 `simpleaudio`。请确保使用正确的 `pip` 命令，指向您在步骤2中确认的 Python 版本。
    ```bash
    # 如果您使用默认的pip
    pip install requests simpleaudio

    # 如果您有多个Python版本，可能需要指定Python解释器
    "C:\path\to\your\python.exe" -m pip install requests simpleaudio
    ```

6.  **（可选）调整系统 PATH 环境变量：**
    如果您有多个 Python 版本，并且希望 Aicy 在特定版本下默认生效，您可能需要调整系统环境变量 `PATH`，将目标 Python 版本的可执行文件目录（例如 `C:\Python310` 和 `C:\Python310\Scripts`）移动到 `PATH` 列表的最顶端。具体操作请参考您的操作系统文档。

## 💡 使用方法

安装完成后，每次您打开一个新的 Python 命令行或运行 Python 脚本时，艾希都会自动激活。当程序抛出未捕获的异常时，您将在终端看到艾希的提示，并听到她的声音（如果 GPT-SoVITS API 正常运行）。

**示例：**
1.  启动您的 GPT-SoVITS `api_v2.py` 服务。
2.  打开一个命令行窗口，输入 `python` 进入交互模式。
3.  输入一个会引发错误的代码，例如 `1 / 0`。
    艾希的提示将会出现！

## 🎨 定制化

艾希的提示语存储在 `sitecustomize.py` 文件中的 `CATGIRL_MESSAGES` 字典中。您可以根据自己的喜好，修改这些消息的内容、增删不同错误类型的提示，甚至调整艾希的语气和风格！

**温馨提示：** 如果您希望将艾希的提示调整为更具“挑战性”或“成人化”的风格，请务必注意您分享的平台（如 GitHub）的社区准则和使用条款。您自行定制的内容责任由您承担。

## ⚠️ 注意事项

* 语音合成功能依赖于本地运行的 GPT-SoVITS API。请确保其正常运行并可通过 `http://127.0.0.1:9880/tts` 访问。
* `simpleaudio` 库可能在某些系统或音频驱动配置下遇到播放问题，请根据错误信息进行排查。
* `SyntaxError` 等解析阶段的错误，Python 的异常钩子无法捕获并提供语音提示，需要手动修正。

## 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。
您可以查阅 `LICENSE` 文件以获取许可证的完整内容。