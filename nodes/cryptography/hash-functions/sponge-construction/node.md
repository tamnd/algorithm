---
tag: 12K42P
kind: technique
slug: sponge-construction
name: Sponge construction
aliases:
- sponge function
area: cryptography/hash-functions
level: advanced
summary: "A mode that builds a hash or XOF from a fixed permutation on r + c bits: absorb the padded input r bits at a time, then squeeze r bits per call. Generic security 2^(c/2); used by SHA-3."
prereqs: [cryptographic-hash-function, collision-resistance]
see_also: [keccak, sha-3, shake, extendable-output-function, indifferentiability-framework, merkle-damgard-construction, length-extension-attack, kmac]
sources:
  - paper: "Guido Bertoni, Joan Daemen, Michaël Peeters and Gilles Van Assche, Sponge functions, ECRYPT Hash Workshop, May 2007"
    locator: the definition of the sponge, the rate and the capacity, inner collisions and the generic attacks
  - paper: "Guido Bertoni, Joan Daemen, Michaël Peeters and Gilles Van Assche, On the indifferentiability of the sponge construction, Advances in Cryptology, EUROCRYPT 2008, LNCS 4965, Springer, 2008"
    locator: Section 3.5 (the cost N), Theorem 1 with equation (4) and Theorem 2 with equation (6)
  - paper: "Guido Bertoni, Joan Daemen, Michaël Peeters and Gilles Van Assche, Duplexing the sponge, single-pass authenticated encryption and other applications, Selected Areas in Cryptography, SAC 2011, LNCS 7118, Springer, 2012"
    locator: the duplex construction and the lemma that relates its outputs to sponge outputs
  - paper: doi:10.6028/NIST.FIPS.202
    title: NIST, FIPS 202, SHA-3 Standard, Permutation-Based Hash and Extendable-Output Functions, August 2015
    locator: Section 4 (Algorithm 8 and Figure 7), Section 5.1 (Algorithm 9, pad10*1), Section 6, and Appendix A.1 (Table 4)
---

The sponge construction builds a hash function, or an [extendable-output function](/extendable-output-function/), from one fixed permutation $f$ on $b$ bits. The state is split into an outer part of $r$ bits, the rate, and an inner part of $c = b - r$ bits, the capacity. The sponge absorbs the padded input $r$ bits at a time by XOR into the outer part, with a call of $f$ after each block, and then squeezes the output $r$ bits at a time, again with a call of $f$ between blocks. The inner part is never touched by the input and never shown in the output, and this is where the security lives: with a random permutation, no generic attack does much better than $2^{c/2}$ calls of $f$. Bertoni, Daemen, Peeters and Van Assche introduced the sponge in 2007 and proved it indifferentiable from a random oracle in 2008. [Keccak](/keccak/), and so [SHA-3](/sha-3/) and [SHAKE](/shake/), are sponges over Keccak-f[1600].

**Notation.** $f$ is the permutation on $b$-bit states, $r$ the rate, $c = b - r$ the capacity. $M$ is the input and $\ell$ the number of output bits. $\mathrm{pad}(r, m)$ is a padding rule whose output, appended to an $m$-bit string, gives a positive multiple of $r$ bits. $\mathrm{Trunc}_r(S)$ is the first $r$ bits of $S$. $N$ is the cost of an attack: its number of calls to $f$ or $f^{-1}$. The toy numbers come from the code of this page, which uses a random permutation on 16 bits with $r = c = 8$. The code is for study only and is not constant time.

## In plain words

Think of a large state, most of which is hidden. You pour the message into the visible part, a block at a time, and stir the whole state after each block with a fixed public permutation. When the message is in, you read the visible part as output, stir, read again, and so on for as long as you want output. The hidden part is never set by you and never shown to you. To force two messages into the same state, or to continue a hash you only saw the output of, you would need to control or know the hidden part, and the only generic way is a birthday search on it, about $2^{c/2}$ stirs.

## When it applies

- **You have a wide permutation, not a compression function.** The sponge needs only $f$ and never its inverse. Keccak-f[1600] has $b = 1600$; lightweight designs use permutations of a few hundred bits.
- **You want any output length.** The same instance gives a hash of fixed length or an XOF, and one squeeze can be read in pieces.
- **You can trade speed for security.** For a fixed $b$, a larger $c$ means a smaller $r$, so fewer input bits per call. SHA3-256 uses $c = 512$ and $r = 1088$; SHAKE128 uses $c = 256$ and $r = 1344$.
- **The target security is $c/2$ bits.** Choose $c$ at twice the security level. FIPS 202 sets $c = 2d$ for SHA3-$d$, which gives the $d$ bits of preimage resistance of a $d$-bit random function.

## The template

```pseudo id=main
SPONGE[f, pad, r](M, ℓ)                  ▷ returns the first ℓ bits of Z
L1  S ← 0^b
L2  P ← M ‖ pad(r, |M|)                   ▷ a positive multiple of r bits
L3  for each r-bit block P_i of P do      ▷ absorbing
L4      S ← S ⊕ (P_i ‖ 0^c)
L5      S ← f(S)
L6  Z ← Trunc_r(S); while |Z| < ℓ do      ▷ squeezing
L7      S ← f(S)
L8      Z ← Z ‖ Trunc_r(S)
```

This is FIPS 202 Algorithm 8. The output length $\ell$ does not change the output bits, only where the squeeze stops, so a sponge can be read as an infinite string.

### Padding

The padding must make the map from $M$ to the block sequence injective, and its last block must not be all zeros, or two inputs of different lengths could absorb to the same state. Keccak uses the multi-rate padding pad10*1 (FIPS 202 Algorithm 9): append a 1, then $j = (-|M| - 2) \bmod r$ zeros, then a 1. It always adds at least 2 bits and at most $r + 1$ bits. The final 1 in the last position of the block makes the padding safe for any family of sponges with the same $f$ and different rates.

In bytes, an implementation adds the domain bits and the first 1 in one byte, zeros, and sets the top bit of the last byte of the block. The code uses the byte $\texttt{1F}$ for SHAKE: the suffix bits 1111 and the first padding bit. Two boundary cases matter:

- When $r - 1$ bytes of the last block are filled, the padding is one byte, $\texttt{1F} \mid \texttt{80} = \texttt{9F}$ for SHAKE ($\texttt{86}$ for SHA-3, $\texttt{81}$ for the original Keccak).
- When the message fills whole blocks, the padding is a full extra block, $\texttt{1F}\ \texttt{00} \cdots \texttt{00}\ \texttt{80}$.

The tests absorb a 340-byte message in two pieces cut at every one of 0, 1, 100, 167, 168, 169, 200, 335, 336, 337 and 340 bytes, feed 170 bytes one byte at a time, hash messages of 166 to 169 and 335 to 336 bytes, and squeeze 400 bytes in pieces that cross the 168-byte rate boundary. All agree with `hashlib.shake_128`.

### Security

**Inner collisions.** Two inputs that lead to the same inner part $S[r..b)$ after absorbing can be fixed in the next block to give the same full state: XOR the difference of the outer parts into the next block of one of them. From then on, every common suffix gives the same output. A birthday search on the $c$ inner bits finds an inner collision in about $2^{c/2}$ calls. This is the main generic attack. A meet-in-the-middle search on the inner part, possible because $f$ is a public permutation, gives preimages at about the same cost.

**Indifferentiability.** The sponge with a random permutation is indifferentiable from a random oracle with advantage below $f_P(N) \approx ((1 - 2^{-r}) N^2 + (1 + 2^{-r}) N)/2^{c+1}$ for $N < 2^c$, and with a random transformation below $f_T(N) \approx N(N+1)/2^{c+1}$ (BDPV 2008, Theorems 2 and 1). The exact product forms are on the [indifferentiability](/indifferentiability-framework/) page. So, up to $2^{c/2}$ calls of $f$, any attack on the sponge that does not use the structure of $f$ works as well on a random oracle. This is the flat sponge claim.

**Consequences for a $d$-bit output.** Collisions cost about $\min(2^{d/2}, 2^{c/2})$ and preimages about $\min(2^d, 2^{c/2})$, up to the gap between the generic bound and the best known attacks. FIPS 202 Table 4 lists SHA3-256 at 128 bits for collisions and 256 bits for preimages and second preimages ($c = 512$), and SHAKE128 with $d$ output bits at $\min(d/2, 128)$ for collisions and at least $\min(d, 128)$ for preimages ($c = 256$).

### No length extension

A [length-extension attack](/length-extension-attack/) on a Merkle-Damgard hash works because the digest is the whole chaining value. A sponge digest is at most the outer part of a state, and for SHA3-256 only 256 of the 1088 outer bits. To absorb more blocks after $M \| \mathrm{pad}$, an attacker needs the $c$ inner bits, which no output reveals, so it must guess them, at cost $2^c$. This is why $H(K \| M)$ is a secure MAC for a sponge hash, the basis of [KMAC](/kmac/), while it is broken for SHA-256. FIPS 202 Appendix A.1 says that the SHA-3 functions are designed to resist length extension.

## Classic examples

### A toy sponge, step by step

The toy sponge has a random 16-bit permutation (seed 7) and $r = c = 1$ byte, with the padding byte $\texttt{01}$ and the top bit in the last byte. The input "ab" pads to $\texttt{61}\ \texttt{62}\ \texttt{81}$: since $r$ is one byte, the single padding byte is $\texttt{01} \mid \texttt{80}$.

| Block | State in, after XOR | State out, after $f$ |
|---|---|---|
| $\texttt{61}$ | $\texttt{61}\ \texttt{00}$ | $\texttt{e7}\ \texttt{4f}$ |
| $\texttt{62}$ | $\texttt{85}\ \texttt{4f}$ | $\texttt{27}\ \texttt{34}$ |
| $\texttt{81}$ | $\texttt{a6}\ \texttt{34}$ | $\texttt{6b}\ \texttt{07}$ |

The first output byte is $\texttt{6b}$, and three more calls of $f$ give the 4-byte output $\texttt{6b597305}$. The inner byte ($\texttt{4f}$, $\texttt{34}$, $\texttt{07}$) is never set by the input.

### An inner collision on the toy sponge

With $c = 8$ bits, a birthday search over random 2-byte messages finds two with the same inner byte after 39 tries: $\texttt{07d2}$ and $\texttt{227e}$. One more block cancels the difference in the outer byte, $\texttt{00}$ for the first and $\texttt{85}$ for the second, and both 3-byte messages $\texttt{07d200}$ and $\texttt{227e85}$ reach the full state $\texttt{ce8e}$. Their outputs agree for every suffix: $\texttt{d6dfa913a93034de}$ with no suffix, and $\texttt{e4159320597c87fb}$ with the suffix "x". Over 40 seeds the search took 22 tries on average (from 7 to 48), close to the birthday estimate $\sqrt{\pi 2^8 / 2} \approx 20$.

### SHAKE128 and SHA-3

SHAKE128 is the sponge with $f$ = Keccak-f[1600], $r = 1344$ bits (168 bytes) and $c = 256$, with the suffix 1111 before pad10*1. The code builds it from the general sponge class, and its first 32 output bytes for the empty input are $\texttt{7f9c2ba4e88f827d616045507605853ed73b8093f6efbc88eb1a6eacfa66ef26}$, as in the NIST example values. SHA3-256 is the same with $c = 512$, $r = 1088$, the suffix 01 and $\ell = 256$. See [Keccak](/keccak/), [SHA-3](/sha-3/) and [SHAKE](/shake/).

## Variations

- **Duplex construction** (BDPV 2011). The state is kept between calls: each call absorbs one padded block and returns up to $r$ bits. Every output equals a sponge output on the concatenation of the padded inputs so far, so the sponge security carries over. Duplex gives single-pass authenticated encryption (SpongeWrap), reseedable random generators, and the lightweight AEAD scheme Ascon is built on a variant of it.
- **Keyed sponge.** Put a key in the first blocks. KMAC (SP 800-185) is a keyed cSHAKE.
- **Domain separation by suffix bits.** FIPS 202 appends 01 for SHA-3 and 1111 for SHAKE before the padding, so the functions never share an input to the sponge.
- **Tree hashing on top of a sponge.** KangarooTwelve and ParallelHash split the input, hash the parts with a sponge, and hash the chaining values.
- **Random transformation in place of a permutation.** The sponge does not need $f$ to be invertible; the bound $f_T$ is then slightly weaker.

## Pitfalls

- **The capacity is the security, not the output length.** A 512-bit output from SHAKE128 still gives at most 128 bits of security. Choose $c$ at twice the target.
- **Never absorb into the inner part.** An implementation that XORs input into the capacity, or that lets the caller set it, loses the proof.
- **Padding at the boundary.** A message that fills a block exactly needs a whole extra padding block, and a block with one free byte gets a single byte that holds both the first and the last padding bits. Both cases are classic bugs; test them.
- **Absorb after squeeze.** A plain sponge must not take more input after the squeeze has started. Use the duplex construction for that.
- **Keccak is not SHA-3.** The original Keccak padding has no suffix bits, so Keccak-256 and SHA3-256 differ on every input. See [Keccak](/keccak/).
- **For study only.** The code is a direct transcription, not constant time and slow. Use `hashlib.sha3_256`, `hashlib.shake_128`, OpenSSL or XKCP.

## Exercises

1. Show that the zero padding (append zeros to fill the block) is not injective, and find two inputs that give the same SHAKE128 output under it.
2. For the toy sponge with $r = c = 8$ bits, how many tries does the inner collision search need on average? How does the number change if $r = 4$ and $c = 12$?
3. Explain the preimage attack in about $2^{c/2}$ calls when $f$ is a public permutation: meet in the middle on the inner part, using $f^{-1}$ from the output side.
4. A designer wants 128-bit security with Keccak-f[1600] and as many input bits per call as possible. Give $r$ and $c$, and compare with SHAKE128.

## References
