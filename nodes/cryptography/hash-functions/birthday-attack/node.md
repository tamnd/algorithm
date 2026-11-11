---
tag: 4ZQ3BQ
kind: algorithm
slug: birthday-attack
name: Birthday attack
aliases:
- birthday collision search
area: cryptography/hash-functions
level: core
summary: Hash many distinct inputs and keep the digests in a table until two match. For an n-bit hash this finds a collision after about 1.25 times 2^(n/2) queries.
solves: [collision-finding]
model: query-model
complexity:
  vars: {n: the digest length in bits, N: the number of digests 2^n, q: the number of queries}
  time: {worst: O(2^n), average: Θ(2^(n/2))}
  space: {extra: Θ(2^(n/2))}
properties: {deterministic: true}
history:
  year: 1979
  people: [Gideon Yuval]
  note: Yuval showed that a signer can be cheated with two meaningful messages that collide under a 2^(n/2) search, which made the birthday paradox an attack on hash functions.
prereqs: [collision-resistance, birthday-paradox]
see_also: [collision-finding, pollard-rho-collision-search, birthday-paradox, multicollision-attack, generalized-birthday-problem, prp-prf-switching-lemma, brassard-hoyer-tapp-collision, distinguished-points]
sources:
  - paper: "Gideon Yuval, How to swindle Rabin, Cryptologia 3(3), 1979, pages 187 to 190"
    locator: the attack on a signed hash with 2^(n/2) variants of a fair and a fraudulent message
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Section 6.4.1 (birthday attacks for finding collisions) and Appendix A.4 (the upper bound q^2/2N and the lower bound q(q-1)/4N for q at most sqrt(2N))
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Section 8.3 (generic birthday attacks on collision resistance) and Appendix B.1 (the birthday paradox, with the bound for non-uniform outputs)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 2.1.5 (birthday problems) and Section 9.7.1 (Yuval's birthday attack)
  - paper: "Karthikeyan Bhargavan and Gaetan Leurent, On the practical (in-)security of 64-bit block ciphers: collision attacks on HTTP over TLS and OpenVPN, ACM CCS 2016, pages 456 to 467"
    locator: the Sweet32 attack on 3DES and Blowfish in CBC mode after about 2^32 blocks
  - url: "https://csrc.nist.gov/pubs/fips/180-4/upd1/final"
    title: NIST, FIPS 180-4, Secure Hash Standard, 2015
    locator: Section 6.2 (SHA-256), the hash that is truncated in the example
---

The birthday attack is the generic way to find a collision of a hash function $H$ with $n$-bit output: hash many distinct inputs, keep each digest in a table, and stop when a digest repeats. It solves [collision finding](/collision-finding/) for every hash in about $\sqrt{\pi 2^n/2} \approx 1.25 \cdot 2^{n/2}$ queries on average, far fewer than the $2^n$ that a search for one fixed digest needs. This is why a hash with $n$-bit output gives at most $n/2$ bits of [collision resistance](/collision-resistance/), and why SHA-256 has 256 bits of output for 128-bit security. The same count is behind the [birthday paradox](/birthday-paradox/): in a room of 23 people, two share a birthday with probability above one half.

## In plain words

Imagine a hash as a machine that gives each document a number from a fixed range. You want two different documents with the same number. Do not pick one number and hunt for a second document that hits it: that takes about as many tries as there are numbers. Instead, hash many documents and watch for any two that match.

Each new document can match any of the ones before it, so the number of pairs grows much faster than the number of documents. With a million possible numbers, about twelve hundred documents are enough for an even chance of a match. In general, the square root of the size of the range is the right scale.

The price is memory: you must remember every number you have seen.

## The problem

The input is a function $H : \{0,1\}^\ast \to \{0,1\}^n$, given as a black box in the [query model](/query-model/). The output is a *collision*: two inputs $x_1 \ne x_2$ with $H(x_1) = H(x_2)$. The cost is the number $q$ of calls of $H$. Write $N = 2^n$. For the average case, $H$ is modelled as a random function, so the digests of distinct inputs are independent and uniform on $N$ values.

## The algorithm

BIRTHDAY-ATTACK feeds distinct inputs to $H$ and stores each digest with the input that gave it.

```pseudo id=main
BIRTHDAY-ATTACK(H, prefix)
L1  T ← empty dictionary                     ▷ digest → input
L2  for i ← 0, 1, 2, ... do
L3      x ← prefix ∥ i                       ▷ i in 8 bytes, so each x is new
L4      y ← H(x)
L5      if y ∈ T then return (T[y], x)
L6      T[y] ← x
```

The inputs need only be distinct. A counter is the simplest choice. Yuval's form uses $n/2$ independent choices of wording in a letter, so that each input is a meaningful text.

The Python code for this page runs the attack on SHA-256 truncated to 16, 24 and 32 bits. It also computes the exact probability and the bounds below. It is for study only and it is not constant time. Full SHA-256 is far out of reach of this attack. Use the hash functions of the Python standard library (hashlib), a FIPS 140 validated module, or libsodium for real work.

## Example

Let $H(x)$ be the first 24 bits of SHA-256$(x)$, so $N = 2^{24} = 16777216$. The inputs are the 4 bytes `algo` followed by an 8-byte big-endian counter.

The attack stops at query $q = 6603$. The inputs with counters 6063 and 6602 give

| counter | SHA-256 of the input, first 8 bytes |
|---|---|
| 6063 | `4b6ce1fbe9abb915` |
| 6602 | `4b6ce1de0fc6d539` |

The first 3 bytes match, so the two inputs collide under $H$. The expected stopping point is $\sqrt{\pi N/2} + 2/3 \approx 5134$. The median is $1.1774 \cdot 2^{12} \approx 4823$. With 32 bits, the same code stops at query 86504, near the expected value $82137$.

The probability $P(q)$ that $q$ random digests contain a repeat, for $n = 24$:

| $q$ | $P(q)$ exact | lower bound $1 - e^{-q(q-1)/2N}$ | upper bound $q(q-1)/2N$ | $q(q-1)/4N$ |
|---|---|---|---|---|
| 1024 | 0.0307 | 0.0307 | 0.0312 | 0.0156 |
| 2048 | 0.1175 | 0.1174 | 0.1249 | 0.0625 |
| 4096 | 0.3934 | 0.3934 | 0.4999 | 0.2499 |
| 4823 | 0.5000 | 0.5000 | 0.6931 | 0.3465 |
| 8192 | 0.8647 | 0.8646 | 1.9998 | 0.9999 |

**Simulation.** The test draws 3000 runs of $q$ uniform values from $2^{16}$ with the seed 20240611. The observed rates are 0.075, 0.488 and 0.850 for $q$ = 100, 302 and 500. The formula gives 0.073, 0.501 and 0.852. Over 300 runs of the attack on SHA-256 truncated to 16 bits, the mean stopping point is 316.9. The formula gives 321.5.

## Correctness

Each input has the form prefix $\|$ $i$ with a different $i$, so all inputs are distinct. The table maps each digest seen so far to the first input that gave it. Line L5 returns $(T[y], x)$ only when $y = H(x)$ is already a key of $T$. Then $H(T[y]) = y = H(x)$, and $T[y] \ne x$ because $T[y]$ was made by an earlier counter. So each output is a real collision. The loop ends: after $N + 1$ queries, two of the $N + 1$ digests are equal by the pigeonhole principle. The full proof is below.

## Complexity

Let $q$ digests be independent and uniform on $N$ values. The probability that they are all distinct is

$$\bar P(q) = \prod_{i=1}^{q-1} \left(1 - \frac{i}{N}\right).$$

Since $1 - x \le e^{-x}$, and by the union bound over the $\binom{q}{2}$ pairs,

$$1 - e^{-q(q-1)/2N} \;\le\; P(q) = 1 - \bar P(q) \;\le\; \frac{q(q-1)}{2N}.$$

Katz and Lindell also give $P(q) \ge q(q-1)/4N$ for $q \le \sqrt{2N}$ (Appendix A.4). The two sides meet up to a factor of 2, so $P(q) = \Theta(q^2/N)$ while $q \le \sqrt{2N}$.

- **Median.** Setting $1 - e^{-q^2/2N} = 1/2$ gives $q = \sqrt{2 \ln 2} \cdot \sqrt N \approx 1.1774 \cdot 2^{n/2}$. For probability $p$, $q \approx \sqrt{2N \ln(1/(1-p))}$.
- **Mean.** The expected index of the first repeat is $\sum_{q \ge 0} \bar P(q) \approx \sqrt{\pi N/2} + 2/3 \approx 1.2533 \cdot 2^{n/2}$.
- **Worst case.** At most $N + 1$ queries.
- **Space.** The table holds every digest, so $\Theta(2^{n/2})$ entries on average. Each entry holds a digest and an input.
- **Time per query.** One call of $H$ and one expected $O(1)$ lookup in a [hash table](/hash-table/). A sorted list gives $O(q \log q)$ instead.

| hash | $n$ | median queries $1.1774 \cdot 2^{n/2}$ |
|---|---|---|
| CRC-32, a 32-bit checksum | 32 | $2^{16.2}$ |
| a 64-bit block or digest | 64 | $2^{32.2}$ |
| MD5 | 128 | $2^{64.2}$ |
| SHA-1 | 160 | $2^{80.2}$ |
| SHA-256 | 256 | $2^{128.2}$ |

Real attacks on MD5 and SHA-1 are much cheaper than these numbers, because they use the structure of the compression function. See [collision finding](/collision-finding/).

## Properties

- **Generic.** It uses $H$ only as a black box. No hash with $n$-bit output can resist more than about $2^{n/2}$ queries.
- **Optimal for classical query algorithms.** By the upper bound above, $q$ queries to a random function find a collision with probability at most $q^2/2N$. So $\Omega(2^{n/2})$ queries are needed for a constant success rate.
- **Memory bound.** The attack needs as much memory as time. This is its main cost in practice, and the reason to use [Pollard rho](/pollard-rho-collision-search/).
- **Free choice of inputs.** Any distinct inputs work. This is what lets the attacker choose meaningful texts.
- **Non-uniform outputs help.** If $H$ is not uniform, collisions come sooner: the probability of a repeat is smallest when the outputs are uniform.

## Variants and improvements

- **Two lists (Yuval).** Make $2^{n/2}$ variants of a fair message and $2^{n/2}$ variants of a fraudulent one, and look for a digest common to both lists. About $2^{n/2}$ variants of each give a match with constant probability. Variants come from $n/2$ independent changes, such as a space or two spaces after a sentence. The victim signs the fair one, and the signature is valid on the fraudulent one.
- **Memoryless search.** [Pollard rho collision search](/pollard-rho-collision-search/) walks $x \mapsto H(x)$ and finds the cycle with $O(1)$ memory, at about three times the queries.
- **Parallel search.** Van Oorschot and Wiener let many machines walk until a [distinguished point](/distinguished-points/) and share only those points. The speedup is linear in the number of machines.
- **Generalized birthday.** To find $k$ values that XOR to zero, one from each of $k$ lists, [Wagner's algorithm](/wagners-algorithm/) is faster than $2^{n/2}$. See the [generalized birthday problem](/generalized-birthday-problem/).
- **Multicollisions.** For an iterated hash, Joux finds $2^t$ messages with one digest at the cost of $t$ birthday attacks. See [multicollision attack](/multicollision-attack/).
- **Quantum search.** The [Brassard, Hoyer and Tapp algorithm](/brassard-hoyer-tapp-collision/) finds a collision in about $2^{n/3}$ quantum queries, with $2^{n/3}$ memory.

## When to use it

Use it to set the security level of each hash, MAC tag, nonce or block size. To reach $s$ bits of collision resistance, choose an output of at least $2s$ bits. Use the attack itself to find a collision of a short digest, for example a truncated hash used as an identifier, with enough memory for about $2^{n/2}$ entries. When memory is short, use the rho or distinguished point method instead.

The same bound decides how much data a key may protect:

- **[PRP-PRF switching](/prp-prf-switching-lemma/).** A random permutation on $n$-bit blocks and a random function differ only when the function repeats a value. So an adversary with $q$ queries has advantage at most $q(q-1)/2^{n+1}$ in telling them apart.
- **Sweet32.** In [CBC mode](/cbc-mode/) with a 64-bit block, two equal ciphertext blocks reveal the XOR of two plaintext blocks. About $2^{32}$ blocks, or 32 GiB, give such a pair with good probability. Bhargavan and Leurent used this in 2016 to recover HTTP cookies from [Triple DES](/triple-des/) and [Blowfish](/blowfish/) connections. Use a 128-bit block cipher such as AES.
- **Random nonces.** Random 96-bit nonces for AES-GCM repeat after about $2^{48}$ messages, which is why NIST limits the number of messages per key.

## Pitfalls

- **Half the output length.** A 128-bit digest gives 64 bits of collision security, not 128. Truncating a hash to $n$ bits cuts the collision cost to $2^{n/2}$.
- **Collisions are not preimages.** The attack does not help to find an input for a given digest. That costs $2^n$; see [preimage finding](/preimage-finding/).
- **The adversary chooses the pair.** The attack controls both messages. Protocols where the attacker chooses the message that someone else will sign or commit to need collision resistance, not only second-preimage resistance.
- **Memory is the real limit.** At $n = 80$ the table would hold about $2^{40}$ entries. Use the memoryless or parallel methods.
- **Counting from one.** The probability of a repeat with $q$ values uses $q(q-1)/2$ pairs, not $q^2$. The difference matters only for small $q$.

## Implementations

## History

The birthday problem is an old exercise of probability theory. Yuval turned it into an attack on hash-then-sign in 1979: a signer who signs the hash of a contract can be cheated with a fraudulent contract that has the same 64-bit hash, after about $2^{32}$ variants of each. Since then, every hash standard has fixed its output length from this bound. The bound has also limited block ciphers: the Sweet32 attack of Bhargavan and Leurent in 2016 showed that 64-bit blocks are unsafe for long connections, and led TLS libraries and OpenVPN to move away from Triple DES and Blowfish.

## References
