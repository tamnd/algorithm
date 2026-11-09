---
tag: A1YY3R
kind: concept
slug: predicate-specification-patterns
name: Property specification patterns
aliases:
- Specification patterns
- Dwyer patterns
- property patterns
area: logic-and-constraints/model-checking
level: intro
summary: A catalogue of the temporal properties that occur again and again in practice, such as absence, response and precedence, each with a scope and ready-made formulas in LTL and CTL.
prereqs: [linear-temporal-logic]
see_also: [computation-tree-logic, safety-property, liveness-property, ltl-model-checking, vacuity-checking, temporal-logic]
sources:
  - paper: doi:10.1145/302405.302672
    title: Matthew B. Dwyer, George S. Avrunin and James C. Corbett, Patterns in property specifications for finite-state verification, 21st International Conference on Software Engineering (ICSE 1999), ACM, 1999, pages 411 to 420
    locator: the pattern hierarchy, the five scopes, the mappings to LTL and CTL, and the survey of 555 specifications
  - paper: "Matthew B. Dwyer, George S. Avrunin and James C. Corbett, Property specification patterns for finite-state verification, Second Workshop on Formal Methods in Software Practice (FMSP 1998), ACM"
    locator: the first version of the pattern system
  - paper: "Sascha Konrad and Betty H. C. Cheng, Real-time specification patterns, 27th International Conference on Software Engineering (ICSE 2005), ACM"
    locator: patterns with time bounds, mapped to MTL, TCTL and RTGIL
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 5, Section 5.1 (the common LTL properties of reactive systems)
---

Property specification patterns are a catalogue of the shapes of temporal property that engineers write most often, such as "$P$ never happens", "$S$ always answers $P$" and "$S$ comes before $P$". Each pattern is combined with a *scope*, the part of a run where it must hold, and comes with tested formulas in [LTL](/linear-temporal-logic/), [CTL](/computation-tree-logic/) and other logics. Dwyer, Avrunin and Corbett proposed the system in 1998 and 1999, after a survey of 555 property specifications from at least 35 sources, in which about 92% matched one of their patterns. The point is practical: a user picks a pattern and a scope instead of writing a temporal formula from scratch, which avoids the most common errors with nested until operators.

## In plain words

Most rules that people want to check fall into a few kinds. "This bad thing never happens." "This good thing happens at some point." "Every request gets an answer." "You must log in before you can buy." Writing such rules in temporal logic is easy to get wrong, in particular when the rule holds only in part of a run, such as "between start and stop".

The patterns are a phrase book. You choose the kind of rule, for example "response", and the part of the run, for example "after the system starts". The catalogue gives the correct formula. A study of hundreds of real rules found that almost all of them fit one of these kinds. This saves time, and the formulas in the catalogue have been checked by many users.

## The idea

**Patterns.** Each pattern is about one or two state formulas $P$ and $S$, called *events*. They form a small hierarchy.

- *Occurrence patterns.* **Absence**: $P$ does not occur. **Universality**: $P$ holds throughout. **Existence**: $P$ occurs. **Bounded existence**: $P$ occurs at most $k$ times.
- *Order patterns.* **Precedence**: $S$ occurs before the first $P$ ("$S$ precedes $P$"). **Response**: each $P$ is followed by an $S$ ("$S$ responds to $P$"). **Chain precedence** and **chain response**: the same with sequences of events in place of $S$ or $P$.

**Scopes.** A scope is the part of the run where the pattern must hold, given by two more events $Q$ and $R$: **global** (the whole run), **before $R$** (up to the first $R$), **after $Q$** (from the first $Q$ on), **between $Q$ and $R$** (each interval from a $Q$ to the next $R$, if that $R$ comes), and **after $Q$ until $R$** (the same, but the interval also counts if no $R$ comes). The intervals are closed on the left and open on the right.

**Mappings.** For each pair of pattern and scope, the catalogue gives a formula in several logics. Some LTL mappings, where $\varphi\ \mathsf{W}\ \psi$ is weak until, $(\varphi\ \mathsf{U}\ \psi) \vee \mathsf{G}\,\varphi$:

| Pattern | Global | Before $R$ | After $Q$ |
|---|---|---|---|
| Absence | $\mathsf{G}\, \neg P$ | $\mathsf{F} R \to (\neg P\ \mathsf{U}\ R)$ | $\mathsf{G}(Q \to \mathsf{G}\, \neg P)$ |
| Existence | $\mathsf{F}\, P$ | $\neg R\ \mathsf{W}\ (P \wedge \neg R)$ | $\mathsf{G}\, \neg Q \vee \mathsf{F}(Q \wedge \mathsf{F}\, P)$ |
| Universality | $\mathsf{G}\, P$ | $\mathsf{F} R \to (P\ \mathsf{U}\ R)$ | $\mathsf{G}(Q \to \mathsf{G}\, P)$ |
| Precedence | $\neg P\ \mathsf{W}\ S$ | $\mathsf{F} R \to (\neg P\ \mathsf{U}\ (S \vee R))$ | see below |
| Response | $\mathsf{G}(P \to \mathsf{F}\, S)$ | $\mathsf{F} R \to (P \to (\neg R\ \mathsf{U}\ (S \wedge \neg R)))\ \mathsf{U}\ R$ | $\mathsf{G}(Q \to \mathsf{G}(P \to \mathsf{F}\, S))$ |

Absence between $Q$ and $R$ is $\mathsf{G}((Q \wedge \neg R \wedge \mathsf{F} R) \to (\neg P\ \mathsf{U}\ R))$, and absence after $Q$ until $R$ is $\mathsf{G}((Q \wedge \neg R) \to (\neg P\ \mathsf{W}\ R))$.

The formulas encode some conventions that a hand-written formula often gets wrong. "Before $R$" makes no demand when $R$ never happens: absence before $R$ is vacuously true on a run without $R$. Precedence allows $S$ and the first $P$ at the same position, because the until operator only constrains the positions strictly before its right operand. In the existence pattern before $R$, the event $P$ must occur strictly before the first $R$.

**The survey.** Dwyer, Avrunin and Corbett collected 555 specifications for finite-state verification from at least 35 sources, from hardware and software, in several logics, and classified them by hand. About 92% matched a pattern, and response, universality and absence were the most common patterns. This is an empirical result about the collection they studied, not a theorem.

## Examples

**Reading a formula on words.** On the word $\{P\}\ \{R\}\ \emptyset^\omega$, absence before $R$, $\mathsf{F} R \to (\neg P\ \mathsf{U}\ R)$, is false, since $P$ occurs at position 0 and the first $R$ is at position 1. On $\{R\}\ \{P\}\ \emptyset^\omega$ it is true, because the scope ends at position 0. On $\emptyset\ \{P\}^\omega$ it is also true, because there is no $R$ and so no scope. Response before $R$ is false on $\{P\}\ \{R\}\ \{S\}^\omega$: the answer $S$ comes, but only after the scope has closed.

**The scope "after $Q$" with a non-monotone pattern.** For absence, existence, universality and response, the formulas of the after-$Q$ column give the same result whether "after $Q$" means after the first $Q$ or after some $Q$, because a demand that holds from the first $Q$ on also holds from each later $Q$, and for existence the converse holds too. For precedence this is not so. The formula $\mathsf{G}\,\neg Q \vee \mathsf{F}(Q \wedge (\neg P\ \mathsf{W}\ S))$ is true on $\{P, Q\}\ \{Q, S\}\ \emptyset^\omega$, because the constraint holds from the second $Q$, but precedence from the first $Q$ fails: $P$ occurs there and $S$ has not occurred. A user must decide which reading is meant and check the formula on such small words.

**From English to a formula.** "Each request that is made before shutdown is granted before shutdown" is response ($P$ = request, $S$ = grant) with scope before $R$ = shutdown. The table gives $\mathsf{F} R \to (P \to (\neg R\ \mathsf{U}\ (S \wedge \neg R)))\ \mathsf{U}\ R$. "The log is never written while the lock is held" is absence ($P$ = write) between $Q$ = lock and $R$ = unlock, or after $Q$ until $R$ if the lock may never be released.

**A typical mistake.** A user who writes $\neg P\ \mathsf{U}\ R$ for "no $P$ before $R$" demands that $R$ eventually happens, which the requirement did not say. A run with no $R$ and no $P$ then fails the check. The pattern formula $\mathsf{F} R \to (\neg P\ \mathsf{U}\ R)$ avoids this. The weak until $\neg P\ \mathsf{W}\ R$ is close but not the same: on a run with a $P$ and no $R$ it is false, while the pattern, which makes no demand when the scope never closes, is true.

## Where it is used

- Front ends of model checkers and requirement tools, where a user fills in a pattern and a scope in a structured English grammar and the tool produces LTL or CTL.
- The extension to real time by Konrad and Cheng (2005), with bounds on the delays, mapped to timed logics; and probabilistic patterns for [PCTL](/pctl-model-checking/) with probability bounds.
- Teaching: the table is a good set of exercises for reading and writing LTL.
- Runtime verification and testing, where monitors are generated from the patterns.
- Checking for vacuous success: a pattern with an implication, such as response, can pass because its trigger $P$ never happens; [vacuity checking](/vacuity-checking/) detects this.

## References
