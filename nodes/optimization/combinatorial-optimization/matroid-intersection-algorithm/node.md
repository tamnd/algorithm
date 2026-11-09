---
tag: 1YKCWY
kind: algorithm
slug: matroid-intersection-algorithm
name: Matroid intersection algorithm
aliases:
- Edmonds matroid intersection
- augmenting path algorithm for matroid intersection
- matroid intersection augmenting path algorithm
area: optimization/combinatorial-optimization
level: advanced
summary: Augment a common independent set along shortest exchange paths in an exchange graph.
solves: [matroid-intersection]
model: word-ram
complexity:
  vars: {n: the number of elements, r: the size of a largest common independent set, Q: the time of one independence oracle call}
  time: {worst: O(n r^2 Q), average: O(n r^2 Q), best: O(n r^2 Q)}
  space: {extra: O(n r)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1970
  people: [Jack Edmonds, Eugene L. Lawler, William H. Cunningham]
  note: Edmonds proved the min-max theorem with an algorithm in 1970. Lawler (1975) and Edmonds (1979) gave the augmenting path form, and Cunningham (1986) analyzed shortest augmenting paths in phases.
prereqs: [matroid-intersection, matroid, breadth-first-search, augmenting-path]
see_also: [matroid-intersection, matroid-intersection-theorem, rado-edmonds-theorem, bipartite-matching, hopcroft-karp, augmenting-path, partition-matroid, graphic-matroid]
sources:
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer, 2003
    locator: Chapter 41, Matroid intersection (the exchange graph, the augmenting path algorithm and its running time)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer, 2018
    locator: Chapter 13, Matroids (the sections on matroid intersection and weighted matroid intersection)
  - paper: doi:10.1007/BF01681329
    title: Eugene L. Lawler, Matroid intersection algorithms, Mathematical Programming 9, 31 to 56, 1975
    locator: the augmenting path algorithm and its weighted version
  - paper: doi:10.1137/0215066
    title: William H. Cunningham, Improved bounds for matroid partition and intersection algorithms, SIAM Journal on Computing 15(4), 948 to 957, 1986
    locator: the bound on oracle calls with shortest augmenting paths in phases
  - paper: "Jack Edmonds, Submodular functions, matroids, and certain polyhedra, in Combinatorial Structures and Their Applications (Proceedings of the Calgary International Conference, 1969), Gordon and Breach, 1970, 69 to 87"
    locator: the matroid intersection theorem and the first algorithm
  - book: isbn:9780486414539
    title: Eugene L. Lawler, Combinatorial Optimization, Networks and Matroids, Holt, Rinehart and Winston, 1976 (Dover reprint 2001)
    locator: Chapter 8, Matroid intersections
---

The matroid intersection algorithm finds a largest set that is independent in two given [matroids](/matroid/) at once, which is the [matroid intersection](/matroid-intersection/) problem. It grows a common independent set $I$ one element at a time. In each round it builds an *exchange graph* on the elements, in which arcs record which single exchanges keep $I$ independent in the first or in the second matroid, and it augments $I$ along a shortest path from the elements that the first matroid would accept to those that the second would accept. When no such path exists, the elements that can reach the target form a set $U$ with $|I| = r_1(U) + r_2(E \setminus U)$, which proves that $I$ is optimal. This is the algorithmic proof of [Edmonds' matroid intersection theorem](/matroid-intersection-theorem/). With independence oracles the method uses $O(n r^2)$ oracle calls, and for two [partition matroids](/partition-matroid/) it becomes the [augmenting path](/augmenting-path/) algorithm for [bipartite matching](/bipartite-matching/).

## In plain words

Several companies offer to build links between towns. You want as many links as possible, with two rules: the links must not form a loop, and each company may build at most one link. Each rule alone is easy, and the simple greedy method is exact for each. Together they are not, and greedy can get stuck.

The algorithm gets unstuck by trades. Suppose a new link would not form a loop, but its company is already used. Drop the link of that company. Now perhaps a link of a free company fits into the network. If so, you have one more link than before. The algorithm looks for the shortest chain of such trades, using a map of all allowed single trades. When no chain exists, the same map points to a group of links that explains why no larger choice can exist.

## The problem

The input is a finite ground set $E = \{0, \ldots, n-1\}$ and two matroids $M_1 = (E, \mathcal{I}_1)$ and $M_2 = (E, \mathcal{I}_2)$, each given by an *independence oracle* that answers whether a set is independent. The output is a set $I \in \mathcal{I}_1 \cap \mathcal{I}_2$ of largest size, together with a set $U \subseteq E$ that certifies optimality: $|I| = r_1(U) + r_2(E \setminus U)$, where $r_1$ and $r_2$ are the rank functions.

## The algorithm

For a common independent set $I$, the exchange graph $D(I)$ has vertex set $E$ and, for $y \in I$ and $x \notin I$, an arc $(y, x)$ if $I - y + x \in \mathcal{I}_1$, and an arc $(x, y)$ if $I - y + x \in \mathcal{I}_2$.

```pseudo id=main
MATROID-INTERSECTION(E, M1, M2)
L1  I ← ∅
L2  repeat
L3      X1 ← {x ∉ I : I + x ∈ I1};  X2 ← {x ∉ I : I + x ∈ I2}
L4      build D(I): arc (y, x) if I − y + x ∈ I1, arc (x, y) if I − y + x ∈ I2, for y ∈ I and x ∉ I
L5      find a shortest path P in D(I) from X1 to X2 by breadth-first search
L6      if there is no such path then
L7          U ← the set of elements that have a path to X2 in D(I)
L8          return I and U
L9      I ← I △ V(P)                    ▷ add the elements of P outside I, remove those inside I
```

A path alternates between elements outside $I$ and elements inside $I$. It starts with an element $x_0$ that $M_1$ would accept, and ends with an element that $M_2$ would accept. Each step $(x_{i-1}, y_i)$ is an exchange allowed in $M_2$, and each step $(y_i, x_i)$ an exchange allowed in $M_1$. A path of one vertex, $x_0 \in X_1 \cap X_2$, simply adds $x_0$. The path must be *shortest*: a path with a shortcut can lead to a set that is not independent.

## Example

Take six links between towns 1 to 5, offered by four companies:

| element | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ |
| --- | --- | --- | --- | --- | --- | --- |
| link | 1-5 | 2-5 | 3-4 | 1-2 | 2-5 | 1-4 |
| company | red | yellow | yellow | green | blue | yellow |

$M_1$ is the [graphic matroid](/graphic-matroid/) (no cycle) and $M_2$ the [partition matroid](/partition-matroid/) with at most one link per company. The breadth-first search takes the elements in the order $a, \ldots, f$.

| round | $I$ | $X_1$ | $X_2$ | shortest path | new $I$ |
| --- | --- | --- | --- | --- | --- |
| 1 | $\emptyset$ | all | all | $a$ | $\{a\}$ |
| 2 | $\{a\}$ | $b, c, d, e, f$ | $b, c, d, e, f$ | $b$ | $\{a, b\}$ |
| 3 | $\{a, b\}$ | $c, f$ | $d, e$ | $c \to b \to d$ | $\{a, c, d\}$ |
| 4 | $\{a, c, d\}$ | $f$ | $e$ | none | stop |

In round 3, greedy is stuck: $c$ and $f$ fit in the forest but their company, yellow, is taken by $b$, and $d$ and $e$ have free companies but close a cycle with $a$ and $b$. The arc $(c, b)$ says that $\{a, c\}$ uses each company once, and the arc $(b, d)$ says that $\{a, d\}$ is a forest. So the path $c \to b \to d$ trades $b$ for $c$ and $d$, and gives $\{a, c, d\}$: links 1-5, 3-4 and 1-2 from red, yellow and green.

In round 4, the elements with a path to $X_2 = \{e\}$ are $U = \{a, d, e\}$. The links of $U$ lie on the towns 1, 2 and 5, so $r_1(U) = 2$. The other links $b, c, f$ are all yellow, so $r_2(E \setminus U) = 1$. So no common independent set has more than $2 + 1 = 3$ elements, and $\{a, c, d\}$ is optimal, although each matroid alone has rank 4.

## Correctness

The [proof](proofs/correctness.md) has four steps.

- **Exchange lemma.** If $I - y_i + x_i$ is independent for each $i$, and $I - y_i + x_j$ is dependent for all $i < j$, then the whole exchange $I - \{y_1, \ldots, y_m\} + \{x_1, \ldots, x_m\}$ is independent. The proof follows the unique circuit of $I + x_j$.
- **Augmentation.** A shortest path has no shortcut arcs, which gives exactly this triangular pattern in $M_1$ and in reverse order in $M_2$. Its inner elements are spanned by $I$, so the end elements can be added. So $I \triangle V(P)$ is common independent and one element larger.
- **Certificate.** If no path exists, every element of $U$ outside $I$ is spanned in $M_1$ by $I \cap U$, and every element outside $U$ and $I$ is spanned in $M_2$ by $I \setminus U$. This gives $|I| = r_1(U) + r_2(E \setminus U)$.
- **Weak duality.** Every common independent set $J$ has $|J| = |J \cap U| + |J \setminus U| \le r_1(U) + r_2(E \setminus U)$. So $I$ is optimal, and the algorithm stops after at most $r + 1$ rounds.

## Complexity

Let $n = |E|$, $r$ the size of the answer, and $Q$ the time of one oracle call.

- **Rounds.** Each round except the last adds one element, so there are $r + 1$ rounds.
- **One round.** Line L3 makes $2(n - |I|)$ oracle calls, and line L4 makes $2 |I| (n - |I|) = O(n r)$ calls. The graph has $O(n r)$ arcs, so breadth-first search and the search for $U$ take $O(n r)$ time.
- **Total.** $O(n r^2)$ oracle calls and $O(n r^2 Q)$ time. For $r \le n/2$ this is also the best case, because every round builds the full exchange graph.
- **Space.** $O(n r)$ for the exchange graph.
- **Faster versions.** Cunningham (1986) augmented along a maximal set of shortest paths in each phase, as in [Hopcroft-Karp](/hopcroft-karp/), and showed that $O(\sqrt{r})$ phases suffice. This gives $O(n r^{1.5})$ oracle calls. For special matroids, such as two partition matroids or a graphic and a partition matroid, the exchange graph can be built and searched much faster with problem-specific data structures.

## Properties

- **Exact, with a certificate.** The output comes with a set $U$ that proves optimality, and it can be checked with rank computations, which take $O(n)$ oracle calls each by the greedy method.
- **Oracle model.** The algorithm needs only independence tests, so it works for any matroids that have such a test: graphic, linear, partition, transversal and others.
- **Invariant.** After round $k$ the set $I$ is a common independent set of size $k$. Unlike greedy, the algorithm revises earlier choices by exchanges.
- **Deterministic.** With a fixed order of the elements in the breadth-first search, the output is fixed. Different orders can give different optimal sets.

## Variants and improvements

- **Weighted matroid intersection.** Find a common independent set of largest weight. Lawler (1975) and Edmonds (1979) gave primal-dual algorithms, and Frank (1981) gave a simple weight-splitting algorithm. Each round uses shortest paths with vertex lengths given by the weights, and the result for each size $k$ is a heaviest common independent set of size $k$.
- **Matroid union and partition.** The largest set that is the union of independent sets of $k$ matroids can be found by matroid intersection, or directly by Edmonds' matroid partition algorithm (1965). This gives $k$ edge-disjoint spanning trees.
- **[Bipartite matching](/bipartite-matching/).** For the two partition matroids of a bipartite graph, $D(I)$ is essentially the residual graph of the matching, and the algorithm is the classic augmenting path method. Cunningham's phases correspond to [Hopcroft-Karp](/hopcroft-karp/).
- **Rank oracles.** With rank oracles instead of independence oracles, binary search finds the arcs with fewer oracle calls. Recent work has reduced the number of calls further.
- **Three or more matroids.** Not solvable by this method: the problem is NP-hard for three matroids. The greedy method gives a set at least $1/k$ of the optimum for $k$ matroids.

## When to use it

- When the feasible sets are the common independent sets of two matroids, for example colorful forests, bipartite matchings, [arborescences](/arborescence/) (a graphic matroid and a partition matroid on the heads of the arcs), or independent sets that meet each class at most a given number of times.
- When a proof of optimality is wanted: the set $U$ is a short certificate.
- As a subroutine for matroid union, packing and covering problems.

For bipartite matching alone, use a specialized algorithm such as [Hopcroft-Karp](/hopcroft-karp/). For weighted problems, use the weighted version, not repeated runs of this one.

## Pitfalls

- **Not shortest.** Augmenting along a path that is not shortest can give a set that is dependent in one of the matroids. Breadth-first search, or another way to remove shortcuts, is essential.
- **Arc directions.** The arcs for $M_1$ go from $I$ to $E \setminus I$, and those for $M_2$ go from $E \setminus I$ to $I$. Swapping them gives paths of the wrong kind.
- **Using greedy.** Taking elements greedily while both matroids accept them gives only a maximal common independent set, which can be half the optimum. In the example greedy stops at $\{a, b\}$.
- **The certificate set.** $U$ is the set of elements that can *reach* $X_2$, not the set reachable from $X_1$. The two choices give different sets, but the second one, with the roles of the matroids exchanged, also works: $E \setminus U'$ with $U'$ reachable from $X_1$ gives $r_1(E \setminus U') + r_2(U') = |I|$.
- **Oracle cost.** Each oracle call tests a whole set. Rebuilding the forest or the matrix from scratch for each call multiplies the time by $n$. Incremental data structures avoid this in practice.

## Implementations

## History

Jack Edmonds stated and proved the matroid intersection theorem at the Calgary conference of 1969, published in 1970, together with an algorithm for the weighted case and the result that the intersection of two matroid polytopes is integral. Edmonds had already treated matroid partition in 1965. Aigner and Dowling (1971), Lawler (1975) and Edmonds (1979) gave the augmenting path algorithm in the form used today, with the exchange graph. Cunningham (1986) showed that shortest augmenting paths in phases need $O(\sqrt{r})$ phases, in analogy with Hopcroft and Karp for bipartite matching. The method is a central example in the theory of combinatorial min-max relations, and Lawler's 1976 book made it a standard part of combinatorial optimization courses.

## References
