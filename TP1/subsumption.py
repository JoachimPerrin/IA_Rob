class SubsumptionArchitecture:
    """A subsumption architecture for behavior-based robotics.

    Attributes
    ----------
    behaviors : list
        A list of all behaviors in the architecture.
    sensors_data : dict
        The current sensory data from the environment.
    """

    def __init__(self):
        self.behaviors = []
        self.sensors_data = {}

    def add_behavior(self, behavior):
        self.behaviors.append(behavior)

    def update_sensors(self, sensors_data):
        self.sensors_data.update(sensors_data)

    def run(self):
        """Run the subsumption architecture.

        Returns
        -------
        dict
            The command to be executed by the robot, of the form:
            {
                'forward': float between -1 and 1,
                'angular': float between -1 and 1
            }
        """

        for prio in range(4):
            for behavior in behavior:
                if(behavior.is_active and behavior.priority == prio):
                    behavior.execute
                    break

        print(self.sensors_data)
        return {
            'forward': 0.5,
            'angular': 1.
        }
