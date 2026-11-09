---
tag: 5VREF5
kind: algorithm
slug: weiszfelds-algorithm
name: Weiszfeld's algorithm
aliases:
- Weiszfeld iteration
- Weiszfeld's method
- Weiszfeld-Kuhn algorithm
area: geometry/geometric-optimization
level: core
summary: Iteratively reweighted averaging for the geometric median. Each step lowers the sum of distances; a data point needs the Kuhn or Vardi-Zhang step to keep the iteration defined.
solves: [geometric-median]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, k: the number of iterations}
  time: {worst: O(k n d)}
  space: {extra: O(d)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1937
  people: [Endre Weiszfeld]
  note: "Weiszfeld gave the iteration in 1937. Kuhn proved convergence in 1973 under conditions, and Vardi and Zhang gave in 2000 a step at data points that makes it converge from every start."
prereqs: [geometric-median, euclidean-distance, convex-function, gradient-descent]
see_also: [fermat-point, facility-location-problem, k-median-problem, fixed-point-iteration, subgradient, second-order-cone-programming, weighted-median, lloyds-algorithm]
sources:
  - paper: "Endre Weiszfeld, Sur le point pour lequel la somme des distances de n points donnés est minimum, Tôhoku Mathematical Journal 43, 1937"
    locator: the iteration and the original convergence argument
  - paper: doi:10.1007/BF01584648
    title: Harold W. Kuhn, A note on Fermat's problem, Mathematical Programming 4, 1973
    locator: the optimality test at a data point, the descent step from a data point, and the convergence theorem
  - paper: "I. Norman Katz, Local convergence in Fermat's problem, Mathematical Programming 6, 1974"
    locator: the local rate of convergence, linear when the median is not a data point, and the cases at a data point
  - paper: doi:10.1007/BF01587094
    title: Ramaswamy Chandrasekaran and Arie Tamir, Open questions concerning Weiszfeld's algorithm for the Fermat-Weber location problem, Mathematical Programming 44, 1989
    locator: the counterexample to Kuhn's claim on the set of bad starting points, and the open conjecture
  - paper: doi:10.1073/pnas.97.4.1423
    title: Yehuda Vardi and Cun-Hui Zhang, The multivariate L1-median and associated data depth, Proceedings of the National Academy of Sciences 97(4), 2000
    locator: the modified iteration that converges from every starting point
  - paper: doi:10.1007/s10957-014-0586-7
    title: Amir Beck and Shoham Sabach, Weiszfeld's method, old and new results, Journal of Optimization Theory and Applications 164(1), 2015
    locator: the survey of convergence results, the non-asymptotic sublinear rate, and the counterexample of Chandrasekaran and Tamir in three dimensions
---

Weiszfeld's algorithm computes the [geometric median](/geometric-median/) of $n$ points in $\mathbb{R}^d$, the point $x$ that minimizes $\sum_i w_i |x - a_i|$. Each step replaces the current point $y$ by the average of the data points with weights $w_i / |y - a_i|$, so near points count more. Each step costs $O(nd)$ time and never increases the cost. The plain step is undefined when $y$ is a data point, which is the weak spot of the method: Kuhn (1973) gave a test and a descent step for that case, and Vardi and Zhang (2000) combined them into one map that converges to the median from every starting point.

## In plain words

You want one meeting point for a group of people, so that the total walking distance is as small as possible. Start with a guess, for example the average position.

Now ask each person how far they are from the guess. Take a new average, but let near people count more and far people count less: each person counts in proportion to one over their distance. Move the guess there and repeat.

Each move makes the total distance smaller, and the guesses close in on the best meeting point. One case needs care. If the guess lands exactly on a person, that person's distance is zero, and "one over the distance" makes no sense. Then a separate test decides whether that person's spot is already the answer. If it is not, a separate rule moves the guess off the spot in the best direction.

## The problem

Notation: the data points are $a_1, \ldots, a_n \in \mathbb{R}^d$ with weights $w_i > 0$; copies of one point are merged and their weights added. The cost is $f(x) = \sum_i w_i |x - a_i|$ with the [Euclidean distance](/euclidean-distance/). For a point $y$, write $\delta_i = |y - a_i|$, and over the indices with $\delta_i > 0$,

$$S(y) = \sum \frac{w_i}{\delta_i}, \qquad \tilde T(y) = \frac{1}{S(y)} \sum \frac{w_i}{\delta_i}\, a_i, \qquad R(y) = \sum w_i \frac{a_i - y}{\delta_i}, \qquad r = |R(y)|,$$

and $\eta(y) = w_k$ if $y = a_k$, else $\eta(y) = 0$. Away from the data points, $f$ is differentiable with $\nabla f(y) = -R(y)$, and $\tilde T(y) - y = R(y)/S(y)$. So the plain step $y \mapsto \tilde T(y)$ is a [gradient descent](/gradient-descent/) step with step length $1/S(y)$.

The input is the points, the weights, a start $y_0$ and a tolerance. The output is an approximation of a minimizer of $f$. No general position is assumed. If the points lie on a line, $f$ can have a segment of minimizers, and the iteration finds one of them.

## The algorithm

The form below is the map of Vardi and Zhang. When $y$ is not a data point, $\eta = 0$ and line L9 is the plain Weiszfeld step $y' = T/S$. When $y = a_k$, line L8 is Kuhn's test, and line L9 is Kuhn's step from $a_k$.

```pseudo id=main
WEISZFELD(a[1..n], w[1..n], y0, tol, K)
L1  y ← y0
L2  repeat at most K times
L3      S ← 0;  T ← 0;  R ← 0;  η ← 0         ▷ T and R are vectors in R^d
L4      for i ← 1 to n do
L5          if a_i = y then η ← η + w_i; continue with the next i
L6          δ ← |a_i − y|;  S ← S + w_i/δ;  T ← T + (w_i/δ) a_i;  R ← R + (w_i/δ)(a_i − y)
L7      r ← |R|
L8      if r ≤ η then return y                 ▷ y is a geometric median
L9      λ ← η / r;  y' ← (1 − λ) T/S + λ y
L10     step ← |y' − y|;  y ← y'
L11     if step ≤ tol · (1 + |y|) then return y
L12 return y
```

Line L8 covers two cases. If $y$ is not a data point, $\eta = 0$, and $r \le 0$ means $\nabla f(y) = 0$. If $y = a_k$, the test $|R(a_k)| \le w_k$ is exactly the condition for $a_k$ to be a minimizer. In both cases $y$ is optimal. Line L11 is a stopping rule, not a proof of accuracy; the section on correctness gives a certificate.

A default start is the weighted centroid. Every later iterate is a weighted average of the data points and of the previous iterate, so all iterates from $y_1$ on lie in the [convex hull](/convex-hull/) of the data points.

## Example

Take the pentagon $(0, 0), (4, 0), (5, 3), (3, 5), (0, 4)$ with unit weights. It is symmetric in the line $x = y$, so the median lies on that line, and so do all iterates from the centroid $(12/5, 12/5)$.

| step | $y_k$ (both coordinates) | $f(y_k)$ |
|---|---|---|
| 0 | 2.40000 | 14.499660 |
| 1 | 2.52362 | 14.460020 |
| 2 | 2.58372 | 14.450548 |
| 3 | 2.61309 | 14.448272 |
| 4 | 2.62749 | 14.447723 |
| 5 | 2.63455 | 14.447591 |
| 6 | 2.63802 | 14.447559 |
| limit | 2.64137 | 14.447549 |

The distance to the limit is 0.24137, 0.11775, 0.05765, 0.02828, 0.01388, 0.00682, 0.00335: it about halves at each step, a linear rate. No vertex passes Kuhn's test, so the median is not a data point.

**A start at a data point.** For the square $(0, 0), (4, 0), (4, 4), (0, 4)$ and $y_0 = (0, 0)$, the plain step divides by zero. In the loop, $\eta = 1$ and $R = (1, 0) + (0, 1) + (1, 1)/\sqrt{2}$, so $r = 1 + \sqrt{2} \approx 2.414 > 1$, and $(0, 0)$ is not the median. Line L9 gives $y_1 \approx (1.47759, 1.47759)$ with cost $11.5035$, down from $8 + 4\sqrt{2} \approx 13.6569$, and the iterates go on to the center $(2, 2)$.

## Correctness

Three facts carry the proof; the full argument is below.

**Optimality.** $f$ is a [convex function](/convex-function/). At a point $y$ that is not a data point it is differentiable, so $y$ is a minimizer iff $R(y) = 0$, iff $\tilde T(y) = y$. At $a_k$ the one-sided derivative in a unit direction $v$ is $w_k - \langle R(a_k), v \rangle$, with smallest value $w_k - |R(a_k)|$, so $a_k$ is a minimizer iff $|R(a_k)| \le w_k$. This is Kuhn's test of line L8.

**Descent.** For $\delta > 0$, $|z - a| \le |z - a|^2/(2\delta) + \delta/2$, with equality when $|z - a| = \delta$. With $\delta = \delta_i$ this bounds $f$ from above by a quadratic $g$ that touches $f$ at $y$, and $\tilde T(y)$ is the minimizer of $g$. So $f(\tilde T(y)) \le f(y) - \frac{1}{2} S(y)\, |\tilde T(y) - y|^2$. At a data point that fails the test, the step of line L9 lowers $f$ by at least $(r - \eta)^2 / (2 S(y))$.

**No sticking at a wrong data point.** If $a_k$ fails Kuhn's test, then for $y$ close to $a_k$ the plain step moves away: $|\tilde T(y) - a_k| / |y - a_k| \to |R(a_k)| / w_k > 1$ as $y \to a_k$.

From these, the cost $f(y_k)$ converges to the minimum from every start. If the points are not all on one line, $f$ is strictly convex, the median $x^*$ is unique, and $y_k \to x^*$.

**A certificate.** Every iterate after the first lies in the convex hull of the data points, and so does $x^*$. If $D$ is the diameter of the points and $y$ is not a data point, convexity gives $f(y) - f(x^*) \le |\nabla f(y)|\, D = |R(y)|\, D$, a bound that can be computed. When the iterates approach a data point, Kuhn's test at the nearest data point gives the exact answer instead.

## Complexity

- **One step:** lines L3 to L11 take $\Theta(nd)$ arithmetic operations and $n$ square roots.
- **$k$ steps:** $O(knd)$ time and $O(d)$ extra space besides the input.
- **Rate when the median is not a data point:** linear (Katz 1974), with a ratio that depends on the input; it was about 0.49 in the example.
- **Rate when the median is a data point $a_k$:** near $a_k$ the plain step gives $\tilde T(y) - a_k \approx (|y - a_k| / w_k)\, R(a_k)$, so the distance to $a_k$ shrinks by a factor that tends to $|R(a_k)| / w_k$. For the triangle $(0, 0), (4, 0), (-1, 1)$ the median is $(0, 0)$, $|R| \approx 0.7654$, and the distance drops from about $9.2 \cdot 10^{-4}$ after 21 steps to about $3.0 \cdot 10^{-7}$ after 51 steps, a factor of $0.7654^{30}$. When $|R(a_k)| = w_k$ the rate is sublinear, and the iteration never lands on $a_k$ exactly.
- **Global bound:** Beck and Sabach prove a sublinear bound on $f(y_k) - f(x^*)$ that holds from the first step. No bound of the form $O(\log(1/\varepsilon))$ steps holds for all inputs.

## Properties

- **Monotone.** $f(y_{k+1}) < f(y_k)$ until a minimizer is reached.
- **Stays in the hull.** From $y_1$ on, every iterate lies in the convex hull of the data points.
- **Affine behavior.** The map commutes with rotations, translations and uniform scaling of the input, so the iterates do too.
- **Deterministic and numerical.** The iterates are irrational in general, and the median itself can need roots of high degree, so floats are the normal arithmetic. Only Kuhn's test compares exact quantities, $|R|^2$ against $w_k^2$, and with floats it carries rounding error.
- **Any dimension.** Nothing in the method depends on $d$ beyond the $O(d)$ cost of a vector operation.

## Variants and improvements

- **Kuhn's step.** Kuhn (1973) proposed to test each data point that an iterate reaches and to step away along $R(a_k)$ if the test fails. The Vardi-Zhang map of line L9 is the same step, written as one formula for all $y$.
- **Snapping.** When the steps become small, test the nearest data point with Kuhn's test, and return it if it passes. This removes the slow approach to a data-point median.
- **Over-relaxation.** Steps $y + \lambda (\tilde T(y) - y)$ with $\lambda \in (1, 2)$ are often faster and keep the descent for suitable $\lambda$.
- **Smoothing.** Replace $|x - a_i|$ by $\sqrt{|x - a_i|^2 + \varepsilon^2}$. The iteration is then always defined, and Beck and Sabach analyze an accelerated method of this kind.
- **Other solvers.** The problem is a [second-order cone program](/second-order-cone-programming/), so interior-point methods reach accuracy $\varepsilon$ in time polynomial in $n$, $d$ and $\log(1/\varepsilon)$. Cohen, Lee, Miller, Pachocki and Sidford (2016) give nearly linear time. See [geometric median](/geometric-median/).
- **Clustering.** The $k$-median heuristic of [Lloyd type](/lloyds-algorithm/) uses a Weiszfeld step as its center update.

## When to use it

Use Weiszfeld's algorithm for the geometric median of a few hundred to millions of points when moderate accuracy is enough. Each step is one pass over the data, and the code fits in a dozen lines. For high accuracy on hard inputs, or when the median sits on or near a data point with $|R| \approx w_k$, use snapping, a smoothed and accelerated variant, or a cone-programming solver. For points on a line use the [weighted median](/weighted-median/), which is exact and takes linear time.

## Pitfalls

- **Division by zero.** The plain step fails when an iterate equals a data point. Starting at a data point, a common default, triggers it at once. Use lines L5, L8 and L9.
- **Dropping the zero term.** Some code skips the term with $\delta_i = 0$ and takes the plain step $\tilde T(a_k)$. That step is not a descent step in general, and when $a_k$ is the median it moves the iterate away from the answer. Use Kuhn's test first.
- **Stopping on a small step.** A small step does not mean a small error, since a slow linear rate gives small steps far from the optimum. Use the certificate $|R(y)|\,D$, or Kuhn's test at the nearest data point.
- **Collinear input.** The minimizer need not be unique. All points of the middle segment are optimal, and the iterate stops at one of them.
- **Duplicates.** Copies of a point must add their weights in $\eta$, as line L5 does. Testing only one copy against $|R|$ gives a wrong answer for Kuhn's test.

## Implementations

## History

Endre Weiszfeld published the iteration in 1937, in a French paper in the Tôhoku Mathematical Journal, while a student in Budapest; he later worked in operations research in the United States as Andrew Vázsonyi. His convergence argument missed the data-point case. Kuhn and Kuenne rediscovered the method in 1962 for location problems, and Kuhn's 1973 note gave the optimality test at data points, the descent step from them, and a convergence proof. Kuhn also claimed that only countably many starting points lead to a data point; Chandrasekaran and Tamir (1989) found counterexamples when the data points lie in a proper affine subspace, and the general question was argued over in later papers. Vardi and Zhang (2000) wrote Kuhn's step into the map itself, which gives convergence from every start, in a paper on the multivariate L1-median in statistics.

## References
