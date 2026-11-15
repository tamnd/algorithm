---
tag: W9NV76
kind: algorithm
slug: alc-tableau-algorithm
name: Tableau algorithm for ALC
aliases:
- Schmidt-Schauss-Smolka tableau
- DL tableau
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: core
summary: Tries to build a model of a concept in negation normal form by expansion rules for and, or, some and all, and reports a clash if none exists.
solves: [concept-satisfiability]
model: word-ram
complexity:
  vars: {n: the size of the concept and the TBox}
  time: {worst: 2^O(n^2), general_tbox: 2^2^O(n)}
  space: {extra: O(n^3), general_tbox: 2^O(n)}
properties: {deterministic: true, exact: true, recursive: true, builds_model: true}
history:
  year: 1991
  people: [Manfred Schmidt-Schauß, Gert Smolka]
  note: Schmidt-Schauß and Smolka defined ALC and gave a calculus of constraint systems that decides satisfiability and subsumption. They showed that a depth-first form of it runs in polynomial space. The name tableau came later, when ALC was seen to be a notational variant of the modal logic K.
prereqs: [alc-description-logic, tbox-and-abox, concept-satisfiability, chronological-backtracking]
see_also: [tableau-blocking, concept-subsumption, alc-pspace-completeness, alc-general-tbox-exptime, alc-modal-k-correspondence, hypertableau, el-classification, dpll]
sources:
  - paper: doi:10.1016/0004-3702(91)90078-X
    title: Manfred Schmidt-Schauß and Gert Smolka, Attributive concept descriptions with complements, Artificial Intelligence 48(1), 1991
    locator: pages 1 to 26 (the completion rules for constraint systems, and the polynomial space bound of the depth-first search)
  - book: isbn:9780521695428
    title: Franz Baader, Ian Horrocks, Carsten Lutz and Ulrike Sattler, An Introduction to Description Logic, Cambridge University Press, 2017
    locator: Chapter 4, Section 4.2 (the tableau algorithm for ALC, for ABoxes, acyclic TBoxes and general TBoxes with blocking)
  - book: isbn:9780521876254
    title: Franz Baader, Diego Calvanese, Deborah L. McGuinness, Daniele Nardi and Peter F. Patel-Schneider (eds.), The Description Logic Handbook, second edition, Cambridge University Press, 2007
    locator: Chapter 2, Basic Description Logics, by Franz Baader and Werner Nutt, Section 2.3 (tableau algorithms)
  - paper: "Klaus Schild, A correspondence theory for terminological logics: preliminary report, Proceedings of the 12th International Joint Conference on Artificial Intelligence (IJCAI), 1991"
    locator: ALC as a notational variant of the multimodal logic K (general locator)
  - paper: doi:10.1613/jair.21
    title: Martin Buchheit, Francesco M. Donini and Andrea Schaerf, Decidable reasoning in terminological knowledge representation systems, Journal of Artificial Intelligence Research 1, 1993
    locator: pages 109 to 138 (a calculus for general inclusions and the test that stops it, general locator)
  - paper: "Francesco M. Donini and Fabio Massacci, EXPTIME tableaux for ALC, Artificial Intelligence 124(1), 2000, pages 87 to 138"
    locator: tableau calculi for ALC with general TBoxes that run in exponential time
  - paper: doi:10.1007/s10817-011-9243-0
    title: Rajeev Goré and Linh Anh Nguyen, ExpTime tableaux for ALC using sound global caching, Journal of Automated Reasoning 50(4), 2013
    locator: pages 355 to 381 (global caching of node labels, and the exponential time bound)
  - paper: "Ian Horrocks and Peter F. Patel-Schneider, Optimizing description logic subsumption, Journal of Logic and Computation 9(3), 1999"
    locator: lazy unfolding, absorption, semantic branching, backjumping and caching (general locator)
---

The tableau algorithm for ALC decides whether an [ALC](/alc-description-logic/) concept is satisfiable with respect to a TBox by trying to build a tree-shaped model of it. It works on concepts in negation normal form, has one rule for each constructor, and backtracks over the choices of the ⊔-rule. Without a TBox it runs in polynomial space, and with a general TBox it needs [blocking](/tableau-blocking/) to stop. Most reasoners for expressive description logics use a form of it.

## In plain words

You want to know if a description can be true of anything. The method tries to build an example. It starts with one object and writes down what the description says about it. For "this or that", it tries "this" first, and comes back to try "that" if the first try fails. If the object must have a link to some object of a kind, the method makes a new object at the end of a new link. If all linked objects must have a property, each new object gets it. A list with a fact and its opposite is a failure. If one try ends with no failure, it is an example, and the answer is yes. If all tries fail, the answer is no. Background rules can ask for an endless chain of objects. Then the method stops at an object that repeats an earlier one.

## The problem

The input is an ALC concept $C$ and a TBox $T$, a finite set of general concept inclusions $D \sqsubseteq E$. The TBox can be empty. The question is whether some interpretation $I = (\Delta^I, \cdot^I)$ is a model of $T$ and has $C^I \neq \emptyset$. This is [concept satisfiability](/concept-satisfiability/). [Concept subsumption](/concept-subsumption/) reduces to it: $C \sqsubseteq_T D$ holds if and only if $C \sqcap \neg D$ is not satisfiable with respect to $T$.

A concept is in negation normal form (NNF) when $\neg$ occurs only in front of concept names. Each concept has an equivalent one in NNF of linear size: push $\neg$ inward with the De Morgan laws, $\neg \exists r.C \equiv \forall r.\neg C$ and $\neg \forall r.C \equiv \exists r.\neg C$. For example, $\neg(A \sqcap \exists r.(B \sqcup \neg \forall s.C))$ becomes $\neg A \sqcup \forall r.(\neg B \sqcap \forall s.C)$.

## The algorithm

Each node of the tree has a *label*, a set of concepts in NNF. The search is depth first. It first completes the label of a node with the ⊓-rule and the ⊔-rule, then makes one child for each $\exists r.D$ in the label (the ∃-rule), and gives the child each $E$ with $\forall r.E$ in the label (the ∀-rule). A label has a *clash* when it holds $\bot$, or $A$ and $\neg A$ for a concept name $A$. Each inclusion $D \sqsubseteq E$ of $T$ becomes the concept $\mathrm{nnf}(\neg D \sqcup E)$, which goes into every label.

```pseudo id=main
SAT(C, T)
L1  C_T ← {nnf(¬D ⊔ E) : D ⊑ E in T}
L2  return NODE({nnf(C)} ∪ C_T, [])

NODE(S, P)                                   ▷ P is the list of the completed labels of the ancestors
L3  for each L in COMPLETIONS(S) do
L4      ok ← true
L5      for each ∃r.D in L do
L6          S′ ← {D} ∪ {E : ∀r.E in L} ∪ C_T
L7          if T is not empty and S′ ⊆ L″ for some L″ in P + [L] then continue    ▷ blocked
L8          if NODE(S′, P + [L]) is false then ok ← false, and leave this loop
L9      if ok then return true
L10 return false

COMPLETIONS(S)                               ▷ yields the clash-free completions of S, one at a time
L11 L ← the closure of S under the ⊓-rule: with D ⊓ E, add D and E
L12 if ⊥ is in L, or A and ¬A are in L for some A, then return
L13 if some D ⊔ E in L has D not in L and E not in L then
L14     yield each label of COMPLETIONS(L ∪ {D}), then each label of COMPLETIONS(L ∪ {E})
L15 else yield L
```

The ⊔-rule is the only choice point. COMPLETIONS returns the completions lazily, so NODE tries the next one only when a child of the current one fails. A node is blocked at line L7 when an ancestor, or the node itself, already holds every concept that the child would get. Then the child is not built, and the edge goes to that ancestor. Without a TBox, line L7 never blocks. The labels of the ancestors are final when line L7 tests them, because each label is complete before its children are made.

When SAT returns true, the successful calls give a model. The elements are the nodes, $A^I$ is the set of nodes whose label holds $A$, and $r^I$ is the set of $r$-edges, with each blocked edge sent to its blocking node.

## Example

Take the concept $(A \sqcup \exists r.B) \sqcap \neg A \sqcap \forall r.(\neg B \sqcup C)$ with the empty TBox. It is already in NNF.

| step | node | label and action |
|---|---|---|
| 1 | root | ⊓-rule: $\{A \sqcup \exists r.B,\ \neg A,\ \forall r.(\neg B \sqcup C)\}$ |
| 2 | root | ⊔-rule, first choice $A$: clash with $\neg A$, backtrack |
| 3 | root | second choice $\exists r.B$: the label is complete |
| 4 | child | ∃-rule and ∀-rule: $\{B,\ \neg B \sqcup C\}$ |
| 5 | child | first choice $\neg B$: clash with $B$, backtrack |
| 6 | child | second choice $C$: complete, no ∃, return true |

The run expands 2 nodes and meets 2 clashes. The model has $\Delta^I = \{0, 1\}$, $r^I = \{(0, 1)\}$, $B^I = C^I = \{1\}$ and $A^I = \emptyset$, and the root 0 is an instance of the input concept.

With the TBox $T = \{A \sqsubseteq \exists r.A\}$ and the concept $A$, the root gets $\{A,\ \neg A \sqcup \exists r.A\}$. The choice $\neg A$ clashes, so the root label becomes $\{A,\ \neg A \sqcup \exists r.A,\ \exists r.A\}$. The child would get $\{A,\ \neg A \sqcup \exists r.A\}$, which is a subset of the root label, so line L7 blocks it. The model has one element in $A^I$ with an $r$-edge to itself. Without line L7 the search would make an endless chain of $r$-successors.

## Correctness

The algorithm is sound: when it returns true, the interpretation above is a model of $T$ and the root is in $C^I$. The proof is an induction on the concepts of each label, and it uses that each label is clash-free and complete for the ⊓-rule and the ⊔-rule. A blocked edge is safe because the blocking label holds all that the child would need. It is complete: if $x \in C^J$ in some model $J$ of $T$, then the choices that $x$ satisfies lead to a run that returns true, and each $\exists r.D$ is matched by an $r$-successor of $x$ in $J$. It terminates: without a TBox the role depth drops at each level, and with blocking the initial labels on one path are different subsets of a set of size $O(n)$. The full proof is below.

## Complexity

Let $n$ be the size of the input, and $m = O(n)$ the number of its subconcepts. A label has at most $m$ concepts, and one label has at most $2^m$ completions.

- **Empty TBox.** The tree has depth at most the role depth of $C$. The search keeps only the current path, so the space is $O(n^3)$ words. The time is $2^{O(n^2)}$ in the worst case. [Concept satisfiability](/concept-satisfiability/) in ALC without a TBox is PSPACE-complete ([ALC is PSPACE-complete](/alc-pspace-completeness/)), and this search meets that upper bound.
- **General TBox.** A path can have $2^m$ nodes before blocking stops it, so the time is $2^{2^{O(n)}}$ in the worst case and the space is $2^{O(n)}$. The problem is EXPTIME-complete ([ALC with general TBoxes is EXPTIME-complete](/alc-general-tbox-exptime/)), so this form of the algorithm is not worst-case optimal. It is a double exponential bound for a deterministic search.

## Properties

- **Builds a model.** A run that returns true gives a finite model with at most one element for each expanded node. So ALC with a general TBox has the finite model property.
- **Tree models.** Without blocking the model is a tree. With blocking it is a tree with some edges back to ancestors.
- **One kind of choice.** Only the ⊔-rule branches, and the search must undo it on failure. The order of the other rules does not change the answer.
- **One branch at a time.** The search works on one path of the tree at a time, which is why the empty TBox case fits in polynomial space.
- **Modal logic view.** ALC is a notational variant of the modal logic K with many modalities (see [ALC and modal logic K](/alc-modal-k-correspondence/)), and the model is a [Kripke structure](/kripke-structure/). The algorithm is then a tableau for K.

## Variants and improvements

- **ABox consistency.** Start with one node for each individual of the ABox, with its assertions, and the role assertions as edges. The rules are the same. Blocking applies only to the new nodes.
- **Acyclic TBoxes.** Replace a defined name by its definition only when it appears in a label (lazy unfolding). This keeps the polynomial space bound, while a full unfolding first can make the concept exponentially larger.
- **Exponential time.** Cache the result for each label that was seen, or let all nodes with the same label share one node. With such global caching the time is $2^{O(n)}$, which is worst-case optimal (Donini and Massacci 2000, Goré and Nguyen 2013).
- **Optimizations in reasoners.** Absorption moves inclusions $A \sqsubseteq E$ with a concept name on the left into lazy unfolding, so the large disjunctions of line L1 do not come up at each node. Semantic branching adds $\neg D$ in the second branch of a choice. Backjumping goes back to the last choice that caused the clash, as in [conflict-directed backjumping](/conflict-directed-backjumping/).
- **More expressive logics.** Number restrictions, inverse roles, role hierarchies and nominals each add rules and change the blocking condition. This leads to the tableaux for SHIQ and [SROIQ](/sroiq/). The [hypertableau](/hypertableau/) calculus makes less nondeterminism from the TBox.

## When to use it

Use it for an expressive description logic with disjunction and full negation, where you need satisfiability, subsumption or consistency, and where a model is a useful output. For the EL family, [EL classification](/el-classification/) runs in polynomial time and is much faster. For logics without disjunction and negation, [structural subsumption](/structural-subsumption/) can be enough.

## Pitfalls

- **Forgetting NNF.** The ⊔-rule and the clash test are correct only on concepts in NNF. Convert the concept and each TBox concept first.
- **No blocking with a TBox.** With a cyclic or general TBox, the search without blocking does not stop on an input such as $T = \{A \sqsubseteq \exists r.A\}$.
- **Subset blocking in larger logics.** With inverse roles, a child can change the label of its parent, and subset blocking is not sound. Such logics need equality, dynamic or pairwise blocking (see [blocking](/tableau-blocking/)).
- **Keeping the whole tree.** A program that keeps every node to return a model, as the code here does, can use exponential memory even with an empty TBox. Keep only the current path when you only need the answer.

## Implementations

## History

Schmidt-Schauß and Smolka (1991) defined ALC and gave the first decision procedure for its satisfiability and subsumption, as rules that complete a set of constraints. They proved that a depth-first form of it uses polynomial space, and that the problem is PSPACE-complete. Schild (1991) saw that ALC is a notational variant of the modal logic K, so their procedure is a tableau in the sense of modal logic, and the name stayed. Buchheit, Donini and Schaerf (1993) gave a terminating calculus for general inclusions. In the late 1990s Horrocks and others built fast reasoners on tableaux with many optimizations.

## References
