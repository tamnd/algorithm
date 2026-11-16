# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monte-carlo-localization/. The authors are listed in prov/GRKHHG.jsonl.

"""Monte Carlo localization (MCL) and augmented MCL.

The notation follows Thrun, Burgard and Fox (2005), Sections 8.3 and 8.3.5.
The belief is a list of N particles, each a pose. The models are callables:

  sample_motion(rng, x, u)   one draw of x_t from p(x_t | u_t, x_{t-1} = x, m)
  likelihood(z, x)           p(z_t | x_t = x, m), a number >= 0
  sample_pose(rng)           one pose drawn uniformly from the free space

A pose can be any value that these callables accept. rng is a random.Random.
"""

import robest


class Recovery:
    """The state of the random particle injection of augmented MCL.

    w_slow and w_fast are averages of the mean weight with the rates
    a_slow < a_fast. When the short term average falls below the long term
    average, a fraction max(0, 1 - w_fast / w_slow) of the new particles
    are random poses. This is a heuristic: it has no guarantee to find the
    true pose, and a_slow and a_fast are set by hand.
    """

    def __init__(self, a_slow, a_fast, sample_pose):
        if not 0.0 <= a_slow < a_fast <= 1.0:
            raise ValueError("need 0 <= a_slow < a_fast <= 1")
        self.a_slow = a_slow
        self.a_fast = a_fast
        self.sample_pose = sample_pose
        self.w_slow = 0.0
        self.w_fast = 0.0

    def observe(self, w_avg):
        """Update both averages with the mean weight of one step."""
        self.w_slow += self.a_slow * (w_avg - self.w_slow)
        self.w_fast += self.a_fast * (w_avg - self.w_fast)

    def p_random(self):
        """Return the probability to replace a new particle by a random pose."""
        if self.w_slow <= 0.0:
            return 0.0
        return max(0.0, 1.0 - self.w_fast / self.w_slow)


def mcl(particles, u, z, sample_motion, likelihood, rng, recovery=None):
    """One step of MCL, or of augmented MCL if recovery is a Recovery.

    Return (the new particles, the mean weight w_avg). Plain MCL raises
    ValueError if every weight is 0, because then no particle explains z.
    Augmented MCL then keeps the moved particles and lets the injection act.
    """
    n = len(particles)
    if n == 0:
        raise ValueError("no particles")
    moved, weights = [], []
    for x in particles:  # @line L1
        xm = sample_motion(rng, x, u)  # @line L2
        moved.append(xm)
        weights.append(likelihood(z, xm))  # @line L3
    w_avg = sum(weights) / n  # @line L4
    if recovery is not None:
        recovery.observe(w_avg)  # @line L5
    if w_avg <= 0.0:
        if recovery is None:
            raise ValueError("every particle has weight 0")
        weights = [1.0] * n
    new = [moved[i] for i in robest.low_variance_resample(rng, weights)]  # @line L6
    if recovery is not None:
        p = recovery.p_random()
        for k in range(n):  # @line L7
            if rng.random() < p:
                new[k] = recovery.sample_pose(rng)
    return new, w_avg  # @line L8
