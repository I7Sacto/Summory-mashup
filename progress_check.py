#!/usr/bin/env python3
import os
import time
from datetime import datetime
import subprocess

PROGRESS_FILE = '/tmp/progress.txt'
LOGFILE = '/mnt/sdb1/Performance.txt'

# ANSI кольори
COLOR_PINK = '\033[95m'
COLOR_BLUE = '\033[94m'
COLOR_RESET = '\033[0m'

def write_progress(p):
    with open(PROGRESS_FILE, 'w') as f:
        f.write(str(p))

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if os.path.exists(LOGFILE):
        with open(LOGFILE, 'a') as f:
            f.write(f"[{ts}] {msg}\n")

# --- Приклади перевірок ---
def check_ssh_from_ip(ip_prefix="192.168.1."):
    ok = False
    SSH_LOG_FILE = "/var/log/secure"  # Padavan
    try:
        # Використовуємо sudo для читання
        output = subprocess.getoutput(f"sudo cat {SSH_LOG_FILE} | grep 'Accepted' | grep '{ip_prefix}'")
        if output.strip():
            ok = True
    except:
        pass
    log("ssh_from_ip=OK" if ok else "ssh_from_ip=FAIL")
    return ok


def check_ip_forward():
    ok = False
    try:
        with open("/etc/sysctl.conf") as f:
            for line in f:
                if "net.ipv4.ip_forward=1" in line.strip():
                    ok = True
                    break
    except:
        pass
    log("ip_forward=OK" if ok else "ip_forward=FAIL")
    return ok

# --- Перевірка nameserver 8.8.8.8 ---
def check_resolv():
    ok = False
    try:
        with open("/etc/resolv.conf") as f:
            for line in f:
                if "8.8.8.8" in line:
                    ok = True
                    break
    except:
        pass
    log("resolv=OK" if ok else "resolv=FAIL")
    return ok

# --- Перевірка NAT у iptables ---
def check_nat():
    ok = False

    try:
        output = subprocess.getoutput("sudo iptables -t nat -S POSTROUTING")

        if "-j MASQUERADE" in output or "-j SNAT" in output:
            ok = True

    except:
        ok = False

    return ok

# --- Перевірка network.config ---
def check_network_config():
    ok = os.path.exists("/root/network.config")
    log("network_config=OK" if ok else "network_config=NOT FOUND")
    return ok

# --- Перевірка FTP завантаження ---
def check_ftp_upload():
    # Спрощено: перевірка існування файлу, який мав бути завантажений на FTP
    ok = False

    try:
        cmd = (
            "ssh -o StrictHostKeyChecking=no "
            "padavan@sysadmin.local "
            "'test -f ~/network.config && echo OK'"
        )

        output = subprocess.getoutput(cmd)

        if "OK" in output:
            ok = True

    except:
        pass

    log("ftp_upload=OK" if ok else "ftp_upload=FAIL")

    return ok

# --- Перевірка копіювання Setup.txt через scp ---

def check_scp_setup():
    ok = False
    try:
        cmd = (
            "ssh -o StrictHostKeyChecking=no "
            "padavan@192.168.2.6 "
            "'grep -i \"Router is Setuped\" ~/Setup.txt && echo OK'"
        )
        output = subprocess.getoutput(cmd)
        print("scp_setup_output=", repr(output))  # точний вивід

        # Перевірка: достатньо, щоб у виводі було слово OK
        if "OK" in output.split():
            ok = True
    except Exception as e:
        log(f"scp_setup_error={e}")

    log("scp_setup=OK" if ok else "scp_setup=FAIL")
    return ok


def check_forward_ssh():
    ok = False
    output = subprocess.getoutput("sudo iptables -t nat -S PREROUTING")

    log("forward_ssh_output=\n" + output)

    expected = ("-A PREROUTING -i enp0s8 -p tcp -m tcp --dport 12345 -j DNAT --to-destination 192.168.2.10:22"

    )

    log("forward_ssh_expected=" + expected)

    ok = expected in output

    log("forward_ssh=" + ("OK" if ok else "FAIL"))

    return ok






# --- Словник кроків ---
TASKS = {
    1: check_ssh_from_ip,
    2: check_ip_forward,
    3: check_resolv,
    4: check_nat,
    5: check_network_config,
    6: check_ftp_upload,
    7: check_scp_setup
}

def update_progress(task_status):
    success_count = sum(1 for v in task_status.values() if v)
    percent = int((success_count / len(TASKS)) * 100)
    write_progress(percent)
    # Відображення прогресбару у кольорах
    print(f"\r{COLOR_PINK}Progress: {percent} %{COLOR_RESET} {COLOR_BLUE}user@localhost ~$ {COLOR_RESET}", end='')

def monitor_tasks():
    task_status = {num: False for num in TASKS}
    while True:
        updated = False
        for num, func in TASKS.items():
            current = func()
            if current and not task_status[num]:
                task_status[num] = True
                updated = True
        if updated:
            update_progress(task_status)
        time.sleep(2)

if __name__ == "__main__":
    write_progress(0)
    update_progress({})  # початковий прогрес
    monitor_tasks()
