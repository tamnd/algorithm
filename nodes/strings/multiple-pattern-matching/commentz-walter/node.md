---
tag: 1K05ZQ
kind: algorithm
slug: commentz-walter
name: Commentz-Walter algorithm
aliases:
- Commentz-Walter multiple pattern matching
area: strings/multiple-pattern-matching
level: advanced
summary: Multi-pattern generalization of Boyer-Moore that scans the text right to left with shifts from a reversed trie.
solves: [multiple-string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the total length of the patterns, w: the shortest nonempty pattern length, L: the largest pattern length, z: the number of occurrences}
  time: {build: O(m), worst: O(n·L + z), best: O(n/w + z)}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1979
  people: [Beate Commentz-Walter]
  note: Presented at ICALP 1979. GNU fgrep 2.0 and Hume's gre were based on it, according to Wu and Manber (1994).
prereqs: [boyer-moore, trie, failure-link, multiple-string-matching]
see_also: [aho-corasick, set-horspool, wu-manber, good-suffix-rule, bad-character-rule, boyer-moore-horspool, block-shift-table, dictionary-matching]
sources:
  - paper: doi:10.1007/3-540-09510-1_10
    title: Beate Commentz-Walter, A string matching algorithm fast on the average, Automata, Languages and Programming (ICALP 1979), Lecture Notes in Computer Science 71, 118-132
    locator: the trie of the reversed patterns, the right-to-left scan, and the shift functions built from it
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 3, Multiple string matching (Commentz-Walter among the suffix-based algorithms, with Set Horspool as its simplification)
  - url: https://www.cs.arizona.edu/sites/default/files/TR94-17.pdf
    title: Sun Wu and Udi Manber, A fast algorithm for multi-pattern searching, Technical Report TR 94-17, Department of Computer Science, University of Arizona, May 1994
    locator: Section 1 (Commentz-Walter as the basis of gre and GNU fgrep 2.0) and Section 3 (experiments against Commentz-Walter)
  - paper: doi:10.1145/359842.359859
    title: Robert S. Boyer and J Strother Moore, A fast string searching algorithm, Communications of the ACM 20(10) (1977), 762-772
    locator: the two shift heuristics for one pattern, which Commentz-Walter extends to a set
---

The Commentz-Walter algorithm finds all occurrences of a set of patterns by carrying the ideas of [Boyer-Moore](/boyer-moore/) over to the [trie](/trie/) used by [Aho-Corasick](/aho-corasick/). It places a window whose length $w$ is that of the shortest pattern, reads the text from the window end to the left through the trie of the reversed patterns, reports each pattern whose reverse it spells, and then shifts the window by the largest distance that three precomputed functions prove safe. Two of them play the role of the [good-suffix rule](/good-suffix-rule/), one for patterns that contain the matched part and one for patterns that overlap it, and the third is the [bad-character rule](/bad-character-rule/) for the character that stopped the reading. On typical text with few patterns it reads only a fraction of the characters, but its worst case is $\Theta(nL)$.

## In plain words

Put a frame as long as the shortest pattern at the start of the text. Read the text backward from the right end of the frame, and follow a tree that holds all patterns written backward. Each time the letters read spell a whole pattern backward, report it.

When the reading stops, two things are known: the letters that matched, and the letter that did not. Each of them rules out many places where a pattern could end next. The method moves the frame to the first place that neither of them rules out. To make this fast, the safe moves are computed once, before the search, for each node of the tree and each letter.

## The problem

Given a text $T = T[0 \ldots n-1]$ and patterns $P_0, \ldots, P_{k-1}$, output every pair $(s, j)$ with $T[s \ldots s + |P_j| - 1] = P_j$. Indices are 0-based. Occurrences may overlap. A pattern listed twice is reported once for each index, and the empty pattern occurs at every $s$ from $0$ to $n$. The alphabet is general: characters are compared for equality and used as keys of small tables. Write $w$ for the shortest nonempty length, $L$ for the longest and $m$ for the total length.

## The algorithm

**The trie and its strings.** The trie of the reversed nonempty patterns has a node $v$ for each suffix $y(v)$ of a pattern; the path from the root to $v$ spells $y(v)$ backward, and the depth of $v$ is $d(v) = |y(v)|$. The list $\mathrm{out}[v]$ holds the indices $j$ with $P_j = y(v)$. The failure link $\mathrm{fail}(v)$ is the node of the longest proper prefix of $y(v)$ that is also a pattern suffix: it is the [failure link](/failure-link/) of Aho-Corasick in the trie of the reversed patterns.

**The three shift functions.** After the reading stops at node $v$, the text ends at $\mathrm{pos}$ with $y(v)$, preceded by the character $c$ that has no child, or by the start of the text.

- $\mathrm{shift1}(v)$, for patterns that contain the matched part: the smallest $\delta \ge 1$ such that $y(v)$ occurs in some pattern ending $\delta$ characters before its end, that is, $y(v)\, x$ is a pattern suffix with $|x| = \delta$; at most $w$. Such a pattern suffix is a node $v'$ whose failure chain passes through $v$, and the minimum is reached by a node with $\mathrm{fail}(v') = v$.
- $\mathrm{shift2}(v)$, for patterns that overlap the matched part on the right: the smallest $|P_j| - i$ over the patterns $P_j$ and lengths $1 \le i < |P_j|$ such that the prefix of $P_j$ of length $i$ is a suffix of $y(v)$; at most $w$. It satisfies $\mathrm{shift2}(v) = \min(\mathrm{shift2}(\mathrm{parent}(v)), g(v))$ with $\mathrm{shift2}(\mathrm{root}) = w$, where $g(v)$ is the smallest $d(v') - d(v)$ over the pattern nodes $v'$ whose failure chain passes through $v$.
- $\mathrm{char}(c)$, for the mismatched character: $1 + e$ for the smallest distance $e$ from the end of a pattern at which $c$ occurs, that is, the smallest depth of a trie node entered by $c$; and $w + 1$ if this is larger, or if $c$ occurs in no pattern.

The shift is

$$\mathrm{shift}(v, c) = \min\Big(\max\big(\mathrm{shift1}(v),\ \mathrm{char}(c) - d(v) - 1\big),\ \mathrm{shift2}(v)\Big).$$

```pseudo id=main
COMMENTZ-WALTER(T[0 .. n-1], P_0, ..., P_{k-1})
L1  output (s, j) for every s in 0 .. n and every j with P_j = ε
L2  if no pattern is nonempty then return
L3  build the trie of the reversed nonempty patterns with d, out, parent and fail
L4  w ← the shortest nonempty length; char[c] ← min({w + 1} ∪ {d(u) : u is entered by c})
L5  shift1[v] ← min({w} ∪ {d(u) − d(v) : fail(u) = v})
L6  shift2[root] ← w; shift2[v] ← min(shift2[parent(v)], g(v)) in breadth-first order
L7  pos ← w − 1
L8  while pos ≤ n − 1 do
L9      v ← root; i ← pos
L10     while i ≥ 0 and v has a child for T[i] do
L11         v ← that child; i ← i − 1
L12         output (i + 1, j) for every j in out[v]
L13     c ← T[i] if i ≥ 0, else a character that occurs in no pattern
L14     pos ← pos + min(max(shift1[v], char[c] − d(v) − 1), shift2[v])
```

The values $g(v)$ come from one pass over the nodes in decreasing depth: each node $u$ passes to $\mathrm{fail}(u)$ the value $d(u) - d(\mathrm{fail}(u))$ if $u$ is a pattern node, and $g(u) + d(u) - d(\mathrm{fail}(u))$ otherwise, and each node keeps the minimum it receives. The window is $T[\mathrm{pos} - w + 1 \ldots \mathrm{pos}]$, but the reading of lines L10 to L12 continues to the left of it while the trie allows, so that longer patterns are found.

## Example

Take the patterns $P_0 = $ caacb, $P_1 = $ cbaa, $P_2 = $ accb, and the text ccdaaacaacbaaddbcd ($n = 18$). Then $w = 4$, and $\mathrm{char}(\mathrm{a}) = 1$, $\mathrm{char}(\mathrm{b}) = 1$, $\mathrm{char}(\mathrm{c}) = 2$, and $\mathrm{char}(c) = 5$ for d and all other characters. The trie has 12 nodes; each is named by its string $y(v)$, a pattern suffix.

| $y(v)$ | root | b | cb | acb | aacb | caacb | a | aa | baa | cbaa | ccb | accb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| shift1 | 1 | 2 | 2 | 4 | 4 | 4 | 1 | 2 | 4 | 4 | 4 | 4 |
| shift2 | 4 | 4 | 2 | 2 | 2 | 2 | 3 | 3 | 3 | 3 | 2 | 2 |

For example, $\mathrm{shift1}(\mathrm{b}) = 2$ because b occurs in cbaa two characters before the end, and $\mathrm{shift2}(\mathrm{cb}) = 2$ because the prefix cb of cbaa is a suffix of cb, which gives $|\mathrm{cbaa}| - 2 = 2$.

| pos | read, as matched | stopped by | output | shift1 | char − d − 1 | shift2 | shift |
|---|---|---|---|---|---|---|---|
| 3 | a | d | | 1 | 5 − 1 − 1 = 3 | 3 | 3 |
| 6 | none | c | | 1 | 2 − 0 − 1 = 1 | 4 | 1 |
| 7 | a | c | | 1 | 2 − 1 − 1 = 0 | 3 | 1 |
| 8 | aa | c | | 2 | 2 − 2 − 1 = −1 | 3 | 2 |
| 10 | caacb | a | (6, 0) | 4 | 1 − 5 − 1 = −5 | 2 | 2 |
| 12 | cbaa | a | (9, 1) | 4 | 1 − 4 − 1 = −4 | 3 | 3 |
| 15 | b | d | | 2 | 5 − 1 − 1 = 3 | 4 | 3 |

The output is (6, 0) and (9, 1): caacb at 6 and cbaa at 9, which overlap. At pos 3 the character d occurs in no pattern, so the window jumps past it. At pos 8 the matched part aa occurs in cbaa two places before its end, and shift1 decides. At pos 10 shift2 limits the move to 2, because the prefix cb of cbaa is a suffix of the match caacb; that is the next occurrence. The search uses 7 windows and reads 21 characters for $n = 18$; a left-to-right method reads all 18 and visits 15 window ends.

## Correctness

The reading at $\mathrm{pos}$ reports exactly the patterns that end at $\mathrm{pos}$, because it follows the text backward through the trie until the text leaves it, and passes through the node of every reversed pattern on the way. The shift skips no end position. Let a pattern $P$ end at $\mathrm{pos} + \delta$, $\delta \ge 1$, and let the reading stop at $v$ with the character $c$ at $i = \mathrm{pos} - d(v)$.

- If the occurrence covers $i$, it contains $y(v)$ ending $\delta$ before its end, so $\delta \ge \mathrm{shift1}(v)$ (or $\delta \ge w$); and it has $c$ at distance $\delta + d(v)$ from its end, so $\delta \ge \mathrm{char}(c) - d(v) - 1$.
- If it starts inside $y(v)$, a prefix of $P$ of length $i' = |P| - \delta$ is a suffix of $y(v)$, so $\delta \ge \mathrm{shift2}(v)$.
- If it starts after $\mathrm{pos}$, then $\delta \ge |P| \ge w \ge \mathrm{shift2}(v)$.

In each case $\delta$ is at least the shift. The full proof, including the computation of the tables, is in the proof file below.

## Complexity

- **Preprocessing.** The trie, the failure links and the three tables take $O(m)$ time with hashed children, and the table char has at most $\min(\sigma, m)$ entries.
- **Worst case.** Each window reads at most $L + 1$ characters and the shift is at least 1, so the time is $O(nL + z)$. This is reached without any occurrence: with the text $a^n$ and the patterns $a^{L-1} b$ and $b a^{L-1}$, each window reads $L$ characters and shifts by 1, which gives $(n - L + 1) L$ reads (388, 744 and 1360 reads for $n = 100$ and $L = 4, 8, 16$).
- **Best case.** If each window stops after one character and shifts by $w$, the time is $O(n/w + z)$.
- **Space.** $O(m)$.

**Measured averages.** On a random text of $10^5$ characters with $k$ random patterns of length 8 (the same data as on the [Set Horspool](/set-horspool/) page), the characters read per text character were:

| alphabet | $k = 1$ | $k = 10$ | $k = 100$ | $k = 1000$ |
|---|---|---|---|---|
| 4 letters, Commentz-Walter | 0.24 | 0.94 | 2.26 | 3.60 |
| 4 letters, Set Horspool | 0.29 | 1.95 | 4.20 | 5.90 |
| 26 letters, Commentz-Walter | 0.15 | 0.41 | 1.40 | 1.93 |
| 26 letters, Set Horspool | 0.15 | 0.46 | 2.14 | 2.83 |

The shift functions that use the matched part keep shifts above 1 where the single-character shift of Set Horspool falls to 1, but both read more than one character per text character for large sets, where Aho-Corasick reads exactly one.

## Properties

- **Deterministic and exact.** No hashing; the output is always the set of occurrences.
- **Not online.** Each window is read backward, up to $L$ characters before its end.
- **Shifts bounded by the shortest pattern.** No shift exceeds $w$, so one short pattern slows the search for all.
- **Safe but not always maximal.** The bad-character part uses the nearest occurrence of $c$ in any pattern, not in the patterns that agree with the matched part, so the shift can be shorter than the largest safe shift.
- **Shares the trie of Aho-Corasick.** The trie and the failure links are those of [Aho-Corasick](/aho-corasick/) on the reversed patterns.

## Variants and improvements

- **[Set Horspool](/set-horspool/).** Keeps the reversed trie and drops shift1 and shift2: the shift depends only on the last character of the window. It is simpler and nearly as fast for small sets over large alphabets.
- **[Wu-Manber](/wu-manber/).** Drops the trie and shifts on blocks of 2 or 3 characters through a [block shift table](/block-shift-table/); faster for large sets in practice.
- **Factor-based scans.** Set backward oracle matching and set BDM read the window backward in an automaton of all factors of the reversed patterns and shift past the read part, which gives shifts that do not depend on the matched part being a pattern suffix; see [backward DAWG matching](/backward-dawg-matching/) for one pattern.
- **Bounded worst case.** Like the Galil rule for [Boyer-Moore](/boyer-moore/), remembering which part of the window is known to match, or running [Aho-Corasick](/aho-corasick/) side by side, gives an $O(n + m + z)$ worst case at the cost of more bookkeeping.

## When to use it

Use Commentz-Walter for a moderate number of patterns over a large alphabet when average speed matters, the shortest pattern is not very short, and the extra preprocessing is acceptable. For a few patterns, [Set Horspool](/set-horspool/) is simpler; for thousands of patterns, [Wu-Manber](/wu-manber/) is usually faster; for a worst-case guarantee or a small alphabet with many patterns, use [Aho-Corasick](/aho-corasick/).

## Pitfalls

- **Only one of the good-suffix parts.** Using shift1 without shift2 can skip an occurrence that overlaps the matched part on the right, such as cbaa after caacb in the example: there shift1 is 4 and the next occurrence is 2 ahead.
- **Combining with max instead of min.** The bad-character value bounds only the patterns that cover the mismatched position; the result must be capped by shift2, which covers the others.
- **Bad-character value from one pattern.** The function char must take the nearest occurrence over all patterns, or a shift can skip an occurrence of another pattern.
- **Stopping the reading at the window.** Patterns longer than $w$ end at $\mathrm{pos}$ but begin before the window; the reading must go on, down to the start of the text.
- **The start of the text.** When the reading reaches $T[0]$ there is no mismatched character; treat it as a character absent from all patterns, which leaves the shift at $\mathrm{shift2}$ or less.

## Implementations

## History

Beate Commentz-Walter presented the algorithm at ICALP 1979, three years after the [Boyer-Moore](/boyer-moore/) algorithm (published in 1977) and four years after [Aho-Corasick](/aho-corasick/) (1975), and combined the two. The formulation of the shift functions on this page, with shift1, shift2 and char on the trie of reversed patterns, is the one used in later expositions. Andrew Hume's gre and version 2.0 of GNU fgrep were based on it, according to Wu and Manber (1994), whose own algorithm was faster for large sets. Navarro and Raffinot (2002) describe it with its simplification Set Horspool among the suffix-based methods.

## References
