---
tag: HJZJTY
kind: algorithm
slug: twofish
name: Twofish
area: cryptography/symmetric-ciphers
level: advanced
summary: A 128-bit block cipher with 128, 192 or 256-bit keys, a 16-round Feistel network with key-dependent S-boxes, an MDS matrix and a pseudo-Hadamard transform. An AES finalist in 1999.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {b: the number of 16-byte blocks}
  time: {worst: Θ(b), average: Θ(b), best: Θ(b)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 1998
  people: [Bruce Schneier, John Kelsey, Doug Whiting, David Wagner, Chris Hall, Niels Ferguson]
  note: Submitted to the NIST AES competition in June 1998 and chosen as one of the five finalists in 1999.
prereqs: [feistel-network, s-box, key-schedule, gf2-polynomial-arithmetic]
see_also: [blowfish, advanced-encryption-standard, serpent, rc6, key-whitening, block-cipher, differential-cryptanalysis]
sources:
  - url: "https://www.schneier.com/wp-content/uploads/2016/02/paper-twofish-paper.pdf"
    title: Bruce Schneier, John Kelsey, Doug Whiting, David Wagner, Chris Hall and Niels Ferguson, Twofish, a 128-bit block cipher, AES submission, 15 June 1998
    locator: Section 3 (building blocks), Section 4 (the cipher, the functions F, g and h, the key schedule and the q permutations in Section 4.3.5), Section 8 (cryptanalysis) and Appendix A (test vectors)
  - paper: doi:10.6028/jres.106.023
    title: James Nechvatal and others, Report on the development of the Advanced Encryption Standard (AES), Journal of Research of NIST 106(3), 2001
    locator: the evaluation of the five finalists
  - url: "https://www.cl.cam.ac.uk/~rja14/serpent.html"
    title: Ross Anderson, the Serpent home page
    locator: the vote at the third AES candidate conference, April 2000
---

Twofish is a [block cipher](/block-cipher/) on 128-bit blocks with a key of 128, 192 or 256 bits, built as a 16-round [Feistel network](/feistel-network/). Schneier, Kelsey, Whiting, Wagner, Hall and Ferguson submitted it to the AES competition in 1998, and it was one of the five finalists; NIST chose Rijndael as [AES](/advanced-encryption-standard/). Its round function combines four key-dependent 8-bit [S-boxes](/s-box/), a 4 by 4 maximum distance separable (MDS) matrix over $\mathrm{GF}(2^8)$, a pseudo-Hadamard transform and one-bit rotations. No attack on the full 16 rounds faster than [exhaustive search](/exhaustive-key-search/) is published.

**Notation.** A block is four 32-bit words $R_0, R_1, R_2, R_3$, each read little-endian from 4 bytes. $+$ is addition modulo $2^{32}$, $\oplus$ is XOR, and ROL and ROR rotate a 32-bit word. The key has $8k$ bytes, with $k \in \{2, 3, 4\}$, read as $2k$ little-endian words $M_0, \ldots, M_{2k-1}$. $K_0, \ldots, K_{39}$ are the 40 subkey words and $\rho = 2^{24} + 2^{16} + 2^8 + 1$.

## In plain words

Twofish holds a block as four words. In each of 16 rounds, it takes the two left words and sends each one through a mixing function g. The function g cuts a word into four bytes, sends each byte through a lookup table that depends on the key, and then mixes the four bytes with a small matrix, so that each output byte depends on each input byte. The two results are added to each other in two ways, and two round keys are added. The two outputs change the two right words, together with a rotation by one bit. Then the left and right pairs trade places.

Before the first round and after the last, four key words are XORed into the block. The key schedule builds the round keys with the same function g, so the same code does both jobs.

## The problem

Twofish computes a permutation $E_K$ of $\{0,1\}^{128}$ for each key $K$ of 16, 24 or 32 bytes, and its inverse $D_K$. The security goal is that $E_K$ is a [pseudorandom permutation](/pseudorandom-permutation/): an attacker who does not know $K$ cannot tell it from a random permutation. There is no proof of this; it rests on cryptanalysis. Long messages need a mode of operation.

## The algorithm

The functions follow Section 4 of the Twofish paper. $q_0$ and $q_1$ are two fixed permutations of bytes, built from four 4-bit tables each (Section 4.3.5). MDS is a fixed 4 by 4 matrix over $\mathrm{GF}(2^8)$ with the polynomial $x^8 + x^6 + x^5 + x^3 + 1$, and RS is a fixed 4 by 8 matrix over $\mathrm{GF}(2^8)$ with $x^8 + x^6 + x^3 + x^2 + 1$.

```pseudo id=main
TWOFISH-ENCRYPT(x)
L1  (R0, R1, R2, R3) ← the four words of x, each XORed with K0, K1, K2, K3   ▷ input whitening
L2  for r ← 0 to 15 do
L3      (F0, F1) ← F(R0, R1, r)
L4      (R0, R1, R2, R3) ← (ROR(R2 ⊕ F0, 1), ROL(R3, 1) ⊕ F1, R0, R1)
L5  return (R2 ⊕ K4, R3 ⊕ K5, R0 ⊕ K6, R1 ⊕ K7)   ▷ undo the last swap, output whitening

F(R0, R1, r)                                 ▷ g(X) = h(X, S)
L6  T0 ← g(R0)
L7  T1 ← g(ROL(R1, 8))
L8  F0 ← T0 + T1 + K[2r + 8]                 ▷ the pseudo-Hadamard transform, with keys
L9  F1 ← T0 + 2·T1 + K[2r + 9]
L10 return (F0, F1)

h(X, L)                                      ▷ L = (L0, ..., L(k−1)), four bytes per word
L11 y ← the 4 bytes of X; for j ← k − 1 down to 0: send each byte through q0 or q1, then XOR byte i of Lj
L12 return MDS · (each byte of y through one more q0 or q1)

KEY-SCHEDULE(M)
L13 Me ← (M0, M2, ..., M(2k−2)), Mo ← (M1, M3, ..., M(2k−1))
L14 S ← (S(k−1), ..., S0), where Si is RS times the key bytes 8i to 8i + 7
L15 for i ← 0 to 19 do
L16     A ← h(2iρ, Me)
L17     B ← ROL(h((2i + 1)ρ, Mo), 8)
L18     K[2i] ← A + B
L19     K[2i + 1] ← ROL(A + 2B, 9)
```

The choice of $q_0$ or $q_1$ at each position of h is a fixed table in Section 4.3.2. With a 128-bit key ($k = 2$), each byte goes through three permutations, $q \oplus L_1$, $q \oplus L_0$, $q$, then the MDS matrix. The vector $S$ of line L14 is the part of the key that defines the S-boxes of g. Decryption runs the rounds backward: from the state after round $r$, the words $R_2, R_3$ are the old $R_0, R_1$, so F can be recomputed and the old $R_2 = \mathrm{ROL}(R_0', 1) \oplus F_0$ and $R_3 = \mathrm{ROR}(R_1' \oplus F_1, 1)$ follow.

The Python code for this page is for study only. It is not constant time: the q tables are read at secret indices. Do not use it to protect real data. Use AES-GCM or ChaCha20-Poly1305 from a FIPS 140 validated module, or libsodium, instead. Several libraries still offer Twofish, for example Botan and libgcrypt, for old data.

## Example

Take the first vector of Appendix A.1 of the paper: the 128-bit key is all zero and the plaintext is all zero. Then $S = (0, 0)$, and the key schedule gives $K_0, \ldots, K_3$ = 52C54DDE, 11F0626D, 7CAC9D4A, 4D1B4AAA, $K_4, \ldots, K_7$ = B7B83A10, 1E7D0BEB, EE9C341F, CFE14BE4, and $K_8, K_9$ = F98FFEF9, 9C5B3C17.

| step | $R_0$ | $R_1$ | $R_2$ | $R_3$ |
|---|---|---|---|---|
| after line L1 | 52C54DDE | 11F0626D | 7CAC9D4A | 4D1B4AAA |
| round 1: $T_0$ = C06D4949, $T_1$ = 41B9BFC1, $F_0$ = FBB70803, $F_1$ = E03C04E2 | C38DCAA4 | 7A0A91B6 | 52C54DDE | 11F0626D |
| round 2 | 55A538DE | 5C5A4DB6 | C38DCAA4 | 7A0A91B6 |
| round 16 | C1708BA9 | 9522A3CE | EB27628F | 2C51191D |

Line L5 gives the words $R_2 \oplus K_4$ = 5C9F589F, $R_3 \oplus K_5$ = 322C12F6, $R_0 \oplus K_6$ = 2FECBFB6 and $R_1 \oplus K_7$ = 5AC3E82A. Written as little-endian bytes, the ciphertext is 9F589F5CF6122C32B6BFEC2F2AE8C35A, the value in Appendix A.1. The test file also checks the two other keys of Appendix A.1 (192 and 256 bits) and the chained tables of Appendix A.2, where each ciphertext becomes the next plaintext and the previous ciphertexts become the key, for example the 128-bit chain at step 49 gives 5D9D4EEFFA9151575524F115815A12E0.

## Correctness

TWOFISH-DECRYPT inverts TWOFISH-ENCRYPT for every key. Each round maps $(R_0, R_1, R_2, R_3)$ to a new state from which $R_0$ and $R_1$ can be read directly, so $F_0$ and $F_1$ can be computed again, and the rotations and XORs on $R_2$ and $R_3$ can be undone. The function g need not be a bijection for this. The whitening steps are XORs with fixed words. The [proof](proofs/correctness.md) gives each step.

## Complexity

One block costs 16 rounds. A round costs two calls of g and a few additions, XORs and rotations. With a 128-bit key, one call of g costs 12 lookups of $q_0$ or $q_1$ and one product with the MDS matrix, which is 16 multiplications in $\mathrm{GF}(2^8)$. Fast code does not compute g this way. It folds the q permutations, the key bytes of $S$ and the MDS column into four tables of 256 words at key setup, so that g costs 4 table lookups and 3 XORs. The paper reports 17.8 clock cycles per byte for a fully optimized implementation on a Pentium Pro. So $b$ blocks cost $\Theta(b)$ time and the key state is 40 subkey words plus the tables, independent of $b$.

The key schedule costs 40 calls of h, one for each subkey word, plus the RS products.

The designers' best attack breaks 5 rounds (without the final whitening) with $2^{22.5}$ chosen plaintexts and $2^{51}$ work (Schneier et al. 1998, Section 8.1). Later work also reaches only reduced versions.

## Properties

- **Feistel-like structure with rotations.** The one-bit rotations of line L4 break the byte alignment that a pure Feistel round would keep. They also make the structure slightly different from a Feistel network, but still easy to invert.
- **Key-dependent S-boxes.** The 8-bit S-boxes are $q$ permutations mixed with key bytes, so they are bijective for every key, unlike the random-looking tables of Blowfish.
- **MDS matrix.** If an input to the matrix has $j$ nonzero bytes, with $1 \le j \le 4$, then the output has at least $5 - j$ nonzero bytes. So the branch number is 5, the largest possible for a 4 by 4 matrix.
- **Pseudo-Hadamard transform.** $(a, b) \mapsto (a + b, a + 2b)$ modulo $2^{32}$, invertible because 2 times the first output minus the second gives $a$.
- **Whitening.** The XOR of $K_0$ to $K_7$ before and after the rounds; see [key whitening](/key-whitening/).

## Variants and improvements

- **Key setup tradeoffs.** The paper describes several ways to compute g, from full precomputed tables to computing h on the fly. They trade key setup time against encryption speed and memory.
- **Reduced rounds.** Versions with fewer rounds are used in cryptanalysis, for example the 5-round attack above.
- **[Blowfish](/blowfish/).** The 64-bit predecessor by Schneier, with key-dependent tables made by running the cipher.

## When to use it

Twofish is still unbroken, but there is little reason to choose it for new work. AES is the standard, has hardware support in most processors, and has had more analysis. Twofish appears in disk encryption tools as an option, sometimes in a cascade with AES and [Serpent](/serpent/). Use it when a format requires it.

## Pitfalls

- **Byte order.** Words are little-endian, unlike Blowfish. The key bytes enter RS in their own order, and the vector $S$ is used in reverse order in h.
- **The rotation of $R_1$.** Line L7 rotates $R_1$ left by 8 before g. Without it, the test vectors fail.
- **Rotations differ in the two halves.** $R_2 \oplus F_0$ is rotated right after the XOR, but $R_3$ is rotated left before the XOR.
- **Output order.** Line L5 undoes the last swap: the ciphertext starts with $R_2$, not $R_0$.
- **Timing.** Table lookups at key-dependent indices leak through the cache.

## Implementations

## History

NIST called for AES candidates in 1997. The Twofish team submitted their design on 15 June 1998. NIST chose Twofish as one of the five finalists in August 1999, with MARS, [RC6](/rc6/), Rijndael and Serpent. In the informal vote at the third AES conference in April 2000, Twofish got the third highest number of positive votes, after Rijndael and Serpent. NIST announced Rijndael as the AES in October 2000.

## References
