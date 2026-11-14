---
tag: 9DFJ45
kind: algorithm
slug: optimization-based-mesh-smoothing
name: Optimization-based mesh smoothing
aliases:
- Freitag-Plassmann smoothing
- local mesh optimization
area: cad/mesh-generation-for-analysis
level: advanced
summary: Moves each vertex to maximise the worst quality of its incident elements, a nonsmooth optimisation that, unlike Laplacian smoothing, cannot invert elements.
solves: [mesh-generation]
model: real-ram
complexity:
  vars: {d: the number of elements around the vertex, s: the number of steps}
  time: {per-vertex: O(s d^3)}
  space: {extra: O(d)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2000
  people: [Lori A. Freitag, Paul Plassmann]
  note: Freitag and Plassmann published the max-min local optimisation of element quality with an active set and a steepest ascent direction, and untangling by linear programming, in 2000, after earlier work by Freitag and coauthors on parallel smoothing.
prereqs: [mesh-quality-measures, laplacian-smoothing, subgradient]
see_also: [mesh-untangling, optimal-delaunay-triangulation, quadratic-programming, gradient-descent, bundle-method, topological-tetrahedral-mesh-improvement, convex-function, mesh-generation]
sources:
  - paper: doi:10.1002/1097-0207(20000910/20)49:1/2<109::AID-NME925>3.0.CO;2-U
    title: Lori A. Freitag and Paul Plassmann, Local optimization-based simplicial mesh untangling and improvement, International Journal for Numerical Methods in Engineering 49(1-2), 2000, 109 to 125
    locator: the max-min formulation, the convexity of the level sets of the quality measures, the active set and the search direction of least norm, and the line search (general locator)
  - book: isbn:978-1-84821-029-5
    title: Pascal Jean Frey and Paul-Louis George, Mesh Generation, Application to Finite Elements, 2nd edition, ISTE and Wiley, 2008
    locator: chapter 18 (mesh optimisation, including point relocation)
---

Optimization-based mesh smoothing moves one vertex of a mesh at a time to the position that makes the worst element around it as good as possible. The worst quality is the minimum of several smooth functions, so it has corners and ordinary gradient methods do not apply. Freitag and Plassmann solve it as a nonsmooth problem: they keep the set of elements that are nearly the worst, take the direction of least norm in the convex hull of their quality gradients, and search along it. A step is accepted only if the worst quality goes up and no element turns over, so, unlike [Laplacian smoothing](/laplacian-smoothing/), the method never inverts an element. For the mean ratio of triangles the problem has convex level sets, so a stationary point is the best position over the whole star.

## In plain words

A point of a mesh is joined to a ring of neighbours. Each triangle around it has a score, and the worst score is what matters, because one bad triangle can spoil a simulation.

The method looks at the triangles that are now the worst, and finds a direction that makes all of them better at the same time. It moves the point a little in that direction, but only if the worst score really goes up and no triangle turns inside out. When no direction helps the worst triangles together, it stops.

Laplacian smoothing simply moves the point to the middle of its neighbours. That is cheap, but in a ring shaped like an arrow the middle can lie outside the ring, and a triangle flips over. This method checks every move, so that cannot happen.

## The problem

A free vertex at $x$ has star triangles $\tau_i = (x, a_i, b_i)$ whose outer edges form a closed polygon, the link. The quality of $\tau_i$ is the mean ratio from the [mesh quality measures](/mesh-quality-measures/),

$$q_i(x) = \frac{4\sqrt3\,A_i(x)}{\ell_{i1}^2 + \ell_{i2}^2 + \ell_{i3}^2},$$

which is 1 for an equilateral triangle, 0 for a flat one and negative for a clockwise one. The problem is to find

$$\max_{x \in K} Q(x), \qquad Q(x) = \min_i q_i(x),$$

where $K$, the kernel of the star, is the set of positions with all $A_i > 0$. $Q$ is not differentiable where two qualities tie, which is the usual case at the optimum, because if one quality were alone at the bottom the point could move to raise it. For a whole mesh, the method is applied to each free vertex in turn.

## The algorithm

ORIENT2D is the exact [orientation test](/orientation-test/). The tolerance $\delta$ defines the active set, and $\varepsilon$ the stopping test.

```pseudo id=main
SMOOTH-VERTEX(x, link)
L1  if ORIENT2D(x, a_i, b_i) ≤ 0 for some i then fail   ▷ tangled: untangle first
L2  repeat at most max_iter times
L3      q_i ← q_i(x) for all i;  m ← min_i q_i
L4      I ← {i : q_i ≤ m + δ};  G ← {∇q_i(x) : i ∈ I}
L5      d ← the point of least norm in the convex hull of G
L6      if |d|² ≤ ε then return x                        ▷ stationary
L7      α ← min over inactive j with |d|² > ∇q_j · d of (q_j − m) / (|d|² − ∇q_j · d), or 1 if none
L8      halve α until x + αd passes ORIENT2D for all i and min_i q_i(x + αd) > m, at most 60 times
L9      if no α passed then return x
L10     x ← x + αd
L11 return x
```

L5 is a small quadratic program. In the plane the hull of the gradients is a polygon, and its point of least norm is the origin, a gradient, or the foot of the origin on a segment between two gradients, so it is found by checking these cases. L7 predicts the step from linear models: along $d$, every active quality rises at rate at least $|d|^2$, and the step ends where an inactive quality, rising more slowly, would meet them. L8 then backtracks until the real worst quality rises. In 3D the same scheme works with the tetrahedron mean ratio $12(3V)^{2/3}/\sum \ell^2$ and a small quadratic program in L5.

## Example

Take a free vertex at the origin with the link polygon $(-2, 0)$, $(0, -2)$, $(6, -1)$, $(1, 0)$, $(6, 1)$, $(0, 2)$, shaped like an arrow pointing left with a notch at $(1, 0)$. The six triangles from the origin are counterclockwise, and the worst mean ratio is 0.0541.

Laplacian smoothing moves the vertex to the mean of the link vertices, $(11/6, 0)$. That point is beyond the notch, outside the kernel. The two triangles at the notch, $(x, (6,-1), (1,0))$ and $(x, (1,0), (6,1))$, become clockwise, with mean ratio $-0.0641$ each.

Max-min smoothing takes 4 accepted steps. The worst quality goes $0.0541, 0.0979, 0.1010, 0.1011, 0.1011$, and the vertex ends at about $(-1.778, 0)$, where four of the six triangles tie at 0.1011. A grid search over the kernel with step about 0.05 finds its best value 0.1004 near $(-1.733, 0)$, slightly below, as a grid must be. The best position is near the left corner, because the two long thin triangles toward $(6, \pm1)$ are bad from anywhere.

On a $5 \times 5$ square grid split into 50 triangles, with the 16 inner vertices moved randomly by up to 0.35, the worst mean ratio is 0.224. Sweeps of max-min smoothing over the inner vertices raise it to 0.695 after one sweep, 0.814 after three and 0.846 after five. Three sweeps of Laplacian smoothing give 0.855 on the same mesh. On a convex, nearly regular mesh Laplacian smoothing does as well; the gain of max-min is safety on bad stars. These are measurements.

## Correctness

The full proof is in the proof file. Validity and monotonicity follow from the acceptance test of L8: the exact orientation test keeps every position in the kernel, and the worst quality rises at each accepted step. Since the other triangles of the mesh do not change, the worst quality of the whole mesh never goes down.

The optimality statement uses the shape of the quality. On the kernel, $q_i(x) \ge t$ is the same as $4\sqrt3\,A_i(x) - t\,S_i(x) \ge 0$, where $A_i$ is affine and the sum of squared edge lengths $S_i$ is a convex quadratic, so the left side is a concave function and its superlevel set is convex. If $0$ is in the convex hull of the active gradients at $x$ but some $y$ in the kernel were better, concavity would give $\nabla q_i(x) \cdot (y - x) > 0$ for every active $i$, so no convex combination of these gradients could be zero. So a stationary point is a global maximum over the kernel. When $d \ne 0$, the least norm property gives $\nabla q_i \cdot d \ge |d|^2$ for every active $i$, so $d$ is a direction of ascent of the worst quality, like a [subgradient](/subgradient/) step for a concave function.

What is measured is the quality value reached and how many steps it takes. What is proved is that elements never invert, the worst quality never goes down, and stationary points are optimal for one vertex.

## Complexity

One iteration computes $d$ qualities and gradients in $O(d)$ time, solves the least norm problem over at most $d$ gradients, which costs $O(d^3)$ with the case check of the plane and is constant in practice because the active set has two to four members, and runs a line search of at most 60 trials of $O(d)$ each. With $s$ steps, a vertex costs $O(s d^3)$ in the worst case, and the number of steps is small in practice, often under 10. A sweep over a mesh with $n$ free vertices costs $O(n)$ vertex smoothings. Each vertex costs more than a Laplacian move, which is one average, so codes often apply the method only where the quality is below a threshold. The space is $O(d)$.

## Properties

- **Never inverts, proved.** Each accepted position passes an exact orientation test.
- **Monotone, proved.** The worst quality of the star, and of the mesh, never goes down.
- **Globally optimal for one vertex, proved.** For the mean ratio, the level sets are convex, so a stationary point is the best position in the kernel.
- **Local in the mesh.** Vertices are moved one at a time; the result over a mesh is not a joint optimum.
- **Nonsmooth.** The objective is a minimum of smooth functions, so the method works with an active set.

## Variants and improvements

- **Smart Laplacian.** Move the vertex to the Laplacian target only if the worst quality rises; otherwise keep it. This is cheaper but stops at worse positions.
- **Combined smoothing.** Use Laplacian smoothing first and the max-min method only for vertices whose star has quality below a threshold. Freitag studied such combinations in the late 1990s.
- **Other measures.** The same scheme works with the smallest angle, the smallest sine of a dihedral angle in 3D, or the condition number of the element Jacobian. The convexity of level sets must be checked for each measure.
- **Linear programming.** Amenta, Bern and Eppstein showed that for some measures, such as the smallest angle, the best position solves an LP-type problem, which can be solved in linear time in the number of elements for a fixed dimension.
- **Untangling.** If the kernel is empty or the start is tangled, [mesh untangling](/mesh-untangling/) maximises the smallest signed area first, which Freitag and Plassmann pose as a [linear program](/linear-programming-problem/).
- **With topology changes.** In 3D, smoothing is combined with flips in [topological tetrahedral mesh improvement](/topological-tetrahedral-mesh-improvement/), because moving vertices alone cannot remove many bad tetrahedra.
- **Global energies.** [Optimal Delaunay triangulation](/optimal-delaunay-triangulation/) moves vertices to lower an integral error and changes the connectivity.

## When to use it

Use it after mesh generation when the worst element matters, for example before a finite element solve where one flat element ruins the conditioning, and when the mesh has nonconvex stars near the boundary or near features, where Laplacian smoothing can invert elements. Use plain Laplacian smoothing on a nearly regular mesh, where it is cheaper and as good. Use untangling first if some elements are already inverted.

## Pitfalls

- **Average instead of minimum.** Maximising the mean quality of the star can leave one bad element. The worst element is the target.
- **Quality measures without sign.** A measure such as the ratio of the shortest edge to the circumradius, or the absolute value of the area, is positive for a clockwise triangle too. With such a measure the line search can step out of the kernel and accept a folded star. Use a signed measure, or test the orientation.
- **Float orientation.** In exact arithmetic a rise of the signed worst quality from a positive value keeps the vertex in the kernel, but for a nearly flat element the float sign can be wrong. Test orientation exactly.
- **Tiny active set tolerance.** With $\delta = 0$, the direction ignores a quality that is about to become the worst, and the steps become very short. A small positive $\delta$ is better.
- **Expecting a fix for bad topology.** Smoothing cannot fix a vertex of degree 3 or 12 in a triangle mesh; flips are needed.

## Implementations

## History

Laplacian smoothing, in which a vertex moves to the mean of its neighbours, was the standard for many years, and it can invert elements. In the 1990s several groups moved vertices by local optimisation instead. Lori Freitag and Paul Plassmann, with Mark Jones, worked on parallel optimisation-based smoothing in the mid 1990s, and Freitag and Ollivier-Gooch combined it with face and edge swaps for tetrahedra. Amenta, Bern and Eppstein studied the problem as an LP-type problem in 1999. Freitag and Plassmann's paper of 2000 gave the active set method described here, the proof that the level sets of the common quality measures are convex, and untangling by linear programming. The method is in the Mesquite library and in many mesh generators.

## References
