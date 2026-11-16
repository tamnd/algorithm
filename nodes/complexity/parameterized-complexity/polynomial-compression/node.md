---
tag: 9DN17Y
kind: definition
slug: polynomial-compression
name: Polynomial compression
aliases:
- compression
area: complexity/parameterized-complexity
level: research
summary: "A polynomial-time map from an instance with parameter k to a string of size poly(k) in some fixed language, with the same answer. It relaxes a polynomial kernel and is what lower bounds rule out."
prereqs: [polynomial-kernel]
see_also: [kernel-lower-bounds, cross-composition, polynomial-parameter-transformation, kernelization, buss-kernel, nemhauser-trotter-theorem, lossy-kernelization, np]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 15, Lower bounds for kernelization (the definition of compression and its link to kernels)
  - book: isbn:9781107057760
    title: Fedor V. Fomin, Daniel Lokshtanov, Saket Saurabh and Meirav Zehavi, Kernelization, Theory of Parameterized Preprocessing, Cambridge University Press, 2019
    locator: Chapter 17, Framework
  - paper: doi:10.1016/j.jcss.2010.06.007
    title: "Lance Fortnow and Rahul Santhanam, Infeasibility of instance compression and succinct PCPs for NP, Journal of Computer and System Sciences 77(1), 91-106 (2011)"
    locator: instance compression and the distillation theorem
  - paper: doi:10.1145/2629620
    title: "Holger Dell and Dieter van Melkebeek, Satisfiability allows no nontrivial sparsification unless the polynomial-time hierarchy collapses, Journal of the ACM 61(4), article 23 (2014)"
    locator: compression lower bounds of the form O(k^(d-e)) bits
---

A polynomial compression shrinks an instance of a parameterized problem to a string of size polynomial in the parameter, like a [polynomial kernel](/polynomial-kernel/), but the output may belong to any fixed language, not only to the problem itself. It is the weakest form of polynomial preprocessing that the theory of [kernel lower bounds](/kernel-lower-bounds/) can rule out, so those bounds are stated for compressions. For NP-complete problems the two notions are close: a compression into a language in NP gives a polynomial kernel.

## Definition

Let $Q \subseteq \Sigma^* \times \mathbb{N}$ be a parameterized problem and let $R \subseteq \Sigma^*$ be a language. A *compression* of $Q$ into $R$ of size $f$ is an algorithm that takes an instance $(x, k)$, runs in time polynomial in $|x| + k$, and outputs a string $y$ with

- $|y| \le f(k)$, and
- $y \in R$ if and only if $(x, k) \in Q$.

It is a *polynomial compression* if $f$ is a polynomial. The language $R$ is fixed in advance but otherwise arbitrary: it need not be in NP and need not be decidable.

A *kernel* is the special case where $R$ is $Q$ itself: the output is an instance $(x', k')$ of $Q$ with $|x'| + k' \le f(k)$.

**From compression to kernel.** Let $Q$ have a polynomial compression into a language $R \in \mathrm{NP}$, and let the classical form of $Q$, with $k$ written in unary, be NP-hard. Then $Q$ has a polynomial kernel. *Proof.* Compress $(x, k)$ to $y$ with $|y| \le p(k)$. Since $R \in \mathrm{NP}$ and $Q$ is NP-hard, a Karp reduction maps $y$ to an instance $(x', k')$ of $Q$ in time polynomial in $|y|$, so $|x'| + k' \le \mathrm{poly}(p(k))$, with the same answer. The composed map is a polynomial kernel. $\square$

## Examples and non-examples

- **Every polynomial kernel is a polynomial compression.** For [vertex cover](/parameterized-vertex-cover/), the [Buss kernel](/buss-kernel/) leaves at most $k^2$ edges, and the [Nemhauser-Trotter](/nemhauser-trotter-theorem/) kernel leaves at most $2k$ vertices. A graph on $2k$ vertices is written as the upper half of its adjacency matrix with $\binom{2k}{2} = k(2k - 1)$ bits, which is 15 bits for $k = 3$. So vertex cover has a compression with $O(k^2)$ bits.
- **A compression that is not a kernel.** The string above is a bit vector, not a graph with a number, so it is an instance of the language "bit vectors that encode a graph with a vertex cover of size at most $k$" rather than of vertex cover itself. This is the usual reason to state results for compressions: the encoding may be shorter than any instance of $Q$.
- **Sharp size bounds.** Dell and van Melkebeek proved that vertex cover has no compression into any language with $O(k^{2 - \varepsilon})$ bits, unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$. So the $O(k^2)$ bits above are close to the best.
- **No polynomial compression.** k-Path, CNF-SAT parameterized by the number of variables, and treewidth have no polynomial compression unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$; see [cross-composition](/cross-composition/). Each of them is FPT and has a compression of exponential size.
- **No compression at all.** If $Q$ has a compression of any size $f(k)$ into a decidable language $R$, then $Q$ is FPT: compress, then decide $y$ by brute force in time that depends only on $f(k)$. So a W[1]-hard problem such as [clique](/parameterized-clique/) has no compression into a decidable language unless $\mathrm{FPT} = \mathrm{W[1]}$.

## Related definitions

- **Kernel and polynomial kernel.** The case $R = Q$; see [kernelization](/kernelization/).
- **Instance compression.** Harnik and Naor asked whether NP problems can be compressed to a size polynomial in a witness length, for uses in cryptography. Fortnow and Santhanam showed that SAT has no such compression in its number of variables unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$, by their theorem on OR-distillation.
- **OR-distillation.** A map from $t$ instances of size at most $n$ to one string of size $\mathrm{poly}(n)$ that keeps the OR of the answers. A [cross-composition](/cross-composition/) followed by a polynomial compression gives one.
- **Polynomial parameter transformation.** A reduction that keeps the parameter polynomial, so that a polynomial compression of the target gives one for the source; see [polynomial parameter transformation](/polynomial-parameter-transformation/).
- **Approximate compression.** The lossy version keeps a ratio $\alpha$ between solution values instead of the exact answer; see [lossy kernelization](/lossy-kernelization/).

## References
