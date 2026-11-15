---
tag: X2MDPB
kind: definition
slug: co-np-complete
name: coNP-complete
aliases:
- coNP-completeness
area: complexity/np-completeness
level: core
summary: A problem in coNP to which every coNP problem reduces by a Karp reduction; equivalently, its complement is NP-complete. TAUT and UNSAT are examples.
prereqs: [co-np, np-complete]
see_also: [co-np, np-complete, np-hard, sat, turing-reduction, polynomial-hierarchy, boolean-hierarchy, good-characterization]
sources:
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Section 2.6 (coNP, coNP-completeness and TAUTOLOGY)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Section 7.1 (the structure of NP, complements of NP-complete problems)
  - paper: doi:10.1145/800157.805047
    title: Stephen A. Cook, The complexity of theorem-proving procedures, Proceedings of the 3rd ACM Symposium on Theory of Computing (1971), 151 to 158
    locator: Theorem 1 (every NP set is P-reducible to the DNF tautologies) and Theorem 2
  - paper: doi:10.2307/2273702
    title: Stephen A. Cook and Robert A. Reckhow, The relative efficiency of propositional proof systems, Journal of Symbolic Logic 44(1), 36 to 50 (1979)
    locator: the definition of a propositional proof system and the theorem that a polynomially bounded system exists if and only if NP = coNP
---

A problem is coNP-complete when it is in [coNP](/co-np/) and every problem in coNP reduces to it by a [polynomial-time reduction](/polynomial-time-reduction/) (a Karp reduction). Under Karp reductions this holds exactly when its complement is [NP-complete](/np-complete/). The standard examples are TAUT, the set of propositional tautologies, and UNSAT, the set of unsatisfiable formulas. A coNP-complete problem is in NP only if NP = coNP, which is open; this is why no one expects short proofs that a formula is unsatisfiable.

## Definition

The model is the deterministic [multitape Turing machine](/multitape-turing-machine/), and $\le_m^p$ is the polynomial-time many-one (Karp) reduction.

**Definition.** A language $L$ is coNP-complete when
1. $L \in \mathsf{coNP}$, that is, $\overline{L} \in \mathsf{NP}$, and
2. $A \le_m^p L$ for every $A \in \mathsf{coNP}$.

A language that satisfies condition 2 alone is coNP-hard.

**Complements.** For every function $f$, $x \in A \iff f(x) \in B$ is the same statement as $x \in \overline{A} \iff f(x) \in \overline{B}$. So $A \le_m^p B$ if and only if $\overline{A} \le_m^p \overline{B}$, with the same $f$. It follows that $L$ is coNP-complete if and only if $\overline{L}$ is NP-complete, and that $L$ is coNP-hard if and only if $\overline{L}$ is NP-hard. Here the complement is taken in $\{0,1\}^*$. The complement of UNSAT is SAT together with the strings that encode no formula; a polynomial-time check of the encoding moves these strings to a fixed no-instance, so the difference does not change any of the statements.

**The main fact.** If some coNP-complete problem $L$ is in NP, then $\mathsf{NP} = \mathsf{coNP}$.

Proof. Let $A \in \mathsf{coNP}$. Then $A \le_m^p L$ by some $f$. Since $L \in \mathsf{NP}$, a verifier for $A$ computes $f(x)$ and runs the verifier of $L$ on $f(x)$; so $A \in \mathsf{NP}$, and $\mathsf{coNP} \subseteq \mathsf{NP}$. Now let $B \in \mathsf{NP}$. Then $\overline{B} \in \mathsf{coNP} \subseteq \mathsf{NP}$, so $B \in \mathsf{coNP}$. Thus $\mathsf{NP} \subseteq \mathsf{coNP}$ too. $\blacksquare$

By the same argument, an NP-complete problem is in coNP only if NP = coNP. So a problem in NP ∩ coNP, such as the decision version of [integer factorization](/integer-factorization/) or a [good characterization](/good-characterization/), is not NP-complete or coNP-complete unless NP = coNP.

**Say which reduction.** With polynomial-time Turing ([Cook](/turing-reduction/)) reductions, a language and its complement reduce to each other with one query, by inverting the answer. So TAUT is NP-hard under Cook reductions, and SAT is coNP-hard under Cook reductions. Under Karp reductions, TAUT is NP-hard only if NP = coNP. A page that calls a problem "NP-hard" or "coNP-complete" must say which reduction it uses; on this site it is the Karp reduction unless the page says otherwise.

## Examples and non-examples

**UNSAT and TAUT.** UNSAT is the set of CNF formulas with no satisfying assignment; it is the complement of [SAT](/sat/), so it is coNP-complete. TAUT is the set of formulas that are true under every assignment. The map $\varphi \mapsto \lnot\varphi$ is a Karp reduction from UNSAT to TAUT and back: $\varphi$ is unsatisfiable exactly when $\lnot\varphi$ is a tautology. By De Morgan's laws, the negation of a CNF formula is a DNF formula of the same length, so UNSAT also reduces to DNF-TAUT, the tautologies in disjunctive normal form. Cook (1971, Theorem 1) stated his theorem for this set: every set accepted in polynomial time by a nondeterministic machine is P-reducible to the DNF tautologies, where his P-reducibility is a polynomial-time Turing reduction.

**A worked example.** Let $\varphi$ be the CNF formula with all 8 clauses $(\ell_1 \lor \ell_2 \lor \ell_3)$, $\ell_i \in \{x_i, \lnot x_i\}$. A script checked all 8 assignments: each falsifies exactly one clause, so $\varphi \in \mathrm{UNSAT}$. The reduction gives $\lnot\varphi$, the DNF with the 8 terms $(\bar\ell_1 \land \bar\ell_2 \land \bar\ell_3)$, and every assignment makes exactly one term true, so $\lnot\varphi \in \mathrm{TAUT}$. Now drop the clause $(x_1 \lor x_2 \lor x_3)$. The 7 remaining clauses have exactly one satisfying assignment, $x_1 = x_2 = x_3 = 0$, found by the script. That assignment is a short certificate that the formula is not in UNSAT, and that its negation, the DNF without the term $(\lnot x_1 \land \lnot x_2 \land \lnot x_3)$, is not in TAUT. This is the asymmetry: a no-answer for TAUT has a certificate of $n$ bits, but the only general proof of a yes-answer known here is the table of $2^n$ rows.

**Two small DNF formulas.** $(x \land y) \lor \lnot x \lor \lnot y$ is a tautology; the script checked its 4 rows. $(x \land y) \lor \lnot x \lor z$ is not; its only falsifying assignment is $x = 1, y = 0, z = 0$.

**Other coNP-complete problems.** The complement of every NP-complete problem is coNP-complete: "this graph has no Hamiltonian cycle", "this graph is not 3-colorable", "every tour of these cities has length more than $k$", "these two formulas are equivalent" (the formula $\varphi \leftrightarrow \psi$ is a tautology). Cook (1971, Theorem 2) also showed that the tautologies, the DNF tautologies and D3, the DNF tautologies with at most 3 literals per term, are all P-reducible to each other; he noted that D2 is in polynomial time.

**Non-examples.**
- SAT is NP-complete. It is coNP-complete only if NP = coNP.
- TAUT is coNP-complete and also NP-hard under Cook reductions, but that does not make it NP-complete: it is in NP only if NP = coNP.
- PRIMES is in coNP (a factor is a certificate of compositeness), but it is in P by the [AKS primality test](/aks-primality-test/), so it is coNP-complete only if P = NP.
- Problems complete for higher levels of the [polynomial hierarchy](/polynomial-hierarchy/), such as $\Pi_2^p$-complete problems, are coNP-hard but not known to be in coNP.

## Related definitions

- [coNP](/co-np/): the class; [NP-complete](/np-complete/) and [NP-hard](/np-hard/): the same notions for NP.
- Propositional proof systems (Cook and Reckhow 1979): a polynomial-time function whose range is TAUT. A proof system in which every tautology has a proof of polynomial length exists if and only if NP = coNP. Proof complexity studies lower bounds for specific systems, such as resolution, as a way toward this question.
- [Polynomial hierarchy](/polynomial-hierarchy/): coNP is $\Pi_1^p$. NP = coNP would collapse the hierarchy to its first level.
- [Boolean hierarchy](/boolean-hierarchy/): the class DP of intersections of an NP set and a coNP set, with complete problems such as "$\varphi$ is satisfiable and $\psi$ is not".
- [Cook reduction](/turing-reduction/): the reduction under which NP-hardness and coNP-hardness coincide.

## References
