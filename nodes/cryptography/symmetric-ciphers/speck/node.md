---
tag: 7HAM9F
kind: algorithm
slug: speck
name: SPECK
area: cryptography/symmetric-ciphers
level: advanced
summary: An NSA family of lightweight ARX block ciphers (2013) for software, with blocks of 32 to 128 bits. A round is one addition, two rotations and two XORs. ISO declined to standardize it in 2018.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {T: the number of rounds, b: the number of blocks}
  time: {worst: Θ(b T), average: Θ(b T), best: Θ(b T)}
  space: {extra: Θ(T)}
properties: {deterministic: true}
history:
  year: 2013
  people: [Ray Beaulieu, Douglas Shors, Jason Smith, Stefan Treatman-Clark, Bryan Weeks, Louis Wingers]
  note: A team of the US National Security Agency published SPECK with SIMON in June 2013 as ePrint 2013/404. A proposal to add both to ISO/IEC 29192-2 was stopped in 2018.
prereqs: [block-cipher]
see_also: [simon-cipher, lightweight-cryptography, chacha20, xtea, key-schedule, differential-cryptanalysis, present]
sources:
  - paper: "Ray Beaulieu, Douglas Shors, Jason Smith, Stefan Treatman-Clark, Bryan Weeks and Louis Wingers, The SIMON and SPECK families of lightweight block ciphers, IACR Cryptology ePrint Archive, Report 2013/404, 2013"
    locator: Section 4 (the SPECK round function and key schedule), Table 4.1 (the parameter sets, rotation amounts and round counts), and the appendix of test vectors
  - paper: "Ray Beaulieu, Douglas Shors, Jason Smith, Stefan Treatman-Clark, Bryan Weeks and Louis Wingers, Notes on the design and analysis of SIMON and SPECK, IACR Cryptology ePrint Archive, Report 2017/560"
    locator: the design rationale of SPECK, the choice of the rotation amounts and the number of rounds, and a survey of the published attacks
  - paper: "Tomer Ashur and Atul Luykx, An account of the ISO/IEC standardization of the Simon and Speck block cipher families, in Security of Ubiquitous Computing Systems, Springer, 2021"
    locator: the history of the ISO/IEC JTC 1/SC 27 project to add SIMON and SPECK to ISO/IEC 29192-2 and its cancellation in 2018
  - paper: "Paul Crowley and Eric Biggers, Adiantum: length-preserving encryption for entry-level processors, IACR Transactions on Symmetric Cryptology 2018(4)"
    locator: the introduction, on the earlier plan to use Speck for storage encryption on low-end Android devices and the reasons to replace it
---

SPECK is a family of lightweight [block ciphers](/block-cipher/) published by a team of the US National Security Agency in 2013, together with [SIMON](/simon-cipher/). SPECK aims at software: its round is ARX, one addition modulo $2^n$, two rotations and two XORs on $n$-bit words, which is fast on almost each processor, and its key schedule reuses the round function. There are ten parameter sets, with blocks of 32 to 128 bits and keys of 64 to 256 bits. Like SIMON, it came without a public design rationale, and an ISO/IEC project to standardize it was stopped in 2018. This page implements all ten parameter sets and checks the published vectors.

## In plain words

SPECK splits the block into a left word and a right word. In each round it rotates the left word to the right by 8 places, adds the right word to it as numbers, and XORs a round key into the result; this is the new left word. Then it rotates the right word to the left by 3 places and XORs the new left word into it; this is the new right word. The addition is the only nonlinear step: its carries mix the low bits into the high bits. The cipher repeats this 22 to 34 times. To make the round keys, SPECK runs the same round on the key words, with the round number in place of a key. On a computer each round is a handful of fast instructions and needs no table.

## The problem

Give a family of block ciphers that is small in code and fast on microcontrollers and general processors, for many block and key sizes, with a margin against known attacks. SIMON targets hardware; SPECK targets software, where an adder is free.

## The algorithm

Let $n$ be the word size, $m$ the number of key words and $T$ the number of rounds (Table 4.1 of the paper). The rotation amounts are $\alpha = 7, \beta = 2$ for $n = 16$, and $\alpha = 8, \beta = 3$ otherwise.

| block $2n$ | key $mn$ | $n$ | $m$ | $T$ |
|---|---|---|---|---|
| 32 | 64 | 16 | 4 | 22 |
| 48 | 72, 96 | 24 | 3, 4 | 22, 23 |
| 64 | 96, 128 | 32 | 3, 4 | 26, 27 |
| 96 | 96, 144 | 48 | 2, 3 | 28, 29 |
| 128 | 128, 192, 256 | 64 | 2, 3, 4 | 32, 33, 34 |

Write $\ggg$ and $\lll$ for rotation of an $n$-bit word, and $+$, $-$ for arithmetic modulo $2^n$.

**Key schedule.** The key is $\ell_{m-2}, \ldots, \ell_0, k_0$. For $i = 0, \ldots, T - 2$:
$$\ell_{i+m-1} = (k_i + (\ell_i \ggg \alpha)) \oplus i, \qquad k_{i+1} = (k_i \lll \beta) \oplus \ell_{i+m-1}.$$
This is the round function applied to the pair $(\ell_i, k_i)$ with the round number $i$ as the key.

```pseudo id=main
SPECK-ENCRYPT((x, y), key)
L1  k[0..T−1] ← KEY-SCHEDULE(key)
L2  for i ← 0 to T − 1 do
L3      x ← ((x ⋙ α) + y) ⊕ k[i]
L4      y ← (y ⋘ β) ⊕ x
L5  return (x, y)

SPECK-DECRYPT((x, y), key)
L6  k[0..T−1] ← KEY-SCHEDULE(key)
L7  for i ← T − 1 downto 0 do
L8      y ← (x ⊕ y) ⋙ β
L9      x ← ((x ⊕ k[i]) − y) ⋘ α
L10 return (x, y)
```

Line L3 gives the nonlinearity: the carries of the addition depend on both words. Line L4 spreads the new $x$ into $y$, so both words change in each round. SPECK is not a Feistel network; each round is still invertible because each step is (rotation, addition of a known word, XOR with a known word). The round is close to the MIX function of Threefish, with fixed rotation amounts. The round counter $i$ in the key schedule makes the round keys differ and stops slide attacks.

The code on this page is for study only. It is not constant time as Python runs it, and it must not protect real data. Use a vetted cipher from libsodium, OpenSSL or a FIPS 140 validated module.

## Example

SPECK64/128 with the key 1b1a1918 13121110 0b0a0908 03020100 ($\ell_2, \ell_1, \ell_0, k_0$) and the plaintext $(x, y) = $ (3b726574, 7475432d), the vector of the paper's appendix.

| step | value |
|---|---|
| round keys $k_0, \ldots, k_3$ | 03020100, 131d0309, bbd80d53, 0d334df3 |
| round 1, line L3: $(x \ggg 8) + y$ | 743b7265 + 7475432d = e8b0b592 |
| round 1, after line L3 ($\oplus k_0$) | $x = $ ebb2b492 |
| round 1, after line L4 | $y = $ a3aa196b $\oplus$ ebb2b492 = 4818adf9 |
| round 2 | (c81963a4, 88dc0c6e) |
| after 27 rounds | (8c6fa548, 454e028b) |

The tests check the paper's vectors for SPECK32/64, 48/72, 64/96, 64/128, 128/128 and 128/256, a round trip for all ten parameter sets, and that the key schedule equals the round function with the counter as key.

## Correctness

Each step of a round has an inverse. Given the output $(x', y')$ of lines L3 and L4: $y' = (y \lll \beta) \oplus x'$, so $y = (x' \oplus y') \ggg \beta$, which is line L8. Then $x' = ((x \ggg \alpha) + y) \oplus k$, so $x = ((x' \oplus k) - y) \lll \alpha$, which is line L9. Decryption runs these inverses with the round keys in the reverse order, so it inverts encryption. The proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

Each round costs one addition, two rotations and two XORs on $n$-bit words, and each key schedule step the same. So a block costs $\Theta(T)$ word operations and $b$ blocks cost $\Theta(b T)$. The round keys take $\Theta(T)$ words, or $m$ words if they are made on the fly during encryption. The paper reports software results on 8-bit, 16-bit and 64-bit processors, where the code is small and fast because each step is one instruction or a few.

## Properties

- **Ten parameter sets**, from SPECK32/64 to SPECK128/256.
- **ARX.** Addition, rotation and XOR only: no tables, so no cache-timing leaks from table lookups, and simple constant-time code.
- **Key schedule reuses the round.** The same code serves both, which saves program memory.
- **Not Feistel.** Decryption needs subtraction and the inverse rotations, so encryption and decryption differ; many modes, such as CTR, need only encryption.
- **Late rationale.** As for SIMON, the reasons for the rotation amounts and round counts came in the designers' notes of 2017.

## Variants and improvements

- **SIMON and SPECK compared.** Both come from the same paper with the same parameter sets. [SIMON](/simon-cipher/) is a Feistel network whose round uses AND, XOR and rotation and whose key schedule is a linear map with constants; it is the smaller in hardware. SPECK uses modular addition in a non-Feistel ARX round and a key schedule built from its own round; it is the faster in software. SPECK has fewer rounds because one addition mixes more than one AND.
- **Cryptanalysis.** Differential and linear attacks, many found with automatic search tools, reach a large part of the rounds of each member, but none breaks a full member.
- **Other ARX designs.** [ChaCha20](/chacha20/) and Threefish use ARX for a stream cipher and a large block cipher. [XTEA](/xtea/) is an earlier small ARX-like block cipher. Chaskey (2014) is an ARX MAC for microcontrollers.

## When to use it

SPECK suits software on constrained processors where a small, fast block cipher is required and a non-standard algorithm is acceptable. Many projects avoid it because of the missing rationale at publication, its origin and the failed ISO/IEC process. In 2018 Google planned to use SPECK for storage encryption on entry-level Android devices, and then designed Adiantum, built on [ChaCha](/chacha20/), instead (Crowley and Biggers). For new designs prefer [Ascon](/ascon/) (NIST SP 800-232) or a ChaCha-based scheme.

## Pitfalls

- **Word and byte order.** The paper writes the key as $\ell_{m-2}, \ldots, \ell_0, k_0$ and the block as $(x, y)$ with $x$ first; the bytes of each word are little-endian in many implementations. Check a vector before you combine two implementations.
- **The rotation amounts of SPECK32.** Only $n = 16$ uses $\alpha = 7$ and $\beta = 2$.
- **Small blocks.** SPECK32/64 has a 32-bit block and reaches the [birthday bound](/birthday-attack/) after about $2^{16}$ blocks under one key.
- **The key schedule counter.** It is XORed after the addition, and it runs from 0. Starting at 1 gives a different cipher.

## Implementations

## History

The NSA team that designed SIMON designed SPECK at the same time, and both appeared on the IACR ePrint archive in June 2013. SPECK drew more academic analysis than most lightweight ciphers because of its simple ARX round. The designers published design notes in 2017. The NSA proposed SIMON and SPECK for ISO/IEC 29192-2, and after objections from several national bodies the project was stopped in 2018, as told by Ashur and Luykx. SPECK was briefly added to the Linux kernel in 2018 for Android storage encryption; Google then moved to Adiantum.

## References
