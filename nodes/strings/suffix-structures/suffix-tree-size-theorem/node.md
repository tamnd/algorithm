---
tag: S54V4V
kind: theorem
slug: suffix-tree-size-theorem
name: Suffix tree size theorem
aliases:
- linear size of suffix trees
area: strings/suffix-structures
level: core
summary: A suffix tree of an n-character string has at most n leaves and at most 2n nodes.
prereqs: [suffix-tree]
see_also: [suffix-trie, suffix-automaton-size-theorem, suffix-tree-construction, ukkonen-algorithm, maximal-repeats, radix-tree, implicit-suffix-tree, distinct-substrings-counting]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 5, Introduction to suffix trees (the definition with the terminal symbol, and the bound on the number of nodes and the space with edge labels as index pairs)
  - paper: doi:10.1145/321941.321946
    title: Edward M. McCreight, A space-economical suffix tree construction algorithm, Journal of the ACM 23(2), 1976
    locator: pages 262 to 272; the linear bound on the number of nodes of the compact tree
  - book: isbn:9780521848992
    title: Maxime Crochemore, Christophe Hancart and Thierry Lecroq, Algorithms on Strings, Cambridge University Press, 2007
    locator: Chapter 5, Structures for indexes (the size of the compact suffix tree)
---

The [suffix tree](/suffix-tree/) of a string $S$ of length $n \ge 1$, with a [sentinel](/sentinel-character/) appended, has exactly $n + 1$ leaves and at most $n$ inner nodes, so at most $2n + 1$ nodes and $2n$ edges. Without the sentinel, the tree has at most $n$ leaves and at most $2n - 1$ nodes for $n \ge 2$. Since each edge label is stored as two indices into $S$, the tree takes $O(n)$ words, while the [suffix trie](/suffix-trie/) it compacts can have $\Theta(n^2)$ nodes. This bound is what makes linear-time suffix tree algorithms possible.

## Statement

Let $S = S[0 \ldots n-1]$, 0-based, over any alphabet, and $T = S\$$, where $\$$ is a symbol that does not occur in $S$. The suffix tree of $T$ is the compact trie of the suffixes $T_i = T[i \ldots n]$, $0 \le i \le n$: each edge has a nonempty label, the child edges of a node start with distinct symbols, and each node other than the root and the leaves has at least two children. The tree is unique, so the statement is about the tree, not about a construction.

**Theorem.** For $n \ge 1$:

1. **(Leaves.)** The suffix tree of $T$ has exactly $n + 1$ leaves, one for each suffix of $T$.
2. **(Inner nodes.)** It has at most $n$ inner nodes, the root included. Equivalently, $S$ has at most $n - 1$ distinct nonempty right-branching substrings: substrings $x$ such that $xc$ and $xd$ are substrings of $T$ for two symbols $c \ne d$.
3. **(Total.)** It has at most $2n + 1$ nodes and at most $2n$ edges, and with labels stored as index pairs it takes $O(n)$ words.
4. **(No sentinel.)** The compact trie of the suffixes of $S$ alone, the implicit suffix tree, has at most $n$ leaves and, for $n \ge 2$, at most $2n - 1$ nodes.

The bounds hold for every alphabet, of any size.

## In plain words

Each ending of the text has its own leaf, so there is one leaf for each letter of the text, plus one for the end mark. Every other node, except the top, is a place where the tree splits into at least two branches.

Think of a tree where each split sends paths two ways. Each split adds at least one more path, and the paths end at the leaves. So there are fewer splits than leaves. So the whole tree has at most about twice as many nodes as the text has letters.

The letters on the edges are not stored, only where they start and end in the text. So the tree takes space in proportion to the length of the text.

## Proof

**Leaves.** Since $\$$ occurs only at index $n$, no suffix $T_j$ is a proper prefix of another suffix $T_i$: for $i < j$, $T_j$ has $\$$ at offset $n - j$, but $T_i$ has there the symbol $T[i + n - j]$ with $i + n - j < n$, which is not $\$$. In the trie of the suffixes, a string ends at a leaf if and only if it is not a proper prefix of another string of the trie. So each $T_i$ ends at a leaf, different suffixes end at different leaves, and each leaf is the end of some suffix (a leaf ends a path that spells a whole inserted string). Compaction removes only nodes with one child, which are not leaves. So there are exactly $n + 1$ leaves.

**Inner nodes.** Let $L = n + 1$ be the number of leaves and $I$ the number of inner nodes, the root included. The root has at least two children: the edge that starts with $\$$ (from the suffix $T_n = \$$) and the edge that starts with $S[0]$, which is not $\$$. Each other inner node has at least two children. Each node except the root is the child of exactly one node, so the number of edges is

$$E = L + I - 1 \ \ge\ 2I,$$

which gives $I \le L - 1 = n$.

**Right-branching substrings.** For an inner node $v \ne$ root, with path label $x$, two child edges start with different symbols $c \ne d$, so $xc$ and $xd$ are substrings of $T$, and $x$ is a nonempty substring of $S$ (it contains no $\$$, since $\$$ ends each path that contains it, at a leaf). Conversely, if $xc$ and $xd$ are substrings with $c \ne d$, the paths of $xc$ and $xd$ split exactly after $x$; a split inside an edge is impossible, so $x$ is the path label of a node. So the nonempty right-branching substrings are in bijection with the inner nodes other than the root, and there are at most $n - 1$ of them.

**Total and space.** The number of nodes is $L + I \le 2n + 1$, and the number of edges is one less, at most $2n$. Each node stores a constant number of integers (two for its label, a string depth, a leaf number) besides its child map, and the child maps hold one entry for each edge, $2n$ in all. So the space is $O(n)$ words.

**No sentinel.** In the compact trie of the suffixes of $S$ alone, every leaf still ends some suffix of $S$ (the end of a path that is a prefix of no other suffix), and different leaves end different suffixes, so $L \le n$. If $S$ has two different symbols, the root has at least two children, and the count above gives $I \le L - 1$, so at most $2L - 1 \le 2n - 1$ nodes. If $S = \texttt{a}^n$, every suffix is a prefix of $S$, and the tree is the root with one leaf edge labeled $S$: 2 nodes, and $2 \le 2n - 1$ for $n \ge 2$. $\blacksquare$

## Consequences

- **Linear-time construction is possible.** The output has $O(n)$ size, so algorithms such as [Ukkonen's](/ukkonen-algorithm/), [McCreight's](/mccreight-algorithm/) and [Weiner's](/weiner-algorithm/) can build it in $O(n)$ time for a constant alphabet, even though the [suffix trie](/suffix-trie/) has $\Theta(n^2)$ nodes in the worst case.
- **Reporting in $O(occ)$.** A subtree with $k$ leaves has fewer than $2k$ nodes, so listing the occurrences below the locus of a pattern takes time linear in their number.
- **Few right-maximal repeats.** By part 2, a string of length $n$ has at most $n - 1$ distinct right-branching substrings, and so at most $n - 1$ [maximal repeats](/maximal-repeats/), which are among them.
- **LCP intervals.** The inner nodes correspond to the LCP intervals of the [suffix array](/suffix-array/), so there are at most $n$ of them, and a stack-based scan of the LCP array visits them all in $O(n)$ time.
- **Distinct substrings.** The number of distinct substrings of $S$ is the total length of the edge labels without $\$$, which the tree computes in $O(n)$ time from $O(n)$ nodes, although the number itself can be $\Theta(n^2)$. See [distinct substrings counting](/distinct-substrings-counting/).

## Tightness

- **Upper bound.** For $S = \texttt{a}^n$, $T = \texttt{a}^n\$$ has the right-branching substrings $\texttt{a}^k$ for $1 \le k \le n - 1$ (each followed by $\texttt{a}$ and by $\$$), so the tree has $n + 1$ leaves, $n$ inner nodes and $2n + 1$ nodes. The bound is reached exactly when all inner nodes have two children, which also happens for many other strings over two letters.
- **Lower bound.** The tree always has at least $n + 2$ nodes, the root and $n + 1$ leaves. This is reached when the symbols of $S$ are pairwise distinct, for example $S = \texttt{abc}$: no nonempty substring is right-branching, and the root has $n + 1$ leaf children.
- **The implicit tree.** For $S = \texttt{a}^{n-1}\texttt{b}$, $n \ge 2$, no suffix is a prefix of another (each ends with the only $\texttt{b}$), so the implicit tree equals the suffix tree of $S$ seen as ending with the unique symbol $\texttt{b}$: $n$ leaves and the $n - 1$ inner nodes root, $\texttt{a}, \ldots, \texttt{a}^{n-2}$, so $2n - 1$ nodes. A search over all strings of length up to 8 over two letters shows that $\texttt{a}^{n-1}\texttt{b}$ and $\texttt{b}^{n-1}\texttt{a}$ are the only ones that reach it.
- **Labels.** Written out, the labels are long: when the symbols of $S$ are pairwise distinct, the root has the $n + 1$ leaf edges $T_0, \ldots, T_n$, of total length $(n + 1)(n + 2)/2$. Index pairs are needed for linear space.

## History

The linear bound appears with the first linear-time constructions: Weiner in 1973 and McCreight in 1976, whose paper stresses the space economy of storing labels as pointers into the text. Textbooks such as Gusfield (Chapter 5) and Crochemore, Hancart and Lecroq prove it by the same count of branching nodes. The companion bound for the [suffix automaton](/suffix-automaton/), at most $2n - 1$ states, is due to Blumer and others; see the [suffix automaton size theorem](/suffix-automaton-size-theorem/).

## References
