import m5
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
from m5.objects import StridePrefetcher
from my_riscv_board import MyRiscvBoard

processor = SimpleProcessor(
    cpu_type=CPUTypes.O3,
    isa=ISA.RISCV,
    num_cores=2,
)

# Now assemble the RISC-V board.
board = MyRiscvBoard()
board.processor = processor

# Set the workload (downloaded automatically from gem5 resources).
board.set_se_binary_workload(obtain_resource("riscv-hello"))
# board.set_se_binary_workload(obtain_resource("riscv-cch-st"))
# Create and run the simulation.
simulator = Simulator(
    board=board
)

simulator.run()
