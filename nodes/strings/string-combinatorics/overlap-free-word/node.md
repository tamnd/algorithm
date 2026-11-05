---
tag: 8H8PRX
kind: definition
slug: overlap-free-word
name: Overlap-free word
aliases:
- overlap-free
area: strings/string-combinatorics
level: core
summary: A word containing no factor of the form axaxa.
prereqs: [overlap]
see_also: [thue-morse-word, square-free-word, cube, repetition-threshold, string-morphism, thue-theorem, avoidability, square]
sources:
  - book: isbn:9780521823326
    title: Jean-Paul Allouche and Jeffrey Shallit, Automatic Sequences, Cambridge University Press, 2003
    locator: Chapter 1, Stringology (overlap-free words, the Thue-Morse sequence, and the structure of binary overlap-free words)
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 2, Square-free words (J. Berstel and C. Reutenauer), overlap-free words and the Thue-Morse morphism
  - paper: "Antonio Restivo and Sergio Salemi, Overlap free words on two symbols, in Automata on Infinite Words, Lecture Notes in Computer Science 192, Springer, 1985, 198-206"
    locator: the factorization of binary overlap-free words through the Thue-Morse morphism and the polynomial bound on their number
  - paper: "Axel Thue, Über die gegenseitige Lage gleicher Teile gewisser Zeichenreihen, Norske Vid. Selsk. Skr. I. Mat.-Nat. Kl. Christiania 1, 1912, 1-67; English translation in J. Berstel, Axel Thue's papers on repetitions in words: a translation, Publications du LaCIM 20, Université du Québec à Montréal, 1995"
    locator: the infinite binary word without overlaps
---

An overlap-free word is a word with no factor of the form $axaxa$, where $a$ is a letter and $x$ is a word: no [overlap](/overlap/). Equivalently, no factor has exponent more than 2, and no two occurrences of the same factor share a position. On two letters squares cannot be avoided but overlaps can: the [Thue-Morse word](/thue-morse-word/) is an infinite binary overlap-free word, and the binary overlap-free words of length $n$ are few, their number growing only polynomially in $n$.

## Definition

Let $\Sigma$ be an [alphabet](/alphabet/); only equality of letters is used. Indices are 0-based, and $s[i..j]$ includes both ends.

**Overlap-free word.** A finite or infinite word $w$ over $\Sigma$ is *overlap-free* if no factor of $w$ is an overlap $axaxa$ with $a \in \Sigma$ and $x \in \Sigma^*$.

**Equivalent forms.** By the three equivalent conditions on the [overlap](/overlap/) page, $w$ is overlap-free if and only if

1. every factor $f$ of $w$ satisfies $|f| \le 2\,\mathrm{per}(f)$, that is, has exponent at most 2 (the word is *$2^+$-power-free*); and if and only if
2. no nonempty word has two occurrences in $w$ at positions $i < j < i + |u|$.

**Closure.** Factors, reversals and images under a renaming of letters of overlap-free words are overlap-free. For binary words, the Thue-Morse morphism $\mu(0) = 01$, $\mu(1) = 10$ maps overlap-free words to overlap-free words, and $\mu(w)$ is overlap-free only if $w$ is; the proof is on the [Thue-Morse word](/thue-morse-word/) page.

**Structure of binary overlap-free words.** Restivo and Salemi (1985) showed that every binary overlap-free word $w$ can be written $w = x\,\mu(y)\,z$ where $y$ is overlap-free and $x$ and $z$ have length at most 2. Applying this again to $y$ peels off one layer of $\mu$ per step, which leads to a description of all binary overlap-free words by $O(\log n)$ choices of short prefixes and suffixes, and to their result that the number of binary overlap-free words of length $n$ is bounded by a polynomial in $n$.

## Examples and non-examples

- **Overlap-free.** `0110100110010110` (a prefix of the Thue-Morse word), `001001` (a square, but of exponent exactly 2), `aabaab`, `abcacb`, and every [square-free word](/square-free-word/).
- **Not overlap-free.** `000` ($a = 0$, $x$ empty), `01010`, `0010010` (period 3, length 7), `alfalfa`, `banana` (it contains `anana`).
- **The infinite case.** The Thue-Morse word $0110100110010110\cdots$ and its complement are overlap-free. A word that is ultimately periodic is never overlap-free, because it contains a cube $uuu$, and $uua$ with $a$ the first letter of $u$ is an overlap.

The numbers of binary overlap-free words of length $n$ are as follows.

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| count | 1 | 2 | 4 | 6 | 10 | 14 | 20 | 24 | 30 | 36 | 44 | 48 | 60 | 60 | 62 | 72 |

| $n$ | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| count | 82 | 88 | 96 | 112 | 120 | 120 | 136 | 148 | 164 | 152 | 154 | 148 | 162 | 176 | 190 |

The counts are not monotone (164 words of length 24 but 152 of length 25): some overlap-free words cannot be extended by any letter on the right without creating an overlap. Over three letters the counts of lengths $0, \ldots, 8$ are $1, 3, 9, 24, 66, 174, 462, 1206, 3162$, and they grow exponentially, since already the square-free ternary words do.

## Related definitions

- **Square-free word.** No factor $uu$; a stronger condition, possible only on three or more letters. See [square-free word](/square-free-word/) and [Thue's theorem](/thue-theorem/).
- **Cube-free word.** No factor $uuu$; a weaker condition, since a cube contains an overlap. See [cube](/cube/).
- **$\alpha$-power-free words.** No factor of exponent at least $\alpha$ (or more than $\alpha$). Overlap-free means $2^+$-power-free; the least $\alpha$ that can be avoided on $k$ letters is the [repetition threshold](/repetition-threshold/), which equals 2 for $k = 2$.
- **The Thue-Morse morphism.** The [morphism](/string-morphism/) $\mu$ generates the Thue-Morse word and, by the Restivo-Salemi factorization, all binary overlap-free words up to short ends.
- **Avoidability.** Overlap-freeness avoids the pattern $xyxyx$ with $|x| = 1$; general patterns are treated by [avoidability](/avoidability/).

## References
