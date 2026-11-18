---
tag: 6YQPVW
kind: algorithm
slug: liang-hyphenation
name: Liang's hyphenation algorithm
aliases:
- Knuth-Liang hyphenation
- pattern-based hyphenation
area: strings/text-processing-and-typesetting
level: core
summary: Match all hyphenation patterns of a language against the word, take the largest digit at each gap, and allow a break where it is odd.
solves: [hyphenation-problem]
model: word-ram
complexity:
  vars: {k: the number of letters of the word, l: the length of the longest pattern, P: the total length of the patterns}
  time: {worst: O(k l^2), best: Θ(k)}
  space: {extra: Θ(k), trie: O(P)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1983
  people: [Franklin Mark Liang]
  note: Liang developed the method and its pattern generator in his Stanford thesis of 1983, and TeX82 adopted it.
prereqs: [hyphenation-problem, trie]
see_also: [packed-trie, hyphenation-pattern-generation, dictionary-matching, aho-corasick, box-glue-penalty-model, knuth-plass-line-breaking]
sources:
  - url: http://bitsavers.trailing-edge.com/pdf/stanford/Stanford_CS_TR_Collection_2025-12-12/PDF/1983/CS-TR-83-977.pdf
    title: "Franklin Mark Liang, Word Hy-phen-a-tion by Com-put-er, PhD thesis, Stanford University, August 1983, report STAN-CS-83-977"
    locator: "Chapter 3 (hyphenation by patterns, the rule of the largest digit) and Table 5 (the TeX82 patterns)"
  - book: isbn:0201134470
    title: "Donald E. Knuth, The TeXbook, Computers and Typesetting volume A, Addison-Wesley"
    locator: "Appendix H, Hyphenation (the example with hyphenation and the patterns command)"
  - book: isbn:0201134373
    title: "Donald E. Knuth, TeX: The Program, Computers and Typesetting volume B, Addison-Wesley, 1986"
    locator: "the parts on hyphenation and on the initialization of the pattern memory"
---

Liang's hyphenation algorithm decides where a word may be hyphenated from a set of short letter patterns. Each pattern holds a digit in each gap between its letters. The algorithm finds every pattern that occurs in the word, takes the largest digit at each gap, and allows a hyphen where this value is odd. Franklin Liang designed it in 1983 for TeX82, and TeX and many other programs still use it. With about 4500 patterns in a table of about 25K bytes, his English set finds 89 percent of the hyphens of his word list with almost no errors (a measurement on that list).

## In plain words

Think of each pattern as a small vote on a few gaps of a word. The pattern "hy3ph" says: when you see the letters h, y, p, h together, the gap between y and p gets a 3. An odd number is a vote for a hyphen and an even number is a vote against it. Larger numbers beat smaller ones, so a later pattern can overrule an earlier rule with an exception.

To hyphenate a word, put a dot at each end, find every pattern that occurs anywhere in it, and write the largest number at each gap. Then put a hyphen at each odd gap that is not too near the ends. A [trie](/trie/) of the patterns makes the search fast.

## The problem

The input is a word $u$ of $k$ letters, a set $P$ of patterns, and the limits $\lambda$ and $\rho$ (\lefthyphenmin and \righthyphenmin; plain TeX uses 2 and 3). A pattern is a string of letters $q_0 \cdots q_{m-1}$ with a digit $d[0], \ldots, d[m]$ in each of its $m + 1$ gaps; a missing digit is 0. The letter "." stands for the edge of the word, so ".ach4" matches only at the start. The output is the set of positions $j$ ($1 \le j \le k-1$, a hyphen before letter $j$) whose value is odd and with $j \ge \lambda$ and $k - j \ge \rho$. The value of a gap is the largest digit that any occurrence of a pattern in ".$u$." places on it, or 0. This is a method for the [hyphenation problem](/hyphenation-problem/).

## The algorithm

The patterns are stored in a trie whose node for the letters $q$ holds the digits $d$ when $q$ is a pattern.

```pseudo id=main
LIANG-HYPHENATE(word, trie, λ, ρ)
L1  u ← "." + lowercase(word) + "."
L2  v[0 .. |u|] ← 0
L3  for i ← 0 to |u| - 1 do                ▷ every start position
L4      node ← root of trie
L5      for j ← i to |u| - 1 do
L6          node ← child of node on u[j]
L7          if node = nil then break        ▷ no pattern starts with u[i .. j]
L8          if node holds digits d[0 .. j - i + 1] then
L9              for t ← 0 to j - i + 1 do v[i + t] ← max(v[i + t], d[t])
L10 return the positions p with v[p + 1] odd, λ ≤ p and k - p ≥ ρ
```

Line L1 adds the edge marks. The outer loop of line L3 tries each start position, and the walk of lines L5 to L7 follows the letters of $u$ from there down the trie, so it visits exactly the patterns that occur at $i$, from short to long. It stops as soon as no pattern can be longer. Line L9 raises each gap that the pattern covers to the digit of the pattern. Gap $p + 1$ of $u$ is the gap before letter $p$ of the word, which gives the shift in line L10.

TeX also keeps an exception list, set with \hyphenation; a word in this list gets its listed positions, and the patterns are not used.

## Example

The patterns of TeXbook Appendix H are hy3ph, he2n, hena4, hen5at, 1na, n2at, 1tio, 2io and o2n. The word is "hyphenation", so $u$ = .hyphenation. The patterns that occur, and the gaps of the word they set (gap $p$ is before letter $p$, counting from 0):

| start in $u$ | pattern | letters it covers | digits it sets |
|---|---|---|---|
| 1 | hy3ph | h y p h | gap 2 = 3 |
| 4 | he2n | h e n | gap 5 = 2 |
| 4 | hena4 | h e n a | gap 7 = 4 |
| 4 | hen5at | h e n a t | gap 6 = 5 |
| 6 | 1na | n a | gap 5 = 1 |
| 6 | n2at | n a t | gap 6 = 2 |
| 8 | 1tio | t i o | gap 7 = 1 |
| 9 | 2io | i o | gap 8 = 2 |
| 10 | o2n | o n | gap 10 = 2 |

At start 4 the walk visits he, hen, hena and henat in one pass and finds three patterns on the way. The largest digit per gap gives, for the gaps 1 to 10 (before y, p, h, e, n, a, t, i, o, n):

| gap | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| value | 0 | 3 | 0 | 0 | 2 | 5 | 4 | 2 | 0 | 2 |

The odd gaps are 2 and 6, both inside the limits $\lambda = 2$ and $\rho = 3$, so the result is hy-phen-ation. The gap 7 (before "tion") gets 1 from 1tio but 4 from hena4, and the even value wins, so "a-tion" is not allowed. The dictionary has a hyphen there, so this is a miss, the safe kind of mistake. The run takes 33 trie steps for the 13 start positions.

## Correctness

The claim is that line L9 leaves in $v$ exactly the value of each gap, the largest digit of all patterns that occur in $u$ and cover it. The invariant of the inner loop is that, before line L6 at step $j$, `node` is the trie node of $u[i \ldots j-1]$. So the walk from $i$ meets every pattern that starts at $i$, and stops only when no pattern can start with $u[i \ldots j]$. Each update is a maximum with a digit of a real occurrence, so no value is too large, and every occurrence is met, so none is too small. The full proof is in the proof file.

## Complexity

In the [word RAM](/word-ram/) with a child lookup in $O(1)$ time (an array per node or a [packed trie](/packed-trie/)):

- **Time.** Line L3 runs $k + 2$ times. The walk from $i$ is at most as deep as the trie, so it takes at most $l$ steps, where $l$ is the length of the longest pattern. Line L9 costs at most $l + 1$ updates per pattern found, and at most $l$ patterns start at each $i$. So the time is $O(k l)$ trie steps plus $O(k l^2)$ updates in the worst case. If no bound on $l$ is known, the walk is bounded by $|u| - i$ and the trie steps by $(k+2)(k+3)/2 = O(k^2)$; the test `test_trie_steps_are_at_most_quadratic` checks this bound. The best case is $\Theta(k)$, when no letter of $u$ starts a pattern. Table 5 of Liang lists TeX82 patterns of length at most 8, so for English the cost is linear in $k$ with a small constant.
- **Space.** The array $v$ takes $\Theta(k)$. The trie takes $O(P)$ nodes for patterns of total length $P$.

## Properties

- **Order free.** The value of a gap is a maximum, so the result does not depend on the order of the patterns or of the start positions.
- **Exceptions by levels.** A pattern with a larger digit overrules all smaller ones on its gap. Odd levels allow and even levels forbid, so the patterns form a list of rules with exceptions and exceptions to exceptions.
- **Works on unknown words.** The patterns describe parts of words, so they also give results for words that were not in the training list. These results can be wrong.
- **Deterministic and static.** The result depends only on the word and the patterns.

## Variants and improvements

- **Automaton search.** Build an [Aho-Corasick](/aho-corasick/) automaton of the patterns. One pass over $u$ then reports all occurrences, in $O(k + z)$ time for $z$ occurrences. TeX uses the simpler walk, because words are short.
- **Packed storage.** TeX82 stores the pattern trie as a [packed trie](/packed-trie/) with suffix compression, so that each step is one table lookup.
- **Several languages.** TeX3 keeps one pattern set per language and selects it with \language.
- **Breaks that change the spelling.** Some pattern libraries for word processors add a way to give a replacement text at a break, for words such as the old German "Zuk-ker" from "Zucker".
- **Learning the patterns.** The patterns are not written by hand. [Hyphenation pattern generation](/hyphenation-pattern-generation/) learns them from a hyphenated word list.

## When to use it

Use it when the program must hyphenate any word, including words that no list holds, in little space. It needs a pattern set for the language; such sets exist for many languages in the TeX distributions. Use a lookup in a hyphenated word list instead when the words are known in advance and every hyphen must be correct, for example in a fixed glossary. Use a list of exceptions together with the patterns to fix the errors that matter.

## Pitfalls

- **Missing the edge marks.** If line L1 does not add ".", the patterns that start or end with "." never match, and words lose the hyphens that depend on their first or last letters. The patterns of `test_against_brute_force_on_random_patterns` include edge marks, so this test catches the error.
- **Stopping at the first pattern.** If the walk of line L5 stops when line L8 finds a pattern, it misses the longer patterns at the same start. In the example, it would stop at he2n and miss hena4 and hen5at, and give "hy-phenation".
- **Adding or overwriting instead of the maximum.** Line L9 must take the maximum. With the last digit or the sum, the result depends on the order of the patterns.
- **Off by one in the gaps.** Gap $p + 1$ of $u$ is the gap before letter $p$ of the word (line L10). With $v[p]$ the hyphens move one letter to the left.
- **Applying the limits to $u$.** $\lambda$ and $\rho$ count letters of the word, not of $u$ with its two marks.
- **Duplicates.** When a pattern set lists the same letters twice, the digits must be merged by the maximum per gap, not replaced.

## Implementations

## History

The first TeX used rules on letter classes and a list of about 300 exceptions, and found about 40 percent of the hyphens of a pocket dictionary with about 1 percent errors (Liang's measurement). Liang, a student of Donald Knuth at Stanford, replaced it with the pattern method and wrote patgen to learn the patterns. His thesis of 1983 reports 4447 distinct patterns for TeX82, in a packed trie of 5943 locations, that find 89.3 percent of the hyphens of his copy of Webster's Pocket Dictionary with essentially no errors. These numbers are measurements on that one word list. The method became part of TeX82 and is described in Appendix H of the TeXbook.

## References
