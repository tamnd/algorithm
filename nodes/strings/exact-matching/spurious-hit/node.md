---
tag: V01JY2
kind: concept
slug: spurious-hit
name: Spurious hit
area: strings/exact-matching
level: intro
summary: A position where the Rabin-Karp hash of a text window equals the pattern hash but the strings differ, requiring an explicit check.
prereqs: [rabin-karp, polynomial-rolling-hash, hash-collision]
see_also: [polynomial-hash-collision-bound, las-vegas-algorithm, monte-carlo-algorithm, anti-hash-tests, string-matching]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 32.2, The Rabin-Karp algorithm (the term spurious hit, the example with modulus 13, and the expected running time with v valid shifts)
  - paper: doi:10.1147/rd.312.0249
    title: R. M. Karp and M. O. Rabin, Efficient randomized pattern-matching algorithms, IBM Journal of Research and Development 31(2) (1987), 249-260
    locator: the fingerprint method with a random prime modulus and its error probability
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 5.3, Substring search (Rabin-Karp fingerprint search, its Monte Carlo and Las Vegas versions)
---

A spurious hit is a shift $s$ where the [Rabin-Karp](/rabin-karp/) hash of the text window $T[s \ldots s+m-1]$ equals the hash of the pattern $P$, but the window is not equal to $P$. It is a [hash collision](/hash-collision/) between the window and the pattern. A correct algorithm must compare the characters at each hit to reject the spurious ones, and the expected number of spurious hits decides whether Rabin-Karp runs in linear time.

## In plain words

Rabin-Karp turns the pattern into a number, a hash, and does the same for each piece of the text of the same length. Comparing two numbers is fast. If the numbers differ, the strings differ, so the piece is skipped.

But two different strings can get the same number, because there are many more strings than numbers. When a piece of text has the same number as the pattern but different letters, that is a spurious hit: a false alarm. The algorithm cannot tell a false alarm from a real match by the numbers alone, so it compares the letters every time the numbers are equal. With a good hash, false alarms are rare and this extra work is small.

## The idea

**Setting.** The alphabet is an integer alphabet $\{0, \ldots, \sigma - 1\}$, and indices are 0-based. Rabin-Karp fixes a base $d \ge \sigma$ and a modulus $q$, and uses the [polynomial hash](/polynomial-rolling-hash/)

$$h(x[0 \ldots m-1]) = \Big(\sum_{i=0}^{m-1} x[i]\, d^{\,m-1-i}\Big) \bmod q .$$

The hash of the next window follows from the hash of the current one in $O(1)$ arithmetic operations:

$$h(T[s+1 \ldots s+m]) = \big(d\,(h(T[s \ldots s+m-1]) - T[s]\, d^{\,m-1}) + T[s+m]\big) \bmod q .$$

**Definition.** A shift $s$ with $0 \le s \le n - m$ is a *hit* when $h(T[s \ldots s+m-1]) = h(P)$. A hit is *valid* when $T[s \ldots s+m-1] = P$, and *spurious* otherwise. Each valid shift is a hit, because equal strings have equal hashes. The converse fails as soon as $q < \sigma^m$, because then $h$ maps $\sigma^m$ strings into $q$ values and cannot be one-to-one.

**The cost of a hit.** Rabin-Karp compares the $m$ characters at each hit. A valid hit must be confirmed in any case, so the extra cost of hashing is the work on spurious hits: $O(m)$ each. With $v$ valid shifts and $h_s$ spurious hits, the search takes

$$O\big(n + m(v + h_s)\big)$$

time, after $O(m)$ preprocessing.

**How many spurious hits.** CLRS uses a heuristic model: if the window hashes behave like independent uniform values modulo $q$, each shift is a spurious hit with probability at most $1/q$, so $\mathbb{E}[h_s] \le (n - m + 1)/q$. With $q \ge m$ this gives $O(n + mv)$ expected time. The model is not a theorem about a fixed hash: an adversary who knows $d$ and $q$ can build a text where every window collides (see [anti-hash tests](/anti-hash-tests/)).

**A provable bound with a random base.** Let $q$ be a prime and choose the base $d$ uniformly at random from $\{0, \ldots, q - 1\}$, with $q > \sigma$. For two distinct strings $x \ne y$ of length $m$, the difference $\sum_i (x[i] - y[i])\, d^{\,m-1-i}$ is a nonzero polynomial in $d$ of degree at most $m - 1$ over the field $\mathbb{Z}_q$, because some coefficient $x[i] - y[i]$ is nonzero modulo $q$. Such a polynomial has at most $m - 1$ roots, so

$$\Pr_d\big[h(x) = h(y)\big] \le \frac{m - 1}{q} .$$

By [linearity of expectation](/linearity-of-expectation/) over the at most $n - m + 1$ shifts, $\mathbb{E}[h_s] \le (n - m + 1)(m - 1)/q$, for every text and pattern. Choosing $q \ge n m$ makes the expected number of spurious hits less than 1. The page [polynomial hash collision bound](/polynomial-hash-collision-bound/) states this bound in general. Karp and Rabin analyzed a different random choice: a fixed base and a random prime modulus.

**Verify or not.** If the algorithm compares the characters at each hit, it never makes a wrong report, and only its running time is random: a [Las Vegas](/las-vegas-algorithm/) algorithm. If it reports each hit without the check, it runs in $O(n + m)$ time always, but it may report a spurious hit as an occurrence: a [Monte Carlo](/monte-carlo-algorithm/) algorithm whose error probability is the probability of a spurious hit.

## Examples

**Spurious hits with a bad modulus.** Take decimal digits, $d = 10$, the pattern $P$ = 8182 and the text $T$ = 2718281828459045, so $n = 16$ and $m = 4$. With $q = 11$, $h(P) = 8182 \bmod 11 = 9$. The window hashes are:

| $s$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| window | 2718 | 7182 | 1828 | 8281 | 2818 | 8182 | 1828 | 8284 | 2845 | 8459 | 4590 | 5904 | 9045 |
| $\bmod 11$ | 1 | 10 | 2 | 9 | 2 | 9 | 2 | 1 | 7 | 0 | 3 | 8 | 3 |

There are two hits, at $s = 3$ and $s = 5$. The hit at $s = 5$ is valid. The hit at $s = 3$ is spurious: $8281 \ne 8182$, but $8281 = 752 \cdot 11 + 9$. The check of the 4 characters rejects it at the first character.

The modulus 11 is a bad choice for base 10. Since $10 \equiv -1 \pmod{11}$, the hash is the alternating sum of the digits, so any two windows whose digits in even places and in odd places have the same sums collide. Here 8281 and 8182 both have the digit sums $8 + 8$ and $2 + 1$ in those places.

**The same input with another modulus.** With $q = 13$ or $q = 7$, the only hit is $s = 5$, and there is no spurious hit.

**Rolling update.** With $q = 11$, the hash of the window 2718 is 1. The next hash is $(10 \cdot (1 - 2 \cdot 1000) + 8) \bmod 11 = 10$, the same as $7182 \bmod 11$.

**A non-example.** A valid shift is never spurious, even if the hash is weak. And a shift whose hash differs from $h(P)$ is never an occurrence, so there are no "false negatives": hashing can only add work, never miss an occurrence.

## Where it is used

- [Rabin-Karp](/rabin-karp/) checks each hit; its worst case $\Theta((n - m + 1)m)$ appears when every shift is a hit, valid or spurious.
- [Karp-Rabin for many patterns](/karp-rabin-multiple-patterns/) compares the window hash with a set of pattern hashes; a spurious hit can now match any of them.
- [Substring equality queries](/substring-equality-queries/) with prefix hashes have the same issue: equal hashes may come from different substrings.
- [Fingerprinting](/fingerprinting/) in general, where the probability of a spurious hit is the error of the method.
- Contest problems that break a fixed hash on purpose: [anti-hash tests](/anti-hash-tests/).

## References
