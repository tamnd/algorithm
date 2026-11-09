---
tag: 2N1RSX
kind: concept
slug: unsat-core
name: Unsatisfiable core
aliases:
- unsat core
- minimal unsatisfiable subset
- UC
- unsatisfiable subset
area: logic-and-constraints/smt
level: core
summary: A subset of the assertions of an unsatisfiable problem that is still unsatisfiable. Solvers need not return a minimal one; a minimal unsatisfiable subset is a core with no smaller core inside.
prereqs: [smt-problem, sat]
see_also: [minimal-unsatisfiable-subset, minimal-correction-subset, theory-conflict-explanation, incremental-solving, smt-lib, maxsmt, cegar, cdcl-t]
sources:
  - url: https://smt-lib.org/papers/smt-lib-reference-v2.7-r2025-07-07.pdf
    title: Clark Barrett, Pascal Fontaine and Cesare Tinelli, The SMT-LIB Standard, Version 2.7, release of July 7, 2025
    locator: Section 4.2.7 (get-unsat-assumptions and get-unsat-core), note 52 (the result is not required to be minimal), Section 4.1.7 (the option produce-unsat-cores)
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.7.4 (producing proofs), Section 33.7.5 (identifying unsatisfiable cores, with the proof-based, assumption-based and lemma-lifting approaches)
  - paper: doi:10.1007/978-3-540-72788-0_32
    title: Alessandro Cimatti, Alberto Griggio and Roberto Sebastiani, A simple and flexible way of computing small unsatisfiable cores in SAT modulo theories, SAT 2007, LNCS 4501, pages 334 to 339
    locator: the lemma-lifting approach
  - paper: doi:10.1007/978-3-540-24605-3_37
    title: Niklas Eén and Niklas Sörensson, An extensible SAT-solver, SAT 2003, LNCS 2919, pages 502 to 518
    locator: incremental solving under assumptions, the final conflict expressed in the assumptions
  - paper: doi:10.1007/s10817-007-9084-z
    title: Mark H. Liffiton and Karem A. Sakallah, Algorithms for computing minimal unsatisfiable subsets of constraints, Journal of Automated Reasoning 40(1), 2008, pages 1 to 33
    locator: minimal unsatisfiable subsets, minimal correction subsets and their hitting set duality
  - paper: doi:10.1109/fmcad.2016.7886661
    title: Ofer Guthmann, Ofer Strichman and Anna Trostanetski, Minimal unsatisfiable core extraction for SMT, FMCAD 2016, pages 57 to 64
    locator: extraction of minimal cores in SMT solvers
---

An *unsatisfiable core* of an unsatisfiable problem is a subset of its assertions that is still unsatisfiable. It tells the user which parts of the problem cause the failure. The whole set of assertions is always a core, so the word alone promises nothing about size. A *minimal unsatisfiable subset* (MUS) is a core in which every proper subset is satisfiable: no assertion can be removed. A *minimum* core is a core of the smallest size. Every minimum core is minimal, and every minimal core is a core, but the converses fail. This page keeps the alias "minimal unsatisfiable subset" because many texts use the two names loosely, but the two are not the same thing: the [minimal unsatisfiable subset](/minimal-unsatisfiable-subset/) page treats the minimal notion and the algorithms that compute it. The SMT-LIB standard asks a solver only for a core, and says in a note that the result is not required to be minimal.

## In plain words

A solver says "no solution". The user asks "why?". A list of all the rules is a true answer, but not a useful one.

An unsat core is a shorter list of rules that already have no solution together. The rules that are not on the list played no part.

A solver gets a core almost for free: it notes which rules it used to reach its "no". But it may also have used rules that it did not need, so the list can still be too long. A minimal list is one where every rule is needed: drop any one, and a solution exists. Finding such a list takes extra work, usually one more solver call for each rule on the list.

## The idea

**Definitions.** Let $A = \{A_1, \ldots, A_m\}$ be a set of assertions with no model in the theory $T$.

- A *core* is a subset $C \subseteq A$ that is $T$-unsatisfiable.
- A *minimal unsatisfiable subset* is a core $C$ such that every $C' \subsetneq C$ is $T$-satisfiable.
- A *minimum* core is a core of the smallest size.

A problem can have many minimal cores of different sizes, so minimal does not mean minimum. In SAT, the number of MUSes can be exponential in $m$.

**Cores in SMT-LIB.** The SMT-LIB standard (Section 4.2.7) defines the command `get-unsat-core`. It returns the labels of a subset $A'_n$ of the *labeled* assertions, those asserted as `(assert (! t :named f))`, such that $A'_n$ together with all unlabeled assertions and the assumptions of the last check is unsatisfiable. Unlabeled assertions and assumptions are never in the answer. The companion command `get-unsat-assumptions` returns a subset of the assumptions of the last `check-sat-assuming` that still gives `unsat`, and note 52 of the standard says that it is not required to be minimal, because "the minimization problem alone is NP-hard in general", and a solver can comply by returning all the assumptions. Both commands need an option, `:produce-unsat-cores` or `:produce-unsat-assumptions`, which is false by default.

**How solvers find a core.** The Handbook (Section 33.7.5) names three approaches.

- *Assumptions.* Give each assertion $A_i$ a fresh selector variable $s_i$, assert $s_i \rightarrow A_i$, and solve under the assumptions $s_1, \ldots, s_m$. When the search fails, the final conflict can be written over the selectors alone, and the core is the set of $A_i$ whose selectors appear in it. This is the method of [incremental solving](/incremental-solving/).
- *Proofs.* Record the resolution proof of the empty clause. Its leaves are input clauses and theory lemmas. The core is the set of input clauses among the leaves. Theory lemmas are $T$-valid, so they are left out.
- *Lemma lifting.* Give the [Boolean abstraction](/boolean-abstraction/) of the input together with all the theory lemmas of the run to a propositional core extractor, then remove the lemmas from its core and map the rest back.

None of the three aims at a minimal core. The core depends on the order of the search, and it often contains assertions that the refutation used but did not need.

**From a core to an MUS.** The simplest method is *deletion*: for each assertion $c$ of the core in turn, check the core without $c$; if it is still unsatisfiable, drop $c$ for good. This needs one solver call per assertion, and its result is minimal: an assertion that stayed was needed at the time it was tested, and the set only got smaller later. Faster methods reuse the core of each failed check, or split the set in halves, as in QuickXplain. A *minimal correction subset* (MCS) is the dual notion: a set of assertions whose removal makes the rest satisfiable, with no proper subset that does the same. The MUSes and the MCSes of a set are minimal hitting sets of each other (Liffiton and Sakallah).

**Not a theory conflict.** A [theory conflict explanation](/theory-conflict-explanation/) is a set of *literals* inside one theory check. A core is a set of input *assertions*, and its unsatisfiability can need both Boolean and theory reasoning.

## Examples

Take six integer constraints over $x$ and $y$.

| label | assertion |
|---|---|
| $A_1$ | $x \ge 1$ |
| $A_2$ | $y \ge x$ |
| $A_3$ | $y \le 0$ |
| $A_4$ | $x \le 5$ |
| $A_5$ | $x + y \ge 20$ |
| $A_6$ | $x \le 0$ |

A script checked every subset by search over $[-40, 40]^2$, which contains a witness for each satisfiable subset. The set of all six is unsatisfiable, and 28 of the 64 subsets are cores. Exactly five are minimal.

- $\{A_1, A_6\}$: $x \ge 1$ and $x \le 0$. This is the only minimum core, of size 2.
- $\{A_1, A_2, A_3\}$: $y \ge x \ge 1$, but $y \le 0$.
- $\{A_2, A_3, A_5\}$: $x \le y \le 0$, so $x + y \le 0$.
- $\{A_3, A_4, A_5\}$: $x + y \le 5$.
- $\{A_3, A_5, A_6\}$: $x + y \le 0$.

A solver that returns all six labels gives a correct core that is not minimal. Deletion in the order $A_1, \ldots, A_6$ drops $A_1$, $A_2$ and $A_4$, keeps $A_3$, $A_5$ and $A_6$, and stops at the MUS $\{A_3, A_5, A_6\}$. It is minimal, but it has three elements, while the minimum core has two. In SMT-LIB, the user would label the assertions, set `:produce-unsat-cores` to true, call `check-sat`, and then `get-unsat-core`.

## Where it is used

- **Debugging specifications.** A core points to the few requirements, or the few lines of a program, that are in conflict.
- **Abstraction refinement.** [CEGAR](/cegar/) and [bounded model checking](/bounded-model-checking/) use cores to see which parts of a model a proof needed, and keep only those in the abstraction.
- **[MaxSMT](/maxsmt/).** Core-guided algorithms find a core, relax it, and repeat. Cores and [minimal correction subsets](/minimal-correction-subset/) are dual.
- **[Incremental solving](/incremental-solving/).** Assumptions and their failed subset tell the user which of the tried guesses was wrong.
- **Explanations and diagnosis.** Product configuration and constraint tools show a minimal core to the user as the reason for a failure.

## References
