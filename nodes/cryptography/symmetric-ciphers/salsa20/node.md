---
tag: 12PMYB
kind: algorithm
slug: salsa20
name: Salsa20
area: cryptography/symmetric-ciphers
level: advanced
summary: Bernstein's 2005 ARX stream cipher. A 20-round hash of key, nonce and block counter, with a feedforward, gives 64 bytes of keystream. Salsa20/12 is in the eSTREAM software portfolio.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {m: the message length in bytes, r: the number of rounds}
  time: {worst: Θ(r m), average: Θ(r m), best: Θ(r m)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2005
  people: [Daniel J. Bernstein]
  note: Bernstein submitted Salsa20 to the eSTREAM project in 2005. The final eSTREAM portfolio of April 2008 put Salsa20/12 in profile 1, for software.
prereqs: [stream-cipher]
see_also: [chacha20, rc4, pseudorandom-function, nonce, ctr-mode, avalanche-effect, differential-cryptanalysis, trivium]
sources:
  - url: "https://cr.yp.to/snuffle/spec.pdf"
    title: Daniel J. Bernstein, Salsa20 specification, 2005
    locator: Sections 3 to 6 (quarterround, rowround, columnround, doubleround), Section 8 (the hash and its examples), Section 9 (expansion and examples), Section 10 (encryption)
  - paper: "Daniel J. Bernstein, The Salsa20 family of stream ciphers, in New Stream Cipher Designs, The eSTREAM Finalists, LNCS 4986, Springer, 2008"
    locator: the design rationale, the reduced versions Salsa20/8 and Salsa20/12, and the security claims
  - paper: "Jean-Philippe Aumasson, Simon Fischer, Shahram Khazaei, Willi Meier and Christian Rechberger, New features of Latin dances, analysis of Salsa, ChaCha, and Rumba, Fast Software Encryption (FSE 2008), LNCS 5086"
    locator: Table 1 (key recovery on the 256-bit Salsa20/8 in 2^251 trials and on Salsa20/7 in 2^151, success probability 1/2) and Section 3 (probabilistic neutral bits)
  - paper: "Steve Babbage, Christophe De Canniere, Anne Canteaut, Carlos Cid, Henri Gilbert, Thomas Johansson, Matthew Parker, Bart Preneel, Vincent Rijmen and Matthew Robshaw, The eSTREAM portfolio, ECRYPT, April 2008, revised September 2008"
    locator: the profile 1 (software) portfolio, HC-128, Rabbit, Salsa20/12 and SOSEMANUK
---

Salsa20 is a [stream cipher](/stream-cipher/) that Daniel J. Bernstein designed in 2005. Its core is a function of 64 bytes to 64 bytes built from 32-bit additions, rotations and XORs (ARX), applied to a block that holds four constants, a 256-bit (or 128-bit) key, a 64-bit nonce and a 64-bit block counter. Twenty rounds and a final feedforward make one 64-byte keystream block. The reduced version Salsa20/12 is in the profile 1 (software) portfolio of eSTREAM, and [ChaCha20](/chacha20/) is its later variant.

## In plain words

Salsa20 puts sixteen numbers in a four by four grid: four fixed numbers on the diagonal, the key, a fresh number for each message, and a block counter. It then mixes the grid. Each step adds two numbers, rotates the bits of the sum, and XORs the result into a third number. The cipher mixes all four columns, then all four rows, and repeats this ten times. At the end it adds the original grid back, so nobody can run the mixing backwards. The 64 bytes that result are the keystream for one block. The next block uses the next counter value. To encrypt, XOR the keystream with the message. The same steps decrypt.

## The problem

The input is a key $k$ of 32 bytes (or 16), a nonce $v$ of 8 bytes, and a message $m$ of length below $2^{70}$ bytes. The output is $c = m \oplus Z$, where byte $i$ of $Z$ is byte $i \bmod 64$ of $\mathrm{Salsa20}_k(v, \lfloor i/64 \rfloor)$, as in Section 10 of the specification. The pair $(k, v)$ must not repeat.

The security model: $(v, i) \mapsto \mathrm{Salsa20}_k(v, i)$ is assumed to be a [pseudorandom function](/pseudorandom-function/) of the 128-bit input. Then encryption is a counter-mode scheme and is IND-CPA secure for nonce-respecting adversaries, in the standard model, with no birthday term, because no input repeats. We write $k$ for the key, $A$ for an adversary and $\mathrm{Adv}$ for its advantage.

## The algorithm

All words are 32-bit, $+$ is addition modulo $2^{32}$ and $\lll$ is left rotation. Bytes become words little-endian.

```pseudo id=main
QUARTERROUND(y0, y1, y2, y3)               ▷ specification, Section 3
L1  z1 ← y1 ⊕ ((y0 + y3) ⋘ 7)
L2  z2 ← y2 ⊕ ((z1 + y0) ⋘ 9)
L3  z3 ← y3 ⊕ ((z2 + z1) ⋘ 13)
L4  z0 ← y0 ⊕ ((z3 + z2) ⋘ 18)
    return (z0, z1, z2, z3)

SALSA20-HASH(x)                            ▷ x is 16 words; Section 8
L5  z ← x
L6  repeat 10 times                        ▷ 10 double rounds = 20 rounds
L7      z ← COLUMNROUND(z)                  ▷ QR on (z0,z4,z8,z12) (z5,z9,z13,z1) (z10,z14,z2,z6) (z15,z3,z7,z11)
L8      z ← ROWROUND(z)                     ▷ QR on (z0,z1,z2,z3) (z5,z6,z7,z4) (z10,z11,z8,z9) (z15,z12,z13,z14)
L9  return z + x                           ▷ the feedforward, word by word

ENCRYPT(k, v, m)                           ▷ Sections 9 and 10
L10 x(i) ← (σ0, k[0..15], σ1, v, i, σ2, k[16..31], σ3), σ = "expand 32-byte k"
L11 for each block i: Z ← SALSA20-HASH(x(i))
L12     c[64i ..] ← m[64i ..] ⊕ Z, truncated to the bytes of m
```

The 16 words, as a $4 \times 4$ matrix by rows, are:

| | col 0 | col 1 | col 2 | col 3 |
|---|---|---|---|---|
| row 0 | $\sigma_0$ | key | key | key |
| row 1 | key | $\sigma_1$ | nonce | nonce |
| row 2 | counter | counter | $\sigma_2$ | key |
| row 3 | key | key | key | $\sigma_3$ |

The constants are on the diagonal. A 16-byte key uses $\tau$ = "expand 16-byte k" and repeats the key in both halves. Each quarterround starts at a diagonal word, so the column round (line L7) and the row round (line L8) each mix one word of each row and of each column with the constants.

The code on this page is for study only. It is not constant time as Python runs it, and it must not protect real data. Use XSalsa20-Poly1305 or ChaCha20-Poly1305 from libsodium.

## Example

The specification, Section 3, gives quarterround(0xe7e8c006, 0xc4f9417d, 0x6479b4b2, 0x68c67137). The four lines compute:

| line | sum before the rotation | new word |
|---|---|---|
| L1 | $y_0 + y_3 = $ 0x50af313d | $z_1 = $ 0x9361dfd5 |
| L2 | $z_1 + y_0 = $ 0x7b4a9fdb | $z_2 = $ 0xf1460244 |
| L3 | $z_2 + z_1 = $ 0x84a7e219 | $z_3 = $ 0x948541a3 |
| L4 | $z_3 + z_2 = $ 0x85cb43e7 | $z_0 = $ 0xe876d72b |

This is the value in the specification. Section 9 expands the key bytes 1 to 16 and 201 to 216 with the input bytes 101 to 116; the output starts 69, 37, 68, 39, 41, 15, 107, 193. The hash of 64 zero bytes is 64 zero bytes, because each operation maps zero words to zero words; the constants in line L10 keep this input out of real use.

## Correctness

Each line L1 to L4 has the form $z \leftarrow y \oplus f(\ldots)$ where $f$ does not read $y$, so the quarterround is invertible, and the 20 rounds are a permutation of the 16-word state. Decryption does not invert them: it recomputes the same keystream, because the hash is a deterministic function of $(k, v, i)$, and $(m \oplus Z) \oplus Z = m$. The counter $i$ is distinct for each block of a message, and the nonce for each message, so under one key no hash input repeats. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- One hash costs $r = 20$ rounds of 4 quarterrounds: 320 additions, 320 rotations and 320 XORs, plus 16 additions for line L9. It makes 64 bytes.
- A message of $m$ bytes costs $\lceil m/64 \rceil$ hashes, so the time is $\Theta(r m)$ and the extra space is the 64-byte state.
- The blocks are independent, so SIMD code computes several at once, and a reader can seek to block $i$ directly.

## Properties

- **Reduced rounds.** Salsa20/8 and Salsa20/12 use 8 and 12 rounds. Salsa20/12 is the eSTREAM profile 1 version. Aumasson, Fischer, Khazaei, Meier and Rechberger (FSE 2008) recover the 256-bit key of Salsa20/8 in about $2^{251}$ trials and of Salsa20/7 in about $2^{151}$ trials, with success probability 1/2 (their Table 1). Their method combines a biased output difference after a few rounds with probabilistic neutral key bits, so that only part of the key needs an exhaustive search. The attack on 8 rounds is only slightly faster than the $2^{256}$ of a key search, and no attack on 12 or 20 rounds is known.
- **Diffusion.** In a quarterround each word changes once. ChaCha changes each word twice per quarterround and so diffuses faster; see [ChaCha20](/chacha20/).
- **No secret-dependent lookups.** ARX operations run in constant time on common processors, so there are no cache timing leaks of the kind that hit table-based AES.
- **Malleable.** As for each stream cipher, a flipped ciphertext bit flips the same plaintext bit.

## Variants and improvements

- **XSalsa20.** A 192-bit nonce: HSalsa20 hashes the key with the first 128 bits of the nonce to a subkey, and Salsa20 runs with that subkey and the last 64 bits. A random 192-bit nonce is safe; a random 64-bit nonce collides after about $2^{32}$ messages. NaCl and libsodium use XSalsa20 with Poly1305 in crypto_secretbox.
- **ChaCha.** The 2008 variant with a new quarter round and a new state layout. It replaced Salsa20 in TLS and other IETF protocols.
- **Salsa20 core as a hash.** scrypt uses Salsa20/8 core as its mixing function.

## When to use it

Use XSalsa20-Poly1305 through libsodium when you need random nonces and a well-studied software cipher. For IETF protocols use ChaCha20-Poly1305. Do not use Salsa20 without a MAC.

## Pitfalls

- **Nonce reuse.** With only 64 bits, random nonces repeat after about $2^{32}$ messages, and a repeat gives $c \oplus c' = m \oplus m'$. Use a counter, or XSalsa20.
- **Wrong counter position.** In line L10 the 64-bit counter is words 8 and 9, after the nonce in words 6 and 7. An implementation that swaps them still round-trips, but it fails the Section 9 vector.
- **Missing feedforward.** Line L9 adds $x$. Without it, the rounds can be run backwards from one keystream block to recover the key words.
- **Rotation amounts.** Lines L1 to L4 use 7, 9, 13 and 18 in that order. Using the ChaCha amounts (16, 12, 8, 7) gives a different cipher.
- **Confusing the hash with a hash function.** The "Salsa20 hash" is not collision resistant in the sense of a [cryptographic hash function](/cryptographic-hash-function/): it maps 0 to 0 and has other simple structure. It is safe only with the constants of line L10.

## Implementations

## History

Bernstein published Salsa20 in 2005 and submitted it to eSTREAM, the ECRYPT stream cipher project. He also proposed Salsa20/8 and Salsa20/12 for evaluation. The eSTREAM portfolio of April 2008 put Salsa20/12 in profile 1, next to HC-128, Rabbit and SOSEMANUK. The chapter "The Salsa20 family of stream ciphers" in New Stream Cipher Designs (LNCS 4986, 2008) collects the design. The best attack in that period, by Aumasson et al., reached 8 rounds. Bernstein then published ChaCha in 2008.

## References
