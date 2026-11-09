---
tag: VE2Q7W
kind: technique
slug: lexicographic-optimization
name: Lexicographic optimization
aliases:
- lexicographic ordering of objectives
- preemptive priority optimization
- lexicographic method
- preemptive optimization
area: optimization/multi-objective
level: intro
summary: Optimizes objectives in a fixed priority order, each one subject to the optimum of the previous ones.
prereqs: [scalarization, lexicographic-order]
see_also: [goal-programming, weighted-sum-method, utility-function, nadir-point, epsilon-constraint-method, lexicographic-order]
sources:
  - book: isbn:9783540213987
    title: Matthias Ehrgott, Multicriteria Optimization, second edition, Springer, 2005
    locator: Chapter 5 (lexicographic optimality and its relation to efficiency)
  - book: isbn:9780792382782
    title: Kaisa Miettinen, Nonlinear Multiobjective Optimization, Kluwer, 1999
    locator: Part II, Chapter 4 (a priori methods, lexicographic ordering)
  - paper: doi:10.1007/BF00934527
    title: H. D. Sherali and A. L. Soyster, Preemptive and nonpreemptive multi-objective programming, Relationship and counterexamples, Journal of Optimization Theory and Applications 39(2), 1983
    locator: pages 173 to 186 (weights that make a weighted sum reproduce a preemptive solution for linear programs, and counterexamples otherwise)
---

Lexicographic optimization ranks the objectives of a [multi-objective optimization](/multi-objective-optimization/) problem in a strict order of importance. It minimizes the most important objective first, then the second among the optimal solutions of the first, and so on. Its answer is always [Pareto optimal](/pareto-optimality/). It costs $p$ single-objective solves, one per objective. The preference it models is real and common, but no real-valued [utility function](/utility-function/) can represent it on a continuum, and it reaches at most $p!$ points of the front.

## In plain words

Rank your goals. Safety comes first, then cost, then speed. Among all choices, keep only the safest ones. Among those, keep only the cheapest. Among those, take the fastest.

No amount of saving on cost can make up for a small loss in safety. A lower goal only breaks ties left by the goals above it.

The answer is always a fair trade-off. A choice that is better on every count would have won at the first goal where the two differ.

## When it applies

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p \ge 2$, $y = f(x)$ is the image of $x \in X$, and $Y = f(X)$. A priority order is a permutation $\pi$ of $\{1, \ldots, p\}$; objective $\pi(1)$ is the most important. A point $\hat{x}$ is *lexicographically optimal* for $\pi$ when $(f_{\pi(1)}(\hat{x}), \ldots, f_{\pi(p)}(\hat{x}))$ is minimal in the [lexicographic order](/lexicographic-order/) over $X$.

Use it when:

- the objectives have a clear order of importance, such as safety before cost, or legal limits before profit;
- one wants a Pareto optimal point from a solver that handles only one objective, without weights;
- one needs the end points of a two-objective front, for example to compute the [nadir point](/nadir-point/), or to start the [epsilon-constraint method](/epsilon-constraint-method/).

**Lexicographic optima are Pareto optimal.** Let $\hat{x}$ be lexicographically optimal for some $\pi$. Then $\hat{x}$ is Pareto optimal.

*Proof.* Let $f(x) \prec f(\hat{x})$. Let $k$ be the first position with $f_{\pi(k)}(x) \ne f_{\pi(k)}(\hat{x})$; it exists because $f(x) \ne f(\hat{x})$. Since $f(x) \leqq f(\hat{x})$, $f_{\pi(k)}(x) < f_{\pi(k)}(\hat{x})$. The two vectors agree before position $k$, so $x$ is lexicographically smaller, a contradiction. $\square$

**No utility on a continuum.** The lexicographic order on $\mathbb{R}^2$ has no real-valued representation, as proved on the [utility function](/utility-function/) page. So no scalarizing function of the form $s(f(x))$, continuous or not, can model it on all of $\mathbb{R}^2$. On a finite or bounded integer set it can be modelled, as follows.

**A weighted sum for integer objectives.** Let all values $f_i(x)$ be integers in an interval of length $R$, that is, $|f_i(x) - f_i(x')| \le R$ for all $i, x, x'$. Let $M = R + 1$ and give objective $\pi(k)$ the weight $M^{p - k}$. Then the minimizers of this weighted sum are exactly the lexicographic optima.

*Proof.* Let $x$ and $x'$ have different images, and let $k$ be the first position where they differ, with $f_{\pi(k)}(x) < f_{\pi(k)}(x')$, so the difference is at least 1. The weighted sum of $x'$ minus that of $x$ is at least $M^{p - k} - \sum_{j > k} R\, M^{p - j} = M^{p - k} - R (M^{p - k} - 1)/(M - 1) = 1 > 0$. So $x$ has the smaller sum exactly when it is lexicographically smaller. $\square$

The weights grow like $M^{p-1}$. For large ranges this causes overflow or loss of precision in floating point, so the sequential method is better. For linear programs Sherali and Soyster (1983) show that suitable finite weights always exist. For nonlinear problems they need not exist: minimize $f_1(t) = t$ and $f_2(t) = 1 - \sqrt{t}$ over $t \in [0, 1]$. The lexicographic optimum for $\pi = (1, 2)$ is $t = 0$ with the image $(0, 1)$. For weights $\lambda > 0$, $\lambda_1 t + \lambda_2 (1 - \sqrt{t}) < \lambda_2$ for small $t > 0$, so $t = 0$ is never optimal. The point $(0, 1)$ is Pareto optimal but not properly efficient: near it, a tiny loss in $f_1$ buys a much larger gain in $f_2$.

## The template

```pseudo id=main
LEXICOGRAPHIC(X, f, π)
L1  X_0 ← X
L2  for k ← 1 to p do
L3      v_k ← min { f_{π(k)}(x) : x ∈ X_{k−1} }
L4      X_k ← { x ∈ X_{k−1} : f_{π(k)}(x) ≤ v_k }
L5  return any x in X_p
```

In practice line L4 adds the constraint $f_{\pi(k)}(x) \le v_k$ to the problem, and line L3 of the next round solves it. The constraint is $\le$, not $=$, because no feasible point is below $v_k$.

**Correctness.** By induction, $X_k$ is the set of $x \in X$ whose first $k$ entries in the order $\pi$ are lexicographically minimal. So $X_p$ is the set of lexicographic optima.

**Cost.** $p$ single-objective solves, each with up to $p - 1$ extra constraints. If some $X_k$ has only one image, the remaining solves can be skipped.

### A worked example

Take $a = (2, 9)$, $b = (3, 6)$, $c = (4, 7)$, $d = (5, 4)$, $e = (7, 3)$, $f = (8, 5)$ and $g = (9, 1)$, and add the point $a' = (2, 10)$.

| order | step | value | points kept |
|---|---|---|---|
| $(1, 2)$ | $\min y_1$ | 2 | $a$, $a'$ |
| | $\min y_2$ among them | 9 | $a$ |
| $(2, 1)$ | $\min y_2$ | 1 | $g$ |
| | $\min y_1$ among them | 9 | $g$ |

The point $a'$ also minimizes $y_1$ but is dominated by $a$; the second step removes it. The two lexicographic optima $a$ and $g$ are the end points of the front, and the [nadir point](/nadir-point/) is $(g_1, a_2) = (9, 9)$.

The values lie in $[1, 10]$, so $R = 9$ and $M = 10$. The weighted sum $10 y_1 + y_2$ gives $29, 30, 36, 47, 54, 73, 85, 91$ for $a, a', b, c, d, e, f, g$, so its minimizer is $a$, as the theorem says.

## Classic examples

- **Preemptive [goal programming](/goal-programming/).** The deviations from the goals are put into priority levels and minimized in order.
- **End points of a front.** For two objectives, the two lexicographic optima are the extreme points of the front, and they give the [nadir point](/nadir-point/) exactly.
- **Phase one and phase two of the simplex method.** Minimizing the infeasibility first and the cost second is a lexicographic problem with two objectives.
- **Tie-breaking in algorithms.** Many algorithms break ties of a main cost by a second key, for example the shortest path with the fewest edges among the shortest ones. This is lexicographic optimization with $p = 2$.

## Variations

- **Relaxed levels.** Line L4 keeps the solutions within a tolerance, $f_{\pi(k)}(x) \le v_k + \tau_k$, so that a lower objective can buy a large gain for a small loss in a higher one. With $\tau_k > 0$, the answer is no longer always Pareto optimal, and a final cleanup step is needed.
- **Lexicographic max-ordering.** Sort the values of each solution from the worst to the best and compare these sorted vectors lexicographically. It gives fair solutions when the objectives are of the same kind.
- **Weights instead of stages.** The weighted sum with $M^{p-k}$ is one solve, but it needs exact arithmetic or small ranges.

## Pitfalls

- **Floating point.** The constraint $f_{\pi(k)}(x) \le v_k$ with a value $v_k$ from a floating point solver may make the next problem infeasible. Add a small tolerance, and accept that the answer is then only nearly lexicographic.
- **Too strong a preference.** Strict priorities ignore any amount of gain in lower objectives. A decision maker often accepts a tiny loss in the first objective for a large gain elsewhere, and the method cannot show this.
- **Few points.** Each order gives one point, so all orders together give at most $p!$ points of the front. It is not a method to trace the front.
- **Huge weights.** The one-solve weighted form with $M^{p-1}$ overflows or loses precision for large ranges or many objectives.

## Exercises

1. Show that for $p = 2$ the two lexicographic optima, for $\pi = (1, 2)$ and $\pi = (2, 1)$, coincide if and only if the front has a single point. *Answer:* if they coincide at $\hat{y}$, then $\hat{y}$ attains the ideal point, so the front is $\{\hat{y}\}$. Conversely a single front point is optimal for both orders.
2. For integer objectives in $\{0, \ldots, R\}$, show that the weights $R^{p-1}, \ldots, R, 1$ can fail, and that $M = R + 1$ is the smallest base that always works. *Answer:* with $p = 2$, $R = 2$, the weights $(2, 1)$ give the equal sums $2 \cdot 0 + 2 = 2 \cdot 1 + 0$ for $(0, 2)$ and $(1, 0)$, so $(1, 0)$ is also optimal, though $(0, 2)$ is lexicographically smaller.

## References
