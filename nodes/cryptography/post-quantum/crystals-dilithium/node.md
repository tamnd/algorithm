---
tag: 1PTKAJ
kind: algorithm
slug: crystals-dilithium
name: CRYSTALS-Dilithium
aliases:
- Dilithium
- ML-DSA
- FIPS 204
area: cryptography/post-quantum
level: advanced
summary: "The module-lattice signature that NIST standardized as ML-DSA (FIPS 204, 2024). Fiat-Shamir with aborts over Z_8380417[X]/(X^256 + 1), with hints that shrink the public key."
model: word-ram
complexity:
  vars: {k: the rows of the matrix A, l: the columns of A, n: the polynomial degree (256)}
  time: {worst: ∞, average: Θ(k l n + (k + l) n log n), best: Θ(k l n + (k + l) n log n)}
  space: {extra: Θ(k l n)}
properties: {deterministic: false, randomized: true}
history:
  year: 2018
  people: [Léo Ducas, Eike Kiltz, Tancrède Lepoint, Vadim Lyubashevsky, Peter Schwabe, Gregor Seiler, Damien Stehlé]
  note: Submitted to the NIST process in 2017 and published in TCHES 2018, issue 1. NIST selected it in July 2022 and published it as ML-DSA in FIPS 204 in August 2024.
prereqs: [fiat-shamir-with-aborts, module-learning-with-errors, module-short-integer-solution, digital-signature]
see_also: [crystals-kyber, falcon, fiat-shamir-heuristic, quantum-random-oracle-model, strong-unforgeability, schnorr-signature, number-theoretic-transform, nist-pqc-standardization]
sources:
  - paper: doi:10.13154/tches.v2018.i1.238-268
    title: Léo Ducas, Eike Kiltz, Tancrède Lepoint, Vadim Lyubashevsky, Peter Schwabe, Gregor Seiler and Damien Stehlé, CRYSTALS-Dilithium, a lattice-based digital signature scheme, IACR TCHES 2018(1), pages 238 to 268
    locator: the signature with HighBits, LowBits and hints, the rejection conditions, the security sketch under MLWE and SelfTargetMSIS, and the parameter choice
  - paper: doi:10.6028/NIST.FIPS.204
    title: NIST, FIPS 204, Module-Lattice-Based Digital Signature Standard, August 2024
    locator: "Algorithms 1 to 3 (ML-DSA.KeyGen, Sign and Verify with a context string), Algorithms 6 to 8 (the internal functions), Section 7.4 (Power2Round, Decompose, HighBits, LowBits, MakeHint and UseHint), Tables 1 and 2 (parameter sets and sizes)"
  - url: "https://github.com/usnistgov/ACVP-Server/tree/master/gen-val/json-files"
    title: NIST, ACVP-Server, the files ML-DSA-keyGen-FIPS204 and ML-DSA-sigGen-FIPS204
    locator: "keyGen tcIds 1, 26 and 51, and sigGen test group 1 (ML-DSA-44, deterministic, external, pure), tcId 7 (copied in the tests)"
  - paper: doi:10.1007/978-3-319-78372-7_18
    title: Eike Kiltz, Vadim Lyubashevsky and Christian Schaffner, A concrete treatment of Fiat-Shamir signatures in the quantum random-oracle model, EUROCRYPT 2018, LNCS 10822, pages 552 to 586
    locator: the security of Fiat-Shamir with aborts signatures in the QROM under MLWE and SelfTargetMSIS, and the Dilithium instance
  - paper: doi:10.1007/978-3-031-38554-4_11
    title: Julien Devevey, Pouria Fallahpour, Alain Passelègue and Damien Stehlé, A detailed analysis of Fiat-Shamir with aborts, CRYPTO 2023, LNCS 14085, pages 327 to 357
    locator: the gap in earlier proofs about the aborted transcripts, and corrected bounds in the ROM and the QROM
  - paper: doi:10.1007/978-3-642-29011-4_43
    title: Vadim Lyubashevsky, Lattice signatures without trapdoors, EUROCRYPT 2012, LNCS 7237, pages 738 to 755
    locator: the rejection sampling signature that Dilithium follows
---

CRYSTALS-Dilithium is a digital signature scheme over module lattices, standardized by NIST in August 2024 as ML-DSA in FIPS 204. It follows the [Fiat-Shamir with aborts](/fiat-shamir-with-aborts/) pattern of Lyubashevsky: the signer commits to $w = A y$ for a random mask $y$, hashes the high part of $w$ with the message into a sparse challenge $c$, and answers $z = y + c s_1$, but restarts whenever $z$ or a low part of $w - c s_2$ could reveal the secret. Two ideas make it compact: only the high bits of $w$ enter the hash, and the public key keeps only the high bits of $t = A s_1 + s_2$, with the signer sending a short hint to fix the rounding. All arithmetic is in $R_q = \mathbb{Z}_q[X]/(X^{256}+1)$ with $q = 8380417$ and uses the [NTT](/number-theoretic-transform/). The scheme is [strongly unforgeable](/strong-unforgeability/) under module-LWE and module-SIS type assumptions, with proofs in the [quantum random oracle model](/quantum-random-oracle-model/).

**Notation.** $R_q$ as above, $q = 8380417 = 2^{23} - 2^{13} + 1$, $n = 256$, $d = 13$. $A \in R_q^{k \times l}$, $s_1 \in R_q^l$ and $s_2 \in R_q^k$ have coefficients in $[-\eta, \eta]$. $c$ has $\tau$ coefficients in $\{-1, 1\}$ and the rest 0, so $\beta = \tau \eta$ bounds $\|c s_i\|_\infty$. $\|\cdot\|_\infty$ is the largest coefficient in absolute value after centering mod $q$. $H(x, \ell)$ is SHAKE256 with $\ell$ bytes of output. $\mathrm{Decompose}$ writes $r = r_1 \cdot 2\gamma_2 + r_0$ with $r_0$ centered; HighBits returns $r_1$ and LowBits returns $r_0$. $\mathrm{Power2Round}$ does the same with $2^d$. $\mathrm{MakeHint}(z, r)$ is 1 when adding $z$ to $r$ changes its high bits, and $\mathrm{UseHint}(h, r)$ uses that bit to recover $\mathrm{HighBits}(r + z)$ from $r$.

## In plain words

The signer has a short secret and a public key computed from it with noise. To sign, the signer picks a large random mask, computes a commitment from it, and hashes the commitment with the message to get a small challenge. The answer is the mask plus the challenge times the secret. A verifier can check the answer with the public key only.

The answer must not show the secret. The mask hides it only when the answer lands in a safe middle range, so the signer throws away answers near the edge and tries again with a new mask. On average this takes four to five tries.

To keep keys and signatures short, only the top digits of some numbers are kept. The signer sends a few hint bits so that the verifier rounds in the same way.

## The problem

ML-DSA solves the [digital signature](/digital-signature/) problem: KeyGen outputs $(pk, sk)$, Sign$(sk, M)$ outputs $\sigma$, and Verify$(pk, M, \sigma)$ accepts honest signatures. The goal is strong unforgeability under chosen message attack: after seeing signatures on messages of its choice, no efficient adversary can output a valid pair $(M, \sigma)$ that it was not given. The assumptions are module-LWE (the key looks random), module-SIS, and SelfTargetMSIS, a module-SIS problem with a hash in the equation.

## The algorithm

```pseudo id=main
KEYGEN_INTERNAL(ξ)                                    ▷ FIPS 204 Algorithm 6
L1  (ρ, ρ', K) ← H(ξ ‖ k ‖ l, 128)                    ▷ 32, 64 and 32 bytes
L2  Â ← ExpandA(ρ);  (s1, s2) ← ExpandS(ρ')
L3  t ← NTT⁻¹(Â ∘ NTT(s1)) + s2
L4  (t1, t0) ← Power2Round(t)                         ▷ t = t1·2^d + t0
L5  pk ← pkEncode(ρ, t1);  tr ← H(pk, 64)
L6  return pk, sk = skEncode(ρ, K, tr, s1, s2, t0)

SIGN_INTERNAL(sk, M', rnd)                            ▷ Algorithm 7
L7  μ ← H(tr ‖ M', 64);  ρ'' ← H(K ‖ rnd ‖ μ, 64);  κ ← 0
L8  loop
L9      y ← ExpandMask(ρ'', κ);  κ ← κ + l            ▷ coefficients in (−γ1, γ1]
L10     w ← NTT⁻¹(Â ∘ NTT(y));  w1 ← HighBits(w)
L11     c̃ ← H(μ ‖ w1Encode(w1), λ/4);  c ← SampleInBall(c̃)
L12     z ← y + c·s1;  r0 ← LowBits(w − c·s2)
L13     if ‖z‖∞ ≥ γ1 − β or ‖r0‖∞ ≥ γ2 − β then continue    ▷ reject
L14     h ← MakeHint(−c·t0, w − c·s2 + c·t0)
L15     if ‖c·t0‖∞ ≥ γ2 or h has more than ω ones then continue
L16     return σ = sigEncode(c̃, z, h)

VERIFY_INTERNAL(pk, M', σ)                            ▷ Algorithm 8
L17 (ρ, t1) ← pkDecode(pk);  (c̃, z, h) ← sigDecode(σ);  if h is malformed return false
L18 if ‖z‖∞ ≥ γ1 − β return false
L19 μ ← H(H(pk, 64) ‖ M', 64);  c ← SampleInBall(c̃)
L20 w'approx ← NTT⁻¹(Â ∘ NTT(z) − NTT(c) ∘ NTT(t1·2^d))
L21 w1' ← UseHint(h, w'approx)
L22 return c̃ = H(μ ‖ w1Encode(w1'), λ/4)

ML-DSA.KEYGEN()                                       ▷ Algorithm 1
L23 ξ ← 32 fresh random bytes;  return KeyGen_internal(ξ)
ML-DSA.SIGN(sk, M, ctx)                               ▷ Algorithm 2, |ctx| ≤ 255
L24 M' ← 0 ‖ |ctx| ‖ ctx ‖ M;  rnd ← 32 fresh random bytes (hedged) or 0^32 (deterministic)
    return Sign_internal(sk, M', rnd)
ML-DSA.VERIFY(pk, M, σ, ctx)                          ▷ Algorithm 3
L25 M' ← 0 ‖ |ctx| ‖ ctx ‖ M;  return Verify_internal(pk, M', σ)
```

**The rejection conditions.** Line L13 is the abort of Fiat-Shamir with aborts. The mask $y$ is uniform in a box of half-width $\gamma_1$, and $c s_1$ moves it by at most $\beta$. Keeping only the $z$ inside the smaller box of half-width $\gamma_1 - \beta$ makes $z$ uniform there whatever $s_1$ is (see the technique page). The second test of line L13 makes sure that $w - c s_2$ and $w$ have the same high bits, which the verifier needs, and that the low bits leak nothing on $s_2$. Line L15 makes the hint valid and short. FIPS 204, Table 1, gives the expected number of iterations of the loop as 4.25, 5.1 and 3.85 for the three sets.

**Rounding and hints.** Power2Round splits $t$ at $2^{13}$; only $t_1$ is public, which shrinks the public key by almost half. The verifier can compute $A z - c t_1 2^d = w - c s_2 + c t_0$, which differs from what the signer rounded by the unknown $c t_0$. MakeHint records, coefficient by coefficient, whether adding $-c t_0$ moves the value into a neighbouring band of width $2\gamma_2$, and UseHint moves the high bits up or down by one band to match.

**Hedged and deterministic signing.** With a fresh $rnd$ (the default, called hedged), two signatures of the same message differ, and a fault or a weak random source does not leak the key at once. With $rnd = 0^{32}$ the scheme is deterministic. Both verify the same way. FIPS 204 also defines HashML-DSA (Algorithms 4 and 5), which signs a hash of the message with an OID in $M'$; the code here does not implement it.

**Parameter sets** (FIPS 204, Tables 1 and 2):

| set | $(k, l)$ | $\eta$ | $\tau$ | $\lambda$ | $\gamma_1$ | $\gamma_2$ | $\omega$ | $pk$ | $sk$ | $\sigma$ | category |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ML-DSA-44 | (4, 4) | 2 | 39 | 128 | $2^{17}$ | $(q-1)/88$ | 80 | 1312 | 2560 | 2420 | 2 |
| ML-DSA-65 | (6, 5) | 4 | 49 | 192 | $2^{19}$ | $(q-1)/32$ | 55 | 1952 | 4032 | 3309 | 3 |
| ML-DSA-87 | (8, 7) | 2 | 60 | 256 | $2^{19}$ | $(q-1)/32$ | 75 | 2592 | 4896 | 4627 | 5 |

Sizes are in bytes. $\beta = \tau\eta$ is 78, 196 and 120.

## Example

**Rounding.** For ML-DSA-44, $2\gamma_2 = 190464$. Decompose$(1000000)$ gives $r_1 = 5$ and $r_0 = 47680$, because $1000000 = 5 \cdot 190464 + 47680$. Power2Round$(1000000)$ gives $(122, 576)$, because $1000000 = 122 \cdot 8192 + 576$. The top value $q - 1$ is a special case: Decompose returns $r_1 = 0$ and $r_0 = -1$, so that $r_1$ stays in $[0, 43]$.

**A hint.** Take $r = 860000$, which decomposes as $(5, -92320)$, and $z = -5000$. Then $r + z = 855000$ decomposes as $(4, 93144)$: the high bits changed, so MakeHint$(z, r) = 1$. UseHint$(1, r)$ sees $r_0 \le 0$ and returns $r_1 - 1 = 4$, the high bits of $r + z$.

**An official vector.** ACVP ML-DSA-sigGen-FIPS204, test group 1 (ML-DSA-44, deterministic, external interface, pure), tcId 7 signs the one-byte message `C9` with a context string of 103 bytes. The expected signature of 2420 bytes has SHA-256 `1623f70687f1e8592435757c00488e73631c4ead662fd9a4dc51fe971f5b0b86`, which the code on this page reproduces, together with the key generation vectors tcId 1, 26 and 51.

## Correctness

Let $\sigma = (\tilde c, z, h)$ come from line L16. The verifier computes $A z - c t_1 2^d = A y + c A s_1 - c (A s_1 + s_2 - t_0) = w - c s_2 + c t_0$. Since $\|c t_0\|_\infty < \gamma_2$, UseHint with the hint of line L14 returns HighBits$(w - c s_2)$. Since $\|c s_2\|_\infty \le \beta$ and $\|\mathrm{LowBits}(w - c s_2)\|_\infty < \gamma_2 - \beta$, adding $c s_2$ back does not cross a band border, so HighBits$(w - c s_2) = w_1$. The verifier hashes the same $\mu$ and $w_1$, gets $\tilde c$, and the norm test passes because of line L13. The full proof, with the band argument for UseHint, is in the proof file.

## Complexity

One loop iteration costs $l$ forward NTTs for $y$, $k$ inverse NTTs for $w$, products in the NTT domain, and the sampling of $\hat{A}$ once per signature ($k l$ polynomials from SHAKE128). That is $\Theta(k l n + (k + l) n \log n)$ per iteration, and the loop runs about 4 to 5 times on average. The number of iterations has a geometric distribution, so it has no fixed upper bound; FIPS 204 lets an implementation stop after a large limit. Verification costs one iteration without rejection. Keys and signatures have $\Theta((k + l) n)$ coefficients. The extra memory is $\Theta(k l n)$ for $\hat{A}$, or less if it is sampled on the fly.

## Properties

- **SUF-CMA in the QROM.** Kiltz, Lyubashevsky and Schaffner (2018) prove that Fiat-Shamir with aborts signatures are secure in the quantum random oracle model if MLWE and SelfTargetMSIS are hard, and add MSIS for strong unforgeability. Devevey, Fallahpour, Passelègue and Stehlé (2023) and Barbosa and others (2023) found a gap about the aborted iterations in earlier proofs and gave corrected bounds; the gap does not lead to an attack on the parameters.
- **Uniform rejection.** Dilithium uses uniform masks and a box test, not Gaussians, so the signer needs no Gaussian sampler and is easier to make constant time than [Falcon](/falcon/).
- **Public key compression.** The public key holds $t_1$ only, and the hint $h$ lets the verifier work without $t_0$. The secret key holds $t_0$.
- **Context strings.** The external functions bind a context string of up to 255 bytes into $M'$, which separates uses of one key in different protocols.
- **Medium sizes.** Signatures are about 2.4 to 4.6 kB, larger than Falcon but with simpler signing.

## Variants and improvements

- **Round 3 Dilithium** (2021) hashed $\mu$ with a 48-byte $tr$, had a 32-byte challenge seed at every level, and had no context string. FIPS 204 changed these, so round 3 known answer files do not match ML-DSA.
- **HashML-DSA** signs a pre-hash such as SHA-512 of the message, for messages that do not fit in memory.
- **Bai-Galbraith compression** (2014) is the source of the idea of dropping the low bits of $t$; Dilithium adds the hints.
- **Gaussian Fiat-Shamir with aborts**, as in BLISS (2013), uses Gaussian masks and bimodal rejection for smaller signatures, at the cost of a Gaussian sampler with a history of side-channel attacks.

## When to use it

Use ML-DSA as the default post-quantum signature: it is a NIST standard, it is fast for both signing and verification, and it is simple to implement in constant time. Use ML-DSA-65 for most systems. Prefer [Falcon](/falcon/) (FN-DSA) only when signature size is critical and you can trust a careful floating-point implementation, and SLH-DSA when you want hash-based assumptions only.

## Pitfalls

- **Leaking rejected iterations.** The values of rejected iterations, and which condition rejected them, must not leak through timing; some leak bits of the secret.
- **Bad hint encoding.** Verify must reject a hint with more than $\omega$ ones or with indices out of order, or signatures become malleable and strong unforgeability fails.
- **Mixing round 3 and FIPS 204.** The hashing of $\mu$ and the context byte changed, so keys and test vectors of the two do not interoperate.
- **Deterministic signing on faulty hardware.** A fault in one of two deterministic signatures of the same message can leak the key; hedged signing reduces this risk.
- **Bounding the loop too low.** A low iteration limit makes some messages fail to sign.

## Implementations

The Python code on this page follows FIPS 204 with SHAKE from hashlib. The tests compare against NIST ACVP vectors copied by hand: key generation tcIds 1, 26 and 51 and the deterministic signature of sigGen tcId 7 for ML-DSA-44, with SHA-256 digests for the long values. They also check forgeries, the hedged mode, the rounding identities and the hints. The code is for study only: it is not constant time and must not be used to protect real data. Use a FIPS 140 validated module, or a reviewed library such as liboqs, BoringSSL or AWS-LC.

## History

Lyubashevsky introduced Fiat-Shamir with aborts in 2009 and the lattice signature without trapdoors in 2012. Güneysu, Lyubashevsky and Pöppelmann (2012) made it practical over rings, and Bai and Galbraith (2014) dropped the low bits of the public key. Ducas, Kiltz, Lepoint, Lyubashevsky, Schwabe, Seiler and Stehlé combined these ideas over module lattices in CRYSTALS-Dilithium, submitted to NIST in 2017 and published in TCHES in 2018. NIST selected it in July 2022, released the draft of FIPS 204 in August 2023, and published the final standard on 13 August 2024.

## References
