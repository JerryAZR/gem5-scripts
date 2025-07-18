from typing import Type

from m5.objects import (
    BasePrefetcher,
    Cache,
    Clusivity,
    StridePrefetcher,
)

class L3Cache(Cache):
    """
    A more realistic L3 Cache, shared among multiple cores.
    """

    def __init__(
        self,
        size: str = "16MiB",                # Modern CPUs typically have 16–64MB
        assoc: int = 16,                    # 16-way is common
        tag_latency: int = 30,              # Higher than L2 (~3x typical)
        data_latency: int = 30,
        response_latency: int = 2,
        mshrs: int = 64,                    # More MSHRs to track concurrent misses
        tgts_per_mshr: int = 20,
        writeback_clean: bool = True,       # To support exclusive behavior in upper levels
        clusivity: Clusivity = "mostly_incl",  # Inclusive for coherence
        PrefetcherCls: Type[BasePrefetcher] = StridePrefetcher,
    ):
        super().__init__()
        self.size = size
        self.assoc = assoc
        self.tag_latency = tag_latency
        self.data_latency = data_latency
        self.response_latency = response_latency
        self.mshrs = mshrs
        self.tgts_per_mshr = tgts_per_mshr
        self.writeback_clean = writeback_clean
        self.clusivity = clusivity
        self.prefetcher = PrefetcherCls()
