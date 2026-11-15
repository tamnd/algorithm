---
tag: V950Q8
kind: problem
slug: ontology-classification
name: Ontology classification
aliases:
- TBox classification
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: core
summary: Compute the subsumption hierarchy among all concept names of an ontology.
prereqs: [concept-subsumption, concept-satisfiability, tbox-and-abox]
see_also: [el-classification, alc-tableau-algorithm, hypertableau, alc-general-tbox-exptime, ontology-knowledge-representation, instance-checking, transitive-reduction]
sources:
  - paper: "Franz Baader, Bernhard Hollunder, Bernhard Nebel, Hans-Jürgen Profitlich and Enrico Franconi, An empirical analysis of optimization techniques for terminological representation systems, or: making KRIS get a move on, Applied Intelligence 4(2), 1994, pages 109 to 132"
    locator: the brute force, the simple traversal and the enhanced traversal methods to build the hierarchy (top search and bottom search)
  - paper: doi:10.1016/j.websem.2011.12.007
    title: Birte Glimm, Ian Horrocks, Boris Motik, Rob Shearer and Giorgos Stoilos, A novel approach to ontology classification, Journal of Web Semantics 14, 2012
    locator: pages 84 to 101 (known and possible subsumptions from models, and the count of subsumption tests)
  - book: isbn:9780521876254
    title: Franz Baader, Diego Calvanese, Deborah L. McGuinness, Daniele Nardi and Peter F. Patel-Schneider (eds.), The Description Logic Handbook, second edition, Cambridge University Press, 2007
    locator: Chapter 9, Implementation and Optimization Techniques, by Ian Horrocks (classification and the optimizations of the hierarchy computation)
  - book: isbn:9780521695428
    title: Franz Baader, Ian Horrocks, Carsten Lutz and Ulrike Sattler, An Introduction to Description Logic, Cambridge University Press, 2017
    locator: Chapter 2 (classification as a reasoning task) and Chapter 6 (classification of EL TBoxes in polynomial time)
---

Ontology classification is the problem of computing all subsumptions $A \sqsubseteq_T B$ between the concept names $A$ and $B$ of a TBox $T$, usually given as the hierarchy of direct subsumptions. It is the first thing an ontology tool does after loading an ontology, and it shows both the class tree and the names that cannot have instances. With a subsumption test as a black box it needs up to $n(n - 1)$ tests for $n$ names, so the methods differ in how many tests they avoid.

## In plain words

An ontology names many kinds of things and gives rules about them. You want to see the kinds as a tree, with each kind below the kinds that include it, such as "mother" below "woman" and below "parent". The rules often say this only in an indirect way, so a program must work it out. The simple method asks about every pair of kinds. Better methods put the kinds into the tree one at a time, and ask only about the places where a kind can go. They also skip questions whose answer follows from earlier answers.

## Definition

The logic is ALC (or another description logic), with interpretations $I = (\Delta^I, \cdot^I)$ and a TBox $T$ of GCIs (see [TBox and ABox](/tbox-and-abox/)). Let $N_T$ be the set of concept names in $T$, with $n = |N_T|$.

- **Input.** A TBox $T$.
- **Output.** The relation $\{(A, B) \in N_T \times N_T : A \sqsubseteq_T B\}$, together with the names that are unsatisfiable with respect to $T$ (those with $A \sqsubseteq_T \bot$).

The relation is a preorder: reflexive and transitive. Names with $A \equiv_T B$ form one class, and the classes form a partial order. The *taxonomy* is its Hasse diagram, the [transitive reduction](/transitive-reduction/): $B$ is a *direct subsumer* of $A$ when $A \sqsubseteq_T B$, $A \not\equiv_T B$, and no name $C$ lies strictly between them. Unsatisfiable names sit below every other name, and are usually listed apart. As a decision problem, the question is whether a given pair $(A, B)$ is in the relation, which is [concept subsumption](/concept-subsumption/) for names. The input has no ABox, so the complexity is combined complexity.

## Variants

- **With an ABox.** Classify the TBox, then find for each individual its most specific names (realization).
- **Incremental classification.** Update the hierarchy after a small change of the TBox, without starting again.
- **Classification of complex concepts.** Insert a concept $C$ that is not a name into a known hierarchy, to find its direct subsumers and subsumees.

## Examples

Take the family TBox from the Description Logic Handbook (Chapter 2), without its number restriction:

- $\mathit{Woman} \equiv \mathit{Person} \sqcap \mathit{Female}$, $\mathit{Man} \equiv \mathit{Person} \sqcap \neg \mathit{Woman}$
- $\mathit{Mother} \equiv \mathit{Woman} \sqcap \exists \mathit{hasChild}.\mathit{Person}$, $\mathit{Father} \equiv \mathit{Man} \sqcap \exists \mathit{hasChild}.\mathit{Person}$
- $\mathit{Parent} \equiv \mathit{Father} \sqcup \mathit{Mother}$, $\mathit{Grandmother} \equiv \mathit{Mother} \sqcap \exists \mathit{hasChild}.\mathit{Parent}$
- $\mathit{MotherWithoutDaughter} \equiv \mathit{Mother} \sqcap \forall \mathit{hasChild}.\neg \mathit{Woman}$, $\mathit{Wife} \equiv \mathit{Woman} \sqcap \exists \mathit{hasHusband}.\mathit{Man}$

The TBox has 10 names, so the brute force makes $10 \cdot 9 = 90$ subsumption tests. Of these, 24 succeed, and no name is unsatisfiable. The taxonomy has 11 direct edges:

| name | direct subsumers |
|---|---|
| Person, Female | none (top level) |
| Woman | Person, Female |
| Man | Person |
| Parent | Person |
| Mother | Woman, Parent |
| Father | Man, Parent |
| Grandmother | Mother |
| MotherWithoutDaughter | Mother |
| Wife | Woman |

The subsumption $\mathit{Mother} \sqsubseteq_T \mathit{Parent}$ comes from the disjunction in the definition of Parent, and $\mathit{Grandmother} \sqsubseteq_T \mathit{Parent}$ then follows by transitivity, so a smart method does not test it.

## Known algorithms

- **Brute force.** Test every ordered pair of names with a subsumption procedure, such as the [tableau algorithm for ALC](/alc-tableau-algorithm/). This makes $n(n - 1)$ tests.
- **Enhanced traversal.** Insert the names one at a time into the taxonomy built so far. A *top search* goes down from $\top$ and keeps only the nodes that subsume the new name, to find its direct subsumers. A *bottom search* goes up from $\bot$ to find its direct subsumees. Subsumptions that are told in the TBox, and the transitivity of the order, prune the search (Baader and others 1994).
- **Known and possible subsumers.** Build a model for each name once. A name $B$ that is false for an instance of $A$ in this model is not a subsumer of $A$, and needs no test. Only the pairs that are still possible get a test (Glimm and others 2012).
- **Saturation for EL.** [EL classification](/el-classification/) derives all subsumptions between names in one run, in polynomial time.

When no name subsumes another, every method that uses only subsumption tests makes all $n(n - 1)$ tests. A failed test $A \not\sqsubseteq_T B$ rules out only the pairs $(D, C)$ with $A \sqsubseteq_T D$ and $C \sqsubseteq_T B$, and here the only such pair is $(A, B)$ itself.

## Bounds

| logic and TBox | complexity | reason |
|---|---|---|
| ALC, acyclic TBox | PSPACE-complete | $n(n - 1)$ tests in polynomial space, and one subsumption reduces to it |
| ALC, general TBox | EXPTIME-complete | $n(n - 1)$ tests in exponential time, and one subsumption reduces to it |
| EL, general TBox | in P | polynomial saturation |

The bounds for one test are on the page [concept subsumption](/concept-subsumption/), and the EXPTIME lower bound is on [ALC with general TBoxes is EXPTIME-complete](/alc-general-tbox-exptime/).

## Reductions

- **To subsumption.** Classification makes at most $n(n - 1)$ calls to subsumption, and $n$ calls to satisfiability for the unsatisfiable names.
- **From subsumption.** To decide $C \sqsubseteq_T D$, classify $T \cup \{A \equiv C,\ B \equiv D\}$ for new names $A$ and $B$, and look at the pair $(A, B)$.

## Applications

- **Ontology editors.** Tools show the inferred hierarchy next to the one the modeller wrote, and list the unsatisfiable names as errors.
- **Large terminologies.** Medical terminologies such as SNOMED CT are classified with EL reasoners, and the hierarchy is the product that users see.
- **Faster reasoning.** Later tasks, such as realization and query answering, use the stored hierarchy instead of new subsumption tests.

## References
