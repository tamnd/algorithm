---
tag: E0JZHD
kind: definition
slug: tbox-and-abox
name: TBox and ABox
aliases:
- terminological box
- assertional box
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: core
summary: A knowledge base splits into a TBox of concept inclusion axioms and an ABox of assertions about named individuals.
prereqs: [description-logic, alc-description-logic]
see_also: [concept-subsumption, instance-checking, ontology-classification, open-world-assumption, unique-name-assumption, closed-world-assumption, datalog, ontology-mediated-query-answering]
sources:
  - book: isbn:9780521695428
    title: Franz Baader, Ian Horrocks, Carsten Lutz and Ulrike Sattler, An Introduction to Description Logic, Cambridge University Press, 2017
    locator: Chapter 2 (TBoxes, acyclic TBoxes and their unfolding, ABoxes and knowledge bases)
  - book: isbn:9780521876254
    title: Franz Baader, Diego Calvanese, Deborah L. McGuinness, Daniele Nardi and Peter F. Patel-Schneider (eds.), The Description Logic Handbook, second edition, Cambridge University Press, 2007
    locator: Chapter 2, Basic Description Logics, by Franz Baader and Werner Nutt, Section 2.2 (terminologies, world descriptions, the family TBox)
  - paper: "Bernhard Nebel, Terminological reasoning is inherently intractable, Artificial Intelligence 43, 1990"
    locator: the exponential size of unfolded terminologies and the hardness of subsumption with respect to acyclic TBoxes (general locator)
---

A description logic knowledge base $K = (T, A)$ has two parts. The TBox $T$ (terminological box) holds the general knowledge: inclusions between concepts, such as "every mother is a parent". The ABox $A$ (assertional box) holds facts about named individuals, such as "Mary is a woman" and "Peter is a child of Mary". Both parts are sets of axioms with a model-theoretic meaning, and both are read under the [open-world assumption](/open-world-assumption/).

## Definition

The syntax of concepts and interpretations is that of [ALC](/alc-description-logic/) or of another [description logic](/description-logic/).

**TBox.** A general concept inclusion (GCI) is an axiom $C \sqsubseteq D$ for concepts $C$ and $D$. A TBox $T$ is a finite set of GCIs. An interpretation $I$ satisfies $C \sqsubseteq D$ when $C^I \subseteq D^I$, and it is a model of $T$ when it satisfies each GCI of $T$. The axiom $C \equiv D$ stands for the two GCIs $C \sqsubseteq D$ and $D \sqsubseteq C$.

These kinds of TBox matter for the cost of reasoning:

- **Empty.** $T = \emptyset$. Every interpretation is a model.
- **Acyclic.** Every axiom is a definition $A \equiv C$ or a primitive definition $A \sqsubseteq C$ with a concept name $A$ on the left. Each name is on the left of at most one axiom. The graph with an edge from $A$ to each name in its right side has no cycle. A name on the left of a definition is *defined*, and the other names are *primitive*.
- **General.** Any finite set of GCIs. It can have complex concepts on the left, and cycles.

An acyclic TBox can be *unfolded*. First write each primitive definition $A \sqsubseteq C$ as $A \equiv C \sqcap A'$ with a new name $A'$. Then replace each defined name by its definition until only primitive names are left. A subsumption $C \sqsubseteq D$ follows from $T$ if and only if the unfolding of $C$ is subsumed by the unfolding of $D$ with the empty TBox. The unfolding can be exponentially larger than $C$ and $T$ together (Nebel 1990).

**ABox.** A concept assertion is an axiom $C(a)$, and a role assertion is an axiom $r(a, b)$, for individual names $a$ and $b$, a concept $C$ and a role name $r$. An ABox $A$ is a finite set of assertions. An interpretation $I$ satisfies $C(a)$ when $a^I \in C^I$, and $r(a, b)$ when $(a^I, b^I) \in r^I$. It is a model of $A$ when it satisfies each assertion.

**Knowledge base.** A knowledge base is a pair $K = (T, A)$. An interpretation is a model of $K$ when it is a model of $T$ and of $A$. $K$ is *consistent* when it has a model. An axiom $\alpha$ *follows from* $K$, written $K \models \alpha$, when every model of $K$ satisfies $\alpha$. Unless a text says otherwise, two individual names can denote the same element: the [unique name assumption](/unique-name-assumption/) is not made, as in OWL.

## Examples and non-examples

- An acyclic TBox: $\mathit{Woman} \equiv \mathit{Person} \sqcap \mathit{Female}$ and $\mathit{Mother} \equiv \mathit{Woman} \sqcap \exists \mathit{hasChild}.\mathit{Person}$. The names Woman and Mother are defined, and Person and Female are primitive. Unfolding Mother gives $\mathit{Person} \sqcap \mathit{Female} \sqcap \exists \mathit{hasChild}.\mathit{Person}$.
- A general TBox: $\{\exists \mathit{hasChild}.\mathit{Person} \sqsubseteq \mathit{Parent}\}$ has a complex left side. $\{\mathit{Human} \sqsubseteq \exists \mathit{hasParent}.\mathit{Human}\}$ is cyclic: in each model, a human has an endless chain of human ancestors, which either is infinite or runs in a cycle.
- Exponential unfolding: the acyclic TBox $A_i \equiv \forall r.A_{i+1} \sqcap \forall s.A_{i+1}$ for $i = 0, \ldots, n - 1$ has size linear in $n$. Unfolding $A_0$ gives one copy of $A_n$ for each of the $2^n$ words over $r$ and $s$ of length $n$, a concept of size $6 \cdot 2^n - 5$ (7, 19, 43, 91 and 187 for $n = 1$ to $5$).
- An ABox: $\{\mathit{Woman}(\mathit{mary}),\ \mathit{hasChild}(\mathit{mary}, \mathit{peter}),\ \mathit{Person}(\mathit{peter})\}$. With the acyclic TBox above, $K \models \mathit{Mother}(\mathit{mary})$.
- The ABox $\{A(a),\ \neg A(b)\}$ is consistent, and it forces $a^I \neq b^I$. The ABox $\{A(a),\ \neg A(a)\}$ is inconsistent.

These are not TBoxes or ABoxes of ALC, or not of the kind named:

- $\{\mathit{Mother} \equiv \mathit{Woman} \sqcap \exists \mathit{hasChild}.\mathit{Mother}\}$ is not acyclic: Mother uses itself.
- $\{A \equiv B,\ A \equiv C\}$ is not acyclic: the name $A$ is on the left of two definitions.
- $\exists x\, \mathit{hasChild}(\mathit{mary}, x)$ is not an assertion, since an ABox has no variables. Write $(\exists \mathit{hasChild}.\top)(\mathit{mary})$.
- $r \sqsubseteq s$ is a role inclusion. Logics with H put it in a separate RBox.
- A database table is not an ABox: under the [closed-world assumption](/closed-world-assumption/) a missing row is false, while in an ABox a missing assertion is unknown.

## Related definitions

- The tasks on a knowledge base: [concept subsumption](/concept-subsumption/) with respect to $T$, [instance checking](/instance-checking/) on $K$, and [ontology classification](/ontology-classification/) of $T$.
- The open-world reading and the absence of unique names: [open-world assumption](/open-world-assumption/) and [unique name assumption](/unique-name-assumption/).
- A TBox used to answer queries over data: [ontology-mediated query answering](/ontology-mediated-query-answering/).

## References
