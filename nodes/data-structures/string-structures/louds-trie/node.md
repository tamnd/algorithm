---
tag: C20ZQR
kind: data-structure
slug: louds-trie
name: LOUDS trie
aliases:
- level-order unary degree sequence
area: data-structures/string-structures
level: research
summary: Succinct trie encoding the tree shape in breadth-first order as a bit string with rank and select.
implements: [string-symbol-table]
model: word-ram
complexity:
  vars: {n: the number of trie nodes, m: the length of the key, σ: the size of the alphabet}
  time: {worst: O(m log σ)}
  space: {extra: O(n log σ)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [trie, louds-tree, rank, bit-vector]
see_also: [louds-tree, trie, succinct-data-structures, rank-select-dictionary, dfuds, balanced-parentheses, ordinal-tree, double-array-trie]
sources:
  - paper: Guy Jacobson, Space-efficient static trees and graphs, 30th Annual Symposium on Foundations of Computer Science (FOCS 1989), doi:10.1109/SFCS.1989.63533
    locator: pages 549 to 554, the level-order unary degree sequence of an ordinal tree in 2n + 1 bits, and navigation to the parent and children with rank and select
  - paper: O'Neil Delpratt, Naila Rahman and Rajeev Raman, Engineering the LOUDS succinct tree representation, Experimental Algorithms (WEA 2006), LNCS 4007, doi:10.1007/11764298_12
    locator: pages 134 to 145, the node numbering and the formulas for parent and child with rank and select, and an experimental comparison with other succinct trees
  - book: Gonzalo Navarro, Compact Data Structures, a practical approach, Cambridge University Press, 2016, isbn 9781107152380
    locator: Chapter 8, the LOUDS representation of ordinal trees and its use for tries with labels in level order
  - paper: Huanchen Zhang, Hyeontaek Lim, Viktor Leis, David G. Andersen, Michael Kaminsky, Kimberly Keeton and Andrew Pavlo, SuRF, practical range query filtering with fast succinct tries, SIGMOD 2018, doi:10.1145/3183713.3196931
    locator: pages 323 to 336, the fast succinct trie with LOUDS-Dense for the upper levels and LOUDS-Sparse for the lower levels
---

A LOUDS trie is a static [trie](/trie/) stored as a bit string and two arrays, with no pointers. The shape of the trie is written in breadth-first order, each node as its number of children in unary, in $2n + 1$ bits for $n$ nodes, the encoding of the [LOUDS tree](/louds-tree/) due to Jacobson (1989). The edge symbols go in an array in the same order, and a second bit array marks the nodes that end a key. With [rank](/rank/) and select on the bit string, moving from a node to its children or to its parent takes constant time, so a lookup of a key of length $m$ takes $O(m \log \sigma)$ time with a binary search among the children, while the trie takes about $n (2 + \log \sigma + 1)$ bits plus the $o(n)$ bits of the rank and select index. This page covers the trie built on the encoding; the encoding itself, for general ordinal trees, is the subject of the page of the LOUDS tree.

## In plain words

A pointer trie spends a pointer of 64 bits on every edge, far more than the symbol on the edge. For a large static dictionary, such as the words of a spell checker or the keys of a filter, these pointers are most of the memory.

LOUDS throws the pointers away. Number the nodes level by level, left to right. Then the children of a node are a run of consecutive numbers, and it is enough to know where each run starts. Writing each node's child count in unary, as that many 1s and a 0, gives a bit string from which the runs can be computed by counting bits. Counting bits up to a position (rank) and finding the position of the $j$-th bit (select) are fast with a small index. The edge symbols are stored in the same node order, one per node.

## The abstract type

The LOUDS trie implements a static [string symbol table](/string-symbol-table/), or a set of strings: membership, listing the keys with a given prefix, and, with an extra array of values in node order, lookup of a value. The set is built once from the keys; inserting a key later means rebuilding.

## Representation

Number the nodes $0, 1, \ldots, n - 1$ in breadth-first order, with the children of each node in increasing order of their symbols; node 0 is the root.

- $B$, the LOUDS bit string: $10$, followed by $1^{d} 0$ for each node in order, where $d$ is its number of children. It has $n$ ones and $n + 1$ zeros.
- $L[y]$, the symbol on the edge into node $y$, for $y \ge 1$.
- $E[y]$, one bit, set if the string of node $y$ is a key.
- A rank and select index on $B$: $rank_1(i)$ counts the 1s in $B[0 \ldots i - 1]$, $rank_0(i) = i - rank_1(i)$, and $select_b(j)$ is the position of the $j$-th bit equal to $b$, counting from 1.

**Invariant.** (L1) The $(x + 1)$-th 1 of $B$ stands for node $x$; the leading 1 stands for the root, and each other 1 for a child in the group of its parent. (L2) The $(x + 1)$-th 0 of $B$ ends the group of node $x$, so the group of $x$ lies between the $(x + 1)$-th and the $(x + 2)$-th 0. (L3) The labels in each group are distinct and increasing. (L4) Every leaf other than the root ends a key.

(L1) and (L2) hold because breadth-first order lists the groups in the order of their parents and the children in the order of their numbers: the 1s after the leading one are the nodes $1, 2, \ldots$ in order.

## Operations

```pseudo id=main
CHILDREN(x)                                ▷ the children of x are the nodes first … last − 1
L1  a ← select_0(x + 1) + 1;  e ← select_0(x + 2)
L2  first ← rank_1(a);  last ← first + (e − a)
CHILD(x, c)
L3  binary search c in L[first … last − 1];  return its node, or NIL
PARENT(x)
L4  p ← select_1(x + 1);  return rank_0(p) − 1
CONTAINS(s)
L5  x ← 0;  for each symbol c of s:  x ← CHILD(x, c);  if x = NIL, return false
L6  return E[x]
BUILD(keys)
L7  build a pointer trie; walk it in breadth-first order, writing 1^d 0, the child labels and the key bits
```

In CHILDREN, the group of $x$ is $B[a \ldots e - 1]$, all 1s, by (L2). The 1s before position $a$ are the root and the children of nodes $0, \ldots, x - 1$, so by (L1) the first 1 of the group is node $rank_1(a)$. In PARENT, the 1 of node $x$ lies in the group of its parent $q$, which follows the $(q + 1)$-th 0, so the number of 0s before it is $q + 1$.

## Example

Take the keys i, in, inn, tea, ten and to. The breadth-first numbering is:

| node | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| string | ε | i | t | in | te | to | inn | tea | ten |
| children | 2 | 1 | 2 | 1 | 2 | 0 | 0 | 0 | 0 |
| L | | i | t | n | e | o | n | a | n |
| E | 0 | 1 | 0 | 1 | 0 | 1 | 1 | 1 | 1 |

So $B = 10\ 110\ 10\ 110\ 10\ 110\ 0\ 0\ 0\ 0$, written without spaces 1011010110101100000, 19 bits for 9 nodes. Its 0s are at positions 1, 4, 6, 9, 11, 15, 16, 17 and 18.

CHILD(2, o), the child of t by o: the third 0 is at position 6 and the fourth at 9, so the group is $B[7 \ldots 8]$ and $a = 7$. There are 4 ones before position 7, so the children are nodes 4 and 5, with labels e and o, and the answer is node 5, the key to. PARENT(7): the eighth 1 is at position 12, and there are 5 zeros before it, so the parent is node 4, te. CONTAINS(te) reaches node 4 and returns $E[4] = 0$.

## Correctness

(L1) and (L2) follow from breadth-first order, and they give the formulas of CHILDREN and PARENT; (L3) makes the binary search of CHILD correct, and then CONTAINS follows the unique path of $s$ as in any trie. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

With a rank and select index of $o(n)$ bits that answers in $O(1)$ time, CHILDREN and PARENT take $O(1)$ time, CHILD takes $O(\log \sigma)$ for the binary search among at most $\sigma$ labels, and CONTAINS takes $O(m \log \sigma)$. Listing the $k$ keys below a node takes time proportional to the size of the subtree.

The space is $2n + 1$ bits for $B$, $n \lceil \log_2 \sigma \rceil$ bits for $L$, $n$ bits for $E$, and $o(n)$ bits for the index. A pointer trie with an array of children takes $\Theta(n \sigma)$ words; with sorted child lists, $\Theta(n)$ words.

The Python implementation answers rank in $O(64)$ steps and select by a binary search over block counts followed by a scan, which is enough to test the layout but not a constant-time index.

## Variants

- **LOUDS tree.** The encoding without labels, for ordinal trees in general, with the same parent and child formulas; see the [LOUDS tree](/louds-tree/).
- **DFUDS and balanced parentheses.** Other succinct tree encodings support subtree size, depth and level-ancestor queries that LOUDS lacks; see [DFUDS](/dfuds/) and [balanced parentheses](/balanced-parentheses/). LOUDS is the simplest and is fast for walking down from the root, which is what a trie lookup needs.
- **LOUDS-Dense and LOUDS-Sparse.** SuRF (Zhang et al. 2018) encodes the upper levels of a trie with one bitmap of $\sigma$ bits per node, for speed, and the lower levels with the labels-and-bits layout above, for space.
- **Path compression.** Chains of single-child nodes can be cut and their strings stored apart, as in a [radix tree](/radix-tree/), which reduces $n$ for sparse key sets.

## When to use it

Use a LOUDS trie for a large static set of strings that must stay in memory, such as a dictionary for an input method, a spell checker or the keys of a range filter, where a pointer trie would be several times larger. If the set changes often, use a [double-array trie](/double-array-trie/), an [adaptive radix tree](/adaptive-radix-tree/), or a [hash table](/hash-table/) instead.

## Pitfalls

- **The leading 10.** Without the super-root bits, the formulas shift by one and the root has no 1 of its own; keep the convention consistent.
- **Counting from 0 or 1.** select counts from 1 and node numbers from 0 in the formulas above; mixing the two gives off-by-one errors in every navigation.
- **Child order.** The binary search of CHILD needs the children of each node in symbol order, which the breadth-first walk must produce.
- **Rank cost.** A rank computed by scanning the bit string makes every step linear; the index is what makes LOUDS fast.

## Implementations

The Python module has a bit vector with block counts for rank and select, and a class that builds a pointer trie, walks it in breadth-first order to write $B$, $L$ and $E$, and then drops it. Navigation follows the formulas of the pseudocode. check_invariant verifies the length of $B$, the parent of every child and the sorted labels. The tests replay the example, check rank and select against a scan on 200 random bit strings, and compare 600 random key sets with a Python set, including prefix listing.

## History

Jacobson (1989) introduced the level-order unary degree sequence as a succinct encoding of ordinal trees with navigation by rank and select. Delpratt, Rahman and Raman (2006) engineered it and compared it with other succinct trees. LOUDS tries are used in libraries of static dictionaries and in SuRF, the range filter of Zhang et al. (2018), and Navarro's book on compact data structures covers the encoding and its use for tries.

## References
