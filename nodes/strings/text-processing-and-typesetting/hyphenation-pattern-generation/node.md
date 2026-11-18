---
tag: 980NJ6
kind: algorithm
slug: hyphenation-pattern-generation
name: Hyphenation pattern generation
aliases:
- patgen
area: strings/text-processing-and-typesetting
level: advanced
summary: Learn hyphenation patterns from a hyphenated word list in levels, greedily keeping patterns whose good matches outweigh bad ones at each level.
solves: [hyphenation-problem]
model: word-ram
complexity:
  vars: {N: the total number of letters of the word list, P: the number of passes, L: the length of the longest pattern, Q: the total length of the patterns}
  time: {worst: O(P N L^2)}
  space: {extra: O(N L + Q)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1983
  people: [Franklin Mark Liang]
  note: Liang wrote the pattern generator patgen for his Stanford thesis of 1983 and used it to make the English patterns of TeX82.
prereqs: [liang-hyphenation]
see_also: [hyphenation-problem, packed-trie, trie, greedy-algorithm, decision-tree, overfitting]
sources:
  - url: http://bitsavers.trailing-edge.com/pdf/stanford/Stanford_CS_TR_Collection_2025-12-12/PDF/1983/CS-TR-83-977.pdf
    title: "Franklin Mark Liang, Word Hy-phen-a-tion by Com-put-er, PhD thesis, Stanford University, August 1983, report STAN-CS-83-977"
    locator: "Chapter 4, Pattern generation (the word list, the levels, the selection rule, the dynamic packed trie) and Table 5 (the parameters and the results for TeX82)"
  - book: isbn:0201134470
    title: "Donald E. Knuth, The TeXbook, Computers and Typesetting volume A, Addison-Wesley"
    locator: "Appendix H, Hyphenation"
---

Hyphenation pattern generation learns the patterns of [Liang's hyphenation](/liang-hyphenation/) from a list of words with their hyphens marked. It works in levels. Odd levels add patterns that allow hyphens, and even levels add patterns that forbid them, each one able to overrule the levels below it. Inside a level, it tries all strings of a given length with the digit at a given gap, counts on how many gaps of the list each one would help and hurt, and keeps the strings whose weighted score reaches a threshold. Franklin Liang wrote it as the program patgen in 1983, and it made the English patterns of TeX82.

## In plain words

Suppose you want short rules such as "put a hyphen before ti" that explain a hyphenated word list. Start with no rules. Look at every gap of every word where the rules are still wrong. For each short piece of letters around such a gap, count how often a new rule on that piece would fix a gap and how often it would break one. Keep the pieces that fix much more than they break.

The first rules are too general and make some wrong hyphens. So the next level looks for rules that forbid hyphens, and only where the current rules are wrong. Then a third level allows hyphens again, and so on. Each level fixes some of the errors of the level below, which is how a short list of patterns can describe a long list of words.

## The problem

The input is a list of words $w$ with their sets $H(w)$ of correct hyphen positions, and for each level $\ell = 1, 2, \ldots$ the parameters $\gamma_\ell$ (the good weight), $\delta_\ell$ (the bad weight), $\theta_\ell$ (the threshold) and a range $k_{\min} \ldots k_{\max}$ of pattern lengths. The limits $\lambda$ and $\rho$ select the counted gaps: a gap $g$ of a word of $n$ letters is counted when $g \ge \lambda$ and $n - g \ge \rho$. The output is a set of patterns, each a string of letters (with "." for a word edge) and a digit for each gap. The aim is a small set whose values, by Liang's rule, are odd on the correct hyphens and even elsewhere, for as many counted gaps as possible. It is a method for building a solution of the [hyphenation problem](/hyphenation-problem/); it does not promise the smallest set or the best one.

At level $\ell$, with the patterns $\Pi$ chosen so far, call a counted gap *now* if its value under $\Pi$ is odd. Then:

- at an odd level, a gap is *good* if it is a correct hyphen and not now, and *bad* if it is not a correct hyphen and not now;
- at an even level, a gap is *good* if it is not a correct hyphen but now, and *bad* if it is a correct hyphen and now.

A string $q$ with the dot at its gap $d$ is kept when $\gamma \cdot \mathrm{good}(q) - \delta \cdot \mathrm{bad}(q) \ge \theta$, where the counts are over the gaps where $q$ occurs with its gap $d$ on them.

## The algorithm

```pseudo id=main
GENERATE(list, levels)
G1  Π ← the empty set of patterns
G2  for each level ℓ = 1, 2, ... with parameters (γ, δ, θ, kmin, kmax) do
G3      for k ← kmin to kmax do
G4          for d ← 0 to k do                   ▷ one pass for each dot position
G5              good[·] ← 0; bad[·] ← 0
G6              for each word w of the list do
G7                  v ← the gap values of w under Π, by Liang's rule
G8                  for each counted gap g of w that is good or bad at level ℓ do
G9                      q ← the k letters of .w. that have their gap d on g
G10                     add 1 to good[q] or to bad[q]
G11             for each string q with a count do
G12                 if γ · good[q] - δ · bad[q] ≥ θ then
G13                     put the digit ℓ at gap d of q in Π (keep the larger digit)
G14 return Π
```

Line G7 hyphenates each word with the patterns chosen so far, so every pass sees the effect of all earlier passes, also those of the same level. Line G9 finds the one string of length $k$ that has its gap $d$ on the gap $g$; near the edges of the word, the string may contain a "." and there may be no such string. Lines G11 to G13 run after all words are counted, so the patterns of a pass do not change its own counts. A pattern of length $k$ takes $k + 1$ passes, one for each position of its digit.

## Example

The word list for this example has 32 English words made up for the page (the tests of this page use it), with 38 correct hyphens, for example hy-phen-ation, com-put-er, mon-ster and ta-ble. The limits are $\lambda = \rho = 2$. The three levels are:

| level | $\gamma$ | $\delta$ | $\theta$ | lengths | passes | patterns kept | found | errors | missed |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 1 | 2 | 2 to 3 | 7 | 7 | 27 | 3 | 11 |
| 2 | 1 | 2 | 1 | 2 to 4 | 12 | 3 | 27 | 0 | 11 |
| 3 | 1 | 100 | 1 | 2 to 8 | 42 | 11 | 38 | 0 | 0 |

**Level 1.** In the first pass ($k = 2$, $d = 0$, so the hyphen goes before the two letters), "te" sits after 11 good gaps and 2 bad ones, so its score is $11 - 2 = 9 \ge 2$ and 1te is kept. "ti" scores $6 - 1 = 5$. "er" is after 1 good gap and 15 bad ones, so it is rejected. The length-2 passes keep 1be, 1bl, 1ce, 1te, 1ti, n1a and n1s, and the length-3 passes add nothing. These seven patterns find 27 of the 38 hyphens but make 3 errors: hyphen-a-tion (the hyphen before "tion" is wrong), compu-ter and mon-s-ter.

**Level 2.** Now the good gaps are the 3 errors. The level keeps ena2, u2t and n1s2 (the digit 2 is added to the existing pattern n1s), which remove all three errors and keep the 27 correct hyphens.

**Level 3.** The bad weight is 100, so a pattern is kept only if it makes no wrong hyphen. The level adds 3co, 3de, 3gi, 3go, 3gr, 3ph, 3pu, r3e, 3ri, 3va and a 3 at the end of u2t, which gives u2t3. Now com-put-er gets its hyphen before "p" from 3pu and after "t" from u2t3. The final 19 patterns hyphenate all 38 gaps of the list correctly, and give no wrong hyphen. On words outside the list they can be wrong: the list is far too small for real use.

## Correctness

The claim is that each pass keeps exactly the strings that meet the rule of line G12 for the counts of the claim, under the patterns from before the pass. Line G7 computes the values by Liang's rule, so "now" is right. Line G8 sees each counted gap once, and a gap cannot be both good and bad. For a gap $g$ and a dot $d$, the only string of length $k$ with its gap $d$ on $g$ starts at position $g + 1 - d$ of ".$w$.", so line G10 adds each good or bad gap to exactly one count. Lines G11 to G13 then apply the rule, and adding a digit by the maximum is the same as having two patterns, because Liang's rule takes the maximum. Each pass reads the list once, so the method stops after $\sum_\ell \sum_k (k+1)$ passes. The full proof is in the proof file.

This is correctness of the procedure, not of its result. The rule is a heuristic, and whether the final patterns are right on the whole list depends on the parameters.

## Complexity

Let $N$ be the number of letters of the list and $P$ the number of passes. One pass computes the gap values of each word, which takes $O(n L^2)$ for a word of $n$ letters with a lookup of each substring of length at most $L$, and it counts each gap once. So a pass takes $O(N L^2)$, and the run takes $O(P N L^2)$ time. Space is $O(N L)$ for the counts of one pass, plus the patterns. With a trie of the patterns, as in patgen, the values cost $O(n L)$ per word instead.

Liang's TeX82 run took 109 passes and about one hour of computer time (his measurement on a 1983 machine).

## Properties

- **Greedy.** Each pass keeps every string that meets the rule, and never takes a pattern back. A later level can only overrule it with a larger digit.
- **Levels alternate.** Odd levels only add hyphens and even levels only remove them, because a digit $\ell$ is odd exactly at odd levels and is larger than all earlier digits.
- **Order dependent.** The result depends on the order of the levels, the lengths and the dot positions, because each pass sees the patterns of the passes before it.
- **Trade-off by weights.** A high bad weight gives safe patterns that miss hyphens; a high good weight gives patterns that find more hyphens with more errors.

## Variants and improvements

- **Liang's parameters for TeX82.** Liang used five levels, with good weight, bad weight and threshold 1, 2, 20 (level 1), 2, 1, 8 (level 2), 1, 4, 7 (level 3), 3, 2, 1 (level 4) and 1, infinity, 4 (level 5), and pattern lengths of up to 4, 4, 5, 6 and 8. The levels kept 458, 509, 985, 1647 and 1320 patterns: 4919 in all, of which 4447 are distinct strings. They pack into a [packed trie](/packed-trie/) of 5943 locations with 181 different digit lists, and find 89.3 percent of the hyphens of his list. These are his measurements on that list.
- **Counting in a trie.** patgen keeps the patterns and the candidate counts in a dynamic packed trie, not in a hash map, to save memory on a large list.
- **Skipping useless candidates.** A string that already has a digit of at least $\ell$ at gap $d$ cannot change anything at level $\ell$, so an implementation can drop it before it counts.
- **Exceptions.** Words that the patterns still get wrong go into an exception list, as \hyphenation in TeX.
- **Weighted lists.** A word can count more than once, for example by its frequency in a body of text, so that common words get more weight.

## When to use it

Use it to make a pattern set for a language from a hyphenated word list, when the patterns will be used by Liang's method, as in TeX and many word processors. The list must be large and correct, because the patterns learn its errors too. If only a fixed set of words is ever hyphenated, a lookup in the list itself is simpler and exact.

## Pitfalls

- **Overfitting.** With a bad weight of 100 and long patterns, the last levels can learn single words, as in the example. The patterns are then exact on the list and no better than chance on new words. Test them on words that were not in the list.
- **Counting with the new patterns.** If line G13 adds patterns during the counting loop, the counts of the same pass change while they are being made, and the result depends on the order of the words.
- **Forgetting the edges.** Without the "." marks, no pattern can depend on the start or the end of a word, and the method misses rules such as "no hyphen after the first letter".
- **Different limits.** The counted gaps of line G8 must use the same $\lambda$ and $\rho$ as the typesetter, or the counts include gaps that are never used.

## Implementations

## History

The first TeX used rules on letter classes for hyphenation. Liang, a student of Donald Knuth at Stanford, replaced them with patterns and wrote patgen to learn them; his thesis of 1983 describes the method and the TeX82 run on a word list based on Webster's Pocket Dictionary, with the 676 most common words fully hyphenated and over 1000 exceptions added after a test on a larger dictionary. The same program was later used to make the pattern sets of many other languages in the TeX distributions.

## References
