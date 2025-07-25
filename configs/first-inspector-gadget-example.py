# Copyright (c) 2021 The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import m5
from m5.objects import Root

#### Import DDR3_1600_8x8 here.
from m5.objects.DRAMInterface import DDR3_1600_8x8

from components.three_level_cache_hierachy import ThreeLevelCacheHierarchy
from components.hybrid_generator import HybridGenerator

#### Import InspectedMemory here.
from components.inspected_memory import InspectedMemory

from gem5.components.boards.test_board import TestBoard
from gem5.simulate.simulator import Simulator


cache_hierarchy = ThreeLevelCacheHierarchy()

#### Add your code for inspected memory here.
memory = InspectedMemory(
    dram_interface_class=DDR3_1600_8x8,
    num_channels=2,
    interleaving_size="128",
    size="512MiB",
)

generator = HybridGenerator(
    num_cores=6,
    rate="1GB/s",
    duration="1ms",
)

motherboard = TestBoard(
    clk_freq="4GHz",
    generator=generator,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# root = Root(full_system=False, system=motherboard)
# motherboard._pre_instantiate()
# m5.instantiate()
# generator.start_traffic()
# print("Beginning simulation!")
# exit_event = m5.simulate()
# print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}.")

# Create and run the simulation.
simulator = Simulator(
    board=motherboard
)
simulator.run()
