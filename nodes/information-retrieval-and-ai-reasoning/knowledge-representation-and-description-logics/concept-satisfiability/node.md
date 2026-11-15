---
tag: 0G8WMV
kind: problem
slug: concept-satisfiability
name: Concept satisfiability
aliases:
- concept consistency
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: core
summary: Decide whether a concept can have an instance in some model of the TBox.
prereqs: [alc-description-logic, tbox-and-abox]
see_also: [concept-subsumption, alc-tableau-algorithm, tableau-blocking, alc-pspace-completeness, alc-general-tbox-exptime, alc-modal-k-correspondence, pspace, exptime]
sources:
  - paper: doi:10.1016/0004-3702(91)90078-X
    title: Manfred Schmidt-Schauß and Gert Smolka, Attributive concept descriptions with complements, Artificial Intelligence 48(1), 1991
    locator: pages 1 to 26 (satisfiability and subsumption of ALC concepts are PSPACE-complete)
  - book: isbn:9780521695428
    title: Franz Baader, Ian Horrocks, Carsten Lutz and Ulrike Sattler, An Introduction to Description Logic, Cambridge University Press, 2017
    locator: Chapter 2 (reasoning tasks and their reductions), Chapter 4 (tableau algorithms) and Chapter 5 (the complexity of ALC with and without TBoxes)
  - book: isbn:9780521876254
    title: Franz Baader, Diego Calvanese, Deborah L. McGuinness, Daniele Nardi and Peter F. Patel-Schneider (eds.), The Description Logic Handbook, second edition, Cambridge University Press, 2007
    locator: Chapter 3, Complexity of Reasoning, by Francesco M. Donini (the complexity results for the AL family)
  - paper: "Klaus Schild, A correspondence theory for terminological logics: preliminary report, Proceedings of the 12th International Joint Conference on Artificial Intelligence (IJCAI), 1991"
    locator: the correspondence with modal logic K and propositional dynamic logic, and the EXPTIME bound for general inclusions (general locator)
  - paper: doi:10.1016/0022-0000(79)90046-1
    title: Michael J. Fischer and Richard E. Ladner, Propositional dynamic logic of regular programs, Journal of Computer and System Sciences 18(2), 1979
    locator: pages 194 to 211 (the EXPTIME lower bound for propositional dynamic logic)
  - paper: "Carsten Lutz, Complexity of terminological reasoning revisited, Proceedings of the 6th International Conference on Logic for Programming and Automated Reasoning (LPAR'99), LNAI 1705, Springer, 1999"
    locator: ALC satisfiability with respect to acyclic TBoxes stays in PSPACE (general locator)
  - paper: "Yevgeny Kazakov, RIQ and SROIQ are harder than SHOIQ, Proceedings of the 11th International Conference on Principles of Knowledge Representation and Reasoning (KR 2008)"
    locator: SROIQ satisfiability is N2EXPTIME-complete (general locator)
---

Concept satisfiability is the problem of deciding whether a concept $C$ can have an instance: whether some model $I$ of a TBox $T$ has $C^I \neq \emptyset$. A concept that cannot is a modelling error, and many other reasoning tasks reduce to this one. For [ALC](/alc-description-logic/) it is PSPACE-complete without a TBox and EXPTIME-complete with a general TBox.

## In plain words

You have a set of background rules and a description of a kind of thing. The question is whether the description can be true of anything at all, in some world where every rule holds. "A parent with no children" cannot be true of anything, because a parent has a child by definition. Such a description is a mistake in the rules or in the description. A program finds these mistakes by trying to build a small world in which some object fits the description, and it reports success or a proof that no such world exists.

## Definition

The logic is ALC, with interpretations $I = (\Delta^I, \cdot^I)$ as on its page, and a TBox is a finite set of GCIs $C \sqsubseteq D$ (see [TBox and ABox](/tbox-and-abox/)).

- **Input.** An ALC concept $C$ and a TBox $T$. The size $n$ of the input is $|C|$ plus the sizes of the concepts in $T$.
- **Question.** Is there a model $I$ of $T$ with $C^I \neq \emptyset$?

If the answer is yes, $C$ is *satisfiable with respect to* $T$. If $T = \emptyset$, $C$ is *satisfiable*. The input has no ABox, so the complexity on this page is combined complexity: it is measured in the size of the concept and the TBox together.

## Variants

- **Empty TBox.** Satisfiability of a single concept.
- **Acyclic TBox.** The TBox holds only definitions $A \equiv C$ and $A \sqsubseteq C$ without cycles.
- **General TBox.** Any finite set of GCIs.
- **Knowledge base consistency.** The input also has an ABox, and the question is whether $(T, A)$ has a model.
- **Finite satisfiability.** The model must be finite. For ALC this is the same problem, because ALC has the finite model property, also with general TBoxes.
- **Other logics.** In [EL](/el-description-logic/) without $\bot$ every concept is satisfiable, so the problem is trivial. In larger logics the cost rises: SROIQ, the logic of OWL 2 DL, is N2EXPTIME-complete (Kazakov 2008).

## Examples

- $\exists r.A \sqcap \forall r.(\neg A \sqcup B) \sqcap \forall r.\neg B$ is not satisfiable. An instance has an $r$-successor $y$ in $A$, and $y$ must also be in $\neg A \sqcup B$ and in $\neg B$. Both choices for the disjunction fail.
- $A \sqcap \neg B \sqcap \exists r.(\neg A \sqcap B \sqcap \exists r.(\neg A \sqcap \neg B \sqcap \exists r.(A \sqcap B)))$ is satisfiable by an $r$-chain of 4 elements. An instance and the successors that the concept asks for have the 4 different combinations of $A$ and $B$, so they are 4 different elements, and no model has 3 elements. A search over small interpretations cannot prove that a concept is unsatisfiable.
- With $T = \{A \sqsubseteq \exists r.A\}$, $A$ is satisfiable, for example by one element in $A$ with an $r$-edge to itself. Each model of $T$ in which $A$ is not empty has an $r$-cycle or an infinite $r$-chain.
- With $T = \{A \sqsubseteq \exists r.A,\ A \sqsubseteq \forall r.\neg A\}$, $A$ is not satisfiable: an element in $A$ needs an $r$-successor in $A$, and all its $r$-successors must be outside $A$.

## Known algorithms

- **The [tableau algorithm for ALC](/alc-tableau-algorithm/).** It tries to build a tree-shaped model. Without a TBox it runs in polynomial space. With a general TBox it needs [blocking](/tableau-blocking/), and its simple form takes double exponential time.
- **Tableaux with caching.** EXPTIME tableaux share the result of each label that was seen. They match the EXPTIME bound for general TBoxes.
- **Optimized reasoners.** Practical reasoners use tableaux or the [hypertableau](/hypertableau/) calculus, with absorption, backjumping and caching.
- **For EL.** Satisfiability with $\bot$ falls out of [EL classification](/el-classification/) in polynomial time.

## Bounds

| logic and TBox | complexity | source |
|---|---|---|
| ALC, empty TBox | PSPACE-complete | Schmidt-Schauß and Smolka 1991 |
| ALC, acyclic TBox | PSPACE-complete | Lutz 1999 |
| ALC, general TBox | EXPTIME-complete | Schild 1991, with Fischer and Ladner 1979 |
| EL with $\bot$, general TBox | in P | see [EL classification](/el-classification/) |
| SROIQ | N2EXPTIME-complete | Kazakov 2008 |

The proofs for ALC are on the pages [ALC is PSPACE-complete](/alc-pspace-completeness/) and [ALC with general TBoxes is EXPTIME-complete](/alc-general-tbox-exptime/). The upper bound without a TBox comes from a tableau that keeps one branch at a time. The EXPTIME lower bound comes from the hardness of propositional dynamic logic. So the problem with a general TBox is not in [PSPACE](/pspace/) unless PSPACE = [EXPTIME](/exptime/), and it has no polynomial-time algorithm, because P is a proper subset of EXPTIME.

## Reductions

- **To and from subsumption.** $C$ is satisfiable with respect to $T$ if and only if $C \sqsubseteq_T \bot$ does not hold. In the other direction, $C \sqsubseteq_T D$ holds if and only if $C \sqcap \neg D$ is not satisfiable with respect to $T$. See [concept subsumption](/concept-subsumption/).
- **To consistency.** $C$ is satisfiable with respect to $T$ if and only if the knowledge base $(T, \{C(a)\})$ is consistent, for a new individual name $a$.
- **To and from modal logic.** ALC concepts are formulas of the multimodal logic K, and a general TBox acts as a universal modality. See [ALC and modal logic K](/alc-modal-k-correspondence/).

## Applications

- **Finding modelling errors.** An ontology editor reports each concept name that is unsatisfiable with respect to the TBox, since no instance can ever have that name.
- **Subsumption and classification.** By the reduction above, a satisfiability procedure answers subsumption questions, and so builds the class hierarchy of an ontology ([ontology classification](/ontology-classification/)).

## References
