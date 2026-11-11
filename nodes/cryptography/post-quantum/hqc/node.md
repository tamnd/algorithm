---
tag: E4EFXK
kind: algorithm
slug: hqc
name: HQC
aliases:
- Hamming Quasi-Cyclic
- HQC-KEM
area: cryptography/post-quantum
level: advanced
summary: A code-based KEM on random quasi-cyclic codes, with a public concatenated Reed-Muller and Reed-Solomon code for decoding. NIST selected it in March 2025 as a backup to ML-KEM.
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {n: the length of the ring (a prime), w: "the weight of the sparse vectors (w, wr and we are all of this order)", n1: the Reed-Solomon length in bytes, n2: the length of the repeated Reed-Muller code in bits}
  time: {worst: O(n w + n1^2 + n1 n2 log n2), average: O(n w + n1^2 + n1 n2 log n2), best: O(n w + n1^2 + n1 n2 log n2)}
  space: {extra: O(n)}
properties: {deterministic: false, randomized: true}
history:
  year: 2017
  people: [Carlos Aguilar Melchor, Nicolas Aragon, Slim Bettaieb, Loïc Bidoux, Olivier Blazy, Jean-Christophe Deneuville, Philippe Gaborit, Edoardo Persichetti, Gilles Zémor]
  note: HQC was submitted to the NIST process in 2017, based on the scheme of Aguilar Melchor, Blazy, Deneuville, Gaborit and Zémor. NIST selected it for standardization in March 2025 (NIST IR 8545).
prereqs: [code-based-cryptography, reed-solomon-code, reed-muller-code, key-encapsulation-mechanism, fujisaki-okamoto-transform]
see_also: [bike, mceliece-cryptosystem, syndrome-decoding-problem, information-set-decoding, fast-walsh-hadamard-transform, learning-with-errors, crystals-kyber, shake]
sources:
  - url: "https://pqc-hqc.org/"
    title: "Carlos Aguilar Melchor, Nicolas Aragon, Slim Bettaieb and others, HQC: Hamming Quasi-Cyclic, specification, version of 22 August 2025"
    locator: the specification (the PKE, the KEM with the salt and implicit rejection, and HQC-1 with n = 17669, n1 = 46, n2 = 384, w = 66, wr = we = 75)
  - paper: "Carlos Aguilar Melchor, Olivier Blazy, Jean-Christophe Deneuville, Philippe Gaborit and Gilles Zémor, Efficient encryption from random quasi-cyclic codes, IEEE Transactions on Information Theory 64(5), pages 3927 to 3943, 2018"
    locator: the whole paper (the HQC framework, its IND-CPA proof under quasi-cyclic syndrome decoding, and the analysis of the decryption failure rate)
  - url: "https://doi.org/10.6028/NIST.IR.8545"
    title: NIST IR 8545, Status Report on the Fourth Round of the NIST Post-Quantum Cryptography Standardization Process, March 2025
    locator: Section 3.1 (the HQC scheme and the reasons for its selection), Table 8 (hqc-128 has an encapsulation key of 2249 bytes, a decapsulation key of 40 bytes and a ciphertext of 4497 bytes)
  - paper: "Dennis Hofheinz, Kathrin Hövelmanns and Eike Kiltz, A modular analysis of the Fujisaki-Okamoto transformation, TCC 2017, LNCS 10677, pages 341 to 371"
    locator: the transforms with implicit rejection used to turn the PKE into an IND-CCA2 KEM
  - paper: "Qian Guo, Clemens Hlauschek, Thomas Johansson, Norman Lahr, Alexander Nilsson and Robin Leander Schröder, Don't reject this, key-recovery timing attacks due to rejection-sampling in HQC and BIKE, IACR Transactions on Cryptographic Hardware and Embedded Systems 2022(3)"
    locator: the whole paper (timing leaks of the sampler in the re-encryption step reveal the secret key)
  - paper: "Irving S. Reed, A class of multiple-error-correcting codes and the decoding scheme, Transactions of the IRE Professional Group on Information Theory 4(4), pages 38 to 49, 1954"
    locator: the whole paper (Reed-Muller codes and majority decoding)
  - paper: "Irving S. Reed and Gustave Solomon, Polynomial codes over certain finite fields, Journal of the Society for Industrial and Applied Mathematics 8(2), pages 300 to 304, 1960"
    locator: the whole paper (Reed-Solomon codes)
---

HQC (Hamming Quasi-Cyclic) is a code-based [KEM](/key-encapsulation-mechanism/). Unlike [McEliece](/mceliece-cryptosystem/) and [BIKE](/bike/), it does not hide a decodable code inside the public key. The code used for decoding is public and fixed: a [Reed-Solomon code](/reed-solomon-code/) concatenated with a repeated [Reed-Muller code](/reed-muller-code/). Security instead comes from a random quasi-cyclic code given by a dense polynomial $h$: the public key is $(h, s = x + hy)$ with sparse secrets $x, y$, much as in [learning with errors](/learning-with-errors/). Decryption leaves a noisy codeword whose noise has known statistics, so the decryption failure rate can be bounded with more confidence than for BIKE. In March 2025 NIST selected HQC for standardization as a backup to ML-KEM (NIST IR 8545).

**Notation.** $\mathcal{R} = \mathbb{F}_2[x]/(x^n - 1)$ with $n$ prime and 2 primitive modulo $n$. $\mathcal{S}_w$ is the set of elements of $\mathcal{R}$ of [Hamming weight](/hamming-weight/) $w$. $\mathcal{C}$ is the public concatenated code of length $n_1 n_2 \le n$ and dimension $k$ bits, with generator matrix $G$ and a decoder $\mathcal{C}.\mathrm{Decode}$. $\mathrm{Trunc}$ keeps the first $n_1 n_2$ coordinates. $\mathbf{G}$, $\mathbf{H}$ and $\mathbf{K}$ are hash functions (random oracles), $\sigma$ a secret random string, $\lambda$ the security parameter, $\mathcal{A}$ an adversary and $\mathrm{Adv}$ its advantage. **Security model.** The PKE is IND-CPA if decisional quasi-cyclic syndrome decoding is hard: no efficient $\mathcal{A}$ tells $(h, x + hy)$ or $(h, r_1 + hr_2, s r_2 + e)$ from uniform with non-negligible $\mathrm{Adv}$. The KEM uses the HHK version of the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/) with implicit rejection and a salt, and it is IND-CCA2 in the random oracle model, with a loss that grows with the decryption failure rate.

## In plain words

The receiver publishes a random-looking pair: a random polynomial $h$ and $s = x + hy$, where $x$ and $y$ are secret and sparse. To send a message, the sender encodes it with a public error-correcting code and hides it with $s r_2$, where $r_2$ is a fresh sparse polynomial, and also sends $u = r_1 + h r_2$ as a hint.

The receiver multiplies the hint by $y$ and subtracts. The large random parts cancel, and only a moderate amount of noise remains, made of products of sparse vectors. The public code is strong enough to remove that noise, so the receiver reads the message. An attacker without $y$ sees only random-looking vectors.

## The problem

Key encapsulation: key generation outputs a public key and a private key; encapsulation with the public key outputs a ciphertext and a shared key; decapsulation with the private key recovers the same key, except with a tiny failure probability.

## The algorithm

```pseudo id=main
KEYGEN()
L1  h ← a uniform element of R;  x, y ← uniform elements of S_w
L2  s ← x + h·y
L3  return pk = (h, s) and sk = (x, y)

ENCRYPT(pk, m, θ)                           ▷ m has k bits; θ seeds the randomness
L4  r1, r2 ← elements of S_wr;  e ← an element of S_we, all derived from θ
L5  u ← r1 + h·r2;  v ← Trunc(m·G + s·r2 + e)
L6  return (u, v)

DECRYPT(sk, (u, v))
L7  return C.DECODE(v − Trunc(u·y))         ▷ v − u·y = m·G + x·r2 − r1·y + e

ENCAPS(pk)
L8  m ← a random k-bit string;  salt ← a random string
L9  θ ← G(H(pk), m, salt);  (u, v) ← ENCRYPT(pk, m, θ)
L10 return c = (u, v, salt) and K = K(m, c)

DECAPS(sk, c)
L11 m' ← DECRYPT(sk, (u, v))
L12 θ' ← G(H(pk), m', salt);  if ENCRYPT(pk, m', θ') = (u, v)
L13 then return K(m', c) else return K(σ, c)
```

**The public code.** For HQC-1, a message of $k = 128$ bits is 16 bytes. The outer code is a shortened Reed-Solomon code $[46, 16, 31]$ over $\mathbb{F}_{256}$, which corrects 15 wrong bytes; it is decoded with syndromes, the Berlekamp-Massey algorithm, Chien search and Forney's formula. Each of the 46 bytes is then encoded with the first-order Reed-Muller code $\mathrm{RM}(1, 7)$, a $[128, 8, 64]$ code, repeated 3 times, which gives a $[384, 8, 192]$ inner code. The inner decoder adds the 3 copies as values $\pm 1$ and finds the most likely byte with the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/) on 128 points. So $n_1 n_2 = 46 \cdot 384 = 17664 \le n = 17669$.

## Example

**The noise.** The decryption noise is $x r_2 + r_1 y + e$. With $w = 66$ and $w_r = w_e = 75$ it is the sum of up to $2 \cdot 66 \cdot 75 + 75 = 9975$ terms at nearly random positions, so each bit is 1 with probability about $(1 - e^{-2 \cdot 9975/17669})/2 \approx 0.338$. That predicts about 5976 flipped bits out of 17664, or about 130 per block of 384 bits. This is more than the 95 errors that the inner code is sure to correct, but the noise is spread at random, and maximum likelihood decoding still finds the right byte almost always; the Reed-Solomon code corrects the rare wrong bytes. With a fixed seed, the tests measured noise weights near this prediction, and in 20 decryptions no byte was wrong after the inner decoder.

**Sizes of HQC-1.** The public key is a 40-byte seed for $h$ plus $s$, which is $\lceil 17669/8 \rceil = 2209$ bytes, so 2249 bytes. The decapsulation key is a 40-byte seed. NIST IR 8545 (Table 8) lists a ciphertext of 4497 bytes; for hqc-256 the sizes are 7245 and 14485 bytes. Compared with BIKE at the same level, the public key is 41 to 47 percent larger and the ciphertext about 3 times larger.

## Correctness

In line L7, $v - u y = mG + (x + hy) r_2 + e - (r_1 + h r_2) y$, truncated, and $h y r_2$ cancels because $\mathcal{R}$ is commutative. What remains is $mG + x r_2 - r_1 y + e$. If the public decoder corrects this noise, DECRYPT returns $m$. In DECAPS, $m' = m$ gives $\theta' = \theta$, and ENCRYPT is deterministic in $\theta$, so the re-encryption equals $(u, v)$ and line L13 returns $K$. So the KEM fails only when decoding fails, and the HQC analysis bounds that probability below $2^{-128}$ for HQC-1. The proof file has the details.

## Complexity

**Ring products.** Every product in the scheme has one sparse factor, so it costs $O(nw)$ bit operations as a sum of $w$ rotations, or $O(n w / w_{\mathrm{word}})$ word operations.

**Encoding and decoding.** Reed-Solomon encoding and decoding cost $O(n_1^2)$ field operations, and Reed-Muller decoding costs $O(n_2 \log n_2)$ per byte with the transform, so $O(n_1 n_2 \log n_2)$ in total.

**KEM.** Decapsulation decrypts and then encrypts again, so it costs about twice an encryption plus decoding.

**Space.** Keys and ciphertexts are $O(n)$ bits.

## Properties

- **No hidden structure in the public key.** The decoding code is public; only the sparse $(x, y)$ is secret. Structural attacks of the McEliece type do not apply.
- **An analyzable failure rate.** The noise is a sum of products of independent sparse vectors, so its weight distribution can be computed, and the failure of the concatenated decoder can be bounded. This is the main advantage over BIKE named by NIST.
- **Larger ciphertexts.** The ciphertext holds two vectors of about $n$ bits, so it is about twice the size of the public key.
- **Reduction to a decisional problem.** The IND-CPA proof uses decisional quasi-cyclic syndrome decoding, which is not known to be as hard as the search problem in general; the best attacks are still [information set decoding](/information-set-decoding/) with a polynomial gain from the cyclic structure.

## Variants and improvements

- **Older HQC versions.** Earlier rounds used BCH codes with repetition codes, then Reed-Muller and Reed-Solomon codes, and the parameters changed as the failure analysis improved.
- **HQC with rank metric (RQC).** The same framework with rank metric codes, also by Aguilar Melchor and others; it was not kept in the NIST process.
- **Later specifications.** Recent versions use a salt in the KEM, and the 2025 version also changes details of key derivation and sampling. Check the version of the specification that a library implements.

## When to use it

Use HQC when a standard or a protocol calls for a code-based KEM, for example as a backup to ML-KEM that relies on a different hard problem. NIST plans a standard for HQC; until it is final, prefer ML-KEM for new designs and use HQC from a vetted library. Do not use the code of this page for real data.

## Pitfalls

- **Timing leaks.** Rejection sampling of fixed weight vectors in the re-encryption step leaked the secret key through timing (Guo, Hlauschek, Johansson, Lahr, Nilsson and Schröder, 2022). The decoders must also run in constant time.
- **Skipping the re-encryption check.** The PKE alone is only IND-CPA. Without the check in line L12, an attacker can learn the key from decryption failures with chosen ciphertexts.
- **Non-uniform randomness.** The vectors $r_1$, $r_2$ and $e$ must have exactly the specified weight and be derived from $\theta$ exactly as in the specification, or re-encryption fails for honest ciphertexts.

## Implementations

The Python code below is for study only. It is not constant time and uses the random module. Use a vetted implementation for real data, for example a FIPS 140 validated module once an HQC standard exists, or the reference code of the HQC team; libsodium has no HQC. The code has the real HQC-1 parameters, the real ring, the real weights, the concatenated Reed-Solomon and Reed-Muller code with full decoders, and the KEM with the salt and implicit rejection. **It does not follow the byte-level specification.** The hash functions, the seed expansion, the sampling of fixed weight vectors, the bit order of the codes and all encodings are simplified, so the outputs cannot match the official KAT files, and the tests do not use them; there are no official test vectors for this code. The tests check the Reed-Solomon decoder against brute force on a $[7, 3]$ code over $\mathbb{F}_8$, the Reed-Muller decoder against brute force nearest codeword search, the noise weight against the prediction above, and the PKE and KEM round trips with implicit rejection.

## History

Aguilar Melchor, Blazy, Deneuville, Gaborit and Zémor proposed the framework in a 2016 preprint, published in 2018, as a code-based analogue of the LWE schemes. HQC entered the NIST process in 2017 and changed its public code over the rounds to lower the failure rate and the sizes. It reached round 4 with BIKE and Classic McEliece, and in March 2025 NIST IR 8545 selected HQC, citing its more mature failure analysis compared with BIKE and its smaller public keys compared with Classic McEliece.

## References
