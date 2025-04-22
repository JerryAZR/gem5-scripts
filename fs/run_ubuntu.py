import m5
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
from gem5.simulate.exit_event import ExitEvent
from my_riscv_board import MyRiscvBoard

def handle_workend():
    print("Dump stats at the end of the ROI!")
    m5.stats.dump()
    yield False


def handle_workbegin():
    print("Done booting Linux")
    print("Switching CPU to TIMING for real workload...")
    board.processor.switch()
    print("Resetting stats at the start of ROI!")
    m5.stats.reset()
    yield False


def exit_event_handler():
    print("first exit event: Kernel booted")
    yield False
    print("second exit event: In after boot")
    yield False
    print("third exit event: After run script")
    yield True


# Now assemble the RISC-V board.
board = MyRiscvBoard()

# Set the workload (downloaded automatically from gem5 resources).
# workload = obtain_resource("riscv-ubuntu-22.04-boot")
board.set_kernel_disk_workload(
    kernel=obtain_resource("riscv-linux-6.6.33-kernel"),
    disk_image=obtain_resource("riscv-ubuntu-22.04-img"),
    bootloader=obtain_resource("riscv-bootloader-opensbi-1.3.1"),
    readfile="/home/jerry/projects/gem5/workloads/fs/hello"
)

# Create and run the simulation.
simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.WORKBEGIN: handle_workbegin(),
        ExitEvent.WORKEND: handle_workend(),
        ExitEvent.EXIT: exit_event_handler(),
    },
)

simulator.run()
