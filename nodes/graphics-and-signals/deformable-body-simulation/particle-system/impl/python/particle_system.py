# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/particle-system/. The authors are listed in prov/8JJ5P6.jsonl.

"""A 2D particle system with the emission, update and death rules of Reeves 1983.

Each frame does the steps of Reeves, Section 2: generate new particles, give
each one its attributes, remove the particles whose lifetime is over, and move
the others. Rendering is left out. Every random attribute is a mean plus
Rand() times a variance, where Rand() is uniform in [-1, 1] (Reeves, Sections
2.1 and 2.2). The motion uses symplectic Euler (velocity first) with a constant
acceleration; Reeves adds the acceleration to the velocity and the velocity to
the position once per frame, and does not fix the order, so the order here is
our choice. Positions are (x, y) with y up, in metres.
"""

import math

GRAVITY = (0.0, -9.81)


def rand_pm1(rng):
    """Reeves's Rand(): a uniform number in [-1, 1]."""
    return 2.0 * rng.random() - 1.0


class Params:
    """The parameters of one particle system. Each pair (mean, var) gives the range mean +- var."""

    def __init__(self, mean_parts=10.0, delta_mean_parts=0.0, var_parts=0.0,
                 radius=0.0, ejection=0.0, mean_speed=1.0, var_speed=0.0,
                 mean_life=10, var_life=0, accel=GRAVITY, floor=None):
        self.mean_parts = mean_parts
        self.delta_mean_parts = delta_mean_parts
        self.var_parts = var_parts
        self.radius = radius          # generation shape: segment of half width radius on the x axis
        self.ejection = ejection      # largest angle from the vertical, in radians
        self.mean_speed = mean_speed
        self.var_speed = var_speed
        self.mean_life = mean_life    # lifetime in frames
        self.var_life = var_life
        self.accel = accel
        self.floor = floor            # region of interest: kill particles with y < floor


class Particle:
    __slots__ = ("x", "v", "life", "ident")

    def __init__(self, x, v, life, ident):
        self.x = x
        self.v = v
        self.life = life
        self.ident = ident


class ParticleSystem:
    def __init__(self, params, origin=(0.0, 0.0), f0=0):
        self.p = params
        self.origin = origin
        self.f0 = f0
        self.frame = f0
        self.particles = []
        self.next_ident = 0

    def emit_count(self, rng):
        p = self.p
        mean = p.mean_parts + p.delta_mean_parts * (self.frame - self.f0)  # @line L1
        return max(0, int(math.floor(mean + rand_pm1(rng) * p.var_parts + 0.5)))  # @line L2

    def new_particle(self, rng):
        p = self.p
        x = (self.origin[0] + rand_pm1(rng) * p.radius, self.origin[1])
        angle = rand_pm1(rng) * p.ejection
        speed = p.mean_speed + rand_pm1(rng) * p.var_speed
        v = (speed * math.sin(angle), speed * math.cos(angle))
        life = max(1, int(math.floor(p.mean_life + rand_pm1(rng) * p.var_life + 0.5)))
        part = Particle(x, v, life, self.next_ident)  # @line L3
        self.next_ident += 1
        return part

    def step(self, dt, rng):
        """Compute one frame and return the number of particles born in it."""
        n = self.emit_count(rng)
        for _ in range(n):
            self.particles.append(self.new_particle(rng))
        floor = self.p.floor
        self.particles = [q for q in self.particles  # @line L4
                          if q.life > 0 and (floor is None or q.x[1] >= floor)]
        ax, ay = self.p.accel
        for q in self.particles:
            q.v = (q.v[0] + dt * ax, q.v[1] + dt * ay)  # @line L5
            q.x = (q.x[0] + dt * q.v[0], q.x[1] + dt * q.v[1])  # @line L6
            q.life -= 1  # @line L7
        self.frame += 1
        return n

    def alive(self):
        return len(self.particles)

    def state(self):
        return [(q.ident, q.x, q.v, q.life) for q in self.particles]


def free_fall(y0, steps, dt, g=9.81, order="symplectic"):
    """Height of one particle dropped from rest. order is "symplectic" or "explicit"."""
    y, v = y0, 0.0
    for _ in range(steps):
        if order == "symplectic":
            v -= dt * g
            y += dt * v
        else:
            y += dt * v
            v -= dt * g
    return y
