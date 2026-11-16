---
tag: S793VW
kind: definition
slug: polynomial-kernel
name: Polynomial kernel
aliases:
- poly kernel
area: complexity/parameterized-complexity
level: advanced
summary: "A kernel whose output has size at most a polynomial in the parameter k. Every FPT problem has a kernel, but many have no polynomial one unless NP is a subset of coNP/poly."
prereqs: [kernel, kernelization]
see_also: [buss-kernel, kernel-lower-bounds, cross-composition, polynomial-compression, polynomial-parameter-transformation, nemhauser-trotter-theorem, sunflower-lemma, p-poly]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 2, Kernelization (polynomial and linear kernels); Chapter 15, Lower bounds for kernelization
  - paper: doi:10.1016/j.jcss.2009.04.001
    title: "Hans L. Bodlaender, Rodney G. Downey, Michael R. Fellows and Danny Hermelin, On problems without polynomial kernels, Journal of Computer and System Sciences 75(8), 423-434 (2009)"
    locator: the composition framework; k-path and problems parameterized by treewidth have no polynomial kernel
  - paper: doi:10.1145/2629620
    title: "Holger Dell and Dieter van Melkebeek, Satisfiability allows no nontrivial sparsification unless the polynomial-time hierarchy collapses, Journal of the ACM 61(4), article 23 (2014)"
    locator: the bound of O(k^(2-e)) bits for vertex cover kernels and compressions
  - paper: doi:10.1016/0304-3975(83)90020-8
    title: "Chee K. Yap, Some consequences of non-uniform conditions on uniform classes, Theoretical Computer Science 26(3), 287-300 (1983)"
    locator: NP is a subset of coNP/poly implies a collapse of the polynomial hierarchy to its third level
  - paper: doi:10.1006/jagm.2001.1186
    title: "Jianer Chen, Iyad A. Kanj and Weijia Jia, Vertex cover: further observations and further improvements, Journal of Algorithms 41(2), 280-301 (2001)"
    locator: the kernel with at most 2k vertices
---

A polynomial kernel for a [parameterized problem](/parameterized-problem/) is a [kernel](/kernel/) whose output size is bounded by a polynomial in the parameter: it maps $(x, k)$ in polynomial time to an equivalent $(x', k')$ with $|x'| + k' \le g(k)$ and $g(k) = k^{O(1)}$. Every decidable [fixed-parameter tractable](/fixed-parameter-tractable/) problem has a kernel, but the general construction gives a size that is as large as the running time $f(k)$, which is usually exponential. A polynomial kernel is a stronger property. Vertex cover has one, with $O(k^2)$ edges, but k-path has none unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$, although both problems are FPT. So the existence of a polynomial kernel splits the class FPT, and the tools that show the split are the [kernel lower bounds](/kernel-lower-bounds/).

## Definition

Let $L \subseteq \Sigma^* \times \mathbb{N}$ be a parameterized problem. A *polynomial kernel* for $L$ is a kernelization for $L$ whose size function $g$ satisfies $g(k) \le c \cdot k^{d}$ for constants $c$ and $d$ and all $k \ge 1$. The kernel is *linear* if $d = 1$ and *quadratic* if $d = 2$.

The size counts the length of the encoding of $x'$. Graph kernels are often stated as a number of vertices or edges. A bound of $p(k)$ vertices gives at most $p(k)^2$ bits for an adjacency matrix, so "polynomial" does not depend on the unit. "Linear" does: a kernel with $2k$ vertices is linear in vertices but may need $\Theta(k^2)$ bits.

The lower bounds use a weaker object. A *polynomial compression* of $L$ into a language $R$ maps $(x, k)$ in polynomial time to a string $y$ with $|y| \le k^{O(1)}$ such that $(x, k) \in L$ if and only if $y \in R$. A polynomial kernel is a polynomial compression into $L$ itself, so a proof that no polynomial compression exists also rules out polynomial kernels.

## Examples and non-examples

Polynomial kernels for [vertex cover](/parameterized-vertex-cover/) with the cover size $k$, and their sizes for $k = 10$:

| kernel | vertices | edges | vertices for $k = 10$ |
|---|---|---|---|
| [Buss kernel](/buss-kernel/) | $k^2 + k$ | $k^2$ | 110 |
| [crown reduction](/crown-reduction/) | $3k$ | $O(k^2)$ | 30 |
| [LP kernel](/lp-kernelization/) of Chen, Kanj and Jia | $2k$ | $O(k^2)$ | 20 |

All three are quadratic in bits. Dell and van Melkebeek proved that vertex cover has no kernel, and no compression into any language, of $O(k^{2 - \varepsilon})$ bits for a constant $\varepsilon > 0$, unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$. Since $O(k^{2-\varepsilon})$ edges take $O(k^{2-\varepsilon} \log k)$ bits, this also rules out kernels with $O(k^{2 - \varepsilon})$ edges.

Other problems with a polynomial kernel:

- [d-Hitting set](/parameterized-hitting-set/), with $O(d!\,k^d)$ sets by the [sunflower lemma](/sunflower-lemma/).
- [Feedback vertex set](/parameterized-feedback-vertex-set/), with $O(k^2)$ vertices.
- [Cluster editing](/cluster-editing/), with $O(k)$ vertices.

FPT problems with no polynomial kernel unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$:

- k-path, which asks for a simple path on $k$ vertices. Bodlaender, Downey, Fellows and Hermelin showed this with an OR-composition: many instances with the same $k$ combine into one instance whose answer is the OR of theirs, by taking the disjoint union of the graphs.
- Vertex cover with the [treewidth](/treewidth/) as the parameter, and many other problems parameterized by treewidth, by the same paper.

The assumption $\mathrm{NP} \not\subseteq \mathrm{coNP/poly}$ is standard because its failure has a strong consequence: by a result of Yap (1983), $\mathrm{NP} \subseteq \mathrm{coNP/poly}$ implies that the [polynomial hierarchy](/polynomial-hierarchy/) collapses to its third level. See [P/poly](/p-poly/) for advice classes.

Non-examples:

- The kernel from the general proof that FPT problems have kernels. For vertex cover with the $O(2^k (n + m))$ algorithm, it has size about $2^k$, which is not polynomial, although vertex cover also has a polynomial kernel.
- [p-Clique](/parameterized-clique/) has no kernel of any size unless $\mathrm{FPT} = \mathrm{W[1]}$, so it has no polynomial kernel either. This is a different reason from the one for k-path.
- A map to an instance with $k^2$ vertices that takes time $2^k n$. A kernel must run in polynomial time.

## Related definitions

- [Kernel](/kernel/) is the general notion, and [kernelization](/kernelization/) is the technique to build one.
- [Kernel lower bounds](/kernel-lower-bounds/) and [cross-composition](/cross-composition/) prove that no polynomial kernel exists under $\mathrm{NP} \not\subseteq \mathrm{coNP/poly}$.
- A [polynomial parameter transformation](/polynomial-parameter-transformation/) from $A$ to $B$ moves a lower bound from $A$ to $B$. It also moves a polynomial kernel from $B$ to $A$ when the classical form of $B$ is in NP and that of $A$ is NP-hard.
- A [polynomial compression](/polynomial-compression/) is the weaker object that the lower bounds actually rule out.

## References
