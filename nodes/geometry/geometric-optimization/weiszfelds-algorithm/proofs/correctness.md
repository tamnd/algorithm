---
title: Weiszfeld's algorithm with the Vardi-Zhang step lowers the cost at each step and converges to the geometric median
proves: [correctness]
status: full
---

**Setting.** The data points $a_1, \ldots, a_n \in \mathbb{R}^d$ are distinct, with weights $w_i > 0$; copies of one point are merged first, and their weights added, which does not change $f$. Let $f(x) = \sum_i w_i |x - a_i|$, $W = \sum_i w_i$, $w_{\min} = \min_i w_i$, $A = \{a_1, \ldots, a_n\}$, $H$ the convex hull of $A$ and $D$ the diameter of $A$. We assume $n \ge 2$, so $D > 0$; for $n = 1$ the start passes the test of line L8 after one step. For a point $y$ let $\delta_i = |y - a_i|$, and over the indices $i$ with $\delta_i > 0$ let

$$S(y) = \sum \frac{w_i}{\delta_i}, \qquad \tilde T(y) = \frac{1}{S(y)} \sum \frac{w_i}{\delta_i}\, a_i, \qquad R(y) = \sum w_i\, \frac{a_i - y}{\delta_i}.$$

Let $\eta(y) = w_k$ if $y = a_k$ and $\eta(y) = 0$ if $y \notin A$, and $r = |R(y)|$. The map of the algorithm is $T(y) = y$ if $r \le \eta(y)$, and otherwise

$$T(y) = \Big(1 - \frac{\eta(y)}{r}\Big) \tilde T(y) + \frac{\eta(y)}{r}\, y .$$

Lines L3 to L7 compute $S$, $S \tilde T$, $R$ and $\eta$; line L8 returns $y$ when $T(y) = y$; and line L9 computes $T(y)$. So the iterates of the algorithm are $y_{j+1} = T(y_j)$. A direct expansion gives the identity

$$\tilde T(y) - y = \frac{R(y)}{S(y)}. \tag{1}$$

**Lemma 1 (optimality).** A point $y \notin A$ minimizes $f$ iff $R(y) = 0$. A data point $a_k$ minimizes $f$ iff $|R(a_k)| \le w_k$. In both cases this is the condition $r \le \eta(y)$, so $T(y) = y$ iff $y$ minimizes $f$.

*Proof.* $f$ is convex, as a sum of norms of affine maps, so $y$ is a minimizer iff the one-sided derivative $f'(y; v) = \lim_{t \downarrow 0} (f(y + tv) - f(y))/t$ is at least 0 for every unit vector $v$. A term with $\delta_i > 0$ is differentiable at $y$ with gradient $w_i (y - a_i)/\delta_i$. A term with $a_i = y$ contributes $w_i |v|$. Hence $f'(y; v) = \eta(y) - \langle R(y), v \rangle$, whose smallest value over unit vectors is $\eta(y) - r$ (at $v = R/r$ if $r > 0$, and any $v$ if $r = 0$). So $y$ is a minimizer iff $r \le \eta(y)$. For $y \notin A$, $\eta = 0$ and this reads $R(y) = 0$. $\square$

**Lemma 2 (the hull).** For every $y$, $T(y)$ lies in the convex hull of $A \cup \{y\}$. If $y \notin A$ or $y \in H$, then $T(y) \in H$.

*Proof.* $\tilde T(y)$ is an average of data points with positive weights, so $\tilde T(y) \in H$. $T(y)$ is $y$ or a convex combination of $\tilde T(y)$ and $y$; if $\eta(y) = 0$ it is $\tilde T(y)$ or $y$ with $R(y) = 0$, and in that case $y = \tilde T(y)$ by (1). $\square$

So from $y_1$ on, every iterate lies in $H$: if $y_0 \in A$ then $y_0 \in H$; otherwise $y_1 = T(y_0) \in H$ by Lemma 2.

**Lemma 3 (descent).** Let $y \in H$ with $T(y) \ne y$, and let $h = T(y) - y$. Then

$$f(T(y)) \le f(y) - \frac{w_{\min}}{2D}\, |h|^2 .$$

*Proof.* For $\delta > 0$ and any $z$, $(|z - a| - \delta)^2 \ge 0$ gives

$$|z - a| \le \frac{|z - a|^2}{2\delta} + \frac{\delta}{2}, \tag{2}$$

with equality when $|z - a| = \delta$. Let $I$ be the set of $i$ with $\delta_i > 0$, and

$$g(z) = \sum_{i \in I} w_i \Big( \frac{|z - a_i|^2}{2\delta_i} + \frac{\delta_i}{2} \Big).$$

By (2), $\sum_{i \in I} w_i |z - a_i| \le g(z)$ for all $z$, with equality at $z = y$. $g$ is a quadratic with Hessian $S(y)$ times the identity, its gradient at $y$ is $-R(y)$, so

$$g(y + u) = g(y) - \langle R(y), u \rangle + \tfrac{1}{2} S(y) |u|^2 . \tag{3}$$

*Case $y \notin A$.* Then $f = \sum_{i \in I} w_i |\cdot - a_i|$, and $h = R/S$ by (1), since $\eta = 0$. By (3), $f(y + h) \le g(y + h) = g(y) - |R|^2/S + |R|^2/(2S) = f(y) - \frac{1}{2} S |h|^2$.

*Case $y = a_k$, $r > w_k$.* Then $h = (1 - w_k/r)\, R/S$, so $h = t R/r$ with $t = (r - w_k)/S > 0$, and $f(y + h) = w_k t + \sum_{i \in I} w_i |y + h - a_i| \le w_k t + g(y + h)$. By (3), $g(y + h) = f(y) - r t + \frac{1}{2} S t^2$, since $g(y) = f(y)$. So $f(y + h) \le f(y) - (r - w_k) t + \frac{1}{2} S t^2 = f(y) - \frac{1}{2} S t^2 = f(y) - \frac{1}{2} S |h|^2$.

In both cases $y \in H$ gives $\delta_i \le D$ for all $i$, and $I$ is not empty, so $S(y) \ge w_{\min}/D$. $\square$

**Lemma 4 (repulsion).** Let $a_k$ fail the test, $|R(a_k)| > w_k$. There is $\rho > 0$ such that every $y$ with $0 < |y - a_k| < \rho$ satisfies $|T(y) - a_k| > |y - a_k|$.

*Proof.* Take $\rho$ smaller than the distance from $a_k$ to every other data point. For $0 < \delta_k = |y - a_k| < \rho$, $y \notin A$, so $T(y) = \tilde T(y)$, and the term $i = k$ of $\sum_i (w_i/\delta_i)(a_i - a_k)$ is zero. Hence

$$\frac{|T(y) - a_k|}{\delta_k} = \frac{|N(y)|}{w_k + \delta_k \sum_{i \ne k} w_i/\delta_i}, \qquad N(y) = \sum_{i \ne k} w_i\, \frac{a_i - a_k}{\delta_i}.$$

As $y \to a_k$, $\delta_i \to |a_k - a_i| > 0$ for $i \ne k$, so $N(y) \to R(a_k)$ and the sum in the denominator stays bounded while $\delta_k \to 0$. The ratio tends to $|R(a_k)|/w_k > 1$, so it exceeds 1 for all $y$ close enough to $a_k$; shrink $\rho$ to that range. $\square$

**Theorem.** Let $y_0$ be any point and $y_{j+1} = T(y_j)$.

1. $f(y_{j+1}) \le f(y_j)$, with equality only when $y_j$ is a minimizer, and then $y_{j+1} = y_j$.
2. $f(y_j) \to \min f$.
3. If the data points do not all lie on one line, the minimizer $x^*$ is unique and $y_j \to x^*$.

*Proof.* Part 1 is Lemma 1 and Lemma 3, applied from $j = 1$ on (all these iterates lie in $H$), and for $j = 0$ it follows from the same computation with $D$ replaced by $\max_i \delta_i$. If some $y_j$ is a minimizer, the sequence is constant from there and all parts hold. Assume from now on that no iterate is a minimizer.

*Steps go to zero.* By Lemma 3, for $j \ge 1$, $|y_{j+1} - y_j|^2 \le (2D/w_{\min})\,(f(y_j) - f(y_{j+1}))$. The sum over $j$ telescopes and $f \ge 0$, so $\sum_j |y_{j+1} - y_j|^2 < \infty$ and $|y_{j+1} - y_j| \to 0$.

*Limit points.* The iterates lie in the compact set $H$, so the set $L$ of limit points is not empty. A bounded sequence whose steps tend to 0 has a connected set of limit points: if $L$ were the union of two disjoint nonempty closed sets $L_1, L_2$ at distance $\gamma > 0$, the sequence would pass infinitely often from within $\gamma/3$ of $L_1$ to within $\gamma/3$ of $L_2$ with steps below $\gamma/3$, so infinitely many iterates would lie at distance at least $\gamma/3$ from both, and a limit point of those would lie in $L$ but in neither set. Let $y^* \in L$ with $y^* \notin A$. Near $y^*$, $T = \tilde T$ is continuous. If $y_{j_m} \to y^*$, then $y_{j_m + 1} = T(y_{j_m}) \to T(y^*)$, and $|y_{j_m + 1} - y_{j_m}| \to 0$ gives $T(y^*) = y^*$; by Lemma 1, $y^*$ is a minimizer. So $L \subseteq M \cup A$, where $M$ is the set of minimizers.

*Part 2.* The values $f(y_j)$ decrease, so they converge to some $f_\infty$, and $f(y^*) = f_\infty$ for every $y^* \in L$, by continuity of $f$. If $L$ meets $M$, then $f_\infty = \min f$. Otherwise $L \subseteq A$ is a finite connected set, so $L = \{a_k\}$ and $y_j \to a_k$. Suppose $a_k$ fails the test, and take $\rho$ from Lemma 4. For $j \ge J$, $|y_j - a_k| < \rho$. If $y_j = a_k$ for some $j \ge J$, then $y_{j+1} \ne a_k$, since $T(a_k) - a_k = h \ne 0$. Once some $y_j \ne a_k$ with $j \ge J$, Lemma 4 gives $|y_{j+1} - a_k| > |y_j - a_k| > 0$, and by induction the distances to $a_k$ increase from then on, which contradicts $y_j \to a_k$. So $a_k$ passes the test, $a_k \in M$ by Lemma 1, and $f_\infty = f(a_k) = \min f$.

*Part 3.* If the data points are not on one line, then every line misses some $a_i$. Along a line that misses $a_i$, the term $|x - a_i|$ is strictly convex, and the other terms are convex, so $f$ is strictly convex along every line, and its minimizer $x^*$ (which exists, since $f(x) \to \infty$ as $|x| \to \infty$) is unique. Then $L \subseteq \{x^*\} \cup A$ is finite and connected, so $L$ is one point and the sequence converges. Its limit has value $\min f$ by part 2, so it is $x^*$. $\blacksquare$

**Remarks.** The stopping rule of line L11 is not part of the theorem; the algorithm returns after $K$ steps at most, so it terminates. The theorem covers the plain Weiszfeld iteration whenever no iterate lands on a data point, since then $T = \tilde T$ along the whole sequence. Kuhn (1973) stated part 3 for the plain iteration under that condition. For the certificate on the main page: for $y \in H \setminus A$, convexity gives $f(x^*) \ge f(y) + \langle \nabla f(y), x^* - y \rangle \ge f(y) - |R(y)|\, D$, because $x^* \in H$ (by Lemma 2 and part 3, or because a point outside $H$ can be projected onto $H$, which shortens every distance to a data point).
