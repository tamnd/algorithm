---
tag: RQH8DT
kind: algorithm
slug: barnes-hut-algorithm
name: Barnes-Hut algorithm
aliases:
- Barnes-Hut tree code
- Barnes-Hut simulation
area: scientific-computing/n-body-and-particle-methods
level: core
summary: "Builds an octree of the particles and treats each far cell as one pseudo-particle at its center of mass; a force step costs O(N log N) for non-pathological distributions."
model: real-ram
complexity:
  vars: {N: the number of particles}
  time: {best: "Θ(N log N)", average: "Θ(N log N)", worst: "Θ(N^2)"}
  space: {extra: "Θ(N)"}
properties: {deterministic: true}
history:
  year: 1986
  people: [Josh Barnes, Piet Hut]
  note: Barnes and Hut published the tree code with an octree rebuilt at each step and the opening angle criterion in Nature in 1986.
prereqs: [direct-n-body-summation, octree, multipole-expansion, multipole-acceptance-criterion]
see_also: [fast-multipole-method, hashed-oct-tree, gravitational-softening, quadtree, treepm-method, particle-mesh-method, kd-tree, z-order-curve]
sources:
  - paper: doi:10.1038/324446a0
    title: "Josh Barnes and Piet Hut, A hierarchical O(N log N) force-calculation algorithm, Nature 324, 1986, 446-449"
    locator: the tree construction, the opening criterion and the cost estimate
  - paper: doi:10.1006/jcph.1994.1050
    title: "John K. Salmon and Michael S. Warren, Skeletons from the treecode closet, Journal of Computational Physics 111(1), 1994, 136-155"
    locator: the error analysis of the opening criterion
  - book: isbn:9780521432726
    title: Sverre J. Aarseth, Gravitational N-Body Simulations, Tools and Algorithms, Cambridge University Press, 2003
    locator: Chapter 6 (tree codes), Section 6.2 (basic formulation)
  - paper: doi:10.1111/j.1365-2966.2005.09655.x
    title: "Volker Springel, The cosmological simulation code GADGET-2, Monthly Notices of the Royal Astronomical Society 364(4), 2005, 1105-1134"
    locator: Section 3.1 (the tree algorithm and its opening criteria)
---

The Barnes-Hut algorithm computes approximate gravitational forces on $N$ bodies with a tree. It puts the bodies in an [octree](/octree/) (a [quadtree](/quadtree/) in 2D), stores in each cell the total mass and the center of mass, and for each body walks the tree from the root. A cell that is small compared with its distance, $s / d < \theta$ by the [multipole acceptance criterion](/multipole-acceptance-criterion/), acts as one body at its center of mass; a cell that is too close is opened, and its children are tested. For well-spread distributions and a fixed $\theta$, each walk visits $O(\log N)$ cells, so a force step costs $O(N \log N)$ instead of the $\Theta(N^2)$ of [direct summation](/direct-n-body-summation/). The opening angle $\theta$ sets the trade between speed and accuracy: $\theta = 0$ gives direct summation, and $\theta \approx 0.5$ to $0.7$ gives force errors of about one percent. It is the base of most collisionless tree codes for galaxies and cosmology.

## In plain words

To find the pull of a distant group of stars, you do not need each star. The group pulls almost like one heavy star at its center. A group that is close needs more detail.

So put all bodies in a box, and cut the box into eight smaller boxes, and cut again, until each box holds at most one body. Each box remembers its total weight and its center. To find the pull on one body, start with the biggest box. If a box looks small from where the body is, use it as one heavy star. If it looks big, look inside it at its smaller boxes. Far away, big boxes are enough, so each body needs far fewer steps than one for each other body.

## The problem

The input is $N$ masses $m_i > 0$, positions $\mathbf{x}_i \in \mathbb{R}^3$, $G$ ($G = 1$ in code units), a softening parameter $\epsilon \ge 0$ and an opening angle $\theta \ge 0$. The output is an approximation $\tilde{\mathbf{a}}_i$ of each acceleration

$$\mathbf{a}_i = G \sum_{j \ne i} m_j \frac{\mathbf{x}_j - \mathbf{x}_i}{\left(|\mathbf{x}_j - \mathbf{x}_i|^2 + \epsilon^2\right)^{3/2}},$$

with the error measured against direct summation as $|\tilde{\mathbf{a}}_i - \mathbf{a}_i| / |\mathbf{a}_i|$. The error is controlled by $\theta$, not bounded by a given tolerance.

## The algorithm

```pseudo id=main
BARNES-HUT(m, x, theta, epsilon, G)
L1  root ← the smallest cube that holds all bodies
L2  for i ← 1 to N do INSERT(root, i)
      INSERT(C, i):
L3      if C is a leaf with no body then store i in C; return
L4      if C is a leaf with body k then split C into 8 children; move k to its child
L5      INSERT(the child of C whose cube holds x_i, i)
L6  for each cell C, children first do  M_C ← total mass;  z_C ← center of mass
    for i ← 1 to N do  a_i ← 0;  WALK(root):
L7      if C is a leaf then add the pair force of each body j ≠ i in C to a_i
L8      else if s_C / |z_C - x_i| < theta and x_i is not in C then
            add G M_C (z_C - x_i) / (|z_C - x_i|² + epsilon²)^{3/2} to a_i
L9      else WALK each child of C
L10 return a
```

Lines L1 to L5 build the tree by insertion. A leaf holds one body; when a second body arrives, line L4 splits the leaf and moves the first body down, so the tree is as deep as needed to separate the bodies. Line L6 fills in the monopole of each cell from its children in one pass from the leaves up. Lines L7 to L9 are the walk for one target. The test "$\mathbf{x}_i$ is not in $C$" of line L8 stops a cell from acting on a body inside it, which the bare $s / d$ test allows for $\theta > 1/\sqrt{3}$. The code stops splitting at a fixed depth, so bodies at the same point share one leaf.

## Example

Take $N = 300$ bodies with masses uniform in $[0.5, 1.5]$ and positions uniform in the cube $[-1, 1]^3$ (seed 1), $G = 1$ and $\epsilon = 0$. Direct summation uses $300 \cdot 299 = 89700$ pair interactions (each ordered pair once). The walk of this implementation gives:

| $\theta$ | interactions | median relative force error | largest relative force error |
|---|---|---|---|
| 1.0 | 10417 | $4.0 \times 10^{-2}$ | 1.31 |
| 0.7 | 20143 | $1.6 \times 10^{-2}$ | 0.17 |
| 0.5 | 34319 | $5.7 \times 10^{-3}$ | 0.038 |
| 0.3 | 61433 | $9.7 \times 10^{-4}$ | 0.018 |
| 0 | 89700 | $6 \times 10^{-16}$ | $3 \times 10^{-15}$ |

These are measurements. The median error falls by a factor of about 40 from $\theta = 1$ to $\theta = 0.3$, faster than $\theta^2$, which is the size of the quadrupole term of the [multipole expansion](/multipole-expansion/) relative to the monopole. The largest error is much larger than the median: a few bodies have a small total force, and a large relative error. At $\theta = 0$ the result agrees with direct summation up to rounding.

## Correctness

By Lemma 1 of the proof file, the tree puts each body in exactly one leaf, and the cells below any cell partition its bodies. The walk replaces a cell either by its monopole, by its bodies (at a leaf) or by its children, so each body other than $i$ contributes exactly once, either directly or through the monopole of exactly one accepted cell (Lemma 3). With $\theta = 0$ no cell is accepted, and the result is the direct sum (Theorem 1). For an accepted cell with all bodies within $b < d$ of the center of mass, the error of the monopole potential is at most $G M b^2 / (d^2 (d - b))$, because the dipole term about the center of mass is zero (Theorem 2). In 3D, $b \le \sqrt{3}\, s$, so for $\theta < 1/\sqrt{3}$ the relative error of each accepted cell is below $(\sqrt{3}\,\theta)^2 / (1 - \sqrt{3}\,\theta)$. For larger $\theta$ no bound in terms of $\theta$ holds, which is why codes add refinements to the criterion.

## Complexity

The model is the [real RAM](/real-ram/), with $N$ bodies in 3D.

- **Tree build.** Each insertion walks down one path, so the build costs $O(N \cdot \text{depth})$. For bodies with a bounded ratio of the largest to the smallest distance, the depth is $O(\log N)$ (theorem for this case), and line L6 costs $O(\text{number of cells}) = O(N \cdot \text{depth})$.
- **Walk, uniform case (argument, not a theorem).** At a level with cells of side $s$, the cells that the target must open lie within distance about $s / \theta$ of it, and there are $O(\theta^{-3})$ of them. Each opened cell has at most 8 children, so each level costs $O(\theta^{-3})$, and the walk costs $O(\theta^{-3} \log N)$. Over all targets this is $O(N \log N)$ for a fixed $\theta$ (Barnes and Hut 1986). In this implementation, with the same kind of random bodies (seed 3), the count per body grows slowly: 48, 59 and 78 interactions per body for $N = 125$, $250$ and $500$ at $\theta = 0.7$ (measurement).
- **Worst case.** Bodies with very different scales make a deep tree: for example, bodies at $2^{-k}$ for $k = 1, \ldots, N$ along a line give depth $\Theta(N)$, and the build costs $\Theta(N^2)$. The walk is also at most $\Theta(N^2)$ in total, since each target visits each cell at most once.
- **Space.** $\Theta(N)$ cells when the depth is $O(\log N)$, with one mass and one center of mass each.

## Properties

- **Not symmetric.** The force of a cell on body $i$ and the force of body $i$ on the bodies of that cell come from different approximations, so momentum is not conserved exactly. The momentum error is of the order of the force error.
- **Controlled by one parameter.** $\theta$ sets the error and the cost. The error is not bounded by a tolerance given in advance, unlike in the [fast multipole method](/fast-multipole-method/).
- **Adaptive.** The tree follows the mass, so dense regions get deep trees, and empty regions cost nothing.
- **Rebuilt each step.** The original algorithm rebuilds the tree at each step, which costs $O(N \log N)$ like the walk.

## Variants and improvements

- **Quadrupole moments.** Storing the traceless quadrupole of each cell removes the leading error term and allows a larger $\theta$ for the same accuracy.
- **Other criteria.** The offset criterion, the error-bound criteria of Salmon and Warren, and the relative criterion of GADGET-2; see [multipole acceptance criterion](/multipole-acceptance-criterion/).
- **Group walks.** Bodies of one small cell share one walk and one interaction list, which is good for vector and GPU hardware.
- **Parallel trees.** The [hashed oct-tree](/hashed-oct-tree/) stores cells in a hash table with [Morton keys](/z-order-curve/), and the bodies are divided among processors by a space-filling curve.
- **Hybrid codes.** [TreePM](/treepm-method/) uses the tree only for the short-range part of the force and a [mesh](/particle-mesh-method/) for the long-range part.
- **Fast multipole method.** The [FMM](/fast-multipole-method/) adds cell-to-cell interactions with local expansions and reaches $O(N)$ for a fixed accuracy.

## When to use it

Use Barnes-Hut for collisionless systems with $10^4$ or more bodies, where force errors of 0.1 to 1 percent are acceptable, such as galaxies, dark matter halos and the formation of structure, with [softening](/gravitational-softening/). Use it for open boundaries and very clustered mass, where a mesh is not efficient. Use [direct summation](/direct-n-body-summation/) for small $N$ and for collisional systems, where every encounter matters, and the [fast multipole method](/fast-multipole-method/) when a guaranteed accuracy or $O(N)$ cost is needed.

## Pitfalls

- **Large opening angles.** For $\theta > 1/\sqrt{3}$ the bare test can accept a cell that contains the target, and the force error has no bound. Add the test of line L8 or the offset criterion.
- **Measuring the error at one $\theta$ only.** The error depends on the distribution. Measure it against direct summation on a sample of bodies for the actual problem.
- **Ignoring the tail of the error distribution.** The median error can be small while a few bodies have large errors. Report a high percentile as well.
- **Coincident bodies.** Without a depth limit or a bucket of several bodies per leaf, two bodies at the same point make the insertion run forever.
- **Momentum drift.** The forces are not symmetric, so the total momentum drifts. This is not an error of the integrator.

## Implementations

## History

Barnes and Hut published the algorithm in 1986, after earlier tree methods of Appel (1985) and others. Their octree is rebuilt at each step, uses monopoles (later quadrupoles), and has the opening angle criterion. Salmon and Warren (1994) showed that the criterion can give unbounded errors and gave error bounds, and Warren and Salmon built parallel codes with a [hashed oct-tree](/hashed-oct-tree/). Tree codes such as GADGET-2 (Springel 2005) carry the method to cosmological simulations with billions of bodies.

## References
