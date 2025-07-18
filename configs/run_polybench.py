import m5
import os
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
from gem5.simulate.exit_event import ExitEvent
from m5.objects import (
    NextLinePrefetcher
)
from boards.my_riscv_board import MyRiscvBoard
from benchmark_list import prepare_benchmark

CHECKPOINT_PATH = "/home/jerry/projects/gem5/checkpoints"
checkpoint_valid = os.path.exists(os.path.join(CHECKPOINT_PATH, "m5.cpt"))

def handle_workend():
    print("WORKEND triggered")
    print("Dumping stats at end of ROI!")
    m5.stats.dump()
    yield False

def handle_workbegin():
    print("WORKBEGIN triggered, switching CPU type")
    board.processor.switch()
    print("Resetting stats for the beginning of ROI!")
    m5.stats.reset()
    yield False

def exit_event_handler():
    if not checkpoint_valid:
        print("first exit event: Kernel booted")
        yield False
        print("second exit event: In after boot. Creating checkpoint...")
        simulator.save_checkpoint(CHECKPOINT_PATH)
        yield False
    print("third exit event: After run script")
    yield True

# Now assemble the RISC-V board.
board = MyRiscvBoard(l2_prefetcher=NextLinePrefetcher)

# Set the workload (downloaded automatically from gem5 resources).
# workload = obtain_resource("riscv-ubuntu-22.04-boot")
board.set_kernel_disk_workload(
    kernel=obtain_resource("riscv-linux-6.6.33-kernel"),
    disk_image=obtain_resource("riscv-ubuntu-22.04-img"),
    bootloader=obtain_resource("riscv-bootloader-opensbi-1.3.1"),
    readfile=prepare_benchmark("seidel-2d")
)

# Create and run the simulation.
simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.WORKBEGIN: handle_workbegin(),
        ExitEvent.WORKEND: handle_workend(),
        ExitEvent.EXIT: exit_event_handler(),
    },
    checkpoint_path=CHECKPOINT_PATH
)

TICK_RATE = 1_000_000_000
simulator.run(TICK_RATE * 3600)
