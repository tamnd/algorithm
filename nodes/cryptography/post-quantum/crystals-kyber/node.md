---
tag: X4A2D0
kind: algorithm
slug: crystals-kyber
name: CRYSTALS-Kyber
aliases:
- Kyber
- ML-KEM
- FIPS 203
area: cryptography/post-quantum
level: advanced
summary: "The module-LWE KEM that NIST standardized as ML-KEM (FIPS 203, 2024): an LWE encryption over Z_3329[X]/(X^256 + 1) with compression and the NTT, made IND-CCA by an FO transform."
model: word-ram
complexity:
  vars: {k: "the module rank (2, 3 or 4)", n: the polynomial degree (256)}
  time: {worst: Θ(k^2 n + k n log n), average: Θ(k^2 n + k n log n), best: Θ(k^2 n + k n log n)}
  space: {extra: Θ(k^2 n)}
properties: {deterministic: false, randomized: true}
history:
  year: 2018
  people: [Joppe Bos, Léo Ducas, Eike Kiltz, Tancrède Lepoint, Vadim Lyubashevsky, John M. Schanck, Peter Schwabe, Gregor Seiler, Damien Stehlé]
  note: Submitted to the NIST process in 2017 and published at IEEE EuroS&P 2018. NIST selected it in July 2022 and published it as ML-KEM in FIPS 203 in August 2024.
prereqs: [module-learning-with-errors, key-encapsulation-mechanism, fujisaki-okamoto-transform, number-theoretic-transform]
see_also: [regev-encryption, crystals-dilithium, saber, newhope, frodokem, ntru-encrypt, hybrid-key-exchange, nist-pqc-standardization]
sources:
  - paper: doi:10.1109/EuroSP.2018.00032
    title: Joppe Bos, Léo Ducas, Eike Kiltz, Tancrède Lepoint, Vadim Lyubashevsky, John M. Schanck, Peter Schwabe, Gregor Seiler and Damien Stehlé, CRYSTALS-Kyber, a CCA-secure module-lattice-based KEM, IEEE EuroS&P 2018, pages 353 to 367
    locator: the CPA-secure encryption Kyber.CPAPKE, the compression functions, the CCA-secure KEM by an FO transform, and the parameter choice
  - paper: doi:10.6028/NIST.FIPS.203
    title: NIST, FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard, August 2024
    locator: "Algorithms 13 to 15 (K-PKE), 16 to 18 (internal functions), 19 to 21 (ML-KEM.KeyGen, Encaps and Decaps with input checks), Section 4.2.1 (Compress and Decompress), Section 4.3 (the NTT with zeta = 17), Section 8 (parameter sets and sizes) and Appendix C (differences from the round 3 submission)"
  - url: "https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf"
    title: Roberto Avanzi and others, CRYSTALS-Kyber, Algorithm Specifications and Supporting Documentation, version 3.02, 2021
    locator: the round 3 KEM with the hash of m and the key derivation from H(c), which FIPS 203 changed
  - url: "https://github.com/usnistgov/ACVP-Server/tree/master/gen-val/json-files"
    title: NIST, ACVP-Server, the files ML-KEM-keyGen-FIPS203 and ML-KEM-encapDecap-FIPS203
    locator: "keyGen tcIds 1, 26 and 51, and encapDecap test group 1, tcId 1 (copied in the tests)"
  - paper: "Dennis Hofheinz, Kathrin Hövelmanns and Eike Kiltz, A modular analysis of the Fujisaki-Okamoto transformation, TCC 2017, LNCS 10677, Springer, 2017, pages 341 to 371"
    locator: the transforms with implicit rejection and their bounds in the random oracle and quantum random oracle models
  - paper: doi:10.6028/NIST.IR.8413-upd1
    title: Gorjan Alagic and others, Status report on the third round of the NIST post-quantum cryptography standardization process, NIST IR 8413, July 2022
    locator: the selection of CRYSTALS-Kyber as the KEM to standardize
---

CRYSTALS-Kyber is a key encapsulation mechanism built on the [module learning with errors](/module-learning-with-errors/) problem. NIST selected it in 2022 and published it in August 2024 as ML-KEM in FIPS 203, the first post-quantum KEM standard. Its core is a [Regev-style encryption](/regev-encryption/) over a module of rank $k$ over the ring $R_q = \mathbb{Z}_q[X]/(X^{256}+1)$ with $q = 3329$, with the ciphertext compressed by rounding and all products done in the [number-theoretic transform](/number-theoretic-transform/) domain. A variant of the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/) with implicit rejection turns this CPA-secure encryption into an [IND-CCA](/ind-cca-security/) [KEM](/key-encapsulation-mechanism/). ML-KEM-768 has an encapsulation key of 1184 bytes and a ciphertext of 1088 bytes, and it runs faster than an elliptic curve key exchange.

**Notation.** $R_q = \mathbb{Z}_q[X]/(X^{256}+1)$ with $q = 3329$ and $n = 256$. Bold letters are vectors or matrices over $R_q$ of size $k$ or $k \times k$. A hat, as in $\hat{t}$, marks a value in the NTT domain, and $\circ$ is the product there. $\mathrm{CBD}_\eta$ is the centered binomial distribution with values in $[-\eta, \eta]$. $H$ is SHA3-256, $G$ is SHA3-512 split into two 32-byte halves, $J$ is SHAKE256 with a 32-byte output, $\mathrm{PRF}_\eta(s, b)$ is SHAKE256 of $s \| b$ with $64\eta$ bytes of output, and SampleNTT reads SHAKE128 (see [SHA-3](/sha-3/) and [SHAKE](/shake/)). $\mathrm{Compress}_d$ and $\mathrm{Decompress}_d$ map between $\mathbb{Z}_q$ and $d$ binary digits. ByteEncode$_d$ packs 256 numbers of $d$ binary digits into $32d$ bytes.

## In plain words

Kyber is a way for two computers to agree on a secret key over an open line, in a form that quantum computers are not known to break. The receiver publishes a key made of noisy equations in a secret. The sender picks a random 32-byte message, hides it in new noisy equations made from the public key, and both sides derive the shared key from that message.

The equations use polynomials instead of plain numbers, which makes the keys short and the arithmetic fast. The sender also throws away the low digits of the ciphertext to make it shorter; that adds a bit more noise, which the receiver can still remove.

To stop an attacker who sends crafted ciphertexts, the receiver encrypts the message again after decryption. If the result differs from what arrived, the receiver returns a random-looking key instead of an error.

## The problem

ML-KEM solves the [key encapsulation](/key-encapsulation-mechanism/) problem: KeyGen outputs an encapsulation key $ek$ and a decapsulation key $dk$; Encaps$(ek)$ outputs a shared key $K$ of 32 bytes and a ciphertext $c$; Decaps$(dk, c)$ recovers $K$. The goal is IND-CCA2 security: an adversary that can ask for the decapsulation of any ciphertext except the challenge cannot tell the real $K$ from a random string. The assumption is that decision module-LWE is hard over $R_q$ with rank $k$.

## The algorithm

FIPS 203 builds ML-KEM in three layers: the CPA-secure encryption K-PKE (Algorithms 13 to 15), the internal KEM functions that take their randomness as input (Algorithms 16 to 18), and the external functions that draw the randomness and check the inputs (Algorithms 19 to 21).

```pseudo id=main
K-PKE.KEYGEN(d)                                   ▷ Algorithm 13, d is 32 bytes
L1  (ρ, σ) ← G(d ‖ k)                              ▷ k as one byte: domain separation
L2  Â[i][j] ← SampleNTT(ρ ‖ j ‖ i) for i, j < k    ▷ uniform in the NTT domain
L3  s, e ← k polynomials each from CBD_η1(PRF_η1(σ, N)), N = 0, 1, ..., 2k − 1
L4  t̂ ← Â ∘ NTT(s) + NTT(e)
L5  return ek = ByteEncode_12(t̂) ‖ ρ,  dk_PKE = ByteEncode_12(NTT(s))

K-PKE.ENCRYPT(ek, m, r)                           ▷ Algorithm 14, m and r are 32 bytes
L6  decode t̂ and ρ from ek, and rebuild Â as in line L2
L7  y ← CBD_η1 (k polynomials), e1 ← CBD_η2 (k polynomials), e2 ← CBD_η2, all from PRF(r, N)
L8  u ← NTT⁻¹(Âᵀ ∘ NTT(y)) + e1
L9  μ ← Decompress_1(ByteDecode_1(m));  v ← NTT⁻¹(t̂ᵀ ∘ NTT(y)) + e2 + μ
L10 return c = ByteEncode_du(Compress_du(u)) ‖ ByteEncode_dv(Compress_dv(v))

K-PKE.DECRYPT(dk_PKE, c)                          ▷ Algorithm 15
L11 u' ← Decompress_du(ByteDecode_du(c1));  v' ← Decompress_dv(ByteDecode_dv(c2))
L12 w ← v' − NTT⁻¹(ŝᵀ ∘ NTT(u'))
L13 return m = ByteEncode_1(Compress_1(w))

ML-KEM.KEYGEN_INTERNAL(d, z)                      ▷ Algorithm 16
L14 (ek, dk_PKE) ← K-PKE.KeyGen(d)
L15 return ek, dk = dk_PKE ‖ ek ‖ H(ek) ‖ z

ML-KEM.ENCAPS_INTERNAL(ek, m)                     ▷ Algorithm 17
L16 (K, r) ← G(m ‖ H(ek))
L17 c ← K-PKE.Encrypt(ek, m, r);  return (K, c)

ML-KEM.DECAPS_INTERNAL(dk, c)                     ▷ Algorithm 18
L18 split dk into dk_PKE, ek, h and z
L19 m' ← K-PKE.Decrypt(dk_PKE, c);  (K', r') ← G(m' ‖ h);  K̄ ← J(z ‖ c)
L20 c' ← K-PKE.Encrypt(ek, m', r')
L21 if c ≠ c' then K' ← K̄                          ▷ implicit rejection
    return K'

ML-KEM.KEYGEN()                                   ▷ Algorithm 19
L22 d, z ← 32 fresh random bytes each;  return KeyGen_internal(d, z)
ML-KEM.ENCAPS(ek)                                 ▷ Algorithm 20
L23 check the length of ek and that ByteEncode_12(ByteDecode_12(t̂ part)) = t̂ part
    m ← 32 fresh random bytes;  return Encaps_internal(ek, m)
ML-KEM.DECAPS(dk, c)                              ▷ Algorithm 21
L24 check the lengths of dk and c and that H(ek) = h;  return Decaps_internal(dk, c)
```

**Compression.** $\mathrm{Compress}_d(x) = \lceil (2^d/q) \cdot x \rfloor \bmod 2^d$ and $\mathrm{Decompress}_d(y) = \lceil (q/2^d) \cdot y \rfloor$, where $\lceil \cdot \rfloor$ rounds to the nearest integer. Decompress after Compress moves $x$ by at most $\lceil q/2^{d+1} \rfloor$ on the circle $\mathbb{Z}_q$. With $d = 1$, Compress tells whether $x$ is closer to $q/2$ than to 0, which is the rounding step of Regev decryption.

**The NTT.** $q - 1 = 3328 = 2^8 \cdot 13$, so $\mathbb{Z}_q$ has a primitive 256th root of unity, $\zeta = 17$, but no 512th root. $X^{256} + 1$ then splits into the 128 quadratic factors $X^2 - \zeta^{2\,\mathrm{BitRev}_7(i) + 1}$, and the NTT of FIPS 203 (Algorithm 9) has 7 layers, not 8. A product in the NTT domain is 128 products of degree-1 polynomials modulo these factors (Algorithms 11 and 12). The matrix $\hat{A}$ is sampled directly in the NTT domain, so it is never transformed.

**Parameter sets** (FIPS 203, Tables 2 and 3):

| set | $k$ | $\eta_1$ | $\eta_2$ | $d_u$ | $d_v$ | $ek$ bytes | $dk$ bytes | $c$ bytes | category |
|---|---|---|---|---|---|---|---|---|---|
| ML-KEM-512 | 2 | 3 | 2 | 10 | 4 | 800 | 1632 | 768 | 1 |
| ML-KEM-768 | 3 | 2 | 2 | 10 | 4 | 1184 | 2400 | 1088 | 3 |
| ML-KEM-1024 | 4 | 2 | 2 | 11 | 5 | 1568 | 3168 | 1568 | 5 |

The shared key is always 32 bytes. FIPS 203 gives decapsulation failure rates of about $2^{-139}$, $2^{-164}$ and $2^{-175}$ for the three sets. The categories are the [NIST security levels](/nist-security-levels/).

**Differences from the round 3 Kyber.** FIPS 203, Appendix C, lists the changes that alter the input and output behavior. The round 3 KEM hashed the random $m$ before use ($m \leftarrow H(m)$); ML-KEM does not, because it requires an approved random source. Round 3 derived the shared key as a hash of $\bar K$ and $H(c)$; ML-KEM takes $K$ from $G(m \| H(ek))$ directly and no longer hashes the ciphertext, and Decaps changed to match. The shared key has a fixed length of 32 bytes. ML-KEM adds the input checks of lines L23 and L24. After the initial public draft of August 2023, the final standard added the domain separation byte $k$ in line L1 and restored the index order of $\hat A$ of round 3, which the draft had swapped by mistake. So the round 3 known answer files do not match ML-KEM.

## Example

**One coefficient.** Take $q = 3329$. A message bit 1 becomes $\mathrm{Decompress}_1(1) = 1665$. If the noise in that coefficient after decryption is $+200$, then $w = 1865$, and $\mathrm{Compress}_1(1865) = \lceil 2 \cdot 1865 / 3329 \rfloor = \lceil 1.12 \rfloor = 1$, the right bit. With noise $+900$, $w = 2565$ and $\lceil 1.54 \rfloor = 2 \equiv 0$, a decryption failure; the bit survives while the noise stays below about $q/4 \approx 832$. Compression with $d = 10$ sends $x = 1000$ to $308$ and back to $1001$; with $d = 4$ it sends $1000$ to $5$ and back to $1040$, a rounding error of 40, below the bound $\lceil 3329/32 \rfloor = 104$.

**The NTT root.** $17^{128} \equiv 3328 \equiv -1 \pmod{3329}$, so 17 has order exactly 256.

**An official vector.** ACVP test group 1 of ML-KEM-encapDecap-FIPS203, tcId 1, is ML-KEM-512 encapsulation with the message $m$ = `DCACFE4D...4CC0EF4A`. The expected shared key is $K$ = `2D74374B55D29AA585E144A29BA4F0A96537A73B4F176C5527075F66E38E8858`, and the 768-byte ciphertext has SHA-256 `081d14f4...07b81e4a`. The code on this page reproduces both, and the key generation vectors tcId 1, 26 and 51 for the three parameter sets.

## Correctness

Decryption computes $w = v' - \mathbf{s}^\mathsf{T} \mathbf{u}'$. With $\mathbf{t} = A\mathbf{s} + \mathbf{e}$, $\mathbf{u}' = \mathbf{u} + \mathbf{c}_u$ and $v' = v + c_v$ for the compression errors $\mathbf{c}_u, c_v$, this is $w = \mu + \mathbf{e}^\mathsf{T}\mathbf{y} + e_2 + c_v - \mathbf{s}^\mathsf{T}(\mathbf{e}_1 + \mathbf{c}_u)$, the message plus a noise polynomial whose coefficients are sums of products of small terms. When each coefficient of the noise is below $\lceil q/4 \rfloor$ in absolute value, Compress$_1$ returns $m$, the re-encryption in line L20 gives $c' = c$, and Decaps returns $K' = K$. The full proof is in the proof file; the probability that the noise is too large is the failure rate above, computed in the Kyber papers by convolving the exact distributions.

## Complexity

The work is dominated by sampling $\hat{A}$ ($k^2$ polynomials from SHAKE128, $\Theta(k^2 n)$) and by $k$ forward and $k$ inverse NTTs ($\Theta(k\, n \log n)$). Products in the NTT domain cost $\Theta(k^2 n)$. Decaps costs one decryption and one full encryption. Keys and ciphertexts have $\Theta(k n)$ coefficients. On a modern x86 core the optimized AVX2 code runs each operation of ML-KEM-768 in a few tens of thousands of cycles. The extra memory is $\Theta(k^2 n)$ if $\hat{A}$ is stored, or $\Theta(k n)$ if it is sampled one entry at a time.

## Properties

- **IND-CCA2.** K-PKE is IND-CPA under decision module-LWE: the public key $(\hat A, \hat t)$ is pseudorandom, and then $(\mathbf{u}, v)$ is pseudorandom too. The FO transform with implicit rejection makes the KEM IND-CCA2 in the [random oracle model](/random-oracle-model/), with a bound that also covers the decryption failures, and in the [quantum random oracle model](/quantum-random-oracle-model/) with a looser bound (Hofheinz, Hövelmanns and Kiltz 2017, and later work).
- **Implicit rejection.** A bad ciphertext gives the pseudorandom key $J(z \| c)$, not an error, so an attacker learns nothing from the form of the answer.
- **Small, nonzero failure rate.** Correctness holds except with probability about $2^{-139}$ or less, which the security proof accounts for.
- **Binding.** The key depends on $H(ek)$, so it is bound to the public key; it is not bound to the ciphertext by a hash, which some protocols must keep in mind.
- **Randomized.** Encaps needs 32 fresh random bytes; KeyGen needs 64.

## Variants and improvements

- **Round 3 Kyber** (2021) differs as listed above. Kyber-90s replaced SHAKE and SHA-3 by AES and SHA-2 in round 2 and 3, and was dropped.
- **[Saber](/saber/)** uses module learning with rounding and a power-of-two modulus, so it has no NTT. **[NewHope](/newhope/)** is the ring version with $n = 1024$. **[FrodoKEM](/frodokem/)** uses plain LWE without ring structure.
- **Hybrids.** X25519MLKEM768 combines [X25519](/x25519/) and ML-KEM-768 in TLS 1.3, so that the key stays secret if either part holds (see [hybrid key exchange](/hybrid-key-exchange/)).
- **Seeds as keys.** FIPS 203 allows storing the 64-byte seed $(d, z)$ instead of $dk$; the domain separation byte of line L1 stops a seed from being reused at another security level.

## When to use it

Use ML-KEM when you need a post-quantum key exchange or key transport today. It is the NIST standard, it is fast, and its sizes fit in one network packet for ML-KEM-768. The common choice is ML-KEM-768 in a hybrid with X25519. Choose ML-KEM-1024 for category 5. Prefer FrodoKEM only if you do not want to rely on the structure of module lattices and can pay ten times the size.

## Pitfalls

- **Timing leaks.** KyberSlash (2023 and 2024) found that several implementations computed Compress with a division whose time depends on the secret, which leaks the key over the network. Use constant-time code throughout, including the comparison in line L21.
- **Skipping the input checks.** Line L23 must reject an $ek$ whose coefficients are not below $q$; line L24 must check $H(ek)$.
- **Explicit rejection.** Returning an error instead of $J(z \| c)$ opens a chosen ciphertext attack through decryption failures.
- **Bad randomness.** ML-KEM no longer hashes $m$; a weak random source for $m$ or $d$ breaks the key directly.
- **Old vectors.** The round 3 known answer tests do not match FIPS 203. Test with the ACVP vectors of FIPS 203.

## Implementations

The Python code on this page follows FIPS 203 algorithm by algorithm, with SHA-3 and SHAKE from hashlib. The tests compare against NIST ACVP vectors copied by hand: key generation tcIds 1, 26 and 51 (one per parameter set) and encapsulation tcId 1 of ML-KEM-512, with SHA-256 digests for the long values. They also check the sizes, the NTT, the compression bound, implicit rejection and the modulus check. The code is for study only: it is not constant time and must not be used to protect real data. Use a FIPS 140 validated module, or a reviewed library such as liboqs, BoringSSL or AWS-LC.

## History

Bos, Ducas, Kiltz, Lepoint, Lyubashevsky, Schanck, Schwabe, Seiler and Stehlé submitted CRYSTALS-Kyber to the NIST process in 2017 and published it at IEEE EuroS&P 2018. Round 2 (2019) changed the modulus from 7681 to 3329 and dropped the compression of the public key, and round 3 (2020 and 2021) set $\eta_1 = 3$ for Kyber512. In July 2022 NIST chose Kyber as the KEM to standardize (NIST IR 8413). The initial public draft of FIPS 203 appeared in August 2023 and the final standard on 13 August 2024. Browsers and TLS libraries deployed hybrid Kyber and then ML-KEM from 2023 on.

## References
