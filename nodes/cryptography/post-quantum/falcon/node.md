---
tag: PSM659
kind: algorithm
slug: falcon
name: Falcon
aliases:
- FN-DSA
- FIPS 206
area: cryptography/post-quantum
level: advanced
summary: "A hash-and-sign signature over NTRU lattices in the GPV framework, with fast Fourier sampling. It has the shortest signatures of the NIST lattice schemes and is planned as FN-DSA."
model: word-ram
complexity:
  vars: {n: the ring degree (512 or 1024)}
  time: {worst: ∞, average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n log n)}
properties: {deterministic: false, randomized: true}
history:
  year: 2017
  people: [Pierre-Alain Fouque, Jeffrey Hoffstein, Paul Kirchner, Vadim Lyubashevsky, Thomas Pornin, Thomas Prest, Thomas Ricosset, Gregor Seiler, William Whyte, Zhenfei Zhang]
  note: Submitted to the NIST process in 2017; the round 3 specification v1.2 is from 2020. NIST selected it in July 2022 for a future standard named FN-DSA (FIPS 206).
prereqs: [gpv-signature, gaussian-sampling-over-lattices, ntru-problem, digital-signature]
see_also: [crystals-dilithium, ntru-encrypt, trapdoor-sampling-lattices, hash-and-sign-paradigm, fast-fourier-transform, babai-nearest-plane, timing-attack, nist-pqc-standardization]
sources:
  - url: "https://falcon-sign.info/falcon.pdf"
    title: Pierre-Alain Fouque, Jeffrey Hoffstein, Paul Kirchner, Vadim Lyubashevsky, Thomas Pornin, Thomas Prest, Thomas Ricosset, Gregor Seiler, William Whyte and Zhenfei Zhang, Falcon, fast-Fourier lattice-based compact signatures over NTRU, specification v1.2, 2020
    locator: "the algorithms KeyGen, NTRUGen, NTRUSolve, ffLDL, Sign, ffSampling, SamplerZ, Compress and Verify, and the parameter table with sigma and floor(beta^2)"
  - paper: doi:10.1145/1374376.1374407
    title: Craig Gentry, Chris Peikert and Vinod Vaikuntanathan, Trapdoors for hard lattices and new cryptographic constructions, STOC 2008, pages 197 to 206
    locator: the hash-and-sign framework with a preimage sampleable function, which Falcon instantiates on NTRU lattices
  - paper: doi:10.1145/2930889.2930923
    title: Léo Ducas and Thomas Prest, Fast Fourier orthogonalization, ISSAC 2016, pages 191 to 198
    locator: the ffLDL decomposition and the fast Fourier nearest plane and sampler in O(n log n)
  - url: "https://github.com/QubitEthereum/falcon"
    title: The Falcon round 3 submission package (a mirror on GitHub), file KAT/falcon512-KAT.rsp
    locator: count = 0 (the public key and signed message, copied in the tests)
  - paper: doi:10.6028/NIST.IR.8413-upd1
    title: NIST, IR 8413 (update 1), Status report on the third round of the NIST post-quantum cryptography standardization process, 2022
    locator: the section on the selected signatures (Falcon, and the remarks on its floating point arithmetic)
---

Falcon is a lattice signature in the hash-and-sign style. The signer hashes the message with a random salt to a point $c$ in $\mathbb{Z}_q^n$ and then uses a secret short basis of an NTRU lattice to find a short vector $(s_1, s_2)$ with $s_1 + s_2 h \equiv c \pmod q$, where $h$ is the public key. The verifier recomputes $s_1$ from $s_2$ and checks that the pair is short. Falcon is the [GPV framework](/gpv-signature/) instantiated on NTRU lattices: the short vector comes from a [discrete Gaussian sampler](/gaussian-sampling-over-lattices/) so that signatures leak nothing about the basis, and the sampler is the fast Fourier sampler of Ducas and Prest, which runs in $O(n \log n)$. NIST selected Falcon in 2022 for the standard FN-DSA (FIPS 206). Falcon-512 has a public key of 897 bytes and signatures of at most 666 bytes, the smallest sum among the lattice candidates.

**Notation.** $R = \mathbb{Z}[x]/(x^n + 1)$ with $n \in \{512, 1024\}$ and $q = 12289$. The secret polynomials $f, g, F, G \in R$ satisfy the NTRU equation $f G - g F = q$, and $f$ is invertible modulo $q$. The public key is $h = g f^{-1} \bmod q$. The NTRU lattice is $\Lambda = \{(a, b) \in R^2 : a + b h \equiv 0 \pmod q\}$; it has the public basis $\begin{pmatrix} -h & 1 \\ q & 0 \end{pmatrix}$ and the secret short basis $B = \begin{pmatrix} g & -f \\ G & -F \end{pmatrix}$, where each entry stands for the $n \times n$ block of a multiplication. $\sigma$ is the standard deviation of the signer, and $\lfloor \beta^2 \rfloor$ is the bound on the squared norm of a signature. HashToPoint maps a byte string to $\mathbb{Z}_q^n$ with SHAKE256.

## In plain words

The public key describes a large grid of points in a space with many dimensions. Anyone can find some grid point near a target, but only the holder of a secret set of short directions can find a very near one.

To sign, the signer turns the message and a random salt into a target. With the short directions, the signer walks from the target to a near grid point, taking each step with a small random choice. The difference between the target and the grid point is the signature. It is short, and because of the random choices it shows nothing about the secret directions.

To verify, anyone recomputes the target and checks two things: the signature leads from the target to a grid point, and it is short.

## The problem

Falcon solves the [digital signature](/digital-signature/) problem with existential unforgeability under chosen message attack. A forger who can make a short pair $(s_1, s_2)$ with $s_1 + s_2 h \equiv c$ for a new hash value $c$ solves an instance of SIS on the NTRU lattice, which is believed hard when $h$ looks random ([NTRU problem](/ntru-problem/)). The difficulty of the design is the signer: it must output short vectors whose distribution does not depend on the secret basis.

## The algorithm

```pseudo id=main
KEYGEN(n)
L1  sample f, g ∈ R with coefficients from D_{Z, σ_fg}, σ_fg = 1.17·√(q / 2n)
L2  if f is not invertible mod q, or the Gram-Schmidt norm of B is above 1.17·√q, go to L1
L3  (F, G) ← NTRUSolve(f, g, q);  if it fails, go to L1      ▷ f G − g F = q
L4  h ← g · f⁻¹ mod q
L5  B ← [[g, −f], [G, −F]];  T ← ffLDL tree of B·B* (in FFT form)
L6  return pk = h, sk = (B, T)

SIGN(sk, m)
L7  r ← 40 random bytes (the salt)
L8  c ← HashToPoint(r ‖ m, q, n)
L9  loop
L10     v ← ffSampling((c, 0), T)                 ▷ a vector of Λ near (c, 0), Gaussian with width σ
L11     (s1, s2) ← (c, 0) − v
L12     if ‖(s1, s2)‖² ≤ ⌊β²⌋ then leave the loop
L13 s ← Compress(s2, slen);  if s = ⊥, go to L7
L14 return sig = (r, s)

VERIFY(pk, m, sig)
L15 c ← HashToPoint(r ‖ m, q, n)
L16 s2 ← Decompress(s, n);  if s2 = ⊥ return false
L17 s1 ← c − s2·h mod q, with coefficients centered in (−q/2, q/2]
L18 return ‖(s1, s2)‖² ≤ ⌊β²⌋
```

**NTRUSolve.** Line L3 finds $F, G$ by a descent over the tower of rings $\mathbb{Z}[x]/(x^{n/2^i} + 1)$. The field norm $N(f) = f(x) f(-x)$, read as a polynomial in $x^2$, halves the degree. At degree 1 the extended Euclidean algorithm solves $u N(f) + v N(g) = 1$ over the integers. On the way back up, the solution is lifted with $F \leftarrow F(x^2) g(-x)$ and $G \leftarrow G(x^2) f(-x)$, and then reduced in the style of Babai so that $F, G$ stay short.

**The sampler.** Line L10 is a randomized [nearest plane](/babai-nearest-plane/) on the basis $B$: it walks over the Gram-Schmidt vectors from the last to the first and, at each step, picks an integer coefficient from a one-dimensional discrete Gaussian centered at the exact real coefficient. This is Klein's sampler, as used by GPV. Ducas and Prest showed that over the ring the Gram-Schmidt step has the recursive structure of the FFT, which gives the ffLDL tree of line L5 and a sampler in $O(n \log n)$ operations on floating point numbers. The leaves of the tree hold the widths $\sigma / \|\tilde b_i\|$, so each base sample needs a width in $[\sigma_{\min}, \sigma_{\max}]$, and SamplerZ draws it with a constant-time rejection sampler.

**Parameter sets** (from the parameter table of the specification):

| set | $n$ | $\sigma$ | $\lfloor \beta^2 \rfloor$ | public key | signature | category |
|---|---|---|---|---|---|---|
| Falcon-512 | 512 | 165.7366171829776 | 34034726 | 897 bytes | 666 bytes | 1 |
| Falcon-1024 | 1024 | 168.38857144654395 | 70265242 | 1793 bytes | 1280 bytes | 5 |

The bound is $\lfloor \beta^2 \rfloor = \lfloor (1.1 \sigma)^2 \cdot 2n \rfloor$, which the tests check for both sets.

## Example

**A toy key with $n = 2$.** Take $f = 2 + x$ and $g = 1 - x$ in $\mathbb{Z}[x]/(x^2 + 1)$. The field norms are $N(f) = (2 + x)(2 - x) = 4 - x^2 = 5$ and $N(g) = 2$, which are coprime, so NTRUSolve succeeds and gives $F = -1755 - 1756x$ and $G = 3511 - 1756x$. Check the NTRU equation: $f G = 8778 - x$ and $g F = -3511 - x$, so $f G - g F = 12289 = q$. The public key is $h = 2458 + 4915x$: indeed $f h = 4916 - 4915 + 12288x \equiv 1 - x = g \pmod q$.

**A toy signature.** For the target $c = 5000 + 100x$, the exact nearest plane on $B$ gives $s_1 = 60 + 1827x$ and $s_2 = -1084 + 402x$, and $s_1 + s_2 h \equiv 5000 + 100x \pmod q$. The squared norm is 4678189, much larger than $q$. The reason is visible in the Gram-Schmidt norms of $B$: they are $\sqrt{7} \approx 2.65$ for the two rows of $(f, g)$ and about 4645 for the two rows of $(F, G)$. Their product is $q^n$ in every case, so a good basis must balance them near $\sqrt q$; this is the test of line L2 with the constant 1.17.

**An official vector.** The round 3 file falcon512-KAT.rsp, count 0, has a 33-byte message that starts with `D81C4D8D`, a public key of 897 bytes, and a signed message. The verifier on this page accepts it, and rejects it when one byte of the message or the signature changes.

## Correctness

Every vector $v$ returned at line L10 is in $\Lambda$, because ffSampling returns an integer combination of the rows of $B$, and both rows are in $\Lambda$: $g + (-f) h = g - g = 0$ and $G + (-F) h = (f G - g F)/f = q/f \equiv 0 \pmod q$. So $s_1 + s_2 h = c - (v_1 + v_2 h) \equiv c \pmod q$. Line L17 then computes a vector $s_1'$ that is congruent to $s_1$ modulo $q$. Centering picks, for each coefficient, the value of smallest absolute value in its class, so $\|s_1'\| \le \|s_1\|$, and line L18 accepts because line L12 did. Decompress inverts Compress on every $s_2$ that Compress accepts. The full argument is in the proof file.

## Complexity

KeyGen is dominated by NTRUSolve, which works on polynomials with large integer coefficients; it is the slowest part of Falcon, but it runs once per key. Signing costs $\Theta(n \log n)$ floating point operations for the FFT and for ffSampling, plus $\Theta(n)$ base samples; the loop of line L9 almost always succeeds the first time. Verification costs one HashToPoint and one product in $\mathbb{Z}_q[x]/(x^n+1)$, which is $\Theta(n \log n)$ with the NTT. The tree takes $\Theta(n \log n)$ floating point numbers. The toy signer on this page uses Klein's sampler on the $2n \times 2n$ integer basis, which costs $\Theta(n^2)$ per signature after a $\Theta(n^3)$ Gram-Schmidt step.

## Properties

- **Security.** In the random oracle model, Falcon is unforgeable if SIS on the NTRU lattice is hard, by the GPV argument: the signature distribution is close to a Gaussian that does not depend on the basis, so a forger can be turned into a solver of SIS. The salt $r$ makes each hashed point fresh and gives a tight reduction. Boneh, Dagdelen, Fischlin, Lehmann, Schaffner and Zhandry (2011) proved GPV-type signatures secure in the quantum random oracle model.
- **No leak.** Plain nearest plane or rounding (as in GGH and early NTRUSign) leaks the basis through the shape of signatures; the [Nguyen-Regev attack](/gpv-signature/) recovers the key. The Gaussian sampler removes this leak, provided that $\sigma$ is above the smoothing parameter of the lattice.
- **Compact.** Falcon has the smallest public key plus signature of the lattice schemes selected by NIST.
- **Floating point.** The signer needs 53-bit floating point arithmetic with exact IEEE 754 behaviour, or an emulation of it. NIST IR 8413 notes this as the main difficulty of the scheme.

## Variants and improvements

- **FN-DSA (FIPS 206).** NIST announced that Falcon will become FN-DSA. At the time of writing (November 2026) this page could not confirm from a primary source that FIPS 206 has been published as a final standard; secondary sources say that the draft was still in progress. Check the NIST site before you rely on the details, which may differ from round 3.
- **Mitaka** (Espitau and others, 2022) replaces the fast Fourier sampler by a hybrid sampler that avoids most floating point, with slightly larger signatures.
- **Hawk** (Ducas and others) uses a module lattice and the lattice isomorphism problem for a simpler signer without floating point.
- **ModFalcon** and other variants work over module lattices to get more parameter choices between 512 and 1024.

## When to use it

Use Falcon (FN-DSA when final) when the size of the signature plus the public key matters most, for example in certificates, firmware updates, or blockchains, and when you can use a well tested implementation. Prefer [ML-DSA](/crystals-dilithium/) for general use: it is already a final standard and easier to implement safely. Falcon verification is simple and fast and is safe to implement on small devices.

## Pitfalls

- **Floating point side channels.** Timing differences in floating point operations, or in the base sampler, can leak the secret basis; practical [timing attacks](/timing-attack/) and power attacks exist on unprotected code.
- **Bad base sampler.** A sampler with the wrong width or a biased tail breaks the zero-knowledge argument, and the key can then be learned from many signatures.
- **Reusing the salt.** Two signatures for the same $c$ with different random choices give a short lattice vector $(s_1 - s_1', s_2 - s_2')$ that leaks information; the salt must be fresh.
- **Detached and attached formats.** The round 3 known answer files wrap the signature in a different header than the detached format of the specification; mixing them makes valid signatures fail.

## Implementations

The Python code on this page has two parts. Part 1 is the verifier of the specification for Falcon-512 and Falcon-1024: HashToPoint, public key decoding, decompression and the norm check. The tests run it on the official known answer vector falcon512-KAT.rsp count 0, copied by hand with SHA-256 digests of the copies, and check that changed messages and signatures fail. Part 2 is a toy signer for $n = 16$: it has the real key generation with NTRUSolve and the real verification equation, but it uses Klein's sampler on the integer basis instead of ffSampling and a simple rejection sampler for the integers. So the signer is a simpler variant of the named algorithm, and no official vector checks it. The code is for study only: it is not constant time, and the signer uses floating point. Use the reference code of the Falcon team or liboqs, and a validated module once FN-DSA is final.

## History

Hoffstein, Pipher and Silverman proposed NTRU in 1996, and NTRUSign (2003) used the NTRU lattice for hash-and-sign, but its signatures leaked the basis and were broken by Nguyen and Regev in 2006. Gentry, Peikert and Vaikuntanathan (2008) fixed the leak with Gaussian sampling. Stehlé and Steinfeld (2011) proved security for NTRU keys with Gaussian coefficients, and Ducas, Lyubashevsky and Prest (2014) gave an efficient NTRU instance of GPV. Ducas and Prest (2016) found the fast Fourier sampler, and Fouque and others submitted Falcon to the NIST process in 2017. NIST selected Falcon in July 2022.

## References
