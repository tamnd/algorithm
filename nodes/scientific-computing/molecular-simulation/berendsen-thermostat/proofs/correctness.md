---
title: The Berendsen scaling relaxes the kinetic energy at rate 1 / tau, and it does not give the canonical distribution
proves: [correctness]
status: full
---

We use the pseudocode of the page, with $K_0 = N_f k_B T / 2$ the target kinetic energy and $\tau \ge h$ the coupling time.

**Claim 1 (the scale factor is real).** If $K > 0$ and $\tau \ge h$, then $\lambda^2 = 1 + \frac{h}{\tau}\bigl(\frac{K_0}{K} - 1\bigr) \ge 0$, so line L8 is defined.

*Proof.* $K_0 / K > 0$, so $\lambda^2 > 1 - h / \tau \ge 0$. $\square$

For $\tau < h$ and $K$ much larger than $K_0$, $\lambda^2$ is negative. The implementation raises an error for $\tau < h$.

**Claim 2 (one scaling).** Let $K$ be the kinetic energy after the Verlet part of a step (line L7). After line L9 the kinetic energy is
$$K' = \lambda^2 K = K + \frac{h}{\tau}(K_0 - K).$$

*Proof.* Line L9 multiplies each velocity by $\lambda$, and $K$ is quadratic in the velocities, so $K' = \lambda^2 K$. Insert $\lambda^2$ from line L8. $\square$

So the scaling is the explicit Euler step, with step $h$, for $dK / dt = (K_0 - K) / \tau$. This is the equation that Berendsen et al. (1984) give for the temperature.

**Claim 3 (free particles).** If $f = 0$, then after $n$ steps $K_n - K_0 = (K_{\text{init}} - K_0)(1 - h/\tau)^n$.

*Proof.* With $f = 0$ the Verlet part does not change $v$, so $K$ before line L9 of step $n$ is $K_{n-1}$. Claim 2 gives $K_n - K_0 = (1 - h/\tau)(K_{n-1} - K_0)$. Induction on $n$ gives the claim. $\square$

**Claim 4 (not canonical).** There is a system for which the Berendsen dynamics does not have the canonical distribution as a limit: free particles.

*Proof.* In the canonical ensemble, $K$ has the gamma law with shape $N_f / 2$ and scale $k_B T$, with variance $N_f (k_B T)^2 / 2 > 0$. For free particles and $h \le \tau$, Claim 3 gives $|K_n - K_0| \le |K_{\text{init}} - K_0| (1 - h/\tau)^n$. For $h < \tau$ this tends to 0 for every start, so the law of $K_n$ tends to the point mass at $K_0$, with variance 0. For $h = \tau$, $K_n = K_0$ after one step. In both cases the limit is not the gamma law. $\square$

The free gas is a simple case, but the cause is general: the scaling is deterministic and always pushes $K$ toward $K_0$, and nothing adds the fluctuations back. On the harmonic test of the page, the variance of $K$ falls far below the canonical value (a measurement, given on the page). The scaling also does not keep the volume of phase space, so there is no Liouville argument for any invariant density.

**Claim 5 (weak coupling limit).** As $\tau \to \infty$ with $K$ bounded away from 0, $\lambda \to 1$, and the step tends to the velocity Verlet step.

*Proof.* $|\lambda^2 - 1| = \frac{h}{\tau} |K_0 / K - 1|$, which tends to 0. $\square$
