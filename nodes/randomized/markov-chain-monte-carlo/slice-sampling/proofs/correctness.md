---
title: The slice sampler with stepping out and shrinkage leaves π invariant
proves: [correctness]
status: full
---

**Setting.** Let $f \ge 0$ on $\mathbb{R}$ with $0 < \int f < \infty$ and $\pi = f/\int f$. Let $U = \{(x, y) : 0 < y < f(x)\}$ and let $\mu$ be the uniform distribution on $U$, with density $\mathbf{1}_U(x, y)/\int f$. For $y > 0$, the slice is $S_y = \{x : f(x) > y\}$. We assume that the shrinkage loop ends with probability 1; this holds, for example, when $S_y$ contains an open interval around each of its points, as it does for a lower semicontinuous $f$.

**Step 1: the marginal and the conditionals of $\mu$.** The $x$-marginal of $\mu$ has density $\int_0^{f(x)}dy/\int f = \pi(x)$. Given $x$, $y$ is uniform on $(0, f(x))$. Given $y$, $x$ is uniform on $S_y$, which has finite length $|S_y| \le \int f/y$.

**Step 2: the vertical move.** Line L3 draws $y$ from the exact conditional of $\mu$ given $x$, so it is a Gibbs update and leaves $\mu$ invariant (see the proof on the [Gibbs sampling](/gibbs-sampling/) page).

**Step 3: reduction for the horizontal move.** Lines L4 to L9 keep $y$ fixed and map $x_0 \in S_y$ to $x_1 \in S_y$ with a transition density $T_y(x_0, x_1)$. If $T_y(x_0, x_1) = T_y(x_1, x_0)$ for all $x_0, x_1 \in S_y$, then for every measurable $A \subseteq S_y$, $\int_{S_y}\int_A T_y(x_0, x_1)\,dx_1\,dx_0 = \int_A\int_{S_y}T_y(x_1, x_0)\,dx_0\,dx_1 = |A|$, so the uniform distribution on $S_y$ is invariant. Then the horizontal move preserves the conditional of $x$ given $y$ and does not change $y$, so it leaves $\mu$ invariant. Steps 4 to 6 prove the symmetry.

**Step 4: the grid.** Line L4 sets $L = x_0 - wU$. All later endpoints of the stepping-out phase are $L + jw$ for integers $j$, so they lie on the grid $G_\theta = \theta + w\mathbb{Z}$ with $\theta = (x_0 - wU) \bmod w$. Since $U$ is uniform on $[0, 1)$, $\theta$ is uniform on $[0, w)$, whatever $x_0$ is. Fix $\theta$. Number the cells $C_j = [\theta + jw, \theta + (j + 1)w)$, and let $g_j = \theta + jw$ be the left end of $C_j$. The start cell is the cell $c$ that contains $x_0$.

**Step 5: stepping out is symmetric.** For fixed $\theta$, the procedure from start cell $c$ ends with the interval $[g_a, g_{b+1})$, for some $a \le c \le b$. Line L5 moves the left end from $g_c$ to $g_{c-1}$, and so on, and it stops at $g_a$ exactly when $g_{a+1}, \ldots, g_c \in S_y$ and either $g_a \notin S_y$ or the budget is used, $J = c - a$. Line L6 stops at $g_{b+1}$ exactly when $g_{c+1}, \ldots, g_b \in S_y$ and either $g_{b+1} \notin S_y$ or $K = b - c$. So the outcome $[g_a, g_{b+1})$ needs the condition

$$(\ast)\qquad g_{a+1}, \ldots, g_b \in S_y,$$

which does not depend on $c$. Given $(\ast)$, count the values $J \in \{0, \ldots, m - 1\}$, with $K = m - 1 - J$, that give this outcome:

- if $g_a \notin S_y$ and $g_{b+1} \notin S_y$: we need $J \ge c - a$ and $K \ge b - c$, that is, $c - a \le J \le m - 1 - (b - c)$, which has $\max(0, m - (b - a))$ values;
- if $g_a \notin S_y$ and $g_{b+1} \in S_y$: we need $K = b - c$ and $J \ge c - a$, that is, $J = m - 1 - (b - c) \ge c - a$, which has one value if $b - a \le m - 1$ and none otherwise;
- if $g_a \in S_y$ and $g_{b+1} \notin S_y$: by the mirror argument, one value if $b - a \le m - 1$ and none otherwise;
- if $g_a \in S_y$ and $g_{b+1} \in S_y$: we need $J = c - a$ and $K = b - c$, so $J + K = b - a = m - 1$, which has one value if $b - a = m - 1$ and none otherwise.

In each case the count depends on $a$, $b$ and the slice, but not on $c$. Since $J = \lfloor mV\rfloor$ is uniform on $\{0, \ldots, m - 1\}$, for each $\theta$ the probability of the interval $I = [g_a, g_{b+1})$ is the same from every start in $I \cap S_y$. Call it $p_\theta(I)$.

**Step 6: shrinkage is symmetric.** Fix $I = (L, R)$ and $x_0, x_1 \in I \cap S_y$. Consider a run of lines L7 to L9 from $x_0$ that draws rejected points $r_1, \ldots, r_k \notin S_y$ and then accepts $x_1$. Let $I_0 = I$ and let $I_i$ be the interval after the cut at $r_i$. The density of this run is $\prod_{i=0}^{k}1/|I_i|$, since each draw is uniform on the current interval. The run is possible only if $x_1 \in I_k$. Since each cut keeps the side of $x_0$, $x_1 \in I_k$ holds exactly when no $r_i$ lies between $x_0$ and $x_1$. In that case, $r_i < x_0$ if and only if $r_i < x_1$, so the run from $x_1$ that draws the same points $r_1, \ldots, r_k$ and then $x_0$ cuts at the same places on the same sides and has the same intervals $I_0, \ldots, I_k$. Its points $r_i$ are rejected for the same reason, $r_i \notin S_y$, and its last point $x_0$ is in $S_y$, so it is accepted. So the two runs have the same density. Integrate over $k$ and over the rejected points: the shrinkage density $s_I(x_0, x_1)$ equals $s_I(x_1, x_0)$.

**Step 7: conclusion.** For $x_0, x_1 \in S_y$,

$$T_y(x_0, x_1) = \frac1w\int_0^w\sum_{I}p_\theta(I)\,\mathbf{1}\{x_0, x_1 \in I\}\,s_I(x_0, x_1)\,d\theta,$$

where the sum is over the intervals $I = [g_a, g_{b+1})$ of the grid $G_\theta$, and an interval that does not contain $x_1$ contributes nothing, since shrinkage stays inside $I$. By Step 5, $p_\theta(I)$ is the same from $x_0$ and from $x_1$ when both are in $I \cap S_y$, and by Step 6, $s_I$ is symmetric. So $T_y(x_0, x_1) = T_y(x_1, x_0)$. By Step 3 the horizontal move leaves $\mu$ invariant. Now let $X_{t-1} \sim \pi$. After line L3, the pair $(X_{t-1}, y)$ has law $\mu$ by Step 1. After lines L4 to L9, the pair $(X_t, y)$ still has law $\mu$, so $X_t \sim \pi$ by Step 1. So $\pi$ is a stationary distribution of the chain. $\blacksquare$

**Remarks.** For $x \in \mathbb{R}^d$ updated one coordinate at a time, apply the argument to the conditional density of one coordinate, as in the systematic scan of Gibbs sampling. The proof shows why line L4 splits the budget $m$ at random: with a fixed split, the count in Step 5 would depend on $c$. It also shows why line L9 must keep the side of the current point: a cut that kept the other side would break Step 6.
