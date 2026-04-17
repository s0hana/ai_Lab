class Performance:
    def __init__(self, robot):
        self.robot = robot
        self.environment = robot.environment

    def calculate(self):
        collected_objects = len(self.robot.collected_objects)
        total_moves = self.robot.movement_actions
        total_actions = (
            self.robot.movement_actions +
            self.robot.cleaning_actions +
            self.robot.biohazard_checks +
            self.robot.accessibility_checks
        )

        if total_moves > 0:
            efficiency = (collected_objects / total_moves)*100
        else:
            efficiency = 0

        total_humans = len(self.environment.get_human_positions())
        total_acc = len(self.environment.get_accessible_positions())

        human_percentage = (total_humans / total_acc) * 100

        print("----- Performance Report -----")
        print(f"Collected objects: {collected_objects}")
        print(f"Total actions: {total_actions}")
        print(f"Total moves: {total_moves}")
        print(f"Efficiency (objects per move): {efficiency:.4f}%")
        print(f"Total humans: {total_humans}")
        print(f"Total accessible points: {total_acc}")