---
tag: TJETK7
kind: definition
slug: np-hard
name: NP-hard
aliases:
- NP-hard problem
- NP-hardness
area: complexity/np-completeness
level: intro
summary: A problem is NP-hard when every problem in NP reduces to it by a polynomial-time Karp reduction. It need not be in NP; the halting problem is NP-hard.
prereqs: [np, polynomial-time-reduction]
see_also: [np-complete, co-np-complete, reduction, turing-reduction, strong-np-hardness, weak-np-hardness, np-hardness-reductions, halting-problem]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Section 5.1 (Turing reducibility and NP-hard problems) and Section 5.2 (a terminological history)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Section 2.2 (reducibility, NP-hardness and NP-completeness)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 34.3 (NP-completeness and reducibility, the definition of NP-hard)
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in R. E. Miller and J. W. Thatcher (eds.), Complexity of Computer Computations, Plenum Press (1972), 85 to 103
    locator: Definition 3 (polynomial-time reducibility) and Definition 5 (complete problems)
  - paper: doi:10.1145/1811129.1811130
    title: Donald E. Knuth, A terminological proposal, SIGACT News 6(1), 12 to 18 (1974)
    locator: the proposal of a term for a one-sided version of polynomial complete
---

A problem $H$ is NP-hard when every problem in [NP](/np/) reduces to it by a [polynomial-time reduction](/polynomial-time-reduction/) (a Karp reduction, also called a polynomial-time many-one [reduction](/reduction/)). An NP-hard problem is at least as hard as every problem in NP: a polynomial-time algorithm for it would give one for all of NP, and so P = NP. NP-hard problems need not be in NP; the [halting problem](/halting-problem/) is NP-hard and is not even decidable. A problem that is NP-hard and also in NP is [NP-complete](/np-complete/).

## Definition

The model is the deterministic [multitape Turing machine](/multitape-turing-machine/), and languages are subsets of $\{0,1\}^*$ under a fixed reasonable encoding (see [decision problem](/decision-problem/)).

**Karp reduction.** $A \le_m^p B$ when there is a function $f$, computable in polynomial time, with $x \in A \iff f(x) \in B$ for every string $x$.

**NP-hard (under Karp reductions).** A language $H$ is NP-hard when $A \le_m^p H$ for every $A \in \mathsf{NP}$.

On this site, "NP-hard" means NP-hard under Karp reductions unless a page says otherwise.

**The working form.** Karp reductions are transitive: if $A \le_m^p B$ by $f$ in time $p$ and $B \le_m^p C$ by $g$ in time $q$, then $g \circ f$ reduces $A$ to $C$ in time $p(n) + q(p(n))$, because $|f(x)| \le p(|x|)$. So if one NP-hard problem $K$ reduces to $H$, then $H$ is NP-hard. In practice $K$ is [SAT](/sat/) (NP-complete by the [Cook-Levin theorem](/cook-levin-theorem/)), [3-SAT](/3-sat/) or another known NP-complete problem. The reduction goes from the known hard problem $K$ to the new problem $H$. A reduction in the other direction, from $H$ to $K$, only shows that $H$ is not harder than $K$.

**NP-hard under Cook reductions.** A [Cook reduction](/turing-reduction/) $A \le_T^p B$ is a polynomial-time [oracle machine](/oracle-turing-machine/) that decides $A$ with unit-cost queries to $B$. A problem $H$ is NP-hard under Cook reductions when $\mathsf{NP} \subseteq \mathsf{P}^H$. Every Karp reduction is a Cook reduction with one query, so Karp-hard implies Cook-hard. Garey and Johnson (Section 5.1) define "NP-hard" with this Turing form, because it applies to search and optimization problems as well as to languages. The two notions differ on known problems. TAUT, the set of propositional tautologies, is NP-hard under Cook reductions: a formula $\varphi$ is satisfiable if and only if $\lnot\varphi$ is not a tautology, so one query and a negated answer decide SAT. TAUT is in [coNP](/co-np/), and so it is NP-hard under Karp reductions only if NP = coNP (see [coNP-complete](/co-np-complete/)).

**What follows from NP-hardness.**
- If an NP-hard problem (Karp or Cook) is in P, then P = NP.
- If a problem that is NP-hard under Karp reductions is in coNP, then NP = coNP.
- NP-hardness is not a proof that a problem needs exponential time. Whether NP-hard problems have polynomial-time algorithms is the [P versus NP problem](/p-versus-np-problem/), which is open.

## Examples and non-examples

**The halting problem is NP-hard.** Let HALT $= \{\langle M, w\rangle : M \text{ halts on } w\}$. The map sends a CNF formula $\varphi$ with $n$ variables to $\langle M_\varphi, \varepsilon\rangle$, where $M_\varphi$ ignores its input, tries the $2^n$ assignments of $\varphi$ in order, halts as soon as one satisfies $\varphi$, and enters an endless loop if none does.
- Cost: $M_\varphi$ is a fixed program with $\varphi$ written into it, so its encoding has length $O(|\varphi|)$ and $f$ runs in linear time. The running time of $M_\varphi$ does not matter; only the time to write it down counts.
- If $\varphi$ is satisfiable, $M_\varphi$ reaches a satisfying assignment after at most $2^n$ tries and halts.
- If $M_\varphi$ halts on some run, the only halting instruction follows a successful check of an assignment, so that assignment satisfies $\varphi$.

So $\mathrm{SAT} \le_m^p \mathrm{HALT}$, and HALT is NP-hard because SAT is. HALT is not in NP, since every language in NP is decidable.

**PSPACE and EXPTIME problems.** Since $\mathsf{NP} \subseteq \mathsf{PSPACE}$, every problem that is PSPACE-complete under polynomial-time many-one reductions is NP-hard. [QSAT](/qsat/), the truth of quantified Boolean formulas, is an example: a CNF formula $\varphi(x_1, \ldots, x_n)$ is satisfiable exactly when $\exists x_1 \cdots \exists x_n\, \varphi$ is true, and this map is a Karp reduction. Equivalence of regular expressions is also NP-hard; Karp (1972) gave a reduction from 3-SAT and noted that its membership in NP was in doubt (see [regex equivalence](/regex-equivalence-pspace-completeness/)).

**Optimization problems.** Finding a [maximum clique](/maximum-clique/) is NP-hard under Cook reductions: one call to an algorithm for it answers the decision question "is there a clique of size $k$?", which is NP-complete. Optimization problems are not languages, so they can be NP-hard only in the Cook sense or through their decision versions.

**A worked Cook reduction.** SAT reduces to TAUT by a Cook reduction with one query. For $\varphi = (x \lor y) \land \lnot x \land \lnot z$, the negation $\lnot\varphi$ is not a tautology, because $x = 0, y = 1, z = 0$ makes $\varphi$ true and $\lnot\varphi$ false; so the reduction answers "satisfiable". The answer of the oracle is inverted, which is what a Karp reduction cannot do.

**Hard problems with easy cases.** NP-hardness is a statement about all instances. [2-SAT](/2-sat/) and [Horn-SAT](/horn-sat/) are special cases of SAT in P. Knapsack is NP-hard but has a [pseudo-polynomial](/pseudo-polynomial-time/) algorithm, so it is only [weakly NP-hard](/weak-np-hardness/); [3-partition](/three-partition/) and [bin packing](/bin-packing-np-hardness/) stay NP-hard with numbers in unary and are [strongly NP-hard](/strong-np-hardness/).

**Non-examples.** The empty language and $\{0,1\}^*$ are not NP-hard under Karp reductions, because a reduction from a language with both yes-instances and no-instances needs targets of both kinds. A problem in P is NP-hard if and only if P = NP. [2-SAT](/2-sat/) is in P (in fact in linear time), so it is NP-hard only if P = NP. Problems such as [graph isomorphism](/graph-isomorphism-problem/) and [integer factorization](/integer-factorization/) are in NP but are not known to be NP-hard; they are candidates for [NP-intermediate](/np-intermediate/) problems.

## Related definitions

- [NP-complete](/np-complete/): NP-hard and in NP.
- [coNP-complete](/co-np-complete/): the same notion for coNP; coNP-hard problems are the complements of NP-hard ones under Karp reductions.
- [Strong NP-hardness](/strong-np-hardness/) and [weak NP-hardness](/weak-np-hardness/): NP-hardness of number problems with numbers in unary or in binary.
- [Polynomial-time reduction](/polynomial-time-reduction/), [Cook reduction](/turing-reduction/), [Levin reduction](/levin-reduction/) and [parsimonious reduction](/parsimonious-reduction/): the reduction types; each gives its own form of hardness.
- [NP-hardness reductions](/np-hardness-reductions/) and [gadget reductions](/gadget-reduction/): the methods used to prove NP-hardness; [NP-completeness proof](/np-completeness-proof/) gives the steps.
- Hardness for other classes: PSPACE-hard, EXPTIME-hard and P-hard are defined in the same way; P-hardness uses logspace reductions, because every nontrivial problem in P is hard for P under polynomial-time reductions.

## References
