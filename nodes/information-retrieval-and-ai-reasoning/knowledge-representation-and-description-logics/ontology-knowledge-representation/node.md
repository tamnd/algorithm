---
tag: TB4RNF
kind: concept
slug: ontology-knowledge-representation
name: Ontology (knowledge representation)
aliases:
- formal ontology
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: intro
summary: A formal and explicit specification of the concepts of a domain, their relations and the axioms that constrain them, shared by the people and programs that use it.
prereqs: [description-logic, semantic-network]
see_also: [tbox-and-abox, ontology-classification, concept-subsumption, ontology-mediated-query-answering, open-world-assumption, el-description-logic, dl-lite, frame-knowledge-representation]
sources:
  - paper: doi:10.1006/knac.1993.1008
    title: Thomas R. Gruber, A translation approach to portable ontology specifications, Knowledge Acquisition 5(2), 1993, pages 199 to 220
    locator: the definition of an ontology as an explicit specification of a conceptualization (general locator)
  - paper: doi:10.1016/S0169-023X(97)00056-6
    title: Rudi Studer, V. Richard Benjamins and Dieter Fensel, Knowledge engineering, principles and methods, Data and Knowledge Engineering 25(1-2), 1998, pages 161 to 197
    locator: Section 6.1, the definition of an ontology as a formal, explicit specification of a shared conceptualisation
  - paper: doi:10.1007/978-3-540-92673-3_0
    title: Nicola Guarino, Daniel Oberle and Steffen Staab, What is an ontology?, in Steffen Staab and Rudi Studer (eds.), Handbook on Ontologies, second edition, Springer, 2009, pages 1 to 17
    locator: the analysis of the definitions of Gruber and of Studer and colleagues, and the meaning of conceptualization, explicit, formal and shared (general locator)
---

In knowledge representation, an ontology is a shared vocabulary for a domain, the classes, relations and individuals that people and programs use to talk about it, together with axioms that fix what the terms mean. Gruber (1993) called it an explicit specification of a conceptualization, and Studer, Benjamins and Fensel (1998) added that the specification is formal and the conceptualization is shared. Today most ontologies are written in a [description logic](/description-logic/), so that a reasoner can check them and derive facts that are not stated. The description logic pages give the languages and the reasoning tasks; this page is about the ontology as an artifact: what it contains, why it is written down, and how it is used.

## In plain words

When two programs exchange data about patients, they must agree on what "patient", "diagnosis" and "treated by" mean. An ontology writes this agreement down. It lists the kinds of things in the domain, the ways they can be related, and rules such as "every surgeon is a doctor" or "a person has exactly one birth date". The rules are written in a precise logical language, not in prose. Then a program can check that the rules do not contradict each other, find the class in which a new term belongs, and answer questions with facts that follow from the rules even if nobody typed them in. The same ontology can serve many databases and programs, which is the point of writing it.

## The idea

Guarino, Oberle and Staab (2009) take the definition apart word by word:

- A **conceptualization** is the set of distinctions that a community makes about a domain: which kinds of things exist and which relations hold between them. It exists in people's heads and in their practice.
- **Explicit** means that the terms and their constraints are written down.
- **Formal** means that they are written in a language with a precise meaning, so that a machine can process them.
- **Shared** means that a group agrees on them, not one person or one program.

An ontology is a set of axioms over a vocabulary. The vocabulary has class names, such as *Person* and *Course*, property names, such as *teaches*, and individual names. The axioms come in a few kinds:

- **taxonomy:** subclass axioms, such as $\mathit{Professor} \sqsubseteq \mathit{Person}$;
- **definitions:** necessary and sufficient conditions, such as $\mathit{Teacher} \equiv \mathit{Person} \sqcap \exists \mathit{teaches}.\mathit{Course}$;
- **constraints:** disjointness, such as $\mathit{Person} \sqcap \mathit{Course} \sqsubseteq \bot$, domains and ranges of properties, and number restrictions;
- **facts:** assertions about individuals, such as $\mathit{teaches}(\mathit{ann}, \mathit{logic101})$.

In a description logic the first three kinds form the TBox and the facts form the ABox; the [TBox and ABox](/tbox-and-abox/) page gives the split. Many authors call only the TBox the ontology and treat the ABox as data that the ontology describes.

The meaning is the set of all models of the axioms. An ontology does not list everything that is true; it states constraints, and anything that holds in all models follows. This is the [open-world assumption](/open-world-assumption/): a fact that is not stated is unknown, not false. It is the main difference from a database schema, in which a missing fact is false.

An ontology differs from a [semantic network](/semantic-network/) or a [frame system](/frame-knowledge-representation/) in that its axioms have a fixed model-theoretic meaning, so two tools that read the same ontology must draw the same conclusions.

## Examples

**Classification.** Take the axioms

- $\mathit{Student} \sqsubseteq \mathit{Person}$,
- $\mathit{Teacher} \equiv \mathit{Person} \sqcap \exists \mathit{teaches}.\mathit{Course}$,
- $\mathit{TeachingAssistant} \equiv \mathit{Student} \sqcap \exists \mathit{teaches}.\mathit{Course}$.

Nobody wrote that a teaching assistant is a teacher, but it follows: a teaching assistant is a student, so a person, and teaches a course, so it meets the definition of *Teacher*. A reasoner that performs [ontology classification](/ontology-classification/) adds $\mathit{TeachingAssistant} \sqsubseteq \mathit{Teacher}$ to the hierarchy.

**Error detection.** Add the axioms $\mathit{Person} \sqcap \mathit{Course} \sqsubseteq \bot$ and $\mathit{Seminar} \sqsubseteq \mathit{Course} \sqcap \mathit{Person}$, the second written by mistake. Then *Seminar* has no instances in any model, so it is unsatisfiable, and a [concept satisfiability](/concept-satisfiability/) check reports it.

**Query answering with incomplete data.** With the ABox $\mathit{Student}(\mathit{bob})$ and $\mathit{teaches}(\mathit{bob}, c)$, $\mathit{Course}(c)$, the query "list all teachers" returns *bob*, although no table lists him as a teacher. This is [ontology-mediated query answering](/ontology-mediated-query-answering/).

## Where it is used

- **Data integration.** Several databases are mapped to one ontology, and queries are written against the ontology. Logics such as [DL-Lite](/dl-lite/) are designed so that such queries can be rewritten into database queries.
- **Large terminologies.** Fields such as medicine and biology keep large vocabularies of terms with subclass and part-of relations. Logics such as [EL](/el-description-logic/), in which classification takes polynomial time, are used for them.
- **Exchange between programs.** Programs that commit to one ontology can exchange data and agree on the meaning of each field, which is the use that Gruber (1993) had in mind.
- **Checking a model of a domain.** Writing a domain as axioms and running a reasoner finds unsatisfiable classes and unwanted subclass relations, as in the examples above.

## References
