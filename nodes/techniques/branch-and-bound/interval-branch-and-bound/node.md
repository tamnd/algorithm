---
tag: AGSJXC
kind: algorithm
slug: interval-branch-and-bound
name: Interval branch and bound
aliases:
- interval-arithmetic branch and bound
- Moore branch and bound
area: techniques/branch-and-bound
level: advanced
summary: Global optimisation by bisecting boxes and bounding the objective with interval arithmetic.
solves: [global-optimization]
model: real-ram
complexity:
  vars: {N: the number of boxes made, C: the time to evaluate the interval extension once, d: the dimension}
  time: {worst: O(N (C + d + log N))}
  space: {extra: O(N d)}
properties: {deterministic: true, recursive: false}
prereqs: [interval-arithmetic, best-first-branch-and-bound, bounding-function]
see_also: [interval-arithmetic, global-optimization, interval-newton-method, bisection-method, lipschitz-condition, best-first-branch-and-bound, branching-rule, fathoming-rule]
sources:
  - book: isbn:9780898716696
    title: Ramon E. Moore, R. Baker Kearfott and Michael J. Cloud, Introduction to Interval Analysis
    locator: Chapters on interval extensions of functions and on global optimization
  - paper: doi:10.1007/BF01933121
    title: S. Skelboe, Computation of rational interval functions, BIT 14(1), 1974
    locator: pp. 87 to 95
  - paper: doi:10.1007/BF00933139
    title: Eldon Hansen, Global optimization using interval analysis, the one-dimensional case, Journal of Optimization Theory and Applications 29(3), 1979
    locator: pp. 331 to 344
  - paper: doi:10.1007/BF01396702
    title: Eldon Hansen, Global optimization using interval analysis, the multi-dimensional case, Numerische Mathematik 34(3), 1980
    locator: pp. 247 to 270
  - book: isbn:9780824740597
    title: Eldon Hansen and G. William Walster, Global Optimization Using Interval Analysis, second edition
    locator: Chapters on unconstrained and constrained global optimization
---

Interval branch and bound finds the global minimum of a function over a box in $\mathbb{R}^d$ with a guarantee. It evaluates the function in [interval arithmetic](/interval-arithmetic/) on a box, which gives an interval that contains every value of the function on the box; the lower end of that interval is a [bound](/bounding-function/). Values at sample points give an upper bound on the minimum. Boxes whose lower bound is above the best value found are discarded, and the others are cut in half until they are small. The result is an interval that contains the global minimum and a list of small boxes that contain every global minimizer. Skelboe (1974) and Hansen (1979, 1980) gave the method its standard form.

## In plain words

You want the lowest point of a landscape inside a fenced area, and you must be sure that you did not miss it. A special calculator takes a whole region and tells you a height that no point in the region is below. Plain sampling cannot give such a promise.

Keep a list of regions. Take the region with the lowest promise, cut it in two, and ask the calculator about each half. Also measure the real height at the center of each half; the lowest height you measured is a point you know. A region whose promise is above that height cannot hold the lowest point, so drop it. Stop cutting a region when it is small enough. The small regions that are left hold the lowest point.

## The problem

Given a box $X = [a_1, b_1] \times \cdots \times [a_d, b_d]$ and a function $f : X \to \mathbb{R}$ that attains its minimum $f^* = \min_{x \in X} f(x)$, find an interval $[\underline{f}, \overline{f}] \ni f^*$ and a set of boxes of width at most $\varepsilon$ whose union contains every global minimizer. The method needs an *inclusion function* $F$: for every box $Y \subseteq X$, $F(Y)$ is an interval with $f(Y) \subseteq F(Y)$. The *natural interval extension*, which evaluates a formula for $f$ in interval arithmetic, is one; by the fundamental theorem of interval arithmetic it contains the range of $f$ on $Y$. The width $w(Y)$ of a box is the length of its longest side.

## The algorithm

Write $\underline{F}(Y)$ for the lower end of $F(Y)$ and $\mathrm{mid}(Y)$ for the center of $Y$.

```pseudo id=main
INTERVAL-BB(f, F, X, ε)
L1  x̄ ← mid(X); f̄ ← f(x̄); insert (F̲(X), X) into a min-priority queue H; R ← ∅
L2  while H is not empty do
L3      (β, Y) ← EXTRACT-MIN(H)                        ▷ the box with the least lower bound
L4      if β > f̄ then break                            ▷ no box left holds a global minimizer
L5      if w(Y) ≤ ε then R ← R ∪ {(β, Y)}; continue     ▷ small enough: keep for the answer
L6      cut Y at the midpoint of a longest side into Y₁ and Y₂
L7      for Z in (Y₁, Y₂) do
L8          if f(mid(Z)) < f̄ then f̄ ← f(mid(Z)); x̄ ← mid(Z)   ▷ a better known value
L9          if F̲(Z) ≤ f̄ then insert (F̲(Z), Z) into H         ▷ else Z is discarded
L10 R ← {(β, Y) ∈ R : β ≤ f̄}; return (min of β over R, f̄, x̄, R)
```

The box with the least lower bound is taken first, as in [best-first branch and bound](/best-first-branch-and-bound/). This order is due to Skelboe. Line L8 is the *midpoint test*: the value at a real point is an upper bound on $f^*$, and it is used at line L9 to discard boxes. The longest side is cut first, which keeps boxes from growing long and thin.

## Example

Minimize $f(x) = (x^2 - 2)^2 + x - 4$ over $X = [-3, 3]$ with $\varepsilon = \frac{1}{2}$, with $F$ the natural interval extension of this formula. For example, on $[-3, 0]$, $x^2 \in [0, 9]$, $x^2 - 2 \in [-2, 7]$, $(x^2 - 2)^2 \in [0, 49]$, and $F([-3, 0]) = [0, 49] + [-3, 0] - 4 = [-7, 45]$. At the start, $\overline{f} = f(0) = 0$.

| step | box taken | lower bound | children: lower bound | $\overline{f}$ after |
|---|---|---|---|---|
| 1 | $[-3, 3]$ | $-7$ | $[-3, 0]$: $-7$; $[0, 3]$: $-4$, discarded | $f(-\frac{3}{2}) = -\frac{87}{16}$ |
| 2 | $[-3, 0]$ | $-7$ | $[-3, -\frac{3}{2}]$: $-\frac{111}{16}$; $[-\frac{3}{2}, 0]$: $-\frac{11}{2}$ | $-\frac{87}{16}$ |
| 3 | $[-3, -\frac{3}{2}]$ | $-\frac{111}{16}$ | $[-3, -\frac{9}{4}]$: $\frac{609}{256}$, discarded; $[-\frac{9}{4}, -\frac{3}{2}]$: $-\frac{99}{16}$ | $-\frac{87}{16}$ |
| 4 | $[-\frac{9}{4}, -\frac{3}{2}]$ | $-\frac{99}{16}$ | $[-\frac{9}{4}, -\frac{15}{8}]$: about $-3.95$, discarded; $[-\frac{15}{8}, -\frac{3}{2}]$: $-\frac{93}{16}$ | $-\frac{87}{16}$ |
| 5 | $[-\frac{15}{8}, -\frac{3}{2}]$ | $-\frac{93}{16}$ | width $\frac{3}{8}$: kept in $R$ | |
| 6 | $[-\frac{3}{2}, 0]$ | $-\frac{11}{2}$ | $[-\frac{3}{2}, -\frac{3}{4}]$: $-\frac{11}{2}$; $[-\frac{3}{4}, 0]$: about $-2.68$, discarded | $-\frac{87}{16}$ |
| 7 | $[-\frac{3}{2}, -\frac{3}{4}]$ | $-\frac{11}{2}$ | $[-\frac{3}{2}, -\frac{9}{8}]$: $-\frac{11}{2}$; $[-\frac{9}{8}, -\frac{3}{4}]$: about $-4.59$, discarded | $-\frac{87}{16}$ |
| 8 | $[-\frac{3}{2}, -\frac{9}{8}]$ | $-\frac{11}{2}$ | width $\frac{3}{8}$: kept in $R$ | |

The result is $f^* \in [-\frac{93}{16}, -\frac{87}{16}] = [-5.8125, -5.4375]$, and every global minimizer lies in $[-\frac{15}{8}, -\frac{9}{8}]$, after 8 boxes and 6 cuts. The true minimum is about $-5.4442$ at $x \approx -1.4730$. The local minimum near $x \approx 1.35$, with value about $-2.62$, was discarded at step 1. With $\varepsilon = 2^{-10}$, the enclosure has width less than $10^{-3}$.

## Correctness

If a box $Y$ contains a global minimizer $x^*$, then $\underline{F}(Y) \le f(x^*) = f^*$. Every value $\overline{f}$ is the value of $f$ at a point of $X$, so $f^* \le \overline{f}$. So a box with $\underline{F}(Y) > \overline{f}$ contains no global minimizer, and the boxes discarded at line L4, line L9 and line L10 lose none. The two halves of a box cover it. So at every step, every global minimizer is in a box of $H$ or of $R$. When the loop ends, the boxes still in $H$ have bounds above $\overline{f}$, so every global minimizer is in a box of $R$, and $\min_R \beta \le f^* \le \overline{f}$. The loop ends because a box of width $w$ is cut at most $d \lceil \log_2 (w(X)/\varepsilon) \rceil$ times along a path, and every cut makes two boxes. The [proof](proofs/correctness.md) gives the details.

## Complexity

Each box costs one evaluation of $F$ and one of $f$, $O(d)$ to cut and copy, and $O(\log N)$ for the queue, which gives $O(N (C + d + \log N))$. The boxes in $H$ and $R$ take $O(N d)$ memory. A box is cut along a path at most $d \lceil \log_2 (w(X)/\varepsilon) \rceil$ times, so $N \le 2^{d \lceil \log_2(w(X)/\varepsilon) \rceil + 1}$, which is $O((2 w(X)/\varepsilon)^d)$. This worst case happens, for example, for a constant function, where no box is ever discarded. Global optimization of a general function is hard, and the number of boxes depends on how flat $f$ is near its minimizers and on how much $F$ overestimates the range.

For the natural interval extension of a formula, the overestimation on a small box is at most a constant times the width of the box, under mild conditions on the formula (Moore, Kearfott and Cloud). So the gap between $\min_R \beta$ and $f^*$ shrinks as $\varepsilon$ shrinks.

## Properties

- **Guaranteed.** With exact or outward-rounded arithmetic, the result is a proof: $f^*$ lies in the returned interval and every global minimizer lies in a returned box.
- **No derivatives needed.** The basic method needs only $f$ and an inclusion function, which can be computed from a formula automatically.
- **All minimizers.** It does not return one minimizer but a cover of all of them, so it finds several global minimizers when they exist.
- **Depends on the formula.** Two formulas for the same $f$ can give very different inclusion functions.

## Variants and improvements

- **Monotonicity test.** Hansen evaluates an inclusion of the gradient on a box. If $\partial f / \partial x_i$ does not contain 0 on a box in the interior of $X$, the box holds no minimizer and is discarded; on the border of $X$ it is reduced to a face.
- **Interval Newton steps.** An [interval Newton method](/interval-newton-method/) on the gradient can shrink a box around a stationary point or prove that it has none.
- **Concavity test.** A box on which the Hessian cannot be positive semidefinite holds no interior minimizer.
- **Better inclusion functions.** Centered forms and mean value forms use the gradient and are tighter than the natural extension on small boxes.
- **Constraints.** Boxes that are certainly infeasible are discarded, and boxes that are certainly feasible give upper bounds; Hansen and Walster treat constrained problems in this way.

## When to use it

Use interval branch and bound when a global minimum must be certain, such as in proofs by computer, safety checks and rigorous bounds, and when the dimension is small. For problems with many variables, or when an approximate answer is enough, local methods with many starts or other [global optimization](/global-optimization/) methods are faster.

## Pitfalls

- **Rounding.** With floating point, the ends of each interval must be rounded outward, down for the lower end and up for the upper end. Rounding to nearest can lose the guarantee. The code here uses exact rational numbers instead.
- **The dependency problem.** Each occurrence of a variable is treated as independent. Written as $x^4 - 4x^2 + x$, the same function of the example gives the root bound $-39$ instead of $-7$, and with $\varepsilon = \frac{1}{2}$ the search makes 20 boxes, keeps 7 and returns the lower bound $-\frac{87}{8} = -10.875$ instead of $-5.8125$.
- **Too small an $\varepsilon$.** Near a flat minimum, many boxes have bounds below $\overline{f}$, and their number grows like $\varepsilon^{-d}$.
- **Points outside the domain.** The inclusion function must be defined on all of $X$; a function such as $\sqrt{x}$ or $1/x$ needs care at the ends.

## Implementations

## History

Moore developed interval analysis and its use to bound the range of a function. Skelboe (1974) computed the range of rational functions by repeated bisection, always cutting the box with the least lower bound. Hansen (1979) gave a global optimization method for one dimension with interval arithmetic, and Hansen (1980) extended it to several dimensions, with tests that use the gradient and Newton steps. Hansen and Walster wrote a book on the subject.

## References
