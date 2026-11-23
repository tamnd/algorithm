---
tag: 573MEV
kind: theorem
slug: post-processing-theorem
name: Post-processing theorem
aliases:
- closure under post-processing
area: security-and-privacy/differential-privacy
level: intro
summary: "Any function applied to the output of a differentially private algorithm, without access to the data, is private with the same parameters."
prereqs: [differential-privacy-definition, approximate-differential-privacy]
see_also: [sequential-composition-theorem, group-privacy-theorem, randomized-response, laplace-mechanism, binary-tree-mechanism, renyi-differential-privacy, convex-combination, total-variation-distance]
sources:
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), 2014, pages 211 to 407"
    locator: "Section 2.3, Proposition 2.1 (post-processing) with its proof, and Section 2.3.1 (its use in the economic view of the guarantee)"
  - paper: doi:10.1109/CSF.2017.11
    title: "Ilya Mironov, Renyi differential privacy, IEEE 30th Computer Security Foundations Symposium (CSF 2017), pages 263 to 275"
    locator: the post-processing property of Renyi differential privacy
---

The post-processing theorem says that differential privacy cannot be lost by computation on the output alone. If a mechanism $M$ is $(\varepsilon, \delta)$-differentially private, then $g(M(x))$ is $(\varepsilon, \delta)$-DP for every map $g$, deterministic or randomized, that does not read the data. So an analyst who sees a private release can round it, clean it, fit a model to it or publish any function of it, and the privacy guarantee stays the same. Dwork and Roth (2014) state it as Proposition 2.1. It is the reason a private release can be treated as public from then on.

## Statement

**Theorem (post-processing; Dwork-Roth Proposition 2.1).** Fix a neighbor relation $\sim$ (add/remove or replace). Let $M$ be a mechanism with outputs in a set $\mathcal Y$ that is $(\varepsilon, \delta)$-[differentially private](/approximate-differential-privacy/) under $\sim$, with $\varepsilon \ge 0$ and $0 \le \delta < 1$. Let $g$ be a randomized map from $\mathcal Y$ to a set $\mathcal Z$, given as $g(y) = G(y, \omega)$, where $G$ is a fixed function and $\omega$ is a random value that is independent of the data and of the coins of $M$. Then the mechanism $x \mapsto g(M(x))$ is $(\varepsilon, \delta)$-DP under $\sim$.

The case $\delta = 0$ gives the same statement for pure [$\varepsilon$-DP](/differential-privacy-definition/). The map $g$ may depend on any public information that was fixed before the data were read. It may not read $x$, and it may not see the internal coins of $M$, such as the noise that $M$ added.

## In plain words

A private output is a noisy picture of the data. Whatever you do with the picture alone, you cannot make it sharper than it is. Any question about the processed output is also a question about the original output: "is $g(y)$ in $S$?" is the question "is $y$ in the set of values that $g$ sends into $S$?". The original output passed every such question with the bound $e^{\varepsilon}$ and $\delta$, so the processed output passes them too. Extra coins in $g$ do not help, because they do not depend on the data.

## Proof

Fix neighbors $x \sim x'$ and a set $S \subseteq \mathcal Z$.

*Deterministic maps.* First let $g$ be a fixed function, and let $T = \{y \in \mathcal Y : g(y) \in S\}$. Then $g(M(x)) \in S$ exactly when $M(x) \in T$, so

$$\Pr[g(M(x)) \in S] = \Pr[M(x) \in T] \le e^{\varepsilon}\Pr[M(x') \in T] + \delta = e^{\varepsilon}\Pr[g(M(x')) \in S] + \delta.$$

The inequality is the definition of $(\varepsilon, \delta)$-DP for the set $T$.

*Randomized maps.* For each fixed value $w$ of $\omega$, the map $g_w(y) = G(y, w)$ is deterministic, so the first part gives $\Pr[g_w(M(x)) \in S] \le e^{\varepsilon}\Pr[g_w(M(x')) \in S] + \delta$. The value $\omega$ is independent of the coins of $M$, so $\Pr[g(M(x)) \in S] = \mathbb E_\omega\big[\Pr[g_\omega(M(x)) \in S]\big]$, and the same for $x'$. Taking the expectation of the inequality over $\omega$, and using that expectation is linear and keeps the order, gives

$$\Pr[g(M(x)) \in S] \le e^{\varepsilon}\Pr[g(M(x')) \in S] + \delta.$$

This holds for all $x \sim x'$ and all $S$, which is the claim. $\square$

The second part is the argument of Dwork and Roth: a randomized map is a [convex combination](/convex-combination/) of deterministic maps, and the bound is kept by convex combinations because both sides are linear in the mixing weights. (For general output spaces, $G$ and $S$ must be measurable, so that $T$ is an event.)

## Consequences

- **Cleaning a release is free.** Rounding a noisy count to an integer, clamping it at 0, or making a noisy [histogram](/histogram/) consistent with known totals keeps the same $(\varepsilon, \delta)$. The [binary tree mechanism](/binary-tree-mechanism/) uses this to turn noisy tree nodes into prefix sums.
- **Derived statistics are free.** From a noisy sum $\tilde s$ and a noisy count $\tilde n$, released together with a total budget $\varepsilon$, the ratio $\tilde s/\tilde n$ is a private mean at no extra cost.
- **Models and synthetic data.** A model trained only on a private release, or on private synthetic data, is private with the parameters of the release.
- **Randomized response, processed.** [Randomized response](/randomized-response/) with truth probability $3/4$ is $\ln 3$-DP. If the analyst flips each answer again with probability $1/4$, the answer is true with probability $\frac34 \cdot \frac34 + \frac14 \cdot \frac14 = 0.625$, which is $\ln(0.625/0.375) = \ln(5/3) = 0.510826$-DP. The theorem only promises $\ln 3 = 1.098612$; processing can make the guarantee better, never worse.
- **Other definitions.** The same closure holds for the profile $\delta(\varepsilon)$ at each $\varepsilon$, and for [Renyi DP](/renyi-differential-privacy/), [zero-concentrated DP](/zero-concentrated-differential-privacy/) and [Gaussian DP](/gaussian-differential-privacy/), where it follows from the data processing inequality of the divergence that each uses.
- **The economic view.** For any future event that depends only on the output, the probability changes by at most the factor $e^{\varepsilon}$ when one record is added or removed. Dwork and Roth (Section 2.3.1) use the theorem in this form to argue that a person loses little by joining a dataset.

## Tightness

The parameters cannot be improved in general: when $g$ is the identity, $g(M(x)) = M(x)$, and the bound is exactly that of $M$. The [Laplace mechanism](/laplace-mechanism/) on a count reaches its $\varepsilon$ exactly, so the identity post-processing of it reaches $\varepsilon$ too.

The hypotheses are needed.

- **The map must not read the data.** Let $M(x) = c(x) + Z$ be a Laplace count, and let $g(y, x) = c(x)$. Then $g$ releases the exact count, which is not DP for any $\varepsilon$. Any step that uses the data again, such as a second query, is not post-processing; it is covered by the [sequential composition theorem](/sequential-composition-theorem/) and costs budget.
- **The map must not see the coins of $M$.** If $g$ knows the noise $Z$, it computes $y - Z = c(x)$. A system that logs the noise next to the release breaks privacy, although the formula for the release is private.
- **Side information that depends on the data.** If $g$ uses a second dataset that shares records with $x$, the result is a joint release of two functions of the data, and the theorem does not apply.

## History

The closure under post-processing is built into the definition of Dwork, McSherry, Nissim and Smith (2006): the bound holds for every set of outputs, and the proof above uses nothing else. Dwork and Roth (2014) state it as Proposition 2.1 for $(\varepsilon, \delta)$-DP and randomized maps, with the proof by deterministic maps and convex combinations. Later definitions, such as Renyi DP (Mironov 2017), were chosen so that they keep this property.

## References
