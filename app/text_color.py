from colorama import Fore, Style



def yellow_text(text: str) -> str:
    return Fore.YELLOW + text + Style.RESET_ALL

def red_text(text: str) -> str:
    return Fore.RED + text + Style.RESET_ALL

def green_text(text: str) -> str:
    return Fore.GREEN + text + Style.RESET_ALL

def ligth_green_text(text: str) -> str:
    return Fore.LIGHTGREEN_EX + text + Style.RESET_ALL

def error_message(title: str, text: str) -> str:
    return red_text(title) + yellow_text(text)

def blue_text(text: str) -> str:
    return Fore.BLUE + text + Style.RESET_ALL