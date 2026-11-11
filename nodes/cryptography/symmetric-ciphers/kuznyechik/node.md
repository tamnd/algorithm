---
tag: 0Z0TM1
kind: algorithm
slug: kuznyechik
name: Kuznyechik
aliases:
- Grasshopper
area: cryptography/symmetric-ciphers
level: advanced
summary: The 128-bit block cipher of the Russian standard GOST R 34.12-2015. It is a substitution-permutation network with a 256-bit key, 9 rounds and a linear layer over GF(2^8).
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of 16-byte blocks}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2015
  people: [Center for Information Protection and Special Communications of the FSB, InfoTeCS]
  note: Kuznyechik became part of GOST R 34.12-2015 on 19 June 2015, next to the old cipher, which the standard renamed Magma. RFC 7801 of 2016 gives an English text.
prereqs: [substitution-permutation-network, s-box, gf2-polynomial-arithmetic]
see_also: [gost-28147-89, advanced-encryption-standard, feistel-network, key-schedule, block-cipher, aria, camellia]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc7801"
    title: Vasily Dolmatov (editor), GOST R 34.12-2015, block cipher "Kuznyechik", RFC 7801, March 2016
    locator: Section 2 (general information), Section 4.1 (the S-box pi), Section 4.2 (the linear map l), Section 4.3 (the transformations X, S, R, L and F), Section 4.4 (the key schedule), Section 4.5 (encryption and decryption) and Section 5 (the examples)
  - paper: doi:10.1007/978-3-662-49890-3_15
    title: Alex Biryukov, Léo Perrin and Aleksei Udovenko, Reverse-engineering the S-box of Streebog, Kuznyechik and STRIBOBr1, Eurocrypt 2016, LNCS 9665, Springer, 2016
    locator: the abstract and the decomposition of the S-box as a 2-round Feistel-like structure with finite field multiplication, between linear layers
---

Kuznyechik, Russian for grasshopper, is a [block cipher](/block-cipher/) on 128-bit blocks with a 256-bit key. It is one of the two ciphers of the Russian standard GOST R 34.12-2015; the other is the old [GOST 28147-89](/gost-28147-89/), renamed Magma. Kuznyechik is a [substitution-permutation network](/substitution-permutation-network/) like [AES](/advanced-encryption-standard/): each of its 9 rounds adds a round key, puts each byte through an 8-bit [S-box](/s-box/), and applies a linear map over the field $GF(2^8)$. The key schedule is a [Feistel network](/feistel-network/) that uses the round of the cipher as its function.

**Notation.** A block is 16 bytes $a_{15} \| \cdots \| a_0$, with $a_{15}$ the first byte. $\oplus$ is XOR. $\pi$ is the S-box, a permutation of the bytes given as a table in RFC 7801. Bytes are elements of the field $Q = GF(2)[x]/(p(x))$ with $p(x) = x^8 + x^7 + x^6 + x + 1$, and a product such as $148 \cdot a$ is a product in $Q$, where 148 stands for the polynomial with those bits. $X[k](a) = k \oplus a$, $S$ applies $\pi$ to each byte, and $L$ is the linear map of lines L6 to L9. $n$ is the number of blocks.

## In plain words

Kuznyechik works on a block of 16 bytes. In each of 9 rounds, it mixes a part of the key into the block, replaces each byte with a fixed table, and then mixes all bytes together with a step that makes every output byte depend on every input byte. After the last round, it mixes in one more part of the key.

The mixing step works like a shift register. Sixteen times, it computes one new byte from all 16 bytes, puts it at the front, and drops the last byte. The parts of the key come from the main key by 32 rounds of the same kind of work.

## The problem

Kuznyechik computes a permutation $E_K$ of $\{0,1\}^{128}$ for each key $K$ of 256 bits, and its inverse $D_K$. Messages longer than one block need a mode of operation, such as [CTR](/ctr-mode/). The goal is that $E_K$ behaves like a [pseudorandom permutation](/pseudorandom-permutation/). The 128-bit block removes the data limit of the 64-bit Magma at practical scales.

## The algorithm

```pseudo id=main
KUZNYECHIK-ENCRYPT(K₁ .. K₁₀, a)
L1  for i ← 1 to 9 do
L2      a ← a ⊕ Kᵢ                                     ▷ X[Kᵢ]
L3      a ← π(a₁₅) ‖ … ‖ π(a₀)                          ▷ S
L4      a ← L(a)
L5  return a ⊕ K₁₀

L(a)
L6  repeat 16 times
L7      a ← l(a₁₅, …, a₀) ‖ a₁₅ ‖ … ‖ a₁               ▷ R
L8  return a

l(a₁₅, …, a₀)
L9  return 148·a₁₅ ⊕ 32·a₁₄ ⊕ 133·a₁₃ ⊕ 16·a₁₂ ⊕ 194·a₁₁ ⊕ 192·a₁₀ ⊕ 1·a₉ ⊕ 251·a₈
           ⊕ 1·a₇ ⊕ 192·a₆ ⊕ 194·a₅ ⊕ 16·a₄ ⊕ 133·a₃ ⊕ 32·a₂ ⊕ 148·a₁ ⊕ 1·a₀

KUZNYECHIK-KEY-SCHEDULE(K)                              ▷ C_j = L(j as a 128-bit block)
L10 (a₁, a₀) ← (the first 16 bytes of K, the last 16 bytes of K);  (K₁, K₂) ← (a₁, a₀)
L11 for i ← 1 to 4 do
L12     for j ← 1 to 8 do
L13         (a₁, a₀) ← (L(S(a₁ ⊕ C_(8(i−1)+j))) ⊕ a₀, a₁)    ▷ F[C]
L14     (K_(2i+1), K_(2i+2)) ← (a₁, a₀)
L15 return K₁, …, K₁₀
```

Line L7 is one step of a linear feedback shift register over $Q$, and 16 steps replace every byte. The round constants $C_1, \ldots, C_{32}$ are the images under $L$ of the numbers 1 to 32. The key schedule runs 32 Feistel rounds and keeps the state after each 8 rounds as two round keys.

Decryption undoes each step in reverse order: $a \leftarrow a \oplus K_{10}$, then for $i = 9$ down to 1, $a \leftarrow S^{-1}(L^{-1}(a)) \oplus K_i$. Here $S^{-1}$ uses the inverse table of $\pi$, and $L^{-1}$ is 16 steps of $R^{-1}(a_{15} \| \cdots \| a_0) = a_{14} \| \cdots \| a_0 \| l(a_{14}, \ldots, a_0, a_{15})$.

The Python code for this page is for study only. It is not constant time, because the S-box is a table indexed by secret bytes. Do not use it to protect real data. Use a validated library that implements GOST R 34.12-2015, or AES from a library such as OpenSSL.

## Example

Take the examples of RFC 7801, Section 5. The key is 8899AABBCCDDEEFF0011223344556677FEDCBA98765432100123456789ABCDEF, so line L10 gives $K_1$ = 8899AABBCCDDEEFF0011223344556677 and $K_2$ = FEDCBA98765432100123456789ABCDEF. The first round constant is $C_1$ = 6EA276726C487AB85D27BD10DD849401. The key schedule then gives $K_3$ = DB31485315694343228D6AEF8CC78C44 and $K_{10}$ = 72E9DD7416BCF45B755DBAA88E4A4043.

The plaintext is 1122334455667700FFEEDDCCBBAA9988.

| step | block |
|---|---|
| line L2, round 1 | 99BB99FF99BB99FFFFFFFFFFFFFFFFFF |
| line L3, round 1 | E87DE8B6E87DE8B6B6B6B6B6B6B6B6B6 |
| line L4, round 1 | E297B686E355B0A1CF4A2F9249140830 |
| round 2 | 285E497A0862D596B36F4258A1C69072 |
| round 9 | 0D8E40E4A800D06B2F1B37EA379EAD8E |
| line L5 | 7F679D90BEBC24305A468D42B9D4EDCD |

After line L2, the block has only the bytes 99, BB and FF, so after line L3 it has only $\pi$(99) = E8, $\pi$(BB) = 7D and $\pi$(FF) = B6. Line L4 then spreads these bytes over the whole block. The last row is the ciphertext of Section 5.5 of RFC 7801. The test file checks the examples for $S$, $R$, $L$, the key schedule and encryption and decryption.

## Correctness

Each round is a bijection: the key XOR is its own inverse, $S$ is a bijection because $\pi$ is a permutation, and $L$ is a bijection because each step $R$ can be undone, as the formula for $R^{-1}$ shows. So encryption is a bijection, and the decryption above inverts it. The key schedule does not need to be invertible. The [proof](proofs/correctness.md) gives the details, including why $R^{-1}$ is correct.

## Complexity

A block costs 9 rounds. In a direct form, each round costs 16 S-box lookups and 16 steps $R$, each with 16 multiplications in $Q$. So $n$ blocks cost $\Theta(n)$ time. Real implementations merge $S$ and $L$ into 16 tables of 256 entries of 16 bytes each, so a round costs 16 lookups and XORs, as with AES. The cipher keeps 10 round keys, which is $\Theta(1)$ extra space. The key schedule costs 32 rounds of the cipher, once for each key.

## Properties

- **A linear map from a shift register.** $L$ is 16 steps of one simple step, which suits hardware. Its matrix over $Q$ is the 16th power of the matrix of $R$.
- **An S-box with a hidden structure.** The designers did not publish how they chose $\pi$. Biryukov, Perrin and Udovenko (Eurocrypt 2016) found that it decomposes into a kind of 2-round Feistel network with field multiplication in place of XOR, between two linear layers. Some of its small 4-bit parts have weak properties. The same S-box is in the hash function Streebog.
- **Key schedule from the cipher.** The round keys come from Feistel rounds with the round function $LSX$, so the key schedule reuses the code of encryption.
- **Avalanche.** With the key of the example, a one-bit change of the plaintext changes on average 63.80 of the 128 ciphertext bits over 500 random trials. The ideal value is 64.

## Variants and improvements

- **[Magma](/gost-28147-89/).** The other cipher of GOST R 34.12-2015, a Feistel network with a 64-bit block.
- **Other ciphers of the same shape.** [AES](/advanced-encryption-standard/), [ARIA](/aria/) and [Camellia](/camellia/) are national or international standards with 128-bit blocks. AES and ARIA are substitution-permutation networks, as Kuznyechik is.

## When to use it

Use Kuznyechik where Russian standards require it, through a validated library. Elsewhere, AES has more analysis, more support and hardware instructions on most processors. The hidden structure of the S-box gives no known attack, but it is a reason for some users to prefer ciphers with a public design rationale.

## Pitfalls

- **The text of $l$ in RFC 7801.** Section 4.2 of RFC 7801 writes the second term as $32 \cdot a_{15}$. It must be $32 \cdot a_{14}$, as in line L9 and as the examples of Section 5 confirm.
- **The field polynomial.** $Q$ uses $x^8 + x^7 + x^6 + x + 1$, not the polynomial of AES.
- **Byte order.** $a_{15}$ is the first byte of the block, and $R$ puts the new byte at the front.
- **The round constants.** $C_j$ is $L$ applied to the number $j$, placed in the last byte of the block.
- **Timing.** Table lookups at secret indices can leak through the cache.

## Implementations

## History

The Center for Information Protection and Special Communications of the Federal Security Service of the Russian Federation developed Kuznyechik with InfoTeCS. The Federal Agency on Technical Regulating and Metrology approved GOST R 34.12-2015 on 19 June 2015. The standard contains Kuznyechik and Magma. RFC 7801 of 2016 gives an English text of the Kuznyechik part. In 2016 Biryukov, Perrin and Udovenko published their analysis of the S-box.

## References
