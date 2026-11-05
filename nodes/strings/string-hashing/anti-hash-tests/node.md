---
tag: 8J3FT5
kind: concept
slug: anti-hash-tests
name: Anti-hash tests
aliases:
- hash collision attacks
- adversarial collision inputs
area: strings/string-hashing
level: intro
summary: Adversarial string pairs that collide under a fixed base and modulus, such as Thue-Morse strings against modulus 2^64.
prereqs: [polynomial-rolling-hash, hash-collision, thue-morse-word]
see_also: [polynomial-hash-collision-bound, birthday-paradox, algorithmic-complexity-attack, universal-string-hashing, lll-algorithm, chinese-remainder-theorem, rabin-karp, siphash]
sources:
  - url: https://ioinformatics.org/journal/INFOL119.pdf
    title: Jakub Pachocki and Jakub Radoszewski, Where to use and how not to use polynomial string hashing, Olympiads in Informatics 7 (2013), 90-100
    locator: Section 2.4 with Theorem 1 (Thue-Morse strings collide modulo 2^64 for every odd base) and Section 2.3 (the birthday paradox for fixed parameters)
  - url: https://arxiv.org/abs/1504.06804
    title: Mikkel Thorup, High speed hashing for integers and strings, lecture notes (arXiv 1504.06804)
    locator: Section 5.3, Hashing variable length strings (the collision bound for a random point modulo a prime, which a fixed point does not have)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Section 5.1, The birthday paradox
---

Anti-hash tests are inputs built to make a string hash fail: two different strings with the same hash, or many strings with one hash. They exist for every hash whose parameters are fixed or can be guessed, because a hash maps infinitely many strings to finitely many values. For the [polynomial rolling hash](/polynomial-rolling-hash/) they are easy to build in three common cases: arithmetic modulo $2^{64}$, where strings built from the [Thue-Morse word](/thue-morse-word/) collide for every odd base; a fixed prime modulus near $10^9$, where the [birthday paradox](/birthday-paradox/) gives a collision among a few tens of thousands of random strings; and a fixed base with a larger prime, where a short search finds strings whose difference is a multiple of the modulus. The defense is a prime modulus with a base drawn at run time, which restores the [collision bound](/polynomial-hash-collision-bound/) for inputs fixed before the draw.

## In plain words

A hash turns a string into a number from a limited range. There are more strings than numbers, so some different strings must share a number. A hash is safe in practice only if nobody can find such strings when they want to.

If the method and all its constants are known, a person who wants to break a program can search for two strings with the same number and feed them to it. The program then thinks the strings are equal, or puts them all in one bucket and becomes slow. Programming contests call such inputs anti-hash tests.

The cure is to make one constant a secret random choice, made each time the program runs. Then the person who writes the input does not know which strings will clash.

## The idea

Write $h_{B,M}(x) = \sum_{i=0}^{\ell-1} c(x_i)\, B^{\ell-1-i} \bmod M$ for a string $x = x_0 \cdots x_{\ell-1}$, base $B$ and modulus $M$. Indices are 0-based, and the codes here are the ASCII values, so $c(\mathrm{a}) = 97$ and $c(\mathrm{b}) = 98$. Two strings $x \ne y$ of the same length collide exactly when $M$ divides the difference

$$D(B) = \sum_{i} (c(x_i) - c(y_i))\, B^{\ell-1-i}.$$

An attack is a way to make $M$ divide $D(B)$.

**1. Modulus $2^{64}$, every odd base (Thue-Morse).** Define $S_0 = \mathrm{a}$, $T_0 = \mathrm{b}$ and $S_{i+1} = S_i T_i$, $T_{i+1} = T_i S_i$. Then $S_k$ is the prefix of length $2^k$ of the Thue-Morse word, and $T_k$ is $S_k$ with a and b swapped. Since $h(uv) = h(u) B^{|v|} + h(v)$,

$$h(S_{i+1}) - h(T_{i+1}) = \big(h(S_i) - h(T_i)\big)\big(B^{2^i} - 1\big), \quad\text{so}\quad D_k = (c(\mathrm{a}) - c(\mathrm{b})) \prod_{i=0}^{k-1}\big(B^{2^i} - 1\big).$$

For odd $B$, $B - 1$ is even; $B^2 - 1 = (B-1)(B+1)$ is a product of two consecutive even numbers, so 8 divides it; and $B^{2^{i}} - 1 = (B^{2^{i-1}} - 1)(B^{2^{i-1}} + 1)$ adds at least one factor 2 at each step. So $2^{i+2}$ divides $B^{2^i} - 1$ for $i \ge 1$, and the power of 2 in $D_k$ is at least

$$1 + \sum_{i=1}^{k-1} (i + 2) = \frac{k^2 + 3k - 2}{2}.$$

For $k = 10$ this is 64. So the two strings $S_{10}$ and $T_{10}$, of length 1024, collide modulo $2^{64}$ for every odd base. Pachocki and Radoszewski prove the weaker count $k(k+1)/2$, which gives length 2048 with $k = 11$. The count above is exact for $B \equiv 3 \pmod 8$, so for $B = 3$ the length 512 is not enough.

**2. Modulus $2^{64}$, even base.** Then $B^{64} \equiv 0$, so only the last 64 characters count. Any two strings that differ only before their last 64 characters collide, such as a followed by 64 copies of x and b followed by 64 copies of x.

**3. Fixed small prime: the birthday attack.** For a fixed $B$ and $M$, compute the hashes of random strings until two are equal. If the hash behaves like a random function, a collision is expected after about $\sqrt{\pi M / 2}$ strings, by the [birthday paradox](/birthday-paradox/). For $M = 10^9 + 7$ that is about 40 000 strings; for $M$ near $10^{18}$ it is about $1.25 \times 10^9$, which is slow but feasible with care.

**4. Fixed larger prime or a pair of primes: the tree attack.** Look for coefficients $d_j \in \{-1, 0, 1\}$, not all zero, with $\sum_j d_j B^{n-1-j} \equiv 0 \pmod M$. Then the strings $x$ with b where $d_j = 1$ and a elsewhere, and $y$ with b where $d_j = -1$ and a elsewhere, collide. Start with the $n = 2^k$ values $B^{n-1-j} \bmod M$, each a tree with one leaf. In each round, sort the values and pair neighbors, replacing each pair by its difference, the larger minus the smaller; the sign of each leaf flips in the subtracted tree. The differences of sorted neighbors are much smaller than the values, so after a few rounds some value becomes 0, and the leaves of its tree give the $d_j$. This is a heuristic without a proof of success, but it works well in practice. A pair of hashes modulo two primes $p_1, p_2$ with the same base is one hash modulo $p_1 p_2$; with different bases, the [Chinese remainder theorem](/chinese-remainder-theorem/) gives one base $B$ modulo $p_1 p_2$ that acts as both. [Lattice reduction](/lll-algorithm/) finds even shorter collisions.

**Why a random base defeats these.** For a prime $p$ and a base drawn uniformly after the strings are fixed, two distinct strings of length at most $n$ collide with probability at most $(n-1)/p$, whatever the strings are. An attacker who must commit to the input first cannot do better than this bound. Attacks 1 and 2 survive a random base, because they break $2^{64}$ for every odd base or every even base; attacks 3 and 4 need the base. A random base also does not help if the program reveals hash values or its base, for example in its output, its timing or a fixed random seed.

## Examples

The pairs below collide under the stated parameters; the codes are the ASCII values.

| hash | colliding pair | length |
|---|---|---|
| modulo $2^{64}$, every odd base | $S_{10}$ and $T_{10}$ (Thue-Morse) | 1024 |
| modulo $2^{64}$, every even base | a $x^{64}$ and b $x^{64}$ | 65 |
| modulo $10^9 + 7$, base 131 | awqltuyhia and biokpmppic, both of hash 980911739 | 10 |
| modulo $10^9 + 7$, base 131 | a pair from the tree attack | 512 |
| modulo $2^{61} - 1$, base 131 | a pair from the tree attack | 4096 |
| modulo $(10^9 + 7) \cdot 998244353$, base 131 | a pair from the tree attack | 4096 |

The birthday pair in the third row came up after 64 505 random strings of 10 lowercase letters, in line with the expected order of 40 000. The first eight characters of $S_{10}$ are abbabaab. For the base 3 modulo $2^{64}$, the Thue-Morse pair of length 512 does not collide, as the count of factors 2 predicts: it is $(81 + 27 - 2)/2 = 53 < 64$ for $k = 9$.

**A non-example.** With $p = 2^{61} - 1$ and a base drawn at run time, none of these pairs is a threat in advance. The Thue-Morse pair of length 1024 collides for at most 1023 of the $p$ bases, a probability below $4.5 \times 10^{-16}$. The tree-attack pair for base 131 collides for base 131 and at most 4094 other bases.

## Where it is used

- **Programming contests.** In contests with hacking phases, contestants submit anti-hash tests against solutions with a fixed base, a well-known modulus, or arithmetic modulo $2^{64}$. Pachocki and Radoszewski wrote their paper to explain these failures to contestants.
- **Denial of service on hash tables.** Many keys with one hash value make a [hash table](/hash-table/) degrade from $O(1)$ to $\Theta(n)$ time per operation. This is an [algorithmic complexity attack](/algorithmic-complexity-attack/), and it led language runtimes to use keyed hashes such as [SipHash](/siphash/) with a random key per process.
- **Testing hash-based code.** Test suites for [Rabin-Karp](/rabin-karp/), substring hashing and hash tables include such pairs, to check that the code verifies matches or that its parameters are random.
- **Choosing parameters.** The attacks explain the usual advice: a prime modulus, a large one such as $2^{61} - 1$, and a base drawn at run time.

## References
