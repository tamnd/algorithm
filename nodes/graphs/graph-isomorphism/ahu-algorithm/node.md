---
tag: 9MMJGB
kind: algorithm
slug: ahu-algorithm
name: Aho-Hopcroft-Ullman tree isomorphism algorithm
aliases:
- AHU algorithm
- AHU tree canonical form
- Aho-Hopcroft-Ullman tree isomorphism
area: graphs/graph-isomorphism
level: intro
summary: Tests whether two rooted trees are isomorphic by giving each vertex an integer code built from the sorted codes of its children, level by level from the leaves; linear time with radix sorting.
solves: [tree-isomorphism]
model: word-ram
complexity:
  vars: {n: the number of vertices of each tree}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, directed: false}
prereqs: [rooted-tree, breadth-first-search, radix-sort, graph-isomorphism-definition]
see_also: [tree-isomorphism, tree-center, canonical-labeling, weisfeiler-leman, string-sorting, lexicographic-order, hash-consing]
sources:
  - book: isbn:9780201000290
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms, Addison-Wesley, 1974
    locator: Section 3.2, Radix sorting (Algorithm 3.2, lexicographic sort of strings of different lengths, and Example 3.2, isomorphism of rooted trees)
  - book: isbn:9783540435506
    title: Gabriel Valiente, Algorithms on Trees and Graphs, Springer, 2002
    locator: Chapter 4, Tree isomorphism (unordered tree isomorphism by bottom-up certificates)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 7, Computing isomorphism (certificates of trees, rooted at the center)
  - paper: "Steven Lindell, A logspace algorithm for tree canonization, Proceedings of the 24th ACM Symposium on Theory of Computing (STOC 1992), 400 to 404"
    locator: the whole paper
---

The Aho-Hopcroft-Ullman (AHU) algorithm decides whether two rooted trees are isomorphic. It processes the levels of both trees from the deepest up. At each level it gives every vertex an integer code, so that two vertices of the same level get the same code exactly when their subtrees are isomorphic. The code of a vertex is the rank of the sorted list of its children's codes. With a radix sort of these lists the whole test takes $\Theta(n)$ time, which solves rooted [tree isomorphism](/tree-isomorphism/) optimally; rooting free trees at their [centers](/tree-center/) extends it to unrooted trees.

## In plain words

Two family trees have the same shape if you can rename the people so that every parent and child pair matches. Start with the people who have no children: they all look the same, so give them the number 0. Then go one generation up. Describe each person by the sorted list of the numbers of their children. Two people with the same list have the same shape below them. Give each different list its own new number. Repeat until you reach the top person. At each generation, if the two trees have different collections of numbers, the trees differ. If you reach the top without a difference, the trees have the same shape.

## The problem

The input is two rooted trees $T_1 = (V_1, E_1, r_1)$ and $T_2 = (V_2, E_2, r_2)$, each with $n$ vertices, given as edge lists. The trees are undirected, uncolored and unlabeled: the names of the vertices do not count, and the children of a vertex have no order. The question is whether there is a bijection $\varphi : V_1 \to V_2$ with $\varphi(r_1) = r_2$ that maps edges to edges. This is the rooted case of [tree isomorphism](/tree-isomorphism/). Ordered trees, where the order of the children counts, are easier: compare their parenthesis strings.

## The algorithm

The level of a vertex is its distance from the root. $L_i(T)$ is the set of vertices at level $i$, and $h(T)$ is the largest level.

```pseudo id=main
AHU-ISOMORPHIC(T1, r1, T2, r2)
L1  if |V1| ≠ |V2| then return false
L2  run BFS from r1 in T1 and from r2 in T2: the children and the level of each vertex
L3  if h(T1) ≠ h(T2) then return false
L4  for i ← h down to 0 do
L5      for each v in L_i(T1) ∪ L_i(T2): key(v) ← the sorted list of code(c) over the children c of v
L6      sort the keys of level i of both trees together, lexicographically, and remove copies
L7      for each v in L_i(T1) ∪ L_i(T2): code(v) ← the rank of key(v) in the sorted list (0, 1, 2, ...)
L8      if the sorted list of codes of L_i(T1) ≠ that of L_i(T2) then return false
L9  return true
```

A leaf has the empty key, so all leaves of a level get the same code. The codes of level $i$ are a common numbering for both trees, built at line L6 from the keys of both trees. Line L8 compares the two collections of codes; if they agree at level 0, the two roots have the same code, because each tree has one vertex at level 0.

The codes are small: the codes of level $i$ are less than $|L_i(T_1)| + |L_i(T_2)|$, and a key at level $i$ has one entry for each child. So the total length of all keys is $2n - 2$, and line L6 can sort them with the lexicographic radix sort of Aho, Hopcroft and Ullman for strings of different lengths (bucket by length, then by position from the last), in time linear in the total length plus the size of the alphabet of that level.

**Unrooted trees.** A free tree has one or two [centers](/tree-center/), and every isomorphism maps centers to centers. If both trees have one center, compare them rooted at their centers. If both have two, root $T_1$ at one of its centers and try $T_2$ rooted at each of its two centers. If the numbers of centers differ, the trees are not isomorphic.

## Example

$T_1$ has root 0 with children 1, 2, 3; vertex 1 has children 4, 5; vertex 2 has child 6; vertex 6 has child 7. $T_2$ is the same tree with the names changed by $0 \mapsto 7, 1 \mapsto 5, 2 \mapsto 3, 3 \mapsto 0, 4 \mapsto 1, 5 \mapsto 6, 6 \mapsto 2, 7 \mapsto 4$, so its root is 7. Both trees have 8 vertices and height 3.

| level | keys in $T_1$ | keys in $T_2$ | sorted distinct keys | codes in $T_1$ | codes in $T_2$ |
|---|---|---|---|---|---|
| 3 | 7: () | 4: () | () | 7: 0 | 4: 0 |
| 2 | 4: (), 5: (), 6: (0) | 1: (), 6: (), 2: (0) | (), (0) | 4: 0, 5: 0, 6: 1 | 1: 0, 6: 0, 2: 1 |
| 1 | 1: (0, 0), 2: (1), 3: () | 5: (0, 0), 3: (1), 0: () | (), (0, 0), (1) | 1: 1, 2: 2, 3: 0 | 5: 1, 3: 2, 0: 0 |
| 0 | 0: (0, 1, 2) | 7: (0, 1, 2) | (0, 1, 2) | 0: 0 | 7: 0 |

At every level the two collections of codes are equal, so the algorithm returns true.

Now compare $T_1$ with $T_3$: root 0 with children 1, 2, 3; vertex 1 has children 4, 5, 6; vertex 4 has child 7. $T_3$ also has 8 vertices, height 3, and 3 vertices at levels 1 and 2. At level 2 the keys of $T_3$ are $4{:}(0)$, $5{:}()$, $6{:}()$, which give the codes $\{1, 0, 0\}$, the same collection as $T_1$. At level 1 the keys are $1{:}(0, 0)$, $2{:}(1)$, $3{:}()$ in $T_1$ and $1{:}(0, 0, 1)$, $2{:}()$, $3{:}()$ in $T_3$. The sorted distinct keys are $(), (0, 0), (0, 0, 1), (1)$, so $T_1$ gets the codes $\{1, 3, 0\}$ and $T_3$ gets $\{2, 0, 0\}$. Line L8 returns false at level 1.

## Correctness

**Theorem.** AHU-ISOMORPHIC returns true exactly when there is an isomorphism from $T_1$ to $T_2$ that maps $r_1$ to $r_2$.

The key invariant, proved by induction from the deepest level up: after line L7 for level $i$, two vertices $u, v$ of level $i$ (in the same tree or in different trees) have $\mathrm{code}(u) = \mathrm{code}(v)$ if and only if the subtree of $u$ is isomorphic to the subtree of $v$ as rooted trees. For the induction step, two subtrees are isomorphic exactly when there is a bijection between the children that pairs each child with a child of isomorphic subtree, that is, when the multisets of children's codes are equal, and the sorted key is a way to write this multiset. Line L8 then holds at every level when the trees are isomorphic, because an isomorphism of the rooted trees maps level $i$ onto level $i$ and keeps codes. If line L8 holds at level 0, the roots have equal codes, so the whole trees are isomorphic. The full proof is below.

## Complexity

The model is the [word RAM](/word-ram/) with words of $\Theta(\log n)$ binary digits.

- **Lines L1 to L3.** BFS takes $\Theta(n)$ time on each tree.
- **Line L5.** The keys of level $i$ have total length $|L_{i+1}(T_1)| + |L_{i+1}(T_2)|$, the number of children. Writing them costs that much, and over all levels $2n - 2$.
- **Line L6.** The entries of keys at level $i$ are codes of level $i + 1$, all less than $k_{i+1} = |L_{i+1}(T_1)| + |L_{i+1}(T_2)|$. The lexicographic radix sort of strings of different lengths sorts $k_i$ strings of total length $k_{i+1}$ over an alphabet of size $k_{i+1}$ in $O(k_i + k_{i+1})$ time. Sorting each key itself (line L5) is part of the same pass: AHU sort all (code, parent) pairs of a level once with a [counting sort](/counting-sort/) and then read the keys in sorted order. Summed over the levels, this is $O(n)$.
- **Lines L7 and L8.** One pass over the sorted list gives the ranks, and comparing the codes of a level is a counting sort plus a scan, $O(k_i)$.

The total is $\Theta(n)$ time in every case, since BFS alone reads the whole input, and $\Theta(n)$ extra space for the keys and codes. The unrooted version adds a center computation, $O(n)$, and at most two rooted tests. The implementation below uses the library sort instead of radix sort, so it takes $O(n \log n)$ time.

## Properties

- **Iterative.** The algorithm goes level by level after one BFS, so it needs no recursion and works on paths of any length.
- **Canonical codes.** Run on one tree alone, the codes of each level depend only on the shapes of the subtrees, so the list of sorted keys of all levels is a complete [invariant](/isomorphism-invariant/) of the rooted tree. Comparing many trees then takes linear time each plus a comparison of these lists.
- **Exact, not hashing.** The codes are ranks of sorted lists, not hash values, so two different shapes never get the same code within one run.
- **A special case of color refinement.** On a rooted tree, the codes are the classes of [color refinement](/weisfeiler-leman/) restricted to one level, which is why color refinement identifies trees.

## Variants and improvements

- **Parenthesis strings.** Write the code of a vertex as "(" followed by the sorted codes of its children and ")". The string of the root is a canonical form. It is simple, but sorting long strings can cost $\Theta(n^2)$ time on deep trees with many children per level; with the integer codes above it is linear.
- **Hashing children's multisets.** Replace the sort by a dictionary from keys to new codes, as the implementation below does. With sorted keys and a hash map, this runs in expected $O(n \log n)$ time and is the usual choice in practice.
- **Free trees.** Root at the center or centers, as above. An alternative is to subdivide the central edge when there are two centers, which gives a single center.
- **Labeled and colored trees.** Put the vertex color at the start of each key; then codes are equal only for subtrees with equal colors.
- **Logspace.** Lindell (1992) showed that tree isomorphism and canonization can be done in logarithmic space, with a different, comparison-based method.

## When to use it

Use AHU to compare or to canonize trees: parse trees, molecules without cycles, phylogenetic trees, XML documents without order, or the decomposition trees inside other isomorphism algorithms, such as the tree of triconnected components in [planar graph isomorphism](/planar-graph-isomorphism/). For general graphs it does not apply; there [color refinement](/weisfeiler-leman/) is the analogue, but it is not complete. For ordered trees, compare the preorder parenthesis strings directly. To measure how different two trees are, use [tree edit distance](/tree-edit-distance/) instead.

## Pitfalls

- **Codes from different trees in different numberings.** If $T_1$ and $T_2$ are numbered separately at line L6, the same shape can get code 2 in one tree and code 5 in the other. Either number both trees together, as line L6 does, or compare the sorted key lists level by level, not the codes.
- **Not sorting the children's codes.** The key at line L5 must be sorted (or be a multiset). Without the sort, the test treats the trees as ordered and rejects isomorphic trees whose children come in another order.
- **Free trees rooted at arbitrary vertices.** Rooting both free trees at vertex 0 gives wrong answers. Root at the centers, and when there are two, try both centers of one tree.
- **Comparing only the roots.** Codes compared across levels mean nothing: a leaf at level 3 and a leaf at level 1 both have code 0 while their positions differ. Compare codes only within one level, as line L8 does.
- **Recursion on deep trees.** A recursive version that computes the code of a vertex from its children fails on long paths with Python's default stack. The level order of line L4 avoids recursion.

## Implementations

## History

Aho, Hopcroft and Ullman gave the algorithm in 1974 in The Design and Analysis of Computer Algorithms, as Example 3.2, an application of their lexicographic sort of strings of different lengths. Lindell (1992) later put tree canonization in logarithmic space.

## References
