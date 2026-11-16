---
tag: X7DV33
kind: definition
slug: polynomial-hierarchy
name: Polynomial hierarchy (PH)
aliases:
- PH
area: complexity/complexity-classes
level: advanced
summary: The union of the classes Sigma_k^p and Pi_k^p, defined by k alternating quantifiers over polynomial-length strings, or by towers of NP oracles. It lies between NP and PSPACE.
prereqs: [np, co-np, oracle-turing-machine]
see_also: [karp-lipton-theorem, toda-theorem, boolean-hierarchy, qsat, alternating-turing-machine, sipser-gacs-theorem, pspace, baker-gill-solovay-theorem]
sources:
  - paper: doi:10.1109/SWAT.1972.29
    title: Albert R. Meyer and Larry J. Stockmeyer, The equivalence problem for regular expressions with squaring requires exponential space, 13th Symposium on Switching and Automata Theory, 125 to 129 (1972)
    locator: the first definition of the hierarchy
  - paper: doi:10.1016/0304-3975(76)90061-X
    title: Larry J. Stockmeyer, The polynomial-time hierarchy, Theoretical Computer Science 3(1), 1 to 22 (1976)
    locator: the oracle definition, the quantifier characterization and complete problems
  - paper: doi:10.1016/0304-3975(76)90062-1
    title: Celia Wrathall, Complete sets and the polynomial-time hierarchy, Theoretical Computer Science 3(1), 23 to 33 (1976)
    locator: the quantifier characterization and the completeness of quantified formulas with k alternations
  - paper: doi:10.1145/322234.322243
    title: Ashok K. Chandra, Dexter C. Kozen and Larry J. Stockmeyer, Alternation, Journal of the ACM 28(1), 114 to 133 (1981)
    locator: the levels of the hierarchy as alternating polynomial time with a bounded number of alternations
  - paper: doi:10.1109/SFCS.1985.49
    title: Andrew Chi-Chih Yao, Separating the polynomial-time hierarchy by oracles, 26th IEEE Symposium on Foundations of Computer Science, 1 to 10 (1985)
    locator: the oracle relative to which PH is not equal to PSPACE
  - paper: doi:10.1006/jcss.2001.1775
    title: Christopher Umans, The minimum equivalent DNF problem and shortest implicants, Journal of Computer and System Sciences 63(4), 597 to 611 (2001)
    locator: the Sigma_2^p-completeness of the minimum equivalent DNF problem
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 5, The polynomial hierarchy and alternations
---

The polynomial hierarchy (PH) is a sequence of complexity classes that extends [NP](/np/) and [coNP](/co-np/) by alternating quantifiers. Its $k$-th level $\Sigma_k^p$ contains the problems of the form "there is a $y_1$ such that for every $y_2$ there is a $y_3$ ..." with $k$ quantifiers over strings of polynomial length and a polynomial-time test at the end, and $\Pi_k^p$ is the same with the first quantifier universal. Level 1 is NP and coNP, and every level is inside [PSPACE](/pspace/). Meyer and Stockmeyer defined the hierarchy in 1972. It is conjectured to be infinite, which is a stronger assumption than $\mathsf{P} \ne \mathsf{NP}$, and many results take the form "if X, then PH collapses" as evidence that X is false.

## Definition

**By quantifiers.** For $k \ge 1$, a language $L$ is in $\Sigma_k^p$ if there are a polynomial $q$ and a polynomial-time predicate $R$ such that

$$x \in L \iff \exists y_1\ \forall y_2\ \exists y_3 \cdots Q_k y_k\ \ R(x, y_1, \ldots, y_k),$$

where every $y_i$ ranges over $\{0,1\}^{q(|x|)}$ and $Q_k$ is $\exists$ for odd $k$ and $\forall$ for even $k$. The class $\Pi_k^p$ is the same with the quantifiers starting with $\forall$, so $\Pi_k^p = \mathsf{co}\Sigma_k^p$. Set $\Sigma_0^p = \Pi_0^p = \mathsf{P}$. Then

$$\mathsf{PH} = \bigcup_{k \ge 0} \Sigma_k^p.$$

**By oracles.** With [oracle Turing machines](/oracle-turing-machine/),

$$\Sigma_{k+1}^p = \mathsf{NP}^{\Sigma_k^p}, \qquad \Delta_{k+1}^p = \mathsf{P}^{\Sigma_k^p}, \qquad \Pi_{k+1}^p = \mathsf{co}\Sigma_{k+1}^p.$$

So $\Sigma_1^p = \mathsf{NP}$, $\Delta_2^p = \mathsf{P}^{\mathsf{NP}}$ and $\Sigma_2^p = \mathsf{NP}^{\mathsf{NP}}$. Stockmeyer (1976) and Wrathall (1976) proved that the two definitions give the same classes. One direction: an $\mathsf{NP}^{\Sigma_k^p}$ machine guesses its computation, together with the oracle answers and a $\Sigma_k^p$ witness for each yes answer, and a no answer is a $\Pi_k^p$ statement that merges with the next quantifier block.

**By alternating machines.** $\Sigma_k^p$ is the class of languages decided by [alternating Turing machines](/alternating-turing-machine/) in polynomial time that start in an existential state and alternate at most $k - 1$ times (Chandra, Kozen and Stockmeyer 1981). With no bound on alternations, alternating polynomial time is PSPACE.

**Basic inclusions.** For every $k$:

$$\Sigma_k^p \cup \Pi_k^p \subseteq \Delta_{k+1}^p \subseteq \Sigma_{k+1}^p \cap \Pi_{k+1}^p, \qquad \mathsf{PH} \subseteq \mathsf{PSPACE}.$$

The last inclusion holds because a recursive evaluation of the $k$ quantifiers reuses the same polynomial space for each branch.

**Collapse.** If $\Sigma_k^p = \Pi_k^p$ for some $k \ge 1$, then $\mathsf{PH} = \Sigma_k^p$. Proof: take $L \in \Sigma_{k+1}^p$, written as $\exists y_1\, \varphi(x, y_1)$ with $\varphi$ a $\Pi_k^p$ predicate. By assumption $\varphi$ is also $\Sigma_k^p$, so it begins with $\exists$, and the two existential blocks merge into one. So $\Sigma_{k+1}^p = \Sigma_k^p$, and induction gives the rest. In the same way $\mathsf{P} = \mathsf{NP}$ implies $\mathsf{PH} = \mathsf{P}$. "PH collapses" means that $\mathsf{PH} = \Sigma_k^p$ for some $k$. A further consequence: if PH has a complete problem under polynomial-time many-one reductions, that problem lies in some $\Sigma_k^p$ and PH collapses to that level. Since PSPACE has complete problems, $\mathsf{PH} = \mathsf{PSPACE}$ would collapse PH.

## Examples and non-examples

**Quantified formulas with $k$ blocks.** $\Sigma_k$-SAT is the set of true quantified Boolean formulas $\exists X_1 \forall X_2 \cdots Q_k X_k\ \varphi$, where the $X_i$ are disjoint blocks of variables. It is $\Sigma_k^p$-complete under polynomial-time many-one reductions (Stockmeyer 1976, Wrathall 1976), by the [Cook-Levin theorem](/cook-levin-theorem/) applied to the predicate $R$. For $k = 3$ the last block may be taken existential and $\varphi$ a 3-CNF. With an unbounded number of blocks the problem is [QBF](/qbf/), also called [QSAT](/qsat/), which is PSPACE-complete.

**A natural $\Sigma_2^p$ problem: the shortest equivalent DNF.** Given a DNF formula $\varphi$ and a number $k$, is there a DNF $\psi$ of size at most $k$ that is equivalent to $\varphi$? The question has the form "there is a $\psi$ such that for every assignment $a$, $\psi(a) = \varphi(a)$", so it is in $\Sigma_2^p$, and Umans (2001) proved it is $\Sigma_2^p$-complete. A small case: $\varphi = x_1 x_2 \lor x_1 \bar{x}_2 \lor x_3$ over 3 variables. A term can contain each variable positively, negatively or not at all, which gives $3^3 = 27$ terms. None of the $27$ one-term DNFs is equivalent to $\varphi$. Among the $351$ pairs of distinct terms, exactly $3$ are: $x_1 \lor x_3$, $x_1 \lor \bar{x}_1 x_3$ and $x_1 \bar{x}_3 \lor x_3$. Each candidate is checked on all $8$ assignments, which is the $\forall$ part. With $n$ variables and $k$ terms, the brute force tries up to $3^{nk}$ candidates for the guess and $2^n$ assignments for the check. A polynomial-time reduction of this problem to SAT would put $\Sigma_2^p$ in NP and collapse PH.

**Other natural problems.** Many problems in logic and AI are complete for the second level: the existence of a stable model of a disjunctive logic program ([disjunctive ASP](/disjunctive-asp-sigma2-completeness/)), several forms of [abductive reasoning](/abductive-reasoning/), and credulous reasoning in [default logic](/default-logic-complexity/). In $\Delta_2^p = \mathsf{P}^{\mathsf{NP}}$, the problem "is the last bit of the lexicographically largest satisfying assignment equal to 1" is complete, and so are many questions about the exact value of an optimum, such as whether a TSP instance has a unique optimal tour.

**Problems in low levels.** [BPP](/bpp/) $\subseteq \Sigma_2^p \cap \Pi_2^p$ ([Sipser-Gács theorem](/sipser-gacs-theorem/)). The [Boolean hierarchy](/boolean-hierarchy/), including DP, lies inside $\Delta_2^p$. [Graph isomorphism](/graph-isomorphism-problem/) is in $\mathsf{NP} \cap \mathsf{coAM}$, and if it were NP-complete, PH would collapse to $\Sigma_2^p$.

**Above PH.** [Toda's theorem](/toda-theorem/) gives $\mathsf{PH} \subseteq \mathsf{P}^{\mathsf{PP}}$, so a polynomial-time machine with a counting oracle decides all of PH. PSPACE contains PH, and whether the inclusion is strict is open.

**Non-examples.** Problems that are hard for PSPACE, such as QBF with unbounded alternation and the winner of generalized geography, are not in PH unless PH collapses, because PH would then contain a PSPACE-complete problem. An [EXPTIME](/exptime/)-complete problem is not in P by the [time hierarchy theorem](/time-hierarchy-theorem/), and it is in PH only if $\mathsf{EXPTIME} = \mathsf{PSPACE}$, which is open and believed false.

## Related definitions

- [Karp-Lipton theorem](/karp-lipton-theorem/): if NP has polynomial-size circuits, PH collapses to $\Sigma_2^p$.
- [Boolean hierarchy](/boolean-hierarchy/): Boolean combinations of NP sets, inside $\Delta_2^p$.
- [Toda's theorem](/toda-theorem/): PH is inside $\mathsf{P}^{\#\mathsf{P}}$.
- Oracles: relative to the oracle of the [Baker-Gill-Solovay theorem](/baker-gill-solovay-theorem/) with $\mathsf{P}^A = \mathsf{NP}^A$, PH collapses to P. Yao (1985) gave oracles relative to which PH is not equal to PSPACE and the levels are distinct, from lower bounds on constant-depth circuits ([AC0](/ac0/)), and Håstad (1986) gave simpler and stronger bounds of the same kind. Rossman, Servedio and Tan (2015) proved that PH is infinite relative to a random oracle.
- [Alternating Turing machines](/alternating-turing-machine/): the machine model behind the levels.

## References
