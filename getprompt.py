import re
from pathlib import Path

MAIN_PROMPT_FILE = Path("promptLib/mainprompt")
ACCURACY_PROMPT_FILE = Path("promptLib/accuracyprompt")
SUPPORT_PROMPT_FILE = Path("promptLib/supportprompt")


def _get_section(filePath,title: str) -> str:
    text = filePath.read_text(encoding="utf-8")
    pattern = rf"{title}:\s*\"\"\"\s*(.*?)\s*\"\"\""
    match = re.search(pattern, text, re.S)
    if not match:
        raise ValueError(f"Section '{title}' not found in prompt.lib")
    return match.group(1).strip()

def get_prompt_titles() -> list[str]:
    text = SUPPORT_PROMPT_FILE.read_text(encoding="utf-8")
    titles = re.findall(
        r'^\s*(.+?)\s*:\s*\n\s*"""',
        text,
        re.MULTILINE
    )
    return [t.strip() for t in titles]

def get_main_prompt() -> str:
    return _get_section(MAIN_PROMPT_FILE, "擷取題目")

def get_accuracy_prompt() -> str :
    return _get_section(ACCURACY_PROMPT_FILE,"增加精準度")

def get_support_prompt(title) -> str :
    return _get_section(SUPPORT_PROMPT_FILE, title)