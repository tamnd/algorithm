---
tag: 2DQNP0
kind: concept
slug: unique-name-assumption
name: Unique name assumption
aliases:
- UNA
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: core
summary: Different individual names denote different objects, an assumption made by databases and some logics but not by OWL.
prereqs: [tbox-and-abox, open-world-assumption]
see_also: [closed-world-assumption, instance-checking, bisimulation, datalog, sroiq, herbrand-universe]
sources:
  - paper: "Raymond Reiter, Equality and domain closure in first-order databases, Journal of the ACM 27(2), 1980"
    locator: the unique name axioms and the domain closure axiom for databases (general locator)
  - book: isbn:9780521695428
    title: Franz Baader, Ian Horrocks, Carsten Lutz and Ulrike Sattler, An Introduction to Description Logic, Cambridge University Press, 2017
    locator: Chapter 2 (the semantics of individual names, with and without the unique name assumption)
  - book: isbn:9780521876254
    title: Franz Baader, Diego Calvanese, Deborah L. McGuinness, Daniele Nardi and Peter F. Patel-Schneider (eds.), The Description Logic Handbook, second edition, Cambridge University Press, 2007
    locator: Chapter 2, Basic Description Logics, by Franz Baader and Werner Nutt (individual names in ABoxes and the unique name assumption)
  - url: "https://www.w3.org/TR/owl2-primer/"
    title: W3C OWL Working Group, OWL 2 Web Ontology Language Primer (Second Edition), W3C Recommendation, 2012
    locator: the section on equality and inequality of individuals, owl:sameAs and owl:differentFrom (general locator)
---

The unique name assumption (UNA) is the rule that two different individual names denote two different objects: $a^I \neq b^I$ for all names $a \neq b$ in every interpretation $I$. Databases make it, and so do many description logic texts. OWL does not: two names can denote one object unless the ontology says that they are different.

## In plain words

If a list of facts names "Peter" and "Paul", are they two people? Under the unique name assumption, yes, always. Without it, they might be one person with two names, as when two sources give the same person different names. Then the reasoner treats them as different only if some fact says so, and treats them as the same only if the facts force it.

## The idea

Without the UNA, the map $\cdot^I$ on individual names can be any function into $\Delta^I$. With it, the map must be one to one. Reiter (1980) wrote the UNA as axioms $a \neq b$, one for each pair of different constants, and used them with a domain closure axiom to make a database a theory of first-order logic with equality.

OWL leaves the UNA out and gives the modeller two assertions: owl:sameAs states $a^I = b^I$, and owl:differentFrom (or owl:AllDifferent for a list) states $a^I \neq b^I$. Data from many sources often uses several names for one thing, and this choice fits that case.

Whether the UNA changes the answers depends on the logic. In ALC it does not change consistency or [instance checking](/instance-checking/). Take a model in which $a$ and $b$ share an element, add a new copy of that element for $b$ with the same concept names and the same edges in and out, and point $b$ there. The copy is [bisimilar](/bisimulation/) to the original, so it is in the same ALC concepts, and the result is still a model. With number restrictions or nominals the UNA matters, since these constructors can count elements or name them.

## Examples

- The ABox $\{\mathit{hasChild}(\mathit{mary}, \mathit{peter}),\ \mathit{hasChild}(\mathit{mary}, \mathit{paul}),\ ({\leq} 1\, \mathit{hasChild})(\mathit{mary})\}$ is consistent without the UNA: Peter and Paul are one child. With the UNA it is inconsistent.
- Without the UNA, the same ABox entails that Peter and Paul are the same individual, which OWL writes as owl:sameAs.
- The ABox $\{A(a),\ \neg A(b)\}$ forces $a^I \neq b^I$ in every model, with or without the UNA.
- In ALC, the ABox $\{r(a, b),\ (\forall r.\neg A)(a),\ A(b)\}$ is inconsistent with and without the UNA, and $\{r(a, b),\ A(b)\}$ entails $(\exists r.A)(a)$ in both readings.

## Where it is used

- **Databases and Datalog.** Each constant is a different value, and the [closed-world assumption](/closed-world-assumption/) goes with it. In [Datalog](/datalog/) the UNA and the closed domain are built into the semantics, through the [Herbrand universe](/herbrand-universe/).
- **OWL ontologies.** The UNA is not made, which matters for OWL 2 DL, based on [SROIQ](/sroiq/), since it has number restrictions and nominals.
- **Description logic texts.** Some texts make the UNA and others do not, so a result about logics with counting can depend on which reading is in use.

## References
