---
tag: 6RMKZK
kind: concept
slug: kernel-lower-bounds
name: Kernel lower bounds
aliases:
- kernelization lower bounds
area: complexity/parameterized-complexity
level: research
summary: "Methods that show a parameterized problem has no polynomial kernel, or no kernel below a given size, unless NP is a subset of coNP/poly, which would collapse the polynomial hierarchy."
prereqs: [polynomial-compression, p-poly, co-np]
see_also: [cross-composition, polynomial-parameter-transformation, polynomial-kernel, lossy-kernelization, polynomial-hierarchy, karp-lipton-theorem, parameterized-longest-path, sunflower-lemma]
sources:
  - paper: doi:10.1016/j.jcss.2009.04.001
    title: "Hans L. Bodlaender, Rodney G. Downey, Michael R. Fellows and Danny Hermelin, On problems without polynomial kernels, Journal of Computer and System Sciences 75(8), 423-434 (2009)"
    locator: OR-composition, the k-path example and the AND-conjecture
  - paper: doi:10.1016/j.jcss.2010.06.007
    title: "Lance Fortnow and Rahul Santhanam, Infeasibility of instance compression and succinct PCPs for NP, Journal of Computer and System Sciences 77(1), 91-106 (2011)"
    locator: an OR-distillation of an NP-hard language implies NP is a subset of coNP/poly
  - paper: doi:10.1016/0304-3975(83)90020-8
    title: "Chee K. Yap, Some consequences of non-uniform conditions on uniform classes, Theoretical Computer Science 26(3), 287-300 (1983)"
    locator: NP in coNP/poly implies the collapse of the polynomial hierarchy to its third level
  - paper: doi:10.1137/130927115
    title: "Andrew Drucker, New limits to classical and quantum instance compression, SIAM Journal on Computing 44(5), 1443-1479 (2015)"
    locator: AND-distillation of an NP-hard language also implies NP is a subset of coNP/poly
  - paper: doi:10.1145/2629620
    title: "Holger Dell and Dieter van Melkebeek, Satisfiability allows no nontrivial sparsification unless the polynomial-time hierarchy collapses, Journal of the ACM 61(4), article 23 (2014)"
    locator: polynomial lower bounds, no O(k^(2-e)) bits for vertex cover and no O(k^(d-e)) bits for d-hitting set
  - paper: doi:10.1137/120880240
    title: "Hans L. Bodlaender, Bart M. P. Jansen and Stefan Kratsch, Kernelization lower bounds by cross-composition, SIAM Journal on Discrete Mathematics 28(1), 277-305 (2014)"
    locator: cross-composition, the general form of the framework
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 15, Lower bounds for kernelization
  - book: isbn:9781107057760
    title: Fedor V. Fomin, Daniel Lokshtanov, Saket Saurabh and Meirav Zehavi, Kernelization, Theory of Parameterized Preprocessing, Cambridge University Press, 2019
    locator: Chapters 17 to 20 (the framework, instance selectors, polynomial parameter transformations and polynomial lower bounds)
---

A kernel lower bound shows that a parameterized problem has no [polynomial kernel](/polynomial-kernel/), or no kernel below some polynomial size. Such bounds cannot be unconditional while $\mathrm{P} = \mathrm{NP}$ is open, so they hold *unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$*, which would collapse the [polynomial hierarchy](/polynomial-hierarchy/) to its third level (Yap 1983). The method, built from 2008 to 2012, rests on one theorem of Fortnow and Santhanam and on reductions that pack many instances into one.

## In plain words

A kernel is a fast cleanup step that shrinks an input to a size that depends only on a small number, the parameter. Some problems have small kernels and some seem not to. How can one show that no small kernel exists?

The idea is to take a huge pile of separate inputs and glue them into one input whose answer is "yes" exactly when at least one input in the pile has the answer "yes". The parameter of the glued input stays small. If a small kernel existed, it would shrink the whole pile to a short text that still knows whether some input is a yes. A known theorem says that such strong shrinking of a pile of hard inputs is not possible unless a widely believed claim about complexity classes is false.

## The idea

**OR-distillation.** Let $L$ and $R$ be languages. An *OR-distillation* of $L$ into $R$ is a polynomial-time algorithm that takes strings $x_1, \ldots, x_t$, each of length at most $n$, and outputs one string $y$ with $|y| \le \mathrm{poly}(n)$, a bound that does not depend on $t$, such that $y \in R$ if and only if $x_i \in L$ for some $i$.

**Theorem (Fortnow and Santhanam, 2008).** If an NP-hard language has an OR-distillation into any language $R$, then $\mathrm{NP} \subseteq \mathrm{coNP/poly}$.

**Theorem (Yap, 1983).** If $\mathrm{NP} \subseteq \mathrm{coNP/poly}$, then the polynomial hierarchy collapses to $\Sigma_3^p$. This is a relative of the [Karp-Lipton theorem](/karp-lipton-theorem/), with [P/poly](/p-poly/) replaced by coNP/poly.

**Composition.** Let $Q$ be a parameterized problem. An *OR-composition* of an NP-hard language $L$ into $Q$ is a polynomial-time algorithm that maps $x_1, \ldots, x_t$ of length at most $n$ to one instance $(y, k)$ of $Q$ with $k \le \mathrm{poly}(n + \log t)$, such that $(y, k) \in Q$ if and only if some $x_i \in L$. Bodlaender, Downey, Fellows and Hermelin stated the first form of this, and Bodlaender, Jansen and Kratsch generalized it to [cross-composition](/cross-composition/).

**The main lemma.** If $L$ is NP-hard and OR-composes into $Q$, then $Q$ has no [polynomial compression](/polynomial-compression/), and so no polynomial kernel, unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$.

*Proof.* Assume $Q$ has a compression of size $k^c$ into a language $R$. Given $x_1, \ldots, x_t$ of length at most $n$, first remove the duplicates. There are fewer than $2^{n+1}$ strings of length at most $n$, so now $t < 2^{n+1}$ and $\log t \le n + 1$. Compose, which gives $k \le \mathrm{poly}(n + \log t) = \mathrm{poly}(n)$, and then compress to a string of length $k^c = \mathrm{poly}(n)$. The result is in $R$ exactly when some $x_i \in L$, so it is an OR-distillation of $L$ into $R$. By Fortnow and Santhanam, $\mathrm{NP} \subseteq \mathrm{coNP/poly}$. $\square$

**Transfer.** A [polynomial parameter transformation](/polynomial-parameter-transformation/) from $P$ to $Q$ maps an instance with parameter $k$ to an equivalent one with parameter $\mathrm{poly}(k)$. If $P$ has no polynomial compression, then neither has $Q$. This spreads one lower bound to many problems.

**AND version.** Replace "some $x_i \in L$" by "all $x_i \in L$". Bodlaender et al. conjectured that AND-distillation of an NP-hard language is also impossible, and Drucker (2012) proved that it implies $\mathrm{NP} \subseteq \mathrm{coNP/poly}$ as well. This turned conditional results for AND-compositions into results with the same assumption as the OR case.

**Polynomial lower bounds.** Dell and van Melkebeek refined the method with a communication argument. It shows lower bounds on the exponent of a kernel that exists, such as $O(k^{2 - \varepsilon})$ bits for vertex cover.

## Examples

- **k-Path.** Does $G$ have a simple path on $k$ vertices? The disjoint union $G_1 \cup \cdots \cup G_t$ has such a path if and only if some $G_i$ has one, and the parameter stays $k$. So this is an OR-composition of the NP-hard problem into itself, with $k \le n$, and k-path has no polynomial kernel unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$. For instance, with $k = 4$, take a path on 3 vertices, a star with 3 leaves and a 4-cycle; only the 4-cycle has a path on 4 vertices, and a scratch check confirmed that the union has one. With a triangle in place of the 4-cycle, no graph has one and the union has none. The problem is still FPT, with time $2^{O(k)} n^{O(1)}$, see [parameterized longest path](/parameterized-longest-path/), so it has a kernel of exponential size.
- **Treewidth.** The treewidth of a disjoint union is the largest treewidth of its parts, so "treewidth at most $k$" has an AND-composition. Since Drucker's theorem, it has no polynomial kernel in $k$ unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$. See [treewidth](/treewidth/).
- **CNF-SAT by the number of variables.** Brute force gives a trivial kernel of size $2^n$ in the number $n$ of variables. A cross-composition with selector variables shows that there is no polynomial compression; see [cross-composition](/cross-composition/).
- **Disjoint cycles and disjoint paths.** Bodlaender, Thomassé and Yeo proved these have no polynomial kernels by polynomial parameter transformations from a problem called disjoint factors; see [polynomial parameter transformation](/polynomial-parameter-transformation/).
- **Vertex cover and d-hitting set.** These have polynomial kernels. Dell and van Melkebeek proved that vertex cover has no compression into $O(k^{2 - \varepsilon})$ bits and d-hitting set none into $O(k^{d - \varepsilon})$ bits, so the kernels with $O(k^2)$ edges and the [sunflower](/sunflower-lemma/) kernel with $O(k^d)$ sets are close to the best.

## Where it is used

Kernel lower bounds separate problems with polynomial kernels from those that are FPT but have none. For the second group, research turns to other models of preprocessing. A Turing kernel may call the problem on many small instances, and k-path has polynomial-size Turing kernels on some graph classes. A [lossy kernel](/lossy-kernelization/) gives up exactness, and connected vertex cover, which has no polynomial kernel, has polynomial approximate kernels for every ratio above 1. The same OR-composition idea, with a gap, also rules out lossy kernels for some problems. The books of Cygan et al. (Chapter 15) and Fomin et al. (Chapters 17 to 20) present the theory in full.

## References
