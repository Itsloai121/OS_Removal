# OS Removal Lab

**OS Removal Lab** is a cross-platform Python TUI (terminal user interface) for an educational cybersecurity lab. It presents two platform choices:

1. **Windows** — previews the impact of removing `C:\Windows\System32`.
2. **Linux** — previews the impact of removing the root filesystem (`/`).

## Safety and scope

This project is deliberately a **non-destructive simulator**, not an operating-system wiper or privilege-escalation tool.

- It does **not** delete, overwrite, encrypt, or modify files.
- It does **not** run shell commands or invoke external programs.
- It does **not** change permissions, bypass access controls, or attempt to gain Administrator/root privileges.
- It only reads basic platform and current-process privilege information.
- Its simulation report explicitly marks destructive actions as blocked and privilege escalation as not attempted.

Removing Windows System32 or a Linux root filesystem can make a machine unbootable and cause permanent data loss. The tool therefore displays the affected target and likely consequences without performing the operation.

## Requirements

- Python 3.9 or newer
- No third-party packages required

## Run

Open a terminal in this directory and run:

### Windows

```powershell
py -3 os_removal_lab.py
```

### Linux

```bash
python3 os_removal_lab.py
```

The program displays a menu with **Windows**, **Linux**, and **Quit**. Choose a platform, review the impact preview, then type `SIMULATE` to see the safe walkthrough. Press Enter at the prompt to return to the menu.

## Privilege display

The tool reports whether the current process is running as Administrator on Windows or as UID 0 (root) on Linux. It does not request elevation; elevated privileges are neither needed nor used by this simulator.

## Project files

```text
os_removal_lab/
├── os_removal_lab.py
└── README.md
```

## Educational use

Use this project to discuss operating-system critical directories, availability risks, least privilege, recovery planning, and why destructive actions require strict safeguards in a controlled lab.

## License

You may adapt this educational simulator for coursework and internal demonstrations. Keep the non-destructive safeguards intact when modifying it.
