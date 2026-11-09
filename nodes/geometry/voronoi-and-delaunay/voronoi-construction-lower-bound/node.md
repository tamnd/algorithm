---
tag: VZ0TX1
kind: theorem
slug: voronoi-construction-lower-bound
name: Voronoi construction lower bound
aliases:
- Omega(n log n) lower bound for Voronoi diagrams
- Delaunay triangulation lower bound
area: geometry/voronoi-and-delaunay
level: advanced
summary: Constructing a Voronoi diagram or Delaunay triangulation of n points needs Omega(n log n) time in the algebraic decision tree model.
prereqs: [voronoi-diagram, delaunay-triangulation, algebraic-decision-tree, comparison-sort-lower-bound]
see_also: [voronoi-diagram-construction, delaunay-triangulation-construction, convex-hull-lower-bound, sorting-problem, element-distinctness-lower-bound, fortunes-algorithm, dwyer-algorithm, paraboloid-lifting-map]
sources:
  - paper: doi:10.1109/SFCS.1975.8
    title: M. I. Shamos and D. Hoey, Closest-point problems, 16th Annual Symposium on Foundations of Computer Science, 1975
    locator: the reduction of sorting to the Voronoi diagram and the resulting Omega(n log n) lower bound
  - paper: "M. Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing, 1983, 80-86"
    locator: the algebraic computation tree model and lower bounds from the number of connected components
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 7 (the remark that sorting reduces to the Voronoi diagram, so the sweep is optimal)
---

The Voronoi construction lower bound says that every algorithm that computes the [Voronoi diagram](/voronoi-diagram/) or the [Delaunay triangulation](/delaunay-triangulation/) of $n$ points in the plane needs $\Omega(n \log n)$ time in the worst case, in the [algebraic decision tree](/algebraic-decision-tree/) model and in the stronger algebraic computation tree model. The reason is that the diagram holds the sorted order of the input: for points on a line or on a parabola, reading the diagram gives the points from left to right. So the $O(n \log n)$ algorithms, such as [Fortune's sweep](/fortunes-algorithm/), are optimal in these models, even for inputs in general position.

## Statement

**Setting.** $P = (p_1, \ldots, p_n)$ is a list of $n$ points $p_i = (x_i, y_i)$ in the plane, given by their $2n$ real coordinates. The output must contain the *combinatorial* Delaunay structure: the set of index triples $\{i, j, k\}$ of the Delaunay triangles, or, for the Voronoi diagram, the set of index pairs $\{i, j\}$ whose cells share an edge. Any usual output format, such as a [doubly connected edge list](/doubly-connected-edge-list/) or a [quad-edge structure](/quad-edge-data-structure/) whose records name the sites, holds this information.

**Model.** An *algebraic computation tree* is a rooted tree. A computation node computes a new value as $a + b$, $a - b$, $a \cdot b$ or $a / b$ from inputs, constants and earlier values, and has one child. A branch node tests the sign of a computed value and has at most three children, for $< 0$, $= 0$ and $> 0$. Each leaf is labelled with a fixed combinatorial answer. The *cost* of an input is the number of nodes on its path. An algebraic decision tree is the special case in which the branch nodes test the sign of a polynomial of bounded degree in the inputs. A program for the real RAM that uses no floor function and never uses a real value as a memory address unfolds into such a tree for each $n$, with cost at most its running time.

**Theorem.** Let $n \ge 3$. Every algebraic computation tree that computes the combinatorial Delaunay triangulation of $n$ points has an input of cost at least

$$\log_3 \frac{(n - 1)!}{2} \ge (n - 1) \log_3 \frac{n - 1}{e} - \log_3 2,$$

which is $\Omega(n \log n)$. This holds even if the input is restricted to points in general position: no three on a line and no four on a circle. The same bound holds for the Voronoi diagram, given as the set of pairs of sites with a common edge, with $n!/2$ in place of $(n - 1)!/2$ for collinear inputs.

Notation used on this site: $\mathrm{orient}(p, q, r)$ is positive when $p, q, r$ turn counterclockwise, and $\mathrm{incircle}(a, b, c, d)$, for counterclockwise $a, b, c$, is positive when $d$ is strictly inside their circle.

## In plain words

Put the numbers to be sorted on a curve, as points: the number $x$ becomes the point $(x, x^2)$. Then the Delaunay triangulation of these points joins each point to the next one from left to right. So a program that builds the triangulation has, in effect, sorted the numbers.

A program that only compares and computes can end in a limited number of ways: at most three ways per test. To give a different answer for each order of the numbers, it needs about $n \log n$ tests, as in sorting.

## Proof

**Lemma 1 (points on a parabola).** Let $x_1, \ldots, x_n$ be distinct positive reals and $p_i = (x_i, x_i^2)$. Then no three of the points are on a line, no four are on a circle, all of them are corners of their convex hull, and the hull, in counterclockwise order, visits them in increasing order of $x_i$. The Delaunay triangulation is unique, and its boundary edges are the pairs of points that are consecutive in the sorted order, together with the pair of the smallest and the largest.

*Proof.* A line $y = a x + b$ meets the parabola $y = x^2$ where $x^2 - a x - b = 0$, at most twice, and a vertical line meets it once. A circle $x^2 + y^2 + D x + E y + F = 0$ meets it where $x^4 + (1 + E) x^2 + D x + F = 0$. This quartic has no $x^3$ term, so if it has four real roots, their sum is $0$. Four positive numbers do not sum to $0$, so no four points are on one circle. The parabola is the graph of a strictly convex function, so each point lies strictly below the chord of any two points on either side of it, and the points are in convex position. Walking counterclockwise, the lower chain of the hull goes from left to right through all the points, since every point is below the chord from the leftmost to the rightmost point, and the upper chain is the single edge back from the rightmost to the leftmost point. With no four points on a circle, the Delaunay triangulation is unique, and like every triangulation of a point set it contains all hull edges as boundary edges and no other boundary edges. $\square$

**Lemma 2 (counting leaves).** Let $\mathcal{T}$ be a tree whose nodes have at most three children and whose longest root-to-leaf path has $c$ branch nodes. Then $\mathcal{T}$ has at most $3^c$ leaves.

*Proof.* Computation nodes have one child and do not change the number of paths. By induction on $c$, a tree with at most $c$ branch nodes on each path has at most $3^c$ leaves. $\square$

**Proof of the theorem.** Let $\mathcal{T}$ be an algebraic computation tree that outputs the combinatorial Delaunay triangulation for every input of $n$ points in general position. Consider the inputs $p_i = (x_i, x_i^2)$ with distinct positive $x_i$; they are in general position by Lemma 1. For such an input, let $\sigma$ be the order of the indices by increasing $x_i$. By Lemma 1, the boundary edges of the output, that is, the index pairs that lie in exactly one output triangle, form the cycle $\sigma(1), \sigma(2), \ldots, \sigma(n), \sigma(1)$ on the indices. Every cyclic order of the $n$ indices arises in this way, from a suitable choice of the $x_i$, and two inputs whose cycles differ, as undirected cycles, need different outputs. There are $(n - 1)!/2$ undirected cycles through $n$ labelled vertices for $n \ge 3$. A leaf outputs one fixed answer, so $\mathcal{T}$ has at least $(n - 1)!/2$ leaves. By Lemma 2 some path has at least $\log_3 ((n - 1)!/2)$ branch nodes, and its cost is at least that.

For the estimate, $\ln m! \ge m \ln m - m$ for $m \ge 1$, because $\ln m! = \sum_{j=1}^{m} \ln j \ge \int_1^m \ln t \, dt = m \ln m - m + 1$. With $m = n - 1$ this gives the displayed bound, which is $\Omega(n \log n)$.

For the Voronoi diagram, a pair $\{i, j\}$ has a common Voronoi edge exactly when $ij$ is a Delaunay edge, by [Voronoi-Delaunay duality](/voronoi-delaunay-duality/) for points in general position, so the set of Voronoi neighbour pairs contains the same cycle and the same count applies. With collinear inputs $(x_i, 0)$ the neighbour pairs form the path of the sorted order, and the $n!/2$ undirected paths give the stronger count. $\blacksquare$

## Consequences

- **Optimal algorithms.** [Fortune's algorithm](/fortunes-algorithm/), the divide and conquer algorithms of Shamos and Hoey and of [Guibas and Stolfi](/guibas-stolfi-algorithm/), and the 3D hull method all run in $O(n \log n)$ worst-case time and are optimal in the algebraic computation tree model. The randomized incremental method is optimal in expectation.
- **Reduction from sorting.** Given distinct numbers $x_1, \ldots, x_n$, build the Delaunay triangulation of the points $(x_i, x_i^2)$ for $x_i > 0$ (shift the numbers first), find the hull cycle from the triangles that have a boundary edge, and cut it at the edge between the smallest and the largest number, which takes $O(n)$ time. So sorting reduces to Delaunay triangulation in linear time. For example, $3, 1, 4, 2$ give the points $(3,9)$, $(1,1)$, $(4,16)$, $(2,4)$; the triangulation has the triangles with indices $\{1, 2, 3\}$ and $\{1, 2, 4\}$, its boundary cycle visits the indices $2, 4, 1, 3$, and these are the numbers $1, 2, 3, 4$ in order.
- **Related problems.** The [lifting map](/paraboloid-lifting-map/) gives the same bound for the [3D convex hull](/convex-hull-3d/), and the problem of the [planar convex hull](/convex-hull-lower-bound/) has the same bound by a similar argument on the parabola. The [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) of the collinear points $(x_i, 0)$ is the sorted path, so it has the same bound.
- **Expected and output-sensitive bounds.** The theorem is about the worst case. A randomized tree also needs $\Omega(n \log n)$ expected cost on its worst input: by Yao's principle it is enough to bound the average depth of a deterministic tree over the $(n - 1)!/2$ cycles, chosen uniformly, and a tree with at most three children per node and $N$ leaves has average leaf depth at least $\log_3 N$. For the Delaunay triangulation the output always has $\Theta(n)$ size, so there is no output-sensitive speed-up of the kind that exists for convex hulls.

## Tightness

- **The model matters.** With the floor function, or with integer coordinates on a word RAM, the bound does not hold: integer sorting is faster than $O(n \log n)$, and faster Delaunay algorithms for integer coordinates are known. With random inputs, such as points uniform in a square, [Dwyer's algorithm](/dwyer-algorithm/) takes $O(n \log \log n)$ expected time, which does not contradict a worst-case bound.
- **Extra input structure.** If the points are given in the order of a convex polygon, the Delaunay triangulation takes $O(n)$ time by the algorithm of Aggarwal, Guibas, Saxe and Shor; the lower bound needs the order to be unknown. The parabola inputs of the proof are in convex position but not given in hull order.
- **Positive coordinates in Lemma 1.** Four points on the parabola can lie on one circle when their $x$-coordinates sum to $0$: for $x = -2, -1, 1, 2$ the four points have $\mathrm{incircle} = 0$. The proof uses positive $x_i$ to stay in general position.
- **The output must name the sites.** If an algorithm only outputs the coordinates of the Voronoi vertices as an unordered list of numbers, the leaf count does not apply, because the numbers are computed values and not fixed labels. Lower bounds for such outputs use the topological method of Ben-Or.
- **The constant.** The bound $\log_3((n - 1)!/2)$ is about $0.63 \, n \log_2 n$ for large $n$; the best algorithms use a few times more in-circle and orientation tests. The constant is not tight.

## History

M. I. Shamos and D. Hoey observed in 1975 that the Voronoi diagram of points on a line gives their sorted order, so that the $\Omega(n \log n)$ bound for sorting carries over, and gave a matching $O(n \log n)$ algorithm. The algebraic computation tree model, in which the bound holds for programs that use arithmetic and not only comparisons, was made precise by M. Ben-Or in 1983, whose method also gives bounds for problems with a yes or no answer, such as element distinctness. Textbooks state the result as the optimality of Fortune's sweep.

## References
