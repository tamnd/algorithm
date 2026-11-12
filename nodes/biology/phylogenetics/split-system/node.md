---
tag: 1ZMY7S
kind: data-structure
slug: split-system
name: Split system
aliases:
- set of splits
- split encoding of a tree
area: biology/phylogenetics
level: advanced
summary: A set of splits of a fixed taxon set, stored as bit masks of the side without a reference taxon. It tests compatibility with one AND and converts to and from the unique tree of a compatible set.
model: word-ram
complexity:
  vars: {n: the number of taxa, k: the number of splits, w: the word size}
  time: {worst: O(n (n + k))}
  space: {extra: O(k n/w)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [splits-of-a-tree, bitmask, breadth-first-search]
see_also: [split-decomposition, split-network-construction, neighbor-net, phylogenetic-network, robinson-foulds-distance, consensus-tree, day-algorithm, hash-table]
sources:
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, Oxford University Press, 2003
    locator: Section 3.1, Theorem 3.1.4 (splits equivalence) and Chapter 3 on splits and their compatibility
  - paper: doi:10.1016/1055-7903(92)90021-8
    title: Hans-Jürgen Bandelt and Andreas W. M. Dress, Split decomposition, a new and useful approach to phylogenetic analysis of distance data, Molecular Phylogenetics and Evolution 1(3), 1992, 242-252
    locator: weakly compatible split systems and their use as a representation of data that does not fit a tree
  - paper: "Peter Buneman, The recovery of trees from measures of dissimilarity, in Mathematics in the Archaeological and Historical Sciences, Edinburgh University Press, 1971, pages 387 to 395"
    title: Peter Buneman, The recovery of trees from measures of dissimilarity, 1971
    locator: pairwise compatible splits and the unique tree they determine
---

A split system is a set of [splits](/splits-of-a-tree/) of a fixed set of $n$ taxa, each split being a partition of the taxa into two nonempty parts. The splits of one tree form a compatible split system, and by the splits-equivalence theorem every compatible system that holds the trivial splits comes from exactly one tree. Split systems that are not compatible arise from conflicting data and are drawn as [split networks](/split-network-construction/). This page describes the usual representation: each split is a bit mask of its side without a fixed reference taxon, which makes membership a hash lookup and compatibility one AND operation, and it gives the conversions between a tree and its split system.

## In plain words

Cut one branch of a tree of species, and the species fall into two groups. A split system is a bag of such two-group divisions. It may come from one tree, from many trees, or from data that fits no tree at all.

Each division is stored as a row of on-off switches, one switch per species, with the switches on for one of the two groups. To give each division only one form, we always record the group that does not hold the first species.

Two divisions can come from the same tree when their recorded groups do not overlap, or when one group sits inside the other. One AND operation on the switches tests this. If every pair passes the test, the bag rebuilds its tree: take the groups from the largest to the smallest, and hang each group below the smallest larger group that contains it.

## The abstract type

The taxon set $X = \{x_0, x_1, \ldots, x_{n-1}\}$ is fixed when the system is created, and $r = x_0$ is the *reference taxon*. The system is a set $\Sigma$ of $X$-splits with these operations.

- `add(A)`: insert the split $A \mid X \setminus A$, for a set $A$ with $\emptyset \ne A \ne X$.
- `contains(A)`: whether the split $A \mid X \setminus A$ is in $\Sigma$. The same split is found from either side.
- `size()` and `splits()`: the number of splits, and each split as a pair of sides.
- `is-compatible()`: whether each pair of splits in $\Sigma$ is compatible.
- `from-tree(T)`: the system $\Sigma(T)$ of all splits of an unrooted phylogenetic tree $T$, trivial ones included.
- `to-tree()`: the unique unrooted phylogenetic tree $T$ with $\Sigma(T) = \Sigma \cup \{\text{trivial splits}\}$, or an error if $\Sigma$ is not compatible. It needs $n \ge 3$.

The type stores any set of splits. The structure of a system that is not compatible is studied elsewhere: weakly compatible systems come from [split decomposition](/split-decomposition/), circular ones from [NeighborNet](/neighbor-net/), and both are drawn as [phylogenetic networks](/phylogenetic-network/).

## Representation

Taxon $x_i$ is bit $i$. A set $A \subseteq X$ is the [bit mask](/bitmask/) $m(A) = \sum_{x_i \in A} 2^i$, and $X$ is the mask $F = 2^n - 1$. A split has two sides, with masks $m$ and $F \oplus m$; the system stores the one whose bit 0 is clear, the side without $r$:
$$\operatorname{norm}(m) = \begin{cases} F \oplus m & \text{if bit 0 of } m \text{ is set,} \\ m & \text{otherwise.} \end{cases}$$
The masks are kept in a [hash table](/hash-table/).

**Invariant.** Every stored mask $m$ has bit 0 clear and $0 < m < F$, and each split of $\Sigma$ is stored as exactly one mask.

The stored masks are the clusters of the tree rooted at the leaf $r$: the mask of the edge above a vertex $v$ is the set of taxa below $v$. Compatibility then becomes a test on two masks. By the lemma on the page of [splits](/splits-of-a-tree/), two splits whose sides without $r$ are $a$ and $b$ are compatible exactly when $a$ and $b$ are disjoint or nested, that is,
$$c = a \wedge b \quad \text{is } 0, \ a \text{ or } b.$$

A mask takes $\lceil n / w \rceil$ machine words. For $n \le 64$, as is common in phylogenetics, it is one word, and all mask operations take $O(1)$ time.

## Operations

`add` and `contains` normalize the mask and use the hash table. `is-compatible` tests all $\binom{k}{2}$ pairs. The conversions are the two procedures below. A tree is given as an adjacency list, with the taxa at the leaves.

```pseudo id=main
FROM-TREE(T)                              ▷ T an unrooted tree on X, r = x_0
L1  order ← the vertices of T in breadth-first order from r; parent[r] ← none
L2  for each vertex v in reverse order do
L3      below[v] ← m({v}) if v is a taxon other than r, else 0
L4      for each neighbour u of v with u ≠ parent[v] do below[v] ← below[v] ∨ below[u]
L5      if v ≠ r then add the mask below[v] to Σ   ▷ the edge from v to parent[v]
L6  return Σ
```

The reverse of a [breadth-first](/breadth-first-search/) order lists each vertex after all vertices below it, so `below[v]` is the mask of the taxa below $v$ when the tree hangs from $r$. That is the side without $r$ of the edge above $v$.

```pseudo id=to-tree
TO-TREE(Σ)                                ▷ masks already normalized; n ≥ 3
L7  top ← F ⊕ 1                            ▷ the cluster X ∖ {r}
L8  H ← Σ ∪ {m({x}) : x ≠ r} ∪ {top}
L9  sort H by decreasing number of set bits
L10 deepest[x] ← top for each taxon x
L11 for each C in H, in this order do
L12     v(C) ← the leaf x if C = m({x}), else a new inner vertex
L13     if C = top then p ← r
L14     else P ← deepest[x] for any taxon x of C
L15          if deepest[y] ≠ P for some taxon y of C then error "not compatible"
L16          p ← v(P)
L17     for each taxon y of C do deepest[y] ← C
L18     add the edge {v(C), p}
L19 return the tree
```

Lines L7 to L19 build the Hasse diagram of the clusters, as in the proof of the splits-equivalence theorem. At each step `deepest[y]` is the smallest cluster seen so far that holds $y$. A cluster $C$ hangs below the smallest larger cluster that contains it, and when the system is compatible, every taxon of $C$ has the same such cluster. If two taxa of $C$ have different values of `deepest`, some earlier cluster holds one of them and not the other, so it crosses $C$, and line L15 reports that.

## Example

Take $X = \{a, b, c, d, e\}$ with $a, b, c, d, e$ as bits 0 to 4, so $r = a$ and $F = 31$. Let $T$ be the tree with an inner vertex 0 joined to $a$, $b$ and vertex 1, vertex 1 joined to $c$ and vertex 2, and vertex 2 joined to $d$ and $e$; in [Newick format](/newick-format/) it is `(a,b,(c,(d,e)));`.

**From the tree.** The breadth-first order from $a$ is $a, 0, b, 1, c, 2, d, e$. In reverse, `below` is $d = 8$, $e = 16$, then vertex 2 gets $8 \vee 16 = 24$ ($de$), $c = 4$, vertex 1 gets $4 \vee 24 = 28$ ($cde$), $b = 2$, and vertex 0 gets $2 \vee 28 = 30$ ($bcde$). So
$$\Sigma(T) = \{2, 4, 8, 16, 30, 28, 24\},$$
seven splits for $2 \cdot 5 - 3 = 7$ edges. The nontrivial ones are $28 = cde$, the split $ab \mid cde$, and $24 = de$, the split $abc \mid de$.

**Compatibility.** $28 \wedge 24 = 24$, which equals the second mask, so the two nontrivial splits are compatible (nested). Now add the split $bc \mid ade$. Its side without $a$ is $bc$, mask $6$. Then $6 \wedge 28 = 4$, which is neither 0 nor 6 nor 28, so $bc \mid ade$ is not compatible with $ab \mid cde$, and the system is no longer compatible.

**Back to the tree.** For $\Sigma = \{28, 24\}$, line L8 adds the singletons and $top = 30$, and line L9 gives the order $30, 28, 24$, then the singletons.

| step | $C$ | $P$ | the edge added | `deepest` after, for $b, c, d, e$ |
|---|---|---|---|---|
| 1 | $30 = bcde$ | (top) | $v(30) - a$ | $30, 30, 30, 30$ |
| 2 | $28 = cde$ | $30$ | $v(28) - v(30)$ | $30, 28, 28, 28$ |
| 3 | $24 = de$ | $28$ | $v(24) - v(28)$ | $30, 28, 24, 24$ |
| 4 | $b$ | $30$ | $b - v(30)$ | $2, 28, 24, 24$ |
| 5 | $c$ | $28$ | $c - v(28)$ | $2, 4, 24, 24$ |
| 6 | $d$ | $24$ | $d - v(24)$ | $2, 4, 8, 24$ |
| 7 | $e$ | $24$ | $e - v(24)$ | $2, 4, 8, 16$ |

The result is the tree we started from, with $v(30), v(28), v(24)$ as the vertices 0, 1, 2. With the mask 6 added, $bc$ comes after $de$ (both have two set bits; any order of the two gives an error). At $C = 6$, `deepest[b]` is 30 but `deepest[c]` is 28, so line L15 stops: the cluster $cde$ holds $c$ but not $b$, and it crosses $bc$.

## Correctness

FROM-TREE is correct because, when the tree hangs from $r$, deleting the edge from $v$ to its parent leaves the taxa below $v$ on one side and the rest, $r$ included, on the other. Line L4 computes the taxa below $v$ from those below its children, and the reverse breadth-first order computes the children first.

For TO-TREE, the proof in the proofs file shows by induction over the sorted order: if no error has occurred before $C$, the clusters already processed are pairwise disjoint or nested, and `deepest[y]` is the smallest of them that holds $y$. From this, line L15 raises an error at $C$ exactly when some processed cluster crosses $C$, so the run ends without error exactly when $\Sigma$ is compatible; and then each cluster is joined to the smallest cluster that strictly contains it, which is the tree of the splits-equivalence theorem. Its splits are $\Sigma$ plus the trivial splits, and by the uniqueness part of that theorem it is the only such tree.

## Complexity

Let $k = |\Sigma|$, and let masks take $\lceil n/w \rceil$ words.

| operation | time | notes |
|---|---|---|
| `add`, `contains` | $O(n/w + 1)$ expected | normalize and hash one mask; $O(n)$ if the input is a list of taxa |
| `is-compatible` | $O(k^2 (n/w + 1))$ | one AND per pair |
| `from-tree` | $O(n (n/w + 1))$ | one OR per edge, $O(n)$ for $n \le w$ |
| `to-tree` | $O(n (n + k))$ | lines L15 and L17 visit each taxon of each of the $k + n$ clusters once; the sort is $O((n + k) \log (n + k))$, and $\log k \le n$ |
| space | $O(k (n/w + 1))$ words | one mask per split |

For a compatible system $k \le 2n - 3$, so `to-tree` takes $O(n^2)$ time. Lines L15 and L17 can visit fewer taxa if each cluster lists only its children, but the simple version is fast enough for the use it has here: the bound $O(n^2)$ matches the size of the masks.

## Variants

- **Clusters of rooted trees.** For a rooted tree, store the cluster of each vertex as a mask, with no normalization. A set of clusters comes from a rooted tree exactly when it is a hierarchy (any two clusters disjoint or nested), and TO-TREE without the reference taxon builds the tree.
- **Weighted split systems.** Store a weight with each mask, usually the length of the edge. The weighted splits of a tree give its path-length metric as $d(x, y) = \sum \text{weight}$ over the splits that separate $x$ and $y$; see [tree metric](/tree-metric/).
- **Split counts over many trees.** A hash table from masks to counts, filled with the splits of many trees, gives the support of each split, which is what [phylogenetic bootstrap](/phylogenetic-bootstrap/) values and the majority-rule [consensus tree](/consensus-tree/) use.
- **Systems that are not compatible.** Weakly compatible and circular systems, which come from [split decomposition](/split-decomposition/) and [NeighborNet](/neighbor-net/), are represented in the same way but are drawn as [split networks](/split-network-construction/).

## When to use it

Use the bit mask form when many trees on the same taxa must be compared or combined: the [Robinson-Foulds distance](/robinson-foulds-distance/) is the size of the symmetric difference of two mask sets, and the splits of a set of bootstrap trees are counted with one hash table. For one comparison of two large trees, [Day's algorithm](/day-algorithm/) is faster, since it needs no masks of $n$ bits.

## Pitfalls

- **No normalization.** If the two sides of a split are stored as they come, the split $A \mid B$ gets two masks, and lookups and counts across trees miss it. Fix one side, for example the side without $x_0$.
- **Different taxon orders.** Masks from two trees can only be compared if both trees use the same map from taxa to bits. Build the map once, from the union of the taxa, and check that both trees have the same taxa.
- **Trivial splits.** Some programs store the trivial splits and some do not. They do not change a symmetric difference of two trees on the same taxa, but they change the counts and the sizes.
- **Vertices of degree 2.** A tree with a vertex of degree 2 gives the same split for two edges. FROM-TREE stores it once; the edge count and the split count then differ.
- **Large taxon sets.** For $n > w$ every mask operation costs $\lceil n / w \rceil$ words, and a system of $2n - 3$ splits takes $\Theta(n^2 / w)$ words. For trees with $10^5$ taxa use cluster intervals as in [Day's algorithm](/day-algorithm/) instead.

## Implementations

## History

Splits as the edges of a tree, and the theorem that pairwise compatible splits determine a unique tree, go back to Buneman (1971). Bandelt and Dress (1992) made split systems that are not compatible a tool of data analysis with split decomposition, which led to the split networks of programs such as SplitsTree. Bit masks of the side without one taxon are the usual way to store splits in programs that count them over many trees, such as consensus and bootstrap programs.

## References
