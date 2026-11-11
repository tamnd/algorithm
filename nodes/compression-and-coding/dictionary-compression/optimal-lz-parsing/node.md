---
tag: 3V4KB0
kind: problem
slug: optimal-lz-parsing
name: Optimal LZ parsing
aliases:
- optimal LZ77 parsing
- minimum-cost parse
- bit-optimal LZ77 parsing
area: compression-and-coding/dictionary-compression
level: advanced
summary: Find the LZ77 parse of a text into literals and copies whose total encoded size, under a given cost model, is the smallest.
prereqs: [optimal-parsing, greedy-parsing, elias-gamma-coding]
see_also: [lz77, lzss, lazy-matching, match-finding, lzma, zstandard, deflate, dag-shortest-paths]
sources:
  - paper: doi:10.1137/120869511
    title: Paolo Ferragina, Igor Nitto and Rossano Venturini, On the bit-complexity of Lempel-Ziv compression, SIAM Journal on Computing 42(4), 1521-1541, 2013
    locator: "Section 2 (the graph of all LZ77 parses and its Θ(n^2) edges), Lemma 1 (greedy can use Ω(log n / log log n) times more bits), Section 3 (maximal edges, Theorem 1) and Theorem 2 (the bit-optimal parse in O(n log n) time for the usual integer codes)"
  - paper: "Paolo Ferragina, Igor Nitto and Rossano Venturini, On the bit-complexity of Lempel-Ziv compression, Proceedings of the 20th ACM-SIAM Symposium on Discrete Algorithms (SODA 2009), 768-777"
    locator: the conference version of the same results
  - paper: doi:10.1145/322344.322346
    title: James A. Storer and Thomas G. Szymanski, Data compression via textual substitution, Journal of the ACM 29(4), 928-951, 1982
    locator: the macro model with pointers to earlier text, a flag to tell pointers from symbols, and a fixed pointer size
  - paper: doi:10.1109/TIT.1977.1055714
    title: Jacob Ziv and Abraham Lempel, A universal algorithm for sequential data compression, IEEE Transactions on Information Theory 23(3), 337-343, 1977
    locator: the LZ77 parse with copies from a sliding window
---

Optimal LZ parsing is the problem of cutting a text into [LZ77](/lz77/) phrases, literals and copies from earlier text, so that the total number of output bits under a given cost model is as small as possible. When every phrase costs the same, [greedy parsing](/greedy-parsing/) already solves it. When a copy costs more for a larger distance or length, as in every real format, greedy can lose, and the problem becomes a shortest path problem over the text positions with up to $\Theta(n^2)$ edges. Ferragina, Nitto and Venturini showed that a small set of edges suffices, which gives the bit-optimal parse in $O(n \log n)$ time for the usual integer codes.

## In plain words

An LZ77 compressor writes a text as letters and "copy so many letters from so far back". Each choice has a price in bits. A copy from close by is cheap to write, and a copy from far back costs more because the distance is a bigger number. A long copy is usually a good deal, but not always.

The question is: among all ways to write the text, which one has the lowest total price? The number of ways is huge, but the best way can be found by working backward from the end of the text. At each place you only need, for each copy length, the closest place where that copy starts, because a closer copy is never more expensive.

## Definition

**Input.** A string $t = t[0 \ldots n-1]$ over an alphabet $\Sigma$ of size $\sigma$, and a cost model. The model gives the cost $\lambda(c)$ in bits of a literal $c \in \Sigma$, and the cost $\kappa(\ell, d)$ of a copy of length $\ell$ and distance $d$. It may also give a minimum copy length $\ell_{\min}$, a maximum length $\ell_{\max}$, and a window $w$. The model is the worst case: the text is given, with no probability model.

**Phrases.** At position $i$, a literal covers $t[i]$. A copy $(\ell, d)$ with $\ell_{\min} \le \ell \le \ell_{\max}$ and $1 \le d \le \min(i, w)$ covers $t[i \ldots i+\ell-1]$ and is valid if $t[i-d+k] = t[i+k]$ for $0 \le k < \ell$. The source may overlap the phrase.

**Output.** A parse, a sequence of valid phrases that covers $t$ from left to right, of minimum total cost.

**The standard assumption.** $\kappa(\ell, d)$ is non-decreasing in $d$ (and, for the faster algorithms, in $\ell$). Both parts hold for fixed-width fields and for [Elias gamma](/elias-gamma-coding/) and other universal integer codes. The first part holds for the distance codes of [DEFLATE](/deflate/) with fixed Huffman tables, but the second does not: there a copy of length 258 has a shorter code than a copy of length 257.

**Lemma 1.** Under the assumption, for each position $i$ and length $\ell$ the best copy uses the smallest distance $d_i(\ell)$ of a valid copy of length $\ell$. *Proof.* Any other valid copy of the same length has a larger distance and a cost at least as large, and it covers the same positions. $\square$

A copy of length $\ell$ at distance $d$ is also a valid copy of each shorter length at the same distance. So $d_i(\ell)$ is non-decreasing in $\ell$, and a scan over the sources from the nearest to the farthest lists all the pairs $(\ell, d_i(\ell))$: each time the match length grows, the new lengths get the current distance.

**Lemma 2.** Let $C[i]$ be the least cost of a parse of $t[i \ldots n-1]$. Then $C[n] = 0$ and
$$C[i] = \min\Big(\lambda(t[i]) + C[i+1],\ \min_{\ell} \big(\kappa(\ell, d_i(\ell)) + C[i+\ell]\big)\Big),$$
where $\ell$ runs over the valid copy lengths at $i$. *Proof.* The parses of $t[i \ldots]$ are the first phrase followed by a parse of the rest, and the rest must be optimal; Lemma 1 fixes the distance for each length. This is the recurrence of [optimal parsing](/optimal-parsing/) for the graph whose edges are the copies. $\square$

## Variants

- **Equal phrase costs.** Minimize the number of phrases. With $\ell_{\min} = 1$, greedy parsing is optimal, with or without a window ([greedy parsing](/greedy-parsing/) has the proof).
- **The flag model.** A flag bit tells literals from copies, and the fields have fixed widths, as in [LZSS](/lzss/). Storer and Szymanski (1982) studied this model. All copies cost the same, but $\ell_{\min} > 1$ and the fixed literal cost make greedy suboptimal.
- **Variable-length integer codes.** The copy costs $|f(d)| + |g(\ell)|$ for prefix codes $f$ and $g$ of the integers, such as Elias gamma or delta codes. This is the setting of Ferragina, Nitto and Venturini, with the first occurrence of each new symbol as a literal.
- **Adaptive costs.** In DEFLATE, [LZMA](/lzma/) and [Zstandard](/zstandard/), the code lengths come from Huffman tables or an adaptive range coder, which depend on the parse. Encoders then fix the costs from an earlier pass and parse again, so they solve the problem only for estimated costs.
- **Costs with state.** LZMA gives a lower cost to a copy that reuses one of the last four distances. Then the cost depends on the earlier phrases, and the dynamic program needs the recent distances as part of its state.

## Examples

All numbers below come from the implementation in `impl/python`, and the tests check them.

**The distance list.** For $t$ = `abcabxbcab` at position 6 (the text `bcab`), the nearest source with a common first symbol is at distance 2 (`b` then `x`), and the nearest source of `bcab` is at distance 5. So the list is $(1, 2), (2, 5), (3, 5), (4, 5)$.

**The gamma model.** A literal costs 9 bits, and a copy costs $1 + \gamma(\ell) + \gamma(d)$ bits with $\gamma(x) = 2 \lfloor \log_2 x \rfloor + 1$; $\ell_{\min} = 1$ and there is no window. For $t$ = `aabbaa`:

| Parse | Phrases | Bits |
|---|---|---|
| Greedy | `a`, copy (1, 1), `b`, copy (1, 1), copy (2, 4) | $9 + 3 + 9 + 3 + 9 = 33$ |
| Optimal | `a`, copy (1, 1), `b`, copy (1, 1), copy (1, 3), copy (1, 1) | $9 + 3 + 9 + 3 + 5 + 3 = 32$ |

The far copy (2, 4) costs 9 bits, but the two close copies (1, 3) and (1, 1) cost 8 bits together, so the optimal parse has more phrases and fewer bits.

**The flag model.** A literal costs 9 bits, a copy costs 17 bits (a flag, 4 bits of length and 12 bits of distance), with $2 \le \ell \le 17$ and $w = 4096$. For $t$ = `aabaaaa`, greedy writes `a`, `a`, `b`, copy (2, 3), copy (2, 1) for 61 bits. The optimal parse writes `a`, `a`, `b`, `a` and copy (3, 1) for 53 bits.

**A longer text.** The test builds a text of 752 bytes from 150 words chosen with a fixed seed from `the`, `then`, `there`, `other`, `them` and `hat`, each followed by a space. In the gamma model, greedy uses 1501 bits in 85 phrases and the optimal parse 1364 bits in 88 phrases. In the flag model, greedy uses 1383 bits and the optimal parse 1319 bits, both with 87 phrases.

## Known algorithms

**Dynamic program over all edges.** Compute the list $(\ell, d_i(\ell))$ at each position and run Lemma 2 from right to left.

```pseudo id=main
OPTIMAL-LZ-PARSE(t)
L1  C[n] ← 0
L2  for i ← n − 1 downto 0 do
L3      C[i] ← λ(t[i]) + C[i + 1]; choice[i] ← literal
L4      for each (ℓ, d) in the list of i, with ℓ ≥ ℓmin do
L5          if κ(ℓ, d) + C[i + ℓ] < C[i] then
L6              C[i] ← κ(ℓ, d) + C[i + ℓ]; choice[i] ← copy (ℓ, d)
L7  i ← 0; while i < n do emit choice[i]; advance i past it
L8  return C[0]
```

The lists have up to $n - i$ entries at position $i$: for $t = a^n$ each length from 1 to $n-i$ is a valid copy at distance 1. So the graph has $\Theta(n^2)$ edges in the worst case, and the dynamic program takes $\Theta(n^2)$ time on top of the cost of the lists. The implementation finds the lists by trying every source, which is a reference method, not a fast one. With $\ell_{\max}$ bounded, as in real formats, there are at most $n \ell_{\max}$ edges.

**Maximal edges (Ferragina, Nitto and Venturini).** Assume also $\ell_{\min} = 1$ and $\kappa$ non-decreasing in $\ell$. Then $C[i] \ge C[j]$ for $i < j$: in an optimal parse of $t[i \ldots]$, the phrase that covers position $j$ has a suffix that starts at $j$, is a valid phrase of no larger cost, and with the rest of the parse covers $t[j \ldots]$. Split the distances into classes on which $|f(d)|$ is constant, and the lengths into classes on which $|g(\ell)|$ is constant. Inside one pair of classes all edges at $i$ cost the same, so the longest one is best, because it ends at the position with the smallest $C$. So each position needs only, for each distance class, the longest copy with a distance in the class, and then, for each length class up to that length, its largest length. For codes such as Elias gamma there are $O(\log n)$ classes, and the paper finds these edges for all positions and runs the shortest path computation in $O(n \log n)$ time and $O(n)$ space in total. The tests check that the maximal edges give the same optimum as all edges.

**Heuristics in practice.** LZMA's normal mode runs an optimal parse over a block of positions with price tables taken from its range coder state. Zstandard's `btopt` and `btultra` strategies do the same with binary tree match finders. These encoders solve the problem for estimated prices, not exactly.

## Bounds

- Any algorithm must read the input, so $\Omega(n)$ time.
- The graph of all copies has $\Theta(n^2)$ edges in the worst case, so methods that list all edges are quadratic. The maximal edge method avoids this for costs with $O(\log n)$ classes.
- Greedy can be far from optimal in bits: Ferragina, Nitto and Venturini (Lemma 1) give a family of strings on which greedy uses $\Omega(\log n / \log \log n)$ times more bits than the optimum, under a cost model with variable-length integer codes.
- The optimum is never worse than greedy, lazy matching, or any other rule, since each of them outputs one of the parses over which the minimum is taken.

## Reductions

- **To shortest paths.** The problem is a shortest path from node 0 to node $n$ in a [directed acyclic graph](/directed-acyclic-graph/) whose nodes are positions and whose edges are phrases; [DAG shortest paths](/dag-shortest-paths/) solve it in time linear in the edges.
- **From optimal parsing.** It is the special case of [optimal parsing](/optimal-parsing/) where the dictionary at position $i$ is the set of substrings that start before $i$. The general technique lists the phrases at each position; here the list must be cut down to one distance per length (Lemma 1) and, for speed, to the maximal edges.
- **To greedy.** With equal phrase costs and $\ell_{\min} = 1$ the problem reduces to the greedy parse, which needs one longest match per phrase.

## Applications

- Encoders that aim at the best ratio for a format whose decoder is fixed: LZMA and xz, Zstandard at high levels, and DEFLATE encoders that repeat the parse with costs from the Huffman codes of the previous pass.
- The study of how much the parse matters: the gap between greedy, [lazy matching](/lazy-matching/) and the optimum on a given text measures the loss of the fast parse rules.
- [Match finding](/match-finding/) design: an optimal parser needs every pair $(\ell, d_i(\ell))$, not only the longest match, which is why binary tree finders, which list these pairs in one walk, go with optimal parsers.

## References
