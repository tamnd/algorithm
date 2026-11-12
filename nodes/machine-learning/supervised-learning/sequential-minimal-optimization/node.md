---
tag: 9XT69N
kind: algorithm
slug: sequential-minimal-optimization
name: Sequential minimal optimization
aliases:
- SMO
- Platt's SMO algorithm
area: machine-learning/supervised-learning
level: advanced
summary: "Solves the soft margin SVM dual by optimizing two Lagrange multipliers at a time in closed form, chosen by Platt's heuristics, so no numerical QP solver is needed."
solves: [svm-training]
model: real-ram
complexity:
  vars: {n: the number of training points, t: the cost of one kernel evaluation, s: the number of successful two-variable steps}
  time: {worst: "O(n^2 t + s n)", best: "Θ(n^2 t)"}
  space: {extra: Θ(n^2)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 1998
  people: [John C. Platt]
  note: Platt published SMO as a Microsoft Research technical report in 1998. Keerthi, Shevade, Bhattacharyya and Murthy improved its stopping test in 2001, and Fan, Chen and Lin gave the second order working set selection of LIBSVM in 2005.
prereqs: [support-vector-machine, kkt-conditions, coordinate-descent]
see_also: [svm-training, support-vector-machine, support-vector-regression, quadratic-programming, kkt-conditions, coordinate-descent, kernel-trick, hinge-loss]
sources:
  - paper: "John C. Platt, Sequential minimal optimization: a fast algorithm for training support vector machines, Microsoft Research Technical Report MSR-TR-98-14, 1998"
    locator: Section 2 (the analytic solution for two multipliers, the bounds L and H, the threshold update, and the heuristics for choosing the two multipliers) and the pseudocode in the appendix
  - paper: "S. S. Keerthi, S. K. Shevade, C. Bhattacharyya and K. R. K. Murthy, Improvements to Platt's SMO algorithm for SVM classifier design, Neural Computation 13(3), 2001"
    locator: pp. 637 to 649 (the two thresholds b_up and b_low, and the maximal violating pair)
  - paper: "Rong-En Fan, Pai-Hsuen Chen and Chih-Jen Lin, Working set selection using second order information for training support vector machines, Journal of Machine Learning Research 6, 2005"
    locator: pp. 1889 to 1918 (WSS3, the second order choice of the second multiplier)
  - paper: doi:10.1145/1961189.1961199
    title: Chih-Chung Chang and Chih-Jen Lin, LIBSVM, a library for support vector machines, ACM Transactions on Intelligent Systems and Technology 2(3), 2011
    locator: Section 4 (the SMO type decomposition method, the stopping condition and shrinking)
  - book: isbn:9780262194754
    title: Bernhard Schölkopf and Alexander J. Smola, Learning with Kernels, MIT Press, 2002
    locator: Chapter 10 (implementation; sequential minimal optimization)
---

Sequential minimal optimization (SMO) trains a [support vector machine](/support-vector-machine/) by solving its dual quadratic program two variables at a time. The equality constraint $\sum_i \alpha_i y_i = 0$ means that one multiplier cannot move alone, but two can, and the best move of two multipliers has a closed form: a one-dimensional quadratic, clipped to a box. Platt (1998) combined this step with heuristics that choose the pair, and with a cache of errors. SMO needs no numerical QP solver and only $O(n)$ extra memory beyond the kernel values, and its descendants are the solvers of LIBSVM and scikit-learn.

## In plain words

Training an SVM means choosing one weight per training point, under two rules: each weight lies between 0 and a limit $C$, and the weights of the positive points and of the negative points have the same total. Changing one weight alone would break the second rule, so SMO changes two weights at a time, one up and one down so that the totals stay equal.

For two weights, the best change can be worked out with a short formula, and then cut back if it leaves the allowed range. SMO repeats this. It picks a point that breaks the optimality conditions, then a partner that will give a large step, and stops when every point satisfies the conditions within a small tolerance.

## The problem

The input is a kernel matrix $K_{ij} = k(x_i, x_j)$, labels $y_i \in \{-1, +1\}$, a box limit $C > 0$ and a tolerance $\tau > 0$. The task is the soft margin SVM dual of [SVM training](/svm-training/):

$$\max_{\alpha} \; W(\alpha) = \sum_i \alpha_i - \tfrac12 \sum_{i,j} \alpha_i \alpha_j y_i y_j K_{ij} \quad \text{subject to } 0 \le \alpha_i \le C, \; \sum_i \alpha_i y_i = 0.$$

The classifier is $f(x) = \sum_j \alpha_j y_j k(x_j, x) + b$. Platt writes $u = w \cdot x - b$, so his threshold has the opposite sign of $b$ here. The error of point $i$ is $E_i = f(x_i) - y_i$. The [KKT conditions](/kkt-conditions/) at an optimum, with $r_i = y_i E_i = y_i f(x_i) - 1$, are

$$\alpha_i = 0 \Rightarrow r_i \ge 0, \qquad 0 < \alpha_i < C \Rightarrow r_i = 0, \qquad \alpha_i = C \Rightarrow r_i \le 0.$$

A point violates them by more than $\tau$ when $r_i < -\tau$ and $\alpha_i < C$, or when $r_i > \tau$ and $\alpha_i > 0$.

## The algorithm

```pseudo id=main
SMO(K, y, C, τ, ε)
L1  α ← 0, b ← 0, E_i ← −y_i for each i                ▷ f = 0 at the start
L2  changed ← 0, examineAll ← true
L3  while changed > 0 or examineAll do
L4      changed ← 0
L5      for each i in (all points if examineAll, else the points with 0 < α_i < C) do
L6          changed ← changed + EXAMINE(i)
L7      if examineAll then examineAll ← false else if changed = 0 then examineAll ← true
L8  return (α, b)

EXAMINE(i2)
L9  r ← y_i2 E_i2
L10 if (r < −τ and α_i2 < C) or (r > τ and α_i2 > 0) then              ▷ i2 violates the KKT conditions
L11     if more than one point is non-bound then i1 ← argmax |E_i1 − E_i2| over them; if TAKESTEP(i1, i2) then return 1
L12     for each non-bound i1, from a random start do if TAKESTEP(i1, i2) then return 1
L13     for each i1, from a random start do if TAKESTEP(i1, i2) then return 1
L14 return 0

TAKESTEP(i1, i2)                                       ▷ write 1, 2 for i1, i2 and s = y_1 y_2
L15 if i1 = i2 then return false
L16 if y_1 ≠ y_2 then L ← max(0, α_2 − α_1), H ← min(C, C + α_2 − α_1) else L ← max(0, α_1 + α_2 − C), H ← min(C, α_1 + α_2)
L17 if L = H then return false
L18 η ← K_11 + K_22 − 2 K_12
L19 if η > 0 then a_2 ← clip(α_2 + y_2 (E_1 − E_2)/η, L, H)
L20 else a_2 ← the end, L or H, with the larger W (α_2 if they differ by at most ε)
L21 if |a_2 − α_2| < ε (a_2 + α_2 + ε) then return false
L22 a_1 ← α_1 + s (α_2 − a_2)
L23 b_1 ← b − E_1 − y_1 (a_1 − α_1) K_11 − y_2 (a_2 − α_2) K_12, b_2 ← b − E_2 − y_1 (a_1 − α_1) K_12 − y_2 (a_2 − α_2) K_22, b ← b_1 if 0 < a_1 < C, else b_2 if 0 < a_2 < C, else (b_1 + b_2)/2
L24 update E_i for each i by the change of f, and set α_1 ← a_1, α_2 ← a_2
L25 return true
```

**The two-variable step (lines L16 to L22).** Fix every multiplier except $\alpha_1$ and $\alpha_2$. The constraint $\sum_i \alpha_i y_i = 0$ gives $y_1 \alpha_1 + y_2 \alpha_2 = \text{const}$, so $\alpha_1 = \text{const} - s \alpha_2$, and the box $[0, C]^2$ cuts this line to a segment. If $y_1 \ne y_2$, then $\alpha_2 - \alpha_1$ is constant and the segment is $\alpha_2 \in [\max(0, \alpha_2 - \alpha_1), \min(C, C + \alpha_2 - \alpha_1)]$. If $y_1 = y_2$, then $\alpha_1 + \alpha_2$ is constant and the segment is $[\max(0, \alpha_1 + \alpha_2 - C), \min(C, \alpha_1 + \alpha_2)]$. These are $L$ and $H$ of line L16. Along the segment, $W$ is a quadratic in $\alpha_2$ with second derivative $-\eta$, where $\eta = K_{11} + K_{22} - 2K_{12} = \lVert \varphi(x_1) - \varphi(x_2) \rVert^2 \ge 0$, and with derivative $y_2 (E_1 - E_2)$ at the current point. So when $\eta > 0$ the unconstrained maximum is $\alpha_2 + y_2 (E_1 - E_2)/\eta$, and because the function is concave in one variable, clipping it to $[L, H]$ gives the maximum on the segment. When $\eta = 0$ (two points with the same features), $W$ is linear on the segment and the better end wins (line L20). With an indefinite kernel $\eta < 0$ is possible, and the same rule applies.

**The threshold (line L23).** After the step, $b_1$ is the threshold that makes $E_1 = 0$, so $y_1 f(x_1) = 1$, and $b_2$ makes $E_2 = 0$. If $a_1$ is strictly inside $(0, C)$, the KKT conditions demand $y_1 f(x_1) = 1$, so $b = b_1$. If both new values are at bounds, every $b$ between $b_1$ and $b_2$ satisfies the KKT conditions of the two points, and Platt takes the midpoint. If both are free, $b_1 = b_2$.

**The heuristics.** The outer loop (lines L3 to L7) alternates one pass over all points with repeated passes over the non-bound points, where $0 < \alpha_i < C$, since those are the ones most likely to still violate the conditions. The first multiplier $i_2$ is any violator. For the second, line L11 picks the point that maximizes $|E_1 - E_2|$, which is a cheap estimate of the step size $|E_1 - E_2|/\eta$. If that step fails, lines L12 and L13 try the non-bound points and then all points, each from a random start so as not to favor the points at the front. Line L21 refuses steps that change $\alpha_2$ by a tiny relative amount.

**The error cache (line L24).** After a step, $f$ changes by $y_1 (a_1 - \alpha_1) k(x_1, \cdot) + y_2 (a_2 - \alpha_2) k(x_2, \cdot) + \Delta b$, so each $E_i$ is updated in $O(1)$ from two kernel values. Platt caches $E_i$ for the non-bound points and computes the others when needed; the implementation here caches all of them.

## Example

Take six points in $\mathbb{R}^2$ with the linear kernel and $C = 1$: positive $(2, 2)$, $(1, 3)$, $(3, 1)$ and negative $(0, 0)$, $(1, 0)$, $(2, 3)$. The negative point $(2, 3)$ lies among the positive ones, so the data is not separable.

**One step by hand.** At the start $\alpha = 0$, $b = 0$ and $E_i = -y_i$. Take $i_1 = (0, 0)$ with $y_1 = -1$ and $i_2 = (2, 2)$ with $y_2 = +1$. Then $K_{11} = 0$, $K_{12} = 0$, $K_{22} = 8$, so $\eta = 8$. The labels differ, so $L = \max(0, 0 - 0) = 0$ and $H = \min(1, 1 + 0 - 0) = 1$. The step is

$$a_2 = 0 + (+1)\frac{E_1 - E_2}{\eta} = \frac{1 - (-1)}{8} = \frac14, \qquad a_1 = 0 + (-1)(0 - \tfrac14) = \tfrac14.$$

Both are free. The thresholds are $b_1 = 0 - 1 - 0 - 0 = -1$ and $b_2 = 0 - (-1) - 0 - (+1)\tfrac14 \cdot 8 = -1$, equal as they should be. Now $w = \tfrac14 (2, 2) - \tfrac14 (0, 0) = (\tfrac12, \tfrac12)$ and $f(x) = \tfrac12 x_1 + \tfrac12 x_2 - 1$, which puts both points exactly on their margins: $f(0, 0) = -1$ and $f(2, 2) = 1$.

**The full run.** With $\tau = 10^{-7}$, SMO stops after 37 successful steps with $W = 28/9 \approx 3.11111$, $w = (2/3, 2/3)$ and $b = -5/3$, to within $10^{-7}$. The points $(1, 3)$, $(3, 1)$, $(2, 2)$ and $(1, 0)$ lie on their margins, and $(2, 3)$ has $\alpha = C$ with $y f = -5/3$. An exact solver with fractions, which tries every split of the points into $\alpha = 0$, free and $\alpha = C$ and solves the KKT system for each, gives the same $W$, $w$, $b$ and decision values. Its $\alpha = (0, \tfrac{17}{18}, \tfrac56, 0, \tfrac79, 1)$ differs from the $\alpha \approx (1, \tfrac49, \tfrac13, 0, \tfrac79, 1)$ of SMO. Both are optimal: the dual has many optimal $\alpha$ here, because four margin points in $\mathbb{R}^2$ give more multipliers than conditions. So compare $W$, $w$, $b$ and $f$, not $\alpha$.

## Correctness

Each step keeps $\alpha$ feasible: line L22 keeps $y_1 \alpha_1 + y_2 \alpha_2$ fixed, and $[L, H]$ is exactly the part of the line inside the box. Each successful step increases $W$, since it maximizes $W$ on a segment that contains the old point. Write $F_i = \sum_j \alpha_j y_j K_{ij} - y_i$, so that $E_i = F_i + b$. Point $i$ is satisfied with threshold $b$ if and only if $b \ge -F_i - \tau$ when $i$ can move up in the direction $y_i$ (that is, $y_i = 1, \alpha_i < C$ or $y_i = -1, \alpha_i > 0$), and $b \le -F_i + \tau$ when it can move down. If no $b$ satisfies all points, there are $i$ that can move up and $j$ that can move down with $F_j - F_i > 2\tau$. Moving $\alpha_i$ by $y_i t$ and $\alpha_j$ by $-y_j t$ is feasible for small $t > 0$ and has slope $F_j - F_i > 0$, so whichever of $i, j$ violates the conditions finds a successful step in line L13. Hence, with $\varepsilon = 0$ in exact arithmetic, SMO stops only when some threshold satisfies every KKT condition within $\tau$. The proofs folder has the full argument.

The threshold returned by line L23 need not be that threshold: Keerthi et al. (2001) showed that a single $b$ can make points look like violators when the multipliers are already optimal, or hide a violation. Their fix keeps two thresholds, $b_{\text{up}} = \min$ and $b_{\text{low}} = \max$ of the bounds above, and stops when $b_{\text{low}} \le b_{\text{up}} + 2\tau$.

Platt did not prove that SMO stops. Keerthi and Gilbert (2002) proved finite termination for a generalized SMO that always picks a violating pair, and Lin (2001, 2002) proved convergence for the maximal violating pair rule.

## Complexity

- **Each step.** Lines L15 to L23 cost $O(1)$ kernel values. The error update of line L24 costs $O(n)$ kernel values. The second choice of line L11 costs $O(n)$. So a successful step costs $O(n t)$, or $O(n)$ with the kernel matrix in memory.
- **The number of steps.** It depends on the data and on $C$. Platt reported running times that grew between linearly and quadratically with $n$ on his test problems, much faster than chunking with a QP solver. Large $C$ and overlapping classes need more steps, because more multipliers end strictly inside $(0, C)$.
- **Memory.** SMO needs $O(n)$ for $\alpha$ and the error cache, plus a kernel cache. The table in the front matter assumes the whole kernel matrix is stored, which costs $\Theta(n^2 t)$ time and $\Theta(n^2)$ space.

## Properties

- **No QP solver.** Each subproblem is solved in closed form.
- **Feasible at every step.** The current $\alpha$ always satisfies the constraints, so the algorithm can stop early with a valid, if not optimal, classifier.
- **Monotone.** $W$ never decreases.
- **Sparse.** Most multipliers stay at 0 when $C$ is not large, so most points never enter the error cache as non-bound points.
- **Randomized.** The random start points of lines L12 and L13 change the order of the steps, and possibly which optimal $\alpha$ is returned when the optimum is not unique. The classifier $f$ is unique when $K$ is positive definite.

## Variants and improvements

- **Two thresholds (Keerthi et al. 2001).** Track $b_{\text{up}}$ and $b_{\text{low}}$ and choose the maximal violating pair; this removes most wasted steps and gives a sound stopping test.
- **Second order selection (WSS3, Fan, Chen and Lin 2005).** Pick $i$ as the maximal violator, and then $j$ to maximize the guaranteed increase $b_{ij}^2/\eta_{ij}$. This is the rule of LIBSVM.
- **Shrinking and caching.** Remove points that are likely to stay at a bound, and keep the most used kernel columns in a cache.
- **Regression and one-class problems.** The same two-variable step solves the dual of [support vector regression](/support-vector-regression/) and of the one-class SVM, with $2n$ variables for SVR.
- **Linear kernels.** For a linear kernel, keep $w$ explicitly; then $f(x_i)$ costs $O(d)$. Dual coordinate descent of [SVM training](/svm-training/) goes further and drops the bias, so it can move one variable at a time.

## When to use it

Use SMO, or the SMO type solver in LIBSVM, to train a kernel SVM on up to a few hundred thousand points. For a linear kernel with many points and sparse features, dual coordinate descent or Pegasos is faster. For tiny problems a general QP solver is simple and exact.

## Pitfalls

- **The step threshold.** With $\varepsilon = 10^{-3}$ in line L21, a step that changes $\alpha_2$ by less than about $0.1\,\%$ is refused. On 30 points with $C = 10$ and overlapping classes (seed 3), the run then ends with a KKT violation of $0.086$, far above $\tau = 10^{-3}$. With $\varepsilon = 10^{-8}$ the violation is below $\tau$ on every test problem.
- **Sign conventions.** Platt's $u = w \cdot x - b$ flips the sign of the threshold. Mixing conventions breaks the update of line L23.
- **Rounding at the bounds.** A multiplier that should be 0 can end at $10^{-17}$ and count as non-bound. Snap values within a tiny relative distance of 0 or $C$ onto the bound.
- **Comparing solutions.** The optimal $\alpha$ need not be unique, as in the example. Test the objective, $w$ or $f$, and the KKT conditions.
- **A stale error cache.** Forgetting to apply the change of $b$ to every cached error gives wrong choices of pairs and wrong stopping.
- **Kernels that are not PSD.** Then $\eta < 0$ can happen, the dual is not concave, and SMO finds only a local optimum.

## Implementations

## History

Before SMO, SVMs were trained by chunking (Vapnik) or by decomposition with a general QP solver on a working set (Osuna, Freund and Girosi 1997). John Platt's 1998 technical report took the working set down to its minimum size of two, where the subproblem has a closed form. Keerthi, Shevade, Bhattacharyya and Murthy (2001) found the inefficiency of the single threshold and proposed two thresholds and the maximal violating pair. Fan, Chen and Lin (2005) added second order working set selection, which became the solver of LIBSVM.

## References
