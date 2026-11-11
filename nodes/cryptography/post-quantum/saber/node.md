---
tag: 0XW32T
kind: algorithm
slug: saber
name: SABER
aliases:
- SABER KEM
area: cryptography/post-quantum
level: advanced
summary: "A KEM built on module learning with rounding, with all moduli powers of two. It replaces random errors by rounding and needs no NTT. A NIST round 3 finalist that was not selected."
model: word-ram
complexity:
  vars: {l: the module rank (2 to 4), n: the polynomial degree (256)}
  time: {worst: Θ(l^2 n^1.58), average: Θ(l^2 n^1.58), best: Θ(l^2 n^1.58)}
  space: {extra: Θ(l^2 n)}
properties: {deterministic: false, randomized: true}
history:
  year: 2018
  people: [Jan-Pieter D'Anvers, Angshuman Karmakar, Sujoy Sinha Roy, Frederik Vercauteren]
  note: Published at AFRICACRYPT 2018 and submitted to the NIST process in 2017. A round 3 finalist; NIST did not select it in July 2022.
prereqs: [learning-with-rounding, module-learning-with-errors, key-encapsulation-mechanism, fujisaki-okamoto-transform]
see_also: [crystals-kyber, frodokem, newhope, regev-encryption, toom-cook-multiplication, karatsuba-multiplication, sha-3, nist-pqc-standardization]
sources:
  - paper: doi:10.1007/978-3-319-89339-6_16
    title: Jan-Pieter D'Anvers, Angshuman Karmakar, Sujoy Sinha Roy and Frederik Vercauteren, Saber, module-LWR based key exchange, CPA-secure encryption and CCA-secure KEM, AFRICACRYPT 2018, LNCS 10831, pages 282 to 305
    locator: the encryption with the constants h1 and h2, the analysis of the failure probability, and the use of Toom-Cook and Karatsuba
  - url: "https://www.esat.kuleuven.be/cosic/pqcrypto/saber/"
    title: The Saber team, SABER, Mod-LWR based KEM, NIST round 3 submission, 2020
    locator: "the algorithms Saber.PKE.KeyGen, Enc and Dec and Saber.KEM.KeyGen, Encaps and Decaps, and the parameter table of LightSaber, Saber and FireSaber"
  - url: "https://github.com/KULeuven-COSIC/SABER"
    title: The Saber team, reference implementation and known answer tests
    locator: "KAT/Saber/PQCkemKAT_2304.rsp, count = 0 (the seed, the shared secret and the digests of pk, sk and ct are copied in the tests)"
  - paper: doi:10.6028/NIST.IR.8413-upd1
    title: NIST, IR 8413 (update 1), Status report on the third round of the NIST post-quantum cryptography standardization process, 2022
    locator: the section on Saber (a finalist, compared with Kyber, and not selected)
---

SABER is a key encapsulation mechanism whose security rests on module [learning with rounding](/learning-with-rounding/) (MLWR). Where [Kyber](/crystals-kyber/) adds small random errors to hide $A^\mathsf{T} s$, Saber drops the low bits instead: the public key is $b = \lfloor (p/q) (A^\mathsf{T} s) \rceil$ with $q = 2^{13}$ and $p = 2^{10}$, and the deterministic rounding error plays the part of the noise. Because all moduli are powers of two, rounding is a shift, reduction is a mask, and there is no need for the NTT; multiplication uses [Toom-Cook](/toom-cook-multiplication/) and [Karatsuba](/karatsuba-multiplication/). A [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/) makes it IND-CCA secure. Saber was one of the four KEM finalists in round 3 of the NIST process, but NIST chose Kyber in 2022.

**Notation.** $R_q = \mathbb{Z}_q[x]/(x^{256}+1)$. The moduli are $q = 2^{\epsilon_q}$, $p = 2^{\epsilon_p}$ and $T = 2^{\epsilon_T}$, with $\epsilon_q = 13$, $\epsilon_p = 10$ and $\epsilon_T = 3$, 4 or 6. $A \in R_q^{l \times l}$ is generated from a seed with SHAKE128. The secrets $s, s' \in R^l$ have coefficients from the centered binomial distribution $\beta_\mu$ with values in $[-\mu/2, \mu/2]$. The constants $h_1 = 2^{\epsilon_q - \epsilon_p - 1}$ and $h_2 = 2^{\epsilon_p - 2} - 2^{\epsilon_p - \epsilon_T - 1} + 2^{\epsilon_q - \epsilon_p - 1}$ turn the floor of a shift into rounding and center the decryption window. $\gg$ is a right shift, $H$ is SHA3-256 and $G$ is SHA3-512. A message $m$ is 256 bits, one bit per coefficient.

## In plain words

Saber lets two parties agree on a secret key. The public key is a random table times a small secret, with the lowest digits of each number thrown away. Throwing away digits hides the secret in the same way that random noise would, and it costs nothing.

To send a key, the sender does the same with a fresh small secret and hides a random message in the top bit of some numbers, then keeps only a few top digits. The receiver, using the secret, gets almost the same numbers. The difference is small, so the receiver can read the top bit and get the message.

All numbers are reduced modulo powers of two, so every step is a shift or a mask. The receiver then checks the ciphertext by repeating the sender's work.

## The problem

Saber is a [key encapsulation mechanism](/key-encapsulation-mechanism/) with IND-CCA security. The underlying public key encryption must be IND-CPA secure, which reduces to the decision MLWR problem: $(A, \lfloor (p/q) A^\mathsf{T} s \rceil)$ is hard to tell from $(A, \text{uniform})$. Since no random errors are sampled, the design must check that the rounding errors are still small enough for decryption to succeed.

## The algorithm

```pseudo id=main
PKE.KEYGEN()
L1  seedA ← SHAKE128(32 random bytes, 32);  A ← GenMatrix(seedA)      ▷ l × l over R_q
L2  s ← β_μ(R^l) from a random seed
L3  b ← ((Aᵀ·s + h1) mod q) ≫ (ε_q − ε_p)                              ▷ in R_p^l
L4  return pk = (seedA, b), sk = s

PKE.ENC(pk, m, r)
L5  A ← GenMatrix(seedA);  s' ← β_μ(R^l) from the seed r
L6  b' ← ((A·s' + h1) mod q) ≫ (ε_q − ε_p)
L7  v' ← bᵀ·(s' mod p)  (mod p)
L8  c_m ← ((v' + h1 − 2^(ε_p − 1)·m) mod p) ≫ (ε_p − ε_T)              ▷ in R_T
L9  return ct = (c_m, b')

PKE.DEC(sk, ct)
L10 v ← b'ᵀ·(s mod p)  (mod p)
L11 m' ← ((v − 2^(ε_p − ε_T)·c_m + h2) mod p) ≫ (ε_p − 1)
L12 return m'

KEM.KEYGEN()
L13 (pk, s) ← PKE.KeyGen();  z ← 32 random bytes;  return pk, sk = (s, pk, H(pk), z)
KEM.ENCAPS(pk)
L14 m ← H(32 random bytes)
L15 (K̂, r) ← G(m ‖ H(pk))
L16 c ← PKE.Enc(pk, m, r)
L17 return c, K = H(K̂ ‖ H(c))
KEM.DECAPS(sk, c)
L18 m' ← PKE.Dec(s, c)
L19 (K̂', r') ← G(m' ‖ H(pk))
L20 c' ← PKE.Enc(pk, m', r')
L21 if c = c' return H(K̂' ‖ H(c)) else return H(z ‖ H(c))            ▷ implicit rejection
```

**Rounding instead of errors.** Line L3 computes $A^\mathsf{T} s$ exactly modulo $q$ and keeps the top 10 of 13 bits; adding $h_1 = 4$ first turns the floor into rounding to the nearest. The secret enters only through $A^\mathsf{T} s$, and the rounding loses 3 bits per coefficient. Line L8 keeps only $\epsilon_T$ bits of $v'$, after the message bit is placed at the top position $2^{\epsilon_p - 1}$. Line L11 removes $c_m$ and reads the top bit, with $h_2$ chosen to put the expected value in the middle of the decision window.

**Multiplication.** $q$ is a power of two, so $x^{256} + 1$ does not split into linear factors and there is no NTT. The reference code multiplies with Toom-Cook 4-way down to degree 64, then Karatsuba down to degree 16, then schoolbook. Since the secret polynomials are small, one product with $A$ fits in 16-bit words.

**Parameter sets** (round 3 specification):

| set | $l$ | $\mu$ | $T$ | pk | sk | ct | category |
|---|---|---|---|---|---|---|---|
| LightSaber | 2 | 10 | $2^3$ | 672 | 1568 | 736 | 1 |
| Saber | 3 | 8 | $2^4$ | 992 | 2304 | 1088 | 3 |
| FireSaber | 4 | 6 | $2^6$ | 1312 | 3040 | 1472 | 5 |

Sizes are in bytes. All sets have $n = 256$, $q = 2^{13}$ and $p = 2^{10}$, so $h_1 = 4$; for Saber, $h_2 = 256 - 32 + 4 = 228$.

## Example

**Rounding a coefficient.** With $q = 8192$ and $p = 1024$, line L3 maps a coefficient $x$ of $A^\mathsf{T} s$ to $(x + 4) \gg 3$, which is $x/8$ rounded to the nearest integer. The coefficient 5003 ($5003/8 = 625.375$) gives $5007 \gg 3 = 625$, and 5005 ($5005/8 = 625.625$) gives $5009 \gg 3 = 626$.

**Hiding one bit.** Take Saber ($\epsilon_T = 4$) and a coefficient $v' = 700$ of line L7. For the bit $m = 1$, line L8 gives $c_m = (700 + 4 - 512) \gg 6 = 192 \gg 6 = 3$. Suppose that the receiver's $v$ differs by 10, so $v = 710$. Line L11 computes $(710 - 3 \cdot 64 + 228) \bmod 1024 = 746$, and $746 \gg 9 = 1$. For the bit $m = 0$, $c_m = 704 \gg 6 = 11$, and line L11 computes $(710 - 704 + 228) = 234$, and $234 \gg 9 = 0$.

**An official vector.** The known answer file `PQCkemKAT_2304.rsp` of the reference package, count 0, gives the shared secret `156533536C8435F82CC36FC1EF9528DEDC49223DDA0091617DC1ACAF6058D1CA`. The code on this page reproduces it from the DRBG seed of the file, together with the SHA-256 digests of the official pk, sk and ct.

## Correctness

Let $e_1 = (A^\mathsf{T} s + h_1 \bmod q) - 8 b$ and $e_2 = (A s' + h_1 \bmod q) - 8 b'$ be the rounding errors of lines L3 and L6, with coefficients in $[0, 7]$. Then modulo $q$,
$$8 v - 8 v' \equiv (A s' + h_1 - e_2)^\mathsf{T} s - (A^\mathsf{T} s + h_1 - e_1)^\mathsf{T} s' = (h_1 - e_2)^\mathsf{T} s - (h_1 - e_1)^\mathsf{T} s',$$
because $s'^\mathsf{T} A^\mathsf{T} s = s^\mathsf{T} A s'$ in the commutative ring. So $v - v' \equiv \delta \pmod p$ for a small polynomial $\delta$. Line L11 then sees $2^9 m + 2^8 + \delta + e_3 - 32$, where $e_3 \in [0, 63]$ is the rounding error of line L8, and returns $m$ when every coefficient of $\delta$ is at most 224 in absolute value. The FO part then works as in Kyber. The full proof is in the proof file. The round 3 specification gives failure rates of about $2^{-120}$, $2^{-136}$ and $2^{-165}$ for the three sets.

## Complexity

The work is in the $l^2$ products of line L3 or L6 and the $l$ products of lines L7 and L10, each a product in $\mathbb{Z}[x]/(x^{256}+1)$. With Karatsuba alone, one product costs $\Theta(n^{\log_2 3}) \approx \Theta(n^{1.58})$, which is the figure in the complexity field; Toom-Cook 4-way alone would give $\Theta(n^{\log_4 7}) \approx \Theta(n^{1.40})$, and the reference code mixes the two. The total is $\Theta(l^2)$ products, plus SHAKE128 for $A$. Decapsulation adds one re-encryption. The extra memory is $\Theta(l^2 n)$ for $A$, or $\Theta(l n)$ if $A$ is made one entry at a time.

## Properties

- **IND-CCA security.** Saber.PKE is IND-CPA secure if MLWR is hard, and the FO transform with implicit rejection gives IND-CCA in the ROM and the QROM.
- **No error sampling for the public parts.** Only the secrets are sampled. This saves randomness and makes masking against side channels cheaper than for schemes with sampled errors.
- **Power-of-two moduli.** Reduction is free, and the same multiplier works for any $q$, but there is no NTT, so the products cost more than in Kyber on many processors.
- **Compact keys.** The rounding to $p$ and $T$ compresses keys and ciphertexts by design. Saber's public key has 992 bytes against 1184 for Kyber-768, and the ciphertexts have the same size, 1088 bytes.

## Variants and improvements

- **LightSaber and FireSaber** are the sets for categories 1 and 5.
- **uSaber** uses a uniform secret distribution instead of the binomial one, which makes masking simpler.
- **Scabbard** (2021) is a family of variants with other rings, including Florete, Espada and Sable, by some of the same authors.

## When to use it

Saber is not a standard, so for new systems use [ML-KEM](/crystals-kyber/). Saber is of interest when you study learning with rounding, when the hardware has a fast generic multiplier but no NTT support, or when masking against power analysis is the main cost, since only the secrets are random.

## Pitfalls

- **Timing in decapsulation.** The comparison of line L21 and the selection of the key must run in constant time, or decapsulation becomes an oracle that leaks the secret key.
- **Wrong rounding constant.** Leaving out $h_1$ or $h_2$ changes floors into the wrong rounding and raises the failure rate by many orders of magnitude.
- **Treating rounding as random noise.** The rounding error is a deterministic function of $A^\mathsf{T} s$, so proofs and attacks for LWE do not carry over without the LWR reductions.

## Implementations

The Python code on this page implements Saber (the middle set) of round 3, with the byte layout of the reference code. The tests run the NIST AES-256 CTR_DRBG and reproduce the official known answer vector `PQCkemKAT_2304.rsp`, count 0: the shared secret is compared with the value copied from the file, and pk, sk and ct are compared through SHA-256 digests of the official hex. They also test implicit rejection, PKE round trips, and the Karatsuba product. The code uses Karatsuba alone instead of Toom-Cook 4-way plus Karatsuba; the products are the same. The code is for study only: it is not constant time and must not be used to protect real data.

## History

Banerjee, Peikert and Rosen (2012) introduced learning with rounding to build pseudorandom functions, and Alwen and others (2013) and Bogdanov and others (2016) gave reductions from LWE. D'Anvers, Karmakar, Roy and Vercauteren built Saber on module LWR, submitted it to NIST in 2017 and published it at AFRICACRYPT 2018. It became a finalist in July 2020. In July 2022 NIST selected Kyber and noted, in IR 8413, that Saber and Kyber were close, with Kyber preferred.

## References
