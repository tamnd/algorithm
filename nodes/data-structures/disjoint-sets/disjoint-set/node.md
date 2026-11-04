---
tag: 6TK8B6
kind: abstract-type
slug: disjoint-set
name: Disjoint-set data structure
aliases:
- union-find
- merge-find set
area: data-structures/disjoint-sets
level: core
summary: Abstract type of a partition of elements into disjoint sets with make-set, find-set and union operations.
prereqs: [equivalence-relation, asymptotic-notation]
see_also: [dynamic-equivalence-problem, disjoint-set-forest, quick-find, union-by-rank, path-compression, union-find-amortized-bound, union-find-lower-bound, kruskal]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 19, Section 19.1 (Disjoint-set operations), Section 19.2 (Linked-list representation) and Section 19.3 (Disjoint-set forests)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.5, Case study, union-find (the API and the table of costs of quick-find, quick-union and weighted quick-union)
  - book: isbn:9780898711875
    title: Robert Endre Tarjan, Data Structures and Network Algorithms, SIAM, 1983
    locator: Chapter 2, Disjoint sets
  - paper: doi:10.1145/62.2160
    title: "Robert E. Tarjan and Jan van Leeuwen, Worst-case analysis of set union algorithms, Journal of the ACM 31(2) (1984), 245-281"
    locator: Section 1 (the problem and the operations) and the summary of the bounds
---

A disjoint-set data structure is an abstract data type that holds a collection of pairwise disjoint sets of elements and supports three operations: `make-set` adds a new element in a set of its own, `find` returns the representative element of the set that holds an element, and `union` merges two sets into one. It is also called union-find. The sets are the classes of an [equivalence relation](/equivalence-relation/) that only grows, so the type is the natural tool for the [dynamic equivalence problem](/dynamic-equivalence-problem/). The best implementation, a [disjoint-set forest](/disjoint-set-forest/) with [union by rank](/union-by-rank/) and [path compression](/path-compression/), does each operation in $O(\alpha(n))$ amortized time, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/), and no structure can do better.

## In plain words

Think of people at a large party who form groups. At the start, each person stands alone. Two groups can join into one group, but a group never splits. You often want to know whether two people are in the same group.

Each group picks one member as its leader. To answer the question, ask each person for the leader of their group, and compare the two leaders. To join two groups, the two leaders agree that one of them now leads both groups.

The type says only what these three actions do. It does not say how the groups are stored. A table of group names, linked lists, or trees of pointers can all store them, with very different speeds. The best method makes each action cost almost nothing, a small constant for every input of practical size.

## Operations

Let $U$ be a set of elements. A disjoint-set value $D$ is a finite set of nonempty sets $S_1, \ldots, S_k \subseteq U$ that are pairwise disjoint. Each set $S_i$ has one *representative* $\mathrm{rep}(S_i) \in S_i$. We write $E(D) = S_1 \cup \cdots \cup S_k$ for the elements of $D$, and $[x]_D$ for the set of $D$ that holds $x \in E(D)$.

| operation | signature | what it does |
|---|---|---|
| `new` | $\text{new}() \to D$ | the empty collection |
| `make-set` | $\text{make-set}(D, x) \to D$ | for $x \notin E(D)$: adds the set $\{x\}$, with representative $x$ |
| `find` | $\text{find}(D, x) \to U$ | for $x \in E(D)$: returns $\mathrm{rep}([x]_D)$ |
| `union` | $\text{union}(D, x, y) \to D$ | for $x, y \in E(D)$: if $[x]_D \ne [y]_D$, replaces the two sets by $[x]_D \cup [y]_D$ and chooses its representative; else does nothing |

Two operations are common additions. `connected(D, x, y)` returns whether $[x]_D = [y]_D$; it is $\text{find}(D, x) = \text{find}(D, y)$. `count(D)` returns the number $k$ of sets; an implementation keeps a counter that `make-set` raises by one and that a `union` of two different sets lowers by one. Some implementations also give `size(D, x)` $= |[x]_D|$.

CLRS writes `find-set` for `find`, and its `union` takes two elements of different sets. Sedgewick and Wayne take the elements to be the integers $0$ to $n - 1$, all made at the start, so their type has no `make-set`. These differences do not change the costs. A `find` may change the internal state, as path compression does, but it never changes $D$ as seen through the operations.

There is no operation that splits a set or removes an element. Types that allow this, such as the [union-find with rollback](/union-find-with-rollback/) or [dynamic connectivity](/dynamic-connectivity/), are harder.

## Laws

Each implementation meets these laws, for all elements $x, y, z$ of $E(D)$ and each $w \notin E(D)$.

$$\begin{aligned}
&(\text{D1})\quad \text{find}(\text{make-set}(D, w), w) = w, \qquad \text{find}(\text{make-set}(D, w), x) = \text{find}(D, x),\\
&(\text{D2})\quad \text{find}(D, x) \in [x]_D, \qquad \text{find}(D, \text{find}(D, x)) = \text{find}(D, x),\\
&(\text{D3})\quad \text{find}(D, x) = \text{find}(D, y) \iff [x]_D = [y]_D,\\
&(\text{D4})\quad \text{connected}(\text{union}(D, x, y), z, z') \iff \text{connected}(D, z, z') \text{ or } \big(\text{connected}(D, z, x) \text{ and } \text{connected}(D, y, z')\big) \text{ or } \big(\text{connected}(D, z, y) \text{ and } \text{connected}(D, x, z')\big),\\
&(\text{D5})\quad \text{find}(\text{union}(D, x, y), z) = \text{find}(D, z) \quad \text{if } [z]_D \ne [x]_D \text{ and } [z]_D \ne [y]_D.
\end{aligned}$$

(D1) says that a new element is alone and is its own representative, and that `make-set` does not touch the other sets. (D2) says that the representative is a member of the set and is its own representative. (D3) is the main use of the type: two elements are in the same set exactly when their representatives are equal. (D4) says that `union` merges exactly the two sets of $x$ and $y$: two elements are connected after it when they were connected before, or when one was with $x$ and the other with $y$. (D5) says that a union does not change the representative of a set that it does not touch. Between two unions, repeated calls of `find` on one set return the same element.

By (D4), `connected` after a sequence of unions is the smallest equivalence relation that contains the pairs given to `union`. The type does not fix which of the two old representatives, or which other member, becomes the representative of the merged set. Code must not rely on that choice.

**Example.** Start with `make-set` of $0, 1, \ldots, 7$. Then do `union(1, 2)`, `union(3, 4)`, `union(2, 4)`, `union(5, 6)` and `union(1, 3)`. The sets are $\{0\}$, $\{1, 2, 3, 4\}$, $\{5, 6\}$ and $\{7\}$, so `count` is 4. The last union does nothing, because 1 and 3 are already in one set after `union(2, 4)`. Now `connected(1, 4)` is true and `connected(4, 5)` is false. Which of 1, 2, 3 and 4 `find(4)` returns depends on the implementation, but by (D3) it is the same element that `find(1)` returns.

## Implementations

Let $n$ be the number of `make-set` operations and $m \ge n$ the total number of operations. The costs are worst case per operation unless the table says otherwise.

| implementation | make-set | find | union | total for $m$ operations |
|---|---|---|---|---|
| [quick-find](/quick-find/) (array of set ids) | $O(1)$ | $O(1)$ | $O(n)$ | $O(mn)$ |
| [linked lists](/linked-list-disjoint-sets/) with union by size | $O(1)$ | $O(1)$ | $O(n)$, $O(\log n)$ amortized | $O(m + n \log n)$ |
| [quick-union](/quick-union/) (forest, any link) | $O(1)$ | $O(n)$ | $O(n)$ | $O(mn)$ |
| forest with [union by size](/union-by-size/) or [by rank](/union-by-rank/) | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(m \log n)$ |
| forest with [path compression](/path-compression/) only | $O(1)$ | $O(n)$ | $O(n)$ | $O(m \log_{1 + m/n} n)$ |
| [forest](/disjoint-set-forest/) with union by rank and path compression | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(m\,\alpha(m, n))$ |
| the same with [path halving](/path-halving/) or [path splitting](/path-splitting/) | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(m\,\alpha(m, n))$ |
| [Blum's structure](/blum-union-find/) | $O(1)$ | $O(\log n/\log\log n)$ | $O(\log n/\log\log n)$ | $O(m \log n/\log\log n)$ |
| [Gabow-Tarjan](/gabow-tarjan-union-find/), unions known in advance, word RAM | | | | $O(m + n)$ |

The bounds for path compression without a linking rule are those of Tarjan and van Leeuwen (1984). The bound with union by rank and path compression is [Tarjan's bound](/union-find-amortized-bound/). The last row solves only the special case of [static tree set union](/static-tree-set-union/), in which the shape of the unions is known before the first operation.

In practice the forest with union by size or by rank and path compression, or path halving, is the standard choice. It needs two integer arrays of length $n$ and about ten lines of code. Quick-find is good when finds far outnumber unions and $n$ is small. The linked-list form is good when the program must also list the members of a set.

Extensions store more data per element. [Weighted union-find](/weighted-union-find/) keeps a value relative to the representative, which answers queries such as "how much heavier is $x$ than $y$". [Union-find with rollback](/union-find-with-rollback/) undoes the last unions.

## Lower bounds

**Cell-probe model.** Fredman and Saks (1989) proved that every implementation in the [cell-probe model](/cell-probe-model/) with words of $O(\log n)$ bits needs $\Omega(m\,\alpha(m, n))$ probes for some sequence of $n - 1$ unions and $m \ge n$ finds. So the forest with union by rank and path compression is optimal up to a constant factor, even against algorithms that use arithmetic on addresses. The [union-find lower bound](/union-find-lower-bound/) page states the theorem and sketches its proof, and the [Fredman-Saks lower bound](/fredman-saks-lower-bound/) page gives the method behind it.

**Pointer machine.** Tarjan (1979) proved the same bound for a class of [pointer machine](/pointer-machine/) algorithms that keep the sets in separate linked structures. La Poutré (1990) removed that condition.

**One operation.** Fredman and Saks also showed that some single operation must cost $\Omega(\log n/\log\log n)$ in the worst case. Blum's structure meets this bound, so no implementation can make every operation cost $O(\alpha(n))$ in the worst case.

## References
