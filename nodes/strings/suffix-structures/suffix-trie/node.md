---
tag: J5APVR
kind: data-structure
slug: suffix-trie
name: Suffix trie
aliases:
- naive suffix tree
area: strings/suffix-structures
level: intro
summary: A trie holding all suffixes of a string; quadratic in size, so rarely used directly.
implements: [full-text-index]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, occ: the number of occurrences}
  time: {worst: O(m)}
  space: {extra: O(n^2)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [trie, suffix]
see_also: [suffix-tree, suffix-automaton, suffix-array, sentinel-character, suffix-link, ukkonen-algorithm, distinct-substrings-counting, count-distinct-substrings]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 5, Introduction to suffix trees (the keyword tree of all suffixes and its compaction)
  - paper: doi:10.1007/BF01206331
    title: Esko Ukkonen, On-line construction of suffix trees, Algorithmica 14(3), 1995
    locator: pages 249 to 260; Section 2 (on-line construction of suffix tries with suffix links, in time proportional to the size of the trie)
  - book: isbn:9780521848992
    title: Maxime Crochemore, Christophe Hancart and Thierry Lecroq, Algorithms on Strings, Cambridge University Press, 2007
    locator: Chapter 5, Structures for indexes (the suffix trie and its compact form)
---

A suffix trie is the [trie](/trie/) of all [suffixes](/suffix/) of a string: each path from the root spells a substring, and each substring is spelled by exactly one path. It answers "is $P$ a substring?" in $\Theta(m)$ time for a pattern of length $m$, whatever the text length $n$, and it counts and lists the occurrences of $P$ from the node that the walk reaches. Its weakness is size: it has one node for each distinct substring, which is $\Theta(n^2)$ in the worst case even over two letters. The [suffix tree](/suffix-tree/) compacts its chains of one-child nodes to reach $\Theta(n)$ size, and the [suffix automaton](/suffix-automaton/) merges its equivalent nodes.

## In plain words

Take a word and write down all its endings: for "abab" these are "abab", "bab", "ab" and "b". Put all of them into a trie, the tree in which each edge carries one letter and words with the same start share a path.

Every piece of the word is the start of some ending. So every piece of the word is a path from the top of the trie, and a path exists only for a piece of the word. To test whether a pattern occurs in the text, follow its letters from the top. If you can follow all of them, it occurs. The endings that pass below the node where you stop tell you where it occurs.

The cost is memory. A long text has very many different pieces, and the trie keeps a node for each one.

## The abstract type

A suffix trie implements the static [full-text index](/full-text-index/) of a text $S$: `contains(P)` tells whether $P$ occurs in $S$, `count(P)` gives the number of occurrences, and `occurrences(P)` lists their start positions. It is built once from $S$ and then only queried.

## Representation

The text is $S = S[0 \ldots n-1]$ over a general alphabet $\Sigma$: the code only tests symbols for equality and uses them as keys of a map. Indices are 0-based. No [sentinel](/sentinel-character/) is appended, so a suffix can end at an inner node. Each node $x$ has:

- $x.next$, a map from symbols to children;
- $x.count$, a counter;
- $x.ends$, a list of positions.

For a node $x$, let $str(x)$ be the string on the path from the root to $x$.

**Invariant.**

- **(ST1) Nodes are substrings.** The map $x \mapsto str(x)$ is a bijection from the nodes to the distinct substrings of $S$, the empty string included.
- **(ST2) Counts.** For each node $x \ne root$, $x.count$ is the number of positions $i$ with $S[i \ldots i + |str(x)| - 1] = str(x)$.
- **(ST3) Ends.** For each node $x$, $x.ends$ is the list of positions $i \in \{0, \ldots, n-1\}$ with $S_i = str(x)$. A position is in exactly one list.

By (ST1), the number of nodes is $1 + d(S)$, where $d(S)$ is the number of distinct nonempty substrings of $S$.

## Operations

```pseudo id=main
SUFFIX-TRIE-BUILD(S)                     ▷ S[0 .. n − 1]
L1  root ← a new node with no children, count 0, ends empty
L2  for i ← 0 to n − 1 do                 ▷ insert the suffix S[i .. n − 1]
L3      x ← root
L4      for j ← i to n − 1 do
L5          if x.next[S[j]] = NIL then x.next[S[j]] ← a new node
L6          x ← x.next[S[j]]; x.count ← x.count + 1
L7      append i to x.ends

FIND(P)                                  ▷ the node of P, or NIL
L8  x ← root
L9  for each symbol c of P, in order do
L10     x ← x.next[c]
L11     if x = NIL then return NIL
L12 return x
```

**Build.** Each pass of line L2 inserts one suffix, as TRIE-PUT does in a [trie](/trie/). Line L6 counts the suffix at each node on its path, and line L7 records where the suffix ends.

**Contains.** $P$ is a substring if and only if FIND$(P) \ne$ NIL.

**Count.** For a nonempty $P$, the answer is FIND$(P).count$, or 0 if FIND returns NIL.

**Occurrences.** For a nonempty $P$ with node $x$, collect the lists $y.ends$ of all nodes $y$ in the subtree of $x$, with an explicit stack, and sort them. A suffix $S_i$ ends in the subtree of $x$ if and only if $P$ is a prefix of $S_i$, which means that $P$ occurs at $i$.

## Example

Build the suffix trie of $S = \texttt{abab}$. The suffixes are $S_0 = \texttt{abab}$, $S_1 = \texttt{bab}$, $S_2 = \texttt{ab}$ and $S_3 = \texttt{b}$. Each line below is a node: the symbol of its edge, then its count and its list of ends.

```
(root)
├── a   count 2
│   └── b   count 2, ends [2]
│       └── a   count 1
│           └── b   count 1, ends [0]
└── b   count 2, ends [3]
    └── a   count 1
        └── b   count 1, ends [1]
```

The state after each insert:

| step | suffix inserted | new nodes | nodes in total |
|---|---|---|---|
| $i = 0$ | abab | a, ab, aba, abab | 5 |
| $i = 1$ | bab | b, ba, bab | 8 |
| $i = 2$ | ab | none (path a, ab exists) | 8 |
| $i = 3$ | b | none (path b exists) | 8 |

The 8 nodes are the root and the 7 distinct nonempty substrings a, b, ab, ba, aba, bab and abab. The query $P = \texttt{ab}$ reaches the node $\texttt{ab}$ with count 2. Its subtree holds the ends $[2]$ and $[0]$, so $\texttt{ab}$ occurs at positions 0 and 2. The query $\texttt{aa}$ stops at the node $\texttt{a}$, which has no child $\texttt{a}$, so it does not occur. The suffix $\texttt{ab}$ ends at an inner node: without a sentinel, not every suffix has a leaf.

## Correctness

The build keeps (ST1) to (ST3) for the suffixes inserted so far. After the insert of $S_0, \ldots, S_{i}$, the nodes are the distinct prefixes of these suffixes, each count is the number of these suffixes that have $str(x)$ as a prefix, and each end list is right. Since each substring is a prefix of a suffix, after the last insert the nodes are exactly the substrings, and "$str(x)$ is a prefix of $S_i$" is the same as "$str(x)$ occurs at $i$". FIND follows the unique path of $P$, so it returns a node exactly when $P$ is a substring. The full proof is in the proof file.

## Complexity

The costs are in the [word RAM](/word-ram/), with a child map that answers in $O(1)$ time (an array for a constant or integer alphabet, a hash map in expectation for a general one).

| operation | time | notes |
|---|---|---|
| build | $\Theta(n(n+1)/2)$ steps of line L6 | always, even for $\texttt{a}^n$ |
| contains$(P)$ | $O(m)$ | at most $m$ steps of line L10 |
| count$(P)$ | $O(m)$ | |
| occurrences$(P)$ | $O(m + t + occ \log occ)$ | $t$ nodes in the subtree, $t \le occ \cdot (n - m + 1)$ |
| space | $\Theta(1 + d(S))$ nodes | $d(S) \le n(n+1)/2$ |

**Build time.** The suffix $S_i$ has $n - i$ symbols, so line L6 runs $\sum_{i=0}^{n-1} (n - i) = n(n+1)/2$ times.

**Size.** The number of nodes is $1 + d(S)$. Each substring is fixed by its start and its length, so $d(S) \le n(n+1)/2$, with equality when all symbols are distinct. The size is quadratic even over a two-letter alphabet: for $S = \texttt{a}^k\texttt{b}^k$, $n = 2k$, the distinct nonempty substrings are $\texttt{a}^i\texttt{b}^j$ with $0 \le i, j \le k$ and $i + j \ge 1$, so the trie has $(k+1)^2 = (n/2 + 1)^2$ nodes. Periodic strings are small: $\texttt{a}^n$ gives $n + 1$ nodes, and $(\texttt{ab})^{n/2}$ gives $2n$ nodes. The total length of the end lists is $n$, and the counts take one word each.

**Occurrences.** The subtree of the node of $P$ holds one path for each occurrence, of length at most $n - m$ below the node, so its size is $t \le 1 + occ \cdot (n - m)$. The [suffix tree](/suffix-tree/) reduces this to $O(occ)$ by compacting the paths.

## Variants

- **Suffix trie with a sentinel.** Build the trie of $S\$$. Then each suffix ends at its own leaf, the leaves are in one-to-one correspondence with the suffixes, and the end lists are not needed.
- **Online construction with suffix links.** Ukkonen builds the suffix trie of $S[0 \ldots j]$ from that of $S[0 \ldots j-1]$ by walking the [suffix links](/suffix-link/) of the nodes of the current suffixes and adding one child to each. This takes time proportional to the size of the final trie. Compacting this method gives [Ukkonen's algorithm](/ukkonen-algorithm/).
- **Suffix tree.** Replace each maximal chain of one-child nodes by one edge labeled with a substring, stored as two indices into $S$. The result has at most $2n$ nodes. See the [suffix tree size theorem](/suffix-tree-size-theorem/).
- **Suffix automaton.** Merge nodes whose subtrees are equal as automata. The result is the [suffix automaton](/suffix-automaton/), with at most $2n - 1$ states.
- **Depth-limited trie.** Insert only the first $k$ symbols of each suffix. The trie then indexes the substrings of length at most $k$, has at most $nk + 1$ nodes, and supports [q-gram filtering](/q-gram-filtering/) style lookups.

## When to use it

Use a suffix trie to teach and to test: it is the simplest full-text index, it is easy to get right, and it is the oracle against which suffix trees and suffix automata are checked. Use it in practice only for short texts, or with a depth limit. For long texts use a [suffix array](/suffix-array/), a [suffix tree](/suffix-tree/) or a [suffix automaton](/suffix-automaton/), which take $O(n)$ space.

## Pitfalls

- **Recursion on deep tries.** The trie of $\texttt{a}^n$ is a path of length $n$. A recursive walk overflows the stack in Python for $n$ of a few thousand. Use an explicit stack, as in the occurrence walk.
- **Counting at the wrong place.** Incrementing the count only at the end node of a suffix (line L7) gives the number of suffixes equal to $str(x)$, which is 0 or 1. The occurrence count must be incremented at each node of the path, as line L6 does.
- **Forgetting suffixes that end inside.** Without a sentinel, the suffix $\texttt{ab}$ of $\texttt{abab}$ ends at an inner node. Code that collects positions only at leaves misses it. Keep the end lists at each node, or append a sentinel.
- **Expecting linear size.** The number of nodes is the number of distinct substrings, which grows as $n^2$ for most texts. A text of $10^5$ random letters gives billions of nodes.

## Implementations

## History

The trie of all suffixes is the starting point of the expositions of suffix trees, for example in Gusfield's Chapter 5 and in Chapter 5 of Crochemore, Hancart and Lecroq. Ukkonen's 1995 paper first gives an online construction of the suffix trie, with suffix links, in time proportional to its size, and then compacts it to obtain a linear-time suffix tree construction.

## References
