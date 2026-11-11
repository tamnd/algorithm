---
tag: 8ZNYFG
kind: algorithm
slug: newhope
name: NewHope
aliases:
- NewHope key exchange
area: cryptography/post-quantum
level: advanced
summary: "A ring-LWE key exchange (2016) and later KEM over Z_12289[x]/(x^n + 1) with n = 512 or 1024. Google tested it in Chrome as CECPQ1; it was a NIST round 2 candidate and led to Kyber."
model: word-ram
complexity:
  vars: {n: the ring degree (512 or 1024)}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: false, randomized: true}
history:
  year: 2016
  people: [Erdem Alkim, Léo Ducas, Thomas Pöppelmann, Peter Schwabe]
  note: The key exchange with reconciliation appeared at USENIX Security 2016 and ran in Chrome as CECPQ1. NewHope-Simple removed the reconciliation. The NIST round 2 KEM was not selected for round 3 in July 2020.
prereqs: [ring-learning-with-errors, regev-encryption, number-theoretic-transform, key-encapsulation-mechanism]
see_also: [crystals-kyber, frodokem, saber, ntru-encrypt, hybrid-key-exchange, x25519, ring-lwe-hardness, nist-pqc-standardization]
sources:
  - url: "https://www.usenix.org/conference/usenixsecurity16/technical-sessions/presentation/alkim"
    title: Erdem Alkim, Léo Ducas, Thomas Pöppelmann and Peter Schwabe, Post-quantum key exchange, a new hope, USENIX Security 2016, pages 327 to 343
    locator: "the protocol with n = 1024, q = 12289 and binomial noise, the reconciliation in the lattice D4, the choice of a fresh a for each key, and the NTT"
  - url: "https://eprint.iacr.org/2016/1157"
    title: Erdem Alkim, Léo Ducas, Thomas Pöppelmann and Peter Schwabe, NewHope without reconciliation, IACR ePrint 2016/1157
    locator: the encryption-based NewHope-Simple, with each key bit spread over several coefficients and a compressed second component
  - url: "https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization/round-2-submissions"
    title: Thomas Pöppelmann, Erdem Alkim, Roberto Avanzi, Joppe Bos, Léo Ducas, Antonio de la Piedra, Peter Schwabe, Douglas Stebila and others, NewHope, algorithm specifications and supporting documentation, NIST round 2 submission, 2019
    locator: "the algorithms NewHope-CPA-PKE and NewHope-CPA-KEM, the parameter table, and the package file KAT/newhope512cpa/PQCkemKAT_896.rsp, count = 0 (copied in the tests)"
  - paper: doi:10.6028/NIST.IR.8309
    title: NIST, IR 8309, Status report on the second round of the NIST post-quantum cryptography standardization process, July 2020
    locator: the section on NewHope (not advanced to round 3, with Kyber preferred as the structured lattice KEM)
---

NewHope is a post-quantum key exchange built on [ring learning with errors](/ring-learning-with-errors/). Its first version (2016) was an unauthenticated Diffie-Hellman-like exchange: each party sends $b = a s + e$ for a fresh public polynomial $a$, both compute approximately the same ring element, and a reconciliation step turns the approximate agreement into an exact key. It used the ring $\mathbb{Z}_{12289}[x]/(x^{1024}+1)$, the [NTT](/number-theoretic-transform/) for products, and binomial noise, and it ran in Google Chrome in 2016 as CECPQ1, combined with [X25519](/x25519/). The later NewHope-Simple and the NIST submission replaced reconciliation by encryption in the style of [Regev](/regev-encryption/): the key is encrypted as the top bit of several coefficients. This page implements NewHope512-CPA-KEM of the NIST round 2 submission. NIST did not take NewHope to round 3, and its ideas live on in [Kyber](/crystals-kyber/).

**Notation.** $R_q = \mathbb{Z}_q[x]/(x^n + 1)$ with $q = 12289$ and $n \in \{512, 1024\}$; since $q \equiv 1 \pmod{2n}$, $R_q$ has a full NTT, here with $\gamma = 10968$, a primitive $1024$-th root of unity, and $\omega = \gamma^2 = 3$. $\psi_k$ is the centered binomial distribution $\sum_{i=1}^{k} (a_i - b_i)$ with $k = 8$, so noise values lie in $[-8, 8]$. $\hat x$ is a polynomial in the NTT domain and $\circ$ the coefficientwise product. Encode places each of the 256 message bits at $\lfloor q/2 \rfloor = 6144$ in $n/256$ coefficients; Decode reads a bit back from the sum of $|x_j - \lfloor q/2 \rfloor|$ over those coefficients. Compress keeps 3 bits per coefficient.

## In plain words

NewHope lets two parties agree on a secret key over a public channel. The public key is a random polynomial times a small secret, plus a little noise; without the secret, it looks random.

To send a key, the sender picks a random key, places each of its bits at the top of two numbers, and adds a mask made from the public key and a fresh small secret. The sender also sends a hint made from the random polynomial and the same fresh secret.

The receiver uses the secret to rebuild the mask from the hint. The rebuilt mask is off by a little noise, so each pair of numbers is near the top or near the bottom, and the receiver reads the bit from where it lies. Both sides then hash the key.

## The problem

NewHope-CPA-KEM is a [key encapsulation mechanism](/key-encapsulation-mechanism/) for ephemeral keys, secure against passive attackers (IND-CPA) under the decision ring-LWE assumption. The original 2016 protocol solves the same problem as unauthenticated Diffie-Hellman: two parties derive a shared key so that an eavesdropper learns nothing about it. Neither protects against active attackers by itself; that needs authentication, or the CCA version with the FO transform.

## The algorithm

```pseudo id=main
CPA-PKE.KEYGEN()
L1  z ← SHAKE256(32 random bytes, 64);  (publicseed, noiseseed) ← z
L2  â ← GenA(publicseed)                           ▷ uniform, sampled directly in the NTT domain
L3  s ← Sample(noiseseed, 0);  e ← Sample(noiseseed, 1);  ŝ ← NTT(s);  ê ← NTT(e)
L4  b̂ ← â ∘ ŝ + ê
L5  return pk = (b̂, publicseed), sk = ŝ

CPA-PKE.ENCRYPT(pk, μ, coin)
L6  â ← GenA(publicseed)
L7  s' ← Sample(coin, 0);  e' ← Sample(coin, 1);  e'' ← Sample(coin, 2)
L8  t̂ ← NTT(s');  û ← â ∘ t̂ + NTT(e')
L9  v' ← NTT⁻¹(b̂ ∘ t̂) + e'' + Encode(μ)
L10 return c = (û, Compress(v'))

CPA-PKE.DECRYPT(sk, c)
L11 v' ← Decompress(h);  ŝ ← sk
L12 return Decode(NTT⁻¹(ŝ ∘ û) − v')

CPA-KEM.KEYGEN()
L13 return CPA-PKE.KeyGen()
CPA-KEM.ENCAPS(pk)
L14 (K, coin') ← SHAKE256(32 random bytes, 64)
L15 c ← CPA-PKE.Encrypt(pk, K, coin')
L16 return c, ss = SHAKE256(K, 32)
CPA-KEM.DECAPS(sk, c)
L17 return SHAKE256(CPA-PKE.Decrypt(sk, c), 32)
```

**Encode and Decode.** For $n = 512$, bit $i$ of $\mu$ goes into coefficients $i$ and $i + 256$. Decode adds $|x_i - 6144| + |x_{i+256} - 6144|$ and returns 1 when the sum is below 6144. Spreading one bit over two coefficients lowers the failure rate a lot, since both noise values must be large for an error. The reference code subtracts $v'$ from $s u$, as line L12 does; Decode gives the same bit for both signs when the noise is small.

**The NTT of the reference code.** The forward NTT reads its input in bit-reversed order and multiplies by powers of $\gamma$ first, which turns the negacyclic product into a cyclic one. The inverse writes natural order. The code on this page follows the same steps, so the bytes of keys and ciphertexts match the official files. Since $s$, $e$ and $e'$ are sampled with independent coefficients, reading them in another order does not change their distribution.

**Parameter sets** (round 2 specification):

| set | $n$ | $q$ | $k$ | pk | sk | ct | security |
|---|---|---|---|---|---|---|---|
| NewHope512-CPA-KEM | 512 | 12289 | 8 | 928 | 896 | 1088 | category 1 |
| NewHope1024-CPA-KEM | 1024 | 12289 | 8 | 1824 | 1792 | 2176 | category 5 |

Sizes are in bytes. The CCA versions add a hash to the ciphertext (1120 and 2208 bytes) and store more in the secret key.

## Example

**Decoding one bit.** Take $n = 512$, so $q = 12289$ and $\lfloor q/2 \rfloor = 6144$. For the bit 1, both coefficients start at 6144. After noise, say they are $6144 + 900$ and $6144 - 2000$. Decode computes $900 + 2000 = 2900 < 6144$ and returns 1. For the bit 0 with noise $1500$ and $-800$, the coefficients are 1500 and $12289 - 800 = 11489$; Decode computes $|1500 - 6144| + |11489 - 6144| = 4644 + 5345 = 9989 \ge 6144$ and returns 0.

**Compression.** Compress maps $x$ to $\lfloor (8x + 6144)/q \rfloor \bmod 8$. The coefficient $x = 5000$ becomes $\lfloor 46144 / 12289 \rfloor = 3$, and Decompress maps 3 back to $\lfloor (3 \cdot 12289 + 4)/8 \rfloor = 4608$. The rounding error, 392, is at most about $q/16 \approx 768$.

**An official vector.** The round 2 package file `KAT/newhope512cpa/PQCkemKAT_896.rsp`, count 0, gives the shared secret `E2D149E453F227B4D96786194C365E4B4321E01277A37764D384C3103D4F978F`. The code on this page reproduces it from the DRBG seed of the file, together with the SHA-256 digests of the official pk, sk and ct.

## Correctness

Write $s, e, s', e'$ for the polynomials that the NTT values represent. Then $u = a s' + e'$ and $v' = (a s + e) s' + e'' + \mathrm{Encode}(\mu) + c_v$, where $c_v$ is the compression error. So
$$s u - v' = -\left(\mathrm{Encode}(\mu) + e s' - s e' + e'' + c_v\right),$$
because $a s s' = s a s'$ in the commutative ring. Let $n_e = e s' - s e' + e'' + c_v$. If $|n_{e,i}| + |n_{e,i+256}| < 6142$ for every $i$, Decode returns every bit of $\mu$, and both sides hash the same $K$. The noise terms are sums of 512 products of values in $[-8, 8]$, so this holds except with tiny probability; the specification gives a failure rate of about $2^{-213}$ for NewHope512. The full proof, with the effect of the bit-reversed NTT, is in the proof file.

## Complexity

Each operation needs a constant number of NTTs and inverse NTTs, each $\Theta(n \log n)$, plus $\Theta(n)$ work for sampling, coefficientwise products, Encode, Decode and packing. GenA reads about $2n$ bytes from SHAKE128 with rejection of values above $5q$. Keys and ciphertexts have $\Theta(n)$ coefficients of 14 bits, and the extra memory is $\Theta(n)$.

## Properties

- **IND-CPA under ring-LWE.** The public key and the ciphertext are ring-LWE samples, so both look uniform, and the key $K$ is hidden. NewHope-CPA-KEM is meant for ephemeral keys, where each key pair is used once.
- **IND-CCA version.** NewHope-CCA-KEM adds a variant of the FO transform with re-encryption and a hash of the ciphertext.
- **A fresh $a$ for each key.** The 2016 paper insisted on generating $a$ from a seed for each key pair, which removes the risk of a backdoored fixed $a$ and of precomputation over all users. Kyber kept this.
- **Simple parameters.** $q = 12289$ is the smallest prime with $q \equiv 1 \pmod{2048}$, which allows the NTT for $n = 1024$; the noise is binomial, which is easy to sample in constant time.

## Variants and improvements

- **NewHope (2016)** used $n = 1024$ and binomial noise with $k = 16$, and reconciliation: the responder sends 2 bits per coefficient of hint, and the key bits are decoded with the lattice $\tilde D_4$ from 4 coefficients each. The failure rate was below $2^{-60}$.
- **NewHope-Simple (2016)** replaced reconciliation by encryption, at a small cost in ciphertext size, and is the basis of the NIST submission.
- **NewHope-CPA-KEM and NewHope-CCA-KEM** (2017 to 2019) are the NIST round 1 and 2 versions, with $n = 512$ and $n = 1024$.
- **Kyber** moved from ring-LWE to module-LWE, which allows a degree of 256 for all security levels and gives more flexible parameters.

## When to use it

NewHope is not a standard; for new systems use [ML-KEM](/crystals-kyber/). Study NewHope to learn the step from Diffie-Hellman-style ring-LWE exchange with reconciliation to encryption-based KEMs, and as the scheme of the first large post-quantum experiment on the web.

## Pitfalls

- **Reusing CPA keys.** The CPA version is not safe if a key pair is used for many exchanges with active attackers: chosen ciphertexts can reveal the secret coefficient by coefficient. Use the CCA version or fresh keys.
- **Timing in GenA and Sample.** Rejection in GenA depends only on public data, but the noise sampler and Decode must be constant time.
- **NTT order.** The reference NTT expects bit-reversed input; an NTT that reads natural order computes a different (but valid) scheme, and the test vectors fail.
- **Reconciliation bias.** Simple reconciliation methods can bias the key; the 2016 protocol needs its randomized rounding to make the key uniform.

## Implementations

The Python code on this page implements NewHope512-CPA-KEM of the NIST round 2 submission, with the NTT of the reference code. The tests run the NIST AES-256 CTR_DRBG and reproduce the official known answer vector `PQCkemKAT_896.rsp`, count 0: the shared secret is compared with the value copied from the file, and pk, sk and ct through SHA-256 digests of the official hex. They also check the first entries of the precomputed tables, the negacyclic product, and round trips. The 2016 reconciliation protocol, the CCA versions and NewHope1024 are not implemented. The code is for study only: it is not constant time and must not be used to protect real data.

## History

Ding (2012) and Peikert (2014) proposed key exchange from ring-LWE with reconciliation, and Bos, Costello, Naehrig and Stebila (2015) tested it in TLS. Alkim, Ducas, Pöppelmann and Schwabe made it much faster and better analysed in NewHope (2016). In July 2016 Google ran the experiment CECPQ1 in Chrome Canary, with a hybrid of X25519 and NewHope, and ended it later that year. NewHope-Simple appeared in late 2016, and the NewHope team submitted NewHope to NIST in 2017. In July 2020 NIST did not move it to round 3, since Kyber covered the same space with more flexibility.

## References
