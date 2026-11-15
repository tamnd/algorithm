---
tag: 88CGEK
kind: problem
slug: concept-subsumption
name: Concept subsumption
aliases:
- subsumption checking in description logics
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: core
summary: Decide whether every instance of concept C is an instance of concept D in every model of the TBox.
prereqs: [alc-description-logic, tbox-and-abox, concept-satisfiability]
see_also: [ontology-classification, alc-tableau-algorithm, structural-subsumption, el-classification, alc-pspace-completeness, alc-general-tbox-exptime, query-containment-problem, instance-checking]
sources:
  - book: isbn:9780521695428
    title: Franz Baader, Ian Horrocks, Carsten Lutz and Ulrike Sattler, An Introduction to Description Logic, Cambridge University Press, 2017
    locator: Chapter 2 (subsumption and its reduction to satisfiability), Chapter 5 (complexity) and Chapter 6 (subsumption in EL)
  - book: isbn:9780521876254
    title: Franz Baader, Diego Calvanese, Deborah L. McGuinness, Daniele Nardi and Peter F. Patel-Schneider (eds.), The Description Logic Handbook, second edition, Cambridge University Press, 2007
    locator: Chapter 2, Basic Description Logics, by Franz Baader and Werner Nutt, Section 2.3 (structural subsumption and tableau algorithms), and Chapter 3, Complexity of Reasoning, by Francesco M. Donini
  - paper: doi:10.1016/0004-3702(91)90078-X
    title: Manfred Schmidt-Schauß and Gert Smolka, Attributive concept descriptions with complements, Artificial Intelligence 48(1), 1991
    locator: pages 1 to 26 (subsumption in ALC is PSPACE-complete)
  - paper: "Ronald J. Brachman and Hector J. Levesque, The tractability of subsumption in frame-based description languages, Proceedings of the National Conference on Artificial Intelligence (AAAI-84), 1984"
    locator: subsumption in FL- is polynomial, and adding role restrictions makes it coNP-hard (general locator)
  - paper: "Bernhard Nebel, Terminological reasoning is inherently intractable, Artificial Intelligence 43, 1990"
    locator: subsumption with respect to acyclic TBoxes is coNP-hard already for a small language (general locator)
  - paper: "Franz Baader, Sebastian Brandt and Carsten Lutz, Pushing the EL envelope, Proceedings of the 19th International Joint Conference on Artificial Intelligence (IJCAI), 2005"
    locator: polynomial subsumption in EL++ with general TBoxes, and EXPTIME-hardness of extensions (general locator)
---

Concept subsumption is the problem of deciding whether a concept $D$ is more general than a concept $C$ with respect to a TBox $T$: whether $C^I \subseteq D^I$ in every model $I$ of $T$. It is the central task of description logic reasoners, since the class hierarchy of an ontology is made of subsumptions. In [ALC](/alc-description-logic/) it reduces to [concept satisfiability](/concept-satisfiability/) and has the same complexity, while in logics without negation it is the main problem on its own.

## In plain words

You have background rules and two descriptions. The question is whether everything that fits the first description must also fit the second, in every world where the rules hold. "A woman with a child" always fits "a parent", once the rules say what a woman and a parent are. The answer must hold in all worlds, not only in the facts you have written down. A program can check it by trying to build a world with a thing that fits the first description but not the second. If no such world exists, the first description is a special case of the second.

## Definition

The logic is ALC with interpretations $I = (\Delta^I, \cdot^I)$, and a TBox is a finite set of GCIs (see [TBox and ABox](/tbox-and-abox/)).

- **Input.** ALC concepts $C$ and $D$, and a TBox $T$. The size $n$ is $|C| + |D|$ plus the size of $T$.
- **Question.** Is $C^I \subseteq D^I$ for every model $I$ of $T$?

If the answer is yes, $C$ is *subsumed by* $D$ with respect to $T$, written $C \sqsubseteq_T D$ or $T \models C \sqsubseteq D$. $C$ and $D$ are *equivalent* with respect to $T$, $C \equiv_T D$, when each subsumes the other. As for satisfiability, there is no ABox, and the complexity is combined complexity.

## Variants

- **Empty, acyclic or general TBox.** As on the page for satisfiability.
- **Between concept names.** Subsumption between two names of the TBox. This is the step that [ontology classification](/ontology-classification/) repeats.
- **Logics without full negation.** In FL0, EL and their relatives, subsumption cannot be reduced to satisfiability, and it has its own algorithms and bounds.

## Examples

- $\exists r.A \sqcap \forall r.B \sqsubseteq \exists r.(A \sqcap B)$ holds with the empty TBox. The $r$-successor in $A$ is also in $B$.
- $\forall r.(A \sqcap B) \equiv \forall r.A \sqcap \forall r.B$ and $\exists r.(A \sqcup B) \equiv \exists r.A \sqcup \exists r.B$.
- $\forall r.A \sqcup \forall r.B \sqsubseteq \forall r.(A \sqcup B)$ holds, but not the converse. A counterexample is an element with an $r$-successor in $A$ but not $B$, and another in $B$ but not $A$.
- $\exists r.(A \sqcap B) \sqsubseteq \exists r.A \sqcap \exists r.B$ holds, but not the converse: two different successors can carry $A$ and $B$.
- With $T = \{A \sqsubseteq \exists r.A,\ A \sqsubseteq B,\ \exists r.B \sqsubseteq C\}$, $A \sqsubseteq_T C$ holds: an element of $A$ has an $r$-successor in $A$, so in $B$, so the element is in $\exists r.B$ and in $C$. The subsumption fails with the empty TBox.
- With the family TBox $\mathit{Woman} \equiv \mathit{Person} \sqcap \mathit{Female}$, $\mathit{Mother} \equiv \mathit{Woman} \sqcap \exists \mathit{hasChild}.\mathit{Person}$ and $\mathit{Parent} \equiv \mathit{Person} \sqcap \exists \mathit{hasChild}.\mathit{Person}$, the subsumption $\mathit{Mother} \sqsubseteq_T \mathit{Parent}$ holds.

## Known algorithms

- **Reduce to satisfiability.** Test whether $C \sqcap \neg D$ is satisfiable with respect to $T$, for example with the [tableau algorithm for ALC](/alc-tableau-algorithm/). The subsumption holds if and only if the test fails.
- **[Structural subsumption](/structural-subsumption/).** Bring both concepts to a normal form and compare their parts. This is complete for small logics without disjunction and full negation, such as FL- and FL0 with the empty TBox.
- **Saturation for EL.** [EL classification](/el-classification/) derives all subsumptions between names of an EL TBox in polynomial time.

## Bounds

| logic and TBox | complexity | source |
|---|---|---|
| ALC, empty or acyclic TBox | PSPACE-complete | by the reduction, from satisfiability |
| ALC, general TBox | EXPTIME-complete | by the reduction, from satisfiability |
| FL-, empty TBox | in P | Brachman and Levesque 1984 |
| FL- with role restrictions, empty TBox | coNP-hard | Brachman and Levesque 1984 |
| FL0, acyclic TBox | coNP-hard | Nebel 1990 |
| EL, general TBox | in P | Baader, Brandt and Lutz 2005 |

For ALC the reduction runs both ways in polynomial time, so the bounds are those of [concept satisfiability](/concept-satisfiability/), with proofs on [ALC is PSPACE-complete](/alc-pspace-completeness/) and [ALC with general TBoxes is EXPTIME-complete](/alc-general-tbox-exptime/). PSPACE and EXPTIME are closed under complement, so moving from satisfiability to its complement does not change the class.

## Reductions

- **To unsatisfiability.** $C \sqsubseteq_T D$ if and only if $C \sqcap \neg D$ is not satisfiable with respect to $T$. This needs $\neg$, so it works in ALC but not in EL.
- **From unsatisfiability.** $C$ is not satisfiable with respect to $T$ if and only if $C \sqsubseteq_T \bot$.
- **To instance checking.** $C \sqsubseteq_T D$ if and only if $(T, \{C(a)\}) \models D(a)$ for a new individual name $a$. See [instance checking](/instance-checking/).
- **Query containment.** Subsumption is the description logic form of [query containment](/query-containment-problem/): a concept is a query with one answer variable, and $C \sqsubseteq_T D$ says that every answer to $C$ is an answer to $D$.

## Applications

- **Class hierarchies.** Ontology tools compute the subsumptions between all concept names and show them as a hierarchy.
- **Checking a new definition.** A modeller adds a definition and asks where it falls in the hierarchy, or whether it is equivalent to a name that is already there.
- **Answering queries.** A query concept that subsumes a stored concept returns all its instances, which lets a system answer by the hierarchy.

## References
