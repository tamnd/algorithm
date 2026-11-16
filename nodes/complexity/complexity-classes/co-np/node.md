---
tag: RFB7M7
kind: definition
slug: co-np
name: co-NP
aliases:
- coNP
area: complexity/complexity-classes
level: intro
summary: "The complements of NP languages: problems whose no-instances have polynomial-length certificates checkable in polynomial time. Tautology is the standard complete problem."
prereqs: [np]
see_also: [np, co-np-complete, good-characterization, p, polynomial-hierarchy, haken-resolution-lower-bound, immerman-szelepcsenyi-theorem, class-inclusions-chain]
sources:
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Section 2.6.1, coNP
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley, 1994
    locator: Chapter 10, coNP and function problems
  - paper: doi:10.2307/2273702
    title: Stephen A. Cook and Robert A. Reckhow, The relative efficiency of propositional proof systems, Journal of Symbolic Logic 44(1) (1979), 36 to 50
    locator: propositional proof systems and the equivalence with NP = coNP
  - paper: doi:10.1137/0204018
    title: Vaughan R. Pratt, Every prime has a succinct certificate, SIAM Journal on Computing 4(3) (1975), 214 to 220
    locator: primality is in NP
---

coNP is the class of languages whose complements are in [NP](/np/). In a problem in NP, every yes-instance has a short certificate. In a problem in coNP, every no-instance has one: a short proof that the answer is no, which a deterministic polynomial-time verifier checks. The standard example is tautology, where a falsifying assignment proves that a formula is not a tautology. Whether $\mathsf{NP} = \mathsf{coNP}$ is open, and most researchers believe the two classes are different.

## Definition

Fix the alphabet $\{0, 1\}$. For a language $L$, write $\overline{L} = \{0, 1\}^* \setminus L$. Then

$$\mathsf{coNP} = \{ L : \overline{L} \in \mathsf{NP} \}.$$

**By verifiers.** Unfolding the [verifier definition of NP](/np/), $L \in \mathsf{coNP}$ when there are a polynomial $p$ and a deterministic polynomial-time machine $V$ such that for every $x$

$$x \in L \iff \forall u \in \{0, 1\}^{p(|x|)} : V(x, u) = 1.$$

A string $u$ with $V(x, u) = 0$ is a certificate that $x \notin L$. So a language is in coNP when its no-instances have short certificates. The quantifier is "for all" where NP has "there exists".

**Complements of problems.** For a decision problem, the complement swaps the yes-instances and the no-instances and keeps the strings that do not encode an instance on the "no" side. The set of well-formed encodings is in P for every reasonable encoding, so this choice does not change membership in NP or coNP. The complement of SAT is UNSAT, the set of unsatisfiable formulas, and $\text{UNSAT} \in \mathsf{coNP}$.

**coNP is not the complement of NP.** The complement of the class NP is the set of all languages that are not in NP, which contains undecidable languages. coNP is the set of complements of the languages in NP. The two classes have $\mathsf{P}$ in common: $\mathsf{P} \subseteq \mathsf{NP} \cap \mathsf{coNP}$, because P is closed under complement.

**Basic facts.**

- $\mathsf{coNP} \subseteq \mathsf{PSPACE} \subseteq \mathsf{EXP}$, because these classes are closed under complement and contain NP.
- coNP is closed under union, intersection and polynomial-time many-one reductions.
- A language is *coNP-complete* when it is in coNP and every language in coNP reduces to it by a polynomial-time many-one reduction. $L$ is coNP-complete if and only if $\overline{L}$ is NP-complete, because $A \le_p B$ by a map $f$ exactly when $\overline{A} \le_p \overline{B}$ by the same $f$. See [coNP-complete](/co-np-complete/).
- *$\mathsf{NP} = \mathsf{coNP}$ if and only if some NP-complete language $L$ is in coNP.* If $L \in \mathsf{coNP}$, take any $A \in \mathsf{NP}$. Then $A \le_p L$, so $\overline{A} \le_p \overline{L}$ by the same map, and $\overline{L} \in \mathsf{NP}$. So $\overline{A} \in \mathsf{NP}$ and $A \in \mathsf{coNP}$. This gives $\mathsf{NP} \subseteq \mathsf{coNP}$, and taking complements gives $\mathsf{coNP} \subseteq \mathsf{NP}$. The other direction is clear.
- If $\mathsf{P} = \mathsf{NP}$, then $\mathsf{NP} = \mathsf{P} = \mathsf{coP} = \mathsf{coNP}$. So a proof of $\mathsf{NP} \ne \mathsf{coNP}$ would also prove $\mathsf{P} \ne \mathsf{NP}$. The converse is not known: $\mathsf{NP} = \mathsf{coNP}$ together with $\mathsf{P} \ne \mathsf{NP}$ is not ruled out.

**Proof systems.** Cook and Reckhow (1979) defined a propositional proof system as a polynomial-time function whose range is exactly the set of tautologies, and showed that $\mathsf{NP} = \mathsf{coNP}$ if and only if some proof system gives every tautology a proof of length polynomial in the length of the tautology. So a proof of $\mathsf{NP} \ne \mathsf{coNP}$ would need a superpolynomial lower bound for every proof system. Lower bounds are known for weak systems. For resolution, Haken (1985) proved that the pigeonhole tautologies need proofs of exponential length ([Haken's lower bound](/haken-resolution-lower-bound/)).

## Examples and non-examples

**Examples.**

- *Tautology.* TAUT is the set of Boolean formulas that are true under every assignment. A formula $\varphi$ is a tautology exactly when $\neg \varphi$ is unsatisfiable, and this map is a reduction from TAUT to UNSAT and back, so TAUT is coNP-complete. The formula $(x \to y) \lor (y \to x)$ is true in all 4 rows of its truth table. The formula $(x \to y) \to ((y \to z) \to (x \to z))$ is true in all 8 rows. The formula $(x \to y) \lor ((y \to z) \land z)$ is not a tautology: it is false at $x = 1, y = 0, z = 0$ and true in the other 7 rows. That one row is the certificate for the no-answer, and checking it takes one evaluation. A yes-answer, as far as anyone knows, needs a check of all $2^n$ rows or a proof in some proof system.
- *Primality.* A number $N$ is prime when no $d$ with $1 < d < N$ divides it, a "for all" statement, so primality is in coNP with a divisor as the certificate of compositeness. Pratt (1975) showed that primality is in NP too, so it is in $\mathsf{NP} \cap \mathsf{coNP}$. It is in P by the [AKS test](/aks-primality-test/).
- *Factoring.* "Does $N$ have a prime factor at most $k$?" is in $\mathsf{NP} \cap \mathsf{coNP}$: the full prime factorization, with a primality certificate for each factor, proves the answer in both directions. See [good characterization](/good-characterization/).
- *Graph non-isomorphism.* Are two graphs not isomorphic? This is the complement of the [graph isomorphism problem](/graph-isomorphism-problem/), so it is in coNP. It has an interactive proof with public coins and lies in [AM](/arthur-merlin/). It is not known to be in NP.
- *Every problem in P*, with the empty certificate.

**Non-examples and open cases.**

- *SAT, clique, 3-coloring and the other NP-complete problems* are not known to be in coNP. If one of them is, then $\mathsf{NP} = \mathsf{coNP}$. There is no known short proof that a formula is unsatisfiable or that a graph has no 3-coloring.
- *The halting problem and its complement* are undecidable, so they are in neither class.
- *Nondeterministic space is different.* For space, the analogous question has a positive answer: $\mathsf{NL} = \mathsf{coNL}$ and $\mathsf{NSPACE}(s(n)) = \mathsf{coNSPACE}(s(n))$ for $s(n) \ge \log n$ ([Immerman-Szelepcsényi theorem](/immerman-szelepcsenyi-theorem/)). No such result is known for nondeterministic time.

## Related definitions

- [NP](/np/) is the class of the complements. $\mathsf{NP} \cap \mathsf{coNP}$ is the class of problems with a [good characterization](/good-characterization/), a short proof for each answer.
- coNP is the level $\Pi_1^p$ of the [polynomial hierarchy](/polynomial-hierarchy/). If $\mathsf{NP} = \mathsf{coNP}$, the hierarchy collapses to its first level.
- The [Boolean hierarchy](/boolean-hierarchy/) studies differences of NP sets, such as $L_1 \cap \overline{L_2}$ with $L_1, L_2 \in \mathsf{NP}$.
- The prefix "co" names the class of complements in other settings too: [coRP](/co-rp/) is the class of complements of [RP](/rp/) languages, and coNL that of NL languages.
- coNP sits beside NP in the [chain of inclusions](/class-inclusions-chain/): $\mathsf{P} \subseteq \mathsf{NP} \cap \mathsf{coNP}$ and $\mathsf{NP} \cup \mathsf{coNP} \subseteq \mathsf{PSPACE}$.

## References
