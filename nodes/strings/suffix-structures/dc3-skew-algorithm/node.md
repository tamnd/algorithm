---
tag: M5ZHTB
kind: algorithm
slug: dc3-skew-algorithm
name: DC3 (skew) algorithm
aliases:
- skew algorithm
- Kärkkäinen-Sanders algorithm
area: strings/suffix-structures
level: advanced
summary: Linear-time suffix array construction by recursing on the suffixes at positions not divisible by 3.
solves: [suffix-array-construction]
model: word-ram
complexity:
  vars: {n: the length of the text}
  time: {best: Θ(n), average: Θ(n), worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: true}
history:
  year: 2003
  people: [Juha Kärkkäinen, Peter Sanders, Stefan Burkhardt]
  note: Kärkkäinen and Sanders gave the algorithm at ICALP 2003; the journal version with Burkhardt appeared in the Journal of the ACM in 2006.
prereqs: [suffix-array, radix-sort, master-theorem]
see_also: [sa-is, farach-algorithm, prefix-doubling, larsson-sadakane-algorithm, karp-miller-rosenberg-algorithm, suffix-array-construction, kasai-algorithm, counting-sort]
sources:
  - paper: doi:10.1007/3-540-45061-0_73
    title: Juha Kärkkäinen and Peter Sanders, Simple linear work suffix array construction, ICALP 2003, LNCS 2719
    locator: pages 943 to 955, the skew algorithm with the sample of positions not divisible by 3
  - paper: doi:10.1145/1217856.1217858
    title: Juha Kärkkäinen, Peter Sanders and Stefan Burkhardt, Linear work suffix array construction, Journal of the ACM 53(6), 2006
    locator: pages 918 to 936, the DC3 algorithm, its C++ code, the difference cover generalization and the parallel and external memory versions
  - paper: doi:10.1145/1242471.1242472
    title: Simon J. Puglisi, William F. Smyth and Andrew H. Turpin, A taxonomy of suffix array construction algorithms, ACM Computing Surveys 39(2), 2007
    locator: the section on recursive algorithms, with KS and its practical speed compared with other methods
---

The DC3 algorithm, also called the skew algorithm, builds the [suffix array](/suffix-array/) of a text of length $n$ over an integer alphabet in $\Theta(n)$ time. It sorts the suffixes that start at positions not divisible by 3 by one recursive call on a string of about $2n/3$ symbols, sorts the other suffixes with one [radix sort](/radix-sort/) pass, and merges the two lists. It was the first linear-time [suffix array construction](/suffix-array-construction/) that is short enough to write as a page of code, and it adapts well to parallel and external memory models.

## In plain words

Two endings of a long text can share a long start, which makes sorting them slow. DC3 splits the endings into two teams. The big team holds two out of every three endings. Cut the text into blocks of three letters, give each distinct block a number, and write the big team as a shorter text of block numbers. Sorting the endings of this shorter text sorts the big team, and the same method does it, on a text two thirds as long.

The small team holds the other endings. Each of them is one letter followed by an ending of the big team, whose place is now known. So one quick sort by two keys puts the small team in order.

Last, merge the two teams. To compare endings from different teams, look at one or two letters, then at the places of two big-team endings.

## The problem

Given a text $T = T[0 \ldots n-1]$, compute its suffix array $SA$: the start positions of the suffixes $T_i = T[i \ldots n-1]$ in increasing lexicographic order. Positions are 0-based.

**Alphabet.** The core algorithm needs an integer alphabet: symbols $1, \ldots, K$ with $K = O(n)$, so that counting sort runs in $O(n)$ time. A general ordered alphabet is first mapped to $1, \ldots, \sigma$ by sorting the distinct symbols, in $O(n \log \sigma)$ time.

**End of text.** Three copies of the symbol 0 are appended after $T$ as padding, so that every triple $T[i \ldots i+2]$ with $i < n$ is defined. They act as end markers smaller than all symbols, but they are not part of the output: no sentinel suffix is listed, and a proper prefix sorts before the longer suffix.

## The algorithm

Let $n_0 = \lceil n/3 \rceil$, $n_1 = \lfloor (n+1)/3 \rfloor$ and $n_2 = \lfloor n/3 \rfloor$ be the numbers of positions $i < n$ with $i \bmod 3 = 0$, $1$ and $2$. The *sample* $B_{12}$ is the set of positions with $i \bmod 3 \ne 0$. When $n \bmod 3 = 1$, the sample also gets the dummy position $n$, whose suffix is empty; its triple is $(0, 0, 0)$.

```pseudo id=main
DC3(T, n, K)                              ▷ T[0..n−1] in 1..K, T[n..n+2] = 0
L1  if n ≤ 1 then return [0 .. n−1]; B12 ← positions i < n + (n0 − n1) with i mod 3 ≠ 0
L2  radix sort B12 by the triples (T[i], T[i+1], T[i+2]), in three counting-sort passes
L3  name each triple by its rank among the distinct triples, from 1
L4  if two sample positions have the same name then
L5      R ← names of the positions ≡ 1 in order, then names of the positions ≡ 2 in order
L6      SA_R ← DC3(R, n0 + n2, number of names); rank(i) ← rank of the suffix of R for i
L7  else rank(i) ← name(i)
L8  B0 ← positions i ≡ 0, sorted by (T[i], rank(i+1)) with one counting sort of the sorted B12
L9  merge B12 and B0: for j ≡ 1 compare (T[i], rank(i+1)); for j ≡ 2 compare (T[i], T[i+1], rank(i+2))
L10 return the merged list, without the dummy
```

**Why the reduced string works (L5).** The name of $i$ stands for the triple $T[i \ldots i+2]$, and the names keep the order of the triples. So the run of names $name(i)\,name(i+3)\,name(i+6) \cdots$ spells $T_i$ three symbols at a time, and comparing such runs is comparing suffixes. In $R$, the run of a position $\equiv 1$ is followed by the runs of the positions $\equiv 2$, but the comparison never reaches them: the last triple of the first half contains a 0 that ends it. This is why the dummy is needed when $n \bmod 3 = 1$: without it, the last position $\equiv 1$ would be $n - 3$, whose triple has no 0.

**Why ranks of the sample are enough (L8, L9).** For $i \equiv 0$, $T_i$ is $T[i]$ followed by $T_{i+1}$, and $i + 1$ is in the sample. When a position $i \equiv 0$ is compared with $j \equiv 1$, both $i + 1$ and $j + 1$ are in the sample. When it is compared with $j \equiv 2$, one step is not enough, since $j + 1 \equiv 0$, but $i + 2$ and $j + 2$ are both in the sample. So every comparison needs at most two symbols and one rank. A position beyond the end has rank 0, the rank of the empty suffix.

**Why 3.** The sample must have two properties: for any $i$ and $j$, some $\ell < 3$ puts both $i + \ell$ and $j + \ell$ in the sample, and the sample must be a constant fraction smaller than $n$. The set $\{1, 2\}$ is a *difference cover* modulo 3: every difference modulo 3 is a difference of two of its members. With the residues 0 and 1 modulo 2 this is impossible, which is why [Farach's algorithm](/farach-algorithm/), which splits into odd and even positions, needs a much harder merge.

## Example

The text is $T = \texttt{yabbadabbado}$, $n = 12$. The symbols map to $\texttt{a} = 1$, $\texttt{b} = 2$, $\texttt{d} = 3$, $\texttt{o} = 4$, $\texttt{y} = 5$, so $T = 5, 1, 2, 2, 1, 3, 1, 2, 2, 1, 3, 4$ and $K = 5$. Here $n_0 = n_1 = n_2 = 4$, so there is no dummy.

**L1 to L3.** The sample positions, their triples and their names (the triples sorted are `abb`, `ada`, `bad`, `bba`, `dab`, `do0`, `o00`):

| position | 1 | 4 | 7 | 10 | 2 | 5 | 8 | 11 |
|---|---|---|---|---|---|---|---|---|
| triple | abb | ada | bba | do0 | bba | dab | bad | o00 |
| name | 1 | 2 | 4 | 6 | 4 | 5 | 3 | 7 |

**L4 to L6.** The name 4 occurs twice (positions 7 and 2), so the algorithm recurses on $R = 1, 2, 4, 6, 4, 5, 3, 7$ of length 8 with 7 names. The recursive call returns $SA_R = [0, 1, 6, 4, 2, 5, 3, 7]$. Index $x < 4$ of $R$ stands for position $3x + 1$ and index $x \ge 4$ for position $3(x - 4) + 2$, so the sorted sample is

| rank | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| position | 1 | 4 | 8 | 2 | 7 | 5 | 10 | 11 |
| suffix | abbadabbado | adabbado | bado | bbadabbado | bbado | dabbado | do | o |

The tie between 7 and 2 is broken by the next triples: `bba` then `do0` for position 7, `bba` then `dab` for position 2, and `dab` < `do0`.

**L8.** The positions $\equiv 0$ are 0, 3, 6 and 9, with the keys $(\texttt{y}, rank(1)) = (5, 1)$, $(\texttt{b}, rank(4)) = (2, 2)$, $(\texttt{a}, rank(7)) = (1, 5)$ and $(\texttt{a}, rank(10)) = (1, 7)$. So $B_0$ in order is 6, 9, 3, 0.

**L9.** The merge compares, for example, 6 with 4 ($4 \equiv 1$): $(\texttt{a}, rank(7)) = (1, 5)$ against $(\texttt{a}, rank(5)) = (1, 6)$, so 6 comes first. It compares 9 with 8 ($8 \equiv 2$): $(\texttt{a}, \texttt{d}, rank(11)) = (1, 3, 8)$ against $(\texttt{b}, \texttt{a}, rank(10)) = (2, 1, 7)$, so 9 comes first. The result is

$$SA = [1, 6, 4, 9, 3, 8, 2, 7, 5, 10, 11, 0].$$

## Correctness

The proof has four steps; the full proof is in the proof file of this page.

1. **Reduced string.** Comparing two suffixes of $R$ compares the runs of names, and so the triples, and so the padded suffixes of $T$. The 0 in the last triple of each half ends every comparison inside one half. So the suffix array of $R$ gives the order of the sample suffixes. If all names are already different, the first triple decides every comparison, and the names are the ranks.
2. **Non-sample suffixes.** $T_i = T[i]\,T_{i+1}$, and $rank(i+1)$ orders the suffixes $T_{i+1}$, so the pair $(T[i], rank(i+1))$ orders the suffixes $T_i$ with $i \equiv 0$. Line L8 sorts by this pair with one stable counting sort, since the positions $i + 1$ are taken in sample order.
3. **Merge.** By the choice of one or two leading symbols, the ranks in each comparison are of sample positions, or 0 beyond the end, and the pairs or triples compare as the suffixes do. Two different suffixes never give equal keys.
4. **Recursion.** $|R| = n_0 + n_2 < n$ for $n \ge 2$, so the recursion ends, and the claim follows by induction on $n$.

## Complexity

| case | time | extra space |
|---|---|---|
| integer alphabet, $K = O(n)$ | $\Theta(n)$ in every case | $\Theta(n)$ words |
| general ordered alphabet | $O(n \log \sigma)$ to rank the symbols, then $\Theta(n)$ | $\Theta(n)$ words |

**Time.** Without the recursive call, each line is a scan or a counting sort with $O(n + K)$ buckets, and in the recursive call the alphabet is the set of names, of size at most $|R|$. The reduced string has length $n_0 + n_2 \le \lceil 2n/3 \rceil + 1$. So the time is $t(n) = t(2n/3 + O(1)) + O(n)$, and by the [master theorem](/master-theorem/) $t(n) = O(n)$: the sizes form a geometric series $n + 2n/3 + 4n/9 + \cdots \le 3n$.

**Recursion depth.** $O(\log_{3/2} n)$ levels. On a text with all symbols different, no level recurses; on $\texttt{a}^n$, every level does, since all inner triples are equal.

**Space.** The text, the names, the reduced string, the sorted sample and the output take a constant number of arrays of $n$ integers at the top level, and two thirds of that at each lower level. This is more than [SA-IS](/sa-is/) needs in practice.

## Properties

- **Not adaptive.** The work is $\Theta(n)$ on every input; only the number of levels changes with the text.
- **Not comparison based.** It sorts integer keys with counting sort; symbols are compared only when they are first ranked.
- **Recursive.** One recursive call per level on a string two thirds as long.
- **Simple parts.** Every step is a counting sort, a scan or a merge, which is why it carries over to parallel machines and external memory with good bounds.
- **Output.** The sample ranks of the top level are thrown away; the inverse suffix array is not a by-product, and [Kasai's algorithm](/kasai-algorithm/) must build it to get the LCP array.

## Variants and improvements

- **Difference covers.** DC3 uses the difference cover $\{1, 2\}$ modulo 3. Any difference cover $D$ modulo $v$ works: the sample is the positions with $i \bmod v \in D$, and the merge compares at most $v$ symbols and one rank. Larger $v$ gives a smaller sample, with $|D| = O(\sqrt{v})$, which trades time for space; Kärkkäinen, Sanders and Burkhardt call the general method DC$v$.
- **Parallel and external memory.** The journal paper gives versions for the PRAM, the BSP model and external memory, all built from sorting and scanning.
- **LCP array.** The algorithm can be extended to compute the LCP array during the merge, with range minimum queries on the LCP values of the sample; most programs instead run [Kasai's algorithm](/kasai-algorithm/) afterwards.
- **Farach's algorithm.** [Farach's algorithm](/farach-algorithm/) of 1997 builds the suffix tree in linear time by recursing on the odd positions, and merges the odd and even trees; DC3 replaces that merge with a simple comparison.
- **SA-IS.** [SA-IS](/sa-is/) also recurses on a reduced string of at most $n/2$ symbols, with induced sorting instead of a merge; it is faster and uses less memory, and has mostly replaced DC3 in practice.

## When to use it

Use DC3 when a guaranteed linear time matters and a short, clear program is wanted, for teaching, or as the base of a parallel or external memory suffix sort. For the fastest sequential construction in practice, use [SA-IS](/sa-is/) or a tuned library. For a short program on small inputs, [prefix doubling](/prefix-doubling/) or the [Larsson-Sadakane algorithm](/larsson-sadakane-algorithm/) is simpler still.

## Pitfalls

- **The dummy for $n \bmod 3 = 1$.** Without the dummy position $n$, the last triple of the first half of $R$ has no 0, and a comparison can run into the second half and give the wrong order. The dummy must then be skipped when the sample is merged.
- **Padding.** The text needs three trailing zeros, and the rank array needs zero entries beyond the sample, so that $rank(i+1)$ and $rank(i+2)$ are 0 for positions at or past the end.
- **Symbols must be at least 1.** The value 0 is the end marker; a text that contains 0 must first be shifted.
- **Index maps.** Index $x$ of $R$ maps to $3x + 1$ for $x < n_0$ and to $3(x - n_0) + 2$ otherwise. Using $n_1$ in place of $n_0$ breaks the case with the dummy.
- **Radix sort order.** The three counting-sort passes must use the last symbol of the triple first, and each must be stable.
- **Deep recursion.** The depth is only $O(\log n)$, but each level holds its arrays until it returns; a recursive program is fine, but its peak memory is the sum over the levels.

## Implementations

The Python module maps the symbols to $1, \ldots, \sigma$, appends three zeros and calls the recursive core, whose depth is $O(\log n)$. Counting sorts are done by a helper that sorts a list of positions by the symbol at a fixed offset. The tests compare the result with sorting all suffixes, on random strings over alphabets of size 1, 2 and 4, on the empty string, on $\texttt{a}^n$ and on $(\texttt{ab})^n$.

## History

In 2003, Juha Kärkkäinen and Peter Sanders presented "Simple linear work suffix array construction" at ICALP. Three groups found linear-time direct suffix array constructions that year: Kärkkäinen and Sanders, Kim, Sim, Park and Park, and Ko and Aluru. The skew algorithm was the simplest of them. It takes the recursion on a fraction of the positions from [Farach's](/farach-algorithm/) suffix tree algorithm of 1997, but chooses two thirds of the positions so that the merge is easy. The journal version, "Linear work suffix array construction", with Stefan Burkhardt, appeared in the Journal of the ACM in 2006 and added the difference cover generalization and the parallel and external memory versions.

## References
