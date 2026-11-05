---
tag: 55Q9YH
kind: technique
slug: universal-string-hashing
name: Universal string hashing
aliases:
- Carter-Wegman string hashing
- polynomial universal hash family
area: strings/string-hashing
level: advanced
summary: Choose a random polynomial hash from a family so that any fixed pair of distinct strings collides with low probability.
prereqs: [universal-hash-family, polynomial-rolling-hash, polynomial-hash-collision-bound]
see_also: [hash-table, multiply-shift-hashing, tabulation-hashing, k-independent-hashing, pairwise-independence, siphash, poly1305, anti-hash-tests]
sources:
  - paper: doi:10.1016/0022-0000(79)90044-8
    title: J. Lawrence Carter and Mark N. Wegman, Universal classes of hash functions, Journal of Computer and System Sciences 18(2) (1979), 143-154
    locator: the definition of universal classes and the class of functions ((ax + b) mod p) mod m
  - paper: doi:10.1016/0022-0000(81)90033-7
    title: Mark N. Wegman and J. Lawrence Carter, New hash functions and their use in authentication and set equality, Journal of Computer and System Sciences 22(3) (1981), 265-279
    locator: strongly universal classes and their use for authentication and for testing set equality
  - url: https://arxiv.org/abs/1504.06804
    title: Mikkel Thorup, High speed hashing for integers and strings, lecture notes (arXiv 1504.06804)
    locator: Section 3.2 (multiply-mod-prime) and Section 5.3, Hashing variable length strings (the bound d/p, the composition with multiply-mod-prime, Exercise 5.4, and the speed-up by chunks)
  - paper: doi:10.1007/3-540-55719-9_77
    title: Martin Dietzfelbinger, Joseph Gil, Yossi Matias and Nicholas Pippenger, Polynomial hash functions are reliable, ICALP 1992, Lecture Notes in Computer Science 623, 235-246
    locator: random polynomials of bounded degree over a prime field as hash functions with limited independence
  - paper: doi:10.1093/comjnl/bxt070
    title: Daniel Lemire and Owen Kaser, Strongly universal string hashing is fast, The Computer Journal 57(11) (2014), 1624-1638
    locator: the multilinear families, their proofs of strong universality, and the measured speed
---

Universal string hashing picks a hash function for strings at random from a family, so that for every fixed pair of different strings the probability of a collision is small, with no assumption about how the strings are distributed. The standard family has two stages: a [polynomial hash](/polynomial-rolling-hash/) with a random base $c$ modulo a prime $p$ compresses a string of length at most $\ell$ to a number in $\{0, \ldots, p-1\}$ with collision probability at most $(\ell - 1)/p$, and a [universal hash](/universal-hash-family/) such as $((a v + b) \bmod p) \bmod m$ maps that number to one of $m$ buckets with collision probability at most $1/m$. Together they collide with probability at most $(\ell - 1)/p + 1/m$, which is close to $1/m$ when $p$ is much larger than $\ell m$. The idea goes back to Carter and Wegman (1979), and it gives [hash tables](/hash-table/) with string keys the same expected bounds as tables with integer keys.

## In plain words

A hash table puts each key in one of $m$ boxes, chosen by a hash function. If many keys land in one box, the table gets slow. For any one fixed hash function, someone can find many keys that land in one box.

The way out is to choose the hash function at random when the table is made, from a large family of functions. Then for any two different keys, fixed in advance, the chance that they land in the same box is about one in $m$, as if each key had picked its box at random.

For strings, the method first turns the string into one large number with a random base, and then turns that number into a box number with a second random rule. Each step adds a small chance of a clash, and the two chances add up.

## When it applies

- **Hashing strings into tables.** A [hash table](/hash-table/), a [perfect hashing](/perfect-hashing/) scheme or a sketch needs a hash of string keys with a proved bound on collisions, whatever the keys are.
- **Keys fixed before the seeds.** The bound holds for keys that do not depend on the random seeds. It holds for an adversary who chooses keys but never sees hash values or the timing that reveals them; against one who does, use a keyed function such as [SipHash](/siphash/).
- **Pairwise bounds suffice.** The analysis needs only the probability that two given keys collide, as for the expected length of a chain. Uses that need more independence take a family with stronger guarantees (see Variations).
- **Strings of bounded length.** The bound grows with the length $\ell$, so $p$ must be much larger than $\ell m$.

## The template

The strings are over an integer alphabet with codes $\mathrm{code}(x) \in \{1, \ldots, p - 1\}$; the code 0 is not used, which makes strings of different lengths safe (see Pitfalls). Indices are 0-based, and $\ell$ is the largest length of a key. A family $H$ of functions into $\{0, \ldots, m-1\}$ is *$\varepsilon$-almost universal* if $\Pr_{h \in H}[h(x) = h(y)] \le \varepsilon$ for all keys $x \ne y$, and *universal* if $\varepsilon = 1/m$.

```pseudo id=main
UNIVERSAL-STRING-HASH(x[0 .. ℓ_x − 1])
L1  once per table: c ← uniform from {0, ..., p − 1}; a ← uniform from {1, ..., p − 1}; b ← uniform from {0, ..., p − 1}   ▷ hole: the prime and the seeds
L2  v ← 0
L3  for i ← 0 to ℓ_x − 1 do v ← (c · v + code(x[i])) mod p        ▷ hole: the compressor
L4  return ((a · v + b) mod p) mod m                                 ▷ hole: the final hash into m buckets
```

**The holes.**

- *The prime and the seeds.* A prime $p$ larger than every code and much larger than $\ell m$, such as $2^{61} - 1$ or $2^{89} - 1$; Thorup suggests $2^{89} - 1$ with 64-wide characters. The seeds are drawn once, when the table is created, and kept secret.
- *The compressor.* Line L3 is Horner's rule for $g_c(x) = \sum_{i} \mathrm{code}(x[i])\, c^{\ell_x - 1 - i} \bmod p$. It can be replaced by any family that is $\varepsilon_1$-almost universal from strings to $\{0, \ldots, p-1\}$, such as a faster hash of fixed-size chunks followed by the polynomial on the chunk values.
- *The final hash.* Line L4 is the multiply-mod-prime family of Carter and Wegman. [Multiply-shift hashing](/multiply-shift-hashing/) into $2^k$ buckets is faster on binary computers, and [tabulation hashing](/tabulation-hashing/) gives stronger independence.

**Lemma 1 (the compressor).** For different strings $x, y$ of length at most $\ell$, $\Pr_c[g_c(x) = g_c(y)] \le (\ell - 1)/p$.

*Proof.* $g_c(x) - g_c(y)$ is a polynomial in $c$ of degree at most $\ell - 1$. It is not the zero polynomial modulo $p$. If $|x| > |y|$, its coefficient of $c^{|x| - 1}$ is $\mathrm{code}(x[0]) \in \{1, \ldots, p-1\}$. If $|x| = |y|$, it has the coefficient $\mathrm{code}(x[i]) - \mathrm{code}(y[i]) \not\equiv 0$ at the first $i$ where $x$ and $y$ differ. A nonzero polynomial of degree at most $\ell - 1$ over the field $\mathbb{Z}_p$ has at most $\ell - 1$ roots, and $c$ is uniform over $p$ values. $\square$

**Lemma 2 (the final hash).** For $u \ne v$ in $\{0, \ldots, p-1\}$, $\Pr_{a, b}[f_{a,b}(u) = f_{a,b}(v)] \le 1/m$, where $f_{a,b}(u) = ((a u + b) \bmod p) \bmod m$.

*Proof.* The map $(a, b) \mapsto (s, t) = ((a u + b) \bmod p, (a v + b) \bmod p)$ is a bijection from $\{1, \ldots, p-1\} \times \{0, \ldots, p-1\}$ onto the pairs with $s \ne t$: given $(s, t)$, $a = (s - t)(u - v)^{-1}$ and $b = s - a u$ modulo $p$, and $a \ne 0$ exactly when $s \ne t$. So $(s, t)$ is uniform over the $p(p-1)$ pairs with $s \ne t$. For each $s$, at most $\lceil p/m \rceil - 1 \le (p - 1)/m$ values $t \ne s$ have $t \equiv s \pmod m$. So at most $p(p-1)/m$ of the $p(p-1)$ pairs collide. $\square$

**Theorem (composition).** For different strings $x, y$ of length at most $\ell$, $\Pr[h(x) = h(y)] \le (\ell - 1)/p + 1/m$, where $h$ is the function of lines L2 to L4.

*Proof.* A collision needs $g_c(x) = g_c(y)$, of probability at most $(\ell - 1)/p$ by Lemma 1, or $g_c(x) \ne g_c(y)$ and $f_{a,b}(g_c(x)) = f_{a,b}(g_c(y))$. The seeds $a, b$ are independent of $c$, so for each fixed $c$ with $g_c(x) \ne g_c(y)$ the second event has probability at most $1/m$ by Lemma 2. Add the two bounds. $\square$

In general, an $\varepsilon_1$-almost universal compressor followed by an independent $\varepsilon_2$-almost universal final hash is $(\varepsilon_1 + \varepsilon_2)$-almost universal, by the same argument. If $\ell \le p/m$, the bound is at most $2/m$, which is Thorup's Exercise 5.4.

**Cost.** One multiplication and one reduction modulo $p$ per character, and $O(1)$ more for line L4; three seeds of $O(\log p)$ binary places.

**Example.** Take $p = 101$, $m = 10$, the codes a = 1, b = 2, c = 3, and the seeds $c = 5$, $a = 17$, $b = 33$.

| key $x$ | $v = g_5(x)$ | $(17 v + 33) \bmod 101$ | bucket |
|---|---|---|---|
| ab | 7 | 51 | 1 |
| ba | 11 | 18 | 8 |
| abc | 38 | 73 | 3 |
| cba | 86 | 81 | 1 |
| b | 2 | 67 | 7 |

The keys ab and cba share bucket 1 though their compressed values 7 and 86 differ: a collision of the final stage. Over all seeds, the exact collision probabilities are as follows.

| pair | $\Pr_c[g_c(x) = g_c(y)]$ | Lemma 1 bound | $\Pr[h(x) = h(y)]$ | theorem bound |
|---|---|---|---|---|
| ab, ba | $1/101$ | $1/101$ | $1021/10201 \approx 0.1001$ | $0.1099$ |
| abc, cba | $2/101$ | $2/101$ | $5564/51005 \approx 0.1091$ | $0.1198$ |
| aab, bab | $1/101$ | $2/101$ | $1021/10201 \approx 0.1001$ | $0.1198$ |

For ab and ba the difference polynomial is $(1 \cdot c + 2) - (2c + 1) = 1 - c$, with the single root $c = 1$. For abc and cba it is $-2c^2 + 2 = -2(c - 1)(c + 1)$, with the roots $1$ and $100$, so Lemma 1 is tight there.

## Classic examples

- **[Hash tables](/hash-table/) with string keys.** With chaining and $n$ keys in $m$ buckets, the expected number of other keys in the bucket of a given key is at most $(n-1)\big((\ell - 1)/p + 1/m\big)$, so operations take $O(\ell + 1 + n/m)$ expected time for every set of keys.
- **[Perfect hashing](/perfect-hashing/) of strings.** The two-level scheme of Fredman, Komlós and Szemerédi needs only a universal family at each level; with a string compressor in front, it stores a static set of strings with $O(1)$ worst-case lookups after $O(\ell)$ work to compress the key.
- **Message authentication.** The Wegman-Carter construction authenticates a message by a universal hash of the message, hidden by a one-time pad. [Poly1305](/poly1305/) follows this pattern with a polynomial evaluated at a secret point modulo the prime $2^{130} - 5$.
- **[Rabin-Karp](/rabin-karp/) and [string equality testing](/string-equality-testing/).** Both use the compressor of line L3 alone, with $m = p$, and compare the values of Lemma 1.

## Variations

- **Strongly universal families.** A family is strongly universal (pairwise independent) if $(h(x), h(y))$ is uniform over all pairs of buckets for every $x \ne y$. For strings of one fixed length $d$, the multilinear family $h(x) = (b + \sum_{i} a_i\, \mathrm{code}(x[i])) \bmod p$ with independent uniform $a_0, \ldots, a_{d-1}, b$ is strongly universal into $\{0, \ldots, p-1\}$. It needs a random key for each position. Lemire and Kaser give multilinear families for strings with simple proofs of strong universality, and measure about 0.2 CPU cycles per byte.
- **Higher independence.** A random polynomial of degree $k - 1$ over a prime field, applied to the compressed value, gives a $k$-wise independent final stage; Dietzfelbinger, Gil, Matias and Pippenger study such polynomials as hash functions. See [k-independent hashing](/k-independent-hashing/).
- **Chunks first.** Thorup reduces each chunk of 32 words to one word with a fast strongly universal multiply-shift scheme, and runs the polynomial over the chunk values. Each stage adds its collision probability, and the slow modular arithmetic runs once per chunk.
- **A random final stage only.** A design that fixes the base of the compressor and draws only $a$ and $b$ gains nothing against chosen keys: two strings that collide in the compressor collide for every final seed.

## Pitfalls

- **The code 0 with keys of different lengths.** If a character has code 0, then 0x and x have the same compressed value for every $c$, since Horner's rule ignores leading zeros. Use codes from 1, or append the length of the key.
- **Long keys and a small prime.** The bound $(\ell - 1)/p$ is useless when $\ell$ is close to $p$. A 32-wide prime and keys of a million characters give no guarantee; use a prime above $\ell m$.
- **Arithmetic modulo $2^{64}$.** The compressor needs a prime field. With wrap-around arithmetic, Thue-Morse strings collide for every odd base; see [anti-hash-tests](/anti-hash-tests/).
- **Fixed or leaked seeds.** The probability is over the seeds. A seed fixed in the code, derived from the clock in a guessable way, or revealed by output or timing lets an adversary choose colliding keys.
- **More than pairs.** A universal family bounds the expected chain length but not, for example, the behavior of linear probing, which needs more independence. Check which property the analysis of the data structure uses.
- **Bias of the final modulo.** $(s \bmod m)$ for uniform $s$ in $\{0, \ldots, p-1\}$ is not exactly uniform when $m$ does not divide $p$. This does not affect Lemma 2, but a strongly universal analysis must count the bias, of order $m/p$.

## Exercises

1. Prove the general composition: an $\varepsilon_1$-almost universal family followed by an independent $\varepsilon_2$-almost universal family is $(\varepsilon_1 + \varepsilon_2)$-almost universal.
2. Show that with $\mathrm{code}(\mathrm{a}) = 0$, the keys b and ab collide for every seed, and that appending the length of the key to the string restores Lemma 1.
3. Verify the entry $1021/10201$ of the example table. *Hint:* for $p = 101$ and $m = 10$, exactly 920 of the 10100 pairs $(s, t)$ with $s \ne t$ have $t \equiv s \pmod{10}$, so the final stage collides with probability $920/10100$ whenever the compressed values differ, which happens for 100 of the 101 bases.
4. Prove that the multilinear family on strings of fixed length $d$ is strongly universal into $\{0, \ldots, p - 1\}$.
5. A table stores $n = 10^6$ string keys of length at most $\ell = 10^4$ in $m = 2^{20}$ buckets with $p = 2^{61} - 1$. Bound the expected number of other keys in the bucket of a key. *Answer:* $(n - 1)\big((\ell - 1)/p + 1/m\big) < 0.954$.

## References
