---
tag: JV176X
kind: algorithm
slug: camellia
name: Camellia
area: cryptography/symmetric-ciphers
level: advanced
summary: A 128-bit block Feistel cipher by NTT and Mitsubishi Electric (2000), with 18 or 24 rounds and FL layers. It is in RFC 3713 and ISO/IEC 18033-3, and is a common alternative to AES.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {b: the number of 16-byte blocks}
  time: {worst: Θ(b), average: Θ(b), best: Θ(b)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2000
  people: [Kazumaro Aoki, Tetsuya Ichikawa, Masayuki Kanda, Mitsuru Matsui, Shiho Moriai, Junko Nakajima, Toshio Tokita]
  note: NTT and Mitsubishi Electric designed Camellia in 2000 and presented it at Selected Areas in Cryptography 2000. The IETF published it as RFC 3713 in 2004.
prereqs: [feistel-network, s-box, key-schedule]
see_also: [advanced-encryption-standard, aria, sm4, data-encryption-standard, block-cipher, differential-cryptanalysis, linear-cryptanalysis, key-whitening]
sources:
  - paper: doi:10.1007/3-540-44983-3_4
    title: "Kazumaro Aoki, Tetsuya Ichikawa, Masayuki Kanda, Mitsuru Matsui, Shiho Moriai, Junko Nakajima and Toshio Tokita, Camellia: a 128-bit block cipher suitable for multiple platforms, design and analysis, Selected Areas in Cryptography (SAC 2000), LNCS 2012, Springer, 2001"
    locator: the structure of the cipher, the design of the F-function, the S-boxes, the P-function and the FL-function, and the security evaluation against differential and linear cryptanalysis
  - url: "https://www.rfc-editor.org/rfc/rfc3713"
    title: Mitsuru Matsui, Junko Nakajima and Shiho Moriai, A description of the Camellia encryption algorithm, RFC 3713, April 2004
    locator: Section 2.2 (key scheduling), Section 2.3 (data randomizing), Section 2.4 (the F-function, the FL-function and the S-boxes) and Appendix A (example data)
  - paper: "ISO/IEC 18033-3, Information technology, Security techniques, Encryption algorithms, Part 3: Block ciphers"
    locator: the clause on Camellia, one of the 128-bit block ciphers of the standard
---

Camellia is a [block cipher](/block-cipher/) on 128-bit blocks with keys of 128, 192 or 256 bits. It is a [Feistel network](/feistel-network/) of 18 rounds for a 128-bit key and 24 rounds for longer keys. After every 6 rounds, it inserts a layer of the key-dependent linear functions FL and FL⁻¹, and it uses [key whitening](/key-whitening/) at both ends. NTT and Mitsubishi Electric designed it in 2000. It has the same interface as [AES](/advanced-encryption-standard/), and standards such as RFC 3713 and ISO/IEC 18033-3 list it as an alternative to AES.

**Notation.** A block is two 64-bit halves $D_1 \| D_2$, read big-endian. $kw_1, \ldots, kw_4$ are the whitening keys, $k_1, \ldots, k_R$ the round keys with $R = 18$ or $24$, and $ke_1, \ldots, ke_{R/3 - 2}$ the FL keys, all of 64 bits. $\oplus$ is XOR, $\wedge$ is AND, $\vee$ is OR, and $\mathrm{ROL}_s$ is rotation to the left by $s$ places. $K$ is the key and $b$ is the number of blocks.

## In plain words

Camellia cuts a block into a left half and a right half. It mixes a secret value into each half. Then, in each round, it sends one half through a mixing function and adds the result into the other half, and the next round goes the other way. The mixing function adds a round key, puts each of the eight bytes through a substitution table, and then mixes the eight bytes together so that each output byte depends on many input bytes.

After every six rounds, Camellia puts in a different layer: a small function on each half that uses AND, OR and a rotation with a secret key. This layer breaks up the regular pattern of the rounds. At the end, it mixes in two more secret values. Decryption is the same process with the keys in reverse order.

## The problem

Camellia computes a permutation $E_K$ of $\{0,1\}^{128}$ for each key $K$ of 16, 24 or 32 bytes, and its inverse $D_K$. Messages longer than one block need a mode of operation such as [CBC](/cbc-mode/), [CTR](/ctr-mode/) or [GCM](/gcm-mode/). The security goal is that $E_K$ is a [pseudorandom permutation](/pseudorandom-permutation/). There is no proof of this: the designers bound the probability of differential and linear characteristics, and the rest rests on the absence of a known attack.

## The algorithm

```pseudo id=main
CAMELLIA-ENCRYPT(kw, k, ke, M)              ▷ R = 18 or 24 round keys
L1  (D1, D2) ← M, as two 64-bit halves
L2  D1 ← D1 ⊕ kw1;  D2 ← D2 ⊕ kw2
L3  for r ← 1, 3, 5, ..., R − 1 do
L4      if r > 1 and r − 1 is a multiple of 6 then
L5          j ← (r − 1)/3 − 1;  D1 ← FL(D1, ke_j);  D2 ← FL⁻¹(D2, ke_{j+1})
L6      D2 ← D2 ⊕ F(D1, k_r)
L7      D1 ← D1 ⊕ F(D2, k_{r+1})
L8  return (D2 ⊕ kw3) ‖ (D1 ⊕ kw4)

F(X, k)
L9  x1 ‖ x2 ‖ ... ‖ x8 ← X ⊕ k, as eight bytes
L10 (t1, ..., t8) ← (s1(x1), s2(x2), s3(x3), s4(x4), s2(x5), s3(x6), s4(x7), s1(x8))
L11 return P(t1, ..., t8)                   ▷ each output byte is the XOR of 5 or 6 of the t_i

FL(X, k)
L12 (x1, x2) ← X and (k1, k2) ← k, as 32-bit halves
L13 x2 ← x2 ⊕ ROL_1(x1 ∧ k1)
L14 x1 ← x1 ⊕ (x2 ∨ k2)
L15 return x1 ‖ x2

KEY-SCHEDULE(K)
L16 (KL, KR) ← K split into two 128-bit values (KR ← 0 for a 128-bit key)
L17 (D1, D2) ← KL ⊕ KR;  D2 ← D2 ⊕ F(D1, Σ1);  D1 ← D1 ⊕ F(D2, Σ2)
L18 (D1, D2) ← (D1, D2) ⊕ KL;  D2 ← D2 ⊕ F(D1, Σ3);  D1 ← D1 ⊕ F(D2, Σ4)
L19 KA ← D1 ‖ D2
L20 KB ← two more such rounds on KA ⊕ KR with Σ5 and Σ6   ▷ used for 192-bit and 256-bit keys
L21 kw, k, ke ← 64-bit halves of KL, KR, KA, KB, each rotated left by a fixed amount
```

FL⁻¹ undoes FL: it computes $x_1 \leftarrow x_1 \oplus (x_2 \vee k_2)$ and then $x_2 \leftarrow x_2 \oplus \mathrm{ROL}_1(x_1 \wedge k_1)$. The S-box $s_1$ is a fixed table of 256 bytes. The other three come from it: $s_2(x) = \mathrm{ROL}_1(s_1(x))$, $s_3(x) = \mathrm{ROL}_7(s_1(x))$ and $s_4(x) = s_1(\mathrm{ROL}_1(x))$ on bytes. The six constants $\Sigma_1, \ldots, \Sigma_6$ are hex digits of square roots of small primes. For a 192-bit key, $KR$ is the last 64 bits followed by their complement. RFC 3713, Section 2.2, gives the table of rotations for line L21. For a 128-bit key, $k_1 \| k_2 = KA$, $kw_1 \| kw_2 = KL$, and $kw_3 \| kw_4 = \mathrm{ROL}_{111}(KA)$.

Decryption is the same network with the keys in reverse order: $kw_3, kw_4$ in line L2, $k_R, \ldots, k_1$ in the rounds, the FL keys reversed, and $kw_1, kw_2$ in line L8.

The Python code for this page is for study only. It is not constant time, because each S-box lookup uses a secret index. Do not use it to protect real data. Use the Camellia or AES code of a validated library such as OpenSSL instead.

## Example

Take the 128-bit example of RFC 3713, Appendix A: the key and the plaintext are both 0123456789ABCDEFFEDCBA9876543210. Lines L17 to L19 give $KA$ = AE71C3D55BA6BF1D 169240A795F89256, and so $k_1$ = AE71C3D55BA6BF1D and $k_2$ = 169240A795F89256. Line L2 XORs the key into the plaintext, which gives zero, because $kw_1 \| kw_2 = KL$ is equal to the plaintext here.

| step | $D_1$ | $D_2$ |
|---|---|---|
| line L2 | 0000000000000000 | 0000000000000000 |
| round 1: $F(D_1, k_1)$ = 77933E474A99FA36 | 0000000000000000 | 77933E474A99FA36 |
| round 2: $F(D_2, k_2)$ = D5BD24691D280080 | D5BD24691D280080 | 77933E474A99FA36 |
| rounds 3 to 6 | 695E2DBC2A7211D1 | 029D886D6C0DFB08 |
| line L5, FL and FL⁻¹ | 86B8F745AAE24AD9 | ED007390A60DBA29 |
| rounds 7 to 12, line L5, rounds 13 to 18 | 57D98D1F68B974BF | 2E4C6600B57CC4A0 |

Line L8 XORs $kw_3$ = 492B5738E1EAADD3 into $D_2$ and $kw_4$ = 5F8E8B492053CAFC into $D_1$, and swaps the halves. The result 67673138549669730857065648EABE43 is the ciphertext of the RFC. The test file checks the three examples of Appendix A, for 128-bit, 192-bit and 256-bit keys, in both directions.

## Correctness

Decryption inverts encryption for every set of subkeys. Each Feistel round changes one half by XOR with a function of the other half, so it is its own inverse, and F need not be invertible. Lines L13 and L14 each change one 32-bit half by XOR with a value that does not depend on that half, so FL⁻¹ undoes FL. The [proof](proofs/correctness.md) shows that the inverse of the whole network, after a swap of the halves is moved through each step, is the same network with the subkeys in reverse order.

## Complexity

A block costs $R$ calls of F, which are 18 or 24, plus 2 or 3 FL layers and 4 whitening XORs. Each call of F costs 8 S-box lookups and the byte XORs of P. So $b$ blocks cost $\Theta(b)$ time and the subkeys take $\Theta(1)$ space: 26 subkeys of 64 bits for a 128-bit key and 34 for a longer key. Key setup costs 4 calls of F for a 128-bit key and 6 for a longer key, plus rotations. This is cheap, so Camellia suits frequent key changes. A table implementation merges each S-box with P into tables of 64-bit words, as AES does with its T-tables.

## Properties

- **Feistel structure.** Encryption and decryption share one network, and F needs no inverse.
- **S-boxes.** $s_1$ is affine equivalent to the inverse map in the field of 256 elements, like the S-box of AES, so its best differential and linear probabilities are $2^{-6}$.
- **P-function.** P is a byte-wise linear map with branch number 5: a change in $m$ input bytes changes at least $5 - m$ output bytes. The designers use this to bound the number of active S-boxes over many rounds.
- **FL layers.** FL and FL⁻¹ are linear for a fixed key but depend on the key. They break the regular round structure, so that no two parts of the cipher are the same function. The designers added them as a margin against attacks that need a regular structure, such as the [slide attack](/slide-attack/).
- **Avalanche.** With the key of the example, a one-bit change of the plaintext changes on average 63.87 of the 128 ciphertext bits over 1000 random trials. The ideal value is 64.
- **No proof.** There is no proof of security. The designers bound differential and linear characteristics, and the published attacks reach only versions with fewer rounds.

## Variants and improvements

- **Key sizes.** Camellia-128 has 18 rounds and two FL layers. Camellia-192 and Camellia-256 have 24 rounds and three FL layers and use $KB$.
- **Modes.** Camellia uses the same modes as AES. RFCs define Camellia in TLS and IPsec, for example in CBC, CTR and GCM.
- **Other ciphers.** [ARIA](/aria/), the Korean standard, has the same interface but is a [substitution-permutation network](/substitution-permutation-network/). [SM4](/sm4/), the Chinese standard, is an unbalanced Feistel cipher with a 128-bit key only.

## When to use it

Use Camellia when a standard or a partner needs it, for example Japanese government systems that follow the CRYPTREC list. It is a sound cipher, but AES has wider hardware support, so AES is the default choice. In both cases, use an authenticated mode such as GCM.

## Pitfalls

- **Halves, not words.** The block is two 64-bit halves for F and four 32-bit words inside FL. A wrong split passes a round trip test, but fails the RFC vectors.
- **FL versus FL⁻¹.** Line L5 applies FL to the left half and FL⁻¹ to the right half. Exchanging them gives a different cipher.
- **The rotation table.** Line L21 has a separate table for each key size, with rotations past 64, such as 77, 94 and 111. A wrong entry still gives a permutation, so only the test vectors find it.
- **The final swap.** Line L8 outputs $D_2$ first. Without the swap, decryption with reversed keys fails.
- **Table lookups and timing.** An S-box lookup at a secret index can leak through the cache. Use a constant-time library.

## Implementations

## History

NTT and Mitsubishi Electric designed Camellia in 2000. Mitsuru Matsui of Mitsubishi Electric, one of the authors, had published [linear cryptanalysis](/linear-cryptanalysis/) in 1993, and the design bounds both differential and linear characteristics. Aoki and six coauthors presented it at Selected Areas in Cryptography in 2000. The European NESSIE project selected Camellia in 2003, and the Japanese CRYPTREC list includes it. The IETF published it as RFC 3713 in 2004, and ISO/IEC 18033-3 includes it.

## References
