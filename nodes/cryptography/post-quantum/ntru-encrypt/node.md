---
tag: T0H5SG
kind: algorithm
slug: ntru-encrypt
name: NTRUEncrypt
aliases:
- NTRU cryptosystem
- NTRU-HPS
- NTRU-HRSS
area: cryptography/post-quantum
level: advanced
summary: "The 1998 encryption scheme of Hoffstein, Pipher and Silverman in Z[x]/(x^N - 1), with h = p g / f mod q, and its NIST round 3 KEM form (NTRU-HPS and NTRU-HRSS)."
model: word-ram
complexity:
  vars: {N: the ring degree}
  time: {worst: Θ(N^2), average: Θ(N^2), best: Θ(N^2)}
  space: {extra: Θ(N)}
properties: {deterministic: false, randomized: true}
history:
  year: 1998
  people: [Jeffrey Hoffstein, Jill Pipher, Joseph H. Silverman]
  note: Presented at the rump session of CRYPTO 1996 and published at ANTS-III in 1998. Standardized in IEEE 1363.1-2008. The NIST round 3 finalist NTRU merged NTRU-HPS and NTRU-HRSS and was not selected in 2022.
prereqs: [ntru-problem, polynomial-multiplication, modular-inverse, key-encapsulation-mechanism]
see_also: [ntru-prime, falcon, crystals-kyber, newhope, regev-encryption, lattice-based-cryptography, extended-euclidean-algorithm, nist-pqc-standardization]
sources:
  - paper: doi:10.1007/BFb0054868
    title: Jeffrey Hoffstein, Jill Pipher and Joseph H. Silverman, NTRU, a ring-based public key cryptosystem, ANTS-III, LNCS 1423, 1998, pages 267 to 288
    locator: "Section 1 (key creation, encryption and decryption), Section 2 (why decryption works and the decryption failures), Section 3 (the lattice attacks and the parameter sets)"
  - url: "https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization/round-3-submissions"
    title: Cong Chen, Oussama Danba, Jeffrey Hoffstein, Andreas Hülsing, Joost Rijneveld, John M. Schanck, Peter Schwabe, William Whyte, Zhenfei Zhang and others, NTRU, algorithm specifications and supporting documentation, NIST round 3 submission, 2020
    locator: "the OWCPA scheme and the KEM, the sample spaces (ternary and fixed type), the parameter sets ntruhps2048509, ntruhps2048677, ntruhps4096821 and ntruhrss701, and the package file KAT/ntruhps2048509/PQCkemKAT_935.rsp, count = 0 (copied in the tests)"
  - paper: "IEEE Std 1363.1-2008, IEEE standard specification for public key cryptographic techniques based on hard problems over lattices"
    title: IEEE 1363.1-2008
    locator: the NTRUEncrypt scheme with its encoding and padding (SVES)
  - paper: doi:10.6028/NIST.IR.8413-upd1
    title: NIST, IR 8413 (update 1), Status report on the third round of the NIST post-quantum cryptography standardization process, 2022
    locator: the section on NTRU (a finalist, and the reasons it was not selected)
---

NTRUEncrypt is a public key encryption scheme in the ring $\mathbb{Z}[x]/(x^N - 1)$, proposed by Hoffstein, Pipher and Silverman in 1996 and published in 1998. The secret key is a short polynomial $f$ and the public key is $h = p \cdot g \cdot f^{-1} \bmod q$ for another short $g$. To encrypt a short message $m$, one computes $e = r h + m \bmod q$ with a random short $r$. To decrypt, one multiplies by $f$: $f e = p r g + f m \pmod q$, and when $q$ is large enough the right side has small coefficients, so it is known exactly over the integers, and reducing it modulo $p$ leaves $f m$. NTRU was the first practical lattice-based scheme and is much older than [Regev encryption](/regev-encryption/); its hardness is the [NTRU problem](/ntru-problem/), the difficulty of finding $f, g$ from $h$. Its modern form, the NIST round 3 KEM NTRU (NTRU-HPS and NTRU-HRSS), is perfectly correct and was a finalist. This page is about the encryption scheme; the hardness question is on the NTRU problem page.

**Notation.** $R = \mathbb{Z}[x]/(x^N - 1)$, with the cyclic product $\circledast$ written as a plain product. $p$ is a small modulus (3 in practice) and $q$ a larger one (a power of two) with $\gcd(p, q) = 1$. A ternary polynomial has coefficients in $\{-1, 0, 1\}$. $\mathcal{L}(d_1, d_2)$ is the set of ternary polynomials with $d_1$ coefficients 1 and $d_2$ coefficients $-1$. $f_p$ and $f_q$ are inverses of $f$ in $R/pR$ and $R/qR$. "Centered mod $q$" means the representative in $(-q/2, q/2]$. In the KEM, $\Phi_1 = x - 1$ and $\Phi_N = 1 + x + \dots + x^{N-1}$, so $x^N - 1 = \Phi_1 \Phi_N$.

## In plain words

The owner picks two small random secret polynomials, f and g, and publishes h, which is g divided by f, with all numbers taken modulo q. Without f, h looks random.

To send a short message, the sender picks a small random polynomial r, multiplies it by h, and adds the message.

The owner multiplies the ciphertext by f. This cancels the division by f, so the result is a combination of small polynomials: r times g times p, plus f times the message. If q is large enough, no number wraps around modulo q, so the owner knows the result exactly. Modulo p the first part vanishes, and dividing by f gives the message.

## The problem

NTRUEncrypt solves the [public key encryption](/public-key-encryption/) problem for messages that are short polynomials. The 1998 scheme is one-way: given $h$ and $e$, it should be hard to find $m$. For IND-CCA security it needs a padding scheme (SVES in IEEE 1363.1) or, as in the NIST submission, a KEM built from a deterministic one-way scheme. The design must make decryption work: the integer polynomial $p r g + f m$ must have all coefficients in $(-q/2, q/2]$.

## The algorithm

```pseudo id=main
KEYGEN(N, p, q)                                        ▷ the 1998 scheme
L1  f ← random in L(d_f, d_f − 1);  g ← random in L(d_g, d_g)
L2  f_p ← f⁻¹ mod p;  f_q ← f⁻¹ mod q;  if either does not exist, go to L1
L3  h ← p · f_q · g  mod q
L4  return pk = h, sk = (f, f_p)

ENCRYPT(h, m)                                          ▷ m ternary (centered mod p)
L5  r ← random in L(d_r, d_r)
L6  return e ← r·h + m  mod q

DECRYPT((f, f_p), e)
L7  a ← f·e mod q, centered in (−q/2, q/2]             ▷ a = p·r·g + f·m over Z if no wrap
L8  return f_p·a mod p, centered

NTRU-HPS KEM KEYGEN                                    ▷ NIST round 3, ntruhps2048509
L9  f ← ternary;  g ← fixed type (q/16 − 1 ones and q/16 − 1 minus ones)
L10 h ← 3g / f in Z_q[x]/(x^N − 1);  h_q ← f / (3g) mod (q, Φ_N);  f_3 ← f⁻¹ mod (3, Φ_N)
L11 return pk = h, sk = (f, f_3, h_q, a PRF key z)
ENCAPS(h)
L12 r ← ternary;  m ← fixed type
L13 c ← r·h + m  mod q
L14 return c, K = SHA3-256(r ‖ m)
DECAPS(sk, c)
L15 a ← c·f mod q, centered;  m' ← a·f_3 mod (3, Φ_N)
L16 r' ← (c − m')·h_q mod (q, Φ_N)
L17 if r' is ternary and m' has fixed type, return SHA3-256(r' ‖ m'); else return SHA3-256(z ‖ c)
```

**Inverses.** Line L2 finds $f_p$ with the [extended Euclidean algorithm](/extended-euclidean-algorithm/) over $\mathbb{F}_p[x]$, applied to $f$ and $x^N - 1$. For $q = 2^k$, it first finds the inverse modulo 2 and then lifts it with Newton steps $b \leftarrow b (2 - f b)$, each of which doubles the number of correct binary digits. Many implementations pick $f = 1 + p F$ with a short $F$, so that $f_p = 1$ and line L8 needs no product.

**Why the KEM never fails.** In NTRU-HPS, $g$ and $m$ have exactly $q/8 - 2$ nonzero coefficients, and $r$ and $f$ are ternary. So each coefficient of $3 r g$ is at most $3(q/8 - 2)$ and each coefficient of $m f$ at most $q/8 - 2$ in absolute value, and their sum is below $q/2$. Decryption is then correct for every key and every message, which removes the attacks that use decryption failures. NTRU-HRSS gets the same with a different choice of $q$ and with $m$ lifted by $\Phi_1$.

**The KEM has no re-encryption.** Since the OWCPA scheme encrypts both $r$ and $m$, decapsulation recovers both and can check them directly (line L17), instead of encrypting again as the FO transform does.

**Parameter sets of round 3:**

| set | $N$ | $q$ | pk | sk | ct | category |
|---|---|---|---|---|---|---|
| ntruhps2048509 | 509 | 2048 | 699 | 935 | 699 | 1 |
| ntruhps2048677 | 677 | 2048 | 930 | 1234 | 930 | 3 |
| ntruhps4096821 | 821 | 4096 | 1230 | 1590 | 1230 | 5 |
| ntruhrss701 | 701 | 8192 | 1138 | 1450 | 1138 | 3 |

Sizes are in bytes. All sets have $p = 3$, and $N$ is a prime for which $\Phi_N$ is irreducible modulo 2 and 3.

## Example

**A toy decryption.** Take $N = 5$, $p = 3$, $q = 32$, $f = 1 + x - x^2$ and $g = x - x^3$ (here $f$ is invertible modulo 3 and 32 in $\mathbb{Z}[x]/(x^5 - 1)$). With $r = 1 - x^4$ and $m = -1 + x^2$, the integer polynomial $p r g + f m$ is $3(-1 + x + x^2 - x^3) + (-1 - x + 2x^2 + x^3 - x^4)$, where $x^5 = 1$ was used in both products. That is $-4 + 2x + 5x^2 - 2x^3 - x^4$. All coefficients are in $(-16, 16]$, so line L7 recovers this polynomial exactly. Modulo 3 it is $f m \bmod 3$, and line L8 multiplies by $f_3$ and returns $m = -1 + x^2$.

**When it fails.** The tests take $N = 11$, $p = 3$, $d_f = 4$, $d_g = d_r = 3$. Then each coefficient of $p r g + f m$ is at most $3 \cdot 6 + 7 = 25$ in absolute value, so $q = 256$ never fails, while $q = 32$ fails in some of 400 trials, because a coefficient wraps around modulo $q$.

**An official vector.** The round 3 package file `KAT/ntruhps2048509/PQCkemKAT_935.rsp`, count 0, gives the shared secret `176FDBB009DD3F848B365AB7F18D9C0C91721931C8594C2C6F043C8600791A6C`. The code on this page reproduces it from the DRBG seed of the file, together with the SHA-256 digests of the official pk, sk and ct.

## Correctness

Modulo $q$, $f e = f (p f_q g r + m) \equiv p r g + f m$, because $f f_q \equiv 1$. If every coefficient of the integer polynomial $p r g + f m$ lies in $(-q/2, q/2]$, centering in line L7 returns it exactly. Modulo $p$ it is $f m$, and $f_p f m \equiv m$; since $m$ is centered mod $p$, line L8 returns $m$. For NTRU-HPS the bound holds for all inputs, and the same argument, done modulo $\Phi_N$ for the inverses, shows that line L17 returns the key of line L14. The full proof is in the proof file.

## Complexity

The cost is a constant number of products in $R/qR$. With schoolbook multiplication each costs $\Theta(N^2)$; the reference code uses Toom-Cook and Karatsuba, and since one factor is ternary, products need no multiplications at all. Key generation also computes inverses, which cost $\Theta(N^2)$ with the extended Euclidean algorithm. The code on this page uses Kronecker substitution on Python integers, which is fast in practice. Keys and ciphertexts have $N$ coefficients of $\log_2 q$ bits, and the extra memory is $\Theta(N)$.

## Properties

- **Security.** Recovering the key is the NTRU problem: find a short vector $(f, g)$ in the lattice $\{(u, v) : v \equiv u h / p \pmod q\}$ of dimension $2N$. The best known attacks are lattice reduction (BKZ), the hybrid attack of Howgrave-Graham, and attacks on overstretched parameters with large $q$.
- **IND-CCA KEM.** The round 3 KEM is IND-CCA secure in the ROM and the QROM if the OWCPA scheme is one-way, with a tight reduction thanks to perfect correctness.
- **Fast.** Encryption and decryption are a few ring products with small factors; NTRU has always been among the fastest public key schemes.
- **Not an NTT ring.** $x^N - 1$ with prime $N$ and $q$ a power of two do not allow an NTT, so products use Toom-Cook and Karatsuba.

## Variants and improvements

- **IEEE 1363.1 (2008)** standardized NTRUEncrypt with the SVES padding for CCA security, and X9.98 did the same in finance.
- **NTRU-HRSS** (Hülsing, Rijneveld, Schanck and Schwabe, 2017) uses $q$ large enough for any ternary $g$ and $m$, with no fixed weight, and was used with X25519 in Google's CECPQ2 experiment in 2018 and 2019.
- **NTRU-HPS** is the line of the original authors with fixed-weight $g$ and $m$.
- **NTRU (round 3)** merged the two families in one submission; NIST did not select it in 2022.
- **NTRU Prime** changes the ring to $\mathbb{Z}_q[x]/(x^p - x - 1)$, see [NTRU Prime](/ntru-prime/).
- **NTRUSign** used the same lattice for signatures and was broken; [Falcon](/falcon/) uses the NTRU lattice safely with Gaussian sampling.

## When to use it

NTRU is mature and fast, its patents are no longer a barrier, and its KEM is perfectly correct. It is not a NIST standard, so new systems should prefer [ML-KEM](/crystals-kyber/). Use NTRU where it is already deployed, or in hybrid experiments. Use the 1998 scheme only to learn: without padding it is malleable and not CCA secure.

## Pitfalls

- **Decryption failures.** In the 1998 scheme a small $q$ makes some ciphertexts fail to decrypt, and an attacker who can see failures can recover $f$. Choose parameters where failures cannot happen, as in round 3.
- **No padding.** $e + x^i h$ is a valid ciphertext of a related message, so the raw scheme is malleable.
- **Wrong ring.** Products in $\mathbb{Z}[x]/(x^N - 1)$ are cyclic, not negacyclic; mixing them with $x^N + 1$ breaks decryption.
- **Timing.** The checks of line L17 and the sorting step of the fixed-type sampler must run in constant time.

## Implementations

The Python code on this page has two parts. The first is the 1998 scheme for any $(N, p, q)$, tested with $N = 107$, $p = 3$, $q = 64$, which this page takes to be the smallest set of the 1998 paper, and with a toy set that shows decryption failures. The second is the round 3 KEM ntruhps2048509 with the byte formats of the reference code. The tests run the NIST AES-256 CTR_DRBG and reproduce the official known answer vector `PQCkemKAT_935.rsp`, count 0: the shared secret against the copied value, and pk, sk and ct through SHA-256 digests of the official hex. They also check implicit rejection and the packing. NTRU-HRSS and the larger HPS sets are not implemented. The code is for study only: it is not constant time and must not be used to protect real data.

## History

Hoffstein, Pipher and Silverman presented NTRU at the rump session of CRYPTO 1996 and published it at ANTS-III in 1998. Coppersmith and Shamir (1997) noted the lattice attack, which set the parameter sizes. Howgrave-Graham, Nguyen, Pointcheval, Proos, Silverman, Singer and Whyte (2003) showed that decryption failures leak the key, which led to new parameters and padding. IEEE 1363.1 followed in 2008. Stehlé and Steinfeld (2011) gave a version with a proof from ring-LWE. For NIST, NTRUEncrypt and NTRU-HRSS-KEM were submitted in 2017 and merged in round 2; the merged NTRU was a finalist in round 3 and was not selected in July 2022.

## References
