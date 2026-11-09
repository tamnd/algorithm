---
tag: K2JR62
kind: technique
slug: bounded-model-checking
name: Bounded model checking
aliases:
- BMC
- Symbolic model checking without BDDs
area: logic-and-constraints/model-checking
level: advanced
summary: Search for counterexamples of length at most k by unrolling the transition relation k times into one formula and giving it to a SAT or SMT solver.
prereqs: [sat, kripke-structure, linear-temporal-logic, safety-property]
see_also: [sat-based-bounded-model-checking, completeness-threshold, k-induction, ic3-pdr, interpolation-based-model-checking, symbolic-model-checking, incremental-sat, counterexample-generation]
sources:
  - paper: doi:10.1007/3-540-49059-0_14
    title: Armin Biere, Alessandro Cimatti, Edmund M. Clarke and Yunshan Zhu, Symbolic model checking without BDDs, TACAS 1999, LNCS 1579
    locator: pages 193 to 207 (the bounded semantics of LTL, the translation to propositional formulas, the bound by the diameter, and the experiments against SMV)
  - paper: doi:10.1016/S0065-2458(03)58003-2
    title: Armin Biere, Alessandro Cimatti, Edmund M. Clarke, Ofer Strichman and Yunshan Zhu, Bounded model checking, Advances in Computers 58, 2003
    locator: pages 117 to 148 (a survey of the method, the completeness thresholds, and the relation to induction)
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (editors), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: the chapter Bounded Model Checking by Armin Biere (the encodings, completeness, and the induction-based extensions)
---

Bounded model checking (BMC) looks for a counterexample to a temporal property among the paths of a fixed length $k$. It writes the question "is there a path of $k$ steps from an initial state that violates the property?" as one propositional formula, with a copy of the state variables for each time step, and asks a SAT solver. A satisfying assignment is a counterexample, and it is a shortest one if $k$ grows from 0. If the formula is unsatisfiable, no counterexample of that length exists, and $k$ grows. Biere, Cimatti, Clarke and Zhu introduced the method in 1999 under the title "Symbolic model checking without BDDs". It replaced the BDDs of [symbolic model checking](/symbolic-model-checking/) with SAT solvers, which often handle large designs better. Plain BMC finds bugs but cannot prove a property, unless $k$ reaches a [completeness threshold](/completeness-threshold/). The exact formulas, the CNF encoding and the loop conditions for LTL are on the page [SAT-based bounded model checking](/sat-based-bounded-model-checking/). [k-induction](/k-induction/), [interpolation](/interpolation-based-model-checking/) and [IC3](/ic3-pdr/) extend BMC to complete methods.

## In plain words

We want to know whether a machine can reach a bad state. BMC asks a narrower question: can it reach a bad state in exactly $k$ steps? We write $k$ copies of the machine's step rule one after another, like frames of a film, and ask a SAT solver to fill in values so that the first frame is a start state and some frame is bad.

If the solver finds values, we have a concrete bad run, step by step. If not, there is no bad run of that length, and we try $k + 1$. Short bugs are found quickly. But a "no" for every $k$ we tried says nothing about longer runs, unless we know how long runs can usefully be.

## When it applies

- **Finding bugs.** Most bugs in hardware and in software show up in short runs. BMC finds the shortest counterexample, which is easy to read.
- **Large designs.** The formula has size linear in $k$ times the size of the design, and modern SAT solvers handle millions of clauses. BDD methods can fail on such designs because of the BDD size.
- **Shallow properties.** When the bound $k$ needed in practice is small, or a [completeness threshold](/completeness-threshold/) is known and small, BMC also proves properties.
- **Software.** Loops and recursion are unrolled a fixed number of times, and the program becomes one formula over bit-vectors or other SMT theories. Tools such as CBMC check C programs this way.

## The template

A finite system has state variables $s$, an initial-state predicate $I(s)$ and a transition relation $T(s, s')$. Write $s_0, \ldots, s_k$ for $k + 1$ copies of the variables and $\mathrm{path}_k = \bigwedge_{i=0}^{k-1} T(s_i, s_{i+1})$.

```pseudo id=main
BMC(I, T, φ, kmax)
L1  for k ← 0 to kmax do
L2      F ← I(s_0) ∧ path_k ∧ [¬φ]_k                          ▷ [¬φ]_k: a k-step path violates φ
L3      if SAT(F) then return FAILS, with the path s_0, ..., s_k read from the model
L4  return NO COUNTEREXAMPLE UP TO kmax
```

For an invariant $\mathrm{G}\,P$ one can take $[\neg \mathrm{G}\,P]_k = \neg P(s_k)$, since the shorter paths were checked in earlier rounds. For a general LTL formula, a counterexample may be infinite. BMC then looks for either a finite prefix that already violates the formula, or a *lasso*: a path $s_0, \ldots, s_k$ with a back edge $T(s_k, s_l)$ for some $l \le k$, which describes an infinite path. The translation $[\neg \varphi]_k$ is a disjunction over these cases. Its details, and the CNF encoding, are on [SAT-based bounded model checking](/sat-based-bounded-model-checking/).

**Why it is sound.** Each model of $F$ gives values to $s_0, \ldots, s_k$ that satisfy $I$, each step of $T$, and the bounded semantics of $\neg \varphi$. Biere et al. showed that the bounded semantics implies the usual semantics: a model is a real counterexample.

**Why it is incomplete, and when it is complete.** An unsatisfiable $F$ only excludes counterexamples of length $k$ (or with loops of that size). For invariants, every reachable state is reached within the *diameter* $d$ of the system, the largest shortest distance from an initial state to a reachable state. So if no bad state is found for $k \le d$, the property holds. Biere et al. gave this bound; it is a [completeness threshold](/completeness-threshold/). Biere et al. express the test for $d$ as a quantified Boolean formula, which is expensive to decide, so the over-approximation by the *recurrence diameter*, the length of the longest simple path from an initial state, is used instead. That one can be checked with a SAT query of the same shape, but it can be exponentially larger than $d$.

## Classic examples

- **Hardware counterexamples.** Biere et al. (1999) reported circuits where SAT-based BMC found counterexamples faster than the BDD-based model checker SMV. These are measured results on their benchmarks, not a general claim.
- **Industrial use.** After 1999 BMC became a standard engine in commercial and academic hardware verification tools, together with BDD-based and later IC3-based engines.
- **Software.** CBMC (Clarke, Kroening and Lerda, 2004) unrolls C programs and checks assertions, array bounds and pointer safety with SAT. ESBMC and other tools follow the same pattern with SMT solvers.
- **A small example.** For the 3-bit counter with an enable input on the page [SAT-based bounded model checking](/sat-based-bounded-model-checking/), and the property "the counter is never 7", the formula is unsatisfiable for $k < 7$ and satisfiable at $k = 7$, which gives a counterexample of length 7.

## Variations

- **Incremental BMC.** The formula for $k + 1$ contains the one for $k$, so an [incremental SAT](/incremental-sat/) solver keeps learned clauses across rounds.
- **Completeness by induction.** [k-induction](/k-induction/) adds an induction step to each round and proves invariants.
- **Completeness by abstraction.** [Interpolation](/interpolation-based-model-checking/) turns each unsatisfiable BMC query into an over-approximate image, and [CEGAR](/cegar/) uses BMC to check abstract counterexamples.
- **Without unrolling.** [IC3](/ic3-pdr/) keeps the SAT queries to one step of $T$ and builds an inductive invariant.
- **Bounded semantics for other logics.** BMC has been extended to ACTL, to timed and hybrid systems, and to SMT theories for software.
- **Linear encodings.** The original LTL translation grows faster than linearly in $k$. Later encodings, such as that of Biere, Heljanko, Junttila, Latvala and Schuppan (2006), are linear in $k$ and in the formula.

## Pitfalls

- **Taking "no counterexample up to $k$" as a proof.** It is a proof only when $k$ reaches a completeness threshold. Report the bound with the result.
- **Checking only the last state for general properties.** For invariants $\neg P(s_k)$ suffices if all earlier $k$ were checked. For an LTL formula, a violation can need a loop; checking only finite prefixes misses liveness counterexamples.
- **Non-total transition relations.** If some states have no successor, a path of length $k$ may not exist even though a shorter path reaches a bad state. Check every $k$, or test $\bigvee_i \neg P(s_i)$.
- **Large $k$.** The formula grows linearly in $k$, but the SAT time can grow much faster. BMC is best for shallow bugs.

## Exercises

1. Show that for invariants, checking $\neg P(s_k)$ for each $k$ from 0 to $K$ finds the same counterexamples as checking $\bigvee_{i \le K} \neg P(s_i)$ once, if $T$ is total.
2. Give a system with diameter 1 and recurrence diameter $2^n - 1$. *Hint:* let the only initial state have an edge to every other state, and add a simple path through all states.
3. Write $[\neg \mathrm{F}\,p]_k$ for the lasso case. *Answer:* $\bigvee_{l=0}^{k} T(s_k, s_l) \wedge \bigwedge_{i=0}^{k} \neg p(s_i)$.
4. Why does BMC find the shortest counterexample, while a depth-first explicit-state search may not?

## References
