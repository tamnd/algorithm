---
tag: D4GH2P
kind: definition
slug: sentinel-character
name: Sentinel character
aliases:
- terminal symbol
- end marker
- dollar sign
area: strings/suffix-structures
level: intro
summary: A unique end symbol appended to a string so that no suffix is a prefix of another.
prereqs: [suffix, alphabet]
see_also: [suffix-tree, suffix-array, suffix-trie, burrows-wheeler-transform, generalized-suffix-tree, implicit-suffix-tree, lexicographic-order]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 5, Introduction to suffix trees (the terminal character $ that makes each suffix end at a leaf), and Chapter 6 (implicit suffix trees in Ukkonen's algorithm)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 32.5, Suffix arrays
  - paper: "Michael Burrows and David J. Wheeler, A block-sorting lossless data compression algorithm, Research Report 124, Digital Systems Research Center, 1994"
    locator: the transform and its inverse (the original version stores the row index of the input instead of an end symbol)
---

A sentinel character is a symbol that does not occur in a string and is appended to its end, usually written $\$$. It makes each [suffix](/suffix/) of the extended string end with a symbol that occurs only once, so no suffix is a proper prefix of another. This one fact makes every suffix end at a leaf of the [suffix tree](/suffix-tree/), fixes the order of the [suffix array](/suffix-array/), and makes the [Burrows-Wheeler transform](/burrows-wheeler-transform/) invertible without extra data.

## Definition

Let $S = S[0 \ldots n-1]$ be a string over an ordered [alphabet](/alphabet/) $\Sigma$, with 0-based indices. A *sentinel* is a symbol $\$ \notin \Sigma$. The *terminated string* is $S\$ = S[0 \ldots n-1]\,\$$, of length $n + 1$, with $S\$[n] = \$$. The order on $\Sigma$ is extended to $\Sigma \cup \{\$\}$ by one of two conventions:

- **smallest sentinel:** $\$ < c$ for each $c \in \Sigma$. This is the usual convention for suffix arrays and the Burrows-Wheeler transform;
- **largest sentinel:** $\$ > c$ for each $c \in \Sigma$. Some texts use this, and the order of the suffixes then changes (see the examples).

For trees and automata only equality matters, so the order of $\$$ is not used there.

**Property (prefix-freeness).** For $0 \le i < j \le n$, the suffix $(S\$)_j$ is not a prefix of $(S\$)_i$.

*Proof.* The suffix $(S\$)_j$ has length $n + 1 - j$, and its last symbol, at index $n - j$, is $\$$. If it were a prefix of $(S\$)_i$, then $(S\$)_i[n - j] = S\$[i + n - j] = \$$. But $i + n - j < n$, and $\$$ occurs in $S\$$ only at index $n$. $\square$

**Property (order).** With the smallest sentinel, the suffix array of $S\$$ is $n$ followed by the suffix array of $S$: for $0 \le i, j < n$, $(S\$)_i < (S\$)_j$ if and only if $S_i < S_j$, and $(S\$)_n = \$$ is the smallest suffix.

*Proof.* Let $\ell$ be the length of the longest common prefix of $S_i$ and $S_j$. If neither is a prefix of the other, both terminated suffixes differ first at offset $\ell$, at the same two symbols of $\Sigma$, so the order is the same. If $S_j$ is a proper prefix of $S_i$, then $S_j < S_i$, and the terminated suffixes differ first at offset $\ell = |S_j|$, where $(S\$)_j$ has $\$$ and $(S\$)_i$ has a symbol of $\Sigma$, which is larger. The suffix $\$$ is smaller than every other suffix because its first symbol is. $\square$

With the largest sentinel the second property fails: a suffix that is a prefix of another now comes after it.

## Examples and non-examples

**Smallest sentinel.** For $S = \texttt{banana}$, the suffix array of $\texttt{banana\$}$ is $[6, 5, 3, 1, 0, 4, 2]$, which is $6$ followed by the suffix array $[5, 3, 1, 0, 4, 2]$ of banana. The Burrows-Wheeler transform, the symbol before each sorted suffix, is $\texttt{annb\$aa}$.

**Largest sentinel.** With $\$$ larger than each letter, the suffix array of $\texttt{banana\$}$ is $[1, 3, 5, 0, 2, 4, 6]$. Now $\texttt{anana\$} < \texttt{ana\$} < \texttt{a\$}$, because at the offset where the shorter suffix has $\$$, the longer one has $\texttt{n}$, and $\$ > \texttt{n}$. For $\texttt{aaaa}$ the two conventions give $[4, 3, 2, 1, 0]$ and $[0, 1, 2, 3, 4]$.

**Leaves of the suffix trie.** In the [suffix trie](/suffix-trie/) of $\texttt{abab}$, the suffix $\texttt{ab}$ ends at an inner node, on the path of $\texttt{abab}$, and $\texttt{b}$ ends on the path of $\texttt{bab}$. In the trie of $\texttt{abab\$}$, each of the 5 suffixes ends at its own leaf. This is why a suffix tree is usually built for $S\$$: then it has exactly $n + 1$ leaves.

**Generalized sentinels.** To index several strings $S^1, \ldots, S^k$ at the same time, as in a [generalized suffix tree](/generalized-suffix-tree/), each string gets its own sentinel: $S^1\$_1 S^2\$_2 \cdots S^k\$_k$, with distinct symbols $\$_1, \ldots, \$_k \notin \Sigma$. With one shared $\$$, a suffix of the concatenation could match across the end of one string into the next, and the structure would report substrings that occur in no single string.

**Non-examples.**

- Appending $\texttt{a}$ to banana does not give a sentinel: $\texttt{a}$ already occurs, and in $\texttt{bananaa}$ the suffix $\texttt{a}$ is a prefix of $\texttt{aa}$.
- A $\texttt{\#}$ is not a sentinel for a text that already contains $\texttt{\#}$. In C, the end byte 0 works as a sentinel only for strings without a 0 byte.
- A symbol that is unique but placed at the start of the string, as in $\$S$, does not make the suffixes prefix-free: it only makes the prefixes suffix-free.

## Related definitions

- **Implicit suffix tree.** The tree of $S$ without the sentinel, in which some suffixes end inside an edge or at an inner node. [Ukkonen's algorithm](/ukkonen-algorithm/) keeps this [implicit suffix tree](/implicit-suffix-tree/) and turns it into the true suffix tree by one more step with $\$$.
- **Sentinel search.** In [sentinel search](/sentinel-search/), a copy of the key is put at the end of an array so that a loop needs no index test. It is a different use of the same word.
- **Integer alphabets.** Suffix sorting programs such as [SA-IS](/sa-is/) map the alphabet to $1, \ldots, \sigma$ and use $0$ as the sentinel, so the smallest-sentinel convention holds by construction.
- **Rotations.** The rows of the Burrows-Wheeler matrix are rotations of $S\$$. Because $\$$ is unique, sorting the rotations gives the same order as sorting the suffixes. Without a sentinel, rotations and suffixes can sort in different orders; the [circular suffix array](/circular-suffix-array/) sorts the rotations directly.

## References
