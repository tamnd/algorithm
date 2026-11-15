---
tag: ZMNWQC
kind: concept
slug: open-world-assumption
name: Open-world assumption
aliases:
- OWA
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: core
summary: A statement not entailed by the knowledge base is unknown rather than false, as in first-order and description logics.
prereqs: [tbox-and-abox, closed-world-assumption]
see_also: [unique-name-assumption, instance-checking, negation-as-failure, datalog, nonmonotonic-reasoning, circumscription, ontology-mediated-query-answering, first-order-theorem-proving]
sources:
  - book: isbn:9780521695428
    title: Franz Baader, Ian Horrocks, Carsten Lutz and Ulrike Sattler, An Introduction to Description Logic, Cambridge University Press, 2017
    locator: Chapter 2 (knowledge bases, entailment and the open-world reading of ABoxes)
  - book: isbn:9780521876254
    title: Franz Baader, Diego Calvanese, Deborah L. McGuinness, Daniele Nardi and Peter F. Patel-Schneider (eds.), The Description Logic Handbook, second edition, Cambridge University Press, 2007
    locator: Chapter 2, Basic Description Logics, by Franz Baader and Werner Nutt (ABoxes compared with databases, open-world semantics)
  - paper: doi:10.1007/978-1-4684-3384-5_3
    title: "Raymond Reiter, On closed world data bases, in H. Gallaire and J. Minker (editors), Logic and Data Bases, Plenum Press, 1978"
    locator: pp. 55 to 76 (the open and the closed reading of a database, and the closed world assumption)
  - url: "https://www.w3.org/TR/owl2-primer/"
    title: W3C OWL Working Group, OWL 2 Web Ontology Language Primer (Second Edition), W3C Recommendation, 2012
    locator: the remarks on the open-world assumption and on the absence of unique names (general locator)
---

The open-world assumption (OWA) is the rule that a statement which does not follow from a knowledge base is unknown, not false. It is the opposite of the [closed-world assumption](/closed-world-assumption/) of databases and of planning, where every fact that is not stated or derived is taken to be false, so that a state is a plain set of true facts. Under the OWA, a knowledge base describes all the worlds that agree with it, and a query gets the answer yes only when it holds in all of them. First-order logic, description logics and OWL use the OWA.

## In plain words

A list of facts is often incomplete. If the list does not say that Peter has a sister, one reading says "Peter has no sister". That is the closed-world reading, and it is right for a train timetable, where a train that is not listed does not run. The open-world reading says "we do not know". It is right for knowledge that grows over time, such as facts about people collected from many places. Under the open-world reading, the answer to a question is "yes" only if the facts force it, "no" only if the facts rule it out, and "unknown" in all other cases. A new fact can then add answers but never takes an earlier answer back.

## The idea

A knowledge base $K = (T, A)$ has models $I = (\Delta^I, \cdot^I)$, as on the page [TBox and ABox](/tbox-and-abox/). Under the OWA, $K \models \alpha$ means that $\alpha$ holds in every model of $K$. For an assertion $C(a)$ there are three cases:

- $K \models C(a)$: the answer is yes.
- $K \models \neg C(a)$: the answer is no.
- neither: the answer is unknown, and some models of $K$ have $a^I \in C^I$ while others do not.

The models of $K$ can have more elements than the named individuals, more role edges than the ABox lists, and larger extensions of the concept names. So an ABox is a partial description, not a single structure. A database under the closed-world assumption is one finite structure, and a query is evaluated in it.

Three consequences follow.

- **Monotonicity.** If $K \subseteq K'$, every consequence of $K$ is a consequence of $K'$, since each model of $K'$ is a model of $K$. Reasoning under the closed-world assumption is not monotonic: a new fact can remove a conclusion. This is the domain of [nonmonotonic reasoning](/nonmonotonic-reasoning/), with [negation as failure](/negation-as-failure/) and [circumscription](/circumscription/).
- **Unnamed objects.** An axiom such as $\mathit{Person} \sqsubseteq \exists \mathit{hasMother}.\mathit{Person}$ does not ask the ABox to name a mother. Each model supplies one. In a database the same rule would be a constraint, and a person without a mother row would break it.
- **Case analysis.** A query can follow from $K$ while no single model shows why, as in the example of the page [instance checking](/instance-checking/). This is one source of the higher cost of reasoning under the OWA.

The OWA often comes with the absence of the [unique name assumption](/unique-name-assumption/): two names can denote the same element unless the knowledge base says otherwise.

## Examples

- A flight table lists flights from Vienna to London only. Under the closed-world assumption the question "is there a flight from Vienna to New York?" gets the answer no. If the same facts are an ABox, the answer is unknown, because some models add such a flight.
- The ABox $\{\mathit{Person}(\mathit{bob})\}$ with $T = \{\mathit{Person} \sqsubseteq \exists \mathit{hasMother}.\mathit{Person}\}$ entails $(\exists \mathit{hasMother}.\top)(\mathit{bob})$. No individual name is a mother of Bob, and the knowledge base is still consistent.
- The ABox $\{\mathit{hasChild}(\mathit{mary}, \mathit{peter}),\ \mathit{hasChild}(\mathit{mary}, \mathit{paul})\}$ does not entail that Mary has at most two children, since some models add more. Without the unique name assumption, it does not entail that she has at least two either, since Peter and Paul can be one person.
- Adding $\mathit{Female}(\mathit{peter})$ to an ABox can only add consequences. Under the closed-world assumption, the same step removes the conclusion that Peter is not female.

## Where it is used

- **Description logics and OWL.** All the standard reasoning tasks, such as [instance checking](/instance-checking/), are defined by entailment under the OWA.
- **Query answering over ontologies.** In [ontology-mediated query answering](/ontology-mediated-query-answering/), the answers to a query are the *certain answers*: the tuples that are answers in every model of the ontology and the data.
- **Theorem proving.** A [first-order prover](/first-order-theorem-proving/) proves what holds in all models, and a failed proof does not show the negation.
- **Where the closed reading wins.** Databases, [Datalog](/datalog/), logic programs with negation as failure and planning states read the data as complete. Systems that mix the two close some predicates and leave the rest open.

## References
