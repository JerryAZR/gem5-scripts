from gem5.components.boards.riscv_board import RiscvBoard
from gem5.components.memory import DualChannelDDR4_2400
from gem5.components.processors.simple_switchable_processor import SimpleSwitchableProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import (
    PrivateL1SharedL2CacheHierarchy,
)
from three_level_cache_hierachy import ThreeLevelCacheHierarchy
# from gem5.resources.resource import obtain_resource
# from gem5.simulate.simulator import Simulator
from gem5.isas import ISA

class MyRiscvBoard(RiscvBoard):
    def __init__(self):
        memory = DualChannelDDR4_2400(size="4GiB")
        processor = SimpleSwitchableProcessor(
            starting_core_type=CPUTypes.ATOMIC,
            switch_core_type=CPUTypes.TIMING,
            num_cores=1,
            isa=ISA.RISCV
        )
        # cache_hierarchy = PrivateL1SharedL2CacheHierarchy(
        #     l1d_size="64KiB", l1i_size="64KiB", l2_size="1MiB"
        # )
        cache_hierarchy = ThreeLevelCacheHierarchy()

        super().__init__(
            clk_freq="1.4GHz",
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy
        )