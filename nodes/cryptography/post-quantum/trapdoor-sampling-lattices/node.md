---
tag: M0ZP5R
kind: technique
slug: trapdoor-sampling-lattices
name: Trapdoor sampling for lattices
aliases:
- lattice trapdoors
- Micciancio-Peikert trapdoors
- gadget trapdoors
area: cryptography/post-quantum
level: advanced
summary: "Make a random-looking matrix A with a secret that lets one sample short Gaussian solutions of A x = u mod q without leaking it: Ajtai, Alwen-Peikert, and the Micciancio-Peikert gadget."
prereqs: [short-integer-solution, gaussian-sampling-over-lattices, lattice-basis, gram-schmidt-orthogonalization]
see_also: [gpv-signature, falcon, identity-based-encryption, attribute-based-encryption, lattice-based-cryptography, learning-with-errors, hash-and-sign-paradigm, fiat-shamir-with-aborts]
sources:
  - paper: doi:10.1007/3-540-48523-6_1
    title: Miklós Ajtai, Generating hard instances of the short basis problem, ICALP 1999, LNCS 1644
    locator: the construction of a random matrix A together with a short basis of its lattice
  - paper: doi:10.4230/LIPIcs.STACS.2009.1832
    title: Joël Alwen and Chris Peikert, Generating shorter bases for hard random lattices, STACS 2009
    locator: "the two constructions of A with a short basis S, and the bounds on |S| and on the Gram-Schmidt norm |S~|"
  - paper: doi:10.1007/978-3-642-29011-4_41
    title: Daniele Micciancio and Chris Peikert, Trapdoors for lattices, simpler, tighter, faster, smaller, EUROCRYPT 2012
    locator: "Section 4 (the gadget G, its basis S_G, inversion and sampling for G), Section 5 (the trapdoor R with A [R; I] = H G, the short basis built from R, and SamplePre with a perturbation)"
  - paper: doi:10.1145/1374376.1374407
    title: Craig Gentry, Chris Peikert and Vinod Vaikuntanathan, Trapdoors for hard lattices and new cryptographic constructions, STOC 2008
    locator: "preimage sampleable functions, and SamplePre from a short basis with the randomized nearest plane"
---

A lattice trapdoor is secret information about a public matrix $A \in \mathbb{Z}_q^{n \times m}$ that makes the function $x \mapsto A x \bmod q$ invertible on short inputs. Without it, finding a short $x$ with $A x \equiv u$ is the [short integer solution](/short-integer-solution/) problem, which is hard. With it, one can sample a short $x$ from a discrete Gaussian on the solution set, so that the output reveals nothing about the trapdoor. The technique has two parts: generate $A$ together with the trapdoor so that $A$ looks uniform, and sample preimages with it. Ajtai (1999) and Alwen and Peikert (2009) generated $A$ with a short basis of its lattice, used with [Gaussian sampling](/gaussian-sampling-over-lattices/) by Gentry, Peikert and Vaikuntanathan (2008). Micciancio and Peikert (2012) made it simpler and faster with a fixed "gadget" matrix $G$ whose preimages are easy, and a short matrix $R$ with $A \binom{R}{I} = G$. This page is about the technique; the sampler over a given basis is on the Gaussian sampling page.

## In plain words

We want a lock that anyone can close but only the owner can open. Here, closing means multiplying a short vector by a public table of numbers, and opening means finding a short vector that gives a chosen result.

There is one table for which opening is easy for everyone: the gadget, which just writes numbers in binary. The owner hides the gadget inside a random-looking public table by mixing in a secret small matrix. To open, the owner solves the easy gadget problem and then uses the secret matrix to translate the answer back.

The translated answer alone would have a shape that shows the secret. So the owner first adds well-chosen random noise, and the final answer looks the same whatever secret was used.

## When it applies

The technique applies when:

- a scheme must invert $f_A(x) = A x \bmod q$ on short inputs, for a target $u$ that someone else chose or that a hash produced, as in [hash-and-sign signatures](/gpv-signature/), [identity-based encryption](/identity-based-encryption/) (the key for an identity is a short preimage of a hash of it) and [attribute-based encryption](/attribute-based-encryption/);
- the outputs are published, so their distribution must not depend on the trapdoor: they must be Gaussian with a parameter above the smoothing parameter of the lattice;
- $A$ must be statistically close to uniform, or pseudorandom under LWE, so that security can rest on SIS or LWE for a uniform $A$.

It does not apply to schemes that only need $A$ to be random and never invert it, such as most LWE encryption and [Fiat-Shamir with aborts](/fiat-shamir-with-aborts/) signatures, which avoid trapdoors.

## The template

The holes are written in angle brackets. Throughout, $\Lambda^\perp(A) = \{x \in \mathbb{Z}^m : A x \equiv 0\}$, $\Lambda_u^\perp(A)$ is its coset of solutions of $A x \equiv u$, and $D_{\Lambda, s}$ is the discrete Gaussian with parameter $s$ (density proportional to $e^{-\pi \|x\|^2 / s^2}$).

```pseudo id=main
TRAPGEN(n, q)
L1  Ā ← uniform in Z_q^{n×m̄};  R ← ⟨SMALL⟩ in Z^{m̄×w}
L2  A ← [Ā | ⟨H⟩·⟨G⟩ − Ā R] mod q             ▷ so A·[R; I] = H·G
L3  return pk = A, trapdoor = R

SAMPLEPRE(R, u, s)                            ▷ a sample of D_{Λ_u⊥(A), s}
L4  p ← ⟨PERTURB⟩(s, R)                        ▷ Gaussian with covariance s²I − s_G²·[R; I][R; I]ᵀ
L5  v ← H⁻¹ (u − A p) mod q
L6  z ← ⟨SAMPLE-G⟩(v, s_G)                      ▷ Gaussian z with G z ≡ v
L7  return x ← p + [R; I] z
```

The holes are:

- **$\langle G \rangle$, the gadget.** A fixed matrix whose lattice $\Lambda^\perp(G)$ has a known short basis $S_G$, and for which inversion and Gaussian sampling are fast. The standard choice is $G = I_n \otimes g^\mathsf{T}$ with $g = (1, 2, 4, \dots, 2^{k-1})$ and $q = 2^k$, so $w = n k$. Its basis $S_k$ has columns $2 e_j - e_{j+1}$ and $2 e_{k-1}$, with Gram-Schmidt norm 2.
- **$\langle \mathrm{SMALL} \rangle$, the trapdoor distribution.** $R$ with small entries, for example in $\{-1, 0, 1\}$ or Gaussian. If $\bar m$ is large enough, $[\bar A \mid -\bar A R]$ is statistically close to uniform by the leftover hash lemma; with $R$ Gaussian and $\bar A$ of the form $[I \mid A']$, $A$ is pseudorandom under LWE, with a smaller $\bar m$.
- **$\langle H \rangle$, the tag.** An invertible matrix over $\mathbb{Z}_q$, usually $I$. Different tags give different functions with one trapdoor, which identity-based and attribute-based schemes and chosen-ciphertext security use.
- **$\langle \mathrm{SAMPLE\text{-}G} \rangle$, the gadget sampler.** For $q = 2^k$, sample each digit $x_j$ in the coset of $2\mathbb{Z}$ fixed by the low bit of the current target, then halve the remaining target. For any $q$, Genise and Micciancio (2018) give a sampler of the same cost.
- **$\langle \mathrm{PERTURB} \rangle$, the perturbation.** A Gaussian $p$ with covariance $\Sigma_p = s^2 I - s_G^2 T T^\mathsf{T}$, $T = \binom{R}{I}$, which exists if $s^2 > s_G^2 (s_1(R)^2 + 1)$, where $s_1(R)$ is the largest singular value of $R$. It does not depend on $u$, so it can be sampled offline.

**Walk-through.** Line L2 hides the gadget: $A T = \bar A R + H G - \bar A R = H G$. In line L5, $v$ is chosen so that $H G z \equiv u - A p$; then $A x = A p + A T z = A p + H G z \equiv u$, so line L7 returns a preimage. The vector $T z$ alone is short but has covariance about $s_G^2 T T^\mathsf{T}$, a shape that reveals $R$. Adding $p$ makes the covariance $\Sigma_p + s_G^2 T T^\mathsf{T} = s^2 I$, which is spherical and independent of $R$. The convolution theorem of Peikert (2010) makes this exact for discrete Gaussians, above the smoothing parameter.

**The older way: a short basis.** Ajtai (1999) and Alwen and Peikert (2009) generate $A$ with a short basis $S$ of $\Lambda^\perp(A)$, and GPV sample with Klein's randomized nearest plane over $S$, with $s \ge \|\tilde S\| \cdot \omega(\sqrt{\log m})$. MP12 trapdoors also give such a basis, $S = \begin{pmatrix} I & R \\ 0 & I \end{pmatrix} \begin{pmatrix} I & 0 \\ W & S_G \end{pmatrix}$ up to the order of columns, with $W$ a solution of $G W \equiv -\bar A$, but the template above is faster and needs no Gram-Schmidt step.

**A toy run.** The code uses $n = 2$, $k = 8$, $q = 256$, $\bar m = 16$, so $w = 16$ and $m = 32$. The tests check $A T \equiv G$ column by column, that the binary digits invert $G$, that the gadget sampler hits every target, and that SamplePre returns preimages with $\|x\| \le s \sqrt m$. For one gadget block and $u = 5$, both $(1, 0, 1, 0, 0, 0, 0, 0)$ and $(-1, 3, 2, -1, 0, 0, 0, 0)$ are preimages, since $-1 + 2 \cdot 3 + 4 \cdot 2 - 8 = 5$; the sampler outputs vectors of the second kind, with Gaussian digits. **The leak test** estimates the cross covariance $E[x_{\mathrm{top}} x_{\mathrm{bottom}}^\mathsf{T}]$ from 1200 preimages. Without line L4 it equals $\frac{s_G^2}{2\pi} R$, and its correlation with $R$ is above 0.9; with line L4 it is below 0.3 in absolute value, that is, noise.

## Classic examples

- **[GPV signatures](/gpv-signature/).** Hash the message to $u$ and return a sample of $D_{\Lambda_u^\perp(A), s}$. Security rests on SIS.
- **[Falcon](/falcon/).** The NTRU trapdoor: the basis $\begin{pmatrix} g & -f \\ G & -F \end{pmatrix}$ with $f G - g F = q$, found by NTRUSolve, is a short basis of an NTRU lattice, used with the fast Fourier sampler.
- **[Identity-based encryption](/identity-based-encryption/).** In GPV IBE, the secret key of an identity is a Gaussian preimage of $H(\mathrm{id})$ under $A$, and encryption is dual Regev encryption to that syndrome. Agrawal, Boneh and Boyen (2010) use the tag $H$ to get security without random oracles.
- **[Attribute-based encryption](/attribute-based-encryption/).** Boneh, Gentry, Gorbunov and others (2014) use gadget matrices to evaluate circuits on public matrices, and trapdoor sampling to give keys for a policy.
- **Trapdoor delegation.** Cash, Hofheinz, Kiltz and Peikert ("Bonsai trees", 2010) extend $A$ to $[A \mid A']$ and use the trapdoor of $A$ to sample a short basis of the larger lattice, for hierarchical IBE.

## Variations

- **Short basis trapdoors** (Ajtai 1999, Alwen and Peikert 2009) versus **gadget trapdoors** (MP12): the second gives smaller $s$, no Gram-Schmidt, and an offline/online split.
- **Statistical versus computational trapdoors:** $R$ uniform in $\{-1,0,1\}$ with a large $\bar m$, or $R$ Gaussian with $\bar A = [I \mid \hat A]$, $\bar m = 2n$ and $A$ pseudorandom under LWE.
- **Ring and module versions** replace $\mathbb{Z}_q^{n \times m}$ by matrices over $R_q$ and save a factor $n$ in key size.
- **Approximate trapdoors** (Chen, Genise and Mukherjee, 2019) drop the low digits of the gadget and return $x$ with $A x \approx u$, for shorter keys and signatures.
- **Other bases $b$:** $g = (1, b, \dots, b^{k-1})$ trades the length of $G$ against the size of its digits.

## Pitfalls

- **Skipping the perturbation.** $x = T z$ is a valid short preimage, but over many samples its covariance reveals $R$; the leak test shows this.
- **Width too small.** If $s^2 \le s_G^2 (s_1(R)^2 + 1)$, the covariance $\Sigma_p$ is not positive definite and the output cannot be spherical.
- **Repeated targets.** Two independent preimages of the same $u$ differ by a short vector of $\Lambda^\perp(A)$, and the security proof of GPV signatures then fails. Signatures need a salt or state.
- **$A$ not uniform.** With $\bar m$ too small and $R$ ternary, $[\bar A \mid -\bar A R]$ is not close to uniform, and the security proof does not apply.
- **Floating point and timing.** The perturbation uses a Cholesky factor and real Gaussians; precision errors and timing differences can leak the trapdoor.
- **Wrong parameter convention.** $s$ versus $\sigma = s / \sqrt{2\pi}$, as on the Gaussian sampling page.

## Exercises

1. Show that $S_k$ is a basis of $\Lambda^\perp(g^\mathsf{T})$ for $q = 2^k$, and that, taken in a suitable order, its Gram-Schmidt vectors all have length 2.
2. Prove that the gadget sampler of the template returns $x$ with $g^\mathsf{T} x \equiv u \pmod{2^k}$ for every $u$.
3. Verify that $A \binom{R}{I} = H G$ for $A = [\bar A \mid H G - \bar A R]$, and use it to write a short basis of $\Lambda^\perp(A)$ from $R$ and $S_G$.
4. Show that $\Sigma_p = s^2 I - s_G^2 T T^\mathsf{T}$ is positive definite exactly when $s > s_G \sqrt{s_1(R)^2 + 1}$.
5. Without the perturbation, compute $E[x x^\mathsf{T}]$ for $x = T z$ with $z$ spherical, and explain how an attacker estimates $R$ from it.

## References
