---
tag: 45PASJ
kind: technique
slug: reverse-search
name: Reverse search
aliases:
- Avis-Fukuda reverse search
- backtracking-free enumeration
- reverse search enumeration
area: combinatorics/exhaustive-search
level: advanced
summary: Enumerate objects by defining a parent rule and traversing the implicit tree of objects with a local search, without storing visited objects.
prereqs: [depth-first-search, local-search, enumeration-problem]
see_also: [output-sensitive-enumeration, tsukiyama-algorithm, vertex-enumeration, canonical-augmentation, spanning-tree-enumeration, local-search, depth-first-search, enumeration-problem]
sources:
  - paper: doi:10.1016/0166-218X(95)00026-N
    title: David Avis and Komei Fukuda, Reverse search for enumeration, Discrete Applied Mathematics 65, 1996, 21 to 46
    locator: the reverse search procedure with an adjacency oracle and a local search function, its time and space bounds, and the applications to vertices of arrangements and polytopes, triangulations, spanning trees and connected induced subgraphs
  - paper: "David Avis and Komei Fukuda, A pivoting algorithm for convex hulls and vertex enumeration of arrangements and polyhedra, Discrete and Computational Geometry 8, 1992, 295 to 313"
    locator: vertex enumeration by reversing the simplex method with Bland's rule, in time linear in the number of vertices and in space polynomial in the input
  - paper: "Brendan D. McKay, Isomorph-free exhaustive generation, Journal of Algorithms 26(2), 1998, 306 to 324"
    locator: canonical construction path, a parent rule for objects up to isomorphism
  - paper: "Yann Strozecki, Enumeration complexity, Bulletin of the EATCS 129, 2019"
    locator: the flashlight method, reverse search and the trick of alternating outputs that bounds the delay
---

Reverse search, due to Avis and Fukuda, lists all objects of a class by giving each object except one root a *parent*, by a rule that moves it one step closer to the root. The parent links form a tree on the objects, and reverse search walks this tree depth first, from the root downward, by running the rule in reverse. It needs no list of the objects already seen and no stack: the current object and one index are enough, because the way back up is the parent rule itself. The time is proportional to the number of objects times the cost of a few local steps, so the method gives output-sensitive enumeration in polynomial space for vertices of polytopes, triangulations, spanning trees and many other classes.

## In plain words

Imagine a large hill with many paths. From every spot there is one fixed way to take a step uphill, and from every spot the uphill steps lead to the top. If you start at the top and ask, at each spot, "from which nearby spots would the uphill step lead to me?", you can walk down to every spot exactly once.

You never need to remember where you have been. When you finish below a spot, you take its uphill step to go back, and then you try its next nearby spot. So the method uses very little memory, even when there are millions of spots.

The art is in the choice of the uphill rule. It must be cheap, and it must always lead to the top.

## When it applies

Reverse search needs three things:

1. **A finite set $V$ of objects with a root $s \in V$.** The objects are the solutions to list.
2. **An adjacency oracle.** For a constant bound $\delta$, the function ADJ$(v, j)$ for $j = 1, \ldots, \delta$ returns the $j$-th neighbor of $v$ or *null*. This defines a graph on $V$.
3. **A local search function $f$.** For each $v \ne s$, $f(v)$ is a neighbor of $v$, and $v$ is among the neighbors ADJ$(f(v), \cdot)$. Repeated application of $f$ from any $v$ reaches $s$.

The third condition holds when $f$ strictly decreases a potential that has its unique minimum at $s$, such as the objective of the simplex method, the number of inversions of a permutation, or the distance to a fixed spanning tree. Then the edges $\{v, f(v)\}$ form a spanning tree of $V$, the *search tree*, rooted at $s$. The children of $v$ are the neighbors $w$ of $v$ with $f(w) = v$.

The method fits when the objects are connected by small local changes (a pivot, a flip, a swap, an exchange of one element) and a canonical improving change is easy to compute.

## The template

The recursive form is a [depth-first search](/depth-first-search/) of the search tree:

```pseudo
RS(v):
    OUTPUT(v)
    for j ← 1 to δ do
        w ← ADJ(v, j)
        if w ≠ null and f(w) = v then RS(w)
```

The form of Avis and Fukuda removes the recursion. It returns from a child $u$ to its parent with $f$, and then finds the index of $u$ in the neighbor list of the parent, to go on from there:

```pseudo id=main
REVERSE-SEARCH(s, δ, ADJ, f)
L1  v ← s, j ← 0
L2  OUTPUT(v)
L3  loop
L4      while j < δ do
L5          j ← j + 1
L6          w ← ADJ(v, j)
L7          if w ≠ null and f(w) = v then          ▷ w is a child of v: go down
L8              v ← w, j ← 0
L9              OUTPUT(v)
L10     if v = s then return
L11     u ← v, v ← f(v), j ← 0                    ▷ go up to the parent
L12     repeat j ← j + 1 until ADJ(v, j) = u       ▷ go on after the child u
```

**Why it works.** Since every $v \ne s$ reaches $s$ under $f$, and each object has one parent, the parent edges form a tree. The loop of lines L4 to L9 tries the neighbors of $v$ from index $j + 1$ on and goes down at the first child. When the neighbors of $v$ are exhausted, lines L11 and L12 return to the parent with $j$ equal to the index of $v$ in the list of its parent, which is exactly the state just before the descent to $v$. So the procedure is a depth-first traversal of the search tree, and it outputs each object exactly once.

**Cost.** Let $t_A$ and $t_f$ be the costs of one call of ADJ and of $f$, and let $N = |V|$. For each object $v$, line L6 runs at most $\delta$ times over all visits to $v$, because $j$ only increases while the walk is at or below $v$. Line L7 calls $f$ once per neighbor, and line L12 calls ADJ at most $\delta$ times once per object. So the total time is $O(N \delta (t_A + t_f))$, and the space is that of two objects and the index $j$, with no dependence on $N$.

**Delay.** The time between two outputs can be large: after a deep leaf the walk climbs many levels without an output. Print an object when the walk enters it if its depth is even, and when the walk leaves it if its depth is odd. Then between two outputs the walk moves along at most a constant number of tree edges, so the delay is $O(\delta (t_A + t_f))$.

## Classic examples

**Permutations by adjacent swaps.** Let $V$ be the permutations of $1, \ldots, n$, with root the identity $s = 1\,2 \cdots n$. ADJ$(\pi, j)$ swaps the entries at positions $j$ and $j + 1$, so $\delta = n - 1$. Let $f(\pi)$ swap the first adjacent pair that is out of order; this removes one inversion, so it reaches $s$. For $n = 3$, the search tree is

| object | parent | children |
|---|---|---|
| 1 2 3 | none | 2 1 3, 1 3 2 |
| 2 1 3 | 1 2 3 | 2 3 1 |
| 2 3 1 | 2 1 3 | 3 2 1 |
| 3 2 1 | 2 3 1 | none |
| 1 3 2 | 1 2 3 | 3 1 2 |
| 3 1 2 | 1 3 2 | none |

and the output order is $123, 213, 231, 321, 132, 312$. The swap at position 2 of $312$ gives $321$, a neighbor, but $f(321) = 231 \ne 312$, so $321$ is not a child of $312$. This is how reverse search avoids a second visit without a table of visited objects.

**Vertices of a polytope.** For a simple polytope given by linear inequalities, take the vertices as objects, the pivots of the simplex method as adjacency, and the simplex step with Bland's rule toward the optimal vertex of a fixed objective as $f$. Reverse search then lists all vertices by running the simplex method backward, with space polynomial in the input. This is the method of Avis and Fukuda for [vertex enumeration](/vertex-enumeration/) and the [convex hull](/convex-hull/) in the dual form.

**Spanning trees.** Fix a spanning tree $T_0$ of a connected graph. For $T \ne T_0$, let $f(T)$ add the smallest edge of $T_0$ that is not in $T$ and remove an edge of the cycle it closes that is not in $T_0$, chosen by a fixed rule, so that $|T \cap T_0|$ grows. The objects are all [spanning trees](/spanning-tree-enumeration/), and adjacency is the exchange of one edge.

**Maximal independent sets.** The [algorithm of Tsukiyama and others](/tsukiyama-algorithm/) can be read as a reverse search: the parent of a maximal independent set is found by restricting it to a prefix of the vertices and extending it greedily.

**Triangulations of a convex polygon.** Objects are triangulations, adjacency is the flip of a diagonal, and $f$ is a flip toward the triangulation in which all diagonals meet at vertex 1.

## Variations

- **Recursion with a stack.** The recursive form is simpler and faster in practice. It needs a stack of depth at most the height of the tree, which is often small.
- **Canonical augmentation.** For objects up to isomorphism, such as graphs, define the parent by deleting a canonically chosen part. McKay's [canonical augmentation](/canonical-augmentation/) is this idea, and it lists each isomorphism class once.
- **Parallel reverse search.** Different subtrees of the search tree are independent, so they can be explored on different processors without communication about visited objects.
- **Estimation.** The size of the search tree can be estimated before a full run by random walks from the root, as for [backtracking](/generic-backtracking-algorithm/) trees.
- **Bounded delay.** The alternating output above turns the amortized bound into a bound on the delay.

## Pitfalls

- **A function $f$ that cycles.** If $f$ can return to an earlier object, the parent edges do not form a tree, and the walk never ends or misses objects. Prove that $f$ decreases a potential with a unique minimum.
- **Asymmetric adjacency.** Line L12 needs $v$ to be in the neighbor list of $f(v)$. If the oracle is not symmetric, the walk cannot find its place in the parent's list.
- **Degeneracy.** In vertex enumeration of a polytope that is not simple, one vertex has many bases. Reverse search then lists bases, not vertices, and needs a lexicographic rule to output each vertex once.
- **An object with several encodings.** If the same object is stored in two forms, the test $f(w) = v$ must compare objects, not encodings.
- **Cost of $f$.** The test $f(w) = v$ runs $\delta$ times per object, so a slow $f$ dominates. A cheaper test that only decides whether $f(w) = v$ often helps.

## Exercises

1. For the permutation example, draw the search tree for $n = 4$ and check that it has 24 nodes. What is the height of the tree for general $n$?
2. Use reverse search to list all subsets of $\{1, \ldots, n\}$: the root is the empty set, the neighbors of $S$ add or remove one element, with the additions in increasing order of the element, and $f(S)$ removes the largest element. Show that the output order is lexicographic order of the sorted lists.
3. Prove that line L12 always stops, and that after it $j$ is the index of $u$ in the list of $v$.
4. Give a reverse search for the connected induced subgraphs of a connected graph whose vertices are numbered $1, \ldots, n$. Hint: remove the largest vertex whose removal keeps the subgraph connected.
5. Prove that the alternating output rule gives a delay of $O(\delta (t_A + t_f))$.

## References
