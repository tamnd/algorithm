---
title: The WCSPH step conserves linear and angular momentum
proves: [correctness]
status: full
---

We use the notation of the page.
The step has no walls (line L11 is skipped) and no gravity ($g = 0$).
The arithmetic is exact real arithmetic; in floating point the same identities hold up to rounding.
The masses are positive and constant.

## The pair term

**Lemma 1.** For $i \ne j$, $\nabla W_{ji} = -\nabla W_{ij}$, and $\nabla W_{ij} = f(r_{ij})\,(x_i - x_j)$ for a scalar $f(r_{ij})$ with $r_{ij} = |x_i - x_j|$.

*Proof.*
$W_{ij} = W(r_{ij}, h)$ depends on $x_i$ only through $r_{ij}$.
The chain rule gives $\nabla_{x_i} W_{ij} = W'(r_{ij})\,(x_i - x_j)/r_{ij}$ for $r_{ij} > 0$, so $f = W'/r$.
Swapping $i$ and $j$ changes the sign of $x_i - x_j$ and leaves $r_{ij}$ fixed.
At $r_{ij} = 0$ the gradient is 0, since the cubic spline has a smooth maximum there. $\square$

**Lemma 2.** The scalar $s$ of lines L6 and L7 is symmetric in $i$ and $j$.

*Proof.*
$p_i/\rho_i^2 + p_j/\rho_j^2$ is symmetric.
In $\Pi_{ij}$, the product $(v_i - v_j)\cdot(x_i - x_j)$ does not change when $i$ and $j$ swap, because both factors change sign.
The same holds for $|x_i - x_j|^2$ and $\bar\rho_{ij} = (\rho_i + \rho_j)/2$. $\square$

So the code may compute $s$ once per pair, as lines L5 to L8 do.

## Linear momentum

**Claim 1.** Let $P = \sum_i m_i v_i$. After lines L4 to L9, $P$ has the same value as before.

*Proof.*
With $g = 0$, line L4 sets every $a_i$ to 0.
Each pair $(i, j)$ in line L8 adds $-m_j s \nabla W_{ij}$ to $a_i$ and $+m_i s \nabla W_{ij}$ to $a_j$.
Its contribution to $\sum_k m_k a_k$ is $-m_i m_j s\nabla W_{ij} + m_j m_i s \nabla W_{ij} = 0$.
So $\sum_k m_k a_k = 0$ after line L8.
Line L9 changes $P$ by $\Delta t \sum_k m_k a_k = 0$. $\square$

## Angular momentum

In 2D the cross product of $a = (a_x, a_y)$ and $b = (b_x, b_y)$ is the scalar $a \times b = a_x b_y - a_y b_x$.
It is bilinear and $a \times a = 0$.

**Claim 2.** The total torque $\sum_k x_k \times m_k a_k$ of the forces of line L8 is 0.

*Proof.*
The pair $(i, j)$ adds $m_i m_j s$ times
$$-x_i \times \nabla W_{ij} + x_j \times \nabla W_{ij} = -(x_i - x_j)\times \nabla W_{ij}.$$
By Lemma 1, $\nabla W_{ij} = f\,(x_i - x_j)$, so this is $-f\,(x_i - x_j)\times(x_i - x_j) = 0$. $\square$

**Claim 3.** Let $L = \sum_k m_k\, x_k \times v_k$. After lines L9 and L10, $L$ has the same value as before.

*Proof.*
Write $x, v$ for the old state and $x', v'$ for the new state, with $v' = v + \Delta t\, a$ and $x' = x + \Delta t\, v'$.
Then
$$\sum_k m_k\, x'_k \times v'_k = \sum_k m_k\, x_k \times v'_k + \Delta t \sum_k m_k\, v'_k \times v'_k = \sum_k m_k\, x_k \times v'_k,$$
since $v'_k \times v'_k = 0$.
Next,
$$\sum_k m_k\, x_k \times v'_k = \sum_k m_k\, x_k \times v_k + \Delta t \sum_k x_k \times m_k a_k = L,$$
by Claim 2. $\square$

Claim 3 uses the order of lines L9 and L10.
The position update must use the new velocity; with the explicit Euler order ($x' = x + \Delta t\, v$, then $v' = v + \Delta t a$) the term $\Delta t^2 \sum_k m_k\, v_k \times a_k$ is left over, and $L$ drifts.

## Consistency of the state equation

**Claim 4.** For $\rho > 0$, the Tait pressure is 0 if and only if $\rho = \rho_0$, it is increasing in $\rho$, and its derivative at $\rho_0$ is $c^2$.

*Proof.*
$p(\rho) = B((\rho/\rho_0)^\gamma - 1)$ with $B > 0$ and $\gamma = 7$ is 0 exactly at $\rho = \rho_0$.
Its derivative is $p'(\rho) = B\gamma\rho^{\gamma - 1}/\rho_0^\gamma > 0$.
At $\rho_0$ it is $B\gamma/\rho_0 = c^2$, since $B = \rho_0 c^2/\gamma$. $\square$

So $c$ is the speed of sound of the discrete fluid near rest, and a compression $e = (\rho - \rho_0)/\rho_0$ gives $p = \rho_0 c^2 e + O(e^2)$.

Claims 1 and 3 hold for any positions, velocities, masses and step size, and for any $\alpha \ge 0$. They are the momentum laws of a closed system, kept exactly by the discrete step. $\blacksquare$
