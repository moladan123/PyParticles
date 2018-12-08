import tkinter as tk
from random import randint
from random import random
from math import sqrt
from time import sleep


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def magnitude(self):
        return sqrt(self.x**2 + self.y**2)

    def normalized(self):
        if self.magnitude() != 0:
            return Vector(self.x/self.magnitude(), self.x/self.magnitude())
        else:
            return Vector(0, 0)

    def set_magnitude(self, magnitude: float):
        if magnitude == 0 or self.magnitude() == 0:
            self.x = 0
            self.y = 0
        else:
            self.x = self.x * magnitude / self.magnitude()
            self.y = self.y * magnitude / self.magnitude()

    def scaled(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class Particle:

    damping = 1.0

    def __init__(self, x, y, vx=0, vy=0, ax=0, ay=-1):
        """Need the position, velocity, and acceleration in
        order to create particle"""
        self.location = Vector(x, y)
        self.velocity = Vector(vx, vy)
        self.acceleration = Vector(ax, ay)

    def collide(self, other):
        self.velocity, other.velocity = \
            other.velocity.set_magnitude(self.velocity.magnitude() * Particle.damping), \
            self.velocity.set_magnitude(other.velocity.magnitude() * Particle.damping)

    def __str__(self):
        return "particle at " + str(self.location)


class ParticleSystem:
    particles = []

    def __init__(self, num_particles: int):
        if ParticleSystem.particles == []:
            ParticleSystem.particles = [Particle(randint(0, canvas_width), randint(0, canvas_height), vx=random(), vy=random()) for _ in range(num_particles)]

    def _integrate(self, delta_time):
        # calculate speeds from accelerations, and locations from speeds (use verlet integration when I learn how to do it)
        for particle in ParticleSystem.particles:
            try:
                particle.velocity += particle.acceleration.scaled(delta_time)
                particle.location += particle.velocity.scaled(delta_time)
            except:
                print(particle)

    def _calculate_collision(self):
        # calculate collisions
        particles = ParticleSystem.particles
        for i in range(len(particles)):
            for j in range(i + 1, len(particles)):
                # base collision naively based of whether they occupy the
                # same pixel. This only works since particles are 1 pixel each
                if particles[i].location == particles[j].location:
                    particles[i].collide(particles[j])

    def _check_bounds(self):
        for particle in ParticleSystem.particles:
            if particle.location.x < 0:
                particle.velocity.x = abs(particle.velocity.x)
            if particle.location.y < 0:
                particle.velocity.y = abs(particle.velocity.y)
            if particle.location.x > canvas_width:
                particle.velocity.x = -abs(particle.velocity.x)
            if particle.location.y > canvas_height:
                particle.velocity.y = -abs(particle.velocity.y)


    def simulate(self, delta_time):
        self._check_bounds()
        self._integrate(delta_time)
        self._calculate_collision()

NUM_PARTICLES_PER_CLICK = 10
FRAME_RATE = 60

canvas_width = 500
canvas_height = 150
master = tk.Tk()
master.title("Points")
w = tk.Canvas(master,
           width=canvas_width,
           height=canvas_height)


# seems kinda weird to put it here but keeping
# it anywhere else crashes the program
def paint(event):
    w.delete("all")

    for particle in ParticleSystem.particles:
        draw_point(particle)

    #create_explosion(event.x, event.y)
    ParticleSystem(100).simulate(1/2)

    print([str(particle) for particle in ParticleSystem.particles])

w.pack(expand=tk.YES, fill=tk.BOTH)
w.bind("<B1-Motion>", paint)

message = tk.Label(master, text="Particles")
message.pack(side=tk.BOTTOM)


def draw_point(particle, random=True):
    x, y = particle.location.x, particle.location.y
    if random:
        color = "#" + "".join([str(randint(0, 9)) for _ in range(6)])
    else:
        color = "#555555"
    w.create_oval(x, y, x, y, fill=color, outline="")


def create_explosion(x, y):
    for i in range(NUM_PARTICLES_PER_CLICK):
        ParticleSystem.particles.append(Particle(x, y, vx=random(), vy=random()))


if __name__ == "__main__":
    p = ParticleSystem(100)

    tk.mainloop()
