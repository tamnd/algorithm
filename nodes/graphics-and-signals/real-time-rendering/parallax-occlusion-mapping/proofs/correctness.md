---
title: The march with a secant step lands within one step of the first hit
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page. Arithmetic is exact (real-ram). The depth map $m$ is continuous with values in $[0, 1]$. Line L1 gives the offset $\Delta$ per unit of depth, and the ray at depth $r \in [0, 1]$ is at the texture coordinate $p(r) = uv_0 + r \Delta$. Let
$$f(r) = r - m(p(r)).$$
The ray is at or below the surface at depth $r$ exactly when $f(r) \ge 0$. The function $f$ is continuous, $f(0) = -m(uv_0) \le 0$ and $f(1) = 1 - m(p(1)) \ge 0$. Let $Z = \{r \in [0, 1] : f(r) \ge 0\}$. It is closed and contains 1, so it has a least element $r^* = \min Z$, the depth of the first hit of the view ray with the height field.

**Lemma 1 (the march stops, with a bracket).** If line L3 does not return, the loop of lines L4 to L9 returns at the least $i$ with $f(i/k) \ge 0$, and then $f((i-1)/k) < 0 \le f(i/k)$. Such an $i \le k$ exists.

*Proof.* $f(k/k) = f(1) \ge 0$, so some $i \le k$ passes the test of line L6, and the loop returns at the least one. Line L9 keeps $(r_{prev}, f_{prev})$ equal to the previous sample, so at the return $r_{prev} = (i-1)/k$ and $f_{prev} = f((i-1)/k)$. For $i = 1$ this is the value of line L2, which is negative because line L3 did not return. For $i > 1$ it is negative because sample $i - 1$ failed the test. $\square$

**Lemma 2 (the secant step stays in the bracket).** At line L7, $t \in (0, 1]$, so $\hat r$ of line L8 lies in $(r_{prev}, r]$. Also $\hat r$ is the root of the line through $(r_{prev}, f_{prev})$ and $(r, f)$.

*Proof.* $f_{prev} < 0 \le f$, so $f_{prev} - f < 0$ and $t = f_{prev}/(f_{prev} - f) = (-f_{prev})/((-f_{prev}) + f)$, a positive number at most 1. The line through the two points is $\ell(s) = f_{prev} + (s - r_{prev}) (f - f_{prev})/(r - r_{prev})$, and $\ell(\hat r) = f_{prev} + t (f - f_{prev}) = f_{prev} - f_{prev} = 0$. $\square$

**Theorem 1 (one step of error).** Suppose $f(r) \ge 0$ for all $r \in [r^*, \min(1, r^* + 1/k)]$: once the ray enters the height field, it stays inside for at least one step. Then the returned depth satisfies $|\hat r - r^*| \le 1/k$.

*Proof.* If $r^* = 0$, then $f(0) \ge 0$ and line L3 returns $0 = r^*$. Otherwise let $i = \lceil r^* k \rceil \ge 1$, so $(i-1)/k < r^* \le i/k \le r^* + 1/k$, and $i/k \le 1$. By the assumption $f(i/k) \ge 0$. Every earlier sample $j/k$ with $j < i$ has $j/k < r^*$, so $j/k \notin Z$ and $f(j/k) < 0$. So by Lemma 1 the loop returns at this $i$, and by Lemma 2, $\hat r \in ((i-1)/k, i/k]$. Both $\hat r$ and $r^*$ lie in this interval of length $1/k$. $\square$

**Theorem 2 (exact for a planar map).** If $m(p(r)) = a + b r$ along the ray for constants $a$ and $b$, the result is exact: $\hat r = r^*$.

*Proof.* Then $f(r) = (1 - b) r - a$ is affine. If $a = 0$, line L3 returns $0 = r^*$. Otherwise $f(0) = -a < 0$ and $f(1) \ge 0$ give $1 - b > 0$, so $f$ is increasing with the single root $r^* = a/(1 - b)$. The line of Lemma 2 through two points of an affine function is the function itself, so its root $\hat r$ is $r^*$. $\square$

**Theorem 3 (without the assumption, the result is still a hit).** In every case $\hat r$ lies within $1/k$ of a root of $f$, that is, of a point where the ray meets the height field.

*Proof.* By Lemma 1, $f$ changes sign on $[(i-1)/k, i/k]$, so by the intermediate value theorem it has a root there, and by Lemma 2 $\hat r$ lies in the same interval. $\square$

The root of Theorem 3 need not be the first one. If the ray passes through a feature thinner than one step, the samples miss it, and the result is a later hit. The code test `test_thin_wall_is_missed_by_a_coarse_march` shows this with a wall one texel wide.

**Cost.** Lines L1 to L3 take $O(1)$ time and one sample. The loop runs at most $k$ times, with one sample of $m$ each. Lines L7 and L8 run once. So one pixel takes $O(k)$ time and at most $k + 1$ samples, and $O(1)$ space.
