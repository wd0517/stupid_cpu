import time
from multiprocessing import Pool

import psutil

from .quota_cpu_cgroups import CustomCgroup, add_to_cgroup
from .utils import set_proc_name
from .consts import (
    CGROUP_NAME,
    CPU_LIMIT,
    CPU_COUNT
)


def stupid_cpu_slave_task():
    set_proc_name(b'stupid-cpu [slave]')
    add_to_cgroup(CGROUP_NAME)

    a = 0
    while True:
        a += 1


def main():
    cg = CustomCgroup(CGROUP_NAME)
    cg.set_cpu_limit(CPU_LIMIT)
    cg.set_memory_limit(100)

    set_proc_name(b'stupid-cpu [master]')

    p = Pool()
    for i in range(CPU_COUNT):
        p.apply_async(stupid_cpu_slave_task)

    cur_cpu_limit = CPU_LIMIT
    while True:
        cur_cpu_percent = psutil.cpu_percent(3)
        if cur_cpu_percent > CPU_LIMIT:
            cur_cpu_limit = cur_cpu_limit - (cur_cpu_percent - CPU_LIMIT)
        else:
            cur_cpu_limit = CPU_LIMIT

        if cur_cpu_limit < 0:
            cur_cpu_limit = 0

        cg.set_cpu_limit(cur_cpu_limit)


if __name__ == '__main__':
    main()
