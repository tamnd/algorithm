---
tag: JWK9ZR
kind: problem
slug: dynamic-equivalence-problem
name: Dynamic equivalence problem
aliases:
- union-find problem
- disjoint-set union problem
area: data-structures/disjoint-sets
level: core
summary: Maintain an equivalence relation under merges of classes and same-class queries.
prereqs: [equivalence-relation, disjoint-set]
see_also: [disjoint-set-forest, incremental-connectivity, union-find-amortized-bound, union-find-lower-bound, static-tree-set-union, dynamic-connectivity, kruskal, quick-find]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.5, Case study, union-find (the dynamic connectivity problem and its three implementations)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 19, Sections 19.1 to 19.4, and the chapter notes
  - paper: doi:10.1145/62.2160
    title: "Robert E. Tarjan and Jan van Leeuwen, Worst-case analysis of set union algorithms, Journal of the ACM 31(2) (1984), 245-281"
    locator: Section 1, the set union problem
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.3 (the equivalence problem, Algorithm E)
  - paper: doi:10.1145/73007.73040
    title: "Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, Proceedings of the 21st Annual ACM Symposium on Theory of Computing (1989), 345-354"
    locator: the lower bounds for the set union problem
---

The dynamic equivalence problem asks for a data structure that keeps an [equivalence relation](/equivalence-relation/) on $n$ elements while new pairs are declared equivalent, and that answers, at any time, whether two elements are equivalent. A pair may only join two classes; classes never split. The [disjoint-set](/disjoint-set/) type is the interface for it, and the [disjoint-set forest](/disjoint-set-forest/) with union by rank and path compression solves it in $O(n + m\,\alpha(m, n))$ time for $m$ operations, which is optimal in the [cell-probe model](/cell-probe-model/). Sedgewick and Wayne present the same problem as *dynamic connectivity*, and in graph terms it is [incremental connectivity](/incremental-connectivity/).

## In plain words

You have a list of items, and you learn facts one at a time: "this item is the same as that item". Sameness passes on, so if one item is the same as a second, and the second the same as a third, then the first is the same as the third. Between the facts, someone asks you: "are these two items the same?". You must answer at once, from the facts so far.

You never learn that two items are different after all. So the groups of same items only grow and merge. The problem is to answer each question quickly, without going over all the facts again each time.

## Definition

**Input.** A number $n$ and a sequence of operations $o_1, o_2, \ldots, o_m$ on the elements $\{0, 1, \ldots, n - 1\}$, given one at a time. Each operation is one of:

- $\mathrm{union}(x, y)$: declare $x$ and $y$ equivalent;
- $\mathrm{same}(x, y)$: ask whether $x$ and $y$ are equivalent.

**State.** Let $R_t$ be the set of pairs $(x, y)$ of the unions among $o_1, \ldots, o_t$, and let $\equiv_t$ be the equivalence closure of $R_t$: the smallest equivalence relation on $\{0, \ldots, n - 1\}$ that contains $R_t$. Its classes are the [connected components](/connected-components/) of the graph with the edges $R_t$.

**Output.** For each query $o_t = \mathrm{same}(x, y)$, the answer is true if $x \equiv_{t-1} y$ and false otherwise. The problem is *online*: the answer to $o_t$ must be given before $o_{t+1}$ is read.

**Cost.** The cost of a solution is the total time of the $m$ operations, as a function of $n$ and $m$, in the worst case over all sequences. A per-operation bound can be amortized or worst case.

The [disjoint-set](/disjoint-set/) type adds `find`, which names a representative of the class; then $\mathrm{same}(x, y)$ is $\mathrm{find}(x) = \mathrm{find}(y)$. Tarjan and van Leeuwen state the problem as the *set union problem*: the sets have names, $\mathrm{find}(x)$ returns the name of the set of $x$, and $\mathrm{union}(A, B)$ merges two sets given by their names.

## Variants

- **With names or representatives.** $\mathrm{find}(x)$ returns the name of the class. This is the form of the [disjoint-set](/disjoint-set/) type, and each solution below gives it at no extra cost.
- **Counts and sizes.** Report the number of classes, or the size of the class of $x$. A counter and a size field at each root give these in $O(1)$ extra time.
- **Offline.** The whole sequence is known before the first answer. The online lower bounds below are proved for online algorithms. When the unions form a tree that is known in advance, the problem is [static tree set union](/static-tree-set-union/), which the [Gabow-Tarjan](/gabow-tarjan-union-find/) algorithm solves in linear time on a RAM.
- **Intervals.** The elements are $0$ to $n - 1$ on a line, and each union joins two adjacent classes, so each class is an interval. This is the case of [offline minimum](/offline-minimum/) and [painting subarrays](/offline-subarray-painting/).
- **With undo.** Allow the last union to be undone. This is [union-find with rollback](/union-find-with-rollback/), with $\Theta(\log n/\log\log n)$ amortized cost in the worst case (Westbrook and Tarjan; see that page).
- **With deletions.** Allow a pair to be removed, which can split a class. This is no longer an equivalence that only grows; it is [dynamic connectivity](/dynamic-connectivity/), or [decremental connectivity](/decremental-connectivity/) if there are only deletions.
- **With relative values.** Each union states a difference, such as "$x$ is 3 heavier than $y$", and a query asks for the difference of two elements of one class. This is [weighted union-find](/weighted-union-find/); the case of parities is [union-find with parity](/dsu-with-parity/).

## Examples

**A short sequence.** Let $n = 6$. The operations and answers are:

| $t$ | operation | answer | classes after $o_t$ |
|---|---|---|---|
| 1 | union(0, 1) | | {0, 1} {2} {3} {4} {5} |
| 2 | union(2, 3) | | {0, 1} {2, 3} {4} {5} |
| 3 | same(1, 3) | false | |
| 4 | union(1, 2) | | {0, 1, 2, 3} {4} {5} |
| 5 | same(0, 3) | true | |
| 6 | union(4, 5) | | {0, 1, 2, 3} {4, 5} |
| 7 | same(3, 4) | false | |
| 8 | union(0, 3) | | no change |
| 9 | union(5, 3) | | {0, 1, 2, 3, 4, 5} |
| 10 | same(0, 4) | true | |

The answer of step 5 uses transitivity: $0 \equiv 1$, $1 \equiv 2$ and $2 \equiv 3$. The union of step 8 changes nothing, because 0 and 3 are already equivalent.

**The worst case for a slow method.** Recomputing the components with a graph search after each union costs $\Theta(n + t)$ at step $t$, so $\Theta(m(n + m))$ in all. The forest costs $O(\alpha(m, n))$ amortized per operation instead.

## Known algorithms

| algorithm | union | same / find | total for $m \ge n$ operations |
|---|---|---|---|
| [quick-find](/quick-find/) | $O(n)$ | $O(1)$ | $O(mn)$ |
| [linked lists](/linked-list-disjoint-sets/) with union by size | $O(\log n)$ amortized | $O(1)$ | $O(m + n \log n)$ |
| [quick-union](/quick-union/) | $O(n)$ | $O(n)$ | $O(mn)$ |
| forest with [union by rank](/union-by-rank/) or [by size](/union-by-size/) | $O(\log n)$ | $O(\log n)$ | $O(m \log n)$ |
| [disjoint-set forest](/disjoint-set-forest/) with rank and [path compression](/path-compression/) | | | $O(m\,\alpha(m, n))$ |
| [Blum's structure](/blum-union-find/) | $O(\log n/\log\log n)$ | $O(\log n/\log\log n)$ | $O(m \log n/\log\log n)$ |

Each bound of the table is worst case unless it says amortized. The bound of the fifth row is [Tarjan's union-find bound](/union-find-amortized-bound/), and the same bound holds with [path halving](/path-halving/) or [path splitting](/path-splitting/) and with [randomized linking](/randomized-linking/) in expectation.

## Bounds

- **Upper bound.** $O(n + m\,\alpha(m, n))$ time for $n$ elements and $m$ operations, by the forest with union by rank and path compression (Tarjan, 1975).
- **Amortized lower bound.** $\Omega(m\,\alpha(m, n))$ in the [cell-probe model](/cell-probe-model/) with words of $O(\log n)$ bits, for $n - 1$ unions and $m \ge n$ finds (Fredman and Saks, 1989). The same bound holds on the [pointer machine](/pointer-machine/) for separable algorithms (Tarjan, 1979) and for all algorithms (La Poutré, 1990). See the [union-find lower bound](/union-find-lower-bound/).
- **Worst case of one operation.** $\Theta(\log n/\log\log n)$: Blum (1986) gave the upper bound, and Fredman and Saks proved the lower bound in the cell-probe model with words of polylogarithmic size.

So the problem is solved up to constant factors, both in the amortized sense and for a single operation.

## Reductions

- **Incremental connectivity is the same problem.** A union is the insertion of an edge, and a query asks whether two vertices are in one [connected component](/connected-components/). Each reduction costs $O(1)$ per operation. So the bounds of this page are the bounds of [incremental connectivity](/incremental-connectivity/).
- **Lower bounds go up.** Each problem that can answer the queries of this problem, such as [dynamic connectivity](/dynamic-connectivity/), needs at least the same time.
- **Equivalence of automata.** The [Hopcroft-Karp](/hopcroft-karp-equivalence/) test of two DFAs merges pairs of states that must be equivalent, and it reduces to this problem with $O(n |\Sigma|)$ unions.
- **Offline minimum.** [Offline minimum](/offline-minimum/) reduces to $n$ makes and $O(n)$ unions and finds of this problem, after a sort.

## Applications

- [Kruskal's algorithm](/kruskal/) for the [minimum spanning tree](/minimum-spanning-tree/): an edge is taken when its ends are not yet equivalent.
- [Connected component labeling](/connected-component-labeling/) of images, and [percolation](/percolation/) models.
- [Tarjan's offline LCA algorithm](/tarjan-offline-lca/).
- [Congruence closure](/congruence-closure/) in theorem provers, and unification of types and terms.
- Compilers: storage for variables that the program declares to share memory. This was the setting of the paper of Galler and Fischer and of Algorithm E of Knuth.

## References
