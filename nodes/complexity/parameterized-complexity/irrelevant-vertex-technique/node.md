---
tag: C3AJD5
kind: technique
slug: irrelevant-vertex-technique
name: Irrelevant vertex technique
aliases:
- irrelevant vertex
area: complexity/parameterized-complexity
level: research
summary: "While the treewidth is large in terms of k, find a vertex that no solution needs and delete it. At small treewidth, use dynamic programming. The method comes from Robertson and Seymour."
prereqs: [treewidth, grid-minor-theorem, dp-on-tree-decompositions]
see_also: [parameterized-disjoint-paths, minor-testing, courcelle-theorem, bidimensionality-theory, meta-theorems, graph-minor-theorem, planar-graph, kernelization]
sources:
  - paper: doi:10.1016/j.jctb.2007.12.007
    title: "Neil Robertson and Paul D. Seymour, Graph minors. XXII. Irrelevant vertices in linkage problems, Journal of Combinatorial Theory, Series B 102(2), 530-563 (2012)"
    locator: the main theorem, a vertex deep inside a large flat wall is irrelevant for a linkage problem with k pairs
  - paper: doi:10.1006/jctb.1995.1006
    title: "Neil Robertson and Paul D. Seymour, Graph minors. XIII. The disjoint paths problem, Journal of Combinatorial Theory, Series B 63(1), 65-110 (1995)"
    locator: the algorithm for disjoint paths and minor testing, which deletes irrelevant vertices until the treewidth is bounded
  - book: isbn:9783319212746
    title: "Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015"
    locator: "Section 7.8, Irrelevant vertex technique (planar vertex deletion, the definition of an irrelevant vertex, the criterion by nested cyclic separators), and the bibliographic notes of Chapter 7"
  - paper: doi:10.1016/j.jctb.2016.10.001
    title: "Isolde Adler, Stavros G. Kolliopoulos, Philipp Klaus Krause, Daniel Lokshtanov, Saket Saurabh and Dimitrios M. Thilikos, Irrelevant vertices for the planar disjoint paths problem, Journal of Combinatorial Theory, Series B 122, 815-843 (2017)"
    locator: the size of a planar grid that guarantees an irrelevant vertex for k pairs
---

The irrelevant vertex technique solves a parameterized graph problem with parameter $k$ by a loop. While the [treewidth](/treewidth/) of the graph is large in terms of $k$, it finds a vertex whose deletion does not change the answer, and deletes it. When the treewidth is small, it solves the rest by a [dynamic program on a tree decomposition](/dp-on-tree-decompositions/). Robertson and Seymour built it for the [disjoint paths problem](/parameterized-disjoint-paths/) and [minor testing](/minor-testing/) in Graph Minors XIII. It differs from [bidimensionality](/bidimensionality-theory/), which answers at once when the treewidth is large, and from [Courcelle's theorem](/courcelle-theorem/), which only covers the small-treewidth case.

## In plain words

Some problems become easy on graphs that look like thin trees. The hard case is a graph that contains a big grid. In a big grid with nothing strange in it, a vertex deep in the middle is not needed by any solution: every solution can be moved around it, like a road that goes around a single closed house in a large town. So you delete that vertex. You repeat this until the graph is thin, and then you solve it on the thin graph. The hard part of the method is the proof that the chosen vertex is really not needed. That proof is different for each problem, and for disjoint paths it took a long series of papers.

## When it applies

- The problem has a parameter $k$ and is solvable in time $f(k, t) \cdot n^{O(1)}$ when a tree decomposition of width $t$ is given. This is often true by [Courcelle's theorem](/courcelle-theorem/) or by a direct dynamic program.
- A large treewidth gives a large grid or wall by the [grid minor theorem](/grid-minor-theorem/), and the problem does not answer itself on a large grid. For example, a linkage can exist or not exist in a graph with a huge grid, so the answer is not forced.
- A vertex that is far from the terminals and deep inside a well-behaved part of the grid can be proved *irrelevant*: $(G, k)$ and $(G - v, k)$ have the same answer. For problems with a solution set $D$, the proof must hold for every possible solution, not just for one.

## The template

Let $W(k)$ be a treewidth threshold. Call a vertex $v$ *irrelevant* for $(G, k)$ if $(G, k)$ is a yes-instance exactly when $(G - v, k)$ is a yes-instance.

```pseudo id=template
SOLVE(G, k)                              ▷ parameter k
L1  while TREEWIDTH-APPROX(G) > W(k)     ▷ hole W: the threshold for k
L2      M ← FIND-STRUCTURE(G, k)         ▷ hole: a large grid, wall or flat wall, with its model
L3      if M is a direct certificate
L4          return ANSWER(M)              ▷ hole: answer at once, for example from a huge clique minor
L5      v ← IRRELEVANT(G, M, k)          ▷ hole: a vertex far inside M, proved irrelevant
L6      G ← G - v                        ▷ the answer does not change
L7  return SOLVE-BOUNDED-TW(G, k)        ▷ hole: dynamic program on width at most W(k)
```

**Lemma (correctness).** If IRRELEVANT returns an irrelevant vertex in every round, and ANSWER is correct, then SOLVE is correct. *Proof.* Each deletion at L6 keeps the answer, by the definition of irrelevant. The loop ends when the treewidth is at most $W(k)$, and SOLVE-BOUNDED-TW is correct there. $\square$

**Lemma (time).** Each round deletes one vertex, so there are at most $n$ rounds. If one round takes $g(k) \cdot n^c$ time, the loop takes $g(k) \cdot n^{c+1}$ time, and the total is FPT in $k$. This is the source of the extra factor of $n$ in the $n^3$ bound of Graph Minors XIII. Faster algorithms delete many irrelevant vertices in one round.

## Classic examples

### Two pairs on the outer ring of a grid (a toy case)

This example fills only the hole IRRELEVANT. Take the 4 by 4 grid and two pairs whose four terminals lie on the outer ring of 12 vertices. Then IRRELEVANT can return any of the 4 inner vertices, because every inner vertex is irrelevant. *Proof.* If the pairs do not cross on the ring, each pair can use its own arc of the ring, so the answer is yes in $G$ and in $G - v$. If they cross, the grid is planar with the four terminals on the outer face in crossing order, so two disjoint paths would have to cross, and the answer is no in $G$ and so also in $G - v$. A brute-force check over all 1485 instances (495 choices of terminals, 3 pairings each) and all 4 inner vertices finds no case where the deletion changes the answer.

### Disjoint paths and minor testing (Robertson and Seymour)

For [disjoint paths](/parameterized-disjoint-paths/) with $k$ pairs, W is a function of $k$ from the grid minor theorem. FIND-STRUCTURE returns either a large clique minor or a large *flat wall*: a wall that, after removing a bounded number of vertices, sits in a part of the graph that can be drawn in the plane with the wall boundary outside. If there is a large clique minor that the terminals can reach by disjoint paths, the clique minor routes all pairs and ANSWER returns yes. The case where a small separator cuts the terminals off from the clique minor is handled by recursion and is left out here. In a flat wall far from the terminals, IRRELEVANT returns the central vertex. The proof that it is irrelevant is the content of Graph Minors XXII: every linkage can be rerouted to avoid the center. SOLVE-BOUNDED-TW is a dynamic program. The total time is $f(k) \cdot n^3$. [Minor testing](/minor-testing/) is solved the same way. The structure theory behind the flat wall is the same theory that proves the [graph minor theorem](/graph-minor-theorem/).

### Planar vertex deletion (Cygan et al., Section 7.8)

The problem asks whether at most $k$ vertices can be deleted to make $G$ planar. Here $v$ is irrelevant if, for every set $D$ with $|D| \le k$, $G - D$ is planar exactly when $G - (D \cup \{v\})$ is planar. The criterion in Cygan et al. is: $v$ is surrounded by $k + 2$ disjoint, nested cyclic separators, and the part inside them is planar. Any $D$ of size $k$ misses at least two of the separators, and they shield $v$. The algorithm runs in time $2^{O(k^2 \log k)} \cdot n^{O(1)}$. Jansen, Lokshtanov and Saurabh later gave time $k^{O(k)} \cdot n$ (Cygan et al., bibliographic notes of Chapter 7).

## Variations

- **Irrelevant edges.** Some versions delete or contract an edge instead of a vertex. The same template applies.
- **Many deletions per round.** To get $n^2$ or almost-linear time, later algorithms find many irrelevant vertices at once, or reuse the structure between rounds.
- **Protrusion replacement.** Instead of deleting one vertex, replace a large part of bounded treewidth with a small part that behaves the same way toward the rest of the graph. This is the basis of meta-kernelization; see [meta-theorems](/meta-theorems/).
- **Planar graphs with explicit bounds.** On planar graphs the structure around the vertex is a set of concentric cycles, and the number of cycles needed for an irrelevant vertex can be made explicit. Adler et al. (2017) studied this size for planar disjoint paths.

## Pitfalls

- **Irrelevance must hold for all solutions.** It is not enough that one solution avoids $v$. In a deletion problem, deleting $v$ can turn a no-instance into a yes-instance, because $v$ can be part of every obstruction. So the definition must quantify over every candidate set $D$ of size at most $k$, as in the planar vertex deletion example.
- **Minors are not subgraphs.** The grid minor theorem gives a grid as a minor. The irrelevance proof works in a wall that is a subdivision (a topological minor) or in a flat part of the graph. A vertex in a branch set of a minor model need not be irrelevant.
- **The terminals must be far away.** In the toy example, a terminal inside the grid would change the answer. The proofs always keep the irrelevant vertex far from the terminals or from any set that the solution must touch.
- **The functions are huge.** The threshold $W(k)$ comes from the grid minor theorem and the flat wall theorem, and $f(k)$ in Graph Minors XIII is not practical. The method proves that a problem is FPT; it is rarely the fastest known algorithm.
- **Large treewidth may force the answer.** For problems such as vertex cover or feedback vertex set on planar graphs, a large grid already gives a no answer. Then [bidimensionality](/bidimensionality-theory/) is the simpler method, and no irrelevant vertex is needed.

## Exercises

1. In the toy example, prove that two pairs that do not cross on the ring of the 4 by 4 grid are always linked by paths on the ring alone. Then explain which step of the irrelevance proof fails when one terminal is an inner vertex.
2. Let $K_5$ be an instance of planar vertex deletion with $k = 0$. Show that no vertex of $K_5$ is irrelevant. Hint: $K_5$ is not planar, but $K_5 - v$ is planar for each $v$.
3. Suppose one round of the template takes time $2^{k^2} \cdot n^2$ and $W(k) = 10k$, and the dynamic program at L7 takes time $2^{W(k)} \cdot n$. Give the total running time and show that it is FPT in $k$.

## References
