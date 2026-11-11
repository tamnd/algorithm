---
tag: ADV21B
kind: algorithm
slug: present
name: PRESENT
area: cryptography/symmetric-ciphers
level: advanced
summary: An ultra-lightweight SPN block cipher (CHES 2007) with a 64-bit block, an 80 or 128-bit key, one 4-bit S-box and a bit permutation, in 31 rounds. It is in ISO/IEC 29192-2.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of 64-bit blocks}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2007
  people: [Andrey Bogdanov, Lars R. Knudsen, Gregor Leander, Christof Paar, Axel Poschmann, Matthew J. B. Robshaw, Yannick Seurin, Charlotte Vikkelsoe]
  note: PRESENT was presented at CHES 2007 as a block cipher for RFID tags and sensors, with about 1570 gate equivalents for the 80-bit version. ISO/IEC 29192-2 standardized it in 2012.
prereqs: [substitution-permutation-network, s-box, block-cipher]
see_also: [lightweight-cryptography, substitution-permutation-network, s-box, differential-cryptanalysis, linear-cryptanalysis, simon-cipher, speck, bit-slicing]
sources:
  - paper: "Andrey Bogdanov, Lars R. Knudsen, Gregor Leander, Christof Paar, Axel Poschmann, Matthew J. B. Robshaw, Yannick Seurin and Charlotte Vikkelsoe, PRESENT: An ultra-lightweight block cipher, Cryptographic Hardware and Embedded Systems (CHES 2007), LNCS 4727, pages 450 to 466"
    locator: Section 3 (the round function, the S-box, the permutation P(i) = 16 i mod 63 and the key schedules), Section 4 (the design criteria of the S-box), Sections 5 and 6 (security and hardware), and the appendix with the test vectors of PRESENT-80
  - paper: "ISO/IEC 29192-2:2012, Information technology, Security techniques, Lightweight cryptography, Part 2: Block ciphers"
    locator: the clause on PRESENT, a lightweight block cipher with a 64-bit block and keys of 80 or 128 bits
  - paper: "Joo Yeon Cho, Linear cryptanalysis of reduced-round PRESENT, Topics in Cryptology (CT-RSA 2010), LNCS 5985"
    locator: the multidimensional linear attack on 26 of the 31 rounds of PRESENT
---

PRESENT is a lightweight [block cipher](/block-cipher/) with a 64-bit block and an 80-bit or 128-bit key, by Bogdanov, Knudsen, Leander, Paar, Poschmann, Robshaw, Seurin and Vikkelsoe (CHES 2007). It is a [substitution-permutation network](/substitution-permutation-network/) of 31 rounds. Each round XORs a round key, applies one 4-bit [S-box](/s-box/) sixteen times in parallel, and moves the 64 bits by a fixed permutation that costs only wires in hardware. The 80-bit version needs about 1570 gate equivalents, which made it a reference point of [lightweight cryptography](/lightweight-cryptography/). PRESENT is in ISO/IEC 29192-2. This page implements PRESENT-80.

## In plain words

PRESENT encrypts 8 bytes at a time. It holds the block as 64 bits and repeats a simple round 31 times. First it mixes in a round key with XOR. Then it cuts the block into 16 groups of 4 bits and replaces each group by a fixed table of 16 entries. Then it moves every bit to a new place by a fixed rule, so the 4 bits of one group go to four different groups in the next round. After the last round it mixes in one more key. The round keys come from the main key: it rotates the key, puts a few bits through the same table and adds the round number. In a chip, the table is a small circuit and the bit move is only wiring, so the whole cipher is very small.

## The problem

Encrypt a 64-bit block under an 80-bit key with a keyed permutation that is secure against known attacks, and that is as small as possible in hardware: few gates, low power, and a modest speed. The target is devices such as RFID tags and sensor nodes, where AES costs too much area.

## The algorithm

Number the bits of the 64-bit state $b_{63} \ldots b_0$, with $b_0$ the least significant bit. The S-box $S$ in hexadecimal is

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $S(x)$ | C | 5 | 6 | B | 9 | 0 | A | D | 3 | E | F | 8 | 4 | 7 | 1 | 2 |

The permutation moves bit $i$ to bit $P(i) = 16 i \bmod 63$ for $0 \le i \le 62$, and $P(63) = 63$.

**Key schedule of PRESENT-80.** Hold the key in an 80-bit register $k_{79} \ldots k_0$. Round key $K_i$ is the leftmost 64 bits $k_{79} \ldots k_{16}$. After extracting $K_i$, for $i = 1, \ldots, 31$: rotate the register left by 61 places; replace $k_{79} \ldots k_{76}$ by $S(k_{79} \ldots k_{76})$; and XOR the 5-bit round counter $i$ into $k_{19} \ldots k_{15}$. PRESENT-128 uses a 128-bit register, two S-boxes on the top 8 bits and the counter in $k_{66} \ldots k_{62}$.

```pseudo id=main
PRESENT-ENCRYPT(state, key)
L1  K1, ..., K32 ← KEY-SCHEDULE(key)
L2  for i ← 1 to 31 do
L3      state ← state ⊕ Ki                         ▷ addRoundKey
L4      state ← S applied to each of the 16 nibbles   ▷ sBoxLayer
L5      state ← bit i moved to bit P(i), for each i   ▷ pLayer
L6  return state ⊕ K32

PRESENT-DECRYPT(state, key)
L7  K1, ..., K32 ← KEY-SCHEDULE(key)
L8  state ← state ⊕ K32
L9  for i ← 31 downto 1 do
L10     state ← bit P(i) moved to bit i, for each i
L11     state ← S⁻¹ applied to each nibble
L12     state ← state ⊕ Ki
L13 return state
```

The S-box gives the nonlinearity. Its design criteria (Section 4 of the paper) are: each nonzero input difference gives each output difference at most 4 times out of 16, a single-bit input difference never gives a single-bit output difference, and each linear approximation has a bias of at most $1/4$. The permutation sends the four output bits of each S-box to four different S-boxes of the next round, and the four input bits of each S-box come from four different S-boxes. With the S-box property, the paper shows that each 5-round differential characteristic has at least 10 active S-boxes. The key schedule's S-box and round counter make the round keys differ, which stops slide attacks.

The code on this page is for study only. It is not constant time as Python runs it, and it must not protect real data. Use a vetted cipher from libsodium, OpenSSL or a FIPS 140 validated module.

## Example

Encrypt the zero block with the zero 80-bit key. The first round keys are $K_1 = $ 0000000000000000, $K_2 = $ c000000000000000 and $K_3 = $ 5000180000000001, and the last is $K_{32} = $ 6dab31744f41d700.

| step | state |
|---|---|
| plaintext | 0000000000000000 |
| round 1, after line L3 ($\oplus K_1$) | 0000000000000000 |
| round 1, after line L4 ($S(0) = \mathrm{C}$) | cccccccccccccccc |
| round 1, after line L5 | ffffffff00000000 |
| after 31 rounds and line L6 | 5579c1387b228445 |

In round 1, each nibble is C, binary 1100, so bits $4j + 2$ and $4j + 3$ are set for $j = 0, \ldots, 15$. The permutation sends bit $4j + 2$ to $(64j + 32) \bmod 63 = j + 32$ and bit $4j + 3$ to $j + 48$, which sets bits 32 to 63. The final ciphertext matches the appendix of the paper. The other three vectors there (pairs of all-zero and all-one blocks and keys) give e72c46c0f5945049, a112ffc72f68417b and 3333dcd3213210d2, and the tests check all four.

## Correctness

Each step of a round has an inverse: XOR with $K_i$ is its own inverse, $S$ is a bijection of $\{0,1\}^4$ (its table has 16 different entries), so the S-box layer is a bijection, and $P$ is a bijection of the bit positions. For $P$, the map $i \mapsto 16 i \bmod 63$ is a bijection of $\{0, \ldots, 62\}$ because $\gcd(16, 63) = 1$, and $P(63) = 63$. Decryption applies the inverse steps in the reverse order with the same round keys, so it inverts encryption. Because $16^3 = 4096 \equiv 1 \pmod{63}$, $P$ applied three times is the identity, and the tests check this. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

A block costs 31 rounds of 16 S-box lookups and a 64-bit permutation, so $\Theta(1)$ per block and $\Theta(n)$ for $n$ blocks. The key schedule is 31 steps on an 80-bit register. In hardware, the paper's round-based PRESENT-80 takes about 1570 gate equivalents and 32 clock cycles per block. In software, the bit permutation is slow when done bit by bit, as here; [bit-sliced](/bit-slicing/) or table-based code is much faster.

## Properties

- **Block and keys.** A 64-bit block; an 80-bit key (PRESENT-80) or a 128-bit key (PRESENT-128); 31 rounds and 32 round keys.
- **One small S-box.** The same 4-bit S-box in all 16 positions and in the key schedule, so a chip needs one S-box circuit for a serial design.
- **A wiring permutation.** The bit permutation costs no gates.
- **Wide trail bounds.** At least 10 active S-boxes over 5 rounds gives a bound of $2^{-20}$ on each 5-round differential characteristic, so the 31 rounds have a large margin against classic [differential](/differential-cryptanalysis/) and [linear cryptanalysis](/linear-cryptanalysis/).
- **Encryption only is cheap.** In CTR mode or as part of a MAC, only the encryption circuit is needed.

## Variants and improvements

- **PRESENT-128** has the same round function and a 128-bit key schedule. The paper suggests it for higher security levels.
- **Attacks.** The best attacks reach reduced rounds. A multidimensional linear attack breaks 26 of the 31 rounds of PRESENT-80 (Cho, 2010). No practical attack on the full 31 rounds is known.
- **Later lightweight block ciphers** such as [SIMON](/simon-cipher/), [SPECK](/speck/), SKINNY and GIFT followed PRESENT. GIFT keeps the idea of a 4-bit S-box and a bit permutation, with a smaller S-box cost.
- **Lightweight AEAD.** The NIST process ended with [Ascon](/ascon/), a permutation-based design, rather than a block cipher in a mode.

## When to use it

Use PRESENT where a standard, very small block cipher is needed in hardware, such as RFID tags or sensors that must meet ISO/IEC 29192-2, and where the 64-bit block is acceptable for the amount of data. Change the key well before $2^{32}$ blocks because of the [birthday bound](/birthday-attack/). In software on a general processor, AES (often with hardware support) or [Ascon](/ascon/) is faster and safer. For new designs that need authenticated encryption on small devices, prefer [Ascon](/ascon/), as in NIST SP 800-232.

## Pitfalls

- **Bit numbering.** The paper numbers bits from the right, with bit 0 the least significant. Code that numbers from the left gets a different permutation and wrong vectors.
- **The round counter.** It is XORed into $k_{19} \ldots k_{15}$ of the 80-bit register, after the rotation and the S-box. A counter from 0 or at other bits gives a different cipher.
- **The last key addition.** There are 31 rounds and 32 round keys. Code that stops after round 31 without line L6 is wrong.
- **Table lookups in software.** An S-box in a table indexed by secret data can leak through cache timing. Use bit-sliced code where timing matters.
- **The 64-bit block.** As for every 64-bit cipher, large amounts of data under one key leak information through block collisions.

## Implementations

## History

The authors, from Ruhr University Bochum, the Technical University of Denmark and Orange Labs, presented PRESENT at CHES 2007 in Vienna. They wanted a cipher for passive RFID tags and similar devices, where the area budget is a few thousand gates. The design used a 4-bit S-box in the manner of Serpent, and chose a 64-bit block and an 80-bit key as enough for the target. PRESENT became one of the most analysed lightweight ciphers, and in 2012 it entered ISO/IEC 29192-2, the part of the lightweight cryptography standard for block ciphers. It also helped start the line of research that led to the NIST lightweight cryptography process.

## References
