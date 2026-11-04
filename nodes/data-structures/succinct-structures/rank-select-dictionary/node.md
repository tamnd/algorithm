---
tag: P99JRP
kind: data-structure
slug: rank-select-dictionary
name: Rank/select dictionary
aliases:
- rank/select structure
- rank-select index
area: data-structures/succinct-structures
level: advanced
summary: A bit vector augmented with an o(n)-bit index that answers rank and select in constant time.
model: word-ram
complexity:
  vars: {n: the number of bits}
  time: {build: O(n), access: O(1), rank: O(1), select: O(1)}
  space: {total: n + O(n / log log n)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1996
  people: [David Clark, J. Ian Munro]
  note: Clark's thesis and Munro's paper Tables gave constant-time select on top of Jacobson's constant-time rank.
prereqs: [jacobson-rank, rank-select-problem, bit-vector]
see_also: [fully-indexable-dictionary, rrr-bitvector, sd-array, elias-fano-encoding, louds-tree, balanced-parentheses-representation, wavelet-tree, patrascu-succinct-lower-bound]
sources:
  - paper: "David Clark, Compact Pat Trees, PhD thesis, University of Waterloo, 1996"
    locator: the select structure with groups of lg^2 n ones, sparse groups stored in full and dense groups subdivided
  - paper: doi:10.1007/3-540-62034-6_35
    title: J. Ian Munro, Tables, 16th Conference on Foundations of Software Technology and Theoretical Computer Science (FSTTCS 1996), Lecture Notes in Computer Science 1180, 37-42
    locator: the constant-time select on the word RAM with o(n) extra bits
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 4, Sections 4.2.2 (rank in constant time) and 4.3 (Select), in particular 4.3.3 (Constant Time)
  - paper: doi:10.1137/1.9781611972870.6
    title: Daisuke Okanohara and Kunihiko Sadakane, Practical entropy-compressed rank/select dictionary, Ninth Workshop on Algorithm Engineering and Experiments (ALENEX 2007), 60-70
    locator: the darray, a practical select index with dense and sparse blocks, and the term rank/select dictionary
  - paper: doi:10.1016/j.tcs.2007.07.041
    title: Alexander Golynski, Optimal lower bounds for rank and select indexes, Theoretical Computer Science 387(3), 2007, 348-359
    locator: the lower bound Ω(n lg lg n / lg n) for the index, and a select index of (1 + o(1)) n lg lg n / lg n + O(n / lg n) bits
---

A rank/select dictionary is a static [bit vector](/bit-vector/) $B$ of $n$ bits together with an index of $o(n)$ bits that answers $\text{rank}_b(i)$ and $\text{select}_b(j)$, for $b \in \{0, 1\}$, in $O(1)$ time on the [word RAM](/word-ram/). The rank part is [Jacobson's rank structure](/jacobson-rank/). The select part, due to Clark and Munro in 1996, cuts the list of positions of the 1s into groups; it stores the positions of a group in full when the group is spread out, and it subdivides the group when it is dense. The total space is $n + O(n / \lg \lg n)$ bits in Clark's form, and $n + O(n \lg \lg n / \lg n)$ bits with later refinements. This is the solution of the [rank and select problem](/rank-select-problem/) that most succinct structures build on.

## In plain words

Finding the tenth 1 in a long row of bits is the reverse of counting. A list of the place of each 1 would answer at once, but it takes a full number for each 1, which is far more than the row.

The trick is to treat the 1s in groups. For each group of many 1s, write where the group starts. If the group is spread over a very long stretch of the row, there are few such groups, so you can afford to write the place of each of its 1s. If the group is packed into a short stretch, you only need small numbers to point inside it, so you split it into smaller groups and do the same again. At the end, the 1 you want is inside a stretch of only a few bits, and one short look at the row finds it.

## The abstract type

The structure answers the queries of the [rank and select problem](/rank-select-problem/) on a static bit vector: `build(B)`, `access(i)`, `rank1(i)` and `rank0(i)` for $0 \le i \le n$, `select1(j)` for $1 \le j \le m$ and `select0(j)` for $1 \le j \le n - m$, where $m$ is the number of 1s. The rank of this page counts the bits before position $i$, and select returns a 0-based position.

## Representation

Let $\ell = \max(2, \lceil \lg(n + 1) \rceil)$, and let $P[0 \ldots m-1]$ be the positions of the 1s in increasing order. The structure keeps $B$ in plain form, a rank index, and a select index for the 1s with four parameters: the group size $k_1 = \ell^2$, the group threshold $T_1 = \ell^4$, the subgroup size $k_2 = \lceil \lg \ell \rceil^2$ and the subgroup threshold $T_2 = k_2^2$.

- **Rank index.** Words $W[0 \ldots]$ of $w$ bits. $RS[q]$ is $\text{rank}_1$ at the start of superblock $q$, of $s$ words, and $RB[k]$ is $\text{rank}_1$ at the start of word $k$ minus $RS[\lfloor k/s \rfloor]$.
- **Groups.** Group $g$ is $Q_g = P[g k_1 \ldots \min(m, (g+1) k_1) - 1]$. $G[g]$ is its first position. The group is *sparse* if its *span* $\max Q_g - \min Q_g$ is at least $T_1$, and then $E_1[g]$ lists all of $Q_g$.
- **Subgroups.** A dense group is cut into subgroups $R_{g,h}$ of $k_2$ consecutive 1s. $S[g][h]$ is the first position of $R_{g,h}$ minus $G[g]$. A subgroup is *sparse* if its span is at least $T_2$, and then $E_2[g][h]$ lists its positions minus $G[g]$; else $E_2[g][h]$ is empty.

The select index for the 0s is the same structure built on the positions of the 0s. The invariant is that each field holds the value that its definition gives; the structure is static.

## Operations

```pseudo id=main
BUILD-SELECT(P[0 .. m − 1])                  ▷ P: the positions of the 1s, increasing
L1  for g ← 0 to ⌈m / k1⌉ − 1 do
L2      Q ← P[g·k1 .. min(m, (g + 1)·k1) − 1]   ▷ the 1s of group g
L3      G[g] ← Q[0]
L4      if Q[last] − Q[0] ≥ T1 then sparse[g] ← true, E1[g] ← Q
L5      else
L6          sparse[g] ← false
L7          for h ← 0 to ⌈|Q| / k2⌉ − 1 do
L8              R ← Q[h·k2 .. min(|Q|, (h + 1)·k2) − 1]
L9              S[g][h] ← R[0] − Q[0]                ▷ less than T1
L10             if R[last] − R[0] ≥ T2 then E2[g][h] ← [r − Q[0] for each r in R]
L11             else E2[g][h] ← empty

SELECT1(j)                                   ▷ 1 ≤ j ≤ m
L12 g ← ⌊(j − 1) / k1⌋, t ← (j − 1) mod k1
L13 if sparse[g] then return E1[g][t]
L14 h ← ⌊t / k2⌋, u ← t mod k2
L15 if E2[g][h] is not empty then return G[g] + E2[g][h][u]
L16 return SCAN(G[g] + S[g][h], u + 1)       ▷ the answer is less than T2 bits after the start

RANK1(i)                                     ▷ 0 ≤ i ≤ n
L17 k ← ⌊i / w⌋
L18 return RS[⌊k / s⌋] + RB[k] + POPCOUNT(W[k] and (2^(i mod w) − 1))
```

SCAN$(p, u)$ returns the position of the $u$-th 1 at or after position $p$. It reads the word of $p$ with the bits below $p$ masked off, then the next words, and subtracts their population counts until the word that holds the wanted 1, where a select inside one word finishes. The answer is less than $T_2$ bits after $p$, so SCAN reads at most $\lceil T_2 / w \rceil + 1$ words.

**Build.** Lines L1 to L11 split $P$ into groups and subgroups and fill the fields. The time is $O(n)$: one pass over $B$ to list $P$ and to fill the rank index, and $O(1)$ work for each 1.

**Select.** Line L12 finds the group of the $j$-th 1 and its index $t$ inside the group. A sparse group answers by one read of $E_1$. Otherwise line L14 finds the subgroup and the index $u$ inside it. A sparse subgroup answers by one read of $E_2$. A dense subgroup spans fewer than $T_2 = \lceil \lg \ell \rceil^4$ bits, which is $O(w)$ once $\lceil \lg \ell \rceil^4 \le \ell$, so SCAN reads $O(1)$ words. The time is $O(1)$.

**Rank.** Line L18 is Jacobson's formula with blocks of one word and POPCOUNT in place of the table. Then $\text{rank}_0(i) = i - \text{rank}_1(i)$ and $\text{access}(i) = \text{rank}_1(i+1) - \text{rank}_1(i)$, or a direct read of $W$.

## Example

Take $B = 1011\,0010\,1100\,0111\,0000\,0000\,01$, with $n = 26$ and the 1s at $P = [0, 2, 3, 6, 8, 9, 13, 14, 15, 25]$. The real parameters are too large for a small example, so take $k_1 = 4$, $T_1 = 7$, $k_2 = 2$ and $T_2 = 3$.

| group | $Q_g$ | span | kind | fields |
|---|---|---|---|---|
| 0 | 0, 2, 3, 6 | 6 | dense | $G = 0$; subgroups $[0, 2]$ (span 2, dense, $S = 0$) and $[3, 6]$ (span 3, sparse, $S = 3$, $E_2 = [3, 6]$) |
| 1 | 8, 9, 13, 14 | 6 | dense | $G = 8$; subgroups $[8, 9]$ (dense, $S = 0$) and $[13, 14]$ (dense, $S = 5$) |
| 2 | 15, 25 | 10 | sparse | $G = 15$, $E_1 = [15, 25]$ |

- SELECT1$(4)$: $g = 0$, $t = 3$; $h = 1$, $u = 1$; the subgroup is sparse, so the answer is $0 + E_2[0][1][1] = 6$.
- SELECT1$(6)$: $g = 1$, $t = 1$; $h = 0$, $u = 1$; the subgroup is dense, so SCAN$(8 + 0, 2)$ finds the 1s at 8 and 9 and returns 9.
- SELECT1$(8)$: $g = 1$, $t = 3$; $h = 1$, $u = 1$; SCAN$(8 + 5, 2)$ returns 14.
- SELECT1$(10)$: $g = 2$, $t = 1$; the group is sparse, so the answer is $E_1[2][1] = 25$.

## Correctness

Each field holds its defined value after BUILD. SELECT1 is correct because the $j$-th 1 is element $t$ of group $g$, and element $u$ of subgroup $h$ of that group. If the subgroup is dense, SCAN starts at the first 1 of the subgroup, so the $(u+1)$-th 1 from there is element $u$ of the subgroup. RANK1 is correct by the argument of [Jacobson's rank structure](/jacobson-rank/). The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

| operation | time, worst case |
|---|---|
| build | $O(n)$ |
| access, rank | $O(1)$ |
| select | $O(1)$: at most two reads of the index and one SCAN of $O(1)$ words |

**Space of the select index.** Each count below uses $m \le n$.

- $G$: $\lceil m / k_1 \rceil$ entries of $\ell$ bits, $O(n / \ell)$ bits.
- $E_1$: a sparse group spans at least $T_1 = \ell^4$ positions, and the spans of different groups do not overlap, so there are at most $n / \ell^4 + 1$ sparse groups. Each stores $k_1 = \ell^2$ positions of $\ell$ bits, so $O(n / \ell)$ bits in all.
- $S$: one entry for each subgroup, $O(m / k_2)$ entries of $\lceil \lg T_1 \rceil = O(\lg \ell)$ bits, so $O(n \lg \ell / \lg^2 \ell) = O(n / \lg \ell)$ bits.
- $E_2$: a sparse subgroup spans at least $T_2 = k_2^2$ positions, so there are at most $n / k_2^2 + O(n/k_1)$ of them, each with $k_2$ entries of $O(\lg \ell)$ bits. That is $O(n \lg \ell / k_2) = O(n / \lg \ell)$ bits.

With $\ell = \Theta(\lg n)$, the select index takes $O(n / \lg \lg n)$ bits, and the rank index $O(n \lg \lg n / \lg n)$ bits. The total is $n + O(n / \lg \lg n) = n + o(n)$ bits. Raman, Raman and Rao, and later Golynski, reduced the select index to $O(n \lg \lg n / \lg n)$ bits, which Golynski proved optimal when $B$ is stored in plain form.

## Variants

- **The darray.** Okanohara and Sadakane keep only the first level with fixed sizes: a block of 1024 ones is stored in full if it spans at least $2^{16}$ bits, else every 32nd 1 of it is sampled and the rest is found by a scan. It is fast and small in practice, though not $O(1)$ in the worst case.
- **Select by rank.** Store only the rank index and find select by a binary search over the superblock counts and then inside the superblock, in $O(\lg n)$ time. Navarro, Section 4.3.1, describes this simple heuristic.
- **Select9 and broadword select.** Vigna's select9 adds a two-level inventory of samples to the rank9 layout and selects inside a word with broadword operations.
- **Compressed form.** On top of an [RRR](/rrr-bitvector/) encoding the same index gives a [fully indexable dictionary](/fully-indexable-dictionary/) in $\lg \binom{n}{m} + o(n)$ bits. For very sparse vectors the [SD-array](/sd-array/) is smaller.
- **Optimal redundancy.** Pătraşcu's structure uses $n + n / (\lg n / t)^t + \tilde{O}(n^{3/4})$ bits for $O(t)$ time, and this is optimal up to constants in the exponent; see [Pătraşcu's lower bounds](/patrascu-succinct-lower-bound/).

## When to use it

Use a rank/select dictionary when a structure needs both rank and select on a static bit vector with about as many 0s as 1s: [LOUDS trees](/louds-tree/), [balanced parentheses](/balanced-parentheses-representation/), the bit vectors of a [wavelet tree](/wavelet-tree/), and the upper bits of [Elias-Fano](/elias-fano-encoding/). If only rank is needed, [Jacobson's rank structure](/jacobson-rank/) alone is smaller. If the vector has few 1s or few 0s, the [RRR bit vector](/rrr-bitvector/) or the [SD-array](/sd-array/) uses less space.

## Pitfalls

- **Select of the 0s needs its own index.** The groups of line L2 are groups of 1s. $\text{select}_0$ cannot use them; build the same index on the positions of the 0s, or answer $\text{select}_0$ by binary search over $\text{rank}_0$.
- **The last group.** The last group and the last subgroup can be short. Lines L2 and L8 take the minimum with $m$ and $|Q|$; code that assumes full groups reads past the end of $P$.
- **Relative offsets.** $E_2$ and $S$ store positions minus $G[g]$, so that they fit in $O(\lg \ell)$ bits. Line L15 must add $G[g]$ back, but line L13 must not, because $E_1$ holds absolute positions.
- **SCAN from the wrong place.** SCAN must start at the first 1 of the subgroup and look for its $(u+1)$-th 1. Starting at the start of the group, or asking for the $u$-th 1, gives a wrong position.
- **Asymptotic parameters.** For $n$ up to $2^{64}$, $\lceil \lg \ell \rceil^4$ is larger than $\ell$, so the dense case scans more than one word in practice. Fixed parameters, as in the darray or select9, are faster on real machines.

## Implementations

## History

Jacobson's 1989 structure gave rank in constant time on the word RAM, but select was slower. David Clark, in his 1996 thesis "Compact Pat Trees" at the University of Waterloo, gave the select index with sparse and dense groups described here, with $O(1)$ time and $o(n)$ extra bits. Munro's paper "Tables" of the same year presented constant-time rank and select on the word RAM. Raman, Raman and Rao (2002) lowered the redundancy and compressed the vector itself, and Golynski (2006) matched their redundancy with a lower bound for the plain-vector case. Okanohara and Sadakane named the practical rank/select dictionaries and gave the darray in 2007.

## References
