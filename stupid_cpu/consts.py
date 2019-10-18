import psutil


CGROUP_NAME = 'stupid_cpu'
CPU_LIMIT = 30
CPU_COUNT = psutil.cpu_count()
CPU_PER_PERIOD = 100000
