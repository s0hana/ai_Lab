import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

class RobotVisualizer:
    def __init__(self, robot):
        self.robot = robot
        self.running = True

        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25)

        ax_stop = plt.axes([0.7, 0.05, 0.1, 0.075])
        self.btn_stop = Button(ax_stop, 'Stop')
        self.btn_stop.on_clicked(self.stop)

        ax_start = plt.axes([0.81, 0.05, 0.1, 0.075])
        self.btn_start = Button(ax_start, 'Start')
        self.btn_start.on_clicked(self.start)

    def stop(self, event):
        self.running = False

    def start(self, event):
        self.running = True

    def draw(self):
        self.ax.clear()
        grid = self.robot.environment.campus

        self.ax.imshow(grid, cmap='viridis')

        x, y = self.robot.position.get_coordinate()
        self.ax.plot(y, x, 'ro')

        for (vx, vy) in self.robot.visited:
            self.ax.plot(vy, vx, 'w.', markersize=1)

        self.ax.set_title("Robot Animation")

    def update(self, frame):
        if self.running:
            self.robot.drive_one_step(frame)

        self.draw()

    def animate(self):
        self.ani = FuncAnimation(self.fig, self.update, interval=50)
        plt.show()