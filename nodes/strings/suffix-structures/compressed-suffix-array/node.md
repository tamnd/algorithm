---
tag: M2B1RW
kind: data-structure
slug: compressed-suffix-array
name: Compressed suffix array
aliases:
- CSA
area: strings/suffix-structures
level: research
summary: A suffix array stored in space close to the compressed text size, with fast search.
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, σ: the alphabet size, s: the sampling step of the suffix array, k: the number of occurrences}
  time: {worst: O(m log n + k s)}
  space: {extra: O(n log σ / log n + n / s)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [suffix-array, elias-gamma-coding, succinct-data-structures]
see_also: [fm-index, compressed-suffix-tree, r-index, full-text-index, suffix-array-search, burrows-wheeler-transform, compressed-indexing, elias-gamma-coding]
sources:
  - paper: doi:10.1145/335305.335351
    title: Roberto Grossi and Jeffrey Scott Vitter, Compressed suffix arrays and suffix trees with applications to text indexing and string matching, STOC 2000
    locator: pages 397 to 406, the recursive decomposition of the suffix array with the neighbor function
  - paper: doi:10.1137/S0097539702402354
    title: Roberto Grossi and Jeffrey Scott Vitter, Compressed suffix arrays and suffix trees with applications to text indexing and string matching, SIAM Journal on Computing 35(2), 2005
    locator: pages 378 to 407, the journal version with the space and lookup time trade-offs
  - paper: doi:10.1016/S0196-6774(03)00087-7
    title: Kunihiko Sadakane, New text indexing functionalities of the compressed suffix arrays, Journal of Algorithms 48(2), 2003
    locator: pages 294 to 313, the self-index that stores only the Psi function, the first symbols and samples, with search and extraction
  - paper: doi:10.1145/1216370.1216372
    title: Gonzalo Navarro and Veli Mäkinen, Compressed full-text indexes, ACM Computing Surveys 39(1), 2007
    locator: the sections on the Psi function, its compressibility and the Sadakane and Grossi-Vitter indexes
---

A compressed suffix array (CSA) stores the [suffix array](/suffix-array/) of a text in space near the size of the compressed text, and still gives the value $SA[i]$, the inverse, and pattern search. Its core is the function $\Psi$, which maps the rank of each suffix to the rank of the suffix one position later. $\Psi$ is increasing on the block of suffixes that start with one symbol, so its gaps are small and compress well with codes such as [Elias gamma](/elias-gamma-coding/). Grossi and Vitter introduced the CSA in 2000, and Sadakane turned it into a self-index that also replaces the text; it is the twin of the [FM-index](/fm-index/), whose LF mapping is the inverse of $\Psi$.

## In plain words

A suffix array lists the endings of a text in sorted order, with one large number per ending. That is many times the size of the text.

Take a row of the list and remove the first letter of its ending: what is left is another ending, at another row. Write down that row number for each row. For the rows whose endings start with the same letter, these numbers go up in order. So you can store the small steps between them in place of the large numbers.

From these numbers and the first letter of each row you can spell out any ending, letter by letter. That is enough to search for a word by binary search. To get the position of an ending in the text, keep the positions of a few rows and step through the numbers until you reach one of them.

## The abstract type

The structure is static. It is built once from a text $T$ and supports:

- `lookup(i)`: the value $SA[i]$;
- `inverse(p)`: the rank of the suffix that starts at $p$;
- `find(P)`: the range of ranks of the suffixes that start with $P$, so `count` is its size;
- `locate(P)`: the positions of the occurrences, by `lookup` on that range;
- `extract(l, r)`: the substring $T[l \ldots r-1]$, so the text need not be kept.

## Representation

The text $T = T[0 \ldots n-1]$ is over a general ordered alphabet of $\sigma$ symbols, coded $1, \ldots, \sigma$. A sentinel $\$$ with code 0, unique and smallest, is appended, so $T' = T\$$ has $n + 1$ positions and the rows are $0, \ldots, n$, all 0-based. $SA$ is the suffix array of $T'$, $SA[0] = n$, and $ISA$ is its inverse.

**The $\Psi$ function.** $\Psi(i) = ISA[(SA[i] + 1) \bmod (n + 1)]$: the row of the suffix one position after the suffix of row $i$. Following $\Psi$ from row $i$ reads the suffix $T'_{SA[i]}$ one symbol at a time.

**The first symbol.** $F(i) = T'[SA[i]]$. The rows with $F(i) = c$ form the block $C[c], \ldots, C[c+1] - 1$, where $C[c]$ counts the symbols smaller than $c$. Within a block, $\Psi$ is increasing: two suffixes $cX < cY$ have $X < Y$.

**Stored data.** The implementation follows Sadakane:

- the sequence $V(i) = F(i)(n + 1) + \Psi(i)$, which is strictly increasing over all rows, stored as an absolute value every $b$ rows and as gamma-coded gaps $V(i) - V(i-1)$ in between, so both $\Psi(i) = V(i) \bmod (n + 1)$ and $F(i) = \lfloor V(i) / (n + 1) \rfloor$ come from one decode;
- $SA[i]$ for the rows whose position is a multiple of $s$ or equal to $n$;
- $ISA[p]$ for the positions $p$ that are multiples of $s$.

**Space.** The gaps in the block of $c$ add up to at most $n + 1$, and there are about $n_c$ of them, where $n_c$ is the number of $c$ in $T$. Gamma codes of such gaps take about $2 n_c \log_2((n + 1)/n_c)$ binary digits, so $\Psi$ takes $O(n H_0 + n)$ binary digits, where $H_0 \le \log_2 \sigma$ is the zero-order [entropy](/shannon-entropy/) of $T$. Sadakane's encoding reaches about $n H_0 + O(n \log \log \sigma)$. The samples add about $2(n/s)$ words, and the block samples $n/b$ words.

## Operations

```pseudo id=main
CSA-LOOKUP(i)                             ▷ returns SA[i]
L1  t ← 0
L2  while SA[i] is not sampled do
L3      i ← Ψ(i); t ← t + 1
L4  return SA[i] − t
COMPARE(i, P)                             ▷ the suffix of row i against P, on |P| symbols
L5  for each symbol x of P do
L6      if F(i) ≠ x then return the sign of F(i) − x
L7      i ← Ψ(i)
CSA-FIND(P)                               ▷ returns the rows [lo, hi) of the suffixes that start with P
L8  lo ← first row with COMPARE(row, P) ≥ 0, by binary search on 0 .. n
L9  hi ← first row with COMPARE(row, P) > 0, by binary search on lo .. n
L10 return [lo, hi)
```

**Lookup.** Each $\Psi$ step moves the position one to the right. Within at most $s - 1$ steps the position reaches a multiple of $s$ or $n$, both sampled, and then $SA[i] = SA[\Psi^t(i)] - t$.

**Inverse and extract.** `inverse(p)` starts at the sampled row of $\lfloor p/s \rfloor s$ and applies $\Psi$ $p \bmod s$ times. `extract(l, r)` takes $i = $ `inverse(l)` and then outputs $F(i)$ and moves to $\Psi(i)$, $r - l$ times.

**Search.** The suffix array is sorted, so the rows that start with $P$ form one range, and two binary searches find it, as in [suffix array search](/suffix-array-search/). Each comparison reads up to $m$ symbols of a suffix with $F$ and $\Psi$, never with the text.

## Example

The text is $T = \texttt{banana}$, so $T' = \texttt{banana\$}$, $n = 6$, with $s = 2$ and $b = 4$.

| row $i$ | $SA[i]$ | suffix | $F(i)$ | $\Psi(i)$ | $V(i) = 7F(i) + \Psi(i)$ |
|---|---|---|---|---|---|
| 0 | 6 | \$ | \$ (0) | 4 | 4 |
| 1 | 5 | a\$ | a (1) | 0 | 7 |
| 2 | 3 | ana\$ | a (1) | 5 | 12 |
| 3 | 1 | anana\$ | a (1) | 6 | 13 |
| 4 | 0 | banana\$ | b (2) | 3 | 17 |
| 5 | 4 | na\$ | n (3) | 1 | 22 |
| 6 | 2 | nana\$ | n (3) | 2 | 23 |

In the block of `a` (rows 1 to 3), $\Psi$ is $0, 5, 6$, increasing; in the block of `n` (rows 5 and 6) it is $1, 2$. The stored values are $V(0) = 4$ and $V(4) = 17$ as block samples and the gaps $3, 5, 1$ and $5, 1$ in gamma code, 15 binary digits in all. The sampled positions are 0, 2, 4 and 6, at the rows 4, 6, 5 and 0.

**Lookup of row 2.** Row 2 has position 3, which is not sampled. $\Psi(2) = 5$, and row 5 holds the sampled position 4, so $SA[2] = 4 - 1 = 3$.

**Search for `ana`.** At row 3, COMPARE reads $F(3) = \texttt{a}$, $\Psi(3) = 6$, $F(6) = \texttt{n}$, $\Psi(6) = 2$, $F(2) = \texttt{a}$: the suffix starts with `ana`. Row 1 reads `a`, then $F(\Psi(1)) = F(0) = \$ < \texttt{n}$, so it is smaller, and row 4 starts with `b`, larger. The two binary searches give the rows $[2, 4)$, and lookup gives the positions 3 and 1.

## Correctness

The full proof is in the proof file of this page. The key facts are:

1. **$\Psi$ reads suffixes.** $SA[\Psi(i)] = SA[i] + 1$ for $SA[i] < n$, so $F(i), F(\Psi(i)), F(\Psi^2(i)), \ldots$ spell $T'_{SA[i]}$.
2. **Monotone blocks.** For $i < j$ in the block of $c$, $T'_{SA[i]} = cX < cY = T'_{SA[j]}$ implies $X < Y$, so $\Psi(i) < \Psi(j)$. Hence $V$ is strictly increasing and its gaps are positive, as the gamma code needs.
3. **Lookup and search.** The lookup loop keeps $SA[i_{\text{start}}] = SA[i] + t$ and stops within $s - 1$ steps. COMPARE is a lexicographic comparison of a prefix of the suffix with $P$, and the binary searches are correct because the suffixes are sorted.

## Complexity

| operation | time with $\Psi$ in $O(1)$ | time in the implementation |
|---|---|---|
| $\Psi(i)$, $F(i)$ | $O(1)$ | $O(b)$ gamma decodes |
| `lookup(i)` | $O(s)$ | $O(s b)$ |
| `inverse(p)` | $O(s)$ | $O(s b)$ |
| `find(P)` | $O(m \log n)$ | $O(m b \log n)$ |
| `locate(P)` | $O(m \log n + k s)$ | $O((m \log n + k s) b)$ |
| `extract(l, r)` | $O(s + r - l)$ | $O((s + r - l) b)$ |

Constant-time $\Psi$ needs a table that decodes many short codes at once, or a compressed bit vector with constant-time select. The build in the implementation sorts the suffixes by prefix doubling in $O(n \log^2 n)$ time with $\Theta(n)$ words; Hon, Sadakane and Sung showed how to build the CSA directly in small space.

**Space trade-offs.** The parameter $s$ trades $n/s$ words of samples against the $s$ steps per lookup; $b$ trades the block samples against the decode time. Grossi and Vitter obtained $O(n \log \sigma)$ binary digits with lookup in $O(\log^\epsilon n)$ time for any fixed $\epsilon > 0$, by storing $\Psi$ at several levels of a recursive decomposition of $SA$.

## Variants

- **Grossi-Vitter.** The original CSA halves the suffix array level by level: it keeps the even values, marks them, and stores $\Psi$ for the odd rows, so $SA[i]$ is found by recursion through the levels. This is an index, not a self-index: it needs the text for search.
- **Sadakane's CSA.** Stores $\Psi$, the block boundaries and samples, and searches without the text, as here; it also supports the operations needed for a [compressed suffix tree](/compressed-suffix-tree/).
- **High-order entropy.** Grossi, Gupta and Vitter split $\Psi$ by the context of $k$ symbols before each suffix and reached space near $n H_k$ binary digits.
- **Backward search on $\Psi$.** The range of $cP$ can be found from the range of $P$ by two binary searches for $\Psi$ values inside the block of $c$, which gives $O(m \log n)$ search, like the [FM-index](/fm-index/) but with $\Psi$ in place of LF.
- **Repetitive text.** For collections with many repeats, $\Psi$ has long runs of consecutive values, and run-length codes of $\Psi$, or the [r-index](/r-index/), use space in the number of runs.

## When to use it

Use a CSA when a suffix array is needed but does not fit in memory, especially when the suffix tree functions are also wanted through a compressed suffix tree. Its $\Psi$ function gives fast forward extraction of the text, which suits extracting snippets. For counting alone, an [FM-index](/fm-index/) with a wavelet tree is usually faster. For a text that fits in memory with its suffix array, the plain suffix array is simpler and much faster.

## Pitfalls

- **The sentinel and the wrap.** $\Psi$ of the last suffix wraps to the row of position 0. Without a sampled position $n$, a lookup loop can pass from $n$ to 0 and count wrong.
- **Gaps that are zero or negative.** Gamma codes need positive integers. Gaps of $\Psi$ alone are negative at the block borders; adding $F(i)(n + 1)$, or storing the block borders separately, avoids this.
- **Bit order.** A gamma code read from the low end of a word must be written so that its leading 1 comes right after the zeros. Writing the binary digits in the usual order makes a trailing zero look like part of the next code.
- **Comparisons with the sentinel.** The sentinel is smaller than all symbols, so a suffix that ends inside $P$ compares as smaller; it is never equal to $P$.

## Implementations

The Python class stores $V$ as block samples and gamma-coded gaps in one Python integer, with the two samples in dictionaries and a list. The tests compare $\Psi$, `lookup`, `inverse` and `extract` with a suffix array built by sorting all suffixes, and `locate` with a scan of the text, on random strings over alphabets of size 1, 2 and 4 and on $\texttt{a}^n$ and $(\texttt{ab})^n$.

## History

Grossi and Vitter introduced compressed suffix arrays at STOC 2000; their structure stored $\Psi$ and recursive samples, and the journal version appeared in the SIAM Journal on Computing in 2005. In the same year, Ferragina and Manzini introduced the FM-index. Sadakane showed in 2000, and in the Journal of Algorithms in 2003, that $\Psi$ and the first symbols suffice to search without the text, which made the CSA a self-index, and later built compressed suffix trees on it. Grossi, Gupta and Vitter in 2003 reached space bounded by the high-order entropy.

## References
