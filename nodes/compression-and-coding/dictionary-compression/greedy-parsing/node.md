---
tag: 08SJN4
kind: technique
slug: greedy-parsing
name: Greedy parsing
aliases:
- greedy LZ parsing
- longest-match parsing
area: compression-and-coding/dictionary-compression
level: intro
summary: Cut the text into phrases by taking, at each position, the longest phrase that the dictionary allows. Optimal in phrase count for LZ77 copies.
prereqs: [greedy-algorithm, match-finding]
see_also: [lazy-matching, optimal-parsing, optimal-lz-parsing, lz77, lzss, lz78, deflate, lempel-ziv-factorization]
sources:
  - paper: doi:10.1137/120869511
    title: Paolo Ferragina, Igor Nitto and Rossano Venturini, On the bit-complexity of Lempel-Ziv compression, SIAM Journal on Computing 42(4), 1521-1541, 2013
    locator: Section 1 (greedy parsing minimizes the number of phrases of LZ77 but not the number of bits) and Lemma 1 (a family of strings on which greedy uses more bits than the optimum by a factor that grows with n)
  - url: https://arxiv.org/abs/1211.5350
    title: Maxime Crochemore, Alessio Langiu and Filippo Mignosi, Note on the greedy parsing optimality for dictionary-based text compression, arXiv 1211.5350, 2012
    locator: the main theorem (greedy parsing is optimal in phrase count for suffix-closed dictionaries, which include the LZ77 dictionaries with a bounded window)
  - paper: "Martin Cohn and Roger Khazan, Parsing with prefix and suffix dictionaries, Proceedings of the Data Compression Conference (DCC 1996), 180-189"
    locator: greedy parsing with suffix dictionaries and flexible parsing with prefix dictionaries
  - paper: doi:10.1145/322344.322346
    title: James A. Storer and Thomas G. Szymanski, Data compression via textual substitution, Journal of the ACM 29(4), 928-951, 1982
    locator: the macro schemes with pointers to earlier text, and the comparison of greedy and optimal parsing for them
---

Greedy parsing cuts a text into phrases from left to right and, at each position, takes the longest phrase that the dictionary of the compressor allows. It is the parse of [LZ77](/lz77/), of [LZSS](/lzss/) and of the fast levels of [DEFLATE](/deflate/). For LZ77 copies where every phrase has the same cost, greedy gives the smallest possible number of phrases, with or without a bounded window. It is not optimal when phrases have different costs in bits, when copies have a minimum length, or for a static dictionary that is not closed under suffixes.

## In plain words

You want to write a long text with as few pieces as possible. Each piece is a single letter, or a copy of some letters that you wrote before. At each step you take the longest copy that you can find. If there is no copy, you write one letter.

This simple rule is the best one when every piece costs the same. The reason is that a long copy never puts you behind: any other plan that reaches further must use a piece that also starts where you are now, and you could take that piece too.

The rule fails when pieces have different prices. A long copy from far back can cost more than two short copies from close by. The rule also fails when short copies are not allowed, because a long first copy can leave a short gap that no copy fits.

## When it applies

The input is a string $t = t[0 \ldots n-1]$ over an alphabet $\Sigma$ of size $\sigma$. A *parse* cuts $t$ into consecutive phrases $t[s_1 \ldots e_1-1], t[s_2 \ldots e_2-1], \ldots$ with $s_1 = 0$, $s_{k+1} = e_k$ and the last end $= n$. Each phrase must be *valid*: it is a member of the dictionary at its position. For the LZ77 family, the phrase $[s, e)$ is valid when it is one literal symbol ($e = s+1$), or a copy: $t[s \ldots e-1] = t[j \ldots j+e-s-1]$ for some source $j < s$, where the source may overlap the phrase and, with a window $w$, $s - j \le w$.

Greedy parsing applies to any dictionary where the encoder can find the longest valid phrase at a position. It gives the minimum number of phrases when the dictionary is *suffix-closed*: if $[s', e)$ is valid and $s' \le s < e$, then $[s, e)$ is valid too.

**Claim.** If the valid phrases are suffix-closed and each single symbol is valid, the greedy parse has the minimum number of phrases.

**Proof.** Let the greedy parse end its phrases at $g_1 < g_2 < \cdots < g_a = n$, and let any other parse end its phrases at $p_1 < p_2 < \cdots < p_b = n$. Put $g_0 = p_0 = 0$. We show $g_k \ge p_k$ for each $k \le \min(a, b)$, by induction on $k$. For $k = 0$ it holds. Assume $g_k \ge p_k$ with $g_k < n$. If $p_{k+1} \le g_k$, then $g_{k+1} > g_k \ge p_{k+1}$. Else $p_k \le g_k < p_{k+1}$, and the phrase $[p_k, p_{k+1})$ of the other parse is valid, so its suffix $[g_k, p_{k+1})$ is valid. Greedy takes the longest valid phrase at $g_k$, so $g_{k+1} \ge p_{k+1}$. Now $g_b \ge p_b = n$, so greedy has ended by step $b$, and $a \le b$. $\square$

**The LZ77 dictionaries are suffix-closed.** Let $[s', e)$ be a copy with source $j$, and let $s' < s < e$. Then $t[s \ldots e-1]$ equals $t[j + (s - s') \ldots]$, a source that starts before $s$ at the same distance $s' - j$, so the window rule still holds. The same holds for the original LZ77 phrase, a copy of length 0 or more followed by one explicit symbol: a suffix of such a phrase is a shorter copy followed by the same symbol. So greedy is optimal in phrase count for LZ77 triples, for literals and copies (LZSS without a minimum length), with an unbounded window and with a window $w$. Crochemore, Langiu and Mignosi state this result for suffix-closed dictionaries, and Ferragina, Nitto and Venturini state it for LZ77.

**Where the condition fails.**

- A minimum copy length $\ell_{\min} > 1$ breaks suffix closure, because a suffix of a copy can be shorter than $\ell_{\min}$.
- A cost in bits that depends on the length and the distance makes the phrase count the wrong measure.
- A static dictionary chosen in advance is usually not suffix-closed.
- For [LZ78](/lz78/) and [LZW](/lzw/) the dictionary is built from the parse itself, so a different cut changes the later dictionaries; greedy there is the definition of the method, and the question of a better parse is the one of [flexible parsing](/optimal-parsing/).

## The template

```pseudo id=main
GREEDY-PARSE(t)
L1  i ← 0; P ← empty list
L2  while i < n do
L3      (ℓ, d) ← LONGEST-PHRASE(t, i)          ▷ hole: the match finder of the dictionary
L4      if ℓ ≥ ℓmin then                        ▷ hole: the shortest phrase worth a copy
L5          append the copy (ℓ, d) to P; i ← i + ℓ
L6      else
L7          append the literal t[i] to P; i ← i + 1
L8  return P
```

The two holes are the dictionary and its [match finder](/match-finding/) in line L3, and the threshold $\ell_{\min}$ in line L4. With an exact match finder the loop does $O(n)$ steps and one search per step. The searches dominate: with the brute force, a search costs $O(n \cdot \ell)$ symbol comparisons. With the suffix array method the longest previous match at every position costs $O(n)$ in total after the [suffix array](/suffix-array/) is built, so the greedy LZ77 parse without a window takes linear time. Real encoders use hash chains with a chain limit. Then line L3 may return a shorter match than the longest one, and the parse is greedy only with respect to the matches the finder sees.

## Classic examples

- [LZ77](/lz77/): the triple (distance, length, next symbol) with the longest copy, in a sliding window. This parse is optimal in phrase count, by the claim above.
- [LZSS](/lzss/): a flag bit selects a literal or a copy, and copies shorter than a threshold are written as literals. The threshold makes greedy suboptimal in phrase count, as the example below shows.
- [DEFLATE](/deflate/): zlib's levels 1 to 3 parse greedily with a short hash chain search, and levels 4 to 9 add [lazy matching](/lazy-matching/).
- The [Lempel-Ziv factorization](/lempel-ziv-factorization/) of string algorithms: each factor is the longest previous factor, or one new symbol. It is the greedy parse with an unbounded window, and it is computed exactly from the [longest previous factor](/longest-previous-factor/) array.
- [LZ78](/lz78/) and [LZW](/lzw/): each phrase is the longest dictionary entry that matches, plus one symbol for LZ78.

### Worked examples

All values here are checked by the tests in `impl/python`.

**Optimal in phrase count.** For $t$ = `aabbaa` the greedy parse with literals and copies is

| Step | Position | Longest copy | Phrase |
|---|---|---|---|
| 1 | 0 | none | literal `a` |
| 2 | 1 | length 1, distance 1 | copy (1, 1) |
| 3 | 2 | none | literal `b` |
| 4 | 3 | length 1, distance 1 | copy (1, 1) |
| 5 | 4 | length 2, distance 4 | copy (2, 4) |

Five phrases is the minimum. The tests compare the greedy count with the minimum over all parses for every string over $\{a, b\}$ of length at most 9, and for random strings with windows from 1 to 5.

**Not optimal in bits.** Let a literal cost 9 bits and a copy cost $1 + \gamma(\ell) + \gamma(d)$ bits, where $\gamma(x) = 2\lfloor \log_2 x \rfloor + 1$ is the length of the [Elias gamma code](/elias-gamma-coding/). For `aabbaa` the greedy parse above costs $9 + 3 + 9 + 3 + 9 = 33$ bits, because copy (2, 4) costs $1 + 3 + 5 = 9$. Replace it by copy (1, 3) and copy (1, 1), which cost $5 + 3 = 8$, and the total is 32 bits, the minimum.

**A minimum copy length.** With $\ell_{\min} = 3$ and $t$ = `aaabaaaaa`, greedy writes 4 literals, takes copy (3, 4) at position 4, and then needs 2 literals for the last `aa`: 7 phrases. The parse with 5 literals and copy (4, 1) at position 5 has 6 phrases.

## Variations

- **Lazy matching.** Before taking the match at $i$, look at the match at $i+1$; if it is longer, write $t[i]$ as a literal and move on. See [lazy matching](/lazy-matching/).
- **Optimal parsing.** Compute the parse of minimum total cost with dynamic programming over the positions. See [optimal parsing](/optimal-parsing/) for general dictionaries and [optimal LZ parsing](/optimal-lz-parsing/) for LZ77 with a cost in bits.
- **Flexible parsing.** For a prefix-closed static dictionary, choose at each step the phrase whose end gives the longest next phrase. It is optimal in phrase count for such dictionaries; see [optimal parsing](/optimal-parsing/).
- **Bounded search.** Limit the chain length or the tree depth of the match finder to trade compression for speed.

## Pitfalls

- **Greedy is not bit-optimal.** In the worked example above, two short copies cost 1 bit less than one long copy. Ferragina, Nitto and Venturini give a family of strings on which greedy uses more bits than the optimum by a factor $\Omega(\log n / \log \log n)$ for a cost model with variable-length integer codes.
- **A minimum copy length breaks optimality in phrase count.** With $\ell_{\min} = 3$, a long early copy can leave a gap of 1 or 2 symbols, which costs one or two literals.
- **Static dictionaries.** With $D = \{a, b, c, d, ab, bcd\}$ and $t$ = `abcd`, greedy gives `ab`, `c`, `d` (3 phrases) but `a`, `bcd` has 2. Greedy can also get stuck if $D$ does not contain each single symbol.
- **Ties in length.** Take the smallest distance among the longest matches. The phrase count does not change, but a short distance costs fewer bits in every common code.
- **Heuristic match finders.** An encoder with a chain limit does not compute the greedy parse; the optimality claim is about the exact longest match.

## Exercises

1. Let $z_T$ be the number of phrases of the greedy LZ77 parse into triples (a copy followed by one symbol), and $z_C$ the number for the greedy parse into literals and copies, with the same window. Show that $z_T \le z_C \le 2 z_T$.
2. Give a static dictionary that is closed under prefixes, contains each single symbol, and is not closed under suffixes, and a text on which greedy is not optimal in phrase count. (One answer: $\{a, b, c, d, ab, bc, bcd\}$ and `abcd`.)

## References
