# process_manager.py

import psutil

cores = psutil.cpu_count()

def get_top_processes(limit=20):
    # Returns list of dictionaries with the top processes by memory usage
    processes = []

    # Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent']):
        try:
            p_info = proc.info

            raw_cpu = p_info['cpu_percent'] or 0
            # Core usage
            core = p_info['cpu_percent']
            p_info['cpu_core'] = core
            # To get the global value instead of the % of a core
            cpu_normalized = raw_cpu/cores
            mem = p_info['memory_percent'] or 0
            p_info['cpu_percent'] = cpu_normalized

            # Combine CPU + RAM usage to get the stress of a process
            p_info['stress'] = cpu_normalized + mem

            processes.append(p_info)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    sorted_procs = sorted(processes, key=lambda p: p['stress'], reverse=True)
    return sorted_procs[:limit]

def kill_process(pid):
    # Kills process by PID
    try:
        process = psutil.Process(pid)
        process.terminate()
        return True, f"Process {pid} terminated"
    except psutil.NoSuchProcess:
        return False, f"Process {pid} not found"
    except psutil.AccessDenied:
        return False, "Permission denied"
    except Exception as e:
        return False, f"Error: {e}"

