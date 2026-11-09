---
tag: WRYARR
kind: algorithm
slug: ltl-to-buchi-translation
name: LTL to Büchi automaton translation
aliases:
- LTL to automaton construction
- LTL to Buchi automaton translation
- tableau construction for LTL
area: logic-and-constraints/model-checking
level: advanced
summary: Build a Büchi automaton with 2^O(|φ|) states that accepts exactly the infinite words that satisfy an LTL formula φ, by a tableau of consistent sets of subformulas and a degeneralization step.
solves: [ltl-satisfiability, ltl-model-checking]
model: word-ram
complexity:
  vars: {n: the number of symbols of the formula, k: the number of until subformulas}
  time: {worst: O(n 4^n)}
  space: {extra: O(k 2^n)}
properties: {deterministic: true, recursive: false, output_size: "at most k 2^n states"}
history:
  year: 1983
  people: [Pierre Wolper, Moshe Y. Vardi, A. Prasad Sistla]
  note: Wolper, Vardi and Sistla gave the tableau translation of temporal logic into automata on infinite words in 1983; Vardi and Wolper made it the basis of LTL model checking in 1986.
prereqs: [linear-temporal-logic, buchi-automaton]
see_also: [ltl-model-checking, automata-theoretic-approach, nested-depth-first-search, ltl-satisfiability, on-the-fly-model-checking, language-containment]
sources:
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 5, Section 5.2 (elementary sets, the generalized Büchi automaton for an LTL formula and its correctness proof); Chapter 4, Section 4.3 (generalized Büchi automata and their degeneralization)
  - paper: doi:10.1006/inco.1994.1092
    title: Moshe Y. Vardi and Pierre Wolper, Reasoning about infinite computations, Information and Computation 115(1), 1994, pages 1 to 37
    locator: the translation of LTL (and extended temporal logics) into Büchi automata with 2^O(|φ|) states
  - paper: "Pierre Wolper, Moshe Y. Vardi and A. Prasad Sistla, Reasoning about infinite computation paths, 24th Annual Symposium on Foundations of Computer Science (FOCS 1983), IEEE"
    locator: the first tableau translation of temporal logic into automata on infinite words
  - paper: "Rob Gerth, Doron Peled, Moshe Y. Vardi and Pierre Wolper, Simple on-the-fly automatic verification of linear temporal logic, Protocol Specification, Testing and Verification XV (PSTV 1995), Chapman and Hall, pages 3 to 18"
    locator: the on-the-fly translation that builds only the reachable tableau nodes (GPVW)
  - paper: "Paul Gastin and Denis Oddoux, Fast LTL to Büchi automata translation, Computer Aided Verification (CAV 2001), Lecture Notes in Computer Science 2102, Springer"
    locator: the translation through very weak alternating automata (LTL2BA)
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: Chapter 9 (the translation of LTL into Büchi automata, in the style of GPVW)
---

The LTL to Büchi automaton translation takes a [linear temporal logic](/linear-temporal-logic/) formula $\varphi$ and builds a [Büchi automaton](/buchi-automaton/) $A_\varphi$ that accepts exactly the infinite words that satisfy $\varphi$. The states of the automaton are the *elementary sets*: the consistent guesses of which subformulas hold at the current position. Transitions check the next-step meaning of $\mathsf{X}$ and $\mathsf{U}$, and one acceptance set per until formula forbids postponing its right operand forever. The result is a generalized Büchi automaton with at most $2^{|\varphi|}$ states, and an ordinary Büchi automaton with at most $|\varphi| \cdot 2^{|\varphi|}$ states after degeneralization. It is the first step of [LTL model checking](/ltl-model-checking/) and of the decision procedure for [LTL satisfiability](/ltl-satisfiability/).

## In plain words

An automaton reads a word one letter at a time and keeps a small memory, its state. To check a formula like "$p$ until $q$" on an infinite word, the automaton does not know the future. In each state it guesses which parts of the formula are true from here on, and it checks each guess one step later.

If it guesses "$p$ until $q$ is true now" and $q$ is false now, then $p$ must be true now and the same guess must hold at the next letter. The danger is that the automaton keeps saying "$q$ comes later" forever. The acceptance rule stops this: a run counts only if, again and again, the promise is kept. There are only so many guesses, one true or false for each part of the formula, so the automaton has at most two to the power of the formula size states.

## The problem

The input is an LTL formula $\varphi$ over atomic propositions $AP_\varphi$, of size $n = |\varphi|$. The output is a Büchi automaton $A = (Q, Q_0, \to, \lambda, F)$ whose states are labelled with letters: a run $q_0 q_1 \ldots$ with $q_0 \in Q_0$ and $q_i \to q_{i+1}$ reads the word $\sigma$ when $\sigma[i] \cap AP_\varphi = \lambda(q_i)$ for each $i$, and it is accepting when it visits $F$ infinitely often. The requirement is

$$L(A) = \mathit{Words}(\varphi) = \{\sigma \in (2^{AP})^\omega : \sigma \models \varphi\}.$$

An intermediate result is a *generalized* Büchi automaton (GBA), whose acceptance condition is a list $F_0, \ldots, F_{k-1}$ of sets: an accepting run visits each $F_i$ infinitely often.

## The algorithm

First rewrite $\varphi$ with only $\mathsf{true}$, atomic propositions, $\neg$, $\wedge$, $\mathsf{X}$ and $\mathsf{U}$ (for example $\mathsf{F}\psi = \mathsf{true}\ \mathsf{U}\ \psi$ and $\mathsf{G}\psi = \neg\mathsf{F}\neg\psi$), and remove double negations. The *closure* $\mathit{cl}(\varphi)$ is the set of subformulas of the result. A set $B \subseteq \mathit{cl}(\varphi)$ is *elementary* if it is the set of subformulas that are true at some position of some word, as far as one position can tell:

- $\mathsf{true} \in B$; $\neg\psi \in B$ iff $\psi \notin B$; $\psi_1 \wedge \psi_2 \in B$ iff $\psi_1 \in B$ and $\psi_2 \in B$;
- if $\psi_2 \in B$ then $\psi_1\, \mathsf{U}\, \psi_2 \in B$; if $\psi_1\, \mathsf{U}\, \psi_2 \in B$ and $\psi_2 \notin B$ then $\psi_1 \in B$.

An elementary set is fixed by its choice of the *base* subformulas, those of the forms $p$, $\mathsf{X}\psi$ and $\psi_1\, \mathsf{U}\, \psi_2$, so there are at most $2^e$ of them, where $e \le n$ is the number of base subformulas.

```pseudo id=main
LTL-TO-GBA(φ)
L1  cl ← the subformulas of φ, rewritten with true, p, ¬, ∧, X and U
L2  Q ← the elementary subsets of cl
L3  Q₀ ← {B ∈ Q : φ ∈ B}
L4  for each B ∈ Q do
L5      for each C ∈ Q do
L6          if (for each Xψ ∈ cl: Xψ ∈ B ⇔ ψ ∈ C) and
L7             (for each ψ₁ U ψ₂ ∈ cl: ψ₁ U ψ₂ ∈ B ⇔ ψ₂ ∈ B or (ψ₁ ∈ B and ψ₁ U ψ₂ ∈ C)) then
L8              add the transition B → C
L9  for each ψ₁ U ψ₂ ∈ cl: F_(ψ₁ U ψ₂) ← {B ∈ Q : ψ₁ U ψ₂ ∉ B or ψ₂ ∈ B}
L10 return (Q, Q₀, →, λ(B) = B ∩ AP, the list of the sets F_(ψ₁ U ψ₂))

DEGENERALIZE(Q, Q₀, →, λ, F₀, …, F_(k−1))           ▷ if k = 0, set k ← 1 and F₀ ← Q
L11 Q' ← Q × {0, …, k − 1};  Q'₀ ← Q₀ × {0}
L12 (q, i) →' (r, j) iff q → r, where j = (i + 1) mod k if q ∈ F_i, and j = i otherwise
L13 return (Q', Q'₀, →', λ'(q, i) = λ(q), F' = F₀ × {0})
```

Line L7 is the expansion law $\psi_1\, \mathsf{U}\, \psi_2 \equiv \psi_2 \vee (\psi_1 \wedge \mathsf{X}(\psi_1\, \mathsf{U}\, \psi_2))$, and line L9 makes sure that a run that keeps $\psi_1\, \mathsf{U}\, \psi_2$ in its states also meets $\psi_2$ again and again. The counter of DEGENERALIZE waits for $F_0$, then for $F_1$, and so on; it passes from $k-1$ back to $0$ only after it has seen each set once.

## Example

For $\varphi = p\ \mathsf{U}\ q$ the base subformulas are $p$, $q$ and $p\, \mathsf{U}\, q$, so there are at most $8$ candidate sets. Three are not elementary: $\{q\}$ and $\{p, q\}$ without the until (since $q$ forces it), and $\{p\,\mathsf{U}\,q\}$ alone (since the until without $q$ forces $p$). The 5 states, written as the base formulas they contain, are:

| State $B$ | Letter $\lambda(B)$ | Initial | In $F_{p\,\mathsf{U}\,q}$ | Successors |
|---|---|---|---|---|
| $\emptyset$ | $\emptyset$ | no | yes | all 5 |
| $\{p\}$ | $\{p\}$ | no | yes | $\emptyset$, $\{p\}$ |
| $\{p,\ p\,\mathsf{U}\,q\}$ | $\{p\}$ | yes | no | $\{p,\ p\,\mathsf{U}\,q\}$, $\{q,\ p\,\mathsf{U}\,q\}$, $\{p, q,\ p\,\mathsf{U}\,q\}$ |
| $\{q,\ p\,\mathsf{U}\,q\}$ | $\{q\}$ | yes | yes | all 5 |
| $\{p, q,\ p\,\mathsf{U}\,q\}$ | $\{p, q\}$ | yes | yes | all 5 |

There are 20 transitions. The state $\{p\}$ asserts that $p\,\mathsf{U}\,q$ is false while $p$ is true, so by line L7 its successor must also make the until false. The state $\{p,\ p\,\mathsf{U}\,q\}$ is the only one outside $F$: a run that stays in it forever reads $\{p\}^\omega$, which does not satisfy $p\,\mathsf{U}\,q$, and the acceptance condition rejects it. The word $\{p\}\{p\}\{q\}\emptyset^\omega$ has the accepting run $\{p, p\mathsf{U}q\}\ \{p, p\mathsf{U}q\}\ \{q, p\mathsf{U}q\}\ \emptyset^\omega$. With one acceptance set, degeneralization keeps 5 states.

Sizes for some other formulas, with $e$ the number of base subformulas after the rewriting:

| $\varphi$ | $e$ | GBA states | initial | transitions | acceptance sets $k$ | Büchi states |
|---|---|---|---|---|---|---|
| $\mathsf{X}\, p$ | 2 | 4 | 2 | 8 | 0 | 4 |
| $\mathsf{F}\, p$ | 2 | 3 | 2 | 6 | 1 | 3 |
| $\mathsf{G}\, p$ | 2 | 3 | 1 | 6 | 1 | 3 |
| $\mathsf{G}\mathsf{F}\, p$ | 3 | 5 | 2 | 10 | 2 | 10 |
| $\mathsf{G}(p \to \mathsf{F}\, q)$ | 4 | 11 | 5 | 44 | 2 | 22 |
| $p\ \mathsf{U}\ (q\ \mathsf{U}\ r)$ | 5 | 12 | 8 | 96 | 2 | 24 |
| $\mathsf{G}\mathsf{F}\, p \wedge \mathsf{G}\mathsf{F}\, q$ | 6 | 25 | 4 | 100 | 4 | 100 |

The construction is not small in practice: a hand-made Büchi automaton for $\mathsf{G}\mathsf{F}\, p$ has 2 states, while the tableau gives 10. Tools therefore use the on-the-fly and simplifying translations listed below.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). For one direction, let $\sigma \models \varphi$ and let $B_i$ be the set of formulas of the closure that hold on the suffix $\sigma^i$. Each $B_i$ is elementary, the sequence respects lines L6 and L7 by the semantics of $\mathsf{X}$ and the expansion law of $\mathsf{U}$, $\varphi \in B_0$, and the sequence meets each $F_{\psi_1 \mathsf{U} \psi_2}$ infinitely often, because a true until is fulfilled at some later position. For the other direction, take an accepting run $B_0 B_1 \ldots$ on $\sigma$ and show by induction on $\psi$ that $\psi \in B_i$ iff $\sigma^i \models \psi$ for every $i$. The only hard case is an until that the run keeps in its states while $\psi_2$ never comes; line L9 and the acceptance condition rule this out. Degeneralization keeps the language because the counter of line L12 returns to 0 infinitely often iff the run visits each $F_i$ infinitely often.

## Complexity

The GBA has at most $2^e \le 2^n$ states and at most $4^e$ transitions; lines L4 to L8 test each pair of states in $O(n)$ time, so LTL-TO-GBA takes $O(n \cdot 4^n)$ time. There are $k \le n$ acceptance sets, one per until subformula, and DEGENERALIZE multiplies the number of states and transitions by $\max(k, 1)$, so the Büchi automaton has at most $n \cdot 2^n = 2^{O(n)}$ states.

The exponential is necessary in the worst case. Let $\varphi_m = \bigwedge_{i=1}^{m} (p_i \leftrightarrow (\neg q\ \mathsf{U}\ (q \wedge p_i)))$, of size $O(m)$: the values of $p_1, \ldots, p_m$ at position 0 must equal their values at the first $q$, which must exist. Every Büchi automaton for $\varphi_m$ has at least $2^m$ states. For each valuation $v \subseteq \{p_1, \ldots, p_m\}$, take an accepting run $\rho_v$ on the word $w_v = v\ (v \cup \{q\})\ \emptyset^\omega$ and let $s_v$ be its state at position 1. If $s_v = s_{v'}$ with $v \neq v'$, then the first state of $\rho_v$ followed by the rest of $\rho_{v'}$ is an accepting run on $v\ (v' \cup \{q\})\ \emptyset^\omega$, which does not satisfy $\varphi_m$. So the $s_v$ are pairwise different.

## Properties

- **Exact.** $L(A_\varphi) = \mathit{Words}(\varphi)$, for every LTL formula.
- **Non-deterministic.** Some LTL formulas, such as $\mathsf{F}\mathsf{G}\, p$, have no deterministic Büchi automaton at all; the tableau automaton is non-deterministic, and determinization needs stronger acceptance conditions (Rabin or parity) and more states.
- **Not minimal.** The automaton has many redundant states, as the table shows. Its size is a bound, not a typical value.
- **Global.** This version builds all elementary sets, including those that no run from an initial state reaches. The on-the-fly versions build only the reachable part.
- **Unambiguous.** Each word has at most one accepting run: the run must be $B_i = \{\psi : \sigma^i \models \psi\}$ by the correctness proof.

## Variants and improvements

- **GPVW** (Gerth, Peled, Vardi and Wolper 1995). Build the nodes on demand by expanding formulas into disjunctive normal form with the expansion laws, starting from $\varphi$. Only the reachable states appear, and the result is usually much smaller. It is the translation in Chapter 9 of Clarke, Grumberg and Peled, and the basis of the early SPIN translator.
- **Through alternating automata.** Translate $\varphi$ into a very weak alternating automaton with $O(|\varphi|)$ states, then to a generalized Büchi automaton, then simplify at each stage (Gastin and Oddoux 2001, LTL2BA). This is fast and gives small automata.
- **Transition-based acceptance.** Put the acceptance sets on transitions instead of states. This often saves a factor, and is the internal form of the Spot library.
- **Simplification.** Rewrite the formula first, then remove states by simulation relations and merge equivalent states (Somenzi and Bloem 2000, Etessami and Holzmann 2000).
- **Use without degeneralization.** An SCC-based emptiness check can work on the generalized automaton directly, which avoids the factor $k$; [nested depth-first search](/nested-depth-first-search/) needs the degeneralized automaton.

## When to use it

Use this tableau when you need a short and provably correct translation, for teaching, for proofs of upper bounds such as the [PSPACE upper bound](/ltl-model-checking-pspace-completeness/), or as a reference to test a faster translator against. For verification tools, use an on-the-fly or alternating-automata translator, or a library such as Spot, which give automata that are often an order of magnitude smaller; the product with the system is what costs time, and it grows with the automaton. In symbolic model checking, the tableau is encoded with one Boolean variable per base subformula, and its size is then linear in $|\varphi|$.

## Pitfalls

- **Forgetting the acceptance sets.** Without line L9, the automaton for $p\,\mathsf{U}\,q$ accepts $\{p\}^\omega$, by staying in $\{p,\ p\,\mathsf{U}\,q\}$. The transitions alone only check the expansion law, which $\mathsf{G}\, p$ also satisfies.
- **Wrong degeneralization.** Taking $F = \bigcup_i F_i$ instead of the counter accepts runs that visit only one set. For $\mathsf{G}\mathsf{F}\, p \wedge \mathsf{G}\mathsf{F}\, q$ it accepts $\{p\}^\omega$.
- **No acceptance set.** If $\varphi$ has no until, the GBA has $k = 0$ and every infinite run accepts; DEGENERALIZE must then make every state accepting, not none.
- **Letter labels.** In this state-labelled form, a state reads exactly the letter $B \cap AP_\varphi$. A product with a system must compare the state label of the system restricted to $AP_\varphi$, not the full label.
- **Translating $\varphi$ instead of $\neg\varphi$.** Model checking needs the automaton for the negation, and complementing a Büchi automaton afterwards is far more expensive than negating the formula first.

## Implementations

## History

Wolper, Vardi and Sistla (1983) gave the tableau translation of temporal logic into Büchi automata, and Vardi and Wolper (1986) used it for model checking: the [automata-theoretic approach](/automata-theoretic-approach/). The journal paper of Vardi and Wolper (1994) gives the translation in full. Lichtenstein and Pnueli (1985) used the same tableau with SCC conditions for model checking. Gerth, Peled, Vardi and Wolper (1995) made the construction on the fly, and since then many translators have been built to reduce the size of the automaton, among them LTL2BA by Gastin and Oddoux (2001) and the Spot library by Duret-Lutz and others.

## References
