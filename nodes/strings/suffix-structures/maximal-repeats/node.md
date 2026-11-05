---
tag: SPD481
kind: problem
slug: maximal-repeats
name: Maximal repeats
aliases:
- maximal repeat pairs
area: strings/suffix-structures
level: advanced
summary: Find repeated substrings that cannot be extended to the left or right with the same occurrences.
model: word-ram
complexity:
  vars: {n: the length of the string, z: the number of maximal pairs reported}
  time: {worst: Θ(n), pairs: Θ(n + z)}
prereqs: [suffix-tree, lcp-array]
see_also: [longest-repeated-substring, lcp-interval-tree, enhanced-suffix-array, burrows-wheeler-transform, computing-runs, genome-repeat, shortest-unique-substring, suffix-automaton]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 7.12, maximal pairs, maximal repeats and supermaximal repeats, with the left-diverse nodes of the suffix tree and the linear-time algorithms
  - paper: doi:10.1016/S1570-8667(03)00065-0
    title: Mohamed Ibrahim Abouelhoda, Stefan Kurtz and Enno Ohlebusch, Replacing suffix trees with enhanced suffix arrays, Journal of Discrete Algorithms 2(1), 2004
    locator: pages 53 to 86; maximal repeated pairs and supermaximal repeats from the lcp-intervals and the Burrows-Wheeler characters
---

A maximal repeat of a string $T$ is a substring that occurs at least twice and whose occurrences cannot all be extended by the same symbol, neither to the left nor to the right. A string of length $n$ has at most $n - 1$ maximal repeats, they are the left-diverse internal nodes of the [suffix tree](/suffix-tree/), and all of them are found in $\Theta(n)$ time. The related maximal pairs, two occurrences that differ on both sides, are reported in $\Theta(n + z)$ time for $z$ pairs. Maximal repeats summarize all repetition in a text without listing the many repeats that are only parts of longer ones.

## In plain words

A piece of text that appears twice is a repeat. Many repeats are boring: if every copy of "bc" has an "a" just before it, then "abc" says the same thing with more letters. A maximal repeat is a piece that you cannot grow on the left or on the right without losing a copy: the letters just before its copies are not all the same, and the letters just after its copies are not all the same. The start and the end of the text count as letters that differ from all others.

In "banana", the piece "ana" is a maximal repeat. "an" is not, because both copies are followed by "a".

## Definition

**Input.** A string $T = T[0 \ldots n-1]$ over an ordered alphabet, with 0-based indices. For the definitions, treat $T[-1]$ and $T[n]$ as two boundary symbols that differ from each other and from all symbols of $T$. A suffix tree for this problem is built for $T\$$ with a unique sentinel $\$$.

**Maximal pair.** A triple $(i, j, \ell)$ with $i < j$, $\ell \ge 1$ and $T[i \ldots i + \ell - 1] = T[j \ldots j + \ell - 1]$, such that $T[i - 1] \ne T[j - 1]$ and $T[i + \ell] \ne T[j + \ell]$.

**Maximal repeat.** A string $u$ that is the substring of some maximal pair. Equivalently, $u$ occurs at least twice, is *left-maximal* (the symbols $T[p - 1]$ at its occurrences $p$ are not all equal) and is *right-maximal* (the symbols $T[p + |u|]$ are not all equal). The two definitions agree: if the left symbols are not all equal and the right symbols are not all equal, then some two occurrences differ on both sides. (Fix an occurrence $p$ with sides $(a, x)$. If no occurrence differs from it on both sides, there is one with $(b, x)$, $b \ne a$, and one with $(a, y)$, $y \ne x$, and these two differ on both sides.)

**Supermaximal repeat.** A maximal repeat that is not a substring of another maximal repeat.

**Output.** The maximal repeats, each given by its length and one occurrence, or the list of all maximal pairs, or the supermaximal repeats.

## Variants

- **Maximal pairs with a gap.** Only pairs with $j - i$ in a given range, for example to find tandem or interspersed repeats; Brodal, Lyngsø, Pedersen and Stoye solved this in $O(n \log n + z)$ time.
- **Supermaximal repeats.** These are the internal nodes $v$ of the suffix tree whose children are all leaves and whose leaves have pairwise different left symbols.
- **Near-supermaximal and $k$-repeats.** Repeats with at least $k$ occurrences, or with an occurrence not inside a longer repeat.
- **Repeats in several strings.** Maximal repeats common to all strings of a set, with a [generalized suffix tree](/generalized-suffix-tree/).
- **Reverse-complement repeats.** In DNA, a repeat may appear as the reverse complement; search $T$ together with its reverse complement.
- **Tandem repeats and runs.** Consecutive copies $uu \ldots$ form a different structure, the runs of the string, computed by [runs algorithms](/computing-runs/).

## Examples

All values checked by script against a brute-force enumeration of the definition.

| $T$ | maximal repeats | supermaximal | maximal pairs |
|---|---|---|---|
| `banana` | `ana`, `a` | `ana` | 2 |
| `mississippi` | `issi`, `i`, `p`, `s` | `issi`, `p` | 10 |
| `xabcyabcwabcyz` | `abcy`, `abc` | `abcy` | 3 |
| `ababab` | `abab`, `ab` | `abab` | 2 |
| `aaaa` | `aaa`, `aa`, `a` | `aaa` | 3 |
| `abcd` | none | none | 0 |

In `banana`, `ana` occurs at 1 and 3, with left symbols `b` and `n` and right symbols `n` and the end, so $(1, 3, 3)$ is a maximal pair. The string `a` occurs at 1, 3, 5; only the pair $(1, 5, 1)$ is maximal, since the occurrences at 3 and 5 share the left symbol `n`, and those at 1 and 3 share the right symbol `n`. The string `an` occurs at 1 and 3 but both copies are followed by `a`, so it is not right-maximal.

In `xabcyabcwabcyz`, `abc` occurs at 1, 5, 9 with left symbols `x`, `y`, `w`, and is a maximal repeat, but `abcy` (at 1 and 9) contains it, so `abc` is not supermaximal. The string $a^n$ has the $n - 1$ maximal repeats $a, a^2, \ldots, a^{n-1}$, which is the largest possible number.

## Known algorithms

| method | time | notes |
|---|---|---|
| enumerate substrings and their occurrences | $O(n^3)$ or more | an oracle for tests |
| [suffix tree](/suffix-tree/), left-diverse nodes | $\Theta(n)$ for an integer alphabet | Gusfield, Section 7.12 |
| suffix tree, maximal pairs | $\Theta(n + z)$ | merge the leaf lists by left symbol, bottom-up |
| suffix array, [LCP array](/lcp-array/) and BWT | $\Theta(n)$ after the arrays | bottom-up traversal of the [lcp-interval tree](/lcp-interval-tree/) |
| [enhanced suffix array](/enhanced-suffix-array/), maximal pairs | $\Theta(n + z)$ | Abouelhoda, Kurtz and Ohlebusch |
| compact DAWG of $T$ | its size | the internal nodes of the CDAWG are exactly the maximal repeats (Raffinot, 2001) |

**Suffix tree method.** Right-maximal repeats are the path labels of the internal nodes of the suffix tree of $T\$$: such a label is followed by at least two different symbols. An internal node $v$ is *left-diverse* if the leaves below it have at least two different left symbols $T[p - 1]$ (with the boundary as one more symbol). A bottom-up pass computes, for each node, either the unique left symbol of its leaves or "diverse", in $O(1)$ time per child. The maximal repeats are the path labels of the left-diverse internal nodes. Since the tree has at most $n - 1$ internal nodes besides the root (see the [size theorem](/suffix-tree-size-theorem/)), there are at most $n - 1$ maximal repeats.

**Suffix array method.** The internal nodes correspond to the lcp-intervals $[l, r]$ with value $\ell \ge 1$: maximal ranges of the [suffix array](/suffix-array/) whose common prefix has length $\ell$. The interval is left-diverse when the [Burrows-Wheeler](/burrows-wheeler-transform/) symbols $T[SA[k] - 1]$ for $l \le k \le r$ are not all equal, or one of them is the boundary. A stack-based scan of the LCP array visits all lcp-intervals in $O(n)$ time.

## Bounds

- **Number.** At most $n - 1$ maximal repeats, reached by $a^n$. The total length of the maximal repeats can be $\Theta(n^2)$, again for $a^n$, so the output must give each repeat as a position and a length.
- **Pairs.** The number $z$ of maximal pairs can be $\Theta(n^2)$; the bound $\Theta(n + z)$ is then optimal for listing them.
- **Upper bound.** $O(n)$ for an integer alphabet of size $n^{O(1)}$, and $O(n \log \sigma)$ for an ordered alphabet of size $\sigma$.
- **Lower bound.** $\Omega(n)$ in the word RAM. Over a general ordered alphabet, the longest repeat is always a maximal repeat, so the string has a maximal repeat if and only if some symbol occurs twice; this is [element distinctness](/element-distinctness/), with an $\Omega(n \log n)$ lower bound in the algebraic decision tree model.

## Reductions

- **Longest repeated substring.** The [longest repeated substring](/longest-repeated-substring/) is a longest maximal repeat: extending it on either side with a common symbol would give a longer repeat.
- **From element distinctness.** As in the bounds.
- **To the CDAWG.** The nodes of the compact directed acyclic word graph are the maximal repeats, so its size is bounded by the number of right extensions of maximal repeats; this number is a measure of repetitiveness used for compressed indexes.

## Applications

- **Genome analysis.** Programs such as REPuter (Kurtz and Schleiermacher) report maximal repeated pairs in whole genomes to find duplications and repeat families; see [genome repeats](/genome-repeat/).
- **Compression and repetitiveness measures.** The number of maximal repeats and of their extensions measures how repetitive a collection is, and bounds the size of the CDAWG.
- **Text mining and phrase extraction.** Maximal repeats are the candidate phrases of a corpus that are not artifacts of longer phrases.
- **Data structure design.** The left-diverse nodes are where the [BWT](/burrows-wheeler-transform/) changes symbol inside a suffix array interval, which connects maximal repeats with run-length compressed indexes.

## References
