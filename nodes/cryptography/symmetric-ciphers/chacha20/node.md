---
tag: 79BC7C
kind: algorithm
slug: chacha20
name: ChaCha20
area: cryptography/symmetric-ciphers
level: advanced
summary: Bernstein's 2008 variant of Salsa20. A 20-round ARX function of key, counter and nonce makes 64-byte keystream blocks. RFC 8439 fixes a 32-bit counter and a 96-bit nonce.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {m: the message length in bytes}
  time: {worst: Θ(m), average: Θ(m), best: Θ(m)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2008
  people: [Daniel J. Bernstein]
  note: Bernstein presented ChaCha at the SASC 2008 workshop as a variant of Salsa20 with faster diffusion. RFC 7539 (2015) and then RFC 8439 (2018) specified ChaCha20 for IETF protocols.
prereqs: [salsa20, stream-cipher]
see_also: [salsa20, chacha20-poly1305, poly1305, ctr-mode, nonce, pseudorandom-function, rc4, avalanche-effect]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc8439"
    title: Yoav Nir and Adam Langley, RFC 8439, ChaCha20 and Poly1305 for IETF Protocols, June 2018
    locator: Section 2.1 (quarter round), 2.1.1 (test vector), 2.2 (state), 2.3 and 2.3.2 (block function and test vector), 2.4 and 2.4.2 (encryption and test vector)
  - paper: "Daniel J. Bernstein, ChaCha, a variant of Salsa20, Workshop Record of SASC 2008, The State of the Art of Stream Ciphers"
    locator: the ChaCha quarter-round, the change of the state layout, and the argument for faster diffusion than Salsa20
  - paper: "Jean-Philippe Aumasson, Simon Fischer, Shahram Khazaei, Willi Meier and Christian Rechberger, New features of Latin dances, analysis of Salsa, ChaCha, and Rumba, Fast Software Encryption (FSE 2008), LNCS 5086"
    locator: Table 1 (ChaCha6 in 2^139 and ChaCha7 in 2^248 trials, success probability 1/2)
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Chapter 3 (stream ciphers) and the description of Salsa20 and ChaCha there
---

ChaCha20 is a [stream cipher](/stream-cipher/) that Daniel J. Bernstein published in 2008 as a variant of [Salsa20](/salsa20/). Its core maps a 256-bit key, a block counter and a nonce to a 64-byte keystream block through 20 rounds of 32-bit additions, rotations and XORs (ARX). It changes the Salsa20 quarter round so that each word is updated twice, which spreads changes faster. RFC 8439 defines the IETF version with a 32-bit counter and a 96-bit nonce, and pairs it with [Poly1305](/poly1305/) in [ChaCha20-Poly1305](/chacha20-poly1305/).

## In plain words

ChaCha20 has a small table of sixteen numbers. Four are fixed, eight hold the key, one counts blocks, and three hold a number that must be new for each message. The cipher mixes the table with twenty rounds of three cheap steps: add two numbers, XOR one into another, and rotate the bits of a number. Then it adds the original table back, so the mixing cannot be run backwards to find the key. The result is 64 bytes of keystream. For the next 64 bytes, it adds one to the counter and does it again. To encrypt, XOR the keystream into the message. The cipher has no tables and no branches on secret data, so it is fast and safe from cache timing leaks on ordinary processors.

## The problem

The input is a key $K$ of 256 bits, a nonce $N$ of 96 bits, an initial counter $c_0$ of 32 bits, and a message $M$ of $m$ bytes. The output is $C = M \oplus Z$, where $Z$ is the first $m$ bytes of $B(K, c_0, N) \Vert B(K, c_0 + 1, N) \Vert \ldots$ and $B$ is the ChaCha20 block function. Decryption is the same map. The pair $(K, N)$ must never repeat, and one pair encrypts at most $2^{32}$ blocks, that is 256 GiB.

The security model: $B(K, \cdot)$ is assumed to be a [pseudorandom function](/pseudorandom-function/) of the 128-bit input (counter and nonce). Then the cipher is a counter-mode construction, and it is IND-CPA secure for nonce-respecting adversaries, in the standard model under that assumption. In the real-or-random form of the game, an adversary $A$ that makes $q$ encryption queries of at most $2^{32}$ blocks each has advantage at most $\mathrm{Adv}^{\mathrm{prf}}_B(A')$ for some $A'$ with about the same running time $t$: there is no birthday term, because the inputs to $B$ never repeat. We write $K$ for the key, $A$ for an adversary and $\mathrm{Adv}$ for its advantage, as in the rest of this area.

## The algorithm

All words are 32-bit, $+$ is addition modulo $2^{32}$, and $\lll$ is a left rotation. The state has 16 words, in a $4 \times 4$ matrix with indices 0 to 15 by rows:

| row | words |
|---|---|
| 0 | the constants 0x61707865, 0x3320646e, 0x79622d32, 0x6b206574 ("expand 32-byte k") |
| 1 and 2 | the key, eight words, little-endian |
| 3 | the counter (word 12) and the nonce (words 13 to 15), little-endian |

```pseudo id=main
QR(a, b, c, d)                             ▷ the ChaCha quarter round
L1  a ← a + b;  d ← d ⊕ a;  d ← d ⋘ 16
L2  c ← c + d;  b ← b ⊕ c;  b ← b ⋘ 12
L3  a ← a + b;  d ← d ⊕ a;  d ← d ⋘ 8
L4  c ← c + d;  b ← b ⊕ c;  b ← b ⋘ 7

BLOCK(K, ctr, N)                           ▷ RFC 8439, Section 2.3
L5  x ← (constants, K, ctr, N) as 16 words
L6  w ← x
L7  repeat 10 times                        ▷ 10 double rounds = 20 rounds
L8      QR(w0,w4,w8,w12); QR(w1,w5,w9,w13); QR(w2,w6,w10,w14); QR(w3,w7,w11,w15)
L9      QR(w0,w5,w10,w15); QR(w1,w6,w11,w12); QR(w2,w7,w8,w13); QR(w3,w4,w9,w14)
L10 return the 16 words w + x, each as 4 bytes, little-endian

ENCRYPT(K, c0, N, M)                       ▷ RFC 8439, Section 2.4
L11 for j ← 0 to ⌈m / 64⌉ − 1 do
L12     Z ← BLOCK(K, c0 + j, N)
L13     C[64j ..] ← M[64j ..] ⊕ Z, truncated to the bytes of M
```

Line L8 is a column round and line L9 a diagonal round. The feedforward of line L10 adds the input; without it, the rounds are a permutation, and anyone who sees a block could run them backwards to the key.

The code on this page is for study only. It is not constant time as Python runs it, and it must not protect real data. Use ChaCha20-Poly1305 from libsodium, OpenSSL or a FIPS 140 validated module.

## Example

RFC 8439, Section 2.1.1, applies QR to $a = $ 0x11111111, $b = $ 0x01020304, $c = $ 0x9b8d6f43, $d = $ 0x01234567. Each line changes two words:

| line | words that change |
|---|---|
| L1 | $a = $ 0x12131415, $d = $ 0x51721330 |
| L2 | $c = $ 0xecff8273, $b = $ 0xd8177edf |
| L3 | $a = $ 0xea2a92f4, $d = $ 0x5881c4bb |
| L4 | $c = $ 0x4581472e, $b = $ 0xcb1cf8ce |

The result $(a, b, c, d) = $ (0xea2a92f4, 0xcb1cf8ce, 0x4581472e, 0x5881c4bb) is the value in the RFC. For the full block function, RFC 8439, Section 2.3.2, uses the key 00 01 ... 1f, the nonce 00 00 00 09 00 00 00 4a 00 00 00 00 and the counter 1; the block starts 10 f1 e7 e4 d1 3b 59 15. Section 2.4.2 encrypts the 114-byte "Ladies and Gentlemen of the class of '99 ..." text with counter 1; the ciphertext starts 6e 2e 35 9a. The test file checks all three vectors.

## Correctness

Each operation of lines L1 to L4 is invertible on 32-bit words, so the rounds are a permutation of the 512-bit state. This is not needed for decryption, which only recomputes the keystream: BLOCK is a deterministic function of $(K, ctr, N)$, so the receiver gets the same $Z$ and $(M \oplus Z) \oplus Z = M$. The counter of line L12 differs for each block of one message, and the nonce differs between messages, so no block input repeats under one key. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- One block costs 80 quarter rounds, that is 320 additions, 320 XORs and 320 rotations, plus 16 additions for the feedforward. It gives 64 bytes.
- A message of $m$ bytes needs $\lceil m/64 \rceil$ blocks, so the time is $\Theta(m)$. The state is 64 bytes, so the extra space is $\Theta(1)$.
- The blocks are independent, so an implementation computes 4 or 8 of them at once in SIMD registers, and it can seek to any block.

## Properties

- **Faster diffusion than Salsa20.** In the Salsa20 quarter round each word is updated once, and the input word $y_2$ does not reach the output word $z_1$. In the ChaCha quarter round each word is updated twice, and each input word reaches all four output words. Over random inputs, one flipped input bit flips on average about 16.3 output bits of a Salsa20 quarter round and about 26.5 output bits of a ChaCha quarter round (the mean over the four input words). Bernstein also reorders the state so that the column and diagonal rounds need no transpose.
- **Best attacks.** Aumasson, Fischer, Khazaei, Meier and Rechberger (FSE 2008) gave key recovery on ChaCha6 in $2^{139}$ trials and on ChaCha7 in $2^{248}$ trials, each with success probability 1/2 (their Table 1). No attack on 20 rounds is known.
- **Constant time in practice.** ChaCha20 uses only additions, XORs and fixed rotations, with no secret-dependent table lookups or branches.
- **Random access.** Block $j$ depends only on $(K, c_0 + j, N)$.
- **Malleable.** Like each stream cipher, it gives no integrity. Use it inside an AEAD.

## Variants and improvements

- **The original layout.** Bernstein's ChaCha uses a 64-bit counter in words 12 and 13 and a 64-bit nonce in words 14 and 15. RFC 8439 uses a 32-bit counter and a 96-bit nonce. Both have 128 bits of counter and nonce, but the RFC layout limits one message to $2^{32}$ blocks (256 GiB), while the original allows $2^{64}$ blocks. A random 64-bit nonce repeats after about $2^{32}$ messages by the [birthday bound](/birthday-attack/), so the original layout needs counter nonces.
- **ChaCha8 and ChaCha12.** The same design with 8 or 12 rounds, for speed.
- **XChaCha20.** A 192-bit nonce: an HChaCha20 call derives a subkey from the key and the first 128 bits of the nonce. It is in an Internet-Draft, not in an RFC. A random 192-bit nonce is safe to choose at random.
- **ChaCha20-Poly1305.** The AEAD of RFC 8439, Section 2.8. It uses block 0 to make a one-time [Poly1305](/poly1305/) key and starts encryption at counter 1. That page covers the AEAD; this page covers only the cipher.

## When to use it

Use ChaCha20 in ChaCha20-Poly1305 when you need fast authenticated encryption in software, in particular on processors without AES instructions. TLS 1.3, SSH and WireGuard use it. Do not use bare ChaCha20 for data that an attacker can change.

## Pitfalls

- **Nonce reuse.** Two messages with the same $(K, N)$ get the same keystream, and $C \oplus C' = M \oplus M'$. Generate nonces with a counter, or use XChaCha20 with random nonces.
- **Counter overflow.** In line L12 the counter is 32 bits. A message longer than $2^{32}$ blocks wraps it to 0 and reuses keystream. Reject such messages.
- **Mixing up the layouts.** An implementation of the 64-bit nonce layout and one of the RFC layout give different output for the same bytes. The test vectors of RFC 8439 catch this.
- **Byte order.** Lines L5 and L10 read and write words little-endian. A big-endian load passes the quarter round test of Section 2.1.1 but fails the block test of Section 2.3.2.
- **Dropping the feedforward.** Without the addition in line L10, the block is an invertible function of a known state with the key inside, and one block reveals the key.

## Implementations

## History

Bernstein designed Salsa20 in 2005 for the eSTREAM project and presented ChaCha at the SASC 2008 workshop as a variant with faster diffusion and the same speed or better. RFC 7539 (2015) specified it for IETF protocols, and RFC 8439 (2018) replaced RFC 7539 with corrections. Aumasson et al. gave the first analysis of reduced-round ChaCha in 2008.

## References
