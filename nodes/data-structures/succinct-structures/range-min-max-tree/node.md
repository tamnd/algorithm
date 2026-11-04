---
tag: EHY1SS
kind: data-structure
slug: range-min-max-tree
name: Range min-max tree
aliases:
- RMM tree
area: data-structures/succinct-structures
level: research
summary: A tree of min and max excess values over a balanced parenthesis sequence that speeds up tree navigation queries.
model: word-ram
complexity:
  vars: {n: the length of the parenthesis sequence}
  time: {fwdsearch: O(log n), bwdsearch: O(log n), findclose: O(log n), findopen: O(log n), enclose: O(log n), rmq: O(log n), build: O(n)}
  space: {total: "n + O(n / log n)"}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2010
  people: [Kunihiko Sadakane, Gonzalo Navarro]
  note: Sadakane and Navarro introduced the range min-max tree at SODA 2010 (journal version in ACM Transactions on Algorithms, 2014) to reduce all succinct tree operations to excess searches; Arroyuelo, Cánovas, Navarro and Sadakane showed in 2010 that its simple form is the fastest practical choice.
prereqs: [balanced-parentheses-representation, parenthesis-matching, segment-tree]
see_also: [dfuds, dynamic-bit-vector, range-minimum-query, lowest-common-ancestor, compressed-suffix-tree, four-russians-method, ordinal-tree, succinct-data-structures]
sources:
  - paper: doi:10.1145/2601073
    title: Gonzalo Navarro and Kunihiko Sadakane, Fully functional static and dynamic succinct trees, ACM Transactions on Algorithms 10(3), Article 16, 2014
    locator: Section 3 (the range min-max tree, fwdsearch and bwdsearch) and Table I (the reductions of the tree operations)
  - paper: doi:10.1137/1.9781611972900.9
    title: Diego Arroyuelo, Rodrigo Cánovas, Gonzalo Navarro and Kunihiko Sadakane, Succinct trees in practice, Workshop on Algorithm Engineering and Experiments (ALENEX 2010), 84-97
    locator: the practical range min-max tree with blocks of a few hundred bits and its comparison with LOUDS, BP and DFUDS
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 7 (Parentheses), Section 7.1 (the range min-max tree and the algorithms for fwdsearch, bwdsearch and minimum excess)
---

The range min-max tree, or rmM-tree, is an index over a [balanced parenthesis](/balanced-parentheses-representation/) sequence $P$ of length $n$ that answers excess searches: the first position after $i$ where the excess reaches a given value (*fwdsearch*), the last such position before $i$ (*bwdsearch*), and the minimum excess in a range. It cuts $P$ into blocks and builds a complete binary tree over them, storing in each node the total change of excess over its range and the minimum and maximum excess reached inside. Because the excess moves by exactly one at each position, a node whose minimum and maximum bracket a value is sure to contain it, so a search climbs and descends the tree in $O(\lg n)$ steps. Sadakane and Navarro introduced it in 2010; all [parenthesis matching](/parenthesis-matching/) queries, and with them every navigation operation on BP and [DFUDS](/dfuds/) trees, reduce to these searches.

## In plain words

Read a string of brackets from left to right and keep a running score: one up for an opening bracket and one down for a closing one. The matching close of an opening bracket is the first place after it where the score falls one below the score just after it.

To find such a place without reading the whole string, cut the string into pieces and note, for each piece, how much the score changes over it and the lowest and highest score it reaches. Put these notes in a tree, where each node sums up its two halves. Since the score moves one step at a time, if a piece's lowest and highest scores surround the target, the target is reached inside. So the search goes up the tree until a piece surrounds the target, then down into it.

## The abstract type

The structure stores a static sequence $P[0..n-1]$ of parentheses, with excess $E(i)$ = (number of `(`) − (number of `)`) in $P[0..i]$ and $E(-1) = 0$, and answers:

- $\text{fwdsearch}(i, d)$: the least $j > i$ with $E(j) = E(i) + d$, or none;
- $\text{bwdsearch}(i, d)$: the greatest $j < i$, $j \ge -1$, with $E(j) = E(i) + d$, or none;
- $\text{minexcess}(i, j)$ and $\text{rmq}(i, j)$: the minimum of $E$ on $[i, j]$ and its leftmost position;
- $\text{findclose}(i) = \text{fwdsearch}(i, -1)$, $\text{findopen}(j) = \text{bwdsearch}(j, 0) + 1$, $\text{enclose}(i) = \text{bwdsearch}(i, -2) + 1$.

The full Navarro-Sadakane version adds the number of minima in a range and the position of the $k$-th minimum, for `degree` and `child(v, i)` on BP trees.

## Representation

Cut $P$ into $\lceil n / b \rceil$ blocks of $b$ symbols and build a complete binary tree with the blocks as leaves, padded to a power of two. For a node $v$ whose range is $P[s..t]$, store

- $e(v) = E(t) - E(s - 1)$, the total excess of the range;
- $m(v) = \min_{s \le k \le t} E(k) - E(s - 1)$, the minimum relative excess;
- $M(v) = \max_{s \le k \le t} E(k) - E(s - 1)$, the maximum relative excess.

For internal $v$ with children $\ell$ and $r$: $e(v) = e(\ell) + e(r)$, $m(v) = \min(m(\ell), e(\ell) + m(r))$ and $M(v) = \max(M(\ell), e(\ell) + M(r))$, so the tree is built bottom up in $O(n / b)$ time after one pass over $P$. Padding leaves have $m = +\infty$ and $M = -\infty$. The excess $E(i)$ itself comes from $\text{rank}_1$ on $P$, as $2\,\text{rank}_1(i + 1) - (i + 1)$; this page's implementation keeps the excess before each block, which is the same information.

The key fact is *discrete continuity*: inside a range, consecutive excess values differ by exactly 1, so every integer between the minimum and the maximum of a range occurs in it. Hence the target value $x$ occurs in the range of $v$, entered with excess $c$ just before it, if and only if $c + m(v) \le x \le c + M(v)$.

## Operations

```pseudo id=main
FWDSEARCH(i, d)
L1  t ← E(i) + d
L2  scan P[i + 1 ..] to the end of the block of i; return the first j with E(j) = t, if any
L3  v ← the leaf of the block of i;  c ← E(last position of that block)
L4  while v is not the root do
L5      if v is a left child and c + m(sibling) ≤ t ≤ c + M(sibling) then return DESCEND(sibling, c, t)
L6      if v is a left child then c ← c + e(sibling)
L7      v ← parent(v)
L8  return none

DESCEND(v, c, t)                         ▷ c is the excess just before the range of v
L9  while v is not a leaf do
L10     if c + m(left(v)) ≤ t ≤ c + M(left(v)) then v ← left(v)
L11     else c ← c + e(left(v));  v ← right(v)
L12 scan the block of v from its start with excess c; return the first j with E(j) = t

FINDCLOSE(i)
L13 return FWDSEARCH(i, −1)
FINDOPEN(j)
L14 return BWDSEARCH(j, 0) + 1
ENCLOSE(i)
L15 return BWDSEARCH(i, −2) + 1
```

**Forward search.** First the rest of the block of $i$ is scanned. Then the search climbs: every right sibling met on the way covers the next stretch of $P$ to the right, in order, and $c$ is kept equal to the excess just before that stretch. The first sibling whose bracket $[c + m, c + M]$ contains the target holds the answer, by discrete continuity, and none of the stretches skipped before it does. The descent always prefers the left child, so it finds the leftmost occurrence.

**Backward search.** The mirror image: scan the block of $i$ leftward, climb looking at left siblings, with $c$ equal to the excess at the end of the stretch, so that the range of a sibling $u$ holds the values $c - e(u) + m(u)$ to $c - e(u) + M(u)$; descend preferring right children and scan the leaf from its end. If the climb reaches the root without success, the answer is $-1$ when the target is 0 (the virtual position before $P$), and none otherwise.

**Range minimum.** Scan the partial blocks at both ends and cover the full blocks in between by $O(\lg n)$ canonical nodes, as in a [segment tree](/segment-tree/), folding $\min(\text{best}, c + m(u))$ and $c \leftarrow c + e(u)$ from left to right. The leftmost position of the minimum $\mu$ is $i$ if $E(i) = \mu$, and otherwise $\text{fwdsearch}(i, \mu - E(i))$, because no position before it in the range is as low.

**Block scans in $O(1)$.** In theory, each block is scanned in chunks of $\frac12 \lg n$ bits with a [Four Russians](/four-russians-method/) table that gives, for each chunk and each relative target, the first position where it is reached, or the chunk's own $e$, $m$ and $M$.

## Example

Take the BP sequence of the tree $A(B(E, F), C, D(G(H)))$, $P$ = `((()())()((())))`, with $n = 16$ and blocks of $b = 4$.

| block | symbols | positions | $E$ at its positions | $e$ | $m$ | $M$ |
|---|---|---|---|---|---|---|
| 0 | `((()` | 0-3 | 1 2 3 2 | 2 | 1 | 3 |
| 1 | `())(` | 4-7 | 3 2 1 2 | 0 | −1 | 1 |
| 2 | `)(((` | 8-11 | 1 2 3 4 | 2 | −1 | 2 |
| 3 | `))))` | 12-15 | 3 2 1 0 | −4 | −4 | −1 |

The internal nodes are $u_{01}$ over blocks 0-1 with $(e, m, M) = (2, 1, 3)$, $u_{23}$ over blocks 2-3 with $(-2, -2, 2)$, and the root with $(0, 0, 4)$.

- FINDCLOSE$(1)$: $E(1) = 2$, so $t = 1$. The rest of block 0 has excess 3, 2: no hit. At the leaf of block 0, $c = 2$; its right sibling, block 1, brackets $[2 - 1, 2 + 1] = [1, 3] \ni 1$, so descend into it and scan: 3, 2, 1 at position 6. The answer is 6.
- FINDCLOSE$(0)$: $t = 0$. Block 0 gives 2, 3, 2; block 1 brackets $[1, 3] \not\ni 0$, so $c \leftarrow 2 + 0 = 2$ and climb to $u_{01}$. Its right sibling $u_{23}$ brackets $[2 - 2, 2 + 2] = [0, 4] \ni 0$. Descend: the left child, block 2, brackets $[2 - 1, 2 + 2] = [1, 4] \not\ni 0$, so $c \leftarrow 4$ and go to block 3, scanned from 4: 3, 2, 1, 0 at position 15.
- ENCLOSE$(11)$: $E(11) = 4$, so the target of BWDSEARCH$(11, -2)$ is 2. Scanning block 2 leftward gives $E(10) = 3$, $E(9) = 2$: hit at 9, and the answer is $10$, node $G$, the parent of $H$.
- RMQ$(4, 11)$: block 1 from position 4 gives the minimum 1 at 6; block 2, positions 8 to 11, gives 1 at 8. The minimum is 1, and its leftmost position is 6.

## Correctness

The proof rests on discrete continuity and on the order in which the climb meets the siblings: the stretches of $P$ covered by the right siblings met on the way up, followed by the rest of the tree, tile the suffix after the block of $i$ from left to right, so the first stretch that brackets the target contains its first occurrence. The full argument, including the backward search and the range minimum, is in [the proof of correctness](proofs/correctness.md).

## Complexity

| operation | time, $b = \Theta(\lg^2 n)$ with chunk tables | this page's implementation |
|---|---|---|
| fwdsearch, bwdsearch, findclose, findopen, enclose | $O(\lg n)$ | $O(b + \lg(n / b))$ |
| minexcess, rmq | $O(\lg n)$ | $O(b + \lg(n / b))$ |
| build | $O(n / \lg n)$ with chunk tables | $O(n)$ |

**Space.** Each of the $O(n / b)$ nodes stores three values of $O(\lg n)$ bits, so the tree takes $O(n \lg n / b)$ bits, which is $O(n / \lg n)$ for $b = \Theta(\lg^2 n)$. The values $m$ and $M$ of a node over a range of length $L$ need only $O(\lg L)$ bits, which lowers the space of the lower levels further.

**Constant time.** Navarro and Sadakane build a two-level scheme: small rmM-trees over chunks of polylogarithmic length, plus a structure over the chunk boundaries, to get all operations in $O(1)$ time with $O(n / \text{polylog}\, n)$ extra bits. The dynamic version, with a tree of fan-out $\Theta(\lg^\varepsilon n)$ over a [dynamic bit vector](/dynamic-bit-vector/), supports insertions and deletions in $O(\lg n / \lg \lg n)$ time.

## Variants

- **Practical rmM-tree.** Blocks of 256 to 1024 bits, a tree stored as arrays with no pointers, and byte-wise tables for scans. Arroyuelo et al. found it the best overall choice among succinct tree representations.
- **Number of minima.** Storing, in each node, the number of positions that reach its minimum gives `degree` and `child(v, i)` on BP trees in $O(\lg n)$ time.
- **Dynamic rmM-tree.** With the blocks as leaves of a balanced tree, insertions and deletions of parentheses update $O(\lg n)$ nodes.
- **For DFUDS and LOUDS.** The same tree over a DFUDS sequence answers its matching queries. LOUDS needs no rmM-tree, only rank and select.
- **Compressed suffix trees.** The topology of a [compressed suffix tree](/compressed-suffix-tree/) is a BP sequence with an rmM-tree, which gives parent, LCA and string-depth navigation.

## When to use it

Use the rmM-tree whenever a static or dynamic tree is stored as parentheses and needs more than parent and child: subtree sizes, depths, level ancestors, lowest common ancestors and child by index. It is the standard engine of BP trees in practice. For a static tree that only needs parent and child steps, [LOUDS](/louds-tree/) avoids it. For [range minimum queries](/range-minimum-query/) on arrays, the same minimum search over the BP or DFUDS of a Cartesian tree gives a succinct solution.

## Pitfalls

- **Relative values.** $m$ and $M$ are relative to the excess before the node's range, not absolute; forgetting to add $c$ breaks every bracket test.
- **Leftmost and rightmost.** A forward descent must prefer the left child and a backward one the right child; otherwise the search finds some occurrence, not the first.
- **The virtual position $-1$.** findopen of a `)` whose match is at 0 needs $E(-1) = 0$; a backward search that ignores it returns none for the root.
- **The block of $i$.** The scan of the block of $i$ must start after $i$ (forward) or before $i$ (backward), and the climb must start at the leaf of that block, not at its parent.
- **Padding.** Padding leaves must have an empty bracket ($m > M$) so that they are never entered.

## Implementations

## History

Sadakane and Navarro presented the range min-max tree at SODA 2010 as part of a "fully functional" succinct tree that supports, through fwdsearch, bwdsearch and range minima, every navigation operation that had been proposed for BP, DFUDS and LOUDS, in a single and simpler framework, both static and dynamic. Arroyuelo, Cánovas, Navarro and Sadakane showed at ALENEX 2010 that a simplified rmM-tree is the fastest practical BP implementation. The journal version appeared in ACM Transactions on Algorithms in 2014.

## References
