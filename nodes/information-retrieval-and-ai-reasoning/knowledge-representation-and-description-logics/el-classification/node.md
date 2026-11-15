---
tag: JW3S50
kind: algorithm
slug: el-classification
name: EL classification by completion rules
aliases:
- CEL algorithm
- Baader-Brandt-Lutz algorithm
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: advanced
summary: Puts an EL TBox in a normal form, then fills the set of subsumers of every concept name with five completion rules. It classifies the whole TBox in polynomial time.
solves: [ontology-classification, concept-subsumption]
model: word-ram
complexity:
  vars: {n: the size of the TBox}
  time: {worst: O(n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: true, exact: true, saturation: true, builds_model: true}
history:
  year: 2005
  people: [Franz Baader, Sebastian Brandt, Carsten Lutz]
  note: Brandt showed in 2004 that EL stays polynomial with general TBoxes. Baader, Brandt and Lutz gave the completion rules in normal form, extended them with bottom, nominals, concrete domains and role inclusions, and showed that most other extensions make subsumption EXPTIME-complete.
prereqs: [el-description-logic, tbox-and-abox, concept-subsumption, ontology-classification]
see_also: [alc-tableau-algorithm, structural-subsumption, horn-sat-forward-chaining, datalog-evaluation, semi-naive-evaluation, dl-lite, sroiq]
sources:
  - paper: "Franz Baader, Sebastian Brandt and Carsten Lutz, Pushing the EL envelope, Proceedings of the 19th International Joint Conference on Artificial Intelligence (IJCAI), 2005"
    locator: pages 364 to 369 (normal form, completion rules, polynomial time, and the EXPTIME-complete extensions)
  - paper: "Sebastian Brandt, Polynomial time reasoning in a description logic with existential restrictions, GCI axioms, and what else?, Proceedings of the 16th European Conference on Artificial Intelligence (ECAI), IOS Press, 2004"
    locator: pages 298 to 302 (EL with general TBoxes and role hierarchies stays polynomial)
  - book: isbn:9780521695428
    title: Franz Baader, Ian Horrocks, Carsten Lutz and Ulrike Sattler, An Introduction to Description Logic, Cambridge University Press, 2017
    locator: Chapter 6 (reasoning in the EL family, general locator)
  - paper: doi:10.1007/s10817-013-9296-3
    title: Yevgeny Kazakov, Markus Krötzsch and František Simančík, The incredible ELK, from polynomial procedures to efficient reasoning with EL ontologies, Journal of Automated Reasoning 53(1), 2014
    locator: pages 1 to 61 (goal-directed rules, the saturation loop and concurrent classification)
---

EL classification by completion rules computes all subsumptions between the concept names of a TBox in the [description logic EL](/el-description-logic/). It first rewrites the TBox into a normal form with four kinds of axioms. Then it fills, for each concept name $X$, a set $S(X)$ of names known to subsume $X$, and for each role a set of known links, with five rules until nothing changes. The whole run takes polynomial time, and it gives every subsumption at once, which is what [ontology classification](/ontology-classification/) needs.

## In plain words

Think of a large list of medical terms with rules such as "every inflammation is a disease". You want the full table of which term falls under which. The method keeps, for each term, a list of the terms known to be above it. At the start each list holds only the term itself. Then the rules add terms to lists. If a list holds a term with a rule "this is always that", the list gets "that". If the rule says "this always has a link to something of a kind", the method draws a link to that kind. Facts about the far end of a link can then add terms at the near end. Nothing is ever taken back, so the lists only grow, and they stop growing after a number of steps that is small compared with the size of the list of rules.

## The problem

The input is a TBox $T$, a finite set of general concept inclusions $C \sqsubseteq D$ between EL concepts. EL concepts are built from concept names $A$, $\top$, conjunction $C \sqcap D$ and existential restriction $\exists r.C$; the code and the proof also allow $\bot$. The TBox may be cyclic. The output is, for all concept names $A$ and $B$ of $T$, whether $A \sqsubseteq_T B$, that is, whether $A^I \subseteq B^I$ in every model $I$ of $T$. A name with $A \sqsubseteq_T \bot$ is unsatisfiable. A subsumption $C \sqsubseteq_T D$ between complex concepts reduces to the same question for two fresh names $Q \sqsubseteq C$ and $D \sqsubseteq P$.

[Concept subsumption](/concept-subsumption/) in EL with a general TBox is decidable in polynomial time. In [ALC](/alc-description-logic/) the same question is EXPTIME-complete ([ALC with general TBoxes](/alc-general-tbox-exptime/)), because ALC has disjunction and value restrictions.

## The algorithm

**Normal form.** Each inclusion is split, with fresh concept names, into axioms of four forms, where $A, A_1, A_2$ are names or $\top$ and $B$ is a name, $\top$ or $\bot$:

$$A \sqsubseteq B, \qquad A_1 \sqcap A_2 \sqsubseteq B, \qquad A \sqsubseteq \exists r.B, \qquad \exists r.A \sqsubseteq B.$$

For example, $\mathit{Disease} \sqcap \exists \mathit{loc}.\exists \mathit{part}.\mathit{Heart} \sqsubseteq \mathit{HeartDisease}$ becomes $\exists \mathit{part}.\mathit{Heart} \sqsubseteq X$, $\exists \mathit{loc}.X \sqsubseteq Y$ and $\mathit{Disease} \sqcap Y \sqsubseteq \mathit{HeartDisease}$. The new TBox has linear size and the same subsumptions between the old names.

**Completion.** The rules work on the sets $S(X)$ and on a relation $R(r)$ for each role $r$. The invariant is that $B \in S(X)$ implies $X \sqsubseteq_T B$, and $(X, Y) \in R(r)$ implies $X \sqsubseteq_T \exists r.Y$.

```pseudo id=main
CLASSIFY(T)                     ▷ T in normal form; ADD(X, B): if B ∉ S(X), add B to S(X) and queue (X, B)
L1  for each name X and X = ⊤: S(X) ← ∅, then ADD(X, X), ADD(X, ⊤); R(r) ← ∅ for each role r
L2  while the queue is not empty do
L3      take (X, A) from the queue                                    ▷ A is new in S(X)
L4      for each A ⊑ B in T: ADD(X, B)                                  ▷ CR1
L5      for each A ⊓ A′ ⊑ B in T (either order) with A′ in S(X): ADD(X, B)   ▷ CR2
L6      for each A ⊑ ∃r.B in T: ADD-EDGE(r, X, B)                       ▷ CR3
L7      for each (W, X) in R(r): for each ∃r.A ⊑ B in T, ADD(W, B); if A = ⊥, ADD(W, ⊥)   ▷ CR4, CR5

ADD-EDGE(r, X, Y)
L8  if (X, Y) is not in R(r) then add it to R(r)
L9      for each A in S(Y) and each ∃r.A ⊑ B in T: ADD(X, B)            ▷ CR4
L10     if ⊥ is in S(Y) then ADD(X, ⊥)                                  ▷ CR5

SUBSUMES(A, B)
L11 return B ∈ S(A) or ⊥ ∈ S(A)
```

The queue holds the pairs that still have to be matched against the axioms. A new element of $S(X)$ fires the axioms that have it on the left (lines L4 to L6), and the existential axioms of the nodes that point to $X$ (line L7). A new edge looks at what is already known about its target (lines L9 and L10). This is the same forward chaining as [Horn-SAT by forward chaining](/horn-sat-forward-chaining/), with the edges as an extra kind of fact.

When the run ends with $\bot \notin S(\top)$, the sets give a model of $T$: one element $d_X$ for each name $X$ with $\bot \notin S(X)$, the name $A$ holds at $d_X$ when $A \in S(X)$, and the $r$-edges are those of $R(r)$. The element $d_A$ is in exactly the names of $S(A)$, so it is a counter-example to every subsumption that line L11 rejects.

## Example

The TBox has four inclusions:

- $\mathit{Pericarditis} \sqsubseteq \mathit{Inflammation} \sqcap \exists \mathit{loc}.\mathit{Pericardium}$
- $\mathit{Inflammation} \sqsubseteq \mathit{Disease}$
- $\mathit{Pericardium} \sqsubseteq \exists \mathit{part}.\mathit{Heart}$
- $\mathit{Disease} \sqcap \exists \mathit{loc}.\exists \mathit{part}.\mathit{Heart} \sqsubseteq \mathit{HeartDisease}$

The normal form has 7 axioms: the first inclusion splits into $\mathit{Pericarditis} \sqsubseteq \mathit{Inflammation}$ and $\mathit{Pericarditis} \sqsubseteq \exists \mathit{loc}.\mathit{Pericardium}$, and the last one into the three axioms with $X$ and $Y$ shown above. The facts that lead to the answer for $\mathit{Pericarditis}$, in an order in which they can be derived, are:

| fact | line | rule | new fact |
|---|---|---|---|
| 1 | L1 | start | $S(\mathit{Pericarditis}) = \{\mathit{Pericarditis}, \top\}$ |
| 2 | L4 | CR1 | $\mathit{Inflammation} \in S(\mathit{Pericarditis})$ |
| 3 | L6, L8 | CR3 | $(\mathit{Pericarditis}, \mathit{Pericardium}) \in R(\mathit{loc})$ |
| 4 | L4 | CR1 | $\mathit{Disease} \in S(\mathit{Pericarditis})$ |
| 5 | L6, L8 | CR3 | $(\mathit{Pericardium}, \mathit{Heart}) \in R(\mathit{part})$ |
| 6 | L9 | CR4 | $\mathit{Heart} \in S(\mathit{Heart})$ and $\exists \mathit{part}.\mathit{Heart} \sqsubseteq X$, so $X \in S(\mathit{Pericardium})$ |
| 7 | L7 | CR4 | $X \in S(\mathit{Pericardium})$, the $\mathit{loc}$-edge, and $\exists \mathit{loc}.X \sqsubseteq Y$, so $Y \in S(\mathit{Pericarditis})$ |
| 8 | L5 | CR2 | $\mathit{Disease}, Y \in S(\mathit{Pericarditis})$, so $\mathit{HeartDisease} \in S(\mathit{Pericarditis})$ |

At the end $S(\mathit{Pericarditis}) = \{\mathit{Pericarditis}, \mathit{Inflammation}, \mathit{Disease}, Y, \mathit{HeartDisease}, \top\}$, so $\mathit{Pericarditis} \sqsubseteq_T \mathit{HeartDisease}$. $S(\mathit{Inflammation}) = \{\mathit{Inflammation}, \mathit{Disease}, \top\}$, so an inflammation in general is not a heart disease. Over the 9 names, with $\top$, $X$ and $Y$, the run adds 25 facts in total.

## Correctness

Each rule adds a fact that follows from earlier facts and one axiom, so the invariant above holds and every "yes" is right. When the queue is empty, the sets are closed under all five rules. Then the interpretation built from $S$ and $R$ is a model of the normalized TBox, and the element $d_A$ lies in $B$ only if $B \in S(A)$, so every "no" is right too. Normalization keeps the subsumptions between the old names, because each model of the old TBox becomes a model of the new one when each fresh name gets the extension of the subconcept it stands for. The full proof is in proofs/correctness.md.

## Complexity

Let $n$ be the size of $T$. The normal form has $O(n)$ axioms and $k = O(n)$ names. Each set $S(X)$ has at most $k + 1$ elements and each relation $R(r)$ at most $k^2$ pairs, but edges into $X$ come only from axioms $A \sqsubseteq \exists r.X$, so there are $O(n^2)$ edges in all. With the axioms indexed by their left side, line L7 costs $O(n^2)$ for each name $X$ over its whole life, times $|S(X)|$, and line L9 costs $|S(Y)|$ for each edge. The time is $O(n^3)$ and the space is $O(n^2)$.

The problem is also hard for polynomial time: propositional Horn clauses $p_1 \wedge p_2 \to q$ are the axioms $P_1 \sqcap P_2 \sqsubseteq Q$, so [Horn-SAT](/horn-sat/) reduces to EL subsumption, and subsumption in EL with general TBoxes is P-complete.

## Properties

- **One pass, all answers.** The run gives the whole subsumption hierarchy at once, not one test at a time.
- **No search.** There is no choice and no backtracking. The result does not depend on the order of the queue.
- **Monotone.** Facts are only added. A new axiom can be handled by adding it and running the loop again from the current sets.
- **A small model.** The model built from $S$ and $R$ has at most one element for each name of the normal form.

## Variants and improvements

- **Larger EL logics.** Baader, Brandt and Lutz (2005) added rules for nominals, concrete domains with a convexity condition, and role inclusions $r_1 \circ \dots \circ r_k \sqsubseteq s$, and kept the polynomial bound. This extension underlies the OWL 2 EL profile.
- **Goal-directed rules.** The ELK reasoner (Kazakov, Krötzsch and Simančík 2014) computes $S(X)$ only for names that are needed, with rules on the original concepts instead of a full normal form, and runs the saturation of different names in parallel.
- **Datalog.** The rules are a fixed Datalog program over the normalized axioms, so [Datalog evaluation](/datalog-evaluation/) with [semi-naive evaluation](/semi-naive-evaluation/) also classifies EL.
- **Query answering.** The same idea with ABox individuals as extra nodes decides instance checking in polynomial time; [ontology-mediated query answering](/ontology-mediated-query-answering/) for EL builds on it.

## When to use it

Use it for ontologies that stay inside EL with $\bot$, such as many large medical and biological ontologies, where a [tableau](/alc-tableau-algorithm/) reasoner is too slow because it tests the pairs one at a time. Do not use it as a general reasoner: with value restrictions, disjunction, negation or number restrictions, subsumption is EXPTIME-complete or worse, and the rules are not complete for those constructors. For [DL-Lite](/dl-lite/) ontologies over large data, query rewriting fits better.

## Pitfalls

- **Skipping the normal form.** Line L6 matches only an axiom $A \sqsubseteq \exists r.B$ with a name $B$. An axiom such as $A \sqsubseteq \exists r.(B \sqcap C)$ must first get a fresh name $Z \sqsubseteq B$, $Z \sqsubseteq C$, $A \sqsubseteq \exists r.Z$; otherwise the edge has no target node and CR4 at line L9 cannot look inside it.
- **Forgetting the backward direction.** A new name in $S(X)$ can fire $\exists r.A \sqsubseteq B$ at every node with an edge into $X$. If line L7 is left out and only line L9 handles CR4, the facts that reach $X$ after the edge was made are lost, and some subsumptions are missed.
- **Forgetting ⊥ along edges.** If line L10 and the ⊥ case of line L7 are left out, $A \sqsubseteq \exists r.B$ with $B \sqsubseteq \bot$ does not make $A$ unsatisfiable, and line L11 misses $A \sqsubseteq_T C$ for every $C$.
- **Extending with value restrictions.** Adding an axiom form $A \sqsubseteq \forall r.B$ with a rule "for each edge $(X, Y)$, add $B$ to $S(Y)$" is unsound: $S(Y)$ is shared by every node that points to $Y$. EL with value restrictions is EXPTIME-complete with general TBoxes.

## Implementations

## History

Early work on EL studied subsumption without a TBox and with acyclic or cyclic TBoxes. Brandt (2004) showed that subsumption stays polynomial with general concept inclusions and role hierarchies. Baader, Brandt and Lutz (2005) gave the algorithm in its present form, with the normal form and the completion rules, extended it with nominals, concrete domains and role inclusions, and showed that most other extensions make the problem EXPTIME-complete. The OWL 2 EL profile is based on this logic. Kazakov, Krötzsch and Simančík (2014) turned the rules into the concurrent reasoner ELK, which classifies very large medical ontologies in seconds.

## References
