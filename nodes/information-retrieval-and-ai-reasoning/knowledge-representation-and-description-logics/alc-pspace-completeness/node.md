---
tag: VX9NF7
kind: theorem
slug: alc-pspace-completeness
name: PSPACE-completeness of ALC concept satisfiability
aliases:
- Schmidt-Schauss-Smolka complexity theorem
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: advanced
summary: Satisfiability of ALC concepts with no TBox is PSPACE-complete, by a depth-first tableau and a reduction from QBF.
prereqs: [alc-description-logic, concept-satisfiability, pspace, qbf]
see_also: [alc-tableau-algorithm, alc-general-tbox-exptime, alc-modal-k-correspondence, concept-subsumption, tbox-and-abox, polynomial-time-reduction, np-complete, savitch-theorem]
sources:
  - paper: doi:10.1016/0004-3702(91)90078-X
    title: Manfred Schmidt-Schauß and Gert Smolka, Attributive concept descriptions with complements, Artificial Intelligence 48(1), 1991
    locator: pages 1 to 26 (the tableau calculus for ALC, and the proof that satisfiability and subsumption are PSPACE-complete)
  - paper: doi:10.1137/0206033
    title: Richard E. Ladner, The computational complexity of provability in systems of modal propositional logic, SIAM Journal on Computing 6(3), 1977
    locator: pages 467 to 480 (satisfiability in the modal logic K is PSPACE-complete)
  - paper: "Carsten Lutz, Complexity of terminological reasoning revisited, Proceedings of the 6th International Conference on Logic for Programming and Automated Reasoning (LPAR'99), LNAI 1705, Springer, 1999"
    locator: ALC satisfiability with respect to acyclic TBoxes stays in PSPACE (general locator)
  - book: isbn:9780521695428
    title: Franz Baader, Ian Horrocks, Carsten Lutz and Ulrike Sattler, An Introduction to Description Logic, Cambridge University Press, 2017
    locator: Chapter 5 (the complexity of ALC concept satisfiability without a TBox, the PSPACE upper bound and the lower bound)
  - book: isbn:9780521876254
    title: Franz Baader, Diego Calvanese, Deborah L. McGuinness, Daniele Nardi and Peter F. Patel-Schneider (eds.), The Description Logic Handbook, second edition, Cambridge University Press, 2007
    locator: Chapter 3, Complexity of Reasoning, by Francesco M. Donini (the complexity of ALC and of its sublanguages, general locator)
---

Schmidt-Schauß and Smolka proved in 1991 that it is PSPACE-complete to decide whether an [ALC](/alc-description-logic/) concept is satisfiable when there is no TBox. The upper bound comes from a [tableau](/alc-tableau-algorithm/) that explores a tree model depth first and keeps only one branch in memory. The lower bound is a reduction from the truth of [quantified Boolean formulas](/qbf/). The same bound holds for [subsumption](/concept-subsumption/), and it is the bound of the modal logic K that Ladner proved in 1977.

## Statement

ALC concepts are built from concept names, $\top$ and $\bot$ with negation $\neg$, conjunction $\sqcap$, disjunction $\sqcup$, existential restriction $\exists r.C$ and universal restriction $\forall r.C$, for role names $r$. The size $|C|$ of a concept is the number of symbols in it. The constructors have no numbers, so there is no question of unary or binary coding. The TBox is empty: $C$ is *satisfiable* if $C^I \neq \emptyset$ for some interpretation $I$, and $C \sqsubseteq D$ if $C^I \subseteq D^I$ for every $I$.

**Theorem.** The following problems are [PSPACE](/pspace/)-complete under polynomial-time many-one reductions.

1. Given an ALC concept $C$, decide whether $C$ is satisfiable.
2. Given ALC concepts $C$ and $D$, decide whether $C \sqsubseteq D$.

Both problems are PSPACE-hard already when there is only one role name. Satisfiability is decided in $O(|C|^2)$ space.

The upper bound stays true for satisfiability with respect to an acyclic TBox, in which every concept name is defined at most once and no name depends on itself (Lutz 1999). This extension is not proved here. With a general TBox the problem is EXPTIME-complete; see [the general TBox theorem](/alc-general-tbox-exptime/).

## In plain words

To check whether an ALC concept can be true of anything, you build a tree of objects that the concept forces to exist. That tree can be very large, but its depth is at most the nesting depth of the concept. You can explore it one path at a time and forget each path when you are done, so the memory you need grows only with the depth. In the other direction, any puzzle about formulas of the form "for every x there is a y such that ..." can be written as one ALC concept. So ALC is exactly as hard as those puzzles, which are believed to need more than polynomial time.

## Proof

The full proof is in the proof file below. Here is its plan.

*Upper bound.* Put $C$ in negation normal form. A *completion* of a set $S$ of subconcepts of $C$ is a superset that contains both conjuncts of each conjunction in it, one disjunct of each disjunction in it, and no clash ($\bot$, or $A$ together with $\neg A$). The procedure $\mathrm{SAT}(S)$ tries every completion $S'$ of $S$. For each $\exists r.D \in S'$ it calls itself on the successor set $\{D\} \cup \{E : \forall r.E \in S'\}$, and it accepts $S'$ if all these calls accept. A successor set has smaller role depth than $S$, so the recursion has at most $|C| + 1$ levels. Each level stores one completion as a bit vector over the at most $2|C|$ subconcepts, which also counts the loop, and the position of the current existential restriction. This gives $O(|C|^2)$ space. Soundness builds a tree model from the accepting calls: a new root with an $r$-edge to the model of each successor set. Completeness reads the completion off a model: the set of subconcepts that hold at an element is a completion, and each $r$-witness of an existential restriction is in every concept of the successor set.

*Lower bound.* Let $\varphi = Q_1 p_1 \cdots Q_m p_m.\, \psi$ be a closed quantified Boolean formula with $\psi$ propositional. With one role $r$ and concept names $P_1, \ldots, P_m$, the concept $C_\varphi$ says, for each depth $i < m$ along $r$:

- if $Q_{i+1} = \forall$, there is an $r$-successor in $P_{i+1}$ and one in $\neg P_{i+1}$; if $Q_{i+1} = \exists$, there is an $r$-successor;
- every $r$-successor keeps the values of $P_1, \ldots, P_i$;

and at depth $m$, the concept $\psi'$ obtained from $\psi$ by reading $p_j$ as $P_j$ holds. Each condition at depth $i$ is put under $i$ nested $\forall r$. There are $O(m^2)$ conjuncts of size $O(m + |\psi|)$. A winning strategy for the existential player in $\varphi$ gives a tree model of $C_\varphi$. Conversely, in any model of $C_\varphi$, induction from depth $m$ up to the root shows that the formula that remains after the first $i$ quantifiers is true under the values at any element at depth $i$. So $\varphi$ is true if and only if $C_\varphi$ is satisfiable.

*Subsumption.* $C \sqsubseteq D$ holds if and only if $C \sqcap \neg D$ is unsatisfiable, and $C$ is satisfiable if and only if $C \not\sqsubseteq \bot$. PSPACE is closed under complement, so the two problems have the same complexity.

For example, $\forall p_1 \exists p_2.\, (p_1 \vee p_2) \wedge (\neg p_1 \vee \neg p_2)$ is true, because $p_2$ can be chosen as the negation of $p_1$. Its concept has four conjuncts:

$$(\exists r.P_1 \sqcap \exists r.\neg P_1) \;\sqcap\; \forall r.\exists r.\top \;\sqcap\; \forall r.\big((\neg P_1 \sqcup \forall r.P_1) \sqcap (P_1 \sqcup \forall r.\neg P_1)\big) \;\sqcap\; \forall r.\forall r.\big((P_1 \sqcup P_2) \sqcap (\neg P_1 \sqcup \neg P_2)\big).$$

A model has five elements: a root, a child $a$ in $P_1$ with a child $a'$ in $P_1$ and not in $P_2$, and a child $b$ not in $P_1$ with a child $b'$ in $P_2$ only. If the two quantifiers are both $\forall$, or are swapped to $\exists p_1 \forall p_2$, the formula is false and the concept is unsatisfiable.

## Consequences

- Subsumption, equivalence and disjointness of ALC concepts without a TBox are PSPACE-complete, by the reductions above.
- ALC is a notational variant of the multimodal logic $\mathrm{K}_m$ ([Schild's correspondence](/alc-modal-k-correspondence/)). The theorem is the description logic form of Ladner's result that satisfiability in K is PSPACE-complete, and either proof gives the other.
- A satisfiable ALC concept can need a model of exponential size. When all quantifiers of $\varphi$ are $\forall$, the elements at depth $m$ of any model of $C_\varphi$ realize all $2^m$ assignments, and elements with different assignments are different. The upper bound avoids this size because it never keeps more than one path of the tree.
- The procedure is deterministic and uses polynomial space. A nondeterministic version that guesses one completion per level also works, and [Savitch's theorem](/savitch-theorem/) turns it into a deterministic one, but this is not needed here.

## Tightness

- *General TBoxes.* With a general TBox the problem is EXPTIME-complete, so it is not in PSPACE unless PSPACE = EXPTIME. A cyclic inclusion such as $A \sqsubseteq \exists r.A$ removes the bound on the depth of the models.
- *Bounded role depth.* If the role depth of the input is at most a fixed $k$, the tree model built in the upper bound has at most $\sum_{i \le k} |C|^i$ nodes, a polynomial. A nondeterministic machine can guess it and check it, so the problem is in NP. It is NP-hard already for $k = 0$, which is propositional satisfiability, so it is [NP-complete](/np-complete/).
- *Fewer constructors.* The hardness proof uses disjunction, both kinds of restriction and negation of names. Donini and coauthors classified the sublanguages of ALC. For example, ALE has existential and universal restrictions but no disjunction, and its satisfiability problem is in coNP. ALU has disjunction but only the unqualified restriction $\exists r.\top$, and its satisfiability problem is in NP. So neither is PSPACE-hard unless NP = PSPACE. The handbook chapter by Donini gives the full table.
- *One role is enough.* The reduction uses a single role name, so the hardness does not come from having many roles.

## History

Schmidt-Schauß and Smolka introduced ALC in their journal paper of 1991. They gave a tableau-style calculus for it and proved that satisfiability and subsumption are PSPACE-complete. Ladner had proved in 1977 that satisfiability in the modal logics K, T and S4 is PSPACE-complete. Schild observed in 1991 that ALC is a syntactic variant of multimodal K, so Ladner's results apply directly. Lutz showed in 1999 that acyclic TBoxes do not raise the complexity, if the algorithm expands defined names lazily instead of unfolding the TBox first. The textbook of Baader, Horrocks, Lutz and Sattler (2017) gives the upper bound and a lower bound by reduction from QBF.

## References
