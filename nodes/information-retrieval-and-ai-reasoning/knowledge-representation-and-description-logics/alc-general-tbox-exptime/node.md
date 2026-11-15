---
tag: 7HWPD2
kind: theorem
slug: alc-general-tbox-exptime
name: EXPTIME-completeness of ALC with general TBoxes
aliases:
- ALC general TBox complexity
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: advanced
summary: Concept satisfiability in ALC with respect to general concept inclusions is EXPTIME-complete.
prereqs: [alc-description-logic, tbox-and-abox, concept-satisfiability, exptime, alternating-turing-machine]
see_also: [alc-pspace-completeness, alc-modal-k-correspondence, alc-tableau-algorithm, tableau-blocking, hypertableau, concept-subsumption, el-description-logic, sroiq]
sources:
  - paper: doi:10.1016/0022-0000(79)90046-1
    title: Michael J. Fischer and Richard E. Ladner, Propositional dynamic logic of regular programs, Journal of Computer and System Sciences 18(2), 1979
    locator: pages 194 to 211 (the EXPTIME lower bound for propositional dynamic logic)
  - paper: "Vaughan R. Pratt, Models of program logics, Proceedings of the 20th Annual Symposium on Foundations of Computer Science (FOCS), 1979"
    locator: pages 115 to 122 (an exponential time decision procedure for propositional dynamic logic)
  - paper: doi:10.1145/322234.322243
    title: Ashok K. Chandra, Dexter C. Kozen and Larry J. Stockmeyer, Alternation, Journal of the ACM 28(1) (1981)
    locator: pp. 114 to 133 (alternating polynomial space equals deterministic exponential time)
  - paper: "Klaus Schild, A correspondence theory for terminological logics: preliminary report, Proceedings of the 12th International Joint Conference on Artificial Intelligence (IJCAI), 1991"
    locator: the translation of terminological logics into propositional dynamic logic and the complexity results that follow (general locator)
  - paper: "Francesco M. Donini and Fabio Massacci, EXPTIME tableaux for ALC, Artificial Intelligence 124(1), 2000, pages 87 to 138"
    locator: tableau calculi for ALC with general TBoxes that run in exponential time
  - paper: doi:10.1007/s10817-011-9243-0
    title: Rajeev Goré and Linh Anh Nguyen, ExpTime tableaux for ALC using sound global caching, Journal of Automated Reasoning 50(4), 2013
    locator: pages 355 to 381 (global caching of node labels, and the exponential time bound)
  - paper: "Carsten Lutz, Complexity of terminological reasoning revisited, Proceedings of the 6th International Conference on Logic for Programming and Automated Reasoning (LPAR'99), LNAI 1705, Springer, 1999"
    locator: ALC satisfiability with respect to acyclic TBoxes stays in PSPACE (general locator)
  - paper: "Yevgeny Kazakov, RIQ and SROIQ are harder than SHOIQ, Proceedings of the 11th International Conference on Principles of Knowledge Representation and Reasoning (KR), 2008"
    locator: pages 274 to 284 (SROIQ is N2EXPTIME-complete)
  - book: isbn:9780521695428
    title: Franz Baader, Ian Horrocks, Carsten Lutz and Ulrike Sattler, An Introduction to Description Logic, Cambridge University Press, 2017
    locator: Chapter 5 (the complexity of ALC with and without TBoxes)
---

Once a TBox may contain arbitrary inclusions $C \sqsubseteq D$, deciding whether an [ALC](/alc-description-logic/) concept is satisfiable becomes [EXPTIME](/exptime/)-complete. Without a TBox the problem is in PSPACE ([the PSPACE theorem](/alc-pspace-completeness/)). A cyclic inclusion such as $A \sqsubseteq \exists r.A$ forces infinite paths, so models no longer have bounded depth, and the problem can encode a machine that runs for exponentially many steps. The upper bound is an elimination of types in exponential time; the lower bound encodes an [alternating Turing machine](/alternating-turing-machine/) with polynomial space.

## Statement

ALC concepts use concept names, $\top$, $\bot$, $\neg$, $\sqcap$, $\sqcup$, $\exists r.C$ and $\forall r.C$. A *general TBox* $\mathcal T$ is a finite set of general concept inclusions $X \sqsubseteq Y$, where $X$ and $Y$ are any ALC concepts, so cycles are allowed. The input size $n$ is the number of symbols of the concept and of all the inclusions. There are no number restrictions, so the coding of numbers does not matter. $C$ is *satisfiable with respect to* $\mathcal T$ if some model $I$ of $\mathcal T$ has $C^I \ne \emptyset$.

**Theorem.** Each of the following problems is EXPTIME-complete under polynomial-time reductions.

1. Given $C$ and a general TBox $\mathcal T$, decide whether $C$ is satisfiable with respect to $\mathcal T$.
2. Given $C$, $D$ and $\mathcal T$, decide whether $C \sqsubseteq_{\mathcal T} D$, that is, $C^I \subseteq D^I$ in every model $I$ of $\mathcal T$.
3. Given $\mathcal T$, decide whether $\mathcal T$ has a model.

Satisfiability is decided in time $2^{O(n)}$. Hardness holds already when $C$ is a conjunction of concept names.

## In plain words

A TBox with general rules can say things like "every person has a parent who is a person". Rules like this can force models that never end. The question is then much harder than without rules. An algorithm can still answer it in exponential time: it lists every possible kind of object, described by the set of subconcepts that the object makes true, and it throws away kinds that need a neighbor that does not exist, until nothing changes. On the other side, rules can describe the steps of a machine that branches and uses a polynomial amount of memory. Such machines can solve every problem that takes exponential time, so no faster general method is expected.

## Proof

The full proof is in the proof file below. Here is its plan.

*Upper bound.* Let $C_{\mathcal T}$ be the negation normal form of the conjunction of $\neg X \sqcup Y$ over the inclusions. A model of $\mathcal T$ is an interpretation in which every element is in $C_{\mathcal T}$. Let $\mathrm{cl}$ be the subconcepts of $C$ and $C_{\mathcal T}$, closed under negation in normal form, so $|\mathrm{cl}| = O(n)$. A *type* is a subset of $\mathrm{cl}$ that contains $C_{\mathcal T}$, holds exactly one of each concept and its negation, and respects $\sqcap$ and $\sqcup$. Start with all types, at most $2^{|\mathrm{cl}|}$ of them. Remove, again and again, each type $t$ with some $\exists r.D \in t$ for which no remaining type contains $D$ and all $E$ with $\forall r.E \in t$. Accept if a remaining type contains $C$. There are at most $2^{|\mathrm{cl}|}$ rounds of $2^{O(|\mathrm{cl}|)}$ steps each. The remaining types, with an $r$-edge from $t$ to $t'$ when $t'$ contains every $E$ with $\forall r.E \in t$, form a model of $\mathcal T$ in which each type is in exactly its own concepts. In the other direction, the set of concepts that hold at an element of a model is a type, and it is never removed, because the successors of the element give it its witnesses.

*Lower bound.* By the theorem of Chandra, Kozen and Stockmeyer, every language in EXPTIME is decided by an alternating machine $M$ in polynomial space $p(n)$, and we may assume that every branch halts. For an input $w$, concept names $S_q$, $H_i$ and $T_{i,a}$ describe the state, the head position and the content of each of the $p(n)$ cells, and a role $r_\mu$ stands for each move $\mu$. The TBox says that each element is one configuration, that an existential configuration has a successor for some applicable move and a universal one for every applicable move, that each move changes the state, the head and the cell under it as $\mu$ says, that the other cells keep their contents, and that the rejecting state is empty. A model of the TBox that contains the initial configuration contains an accepting computation tree, by induction on the height of the computation from each configuration. In the other direction, the set of accepting configurations is a model. The TBox has $O(p(n)^2)$ axioms of size $O(p(n))$.

*Subsumption and consistency.* $C \sqsubseteq_{\mathcal T} D$ if and only if $C \sqcap \neg D$ is unsatisfiable with respect to $\mathcal T$. $C$ is satisfiable with respect to $\mathcal T$ if and only if $\mathcal T \cup \{\top \sqsubseteq \exists u.C\}$ has a model, for a new role name $u$.

For example, take $\mathcal T = \{A_1 \sqsubseteq \exists r.A_2,\ A_2 \sqsubseteq \exists r.A_3,\ A_3 \sqsubseteq \bot\}$ and $C = A_1$. A type is fixed by its choice of $A_1$, $A_2$, $A_3$, $\exists r.A_2$ and $\exists r.A_3$, and the inclusions leave 9 types, none with $A_3$. The first round removes the 6 types that contain $\exists r.A_3$, among them every type with $A_2$. The second round removes the 2 types that contain $\exists r.A_2$, among them every type with $A_1$. One type is left, with none of the five concepts, and $A_1$ is unsatisfiable.

## Consequences

- *Tableau algorithms.* The [ALC tableau](/alc-tableau-algorithm/) with [blocking](/tableau-blocking/) is a decision procedure for general TBoxes, but its standard worst-case bound is doubly exponential, so it is not optimal. Tableaux that reach the EXPTIME bound cache the results of node labels that were seen before; see Donini and Massacci (2000) and the global caching of Goré and Nguyen (2013). Practical reasoners, for example those based on the [hypertableau](/hypertableau/) calculus, put their effort into the cases that occur in real ontologies.
- *Classification.* Subsumption between all pairs of names, and so classification of a TBox, takes exponential time in the worst case.
- *Tractable fragments.* The hardness shows why tractable description logics restrict the constructors. In [EL](/el-description-logic/) subsumption with respect to general TBoxes is in polynomial time.
- *Modal logic.* By [Schild's correspondence](/alc-modal-k-correspondence/), the theorem is the same as the EXPTIME-completeness of multimodal K with the universal modality.

## Tightness

- *Acyclic TBoxes.* If the TBox only defines concept names, without cycles, the problem stays in PSPACE (Lutz 1999), so general inclusions are what raise the complexity.
- *Bound.* The time bound $2^{O(n)}$ cannot be improved to a polynomial, because P is a proper subset of EXPTIME by the time hierarchy theorem.
- *Larger logics.* Some extensions of ALC are harder. For example, [SROIQ](/sroiq/), the logic of OWL 2 DL, is N2EXPTIME-complete (Kazakov 2008).

## History

Fischer and Ladner proved in 1979 that propositional dynamic logic (PDL) is EXPTIME-hard, by an encoding of alternating machines with linear space. In the same year Pratt gave a decision procedure for PDL in exponential time, by eliminating Hintikka sets that cannot be satisfied. Chandra, Kozen and Stockmeyer published the theory of alternation in 1981. Schild showed in 1991 that ALC is a notational variant of multimodal K and that terminological logics with general inclusions can be translated into PDL, so these bounds apply. The textbook of Baader, Horrocks, Lutz and Sattler (2017) proves the theorem directly for ALC. Optimal tableau procedures came later, from Donini and Massacci in 2000 and from Goré and Nguyen with global caching.

## References
