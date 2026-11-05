---
tag: CEFP1M
kind: problem
slug: unimodal-maximum
name: Maximum of a unimodal function
aliases:
- unimodal search
area: searching/sequential-and-binary-search
level: core
summary: Find the maximum of a unimodal function or sequence by evaluating it at a logarithmic number of points.
model: comparison-model
complexity:
  vars: {n: the number of points of the domain}
  time: {worst: Θ(log n)}
prereqs: [unimodal-function, peak-finding]
see_also: [peak-finding, ternary-search, golden-section-search, fibonacci-search-unimodal, unimodal-optimization, bitonic-sequence, find-maximum, rotated-sorted-array-minimum]
sources:
  - paper: doi:10.1090/S0002-9939-1953-0055639-3
    title: J. Kiefer, Sequential minimax search for a maximum, Proceedings of the American Mathematical Society 4(3) (1953)
    locator: pp. 502 to 506 (Fibonacci search is minimax optimal for the number of evaluations)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1, Searching an ordered table (Fibonaccian search, and the exercises on the maximum of a unimodal function)
---

The maximum of a [unimodal function](/unimodal-function/) is the problem of finding the mode of a function that strictly rises up to one point and strictly falls after it, using as few evaluations as possible. On the integers $0, \ldots, n-1$ the [finding the maximum](/find-maximum/) scan needs $n - 1$ comparisons, but unimodality lets each comparison of two values throw away part of the domain, so $\Theta(\log n)$ evaluations are enough. A [binary search](/binary-search/) on the slope uses about $2 \lg n$ evaluations, [ternary search](/ternary-search/) about $3.4 \lg n$, and [Fibonacci search](/fibonacci-search-unimodal/) about $1.44 \lg n$, which Kiefer proved in 1953 to be the least possible. On a real interval the same methods shrink the interval by a fixed factor per evaluation, and the limit of Fibonacci search is [golden section search](/golden-section-search/).

## In plain words

A path goes up a single hill and then down, with no flat parts. You want the top, and each look at a height costs you. Looking at one point tells you nothing. Looking at two points tells you a lot: the top is not beyond the lower of the two, on its far side.

So you look at two points inside the path and throw away the part beyond the lower one. Then you need only one new look, because one of the old points is still inside. If you place the points well, the path left is about 62 percent of the old one after each look. A path of a thousand points then needs about fifteen looks.

## Definition

**Input.** A function $f$ on $D = \{0, 1, \ldots, n-1\}$, $n \ge 1$, given as a black box that returns $f(i)$ for any $i$, and that is strictly unimodal: there is a mode $m$ with $f(0) < \cdots < f(m)$ and $f(m) > f(m + 1) > \cdots > f(n-1)$.

**Output.** The mode $m$, the index of the maximum.

**Cost.** The number of evaluations of $f$. Each comparison involves two values, so a comparison costs at most two evaluations, and less when a value is reused.

**The continuous form.** $f$ is strictly unimodal on a real interval $[a, b]$, and the output is an interval of length at most $\varepsilon$ that contains the mode. The cost is the number of evaluations as a function of $(b - a)/\varepsilon$.

The basic fact is the comparison lemma of the [unimodal function](/unimodal-function/) page: for $x_1 < x_2$, $f(x_1) < f(x_2)$ gives $m > x_1$, $f(x_1) > f(x_2)$ gives $m < x_2$, and equal values give $x_1 < m < x_2$.

## Variants

- **Minimum of a unimodal function.** Apply the method to $-f$; this is the usual form for convex functions in [unimodal optimization](/unimodal-optimization/).
- **Weakly unimodal functions.** With flat parts, two equal values say nothing about the side of the mode, and the worst case is $\Theta(n)$: a function that is constant except for one higher point needs a scan.
- **Bitonic arrays.** An array that rises and then falls is a [bitonic sequence](/bitonic-sequence/); its maximum is the turning point, and the search for a key in it is a maximum search followed by two binary searches.
- **Any peak.** Without unimodality, the same slope search finds a local maximum, which is the [peak finding](/peak-finding/) problem.
- **Rotated sorted arrays.** A sorted array rotated by an unknown amount has a cyclic structure of the same kind, and its minimum is found by a similar search; see [minimum of a rotated sorted array](/rotated-sorted-array-minimum/).

## Examples

For $f = [1, 4, 9, 15, 22, 26, 25, 19, 12, 6, 2]$, with $n = 11$, the mode is $m = 5$.

**Slope search.** Compare $f(mid)$ and $f(mid + 1)$ and keep the side that goes up, as in [peak finding](/peak-finding/): $f(5) = 26 > f(6) = 25$ gives $hi = 5$; $f(2) = 9 < f(3) = 15$ gives $lo = 3$; $f(4) = 22 < f(5) = 26$ gives $lo = 5$. Three comparisons and six evaluations.

**Costs for three methods.** The table gives the worst case over all modes of the number of evaluations, counted by running each method on a strictly unimodal $f$ with each possible mode. The optimum is the result of an exhaustive search over all strategies for $n \le 60$, and the Fibonacci formula below for larger $n$:

| $n$ | 10 | 100 | 1000 |
|---|---|---|---|
| slope search, $2\lceil \lg n \rceil$ | 8 | 14 | 20 |
| ternary search (thirds, then a final scan of at most 3 points) | 8 | 19 | 30 |
| optimal, Fibonacci search | 5 | 10 | 15 |

## Known algorithms

- **Slope search.** Binary search for the first $i$ with $f(i) > f(i + 1)$, which is the mode; the test is a [monotone predicate](/monotone-predicate/) on a unimodal function. It makes $\lceil \lg n \rceil$ comparisons and $2\lceil \lg n \rceil$ evaluations.
- **[Ternary search](/ternary-search/).** Evaluate $f$ at the two points that cut the range into thirds, and drop the third beyond the lower value. Each step costs two evaluations and keeps $2/3$ of the range, so the cost is about $2\log_{3/2} n \approx 3.42 \lg n$ evaluations. It is simple, but it reuses no value.
- **[Fibonacci search](/fibonacci-search-unimodal/).** Keep the range at a Fibonacci size $F_{k} - 1$, and place the two points so that after the comparison the point that stays inside is one of the two points of the next step. So each step needs one new evaluation, and the range shrinks by the ratio of consecutive Fibonacci numbers, about $1/\varphi \approx 0.618$. With $k$ evaluations it finds the mode of every unimodal $f$ on up to $F_{k+2} - 1$ points.
- **[Golden section search](/golden-section-search/).** The continuous limit of Fibonacci search: the points cut the interval in the ratio $\varphi$, and each evaluation shrinks the interval by the factor $1/\varphi$. It does not need $n$ or $\varepsilon$ in advance.

All of these use $O(1)$ extra space.

## Bounds

**Upper bound.** For $n \ge 2$, Fibonacci search uses $k$ evaluations, where $k$ is the smallest integer with $F_{k+2} \ge n + 1$. Since $F_{k+2} \approx \varphi^{k+2}/\sqrt{5}$, this is $\log_\varphi n + O(1) \approx 1.44 \lg n$.

**Lower bound.** No method uses fewer evaluations in the worst case: Kiefer proved that Fibonacci search is minimax optimal. The table above matches this: an exhaustive search over all strategies gives the least worst-case number of evaluations as 2 for $n = 2$, 3 for $n \le 4$, 4 for $n \le 7$, 5 for $n \le 12$, 6 for $n \le 20$, and in general $k$ for $F_{k+1} \le n \le F_{k+2} - 1$.

**A simple lower bound.** Each method needs at least $\lfloor \lg n \rfloor$ evaluations. The adversary of the lower bound on the [peak finding](/peak-finding/) page builds values that grow toward an interval from both sides and have a single peak inside it, so every input it builds is strictly unimodal, and its bound applies here as it is.

The lower bound of [finding the maximum](/find-maximum/), $n - 1$ comparisons, does not apply, because unimodality is extra information.

## Reductions

- **It reduces to [peak finding](/peak-finding/).** A strictly unimodal $f$ has one peak, which is its mode, so any peak-finding method solves it.
- **It reduces to a boundary search.** The test $P(i) = (f(i) > f(i + 1))$ is false before the mode and true from the mode on, so the mode is the first true index, as in [lower and upper bound search](/lower-and-upper-bound-search/).
- **Minimizing a convex function reduces to it,** since a continuous strictly convex function on an interval is unimodal for a minimum.

## Applications

- Tune one parameter of a process whose quality first rises and then falls, such as a step size, a threshold or a temperature, when each trial is costly.
- Find the turning point of a bitonic array, as a first step of a search for a key in it.
- Find the best split point in a balance problem, such as the time at which two opposing costs have the smallest maximum.
- Line search in numerical optimization: the minimum of $f(x + t d)$ in the step $t$ along a direction $d$.

## References
