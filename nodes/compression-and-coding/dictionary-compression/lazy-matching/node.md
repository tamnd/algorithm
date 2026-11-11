---
tag: XTSE0P
kind: technique
slug: lazy-matching
name: Lazy matching
aliases:
- lazy evaluation of matches
area: compression-and-coding/dictionary-compression
level: core
summary: An LZ77 parsing rule that holds back a match at position i, takes the match at i + 1 instead if it is longer, and emits t[i] as a literal.
prereqs: [greedy-parsing, match-finding]
see_also: [deflate, lz77, lzss, optimal-lz-parsing, optimal-parsing, zstandard]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc1951
    title: L. Peter Deutsch, RFC 1951, DEFLATE Compressed Data Format Specification version 1.3, May 1996
    locator: Section 4, Compression algorithm details (lazy matching, and the rule that a long enough match reduces or ends the search for a longer one)
  - url: https://github.com/madler/zlib/blob/v1.2.12/deflate.c
    title: Jean-loup Gailly and Mark Adler, zlib 1.2.12, deflate.c, 2022
    locator: "the header comment (credit for lazy evaluation), configuration_table (good_length, max_lazy, nice_length, max_chain per level), deflate_slow, deflate_fast, longest_match and the TOO_FAR rule"
  - paper: doi:10.1137/120869511
    title: Paolo Ferragina, Igor Nitto and Rossano Venturini, On the bit-complexity of Lempel-Ziv compression, SIAM Journal on Computing 42(4), 1521-1541, 2013
    locator: Section 1 (greedy and its heuristic variants against the bit-optimal parse)
---

Lazy matching is a rule for the parse of an [LZ77](/lz77/) style compressor. When the encoder finds a match at position $i$, it does not take it at once. It first searches at $i+1$. If the match there is longer, it writes $t[i]$ as a literal and keeps the new match in hand; else it takes the match at $i$. The rule is due to Jan-Mark Wams and is the parse of zlib and gzip at compression levels 4 to 9. It often beats [greedy parsing](/greedy-parsing/) in output size, but not always, and it costs about one match search per input position.

## In plain words

You copy a text and you replace repeated words by "copy from earlier". The greedy writer takes the longest copy that starts here, at once. The lazy writer is more careful. Before it takes the copy, it looks one letter further on. If a longer copy starts there, it writes the current letter by itself and takes the longer copy one step later.

The extra look costs time, because the writer now searches at almost every letter. It helps when a short copy at one place would hide a long copy that starts just after it. It can also hurt, because the longer copy may end at a bad place for the next copy.

zlib lets you set how far to go with this. When the copy in hand is already long, the writer skips the extra look or searches less.

## When it applies

The input is a string $t = t[0 \ldots n-1]$ of bytes ($\sigma = 256$). The encoder writes literals and copies (length $\ell$, distance $d$) with a minimum copy length $\ell_{\min}$ (3 in [DEFLATE](/deflate/)) and a window. The cost of a phrase in bits is set later by the entropy coder, so the encoder cannot measure it during the parse.

For LZ77 copies with no minimum length and equal phrase costs, [greedy parsing](/greedy-parsing/) already gives the fewest phrases, and lazy matching cannot do better. Lazy matching is useful when that result does not hold: with $\ell_{\min} > 1$, as in DEFLATE, a short greedy copy can cover the start of a longer copy, and with costs in bits, one long copy is usually cheaper than a short copy and a literal. Lazy matching is a heuristic for these cases. It looks one position ahead. An [optimal parser](/optimal-lz-parsing/) looks at all positions and is slower.

## The template

This is the rule of zlib's `deflate_slow`. The pair `prev` holds the match found at position $i-1$, and `pending` says that $t[i-1]$ is not yet written. A length of 2 stands for "no match".

```pseudo id=main
LAZY-PARSE(t)                                         ▷ zlib deflate_slow
L1  i ← 0; cur ← (2, 0); pending ← false
L2  while i < n do insert position i into the match finder
L3      prev ← cur                                    ▷ the match at i − 1
L4      if prev.ℓ < max_lazy and a candidate exists then
L5          cur ← LONGEST-MATCH(i, prev.ℓ)            ▷ hole: only a match longer than prev.ℓ counts
L6          if cur.ℓ = 3 and cur.d > TOO_FAR then cur ← (2, 0)
        else cur ← (2, 0)
L7      if prev.ℓ ≥ 3 and cur.ℓ ≤ prev.ℓ then         ▷ no better match at i: take prev
L8          emit the copy prev, which starts at i − 1
L9          insert the positions inside it; i ← i − 1 + prev.ℓ; pending ← false; cur ← (2, 0)
L10     else if pending then                          ▷ t[i − 1] is not part of a taken match
L11         emit the literal t[i − 1]; i ← i + 1
L12     else
L13         pending ← true; i ← i + 1
L14 if pending then emit the literal t[n − 1]
```

The holes are the [match finder](/match-finding/) of line L5 and four numbers. zlib passes `prev.ℓ` into the search as the length to beat, and the search also uses two of the numbers:

- `max_lazy`: when the match in hand has at least this length, line L4 skips the search at $i$, and the match is taken.
- `good_length`: when the match in hand has at least this length, the search at $i$ walks only a quarter of the usual chain.
- `nice_length`: the search stops as soon as it finds a match of this length.
- `max_chain`: the number of hash chain entries the search may check.

Line L6 is the `TOO_FAR` rule of zlib: a copy of length 3 at a distance above 4096 is dropped, because three literals are usually cheaper. The levels of zlib 1.2.12 that use this loop are:

| Level | good_length | max_lazy | nice_length | max_chain |
|---|---|---|---|---|
| 4 | 4 | 4 | 16 | 16 |
| 5 | 8 | 16 | 32 | 32 |
| 6 (default) | 8 | 16 | 128 | 128 |
| 7 | 8 | 32 | 128 | 256 |
| 8 | 32 | 128 | 258 | 1024 |
| 9 | 32 | 258 | 258 | 4096 |

Levels 1 to 3 use `deflate_fast`, a greedy loop with no lazy search. There the `max_lazy` field has a different meaning: the positions inside a match are put into the hash chains only when the match is at most that long. Level 0 writes stored blocks.

**Cost.** Each loop step does at most one search, and the search at $i$ also serves as the look ahead for the match at $i-1$. So the number of searches is at most $n$, against one per phrase for greedy parsing. Each search costs $O(\texttt{max\_chain} \cdot \ell_{\max})$ byte comparisons in the worst case, with $\ell_{\max} = 258$ for DEFLATE. The extra memory is that of the match finder.

## Classic examples

- [DEFLATE](/deflate/) in zlib, and so in gzip and PNG: levels 4 to 9 use the loop above. RFC 1951 Section 4 describes the rule as a recommendation; the format does not require any parse.
- [Zstandard](/zstandard/): its strategies `lazy` and `lazy2` look one and two positions ahead, and `btlazy2` does the same with a binary tree match finder.
- [LZSS](/lzss/) style formats in general: any format with a minimum copy length and a literal case can use the rule, because the decoder does not see the parse rule.
- The programs `comic` by Jan-Mark Wams and `freeze` by Leonid Broukhis, which the zlib source names as the origin of the idea.

### Worked examples

All the tokens here come from the implementation in `impl/python`, and the tests check that zlib 1.2.12 makes the same tokens.

**Lazy matching wins.** Let $t$ = `yabcxbcdeabcde` (positions 0 to 13), with no chain limit. Positions 0 to 8 give literals, because no match of length 3 exists there. Then:

| Step at $i$ | prev (match at $i-1$) | cur (match at $i$) | Action |
|---|---|---|---|
| 9 | none | (3, 8): `abc` from position 1 | emit literal `e` = $t[8]$ |
| 10 | (3, 8) | (4, 5): `bcde` from position 5 | longer: emit literal `a` = $t[9]$ |
| 11 | (4, 5) | no match longer than 4 | emit copy (4, 5) for $t[10 \ldots 13]$; stop |

The lazy parse has 9 literals, the literal `a`, and copy (4, 5): 11 tokens. The greedy parse takes copy (3, 8) at position 9 and then needs literals for `d` and `e`: 12 tokens. zlib makes the lazy parse at each level from 4 to 9.

**Lazy matching loses.** Let $t$ = `baaadaaaaad`. Greedy writes `baaad` as literals, then copy (3, 4) at position 5 and copy (3, 6) at position 8: 7 tokens. At position 5 the lazy rule sees copy (4, 1) at position 6, which is longer than (3, 4). So it writes `a` as a literal, takes copy (4, 1) for positions 6 to 9, and then needs a literal for the last `d`: 8 tokens. zlib at level 6 makes the same 8 tokens.

**A long run.** For 1000 bytes `a`, zlib at level 6 writes two literals and then copies (258, 1). It never uses position 0 as a source, because it uses 0 as the end marker of the hash chains, so the first copy starts at position 2 with source 1.

## Variations

- **Look further ahead.** Search at $i+1$ and $i+2$ (Zstandard's `lazy2`), and take the best. Each extra step costs one more search per position.
- **Compare costs, not lengths.** Estimate the bits of each choice with the current Huffman or entropy statistics and pick the cheaper one. This moves the rule toward [optimal LZ parsing](/optimal-lz-parsing/).
- **Optimal parsing.** Compute the cheapest parse over all choices by dynamic programming. LZMA and Zstandard's `btopt` and `btultra` strategies do this, at a much higher cost per byte.
- **Greedy with skipped insertions.** zlib's levels 1 to 3 drop the look ahead and also skip the insertion of positions inside long matches, which makes the match finder faster and weaker.

## Pitfalls

- **Lazy is not always better.** The second worked example has one token more than greedy. The rule compares lengths, not the cost of the rest of the parse.
- **The comparison is strict.** zlib emits the held match when the new match has the same length (line L7 uses $\le$). If ties go to the new match, the parse writes a literal and gains nothing.
- **Insert every position.** The positions inside a taken match must still go into the match finder (line L9), or later searches miss sources in that range. zlib's fast levels skip some of them on purpose.
- **Position 0.** An implementation that wants the same output as zlib must also never use position 0 as a source, and must apply `good_length`, `nice_length` and `TOO_FAR` in the same way. The tests compare token by token with zlib for this reason.
- **The window.** zlib limits the distance to 32506, not 32768, because it keeps 262 bytes of look ahead in its 32 KiB half window. The tests use inputs shorter than this, so the window never matters there.

## References
