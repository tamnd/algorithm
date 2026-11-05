---
tag: Q61TVH
kind: data-structure
slug: compressed-suffix-tree
name: Compressed suffix tree
aliases:
- CST
area: strings/suffix-structures
level: research
summary: A suffix tree stored in compressed space while supporting its navigation operations.
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, σ: the alphabet size, s: the sampling step of the suffix array, b: the block size of the samples}
  time: {worst: O(n)}
  space: {extra: O(n log σ / log n + n / s + n / b)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [compressed-suffix-array, suffix-tree, lcp-array]
see_also: [compressed-suffix-array, enhanced-suffix-array, lcp-interval-tree, lcp-rmq-reduction, fm-index, balanced-parentheses-representation, succinct-data-structures, suffix-link]
sources:
  - paper: doi:10.1007/s00224-006-1198-x
    title: Kunihiko Sadakane, Compressed suffix trees with full functionality, Theory of Computing Systems 41(4), 2007
    locator: pages 589 to 607, the compressed suffix tree from a compressed suffix array, the PLCP bit vector of 2n bits, the balanced parentheses tree and the operations on them
  - paper: doi:10.1016/j.tcs.2009.09.012
    title: Johannes Fischer, Veli Mäkinen and Gonzalo Navarro, Faster entropy-bounded compressed suffix trees, Theoretical Computer Science 410(51), 2009
    locator: pages 5354 to 5364, the tree operations from range minimum, previous smaller value and next smaller value queries on the LCP array, without a stored tree
  - paper: doi:10.1145/2000807.2000821
    title: Luís M. S. Russo, Gonzalo Navarro and Arlindo L. Oliveira, Fully compressed suffix trees, ACM Transactions on Algorithms 7(4), 2011
    locator: the fully compressed suffix tree, which keeps a sample of the nodes and uses suffix links to reach the others
  - paper: doi:10.1145/1216370.1216372
    title: Gonzalo Navarro and Veli Mäkinen, Compressed full-text indexes, ACM Computing Surveys 39(1), 2007
    locator: the compressed suffix array and the function Psi on which compressed suffix trees are built
---

A compressed suffix tree (CST) gives the operations of a [suffix tree](/suffix-tree/), such as parent, child, string depth, lowest common ancestor and [suffix link](/suffix-link/), in space close to the size of the compressed text instead of the $\Theta(n)$ words of a pointer-based tree. It has three parts: a [compressed suffix array](/compressed-suffix-array/) for $SA$, $SA^{-1}$ and $\Psi$; the LCP values in a bit vector of $2n$ positions; and a way to find the tree shape, either a [balanced parentheses](/balanced-parentheses-representation/) sequence (Sadakane, 2007) or range minimum and nearest smaller value queries on the LCP array (Fischer, Mäkinen and Navarro, 2009). This page describes the second form, where each node is a range of ranks.

## In plain words

A suffix tree is one of the most useful tools for text, but it needs many numbers for each letter of the text. For a large genome it does not fit in memory.

A compressed suffix tree keeps only compressed pieces. A compressed suffix array tells you where each sorted ending starts. A short row of bits tells you how many letters each ending shares with the ending before it in the sorted list. From these two, you can find every branch of the tree when you need it.

Each branch is a block of the sorted list, and its depth is the smallest shared count inside the block. To go up, down or sideways, you look for the nearest smaller count to the left or right. Each step is slower than in a normal suffix tree, but the whole structure is many times smaller.

## The abstract type

The structure is static and built from a text $T$. Its nodes are the nodes of the suffix tree of $T\$$. It supports:

- `root()`, `is_leaf(v)`, `parent(v)`, `first_child(v)`, `next_sibling(v)` and `children(v)`;
- `depth(v)`: the string depth, the length of the path label;
- `letter(v, d)`: the symbol at depth $d$ of the path label;
- `child(v, c)`: the child whose edge starts with the symbol $c$;
- `lca(u, v)`: the lowest common ancestor;
- `suffix_link(v)`: the node of $u$ when $v$ is the node of $cu$;
- `find(P)`: the node, or the rank range, of the suffixes that start with $P$.

## Representation

The text is $T = T[0 \ldots n-1]$ over a general ordered alphabet, with the symbols coded $1, \ldots, \sigma$. A sentinel $\$$ with code 0, unique and smallest, is appended, so there are $N = n + 1$ suffixes. Positions and ranks are 0-based. $SA$ is the suffix array of $T\$$ and $LCP[r]$, for $1 \le r \le n$, is the lcp of the suffixes at ranks $r - 1$ and $r$. For the operations, $LCP[0] = LCP[N] = -1$.

**Nodes as ranges.** A node is the range $[lb..rb]$ of the ranks of the suffixes in its subtree. A leaf is $[r..r]$, and the root is $[0..n]$. An internal node is an lcp-interval of the [LCP interval tree](/lcp-interval-tree/): its string depth is $\min LCP[lb+1 \ldots rb]$, and $LCP[lb]$ and $LCP[rb+1]$ are smaller.

**The three parts.**

1. **Compressed suffix array.** $\Psi(i) = SA^{-1}[SA[i] + 1]$, stored as gamma-coded gaps of the increasing values $F(i) \cdot N + \Psi(i)$, where $F(i)$ is the first symbol of the suffix of rank $i$, with a sample every $b$ ranks. $SA[i]$ is found by $\Psi$ steps to a sampled position, a multiple of $s$, and $SA^{-1}[p]$ from a sample at or before $p$. See the [compressed suffix array](/compressed-suffix-array/).
2. **PLCP in a bit vector.** $PLCP[p]$ is the LCP value of the suffix at position $p$, so $LCP[r] = PLCP[SA[r]]$. Since $PLCP[p+1] \ge PLCP[p] - 1$, the values $PLCP[p] + 2p$ strictly increase and are less than $2N$. Sadakane's bit vector $H$ has a 1 at each of them, so it has $2N$ positions, and $PLCP[p] = \mathrm{select}_1(H, p) - 2p$, counting the ones from 0.
3. **Range minima.** The minimum of $LCP$ on each block of $b$ ranks, in a complete binary tree of minima. It answers range minimum queries (RMQ) and the nearest smaller value queries
   - $\mathrm{PSV}(k) = \max\{r < k : LCP[r] < LCP[k]\}$,
   - $\mathrm{NSV}(k) = \min\{r > k : LCP[r] < LCP[k]\}$,

   by a scan inside a block and a walk in the tree of minima. Each $LCP$ value it reads costs one $SA$ lookup and one select.

The text, $SA$ and $LCP$ are not stored.

## Operations

```pseudo id=main
CST-DEPTH(v = [lb..rb])
L1  if lb = rb then return N − SA[lb]
L2  return LCP[RMQ(lb + 1, rb)]
CST-PARENT(v)                          ▷ v is not the root
L3  k ← lb if LCP[lb] > LCP[rb + 1] else rb + 1
L4  return [PSV(k) .. NSV(k) − 1]
CST-FIRST-CHILD(v)                     ▷ v is not a leaf
L5  return [lb .. RMQ(lb + 1, rb) − 1]
CST-NEXT-SIBLING(v)
L6  if v is the root or LCP[lb] > LCP[rb + 1] then return nil
L7  h ← LCP[rb + 1]; return [rb + 1 .. (the first r > rb + 1 with LCP[r] ≤ h) − 1]
CST-LCA(u, v)                          ▷ neither contains the other; u is left of v
L8  k ← RMQ(rb(u) + 1, lb(v)); return [PSV(k) .. NSV(k) − 1]
CST-SUFFIX-LINK(v)                     ▷ v is internal and not the root
L9  return CST-LCA([Ψ(lb)..Ψ(lb)], [Ψ(rb)..Ψ(rb)])
CST-LETTER(v, d)                       ▷ 0 ≤ d < depth(v)
L10 return F(SA⁻¹[SA[lb] + d])
CST-CHILD(v, c)
L11 return the child w of v with CST-LETTER(w, depth(v)) = c, or nil
```

RMQ returns the leftmost position of the minimum. In each case the result is the node that has the value $LCP[k]$ and contains the ranks $k - 1$ and $k$: its range runs from the previous smaller value to just before the next smaller value.

- **Depth (L1, L2).** A leaf of rank $r$ has the path label $T\$[SA[r] \ldots n]$, of length $N - SA[r]$. An internal node has the depth $\min LCP[lb+1 \ldots rb]$.
- **Parent (L3, L4).** The parent's depth is the larger of the two values at the borders of $v$, and the parent is the node with that value around that border.
- **Children (L5 to L7).** The first child ends just before the first minimum of $LCP[lb+1 \ldots rb]$, the first $\ell$-index. A node $v$ has a next sibling if $LCP[rb+1]$ is the depth of its parent, that is, if it is not smaller than $LCP[lb]$; the sibling starts at $rb + 1$ and ends before the next value that is at most this depth.
- **LCA (L8).** For two nodes side by side, the lcp of their suffixes is the minimum of $LCP$ between them, and the LCA is the node with that value at the first minimum.
- **Suffix link (L9).** If $v$ has the label $cu$, then $\Psi$ maps its first and last suffixes to suffixes that start with $u$ and differ at depth $|u|$, so their LCA is the node of $u$. A leaf of rank $r$ links to the leaf $\Psi(r)$, and the leaf of $\$$ links to the root.
- **Letter and child (L10, L11).** The symbol at depth $d$ is the first symbol of the suffix at position $SA[lb] + d$. `child` scans the children.
- **Find.** A walk from the root: take the child for $P[d]$, compare the rest of its edge with $\Psi$ steps, and go on.

## Example

The text is $T = \texttt{mississippi}$, $N = 12$. Here $SA = [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]$, and with the borders, $LCP[0 \ldots 12] = [-1, 0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3, -1]$.

**The bit vector.** By position, $PLCP = [0, 4, 3, 2, 1, 1, 0, 1, 1, 0, 0, 0]$, and the ones of $H$ are at $PLCP[p] + 2p = 0, 6, 7, 8, 9, 11, 12, 15, 17, 18, 20, 22$:

$$H = \texttt{100000111101100101101010},$$

24 positions for 12 values. For example $PLCP[1] = \mathrm{select}_1(H, 1) - 2 = 6 - 2 = 4$, the lcp of `ississippi$` and `issippi$`.

**Operations.**

| call | computation | result |
|---|---|---|
| `depth([3..4])` | $LCP[\mathrm{RMQ}(4, 4)] = LCP[4]$ | 4, the node `issi` |
| `parent([10..11])` | $LCP[10] = 1 > LCP[12] = -1$, so $k = 10$; $\mathrm{PSV}(10) = 8$, $\mathrm{NSV}(10) = 12$ | $[8..11]$, the node `s` |
| `first_child([8..11])` | $\mathrm{RMQ}(9, 11) = 10$ | $[8..9]$, the node `si` |
| `next_sibling([8..9])` | $LCP[8] = 0 \le LCP[10] = 1$; the first $r > 10$ with $LCP[r] \le 1$ is 12 | $[10..11]$, the node `ssi` |
| `next_sibling([10..11])` | $LCP[10] = 1 > LCP[12] = -1$ | nil |
| `lca([2..2], [4..4])` | $\mathrm{RMQ}(3, 4) = 3$, $LCP[3] = 1$; $\mathrm{PSV}(3) = 1$, $\mathrm{NSV}(3) = 5$ | $[1..4]$, the node `i` |
| `suffix_link([10..11])` | $\Psi(10) = 8$, $\Psi(11) = 9$; LCA of the leaves 8 and 9 | $[8..9]$, `ssi` to `si` |
| `suffix_link([3..4])` | $\Psi(3) = 10$, $\Psi(4) = 11$ | $[10..11]$, `issi` to `ssi` |

$\Psi = [5, 0, 7, 10, 11, 4, 1, 6, 2, 3, 8, 9]$ here. With $b = 8$, the gamma-coded gaps of $\Psi$ take 38 binary digits, and $H$ takes 24.

## Correctness

The full proof is in the proof file of this page. Its main steps:

1. **Nodes are lcp-intervals.** By the [LCP-RMQ reduction](/lcp-rmq-reduction/), the suffixes of ranks $a < c$ share $\min LCP[a+1 \ldots c]$ symbols. So a node of depth $\ell > 0$ with label $u$ is the maximal range in which all values are at least $\ell$, and the range of the node with value $LCP[k]$ around $k$ is $[\mathrm{PSV}(k)..\mathrm{NSV}(k) - 1]$.
2. **Parent, children and LCA.** Each follows from step 1: the parent of $v$ is the smallest lcp-interval that strictly contains $v$, the children are cut at the $\ell$-indices, and the LCA of two disjoint ranges has the depth of the minimum between them.
3. **Suffix link.** $\Psi$ maps the ranks of the suffixes that start with $cu$, in order, to ranks of suffixes that start with $u$, and keeps the lcp minus one.
4. **H.** The values $PLCP[p] + 2p$ strictly increase, so the $p$-th one of $H$ is at $PLCP[p] + 2p$.

## Complexity

Let $t_{SA}$ be the time of one $SA$ lookup, $O(s)$ steps of $\Psi$ with $O(b)$ gamma decodes each in the implementation, and $t_{LCP}$ the time of one LCP value, $t_{SA}$ plus one select on $H$.

| operation | time in this implementation | space |
|---|---|---|
| build | $O(n)$ for an integer alphabet with a linear suffix sort; the implementation sorts by prefix doubling | $\Theta(n)$ words during the build only |
| `depth`, `parent`, `first_child`, `next_sibling`, `lca` | $O(b)$ LCP values and $O(\log n)$ steps in the tree of minima, so $O(b \cdot t_{LCP} + \log n)$ | |
| `suffix_link` | the same, plus two $\Psi$ values | |
| `letter(v, d)` | $O(t_{SA})$: one lookup and one inverse | |
| `child(v, c)` | $O(\sigma)$ times the above | |
| the stored parts | | the gaps of $\Psi$, $2N$ positions for $H$, $O(n / s + n / b)$ samples, and $O(n / b)$ block minima |

The gaps of $\Psi$ take space close to the size of the compressed text, as on the [compressed suffix array](/compressed-suffix-array/) page, and $H$ adds $2N$ binary digits. Sadakane's CST takes the size of the compressed suffix array plus $6n + o(n)$ binary digits, with most operations in $O(1)$ time and string depth, letter and child in time that depends on $t_{SA}$. The variant of Fischer, Mäkinen and Navarro drops the parentheses and stores fewer extra structures, so it fits in entropy-bounded space, with operations in time polylogarithmic in $n$.

## Variants

- **Balanced parentheses.** Sadakane stores the tree shape as a [balanced parentheses](/balanced-parentheses-representation/) sequence of at most $4n$ positions, with rank, select and excess queries, and maps each node to its range of leaves. This gives most operations in $O(1)$ time.
- **NSV, PSV and RMQ only.** Fischer, Mäkinen and Navarro, as on this page, find all nodes from the LCP array, with no tree stored.
- **Fully compressed.** Russo, Navarro and Oliveira keep only a sample of the nodes, and reach the others with suffix links and the compressed suffix array. The space is that of the compressed suffix array plus a lower order term.
- **Enhanced suffix array.** The [enhanced suffix array](/enhanced-suffix-array/) gives the same operations with plain arrays, in $\Theta(n)$ words and with faster operations.
- **Index without a tree.** For search only, the [FM-index](/fm-index/) or the [compressed suffix array](/compressed-suffix-array/) is enough; the tree is needed for algorithms that walk it, such as [matching statistics](/matching-statistics/) or [maximal repeats](/maximal-repeats/).

## When to use it

Use a compressed suffix tree when a suffix tree algorithm must run on a text so large that a pointer-based tree, or even an enhanced suffix array, does not fit in memory, such as a collection of genomes. Expect each operation to be slower by a large factor than in a plain tree, since every LCP value costs an $SA$ lookup. If memory is enough, use the [enhanced suffix array](/enhanced-suffix-array/) or a [suffix tree](/suffix-tree/).

## Pitfalls

- **Boundary values.** The values $LCP[0] = LCP[N] = -1$ are needed. With 0 there, PSV and NSV of a 0-index do not exist, and the root cannot be found as a parent.
- **Leftmost minimum.** RMQ must return the leftmost minimum, which is the first $\ell$-index. Another minimum gives a wrong first child.
- **Next sibling test.** A node is the last child if $LCP[lb] > LCP[rb+1]$, with a strict test. With equal values, $rb + 1$ is still an $\ell$-index of the parent.
- **Leaf depth.** The depth of a leaf counts the sentinel. Without the sentinel, a suffix can end inside an edge, and the ranges no longer describe the tree.
- **Cost of LCP.** Each LCP value costs an $SA$ lookup. A scan over a block should read each value once.

## Implementations

The Python class stores $\Psi$ as gamma-coded gaps with samples, $H$ as one integer, and the block minima in a binary tree. It builds $SA$ by prefix doubling and PLCP by Kasai's method, and then drops both. The scans for select and for the block minima are linear inside a block, where a real CST uses constant-time select structures. The tests check every node of the tree against the suffix tree built from the branching substrings of $T\$$: depth, parent, children, suffix link, letters, `child` for each symbol, and `lca` and `find`, on random strings over alphabets of size 1, 2 and 4, on $\texttt{a}^n$ and $(\texttt{ab})^n$, and with several sampling steps and block sizes. The sdsl library of Gog and others gives tested C++ versions of several CSTs.

## History

Munro, Raman and Rao gave a suffix tree in $n \log n + O(n)$ binary digits in 1998, but it still needed the full suffix array. Grossi and Vitter, and then Sadakane, made the suffix array compressed in 2000. Sadakane showed in 2002 how to store the LCP information in $2n + o(n)$ binary digits, and in 2007 he combined it with a compressed suffix array and a balanced parentheses tree into the first compressed suffix tree with all operations. Russo, Navarro and Oliveira reduced the extra space to a lower order term with the fully compressed suffix tree, and Fischer, Mäkinen and Navarro replaced the tree with nearest smaller value queries in 2009. Later work, such as that of Ohlebusch, Fischer and Gog, and of Gog in the sdsl library, made these trees practical.

## References
