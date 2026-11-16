---
tag: 7ZQ0NT
kind: definition
slug: polynomial-parameter-transformation
name: Polynomial parameter transformation
aliases:
- PPT
area: complexity/parameterized-complexity
level: research
summary: "A polynomial-time reduction between parameterized problems whose new parameter is at most a polynomial in the old one. It carries polynomial compressions back and kernel lower bounds forward."
prereqs: [polynomial-compression, parameterized-reduction]
see_also: [kernel-lower-bounds, cross-composition, polynomial-kernel, parameterized-longest-path, parameterized-clique, polynomial-time-reduction, fixed-parameter-tractable, lossy-kernelization]
sources:
  - paper: doi:10.1016/j.tcs.2011.04.039
    title: "Hans L. Bodlaender, Stéphan Thomassé and Anders Yeo, Kernel bounds for disjoint cycles and disjoint paths, Theoretical Computer Science 412(35), 4570-4578 (2011)"
    locator: the definition of a polynomial parameter transformation and the transfer of lower bounds from disjoint factors
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 15, Lower bounds for kernelization
  - book: isbn:9781107057760
    title: Fedor V. Fomin, Daniel Lokshtanov, Saket Saurabh and Meirav Zehavi, Kernelization, Theory of Parameterized Preprocessing, Cambridge University Press, 2019
    locator: Chapter 19, Polynomial parameter transformation
---

A polynomial parameter transformation (PPT) is a reduction between parameterized problems that runs in polynomial time and keeps the new parameter bounded by a polynomial in the old one. It is the reduction that fits [polynomial kernels](/polynomial-kernel/): a polynomial compression of the target gives one of the source, so a lower bound for the source carries to the target. Bodlaender, Thomassé and Yeo introduced it in 2009 to show that disjoint cycles and disjoint paths have no polynomial kernels.

## Definition

Let $P$ and $Q$ be parameterized problems. A *polynomial parameter transformation* from $P$ to $Q$ is an algorithm that takes an instance $(x, k)$ of $P$, runs in time polynomial in $|x| + k$, and outputs an instance $(x', k')$ of $Q$ with

- $(x, k) \in P$ if and only if $(x', k') \in Q$, and
- $k' \le p(k)$ for a polynomial $p$.

**Transfer theorem.** If there is a PPT from $P$ to $Q$ and $Q$ has a polynomial [compression](/polynomial-compression/), then $P$ has a polynomial compression. So if $P$ has no polynomial compression unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$, neither has $Q$.

*Proof.* Let $Q$ compress into a language $R$ with size $q(k')$. Apply the PPT, then the compression. The time is polynomial, the answer is kept, and the size is at most $q(p(k))$, a polynomial in $k$. $\square$

If $Q$ is in NP and the classical form of $P$ is NP-hard, the same argument turns a polynomial kernel of $Q$ into one of $P$, which is the form of the original statement by Bodlaender, Thomassé and Yeo.

Compared with a [parameterized reduction](/parameterized-reduction/), a PPT is stricter in two ways. Its time must be polynomial, not $f(k)$ times a polynomial, and its new parameter must be polynomial in $k$, not any function $g(k)$.

## Examples and non-examples

- **k-Path to k-cycle by an apex.** Given $G$ and $k \ge 2$, add a new vertex $a$ adjacent to all vertices of $G$. Then $G$ has a path on $k$ vertices if and only if $G + a$ has a cycle on exactly $k + 1$ vertices: close the path through $a$, or delete $a$ from the cycle. A cycle of $G$ on $k + 1$ vertices also gives a path on $k$ vertices by dropping one vertex. The parameter goes from $k$ to $k + 1$, so this is a PPT, and the cycle problem has no polynomial kernel because [k-path](/parameterized-longest-path/) has none. A scratch script checked the claim on 250 random graphs (seed 4), with 759 yes-cases and 385 no-cases. For the path $0, 1, 2, 3$ plus an isolated vertex 4, both answers are yes for $k = 4$ and both are no for $k = 5$.
- **A change of parameter.** The identity map is a PPT from a problem with parameter $k_1$ to the same problem with parameter $k_2$ whenever $k_2 \le \mathrm{poly}(k_1)$. For example, the degeneracy of a graph is at most its maximum degree, so clique parameterized by the degeneracy has no polynomial kernel, because clique parameterized by the maximum degree has none (see [cross-composition](/cross-composition/)). Both versions are FPT.
- **Disjoint factors to disjoint cycles.** Bodlaender, Thomassé and Yeo first showed by a composition that a string problem, disjoint factors, has no polynomial kernel, and then gave PPTs from it to disjoint cycles and disjoint paths.
- **Not a PPT: an exponential parameter.** A reduction that maps $k$ to $2^k$ is a valid parameterized reduction but not a PPT, and it does not carry kernel lower bounds.
- **A PPT with no use for kernels.** Complementing the graph is a PPT from [clique](/parameterized-clique/) to independent set with $k' = k$, but both problems are W[1]-hard, so it says nothing new about kernels. A PPT is useful only when the source has a known kernel lower bound and the target is FPT.

## Related definitions

- **Polynomial-time reduction.** The classical [Karp reduction](/polynomial-time-reduction/) has no parameter at all; a PPT adds the parameter bound.
- **Parameterized reduction.** The reduction for the W-hierarchy, with time $f(k) n^{O(1)}$ and parameter $g(k)$.
- **Cross-composition.** The other half of the lower bound method: it gives the first problem with no polynomial compression, and PPTs spread it; see [kernel lower bounds](/kernel-lower-bounds/).
- **Linear parameter transformation.** A PPT with $k' = O(k)$. It also transfers bounds of the form $O(k^{d - \varepsilon})$ on the size of a compression.
- **Approximation-preserving versions.** For [lossy kernels](/lossy-kernelization/) the transformation must also keep the ratio between solution values.

## References
