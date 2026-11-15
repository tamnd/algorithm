---
tag: A6ABQH
kind: theorem
slug: alc-modal-k-correspondence
name: Schild's correspondence theorem
aliases:
- ALC as multimodal K
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: advanced
summary: ALC is a notational variant of the multimodal logic K, with roles as accessibility relations, so results transfer between them.
prereqs: [alc-description-logic, kripke-structure]
see_also: [alc-pspace-completeness, alc-general-tbox-exptime, bisimulation, modal-mu-calculus, temporal-logic, description-logic, tbox-and-abox, concept-subsumption]
sources:
  - paper: "Klaus Schild, A correspondence theory for terminological logics: preliminary report, Proceedings of the 12th International Joint Conference on Artificial Intelligence (IJCAI), 1991"
    locator: pages 466 to 471 (ALC as a notational variant of multimodal K, and the translation of role constructors into propositional dynamic logic)
  - paper: doi:10.1137/0206033
    title: Richard E. Ladner, The computational complexity of provability in systems of modal propositional logic, SIAM Journal on Computing 6(3), 1977
    locator: pages 467 to 480 (satisfiability in the modal logic K is PSPACE-complete)
  - paper: doi:10.1016/0022-0000(79)90046-1
    title: Michael J. Fischer and Richard E. Ladner, Propositional dynamic logic of regular programs, Journal of Computer and System Sciences 18(2), 1979
    locator: pages 194 to 211 (the EXPTIME lower bound for propositional dynamic logic)
  - paper: "Vaughan R. Pratt, Models of program logics, Proceedings of the 20th Annual Symposium on Foundations of Computer Science (FOCS), 1979"
    locator: pages 115 to 122 (an exponential time decision procedure for propositional dynamic logic)
  - book: isbn:9780521876254
    title: Franz Baader, Diego Calvanese, Deborah L. McGuinness, Daniele Nardi and Peter F. Patel-Schneider (eds.), The Description Logic Handbook, second edition, Cambridge University Press, 2007
    locator: the chapter on the relationships of description logics with other formalisms, including modal logics (general locator)
---

Schild observed in 1991 that the [description logic](/description-logic/) [ALC](/alc-description-logic/) and the multimodal logic $\mathrm{K}_m$ are the same logic in two notations. A concept name is a propositional variable, a role name is an accessibility relation, $\exists r.C$ is the diamond $\langle r \rangle$ and $\forall r.C$ is the box $[r]$. An interpretation is a [Kripke structure](/kripke-structure/), and an element is in a concept exactly when the formula holds at that world. So every result about satisfiability, complexity or expressive power of one logic is a result about the other. Inclusions of a general TBox correspond to the universal modality, and regular role constructors correspond to propositional dynamic logic.

## Statement

Fix concept names $A_1, A_2, \ldots$ and role names $r_1, \ldots, r_m$. ALC concepts are built from the names, $\top$ and $\bot$ with $\neg$, $\sqcap$, $\sqcup$, $\exists r_i.C$ and $\forall r_i.C$. Formulas of $\mathrm{K}_m$ are built from propositional variables $p_1, p_2, \ldots$, $\top$ and $\bot$ with $\neg$, $\wedge$, $\vee$, $\langle i \rangle$ and $[i]$ for $i = 1, \ldots, m$. A Kripke model $M = (W, R_1, \ldots, R_m, V)$ has a non-empty set $W$ of worlds, relations $R_i \subseteq W \times W$ and a valuation $V$ that maps each variable to a subset of $W$.

The translation $\pi$ sends $A_j$ to $p_j$, $\top$ to $\top$, $\bot$ to $\bot$, and

$$\pi(\neg C) = \neg \pi(C), \quad \pi(C \sqcap D) = \pi(C) \wedge \pi(D), \quad \pi(C \sqcup D) = \pi(C) \vee \pi(D), \quad \pi(\exists r_i.C) = \langle i \rangle \pi(C), \quad \pi(\forall r_i.C) = [i]\, \pi(C).$$

An interpretation $I$ gives the Kripke model $M_I$ with $W = \Delta^I$, $R_i = r_i^I$ and $V(p_j) = A_j^I$, and every Kripke model arises in this way from exactly one interpretation.

**Theorem.**

1. $\pi$ is a bijection from ALC concepts onto $\mathrm{K}_m$ formulas, and $I \mapsto M_I$ is a bijection from interpretations onto Kripke models.
2. For every concept $C$, interpretation $I$ and element $d$: $d \in C^I$ if and only if $M_I, d \models \pi(C)$.
3. So $C$ is satisfiable if and only if $\pi(C)$ is satisfiable in $\mathrm{K}_m$, and $C \sqsubseteq D$ holds if and only if $\pi(C) \to \pi(D)$ is valid in $\mathrm{K}_m$.
4. Let $\mathcal T$ be a general TBox and $C_{\mathcal T} = \bigsqcap_{X \sqsubseteq Y \in \mathcal T} (\neg X \sqcup Y)$. Then $C$ is satisfiable with respect to $\mathcal T$ if and only if $\pi(C) \wedge \mathrm{A}\, \pi(C_{\mathcal T})$ is satisfiable in $\mathrm{K}_m$ with the universal modality $\mathrm{A}$, where $M, w \models \mathrm{A} \varphi$ means that $\varphi$ holds at every world. It is also equivalent to the satisfiability of $\pi(C) \wedge [(r_1 \cup \cdots \cup r_m)^*]\, \pi(C_{\mathcal T})$ in propositional dynamic logic, where $r_1, \ldots, r_m$ are the roles that occur in $C$ and $\mathcal T$.

## In plain words

A description logic talks about objects, their kinds, and the links between them. Modal logic talks about worlds, the facts true in them, and which worlds can see which others. For ALC and the basic modal logic K these are the same thing with different names: an object is a world, a kind is a fact, and a link is a way of seeing. Each statement in one language becomes one statement in the other, true in the same places. So anything proved about one language, such as how hard it is to decide or which models it needs, holds for the other one too.

## Proof

*Parts 1 and 2.* $\pi$ maps each constructor to one connective and back, so it is a bijection by induction on the structure; the inverse sends $\langle i \rangle$ to $\exists r_i$ and $[i]$ to $\forall r_i$. An interpretation and a Kripke model are the same data: a non-empty set, one binary relation for each $r_i$, one subset for each name. For part 2 use induction on $C$. For names, $d \in A_j^I$ if and only if $d \in V(p_j)$. The Boolean cases follow because both semantics read $\neg$, $\sqcap$ and $\sqcup$ as complement, intersection and union. For $\exists r_i.C$, $d \in (\exists r_i.C)^I$ if and only if some $e$ has $(d, e) \in r_i^I$ and $e \in C^I$, if and only if some $e$ has $d R_i e$ and $M_I, e \models \pi(C)$ by induction, which is the definition of $M_I, d \models \langle i \rangle \pi(C)$. The case of $\forall r_i.C$ and $[i]$ is the same with "every" for "some".

*Part 3.* $C$ is satisfiable if some $C^I$ is not empty, which by part 2 means that $\pi(C)$ holds at some world of some model; by part 1 every model is some $M_I$. $C \sqsubseteq D$ means $C^I \subseteq D^I$ for every $I$, which by part 2 means that $\pi(C) \to \pi(D)$ holds at every world of every model.

*Part 4.* $I$ is a model of $\mathcal T$ if and only if $C_{\mathcal T}^I = \Delta^I$, which by part 2 means $M_I, w \models \mathrm{A}\, \pi(C_{\mathcal T})$ at any world $w$. So $d \in C^I$ for a model $I$ of $\mathcal T$ gives $M_I, d \models \pi(C) \wedge \mathrm{A}\, \pi(C_{\mathcal T})$, and the converse is the same argument read backwards. For the second form, $[(r_1 \cup \cdots \cup r_m)^*] \varphi$ holds at $d$ when $\varphi$ holds at every world reachable from $d$ along the relations $R_1, \ldots, R_m$. If $I$ is a model of $\mathcal T$, $C_{\mathcal T}$ holds everywhere, so the formula holds at any $d \in C^I$. Conversely, if the formula holds at $d$ in some model, let $I'$ be the part of the model that is reachable from $d$, with the relations and the valuation restricted to it. The truth of a $\mathrm{K}_m$ formula at a world depends only on the worlds reachable from it along the relations that the formula mentions, so $d \in C^{I'}$ and every element of $I'$ is in $C_{\mathcal T}^{I'}$. Thus $I'$ is a model of $\mathcal T$ in which $C$ is not empty. $\blacksquare$

For example, $\exists \mathit{hasChild}.\mathit{Doctor} \sqcap \forall \mathit{hasChild}.\mathit{Rich}$ becomes $\langle \mathit{hasChild} \rangle \mathit{Doctor} \wedge [\mathit{hasChild}]\, \mathit{Rich}$. The subsumption $\forall r.(\neg A \sqcup B) \sqcap \forall r.A \sqsubseteq \forall r.B$ is the distribution axiom $[r](p \to q) \to ([r]p \to [r]q)$ that gives the logic K its name.

## Consequences

- *Complexity without a TBox.* Ladner proved in 1977 that satisfiability in K is PSPACE-complete. By part 3 this gives [PSPACE-completeness for ALC](/alc-pspace-completeness/) with one role, and the upper bound for ALC with many roles gives it for $\mathrm{K}_m$.
- *Complexity with a TBox.* By part 4 and the upper bound of Pratt for propositional dynamic logic, satisfiability with respect to general TBoxes is in EXPTIME. The [EXPTIME theorem](/alc-general-tbox-exptime/) proves both bounds directly.
- *Model theory.* ALC concepts are invariant under [bisimulation](/bisimulation/), have the tree model property, and have the finite model property, as modal formulas do. The type elimination in the proof of the EXPTIME theorem builds a model whose size is at most exponential in the input, also with respect to a general TBox.
- *Methods.* Tableau calculi, filtration, automata on infinite trees and the [modal mu-calculus](/modal-mu-calculus/) all come to description logics through the translation, and description logic reasoners can decide modal satisfiability.
- *Extensions.* Schild extended the translation: union, composition and reflexive transitive closure of roles give propositional dynamic logic. In the same way the inverse of a role gives a converse modality. These correspondences carry the EXPTIME bounds of dynamic logic to the matching description logics.

## Tightness

- *General TBoxes need more than K.* No ALC concept can express a TBox. Take $I_1$ with one element $d \in A^{I_1}$ and no edges, and let $I_2$ add an element $e \notin A^{I_2}$ with no edges. Every concept $C$ has $d \in C^{I_1}$ if and only if $d \in C^{I_2}$, because truth at $d$ depends only on the part reachable from $d$. But $I_1$ is a model of $\{\top \sqsubseteq A\}$ and $I_2$ is not. This is why part 4 needs the universal modality or the master modality $[(r_1 \cup \cdots \cup r_m)^*]$, and why the complexity rises from PSPACE to EXPTIME.
- *ABoxes and other constructors.* Individual names have no counterpart in $\mathrm{K}_m$; they need nominals, as in hybrid logic. Number restrictions need graded modalities. The correspondence of the theorem is exact only for ALC.
- *The number of roles.* Each role name is one modality, so $\mathrm{K}_m$ with $m$ fixed matches ALC with at most $m$ role names. The case $m = 1$ is the basic modal logic K.

## History

Modal logic K and its Kripke semantics were developed long before description logics. Ladner proved the PSPACE bound for K in 1977, and Fischer and Ladner the EXPTIME bound for propositional dynamic logic in 1979. ALC was introduced by Schmidt-Schauß and Smolka in 1991 as a terminological logic. In the same year Schild published the correspondence at IJCAI. He used it to transfer complexity results from dynamic logic to terminological logics with role constructors and general inclusions. After his paper, much work on description logics used methods from modal logic, and the Description Logic Handbook treats these relationships in a chapter of their own.

## References
