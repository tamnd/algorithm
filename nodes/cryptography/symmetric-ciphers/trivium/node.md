---
tag: RVXXYX
kind: algorithm
slug: trivium
name: Trivium
area: cryptography/symmetric-ciphers
level: advanced
summary: A bit-oriented stream cipher by De Canniere and Preneel with an 80-bit key, an 80-bit IV and a 288-bit state in three shift registers. It is in the eSTREAM hardware portfolio.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of keystream bits}
  time: {worst: Θ(n + 1152), average: Θ(n + 1152), best: Θ(n + 1152)}
  space: {extra: Θ(288)}
properties: {deterministic: true}
history:
  year: 2005
  people: [Christophe De Cannière, Bart Preneel]
  note: Submitted to the eSTREAM project in 2005 and selected for the hardware profile of the final portfolio in 2008. ISO/IEC 29192-3 later standardized it as a lightweight stream cipher.
prereqs: [stream-cipher, lfsr]
see_also: [grain, a5-1, lfsr, stream-cipher, lightweight-cryptography, block-cipher, linear-cryptanalysis]
sources:
  - paper: "Christophe De Cannière and Bart Preneel, Trivium Specifications, eSTREAM, ECRYPT Stream Cipher Project, Report 2005/030, 2005"
    locator: Section 2 (key stream generation and key and IV setup, with the 1152 initialization rounds)
  - paper: "Christophe De Cannière and Bart Preneel, Trivium, in New Stream Cipher Designs: The eSTREAM Finalists, LNCS 4986, Springer, 2008, pp. 244-266"
    locator: the design rationale, the period and the security claims
  - paper: "Itai Dinur and Adi Shamir, Cube attacks on tweakable black box polynomials, EUROCRYPT 2009, LNCS 5479, pp. 278-299 (full version IACR ePrint 2008/385)"
    locator: Abstract and Section 5 (key recovery for 672 rounds in 2^19, 735 rounds in 2^30 and 767 rounds in 2^45 bit operations)
  - paper: "Yosuke Todo, Takanori Isobe, Yonglin Hao and Willi Meier, Cube attacks on non-blackbox polynomials based on division property, CRYPTO 2017, LNCS 10403, pp. 250-279"
    locator: Abstract (key recovery for 832 initialization rounds of Trivium, faster than exhaustive search)
  - paper: "eSTREAM, ECRYPT Stream Cipher Project, Trivium test vectors, file verified.test-vectors of the Trivium submission package"
    locator: Set 1 vector 0, Set 2 vector 0 and Set 6 vector 0, stream[0..63]
---

Trivium is a [stream cipher](/stream-cipher/) that Christophe De Cannière and Bart Preneel designed for the eSTREAM project in 2005. It takes an 80-bit key and an 80-bit IV, keeps a 288-bit state in three nonlinear shift registers of 93, 84 and 111 bits, and outputs one keystream bit per step. Each step needs only 3 AND gates and 11 XOR gates, so the cipher is very small in hardware. eSTREAM put it in its hardware portfolio (profile 2), and no attack on the full 1152 initialization rounds is faster than exhaustive key search.

## In plain words

Think of three conveyor belts of bits, of lengths 93, 84 and 111, joined end to end in a ring. At each step, the cipher reads two bits from each belt and XORs the six bits to make one bit of keystream. Then it makes a new bit for the start of each belt from bits of the previous belt: a few XORs and one AND of two neighbor bits. The AND makes the process nonlinear, so the bits cannot be solved with plain linear algebra. To start, the key goes on the first belt and the IV on the second, and the cipher turns the belts 1152 times without output. This mixes the key and the IV into all the bits. The sender and the receiver then get the same keystream, and they XOR it with the message.

## The problem

The input is a key $K = (K_1, \ldots, K_{80})$, an IV $IV = (IV_1, \ldots, IV_{80})$ and a message of $n$ bits. The output is the message XOR the keystream $z_1 z_2 \ldots z_n$. Decryption is the same operation. All arithmetic is in GF(2): $+$ is XOR and $\cdot$ is AND.

In the notation of this area, $K$ is the key, $A$ an adversary and $\mathrm{Adv}$ its advantage. The goal is that for a secret random $K$, no efficient $A$ that picks IVs tells the keystreams apart from uniform bits with a large advantage. The designers claim 80-bit security, for up to $2^{64}$ keystream bits for each (key, IV) pair. An IV must not repeat under one key.

## The algorithm

The state is $(s_1, \ldots, s_{288})$. Register A is $s_1 \ldots s_{93}$, register B is $s_{94} \ldots s_{177}$ and register C is $s_{178} \ldots s_{288}$. Each register shifts toward the higher index, and the new bit enters at its first cell.

```pseudo id=main
TRIVIUM(K, IV, n)                          ▷ 80-bit K and IV, n output bits
L1  (s_1, ..., s_93)    ← (K_1, ..., K_80, 0, ..., 0)
L2  (s_94, ..., s_177)  ← (IV_1, ..., IV_80, 0, 0, 0, 0)
L3  (s_178, ..., s_288) ← (0, ..., 0, 1, 1, 1)
L4  for i ← 1 to 1152 + n do
L5      t1 ← s_66 + s_93;  t2 ← s_162 + s_177;  t3 ← s_243 + s_288
L6      if i > 1152 then output z_(i−1152) ← t1 + t2 + t3
L7      t1 ← t1 + s_91 · s_92 + s_171
L8      t2 ← t2 + s_175 · s_176 + s_264
L9      t3 ← t3 + s_286 · s_287 + s_69
L10     (s_1, ..., s_93)    ← (t3, s_1, ..., s_92)
L11     (s_94, ..., s_177)  ← (t1, s_94, ..., s_176)
L12     (s_178, ..., s_288) ← (t2, s_178, ..., s_287)
```

Lines L1 to L3 load the key into register A, the IV into register B, and a fixed pattern of three ones into the last cells of register C. Lines L4 to L12 are one step. Line L5 takes the XOR of two cells of each register. Line L6 outputs their sum, but only after the 1152 initialization steps ($4 \cdot 288$, so each bit of the state is replaced four times). Lines L7 to L9 add one AND term and one cell of the next register to each $t$. Lines L10 to L12 shift each register by one cell and insert the new bit: $t_1$ from register A feeds register B, $t_2$ from B feeds C, and $t_3$ from C feeds A. So the three registers form one ring.

The specification numbers the bits $K_1 \ldots K_{80}$, and the eSTREAM test vectors write the key as 10 bytes. The reference code maps them like this: $K_{80}$ is the least significant bit of byte 0 and $K_1$ is the most significant bit of byte 9, so bit $j$ of byte $b$ is $K_{80 - 8b - j}$. The IV uses the same map. Keystream bit $z_1$ is the least significant bit of the first output byte. A wrong bit order is the most common reason that a new implementation fails the vectors.

The code on this page is for study only. It is not constant time as Python runs it, and it must not protect real data. For real use, take a vetted AEAD such as ChaCha20-Poly1305 or AES-GCM from libsodium, OpenSSL or a FIPS 140 validated module.

## Example

Take the all-zero key and the all-zero IV (eSTREAM Set 2, vector 0). After lines L1 to L3 the only ones are $s_{286} = s_{287} = s_{288} = 1$. The table shows a few steps, the new bits $t_1, t_2, t_3$ of lines L7 to L9, and the number of ones in each register after the step.

| step $i$ | new $t_1$ | new $t_2$ | new $t_3$ | ones in A | ones in B | ones in C |
|---|---|---|---|---|---|---|
| 1 | 0 | 0 | 0 | 0 | 0 | 2 |
| 2 | 0 | 0 | 1 | 1 | 0 | 1 |
| 3 | 0 | 0 | 1 | 2 | 0 | 0 |
| 69 | 1 | 0 | 0 | 2 | 2 | 0 |
| 200 | 0 | 0 | 0 | 2 | 10 | 11 |
| 288 | 0 | 0 | 1 | 27 | 20 | 39 |
| 576 | 0 | 1 | 0 | 39 | 41 | 54 |
| 1152 | 1 | 0 | 1 | 43 | 33 | 56 |

In step 1, $t_3 = s_{243} + s_{288} = 1$, and line L9 adds $s_{286} \cdot s_{287} + s_{69} = 1$, so the new bit is 0. In steps 2 and 3, one of $s_{286}, s_{287}$ is 0, so the AND term is 0 and two ones move into register A. For about the first 66 steps nothing reaches a tap, and the state stays almost empty. After 288 steps the ones spread to all three registers, and after 1152 steps 132 of the 288 bits are one. The output bits $z_1 \ldots z_8$ are 1, 1, 0, 1, 1, 1, 1, 1. Packed with $z_1$ as the least significant bit, they give the byte 0xFB. The first 16 bytes are FBE0BF265859051B517A2E4E239FC97F, as in the eSTREAM vectors.

## Correctness

The state update is a deterministic function of the state, and lines L1 to L3 depend only on $K$ and $IV$. So the sender and the receiver compute the same keystream, and $(m \oplus z) \oplus z = m$. The step map of lines L7 to L12 is also a bijection of the 288-bit state: from the state after a step, the last cell of each register before the step can be solved from the new first cell of the next register. So no two states merge, and the initialization does not lose entropy from the key and the IV. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- Each step does a constant amount of work: 3 ANDs and 11 XORs, plus the shift. The 1152 initialization steps are a fixed cost per IV, so $n$ output bits cost $\Theta(n + 1152)$ steps.
- In hardware the shift is free wiring, and the state is 288 flip-flops. In the designers' estimates the 1-bit design needs about 3488 gate equivalents. Because no tap of lines L5 to L9 reads a cell that the last 64 steps wrote, 64 steps can run in parallel with 64 times the gates.
- In software, a bitsliced form computes 64 bits per step with word operations. The Python code here moves lists of bits and is slow.
- The state is 288 bits plus three temporary bits.

## Properties

- **Nonlinear feedback.** Each feedback contains one quadratic term (an AND of two neighbor cells). Without them the state would be one linear map, and the keystream would fall to linear algebra or [Berlekamp-Massey](/berlekamp-massey/) as in the [LFSR](/lfsr/) page.
- **The output is linear in the state.** Line L6 is an XOR of six cells. The designers chose this so that the security rests on the growth of the degree of the state bits as functions of the key and IV.
- **Cube attacks.** After $r$ initialization rounds each keystream bit is a polynomial in the key and IV bits. Dinur and Shamir (EUROCRYPT 2009) sum it over all values of a chosen set (a "cube") of IV bits and get a linear equation in the key. They recover the key of Trivium with 672 initialization rounds in $2^{19}$ bit operations, with 735 rounds in $2^{30}$, and with 767 rounds in $2^{45}$. Todo, Isobe, Hao and Meier (CRYPTO 2017) used the division property to reach 832 rounds, with a cost near exhaustive search. The full 1152 rounds keep a large margin.
- **Period.** The designers do not prove a period. The state update is a bijection, so the state sequence is a pure cycle, but its length is not known. They argue that short cycles are unlikely for a random 288-bit bijection.
- **Small key.** An 80-bit key was the eSTREAM hardware target. It gives a much smaller margin against exhaustive search than the 128-bit keys of modern ciphers.

## Variants and improvements

- **Kreyvium.** Canteaut et al. (FSE 2016) added a 128-bit key and IV and two extra registers, for use in homomorphic encryption.
- **Bivium.** A reduced version with two registers, proposed by other researchers as a target for analysis. Algebraic and SAT-solver attacks break it, and it is not for use.
- **Other eSTREAM hardware ciphers.** [Grain](/grain/) uses one LFSR and one NFSR with a nonlinear filter, and Grain-128AEADv2 adds authentication. MICKEY 2.0 is the third cipher in profile 2.

## When to use it

Use Trivium where hardware area or power is very small and an 80-bit key is enough, or where the protocol already uses it. For new designs, prefer a cipher with a 128-bit key and authentication, such as Ascon-AEAD128 from the [Ascon](/ascon/) family, which NIST standardized in SP 800-232. Trivium gives only confidentiality, so add a MAC.

## Pitfalls

- **IV reuse.** Two messages under one (key, IV) pair give $c \oplus c' = m \oplus m'$. The IV must be unique for each message.
- **Fewer warm-up rounds.** The cube attacks above recover the key if the 1152 rounds of line L4 are cut to under about 800. Do not shorten them for speed.
- **Bit order.** The vectors use the byte map in the walk-through. Loading the key bytes with the most significant bit first gives a different, wrong cipher that still looks random.
- **No integrity.** The cipher is malleable: a bit flip in the ciphertext flips the same bit of the plaintext.
- **Too much keystream.** The claim covers $2^{64}$ bits per (key, IV) pair. Re-key before that.

## Implementations

## History

De Cannière and Preneel submitted Trivium to eSTREAM, the ECRYPT stream cipher project, in April 2005. They designed it to be as simple as possible, with ideas from block ciphers: the three registers and the AND terms play the role of rounds of a nonlinear permutation. In April 2008 eSTREAM chose it, with Grain v1 and MICKEY 2.0, for the hardware profile of the final portfolio. Cube attacks in 2009 and division-property attacks from 2017 broke reduced versions, but none reached the full 1152 rounds. ISO/IEC 29192-3 (2012) includes Trivium as a lightweight stream cipher.

## References
