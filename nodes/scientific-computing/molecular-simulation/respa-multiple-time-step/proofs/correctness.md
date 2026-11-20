---
title: r-RESPA is a symmetric composition of exact Hamiltonian flows, so it is symplectic, reversible and of order 2, and it is unstable near half a fast period
proves: [correctness]
status: full
---

We use the line numbers of the pseudocode. The state is $(x, v)$, $W$ is the diagonal matrix of inverse masses, and the force is $F = F_{\text{fast}} + F_{\text{slow}}$ with $F_{\text{fast}} = -\nabla U_{\text{fast}}$ and $F_{\text{slow}} = -\nabla U_{\text{slow}}$. Define three maps for a time $t$:
$$\mathcal{K}^{\text{s}}_t(x, v) = (x, v + t W F_{\text{slow}}(x)), \qquad \mathcal{K}^{\text{f}}_t(x, v) = (x, v + t W F_{\text{fast}}(x)), \qquad \mathcal{D}_t(x, v) = (x + t v, v).$$
Each is the exact flow for time $t$ of a Hamiltonian: $U_{\text{slow}}(x)$, $U_{\text{fast}}(x)$ and the kinetic energy $\frac12 v^{\mathsf T} W^{-1} v$, in the coordinates $(x, W^{-1} v)$.

**Claim 1 (the step).** With $\delta = h / n$, one call of `respa_step` is
$$\Psi_h = \mathcal{K}^{\text{s}}_{h/2} \circ \bigl(\mathcal{K}^{\text{f}}_{\delta/2} \circ \mathcal{D}_\delta \circ \mathcal{K}^{\text{f}}_{\delta/2}\bigr)^n \circ \mathcal{K}^{\text{s}}_{h/2}.$$

*Proof.* Line L1 is $\mathcal{K}^{\text{s}}_{h/2}$. Each pass of the loop of line L2 applies line L3, a fast half kick at the current $x$, line L4, a drift, and line L5, a fast half kick at the new $x$, which is $\mathcal{K}^{\text{f}}_{\delta/2} \circ \mathcal{D}_\delta \circ \mathcal{K}^{\text{f}}_{\delta/2}$. The code computes the fast force once per pass, because the force at the end of one pass is the force at the start of the next. Line L6 is $\mathcal{K}^{\text{s}}_{h/2}$ at the final $x$. $\square$

**Claim 2 (special cases).** For $n = 1$, $\Psi_h$ is the velocity Verlet step with the full force $F$. For $F_{\text{slow}} = 0$, $\Psi_h$ is $n$ velocity Verlet steps of size $\delta$ with the force $F_{\text{fast}}$.

*Proof.* Kicks change only $v$ by an amount that depends only on $x$, so any two kicks commute, and $\mathcal{K}^{\text{s}}_t \circ \mathcal{K}^{\text{f}}_t = \mathcal{K}_t$, the kick with the full force. For $n = 1$, $\Psi_h = \mathcal{K}_{h/2} \circ \mathcal{D}_h \circ \mathcal{K}_{h/2}$, the velocity Verlet step. For $F_{\text{slow}} = 0$ the slow kicks are the identity. $\square$

**Claim 3 (symplectic).** $\Psi_h$ is a symplectic map.

*Proof.* The exact flow of a Hamiltonian system is symplectic, and a composition of symplectic maps is symplectic. $\square$

**Claim 4 (time reversal).** Let $R(x, v) = (x, -v)$. Then $R \circ \Psi_h \circ R = \Psi_h^{-1}$: from $(x', -v')$ with $(x', v') = \Psi_h(x, v)$, one step returns to $(x, -v)$.

*Proof.* For each of the three maps, $R \circ \mathcal{M}_t \circ R = \mathcal{M}_{-t} = \mathcal{M}_t^{-1}$: for a kick, $R$ flips the sign of the velocity change, and for a drift, $R$ flips the sign of the position change. $R \circ R$ is the identity, so $R \circ \Psi_h \circ R$ is the same composition with each $t$ replaced by $-t$, and since the list of factors reads the same from both ends, this is the inverse of $\Psi_h$. $\square$

**Claim 5 (order 2).** For a fixed $n$ and smooth forces, the local error of $\Psi_h$ is $O(h^3)$, so the global error over a fixed time is $O(h^2)$.

*Proof.* Each factor agrees with the identity plus $t$ times its vector field up to $O(t^2)$, so the composition agrees with the exact flow of $F$ up to $O(h^2)$: the method has order at least 1. A method whose map satisfies $\Psi_{-h} = \Psi_h^{-1}$ has even order (Hairer, Lubich and Wanner, the theorem on symmetric methods). The palindromic composition of Claim 4 with $h$ replaced by $-h$ is the same composition with all times negated, which is $\Psi_h^{-1}$, so $\Psi_h$ is symmetric and its order is at least 2. $\square$

The test measures the largest energy error over $t \le 20$ for a fast spring of frequency $\Omega = 10$ and a slow pendulum force: it falls from 0.293 to 0.0707, a factor of 4.15, when $h$ is halved with $n = 10$.

**Claim 6 (resonance in the linear model, a theorem).** Let $x$ be one coordinate with $w = 1$, $F_{\text{fast}} = -\Omega^2 x$ and $F_{\text{slow}} = -\kappa x$ with $\kappa > 0$, and replace the inner loop by the exact rotation of the fast oscillator over time $h$, which is its limit as $n \to \infty$. Then the step matrix has determinant 1 and trace
$$\operatorname{tr} = 2 \cos(\Omega h) - \frac{\kappa h}{\Omega} \sin(\Omega h),$$
and for each $\kappa > 0$ there are steps $h$ just below $\pi / \Omega$ with $|\operatorname{tr}| > 2$, where the method is unstable.

*Proof.* The rotation is $R = \begin{pmatrix} \cos \Omega h & \sin(\Omega h)/\Omega \\ -\Omega \sin \Omega h & \cos \Omega h \end{pmatrix}$, and the slow half kick is $K = \begin{pmatrix} 1 & 0 \\ -a & 1 \end{pmatrix}$ with $a = \kappa h / 2$. Both have determinant 1, so $K R K$ does. Its trace is $2\cos \Omega h - 2a \sin(\Omega h)/\Omega$. Put $\Omega h = \pi - \varepsilon$ with small $\varepsilon > 0$: $\operatorname{tr} = -2 + \varepsilon^2 - \frac{\kappa h}{\Omega} \varepsilon + O(\varepsilon^3)$, which is below $-2$ when $\varepsilon < \kappa h / \Omega$ up to higher order. A real $2 \times 2$ matrix with determinant 1 and $|\operatorname{tr}| > 2$ has a real eigenvalue of modulus above 1, so the iterates grow exponentially. $\square$

The width of the unstable band in $h$ is about $\kappa \pi / \Omega^3$, small when the slow force is weak, but it is there for every $\kappa > 0$, and the same holds near every multiple of $\pi / \Omega$. In the test, $\Omega = 10$, $\kappa = 1$ and $h = (\pi - 0.015)/10$ give a trace of $-2.0002$, and 3000 steps make the amplitude grow by a factor of more than $10^{19}$. For nonlinear systems, Ma, Izaguirre and Skeel (2003) report instabilities when $h$ is as small as a third, or possibly a fourth, of the period of the fastest motion. That bound is a measurement and an analysis of model problems, not a theorem for all force fields.
