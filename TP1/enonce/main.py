from env import ModelGUI, ExampleRoom
from subsumption import SubsumptionArchitecture
from behaviors import MoveForwardInRandomDirection, MoveTowardsCoin, AvoidObstacles, Bump


if __name__ == "__main__":

    architecture = SubsumptionArchitecture()

    # Add behaviors to the architecture
    architecture.add_behavior(MoveForwardInRandomDirection())
    architecture.add_behavior(MoveTowardsCoin())
    architecture.add_behavior(AvoidObstacles())
    architecture.add_behavior(Bump())

    playground = ExampleRoom()
    gui = ModelGUI(architecture, playground,
                   playground.agent, draw_sensors=True)
    gui.run()
