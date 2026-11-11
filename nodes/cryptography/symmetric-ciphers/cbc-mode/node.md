---
tag: AAD84Q
kind: technique
slug: cbc-mode
name: Cipher block chaining mode
aliases:
- CBC
area: cryptography/symmetric-ciphers
level: core
summary: XOR each plaintext block with the previous ciphertext block, then encrypt it. IND-CPA secure with a random, unpredictable IV, but malleable, so padding oracles break it.
prereqs: [block-cipher, ecb-mode, initialization-vector]
see_also: [ecb-mode, ctr-mode, cfb-mode, ofb-mode, pkcs7-padding, padding-oracle-attack, cbc-mac, authenticated-encryption]
sources:
  - url: "https://doi.org/10.6028/NIST.SP.800-38A"
    title: Morris Dworkin, NIST Special Publication 800-38A, Recommendation for Block Cipher Modes of Operation, Methods and Techniques, 2001
    locator: Section 6.2 (CBC), Appendix C (generation of IVs) and Appendix F.2 (CBC example vectors)
  - url: "https://cseweb.ucsd.edu/~mihir/papers/sym-enc.html"
    title: Mihir Bellare, Anand Desai, Eron Jokipii and Phillip Rogaway, A concrete security treatment of symmetric encryption, FOCS 1997 (full version on the authors' pages)
    locator: Section 6 of the full version (Proposition 15, Lemma 16 and Theorem 17 on CBC)
  - paper: "Serge Vaudenay, Security flaws induced by CBC padding, applications to SSL, IPSEC, WTLS, EUROCRYPT 2002, LNCS 2332, pages 534 to 545"
    locator: the padding oracle attack on CBC with PKCS #5 style padding
  - paper: "Gregory V. Bard, The vulnerability of SSL to chosen plaintext attack, IACR Cryptology ePrint Archive, report 2004/111"
    locator: the chosen-plaintext attack on CBC with a predictable IV (the IV chained from the last record)
  - paper: "Thai Duong and Juliano Rizzo, Here come the XOR ninjas (the BEAST attack), presented at Ekoparty, 2011"
    locator: the practical attack on CBC in SSL 3.0 and TLS 1.0 with a predictable IV
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 3, the section on modes of operation (CBC with a random IV is CPA-secure; chained CBC is not)
---

Cipher block chaining (CBC) mode encrypts a message with a [block cipher](/block-cipher/) by XOR-ing each plaintext block with the previous ciphertext block before the cipher call. The first block is XOR-ed with an [initialization vector](/initialization-vector/) (IV), which must be random and unpredictable. NIST defines CBC in SP 800-38A, Section 6.2. With such an IV, CBC is secure under a [chosen-plaintext attack](/chosen-plaintext-attack/) up to about $\sigma^2 / 2^n$, where $\sigma$ is the number of blocks encrypted. It gives no integrity, and its malleability makes it fall to the padding oracle attack when the receiver reveals whether the padding of a forged ciphertext is valid.

**Notation.** $E_K$ is a block cipher with key $K$ and block length $n$ bits ($n = 128$ for [AES](/advanced-encryption-standard/)), $D_K = E_K^{-1}$, $P_1, \ldots, P_m$ are the plaintext blocks, $C_0 = IV$ and $C_1, \ldots, C_m$ are the ciphertext blocks. $\mathcal{A}$ is an adversary, $q$ its number of queries and $t$ its running time.

## In plain words

[ECB](/ecb-mode/) encrypts equal blocks to equal results. CBC fixes this by mixing each block with the encrypted block just before it, and the first block with a fresh random value called the IV. So the same message encrypted twice looks different, and equal blocks inside one message look different too. The receiver gets the IV with the ciphertext, and undoes the steps: decrypt a block, then remove the mix with the block before it.

CBC hides the data, but it does not stop changes. If an attacker flips a bit in one encrypted block, the same bit flips in the next decrypted block. If the receiver tells the attacker whether the decrypted message ends in a valid way, the attacker can use these flips to learn the whole message, one byte at a time.

## When it applies

- **Confidentiality of stored or sent data, with a separate MAC.** CBC with a random IV and a [message authentication code](/message-authentication-code/) computed over the IV and the ciphertext (encrypt-then-MAC, see [authenticated encryption](/authenticated-encryption/)) is a sound design. TLS up to version 1.2 and many file formats used CBC with HMAC.
- **When the IV can be random and secret until use.** The sender must pick a new unpredictable IV for each message. If the IV comes from a counter or from the last ciphertext block, use a different mode or encrypt the counter first (SP 800-38A, Appendix C).
- **Not alone.** Without a MAC, CBC is malleable, and a padding error message breaks it. For new designs prefer an AEAD mode such as [GCM](/gcm-mode/) or [ChaCha20-Poly1305](/chacha20-poly1305/).

## The template

The plaintext is a whole number of blocks, usually after [PKCS #7 padding](/pkcs7-padding/).

```pseudo id=main
CBC-ENCRYPT(K, IV, P[1 .. m])
L1  C[0] ← IV                              ▷ IV: random, unpredictable, one block
L2  for i ← 1 to m do
L3      C[i] ← E_K(P[i] ⊕ C[i − 1])
L4  return C[0 .. m]

CBC-DECRYPT(K, C[0 .. m])
L5  IV ← C[0]
L6  for i ← 1 to m do
L7      P[i] ← D_K(C[i]) ⊕ C[i − 1]
L8  return P[1 .. m]
```

The holes are the block cipher $E$ and the source of the IV. Decryption is correct: by line L3, $D_K(C_i) = P_i \oplus C_{i-1}$, so line L7 returns $P_i$.

**Cost.** Both directions use $m$ block cipher calls for $m$ blocks. Encryption is sequential, because line L3 needs $C_{i-1}$. Decryption is parallel and has random access, because line L7 needs only ciphertext blocks. The ciphertext is one block longer than the padded plaintext.

**About the code.** The Python code of this page, with its own AES, is for study only. It is not constant time, and it must not be used to protect real data. Use an AEAD from a FIPS 140 validated module, from libsodium, or from the standard cryptography library of your platform.

### Security with a random IV

Let CBC$\$$ be CBC in which the encryption algorithm picks $IV$ uniformly at random and outputs it as $C_0$. Bellare, Desai, Jokipii and Rogaway (FOCS 1997) measure security in the left-or-right model (LOR-CPA). An LOR-CPA bound is also a bound for [IND-CPA](/ind-cpa-security/) with one challenge (their find-then-guess notion, Theorem 3 of the paper), and the converse holds with a loss of a factor $q_e$, the number of queries (Theorem 4). In the full version, Section 6, they write $l$ for the block length, $\mu_e$ for the total number of plaintext bits in the queries, and $q = \mu_e / l$ for the total number of blocks.

- **Lemma 16 (random function).** If $F$ is a random function from $l$ bits to $l$ bits, then $\mathrm{Adv}^{\text{lor-cpa}}_{\text{CBC}[F]}(\cdot, t, q_e, \mu_e) \le \left(\frac{\mu_e^2}{l^2} - \frac{\mu_e}{l}\right) \cdot \frac{1}{2^l}$.
- **Theorem 17 (pseudorandom permutation).** If $F$ is a PRP family with length $l$, then for any $t$, $q_e$ and $\mu_e = q l$,

$$\mathrm{Adv}^{\text{lor-cpa}}_{\text{CBC}[F]}(\cdot, t, q_e, \mu_e) \le 2 \cdot \mathrm{Adv}^{\text{prp}}_F(t, q) + q^2 \, 2^{-l-1} + \left(\frac{\mu_e^2}{l^2} - \frac{\mu_e}{l}\right) \cdot 2^{-l}.$$

- **Proposition 15 (lower bound).** For a random permutation, $\mu_e \le l \cdot 2^{l/2}$ and $q_e = \mu_e / l$ one-block queries, an adversary reaches advantage at least $0.316 \cdot \left(\frac{\mu_e^2}{l^2} - \frac{\mu_e}{l}\right) \cdot \frac{1}{2^l}$.

With $\sigma = \mu_e / l$ blocks, the bound is about $1.5\,\sigma^2 / 2^n$ plus twice the PRP advantage, and the attack shows that $\sigma^2 / 2^n$ is the right order. The proof is in the standard model and loses only the factor 2 on the PRP term. The idea of the upper bound: as long as all inputs $P_i \oplus C_{i-1}$ to the random function are distinct, each output is a fresh uniform block, independent of the message, so the left and right worlds look the same. Each input is a fresh uniform value XOR a chosen block, so two inputs collide with probability $2^{-l}$, and a union bound over the $\binom{\sigma}{2}$ pairs gives the $\sigma^2$ term. The PRP to PRF step is the [switching lemma](/prp-prf-switching-lemma/). The lower bound attack waits for two equal cipher inputs: then $C_i = C_j$ reveals $P_i \oplus C_{i-1} = P_j \oplus C_{j-1}$, an equation on the plaintexts.

For AES, $n = 128$: after $\sigma = 2^{48}$ blocks (4 PiB) the term $\sigma^2 / 2^{128}$ is $2^{-32}$, and after $2^{64}$ blocks it is 1. For a 64-bit block cipher such as Triple DES, $2^{32}$ blocks (32 GiB) already give constant advantage; this is the Sweet32 attack of Bhargavan and Leurent (2016).

### A predictable IV breaks IND-CPA

**Claim.** If the adversary can predict the IV of the next encryption, CBC is not IND-CPA secure: there is an adversary with one oracle query and advantage 1.

*Proof.* Suppose $\mathcal{A}$ knows that the challenge will use $IV^*$ and that its next oracle query will use $IV'$ (for example, $IV'$ is the last ciphertext block that $\mathcal{A}$ has just seen, as in SSL 3.0 and TLS 1.0, which chained records). It submits the challenge pair $M_0 = 0^n$, $M_1 = 1^n$ and gets $C^* = E_K(IV^* \oplus M_b)$. Then it asks the oracle to encrypt $X = IV' \oplus IV^* \oplus M_0$ and gets $C' = E_K(IV' \oplus X) = E_K(IV^* \oplus M_0)$. It outputs 0 if $C' = C^*$, else 1. If $b = 0$ the two values are equal; if $b = 1$ they differ, because $E_K$ is a permutation and $M_0 \ne M_1$. So the advantage is 1. $\blacksquare$

The same test checks any guess $G$ for any earlier block: submit $IV' \oplus C_{i-1} \oplus G$ and compare with $C_i$. Bard (2004) showed this for SSL, and Duong and Rizzo turned it into the BEAST attack (2011) on HTTPS cookies: they arrange the plaintext so that only one unknown byte falls in the block, and guess it in at most 256 tries. TLS 1.1 (RFC 4346, 2006) replaced the chained IV with an explicit random IV in each record. The test of this page runs the attack on a chained CBC encryptor and recovers a secret vote.

### Malleability and the padding oracle

By line L7, $P_i = D_K(C_i) \oplus C_{i-1}$. If an attacker XORs a value $\Delta$ into $C_{i-1}$, then $P_i$ changes by exactly $\Delta$, and $P_{i-1}$ turns into random-looking data. So CBC gives no integrity: a bit flip in one ciphertext block flips the same bit of the next plaintext block.

Vaudenay (EUROCRYPT 2002) combined this with the padding check. Suppose the receiver decrypts, checks the PKCS #7 padding, and tells the sender (by an error code, an alert or a timing difference) whether the padding was valid. That one bit is a padding oracle. To decrypt a block $C_i$, the attacker sends the two blocks $R \| C_i$, with a chosen block $R$. The receiver computes the last plaintext block $D_K(C_i) \oplus R$.

1. Try the 256 values of the last byte of $R$. For the value $g$ that the oracle accepts, the last decrypted byte is most likely `01`, so the last byte of $D_K(C_i)$ is $g \oplus 01$. (If it was a longer valid padding such as `02 02` by chance, changing byte 15 of $R$ shows it.)
2. Set the last byte of $R$ so that the last decrypted byte becomes `02`, and try the 256 values of byte 15 until the oracle accepts. This gives byte 15 of $D_K(C_i)$.
3. Go on to the left with paddings `03 03 03`, and so on. After 16 bytes, $D_K(C_i)$ is known, and $P_i = D_K(C_i) \oplus C_{i-1}$.

The cost is at most 256 oracle queries for each byte, so at most $256 \cdot 16 = 4096$ for each block, and no key is needed. The test of this page runs the attack against a local oracle that decrypts with the page's own CBC code. For the 24-byte message `PIN=4921; meet at gate 7` (two blocks after padding) it recovers the full plaintext with 3913 oracle queries. In the last block, the guess $g = $ `1f` makes the oracle accept at byte 16, so the last byte of $D_K(C_2)$ is `1e`; XOR with the last byte `16` of $C_1$ gives `08`, the padding byte of a message that ends 8 bytes short of a block. The general attack and its history (Bleichenbacher 1998 for RSA) are on the page on the [padding oracle attack](/padding-oracle-attack/).

The fix is not a better padding check. The fix is to authenticate the ciphertext with a MAC and to check the MAC before any decryption or padding check (encrypt-then-MAC), or to use an AEAD.

## Classic examples

### The SP 800-38A vector

SP 800-38A, Appendix F.2.1, uses the AES-128 key `2b7e151628aed2a6abf7158809cf4f3c` and the IV `000102030405060708090a0b0c0d0e0f`.

| block | plaintext $P_i$ | input $P_i \oplus C_{i-1}$ | ciphertext $C_i$ |
|---|---|---|---|
| 1 | `6bc1bee22e409f96e93d7e117393172a` | `6bc0bce12a459991e134741a7f9e1925` | `7649abac8119b246cee98e9b12e9197d` |
| 2 | `ae2d8a571e03ac9c9eb76fac45af8e51` | `d86421fb9f1a1eda505ee1375746972c` | `5086cb9b507219ee95db113a917678b2` |
| 3 | `30c81c46a35ce411e5fbc1191a0a52ef` | `604ed7ddf32efdff7020d0238b7c2a5d` | `73bed6b8e3c1743b7116e69e22229516` |
| 4 | `f69f2445df4f9b17ad2b417be66c3710` | `8521f2fd3c8eef2cdc3da7e5c44ea206` | `3ff1caa1681fac09120eca307586e1a7` |

Each input block is the XOR of the plaintext block with the ciphertext block in the row above (the IV for row 1). The plaintext and key are the same as in the [ECB](/ecb-mode/) example, but no ciphertext block is the same.

### Error propagation

A flipped bit in $C_i$ garbles all of $P_i$ and flips the same bit in $P_{i+1}$. The blocks after that are correct, so CBC recovers from a bit error after two blocks. A lost or inserted whole block also damages only two blocks. A lost byte, however, shifts all block borders, and every later block is wrong.

### CBC in other constructions

- [CBC-MAC](/cbc-mac/) runs CBC with a zero IV and keeps only the last block as a tag.
- [CCM mode](/ccm-mode/) uses CBC-MAC for the tag and CTR for the encryption.
- TLS 1.0 to 1.2 used CBC with MAC-then-encrypt, which led to padding oracle and timing attacks such as Lucky Thirteen (AlFardan and Paterson 2013); TLS 1.3 (RFC 8446) removed CBC.

## Variations

- **Ciphertext stealing (CBC-CS1, CS2, CS3).** The Addendum to SP 800-38A (2010) defines three ways to encrypt a final partial block without padding, so the ciphertext has the same length as the plaintext. See [block padding](/block-padding/).
- **Encrypted IV.** SP 800-38A, Appendix C, allows the IV to be $E_K(N)$ for a unique nonce $N$; the forward cipher makes the IV unpredictable.
- **Explicit IV per record.** TLS 1.1 and 1.2 send a fresh random IV with each record.
- **PCBC (propagating CBC).** Each block is mixed with both the previous plaintext and ciphertext blocks. It was used in Kerberos version 4. It gives no real integrity: swapping two adjacent ciphertext blocks leaves the later blocks correct.

## Pitfalls

- **Fixed, zero or counter IV.** A fixed IV makes CBC deterministic for the first block, so equal message prefixes show. A counter IV is predictable and allows the attack above. Use a random IV from a cryptographic generator, or encrypt a nonce.
- **Telling the sender that the padding is wrong.** Any difference between "bad padding" and "bad MAC", in the message, in the error code or in the time, is a padding oracle.
- **MAC-then-encrypt.** If the MAC is checked after the padding, the padding check is exposed. Check a MAC over the IV and the ciphertext first.
- **Not covering the IV with the MAC.** A change of the IV changes $P_1$ at will. The MAC must cover $C_0$.
- **Reusing the key for CBC-MAC.** The same key for CBC encryption and CBC-MAC breaks the MAC.

## Exercises

1. Prove that CBC with a fixed IV $0^n$ is not IND-CPA secure, with one oracle query.
2. An attacker can change $C_0$. Show how to change the first plaintext block into any chosen block without the key.
3. Count the padding oracle queries of the attack in the worst case for a message of $m$ blocks, and the expected number if each guess order is random.
4. Show that CBC decryption of $m$ blocks has span one block call when run in parallel, and explain why encryption cannot do the same.
5. With $n = 64$, how many blocks give the term $\sigma^2 / 2^n$ a value of $1/2$?

## References
