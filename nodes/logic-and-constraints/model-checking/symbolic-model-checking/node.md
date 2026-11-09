---
tag: FYQ9Y8
kind: technique
slug: symbolic-model-checking
name: Symbolic model checking
aliases:
- BDD-based model checking
- Symbolic CTL model checking
area: logic-and-constraints/model-checking
level: advanced
summary: Model check CTL or the mu-calculus on sets of states, not single states, by representing state sets and the transition relation as BDDs and computing fixed points.
prereqs: [reduced-ordered-bdd, bdd-quantification, ctl-model-checking, fixed-point, kripke-structure]
see_also: [symbolic-reachability, saturation-algorithm, variable-ordering, modal-mu-calculus, fairness, bounded-model-checking, ic3-pdr, state-explosion-problem]
sources:
  - paper: doi:10.1016/0890-5401(92)90017-A
    title: Jerry R. Burch, Edmund M. Clarke, Kenneth L. McMillan, David L. Dill and L. J. Hwang, Symbolic model checking, 10^20 states and beyond, Information and Computation 98(2), 1992
    locator: pages 142 to 170 (the mu-calculus model checker over BDDs, the encoding of CTL and fairness as fixed points, and the experiments)
  - paper: "Jerry R. Burch, Edmund M. Clarke, Kenneth L. McMillan, David L. Dill and L. J. Hwang, Symbolic model checking, 10^20 states and beyond, Fifth Annual IEEE Symposium on Logic in Computer Science (LICS), 1990"
    locator: the conference version, with the claim of the title
  - book: isbn:9780792393801
    title: Kenneth L. McMillan, Symbolic Model Checking, Kluwer Academic Publishers, 1993
    locator: the chapters on the symbolic CTL algorithm with fairness, on the SMV language and system, and on the cache coherence case studies
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Section 6.7, Symbolic CTL Model Checking (switching functions, the encoding of transition systems, and the symbolic fixed-point computations)
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: the chapters on binary decision diagrams and on symbolic model checking (the fixed-point characterization of CTL and the symbolic algorithm with fairness)
---

Symbolic model checking verifies a finite system against a temporal logic formula by working with sets of states instead of single states. A set of states over $n$ Boolean state variables is a Boolean function, and a [reduced ordered BDD](/reduced-ordered-bdd/) often represents it in far less than $2^n$ space. The transition relation $T(s, s')$ is a BDD over two copies of the variables. The basic step is the *preimage*, $\mathrm{EX}\,Y = \exists s'.\, T(s, s') \wedge Y(s')$, computed with [BDD quantification](/bdd-quantification/). Each CTL operator is a [fixed point](/fixed-point/) of preimage and Boolean operations, so the checker evaluates a formula bottom up, one BDD per subformula, and checks that the initial states lie in the BDD of the whole formula. Burch, Clarke, McMillan, Dill and Hwang introduced the method in 1990 under the title "Symbolic model checking: $10^{20}$ states and beyond", and McMillan's 1993 thesis and his SMV system made it a standard tool for hardware. The forward variant that only computes the reachable states is [symbolic reachability](/symbolic-reachability/).

## In plain words

An explicit model checker visits states one by one, so it stops when there are too many states. A symbolic model checker describes a whole set of states with one formula, kept in a compact shared graph called a BDD. A set of a million states can have a BDD with a few hundred nodes, when the set has regular structure.

The checker then works with these formulas. "The states that have a successor in $Y$" is one BDD operation on the formula for $Y$. Properties such as "on some path, $p$ holds until $q$" become a loop that grows a set until it stops changing. When the loop ends, the checker asks whether every initial state is in the final set.

## When it applies

- **Finite systems with many Boolean state variables.** Hardware designs, protocols and finite-state controllers, where the state is a vector of bits and $T$ is a Boolean formula.
- **The relevant sets have small BDDs.** This holds for many control-dominated designs with a good [variable ordering](/variable-ordering/). It fails for some data paths: Bryant showed in 1991 that the BDD of the middle output bit of an integer multiplier is exponential in the word size for every ordering.
- **Branching-time properties.** CTL, CTL with fairness, and the [modal mu-calculus](/modal-mu-calculus/) map directly to fixed points over state sets. LTL is checked by a symbolic product with a tableau or a Büchi automaton and a fair-cycle test.
- **Exact answers are needed.** Unlike [bounded model checking](/bounded-model-checking/), the method proves properties for all path lengths.

## The template

We use the notation of [CTL model checking](/ctl-model-checking/). A Kripke structure has state variables $\bar x = (x_1, \ldots, x_n)$, next-state copies $\bar x'$, an initial-state BDD $I(\bar x)$, and a transition BDD $T(\bar x, \bar x')$ that is total. Each atomic proposition $p$ is a BDD over $\bar x$. Formulas are in the adequate set $\{\neg, \wedge, \mathrm{EX}, \mathrm{EU}, \mathrm{EG}\}$; the other operators are abbreviations.

```pseudo id=main
SAT(φ)                                                  ▷ returns the BDD of the states that satisfy φ
L1  if φ is an atomic proposition p then return the BDD of p
L2  if φ = ¬ψ then return NOT(SAT(ψ))
L3  if φ = ψ ∧ χ then return AND(SAT(ψ), SAT(χ))
L4  if φ = EX ψ then return PRE(SAT(ψ))
L5  if φ = E[ψ U χ] then                               ▷ least fixed point μZ. χ ∨ (ψ ∧ EX Z)
L6      A ← SAT(ψ); B ← SAT(χ); Z ← B
L7      repeat Z_old ← Z; Z ← OR(Z, AND(A, PRE(Z))) until Z = Z_old
L8      return Z
L9  if φ = EG ψ then                                    ▷ greatest fixed point νZ. ψ ∧ EX Z
L10     A ← SAT(ψ); Z ← A
L11     repeat Z_old ← Z; Z ← AND(A, PRE(Z)) until Z = Z_old
L12     return Z
PRE(Y) = ∃x̄'. T(x̄, x̄') ∧ Y[x̄ := x̄']                    ▷ one relational product
CHECK(φ): return "holds" iff AND(I, NOT(SAT(φ))) is the constant 0
```

The test $Z = Z_{\mathrm{old}}$ is a pointer comparison, since reduced ordered BDDs are canonical. The loop of line L7 computes an increasing sequence of sets, and the loop of line L11 a decreasing one, so each stops after at most $2^n$ rounds, and in practice after a number of rounds close to the length of the longest relevant path. That the loops compute the right sets follows from the [Knaster-Tarski theorem](/knaster-tarski-theorem/): the functions $Z \mapsto \chi \vee (\psi \wedge \mathrm{EX}\,Z)$ and $Z \mapsto \psi \wedge \mathrm{EX}\,Z$ are monotone on the finite lattice of state sets, and the iteration from the bottom or the top reaches the least or the greatest fixed point.

The relational product $\exists \bar x'.\, T \wedge Y'$ is computed in one recursive pass that conjoins and quantifies at the same time, with a [computed table](/computed-table/) for memoization. Its cost is the main cost of the method.

**Fairness.** With fairness constraints $F_1, \ldots, F_k$ (sets that a fair path visits infinitely often), fair $\mathrm{EG}$ is the nested fixed point $\nu Z.\, \psi \wedge \bigwedge_{j} \mathrm{EX}\, \mathrm{E}[\psi\, \mathrm{U}\, (Z \wedge F_j)]$, the Emerson-Lei form. Fair $\mathrm{EX}$ and $\mathrm{EU}$ are then restricted to states with a fair path, $\mathrm{fair} = \mathrm{EG}_{\mathrm{fair}}\, \mathit{true}$. See [fairness](/fairness/).

**Counterexamples.** The checker keeps the sequence of sets from the fixed-point loops and walks back through it to give a path or a lasso as a witness or counterexample; see [counterexample generation](/counterexample-generation/).

## Classic examples

- **The examples of Burch et al.** The 1990 paper and its 1992 journal version reported checking a synchronous pipeline and other circuits whose state spaces had more than $10^{20}$ states. These are measured results on specific designs; the method has no general bound below $2^n$ on BDD size.
- **Cache coherence.** McMillan's thesis used SMV on the Encore Gigamax cache protocol, and Clarke and others checked the IEEE Futurebus+ cache coherence protocol with SMV in 1993 and found errors in the standard.
- **Reachability.** Only $\mathrm{EF}$ in reverse, or the forward image fixed point $\mu Z.\, I \vee \mathrm{post}(Z)$, is needed for invariants; this is [symbolic reachability](/symbolic-reachability/).
- **Mu-calculus.** The same template evaluates any formula of the [modal mu-calculus](/modal-mu-calculus/), with one loop per fixed-point operator, nested by alternation depth.

## Variations

- **Partitioned transition relations.** Burch, Clarke and Long (1991) keep $T$ as a conjunction or disjunction of parts and quantify each variable as soon as no later part uses it (early quantification). This avoids building the BDD of the whole $T$.
- **Frontier sets.** Forward and backward loops can apply the image only to the states added in the last round, or to any set between that frontier and the full set, whichever has the smaller BDD.
- **Saturation.** For asynchronous systems with local events, [saturation](/saturation-algorithm/) applies events bottom up in an MDD and often keeps the peak size far smaller than breadth-first iteration.
- **Forward model checking.** Some CTL formulas can be checked with images instead of preimages, which works well with reachability-based state set restriction.
- **SAT-based methods.** [Bounded model checking](/bounded-model-checking/), [interpolation](/interpolation-based-model-checking/) and [IC3](/ic3-pdr/) replace BDDs with a SAT solver. They are often better on large designs where BDDs blow up, and worse on some designs where BDDs stay small. Both are called symbolic, since both work with formulas, but "symbolic model checking" without a qualifier usually means the BDD-based method.

## Pitfalls

- **Bad variable ordering.** The same set can have a BDD of linear or of exponential size under different orders. Current and next-state copies of a variable should be adjacent, and related variables should be close. Finding an optimal order is NP-hard (see [variable ordering NP-hardness](/variable-ordering-np-hardness/)), so tools use heuristics and dynamic reordering.
- **Building the monolithic transition relation.** For large designs the BDD of $T$ is often much larger than the reachable set. Use partitioned relations.
- **Intermediate blow-up.** A small result can have a huge intermediate BDD inside the relational product. Peak memory, not final size, decides whether a run ends.
- **Non-total transition relations.** The fixed-point characterization of $\mathrm{EG}$ and $\mathrm{AX}$ assumes every state has a successor. Add self-loops to deadlock states, or treat them explicitly.
- **Unreachable states.** The sets computed for subformulas include unreachable states, and their BDDs can be larger than needed. Restricting to the reachable states first can help, or hurt if the reachable set itself has a large BDD.

## Exercises

1. Write $\mathrm{AG}\,p$, $\mathrm{AF}\,p$ and $\mathrm{EF}\,p$ as fixed points of $\mathrm{EX}$, $\neg$ and $\wedge$. *Answer:* $\mathrm{EF}\,p = \mu Z.\, p \vee \mathrm{EX}\,Z$, $\mathrm{AG}\,p = \neg \mathrm{EF}\, \neg p$, $\mathrm{AF}\,p = \neg \mathrm{EG}\, \neg p$.
2. Show that the loop of line L7 needs at most $d + 1$ rounds, where $d$ is the largest distance in the graph from a state of $\mathrm{E}[\psi\,\mathrm{U}\,\chi]$ to a state of $\chi$ along $\psi$-states.
3. A counter with $n$ bits and $T$ "add 1 modulo $2^n$" has a transition BDD of size $O(n)$ under the interleaved order $x_1, x'_1, \ldots, x_n, x'_n$ with $x_1$ the lowest bit. What happens to the size under the order $x_1, \ldots, x_n, x'_1, \ldots, x'_n$? *Hint:* the BDD must remember all of $\bar x$ before it reads any $x'_i$.
4. Give a family of systems where symbolic model checking of $\mathrm{EF}\,p$ needs $2^n$ fixed-point rounds although every BDD stays small. *Hint:* a binary counter that must count to $2^n - 1$.

## References
