---
tag: 4Z4VSH
kind: data-structure
slug: elimination-tree
name: Elimination tree
aliases:
- etree
- elimination forest
area: numerical/linear-systems
level: research
summary: Tree encoding the column dependencies of a sparse Cholesky factorization.
model: word-ram
complexity:
  vars: {n: the order of A, m: the number of nonzeros strictly below the diagonal of A, z: the number of nonzeros strictly below the diagonal of L}
  time: {worst: O(n + m log n)}
  space: {extra: Θ(n)}
  symbolic: {worst: Θ(n + m + z)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [sparse-matrix, cholesky-decomposition, fill-in]
see_also: [fill-reducing-ordering, multifrontal-method, nested-dissection, minimum-degree-ordering, chordal-graph, path-compression, postorder-traversal, disjoint-set]
sources:
  - paper: doi:10.1137/0611010
    title: Joseph W. H. Liu, The role of elimination trees in sparse factorization, SIAM Journal on Matrix Analysis and Applications 11(1), 1990
    locator: pp. 134 to 172 (the survey; ancestor and row subtree properties, equivalent orderings by postorder, the construction algorithm)
  - paper: doi:10.1145/6497.6499
    title: Joseph W. H. Liu, A compact row storage scheme for Cholesky factors using elimination trees, ACM Transactions on Mathematical Software 12(2), 1986
    locator: pp. 127 to 148 (the near-linear construction with path compression, and row subtrees)
  - paper: doi:10.1145/356004.356006
    title: Robert Schreiber, A new implementation of sparse Gaussian elimination, ACM Transactions on Mathematical Software 8(3), 1982
    locator: pp. 256 to 276 (the elimination tree defined from the first off-diagonal nonzero of each column)
  - book: isbn:9780898716139
    title: Timothy A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006
    locator: Chapter 4, Cholesky factorization (Sections 4.1 to 4.5, the elimination tree, row patterns by ereach, postordering, row and column counts; cs_etree and cs_ereach)
  - paper: doi:10.1137/S0895479892236921
    title: John R. Gilbert, Esmond G. Ng and Barry W. Peyton, An efficient algorithm to compute row and column counts for sparse Cholesky factorization, SIAM Journal on Matrix Analysis and Applications 15(4), 1994
    locator: pp. 1075 to 1091
  - paper: doi:10.1137/0205021
    title: Donald J. Rose, R. Endre Tarjan and George S. Lueker, Algorithmic aspects of vertex elimination on graphs, SIAM Journal on Computing 5(2), 1976
    locator: pp. 266 to 283 (the fill path lemma)
  - paper: doi:10.1145/62.2160
    title: Robert E. Tarjan and Jan van Leeuwen, Worst-case analysis of set union algorithms, Journal of the ACM 31(2), 1984
    locator: pp. 245 to 281 (the bound for path compression with arbitrary linking)
---

The elimination tree of a sparse symmetric positive definite matrix $A$ with Cholesky factor $L$ has one node per column, and the parent of column $j$ is the row index of the first nonzero below the diagonal in column $j$ of $L$. That single pointer per column encodes the whole nonzero pattern of $L$: every nonzero $l_{ij}$ has $i$ as an ancestor of $j$, and row $i$ of $L$ is the union of the tree paths from the nonzeros of row $i$ of $A$ up to $i$. The tree is computed from $A$ alone, before $L$ exists, in $O(n + m \log n)$ time and $\Theta(n)$ space with path compression, and from it a sparse Cholesky code gets the column counts (and so exactly how much memory to allocate), the order in which columns may be computed, the independent subtrees that can be factored in parallel, the supernodes, and the postorder used by multifrontal methods.

## In plain words

When a sparse matrix is factored column by column, some columns must wait for others, because their entries change when the earlier columns are eliminated. The elimination tree records the bare minimum of these dependencies: each column points to one later column, the first one it changes. Following the pointers from a column tells you every column it will ever affect, so the shape of the whole factor is known before any arithmetic is done. Columns in different branches never affect each other, which is what lets them be computed at the same time.

## The abstract type

A static forest on the column indices $1, \ldots, n$ of a symmetric sparse pattern, built once:

- `build(A)`: compute $\mathrm{parent}[1..n]$, with $0$ for a root.
- `row_pattern(A, k)`: the column indices $j < k$ with $l_{kj} \ne 0$.
- `postorder()`: an ordering of the nodes in which each subtree is contiguous and each node follows its descendants.
- `column_counts(A)`: $\operatorname{nnz}$ of each column of $L$.

## Representation

**Notation.** $A \in \mathbb{R}^{n \times n}$ symmetric positive definite, or any symmetric pattern with a zero-free diagonal. $G = G(A)$ is its graph with an edge $\{i, j\}$ for each $a_{ij} \ne 0$, $i \ne j$, and $m$ is the number of nonzeros strictly below the diagonal. $L$ is the Cholesky factor, $z$ the number of its nonzeros strictly below the diagonal, so $\operatorname{nnz}(L) = n + z$. The analysis is structural: no entry of $L$ is assumed to vanish by exact cancellation (this holds for generic values; in floating point a cancellation only makes the true factor sparser than predicted).

**Definition.** $\mathrm{parent}(j) = \min\{ i > j : l_{ij} \ne 0 \}$, or $0$ if column $j$ of $L$ has no off-diagonal nonzero. Since $\mathrm{parent}(j) > j$, the graph is a forest; it is a tree exactly when $G$ is connected.

**Properties** (proved in `proofs/correctness.md`):

1. **Ancestor property.** If $l_{ij} \ne 0$ with $i > j$, then $i$ is an ancestor of $j$.
2. **Fill paths.** $l_{ij} \ne 0$ ($i > j$) if and only if $G$ has a path from $i$ to $j$ whose interior vertices are all smaller than $j$ (Rose, Tarjan and Lueker 1976). If $G$ has a path from $i$ to $j > i$ through vertices smaller than $j$, then $j$ is an ancestor of $i$.
3. **Row subtrees.** The pattern of row $k$ of $L$ is $\bigcup \{\text{tree path from } i \text{ to } k\} \setminus \{k\}$ over all $i < k$ with $a_{ki} \ne 0$. It forms a subtree rooted at $k$, the row subtree.
4. **Equivalent orderings.** Renumbering $A$ by any ordering in which each node precedes its parent, in particular a postorder, gives the same filled graph, the same column counts and an isomorphic tree.
5. **Independence.** Columns in disjoint subtrees do not modify each other, so the height of the tree bounds the length of the longest chain of column dependencies.

The structure stores $\mathrm{parent}[1..n]$; construction also uses a work array $\mathrm{anc}[1..n]$ of path-compressed ancestors, and the row pattern uses a mark array.

## Operations

```pseudo id=main
ETREE(A)                            ▷ rows of the strictly lower triangle of A
L1  for k ← 1 to n do
L2      parent[k] ← 0; anc[k] ← 0
L3      for each i < k with a_ki ≠ 0 do
L4          while i ≠ 0 and i < k do
L5              next ← anc[i]; anc[i] ← k     ▷ path compression
L6              if next = 0 then parent[i] ← k
L7              i ← next
L8  return parent
ROW-PATTERN(A, k, parent)           ▷ marks are clear on entry
L9  mark k; R ← empty list
L10 for each i < k with a_ki ≠ 0 do
L11     P ← empty list
L12     while i is not marked do
L13         append i to P; mark i; i ← parent[i]
L14     append P to R
L15 clear the marks of R and k; return R
POSTORDER(parent)
L16 build the list of children of each node, in increasing order
L17 for each root r in increasing order do a depth first search from r, emitting each node after its children
L18 return the emitted order
```

ETREE is Liu's algorithm. It builds the trees of the leading submatrices $A_{1:k,1:k}$ one row at a time: a new node $k$ becomes the parent of the current root of every subtree that contains a column $i$ with $a_{ki} \ne 0$. The climb to that root follows $\mathrm{anc}$, a disjoint-set forest with path compression: every node passed is redirected to $k$, which is the new root of the merged subtree. ROW-PATTERN is Davis's `ereach`: it climbs from each nonzero of row $k$ of $A$ until it meets a node already found, so it returns property 3's union, each node once. Column counts follow by counting, for each $j$, the rows whose pattern contains $j$.

## Example

Take $n = 8$ and the pattern with off-diagonal nonzeros at $\{1,4\}, \{1,6\}, \{2,3\}, \{2,5\}, \{3,8\}, \{4,7\}, \{5,8\}, \{6,7\}, \{7,8\}$, so $m = 9$.

| $k$ | $i < k$ with $a_{ki} \ne 0$ | nodes passed on the climbs | new parents |
|---|---|---|---|
| 1, 2 | none | | |
| 3 | 2 | 2 | $\mathrm{parent}(2) = 3$ |
| 4 | 1 | 1 | $\mathrm{parent}(1) = 4$ |
| 5 | 2 | 2, 3 | $\mathrm{parent}(3) = 5$ |
| 6 | 1 | 1, 4 | $\mathrm{parent}(4) = 6$ |
| 7 | 4, 6 | 4, 6; then 6 | $\mathrm{parent}(6) = 7$ |
| 8 | 3, 5, 7 | 3, 5; then 5; then 7 | $\mathrm{parent}(5) = 8$, $\mathrm{parent}(7) = 8$ |

So $\mathrm{parent} = (4, 3, 5, 6, 8, 7, 8, 0)$, after $13$ steps of the inner loop: the tree is two chains $2 \to 3 \to 5 \to 8$ and $1 \to 4 \to 6 \to 7 \to 8$. At $k = 8$ the climb from $5$ takes one step because $\mathrm{anc}(5) = 8$ was just set, and at $k = 7$ the second climb from $6$ is likewise cut short.

ROW-PATTERN for $k = 8$ climbs $3 \to 5 \to 8$ and $7 \to 8$ and returns $\{3, 5, 7\}$; for $k = 6$ it climbs $1 \to 4 \to 6$ and returns $\{1, 4\}$. The pattern of row $6$ of $A$ is only $\{1\}$, so $l_{64}$ is fill, and similarly row $5$ is $\{2, 3\}$ with $l_{53}$ fill: $z = 11$, two fill entries, and the column counts are $(3, 3, 3, 3, 2, 2, 2, 1)$. The postorder with children in increasing order is $2, 3, 5, 1, 4, 6, 7, 8$, and the height is $4$.

## Correctness

Proofs are in `proofs/correctness.md`. They show the fill path lemma by induction on the elimination game, derive the ancestor and row subtree properties from it, and then prove ETREE by the invariant that after row $k$, $\mathrm{parent}$ is correct on the tree of $A_{1:k,1:k}$ and $\mathrm{anc}[v]$ is $0$ for its roots and a proper ancestor of $v$ in the tree, not exceeding $k$, for the other nodes. The key step is that the nodes with parent $k$ are exactly the roots of the tree of $A_{1:k-1,1:k-1}$ whose subtree contains an $i$ with $a_{ki} \ne 0$. The equivalence of topological orderings is proved by showing that such an ordering is a perfect elimination ordering of the filled graph and preserves every fill path.

The tests check, on $600$ random patterns of order up to $13$ with fixed seeds, that the parent array, the column patterns and the column counts equal those of the brute-force elimination game; that every $l_{ij} \ne 0$ has $i$ as an ancestor of $j$; the fill path characterization by graph search on $200$ more patterns; and, with exact rational $L D L^T$ on $200$ diagonally dominant matrices, that the numerical pattern is always inside the symbolic one (and equal to it in over $80\%$ of the cases, the rest being exact cancellations of small integers).

## Complexity

- **ETREE: $O(n + m \log n)$ time, $\Theta(n)$ extra space (proved).** Each nonzero starts one climb, a find in a disjoint-set forest with path compression, and each node is linked once; Tarjan and van Leeuwen's bound for path compression with arbitrary linking gives $O(n + m \log_{2 + m/n} n)$. Adding union by rank to $\mathrm{anc}$ gives $O(m \, \alpha(m, n))$, but implementations (Davis's `cs_etree`) use compression alone because it is effectively linear. Without compression the climbs cost $\Theta(n^2)$ on the arrow-plus-path pattern of the tests, against fewer than $3n$ steps with it; on random patterns the observed step count is below $m(\log_2 n + 1)$ and at least $m$.
- **ROW-PATTERN: $O(|\text{row } k \text{ of } A| + |\text{row } k \text{ of } L|)$ (proved).** Every iteration of line L13 marks a new node of the output.
- **Symbolic factorization: $\Theta(n + m + z)$ (proved).** Calling ROW-PATTERN for every $k$ lists all of $L$, so it costs the size of the output; this is how the tests count columns. Gilbert, Ng and Peyton compute the column counts alone in $O(m \, \alpha(m, n))$, less than $z$, so memory can be allocated before the pattern is formed.
- **POSTORDER: $\Theta(n)$.**

No floating point is involved: the tree depends on the pattern, and its cost is pointer chasing, so on large problems the random memory accesses of the climbs, not the operation count, set the speed.

## Variants

- **Column elimination tree.** For $P A = L U$ with partial pivoting, the tree of $A^T A$, computed from $A$ in nearly $O(\operatorname{nnz}(A))$ time without forming $A^T A$, contains the dependencies of $L$ and $U$ for every row pivoting sequence (Gilbert and Ng); SuperLU and UMFPACK use it.
- **Supernodal and assembly trees.** Chains of columns with nested patterns are merged into supernodes, giving the assembly tree of the [multifrontal method](/multifrontal-method/); each node is then a dense frontal matrix.
- **Row and column counts in near linear time** (Gilbert, Ng and Peyton 1994), using the postorder and least common ancestors of the row subtrees.
- **Elimination DAGs for unsymmetric patterns.** For LU without symmetric structure the transitive reduction of the graph of $L$ (or $U$) is a DAG rather than a tree (Gilbert and Liu 1993).
- **Tree rotations and reorderings.** Reordering within the equivalence class of topological orders can shorten the tree for parallelism or reduce the working storage of a multifrontal stack (Liu 1990).

## When to use it

Use it in every sparse Cholesky, $L D L^T$ or QR code as the first step of the symbolic analysis, after the [fill-reducing ordering](/fill-reducing-ordering/) and before any numerical work: it gives the memory needed, the column order for left-looking, right-looking or multifrontal factorization, and the task graph for parallel factorization. Use row patterns for sparse triangular solves with a sparse right-hand side, and the height to judge an ordering for parallel use: a nested dissection order of a $k \times k$ grid gives height $O(k)$, while the natural order gives a chain of height $k^2 - 1$.

## Pitfalls

- **Numerical zeros.** The tree is structural; an entry that cancels exactly is still treated as nonzero. This is safe, and the alternative (dropping it) makes the pattern value dependent.
- **Using the pattern of $A$ instead of $L$.** The parent is the first nonzero of column $j$ of $L$, not of $A$; on the example, column $4$ of $A$ starts at row $7$ but $\mathrm{parent}(4) = 6$ because of fill.
- **Unsymmetric input.** ETREE reads only one triangle; for an unsymmetric pattern symmetrize it ($A + A^T$) or use the column tree of $A^T A$ for LU.
- **Recursion depth.** The tree of a band or natural grid ordering is a chain of length $n$, so a recursive postorder overflows the stack; use an explicit stack as in the implementation.
- **Forgetting forests.** A reducible matrix gives several roots; code that assumes a single root misses whole components.

## Implementations

## History

Schreiber (1982) defined the tree from the first off-diagonal nonzero of each column of $L$ and used it to organize sparse elimination. Duff and Reid's assembly trees for the multifrontal method (1983) and George and Liu's work on symbolic factorization used the same structure. Liu (1986) gave the nearly linear construction with path compression and the row subtree characterization, and his 1990 survey, *The role of elimination trees in sparse factorization*, collected its properties and made it the standard tool. Gilbert, Ng and Peyton (1994) gave the near linear column count algorithm, and Davis's CSparse (2006) brought these algorithms into compact codes used inside MATLAB.

## References
