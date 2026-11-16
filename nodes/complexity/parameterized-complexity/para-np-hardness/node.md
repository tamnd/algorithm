---
tag: QZEVWB
kind: definition
slug: para-np-hardness
name: para-NP-hardness
aliases:
- PARA-NP-hard
- NP-hard for a constant parameter
area: complexity/parameterized-complexity
level: advanced
summary: "Hardness for para-NP under parameterized reductions. It holds when the problem is NP-hard for one fixed parameter value, and then the problem is not in XP unless P = NP."
prereqs: [parameterized-reduction, xp, np-hard]
see_also: [xp, w-hardness, w-hierarchy, k-coloring, three-coloring, para-l, parameterized-independent-set, np-complete]
sources:
  - book: isbn:9783540299523
    title: Jörg Flum and Martin Grohe, Parameterized Complexity Theory, Springer, 2006
    locator: Chapter 2, Reductions and Parameterized Intractability (the class para-NP, its characterization by precomputation on the parameter, and the slice criterion for para-NP-completeness)
  - paper: "Jörg Flum and Martin Grohe, Describing parameterized complexity classes, Information and Computation 187(2), 291-319 (2003)"
    locator: the classes para-C for a classical class C
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 13, Fixed-parameter intractability (problems that are NP-hard for a constant parameter value, such as coloring)
  - paper: doi:10.1016/0304-3975(76)90059-1
    title: "Michael R. Garey, David S. Johnson and Larry J. Stockmeyer, Some simplified NP-complete graph problems, Theoretical Computer Science 1(3), 237-267 (1976)"
    locator: NP-completeness of 3-coloring of planar graphs and of vertex cover on planar graphs of maximum degree 3
---

A [parameterized problem](/parameterized-problem/) is para-NP-hard if every problem in the class para-NP has a [parameterized reduction](/parameterized-reduction/) to it. The usual way to prove it is to find one value of the parameter for which the problem is already NP-hard, as for 3-coloring with the number of colors as the parameter. A para-NP-hard problem is not in [XP](/xp/) unless P = NP, so it is much harder than a [W[1]-hard](/w-hardness/) problem such as clique, which is in XP.

## Definition

A parameterized problem is a set $Q \subseteq \Sigma^* \times \mathbb{N}$. For a number $\ell$, the *$\ell$-th slice* of $Q$ is the classical problem $Q_\ell = \{x : (x, \ell) \in Q\}$. Machines are [nondeterministic Turing machines](/nondeterministic-turing-machine/) with several tapes.

**para-NP.** $Q$ is in para-NP if a nondeterministic machine decides it in time $f(k) \cdot |x|^{c}$, for a computable $f$ and a constant $c$. Flum and Grohe show that this is the same as "in NP after a precomputation on the parameter": there are a computable map $\pi$ on the parameters and a problem $R \in \mathsf{NP}$ such that $(x, k) \in Q$ if and only if $(x, \pi(k)) \in R$. In the same way, para-P is the class FPT.

**para-NP-hard.** $Q$ is *para-NP-hard* if $Q' \le_{\mathrm{fpt}} Q$ for every $Q' \in$ para-NP. It is *para-NP-complete* if it is also in para-NP.

**One hard slice is enough.** *If some slice $Q_\ell$ is NP-hard under polynomial-time many-one reductions, then $Q$ is para-NP-hard.*

Proof. Let $Q' \in$ para-NP, decided by a nondeterministic machine $M$ in time $f(k) \cdot |x|^c$, with $f$ computable. Let $L$ be the classical problem of triples $(x, k, 1^t)$ such that $M$ accepts $(x, k)$ within $t \cdot |x|^c$ steps. $L$ is in NP, since a machine can simulate $M$ for that many steps, and that is polynomial in the length of the triple. Since $Q_\ell$ is NP-hard, there is a polynomial-time map $h$ with $y \in L$ if and only if $h(y) \in Q_\ell$. The reduction maps $(x, k)$ to $(h(x, k, 1^{f(k)}), \ell)$. It computes $f(k)$ in time that depends on $k$ only, and then $h$ in time polynomial in $|x| + f(k)$, so the total time has the form $g(k) \cdot |x|^{O(1)}$. The new parameter is the constant $\ell$. Finally $(x, k) \in Q'$ if and only if $M$ accepts $(x, k)$ within $f(k) |x|^c$ steps, if and only if $(x, k, 1^{f(k)}) \in L$, if and only if $(h(x, k, 1^{f(k)}), \ell) \in Q$. $\square$

Flum and Grohe also prove a converse, for nontrivial problems: a problem is para-NP-hard if and only if the union of finitely many of its slices is NP-hard. The proof of the "only if" part is the argument of the next paragraph: the image of SAT under a reduction uses only finitely many parameter values.

**Not in XP unless P = NP.** *If $Q$ is para-NP-hard and $Q \in$ XP, then $\mathsf{P} = \mathsf{NP}$.*

Proof. Give [SAT](/sat/) the constant parameter 0. A nondeterministic machine decides it in polynomial time, so it is in para-NP. Let $R$ be a parameterized reduction from it to $Q$, in time $f(0) \cdot |\varphi|^c$, with new parameter $k' \le g(0) =: K$. Let $A$ decide $Q$ in time $h(k') \cdot |x'|^{e(k')}$. On an output $(x', k')$ with $k' \le K$, the time is at most $H \cdot |x'|^{E}$ with $H = \max_{j \le K} h(j)$ and $E = \max_{j \le K} e(j)$, both constants. Since $|x'| \le f(0) |\varphi|^c$, running $R$ and then $A$ decides SAT in polynomial time. So SAT is in P, and $\mathsf{P} = \mathsf{NP}$. $\square$

In the same way, para-NP = FPT if and only if P = NP: if P = NP, the precomputation form puts every para-NP problem in FPT, and if para-NP = FPT, the case above puts SAT in P.

## Examples and non-examples

**Coloring by the number of colors.** p-Coloring asks whether a graph $G$ has a proper coloring with $q$ colors, with parameter $q$. The slice $q = 3$ is [3-coloring](/three-coloring/), which is NP-complete, so p-Coloring is para-NP-hard. It is in para-NP, since a machine can guess the coloring, so it is para-NP-complete. The slices are different from each other: the Petersen graph is 3-colorable but not 2-colorable, and the Grötzsch graph, with 11 vertices, 20 edges and no triangle, is 4-colorable but not 3-colorable. Slices 1 and 2 are in P. See [k-coloring](/k-coloring/).

**Planar coloring.** On [planar graphs](/planar-graph/), 3-coloring is still NP-complete (Garey, Johnson and Stockmeyer 1976), so planar coloring by the number of colors is para-NP-hard, although every slice with $q \ge 4$ is trivial by the [four color theorem](/four-color-theorem/).

**Independent set by maximum degree.** Independent set and vertex cover are NP-complete on planar graphs of maximum degree 3 (Garey, Johnson and Stockmeyer 1976). With the maximum degree $\Delta$ as the parameter, the slice $\Delta = 3$ is NP-hard, so both problems are para-NP-hard in $\Delta$. With the parameter $k + \Delta$, [independent set](/parameterized-independent-set/) is FPT.

**SAT by clause width.** CNF satisfiability with the largest clause size as the parameter is para-NP-hard, because the slice of width 3 is [3-SAT](/3-sat/).

**Non-example: clique.** p-Clique is W[1]-complete, and every slice is in P, by trying all $\binom{n}{k}$ sets in time $O(n^k k^2)$. So it is in XP, and it is not para-NP-hard unless P = NP. A problem can be NP-complete as a classical problem, with $k$ in the input, while each of its slices is in P. Classical NP-hardness does not give para-NP-hardness.

**Non-example: vertex cover by cover size.** With the cover size $k$ as the parameter, vertex cover is FPT. Its slices are in P, and the slice structure gives no hardness.

## Related definitions

- *[XP](/xp/).* The problems with every slice in P, uniformly. Para-NP-hardness and membership in XP exclude each other unless P = NP.
- *[W[t]-hardness](/w-hardness/).* W[P] is a subset of para-NP: a W[P] problem can guess its $k$ input bits with $O(k \log n)$ nondeterministic bits. So a para-NP-hard problem is W[P]-hard, and W[t]-hard for every $t$. The converse fails for clique unless P = NP.
- *Other para-classes.* Flum and Grohe define para-C for any classical class C, as C after a precomputation on the parameter. Para-P is FPT, para-coNP and para-PSPACE are defined in the same way, and [para-L](/para-l/) is the logarithmic space version. The slice criterion above holds for para-coNP and para-PSPACE as well.
- *[NP-hardness](/np-hard/).* The classical notion, under polynomial-time reductions, for problems without a parameter.

## References
