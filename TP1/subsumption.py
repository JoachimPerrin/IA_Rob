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
        self.behaviors.sort(key=lambda x: x.priority)
        for b in self.behaviors:
            print(b.priority)
        print("done")
    

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
        
        test = 5
        action = {'forward': 0.0, 'angular': 0.0}
        for behavior in self.behaviors:
            action = behavior.execute(self.sensors_data)
            if behavior.is_active():
                test = behavior.priority
                break

        print(f"Choose behaviors {test}")
        print(self.sensors_data)
        return action
