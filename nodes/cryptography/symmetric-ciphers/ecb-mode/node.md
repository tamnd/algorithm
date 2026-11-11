---
tag: 3HG8V8
kind: technique
slug: ecb-mode
name: Electronic codebook mode
aliases:
- ECB
area: cryptography/symmetric-ciphers
level: intro
summary: Encrypt each block of the message on its own with the block cipher. It is deterministic, so equal blocks give equal ciphertext blocks, and it is not IND-CPA secure.
prereqs: [block-cipher, chosen-plaintext-attack]
see_also: [cbc-mode, ctr-mode, xts-mode, ocb-mode, block-padding, advanced-encryption-standard, pseudorandom-permutation, semantic-security]
sources:
  - url: "https://doi.org/10.6028/NIST.SP.800-38A"
    title: Morris Dworkin, NIST Special Publication 800-38A, Recommendation for Block Cipher Modes of Operation, Methods and Techniques, 2001
    locator: Section 6.1 (the ECB mode) and Appendix F.1 (ECB example vectors)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 3, the section on modes of operation (ECB is deterministic and so not CPA-secure)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 7.2.2 (modes of operation, ECB and its properties)
  - paper: "Mihir Bellare, Anand Desai, Eron Jokipii and Phillip Rogaway, A concrete security treatment of symmetric encryption, Proceedings of the 38th IEEE Symposium on Foundations of Computer Science (FOCS), 1997"
    locator: the security definitions for symmetric encryption that rule out deterministic schemes
---

Electronic codebook (ECB) mode is the simplest mode of operation of a [block cipher](/block-cipher/): it cuts the message into blocks and encrypts each block on its own with the same key. NIST defines it in SP 800-38A, Section 6.1. Because it is deterministic, two equal plaintext blocks always give two equal ciphertext blocks, so ECB leaks the patterns of the data and is not secure under a [chosen-plaintext attack](/chosen-plaintext-attack/). Use it only as a building block inside other constructions, never to encrypt messages.

**Notation.** $E_K$ is a block cipher with key $K$ and block length $n$ bits ($n = 128$ for [AES](/advanced-encryption-standard/)), $D_K = E_K^{-1}$, $P_1, \ldots, P_m$ are the plaintext blocks and $C_1, \ldots, C_m$ the ciphertext blocks. $\mathcal{A}$ is an adversary and $q$ its number of queries.

## In plain words

A block cipher turns 16 bytes into 16 other bytes under a key, and it can turn them back. ECB uses it in the most direct way. It cuts the message into pieces of 16 bytes and encrypts each piece alone. Each piece always gives the same result under the same key, like a fixed code book. This is the problem. If two pieces of the message are equal, their encrypted pieces are equal too, and anyone can see that. A picture with large areas of one color keeps its outline after ECB encryption. An attacker can also move, delete or repeat encrypted pieces, and the receiver gets a changed message without any warning.

## When it applies

- **One block of random data, encrypted once.** If each plaintext block is unique and random, for example a fresh random key of one block, ECB on that one block is just the [pseudorandom permutation](/pseudorandom-permutation/) $E_K$ applied once. No pattern can leak, because no block repeats.
- **A building block inside a mode.** Many modes call $E_K$ on inputs that they make distinct on purpose: [CTR mode](/ctr-mode/) encrypts distinct counter blocks, [XTS](/xts-mode/) and [OCB](/ocb-mode/) mask each block with a distinct offset before the cipher call. These modes are "ECB on masked inputs". The mask is what makes them safe.
- **Never for a message of two or more blocks that can repeat.** Text, images, database records and network packets have repeated blocks. For them, use [CBC](/cbc-mode/) or CTR for confidentiality, and an [authenticated encryption](/authenticated-encryption/) mode such as [GCM](/gcm-mode/) when the data must also be protected against changes.

## The template

The message length must be a whole multiple of $n$ bits. A longer message is first padded, for example with [PKCS #7 padding](/pkcs7-padding/) (see [block padding](/block-padding/)).

```pseudo id=main
ECB-ENCRYPT(K, P[1 .. m])                  ▷ each P[i] is one n-bit block
L1  for i ← 1 to m do
L2      C[i] ← E_K(P[i])
L3  return C[1 .. m]

ECB-DECRYPT(K, C[1 .. m])
L4  for i ← 1 to m do
L5      P[i] ← D_K(C[i])
L6  return P[1 .. m]
```

The only hole of the template is the block cipher $E$. Decryption is correct because $D_K(E_K(x)) = x$ for each block $x$: lines L4 to L6 undo lines L1 to L3 block by block.

**Cost.** Encryption and decryption of $m$ blocks take $m$ calls of the block cipher and no other work. The calls are independent, so all of them can run in parallel, and any block can be decrypted alone (random access). There is no initialization vector and no state.

**About the code.** The Python code of this page, with its own AES, is for study only. It is not constant time, and it must not be used to protect real data. Use an authenticated mode from a FIPS 140 validated module, from libsodium, or from the cryptography library of your platform.

### ECB is not IND-CPA secure

**Claim.** For every block cipher $E$ with $n \ge 1$, there is an adversary $\mathcal{A}$ that makes one challenge query of two blocks, no other query, runs in time $O(n)$, and has advantage 1 in the IND-CPA game against ECB.

*Proof.* In the IND-CPA game a random bit $b$ is chosen, and the challenger encrypts $M_b$ for the two equal-length messages $M_0, M_1$ that $\mathcal{A}$ submits. The advantage is $\mathrm{Adv}^{\text{ind-cpa}}(\mathcal{A}) = \left|\Pr[\mathcal{A} \Rightarrow 1 \mid b = 1] - \Pr[\mathcal{A} \Rightarrow 1 \mid b = 0]\right|$. Let $\mathcal{A}$ submit $M_0 = 0^n \| 0^n$ and $M_1 = 0^n \| 1^n$, receive $C = C_1 \| C_2$, and output 0 if $C_1 = C_2$, else 1.

- If $b = 0$, then $C_1 = E_K(0^n) = C_2$, so $\mathcal{A}$ outputs 0 with probability 1.
- If $b = 1$, then $C_1 = E_K(0^n)$ and $C_2 = E_K(1^n)$. Since $E_K$ is a permutation and $0^n \ne 1^n$, $C_1 \ne C_2$, so $\mathcal{A}$ outputs 1 with probability 1.

So the advantage is $|1 - 0| = 1$. $\blacksquare$

The same argument works with one-block messages if $\mathcal{A}$ may also ask the encryption oracle: it asks for $E_K(M_0)$ and compares the answer with the challenge. So the flaw is not the length of the message. It is that encryption is a fixed function of the key and the plaintext. Every deterministic scheme fails IND-CPA in this way, which is why secure modes add a random [initialization vector](/initialization-vector/) or a [nonce](/nonce/).

### Other properties

- **Error propagation.** A changed bit in $C_i$ changes all of $P_i$ (about half of its bits on average, for a good cipher) and no other block.
- **No integrity.** An attacker can delete, repeat or reorder ciphertext blocks, and can paste blocks from another message under the same key. Each change decrypts to valid-looking blocks.

## Classic examples

### The SP 800-38A vector

SP 800-38A, Appendix F.1.1, uses the AES-128 key `2b7e151628aed2a6abf7158809cf4f3c`. The first plaintext block `6bc1bee22e409f96e93d7e117393172a` encrypts to `3ad77bb40d7a3660a89ecaf32466ef97`, and the second block `ae2d8a571e03ac9c9eb76fac45af8e51` encrypts to `f5d3d58503b9699de785895a96fdbaaf`. In ECB the input block of each cipher call is the plaintext block itself; the CBC example of the same appendix starts from the same key and plaintext but gives other ciphertext blocks, because the input blocks differ.

### The pattern leak on a small bitmap

Take a picture of 9 by 7 pixels and let each pixel be one AES block: a white pixel `.` is the block of 16 zero bytes, a black pixel `#` is the block of 16 bytes `ff`. Encrypt the picture row by row in ECB under the key of SP 800-38A. The white block encrypts to `7df76b0c1ab899b33e42f047b91b546f` and the black block to `8af2860142f786f409307c1a3f7eaaac`. The table shows the first byte of each ciphertext block.

| row | plaintext | ciphertext (first byte of each block) |
|---|---|---|
| 1 | `.........` | `7d 7d 7d 7d 7d 7d 7d 7d 7d` |
| 2 | `.##...##.` | `7d 8a 8a 7d 7d 7d 8a 8a 7d` |
| 3 | `..##.##..` | `7d 7d 8a 8a 7d 8a 8a 7d 7d` |
| 4 | `...###...` | `7d 7d 7d 8a 8a 8a 7d 7d 7d` |
| 5 | `..##.##..` | `7d 7d 8a 8a 7d 8a 8a 7d 7d` |
| 6 | `.##...##.` | `7d 8a 8a 7d 7d 7d 8a 8a 7d` |
| 7 | `.........` | `7d 7d 7d 7d 7d 7d 7d 7d 7d` |

The attacker does not know the key, but the X is plain to see: the ciphertext is the picture with two new colors. In a real image each pixel is a few bytes, so a block holds several pixels, but large areas of one color still repeat whole blocks; this is the well known "ECB penguin" picture. Under [CBC](/cbc-mode/) with a random IV or under [CTR](/ctr-mode/), all 63 ciphertext blocks of this picture differ, with overwhelming probability.

### ECB inside other modes

- [CTR mode](/ctr-mode/) is ECB applied to the counter blocks $T_1, T_2, \ldots$, which are distinct, followed by an XOR with the message.
- [XTS mode](/xts-mode/) is ECB on $P_j \oplus \Delta_j$, with a mask $\Delta_j$ that depends on the sector number and the block position, so equal blocks at different places give different ciphertext.
- [OCB mode](/ocb-mode/), the offset codebook mode, also masks each block with a distinct offset before and after the cipher call.

## Variations

- **Ciphertext stealing for ECB.** A final partial block can be handled by stealing bytes from the previous ciphertext block, as XTS does. This removes the need for padding but does not fix the leak.
- **Tweakable codebook.** Replace $E_K(P_i)$ by $\tilde{E}_K^{T_i}(P_i)$ with a tweak $T_i$ that differs for each position. This is the idea of XTS and of the XEX construction of Rogaway.
- **Deterministic encryption on purpose.** For unique inputs, a deterministic scheme can be fine and useful (for example to search encrypted keys). The secure version of this idea for long messages is the SIV construction (see [authenticated encryption](/authenticated-encryption/)), which leaks only whether two whole messages are equal.

## Pitfalls

- **Library defaults.** Some libraries pick ECB when the caller names only the cipher. In the SunJCE provider of Java, the transformation name `AES` alone means `AES/ECB/PKCS5Padding`. Always name the mode in full.
- **"The data is random, so ECB is fine."** This holds only when no block can repeat. Fixed headers, zero padding and structured fields repeat often.
- **Treating ECB as integrity protection.** Changing blocks gives no error. A swap of two ciphertext blocks swaps two plaintext blocks.
- **Forgetting the padding rule.** ECB needs whole blocks. Ad hoc padding with zeros is ambiguous; see [block padding](/block-padding/).

## Exercises

1. Show that ECB is not secure even against an eavesdropper who sees one ciphertext, if messages have at least two blocks (no oracle queries).
2. An attacker sees $C_1 \| C_2 \| C_3$ under ECB and knows $P_2$. Which plaintext does $C_2 \| C_1 \| C_3$ decrypt to?
3. A database stores AES-ECB encryptions of 16-byte salary fields. Explain what an insider who can add records with known salaries learns.
4. Let $E_K$ be a [pseudorandom permutation](/pseudorandom-permutation/). Prove that ECB restricted to one-block messages, each encrypted at most once, is indistinguishable from random one-block strings, with advantage at most the PRP advantage plus the birthday term $q(q-1)/2^{n+1}$.

## References
