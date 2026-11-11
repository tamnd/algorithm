---
tag: H257TC
kind: algorithm
slug: bike
name: BIKE
aliases:
- Bit Flipping Key Encapsulation
- QC-MDPC KEM
area: cryptography/post-quantum
level: advanced
summary: A code-based KEM on quasi-cyclic moderate-density parity-check codes, decoded by bit flipping. A NIST round 4 candidate; NIST selected HQC instead in March 2025.
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {r: the block length (a prime), d: "the weight of each secret block h0, h1", t: the error weight, I: the number of decoder iterations}
  time: {worst: O(r^2), average: O(r^2), best: O(r^2)}
  space: {extra: O(r)}
properties: {deterministic: false, randomized: true}
history:
  year: 2017
  people: [Nicolas Aragon, Paulo Barreto, Slim Bettaieb, Shay Gueron, Rafael Misoczki, Edoardo Persichetti, Nicolas Sendrier, Jean-Pierre Tillich, Valentin Vasseur, Gilles Zémor]
  note: BIKE was submitted to the NIST process in 2017 and reached round 4. It builds on QC-MDPC McEliece (Misoczki, Tillich, Sendrier and Barreto, 2013). NIST IR 8545 (March 2025) did not select it.
prereqs: [code-based-cryptography, ldpc-code, bit-flipping-decoding, key-encapsulation-mechanism]
see_also: [hqc, mceliece-cryptosystem, niederreiter-cryptosystem, fujisaki-okamoto-transform, syndrome-decoding-problem, information-set-decoding, shake]
sources:
  - url: "https://bikesuite.org/"
    title: "Nicolas Aragon, Paulo S. L. M. Barreto, Slim Bettaieb and others, BIKE: Bit Flipping Key Encapsulation, round 4 submission, specification version 5.1, October 2022"
    locator: the specification (the KEM, the BGF decoder with 5 iterations and the threshold rule, and the parameters r = 12323, w = 142, t = 134 for level 1)
  - paper: "Rafael Misoczki, Jean-Pierre Tillich, Nicolas Sendrier and Paulo S. L. M. Barreto, MDPC-McEliece: new McEliece variants from moderate density parity-check codes, IEEE ISIT 2013, pages 2069 to 2073"
    locator: the whole paper (QC-MDPC codes, the public key h1 / h0, and bit flipping decoding)
  - paper: "Nir Drucker, Shay Gueron and Dusan Kostic, QC-MDPC decoders with several shades of gray, PQCrypto 2020, LNCS 12100, pages 35 to 50"
    locator: the whole paper (the Black-Gray-Flip decoder and its failure rate)
  - paper: "Qian Guo, Thomas Johansson and Paul Stankovski, A key recovery attack on MDPC with CCA security using decoding errors, Asiacrypt 2016, LNCS 10031, pages 789 to 815"
    locator: the whole paper (the reaction attack, in which decoding failures depend on the distance spectrum of the secret key)
  - paper: "Nicolas Sendrier and Valentin Vasseur, On the decoding failure rate of QC-MDPC bit-flipping decoders, PQCrypto 2019, LNCS 11505, pages 404 to 416"
    locator: the whole paper (a model of the counters and of the failure rate of bit flipping)
  - paper: "Robert G. Gallager, Low-density parity-check codes, IRE Transactions on Information Theory 8(1), pages 21 to 28, 1962"
    locator: the whole paper (sparse parity check codes and bit flipping decoding)
  - url: "https://doi.org/10.6028/NIST.IR.8545"
    title: NIST IR 8545, Status Report on the Fourth Round of the NIST Post-Quantum Cryptography Standardization Process, March 2025
    locator: Section 3.1 and Section 3.2 (HQC is selected, BIKE is not, and the reasons), Table 8 (BIKE level 1 has an encapsulation key of 1541 bytes and a ciphertext of 1573 bytes)
  - paper: "Dennis Hofheinz, Kathrin Hövelmanns and Eike Kiltz, A modular analysis of the Fujisaki-Okamoto transformation, TCC 2017, LNCS 10677, pages 341 to 371"
    locator: the transforms with implicit rejection, and the correctness error that enters the bound
---

BIKE (Bit Flipping Key Encapsulation) is a code-based [KEM](/key-encapsulation-mechanism/). Its secret key is a sparse parity check matrix $H = (h_0 \mid h_1)$ made of two circulant blocks of size $r \times r$, each with $d$ ones per column: a quasi-cyclic moderate-density parity-check (QC-MDPC) code. The public key is the dense polynomial $h = h_1 h_0^{-1}$. A sender picks a sparse error $(e_0, e_1)$ of weight $t$ and sends $c_0 = e_0 + e_1 h$; the owner multiplies by $h_0$ to get the syndrome $e_0 h_0 + e_1 h_1$, and recovers the error with a bit flipping decoder. Keys and ciphertexts are small (about 1.5 KB at level 1), but the decoder sometimes fails, and its decoding failure rate (DFR) must be proved negligible for CCA security. BIKE reached round 4 of the NIST process, and in March 2025 NIST selected [HQC](/hqc/) instead (NIST IR 8545).

**Notation.** $\mathcal{R} = \mathbb{F}_2[x]/(x^r - 1)$ with $r$ prime and 2 primitive modulo $r$, so that $x^r - 1 = (x - 1)\Phi_r(x)$ with $\Phi_r$ irreducible. $h_0, h_1 \in \mathcal{R}$ have weight $d$ each (odd), so $w = 2d$ is the row weight of $H$. $(e_0, e_1) \in \mathcal{R}^2$ has total weight $t$, and $n = 2r$. $|s|$ is the [Hamming weight](/hamming-weight/) of $s$. $\mathbf{H}$, $\mathbf{L}$ and $\mathbf{K}$ are hash functions (modeled as random oracles), $\sigma$ a secret random string, $\lambda$ the security parameter, $\mathcal{A}$ an adversary and $\mathrm{Adv}$ its advantage. The DFR is the probability, over keys and messages, that decoding does not return the error. **Security model.** BIKE claims IND-CCA2 security as a KEM in the random oracle model, under the hardness of quasi-cyclic syndrome decoding and the indistinguishability of $h$ from random, provided that the DFR is at most $2^{-\lambda}$; this is where the analysis is weakest.

## In plain words

Each bit of the secret error takes part in $d$ parity checks. The receiver computes which checks fail. A bit that is wrong makes almost all of its checks fail, while a correct bit only sees a few failed checks by chance.

So the receiver counts, for each bit, how many of its checks fail, and flips every bit whose count is above a threshold. Then it computes the checks again and repeats. After a few rounds, all checks pass and the error is found.

Sometimes the counts mislead the decoder and it gives up. That rare event is a decoding failure, and an attacker who can see failures learns about the secret key.

## The problem

Key encapsulation: key generation outputs a public and a private key; encapsulation with the public key outputs a ciphertext and a shared key; decapsulation with the private key recovers the same shared key from the ciphertext. In BIKE this holds except with the probability of a decoding failure.

## The algorithm

```pseudo id=main
KEYGEN()
L1  h0, h1 ← random elements of R, each of odd weight d
L2  h ← h1 · h0⁻¹ in R;  σ ← a random 256-bit string
L3  return pk = h and sk = (h0, h1, σ)

ENCAPS(h)
L4  m ← a random 256-bit string
L5  (e0, e1) ← H(m)                         ▷ a vector of total weight t in R²
L6  c ← (c0, c1) = (e0 + e1·h, m ⊕ L(e0, e1))
L7  return c and K = K(m, c)

DECAPS(sk, c)
L8  e' ← BGF(c0·h0, h0, h1)                 ▷ c0·h0 = e0·h0 + e1·h1, the syndrome
L9  m' ← c1 ⊕ L(e')
L10 if e' = H(m') then return K(m', c) else return K(σ, c)
```

**The decoder.** Let $s$ be the current syndrome. The counter of a position $j$ is $\mathrm{ctr}_j = |s \wedge H_j|$, the number of unsatisfied parity checks that contain $j$, where $H_j$ is column $j$ of $H$. Bit flipping flips the positions with $\mathrm{ctr}_j \ge T$ and repeats. The Black-Gray-Flip (BGF) decoder of Drucker, Gueron and Kostic adds two masked steps in the first iteration: positions that were flipped (black) or that came close to the threshold (gray) get a second look with a fixed threshold $\lceil (d+1)/2 \rceil + 1$.

```pseudo id=bgf
BGF(s, h0, h1)
B1  e ← 0;  repeat I = 5 times:
B2    T ← threshold(|s + e·Hᵀ|)
B3    for each position j, counted on s + e·Hᵀ: if ctr_j ≥ T then flip e_j and mark j black; else if ctr_j ≥ T − τ then mark j gray
B4    in the first iteration only: for the black positions, then for the gray positions, recount and flip j if ctr_j ≥ (d + 1)/2 + 1
B5  if s = e·Hᵀ then return e else return failure
```

The specification uses $\tau = 3$ and a threshold that is an affine function of the syndrome weight, fitted for each security level (for level 1, $\max(\lfloor 0.0069722\,|s| + 13.530 \rfloor, 36)$). The implementation here computes the threshold for the toy parameters from the counter model of Sendrier and Vasseur: the smallest $T$ at which a counter value is more likely to come from an error position than from a correct position.

## Example

**Counters by hand.** Take $r = 7$, $h_0 = 1 + x + x^3$, $h_1 = 1 + x^2 + x^3$, and a single error $e = (x^2, 0)$. The syndrome is $s = x^2 h_0 = x^2 + x^3 + x^5$. For block 0, $\mathrm{ctr}_j = s_j + s_{j+1} + s_{j+3}$ (indices mod 7), which gives $(1, 1, 3, 1, 1, 1, 1)$ for $j = 0, \ldots, 6$. For block 1, $\mathrm{ctr}_j = s_j + s_{j+2} + s_{j+3}$, which gives $(2, 1, 2, 2, 0, 1, 1)$. Only position 2 of block 0 reaches $d = 3$, so a threshold of 3 flips exactly the error bit, and the new syndrome is 0.

**Toy parameters.** The tests use $r = 587$ (a prime with 2 primitive), $d = 15$ and $t = 18$. The public key and $c_0$ are 587 bits each. On 150 decodings with a fixed seed, BGF did not fail once. With $t = 24$ on 100 fixed instances, BGF failed 13 times and plain bit flipping with the same threshold and 5 iterations failed 24 times. So the DFR rises fast with $t$, and BGF helps.

**Real parameters.** Level 1 uses $r = 12323$, $w = 142$ (so $d = 71$) and $t = 134$. NIST IR 8545 (Table 8) lists an encapsulation key of 1541 bytes and a ciphertext of 1573 bytes; for level 5 the sizes are 5122 and 5154 bytes. Classic McEliece needs 261120 bytes for its smallest public key.

## Correctness

Since $h = h_1 h_0^{-1}$, the owner computes $c_0 h_0 = e_0 h_0 + e_1 h_1 = (e_0, e_1) H^T$, the syndrome of the error under the secret sparse matrix. If BGF returns $(e_0, e_1)$, then $m' = c_1 \oplus \mathbf{L}(e_0, e_1) = m$, the check $\mathbf{H}(m) = (e_0, e_1)$ passes, and DECAPS returns $\mathbf{K}(m, c) = K$. So decapsulation fails only when the decoder fails or returns another vector with the same syndrome, and the probability of this is the DFR. The proof file shows this, and also that the counters are the number of failed checks.

## Complexity

**Key generation.** Inversion in $\mathcal{R}$ by the extended Euclidean algorithm costs $O(r^2)$ bit operations ($O(r^2/w_{\mathrm{word}})$ word operations); the multiplication by the sparse $h_1$ costs $O(dr)$. The specification uses an inversion based on exponentiation that is constant time.

**Encapsulation.** Sampling the error and the product $e_1 h$ (sparse times dense) cost $O(tr)$ bit operations.

**Decapsulation.** Each decoder iteration computes all $2r$ counters in $O(dr)$ operations, so BGF costs $O(I d r)$ with $I = 5$ plus the masked steps. With $d \approx \sqrt{r}$ this is about $O(r^{3/2})$.

**Space.** $O(r)$ bits for keys, ciphertexts and counters.

## Properties

- **Small keys.** The public key is one element of $\mathcal{R}$, $r$ bits, because the code is quasi-cyclic.
- **Decoding failures.** Bit flipping is not a bounded distance decoder. The DFR must be at most $2^{-128}$ at level 1, which cannot be measured by simulation; it is extrapolated from models and from simulations with smaller $r$.
- **Ephemeral or static keys.** With a negligible DFR and the KEM transform, keys may be reused. With a measurable DFR, keys must be ephemeral, because of reaction attacks.
- **Two hard problems.** Security needs the quasi-cyclic syndrome decoding problem and the quasi-cyclic codeword finding problem (finding the sparse $(h_0, h_1)$ from $h$) to be hard. The best attacks are [information set decoding](/information-set-decoding/), with a gain from the quasi-cyclic structure that is polynomial in $r$ (about $\sqrt{r}$ for decoding, because each of the $r$ shifts of the target is a valid target).

## Variants and improvements

- **Decoders.** Gallager's bit flipping (1962), the step-by-step and parallel variants studied for QC-MDPC, and the BGF decoder (2020) with fewer iterations and a lower DFR. BIKE round 4 uses BGF with 5 iterations.
- **Earlier BIKE versions.** Rounds 1 and 2 had three variants (BIKE-1, BIKE-2, BIKE-3) with ephemeral keys; round 3 kept one variant with CCA security.
- **QC-MDPC McEliece.** The 2013 encryption scheme of Misoczki, Tillich, Sendrier and Barreto, which BIKE turns into a KEM.

## When to use it

BIKE is not a NIST standard: NIST IR 8545 selected HQC as the code-based backup KEM to ML-KEM, partly because the DFR analysis of HQC is more mature. Use BIKE only where a protocol already specifies it, and prefer a standardized KEM otherwise. Do not use the toy code of this page.

## Pitfalls

- **Reaction attacks.** Guo, Johansson and Stankovski (2016) observed that the failure probability of a ciphertext depends on the distances between its error positions. If the secret $h_0$ has two ones at distance $\delta$, errors with many pairs at distance $\delta$ fail less often. An attacker who sends many chosen ciphertexts and sees which ones fail learns the distance spectrum of $h_0$, and then rebuilds $h_0$. This recovered the keys of the QC-MDPC parameters of that time when the keys were static. The defenses are ephemeral keys or a DFR below $2^{-\lambda}$, together with the KEM transform. This page describes the attack but does not implement it.
- **Weak keys.** Some keys have a much higher DFR than the average, for example keys with special structure in $h_0$. The DFR claim must cover them.
- **Timing leaks.** Data-dependent iteration counts, early exits and variable time rotations leak the error or the key. Real implementations run a fixed number of iterations in constant time.
- **Assuming the decoder never fails.** Code that skips the check in line L10 or the implicit rejection opens chosen ciphertext attacks.

## Implementations

The Python code below is for study only. It is not constant time, it uses the random module, and the toy parameters give no security. Use a vetted implementation for real data, for example a FIPS 140 validated module that offers ML-KEM or a future HQC standard; libsodium has no code-based KEM. **This is not the full BIKE specification.** It has the BIKE round 4 structure (the key $h_1 h_0^{-1}$, the ciphertext $(e_0 + e_1 h, m \oplus \mathbf{L}(e))$, the BGF decoder and implicit rejection), but the parameters are toy size ($r = 587$, $d = 15$, $t = 18$), the hash functions, error sampling and encodings are simplified, and the threshold rule is computed from a model instead of the fitted rule. So the official BIKE KAT files do not apply, and there are no official test vectors for the toy parameters. The tests check the ring arithmetic against schoolbook multiplication, the counters against direct counting, the round trip, implicit rejection, and the failure counts above under fixed seeds.

## History

Gallager introduced low-density parity-check codes and bit flipping in 1962. Misoczki, Tillich, Sendrier and Barreto proposed QC-MDPC McEliece in 2013, with moderate density so that the dual code has no low-weight structure to find. Guo, Johansson and Stankovski showed the reaction attack in 2016. BIKE entered the NIST process in 2017, merged variants over the rounds, adopted the BGF decoder of Drucker, Gueron and Kostic (2020), and reached round 4 in 2022. In March 2025 NIST IR 8545 selected HQC and not BIKE.

## References
