---
tag: VC32DH
kind: definition
slug: square-free-word
name: Square-free word
aliases:
- squarefree word
area: strings/string-combinatorics
level: core
summary: A word containing no square factor.
prereqs: [square]
see_also: [thue-theorem, overlap-free-word, thue-morse-word, main-lorentz-algorithm, repetition-threshold, abelian-square, string-morphism, avoidability]
sources:
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 2, Square-free words (J. Berstel and C. Reutenauer), the binary case, the ternary infinite words and square-free morphisms
  - book: isbn:9780521823326
    title: Jean-Paul Allouche and Jeffrey Shallit, Automatic Sequences, Cambridge University Press, 2003
    locator: Chapter 1, Stringology (square-free words and Thue's construction)
  - paper: "Axel Thue, Über unendliche Zeichenreihen, Norske Vid. Selsk. Skr. I. Mat.-Nat. Kl. Christiania 7, 1906, 1-22; English translation in J. Berstel, Axel Thue's papers on repetitions in words: a translation, Publications du LaCIM 20, Université du Québec à Montréal, 1995"
    locator: the infinite square-free word over three letters
  - paper: doi:10.1016/0020-0190(81)90024-7
    title: Maxime Crochemore, An optimal algorithm for computing the repetitions in a word, Information Processing Letters 12(5), 1981, 244-250
    locator: the O(n log n) computation of all repetitions, which in particular tests square-freeness
---

A square-free word is a word with no factor of the form $uu$ with $u$ nonempty, that is, no [square](/square/): no block of letters is followed at once by a copy of itself. On two letters only six nonempty words are square-free, the longest being `aba` and `bab`, but on three letters there are square-free words of every length and even infinite ones, by [Thue's theorem](/thue-theorem/). Square-free words are the starting point of the study of avoidable repetitions in combinatorics on words.

## Definition

Let $\Sigma$ be an [alphabet](/alphabet/); only equality of letters is used. Indices are 0-based, and $s[i..j]$ includes both ends.

**Square-free word.** A finite or infinite word $w$ is *square-free* if there are no index $i$ and length $p \ge 1$ with $w[i..i+p-1] = w[i+p..i+2p-1]$. Equivalently, every factor $f$ of $w$ with $|f| \ge 2$ satisfies $|f| < 2\,\mathrm{per}(f)$: all factors have exponent less than 2.

**Basic facts.**

- *Closure.* Factors, reversals and renamings of letters of square-free words are square-free.
- *Stronger than overlap-free.* An [overlap](/overlap/) $axaxa$ starts with the square $axax$, so a square-free word is [overlap-free](/overlap-free-word/). The converse fails: `aa` is overlap-free.
- *Primitive.* A nonempty square-free word is a [primitive word](/primitive-word/), because a proper power $u^m$ with $m \ge 2$ begins with $uu$.
- *Checking one new letter.* If $w$ is square-free, then $wa$ is square-free if and only if no suffix of $wa$ is a square, because every other factor of $wa$ is a factor of $w$. This is the step of the backtracking search for square-free words.

**The binary case.** Over two letters $a, b$, every word of length 4 contains a square: a square-free word has $w[0] \ne w[1] \ne w[2] \ne w[3]$, so $w = abab$ or $baba$, a contradiction. The binary square-free words are $\varepsilon$, `a`, `b`, `ab`, `ba`, `aba`, `bab`.

**The ternary case.** There is an infinite square-free word over three letters (Thue, 1906). One is $c = 2102012101202102012021012102012\cdots$, the sequence of the numbers of ones between consecutive zeros of the [Thue-Morse word](/thue-morse-word/), or the fixed point of the [morphism](/string-morphism/) $2 \mapsto 210$, $1 \mapsto 20$, $0 \mapsto 1$. The proof is on the page of [Thue's theorem](/thue-theorem/).

## Examples and non-examples

- **Square-free.** `abcacb`, `abcbacbcabcba`, `abacabcacbabcabacabcb`, and every prefix of $c$, such as `2102012101202102012`.
- **Not square-free.** `aa`, `abab`, `abcabc`, and `abcbc`, which contains `bcbc`.
- **A square-free word that cannot be extended.** `abacaba` is square-free, but `abacabaa` ends with `aa`, `abacabab` ends with `abab`, and `abacabac` is $(abac)^2$. It is the shortest ternary square-free word with no square-free extension on the right. Square-free words of every length still exist, because some branches never die.

The numbers of ternary square-free words of length $n$ are as follows.

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| count | 3 | 6 | 12 | 18 | 30 | 42 | 60 | 78 | 108 | 144 | 204 | 264 |

| $n$ | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| count | 342 | 456 | 618 | 798 | 1044 | 1392 | 1830 | 2388 | 3180 | 4146 | 5418 | 7032 |

For $n \ge 2$ each count is a multiple of 6: a square-free word of length at least 2 uses at least two letters, so no permutation of the three letters other than the identity fixes it, and the six permutations split the words into classes of six.

## Related definitions

- **Square and repetitions.** A [square](/square/) is $uu$; the [Main-Lorentz algorithm](/main-lorentz-algorithm/) and Crochemore's algorithm decide whether a word of length $n$ is square-free in $O(n \log n)$ time, and linear-time tests exist for a fixed alphabet through the [runs](/maximal-repetition/) of the word.
- **Overlap-free and $\alpha$-power-free words.** Weaker conditions; the least exponent avoidable on $k$ letters is the [repetition threshold](/repetition-threshold/), which is $7/4$ for three letters.
- **Square-free morphism.** A [morphism](/string-morphism/) that maps square-free words to square-free words; iterating one from a letter gives infinite square-free words.
- **Abelian square-free word.** No factor $uv$ with $v$ a permutation of $u$; this needs four letters. See [abelian square](/abelian-square/) and [Keränen's theorem](/keranen-theorem/).
- **Avoidable pattern.** Square-freeness avoids the pattern $xx$; see [avoidability](/avoidability/).
- **Square-free integers.** A different notion: an integer with no repeated prime factor, as in [square-free factorization](/square-free-factorization/) of polynomials.

## References
