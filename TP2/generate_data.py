import math

from spg.agent import HeadAgent
from spg.element.wall import ColorWall
from spg.playground import ConnectedRooms
from spg.view import HeadAgentGUI
from spg.agent.sensor import RGBSensor

import numpy as np
import pickle as pk


import math

from spg.agent.agent import Agent
from spg.agent.part import ForwardBase, Head
from spg.agent.sensor import DistanceSensor, RGBSensor

starting_room = -1
sensory_states = [[]]
actions = [[]]
limit = 5
epoch = 0
starting = True


class ExampleAgent(Agent):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        base = ForwardBase(linear_ratio=1, angular_ratio=0.3)
        self.add(base)

        # SENSORS
        self.distance = DistanceSensor(
            fov=360,
            resolution=32,
            max_range=150,
            invisible_elements=self._parts,
            normalize=True,
        )
        # self.rgb = RGBSensor(
        #     fov=180,
        #     resolution=32,
        #     max_range=600,
        #     invisible_elements=self._parts,
        #     invisible_when_grasped=True,
        # )
        self.base.add(self.distance)
        # self.base.add(self.rgb)


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
            self.agent, self._room_coordinate_sampler[starting_room], allow_overlapping=True)


playground = ExampleRoom()


def on_update(self, _):
    global epoch
    global starting
    commands = self._get_commands()
    self._playground.step(commands=commands, messages=self._message)

    if self.print_rewards:

        for agent in self._playground.agents:
            if agent.reward != 0:
                print(agent.reward)

    if self.print_messages:

        for agent in self._playground.agents:
            for comm in agent.communicators:
                for _, msg in comm.received_messages:
                    print(f"Agent {agent.name} received message {msg}")

    self._message = {}

    x, y = self._playground.agents[0].position
    if max(abs(x + 200),  abs(y + 200)) < 100:
        epoch += 1
        print(epoch)
        if epoch == limit:
            pk.dump(sensory_states, open(
                f"sensory_states_wall.pk", "wb"))
            pk.dump(actions, open(f"actions_wall.pk", "wb"))
            quit()

        else:
            sensory_states.append([])
            actions.append([])
            starting = True
            self._playground.reset()
    else:

        command_dict = list(commands.values())[0]
        action = [
            command_dict["angular"] if "angular" in command_dict else 0,
            command_dict["forward"] if "forward" in command_dict else 0
        ]

        if not starting or (action[0] != 0 or action[1] != 0):
            if starting:
                starting = False
                print("Now started")
            actions.append(action)
            distance = (
                self._playground.agents[0].sensors[0]._values).reshape(-1, 1)
            # rgb = self._playground.agents[0].sensors[1]._values
            # sensory_states.append(np.concatenate([rgb, distance], axis=1))
            sensory_states.append(distance)


HeadAgentGUI.on_update = on_update
gui = HeadAgentGUI(playground, playground.agent, draw_sensors=True)
gui.run()
