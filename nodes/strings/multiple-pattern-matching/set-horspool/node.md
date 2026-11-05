---
tag: 3G04XE
kind: algorithm
slug: set-horspool
name: Set Horspool algorithm
aliases:
- Set-Horspool
- multi-pattern Horspool
area: strings/multiple-pattern-matching
level: advanced
summary: Extends Horspool's bad-character shift to a set of patterns using a shared shift table.
solves: [multiple-string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the total length of the patterns, L: the largest pattern length, ℓ: the shortest nonempty pattern length, z: the number of occurrences}
  time: {build: O(m), worst: O(n·L + z), best: O(n/ℓ + z)}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2002
  people: [Gonzalo Navarro, Mathieu Raffinot]
  note: Navarro and Raffinot present Set Horspool in their 2002 book as the Horspool simplification of the Commentz-Walter algorithm of 1979; the shift rule is Horspool's of 1980.
prereqs: [boyer-moore-horspool, trie, multiple-string-matching]
see_also: [commentz-walter, wu-manber, aho-corasick, bad-character-rule, block-shift-table, boyer-moore, karp-rabin-multiple-patterns, backward-dawg-matching]
sources:
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 3, Multiple string matching (the suffix-based approach, with Commentz-Walter, Set Horspool and Wu-Manber, and the experimental map of the best algorithm by alphabet size and number of patterns)
  - paper: doi:10.1002/spe.4380100608
    title: R. Nigel Horspool, Practical fast searching in strings, Software, Practice and Experience 10(6) (1980), 501-506
    locator: the shift by the text character aligned with the last pattern position, for one pattern
  - paper: doi:10.1007/3-540-09510-1_10
    title: Beate Commentz-Walter, A string matching algorithm fast on the average, Automata, Languages and Programming (ICALP 1979), Lecture Notes in Computer Science 71, 118-132
    locator: the trie of the reversed patterns read right to left, and the shift functions that Set Horspool replaces by one character table
---

Set Horspool finds all occurrences of a set of patterns by reading the text backward from the end of a window, through the [trie](/trie/) of the reversed patterns, and then shifting the window by a distance read from a table indexed by the last character of the window. The window has the length $\ell$ of the shortest pattern, and the table is the [Horspool](/boyer-moore-horspool/) shift of all patterns at once: the smallest distance at which the last window character can appear in some pattern. With few patterns over a large alphabet, most shifts are close to $\ell$ and the algorithm reads only a fraction of the text. With many patterns the shifts fall to 1, and its worst case is $O(nL)$, so [Aho-Corasick](/aho-corasick/) is then the better choice.

## In plain words

Put a frame as long as the shortest pattern over the start of the text. Read the text backward from the right end of the frame, and follow a tree that holds all patterns written backward. Each time the letters read so far spell a whole pattern backward, that pattern ends at the right edge of the frame.

Then move the frame. The last letter under the frame decides how far: if that letter is far from the end in every pattern, or in no pattern at all, the frame can jump a long way, since no pattern can end in between. A small table, made once before the search, gives the jump for each letter.

## The problem

Given a text $T = T[0 \ldots n-1]$ and patterns $P_0, \ldots, P_{k-1}$, output every pair $(s, j)$ with $T[s \ldots s + |P_j| - 1] = P_j$. Indices are 0-based. Occurrences may overlap. A pattern listed twice is reported once for each index, and the empty pattern occurs at every $s$ from $0$ to $n$. The alphabet is general: characters are compared for equality and used as keys of a small table, so the shift table has one entry per character that occurs in the patterns, and all other characters share a default. Let $\ell$ be the length of the shortest nonempty pattern, $L$ the length of the longest, and $m$ the total length.

## The algorithm

The trie of the reversed nonempty patterns has a node for each suffix of a pattern; the node of a suffix $u$ is reached from the root by reading $u$ from right to left, and $\mathrm{out}[v]$ lists the indices $j$ whose whole pattern is the string of $v$. The shift table is

$$d[c] = \min\Big(\{\ell\} \cup \big\{\, \delta : 1 \le \delta \le \ell - 1,\ P_j[|P_j| - 1 - \delta] = c \text{ for some } j \,\big\}\Big).$$

So $d[c]$ is the distance from the end of a pattern to the nearest earlier copy of $c$ among the last $\ell$ characters of all patterns, and $\ell$ if there is none.

```pseudo id=main
SET-HORSPOOL(T[0 .. n-1], P_0, ..., P_{k-1})
L1  output (s, j) for every s in 0 .. n and every j with P_j = ε
L2  if no pattern is nonempty then return
L3  build the trie of the reversed nonempty patterns, with out[v]
L4  ℓ ← the shortest length of a nonempty pattern
L5  d[c] ← ℓ for every character c
L6  for each nonempty P_j and i ← |P_j| − ℓ to |P_j| − 2 do d[P_j[i]] ← min(d[P_j[i]], |P_j| − 1 − i)
L7  pos ← ℓ − 1
L8  while pos ≤ n − 1 do
L9      v ← root; i ← pos
L10     while i ≥ 0 and v has a child for T[i] do
L11         v ← that child; i ← i − 1
L12         output (i + 1, j) for every j in out[v]
L13     pos ← pos + d[T[pos]]
```

The window is $T[\mathrm{pos} - \ell + 1 \ldots \mathrm{pos}]$, but the backward reading of lines L10 to L12 is not limited to it: it goes on to the left while the trie allows, so that patterns longer than $\ell$ are found. At line L12 the string read is $T[i+1 \ldots \mathrm{pos}]$, so a pattern of the node ends at $\mathrm{pos}$ and starts at $i + 1$. Line L13 is the shift; it depends only on the character $T[\mathrm{pos}]$, not on what the reading found. In code, $d$ is a dictionary with the default $\ell$, so line L5 costs nothing.

## Example

Take the patterns $P_0 = $ aab, $P_1 = $ abaa, $P_2 = $ bab and the text cabaabcbabaab ($n = 13$). The shortest length is $\ell = 3$. Line L6 looks at the last three characters of each pattern, without the last one: aa from aab, aa from abaa, and ba from bab. The character a is at distance 1 from the end (in aab and abaa) and b at distance 2 (in bab), so $d[\mathrm{a}] = 1$, $d[\mathrm{b}] = 2$, and $d[c] = 3$ for c and every other character.

| pos | window | read, right to left | stopped by | output | $T[\mathrm{pos}]$ | shift |
|---|---|---|---|---|---|---|
| 2 | cab | ba | c | | b | 2 |
| 4 | baa | aaba | c | (1, 1) | a | 1 |
| 5 | aab | baa | b | (3, 0) | b | 2 |
| 7 | bcb | b | c | | b | 2 |
| 9 | bab | bab | c | (7, 2) | b | 2 |
| 11 | baa | aaba | b | (8, 1) | a | 1 |
| 12 | aab | baa | b | (10, 0) | b | 2 |

At pos 4 the reading goes past the left end of the window baa and finds abaa at 1. At pos 12 the next position would be 14, past the text, and the search ends. The output is (1, 1), (3, 0), (7, 2), (8, 1) and (10, 0); the occurrences of abaa at 1 and aab at 3 overlap. The algorithm visits 7 windows and reads 27 characters, against $n = 13$ windows for a left-to-right method; with only the patterns aab and bab, the reading would be shorter, since the long pattern abaa keeps the reading going.

## Correctness

Two facts give the result. First, the reading at $\mathrm{pos}$ reports exactly the patterns that end at $\mathrm{pos}$: a pattern ends at $\mathrm{pos}$ if and only if its reverse is a prefix of $T[\mathrm{pos}], T[\mathrm{pos} - 1], \ldots, T[0]$, and the trie walk follows that sequence until it leaves the trie, passing through the node of every reversed pattern that is such a prefix. Second, the shift skips no end position: if some $P_j$ ended at $\mathrm{pos} + \delta$ with $1 \le \delta < d[T[\mathrm{pos}]]$, then $\delta < \ell \le |P_j|$, so the occurrence covers $\mathrm{pos}$ at the index $|P_j| - 1 - \delta \ge |P_j| - \ell$, and $T[\mathrm{pos}] = P_j[|P_j| - 1 - \delta]$ gives $d[T[\mathrm{pos}]] \le \delta$ by line L6, a contradiction. No pattern ends before $\ell - 1$, the first window. The full proof is in the proof file below.

## Complexity

- **Preprocessing.** The trie takes $O(m)$ time with hashed children, and the shift table $O(k \ell) = O(m)$.
- **Worst case.** Each window reads at most $L + 1$ characters, and there are at most $n$ windows, so the time is $O(nL + z)$. This is reached: with the text $a^n$ and the pattern $b a^{L-1}$, every window reads $L$ characters and shifts by 1, which gives $(n - L + 1) L$ reads.
- **Best case.** If every window stops after one character and shifts by $\ell$, the time is $O(n/\ell + z)$, which is sublinear in $n$.
- **Space.** $O(m)$ for the trie and at most $\min(\sigma, m)$ table entries.

**Measured averages.** On a random text of $10^5$ characters with $k$ random patterns of length 8, the number of characters read per text character and the mean shift were as follows.

| alphabet | $k = 1$ | $k = 10$ | $k = 100$ | $k = 1000$ |
|---|---|---|---|---|
| 4 letters: reads per character | 0.29 | 1.95 | 4.20 | 5.90 |
| 4 letters: mean shift | 4.79 | 1.25 | 1.00 | 1.00 |
| 26 letters: reads per character | 0.15 | 0.46 | 2.14 | 2.83 |
| 26 letters: mean shift | 6.93 | 3.01 | 1.00 | 1.00 |

With more patterns, almost every character occurs at distance 1 from the end of some pattern, so the shift drops to 1, and the backward reading also gets longer because more paths of the trie match. This is the reason Navarro and Raffinot recommend Set Horspool only for small sets over large alphabets.

## Properties

- **Deterministic and exact.** No hashing and no probability: the output is always the set of occurrences.
- **Not online.** The window must be complete before it is read backward, and the reading looks back up to $L$ characters before the window.
- **Shift from one character.** The shift ignores what the backward reading matched; this is what makes it simple, and also what makes it weaker than Commentz-Walter, whose shifts use the matched suffix.
- **Bounded by the shortest pattern.** No shift exceeds $\ell$, so one short pattern slows down the search for all others.

## Variants and improvements

- **[Commentz-Walter](/commentz-walter/).** Combines the reversed trie with shifts computed from the matched suffix and the mismatched character, the analogues of the good-suffix and bad-character rules of [Boyer-Moore](/boyer-moore/). The shifts are longer, the tables more complex.
- **[Wu-Manber](/wu-manber/).** Replaces the single character by a block of $B$ characters and the trie by a hash table of pattern prefixes. Blocks are much less likely to occur near the end of a pattern than single characters, so shifts stay long for thousands of patterns.
- **Set Backward Oracle Matching and set BDM.** Read the window backward in an automaton that recognizes all factors of the reversed patterns, such as a factor oracle or a [suffix automaton](/suffix-automaton/), and shift past the left end of the read part; see [backward DAWG matching](/backward-dawg-matching/) for one pattern. Navarro and Raffinot find these best for large sets of long patterns.
- **Several characters for the shift.** Using the last two characters of the window, as in the Wu-Manber [block shift table](/block-shift-table/), lengthens shifts for large sets.

## When to use it

Use Set Horspool for a handful of patterns over a large alphabet, such as words in natural-language text, when the shortest pattern is not too short. It is a short program and reads only part of the text. For many patterns, short patterns or small alphabets such as DNA, use [Aho-Corasick](/aho-corasick/), which reads each character once, or [Wu-Manber](/wu-manber/), whose block shifts stay long. For a worst-case guarantee, use Aho-Corasick.

## Pitfalls

- **Stopping the reading at the window.** Patterns longer than $\ell$ end at $\mathrm{pos}$ but start before the window; the backward reading must continue past the window edge, down to the start of the text.
- **Shifts from whole patterns.** Computing the shift over all characters of every pattern, instead of the last $\ell$, is still safe but gives shorter shifts. Computing it over the first $\ell$ characters is wrong: it can skip occurrences of longer patterns.
- **Including the last character.** The distance 0 must not be used: $d[c]$ ranges over $1 \le \delta \le \ell - 1$, or the window never moves.
- **Empty and very short patterns.** An empty pattern gives $\ell = 0$ and no progress; treat it apart, as line L1 does. A pattern of length 1 forces all shifts to 1.
- **Reading before the text.** The loop of line L10 must test $i \ge 0$ before it reads $T[i]$.

## Implementations

## History

Horspool (1980) simplified the [Boyer-Moore](/boyer-moore/) algorithm by shifting on the text character under the last pattern position only. Commentz-Walter (1979) had already combined Boyer-Moore shifts with a trie of the reversed patterns for a set of patterns. Navarro and Raffinot, in their 2002 book, describe the algorithm that uses the reversed trie with Horspool's shift and call it Set Horspool; their experiments place it as the best choice for small sets over large alphabets and show that it degrades quickly as the set grows.

## References
