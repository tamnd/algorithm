---
tag: 8RADX1
kind: definition
slug: safety-property
name: Safety property
aliases:
- Invariant property
- Safety
area: logic-and-constraints/model-checking
level: intro
summary: A property stating that nothing bad happens. Each violation has a finite bad prefix, and the safety properties are exactly the closed sets of infinite words.
prereqs: [kripke-structure, temporal-logic]
see_also: [liveness-property, invariant-checking, fairness, linear-temporal-logic, buchi-automaton, liveness-to-safety, bounded-model-checking, reachability-problem]
sources:
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 3, Section 3.3 (invariants, safety properties, bad prefixes and the closure of a property) and Section 3.4 (the decomposition into safety and liveness); Chapter 4 (checking regular safety properties with automata)
  - paper: doi:10.1109/TSE.1977.229904
    title: Leslie Lamport, Proving the correctness of multiprocess programs, IEEE Transactions on Software Engineering SE-3(2), 1977, pages 125 to 143
    locator: the informal split of correctness properties into safety ("something bad does not happen") and liveness
  - paper: doi:10.1016/0020-0190(85)90056-0
    title: Bowen Alpern and Fred B. Schneider, Defining liveness, Information Processing Letters 21(4), 1985, pages 181 to 185
    locator: the formal definition of safety by bad prefixes, and the characterization of safety properties as the closed sets
  - paper: "A. Prasad Sistla, Safety, liveness and fairness in temporal logic, Formal Aspects of Computing 6(5), 1994, pages 495 to 511"
    locator: syntactic characterization of the LTL formulas that express safety properties
---

A safety property says that nothing bad ever happens: two processes are never both in the critical section, a buffer never overflows, a message is never received before it is sent. Its defining feature is that each violation shows up after finitely many steps, so a finite execution prefix proves that the property fails. The simplest safety properties are invariants of states, and [invariant checking](/invariant-checking/) is the problem of verifying one. The informal name is Lamport's (1977); the formal definition below is due to Alpern and Schneider (1985).

## Definition

Fix a set $AP$ of atomic propositions and write $\Sigma = 2^{AP}$. A **linear-time property** is a set $P \subseteq \Sigma^\omega$ of infinite words. A [Kripke structure](/kripke-structure/) $M$ satisfies $P$ when the trace of each path from an initial state is in $P$. For a word $\sigma$, write $\sigma[0..i)$ for its prefix of length $i$, and $\mathit{pref}(\sigma)$ for the set of its finite prefixes.

**Bad prefix.** A finite word $u \in \Sigma^*$ is a *bad prefix* for $P$ if no infinite extension of $u$ is in $P$: $u \sigma' \notin P$ for each $\sigma' \in \Sigma^\omega$.

**Safety property.** $P$ is a **safety property** if each word outside $P$ has a bad prefix:

$$\text{for all } \sigma \notin P \text{ there is an } i \text{ such that } \sigma[0..i) \text{ is a bad prefix for } P.$$

**Invariant.** For a propositional formula $p$ over $AP$, the property $\{\sigma : \sigma[i] \models p \text{ for each } i\}$, written $\mathsf{G}\,p$ in [LTL](/linear-temporal-logic/), is an **invariant**. It is a safety property: a word outside it has a position $i$ with $\sigma[i] \not\models p$, and $\sigma[0..i+1)$ is a bad prefix.

**Closure.** The *closure* of $P$ is the set of words all of whose prefixes can still be extended into $P$:

$$\mathit{cl}(P) = \{ \sigma \in \Sigma^\omega : \mathit{pref}(\sigma) \subseteq \mathit{pref}(P) \}.$$

Always $P \subseteq \mathit{cl}(P)$.

*Lemma.* $P$ is a safety property if and only if $P = \mathit{cl}(P)$.

*Proof.* Suppose $P$ is a safety property and $\sigma \in \mathit{cl}(P)$. If $\sigma \notin P$, then some prefix of $\sigma$ is a bad prefix, so it is not a prefix of any word in $P$, which contradicts $\sigma \in \mathit{cl}(P)$. So $\mathit{cl}(P) \subseteq P$. Conversely, suppose $P = \mathit{cl}(P)$ and $\sigma \notin P$. Then $\sigma \notin \mathit{cl}(P)$, so some prefix $u$ of $\sigma$ is not in $\mathit{pref}(P)$. No extension of $u$ is in $P$, so $u$ is a bad prefix. $\blacksquare$

**Topology.** Give $\Sigma^\omega$ the metric $d(\sigma, \tau) = 2^{-n}$, where $n$ is the first position at which $\sigma$ and $\tau$ differ ($d = 0$ if they are equal). Two words are close when they share a long prefix. Then $\mathit{cl}(P)$ is the topological closure of $P$, and the lemma says: **the safety properties are exactly the closed sets** (Alpern and Schneider 1985). This is the starting point of the decomposition theorem on the [liveness property](/liveness-property/) page.

**Satisfaction by finite prefixes.** A Kripke structure $M$ satisfies a safety property $P$ if and only if no finite trace of $M$ from an initial state is a bad prefix for $P$. So a counterexample to a safety property is always a finite path, which is why a safety check is a [reachability](/reachability-problem/) question.

## Examples and non-examples

**Mutual exclusion.** In the two-process structure of the [Kripke structure](/kripke-structure/) page, "never $c_1 \wedge c_2$" is the invariant $\mathsf{G}\,\neg(c_1 \wedge c_2)$. A bad prefix is any finite trace that ends in a state labelled $c_1, c_2$. The structure satisfies it, because no such state is reachable.

**Order of events.** "No $\mathit{grant}$ before the first $\mathit{req}$" is a safety property that is not an invariant: whether a state is bad depends on the history. A bad prefix is a word with $\mathit{grant}$ at some position and no $\mathit{req}$ before or at that position. A deterministic automaton with two states (no request yet, request seen) recognizes the bad prefixes, and the property becomes an invariant of the product of $M$ with this automaton.

**Bounded response.** "Each $\mathit{req}$ is followed by $\mathit{ack}$ within 3 steps" is a safety property: a violation is visible 3 steps after the unanswered request.

**Non-example: eventually.** "Eventually $c_1$", or $\mathsf{F}\,c_1$, is not a safety property. Each finite word $u$ extends to $u\{c_1\}^\omega$, which satisfies it, so there is no bad prefix, but $\emptyset^\omega$ violates it. It is a [liveness property](/liveness-property/).

**Non-example: until.** $p\,\mathsf{U}\,q$ is neither. The word $\{p\}^\omega$ violates it, but each of its prefixes $\{p\}^i$ extends to $\{p\}^i \{q\}^\omega$, so $\{p\}^\omega \in \mathit{cl}(P) \setminus P$ and $P$ is not closed. And the prefix $\emptyset$ is bad, so it is not a liveness property either. It is the intersection of the safety property "weak until" ($p\,\mathsf{W}\,q$, which allows $p$ forever) and the liveness property $\mathsf{F}\,q$.

**Edge cases.** $\Sigma^\omega$ (true) and $\emptyset$ (false) are both safety properties. For $\emptyset$, the empty word is a bad prefix of every word.

## Related definitions

- **Liveness property.** A [liveness property](/liveness-property/) is one with no bad prefix at all: each finite word extends into it. The only property that is both safety and liveness is $\Sigma^\omega$. Every property is the intersection of a safety property and a liveness property; the proof is on the liveness page.
- **Invariant checking.** [Invariant checking](/invariant-checking/) is the problem of verifying the special case $\mathsf{G}\,p$. The general case reduces to it: for a regular safety property, build a finite automaton $A$ for its bad prefixes, and check the invariant "$A$ is not in an accepting state" on the product $M \otimes A$ (Baier and Katoen, Chapter 4). This page defines the class; the invariant checking page solves the problem.
- **Safety in LTL.** Each LTL formula in positive normal form that uses only $\mathsf{X}$, $\mathsf{G}$, $\mathsf{W}$ and $\mathsf{R}$ expresses a safety property, and each LTL-definable safety property has such a formula (Sistla 1994). Deciding whether a given LTL formula defines a safety property is PSPACE-complete (Sistla 1994).
- **Safety in CTL.** The branching-time analogue is $\mathsf{AG}\,p$ in [CTL](/computation-tree-logic/), which the [CTL labelling algorithm](/ctl-labelling-algorithm/) checks in linear time.
- **Fairness.** Suppose each finite path of $M$ extends to a [fair](/fairness/) path (the fairness assumption is then called *realizable*). Then $M$ satisfies a safety property on its fair paths if and only if it satisfies it on all its paths, because a bad prefix of an unfair path is also a prefix of a fair path. So fairness matters for liveness, not for safety.
- **Liveness to safety.** The [liveness-to-safety](/liveness-to-safety/) transformation reduces a liveness check on $M$ to a safety check on a larger structure, so that safety engines such as [IC3/PDR](/ic3-pdr/) can be used.
- **Bounded model checking.** Because violations are finite, [bounded model checking](/bounded-model-checking/) is a complete method for finding them: a violation of length $k$ is found at bound $k$.

## References
