---
tag: 9DN8TB
kind: algorithm
slug: sm4
name: SM4
aliases:
- SMS4
area: cryptography/symmetric-ciphers
level: advanced
summary: The Chinese national block cipher GB/T 32907-2016, first used in WAPI. It is an unbalanced Feistel network with a 128-bit block, a 128-bit key and 32 rounds.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of 16-byte blocks}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2006
  people: [Shu-Wang Lu]
  note: Lu designed SMS4 for the Chinese wireless LAN standard WAPI of 2003. The cipher was published on its own in 2006, renamed SM4 in 2012, and became the national standard GB/T 32907 in 2016.
prereqs: [feistel-network, s-box, block-cipher]
see_also: [advanced-encryption-standard, kuznyechik, aria, camellia, differential-cryptanalysis, linear-cryptanalysis, key-schedule]
sources:
  - url: "https://datatracker.ietf.org/doc/html/draft-ribose-cfrg-sm4-10"
    title: Ronald Henry Tse, Wai Kit Wong and Markku-Juhani O. Saarinen, The SM4 blockcipher algorithm and its modes of operations, Internet-Draft draft-ribose-cfrg-sm4-10, April 2018
    locator: Section 1.2 (history), Sections 4 to 7 (the structure, the functions T and T', the S-box, encryption, decryption and the key schedule with FK and CK), Section 11 (the summary of cryptanalysis) and Appendix A.1 (the examples of GB/T 32907-2016)
  - paper: "GB/T 32907-2016, Information security technology, SM4 block cipher algorithm, Standardization Administration of the People's Republic of China, 2016"
    locator: the national standard; Sections 1 to 7 of the Internet-Draft follow its sections, and Appendix A.1 of the draft repeats its examples
  - paper: "ISO/IEC 18033-3:2010/Amd 1:2021, Information technology, Security techniques, Encryption algorithms, Part 3: Block ciphers, Amendment 1: SM4"
    locator: the amendment that adds SM4 to the block ciphers of ISO/IEC 18033-3
---

SM4 is a [block cipher](/block-cipher/) with a 128-bit block and a 128-bit key. It is the block cipher of the Chinese commercial cryptography standards, and was first called SMS4. Its structure is an unbalanced [Feistel network](/feistel-network/) on four 32-bit words: each of 32 rounds computes one new word from the other three and a round key, and XORs it into the fourth. The round function is four 8-bit [S-boxes](/s-box/) followed by a linear map of XORs and rotations. The key schedule has the same shape as encryption.

**Notation.** A block is four 32-bit words $X_0, X_1, X_2, X_3$, read big-endian from the bytes. The key is four words $MK_0, \ldots, MK_3$. $\oplus$ is XOR and $x \lll s$ is rotation to the left by $s$ places. $S$ is the 8-bit S-box, given as a table in the standard. For a word $A$ with bytes $a_0 \| a_1 \| a_2 \| a_3$, $\tau(A) = S(a_0) \| S(a_1) \| S(a_2) \| S(a_3)$. $T(A) = L(\tau(A))$ and $T'(A) = L'(\tau(A))$, with $L'(B) = B \oplus (B \lll 13) \oplus (B \lll 23)$. $FK_0, \ldots, FK_3$ and $CK_0, \ldots, CK_{31}$ are fixed constants. $n$ is the number of blocks.

## In plain words

SM4 cuts a block into four words. In each of 32 rounds, it mixes three of the words and a part of the key into one word, puts each byte of that word through a fixed table, and spreads the bits with a few turns and mixes. It mixes the result into the fourth word. Then the words move one place along, and the new word goes to the end.

After 32 rounds, the cipher outputs the last four words in reverse order. This reverse order makes decryption the same process as encryption, with the parts of the key in reverse order. The parts of the key come from the key in the same way, with a different spreading step and fixed constants.

## The problem

SM4 computes a permutation $E_K$ of $\{0,1\}^{128}$ for each key $K$ of 128 bits, and its inverse $D_K$. Messages longer than one block need a mode of operation; the Internet-Draft describes ECB, [CBC](/cbc-mode/), [CFB](/cfb-mode/), [OFB](/ofb-mode/) and [CTR](/ctr-mode/) with SM4. The goal is that $E_K$ behaves like a [pseudorandom permutation](/pseudorandom-permutation/).

## The algorithm

```pseudo id=main
SM4-ENCRYPT(rk₀ .. rk₃₁, X₀, X₁, X₂, X₃)
L1  for i ← 0 to 31 do
L2      X_(i+4) ← X_i ⊕ T(X_(i+1) ⊕ X_(i+2) ⊕ X_(i+3) ⊕ rk_i)
L3  return (X₃₅, X₃₄, X₃₃, X₃₂)

T(A)
L4  B ← τ(A)                                          ▷ four S-box lookups
L5  return B ⊕ (B ⋘ 2) ⊕ (B ⋘ 10) ⊕ (B ⋘ 18) ⊕ (B ⋘ 24)    ▷ L(B)

SM4-KEY-SCHEDULE(MK₀ .. MK₃)
L6  for i ← 0 to 3 do K_i ← MK_i ⊕ FK_i
L7  for i ← 0 to 31 do
L8      K_(i+4) ← K_i ⊕ T′(K_(i+1) ⊕ K_(i+2) ⊕ K_(i+3) ⊕ CK_i)
L9  return (K₄, …, K₃₅) as (rk₀, …, rk₃₁)
```

Line L2 is the round function $F(X_i, X_{i+1}, X_{i+2}, X_{i+3}, rk_i)$ of the standard. Only one word in four changes in each round, so the network is unbalanced: the part that the round function reads is three times as wide as the part it changes. The constants are $FK$ = (A3B1BAC6, 56AA3350, 677D9197, B27022DC), and byte $j$ of $CK_i$ is $(4i + j) \cdot 7 \bmod 256$, so $CK_0$ = 00070E15.

Decryption is line L1 to line L3 with the round keys in reverse order, $rk_{31}, \ldots, rk_0$.

The Python code for this page is for study only. It is not constant time, because the S-box is a table indexed by secret bytes. Do not use it to protect real data. Use SM4 or AES from a validated library such as OpenSSL instead.

## Example

Take Example 1 of GB/T 32907-2016, as given in Appendix A.1.1 of the Internet-Draft. The key and the plaintext are both 0123456789ABCDEFFEDCBA9876543210, so $X_0$ = 01234567, $X_1$ = 89ABCDEF, $X_2$ = FEDCBA98 and $X_3$ = 76543210.

Line L6 gives $K_0, \ldots, K_3$ = A292FFA1, DF01FEBF, 99A12B0F, C42410CC, and the key schedule gives $rk_0$ = F12186F9. In round 1, the input of $T$ is $X_1 \oplus X_2 \oplus X_3 \oplus rk_0$ = F002C39E. Line L4 gives $B$ = 18E992B1, line L5 gives $T$ = 26D99622, and line L2 gives $X_4$ = 01234567 ⊕ 26D99622 = 27FAD345.

| round $i + 1$ | $rk_i$ | new word $X_{i+4}$ |
|---|---|---|
| 1 | F12186F9 | 27FAD345 |
| 2 | 41662B61 | A18B4CB2 |
| 3 | 5A6AB19A | 11C1E22A |
| 4 | 7BA92077 | CC13E2EE |
| 29 | 428D3654 | 536E4246 |
| 30 | 62293496 | 86B3E94F |
| 31 | 01CF72E5 | D206965E |
| 32 | 9124A012 | 681EDF34 |

Line L3 outputs $(X_{35}, X_{34}, X_{33}, X_{32})$, so the ciphertext is 681EDF34D206965E86B3E94F536E4246. The draft lists all 32 round keys and words, and the test file checks Example 1 and Example 4 of the draft in both directions.

## Correctness

Each round maps $(X_i, X_{i+1}, X_{i+2}, X_{i+3})$ to $(X_{i+1}, X_{i+2}, X_{i+3}, X_{i+4})$, and $X_i$ can be found again as $X_{i+4} \oplus T(X_{i+1} \oplus X_{i+2} \oplus X_{i+3} \oplus rk_i)$, since the XOR of three words does not depend on their order. So the round is a bijection whatever $T$ is. The reverse order of line L3 makes this inverse the same computation as encryption, with the round keys reversed. The [proof](proofs/correctness.md) gives the details.

## Complexity

A block costs 32 rounds. Each round costs 3 XORs to form the input, 4 S-box lookups, 4 rotations and 5 XORs. So $n$ blocks cost $\Theta(n)$ time. The cipher keeps 32 round keys, which is $\Theta(1)$ extra space. Fast software merges $\tau$ and $L$ into four tables of 256 words, so a round costs 4 lookups and a few XORs.

Section 11 of the Internet-Draft summarizes the published attacks. The best in its table reach 24 of the 32 rounds: a linear attack with time $2^{122.6}$ and data $2^{122.6}$. The draft states that no published attack reaches beyond 24 rounds.

## Properties

- **Unbalanced Feistel network.** Each round changes one word of four. Decryption needs no inverse of $T$, and it is the same circuit as encryption.
- **The linear map $L$.** The draft states that the round function is of SP type with branch number 5, and cites a proof that 27 rounds have at least 22 active S-boxes.
- **The S-box.** Section 10.2 of the draft gives its maximum differential probability as $2^{-6}$, its nonlinearity as 112 and its maximum linear advantage as $2^{-4}$.
- **Same structure for the key schedule.** The key schedule uses $T'$, with fewer rotations, and the constants $FK$ and $CK$, so that the round keys do not repeat the structure of encryption exactly.
- **Avalanche.** With the key of the example, a one-bit change of the plaintext changes on average 63.56 of the 128 ciphertext bits over 1000 random trials. The ideal value is 64.

## Variants and improvements

- **SMS4.** The name of the cipher in the publications of 2003 and 2006. The algorithm is the same.
- **Other national ciphers.** [Kuznyechik](/kuznyechik/) (Russia), [ARIA](/aria/) (Korea) and [Camellia](/camellia/) (Japan) are 128-bit block ciphers from other national standards. [AES](/advanced-encryption-standard/) is the international default.

## When to use it

Use SM4 where Chinese standards require it, for example in products for the Chinese market, through a validated library. Elsewhere, AES has more analysis and wider support. SM4 has a 128-bit key only, so it has no option for a larger key.

## Pitfalls

- **The output order.** Line L3 outputs the last four words in reverse order. An implementation that outputs them in order gives a different cipher, and its decryption with reversed keys fails.
- **$T$ and $T'$.** Encryption uses $L$ with rotations by 2, 10, 18 and 24. The key schedule uses $L'$ with rotations by 13 and 23.
- **Byte order.** Words are big-endian, and $a_0$ is the high byte of a word.
- **Example 3 of the draft.** It encrypts a block one million times with the same key. It is a slow test in Python, and this page does not run it.
- **Timing.** Table lookups at secret indices can leak through the cache.

## Implementations

## History

Shu-Wang Lu designed the cipher, under the name SMS4, for WAPI, the Chinese standard for the security of wireless networks, GB 15629.11-2003. The cipher was published on its own in 2006. In 2012 it became the industry standard GM/T 0002-2012 under the name SM4, and in 2016 the national standard GB/T 32907-2016. A proposal to add SMS4 to IEEE 802.11i did not succeed. ISO/IEC added SM4 to the block ciphers of ISO/IEC 18033-3 in an amendment of 2021.

## References
