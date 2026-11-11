---
tag: VMZSV3
kind: definition
slug: compression-function
name: Compression function
aliases:
- fixed-input-length hash
area: cryptography/hash-functions
level: core
summary: A function from a chaining value and a fixed-size message block to a new chaining value. Iterated hash functions apply it once per block.
prereqs: [cryptographic-hash-function, collision-resistance]
see_also: [merkle-damgard-construction, merkle-damgard-theorem, davies-meyer-construction, miyaguchi-preneel-construction, sponge-construction, block-cipher, ideal-cipher-model, nmac]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 9, Section 9.3.1 (the general iterated model and Fact 9.24), Section 9.4.1 (Algorithms 9.41 to 9.43) and Section 9.7.2 (Table 9.11, Definition 9.97, Note 9.98 and Fact 9.99)
  - paper: "Bart Preneel, René Govaerts and Joos Vandewalle, Hash functions based on block ciphers, a synthetic approach, Advances in Cryptology, CRYPTO 1993, LNCS 773, Springer, 1994"
    locator: the 64 schemes of the form E_a(b) XOR c and the 12 schemes the authors regard as secure
  - paper: "John Black, Phillip Rogaway and Thomas Shrimpton, Black-box analysis of the block-cipher-based hash-function constructions from PGV, Advances in Cryptology, CRYPTO 2002, LNCS 2442, Springer, 2002"
    locator: full version of May 31, 2002, Definition 2.2, Lemma 3.2, Lemma 3.3, Theorems 3.1, 4.1, 6.1 and 6.4, and Figure 1
  - paper: "Ralph C. Merkle, One way hash functions and DES, Advances in Cryptology, CRYPTO 1989, LNCS 435, Springer, 1990"
    locator: the iteration of a fixed-size function with the length in the last block
  - paper: "Ivan B. Damgård, A design principle for hash functions, Advances in Cryptology, CRYPTO 1989, LNCS 435, Springer, 1990"
    locator: the proof that a collision-free function on fixed-size inputs gives a collision-free function on inputs of any length
  - paper: "Bert den Boer and Antoon Bosselaers, Collisions for the compression function of MD5, Advances in Cryptology, EUROCRYPT 1993, LNCS 765, Springer, 1994"
    locator: one message block and two chaining values that differ in the top bit of each word, with the same output
  - paper: "Marc Stevens, Pierre Karpman and Thomas Peyrin, Freestart collision for full SHA-1, Advances in Cryptology, EUROCRYPT 2016, LNCS 9665, Springer, 2016"
    locator: a collision of the full 80-step SHA-1 compression function with a chosen chaining value
  - paper: "Mihir Bellare, New proofs for NMAC and HMAC, security without collision-resistance, Advances in Cryptology, CRYPTO 2006, LNCS 4117, Springer, 2006"
    locator: NMAC and HMAC are PRFs if the compression function, keyed by its chaining value, is a PRF
  - paper: doi:10.6028/NIST.FIPS.180-4
    title: NIST, FIPS 180-4, Secure Hash Standard (SHS), August 2015
    locator: Section 6.2.2, the SHA-256 hash computation, whose steps 1 to 4 for one block are the SHA-256 compression function
---

A compression function is a function $f$ that takes two inputs of fixed size, a chaining value $h$ of $n$ bits and a message block $m$ of $b$ bits, and returns a new chaining value of $n$ bits. Because it maps $n + b$ bits to $n$ bits, it compresses. A hash function for messages of any length is built by running $f$ once per block, with the output of one call as the chaining input of the next. This is the [Merkle-Damgard construction](/merkle-damgard-construction/), and MD5, SHA-1 and SHA-2 are all built this way. Most of the security of such a hash function is a property of $f$, so $f$ is the part that designers build and that attackers study.

**Notation.** $n$ is the chaining length and the output length, $b$ is the block length. $IV$ is a fixed initial chaining value. $q$ is the number of queries an adversary makes to $f$, or to a block cipher $E$ in the [ideal cipher model](/ideal-cipher-model/). $E_k(x)$ is the encryption of $x$ under the key $k$. All the numbers in the examples below were computed by a short script, and the SHA-256 values were checked against `hashlib.sha256`.

## Definition

A **compression function** is a function

$$f : \{0,1\}^n \times \{0,1\}^b \to \{0,1\}^n,$$

with $b \ge 1$. The first input is the **chaining value**, and the second is the **message block**. A function with these input and output sizes is also called a fixed-input-length hash function, since it is defined only on inputs of exactly $n + b$ bits.

**Iteration.** For a message that was padded to blocks $m_1, \ldots, m_\ell$, the iterated hash is

$$H_0 = IV, \qquad H_i = f(H_{i-1}, m_i) \text{ for } i = 1, \ldots, \ell, \qquad \mathrm{Hash}(M) = g(H_\ell),$$

where $g$ is the identity or a final transform, for example a truncation. HAC calls this the general model for iterated hash functions (Section 9.3.1). The padding rule is part of the hash function, not of $f$; with MD strengthening, the last block holds the message length.

### Security notions

The notions below are the ones for a hash function, applied to $f$. The difference is how much the attacker controls the chaining input. HAC Table 9.11 and Definition 9.97 give the same list.

| notion | the attacker must find | generic cost |
| --- | --- | --- |
| collision for the fixed $IV$ | $m \ne m'$ with $f(IV, m) = f(IV, m')$ | $2^{n/2}$ |
| semi-free-start collision | $h$ and $m \ne m'$ with $f(h, m) = f(h, m')$ | $2^{n/2}$ |
| free-start collision (pseudo-collision) | $(h, m) \ne (h', m')$ with $f(h, m) = f(h', m')$ | $2^{n/2}$ |
| near-collision | two inputs whose outputs differ in only a few bits | less than $2^{n/2}$, depends on the number of bits |
| preimage | for a given $y$, an $m$ with $f(IV, m) = y$ | $2^n$ |
| pseudo-preimage | for a given $y$, any $(h, m)$ with $f(h, m) = y$ | $2^n$ |
| second preimage | for a given $(h, m)$, a different input with the same output | $2^n$ |

The generic cost is the cost of an attack that works for every $f$: a [birthday attack](/birthday-attack/) for collisions, and trial of random inputs for preimages. For a random function $f$, no attack does much better, so a compression function is said to be broken when an attack on it costs less.

**The notion that the Merkle-Damgard theorem uses** is the strongest one in the table: $f$ is collision resistant if it is hard to find any $(h, m) \ne (h', m')$ with $f(h, m) = f(h', m')$. The chaining values are free. The [Merkle-Damgard theorem](/merkle-damgard-theorem/) says that, with MD strengthening, a collision of the hash gives such a collision of $f$. So a free-start collision of $f$ does not break the hash function, but it removes the proof of its security.

Black, Rogaway and Shrimpton (2002, Definition 2.2) state this for a function $f^E$ that calls a block cipher $E$. They fix a constant $h_0$, and the advantage of $\mathcal{A}$ is the probability that it outputs $(h, m) \ne (h', m')$ with $f^E(h, m) = f^E(h', m')$, or a pair $(h, m)$ with $f^E(h, m) = h_0$. The second event is also counted, because a block that maps to the initial value gives a collision with the empty message when no length is encoded.

**Keyed use.** In [NMAC](/nmac/) and HMAC the chaining value is a secret key. The notion there is that $f(K, \cdot)$, for a uniform secret $K$, is a [pseudorandom function](/pseudorandom-function/) of the block. Bellare (2006) proved NMAC and HMAC secure under this assumption alone, without collision resistance.

### Iteration and the security of the hash

Three facts connect $f$ and the iterated hash. They hold with MD strengthening.

1. **Collisions.** A collision of the hash gives a collision of $f$ (HAC Fact 9.24, and Lemma 3.2 of Black, Rogaway and Shrimpton). The proof is on the [Merkle-Damgard theorem](/merkle-damgard-theorem/) page.
2. **Inversion.** In the ideal cipher setting of Black, Rogaway and Shrimpton (Lemma 6.2), an inverse of the hash at a random point gives an inverse of $f$.
3. **The other direction.** An attack on $f$ with the fixed $IV$ is also an attack on the hash. For example, if $f(IV, m_1') = f(IV, m_1)$ with $m_1' \ne m_1$, then $m_1' m_2 \ldots m_t$ is a second preimage of $m_1 m_2 \ldots m_t$ (HAC Note 9.98). Also, if pseudo-preimages of $f$ cost $2^s$ with $s < n$, a meet-in-the-middle attack finds preimages of the hash in about $2 \cdot 2^{(n+s)/2}$ operations, even with MD strengthening (HAC Fact 9.99).

So a compression function that is collision resistant in the strong sense is enough for a collision resistant hash. It is not enough for all the other properties: the iterated hash still has [length extension](/length-extension-attack/), [multicollisions](/multicollision-attack/) and long-message second preimages, which a random function does not have.

### Compression functions from block ciphers

A [block cipher](/block-cipher/) $E : \{0,1\}^n \times \{0,1\}^n \to \{0,1\}^n$ is a family of permutations, so it does not compress by itself. A feed-forward XOR makes it a compression function with $b = n$. Preneel, Govaerts and Vandewalle (1993) looked at all 64 schemes of the form

$$f(h, m) = E_a(x) \oplus c, \qquad a, x, c \in \{h, m, h \oplus m, v\},$$

with $v$ a constant. They regarded 12 of them as secure. Black, Rogaway and Shrimpton (2002) proved bounds for all 64 in the ideal cipher model, where the adversary may query $E$ and $E^{-1}$:

| group | schemes | collision bound | inversion bound |
| --- | --- | --- | --- |
| group 1 | 12 (the 12 of PGV) | $q(q+1)/2^n$ for $f$ and for the hash (Lemma 3.3, Theorem 3.1) | $q/2^{n-1}$ (Theorem 6.1) |
| group 2 | 8 more | $3q(q+1)/2^n$ for the hash only (Theorem 4.1) | $9(q+3)^2/2^n$ (Theorem 6.4) |
| group 3 | the other 44 | constant: a collision with a few queries | constant |

For group 2, $f$ itself is not collision resistant, but the iterated hash with a fixed $IV$ is. This was a new result: these 8 schemes cannot be proved secure by the Merkle-Damgard route, but they are secure all the same. So 20 of the 64 schemes give a collision resistant hash function. The three group-1 schemes in common use are:

- [Davies-Meyer](/davies-meyer-construction/): $f(h, m) = E_m(h) \oplus h$, scheme $f_5$ (HAC Algorithm 9.42).
- Matyas-Meyer-Oseas: $f(h, m) = E_{g(h)}(m) \oplus m$, scheme $f_1$ (HAC Algorithm 9.41).
- [Miyaguchi-Preneel](/miyaguchi-preneel-construction/): $f(h, m) = E_{g(h)}(m) \oplus m \oplus h$, scheme $f_3$ (HAC Algorithm 9.43).

Here $g$ maps the chaining value to a key. The bounds are tight up to a constant: Figure 1 of the paper also gives attacks with success about $q^2/2^n$ for collisions.

A dedicated compression function is a block cipher in Davies-Meyer form that was designed for hashing only. In MD4, MD5, SHA-1 and SHA-2, the message block is the key of an internal cipher, and the feed-forward is addition modulo $2^{32}$ or $2^{64}$ word by word.

## Examples and non-examples

**Example: the SHA-256 compression function.** Here $n = 256$ and $b = 512$, so $f$ maps 768 bits to 256 bits. It is $f(H, Y) = E_Y(H) + H$ word by word, where $E$ is the 64-round cipher inside SHA-256 (see the [SHA-2](/sha-2/) page). The message "abc" pads to a single block $Y$, so its digest is one call of $f$:

$$f(IV, Y) = \texttt{ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad} = \mathrm{SHA\text{-}256}(\texttt{abc}).$$

**Example: a fixed point that costs nothing.** In the Davies-Meyer form, $f(h, m) = h$ exactly when $E_m(h) = 0$, so $h = E_m^{-1}(0)$ is a fixed point for any block $m$. For SHA-256 and the all-zero block $m = 0^{512}$, running the 64 rounds backward from the zero state gives

$$h^* = \texttt{f8c9259fa4f5d787b570afa9219166a63636fc5c30ac289155d0cc4ffcb4b03d}, \qquad f(h^*, 0^{512}) = h^*.$$

For a random function, finding a fixed point takes about $2^{256}$ trials. So the SHA-256 compression function is easy to tell from a random function. This does not break SHA-256, because the attacker does not control the chaining value after the fixed $IV$, but it shows that "the compression function is ideal" is a false assumption for SHA-256. Dean (1999) and Kelsey and Schneier (2005) used such fixed points for second preimages of long messages. See [Davies-Meyer](/davies-meyer-construction/).

**Example: a pseudo-collision of MD5.** Den Boer and Bosselaers (1993) found one message block $m$ and two chaining values $h \ne h'$ with $f(h, m) = f(h', m)$, where $h$ and $h'$ differ only in the top bit of each of the four words. This is a free-start collision. It did not give collisions of MD5 with its fixed $IV$, but it removed the Merkle-Damgard proof for MD5. Full collisions followed in 2004 (see [MD5](/md5/)).

**Example: a free-start collision of SHA-1.** Stevens, Karpman and Peyrin (2016) found a collision of the full SHA-1 compression function with a chaining value of their choice. The first collision of SHA-1 itself followed in 2017 (see [SHA-1](/sha-1/)).

**Non-example: a block cipher with no feed-forward.** $f(h, m) = E_m(h)$ has the right sizes, but the attacker can invert it: for any target $y$ and any block $m$, $h = E_m^{-1}(y)$ is a pseudo-preimage. With the key on the other side, $f(h, m) = E_h(m)$, a collision costs two decryptions: pick $h \ne h'$ and take $m = E_h^{-1}(y)$ and $m' = E_{h'}^{-1}(y)$. This is scheme 2 of Figure 1 of Black, Rogaway and Shrimpton, in group 3.

**Non-example: a linear function.** $f(h, m) = h \oplus m$ with $b = n$ is a compression function in the sense of the sizes, but $f(h, m) = f(h \oplus d, m \oplus d)$ for every $d$, so collisions are free.

**Non-example: Keccak-f.** The permutation [Keccak](/keccak/)-f[1600] maps 1600 bits to 1600 bits, so it does not compress. SHA-3 does not use a compression function at all: it uses the permutation in the [sponge construction](/sponge-construction/), which keeps part of the state secret instead of compressing.

## Related definitions

- **[Cryptographic hash function](/cryptographic-hash-function/).** The function on messages of any length that the iteration builds from $f$.
- **[Collision resistance](/collision-resistance/), [preimage resistance](/preimage-resistance/) and [second-preimage resistance](/second-preimage-resistance/).** The three main notions, defined for hash functions and applied to $f$ above.
- **[Merkle-Damgard construction](/merkle-damgard-construction/).** The iteration with MD strengthening.
- **[Merkle-Damgard theorem](/merkle-damgard-theorem/).** A collision resistant $f$ gives a collision resistant hash.
- **[Ideal cipher model](/ideal-cipher-model/).** The model in which the bounds of Black, Rogaway and Shrimpton hold.
- **[Indifferentiability](/indifferentiability-framework/).** The notion that says when the iterated hash behaves like a [random oracle](/random-oracle-model/), if $f$ is ideal. Plain Merkle-Damgard does not.
- **[Sponge construction](/sponge-construction/).** An iteration that uses a permutation, not a compression function.
- **[Pseudorandom function](/pseudorandom-function/).** The notion for $f$ keyed by its chaining value, used for [NMAC](/nmac/) and [HMAC](/hmac/).

## References
