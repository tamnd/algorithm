---
tag: JK8AA5
kind: technique
slug: witness-configuration-method
name: Witness configuration method
aliases:
- Michelucci-Foufou witness method
area: cad/geometric-constraint-solving
level: research
summary: Michelucci and Foufou's test of rigidity and redundant constraints by the Jacobian rank at a random configuration with the same incidences, which avoids the errors of counting.
prereqs: [rigidity-matrix, schwartz-zippel-lemma]
see_also: [generic-rigidity, laman-theorem, pebble-game-rigidity, double-banana-graph, gortler-healy-thurston-theorem, polynomial-identity-testing, well-constrained-system, dr-plan]
sources:
  - paper: doi:10.1016/j.cad.2006.01.005
    title: Dominique Michelucci and Sebti Foufou, Geometric constraint solving, the witness configuration method, Computer-Aided Design 38(4), 284 to 299, 2006
    locator: the definition of a witness, the rank of the Jacobian at the witness, the detection of dependent constraints and of rigid subsystems, and the comparison with degree of freedom counting
  - paper: doi:10.1145/322217.322225
    title: J. T. Schwartz, Fast probabilistic algorithms for verification of polynomial identities, Journal of the ACM 27(4), 701 to 717, 1980
    locator: the bound on the probability that a nonzero polynomial vanishes at a random point of a grid
  - paper: doi:10.1090/S0002-9947-1978-0511410-9
    title: L. Asimow and B. Roth, The rigidity of graphs, Transactions of the American Mathematical Society 245, 279 to 289, 1978
    locator: generic points are regular points, where the rank of the rigidity matrix is maximal and decides rigidity
  - paper: arXiv:1904.00526
    title: Qiang Zou and Hsi-Yung Feng, On limitations of the witness configuration method for geometric constraint solving in CAD modeling, 2019
    locator: the limitations of the method for the three tasks of characterizing the constraint state, decomposing the system and prioritizing constraints
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, CRC Press, 2018
    locator: the chapters on combinatorial rigidity and on the analysis of constraint systems
---

The witness configuration method analyses a geometric constraint system by linear algebra at one random solution of a similar system. Choose random positions for the geometric elements, keep the incidences that the system requires, and measure the dimension values (distances, angles) from these positions. The result, the *witness*, solves a system with the same structure as the user's. The rank of the Jacobian at the witness then tells, with a proved small error probability, whether the system is under-constrained, well-constrained or over-constrained, which constraints are redundant, and which subsystems are rigid. Unlike [degree of freedom counting](/degrees-of-freedom-analysis/), it sees dependencies that come from geometry, as in the [double banana](/double-banana-graph/), because it does not count at all.

## In plain words

To check whether a drawing is fixed by its dimensions, you could count the dimensions and compare with the number of ways the parts can move. Counting is quick, but it is fooled when two dimensions say the same thing in a hidden way. The witness method instead makes up a random drawing of the same kind, with the same kinds of dimensions, and tests that drawing directly with a small calculation. A random drawing has no hidden coincidences, except those that every drawing of this kind must have. So whatever the test finds there is almost surely true for every typical drawing of this kind.

## When it applies

- **Polynomial constraints.** Each constraint is a polynomial equation in the coordinates and the dimension values: squared distances, incidences, parallelism, tangency, and angles through their cosines or tangents. Then the entries of the Jacobian are polynomials in the coordinates.
- **A structural question.** The question is about a typical instance of the system: is it generically rigid, which constraints are generically redundant. The method answers for almost all dimension values, not for the user's specific values.
- **A witness can be built.** There must be an easy way to get random points that satisfy the constraints whose values are not free. For distance and angle constraints any random placement works, since the values are read from it. Incidences such as a point on a line must hold at the witness, so the witness is built by a construction: choose the line at random, then the point at random on it.
- **Exact or modular arithmetic.** The rank of a matrix is not a continuous function of its entries, so the method should run in exact rational arithmetic or modulo a large prime. In floating point the rank depends on a tolerance.

## The template

For distance constraints between $n$ points in $\mathbb{R}^d$, the Jacobian of the squared distances is twice the [rigidity matrix](/rigidity-matrix/). Let $D = d(d + 1)/2$ be the dimension of the rigid motions when the points span $\mathbb{R}^d$.

```pseudo id=template
WITNESS-ANALYSIS(n, E, d, N)
L1  choose a witness p with independent uniform integer coordinates in 1..N
L2  build the Jacobian J of the constraints at p, one row per constraint
L3  for each constraint e, in order of priority
L4      if the row of e lies in the span of the earlier rows, mark e redundant
L5  r ← rank of J (the number of rows not marked redundant)
L6  flex ← (dn − D) − r
L7  verdict ← well-constrained if flex = 0 and nothing is redundant, else under- or over-constrained
L8  return r, the redundant constraints, flex and the verdict
```

The greedy pass in lines L3 and L4 finds a basis of the row space: the rows not marked redundant are independent, and each marked row depends on the rows before it. The constraints marked redundant are exactly those that a [well-constrained system](/well-constrained-system/) would drop, given the priority order.

**Theorem (one-sided error).** Let $r^*$ be the generic rank of $J$, the largest rank over all placements. Then for every witness $p$, the rank $r$ in line L5 satisfies $r \le r^*$. For a witness drawn as in line L1,
$$ \Pr[r < r^*] \le \frac{r^*}{N} . $$

*Proof.* Every entry of $J$ is a polynomial of degree at most 1 in the coordinates, for example $p_{i,k} - p_{j,k}$. A matrix has rank at least $s$ exactly when some $s \times s$ minor is nonzero. *Upper bound.* Every minor of size $r^* + 1$ is a polynomial that vanishes at every placement, since no placement has rank above $r^*$. So it vanishes at $p$, and $r \le r^*$. *Lower bound.* Some $r^* \times r^*$ minor $M$ is nonzero at some placement, so $M$ is a nonzero polynomial in the $dn$ coordinates, of degree at most $r^*$. By the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/), a nonzero polynomial of degree $r^*$ vanishes at a uniform random point of $\{1, \ldots, N\}^{dn}$ with probability at most $r^*/N$. If $M(p) \ne 0$ then $r \ge r^*$. $\square$

**Consequences.** The rank can only be too small. So the answer "rigid" (flex $= 0$) is always correct: the framework is infinitesimally rigid at $p$, hence generically rigid by the [Asimow and Roth theorem](/asimow-roth-theorem/). A row that is *not* marked redundant is truly independent at a generic placement. Only the answers "flexible" and "redundant" can be wrong, and only with probability at most $r^*/N$. With $t$ independent witnesses and the largest rank kept, the bound becomes $(r^*/N)^t$. For $n = 1000$ points in space and $N = 2^{31}$, one witness errs with probability below $3000 \cdot 2^{-31} < 2 \cdot 10^{-6}$.

**Rigid subsystems.** The kernel of $J$ at the witness is the space of infinitesimal motions. A subset $S$ of the points is rigid inside the system when every motion in the kernel restricts on $S$ to a rigid motion of $S$, which is a rank test on the kernel basis. Michelucci and Foufou use this to find the rigid parts and to guide the decomposition of the system.

**Cost.** For $m$ constraints and $dn$ unknowns, elimination takes $O(m (dn) \min(m, dn))$ field operations. Over the rationals the numbers grow, so a fraction-free elimination or arithmetic modulo a random prime of about 31 bits is used in practice; the probability bound then also accounts for the prime.

## Classic examples

The ranks below are computed exactly over the rationals by the implementation, at random witnesses with $N = 10^6$ unless the points are given.

**A triangle, a square and $K_4$ in the plane.** The triangle has rank $3 = 2 \cdot 3 - 3$ and no redundant edge: well-constrained. The 4-cycle has rank 4 against $2 \cdot 4 - 3 = 5$: one flex, under-constrained. The complete graph $K_4$, with its edges in the order $01, 02, 03, 12, 13, 23$, has rank 5, and the pass marks $23$ redundant: over-constrained, although the count $6 > 5$ already shows it.

**Agreement with Laman's count.** In the plane, the generic rank is the size of the largest edge set in which every $k \ge 2$ vertices span at most $2k - 3$ edges, by [Laman's theorem](/laman-theorem/). On 150 random graphs with up to 7 vertices, the largest rank over two witnesses equals this count, computed by brute force over vertex subsets, every time. On 60 more such graphs, a single witness with $N = 10^6$ also agreed every time, and the number of edges marked redundant was always $m$ minus the rank.

**The double banana.** In space, the [double banana](/double-banana-graph/) has $18 = 3 \cdot 8 - 6$ edges and passes every subset count. The witness gives rank 17, flex 1 and one redundant edge. A counting method, such as a [pebble game](/pebble-game-rigidity/) for the $(3, 6)$ count, would accept it as well-constrained.

**A theorem hidden in the incidences.** Take two lines, three points on each, and the three points where cross joins meet. Pappus's theorem says that these three points are always collinear. A constraint "these three points are collinear" therefore adds nothing, but a count treats it as one more equation. A witness built by the construction (random lines, random points on them, intersections computed) satisfies the collinearity, and its Jacobian row lies in the span of the others, so the method marks it redundant.

**Tiny grids.** With $N = 2$, so that every coordinate is 1 or 2, many witnesses are special. On 150 random graphs the witness rank fell below the Laman count on some of them and never rose above it, as the theorem says.

## Variations

- **Several witnesses.** Keep the largest rank over $t$ independent witnesses. The rank never overshoots, so the maximum is safe, and the error probability drops to $(r^*/N)^t$.
- **Modular witnesses.** Choose a random prime $q$ and work in $\mathbb{Z}/q$. The Schwartz-Zippel bound holds over any field, and a bad prime adds a small, bounded failure probability.
- **The user's sketch as witness.** The approximate drawing that the user made is often near a valid configuration and can serve as a witness after a small correction. It is cheap, but it is the most likely witness to be special; see Pitfalls.
- **Global rigidity.** The same idea with a random combination of the self-stresses at the witness decides generic global rigidity by the rank of the stress matrix, as in the [Gortler, Healy and Thurston theorem](/gortler-healy-thurston-theorem/).
- **Other constraint types.** Angles, tangencies, parallelism and point-on-curve constraints add Jacobian rows like distances do. The witness must satisfy every constraint whose value is fixed by the type, such as an incidence, and may take the values of the others from its own geometry.

## Pitfalls

- **A special witness.** Points on a grid, on a circle, with equal lengths or with parallel sides are not random. For example, $K_{3,3}$ with its six points on the circle $x^2 + y^2 = 25$, at $(5, 0), (0, 5), (-5, 0)$ and $(3, 4), (-4, -3), (4, -3)$, has rank 8, while a random witness gives 9, the generic rank. The rank drop is real for that placement but false for the system. Use random coordinates from a large range, and never only the user's sketch.
- **The wrong component.** When incidences define a set with several components, a witness can land on a degenerate one, for example with two points that coincide, which satisfies "point on line" constraints trivially. The rank there need not be the rank at the configurations the user wants. Build the witness so that distinct elements are distinct.
- **Generic is not specific.** The method answers for typical dimension values. The user's actual values may be special: three points with lengths $1, 1, 2$ force a collinear triangle, which is flexible to first order although the triangle is generically rigid. It also says nothing about whether the user's values have a real solution at all, which is the hard [distance geometry problem](/distance-geometry-problem/).
- **Floating point.** A numerical rank needs a threshold on singular values, and near-dependent rows of a badly scaled sketch can fall on either side. Exact rational or modular arithmetic removes the threshold.
- **Order dependence.** Which constraint is marked redundant depends on the order in lines L3 and L4. The number of redundant constraints does not. Order the constraints by user priority so that the dropped ones are the least important. Zou and Feng (2019) discuss why the method alone does not settle the CAD tasks of characterizing the constraint state, decomposing the system and prioritizing constraints.

## Exercises

1. Show that for a 1-dimensional placement, the rank of the rigidity matrix at any placement with distinct coordinates is $n - c$, where $c$ is the number of connected components. Why is any injective witness enough here?
2. The prism graph in the plane has 9 edges and rank 9. Find a placement of it with rank 8 and explain what the drop means geometrically.
3. Give a constraint system whose generic rank is $r^*$ and a placement in $\{1, 2\}^{dn}$ where the rank is below $r^*$. Compare with the bound $r^*/N$.
4. Prove that the rank at the witness cannot exceed the generic rank using only the fact that the set of placements of rank at most $s$ is closed.
5. Design the witness construction for a sketch with constraints "point on circle", "line tangent to circle" and "distance between points". Which values are taken from the witness, and which are enforced by the construction?

## References
