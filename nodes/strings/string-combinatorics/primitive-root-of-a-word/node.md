---
tag: 0VH8YS
kind: problem
slug: primitive-root-of-a-word
name: Primitive root of a word
aliases:
- primitive root computation
- root of a word
area: strings/string-combinatorics
level: core
summary: Find the shortest word u such that the input equals u raised to some power.
model: comparison-model
complexity:
  vars: {n: the length of the word}
  time: {worst: Θ(n)}
  space: {aux: Θ(n)}
prereqs: [primitive-word, periodicity-detection]
see_also: [string-compression-by-period, string-period, prefix-function, lyndon-schutzenberger-theorem, fine-and-wilf-theorem, word-conjugacy, knuth-morris-pratt, z-algorithm]
sources:
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 1, Words (D. Perrin), primitive words and the uniqueness of the primitive root
  - book: isbn:9780521848992
    title: Maxime Crochemore, Christophe Hancart and Thierry Lecroq, Algorithms on Strings, Cambridge University Press, 2007
    locator: Chapter 1, Tools (periods, borders and primitive words), and the exercises on testing primitivity with the border table
  - paper: doi:10.1137/0206024
    title: Donald E. Knuth, James H. Morris and Vaughan R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2), 1977, 323-350
    locator: the linear-time failure function, which gives the smallest period of the word
---

The primitive root of a nonempty word $s$ is the shortest word $\rho$ with $s = \rho^m$ for some integer $m \ge 1$; the integer $m$ is the exponent of $s$. The root exists and is unique, and $\rho$ is a [primitive word](/primitive-word/). It can be computed in $O(n)$ time from the smallest [period](/string-period/) $p$ of $s$: the root has length $p$ if $p$ divides $n$, and is $s$ itself otherwise.

## In plain words

Some words are a short piece written out several times, like `abcabcabc`, which is `abc` three times. The task is to find the shortest such piece and how many times it repeats. A word that is not made of repeated copies is its own piece, used once. The quick way is to find the smallest shift that makes the word line up with itself. If that shift fits a whole number of times into the length, the first stretch of that size is the piece. If it does not fit evenly, the word is not built from whole copies of anything shorter.

## Definition

**Input.** A word $s = s[0..n-1]$ with $n \ge 1$ over an [alphabet](/alphabet/) $\Sigma$. Algorithms test letters only for equality. Indices are 0-based.

**Output.** The length $d$ of the primitive root and the exponent $m = n/d$, so that $s = (s[0..d-1])^m$ and $s[0..d-1]$ is primitive. Returning $d$ is enough, since $\rho = s[0..d-1]$.

**Existence and uniqueness.** Shown on the [primitive word](/primitive-word/) page, using the [Fine and Wilf theorem](/fine-and-wilf-theorem/): each nonempty word is a power of exactly one primitive word.

**The root from the smallest period.** Let $p = \mathrm{per}(s)$. Then $d = p$ if $p$ divides $n$, and $d = n$ otherwise.

*Proof.* The root length $d$ is a period of $s$ and divides $n$. If $p \mid n$, then $s = u^{n/p}$ with $u = s[0..p-1]$, so the root of $u$, of length at most $p$, is also a root of $s$, and uniqueness gives $d \le p$; with $d \ge p$ this gives $d = p$. If $p \nmid n$, assume $d < n$. Then $d \le n/2$ and $p \le d$, so $p + d \le n$, and by Fine and Wilf $\gcd(p, d)$ is a period; minimality of $p$ gives $p \mid d$, and $d \mid n$ then gives $p \mid n$, a contradiction. So $d = n$. $\square$

**The root from the doubled word.** $d$ is the least $i \ge 1$ such that $s$ occurs in $ss$ at position $i$. This follows from the class-size fact on the [conjugacy](/word-conjugacy/) page: the occurrence at $i$ is the rotation $\mathrm{rot}_{i \bmod n}(s)$, which equals $s$ exactly when $d$ divides $i$.

## Variants

- **Primitivity test.** Decide whether $d = n$. Same cost.
- **Roots of all prefixes.** For each $i$, the root length of $s[0..i]$: from the prefix function, $d_i = i + 1 - \pi[i]$ when that number divides $i + 1$, and $d_i = i + 1$ otherwise, all in $O(n)$.
- **Roots of factors.** Queries asking for the primitive root of $s[i..j]$ after preprocessing.
- **$k$-th roots.** Decide whether $s = u^k$ for a given $k$. This holds if and only if $k$ divides the exponent $m$, by the uniqueness of the root.
- **Fractional root.** The shortest $u$ such that $s$ is a prefix of $uuu\cdots$; this is $s[0..p-1]$ with $p = \mathrm{per}(s)$, the problem of [compression by the period](/string-compression-by-period/).

## Examples

| $s$ | $n$ | $\mathrm{per}(s)$ | root $\rho$ | exponent $m$ |
| --- | --- | --- | --- | --- |
| `a` | 1 | 1 | `a` | 1 |
| `aaaaaa` | 6 | 1 | `a` | 6 |
| `abab` | 4 | 2 | `ab` | 2 |
| `abaaba` | 6 | 3 | `aba` | 2 |
| `abcabcabc` | 9 | 3 | `abc` | 3 |
| `abaab` | 5 | 3 | `abaab` | 1 |
| `abababa` | 7 | 2 | `abababa` | 1 |
| `abcabcab` | 8 | 3 | `abcabcab` | 1 |

The words `abababa` and `abcabcab` have small periods that do not divide their lengths, so they are primitive although they look repetitive. For the prefixes of `aabaabaab` the smallest periods are $1, 1, 3, 3, 3, 3, 3, 3, 3$ and the root lengths are $1, 1, 3, 4, 5, 3, 7, 8, 3$: the prefixes of lengths 6 and 9 are $(aab)^2$ and $(aab)^3$, and the others of length at least 3 are primitive.

## Known algorithms

**Try the divisors, $O(n\,\tau(n))$.** For each divisor $d$ of $n$ in increasing order, test whether $s[i] = s[i + d]$ for all $i < n - d$; the first that passes is the root length. With $\tau(n)$ the number of divisors this costs $O(n\,\tau(n))$, which is $O(n^{1 + \varepsilon})$ for every $\varepsilon > 0$.

**Prefix function, $O(n)$.** Compute $\pi$ with [Knuth-Morris-Pratt](/knuth-morris-pratt/) preprocessing, take $p = n - \pi[n-1]$, and apply the rule above:

```pseudo id=root
PRIMITIVE-ROOT-LENGTH(s)       ▷ s[0 .. n − 1], n ≥ 1
L1  π ← PREFIX-FUNCTION(s)
L2  p ← n − π[n − 1]
L3  if n mod p = 0 then return p
L4  return n
```

**Search in the doubled word, $O(n)$.** Find the first occurrence of $s$ in $ss$ at a position $i \ge 1$ with a linear-time matcher, such as the [Z-algorithm](/z-algorithm/) on $s$ followed by $s$. Then $d = i$, and an occurrence is always found at $i = n$ or before.

**History.** The uniqueness of the primitive root is a basic fact of combinatorics on words, a consequence of the theorems of Lyndon and Schützenberger (1962) and of Fine and Wilf (1965). The linear-time computation through the smallest period follows from the failure function of Knuth, Morris and Pratt (1977).

## Bounds

**Upper bound.** $O(n)$ time with equality tests, $O(n)$ extra space for the table.

**Lower bound.** At least $\lceil n/2 \rceil$ comparisons in the worst case for $n \ge 2$ and two letters. *Proof.* On $s = a^n$ the answer is $d = 1$. If some index $j$ takes part in no comparison, change $s[j]$ to $b$: the answer stays 1, but the new word has exactly one `b`, so it is not a power $u^m$ with $m \ge 2$ (each copy of $u$ would contain the same number of letters `b`), and its root has length $n \ne 1$. Each comparison involves two indices. $\square$

## Reductions

- **To the smallest period.** As in the rule above, one division after [periodicity detection](/periodicity-detection/).
- **To string matching.** One search for $s$ in $ss$.
- **Conjugacy classes.** The number of distinct rotations of $s$ is $d$, so counting the [conjugates](/word-conjugacy/) of a word is this problem.
- **Commuting words.** By the [Lyndon-Schützenberger theorem](/lyndon-schutzenberger-theorem/), $uv = vu$ if and only if $u$ and $v$ have the same primitive root (or one is empty), so testing commutation reduces to two root computations and one comparison.

## Applications

- **Canonical forms.** A periodic word is stored as its root and exponent, and the root of a [Lyndon word](/lyndon-word/) power is the word that indexes its [necklace](/necklace/).
- **Repetitions.** Runs and squares are described by primitive roots; a [square](/square/) $uu$ is primitively rooted when $u$ is its own root.
- **Equations on words.** Solutions of word equations such as $xy = yx$ or $x^i = y^j$ are described by common roots.
- **Necklace counting.** The size of a necklace class is the root length, which is the basis of the counts in the [Witt formula](/witt-formula/).

## References
