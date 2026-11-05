---
tag: KNJ5V3
kind: definition
slug: cube
name: Cube
aliases:
- cubic word
area: strings/string-combinatorics
level: intro
summary: A nonempty word of the form uuu.
prereqs: [square]
see_also: [square, overlap-free-word, thue-morse-word, square-free-word, maximal-repetition, repetition-threshold, abelian-square, dejean-theorem]
sources:
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 2, Square-free words and idempotent semigroups (J. Berstel and C. Reutenauer), the Thue-Morse word and the avoidance of cubes and overlaps
  - book: isbn:9780821844809
    title: Jean Berstel, Aaron Lauve, Christophe Reutenauer and Franco V. Saliola, Combinatorics on Words, Christoffel Words and Repetitions in Words, CRM Monograph Series 27, American Mathematical Society, 2008
    locator: Part II, Repetitions in words (the Thue-Morse word, overlap-free and cube-free words)
  - book: isbn:9780521823326
    title: Jean-Paul Allouche and Jeffrey Shallit, Automatic Sequences, Cambridge University Press, 2003
    locator: Chapter 1, Stringology (powers, overlaps and the Thue-Morse word)
  - paper: "Franz-Josef Brandenburg, Uniformly growing k-th power-free homomorphisms, Theoretical Computer Science 23(1), 1983, 69-82"
    title: Franz-Josef Brandenburg, Uniformly growing k-th power-free homomorphisms
    locator: the exponential growth of the number of binary cube-free words
  - paper: "F. Michel Dekking, Strongly non-repetitive sequences and progression-free sets, Journal of Combinatorial Theory, Series A 27(2), 1979, 181-185"
    title: F. Michel Dekking, Strongly non-repetitive sequences and progression-free sets
    locator: the infinite ternary word without Abelian cubes and the binary word without Abelian fourth powers
---

A cube is a word of the form $uuu$ with $u$ nonempty, such as `aaa` or `abcabcabc`. Cubes are the third powers of the hierarchy of repetitions that starts with the [square](/square/) $uu$. Over two letters, squares cannot be avoided in long words, but cubes can: the [Thue-Morse word](/thue-morse-word/) is an infinite binary word with no cube, and even with no [overlap](/overlap-free-word/). A word with no factor that is a cube is cube-free.

## Definition

Let $\Sigma$ be an [alphabet](/alphabet/); only equality of letters is used. Indices are 0-based.

**Cube.** A word $w \in \Sigma^+$ is a cube if $w = uuu$ for some $u \in \Sigma^+$. Then $|w| = 3|u|$ and $w$ has the [period](/string-period/) $|u|$. Equivalently, $w$ is a cube when $|w|$ is a multiple of 3 and $|w|/3$ is a period of $w$. The word $u$ is a root of the cube. A cube is primitively rooted if $u$ is a [primitive word](/primitive-word/); each cube $z^{3k}$ with $z$ primitive contains the primitively rooted cube $zzz$ as a prefix.

**Cube factor and cube-free word.** A word $w$ contains a cube if some factor $w[i..i+3p-1]$ with $p \ge 1$ is a cube, that is, $w[j] = w[j+p]$ for $i \le j < i + 2p$. A finite or infinite word is cube-free if it contains no cube.

**Fractional powers.** For a word $x$ with smallest period $p$, the exponent of $x$ is $|x|/p$. A cube has exponent at least 3. An overlap is a word $a\,v\,a\,v\,a$ with $a$ a letter, of exponent $2 + 1/(|v| + 1)$. Each cube $uuu$ with $u = av$ contains the overlap $avava$ as a prefix, so an overlap-free word is cube-free. The [repetition threshold](/repetition-threshold/) asks for the least exponent that can be avoided on $\sigma$ letters.

### Basic facts

1. **One letter.** Over $\{a\}$, the only cube-free words are $\varepsilon$, $a$ and $aa$.
2. **Two letters.** There are infinite binary cube-free words. The Thue-Morse word $t = $ `abbabaabbaababba` $\cdots$, the fixed point of $a \mapsto ab$, $b \mapsto ba$, is overlap-free (Thue, 1912), so it is cube-free. It contains squares, such as `abab` and `aa`, which is unavoidable on two letters: each binary word of length 4 contains a square.
3. **Growth.** The number $c(n)$ of binary cube-free words of length $n$, for $n = 0$ to $20$, is 1, 2, 4, 6, 10, 16, 24, 36, 56, 80, 118, 174, 254, 378, 554, 802, 1168, 1716, 2502, 3650, 5324. Brandenburg proved that it grows exponentially in $n$.
4. **Distinct cubes.** The map $uuu \mapsto uu$ is injective on words, so a word has at most as many distinct cube factors as distinct [square](/square/) factors, see [counting distinct squares](/counting-distinct-squares/).
5. **Cubes and runs.** Each occurrence of a primitively rooted cube $zzz$ lies inside a unique [run](/maximal-repetition/) of period $|z|$, and that run has exponent at least 3.

## Examples and non-examples

**Cubes.**

- `aaa` $= a^3$, root `a`.
- `ababab` $= ($`ab`$)^3$, root `ab`, period 2, length 6.
- `abaabaaba` $= ($`aba`$)^3$.
- `aaaaaa` $= ($`aa`$)^3$ is a cube whose root is not primitive. It also has the primitively rooted cube `aaa` as a factor.

**Non-examples.**

- `aabaabaa` has the smallest period 3 and length 8, so its exponent is $8/3 < 3$. It is not a cube and contains no cube, but its prefix `aabaaba`, of length 7 and period 3, is an overlap.
- `abababa` has the period 2 and length 7, so its exponent is $7/2$. It is not a cube, but it contains the cube `ababab`.
- `abab` and `aa` are squares, not cubes. The word `aabaa` has no cube.
- The prefix of length 256 of the Thue-Morse word contains no cube and no overlap.

## Related definitions

- **[Square](/square/).** A word $uu$; the cube is the next integer power.
- **[Overlap-free word](/overlap-free-word/).** A word with no factor $avava$. Overlap-free implies cube-free, and the Thue-Morse word is the standard binary example.
- **[Square-free word](/square-free-word/).** A word with no square factor. Over three letters there are infinite square-free words, by the [Thue theorem](/thue-theorem/).
- **[Maximal repetition (run)](/maximal-repetition/).** A maximal periodic factor of exponent at least 2; the runs of exponent at least 3 hold all the cubes of a word.
- **[Repetition threshold](/repetition-threshold/) and [Dejean's theorem](/dejean-theorem/).** The least avoidable exponent on each alphabet size; for two letters it is 2, so cubes, of exponent 3, are avoidable.
- **[Abelian square](/abelian-square/).** The Abelian analogue: $uv$ with $v$ a permutation of $u$. Abelian cubes $uvw$ with three permutations of each other are avoidable on three letters (Dekking, 1979).

## References
