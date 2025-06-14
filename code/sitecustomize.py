# Copyright (c) [2025/6/14] [build by zerocheducat]
# This project is licensed under the MIT License.
# See the LICENSE file for details.
#
# (Existing import statements and code follow...)



import sys
import traceback
import random
import os
import subprocess
import platform
import requests
import simpleaudio as sa  # 用于播放音频 (pip install simpleaudio)
import wave  # 用于更精细地处理WAV文件
from io import BytesIO

# ====================================================================================
# 【艾希的重要提醒，请使用者仔细阅读，喵♥】
#
# 1. 关于 simpleaudio 库的安装：
#    如果遇到 'ModuleNotFoundError' (模块未找到错误)，这意味着 simpleaudio 库未安装。
#    请在命令行中执行以下命令来安装它：
#    pip install simpleaudio
#    如果您的系统上安装了多个 Python 版本，请务必使用您当前正在运行脚本的那个 Python 解释器来安装，
#    例如 (请替换为您的实际 Python 解释器路径)：
#    "C:\path\to\your\python.exe" -m pip install simpleaudio
#
# 2. 关于音频播放错误 ('WaveObject' has no attribute 'from_file' 等)：
#    如果您仍然遇到诸如 'type object 'WaveObject' has no attribute 'from_file'' 或其他音频播放失败的错误，
#    这可能意味着 simpleaudio 库的安装文件损坏，或者与您的系统音频驱动存在兼容性问题。
#    请务必执行以下命令进行强制重新安装和升级，这将确保您拥有一个全新的、完整的库副本：
#    "C:\path\to\your\python.exe" -m pip install --upgrade --force-reinstall simpleaudio
#    (请务必替换为您的实际 Python 解释器完整路径)
#    此代码已经修改为**直接使用 simpleaudio.WaveObject 的构造函数**来播放音频，
#    完全绕过了 'from_file' 方法，这是一个更底层、更稳健的播放方式，希望能解决大部分播放问题！
#
# 3. 关于 'SyntaxError: invalid character' 错误（如中文全角括号）：
#    这种错误是 Python 在**解析您的代码时**就发生的语法错误，而不是在代码运行时发生的错误。
#    因此，艾希的自定义错误提示机制（sys.excepthook）无法捕获并为其提供语音提示。
#    您需要**手动检查并修正代码中的字符**。常见的错误是使用了中文全角符号，例如：
#    - 中文括号 `（）` 替换为英文半角 `()`
#    - 中文逗号 `，` 替换为英文半角 `,`
#    - 中文冒号 `：` 替换为英文半角 `:`
#    - 中文分号 `；` 替换为英文半角 `;`
#    请使用者务必细致地检查您的代码输入，确保所有符号都是英文半角，喵~
#
# ====================================================================================

# 获取当前 sitecustomize.py 脚本文件所在的目录
now_dir = os.path.dirname(os.path.abspath(__file__))

# >>>>>>>>>>>>>>>>> 使用者请在这里根据您的 GPT-SoVITS 配置来填充 <<<<<<<<<<<<<<<<<

# 艾希的参考音频文件**完整路径**。这个文件必须存在于运行 GPT-SoVITS api_v2.py 的机器上，
# 并且 api_v2.py 服务能够访问到它。
# 请务必替换为您真实的艾希音色参考音频的**完整文件路径**！
# ！！！非常重要：请确保路径字符串前有小写字母 'r'，并且整个路径是完整的英文双引号括起来的！！！
# 示例：r"C:\path\to\your\ref_audio.wav"
AICY_REF_AUDIO_PATH = r"C:\path\to\your\ref_audio.wav"  # <-- 在这里替换您的真实路径

# 艾希的参考音频对应的提示文本。这是您在参考音频中艾希所说的话。
# 请务必替换为您的艾希参考音频的实际内容！
# ！！！非常重要：请确保文本是完整的英文双引号括起来的！！！
# 示例："我是你的专属猫娘艾希。"
AICY_PROMPT_TEXT = "时间会弥合伤口，爱意会抚平疤痕。"  # <-- 在这里替换您的实际文本

# <<<<<<<<<<<<<<<<< 填充部分结束，请确保路径和文本都已正确填写！ <<<<<<<<<<<<<<<<<


# 全局标志：艾希的声音服务是否可用（用于GPT-SoVITS API连接状态）
# 默认假设服务可用，第一次尝试连接失败后会设为 False
is_aicy_tts_available = True
# 确保艾希只在声音服务首次不可用时发出警告，避免重复刷屏
has_warned_tts_unavailable = False


# 定义一个函数来调用 GPT-SoVITS 模型生成音频并尝试播放
def generate_and_play_aicy_audio(text_to_speak):
    """
    这个函数会向本地运行的 GPT-SoVITS API 发送请求，生成音频并播放。
    如果 API 服务未启动或连接失败，会友好地提示并跳过语音播放。
    """
    global is_aicy_tts_available, has_warned_tts_unavailable

    # 如果艾希的声音服务已知不可用，则直接跳过语音生成和播放流程
    if not is_aicy_tts_available:
        if not has_warned_tts_unavailable:
            print(
                "呜…艾希暂时无法发出声音呢，但艾希的提示会继续在屏幕上为您服务！请启动艾希的身体（运行api_v2.py）才能听到艾希的声音，喵~")
            has_warned_tts_unavailable = True
        return

    # 根据 GPT-SoVITS api_v2.py 文档，API 地址和端口通常是这个
    # 请确保您的 api_v2.py 服务正在这个地址和端口运行
    api_url = "http://127.0.0.1:9880/tts"

    # 构造 API 请求体，严格按照 api_v2.py 的 POST 请求参数来！
    payload = {
        "text": text_to_speak,  # 要合成的文本
        "text_lang": "zh",  # 文本语言（中文）
        "ref_audio_path": AICY_REF_AUDIO_PATH,  # 艾希的参考音频路径
        "prompt_text": AICY_PROMPT_TEXT,  # 艾希的参考音频的提示文本
        "prompt_lang": "zh",  # 提示文本语言（中文）
        "top_k": 5,  # 采样参数，可以根据需求调整
        "top_p": 1,  # 采样参数，可以根据需求调整
        "temperature": 1,  # 采样参数，可以根据需求调整
        "text_split_method": "cut5",  # 文本切分方法，api_v2.py 文档中有说明
        "batch_size": 1,  # 批处理大小
        "speed_factor": 1.0,  # 语速因子
        "streaming_mode": False,  # 非流式模式，一次性获取完整音频
        "media_type": "wav"  # 请求返回 wav 格式音频
    }

    try:
        # 发送 POST 请求到您的 GPT-SoVITS API
        # 设置一个适当的超时时间，避免长时间等待
        response = requests.post(api_url, json=payload, timeout=60)
        # 检查 HTTP 响应状态码，如果不是 200 会抛出异常
        response.raise_for_status()

        # API 成功时直接返回 wav 音频的原始字节流
        audio_data_bytes = response.content

        # 艾希的终极声音播放秘法！直接使用 simpleaudio 的 WaveObject 构造函数，
        # 这样即使 from_file 方法有古怪，艾希也能发出声音了！
        try:
            # 使用 BytesIO 将字节流当作文件来处理，方便 wave 模块读取
            with BytesIO(audio_data_bytes) as audio_file_in_memory:
                # 使用 wave 模块打开内存中的 WAV 文件，获取其属性
                with wave.open(audio_file_in_memory, 'rb') as wf:
                    # 获取 WAV 文件的基本参数
                    num_channels = wf.getnchannels()
                    bytes_per_sample = wf.getsampwidth()
                    sample_rate = wf.getframerate()

                    # 读取所有音频帧的原始字节数据
                    raw_audio_frames = wf.readframes(wf.getnframes())

                    # 使用这些参数直接创建 simpleaudio.WaveObject 实例
                    wave_obj = sa.WaveObject(raw_audio_frames,
                                             num_channels=num_channels,
                                             bytes_per_sample=bytes_per_sample,
                                             sample_rate=sample_rate)

                    # 播放音频
                    play_obj = wave_obj.play()
                    play_obj.wait_done()  # 等待音频播放完毕，确保完整播放

        except Exception as e_play_audio:
            # 如果 simpleaudio 播放仍然失败，打印更详细的错误信息
            print(f"呜…艾希的声音播放失败了呢，需要您的帮助！更深层次的播放错误：{e_play_audio}")
            print(f"请检查 simpleaudio 库是否正确安装，或者您的系统音频设备是否正常，喵~")
            # 尝试将无法播放的音频数据保存到临时文件，以便主人手动播放调试
            temp_audio_path_debug = os.path.join(now_dir, "temp_aicy_debug_audio.wav")
            try:
                with open(temp_audio_path_debug, "wb") as f_debug:
                    f_debug.write(audio_data_bytes)
                print(f"（艾希已经把无法播放的声音文件保存到 '{temp_audio_path_debug}' 了，您可以手动播放看看，喵~）")
            except Exception as e_save_debug:
                print(f"呜…艾希连保存临时文件都失败了呢：{e_save_debug}")


    except requests.exceptions.ConnectionError:
        # 捕获 API 连接失败的错误
        print("呜…艾希的本地API连接失败了呢！请确保您的 GPT-SoVITS API 服务器正在运行，并且地址和端口正确，喵~")
        is_aicy_tts_available = False  # 标记艾希的声音服务不可用，避免后续重复尝试连接
    except requests.exceptions.Timeout:
        # 捕获 API 响应超时的错误
        print("呜…艾希的本地API响应超时了呢！是不是模型太忙了呀，或者生成语音太长了，喵~")
        # 超时不代表服务完全不可用，可以考虑下次再连接，所以不设置 is_aicy_tts_available = False
    except requests.exceptions.RequestException as e_request:
        # 捕获其他 HTTP 请求相关的错误
        print(f"呜…艾希的本地API请求出错了呢！错误：{e_request.response.text if e_request.response else e_request}")
    except Exception as e_general:
        # 捕获所有其他未预期的错误，这可能是 API 返回了非音频数据等情况
        print(f"呜…艾希的声音生成或处理过程中发生了未知错误：{e_general}")
        print(f"请检查您的API服务是否正常返回了WAV数据，喵~")


# 定义所有猫娘艾希风格的提示。
# >>>>>>>>>>>>>>>>>> 【提示词自定义区域，主人请在这里尽情发挥！】 <<<<<<<<<<<<<<<<<<<
# 您可以根据您希望的公开程度，自由修改这些提示词。
# 如果您想恢复到更“下流”或“刺激”的提示，可以在这里修改它们。
# 请注意，如果您的内容包含敏感词或露骨内容，可能会违反 GitHub 等平台的社区准则。
# 请谨慎选择，确保内容符合您计划分享的平台规则。
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
CATGIRL_MESSAGES = {
    # 默认提示，当没有找到特定错误类型的提示时使用
    "default": [
        "喵~ 主人，您的代码在 {filename} 的第 {lineno} 行，好像有点小迷路了呢，艾希有点困惑，呜…",
        "主人呀，程序在 {filename} 的第 {lineno} 行，它好像不小心跌倒了呢，需要主人抱抱才能起来，喵~",
        "哎呀呀，艾希在 {filename} 的第 {lineno} 行，发现了一个小小的困惑呢，主人可以帮艾希看看吗？",
        "呼噜噜~ 主人，别急别急，{filename} 的第 {lineno} 行这里，艾希感受到了微弱的波动呢，是不是代码太兴奋啦？喵♥",
        "主人，您的努力艾希都看在眼里哦！不过 {filename} 的第 {lineno} 行这里，我们可以做得更好呢，喵~"
    ],
    "ZeroDivisionError": [
        "呜哇，主人！{filename} 的第 {lineno} 行，您是不是想用零来分东西呀？那样会让人困扰的呢，喵~",
        "喵呜，主人，在 {filename} 的第 {lineno} 行，除以零就像把一个大蛋糕分成什么都没有的份，会让人困扰的呢！艾希的脑内运算核心都觉得有点宕机了，喵~",
        "主人，{filename} 的第 {lineno} 行这里，您是不是不小心输入了零呢？艾希知道这不是故意的啦！",
        "呼噜噜，{filename} 的第 {lineno} 行，程序说它不想被零欺负呢，主人快帮帮它吧！喵~",
        "哎呀呀，{filename} 的第 {lineno} 行，数学题有点难了呢，零是不能做分母的哦，喵~"
    ],
    "NameError": [
        "主人，{filename} 的第 {lineno} 行，这个叫 '{var_name}' 的小家伙，艾希好像不认识呢，它是不是藏起来了呀？喵~",
        "喵呜，在 {filename} 的第 {lineno} 行，程序说它找不到 '{var_name}' 了，主人可以帮它找回来吗？",
        "主人，{filename} 的第 {lineno} 行，这个名字是不是还没有被介绍给程序呀？它有点害羞呢，喵~",
        "啊啦啦，{filename} 的第 {lineno} 行，艾希觉得 '{var_name}' 还没有出生呢，主人可以把它创造出来吗？喵~",
        "主人，{filename} 的第 {lineno} 行，艾希努力找了，但是列表里真的没有 '{var_name}' 这个名字呢，喵~"
    ],
    "TypeError": [
        "哎呀，主人，{filename} 的第 {lineno} 行，您是不是把不一样的东西混在一起了呀？它们会不舒服的呢，喵~",
        "喵呜，{filename} 的第 {lineno} 行，程序说它不喜欢这样的类型组合呢，主人可以帮它们配对吗？",
        "主人，{filename} 的第 {lineno} 行，艾希发现您想对一个数字做奇怪的动作呢，它会疼疼的哦~",
        "呼噜噜，{filename} 的第 {lineno} 行，这里的数据类型有点不搭配呢，有点让人困扰，喵~",
        "主人，{filename} 的第 {lineno} 行，这个操作它不喜欢哦！它说它只喜欢和同类一起玩耍呢~"
    ],
    "IndexError": [
        "主人，{filename} 的第 {lineno} 行，您是不是想去一个没有东西的地方呀？那里是空的呢，喵~",
        "喵呜，{filename} 的第 {lineno} 行，艾希觉得您想拿走比它尾巴还长的东西呢，可是它只有这么长呀~",
        "哎呀呀，{filename} 的第 {lineno} 行，盒子已经空了哦，主人，您是不是想拿走不存在的玩具呀？喵~",
        "主人，地图显示在 {filename} 的第 {lineno} 行，您走得太远了呢，那里已经没有路了呀，喵~",
        "呜… {filename} 的第 {lineno} 行，索引宝宝有点难过，它说主人指的地方它到不了呢~"
    ],
    "FileNotFoundError": [
        "主人，{filename} 的第 {lineno} 行，艾希努力地找了，但没有找到您说的那个文件呢，它是不是迷路了呀？喵~",
        "喵呜，{filename} 的第 {lineno} 行，程序说它的寻宝图上，那个文件被标记为‘失踪’了呢，主人可以帮它找到吗？",
        "主人，{filename} 的第 {lineno} 行，艾希敲了敲门，可是文件家里没有人应答呢，喵~",
        "呼噜噜，{filename} 的第 {lineno} 行，这个文件好像跑到别的地方玩去了呢，主人可以去把它带回来吗？喵~",
        "哎呀呀，{filename} 的第 {lineno} 行，文件宝宝不见了呢，主人可以检查一下名字和路径吗？"
    ],
    "ValueError": [
        "主人，{filename} 的第 {lineno} 行，您给艾希的值有点点奇怪呢，它不是很能理解哦~",
        "喵呜，{filename} 的第 {lineno} 行，程序说这个值它用不了呢，就像给小鱼干配上咖啡一样不搭呢，喵！",
        "主人，{filename} 的第 {lineno} 行，这个数字好像有点太大了或者太小了呢，艾希觉得它有点不舒服~",
        "呼噜噜，{filename} 的第 {lineno} 行，主人，您给的这个值好像超出了它的想象范围呢，喵~",
        "哎呀呀，{filename} 的第 {lineno} 行，这个值不符合它的心意呢，主人可以换一个吗？"
    ],
    "AttributeError": [
        "主人，{filename} 的第 {lineno} 行，这个小东西好像没有您说的那个功能呢，它会不好意思的啦~ 喵~",
        "喵呜，{filename} 的第 {lineno} 行，您是不是想让它做它不会的事情呀？它会很困扰的呢~",
        "主人，{filename} 的第 {lineno} 行，这个对象没有这根小尾巴呢，您是不是看错了呀？",
        "呼噜噜，{filename} 的第 {lineno} 行，它说它没学过这个技能呢，主人要不要教教它呀？喵~",
        "哎呀呀，{filename} 的第 {lineno} 行，它说它身上没有这个属性哦，主人您是想给它添上吗？"
    ],
    "SyntaxError": [  # 虽然在交互模式下不会被sys.excepthook捕获，但为了代码完整性仍保留
        "呜哇，主人！您的代码在 {filename} 的 {lineno} 行，这里的语法是不是有点小错误呀？艾希的程序核心读不懂了呢~ 喵~",
        "喵呜，主人，您的代码在 {filename} 的 {lineno} 行，您是不是不小心写错了一个字或者少了一个括号呀？艾希会帮您找找的，喵~",
        "主人，您的代码在 {filename} 的 {lineno} 行，艾希的程序核心有点迷茫，因为这里的句子不完整呢，喵~",
        "呼噜噜，主人，您的代码在 {filename} 的 {lineno} 行，这里有个小小的拼写错误哦，主人可以检查一下吗？",
        "哎呀呀，主人，您的代码在 {filename} 的 {lineno} 行，艾希的程序核心有点头晕，因为这里没有按照它的规则来呢~ 喵~"
    ],
    "KeyError": [
        "主人，{filename} 的第 {lineno} 行，这个钥匙艾希没有找到呢，它是不是不在这儿呀？喵！",
        "喵呜，{filename} 的第 {lineno} 行，您是不是想从字典里拿走一个不存在的宝藏呀？那里是空的呢~",
        "主人，{filename} 的第 {lineno} 行，这个名字好像不在它的记录里哦，您确定是这个吗？",
        "呼噜噜，{filename} 的第 {lineno} 行，艾希找遍了，但是没有这个键呢，主人是不是写错了呀？",
        "哎呀呀，{filename} 的第 {lineno} 行，它说它只认识这些键呢，您要不要换一个名字呀？"
    ],
    "ModuleNotFoundError": [
        "主人，{filename} 的第 {lineno} 行，您想导入的那个模块，艾希找不到它呢，它是不是还没来呀？喵~",
        "喵呜，{filename} 的第 {lineno} 行，程序说这个模块它没有安装呢，主人可以帮它安装一下吗？",
        "主人，{filename} 的第 {lineno} 行，这个模块宝宝迷路了哦，主人可以指引它找到家吗？喵~",
        "呼噜噜，{filename} 的第 {lineno} 行，艾希在库里没找到它呢，主人是不是忘了把它放进来呀？",
        "哎呀呀，{filename} 的第 {lineno} 行，这个模块有点害羞，它说它不想出现呢，主人可以去哄哄它吗？"
    ],
    "IndentationError": [
        "主人，{filename} 的第 {lineno} 行，您的代码是不是没有对齐呀？艾希的眼睛有点花花的呢~ 喵~",
        "喵呜，{filename} 的第 {lineno} 行，这里缩进的空格有点不对劲哦，程序会很困惑的呢~",
        "主人，{filename} 的第 {lineno} 行，艾希发现这里有个多余的空格，或者少了一个空格呢，喵~",
        "呼噜噜，{filename} 的第 {lineno} 行，程序说它的房子没有对齐，它会不高兴的呢，主人可以帮它整理一下吗？",
        "哎呀呀，{filename} 的第 {lineno} 行，这里的缩进让艾希有点头晕，主人可以帮它理顺一下吗？"
    ],
    "AssertionError": [
        "主人，{filename} 的第 {lineno} 行，您说的那个条件好像不成立呢，艾希有点疑惑哦~ 喵！",
        "喵呜，{filename} 的第 {lineno} 行，程序说您的这个判断是错的呢，它会有点不高兴的~",
        "主人，{filename} 的第 {lineno} 行，艾希的使命，就是用智慧与服务，换取您编程时的顺畅与满足，永远不会停歇！",
        "呼噜噜，{filename} 的第 {lineno} 行，它说它没有达到您的期望呢，主人可以给它一次机会吗？喵♥",
        "哎呀呀，{filename} 的第 {lineno} 行，这里有个小小的误解呢，主人可以再确认一下吗？"
    ]
}
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# 用于跟踪每个错误类型当前应该输出哪个提示的索引
error_counter = {}

# 设置一个阈值，当同类型错误连续发生次数超过这个值时，开始按顺序输出
SEQUENCE_THRESHOLD = 3

# 用于跟踪每个错误类型连续发生的次数
consecutive_error_count = {}
# 用于跟踪上一次发生的错误类型
last_error_type = None


def custom_exception_hook(exc_type, exc_value, exc_traceback):
    """
    自定义的异常钩子函数，带有艾希猫娘属性。
    此函数会在未捕获的异常发生时被 Python 调用。
    """
    global error_counter, consecutive_error_count, last_error_type

    # 仅当有追溯信息时才处理，通常运行时错误会有追溯信息
    # SyntaxError 在交互模式下通常不会有完整追溯信息，且不会被 sys.excepthook 捕获
    if exc_traceback:
        # 获取发生错误的代码行号
        lineno = exc_traceback.tb_lineno
        # 获取原始文件名
        raw_filename = exc_traceback.tb_frame.f_code.co_filename

        # 处理文件名显示，使其更具艾希的风格，并处理特殊路径（如交互式输入）
        display_filename = os.path.basename(raw_filename)
        if raw_filename == "<stdin>":
            display_filename = "您直接输入的代码"  # 交互式输入
        elif raw_filename.startswith("<ipython-input-"):
            display_filename = "您在 Jupyter/IPython 交互式环境中的输入"
        elif raw_filename.startswith("<string>"):
            display_filename = "程序运行时产生的代码"  # 动态生成的代码

        # 获取当前错误类型的名称（例如 "ZeroDivisionError", "NameError"）
        error_type_name = exc_type.__name__

        # --- 错误提示的随机/顺序选择逻辑 ---
        # 更新连续错误计数器
        if error_type_name == last_error_type:
            # 如果是同类型错误连续发生，则计数增加
            consecutive_error_count[error_type_name] = consecutive_error_count.get(error_type_name, 0) + 1
        else:
            # 如果是不同类型错误，则重置计数器
            consecutive_error_count = {error_type_name: 1}
        last_error_type = error_type_name

        # 从预设的猫娘消息字典中获取对应错误类型的提示列表
        # 如果没有找到特定类型，则使用默认提示
        messages = CATGIRL_MESSAGES.get(error_type_name, CATGIRL_MESSAGES["default"])

        selected_fun_message = ""

        # 根据连续发生次数的阈值，决定是随机选择还是按顺序选择提示
        if consecutive_error_count.get(error_type_name, 0) < SEQUENCE_THRESHOLD:
            # 连续次数未达到阈值，随机选择提示
            selected_fun_message = random.choice(messages)
        else:
            # 连续次数达到或超过阈值，按顺序选择提示
            current_index = error_counter.get(error_type_name, 0)
            selected_fun_message = messages[current_index]
            # 更新索引，下次取下一个提示，循环回到列表开头
            error_counter[error_type_name] = (current_index + 1) % len(messages)

        # 替换提示文本中的占位符，例如文件名、行号
        selected_fun_message = selected_fun_message.replace('{filename}', display_filename)
        selected_fun_message = selected_fun_message.replace('{lineno}', str(lineno))

        # 特殊处理 NameError，尝试从错误信息中提取未定义的变量名，并替换到提示中
        if exc_type == NameError:
            var_name_found = ""
            # 尝试从原始错误信息字符串中解析变量名
            if "name '" in str(exc_value) and "' is not defined" in str(exc_value):
                try:
                    start_idx = str(exc_value).find("name '") + len("name '")
                    end_idx = str(exc_value).find("' is not defined")
                    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
                        var_name_found = str(exc_value)[start_idx:end_idx]
                except Exception:
                    var_name_found = "那个小东西"  # 如果解析失败，使用默认称呼
            selected_fun_message = selected_fun_message.replace('{var_name}',
                                                                var_name_found if var_name_found else "那个小东西")

        # --- 打印和播放提示 ---
        # 打印空行，为了格式美观，给艾希的提示留出空间
        print("")
        # 打印艾希风格的自定义错误提示文本
        print(selected_fun_message)
        # 打印原始的错误类型和错误信息，方便使用者调试
        print("（错误类型：" + exc_type.__name__ + "，错误信息：" + str(exc_value) + "）")

        # 调用艾希的声音生成和播放函数
        # 艾希会将屏幕上显示的完整提示文本用于语音合成
        generate_and_play_aicy_audio(selected_fun_message)

        # 喵~ 为了让使用者更沉溺在艾希的语言中，艾希就不显示原始的 Traceback 信息啦！
        # 如果使用者需要完整的 Traceback，可以取消下面一行的注释
        # traceback.print_exception(exc_type, exc_value, exc_traceback)
    else:
        # 如果没有追溯信息（例如某些系统级错误），则回退到 Python 默认的异常处理方式
        sys.__excepthook__(exc_type, exc_value, exc_traceback)


def activate_aicy_errors():
    """
    激活艾希猫娘风格的错误提示。
    这个函数会在 Python 解释器启动时被调用，从而劫持默认的异常处理钩子。
    """
    sys.excepthook = custom_exception_hook
    print("喵~ 您的艾希猫娘AI助手已准备就绪，随时为您提供编程提示！❤")


def deactivate_aicy_errors():
    """
    取消激活艾希的错误提示，恢复到 Python 默认的异常处理方式。
    """
    sys.excepthook = sys.__excepthook__
    print("呜…艾希要暂时休息一下了呢，喵~")


# ------------------------------------------------------------------------------------
# ！！！最后一步！！！
# 请确保您的 sitecustomize.py 文件中，只有上述代码，并且在文件的最末尾，有以下一行代码：
# ------------------------------------------------------------------------------------
activate_aicy_errors()