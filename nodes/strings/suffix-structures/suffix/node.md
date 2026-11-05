---
tag: 1CQXNN
kind: definition
slug: suffix
name: Suffix
aliases:
- suffixes
area: strings/suffix-structures
level: intro
summary: A suffix of a string is any of its trailing substrings, starting at some position.
prereqs: [alphabet]
see_also: [sentinel-character, suffix-array, suffix-trie, suffix-tree, suffix-automaton, border, lexicographic-order, lcp-array]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 32 (the notation for prefix and suffix and Lemma 32.1, the overlapping-suffix lemma) and Section 32.5, Suffix arrays
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 1 (the definitions of prefix, suffix and substring) and Chapter 5, Introduction to suffix trees
  - book: isbn:9780521848992
    title: Maxime Crochemore, Christophe Hancart and Thierry Lecroq, Algorithms on Strings, Cambridge University Press, 2007
    locator: Chapter 1, Tools (words, factors, prefixes and suffixes)
---

A suffix of a string is a part of the string that ends at its last character: the string with some number of its first characters removed. A string of length $n$ has exactly $n + 1$ suffixes, one for each start position, and each substring of the string is a prefix of one of them. This last fact is the base of the [suffix array](/suffix-array/), the [suffix tree](/suffix-tree/) and the [suffix automaton](/suffix-automaton/), which store all suffixes in a compact form and so answer questions about all substrings.

## Definition

Let $\Sigma$ be an [alphabet](/alphabet/) and let $S = S[0]S[1] \cdots S[n-1]$ be a string of length $n \ge 0$ over $\Sigma$. Indices are 0-based. For integers $0 \le i \le j \le n$, write $S[i \ldots j-1]$ for the substring $S[i]S[i+1] \cdots S[j-1]$, which is the empty string $\varepsilon$ when $i = j$.

**Suffix.** A string $u$ is a *suffix* of $S$ if $S = vu$ for some string $v$. Equivalently, $u = S[i \ldots n-1]$ for some $i$ with $0 \le i \le n$. We write $S_i$ for this suffix, the *suffix at position $i$*. It has length $n - i$.

**Kinds of suffix.**

- $S_0 = S$ is the whole string, and $S_n = \varepsilon$ is the empty suffix.
- A suffix is *proper* if it is not $S$ itself, that is, if $i \ge 1$.
- A suffix is *nonempty* if $i \le n - 1$. Suffix arrays and suffix trees usually index only the $n$ nonempty suffixes $S_0, \ldots, S_{n-1}$.

**Prefix and substring.** In the same way, $u$ is a *prefix* of $S$ if $S = uv$, that is, $u = S[0 \ldots j-1]$ for some $0 \le j \le n$. A *substring* (or *factor*) is a string $S[i \ldots j-1]$ with $0 \le i \le j \le n$.

**Basic facts.**

1. **Count.** $S$ has exactly $n + 1$ suffixes, and they are pairwise distinct as strings, because $S_i$ has length $n - i$ and these lengths differ.
2. **Substrings are prefixes of suffixes.** For $0 \le i \le j \le n$, the substring $S[i \ldots j-1]$ is the prefix of length $j - i$ of $S_i$. So a pattern $P$ occurs at position $i$ of $S$ if and only if $P$ is a prefix of $S_i$.
3. **Suffix of a suffix.** For $i \le k$, $S_k$ is a suffix of $S_i$. So the suffixes of $S$ are closed under removal of the first character: $S_{i+1}$ is $S_i$ without its first character, for $i < n$.
4. **Order.** Under the [lexicographic order](/lexicographic-order/), two different suffixes never compare equal. If $S_k$ is a proper prefix of $S_i$, then $S_k < S_i$. This can happen only when $k > i$, and then the prefix $S_k$ of $S_i$ is also a suffix of $S_i$, so it is a [border](/border/) of $S_i$.

Fact 2 has a one-line proof: $S_i = S[i \ldots j-1] \cdot S[j \ldots n-1]$. Fact 4 holds because two different strings of which neither is a prefix of the other differ at a first position, and the order is decided there; when one is a prefix of the other, the shorter one is smaller. The case "one suffix is a prefix of another" is the reason for the [sentinel character](/sentinel-character/): after a unique end symbol is appended, no suffix is a proper prefix of another.

## Examples and non-examples

**The suffixes of banana.** For $S = \texttt{banana}$, $n = 6$:

| $i$ | $S_i$ | length |
|---|---|---|
| 0 | banana | 6 |
| 1 | anana | 5 |
| 2 | nana | 4 |
| 3 | ana | 3 |
| 4 | na | 2 |
| 5 | a | 1 |
| 6 | $\varepsilon$ | 0 |

In lexicographic order, the nonempty suffixes are $S_5 < S_3 < S_1 < S_0 < S_4 < S_2$ (a, ana, anana, banana, na, nana). The list of their start positions, $[5, 3, 1, 0, 4, 2]$, is the [suffix array](/suffix-array/) of banana. Here $S_5 = \texttt{a}$ is a prefix of $S_3 = \texttt{ana}$, and $S_3$ is a prefix of $S_1 = \texttt{anana}$, as fact 4 allows.

**Substrings as prefixes.** The substring $\texttt{nan} = S[2 \ldots 4]$ is the prefix of length 3 of $S_2 = \texttt{nana}$. The substring $\texttt{an}$ is a prefix of $S_1$ and of $S_3$, so it occurs at positions 1 and 3. Banana has 15 distinct nonempty substrings.

**Unary and periodic strings.** For $S = \texttt{aaaa}$, each suffix is a prefix of each longer one, and the sorted order is $S_3 < S_2 < S_1 < S_0$. For $S = \texttt{abab}$ the sorted order is $S_2 < S_0 < S_3 < S_1$ (ab, abab, b, bab).

**Non-examples.**

- $\texttt{nan}$ is a substring of banana but not a suffix: no suffix of length 3 equals it, because $S_3 = \texttt{ana}$.
- $\texttt{bnn}$ is a [subsequence](/subsequence/) of banana (positions 0, 2 and 4), but not a substring and so not a suffix.
- $\texttt{ananas}$ is not a suffix: a suffix of $S$ is never longer than $S$, and $\texttt{ananas}$ ends with $\texttt{s}$.

## Related definitions

- **Prefix.** The dual notion. A string that is both a proper prefix and a proper suffix of $S$ is a [border](/border/) of $S$, and borders give the [string period](/string-period/).
- **Sentinel.** A [sentinel character](/sentinel-character/) appended to $S$ makes the set of suffixes prefix-free.
- **Lexicographic order.** The order in which a [suffix array](/suffix-array/) lists the suffixes. See [lexicographic order](/lexicographic-order/).
- **Longest common prefix.** For two suffixes $S_i$ and $S_j$, the length of their longest common prefix is a [longest common extension query](/longest-common-extension-query/). The [LCP array](/lcp-array/) stores it for neighbors in sorted order.
- **Structures over all suffixes.** The [suffix trie](/suffix-trie/) is the [trie](/trie/) of all suffixes, the [suffix tree](/suffix-tree/) is its compacted form, the [suffix array](/suffix-array/) is the sorted list of suffixes, and the [suffix automaton](/suffix-automaton/) is the smallest automaton that accepts exactly the suffixes.

## References
