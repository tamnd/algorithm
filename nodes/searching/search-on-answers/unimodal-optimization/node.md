---
tag: FHQ66K
kind: problem
slug: unimodal-optimization
name: Unimodal function optimization
aliases:
- finding the extremum of a unimodal function
- one-dimensional unimodal minimization
area: searching/search-on-answers
level: intro
summary: Find the maximum or minimum of a unimodal function using only function evaluations.
prereqs: [unimodal-function, fibonacci-numbers]
see_also: [ternary-search, golden-section-search, fibonacci-search-unimodal, unimodal-maximum, peak-finding, binary-search-on-real-numbers, convex-function, monotone-predicate]
sources:
  - paper: doi:10.1090/S0002-9939-1953-0055639-3
    title: "J. Kiefer, Sequential minimax search for a maximum, Proceedings of the American Mathematical Society 4(3) (1953), 502-506"
    locator: the minimax theorem for N evaluations and the Fibonacci strategy
  - book: isbn:9780521880688
    title: William H. Press, Saul A. Teukolsky, William T. Vetterling and Brian P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Sections 10.1 (bracketing a minimum), 10.2 (golden section search) and 10.3 (Brent's method)
  - book: isbn:9783319725468
    title: Antti Laaksonen, Guide to Competitive Programming, first edition, Springer, 2017
    locator: Section 8.3, Finding Minimum Values
---

Unimodal function optimization asks for the point where a [unimodal function](/unimodal-function/) takes its maximum (or minimum), when the only access to the function is to evaluate it at chosen points. Each comparison of two values removes a part of the domain, so the mode can be found with a logarithmic number of evaluations: on $n$ integer points, $N$ evaluations suffice exactly when $n \le F_{N+2} - 1$, where $F_k$ are the [Fibonacci numbers](/fibonacci-numbers/). [Fibonacci search](/fibonacci-search-unimodal/) meets this bound, [golden-section search](/golden-section-search/) is within a constant factor of it without knowing $N$ in advance, and [ternary search](/ternary-search/) is the simplest method.

## In plain words

A function goes up to one highest point and then goes down, and you want that highest point. You cannot see the whole curve. You can only ask for its value at one point at a time, and each question costs something.

If you know the values at two points, the higher of the two tells you which side of the curve you are on. The top cannot be beyond the lower point on the far side, so you throw that part away. Then you ask about a new point in the part that is left. The best methods place the points so that one old point can be used again in the next step. Then each new question shrinks the part that is left by a fixed fraction.

## Definition

**Discrete form.** The input is a number $n \ge 1$ and an oracle for $f : \{1, \ldots, n\} \to \mathbb{R}$, which is promised to be strictly unimodal for a maximum. The output is the mode $m$, the unique index with $f(m) = \max f$. The cost is the number of oracle calls.

**Continuous form.** The input is an interval $[a, b]$, a tolerance $\varepsilon > 0$ and an oracle for a strictly unimodal $f : [a, b] \to \mathbb{R}$. The output is an interval of length at most $\varepsilon$ that holds the mode. With finitely many evaluations the exact mode of a continuous function cannot be known, so the output is an interval of uncertainty.

**The interval of uncertainty.** After evaluations at points $x_1 < x_2 < \cdots < x_t$ with distinct values, let $x_j$ have the largest value. By the comparison lemma on the page [unimodal function](/unimodal-function/), the mode lies in the open interval $(x_{j-1}, x_{j+1})$, with $x_0 = a$ and $x_{t+1} = b$ (or $0$ and $n + 1$ in the discrete form), and every point of this interval is the mode of some unimodal function with the same values at $x_1, \ldots, x_t$. So a method needs to keep only this *bracket* and the best point $x_j$ inside it.

The minimum form is the same problem for $-f$.

## Variants

- **Known or unknown budget.** If the number $N$ of evaluations is fixed in advance, Fibonacci search is optimal. If the method must stop at a tolerance or may be stopped at any time, golden-section search has a fixed ratio and is nearly as good.
- **Weakly unimodal functions.** With flat parts allowed, the comparison of two equal values gives no information. The sequence that is $0$ everywhere except a single $1$ is weakly unimodal, and an adversary that answers $0$ forces every method to evaluate all $n$ points. So this variant needs $n$ evaluations in the worst case.
- **Derivative available.** If $f$ is differentiable and unimodal with $f' > 0$ before the mode and $f' < 0$ after it, the sign of $f'$ is a [monotone predicate](/monotone-predicate/), and [bisection](/binary-search-on-real-numbers/) halves the interval with each derivative evaluation.
- **Local maximum of any array.** Without unimodality, a local maximum (an index no smaller than its neighbours) still exists and can be found with $O(\log n)$ evaluations. This is [peak finding](/peak-finding/).
- **Noisy evaluations.** When each value has random error, the comparison may be wrong, and stochastic approximation methods replace exact search.
- **Many dimensions.** For functions of several variables, no analogue of the logarithmic bound holds for unimodality alone, and methods use convexity or line searches along directions.

## Examples

**A sequence of 12 items.** Let $f = (2, 5, 9, 14, 20, 23, 21, 18, 11, 8, 4, 1)$ on indices $1$ to $12$, with mode $6$. Since $12 \le F_7 - 1 = 12$, five evaluations are enough, and Fibonacci search uses exactly five: it starts with the bracket $(0, 13)$ and the points $5$ and $8$. Then $f(5) = 20 > f(8) = 18$ leaves the bracket $(0, 8)$ with best point $5$; the next points are $3$ (bracket $(3, 8)$), then $6$ (bracket $(5, 8)$, best point $6$), then $7$ (bracket $(5, 7)$). The only index left is $6$.

**A continuous minimum.** $f(x) = (x - 2)^2$ on $[0, 5]$ has its minimum at $2$. With $N = 10$ evaluations, the best guaranteed interval has length about $5/F_{11} = 5/89 \approx 0.056$; golden-section search guarantees $5 \cdot 0.618^9 \approx 0.066$; ternary search with the same 10 evaluations (5 steps) guarantees $5 \cdot (2/3)^5 \approx 0.66$.

**The budget for common sizes.** The smallest $N$ with $F_{N+2} - 1 \ge n$ is $5$ for $n = 10$, $10$ for $n = 100$, $15$ for $n = 1000$ and $29$ for $n = 10^6$. A binary search on the predicate $f(i) > f(i+1)$ needs $\lceil \lg n \rceil$ steps of two evaluations each, that is $8$, $14$, $20$ and $40$ evaluations.

## Known algorithms

| method | evaluations for a factor $r$ of reduction | needs $N$ in advance | page |
|---|---|---|---|
| Fibonacci search | $N$ with $F_{N+1} \ge r$, about $\log_\varphi r + 0.67$ | yes | [Fibonacci search](/fibonacci-search-unimodal/) |
| Golden-section search | $1 + \lceil \log_\varphi r \rceil$ | no | [golden-section search](/golden-section-search/) |
| Binary search on differences | $2 \lceil \lg r \rceil$ (discrete) | no | [unimodal maximum](/unimodal-maximum/) |
| Ternary search | $2 \lceil \log_{3/2} r \rceil$ | no | [ternary search](/ternary-search/) |
| Brent's method | superlinear near a smooth minimum, golden-section steps otherwise | no | Numerical Recipes, Section 10.3 |

Here $\varphi = (1 + \sqrt 5)/2 \approx 1.618$ and $\log_\varphi r \approx 1.44 \lg r$. The ternary search counts assume two new evaluations per step; the version that reuses nothing is the simplest to write and the slowest of the four.

## Bounds

**Theorem (discrete).** For $N \ge 1$, there is a method that finds the mode of every strictly unimodal $f$ on $\{1, \ldots, n\}$ with at most $N$ evaluations if and only if $n \le F_{N+2} - 1$.

*Proof of the lower bound.* A state is a bracket $(l, r)$ of integers with one evaluated point $p$, $l < p < r$, whose value is larger than the values at $l$ and $r$ (when these are evaluated). Call $p - l$ and $r - p$ its two *parts* and $g = r - l$ its *gap*. The method is done exactly when $g = 2$, because otherwise some index other than $p$ is still a possible mode. We show by induction on $k$: if the method can finish from a state with $k$ evaluations left against every answer, then $g \le F_{k+3}$ and both parts are at most $F_{k+2}$.

For $k = 0$ the state must already be done, so $g = 2 = F_3$ and both parts are $1 = F_2$. Let $k \ge 1$, let the parts be $a \le b$, and let the method evaluate $q$. If $q$ is outside $(l, r)$ or $q = p$, the bracket does not change, and the claim for $k - 1$ gives a stronger bound. Otherwise the adversary may choose either of the two answers of the comparison lemma, and both give states that must be finished with $k - 1$ evaluations.

- If $q$ is in the larger part, at distance $w$ from $p$, the two possible states have parts $(a, w)$ and $(w, b - w)$, with gaps $a + w$ and $b$. By induction $b \le F_{k+2}$ and $a \le F_{k+1}$, so $g = a + b \le F_{k+1} + F_{k+2} = F_{k+3}$.
- If $q$ is in the smaller part, at distance $w$ from $p$, one possible state has parts $(w, b)$. By induction $b \le F_{k+1}$, so $a + b \le 2F_{k+1} \le F_{k+3}$, and both parts are at most $F_{k+1} \le F_{k+2}$.

The adversary's answers are realizable: when it keeps the side of $p$, it gives $q$ a value between $f(p)$ and the value at the bracket end on that side; when it keeps the side of $q$, it gives $q$ the value $f(p) + 1$. In both cases the values stay strictly increasing up to the best point and strictly decreasing after it. Now take a method for $n$ points. Its first evaluation, at some $p$, gives the state with bracket $(0, n + 1)$ and $N - 1$ evaluations left. So $n + 1 \le F_{N+2}$. $\square$

*Proof of the upper bound.* Pad $f$ to length $F_{N+2} - 1$ with values that decrease and are below $f(n)$; the padded function is still unimodal with the same mode. Start with the bracket $(0, F_{N+2})$ and evaluate $p = F_N$, which gives parts $(F_N, F_{N+1})$. From a state with parts $\{F_{k+1}, F_{k+2}\}$ and $k$ evaluations left, evaluate the point $q$ in the larger part at distance $F_k$ from $p$. Both possible new states have parts $\{F_k, F_{k+1}\}$, as in the first case above with $w = F_k$. After $k$ more steps the parts are $\{F_1, F_2\} = \{1, 1\}$ and the method is done. This is [Fibonacci search](/fibonacci-search-unimodal/). $\square$

**Theorem (continuous; Kiefer 1953).** For a method with $N \ge 1$ evaluations on $[a, b]$, the worst-case final interval of uncertainty is at least $(b - a)/F_{N+1}$, and for each $\delta > 0$ a method achieves at most $(b - a)/F_{N+1} + \delta$. The same induction, with lengths in place of integer gaps, proves the lower bound; the $\delta$ is needed because two evaluations at the same point give no information.

**Consequences.** On $n$ points the cost is $\log_\varphi n + O(1) \approx 1.44 \lg n$ evaluations, so $\Theta(\log n)$. Golden-section search ends with an interval $\varphi^2/\sqrt 5 \approx 1.17$ times longer than the optimum for large $N$. Without unimodality, the maximum of an arbitrary sequence needs all $n$ evaluations, since any value not evaluated may be the largest.

## Reductions

- **To a threshold search.** On integers, $f$ is strictly unimodal if and only if $P(i) = (f(i) > f(i+1))$ is false and then true, with threshold at the mode. So unimodal maximization reduces to a [lower bound search](/lower-and-upper-bound-search/) with two evaluations per step. The Fibonacci bound shows that this reduction costs a factor of about $2/1.44 \approx 1.39$ in evaluations.
- **Convex minimization.** A continuous strictly convex function on a closed interval is unimodal for a minimum, so every method here minimizes it. Many problems of [binary search on the answer](/binary-search-on-answer/) type have a convex cost in one parameter and are solved by [ternary search](/ternary-search/).

## Applications

- **Line search.** Methods for functions of many variables choose a direction and then minimize along a line, often by bracketing and golden-section search or Brent's method.
- **Tuning one parameter.** Experiments in which each trial is expensive, such as setting a temperature or a dose, with a response that has one best value. This was Kiefer's motivation.
- **Bitonic data.** The largest item of an array that increases and then decreases, such as a rotated or mountain array.
- **Programming contests.** The minimum of a convex cost over an integer or real parameter, such as a position or a time.

## References
