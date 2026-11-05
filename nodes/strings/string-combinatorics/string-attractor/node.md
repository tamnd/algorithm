---
tag: PED59F
kind: concept
slug: string-attractor
name: String attractor
aliases:
- attractor of a string
area: strings/string-combinatorics
level: research
summary: A set of positions whose occurrences hit every distinct substring of the word.
prereqs: [lempel-ziv-factorization]
see_also: [burrows-wheeler-transform, r-index, smallest-grammar-problem, hitting-set, subword-complexity, sturmian-word, thue-morse-word, run-length-encoding]
sources:
  - paper: "Dominik Kempa and Nicola Prezza, At the roots of dictionary compression: string attractors, Proceedings of the 50th Annual ACM SIGACT Symposium on Theory of Computing (STOC 2018), 827-840"
    locator: the definition of string attractors, the attractors induced by LZ77, grammars, macro schemes and BWT runs, and the NP-completeness of finding a smallest attractor
  - paper: "Tomasz Kociumaka, Gonzalo Navarro and Nicola Prezza, Toward a definitive compressibility measure for repetitive sequences, IEEE Transactions on Information Theory 69(4), 2023, 2074-2092"
    locator: the measure delta, the bound delta at most gamma, and the bound z = O(delta log(n/delta))
  - paper: "Gonzalo Navarro, Indexing highly repetitive string collections, part I: repetitiveness measures, ACM Computing Surveys 54(2), 2021, article 29"
    locator: the section on string attractors and the comparison of the measures delta, gamma, b, z, g and r
  - paper: "Sabrina Mantaci, Antonio Restivo, Giuseppe Romana, Giovanna Rosone and Marinella Sciortino, A combinatorial view on string attractors, Theoretical Computer Science 850, 2021, 236-248"
    locator: smallest attractors of standard Sturmian words and other families from combinatorics on words
---

A string attractor of a string $T$ is a set $\Gamma$ of positions such that every distinct substring of $T$ has at least one occurrence that contains a position of $\Gamma$. The size $\gamma(T)$ of a smallest attractor is a measure of repetitiveness: it is at most the number of phrases of the [Lempel-Ziv factorization](/lempel-ziv-factorization/), the number of runs of the [Burrows-Wheeler transform](/burrows-wheeler-transform/) and the size of a smallest grammar, and at least the substring-complexity measure $\delta$. Kempa and Prezza introduced attractors in 2018 to explain why all these compressors land within logarithmic factors of each other.

## In plain words

Mark a few positions in a text. The marks form an attractor if every piece of the text, of any length, appears somewhere in the text at a place that covers a mark. A text made of the same few blocks repeated over and over needs few marks, because each piece can be found next to one of them, while a text with no repetition needs a mark almost everywhere.

The smallest number of marks is a measure of how repetitive the text is. Each of the usual ways of compressing repetitive text, such as copying earlier pieces or reusing grammar rules, gives an attractor of about its own size, so this number is never larger than what those compressors produce. Finding the smallest set of marks is hard in general.

## The idea

Let $T = T[0..n-1]$ be a string over an [alphabet](/alphabet/) $\Sigma$, with 0-based indices; only equality of letters is used. An occurrence $T[i..j]$ *crosses* a position $k$ if $i \le k \le j$.

**Definition.** A set $\Gamma \subseteq \{0, \ldots, n-1\}$ is a *string attractor* of $T$ if every nonempty substring $S$ of $T$ has an occurrence $T[i..j] = S$ that crosses some $k \in \Gamma$. The smallest size of an attractor is $\gamma(T)$.

The definition asks for one occurrence per distinct substring, not for every occurrence. Finding a smallest attractor is a [hitting set](/hitting-set/) problem: the ground set is the set of positions, and each distinct substring $S$ contributes the set of positions crossed by its occurrences.

**Two easy bounds.**

- $\gamma(T) \ge |\{\text{letters occurring in } T\}|$, because a substring of length 1 crosses only its own position, so every letter of $T$ must occur at a position of $\Gamma$.
- $\gamma(T) \ge \delta(T)$, where $d_k$ is the number of distinct substrings of length $k$ and $\delta(T) = \max_{k \ge 1} d_k / k$, the measure of Kociumaka, Navarro and Prezza built from the [factor complexity](/subword-complexity/). *Proof.* Fix $k$ and an attractor $\Gamma$. Each distinct substring of length $k$ has an occurrence starting at some $i$ with $i \le q \le i + k - 1$ for some $q \in \Gamma$. For a fixed $q$ at most $k$ starting positions $i$ satisfy this, and an occurrence determines its substring, so $d_k \le k |\Gamma|$. $\square$

**Attractors from Lempel-Ziv.** Use the LZ77 parsing in which each phrase is the longest prefix of the remaining suffix that has an occurrence starting at an earlier position (overlap allowed), or a single fresh letter if there is none; let $z$ be the number of phrases. Then the set $\Gamma_{LZ}$ of the last positions of the phrases is an attractor, so $\gamma(T) \le z$.

*Proof.* Let $S$ be a substring and $T[i..j]$ its leftmost occurrence. Suppose it crosses no phrase end. Then it lies inside one phrase $T[a..b]$ with $a \le i \le j < b$. That phrase is not a fresh letter, since it has length at least 2, so $T[a..b]$ also occurs at some $a' < a$, and then $S = T[i..j]$ also occurs at $a' + (i - a) < i$, which contradicts leftmostness. $\square$

**Other compressors.** Kempa and Prezza showed in the same way that a straight-line program with $g$ rules, a bidirectional macro scheme with $b$ phrases and a BWT with $r$ runs each yield an attractor of size $O(g)$, $b$ and $r$. Together with the bound $z = O(\delta \log(n/\delta))$ of Kociumaka, Navarro and Prezza, this places the measures in the order
$$ \delta \le \gamma \le b \le z, \qquad \gamma = O(g), \qquad \gamma \le r, $$
and shows that $b$ and $z$ are $O(\gamma \log(n/\gamma))$, since $\delta \log(n/\delta)$ grows with $\delta$ for $\delta < n/e$.

**Hardness.** Kempa and Prezza proved that deciding whether $\gamma(T) \le p$ is NP-complete. A smallest attractor of a short string can be found by trying sets in order of size, and the greedy hitting-set rule gives a logarithmic approximation; in practice $\gamma$ itself is rarely computed, and the measures $\delta$, $z$ and $r$, which take linear or near-linear time, stand in for it.

**Not monotone.** Unlike $z$, $\gamma$ can decrease when a letter is appended: $\gamma(\texttt{aababba}) = 3$ but $\gamma(\texttt{aababbab}) = 2$, with attractor $\{1, 5\}$.

## Examples

**`banana`.** Three letters occur, so $\gamma \ge 3$, and $\Gamma = \{0, 2, 3\}$ is an attractor. Each of the 15 distinct substrings has an occurrence crossing a position of $\Gamma$:

| substrings | occurrence used | position hit |
| --- | --- | --- |
| `b`, `ba`, `ban`, `bana`, `banan`, `banana` | starting at 0 | 0 |
| `n`, `na`, `nan`, `nana` | starting at 2 | 2 |
| `a` | at 3 | 3 |
| `an`, `ana`, `anan`, `anana` | starting at 1 | 2 |

So $\gamma(\texttt{banana}) = 3$. The LZ77 phrases are `b`, `a`, `n`, `ana`, giving $z = 4$ and the attractor $\{0, 1, 2, 5\}$. Here $\delta = 3$, from $d_1 = 3$.

**More values.** The following were computed by exhaustive search over all position sets.

| string | $n$ | $\delta$ | $\gamma$ | a smallest attractor | $z$ |
| --- | --- | --- | --- | --- | --- |
| `aababb` | 6 | 2 | 3 | $\{0, 2, 4\}$ | 5 |
| `abracadabra` | 11 | 5 | 5 | $\{0, 1, 2, 4, 6\}$ | 8 |
| `mississippi` | 11 | 4 | 4 | $\{0, 5, 7, 9\}$ | 8 |
| `abaababaabaab` | 13 | 2 | 2 | $\{4, 7\}$ | 6 |

In `aababb` the counts $d_k$ for $k = 1, \ldots, 6$ are $2, 4, 4, 3, 2, 1$, so $\delta = 2$ while $\gamma = 3$: the lower bound $\delta$ is not always attained. It is the shortest binary example.

**Sturmian words.** The last row is a prefix of the [Fibonacci word](/fibonacci-word/). Every prefix of the Fibonacci word of length 2 to 40 has $\gamma = 2$, by exhaustive search, and Mantaci, Restivo, Romana, Rosone and Sciortino showed that every standard [Sturmian word](/sturmian-word/) has a smallest attractor of size 2. Two positions suffice although the number of LZ77 phrases grows like $\log n$.

**Thue-Morse prefixes.** For the prefixes of the [Thue-Morse word](/thue-morse-word/) $abbabaab\cdots$, exhaustive search gives $\gamma = 2$ for lengths 2 to 6, $3$ for 7 to 14, $4$ for 15 and 16, $3$ for 17 to 24, and $4$ for every length from 25 to 60. The drop from 16 to 17 is another case of non-monotonicity.

**Worst cases.** Among all binary strings of length $n$, the largest $\gamma$ is $1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4$ for $n = 1, \ldots, 12$, and among ternary strings it is $1, 2, 3, 3, 3, 4, 4, 4$ for $n = 1, \ldots, 8$. A unary string has $\gamma = 1$.

**Checks.** For all strings of length at most 10 over one letter, at most 12 over two letters and at most 8 over three letters, a script computed $\gamma$ by brute force and confirmed $\delta \le \gamma \le z$, the letter-count bound, and that the LZ77 phrase ends form an attractor.

## Where it is used

- **Comparing compressors.** Attractors give a common lower bound for dictionary compressors (LZ77, grammars, macro schemes, run-length BWT), so bounds proved in terms of $\gamma$ or $\delta$ apply to all of them, and conversions between the representations cost at most logarithmic factors.
- **Universal compressed indexes.** Kempa and Prezza built, from any given attractor of size $\gamma'$, a data structure of $O(\gamma' \log(n/\gamma'))$ words that gives random access to the text in $O(\log(n/\gamma'))$ time, and Navarro and Prezza gave indexes for pattern search in comparable space. Structures such as the [r-index](/r-index/), of size $O(r)$, and [grammar](/smallest-grammar-problem/)-based indexes fit this framework.
- **Combinatorics on words.** Attractor sizes have been computed for Sturmian, Thue-Morse, period-doubling and other automatic sequences, often by automated proofs, and $\gamma$ joins [subword complexity](/subword-complexity/) and [run-length encoding](/run-length-encoding/) among the simple descriptive measures of a word.
- **Repetitiveness measures.** The measure $\delta$, introduced as a lower bound for $\gamma$, turned out to be computable in linear time, monotone, and within a logarithmic factor of every compressor, and it is now the reference measure for highly repetitive collections such as genome databases and versioned documents.

## References
