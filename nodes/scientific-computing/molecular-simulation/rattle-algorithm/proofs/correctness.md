---
title: RATTLE solves the constrained velocity Verlet equations, keeps both constraints, is time-reversible, and gives the SHAKE positions
proves: [correctness]
status: full
---

We use the line numbers of the pseudocode. There are $N$ atoms with inverse masses $w_i \ge 0$, forces $f(x)$, and constraints $c = (i, j, d_c)$ with $\sigma_c(x) = \frac12 (|x_i - x_j|^2 - d_c^2)$. Let $G(x)$ be the $C \times 3N$ matrix whose row $c$ is $\nabla \sigma_c(x)$: it has $x_i - x_j$ at atom $i$, $-(x_i - x_j)$ at atom $j$ and 0 elsewhere. Let $W$ be the diagonal matrix of inverse masses. The RATTLE equations of Andersen (1983) for one step from $(x^0, v^0)$ are
$$\begin{aligned} v^{1/2} &= v^0 + \tfrac{h}{2} W \bigl(f(x^0) - G(x^0)^{\mathsf T} \lambda\bigr), & x^1 &= x^0 + h v^{1/2}, & \sigma(x^1) &= 0, \\ v^1 &= v^{1/2} + \tfrac{h}{2} W \bigl(f(x^1) - G(x^1)^{\mathsf T} \mu\bigr), & & & G(x^1) v^1 &= 0. \end{aligned}$$
The unknowns are $x^1$, $v^{1/2}$, $v^1$ and the multipliers $\lambda, \mu \in \mathbb{R}^C$. The equation $G(x) v = 0$ is the time derivative of $\sigma(x) = 0$: each bond has zero relative velocity along itself.

**Claim 1 (the position stage).** After the loop of line L3, $x^1 = x^0 + h v^{1/2}$, $v^{1/2} - v^0 - \frac{h}{2} W f(x^0) = -W G(x^0)^{\mathsf T} \gamma$ for some $\gamma$, and every bond holds to the tolerance.

*Proof.* Lines L1 and L2 start the identities with $\gamma = 0$. Each update of line L4 adds $w_i g r_c$ to $x_i$ and $w_i g r_c / h$ to $v_i$, and subtracts the same from atom $j$, where $r_c$ is the bond vector at $x^0$. So $x - h v^{1/2}$ does not change, and $v^{1/2}$ changes by $\frac{g}{h} W$ times row $c$ of $G(x^0)$, so the identity holds with $\gamma_c$ the sum of the values $-g / h$ for constraint $c$. The formula for $g$ is the Newton step of the SHAKE page, and the loop ends only after a sweep with no correction, so every bond holds to the tolerance. $\square$

With $\lambda = 2\gamma / h$ this is the first line of the RATTLE equations.

**Claim 2 (the velocity stage).** After the loop of line L7, $v^1 - v^{1/2} - \frac{h}{2} W f(x^1) = -W G(x^1)^{\mathsf T} \delta$ for some $\delta$, and $|G(x^1) v^1|_c \le \tau d_c^2$ for every constraint.

*Proof.* Line L6 starts the identity with $\delta = 0$. Line L8 adds $w_i k r$ to $v_i$ and subtracts $w_j k r$ from $v_j$, where $r = x^1_i - x^1_j$ is row $c$ of $G(x^1)$ at atom $i$. Its change of $r \cdot (v_i - v_j)$ is $(w_i + w_j) k |r|^2$, and since $|r| = d_c$ up to the tolerance of Claim 1, $k = -r \cdot v_{ij} / ((w_i + w_j) d_c^2)$ makes $r \cdot v_{ij}$ zero up to that tolerance. The loop ends only after a sweep in which every constraint passed the test. $\square$

The velocity equations are linear in $\delta$ with the matrix $G(x^1) W G(x^1)^{\mathsf T}$, which is symmetric and positive definite when the rows of $W^{1/2} G(x^1)$ are linearly independent. Then the Gauss-Seidel sweeps of line L7 converge for every start, by the classical theorem on the Gauss-Seidel method. The position stage is the SHAKE iteration and converges near a solution under the condition proved on the [SHAKE](/shake-constraint-algorithm/) page.

**Claim 3 (time reversal).** Suppose $(x^0, v^0)$ satisfies both constraints, and that the RATTLE equations have locally unique solutions. If one step maps $(x^0, v^0)$ to $(x^1, v^1)$, then one step maps $(x^1, -v^1)$ to $(x^0, -v^0)$.

*Proof.* Start from $(x^1, -v^1)$ and try the multiplier $\mu$ in the first stage:
$$-v^1 + \tfrac{h}{2} W \bigl(f(x^1) - G(x^1)^{\mathsf T} \mu\bigr) = -v^{1/2},$$
by the third equation of the forward step. Then the new position is $x^1 - h v^{1/2} = x^0$, which satisfies $\sigma(x^0) = 0$, so $\mu$ solves the position stage. In the second stage try $\lambda$: $-v^{1/2} + \frac{h}{2} W (f(x^0) - G(x^0)^{\mathsf T} \lambda) = -v^0$ by the first equation of the forward step, and $G(x^0)(-v^0) = 0$ by the assumption on the start. By uniqueness these are the solutions. $\square$

The test runs 200 steps forward and 200 back with the velocities reversed and returns to the start within $10^{-9}$.

**Claim 4 (the positions are those of SHAKE).** If $x^{n-1}, x^n, x^{n+1}$ are three positions of a RATTLE run, then $x^{n+1} = 2x^n - x^{n-1} + h^2 W f(x^n) - h^2 W G(x^n)^{\mathsf T} \nu$ for some $\nu$, and $\sigma(x^{n+1}) = 0$. So, from the same two starting positions, RATTLE and the constrained position Verlet method of the SHAKE page give the same positions, as long as the SHAKE equations have a locally unique solution.

*Proof.* From the equations of two consecutive steps, $v^{n+1/2} - v^{n-1/2} = h W f(x^n) - \frac{h}{2} W G(x^n)^{\mathsf T} (\mu_{n-1} + \lambda_n)$, where $\mu_{n-1}$ comes from the second stage of step $n$ and $\lambda_n$ from the first stage of step $n + 1$. Both use $G(x^n)$. Multiply by $h$ and use $x^{n+1} - x^n = h v^{n+1/2}$ and $x^n - x^{n-1} = h v^{n-1/2}$, with $\nu = \frac12 (\mu_{n-1} + \lambda_n)$. $\square$

**Claim 5 (order and symplecticity).** RATTLE is a symplectic map on the manifold of states that satisfy both constraints, and it has order 2. These are theorems of Leimkuhler and Skeel (1994), also proved by Hairer, Lubich and Wanner (2006) for constrained mechanical systems. We do not repeat the proofs. The test checks the consequences: for a pendulum the map preserves the area $d\theta \, d\omega$ to $10^{-7}$, the period error falls by a factor of 4 when $h$ is halved, and the energy error does not grow over thirty periods.

In floating-point arithmetic with a tolerance $\tau$, every claim holds up to errors of size $\tau$ and rounding. Claim 3 needs a tight tolerance: a loose one breaks reversibility and symplecticity, and the energy then drifts.
