import numpy as np
from spg.element.wall import ColorWall
from spg.element import Coin
from spg.playground import ConnectedRooms
from spg.view import GUI
from spg.agent.agent import Agent
from spg.agent.part import ForwardBase
from spg.agent.sensor import DistanceSensor, RGBSensor


class ExampleAgent(Agent):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        base = ForwardBase(linear_ratio=1, angular_ratio=0.2 / np.pi)
        self.add(base)

        # SENSORS
        self.distance = DistanceSensor(
            fov=180,
            resolution=4,
            max_range=50,
            invisible_elements=self._parts,
            normalize=True,
        )
        self.rgb = RGBSensor(
            fov=5,
            resolution=4,
            max_range=600,
            invisible_elements=self._parts
        )
        self.bump = DistanceSensor(
            fov=90,
            resolution=16,
            max_range=25,
            invisible_elements=self._parts,
            normalize=True,
        )
        self.base.add(self.distance)
        self.base.add(self.rgb)
        self.base.add(self.bump)


class ExampleRoom(ConnectedRooms):
    def __init__(self):

        n_w = 3
        n_h = 3

        super().__init__(
            room_layout=(n_w, n_h),
            size_room=(200, 200),
            doorstep_length=150,
            centered_doorstep=True,
            background=(23, 73, 71),
            wall_cls=ColorWall,
            seed=1,
        )

        self.agent = ExampleAgent()

        self.add(
            self.agent, self._room_coordinate_sampler[4], allow_overlapping=True)

        self._task_elems = []
        room = np.random.randint(9)
        coin = Coin(None, color=(255, 215, 0))
        coin.graspable = True
        self.add(
            coin,
            self._room_coordinate_sampler[room],
            allow_overlapping=False,
        )
        self._task_elems.append(coin)


class ModelGUI(GUI):

    def __init__(self, architecture, playground, agent, draw_sensors=False):
        super().__init__(playground, agent, draw_sensors=draw_sensors)
        self.architecture = architecture

    def _get_commands(self):
        # distance = (
        #    self._playground.agents[0].sensors[0]._values).reshape(1, -1)
        sensor_values = {
            'distance': self._playground.agents[0].sensors[0]._values,
            'rgb': self._playground.agents[0].sensors[1]._values,
            'bump': self._playground.agents[0].sensors[2]._values
        }
        self.architecture.update_sensors(sensor_values)
        command_dict = {
            self._keyboard_agent: self.architecture.run()
        }
        return command_dict
