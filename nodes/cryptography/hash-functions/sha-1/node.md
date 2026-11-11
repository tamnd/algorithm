---
tag: THSRT9
kind: algorithm
slug: sha-1
name: SHA-1
aliases:
- Secure Hash Algorithm 1
area: cryptography/hash-functions
level: core
summary: The 160-bit NIST hash of FIPS 180-1 (1995), 80 steps on five 32-bit words. Collisions since 2017 (SHAttered) and chosen-prefix since 2020; NIST retires it by 2030.
model: word-ram
complexity:
  vars: {n: the message length in bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 1995
  people: [National Security Agency, NIST]
  note: The NSA designed SHA-0 (FIPS 180, 1993) and SHA-1 (FIPS 180-1, 1995), which adds one rotation to the message schedule. The first SHA-1 collision was published in 2017.
prereqs: [merkle-damgard-construction, davies-meyer-construction]
see_also: [md5, sha-2, sha-3, chosen-prefix-collision, collision-finding, collision-resistance, length-extension-attack, hmac]
sources:
  - paper: doi:10.6028/NIST.FIPS.180-4
    title: NIST, FIPS 180-4, Secure Hash Standard (SHS), August 2015
    locator: Section 4.1.1 (the functions), Section 4.2.1 (the constants), Section 5.1.1 (padding), Section 5.3.1 (initial hash value) and Section 6.1 (SHA-1 preprocessing and hash computation)
  - url: "https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/SHA1.pdf"
    title: NIST, Cryptographic Standards and Guidelines, Examples with Intermediate Values, SHA-1
    locator: the one-block message "abc" with the registers after each step, and the two-block 448-bit message
  - paper: "Xiaoyun Wang, Yiqun Lisa Yin and Hongbo Yu, Finding collisions in the full SHA-1, Advances in Cryptology, CRYPTO 2005, LNCS 3621, Springer, 2005"
    locator: the first collision attack on the full SHA-1, in about 2^69 operations
  - paper: "Marc Stevens, Elie Bursztein, Pierre Karpman, Ange Albertini and Yarik Markov, The first collision for full SHA-1, Advances in Cryptology, CRYPTO 2017, LNCS 10401, Springer, 2017"
    locator: the SHAttered collision, about 2^63.1 SHA-1 computations, and the two colliding PDF files
  - paper: "Gaëtan Leurent and Thomas Peyrin, SHA-1 is a Shambles: first chosen-prefix collision on SHA-1 and application to the PGP web of trust, 29th USENIX Security Symposium, 2020"
    locator: the first chosen-prefix collision of SHA-1, about 2^63.4 SHA-1 computations, and the PGP key impersonation
  - url: "https://www.nist.gov/news-events/news/2022/12/nist-retires-sha-1-cryptographic-algorithm"
    title: NIST, NIST Retires SHA-1 Cryptographic Algorithm, news release, December 15, 2022
    locator: SHA-1 should be phased out by December 31, 2030
  - url: "https://shattered.io/"
    title: Stevens, Bursztein, Karpman, Albertini and Markov, SHAttered, 2017
    locator: the files shattered-1.pdf and shattered-2.pdf and their common SHA-1 digest
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 9.4.2, Algorithm 9.53 (SHA-1) and Remark 9.54
---

SHA-1 is the 160-bit [cryptographic hash function](/cryptographic-hash-function/) of the NIST Secure Hash Standard. The NSA designed it in the [MD4](/md4/) style: a [Merkle-Damgard](/merkle-damgard-construction/) hash over a compression function of 80 steps on five 32-bit registers, with a linear message schedule that expands each block of 16 words to 80. From 1995 to about 2015 it signed most certificates, software updates and version control objects. It is broken for [collision resistance](/collision-resistance/). Stevens et al. published the first collision (SHAttered) in 2017, after about $2^{63.1}$ SHA-1 computations. Leurent and Peyrin published a [chosen-prefix collision](/chosen-prefix-collision/) (Shambles) in 2020, after about $2^{63.4}$. NIST said in December 2022 that SHA-1 should be phased out by December 31, 2030.

**Notation.** Words have 32 bits. $+$ is addition modulo $2^{32}$, $\mathrm{ROTL}^s$ is left rotation by $s$, and $\wedge$, $\oplus$, $\neg$ are bitwise operations. Words are big-endian. $(H_0, \ldots, H_4)$ is the chaining value, $W_0, \ldots, W_{79}$ the expanded block. $n$ is the message length in bytes.

## In plain words

SHA-1 is a close relative of MD4 and MD5. It pads the message to whole blocks of 64 bytes, with the length at the end. Its state is five 32-bit numbers that start at fixed values. For each block, it first stretches the 16 words of the block to 80 words: each new word is the XOR of four earlier words, rotated by one bit. Then it runs 80 steps. Each step makes a new number from a rotated copy of the first number, a mix of three others, the fifth number, a constant and one of the 80 words, and shifts the five numbers down by one place. After the 80 steps it adds the old state. The last state is the 20-byte digest.

## The problem

The input is a message $M$ of $8n$ bits with $8n < 2^{64}$. The output is a 160-bit digest. The goal was collision resistance at $2^{80}$ and preimage resistance at $2^{160}$. FIPS 202, Table 4 lists the collision strength of SHA-1 as "< 80" bits.

## The algorithm

The step functions are $\mathrm{Ch}(x, y, z) = (x \wedge y) \oplus (\neg x \wedge z)$ for steps 0 to 19, $\mathrm{Parity}(x, y, z) = x \oplus y \oplus z$ for steps 20 to 39 and 60 to 79, and $\mathrm{Maj}(x, y, z) = (x \wedge y) \oplus (x \wedge z) \oplus (y \wedge z)$ for steps 40 to 59. The constants are $K = \texttt{5A827999}$, $\texttt{6ED9EBA1}$, $\texttt{8F1BBCDC}$ and $\texttt{CA62C1D6}$ for the four groups of 20 steps; they are $\lfloor 2^{30} \sqrt{v} \rfloor$ for $v = 2, 3, 5, 10$. The IV is $\texttt{67452301}$, $\texttt{EFCDAB89}$, $\texttt{98BADCFE}$, $\texttt{10325476}$, $\texttt{C3D2E1F0}$.

```pseudo id=main
SHA-1(M)
L1  P ← M ‖ 1 ‖ 0^k ‖ [8n]_64            ▷ |P| ≡ 0 mod 512; length big-endian
L2  H ← IV
L3  for each 512-bit block Y of P, in order, do
L4      H ← COMPRESS(H, Y)
L11 return H0 ‖ H1 ‖ H2 ‖ H3 ‖ H4         ▷ big-endian words

COMPRESS(H, Y)
L5  W[0..15] ← the words of Y; for t ← 16 to 79: W[t] ← ROTL¹(W[t−3] ⊕ W[t−8] ⊕ W[t−14] ⊕ W[t−16])
L6  (a, b, c, d, e) ← (H0, H1, H2, H3, H4)
L7  for t ← 0 to 79 do
L8      T ← ROTL⁵(a) + f_t(b, c, d) + e + K_t + W[t]
L9      (a, b, c, d, e) ← (T, a, ROTL³⁰(b), c, d)
L10 return (H0 + a, H1 + b, H2 + c, H3 + d, H4 + e)
```

The message schedule of line L5 is linear over GF(2). SHA-0 had the same schedule without the rotation $\mathrm{ROTL}^1$; that rotation is the only change from SHA-0 to SHA-1, and it was added after the NSA found a weakness that it did not publish. Each step changes only $a$ and $c$; the other registers move down one place.

## Example

Hash `abc`. The padded block has $W_0 = \texttt{61626380}$, $W_{15} = \texttt{00000018}$ and zeros between. The schedule gives $W_{16} = \mathrm{ROTL}^1(W_{13} \oplus W_8 \oplus W_2 \oplus W_0) = \mathrm{ROTL}^1(\texttt{61626380}) = \texttt{C2C4C700}$. The registers after some steps are:

| after step $t$ | $a$ | $b$ | $c$ | $d$ | $e$ |
|---|---|---|---|---|---|
| 0 | `0116FC33` | `67452301` | `7BF36AE2` | `98BADCFE` | `10325476` |
| 1 | `8990536D` | `0116FC33` | `59D148C0` | `7BF36AE2` | `98BADCFE` |
| 2 | `A1390F08` | `8990536D` | `C045BF0C` | `59D148C0` | `7BF36AE2` |
| 19 | `FD9E1D7D` | `DC64901D` | `20AA99CA` | `D3A49608` | `C82F758B` |
| 39 | `32DE1CBA` | `4C986405` | `F718E5CF` | `03D447F6` | `F72EEC32` |
| 59 | `3F52DE5A` | `09D785FD` | `3498BFD4` | `F211824F` | `D79915AB` |
| 79 | `42541B35` | `5738D5E1` | `21834873` | `681E6DF6` | `D8FDF6AD` |

After step 0, $c = \mathrm{ROTL}^{30}(\texttt{EFCDAB89}) = \texttt{7BF36AE2}$. Adding the IV to the step 79 row gives the digest `a9993e364706816aba3e25717850c26c9cd0d89d`. The NIST example for "abc" lists the same registers; the tests check steps 0 and 1, the digest, and the two-block example `84983e441c3bd26ebaae4aa1f95129e5e54670f1` of the 448-bit message "abcdbcde...nopq".

**The SHAttered collision.** The two PDF files of SHAttered start with the same 192 bytes. Bytes 192 to 319 (two blocks) differ. After these 320 bytes, the SHA-1 chaining values are equal, and the rest of the two files is the same. The tests embed only the first 320 bytes of each file (no download). Both prefixes, hashed as messages, give `f92d74e3874587aaf443d1db961d4e26dde13e9c`, and a common suffix keeps the collision. The full files have the SHA-1 digest `38762cf7f55934b34d179ae6a4c80cadccbb7f0a`, as published on shattered.io, while their SHA-256 digests differ.

## Correctness

The padding of line L1 is injective and gives whole blocks, and the loop computes the Merkle-Damgard iteration. Each step of lines L8 and L9 is a bijection of the five registers for fixed $W[t]$: the output gives $a$, $b$ (by rotating back by 30), $c$ and $d$, and then $e = T - \mathrm{ROTL}^5(a) - f_t(b, c, d) - K_t - W[t]$. So COMPRESS is the [Davies-Meyer](/davies-meyer-construction/) form $E_Y(H) + H$ with the 80 steps as a cipher keyed by the block. This cipher is SHACAL-1, which was proposed to NESSIE as a block cipher. The full proof is below.

## Complexity

The schedule takes 64 XOR and rotate operations, and each of the 80 steps about 4 additions, 2 rotations and a step function. The cost per block is a constant, the number of blocks is $\lfloor (n + 8)/64 \rfloor + 1$, so the time is $\Theta(n)$ and the extra space $\Theta(1)$ (the 80-word schedule can be kept as a ring of 16 words). Many x86 and ARM processors have SHA-1 instructions.

## Properties

- 160-bit digest, 512-bit block, big-endian words.
- Generic bounds: collisions in about $2^{80}$ by the [birthday attack](/birthday-attack/), preimages in $2^{160}$. Real attacks: collisions in about $2^{63.1}$ (Stevens et al. 2017), chosen-prefix collisions in about $2^{63.4}$ (Leurent and Peyrin 2020). No practical preimage attack is known.
- [Length extension](/length-extension-attack/) works, as for each plain Merkle-Damgard hash.
- HMAC-SHA-1 does not need collision resistance and has no known practical attack, but it should also be replaced in new designs.

## Variants and improvements

- SHA-0 (FIPS 180, 1993) lacks the rotation in the schedule. Joux, Carribault, Lemuet and Jalby found a full SHA-0 collision in 2004.
- [SHA-2](/sha-2/) (2001) uses a non-linear schedule, more registers and 64 or 80 steps. No practical attack on it is known.
- Hardened SHA-1 with collision detection (Stevens and Shumow 2017) gives the normal digest for normal input and a different one for input that shows the signs of the known attacks. Git uses it, and it also supports SHA-256 repositories.

## When to use it

Do not use SHA-1 for new designs. Do not accept SHA-1 signatures on certificates or code. Browsers and CAs stopped trusting SHA-1 certificates in 2017. HMAC-SHA-1 and old protocols that need SHA-1 for interoperability may run until the NIST transition date of December 31, 2030. Use [SHA-256](/sha-2/), SHA-512/256 or [SHA3-256](/sha-3/) instead.

## Pitfalls

- A collision with a shared prefix and a shared suffix is enough to make two different documents with one signature, as SHAttered shows with PDF files.
- The rotation in line L5 is easy to forget. Without it, the function is SHA-0, and the NIST vectors fail.
- Words are big-endian, unlike MD5. The length field is big-endian too.
- The code on this page is for study only. It is not constant time, and it must not protect real data. Use `hashlib.sha256` or a FIPS 140 validated module.

## Implementations

## History

NIST published the Secure Hash Standard with SHA, now called SHA-0, in FIPS 180 in 1993. In 1995, FIPS 180-1 replaced it with SHA-1, which adds a one-bit rotation to the message schedule. Chabaud and Joux found a theoretical collision attack on SHA-0 in 1998. In 2005, Wang, Yin and Yu gave a collision attack on SHA-1 in about $2^{69}$ operations, and NIST began the move to SHA-2. Stevens, Bursztein, Karpman, Albertini and Markov published the first SHA-1 collision in February 2017 (CRYPTO 2017); it took about $2^{63.1}$ SHA-1 computations, about 6500 CPU years and 110 GPU years. Leurent and Peyrin published a chosen-prefix collision in January 2020 (USENIX Security 2020) and used it to make two PGP keys with the same SHA-1 certification signature. On December 15, 2022, NIST announced that SHA-1 should be phased out by December 31, 2030.

## References
