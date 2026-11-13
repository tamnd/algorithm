---
tag: VE7685
kind: technique
slug: simulation-of-simplicity
name: Simulation of simplicity
aliases:
- symbolic perturbation
area: cad/solid-modeling
level: advanced
summary: Edelsbrunner and Mucke's rule that moves each input coordinate by a power of an infinitesimal, so every predicate sign is nonzero and consistent and algorithms may assume general position.
prereqs: [general-position, orientation-test, determinant, geometric-robustness-problem]
see_also: [exact-geometric-computation, degeneracy-in-sweeps, general-position-delaunay, in-circle-test, regularized-set-operations, csg-ray-casting, boundary-evaluation, arbitrary-precision-arithmetic]
sources:
  - paper: doi:10.1145/77635.77639
    title: Herbert Edelsbrunner and Ernst Peter Mücke, Simulation of Simplicity, a technique to cope with degenerate cases in geometric algorithms, ACM Transactions on Graphics 9(1), 66 to 104, 1990
    locator: the whole paper (the perturbation of the coordinates by powers of one infinitesimal, the sign of a perturbed determinant as the first nonzero minor in a fixed order, and the orientation and in-sphere tests; section numbers not checked)
  - paper: doi:10.1007/PL00009330
    title: Raimund Seidel, The nature and meaning of perturbations in geometric computing, Discrete and Computational Geometry 19(1), 1 to 17, 1998
    locator: the whole paper (what a perturbation scheme guarantees, the cost of output degeneracies, and a comparison of schemes)
  - paper: doi:10.1016/0925-7721(95)00040-2
    title: Chee K. Yap, Towards exact geometric computation, Computational Geometry 7(1-2), 3 to 23, 1997
    locator: the discussion of degeneracies and of perturbation as a part of exact geometric computation
---

Simulation of simplicity (SoS) is a technique of Edelsbrunner and Mücke that removes the degenerate cases of a geometric algorithm without writing code for them. It moves the $j$-th coordinate of the $i$-th input point by $\varepsilon^{2^{id - j}}$, where $\varepsilon > 0$ is an infinitesimal, and it evaluates each predicate on the moved input. The sign of a moved predicate is never zero, and it is the sign of the first nonzero number in a fixed list of minors of the original input, so it costs only a few extra exact evaluations. All the answers come from one real input in [general position](/general-position/), so an algorithm proved for general position is correct on them, but its output is the output for the moved input, and the caller must remove the zero-size parts.

## In plain words

Many geometric programs are correct only when nothing lines up: no three points on one line, no two points with the same x. Real models line up all the time, and writing a special case for each way of lining up is long and easy to get wrong.

This technique pretends that each point was pushed by a tiny amount, with a different and much smaller push for each later point. Then nothing lines up any more. The trick is that the program never computes the pushed points. When a test comes out exactly zero, a short fixed list of extra tests on the original numbers says which way the push breaks the tie.

All tie breaks come from one pushed input, so they never contradict each other. The cost is that the answer describes the pushed input, so a flat triangle can appear and must be removed afterward.

## When it applies

- **The predicates are signs of polynomials in the input coordinates.** Orientation, in-circle and in-sphere tests are determinants of the input. A predicate on a constructed point, such as the side of the crossing point of two lines, is a rational function of the input. SoS can handle it only if it is written in terms of the original coordinates, and the list of extra terms grows.
- **The algorithm is correct for general position.** SoS does not change the algorithm. It changes the predicates so that the general position proof applies.
- **The predicates are evaluated exactly.** The tie break is chosen when the exact value is $0$. A rounded value that is $0$ for a nonzero input, or nonzero for a zero input, gives a wrong tie break. So SoS sits on top of exact or filtered arithmetic, as in [exact geometric computation](/exact-geometric-computation/), and it does not replace it.
- **The output for a nearby input is acceptable.** The result is the exact result for the moved input. It is combinatorially close to a correct result for the real input, but it can contain parts of zero length, area or volume.

How it differs from the two pages it is close to: the [geometric robustness problem](/geometric-robustness-problem/) is the failure that rounding causes, and SoS does not address rounding at all. Exact geometric computation makes every sign exact, including the zero signs. SoS takes those exact zero signs and turns them into consistent nonzero signs.

## The template

Index the input points $1, \ldots, n$ and their coordinates $1, \ldots, d$. Replace coordinate $p_{i,j}$ by
$$p_{i,j}(\varepsilon) = p_{i,j} + \varepsilon^{2^{id - j}}.$$
A predicate is the sign of a polynomial $f$ in the coordinates. Expand $f(p(\varepsilon))$ as a polynomial in $\varepsilon$ and order its terms by increasing exponent. The perturbed sign is the sign of the lowest nonzero term, which is the sign of $f(p(\varepsilon))$ for every small enough $\varepsilon > 0$.

```pseudo id=main
SOS-SIGN(f, input)                              ▷ general form
L1  v ← f(input), evaluated exactly
L2  if v ≠ 0 then return sign(v)
L3  for each set S of perturbed coordinates, in increasing order of Σ_{(i,j) ∈ S} 2^{id−j} do
L4      c ← coefficient of Π_{(i,j) ∈ S} ε^{2^{id−j}} in f(p(ε)), a polynomial in the input
L5      if c ≠ 0 then return sign(c)
L6  ▷ not reached for a nonzero f of degree at least 1 in each point

ORIENT2D-SOS(P, i, j, k)                        ▷ the plane, d = 2
L7  sort (i, j, k) increasingly to (a, b, c); s ← sign of the sorting permutation
L8  for v in D(p_a, p_b, p_c), x_c − x_b, y_b − y_c, x_a − x_c do
L9      if v ≠ 0 then return s · sign(v)
L10 return s
```

Here $D(p, q, r) = (q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$ is the [orientation test](/orientation-test/), positive for a left turn.

**Why the sign is never zero and is well defined.** A monomial of $f(p(\varepsilon))$ that takes the perturbation from a set $S$ of coordinates has the exponent $\sum_{(i,j) \in S} 2^{id - j}$. The numbers $id - j$ are distinct for distinct pairs $(i, j)$, so by the uniqueness of binary expansions, distinct sets $S$ give distinct exponents. Hence the coefficient of each power of $\varepsilon$ belongs to one set $S$, and it is the partial derivative of $f$ with respect to the coordinates in $S$, a minor of the input when $f$ is a determinant. For the orientation determinant with a column of ones, taking the perturbation of $x$ from one row and of $y$ from another gives a coefficient $\pm 1$, so some coefficient is a nonzero constant and the loop of L3 always returns.

**Why the answers are consistent.** An algorithm evaluates finitely many predicates. Each has a fixed sign on an interval $(0, \varepsilon_f)$, and the minimum of the $\varepsilon_f$ is positive. For any $\varepsilon$ below that minimum, every answer of SOS-SIGN is the exact sign of the predicate on one real input $p(\varepsilon)$, and that input is in general position for all the predicates. So the answers obey every law that exact signs on a real input obey, and the general position proof of the algorithm applies to them.

**The plane.** For $d = 2$ the point $i$ moves by $(\varepsilon^{2^{2i - 1}}, \varepsilon^{2^{2i - 2}})$. For $a < b < c$, the exponents of the first terms of the moved $D(p_a, p_b, p_c)$, with $a, b, c = 1, 2, 3$, are $0$, $1$, $2$, $4$, $6$: the input $D$, then the moves of $y_1$, $x_1$ and $y_2$ alone, then the product of the moves of $x_1$ and $y_2$, whose coefficient is $+1$. Their coefficients are the four values of L8 and the constant of L10. For other indices the exponents differ, but the order of the five terms is the same. A permutation of the three rows multiplies the determinant by its sign, which is L7. This list was checked against the moved determinant computed with $\varepsilon = 10^{-4}$ in exact rational arithmetic, for all ordered triples of 400 random sets of 5 points in $\{0, 1, 2\}^2$.

**Cost.** L1 is the predicate itself. In the plane the other four values are differences of coordinates, so a degenerate case costs a few subtractions more. In higher dimensions the list of minors is longer, but the loop stops at the first nonzero term, which on most degenerate inputs is one of the first few.

**Example.** The values below are from ORIENT2D-SOS.

| index : point | call | first nonzero value | result |
|---|---|---|---|
| 1 : $(0,0)$, 2 : $(1,1)$, 3 : $(2,2)$ | $(1, 2, 3)$ | $D = 0$, $x_3 - x_2 = 1$ | $+1$, left turn |
| same | $(2, 1, 3)$ | the same value, odd permutation | $-1$ |
| same | $(3, 2, 1)$ | the same value, odd permutation | $-1$ |
| 1 : $(2,2)$, 2 : $(0,0)$, 3 : $(1,1)$ | $(1, 2, 3)$ | $D = 0$, $x_3 - x_2 = 1$ | $+1$ |
| 1 : $(1,1)$, 2 : $(1,1)$, 3 : $(3,2)$ | $(1, 2, 3)$ | $D = 0$, $x_3 - x_2 = 2$ | $+1$ |
| 1, 2, 3 all at $(5,5)$ | $(1, 2, 3)$ | all four are $0$ | $+1$ |

The three collinear points of the first row become a very thin left-turning triangle. The calls $(1, 2, 3)$, $(2, 3, 1)$ and $(3, 1, 2)$ all give $+1$, and the odd orders all give $-1$, which is what three real points in a triangle give. The duplicate points of the fifth row become two distinct points, and even three equal points get an orientation.

## Classic examples

- **Comparisons in one dimension.** With $d = 1$, point $i$ moves by $\varepsilon^{2^{i - 1}}$, so a lower index gets a larger move. Two equal keys compare by index: $x_i = x_j$ with $i < j$ gives $x_i(\varepsilon) > x_j(\varepsilon)$. This is the common tie break by position, and it is the simplest case of the scheme. Sweeps use it to give distinct event times ([degeneracy in sweeps](/degeneracy-in-sweeps/)).
- **Convex hulls and Delaunay triangulations.** Edelsbrunner and Mücke apply SoS to the orientation and in-sphere determinants, so that hull and Delaunay programs never see coplanar or cospherical points. A Delaunay program then returns a triangulation of four cocircular points, and the choice between the two diagonals depends on the indices only ([general position for Delaunay](/general-position-delaunay/)).
- **Boolean operations and ray casting.** In [CSG ray casting](/csg-ray-casting/) and [boundary evaluation](/boundary-evaluation/), a ray in a face plane and a face in the plane of another face are degenerate cases. A perturbation of the solids makes the tests nonzero, but see the first pitfall below.

## Variations

- **Other orders of the infinitesimals.** Any assignment of exponents that keeps the sets $S$ in distinct orders works, with the same proof. The powers of 2 are the simplest. Seidel describes what any scheme of this kind guarantees and what it costs, and compares several schemes from the literature.
- **Perturbation of the parameters only.** For a predicate that depends on a few parameters, such as the heights of a lifting map, it is enough to move those parameters. The extra terms are then fewer.
- **Lazy evaluation.** Compute the extra terms of L3 only when the exact value is zero, and in the same exact arithmetic. With a floating-point filter in front, the extra terms cost nothing on inputs without degeneracies.

## Pitfalls

- **Degenerate output and regularized sets.** SoS answers for the moved input, not the real one. A collinear triple becomes a triangle of area $0$. Two cubes that share a face are moved either into a thin overlap or apart by a thin gap, and the result of a union is then one solid with a face pair of zero distance or two solids. The [regularized set operations](/regularized-set-operations/) give a different answer: the closed union is one cube, and the shared face is not on its boundary. The caller must remove these zero-size parts after the algorithm, and Seidel points out that this step is not always simple.
- **Rounded input to the tie break.** SoS needs the exact sign of $D$ and of each minor. A float $D$ that is $0$ for an input that is not degenerate makes SoS break a tie that does not exist, so the answer can disagree with an exact answer on another call. Use exact or filtered predicates.
- **The order of the indices matters.** The result depends on how the points are numbered. Two runs on the same set in a different order can give combinatorially different outputs, both correct for their own moved input. Tests must compare structures that do not depend on the order, such as the area or the volume.
- **Constructed points.** A predicate on an intersection point is a rational function of the input. Moving the intersection point by its own infinitesimal breaks the consistency with the lines it came from. The move must be derived from the moves of the original coordinates.
- **Different predicates in one program.** All predicates must use the same moved input. A program that breaks ties of the orientation test with SoS and ties of a distance comparison by another rule loses the consistency.

## Exercises

1. Show that for $a < b < c$ and $d = 2$, the coefficient of the move of $y_a$ in the moved determinant $D(p_a, p_b, p_c)$ is $x_c - x_b$, and the coefficient of the move of $x_a$ is $y_b - y_c$.
2. Prove that the five exponents of the plane case are in the same order for every $a < b < c$, and that no other term comes before the constant term.
3. Give a set of four points with integer coordinates and indices for which the planar convex hull under SoS has a vertex of angle $\pi$, and say which post-processing removes it.
4. Derive the extra terms of a one-dimensional test "is $x_i + x_j < x_k$" under SoS with $d = 1$.
5. Two unit squares share an edge. Describe the union that a planar Boolean operation with SoS returns, and the post-processing step that turns it into the regularized union.

## References
