---
tag: 74AABT
kind: technique
slug: gcm-mode
name: Galois/Counter mode
aliases:
- GCM
- AES-GCM
area: cryptography/symmetric-ciphers
level: core
summary: AEAD mode that encrypts with CTR and authenticates with GHASH, a polynomial in a secret H over GF(2^128). Fast and parallel; one repeated IV reveals H and allows forgeries.
prereqs: [ctr-mode, authenticated-encryption, gf2-polynomial-arithmetic]
see_also: [poly1305, chacha20-poly1305, ccm-mode, eax-mode, ocb-mode, nonce, cmac, universal-hash-family]
sources:
  - url: "https://csrc.nist.gov/CSRC/media/Projects/Block-Cipher-Techniques/documents/BCM/proposed-modes/gcm/gcm-spec.pdf"
    title: David A. McGrew and John Viega, The Galois/Counter Mode of Operation (GCM), submission to NIST, revised 2005
    locator: Section 2.3 (encryption, Equations 1 and 2), Section 2.5 (Algorithm 1, multiplication in GF(2^128)) and Appendix B (AES test vectors, Test Cases 1 to 7 and 16)
  - paper: "David A. McGrew and John Viega, The security and performance of the Galois/Counter Mode (GCM) of operation, INDOCRYPT 2004, LNCS 3348, pages 343 to 355"
    locator: the definition of GCM and its security theorems for privacy and authenticity
  - url: "https://doi.org/10.6028/NIST.SP.800-38D"
    title: Morris Dworkin, NIST Special Publication 800-38D, Recommendation for Block Cipher Modes of Operation, Galois/Counter Mode (GCM) and GMAC, 2007
    locator: Section 6 (Algorithms 1 to 3, multiplication, GHASH and GCTR), Section 7 (Algorithms 4 and 5), Section 8 (uniqueness of IVs) and Appendix C (short tags)
  - paper: "Antoine Joux, Authentication failures in NIST version of GCM, comments submitted to NIST, 2006"
    locator: the recovery of H from two messages under one IV, and the forgery that follows
  - paper: "Niels Ferguson, Authentication weaknesses in GCM, comments submitted to NIST, 2005"
    locator: the forgery against short tags that uses blocks at positions 2^i, and the recovery of H that follows
  - paper: "Tetsu Iwata, Keisuke Ohashi and Kazuhiko Minematsu, Breaking and repairing GCM security proofs, CRYPTO 2012, LNCS 7417, pages 31 to 49"
    locator: the flaw in the original proof for IVs that are not 96 bits, and the repaired bounds
  - paper: "Hanno Boeck, Aaron Zauner, Sean Devlin, Juraj Somorovsky and Philipp Jovanovic, Nonce-disrespecting adversaries: practical forgery attacks on GCM in TLS, USENIX WOOT 2016"
    locator: the scan of TLS servers that repeat GCM nonces, and the forgeries against them
---

Galois/Counter Mode (GCM) is an [authenticated encryption](/authenticated-encryption/) mode for a 128-bit [block cipher](/block-cipher/), almost always AES. McGrew and Viega proposed it in 2004, and NIST standardized it in SP 800-38D (2007). GCM encrypts with [CTR mode](/ctr-mode/) and authenticates the associated data and the ciphertext with GHASH, a polynomial evaluated at a secret point $H = E_K(0^{128})$ in the field $\mathrm{GF}(2^{128})$. The polynomial value is masked with $E_K(J_0)$ to form the tag. It is the EtM shape with a Carter and Wegman MAC, and it is the most used AEAD on the internet: TLS, QUIC, IPsec and SSH all have it. Its weak point is the IV: if one IV is used twice under one key, an attacker gets $H$ and can forge tags at will.

**Notation.** $E_K$ is AES with key $K$. $IV$ is the initialization vector, $A$ the associated data, $P$ the plaintext, $C$ the ciphertext, $T$ the tag of $t$ bits. $u$ and $v$ are the numbers of zero bits that pad $C$ and $A$ to whole blocks, and $s$ the number that pads $IV$. $[x]_{64}$ is $x$ as a 64-bit big-endian integer. $\oplus$ and $\cdot$ are addition and multiplication in $\mathrm{GF}(2^{128})$.

## In plain words

GCM does two jobs with one key. First it hides the message with counter mode: it encrypts the numbers 2, 3, 4 and so on after the IV, and XORs the results into the message. Then it computes a checksum of the header and the ciphertext. The checksum treats each 16-byte block as a number in a special arithmetic with no carries, and evaluates a polynomial with these numbers as coefficients at a secret point $H$. Finally it hides the checksum by XOR with the encryption of counter 1. The receiver recomputes the checksum and compares it with the tag before it decrypts anything. Every step is cheap, and the blocks can be processed in parallel.

## When it applies

- **A channel where every message gets a unique IV.** TLS 1.2 and 1.3, QUIC, IPsec ESP (RFC 4106) and SSH all use AES-GCM with an IV built from a sequence number, so it never repeats.
- **High speed.** On processors with AES instructions and carry-less multiplication (AES-NI and PCLMULQDQ, or ARMv8 Crypto), AES-GCM runs at about one cycle per byte or less.
- **Authentication only.** With an empty plaintext GCM is GMAC, a MAC on $A$ alone. It still needs a unique IV.
- **Not with random IVs at large scale.** With random 96-bit IVs, SP 800-38D, Section 8.3, limits one key to $2^{32}$ messages, so that the chance of a repeat stays below $2^{-32}$.
- **Not where IVs may repeat.** A device that loses its counter, or many senders with one key, should use a misuse resistant mode such as AES-GCM-SIV (RFC 8452), or [ChaCha20-Poly1305](/chacha20-poly1305/) with XChaCha20 and random 192-bit nonces.

## The template

```pseudo id=main
MULT(X, Y)                                 ▷ X · Y in GF(2^128), SP 800-38D Algorithm 1
L1  Z ← 0^128;  V ← Y
L2  for i ← 0 to 127 do
L3      if X_i = 1 then Z ← Z ⊕ V
L4      if V_127 = 0 then V ← rightshift(V) else V ← rightshift(V) ⊕ R
L5  return Z

GHASH_H(X_1 … X_m)                         ▷ Algorithm 2
L6  Y ← 0^128
L7  for i ← 1 to m do Y ← MULT(Y ⊕ X_i, H)
L8  return Y

GCM-ENCRYPT(K, IV, A, P)                   ▷ Algorithm 4
L9  H ← E_K(0^128)
L10 if |IV| = 96 then J_0 ← IV ‖ 0^31 ‖ 1
L11 else J_0 ← GHASH_H(IV ‖ 0^(s+64) ‖ [|IV|]_64)
L12 C ← GCTR_K(inc32(J_0), P)
L13 S ← GHASH_H(A ‖ 0^v ‖ C ‖ 0^u ‖ [|A|]_64 ‖ [|C|]_64)
L14 T ← MSB_t(GCTR_K(J_0, S))              ▷ that is, MSB_t(E_K(J_0) ⊕ S)
L15 return (C, T)

GCM-DECRYPT(K, IV, A, C, T)                ▷ Algorithm 5
L16 compute H, J_0 and S as in L9 to L11 and L13
L17 if MSB_t(E_K(J_0) ⊕ S) ≠ T then return FAIL      ▷ constant-time comparison
L18 return GCTR_K(inc32(J_0), C)
```

GCTR is CTR mode in which the counter function is inc32: it adds 1 modulo $2^{32}$ to the rightmost 32 bits and leaves the leftmost 96 bits alone. The holes of the template are the cipher, the tag length $t$ and the IV length. SP 800-38D allows $t \in \{128, 120, 112, 104, 96\}$, and 64 or 32 only under the conditions of its Appendix C.

**The bit order.** This is the part that confuses implementers. A block is a string of bits $X_0 X_1 \ldots X_{127}$, where $X_0$ is the leftmost bit, the high bit of the first byte. GCM reads the block as the polynomial $X_0 + X_1 x + \cdots + X_{127} x^{127}$: the leftmost bit is the constant term. The field is $\mathrm{GF}(2)[x]$ modulo $f(x) = x^{128} + x^7 + x^2 + x + 1$. So in this order:

- the element 1 is the block `80000000000000000000000000000000`;
- multiplication by $x$ moves every coefficient one place up, which is a shift to the right ("rightshift" in L4);
- the coefficient $X_{127}$ shifts out as $x^{128}$, and $x^{128} = x^7 + x^2 + x + 1$ modulo $f$, which in this order is the block $R = 11100001 \,\|\, 0^{120}$, the byte `e1` followed by 15 zero bytes.

Algorithm 1 is the school method: for each bit $X_i$ of the first factor it adds $V = Y \cdot x^i$, and it keeps $V$ reduced with L4. The test `test_gcm_bit_order_is_the_reflected_polynomial_basis` reverses the bits of each block, multiplies as ordinary polynomials modulo $f$ with the constant 0x87, and gets the same result. Hardware with carry-less multiplication usually works on the reversed bits for this reason.

**Why GHASH is a polynomial.** Unroll L7 for blocks $X_1, \ldots, X_m$: $S = X_1 H^m \oplus X_2 H^{m-1} \oplus \cdots \oplus X_m H$. The last block is the length block, so the tag is $T = E_K(J_0) \oplus \sum_i X_i H^{m+1-i}$. For two different inputs of at most $m$ blocks, the difference of their GHASH values is a nonzero polynomial in $H$ of degree at most $m$, so it takes any given value for at most $m$ values of $H$. The lengths in the last block make the encoding of $(A, C)$ injective. This is the almost-XOR-universal property, and with the mask $E_K(J_0)$, which is fresh for each IV, a forgery attempt succeeds with probability about $m/2^t$ plus the PRP terms.

**Security model.** McGrew and Viega (INDOCRYPT 2004) proved GCM secure as a nonce-based AEAD: privacy (indistinguishable from random bits) and authenticity (INT-CTXT), against nonce-respecting adversaries, if AES is a PRP. The bounds have a PRP term, a birthday term of about $\sigma^2/2^{128}$ for $\sigma$ blocks, and a forgery term of about $q_v \ell / 2^t$ for $q_v$ forgery attempts of length at most $\ell$ blocks. Iwata, Ohashi and Minematsu (CRYPTO 2012) found that the original proof was wrong for IVs that are not 96 bits long, because the counter values of two such IVs can collide more often than claimed. They gave a repaired proof with larger constants. For 96-bit IVs the reduction is tight up to the birthday term. Use 96-bit IVs.

**About the code.** The Python code of this page is for study only. It is not constant time: AES uses table lookups and MULT branches on secret bits. Do not use it to protect real data. Use AES-GCM from a FIPS 140 validated module, or the AEAD functions of libsodium. The code follows the template with line markers, checks the tag before it decrypts, and compares tags with OR folding.

### Nonce reuse gives H, and then any forgery

Suppose the sender encrypts two one-block messages $P_1, P_2$ with no associated data under the same key and the same IV. Then $J_0$, $E_K(J_0)$ and the keystream are the same, and the length block $L = [0]_{64} \,\|\, [128]_{64}$ is the same. By the unrolled form, $T_i = C_i H^2 \oplus L H \oplus E_K(J_0)$. Add the two tags:

$$T_1 \oplus T_2 = (C_1 \oplus C_2) \cdot H^2.$$

$C_1 \ne C_2$ when $P_1 \ne P_2$, so $H^2 = (T_1 \oplus T_2) \cdot (C_1 \oplus C_2)^{-1}$. In a field of characteristic 2, squaring is a bijection (the Frobenius map), and its inverse is $y \mapsto y^{2^{127}}$, because $(y^{2^{127}})^2 = y^{2^{128}} = y$. So $H = (H^2)^{2^{127}}$, with no search. Then $E_K(J_0) = T_1 \oplus \mathrm{GHASH}_H(C_1 \,\|\, L)$. With $H$ and $E_K(J_0)$, the attacker computes a valid tag for any $(A', C')$ under that IV. If it knows $P_1$, it also knows the keystream $P_1 \oplus C_1$, so it can choose the plaintext of $C'$. And $H$ stays the same for every IV under the key, so the attacker can forge GHASH under other IVs, as long as it knows $E_K(J_0)$ for them.

For longer messages Joux (2006) noted that $T_1 \oplus T_2$ is a polynomial in $H$ with known coefficients, and that $H$ is one of its roots. Its roots can be found in polynomial time, and a few messages leave one common root. Boeck and others (WOOT 2016) found TLS servers on the internet that repeated GCM nonces, and forged records on them.

### Short tags

With a $t$-bit tag, each forgery attempt succeeds with probability about $m/2^t$ for messages of $m$ blocks, not $2^{-t}$, because of the degree of the polynomial. Ferguson (2005) made this sharper. Squaring is linear over $\mathrm{GF}(2)$, so if the attacker changes only the ciphertext blocks at positions $2^i$, the change of the tag is a $\mathrm{GF}(2)$-linear function of the bits of $H$. The attacker picks the changes so that many bits of this change are zero for every $H$, and a forgery then succeeds much more often than $2^{-t}$. Each success gives linear equations on the bits of $H$, and the next forgeries become easier, until $H$ is known. For this reason SP 800-38D, Appendix C, limits the length of the messages and the number of failed attempts per key for 32-bit and 64-bit tags.

## Classic examples

### Test Case 2 of the specification

The GCM specification, Appendix B, Test Case 2: $K = 0^{128}$, $IV = 0^{96}$, $P = 0^{128}$, no $A$.

| step | value |
|---|---|
| $H = E_K(0^{128})$ | `66e94bd4ef8a2c3b884cfa59ca342b2e` |
| $J_0 = Y_0$ | `00000000000000000000000000000001` |
| $E_K(J_0)$ | `58e2fccefa7e3061367f1d57a4e7455a` |
| $E_K(\mathrm{inc32}(J_0))$ | `0388dace60b6a392f328c2b971b2fe78` |
| $C = P \oplus E_K(\mathrm{inc32}(J_0))$ | `0388dace60b6a392f328c2b971b2fe78` |
| $X_1 = C \cdot H$ | `5e2ec746917062882c85b0685353deb7` |
| $[0]_{64} \,\|\, [128]_{64}$ | `00000000000000000000000000000080` |
| $S = (X_1 \oplus L) \cdot H$ | `f38cbb1ad69223dcc3457ae5b6b0f885` |
| $T = E_K(J_0) \oplus S$ | `ab6e47d42cec13bdf53a67b21257bddf` |

The tests check this trace and the full results of Test Cases 1 to 7 and 16, which cover 96-bit IVs, an 8-byte IV (Test Case 5), a 60-byte IV (Test Case 6), associated data, a partial last block, and 192 and 256-bit keys.

### A nonce reuse in numbers

Key `000102030405060708090a0b0c0d0e0f`, IV `cafebabefacedbaddecaf888` used twice, no $A$.

| | value |
|---|---|
| $P_1$ | `pay 10 EUR to A.` |
| $C_1$, $T_1$ | `f918be96b4c7a144ff42e9fc32dae1c9`, `e6e44832d96af5dbd0dd1b13a762fca1` |
| $P_2$ | `pay 20 EUR to B.` |
| $C_2$, $T_2$ | `f918be96b7c7a144ff42e9fc32dae2c9`, `4e9823f72217e531daef18ec50ad7344` |
| $C_1 \oplus C_2$ | `00000000030000000000000000000300` |
| $T_1 \oplus T_2$ | `a87c6bc5fb7d10ea0a3203fff7cf8fe5` |
| $H^2$ | `70a464963f89b8747f39dd0bf8afb53e` |
| $H = (H^2)^{2^{127}}$ | `c6a13b37878f5b826f4f8162a1c8d879` |
| $E_K(J_0)$ | `a945054aec8b8f4e4bdfe17f0557f09a` |
| forged $P'$ | `pay 9999 EUR, E.` |
| forged $C'$, $T'$ | `f918be96bcceb8388a559cda71dae5c9`, `b57de4624d46ec2914ad3d68a5ede0ac` |

The recovered $H$ equals $E_K(0^{128})$, and the receiver accepts $(C', T')$ and returns `pay 9999 EUR, E.`. The test runs the attack for five random keys, with a forged header as well, and checks that with fresh IVs the same computation gives a wrong $H$.

## Variations

- **GMAC.** GCM with an empty plaintext: a nonce-based MAC on $A$.
- **AES-GCM-SIV (RFC 8452).** Computes POLYVAL (GHASH with the bit order reversed) on the plaintext, derives the IV for CTR from it, and derives fresh keys per nonce. A repeated nonce leaks only equality of messages.
- **IV constructions.** SP 800-38D, Section 8.2, gives the deterministic construction (a fixed field and a counter) and the random bit generator construction. TLS 1.3 XORs a per-connection IV with the record sequence number.
- **Other hash fields.** [Poly1305](/poly1305/) is the same idea with a prime field $\mathbb{Z}_{2^{130}-5}$ and addition of the mask modulo $2^{128}$; it is the MAC of [ChaCha20-Poly1305](/chacha20-poly1305/).
- **Other AEAD modes with AES.** [CCM](/ccm-mode/) (CBC-MAC and CTR, no field arithmetic), [EAX](/eax-mode/) (OMAC and CTR) and [OCB](/ocb-mode/) (one pass).

## Pitfalls

- **Repeating an IV under one key.** It gives the XOR of the plaintexts, as in CTR, and it gives $H$, which allows forgeries for the life of the key.
- **Random IVs beyond the limit.** With random 96-bit IVs, $2^{32}$ messages is the limit of SP 800-38D. Many keys per sender, or XChaCha20-Poly1305, avoid it.
- **IVs that are not 96 bits.** They pass through GHASH, so two different IVs can give overlapping counters, and the proofs are weaker. Use 96-bit IVs.
- **Short tags.** A 32-bit tag gives far less than 32 bits of forgery resistance for long messages (Ferguson 2005).
- **Releasing plaintext before the tag check.** Streaming decryptors that output plaintext before the end lose the INT-CTXT guarantee in practice. Check first, as L17 does.
- **Counter overflow.** A message has at most $2^{32} - 2$ blocks, so that inc32 never reaches $J_0$ again. SP 800-38D sets $|P| \le 2^{39} - 256$ bits.
- **Timing.** A table-based GHASH leaks $H$ through cache timing. Use carry-less multiply instructions or a constant-time bitsliced method.

## Exercises

1. Show that the map $y \mapsto y^2$ on $\mathrm{GF}(2^{128})$ is $\mathrm{GF}(2)$-linear, and that $y^{2^{127}}$ is its inverse.
2. Two messages of two blocks each, with no $A$, are encrypted under one IV. Write $T_1 \oplus T_2$ as a polynomial in $H$, and say how many candidates for $H$ it gives at most.
3. Show that without the length block, GHASH would give the same value for $A = \varepsilon, C = X$ and $A = X, C = \varepsilon$ when $X$ is one block, and build a forgery from it.
4. With random 96-bit IVs, how many messages give a chance of $2^{-32}$ that some IV repeats? Compare with the limit of SP 800-38D.
5. Explain why a 64-bit block cipher cannot be used in GCM, and what changes would be needed.

## References

- David A. McGrew and John Viega, The Galois/Counter Mode of Operation (GCM), 2005, and INDOCRYPT 2004.
- Morris Dworkin, NIST SP 800-38D, 2007.
- Antoine Joux, Authentication failures in NIST version of GCM, 2006.
- Niels Ferguson, Authentication weaknesses in GCM, 2005.
- Tetsu Iwata, Keisuke Ohashi and Kazuhiko Minematsu, CRYPTO 2012.
- Hanno Boeck, Aaron Zauner, Sean Devlin, Juraj Somorovsky and Philipp Jovanovic, USENIX WOOT 2016.
