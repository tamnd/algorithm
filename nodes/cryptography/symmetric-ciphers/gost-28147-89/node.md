---
tag: QNHVZN
kind: algorithm
slug: gost-28147-89
name: GOST 28147-89
aliases:
- Magma
area: cryptography/symmetric-ciphers
level: advanced
summary: The Soviet and Russian standard block cipher, a 32-round Feistel network on 64-bit blocks with a 256-bit key. Its 2015 form with fixed S-boxes is called Magma.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of 8-byte blocks}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 1989
  people: [Government Committee of the USSR for Standards]
  note: GOST 28147-89 was the standard cipher of the USSR from 1989 and later of Russia. GOST R 34.12-2015 kept it under the name Magma, with a fixed set of S-boxes.
prereqs: [feistel-network, s-box, block-cipher]
see_also: [kuznyechik, data-encryption-standard, advanced-encryption-standard, key-schedule, slide-attack, meet-in-the-middle-attack, birthday-attack]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc5830"
    title: Vasily Dolmatov (editor), GOST 28147-89, encryption, decryption, and message authentication code (MAC) algorithms, RFC 5830, March 2010
    locator: Section 4 (general statements, the S-box remark), Section 5 (the electronic codebook mode, 32 rounds) and Sections 6 to 8 (the other modes and the MAC)
  - url: "https://www.rfc-editor.org/rfc/rfc8891"
    title: Vasily Dolmatov (editor) and Dmitry Baryshkov, GOST R 34.12-2015, block cipher "Magma", RFC 8891, September 2020
    locator: Section 4.1 (the S-boxes), Section 4.2 (the transformations t, g, G and G*), Section 4.3 (the key schedule), Section 5 (encryption and decryption), Appendix A (test examples) and Appendix B (the differences from GOST 28147-89)
  - url: "https://www.rfc-editor.org/rfc/rfc4357"
    title: Vladimir Popov, Igor Kurepkin and Serguei Leontiev, Additional cryptographic algorithms for use with GOST 28147-89, GOST R 34.10-94, GOST R 34.10-2001, and GOST R 34.11-94 algorithms, RFC 4357, January 2006
    locator: Section 2.3.2 (CryptoPro key meshing), Section 8.1 and Section 11.1 (the S-box parameter sets)
  - paper: doi:10.1007/978-3-642-21702-9_17
    title: Takanori Isobe, A single-key attack on the full GOST block cipher, Fast Software Encryption 2011, LNCS 6733, Springer, 2011
    locator: pp. 290-305
  - paper: doi:10.1007/978-3-642-34047-5_2
    title: Itai Dinur, Orr Dunkelman and Adi Shamir, Improved attacks on full GOST, Fast Software Encryption 2012, LNCS 7549, Springer, 2012
    locator: pp. 9-28, the abstract and the summary of earlier attacks
---

GOST 28147-89 is a [block cipher](/block-cipher/) on 64-bit blocks with a 256-bit key. It was the cipher standard of the USSR and then of Russia, the counterpart of [DES](/data-encryption-standard/). It is a 32-round [Feistel network](/feistel-network/) with a very simple round: add a key word, put the result through eight 4-bit [S-boxes](/s-box/), and rotate it by 11 places. The key schedule only reads the eight key words in a fixed order. The 1989 standard did not fix the S-boxes. GOST R 34.12-2015 fixed one set and named the cipher Magma.

**Notation.** A block is two 32-bit words $(a_1, a_0)$, with $a_1$ the high word. The key is eight 32-bit words $k_1, \ldots, k_8$. In the Magma form of RFC 8891, the block and the key are read as big-endian integers, so $k_1$ is the first four bytes of the key. $+$ is addition modulo $2^{32}$, $\oplus$ is XOR, and $x \lll 11$ is rotation to the left by 11 places. $\Pi_0, \ldots, \Pi_7$ are the eight S-boxes, each a permutation of $\{0, \ldots, 15\}$, and $\Pi_0$ acts on the low 4 bits. $n$ is the number of blocks.

## In plain words

GOST cuts the block into a left half and a right half. In each of 32 rounds, it adds a part of the key to the right half, cuts the sum into eight small pieces, replaces each piece with a table, and turns the result by 11 places. It mixes this into the left half, and the halves change places.

The key has eight parts. The first 24 rounds use them in order three times, and the last 8 rounds use them in reverse order. The design has no complex steps, so it is easy to build in hardware. Its safety comes from the large key and the large number of rounds.

## The problem

GOST computes a permutation $E_K$ of $\{0,1\}^{64}$ for each key $K$ of 256 bits, and its inverse $D_K$. The standard of 1989 also defines modes of operation: electronic codebook, a counter mode, cipher feedback and a MAC. The goal is that $E_K$ behaves like a [pseudorandom permutation](/pseudorandom-permutation/). The 256-bit key puts [exhaustive search](/exhaustive-key-search/) far out of reach, but the 64-bit block limits the amount of data that one key can safely protect, because of the [birthday bound](/birthday-attack/).

## The algorithm

```pseudo id=main
MAGMA-ENCRYPT(K₁ .. K₃₂, a₁, a₀)
L1  for i ← 1 to 31 do
L2      (a₁, a₀) ← (a₀, g(Kᵢ, a₀) ⊕ a₁)             ▷ G[Kᵢ]
L3  return (g(K₃₂, a₀) ⊕ a₁) ‖ a₀                  ▷ G*[K₃₂], no swap

g(k, a)
L4  s ← (a + k) mod 2^32
L5  u ← Π₇(s₇) ‖ … ‖ Π₀(s₀)                         ▷ t: the 4-bit pieces of s
L6  return u ⋘ 11

ROUND-KEYS(K)
L7  (k₁, …, k₈) ← the eight 32-bit words of K
L8  return (k₁, …, k₈, k₁, …, k₈, k₁, …, k₈, k₈, …, k₁)
```

The names $t$, $g$, $G$ and $G^*$ are those of RFC 8891. Line L2 is the round $G[K_i]$, a Feistel round with a swap. Line L3 is the last round $G^*[K_{32}]$, which does not swap, so that encryption and decryption have the same form. Decryption is the same procedure with the round keys in reverse order, $K_{32}, \ldots, K_1$.

The original GOST 28147-89 is the same network, but it reads the key words and the block as little-endian numbers, and it leaves the S-boxes to the user. RFC 4357 lists the S-box sets used with the CryptoPro software. Magma fixes the set id-tc26-gost-28147-param-Z. The code of this page takes any S-box set and uses the Magma conventions by default.

The Python code for this page is for study only. It is not constant time, because the S-boxes are tables indexed by secret values. Do not use it to protect real data. Use AES from a validated library such as OpenSSL instead.

## Example

Take the test example of RFC 8891, Appendix A. The key is FFEEDDCCBBAA99887766554433221100F0F1F2F3F4F5F6F7F8F9FAFBFCFDFEFF, so $k_1$ = FFEEDDCC and $k_8$ = FCFDFEFF. The plaintext is FEDCBA9876543210, so $a_1$ = FEDCBA98 and $a_0$ = 76543210.

In round 1, line L4 gives $s$ = 76543210 + FFEEDDCC = 76430FDC. Line L5 gives $u$ = 319AC0D0, and line L6 gives $g(K_1, a_0)$ = D606818C. Line L2 then gives the new $a_0$ = D606818C ⊕ FEDCBA98 = 28DA3B14.

| after round | key | $a_1$ | $a_0$ |
|---|---|---|---|
| 0 (plaintext) | | FEDCBA98 | 76543210 |
| 1 | $k_1$ | 76543210 | 28DA3B14 |
| 2 | $k_2$ | 28DA3B14 | B14337A5 |
| 8 | $k_8$ | 37D97F25 | 46324615 |
| 16 | $k_8$ | 2098CD86 | 4F15B0BB |
| 24 | $k_8$ | 8025C0A5 | B0D66514 |
| 31 | $k_2$ | 239A4577 | C2D8CA3D |
| 32 (line L3) | $k_1$ | 4EE901E5 | C2D8CA3D |

The ciphertext is 4EE901E5C2D8CA3D, as in Appendix A.4 of RFC 8891. The appendix lists the state after each round, and the test file checks $t$, $g$, the round keys and the ciphertext, and decrypts it back.

## Correctness

The cipher is a Feistel network, so it is a permutation for any S-boxes and any round function $g$. The proof does not need $g$ to be invertible. Each round $G[k]$ is undone by the round $G[k]$ with the halves swapped, and the special last round $G^*$ makes decryption equal to encryption with the keys reversed. The [proof](proofs/correctness.md) gives the details.

## Complexity

A block costs 32 rounds, and each round costs one addition, eight 4-bit lookups, one rotation and one XOR. So $n$ blocks cost $\Theta(n)$ time. The cipher keeps 8 key words and the S-boxes, which is $\Theta(1)$ extra space. Software usually merges pairs of 4-bit S-boxes into four 8-bit tables to save lookups.

The best published attacks on the full cipher use the structure of the key schedule. Isobe (FSE 2011, pp. 290-305) gave the first single-key attack on the full 32 rounds for all keys. Dinur, Dunkelman and Shamir (FSE 2012, pp. 9-28) state its cost as $2^{32}$ data, $2^{64}$ memory and $2^{224}$ time. They improved it to $2^{224}$ time with $2^{32}$ data and $2^{36}$ memory, and to $2^{192}$ time with $2^{64}$ data and $2^{36}$ memory. These attacks are far from practical, but they are faster than a search of $2^{256}$ keys.

## Properties

- **Reflection.** The last 8 rounds use the keys of rounds 17 to 24 in reverse order. So, if the two halves are equal after round 24, the last 8 rounds undo rounds 17 to 24, and the ciphertext equals the state after round 16. The attacks above use this property.
- **Additive key.** The key enters by addition modulo $2^{32}$, not by XOR. The carries make the round less linear than an XOR would.
- **Small S-boxes.** Each S-box maps 4 bits to 4 bits. The rotation by 11 places spreads the outputs of one S-box to the inputs of others in the next round.
- **Secret S-boxes.** In the original standard, the S-boxes could be a secret parameter of a network. Their quality depends on the set, and weak sets give weak ciphers.
- **Avalanche.** With the key of the example, a one-bit change of the plaintext changes on average 31.87 of the 64 ciphertext bits over 2000 random trials. The ideal value is 32.

## Variants and improvements

- **Magma.** GOST R 34.12-2015 and RFC 8891 fix the S-boxes and the big-endian byte order. The rounds are the same.
- **CryptoPro key meshing.** RFC 4357 changes the key after each 1024 bytes of data in some modes, to limit the data under one key.
- **[Kuznyechik](/kuznyechik/).** The same 2015 standard adds a new cipher with a 128-bit block, a [substitution-permutation network](/substitution-permutation-network/).

## When to use it

Use GOST or Magma only where Russian standards require it, and then use a validated library. Elsewhere, use [AES](/advanced-encryption-standard/). With a 64-bit block, limit the data under one key to far less than $2^{32}$ blocks, or change the key often.

## Pitfalls

- **The S-box set.** Two implementations with different S-boxes give different ciphers. State the set, for example id-tc26-gost-28147-param-Z for Magma.
- **Byte order.** The original standard and Magma read the key and the block in opposite byte orders. The same key bytes give different round keys.
- **The last round.** The last round does not swap the halves. An implementation that swaps and then swaps back must do it exactly once.
- **The key order.** Rounds 25 to 32 use $k_8, \ldots, k_1$, not $k_1, \ldots, k_8$.
- **Timing.** S-box tables indexed by secret values can leak through the cache.

## Implementations

## History

The cipher was designed in the Soviet Union, and Dinur, Dunkelman and Shamir describe it as a design of the 1970s. The Government Committee of the USSR for Standards published it as GOST 28147-89 in 1989. An English description appeared in RFC 5830 in 2010. Russia replaced the standard with GOST R 34.12-2015, which defines two ciphers: Magma, the old cipher with fixed S-boxes, and the new Kuznyechik. RFC 8891 of 2020 is the English text of the Magma part. Isobe published the first attack on the full cipher for all keys in 2011, and Dinur, Dunkelman and Shamir improved it in 2012.

## References
