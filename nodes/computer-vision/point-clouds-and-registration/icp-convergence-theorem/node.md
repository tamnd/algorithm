---
tag: BF3FAD
kind: theorem
slug: icp-convergence-theorem
name: Monotone convergence of ICP
aliases:
- ICP local convergence
area: computer-vision/point-clouds-and-registration
level: core
summary: "No ICP iteration increases the mean squared closest-point distance, so the cost converges and, for finite clouds, ICP stops at a fixed point. A local minimum is not guaranteed."
prereqs: [iterative-closest-point]
see_also: [coordinate-descent, kabsch-algorithm, optimal-superposition, nearest-neighbor-search, expectation-maximization, trimmed-icp, go-icp, point-to-plane-icp]
sources:
  - paper: doi:10.1109/34.121791
    title: "Paul J. Besl and Neil D. McKay, A method for registration of 3-D shapes, IEEE Transactions on Pattern Analysis and Machine Intelligence 14(2), 1992, 239-256"
    locator: "The convergence theorem for the ICP algorithm and its proof by the two inequalities of the match step and the fit step"
  - paper: doi:10.1109/34.88573
    title: "Shinji Umeyama, Least-squares estimation of transformation parameters between two point patterns, IEEE Transactions on Pattern Analysis and Machine Intelligence 13(4), 1991, 376-380"
    locator: "The least squares rotation and translation for given pairs, with the proper rotation (determinant +1)"
  - paper: doi:10.1007/s11263-006-5167-2
    title: "Helmut Pottmann, Qi-Xing Huang, Yong-Liang Yang and Shi-Min Hu, Geometry and convergence analysis of algorithms for registration of 3D shapes, International Journal of Computer Vision 67(3), 2006, 277-296"
    locator: "The convergence analysis of ICP: linear convergence, a rate result that the monotone theorem does not give"
---

The monotone convergence theorem of [iterative closest point](/iterative-closest-point/) (ICP) says that no iteration of ICP increases the mean squared distance from the moved source points to their closest target points. So the sequence of costs converges. For finite point clouds more is true: the cost becomes constant after finitely many iterations, and ICP with a repeat test stops at a pose that is a fixed point of its two steps. Besl and McKay stated the result in 1992 as convergence to a local minimum. Their proof gives the monotone decrease. It does not give a local minimum when a moved point has two closest target points at the same distance, and it gives no global minimum and no rate.

## Statement

Let $P = (p_1, \ldots, p_n)$ and $Q = \{q_1, \ldots, q_m\}$ be finite point sets in $\mathbb{R}^3$, with $n, m \ge 1$. For a rigid motion $(R, t)$, $R \in SO(3)$, $t \in \mathbb{R}^3$, and a match $c : \{1, \ldots, n\} \to \{1, \ldots, m\}$, let

$$F(R, t, c) = \frac{1}{n} \sum_{i=1}^n |R p_i + t - q_{c(i)}|^2, \qquad E(R, t) = \frac{1}{n} \sum_{i=1}^n \min_j |R p_i + t - q_j|^2 .$$

ICP starts from a pose $(R_0, t_0)$ and, for $k = 0, 1, 2, \ldots$:

1. **Match.** $c_k$ is a closest-point match of $(R_k, t_k)$: $c_k(i)$ is an index $j$ that minimizes $|R_k p_i + t_k - q_j|$. A fixed rule, such as the lowest index, breaks ties.
2. **Fit.** $(R_{k+1}, t_{k+1}) = \mathrm{FIT}(c_k)$ is a minimizer of $F(\cdot, \cdot, c_k)$ over $SO(3) \times \mathbb{R}^3$. FIT is a function of the match, for example the [Kabsch algorithm](/kabsch-algorithm/) with the sign fix.

Write $e_k = E(R_k, t_k)$ and $d_k = F(R_{k+1}, t_{k+1}, c_k)$. Arithmetic is exact.

**Theorem.**

- (a) **Monotone.** $e_k \ge d_k \ge e_{k+1} \ge 0$ for every $k$, so $(e_k)$ and $(d_k)$ converge to the same limit.
- (b) **Finite.** The sequence $(e_k)$ is constant from some index $K \le m^n$ on. So ICP with the stop rule "stop when $c_k = c_{k-1}$ or $e_k = e_{k-1}$" stops after at most $m^n + 1$ iterations.
- (c) **Fixed point.** If ICP stops at iteration $k \ge 1$ by that rule, the returned pose $(R_k, t_k)$ has a closest-point match $c$ such that $(R_k, t_k)$ minimizes $F(\cdot, \cdot, c)$.
- (d) **Local minimum without ties.** If, in addition, every moved point $R_k p_i + t_k$ has only one closest point in $Q$, then $(R_k, t_k)$ is a local minimum of $E$.

Besl and McKay proved part (a): their argument is the two inequalities of Lemma 1 and Lemma 2 below. They stated the conclusion as monotone convergence to a local minimum. Parts (b), (c) and (d) are elementary consequences, written out here; this page does not claim that they appear in the paper in this form.

## In plain words

ICP repeats two steps. First, it pairs each source point with its closest target point. Then it moves the source to fit those pairs as well as possible. Each step can only make the average squared gap smaller or keep it the same. So the gap goes down and settles. There are only finitely many ways to pair the points, so ICP stops after finitely many rounds at a pose where neither step changes anything.

That pose is not always the best one. It is often only the bottom of a nearby valley. If a point is exactly as close to two target points, the pose can even be on a slope.

## Proof

**Lemma 1 (fit step).** For every match $c$ and every pose $(R, t)$, $F(\mathrm{FIT}(c), c) \le F(R, t, c)$.

*Proof.* This is the definition of FIT. A minimizer exists: the minimum over $t$ for fixed $R$ is attained at $t = \bar q_c - R \bar p$, where $\bar p$ and $\bar q_c$ are the centroids of the pairs, and the remaining function of $R$ is continuous on the compact set $SO(3)$. The [Kabsch algorithm](/kabsch-algorithm/) with the sign fix computes one (Umeyama 1991). $\square$

**Lemma 2 (match step).** For every pose $(R, t)$ and every match $c$, $E(R, t) \le F(R, t, c)$, with equality exactly when $c$ is a closest-point match of $(R, t)$.

*Proof.* Term by term, $|R p_i + t - q_{c(i)}|^2 \ge \min_j |R p_i + t - q_j|^2$. The sums are equal only if every term is equal, that is, only if every $c(i)$ is a closest index. $\square$

*Proof of (a).* By Lemma 2 with equality, $e_k = F(R_k, t_k, c_k)$. By Lemma 1 with $(R, t) = (R_k, t_k)$, $d_k = F(R_{k+1}, t_{k+1}, c_k) \le F(R_k, t_k, c_k) = e_k$. By Lemma 2 at the pose $(R_{k+1}, t_{k+1})$, $e_{k+1} \le F(R_{k+1}, t_{k+1}, c_k) = d_k$. Every term is a squared distance, so $e_k \ge 0$. A sequence that does not increase and is bounded below converges, and $d_k$ lies between $e_{k+1}$ and $e_k$, so it has the same limit. $\square$

*Proof of (b).* For $k \ge 1$, $e_k = E(\mathrm{FIT}(c_{k-1}))$, so $e_k$ is a value of the function $c \mapsto E(\mathrm{FIT}(c))$ on the $m^n$ matches. Hence $e_1, e_2, \ldots$ take at most $m^n$ distinct values. A sequence that does not increase changes its value at most (number of values minus one) times, so $(e_k)_{k \ge 1}$ changes at most $m^n - 1$ times and is constant from some $K \le m^n$ on. Then $e_{K+1} = e_K$, and the stop rule holds at the latest at iteration $K + 1 \le m^n + 1$. $\square$

*Proof of (c).* There are two cases at the stop.

- Case $c_k = c_{k-1}$. Then $(R_k, t_k) = \mathrm{FIT}(c_{k-1}) = \mathrm{FIT}(c_k)$ minimizes $F(\cdot, \cdot, c_k)$ by Lemma 1, and $c_k$ is a closest-point match of $(R_k, t_k)$ by the match step.
- Case $e_k = e_{k-1}$. By (a), $e_{k-1} \ge d_{k-1} \ge e_k = e_{k-1}$, so $F(R_k, t_k, c_{k-1}) = d_{k-1} = e_k = E(R_k, t_k)$. By the equality case of Lemma 2, $c_{k-1}$ is a closest-point match of $(R_k, t_k)$, and $(R_k, t_k) = \mathrm{FIT}(c_{k-1})$ minimizes $F(\cdot, \cdot, c_{k-1})$ by Lemma 1. $\square$

*Proof of (d).* Let $c$ be the match of (c). Since each closest point is unique, $c$ is the only closest-point match, and there is a gap $g > 0$ with $|R_k p_i + t_k - q_j| \ge |R_k p_i + t_k - q_{c(i)}| + g$ for every $i$ and every $j \ne c(i)$. The map $(R, t) \mapsto R p_i + t$ is continuous, so for every pose $(R, t)$ near enough to $(R_k, t_k)$ each point $R p_i + t$ moves by less than $g / 2$, and $c$ stays its unique closest-point match. For these poses, $E(R, t) = F(R, t, c) \ge F(R_k, t_k, c) = E(R_k, t_k)$, by Lemma 2 with equality and Lemma 1. $\blacksquare$

## Consequences

- **ICP is coordinate descent.** The theorem is the usual argument for alternating minimization: $F$ is minimized over the match with the pose fixed, then over the pose with the match fixed (see [coordinate descent](/coordinate-descent/)). The same argument gives the monotone decrease of [trimmed ICP](/trimmed-icp/) and of the E and M steps of [expectation maximization](/expectation-maximization/).
- **A safe stop rule.** Because the cost never rises, a test on the decrease of the cost, or on a repeated match, is a sound stop rule.
- **A local method.** The fixed point depends on the start pose. Global methods such as [Go-ICP](/go-icp/) search the whole pose space, and a coarse alignment from features usually starts ICP.
- **Not for every variant.** The proof needs both steps to minimize the same cost. [Point-to-plane ICP](/point-to-plane-icp/) takes a linearized step on a different cost, so this theorem does not cover it.

## Tightness

**No local minimum when there are ties.** Take the source points $(0, 0, 0)$, $(10, 0, 0)$, $(5, 3, 0)$ and the target points $q_1 = (2, 0, 0)$, $q_2 = (0, 0, 0)$, $q_3 = (10, 0, 0)$, $q_4 = (6, 3, 0)$. Start ICP at $R = I$, $t = (1, 0, 0)$, with ties broken by the lowest index.

- The moved point $(1, 0, 0)$ is at distance 1 from both $q_1$ and $q_2$. The tie rule picks $q_1$. The other two points pick $q_3$ (distance 1) and $q_4$ (distance 0). So $e_0 = (1 + 1 + 0)/3 = 2/3$.
- The fit for these pairs is $R = I$, $t = (1, 0, 0)$ again: the centroids are $(5, 1, 0)$ and $(6, 1, 0)$, and the cross covariance of the centered pairs is $\operatorname{diag}(40, 6, 0)$, so the rotation is $I$. So $e_1 = e_0 = 2/3$, and ICP stops.
- Along $t = (s, 0, 0)$ with $s$ just below 1, the first point now matches $q_2$, and $E = (2 s^2 + (1 - s)^2)/3$. At $s = 0.99$, $E = 0.65343 < 2/3$.

So the pose where ICP stops is not a local minimum of $E$. The reason is that $E$ is not differentiable where a closest point changes. This is why part (d) needs unique closest points. With the other tie rule ($q_2$ first), ICP would move on from the same pose.

**No global minimum.** Even with unique closest points, the local minimum of (d) depends on the start pose. The [point-to-plane ICP](/point-to-plane-icp/) page shows a scene where point-to-point ICP from the identity stops 4.26 degrees from the true pose, and the Go-ICP page shows a scene where ICP from the identity stops at the cost 0.7042 while the global minimum is 0.

**No rate.** The theorem says nothing about how fast $e_k$ falls. The bound $m^n + 1$ only counts matches. Pottmann, Huang, Yang and Hu (2006) showed that ICP converges linearly near a solution, and that the point-to-plane form converges quadratically for a zero residual problem from a good start; these are separate results.

**Convergence of the cost, not of the pose.** Part (a) says that the costs converge. Without the stop rule, the poses can keep changing among poses of the same cost, for example when ties let the match change while the cost stays the same.

## History

Besl and McKay published ICP in 1992 together with the monotone convergence theorem, in the form: ICP always converges monotonically to a local minimum of the mean squared distance. Chen and Medioni (1991, 1992) and Zhang (1992) gave related methods at about the same time. The monotone argument is the standard argument for alternating minimization. Later work refined it: Pottmann, Huang, Yang and Hu (2006) studied the rate of ICP and of its point-to-plane form with tools of differential geometry.

## References
