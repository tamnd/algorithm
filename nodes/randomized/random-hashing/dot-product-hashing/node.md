---
tag: 2WYWCR
kind: algorithm
slug: dot-product-hashing
name: Dot-product universal hash family
aliases:
- Dot-product hash function
- dot-product hashing
- linear hashing modulo a prime
- inner-product hash family
area: randomized/random-hashing
level: core
summary: A universal hash family that hashes a vector of key digits by taking their dot product with a random vector modulo a prime.
solves: [dictionary-problem]
model: word-ram
complexity:
  vars: {r: the number of base-p digits of a key, p: "the prime modulus, also the number of slots"}
  time: {worst: Θ(r)}
  space: {extra: Θ(r)}
properties: {deterministic: false, recursive: false}
history:
  year: 1979
  people: [J. Lawrence Carter, Mark N. Wegman]
  note: Carter and Wegman introduced universal classes of hash functions in 1979, among them linear maps; the dot-product family over a prime field is the textbook form used by Kleinberg and Tardos.
prereqs: [universal-hash-family, modular-inverse, linearity-of-expectation]
see_also: [universal-hashing, pairwise-independence, k-independent-hashing, multiply-shift-hashing, universal-hashing-expected-chain-length, universal-string-hashing, separate-chaining, tabulation-hashing]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Section 13.6, Hashing, A Randomized Implementation of Dictionaries (the family h_a(x) = a . x mod p and the proof that it is universal)
  - paper: doi:10.1016/0022-0000(79)90044-8
    title: J. Lawrence Carter and Mark N. Wegman, Universal classes of hash functions, Journal of Computer and System Sciences 18(2), 143 to 154, 1979
    locator: the definition of a universal class and the linear classes of hash functions
  - paper: doi:10.1016/0022-0000(81)90033-7
    title: Mark N. Wegman and J. Lawrence Carter, New hash functions and their use in authentication and set equality, Journal of Computer and System Sciences 22(3), 265 to 279, 1981
    locator: the definition of strongly universal classes
---

The dot-product hash family hashes a key into one of $p$ slots, for a prime $p$, by writing the key as a vector of $r$ digits $x = (x_0, \ldots, x_{r-1})$ in base $p$ and returning $h_a(x) = (a_0 x_0 + \cdots + a_{r-1} x_{r-1}) \bmod p$, where the vector $a$ is drawn uniformly from $\{0, \ldots, p-1\}^r$ once, when the table is built. Two distinct keys collide with probability exactly $1/p$ over the choice of $a$, so the family is [universal](/universal-hash-family/), and a table with [separate chaining](/separate-chaining/) has expected chain length at most $1 + n/p$ for every fixed set of $n$ keys. The proof is one line of linear algebra over the field $\mathbb{Z}_p$: the keys differ in some digit, and that digit's coefficient can absorb any value. Adding a random offset $b$ makes the family strongly universal. The family costs $r$ multiplications and $r$ random numbers, which is why fast tables use [multiply-shift hashing](/multiply-shift-hashing/) instead, but its proof is the simplest of all universal families, and it is the standard first example in the [randomized analysis of hashing](/universal-hashing-expected-chain-length/).

## In plain words

Write each key as a short list of small numbers, its digits. Pick a secret list of random numbers of the same length, once. To hash a key, multiply each digit by its secret number, add everything up, and keep the remainder after dividing by a prime, which is also the number of slots.

Two different keys differ in at least one digit. Whatever the other secret numbers are, exactly one value of the secret number for that digit makes the two sums land in the same slot. So the two keys collide for only one choice in every $p$. Nobody who picks the keys without seeing the secret can make many of them collide, on average.

## The problem

A dictionary stores a set $S$ of $n$ keys from a universe $U$ in a table of $p$ slots and must answer searches fast. A fixed hash function has inputs that put all keys in one slot: for $h(x) = x \bmod p$, all multiples of $p$ collide. The goal is a small family of functions, each easy to store and to evaluate, such that a function drawn at random from it makes each pair of distinct keys collide with probability at most $1/p$. Then the cost of each search is small in expectation for every input, which is the [dictionary problem](/dictionary-problem/) solved with [universal hashing](/universal-hashing/).

## The algorithm

Take $U = \{0, \ldots, p^r - 1\}$, and identify a key $x$ with its base-$p$ digits $x = x_0 + x_1 p + \cdots + x_{r-1} p^{r-1}$.

```pseudo id=main
DRAW(p, r)                                ▷ p is a prime
L1  a ← (a_0, ..., a_{r−1}), each a_i uniform in {0, ..., p − 1}, independent

HASH(a, x)                                ▷ x = (x_0, ..., x_{r−1}), the base-p digits of the key
L2  s ← 0
L3  for i ← 0 to r − 1
L4      s ← (s + a_i · x_i) mod p
L5  return s
```

DRAW runs once, when the table is built or rebuilt. HASH runs for each operation. The strongly universal variant also draws $b$ uniform in $\{0, \ldots, p-1\}$ and returns $(s + b) \bmod p$.

## Example

Let $p = 7$ and $r = 3$, so keys are $0, \ldots, 342$. The key $123 = 4 + 3 \cdot 7 + 2 \cdot 49$ has digits $(4, 3, 2)$, and $124$ has digits $(5, 3, 2)$. Draw $a = (3, 5, 1)$:

| key | digits | $a \cdot x$ | slot |
|---|---|---|---|
| 123 | (4, 3, 2) | 12 + 15 + 2 = 29 | 1 |
| 124 | (5, 3, 2) | 15 + 15 + 2 = 32 | 4 |

The keys 123 and 124 differ only in digit 0, by 1, so they collide exactly when $a_0 \cdot 1 \equiv 0$, that is $a_0 = 0$. That is $49$ of the $343$ vectors, a probability of $1/7$.

Now take the ten keys $7, 14, \ldots, 70$. The fixed function $x \bmod 7$ sends all of them to slot 0. With $a = (3, 5, 1)$ their slots are $5, 3, 1, 6, 4, 2, 1, 6, 4, 2$: no slot gets more than two keys.

For an exact check of the average, take $p = 13$, $r = 3$ and the 40 keys $13, 26, \ldots, 520$. Over all $13^3 = 2197$ vectors $a$, the number of colliding pairs has mean exactly $\binom{40}{2}/13 = 60$. The worst vectors, those with $a_1 = a_2 = 0$, still put all 40 keys in one slot, with $780$ colliding pairs. The guarantee is about the average over $a$, not about each $a$.

## Correctness

**Theorem.** Let $p$ be a prime. For all keys $x \ne y$ in $\{0, \ldots, p^r - 1\}$, $\Pr_a[h_a(x) = h_a(y)] = 1/p$. With the offset $b$, the pair $(h_{a,b}(x), h_{a,b}(y))$ is uniform on $\{0, \ldots, p-1\}^2$.

Put $d = x - y$ as digit vectors. Some digit $d_j$ is not zero. The keys collide when $a_j d_j = -\sum_{i \ne j} a_i d_i$ in $\mathbb{Z}_p$. For each of the $p^{r-1}$ choices of the other coordinates, exactly one $a_j$ solves this, because $d_j$ has an inverse modulo the prime $p$. So $p^{r-1}$ of the $p^r$ vectors make the keys collide. The full proof is below.

Then the [expected chain length bound](/universal-hashing-expected-chain-length/) applies: for each fixed set of $n$ keys, a search for an absent key meets at most $n/p$ keys in expectation, and a search for a stored key at most $1 + (n-1)/p$.

## Complexity

- **Hash time.** $r$ multiplications and additions of numbers below $p$, so $\Theta(r)$ word operations when $p^2$ fits in a word. For a universe of size $u$, $r = \lceil \log_p u \rceil$. Splitting a key into bytes by shifts is cheaper than base-$p$ digits, and it works if $p$ is larger than every byte: see Pitfalls.
- **Draw time and space.** $r$ random numbers below $p$, kept as $\Theta(r)$ words.
- **Table cost.** With chaining and $n \le p$ keys, each operation takes $O(r)$ expected time, for every fixed sequence of operations that does not depend on $a$.

## Properties

- **Exactly universal.** The collision probability is exactly $1/p$ for each pair, not just at most $1/p$.
- **Linear.** $h_a(x + y) = h_a(x) + h_a(y)$ in $\mathbb{Z}_p^r$. This is the source of the proof and also of a weakness: the key $0$ always goes to slot 0, and $h_a$ is not uniform on single keys. The offset $b$ fixes this.
- **Strongly universal with an offset.** $h_{a,b}(x) = (a \cdot x + b) \bmod p$ is [pairwise independent](/pairwise-independence/).
- **Not 3-wise independent.** For keys $x \ne y$ and the key $z = 2x - y$, formed digit by digit modulo $p$, $h_{a,b}(z) = 2h_{a,b}(x) - h_{a,b}(y) \bmod p$ for every $a$ and $b$, so the third value is fixed by the first two. For [k-wise independence](/k-independent-hashing/), use polynomials of degree $k - 1$.

## Variants and improvements

- **The affine family.** $h_{a,b}(x) = (a \cdot x + b) \bmod p$ with $p^{r+1}$ functions, strongly universal.
- **Random bit matrices.** Over the field with two elements, each of $\ell$ output bits is a dot product of the key bits with a random bit row. The result $h(x) = Mx$ for a random $\ell \times w$ bit matrix $M$ is universal with $2^\ell$ slots. Carter and Wegman studied this class in 1979.
- **A table size that is not a prime.** Hash with the affine family modulo a prime $p \ge m$ and then take the value modulo $m$. Each residue class modulo $m$ holds at most $\lceil p/m \rceil$ of the $p$ values, so two keys collide with probability at most $\lceil p/m \rceil / p \le 1/m + 1/p$.
- **Polynomial hashing.** [Universal string hashing](/universal-string-hashing/) uses one random point $z$ and the coefficients $a_i = z^i$. It needs one random number instead of $r$, but its collision probability rises to $(r - 1)/p$.
- **Word-RAM versions.** Replacing arithmetic modulo $p$ by arithmetic modulo a power of two and a final shift gives the vector form of [multiply-shift hashing](/multiply-shift-hashing/), which avoids the division.

## When to use it

Use the dot-product family to teach or to prove universal hashing, to hash fixed-length vectors of small numbers, such as tuples of IDs or IP addresses split into bytes, and whenever a prime modulus is cheap. When speed matters on 64-bit integers, [multiply-shift hashing](/multiply-shift-hashing/) or [tabulation hashing](/tabulation-hashing/) do the same job with one multiplication or a few table lookups. When the analysis needs more than pairs, for example for [linear probing](/linear-probing/) or [cuckoo hashing](/cuckoo-hashing/), use a [k-independent](/k-independent-hashing/) family.

## Pitfalls

- **A composite modulus.** Modulo $4$, the keys $0$ and $2$ collide for $a \in \{0, 2\}$, with probability $1/2$ instead of $1/4$. The digit difference must have an inverse, so the modulus must be a prime.
- **Digits not below p.** The proof needs the key to be a vector in $\mathbb{Z}_p^r$. If a digit can be $p$ or more, for example 8-bit bytes with $p = 251$, the bytes $3$ and $254$ are the same element of $\mathbb{Z}_{251}$, and two different keys can collide for every $a$. Choose $p$ larger than the largest digit, for example $p = 257$ for bytes.
- **Keys of different lengths.** Padding short keys with zero digits makes a key and the same key with extra zeros equal as vectors. Include the length in the key, or use one table per length.
- **An adaptive adversary.** The bound holds for keys fixed before $a$ is drawn. Someone who sees hash values can learn $a$ by solving linear equations, and then produce many collisions. Do not use the family where keys come from an attacker who sees timings or outputs.
- **Expecting a bound for each draw.** In the example with $p = 13$, the mean is 60 colliding pairs, but a few vectors give 780. Universality bounds the mean only; rehash if a chain gets long.

## Implementations

## History

Carter and Wegman introduced universal classes of hash functions in 1979, so that the expected cost of a hash table holds for every input, and studied several linear classes. In 1981 they defined strongly universal classes and used them for authentication and set equality tests. The dot-product family over a prime field is the version in the textbook of Kleinberg and Tardos, whose proof of universality is the one given here.

## References
