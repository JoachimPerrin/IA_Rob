
from spg.element.wall import ColorWall
from spg.playground import ConnectedRooms
from spg.view import GUI
from spg.agent.agent import Agent
from spg.agent.part import ForwardBase
from spg.agent.sensor import DistanceSensor


class ExampleAgent(Agent):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        base = ForwardBase(linear_ratio=1, angular_ratio=0.3)
        self.add(base)

        # SENSORS
        self.distance = DistanceSensor(
            fov=360,
            resolution=32,
            max_range=100,
            invisible_elements=self._parts,
            normalize=True,
        )
        self.base.add(self.distance)


class ExampleRoom(ConnectedRooms):
    def __init__(self):

        n_w = 3
        n_h = 3

        super().__init__(
            room_layout=(n_w, n_h),
            size_room=(200, 200),
            doorstep_length=100,
            centered_doorstep=True,
            background=(23, 73, 71),
            wall_cls=ColorWall,
            seed=1,
        )

        self.agent = ExampleAgent()

        self.add(
            self.agent, self._room_coordinate_sampler[-1], allow_overlapping=True)


class ModelGUI(GUI):

    def __init__(self, model, playground, agent, draw_sensors=False):
        super().__init__(playground, agent, draw_sensors=draw_sensors)
        self.model = model

    def _get_commands(self):
        try:
            distance = (
                self._playground.agents[0].sensors[0]._values).reshape(1, -1)
            action = round(self.model.predict(distance).item()) * 0.2
            command_dict = {
                self._keyboard_agent: {
                    'forward': 0.2,
                    'angular': action
                }
            }
            return command_dict

        except:
            pass
