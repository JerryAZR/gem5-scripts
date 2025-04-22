from gem5.components.cachehierarchies.classic.abstract_classic_cache_hierarchy import (
    AbstractClassicCacheHierarchy,
)
from gem5.components.cachehierarchies.classic.caches.l2cache import L2Cache
from gem5.components.boards.abstract_board import AbstractBoard
from gem5.isas import ISA

from m5.objects import (
    L2XBar,
    SystemXBar,
    BadAddr,
)
from m5.params import (
    VectorParam
)

from l1_l2_cluster import L1L2Cluster

class ThreeLevelCacheHierarchy(AbstractClassicCacheHierarchy):
    # core_clusters = VectorParam.SubSystem([], "Per-core L1+L2+MMU clusters")
    def __init__(self):
        super().__init__()
        self.membus = SystemXBar(width=64)  # L3 to Memory
        self.membus.badaddr_responder = BadAddr()
        self.membus.default = self.membus.badaddr_responder.pio

    def incorporate_cache(self, board: AbstractBoard):
        board.connect_system_port(self.membus.cpu_side_ports)
        # Shared L3 cache (Reuse the L2 types for simplicity)
        self.l3_cache = L2Cache(size="8MiB", assoc=16)
        self.l3_xbar = L2XBar()
        # L3 cache connections
        self.l3_xbar.mem_side_ports.connect(self.l3_cache.cpu_side)
        self.l3_cache.mem_side.connect(self.membus.cpu_side_ports)
        for _, port in board.get_memory().get_mem_ports():
            self.membus.mem_side_ports.connect(port)
        # Create core clusters
        self.core_clusters = [
            L1L2Cluster(core=core, membus=self.l3_xbar,
                l1i_size="32KiB", l1i_assoc=8,
                l1d_size="32KiB", l1d_assoc=8,
                l2_size="1MiB", l2_assoc=16
            ) for core in board.get_processor().get_cores()
        ]
        # Add interrupt controller
        for core in board.get_processor().get_cores():
            if board.get_processor().get_isa() == ISA.X86:
                int_req_port = self.membus.mem_side_ports
                int_resp_port = self.membus.cpu_side_ports
                core.connect_interrupt(int_req_port, int_resp_port)
            else:
                core.connect_interrupt()


    def get_mem_side_port(self):
        return self.membus.mem_side_ports

    def get_cpu_side_port(self):
        return self.membus.cpu_side_ports
