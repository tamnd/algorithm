---
tag: D973ES
kind: algorithm
slug: simon-cipher
name: SIMON
area: cryptography/symmetric-ciphers
level: advanced
summary: An NSA family of lightweight Feistel block ciphers (2013) for hardware, with blocks of 32 to 128 bits. Its round uses only AND, XOR and rotations. ISO declined to standardize it in 2018.
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
  note: A team of the US National Security Agency published SIMON and SPECK together in June 2013 as ePrint 2013/404. A proposal to add them to ISO/IEC 29192-2 was stopped in 2018.
prereqs: [feistel-network, block-cipher]
see_also: [speck, present, lightweight-cryptography, feistel-network, key-schedule, differential-cryptanalysis, bit-slicing]
sources:
  - paper: "Ray Beaulieu, Douglas Shors, Jason Smith, Stefan Treatman-Clark, Bryan Weeks and Louis Wingers, The SIMON and SPECK families of lightweight block ciphers, IACR Cryptology ePrint Archive, Report 2013/404, 2013"
    locator: Section 3 (the SIMON round function, key schedule and constant sequences z0 to z4), Table 3.1 (the parameter sets and round counts), and the appendix of test vectors
  - paper: "Ray Beaulieu, Douglas Shors, Jason Smith, Stefan Treatman-Clark, Bryan Weeks and Louis Wingers, Notes on the design and analysis of SIMON and SPECK, IACR Cryptology ePrint Archive, Report 2017/560"
    locator: the design rationale, the choice of the rotation amounts and of the number of rounds, and a survey of the published attacks
  - paper: "Tomer Ashur and Atul Luykx, An account of the ISO/IEC standardization of the Simon and Speck block cipher families, in Security of Ubiquitous Computing Systems, Springer, 2021"
    locator: the history of the ISO/IEC JTC 1/SC 27 project to add SIMON and SPECK to ISO/IEC 29192-2 and its cancellation in 2018
---

SIMON is a family of lightweight [block ciphers](/block-cipher/) published by a team of the US National Security Agency in 2013, together with its sister family [SPECK](/speck/). It is a [Feistel network](/feistel-network/) on two $n$-bit words whose round function uses only bitwise AND, XOR and fixed rotations, so it is very small in hardware. The family has ten parameter sets, with blocks of 32 to 128 bits and keys of 64 to 256 bits. The designers gave the specification and test vectors but at first no design rationale or security analysis, and in 2018 an ISO/IEC project to standardize SIMON and SPECK was stopped. This page implements all ten parameter sets and checks the published vectors.

## In plain words

SIMON splits the block into a left word and a right word. In each round it takes the left word and makes three rotated copies of it: by 1, by 8 and by 2 places. It ANDs the first two copies and XORs the third. It XORs the result with the right word and a round key, and this becomes the new left word. The old left word becomes the new right word. This repeats 32 to 72 times, depending on the size. The round keys come from the key by rotations and XORs, plus a fixed bit pattern that makes each round key different. A chip needs only a few AND and XOR gates and wires per bit, and no table and no adder.

## The problem

Give a family of block ciphers for constrained devices that covers many block and key sizes, is as small as possible in hardware, and is also fast on small microcontrollers. Each member must resist known attacks with a margin. SIMON aims at hardware; SPECK aims at software.

## The algorithm

Let $n$ be the word size, $m$ the number of key words, $T$ the number of rounds and $j$ the index of the constant sequence, from this table (Table 3.1 of the paper):

| block $2n$ | key $mn$ | $n$ | $m$ | $T$ | $z_j$ |
|---|---|---|---|---|---|
| 32 | 64 | 16 | 4 | 32 | $z_0$ |
| 48 | 72, 96 | 24 | 3, 4 | 36, 36 | $z_0$, $z_1$ |
| 64 | 96, 128 | 32 | 3, 4 | 42, 44 | $z_2$, $z_3$ |
| 96 | 96, 144 | 48 | 2, 3 | 52, 54 | $z_2$, $z_3$ |
| 128 | 128, 192, 256 | 64 | 2, 3, 4 | 68, 69, 72 | $z_2$, $z_3$, $z_4$ |

Write $S^r$ for left rotation by $r$ of an $n$-bit word, and $f(x) = (S^1 x \wedge S^8 x) \oplus S^2 x$.

**Key schedule.** The key is $k_{m-1}, \ldots, k_0$, and these are the first $m$ round keys. For $i \ge m$, let $t = S^{-3} k_{i-1}$; if $m = 4$, set $t \leftarrow t \oplus k_{i-3}$; then
$$k_i = c \oplus (z_j)_{(i-m) \bmod 62} \oplus k_{i-m} \oplus t \oplus S^{-1} t, \qquad c = 2^n - 4,$$
where $(z_j)_r$ is bit $r$ of the 62-bit sequence $z_j$, read from the left.

```pseudo id=main
SIMON-ENCRYPT((x, y), key)
L1  k[0..T−1] ← KEY-SCHEDULE(key)
L2  for i ← 0 to T − 1 do
L3      (x, y) ← (y ⊕ f(x) ⊕ k[i], x)          ▷ f(x) = (S¹x AND S⁸x) ⊕ S²x
L4  return (x, y)

SIMON-DECRYPT((x, y), key)
L5  k[0..T−1] ← KEY-SCHEDULE(key)
L6  for i ← T − 1 downto 0 do
L7      (x, y) ← (y, x ⊕ f(y) ⊕ k[i])
L8  return (x, y)
```

The AND of two rotations is the only nonlinear part. It has degree 2, so one round is weak, and SIMON relies on many rounds. The rotation by 2 adds diffusion. The constant $c$ and the sequences $z_j$ break the symmetry between rounds, which stops slide and rotational attacks. The $z_j$ are binary sequences of period 31 ($z_0$, $z_1$) or 62 ($z_2$, $z_3$, $z_4$) built from LFSRs, and different sequences separate parameter sets with the same block size.

The code on this page is for study only. It is not constant time as Python runs it, and it must not protect real data. Use a vetted cipher from libsodium, OpenSSL or a FIPS 140 validated module.

## Example

SIMON64/128 with the key 1b1a1918 13121110 0b0a0908 03020100 ($k_3, k_2, k_1, k_0$) and the plaintext $(x, y) = $ (656b696c, 20646e75), the vector of the paper's appendix.

| step | value |
|---|---|
| round keys $k_0, \ldots, k_3$ | 03020100, 0b0a0908, 13121110, 1b1a1918 |
| round keys $k_4, k_5$ | 70a011c3, b770ec49 |
| round 1: $f(x)$ | dfede5f1 |
| round 1: $(x, y)$ | (fc8b8a84, 656b696c) |
| round 2: $f(x)$ | 7b2c2e1b |
| round 2: $(x, y)$ | (154d4e7f, fc8b8a84) |
| after 44 rounds | (44c8fc20, b9dfa07a) |

In round 1, the new $x$ is $y \oplus f(x) \oplus k_0 = $ 20646e75 $\oplus$ dfede5f1 $\oplus$ 03020100 $=$ fc8b8a84. The tests check the paper's vectors for SIMON32/64, 48/72, 48/96, 64/128, 128/128 and 128/256, which use all five sequences $z_0$ to $z_4$, and a round trip for all ten parameter sets.

## Correctness

One round maps $(x, y)$ to $(y \oplus f(x) \oplus k, x)$. Given the output $(x', y')$, we have $x = y'$, and then $y = x' \oplus f(y') \oplus k$. Line L7 computes exactly this, so it inverts line L3 for the same round key. Decryption runs the rounds in the reverse order with the same round keys, so it inverts encryption. This holds for each $f$: a Feistel network is invertible even when its round function is not. The proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

Each round costs three rotations, one AND and three XORs on $n$-bit words, and each key schedule step a few rotations and XORs. So a block costs $\Theta(T)$ word operations and $b$ blocks cost $\Theta(b T)$. Storing the round keys takes $\Theta(T)$ words; a hardware design can compute them on the fly with $m$ words of state. A bit-serial hardware design processes one bit per clock and needs only a few gates per bit of state; the paper compares these areas with those of other lightweight block ciphers.

## Properties

- **Ten parameter sets**, from SIMON32/64 to SIMON128/256, named block size/key size.
- **Feistel structure.** Decryption uses the same round function and reversed round keys.
- **No S-boxes and no additions.** AND, XOR and rotation only. This suits hardware and [bit-sliced](/bit-slicing/) software, and it has no table-lookup timing leaks.
- **Bit-serial friendly.** The round function acts on each bit position with the same small circuit, so a design can process one bit per clock.
- **Late rationale.** The 2013 paper gave no security analysis; the designers' notes of 2017 gave the reasons for the rotation amounts and the round counts.

## Variants and improvements

- **[SPECK](/speck/)** is the software-oriented sister family from the same paper. It replaces the AND-based Feistel round by an ARX round (addition modulo $2^n$, rotation, XOR), and its key schedule reuses the round function. SIMON is the smaller of the two in hardware; SPECK is faster on most processors.
- **SIMECK** (2015) by other authors combines the SIMON round with a key schedule built from the round function, as in SPECK, and other rotation amounts.
- **Cryptanalysis.** Differential, linear, impossible differential and integral attacks reach a large part of the rounds of each member, but none breaks a full member. The designers' notes list the attacks known to them.

## When to use it

SIMON may suit a hardware design with a very small area budget where a 64-bit or 128-bit block cipher is enough. Many users avoid it because of the lack of public rationale at publication and its origin, and because it did not become an ISO/IEC standard. For new designs, [Ascon](/ascon/), the NIST lightweight standard of SP 800-232, gives authenticated encryption with public analysis; [PRESENT](/present/) is the ISO/IEC 29192-2 option among small block ciphers.

## Pitfalls

- **Word order.** The paper writes the key as $k_{m-1}, \ldots, k_0$ and the block as $(x, y)$ with $x$ first. Code that loads bytes in another order gives different results; check the vectors.
- **Reading $z_j$.** Bit $r$ of $z_j$ is the $r$-th bit from the left of the sequence as printed. Some code stores the sequence reversed, as a number with bit 0 on the right; mixing the two conventions breaks the key schedule.
- **The extra term for $m = 4$.** Only key sizes with four words XOR $k_{i-3}$ into $t$.
- **Small blocks.** SIMON32 has a 32-bit block, so the [birthday bound](/birthday-attack/) is reached after about $2^{16}$ blocks. It suits only tiny amounts of data per key.

## Implementations

## History

A team of the US National Security Agency designed SIMON and SPECK and posted them to the IACR ePrint archive in June 2013. The paper gave the specification, hardware and software results and test vectors, but no security analysis, and this drew criticism. Academic cryptanalysis followed, and the designers posted design notes in 2017. The NSA also proposed SIMON and SPECK for ISO/IEC 29192-2. After objections from several national bodies, about the missing analysis and the security margin, the project was stopped in 2018, as told by Ashur and Luykx.

## References
