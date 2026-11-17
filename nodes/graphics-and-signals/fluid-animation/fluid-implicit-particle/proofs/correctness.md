---
title: The end cases, the momentum and the energy of the FLIP transfer
proves: [correctness]
status: full
---

We use the notation of the page, with exact real arithmetic.
We write the claims for the $u$ faces; the $v$ faces are the same.
The masses are $m_p > 0$, $m_f = \sum_p w_{fp} m_p$ is the face mass of line L2, $u^{old}_f$ is the copy of line L3 and $u_f$ is the grid velocity after line L5.
The particle positions in line L6 are those of line L2.
The weights satisfy $w_{fp} \ge 0$ and $\sum_f w_{fp} = 1$ for each particle (the proof of the [PIC](/particle-in-cell/) page, Claim 1).
Line L6 is

$$u'_p = \alpha\left(u_p + \sum_f w_{fp}(u_f - u^{old}_f)\right) + (1 - \alpha)\sum_f w_{fp} u_f.$$

## The end cases

**Claim 1.** If $\alpha = 1$ and $u_f = u^{old}_f$ for every face, then $u'_p = u_p$ for every particle.

*Proof.*
Every term $u_f - u^{old}_f$ is 0, and the second term has the factor $1 - \alpha = 0$. $\square$

**Claim 2.** If $\alpha = 0$, then $u'_p = \sum_f w_{fp} u_f$, the PIC transfer.

*Proof.*
The first term has the factor 0. $\square$

## Linear momentum

**Claim 3.** For every $\alpha$, $\sum_p m_p u'_p = \sum_f m_f u_f$.

*Proof.*
Line L2 gives $m_f u^{old}_f = \sum_p w_{fp} m_p u_p$ for each face with mass, and a face with no mass has $w_{fp} = 0$ for all $p$.
So $\sum_f m_f u^{old}_f = \sum_p m_p u_p$.
For any face field $q_f$, $\sum_p m_p\sum_f w_{fp} q_f = \sum_f m_f q_f$.
Then

$$\sum_p m_p\left(u_p + \sum_f w_{fp}(u_f - u^{old}_f)\right) = \sum_f m_f u^{old}_f + \sum_f m_f(u_f - u^{old}_f) = \sum_f m_f u_f,$$

and the PIC term gives $\sum_f m_f u_f$ too.
A blend of two quantities that are both equal to $\sum_f m_f u_f$ is equal to it. $\square$

So the transfers add no momentum; only lines L4 and L5 change it (gravity and the walls).

## Energy

**Claim 4.** With $\alpha = 1$, line L6 can give a particle kinetic energy larger than the grid kinetic energy $\frac12\sum_f m_f u_f^2$ after line L5.

*Proof.*
Take a grid that does not change between lines L3 and L6.
By Claim 1, the particle energy after line L6 is the particle energy before line L2.
By Claim 4 of the PIC proof (Jensen's inequality), that energy is at least the grid energy after line L2, and it is strictly larger if two particles with different velocities have a weight on the same face.
The grid energy after line L5 is the grid energy after line L2, because the grid did not change. $\square$

So FLIP has no bound of the kind that PIC has: the particle energy is not limited by the grid energy.
The kinetic energy that the grid does not see stays on the particles, which is the reason for the low dissipation and also for the noise.

## Angular momentum

Line L6 does not keep the angular momentum in general.
With $\alpha = 0$ it is the PIC transfer, which loses angular momentum (the PIC page).
With $\alpha = 1$ and $u_f - u^{old}_f$ equal to a constant $\delta$ on every face, $u'_p = u_p + \delta$.
The particle angular momentum changes by $-\delta\sum_p m_p y_p$ and the grid angular momentum by $-\delta\sum_f m_f y_f$.
Without clamping these are equal (the PIC proof, Claim 2), but for a general change of the grid field the interpolated change $\sum_f w_{fp}(u_f - u^{old}_f)$ has the same defect as the PIC transfer. $\blacksquare$
