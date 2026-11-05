---
tag: PG9DBY
kind: abstract-type
slug: full-text-index
name: Full-text index
aliases:
- Text index
- full-text index
- string index
- substring index
- text index
area: strings/suffix-structures
level: intro
summary: Preprocesses a text so that any pattern's occurrences can be found quickly.
prereqs: [string-matching, alphabet, asymptotic-notation]
see_also: [suffix-array, suffix-tree, suffix-automaton, fm-index, compressed-suffix-array, r-index, inverted-index, keyword-in-context-search]
sources:
  - paper: doi:10.1145/1216370.1216372
    title: Gonzalo Navarro and Veli Mäkinen, Compressed full-text indexes, ACM Computing Surveys 39(1), 2007
    locator: Sections 1 to 3 (the count, locate and extract queries, self-indexes, and the classical suffix tree and suffix array indexes)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 5 (suffix trees and exact matching with a preprocessed text) and Chapter 7 (the first applications, and suffix arrays)
  - paper: doi:10.1137/0222058
    title: Udi Manber and Gene Myers, Suffix arrays, a new method for on-line string searches, SIAM Journal on Computing 22(5), 1993
    locator: pages 935 to 948, the search in O(m + log n) time with LCP information
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, Cambridge University Press, 2016
    locator: Chapter 11 (Texts), compressed suffix arrays, the FM-index and compressed suffix trees
---

A full-text index is an abstract data type that holds a fixed text $T$ over an [alphabet](/alphabet/) and answers, for any pattern $P$ given later, how often $P$ occurs in $T$ and where. It turns [string matching](/string-matching/) into a two-phase task: build the index once in time that depends on $T$, then answer each query in time that depends on $|P|$ and on the number of answers, not on $|T|$. The [suffix tree](/suffix-tree/), the [suffix array](/suffix-array/) and the [FM-index](/fm-index/) are its standard implementations. Unlike a word-based [inverted index](/inverted-index/), a full-text index finds any substring, so it also works for DNA, for program code and for languages without spaces.

## In plain words

Think of a very long text that does not change, such as a genome or a book. Many people will search it, each with a different short word. Reading the whole text for each search is slow. A full-text index reads the text once and builds a helper structure. After that, a search for a word looks only at the helper structure and at a few places in the text.

The type says which questions you can ask: does the word occur, how many times, and at which positions. Some indexes can also give back any piece of the text, so you can throw the text away and keep only the index. The type does not say how the helper structure looks. A suffix tree, a sorted list of all text endings, or a compressed form of that list can all play this role, at different speeds and sizes.

## Operations

The text is $T = T[0] T[1] \cdots T[n-1]$ over an alphabet $\Sigma$ of size $\sigma$, with 0-based positions. The pattern is $P = P[0 \ldots m-1]$. The set of occurrences is

$$\mathrm{Occ}(T, P) = \{\, i \in \mathbb{Z} : 0 \le i \le n - m \text{ and } T[i \ldots i+m-1] = P \,\},$$

and $occ = |\mathrm{Occ}(T, P)|$. Occurrences can overlap: $\mathrm{Occ}(\texttt{aaaa}, \texttt{aa}) = \{0, 1, 2\}$.

| operation | signature | what it returns |
|---|---|---|
| `build` | $T \to I$ | an index $I$ of the text $T$ |
| `contains` | $(I, P) \to$ bool | true when $P$ occurs in $T$ |
| `count` | $(I, P) \to \mathbb{N}$ | the number $occ$ of occurrences of $P$ |
| `locate` | $(I, P) \to$ set of positions | the set $\mathrm{Occ}(T, P)$, in any order |
| `extract` | $(I, i, j) \to$ string | the substring $T[i \ldots j-1]$, for $0 \le i \le j \le n$ (optional) |
| `length` | $I \to \mathbb{N}$ | the text length $n$ |

The index is static: there is no operation that changes $T$. An index that supports `extract` can replace the text, and is called a *self-index* (Navarro and Mäkinen, Section 3). The model of the alphabet matters for the costs below. The tables use a general ordered alphabet (symbols are only compared) unless they say otherwise.

## Laws

For each text $T$ of length $n$, each pattern $P$ of length $m$, and $I = \mathrm{build}(T)$:

1. $\mathrm{locate}(I, P) = \mathrm{Occ}(T, P)$.
2. $\mathrm{count}(I, P) = |\mathrm{locate}(I, P)|$.
3. $\mathrm{contains}(I, P) \iff \mathrm{count}(I, P) > 0$.
4. $\mathrm{extract}(I, i, j) = T[i \ldots j-1]$, and so $\mathrm{extract}(I, 0, \mathrm{length}(I)) = T$.
5. If $m > n$, then $\mathrm{count}(I, P) = 0$.
6. **Empty pattern.** $\mathrm{Occ}(T, \varepsilon) = \{0, 1, \ldots, n\}$, so $\mathrm{count}(I, \varepsilon) = n + 1$. An implementation can choose another value for the empty pattern, but it must say so.
7. **Prefix monotonicity.** If $P$ is a prefix of $P'$, then $\mathrm{Occ}(T, P') \subseteq \mathrm{Occ}(T, P)$, so $\mathrm{count}(I, P') \le \mathrm{count}(I, P)$.
8. **Substring closure.** If $P$ occurs in $T$, then each substring of $P$ occurs in $T$. So $\mathrm{contains}(I, P)$ implies $\mathrm{contains}(I, P')$ for each substring $P'$ of $P$.

Law 7 is the reason that the suffix-based indexes work: the suffixes of $T$ that start with $P'$ are among the suffixes that start with $P$, so the search narrows a set of suffixes as it reads the pattern. In a [suffix array](/suffix-array/) this set is one contiguous range of the sorted suffixes.

**Example.** Take $T = \texttt{abracadabra}$, so $n = 11$.

| pattern $P$ | $\mathrm{Occ}(T, P)$ | count |
|---|---|---|
| `abra` | $\{0, 7\}$ | 2 |
| `a` | $\{0, 3, 5, 7, 10\}$ | 5 |
| `bra` | $\{1, 8\}$ | 2 |
| `cad` | $\{4\}$ | 1 |
| `abrac` | $\{0\}$ | 1 |
| `x` | $\emptyset$ | 0 |
| the empty string | $\{0, 1, \ldots, 11\}$ | 12 |

The rows for `abra` and `abrac` show law 7. The suffix array of $T$ is $[10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2]$. The suffixes that start with `a` fill its first 5 entries, $\{10, 7, 0, 3, 5\}$. Those that start with `abra` are the entries 1 and 2, a sub-range of these.

## Implementations

Costs are worst case in the [word RAM](/word-ram/) with words of $\Theta(\log n)$ size, unless the row says otherwise. Space is in words, in addition to the text, unless the structure is a self-index. $H_k$ is the empirical entropy of order $k$ of $T$, and $r$ is the number of runs in the [Burrows-Wheeler transform](/burrows-wheeler-transform/) of $T$.

| structure | space | count$(P)$ | locate$(P)$ | build |
|---|---|---|---|---|
| scan with [KMP](/knuth-morris-pratt/), no index | none | $O(n + m)$ | $O(n + m)$ | none |
| [suffix trie](/suffix-trie/) | $\Theta(n^2)$ nodes in the worst case | $O(m \log \sigma)$ with sorted children | $O(m \log \sigma + occ)$ | $\Theta(n^2)$ |
| [suffix tree](/suffix-tree/) | $\Theta(n)$ | $O(m \log \sigma)$, or $O(m)$ with hashed children (expected) | $O(m \log \sigma + occ)$ | $O(n)$ for an integer alphabet ([Farach](/farach-algorithm/)) |
| [suffix array](/suffix-array/) | $n$ words | $O(m \log n)$ by [binary search](/suffix-array-search/) | $O(m \log n + occ)$ | $O(n)$ for an integer alphabet |
| suffix array with LCP information (Manber and Myers) | $3n$ words | $O(m + \log n)$ | $O(m + \log n + occ)$ | $O(n)$ for an integer alphabet |
| [enhanced suffix array](/enhanced-suffix-array/) | $O(n)$ | $O(m \sigma)$ | $O(m \sigma + occ)$ | $O(n)$ for an integer alphabet |
| [suffix automaton](/suffix-automaton/) | $O(n)$ | $O(m \log \sigma)$ with stored counts | $O(m \log \sigma + occ)$ with extra links | $O(n \log \sigma)$ |
| [FM-index](/fm-index/), a self-index | $n H_k + o(n \log \sigma)$ bits | $O(m \log \sigma)$ with a [wavelet tree](/wavelet-tree/) | $O((m + s \cdot occ) \log \sigma)$, with a sample of every $s$-th text position | $O(n)$ for an integer alphabet |
| [compressed suffix array](/compressed-suffix-array/), a self-index | close to $n H_0$ bits plus lower-order terms | $O(m \log n)$ | $O(m \log n + s \cdot occ)$ | $O(n \log n)$ or better |
| [r-index](/r-index/), a self-index | $O(r)$ words | close to $O(m)$ | close to $O(m + occ)$ | from the BWT |

The [suffix trie](/suffix-trie/) is the direct idea and is too big. The [suffix tree](/suffix-tree/) compacts it to linear size and gives the best query time, but each node needs several words, so it is many times larger than the text. The [suffix array](/suffix-array/) keeps only the leaf order of the suffix tree, in $n$ words. The compressed indexes ([FM-index](/fm-index/), [compressed suffix array](/compressed-suffix-array/), [r-index](/r-index/)) store the same information in space close to the size of the compressed text, and they replace the text. The [keyword-in-context search](/keyword-in-context-search/) problem is a typical client: it locates each occurrence and prints the text around it.

A word-based [inverted index](/inverted-index/) is a different type. It maps each word of a natural-language text to the list of its positions, and it can find only whole words or phrases of words.

## Lower bounds

- **Reading the pattern.** In a model where the index learns the symbols of $P$ only by reading them, and $\sigma \ge 2$, `contains` needs $m$ symbol reads in the worst case. Take $T = P$, so the answer is true. If the query for $P$ does not read $P[k]$, replace $P[k]$ by another symbol: the query reads the same symbols and gives the same answer, but the new pattern has length $n$ and differs from $T$, so the right answer is false. With $w$ symbols packed in a word, the bound is $\lceil m / w \rceil$ word reads.
- **Output.** `locate` writes $occ$ positions, so it needs $\Omega(occ)$ time. So $O(m + occ)$ is optimal for `locate` when $\sigma$ is a constant, and the suffix tree reaches it.
- **Space of a self-index.** There are $\sigma^n$ texts of length $n$, and a self-index must tell all of them apart, because `extract` returns $T$. So for some text it uses at least $\lceil n \log_2 \sigma \rceil$ bits. Compressed indexes go below this only for compressible texts, which is why their space is stated in terms of $H_k$ or $r$.

## References
