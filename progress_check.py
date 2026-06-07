#!/usr/bin/env python3
import os
import time
from datetime import datetime
import subprocess

PROGRESS_FILE = '/tmp/progress.txt'

# ANSI кольори
COLOR_PINK = '\033[95m'
COLOR_BLUE = '\033[94m'
COLOR_RESET = '\033[0m'

def write_progress(p):
    with open(PROGRESS_FILE, 'w') as f:
        f.write(str(p))

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

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
    output = subprocess.getoutput("sudo iptables-save -t nat")

    log("check_nat_output=\n" + output)

    return "192.168.1.0/24" in output and "MASQUERADE" in output

    log("check_nat_expected=" + expected)

    ok = expected in output

    log("check_nat=" + ("OK" if ok else "FAIL"))

    return ok


# --- Перевірка network.config ---
def check_network_config():
    ok = os.path.exists("/root/network.config")
    log("network_config=OK" if ok else "network_config=NOT FOUND")
    return ok

# --- Перевірка FTP завантаження ---

def check_ftp_upload():
    ok = False
    output = subprocess.getoutput(
        "sshpass -p 'porta!!!' ssh -o StrictHostKeyChecking=no "
        "padavan@192.168.2.6 "
        "\"test -f /srv/sftp/upload/network.config && echo OK || echo FAIL\""
    )

    log("ftp_upload_output=" + output)

    return "OK" in output


# --- Перевірка копіювання Setup.txt через scp ---
def check_scp_setup():
    ok = False
    output = subprocess.getoutput(
        "sshpass -p 'porta!!!' ssh -o StrictHostKeyChecking=no "
        "padavan@192.168.2.6 "
        "\"grep -i 'Router is Setuped' /home/padavan/Setup.txt && echo OK || echo FAIL\""
    )

    log("scp_setup_output=" + output)

    return "OK" in output

def check_forward_ssh():
    ok = False
    output = subprocess.getoutput("sudo iptables-save -t nat")

    log("forward_ssh_output=\n" + output)

    return (
        "-A PREROUTING" in output and
        "--dport 12345" in output and
        "DNAT" in output and
        "--to-destination 192.168.1.4:22" in output
    )

    log("forward_ssh_expected=" + expected)

    ok = expected in output

    log("forward_ssh=" + ("OK" if ok else "FAIL"))

    return ok

def check_traffic_pcap():
    ok = os.path.exists("/root/traffic.pcap")
    log("traffic_pcap=OK" if ok else "traffic_pcap=NOT FOUND")
    return ok
# --- Словник кроків ---
TASKS = {
    1: (check_ssh_from_ip, 27),
    2: (check_ip_forward, 8),
    3: (check_resolv, 7),
    4: (check_nat, 10),
    5: (check_network_config, 8),
    6: (check_ftp_upload, 9),
    7: (check_scp_setup, 11),
    8: (check_forward_ssh, 12),
    9: (check_traffic_pcap, 8)
}


def update_progress(task_status):
    percent = sum(pct for num,(func,pct) in TASKS.items() if task_status.get(num))
    write_progress(percent)
    # Відображення прогресбару у кольорах
    print(f"\r{COLOR_PINK}Progress: {percent} %{COLOR_RESET} {COLOR_BLUE}user@localhost ~$ {COLOR_RESET}", end='')

def monitor_tasks():
    task_status = {num: False for num in TASKS}
    while True:
        updated = False
        for num,(func,pct) in TASKS.items():
            current = func()
            if current and not task_status[num]:
                task_status[num] = True
                updated = True
                log(f"Task {num}=OK (+{pct}%)")
        if updated:
            update_progress(task_status)
        time.sleep(2)


if __name__ == "__main__":
    write_progress(0)
    update_progress({})  # початковий прогрес
    monitor_tasks()
