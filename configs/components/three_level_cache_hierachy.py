from typing import Type
from gem5.components.cachehierarchies.classic.abstract_classic_cache_hierarchy import (
    AbstractClassicCacheHierarchy,
)
from gem5.components.boards.abstract_board import AbstractBoard
from gem5.isas import ISA

from m5.objects import (
    L2XBar,
    SystemXBar,
    BadAddr,
    Cache,
    BasePrefetcher,
    StridePrefetcher
)

from .l3cache import L3Cache
from .l1_l2_cluster import L1L2Cluster

class ThreeLevelCacheHierarchy(AbstractClassicCacheHierarchy):
    # core_clusters = VectorParam.SubSystem([], "Per-core L1+L2+MMU clusters")
    def __init__(self, l2_prefetcher: Type[BasePrefetcher] = StridePrefetcher):
        super().__init__()
        self.membus = SystemXBar(width=64)  # L3 to Memory
        self.membus.badaddr_responder = BadAddr()
        self.membus.default = self.membus.badaddr_responder.pio
        self._l2_pf_cls = l2_prefetcher

    def incorporate_cache(self, board: AbstractBoard):
        board.connect_system_port(self.membus.cpu_side_ports)
        # Shared L3 cache (Reuse the L2 types for simplicity)
        self.l3_cache = L3Cache()
        self.l3_xbar = L2XBar()
        # L3 cache connections
        self.l3_xbar.mem_side_ports.connect(self.l3_cache.cpu_side)
        self.l3_cache.mem_side.connect(self.membus.cpu_side_ports)
        for _, port in board.get_memory().get_mem_ports():
            self.membus.mem_side_ports.connect(port)
        # Create core clusters
        self.core_clusters = [
            L1L2Cluster(core=core, membus=self.l3_xbar, l2_pf_cls=self._l2_pf_cls,
                l1i_size="16KiB", l1i_assoc=4,
                l1d_size="16KiB", l1d_assoc=4,
                l2_size="512KiB", l2_assoc=8
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

        if board.has_coherent_io():
            self._setup_io_cache(board)


    def get_mem_side_port(self):
        return self.membus.mem_side_ports

    def get_cpu_side_port(self):
        return self.membus.cpu_side_ports

    def _setup_io_cache(self, board: AbstractBoard) -> None:
        """Create a cache for coherent I/O connections"""
        self.iocache = Cache(
            assoc=8,
            tag_latency=50,
            data_latency=50,
            response_latency=50,
            mshrs=20,
            size="1KiB",
            tgts_per_mshr=12,
            addr_ranges=board.mem_ranges,
        )
        self.iocache.mem_side = self.membus.cpu_side_ports
        self.iocache.cpu_side = board.get_mem_side_coherent_io_port()