---
tag: YQS7JY
kind: definition
slug: matroid
name: Matroid
aliases:
- independence system with exchange property
- matroid structure
area: techniques/greedy
level: core
summary: Set system with hereditary and exchange properties, the structure on which greedy is exactly optimal.
prereqs: [linear-independence, spanning-tree]
see_also: [matroid-greedy-theorem, graphic-matroid, linear-matroid, uniform-matroid, partition-matroid, matroid-intersection, submodular-function, maximum-weight-matroid-basis]
sources:
  - book: isbn:9780199603398
    title: James Oxley, Matroid Theory, second edition
    locator: Chapter 1, Basic definitions and examples
  - paper: doi:10.2307/2371182
    title: Hassler Whitney, On the abstract properties of linear dependence, American Journal of Mathematics 57(3), 1935
    locator: pages 509 to 533
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, sixth edition
    locator: Chapter 13, Matroids
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 16.4, Matroids and greedy methods
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Part IV, Matroids and Submodular Functions
---

A matroid is a finite set together with a family of subsets, called independent, that contains the empty set, is closed under taking subsets, and satisfies an exchange property: a smaller independent set can always be enlarged by an element of a larger one. Hassler Whitney introduced matroids in 1935 to capture what linear independence of vectors and acyclic sets of edges in a graph have in common. Matroids are exactly the set systems on which the [greedy algorithm](/matroid-greedy-algorithm/) finds a maximum-weight independent set for every choice of weights, which is the content of the [matroid greedy theorem](/matroid-greedy-theorem/).

## Definition

**Matroid.** A matroid $M = (E, \mathcal{I})$ is a finite set $E$, the *ground set*, and a family $\mathcal{I}$ of subsets of $E$, the *independent sets*, such that

1. **(I1)** $\emptyset \in \mathcal{I}$;
2. **(I2) hereditary property:** if $B \in \mathcal{I}$ and $A \subseteq B$, then $A \in \mathcal{I}$;
3. **(I3) exchange property:** if $A, B \in \mathcal{I}$ and $|A| < |B|$, then there is an element $x \in B \setminus A$ with $A \cup \{x\} \in \mathcal{I}$.

A pair $(E, \mathcal{I})$ that satisfies (I1) and (I2) but maybe not (I3) is an *independence system*. Subsets of $E$ that are not independent are *dependent*.

**Bases.** A *basis* is a maximal independent set: an independent set to which no element can be added. *All bases have the same size.* If $A$ and $B$ were bases with $|A| < |B|$, then (I3) would give $x \in B \setminus A$ with $A \cup \{x\}$ independent, and $A$ would not be maximal. More generally, for any $X \subseteq E$, all maximal independent subsets of $X$ have the same size, by the same argument applied inside $X$.

**Rank.** The *rank* of $X \subseteq E$ is $r(X) = \max\{|A| : A \subseteq X,\ A \in \mathcal{I}\}$, the common size of the maximal independent subsets of $X$. The rank of the matroid is $r(E)$, the size of a basis. The rank function satisfies $0 \le r(X) \le |X|$, it is monotone ($X \subseteq Y$ implies $r(X) \le r(Y)$), and it is [submodular](/submodular-function/):
$$ r(X \cup Y) + r(X \cap Y) \le r(X) + r(Y). $$
*Proof of submodularity.* Let $I$ be a maximal independent subset of $X \cap Y$, and extend it, by repeated use of (I3), to a maximal independent subset $J$ of $X \cup Y$ with $I \subseteq J$. Then $J \cap X$ and $J \cap Y$ are independent subsets of $X$ and $Y$, and $J \cap X \cap Y = I$ because $I$ was maximal in $X \cap Y$. So $r(X) + r(Y) \ge |J \cap X| + |J \cap Y| = |J| + |J \cap X \cap Y| = r(X \cup Y) + r(X \cap Y)$. $\square$

Conversely, a function from subsets of $E$ to integers with these three properties is the rank function of exactly one matroid, whose independent sets are the sets $X$ with $r(X) = |X|$.

**Circuits.** A *circuit* is a minimal dependent set. In a graph the circuits are the edge sets of cycles, and for vectors they are the minimal linearly dependent sets. A matroid can be defined by its circuits, its bases or its rank function instead of its independent sets; Oxley proves that these definitions are equivalent.

**Weights and the greedy algorithm.** Given weights $w : E \to \mathbb{R}$, the weight of a set is $w(A) = \sum_{x \in A} w(x)$. The [maximum-weight matroid basis](/maximum-weight-matroid-basis/) problem asks for a basis of largest weight. The [matroid greedy algorithm](/matroid-greedy-algorithm/) solves it, and an independence system is a matroid if and only if the greedy algorithm is optimal for all weights.

## Examples and non-examples

**Uniform matroid.** $E$ with $n$ elements and $\mathcal{I} = \{A : |A| \le k\}$. This is the [uniform matroid](/uniform-matroid/) $U_{k,n}$. Its bases are the $k$-subsets.

**Partition matroid.** $E$ split into blocks $E_1, \ldots, E_m$ with capacities $k_1, \ldots, k_m$, and $A$ independent when $|A \cap E_i| \le k_i$ for each $i$. See [partition matroid](/partition-matroid/).

**Graphic matroid.** $E$ is the edge set of a graph and the independent sets are the forests, the edge sets without a cycle. The bases of a connected graph are its spanning trees, and the greedy algorithm for this matroid is [Kruskal's algorithm](/kruskal/). See [graphic matroid](/graphic-matroid/).

**Linear matroid.** $E$ is a finite list of vectors over a field and the independent sets are the linearly independent sublists. Its rank is the rank of the matrix with these columns. See [linear matroid](/linear-matroid/).

**Transversal matroid.** In a bipartite graph with sides $E$ and $F$, a set $A \subseteq E$ is independent when some matching covers all of $A$. The set of jobs that can meet their deadlines in [job sequencing with deadlines](/job-sequencing-with-deadlines/) is an example, with time slots as $F$.

**Not a matroid: matchings.** Let $E$ be the edges of the path $a - b - c - d$, and call a set of edges independent when it is a matching. The family is hereditary, but $\{bc\}$ and $\{ab, cd\}$ violate (I3): both $ab$ and $cd$ share a vertex with $bc$. Matchings are the common independent sets of two partition matroids, which is why [matroid intersection](/matroid-intersection/) is needed for them.

**Not a matroid: independent sets of vertices.** In the path $x - y - z$, the sets of pairwise nonadjacent vertices are hereditary, but $\{y\}$ cannot be enlarged by an element of $\{x, z\}$. Greedy can fail badly for [independent set](/independent-set/) in graphs.

**Not a matroid: knapsack.** Items of sizes $2, 1, 1$ and capacity 2, with a set independent when its total size is at most 2. The set $\{1\}$, the item of size 2, cannot be enlarged by an element of $\{2, 3\}$. This is why greedy by value fails for the 0-1 [knapsack problem](/knapsack-problem/).

## Related definitions

- **Independence system.** A family with (I1) and (I2) only. Greedy is optimal for all weights exactly when (I3) also holds.
- **Rank function.** $r(X)$, defined above; a monotone submodular function. See [rank](/rank/) for the linear algebra case.
- **Dual matroid.** The dual $M^*$ of $M$ has as bases the complements $E \setminus B$ of the bases of $M$. The dual of a graphic matroid of a planar graph is the graphic matroid of its planar dual.
- **Restriction and contraction.** For $X \subseteq E$, the restriction $M | X$ keeps the independent sets inside $X$. Contraction is the dual operation. Both give matroids again, and a matroid obtained from $M$ by restrictions and contractions is a minor of $M$.
- **Matroid intersection.** Common independent sets of two matroids on one ground set. They do not form a matroid in general, but a largest or heaviest one can be found in polynomial time. See [matroid intersection](/matroid-intersection/).
- **Submodular functions.** The rank function is the main example of a [submodular function](/submodular-function/), and much of matroid theory extends to submodular functions.

## References
