---
tag: 63RW19
kind: algorithm
slug: four-point-method
name: Buneman's four-point method
aliases:
- four-point tree reconstruction
area: biology/phylogenetics
level: advanced
summary: Rebuilds a binary tree from its tree metric. It adds the leaves one at a time and uses four-point tests to find the edge where each new leaf attaches. O(n^2) time.
solves: [additive-tree-reconstruction]
model: word-ram
complexity:
  vars: {n: the number of taxa}
  time: {worst: "O(n^2)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1971
  people: [Peter Buneman]
  note: Buneman showed in 1971 and 1974 that the four-point condition identifies the tree. Insertion algorithms that place one leaf at a time by distance tests followed, among them Waterman et al. (1977) and Culberson and Rudnicki (1989).
prereqs: [four-point-condition, additive-tree-reconstruction]
see_also: [tree-metric, neighbor-joining, quartet, splits-of-a-tree, split-decomposition, quartet-max-cut, stepwise-addition]
sources:
  - paper: "Peter Buneman, The recovery of trees from measures of dissimilarity, in F. R. Hodson, D. G. Kendall and P. Tautu (eds), Mathematics in the Archaeological and Historical Sciences, Edinburgh University Press, 1971"
    title: Buneman 1971
    locator: pages 387 to 395, the four-point condition and the recovery of the tree
  - paper: doi:10.1016/0095-8956(74)90047-1
    title: Peter Buneman, A note on the metric properties of trees, Journal of Combinatorial Theory, Series B 17(1), 1974, pages 48 to 50
    locator: the theorem that a metric satisfying the four-point condition is a tree metric
  - paper: doi:10.1016/0022-5193(77)90351-4
    title: M. S. Waterman, T. F. Smith, M. Singh and W. A. Beyer, Additive evolutionary trees, Journal of Theoretical Biology 64(2), 1977, pages 199 to 213
    locator: the construction of an additive tree by adding one taxon at a time
  - paper: "Joseph C. Culberson and Piotr Rudnicki, A fast algorithm for constructing trees from distance matrices, Information Processing Letters 30(4), 1989, pages 215 to 220"
    title: Culberson and Rudnicki 1989
    locator: the O(n^2) insertion algorithm
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, 2004
    locator: Chapter 12, Quartets of species, the four-point condition and tree building from quartets
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, 2003
    locator: Chapter 7, tree metrics and the four-point condition
---

The four-point method builds an unrooted [phylogenetic tree](/phylogenetic-tree/) with edge lengths from a [tree metric](/tree-metric/) on $n$ taxa. It adds the taxa one at a time; to place a new taxon it walks through the current tree, and at each internal node one test of the [four-point condition](/four-point-condition/) on a [quartet](/quartet/) tells which of the three directions holds the attachment point. On the exact leaf metric of a binary tree with positive edge lengths it returns that tree, in $O(n^2)$ time. It is one algorithm for [additive tree reconstruction](/additive-tree-reconstruction/).

## In plain words

Suppose you already have a correct tree for some species, and you want to add one more. Stand at a branching point of the tree. Three branches leave it. Pick one known species down each branch, and compare the new species with these three by one simple sum of distances. The sum is smallest for the branch that leads towards the place where the new species belongs. Walk down that branch to the next branching point and ask again. When the answer points back the way you came, or towards a single species, you have found the right branch. The distances then also tell you where on that branch to attach the new species and how long its own branch is. Repeat until every species is in the tree.

## The problem

The input is $n \ge 2$ taxa and a symmetric $n \times n$ matrix $D$ with zero diagonal. The model assumes that $D$ is the leaf metric of an unrooted binary tree $T$: every internal node has degree 3, every edge has a positive length, and $D_{xy}$ is the length of the path between leaves $x$ and $y$. The output is $T$ with its edge lengths. By the [four-point condition](/four-point-condition/) such a tree exists exactly when $D$ satisfies the four-point condition, and then it is unique. The method does not check the condition; on other input it still returns a binary tree, but the tree depends on the order of the taxa and has no guarantee.

## The algorithm

For a directed edge from node $v$ to a neighbor $u$, the program keeps a representative $\mathrm{rep}(v, u)$: one leaf on the side of $u$ when the edge $\{v, u\}$ is removed. For three leaves $r_1, r_2, r_3$ on the three sides of $v$ and the new leaf $x$, the test computes the three quartet sums
$$s_i = D_{x r_i} + D_{r_j r_k}, \qquad \{i, j, k\} = \{1, 2, 3\}.$$

```pseudo id=main
FOUR-POINT-METHOD(D, n)          ▷ n ≥ 3; for n = 2 the tree is one edge
L1  make a star: center c, edges to leaves 1, 2, 3 with |c i| = (D_ij + D_ik − D_jk) / 2; set the reps
L2  for x ← 4 to n do
L3      v ← c; from ← none
L4      loop
L5          let u_1, u_2, u_3 be the neighbors of v, and r_t ← rep(v, u_t)
L6          i ← the index t with the smallest s_t
L7          if u_i = from or u_i is a leaf then w ← u_i; exit the loop
L8          from ← v; v ← u_i
L9      b ← r_i; let r_j, r_k be the other two reps
L10     t_v ← (D_{r_j b} + D_{r_j r_k} − D_{b r_k}) / 2; t_p ← (D_{r_j x} + D_{r_j b} − D_{b x}) / 2
L11     subdivide {v, w} by a new node p with |v p| = t_p − t_v and |p w| = |v w| − (t_p − t_v); add the edge {p, x} with |p x| = (D_{x r_j} + D_{x b} − D_{r_j b}) / 2; update the reps
L12 return the tree
```

Line L11 updates the representatives in $O(1)$ time: $\mathrm{rep}(v, p)$ is the old $\mathrm{rep}(v, w)$, $\mathrm{rep}(w, p)$ is the old $\mathrm{rep}(w, v)$, $\mathrm{rep}(p, w) = \mathrm{rep}(v, p)$, $\mathrm{rep}(p, v) = \mathrm{rep}(w, p)$, $\mathrm{rep}(p, x) = x$ and $\mathrm{rep}(x, p) = b$. No other representative changes.

## Example

The five taxa A to E have the leaf metric of the tree `((A:2,B:7):1,E:5,(C:3,D:6):2);`.

| | A | B | C | D | E |
|---|---|---|---|---|---|
| A | 0 | 9 | 8 | 11 | 8 |
| B | 9 | 0 | 13 | 16 | 13 |
| C | 8 | 13 | 0 | 9 | 10 |
| D | 11 | 16 | 9 | 0 | 13 |
| E | 8 | 13 | 10 | 13 | 0 |

**The star (line L1).** $|cA| = (9 + 8 - 13)/2 = 2$, $|cB| = (9 + 13 - 8)/2 = 7$ and $|cC| = (8 + 13 - 9)/2 = 6$.

**Insert D.** At $c$ the sides are A, B and C with representatives A, B, C. The sums are $s_A = D_{DA} + D_{BC} = 11 + 13 = 24$, $s_B = 16 + 8 = 24$ and $s_C = D_{DC} + D_{AB} = 9 + 9 = 18$. The minimum points to the leaf C, so D attaches on the edge $\{c, C\}$, with $b = C$, $r_j = A$, $r_k = B$. Line L10 gives $t_v = (8 + 9 - 13)/2 = 2$ and $t_p = (11 + 8 - 9)/2 = 5$. The new node $p_1$ has $|c\,p_1| = 3$, $|p_1 C| = 6 - 3 = 3$ and $|p_1 D| = (11 + 9 - 8)/2 = 6$.

**Insert E.** At $c$ the sides are A, B and $p_1$ with representatives A, B, C. The sums are $8 + 13 = 21$, $13 + 8 = 21$ and $D_{EC} + D_{AB} = 10 + 9 = 19$, so the walk moves to $p_1$. At $p_1$ the sides are $c$, C and D with representatives A, C, D. The sums are $D_{EA} + D_{CD} = 8 + 9 = 17$, $10 + 11 = 21$ and $13 + 8 = 21$. The minimum points back to $c$, the node the walk came from, so E attaches on the edge $\{p_1, c\}$, with $v = p_1$, $b = A$, $r_j = C$, $r_k = D$. Line L10 gives $t_v = (8 + 9 - 11)/2 = 3$ and $t_p = (10 + 8 - 8)/2 = 5$. The new node $p_2$ has $|p_1 p_2| = 2$, $|p_2\, c| = 3 - 2 = 1$ and $|p_2 E| = (10 + 8 - 8)/2 = 5$.

The result has the edges $cA = 2$, $cB = 7$, $c\,p_2 = 1$, $p_2E = 5$, $p_2 p_1 = 2$, $p_1C = 3$ and $p_1D = 6$. This is the tree `((A:2,B:7):1,E:5,(C:3,D:6):2);` that produced the matrix.

## Correctness

**Theorem.** If $D$ is the leaf metric of an unrooted binary tree $T$ with positive edge lengths, the method returns $T$ with its edge lengths.

The proof is by induction on the inserted leaves; the invariant is that the program holds $T$ restricted to the leaves so far, with valid representatives. Let $a$ be the point where the path from the new leaf $x$ first meets the current tree. Because $T$ is binary, $a$ lies strictly inside one edge of the current tree. The key lemma is the quartet test: at a node $v$ whose side 1 holds $a$, the paths give $s_1 < s_2 = s_3$, with a gap of twice the distance from $v$ to the point where the paths to $r_1$ and to $x$ part. So the test in line L6 always points towards $a$. The walk never goes back along its last edge, so in a tree it visits each node at most once, and it stops exactly at the edge that holds $a$. Line L10 computes two medians of three leaves, which give the position of $a$ on that edge and the length of the new pendant edge. The full proof is in the proof file.

## Complexity

The model is the word RAM with unit-cost arithmetic and $O(1)$ access to $D$. Line L1 takes $O(1)$ time. When the current tree has $m$ leaves, the walk visits at most $m - 2$ internal nodes, and each pass of lines L5 to L8 does a constant number of lookups, so inserting leaf $x$ takes $O(x)$ time. The total is $\sum_{x \le n} O(x) = O(n^2)$ in the worst case, which is linear in the $n^2$ entries of the input. A caterpillar whose leaves come in order along the spine reaches this bound. Besides $D$, the program stores $2n - 3$ edges and two representatives per edge, $O(n)$ space.

## Properties

- **Exact on binary tree metrics.** It returns the tree and all edge lengths.
- **Online.** Each new taxon is placed without changing the rest of the tree, so taxa can arrive one at a time.
- **Uses few entries.** Each insertion reads $O(m)$ entries of $D$, not all $O(n^2)$.
- **No robustness.** One test decides each step, so a small error in one entry can send a leaf to a wrong edge. Unlike [neighbor-joining](/neighbor-joining/), the method has no error radius in the sense of Atteson.
- **Order dependent on noisy data.** On exact data every insertion order gives the same tree; on other data the tree can change with the order.

## Variants and improvements

- **Non-binary trees.** If internal nodes may have degree more than 3, the attachment point can be a node, and then the three sums tie. A variant attaches $x$ at $v$ when $s_1 = s_2 = s_3$, and keeps one representative for each of the $\deg(v)$ sides; the test at $v$ then compares all sides.
- **Faster search.** Instead of walking, a program can search the current tree from a centroid, so each insertion uses $O(\log m)$ tests on binary trees; the cost of updating the search structure decides the total time.
- **Buneman tree.** For data that are not a tree metric, Buneman also proposed keeping only the splits that every quartet supports; that tree is unique and order independent, but it is often unresolved. [Split decomposition](/split-decomposition/) generalizes the idea to compatible and weakly compatible splits.
- **Quartet methods.** [Quartet max-cut](/quartet-max-cut/) and [maximum quartet consistency](/maximum-quartet-consistency/) build a tree from many quartet topologies at once, which tolerates errors in single quartets.
- **[Neighbor-joining](/neighbor-joining/).** It is also exact on tree metrics, needs $O(n^3)$ time, and is robust to small errors.

## When to use it

Use it when the distances are exact or nearly exact tree metrics, for example distances read from a known tree, or as a fast way to test whether a matrix is a tree metric: build the tree, then compare its leaf metric with $D$. It is also useful when taxa arrive one at a time. For distances estimated from sequences, use [neighbor-joining](/neighbor-joining/), [BIONJ](/bionj/) or a [least squares](/least-squares-phylogeny/) method, which use all the data at each step.

## Pitfalls

- **Treating it as a robust method.** The output on noisy data can be far from the best fitting tree. Check the fit, for example by comparing the leaf metric of the result with $D$.
- **Zero or negative lengths.** On a tree metric all lengths in line L11 are positive. A zero or negative length shows that the input is not the metric of a binary tree with positive edges.
- **Forgetting the backward test.** The walk must stop when the test points back along the edge it came by; without the $\mathit{from}$ check it loops between two nodes.
- **Stale representatives.** After a subdivision the representatives of the two halves of the old edge must be copied from the old edge, as in line L11. Leaving them unset makes later tests read the wrong leaves.
- **Exact arithmetic.** With floating point input, the strict minimum in line L6 can become a near tie. Integer or rational input avoids this.

## Implementations

## History

Buneman (1971) showed that the leaf metric of a tree determines the tree and stated the four-point condition, and in 1974 he proved that every metric that satisfies the condition is a tree metric. Zaretskii (1965) and Simões-Pereira (1969) had given related characterizations. Waterman, Smith, Singh and Beyer (1977) built additive trees by adding one taxon at a time, and Culberson and Rudnicki (1989) gave an $O(n^2)$ algorithm. The four-point condition became the basis of quartet-based phylogenetics, including the Buneman tree, split decomposition and quartet puzzling.

## References
