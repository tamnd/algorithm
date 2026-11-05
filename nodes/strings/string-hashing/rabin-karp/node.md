---
tag: 1B6QTQ
kind: algorithm
slug: rabin-karp
name: Rabin-Karp algorithm
aliases:
- Karp-Rabin algorithm
- Rabin-Karp string search
area: strings/string-hashing
level: core
summary: Find pattern occurrences by comparing rolling hashes first and verifying each hash match character by character.
solves: [string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, z: the number of occurrences, p: the prime modulus}
  time: {worst: O(n·m), expected: O(n + m + z·m + n·m^2/p)}
  space: {extra: O(1)}
properties: {deterministic: false, recursive: false, online: true}
history:
  year: 1987
  people: [Richard M. Karp, Michael O. Rabin]
  note: Published in the IBM Journal of Research and Development in 1987, after a Harvard technical report of 1981.
prereqs: [polynomial-rolling-hash, polynomial-hash-collision-bound, string-matching]
see_also: [spurious-hit, karp-rabin-multiple-patterns, fingerprinting, naive-string-matching, knuth-morris-pratt, las-vegas-algorithm, monte-carlo-algorithm, anti-hash-tests]
sources:
  - paper: doi:10.1147/rd.312.0249
    title: Richard M. Karp and Michael O. Rabin, Efficient randomized pattern-matching algorithms, IBM Journal of Research and Development 31(2) (1987), 249-260
    locator: the fingerprint method for string matching, its error analysis, and the extensions to two dimensions and to other patterns
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 32.2, The Rabin-Karp algorithm (the procedure RABIN-KARP-MATCHER, spurious hits, and the expected running time)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 4.4, Karp-Rabin fingerprint methods for exact match
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 7, Algebraic techniques (the sections on fingerprinting, string equality and pattern matching)
  - url: https://ioinformatics.org/journal/INFOL119.pdf
    title: Jakub Pachocki and Jakub Radoszewski, Where to use and how not to use polynomial string hashing, Olympiads in Informatics 7 (2013), 90-100
    locator: Section 2 (the polynomial hash, its probability of error, and the modulus 2^64)
---

The Rabin-Karp algorithm solves [string matching](/string-matching/) by hashing. It computes a [polynomial rolling hash](/polynomial-rolling-hash/) of the pattern and of each window of the text with the same length, updates the window hash in $O(1)$ time as the window slides, and compares characters only where the two hashes are equal. With a prime modulus $p$ and a base drawn at random after the input is fixed, a window that is not an occurrence gives a false hash match, a [spurious hit](/spurious-hit/), with probability at most $(m-1)/p$. So the expected time is $O(n + m)$ plus $O(m)$ for each occurrence, while the worst case is $O(nm)$. Its strength is that the same idea extends to many patterns of one length, to two dimensions and to substring comparison, where character-based methods are harder.

## In plain words

To find a word in a long text, the simple method compares the word with every piece of the text of the same length, letter by letter. Rabin-Karp first turns the word into one number. It then turns each piece of the text into a number in the same way, and it compares numbers instead of letters.

The trick is that the number of the next piece comes from the number of the current piece with a few steps: take out the first letter, shift, and add the new last letter. So all the numbers of the text cost about one step per letter.

Equal pieces always give equal numbers. Different pieces can give equal numbers by bad luck, so when the numbers agree, the method checks the letters. If the numbers are computed with a random choice, bad luck is rare and the letter checks are few.

## The problem

Given a text $T = T[0 \ldots n-1]$ and a pattern $P = P[0 \ldots m-1]$ over an alphabet $\Sigma$, output every shift $s$ with $0 \le s \le n - m$ and $T[s \ldots s+m-1] = P$. Indices are 0-based. Occurrences may overlap: the pattern aa occurs at 0, 1 and 2 in aaaa. The empty pattern occurs at every $s$ from $0$ to $n$. The alphabet is integer: each character $a$ has a code $c(a) \in \{1, \ldots, p - 1\}$, and distinct characters have distinct codes. For bytes, $c(a)$ is the byte value plus 1. The algorithm needs only these codes and equality tests of characters.

## The algorithm

Fix a prime $p$ larger than every code. The hash of a string $x$ of length $\ell$ with base $r$ is $h(x) = \sum_{i=0}^{\ell-1} c(x_i)\, r^{\ell-1-i} \bmod p$, computed left to right by Horner's rule. Write $t_s = h(T[s \ldots s+m-1])$ for the hash of the window at $s$.

```pseudo id=main
RABIN-KARP(T[0 .. n-1], P[0 .. m-1])
L1  if m = 0 then output 0, 1, ..., n; return
L2  if m > n then return
L3  r ← a uniform random element of {0, 1, ..., p − 1}
L4  R ← r^(m−1) mod p
L5  hp ← 0; ht ← 0
L6  for i ← 0 to m − 1 do hp ← (hp · r + c(P[i])) mod p; ht ← (ht · r + c(T[i])) mod p
L7  for s ← 0 to n − m do
L8      if hp = ht then
L9          if T[s .. s + m − 1] = P then output s
L10     if s < n − m then
L11         ht ← ((ht − c(T[s]) · R) · r + c(T[s + m])) mod p
```

Line L6 computes $h(P)$ and $t_0$. Line L11 removes the term $c(T[s])\, r^{m-1}$ of the leaving character, multiplies by $r$ to shift the other terms up by one power, and adds the code of the entering character; this gives $t_{s+1}$. Line L9 compares up to $m$ characters, and it is reached only on a hash match. The result of line L11 is reduced to $\{0, \ldots, p-1\}$, also when the value before the reduction is negative.

**The choice of $p$ and $r$.** The bound on spurious hits holds for $p$ prime, $r$ uniform on $\{0, \ldots, p-1\}$, and a text and pattern that do not depend on $r$. A good default is the [Mersenne prime](/mersenne-prime/) $p = 2^{61} - 1$, with 128-bit products. A fixed base written in the code, or arithmetic modulo $2^{64}$, gives no bound at all against chosen inputs; see [anti-hash tests](/anti-hash-tests/).

## Example

Take $T = $ abababbb ($n = 8$), $P = $ aba ($m = 3$), the codes $c(\mathrm{a}) = 1$, $c(\mathrm{b}) = 2$, the small prime $p = 13$ and a draw $r = 5$. Then $R = 5^2 \bmod 13 = 12$ and $h(P) = (1 \cdot 25 + 2 \cdot 5 + 1) \bmod 13 = 36 \bmod 13 = 10$.

| $s$ | window | $t_s$ | L8 | L9 | value before reduction in L11 |
|---|---|---|---|---|---|
| 0 | aba | 10 | match | equal: output 0 | $(10 - 1 \cdot 12) \cdot 5 + 2 = -8$ |
| 1 | bab | 5 | | | $(5 - 2 \cdot 12) \cdot 5 + 1 = -94$ |
| 2 | aba | 10 | match | equal: output 2 | $(10 - 1 \cdot 12) \cdot 5 + 2 = -8$ |
| 3 | bab | 5 | | | $(5 - 2 \cdot 12) \cdot 5 + 2 = -93$ |
| 4 | abb | 11 | | | $(11 - 1 \cdot 12) \cdot 5 + 2 = -3$ |
| 5 | bbb | 10 | match | differ: spurious hit | |

The output is 0 and 2, two overlapping occurrences. The window bbb at $s = 5$ has the same hash as aba but is a different string, so line L9 rejects it. The reason is algebraic: $h(\mathrm{bbb}) - h(\mathrm{aba}) = (2 - 1) r^2 + (2 - 1) = r^2 + 1$, which is zero modulo 13 exactly for $r = 5$ and $r = 8$. So 2 of the 13 bases, that is $m - 1$ of them, make this window a spurious hit, which is the most the [collision bound](/polynomial-hash-collision-bound/) allows. With $p = 2^{61} - 1$ the chance would be about $10^{-18}$.

## Correctness

The algorithm outputs exactly the occurrences, whatever $r$ is; only its running time depends on $r$. The proof rests on one [loop invariant](/loop-invariant/): at line L8 in the pass for $s$, $ht = t_s$. It holds at $s = 0$ by line L6, and line L11 keeps it by the identity $(t_s - c(T[s])\, r^{m-1})\, r + c(T[s+m]) \equiv t_{s+1} \pmod p$. An occurrence at $s$ makes the window equal to $P$, so $t_s = h(P)$ and line L9 confirms it. A shift that is not an occurrence fails the hash test or the character test, so it is not output. The full proof is in the proof file below.

## Complexity

- **Preprocessing.** Line L4 takes $O(\log m)$ multiplications by [fast exponentiation](/modular-exponentiation/), and line L6 takes $O(m)$.
- **Scan.** Lines L8, L10 and L11 cost $O(1)$ for each of the $n - m + 1$ shifts: $O(n)$ in all.
- **Verification.** Line L9 costs $O(m)$ at each hash match. There are $z$ matches at occurrences and $F$ spurious hits, so it costs $O((z + F)m)$.

**Expected time.** For each shift $s$ that is not an occurrence, the window and $P$ are two fixed distinct strings of length $m$, so $\Pr[t_s = h(P)] \le (m-1)/p$. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[F] \le (n - m + 1)(m - 1)/p$, and the expected time is

$$O\!\left(n + m + zm + \frac{(n - m + 1)(m-1)\,m}{p}\right).$$

With $p \ge nm$, the last term is $O(m)$, and the expected time is $O(n + m + zm)$. With $p = 2^{61} - 1$ this holds whenever $nm \le 2^{61} - 1$, about $2.3 \times 10^{18}$.

**Worst case.** The time is $O(nm)$ for every base, because each of the $n - m + 1$ shifts verifies at most $m$ characters. The bound is reached when every window matches, as for $P = a^m$ and $T = a^n$, where $z = n - m + 1$ and every verification succeeds. It is also reached by a bad base: with $r = 1$, every window with the same multiset of characters as $P$ is a hash match.

**Space.** Besides the input, $O(1)$ words: $r$, $R$, $hp$ and $ht$.

## Properties

- **Las Vegas.** With line L9, the output is always correct and only the time is random: a [Las Vegas algorithm](/las-vegas-algorithm/).
- **Monte Carlo variant.** Without line L9, the time is $O(n + m)$ in the worst case, and the output may contain false matches. By the union bound, the probability of any false match is at most $(n - m + 1)(m-1)/p$. This is a [Monte Carlo algorithm](/monte-carlo-algorithm/).
- **Online and one pass.** The text is read once from left to right, and the output for $s$ is known when $T[s + m - 1]$ has been read. The verification looks back $m$ characters, so a streaming version must keep the last $m$ characters, or drop the verification.
- **Arithmetic, not comparisons.** The scan uses multiplications modulo $p$. On the [word RAM](/word-ram/) with $p$ below the word size, each costs $O(1)$.

## Variants and improvements

- **Many patterns of one length.** Store the hashes of $k$ patterns of length $m$ in a [hash table](/hash-table/) and look up each window hash: [Karp-Rabin with many patterns](/karp-rabin-multiple-patterns/), in $O(n + km)$ expected time plus verification.
- **Two dimensions.** Hash each column of an $m \times m$ window, then roll the hash of the row of column hashes. Karp and Rabin described this extension in their paper.
- **Random prime instead of random base.** The original paper reads a string as a binary number and takes it modulo a random prime from a large range. A nonzero difference below $2^m$ has fewer than $m$ prime factors, so few primes cause a false match. This bound counts primes, while the random-base bound counts roots of a polynomial; both need the input to be fixed first.
- **Two hashes.** With two independent bases, or two primes, a window is a spurious hit only if it collides under both, with probability at most $((m-1)/p)^2$ for one prime. This helps when a single word is too small for a large prime.
- **Rolling hashes over GF(2).** The [Rabin fingerprint](/rabin-fingerprint/) uses polynomials over the field with two elements and an irreducible modulus; it rolls with XOR and table lookups and is the usual choice in content-defined chunking.
- **Substring comparison.** The prefix hashes of [substring equality queries](/substring-equality-queries/) answer "is $T[i \ldots i+\ell-1] = T[j \ldots j+\ell-1]$?" in $O(1)$ time; Rabin-Karp is the case where one side is the pattern.

## When to use it

Use Rabin-Karp when the hash itself is the point: many patterns of the same length, two-dimensional patterns, a search for repeated substrings of a given length, or a comparison of files over a network. It is short to write and has small constants. For one pattern where the worst case matters, [Knuth-Morris-Pratt](/knuth-morris-pratt/) has $O(n + m)$ worst-case time with no arithmetic, and Boyer-Moore variants such as [Horspool](/boyer-moore-horspool/) skip text and are faster in practice on large alphabets. For a fixed set of patterns of different lengths, use [Aho-Corasick](/aho-corasick/).

## Pitfalls

- **A fixed base or modulus.** Code with the constants $r = 256$ and $p = 101$, or any constants known in advance, has no probability guarantee: an input chosen against them can make every window a hash match, which gives $\Theta(nm)$ time. Draw $r$ at run time.
- **Modulus $2^{64}$ by overflow.** It is fast, but strings built from the [Thue-Morse word](/thue-morse-word/) of length 2048 collide for every odd base, and the Monte Carlo variant then reports false matches.
- **Negative intermediate values.** In line L11 the value before the reduction is often negative, as in the example. In languages whose `%` keeps the sign, add $p$ before the reduction, or the hash is wrong and real occurrences are missed.
- **Code 0 for a character.** All windows have the same length, so a zero code does not make Rabin-Karp wrong, but it breaks the reuse of the same hashes for strings of different lengths. Codes from 1 avoid the problem.
- **Overflow of the products.** With $p$ near $2^{61}$, the products in line L11 need 128-bit arithmetic. With $p$ near $2^{31}$, reduce $c(T[s]) \cdot R$ before the subtraction so that every intermediate value fits in 64 bits.
- **The empty pattern and $m > n$.** Without lines L1 and L2, $R = r^{-1}$ is needed for $m = 0$, and the loop of line L7 runs a negative number of times for $m > n$.
- **Dropping the check silently.** The Monte Carlo variant is a different algorithm with a different contract. If it is used, the error probability $(n - m + 1)(m - 1)/p$ must be acceptable for the application.

## Implementations

## History

Richard Karp and Michael Rabin described the method in a Harvard technical report in 1981, and published it as "Efficient randomized pattern-matching algorithms" in the IBM Journal of Research and Development in 1987. Their main fingerprint was the residue of the string, read as a number, modulo a random prime; they also gave a fingerprint based on products of 2 by 2 matrices, and they covered two-dimensional patterns. Textbooks such as Cormen, Leiserson, Rivest and Stein present the version with a fixed prime and the decimal digits of a number, and the version with a random base modulo a fixed prime became the standard form in competitive programming, where Pachocki and Radoszewski (2013) described its correct use.

## References
