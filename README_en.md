# Aicy-Error-Assistant: Catgirl AI Programming Assistant 🐾

[中文版本](README.md) | **English Version**

Welcome to Aicy-Error-Assistant! This is a Python `sitecustomize.py` script designed to replace Python's default error messages with personalized voice and text prompts from your very own Catgirl AI, "Aicy." When your Python program encounters an unhandled error, Aicy will charmingly (or with a custom tone, as per your preference) guide you through it!

**Note:** This project aims to provide a fun and personalized coding experience. The voice synthesis feature requires you to have a local [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) instance running with its API service enabled.

## ✨ Features

* **Personalized Error Prompts:** Transforms dry Python error messages into engaging and customized prompts from Aicy.
* **Voice Playback:** Aicy will read out the error messages using your local GPT-SoVITS API, making debugging a more lively experience.
* **Easy Installation:** As a `sitecustomize.py` file, it's simple to install and requires no modifications to your existing project code.
* **Highly Customizable:** You can easily modify Aicy's prompts, tailoring them to any style you desire!

## ⚙️ Requirements

* **Python 3.8+** (Python 3.10 or newer is recommended)
* **A local GPT-SoVITS project** with its API service (`api_v2.py`) running.
    * [GPT-SoVITS GitHub Repository](https://github.com/RVC-Boss/GPT-SoVITS)
* Python libraries: `requests` and `simpleaudio`.

## 🚀 Installation Steps

1.  **Clone or Download this Repository:**
    ```bash
    git clone [https://github.com/zerocheducat/Aicy-Error-Assistant.git](hhttps://github.com/zerocheducat/Aicy-Error-Assistant.git)
    cd Aicy-Error-Assistant
    ```

2.  **Locate Your Python `site-packages` Directory:**
    The `sitecustomize.py` file must be placed in the `site-packages` directory of the specific Python version you wish to enable Aicy for. Common paths are:
    * **Windows:** `C:\Users\YourUser\AppData\Local\Programs\Python\PythonXX\Lib\site-packages\` (Replace `PythonXX` with your Python version, e.g., `Python310`)
    * **macOS/Linux:** `/usr/local/lib/pythonX.Y/site-packages/` or your virtual environment's `lib/pythonX.Y/site-packages/`

    You can find this directory by running the following Python code in your terminal:
    ```bash
    python -c "import site; print(site.getsitepackages())"
    ```
    Choose one of the listed directories, usually the one corresponding to your active Python installation.

3.  **Place the `sitecustomize.py` File:**
    Copy the `sitecustomize.py` file from this repository into the `site-packages` directory you found in the previous step.

4.  **Configure `sitecustomize.py`:**
    Open the `sitecustomize.py` file you just copied to your `site-packages` directory. Find the following section and modify it:
    ```python
    # >>>>>>>>>>>>>>>>> User: Please fill in your GPT-SoVITS configuration here <<<<<<<<<<<<<<<<<

    # The **full path** to Aicy's reference audio file. This file must exist on the machine
    # running the GPT-SoVITS api_v2.py and be accessible by the api_v2.py service.
    # !!! IMPORTANT: Ensure the path string is prefixed with a lowercase 'r' and enclosed in double quotes !!!
    # Example: r"C:\path\to\your\ref_audio.wav"
    AICY_REF_AUDIO_PATH = r"C:\path\to\your\ref_audio.wav" # <-- REPLACE with your actual path

    # The prompt text corresponding to Aicy's reference audio. This is what Aicy says in your reference audio.
    # !!! IMPORTANT: Ensure the text is enclosed in double quotes !!!
    # Example: "I am your exclusive catgirl Aicy."
    AICY_PROMPT_TEXT = "This is a language test." # <-- REPLACE with your actual text

    # <<<<<<<<<<<<<<<<< Configuration section ends. Please ensure path and text are correct! <<<<<<<<<<<<<<<<<
    ```
    * **`AICY_REF_AUDIO_PATH`:** Replace this with the **absolute path** to the reference audio file used by your GPT-SoVITS. This file must be accessible by the `api_v2.py` service.
    * **`AICY_PROMPT_TEXT`:** Replace this with the exact text spoken in the `AICY_REF_AUDIO_PATH` file.

5.  **Install Necessary Python Libraries:**
    In the Python environment where you want Aicy's prompts to be active, install `requests` and `simpleaudio`. Ensure you use the `pip` command corresponding to the Python version confirmed in Step 2.
    ```bash
    # If using the default pip
    pip install requests simpleaudio

    # If you have multiple Python versions, you might need to specify the interpreter
    "C:\path\to\your\python.exe" -m pip install requests simpleaudio
    ```

6.  ** (Optional) Adjust System PATH Environment Variable:**
    If you have multiple Python versions and wish for Aicy to default to a specific one, you might need to adjust your system's `PATH` environment variable. Place the executable directory of your target Python version (e.g., `C:\Python310` and `C:\Python310\Scripts`) at the very top of your `PATH` list. Refer to your operating system's documentation for detailed instructions.

## 💡 Usage

Once installed, Aicy will automatically activate every time you open a new Python command line or run a Python script. When your program encounters an unhandled exception, you will see Aicy's custom prompt in the terminal, and hear her voice (if the GPT-SoVITS API is running correctly).

**Example:**
1.  Start your GPT-SoVITS `api_v2.py` service.
2.  Open a new command line window and type `python` to enter interactive mode.
3.  Type a piece of code that will cause an error, e.g., `1 / 0`.
    Aicy's prompt will appear!

## 🎨 Customization

Aicy's prompt messages are stored in the `CATGIRL_MESSAGES` dictionary within the `sitecustomize.py` file. You are free to modify the content of these messages, add/remove prompts for different error types, or even adjust Aicy's tone and style to your liking!

**Important Note:** If you choose to customize Aicy's prompts to include more explicit or adult-oriented content, please be mindful of the community guidelines and terms of service of the platform you are sharing on (e.g., GitHub). You are solely responsible for the content you customize and publish.

## ⚠️ Important Considerations

* The voice synthesis function relies on a locally running GPT-SoVITS API. Please ensure it is running correctly and accessible at `http://127.0.0.1:9880/tts`.
* The `simpleaudio` library might encounter playback issues on certain systems or with specific audio driver configurations. Please refer to any error messages for troubleshooting.
* Syntax errors (like `SyntaxError`) that occur during the parsing stage cannot be caught by Python's exception hook and thus will not trigger Aicy's voice prompts. These errors need to be manually corrected.

## License

This project is licensed under the [MIT License](LICENSE).
See the `LICENSE` file for the full license text.