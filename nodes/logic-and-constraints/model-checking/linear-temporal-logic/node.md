---
tag: AV91RM
kind: definition
slug: linear-temporal-logic
name: Linear temporal logic
aliases:
- LTL
- propositional linear temporal logic
- PLTL
area: logic-and-constraints/model-checking
level: core
summary: A logic whose formulas talk about one infinite sequence of states, with the operators next, until and the derived eventually and always. A system satisfies a formula when every one of its paths does.
prereqs: [kripke-structure]
see_also: [computation-tree-logic, ctl-star, buchi-automaton, ltl-model-checking, ltl-satisfiability, ltl-to-buchi-translation, stuttering-equivalence, predicate-specification-patterns]
sources:
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 5, Section 5.1 (syntax, semantics over words and over transition systems, equivalences, weak until and release), and Chapter 7, Section 7.7 (stutter equivalence and the stutter invariance of LTL without next)
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: Chapter 3 (CTL*, CTL and LTL over Kripke structures) and Chapter 10 (LTL without the next operator and stuttering)
  - paper: doi:10.1109/SFCS.1977.32
    title: Amir Pnueli, The temporal logic of programs, 18th Annual Symposium on Foundations of Computer Science (FOCS 1977), IEEE, 1977, pages 46 to 57
    locator: the proposal to specify reactive programs with temporal operators over computations
  - paper: doi:10.1016/S0020-0190(97)00133-6
    title: Doron Peled and Thomas Wilke, Stutter-invariant temporal properties are expressible without the next-time operator, Information Processing Letters 63(5), 1997
    locator: main theorem
  - paper: "Pierre Wolper, Temporal logic can be more expressive, Information and Control 56(1-2), 1983"
    locator: the property "p holds at every even position" is not expressible in LTL
  - paper: "Dov Gabbay, Amir Pnueli, Saharon Shelah and Jonathan Stavi, On the temporal analysis of fairness, 7th ACM Symposium on Principles of Programming Languages (POPL 1980)"
    locator: expressive completeness of until and since with respect to first-order logic over the natural numbers (with Kamp's 1968 thesis)
---

Linear temporal logic (LTL) is a logic for statements about one infinite run of a system, read as a sequence of states in time. Its formulas are built from atomic propositions with the Boolean connectives and two temporal operators, $\mathsf{X}$ ("next") and $\mathsf{U}$ ("until"); "eventually" $\mathsf{F}$ and "always" $\mathsf{G}$ are derived from them. A [Kripke structure](/kripke-structure/) satisfies an LTL formula when every path from an initial state satisfies it. Amir Pnueli proposed temporal logic for the specification of programs in 1977, and LTL is the input language of explicit-state checkers such as SPIN.

## Definition

**Notation.** On this page and the other model checking pages, $M = (S, I, R, L)$ is a Kripke structure over a finite set $AP$ of atomic propositions, with $|S|$ states and $|R|$ transitions, and $|M| = |S| + |R|$. A formula is $\varphi$ and its size $|\varphi|$ is the number of symbols in it.

**Syntax.** The LTL formulas over $AP$ are given by the grammar

$$\varphi ::= \mathsf{true} \mid p \mid \neg \varphi \mid \varphi \wedge \varphi \mid \mathsf{X}\, \varphi \mid \varphi\, \mathsf{U}\, \varphi \qquad (p \in AP).$$

The other connectives are abbreviations: $\varphi \vee \psi$, $\varphi \to \psi$ and $\mathsf{false}$ as usual, and

| Operator | Definition | Reading |
|---|---|---|
| $\mathsf{F}\,\varphi$ | $\mathsf{true}\ \mathsf{U}\ \varphi$ | eventually $\varphi$ |
| $\mathsf{G}\,\varphi$ | $\neg \mathsf{F} \neg \varphi$ | always $\varphi$ |
| $\varphi\, \mathsf{R}\, \psi$ | $\neg(\neg \varphi\ \mathsf{U}\ \neg \psi)$ | $\psi$ holds until and including the first $\varphi$, or forever |
| $\varphi\, \mathsf{W}\, \psi$ | $(\varphi\ \mathsf{U}\ \psi) \vee \mathsf{G}\,\varphi$ | weak until: $\psi$ need not come |

**Semantics over words.** A *word* is an infinite sequence $\sigma = A_0 A_1 A_2 \ldots$ of sets $A_i \subseteq AP$, that is, $\sigma \in (2^{AP})^\omega$. Write $\sigma[i] = A_i$ and $\sigma^i = A_i A_{i+1} \ldots$ for the suffix from position $i$. The relation $\sigma \models \varphi$ is defined by induction on $\varphi$:

- $\sigma \models \mathsf{true}$ always,
- $\sigma \models p$ iff $p \in \sigma[0]$,
- $\sigma \models \neg\varphi$ iff not $\sigma \models \varphi$,
- $\sigma \models \varphi \wedge \psi$ iff $\sigma \models \varphi$ and $\sigma \models \psi$,
- $\sigma \models \mathsf{X}\,\varphi$ iff $\sigma^1 \models \varphi$,
- $\sigma \models \varphi\ \mathsf{U}\ \psi$ iff there is $j \ge 0$ with $\sigma^j \models \psi$, and $\sigma^i \models \varphi$ for each $0 \le i < j$.

So $\sigma \models \mathsf{F}\varphi$ iff $\sigma^j \models \varphi$ for some $j$, and $\sigma \models \mathsf{G}\varphi$ iff $\sigma^j \models \varphi$ for each $j$. The set of models of $\varphi$ is $\mathit{Words}(\varphi) = \{\sigma \in (2^{AP})^\omega : \sigma \models \varphi\}$.

**Semantics over a Kripke structure.** The trace of a path $\pi = s_0 s_1 \ldots$ is the word $L(s_0) L(s_1) \ldots$. A state $s$ satisfies $\varphi$, written $s \models \varphi$, if the trace of every path from $s$ is in $\mathit{Words}(\varphi)$. The structure satisfies $\varphi$, written $M \models \varphi$, if $s \models \varphi$ for each $s \in I$. Equivalently, $M \models \varphi$ iff $\mathit{Traces}(M) \subseteq \mathit{Words}(\varphi)$, where $\mathit{Traces}(M)$ is the set of traces of the paths from initial states. Deciding $M \models \varphi$ is the [LTL model checking](/ltl-model-checking/) problem, and deciding whether $\mathit{Words}(\varphi) \neq \emptyset$ is [LTL satisfiability](/ltl-satisfiability/).

**The next-free fragment.** $\mathrm{LTL}_{\setminus \mathsf{X}}$ is the set of formulas without $\mathsf{X}$. Two words are *stutter equivalent* if there is a sequence $B_0 B_1 B_2 \ldots$ of sets with both words in $B_0^+ B_1^+ B_2^+ \cdots$, that is, they differ only in how many times each letter is repeated in a row.

**Proposition (stutter invariance).** If $\varphi \in \mathrm{LTL}_{\setminus \mathsf{X}}$ and $\sigma, \sigma'$ are stutter equivalent, then $\sigma \models \varphi$ iff $\sigma' \models \varphi$.

*Proof.* Fix the blocks: $\sigma$ and $\sigma'$ cut into consecutive non-empty finite blocks, and block $k$ of each is a repetition of $B_k$. If position $i$ is in block $k$ of $\sigma$ and $i'$ is in block $k$ of $\sigma'$, then $\sigma^i$ and $\sigma'^{i'}$ are both in $B_k^+ B_{k+1}^+ \cdots$, so they are stutter equivalent too. We show the claim for all stutter equivalent pairs at once, by induction on $\varphi$. For $p$, both words start with $B_0$. The cases $\neg$ and $\wedge$ follow from the induction hypothesis. Let $\sigma \models \varphi\ \mathsf{U}\ \psi$ with witness $j$, and let $j$ be in block $k$ of $\sigma$. Take $j'$ the first position of block $k$ in $\sigma'$. Then $\sigma^j$ and $\sigma'^{j'}$ are stutter equivalent, so $\sigma'^{j'} \models \psi$ by the hypothesis for $\psi$. Each $i' < j'$ is in a block $k' < k$ of $\sigma'$. Let $i$ be the first position of block $k'$ in $\sigma$. Then $i < j$, so $\sigma^i \models \varphi$, and $\sigma'^{i'} \models \varphi$ by the hypothesis for $\varphi$. So $\sigma' \models \varphi\ \mathsf{U}\ \psi$. The other direction is the same with the roles swapped. $\blacksquare$

The converse also holds: Peled and Wilke (1997) proved that every LTL formula whose set of models is closed under stutter equivalence is equivalent to a formula without $\mathsf{X}$. This is why [partial-order reduction](/partial-order-reduction/) is sound for $\mathrm{LTL}_{\setminus \mathsf{X}}$ and not for full LTL: the reduced graph keeps the traces only up to stuttering.

## Examples and non-examples

**Evaluation on a lasso word.** Let $AP = \{p, q\}$ and $\sigma = \emptyset\ \{p\}\ (\{p,q\}\ \emptyset)^\omega$. The word has four distinct positions: 0, 1, 2 and 3, and position 3 is followed by position 2 again. The truth value of each formula at each position, where T is true and F is false:

| Formula | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| $p$ | F | T | T | F |
| $q$ | F | F | T | F |
| $\mathsf{X}\, p$ | T | T | F | T |
| $p\ \mathsf{U}\ q$ | F | T | T | F |
| $q\ \mathsf{R}\ p$ | F | T | T | F |
| $\mathsf{F}\, q$ | T | T | T | T |
| $\mathsf{G}\, p$ | F | F | F | F |
| $\mathsf{F}\mathsf{G}\, p$ | F | F | F | F |
| $\mathsf{G}\mathsf{F}\, q$ | T | T | T | T |
| $\mathsf{G}(p \to \mathsf{F} q)$ | T | T | T | T |

So $\sigma \models \mathsf{G}\mathsf{F}\, q$ and $\sigma \not\models \mathsf{F}\mathsf{G}\, p$: $q$ comes back forever, but $p$ is false again at every odd position from 3 on. The formula $p\ \mathsf{U}\ q$ is false at 0 because $p$ is false there and $q$ has not come yet.

**Typical properties.** These are the common shapes; the [property specification patterns](/predicate-specification-patterns/) collect them.

- $\mathsf{G}\, \neg(c_1 \wedge c_2)$: mutual exclusion, a [safety property](/safety-property/).
- $\mathsf{G}(\mathit{req} \to \mathsf{F}\, \mathit{grant})$: each request is answered, a response property.
- $\mathsf{G}\mathsf{F}\, \mathit{enabled} \to \mathsf{G}\mathsf{F}\, \mathit{taken}$: strong [fairness](/fairness/) of one transition. LTL can state fairness as a hypothesis inside the formula; CTL cannot.
- $\mathsf{F}\mathsf{G}\, \mathit{stable}$: the system settles, a [liveness property](/liveness-property/).

**A structure that satisfies neither $\varphi$ nor $\neg\varphi$.** Let $M$ have an initial state $s_0$ with two successors $s_1$ and $s_2$, each with a self-loop, and let $p$ hold only in $s_1$. The path $s_0 s_1 s_1 \ldots$ satisfies $\mathsf{F}\, p$ and the path $s_0 s_2 s_2 \ldots$ does not. So $M \not\models \mathsf{F}\, p$ and $M \not\models \neg \mathsf{F}\, p$. For words, exactly one of $\varphi$ and $\neg \varphi$ holds; for structures, this is false, because $\models$ quantifies over all paths. This is why a model checker searches for one path that satisfies $\neg\varphi$.

**Non-example: counting.** The property "$p$ holds at every even position" (and anything at odd positions) is not expressible in LTL (Wolper 1983). It is $\omega$-regular: a two-state [Büchi automaton](/buchi-automaton/) accepts it. LTL has the expressive power of first-order logic over $(\mathbb{N}, <)$ (Kamp 1968, and Gabbay, Pnueli, Shelah and Stavi 1980), which is strictly less than the $\omega$-regular languages.

**Non-example: branching.** "From every reachable state, a reset state is reachable", the CTL formula $\mathsf{AG}\,\mathsf{EF}\, \mathit{reset}$, is not expressible in LTL. An LTL formula holds in $M$ iff it holds for the set of traces of $M$, and two structures can have the same traces but differ on $\mathsf{AG}\,\mathsf{EF}$. In the other direction, $\mathsf{F}\mathsf{G}\, p$ has no CTL equivalent. Both logics are fragments of [CTL*](/ctl-star/).

**Non-example: the next operator under stuttering.** $\mathsf{X}\, p$ holds on $\emptyset\, \{p\}^\omega$ and fails on $\emptyset\, \emptyset\, \{p\}^\omega$, but the two words are stutter equivalent. So $\mathsf{X}\, p$ is not stutter invariant, and by the theorem of Peled and Wilke it has no equivalent in $\mathrm{LTL}_{\setminus \mathsf{X}}$.

## Related definitions

- [Kripke structure](/kripke-structure/): the models over which formulas are evaluated, and their traces.
- [Temporal logic](/temporal-logic/): the family; [computation tree logic](/computation-tree-logic/) is its branching-time member, and [CTL*](/ctl-star/) contains both CTL and LTL.
- [Büchi automaton](/buchi-automaton/): every LTL formula has a Büchi automaton of size $2^{O(|\varphi|)}$ with the same models; see [LTL to Büchi automaton translation](/ltl-to-buchi-translation/).
- [LTL model checking](/ltl-model-checking/) and [LTL satisfiability](/ltl-satisfiability/): the two decision problems; both are [PSPACE](/pspace/)-complete, see [PSPACE-completeness of LTL model checking](/ltl-model-checking-pspace-completeness/).
- [Safety property](/safety-property/) and [liveness property](/liveness-property/): every LTL property is the intersection of a safety and a liveness property.
- [Stuttering equivalence](/stuttering-equivalence/): the equivalence on structures that preserves $\mathrm{LTL}_{\setminus \mathsf{X}}$.
- [Vacuity checking](/vacuity-checking/): tests whether a satisfied formula holds for a trivial reason.

## References
