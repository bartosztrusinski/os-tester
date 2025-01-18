import platform
import psutil

def get_system_info():
    try:
        uname = platform.uname()
        cores = psutil.cpu_count(logical=True)
        ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        
        if uname.system == "Windows":
            version = platform.win32_ver()
            os_version = f"{uname.system} {version[0]} (Build {version[1]})"
        else:
            os_version = f"{uname.system} {uname.release} {uname.version}"
        
        return f"System: {os_version}, {uname.machine}\nCores: {cores}\nRAM: {ram} GB"
    except Exception as e:
        return f"System information could not be determined: {e}"