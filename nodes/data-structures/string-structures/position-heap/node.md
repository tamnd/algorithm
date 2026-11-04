---
tag: PDF2MC
kind: data-structure
slug: position-heap
name: Position heap
area: data-structures/string-structures
level: research
summary: Trie over the reversed prefixes of a text that indexes the position of each pattern occurrence.
implements: [full-text-index]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, z: the number of occurrences}
  time: {worst: O(m^2 + z)}
  space: {extra: O(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [trie, full-text-index, string-matching]
see_also: [suffix-tree, suffix-trie, suffix-array, heap, online-algorithm, lz78-parsing, trie, full-text-index]
sources:
  - paper: Andrzej Ehrenfeucht, Ross M. McConnell, Nissa Osheim and Sung-Whan Woo, Position heaps, a simple and dynamic text indexing data structure, Journal of Discrete Algorithms 9(1), 2011, doi:10.1016/j.jda.2010.12.001
    locator: pages 100 to 121, the definition of the position heap by inserting the suffixes from the shortest, the search that checks the positions on the path and reports the subtree, the linear-time construction, and the maximal-reach pointers for linear-time search
  - paper: Gregory Kucherov, On-line construction of position heaps, Journal of Discrete Algorithms 20, 2013, doi:10.1016/j.jda.2012.08.002
    locator: pages 3 to 11, the position heap built left to right with suffixes inserted from the longest, and its on-line construction in linear time
  - paper: E. G. Coffman Jr. and J. Eve, File structures using hashing functions, Communications of the ACM 13(7), 1970, doi:10.1145/362686.362693
    locator: pages 427 to 432, the sequence hash tree, the trie in which each new string adds one node, which the position heap adapts to text indexing
---

A position heap is a [full-text index](/full-text-index/) with exactly one trie node per text position. The suffixes of the text are inserted one at a time, from the shortest to the longest, and each one adds only the shortest prefix of it that is not yet in the trie, a single new node, labeled with the starting position of the suffix. Seen from the reversed text, these suffixes are its reversed prefixes, and the structure grows when a symbol is appended to the reversed text. Ehrenfeucht, McConnell, Osheim and Woo (2011) introduced it as a simpler alternative to the [suffix tree](/suffix-tree/): its nodes are not compacted, it has $n + 1$ nodes, and a search for a pattern of length $m$ takes $O(m^2 + z)$ time for $z$ occurrences, or $O(m + z)$ with an extra pointer per node.

## In plain words

A [suffix trie](/suffix-trie/) stores every suffix of the text in full, which can take quadratic space. A position heap stores only a piece of each suffix: the shortest beginning of it that is new. So it has one node per position and stays small.

To find a pattern, walk down the trie along it. Every position stored below the end of the walk starts with the pattern, so these are reported without any check. The positions stored on the way down are the only other places where the pattern can start, because their stored piece was shorter than the pattern. Each of these is checked against the text directly.

## The abstract type

The position heap implements a static [full-text index](/full-text-index/): preprocess a text $T$ of length $n$, then report all positions $i$ where a pattern $P$ occurs, $T[i \ldots i + m - 1] = P$. The version on this page also supports prepending a symbol to $T$, which inserts one new suffix.

## Representation

The heap is a trie: each node $x$ spells a string $str(x)$, the symbols on the path from the root, and the children of a node have distinct symbols. Each node other than the root holds a position $pos(x)$ of $T$. Positions are numbered from the left, $0 \le i < n$; the implementation stores the suffix length $n - i$ instead, so that prepending does not renumber the nodes.

**Invariant.**

- (H1) The positions held are $0, 1, \ldots, n - 1$, each once, so there are $n + 1$ nodes with the root.
- (H2) For each node $x$ other than the root, $str(x)$ is a prefix of the suffix $T[pos(x) \ldots]$.
- (H3) Heap order: if $y$ is a child of $x$ and $x$ is not the root, then $pos(y) < pos(x)$.

(H3) gives the name: along each downward path the positions decrease, like the keys of a [heap](/heap/). It holds because the suffixes are inserted from position $n - 1$ down to $0$, and a node is always added below older nodes.

## Operations

```pseudo id=main
PREPEND(c)                                       ▷ T ← c · T; the new suffix starts at 0
L1  x ← root;  k ← 0
L2  while x has a child y by the symbol T[k]:  x ← y;  k ← k + 1
L3  add a child y of x by T[k], with pos(y) ← 0     ▷ the old positions shift by one

SEARCH(P)                                        ▷ m = |P| ≥ 1
L4  x ← root;  k ← 0;  walk down along P while a child exists, k ← the depth reached
L5      for each node z passed at depth < m:  if T[pos(z) …] starts with P, report pos(z)
L6  if k = m:  report pos(y) for every node y in the subtree of x
L7  return the reported positions
```

Building the heap of $T$ is $n$ calls of PREPEND, with the symbols of $T$ from the last to the first. The walk of line L2 always stops before the end of the new suffix: the suffix itself cannot be a node already, since every older node spells a prefix of a shorter suffix.

## Example

Take $T = $ abaabab, so $n = 7$. Inserting the suffixes from position 6 down to 0 adds these nodes:

| position | suffix | node added |
|---|---|---|
| 6 | b | b |
| 5 | ab | a |
| 4 | bab | ba |
| 3 | abab | ab |
| 2 | aabab | aa |
| 1 | baabab | baa |
| 0 | abaabab | aba |

The root has children a (position 5) and b (position 6). Below a are aa (2) and ab (3), and below ab is aba (0). Below b is ba (4), and below ba is baa (1). The positions decrease downward, as (H3) says.

SEARCH(ab) walks root, a, ab and reaches depth 2 = m. The node a, passed at depth 1, is checked: $T[5 \ldots 6] = $ ab, so 5 is reported. The subtree of ab holds positions 3 and 0, reported without checks. The answer is $\{0, 3, 5\}$. SEARCH(abab) walks root, a, ab, aba and stops at depth 3, since aba has no child b. It checks the three positions on the path, 5, 3 and 0, and only $T[3 \ldots 6] = $ abab matches, so the answer is $\{3\}$.

## Correctness

Every position $i$ has its node $x_i$, and $str(x_i)$ and $P$ are both prefixes of the suffix at $i$ when $P$ occurs there, so one of them is a prefix of the other. If $str(x_i)$ is a proper prefix of $P$, then $x_i$ lies on the walk along $P$ above depth $m$ and line L5 checks it; otherwise $x_i$ is in the subtree of the node of $P$, and every position there is an occurrence by (H2). The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

A search walks at most $m$ nodes. It checks at most $m - 1$ positions on the path, each by a comparison of at most $m$ symbols, and reports the subtree in time proportional to its size, all of which are occurrences. So the time is $O(m^2 + z)$. The heap has $n + 1$ nodes, so the space is $O(n)$ words.

A call of PREPEND takes time proportional to the depth of the new node. The depth is not bounded by a constant: for $T = a^n$ the heap is a path of depth $n$, and building it naively takes $\Theta(n^2)$ time. Ehrenfeucht et al. give a linear-time construction, and Kucherov (2013) an on-line one.

## Variants

- **Maximal-reach pointers.** Ehrenfeucht et al. add to each node a pointer to the deepest node whose string is a prefix of the suffix at its position. With these, the checks of line L5 are replaced by pointer comparisons, and the search takes $O(m + z)$ time.
- **Left-to-right construction.** Kucherov (2013) defines the heap with the suffixes inserted from the longest to the shortest, which suits a text that grows at its right end, and builds it on-line in linear time.
- **Sequence hash trees.** Coffman and Eve (1970) used the same rule, each new string adds one node, for a hashing file structure; the position heap applies it to the suffixes of a text.
- **Suffix trees and arrays.** A [suffix tree](/suffix-tree/) answers a search in $O(m + z)$ time without the extra pointers, and a [suffix array](/suffix-array/) in $O(m \log n + z)$; both need a more involved construction.

## When to use it

Use a position heap when you want a simple full-text index with one node per position and an easy update at one end of the text, and the patterns are short, so the $m^2$ term is small. For long patterns, or when the alphabet is large and compact nodes matter, a suffix tree or a [compressed index](/fm-index/) is the usual choice.

## Pitfalls

- **Checking the path.** The positions on the path above depth $m$ are candidates, not answers; reporting them without the check of line L5 gives false occurrences.
- **The last node of a failed walk.** When the walk stops at depth $k < m$, the node at depth $k$ is on the path and must be checked too.
- **Positions shift on prepend.** Storing positions from the left would renumber every node when a symbol is prepended; store the suffix length, or the position from the right end.
- **Depth.** The heap can be as deep as the text, so traversals should use an explicit stack.

## Implementations

The Python class keeps the reversed text, a child map per node, and the suffix length held by each node. PREPEND walks from the root and adds one node, and SEARCH checks the path and collects the subtree with an explicit stack. check_invariant verifies (H1) to (H3). The tests replay the example, a unary text whose heap is a path, an on-line build of mississippi, and 600 random texts against a direct scan.

## History

Coffman and Eve (1970) introduced sequence hash trees for file structures. Ehrenfeucht, McConnell, Osheim and Woo (2011) adapted them to text indexing as position heaps, with a linear-time construction, the maximal-reach pointers and support for updates at the front of the text. Kucherov (2013) gave the on-line left-to-right construction.

## References
