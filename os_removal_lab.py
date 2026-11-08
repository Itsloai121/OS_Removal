#!/usr/bin/env python3
"""OS Removal Lab — a safe, non-destructive operating-system impact simulator.

This educational tool intentionally does not delete files, modify system settings,
run shell commands, or attempt privilege escalation.
"""

from __future__ import annotations

import os
import platform
import sys
import textwrap
from typing import Optional


# ---------- Cross-platform terminal styling ----------
class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    MAGENTA = "\033[95m"


def enable_windows_ansi() -> None:
    """Enable ANSI escape sequences in modern Windows consoles when possible."""
    if os.name != "nt":
        return
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        mode = ctypes.c_uint()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
    except Exception:
        # Styling is optional; the program remains usable without it.
        pass


def clear_screen() -> None:
    # Avoid invoking `clear` / `cls` through a shell.
    print("\033[2J\033[H", end="")


def terminal_width() -> int:
    try:
        return max(60, min(os.get_terminal_size().columns, 100))
    except OSError:
        return 80


def line(char: str = "─", color: str = Style.CYAN) -> str:
    return color + char * terminal_width() + Style.RESET


def say(text: str = "", color: str = Style.WHITE, *, bold: bool = False) -> None:
    prefix = Style.BOLD if bold else ""
    print(f"{prefix}{color}{text}{Style.RESET}")


def wrapped(text: str, *, color: str = Style.WHITE, indent: str = "  ") -> None:
    width = max(40, terminal_width() - len(indent) - 2)
    for item in textwrap.wrap(text, width=width):
        say(indent + item, color)


# ---------- Environment / privilege detection (read-only) ----------
def host_os_name() -> str:
    if sys.platform.startswith("win"):
        return "Windows"
    if sys.platform.startswith("linux"):
        return "Linux"
    return platform.system() or "Unknown"


def privilege_status() -> str:
    """Return the current process privilege level without changing it."""
    if os.name == "nt":
        try:
            import ctypes

            is_admin = bool(ctypes.windll.shell32.IsUserAnAdmin())  # type: ignore[attr-defined]
            return "Administrator" if is_admin else "Standard user (not Administrator)"
        except Exception:
            return "Unable to determine Windows privilege level"

    geteuid = getattr(os, "geteuid", None)
    if callable(geteuid):
        try:
            return "root (UID 0)" if geteuid() == 0 else f"standard user (UID {geteuid()})"
        except OSError:
            return "Unable to determine Linux privilege level"
    return "Privilege check not supported on this platform"


PLATFORM_DETAILS = {
    "Windows": {
        "target": r"C:\Windows\System32",
        "description": (
            "System32 contains essential Windows executables, libraries, drivers, and "
            "components used to boot and operate the system. Removing it would make "
            "Windows unusable and could prevent recovery or startup."
        ),
        "effects": [
            "Core Windows programs and services may stop working.",
            "Drivers and system libraries may become unavailable.",
            "Windows may fail to boot or become unrecoverable without repair media.",
        ],
    },
    "Linux": {
        "target": "/ (the root filesystem)",
        "description": (
            "A Linux installation is made up of many critical directories. Broadly "
            "removing the root filesystem would destroy the operating system, including "
            "programs, configuration, libraries, boot files, and user data."
        ),
        "effects": [
            "Core commands and shared libraries may disappear.",
            "System configuration, services, and package data may be lost.",
            "The machine may fail to boot and user data may be permanently destroyed.",
        ],
    },
}


def header() -> None:
    clear_screen()
    width = terminal_width()
    title = "OS REMOVAL LAB"
    subtitle = "SAFE IMPACT SIMULATOR  •  WINDOWS / LINUX"
    say("╔" + "═" * (width - 2) + "╗", Style.CYAN, bold=True)
    say("║" + title.center(width - 2) + "║", Style.CYAN, bold=True)
    say("║" + subtitle.center(width - 2) + "║", Style.BLUE)
    say("╚" + "═" * (width - 2) + "╝", Style.CYAN, bold=True)
    print()
    say("  [!] SIMULATION ONLY — no files are deleted and no privileges are escalated.", Style.YELLOW, bold=True)
    print(line())


def pause() -> None:
    try:
        input(f"\n{Style.DIM}  Press Enter to return to the menu...{Style.RESET}")
    except (EOFError, KeyboardInterrupt):
        pass


def show_menu() -> Optional[str]:
    header()
    say("  SELECT A PLATFORM", Style.WHITE, bold=True)
    print()
    say("    [1]  Windows  — simulate the impact of removing System32", Style.CYAN, bold=True)
    say("    [2]  Linux    — simulate the impact of removing the root filesystem", Style.MAGENTA, bold=True)
    say("    [Q]  Quit", Style.DIM)
    print()
    say(f"  Detected host: {host_os_name()}  |  Current privilege: {privilege_status()}", Style.GREEN)
    print(line())
    try:
        choice = input("  Choose [1/2/Q]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return None
    if choice == "1":
        return "Windows"
    if choice == "2":
        return "Linux"
    return None if choice in {"q", "quit", "exit"} else "INVALID"


def show_platform(platform_name: str) -> None:
    details = PLATFORM_DETAILS[platform_name]
    header()
    say(f"  {platform_name.upper()} — IMPACT PREVIEW", Style.WHITE, bold=True)
    print()
    say("  Critical target (display only):", Style.DIM)
    say(f"    {details['target']}", Style.RED, bold=True)
    print()
    wrapped(details["description"])
    print()
    say("  POTENTIAL CONSEQUENCES", Style.YELLOW, bold=True)
    for effect in details["effects"]:
        say(f"    • {effect}", Style.WHITE)
    print()
    say("  CURRENT ENVIRONMENT", Style.CYAN, bold=True)
    say(f"    Host OS:       {host_os_name()}", Style.WHITE)
    say(f"    Privilege:     {privilege_status()}", Style.WHITE)
    if host_os_name() != platform_name:
        say("    Note:          You selected a different OS; this is a conceptual preview only.", Style.YELLOW)
    print(line())
    say("  SAFE SIMULATION", Style.GREEN, bold=True)
    say("  Type SIMULATE to view the non-destructive workflow, or press Enter to go back.", Style.DIM)
    try:
        confirmation = input("  > ").strip()
    except (EOFError, KeyboardInterrupt):
        return
    if confirmation == "SIMULATE":
        run_simulation(platform_name, details["target"])
        pause()


def run_simulation(platform_name: str, target: str) -> None:
    steps = [
        ("Platform selection", "Complete"),
        ("Critical system target identification", "Complete"),
        ("Privilege inspection (read-only)", "Complete"),
        ("Destructive operation", "BLOCKED by design"),
        ("Privilege escalation", "NOT ATTEMPTED"),
        ("System files changed", "0"),
    ]
    print()
    say("  SIMULATION REPORT", Style.GREEN, bold=True)
    say(f"  Selected platform: {platform_name}", Style.WHITE)
    say(f"  Target examined:   {target}", Style.WHITE)
    print()
    for label, status in steps:
        color = Style.RED if status in {"BLOCKED by design", "NOT ATTEMPTED"} else Style.GREEN
        if status == "0":
            color = Style.GREEN
        say(f"    {label:<39} {status}", color)
    print()
    say("  Result: simulation finished. Your operating system was not modified.", Style.GREEN, bold=True)


def main() -> int:
    enable_windows_ansi()
    while True:
        choice = show_menu()
        if choice is None:
            clear_screen()
            say("OS Removal Lab closed. No system changes were made.", Style.GREEN, bold=True)
            return 0
        if choice == "INVALID":
            say("  Invalid choice. Select 1, 2, or Q.", Style.RED)
            pause()
            continue
        show_platform(choice)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\n  Exiting safely. No system changes were made.")
        raise SystemExit(0)
