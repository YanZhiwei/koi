import os
import winreg as reg


def get_chrome_path_windows() -> str:
    try:
        # 尝试从注册表获取 Chrome 安装路径
        chrome_reg_path = (
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
        )
        reg_key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, chrome_reg_path, 0, reg.KEY_READ)
        chrome_path, _ = reg.QueryValueEx(reg_key, "")
        reg.CloseKey(reg_key)
        return chrome_path
    except FileNotFoundError:
        return None


def get_chrome_path_linux() -> None:
    possible_paths = [
        "/usr/bin/google-chrome",
        "/usr/local/bin/google-chrome",
        "/opt/google/chrome/google-chrome",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    return None
