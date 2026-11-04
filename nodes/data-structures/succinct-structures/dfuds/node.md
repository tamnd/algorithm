---
tag: BT52AM
kind: data-structure
slug: dfuds
name: DFUDS
aliases:
- depth-first unary degree sequence
area: data-structures/succinct-structures
level: advanced
summary: A succinct tree encoding by the depth-first unary degree sequence, which supports child-rank navigation.
model: word-ram
complexity:
  vars: {n: the number of nodes}
  time: {child: O(1), degree: O(1), parent: O(1), child_rank: O(1), subtree_size: O(1), build: O(n)}
  space: {total: "2 n + o(n)"}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1999
  people: [David Benoit, Erik D. Demaine, J. Ian Munro, Rajeev Raman, Venkatesh Raman, S. Srinivasa Rao]
  note: Benoit, Demaine, Munro and Raman introduced the depth-first unary degree sequence at WADS 1999; the journal version with Raman and Rao appeared in Algorithmica in 2005, and Jansson, Sadakane and Sung added depth and lca.
prereqs: [ordinal-tree, parenthesis-matching, balanced-parentheses-representation]
see_also: [louds-tree, range-min-max-tree, louds-trie, preorder-traversal, unary-coding, cartesian-tree, range-minimum-query, succinct-data-structures]
sources:
  - paper: doi:10.1007/s00453-004-1146-6
    title: David Benoit, Erik D. Demaine, J. Ian Munro, Rajeev Raman, Venkatesh Raman and S. Srinivasa Rao, Representing trees of higher degree, Algorithmica 43(4), 2005, 275-292
    locator: the DFUDS encoding, the proof that it is balanced, and child(v, i), degree, parent and subtree size in O(1) time
  - paper: doi:10.1016/j.jcss.2011.09.002
    title: Jesper Jansson, Kunihiko Sadakane and Wing-Kin Sung, Ultra-succinct representation of ordered trees with applications, Journal of Computer and System Sciences 78(2), 2012, 619-631
    locator: the DFUDS formulas for depth, level ancestor and lca, and the compressed DFUDS by degree entropy
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 8, Section 8.3 (Depth-First Unary Degree Sequence)
---

DFUDS stores an [ordinal tree](/ordinal-tree/) of $n$ nodes as $2n$ parentheses: the nodes are listed in [preorder](/preorder-traversal/), each writes its degree in [unary](/unary-coding/) as that many `(` followed by one `)`, and one extra `(` goes in front. The result is a balanced sequence, and with [parenthesis matching](/parenthesis-matching/) and [rank and select](/rank-select-dictionary/) the $i$-th child, the degree, the parent, the rank among siblings and the subtree size all take $O(1)$ time on the [word RAM](/word-ram/), in $2n + o(n)$ bits. It combines the direct `child(v, i)` of [LOUDS](/louds-tree/) with the preorder numbering and contiguous subtrees of [BP](/balanced-parentheses-representation/). Benoit, Demaine, Munro and Raman introduced it in 1999 for trees of high degree, such as tries.

## In plain words

Walk the tree in the usual depth-first order: a node, then all of its first child's family, then its second child's family, and so on. For each node, write one opening bracket per child and then one closing bracket. Put one more opening bracket at the very start.

The brackets come out properly nested. Each opening bracket a node writes for a child is closed exactly where that child's family ends. So to jump to the third child of a node, find the matching close of the right opening bracket and step one place forward. A node's whole family sits in one stretch of the string, so its size is a subtraction.

## The abstract type

The structure stores a static [ordinal tree](/ordinal-tree/) and answers `child(v, i)`, `degree(v)`, `parent(v)`, `child_rank(v)`, `next_sibling(v)`, `is_leaf(v)`, `subtree_size(v)`, `preorder_rank(v)` and `node_at(k)`; with the Jansson-Sadakane-Sung formulas also `depth`, `level_ancestor` and `lca`. A node is the position where its code starts, and the root is at position 1.

## Representation

Let the nodes in preorder be $v_0, \ldots, v_{n-1}$ with degrees $d_0, \ldots, d_{n-1}$. The DFUDS sequence is

$$U = (\; (^{d_0} )\; (^{d_1} )\; \cdots\; (^{d_{n-1}} ),$$

of $1 + \sum_k (d_k + 1) = 2n$ symbols. Each code ends with one `)`, so the code of $v_k$ starts right after the $k$-th `)`: at $\text{select}_)(k) + 1$, with $\text{select}_)(0) = 0$. A rank and select index on `)` and a matching structure, such as the [range min-max tree](/range-min-max-tree/), sit on top.

The key invariant: the $i$-th `(` from the right in the code of $v$ matches the `)` that ends the subtree of the $i$-th child of $v$, that is, the `)` just before the code of the $(i+1)$-th child, or the end of the subtree of $v$ for the last child.

## Operations

```pseudo id=main
DEGREE(v)
L1  return SELECT)(RANK)(v) + 1) − v          ▷ '(' until the ')' that ends the code

CHILD(v, i)                                   ▷ 1 ≤ i ≤ DEGREE(v)
L2  if i > DEGREE(v) then return none
L3  e ← SELECT)(RANK)(v) + 1)                 ▷ the ')' that ends the code of v
L4  return FINDCLOSE(e − i) + 1

PARENT(v)
L5  if v = 1 then return none
L6  o ← FINDOPEN(v − 1)                       ▷ the '(' in the parent's code
L7  return SELECT)(RANK)(o)) + 1              ▷ the start of that code

CHILD-RANK(v)
L8  o ← FINDOPEN(v − 1)
L9  return SELECT)(RANK)(o) + 1) − o

SUBTREE-SIZE(v)
L10 end ← FWDSEARCH(v − 1, −1)
L11 return (end − v) / 2 + 1
```

Here $\text{rank}_)(v)$ counts the `)` before position $v$.

**Degree.** The code of $v$ is a run of `(` that starts at $v$ and ends at the next `)`.

**Child.** The `(` at $e - i$ is the $i$-th from the right. By the invariant it matches the `)` just before the code of the $i$-th child, so the child starts one position later. For $i = 1$, $e - 1$ matches $e$ itself, and the first child starts at $e + 1$, right after its parent, as preorder demands.

**Parent and child rank.** The `)` at $v - 1$ ends the code of the node before $v$ in preorder, which is the parent itself when $v$ is a first child. Its matching `(` lies in the code of the parent, and counting `)` before it tells which code that is. The distance from that `(` to the end of the code is the rank of $v$ among its siblings.

**Subtree size.** The `(` matched by the `)` at $v - 1$ is the one the parent wrote for $v$, and its match, $end = \text{fwdsearch}(v - 1, -1)$, is the `)` that ends the last code of the subtree of $v$. A subtree of $s$ nodes has codes with $s - 1$ `(` and $s$ `)` in all, so $end - v + 1 = 2s - 1$.

**Others.** `next_sibling(v)` is $\text{child}(\text{parent}(v), \text{child\_rank}(v) + 1)$, or directly $\text{fwdsearch}(v - 1, -1) + 1$ when $o = \text{findopen}(v - 1) > 1$ and $U[o - 1] = ($; the test $o > 1$ excludes the leading `(`. `is_leaf(v)` is $U[v] = )$. `preorder_rank(v)` is $\text{rank}_)(v)$, and `node_at(k)` is $\text{select}_)(k) + 1$.

## Example

The tree $A(B(E, F), C, D(G(H)))$ has preorder $A, B, E, F, C, D, G, H$ and degrees $3, 2, 0, 0, 0, 1, 1, 0$, so $U$ = `(((()(())))()())`.

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $U[i]$ | ( | ( | ( | ( | ) | ( | ( | ) | ) | ) | ) | ( | ) | ( | ) | ) |
| excess | 1 | 2 | 3 | 4 | 3 | 4 | 5 | 4 | 3 | 2 | 1 | 2 | 1 | 2 | 1 | 0 |
| code of | | $A$ | $A$ | $A$ | $A$ | $B$ | $B$ | $B$ | $E$ | $F$ | $C$ | $D$ | $D$ | $G$ | $G$ | $H$ |

The nodes start at $A = 1$, $B = 5$, $E = 8$, $F = 9$, $C = 10$, $D = 11$, $G = 13$, $H = 15$.

- DEGREE$(A)$: $\text{rank}_)(1) = 0$, the first `)` is at 4, so $4 - 1 = 3$.
- CHILD$(A, 2)$: $e = 4$, and the `(` at $4 - 2 = 2$ has excess 3, so its match is the first later position with excess 2, which is 9. The child starts at 10, node $C$. CHILD$(A, 3)$: $\text{findclose}(1) = 10$, so $D$ at 11.
- PARENT$(F = 9)$: $\text{findopen}(8) = 5$, and $\text{rank}_)(5) = 1$, so the parent's code starts at $\text{select}_)(1) + 1 = 5$, node $B$. CHILD-RANK$(F)$: the code of $B$ ends at $\text{select}_)(2) = 7$, and $7 - 5 = 2$.
- SUBTREE-SIZE$(D = 11)$: the excess at 10 is 1, and the first later position with excess 0 is 15, so $(15 - 11)/2 + 1 = 3$.
- `preorder_rank`$(C = 10)$ is $\text{rank}_)(10) = 4$.

## Correctness

The proof first shows that $U$ is balanced and that its matching pairs follow the tree: by induction on the height, the part of $U$ formed by the codes of the subtree of $v$, preceded by one extra `(`, is balanced, and that extra `(` is the one the parent wrote for $v$. From this the invariant follows, and each formula is a count of `(` or `)`. The full argument is in [the proof of correctness](proofs/correctness.md).

## Complexity

| operation | time with the full index | time in this page's implementation |
|---|---|---|
| build | $O(n)$ | $O(n)$ |
| degree, is_leaf, preorder_rank, node_at | $O(1)$ | $O(1)$ |
| child, parent, child_rank, next_sibling, subtree_size | $O(1)$ | $O(n)$ matching scans |
| depth, level_ancestor, lca | $O(1)$ (Jansson, Sadakane and Sung) | not implemented |

**Space.** $U$ has $2n$ bits, and the rank, select and matching indexes add $o(n)$; the minimum for ordinal trees is $2n - \Theta(\lg n)$ bits.

## Variants

- **Ultra-succinct DFUDS.** Jansson, Sadakane and Sung code each unary degree by its frequency and store the tree in $n H^* + o(n)$ bits, where $H^*$ is the entropy of the degree distribution, about $n$ bits for a binary tree whose nodes have 0 or 2 children.
- **Cardinal trees and tries.** Benoit et al. add, for each node, the set of labels of its children in a rank/select structure, giving the child with a given label in $O(1)$ time; this is a DFUDS trie, an alternative to the [LOUDS trie](/louds-trie/).
- **RMQ in $2n + o(n)$ bits.** Fischer and Heun store the 2d-min-heap of an array, a tree closely related to its [Cartesian tree](/cartesian-tree/), in DFUDS, and [range minimum queries](/range-minimum-query/) become excess queries on it.
- **Dynamic DFUDS.** Over a dynamic parenthesis sequence with a [range min-max tree](/range-min-max-tree/), insertion of a leaf inserts one `(` in the parent's code and one `)` for the leaf.

## When to use it

Use DFUDS when a static tree is navigated by child index and also needs preorder numbers or subtree sizes, for example tries over large alphabets stored with their labels in preorder, and succinct RMQ. [BP](/balanced-parentheses-representation/) is simpler for depth and LCA, and [LOUDS](/louds-tree/) is simpler when only parents and children matter and level order is fine.

## Pitfalls

- **The leading parenthesis.** Without it $U$ is not balanced and the formulas for the root and its children fail.
- **Children from the right.** The first child uses the `(` closest to the `)` of the code, not the first `(` of the code. Reversing this gives the children in reverse order.
- **The convention $\text{select}_)(0) = 0$.** PARENT of a child of the root asks for $\text{select}_)(0)$; it must return 0 so that the root starts at 1.
- **Depth is not the excess.** Unlike BP, the excess at a node in DFUDS is not its depth; depth needs the Jansson-Sadakane-Sung formula with range minima.
- **Satellite data in preorder.** Nodes are named by positions; store per-node data in preorder and convert with `preorder_rank`.

## Implementations

## History

Benoit, Demaine, Munro and Raman introduced the depth-first unary degree sequence at WADS 1999 to represent trees of high degree and cardinal trees in near-optimal space with constant-time child by index or label. The journal version, with Raman and Rao, appeared in Algorithmica in 2005. Jansson, Sadakane and Sung (SODA 2007, JCSS 2012) added depth, level ancestor and lowest common ancestor and the entropy-compressed variant, and Navarro and Sadakane's range min-max tree supports its matching queries.

## References
