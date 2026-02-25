class Performance:
    def __init__(self, robot):
        self.robot = robot

    def total_collected(self):
        return len(self.robot.get_collected_objects())

    def total_moves(self):
        return len(self.robot.get_move_history())

    def efficiency(self):
        moves = self.total_moves()
        if moves == 0:
            return 0
        return self.total_collected() / moves

    def summary(self):
        print("---- Robot Performance ----")
        print("Collected objects:", self.total_collected())
        print("Total moves:", self.total_moves())
        print("Total actions: ", self.total_collected()+self.total_moves())
        print("Efficiency (objects per move):", self.efficiency())

