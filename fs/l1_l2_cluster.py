from m5.objects import (
    L2XBar,
    SystemXBar,
    SubSystem
)
from gem5.components.cachehierarchies.classic.caches.l1icache import L1ICache
from gem5.components.cachehierarchies.classic.caches.l1dcache import L1DCache
from gem5.components.cachehierarchies.classic.caches.l2cache import L2Cache
from gem5.components.cachehierarchies.classic.caches.mmu_cache import MMUCache
from gem5.components.processors.base_cpu_core import BaseCPUCore
from typing import Optional

class L1L2Cluster(SubSystem):
    def __init__(
        self,
        core: Optional[BaseCPUCore],
        membus: Optional[SystemXBar],
        l1i_size,
        l1i_assoc,
        l1d_size,
        l1d_assoc,
        l2_size,
        l2_assoc
    ):
        super().__init__()
        self.l1i_cache  = L1ICache(size=l1i_size, assoc=l1i_assoc)
        self.l1d_cache  = L1DCache(size=l1d_size, assoc=l1d_assoc)
        self.l2_cache   = L2Cache(size=l2_size, assoc=l2_assoc)
        self.iptw_cache = MMUCache(size="8KiB", writeback_clean=False)
        self.dptw_cache = MMUCache(size="8KiB", writeback_clean=False)
        self.l2_bus = L2XBar()
        # Internal connection
        self.l1i_cache.mem_side.connect(self.l2_bus.cpu_side_ports)
        self.l1d_cache.mem_side.connect(self.l2_bus.cpu_side_ports)
        self.iptw_cache.mem_side.connect(self.l2_bus.cpu_side_ports)
        self.dptw_cache.mem_side.connect(self.l2_bus.cpu_side_ports)
        self.l2_bus.mem_side_ports.connect(self.l2_cache.cpu_side)
        # External connection
        if (core): self.connect_core_ports(core)
        if (membus): self.connect_mem_ports(membus)

    def connect_core_ports(self, core: BaseCPUCore):
        core.connect_icache(self.l1i_cache.cpu_side)
        core.connect_dcache(self.l1d_cache.cpu_side)
        if hasattr(core, 'connect_walker_ports'):
            core.connect_walker_ports(self.iptw_cache.cpu_side, self.dptw_cache.cpu_side)

    def connect_mem_ports(self, bus: SystemXBar):
        self.l2_cache.mem_side.connect(bus.cpu_side_ports)
