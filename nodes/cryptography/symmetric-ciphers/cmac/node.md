---
tag: 57R39D
kind: algorithm
slug: cmac
name: CMAC
aliases:
- OMAC1
- OMAC
area: cryptography/symmetric-ciphers
level: advanced
summary: CBC-MAC whose last block is XORed with a subkey K1 if it is full, or padded with 10..0 and XORed with K2. Both subkeys come from E_K(0^n) by doubling. Secure for any length.
solves: [message-authentication]
model: word-ram
complexity:
  vars: {m: the number of message blocks, n: the block length}
  time: {worst: Θ(m), average: Θ(m), best: Θ(m)}
  space: {extra: Θ(n)}
properties: {deterministic: true}
history:
  year: 2003
  people: [Tetsu Iwata, Kaoru Kurosawa]
  note: Iwata and Kurosawa published OMAC at FSE 2003, building on XCBC of Black and Rogaway (2000). NIST adopted OMAC1 as CMAC in SP 800-38B (2005), and RFC 4493 (2006) specifies AES-CMAC.
prereqs: [cbc-mac, gf2-polynomial-arithmetic]
see_also: [cbc-mac, message-authentication-code, hmac, eax-mode, xts-mode, ocb-mode, pseudorandom-function, siphash]
sources:
  - url: "https://doi.org/10.6028/NIST.SP.800-38B"
    title: Morris Dworkin, NIST Special Publication 800-38B, Recommendation for Block Cipher Modes of Operation, The CMAC Mode for Authentication, 2005 (updated 2016)
    locator: Section 5.3 (subkeys and R_128), Section 6.1 (subkey generation), Section 6.2 (MAC generation), Section 6.3 (verification), Appendix A (MAC length) and Appendix B (message span of the key)
  - url: "https://www.rfc-editor.org/rfc/rfc4493"
    title: JunHyuk Song, Radha Poovendran, Jicheol Lee and Tetsu Iwata, RFC 4493, The AES-CMAC Algorithm, 2006
    locator: Section 2.3 (Generate_Subkey), Section 2.4 (MAC generation) and Section 4 (test vectors, subkeys and Examples 1 to 4)
  - paper: "Tetsu Iwata and Kaoru Kurosawa, OMAC: One-Key CBC MAC, Fast Software Encryption (FSE 2003), LNCS 2887, pages 129 to 153"
    locator: the definition of OMAC1 and OMAC2 and the proof that OMAC is a variable-input-length PRF with a bound of order m^2 q^2 / 2^n
  - paper: "John Black and Phillip Rogaway, CBC MACs for arbitrary-length messages: the three-key constructions, CRYPTO 2000, LNCS 1880, pages 197 to 215 (Journal of Cryptology 18(2), 2005)"
    locator: XCBC, the three-key design that CMAC reduces to one key
---

CMAC is the standard way to build a MAC for messages of any length from a block cipher. It is [CBC-MAC](/cbc-mac/) with one change at the end: before the last block is encrypted, it is XORed with a secret subkey $K_1$ if it is a full block, or padded with a 1 bit and zeros and XORed with a second subkey $K_2$ if it is not. Both subkeys come from one key: $L = E_K(0^n)$, $K_1 = 2L$ and $K_2 = 4L$, where $2X$ means doubling in $\mathrm{GF}(2^n)$. NIST specifies it in SP 800-38B; it is OMAC1 of Iwata and Kurosawa (FSE 2003), and RFC 4493 gives AES-CMAC with test vectors.

**Notation.** $E_K$ is the block cipher with block length $n$ bits ($n = 128$ for AES), $M = M_1 \cdots M_m$ the message with a last block $M_m^*$ of $1$ to $n$ bits (or empty if $M$ is empty), $\mathrm{dbl}$ the doubling map, $C_i$ the chaining values, $T$ the tag and $t$ its length.

## In plain words

Plain CBC-MAC fails because its tag is also the internal state after the message, so an attacker can continue the chain. CMAC hides the end of the chain. The last block is XORed with a secret value before the final encryption, so the tag no longer tells the attacker the state from which a longer message would continue.

There are two secret values because there are two kinds of last block. A full last block gets $K_1$. A short last block is first padded with a 1 bit and then zeros up to a full block, and it gets $K_2$. Without the two different values, the message `ab` and the message `ab` followed by the padding bytes would give the same tag.

## The problem

[Message authentication](/message-authentication/) for messages of any bit length, from a block cipher, with one key and with no extra block cipher call for messages that are a whole number of blocks long.

## The algorithm

```pseudo id=main
SUBKEYS(K)                              ▷ SP 800-38B, Section 6.1
L1  L ← E_K(0^n)
L2  K1 ← dbl(L)                         ▷ dbl(X) = (X ≪ 1) ⊕ (MSB₁(X) · R_n)
L3  K2 ← dbl(K1)                        ▷ R_128 = 0^120 10000111

CMAC(K, M, t)                           ▷ SP 800-38B, Section 6.2
L4  m ← max(1, ⌈|M| / n⌉);  split M into M_1, …, M_{m−1}, M_m*
L5  if |M_m*| = n then M_m ← M_m* ⊕ K1
L6  else M_m ← (M_m* ‖ 1 0^{n − 1 − |M_m*|}) ⊕ K2
L7  C ← 0^n
L8  for i ← 1 to m − 1 do
L9      C ← E_K(C ⊕ M_i)
L10 C ← E_K(C ⊕ M_m)
L11 return MSB_t(C)

VERIFY(K, M, T)                         ▷ Section 6.3
L12 return CMAC(K, M, |T|) = T, compared in constant time
```

The doubling map is multiplication by the polynomial $x$ in $\mathrm{GF}(2^{128})$ defined by $x^{128} + x^7 + x^2 + x + 1$, with the leftmost bit as the coefficient of $x^{127}$. Shift left by one bit; if a 1 fell off the left end, XOR the constant $R_{128}$ = `00..0087` into the right end. For 64-bit block ciphers the polynomial is $x^{64} + x^4 + x^3 + x + 1$ and $R_{64}$ = `00..001b`. The empty message is one incomplete block: it is padded to $10^{n-1}$ and masked with $K_2$. $L$ and the subkeys are secret, and SP 800-38B, Section 5.3, forbids using $E_K(0^n)$ for any other purpose, for example as a key check value.

**About the code.** The Python code is for study only and is not constant time: the AES in `aes.py` reads tables at secret indices, and `dbl` branches on a secret bit. A real implementation computes the mask from the top bit without a branch. Use AES-CMAC from a FIPS 140 validated module.

## Example

RFC 4493, Section 4, with key $K$ = `2b7e151628aed2a6abf7158809cf4f3c`.

| value | hex |
|---|---|
| $L = E_K(0^{128})$ | `7df76b0c1ab899b33e42f047b91b546f` |
| $K_1 = \mathrm{dbl}(L)$ (top bit of $L$ is 0, so a plain shift) | `fbeed618357133667c85e08f7236a8de` |
| $K_2 = \mathrm{dbl}(K_1)$ (top bit of $K_1$ is 1, so shift and XOR `87`) | `f7ddac306ae266ccf90bc11ee46d513b` |

The four examples of RFC 4493, Section 4, use prefixes of the 64-byte message `6bc1bee2…e66c3710` (the plaintext of SP 800-38A, Appendix F).

| example | length in bytes | case | tag |
|---|---|---|---|
| 1 | 0 | empty, padded, $K_2$ | `bb1d6929e95937287fa37d129b756746` |
| 2 | 16 | full, $K_1$ | `070a16b46b4d4144f79bdd9dd04a287c` |
| 3 | 40 | 8-byte last block, padded, $K_2$ | `dfa66747de9ae63030ca32611497c827` |
| 4 | 64 | full, $K_1$ | `51f0bebf7e3b9d92fc49741779363cfe` |

Trace of Example 3 ($m = 3$): $C_1 = E_K(M_1)$ = `3ad77bb40d7a3660a89ecaf32466ef97` (the same value as the first ECB block of SP 800-38A, F.1.1), $C_2$ = `b148c17f309ee692287ae57cf12add49`. The last block `30c81c46a35ce411` is padded to `30c81c46a35ce4118000000000000000` and XORed with $K_2$ to give `c715b076c9be82dd790bc11ee46d513b`. Then $E_K(C_2 \oplus M_3)$ is the tag `dfa66747de9ae63030ca32611497c827`.

## Correctness

**Claim.** (1) VERIFY accepts every tag that CMAC computes, for every tag length $t$. (2) $\mathrm{dbl}$ is multiplication by $x$ in $\mathrm{GF}(2^n)$, so it is a bijection and $K_1 \ne K_2$ unless $L = 0^n$. (3) Among messages whose last blocks are of the same kind (full, or padded), the map from $M$ to the encoded block sequence $(M_1, \ldots, M_{m-1}, M_m)$ is injective. A full last block $A$ and a padded last block $B$ give the same encoded block only if $A \oplus \mathrm{pad}(B) = K_1 \oplus K_2 = L \cdot (x^2 + x)$, which is a nonzero secret when $L \ne 0^n$. The key step for (3) is that the padding $10^j$ is injective on strings shorter than $n$ bits. The full proof is below.

**Security.** Correctness does not imply security. Iwata and Kurosawa (FSE 2003) prove that OMAC is a pseudorandom function on messages of any length, with a PRF advantage of at most the PRP advantage of $E$ plus a term of order $m^2 q^2 / 2^n$ for $q$ queries of at most $m$ blocks; the paper states the term as $(5m^2 + 1) q^2 / 2^n$. Later work by the same authors (Indocrypt 2003) and by Nandi replaced $m^2 q^2$ by terms in the total number of blocks $\sigma$, of order $\sigma^2 / 2^n$. The reduction is tight in time and queries; the birthday attack on CBC-type MACs shows that a loss of order $q^2 / 2^n$ is necessary. Then, by the theorem on the [MAC](/message-authentication-code/) page, a forgery costs this bound plus $2^{-t}$ per try.

## Complexity

$m$ block cipher calls for a message of $m \ge 1$ blocks, plus one call for $L$ that is done once per key and cached, so $\Theta(m)$ time. Extra space is $\Theta(n)$: the chaining value and the two subkeys. The chain is sequential, as in CBC-MAC. The cost is one call per block, the same as CBC-MAC with no padding, and one call fewer than EMAC.

## Properties

- **Deterministic**, with one valid tag per message and tag length, so it is also strongly unforgeable.
- **Any bit length**, including the empty message, with no length field and no extra block for messages that fill whole blocks.
- **One key.** XCBC needed a block cipher key and two $n$-bit keys; CMAC derives both masks from $E_K(0^n)$.
- **Only the forward cipher**, so it also works with a PRF in place of $E$.
- **Online.** The message can be processed as it arrives, but the last block must be held back until the end is known, because its mask depends on whether it is full.
- **Birthday-bound security.** About $2^{n/2}$ blocks under one key, so $2^{64}$ for AES and only $2^{32}$ for 64-bit ciphers. SP 800-38B, Appendix B, recommends at most $2^{48}$ messages per key with AES and $2^{21}$ with a 64-bit cipher.

## Variants and improvements

- **OMAC2.** The second variant of Iwata and Kurosawa uses $K_2 = L \cdot x^{-1}$ instead of $L \cdot x^2$. It was not standardized.
- **XCBC and TMAC.** XCBC (Black and Rogaway, 2000) uses three keys; TMAC (Kurosawa and Iwata, 2003) uses two. CMAC is their one-key form.
- **Truncated tags.** RFC 4494 uses AES-CMAC-96 in IPsec. SP 800-38B, Appendix A, says that tags of at least 64 bits suffice for most uses, and gives the rule $t \ge \lg(\mathrm{MaxInvalids}/\mathrm{Risk})$ for shorter ones.
- **A PRF for key derivation.** RFC 4615 defines AES-CMAC-PRF-128 for keys of any length, and SP 800-108 allows CMAC as the PRF of its key derivation functions.
- **In other modes.** [EAX](/eax-mode/) uses OMAC with a tweak block for the nonce, the header and the ciphertext. SIV (RFC 5297) uses S2V, a vector form of CMAC.
- **PMAC.** A parallel MAC by Black and Rogaway (2002) with the same doubling masks at each block, related to [OCB](/ocb-mode/).

## When to use it

Use AES-CMAC when a protocol needs a MAC from the block cipher it already has, for example on hardware with AES but no hash function, in smart cards, or in protocols that specify it (IPsec AES-CMAC-96, the 5G integrity algorithm NIA2, Bluetooth and IEEE 802.11 management frames). When a hash function is available, [HMAC](/hmac/) is the more common choice. For encryption with integrity, use an AEAD instead of a separate CMAC.

## Pitfalls

- **Same key for encryption and CMAC.** Use an independent key for the MAC, or an AEAD.
- **Leaking $L = E_K(0^n)$.** It gives both subkeys. Some systems publish $E_K(0^n)$ as a key check value; SP 800-38B forbids this for a CMAC key.
- **Too many blocks with a 64-bit cipher.** CMAC with 3DES reaches its birthday bound after about $2^{32}$ blocks.
- **Wrong bit order in doubling.** CMAC doubles in big-endian order (leftmost bit first), XTS doubles in little-endian order. Mixing them gives wrong subkeys that still look random, so always test against RFC 4493.
- **Comparing tags with an early exit.** Leaks the tag byte by byte under a timing attack.
- **Short tags without a limit on failed tries.** A 32-bit tag allows a forgery after about $2^{32}$ online guesses.

## Implementations

The Python code gives `dbl`, `subkeys` and `cmac` with the line markers of the pseudocode, and `cmac_verify`, which compares every byte. AES comes from `aes.py`, tested against FIPS 197, Appendix C.1. The tests check the subkeys and all four examples of RFC 4493, Section 4, the linearity of doubling, truncated tags, rejection of every changed tag bit and of changed message bits, that padded and full last blocks give different tags, that CMAC equals CBC-MAC with a masked last block, and that the CBC-MAC splice forgery fails.

## History

The variable-length weakness of [CBC-MAC](/cbc-mac/) led to fixes with extra key material. Black and Rogaway (CRYPTO 2000) proposed XCBC, with one block cipher key and two masks, and proved it secure for any length. Kurosawa and Iwata reduced the key to two parts in TMAC (CT-RSA 2003), and Iwata and Kurosawa reduced it to one in OMAC (FSE 2003), where the masks are multiples of $E_K(0^n)$. NIST adopted OMAC1 as CMAC in SP 800-38B in May 2005, and RFC 4493 (June 2006) specified AES-CMAC with the same test vectors. A 2016 update of SP 800-38B moved the examples of Appendix D to the NIST web site.

## References
