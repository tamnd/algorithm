---
tag: 9A46ZH
kind: technique
slug: xts-mode
name: XTS mode
aliases:
- XEX-based tweaked codebook with ciphertext stealing
area: cryptography/symmetric-ciphers
level: advanced
summary: Disk sector encryption from IEEE 1619. Each block is masked by a tweak from the sector number and its position; ciphertext stealing keeps length. No integrity.
prereqs: [block-cipher, ecb-mode, gf2-polynomial-arithmetic]
see_also: [ecb-mode, ctr-mode, ocb-mode, block-padding, authenticated-encryption, pseudorandom-permutation]
sources:
  - paper: "IEEE Std 1619-2007, IEEE Standard for Cryptographic Protection of Data on Block-Oriented Storage Devices, IEEE, 2008"
    locator: Section 5 (XTS-AES encryption and decryption, multiplication by alpha, ciphertext stealing) and Annex B (test vectors, Vectors 1, 2, 3 and 15)
  - url: "https://doi.org/10.6028/NIST.SP.800-38E"
    title: Morris Dworkin, NIST Special Publication 800-38E, Recommendation for Block Cipher Modes of Operation, The XTS-AES Mode for Confidentiality on Storage Devices, 2010
    locator: the whole document (approval of XTS-AES as in IEEE 1619-2007, limit of 2^20 blocks per data unit)
  - paper: "Phillip Rogaway, Efficient instantiations of tweakable blockciphers and refinements to modes OCB and PMAC, ASIACRYPT 2004, LNCS 3329, pages 16 to 31"
    locator: the XEX construction and its proof as a strong tweakable pseudorandom permutation
  - paper: "Moses Liskov, Ronald L. Rivest and David Wagner, Tweakable block ciphers, CRYPTO 2002, LNCS 2442, pages 31 to 46"
    locator: the definition of a tweakable block cipher
---

XTS is the standard mode for encrypting disk sectors. IEEE Std 1619-2007 defines XTS-AES, and NIST approves it for storage in SP 800-38E. It is built on XEX, the tweakable block cipher of Rogaway (Asiacrypt 2004): each 16-byte block is XOR-ed with a mask, encrypted, and XOR-ed with the mask again, and the mask depends on the sector number and on the position of the block in the sector. Ciphertext stealing handles a sector whose length is not a multiple of 16 bytes, so the ciphertext has exactly the length of the plaintext. XTS gives no authentication, and because it works on narrow 16-byte blocks, an attacker can change or replay single blocks.

**Notation.** $E_{K_1}$ and $E_{K_2}$ are AES with two independent keys, $n = 128$. A data unit (a sector) has number $i$ and plaintext blocks $P_0, \ldots, P_m$, all of 16 bytes except perhaps the last. $\alpha$ is the element $x$ of $\mathrm{GF}(2^{128})$ defined by $x^{128} + x^7 + x^2 + x + 1$, and $\otimes$ is multiplication in that field.

## In plain words

A disk is a long row of sectors, and an encrypted sector must keep its size: there is no room for anything extra. So XTS cannot add a random starting value or a check value. Instead it uses the address of the data as the variation. It encrypts the sector number to get a secret starting mask. For each 16-byte block of the sector, it changes the mask in a fixed way, XORs the block with the mask, encrypts it, and XORs it with the mask again.

The result is that the same 16 bytes encrypt to different values in different places on the disk. But at the same place, the same data always gives the same encryption, and nothing detects a change. If the last piece of a sector is shorter than 16 bytes, XTS borrows bytes from the block before it, so no padding is needed.

## When it applies

- **Block storage.** Full disk encryption (BitLocker, FileVault 2, LUKS with dm-crypt, VeraCrypt) and self-encrypting drives use XTS-AES.
- **Length preserving encryption with random access.** Each sector is encrypted on its own, and each block in a sector can be decrypted on its own.
- **Not for messages or network traffic.** XTS is deterministic per position and has no tag. For messages use an AEAD such as [GCM](/gcm-mode/) or [OCB](/ocb-mode/).
- **Not when the attacker can see many versions of the disk and changes matter.** Snapshots show which 16-byte blocks changed, and old blocks can be put back. A wide-block mode or authenticated storage is needed then.

## The template

```pseudo id=main
XTS-ENC(K₁, K₂, i, P)                      ▷ P has at least 16 bytes; i is the sector number
L1  T ← E_K₂(i)                             ▷ i as 16 bytes, little-endian
L2  for j ← 0 to (number of blocks done normally) − 1 do
L3      C[j] ← E_K₁(P[j] ⊕ T) ⊕ T
L4      T ← T ⊗ α
L5  if the last block P[m] has r bytes with 0 < r < 16 then
L6      CC ← E_K₁(P[m−1] ⊕ T) ⊕ T          ▷ the last full block, with its own tweak
L7      PP ← P[m] ‖ CC[r ..]               ▷ steal 16 − r bytes of CC
L8      C[m−1] ← E_K₁(PP ⊕ T⊗α) ⊕ T⊗α ;  C[m] ← CC[.. r]
L9  return C
```

The holes are the cipher, the size of a data unit and the mapping from sector to number $i$. Without stealing, all blocks are done in the loop; with stealing, all but the last two. Decryption runs the same steps with $D_{K_1}$, but with stealing it must take the tweaks in the other order: it decrypts $C_{m-1}$ with $T \otimes \alpha$ first, to get $P_m$ and the stolen bytes, and then decrypts $C_m \| \text{stolen}$ with $T$.

**Cost.** One call of $E_{K_2}$ per sector and one call of $E_{K_1}$ per block, plus one shift and conditional XOR per block for $\otimes \alpha$. All blocks except the stolen pair are independent once the tweaks are known.

**About the code.** The Python code of this page, with its own AES, is for study only. It is not constant time, and it must not be used to protect real data. Use the XTS of a FIPS 140 validated module or of your operating system.

### The tweak and multiplication by alpha

IEEE 1619 encodes the data unit sequence number as a 128-bit little-endian integer, so sector `0x123456789a` becomes the bytes `9a785634120000000000000000000000`. This is encrypted under $K_2$ to give the first mask $T_0$. The mask of block $j$ is $T_j = T_0 \otimes \alpha^j$, computed one step at a time.

Multiplication by $\alpha$ uses the 16 bytes in little-endian order: byte 0 holds the coefficients of $x^0$ to $x^7$, with bit 0 of byte 0 as $x^0$, and the top bit of byte 15 is $x^{127}$. Multiplying by $x$ shifts the whole 128-bit integer left by one. If bit 127 falls out, the term $x^{128}$ is replaced by $x^7 + x^2 + x + 1$, so byte 0 is XOR-ed with `0x87`. For example, with $T_0 = $ `775d1be20e07015ed7585459144a09e1`, the last byte `e1` has its top bit set, so the shift gives `ee ba ...` in the low bytes and the reduction turns `ee` into `69`: $T_1 = $ `69ba36c41d0e02bcaeb1a8b2289412c2`. This byte order is the opposite of the bit order of GHASH in [GCM](/gcm-mode/), although the field polynomial is the same.

### Why the masks work

XEX makes each pair (sector, position) behave like its own random permutation. The core fact is that two different positions get masks that look unrelated.

**Claim.** Let $\pi_2$ be a random permutation and $L_i = \pi_2(i)$. For $(i, j) \ne (i', j')$ with $0 \le j, j' < 2^{20}$, and any fixed 128-bit $c$, $\Pr[\alpha^j L_i \oplus \alpha^{j'} L_{i'} = c] \le 1/(2^n - 1)$.

**Proof.** If $i = i'$, then $j \ne j'$ and the event is $(\alpha^j \oplus \alpha^{j'}) L_i = c$. Since $\alpha = x$ is a primitive element of the field, $\alpha^j \ne \alpha^{j'}$ for $j \ne j'$ below $2^{128} - 1$, so the factor is a nonzero field element and the event fixes $L_i$ to one value, which has probability $2^{-n}$. If $i \ne i'$, then fix $L_{i'}$; the event fixes $L_i$ to one value, and given $L_{i'}$, $L_i$ is uniform on the other $2^n - 1$ values, so the probability is at most $1/(2^n - 1)$. $\blacksquare$

So the inputs $P \oplus T_{i,j}$ that reach $E_{K_1}$ from different positions collide only with probability about $2^{-n}$ per pair. With $\sigma$ blocks this gives a birthday term of order $\sigma^2/2^n$, which is the shape of Rogaway's bound for XEX as a strong tweakable pseudorandom permutation (secure even when the attacker can also ask for decryptions). XTS differs from XEX in using two keys, $K_2$ for the tweak and $K_1$ for the data, and in adding stealing; the XEX proof covers the full blocks. SP 800-38E limits a data unit to $2^{20}$ blocks.

### Ciphertext stealing

When the sector length is $16m + r$ bytes with $0 < r < 16$, the last full plaintext block $P_{m-1}$ is encrypted with its own tweak $T_{m-1}$ to give $CC$. The first $r$ bytes of $CC$ become the short last ciphertext block $C_m$. The other $16 - r$ bytes of $CC$ are appended to the short plaintext block $P_m$ to fill a whole block $PP$, and $PP$ is encrypted with the next tweak $T_m$ to give $C_{m-1}$. No byte is added, and the decryptor can rebuild everything: it decrypts $C_{m-1}$ with $T_m$, reads $P_m$ and the stolen bytes from the result, and puts them behind $C_m$ to recover $CC$. The same idea for CBC is in the [block padding](/block-padding/) page.

### What XTS does not give

- **No authentication.** Any ciphertext decrypts to some plaintext, and no check fails.
- **Malleability at 16-byte resolution.** Changing any bit of a ciphertext block turns that one plaintext block into random bytes and leaves all others intact. An attacker who knows the layout can randomize one chosen field.
- **Replay of blocks.** An old ciphertext block put back at its old position decrypts to the old plaintext. The tests of this page restore an old `balance` field this way.
- **Leaks across time.** The encryption is deterministic for a given key, sector and position, so an attacker with two snapshots of the disk learns exactly which 16-byte blocks changed.

A wide-block mode, which mixes the whole sector so that any change randomizes all of it, reduces these leaks but still cannot detect changes. Only stored tags (with space for them) give integrity.

## Classic examples

The vectors below are from IEEE Std 1619-2007, Annex B, where they are numbered Vector 1 to Vector 18. The IEEE text was not open to the author of this page, so the values were copied from two public copies of that annex: the Linux kernel file `crypto/testmgr.h` (table `aes_xts_tv_template`, entries "XTS-AES 1" to "XTS-AES 3") and the libtomcrypt file `src/modes/xts/xts_test.c` (the 17-byte vector). The two copies agree where they overlap.

### IEEE 1619 Vector 2

Key1 `11111111111111111111111111111111`, Key2 `22222222222222222222222222222222`, data unit sequence number `3333333333`, plaintext 32 bytes of `44`. Ciphertext `c454185e6a16936e39334038acef838b` `fb186fff7480adc4289382ecd6d394f0`. The two plaintext blocks are equal, but the ciphertext blocks differ, because their masks $T_0$ and $T_1$ differ.

### IEEE 1619 Vector 15: stealing with one extra byte

Key1 `fffefdfcfbfaf9f8f7f6f5f4f3f2f1f0`, Key2 `bfbebdbcbbbab9b8b7b6b5b4b3b2b1b0`, sequence number `123456789a`, plaintext `000102...0f10` (17 bytes).

| step | value |
|---|---|
| $T_0 = E_{K_2}(i)$ | `775d1be20e07015ed7585459144a09e1` |
| $T_1 = T_0 \otimes \alpha$ | `69ba36c41d0e02bcaeb1a8b2289412c2` |
| $CC$ from $P_0$ and $T_0$ | `edbf9dace45d6f6a7306e64be5dd824b` |
| $C_1 = CC[0]$ | `ed` |
| $PP = P_1 \| CC[1..15]$ | `10bf9dace45d6f6a7306e64be5dd824b` |
| $C_0$ from $PP$ and $T_1$ | `6c1625db4671522d3d7599601de7ca09` |

The ciphertext is `6c1625db4671522d3d7599601de7ca09ed`, as in the standard. The tests also check Vectors 1 and 3.

## Variations

- **XEX.** One key: the mask is $\alpha^j \otimes E_K(N)$ and the same $K$ encrypts the data. XTS uses a second key for the tweak.
- **XTS-AES-256.** Key1 and Key2 are each 256 bits; the 512-bit key is their concatenation.
- **Wide-block modes.** EME (Halevi and Rogaway) and HCTR2 encrypt a whole sector as one permutation, so a change in one byte randomizes the whole sector.
- **Authenticated storage.** File systems with tags (for example per-sector MACs kept in a separate area) give integrity at the cost of space and I/O.

## Pitfalls

- **Key1 equal to Key2.** XTS needs two independent keys, and FIPS 140 implementation guidance asks the module to check that the two halves differ. The code of this page refuses them by default; IEEE Vector 1 uses equal all-zero keys, so its test sets a flag.
- **Wrong byte order for the tweak or for $\otimes \alpha$.** IEEE 1619 is little-endian in both. A wrong shift still gives the right first block of every sector, so a test with one block per sector does not find it.
- **Swapping the tweaks in stealing on decryption.** Decryption of the stolen pair takes $T_m$ before $T_{m-1}$.
- **Expecting integrity.** Disk encryption with XTS stops a thief who takes a powered-off disk. It does not stop an attacker who can write to the disk.
- **Data units longer than $2^{20}$ blocks.** SP 800-38E forbids it.

## Exercises

1. Show that XTS without stealing on one sector is a permutation for each fixed tweak, and write its inverse.
2. An attacker can see the disk before and after one write. Describe what it learns, and show why a random IV per write would need extra space.
3. An attacker can make the system write a chosen 16-byte block at a chosen position and then read the disk. Show that it can test whether a block at that same position held a guessed value before.
4. Draw the decryption of a 40-byte data unit, and mark which tweak each block uses.

## References
