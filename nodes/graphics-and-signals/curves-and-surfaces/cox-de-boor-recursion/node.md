---
tag: GGMD1V
kind: algorithm
slug: cox-de-boor-recursion
name: Cox-de Boor recursion
aliases:
- Cox-de Boor formula
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Computes the B-splines of degree p from those of degree p - 1 with two linear weights. On one knot span it gives the p + 1 nonzero values in p(p + 1)/2 steps, with 0/0 read as 0.
solves: [spline-evaluation]
model: real-ram
complexity:
  vars: {p: the degree}
  time: {worst: Θ(p^2), best: Θ(p^2)}
  space: {extra: Θ(p)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1972
  people: [Maurice G. Cox, Carl de Boor]
  note: Cox and de Boor published the recurrence for B-spline values independently in 1972. Cox gave a rounding error analysis.
prereqs: [b-spline, knot-vector]
see_also: [de-boor-algorithm, partition-of-unity, spline-evaluation, divided-differences, binary-search, de-casteljau-algorithm, nurbs]
sources:
  - paper: doi:10.1093/imamat/10.2.134
    title: Maurice G. Cox, The numerical evaluation of B-splines, IMA Journal of Applied Mathematics (then J. Inst. Maths Applics) 10(2) (1972), 134 to 149
    locator: the recurrence relation for B-splines and its rounding error analysis
  - paper: "Carl de Boor, On calculating with B-splines, Journal of Approximation Theory 6 (1972), 50 to 62"
    locator: the recurrence for B-splines and its use to evaluate a B-spline series
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter IX, the recurrence relation for B-splines; Chapter X, The stable evaluation of B-splines and splines (the routine BSPLVB)
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 2.2, Definition and properties of B-spline basis functions (the recursive definition and the convention 0/0 = 0); Section 2.5, Computational algorithms (FindSpan and BasisFuns)
---

The Cox-de Boor recursion defines the [B-splines](/b-spline/) $N_{i,p}$ of a [knot vector](/knot-vector/) by induction on the degree: each $N_{i,p}$ is a weighted sum of $N_{i,p-1}$ and $N_{i+1,p-1}$ with weights that are linear in the parameter, and a quotient $0/0$ that repeated knots produce is read as $0$. As an algorithm it computes, at a parameter $u$ in a nonempty knot span, the $p + 1$ B-splines that are not zero there, in $p(p + 1)/2$ steps of a triangle. Every step forms a convex combination, so the method has no cancellation. It is the standard way to get basis values for [spline evaluation](/spline-evaluation/), for collocation and least squares matrices, and for [NURBS](/nurbs/).

## In plain words

A B-spline of degree zero is a switch: it is one on its own interval between two knots and zero elsewhere. A B-spline of the next degree blends two neighbors of the degree below. The blend fades one neighbor out and the other one in, linearly, across the knots that the two neighbors share.

To get the values at one point, start with the one switch that is on there. Then go up one degree at a time. At each level, each value splits into a left part and a right part, and each part goes to one of the two new values next to it. At the end you have one more value than the degree, and all other basis functions are zero at that point.

When two knots are at the same place, a blend can have zero width. That blend is dropped, because its function is zero.

## The problem

The input is a degree $p \ge 0$, a knot vector $t_0 \le \cdots \le t_{n+p+1}$, an index $\mu$ with $p \le \mu \le n$ and $t_\mu < t_{\mu+1}$, and a parameter $u$ with $t_\mu \le u < t_{\mu+1}$. The output is the list of the $p + 1$ values $N_{\mu-p,p}(u), \ldots, N_{\mu,p}(u)$. All other $N_{i,p}(u)$ are zero, by the local support of B-splines.

The B-splines are defined by the recursion itself:

$$N_{i,0}(u) = \begin{cases} 1 & t_i \le u < t_{i+1}, \\ 0 & \text{otherwise}, \end{cases} \qquad N_{i,r}(u) = \omega_{i,r}(u) \, N_{i,r-1}(u) + \bigl(1 - \omega_{i+1,r}(u)\bigr) \, N_{i+1,r-1}(u),$$

$$\omega_{j,r}(u) = \frac{u - t_j}{t_{j+r} - t_j}, \qquad \text{with } \omega_{j,r} N_{j,r-1} = 0 \text{ and } (1 - \omega_{j,r}) N_{j,r-1} = 0 \text{ when } t_{j+r} = t_j.$$

The second rule is the convention $0/0 = 0$. It is consistent: $t_{j+r} = t_j$ means that the support $[t_j, t_{j+r})$ of $N_{j,r-1}$ is empty, so $N_{j,r-1}$ is the zero function, and any value of the weight gives the same product.

The index $\mu$ comes from a span search: [binary search](/binary-search/) for the $\mu$ with $t_\mu \le u < t_{\mu+1}$ costs $O(\log n)$ comparisons. At the right end $u = t_{n+1}$ of the domain, the search returns the last nonempty span $\mu$ with $t_\mu < t_{\mu+1} = t_{n+1}$, and the algorithm below is run with $u = t_{\mu+1}$. It then gives the limits from the left, which is the closed rule at the end of the domain (see [partition of unity](/partition-of-unity/)). The model is the [real RAM](/real-ram/), with exact rational arithmetic in the implementation.

## The algorithm

```pseudo id=main
BASIS-FUNCTIONS(t, p, μ, u)                  ▷ t[μ] ≤ u < t[μ+1], t[μ] < t[μ+1]
L1  N[0] ← 1                                   ▷ N_{μ,0}(u)
L2  for r ← 1 to p
L3      M[0..r] ← 0
L4      for s ← 0 to r − 1                       ▷ N[s] = N_{μ−r+1+s, r−1}(u)
L5          a ← (u − t[μ−r+1+s]) / (t[μ+1+s] − t[μ−r+1+s])
L6          M[s] ← M[s] + (1 − a) · N[s]           ▷ right part, to N_{μ−r+s, r}
L7          M[s+1] ← M[s+1] + a · N[s]             ▷ left part, to N_{μ−r+1+s, r}
L8      N ← M
L9  return N                                   ▷ N[s] = N_{μ−p+s, p}(u), s = 0..p
```

Before the pass $r$, the array $N$ holds the $r$ values of degree $r - 1$ that can be nonzero on the span. Line L5 computes the weight $a = \omega_{j,r}(u)$ of the function $N_{j,r-1}$ with $j = \mu - r + 1 + s$. The denominator is $t_{j+r} - t_j \ge t_{\mu+1} - t_\mu > 0$, because $j \le \mu$ and $j + r \ge \mu + 1$. So the triangle never divides by zero, and the $0/0$ rule is needed only for the two outer functions $N_{\mu-r,r-1}$ and $N_{\mu+1,r-1}$, which are zero at $u$ and are left out. Line L6 sends the part $(1 - a) N[s]$ to the function on the left, and line L7 sends the part $a N[s]$ to the function on the right. Each new value gets one part from each of its two neighbors, except the two outer ones, which get one part each. The weight $a$ lies in $[0, 1]$, so both parts are nonnegative.

## Example

Take $p = 2$, $t = (0, 0, 0, 1, 2, 3, 3, 3)$ and $u = 3/2$. The span is $\mu = 3$, because $t_3 = 1 \le 3/2 < 2 = t_4$.

| Pass | $s$ | $j$ | $t_j$, $t_{j+r}$ | $a$ (L5) | to $M[s]$ (L6) | to $M[s+1]$ (L7) | $N$ after L8 |
|---|---|---|---|---|---|---|---|
| start |  |  |  |  |  |  | $[1]$ |
| $r = 1$ | 0 | 3 | $1, 2$ | $1/2$ | $1/2$ | $1/2$ | $[1/2, 1/2]$ |
| $r = 2$ | 0 | 2 | $0, 2$ | $3/4$ | $1/8$ | $3/8$ |  |
| $r = 2$ | 1 | 3 | $1, 3$ | $1/4$ | $3/8$ | $1/8$ | $[1/8, 3/4, 1/8]$ |

So $N_{1,2}(3/2) = 1/8$, $N_{2,2}(3/2) = 3/4$ and $N_{3,2}(3/2) = 1/8$, and $N_{0,2}(3/2) = N_{4,2}(3/2) = 0$. The middle value $3/4$ is the sum $3/8 + 3/8$ of two parts. The three values sum to 1.

**The 0/0 rule at a triple knot.** On $t = (0, 0, 0, 1)$ with $p = 2$, the recursion gives $N_{0,2}(u) = \frac{u - 0}{0 - 0} N_{0,1}(u) + \frac{1 - u}{1 - 0} N_{1,1}(u)$. The first quotient is $0/0$, and $N_{0,1}$ lives on the empty interval $[t_0, t_2) = [0, 0)$, so the term is 0. Then $N_{1,1}(u) = 1 - u$ on $[0, 1)$, and $N_{0,2}(u) = (1 - u)^2$, the first Bernstein polynomial of degree 2.

**The right end.** On the clamped $t = (0, 0, 0, 1, 2, 2, 2)$ with $p = 2$ the domain is $[0, 2]$. At $u = 2$ the recursion as written gives $N_{i,2}(2) = 0$ for all four $i$, because no span $[t_i, t_{i+1})$ contains 2. With the closed rule the search returns $\mu = 3$, the triangle runs on $[1, 2]$ with $u = 2$, and the values are $0, 0, 0, 1$.

## Correctness

The proof is an invariant of the loop of line L2: after pass $r$, $N[s] = N_{\mu-r+s,r}(u)$ for $s = 0, \ldots, r$. It holds for $r = 0$ by line L1 and the definition of $N_{\mu,0}$. For the step, the support lemma ($N_{i,r}(u) = 0$ unless $t_i \le u < t_{i+r+1}$, by induction on $r$) shows that the only terms of the recursion that are left out are zero, and the remaining terms are the two parts of lines L6 and L7 with the weights of line L5. The value at the right end of the span follows because each value is a polynomial in $u$ on the span. The full proof is below.

## Complexity

Pass $r$ runs the inner loop $r$ times, so there are $\sum_{r=1}^{p} r = p(p + 1)/2$ steps, each with one division, two products and two sums (the product $a \cdot N[s]$ gives both parts). The time is $\Theta(p^2)$ in each case, and the extra space is two arrays of $p + 1$ numbers, $\Theta(p)$. The span search adds $O(\log n)$ comparisons. The recursion run as written, with one call for each term, makes $2^{p+1} - 1$ calls for one value when all knots are distinct $N_{i,p}(u)$, which is exponential in $p$; the triangle shares the values of each degree between neighbors.

## Properties

- **No cancellation.** Every operation forms a nonnegative combination of nonnegative numbers, so the result has a small relative error in floating point. Cox (1972) gave the rounding error analysis.
- **All lower degrees for free.** After pass $r$ the array holds the B-splines of degree $r$ on the same span. Derivative formulas use these values.
- **Partition of unity in each pass.** The two parts of each value sum to the value, so the sum of the array is the same in every pass, equal to 1. This is the proof of the [partition of unity](/partition-of-unity/) on the domain.
- **Exact with rationals.** With rational knots and parameter, every value is rational and the implementation returns it exactly.
- **Only local data.** The values depend only on the $2p$ knots $t_{\mu-p+1}, \ldots, t_{\mu+p}$.

## Variants and improvements

- **Left and right differences.** The NURBS Book (Algorithm A2.2) and de Boor's BSPLVB store the differences $u - t_{\mu+1-r}$ and $t_{\mu+r} - u$ once per pass and reuse them, which removes repeated subtractions. The number of divisions stays $p(p + 1)/2$.
- **Derivatives.** The derivative of $N_{i,p}$ is a combination of $N_{i,p-1}$ and $N_{i+1,p-1}$ with the weights $p/(t_{i+p} - t_i)$ and $-p/(t_{i+p+1} - t_{i+1})$. The NURBS Book (Section 2.3, Algorithm A2.3) computes all derivatives up to a set order from the same triangle.
- **The divided difference form.** $N_{i,p}(x) = (t_{i+p+1} - t_i) [t_i, \ldots, t_{i+p+1}] (\cdot - x)_+^p$, the definition of Curry and Schoenberg, gives the same functions. It cancels badly in floating point and is not used for computation; see [divided differences](/divided-differences/).
- **Curve points only.** When only $C(u) = \sum_i N_{i,p}(u) P_i$ is needed, the [de Boor algorithm](/de-boor-algorithm/) runs the same triangle on the control points and never forms the basis values.
- **Rational basis.** For [NURBS](/nurbs/), multiply the values by the weights $w_i$ and divide by their sum.

## When to use it

Use it when the basis values themselves are needed: to fill the rows of a collocation matrix for interpolation (see the [Schoenberg-Whitney theorem](/schoenberg-whitney-theorem/)), of a least squares matrix in [curve fitting](/curve-fitting/), or of a finite element stiffness matrix, and to evaluate a [tensor product surface](/tensor-product-surface/), where one set of values in each direction serves the whole grid of control points. For one point on one curve, the [de Boor algorithm](/de-boor-algorithm/) costs the same and needs no second pass over the control points. For a polynomial of one piece, in Bernstein form, the [de Casteljau algorithm](/de-casteljau-algorithm/) is the special case.

## Pitfalls

- **Division by zero at repeated knots.** A program that codes the recursion formula directly must test each denominator $t_{j+r} - t_j$ and skip the term when it is zero. Without the test, a knot vector with an end knot of multiplicity $p + 1$ gives $0/0$ and a NaN in [IEEE 754](/ieee-754/) arithmetic.
- **An empty span.** Line L5 divides by $t_{\mu+1+s} - t_{\mu-r+1+s}$, which is positive only when $t_\mu < t_{\mu+1}$. A span search that returns the first $i$ with $t_i \le u$, and not the last, can return an empty span at a repeated knot, and line L5 then divides by zero in pass $r = 1$.
- **The right end of a clamped vector.** With half-open spans no span contains $u = t_{n+1}$ when that knot has multiplicity $p + 1$, so the definition gives all zeros and the curve point $(0, 0)$. The span search must return the last nonempty span for this $u$; line L1 then sets $N_{\mu,0} = 1$ at the closed end.
- **The parameter outside the domain.** For $u < t_p$ or $u > t_{n+1}$, fewer than $p + 1$ B-splines exist on the span, and the values sum to less than 1. On the uniform knots $0, 1, \ldots, 6$ with $p = 2$ the sum is $1/8$ at $u = 1/2$.
- **Exponential recursion.** Code that calls itself for each term of the recursion makes $2^{p+1} - 1$ calls for one value when the knots are distinct, and $p + 1$ times as many for the whole set. Use the triangle.

## Implementations

## History

Maurice Cox and Carl de Boor published the recurrence in 1972 in two independent papers, Cox in the Journal of the Institute of Mathematics and its Applications and de Boor in the Journal of Approximation Theory. The recurrence replaced the divided difference definition of Curry and Schoenberg (1966) for computation, because that definition loses accuracy in floating point. Cox studied the rounding errors of the recurrence and showed that it is stable. De Boor used it in the evaluation of a B-spline series, the [de Boor algorithm](/de-boor-algorithm/), and later in the routine BSPLVB of his book. The NURBS Book (1995, second edition 1997) gives the same triangle as its routine BasisFuns.

## References
