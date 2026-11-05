---
tag: KQB4X1
kind: problem
slug: string-compression-by-period
name: Compressing a string by its smallest period
aliases:
- Compressing a string
area: strings/string-combinatorics
level: core
summary: Problem of finding the shortest string whose repetition forms the given string, derived from the prefix function in linear time.
model: comparison-model
complexity:
  vars: {n: the length of the string}
  time: {worst: Θ(n)}
  space: {aux: Θ(n)}
prereqs: [string-period, prefix-function]
see_also: [primitive-root-of-a-word, periodicity-detection, run-length-encoding, lempel-ziv-factorization, straight-line-program-grammar, grammar-based-compression, maximal-repetition, knuth-morris-pratt]
sources:
  - url: https://cp-algorithms.com/string/prefix-function.html
    title: cp-algorithms, Prefix function. Knuth-Morris-Pratt algorithm
    locator: the section Compressing a string (the shortest t with s = t + ... + t from the last value of the prefix function)
  - book: isbn:9780521848992
    title: Maxime Crochemore, Christophe Hancart and Thierry Lecroq, Algorithms on Strings, Cambridge University Press, 2007
    locator: Chapter 1, Tools (periods and borders, and the border table computed in linear time)
  - paper: doi:10.1137/0206024
    title: Donald E. Knuth, James H. Morris and Vaughan R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2), 1977, 323-350
    locator: the failure function and its relation to the periods of the pattern
---

Compressing a string by its smallest period means storing a string $s$ of length $n$ as a shorter word $t$ and a count, so that $s$ is rebuilt by writing $t$ again and again. In the strict version $s$ must be a whole number of copies, $s = t^k$, and the shortest $t$ is the [primitive root](/primitive-root-of-a-word/) of $s$; in the relaxed version the last copy may be cut short, and the shortest $t$ is the prefix of length $\mathrm{per}(s)$, the smallest [period](/string-period/). Both are read off the last value of the [prefix function](/prefix-function/) in $O(n)$ time, and the same pass gives the answer for every prefix of $s$.

## In plain words

A long string that keeps repeating the same chunk can be written down as the chunk plus a note that says how long to keep going. The task is to find the shortest chunk that works. Some strings end in the middle of a chunk, like a pattern on wallpaper cut off at the edge, and some end exactly at the end of a chunk. The answer comes from one pass over the string that records, for each spot, how far the start of the string reappears there. The last record tells how far the whole string can slide onto itself, and that slide is the chunk length.

## Definition

**Input.** A string $s = s[0..n-1]$ with $n \ge 1$ over an [alphabet](/alphabet/) $\Sigma$. Algorithms test letters only for equality. Indices are 0-based, and $s[i..j]$ includes both ends.

**Output, strict version.** The shortest word $t$ and the integer $k$ with $s = t^k$. Then $|t| = d$, the length of the primitive root, and $k = n/d$.

**Output, relaxed version.** The shortest word $t$ such that $s$ is a prefix of the infinite word $ttt\cdots$, together with $n$. Then $t = s[0..p-1]$ with $p = \mathrm{per}(s)$, because $s$ is a prefix of $t^\infty$ for $t = s[0..q-1]$ exactly when $q$ is a period of $s$.

**Both from the prefix function.** With $p = n - \pi[n-1]$: the relaxed answer has length $p$, and the strict answer has length $p$ if $p$ divides $n$ and $n$ otherwise. The first claim is the duality between periods and borders; the second is proved on the [primitive root](/primitive-root-of-a-word/) page with the [Fine and Wilf theorem](/fine-and-wilf-theorem/).

**Size.** The compressed form takes $p$ letters and one integer, against $n$ letters for $s$. The ratio $n/p$ is the exponent of $s$; compression helps when $s$ has a large exponent.

## Variants

- **Every prefix.** Compress each prefix $s[0..i]$: the relaxed length is $i + 1 - \pi[i]$, and the strict length is the same number if it divides $i + 1$ and $i + 1$ otherwise. One pass of the prefix function gives all $n$ answers.
- **Nested repetitions.** Allow expressions such as $(ab)^3 c\,(ab)^2$ or $((ab)^2 c)^3$, and minimize the length of the expression. Dynamic programming over all factors, using the period of each factor, solves this in polynomial time.
- **Repetitions anywhere.** Replace every long repetition inside $s$, not only $s$ itself, by a root and an exponent. The [runs](/maximal-repetition/) of $s$ list all maximal repetitions, and [run-length encoding](/run-length-encoding/) is the case of period 1.
- **With errors.** Find a short $t$ such that $s$ is within $k$ mismatches of a prefix of $t^\infty$, an approximate period.
- **General compression.** Dictionary methods such as [Lempel-Ziv](/lempel-ziv-factorization/) and [grammars](/straight-line-program-grammar/) capture periodic strings as a special case: a string with small period has a short Lempel-Ziv parse, since the second copy onward is one self-referencing phrase.

## Examples

| $s$ | $n$ | $\pi[n-1]$ | $p$ | relaxed form | strict form |
| --- | --- | --- | --- | --- | --- |
| `abcabcabc` | 9 | 6 | 3 | (`abc`, 9) | `abc`$^3$ |
| `abcabcab` | 8 | 5 | 3 | (`abc`, 8) | `abcabcab`$^1$ |
| `abababa` | 7 | 5 | 2 | (`ab`, 7) | `abababa`$^1$ |
| `aaaaaa` | 6 | 5 | 1 | (`a`, 6) | `a`$^6$ |
| `abaab` | 5 | 2 | 3 | (`aba`, 5) | `abaab`$^1$ |
| `abcd` | 4 | 0 | 4 | (`abcd`, 4) | `abcd`$^1$ |

For the prefixes of `abcabcabcab`, the relaxed lengths are $1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3$ and the strict lengths are $1, 2, 3, 4, 5, 3, 7, 8, 3, 10, 11$: only the prefixes of lengths 6 and 9 are whole powers of `abc`. For the prefixes of `abaababaab` the relaxed lengths are $1, 2, 2, 3, 3, 3, 5, 5, 5, 5$ and the strict lengths are $1, 2, 3, 4, 5, 3, 7, 8, 9, 5$.

## Known algorithms

**Prefix function, $O(n)$.** Compute $\pi$ as in [Knuth-Morris-Pratt](/knuth-morris-pratt/), then apply the rules above.

```pseudo id=compress
COMPRESS-BY-PERIOD(s)            ▷ s[0 .. n − 1], n ≥ 1
L1  π ← PREFIX-FUNCTION(s)
L2  p ← n − π[n − 1]
L3  relaxed ← (s[0 .. p − 1], n)
L4  if n mod p = 0 then strict ← (s[0 .. p − 1], n / p)
L5  else strict ← (s, 1)
L6  return relaxed, strict
```

**Z-array, $O(n)$.** The smallest $p \ge 1$ with $z[p] = n - p$ (or $p = n$ if there is none) is $\mathrm{per}(s)$; see [periodicity detection](/periodicity-detection/).

**Try the candidates, $O(n^2)$.** Test $p = 1, 2, \ldots$ until $s[i] = s[i+p]$ holds for all $i < n - p$. For the strict version only the divisors of $n$ need testing, in $O(n\,\tau(n))$ time.

**History.** The link between the failure function and periods goes back to Knuth, Morris and Pratt (1977); the use of the last failure value to compress a string is a standard exercise on the prefix function in programming courses and contest material.

## Bounds

**Upper bound.** $O(n)$ time with equality tests and $O(n)$ extra space.

**Lower bound.** $\lceil n/2 \rceil$ comparisons in the worst case for $n \ge 2$, by the argument of [periodicity detection](/periodicity-detection/): on $a^n$ every index must be compared, or changing it would change the answer.

## Reductions

- **To periodicity detection.** The relaxed version is the smallest period, and the strict version is one divisibility test more.
- **To the primitive root.** The strict version is the [primitive root](/primitive-root-of-a-word/) problem.
- **To runs.** A string has relaxed length $p \le n/2$ if and only if the whole string is a run of period $p$, so computing the [runs](/maximal-repetition/) of $s$ also answers the question.

## Applications

- **Periodic data.** Repeating signals, tiled textures coded as strings, and generated test data are stored as one period and a length.
- **Bioinformatics.** The unit of a tandem repeat in DNA, such as `CAG` in `CAGCAGCAGCA`, is the relaxed answer for the repeat region.
- **Contest problems.** Questions such as "the shortest string whose repetition gives $s$", or "the shortest generator of each prefix", are solved by the prefix function in one pass.
- **A building block.** The periods of factors are computed inside algorithms for [runs](/maximal-repetition/), squares and grammar compression.

## References
