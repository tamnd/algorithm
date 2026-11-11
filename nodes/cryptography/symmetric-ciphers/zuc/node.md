---
tag: MQAR4N
kind: algorithm
slug: zuc
name: ZUC
aliases:
- ZUC-128
area: cryptography/symmetric-ciphers
level: advanced
summary: A word-oriented stream cipher from China with a 16-cell LFSR over the prime field GF(2^31-1), a bit reorganization and a nonlinear function F. It is the core of 128-EEA3 and 128-EIA3 in LTE.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of 32-bit keystream words}
  time: {worst: Θ(n + 33), average: Θ(n + 33), best: Θ(n + 33)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2010
  people: [DACAS, Chinese Academy of Sciences]
  note: Published by ETSI/SAGE as version 1.0 in June 2010. Version 1.5 of January 2011 changed the initialization after a chosen-IV attack on version 1.4. 3GPP adopted it for LTE as 128-EEA3 and 128-EIA3.
prereqs: [stream-cipher, lfsr]
see_also: [snow-3g, lfsr, stream-cipher, advanced-encryption-standard, s-box, message-authentication-code, a5-1]
sources:
  - paper: "ETSI/SAGE, Specification of the 3GPP Confidentiality and Integrity Algorithms 128-EEA3 & 128-EIA3, Document 2: ZUC Specification, Version 1.6, 28 June 2011"
    locator: Section 3 (the LFSR, the bit-reorganization, the function F, key loading and execution) and the Document History (version 1.5, 4 January 2011, a modification of ZUC in the initialization)
  - paper: "ETSI/SAGE, Specification of the 3GPP Confidentiality and Integrity Algorithms 128-EEA3 & 128-EIA3, Document 3: Implementor's Test Data, Version 1.1, 4 January 2011"
    locator: Sections 3.3 to 3.6 (ZUC test sets 1 to 4)
  - paper: "Hongjun Wu, Tao Huang, Phuong Ha Nguyen, Huaxiong Wang and San Ling, Differential attacks against stream cipher ZUC, ASIACRYPT 2012, LNCS 7658, pp. 262-277"
    locator: the chosen-IV attacks on ZUC 1.4, whose initialization is not injective, and the injective fix used in later versions
---

ZUC is a word-oriented [stream cipher](/stream-cipher/) designed in China and published by ETSI/SAGE in 2010 for 3GPP mobile networks. It takes a 128-bit key and a 128-bit IV and outputs one 32-bit keystream word per clock. It has three layers: a linear feedback shift register of 16 cells over the prime field $\mathrm{GF}(2^{31} - 1)$, a bit reorganization that takes 128 bits from the register, and a nonlinear function $F$ with two 32-bit memory cells. ZUC is the core of the LTE algorithms 128-EEA3 (encryption) and 128-EIA3 (integrity). Its name honors the fifth-century mathematician Zu Chongzhi.

## In plain words

ZUC has three parts. The first is a row of 16 numbers, each between 1 and $2^{31} - 1$. At each clock the row moves one place, and a new number goes in at the end: a fixed sum of five old numbers, each multiplied by a power of 2, modulo the prime $2^{31} - 1$. The second part cuts 16-bit halves out of eight of these numbers and glues them into four 32-bit words. The third part is a small machine with two words of memory. It mixes three of the glued words with its memory by XOR and integer addition, then passes the result through linear maps and S-boxes. Its output XOR the fourth glued word is one keystream word.

## The problem

The input is a key $k = k_0 \| \ldots \| k_{15}$ and an IV $iv = iv_0 \| \ldots \| iv_{15}$, each 16 bytes, and a number $n$. The output is the keystream $Z_1, \ldots, Z_n$ of 32-bit words. 128-EEA3 XORs the keystream with the data, and 128-EIA3 uses it to compute a MAC.

In the notation of this area, $K$ is the key, $A$ an adversary and $\mathrm{Adv}$ its advantage. The goal is that for a secret random $K$, no efficient $A$ that chooses IVs tells the keystreams apart from uniform words with a large advantage. The target is 128-bit security.

## The algorithm

The LFSR cells $s_0, \ldots, s_{15}$ are 31-bit integers in $\{1, \ldots, 2^{31} - 1\}$, and $p = 2^{31} - 1$. For a cell $s_i$, $s_{iH}$ is bits 30 to 15 and $s_{iL}$ is bits 15 to 0. $\boxplus$ is addition modulo $2^{32}$, $\oplus$ is XOR, and $\lll$ is a 32-bit left rotation.

```pseudo id=main
ZUC(k, iv, n)
L1  for i ← 0 to 15: s_i ← k_i ‖ d_i ‖ iv_i;  R1 ← R2 ← 0     ▷ d_i: 15-bit constants
L2  repeat 32 times                                         ▷ initialization stage
L3      BR();  W ← F(X0, X1, X2)
L4      LFSR-CLOCK(W >> 1)
L5  BR();  F(X0, X1, X2)                                    ▷ output discarded
L6  LFSR-CLOCK(0)
L7  for t ← 1 to n do                                       ▷ working stage
L8      BR()           ▷ X0 ← s15H‖s14L, X1 ← s11L‖s9H, X2 ← s7L‖s5H, X3 ← s2L‖s0H
L9      output Z_t ← F(X0, X1, X2) ⊕ X3
L10     LFSR-CLOCK(0)

F(X0, X1, X2)
L11 W ← (X0 ⊕ R1) ⊞ R2
L12 W1 ← R1 ⊞ X1;  W2 ← R2 ⊕ X2
L13 R1 ← S(L1(W1L ‖ W2H));  R2 ← S(L2(W2L ‖ W1H));  return W

LFSR-CLOCK(u)
L14 v ← 2^15 s15 + 2^17 s13 + 2^21 s10 + 2^20 s4 + (1 + 2^8) s0 + u mod p;  if v = 0 then v ← p
L15 (s_0, ..., s_15) ← (s_1, ..., s_15, v)
```

Line L1 loads each cell with a key byte (bits 30 to 23), a 15-bit constant $d_i$ (bits 22 to 8) and an IV byte (bits 7 to 0). The constants are $d_0$ = 0x44D7, $d_1$ = 0x26BC, up to $d_{15}$ = 0x47AC. Lines L2 to L4 run 32 clocks in which the output $W$ of $F$, shifted right by one bit to fit 31 bits, is added into the new cell. Lines L5 and L6 make one clock with the output discarded. Then each clock of lines L7 to L10 gives one word.

Line L8 is the bit reorganization. It joins 16-bit halves of eight cells into four 32-bit words. Line L13 uses two linear maps, $L_1(X) = X \oplus (X \lll 2) \oplus (X \lll 10) \oplus (X \lll 18) \oplus (X \lll 24)$ and $L_2(X) = X \oplus (X \lll 8) \oplus (X \lll 14) \oplus (X \lll 22) \oplus (X \lll 30)$, and the S-box $S = (S_0, S_1, S_0, S_1)$, which applies two fixed $8 \times 8$ S-boxes to the four bytes. Line L14 needs no multiplier: multiplying a 31-bit value by $2^j$ modulo $2^{31} - 1$ is a 31-bit left rotation by $j$, so the sum is five rotations and additions with an end-around carry. A result of 0 is stored as $p$, which is the same element of the field, so a cell is never the all-zero word.

The code on this page is for study only. It is not constant time as Python runs it, because it uses table lookups, and it must not protect real data. Network equipment uses validated implementations of 128-EEA3. For general use, take a vetted AEAD such as AES-GCM or ChaCha20-Poly1305 from libsodium, OpenSSL or a FIPS 140 validated module.

## Example

Take Test Set 1 of the ETSI/SAGE Implementor's Test Data: the zero key and the zero IV. Line L1 gives $s_i = d_i \cdot 2^8$, so $s_0$ = 0044d700 and $s_{15}$ = 0047ac00. The table shows the first clocks of lines L2 to L4: the words of the bit reorganization, the memory after $F$, the output $W$ and the new cell $s_{15}$.

| $t$ | $X_0$ | $X_1$ | $X_2$ | $R_1$ | $R_2$ | $W$ | new $s_{15}$ |
|---|---|---|---|---|---|---|---|
| 0 | 008f9a00 | f100005e | af00006b | 67822141 | 62a3a55f | 008f9a00 | 4563cb1b |
| 1 | 8ac7ac00 | 260000d7 | 780000e2 | 474a2e7e | 119e94bb | 4fe932a0 | 28652a0f |
| 2 | 50cacb1b | 4d000035 | 13000013 | c29687a5 | e9b6eb51 | 291f7a20 | 7464f744 |

At $t = 0$, $s_{15H}$ = 0x008f (bits 30 to 15 of 0047ac00) and $s_{14L}$ = 0x9a00 (bits 15 to 0 of 00789a00), so $X_0$ = 008f9a00. $R_1 = R_2 = 0$, so line L11 gives $W = X_0$. At $t = 1$ the high half of $X_0$ is 0x8ac7, the top 16 bits of the new cell 4563cb1b. The rows match Section 3.3 of the test data. After the 33 clocks, the output is $Z_1$ = 27bede74 and $Z_2$ = 018082da.

## Correctness

Lines L1 to L15 are deterministic functions of $k$ and $iv$, so both sides compute the same $Z_t$, and $(m \oplus Z) \oplus Z = m$. Line L14 keeps each cell in $\{1, \ldots, p\}$, so each cell is a valid 31-bit value and line L8 reads defined bits. In the working stage the update is invertible: $s_0$ can be solved from $v$ because $1 + 2^8$ is invertible modulo $p$, and $R_1, R_2$ can be solved because $S$, $L_1$ and $L_2$ are bijections. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- One clock is a constant number of word operations: the five-term sum of line L14, two additions modulo $2^{32}$, four rotations for each of $L_1$ and $L_2$, and eight byte S-box lookups.
- Initialization is 33 clocks for each IV, and $n$ words cost $\Theta(n + 33)$ clocks.
- The state is 16 cells of 31 bits and two 32-bit words, 560 bits.

## Properties

- **A prime-field LFSR.** Unlike the GF(2) and $\mathrm{GF}(2^{32})$ LFSRs of [LFSR](/lfsr/) and [SNOW 3G](/snow-3g/), the ZUC register works modulo the prime $2^{31} - 1$. Its sequence is linear over $\mathrm{GF}(p)$ but not over GF(2), because the modular additions carry. This makes the linear attacks that work over GF(2) harder.
- **The bit reorganization.** It mixes halves of cells that are far apart in the register, and it crosses the boundary between the prime-field world and the GF(2) world of $F$.
- **The function F.** $L_1$ and $L_2$ are the diffusion layers, and $S_0$ and $S_1$ give the nonlinearity. The memory cells $R_1$ and $R_2$ carry state from clock to clock.
- **The change in version 1.5.** Wu, Huang, Nguyen, Wang and Ling showed that the initialization of ZUC 1.4 is not injective, so a difference in the IV can cancel. Their chosen-IV attack finds two IVs with identical keystreams for about one key in $2^{15.4}$, a keystream reuse. Version 1.5 (4 January 2011) changed the LFSR update during the initialization to be injective. The algorithm on this page, versions 1.5 and 1.6, resists these attacks.

## Variants and improvements

- **128-EEA3 and 128-EIA3.** 128-EEA3 builds the IV from the counter COUNT, the BEARER identity and the DIRECTION bit, and XORs the keystream with the data. 128-EIA3 uses the keystream to compute a 32-bit MAC. In LTE they sit next to the [SNOW 3G](/snow-3g/) based 128-EEA1 and 128-EIA1 and the [AES](/advanced-encryption-standard/) based 128-EEA2 and 128-EIA2.
- **ZUC-256.** A 2018 version with a 256-bit key and a longer initialization, proposed for 5G.

## When to use it

Use ZUC when a 3GPP protocol or a Chinese standard requires 128-EEA3 or 128-EIA3. It is not a general-purpose cipher in common libraries, and it does not authenticate by itself. Outside these settings, use a standard AEAD.

## Pitfalls

- **Using ZUC 1.4.** Old code and documents may follow the 1.4 initialization. Test against Document 3 version 1.1 or later.
- **The cell value 0.** Line L14 must map 0 to $2^{31} - 1$. A plain mod operation stores 0 and breaks the vectors.
- **Bit ranges.** $s_{iH}$ is bits 30 to 15 of a 31-bit cell, not bits 31 to 16. The two halves overlap in bit 15.
- **The shift of $W$.** In the initialization, the input to the LFSR is $W \gg 1$, which drops the lowest bit, so it fits in 31 bits.
- **IV reuse.** As for any additive stream cipher, one (key, IV) pair must not encrypt two messages.

## Implementations

## History

The Data Assurance and Communication Security Research Center (DACAS) of the Chinese Academy of Sciences designed ZUC for the 3GPP algorithm set 128-EEA3 and 128-EIA3. ETSI/SAGE published version 1.0 of the specification on 18 June 2010, followed by corrections to the C code. At the rump session of ASIACRYPT 2010, Wu and others showed chosen-IV attacks on version 1.4, which they published at ASIACRYPT 2012. Version 1.5 of 4 January 2011 modified the initialization, and version 1.6 of 28 June 2011 only adjusted the C code. 3GPP adopted 128-EEA3 and 128-EIA3 for LTE.

## References
