---
title: Max-min smoothing never lowers the worst quality, keeps the star valid, and stops only where no position is better
proves: [correctness, termination]
status: full
---

**Setting.** A free vertex at position $x$ has star triangles $\tau_i = (x, a_i, b_i)$, $i = 1, \dots, m$, whose outer edges $a_i b_i$ form a closed polygon, the link. Let $A_i(x) = \frac12\,\mathrm{orient}(x, a_i, b_i)$ be the signed area, $S_i(x) = |x - a_i|^2 + |x - b_i|^2 + |a_i - b_i|^2$ the sum of squared edge lengths, and

$$q_i(x) = \frac{4\sqrt3\,A_i(x)}{S_i(x)}, \qquad Q(x) = \min_i q_i(x),$$

the mean ratio of $\tau_i$ and the worst quality of the star. The kernel of the star is $K = \{x : A_i(x) > 0 \text{ for all } i\}$, an intersection of open half-planes, so it is open and convex. A position in $K$ gives a valid star: all triangles are counterclockwise and they tile the link polygon.

**Claim 1 (monotone and valid).** SMOOTH-VERTEX started at $x_0 \in K$ produces positions $x_0, x_1, \dots$ in $K$ with $Q(x_0) < Q(x_1) < \cdots$, and it stops after at most `max_iter` steps.

*Proof.* A step is taken only after the test of L8 succeeds: the new position passes the exact orientation test, so it is in $K$, and its worst quality, as computed, is larger than the current one. Otherwise the loop ends at L9. The loop has a fixed bound on its iterations. $\square$

The orientation test is exact, because each float coordinate converts to a Fraction without rounding. The quality comparison is done in floats, so "larger" means larger as computed. Validity is exact; the monotone quality is exact up to the rounding of the quality formula.

**Lemma 2 (convex superlevel sets).** For each $i$ and each $t \ge 0$, the set $\{x \in K : q_i(x) \ge t\}$ is convex. So $q_i$ and $Q$ are quasi-concave on $K$.

*Proof.* On $K$, $S_i > 0$, so $q_i(x) \ge t$ if and only if $\varphi_{i,t}(x) = 4\sqrt3\,A_i(x) - t\,S_i(x) \ge 0$. Here $A_i$ is affine and $S_i$ is a convex quadratic, so $\varphi_{i,t}$ is concave and its superlevel set is convex. The superlevel sets of $Q$ are intersections of those of the $q_i$. $\square$

Freitag and Plassmann state this convexity of the level sets for their quality measures; this is the version for the mean ratio.

**Theorem 3 (stationary means optimal).** Let $x \in K$, $q^* = Q(x)$, and let $I = \{i : q_i(x) = q^*\}$ be the active set. If $0$ lies in the convex hull of $\{\nabla q_i(x) : i \in I\}$, then $Q(y) \le Q(x)$ for every $y \in K$.

*Proof.* Suppose $y \in K$ has $Q(y) > q^*$. Take $i \in I$ and let $\varphi = \varphi_{i,q^*}$ from Lemma 2. Then $\varphi(x) = S_i(x)\,(q_i(x) - q^*) = 0$ and $\varphi(y) = S_i(y)\,(q_i(y) - q^*) > 0$. Since $\varphi$ is concave and differentiable,

$$\nabla\varphi(x) \cdot (y - x) \ge \varphi(y) - \varphi(x) > 0.$$

By the quotient rule, $\nabla q_i = \bigl(4\sqrt3\,\nabla A_i - q_i \nabla S_i\bigr)/S_i$, so at $x$, where $q_i(x) = q^*$, $\nabla\varphi(x) = S_i(x)\,\nabla q_i(x)$. Hence $\nabla q_i(x) \cdot (y - x) > 0$ for every $i \in I$. Every convex combination $g$ of these gradients then has $g \cdot (y - x) > 0$, so $g \ne 0$, which contradicts the assumption. $\square$

**Lemma 4 (the direction rises).** Let $d$ be the point of least norm in the convex hull $C$ of $\{\nabla q_i(x) : i \in I\}$, and suppose $d \ne 0$. Then $\nabla q_i(x) \cdot d \ge |d|^2 > 0$ for every $i \in I$. So for small $\alpha > 0$, $Q(x + \alpha d) > Q(x)$.

*Proof.* For $g \in C$ and $s \in [0, 1]$, the point $d + s(g - d)$ is in $C$, so $|d + s(g - d)|^2 \ge |d|^2$. The derivative at $s = 0$ is $2 d \cdot (g - d) \ge 0$, which gives $g \cdot d \ge |d|^2$. Each active $q_i$ then rises at rate at least $|d|^2$ along $d$. Each inactive $q_j$ is above $q^*$ by a positive margin and is continuous, and $K$ is open. So for small $\alpha$ all $q_i(x + \alpha d) > q^*$ and $x + \alpha d \in K$. $\square$

**Consequence.** If the line search of L8 fails at a point where $d \ne 0$, the failure comes from the bound on the number of halvings, not from the absence of a better point. If the method stops at L6, with $|d|^2$ below the tolerance, the point is stationary up to that tolerance, and by Theorem 3 an exactly stationary point is a global maximum of $Q$ over the kernel. The test of the page compares the result with a grid search over the kernel, the reference method, and they agree to within the grid resolution.

The active set of the code contains every $i$ with $q_i \le q^* + \delta$, a slightly larger set than $I$. This makes the direction more cautious near ties; it does not change Claim 1, which rests only on the tests of L8.

**What is not proved.** Nothing here bounds $Q$ from below: if the link polygon is bad, every position is bad. The kernel can be empty, in which case no position gives a valid star and the method cannot start; this is the task of [mesh untangling](/mesh-untangling/). Over a whole mesh, smoothing one vertex at a time raises the worst quality of each star but does not reach the best positions of all vertices together, and it does not change the connectivity.
