---
tag: SHXFW1
kind: technique
slug: binary-search-on-real-numbers
name: Binary search on real numbers
area: searching/search-on-answers
level: intro
summary: Binary search over a continuous range that halves the interval a fixed number of times or until the precision is reached.
prereqs: [binary-search-on-answer, monotone-predicate, floating-point-arithmetic]
see_also: [bisection-method, ternary-search, fractional-programming, parametric-search, machine-epsilon, root-finding-problem]
sources:
  - url: https://cp-algorithms.com/num_methods/binary_search.html
    title: cp-algorithms, Binary search
    note: the section Continuous search
  - book: isbn:9781305253667
    title: Richard L. Burden, J. Douglas Faires and Annette M. Burden, Numerical Analysis, tenth edition
    locator: Section 2.1, The Bisection Method
  - paper: doi:10.1145/103162.103163
    title: "David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48"
    locator: the sections on rounding error, relative error and ulps
---

Binary search on real numbers finds the threshold of a [monotone predicate](/monotone-predicate/) on a real interval $[a, b]$ by halving the interval that holds it, until the interval is shorter than a tolerance $\varepsilon$ or for a fixed number of steps. After $k$ steps the interval has length $(b - a)/2^k$, so $\lceil \lg((b - a)/\varepsilon) \rceil$ steps reach the tolerance. It is the real-valued form of [binary search on the answer](/binary-search-on-answer/), and it shares its loop with the [bisection method](/bisection-method/) for roots, but it needs monotonicity where the bisection method needs only a sign change.

## In plain words

Sometimes the answer is not a whole number but a real number, such as a time, a radius or an average. You still have a test that says "yes" for large values and "no" for small values. You keep a low value where the test says "no" and a high value where it says "yes". You test the point halfway between them and move one of the two ends to it. The gap between the ends halves each time.

The gap never becomes zero, so you must decide when to stop. You can stop when the gap is smaller than the error you accept, or after a fixed number of steps. On a computer the numbers have limited precision, and a stopping rule that asks for too much precision can run forever.

## When it applies

- **A real answer.** The quantity is a real number in a known interval $[a, b]$, and an approximation within $\varepsilon$ is acceptable.
- **A monotone test.** $P : [a, b] \to \{\text{false}, \text{true}\}$ with $x \le y$ and $P(x) \Rightarrow P(y)$. By the threshold form on an interval, its true set is $[c, b]$ or $(c, b]$, and the search finds $c$.
- **Or a continuous function with a sign change.** For a continuous $g$ with $g(a) < 0 < g(b)$, the [bisection method](/bisection-method/) keeps the sign change and finds *some* root, by the intermediate value theorem, without any monotonicity. If $g$ is non-decreasing, the predicate $g(x) \ge 0$ is monotone and the two views agree.
- **A test that is robust to small errors.** The computed test should be exact or wrong only very close to $c$, so that rounding moves the answer by a small amount.

## The template

```pseudo id=main
REAL-SEARCH(lo, hi, P, steps)        ▷ P(lo) is false or lo = a; P(hi) is true
L1  for s ← 1 to steps do
L2      mid ← lo + (hi − lo) / 2
L3      if P(mid) then hi ← mid      ▷ c ≤ mid
L4      else lo ← mid                ▷ c ≥ mid
L5  return hi                        ▷ c ∈ [lo, hi], hi − lo = (b − a) / 2^steps
```

The holes are $P$ and the number of steps. To find the largest $x$ where a true-then-false test holds, swap the two branches.

**Invariant.** $c \in [lo, hi]$, where $c$ is the threshold. At the start $lo = a$, $hi = b$. If $P(mid)$ is true, $c \le mid$ because $c$ is the infimum of the true set, so $c \in [lo, mid]$. If $P(mid)$ is false, each point below $mid$ is false by monotonicity, so $c \ge mid$ and $c \in [mid, hi]$. Each step halves $hi - lo$ in exact arithmetic, so after $k$ steps $hi - lo = (b - a)/2^k$, and both ends are within that distance of $c$.

**The number of steps.** An absolute error $\varepsilon$ needs $(b - a)/2^k \le \varepsilon$, that is $k = \lceil \lg((b - a)/\varepsilon) \rceil$. For $b - a = 10$ and $\varepsilon = 10^{-6}$, $k = 24$. A relative error $\varepsilon$ on an answer of size about $|c| \ge 1$ needs about $\lg((b - a)/(\varepsilon |c|))$ steps. Each step gains one bit. A double has 53 bits of significand, so full precision needs $(b - a)/2^k \le 2^{-53}|c|$; with $k = 100$ steps this holds whenever $b - a \le 2^{47}|c|$, that is, when the interval is at most about $1.4 \times 10^{14}$ times the answer.

**Two stopping rules.** A fixed number of steps always ends and gives a known error. The rule "while $hi - lo > \varepsilon$" gives the same result in exact arithmetic but can loop forever in floating point, as the pitfalls below show.

## Classic examples

### A cube root

Find $\sqrt[3]{10}$ with $P(x) = (x^3 \ge 10)$ on $[0, 10]$. The first six steps are:

| step | lo | hi | mid | $P(mid)$ |
|---|---|---|---|---|
| 1 | 0 | 10 | 5 | true |
| 2 | 0 | 5 | 2.5 | true |
| 3 | 0 | 2.5 | 1.25 | false |
| 4 | 1.25 | 2.5 | 1.875 | false |
| 5 | 1.875 | 2.5 | 2.1875 | true |
| 6 | 1.875 | 2.1875 | 2.03125 | false |

After 24 steps the interval is $[2.1544343, 2.1544349]$, of length $5.96 \times 10^{-7} < 10^{-6}$, and it holds $\sqrt[3]{10} = 2.15443469\ldots$. Newton's method would need far fewer steps here, because $x^3$ is smooth; the binary search needs only monotonicity.

### The largest average of a long segment

Given $a = [1, 12, -5, -6, 50, 3]$ and $k = 4$, find the largest average of a contiguous segment of length at least $k$. The test "is there such a segment with average at least $t$?" is true for $t \le \mathrm{OPT}$ and false for $t > \mathrm{OPT}$, so it is monotone (true then false). It is equivalent to "is there a segment of length at least $k$ with $\sum (a_i - t) \ge 0$?", which one pass over the prefix sums answers in $O(n)$ time: keep the minimum prefix sum that ends at least $k$ places before the current position. The search on $[\min a, \max a] = [-6, 50]$ tests $t = 22$ (no), $8$ (yes), $15$ (no), $11.5$ (yes), $13.25$ (no), and after 50 steps it brackets $12.75$, the average of $12, -5, -6, 50$. This test is the parametric form of a ratio problem; see [fractional programming](/fractional-programming/).

### Geometry and physics

The smallest radius such that $k$ disks of that radius cover given points, the time when two moving objects first come within a distance, and the largest load a structure takes without failure are all thresholds of monotone tests, and are found this way when the test is easier than a formula.

## Variations

- **Search on the bits of a double.** For non-negative IEEE 754 doubles, the order of the values is the order of their bit patterns read as unsigned integers. A binary search over the 64-bit integers between the patterns of $a$ and $b$ therefore finds the exact smallest double where the computed test is true, in at most 64 steps, with no tolerance.
- **Search on the answer with exact rationals.** When the answer is a fraction with denominator at most $Q$, two such fractions differ by at least $1/Q^2$. A real search to an error less than $1/(2Q^2)$ followed by a rounding to the nearest fraction with denominator at most $Q$ (by continued fractions or the Stern-Brocot tree) gives the exact answer.
- **[Ternary search](/ternary-search/).** For the maximum of a unimodal function, the analogous loop compares two inner points; it searches for the point where the predicate "$f$ is falling at $x$" becomes true, without computing a derivative.
- **[Parametric search](/parametric-search/).** It finds the exact real threshold when the test is an algorithm whose comparisons are signs of low-degree polynomials in $t$.
- **The [bisection method](/bisection-method/).** The same loop for roots of a continuous function, where the invariant is a sign change.

## Pitfalls

- **A tolerance below the spacing of doubles.** Near $10^9$, adjacent doubles are $2^{-23} \approx 1.19 \times 10^{-7}$ apart. With $\varepsilon = 10^{-9}$, the interval shrinks to two adjacent doubles, the midpoint rounds to one of the ends, and $hi - lo$ stays at $1.19 \times 10^{-7}$: the loop "while $hi - lo > \varepsilon$" never ends. Use a fixed number of steps, a relative tolerance, or also stop when $mid$ equals $lo$ or $hi$.
- **A test that is not monotone in floating point.** Rounding can make a monotone test change its value more than once near the threshold. The search then returns one of these points; the error is small only if the test is accurate near $c$. Sums of many terms of mixed sign are the usual cause.
- **Comparing with zero.** A test of the form $g(t) \ge 0$ with a computed $g$ is wrong when the true value is $0$ and the computed value is $-10^{-17}$. Decide which side the boundary belongs to, or use exact arithmetic for the test when the input is integral.
- **The interval does not hold the answer.** If $P(b)$ is false, the search returns $b$ as if it were the threshold. Check the ends, or choose $b$ from a proven bound.
- **Too few steps for a wide range.** With $[a, b] = [0, 10^{18}]$ and an answer near $10^{-6}$, 60 steps leave an absolute error of about $10^{18}/2^{60} \approx 0.87$. Search on a logarithmic scale, or use the bit-pattern variation.

## Exercises

1. Show that REAL-SEARCH with the condition "while $mid \ne lo$ and $mid \ne hi$" stops after finitely many steps for any doubles $lo < hi$.
2. Prove that the segment-average test of the example is monotone, and write the $O(n)$ pass that answers it.
3. The answer of a problem is a fraction $p/q$ with $1 \le q \le 1000$. How many steps of a real search on $[0, 1]$ are enough to identify it exactly?
4. Explain why the bisection method finds a root of $g(x) = (x - 1)(x - 2)(x - 3)$ on $[0, 4]$, while a search for the threshold of $g(x) \ge 0$ on $[0, 4]$ is not well defined.

## References
