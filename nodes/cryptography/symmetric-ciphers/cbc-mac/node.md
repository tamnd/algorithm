---
tag: 3RSETN
kind: algorithm
slug: cbc-mac
name: CBC-MAC
aliases:
- cipher block chaining message authentication code
area: cryptography/symmetric-ciphers
level: core
summary: Encrypt the message in CBC mode with a zero IV and keep the last block as the tag. A secure PRF for messages of one fixed length, but forgeable at once when lengths vary.
solves: [message-authentication]
model: word-ram
complexity:
  vars: {m: the number of message blocks, n: the block length}
  time: {worst: Θ(m), average: Θ(m), best: Θ(m)}
  space: {extra: Θ(n)}
properties: {deterministic: true}
history:
  year: 1985
  people: [National Bureau of Standards, Mihir Bellare, Joe Kilian, Phillip Rogaway]
  note: FIPS 113 (1985) standardized the DES CBC-MAC for US government use, following banking practice. Bellare, Kilian and Rogaway gave the first proof of security in 1994.
prereqs: [message-authentication-code, cbc-mode, pseudorandom-permutation]
see_also: [cmac, message-authentication-code, cbc-mode, ccm-mode, prp-prf-switching-lemma, birthday-attack, hmac]
sources:
  - url: "https://cseweb.ucsd.edu/~mihir/papers/cbc.pdf"
    title: Mihir Bellare, Joe Kilian and Phillip Rogaway, The security of the cipher block chaining message authentication code, Journal of Computer and System Sciences 61(3), 2000, pages 362 to 399 (first version at CRYPTO 1994)
    locator: Theorem 3.1 (information-theoretic bound 1.5 q^2 m^2 / 2^l), Theorem 3.2 (computational case), Theorem 4.1 (security as a MAC) and Proposition 4.2 (the birthday forgery)
  - paper: "Mihir Bellare, Krzysztof Pietrzak and Phillip Rogaway, Improved security analyses for CBC MACs, CRYPTO 2005, LNCS 3621, pages 527 to 545"
    locator: the bounds of order m q^2 / 2^n for the basic CBC-MAC on prefix-free messages and of order m^o(1) q^2 / 2^n for the encrypted CBC-MAC
  - paper: "Erez Petrank and Charles Rackoff, CBC MAC for real-time data sources, Journal of Cryptology 13(3), 2000, pages 315 to 338"
    locator: the security of CBC-MAC on a prefix-free message set, and of EMAC for messages of any length
  - url: "https://doi.org/10.6028/NIST.SP.800-38A"
    title: Morris Dworkin, NIST Special Publication 800-38A, Recommendation for Block Cipher Modes of Operation, Methods and Techniques, 2001
    locator: Appendix F.2.1 (CBC-AES128.Encrypt), used for the derived test vector
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 4, the section on CBC-MAC (basic CBC-MAC, the variable-length attack and the fixes)
---

CBC-MAC computes a tag by encrypting the message in [CBC mode](/cbc-mode/) with a zero IV and keeping only the last ciphertext block. For a block cipher $E_K$ with $n$-bit blocks and a message of $m$ blocks, $Y_0 = 0^n$, $Y_j = E_K(Y_{j-1} \oplus M_j)$, and the tag is $Y_m$. Bellare, Kilian and Rogaway (CRYPTO 1994, JCSS 2000) proved that, for messages of one fixed number of blocks $m$, it is a pseudorandom function and so a secure [MAC](/message-authentication-code/), with a loss of order $q^2 m^2 / 2^n$. When messages of different lengths share a key, it is not secure: two tags give a forgery with no work at all. [CMAC](/cmac/) is the standard repair.

**Notation.** $E_K$ is the block cipher, $n$ its block length in bits ($n = 128$ for AES), $M = M_1 \cdots M_m$ the message in blocks, $Y_j$ the chaining value after block $j$, $T$ the tag, and $q$ the number of tagged messages.

## In plain words

Encrypt the first block. XOR the result into the second block and encrypt again. Continue to the end. The last result is the tag. Every block changes everything after it, so a change anywhere changes the tag.

The weakness comes from the fact that the tag is also the chaining value. If you know the tag $t_1$ of a one-block message $m_1$, then you know the state after $m_1$. Append the block $m_2 \oplus t_1$: the cipher then sees $t_1 \oplus m_2 \oplus t_1 = m_2$ and gives the tag of $m_2$. So if all messages have the same number of blocks, CBC-MAC is safe; if not, use CMAC.

## The problem

[Message authentication](/message-authentication/): from a key shared by sender and receiver, compute a short tag such that no one without the key can compute a valid tag for a new message, even after a chosen message attack. Plain CBC-MAC solves it only on a message space where all messages have the same number of blocks, or more generally where no message is a prefix of another.

## The algorithm

```pseudo id=main
CBC-MAC(K, M[1 .. m])                  ▷ |M| is m·n bits, m ≥ 1
L1  Y ← 0^n
L2  for j ← 1 to m do
L3      Y ← E_K(Y ⊕ M[j])
L4  return Y                            ▷ the tag; may be cut to its first t bits

VERIFY(K, M, T)
L5  return CBC-MAC(K, M) = T, compared in constant time
```

There is no IV in the tag: the zero start value is part of the algorithm. Lines L1 to L3 are exactly CBC encryption with $IV = 0^n$, with all ciphertext blocks thrown away except the last. Messages whose length is not a multiple of $n$ need a padding rule, and the padding must be injective on the message space (ISO/IEC 9797-1 lists several).

**About the code.** The Python code is for study only and is not constant time: the AES in `aes.py` reads tables at secret indices. The tag comparison reads every byte. In practice use CMAC from a FIPS 140 validated module, or `crypto_auth` (HMAC-SHA-512-256) in libsodium.

## Example

Key `000102030405060708090a0b0c0d0e0f`, AES-128, and two one-block messages that the attacker asks the sender to tag.

| message | hex | tag |
|---|---|---|
| $m_1$ = `pay 10 EUR to A.` | `7061792031302045555220746f20412e` | $t_1$ = `ca27f51bf8b4d8e3774d6f5a17cbaa79` |
| $m_2$ = `pay 99 EUR to E.` | `7061792039392045555220746f20452e` | $t_2$ = `fd2ac1d149332f3b2b432e63d3e5a611` |

**The forgery.** The attacker forms the second block $m_2 \oplus t_1$ = `ba468c3bc18df8a6221f4f2e78ebef57` and sends the two-block message $m_1 \,\|\, (m_2 \oplus t_1)$ with the tag $t_2$. The receiver computes $Y_1 = E_K(m_1) = t_1$, then $Y_2 = E_K(t_1 \oplus m_2 \oplus t_1) = E_K(m_2) = t_2$, and accepts. The message was never tagged. The tests check this and the same splice for messages of many blocks.

**A derived standard vector.** There is no official test vector for plain AES CBC-MAC. SP 800-38A, Appendix F.2.1, gives CBC encryption with key `2b7e151628aed2a6abf7158809cf4f3c` and IV `000102030405060708090a0b0c0d0e0f`. With a zero IV, CBC-MAC of the four blocks "Input Block #1" (which is $P_1 \oplus IV$) = `6bc0bce12a459991e134741a7f9e1925`, then $P_2$, $P_3$, $P_4$ of that vector equals its last ciphertext block `3ff1caa1681fac09120eca307586e1a7`. The tests check all four prefixes.

## Correctness

**Claim.** (1) VERIFY accepts every tag that CBC-MAC computes. (2) The tag equals the last block of CBC encryption with a zero IV, which is why the derived vector above is valid. (3) The splice identity: for any messages $M$ and $M' = M'_1 \cdots M'_k$ with tags $T$ and $T'$, the message $M \,\|\, (M'_1 \oplus T) \,\|\, M'_2 \cdots M'_k$ has tag $T'$. The key step for (3) is that the chaining value after $M$ is $T$, so the next cipher input is $T \oplus M'_1 \oplus T = M'_1$, and from there the chain is the chain of $M'$. The full proof is below.

**Security.** The claim above is about correctness and about the attack. For security, Bellare, Kilian and Rogaway prove the following for messages of exactly $m$ blocks.

- Theorem 3.1: with a truly random function in place of $E_K$, any adversary with $q$ queries tells CBC-MAC from a random function of $mn$ bits to $n$ bits with advantage at most $1.5 \, q^2 m^2 / 2^n$.
- Theorem 4.1: if $qm \le 2^{(n+1)/2}$, the MAC advantage is at most $\mathrm{Adv}^{\mathrm{prp}}_E(q', t') + (2 q^2 m^2 + 1)/2^n$ with $q' = mq$ queries and $t' = t + O(mqn)$ time.

The reduction is tight in time and queries. The bound is not tight in $m$: Proposition 4.2 gives a forger that succeeds with probability at least $0.316 \, q(q-1)/2^n$ from internal collisions, so the $q^2$ term is needed, and Bellare, Pietrzak and Rogaway (CRYPTO 2005) improved the dependence on $m$ to about $m q^2 / 2^n$. For AES this means: change the key well before $2^{64}$ blocks, and in practice after far fewer.

## Complexity

One block cipher call per block: $m$ calls for an $m$-block message, so $\Theta(m)$ time in every case, and $\Theta(n)$ extra space for the chaining value. The calls are strictly sequential, because each input depends on the previous output, so CBC-MAC does not run in parallel, unlike [PMAC](/ocb-mode/) or GHASH. Verification costs the same as tagging.

## Properties

- **Deterministic.** One valid tag per message, so EUF-CMA and SUF-CMA are the same notion.
- **A PRF on fixed-length inputs**, by Theorem 3.2 of Bellare, Kilian and Rogaway, so it is also usable as a key derivation PRF on such inputs.
- **Prefix-free security.** Petrank and Rackoff (2000) show that it stays secure on any message set where no message is a prefix of another. Equal lengths are a special case.
- **Forgeable on variable lengths**, by the splice above, with two queries and no computation.
- **Only the forward cipher.** $E_K^{-1}$ is never used.
- **Online but not parallel.** It processes blocks in order with constant memory, but it needs to know where the message ends only at the end.

## Variants and improvements

- **Length prepended.** Put the length as the first block. The message set becomes prefix-free, so the Petrank and Rackoff result applies. The length must be known at the start. Appending the length at the end instead is insecure.
- **EMAC.** Encrypt the CBC-MAC once more under an independent key: $T = E_{K_2}(\mathrm{CBC\text{-}MAC}_{K_1}(M))$. It is secure for messages of any whole number of blocks (Petrank and Rackoff; Bellare, Pietrzak and Rogaway). It is MAC algorithm 2 of ISO/IEC 9797-1.
- **Retail MAC (ANSI X9.19, ISO/IEC 9797-1 algorithm 3).** DES CBC-MAC with the last block processed by triple DES with a second key. Used in banking.
- **XCBC and CMAC.** Black and Rogaway (CRYPTO 2000) replaced the extra encryption by XOR of a key into the last block (XCBC with three keys). OMAC1 (Iwata and Kurosawa, 2003) derives the extra keys from one key, and NIST adopted it as [CMAC](/cmac/).
- **CBC-MAC in [CCM](/ccm-mode/).** CCM prepends a block $B_0$ that encodes the nonce and the message length, which makes the inputs prefix-free.

## When to use it

Use plain CBC-MAC only inside a construction that fixes the length or makes inputs prefix-free, such as CCM, or for a legacy format that requires it. For a general MAC from a block cipher use [CMAC](/cmac/). For a MAC with no block cipher use [HMAC](/hmac/). For encryption with integrity use an AEAD.

## Pitfalls

- **Variable-length messages under one key.** The splice forgery of the example. This also breaks "CBC-MAC with zero padding" when an attacker can choose lengths.
- **A random IV sent with the tag.** If the chain starts at a random $IV$ that is sent next to the tag, changing $M_1$ and $IV$ by the same XOR keeps the tag: a forgery of the first block for free. The tests show it.
- **Returning the intermediate values.** If every $Y_j$ is output, as in CBC encryption, the scheme is not a MAC.
- **The same key for CBC encryption and CBC-MAC.** Then the tag is the last ciphertext block, and an attacker can change earlier ciphertext blocks and still pass the MAC check after decryption. Use independent keys.
- **Truncating too much.** A tag of $t$ bits allows a guess with probability $2^{-t}$ per try.
- **Using it far past the birthday bound.** With 64-bit block ciphers such as DES or 3DES, $2^{32}$ blocks already give collisions that allow forgery.

## Implementations

The Python code gives `cbc_mac` with the line markers of the pseudocode, `cbc_mac_verify` with a comparison that reads every byte, the two repairs (`cbc_mac_length_prepended` and `emac`) and, only as a target of the tests, the broken random IV variant. AES comes from `aes.py`, which is tested against FIPS 197, Appendix C.1. The tests run the derived SP 800-38A vector, the splice forgery on one-block and multi-block messages, check that the two repairs reject the splice, and check that a single changed bit in the message or the tag is rejected.

## History

Banks used DES CBC-MAC for message authentication in the early 1980s, and NBS published it for US government use as FIPS 113 in 1985. ISO later collected the variants in ISO/IEC 9797 and 9797-1. The variable-length weakness was known in that period, and the standards fixed the length or added a final encryption. Bellare, Kilian and Rogaway (CRYPTO 1994, JCSS 2000) gave the first proof, in the concrete security style they introduced: CBC-MAC of a PRF is a PRF on fixed-length inputs. Petrank and Rackoff (2000) extended it to prefix-free inputs and to EMAC. Black and Rogaway (2000) designed XCBC, and Iwata and Kurosawa (2003) reduced it to one key as OMAC, which became CMAC in NIST SP 800-38B (2005).

## References
