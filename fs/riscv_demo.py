from gem5.prebuilt.demo.riscv_demo_board import RiscvDemoBoard
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

board = RiscvDemoBoard()
board.set_workload(obtain_resource("riscv-ubuntu-22.04-boot"))

# Create and run the simulation.
simulator = Simulator(board=board)
simulator.run()
