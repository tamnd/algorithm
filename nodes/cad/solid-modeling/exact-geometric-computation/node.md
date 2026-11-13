---
tag: SZ8S1M
kind: technique
slug: exact-geometric-computation
name: Exact geometric computation
aliases:
- EGC paradigm
area: cad/solid-modeling
level: advanced
summary: Yap's approach that evaluates every geometric predicate exactly, with filters and adaptive precision, so the combinatorial output is always correct.
prereqs: [geometric-robustness-problem, orientation-test, arbitrary-precision-arithmetic, interval-arithmetic]
see_also: [simulation-of-simplicity, shewchuk-expansion-sum, constant-problem, big-integer, catastrophic-cancellation, homogeneous-coordinates, mesh-boolean-operations, boundary-evaluation]
sources:
  - paper: doi:10.1016/0925-7721(95)00040-2
    title: Chee K. Yap, Towards exact geometric computation, Computational Geometry 7(1-2), 3 to 23, 1997
    locator: the whole paper (the principle that every branch of a geometric program is decided exactly, the separation of predicates from constructions, and the use of filters and separation bounds)
  - paper: "Chee K. Yap and Thomas Dubé, The exact computation paradigm, in Ding-Zhu Du and Frank Hwang (eds.), Computing in Euclidean Geometry, 2nd edition, Lecture Notes Series on Computing 4, World Scientific, 1995, ISBN 9789814501637"
    locator: pages 452 to 492 (exact computation, its cost, and the tools of filters and precision bounds)
  - paper: doi:10.1007/PL00009321
    title: Jonathan Richard Shewchuk, Adaptive precision floating-point arithmetic and fast robust geometric predicates, Discrete and Computational Geometry 18(3), 305 to 363, 1997
    locator: the whole paper (expansion arithmetic, the adaptive orientation and in-circle predicates, and their error bounds)
  - paper: "Steven Fortune and Christopher J. Van Wyk, Static analysis yields efficient exact integer arithmetic for computational geometry, ACM Transactions on Graphics 15(3), 223 to 248, 1996"
    locator: the whole paper (static floating-point filters with error bounds computed from the bit length of the integer input)
  - paper: doi:10.1016/j.comgeo.2007.06.003
    title: Lutz Kettner, Kurt Mehlhorn, Sylvain Pion, Stefan Schirra and Chee Yap, Classroom examples of robustness problems in geometric computations, Computational Geometry 40(1), 61 to 78, 2008
    locator: the whole paper (failures of float predicates, which exact predicates remove)
---

Exact geometric computation (EGC) is Yap's approach to the [geometric robustness problem](/geometric-robustness-problem/). It does not ask that every number of a geometric program be exact. It asks that every *decision* be exact: each predicate that chooses a branch returns the sign that it has on the real input. The combinatorial part of the output, which vertex is on which edge and which face bounds which solid, is then the exact one, and the numbers can be rounded at the end. EGC is made fast by floating-point filters that decide most signs in hardware arithmetic, and by exact or adaptive arithmetic for the few signs that the filter cannot decide.

## In plain words

A geometric program makes two kinds of steps. Some steps compute numbers, such as the point where two lines cross. Other steps ask a yes or no question, such as "is this point to the left of that line?", and the answer decides what the program does next.

Errors in the numbers make the picture a little wrong. Errors in the answers make the picture impossible. This approach keeps the answers always right and lets the numbers be a little wrong.

To keep the answers right, the program first tries fast rounded arithmetic and also computes how large the rounding error can be. If the answer is far from zero compared with that error, it is safe. Only when it is too close does the program compute again with more digits, or exactly. Most questions are safe on the first try.

## When it applies

- **The predicates are algebraic.** Each decision is the sign of an expression built from the input by $+$, $-$, $\times$, $/$ and roots. Then the exact sign can be found in finite time. Polyhedral modeling, convex hulls, Delaunay triangulations and planar arrangements are of this kind. A rotation by an angle given in degrees, or an offset of a curved surface, is not, and deciding the sign of a general expression with $\exp$ or $\sin$ is the open [constant problem](/constant-problem/).
- **The input is taken as exact.** The program treats each input double as the exact rational number that it stores. EGC then gives the exact output for that input, not for the decimal values that a designer typed.
- **The algorithm is correct in the [real RAM](/real-ram/).** EGC does not change the algorithm. It makes the predicates behave as the proof assumes, so the proof applies.
- **The degenerate cases are handled.** An exact sign can be $0$. The algorithm must handle the zero cases, or [simulation of simplicity](/simulation-of-simplicity/) must turn them into consistent nonzero signs. EGC and SoS are two separate layers: EGC makes the zero signs exact, and SoS removes them.

## The template

A predicate is the sign of an expression $E$, given as a tree or a directed acyclic graph over the input numbers and the numbers of constructed objects. The program keeps the expression of each constructed number, not only its float value, so it can evaluate it again with more precision.

```pseudo id=main
EGC-SIGN(E)                                    ▷ the sign of an algebraic expression
L1  (v, e) ← float value of E and a bound on its error, both in double precision
L2  if |v| > e then return sign(v)            ▷ the filter: most calls end here
L3  b ← a separation bound for E: if E ≠ 0 then |E| ≥ b
L4  p ← 106                                    ▷ bits of precision
L5  loop
L6      (v, e) ← value of E and its error bound at p bits, by interval or big-float arithmetic
L7      if |v| > e then return sign(v)
L8      if |v| + e < b then return 0          ▷ E is too small to be nonzero
L9      p ← 2p
```

For an expression that uses only $+$, $-$ and $\times$ on integer or float input, L3 to L9 can be one exact evaluation with [big integers](/big-integer/) or with the expansions of [Shewchuk's expansion sum](/shewchuk-expansion-sum/), and the sign of the exact value is the answer.

**Why the answer is exact.** If L2 or L7 returns, then the true value lies in $[v - e, v + e]$, and this interval does not contain $0$, so the sign of $v$ is the sign of $E$. If L8 returns, then $|E| \le |v| + e < b$, and a nonzero $E$ has $|E| \ge b$, so $E = 0$. The loop ends: as $p$ grows, $e \to 0$, so either $|v| > e$ for a nonzero $E$, or $|v| + e < b$ for $E = 0$.

**The cost.** On input without near degeneracies, almost all calls end at L2, and the program runs at close to the speed of plain floating point. The cost of the other calls depends on the degree of $E$. The orientation test on integers of $b$ bits needs at most $2b + 3$ bits. A vertex of a solid computed as the meeting point of three planes, whose planes come from vertices, has an expression of much higher degree, and its exact value has many more bits. This growth along chains of constructions is the main cost of EGC in solid modeling.

**Example.** The segments from $(0, 0)$ to $(1, 1)$ and from $(0, 1)$ to $(1, -1)$ cross at $x = (1/3, 1/3)$. The crossing has the form $x = (N_x / \delta, N_y / \delta)$ with integers $N_x$, $N_y$ and $\delta = (b - a) \times (d - c) = -3$. The float formula gives $(0.3333333333333333, 0.3333333333333333)$. Now test $x$ against the line through $e = (1, 0)$ and $f = (-1, 1)$, which passes exactly through $(1/3, 1/3)$.

- *Float.* The orientation $D(e, f, x)$ evaluates to $+1.11 \times 10^{-16}$, a left turn. This is wrong.
- *L1 and L2.* The error bound of the whole computation, which includes the rounding of $x$, is about $6 \times 10^{-16}$, larger than $|v|$. The filter cannot decide.
- *L3.* $D(e, f, x)$ is linear in $x$, and $e$, $f$ are integers, so $D = M / \delta$ for an integer $M$. If $D \ne 0$, then $|D| \ge 1/|\delta| = 1/3$. This is the separation bound $b = 1/3$.
- *L8.* $|v| + e < 10^{-15} < 1/3$, so $D = 0$: the three lines meet in one point. An evaluation with exact rationals gives the same result.

For the other test lines the filter decides at once. The line from $(7, -2)$ to $(-2, 1)$ misses $x$, and both the float value and the exact value have the sign $-1$.

## Classic examples

- **Adaptive predicates.** Shewchuk's orientation and in-circle predicates evaluate a float approximation with a proved error bound, and then refine with expansion arithmetic in stages, each stage exact up to a smaller bound. The [orientation test](/orientation-test/) page shows the filter and its effect on a grid of near-collinear points.
- **Static filters for integer input.** Fortune and Van Wyk compute the error bound of each predicate once, from the bit length of the integer input, so the filter costs one comparison. A program that fails the filter switches to exact integer arithmetic.
- **Exact predicates and inexact constructions.** Geometry libraries offer kernels that decide all predicates on the input exactly but return constructed points as doubles. This is enough for algorithms that never test constructed points, such as convex hulls and Delaunay triangulations of the input points.
- **Exact constructions.** For Booleans, the cut points are input to later predicates. Libraries keep them as exact rationals in [homogeneous coordinates](/homogeneous-coordinates/), or as lazy expression graphs that are evaluated with more precision only when a filter fails. Exact [mesh Boolean operations](/mesh-boolean-operations/) are built in this way.
- **Polyhedral Booleans.** With exact rational planes and points, [boundary evaluation](/boundary-evaluation/) decides each side test and each coplanarity exactly, and the degenerate cases, such as touching and coplanar faces, become exact zeros that the algorithm handles by rule.

## Variations

- **Exact arithmetic only.** Evaluate all predicates with rationals or big integers and no filter. This is simple and correct. It is much slower than a filter, but it is adequate for small models and for tests.
- **Dynamic filters.** Compute the error bound at run time with [interval arithmetic](/interval-arithmetic/). This adapts to input of any size but costs more per operation than a static bound.
- **Separation bounds for roots.** For expressions with square roots and roots of polynomials, the separation bound of L3 comes from the degree and the size of the coefficients of the expression. Exact number libraries compute such bounds as they build the expression, and they decide signs with L5 to L9.
- **Rounding of the output.** After the exact computation, the constructed points can be rounded to doubles for storage. Rounding can again move a vertex to the wrong side of a face, so a rounding step that keeps the topology valid is a separate problem.

## Pitfalls

- **Exactness of the input.** The double nearest to $0.1$ is not $0.1$. Two faces that a designer meant to be coplanar can have planes from input doubles that differ in the last bit, and EGC then correctly reports a sliver. An exact program on slightly wrong input gives an exact answer to the wrong question.
- **Growth of the numbers.** Each construction that feeds another construction multiplies the degree. A long chain of Booleans on exact rationals can have numbers with thousands of bits. Rounding between operations stops the growth but loses the exactness for the next operation.
- **A filter with a wrong bound.** The error bound must cover every rounding of the float evaluation, including the rounding of the constructed points used in it. A bound for the last subtraction only ignores the error of the constructed point. It is too small in general, and the filter then returns wrong signs.
- **Nonalgebraic operations.** Trigonometric functions, exponentials and numerical surface intersections have no general separation bound. EGC applies to them only through approximations with a tolerance, which is outside the approach.
- **Zero is still a sign.** EGC makes the degenerate cases exact. It does not remove them. A program that crashes on an exact $0$ still crashes.

## Exercises

1. Prove that for integer inputs of at most $b$ bits, the orientation determinant fits in $2b + 3$ bits, and give an input that needs all of them.
2. For the crossing point $x = (N_x / \delta, N_y / \delta)$ of two segments with integer end points, show that the orientation of two integer points and $x$ is an integer divided by $\delta$, and derive the separation bound $1/|\delta|$.
3. Give a forward error bound for the float value of $D(e, f, x)$ in the example, where $x$ is computed by the float formula, and check that it is below $10^{-15}$.
4. A filter compares $|v|$ with $c \cdot u \cdot M$, where $M$ is the sum of the absolute values of the products. Show by an example why the comparison must be $|v| > e$ and not $|v| \ge e$.
5. Estimate the number of bits of a vertex of a polyhedron that is computed from three planes, where each plane comes from three vertices with $b$-bit integer coordinates.

## References
