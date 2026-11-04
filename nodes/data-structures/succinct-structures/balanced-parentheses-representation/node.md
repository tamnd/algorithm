---
tag: 8WYTP6
kind: data-structure
slug: balanced-parentheses-representation
name: Balanced parentheses representation
aliases:
- BP representation
- balanced parentheses tree
area: data-structures/succinct-structures
level: advanced
summary: A succinct tree encoding by a balanced parenthesis sequence, supporting navigation through matching queries.
model: word-ram
complexity:
  vars: {n: the number of nodes}
  time: {parent: O(1), first_child: O(1), next_sibling: O(1), subtree_size: O(1), depth: O(1), lca: O(1), build: O(n)}
  space: {total: "2 n + o(n)"}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1997
  people: [J. Ian Munro, Venkatesh Raman]
  note: Jacobson used balanced parentheses for trees and graphs in 1989; Munro and Raman gave constant-time matching and BP trees in 1997 (SIAM Journal on Computing 2001); Navarro and Sadakane made the set of operations complete with the range min-max tree.
prereqs: [ordinal-tree, parenthesis-matching, rank-select-dictionary]
see_also: [louds-tree, dfuds, range-min-max-tree, balanced-parentheses, dyck-word, preorder-traversal, lowest-common-ancestor, compressed-suffix-tree]
sources:
  - paper: doi:10.1137/S0097539799364092
    title: J. Ian Munro and Venkatesh Raman, Succinct representation of balanced parentheses and static trees, SIAM Journal on Computing 31(3), 2001, 762-776
    locator: the BP encoding of an ordinal tree in 2n + o(n) bits, with parent, child, sibling and subtree size in O(1) time
  - paper: doi:10.1109/SFCS.1989.63533
    title: Guy Jacobson, Space-efficient static trees and graphs, 30th Annual Symposium on Foundations of Computer Science (FOCS 1989), 549-554
    locator: the use of balanced parentheses for trees and planar graphs
  - paper: doi:10.1145/2601073
    title: Gonzalo Navarro and Kunihiko Sadakane, Fully functional static and dynamic succinct trees, ACM Transactions on Algorithms 10(3), Article 16, 2014
    locator: Table I (the operations and their reductions to fwdsearch, bwdsearch and rmq), including lca, level ancestor and depth
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 8, Section 8.2 (Balanced Parentheses)
---

The balanced parentheses (BP) representation stores an [ordinal tree](/ordinal-tree/) of $n$ nodes as a sequence of $2n$ parentheses written by a depth-first traversal: an opening parenthesis when a node is entered and a closing one when it is left. A node is named by the position of its opening parenthesis, and its subtree is exactly the stretch up to the matching close. With [parenthesis matching](/parenthesis-matching/) and the excess of a prefix, all the usual tree operations, including subtree size, depth, ancestor tests and the [lowest common ancestor](/lowest-common-ancestor/), take $O(1)$ time on the [word RAM](/word-ram/), in $2n + o(n)$ bits. Munro and Raman made it constant time in 1997. It is the most complete of the three classic succinct trees, next to [LOUDS](/louds-tree/) and [DFUDS](/dfuds/), and it is the usual topology of [compressed suffix trees](/compressed-suffix-tree/).

## In plain words

Walk around the tree from the root, going down into the first child, then its first child, and so on, and coming back up after each subtree. Write an opening bracket each time you step down into a node and a closing bracket each time you step back up out of it.

Each node gets one pair of brackets, and everything between its two brackets is its subtree. The number of open brackets around a node is its depth. Its parent is the closest pair that wraps it, and its next sibling starts right after its closing bracket. So tree questions become bracket questions, and with a small index those are fast.

## The abstract type

The structure stores a static [ordinal tree](/ordinal-tree/) and answers `first_child(v)`, `next_sibling(v)`, `parent(v)`, `is_leaf(v)`, `subtree_size(v)`, `depth(v)`, `is_ancestor(u, v)`, `lca(u, v)` and `preorder_rank(v)`. With the full Navarro-Sadakane toolkit it also answers `child(v, i)`, `degree(v)`, `level_ancestor(v, d)` and `height(v)`. A node $v$ is the position of its `(` in $P$.

## Representation

$P[0..2n-1]$ is a [bit vector](/bit-vector/) with `(` as 1 and `)` as 0, written by a [preorder](/preorder-traversal/) traversal: `(` on entering a node, `)` after its last child. The excess $E(i) = 2\,\text{rank}_1(i+1) - (i + 1)$ is the number of open pairs after position $i$. On top of $P$ sit a [rank/select](/rank-select-dictionary/) index and a structure for $\text{findclose}$, $\text{enclose}$ and $\text{rmq}$ of the excess, such as the [range min-max tree](/range-min-max-tree/). The invariant is that the pair of $v$ encloses exactly the pairs of its descendants, and the pairs of its children follow each other in order.

## Operations

```pseudo id=main
FIRST-CHILD(v)
L1  if P[v + 1] = ( then
L2      return v + 1                       ▷ else v is a leaf

NEXT-SIBLING(v)
L3  j ← FINDCLOSE(v)
L4  if P[j + 1] = ( then
L5      return j + 1                       ▷ else v is the last child

PARENT(v)
L6  if E(v) = 1 then return none           ▷ v is the root
L7  return ENCLOSE(v)

SUBTREE-SIZE(v)
L8  return (FINDCLOSE(v) − v + 1) / 2

DEPTH(v)
L9  return E(v) − 1                        ▷ the root has depth 0

IS-ANCESTOR(u, v)
L10 return u ≤ v ≤ FINDCLOSE(u)

LCA(u, v)
L11 if u > v then swap u, v
L12 if IS-ANCESTOR(u, v) then return u
L13 m ← RMQ(u, v)                          ▷ leftmost minimum of E on [u, v]
L14 return ENCLOSE(m + 1)
```

**Children and siblings.** The first child, if any, opens right after $v$. The subtree of $v$ ends at $\text{findclose}(v)$, and the next sibling opens right after it; a `)` there closes the parent instead.

**Parent and depth.** The excess at $v$ counts the pairs that are open after $v$ opens, that is, $v$ and its ancestors, so the depth is $E(v) - 1$ and the root is the only node with $E(v) = 1$. The parent is the tightest enclosing pair.

**LCA.** If neither node is an ancestor of the other, the walk from $u$ to $v$ in $P$ climbs out of the subtrees until it reaches the child of the LCA that contains $u$, closes it, and then enters other children. The minimum excess on $[u, v]$ is reached at the `)` of a child of the LCA, so the pair after it is again a child and its enclosing pair is the LCA.

**Other operations.** $\text{preorder\_rank}(v) = \text{rank}_1(v)$, $\text{is\_leaf}(v)$ is $P[v+1] = )$, $\text{level\_ancestor}(v, d) = \text{bwdsearch}(v, -d - 1) + 1$, and $\text{degree}$ and $\text{child}(v, i)$ count the minima of $E$ in the range of $v$, which the range min-max tree stores. In this page's implementation `degree` walks the siblings.

## Example

The tree $A(B(E, F), C, D(G(H)))$ gives $P$ = `((()())()((())))`.

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $P[i]$ | ( | ( | ( | ) | ( | ) | ) | ( | ) | ( | ( | ( | ) | ) | ) | ) |
| $E(i)$ | 1 | 2 | 3 | 2 | 3 | 2 | 1 | 2 | 1 | 2 | 3 | 4 | 3 | 2 | 1 | 0 |
| opens | $A$ | $B$ | $E$ | | $F$ | | | $C$ | | $D$ | $G$ | $H$ | | | | |

- FIRST-CHILD$(B = 1)$: $P[2] = ($, so $E$ at 2. FIRST-CHILD$(E = 2)$: $P[3] = )$, a leaf.
- NEXT-SIBLING$(B)$: $\text{findclose}(1) = 6$ and $P[7] = ($, so $C$. NEXT-SIBLING$(D = 9)$: $\text{findclose}(9) = 14$ and $P[15] = )$, none.
- PARENT$(F = 4)$: $E(4) = 3$, and enclose gives 1, node $B$.
- SUBTREE-SIZE$(D)$: $(14 - 9 + 1)/2 = 3$. DEPTH$(H = 11)$: $E(11) - 1 = 3$.
- LCA$(F, H)$ = LCA$(4, 11)$: $F$ is not an ancestor of $H$, since $\text{findclose}(4) = 5 < 11$. The minimum of $E$ on $[4, 11]$ is 1, first at 6, and $\text{enclose}(7) = 0$, so the answer is $A$.
- LCA$(E, F)$ = LCA$(2, 4)$: the minimum of $E$ on $[2, 4]$ is 2 at position 3, and $\text{enclose}(4) = 1$, node $B$.

## Correctness

Every operation rests on two facts about the preorder writing: the pair of $v$ contains exactly the pairs of the subtree of $v$, and $E(v)$ is the depth of $v$ plus one. The first holds because the traversal writes the whole subtree between entering and leaving $v$. The second holds because the open pairs right after $v$ opens are those of the nodes entered and not yet left, which are $v$ and its ancestors. The LCA rule needs one more fact, about where the excess is lowest between two nodes. All three are proved in [the proof of correctness](proofs/correctness.md).

## Complexity

| operation | time with the full index | time in this page's implementation |
|---|---|---|
| build | $O(n)$ | $O(n)$ |
| first_child, is_leaf, depth, preorder_rank | $O(1)$ | $O(1)$ |
| next_sibling, parent, subtree_size, is_ancestor | $O(1)$ | $O(n)$ scans |
| lca, level_ancestor | $O(1)$ | $O(n)$ scans |
| degree, child$(v, i)$ | $O(1)$ (Navarro-Sadakane) | $O(\text{degree})$ sibling steps |

**Space.** $P$ takes $2n$ bits, rank and select $o(n)$ bits, and the matching and excess structures $o(n)$ bits; Navarro and Sadakane get all operations in $2n + O(n / \text{polylog}\, n)$ bits. The minimum is $\lg C_{n-1} = 2n - \Theta(\lg n)$ bits.

## Variants

- **BP with a range min-max tree.** The practical form uses blocks of a few hundred bits and the [range min-max tree](/range-min-max-tree/), with $O(\lg n)$ time for everything; it is what libraries such as sdsl call the BP support.
- **Dynamic BP.** Inserting or deleting a node inserts or deletes one pair; over a dynamic sequence, all operations take $O(\lg n / \lg \lg n)$ time (Navarro and Sadakane).
- **DFUDS.** The [depth-first unary degree sequence](/dfuds/) is also a balanced sequence, in which `child(v, i)` and `degree` are direct, at the cost of depth-related operations.
- **Binary trees.** A binary tree can be stored as the BP of the ordinal tree obtained by the [left-child right-sibling](/left-child-right-sibling/) correspondence, which maps $n$-node binary trees to $(n+1)$-node ordinal trees.
- **Cartesian trees for RMQ.** The BP or DFUDS of a [Cartesian tree](/cartesian-tree/) answers [range minimum queries](/range-minimum-query/) in $2n + o(n)$ bits without the array.

## When to use it

Use BP when a static tree needs depth-first operations: subtree sizes, ancestor tests, depths, preorder numbers and lowest common ancestors. Compressed suffix trees, XML indexes and succinct phylogenetic or syntax trees use it. When only parents and children are needed, [LOUDS](/louds-tree/) is simpler and often faster; when `child(v, i)` by index dominates, [DFUDS](/dfuds/) is direct.

## Pitfalls

- **Node names are positions.** A node is the position of its `(`, not its preorder number; convert with $\text{rank}_1$ and $\text{select}_1$ when satellite data is stored in preorder.
- **Depth off by one.** $E(v)$ is the depth plus one with the root at depth 0. Mixing the two conventions breaks level ancestor.
- **The end of $P$.** NEXT-SIBLING of the root reads $P[2n]$, past the end; guard it.
- **LCA when one is an ancestor.** The RMQ rule gives the parent of the ancestor in that case, so the ancestor test of line L12 must come first.
- **Degree by walking.** A loop over siblings is $O(\text{degree})$ matching calls; for high-degree nodes use the counting of minima or DFUDS.

## Implementations

## History

Jacobson's 1989 paper used balanced parentheses to encode trees and planar graphs, with matching in $O(\lg n)$ bit probes. Munro and Raman, at FOCS 1997 and in the SIAM Journal on Computing in 2001, gave matching in $O(1)$ time with $o(n)$ extra bits and the BP tree with parent, child, sibling and subtree size in constant time. Geary, Rahman, Raman and Raman simplified the matching structure in 2004 and 2006. Sadakane and Navarro, at SODA 2010 and in ACM Transactions on Algorithms in 2014, reduced all operations to excess searches over the range min-max tree and made the representation fully functional and dynamic.

## References
