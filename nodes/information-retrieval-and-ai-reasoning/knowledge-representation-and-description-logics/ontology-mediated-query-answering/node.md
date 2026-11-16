---
tag: 0999RP
kind: problem
slug: ontology-mediated-query-answering
name: Ontology-mediated query answering
aliases:
- ontology-based data access
- OBDA
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: research
summary: Answer a conjunctive query over data under an ontology, returning the tuples that are answers in every model.
prereqs: [tbox-and-abox, open-world-assumption, instance-checking]
see_also: [perfectref-rewriting, dl-lite, el-description-logic, chase-algorithm, datalog, chandra-merlin-theorem, query-containment-problem, ac0]
sources:
  - paper: doi:10.1007/s10817-007-9078-x
    title: Diego Calvanese, Giuseppe De Giacomo, Domenico Lembo, Maurizio Lenzerini and Riccardo Rosati, Tractable reasoning and efficient query answering in description logics, the DL-Lite family, Journal of Automated Reasoning 39(3), 2007
    locator: pages 385 to 429 (certain answers of conjunctive queries, FO-rewritability, the AC0 data complexity and the NP combined complexity for DL-Lite; general locator)
  - paper: "Franz Baader, Sebastian Brandt and Carsten Lutz, Pushing the EL envelope, Proceedings of the 19th International Joint Conference on Artificial Intelligence (IJCAI), 2005"
    locator: pages 364 to 369 (polynomial reasoning in EL with nominals, which covers instance checking over ABoxes)
  - paper: "Ullrich Hustadt, Boris Motik and Ulrike Sattler, Data complexity of reasoning in very expressive description logics, Proceedings of the 19th International Joint Conference on Artificial Intelligence (IJCAI), 2005"
    locator: the coNP data complexity of reasoning in SHIQ (general locator)
  - paper: "Carsten Lutz, The complexity of conjunctive query answering in expressive description logics, Proceedings of the 4th International Joint Conference on Automated Reasoning (IJCAR), LNAI 5195, Springer, 2008"
    locator: the 2EXPTIME combined complexity of conjunctive query answering in ALCI, and the EXPTIME upper bound for conjunctive queries over ALC (general locator)
  - paper: "Meghyn Bienvenu, Balder ten Cate, Carsten Lutz and Frank Wolter, Ontology-based data access: a study through disjunctive Datalog, CSP, and MMSNP, ACM Transactions on Database Systems 39(4), 2014"
    locator: ontology-mediated queries as pairs of an ontology and a query, and their relation to disjunctive Datalog and constraint satisfaction (general locator)
  - book: isbn:9780521695428
    title: Franz Baader, Ian Horrocks, Carsten Lutz and Ulrike Sattler, An Introduction to Description Logic, Cambridge University Press, 2017
    locator: the chapter on query answering (general locator)
---

Ontology-mediated query answering asks for the answers of a database query over data that is read through an ontology. The data is an ABox, a set of facts about individuals. The ontology is a TBox that adds background knowledge, for example that every professor teaches something. The query is usually a conjunctive query. Because of the [open world assumption](/open-world-assumption/), facts that are missing from the data are unknown, not false, so the answers are the *certain answers*: the tuples that are answers in every model of the TBox and the ABox. The cost depends on the ontology language. In [DL-Lite](/dl-lite/) the query can be rewritten into a first-order query over the data alone, so it runs in a database; in [EL](/el-description-logic/) answering stays polynomial in the data; in ALC it is already coNP-hard in the data.

## In plain words

You have a table of facts and a list of rules about what the words mean. Someone asks a question, such as "which people teach a course?". Some people are not listed as teaching anything, but the rules say that every professor teaches some course, so each professor must be in the answer. The answer should contain exactly the people for whom the facts and the rules together force a yes, no matter how the gaps in the facts are filled in. Finding these people is the task. With simple rules the question can be changed into a larger question that the plain table answers. With rich rules you may have to consider many ways to fill the gaps.

## Definition

An *ontology-mediated query* is a pair $Q = (\mathcal T, q)$ of a TBox $\mathcal T$ in a description logic $\mathcal L$ and a *conjunctive query* (CQ)

$$q(\vec x) = \exists \vec y.\, \alpha_1 \wedge \cdots \wedge \alpha_k,$$

where each atom $\alpha_i$ is $A(t)$ or $r(t, t')$ for a concept name $A$, a role name $r$ and terms among the answer variables $\vec x$ and the bound variables $\vec y$. A *union of conjunctive queries* (UCQ) is a finite disjunction of CQs with the same answer variables. An interpretation $I$ *satisfies* $q(\vec a)$ if some map $h$ from the variables to $\Delta^I$, with $h(\vec x) = \vec a^I$, sends each atom to a true fact of $I$. The bound variables may go to any element, also to elements that are not named in the data.

**Input.** A TBox $\mathcal T$, a CQ $q(\vec x)$, an ABox $\mathcal A$ (see [TBoxes and ABoxes](/tbox-and-abox/)), and a tuple $\vec a$ of individuals of $\mathcal A$ of the length of $\vec x$.

**Question.** Is $\vec a$ a *certain answer*, that is, does every model of $(\mathcal T, \mathcal A)$ satisfy $q(\vec a)$?

The set of certain answers is written $\mathrm{cert}(q, \mathcal T, \mathcal A)$. If $(\mathcal T, \mathcal A)$ has no model, every tuple is a certain answer, so algorithms first test consistency. A CQ with no answer variables is *Boolean*.

Complexity is measured in two ways. In *data complexity* the TBox and the query are fixed, and only $\mathcal A$ and $\vec a$ are the input. This is the measure that matters when the data is large and the ontology and query are small. In *combined complexity* all parts are the input.

## Variants

- **Instance queries.** The query is one atom $A(x)$. This is [instance checking](/instance-checking/), a classical reasoning task of description logics.
- **Unions of conjunctive queries.** The query is a UCQ. Rewriting algorithms produce UCQs even from a single CQ.
- **The ontology language.** The problem is studied for DL-Lite, EL and its Horn extensions, ALC and expressive logics such as SHIQ, and for rule languages such as existential rules.
- **Ontology-based data access.** The data stays in relational sources, and *mappings*, which are queries over the sources, define the ABox. A query is answered by rewriting it with the TBox and then unfolding it with the mappings into a query over the sources.
- **Rewritability questions.** Given $(\mathcal T, q)$, decide whether an equivalent first-order query or an equivalent Datalog program exists, and compute it.

## Examples

- *Anonymous elements.* Let $\mathcal T = \{\mathit{Professor} \sqsubseteq \exists \mathit{teaches}\}$ and $\mathcal A = \{\mathit{Professor}(\mathit{ann})\}$. For $q(x) = \exists y.\, \mathit{teaches}(x, y)$, $\mathit{ann}$ is a certain answer: every model has some $\mathit{teaches}$-successor of $\mathit{ann}$. For $q'(x, y) = \mathit{teaches}(x, y)$ there is no certain answer, because the successor need not be a named individual.
- *Rewriting.* Add $\exists \mathit{teaches}^- \sqsubseteq \mathit{Course}$ to $\mathcal T$, and let $\mathcal A = \{\mathit{Professor}(\mathit{ann}),\ \mathit{teaches}(\mathit{bob}, c_1)\}$. For $q(x) = \exists y.\, \mathit{teaches}(x, y) \wedge \mathit{Course}(y)$, the certain answers are $\mathit{ann}$ and $\mathit{bob}$, though the data has no $\mathit{Course}$ fact. [PerfectRef](/perfectref-rewriting/) finds them with a UCQ that includes $\exists y.\, \mathit{teaches}(x, y)$ and $\mathit{Professor}(x)$.
- *Reasoning by cases.* Let $\mathcal T = \{A \sqsubseteq B \sqcup C,\ B \sqsubseteq D,\ C \sqsubseteq D\}$ and $\mathcal A = \{A(a)\}$. Then $a$ is a certain answer of $D(x)$, but not of $B(x)$ nor of $C(x)$. No single model of $(\mathcal T, \mathcal A)$ gives exactly the certain answers to all queries, which is why disjunction makes the problem hard.

## Known algorithms

- **Query rewriting.** For DL-Lite, compute from $(\mathcal T, q)$ a UCQ $q_{\mathcal T}$ with $\mathrm{cert}(q, \mathcal T, \mathcal A) = q_{\mathcal T}(\mathcal A)$ for every consistent $\mathcal A$, and run it as SQL. [PerfectRef](/perfectref-rewriting/) does this for DL-Lite$_R$. The UCQ can be exponential in $q$. For $\mathcal T_n = \{B_i \sqsubseteq A_i : i \le n\}$ and $q = A_1(x) \wedge \cdots \wedge A_n(x)$, every UCQ rewriting needs all $2^n$ choices of $A_i$ or $B_i$.
- **Datalog rewriting.** For Horn logics such as EL, rewrite into a [Datalog](/datalog/) program and evaluate it with [semi-naive evaluation](/semi-naive-evaluation/). For instance queries in EL, the completion rules of [EL classification](/el-classification/), applied to the individuals of the ABox, are such a program.
- **Materialization and the chase.** For Horn logics the certain answers are the answers over one canonical model, built by the [chase](/chase-algorithm/) of the ABox with the TBox. The canonical model can be infinite, for example with $A \sqsubseteq \exists r.A$. The *combined approach* builds a finite part of it that may give some wrong answers, and removes them by a filter or by a rewriting of the query.
- **Expressive logics.** For ALC and beyond, algorithms reduce the problem to inconsistency tests of the knowledge base extended with the negation of the query, by tableaux, resolution or automata.

## Bounds

| ontology language | query | data complexity | combined complexity |
|---|---|---|---|
| none (plain database) | CQ | in AC0 | NP-complete |
| DL-Lite$_R$ | UCQ | in [AC0](/ac0/) | [NP-complete](/np-complete/) |
| EL | instance query | P-complete | P-complete |
| ALC | instance query | [coNP](/co-np/)-complete | EXPTIME-complete |
| ALC | CQ | coNP-hard | EXPTIME-complete (Lutz 2008) |
| ALCI | CQ | coNP-hard | 2EXPTIME-complete (Lutz 2008) |

The DL-Lite row is from Calvanese et al. (2007). The coNP upper bound for instance queries in ALC is a case of the result of Hustadt, Motik and Sattler (2005) for SHIQ. The EXPTIME lower bounds for ALC come from the [general TBox theorem](/alc-general-tbox-exptime/), and the textbook of Baader, Horrocks, Lutz and Sattler (2017) gives the matching upper bound for instance queries; Lutz (2008) gives the one for CQs. For the lower bound, $C$ is satisfiable with respect to $\mathcal T$ if and only if $(\mathcal T \cup \{A \sqsubseteq C\}, \{A(a)\})$ is consistent for a new name $A$, which holds if and only if $a$ is not a certain answer of $N(x)$ for a new name $N$. Two lower bounds have short proofs.

*EL is P-hard in data complexity.* Fix $\mathcal T_H = \{\exists \mathit{first}.\mathit{True} \sqcap \exists \mathit{second}.\mathit{True} \sqsubseteq \mathit{Fired},\ \exists \mathit{rule}.\mathit{Fired} \sqsubseteq \mathit{True}\}$. For a set of propositional Horn clauses with at most two body atoms, let the ABox have $\mathit{True}(p)$ for each fact $p$, and for each clause $c = (p \leftarrow s \wedge t)$ the facts $\mathit{rule}(p, c)$, $\mathit{first}(c, s)$ and $\mathit{second}(c, t)$, with $s = t$ for clauses with one body atom. If $p$ is derivable, then $\mathit{True}(p)$ follows, by induction on the derivation. In the other direction, the interpretation with the individuals as domain, the ABox edges, $\mathit{True}$ the derivable variables and $\mathit{Fired}$ the clauses whose body atoms are derivable is a model of $\mathcal T_H$ and the ABox. So $p$ is a certain answer of $\mathit{True}(x)$ if and only if $p$ is derivable. Derivability in Horn logic is P-complete ([Horn satisfiability](/horn-sat/)), and the ABox is built in logarithmic space. The upper bound holds because an ABox can be written with nominals, $\{a\} \sqsubseteq A$ and $\{a\} \sqsubseteq \exists r.\{b\}$, and subsumption in EL with nominals is polynomial (Baader, Brandt and Lutz 2005).

*ALC is coNP-hard in data complexity.* Fix $\mathcal T_3 = \{\top \sqsubseteq R \sqcup G \sqcup B,\ \exists s.D \sqsubseteq F\} \cup \{X \sqcap \exists e.X \sqsubseteq D : X \in \{R, G, B\}\}$ and the instance query $F(x)$. For a graph, let the ABox have $e(u, v)$ for each edge and $s(o, v)$ for each vertex $v$, with a new individual $o$. If the graph has a proper [3-coloring](/three-coloring/), the interpretation with the individuals as domain, each vertex in its color, $o$ in $R$, and $D$ and $F$ empty is a model, so $o$ is not a certain answer. If it has none, in any model choose one color among $R$, $G$ and $B$ for each vertex. Some edge $(u, v)$ gets the same color $X$ at both ends, so $u \in X \sqcap \exists e.X \subseteq D$, and then $o \in \exists s.D \subseteq F$. So $o$ is a certain answer of $F(x)$ if and only if the graph is not 3-colorable, which is coNP-complete.

## Reductions

- **To consistency.** For an instance query, $a \in \mathrm{cert}(A, \mathcal T, \mathcal A)$ if and only if $(\mathcal T, \mathcal A \cup \{\neg A(a)\})$ is inconsistent. In ALC the assertion $\neg A(a)$ is allowed; in logics without negation use a new name $\bar A$ with $A \sqcap \bar A \sqsubseteq \bot$.
- **From database query evaluation.** With the empty TBox the certain answers are the answers over $\mathcal A$ as a database, so CQ evaluation, which is NP-complete in combined complexity by the [Chandra-Merlin theorem](/chandra-merlin-theorem/), is a special case.
- **To query containment.** A rewriting $q_{\mathcal T}$ can be made smaller by deleting each CQ that is contained in another one, which is a [query containment](/query-containment-problem/) test.
- **To constraint satisfaction.** Bienvenu, ten Cate, Lutz and Wolter (2014) related ontology-mediated queries with ALC TBoxes and UCQs to disjunctive Datalog and to constraint satisfaction problems, which transfers dichotomy results to data complexity.

## Applications

- *Data access.* Users ask queries in the words of a domain ontology, and the system rewrites them into SQL over existing databases through mappings. DL-Lite was designed for this setting.
- *Data integration.* An ontology gives one view of several sources. Incomplete sources are read under the open world assumption, which is what certain answers express.
- *Large ontologies with data.* In medicine and life sciences, EL ontologies classify records, and Datalog engines answer instance queries over them.

## References
