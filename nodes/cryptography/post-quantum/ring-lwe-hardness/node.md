---
tag: N8N5PZ
kind: theorem
slug: ring-lwe-hardness
name: Ring-LWE hardness theorem
aliases:
- LPR reduction
- Lyubashevsky-Peikert-Regev reduction
area: cryptography/post-quantum
level: research
summary: Lyubashevsky, Peikert and Regev 2010. Quantum reduction from approximate SVP on ideal lattices to search Ring-LWE, and search to decision for cyclotomic rings. PRS 2017 covers any ring.
prereqs: [ring-learning-with-errors, regev-lwe-hardness]
see_also: [module-learning-with-errors, approximate-svp, shortest-independent-vectors-problem, principal-ideal-problem, quantum-principal-ideal-algorithm, unit-group, ideal-class-group, dual-lattice]
sources:
  - paper: "Vadim Lyubashevsky, Chris Peikert and Oded Regev, On ideal lattices and learning with errors over rings, Journal of the ACM 60(6), Article 43, 2013"
    locator: Theorem 3.6 (main theorem), Section 4 (Theorem 4.1 and Lemmas 4.2 to 4.4, the quantum reduction to search Ring-LWE in any number field), Section 5 (Theorems 5.1 to 5.3, search to decision for cyclotomic rings)
  - paper: "Vadim Lyubashevsky, Chris Peikert and Oded Regev, On ideal lattices and learning with errors over rings, EUROCRYPT 2010, LNCS 6110, pages 1 to 23"
    locator: the conference version
  - paper: "Chris Peikert, Oded Regev and Noah Stephens-Davidowitz, Pseudorandomness of Ring-LWE for any ring and modulus, STOC 2017"
    locator: the main theorem (a quantum reduction from worst-case ideal lattice problems to decision Ring-LWE in any number field and for any modulus)
  - paper: "Ronald Cramer, Leo Ducas, Chris Peikert and Oded Regev, Recovering short generators of principal ideals in cyclotomic rings, EUROCRYPT 2016"
    locator: the main result (from any generator of a principal ideal with a short generator, recover a short generator in prime-power cyclotomic rings) and its use with a quantum principal ideal algorithm
  - paper: "Ronald Cramer, Leo Ducas and Benjamin Wesolowski, Short Stickelberger class relations and application to Ideal-SVP, EUROCRYPT 2017"
    locator: the main result (a quantum polynomial-time algorithm for approximate SVP on ideal lattices of prime-power cyclotomic fields with factor exp(O~(n^(1/2))))
  - paper: "Adeline Langlois and Damien Stehle, Worst-case to average-case reductions for module lattices, Designs, Codes and Cryptography 75(3), pages 565 to 599, 2015"
    locator: the main theorems (the module analog of the LPR reduction)
  - paper: "Jean-Francois Biasse and Fang Song, Efficient quantum algorithms for computing class groups and unit groups of number fields, SODA 2016"
    locator: the quantum polynomial-time algorithm for the principal ideal problem
  - paper: "Chris Peikert, A decade of lattice cryptography, Foundations and Trends in Theoretical Computer Science 10(4), pages 283 to 424, 2016"
    locator: Section 4.3.4 (ideal lattices, and why GapSVP with polynomial factors is easy on them) and Section 4.4 (Ring-LWE hardness)
---

The Ring-LWE hardness theorem of Lyubashevsky, Peikert and Regev (LPR, 2010) says that an efficient algorithm for [Ring-LWE](/ring-learning-with-errors/) gives an efficient quantum algorithm for approximate [SVP](/approximate-svp/) on every ideal lattice of the ring's number field, and that for cyclotomic rings the decision form is as hard as the search form. It is the ring analog of [Regev's reduction](/regev-lwe-hardness/) and the main evidence for the ring-based schemes. Peikert, Regev and Stephens-Davidowitz (PRS, 2017) extended the decision result to every number field and every modulus.

**Notation.** $K$ is a number field of degree $n$ with ring of integers $R = \mathcal{O}_K$ and dual ideal $R^\vee$; for the $m$-th cyclotomic field, $n = \varphi(m)$. $q$ is the modulus (not a number of queries) and $\alpha \in (0,1)$ the error rate. An ideal lattice is the image of a nonzero fractional ideal $I \subseteq K$ under the canonical embedding $\sigma : K \to \mathbb{R}^n$. $\Upsilon_\alpha$ is the LPR error family: elliptical Gaussians in the canonical embedding whose widths are random and at most about $\alpha$. $D_\xi$ is the spherical Gaussian of parameter $\xi$. R-LWE$_{q,\psi}$ is search Ring-LWE and R-DLWE$_{q,\psi}$ the decision form, with the secret in $R_q^\vee = R^\vee / q R^\vee$.

## Statement

**Theorem (LPR, Theorem 3.6).** Let $K$ be the $m$-th cyclotomic number field of degree $n = \varphi(m)$ and $R = \mathcal{O}_K$. Let $\alpha < \sqrt{\log n / n}$, and let $q \ge 2$, $q \equiv 1 \pmod m$, be a prime bounded by a polynomial in $n$ with $\alpha q \ge \omega(\sqrt{\log n})$. Then there is a polynomial-time quantum reduction from $\tilde O(\sqrt n / \alpha)$-approximate SIVP (or SVP) on ideal lattices in $K$ to R-DLWE$_{q, \Upsilon_\alpha}$. For any $\ell \ge 1$, there is also such a reduction to R-DLWE$_{q, D_\xi}$ given only $\ell$ samples, with $\xi = \alpha \cdot (n\ell / \log(n\ell))^{1/4}$.

It has two parts.

**Part 1 (LPR, Theorem 4.1): worst case to search, any number field.** Let $K$ be any number field of degree $n$, $\alpha \in (0,1)$ and $q \ge 2$ with $\alpha q \ge 2\,\omega(\sqrt{\log n})$. There is a polynomial-time quantum reduction from the discrete Gaussian sampling problem $K$-DGS$_\gamma$ on ideals $I$ of $K$ to search R-LWE$_{q, \Psi_{\le \alpha}}$ (errors from any elliptical Gaussian of widths at most $\alpha$), with

$$\gamma = \max\Bigl\{\eta_\varepsilon(I) \cdot \tfrac{\sqrt 2}{\alpha} \cdot \omega(\sqrt{\log n}),\; \tfrac{\sqrt{2n}}{\lambda_1(I^\vee)}\Bigr\}.$$

**Part 2 (LPR, Theorems 5.1 to 5.3): search to decision, cyclotomic rings.** For the $m$-th cyclotomic ring, a prime $q \equiv 1 \pmod m$ of polynomial size, and the error family above, search R-LWE reduces to decision R-DLWE in polynomial time, classically.

**Theorem (PRS 2017, informal).** For every number field $K$ and every modulus $q \ge 2$, there is a polynomial-time quantum reduction from approximate SIVP on ideal lattices of $K$, with a polynomial factor, directly to decision Ring-LWE over $\mathcal{O}_K$ with a suitable Gaussian error (whose width is a polynomial fraction of $q$). It needs no search to decision step and no condition that $q$ splits.

## In plain words

If someone can solve the ring form of the noisy equation problem, then a quantum computer can find fairly short vectors in any lattice that comes from an ideal of the ring. The proof follows Regev's plan for plain lattices, step by step, with ring multiplication in place of inner products.

The second part shows that telling ring samples apart from random ones is as hard as finding the secret. The ring splits into many small pieces, and the symmetries of the ring move each piece to every other piece, so an attacker who could guess one piece could guess them all.

The hard problem behind the theorem is about special lattices with symmetry. Quantum attacks on those lattices are known for very large approximation factors, but they do not reach the small factors that the theorem uses, and they do not break the schemes.

## Proof

This is an outline; the complete proofs are LPR Sections 4 and 5.

**Part 1.** The plan is that of [Regev's reduction](/regev-lwe-hardness/): start from wide discrete Gaussian samples on the ideal lattice $I$, which LLL provides, and make them narrower step by step. One step (Lemma 4.2) has two halves.

- *Classical half (Lemma 4.3).* Given polynomially many samples from $D_{I,r}$ and a search R-LWE oracle, solve BDD on the dual ideal $I^\vee$ with distance about $\alpha q / (\sqrt 2\, r)$. For a target $x = v + u$ with $v \in I^\vee$, each sample $y \in I$ gives a pair $(a, b)$ where $a$ is $y$ mapped into $R_q$ by a fixed isomorphism $I / qI \cong R / qR$, and $b$ comes from the ring product $x \cdot y$ instead of an inner product. The product $v \cdot y$ lies in $I^\vee I \subseteq R^\vee$ and gives the term $a \cdot s$ with $s$ determined by $v \bmod qI^\vee$. The product $u \cdot y$ is the error. In the canonical embedding, coordinate $j$ of $u \cdot y$ is $\sigma_j(u)\, \sigma_j(y)$, a Gaussian whose width is proportional to $|\sigma_j(u)|$. So the error is an elliptical Gaussian with widths that depend on the unknown $u$, and only their maximum is bounded. This is why the theorem uses the family $\Psi_{\le\alpha}$ and not one fixed Gaussian.
- *Quantum half (Lemma 4.4).* A BDD solver on $I^\vee$ gives, with the [quantum Fourier transform](/quantum-fourier-transform/), samples from $D_{I, r'}$ with $r' = r \cdot \omega(\sqrt{\log n}) / (\alpha q)$ smaller than $r$. The argument is Regev's, applied to the lattice $\sigma(I)$.

Iterating until the width is near $\eta_\varepsilon(I) \sqrt 2\, \omega(\sqrt{\log n}) / \alpha$ gives $K$-DGS$_\gamma$. Short Gaussian samples give SIVP on $I$ within the stated factor. In a cyclotomic field, multiplying a shortest nonzero $v \in I$ by $1, \zeta, \ldots, \zeta^{n-1}$ gives $n$ linearly independent vectors of the same length in the canonical embedding, so $\lambda_n(I) = \lambda_1(I)$ and SIVP and SVP on ideal lattices are the same problem.

**Part 2.** Let $q \equiv 1 \pmod m$ be prime. Then $q R$ splits into $n$ distinct prime ideals $\mathfrak q_1, \ldots, \mathfrak q_n$, each with $R / \mathfrak q_i \cong \mathbb{Z}_q$, and by the Chinese remainder theorem $R_q^\vee \cong \bigoplus_i R^\vee / \mathfrak q_i R^\vee$.

1. *Guess one component.* To test a guess $g$ for $s \bmod \mathfrak q_i$, change each sample so that, if $g$ is right, the result is still Ring-LWE, and if $g$ is wrong, the component $i$ of $b$ becomes uniform. The oracle that tells "uniform on components $1, \ldots, i$" from "uniform on components $1, \ldots, i-1$" detects the difference. There are $q$ guesses per component, a polynomial number.
2. *Hybrid argument.* A decision oracle for R-DLWE tells real samples from fully uniform ones. A hybrid over the $n$ components gives some index $i$ at which the oracle tells the hybrids $i-1$ and $i$ apart with non-negligible advantage.
3. *Automorphisms.* The Galois group of the cyclotomic field acts transitively on the $\mathfrak q_i$. An automorphism $\tau$ maps a sample for $s$ to a sample for $\tau(s)$ and keeps the error family $\Upsilon_\alpha$ the same, because it only permutes the coordinates of the canonical embedding. So the oracle for one index $i$ serves every component: apply $\tau$, guess, and undo $\tau$.
4. *Fixed and random error shapes.* Part 1 produces samples with one fixed elliptical error, while the decision oracle is only promised to work on average over $\Upsilon_\alpha$. The reduction adds extra Gaussian noise with random widths, so that the oracle sees errors from (close to) $\Upsilon_\alpha$.

Combining Parts 1 and 2 gives Theorem 3.6. The statement for $\ell$ samples of a spherical error $D_\xi$ uses a separate argument in LPR that turns $\ell$ samples into samples with a wider spherical error.

**PRS.** Peikert, Regev and Stephens-Davidowitz avoid the search to decision step. Their classical half uses the decision oracle directly, through a problem they call the oracle hidden center problem: the decision oracle's acceptance probability, as a function of a perturbation of the target, reveals the hidden lattice point. The same iteration then applies. Because no splitting of $q$ and no automorphism is needed, the result holds for every number field and every modulus.

## Consequences

- **Ring-based schemes rest on worst-case problems.** Every scheme proved secure from decision Ring-LWE over a cyclotomic ring, or over any ring with PRS, is secure unless approximate SIVP on ideal lattices with polynomial factors has an efficient quantum algorithm.
- **The pattern extends to modules.** Langlois and Stehlé proved the analog for Module-LWE, from module lattices (see [Module-LWE](/module-learning-with-errors/)).
- **No concrete parameters.** As for plain LWE, the reductions lose polynomial factors and say nothing about the bit security of a parameter set; schemes use the [core-SVP](/core-svp-hardness/) estimates of the attacks on the LWE form.

## Tightness

- **GapSVP is not the right worst-case problem here.** In an ideal lattice of a cyclotomic field, $\lambda_1(I)$ is fixed within a factor of about $\sqrt n$ by $\det(I)$, so GapSVP$_\gamma$ for $\gamma$ a small polynomial is easy on ideal lattices (Peikert's survey, Section 4.3.4). This is why the theorems start from SVP and SIVP, which are search problems.
- **Ideal-SVP is an open question.** Ideal lattices have structure that general lattices lack, and quantum algorithms use it for some factors.
  - Cramer, Ducas, Peikert and Regev (2016) showed that in prime-power cyclotomic rings, a short generator of a principal ideal can be recovered from any generator, using the [unit group](/unit-group/) structure. With the quantum polynomial-time algorithm for the [principal ideal problem](/principal-ideal-problem/) of Biasse and Song (2016) (see [quantum principal ideal algorithm](/quantum-principal-ideal-algorithm/)), this breaks in quantum polynomial time some schemes that relied on a short generator of a principal ideal being hard to find.
  - Cramer, Ducas and Wesolowski (2017) extended this to all ideals, using relations in the [class group](/ideal-class-group/): in prime-power cyclotomic fields, a quantum polynomial-time algorithm finds vectors within a factor $\exp(\tilde O(\sqrt n))$ of the shortest in any ideal lattice. For general lattices, BKZ needs time about $\exp(\tilde O(\sqrt n))$ to reach such a factor.
- **These attacks do not break Ring-LWE as used.** The factor $\exp(\tilde O(\sqrt n))$ is far larger than the polynomial factor $\tilde O(\sqrt n/\alpha)$ in the LPR theorem, so the attacks do not solve the worst-case problem that the theorem reduces from. The reduction also goes one way only: an algorithm for ideal-SVP, even with small factors, is not known to solve Ring-LWE, so Ring-LWE could stay hard even if ideal-SVP became easy. Schemes such as ML-KEM, which use Module-LWE, are a further step away. What the attacks do show is that the worst-case assumption on ideal lattices is less safe than the one on general lattices, for some factors.
- **Ring-LWE versus LWE.** No reduction from LWE to Ring-LWE is known, so the ring problem could in principle be easier than plain LWE, even though no attack shows this.

## History

Lyubashevsky, Peikert and Regev defined Ring-LWE and proved this theorem at EUROCRYPT 2010, with the journal version in 2013. Langlois and Stehlé gave the module version in 2015. Cramer, Ducas, Peikert and Regev (EUROCRYPT 2016) and Cramer, Ducas and Wesolowski (EUROCRYPT 2017) found the quantum attacks on short generators and on ideal-SVP. Peikert, Regev and Stephens-Davidowitz proved the decision result for all rings and moduli at STOC 2017.

## References
