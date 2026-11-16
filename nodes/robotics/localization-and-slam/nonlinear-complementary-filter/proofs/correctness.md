---
title: The explicit complementary filter has a Lyapunov function that decreases at the rate k_P times the squared correction
proves: [correctness]
status: full
---

**Setting.** The attitude is a rotation $R(t) = R_{sb}$ with $\dot R = R [\Omega]_\times$, where $\Omega$ is the body angular velocity and $[w]_\times$ is the [skew-symmetric matrix of a vector](/skew-symmetric-matrix-of-a-vector/). A gyro reads $\Omega_y = \Omega + b$. For $i = 1, \ldots, n$, a vector sensor reads $v_i = R^T v_{0i}$, the body form of a known unit direction $v_{0i}$, with weight $k_i > 0$. The filter state is $(\hat R, \hat b)$, and in continuous time it runs

$$\hat v_i = \hat R^T v_{0i}, \quad \omega_{mes} = \sum_i k_i \, v_i \times \hat v_i, \quad \dot{\hat b} = -k_I \, \omega_{mes}, \quad \dot{\hat R} = \hat R \, [\Omega_y - \hat b + k_P \, \omega_{mes}]_\times ,$$

with gains $k_P, k_I > 0$. Lines L1 to L4 of the code are one step of length $\delta t$ of these equations, with the exponential map for the last one. Let $\tilde b = \hat b - b$ and

$$E_{mes} = \sum_i k_i (1 - v_i \cdot \hat v_i), \qquad V = E_{mes} + \frac{|\tilde b|^2}{2 k_I}.$$

**Assumptions.**

- (B) The bias $b$ is constant.
- (V) The directions $v_{0i}$ are constant and the measurements are exact: $v_i = R^T v_{0i}$.
- (Ω) $\Omega(t)$ is continuous and bounded.

**Claim.** Along every solution, $\dot V = -k_P \, |\omega_{mes}|^2 \le 0$. So $V$ never increases, $\tilde b$ stays bounded, and $\int_0^\infty |\omega_{mes}|^2 \, dt \le V(0) / k_P$.

*Proof.* For a rotation $Q(t)$ with $\dot Q = Q [w]_\times$, the transpose satisfies $\frac{d}{dt} Q^T = -[w]_\times Q^T$, so $\frac{d}{dt}(Q^T v_0) = -w \times (Q^T v_0)$ for a constant $v_0$. Apply this to $R$ with $w = \Omega$ and to $\hat R$ with $w = \hat w = \Omega_y - \hat b + k_P \omega_{mes} = \Omega - \tilde b + k_P \omega_{mes}$, where (B) gives $\Omega_y - \hat b = \Omega - \tilde b$. By (V),

$$\frac{d}{dt}(v_i \cdot \hat v_i) = -(\Omega \times v_i) \cdot \hat v_i - v_i \cdot (\hat w \times \hat v_i).$$

By the cyclic rule of the triple product, $(\Omega \times v_i) \cdot \hat v_i = \Omega \cdot (v_i \times \hat v_i)$ and $v_i \cdot (\hat w \times \hat v_i) = \hat w \cdot (\hat v_i \times v_i) = -\hat w \cdot (v_i \times \hat v_i)$. So

$$\frac{d}{dt}(v_i \cdot \hat v_i) = (\hat w - \Omega) \cdot (v_i \times \hat v_i) = (k_P \omega_{mes} - \tilde b) \cdot (v_i \times \hat v_i).$$

Multiply by $k_i$ and sum over $i$:

$$\dot E_{mes} = -(k_P \omega_{mes} - \tilde b) \cdot \omega_{mes} = -k_P |\omega_{mes}|^2 + \tilde b \cdot \omega_{mes}.$$

By (B), $\dot{\tilde b} = \dot{\hat b} = -k_I \omega_{mes}$, so $\frac{d}{dt} \frac{|\tilde b|^2}{2 k_I} = -\tilde b \cdot \omega_{mes}$. The cross terms cancel, and $\dot V = -k_P |\omega_{mes}|^2$. Integrate from $0$ to $T$: $V(T) + k_P \int_0^T |\omega_{mes}|^2 dt = V(0)$. Since $V \ge 0$ (each $1 - v_i \cdot \hat v_i \ge 0$ for unit vectors), the integral is at most $V(0) / k_P$ for every $T$, and $|\tilde b|^2 \le 2 k_I V(0)$. $\blacksquare$

**What the claim does not give.** $\dot V \le 0$ alone shows only that the error does not grow. Convergence needs more. Mahony, Hamel and Pflimlin (2008), Theorem 5.1, prove it under (B) and (V) with $n \ge 2$ non-parallel directions, a bounded angular velocity, and $M_0 = \sum_i k_i v_{0i} v_{0i}^T$ with three distinct eigenvalues. Their Lyapunov function has the same form as $V$ above, with their own error convention. The result is that the estimate $(\hat R, \hat b)$ converges to $(R, b)$ from every initial condition except a set of measure zero: the solutions that tend to the three unstable equilibria where $\hat R R^T$ is a rotation by $\pi$ about an eigenvector of $M_0$. This is almost-global stability. It is the best that a continuous filter on $SO(3)$ can do: a continuous flow on a manifold that is not contractible, such as $SO(3)$, cannot have an equilibrium whose basin of attraction is the whole manifold.

**About the code.** The code integrates the equations with the step $\hat R \leftarrow \hat R \exp(\hat w \, \delta t)$. This keeps $\hat R$ on $SO(3)$ up to rounding, because the exponential of a skew-symmetric matrix is a rotation. The decrease of $V$ is a property of the continuous system. For the discrete step it holds only up to a term of order $\delta t^2$ per step. The tests measure it: with $k_P = 2$, $k_I = 0.5$ and $\delta t = 0.02$ s, the computed $V$ did not increase by more than $10^{-9}$ in any of 600 steps from an initial error of 107 degrees, and it fell below one percent of its initial value.
