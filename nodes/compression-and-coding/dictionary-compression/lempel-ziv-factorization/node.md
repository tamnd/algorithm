---
tag: N569BT
kind: problem
slug: lempel-ziv-factorization
name: Lempel-Ziv factorization
aliases:
- LZ77 factorization
area: compression-and-coding/dictionary-compression
level: intro
summary: Cut a string, left to right, into its Lempel-Ziv factors, each the longest prefix of the rest that starts earlier, or one new symbol.
model: word-ram
complexity:
  vars: {n: the length of the string}
  time: {worst: Θ(n)}
  space: {aux: Θ(n)}
prereqs: [lempel-ziv-factor, suffix-array]
see_also: [lempel-ziv-parsing, longest-previous-factor, lcp-array, lz77, lz78-parsing, smallest-grammar-problem, string-attractor, compressed-indexing]
sources:
  - paper: doi:10.1007/978-3-642-38905-4_19
    title: Juha Kärkkäinen, Dominik Kempa and Simon J. Puglisi, Linear time Lempel-Ziv factorization, simple, fast, small, CPM 2013, LNCS 7922
    locator: Section 2 (definitions, the example zzzzzipzip, the lemma on PSV and NSV), Fig. 1 (LZ-Factor) and Fig. 2 (algorithm KKP3), pages 189 to 200
  - paper: doi:10.1016/j.ipl.2007.10.006
    title: Maxime Crochemore and Lucian Ilie, Computing Longest Previous Factor in linear time and applications, Information Processing Letters 106(2), 2008
    locator: pages 75 to 80 (the LPF array from the suffix array and LCP array in linear time, and the LZ factorization from LPF)
  - paper: doi:10.1109/TIT.2005.850116
    title: Moses Charikar, Eric Lehman, Ding Liu, Rina Panigrahy, Manoj Prabhakaran, Amit Sahai and abhi shelat, The smallest grammar problem, IEEE Transactions on Information Theory 51(7), 2005
    locator: Section VII.D, Lemma 9 (the LZ77 parse without self-reference has no more phrases than the size of any grammar for the string)
  - paper: doi:10.1016/S0304-3975(02)00777-6
    title: Wojciech Rytter, Application of Lempel-Ziv factorization to the approximation of grammar-based compression, Theoretical Computer Science 302(1-3), 2003
    locator: pages 211 to 222 (the LZ factorization as a lower bound on grammar size, and a grammar of size O(z log(n/z)) built from it)
  - paper: doi:10.1109/TIT.1978.1055934
    title: Jacob Ziv and Abraham Lempel, Compression of individual sequences via variable-rate coding, IEEE Transactions on Information Theory 24(5), 1978
    locator: pages 530 to 536 (the bound on the number of distinct phrases)
---

The Lempel-Ziv factorization problem asks for the cut of a string $T[1..n]$ into its [Lempel-Ziv factors](/lempel-ziv-factor/): from left to right, each factor is the longest prefix of the rest of the string that also starts at an earlier position, or one new symbol. The number of factors, $z$, is the size of the output of an LZ77 compressor with no window limit, and in string algorithms it is the standard measure of how repetitive a string is. Given the [suffix array](/suffix-array/), the factorization takes $O(n)$ time.

## In plain words

Read the text from the start. At each place, find the longest piece that begins here and that also begins somewhere earlier. The earlier copy may run on into the piece itself, so after "ab" the piece "ababab" counts, since it starts two places back. If no letter here was seen before, the piece is that one letter. Cut, and go on from the cut.

The slow way looks back over the whole text at every cut. The fast way first puts all the endings of the text in sorted order. Endings that start alike are then close together in that order. For each place, only two endings need a check: the nearest earlier-starting ending on each side in the sorted order.

## Definition

**Input.** A string $T = T[1..n]$ over an integer alphabet $\Sigma = \{1, \ldots, \sigma\}$ with $\sigma \le n$, in the word RAM model.

**Output.** The factors $f_1, \ldots, f_z$ with $T = f_1 \cdots f_z$, where $f_k$ starts at $p_k = 1 + |f_1 \cdots f_{k-1}|$ and is the Lempel-Ziv factor at $p_k$: its length is $\max(1, \mathrm{lpf}(p_k))$, where $\mathrm{lpf}(i)$ is the length of the longest prefix of $T[i..n]$ that also starts at some $j < i$. Each factor is reported as a pair (source $j$, length) or, when $\mathrm{lpf}(p_k) = 0$, as the new symbol $T[p_k]$. A source may overlap its factor ($j + \mathrm{lpf}(p_k) - 1 \ge p_k$).

## Variants

- **No self-reference.** The source must lie inside $T[1..p_k-1]$. This is the parse used in the bound of Charikar et al. below; it has at least as many factors.
- **Window.** The source must start in $T[p_k - W .. p_k - 1]$ for a window of size $W$, as in compressors. This is a problem of [match finding](/match-finding/), solved with hash chains or trees over the window.
- **LZ77 triple parse.** Each phrase is the longest copy plus one literal symbol; see [LZ77](/lz77/).
- **The LPF array.** Compute $\mathrm{lpf}(i)$ for every $i$, not only at factor starts; this is the [longest previous factor](/longest-previous-factor/) problem. The factorization follows from it in $O(n)$ time.
- **Closest or leftmost sources.** Some uses want, for each factor, the source with the smallest distance $p_k - j$ (it costs fewer bits) or the leftmost one.
- **Fewer bits, not fewer factors.** When each factor has a cost in bits that depends on its distance and length, the problem becomes [optimal LZ parsing](/optimal-lz-parsing/).
- **Other parses.** [LZ78 parsing](/lz78-parsing/) and [LZ-End](/lz-end/) restrict where a source may be; [Lempel-Ziv parsing](/lempel-ziv-parsing/) compares them.

## Examples

**Three short strings.** $abababab = a \mid b \mid ababab$ ($z = 3$); $aaaaaaaa = a \mid aaaaaaa$ ($z = 2$); $zzzzzipzip = z \mid zzzz \mid i \mid p \mid zip$ ($z = 5$, the example of Kärkkäinen, Kempa and Puglisi). In the first two, the long factor overlaps its source.

**The method on abracadabra.** The suffix array is $SA = [11, 8, 1, 4, 6, 9, 2, 5, 7, 10, 3]$. For text position $i$, $\mathrm{PSV}[i]$ is the nearest suffix before $i$ in $SA$ that starts at a position smaller than $i$, and $\mathrm{NSV}[i]$ is the nearest one after it; 0 means "none".

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $T[i]$ | a | b | r | a | c | a | d | a | b | r | a |
| $\mathrm{PSV}[i]$ | 0 | 1 | 2 | 1 | 2 | 4 | 5 | 0 | 6 | 7 | 0 |
| $\mathrm{NSV}[i]$ | 0 | 0 | 0 | 2 | 3 | 2 | 3 | 1 | 2 | 3 | 8 |

The factors start at 1, 2, 3, 4, 5, 6, 7, 8. At $i = 4$, $\mathrm{lcp}(T[4..], T[1..]) = 1$ and $\mathrm{lcp}(T[4..], T[2..]) = 0$, so the factor is $a$ with source 1. At $i = 8$, $\mathrm{PSV}[8] = 0$ and $\mathrm{lcp}(T[8..], T[1..]) = 4$, so the factor is $abra$ with source 1. At $i = 2$, $\mathrm{NSV}[2] = 0$, so the only candidate is $\mathrm{PSV}[2] = 1$; it gives lcp 0, and $b$ is a new symbol. The result is $a \mid b \mid r \mid a \mid c \mid a \mid d \mid abra$, $z = 8$.

## Known algorithms

**Brute force, $O(n^2)$.** At each factor start $p$, run the [Z-algorithm](/z-algorithm/) on $T[p..n]$ followed by $T[1..n]$, or compare with every earlier start. One factor costs $O(n)$, so the total is $O(nz)$, which is $O(n^2)$ in the worst case.

**Suffix tree, $O(n)$.** Store in each node of the [suffix tree](/suffix-tree/) the smallest starting position in its subtree. At a factor start $p$, walk down from the root along $T[p..]$ while the smallest start below the current point is less than $p$. The depth reached is $\mathrm{lpf}(p)$. With a linear-time suffix tree construction for an integer alphabet, the total is $O(n)$, but the tree takes much memory.

**LPF from the suffix array, $O(n)$ (Crochemore and Ilie, 2008).** From the suffix array and the [LCP array](/lcp-array/), compute the whole LPF array in linear time, using the fact that one of the two neighbours below proves the maximum; then read off the factors.

**PSV and NSV with lazy lcp, $O(n)$ (Kärkkäinen, Kempa and Puglisi, 2013).** Algorithm KKP3 needs only the suffix array. It computes $\mathrm{PSV}$ and $\mathrm{NSV}$ in one pass over $SA$ with a stack, and it computes an lcp by direct comparison only at the start of each factor:

```pseudo id=main
LZ-FACTORIZE(T)       ▷ T[1 .. n]; 0 means "no position"
L1  SA ← suffix array of T
L2  S ← stack that holds 0
L3  for each x in SA[1], …, SA[n], 0 do
L4      while top(S) > x do t ← pop(S)
L5          NSV[t] ← x
L6          PSV[t] ← top(S)
L7      push x on S
L8  i ← 1
L9  while i ≤ n do
L10     for each j in {PSV[i], NSV[i]} with j ≠ 0 do
L11         ℓ_j ← lcp(T[j..n], T[i..n]), by comparing symbols one by one
L12     if there is no candidate j or every ℓ_j = 0 then
L13         output the new symbol T[i]; i ← i + 1
L14     else
L15         take j with the largest ℓ_j; output (j, ℓ_j); i ← i + ℓ_j
L16 return the output
```

The suffix array costs $O(n)$ time with [SA-IS](/sa-is/). Lines L2 to L7 push and pop each position once. At a factor of length $\ell$ that starts at $i$, line L11 does at most $\ell + 1$ comparisons for each of the two candidates, so all the comparisons together cost at most $2(n + z) = O(n)$.

**Why two candidates are enough.** Let $j < i$ be any earlier start. In the suffix array, consider the suffixes that start before $i$, together with suffix $i$. For three suffixes $a < b < c$ in lexicographic order, $\mathrm{lcp}(a, c) \le \mathrm{lcp}(b, c)$: if $a$ and $c$ agree on their first $\ell$ symbols, then $b$, which lies between them, agrees with both on those symbols. So among the suffixes with start less than $i$ that come before suffix $i$ in $SA$, the one nearest to it (that is, $\mathrm{PSV}[i]$) has the longest lcp with it, and in the same way $\mathrm{NSV}[i]$ is best among those after it. The larger of the two lcp values is $\mathrm{lpf}(i)$, and its position is a source. On the stack pass: the stack holds positions that increase from bottom to top; when $x$ arrives, each larger position $t$ popped has $x$ as the first later entry of $SA$ with a smaller position, and the entry under $t$ is the last earlier one.

**Other methods.** Many later algorithms trade time for memory, for example by working from the [Burrows-Wheeler transform](/burrows-wheeler-transform/) in compressed space, or compute the parse online, but the linear-time methods above are the practical base.

**History.** Lempel and Ziv defined the copy-based complexity of a sequence in 1976 and the sliding-window compressor in 1977. Linear-time computation with suffix trees dates from the early 1980s. Crochemore and Ilie gave the LPF array from the suffix array in 2008, and Kärkkäinen, Kempa and Puglisi gave the simple, fast and small KKP family in 2013; they credit the lazy lcp computation to earlier work by Kempa and Puglisi and by Goto and Bannai.

## Bounds

**Time.** $\Theta(n)$ on the word RAM for an integer alphabet: the output can have $n$ factors, and the algorithm above runs in $O(n)$. The space is $\Theta(n)$ words for the suffix array and the PSV and NSV arrays.

**Greedy gives the fewest factors.** Call a parse $T = g_1 \cdots g_m$ *admissible* if each $g_k$ is a single symbol or occurs at an earlier position than its own (overlap allowed). Then $z \le m$ for every admissible parse.

*Proof.* Let $e_k$ be the end of the $k$-th Lempel-Ziv factor and $e'_k$ the end of $g_k$ (with $e_0 = e'_0 = 0$). We show $e_k \ge e'_k$ for all $k$ by induction. If $e'_{k+1} \le e_k$ there is nothing to show. Otherwise $g_{k+1} = T[e'_k + 1 .. e'_{k+1}]$ contains position $e_k + 1$, since $e'_k \le e_k$. If $g_{k+1}$ is a copy of earlier text that starts at $j < e'_k + 1$, then $T[e_k + 1 .. e'_{k+1}]$ is a copy that starts at $j + (e_k - e'_k) < e_k + 1$, so $\mathrm{lpf}(e_k + 1) \ge e'_{k+1} - e_k$, and the next factor reaches at least $e'_{k+1}$. If $g_{k+1}$ is a single symbol, it is $T[e_k + 1]$ and the next factor has length at least 1. So the Lempel-Ziv factors reach $n$ in at most $m$ steps. $\square$

**Lower bound on grammar size.** Let $g$ be the size (total length of the right-hand sides) of any context-free grammar that generates only $T$. Then $z \le g$. This is Lemma 9 in Section VII.D of Charikar et al. (2005), for the parse without self-reference, which has at least $z$ factors; Rytter (2003) proves the same bound.

*Proof.* Take the derivation tree of $T$ and keep the subtree below only the first occurrence of each nonterminal, in preorder; make every later occurrence a leaf. A nonterminal does not occur below itself, so a later occurrence of $A$ is disjoint from the first one and lies to its right: it is a copy of earlier text. Each kept nonterminal has as many children as the length of its right-hand side, so the tree has at most $g$ leaves. Read left to right, the leaves give an admissible parse of $T$ with at most $g$ phrases, and the greedy bound gives $z \le g$. $\square$

So $z$ is a lower bound for the [smallest grammar problem](/smallest-grammar-problem/). Rytter (2003) also builds from the factorization a grammar of size $O(z \log(n/z))$, which gives an $O(\log(n/g))$ approximation for the smallest grammar.

**Upper bound on $z$.** $z \le 2 z_{78}$, where $z_{78}$ is the number of phrases of the [LZ78 parsing](/lz78-parsing/). *Proof.* Each LZ78 phrase is an earlier phrase (a copy of earlier text, or empty) followed by one symbol. Split it there; the pieces form an admissible parse with at most $2 z_{78}$ phrases, and the greedy bound applies. $\square$ Since $z_{78} = O(n / \log_\sigma n)$ (proved on [LZ78 parsing](/lz78-parsing/)), also $z = O(n / \log_\sigma n)$ in the worst case, for every string of length $n$ over $\sigma$ symbols.

**Small $z$.** A run $a^n$ has $z = 2$, and $z \ge$ the number of distinct symbols in $T$. A Fibonacci word of length $n$ has $z = \Theta(\log n)$.

## Reductions

- **To the LPF array.** The factorization is read from $\mathrm{lpf}$ by jumping: $p_{k+1} = p_k + \max(1, \mathrm{lpf}(p_k))$.
- **To the suffix array.** The method above reduces the problem in $O(n)$ time to suffix sorting. The suffix array of an integer alphabet of size at most $n$ takes $O(n)$ time, so the two problems have the same time bound.
- **From the factorization to a grammar.** A grammar of size $O(z \log(n/z))$ follows in $O(n)$ more time (Rytter, 2003).
- **From the factorization to runs.** Algorithms for all maximal repetitions (runs) of a string, such as the one of Kolpakov and Kucherov, start from the Lempel-Ziv factorization.

## Applications

- **Compression.** The factors are the tokens of an LZ77 compressor with an unbounded window; real compressors use a window and an [optimal LZ parse](/optimal-lz-parsing/) in bits.
- **Indexes for repetitive data.** Self-indexes for collections of similar strings (genomes of one species, versions of documents) store the factorization in $O(z)$ space; see [compressed indexing](/compressed-indexing/), the [LZ-index](/lz-index/) and [pattern matching in compressed text](/pattern-matching-in-compressed-text/).
- **Measures of repetition.** $z$ bounds the smallest grammar from below and the smallest [string attractor](/string-attractor/) from above.
- **Repetitions in strings.** Runs, squares and other periodic structures are found from the factors.

The page [Lempel-Ziv parsing](/lempel-ziv-parsing/) compares this parse with LZ77 and LZ78; the string combinatorics area has the [Lyndon factorization](/lyndon-factorization/), which cuts a string by lexicographic order and not by repetition.

## References
