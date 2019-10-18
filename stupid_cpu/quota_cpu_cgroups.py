import os

from cgroups import Cgroup
from cgroups.common import CgroupsException

from .consts import (
    CPU_COUNT,
    CPU_PER_PERIOD
)


CustomCgroup = Cgroup


# Cgroup 使用了 cpu.shares 去控制 cpu 的使用率, 该方法在其他进程没有跑满 CPU 时达不到控制目的
# 重写为使用 cpu.cfs_period_us 和 cpu.cfs_quota_us 强制控制对 CPU 时间的使用
def _quota_set_cpu_limit(self, limit=None):
    if 'cpu' in self.cgroups:
        value = int(CPU_PER_PERIOD * CPU_COUNT * (limit / 100))
        # cgroup 限制最小值为 1000
        quota = 1000 if value < 1000 else value

        cpu_cfs_peroid_file = self._get_cgroup_file('cpu', 'cpu.cfs_period_us')
        cpu_cfs_quota_file = self._get_cgroup_file('cpu', 'cpu.cfs_quota_us')
        with open(cpu_cfs_peroid_file, 'w+') as f:
            f.write('{}\n'.format(CPU_PER_PERIOD))
        with open(cpu_cfs_quota_file, 'w+') as f:
            f.write('{}\n'.format(quota))
    else:
        raise CgroupsException(
            'CPU hierarchy not available in this cgroup')


def add_to_cgroup(group_name):
    cg = CustomCgroup(group_name)
    cg.add(os.getpid())


CustomCgroup.set_cpu_limit = _quota_set_cpu_limit
