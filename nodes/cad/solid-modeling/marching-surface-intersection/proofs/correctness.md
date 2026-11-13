---
title: Marching with a short step traces the whole branch of its start point and nothing else
proves: [correctness]
status: full
---

Let $f, g : \mathbb{R}^3 \to \mathbb{R}$ be $C^2$, let $F = (f, g)$, and let $J(x)$ be the $2 \times 3$ matrix with rows $\nabla f(x)^\top$ and $\nabla g(x)^\top$. Write $T(x)$ for the unit vector of $\nabla f(x) \times \nabla g(x)$. Let $C$ be a connected component of $\{F = 0\}$ that is compact and *regular*: $\nabla f \times \nabla g \ne 0$ on $C$. Then $C$ is a closed $C^2$ curve, by the implicit function theorem, and $T$ is a unit tangent field along it. Let $L$ be its length.

The proof uses exact arithmetic: CORRECT returns the limit of its Newton iteration. The tolerance $\tau$ of the implementation adds an error of order $\tau$ to every point and changes no step of the argument when $\tau$ is small compared with the step.

**Lemma 1 (the tangent).** At each $p \in C$, the tangent line of $C$ is spanned by $T(p)$.

*Proof.* $f$ and $g$ are constant on $C$, so their derivatives along $C$ vanish: the tangent vector is perpendicular to $\nabla f(p)$ and to $\nabla g(p)$. These are independent, so the vectors perpendicular to both form the line spanned by their cross product. $\square$

**Lemma 2 (a tube).** There are numbers $\rho > 0$, $K \ge 1$ and $\beta > 0$ such that on the closed tube $U = \{x : \operatorname{dist}(x, C) \le \rho\}$:

1. $U$ meets $\{F = 0\}$ only in $C$;
2. the smallest singular value of $J(x)$ is at least $\beta$, and $\nabla f \times \nabla g \ne 0$;
3. for each $x \in U$ with $\operatorname{dist}(x, C) \le \rho / (2K)$, the Newton iteration $x \leftarrow x - J^\top (J J^\top)^{-1} F(x)$ stays in $U$ and converges to a point $x^* \in C$ with $|x^* - x| \le K |F(x)|$.

*Proof.* (1) By the implicit function theorem, each point of $C$ has a neighborhood in which $\{F = 0\}$ is a single arc of $C$. Finitely many of these neighborhoods cover the compact $C$, and their union contains a tube around $C$; take $\rho$ smaller than its radius. (2) holds on $C$ and is an open condition, so it holds on a tube by compactness. (3) is the local convergence theorem of the Newton method with the pseudoinverse $J^\top (J J^\top)^{-1}$ for underdetermined systems, a form of the [Kantorovich theorem](/kantorovich-theorem/): when $J$ has full row rank with smallest singular value at least $\beta$ and $J$ is Lipschitz on a ball, the iteration from a point with small enough $|F|$ converges quadratically to a zero within a constant times $|F(x)|$ of the start. The constants are uniform on $U$ by compactness, and by (1) the zero lies in $C$. $\square$

**Lemma 3 (one step).** There is $h_1 > 0$ such that for every $p \in C$ and $0 < \delta \le h_1$, the point $q$ = CORRECT$(p + \delta T(p))$ lies on $C$ and satisfies $|q - p| = \delta + O(\delta^2)$, and the arc of $C$ from $p$ to $q$ in the direction of $T(p)$ has length $\delta + O(\delta^2)$. The constants are uniform in $p$.

*Proof.* Parametrize $C$ by arc length near $p$ as $\gamma(s)$ with $\gamma(0) = p$ and $\gamma'(0) = T(p)$ (Lemma 1). Taylor's theorem gives $|p + \delta T(p) - \gamma(\delta)| \le \kappa_{\max} \delta^2 / 2$, where $\kappa_{\max}$ bounds the curvature of $C$. So $\operatorname{dist}(p + \delta T, C) = O(\delta^2)$ and $|F(p + \delta T)| = O(\delta^2)$, since $F$ is Lipschitz. For $\delta$ small, Lemma 2 (3) applies, and $q \in C$ with $|q - (p + \delta T)| \le K \cdot O(\delta^2)$. Hence $|q - \gamma(\delta)| = O(\delta^2)$. Near $\gamma(\delta)$, $C$ is a single arc, by Lemma 2 (1), so $q = \gamma(\delta + O(\delta^2))$, which gives both claims. $\square$

**Lemma 4 (no refused step).** Let $\alpha > 0$ be the turning angle of line L7. For $\delta$ small enough, uniformly on $C$, CORRECT succeeds and the angle between $T(q)$ and $T(p)$ is $O(\delta) < \alpha$. So for $h$ small enough the step control never halves the step, and $\delta = h$ throughout.

*Proof.* Success is Lemma 3. $T$ is Lipschitz on $U$ by Lemma 2 (2), and $|q - p| = O(\delta)$, so the angle is $O(\delta)$. $\square$

**Lemma 5 (the sign of the tangent).** Along the trace, the sign rule of line L5 keeps the direction of travel. That is, if $t'$ points along $C$ in the direction of travel at $p$, the chosen $t$ at the next point $q$ does too.

*Proof.* $T$ is continuous along $C$. The direction of travel at $q$ is $\pm T(q)$ with the sign that makes it close to the direction at $p$, which by Lemma 4 is the sign with $T(q) \cdot t' > 0$. $\square$

**Theorem.** Assume $x_0$ is close enough to $C$ that CORRECT$(x_0) = p_0 \in C$ (Lemma 2 (3)), that the box contains $U$, and that $h$ is small enough for Lemmas 3 and 4 and also satisfies the *separation condition*: any two points of $C$ at distance at most $3h$ in space are joined by an arc of $C$ of length at most $4h$. Then MARCH returns a closed polyline whose vertices lie on $C$, in the order of $C$, with consecutive vertices at arc distance $h + O(h^2)$, and every point of $C$ is within $O(h^2)$ of the polyline. No vertex lies on another component of $\{F = 0\}$.

*Proof.* By Lemmas 3 to 5, the trace for $d = +1$ produces points $p_0, p_1, p_2, \ldots$ on $C$ with arc positions $s_k$, measured from $p_0$ in the direction of travel, that grow by $h + O(h^2)$ at each step. Line L8 never fires, since the points stay on $C \subset U \subseteq$ box. The separation condition exists for small $h$: $C$ is a compact embedded $C^2$ curve, so chord length and arc length are comparable for short arcs, and points far apart along $C$ are a positive distance apart in space.

*The trace leaves.* Once $s_k > 4h$ and $L - s_k > 4h$, the arc distance from $p_k$ to $p_0$ is more than $4h$, so by the separation condition $|p_k - p_0| > 3h > 2h$. So the flag of line L9 is set after a bounded number of steps.

*No early closure.* Suppose line L9 fires at step $k$ with $|p_k - p_0| \le h$. By the separation condition the arc distance from $p_k$ to $p_0$ is at most $4h$, so $s_k \le 4h$ or $L - s_k \le 4h$. The first case is impossible. The flag was set by an earlier point $p_j$ with $|p_j - p_0| > 2h$, so $s_k > s_j \ge |p_j - p_0| > 2h$. On arcs of length at most $4h$, chord and arc length differ by a factor $1 - O(h^2)$, so $|p_k - p_0| \ge s_k (1 - O(h^2)) > h$ for small $h$, against $|p_k - p_0| \le h$. So $L - s_k \le 4h$, and the trace has gone around $C$.

*It closes.* The positions $s_k$ grow by about $h$ until $L - s_k < h/2 + O(h^2)$ for some $k$. Then $|p_k - p_0| \le L - s_k < h$, so line L9 fires at the latest there. It returns the points $p_0, \ldots, p_{k - 1}$ in order along $C$, and the closing segment from $p_{k - 1}$ to $p_0$ spans an arc of length at most $2h + O(h^2)$.

*Cover.* Each segment joins two points of $C$ at arc distance at most $2h + O(h^2)$, and a chord of an arc of length $\ell$ and curvature at most $\kappa_{\max}$ is within $\kappa_{\max} \ell^2 / 8 + O(\ell^3)$ of the arc. Every point of $C$ lies on one of these arcs, which gives the $O(h^2)$ bound.

*Nothing else.* Every vertex is the output of CORRECT from a point in the tube, which by Lemma 2 lies on $C$. $\blacksquare$

**Corollary (one component).** Under the assumptions of the theorem, MARCH returns points of $C$ only. If $\{F = 0\}$ has a second component $C'$, no vertex lies on $C'$, however large the box. So a marching method finds every component only if it is given a start point on each, which is the reason for loop detection and start point searches.

**What is not claimed.** The bounds on $h$ depend on $\rho$, $K$, $\beta$, the curvature of $C$ and the separation condition, none of which MARCH computes. With a larger step, the predictor can land in the tube of another branch, and Lemma 2 no longer protects the trace; this is branch jumping. At a singular point, where Lemma 2 (2) fails, the theorem says nothing, and the passage of the trace through the double point of Viviani's curve on the page is an observed behavior of the example, not a consequence of the theorem.
