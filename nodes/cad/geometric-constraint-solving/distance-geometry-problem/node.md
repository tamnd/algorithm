---
tag: Q3DH81
kind: problem
slug: distance-geometry-problem
name: Distance geometry problem
aliases:
- graph realization problem
- molecular distance geometry problem
area: cad/geometric-constraint-solving
level: core
summary: Find points in d dimensions whose distances match given values on the edges of a graph. It is strongly NP-hard in every dimension and is the core of distance constraint solving.
prereqs: [bar-and-joint-framework, np-hard]
see_also: [cayley-menger-determinant, multidimensional-scaling, semidefinite-programming, partition-problem, global-rigidity, rigidity-matrix, root-identification-problem, constructive-constraint-solving]
sources:
  - paper: "James B. Saxe, Embeddability of weighted graphs in k-space is strongly NP-hard, Proceedings of the 17th Allerton Conference on Communication, Control and Computing, 480 to 489, 1979"
    locator: NP-completeness on a line, strong NP-hardness in every dimension k, hardness with edge weights 1 and 2, and hardness of deciding whether a second embedding exists
  - paper: doi:10.1137/120875909
    title: Leo Liberti, Carlile Lavor, Nelson Maculan and Antonio Mucherino, Euclidean distance geometry and applications, SIAM Review 56(1), 3 to 69, 2014
    locator: the definition of the problem and its variants, complexity, the case of complete graphs, discretizable instances and branch and prune, semidefinite and global optimization methods, and applications to molecules and sensor networks
  - paper: doi:10.1007/978-1-4614-0110-0_24
    title: Marcus Schaefer, Realizability of graphs and linkages, in Thirty Essays on Geometric Graph Theory, Springer, 461 to 482, 2013
    locator: realizability of linkages in the plane is complete for the existential theory of the reals, also with unit lengths
  - paper: doi:10.2307/1968654
    title: I. J. Schoenberg, Remarks to Maurice Fréchet's article "Sur la définition axiomatique d'une classe d'espaces distanciés vectoriellement applicable sur l'espace de Hilbert", Annals of Mathematics 36(3), 724 to 732, 1935
    locator: the complete graph case, solved by the positive semidefinite Gram matrix
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, CRC Press, 2018
    locator: the chapters on distance constraint systems and their realization
---

The distance geometry problem asks for points that fit a list of distances. Some pairs of points come with a required distance, and the task is to place all points in the line, the plane or space so that every listed pair is exactly that far apart. A CAD sketch with only distance constraints, a molecule with distances from NMR, and a sensor network with ranges between nodes are all this problem. It is hard in general, already on a line, but it is easy when every distance is given, and practical when the points can be placed one at a time.

## In plain words

You have a set of pins and a set of strings, and each string has a fixed length and ties two pins together. You want to put the pins on a table so that every string is pulled tight. Sometimes there is no way to do it, sometimes there is exactly one way, and sometimes there are many. Finding a way, or proving that none exists, can take a very long time once there are many strings. If you know the distance between every pair of pins, though, there is a quick and direct method.

## Definition

**Input.** A graph $G = (V, E)$ with $n$ vertices, a length $d_{uv} > 0$ for each edge $uv \in E$, and a dimension $K \ge 1$. In complexity statements the lengths are integers.

**Output.** A *realization*: a map $p : V \to \mathbb{R}^K$ with
$$ \lVert p_u - p_v \rVert = d_{uv} \quad \text{for every } uv \in E, $$
or the answer that none exists. The decision version asks only whether a realization exists. Points of different vertices may coincide. A realization is never unique, since every rigid motion of $\mathbb{R}^K$ maps it to another, so "unique" always means unique up to congruence.

The triple $(G, d, K)$ is a system of $|E|$ quadratic equations $\lVert p_u - p_v \rVert^2 = d_{uv}^2$ in $Kn$ unknowns. In the language of rigidity, a realization is a [bar-and-joint framework](/bar-and-joint-framework/) $(G, p)$ with the given bar lengths.

## Variants

- **Complete graph (Euclidean distance matrix).** All $\binom{n}{2}$ distances are given. This case is solved in polynomial time; see Known algorithms.
- **Matrix completion form.** Some entries of the squared distance matrix are given and the rest must be filled so that the result is a Euclidean distance matrix of rank at most $K$, in the sense of the [Cayley-Menger determinant](/cayley-menger-determinant/) conditions.
- **Molecular distance geometry problem.** $K = 3$, with distances from bond lengths, bond angles and NMR measurements, often given as intervals $[\ell_{uv}, u_{uv}]$ instead of exact values.
- **Sensor network localization.** $K = 2$ or $3$, where some vertices, the anchors, have known positions and the rest must be located from measured ranges.
- **Discretizable instances.** There is an order of the vertices such that each vertex after the first $K$ has edges to at least $K$ earlier ones, which form a simplex in general position. Then each new vertex has at most two positions, and a search tree of depth $n$ finds all realizations.
- **Uniqueness.** Given a realization, decide whether it is the only one up to congruence. For generic instances this is the [global rigidity](/global-rigidity/) of the graph.
- **Approximate version.** Minimize $\sum_{uv \in E} \big(\lVert p_u - p_v \rVert^2 - d_{uv}^2\big)^2$, which is zero exactly at realizations. Measured data are noisy, so this is the form solved in practice.

## Examples

- **A triangle.** Three vertices with all three edges have a realization in the plane exactly when the lengths satisfy the triangle inequality. The lengths $1, 1, 3$ have no realization in any dimension, and the [Cayley-Menger determinant](/cayley-menger-determinant/) of the squared lengths $1, 1, 9$ is $45 > 0$, the sign that shows it.
- **A cycle on a line.** The cycle on vertices $v_0, \ldots, v_5$ with lengths $3, 1, 1, 2, 2, 1$ along the edges $v_0 v_1, \ldots, v_5 v_0$ has the realization $0, 3, 2, 1, 3, 1$ on a line: the steps $+3, -1, -1, +2, -2, -1$ sum to 0. The lengths $3, 1, 1$ on a triangle have none, since no choice of signs makes $\pm 3 \pm 1 \pm 1 = 0$. The proof below turns this into the reduction from partition.
- **Trilateration.** Anchors at $(0, 0)$, $(4, 0)$ and $(0, 3)$ and a point $x$ with squared distances $5$, $13$ and $2$ to them. Subtracting the first equation $\lVert x \rVert^2 = 5$ from the other two gives the linear equations $-8x_1 + 16 = 8$ and $-6x_2 + 9 = -3$, so $x = (1, 2)$, the only solution.
- **Finitely many realizations.** The 4-cycle $a b c d$ in the plane with the diagonal $ac$, lengths $\lvert ab \rvert = \lvert cd \rvert = 4$, $\lvert bc \rvert = \lvert da \rvert = 3$ and $\lvert ac \rvert = 5$, is two triangles on the common side $ac$. Each triangle can lie on either side of $ac$, so up to congruence there are two realizations: the rectangle, with $\lvert bd \rvert = 5$, and the folded shape with $\lvert bd \rvert = 7/5$. This is the generic situation for a rigid graph that is not globally rigid.
- **Infinitely many realizations.** The 4-cycle with four sides of length 1 in the plane has a one-parameter family of realizations, the rhombi. Its graph is not rigid.
- **All distances given.** The four corners of a $4 \times 3$ rectangle with all six distances. The Gram matrix built from the squared distances has rank 2, and its factorization returns the corners up to congruence.

## Known algorithms

- **Complete graphs: Gram matrix factorization.** Fix vertex $0$ and form $G_{ij} = (d_{0i}^2 + d_{0j}^2 - d_{ij}^2)/2$. A realization in $\mathbb{R}^K$ exists exactly when $G$ is positive semidefinite of rank at most $K$, by Schoenberg's theorem, and the factorization $G = U^T U$ gives the points. With an eigenvalue decomposition or an $LDL^T$ variant of [Cholesky decomposition](/cholesky-decomposition/) this costs $O(n^3)$ arithmetic operations. Classical [multidimensional scaling](/multidimensional-scaling/) is the same method with a centred Gram matrix, and on noisy data it keeps the $K$ largest eigenvalues.
- **Trilateration and constructive solving.** If the vertices can be ordered so that each new vertex has $K + 1$ placed neighbours in general position, every new point solves a linear system, and the realization is unique and found in $O(n K^3)$ time. With only $K$ placed neighbours each step has two solutions, as with a [circle-circle intersection](/circle-circle-intersection/) in the plane. This is [constructive constraint solving](/constructive-constraint-solving/), and the choice among the $2^n$ branches is the [root identification problem](/root-identification-problem/).
- **Branch and prune.** For discretizable instances, a depth-first search places the vertices in order, tries both positions of each, and prunes a branch as soon as an extra distance fails. It lists all realizations, in exponential time in the worst case, and works well on protein backbones.
- **Semidefinite relaxation.** Replace the Gram matrix of the unknown points by a matrix variable $X \succeq 0$ whose entries satisfy the linear equations $X_{uu} + X_{vv} - 2X_{uv} = d_{uv}^2$, and drop the rank condition. This is a [semidefinite program](/semidefinite-programming/). When the instance has a unique realization in all dimensions at once, which is universal rigidity, the relaxation returns it, as shown by So and Ye for sensor networks.
- **Local and global optimization.** Minimize the approximate form above with [gradient descent](/gradient-descent/), [Levenberg-Marquardt](/levenberg-marquardt/) or a [Newton method](/newton-method-for-systems/), usually from a starting point given by a relaxation. The function is not convex, so [global optimization](/global-optimization/) methods or many restarts are needed for a guarantee.
- **Exact algebraic methods.** Small systems are solved as polynomial systems, by Gröbner bases or [homotopy continuation](/homotopy-continuation/), which return all complex solutions and filter the real ones.

## Bounds

**Theorem (Saxe 1979).** The distance geometry problem with integer lengths is NP-complete for $K = 1$, and strongly NP-hard for every fixed $K \ge 1$. It stays NP-hard when every length is 1 or 2. Deciding whether an instance with a given realization has a second realization not congruent to it is also NP-hard for every $K$.

The full proofs reduce from [3-SAT](/3-sat/) with gadgets of lengths 1 and 2. The weaker statement for $K = 1$ has a short proof.

**Proof that the line case is NP-complete.** *Membership.* On a line, $p_v - p_u = \pm d_{uv}$ for every edge. Fix a spanning forest. A realization is determined, up to translation of each component, by one sign per tree edge, and every position is an integer sum of lengths. So the signs are a certificate of polynomial size, and checking all edges takes linear time. *Hardness.* Reduce from the [partition problem](/partition-problem/): given positive integers $a_1, \ldots, a_m$, decide whether they split into two parts with equal sums. Build the cycle $v_0 v_1 \cdots v_{m - 1} v_0$ with $d_{v_{i - 1} v_i} = a_i$, indices modulo $m$. A realization gives signs $s_i = (p_{v_i} - p_{v_{i - 1}})/a_i \in \{+1, -1\}$, and going once around the cycle gives $\sum_i s_i a_i = 0$, so the indices with $s_i = +1$ form a partition. Conversely, a partition gives signs with $\sum_i s_i a_i = 0$, and the partial sums $p_{v_j} = \sum_{i \le j} s_i a_i$ are a realization. The reduction takes linear time. $\square$

This reduction alone gives only weak hardness, since partition is solved in [pseudo-polynomial time](/pseudo-polynomial-time/) by the [subset sum](/subset-sum-problem/) table, and so is the cycle on a line. Saxe's 3-SAT reduction uses only lengths 1 and 2, which is why the hardness is strong: it holds even when the lengths are written in unary.

**Upper bounds.** For $K = 1$ the problem is in NP. For $K \ge 2$ a realization may need irrational coordinates, as in an equilateral triangle, so a list of coordinates is not an obvious certificate, and membership in NP is open. The problem is a system of polynomial equations over the reals, so it lies in the existential theory of the reals and can be decided in polynomial space. Schaefer (2013) showed that in the plane it is complete for that class, also when every length is 1.

**What is measured and what is proved.** The hardness results are worst-case theorems. The good behaviour of branch and prune on protein data, and of semidefinite relaxations on random sensor networks, is measured on families of instances, not proved for all inputs.

## Reductions

- **From partition and 3-SAT.** The reductions above. The cycle construction is the simplest, and Saxe's 3-SAT gadgets give strong hardness in every dimension.
- **To rigidity.** For generic lengths, the number of realizations is finite exactly when the graph is rigid, which the [rigidity matrix](/rigidity-matrix/) decides by a rank, and unique exactly when the graph is globally rigid. These properties depend on the graph only, but they say nothing about whether a given instance has any realization.
- **To matrix completion.** Realizability is the completion of a partial squared distance matrix to a Euclidean distance matrix of rank at most $K$, that is, a positive semidefinite Gram matrix of rank at most $K$. Dropping the rank bound gives a semidefinite feasibility problem.
- **To polynomial systems.** Every instance is a system of quadratic equations, and every algebraic method for real polynomial systems applies, with the cost of such methods.

## Applications

- **Distance constraints in CAD.** A 2D sketch or a 3D assembly with only point-to-point distance constraints is an instance with $K = 2$ or $3$. Constraint solvers use decomposition into rigid clusters, as in [DR-plans](/dr-plan/), to break it into small instances that are solved by construction.
- **Protein structure.** NMR experiments give distance intervals between nearby hydrogen atoms, and bond lengths and angles give exact distances. The structure is a realization in $\mathbb{R}^3$.
- **Sensor networks and robot formations.** Nodes measure distances to their neighbours, and anchors know their positions. Localization is the anchored version with $K = 2$ or $3$, and [distance-based formation control](/distance-based-formation-control/) keeps a team of robots at the distances of a target realization.
- **Data visualization.** [Multidimensional scaling](/multidimensional-scaling/) places items in the plane so that their distances approximate given dissimilarities, an approximate version on the complete graph.

## References
