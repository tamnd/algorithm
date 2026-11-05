---
title: Golden-section search keeps the minimum in its interval and reuses one point per step
proves: [correctness]
status: full
---

We use the pseudocode of the page, with $\rho = (\sqrt5 - 1)/2$. The number $\rho$ is the positive root of $\rho^2 + \rho - 1 = 0$, so $\rho^2 = 1 - \rho$ and $1/2 < \rho < 1$. Let $f$ be strictly unimodal for a minimum on $[a_0, b_0]$ with mode $m$: strictly decreasing on the points $\le m$ and strictly increasing on the points $\ge m$. The comparison lemma for a minimum reads, for $x_1 < x_2$: $f(x_1) < f(x_2)$ implies $m < x_2$; $f(x_1) > f(x_2)$ implies $m > x_1$; $f(x_1) = f(x_2)$ implies $x_1 < m < x_2$. Its proof is the one for a maximum with $f$ replaced by $-f$.

**Claim.** GOLDEN-MIN$(f, a_0, b_0, steps)$ evaluates $f$ exactly $steps + 2$ times. Before line L8, $m \in [a, b]$ and, in exact arithmetic, $b - a = \rho^{steps}(b_0 - a_0)$. The returned point is within $\tfrac12 \rho^{steps + 1}(b_0 - a_0)$ of $m$.

*Invariant.* Before each test of line L5, with $L = b - a$:

1. $m \in [a, b]$;
2. $c = a + \rho^2 L$ and $d = a + \rho L$, so $a < c < d < b$;
3. $fc = f(c)$ and $fd = f(d)$.

*Initialization.* Line L2 sets $c = b - \rho L = a + (1 - \rho)L = a + \rho^2 L$ and $d = a + \rho L$. Since $\rho^2 < \rho < 1$, the order $a < c < d < b$ holds. Line L3 sets the values. Item 1 holds by the assumption on $f$.

*Maintenance, case $fc < fd$ (line L6).* By the lemma, $m < d$, so $m \in [a, d]$, the new interval. Its left end is $a' = a$ and its length is $L' = d - a = \rho L$. The new $d$ is the old $c = a + \rho^2 L = a' + \rho L'$, the correct inner point, and its value is the old $fc$. The new $c$ is computed as $b' - \rho L' = a' + (1 - \rho) L' = a' + \rho^2 L'$, and $f$ is evaluated there once.

*Maintenance, case $fc \ge fd$ (line L7).* If $fc > fd$, the lemma gives $m > c$; if $fc = fd$, it gives $c < m < d$. In both cases $m \in [c, b]$, the new interval. Its left end is $a' = c = a + \rho^2 L$ and its length is $L' = b - c = (1 - \rho^2) L = \rho L$. From $\rho^2 + \rho = 1$ we get $\rho(1 + \rho) = 1$, so $a' + \rho^2 L' = a + \rho^2 L (1 + \rho) = a + \rho L$, which is the old $d$. So the old $d$ is the correct new $c$, with value $fd$. The new $d$ is computed as $a' + \rho L'$, and $f$ is evaluated there once.

In both cases the invariant holds again with $L' = \rho L$.

*Termination and result.* The loop runs $steps$ times, with one evaluation each, after the two of line L3: $steps + 2$ evaluations. Before line L8, $b - a = \rho^{steps}(b_0 - a_0)$ and $m \in [a, b]$. Line L8 applies the same case analysis once more without a new evaluation: $m \in [a, d]$ or $m \in [c, b]$, both of length $\rho(b - a)$. The midpoint of an interval of length $\rho^{steps + 1}(b_0 - a_0)$ that holds $m$ is within half that length of $m$. $\square$

**Remark on floating point.** Items 2 and 3 hold only up to rounding, because the reused point keeps its old computed value. The proof of item 1 uses only that $fc$ and $fd$ are the values at two points $c < d$ of $[a, b]$ and that the new interval is $[a, d]$ or $[c, b]$. So the minimum stays in the interval in floating point as long as the computed points keep the order $a \le c < d \le b$, which holds until the interval holds only a few doubles. Rounding affects the length bound, not the bracket.

**Why the ratio must be $\rho$.** Suppose a method uses inner points at the fractions $1 - t$ and $t$ of each interval, with $1/2 < t < 1$, and wants the kept inner point to be an inner point of the next interval. After keeping $[a, d]$, the new length is $tL$ and the old $c$ sits at $(1 - t)L$ from $a$. For it to be at the fraction $t$ of the new interval we need $(1 - t)L = t \cdot tL$, that is $t^2 + t - 1 = 0$, so $t = \rho$.
