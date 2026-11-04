---
tag: QA72X1
kind: data-structure
slug: louds-tree
name: LOUDS tree
aliases:
- LOUDS
- level-order unary degree sequence
area: data-structures/succinct-structures
level: advanced
summary: A succinct tree encoding by the level-order unary degree sequence, using 2n + o(n) bits.
model: word-ram
complexity:
  vars: {n: the number of nodes}
  time: {parent: O(1), child: O(1), degree: O(1), next_sibling: O(1), build: O(n)}
  space: {total: "2 n + o(n)"}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1989
  people: [Guy Jacobson]
  note: Jacobson introduced the level-order unary degree sequence in his 1989 FOCS paper and thesis; Delpratt, Rahman and Raman engineered it in 2006.
prereqs: [ordinal-tree, rank-select-dictionary, level-order-traversal]
see_also: [louds-trie, balanced-parentheses-representation, dfuds, unary-coding, succinct-data-structures, succinct-graph-representation, jacobson-rank, rooted-tree]
sources:
  - paper: doi:10.1109/SFCS.1989.63533
    title: Guy Jacobson, Space-efficient static trees and graphs, 30th Annual Symposium on Foundations of Computer Science (FOCS 1989), 549-554
    locator: the level-order unary degree sequence of an ordinal tree in 2n + 1 bits, and the parent and child formulas with rank and select
  - paper: doi:10.1007/11764298_12
    title: O'Neil Delpratt, Naila Rahman and Rajeev Raman, Engineering the LOUDS succinct tree representation, Experimental Algorithms (WEA 2006), LNCS 4007, 134-145
    locator: the numbering of nodes by level order, the navigation formulas, and the experiments against pointer trees and parenthesis representations
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 8, Section 8.1 (Level-Order Unary Degree Sequence)
---

A LOUDS tree stores the shape of an [ordinal tree](/ordinal-tree/) of $n$ nodes as one bit string of $2n + 1$ bits: the nodes are visited in [level order](/level-order-traversal/), and each node writes its number of children in [unary](/unary-coding/), as that many 1s followed by a 0. With [rank and select](/rank-select-dictionary/) on this string, the parent, the $i$-th child, the degree and the siblings of a node take $O(1)$ time on the [word RAM](/word-ram/), in $2n + o(n)$ bits in all. The nodes are numbered in level order, so satellite data can be kept in a plain array indexed by that number. Jacobson introduced LOUDS in 1989. It is the simplest succinct tree and the usual base of succinct tries, such as the [LOUDS trie](/louds-trie/), but it does not support depth, subtree size or lowest common ancestors.

## In plain words

Visit the nodes of a tree level by level, from the top, and from left to right within each level. For each node, write a 1 for each of its children, and then a 0. Put an extra "10" at the front, as if an imaginary node sat above the root with the root as its only child.

Every node now owns one 1, the one its parent wrote for it, and one group of bits, the 1s it wrote for its own children. The 1s appear in the same order as the nodes, so the tenth 1 belongs to the tenth node. To go from a node to its children, find its group by counting 0s. To go from a node to its parent, find its 1 and count the 0s before it.

## The abstract type

The structure stores a static [ordinal tree](/ordinal-tree/) and answers `parent(k)`, `child(k, i)`, `degree(k)`, `is_leaf(k)`, `next_sibling(k)`, `prev_sibling(k)` and `child_rank(k)`, where a node is named by its level-order number $k$, with the root at $k = 0$. Operations that depend on the depth-first shape, such as `subtree_size`, `depth` and `lca`, are not supported; for them use [BP](/balanced-parentheses-representation/) or [DFUDS](/dfuds/).

## Representation

Let the nodes in level order be $v_0, v_1, \ldots, v_{n-1}$, with $v_0$ the root, and let $d_k$ be the degree of $v_k$. The LOUDS string is

$$L = 10\; 1^{d_0} 0\; 1^{d_1} 0\; \cdots\; 1^{d_{n-1}} 0,$$

of $2 + \sum_k (d_k + 1) = 2 + (n - 1) + n = 2n + 1$ bits, with $n$ ones and $n + 1$ zeros. The prefix 10 is the code of a virtual super-root whose only child is $v_0$. A rank and select index is built on $L$.

Two facts make the navigation work:

- the $(k+1)$-th 1 of $L$ stands for $v_k$, because the children of each node are written in level order, and the root's 1 comes first;
- the code of $v_k$ starts just after the $(k+1)$-th 0 of $L$, because the codes of the super-root and of $v_0, \ldots, v_{k-1}$ each end with one 0.

The invariant is that $L$ is as defined; the structure is static.

## Operations

```pseudo id=main
CHILD(k, i)                                  ▷ the i-th child of v_k, 1 ≤ i ≤ DEGREE(k)
L1  s ← SELECT0(k + 1)                              ▷ the 0 just before the code of v_k
L2  if i > DEGREE(k) then return none
L3  return RANK1(s) + i − 1

DEGREE(k)
L4  return SELECT0(k + 2) − SELECT0(k + 1) − 1

PARENT(k)
L5  if k = 0 then return none
L6  p ← SELECT1(k + 1)                              ▷ the 1 that stands for v_k
L7  return RANK0(p) − 1

NEXT-SIBLING(k)
L8  p ← SELECT1(k + 1)
L9  return k + 1 if L[p + 1] = 1 else none

CHILD-RANK(k)                                ▷ k ≥ 1
L10 p ← SELECT1(k + 1)
L11 return p − SELECT0(RANK0(p))
```

**Child.** The children of $v_k$ are the 1s of its code, which starts at $s + 1$. Since $L[s] = 0$, $\text{rank}_1(s)$ is the number of 1s before the code, so the first child's 1 is the $(\text{rank}_1(s) + 1)$-th 1, which stands for $v_{\text{rank}_1(s)}$. The $i$-th child follows $i - 1$ places later.

**Degree.** The code of $v_k$ lies between the $(k+1)$-th and the $(k+2)$-th 0, and its 1s are the bits strictly between them. `is_leaf(k)` is $L[\text{SELECT0}(k+1) + 1] = 0$.

**Parent.** The 1 at $p$ stands for $v_k$ and lies inside the code of its parent. The number of 0s before $p$ is the number of codes that end before $p$: the super-root's and those of $v_0, \ldots, v_{j-1}$ if the parent is $v_j$. So $j = \text{rank}_0(p) - 1$.

**Siblings.** Siblings are consecutive 1s inside one code, so the next sibling of $v_k$ exists exactly when the bit after its 1 is a 1, and it is $v_{k+1}$. `prev_sibling(k)` is $k - 1$ if $L[p - 1] = 1$. `child_rank(k)` is the distance from the 0 that starts the parent's code to $p$.

**Build.** A breadth-first traversal writes $L$ in $O(n)$ time, and the rank and select index takes $O(n)$ more.

## Example

Take the tree of the [ordinal tree](/ordinal-tree/) page: root $A$ with children $B$, $C$, $D$; $B$ with children $E$, $F$; $D$ with child $G$; $G$ with child $H$. In level order, $v_0, \ldots, v_7 = A, B, C, D, E, F, G, H$, with degrees $3, 2, 0, 1, 0, 0, 1, 0$.

| position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $L$ | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| code of | super | super | $A$ | $A$ | $A$ | $A$ | $B$ | $B$ | $B$ | $C$ | $D$ | $D$ | $E$ | $F$ | $G$ | $G$ | $H$ |
| 1 stands for | $A$ | | $B$ | $C$ | $D$ | | $E$ | $F$ | | | $G$ | | | | $H$ | | |

$L$ has $17 = 2 \cdot 8 + 1$ bits. The 0s are at 1, 5, 8, 9, 11, 12, 13, 15, 16 and the 1s at 0, 2, 3, 4, 6, 7, 10, 14.

- DEGREE$(0)$: $\text{select}_0(2) - \text{select}_0(1) - 1 = 5 - 1 - 1 = 3$.
- CHILD$(0, 3)$: $s = \text{select}_0(1) = 1$, $\text{rank}_1(1) = 1$, so the answer is $1 + 2 = 3$, node $D$.
- CHILD$(1, 2)$: $s = \text{select}_0(2) = 5$, $\text{rank}_1(5) = 4$, so the answer is $4 + 1 = 5$, node $F$.
- PARENT$(6)$: $p = \text{select}_1(7) = 10$ and $\text{rank}_0(10) = 4$, so the parent is $v_3 = D$.
- NEXT-SIBLING$(1)$: $p = \text{select}_1(2) = 2$ and $L[3] = 1$, so $C$. NEXT-SIBLING$(3)$: $p = 4$ and $L[5] = 0$, so $D$ is the last child.
- CHILD-RANK$(5)$: $p = \text{select}_1(6) = 7$, $\text{rank}_0(7) = 2$ and $\text{select}_0(2) = 5$, so $F$ is child $7 - 5 = 2$ of $B$.

## Correctness

The two facts of the representation are proved by induction on the level order: a breadth-first traversal lists the children of $v_0$ first, then those of $v_1$, and so on, which is exactly the order in which their 1s are written. The formulas then follow by counting the 0s and 1s before a position, as explained under Operations. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

| operation | time, worst case |
|---|---|
| build | $O(n)$ |
| parent, child, degree, is_leaf, siblings, child_rank | $O(1)$: at most two selects and one rank |

**Space.** $L$ has $2n + 1$ bits, and the rank and select index adds $o(n)$ bits, for $2n + o(n)$ in all. The [information-theoretic minimum](/information-theoretic-bound/) for ordinal trees is $\lg C_{n-1} = 2n - \Theta(\lg n)$ bits, so LOUDS is succinct. A pointer tree with first-child, next-sibling and parent pointers of 32 bits uses $96 n$ bits.

## Variants

- **LOUDS tries.** Store the label of the edge into each node in an array indexed by its level-order number; `child` by a label becomes a search among the labels of a contiguous range of children. This is the [LOUDS trie](/louds-trie/).
- **Fast child without select0.** Delpratt, Rahman and Raman number the nodes by the positions of their 1s and use the identity $\text{select}_0(\text{rank}_1(p) + 1)$ to move to the children, which replaces some selects by ranks.
- **Graphs.** Jacobson also encoded planar and bounded-genus graphs with similar unary degree sequences; see [succinct graph representations](/succinct-graph-representation/).
- **Binary trees.** A binary tree of $n$ nodes is stored in $2n + 1$ bits by writing two bits for each node, one for each possible child, in level order; Jacobson used this form too.
- **Dynamic LOUDS.** On a [dynamic bit vector](/dynamic-bit-vector/), insertion of a leaf is one insertion of a 1 and one of a 0, in $O(\lg n)$ time.

## When to use it

Use LOUDS when a static tree is navigated mostly between parents and children: tries for dictionaries and autocomplete, the dictionaries of speech and input-method engines, and the trees of XML or file paths where depth-first operations are rare. It is simpler and often faster than [BP](/balanced-parentheses-representation/) or [DFUDS](/dfuds/), since it needs only rank and select. When subtree sizes, depths or lowest common ancestors are needed, use BP with a [range min-max tree](/range-min-max-tree/), or DFUDS.

## Pitfalls

- **The super-root.** Without the leading 10, the formulas shift by one 0 and one 1, and the root has no 1 of its own. Keep the prefix, or adjust every formula consistently.
- **Node names.** The operations here use level-order numbers. Some texts name a node by the position of its 1 or of the start of its code; formulas from different sources cannot be mixed.
- **Degree of the last node.** DEGREE$(n - 1)$ uses the $(n+1)$-th 0, the last bit of $L$. A string without the final 0 breaks it.
- **No subtree operations.** Level order scatters a subtree over many levels, so `subtree_size` and `lca` cannot be computed from a few ranks; code that needs them must not choose LOUDS.
- **Satellite data order.** Data stored per node must be in level order, not in the order of the input tree or in preorder.

## Implementations

## History

Guy Jacobson introduced the level-order unary degree sequence in his 1989 FOCS paper "Space-efficient static trees and graphs" and his Carnegie Mellon thesis, together with the rank structure that makes it navigable. Delpratt, Rahman and Raman studied its engineering in 2006 and found it competitive with pointer trees and with the parenthesis representations. LOUDS tries are now used in practical string dictionaries.

## References
