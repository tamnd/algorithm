---
tag: 38CBMT
kind: problem
slug: instance-checking
name: Instance checking
aliases:
- ABox instance checking
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: core
summary: Decide whether an individual is an instance of a concept in every model of the knowledge base.
prereqs: [tbox-and-abox, concept-satisfiability, open-world-assumption]
see_also: [concept-subsumption, alc-tableau-algorithm, ontology-mediated-query-answering, dl-lite, perfectref-rewriting, el-classification, co-np, ac0]
sources:
  - book: isbn:9780521876254
    title: Franz Baader, Diego Calvanese, Deborah L. McGuinness, Daniele Nardi and Peter F. Patel-Schneider (eds.), The Description Logic Handbook, second edition, Cambridge University Press, 2007
    locator: Chapter 2, Basic Description Logics, by Franz Baader and Werner Nutt (reasoning with ABoxes, the Oedipus example), and Chapter 3, Complexity of Reasoning, by Francesco M. Donini
  - book: isbn:9780521695428
    title: Franz Baader, Ian Horrocks, Carsten Lutz and Ulrike Sattler, An Introduction to Description Logic, Cambridge University Press, 2017
    locator: Chapter 2 (instance checking and its reduction to consistency), Chapter 4, Section 4.2.1 (the tableau for ABox consistency) and Chapter 7 (query answering)
  - paper: doi:10.1007/BF00962071
    title: Andrea Schaerf, On the complexity of the instance checking problem in concept languages with existential quantification, Journal of Intelligent Information Systems 2(3), 1993
    locator: pages 265 to 278 (coNP-hardness in the size of the ABox for a language with existential restrictions)
  - paper: "Ullrich Hustadt, Boris Motik and Ulrike Sattler, Data complexity of reasoning in very expressive description logics, Proceedings of the 19th International Joint Conference on Artificial Intelligence (IJCAI), 2005"
    locator: instance checking in SHIQ is coNP-complete in data complexity (general locator)
  - paper: "Diego Calvanese, Giuseppe De Giacomo, Domenico Lembo, Maurizio Lenzerini and Riccardo Rosati, Tractable reasoning and efficient query answering in description logics: the DL-Lite family, Journal of Automated Reasoning 39(3), 2007"
    locator: query answering over DL-Lite knowledge bases by rewriting, with data complexity in AC0 (general locator)
---

Instance checking is the problem of deciding whether an individual $a$ is an instance of a concept $C$ in every model of a knowledge base $K = (T, A)$, written $K \models C(a)$. Because of the [open-world assumption](/open-world-assumption/), the ABox is not a database: the answer depends on what holds in all models, and it can need a case analysis that no single model shows. For [ALC](/alc-description-logic/) it has the same combined complexity as satisfiability, and it is coNP-complete in the size of the ABox.

## In plain words

You have background rules and a list of facts about named things, such as "Mary has the child Peter". The question is whether a named thing must belong to a kind, given the rules and the facts. "Must" means in every world that agrees with all the rules and facts. A fact that is missing from the list is not false; it is unknown. So the answer can be no even when the list gives no reason against it. The answer can also be yes when no single fact says so, because every possible world gives a reason, only a different one in each world.

## Definition

The logic is ALC with interpretations $I = (\Delta^I, \cdot^I)$. A knowledge base $K = (T, A)$ has a TBox of GCIs and an ABox of assertions $C(a)$ and $r(a, b)$ (see [TBox and ABox](/tbox-and-abox/)). The unique name assumption is not made.

- **Input.** A knowledge base $K = (T, A)$, an individual name $a$ and a concept $C$.
- **Question.** Is $a^I \in C^I$ for every model $I$ of $K$?

The complexity has two measures. *Combined complexity* counts the size of the whole input. *Data complexity* fixes $T$ and $C$, and counts only the size of the ABox $A$. Data complexity matters when a small ontology meets a large set of facts.

## Variants

- **Knowledge base consistency.** Does $K$ have a model at all?
- **Retrieval.** Find all individuals $a$ with $K \models C(a)$.
- **Realization.** For each individual, find the most specific concept names of the TBox that it is an instance of.
- **Conjunctive query answering.** Find all tuples of individuals that match a conjunction of atoms with existential variables. Instance checking is the case of one atom. See [ontology-mediated query answering](/ontology-mediated-query-answering/).

## Examples

- Take the ABox with $\mathit{hasChild}(\mathit{iokaste}, \mathit{oedipus})$, $\mathit{hasChild}(\mathit{iokaste}, \mathit{polyneikes})$, $\mathit{hasChild}(\mathit{oedipus}, \mathit{polyneikes})$, $\mathit{hasChild}(\mathit{polyneikes}, \mathit{thersandros})$, $\mathit{Patricide}(\mathit{oedipus})$ and $\neg \mathit{Patricide}(\mathit{thersandros})$, and the empty TBox. The query is $(\exists \mathit{hasChild}.(\mathit{Patricide} \sqcap \exists \mathit{hasChild}.\neg \mathit{Patricide}))(\mathit{iokaste})$.
- The ABox does not say whether Polyneikes is a patricide. In a model where he is, the child Polyneikes of Iokaste has the child Thersandros, who is not. In a model where he is not, the child Oedipus of Iokaste has the child Polyneikes, who is not. So the query is entailed, but no single child of Iokaste is the witness in every model.
- With the same ABox, $\mathit{Patricide}(\mathit{polyneikes})$ is not entailed, and $\neg \mathit{Patricide}(\mathit{polyneikes})$ is not entailed either.
- With the ABox $\{\mathit{hasChild}(\mathit{mary}, \mathit{peter}),\ \mathit{Female}(\mathit{peter})\}$, the assertion $(\forall \mathit{hasChild}.\mathit{Female})(\mathit{mary})$ is not entailed: some models give Mary another child who is not female.

## Known algorithms

- **Reduce to consistency.** $K \models C(a)$ if and only if $(T, A \cup \{\neg C(a)\})$ is not consistent. Run the [tableau algorithm](/alc-tableau-algorithm/) from the ABox: one node for each individual, with its assertions, and the role assertions as edges. The ⊔-rule does the case analysis of the Oedipus example.
- **Saturation for EL.** The rules of [EL classification](/el-classification/) also apply to ABox assertions, in polynomial time.
- **Rewriting for DL-Lite.** Rewrite the query with the TBox, then evaluate it on the ABox as a database query ([PerfectRef](/perfectref-rewriting/)).

## Bounds

| logic and TBox | combined complexity | data complexity |
|---|---|---|
| ALC, empty or acyclic TBox | PSPACE-complete | coNP-complete |
| ALC, general TBox | EXPTIME-complete | coNP-complete |
| EL, general TBox | in P | in P |
| [DL-Lite](/dl-lite/) | in P | in [AC0](/ac0/) (Calvanese and others 2007) |

The combined bounds for ALC follow from those of [concept satisfiability](/concept-satisfiability/) by the reductions below, and the upper bounds hold for consistency of knowledge bases with ABoxes (DL Handbook, Chapter 3; Baader and others 2017, Chapter 5). The coNP lower bound in data complexity is from Schaerf (1993), for a language with existential restrictions that is much smaller than ALC. Its source is the kind of case analysis that the Oedipus example shows. The coNP upper bound is from Hustadt, Motik and Sattler (2005), who prove it for SHIQ, a logic that contains ALC. So ALC instance checking has no algorithm polynomial in the data unless P = NP.

## Reductions

- **To inconsistency.** $K \models C(a)$ if and only if $K$ with the extra assertion $\neg C(a)$ has no model.
- **From satisfiability.** $C$ is satisfiable with respect to $T$ if and only if $(T, \{C(a)\}) \not\models \bot(a)$.
- **From subsumption.** $C \sqsubseteq_T D$ if and only if $(T, \{C(a)\}) \models D(a)$ for a new name $a$. See [concept subsumption](/concept-subsumption/).

## Applications

- **Retrieval in ontologies.** Find all individuals of a class, including those that only follow from the rules.
- **Ontology-based data access.** A TBox in DL-Lite adds background knowledge to a database, and queries are answered over both.
- **Realization.** Tag each individual with its most specific classes, for search and for display in ontology tools.

## References
