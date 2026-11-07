---
tag: S6W6AA
kind: algorithm
slug: vincent-collins-akritas
name: Vincent-Collins-Akritas algorithm
aliases:
- VCA
- VCA algorithm
- Vincent-Collins-Akritas isolation
- continued fraction real root isolation
- Descartes method
- Collins-Akritas algorithm
area: algebra/polynomial-arithmetic
level: advanced
summary: Isolates real roots by repeated Descartes-sign counts and Mobius transformations of the interval.
solves: [real-root-isolation]
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of f, L: the number of binary digits of the largest absolute value of a coefficient of f}
  time: {worst: O(n^3 (L + log n))}
  space: {extra: O(n^2 (L + log n))}
  tree_size: {worst: O(n (L + log n))}
  bit_time: {worst: O(n^5 (L + log n)^2)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [real-root-isolation, descartes-rule-of-signs, vincent-theorem]
see_also: [vincent-theorem, descartes-rule-of-signs, real-root-isolation, sturm-theorem, sturm-sequence, cauchy-root-bound, continued-fraction, bisection-method]
sources:
  - paper: doi:10.1145/800205.806346
    title: George E. Collins and Alkiviadis G. Akritas, Polynomial real root isolation using Descartes' rule of signs, SYMSAC 1976
    locator: pp. 272 to 275
  - paper: doi:10.1145/1145768.1145786
    title: Arno Eigenwillig, Vikram Sharma and Chee K. Yap, Almost tight recursion tree bounds for the Descartes method, ISSAC 2006
    locator: Section 2.1 (procedure Descartes), Corollary 3.5 (tree size), Theorems 4.1 and 4.2 (bit complexity)
  - paper: doi:10.1016/j.jsc.2005.02.004
    title: Werner Krandick and Kurt Mehlhorn, New bounds for the Descartes method, Journal of Symbolic Computation 41(1), 2006
    locator: pp. 49 to 66
  - paper: doi:10.1016/j.cam.2003.08.015
    title: Fabrice Rouillier and Paul Zimmermann, Efficient isolation of polynomial's real roots, Journal of Computational and Applied Mathematics 162(1), 2004
    locator: pp. 33 to 50
  - url: https://www.numdam.org/item/JMPA_1836_1_1__341_0/
    title: Alexandre Joseph Hidulphe Vincent, Note sur la résolution des équations numériques, Journal de Mathématiques Pures et Appliquées, first series, volume 1, 1836
    locator: pp. 341 to 372
  - paper: doi:10.15388/na.2008.13.3.14557
    title: Alkiviadis G. Akritas, Adam W. Strzeboński and Panagiotis S. Vigklas, Improving the performance of the continued fractions method using new bounds of positive roots, Nonlinear Analysis, Modelling and Control 13(3), 2008
    locator: pp. 265 to 279
  - paper: doi:10.1016/j.jsc.2015.03.004
    title: Michael Sagraloff and Kurt Mehlhorn, Computing real roots of real polynomials, Journal of Symbolic Computation 73, 2016
    locator: pp. 46 to 86
  - paper: doi:10.1145/258726.258745
    title: Joachim von zur Gathen and Jürgen Gerhard, Fast algorithms for Taylor shifts and certain difference equations, ISSAC 1997
    locator: pp. 40 to 47
---

The Vincent-Collins-Akritas algorithm isolates the real roots of a square-free integer polynomial: it returns disjoint intervals, each with exactly one root. It starts with an interval that holds all real roots, maps it onto the positive half-line by a Möbius transformation, and counts the sign changes of the coefficients with [Descartes' rule of signs](/descartes-rule-of-signs/). A count of $0$ or $1$ is exact; a larger count makes the algorithm split the interval in two and repeat. [Vincent's theorem](/vincent-theorem/) shows that short intervals always give $0$ or $1$, so the bisection stops. This page treats the bisection form of Collins and Akritas, also called the Descartes method; the continued fraction form is a variant.

## In plain words

To find where the real roots of a polynomial are, start with an interval that is sure to hold all of them. Change the variable so that this interval becomes the set of all positive numbers, and count how often the signs of the new coefficients change. If they never change, the interval holds no root, so drop it. If they change once, it holds exactly one root, so keep it as an answer. Otherwise cut the interval in half and check each half the same way. The count can be too large, but only for long intervals: once the pieces are short compared with the gaps between the roots, the count is zero or one. All the work is with whole numbers.

## The problem

**Input.** A square-free polynomial $f = \sum_{i=0}^{n} f_i x^i \in \mathbb{Z}[x]$ of degree $n \ge 1$. Square-free means no repeated complex root, that is, $\gcd(f, f') = 1$; for other inputs, divide by $\gcd(f, f')$ first, as the implementation does in `isolate_real_roots`.

**Output.** A sorted list of disjoint items, one for each real root of $f$. Each item is either an open interval with rational endpoints that holds exactly one root, or a rational point that is a root.

The coefficients are integers; the algorithm needs only an ordered ring for its arithmetic, and rational inputs are made integral by clearing denominators. The model is the algebraic one: each addition, multiplication by a power of two, and sign test of an integer is one step. The bit cost, with schoolbook integer arithmetic, is given separately in the Complexity section. $L$ is the number of binary digits of $\max_i |f_i|$.

## The algorithm

For a list of numbers, $\operatorname{Var}$ is the number of sign changes after the zeros are removed. The entry $(A, c, k)$ of the work list stands for the interval $I(c, k) = (-B + c\, h_k,\ -B + (c + 1)\, h_k)$ with $h_k = 2B/2^k$, and the roots of $A$ in $(0, 1)$ are the images of the roots of $f$ in $I(c, k)$ under an affine map.

```pseudo id=main
VCA(f)                               ▷ f ∈ Z[x] square-free, deg f = n ≥ 1
L1  B ← the least power of two with B ≥ 1 + max_{i<n} |f_i| / |f_n|
L2  A ← f(2B·x − B)                  ▷ roots of A in (0, 1) ↔ roots of f in (−B, B)
L3  S ← a stack holding (A, 0, 0);  out ← [ ]
L4  while S is not empty do
L5      (A, c, k) ← pop(S)
L6      v ← Var of the coefficients of (x + 1)^n · A(1/(x + 1))
L7      if v = 0 then continue
L8      if v = 1 then append I(c, k) to out; continue
L9      A_L ← 2^n · A(x/2);  A_R ← A_L(x + 1)
L10     if A_R(0) = 0 then append the midpoint of I(c, k) to out
L11     push (A_R, 2c + 1, k + 1) and then (A_L, 2c, k + 1) onto S
L12 return out, sorted
```

Line L1 is [Cauchy's root bound](/cauchy-root-bound/), rounded up to a power of two so that all endpoints are dyadic rationals. Line L2 is a Taylor shift by $-1$ and two scalings. Line L6 reverses the coefficient list and applies a Taylor shift by $1$; the result is a positive multiple of $(x + 1)^n f\big((u x + u + h_k)/(x + 1)\big)$ for $I(c, k) = (u, u + h_k)$, the Möbius transformation that sends $(0, \infty)$ onto the interval. Line L9 halves the interval: $A_L$ covers the left half and $A_R$ the right half. Line L10 catches a root at the midpoint, which neither open half contains. The stack replaces recursion, and pushing the right half first makes the left half come out first.

## Example

Let $f = x^3 - 7x + 7$, with roots near $-3.0489$, $1.3569$ and $1.6920$. The two positive roots are only $0.335$ apart.

- **L1.** $1 + \max(7, 7, 0) = 8$, so $B = 8$ and the start interval is $(-8, 8)$.
- **L2.** $A = f(16x - 8) = 4096x^3 - 6144x^2 + 2960x - 449$.
- **L6, first pass.** $(x + 1)^3 A(1/(x + 1)) = 463 - 1571x + 1613x^2 - 449x^3$, with signs $+, -, +, -$, so $v = 3$: the three real roots are all in $(-8, 8)$, as they must be.

The passes, in the order the stack gives them:

| interval | $v$ | action |
|---|---|---|
| $(-8, 8)$ | 3 | split at $0$, not a root |
| $(-8, 0)$ | 1 | output |
| $(0, 8)$ | 2 | split at $4$ |
| $(0, 4)$ | 2 | split at $2$ |
| $(0, 2)$ | 2 | split at $1$ |
| $(0, 1)$ | 0 | drop |
| $(1, 2)$ | 2 | split at $3/2$ |
| $(1, 3/2)$ | 1 | output |
| $(3/2, 2)$ | 1 | output |
| $(2, 4)$ | 0 | drop |
| $(4, 8)$ | 0 | drop |

The output is $(-8, 0)$, $(1, 3/2)$, $(3/2, 2)$. The counts $v = 2$ on $(0, 8)$, $(0, 4)$ and $(0, 2)$ are exact, since each of these holds both positive roots; the count $v = 2$ on $(1, 2)$ is exact too. The tests check this output.

## Correctness

Every work list entry $(A, c, k)$ satisfies $A(x) = \lambda f(u + h_k x)$ with $\lambda > 0$, where $I(c, k) = (u, u + h_k)$; line L2 starts this, and line L9 keeps it for both halves. So the polynomial of line L6 is a positive multiple of the Möbius transform of $f$ for $I(c, k)$, whose positive roots are the roots of $f$ in $I(c, k)$. By Descartes' rule, $v$ is at least the number of these roots and has the same parity, so $v = 0$ means no root and $v = 1$ means exactly one. The intervals on the stack, the items of the output, and the dropped intervals always partition $(-B, B)$ up to the midpoints that are not roots, and Cauchy's bound puts every real root in $(-B, B)$. So each root is reported exactly once. The loop ends because, by part 3 of [Vincent's theorem](/vincent-theorem/), an interval of length at most $\operatorname{sep}(f)/\sqrt 3$ always gives $v \le 1$, where $\operatorname{sep}(f)$ is the least distance between two roots of $f$; so the depth of the work list is at most $\lceil \log_2(2\sqrt 3\, B/\operatorname{sep}(f)) \rceil$. The full proof is below.

## Complexity

The cost model is the algebraic one stated in The problem. Each pass of the loop does a reversal and a Taylor shift in line L6, $n$ shifts and a Taylor shift in line L9, and $O(n)$ sign tests. The classical Taylor shift by $\pm 1$ takes $n(n+1)/2$ additions. So each pass costs $O(n^2)$ steps.

- **Tree size.** Eigenwillig, Sharma and Yap (2006, Corollary 3.5) prove that the recursion tree of this method has $O(n(L + \log n))$ nodes for a square-free integer polynomial with coefficients less than $2^L$ in absolute value, and that the bound is tight for $L = \Omega(\log n)$. The proof uses the two-circle theorem of Vincent's theorem and the Davenport-Mahler bound on products of root distances.
- **Time.** Hence $O(n^2) \cdot O(n(L + \log n)) = O(n^3(L + \log n))$ steps in the worst case, plus $O(n^2)$ for lines L1 and L2. This follows from the cited tree bound and the count above.
- **Space.** The stack holds at most one waiting sibling for each level, so at most the depth plus one entries, each with $n + 1$ integers. The depth is at most the tree size, which gives $O(n^2 (L + \log n))$ integers. This is a proved upper bound but a loose one; for typical inputs the depth is much smaller.
- **Bit cost.** The integers grow by about $n$ binary digits per level. Eigenwillig, Sharma and Yap (Theorem 4.1) prove a bit cost of $O(n^5 (L + \log n)^2)$ with classical arithmetic, using only additions and shifts after the first transformation, and (Theorem 4.2) a better bound with a fast Taylor shift.
- **Observed.** On random polynomials the tree is far smaller than the worst case, since few real roots are close together. Rouillier and Zimmermann (2004) report efficient implementations with memory-saving variants of the transformations.

## Properties

- **Exact.** Integer arithmetic only; the answer is certified, not approximate.
- **Deterministic and iterative.** No random choices; an explicit stack replaces recursion.
- **Output.** Intervals with dyadic rational endpoints, and exact dyadic roots when a midpoint is a root. Endpoints of output intervals may be roots that are also reported as points; the open intervals never contain them.
- **Needs square-free input.** A repeated root gives $v \ge 2$ on every interval around it, so the loop would not end. The implementation checks this and raises an error.
- **Counts are upper bounds.** Unlike a [Sturm](/sturm-theorem/) count, the value $v$ can exceed the true count for long intervals, by an even number; this only costs extra splits.
- **No remainder sequence.** The method needs no [Sturm sequence](/sturm-sequence/) and no polynomial division, only Taylor shifts.

## Variants and improvements

- **Continued fraction form (VAS).** Vincent's original method follows the [continued fraction](/continued-fraction/) of each root: it substitutes $x = a + 1/y$ with integers $a$ given by a lower bound on the positive roots, and part 4 of Vincent's theorem shows that the counts reach $0$ or $1$. Akritas, Strzeboński and Vigklas (2008) use good lower bounds for the positive roots, and this variant is often faster than bisection in practice.
- **Bernstein basis.** The same method in the Bernstein basis replaces Taylor shifts by de Casteljau subdivision; Eigenwillig, Sharma and Yap treat both bases in one framework.
- **Fast Taylor shift.** Von zur Gathen and Gerhard (1997) give Taylor shifts with fast multiplication, which improves the bit cost, as in Theorem 4.2 of Eigenwillig, Sharma and Yap.
- **Memory-efficient variants.** Rouillier and Zimmermann (2004) keep the polynomial of the current interval and move between intervals by transformations, instead of storing a polynomial for each waiting interval.
- **Newton steps.** Sagraloff and Mehlhorn (2016) combine the Descartes test with Newton iteration and approximate arithmetic, which gives near-optimal bounds and handles real coefficients given by approximations.
- **Refinement.** Once a root is isolated, the interval can be shrunk by [bisection](/bisection-method/) on the sign of $f$, or by faster methods such as Newton steps on the isolated root.

## When to use it

Use the Descartes method to isolate the real roots of an integer or rational polynomial of moderate degree, when exact and certified intervals are needed, as in computer algebra and [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/). It is usually faster than Sturm bisection because it avoids the remainder sequence and its large coefficients. For polynomials of high degree with many close roots, or for all complex roots, numerical methods with certification are faster. When the number of roots is all that is needed, a single Sturm count gives it exactly.

## Pitfalls

- **Repeated roots.** Without the square-free reduction, the loop does not end on an input such as $x^2$.
- **Zeros in the count.** Zero coefficients must be skipped when counting sign changes in line L6, not counted as changes. The transformed lists often have zeros, for example at an endpoint that is a root.
- **Midpoint roots.** A root at a midpoint is in neither open half. Without line L10 it is lost.
- **Root bound.** Any valid bound works, but it must be strict: a root at $\pm B$ would be lost, because the intervals are open. Cauchy's bound is strict.
- **Floating point.** Sign tests of Taylor-shifted coefficients are unreliable in floating point; the coefficients can be large and cancel. Use exact integers.
- **Deep recursion.** A recursive version recurses once per bisection level, and inputs with very close roots, such as Mignotte's polynomials $x^n - 2(ax - 1)^2$ with large $a$, need many levels. An explicit stack avoids the recursion limit.

## Implementations

## History

Vincent (1836) separated the real roots of a polynomial with continued fraction substitutions and the sign-change count, and proved that the method stops. Collins and Akritas (1976) replaced the continued fractions by bisection of an interval and gave the algorithm in its modern form. Krandick and Mehlhorn (2006) and Eigenwillig, Sharma and Yap (2006) proved the bounds on the recursion tree; the second paper gives the bound $O(n(L + \log n))$, which is the same as the best known bound for Sturm bisection. Akritas, Strzeboński and Vigklas (2008) improved the continued fraction variant, and Sagraloff and Mehlhorn (2016) gave a variant with near-optimal bit cost.

## References
