---
tag: 8W4VPR
kind: algorithm
slug: aria
name: ARIA
area: cryptography/symmetric-ciphers
level: advanced
summary: The Korean standard 128-bit block cipher (KS X 1213, RFC 5794), an involutional SPN with 12, 14 or 16 rounds, two S-box layers and a binary diffusion matrix of branch number 8.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {b: the number of 16-byte blocks}
  time: {worst: Θ(b), average: Θ(b), best: Θ(b)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2003
  people: [Daesung Kwon]
  note: Daesung Kwon and coauthors from Korean universities and the National Security Research Institute presented ARIA at ICISC 2003. Korea made it the standard KS X 1213 in 2004, and the IETF published it as RFC 5794 in 2010.
prereqs: [substitution-permutation-network, s-box, key-schedule]
see_also: [advanced-encryption-standard, camellia, sm4, kuznyechik, block-cipher, differential-cryptanalysis, linear-cryptanalysis, gf2-polynomial-arithmetic]
sources:
  - paper: doi:10.1007/978-3-540-24691-6_32
    title: Daesung Kwon and others, New block cipher ARIA, Information Security and Cryptology (ICISC 2003), LNCS 2971, Springer, 2004
    locator: the structure of the cipher, the two types of S-box layer, the diffusion layer and its branch number, and the security analysis
  - url: "https://www.rfc-editor.org/rfc/rfc5794"
    title: A description of the ARIA encryption algorithm, RFC 5794, IETF, March 2010
    locator: Section 2.2 (key scheduling), Section 2.3 (encryption and decryption), Section 2.4 (the round functions, the S-boxes and the diffusion layer A) and Appendix A (example data)
  - paper: "KS X 1213, 128-bit block encryption algorithm ARIA, Korean Agency for Technology and Standards, 2004"
    locator: the national standard; RFC 5794 describes the same cipher
---

ARIA is a [block cipher](/block-cipher/) on 128-bit blocks with keys of 128, 192 or 256 bits, the Korean national standard KS X 1213. It is a [substitution-permutation network](/substitution-permutation-network/) of 12, 14 or 16 rounds. Its odd rounds and even rounds use two different S-box layers, each the inverse of the other, and both use one diffusion layer $A$ that is its own inverse. Because of this, decryption is the same code as encryption with other round keys. ARIA has the same interface as [AES](/advanced-encryption-standard/) and uses the AES S-box as one of its four S-boxes.

**Notation.** A 128-bit value $x$ is 16 bytes $x_0 \| \ldots \| x_{15}$, with $x_0$ the most significant. $n$ is the number of rounds: 12, 14 or 16 for a key of 128, 192 or 256 bits. $ek_1, \ldots, ek_{n+1}$ are the encryption round keys. $\oplus$ is XOR, and $\ggg s$ and $\lll s$ are rotations of a 128-bit value by $s$ places. $K$ is the key and $b$ is the number of blocks.

## In plain words

ARIA keeps the block as 16 bytes. Each round first mixes in a round key. Then it replaces each byte by a table lookup, with four different tables that it uses in turn. Then it mixes the bytes: each new byte is the XOR of seven old bytes, chosen so that a change in a few bytes spreads to many bytes.

The rounds come in two kinds that alternate. The second kind uses the tables that undo the tables of the first kind. The mixing step undoes itself when you apply it twice. Because of these two facts, the same steps decrypt a block when you use the round keys in reverse order after one small change to them. This lets a chip use one circuit for both directions.

## The problem

ARIA computes a permutation $E_K$ of $\{0,1\}^{128}$ for each key $K$ of 16, 24 or 32 bytes, and its inverse $D_K$. Messages longer than one block need a mode of operation such as [CBC](/cbc-mode/), [CTR](/ctr-mode/) or [GCM](/gcm-mode/). The security goal is that $E_K$ is a [pseudorandom permutation](/pseudorandom-permutation/). There is no proof of this: the designers bound the number of active S-boxes, and the rest rests on the absence of a known attack.

## The algorithm

```pseudo id=main
ARIA-ENCRYPT(ek, x)                         ▷ ek has n + 1 round keys
L1  for r ← 1 to n − 1 do
L2      if r is odd then x ← FO(x, ek_r)
L3      else x ← FE(x, ek_r)
L4  return SL2(x ⊕ ek_n) ⊕ ek_{n+1}

FO(x, k)
L5  return A(SL1(x ⊕ k))
FE(x, k)
L6  return A(SL2(x ⊕ k))
SL1(x)
L7  return SB1(x0) ‖ SB2(x1) ‖ SB3(x2) ‖ SB4(x3) ‖ SB1(x4) ‖ ... ‖ SB4(x15)
SL2(x)
L8  return SB3(x0) ‖ SB4(x1) ‖ SB1(x2) ‖ SB2(x3) ‖ SB3(x4) ‖ ... ‖ SB2(x15)
A(x)
L9  return y0 ‖ ... ‖ y15, where y_i is the XOR of the 7 bytes x_j in row i of the table of A

KEY-SCHEDULE(K)
L10 (KL, KR) ← K followed by zeros up to 256 bits, as two 128-bit values
L11 (CK1, CK2, CK3) ← (C1, C2, C3), (C2, C3, C1) or (C3, C1, C2) for a 128, 192 or 256-bit key
L12 W0 ← KL;  W1 ← FO(W0, CK1) ⊕ KR
L13 W2 ← FE(W1, CK2) ⊕ W0;  W3 ← FO(W2, CK3) ⊕ W1
L14 ek1 .. ek16 ← W0 ⊕ (W1 ⋙ s), W1 ⊕ (W2 ⋙ s), W2 ⊕ (W3 ⋙ s), (W0 ⋙ s) ⊕ W3, for s = 19, 31, −61, −31
L15 ek17 ← W0 ⊕ (W1 ⋘ 19)
```

A rotation to the right by $-61$ places is a rotation to the left by 61 places. The key schedule keeps only the first $n + 1$ round keys. $SB_1$ is the AES S-box, $SB_2$ is a second S-box built from the power map $x^{247}$ in the field of 256 elements and an affine map, $SB_3 = SB_1^{-1}$ and $SB_4 = SB_2^{-1}$. So $SL_2 = SL_1^{-1}$. The constants $C_1, C_2, C_3$ are the first 384 bits of the fractional part of $1/\pi$.

Decryption runs ARIA-ENCRYPT with the round keys $dk_1 = ek_{n+1}$, $dk_r = A(ek_{n+2-r})$ for $r = 2, \ldots, n$, and $dk_{n+1} = ek_1$.

The Python code for this page is for study only. It is not constant time, because each S-box lookup uses a secret index. Do not use it to protect real data. Use the ARIA or AES code of a validated library such as OpenSSL instead.

## Example

Take the 128-bit example of RFC 5794, Appendix A.1: the key is 000102030405060708090A0B0C0D0E0F and the plaintext is 00112233445566778899AABBCCDDEEFF. Line L12 gives $W_1$ = 2AFBEA741E1746DD55C63BA1AFCEA0A5, and lines L14 and L15 give 13 round keys, from $ek_1$ = D415A75C794B85C5E0D2A0B3CB793BF6 to $ek_{13}$ = 0F0AA16DAEE61BD7DFEE5A599970FB35.

| step | state |
|---|---|
| plaintext | 00112233445566778899AABBCCDDEEFF |
| round 1, FO with $ek_1$ | 7FC7F12BEFD0A0791DE87FA96B469F52 |
| round 2, FE with $ek_2$ | AC8DE17E49F7C5117618993162B189E9 |
| round 11, FO with $ek_{11}$ | E7E0D2457ED73D23D481424095AFDCA0 |
| line L4 with $ek_{12}$ and $ek_{13}$ | D718FBD6AB644C739DA95F3BE6451778 |

The last value is the ciphertext of the RFC. The test file checks the three examples of Appendix A in both directions, and three of the round keys of A.1.

## Correctness

Decryption inverts encryption for every key. Two facts make the same code work in both directions. First, $SL_2$ is the inverse of $SL_1$, because $SB_3 = SB_1^{-1}$ and $SB_4 = SB_2^{-1}$ sit in the same byte positions. Second, $A$ is linear and $A(A(x)) = x$. So the inverse of a round $x \mapsto A(SL_1(x \oplus k))$ is $y \mapsto SL_2(A(y)) \oplus k$, and the linearity of $A$ moves each key XOR across the next $A$ as an XOR with $A(k)$. The [proof](proofs/correctness.md) gives the full argument and shows why the number of rounds must be even.

## Complexity

A block costs $n$ rounds, which are 12, 14 or 16, and each round costs 16 S-box lookups and one application of $A$, which is 96 byte XORs in the direct form (6 for each of the 16 output bytes). So $b$ blocks cost $\Theta(b)$ time. The round keys take $n + 1$ values of 128 bits, which is $\Theta(1)$ space. Key setup costs three rounds and 13 to 17 XORs with rotations, so key changes are cheap. Decryption keys cost $n - 1$ extra applications of $A$.

## Properties

- **Involutional SPN.** Encryption and decryption use the same rounds, so one circuit serves both. Only the round keys differ.
- **Diffusion layer.** $A$ is a 16 by 16 binary matrix that acts on bytes, with branch number 8: a nonzero change in $m$ input bytes changes at least $8 - m$ output bytes. For comparison, the MixColumns step of AES has branch number 5 on each 4-byte column.
- **S-boxes.** $SB_1$ and $SB_2$ are each affine equivalent to a power map in the field of 256 elements, with best differential and linear probabilities $2^{-6}$.
- **Avalanche.** With the key of the example, a one-bit change of the plaintext changes on average 63.90 of the 128 ciphertext bits over 1000 random trials. The ideal value is 64.
- **No proof.** As with AES, there is no proof of security, only bounds on characteristics and the absence of a practical attack on the full cipher.

## Variants and improvements

- **Key sizes.** ARIA-128, ARIA-192 and ARIA-256 differ only in the number of rounds and in the order of the constants in line L11.
- **Versions.** The paper at ICISC 2003 describes an earlier version of the cipher. The Korean standard and RFC 5794 describe version 1.0, which the code for this page follows.
- **Modes and protocols.** RFC 6209 adds ARIA cipher suites to TLS, and RFC 8269 adds ARIA to SRTP.
- **Related ciphers.** [Camellia](/camellia/) has the same interface but is a [Feistel network](/feistel-network/). [Kuznyechik](/kuznyechik/), the Russian standard, is also an SPN on 128-bit blocks, with a linear layer over the field of 256 elements.

## When to use it

Use ARIA when a Korean standard or a partner needs it. It is sound, but AES has much wider hardware support and analysis, so AES is the default choice. In both cases, use an authenticated mode such as GCM.

## Pitfalls

- **The order of the S-boxes.** $SL_1$ and $SL_2$ use the four S-boxes in different orders. Exchanging them gives a cipher that still decrypts with the matching keys but fails the test vectors.
- **Decryption keys.** The middle decryption keys are $A(ek_i)$, not $ek_i$. With the plain reversed keys, decryption fails.
- **The last round.** Line L4 has no $A$ and has two key XORs. A last round with $A$ gives a different cipher.
- **Rotation directions.** Line L14 uses rotations to the right by 19 and 31 and to the left by 61 and 31. Only the test vectors find a wrong direction.
- **Table lookups and timing.** An S-box lookup at a secret index can leak through the cache. Use a constant-time library.

## Implementations

## History

A team from Korean universities and the National Security Research Institute designed ARIA, and Daesung Kwon and coauthors presented it at ICISC 2003. Korea made version 1.0 the national standard KS X 1213 in 2004. The IETF published it as RFC 5794 in 2010, and later RFCs added it to TLS and SRTP.

## References
