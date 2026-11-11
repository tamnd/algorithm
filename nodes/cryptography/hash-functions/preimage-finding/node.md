---
tag: HTNXXE
kind: problem
slug: preimage-finding
name: Preimage finding
aliases:
- inverting a hash
area: cryptography/hash-functions
level: core
summary: Given a digest y, find any input x with H(x) = y. Generic cost 2^n for n-bit output. Meet in the middle beats it when the compression function can be run backwards.
prereqs: [preimage-resistance]
see_also: [time-memory-tradeoff, meet-in-the-middle-attack, davies-meyer-construction, md4, md5, second-preimage-finding, collision-finding, password-hashing]
sources:
  - paper: "Gaetan Leurent, MD4 is not one-way, FSE 2008, LNCS 5086, pages 412 to 428"
    locator: the first preimage attack on full MD4, about 2^102 work, from a pseudo-preimage attack and a meet in the middle on the chaining values
  - paper: "Yu Sasaki and Kazumaro Aoki, Finding preimages in full MD5 faster than exhaustive search, EUROCRYPT 2009, LNCS 5479, pages 134 to 152"
    locator: the splice-and-cut meet in the middle, partial matching and the preimage attack on MD5 at about 2^123.4
  - paper: "Xuejia Lai and James L. Massey, Hash functions based on block ciphers, EUROCRYPT 1992, LNCS 658, pages 55 to 70"
    locator: the conversion of a pseudo-preimage attack in 2^p into a preimage attack in about 2^((n+p)/2+1), and the attacks on schemes with no feed-forward
  - paper: "Phillip Rogaway and Thomas Shrimpton, Cryptographic hash-function basics, FSE 2004, LNCS 3017, pages 371 to 388"
    locator: Theorem 7, a second preimage or collision finder from a preimage finder when the hash compresses
  - paper: "Lov K. Grover, A fast quantum mechanical algorithm for database search, STOC 1996, pages 212 to 219"
    locator: the quantum search that inverts an n-bit function with about 2^(n/2) queries
  - paper: doi:10.1109/TIT.1980.1056220
    title: Martin E. Hellman, A cryptanalytic time-memory trade-off, IEEE Transactions on Information Theory 26(4), 1980, pages 401 to 406
    locator: inverting one fixed function many times with precomputed tables
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 9.7.1 (attacks on hash functions) and Section 9.4.1 (hash functions based on block ciphers)
---

Preimage finding is the problem of inverting a hash function: given a digest $y$, find any input $x$ with $H(x) = y$. A hash where this is hard for random targets is [preimage resistant](/preimage-resistance/), or one-way. For a random function with $n$-bit output, nothing beats trying inputs, which takes about $2^n$ calls, and a quantum computer needs about $2^{n/2}$. Structure can lower the cost. When the compression function of an iterated hash can be run backwards, a meet in the middle attack finds a two-block preimage with about $2^{n/2+1}$ calls. This is why designs add a feed-forward, as in Davies-Meyer. The best attacks on real hashes refine this meet in the middle: Leurent (2008) inverted MD4 in about $2^{102}$, and Sasaki and Aoki (2009) inverted MD5 in about $2^{123.4}$. Both remain far from practical.

## In plain words

You are given a fingerprint and asked for any message that has it. You did not see the original message, and any message with that fingerprint will do.

For a good hash the only way is to guess. With fingerprints of $n$ bits you need about $2^n$ guesses, which is far too many for $n = 256$.

If the hash can be run backwards one step, you can start from both ends. Go forward from the start with many first blocks, go backward from the fingerprint with many last blocks, and look for a meeting point in the middle. That needs only about the square root of the guesses.

## Definition

**Input.** A function $H : D \to \{0,1\}^n$, as an oracle or as code, and a target $y \in \{0,1\}^n$. In the standard game $y = H(x)$ for a uniform $x$ of some length, so a preimage exists. Some definitions take $y$ uniform in $\{0,1\}^n$ instead.

**Output.** Any $x' \in D$ with $H(x') = y$. It may equal the original $x$.

**Measure.** Calls of $H$ or of its compression function, memory, and the success probability.

**How it differs from its neighbours.** In [second-preimage finding](/second-preimage-finding/), the original message is given and the answer must differ from it. In [collision finding](/collision-finding/), no target is given at all. Preimage finding is the problem with the least help for the attacker.

## Variants

- **Pseudo-preimage.** For an iterated hash, find a chaining value $h$ and a message $m$ with $f^*(h, m) = y$, where $h$ is free instead of the fixed $IV$. Lai and Massey showed that a pseudo-preimage attack in $2^p$ gives a preimage attack in about $2^{(n+p)/2+1}$, by a meet in the middle between pseudo-preimages and forward states.
- **Multi-target.** Given $t$ digests, invert any one of them. Brute force then costs $2^n/t$. This is the case of a leaked database of unsalted password hashes.
- **Many targets of one function.** Given many digests over time, invert each. Precomputed [time-memory tradeoff](/time-memory-tradeoff/) tables reach $T M^2 = N^2$ after a one-time cost of $N$.
- **Partial preimage.** Find $x$ such that $H(x)$ has $d$ given bits, for example $d$ leading zeros. The generic cost is $2^d$. This is the puzzle of [proof of work](/proof-of-work/).
- **Low-entropy inputs.** If $x$ comes from a small set, such as passwords or PINs, the attacker enumerates the set. Preimage resistance says nothing about this case. Slow, salted [password hashing](/password-hashing/) is the defense.
- **Quantum.** Grover search inverts any $n$-bit function with about $2^{n/2}$ quantum calls, and this is optimal for a random oracle.

## Examples

**Brute force on 16 bits.** The page's code uses a toy two-block hash $H(m_1, m_2) = g(g(IV, m_1), m_2)$ with an $n$-bit state and $g(h, m) = E_m(h)$, where $E$ is a small invertible mixer keyed by a 32-bit block. With $n = 16$, the target is the digest `0xec5` of the message `(0xcafe, 0xbeef)`. Random messages found the preimage `(0xe51eede1, 0x612fa2b5)` after 53523 tries (107046 calls of $E$). The expected count is $2^{16} = 65536$ tries. The preimage is not the original message, and it does not need to be.

**Meet in the middle on 32 bits.** Since $g$ has no feed-forward, anyone can run it backwards: $h = E_{m_2}^{-1}(y)$. So:

1. Store $g(IV, m_1)$ for $2^{16}$ random $m_1$.
2. For random $m_2$, compute $E_{m_2}^{-1}(y)$ and look it up.
3. A match gives $g(g(IV, m_1), m_2) = y$.

For the 32-bit digest `0x2846e4a4` of `(0x01234567, 0x89abcdef)`, the attack stored 65536 states and found the preimage `(0x65750890, 0x5fb33706)` after 177518 calls of $E$ in total. Brute force would need about $2^{32} \approx 4.3 \cdot 10^9$ tries. On 24 bits, over 20 random targets, the mean was 8433 calls, against the model $2^{12} + 2^{12} = 8192$.

**Feed-forward stops it.** With the Davies-Meyer form $g(h, m) = E_m(h) \oplus h$, the backward step would need to solve $E_m(h) \oplus h = y$ for $h$, which is as hard as a preimage of $g$. The code refuses to run the attack in that mode, and the test checks it. Real attacks on Davies-Meyer hashes such as MD4 and MD5 need much more work, below.

The code is for study only and not constant time, and the hash is a toy. For real hashing use SHA-256 or SHA-3 from the standard library, a FIPS 140 validated module, or libsodium.

## Known algorithms

| Algorithm | Cost | Applies to |
|---|---|---|
| brute force | about $2^n$ calls, $O(1)$ memory | any hash |
| brute force, $t$ targets | about $2^n/t$ | any hash |
| time-memory tradeoff | $N$ once, then $T = M = N^{2/3}$ per target | one fixed function, many targets |
| Grover search | about $2^{n/2}$ quantum calls | any hash |
| meet in the middle | about $2^{n/2+1}$ calls and $2^{n/2}$ memory | compression functions that can be inverted, with no feed-forward |
| pseudo-preimage conversion (Lai and Massey) | $2^{(n+p)/2+1}$ from a $2^p$ pseudo-preimage | iterated hashes |
| Leurent's attack on MD4 | about $2^{102}$ | full MD4 ($n = 128$) |
| Sasaki and Aoki on MD5 | about $2^{123.4}$ | full MD5 ($n = 128$) |

**The splice-and-cut method.** Sasaki and Aoki split the 64 steps of the MD5 compression function into two chunks, each of which depends on some message words that the other does not use. They compute one chunk forward and the other backward from the target, through the feed-forward by treating the first and last steps as neighbours, and match the two in the middle on a few bits at a time (partial matching). This gives a pseudo-preimage attack faster than $2^{128}$, which the Lai and Massey conversion makes into a preimage attack. Later work on SHA-1 and SHA-2 uses the same method with bicliques, but only for reduced numbers of rounds.

**Status of real hashes.** No preimage attack faster than brute force is known for full SHA-1, SHA-2, SHA-3 or BLAKE2. For MD5 and MD4 the attacks are theoretical. Both are still broken for collisions, which is the reason not to use them.

## Bounds

- **Generic lower bound.** For a random oracle, $q$ queries find a preimage of a random target with probability at most $q/2^n$, plus a small term for the case where the target has many preimages. So $\Omega(2^n)$ queries are needed.
- **Generic upper bound.** Brute force succeeds with probability about $1 - e^{-q/2^n}$ after $q$ tries.
- **Quantum.** $\Theta(2^{n/2})$ quantum queries, by Grover search and the matching lower bound of Bennett, Bernstein, Brassard and Vazirani.
- **With precomputation.** Hellman's tradeoff, with advice of $M$ words, inverts a random function in time $T$ with $T M^2 \approx N^2$. Lower bounds for this setting are on the [time-memory tradeoff](/time-memory-tradeoff/) page.

## Reductions

- **Preimages give second preimages and collisions.** For a hash that compresses, a preimage finder applied to $H(x)$ for a random $x$ returns a different message with good probability. Rogaway and Shrimpton make this exact in Theorem 7 of their paper. So collision resistance implies preimage resistance for such hashes, up to the amount of compression.
- **The other direction fails.** A collision finder gives no preimages: the identity map on $\{0,1\}^n$ has no collisions but is trivial to invert, and the [birthday attack](/birthday-attack/) gives nothing for a fixed target.
- **From the compression function.** A preimage attack on the compression function with the fixed $IV$ gives a preimage of the full hash. A pseudo-preimage attack, with a free chaining value, gives one too, at the cost of the Lai and Massey conversion.

## Applications

- **One-wayness.** Commitments $H(r \,\|\, m)$, hash-based signatures such as [Lamport](/lamport-signature/) and [SPHINCS+](/sphincs-plus/), and key derivation all rely on preimage resistance, usually for uniform inputs.
- **Passwords.** Recovering a password from its unsalted hash is a preimage search over a small set, not over $2^n$ values. Salts defeat precomputed tables, and slow functions such as bcrypt, scrypt and Argon2 raise the cost per guess.
- **Choosing $n$.** Since quantum search halves the exponent, a 256-bit hash keeps about 128 bits of preimage security against quantum attacks.

## References
