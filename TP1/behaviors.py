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
        return {'forward': val[0], 'angular': val[1]}

class MoveTowardsCoin(Behavior):
    def __init__(self, prio: int = 3):
        self.priority = prio
    
    def execute(self, sensors_data):
        colors = sensors_data['rgb']

        self.active = False
        
        if colors is not None:
            for color in colors:
                if color[0] == 255 and color[1] >= 215 and color[2] == 0:
                    self.active = True
                    
        if self.active:
            return {'forward': 1.0, 'angular':0.0}
        else:
            return {'forward':0.0, 'angular':0.0}


class AvoidObstacles(Behavior):
    def __init__(self, prio: int = 2):
        self.priority = prio

    def execute(self, sensors_data):
        dist = sensors_data['distance']
        print("HERE")
        print(dist)
        if dist is not None and np.any(dist < 1.0):
            self.active = True
            
            return {'forward': 0.5, 'angular': 1.0}
        else:
            self.active = False
            return {'forward': 0.0, 'angular': 0.0}

class Bump(Behavior):
    def __init__(self, prio: int = 1, reactivness: float = -1.0):
        self.priority = prio
        self.reactivness = reactivness

    def execute(self, sensors_data):
        bumps = sensors_data['bump']
        self.active = False
        if bumps is not None and np.any(bumps < 1.0):
            self.active = True
            return {'forward': self.reactivness, 'angular': 0.0}
        else:
            self.active = False
            return {'forward': 0.0, 'angular': 0.0}
