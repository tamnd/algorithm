---
tag: 3NRTQF
kind: algorithm
slug: direct-linearization-method
name: Direct linearization method
aliases:
- DLM tolerance analysis
area: cad/reverse-engineering-and-inspection
level: advanced
summary: Chase and coauthors' tolerance analysis that linearizes the vector loops of an assembly to get sensitivities, then worst case or statistical variation.
model: real-ram
complexity:
  vars: {n: number of manufactured variables, m: "number of kinematic variables, two per 2D loop", V: number of vectors in the loops, k: number of Newton steps}
  time: {worst: "O(k (V m + m^3) + V (m + n) + m^3 + n m^2)"}
  space: {extra: "O(m (m + n))"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1995
  people: [Kenneth W. Chase, Jinsong Gao, Spencer P. Magleby]
  note: Chase, Gao and Magleby published the 2D method with small kinematic adjustments in 1995, and Gao, Chase and Magleby extended it to 3D assemblies in 1998.
prereqs: [vector-loop-closure, tolerance-stack-up]
see_also: [monte-carlo-tolerance-analysis, tolerance-allocation, jacobian-torsor-model, small-displacement-torsor, newton-method-for-systems, four-bar-linkage, freudenstein-equation, kinematic-fixture-analysis]
sources:
  - paper: "Kenneth W. Chase, Jinsong Gao and Spencer P. Magleby, General 2-D tolerance analysis of mechanical assemblies with small kinematic adjustments, Journal of Design and Manufacturing 5(4), 263 to 274, 1995"
    locator: the whole paper (vector loop models with manufactured and kinematic variables, the matrices A and B of partial derivatives, the sensitivities from B^-1 A, and the worst-case and RSS results)
  - paper: "Jinsong Gao, Kenneth W. Chase and Spencer P. Magleby, Generalized 3-D tolerance analysis of mechanical assemblies with small kinematic adjustments, IIE Transactions 30, 367 to 377, 1998"
    locator: the whole paper (the extension of the method to 3D vector loops)
  - book: isbn:9780070181311
    title: Paul J. Drake, Jr. (editor), Dimensioning and Tolerancing Handbook, McGraw-Hill, 1999
    locator: the chapters by Kenneth W. Chase on multi-dimensional tolerance analysis with vector loops and on minimum-cost tolerance allocation, which uses the one-way clutch as its 2D example
  - book: isbn:9780070542358
    title: Walter Rudin, Principles of Mathematical Analysis, 3rd edition, McGraw-Hill, 1976
    locator: Theorem 9.28, the implicit function theorem, and Theorem 5.15, Taylor's theorem
  - paper: doi:10.1016/j.cad.2014.02.014
    title: Hua Chen, Sun Jin, Zhimin Li and Xinmin Lai, A comprehensive study of three dimensional tolerance analysis methods, Computer-Aided Design 53, 1 to 13, 2014
    locator: the part on the direct linearization method and its comparison with the other 3D methods
---

The direct linearization method (DLM) is a tolerance analysis for assemblies whose parts adjust to each other when they are put together, such as a roller that rolls until it touches two surfaces. Chase, Gao and Magleby published it in 1995. The assembly is written as closed [vector loops](/vector-loop-closure/), $h(x, u) = 0$, where $x$ are the part dimensions that have tolerances and $u$ are the *kinematic* variables that the assembly finds by itself. DLM solves the loops once at the nominal dimensions, takes the partial derivatives $A = \partial h / \partial x$ and $B = \partial h / \partial u$, and gets the sensitivity of every output to every dimension from $-B^{-1} A$, with no explicit formula for the output. The worst-case and RSS formulas of [tolerance stack-up](/tolerance-stack-up/) then give the variation. Its model of variation is a first-order (small change) Taylor expansion of the assembly function at the nominal point; this page proves it and bounds its error. [Monte Carlo analysis](/monte-carlo-tolerance-analysis/) solves the loops exactly for each sample instead, at a higher cost.

## In plain words

In many assemblies a gap or an angle is not a sum of part dimensions. It comes out of how the parts settle against each other. You can still write the geometry as chains of arrows that must close into loops. Solve these loops once for the nominal parts. Then ask a linear question: if one dimension changes a little, how much must the free quantities change for the loops to stay closed? That answer is one small linear system, and it gives the sensitivity of the output to each dimension. With the sensitivities, the usual stack-up rules give the worst case and the statistical spread. The method is fast and exact for small changes. For large tolerances it misses the curvature of the true assembly function, and it cannot tell that some parts no longer fit together at all.

## The problem

Input: closed vector loops with manufactured variables $x \in \mathbb{R}^n$ (lengths and angles of parts, each with a nominal value and a symmetric tolerance $T_j$), kinematic variables $u \in \mathbb{R}^m$ (two per loop in the plane, six per loop in space), a starting guess for $u$, and an output, one kinematic variable $u_k$ such as a gap or a contact angle.

Output: the nominal output $u_k(x_0)$, the sensitivities $S_j = \partial u_k / \partial x_j$, the worst-case half-width $W = \sum_j |S_j| T_j$, and the RSS half-width $R = \sqrt{\sum_j S_j^2 T_j^2}$.

The model of variation is that each $x_j$ deviates from its nominal by $\delta_j$: in the worst-case form any $|\delta_j| \le T_j$, and in the statistical form independent with mean $0$ and standard deviation $T_j / 3$. The output is replaced by its first-order expansion $u_k(x_0) + S \cdot \delta$.

## The algorithm

```pseudo id=main
DLM(h, x0, u_guess, T, k)          ▷ loops h, nominal x0, tolerances T, output u_k
L1  u0 ← NEWTON(h, x0, u_guess)                     ▷ assemble the nominal parts
L2  A ← ∂h/∂x at (x0, u0);  B ← ∂h/∂u at (x0, u0)
L3  for j ← 1 to n do
L4      solve B s_j = −A_j                           ▷ error if B is singular
L5      S_j ← component k of s_j                     ▷ ∂u_k / ∂x_j
L6  W ← Σ_j |S_j| T_j                                ▷ worst case
L7  R ← sqrt(Σ_j S_j² T_j²)                          ▷ RSS, 3 sigma
L8  return u0_k, S, W, R

NEWTON(h, x, u)
L9  repeat
L10     r ← h(x, u)
L11     solve B(x, u) δ = −r;  u ← u + δ
L12 until |δ| is below a tolerance and |h(x, u)| is small
L13 return u
```

**The derivatives.** A vector of the loop is $s L (\cos\theta, \sin\theta)$, with sign $s$, length $L$ (a constant or a variable) and absolute angle $\theta = \theta_0 + \sum c_j y_j$, an affine function of angle variables. Its derivative with respect to $L$ is $s (\cos\theta, \sin\theta)$, and with respect to $y_j$ it is $s L c_j (-\sin\theta, \cos\theta)$. Line L2 sums these over the vectors; no finite differences are needed. The rows of $A$ and $B$ are the $x$ and $y$ sums of each loop.

**Why $-B^{-1} A$.** If $x$ changes by $\delta x$ and $u$ by $\delta u$, the loops stay closed to first order when $A\, \delta x + B\, \delta u = 0$, so $\delta u = -B^{-1} A\, \delta x$. Lines L3 to L5 compute column $j$ of $-B^{-1} A$ and keep row $k$. When the output is not a kinematic variable but a function $g(x, u)$, the same columns give $\partial g / \partial x_j + \nabla_u g \cdot s_j$.

## Example

**The one-way clutch.** This is Chase's standard 2D example. A hub has a flat at distance $a$ from the centre of a ring of inner radius $e$, and a roller of radius $c$ wedges between them. The kinematic variables are the position $b$ of the roller contact along the flat and the pressure angle $\phi$ between the two contact normals, which decides whether the clutch locks. The loop goes from the ring centre along the flat ($b$ at $0^\circ$), up to the flat ($a$ at $90^\circ$), up to the roller centre ($c$ at $90^\circ$), and back to the ring centre along the line through the roller contact ($c - e$ at $90^\circ - \phi$). It closes when $\cos\phi = (a + c)/(e - c)$ and $b^2 + (a + c)^2 = (e - c)^2$.

Take $a = 27.645$, $c = 11.43$, $e = 50.8$ mm, each with tolerance $T = 0.0127$ mm. Newton's method gives $b = 4.8105$ mm and $\phi = 7.0184^\circ$. DLM gives:

| dimension | $S_j$ (rad per mm) | $\lvert S_j \rvert T_j$ (rad) |
|---|---|---|
| $a$ | $-0.20788$ | $0.00264$ |
| $c$ | $-0.41420$ | $0.00526$ |
| $e$ | $+0.20632$ | $0.00262$ |

These agree with the derivatives of the closed form, $\partial \phi / \partial a = -1/((e - c)\sin\phi)$ and so on. The worst case is $W = 0.01052$ rad, so $\phi = 7.018^\circ \pm 0.603^\circ$, and the RSS value is $R = 0.00644$ rad, so $\phi = 7.018^\circ \pm 0.369^\circ$ at 3 sigma. At the eight corners of the tolerance box the exact $\phi$ ranges from $-0.631^\circ$ to $+0.579^\circ$ around the nominal: the linear range $\pm 0.603^\circ$ is off by $0.03^\circ$ at each end, the second-order error that the correctness proof bounds. With $T = 0.05$ mm on each dimension DLM says $\pm 2.37^\circ$, but the corners give $-3.03^\circ$ to $+2.07^\circ$, a clearly skewed range. With $T = 0.1$ mm the corner $a + T$, $c + T$, $e - T$ has $a + c > e - c$, so the roller does not fit at all; DLM still returns a number.

**A linear stack.** The housing gap of the stack-up page, $G = A - B - C - D$ with $A = 50 \pm 0.10$ and $B, C, D$ of $20, 15, 14.8 \pm 0.05$, written as one loop, gives sensitivities $+1, -1, -1, -1$, nominal $0.20$, $W = 0.25$ and $R = \sqrt{0.0175} \approx 0.1323$, the stack-up results.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). In short:

- The partial derivatives of line L2 are exact, by the chain rule on each vector.
- If $B$ is nonsingular at the nominal assembly, the implicit function theorem gives a smooth solution $u(x)$ near $x_0$ with derivative $-B^{-1} A$. So the sensitivities of line L5 are the exact first derivatives of the output.
- By Taylor's theorem, $u_k(x_0 + \delta) = u_k(x_0) + S \cdot \delta + r(\delta)$ with $|r(\delta)| \le \tfrac12 M |\delta|^2$, where $M$ bounds the Hessian of $u_k$.
- The worst-case value $W$ of line L6 is the exact range of the linear part over the tolerance box, and the true range is within $W + \tfrac12 M |T|^2$.
- If the deviations are independent with standard deviations $T_j / 3$, the linear part has standard deviation exactly $R / 3$. If they are also normal, it lies in $\pm R$ with probability $0.9973$. Independence is needed for the variance and normality for the probability.
- If every angle is a constant, the loops are linear and DLM is exact for any change.

## Complexity

Each Newton step of lines L9 to L12 builds the $m \times m$ matrix $B$ in $O(V m)$ time and solves with it in $O(m^3)$, so the nominal assembly costs $O(k (V m + m^3))$ for $k$ steps. Line L2 builds $A$ and $B$ in $O(V (m + n))$. Factor $B$ once in $O(m^3)$, and each of the $n$ solves of line L4 costs $O(m^2)$, so the sensitivities cost $O(m^3 + n m^2)$. The code of this page eliminates afresh for each column, $O(n m^3)$, which is fine for the few loops of a real assembly. Lines L6 and L7 take $O(n)$. The extra space is $O(m (m + n))$ for $A$ and $B$. Unlike Monte Carlo, the cost does not grow with the number of samples: one linear solve replaces all of them.

## Properties

- **Local.** The sensitivities are exact derivatives at the nominal point, and the variation is exact only for the linear part.
- **Symmetric.** Its worst-case and RSS ranges are symmetric about the nominal output, even when the true range is not.
- **Distribution-free variance.** The RSS variance of the linear part needs independence but no distribution shape.
- **Exact for linear loops.** With fixed angles, the output is affine in the dimensions and the method has no error.
- **Deterministic.** The same input gives the same output; no sampling.

## Variants and improvements

- **3D loops.** Gao, Chase and Magleby replace the 2D vectors by 3D vectors and rotations, with six equations per loop.
- **Geometric feature variations.** Form, orientation and position variations of features can be modeled as extra small vectors or rotations at the contacts, which keeps the method linear. The [small displacement torsor](/small-displacement-torsor/) and [Jacobian-torsor](/jacobian-torsor-model/) models build the same kind of linear map from 3D feature frames.
- **Mean shift and second order.** The proof shows the bias $\tfrac12 \sum_j H_{jj} \sigma_j^2$ of the output mean. Adding second derivatives estimates it. The estimated mean shift model of the [stack-up page](/tolerance-stack-up/) adds a worst-case part for process drift.
- **Allocation.** The sensitivities are the input of [tolerance allocation](/tolerance-allocation/), which chooses the $T_j$ at least cost.
- **Simulation.** When the assembly is far from linear or a fit can fail, [Monte Carlo analysis](/monte-carlo-tolerance-analysis/) solves the loops for each sample.

## When to use it

Use DLM for an assembly with small kinematic adjustments where the tolerances are small against the dimensions, as in most machined parts. It gives sensitivities, which show where tightening a tolerance helps most, and it costs one linear solve. Check the result with Monte Carlo when the tolerances are large relative to the curvature of the assembly function, when the output is near a limit of assembly (such as the clutch at large tolerances), or when the distributions are far from normal.

## Pitfalls

- **Singular B.** Near a toggle position of a linkage, or when two kinematic vectors are parallel, $B$ is singular or close to it, and the sensitivities blow up. The method then says nothing useful.
- **The wrong branch.** A loop can close in several ways, such as the open and crossed forms of a [four-bar linkage](/four-bar-linkage/). Newton's method finds the one near its starting guess; start from the drawing.
- **Parts that do not fit.** DLM never checks that each sample assembles. A worst-case corner can be impossible, as in the clutch example.
- **Units.** Angles are in radians in the derivatives. A tolerance in degrees must be converted.
- **Correlated dimensions.** RSS assumes independent dimensions. Two dimensions from one setup are not.
- **Mean shift.** A curved assembly function moves the mean of the output away from its nominal value even for centred inputs; DLM reports the nominal value as the mean.

## Implementations

## History

Chase and his group at Brigham Young University developed tolerance analysis with vector loops in the 1980s and 1990s. Chase, Gao and Magleby published the general 2D method with small kinematic adjustments in the Journal of Design and Manufacturing in 1995, and Gao, Chase and Magleby the 3D method in IIE Transactions in 1998. Chase's chapters in the Dimensioning and Tolerancing Handbook of 1999 present the method with worked examples, the one-way clutch among them. Chen, Jin, Li and Lai compare DLM with the other 3D tolerance analysis methods in a survey of 2014.

## References
