---
tag: FW28XV
kind: definition
slug: computation-tree-logic
name: Computation tree logic
aliases:
- CTL
- Branching-time logic CTL
area: logic-and-constraints/model-checking
level: core
summary: A branching-time logic in which each temporal operator is directly preceded by a path quantifier. Each operator is a least or greatest fixed point, which is why CTL is checked in linear time.
prereqs: [kripke-structure, temporal-logic]
see_also: [ctl-model-checking, ctl-labelling-algorithm, ctl-model-checking-linear-time, ctl-satisfiability, ctl-star, linear-temporal-logic, modal-mu-calculus, fairness]
sources:
  - paper: doi:10.1007/BFb0025774
    title: Edmund M. Clarke and E. Allen Emerson, Design and synthesis of synchronization skeletons using branching time temporal logic, Logics of Programs Workshop 1981, Lecture Notes in Computer Science 131, 1982, pages 52 to 71
    locator: the definition of CTL, and its use for the synthesis of synchronization skeletons
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 6, Section 6.2 (syntax, semantics, equivalences and expansion laws of CTL) and Section 6.3 (CTL versus LTL)
  - book: isbn:9780521543101
    title: Michael Huth and Mark Ryan, Logic in Computer Science, second edition, Cambridge University Press, 2004
    locator: Section 3.4 (CTL syntax and semantics, adequate sets) and Section 3.7 (the fixed-point characterization of CTL)
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: Chapter 3 (CTL as a fragment of CTL*) and Chapter 6 (fixed-point characterizations used by symbolic model checking)
---

Computation tree logic (CTL) is a [temporal logic](/temporal-logic/) for branching time. Its formulas speak about the tree of all executions from a state, and each temporal operator ($\mathsf{X}$, $\mathsf{F}$, $\mathsf{G}$, $\mathsf{U}$) must come right after a path quantifier: $\mathsf{A}$ for "on every path" or $\mathsf{E}$ for "on some path". Clarke and Emerson introduced it in 1981. This restriction makes every CTL formula a state property and every operator a fixed point, so CTL can be checked in time linear in both the structure and the formula. This page defines the logic; [CTL model checking](/ctl-model-checking/) is the decision problem, the [CTL labelling algorithm](/ctl-labelling-algorithm/) is the algorithm that solves it, and the [linear-time theorem](/ctl-model-checking-linear-time/) is its bound.

## Definition

**Syntax.** Fix a set $AP$ of atomic propositions. CTL formulas are given by

$$\varphi ::= \mathit{true} \mid p \mid \neg\varphi \mid \varphi \wedge \varphi \mid \mathsf{EX}\,\varphi \mid \mathsf{E}[\varphi\,\mathsf{U}\,\varphi] \mid \mathsf{EG}\,\varphi \qquad (p \in AP).$$

The other operators are abbreviations:

| operator | definition |
|---|---|
| $\mathsf{AX}\,\varphi$ | $\neg\mathsf{EX}\,\neg\varphi$ |
| $\mathsf{EF}\,\varphi$ | $\mathsf{E}[\mathit{true}\,\mathsf{U}\,\varphi]$ |
| $\mathsf{AG}\,\varphi$ | $\neg\mathsf{EF}\,\neg\varphi$ |
| $\mathsf{AF}\,\varphi$ | $\neg\mathsf{EG}\,\neg\varphi$ |
| $\mathsf{A}[\varphi\,\mathsf{U}\,\psi]$ | $\neg\mathsf{E}[\neg\psi\,\mathsf{U}\,(\neg\varphi \wedge \neg\psi)] \wedge \neg\mathsf{EG}\,\neg\psi$ |

So $\{\mathsf{EX}, \mathsf{EU}, \mathsf{EG}\}$, with the Boolean connectives, is an *adequate set*. The size $|\varphi|$ is the number of symbols of $\varphi$ in this syntax.

**Semantics.** Let $M = (S, I, R, L)$ be a [Kripke structure](/kripke-structure/), with $R$ total. For a state $s$:

- $s \models \mathit{true}$; $s \models p$ iff $p \in L(s)$; negation and conjunction as usual.
- $s \models \mathsf{EX}\,\varphi$ iff some $t$ with $(s, t) \in R$ has $t \models \varphi$.
- $s \models \mathsf{E}[\varphi\,\mathsf{U}\,\psi]$ iff there is a path $s_0 s_1 \ldots$ with $s_0 = s$ and a $j \ge 0$ such that $s_j \models \psi$ and $s_i \models \varphi$ for each $i < j$.
- $s \models \mathsf{EG}\,\varphi$ iff there is a path $s_0 s_1 \ldots$ with $s_0 = s$ and $s_i \models \varphi$ for each $i \ge 0$.

Write $[\![\varphi]\!] = \{s \in S : s \models \varphi\}$, and $M \models \varphi$ iff $I \subseteq [\![\varphi]\!]$. Every CTL formula is a *state formula*: its truth depends only on the state.

**Fixed-point characterization.** Order the subsets of $S$ by inclusion, and let $\mathit{pre}_\exists(Z) = \{s : R(s) \cap Z \ne \emptyset\}$ be the set $[\![\mathsf{EX}\,Z]\!]$. Both maps below are monotone, so by the [Knaster-Tarski theorem](/knaster-tarski-theorem/) they have least and greatest fixed points.

*Theorem.* With $\mu$ the least and $\nu$ the greatest fixed point,

$$[\![\mathsf{EG}\,\varphi]\!] = \nu Z.\, [\![\varphi]\!] \cap \mathit{pre}_\exists(Z), \qquad [\![\mathsf{E}[\varphi\,\mathsf{U}\,\psi]]\!] = \mu Z.\, [\![\psi]\!] \cup ([\![\varphi]\!] \cap \mathit{pre}_\exists(Z)).$$

*Proof for $\mathsf{EG}$.* Let $f(Z) = [\![\varphi]\!] \cap \mathit{pre}_\exists(Z)$ and $G = [\![\mathsf{EG}\,\varphi]\!]$.

1. $G = f(G)$. If $s \in G$, take the witness path $s\,s_1 s_2 \ldots$. Then $s \models \varphi$, and $s_1 \in G$ by the suffix $s_1 s_2 \ldots$, so $s \in f(G)$. If $s \in f(G)$, then $s \models \varphi$ and some successor $t$ is in $G$; $s$ followed by a witness path of $t$ is a witness for $s$.
2. $G$ is the greatest fixed point. Let $Z = f(Z)$, or only $Z \subseteq f(Z)$. Each $s \in Z$ satisfies $\varphi$ and has a successor in $Z$. Starting from $s$, choose such a successor again and again; this gives an infinite path inside $Z$, so all its states satisfy $\varphi$, and $s \in G$. So $Z \subseteq G$. $\blacksquare$

*Proof for $\mathsf{EU}$.* Let $g(Z) = [\![\psi]\!] \cup ([\![\varphi]\!] \cap \mathit{pre}_\exists(Z))$ and $U = [\![\mathsf{E}[\varphi\,\mathsf{U}\,\psi]]\!]$.

1. $U = g(U)$, by the same unfolding: a witness either has $j = 0$ (then $s \models \psi$), or $s \models \varphi$ and the suffix from $s_1$ is a witness for $s_1$; and conversely.
2. $U$ is the least fixed point. Let $g(Z) \subseteq Z$. We show by induction on $j$ that a state with a witness of length $j$ is in $Z$. For $j = 0$, $s \models \psi$, so $s \in g(Z) \subseteq Z$. For $j > 0$, $s \models \varphi$ and $s_1$ has a witness of length $j - 1$, so $s_1 \in Z$ by induction, $s \in g(Z)$, and $s \in Z$. So $U \subseteq Z$. $\blacksquare$

The difference between $\nu$ and $\mu$ is the difference between "forever" and "eventually". A greatest fixed point allows an infinite path that never leaves $Z$; a least fixed point needs a finite witness, so $\mathsf{E}[\varphi\,\mathsf{U}\,\psi]$ does not hold on a path that satisfies $\varphi$ forever and never $\psi$. In the same way, with $\mathit{pre}_\forall(Z) = [\![\mathsf{AX}\,Z]\!]$ and the totality of $R$,

$$\mathsf{EF}\,\psi = \mu Z.\, \psi \vee \mathsf{EX}\,Z, \quad \mathsf{AF}\,\psi = \mu Z.\, \psi \vee \mathsf{AX}\,Z, \quad \mathsf{AG}\,\varphi = \nu Z.\, \varphi \wedge \mathsf{AX}\,Z, \quad \mathsf{A}[\varphi\,\mathsf{U}\,\psi] = \mu Z.\, \psi \vee (\varphi \wedge \mathsf{AX}\,Z).$$

On a finite structure the [Kleene iteration](/fixed-point/) reaches these fixed points in at most $|S|$ steps: the $i$-th iterate of $g$ from $\emptyset$ is the set of states with a witness of length less than $i$. These equations are the basis of symbolic model checking, and they make CTL a fragment of the [modal mu-calculus](/modal-mu-calculus/) with alternation depth 1.

## Examples and non-examples

**Mutual exclusion.** On the two-process structure of the [Kripke structure](/kripke-structure/) page, with initial state $(n, n, 1)$:

- $\mathsf{AG}\,\neg(c_1 \wedge c_2)$ holds (safety).
- $\mathsf{AG}(w_1 \to \mathsf{AF}\,c_1)$ fails at the initial state; $(w, n, 1)$ satisfies $w_1$ but not $\mathsf{AF}\,c_1$, because of the cycle $(w,n,1)\,(w,w,1)\,(w,c,0)$ on which $c_1$ never holds.
- $\mathsf{AG}(w_1 \to \mathsf{EF}\,c_1)$ holds: a waiting process can always get in, though it need not.
- $\mathsf{AG}\,\mathsf{EF}\,(n_1 \wedge n_2)$ holds: the initial state stays reachable.

**A small structure.** Take states $0, \ldots, 5$ with edges $0 \to 1, 2$; $1 \to 3$; $2 \to 2, 4$; $3 \to 0$; $4 \to 5$; $5 \to 4$, with $p$ true in $0, 1, 2, 3, 5$ and $q$ true in $3$. Then $[\![\mathsf{EG}\,p]\!] = \{0, 1, 2, 3\}$ (the cycle $0\,1\,3$ and the self-loop on $2$), $[\![\mathsf{E}[p\,\mathsf{U}\,q]]\!] = \{0, 1, 3\}$, and $[\![\mathsf{A}[p\,\mathsf{U}\,q]]\!] = \{1, 3\}$; state $0$ fails the last one because of its edge to $2$. The [labelling algorithm](/ctl-labelling-algorithm/) page works this example out step by step.

**Non-example: $\mathsf{AFG}$.** $\mathsf{A}\,\mathsf{F}\mathsf{G}\,p$ ("on each path, $p$ holds from some point on") is not a CTL formula, because $\mathsf{G}$ is not preceded by a quantifier. It is not equivalent to $\mathsf{AF}\,\mathsf{AG}\,p$: in the structure $s_0 \to s_0$, $s_0 \to s_1$, $s_1 \to s_2$, $s_2 \to s_2$ with $p$ in $s_0$ and $s_2$, each path satisfies $\mathsf{F}\mathsf{G}\,p$, but $\mathsf{AF}\,\mathsf{AG}\,p$ fails on the path $s_0 s_0 s_0 \ldots$, since $s_0$ can still reach $s_1$. No CTL formula expresses it; it is an [LTL](/linear-temporal-logic/) and [CTL*](/ctl-star/) property.

**Non-example: fairness.** $\mathsf{E}\,\mathsf{G}\mathsf{F}\,p$ ("some path visits $p$ infinitely often") is not CTL either. This is why [fair CTL](/fairness/) builds fairness into the semantics instead of the syntax.

## Related definitions

- **CTL model checking.** The problem of deciding $M \models \varphi$. See [CTL model checking](/ctl-model-checking/) for its complexity (P-complete, and PSPACE-complete for succinct structures), the [CTL labelling algorithm](/ctl-labelling-algorithm/) for the algorithm of Clarke, Emerson and Sistla, and the [linear-time theorem](/ctl-model-checking-linear-time/) for the $O(|M|\,|\varphi|)$ bound.
- **CTL satisfiability.** Whether some structure satisfies $\varphi$ is [EXPTIME-complete](/ctl-satisfiability/).
- **CTL*.** [CTL*](/ctl-star/) drops the rule that a quantifier must precede each temporal operator. It contains CTL and LTL.
- **Fragments.** ACTL uses only $\mathsf{A}$ (with negation only on atoms), and ECTL only $\mathsf{E}$. ACTL is preserved by [simulation](/simulation-relation/), which is the basis of abstraction for universal properties.
- **Bisimulation.** On finite structures, two states satisfy the same CTL formulas if and only if they are [bisimilar](/bisimulation/) (Browne, Clarke and Grumberg 1988), and CTL without $\mathsf{X}$ characterizes [stuttering equivalence](/stuttering-equivalence/).
- **Fair CTL and probabilistic CTL.** [Fair CTL](/fairness/) restricts the path quantifiers to fair paths. [PCTL](/probabilistic-ctl/) replaces them with probability bounds.

## References
