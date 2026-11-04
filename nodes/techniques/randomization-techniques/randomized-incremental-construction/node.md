---
tag: YGPW4G
kind: technique
slug: randomized-incremental-construction
name: Randomized incremental construction
aliases:
- Clarkson-Shor technique
- RIC
- random-order incremental construction
area: techniques/randomization-techniques
level: advanced
summary: Inserts objects in random order and maintains the structure, so expected cost per step is bounded by backwards analysis.
prereqs: [backwards-analysis, random-permutation, linearity-of-expectation, expected-running-time]
see_also: [backwards-analysis, delaunay-triangulation-construction, seidel-point-location, convex-hull-3d, seidel-linear-programming, welzls-algorithm, randomized-quicksort, clarksons-algorithm]
sources:
  - paper: doi:10.1007/BF02187740
    title: Kenneth L. Clarkson and Peter W. Shor, Applications of random sampling in computational geometry, II, Discrete and Computational Geometry 4(5) (1989)
    locator: pp. 387 to 421 (randomized incremental algorithms with conflict lists, and the bound on the expected total size of the conflict changes)
  - paper: doi:10.1007/bf02187879
    title: Kenneth L. Clarkson, New applications of random sampling in computational geometry, Discrete and Computational Geometry 2(2) (1987)
    locator: pp. 195 to 222 (random samples of objects and the configurations they define)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 4 (randomized incremental linear programming), Chapter 6 (the trapezoidal map and its search structure) and Chapter 9 (the randomized incremental Delaunay triangulation)
  - book: isbn:9780133363630
    title: Ketan Mulmuley, Computational Geometry, An Introduction Through Randomized Algorithms
    locator: Chapters 1 to 3 (configuration spaces, randomized incremental algorithms, conflict lists and history)
---

Randomized incremental construction builds a structure for a set of $n$ objects by inserting the objects one at a time in a uniformly random order and repairing the structure after each insertion. Each insertion finds the parts of the current structure that the new object destroys, through conflict lists or a history structure, and replaces them by new parts. The random order makes the expected work small for every input: [backwards analysis](/backwards-analysis/) bounds the expected change at each step, and the method of Clarkson and Shor bounds the expected total cost of finding the parts to change. It gives simple expected $O(n \log n)$ algorithms for planar convex hulls, Delaunay triangulations and trapezoidal maps, and expected $O(n)$ algorithms for linear programming in fixed dimension and the smallest enclosing disk.

## In plain words

You want to build something out of many pieces, such as a map of a city made of many streets. The simple plan is to add the streets one at a time and fix the map after each one. The danger is a bad order, in which each new street forces you to redraw most of the map.

The trick is to shuffle the streets first. Then no one, not even an enemy who chose the streets, can make the order bad. At each step, the new street is a random one among those already added. A fixed map has only a few places that depend on any one street, so on average each street changes only a little. Add up these small changes, and the whole job is cheap on average, for every city.

## When it applies

- The output is a structure $F(S)$ that is determined by the set $S$ of objects, not by an order. Examples are a convex hull, a Delaunay triangulation, a trapezoidal map or the optimum of a linear program with a canonical tie rule.
- The structure is made of *configurations* (triangles, trapezoids, hull facets, intervals). Each configuration $\Delta$ is *defined* by a set $D(\Delta)$ of at most $b$ objects, a constant, and it is *in conflict* with a set $K(\Delta)$ of objects. $\Delta$ belongs to $F(R)$ exactly when $D(\Delta) \subseteq R$ and no object of $R$ is in conflict with $\Delta$. This is the framework of Clarkson and Shor, and Mulmuley calls it a configuration space.
- Inserting an object $x$ removes the configurations in conflict with $x$ and creates new configurations, each of which has $x$ in its defining set.
- For a random subset $R$ of size $r$, the expected size of $F(R)$ has a good bound $f(r)$, for example $f(r) = O(r)$ in the plane.

## The template

```pseudo id=main
RIC(S)
L1  x_1, ..., x_n ← the objects of S in a uniformly random order
L2  build F({x_1, ..., x_s}) directly for a small s                 ▷ hole: the start
L3  for each object x_j with j > s, link x_j to the configurations it conflicts with
L4  for i ← s + 1 to n
L5      C ← the configurations of F(S_{i−1}) in conflict with x_i     ▷ hole: found by the conflict lists
L6      remove C and create the new configurations N of F(S_i)        ▷ hole: the local repair
L7      for each Δ in N
L8          K ← the objects x_j, j > i, in conflict with Δ, found among the conflicts of C   ▷ hole
L9          link each object of K to Δ
L10 return F(S_n)
```

The holes are the start of line L2, the repair of line L6 and the conflict update of line L8. Line L8 is the reason for the conflict lists: an object that conflicts with a new configuration $\Delta$ must have conflicted with one of the removed configurations of $C$ that $\Delta$ replaces, so the search for $K$ only looks at the old lists. Instead of the conflict lists, the algorithm can keep a *history structure*: the removed configurations stay in memory as a directed acyclic graph that points to their successors, and $x_i$ is located by a walk down this graph. This is the form of the trapezoidal map and of the Delaunay algorithm in de Berg et al., and it also answers queries later.

### Why the expected cost is small

Write $S_i = \{x_1, \ldots, x_i\}$. Condition on the set $S_i$. In a uniform order, $x_i$ is then uniform in $S_i$.

**Claim 1 (structural change).** The expected number of configurations created at step $i$ is at most $b\, f(i)/i$.

*Proof.* A configuration $\Delta \in F(S_i)$ is new at step $i$ exactly when $x_i \in D(\Delta)$. Given $S_i$, this has probability at most $|D(\Delta)|/i \le b/i$. By linearity of expectation, the expected number of new configurations is at most $(b/i)\,|F(S_i)|$, and the average over $S_i$, a random subset of size $i$, is at most $b f(i)/i$. $\square$

With $f(i) = O(i)$, Claim 1 gives $O(1)$ new configurations per step and $O(n)$ in total. Each configuration is removed at most once after it is created, so the removals cost no more.

**Claim 2 (Clarkson and Shor, 1989).** With conflict lists, the expected total number of links made by line L9 over the whole run is at most

$$ \sum_{i = 1}^{n} b^2\, \frac{n - i}{i} \cdot \frac{f(i)}{i}. $$

*Proof idea.* A link made at step $i$ joins a new configuration $\Delta \in F(S_i)$ to a later object $y$ in conflict with it. Fix $S_i$. For a later object $y$, the configurations of $F(S_i)$ in conflict with $y$ are exactly those that $y$ would destroy if it were inserted next. If $y$ is a random later object, $S_i \cup \{y\}$ is a random set of size $i + 1$, and the configurations destroyed by its last object number, in expectation, at most those created, which is at most $b f(i+1)/(i+1)$ by Claim 1. Summed over the $n - i$ later objects, this bounds the expected total conflict size of $F(S_i)$. Only the configurations that are new at step $i$ get links at step $i$, and backwards analysis on $S_i$ adds the factor $b/i$. Making the conditioning exact needs care, because a new configuration is not a uniform member of $F(S_i)$. The full proof is in Clarkson and Shor, and in de Berg et al., Chapter 9, for the Delaunay case. $\square$

With $f(i) = O(i)$, the sum is $O(b^2 \sum_{i} n/i) = O(n \log n)$. So the total expected time is $O(n \log n)$ when each link and each repair costs $O(1)$.

## Classic examples

- **Sorting as an insertion of points on a line.** Insert $n$ distinct keys in random order into a sorted list. The configurations are the intervals between consecutive inserted keys, each defined by $b = 2$ keys, and an uninserted key conflicts with the interval that holds it. Inserting $x_i$ splits its interval, and each other uninserted key of that interval is moved to one of the two halves with one comparison. This is [randomized quicksort](/randomized-quicksort/) with the pivots chosen in the order of insertion, so the expected number of comparisons is exactly $2(n + 1)H_n - 4n$: 24.44 for $n = 10$ and 647.85 for $n = 100$.
- **[Delaunay triangulation construction](/delaunay-triangulation-construction/).** Insert the points in random order, locate each new point in a triangle, split it and restore the Delaunay property by edge flips. The triangles are configurations defined by 3 points and in conflict with the points inside their circumcircles. The expected number of triangles created is $O(n)$, and the expected time is $O(n \log n)$. De Berg et al. prove that at most $9n + 1$ triangles are created in expectation.
- **The trapezoidal map and [Seidel's point location](/seidel-point-location/).** Insert $n$ non-crossing segments in random order into a [trapezoidal map](/trapezoidal-map/) and keep the history as a search graph. Each trapezoid is defined by at most 4 segments, the expected number of new trapezoids per step is $O(1)$, and the result is a search structure of expected size $O(n)$, built in expected time $O(n \log n)$, with expected query time $O(\log n)$ for each query point.
- **Convex hulls.** In the plane and in three dimensions, see [convex hull in 3D](/convex-hull-3d/), insert the points in random order and keep conflict lists between the uninserted points and the hull facets that they see. The expected time is $O(n \log n)$, which is optimal in the comparison model.
- **[Seidel's linear programming](/seidel-linear-programming/).** The structure is the optimum of the first $i$ constraints, defined by at most $d$ of them. The update is a recursive call in dimension $d - 1$, and the expected time is $O(d!\,n)$.
- **The smallest enclosing disk, [Welzl's algorithm](/welzls-algorithm/).** The structure is the smallest disk of the first $i$ points, defined by at most 3 of them, and the expected time is $O(n)$.

## Variations

- **Conflict lists or history.** Conflict lists need all objects in advance, which is the offline case. A history structure locates each object when it arrives, so the objects need not be known in advance, as long as their order is random. It also gives a point location structure for queries.
- **Random sampling.** Clarkson (1987) studied random samples $R \subseteq S$ and the configurations of $F(R)$, and proved that each of them conflicts with $O((n/r)\log r)$ objects with high probability. Divide-and-conquer algorithms recurse on the conflict lists of a sample, as in [Clarkson's algorithm](/clarksons-algorithm/) for linear programming.
- **Recursive in the dimension.** When the repair of line L6 is itself a problem of the same kind in one dimension less, as in Seidel's algorithm and Welzl's algorithm, the analysis gives a recurrence in $d$ and $n$.
- **Faster than $n \log n$.** If the objects come with extra structure, such as the edges of a simple polygon in order, the location step can be shortened. Seidel's polygon triangulation inserts the edges in random order and uses the polygon order to locate them, for expected $O(n \log^* n)$ time.
- **Dynamic structures.** Random insertion orders also support deletions in some settings, as in randomized dynamic Delaunay triangulations, with expected bounds that need a more careful backwards analysis.

## Pitfalls

- **The order must be truly random.** Inserting in the order of the input gives no guarantee. Some insertion orders force $\Theta(i)$ changes at step $i$ of an incremental Delaunay triangulation, and $\Theta(n^2)$ in total. Shuffle with a [Fisher-Yates shuffle](/fisher-yates-shuffle/) first.
- **The location cost.** Claim 1 bounds only the structural change. Without conflict lists or a history structure, finding the conflicts of $x_i$ by a scan costs $\Theta(i)$ per step, and the total is $\Theta(n^2)$.
- **Degeneracies.** The bounds assume that each configuration has a defining set of size at most $b$ and that $F(S)$ depends only on $S$. Collinear or cocircular points break this unless a symbolic perturbation or a canonical tie rule fixes one structure.
- **The bound is in expectation.** The time on one run can be larger. Tail bounds exist for some problems, but they need their own proofs.
- **The start configuration.** Many algorithms start from a large bounding triangle or box. Its objects are not random, and the analysis must treat them as fixed, which adds a constant number of configurations per step.

## Exercises

1. Show that the expected number of comparisons of the sorting example is $2(n + 1)H_n - 4n$ by showing that it is the same process as randomized quicksort.
2. In the sorting example, with two unbounded intervals, prove by Claim 1 that the expected number of intervals created at step $i$ is at most $2(i + 1)/i$, and by a direct argument that it is exactly 2.
3. Show that in the trapezoidal map of $i$ non-crossing segments in general position there are at most $3i + 1$ trapezoids, and use Claim 1 to bound the expected number of trapezoids created at step $i$.
4. Use Claim 1 and exercise 3 to show that the history structure of the trapezoidal map has expected size $O(n)$.

5. Prove Claim 2 in full for the sorting example, where $b = 2$ and $f(i) = i + 1$, and compare the bound with the exact value.

## References
