---
tag: 31H0MW
kind: definition
slug: modal-mu-calculus
name: Modal mu-calculus
aliases:
- Mu-calculus
- Propositional mu-calculus
- Modal μ-calculus
- L-mu
area: logic-and-constraints/model-checking
level: advanced
summary: Modal logic with least and greatest fixed-point operators. It contains CTL, LTL and CTL*, it cannot tell bisimilar states apart, and its model checking is equivalent to solving parity games.
prereqs: [kripke-structure, fixed-point, computation-tree-logic]
see_also: [mu-calculus-model-checking, emerson-lei-algorithm, knaster-tarski-theorem, computation-tree-logic, ctl-star, linear-temporal-logic, parity-game, bisimulation]
sources:
  - paper: doi:10.1016/0304-3975(82)90125-6
    title: Dexter Kozen, Results on the propositional μ-calculus, Theoretical Computer Science 27(3), 1983, pages 333 to 354
    locator: the syntax with the positivity condition, the semantics by least and greatest fixed points, and the axiom system
  - paper: "E. Allen Emerson and Chin-Laung Lei, Efficient model checking in fragments of the propositional mu-calculus, Proceedings of the First IEEE Symposium on Logic in Computer Science (LICS 1986), pages 267 to 278"
    locator: the notion of alternation depth, and the expression of CTL and of CTL with fairness in the mu-calculus
  - book: "Julian Bradfield and Colin Stirling, Modal mu-calculi, in Patrick Blackburn, Johan van Benthem and Frank Wolter (eds.), Handbook of Modal Logic, Elsevier, 2007"
    locator: Chapter 12 (syntax and semantics, approximants, alternation, the game view, and expressiveness)
  - paper: "Mads Dam, CTL* and ECTL* as fragments of the modal μ-calculus, Theoretical Computer Science 126(1), 1994, pages 77 to 96"
    locator: the translation of CTL* formulas into the mu-calculus
  - paper: "Julian C. Bradfield, The modal mu-calculus alternation hierarchy is strict, Theoretical Computer Science 195(2), 1998, pages 133 to 153"
    locator: the main theorem (for each n there is a formula that is not equivalent to any formula of alternation depth n)
  - paper: "David Janin and Igor Walukiewicz, On the expressive completeness of the propositional mu-calculus with respect to monadic second order logic, CONCUR 1996, Lecture Notes in Computer Science 1119, Springer, pages 263 to 277"
    locator: the main theorem (the mu-calculus expresses exactly the properties of monadic second-order logic that are invariant under bisimulation)
  - paper: "E. Allen Emerson and Charanjit S. Jutla, The complexity of tree automata and logics of programs, 29th IEEE Symposium on Foundations of Computer Science (FOCS 1988), pages 328 to 337"
    locator: the exponential-time decision procedure for satisfiability of the mu-calculus, through automata on infinite trees
---

The modal mu-calculus is propositional modal logic with two extra operators: $\mu Z.\, \varphi$, the least fixed point, and $\nu Z.\, \varphi$, the greatest fixed point, of the function that $\varphi$ defines on sets of states. Kozen introduced it in 1983. It is a small logic with a simple semantics, and yet it contains [CTL](/computation-tree-logic/), [LTL](/linear-temporal-logic/) and [CTL*](/ctl-star/). For this reason it is the common target language of many model checkers and the standard yardstick for branching-time logics. Its formulas do not distinguish [bisimilar](/bisimulation/) states, and its model checking problem is polynomial-time equivalent to solving [parity games](/parity-game/). This page defines the logic; [mu-calculus model checking](/mu-calculus-model-checking/) is the problem of evaluating it, and the [Emerson-Lei algorithm](/emerson-lei-algorithm/) is an algorithm for that problem.

## Definition

**Syntax.** Fix a set of atomic propositions $AP$ and a set of variables $\mathit{Var}$. Formulas in *positive normal form* are given by

$$\varphi ::= \mathit{true} \mid \mathit{false} \mid p \mid \neg p \mid Z \mid \varphi \wedge \varphi \mid \varphi \vee \varphi \mid \Diamond \varphi \mid \Box \varphi \mid \mu Z.\, \varphi \mid \nu Z.\, \varphi$$

with $p \in AP$ and $Z \in \mathit{Var}$. Here $\Diamond \varphi$ ("some successor satisfies $\varphi$") is also written $\langle\cdot\rangle\varphi$ or $\mathsf{EX}\,\varphi$, and $\Box \varphi$ ("each successor satisfies $\varphi$") is also written $[\cdot]\varphi$ or $\mathsf{AX}\,\varphi$. The operators $\mu Z$ and $\nu Z$ bind $Z$; a formula is *closed* if it has no free variable. Negation is applied only to atomic propositions, so every variable occurs positively.

Kozen's original syntax allows negation everywhere, with the condition that each bound variable occurs under an even number of negations. Such a formula has an equivalent in positive normal form of the same size, by pushing negations inward with $\neg \Diamond \varphi = \Box \neg \varphi$, $\neg \mu Z.\, \varphi = \nu Z.\, \neg \varphi[\neg Z / Z]$ and their duals. By renaming, we may assume that each variable is bound at most once.

**Semantics.** Let $M = (S, I, R, L)$ be a [Kripke structure](/kripke-structure/) and $\rho : \mathit{Var} \to 2^S$ a valuation of the variables. The set $[\![\varphi]\!]_\rho \subseteq S$ is defined by

- $[\![\mathit{true}]\!]_\rho = S$, $[\![\mathit{false}]\!]_\rho = \emptyset$, $[\![p]\!]_\rho = \{s : p \in L(s)\}$, $[\![\neg p]\!]_\rho = S \setminus [\![p]\!]_\rho$, $[\![Z]\!]_\rho = \rho(Z)$;
- $[\![\varphi \wedge \psi]\!]_\rho = [\![\varphi]\!]_\rho \cap [\![\psi]\!]_\rho$ and $[\![\varphi \vee \psi]\!]_\rho = [\![\varphi]\!]_\rho \cup [\![\psi]\!]_\rho$;
- $[\![\Diamond \varphi]\!]_\rho = \{s : R(s) \cap [\![\varphi]\!]_\rho \ne \emptyset\}$ and $[\![\Box \varphi]\!]_\rho = \{s : R(s) \subseteq [\![\varphi]\!]_\rho\}$;
- $[\![\mu Z.\, \varphi]\!]_\rho = \bigcap \{T \subseteq S : [\![\varphi]\!]_{\rho[Z \mapsto T]} \subseteq T\}$;
- $[\![\nu Z.\, \varphi]\!]_\rho = \bigcup \{T \subseteq S : T \subseteq [\![\varphi]\!]_{\rho[Z \mapsto T]}\}$.

A simple induction shows that in positive normal form, $[\![\varphi]\!]_\rho$ is monotone in each $\rho(Z)$. So $T \mapsto [\![\varphi]\!]_{\rho[Z \mapsto T]}$ is a monotone map on $(2^S, \subseteq)$, and by the [Knaster-Tarski theorem](/knaster-tarski-theorem/) the two sets above are its least and its greatest [fixed point](/fixed-point/). For a closed formula the valuation does not matter, and we write $M, s \models \varphi$ when $s \in [\![\varphi]\!]$, and $M \models \varphi$ when $I \subseteq [\![\varphi]\!]$. On a finite structure the fixed points are the limits of the iterations from $\emptyset$ and from $S$, which take at most $|S|$ steps each.

**Alternation depth.** The *alternation depth* $\mathit{ad}(\varphi)$ is the largest number of sign blocks on a chain of nested fixed points $\sigma_1 Z_1.\, (\ldots \sigma_2 Z_2.\, (\ldots \sigma_j Z_j.\, \ldots))$, where a new block starts whenever $\sigma_{i+1} \ne \sigma_i$. So $\mathit{ad}(\varphi) = 0$ when $\varphi$ has no fixed point, $\mathit{ad}(\varphi) = 1$ when $\varphi$ is *alternation-free*, and $\nu X.\, \mu Y.\, \ldots$ with $X$ free in the inner part has depth $2$. Refined definitions count a change of sign only when the inner fixed point has the outer variable free (Emerson and Lei 1986), and so give a smaller number for formulas with nested closed subformulas. The alternation depth, not the size, governs the cost of model checking.

## Examples and non-examples

**CTL.** Each CTL operator is a fixed point of a one-step formula. On structures with a total transition relation:

| CTL | mu-calculus |
|---|---|
| $\mathsf{EX}\,p$, $\mathsf{AX}\,p$ | $\Diamond p$, $\Box p$ |
| $\mathsf{E}[p\,\mathsf{U}\,q]$ | $\mu Z.\, q \vee (p \wedge \Diamond Z)$ |
| $\mathsf{A}[p\,\mathsf{U}\,q]$ | $\mu Z.\, q \vee (p \wedge \Box Z)$ |
| $\mathsf{EF}\,p$, $\mathsf{AF}\,p$ | $\mu Z.\, p \vee \Diamond Z$, $\mu Z.\, p \vee \Box Z$ |
| $\mathsf{EG}\,p$, $\mathsf{AG}\,p$ | $\nu Z.\, p \wedge \Diamond Z$, $\nu Z.\, p \wedge \Box Z$ |

Translating inside out gives a formula of linear size. Each fixed point in it is closed, so the formula is alternation-free in the refined sense. In the simple count, a closed subformula of the other sign still adds a block, as in $\mathsf{AG}\,\mathsf{EF}\,p = \nu X.\, (\mu Y.\, p \vee \Diamond Y) \wedge \Box X$, but an algorithm can evaluate a closed subformula once and then treat it as an atomic proposition. The proofs of the $\mathsf{EU}$ and $\mathsf{EG}$ rows are on the [computation tree logic](/computation-tree-logic/) page.

**Infinitely often.** $\mathsf{E}\,\mathsf{G}\mathsf{F}\,p$, "some path visits $p$ infinitely often", is

$$\nu X.\, \mu Y.\, \big((p \wedge \Diamond X) \vee \Diamond Y\big),$$

of alternation depth $2$. The inner part says "there is a finite path to a $p$-state that has a successor in $X$", and the outer $\nu$ asks for the largest set $X$ from which this can be repeated forever. On the structure with edges $0 \to 1$, $0 \to 2$, $1 \to 0$, $2 \to 3$, $3 \to 3$ and $p$ in states $1$ and $2$, the formula holds exactly in $\{0, 1\}$: the path $0\,1\,0\,1 \ldots$ meets $p$ infinitely often, while from $2$ the only path is $2\,3\,3\,3 \ldots$. CTL cannot express this property, and it is the standard example of a property that needs alternation.

**Fairness.** With a justice set $J$, the formula $\nu Z.\, p \wedge \Diamond\, \mu Y.\, \big((Z \wedge J) \vee (p \wedge \Diamond Y)\big)$ says "some path keeps $p$ forever and visits $J$ infinitely often". This is fair $\mathsf{EG}$ from the [fairness](/fairness/) page, and the [Emerson-Lei algorithm](/emerson-lei-algorithm/) page proves the formula correct.

**Even positions.** $\nu Z.\, p \wedge \Box\Box Z$ says "on every path, $p$ holds at positions $0, 2, 4, \ldots$". On the two-state cycle $0 \to 1 \to 0$ with $p$ only in $0$, it holds in $0$ and fails in $1$, while $\mathsf{AG}\,p$ fails in both. Wolper (1983) showed that "$p$ holds at every even position" is not expressible in LTL. On structures that are single paths, CTL* says no more than LTL, so it is not in CTL* either.

**Non-example: a variable under negation.** $\mu Z.\, \neg Z$ and $\mu Z.\, p \vee \neg \Diamond Z$ are not formulas. The map $T \mapsto S \setminus T$ is not monotone and has no fixed point when $S \ne \emptyset$.

**Non-example: counting.** "The state has at least two successors" is not expressible. Let $a$ have two successors $b_1$ and $b_2$, and let $a'$ have one successor $b'$, where $b_1$, $b_2$ and $b'$ have no labels and a self-loop each. The relation $\{(a, a'), (b_1, b'), (b_2, b')\}$ is a bisimulation, and every mu-calculus formula has the same truth value at bisimilar states, by induction on the formula. So no formula holds at $a$ and fails at $a'$.

## Related definitions

- **Hennessy-Milner logic.** The fragment without fixed points. On image-finite structures, two states satisfy the same such formulas if and only if they are [bisimilar](/bisimulation/).
- **Temporal logics.** [CTL](/computation-tree-logic/) embeds in the alternation-free fragment, as above. [LTL](/linear-temporal-logic/) and [CTL*](/ctl-star/) embed too (Dam 1994), but the translation can be exponential and needs alternation, as the $\mathsf{E}\,\mathsf{G}\mathsf{F}\,p$ example shows.
- **Alternation hierarchy.** The classes of formulas of alternation depth at most $n$ form a strict hierarchy: for each $n$ there is a property that needs depth $n + 1$ (Bradfield 1998, and independently Lenzi 1996).
- **Monadic second-order logic.** Over Kripke structures, the mu-calculus expresses exactly the properties of monadic second-order logic that cannot tell bisimilar structures apart (Janin and Walukiewicz 1996).
- **Parity games and parity automata.** Evaluating a formula on a structure is the same as solving a [parity game](/parity-game/) whose priorities come from the alternation of the fixed points; see [mu-calculus model checking](/mu-calculus-model-checking/).
- **Satisfiability.** Deciding whether a formula has a model is EXPTIME-complete. Emerson and Jutla (1988) gave the upper bound through automata on infinite trees, and the lower bound comes from propositional dynamic logic, a fragment. Every satisfiable formula has a finite model.
- **Axioms.** Kozen proposed an axiom system in 1983, with the induction rule "if $\varphi[\psi/Z] \to \psi$ then $\mu Z.\, \varphi \to \psi$". Walukiewicz proved it complete in 2000.
- **Fixed points.** The semantics rests on the [fixed point](/fixed-point/) concept and on the [Knaster-Tarski theorem](/knaster-tarski-theorem/).

## References
