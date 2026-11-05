---
tag: ZDRDPS
kind: algorithm
slug: golden-section-search
name: Golden-section search
aliases:
- golden ratio search
- golden section minimization
area: searching/search-on-answers
level: intro
summary: Unimodal minimization that reuses one function evaluation per step by shrinking the interval by the golden ratio.
solves: [unimodal-optimization]
model: query-model
complexity:
  vars: {r: "the reduction (b − a)/ε of the interval of uncertainty"}
  time: {worst: Θ(log r), average: Θ(log r), best: Θ(log r)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 1953
  people: [Jack Kiefer]
  note: Kiefer derived the golden-section placement as the limit of the optimal Fibonacci placement in 1953.
prereqs: [unimodal-function, ternary-search, fibonacci-numbers]
see_also: [unimodal-optimization, ternary-search, fibonacci-search-unimodal, brent-method, binary-search-on-real-numbers, convex-function, quasiconvex-function]
sources:
  - book: isbn:9780521880688
    title: William H. Press, Saul A. Teukolsky, William T. Vetterling and Brian P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Section 10.1, Initially Bracketing a Minimum, and Section 10.2, Golden Section Search in One Dimension
  - paper: doi:10.1090/S0002-9939-1953-0055639-3
    title: "J. Kiefer, Sequential minimax search for a maximum, Proceedings of the American Mathematical Society 4(3) (1953), 502-506"
---

Golden-section search finds the minimum of a [unimodal function](/unimodal-function/) on an interval by keeping two inner points at the fractions $0.382$ and $0.618$ of the interval. Each step compares their values, discards the part outside one of them, and reuses the other point in the next step, so it costs one new evaluation and shrinks the interval by the factor $1/\varphi \approx 0.618$, where $\varphi = (1 + \sqrt5)/2$ is the golden ratio. With $N$ evaluations the final interval is $\varphi^{-(N-1)}$ times the initial one, within a factor $\varphi^2/\sqrt5 \approx 1.17$ of the best possible, which [Fibonacci search](/fibonacci-search-unimodal/) reaches. Unlike Fibonacci search it needs no budget fixed in advance, so it is the standard safe method for one-dimensional minimization.

## In plain words

You look for the lowest point of a valley, and you can only measure the height at places you choose. You keep two measured places inside the part where the bottom must be. The higher of the two cannot be on the far side of the bottom from the lower one, so you cut off the part beyond the higher place. Now one of the two old places is still inside the part that is left, and you measure only one new place.

For this to work every time, the two places must sit at fixed fractions of the part, and the old place must land on one of the fractions of the new part. Only one fraction does this: about 0.618, the golden ratio. Each new measurement then cuts the part to about 62 percent.

## The problem

The input is a function $f$ on an interval $[a, b]$ that is **strictly unimodal for a minimum**: there is a point $m$ such that $f$ is strictly decreasing on $[a, m]$ and strictly increasing on $[m, b]$. A strictly [convex function](/convex-function/) is an example, and so is any strictly [quasiconvex function](/quasiconvex-function/). The function is an oracle, and the cost is the number of evaluations, as in the [query model](/query-model/). The output is a point within $\varepsilon$ of $m$, or an interval of given length that holds $m$. For a maximum, minimize $-f$. This is the continuous form of [unimodal optimization](/unimodal-optimization/).

The comparison lemma for a minimum: for $x_1 < x_2$, $f(x_1) < f(x_2)$ implies $m < x_2$, $f(x_1) > f(x_2)$ implies $m > x_1$, and $f(x_1) = f(x_2)$ implies $x_1 < m < x_2$. It is the lemma on the page [unimodal function](/unimodal-function/), applied to $-f$.

## The algorithm

Let $\rho = (\sqrt5 - 1)/2 = 1/\varphi \approx 0.618$. It satisfies $\rho^2 = 1 - \rho \approx 0.382$. The inner points of an interval $[a, b]$ of length $L$ are $c = a + \rho^2 L$ and $d = a + \rho L$.

```pseudo id=main
GOLDEN-MIN(f, a, b, steps)               ▷ f strictly unimodal for a minimum on [a, b]
L1  ρ ← (√5 − 1) / 2
L2  c ← b − ρ(b − a);  d ← a + ρ(b − a)
L3  fc ← f(c);  fd ← f(d)
L4  for s ← 1 to steps do
L5      if fc < fd then                  ▷ the minimum is left of d
L6          b ← d;  d ← c;  fd ← fc;  c ← b − ρ(b − a);  fc ← f(c)
L7      else a ← c;  c ← d;  fc ← fd;  d ← a + ρ(b − a);  fd ← f(d)    ▷ right of c
L8  if fc < fd then b ← d else a ← c     ▷ one more cut, with no new evaluation
L9  return a + (b − a) / 2
```

**Why the ratio is $\rho$.** Suppose the inner points sit at the fractions $1 - t$ and $t$ of each interval, with $1/2 < t < 1$. If line L6 keeps $[a, d]$, the new length is $tL$, and the old $c$ is at distance $(1 - t)L$ from $a$. To be the new $d$, it must be at distance $t \cdot tL$. So $t^2 = 1 - t$, and $t = \rho$ is the only solution in $(0, 1)$. The case of line L7 gives the same equation by symmetry.

## Example

Take $f(x) = (x - 2)^2$ on $[0, 5]$, with the minimum at $2$, and $steps = 6$, so 8 evaluations. The rows show the state at line L5.

| step | a | b | c | d | f(c) | f(d) | action |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 5 | 1.9098 | 3.0902 | 0.0081 | 1.1885 | keep $[a, d]$ |
| 2 | 0 | 3.0902 | 1.1803 | 1.9098 | 0.6718 | 0.0081 | keep $[c, b]$ |
| 3 | 1.1803 | 3.0902 | 1.9098 | 2.3607 | 0.0081 | 0.1301 | keep $[a, d]$ |
| 4 | 1.1803 | 2.3607 | 1.6312 | 1.9098 | 0.1360 | 0.0081 | keep $[c, b]$ |
| 5 | 1.6312 | 2.3607 | 1.9098 | 2.0820 | 0.0081 | 0.0067 | keep $[c, b]$ |
| 6 | 1.9098 | 2.3607 | 2.0820 | 2.1885 | 0.0067 | 0.0355 | keep $[a, d]$ |

In each row one of $c$ and $d$ is a point of the previous row: the point $1.9098$ is reused four times. After the loop the interval is $[1.9098, 2.1885]$, of length $5\rho^6 \approx 0.279$, with $c = 2.0163$ and $d = 2.0820$. Line L8 finds $f(c) < f(d)$ and keeps $[1.9098, 2.0820]$, of length $5\rho^7 \approx 0.172$. The result is its midpoint $1.9959$. With the same 8 evaluations, [ternary search](/ternary-search/) makes 4 steps and leaves an interval of length $5 (2/3)^4 \approx 0.988$.

## Correctness

The invariant at line L5 is: the minimum $m$ lies in $[a, b]$, $c = a + \rho^2(b - a)$, $d = a + \rho(b - a)$, and $fc$, $fd$ are the values at $c$ and $d$. If $f(c) < f(d)$, the lemma gives $m < d$, so $[a, d]$ holds $m$; it has length $\rho L$, and the old $c$ is at distance $\rho^2 L = \rho \cdot \rho L$ from $a$, so it is the new $d$. If $f(c) \ge f(d)$, the lemma gives $m > c$, so $[c, b]$ holds $m$; it also has length $\rho L$, and the old $d$ is its new $c$, by the identity $\rho(1 + \rho) = 1$. Line L8 makes one more cut by the same lemma. The full proof is below.

## Complexity

- **Evaluations.** Exactly $steps + 2$. With $N = steps + 2$ evaluations the final interval has length $\rho^{N-1}(b - a)$. A reduction by a factor $r$ needs $N = 1 + \lceil \log_\varphi r \rceil \approx 1 + 1.44 \lg r$ evaluations.
- **Comparison with the optimum.** By Kiefer's theorem, no method with $N$ evaluations can guarantee an interval shorter than $(b - a)/F_{N+1}$, where $F_k$ are the [Fibonacci numbers](/fibonacci-numbers/). From $F_{N+1} \approx \varphi^{N+1}/\sqrt5$, the ratio of the golden-section interval to this bound tends to $\varphi^{N+1}\varphi^{-(N-1)}/\sqrt5 = \varphi^2/\sqrt5 \approx 1.1708$. So golden-section search uses at most one evaluation more than the optimum for the same final length, since $1.1708 < \varphi$.
- **Comparison with ternary search.** Ternary search shrinks by $\sqrt{2/3} \approx 0.816$ per evaluation and needs about $2.37$ times as many evaluations.
- **Time and space.** $O(1)$ work and space per step besides the evaluation.

## Properties

- **One evaluation per step.** The reuse is exact in exact arithmetic, because of $\rho^2 = 1 - \rho$.
- **Constant ratio.** Each step shrinks the interval by the same factor, so the method can stop at any tolerance and need not know the number of evaluations in advance.
- **Comparisons only.** It uses only the order of the two values, so a monotone change of $f$ does not change its steps.
- **Robust.** It converges linearly for every strictly unimodal $f$, smooth or not. It does not exploit smoothness; methods that do are faster on smooth functions but can fail on rough ones.

## Variants and improvements

- **Bracketing first.** If no interval is known, start from two points and step downhill with growing steps, by the factor $\varphi$, until the value rises. This gives a triple $x_1 < x_2 < x_3$ with $f(x_2) < f(x_1)$ and $f(x_2) < f(x_3)$, which holds a minimum of a unimodal $f$ (Numerical Recipes, Section 10.1). Golden-section search then starts from the triple.
- **Three-point form.** Numerical Recipes keeps a bracketing triple instead of two inner points, and puts the new point at the fraction $0.382$ into the larger of the two parts. The steps are the same once the triple has golden proportions, and the form tolerates a start with other proportions.
- **Fibonacci search.** For a known number $N$ of evaluations, the ratios $F_{k}/F_{k+1}$ in place of $\rho$ give the optimal final interval. See [Fibonacci search](/fibonacci-search-unimodal/).
- **Brent's method.** Fit a parabola through the three best points and jump to its vertex when this is safe, and fall back to a golden-section step otherwise. Near a smooth minimum it converges superlinearly. See [Brent's method](/brent-method/).
- **On integers.** Round the inner points to integers. The reuse then holds only approximately; Fibonacci search is the exact integer form.

## When to use it

Use golden-section search to minimize a function of one variable when each evaluation is expensive, the function is unimodal on a known interval, and no derivative is available or the function is not smooth. It is the usual line search of simple optimization codes, and the fallback inside Brent's method. On integers, or when the number of evaluations is fixed, use Fibonacci search. For a cheap function in a short program, [ternary search](/ternary-search/) is simpler.

## Pitfalls

- **Recomputing the reused value.** Calling $f$ at both inner points in each step turns the method into a slower ternary search. Keep $fc$ and $fd$.
- **Drift of the inner points.** Computing the new point as $a + b - d$ instead of from the ends lets rounding errors grow over many steps until $c \ge d$. Compute the new point from $a$, $b$ and $\rho$ as in lines L6 and L7.
- **A tolerance below the precision.** Near a smooth minimum, $f(m + \delta) - f(m) \approx \tfrac12 f''(m)\delta^2$. When this is below the rounding error of $f$, the comparison is noise. So the minimum can be located only to about $\sqrt{\epsilon_{\text{mach}}}\,|m|$, about $10^{-8}|m|$ for doubles, and a smaller tolerance only wastes evaluations (Numerical Recipes, Section 10.2).
- **A function that is not unimodal.** The method then converges to a local minimum or to a point where the function is not smallest, with no warning. Plot or sample the function first when unimodality is not proved.
- **Plateaus.** As for ternary search, flat parts away from the minimum can make line L7 discard the minimum.

## Implementations

## History

Jack Kiefer found the optimal search with a fixed number of evaluations, the Fibonacci search, in 1953, and noted that its ratios tend to the golden ratio when the number of evaluations grows. The golden-section form, with the limit ratio at each step, is the version for an open-ended search. Richard Brent combined it with parabolic interpolation in 1973.

## References
