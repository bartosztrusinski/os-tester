import platform
import subprocess

def get_bios_version():
    system = platform.system()

    try:
        if system == "Windows":
            result = subprocess.check_output(
                ['powershell', '-Command', '(Get-WmiObject Win32_BIOS).SMBIOSBIOSVersion'],
                universal_newlines=True
            )
            return f"BIOS version: {result.strip()}"

        elif system == "Linux":
            result = subprocess.check_output(
                ['sudo', 'dmidecode', '-t', '0'],
                universal_newlines=True
            )
            for line in result.splitlines():
                if "Version" in line:
                    return f"BIOS version: {line.strip()}"
            return "BIOS version could not be determined"

        elif system == "Darwin":
            result = subprocess.check_output(
                ['system_profiler', 'SPHardwareDataType'],
                universal_newlines=True
            )
            for line in result.splitlines():
                if "Boot ROM Version" in line:
                    return f"BIOS version: {line.split(':')[1].strip()}"
            return "BIOS version could not be determined"

        else:
            return "Unsupported OS for BIOS version detection"

    except Exception as e:
        return f"BIOS version could not be determined: {e}"