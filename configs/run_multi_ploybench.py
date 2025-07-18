import m5
import os
from typing import Type
from pathlib import Path
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
from gem5.simulate.exit_event import ExitEvent
from m5.objects import (
    BasePrefetcher,
    NextLinePrefetcher,
    StridePrefetcher,
    MarkovPrefetcher
)
from m5.debug import flags
from boards.my_riscv_board import MyRiscvBoard
from benchmark_list import prepare_benchmark
import gem5.utils.multisim as multisim

multisim.set_num_processes(4)

CHECKPOINT_PATH = "/home/jerry/projects/gem5/checkpoints"
checkpoint_valid = os.path.exists(os.path.join(CHECKPOINT_PATH, "m5.cpt"))
if not checkpoint_valid:
    raise RuntimeError("Checkpoint not found — this script requires an existing checkpoint.")

benchmark_table = {}

def handle_workend():
    print("WORKEND triggered")
    print("Dumping stats at end of ROI!")
    m5.stats.dump()
    yield False

def handle_workbegin(board: MyRiscvBoard):
    print("WORKBEGIN triggered, switching CPU type")
    board.processor.switch()
    print("Resetting stats for the beginning of ROI!")
    m5.stats.reset()
    yield False

def exit_event_handler():
    print("Exit event: After run script")
    yield True

def build_simulator(benchmark: str, prefetcherCls: Type[BasePrefetcher]) -> Simulator:
    # Now assemble the RISC-V board.
    board = MyRiscvBoard(l2_prefetcher=prefetcherCls)

    # Set the workload (downloaded automatically from gem5 resources).
    # workload = obtain_resource("riscv-ubuntu-22.04-boot")
    board.set_kernel_disk_workload(
        kernel=obtain_resource("riscv-linux-6.6.33-kernel"),
        disk_image=obtain_resource("riscv-ubuntu-22.04-img"),
        bootloader=obtain_resource("riscv-bootloader-opensbi-1.3.1"),
        readfile=benchmark_table[benchmark],
        checkpoint=Path(CHECKPOINT_PATH)
    )

    # Create and run the simulation.
    return Simulator(
        board=board,
        on_exit_event={
            ExitEvent.WORKBEGIN: handle_workbegin(board),
            ExitEvent.WORKEND: handle_workend(),
            ExitEvent.EXIT: exit_event_handler(),
        },
        id=f"{benchmark}_{prefetcherCls.__name__}"
    )

# TICK_RATE = 1_000_000_000
# simulator.run(TICK_RATE * 3600)

# flags["MarkovPrefetch"].enable()

benchmarks = ["seidel-2d"]
# prefetchers = [MarkovPrefetcher, StridePrefetcher, NextLinePrefetcher]
prefetchers = [MarkovPrefetcher]

for benchmark in benchmarks:
    benchmark_table[benchmark] = prepare_benchmark(benchmark)
    for prefetcher in prefetchers:
        multisim.add_simulator(
            build_simulator(benchmark, prefetcher)
        )
