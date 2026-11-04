---
tag: DGXANE
kind: concept
slug: linear-matroid
name: Linear matroid
aliases:
- vector matroid
- representable matroid
area: techniques/greedy
level: advanced
summary: A matroid whose ground set is a set of vectors and whose independent sets are the linearly independent subsets.
prereqs: [matroid, linear-independence]
see_also: [matroid, graphic-matroid, uniform-matroid, gaussian-elimination, rank, matroid-greedy-algorithm, bitset-gaussian-elimination, matroid-intersection]
sources:
  - book: isbn:9780199603398
    title: James Oxley, Matroid Theory, second edition
    locator: Chapter 1 (matroids from matrices) and Chapter 6, Matroid representation
  - paper: doi:10.2307/2371182
    title: Hassler Whitney, On the abstract properties of linear dependence, American Journal of Mathematics 57(3), 1935
    locator: pages 509 to 533
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, sixth edition
    locator: Chapter 13, Matroids
---

A linear matroid, or vector matroid, has a finite list of vectors over a field as its ground set, and a sublist is independent when its vectors are linearly independent. It is the example from which matroids were abstracted: Whitney chose the matroid axioms in 1935 so that they hold for linear independence. A matroid that is isomorphic to a linear matroid over a field $\mathbb{F}$ is called representable over $\mathbb{F}$. The greedy algorithm on a linear matroid finds a maximum-weight basis of a set of vectors, with [Gaussian elimination](/gaussian-elimination/) as the independence test.

## In plain words

Take a pile of vectors, for example the columns of a matrix. Call a group of them independent when none of them can be built from the others by adding and scaling. Small independent groups can always grow: if one independent group is bigger than another, the bigger one reaches into some direction that the smaller one does not cover, and one of its vectors can be added to the smaller group.

That growth rule is exactly what makes a matroid. So picking the heaviest vectors that stay independent, one at a time from the heaviest down, gives the heaviest possible independent group. The check "is this still independent?" is done by Gaussian elimination.

## The idea

**Definition.** Let $\mathbb{F}$ be a field and let $v_1, \ldots, v_n$ be vectors in $\mathbb{F}^d$, for example the columns of a $d \times n$ matrix $A$. The linear matroid $M[A]$ has ground set $E = \{1, \ldots, n\}$, and $X \subseteq E$ is independent when the vectors $v_i$, $i \in X$, are linearly independent. Repeated vectors are allowed; they are different elements of $E$.

**It is a matroid.** (I1) The empty set of vectors is independent. (I2) A subset of a linearly independent set is linearly independent. (I3) Let $X$ and $Y$ be independent with $|X| < |Y|$. The span of the vectors of $X$ has dimension $|X|$. If every vector of $Y$ were in this span, then $|Y|$ linearly independent vectors would lie in a space of dimension $|X| < |Y|$, which is impossible. So some $y \in Y$ is not in the span of $X$, and then $X \cup \{y\}$ is linearly independent. $\square$

**Rank, bases and circuits.** The rank of $X \subseteq E$ is the dimension of the span of its vectors, which is the [rank](/rank/) of the submatrix with these columns. The bases are the sets of columns that form a basis of the column space of $A$. The circuits are the minimal linearly dependent sets of columns.

**Independence test.** To test whether a set is independent, or to add one vector to an independent set and test again, reduce the vectors by Gaussian elimination. Keeping the chosen vectors in echelon form, one test of a new vector against $k$ chosen vectors in $\mathbb{F}^d$ costs $O(k d)$ field operations. Over $\mathbb{F}_2$, vectors fit in machine words and each step is one XOR, as in [bitset Gaussian elimination](/bitset-gaussian-elimination/).

**Representability.** Not every matroid is linear. The [uniform matroid](/uniform-matroid/) $U_{2,4}$ is linear over $\mathbb{F}_3$ but not over $\mathbb{F}_2$, and some matroids are not linear over any field. A matroid representable over $\mathbb{F}_2$ is called *binary*, and one representable over every field is called *regular*. [Graphic matroids](/graphic-matroid/) are regular.

## Examples

**Five vectors over $\mathbb{F}_2$.** In $\mathbb{F}_2^3$, written as bit strings, let $a = 110$, $b = 011$, $c = 101$, $d = 111$, $e = 100$. Since $a + b = c$ and $b + d = e$, the sets $\{a, b, c\}$ and $\{b, d, e\}$ are circuits. The third circuit is $\{a, c, d, e\}$. The matroid has rank 3, and 8 of the 10 sets of three elements are bases; the two that are not are the two circuits of size 3.

**Greedy on this matroid.** With weights $w(a) = 5$, $w(b) = 7$, $w(c) = 6$, $w(d) = 2$, $w(e) = 4$, the [matroid greedy algorithm](/matroid-greedy-algorithm/) takes $b$ (weight 7) and $c$ (6), skips $a$ (5), because $a = b + c$, takes $e$ (4), and skips $d$ (2), because the set already has rank 3, and indeed $d = b + e$. The basis $\{b, c, e\}$ has weight 17, the largest over all 8 bases.

**Graphic matroids are linear.** For a graph, give each edge $uv$ the vector $e_u + e_v$ over $\mathbb{F}_2$, where $e_u$ is the unit vector of vertex $u$. A set of edges is linearly independent if and only if it has no cycle, because the vectors of a cycle add up to 0 and a forest always has a leaf edge whose vector is the only one with a 1 in the coordinate of the leaf. So the [graphic matroid](/graphic-matroid/) is binary; with signed incidence vectors $e_u - e_v$ it is linear over every field.

**$U_{2,4}$ over $\mathbb{F}_3$.** The vectors $(1, 0)$, $(0, 1)$, $(1, 1)$, $(1, 2)$ in $\mathbb{F}_3^2$ are pairwise independent, and any three are dependent in a plane. So they represent the uniform matroid $U_{2,4}$. Over $\mathbb{F}_2$ the plane has only three nonzero vectors, so four pairwise independent vectors do not exist and $U_{2,4}$ is not binary.

## Where it is used

- **Maximum-weight bases of vectors.** Choosing the heaviest set of linearly independent features, tests or measurements. The greedy algorithm with Gaussian elimination is exact.
- **XOR bases.** In problems on the largest XOR of a subset of integers, the integers are vectors over $\mathbb{F}_2$, and a greedy basis kept in echelon form answers the queries.
- **Matroid intersection with linear matroids.** Many problems, such as finding a spanning tree with a color constraint, combine a graphic or linear matroid with another one; see [matroid intersection](/matroid-intersection/).
- **Coding theory.** The columns of a generator matrix of a linear code form a linear matroid, and its bases are the information sets of the code.

## References
