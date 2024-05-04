import psutil
import logging

# Set up logging for the module
logger = logging.getLogger('CryptojackingDetection')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# List of known crypto mining process names, this list might need to be updated over time
KNOWN_MINING_PROCESSES = ['xmrig', 'minerd', 'cgminer', 'cpuminer']

def check_high_resource_usage(threshold_cpu=50, threshold_memory=50, duration=60):
    """
    Check for high CPU and memory usage over a specified duration.
    """
    logger.info(f"Monitoring CPU and Memory usage for {duration} seconds...")
    high_usage_detected = False
    for _ in range(duration):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        if cpu_usage > threshold_cpu or memory_usage > threshold_memory:
            logger.warning(f"High CPU usage: {cpu_usage}%, Memory usage: {memory_usage}%")
            high_usage_detected = True
        else:
            logger.info(f"CPU usage: {cpu_usage}%, Memory usage: {memory_usage}%")
    if high_usage_detected:
        inspect_suspicious_processes(threshold_cpu, threshold_memory)

def inspect_suspicious_processes(threshold_cpu, threshold_memory):
    """
    Inspect processes with high CPU or memory usage.
    """
    processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
    for proc in processes:
        info = proc.info
        if info['cpu_percent'] > threshold_cpu or info['memory_percent'] > threshold_memory:
            log_process_info(info)

def log_process_info(proc_info):
    """
    Log information about a process.
    """
    if proc_info['name'].lower() in KNOWN_MINING_PROCESSES:
        logger.warning(f"**Known mining process detected** PID: {proc_info['pid']}, Name: {proc_info['name']}")
    logger.info(f"PID: {proc_info['pid']}, Name: {proc_info['name']}, CPU Usage: {proc_info['cpu_percent']}%, Memory Usage: {proc_info['memory_percent']}%")

if __name__ == "__main__":
    check_high_resource_usage()

