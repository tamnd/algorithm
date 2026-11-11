---
tag: 6XMTK8
kind: algorithm
slug: a5-1
name: A5/1
aliases:
- A5/1 cipher
area: cryptography/symmetric-ciphers
level: intro
summary: The GSM voice cipher. Three short LFSRs of 19, 22 and 23 bits move by a majority rule and XOR their top bits. Public attacks recover the 64-bit state, so A5/1 is broken.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of keystream bits}
  time: {worst: Θ(n + 186), average: Θ(n + 186), best: Θ(n + 186)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 1999
  people: [Marc Briceno, Ian Goldberg, David Wagner]
  note: Designed for GSM in the late 1980s and kept secret. The year and the people are those of the 1999 reverse-engineered publication. Practical attacks followed from 1997 to 2010.
prereqs: [stream-cipher, lfsr]
see_also: [lfsr, stream-cipher, time-memory-tradeoff, rainbow-table, known-plaintext-attack, ciphertext-only-attack, trivium, snow-3g]
sources:
  - url: "http://cryptome.org/jya/a51-pi.htm"
    title: "Marc Briceno, Ian Goldberg and David Wagner, A pedagogical implementation of the GSM A5/1 and A5/2 voice privacy encryption algorithms, 1999"
    locator: the C code (register lengths, tap masks, clocking bits, key and frame loading, the 100 mixing clocks) and its test vector
  - paper: "Jovan Dj. Golić, Cryptanalysis of alleged A5 stream cipher, EUROCRYPT 1997, LNCS 1233, pp. 239-255"
    locator: the description of the generator and the guess-and-determine and time-memory trade-off attacks
  - paper: "Alex Biryukov, Adi Shamir and David Wagner, Real time cryptanalysis of A5/1 on a PC, FSE 2000, LNCS 1978, pp. 1-18"
    locator: the attacks that run on a single PC after a one-time preparation of about 2^48 steps
  - paper: "Elad Barkan, Eli Biham and Nathan Keller, Instant ciphertext-only cryptanalysis of GSM encrypted communication, CRYPTO 2003, LNCS 2729, pp. 600-616"
    locator: the use of the error-correcting code applied before encryption to get ciphertext-only attacks, and the active attacks on the GSM protocol
  - paper: "Karsten Nohl, Attacking phone privacy, Black Hat USA 2010, white paper"
    locator: the public A5/1 rainbow tables and the practical decryption of GSM calls
---

A5/1 is the [stream cipher](/stream-cipher/) that protects GSM voice and data on the radio link between a phone and the base station. It is built from three short [linear feedback shift registers](/lfsr/) of 19, 22 and 23 bits, 64 bits in total. At each clock a majority rule decides which registers move, and the output bit is the XOR of the top bits of the three registers. The design was secret, but it was reverse-engineered and published in 1999. Attacks from 1997 to 2010 made the recovery of its state practical, and A5/1 is now broken.

## In plain words

Take three short rows of bits. Each row can move one place: the bits shift up, the top bit falls out, and a new bottom bit is the XOR of a few fixed bits of the row. Each row has one marked bit near the middle. At each step, look at the three marked bits. Two or three of them agree. Every row whose marked bit agrees with the majority moves, and the other row stays. Then XOR the top bits of the three rows. That is one keystream bit. The key and the frame number fill the rows before the first output bit.

## The problem

The input is a 64-bit session key $K$, a 22-bit frame number $f$ and a number $n$. The output is $n$ keystream bits. GSM uses $n = 228$ for each frame: the first 114 bits encrypt the burst from the network to the phone and the next 114 bits encrypt the burst back. The phone gets $K$ from the SIM card, and a new frame number makes a new keystream for each frame.

In the notation of this area, $A$ is an adversary and $\mathrm{Adv}$ its advantage. The goal was that no efficient $A$ that sees keystream for known frame numbers finds $K$ or tells the keystream apart from random bits with a large advantage. A5/1 does not reach this goal.

## The algorithm

$R_1$, $R_2$ and $R_3$ are the registers, with bit 0 at the bottom. The table gives the lengths, the feedback taps, the clocking bit $c_j$ and the output bit.

| register | length | feedback taps | clocking bit | output bit |
|---|---|---|---|---|
| $R_1$ | 19 | 18, 17, 16, 13 | 8 | 18 |
| $R_2$ | 22 | 21, 20 | 10 | 21 |
| $R_3$ | 23 | 22, 21, 20, 7 | 10 | 22 |

```pseudo id=main
A5/1(K, f, n)
L1  R1 ← R2 ← R3 ← 0
L2  for i ← 0 to 63: STEP each of R1, R2, R3; XOR key bit k_i into bit 0 of each
L3  for i ← 0 to 21: STEP each of R1, R2, R3; XOR frame bit f_i into bit 0 of each
L4  repeat 100 times: MAJORITY-CLOCK()                     ▷ output discarded
L5  for t ← 1 to n: MAJORITY-CLOCK(); output z_t ← R1[18] ⊕ R2[21] ⊕ R3[22]

MAJORITY-CLOCK()
L6  m ← majority(R1[8], R2[10], R3[10])
L7  for j ← 1 to 3: if R_j[c_j] = m then STEP(R_j)

STEP(R)
L8  t ← XOR of the tap bits of R;  R ← (R << 1) | t, cut to the length of R
```

Lines L2 and L3 move all three registers at each step and mix in the key and then the frame number, one bit at a time and least significant bit first. Line L4 makes 100 majority clocks with no output, so that the first output bit depends on all key bits. Line L5 gives one bit for each majority clock. Line L6 takes the value that at least two of the three clocking bits have. Line L7 moves the registers that agree with it, so two or three registers move at each clock.

The code on this page is for study only. It is not constant time as Python runs it, and it must not protect real data. A5/1 is broken. For new designs use a vetted AEAD such as AES-GCM or ChaCha20-Poly1305 from libsodium, OpenSSL or a FIPS 140 validated module.

## Example

Take the test vector of the 1999 pedagogical implementation: key bytes 12 23 45 67 89 AB CD EF and frame number 0x134. This vector is not an official ETSI vector, because the GSM specifications of A5/1 are not public. After line L2 the registers are $R_1$ = 0x04030D, $R_2$ = 0x1FA05C, $R_3$ = 0x3668E1. After line L3 they are 0x0064A2, 0x2BC0E5, 0x72DF8D, and after line L4 they are 0x01DA4B, 0x2CB2F9, 0x08BE5F. The table traces the first clocks of line L5.

| $t$ | clocking bits $R_1[8], R_2[10], R_3[10]$ | majority | registers that move | $R_1$, $R_2$, $R_3$ after the clock | $z_t$ |
|---|---|---|---|---|---|
| 1 | 0, 0, 1 | 0 | $R_1$, $R_2$ | 03B497, 1965F3, 08BE5F | 0 |
| 2 | 0, 1, 1 | 1 | $R_2$, $R_3$ | 03B497, 32CBE7, 117CBE | 1 |
| 3 | 0, 0, 1 | 0 | $R_1$, $R_2$ | 07692F, 2597CE, 117CBE | 0 |
| 4 | 1, 1, 1 | 1 | all three | 06D25E, 0B2F9D, 22F97C | 1 |
| 5 | 0, 1, 0 | 0 | $R_1$, $R_3$ | 05A4BC, 0B2F9D, 45F2F9 | 0 |
| 6 | 0, 1, 0 | 0 | $R_1$, $R_3$ | 034979, 0B2F9D, 0BE5F2 | 0 |
| 7 | 1, 1, 1 | 1 | all three | 0692F2, 165F3A, 17CBE5 | 1 |
| 8 | 0, 1, 0 | 0 | $R_1$, $R_3$ | 0525E4, 165F3A, 2F97CA | 1 |

The first eight bits are 01010011, the byte 0x53. Packed most significant bit first, the 114 bits from the network to the phone are 534EAA582FE8151AB6E1855A728C00 and the 114 bits back are 24FD35A35D5FB6526D32F906DF1AC0, as in the pedagogical code.

## Correctness

Lines L1 to L8 are deterministic functions of $K$ and $f$, so the phone and the network compute the same $z_t$, and $(m \oplus z) \oplus z = m$. At each clock of line L7 at least two registers move, because at least two of the three clocking bits equal the majority. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- Setup is 64 + 22 + 100 = 186 clocks, and $n$ bits cost $\Theta(n + 186)$ clocks.
- Each clock is a constant number of bit operations on three short registers. In hardware a clock is a few gates and one cycle.
- The state is 64 bits.

## Properties

- **Each register alone is weak.** Each feedback polynomial is primitive, so a register that moves at every step has period $2^{L} - 1$ for its length $L$. A linear register alone falls to the [Berlekamp-Massey](/berlekamp-massey/) algorithm.
- **Irregular clocking.** The majority rule makes the registers move unevenly. For random clocking bits, each register moves with probability 3/4. This is the only nonlinear part of the design.
- **The state is small.** The full state is 64 bits, and the frame number is public and known for each frame. The state after line L3 is a linear function of $K$ and $f$ over GF(2). So an attacker who recovers the state of one frame can step back through the 100 majority clocks, which leaves only a few candidates, and solve linear equations for $K$. Then all frames of the session can be decrypted.
- **Known attacks.** Golić (1997) gave a guess-and-determine attack and a time-memory trade-off. Biryukov, Shamir and Wagner (2000) showed attacks that run on a PC in real time after a one-time preparation of about $2^{48}$ steps. Barkan, Biham and Keller (2003) used the GSM error-correcting code, which is applied before encryption, to get known linear relations among plaintext bits and so ciphertext-only attacks. In 2010 Nohl and others published A5/1 [rainbow tables](/rainbow-table/), which made the decryption of GSM calls practical with ordinary hardware. These are forms of the [time-memory trade-off](/time-memory-tradeoff/).

## Variants and improvements

- **A5/2.** A weaker export version with a fourth register that controls the clocking. It is broken much more easily, and the GSM Association withdrew it.
- **A5/3 and GEA3.** Later GSM and GPRS ciphers based on the KASUMI block cipher.
- **3G and 4G.** UMTS and LTE use KASUMI, [SNOW 3G](/snow-3g/), AES and [ZUC](/zuc/) with longer keys and mutual authentication.

## When to use it

Do not use A5/1 to protect data. Implement it only to interoperate with old GSM networks, to analyze GSM traffic with permission, or to study the attacks.

## Pitfalls

- **Bit order.** The pedagogical code loads key bit $i$ from bit $i \bmod 8$ of byte $\lfloor i/8 \rfloor$, least significant bit first, and packs output bits most significant bit first. Mixing these up gives different vectors.
- **Clocking before mixing.** In lines L2 and L3 the register moves first and then the key or frame bit is XORed into bit 0.
- **The 100 mixing clocks.** They use the majority rule, not the regular clock of lines L2 and L3.
- **Keystream reuse.** The keystream depends only on $K$ and $f$. If the frame number repeats under the same key, the keystream repeats, as with a reused [one-time pad](/one-time-pad/).

## Implementations

## History

A5/1 was designed for GSM in the late 1980s and kept secret. Approximate descriptions leaked in 1994. In 1999 Briceno, Goldberg and Wagner published a pedagogical implementation that they reverse-engineered from a GSM phone. Golić had already analyzed the leaked design at EUROCRYPT 1997. Biryukov, Shamir and Wagner gave real-time attacks at FSE 2000, Barkan, Biham and Keller gave ciphertext-only and active attacks at CRYPTO 2003, and Nohl presented practical rainbow table attacks at Black Hat USA 2010. Many networks still offer A5/1 for old phones, and 3G and 4G networks use stronger ciphers.

## References
