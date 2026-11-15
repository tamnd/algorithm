---
tag: B4BYY2
kind: definition
slug: np-complete
name: NP-complete
aliases:
- NP-complete problem
- NP-completeness
- NPC
area: complexity/np-completeness
level: intro
summary: A problem is NP-complete when it is in NP and every problem in NP reduces to it by a Karp reduction. A polynomial-time algorithm for one would give P = NP.
prereqs: [np-hard, np]
see_also: [sat, 3-sat, reduction, cook-levin-theorem, karps-21-np-complete-problems, garey-johnson-compendium, np-completeness-proof, np-intermediate]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Section 2.5 (polynomial transformations and NP-completeness), Section 2.6 (Cook's theorem), Section 3.1 (six basic NP-complete problems) and the Appendix (a list of NP-complete problems)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Section 2.2 (reducibility and NP-completeness, a simple NP-complete language) and Section 2.4 (the web of reductions)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 7.4 (NP-completeness) and Section 7.5 (additional NP-complete problems)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 34.3 (NP-completeness and reducibility) and Section 34.5 (NP-complete problems)
  - paper: doi:10.1145/800157.805047
    title: Stephen A. Cook, The complexity of theorem-proving procedures, Proceedings of the 3rd ACM Symposium on Theory of Computing (1971), 151 to 158
    locator: Theorem 1 and Theorem 2
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in R. E. Miller and J. W. Thatcher (eds.), Complexity of Computer Computations, Plenum Press (1972), 85 to 103
    locator: Definition 5 (complete problems), Theorem 2 and Corollary 1, the Main Theorem
  - paper: doi:10.1145/1811129.1811130
    title: Donald E. Knuth, A terminological proposal, SIGACT News 6(1), 12 to 18 (1974)
    locator: the poll that led to the terms NP-hard and NP-complete
  - paper: "David S. Johnson, A brief history of NP-completeness, 1954-2012, Documenta Mathematica, Extra Volume: Optimization Stories (2012), 359 to 376"
    locator: the sections on Cook, Karp and Levin and on the terminology
  - paper: doi:10.1016/0020-0190(87)90232-8
    title: Ravi B. Boppana, Johan Hastad and Stathis Zachos, Does co-NP have short interactive proofs?, Information Processing Letters 25(2), 127 to 132 (1987)
    locator: the consequence for graph isomorphism (if GI is NP-complete, the polynomial hierarchy collapses to its second level)
---

A problem is NP-complete when it is in [NP](/np/) and it is [NP-hard](/np-hard/): every problem in NP reduces to it by a [polynomial-time reduction](/polynomial-time-reduction/) (a Karp [reduction](/reduction/)). The NP-complete problems are the hardest problems in NP in a precise sense. If any one of them has a polynomial-time algorithm, then every problem in NP has one and P = NP; if any one of them has no polynomial-time algorithm, then none of them has one. [SAT](/sat/) was the first known NP-complete problem ([Cook-Levin theorem](/cook-levin-theorem/)), and [3-SAT](/3-sat/), clique, Hamiltonian cycle, subset sum and thousands of other problems followed.

## Definition

The model is the deterministic [multitape Turing machine](/multitape-turing-machine/); languages are [decision problems](/decision-problem/) under a fixed reasonable encoding, with numbers in binary.

**Definition.** A language $C$ is NP-complete when
1. $C \in \mathsf{NP}$, and
2. $A \le_m^p C$ for every $A \in \mathsf{NP}$, where $\le_m^p$ is the polynomial-time many-one (Karp) reduction.

NP-completeness on this site means completeness under Karp reductions unless a page says otherwise. Karp (1972, Definition 5) used the equivalent form "$C$ is in NP and SAT reduces to $C$", which is equivalent because SAT is NP-complete and Karp reductions are transitive.

**Basic facts.** Let $C$ be NP-complete.
- $C \in \mathsf{P}$ if and only if $\mathsf{P} = \mathsf{NP}$ (Karp 1972, Corollary 1 for SAT). If $C \in \mathsf{P}$ and $A \in \mathsf{NP}$, then $A \le_m^p C$ by some $f$, and computing $f$ and then deciding $C$ decides $A$ in polynomial time.
- $C \in \mathsf{coNP}$ if and only if $\mathsf{NP} = \mathsf{coNP}$.
- Any two NP-complete problems reduce to each other, so they form one equivalence class under Karp reductions.
- To prove a new problem $B$ NP-complete, show $B \in \mathsf{NP}$ and reduce a known NP-complete problem to $B$ (see [NP-completeness proof](/np-completeness-proof/)).

**A language that is NP-complete by design.** Let $U$ be the set of triples $\langle M, x, 1^t\rangle$ such that the [nondeterministic Turing machine](/nondeterministic-turing-machine/) $M$ has an accepting run on $x$ of at most $t$ steps. $U$ is in NP: the certificate is the sequence of choices, and a universal simulation checks it in time polynomial in $|M| + |x| + t$. If $A \in \mathsf{NP}$ is decided by $M_A$ in time $p(n)$, then $x \mapsto \langle M_A, x, 1^{p(|x|)}\rangle$ reduces $A$ to $U$ in polynomial time. So $U$ is NP-complete. The Cook-Levin theorem matters because it shows the same for a natural problem, SAT, with no machine in the input.

**Other reductions.** Cook (1971) proved his theorem with polynomial-time Turing (Cook) reductions, and Levin (1973) with reductions between search problems that also map solutions ([Levin reduction](/levin-reduction/)). With [Cook reductions](/turing-reduction/), the complement of every NP-complete problem is also complete, so that notion does not separate NP from [coNP](/co-np/). Whether the Karp and the Cook notions of NP-completeness define the same class is open.

## Examples and non-examples

**A full NP-completeness proof: 3-SAT to independent set.** INDEPENDENT SET. Instance: a graph $G$ and an integer $k$. Question: does $G$ have $k$ vertices with no edge between any two of them? (See [independent set](/independent-set/).)

Membership: a certificate is a set of $k$ vertices, and the verifier checks the $\binom{k}{2}$ pairs against the edge set in polynomial time.

The map $f$. Let $\varphi$ be a 3-CNF formula with clauses $C_1, \ldots, C_m$. For each clause, make one vertex per literal and join the three vertices of the clause in a triangle. Then join every two vertices in different clauses whose literals are $x_i$ and $\lnot x_i$ (conflict edges). Set $k = m$.

Cost: the graph has $3m$ vertices and at most $3m + \binom{3m}{2}$ edges, and $f$ writes it in time $O(m^2)$.

If $\varphi$ is satisfiable: fix a satisfying assignment and pick one true literal in each clause. The $m$ chosen vertices lie in different triangles, and no two of them are $x_i$ and $\lnot x_i$, because both cannot be true. So they form an independent set of size $m$.

If $G$ has an independent set $S$ of size $m$: take any such $S$. It has at most one vertex per triangle and $m$ vertices, so exactly one vertex per clause. No two vertices of $S$ carry complementary literals, because those are joined by a conflict edge. Set each variable that appears as a literal in $S$ so that the literal is true, and set the other variables to 0. Every clause then contains a true literal, so $\varphi$ is satisfiable.

Worked example. For $\varphi = (x_1 \lor x_2 \lor x_3) \land (\lnot x_1 \lor \lnot x_2 \lor x_3) \land (x_1 \lor \lnot x_2 \lor \lnot x_3)$, a script built $f(\varphi)$: 9 vertices, 15 edges (9 triangle edges and 6 conflict edges) and $k = 3$. The conflict edges join $x_1$ in $C_1$ with $\lnot x_1$ in $C_2$; $x_2$ in $C_1$ with $\lnot x_2$ in $C_2$ and with $\lnot x_2$ in $C_3$; $x_3$ in $C_1$ with $\lnot x_3$ in $C_3$; $\lnot x_1$ in $C_2$ with $x_1$ in $C_3$; and $x_3$ in $C_2$ with $\lnot x_3$ in $C_3$. By brute force, $\varphi$ has 5 satisfying assignments and $G$ has 12 independent sets of size 3. In the forward direction, the assignment $x_1 = x_2 = x_3 = 1$ makes $x_1$ true in $C_1$, $x_3$ true in $C_2$ and $x_1$ true in $C_3$, and these three vertices are independent. In the backward direction, the independent set with $x_1$ from $C_1$, $\lnot x_2$ from $C_2$ and $x_1$ from $C_3$ gives $x_1 = 1$, $x_2 = 0$ and $x_3 = 0$, which satisfies $\varphi$. The counts differ (5 against 12), so this reduction is not [parsimonious](/parsimonious-reduction/).

**Standard NP-complete problems.** [SAT](/sat/), [3-SAT](/3-sat/), [circuit SAT](/circuit-sat/), [clique](/clique-problem/), [vertex cover](/vertex-cover/), [Hamiltonian cycle](/hamiltonian-cycle-np-completeness/), [traveling salesman (decision)](/traveling-salesman-decision/), [3-coloring](/three-coloring/), [subset sum](/subset-sum-problem/), [partition](/partition-problem/), [3-dimensional matching](/three-dimensional-matching/), [exact cover by 3-sets](/exact-cover-by-3-sets/) and [knapsack (decision)](/knapsack-decision/). [Karp's 21 problems](/karps-21-np-complete-problems/) and the [Garey and Johnson compendium](/garey-johnson-compendium/) list many more.

**Non-examples.**
- [2-SAT](/2-sat/) and [Horn-SAT](/horn-sat/) are in P, so they are NP-complete only if P = NP.
- The [halting problem](/halting-problem/) is NP-hard but not in NP, so it is not NP-complete.
- TAUT, the set of tautologies, is [coNP-complete](/co-np-complete/). It is NP-complete only if NP = coNP.
- Karp (1972) listed NONPRIMES (is $k$ composite?) and LINEAR INEQUALITIES (does $Cx \ge d$ have a rational solution?) as problems in NP not known to be complete. Both are now known to be in P, by the [AKS primality test](/aks-primality-test/) and by [Khachiyan's ellipsoid method](/lp-in-p/), so they are NP-complete only if P = NP.
- The decision version of [integer factorization](/integer-factorization/), "does $N$ have a factor at most $k$?", is in NP and in coNP. It is NP-complete only if NP = coNP.
- [Graph isomorphism](/graph-isomorphism-problem/) is in NP and is not known to be NP-complete or in P. If GI were NP-complete, the polynomial hierarchy would collapse to its second level (Boppana, Håstad and Zachos 1987). It is a candidate [NP-intermediate](/np-intermediate/) problem, not a proved one.

**Traps.**
- NP does not mean "not polynomial". It means nondeterministic polynomial time, and P is a subset of NP.
- NP-completeness does not prove that a problem needs exponential time. No superpolynomial lower bound is known for any NP-complete problem. The exponential time hypothesis (stated on the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) page) is an assumption, not a theorem.
- NP-completeness is about the worst case over all instances. Many instances, and many special cases such as planar graphs or bounded treewidth, can be easy.

## Related definitions

- [NP-hard](/np-hard/): the hardness condition alone, without membership in NP.
- [coNP-complete](/co-np-complete/): the complements of NP-complete problems, such as TAUT and UNSAT.
- [Strong NP-hardness](/strong-np-hardness/) and [weak NP-hardness](/weak-np-hardness/) separate number problems by the size of their numbers; see also [pseudo-polynomial time](/pseudo-polynomial-time/).
- [NP-intermediate](/np-intermediate/): problems in NP that are neither in P nor NP-complete. They exist if P is not NP ([Ladner's theorem](/ladner-theorem/), and the [general form](/ladners-theorem/)).
- [Mahaney's theorem](/mahaneys-theorem/): no sparse set is NP-complete unless P = NP.
- [NP-completeness proof](/np-completeness-proof/), [gadget reduction](/gadget-reduction/) and [NP-hardness reductions](/np-hardness-reductions/): how completeness proofs are built.

## References
