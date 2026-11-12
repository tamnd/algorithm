---
tag: JDHTCP
kind: algorithm
slug: b-spline-fitting
name: B-spline least-squares fitting
aliases:
- least-squares B-spline approximation
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Fit the control points of a B-spline curve with a fixed degree and knot vector to many data points by linear least squares. The normal equations are banded and are solved in time linear in the data.
solves: [curve-fitting]
model: real-ram
complexity:
  vars: {m: "the number of data points, minus one", n: "the number of control points, minus one", p: the degree, d: the dimension of the points}
  time: {worst: "O((m + n) p^2 + (m + n) p d)"}
  space: {extra: "O(n p + n d)"}
properties: {deterministic: true, recursive: false, local: false, interpolating: false}
history:
  year: 1968
  people: [Carl de Boor, John R. Rice]
  note: De Boor and Rice described least-squares cubic spline approximation with fixed knots in a Purdue report of 1968. Piegl and Tiller gave the curve form with chord-length parameters and averaged knots used in CAD.
prereqs: [b-spline, knot-vector, least-squares-problem]
see_also: [normal-equations, schoenberg-whitney-theorem, cox-de-boor-recursion, curve-interpolation, smoothing-spline, qr-decomposition, curve-fitting, natural-cubic-spline]
sources:
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 9.4, Global Approximation (page 405), Section 9.4.1, Least Squares Curve Approximation (page 410), Section 9.4.2, Weighted and Constrained Least Squares Curve Fitting, and Section 9.4.4, Approximation to Within a Specified Accuracy
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter XIV, Smoothing and Least-Squares Approximation (least-squares approximation by splines with fixed knots and the banded normal equations)
  - book: isbn:9780898713602
    title: Åke Björck, Numerical Methods for Least Squares Problems, SIAM, 1996
    locator: Chapter 6, Direct methods for sparse problems (banded least squares problems)
---

B-spline least-squares fitting finds the control points of a [B-spline](/b-spline/) curve that pass closest to a set of data points, in the sense of the sum of squared distances. The degree $p$, the [knot vector](/knot-vector/) and a parameter value for each data point are fixed in advance. Then the curve is linear in its control points, and the fit is a linear [least squares problem](/least-squares-problem/). Each data point touches only $p + 1$ basis functions, so the [normal equations](/normal-equations/) have a band matrix of half bandwidth $p$. A band $LDL^T$ factorization solves them in $O((m + n) p^2)$ time for $m + 1$ data points and $n + 1$ control points, plus $O((m + n)pd)$ for the $d$ coordinates. The solution exists and is unique exactly when some increasing choice of $n + 1$ sites satisfies the Schoenberg-Whitney condition.

## In plain words

You have many measured points, for example a few hundred points from a scanner along the edge of a part, and they are noisy. A curve that passes through all of them would wiggle. You want a smooth curve with only a few control points that runs close to all of them.

First you decide the shape of the curve family: the degree and where the pieces join. You also give each measured point a time along the curve. After that, each curve point at a given time is a fixed mix of the control points. So "how far is the curve from the data" is a sum of squares of simple linear expressions, and you find its minimum by solving one linear system. Each point mixes only a few neighbouring control points, so this system is narrow and quick to solve.

## The problem

**Input.** Data points $Q_0, \dots, Q_m \in \mathbb{R}^d$; parameters $t_0 \le t_1 \le \dots \le t_m$; a degree $p \ge 0$; a nondecreasing knot vector $U = (u_0, \dots, u_{n+p+1})$ with $n + p + 2$ knots, usually clamped ($u_0 = \dots = u_p$ and $u_{n+1} = \dots = u_{n+p+1}$), with every $t_k$ in $[u_p, u_{n+1}]$.

**Output.** Control points $P_0, \dots, P_n$ that minimize

$$F(P) = \sum_{k=0}^{m} \left\lVert Q_k - C(t_k) \right\rVert^2, \qquad C(t) = \sum_{i=0}^{n} N_{i,p}(t)\, P_i,$$

where $N_{i,p}$ are the B-splines of degree $p$ on $U$ (see [Cox-de Boor recursion](/cox-de-boor-recursion/)).

In matrix form, let $N$ be the $(m + 1) \times (n + 1)$ collocation matrix with $N_{ki} = N_{i,p}(t_k)$, and let $\mathbf{Q}$ and $\mathbf{P}$ be the matrices with the points as rows. Then $F = \lVert \mathbf{Q} - N \mathbf{P} \rVert_F^2$, and the $d$ columns are $d$ independent least squares problems with the same matrix $N$. This is an instance of [curve fitting](/curve-fitting/).

## The algorithm

FIND-SPAN returns the index $s$ with $u_s \le t < u_{s+1}$ (and $s = n$ at the right end). The $p + 1$ basis functions that can be nonzero at $t$ are $N_{s-p,p}, \dots, N_{s,p}$, and the triangular Cox-de Boor scheme computes them in $O(p^2)$ operations.

```pseudo id=main
BSPLINE-FIT(Q[0 .. m], t[0 .. m], U, p)       ▷ n + 1 = |U| − p − 1 control points
L1  A ← zero (n + 1) × (n + 1) band matrix, half bandwidth p; R ← n + 1 zero vectors
L2  for k ← 0 to m do
L3      s ← FIND-SPAN(U, p, t_k); (B_0, …, B_p) ← (N_{s−p,p}(t_k), …, N_{s,p}(t_k))
L4      for a, b ← 0 to p do A[s − p + a, s − p + b] ← A[s − p + a, s − p + b] + B_a B_b
L5      for a ← 0 to p do R[s − p + a] ← R[s − p + a] + B_a Q_k
L6  factor A = L D Lᵀ, L unit lower triangular with band p   ▷ stop if a pivot is 0
L7  solve L y = R, then D z = y, then Lᵀ P = z; return P
```

Lines L1 to L5 build $A = N^T N$ and $R = N^T \mathbf{Q}$ one data point at a time, without storing $N$. Line L6 is the band form of the factorization $A = LDL^T$: for $i = 0, \dots, n$ and $\max(0, i - p) \le j \le i$,

$$D_i = A_{ii} - \sum_{k = \max(0, i-p)}^{i-1} L_{ik}^2 D_k, \qquad L_{ij} = \frac{1}{D_j}\Big(A_{ij} - \sum_{k = \max(0, i-p)}^{j-1} L_{ik} L_{jk} D_k\Big) \ (j < i).$$

It uses no square roots, so exact rational input gives the exact minimizer. Line L7 is a forward and a backward substitution of band $p$.

## Example

**A trace with exact numbers.** Take degree $p = 1$ and the knots $U = (0, 0, \tfrac12, 1, 1)$, so $n = 2$ and the three basis functions are hats: $N_0$ falls from 1 to 0 on $[0, \tfrac12]$, $N_1$ peaks at $\tfrac12$, $N_2$ rises on $[\tfrac12, 1]$. The data are $Q = (0, 0), (1, 2), (2, 2), (3, 1), (4, 0)$ at $t = 0, \tfrac14, \tfrac12, \tfrac34, 1$.

| $k$ | $t_k$ | span $s$ | $(B_0, B_1)$ | entries of $A$ that grow |
|---|---|---|---|---|
| 0 | 0 | 1 | (1, 0) | $A_{00} \mathrel{+}= 1$ |
| 1 | 1/4 | 1 | (1/2, 1/2) | $A_{00}, A_{01}, A_{11} \mathrel{+}= 1/4$ |
| 2 | 1/2 | 2 | (1, 0) | $A_{11} \mathrel{+}= 1$ |
| 3 | 3/4 | 2 | (1/2, 1/2) | $A_{11}, A_{12}, A_{22} \mathrel{+}= 1/4$ |
| 4 | 1 | 2 | (0, 1) | $A_{22} \mathrel{+}= 1$ |

After L5,

$$A = \begin{pmatrix} 5/4 & 1/4 & 0 \\ 1/4 & 3/2 & 1/4 \\ 0 & 1/4 & 5/4 \end{pmatrix}, \qquad R = \begin{pmatrix} (1/2, 1) \\ (4, 7/2) \\ (11/2, 1/2) \end{pmatrix}.$$

Line L6 gives $D_0 = 5/4$, $L_{10} = 1/5$, $D_1 = 29/20$, $L_{21} = 5/29$, $D_2 = 35/29$. Line L7 gives, for the $y$ coordinate, $y = (1, 33/10, -2/29)$, $z = (4/5, 66/29, -2/35)$ and finally

$$P_0 = (0, \tfrac{12}{35}), \qquad P_1 = (2, \tfrac{16}{7}), \qquad P_2 = (4, -\tfrac{2}{35}).$$

The $x$ data lie on the line $x = 4t$, which is in the spline space, so the $x$ coordinates are reproduced exactly. The $y$ residuals are $-\tfrac{12}{35}, \tfrac{24}{35}, -\tfrac27, -\tfrac4{35}, \tfrac2{35}$, with the sum of squares $\tfrac{24}{35} \approx 0.686$. The fitted curve does not pass through the first and the last data point.

**A cubic fit in floating point.** Take the 11 points $(x, (x - 5)^2/5)$ for $x = 0, \dots, 10$, chord-length parameters (normalized cumulative chord lengths), degree 3, and clamped knots with the inner knots spread over the parameters. The largest distance $\lVert Q_k - C(t_k) \rVert_\infty$ falls as control points are added:

| control points $n + 1$ | inner knots | largest error | sum of squares |
|---|---|---|---|
| 4 | none | 0.342 | 0.785 |
| 5 | 0.4655 | 0.127 | 0.0966 |
| 6 | 0.32, 0.5954 | 0.0935 | 0.0446 |
| 7 | 0.2269, 0.4655, 0.6721 | 0.0368 | 0.00875 |

The data lie on a parabola, but the fit is not exact, because with chord-length parameters $x(t)$ and $y(t)$ are not polynomials in $t$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). In outline:

1. *Normal equations.* For each coordinate, $F$ is a convex quadratic in $P$. Its gradient is zero exactly when $N^T N \mathbf{P} = N^T \mathbf{Q}$, and every solution is a minimizer.
2. *The assembly is right.* Row $k$ of $N$ has nonzeros only in the columns $s - p, \dots, s$, so $(N^T N)_{ij} = \sum_k N_{ki} N_{kj}$ gets exactly the products that L4 adds, and $N^T \mathbf{Q}$ gets exactly the terms of L5. The band is $p$: two B-splines whose indices differ by more than $p$ have disjoint supports.
3. *Uniqueness.* $N^T N$ is positive definite exactly when $N$ has full column rank. This holds if and only if there are sites $t_{k_0} < t_{k_1} < \dots < t_{k_n}$ with $N_{i,p}(t_{k_i}) \ne 0$ for all $i$, by the [Schoenberg-Whitney theorem](/schoenberg-whitney-theorem/) applied to square submatrices of $N$.
4. *The factorization.* A symmetric positive definite matrix has an $LDL^T$ factorization with positive pivots and no pivoting, and the factor of a band matrix has the same band. If $N^T N$ is singular, some pivot in L6 is zero, and the algorithm reports it.

## Complexity

Let $m + 1$ be the number of data points, $n + 1$ the number of control points, $p$ the degree and $d$ the dimension.

- L3 costs $O(\log n)$ for the span by binary search and $O(p^2)$ for the basis values. Over all data points: $O(m(\log n + p^2))$.
- L4 costs $O(p^2)$ and L5 costs $O(pd)$ per data point: $O(mp^2 + mpd)$.
- L6 costs $O(p^2)$ per row: $O(np^2)$.
- L7 costs $O(pd)$ per row and pass: $O(npd)$.

The total is $O((m + n) p^2 + (m + n) p d)$ time, plus $O(m \log n)$ for the spans (which is $O(m)$ if the sites are sorted and the span is advanced instead of searched). The extra space is $O(np)$ for the band and $O(nd)$ for the right-hand side. The data are read once. A dense solve of the normal equations would cost $O(n^3)$, and a dense QR of $N$ $O(mn^2)$.

## Properties

- *Linear and affine invariant.* The result is $(N^T N)^{-1} N^T \mathbf{Q}$, a linear map of the data applied to each coordinate. The B-splines sum to 1, so an affine map of the data maps the fitted control points in the same way.
- *Reproduction.* If the data lie on a curve of the spline space at the given parameters, $Q_k = \sum_i N_{i,p}(t_k) \hat P_i$, and $N$ has full rank, the fit returns $\hat P$ exactly.
- *Orthogonal residual.* At the solution, $N^T(\mathbf{Q} - N \mathbf{P}) = 0$: the residual vector of each coordinate is orthogonal to every basis column.
- *Not interpolating.* The curve passes through no data point in general, not even the end points.
- *Not local.* The inverse of the band matrix is full, so a change in one data point changes every control point, with an effect that decays away from it.

## Variants and improvements

- *Fixed end points.* Piegl and Tiller set $P_0 = Q_0$ and $P_n = Q_m$ and fit only the inner control points, with the end terms moved to the right-hand side (Section 9.4.1). The curve then starts and ends at the data.
- *Weights and constraints.* A weight $w_k > 0$ per data point gives the matrix $N^T W N$. Derivative or point constraints are added with Lagrange multipliers (Section 9.4.2).
- *QR instead of normal equations.* The condition number of $N^T N$ is the square of that of $N$. Givens rotations applied row by row to the band of $N$ give a [QR decomposition](/qr-decomposition/) in $O(mp^2)$ time without forming $N^T N$, and are preferred when $N$ is badly conditioned (Björck, Chapter 6).
- *Smoothing.* Adding $\lambda \int \lVert C'' \rVert^2 dt$ to $F$ adds a band matrix of the same width. With cubic degree and a knot at every site this is the [smoothing spline](/smoothing-spline/).
- *Error control.* Fit, find the spans where the error is too large, insert knots there, and fit again, until every error is below a tolerance (Section 9.4.4).
- *Parameter correction.* The fixed parameters measure the error between $Q_k$ and the point $C(t_k)$, not the distance from $Q_k$ to the curve. Moving each $t_k$ to the foot point of $Q_k$ on the current curve and fitting again reduces the true distance. This is a nonlinear iteration with no guarantee of a global minimum.

## When to use it

Use it to replace many noisy or dense points (scans, sampled outlines, motion capture paths) by a smooth curve with few control points, when you can choose the degree and the knots in advance. If the curve must pass through every point, use [curve interpolation](/curve-interpolation/) instead, for example the [natural cubic spline](/natural-cubic-spline/). If you do not know where to put knots, use the error control variant or a smoothing spline, which needs no knot choice.

## Pitfalls

- *A basis function with no data.* If the sites miss the support of a B-spline, its column of $N$ is zero and the system is singular. For the example above with all sites in $[0, \tfrac14]$, $N_2$ is zero at every site, and L6 finds the pivot $D_2 = 0$. More generally the Schoenberg-Whitney condition can fail even with $m \ge n$, when several basis functions share too few sites. Averaged knots, which put sites in every span, avoid this in practice.
- *Squared condition number.* In floating point the normal equations lose about twice as many digits as the conditioning of $N$ implies. With many knots close together, or with sites clustered in one part of a span, use the QR variant.
- *Parameters fix the error measure.* Uniform parameters on unevenly spaced data give poor fits, because a point is matched to a curve point far from it. Use chord-length or centripetal parameters, and parameter correction if the true distance matters.
- *Too many control points.* With $n$ close to $m$ the fit follows the noise and can oscillate between the data. The fit error alone does not show this: check the curve between the sites.
- *Clamped ends are not end interpolation.* A clamped knot vector makes $C(u_p) = P_0$, but $P_0$ is a fitted value and not $Q_0$. Use the fixed end point variant when the ends must match.

## Implementations

## History

Least-squares approximation by splines with fixed knots was developed in numerical analysis in the 1960s. De Boor and Rice wrote a Purdue report on least-squares cubic spline approximation with fixed knots in 1968, and de Boor's *A Practical Guide to Splines* (1978, revised 2001) gave the B-spline form with the banded normal equations. In CAD the curve form with vector data, chord-length parameters, averaged knots and fixed end points was set out by Piegl and Tiller in *The NURBS Book* (1995, second edition 1997).

## References
