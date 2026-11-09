---
tag: KJM3PC
kind: technique
slug: orderly-generation
name: Orderly generation
aliases:
- Canonical augmentation
- McKay's method
- Orderly algorithm
- Orderly generation and canonical augmentation
- Read-Faradzev orderly algorithm
- isomorph rejection
area: combinatorics/generating-partitions-and-trees
level: advanced
summary: Generate combinatorial objects up to isomorphism by accepting only those that are canonical under a fixed ordering.
prereqs: [canonical-form, generic-backtracking-algorithm, graph-isomorphism-problem]
see_also: [canonical-augmentation, graph-generation, canonical-labeling, nauty, symmetry-breaking, generic-backtracking-algorithm, free-tree-generation, automorphism-orbit]
sources:
  - paper: doi:10.1016/S0167-5060(08)70325-X
    title: Ronald C. Read, Every one a winner, or how to avoid isomorphism search when cataloguing combinatorial configurations, Annals of Discrete Mathematics 2 (1978), 107 to 120
    locator: the whole paper (the orderly algorithm, the condition on the canonical form, and the catalogue of graphs)
  - paper: doi:10.1006/jagm.1997.0898
    title: Brendan D. McKay, Isomorph-free exhaustive generation, Journal of Algorithms 26(2) (1998), 306 to 324
    locator: the introduction and the comparison of orderly generation with canonical construction path
  - book: isbn:9783540289906
    title: Petteri Kaski and Patric R. J. Östergård, Classification Algorithms for Codes and Designs, Springer, 2006
    locator: Chapter 4, Isomorph-free exhaustive generation (orderly generation and canonical augmentation)
---

Orderly generation lists combinatorial objects up to isomorphism without ever comparing two generated objects. Each isomorphism class has one *canonical* member, the one whose code is the largest under a fixed order, and the objects are built one element at a time in a search tree whose nodes are exactly the canonical objects. The method works when the canonical form has one property: removing the last element of a canonical object leaves a canonical object. Read and Faradzev found the method independently in 1978, and the name is also used loosely for the wider family of methods with [canonical augmentation](/canonical-augmentation/).

## In plain words

Suppose you want one copy of each graph with $4$ vertices. Many drawings show the same graph, and comparing every new graph with all earlier ones is slow.

Instead, give each drawing a code, a row of 0s and 1s that says which edges are present. Among all drawings of the same graph, keep only the one with the largest code. Now build graphs by adding edges, one at a time, always to the right of the last edge already present. Keep a new graph only if its code is the largest among its drawings. Under a simple condition on the code, every graph is built exactly once, and no two outputs need to be compared.

## When it applies

- **Objects are built from elements.** An object is a set of elements from a fixed, ordered ground set, such as the edges of a graph on $n$ vertices, the blocks of a design, or the rows of a matrix. Adding one element gives a larger object.
- **A group acts on the objects.** Two objects are isomorphic when a permutation from a group, such as the relabelings of the vertices, maps one to the other.
- **There is a canonical member with the hereditary property.** Each class has one canonical member, and removing the *last* element of a canonical object, in the fixed order, gives a canonical object. For the largest code under lexicographic order this holds, as shown below.
- **A canonicity test is affordable.** Each candidate needs a test of whether it is canonical. This test is the main cost.

## The template

```pseudo id=main
ORDERLY(X)                                    ▷ X is canonical
L1  VISIT(X)
L2  for each element e after the last element of X, in the fixed order do
L3      Y ← X ∪ {e}
L4      if not PRUNE(Y) and IS-CANONICAL(Y) then
L5          ORDERLY(Y)
```

Call ORDERLY on the empty object. The holes are:

- **The order and the code.** A fixed order $e_1, e_2, \ldots, e_N$ of the ground set, and the code of an object $X$, the 0-1 word $c(X)$ with $c_j = 1$ when $e_j \in X$. A group element $\pi$ acts on codes through its action on the ground set.
- **IS-CANONICAL(Y).** True when $c(Y) \ge c(\pi Y)$ for every $\pi$ in the group, that is, when $Y$ has the largest code in its class. A direct test tries all $\pi$; practical tests use partial codes and backtracking, or a [canonical labeling](/canonical-labeling/) program.
- **PRUNE(Y).** An optional test for the property that the objects must have, such as a degree bound or no triangle. It must be hereditary: if $Y$ fails it, every larger object fails it too.

**Why each class appears once.** Let $Y$ be canonical with $m \ge 1$ elements, let $e_j$ be its last element, and let $X = Y \setminus \{e_j\}$. Then $X$ is canonical. Suppose not, so $c(\pi X) > c(X)$ for some $\pi$, with the first difference at a position $i$, where $c(\pi X)_i = 1$ and $c(X)_i = 0$. If $i < j$, then $c(\pi Y) \ge c(\pi X) > c(Y)$, because $c(Y)$ agrees with $c(X)$ before $j$ and adding an element only turns 0s into 1s; this contradicts the choice of $Y$. If $i \ge j$, then $c(\pi X)$ has the $m - 1$ ones of $c(X)$, which all lie before $j$, and one more at $i$, so it has $m$ ones, which is impossible for an object with $m - 1$ elements. So the parent $X$ of $Y$ is canonical and is visited, and $Y$ is tried in line L2 from $X$, since $e_j$ comes after the last element of $X$. The parent is determined by $Y$, so $Y$ is visited once. Non-canonical objects are never visited, so each class appears exactly once.

**The cost.** The search tree has one node per class, and each node tries at most $N$ extensions, each with one canonicity test. No list of earlier outputs is stored, and the subtrees are independent, so the search splits easily into parallel parts.

## Classic examples

- **Graphs.** The ground set is the set of the $\binom{n}{2}$ vertex pairs, in a fixed order, and the group is the symmetric group on the vertices. For $n = 4$ with the pairs ordered $12, 13, 14, 23, 24, 34$, the method visits the $11$ graphs with the codes $000000$, $100000$, $110000$, $111000$, $111100$, $111110$, $111111$, $110100$, $110010$, $110011$, $100001$, in this order, after $24$ canonicity tests. The cycle $110011$ has the parent $110010$, the path. See [graph generation](/graph-generation/).
- **Restricted graphs.** With PRUNE, the same search lists triangle-free graphs, graphs of bounded degree, or [regular graphs](/regular-graph/), as long as the restriction is closed under removing edges. Regularity is not, so it is checked only when a graph is output.
- **Rooted and free trees.** Canonical level sequences of rooted trees have the prefix property, so the [Beyer-Hedetniemi algorithm](/beyer-hedetniemi/) can be seen as an orderly listing whose canonicity test costs nothing, and the [Wright-Richmond-Odlyzko-McKay algorithm](/wright-richmond-odlyzko-mckay/) restricts it to [free trees](/free-tree-generation/).
- **Necklaces.** A necklace is the lexicographically smallest rotation of a word, and the prefixes of necklaces are prenecklaces; the [necklace](/necklace/) generators use this prefix structure in the same way. See [Cattell's necklace generation](/cattell-necklace-generation/).
- **Designs and matrices.** The same scheme lists combinatorial designs and 0-1 matrices up to row and column permutations, with the rows or the entries as elements; Kaski and Östergård describe these uses.

## Variations

- **Partial canonicity tests.** Test only the permutations that can still beat the code of the current prefix, by backtracking over the vertices; this is the usual way to make IS-CANONICAL fast for graphs.
- **Order of the ground set.** The choice of the order changes the shape of the search tree and the cost of the tests. For graphs, both the row by row and the column by column order of the upper triangle of the adjacency matrix are used.
- **Canonical augmentation.** McKay's method replaces "the last element" by a canonically chosen element, which removes the need for the hereditary condition and allows augmentation by vertices instead of edges. It is usually faster for graphs; see [canonical augmentation](/canonical-augmentation/).
- **Counting instead of listing.** If only the number of classes is needed, [Burnside's lemma](/burnside-lemma/) or the [Pólya enumeration theorem](/polya-enumeration-theorem/) gives it without generation.

## Pitfalls

- **The hereditary condition fails.** For an arbitrary canonical form, such as the labeling returned by a canonical labeling program, removing the last element can give a non-canonical object, and the method then misses classes. Use the largest code, check the condition for the form you use, or use canonical augmentation.
- **The canonicity test is the cost.** A test that tries all $n!$ relabelings is fine for $n \le 8$ but not beyond. Use partial tests or a canonical labeling program.
- **Order of extensions.** Only elements after the last element of $X$ may be added. Adding other elements generates objects twice.
- **Non-hereditary filters.** A PRUNE test that is not closed under removal cuts off the parents of valid objects and loses them; apply such tests only at output time.
- **Mixing orders.** The order used to define the code, the meaning of "last element" and the extension order must be the same.

## Exercises

1. Show that, with the pairs ordered $12, 13, 14, 23, 24, 34$, the code $110011$ is the largest code of the 4-cycle, and find the relabeling that gives it from the code $101101$.
2. Run ORDERLY by hand for $n = 3$ with the pairs ordered $12, 13, 23$. Show that it visits the four graphs $000$, $100$, $110$, $111$ and makes six canonicity tests.

## References
