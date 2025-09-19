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
    def __init__(self, prio: int = 4):
        self.priority = prio
        self.active = True

    def execute(self, sensors_data):
        val = np.random.rand(2)
        return {"forward": val[0], "angular": val[1]}


class MoveTowardsCoin(Behavior):
    def __init__(self, prio: int = 3, tolerance: float = 0.9):
        self.priority = prio
        self.active = True
        self.tolerance = np.max(np.min(tolerance, 0.0), 1.0)

    def execute(self, sensors_data):
        if(sensors_data['rgb'][0] >= self.tolerance * 255 
           and sensors_data['rgb'][1] >= self.tolerance * 255 
           and sensors_data['rgb'][2] <= (1-self.tolerance) * 255):
            return {"forward": 1.0}

class AvoidObstacles(Behavior):
    def __init__(self, prio: int = 2, threshold: float = 0.5, ang_vel: float = 1.0):
        self.priority = prio
        self.active = True
        self.threshold = threshold
        self.ang_vel = np.max(np.min(ang_vel, 0.0), 1.0)

    def execute(self, sensors_data):
        if(sensors_data['distance'] < self.threshold):
            return {"angular": self.ang}

class Bump(Behavior):
    def __init__(self, prio: int = 1, reactivness: float = -1.0):
        self.priority = prio
        self.active = True
        self.reactivness = np.max(np.min(reactivness, -1.0), 0.0) # Clamp between -1.0 and 0.0

    def execute(self, sensors_data):
        if(self.sensor['bumb'] == True):
            return {"forward": self.reactivness}
