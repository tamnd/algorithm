---
tag: 7ED47N
kind: concept
slug: np-intermediate
name: NP-intermediate
aliases:
- NPI
area: complexity/complexity-classes
level: advanced
summary: "Problems in NP that are neither in P nor NP-complete. They exist if P is not equal to NP (Ladner), but no natural problem is proved to be one; factoring and graph isomorphism are candidates."
prereqs: [np, np-complete, p-versus-np-problem]
see_also: [ladner-theorem, ladners-theorem, graph-isomorphism-problem, integer-factorization, discrete-logarithm-problem, mahaneys-theorem, schaefer-dichotomy-theorem, csp-dichotomy-theorem]
sources:
  - paper: doi:10.1145/321864.321877
    title: Richard E. Ladner, On the structure of polynomial time reducibility, Journal of the ACM 22(1) (1975), 155 to 171
    locator: existence of NP-intermediate sets and the density of the degrees
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Section 3.3, Ladner's theorem (existence of NP-intermediate problems)
  - paper: doi:10.1145/2897518.2897542
    title: László Babai, Graph isomorphism in quasipolynomial time, Proceedings of the 48th Annual ACM Symposium on Theory of Computing (STOC 2016), 684 to 697
    locator: the main theorem
  - paper: doi:10.1016/0020-0190(87)90232-8
    title: Ravi B. Boppana, Johan Håstad and Stathis Zachos, Does co-NP have short interactive proofs?, Information Processing Letters 25(2) (1987), 127 to 132
    locator: if graph isomorphism is NP-complete, the polynomial hierarchy collapses
  - paper: doi:10.1137/0204018
    title: Vaughan R. Pratt, Every prime has a succinct certificate, SIAM Journal on Computing 4(3) (1975), 214 to 220
    locator: primality is in NP, used for factoring in NP intersect coNP
---

A problem is *NP-intermediate* when it is in [NP](/np/), not in [P](/p/), and not [NP-complete](/np-complete/). The class of such problems is called NPI. If $\mathsf{P} = \mathsf{NP}$, there are none. If $\mathsf{P} \ne \mathsf{NP}$, [Ladner's theorem](/ladner-theorem/) shows that there are infinitely many, but the problems it builds are artificial. No natural problem is known to be NP-intermediate, because a proof would also prove $\mathsf{P} \ne \mathsf{NP}$. [Integer factorization](/integer-factorization/), the [discrete logarithm](/discrete-logarithm-problem/) and [graph isomorphism](/graph-isomorphism-problem/) are the standard candidates.

## In plain words

Problems in NP have answers that are easy to check. Some of them are also easy to solve. Others are the hardest of the group: a fast method for one of them would give fast methods for all. The question is whether anything lies in between, harder than the easy problems but not among the hardest.

If the easy and the hard problems are really different, then there is something in between, and in fact a whole ladder of levels. This is a theorem. But the examples that the theorem gives are made up for the proof. For real problems, such as breaking a number into its prime factors or deciding whether two networks have the same shape, nobody can prove that they are in between, although there is good evidence for it.

## The idea

### Definition and dependence on P versus NP

Use polynomial-time many-one (Karp) reductions. Then

$$\mathsf{NPI} = \mathsf{NP} \setminus (\mathsf{P} \cup \mathsf{NPC}),$$

where NPC is the set of NP-complete languages.

- If $\mathsf{P} = \mathsf{NP}$, every language in P other than $\emptyset$ and $\{0, 1\}^*$ is NP-complete: to reduce $A \in \mathsf{NP} = \mathsf{P}$ to it, decide $A$ and output a fixed yes-instance or a fixed no-instance. So NPI is empty. (The two trivial languages are in P and not NP-complete, because they have no no-instance or no yes-instance to map to.)
- If $\mathsf{P} \ne \mathsf{NP}$, Ladner (1975) proved that NPI is not empty. More strongly, his method gives an infinite chain of languages in NPI, each strictly easier than the one before under polynomial-time reductions. He also proved that the polynomial-time degrees of decidable languages are dense: between any two decidable languages $A <_p B$ there is a third one strictly between them.

So "NPI is not empty" is equivalent to $\mathsf{P} \ne \mathsf{NP}$, and a proof that a specific problem is NP-intermediate would solve the [P versus NP problem](/p-versus-np-problem/).

### The constructed examples

The proof in the textbook of Arora and Barak pads SAT. It takes $\text{SAT}_H = \{ \psi \, 0 \, 1^{n^{H(n)}} : \psi \in \text{SAT}, n = |\psi| \}$ for a slowly growing function $H$ defined by diagonalization against all polynomial-time machines. If $H$ stays bounded, the padding is polynomial and $\text{SAT}_H$ is as hard as SAT. If $H$ grows without limit, the padding is superpolynomial and $\text{SAT}_H$ cannot be NP-complete. The definition of $H$ forces the right behavior. See [Ladner's theorem](/ladner-theorem/) for the full proof, and [the general form](/ladners-theorem/) for the version that works between any two degrees. These languages are defined by simulating machines, and nobody would meet them outside the proof.

### Natural candidates

**Integer factorization.** The decision version "does $N$ have a prime factor at most $k$?" is in $\mathsf{NP} \cap \mathsf{coNP}$: a small divisor proves yes, and the full factorization with [Pratt certificates](/pratt-certificate/) proves no. So it is not NP-complete unless $\mathsf{NP} = \mathsf{coNP}$ ([good characterization](/good-characterization/)). The fastest known classical algorithm, the [general number field sieve](/general-number-field-sieve/), has a heuristic running time of $\exp(O((\log N)^{1/3} (\log \log N)^{2/3}))$, which is superpolynomial in the bit length of $N$. Shor's algorithm factors in polynomial time on a quantum computer ([factoring in BQP](/factoring-in-bqp/)).

**Discrete logarithm.** The same kind of argument places a decision version of the [discrete logarithm problem](/discrete-logarithm-problem/) in $\mathsf{NP} \cap \mathsf{coNP}$. It is also solved by Shor's quantum algorithm and has no known classical polynomial-time algorithm.

**Graph isomorphism.** Given two graphs, are they isomorphic? The problem is in NP, with the isomorphism as the certificate ([graph isomorphism in NP](/graph-isomorphism-in-np/)). Two results make NP-completeness unlikely. Boppana, Håstad and Zachos (1987) showed that if graph isomorphism is NP-complete, then the [polynomial hierarchy](/polynomial-hierarchy/) collapses to its second level. Babai (2016) gave an algorithm of [quasi-polynomial](/quasi-polynomial-time/) time $\exp((\log n)^{O(1)})$ ([Babai's algorithm](/babai-quasipolynomial-algorithm/)), so an NP-completeness proof would put all of NP in quasi-polynomial time. No polynomial-time algorithm is known either. Problems that are equivalent to graph isomorphism under polynomial-time reductions form their own class ([GI-completeness](/gi-completeness/)).

### Where no intermediate problems exist

For some families of problems, every member is in P or NP-complete. Such a result is a *dichotomy theorem*. Schaefer (1978) proved one for Boolean constraint satisfaction problems: each one is in P (for example [2-SAT](/2-sat/) and [Horn-SAT](/horn-sat/)) or NP-complete ([Schaefer's dichotomy theorem](/schaefer-dichotomy-theorem/)). Bulatov and Zhuk (2017) extended it to constraint satisfaction over every finite domain ([CSP dichotomy theorem](/csp-dichotomy-theorem/)), as conjectured by Feder and Vardi. So any NP-intermediate problem must lie outside these families.

[Mahaney's theorem](/mahaneys-theorem/) gives another restriction: if a sparse language, with only polynomially many strings of each length, is NP-complete, then $\mathsf{P} = \mathsf{NP}$. So if $\mathsf{P} \ne \mathsf{NP}$, every sparse language in $\mathsf{NP} \setminus \mathsf{P}$ is NP-intermediate.

## Examples

**A certificate for graph isomorphism.** Let $G$ have the vertices $1, \ldots, 5$ and the edges $12, 23, 34, 45, 51, 13$, and let $H$ have the edges $14, 42, 25, 53, 31, 23$. Both have the degree sequence $(2, 2, 2, 3, 3)$. The map $1 \mapsto 2$, $2 \mapsto 5$, $3 \mapsto 3$, $4 \mapsto 1$, $5 \mapsto 4$ sends the 6 edges of $G$ to the 6 edges of $H$, so it is a certificate that the graphs are isomorphic. Checking it takes one pass over the edges. Of the $5! = 120$ bijections, exactly 2 are isomorphisms. For a no-answer no short certificate is known in general. The cycle on 6 vertices and two disjoint triangles both have all degrees 2, and none of the $6! = 720$ bijections is an isomorphism. Here connectivity separates them, but simple invariants do not separate all pairs of graphs.

**Padding in Ladner's construction.** A formula $\psi$ of length $n$ becomes $\psi \, 0 \, 1^{n^{h}}$ with $h = H(n)$, of length $n + 1 + n^{h}$. For $n = 10, h = 2$ this is 111. For $n = 100, h = 3$ it is $1{,}000{,}101$. For $n = 1000, h = 4$ it is $1{,}000{,}000{,}001{,}001$. In the construction, $H(n)$ is at most $\log \log n$, which is 4 at $n = 2^{16}$ and 6 at $n = 2^{64}$, so it grows very slowly. This slow growth is what keeps $\text{SAT}_H$ in NP while it escapes both P and NP-completeness.

## Where it is used

The candidates for NP-intermediate problems carry much of public-key cryptography: RSA relies on the hardness of factoring, and Diffie-Hellman key exchange and many signature schemes rely on the discrete logarithm. The quantum algorithms of Shor for these problems are the main reason for post-quantum cryptography, which uses problems such as lattice problems instead. In structural complexity, Ladner's delayed diagonalization is a standard technique, and NP-intermediate problems are the background of dichotomy theorems: such a theorem shows that a whole family of problems has no member in NPI.

## References
