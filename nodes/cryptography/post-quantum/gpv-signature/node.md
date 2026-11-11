---
tag: ZA5GEM
kind: algorithm
slug: gpv-signature
name: GPV hash-and-sign lattice signature
aliases:
- Gentry-Peikert-Vaikuntanathan signature
- GPV signature
area: cryptography/post-quantum
level: research
summary: "The 2008 hash-and-sign signature of Gentry, Peikert and Vaikuntanathan: hash to a syndrome u, then sample a short Gaussian x with A x = u using a trapdoor basis. Secure under SIS in the ROM."
model: word-ram
complexity:
  vars: {m: the dimension of the signature vector}
  time: {worst: ∞, average: Θ(m^2), best: Θ(m^2)}
  space: {extra: Θ(m^2)}
properties: {deterministic: false, randomized: true}
history:
  year: 2008
  people: [Craig Gentry, Chris Peikert, Vinod Vaikuntanathan]
  note: Introduced preimage sampleable trapdoor functions at STOC 2008, which fixed the leak that broke the GGH and NTRUSign signatures. Falcon is its efficient form over NTRU lattices.
prereqs: [short-integer-solution, gaussian-sampling-over-lattices, trapdoor-sampling-lattices, hash-and-sign-paradigm, digital-signature]
see_also: [falcon, crystals-dilithium, fiat-shamir-with-aborts, babai-nearest-plane, random-oracle-model, strong-unforgeability, lattice-based-cryptography, closest-vector-problem]
sources:
  - paper: doi:10.1145/1374376.1374407
    title: Craig Gentry, Chris Peikert and Vinod Vaikuntanathan, Trapdoors for hard lattices and new cryptographic constructions, STOC 2008
    locator: "Section 4 (the discrete Gaussian sampler SampleD, a randomized nearest plane), Section 5 (preimage sampleable functions from SIS), Section 6 (hash-and-sign signatures in the random oracle model)"
  - paper: doi:10.1007/11761679_17
    title: Phong Q. Nguyen and Oded Regev, Learning a parallelepiped, cryptanalysis of GGH and NTRU signatures, EUROCRYPT 2006
    locator: "the hidden parallelepiped problem, the moment of order 4 and its minimization by gradient descent"
  - paper: doi:10.1007/978-3-642-29011-4_41
    title: Daniele Micciancio and Chris Peikert, Trapdoors for lattices, simpler, tighter, faster, smaller, EUROCRYPT 2012
    locator: "the gadget G, its basis S_G, and the short basis of Lambda^perp(A) for A = [Abar | G - Abar R] (used for the toy trapdoor)"
---

The GPV signature, by Gentry, Peikert and Vaikuntanathan (2008), is the first lattice signature in the [hash-and-sign](/hash-and-sign-paradigm/) style with a security proof. The public key is a random-looking matrix $A \in \mathbb{Z}_q^{n \times m}$ and the secret key is a short basis $S$ of the lattice $\Lambda^\perp(A) = \{x \in \mathbb{Z}^m : A x \equiv 0 \pmod q\}$. To sign, hash the message to a syndrome $u \in \mathbb{Z}_q^n$, and use $S$ to sample a short vector $x$ with $A x = u$ from a discrete Gaussian. To verify, check $A x = u$ and that $x$ is short. Forging is as hard as the [short integer solution](/short-integer-solution/) problem. The key point is the Gaussian: the earlier schemes GGH and NTRUSign rounded with the secret basis, and their signatures leaked its shape, which Nguyen and Regev (2006) used to recover the key. A Gaussian sample does not depend on the basis that produced it. [Falcon](/falcon/) is the practical form of GPV.

**Notation.** $q$ is the modulus and $A \in \mathbb{Z}_q^{n \times m}$. $\Lambda^\perp(A)$ is the lattice above and $\Lambda_u^\perp(A) = \{x : A x \equiv u\}$ is its coset. $D_{\Lambda + c, s}$ is the discrete Gaussian on a coset with parameter $s$, with probability proportional to $\exp(-\pi \|x\|^2 / s^2)$. $\tilde S$ is the Gram-Schmidt orthogonalization of $S$ and $\|\tilde S\|$ the length of its longest vector. $\eta_\varepsilon(\Lambda)$ is the smoothing parameter. $H$ is a hash function onto $\mathbb{Z}_q^n$, modeled as a random oracle.

## In plain words

The public key is a big random-looking table of numbers. A signature is a list of small numbers that, combined with the table, gives the hash of the message. Without the secret it is hard to find such a short list, even though long lists are easy to find.

The secret is a set of short vectors that the table maps to zero. The signer first finds any list, usually long, that gives the hash. Then it uses the short secret vectors to make the list short.

How this step is done matters. If the signer rounds in a fixed way, the signatures slowly show the shape of the secret vectors, and an attacker can learn them. GPV adds the right amount of randomness, so every signature looks the same whatever secret was used.

## The problem

GPV solves the [digital signature](/digital-signature/) problem with existential unforgeability under chosen message attacks. The underlying tool is a preimage sampleable function (PSF): $f_A(x) = A x \bmod q$ on short inputs. A PSF must have three properties. The output of $f_A$ on a Gaussian input is close to uniform. With the trapdoor, one can sample a preimage of any $u$ from the Gaussian on $\Lambda_u^\perp(A)$, with the same distribution as a Gaussian input conditioned on $f_A(x) = u$. Without it, finding two short preimages of one $u$ is hard, since their difference is a short nonzero vector of $\Lambda^\perp(A)$, a SIS solution.

## The algorithm

The pseudocode uses the gadget trapdoor of Micciancio and Peikert (2012) for the key; GPV allows any generator of $A$ with a short basis.

```pseudo id=main
KEYGEN(n, k, m̄)                              ▷ q = 2^k, w = n k, m = m̄ + w
L1  Ā ← uniform in Z_q^{n×m̄};  R ← random small matrix in Z^{m̄×w}
L2  A ← [Ā | G − Ā R] mod q                  ▷ G = I_n ⊗ (1, 2, …, 2^{k−1})
L3  S ← short basis of Λ⊥(A) built from R;  S̃ ← Gram-Schmidt(S)
L4  s ← ‖S̃‖ · η;  return pk = (A, s), sk = (S, S̃)

SIGN(sk, msg)
L5  salt ← 16 random bytes
L6  u ← H(salt ‖ msg) ∈ Z_q^n
L7  t ← any integer vector with A t ≡ u (mod q)
L8  v ← SampleD(S, S̃, s, center −t)          ▷ randomized nearest plane, v ∈ Λ⊥(A)
L9  return σ = (salt, x ← t + v)

VERIFY(pk, msg, (salt, x))
L10 if ‖x‖ > s·√m, reject
L11 accept iff A x ≡ H(salt ‖ msg) (mod q)
```

**Line L3.** The basis is $S = \begin{pmatrix} R S_G & I + R W \\ S_G & W \end{pmatrix}$, where $S_G$ is a short basis of $\Lambda^\perp(G)$ with columns $2 e_j - e_{j+1}$ and $2 e_{k-1}$ in each block, and $W$ is the binary expansion of $-\bar A$, so that $G W \equiv -\bar A$. Each column is in $\Lambda^\perp(A)$, and $\det S = q^n$. See [trapdoor sampling](/trapdoor-sampling-lattices/).

**Line L7.** $t = \begin{pmatrix} R \\ I \end{pmatrix} G^{-1}(u)$, where $G^{-1}(u)$ is the vector of bits of $u$; then $A t = \bar A R G^{-1}(u) + (G - \bar A R) G^{-1}(u) = u$. This $t$ is short, but it is a fixed linear function of $R$, so it must never be published.

**Line L8.** SampleD is Klein's randomized nearest plane: for $i = m, \dots, 1$ it samples an integer coefficient for $b_i$ from a one-dimensional discrete Gaussian with parameter $s / \|\tilde b_i\|$, centered where the nearest plane step would round. See [Gaussian sampling over lattices](/gaussian-sampling-over-lattices/). Then $x = t + v$ has the distribution $D_{\Lambda_u^\perp(A), s}$, which depends only on $A$, $u$ and $s$.

**The salt.** If the same $u$ were signed twice, the two signatures would be two short preimages of one $u$, and their difference would be a SIS solution. GPV avoids this either by keeping state (store and repeat the first signature) or by hashing a fresh random salt with the message, as here.

**The parameter $\eta$.** $s$ must be at least $\|\tilde S\| \cdot \omega(\sqrt{\log m})$ so that $s$ exceeds the smoothing parameter of every one-dimensional step. The code takes $\eta = \sqrt{\ln(2 m (1 + 1/\varepsilon)) / \pi}$ with $\varepsilon = 2^{-20}$.

## Example

**The trivial preimage.** Take $n = 2$, $k = 8$, $q = 256$. For $u = (200, 37)$, the bits of 200 and 37, least significant first, are $(0,0,0,1,0,0,1,1)$ and $(1,0,1,0,0,1,0,0)$, and $G$ times this 16-bit vector is $(8 + 64 + 128, 1 + 4 + 32) = (200, 37)$. So $t = (R \, G^{-1}(u), G^{-1}(u))$ satisfies $A t = u$.

**Why line L8 is needed.** In the toy instance of the tests ($n = 2$, $k = 8$, $\bar m = 8$, so $m = 24$), $t$ has norm about 9, shorter than the signature, whose norm is about 21. But the top part of $t$ is $R$ times the known bits $G^{-1}(u)$. After 16 signatures with linearly independent bit vectors, an attacker solves a linear system and gets $R$. The Gaussian sample $x = t + v$ has the same distribution for any trapdoor, so it reveals nothing about $R$.

**Sizes in the toy instance.** For the key of the sign and verify test (seed 2), the Gram-Schmidt norms of $S$ go from about $0.3$ to $\sqrt{28} \approx 5.29$, so $\|\tilde S\| \approx 5.29$, $\eta \approx 2.38$, $s \approx 12.6$ and the bound of line L10 is $s \sqrt{24} \approx 61.6$.

**The Nguyen-Regev attack.** A toy GGH signer of dimension 4 signs a target $c$ with Babai rounding, $x = \lfloor c B^{-1} \rceil B$. Then $c - x$ is uniform in the parallelepiped $\{y B : y \in [-1/2, 1/2)^4\}$. From 10000 signatures, the tests estimate $B^\mathsf{T} B$, transform the samples to a hypercube, find the four directions where the fourth moment is smallest by gradient descent, and recover all rows of $B$ up to sign.

## Correctness

By line L7, $A t \equiv u$, and by line L8, $v \in \Lambda^\perp(A)$, so $A x \equiv u$, and line L11 accepts. The vector $x$ is distributed close to $D_{\Lambda_u^\perp(A), s}$. A lattice Gaussian with parameter $s$ above the smoothing parameter has norm at most $s \sqrt{m}$ except with probability below $2^{-m}$ (Banaszczyk's lemma), so line L10 accepts with that probability. The full proof is in the proof file.

## Complexity

Key generation builds $S$ in $\Theta(m^2 n)$ and its Gram-Schmidt form in $\Theta(m^3)$, and stores both, $\Theta(m^2)$. Signing does $m$ steps of the sampler, each with an inner product of length $m$ and a vector update, so $\Theta(m^2)$ arithmetic operations; the one-dimensional rejection sampler has expected $O(1)$ trials but no worst-case bound, so the worst case is unbounded. Verification costs $\Theta(n m)$. Falcon brings signing to $O(m \log m)$ with ring structure and the fast Fourier sampler.

## Properties

- **Security.** Strongly unforgeable in the random oracle model if SIS with bound $2 s \sqrt{m}$ is hard. The reduction programs $H(\mathrm{salt} \| \mathrm{msg}) = A x$ for a Gaussian $x$ it picked, which is close to uniform; a forgery gives a second short preimage, and the difference is a SIS solution. Security in the quantum random oracle model was shown later by Boneh, Dagdelen, Fischlin, Lehmann, Schaffner and Zhandry (2011).
- **Zero knowledge about the trapdoor.** The signature distribution depends only on $A$ and $s$. Two different short bases with $\|\tilde S\| \le s/\eta$ give the same distribution.
- **Quality.** The signature length is about $\|\tilde S\| \cdot \eta \cdot \sqrt{m}$, so better trapdoors give shorter signatures.
- **Identity-based encryption.** The same PSF gives the GPV identity-based encryption scheme, with dual Regev encryption.

## Variants and improvements

- **[Falcon](/falcon/)** uses NTRU lattices for compact keys and the fast Fourier sampler of Ducas and Prest.
- **Peikert's sampler (2010)** replaces Klein's sequential steps by a convolution that can run in parallel.
- **MP12 trapdoors** with perturbation sampling give a sampler with a fixed offline part and a fast online part.
- **Stateful and stateless versions.** The original paper gives both; the salted version is stateless.
- **GGH and NTRUSign** are the insecure ancestors that round deterministically.

## When to use it

Use GPV to study why hash-and-sign lattice signatures need Gaussian sampling, and as the base of identity-based and attribute-based schemes. For real signatures use [Falcon](/falcon/) or [ML-DSA](/crystals-dilithium/): a plain GPV over unstructured lattices has keys of megabytes at real security levels.

## Pitfalls

- **Deterministic rounding.** Babai rounding or nearest plane signatures leak the secret basis; this is the Nguyen-Regev attack.
- **Signing the same syndrome twice.** Two different preimages of one $u$ give a SIS solution and break the proof; use state or a salt.
- **$s$ too small.** If $s$ is below $\|\tilde S\| \cdot \eta$, the distribution depends on the basis and leaks it.
- **Floating point and timing.** The sampler uses real numbers and rejection; small errors or timing differences leak information. Real implementations need careful precision and constant-time code.

## Implementations

The Python code on this page is GPV with a toy MP12 gadget trapdoor ($n = 2$, $q = 256$, $m = 24$), Klein's sampler in floating point with an exact Gram-Schmidt step, a SHAKE256 hash to the syndrome with a 16-byte salt, and the Nguyen-Regev attack on a toy GGH signer of dimension 4. **There is no official vector:** GPV is a scheme from a paper, with no standard parameters or test vectors. The tests check that the basis is in $\Lambda^\perp(A)$ and has determinant $q^n$, sign and verify, the rejection of a long preimage, and that the attack recovers the whole GGH key. The code is for study only: it is not constant time, uses toy sizes, and the attack runs only on a toy signer.

## History

Goldreich, Goldwasser and Halevi proposed GGH signatures in 1997, and Hoffstein and others proposed NTRUSign in 2003; both signed with a short secret basis by rounding. Nguyen and Regev showed in 2006 that these signatures reveal the secret parallelepiped, and broke both. Klein had given a randomized nearest plane algorithm for bounded distance decoding in 2000. Gentry, Peikert and Vaikuntanathan showed at STOC 2008 that it samples a discrete Gaussian, defined preimage sampleable functions, and built GPV signatures and identity-based encryption. Micciancio and Peikert (2012) gave the gadget trapdoors, and Falcon (2017) made the approach practical.

## References
