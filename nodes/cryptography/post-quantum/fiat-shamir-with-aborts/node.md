---
tag: NJ9J4P
kind: technique
slug: fiat-shamir-with-aborts
name: Fiat-Shamir with aborts
aliases:
- Lyubashevsky signatures with rejection
- FSwA
area: cryptography/post-quantum
level: advanced
summary: "Lyubashevsky's way to build lattice signatures from an identification scheme: the response z = y + S c is kept only with a rejection sampling probability that makes z independent of the secret S."
prereqs: [fiat-shamir-heuristic, sigma-protocol, rejection-sampling, short-integer-solution]
see_also: [crystals-dilithium, schnorr-signature, gpv-signature, gaussian-sampling-over-lattices, quantum-random-oracle-model, forking-lemma, zero-knowledge-proof, trapdoor-sampling-lattices]
sources:
  - paper: doi:10.1007/978-3-642-10366-7_35
    title: Vadim Lyubashevsky, Fiat-Shamir with aborts, applications to lattice and factoring-based signatures, ASIACRYPT 2009
    locator: "the identification scheme with aborts, the uniform masking in a box and the abort condition, and the signature over ideal lattices"
  - paper: doi:10.1007/978-3-642-29011-4_43
    title: Vadim Lyubashevsky, Lattice signatures without trapdoors, EUROCRYPT 2012
    locator: "Section 4 (rejection sampling, and the bound M = exp(12/alpha + 1/(2 alpha^2)) for sigma = alpha T), and the signature scheme with its proof from SIS"
  - paper: doi:10.1007/978-3-319-78372-7_18
    title: Eike Kiltz, Vadim Lyubashevsky and Christian Schaffner, A concrete treatment of Fiat-Shamir signatures in the quantum random-oracle model, EUROCRYPT 2018
    locator: "the security of Fiat-Shamir with aborts in the QROM, from lossy identification schemes"
  - paper: "Julien Devevey, Pouria Fallahpour, Alain Passelègue and Damien Stehlé, A detailed analysis of Fiat-Shamir with aborts, CRYPTO 2023"
    title: Julien Devevey, Pouria Fallahpour, Alain Passelègue and Damien Stehlé, A detailed analysis of Fiat-Shamir with aborts, CRYPTO 2023
    locator: the corrected analysis of the aborts in the ROM and the QROM, and the bounds on the number of repetitions
---

Fiat-Shamir with aborts is the technique of Lyubashevsky (2009, 2012) that turns a lattice identification scheme into a signature without a trapdoor. The pattern is that of [Schnorr signatures](/schnorr-signature/): commit to a random mask $y$, derive a challenge $c$ by hashing, and answer $z = y + S c$. Over the integers, unlike in a group of prime order, $z$ is not uniform: it is centered at the secret value $S c$, so each signature would leak a little of $S$. The fix is to abort: the signer keeps $z$ only with a probability chosen by [rejection sampling](/rejection-sampling/) so that the kept $z$ has a fixed distribution that does not depend on $S$ or $c$, and otherwise starts over with a fresh $y$. The expected number of tries is a constant $M$. [ML-DSA (Dilithium)](/crystals-dilithium/) is built this way. This page is about the technique; the [Fiat-Shamir heuristic](/fiat-shamir-heuristic/) page covers the plain transform.

## In plain words

A signer wants to prove it knows a secret, without showing it. It picks a large random mask, sends a fingerprint of it, gets a challenge, and answers with the mask plus the secret times the challenge.

With whole numbers, the answer is not perfectly hidden: on average it sits a little toward the secret. After many signatures, an attacker could average them and find the secret.

So the signer looks at each answer before it sends it. If the answer falls in a place that would show where the center is, the signer throws it away and starts again with a new mask. It keeps answers with exactly the right probabilities, so that the answers it sends follow one fixed pattern that has nothing to do with the secret. On average it needs only a few tries.

## When it applies

The technique applies when:

- there is a linear one-way function $f(x) = A x \bmod q$ on short vectors, and the secret is a short $S$ with public $T = A S$, so that $A z - T c = A y$ can be checked;
- the response $z = y + S c$ must not leak $S$, and the mask $y$ cannot be uniform over the whole group, because the response must stay short for the one-wayness to hold;
- one can find a mask distribution $D_y$ and a target distribution $D_z$ with $D_z(z) \le M \cdot D_y(z - S c)$ for all, or almost all, $z$ and all possible $S c$, for a small $M$.

It does not apply as is when the response must be produced in one try with no repetition, or when the challenge cannot be recomputed from public data. Hash-and-sign signatures with a trapdoor, such as [GPV](/gpv-signature/) and Falcon, solve the same leak problem in another way, with [Gaussian sampling](/gaussian-sampling-over-lattices/) over a lattice.

## The template

The holes are written in angle brackets.

```pseudo id=main
SIGN(sk = S, pk = (A, T = A S), μ)
L1  y ← ⟨MASK⟩                                  ▷ e.g. D_σ^m, or uniform in [−γ, γ]^m
L2  w ← ⟨COMMIT⟩(A y mod q)                      ▷ A y, or only its high bits
L3  c ← H(w, μ) ∈ ⟨CHALLENGES⟩                   ▷ short, e.g. κ entries ±1
L4  z ← y + S c
L5  with probability ⟨ACCEPT⟩(z, S c) return σ = (z, c);  else go to L1

VERIFY(pk, μ, (z, c))
L6  if ‖z‖ > ⟨BOUND⟩, reject
L7  accept iff c = H(⟨COMMIT⟩(A z − T c mod q), μ)
```

The holes are:

- **$\langle \mathrm{MASK} \rangle$ and $\langle \mathrm{ACCEPT} \rangle$** are chosen together. **Gaussian (2012):** $y \leftarrow D_\sigma^m$ and accept with probability $\min\left(1, \frac{D_\sigma^m(z)}{M \cdot D_{\sigma, Sc}^m(z)}\right) = \min\left(1, \frac{1}{M} \exp\frac{-2 \langle z, S c \rangle + \|S c\|^2}{2 \sigma^2}\right)$. With $\sigma = \alpha \cdot T_b$, where $T_b$ bounds $\|S c\|$, the ratio is at most $M = e^{12/\alpha + 1/(2\alpha^2)}$ except with probability $2^{-100}$. **Uniform (2009, and Dilithium):** $y$ uniform in $[-\gamma, \gamma]^m$, and accept exactly when $\|z\|_\infty \le \gamma - \beta$, where $\beta$ bounds $\|S c\|_\infty$. The kept $z$ is uniform in $[-(\gamma - \beta), \gamma - \beta]^m$.
- **$\langle \mathrm{COMMIT} \rangle$.** $A y \bmod q$ itself, or only its high bits, as in Dilithium, which shortens signatures and needs a second rejection condition so that the high bits of $A z - T c$ equal those of $A y$.
- **$\langle \mathrm{CHALLENGES} \rangle$.** A set of short vectors or ring elements with at least $2^{\lambda}$ elements, for example vectors with $\kappa$ entries in $\{-1, 1\}$.
- **$\langle \mathrm{BOUND} \rangle$.** A bound that the target distribution satisfies with overwhelming probability, for example $\eta \sigma \sqrt m$ for the Gaussian.

**Walk-through.** Line L7 works because $A z - T c = A y + A S c - A S c = A y$, so it recomputes the commitment of line L2. Lines L1, L4 and L5 form a rejection sampler: the candidate $z$ has density $D_y(z - S c)$, and each try outputs $z$ with total probability $D_z(z) / M$, whatever $S c$ is. So a try succeeds with probability $1/M$ (minus a negligible amount), the expected number of tries is $M$, and an accepted $z$ has density $D_z$, which does not depend on the secret. With the Gaussian mask, $D_z = D_\sigma^m$, a centered Gaussian. The challenge is derived after $y$, as in Fiat-Shamir, so the full signature can be simulated by picking $z$ from $D_z$ and $c$ at random and programming the hash; the same lemma also bounds what the aborted tries reveal, since they are never output.

**A toy run.** The code takes $q = 8380417$, $\alpha = 12$ and $\eta = 2$, so $M = e^{1 + 1/288} \approx 2.728$. For one coordinate with $S c = 3$, so $T_b = 3$ and $\sigma = 36$, the acceptance probability is $1/e \approx 0.368$ at $z = 0$, $0.292$ at $z = 100$, and $0.464$ at $z = -100$: the rule removes the bias toward $+3$. Over 1500 signatures with $n = 2$, $m = 8$, $k = 4$, $\kappa = 2$, the tests measure a mean number of tries within 0.25 of $M$. **The leak test** uses $m = 4$, $k = 2$ and $\kappa = 1$, so $c = \pm e_i$ and $z = y \pm s_i$. From 60000 responses without line L5, the least squares estimate $E[z c^\mathsf{T}] E[c c^\mathsf{T}]^{-1}$ rounds to $S$ exactly. With line L5, every entry of the estimate rounds to 0 and stays within five standard errors of 0.

## Classic examples

- **Lyubashevsky (2009).** The first version, over ideal lattices, with a uniform mask in a box and the abort rule $\|z\|_\infty \le \gamma - \beta$.
- **Lyubashevsky (2012).** The Gaussian mask and the rejection rule above, with security from SIS; the template's toy run follows it.
- **BLISS** (Ducas, Durmus, Lepoint and Lyubashevsky, 2013). A bimodal Gaussian: $z = y + b S c$ with a random sign $b$, which lets $M$ be much smaller for the same $\sigma$.
- **[ML-DSA (Dilithium)](/crystals-dilithium/).** A uniform mask over module lattices, a commitment to high bits, and rejection on $\|z\|_\infty$ and on the low bits, standardized in FIPS 204.
- **Other proofs of knowledge.** Lattice [zero-knowledge proofs](/zero-knowledge-proof/) and [sigma protocols](/sigma-protocol/) for commitments, ring signatures and group signatures use the same rejection step.

## Variations

- **Gaussian versus uniform masks.** Gaussians give shorter signatures but need a careful sampler; uniform masks are easy to make constant time, as in Dilithium.
- **Bimodal and other target distributions.** BLISS uses two modes; later work uses masks from other distributions to lower $M$ or to avoid Gaussians.
- **Commit to high bits.** Dilithium hashes only the high bits of $A y$ and sends a hint, which shrinks the public key and the signature.
- **Deterministic or hedged signing.** The randomness of $y$ is derived from the key and the message (and possibly fresh randomness), so a bad random number generator cannot reveal $S$.
- **Proofs.** The ROM proof uses the [forking lemma](/forking-lemma/). Kiltz, Lyubashevsky and Schaffner (2018) gave a QROM proof via lossy identification. In 2023 Devevey, Fallahpour, Passelègue and Stehlé, and independently Barbosa and others, pointed out gaps in the earlier treatments of the aborts and gave corrected proofs.

## Pitfalls

- **Skipping or weakening the rejection.** Without line L5, or with a wrong acceptance probability, the responses are biased toward $S c$, and averaging recovers $S$; the leak test shows it with a least squares estimate.
- **Leaking the aborts.** The number of tries and the aborted values must not leak. A timing side channel that shows why a try was rejected, or the value of $y$, can reveal $S$.
- **Reusing a mask.** Two signatures with the same $y$ and different $c$ give $z - z' = S (c - c')$, which reveals $S$ directly. Derive $y$ from fresh or message-dependent randomness.
- **$\sigma$ or $\gamma$ too small.** Then $M$ is large or the inequality $D_z \le M D_y$ fails for many $z$, and the output is no longer independent of $S$.
- **Cutting the loop.** Signers with a fixed limit on the number of tries must handle the failure without bias, for example by restarting with new randomness; the rare long loops are expected.

## Exercises

1. Prove the rejection sampling lemma: if $D_z(z) \le M D_y(z - v)$ for all $z$, then lines L1, L4 and L5 output $z$ with density $D_z$, for every $v$, after $M$ tries on average.
2. For the uniform mask in $[-\gamma, \gamma]^m$ and the rule $\|z\|_\infty \le \gamma - \beta$, compute the success probability of one try and show that it is about $e^{-m \beta / \gamma}$.
3. Show that for $\sigma = \alpha \|v\|$, $\frac{D_\sigma^m(z)}{D_{\sigma, v}^m(z)} = \exp\frac{-2 \langle z, v \rangle + \|v\|^2}{2\sigma^2}$, and bound it by $e^{12/\alpha + 1/(2\alpha^2)}$ when $|\langle z, v \rangle| \le 12 \sigma \|v\|$.
4. Two signatures share the same $y$. Show how to compute $S c$ for a known $c$, and then $S$ from enough such pairs.
5. Explain why the challenge must be computed from $w$ and $\mu$ after $y$ is chosen, and what goes wrong if the signer picks $c$ first.

## References
