---
title: The signed crossing count is the winding number
proves: [correctness]
status: full
---

**Setup.** $P$ is a closed polygon with vertices $v_0, \ldots, v_{n-1}$ (indices mod $n$) and edges $e_i = v_i v_{i+1}$. Repeated vertices, collinear vertices, horizontal edges and self-intersections are allowed. For a point $q$ that is not on $P$, the vectors $v_i - q$ and $v_{i+1} - q$ are not zero. Let $\varphi_i(q)$ be the signed angle from $v_i - q$ to $v_{i+1} - q$, taken in $(-\pi, \pi)$; it is 0 when $v_i = v_{i+1}$. It cannot be $\pm\pi$, because then $q$ would lie between $v_i$ and $v_{i+1}$ on the edge. The *winding number* is

$$\operatorname{wind}(P, q) = \frac{1}{2\pi} \sum_{i=0}^{n-1} \varphi_i(q).$$

**Claim.** WINDING-NUMBER$(P, q)$ returns BOUNDARY exactly when $q$ lies on $P$, and otherwise it returns $\operatorname{wind}(P, q)$, which is an integer.

## Step 1: the boundary test

Line L4 tests $q$ against each closed edge: $\mathrm{orient}(a, b, q) = 0$ puts $q$ on the line $ab$, and the two coordinate ranges put it in the segment. If $q$ is on some edge, the loop reaches that edge, because no earlier line returns, and line L4 returns. If $q$ is on no edge, line L4 never returns. So from now on $q$ is not on $P$.

## Step 2: one edge seen from a point

**Lemma 1.** Let $p$ be a point not on the segment $ab$, and let $\theta(t)$ be a continuous angle of $a + t(b - a) - p$ for $t \in [0, 1]$. Then $\theta(1) - \theta(0)$ is the signed angle $\varphi$ from $a - p$ to $b - p$, and the values $\theta(t)$ lie in an interval of length less than $\pi$.

*Proof.* If $p$ is not on the line $ab$, the segment lies in the open half-plane bounded by the line through $p$ parallel to $ab$. If $p$ is on the line $ab$ but not on the segment, the segment lies in the open half-plane bounded by the line through $p$ perpendicular to $ab$. In both cases every direction $a + t(b - a) - p$ lies in an open half-circle of directions, so a continuous angle stays in an open interval of length $\pi$. The difference $\theta(1) - \theta(0)$ is then an angle from $a - p$ to $b - p$ of absolute value less than $\pi$, and that is $\varphi$. $\square$

## Step 3: crossings of a ray in general position

**Lemma 2.** Let $p$ be a point not on $P$, and let $R$ be the horizontal ray from $p$ to the right, without $p$ itself. Assume that no vertex of $P$ lies on $R$. Let $U$ be the number of edges that cross $R$ from below to above and $D$ the number that cross it from above to below. Then $\operatorname{wind}(P, p) = U - D$.

*Proof.* Measure angles around $p$ so that $R$ has angle 0, and for a point $x \notin R \cup \{p\}$ let $\alpha(x) \in (0, 2\pi)$ be its angle. Write $\alpha_i = \alpha(v_i)$; it is defined since no vertex is on $R$.

An edge meets $R$ in at most one point. If it met $R$ in two points it would lie on the line of $R$, and then, as it does not contain $p$, it would have an endpoint on $R$. Fix an edge $e_i$ and the continuous angle $\theta(t)$ of Lemma 1 with $\theta(0) = \alpha_i$.

- If $e_i$ does not meet $R$, then $\theta(t)$ is never a multiple of $2\pi$. It starts in $(0, 2\pi)$, so it stays there, and $\theta(1) = \alpha_{i+1}$. So $\varphi_i = \alpha_{i+1} - \alpha_i$.
- If $e_i$ crosses $R$ from below to above, then $\theta$ increases through $2\pi$ at the crossing. By Lemma 1 it passes no other multiple of $2\pi$. So $\theta(1) = \alpha_{i+1} + 2\pi$ and $\varphi_i = \alpha_{i+1} - \alpha_i + 2\pi$.
- If $e_i$ crosses $R$ from above to below, then in the same way $\varphi_i = \alpha_{i+1} - \alpha_i - 2\pi$.

Summing over the cycle, the terms $\alpha_{i+1} - \alpha_i$ telescope to 0, and $\sum_i \varphi_i = 2\pi (U - D)$. $\square$

## Step 4: the half-open rule

Let $\delta > 0$ be smaller than the distance from $q$ to $P$ and smaller than every nonzero value $|y(v_i) - y(q)|$. Choose $\varepsilon$ with $0 < \varepsilon < \delta$, also so small that $\mathrm{orient}(a, b, q')$ has the sign of $\mathrm{orient}(a, b, q)$ for every edge $ab$ with $\mathrm{orient}(a, b, q) \ne 0$, where $q' = (x(q), y(q) + \varepsilon)$. This is possible since there are finitely many edges and orient is continuous in its third argument. No vertex has its $y$-coordinate in $(y(q), y(q')]$, so no vertex lies on the ray $R'$ from $q'$.

*The edge conditions.* An edge with $y(a) \le y(q) < y(b)$, as in line L5, has $y(b) > y(q)$ and so $y(b) \ge y(q) + \delta > y(q')$. So it crosses the line $y = y(q')$ upward. Conversely, an edge that crosses this line upward has $y(a) < y(q') < y(b)$, and since no vertex has a height in $(y(q), y(q')]$, it has $y(a) \le y(q) < y(b)$. So the condition of line L5 holds exactly for the edges that cross the line $y = y(q')$ upward. By symmetry, the condition of line L6 holds exactly for the edges that cross it downward. A horizontal edge meets neither condition, and it does not cross the line.

*The side test.* An upward edge crosses the line to the right of $q'$ exactly when $q'$ lies to its left, that is, when $\mathrm{orient}(a, b, q') > 0$. A downward edge crosses it to the right of $q'$ exactly when $\mathrm{orient}(a, b, q') < 0$. For such an edge, $\mathrm{orient}(a, b, q) \ne 0$: otherwise $q$ lies on the line $ab$, which meets the line $y = y(q)$ in exactly one point because the edge is not horizontal, and that point lies on the segment because $y(q)$ is between $y(a)$ and $y(b)$; so $q$ would be on $P$. Hence $\mathrm{orient}(a, b, q)$ and $\mathrm{orient}(a, b, q')$ have the same sign, and lines L5 and L6 test the right side.

So after the loop, $w = U' - D'$ for the ray $R'$ from $q'$, and by Lemma 2, $w = \operatorname{wind}(P, q')$.

## Step 5: moving the point back

Each $\varphi_i(x)$ is a continuous function of $x$ off the closed edge $e_i$, so $\operatorname{wind}(P, x)$ is continuous off $P$. Let $x_t = (x(q), y(q) + t)$ for $0 \le t \le \varepsilon$. The segment from $q$ to $q'$ has length $\varepsilon < \delta$, so it does not meet $P$, and $\operatorname{wind}(P, x_t)$ is continuous in $t$. For $0 < t \le \varepsilon$, no vertex has a height in $(y(q), y(q) + t]$, so the ray from $x_t$ avoids the vertices, and by Lemma 2 the value $\operatorname{wind}(P, x_t)$ is an integer. A continuous integer-valued function on the interval $(0, \varepsilon]$ is constant, so it equals $\operatorname{wind}(P, q') = w$ there. Letting $t \to 0$ gives $\operatorname{wind}(P, q) = w$, and line L7 returns the winding number. $\blacksquare$

**Termination and cost.** The loop runs at most $n$ times, and each pass does a constant number of exact operations.
