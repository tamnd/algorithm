---
tag: DQ8M2F
kind: algorithm
slug: structural-subsumption
name: Structural subsumption algorithm
aliases:
- normalize-compare subsumption
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: core
summary: Normalizes two concepts of a small description logic and compares them part by part. It is sound and complete for FL-, but it fails once role restrictions or full negation are added.
solves: [concept-subsumption]
model: word-ram
complexity:
  vars: {n: the total size of the two concepts}
  time: {expected: O(n), worst: O(n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, exact: true, recursive: true, builds_counter_model: true}
history:
  year: 1984
  people: [Ronald J. Brachman, Hector J. Levesque]
  note: Brachman and Levesque gave a polynomial subsumption test for the language FL- and showed that adding role restrictions, which gives FL, makes subsumption coNP-hard. Their paper started the study of the trade-off between expressive power and the cost of reasoning in description logics.
prereqs: [description-logic, concept-subsumption]
see_also: [alc-tableau-algorithm, el-classification, el-description-logic, ontology-classification, alc-description-logic]
sources:
  - paper: "Ronald J. Brachman and Hector J. Levesque, The tractability of subsumption in frame-based description languages, Proceedings of the 4th National Conference on Artificial Intelligence (AAAI-84), AAAI Press, 1984"
    locator: pages 34 to 37 (FL- with a polynomial subsumption test, and the coNP-hardness of FL)
  - paper: doi:10.1111/j.1467-8640.1987.tb00176.x
    title: Hector J. Levesque and Ronald J. Brachman, Expressiveness and tractability in knowledge representation and reasoning, Computational Intelligence 3, 1987
    locator: pages 78 to 93 (the trade-off between expressive power and tractable reasoning, general locator)
  - book: isbn:9780521876254
    title: Franz Baader, Diego Calvanese, Deborah L. McGuinness, Daniele Nardi and Peter F. Patel-Schneider (eds.), The Description Logic Handbook, second edition, Cambridge University Press, 2007
    locator: Chapter 2, Basic Description Logics, by Franz Baader and Werner Nutt (structural subsumption algorithms, general locator)
  - paper: doi:10.1613/jair.56
    title: Alexander Borgida and Peter F. Patel-Schneider, A semantics and complete algorithm for subsumption in the CLASSIC description logic, Journal of Artificial Intelligence Research 1, 1994
    locator: pages 277 to 308 (normalization and structural comparison for the CLASSIC language)
  - paper: "Bernhard Nebel, Terminological reasoning is inherently intractable, Artificial Intelligence 43(2), 1990"
    locator: subsumption with respect to acyclic TBoxes is coNP-hard already for very small languages (general locator)
---

Structural subsumption decides whether one concept of a small [description logic](/description-logic/) is subsumed by another. It puts both concepts in a normal form and then compares the normal forms part by part, with no search. For the language FL- it is sound and complete and runs in linear time. Early frame-based systems used it, and it fails as soon as the language has role restrictions, disjunction or full negation.

## In plain words

You have two descriptions, and you want to know if everything that fits the first one must fit the second. First you tidy each description: you collect the plain properties, the kinds of links that must exist, and, for each kind of link, everything that all linked objects must satisfy. Then you go through the second description piece by piece. Each property it asks for must be in the first one. Each link it asks for must be there too. For each kind of link, the demands on the linked objects must again pass the same test, one level down. If one piece is missing, the answer is no, and the missing piece shows how to build an object that fits the first description and not the second.

## The problem

The input is two concepts $C$ and $D$ of FL-, and there is no TBox. FL- concepts are built from concept names $A$, the top concept $\top$, conjunction $C \sqcap D$, value restriction $\forall r.C$ and unqualified existential restriction $\exists r.\top$, written $\exists r$. The question is [concept subsumption](/concept-subsumption/): does $C^I \subseteq D^I$ hold in every interpretation $I = (\Delta^I, \cdot^I)$? We write $C \sqsubseteq D$.

FL- has no $\bot$ and no negation, so every concept is satisfiable, and no part of a concept can make another part true by a contradiction. This is why a comparison of parts is enough. FL0 is the part of FL- without $\exists r$, and the same method works for it.

## The algorithm

The normal form of a concept is a tree. Each node $x$ has a set $N_x$ of concept names, a set $E_x$ of roles with $\exists r$, and at most one child $V_x(r)$ for each role $r$, which collects the fillers of all value restrictions on $r$ at that place. The equivalences $\forall r.(C \sqcap D) \equiv \forall r.C \sqcap \forall r.D$ and $\forall r.\top \equiv \top$ justify the merge and the removal of empty children.

```pseudo id=main
NORMALIZE(C)
L1  root ← a new node with N = ∅, E = ∅ and no children
L2  INSERT(root, C)
L3  remove every child V_x(r) whose subtree has no names and no roles   ▷ ∀r.⊤ is ⊤
L4  return root

INSERT(x, C)
L5  if C is a concept name A then add A to N_x
L6  if C is ∃r then add r to E_x
L7  if C is C1 ⊓ C2 then INSERT(x, C1); INSERT(x, C2)
L8  if C is ∀r.C1 then if V_x(r) is undefined, set V_x(r) ← a new empty node; INSERT(V_x(r), C1)
                                                                ▷ C = ⊤ adds nothing

SUBSUMES(c, d)                                ▷ c, d: normal forms of C and D; true iff C ⊑ D
L9  if N_d ⊄ N_c or E_d ⊄ E_c then return false
L10 for each role r with V_d(r) defined do
L11     if V_c(r) is undefined or SUBSUMES(V_c(r), V_d(r)) is false then return false
L12 return true
```

INSERT walks the concept once. Line L8 sends every value restriction on $r$ at the same place to the same child, so $\forall r.A \sqcap \forall r.B$ and $\forall r.(A \sqcap B)$ get the same tree. Line L3 runs bottom up, so a chain such as $\forall r.\forall s.\top$ disappears completely.

SUBSUMES then reads the conjuncts of $D$ off its tree. A name or an $\exists r$ of $D$ must be a conjunct of $C$ at the same place (line L9). A value restriction $\forall r.D'$ of $D$ needs a value restriction $\forall r.C'$ of $C$ with $C' \sqsubseteq D'$ (line L11). If $C$ has no value restriction on $r$, then $C$ says nothing about its $r$-successors, and since $V_d(r)$ is not empty after line L3, the answer is no.

When the answer is no, the failing test gives a counter-model. Build a tree for $C$ with one $r$-successor for each $r \in E_c$. At the node where line L9 fails, the missing name or the missing successor already makes the element fail $D$. Where line L11 fails for $r$, give the element one $r$-successor that is, recursively, in $C'$ but not in $D'$.

## Example

Take $C = A \sqcap \exists r \sqcap \forall r.A \sqcap \forall r.(B \sqcap \forall s.A)$ and $D = \exists r \sqcap \forall r.(A \sqcap B) \sqcap \forall r.\forall s.\top$.

| step | line | state |
|---|---|---|
| 1 | L5 to L8 | root of $C$: $N = \{A\}$, $E = \{r\}$; child for $r$: $N = \{A, B\}$; its child for $s$: $N = \{A\}$ |
| 2 | L5 to L8 | root of $D$: $N = \emptyset$, $E = \{r\}$; child for $r$: $N = \{A, B\}$; its child for $s$ is empty |
| 3 | L3 | the empty child for $s$ in $D$ is removed |
| 4 | L9 | root: $\emptyset \subseteq \{A\}$ and $\{r\} \subseteq \{r\}$, pass |
| 5 | L11 | role $r$: compare the two children |
| 6 | L9 | $\{A, B\} \subseteq \{A, B\}$ and $\emptyset \subseteq \emptyset$, pass; $D$ has no child here |
| 7 | L12 | return true, so $C \sqsubseteq D$ |

The normal forms print as $A \sqcap \exists r \sqcap \forall r.(A \sqcap B \sqcap \forall s.A)$ and $\exists r \sqcap \forall r.(A \sqcap B)$.

Now take $D' = \forall r.\forall s.B$. Its tree has a child for $r$ with a child for $s$ that holds $\{B\}$. At that depth line L9 finds $\{B\} \not\subseteq \{A\}$ and returns false. The counter-model has 3 elements: element 0 in $A$, an $r$-edge to element 1 in $A$ and $B$, and an $s$-edge from 1 to element 2 in $A$ only. Element 0 is in $C$, and it is not in $D'$ because element 2 is not in $B$.

## Correctness

The invariant of NORMALIZE is that after each call INSERT$(x, C')$ the concept read off the tree at $x$ is equivalent to the old one conjoined with $C'$. Line L3 keeps the equivalence because $\forall r.\top \equiv \top$. Soundness of SUBSUMES is an induction on the depth of $d$: each conjunct of $D$ is a conjunct of $C$, or follows from a value restriction of $C$ by induction. Completeness is the counter-model construction above, which is a finite tree. With one role name the counter-model is a path, so it has at most one more element than the larger role depth of $C$ and $D$. The full proof is in proofs/correctness.md.

## Complexity

NORMALIZE does a constant number of set and map operations for each name and constructor of the concept, and SUBSUMES visits each node of the tree of $D$ once and pairs it with one node of the tree of $C$. With hash sets the expected time is $O(n)$, where $n = |C| + |D|$. With sorted sets the time is $O(n \log n)$ in the worst case. The space is $O(n)$. Brachman and Levesque (1984) stated a polynomial bound for FL-.

## Properties

- **Deterministic.** There is no choice and no backtracking.
- **Exact for FL- and FL0.** The answer is right in both directions, and a "no" comes with a counter-model.
- **Syntax directed.** The test compares conjuncts at the same role path, so it is easy to explain which part of $D$ is missing in $C$.
- **Normal form is canonical.** Two FL- concepts are equivalent if and only if they have the same normal form, up to the order of names and roles.

## Variants and improvements

- **CLASSIC.** Borgida and Patel-Schneider (1994) gave a normalize and compare algorithm for the CLASSIC language, with number restrictions and other constructors, and proved it complete with respect to a semantics they defined for it.
- **ALN and languages with ⊥.** With $\bot$, atomic negation or number restrictions, the normal form must first find the parts that are unsatisfiable, such as $A \sqcap \neg A$ or $(\geq 2\, r) \sqcap (\leq 1\, r)$, and replace them by $\bot$. Then the comparison works again for such small languages.
- **Acyclic TBoxes.** Unfold the defined names first and then compare. The unfolding can be exponentially large, and Nebel (1990) showed that subsumption with respect to acyclic TBoxes is coNP-hard even for very small languages.
- **Larger languages.** For [ALC](/alc-description-logic/), use the [tableau algorithm](/alc-tableau-algorithm/). For the [EL family](/el-description-logic/) with a TBox, use [EL classification](/el-classification/).

## When to use it

Use it when the language has only conjunction, value restrictions and unqualified existentials, possibly with simple number restrictions, and you need many subsumption tests, for example to [classify](/ontology-classification/) the concepts of a small frame-based knowledge base. It is fast and easy to explain. Do not use it for a language with disjunction, full negation or qualified existentials together with value restrictions; there it gives wrong "no" answers.

## Pitfalls

- **Keeping empty value restrictions.** If line L3 is left out, $D = \forall r.\top$ keeps an empty child for $r$, and line L11 returns false for $C = A$, although $A \sqsubseteq \forall r.\top$ holds. Remove empty children at line L3 before any comparison.
- **Not merging value restrictions.** If line L8 makes a new child for each $\forall r.C_1$ instead of reusing $V_x(r)$, then $C = \forall r.A \sqcap \forall r.B$ has two children for $r$, and no one of them is below $A \sqcap B$. The test then says no to $C \sqsubseteq \forall r.(A \sqcap B)$, which holds. Line L8 must reuse the child.
- **Adding role restrictions.** FL adds the restricted role $(r : C)$, the $r$-successors that are in $C$. Then $\exists (r : A) \sqcap \forall (r : A).B \sqsubseteq \exists (r : B)$ holds, because the $r$-successor in $A$ must also be in $B$. A part-by-part test at line L9 sees that the role $(r : B)$ is not among the roles of the left side and says no. The correct answer needs reasoning by cases, and subsumption in FL is coNP-hard (Brachman and Levesque 1984).
- **Qualified existentials with value restrictions.** In a language with both $\exists r.C$ and $\forall r.C$, the concept $\exists r.A \sqcap \forall r.B$ is subsumed by $\exists r.(A \sqcap B)$. A comparison that matches $\exists r.(A \sqcap B)$ only with $\exists r.A$ misses this. The value restrictions must first be pushed into each existential of the normal form.

## Implementations

## History

Brachman and Levesque (1984) studied the language FL-, a part of the KL-ONE family, and gave a polynomial algorithm for its subsumption problem. In the same paper they showed that adding role restrictions makes the problem coNP-hard, and Levesque and Brachman (1987) put this into a general trade-off between expressive power and tractability. Nebel (1990) showed that TBoxes add their own source of hardness. Systems of the late 1980s and early 1990s, such as CLASSIC, used normalize and compare methods. For CLASSIC, Borgida and Patel-Schneider (1994) proved the method complete with respect to a semantics they defined for the language. Later systems for expressive logics moved to tableau algorithms, which handle disjunction and negation.

## References
