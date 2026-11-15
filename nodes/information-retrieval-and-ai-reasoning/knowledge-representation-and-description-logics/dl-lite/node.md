---
tag: ZAMQV9
kind: definition
slug: dl-lite
name: DL-Lite
aliases:
- DL-Lite family
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: advanced
summary: Description logics designed so that conjunctive queries over ontologies rewrite into first-order queries over the data.
prereqs: [description-logic, tbox-and-abox]
see_also: [perfectref-rewriting, ontology-mediated-query-answering, el-description-logic, sroiq, open-world-assumption, unique-name-assumption, ac0, instance-checking]
sources:
  - paper: doi:10.1007/s10817-007-9078-x
    title: Diego Calvanese, Giuseppe De Giacomo, Domenico Lembo, Maurizio Lenzerini and Riccardo Rosati, Tractable reasoning and efficient query answering in description logics, the DL-Lite family, Journal of Automated Reasoning 39(3), 2007
    locator: pages 385 to 429 (the syntax and semantics of DL-Lite_core, DL-Lite_F and DL-Lite_R, FO-rewritability of query answering and consistency, and the complexity results; general locator)
  - paper: "Alessandro Artale, Diego Calvanese, Roman Kontchakov and Michael Zakharyaschev, The DL-Lite family and relations, Journal of Artificial Intelligence Research 36, 2009"
    locator: the map of DL-Lite variants and the complexity of reasoning in each (general locator)
  - url: "https://www.w3.org/TR/owl2-profiles/"
    title: W3C OWL Working Group, OWL 2 Web Ontology Language Profiles (Second Edition), W3C Recommendation, 2012
    locator: the section on the OWL 2 QL profile
---

DL-Lite is a family of [description logics](/description-logic/) introduced by Calvanese, De Giacomo, Lembo, Lenzerini and Rosati. It is built so that a conjunctive query over a TBox and an ABox can be rewritten, using the TBox alone, into a union of conjunctive queries over the ABox. The rewritten query is first-order, so it can run as SQL in a relational database that stores the ABox, and answering it has the data complexity of [AC0](/ac0/). To get this property, DL-Lite gives up conjunction and qualified existential restriction on the left of inclusions. It keeps inverse roles, unqualified existential restriction, disjointness, and in some members role inclusions or functional roles. These are the features of conceptual models such as entity-relationship and UML class diagrams. The OWL 2 QL profile is based on DL-Lite$_R$.

## Definition

Let $A$ range over concept names and $P$ over role names. DL-Lite has

$$R \;::=\; P \mid P^-, \qquad B \;::=\; A \mid \exists R, \qquad C \;::=\; B \mid \neg B, \qquad E \;::=\; R \mid \neg R.$$

$R$ is a *basic role*, $B$ a *basic concept*, $C$ a *general concept* and $E$ a *general role*. In an interpretation $I$, $(P^-)^I = \{(e, d) : (d, e) \in P^I\}$, $(\exists R)^I = \{d : (d, e) \in R^I \text{ for some } e\}$, and $\neg$ is complement. So $\exists P$ is the domain of $P$ and $\exists P^-$ is its range. The main members differ in the TBox axioms that they allow.

- **DL-Lite$_{core}$**: concept inclusions $B \sqsubseteq C$. An inclusion $B_1 \sqsubseteq B_2$ is *positive*, and $B_1 \sqsubseteq \neg B_2$ is *negative*; it says that $B_1$ and $B_2$ are disjoint.
- **DL-Lite$_R$**: DL-Lite$_{core}$ with role inclusions $R \sqsubseteq E$.
- **DL-Lite$_F$**: DL-Lite$_{core}$ with functionality assertions $(\mathrm{funct}\ R)$, which say that $R^I$ is a partial function.

An ABox is a finite set of assertions $A(a)$ and $P(a, b)$ over individual names; see [TBoxes and ABoxes](/tbox-and-abox/). The semantics is the usual one with the [open world assumption](/open-world-assumption/). Calvanese and coauthors also adopt the [unique name assumption](/unique-name-assumption/), which matters for functionality.

The defining property is *FO-rewritability*. For every conjunctive query $q$ and every DL-Lite$_R$ or DL-Lite$_F$ TBox $\mathcal T$ there is a union of conjunctive queries $q_{\mathcal T}$, computed from $q$ and $\mathcal T$ alone, such that for every ABox $\mathcal A$ with $(\mathcal T, \mathcal A)$ consistent, the certain answers of $q$ over $(\mathcal T, \mathcal A)$ are the answers of $q_{\mathcal T}$ over $\mathcal A$ read as a finite database. Consistency of $(\mathcal T, \mathcal A)$ is also checked by a first-order query over $\mathcal A$. For DL-Lite$_R$ the rewriting is computed by [PerfectRef](/perfectref-rewriting/). As a result, query answering is in AC0 in data complexity, and knowledge base consistency and subsumption are in polynomial time (Calvanese et al. 2007).

Artale, Calvanese, Kontchakov and Zakharyaschev (2009) organized many more members, for example with Boolean combinations of basic concepts, and gave the complexity of each.

## Examples and non-examples

- A university TBox in DL-Lite$_R$: $\mathit{Professor} \sqsubseteq \exists \mathit{teaches}$ (every professor teaches something), $\exists \mathit{teaches}^- \sqsubseteq \mathit{Course}$ (whatever is taught is a course), $\mathit{Professor} \sqsubseteq \neg \mathit{Course}$ (no professor is a course), and $\mathit{lectures} \sqsubseteq \mathit{teaches}$.
- With the first two axioms and the ABox $\{\mathit{Professor}(\mathit{ann}),\ \mathit{teaches}(\mathit{bob}, c_1)\}$, the query $q(x) = \exists y.\, \mathit{teaches}(x, y) \wedge \mathit{Course}(y)$ has the certain answers $\mathit{ann}$ and $\mathit{bob}$. Neither appears in the data as the subject of a $\mathit{teaches}$ fact with a $\mathit{Course}$ object. The rewriting of $q$ contains the queries $\exists y.\, \mathit{teaches}(x, y)$, which finds $\mathit{bob}$, and $\mathit{Professor}(x)$, which finds $\mathit{ann}$.
- The ABox $\{\mathit{Professor}(\mathit{ann}),\ \mathit{Course}(\mathit{ann})\}$ is inconsistent with $\mathit{Professor} \sqsubseteq \neg \mathit{Course}$. The first-order check is the query $\exists x.\, \mathit{Professor}(x) \wedge \mathit{Course}(x)$, extended by the positive inclusions.
- $(\mathrm{funct}\ \mathit{hasBirthMother})$ is a DL-Lite$_F$ assertion. With the unique name assumption, the ABox $\{\mathit{hasBirthMother}(a, b),\ \mathit{hasBirthMother}(a, c)\}$ is inconsistent with it.
- *Non-example:* $\mathit{Student} \sqcap \mathit{Employee} \sqsubseteq \mathit{WorkingStudent}$ is not a DL-Lite axiom, because conjunction is not allowed on the left.
- *Non-example:* $\exists r.A \sqsubseteq A$ uses a qualified existential restriction on the left. It breaks FO-rewritability. Over this TBox, an individual is a certain answer of $q(x) = A(x)$ if and only if the ABox has an $r$-path from it to an individual with an $A$ fact. A union of conjunctive queries, and even any first-order query, cannot express this kind of reachability in a directed graph.

## Related definitions

- [Ontology-mediated query answering](/ontology-mediated-query-answering/) is the reasoning task that DL-Lite is built for, and [PerfectRef](/perfectref-rewriting/) is its rewriting algorithm.
- [EL](/el-description-logic/) is the other main tractable family. It allows qualified existential restrictions and conjunction everywhere, but query answering in it is not FO-rewritable in general.
- [SROIQ](/sroiq/) and OWL 2 DL contain DL-Lite$_R$ as a fragment, up to syntax.
- [Instance checking](/instance-checking/) is the special case of query answering with an atomic query and one answer variable.

## References
