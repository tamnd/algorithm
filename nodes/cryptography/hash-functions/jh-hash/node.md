---
tag: TGYCB3
kind: algorithm
slug: jh-hash
name: JH
aliases:
- JH hash
- JH42
- JH-256
- JH-512
area: cryptography/hash-functions
level: research
summary: A SHA-3 finalist by Hongjun Wu that XORs a 512-bit block into both halves of a 1024-bit state around a fixed 42-round bijection E8 built from 4-bit S-boxes.
model: word-ram
complexity:
  vars: {N: the message length in bits}
  time: {worst: Θ(N), average: Θ(N), best: Θ(N)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2008
  people: [Hongjun Wu]
  note: Submitted to the SHA-3 competition in 2008 with 35.5 rounds. The final-round tweak of January 2011 raised E8 to 42 rounds (JH42). NIST chose Keccak in 2012.
prereqs: [cryptographic-hash-function, compression-function, advanced-encryption-standard]
see_also: [groestl, skein, keccak, sha-3, sponge-construction, serpent, multicollision-attack, indifferentiability-framework]
sources:
  - url: "https://www3.ntu.edu.sg/home/wuhj/research/jh/jh_round3.pdf"
    title: "Hongjun Wu, The hash function JH, round 3 specification, 16 January 2011"
    locator: Section 4 (4.1 S-boxes, 4.2 linear transformation L, 4.3 permutation P_d, 4.4 round function R_d, 4.5 bijection E_d, 4.6 round constants), Section 5.1 (F_8), Section 6 (padding, IV, truncation), Section 7 (bit-slice form), Section 9 (security claims; 9.6 compression structure, 9.7 rebound), Section 10.3 (speed), Appendix A.1 (constants)
  - url: "https://www3.ntu.edu.sg/home/wuhj/research/jh/jh_20110116.zip"
    title: "JH final-round submission package, 16 January 2011"
    locator: KAT_MCT/ShortMsgKAT_256.txt and KAT_MCT/ShortMsgKAT_512.txt (Len = 0, 8, 16, 512, 1024)
  - paper: "Rishiraj Bhattacharyya, Avradip Mandal and Mridul Nandi, Security analysis of the mode of JH hash function, FSE 2010, LNCS 6147, pages 168 to 191"
    locator: indifferentiability of the JH mode from a random oracle with an ideal permutation, and a meet-in-the-middle preimage attack on JH-512 with about 2^507 work and memory
  - paper: "Dustin Moody, Souradyuti Paul and Daniel Smith-Tone, Improved indifferentiability security bound for the JH mode, Designs, Codes and Cryptography 79(2), 2016"
    locator: the improved indifferentiability bound of about 2^256 queries for the JH mode with a 1024-bit state
  - paper: "Vincent Rijmen, Deniz Toz and Kerem Varıcı, Rebound attack on reduced-round versions of JH, FSE 2010, LNCS 6147, pages 286 to 303"
    locator: semi-free-start collisions for 16 rounds and near collisions for 22 rounds of the compression function, as cited in Section 9.7 of the specification
  - url: "https://doi.org/10.6028/NIST.IR.7896"
    title: "S. Chang, R. Perlner, W. E. Burr, M. S. Turan, J. M. Kelsey, S. Paul and L. E. Bassham, NIST IR 7896, Third-Round Report of the SHA-3 Cryptographic Hash Algorithm Competition, November 2012"
    locator: the sections on JH (security margin and performance)
---

JH is a cryptographic hash function by Hongjun Wu and one of the five finalists of the NIST SHA-3 competition. It keeps a 1024-bit state and reads the message in 512-bit blocks. Each block is XORed into the first half of the state, the whole state goes through a fixed bijection $E_8$, and the same block is XORed into the second half. $E_8$ has 42 rounds of 4-bit S-boxes, a small MDS map and a bit permutation, in the style of [AES](/advanced-encryption-standard/) generalized to a hypercube of 256 elements. The digest is the last $n$ bits of the final state. NIST chose Keccak as SHA-3 in 2012, and JH is now studied for its simple, hardware-friendly design.

**Notation.** $n \in \{224, 256, 384, 512\}$ is the output size in bits. $H$ is the 1024-bit state and $M^{(i)}$ the $i$-th 512-bit block; bit 0 of a word is its leftmost (most significant) bit. $\oplus$ is XOR and $\|$ is concatenation. $E_8$ is a permutation of $\{0,1\}^{1024}$ made of 42 rounds $R_8$ on 256 elements of 4 bits. $S_0$ and $S_1$ are the two 4-bit S-boxes, $L$ the linear map on two 4-bit elements, $P_8$ the permutation of the 256 elements, and $C_r$ the 256-bit round constant of round $r$. Arithmetic on 4-bit elements is in $\mathrm{GF}(2^4)$ with the polynomial $x^4 + x + 1$. $N$ is the message length in bits. The security model is the ideal permutation model: $E_8$ is a random permutation.

## In plain words

JH has a state twice as large as a message block. For each block, it adds the block into the left half of the state, scrambles the whole state with one fixed scrambler, and then adds the same block into the right half.

The scrambler cuts the state into 256 small pieces of 4 bits. In each of its 42 rounds, every piece goes through one of two small tables, and a bit of a round constant chooses which table. Then pairs of pieces are mixed, and the pieces are moved to new places so that, round after round, each piece meets every other one. The hash is the last part of the state after the last block.

## The problem

Build a hash function $H : \{0,1\}^{*} \to \{0,1\}^{n}$ with collision resistance $2^{n/2}$ and preimage resistance $2^n$, small and fast in hardware and fast with bit-slice code on CPUs, and immune to the generic weaknesses of the narrow [Merkle-Damgård construction](/merkle-damgard-construction/): length extension, multicollisions and long-message second preimages. These were the goals of the SHA-3 competition.

## The algorithm

```pseudo id=main
JH(M, n)                                            ▷ Section 6
L1  H ← F8(⟨n⟩ in the first 16 bits ‖ 0^1008, 0^512)
L2  pad M: one 1 bit, 383 + (−N mod 512) zero bits, then N as a 128-bit number
L3  for each 512-bit block m:  H ← F8(H, m)
L4  return the last n bits of H

F8(H, m)                                            ▷ Sections 4 and 5.1
L5  A ← H ⊕ (m ‖ 0^512);  group the bits of A into 256 elements q of 4 bits
L6  for r ← 0 to 41:  q_i ← S_c(q_i) for each i, where c is bit i of C_r
L7      (q_2i, q_2i+1) ← L(q_2i, q_2i+1) = (5•q_2i + 2•q_2i+1, 2•q_2i + q_2i+1)
L8      q ← P8(q)
L9  return (de-grouped q) ⊕ (0^512 ‖ m)
```

The grouping puts bits $i, i + 256, i + 512, i + 768$ of $A$ into element $2i$ and bits $i + 128, i + 384, i + 640, i + 896$ into element $2i + 1$, for $0 \le i < 128$. $P_8 = \phi_8 \circ P'_8 \circ \pi_8$: $\pi_8$ swaps the last two elements of every group of four, $P'_8$ moves the elements in even places to the first half and those in odd places to the second half, and $\phi_8$ swaps the elements of each pair in the second half. $C_0$ is the integer part of $(\sqrt{2} - 1) \cdot 2^{256}$, and $C_r$ is $C_{r-1}$ after one round $R_6$ with all constant bits 0 (Section 4.6).

## Example

JH-256 of the empty message. The intermediate values below come from the code of this page; the official files give only the digest.

1. Line L1 starts from a state whose first two bytes are `01 00` (256) and whose other bits are 0, and compresses it with a zero block. The result $H^{(0)}$ begins `EB98A3412C20D3EB` and ends `89E3AB13D31CD769`.
2. Line L2 pads the empty message to one block: the byte `80`, 47 zero bytes, and the 16-byte length 0. Padding always adds at least 512 bits, so a 3-byte message gives two blocks.
3. Line L3 computes $F_8(H^{(0)}, M^{(1)})$, with 42 rounds of $R_8$ inside $E_8$.
4. Line L4 keeps the last 32 bytes: `46E64619C18BB0A92A5E87185A47EEF83CA747B8FCC8E1412921357E326DF434`, the first entry of `ShortMsgKAT_256.txt`.

## Correctness

The code is checked against the official short-message known-answer tests for JH-256 and JH-512 (messages of 0, 1, 2, 64 and 128 bytes) and against the round constants $C_0$, $C_1$, $C_2$, $C_{40}$ and $C_{41}$ of Appendix A.1. The proof page shows that $E_8$ is a bijection, that $L$ has branch number 3, and that $F_8(\cdot, m)$ can be inverted for each $m$, which is why the security of JH does not reduce to a collision-resistant compression function.

**Security of the construction.** $F_8$ is not collision resistant on its own: for a fixed block, $F_8$ is a bijection of the state that anyone can invert, so pseudo-collisions and pseudo-preimages are free (Section 9.6). The security comes from the fixed IV, the 1024-bit state and $E_8$. In the ideal permutation model, Bhattacharyya, Mandal and Nandi prove that the JH mode is indifferentiable from a random oracle, and Moody, Paul and Smith-Tone raise the bound to about $2^{256}$ queries. That bound reaches the collision level of JH-512 but is below its preimage level. These are bounds on the mode with an ideal $E_8$, not proofs about the real $E_8$, so they are not tight reductions to a concrete assumption.

**Why the large state.** An internal collision of the 1024-bit state costs $2^{512}$ generically, more than a collision of any output. A meet-in-the-middle preimage attack inverts $F_8$ and has to match 1024-bit states; the best one, by Bhattacharyya, Mandal and Nandi, costs about $2^{507}$ work and $2^{507}$ memory on JH-512, which the specification counts as no better than brute force because of the memory accesses.

## Complexity

Each 512-bit block costs one $E_8$: 42 rounds of 256 S-boxes, 128 maps $L$ and one permutation $P_8$. The IV costs one more $E_8$ (it can be stored), and padding adds one block at most. So the time is $\Theta(N)$ for a message of $N$ bits, and the extra space is the 1024-bit state and one 256-bit round constant. In bit-slice form (Section 7), the 256 S-boxes of a round are 2 calls of a 128-bit S-box circuit of 11 steps, $L$ is 10 XORs and $P_8$ is a fixed bit swap. Section 10.3 reports 19.6 cycles per byte with 64-bit code and 23.3 with 32-bit code on an Intel Core 2 T6600.

## Properties

- **Claimed security** (Section 9): collision $2^{n/2}$, preimage $2^n$, second preimage $2^n$, except $2^{512 - \log_2 \bar{l}}$ for JH-512 with messages of $\bar{l}$ blocks.
- **Wide state**: 1024 bits for every $n$, and the digests differ only in the IV and the truncation.
- **One permutation**: the same $E_8$ for every block, with no key schedule and no message expansion.
- **Hardware friendly**: 4-bit S-boxes and XORs only; the round constants can be made on the fly by $R_6$.
- **No key input**: keyed use is through [HMAC](/hmac/).

## Variants and improvements

- **JH with 35.5 rounds**, the version of 2008 and 2009, gives other digests. The final-round tweak of 2011 raised $E_8$ to 42 rounds.
- **$F_d$ for other $d$** (Section 8.1): the same structure on a state of $2^{d+2}$ bits with $6(d - 1)$ rounds. JH uses $d = 8$.
- **[Grøstl](/groestl/)** is another AES-like finalist with a wide pipe, but it uses two permutations per block.
- **The [sponge construction](/sponge-construction/)** of Keccak also uses one fixed permutation of a large state; JH differs in that the message enters both before and after the permutation and the whole state is kept.

## When to use it

Do not choose JH for new systems: few libraries support it, and [SHA-3](/sha-3/), [SHA-2](/sha-2/) and [BLAKE2](/blake2/) are standard and faster in software. JH is still worth study as a compact hardware design with a proof in the ideal permutation model, and as an example of the generalized AES design over a hypercube.

## Pitfalls

- **The round count.** JH with 35.5 rounds and JH42 give different values. Check which version a library or a test vector uses.
- **Bit order.** Bit 0 is the most significant bit, of the state and of each 4-bit element. A little-endian reading gives wrong digests while each round still looks right.
- **Grouping.** $E_8$ groups bits that are 256 places apart; skipping the grouping and de-grouping still gives a permutation and passes simple tests.
- **Padding.** JH always adds at least 512 bits, so a message of 1 to 64 bytes takes two blocks, while SHA-256 needs only one block for up to 55 bytes.
- **Table lookups and timing.** S-boxes as tables in memory can leak through the cache. The bit-slice form of Section 7 is constant time.

## Implementations

The Python code is for study only. It is not constant time, because the S-boxes are tables, and it must not protect real data; use the bit-slice C code of the designer (in `jh_20110116.zip` and in eBASH), or a standard hash. The code follows the hardware description of Sections 4 to 6, one 4-bit element at a time, so it is slow. It gives `linear`, `permute` and `round_function` (lines L6 to L8), the round constants, `e8`, `compress` (lines L5 and L9), `pad`, and `jh(msg, n)` (lines L1 to L4) with `jh256` and `jh512`. It handles whole bytes only. The tests copy by hand the known answers of the final-round package and five round constants of Appendix A.1. They also check that $L$ equals the map $(5A + 2B, 2A + B)$ in $\mathrm{GF}(2^4)$, that $P_8$ is a permutation, the padding, that JH-224 is not a truncation of JH-256, and that one changed bit changes about half of the output bits. Python's standard library has no JH, so there is no second check.

## History

Hongjun Wu, then at the Institute for Infocomm Research and Nanyang Technological University in Singapore, submitted JH to the SHA-3 competition in October 2008. It reached the second round in 2009 and the final round in December 2010, and for the final round the number of rounds went from 35.5 to 42. The S-box selection by round constant bits follows Lucifer, and the bit-slice design follows Serpent (Section 2). NIST IR 7896 (2012) found no attack on the full function and chose Keccak.

## References
