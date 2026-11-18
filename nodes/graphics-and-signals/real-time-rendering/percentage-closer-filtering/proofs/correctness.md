---
title: Percentage-closer filtering returns the weighted fraction of lit taps, and the 2 x 2 bilinear form is the exact box integral of the binary test
proves: [correctness]
status: full
---

We use the notation of the page. The map $S$ has $W$ columns and $H$ rows, and texel $(i, j)$ has its center at $(i + \tfrac12, j + \tfrac12)$. For a receiver depth $z$ and a bias $b$, the binary test of texel $(i, j)$ is $t(i, j) = 1$ if $(i, j)$ is outside the map or $z - b \le S[i, j]$, and $t(i, j) = 0$ otherwise. So $t = 1$ means lit. A kernel $K$ is a finite map from integer offsets $(u, v)$ to weights $K(u, v) \ge 0$, with at least one positive weight. The arithmetic is exact.

## The weighted form

**Theorem 1.** For a lookup at $(x, y)$ with $(i, j) = (\lfloor x \rfloor, \lfloor y \rfloor)$, PCF (lines L1 to L7) returns

$$P = \frac{\sum_{(u, v)} K(u, v)\, t(i + u, j + v)}{\sum_{(u, v)} K(u, v)},$$

and $0 \le P \le 1$. $P$ does not increase when $z$ increases, and does not decrease when $b$ increases. For the kernel with the single tap $K(0, 0) = 1$, $P$ is the binary test of [shadow mapping](/shadow-mapping/) at the texel that holds $(x, y)$, with lit in place of shadowed.

*Proof.* Lines L3 to L6 visit each offset with a positive weight once; L5 adds $K(u, v)\, t(i + u, j + v)$ to $a$ and L6 adds $K(u, v)$ to $w$. Offsets with weight 0 add 0 to both sums, so skipping them does not change $a$ or $w$. L7 returns $a / w$, and $w > 0$. Each $t$ is 0 or 1 and each weight is nonnegative, so $0 \le a \le w$, which gives $0 \le P \le 1$. The test $z - b \le S[i + u, j + v]$ can only change from true to false when $z$ increases, and only from false to true when $b$ increases. So each term of $a$ is monotone in the stated direction, and so is $P$, because $w$ does not depend on $z$ or $b$. With one tap, $P = t(i, j)$. $\square$

For the box kernel of radius $r$ (weight 1 on $[-r, r]^2$), $P$ is the number of lit taps divided by $(2r + 1)^2$. The number of lit taps in a rectangle of texels is also the four-term inclusion-exclusion over the table of prefix counts $C[i, j] = \sum_{i' < i, j' < j} t(i', j')$. This is the second method that the tests use.

## The bilinear form

**Theorem 2.** Let $\bar t(u, v) = t(\lfloor u \rfloor, \lfloor v \rfloor)$ be the binary test of the texel that holds the point $(u, v)$. Then PCF-BILINEAR (lines L8 to L10) returns

$$\int_{y - 1/2}^{y + 1/2} \int_{x - 1/2}^{x + 1/2} \bar t(u, v)\, du\, dv,$$

the mean of the nearest-texel binary test over the unit square centered at $(x, y)$.

*Proof.* Let $i = \lfloor x - \tfrac12 \rfloor$ and $f = x - \tfrac12 - i$, so $0 \le f < 1$ and the interval $[x - \tfrac12, x + \tfrac12]$ is $[i + f, i + f + 1]$. It meets the column $[i, i + 1)$ in a length $1 - f$ and the column $[i + 1, i + 2)$ in a length $f$, and no other column in a set of positive length. In the same way, with $j = \lfloor y - \tfrac12 \rfloor$ and $g = y - \tfrac12 - j$, the rows $j$ and $j + 1$ get the lengths $1 - g$ and $g$. The function $\bar t$ is constant on each texel, so the integral is the sum over the four texels of the overlap area times the test: $(1 - f)(1 - g)\, t(i, j) + f (1 - g)\, t(i + 1, j) + (1 - f) g\, t(i, j + 1) + f g\, t(i + 1, j + 1)$. This is line L10. $\square$

At the texel center $(i' + \tfrac12, j' + \tfrac12)$ we get $i = i'$, $j = j'$ and $f = g = 0$, so the result is $t(i', j')$, the binary test. Between centers the result is continuous in $(x, y)$, because the weights are continuous in $f$ and $g$ and the weights of a texel go to 0 when the square leaves it.

## Filtering the depths first is a different function

**Proposition 3.** The function that averages the depths in the box and compares once returns only 0 or 1, and it can differ from PCF by more than $\tfrac12$.

*Proof.* It returns the value of one comparison, so it is 0 or 1. In the example of the page (floor depth $0.8$, box top $0.3$, $z = 0.8$, $b = 0$, a $3 \times 3$ box at texel $(6, 3)$), three taps hold $0.3$ and six hold $0.8$. The mean depth is $(3 \cdot 0.3 + 6 \cdot 0.8)/9 = 0.6333\ldots < 0.8$, so the single test returns 0. PCF counts the six lit taps and returns $2/3$, so the two differ by $2/3 > \tfrac12$. $\square$
