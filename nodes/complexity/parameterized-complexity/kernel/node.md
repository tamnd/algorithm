---
tag: A4GYN4
kind: definition
slug: kernel
name: Kernel (parameterized complexity)
aliases:
- problem kernel
area: complexity/parameterized-complexity
level: core
summary: "A polynomial-time map from (x, k) to an equivalent instance (x', k') whose size and parameter are at most g(k). A decidable problem has one exactly when it is FPT."
prereqs: [fixed-parameter-tractable, polynomial-time]
see_also: [kernelization, polynomial-kernel, buss-kernel, kernel-lower-bounds, crown-reduction, nemhauser-trotter-theorem, polynomial-compression, lossy-kernelization]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 2, Kernelization (the definition of a kernel and Lemma 2.2, kernels exist exactly for decidable FPT problems)
  - book: isbn:9781447155584
    title: Rodney G. Downey and Michael R. Fellows, Fundamentals of Parameterized Complexity, Springer, 2013
    locator: Chapter 4, Kernelization
  - book: isbn:9780198566076
    title: Rolf Niedermeier, Invitation to Fixed-Parameter Algorithms, Oxford University Press, 2006
    locator: Chapter 7, Data reduction and problem kernels
  - paper: "Liming Cai, Jianer Chen, Rodney G. Downey and Michael R. Fellows, Advice classes of parameterized tractability, Annals of Pure and Applied Logic 84(1), 119-138, 1997"
    locator: the equivalence of fixed-parameter tractability and the existence of a kernel
  - paper: doi:10.1016/j.jcss.2009.04.001
    title: "Hans L. Bodlaender, Rodney G. Downey, Michael R. Fellows and Danny Hermelin, On problems without polynomial kernels, Journal of Computer and System Sciences 75(8), 423-434 (2009)"
    locator: the composition framework and the lower bound for k-path
---

A kernel for a [parameterized problem](/parameterized-problem/) is a polynomial-time algorithm that maps each instance $(x, k)$ to an equivalent instance $(x', k')$ whose size is bounded by a function of $k$ alone. The output is also called the kernel, and the bound is the size of the kernel. After the map, any algorithm, even brute force, runs on an instance whose size does not depend on $n$. The word "kernel" has other meanings in mathematics and in operating systems; on this page it means only the problem kernel of parameterized complexity. A kernel is the formal form of preprocessing with a guarantee, and the [kernelization](/kernelization/) page describes how to build one.

## Definition

Let $L \subseteq \Sigma^* \times \mathbb{N}$ be a parameterized problem. A *kernelization* for $L$ is an algorithm $K$ that, given $(x, k)$, runs in time polynomial in $|x| + k$ and returns an instance $(x', k')$ such that:

1. *Equivalence.* $(x, k) \in L$ if and only if $(x', k') \in L$.
2. *Size bound.* $|x'| + k' \le g(k)$ for a computable function $g : \mathbb{N} \to \mathbb{N}$.

The output $(x', k')$ is a *kernel*, and $g$ is the *size* of the kernel. Most texts call the algorithm itself a kernel too.

**The unit of the size.** By the definition, $|x'|$ is the length of the encoding of $x'$, in symbols or bits. For graph problems, papers often state the size as a number of vertices or of edges instead. These units differ. A kernel with $O(k)$ vertices may have $\Theta(k^2)$ edges, and it then needs $\Theta(k^2)$ bits for an adjacency matrix. The [Buss kernel](/buss-kernel/) has at most $k^2 + k$ vertices and $k^2$ edges, which is $O(k^2 \log k)$ bits as an edge list. Lower bounds such as the one of Dell and van Melkebeek count bits, so a claim about a kernel must name its unit.

**Kernels and FPT.** A decidable parameterized problem $L$ has a kernel if and only if it is [fixed-parameter tractable](/fixed-parameter-tractable/). This is due to Cai, Chen, Downey and Fellows (1997), and it is Lemma 2.2 of Cygan et al.

*Proof.* Suppose $L$ has a kernel of size $g$. Let $D$ be any algorithm that decides $L$, and let $T(s)$ be the largest number of steps of $D$ on an input of size at most $s$. The function $T$ is computable, because $D$ halts on every input. To decide $(x, k)$, run the kernel in time $p(|x| + k)$ and then $D$ on the result, in at most $T(g(k))$ steps. The total is $p(|x| + k) + T(g(k))$, which is FPT time.

Now suppose an algorithm $A$ decides $L$ in time $f(k) \cdot n^{c}$. If $L$ is empty or contains every instance, a constant output is a kernel. Otherwise fix a yes-instance $Y$ and a no-instance $N$. Given $(x, k)$ with $n = |x|$, run $A$ for at most $n^{c+1}$ steps. If $A$ stops, return $Y$ or $N$ according to its answer. If it does not stop, then $f(k) \cdot n^{c} > n^{c+1}$, so $n < f(k)$, and we return $(x, k)$ unchanged, whose size is less than $f(k) + k$. The algorithm runs in time $O(n^{c+1})$ and the output has size at most $\max(|Y|, |N|, f(k) + k)$. $\square$

The kernel from this proof has size about $f(k)$, which is exponential for most problems. A kernel of size $k^{O(1)}$ is a [polynomial kernel](/polynomial-kernel/), and many FPT problems do not have one unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$.

## Examples and non-examples

Kernels for [vertex cover](/parameterized-vertex-cover/) with the parameter $k$, the size of the cover:

| kernel | vertices | edges | method |
|---|---|---|---|
| [Buss kernel](/buss-kernel/) | at most $k^2 + k$ | at most $k^2$ | degree rule and a count |
| [crown reduction](/crown-reduction/) | at most $3k$ | $O(k^2)$ | a crown decomposition from a matching |
| [Nemhauser-Trotter](/nemhauser-trotter-theorem/) and [LP kernel](/lp-kernelization/) | at most $2k$ | $O(k^2)$ | a half-integral LP solution |

A worked case of the Buss kernel. Let $G$ have the edges $\{0, i\}$ for $i = 1, \ldots, 6$ and the edges $\{1, 2\}$, $\{3, 4\}$, $\{7, 8\}$ and $\{8, 9\}$, so $G$ has 10 vertices and 10 edges. Take $k = 4$. Vertex 0 has degree $6 > 4$, so every cover of size at most 4 contains it. Remove vertex 0, set $k' = 3$, and remove the isolated vertices 5 and 6. The kernel is the graph with the edges $\{1, 2\}$, $\{3, 4\}$, $\{7, 8\}$, $\{8, 9\}$ and $k' = 3$: 7 vertices and 4 edges, within $k'^2 + k' = 12$ and $k'^2 = 9$. It has the cover $\{1, 3, 8\}$, and adding vertex 0 gives a cover of $G$ of size 4.

A kernel may return an instance that is not a part of the input. When the Buss rules show that the answer is no, the kernel returns a fixed no-instance, such as one edge with $k' = 0$.

Problems with a kernel but no polynomial kernel, unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$:

- k-path, the question of a simple path on $k$ vertices. It is FPT by [color coding](/color-coding/), so it has a kernel, but Bodlaender, Downey, Fellows and Hermelin proved that it has no polynomial kernel under the assumption.
- Vertex cover with the [treewidth](/treewidth/) as the parameter.

Problems with no kernel at all unless $\mathrm{FPT} = \mathrm{W[1]}$: [p-Clique](/parameterized-clique/) and [p-Independent-Set](/parameterized-independent-set/). A kernel would make them FPT by the theorem above.

These are not kernels:

- A map that runs in time $2^k \cdot n$. The map must run in polynomial time.
- A map whose output size is bounded by $k \log n$. The bound must not depend on $n$.
- A map whose output parameter $k'$ is not bounded by a function of $k$. The size bound covers $k'$ too.

## Related definitions

- [Kernelization](/kernelization/) is the technique of building a kernel from reduction rules.
- A [polynomial kernel](/polynomial-kernel/) has $g(k) = k^{O(1)}$.
- A [polynomial compression](/polynomial-compression/) may map into a different problem. [Kernel lower bounds](/kernel-lower-bounds/) rule out polynomial compressions and so polynomial kernels.
- A [lossy kernel](/lossy-kernelization/) keeps an approximation ratio instead of the exact answer.

## References
