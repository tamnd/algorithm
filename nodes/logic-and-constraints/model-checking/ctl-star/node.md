---
tag: NNARR0
kind: definition
slug: ctl-star
name: CTL*
aliases:
- Full computation tree logic
- CTL star
area: logic-and-constraints/model-checking
level: advanced
summary: The branching-time logic that allows any mix of path quantifiers and LTL operators. It contains CTL and LTL, its model checking is PSPACE-complete, and its satisfiability is 2EXPTIME-complete.
prereqs: [computation-tree-logic, linear-temporal-logic]
see_also: [computation-tree-logic, linear-temporal-logic, ltl-model-checking, ctl-model-checking, modal-mu-calculus, temporal-logic, fairness, bisimulation]
sources:
  - paper: doi:10.1145/4904.4999
    title: E. Allen Emerson and Joseph Y. Halpern, "Sometimes" and "not never" revisited, on branching versus linear time temporal logic, Journal of the ACM 33(1), 1986, pages 151 to 178
    locator: the definition of CTL* and the comparison of its expressive power with CTL and LTL
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 6, Section 6.8 (CTL*, its relation to CTL and LTL, and CTL* model checking by LTL model checking of the innermost path formulas)
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: Chapter 3 (CTL* syntax and semantics, with CTL and LTL as sublogics) and Chapter 4 (model checking CTL* with a tableau for the LTL part)
  - paper: doi:10.1016/0167-6423(87)90036-0
    title: E. Allen Emerson and Chin-Laung Lei, Modalities for model checking, branching time logic strikes back, Science of Computer Programming 8(3), 1987, pages 275 to 306
    locator: the reduction of CTL* model checking to LTL model checking, with the same complexity
  - paper: doi:10.1145/3828.3837
    title: A. Prasad Sistla and Edmund M. Clarke, The complexity of propositional linear temporal logics, Journal of the ACM 32(3), 1985, pages 733 to 749
    locator: PSPACE-completeness of LTL model checking, which gives the lower bound for CTL*
---

CTL* is the branching-time [temporal logic](/temporal-logic/) that allows path quantifiers and temporal operators to be nested freely. [CTL](/computation-tree-logic/) requires a quantifier right before each temporal operator; [LTL](/linear-temporal-logic/) has no quantifier inside the formula at all; CTL* has both and everything between them, such as $\mathsf{A}(\mathsf{G}\mathsf{F}\,\mathit{req} \to \mathsf{G}\mathsf{F}\,\mathit{grant})$ or $\mathsf{E}\,\mathsf{G}\mathsf{F}\,p$. Emerson and Halpern defined it in 1983 (journal version 1986) to compare linear and branching time in one framework. Its model checking costs no more than LTL model checking: PSPACE-complete.

## Definition

Fix a set $AP$ of atomic propositions. CTL* has two kinds of formulas.

**State formulas** $\varphi ::= \mathit{true} \mid p \mid \neg\varphi \mid \varphi \wedge \varphi \mid \mathsf{E}\,\psi$, with $p \in AP$.

**Path formulas** $\psi ::= \varphi \mid \neg\psi \mid \psi \wedge \psi \mid \mathsf{X}\,\psi \mid \psi\,\mathsf{U}\,\psi$.

The usual abbreviations apply: $\mathsf{A}\,\psi = \neg\mathsf{E}\,\neg\psi$, $\mathsf{F}\,\psi = \mathit{true}\,\mathsf{U}\,\psi$, $\mathsf{G}\,\psi = \neg\mathsf{F}\,\neg\psi$. The formulas of CTL* are the state formulas.

**Semantics.** Let $M = (S, I, R, L)$ be a [Kripke structure](/kripke-structure/) with $R$ total, and let $\pi = s_0 s_1 \ldots$ be a path with suffixes $\pi^i$. State formulas are true or false at a state, and path formulas on a path:

- $s \models p$ iff $p \in L(s)$; Booleans as usual; $s \models \mathsf{E}\,\psi$ iff some path $\pi$ from $s$ has $\pi \models \psi$.
- $\pi \models \varphi$ for a state formula $\varphi$ iff $s_0 \models \varphi$.
- $\pi \models \mathsf{X}\,\psi$ iff $\pi^1 \models \psi$.
- $\pi \models \psi_1\,\mathsf{U}\,\psi_2$ iff there is $j \ge 0$ with $\pi^j \models \psi_2$ and $\pi^i \models \psi_1$ for each $i < j$.

$M \models \varphi$ iff each initial state satisfies $\varphi$.

**The sublogics.**

- **CTL** is the fragment in which each $\mathsf{X}$ and $\mathsf{U}$ is directly under $\mathsf{E}$ or $\mathsf{A}$, with only state formulas as its arguments.
- **LTL** is the set of formulas $\mathsf{A}\,\psi$ where $\psi$ is a path formula whose only state subformulas are atomic propositions. $M$ satisfies the LTL formula $\psi$ exactly when its initial states satisfy the CTL* formula $\mathsf{A}\,\psi$.

**Expressiveness.** $\mathrm{CTL} \cup \mathrm{LTL} \subsetneq \mathrm{CTL}^*$. CTL and LTL are incomparable: $\mathsf{AG}\,\mathsf{EF}\,p$ is not in LTL, and $\mathsf{A}\,\mathsf{F}\mathsf{G}\,p$ is not in CTL (Emerson and Halpern 1986). Their disjunction $\mathsf{A}\,\mathsf{F}\mathsf{G}\,p \vee \mathsf{AG}\,\mathsf{EF}\,p$ is a CTL* formula in neither logic. In turn, each CTL* formula can be translated into the [modal mu-calculus](/modal-mu-calculus/) (Dam 1994), with an exponential blow-up, and the inclusion is strict.

**Model checking: PSPACE-complete.** *Algorithm.* Process the state subformulas of $\varphi$ from the inside out. Take an innermost subformula $\mathsf{E}\,\psi$. All the state subformulas of $\psi$ are already labelled, so replace each maximal one by a fresh atomic proposition; now $\psi$ is an LTL formula. Then $s \models \mathsf{E}\,\psi$ if and only if $s \not\models \mathsf{A}\,\neg\psi$, which is one [LTL model checking](/ltl-model-checking/) question per state, answered for all states at once by a product with a [Büchi automaton](/buchi-automaton/) for $\psi$ and an analysis of its strongly connected components. Label the states, and continue outward.

*Cost.* Each LTL step costs $O(|M| \cdot 2^{O(|\psi|)})$ time, and the sizes of the path formulas add up to at most $|\varphi|$, so the total is $O(|M| \cdot 2^{O(|\varphi|)})$. Each LTL step also runs in space polynomial in $|M|$ and $|\psi|$, and the labels need $|S| \cdot |\varphi|$ Boolean values, so the whole algorithm runs in polynomial space. The lower bound holds already for LTL, the fragment $\mathsf{A}\,\psi$, which is PSPACE-hard (Sistla and Clarke 1985). So CTL* model checking is PSPACE-complete, and in time it is linear in $|M|$ (Emerson and Lei 1987). The extra power over CTL costs an exponential in the formula, not in the structure.

**Satisfiability: 2EXPTIME-complete.** Whether a CTL* formula has a model is complete for doubly exponential time: the upper bound is by tree automata (Emerson and Jutla), and the lower bound is Vardi and Stockmeyer (1985). This is one exponential more than [CTL satisfiability](/ctl-satisfiability/) and two more than LTL satisfiability.

## Examples and non-examples

**Strong fairness as a premise.** On the two-process mutual exclusion structure of the [Kripke structure](/kripke-structure/) page, let $\mathit{en}_1 = w_1 \wedge (y = 1)$. Then

$$\mathsf{A}\big((\mathsf{G}\mathsf{F}\,\mathit{en}_1 \to \mathsf{G}\mathsf{F}\,c_1) \to \mathsf{G}(w_1 \to \mathsf{F}\,c_1)\big)$$

holds: every path that is strongly fair to process 1 lets a waiting process 1 enter. Without the premise, $\mathsf{A}\,\mathsf{G}(w_1 \to \mathsf{F}\,c_1)$ fails on the cycle $(w,n,1)\,(w,w,1)\,(w,c,0)$, where $\mathit{en}_1$ holds infinitely often and $c_1$ never. This formula is in LTL (and so in CTL*), not in CTL. CTL handles the same question with [fair CTL](/fairness/).

**Existential fairness.** $\mathsf{E}\,\mathsf{G}\mathsf{F}\,p$ (some path visits $p$ infinitely often) is a CTL* formula. It is in neither CTL nor LTL: LTL has no $\mathsf{E}$ inside formulas, and CTL cannot write $\mathsf{G}\mathsf{F}$ under one quantifier.

**Nested quantifiers on a path.** $\mathsf{A}\,\mathsf{G}(\mathit{req} \to \mathsf{F}\,\mathsf{E}\mathsf{X}\,\mathit{grant})$ says that after each request, the path reaches a state from which a grant is possible in one step. The state formula $\mathsf{EX}\,\mathit{grant}$ sits inside a path formula, which LTL does not allow.

**Non-example: a path formula alone.** $\mathsf{G}\mathsf{F}\,p$ is a path formula, not a CTL* formula; it becomes one under $\mathsf{A}$ or $\mathsf{E}$. Papers often write the LTL formula $\mathsf{G}\mathsf{F}\,p$ and mean $\mathsf{A}\,\mathsf{G}\mathsf{F}\,p$.

## Related definitions

- **CTL and LTL.** [CTL](/computation-tree-logic/) and [LTL](/linear-temporal-logic/) are the two practical fragments. CTL is checked in time $O(|M|\,|\varphi|)$ by the [labelling algorithm](/ctl-labelling-algorithm/); LTL and CTL* need an exponential in $|\varphi|$.
- **CTL+ and fair CTL.** CTL+ allows Boolean combinations of temporal operators under one quantifier, such as $\mathsf{E}(\mathsf{F}\,p \wedge \mathsf{F}\,q)$. It is as expressive as CTL, but its model checking is $\Delta_2^p$-complete (Laroussinie, Markey and Schnoebelen 2001). [Fair CTL](/fairness/) is the fragment of CTL* with fairness premises that CTL algorithms handle with strongly connected components.
- **Bisimulation.** Two states of finite structures satisfy the same CTL* formulas if and only if they are [bisimilar](/bisimulation/), and the same holds for CTL. So CTL* does not separate more states than CTL; it expresses more properties of a given state.
- **Mu-calculus.** The [modal mu-calculus](/modal-mu-calculus/) is strictly more expressive than CTL*; for example, "$p$ holds at each even position of each path" is in the mu-calculus and not in CTL*.

## References
