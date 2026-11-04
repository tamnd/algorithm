---
tag: Q1HEHJ
kind: algorithm
slug: suffix-tree-from-suffix-array
name: Suffix tree from suffix array
aliases:
- Abouelhoda-Kurtz-Ohlebusch construction
area: data-structures/string-structures
level: advanced
summary: Build the suffix tree from the suffix array and LCP array in linear time.
solves: [suffix-tree-construction]
model: word-ram
complexity:
  vars: {n: the length of the text, including the end marker}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
history:
  year: 2001
  people: [Toru Kasai, Gunho Lee, Hiroki Arimura, Setsuo Arikawa, Kunsoo Park]
  note: Kasai and coauthors simulated the bottom-up traversal of the suffix tree with the suffix array, the LCP array and a stack; Abouelhoda, Kurtz and Ohlebusch made the lcp-interval tree explicit in 2004.
prereqs: [suffix-tree, suffix-array, lcp-array, stack]
see_also: [suffix-tree-construction, lcp-interval-tree, enhanced-suffix-array, kasai-algorithm, cartesian-tree, dc3-algorithm, ukkonen-algorithm, farach-algorithm]
sources:
  - paper: Mohamed Ibrahim Abouelhoda, Stefan Kurtz and Enno Ohlebusch, Replacing suffix trees with enhanced suffix arrays, Journal of Discrete Algorithms 2(1), 2004, doi:10.1016/S1570-8667(03)00065-0
    locator: pages 53 to 86, lcp-intervals, the lcp-interval tree as the internal nodes of the suffix tree, and its bottom-up traversal with a stack
  - paper: Toru Kasai, Gunho Lee, Hiroki Arimura, Setsuo Arikawa and Kunsoo Park, Linear-time longest-common-prefix computation in suffix arrays and its applications, Combinatorial Pattern Matching (CPM 2001), LNCS 2089, doi:10.1007/3-540-48194-X_17
    locator: pages 181 to 192, the linear LCP computation and the stack-based bottom-up traversal of the suffix tree
---

A [suffix tree](/suffix-tree/) can be built from the [suffix array](/suffix-array/) and the [LCP array](/lcp-array/) of the text in one left-to-right scan with a [stack](/stack/). The leaves of the suffix tree, read from left to right, are the suffixes in the order of the suffix array, and the string depth of the lowest common ancestor of two adjacent leaves is their LCP value. So the scan keeps the rightmost path of the tree built so far on the stack, pops the nodes deeper than the next LCP value, splits an edge if needed, and hangs the next leaf. With a linear suffix array construction such as the [DC3 algorithm](/dc3-algorithm/) and Kasai's LCP algorithm, this gives a linear-time suffix tree construction for integer alphabets that is simpler than [Farach's algorithm](/farach-algorithm/). The internal nodes it creates are the lcp-intervals of Abouelhoda, Kurtz and Ohlebusch, which form the [lcp-interval tree](/lcp-interval-tree/).

## In plain words

Sort all endings of the text. Neighbors in this sorted list share a start, and the LCP array says how many letters they share. In the suffix tree, two neighbors are leaves that part ways at a branching point exactly that many letters deep.

So build the tree from left to right, one ending at a time. Keep the path from the root to the newest leaf on a stack. For the next ending, go up the path until you are no deeper than the shared length. If the stack has a node at exactly that depth, the new leaf hangs there. If not, the edge you just climbed is cut at that depth, and a new branching node is put there. Each node goes on the stack once and off once, so the work is linear.

## The problem

Given a text $t$ of length $n$ that ends with a unique end marker, its suffix array $SA$ and its LCP array, with $LCP[i]$ the length of the longest common prefix of the suffixes $SA[i-1]$ and $SA[i]$ and $LCP[0] = 0$, build the suffix tree of $t$ ([suffix tree construction](/suffix-tree-construction/)): the compacted trie of its suffixes, with one leaf per suffix, every internal node other than the root branching, children in increasing order of their first symbol, and edges labeled by pairs of positions into $t$.

## The algorithm

Each node $x$ stores its string depth $depth(x)$, the start of one suffix below it, and its children in order. The edge into $x$ from its parent $p$ is labeled $t[start(x) + depth(p) \ldots start(x) + depth(x) - 1]$.

```pseudo id=main
SUFFIX-TREE-FROM-SA(t, SA, LCP)
L1  root ← a node with depth 0; stack ← [root]
L2  for i ← 0 to n − 1: h ← LCP[i]; last ← NIL
L3      while depth(top) > h: last ← pop
L4      if depth(top) < h: u ← a new node with depth h and start(last); replace last, the last child of top, by u; make last the child of u; push u
L5      v ← a new leaf for the suffix SA[i], with depth n − SA[i]; append v to the children of top; push v
L6  return root
```

**The stack.** Before step $i$, the stack holds the path from the root to the leaf of $SA[i-1]$, the rightmost path of the tree of the first $i$ suffixes. The new leaf must hang below the node of depth $h$ on this path, which is the longest common prefix of the new suffix with the previous one.

**Line L3** pops the nodes deeper than $h$; $last$ is the last one popped, the child of the new top on the path. **Line L4** handles the case where the path has no node at depth $h$: the point at depth $h$ lies inside the edge from $top$ to $last$, so the edge is split there by a new node $u$, which takes the place of $last$. **Line L5** adds the leaf. In line L4, $last$ is never NIL: the previous leaf has depth $n - SA[i-1] > h$, because the end marker makes no suffix a prefix of another, so at least one node is popped.

## Example

For banana with the end marker $ smaller than every letter, $t = $ banana$ and $n = 7$:

| i | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| SA[i] | 6 | 5 | 3 | 1 | 0 | 4 | 2 |
| suffix | $ | a$ | ana$ | anana$ | banana$ | na$ | nana$ |
| LCP[i] | 0 | 0 | 1 | 3 | 0 | 0 | 2 |

| i | h | popped | split at depth | leaf added (depth) | stack after, by depth |
|---|---|---|---|---|---|
| 0 | 0 | none | none | 6 (1) under root | 0, 1 |
| 1 | 0 | leaf 6 | none | 5 (2) under root | 0, 2 |
| 2 | 1 | leaf 5 | 1, node a, above leaf 5 | 3 (4) under a | 0, 1, 4 |
| 3 | 3 | leaf 3 | 3, node ana, above leaf 3 | 1 (6) under ana | 0, 1, 3, 6 |
| 4 | 0 | leaf 1, ana, a | none | 0 (7) under root | 0, 7 |
| 5 | 0 | leaf 0 | none | 4 (3) under root | 0, 3 |
| 6 | 2 | leaf 4 | 2, node na, above leaf 4 | 2 (5) under na | 0, 2, 5 |

The result has 7 leaves and the internal nodes a, ana, na and the root. The root's children are, in order, the leaf of suffix 6 (edge $), the node a, the leaf of suffix 0 (edge banana$) and the node na. The node a has the leaf of suffix 5 (edge $) and the node ana (edge na); the node ana has the leaves of suffixes 3 (edge $) and 1 (edge na$); the node na has the leaves of suffixes 4 (edge $) and 2 (edge na$). The splits happen exactly where the LCP value is larger than the depth of every node on the stack: at $i = 2$, 3 and 6.

## Correctness

The tree of the first $i$ suffixes in suffix array order is the compacted trie of these suffixes, and its rightmost path ends at the leaf of $SA[i-1]$. The new suffix shares exactly $LCP[i]$ symbols with $SA[i-1]$ and at most that many with any earlier suffix, so its branching point is the point at depth $LCP[i]$ on the rightmost path, and the new leaf becomes the rightmost child there. Lines L3 and L4 find or create the node at that point. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Each of the $n$ leaves and at most $n - 1$ internal nodes is pushed once and popped at most once, so lines L3 to L5 take $O(n)$ time in total, and the scan is $\Theta(n)$. The tree has at most $2n - 1$ nodes; with the children stored as lists in order, the extra space is $\Theta(n)$ words besides the input arrays. The suffix array and the LCP array can be computed in $O(n)$ time for integer alphabets, so the whole construction is linear, independently of the alphabet size, as long as the children lists are not indexed by symbols.

## Properties

- **Ordered output.** Children are created in the lexicographic order of their first symbols, because the leaves arrive in suffix array order. No sorting of children is needed, which is what makes the construction independent of the alphabet.
- **Not online.** The whole suffix array is needed, so the method builds the tree of a fixed text, unlike [Ukkonen's algorithm](/ukkonen-algorithm/).
- **No suffix links.** The scan does not produce suffix links. They can be added afterward in linear time, for example from the inverse suffix array and range minimum queries.

## Variants and improvements

- **Virtual traversal.** Instead of building nodes, the scan can report each internal node, as an lcp-interval $[i, j]$ with its depth, when it is popped. This bottom-up traversal of the suffix tree is the way Kasai et al. and Abouelhoda, Kurtz and Ohlebusch solve suffix tree problems directly on arrays, in the [enhanced suffix array](/enhanced-suffix-array/).
- **Child table.** Abouelhoda, Kurtz and Ohlebusch store the lcp-interval tree as a child table of $n$ integers, which allows top-down searches on the suffix array with the cost of a suffix tree.
- **Cartesian tree view.** The internal nodes are the nodes of the [Cartesian tree](/cartesian-tree/) of the LCP array, with runs of equal minimum values merged into one node; the stack scan is the standard linear construction of a Cartesian tree.
- **Several texts.** For a [generalized suffix tree](/generalized-suffix-tree/), concatenate the texts with distinct end markers; the same scan applies.

## When to use it

Use this construction when the suffix array is already available, or when a linear-time suffix tree is needed for a large integer alphabet, where Ukkonen's or McCreight's algorithm would pay for searching the children by symbol. It is also a common route in practice, because suffix array libraries are fast and the scan is short. If only a bottom-up traversal is needed, skip the tree and use the virtual traversal on the arrays.

## Pitfalls

- **No end marker.** Without a unique end marker, a suffix can be a prefix of another, its leaf would sit inside an edge, and line L4 could find $last = $ NIL. Append a symbol that is smaller than or different from all others.
- **The LCP convention.** $LCP[i]$ must compare $SA[i-1]$ with $SA[i]$, not $SA[i]$ with $SA[i+1]$; mixing the two shifts every branching point by one leaf.
- **Replacing the wrong child.** The split of line L4 must replace the last child of $top$, which is $last$; looking up the child by its first symbol also works but costs time per symbol.
- **Edge labels as strings.** Storing labels as copied strings makes the tree quadratic in size. Store depths and a start position, as here.

## Implementations

The Python module builds the suffix tree of a text with the sentinel character 0 appended. It computes a simple suffix array, the LCP array by Kasai's algorithm, and then runs lines L1 to L6. Nodes store their depth, the start of a suffix below them and an ordered list of children. The tests replay the banana example and compare the internal nodes, for 600 random texts, with the right-branching substrings computed directly, checking the leaves and the order of the children each time.

## History

Manber and Myers introduced suffix arrays in 1990 as a space-saving alternative to suffix trees. Kasai, Lee, Arimura, Arikawa and Park (2001) gave the linear LCP algorithm and used it with a stack to simulate the bottom-up traversal of the suffix tree. Abouelhoda, Kurtz and Ohlebusch (2004) defined lcp-intervals and the enhanced suffix array, which replaces the suffix tree in many applications, and the conversion between the two by the same scan. With the linear suffix array constructions of 2003, this became a standard way to build suffix trees in linear time for integer alphabets.

## References
