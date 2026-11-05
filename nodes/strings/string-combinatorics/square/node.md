---
tag: 4HX86Y
kind: definition
slug: square
name: Square
aliases:
- tandem repeat of period p
- squared word
area: strings/string-combinatorics
level: intro
summary: A nonempty word of the form uu, where u is nonempty.
prereqs: [string-period]
see_also: [square-free-word, overlap, cube, abelian-square, counting-distinct-squares, main-lorentz-algorithm, maximal-repetition, thue-theorem]
sources:
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 2, Square-free words (J. Berstel and C. Reutenauer), squares, square-free words and the binary case
  - paper: doi:10.1016/0020-0190(81)90024-7
    title: Maxime Crochemore, An optimal algorithm for computing the repetitions in a word, Information Processing Letters 12(5), 1981, 244-250
    locator: the bound O(n log n) on the number of occurrences of primitively rooted squares, attained by the Fibonacci words
  - paper: doi:10.1006/jcta.1997.2843
    title: Aviezri S. Fraenkel and Jamie Simpson, How many squares can a string contain?, Journal of Combinatorial Theory, Series A 82(1), 1998, 112-120
    locator: the main theorem (a word of length n contains at most 2n distinct squares)
  - book: isbn:9780521848992
    title: Maxime Crochemore, Christophe Hancart and Thierry Lecroq, Algorithms on Strings, Cambridge University Press, 2007
    locator: Chapter 9, Local periods (squares in a word and their detection)
---

A square is a word of the form $uu$ with $u$ nonempty, such as `aa`, `abab` or `abcabc`: a word made of two equal halves. Squares are the simplest repetitions in strings; in biology they are called tandem repeats. Every binary word of length at least 4 contains a square, while over three letters there are infinite words with no square at all, the [square-free words](/square-free-word/) of [Thue's theorem](/thue-theorem/).

## Definition

Let $\Sigma$ be an [alphabet](/alphabet/); only equality of letters is used. Indices are 0-based, and $s[i..j]$ includes both ends.

**Square.** A word $w$ is a *square* if $w = uu$ for a nonempty word $u$, its *root*; the length $|u|$ is the *period* of the square. Equivalently, $|w| = 2p$ is even and $w[0..p-1] = w[p..2p-1]$, that is, $p$ is a [period](/string-period/) of $w$ and $|w| = 2p$.

**Occurrence.** A word $s$ *contains a square* at position $i$ with period $p$ if $s[i..i+2p-1]$ is a square of period $p$, that is, $s[i+t] = s[i+p+t]$ for $0 \le t < p$. A word with no square factor is *square-free*.

**Primitively rooted square.** A square $uu$ is *primitively rooted* if $u$ is a [primitive word](/primitive-word/). Every square $uu$ equals $\rho^{2m}$, where $\rho$ is the primitive root of $u$ and $u = \rho^m$, so it starts with the primitively rooted square $\rho\rho$.

**Smallest period of a square.** If $w = uu$, then $\mathrm{per}(w)$ divides $|u|$. *Proof.* Let $p = \mathrm{per}(w) \le |u|$. Both $p$ and $|u|$ are periods, and $p + |u| \le 2|u| = |w|$, so by the [Fine and Wilf theorem](/fine-and-wilf-theorem/) $\gcd(p, |u|)$ is a period, and minimality of $p$ gives $p = \gcd(p, |u|)$, a divisor of $|u|$. $\square$

**Binary words of length 4 contain squares.** Let $w$ be a binary word of length 4 with no square. Then $w[0] \ne w[1]$, $w[1] \ne w[2]$ and $w[2] \ne w[3]$, since equal neighbours form a square of period 1. With two letters this forces $w = $ `abab` or $w = $ `baba`, both squares, a contradiction. So the only binary square-free words are $\varepsilon$, `a`, `b`, `ab`, `ba`, `aba`, `bab`.

## Examples and non-examples

- **Squares.** `aa`, `abab` $= (ab)^2$, `abaaba` $= (aba)^2$, `aaaa` $= (aa)^2$, which is also $(a)^4$; its smallest period is 1, a divisor of 2.
- **Squares inside a word.** `mississippi` contains the distinct squares `ss`, `pp`, `ississ` and `ssissi`, with 5 occurrences (`ss` occurs twice). `abaababaab` contains `aa`, `abab`, `baba`, `abaaba` and the whole word, with 6 occurrences.
- **Non-example: odd length.** `aba` is not a square; it has period 2 but length 3. It is a fractional power of exponent $3/2$.
- **Non-example: equal halves after rotation.** `abba` is not a square, because its halves `ab` and `ba` differ, though they have the same letters. It is an [abelian square](/abelian-square/).
- **Square-free words.** `abcacb` contains no square, and neither does any factor of the infinite square-free ternary words.
- **Many occurrences.** The word $a^n$ has $\sum_{p=1}^{\lfloor n/2 \rfloor} (n - 2p + 1)$ occurrences of squares, which is $\Theta(n^2)$; but only $\lfloor n/2 \rfloor$ distinct squares, and only $n - 1$ occurrences of primitively rooted squares (the occurrences of `aa`).

The largest number of distinct squares in a binary word of length $n$ is as follows.

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| max distinct squares | 0 | 1 | 1 | 2 | 2 | 3 | 3 | 4 | 5 | 6 | 7 | 7 | 8 | 9 |

## Related definitions

- **Square-free word.** A word with no square factor; infinite ones exist over three letters. See [square-free word](/square-free-word/) and [Thue's theorem](/thue-theorem/).
- **Overlap and cube.** An [overlap](/overlap/) $axaxa$ is a square followed by one more letter; a [cube](/cube/) is $uuu$.
- **Abelian square.** A word $uv$ where $v$ is a permutation of $u$; see [abelian square](/abelian-square/).
- **Counting squares.** The number of occurrences of primitively rooted squares in a word of length $n$ is $O(n \log n)$ (Crochemore), and the number of distinct squares is at most $2n$ (Fraenkel and Simpson); see [counting distinct squares](/counting-distinct-squares/).
- **Finding squares.** The [Main-Lorentz algorithm](/main-lorentz-algorithm/) finds all squares in $O(n \log n)$ time by divide and conquer, and every square lies inside a [run](/maximal-repetition/), so the runs of a word describe all its squares.

## References
