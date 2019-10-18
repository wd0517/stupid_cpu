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
    # 将子进程交给 cgroup 管理，没有使用进程组的方式
    add_to_cgroup(CGROUP_NAME)
    # 单进程将 CPU 跑满 100%
    a = 0
    while True:
        a += 1


def main():
    cg = CustomCgroup(CGROUP_NAME)
    cg.set_cpu_limit(CPU_LIMIT)
    cg.set_memory_limit(100)

    set_proc_name(b'stupid-cpu [master]')

    p = Pool()
    # GIL 导致单进程只能跑满一个 CPU, 所以我们启动和 CPU 核数一样的子进程数
    for i in range(CPU_COUNT):
        p.apply_async(stupid_cpu_slave_task)

    # 动态调整 cgroup 参数
    # 当其他进程的 CPU 占用变高时, 调低本应用的 CPU 使用限制, 不影响系统正常使用
    cur_cpu_limit = CPU_LIMIT
    while True:
        time.sleep(5)
        cur_cpu_percent = psutil.cpu_percent()
        if cur_cpu_percent > CPU_LIMIT:
            cur_cpu_limit = cur_cpu_limit - (cur_cpu_percent - CPU_LIMIT)
        else:
            cur_cpu_limit = CPU_LIMIT

        if cur_cpu_limit < 0:
            cur_cpu_limit = 0

        cg.set_cpu_limit(cur_cpu_limit)


if __name__ == '__main__':
    main()
