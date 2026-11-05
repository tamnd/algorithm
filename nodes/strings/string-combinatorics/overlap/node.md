---
tag: C2W9F2
kind: definition
slug: overlap
name: Overlap
aliases:
- overlapping word
area: strings/string-combinatorics
level: intro
summary: A word of the form axaxa, where a is a letter and x is a word.
prereqs: [string-period]
see_also: [overlap-free-word, thue-morse-word, square, cube, square-free-word, repetition-threshold, avoidability, maximal-repetition]
sources:
  - book: isbn:9780521823326
    title: Jean-Paul Allouche and Jeffrey Shallit, Automatic Sequences, Cambridge University Press, 2003
    locator: Chapter 1, Stringology (overlaps, overlap-free words, and the overlap-freeness of the Thue-Morse sequence)
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 2, Square-free words (J. Berstel and C. Reutenauer), overlap-free words and the Thue-Morse word
  - book: isbn:9780521865722
    title: Jeffrey Shallit, A Second Course in Formal Languages and Automata Theory, Cambridge University Press, 2009
    locator: Chapter 2, Combinatorics on words (squares, overlaps and the Thue-Morse word)
  - paper: "Axel Thue, Über die gegenseitige Lage gleicher Teile gewisser Zeichenreihen, Norske Vid. Selsk. Skr. I. Mat.-Nat. Kl. Christiania 1, 1912, 1-67; English translation in J. Berstel, Axel Thue's papers on repetitions in words: a translation, Publications du LaCIM 20, Université du Québec à Montréal, 1995"
    locator: the construction of an infinite binary word with no overlap (the Thue-Morse word)
---

An overlap is a word of the form $axaxa$, where $a$ is a letter and $x$ is a word, possibly empty: a [square](/square/) $axax$ followed by one more letter that repeats its start. Overlaps are the shortest repetitions of exponent more than 2, and a word contains one exactly when two occurrences of some factor share a position, which explains the name. Binary words cannot avoid squares beyond length 3, but the [Thue-Morse word](/thue-morse-word/) is an infinite binary word without overlaps, so overlaps are the natural repetitions to avoid over two letters.

## Definition

Let $\Sigma$ be an [alphabet](/alphabet/); only equality of letters is used. Indices are 0-based, and $s[i..j]$ includes both ends.

**Overlap.** A word $w$ is an *overlap* if $w = axaxa$ for a letter $a \in \Sigma$ and a word $x \in \Sigma^*$. Its length is $2p + 1$ with $p = |ax| \ge 1$, and $p$ is a [period](/string-period/) of $w$, so its exponent is $(2p+1)/p > 2$. The shortest overlaps are the words $aaa$.

**Containing an overlap.** A word *contains an overlap* if some factor of it is an overlap, and it is *overlap-free* otherwise; see [overlap-free word](/overlap-free-word/).

**Three equivalent conditions.** For a word $s$, the following are equivalent.

1. $s$ contains an overlap as a factor.
2. $s$ has a factor of exponent more than 2, that is, a factor $f$ with $|f| > 2\,\mathrm{per}(f)$.
3. Some nonempty word $u$ has two occurrences in $s$ at positions $i < j$ with $j < i + |u|$, so that the two occurrences share a position.

*Proof.* (1) implies (2): an overlap $axaxa$ has period $p = |ax|$ and length $2p + 1 > 2p$, so its smallest period is at most $p$ and its exponent is more than 2. (2) implies (3): let $f = s[i..i+m-1]$ have period $p$ with $m > 2p$. Take $u = s[i..i+m-p-1]$, of length $m - p > p$. The period gives $s[i+t] = s[i+p+t]$ for $0 \le t < m - p$, so $u$ also occurs at $j = i + p$, and $j < i + |u|$ since $p < m - p$. (3) implies (1): let $p = j - i$, so $1 \le p < |u|$. For $0 \le t < |u|$ we have $s[i + t] = s[j + t] = s[i + p + t]$, so the factor $g = s[i..i+p+|u|-1]$ has period $p$, and its length is $p + |u| \ge 2p + 1$. Its prefix of length $2p+1$ is $y\,y\,a$ with $y = g[0..p-1]$ and $a = g[0]$; writing $y = ax$ gives $axaxa$. $\square$

## Examples and non-examples

- **Overlaps in English.** `alfalfa` $= a\,x\,a\,x\,a$ with $a = $ `a`, $x = $ `lf`; `entente` with $a = $ `e`, $x = $ `nt`. The word `banana` is not an overlap, but it contains the overlap `anana` (two occurrences of `ana` at positions 1 and 3 share the letter at position 3).
- **Short overlaps.** `aaa` (with $x$ empty), `ababa`, `abaabaa`.
- **Squares that are not overlaps.** `abab` and `aa` are squares of exponent exactly 2, and neither contains an overlap. Every overlap contains a square, the prefix $axax$, but not conversely.
- **Not an overlap: exponent less than 2.** `aabaa` has smallest period 3 and exponent $5/3$; it contains no overlap.

The numbers of words of length $n$ with no overlap are as follows.

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| binary, overlap-free | 1 | 2 | 4 | 6 | 10 | 14 | 20 | 24 | 30 | 36 | 44 | 48 | 60 |
| ternary, overlap-free | 1 | 3 | 9 | 24 | 66 | 174 | 462 | 1206 | 3162 | | | | |

The binary count grows only polynomially in $n$, while the ternary count grows exponentially, because ternary [square-free words](/square-free-word/) are overlap-free.

## Related definitions

- **Square.** A word $uu$ with $u$ nonempty; an overlap is a square followed by the first letter of its root. See [square](/square/).
- **Cube.** A word $uuu$; every cube contains an overlap $uua$ with $a$ the first letter of $u$. See [cube](/cube/).
- **Overlap-free word.** A word with no overlap factor; the [Thue-Morse word](/thue-morse-word/) is the standard infinite example. See [overlap-free word](/overlap-free-word/).
- **Exponent and repetition threshold.** An overlap is a $(2 + \varepsilon)$-power. The [repetition threshold](/repetition-threshold/) on two letters is 2, attained by the Thue-Morse word: binary words can avoid every exponent above 2 but not the squares.
- **Overlapping occurrences.** Condition 3 is the reason that the occurrences of a pattern in a text can overlap only when the pattern has a period shorter than itself, a fact used in [string matching](/string-matching/).
- **Runs.** A [maximal repetition](/maximal-repetition/) of exponent more than 2 contains an overlap.

## References
