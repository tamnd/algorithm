---
tag: 21ZQTC
kind: data-structure
slug: suffix-tree
name: Suffix tree
aliases:
- Patricia suffix tree
- Weiner tree
- compact suffix trie
area: strings/suffix-structures
level: core
summary: A compacted suffix trie with linear size, supporting substring queries in time linear in the pattern length.
implements: [full-text-index]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, z: the number of occurrences}
  time: {query: O(m), report: O(m + z), build: O(n)}
  space: {extra: O(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [suffix-trie, sentinel-character]
see_also: [suffix-tree-size-theorem, suffix-tree-construction, ukkonen-algorithm, suffix-link, suffix-array, suffix-automaton, generalized-suffix-tree, radix-tree]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 5, Introduction to suffix trees (the definition, the naive construction and the use for exact matching); Chapter 7 (applications)
  - paper: doi:10.1109/SWAT.1973.13
    title: Peter Weiner, Linear pattern matching algorithms, 14th Annual Symposium on Switching and Automata Theory, 1973
    locator: pages 1 to 11; the first linear-time construction of a compacted tree of all suffixes
  - paper: doi:10.1145/321941.321946
    title: Edward M. McCreight, A space-economical suffix tree construction algorithm, Journal of the ACM 23(2), 1976
    locator: pages 262 to 272
  - paper: doi:10.1007/BF01206331
    title: Esko Ukkonen, On-line construction of suffix trees, Algorithmica 14(3), 1995
    locator: pages 249 to 260
  - paper: doi:10.1109/SFCS.1997.646102
    title: Martin Farach, Optimal suffix tree construction with large alphabets, FOCS 1997
    locator: pages 137 to 143; linear time for an integer alphabet
---

A suffix tree is the [suffix trie](/suffix-trie/) with each chain of one-child nodes replaced by one edge labeled with a substring. For a text $S$ of length $n$ with a [sentinel](/sentinel-character/) appended, it has exactly $n + 1$ leaves, one for each suffix, and at most $2n + 1$ nodes in total for $n \ge 1$; each edge label is stored as two indices into the text, so the whole tree takes $O(n)$ space. It finds a pattern of length $m$ in $O(m)$ time for a constant alphabet, and with a depth-first walk it answers many questions about repeats and common substrings in linear time. Weiner built it in linear time in 1973, and [Ukkonen's algorithm](/ukkonen-algorithm/) is the construction most often taught.

## In plain words

Put all endings of a word into a [trie](/trie/), one letter on each edge. Many nodes of this trie have only one child: the path just runs along without a choice. Squeeze each such run into one edge, and write the whole run of letters on that edge. What is left is the suffix tree.

Each branch point now means "here the endings go different ways". There are fewer branch points than letters in the word, so the tree is small. The letters on a long edge are not copied; the edge only remembers where they are in the word, as a start and an end. Searching works as in the trie: follow the letters of the pattern down from the top, along the edges.

## The abstract type

A suffix tree implements the static [full-text index](/full-text-index/) of a text $S$: `contains(P)`, `count(P)` and `occurrences(P)` for a pattern $P$. It also gives, through its shape, the right-branching substrings of $S$ (its inner nodes), the [suffix array](/suffix-array/) (the leaves in order), and the longest common prefix of any two suffixes (the string depth of their [lowest common ancestor](/lowest-common-ancestor/)).

## Representation

The text is $S = S[0 \ldots n-1]$, 0-based, and the tree is built for $T = S\$$, with a unique sentinel $\$$ at index $n$ that is smaller than every symbol. The code uses symbols as hash keys and compares them for equality; the order is needed only to list the leaves in suffix order. Each node $v$ has

- an incoming edge label $T[start(v) \ldots end(v) - 1]$, stored as the two integers;
- a map $children(v)$ from the first symbol of each child edge to the child;
- the *string depth* $depth(v)$, the length of the path label $str(v)$ from the root to $v$;
- for a leaf, the start $i$ of its suffix.

**Invariant.**

- **(T1) Compact trie.** Each edge label is nonempty, the child edges of a node start with distinct symbols, and each inner node other than the root has at least two children.
- **(T2) Leaves are suffixes.** There are exactly $n + 1$ leaves, and the leaf with start $i$ has $str(v) = T[i \ldots n]$.
- **(T3) Depths.** $depth(v) = |str(v)|$.

Because $\$$ occurs only at the end, no suffix of $T$ is a prefix of another, so every suffix ends at a leaf. Without the sentinel, a suffix that is also a prefix of a longer suffix, such as $\texttt{ab}$ in $\texttt{abab}$, ends inside an edge, and (T2) fails. By (T1) and (T2), the inner nodes are the root and the substrings $x$ of $S$ that are followed in $T$ by two different symbols, the *right-branching* substrings. The [suffix tree size theorem](/suffix-tree-size-theorem/) gives at most $n$ inner nodes and $2n + 1$ nodes for $T$ of length $n + 1$.

Many constructions also store a [suffix link](/suffix-link/) at each inner node: from the node of $cx$, for a symbol $c$, to the node of $x$.

## Operations

```pseudo id=main
SUFFIX-TREE-BUILD(S)                      ▷ T = S$, quadratic time
L1  for i ← 0 to n do                      ▷ insert the suffix T[i .. n]
L2      v ← root; j ← i                    ▷ T[i .. j − 1] is spelled at v
        loop
L3          if v has no child edge starting with T[j] then
L4              add a leaf for i under v with label T[j .. n]; break
L5          w ← the child of v by T[j]; (a, b) ← the label of w
L6          k ← the length of the common prefix of T[a .. b − 1] and T[j ..]
L7          if k = b − a then v ← w; j ← j + k; continue
L8          split the edge into w at k: a new inner node u with label T[a .. a + k − 1]
L9          add a leaf for i under u with label T[j + k .. n]; break

LOCUS(P)                                  ▷ the highest node below the end of P
L10 v ← root; i ← 0
    while i < m do
L11     w ← the child of v by P[i]; if none then return NIL
L12     match P[i ..] along the label of w; on a mismatch return NIL; v ← w
L13 return v
```

**Build.** This is the naive construction: each suffix is inserted as into a [radix tree](/radix-tree/), splitting an edge where it leaves the tree. It takes $O(n^2)$ time in the worst case and is the oracle for the fast constructions; see [suffix tree construction](/suffix-tree-construction/) for $O(n)$ methods.

**Search.** $P$ occurs in $S$ if and only if LOCUS$(P) \ne$ NIL. The pattern may end inside the edge into the returned node $v$; the occurrences are then the same as those of $str(v)$.

**Count.** Store at each node the number of leaves below it, other than the leaf of $\$$, by one post-order pass. Then count$(P)$ is this number at LOCUS$(P)$, in $O(m)$ time.

**Occurrences.** Walk the subtree of LOCUS$(P)$ and report the start of each leaf. Every inner node has at least two children, so a subtree with $occ$ leaves has fewer than $2 \cdot occ$ nodes, and the walk takes $O(occ)$ time.

**Suffix array.** A depth-first walk that visits the children in the order of their first symbols, $\$$ first, lists the leaves in the order of the suffixes. Removing the leaf of $\$$ gives the suffix array of $S$.

## Example

The suffix tree of $T = \texttt{banana\$}$. Each line is an edge, with its label, the string depth of the node below it, and, for a leaf, the start of its suffix.

```
(root)
├── $             depth 1, leaf 6
├── a             depth 1
│   ├── $         depth 2, leaf 5
│   └── na        depth 3
│       ├── $     depth 4, leaf 3
│       └── na$   depth 6, leaf 1
├── banana$       depth 7, leaf 0
└── na            depth 2
    ├── $         depth 3, leaf 4
    └── na$       depth 5, leaf 2
```

The tree has 7 leaves and 4 inner nodes: the root and the right-branching substrings $\texttt{a}$, $\texttt{ana}$ and $\texttt{na}$. The suffix trie of $\texttt{banana\$}$ has 23 nodes; the suffix tree has 11. The edge $\texttt{na\$}$ below $\texttt{ana}$ is stored as $[4, 7)$, the positions of $\texttt{na\$}$ in $T$.

The query $P = \texttt{an}$ goes down the edge $\texttt{a}$, then into the edge $\texttt{na}$ and stops after its first symbol. LOCUS returns the node $\texttt{ana}$, which has 2 real leaves, 3 and 1: $\texttt{an}$ occurs at positions 1 and 3. The query $\texttt{nab}$ goes down $\texttt{na}$ and finds no child edge starting with $\texttt{b}$, so it does not occur. Reading the leaves in symbol order gives $6, 5, 3, 1, 0, 4, 2$, and without the 6 this is the suffix array $[5, 3, 1, 0, 4, 2]$.

## Correctness

The build keeps (T1) to (T3) for the tree of the suffixes $T_0, \ldots, T_{i-1}$ inserted so far. The walk of lines L2 to L7 follows the longest prefix of $T_i$ that is spelled from the root. That prefix is not all of $T_i$, since $T_i$ ends with $\$$, which appears in no other suffix at the same depth. If it ends at a node, line L4 adds a child with a new first symbol; if it ends inside an edge, line L8 creates a node with two children, the old one and the new leaf. In both cases labels stay nonempty, first symbols stay distinct, and no inner node gets one child. LOCUS follows the unique path that spells $P$, because the first symbols of child edges are distinct, and $P$ is a substring if and only if it is a prefix of some suffix, that is, spelled by a path. The proof file gives the details and the count of nodes.

## Complexity

The query costs assume that finding the child of a node by a symbol takes $O(1)$ time: an array of size $|\Sigma|$ at each node for a constant alphabet, or a hash table, which gives $O(1)$ expected time. With children in sorted lists or balanced trees, each step costs $O(\log |\Sigma|)$.

| operation | time | notes |
|---|---|---|
| build, naive (as above) | $O(n^2)$ worst | $O(n \log n)$ expected on random text |
| build, [Ukkonen](/ukkonen-algorithm/), [McCreight](/mccreight-algorithm/), [Weiner](/weiner-algorithm/) | $O(n)$ for a constant alphabet | $O(n \log \lvert\Sigma\rvert)$ with ordered child maps |
| build, Farach | $O(n)$ for an integer alphabet | also from $SA$ and LCP in $O(n)$ |
| contains, count | $O(m)$ | |
| occurrences | $O(m + occ)$ | |
| longest common prefix of two suffixes | $O(1)$ | after $O(n)$ preprocessing for LCA |
| space | $O(n)$ words | at most $2n + 1$ nodes for $n \ge 1$ |

The constant in the space is large: with child maps, suffix links and depths, a pointer-based suffix tree takes several machine words for each text symbol, which is several times the $n$ words of a [suffix array](/suffix-array/).

## Variants

- **Generalized suffix tree.** The tree of the suffixes of several strings, each with its own end marker; it finds the longest common substring. See the [generalized suffix tree](/generalized-suffix-tree/).
- **Implicit suffix tree.** The same tree without the sentinel, where some suffixes end inside edges or at inner nodes. Ukkonen's algorithm keeps this tree while it reads the text; see the [implicit suffix tree](/implicit-suffix-tree/).
- **Suffix tree with suffix links.** Inner nodes carry [suffix links](/suffix-link/); the linear-time constructions need them, and so do [matching statistics](/matching-statistics/).
- **Sparse suffix tree.** Only the suffixes that start at selected positions, such as word starts. See the [sparse suffix tree](/sparse-suffix-tree/).
- **Enhanced and compressed forms.** The [suffix array](/suffix-array/) with the LCP array and a child table simulates the tree in less space ([enhanced suffix array](/enhanced-suffix-array/)), and compressed suffix trees use compressed suffix arrays.
- **Suffix automaton.** Merging nodes with the same set of end positions, instead of compacting chains, gives the [suffix automaton](/suffix-automaton/), whose reverse suffix links form the suffix tree of the reversed string.

## When to use it

Use a suffix tree when you need many structural queries on one text: repeats, the longest common substring of two strings, palindromes with LCA queries, or the online matching of many patterns against one text. Its operations are simple to state on the tree, and many textbook string problems have linear-time solutions as one walk over it. When memory matters, or when you only need pattern search, a [suffix array](/suffix-array/) with [binary search](/suffix-array-search/), or an [FM-index](/fm-index/), does the same with several times less space.

## Pitfalls

- **No sentinel.** Without a unique end marker, the suffix $\texttt{ab}$ of $\texttt{abab}$ has no leaf, and code that counts occurrences by leaves gets 1 instead of 2 for $\texttt{ab}$. Append $\$$, or handle suffixes that end at inner nodes.
- **Copying edge labels.** Storing the label as a string, not as two indices, makes the total size quadratic: the labels of the leaf edges of $\texttt{a}^n\$$ sum to more than $n^2/2$ symbols.
- **Recursive walks.** The tree of $\texttt{a}^n\$$ has depth $n + 1$. A recursive depth-first walk overflows the stack in Python for large $n$; use an explicit stack.
- **The sentinel leaf.** The leaf of the suffix $\$$ alone is not an occurrence of anything in $S$. Counting leaves without excluding it gives $n + 1$ for the empty pattern.
- **Child maps that cost $|\Sigma|$.** An array of size $|\Sigma|$ at each node costs $\Theta(n |\Sigma|)$ space, which is too much for large alphabets such as words or integers.

## Implementations

## History

Weiner introduced the structure in 1973, under the name position tree, with the first linear-time construction. McCreight gave a more space-economical construction in 1976 that inserts the suffixes from the longest, and Ukkonen in 1995 an online construction that reads the text from left to right. Farach showed in 1997 that the suffix tree can be built in linear time for an integer alphabet. Gusfield's 1997 book collected many of its applications. Since the 1990s, the suffix array and compressed indexes have replaced it in practice for large texts, while it remains the standard model for reasoning about substrings.

## References
