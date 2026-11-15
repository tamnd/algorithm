---
tag: XC4JTK
kind: concept
slug: description-logic
name: Description logic
aliases:
- terminological logic
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: intro
summary: A family of decidable fragments of first-order logic that describe concepts, roles and individuals, used for ontologies.
prereqs: []
see_also: [alc-description-logic, tbox-and-abox, concept-subsumption, el-description-logic, dl-lite, sroiq, semantic-network, ontology-knowledge-representation]
sources:
  - book: isbn:9780521695428
    title: Franz Baader, Ian Horrocks, Carsten Lutz and Ulrike Sattler, An Introduction to Description Logic, Cambridge University Press, 2017
    locator: Chapter 1 (introduction and history) and Chapter 2 (the basic description logic ALC, knowledge bases and reasoning tasks)
  - book: isbn:9780521876254
    title: Franz Baader, Diego Calvanese, Deborah L. McGuinness, Daniele Nardi and Peter F. Patel-Schneider (eds.), The Description Logic Handbook, second edition, Cambridge University Press, 2007
    locator: Chapter 1, An Introduction to Description Logics, by Daniele Nardi and Ronald J. Brachman, and Chapter 2, Basic Description Logics, by Franz Baader and Werner Nutt
  - paper: "Ronald J. Brachman and James G. Schmolze, An overview of the KL-ONE knowledge representation system, Cognitive Science 9(2), 1985"
    locator: the KL-ONE system, its concepts, roles and classifier (general locator)
  - paper: "Manfred Schmidt-Schauß and Gert Smolka, Attributive concept descriptions with complements, Artificial Intelligence 48(1), 1991, pages 1 to 26"
    locator: the definition of ALC and the decidability of its satisfiability and subsumption
  - url: "https://www.w3.org/TR/owl2-overview/"
    title: W3C OWL Working Group, OWL 2 Web Ontology Language Document Overview (Second Edition), W3C Recommendation, 2012
    locator: the overview of OWL 2 and its profiles (general locator)
---

A description logic (DL) is a logic for writing down the terms of a domain and the facts about them. It has *concepts* (sets of objects), *roles* (binary relations) and *individuals* (named objects), and a small set of constructors that build complex concepts from simple ones. Most description logics are decidable fragments of first-order logic, and the members of the family trade expressive power against the cost of reasoning. The Web Ontology Language OWL 2 is based on the description logic SROIQ.

## In plain words

A description logic is a precise language for a vocabulary. You name kinds of things, such as person or woman, and links between things, such as has child. Then you combine them: "a woman who has at least one child that is a person" describes a mother. You write general rules, such as "every mother is a parent", and facts about named things, such as "Mary has the child Peter". A program called a reasoner then finds what follows. It can tell you that one kind is always inside another, that a description can never be true of anything, or that Mary must be a mother. The language is kept small on purpose, so that the reasoner always finishes with a correct answer.

## The idea

### Syntax

Fix a set of concept names $A, B, \ldots$, a set of role names $r, s, \ldots$ and a set of individual names $a, b, \ldots$. The basic logic [ALC](/alc-description-logic/) builds concepts from the names with $\top$, $\bot$, $\neg C$, $C \sqcap D$, $C \sqcup D$, $\exists r.C$ and $\forall r.C$. Other members of the family add or remove constructors. The letters in the name of a logic list its features.

| letter | feature | example |
|---|---|---|
| ALC | the logic above | $\neg A \sqcap \forall r.B$ |
| S | ALC with transitive roles | $r$ is transitive |
| H | role inclusions | $r \sqsubseteq s$ |
| I | inverse roles | $\exists r^-.A$ |
| O | nominals, concepts with one named element | $\{a\}$ |
| N | unqualified number restrictions | $\geq 2\, r$ |
| Q | qualified number restrictions | $\geq 2\, r.A$ |
| F | functional roles | $\leq 1\, r$ |
| R | complex role inclusions and role axioms | $r \circ s \sqsubseteq r$ |

So SHIQ is ALC with transitive roles, role inclusions, inverse roles and qualified number restrictions. Lighter logics drop constructors: [EL](/el-description-logic/) keeps only $\top$, $\sqcap$ and $\exists r.C$, and [DL-Lite](/dl-lite/) allows only simple inclusions with unqualified $\exists r$ on the left.

### Semantics

An interpretation $I = (\Delta^I, \cdot^I)$ has a nonempty domain $\Delta^I$ and maps each concept name $A$ to a set $A^I \subseteq \Delta^I$, each role name $r$ to a relation $r^I \subseteq \Delta^I \times \Delta^I$, and each individual name $a$ to an element $a^I \in \Delta^I$. Each constructor has a fixed meaning as a set. For example, $(C \sqcap D)^I = C^I \cap D^I$, and $(\exists r.C)^I$ is the set of elements with an $r$-successor in $C^I$. The ALC page gives all the rules. An interpretation of a logic with role names only is a [Kripke structure](/kripke-structure/) with one accessibility relation for each role.

### Knowledge bases and reasoning

A knowledge base $K = (T, A)$ has a [TBox and an ABox](/tbox-and-abox/). The TBox $T$ is a finite set of general concept inclusions $C \sqsubseteq D$. The ABox $A$ is a finite set of assertions $C(a)$ and $r(a, b)$. An interpretation is a model of $K$ when it satisfies each axiom: $C^I \subseteq D^I$, $a^I \in C^I$ and $(a^I, b^I) \in r^I$. A statement follows from $K$ when it holds in every model of $K$. So a DL makes the [open-world assumption](/open-world-assumption/): what is not stated is unknown, not false. In OWL, and in most DL texts, the [unique name assumption](/unique-name-assumption/) does not hold, and two names can denote the same element.

The main reasoning tasks are [concept satisfiability](/concept-satisfiability/), [concept subsumption](/concept-subsumption/), knowledge base consistency, [instance checking](/instance-checking/) and [ontology classification](/ontology-classification/). Satisfiability, subsumption and instance checking reduce to knowledge base consistency, and in logics with full negation, such as ALC, subsumption and satisfiability reduce to each other.

### Relation to first-order logic

Each concept $C$ translates to a formula $\pi_x(C)$ with one free variable $x$: $\pi_x(A) = A(x)$, $\pi_x(C \sqcap D) = \pi_x(C) \land \pi_x(D)$, $\pi_x(\exists r.C) = \exists y\, (r(x, y) \land \pi_y(C))$ and $\pi_x(\forall r.C) = \forall y\, (r(x, y) \to \pi_y(C))$, where $\pi_y$ swaps the roles of $x$ and $y$. An inclusion $C \sqsubseteq D$ becomes $\forall x\, (\pi_x(C) \to \pi_x(D))$. The translation uses only two variables, and each quantifier is guarded by a role atom. The two-variable fragment and the guarded fragment of first-order logic are both decidable, while full first-order logic is not.

## Examples

Take the concept names Person, Female, Woman, Mother, Parent and the role hasChild.

- The TBox $\{\mathit{Woman} \equiv \mathit{Person} \sqcap \mathit{Female},\ \mathit{Mother} \equiv \mathit{Woman} \sqcap \exists \mathit{hasChild}.\mathit{Person},\ \mathit{Parent} \equiv \mathit{Person} \sqcap \exists \mathit{hasChild}.\mathit{Person}\}$ defines three names. Each $\equiv$ stands for two inclusions.
- From this TBox, $\mathit{Mother} \sqsubseteq \mathit{Parent}$ follows, so a classifier puts Mother below Parent.
- The ABox $\{\mathit{Woman}(\mathit{mary}),\ \mathit{hasChild}(\mathit{mary}, \mathit{peter}),\ \mathit{Person}(\mathit{peter})\}$ with this TBox entails $\mathit{Mother}(\mathit{mary})$.
- The concept $\exists \mathit{hasChild}.\mathit{Female} \sqcap \forall \mathit{hasChild}.\neg \mathit{Female}$ is unsatisfiable: no element can have a female child while all its children are not female.
- The ABox does not entail $\neg \mathit{Parent}(\mathit{peter})$, because some models give Peter a child. Under the open-world assumption the absence of a fact proves nothing.

## Where it is used

- **Ontology languages.** OWL 2 DL is based on SROIQ with datatypes (see [SROIQ](/sroiq/)). The profiles OWL 2 EL and OWL 2 QL are based on EL and DL-Lite. See [ontology](/ontology-knowledge-representation/).
- **Large biomedical terminologies.** SNOMED CT and many ontologies of the life sciences are written in EL or close variants, and reasoners classify them in polynomial time with [EL classification](/el-classification/).
- **Access to data.** In [ontology-mediated query answering](/ontology-mediated-query-answering/), a TBox in a logic such as DL-Lite adds background knowledge to a database, and queries are rewritten so that the database answers them.
- **Origins.** Description logics grew out of [semantic networks](/semantic-network/) and [frames](/frame-knowledge-representation/), whose meaning was informal. The system KL-ONE (Brachman and Schmolze 1985) had concepts, roles and a classifier that placed each concept in a hierarchy, and the logics that followed gave these a model-theoretic semantics.

## References
