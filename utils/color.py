RESET = "\033[0m"

_FG = {
    "black":          30,
    "red":            31,
    "green":          32,
    "yellow":         33,
    "blue":           34,
    "magenta":        35,
    "cyan":           36,
    "white":          37,
    "gray":           90,
    "grey":           90,
    "bright_red":     91,
    "bright_green":   92,
    "bright_yellow":  93,
    "bright_blue":    94,
    "bright_magenta": 95,
    "bright_cyan":    96,
    "bright_white":   97,
    "purple":         35,
    "pink":           95,
}

_BG = {k: v + 10 for k, v in _FG.items()}

_STYLES = {
    "bold":          1,
    "dim":           2,
    "italic":        3,
    "underline":     4,
    "blink":         5,
    "reverse":       7,
    "strikethrough": 9,
}

def colorize(text: str, fg: str = None, bg: str = None, **styles) -> str:
    codes = []

    if fg:
        code = _FG.get(fg.lower())
        if code is None:
            raise ValueError(f"Unknown fg color: {fg!r}. Available: {', '.join(_FG)}")
        codes.append(code)

    if bg:
        code = _BG.get(bg.lower())
        if code is None:
            raise ValueError(f"Unknown bg color: {bg!r}. Available: {', '.join(_BG)}")
        codes.append(code)

    for style, enabled in styles.items():
        if not enabled:
            continue
        code = _STYLES.get(style.lower())
        if code is None:
            raise ValueError(f"Unknown style: {style!r}. Available: {', '.join(_STYLES)}")
        codes.append(code)

    if not codes:
        return text

    seq = ";".join(str(c) for c in codes)
    return f"\033[{seq}m{text}{RESET}"
