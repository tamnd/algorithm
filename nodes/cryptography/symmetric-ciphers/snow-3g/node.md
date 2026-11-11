---
tag: YDPQ53
kind: algorithm
slug: snow-3g
name: SNOW 3G
aliases:
area: cryptography/symmetric-ciphers
level: advanced
summary: A word-oriented stream cipher of ETSI/SAGE with a 16-word LFSR over GF(2^32) and a 3-register FSM. It is the core of UEA2 and UIA2 in UMTS and of 128-EEA1 and 128-EIA1 in LTE.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of 32-bit keystream words}
  time: {worst: Θ(n + 33), average: Θ(n + 33), best: Θ(n + 33)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2006
  people: [Patrik Ekdahl, Thomas Johansson]
  note: ETSI SAGE derived SNOW 3G in 2006 from SNOW 2.0 of Ekdahl and Johansson (2002), adding a third FSM register and a second S-box. 3GPP adopted it for UMTS and then LTE.
prereqs: [stream-cipher, lfsr]
see_also: [zuc, lfsr, stream-cipher, advanced-encryption-standard, s-box, message-authentication-code, a5-1, grain]
sources:
  - paper: "ETSI/SAGE, Specification of the 3GPP Confidentiality and Integrity Algorithms UEA2 & UIA2, Document 2: SNOW 3G Specification, Version 1.1, 6 September 2006"
    locator: Sections 3 and 4 (the LFSR, the FSM, the S-boxes S1 and S2, initialization and keystream), Section 5 (tables SR and SQ), Annex 1
  - paper: "ETSI/SAGE, Specification of the 3GPP Confidentiality and Integrity Algorithms UEA2 & UIA2, Document 3: Implementors' Test Data, Version 1.0, 10 January 2006"
    locator: Sections 3.3 to 3.6 (SNOW 3G test sets 1 to 4)
  - paper: "Patrik Ekdahl and Thomas Johansson, A new version of the stream cipher SNOW, Selected Areas in Cryptography (SAC 2002), LNCS 2595, pp. 47-61"
    locator: SNOW 2.0, the LFSR over GF(2^32) and the FSM on which SNOW 3G is based
  - paper: "Jing Yang, Thomas Johansson and Alexander Maximov, Vectorized linear approximations for attacks on SNOW 3G, IACR Transactions on Symmetric Cryptology 2019(4)"
    locator: the fast correlation attack on SNOW 3G with complexity about 2^177, above exhaustive search of the 128-bit key
---

SNOW 3G is a word-oriented [stream cipher](/stream-cipher/) that the ETSI Security Algorithms Group of Experts (SAGE) specified in 2006 for 3GPP mobile networks. It takes a 128-bit key and a 128-bit IV, and outputs one 32-bit keystream word per clock. Its state is a linear feedback shift register of 16 words over $\mathrm{GF}(2^{32})$ and a finite state machine (FSM) of three 32-bit registers with two S-boxes. SNOW 3G is the core of the UMTS confidentiality and integrity algorithms UEA2 and UIA2, and of the LTE algorithms 128-EEA1 and 128-EIA1. No published attack on the full cipher is faster than exhaustive key search.

## In plain words

SNOW 3G has two parts. The first part is a row of 16 boxes, each holding a 32-bit word. At each clock the row moves one place, and a new word goes in at the end: a mix of three old words, two of them multiplied by a fixed field element. This part alone is linear, so it is fast and has a very long period, but it is easy to predict. The second part is a small machine with three words of memory. It reads two words of the row, adds them to its memory with normal integer addition, and passes its memory through two AES-like S-boxes. The output word is the machine's output XOR the first word of the row. The integer additions and the S-boxes hide the linear structure.

## The problem

The input is a key $K = (k_0, k_1, k_2, k_3)$ and an IV $(IV_0, IV_1, IV_2, IV_3)$, each four 32-bit words, and a number $n$. The output is the keystream $z_1, \ldots, z_n$ of 32-bit words. UEA2 XORs the keystream with the data. The words are big-endian: $k_0$ is the first four key bytes.

In the notation of this area, $K$ is the key, $A$ an adversary and $\mathrm{Adv}$ its advantage. The goal is that for a secret random $K$, no efficient $A$ that chooses IVs tells the keystreams apart from uniform words with a large advantage. The 3GPP requirement is 128-bit security.

## The algorithm

The LFSR holds $s_0, \ldots, s_{15}$. The FSM holds $R_1, R_2, R_3$. $\boxplus$ is addition modulo $2^{32}$ and $\oplus$ is XOR. $\alpha$ is a root of a fixed polynomial of degree 4 over $\mathrm{GF}(2^8)$, so $\mathrm{GF}(2^{32}) = \mathrm{GF}(2^8)(\alpha)$, and multiplication by $\alpha$ or $\alpha^{-1}$ is a byte shift and one table lookup (MUL$\alpha$, DIV$\alpha$).

```pseudo id=main
SNOW-3G(K, IV, n)
L1  load s_0..s_15 from K and IV;  R1 ← R2 ← R3 ← 0
L2  repeat 32 times                              ▷ initialization mode
L3      F ← FSM-CLOCK()
L4      LFSR-CLOCK(F)
L5  FSM-CLOCK()                                  ▷ output discarded
L6  LFSR-CLOCK(0)
L7  for t ← 1 to n do                            ▷ keystream mode
L8      F ← FSM-CLOCK()
L9      output z_t ← F ⊕ s_0
L10     LFSR-CLOCK(0)

FSM-CLOCK()
L11 F ← (s_15 ⊞ R1) ⊕ R2
L12 r ← R2 ⊞ (R3 ⊕ s_5)
L13 R3 ← S2(R2);  R2 ← S1(R1);  R1 ← r;  return F

LFSR-CLOCK(F)
L14 v ← α·s_0 ⊕ s_2 ⊕ α^(−1)·s_11 ⊕ F
L15 (s_0, ..., s_15) ← (s_1, ..., s_15, v)
```

Line L1 loads the LFSR. With $\mathbf{1}$ the all-ones word, $(s_0, \ldots, s_{15})$ is $k_0 \oplus \mathbf{1}, k_1 \oplus \mathbf{1}, k_2 \oplus \mathbf{1}, k_3 \oplus \mathbf{1}, k_0, k_1, k_2, k_3, k_0 \oplus \mathbf{1}, k_1 \oplus \mathbf{1} \oplus IV_3, k_2 \oplus \mathbf{1} \oplus IV_2, k_3 \oplus \mathbf{1}, k_0 \oplus IV_1, k_1, k_2, k_3 \oplus IV_0$. Lines L2 to L4 run 32 clocks in which the FSM output feeds back into the LFSR, so the key and IV spread into the whole state. Lines L5 and L6 make one more clock with no output. Lines L7 to L10 output one word per clock.

The FSM (lines L11 to L13) is the nonlinear part. $S_1$ applies the AES S-box to each byte of a word and then the AES MixColumn. $S_2$ has the same shape, with the S-box $S_Q$ (from the Dickson polynomial $g_{49}$ over $\mathrm{GF}(2^8)$, plus the constant 0x25) and a MixColumn over a different field. Line L14 is the linear feedback. In code, $\alpha \cdot s_0$ is (s_0 << 8) ⊕ MUL$\alpha$[s_0 >> 24], and $\alpha^{-1} \cdot s_{11}$ is (s_11 >> 8) ⊕ DIV$\alpha$[s_11 & 0xff]. Both tables come from MULxPOW with the reduction byte 0xA9 (Section 3.4 of the specification).

The code on this page is for study only. It is not constant time as Python runs it, because it uses table lookups, and it must not protect real data. Network equipment uses validated implementations of UEA2 and 128-EEA1. For general use, take a vetted AEAD such as AES-GCM or ChaCha20-Poly1305 from libsodium, OpenSSL or a FIPS 140 validated module.

## Example

Take Test Set 1 of the ETSI/SAGE Implementors' Test Data: $K$ = 2BD6459F 82C5B300 952C4910 4881FF48 and $IV$ = EA024714 AD5C4D84 DF1F9B25 1C0BF45F. Line L1 gives $s_0 = k_0 \oplus \mathbf{1}$ = D429BA60 and $s_{15} = k_3 \oplus IV_0$ = A283B85C. The table shows the first clocks of lines L2 to L4, with the values before each clock.

| clock | $s_0$ | $s_{15}$ | $R_1$ | $R_2$ | $R_3$ | $F$ |
|---|---|---|---|---|---|---|
| 0 | D429BA60 | A283B85C | 00000000 | 00000000 | 00000000 | A283B85C |
| 1 | 7D3A4CFF | 97DF2884 | 82C5B300 | 63636363 | 25252525 | 79C7B8E7 |
| 2 | 6AD3B6EF | 311BA301 | 136CCF98 | 486C5BC4 | 93939393 | 0CE4295D |

In clock 0, $F = (s_{15} \boxplus 0) \oplus 0 = s_{15}$. Line L13 then sets $R_2 = S_1(0)$ = 63636363, since the AES S-box maps 0 to 0x63 and MixColumn keeps a word of four equal bytes. In the same way $R_3 = S_2(0)$ = 25252525, since $S_Q(0)$ = 0x25. $R_1 = R_2 \boxplus (R_3 \oplus s_5) = s_5$ = 82C5B300. The rows match the table in Section 3.3 of the test data. After the 33 clocks of lines L2 to L6, the output is $z_1$ = ABEE9704 and $z_2$ = 7AC31373.

## Correctness

Lines L1 to L15 are deterministic functions of $K$ and $IV$, so sender and receiver compute the same $z_t$, and $(m \oplus z) \oplus z = m$. In the keystream mode the LFSR update is invertible, because $s_0$ can be solved from $v$ at line L14 ($\alpha \ne 0$), and the FSM update is invertible because $S_1$ and $S_2$ are bijections. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- One clock is a constant number of word operations: two S-box words (eight byte lookups and a MixColumn each), two table lookups for $\alpha$ and $\alpha^{-1}$, two additions modulo $2^{32}$ and some XORs and shifts.
- Initialization is 33 clocks for each IV. $n$ words cost $\Theta(n + 33)$ clocks.
- The state is 16 + 3 = 19 words, 608 bits. Fast software uses precomputed tables that join each S-box with its MixColumn, as in table-based AES.

## Properties

- **The LFSR.** Its feedback $s_{t+16} = \alpha s_t \oplus s_{t+2} \oplus \alpha^{-1} s_{t+11}$ is linear over $\mathrm{GF}(2^{32})$. The designers chose the polynomial so that the LFSR alone has maximal period $2^{512} - 1$ from a nonzero state.
- **The FSM.** The additions modulo $2^{32}$ are not linear over GF(2), and $S_1$ and $S_2$ are nonlinear. The third register $R_3$ and the S-box $S_2$, which SNOW 2.0 did not have, were added against algebraic attacks.
- **Attacks.** Linear distinguishers and fast correlation attacks exist for SNOW 2.0 and SNOW 3G, but the best on SNOW 3G, by Yang, Johansson and Maximov (2019), needs about $2^{177}$ operations, more than the $2^{128}$ of exhaustive key search. Fault attacks need physical access to the device, and other attacks target versions with fewer initialization clocks.
- **Word output.** Each clock gives 32 bits, so software speed is high compared with bit-oriented ciphers such as [Trivium](/trivium/) and [Grain](/grain/).

## Variants and improvements

- **SNOW 1.0 and SNOW 2.0.** Ekdahl and Johansson proposed SNOW 1.0 for NESSIE in 2000. Distinguishing and guess-and-determine attacks showed weaknesses, and SNOW 2.0 (SAC 2002) fixed them. SNOW 2.0 is in ISO/IEC 18033-4.
- **UEA2 and UIA2.** UEA2 forms the IV from the frame counter, the bearer identity and the direction bit, and XORs the keystream with the data. UIA2 uses the first keystream words as keys of a polynomial MAC over $\mathrm{GF}(2^{64})$. In LTE the same pair is 128-EEA1 and 128-EIA1, next to [AES](/advanced-encryption-standard/) (EEA2) and [ZUC](/zuc/) (EEA3).
- **SNOW-V and SNOW-Vi.** Ekdahl, Johansson, Maximov and Yang proposed these in 2019 and 2021 for 5G, with 256-bit keys and an FSM that uses AES rounds to run fast on CPUs with AES instructions.

## When to use it

Use SNOW 3G when a 3GPP protocol requires UEA2, UIA2, 128-EEA1 or 128-EIA1, for example in a test tool or a base station stack. It is not a general-purpose cipher: it has no built-in authentication and no common software library offers it for general use. Outside mobile networks, use a standard AEAD.

## Pitfalls

- **Bit and word order.** The key and IV are big-endian words with $k_0$ first, and the IV words go into $s_{15}, s_{12}, s_{10}, s_9$ in that order. A different load still gives random-looking output, so test with Document 3.
- **IV reuse.** The cipher is additive. UEA2 builds the IV from a counter, and a counter reset under one key gives a two-time pad.
- **Missing the discarded clock.** Lines L5 and L6 run once before the first output word. Without them the output shifts by one word and fails the vectors.
- **Truncated initialization.** Do not cut the 32 clocks of line L2. Published attacks target versions with fewer initialization clocks, and the margin comes from the full count.
- **Table timing.** Table lookups indexed by secret bytes leak through cache timing on shared CPUs.

## Implementations

## History

Patrik Ekdahl and Thomas Johansson of Lund University designed SNOW 1.0 for the NESSIE project in 2000 and SNOW 2.0 in 2002. In 2006 ETSI SAGE took SNOW 2.0 as the base of a second algorithm set for UMTS, made the FSM stronger, and named it SNOW 3G. The specification Version 1.0 appeared on 10 January 2006 and Version 1.1 on 6 September 2006, with no change to the algorithm. 3GPP adopted UEA2 and UIA2 for UMTS, and then 128-EEA1 and 128-EIA1 for LTE.

## References
