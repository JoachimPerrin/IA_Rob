from abc import ABC, abstractmethod
import numpy as np


class Behavior(ABC):
    def __init__(self, priority):
        self.priority = priority
        self.active = False

    @abstractmethod
    def execute(self, sensors_data):
        """Execute the behavior.

        Parameters
        ----------
        sensors_data : dict
            The sensory data from the environment.


        Returns
        -------
        dict
            The action to be taken by the behavior, of the form:
            {
                'forward': float between -1 and 1,
                'angular': float between -1 and 1
            }
        """
        pass

    def is_active(self):
        return self.active


class MoveForwardInRandomDirection(Behavior):
    def __init__(self):
        ...

    def execute(self, sensors_data):
        ...


class MoveTowardsCoin(Behavior):
    def __init__(self):
        ...

    def execute(self, sensors_data):
        ...


class AvoidObstacles(Behavior):
    def __init__(self):
        ...

    def execute(self, sensors_data):
        ...


class Bump(Behavior):
    def __init__(self):
        ...

    def execute(self, sensors_data):
        ...
