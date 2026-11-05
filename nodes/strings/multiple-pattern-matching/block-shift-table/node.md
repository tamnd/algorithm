---
tag: 6VQ0DC
kind: concept
slug: block-shift-table
name: Block shift table
aliases:
- Wu-Manber SHIFT table
- q-gram shift table
area: strings/multiple-pattern-matching
level: advanced
summary: Table giving how far to shift for each q-gram block, used by Wu-Manber to skip text quickly.
prereqs: [bad-character-rule, boyer-moore-horspool, multiple-string-matching]
see_also: [wu-manber, set-horspool, commentz-walter, hash-table, karp-rabin-multiple-patterns, boyer-moore]
sources:
  - url: https://www.cs.arizona.edu/sites/default/files/TR94-17.pdf
    title: Sun Wu and Udi Manber, A fast algorithm for multi-pattern searching, Technical Report TR 94-17, Department of Computer Science, University of Arizona, May 1994
    locator: Section 2.2 (the SHIFT table, its two cases, the compressed table) and Section 3.1 (Lemma 1, the probability of each shift value for B in the order of log_c 2M)
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 3, Multiple string matching (the Wu-Manber algorithm and its shift table on blocks of characters)
  - paper: doi:10.1002/spe.4380100608
    title: R. Nigel Horspool, Practical fast searching in strings, Software, Practice and Experience 10(6) (1980), 501-506
    locator: the shift table indexed by one text character, the case B = 1 for one pattern
---

A block shift table maps each string $X$ of $B$ characters, a block, to the distance a search window may move when $X$ is the last block of the window. For a set of patterns cut to a common length $\ell$, the entry is the distance from the end of a cut pattern to the nearest earlier end of $X$ in some cut pattern, or $\ell - B + 1$ if $X$ occurs in none. It is the shift table of the [Wu-Manber](/wu-manber/) algorithm and the block version of Horspool's [bad-character](/bad-character-rule/) shift. With $B = 1$ and many patterns almost every character ends some pattern and the shifts vanish; with $B$ about $\log_\sigma(2k\ell)$ for $k$ patterns, most blocks occur in no pattern and the expected shift is at least half the maximum.

## In plain words

When a search frame moves over a text, the last few letters under the frame tell how far it can jump. If those letters appear in no pattern, no pattern can cover them, and the frame can jump almost its whole length. If they appear in a pattern, the frame may jump only so far that those letters line up with their place in the pattern.

One letter is a poor guide when there are many patterns, because every letter appears near the end of some pattern. A pair or a triple of letters is a much better guide: there are many more pairs than letters, and most of them appear in no pattern. The table stores, for each such small group of letters, the safe jump.

## The idea

**Setting.** Patterns $P_0, \ldots, P_{k-1}$ are nonempty, $\ell$ is the shortest length, and the cut patterns are $\hat P_j = P_j[0 \ldots \ell - 1]$. A window is $T[s \ldots \mathrm{pos}]$ with $\mathrm{pos} = s + \ell - 1$; a pattern is a candidate at the window when it starts at $s$. Indices are 0-based. A block is a string of $B$ characters, $1 \le B \le \ell$, and the block of the window is $X = T[\mathrm{pos} - B + 1 \ldots \mathrm{pos}]$. The alphabet is general: blocks are keys of a table, packed into integers or hashed.

**Definition.** Say $X$ *ends at* $q$ in $\hat P_j$ if $\hat P_j[q - B \ldots q - 1] = X$, for $B \le q \le \ell$. Then

$$\mathrm{SHIFT}[X] = \min\Big(\{\ell - B + 1\} \cup \{\ell - q : X \text{ ends at } q \text{ in some } \hat P_j\}\Big).$$

So $\mathrm{SHIFT}[X] = 0$ exactly when $X$ is the last block of some cut pattern, and only then must the window be checked. Building the table takes one pass over the $\ell - B + 1$ blocks of each cut pattern, $O(B k \ell)$ time.

**Safety.** If $\mathrm{SHIFT}[X] = d$, then no pattern starts at $s + \delta$ for $0 \le \delta < d$. Suppose $P_j$ starts at $s + \delta$. If $\delta \le \ell - B$, the window block lies inside the cut part of that occurrence and ends at its index $q = \ell - \delta$; so $X$ ends at $q$ in $\hat P_j$, and $d \le \ell - q = \delta$. If $\delta \ge \ell - B + 1$, then $\delta \ge d$ since no entry exceeds $\ell - B + 1$. Both contradict $\delta < d$.

**Maximality for blocks that occur.** If $X$ ends at $q$ in $\hat P_j$ with $\ell - q = \mathrm{SHIFT}[X]$, put $P_j$ at $s + \ell - q$ in some text. Then $X$ is the block of the window at $s$, and a shift longer than $\ell - q$ would skip the occurrence. So for every block that occurs in a cut pattern, the entry is the longest safe shift that depends only on $X$. For blocks that do not occur, the default $\ell - B + 1$ can be raised, as the end of the examples shows.

**Why blocks help.** Each value $v \in \{0, \ldots, \ell - B\}$ is taken by at most $k$ blocks, one per pattern, the block that ends at $q = \ell - v$. Out of $\sigma^B$ blocks, a uniformly random block therefore has $\mathrm{SHIFT} \le v - 1$ with probability at most $v k / \sigma^B$. If $\sigma^B \ge 2 k \ell$, this is at most $v / (2\ell)$, and with $D = \ell - B + 1$,

$$\mathbb{E}[\mathrm{SHIFT}] = \sum_{v=1}^{D} \Pr[\mathrm{SHIFT} \ge v] \ge \sum_{v=1}^{D} \Big(1 - \frac{v}{2\ell}\Big) = D - \frac{D(D+1)}{4\ell} \ge \frac{D}{2},$$

since $D + 1 \le \ell + 1 \le 2\ell$. The probability of a zero shift is at most $k/\sigma^B \le 1/(2\ell)$. This is the argument of Wu and Manber for $B = \lceil \log_\sigma 2k\ell \rceil$. Larger $B$ lowers the maximum shift $\ell - B + 1$, so the best $B$ is the smallest one that makes most blocks absent from the patterns.

**Compressed tables.** The table can have fewer entries than blocks: map each block to an entry by a hash function and store, in each entry, the minimum shift of the blocks mapped to it. Every stored value is at most the true entry of each of its blocks, so the shifts stay safe; collisions only make some shifts shorter. Wu and Manber use $2^{15}$ entries.

## Examples

**One table, three block sizes.** Take the patterns search, pattern, tern, text and barn, so $\ell = 4$ and the cut patterns are sear, patt, tern, text and barn, over the 26 lowercase letters. The entries that differ from the default are:

| $B$ | default | shift 0 | shift 1 | shift 2 | shift 3 |
|---|---|---|---|---|---|
| 1 | 4 | n, r, t | a, x | e | b, p, s |
| 2 | 3 | ar, rn, tt, xt | at, ea, er, ex | ba, pa, se, te | all others |
| 3 | 2 | arn, att, ear, ern, ext | bar, pat, sea, ter, tex | all others | |

For $B = 1$, the character a is at distance 1 from the end of sear and at distance 2 in patt and barn, so its shift is 1. For $B = 2$, the block ar ends sear, so its shift is 0, and every block that occurs in no cut pattern, such as fo, gets the default 3.

Over a uniformly random block, the three tables behave as follows.

| $B$ | blocks | blocks with shift 0 | probability of shift 0 | mean shift | largest shift |
|---|---|---|---|---|---|
| 1 | 26 | 3 | 0.115 | 3.12 | 4 |
| 2 | 676 | 4 | 0.0059 | 2.96 | 3 |
| 3 | 17576 | 5 | 0.00028 | 2.00 | 2 |

With only five patterns, $B = 1$ already gives long shifts, but a window needs a check in 1 case out of 9; with $B = 2$ in 1 case out of 169. With hundreds of patterns, almost every single character ends some pattern, and only $B \ge 2$ keeps the mean shift long; the [Wu-Manber](/wu-manber/) page measures this on random text.

**A search.** On the text fastsearchforpatternsinlongtext with $B = 2$, the windows end at 3, 6, 7, 8, 11, 14, 16, 17, 19, 20, 23, 26, 29 and 30: 14 windows for 31 characters, with shift 0 at the ends of sear (7), patt (16), tern (19) and text (30).

**Variations.** The default $\ell - B + 1$ assumes that a pattern may start inside the window block. It may start there only if a suffix of $X$ of length $\ell - \delta$ is a prefix of some cut pattern, for $\ell - B + 1 \le \delta \le \ell - 1$. So the longest safe shift for $X$ is

$$\min\Big(\{\ell\} \cup \{\ell - q : X \text{ ends at } q \text{ in some } \hat P_j\} \cup \{\delta \in [\ell - B + 1, \ell - 1] : X[B - \ell + \delta \ldots B - 1] \text{ is a prefix of some } \hat P_j\}\Big).$$

In the example with $B = 2$, the blocks rc, or and nl end in a character that starts no pattern, so their shift rises from 3 to 4, and the search above needs 12 windows instead of 14. The original algorithm keeps the simpler default.

## Where it is used

- **[Wu-Manber](/wu-manber/).** The table is the main engine of the algorithm: most windows are passed over with one lookup, and only zero-shift windows consult the hash and prefix tables. It was used in agrep and glimpse.
- **Horspool for one pattern.** With $k = 1$ and $B = 1$, the table agrees with the shift table of [Horspool](/boyer-moore-horspool/) except at the last pattern character, which gets 0 here. Horspool compares the window there and then shifts by the distance to the previous copy of that character, while Wu-Manber shifts by 1. [Set Horspool](/set-horspool/) uses Horspool's form for a set of patterns.
- **Small alphabets.** For DNA, single characters give useless shifts, and blocks of several bases (so-called $q$-grams) are a common remedy in Boyer-Moore-type matchers for one or many patterns.

## References
