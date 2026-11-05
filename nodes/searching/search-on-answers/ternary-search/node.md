---
tag: R8SB5Q
kind: algorithm
slug: ternary-search
name: Ternary search
aliases:
- ternary search on integers
- three-point search
- trinary search
area: searching/search-on-answers
level: intro
summary: Shrink an interval to a third at each step by comparing two interior points of a unimodal function.
solves: [unimodal-optimization]
model: query-model
complexity:
  vars: {n: "the number of integer candidates, or (b − a)/ε for a real interval of length b − a and tolerance ε"}
  time: {worst: Θ(log n), average: Θ(log n), best: Θ(log n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: true, recursive: false}
prereqs: [unimodal-function, binary-search, loop-invariant]
see_also: [unimodal-optimization, golden-section-search, fibonacci-search-unimodal, binary-search-on-real-numbers, unimodal-maximum, peak-finding, convex-function, quasiconvex-function]
sources:
  - book: isbn:9783319725468
    title: Antti Laaksonen, Guide to Competitive Programming, first edition, Springer, 2017
    locator: Section 8.3.1, Ternary Search
  - url: https://cp-algorithms.com/num_methods/ternary_search.html
    title: cp-algorithms, Ternary Search
  - paper: doi:10.1090/S0002-9939-1953-0055639-3
    title: "J. Kiefer, Sequential minimax search for a maximum, Proceedings of the American Mathematical Society 4(3) (1953), 502-506"
    note: the optimal method that ternary search approximates
---

Ternary search finds the maximum of a [unimodal function](/unimodal-function/) on an interval by evaluating it at two inner points, at one third and two thirds of the interval, and discarding the third that cannot hold the maximum. Each step keeps two thirds of the interval, so $\lceil \log_{3/2} n \rceil$ steps reduce $n$ integer candidates to one, and $\log_{3/2}((b - a)/\varepsilon)$ steps reduce a real interval to length $\varepsilon$. It solves [unimodal optimization](/unimodal-optimization/) with no derivative and almost no code. It uses about 2.4 times as many evaluations as [golden-section search](/golden-section-search/), because it throws away both inner values at each step.

## In plain words

A road goes up a hill and then down, and you want the top. You cannot see the road, but you can ask for the height at any place. Pick two places, one a third of the way along and one two thirds of the way along. If the first place is lower than the second, the top cannot be before the first place, because the road only goes up until the top. So you drop the first third. Otherwise you drop the last third. Then you do the same with the part that is left. Each round the part that is left gets smaller by a third, and after a few dozen rounds it is so small that any place in it is as good as the top.

## The problem

The input is a function $f$ on an interval $[a, b]$ of reals, or on the integers $\{a, \ldots, b\}$, that is **strictly unimodal for a maximum**: there is a mode $m$ such that $f$ is strictly increasing on the points $\le m$ and strictly decreasing on the points $\ge m$. The function is given as an oracle: the algorithm learns about $f$ only by asking for $f(x)$, and its cost is the number of such evaluations, as in the [query model](/query-model/). The output is $m$ on the integers, or a point within $\varepsilon$ of $m$ on a real interval. For a minimum, reverse the comparison. This is the problem of [unimodal optimization](/unimodal-optimization/).

The method rests on the comparison lemma for unimodal functions. For $x_1 < x_2$:

- $f(x_1) < f(x_2)$ implies $m > x_1$;
- $f(x_1) > f(x_2)$ implies $m < x_2$;
- $f(x_1) = f(x_2)$ implies $x_1 < m < x_2$.

*Proof.* If $m \le x_1$, then $f$ is strictly decreasing on $[m, \infty)$, which holds $x_1 < x_2$, so $f(x_1) > f(x_2)$; this proves the first item by contraposition. The second item is the mirror image. If $f(x_1) = f(x_2)$, the first two arguments show that $m \le x_1$ and $m \ge x_2$ are both impossible. $\square$

## The algorithm

TERNARY-MAX works on a real interval for a fixed number of steps. TERNARY-INT works on integers and stops when one candidate is left.

```pseudo id=main
TERNARY-MAX(f, lo, hi, steps)            ▷ f strictly unimodal on [lo, hi]
L1  for s ← 1 to steps do
L2      m1 ← lo + (hi − lo) / 3
L3      m2 ← hi − (hi − lo) / 3
L4      if f(m1) < f(m2) then lo ← m1      ▷ the mode is right of m1
L5      else hi ← m2                     ▷ the mode is left of m2
L6  return lo + (hi − lo) / 2

TERNARY-INT(f, lo, hi)                   ▷ integers lo ≤ hi, f strictly unimodal on them
L7  while lo < hi do
L8      d ← ⌊(hi − lo) / 3⌋
L9      m1 ← lo + d;  m2 ← hi − d          ▷ lo ≤ m1 < m2 ≤ hi
L10     if f(m1) < f(m2) then lo ← m1 + 1
L11     else hi ← m2 − 1
L12 return lo
```

In TERNARY-INT, $d$ can be $0$ when two or three candidates are left. Then $m_1 = lo$ and $m_2 = hi$ are still distinct, and the step removes one end.

## Example

**Integers.** Take the 12 values $f = (2, 5, 9, 14, 20, 23, 21, 18, 11, 8, 4, 1)$ at the indices $0$ to $11$. The mode is index $5$. TERNARY-INT$(f, 0, 11)$ runs:

| lo | hi | d | m1 | m2 | f(m1) | f(m2) | action |
|---|---|---|---|---|---|---|---|
| 0 | 11 | 3 | 3 | 8 | 14 | 11 | hi ← 7 |
| 0 | 7 | 2 | 2 | 5 | 9 | 23 | lo ← 3 |
| 3 | 7 | 1 | 4 | 6 | 20 | 21 | lo ← 5 |
| 5 | 7 | 0 | 5 | 7 | 23 | 18 | hi ← 6 |
| 5 | 6 | 0 | 5 | 6 | 23 | 21 | hi ← 5 |

It returns $5$ after 5 iterations and 10 evaluations. The bound below allows $\lceil \log_{3/2} 12 \rceil = 7$ iterations. On the same values, [Fibonacci search](/fibonacci-search-unimodal/) needs 5 evaluations, because it reuses one inner value at each step.

**Reals.** Take $f(x) = -(x - 2)^2$ on $[0, 5]$, with the mode $2$. The first four steps of TERNARY-MAX are:

| step | lo | hi | m1 | m2 | action |
|---|---|---|---|---|---|
| 1 | 0 | 5 | 1.6667 | 3.3333 | $f(m_1) > f(m_2)$, hi ← 3.3333 |
| 2 | 0 | 3.3333 | 1.1111 | 2.2222 | $f(m_1) < f(m_2)$, lo ← 1.1111 |
| 3 | 1.1111 | 3.3333 | 1.8519 | 2.5926 | $f(m_1) > f(m_2)$, hi ← 2.5926 |
| 4 | 1.1111 | 2.5926 | 1.6049 | 2.0988 | $f(m_1) < f(m_2)$, lo ← 1.6049 |

After four steps the interval is $[1.6049, 2.5926]$, of length $5 \cdot (2/3)^4 \approx 0.988$, and it holds $2$. After 60 steps the length is $5 \cdot (2/3)^{60} \approx 1.4 \times 10^{-10}$.

## Correctness

The invariant of both loops is that the mode lies in the current range: $m \in [lo, hi]$. It holds at the start. In line L4, $f(m_1) < f(m_2)$ gives $m > m_1$ by the comparison lemma, so $m \in [m_1, hi]$. In line L5, $f(m_1) \ge f(m_2)$ gives $m < m_2$, either by the second item or by the third, so $m \in [lo, m_2]$. TERNARY-INT uses the same argument with integers: $m > m_1$ means $m \ge m_1 + 1$, and $m < m_2$ means $m \le m_2 - 1$. When TERNARY-INT stops, $lo = hi$, so $lo = m$. The real version keeps $m$ in an interval of length $(2/3)^{steps}(b - a)$ and returns its midpoint. The full proof, with the count of iterations, is below.

## Complexity

- **Real version.** Each step multiplies the length by exactly $2/3$ and makes 2 evaluations. To reach length $\varepsilon$ from $b - a$ it needs $\lceil \log_{3/2}((b - a)/\varepsilon) \rceil \approx 1.71 \lg((b - a)/\varepsilon)$ steps, so about $3.42 \lg((b - a)/\varepsilon)$ evaluations.
- **Integer version.** One iteration takes $s$ candidates to at most $\lceil 2(s - 1)/3 \rceil \le 2s/3$. So it makes at most $\lceil \log_{3/2} n \rceil$ iterations and $2 \lceil \log_{3/2} n \rceil$ evaluations for $n \ge 2$ candidates.
- **Space.** $O(1)$ besides the evaluations.

**Comparison with the optimum.** Golden-section search shrinks the interval by $1/\varphi \approx 0.618$ per evaluation, so it needs about $\log_\varphi r \approx 1.44 \lg r$ evaluations for a reduction by $r$. Ternary search shrinks by $\sqrt{2/3} \approx 0.816$ per evaluation, so it needs $\ln \varphi / \ln \sqrt{3/2} \approx 2.37$ times as many. [Fibonacci search](/fibonacci-search-unimodal/) is optimal among all methods with a fixed number of evaluations, by Kiefer's theorem on the page [unimodal optimization](/unimodal-optimization/). The time is still $\Theta(\log n)$ evaluations in every case; the difference is in the constant.

## Properties

- **Only comparisons of values.** The method uses the order of $f(m_1)$ and $f(m_2)$, never their size, so it works for any $f$ with values in an ordered set and is not affected by a monotone change of $f$.
- **No reuse.** Both inner points are new at each step. Golden-section and Fibonacci search place the points so that one of them is reused.
- **Same work on each input.** The real version always makes $2 \cdot steps$ evaluations. The integer version makes between about $2 \log_3 n$ and $2 \log_{3/2} n$ evaluations, depending on which branch is taken.
- **Not robust to plateaus.** Strictness is used in the third item of the comparison lemma; see the pitfalls.

## Variants and improvements

- **Minimum.** Use $f(m_1) > f(m_2)$ in lines L4 and L10. A strictly [convex function](/convex-function/) is strictly unimodal for a minimum, so the method finds its minimum; this is the common use, for example the minimum of a sum of convex costs.
- **Binary search on the slope.** On integers, the predicate "$f(x) > f(x + 1)$" is false before the mode and true from the mode on. A [binary search](/binary-search/) for its first true value finds $m$ with $2 \lceil \lg n \rceil$ evaluations, fewer than ternary search. On a real interval, the analogous dichotomous search compares $f(c - \delta)$ and $f(c + \delta)$ at the center $c$, and keeps a bit more than half per pair of evaluations. On an array this is the [unimodal maximum](/unimodal-maximum/) search.
- **Golden-section search.** Put the inner points at the ratios $0.382$ and $0.618$. Then the kept inner point is one of the next two, and each step needs one new evaluation. See [golden-section search](/golden-section-search/).
- **Fibonacci search.** For a known number of evaluations on integers, place the points at Fibonacci numbers. This is optimal. See [Fibonacci search](/fibonacci-search-unimodal/).
- **Brent's method.** For a smooth $f$, mix golden-section steps with parabolic interpolation through three points, which converges much faster near a smooth maximum; see [Brent's method](/brent-method/).
- **Small ranges.** Stop TERNARY-INT when a few candidates are left and evaluate them all. This avoids the slow last iterations, where $d = 0$ and one candidate goes per two evaluations.

## When to use it

Use ternary search when the function is cheap to evaluate, the code must be short, and the unimodality is easy to prove, as in contest problems: the minimum of a convex cost over a real parameter, or a nested search where the inner function is the maximum of a unimodal function of a second variable. When each evaluation is expensive, use golden-section search, or Fibonacci search on integers. When the function is a sorted-then-reversed array, use the binary search on the slope. When the function is smooth and its derivative is known, a root-finding method on the derivative converges faster.

## Pitfalls

- **Plateaus.** On $f = (1, 2, 2, 2, 2, 2, 3, 1)$, which rises to the mode $6$ with a flat part, TERNARY-INT$(f, 0, 7)$ compares $f(2) = 2$ with $f(5) = 2$, takes line L11 and sets $hi \leftarrow 4$, which loses the mode. The method is correct when equal values occur only on the set of maxima, for example for a concave $f$: then $f(m_1) = f(m_2)$ means both points are maxima or the maxima lie between them. For a general weakly unimodal $f$, no method based on comparisons can avoid scanning the flat parts.
- **Rounding of the inner points on integers.** With $m_1 = \lfloor (2lo + hi)/3 \rfloor$ and $m_2 = \lfloor (lo + 2hi)/3 \rfloor$, the two points coincide for $hi = lo + 1$, and the loop with updates $lo \leftarrow m_1$ or $hi \leftarrow m_2$ never ends. The symmetric form of line L9 and the updates $m_1 + 1$ and $m_2 - 1$ avoid this.
- **A stopping rule on the length in floating point.** "While $hi - lo > \varepsilon$" can loop forever when $\varepsilon$ is below the spacing of doubles near $m$, as for [binary search on real numbers](/binary-search-on-real-numbers/). Use a fixed number of steps.
- **Noise in $f$.** Near the mode, $f(m_1)$ and $f(m_2)$ differ by about the square of the distance to $m$ for a smooth $f$. Rounding errors in $f$ then decide the comparison. So the location of a smooth maximum is only accurate to about the square root of the precision of $f$, about $10^{-8}$ for doubles, no matter how many steps run.
- **A function that is not unimodal.** The method returns a point with no warning. A sum of unimodal functions is not unimodal in general; a sum of convex functions is convex.

## Implementations

## History

The name and the method are folklore. The question of the best placement of evaluations for a unimodal function was settled by Jack Kiefer in 1953, who showed that Fibonacci placement is optimal and that golden-section placement is its limit. Ternary search, which keeps the equal division into thirds, is the simplest method of the family and is the one usually taught in programming courses.

## References
