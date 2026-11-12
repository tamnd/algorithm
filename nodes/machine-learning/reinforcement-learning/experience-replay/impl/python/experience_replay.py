# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/experience-replay/. The authors are listed in prov/05WE42.jsonl.

"""Experience replay: a circular buffer of transitions with uniform sampling.

A transition is a tuple (s, a, r, s_next, done). The buffer keeps the last
`capacity` transitions; a new one overwrites the oldest. Sampling draws
indices uniformly with replacement from the stored transitions.

replay_q_learning runs tabular Q-learning updates on minibatches drawn from a
buffer, so that data collected by any behavior policy is reused many times.
Cost: add is O(1), sample is O(B) for a minibatch of size B, memory is
O(capacity) transitions.
"""

import random
from typing import Any


class ReplayBuffer:
    """A fixed-capacity circular buffer of transitions."""

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self.data: list[Any] = []  # @line L1
        self.next = 0  # the slot that the next add writes

    def __len__(self) -> int:
        return len(self.data)

    def add(self, transition: Any) -> None:
        """Store a transition; overwrite the oldest one when the buffer is full."""
        if len(self.data) < self.capacity:
            self.data.append(transition)  # @line L3
        else:
            self.data[self.next] = transition  # @line L3
        self.next = (self.next + 1) % self.capacity  # @line L4

    def sample(self, batch_size: int, rng: random.Random) -> list[Any]:
        """Return batch_size transitions drawn uniformly with replacement."""
        if not self.data:
            raise ValueError("cannot sample from an empty buffer")
        n = len(self.data)
        return [self.data[rng.randrange(n)] for _ in range(batch_size)]  # @line L6

    def in_order(self) -> list[Any]:
        """Return the stored transitions from the oldest to the newest."""
        if len(self.data) < self.capacity:
            return list(self.data)
        return self.data[self.next:] + self.data[: self.next]


def collect(step, start: int, n_actions: int, buffer: ReplayBuffer, n_steps: int,
            rng: random.Random) -> None:
    """Act with the uniform random behavior policy for n_steps and store each transition.

    step(s, a) returns (r, s_next, done). An episode restarts at start after done.
    """
    s = start
    for _ in range(n_steps):
        a = rng.randrange(n_actions)  # @line L2
        r, s2, done = step(s, a)  # @line L2
        buffer.add((s, a, r, s2, done))
        s = start if done else s2


def replay_q_learning(buffer: ReplayBuffer, n_states: int, n_actions: int, gamma: float,
                      lr: float, n_updates: int, batch_size: int, rng: random.Random,
                      q: list[list[float]] | None = None) -> list[list[float]]:
    """Run n_updates minibatch Q-learning updates from the buffer; return the table Q."""
    if q is None:
        q = [[0.0] * n_actions for _ in range(n_states)]
    for _ in range(n_updates):  # @line L5
        for s, a, r, s2, done in buffer.sample(batch_size, rng):  # @line L6
            target = r if done else r + gamma * max(q[s2])  # @line L7
            q[s][a] += lr * (target - q[s][a])  # @line L7
    return q
