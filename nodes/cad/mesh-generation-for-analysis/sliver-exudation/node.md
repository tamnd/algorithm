---
tag: 4WRSY6
kind: algorithm
slug: sliver-exudation
name: Sliver exudation
aliases:
- Cheng-Dey-Edelsbrunner sliver removal
area: cad/mesh-generation-for-analysis
level: research
summary: Removes slivers from a Delaunay tetrahedral mesh by giving each vertex a small weight, so that the weighted Delaunay triangulation of the same points avoids them.
solves: [mesh-generation]
model: real-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1999
  people: [Siu-Wing Cheng, Tamal K. Dey, Herbert Edelsbrunner, Michael A. Facello, Shang-Hua Teng]
  note: Presented at SoCG 1999 and published in the Journal of the ACM in 2000, it was the first proof that the slivers of a Delaunay mesh with bounded radius-edge ratio can be removed without moving or adding vertices.
prereqs: [tetrahedral-delaunay-refinement, regular-triangulation, sliver-tetrahedron]
see_also: [power-diagram, radius-edge-ratio, mesh-quality-measures, protecting-balls, isosurface-stuffing, topological-tetrahedral-mesh-improvement, optimization-based-mesh-smoothing, delaunay-refinement]
sources:
  - paper: doi:10.1145/355483.355487
    title: Siu-Wing Cheng, Tamal K. Dey, Herbert Edelsbrunner, Michael A. Facello and Shang-Hua Teng, Sliver exudation, Journal of the ACM 47(5), 2000, 883 to 904
    locator: Section 2.4 (Ratio Property), Section 4.2 (Weight Property), Section 4.5 (the measure Sigma), Section 5.1 (periodic point sets and Claim 7, the Weighted Ratio Property), Section 6.5 (the Sliver Theorem), Section 7.1 (pumping and the skyline), Section 8.1 (the constant is "miserably tiny")
  - paper: doi:10.1145/304893.304894
    title: Siu-Wing Cheng, Tamal K. Dey, Herbert Edelsbrunner, Michael A. Facello and Shang-Hua Teng, Sliver exudation, Proceedings of the 15th Annual Symposium on Computational Geometry, 1999, 1 to 13
    locator: the conference version (general locator)
  - paper: doi:10.1007/s003660200020
    title: Herbert Edelsbrunner and Damrong Guoy, An experimental study of sliver exudation, Engineering with Computers 18(3), 2002, 229 to 240
    locator: Section 3 (function Pump with the bound 0.45 d_u, the O(n) running time, the remark that the proved constant is "positive but miserably small" and around 5 degrees in practice), Section 4 (experiments), Section 5 (the boundary as the main limitation)
  - book: isbn:9781584887300
    title: Siu-Wing Cheng, Tamal K. Dey and Jonathan Richard Shewchuk, Delaunay Mesh Generation, CRC Press, 2013
    locator: Chapter 7 (weighted Delaunay triangulations, pages 169 to 184), Chapter 10 (sliver exudation, pages 223 to 246), Chapter 11 (refinement for sliver exudation, pages 247 to 260)
  - paper: doi:10.1137/S0097539703418808
    title: Siu-Wing Cheng and Tamal K. Dey, Quality meshing with weighted Delaunay refinement, SIAM Journal on Computing 33(1), 2003, 69 to 93
    locator: Section 5 (pumping mixed with refinement for polyhedral domains, Lemma 5.1 on the orthoradius-edge ratio)
  - paper: doi:10.1145/1276377.1276448
    title: François Labelle and Jonathan Richard Shewchuk, Isosurface stuffing, fast tetrahedral meshes with good dihedral angles, ACM Transactions on Graphics 26(3), 2007, article 57
    locator: Section 2, the remark that the provable angle bounds of Delaunay methods with sliver removal are below 0.1 degree and probably below a millionth of a degree
---

Sliver exudation removes [slivers](/sliver-tetrahedron/) from a Delaunay tetrahedral mesh without moving any vertex or adding one. It gives each vertex $p$ a weight $P^2$, the squared radius of a small sphere around $p$, and replaces the Delaunay triangulation by the [weighted Delaunay (regular) triangulation](/regular-triangulation/) of the same points. Cheng, Dey, Edelsbrunner, Facello and Teng proved that if the Delaunay mesh has bounded [radius-edge ratio](/radius-edge-ratio/), as [tetrahedral Delaunay refinement](/tetrahedral-delaunay-refinement/) produces, then weights exist that make every tetrahedron fat, and the weights can be found one vertex at a time. The proof gives a positive constant that the authors call "miserably tiny", while in practice the method raises the smallest dihedral angle to about $5°$.

## In plain words

A Delaunay mesh with good radius-edge ratios can still contain slivers: flat tetrahedra whose four vertices lie near a circle. A sliver is fragile. If one of its vertices gets a weight, its orthosphere (the sphere that is orthogonal to the four weighted spheres) moves, and some other vertex falls inside it, so the sliver leaves the triangulation. Sliver exudation visits each vertex once. It removes the vertex, looks at the finitely many weights at which the triangulation around it changes, tries one weight between each pair, and keeps the weight whose star has the largest smallest dihedral angle. The weight stays below $(0.45\, d)^2$, where $d$ is the distance to the nearest other vertex, so the spheres stay disjoint and no vertex disappears.

## The problem

The input is a finite point set $S$ in $\mathbb{R}^3$ whose Delaunay triangulation $\mathrm{Del}\, S$ has the *Ratio Property* $[\rho_0]$: every tetrahedron has circumradius $R$ and shortest edge $L$ with $R / L \le \rho_0$. The output is a weight $w_p = P^2 \ge 0$ for each point $p$, and the weighted Delaunay triangulation of the weighted points, chosen so that no tetrahedron is a sliver.

Two weighted points $(p, w_p)$ and $(x, w_x)$ have *power distance* $\pi = |p - x|^2 - w_p - w_x$. Four weighted points in general position have a unique *orthosphere* $(z, Z^2)$ with $|p - z|^2 - Z^2 = w_p$ for each of them; with zero weights it is the circumsphere. A weighted point $(e, w_e)$ *conflicts* with the tetrahedron if its power distance to the orthosphere is negative. The weighted Delaunay triangulation has a tetrahedron on four weighted points exactly when no other weighted point conflicts with it. Its sizes are measured, as in the paper, by $\Sigma = V / L^3$, the volume over the cube of the shortest edge. A tetrahedron is a sliver when $\Sigma$ is small though its ratio is bounded.

The weights must satisfy the *Weight Property* $[\Omega_0]$ for a constant $\Omega_0 \in (0, \frac12)$: for every two points $p, q$, $0 \le P \le \Omega_0 |p - q|$. Then the spheres are disjoint, and every point remains a vertex.

This page makes three kinds of claim.

- *Existence theorem, cited.* The Sliver Theorem (Section 6.5 of the paper): "Assume Del S has Ratio Property $[\rho_0]$. Then there is a constant $\Sigma_0 > 0$ and a weight assignment defining a set of spheres with Weight Property $[\Omega_0]$ such that $\Sigma > \Sigma_0$ for all tetrahedra pqrs" of the weighted Delaunay triangulation. The theorem is stated for periodic point sets $S = S_0 + \mathbb{Z}^3$, which have no boundary. The paper gives no number for $\Sigma_0$; its Section 8.1 says "the estimate for $\Sigma_0$ provided by the Sliver Theorem is miserably tiny" and leaves open how it depends on $\rho_0$ and $\Omega_0$. Claim 7 (Section 5.1) adds that the weighted triangulation has orthoradius over shortest edge $Z / L \le \rho_1$ for a constant $\rho_1$ that depends only on $\rho_0$ and $\Omega_0$, also without a number.
- *Proved here.* The power test that the implementation uses, and the fact that pumping never lowers the smallest dihedral angle of the mesh. Also a lemma that turns the theorem into a dihedral angle bound with explicit dependence: every dihedral angle $\theta$ of the weighted triangulation of the theorem satisfies $\sin\theta \ge \Sigma_0 (1 - 4\Omega_0^2)^2 / (2\rho_1^4)$. For $\Omega_0 = 0.45$ the factor $(1 - 4\Omega_0^2)^2/2$ is $0.018$, so the bound is a tiny multiple of a tiny constant. See `proofs/correctness.md`.
- *Measured, no guarantee.* Edelsbrunner and Guoy write that the proved constant is "positive but miserably small" and that the constant reached in practice is "much larger and possibly around 5°". On a mesh of more than 76,000 tetrahedra they moved every dihedral angle above $5°$ except one, which was above $3°$, next to the boundary. Labelle and Shewchuk note that the provable bounds of Delaunay methods with sliver removal are below $0.1°$ and probably below a millionth of a degree. In the example below the smallest angle rises from $0.14°$ to $5.20°$.

A radius-edge bound alone does not remove slivers: a sliver can have $R / L$ as low as $1/\sqrt2$. That is why sliver exudation exists, and why it needs the Ratio Property only as a hypothesis, not as the goal.

## The algorithm

Fix the weights of all vertices except $u$, and let $T_u$ be the weighted Delaunay triangulation without $u$. For each tetrahedron $t$ of $T_u$ the *critical weight* $w_t$ is the power distance from $u$ (at weight $0$) to the orthosphere of $t$. The weighted point $(u, w)$ conflicts with $t$ exactly when $w > w_t$. So the triangulation with $u$ at weight $w$ is $T_u$ with the tetrahedra $\{t : w_t < w\}$ removed and $u$ joined to the boundary of the hole, and it changes only when $w$ crosses a critical weight.

```pseudo id=main
SLIVER-EXUDATION(S, Ω0)
L1  T ← the Delaunay triangulation of S; every weight is 0
L2  for each vertex u, once, in any order:
L3      T_u ← the weighted Delaunay triangulation of S without u
L4      for each tetrahedron t of T_u: w_t ← power distance from (u, 0) to the orthosphere of t
L5      W ← (Ω0 d_u)^2, where d_u is the distance from u to its nearest other point
L6      candidates ← 0 and one weight strictly between each two consecutive critical weights in [0, W]
L7      for each candidate w: star(w) ← u joined to the boundary of {t in T_u : w_t < w}; ζ(w) ← its smallest dihedral angle
L8      w* ← the candidate of largest ζ, keeping 0 on ties
L9      w_u ← w*; T ← (T_u minus the removed tetrahedra) plus star(w*)
L10 return T and the weights
L11 conflict test: (e, w_e) conflicts with abcd iff -det[p - e, |p - e|^2 - w_p + w_e] (rows p = a, b, c, d) has the sign of orient3d(a, b, c, d)
```

The test of L11 is the weighted form of the insphere test: with all weights $0$ it is the insphere determinant. The paper's own rule (Section 7.1) picks the weight that maximizes the smallest $\Sigma$ in the star; Edelsbrunner and Guoy's implementation, and this one, maximize the smallest dihedral angle instead. Edelsbrunner and Guoy evaluate the star at each critical weight as it grows; here a weight strictly between two critical weights is used, so no four weighted points are ever on a common orthosphere.

The paper treats periodic sets. The implementation puts the points in a box whose 8 corners are part of the input and keep weight $0$; only the points strictly inside are pumped. Coordinates and weights are integers, so every orientation and power test is exact integer arithmetic, and the critical weights are exact fractions. L3 rebuilds the triangulation without $u$ by Bowyer-Watson insertion with the power test.

## Example

The input is 27 points near the grid points $(i, j, k) \cdot 1000$ for $i, j, k \in \{1, 2, 3\}$, each coordinate moved by a random integer in $[-100, 100]$ (seed 2), inside the box $[0, 4000]^3$, with $\Omega_0 = 0.45$. The steps come from the implementation, and the test file checks them.

| Step | Vertex | What happens |
|---|---|---|
| L1 | | 35 vertices, 151 tetrahedra; smallest dihedral angle $0.14°$, 9 tetrahedra below $5°$ and 17 below $10°$ |
| | | the worst is a sliver on $(3034, 1095, 993)$, $(3051, 990, 1992)$, $(3002, 2083, 1089)$, $(3018, 2067, 2035)$, with angles $0.14°$ and $179.78°$ and radius-edge ratio $2.90$ |
| pump 2 | $(992, 943, 2088)$ | weight $138757$ of at most $156905$; the smallest angle in its star rises from $3.10°$ to $4.77°$ |
| pump 7 | $(1000, 3085, 1030)$ | weight $183429$; star from $5.20°$ to $22.30°$ |
| pump 19 | $(3034, 1095, 993)$ | weight $44845$ of at most $199742$; star from $0.14°$ to $5.47°$; the worst sliver is gone and the mesh minimum rises to $3.02°$ |
| pump 23 | $(3018, 2067, 2035)$ | weight $103673$, chosen among 14 candidates; star from $3.02°$ to $16.74°$; the mesh minimum rises to $5.20°$ |
| end | | 139 tetrahedra; smallest angle $5.20°$, none below $5°$ and 6 below $10°$; 11 of the 27 points got a positive weight, the largest with $P / d_u = 0.435$ |

Sixteen of the 27 pumps keep weight $0$, because no weight improves their star. The number of tetrahedra drops, as Edelsbrunner and Guoy also observe, because a sliver and its neighbors are replaced by fewer tetrahedra. With seed 1 and moves up to $150$, the minimum rises from $1.54°$ to $3.03°$, and the worst remaining tetrahedron has a box corner as a vertex, which is never pumped: near the boundary the method has little room, as the paper's boundary-free setting suggests.

## Correctness

*The power test.* Lift each weighted point to $p^+ = (p, |p|^2 - w_p)$ in $\mathbb{R}^4$. The four lifted vertices of a tetrahedron lie on the graph of an affine function $h(x) = 2 z \cdot x - |z|^2 + Z^2$, where $(z, Z^2)$ is the orthosphere, and the power distance of $(e, w_e)$ to the orthosphere is $|e|^2 - w_e - h(e)$. Column operations turn the determinant of L11 into $\pi$ times $\mathrm{orient3d}(a, b, c, d)$, so the test returns $-\pi\, |\mathrm{orient3d}|$, positive exactly in conflict. The full proof is in `proofs/correctness.md`, and the tests compare the test with an orthosphere computed by exact Gaussian elimination on 300 random weighted configurations.

*Each pump keeps the triangulation regular.* By the lifting, the weighted Delaunay triangulation is the projection of the lower convex hull of the lifted points, and adding $(u, w)$ removes exactly the facets whose hyperplane passes above $u^+$, which are the tetrahedra with $w_t < w$, and cones $u$ to the horizon. The tests check that the final mesh has no conflict between any tetrahedron and any weighted point, that the volumes sum to the box, and that it equals a triangulation rebuilt from scratch with the final weights.

*The smallest dihedral angle never decreases.* Weight $0$ is always a candidate, and at weight $0$ the star is the current star of $u$. A larger weight only removes more tetrahedra of $T_u$. So the new mesh consists of tetrahedra of the old mesh and the new star, whose smallest angle is at least that of the old star. The tests check this after every pump.

*The guarantee.* The Sliver Theorem is cited, not proved here. Its proof shows that for each vertex the weights at which the star contains a sliver cover only part of the interval $[0, (\Omega_0 d_u)^2]$, and picks a weight outside them; the Ratio Property bounds how many tetrahedra can ever appear in the star. The bound $\sin\theta \ge 8\Sigma / \lambda^4$, with $\lambda$ the longest over the shortest edge, and $\lambda \le 2\rho_1 / \sqrt{1 - 4\Omega_0^2}$ under the Weight Property, are proved in `proofs/correctness.md` and checked on every tetrahedron of the tests.

## Complexity

Under the Ratio Property the star of every vertex has constant size (Cheng et al.), so a pump looks at a constant number of critical weights and takes constant time once the vertex is located, and the whole method runs in $O(n)$ time after the Delaunay triangulation is built, as Edelsbrunner and Guoy note. The paper states $O(n \log n)$ when the triangulation is included. Space is $O(n)$.

The implementation is simpler: it rebuilds the triangulation without $u$ from scratch for each pump, with linear scans, so a pump costs $O(n^2)$ and the run $O(n^3)$. For the 35 points of the example the whole run takes about half a second.

## Properties

- **No new vertices, no moved vertices.** Only the connectivity changes, through the weights.
- **Monotone.** The smallest dihedral angle of the mesh never decreases, and the smallest angle of each pumped star does not decrease either.
- **Every vertex once, in any order.** Edelsbrunner and Guoy note that one pass suffices.
- **Existence guarantee, no explicit constant.** $\Sigma > \Sigma_0$ for periodic inputs with bounded ratio; the paper does not compute $\Sigma_0$.
- **Weak at the boundary.** The theorem has no boundary. Edelsbrunner and Guoy name the boundary as the main limitation in practice.
- **Exact here.** Integer coordinates and weights; all signs are exact.

## Variants and improvements

- **Refinement with pumping.** Cheng and Dey (SIAM J. Computing, 2003) mix pumping with Delaunay refinement for polyhedral domains, giving the first deterministic method with boundaries; Chapter 11 of Cheng, Dey and Shewchuk presents it as refinement for sliver exudation.
- **Random perturbation.** Chew (1997) and Li and Teng (2001) remove slivers by choosing each new vertex at random in a small region around the circumcenter, with probabilistic arguments and, again, very small constants.
- **Lattice methods.** [Isosurface stuffing](/isosurface-stuffing/) proves dihedral angles of at least $10.78°$, a far better constant, by giving up the Delaunay property and sharp features.
- **Mesh improvement.** [Topological improvement](/topological-tetrahedral-mesh-improvement/) and [optimization-based smoothing](/optimization-based-mesh-smoothing/) have no guarantee but reach $30°$ or more in practice.
- **Weighted features.** [Protecting balls](/protecting-balls/) use the same weighted Delaunay machinery to keep sharp edges in the mesh.

## When to use it

Use it as a last step after tetrahedral Delaunay refinement when slivers remain, the vertices must not move, and a weighted Delaunay mesh is acceptable for the solver. It works best in the interior of the domain. If the target is a specific dihedral angle such as $15°$ or more, use mesh improvement instead or after it, because the proved constant gives no such assurance.

## Pitfalls

- **Expecting a usable constant.** The theorem gives only existence; the measured $5°$ is what to expect.
- **Weights too large.** Above $\Omega_0 = \frac12$ two spheres can overlap and a vertex can become redundant and vanish from the triangulation.
- **Ignoring the boundary.** Near the boundary the star is cut off and pumping has few options; Edelsbrunner and Guoy also bound weights so that boundary triangles stay in the mesh.
- **Inexact power tests.** The critical weights are close together for a sliver, and a floating point comparison can choose a weight on a critical value, where four weighted points are coplanar in the lifted space.
- **Confusing the measures.** The paper's sliver measure $\Sigma$ is a volume ratio, not a dihedral angle; the dihedral bound needs a second step.

## Implementations

## History

Slivers were known as the weak point of three-dimensional Delaunay refinement through the 1990s: Shewchuk's 1998 analysis bounds only the radius-edge ratio, and Chew's 1997 method removes slivers by random choice with a weak guarantee. Cheng, Dey, Edelsbrunner, Facello and Teng presented sliver exudation at SoCG 1999 and in the Journal of the ACM in 2000, with the first proof that weights alone can remove slivers. Edelsbrunner and Guoy tested it in 2002 and found the minimum angle reaches about $5°$ in practice. Cheng and Dey combined it with refinement for domains with boundaries, and the material forms Chapters 10 and 11 of Cheng, Dey and Shewchuk's *Delaunay Mesh Generation* (2013).

## References
