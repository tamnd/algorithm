---
tag: THR1ZW
kind: algorithm
slug: conflict-driven-answer-set-solving
name: Conflict-driven answer set solving
aliases:
- CDNL-ASP
- conflict-driven nogood learning for ASP
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: research
summary: Encodes completion and loop constraints as nogoods and runs CDCL-style search with unfounded set checks to find stable models.
model: word-ram
complexity:
  vars: {n: the number of atoms, s: "the size of the program, the number of rules plus the number of body literals"}
  time: {worst: "2^O((n + s) log(n + s))"}
  space: {extra: "2^O((n + s) log(n + s))"}
properties: {deterministic: true}
history:
  year: 2007
  people: [Martin Gebser, Benjamin Kaufmann, André Neumann, Torsten Schaub]
  note: The clasp solver of Gebser, Kaufmann, Neumann and Schaub used conflict-driven nogood learning for answer sets from 2007. Gebser, Kaufmann and Schaub gave the full account with proofs in 2012.
prereqs: [cdcl, clark-completion, loop-formulas]
see_also: [smodels-algorithm, answer-set-programming, fages-theorem, stable-model-semantics, first-uip, unit-propagation, answer-set-grounding, stable-model-np-completeness]
sources:
  - paper: doi:10.1016/j.artint.2012.04.001
    title: "Martin Gebser, Benjamin Kaufmann and Torsten Schaub, Conflict-driven answer set solving: From theory to practice, Artificial Intelligence 187-188, 52 to 89 (2012)"
    locator: the nogoods of the completion and the loop nogoods, the theorem that answer sets are the solutions of both, the algorithm CDNL-ASP with its propagation, unfounded set check and conflict analysis
  - book: isbn:9781608459711
    title: Martin Gebser, Roland Kaminski, Benjamin Kaufmann and Torsten Schaub, Answer Set Solving in Practice, Morgan and Claypool (2012)
    locator: Chapter 5 on the characterizations by completion and loop nogoods and Chapter 6 on conflict-driven solving
  - paper: doi:10.1016/j.artint.2004.04.004
    title: "Fangzhen Lin and Yuting Zhao, ASSAT: computing answer sets of a logic program by SAT solvers, Artificial Intelligence 157(1-2), 115 to 137 (2004)"
    locator: loop formulas and the theorem that the models of the completion and the loop formulas are the answer sets
  - paper: doi:10.1016/s0004-3702(02)00187-x
    title: Patrik Simons, Ilkka Niemelä and Timo Soininen, Extending and implementing the stable model semantics, Artificial Intelligence 138(1-2), 181 to 234 (2002)
    locator: the earlier smodels search without learning, for comparison
---

Conflict-driven answer set solving finds the [answer sets](/stable-model-semantics/) of a ground normal program with the search engine of [CDCL](/cdcl/): decisions, propagation, conflict analysis to the [first UIP](/first-uip/), nogood learning and backjumping. What differs from CDCL is the input and one extra propagator. The constraints are not a CNF formula but *nogoods* built from the program: one set from the [Clark completion](/clark-completion/), with a variable for each rule body, and one set from the [loop formulas](/loop-formulas/), which is exponential in size and so is added only on demand. After unit propagation, an *unfounded set* check finds atoms that only support each other, and adds the loop nogoods that make them false. Gebser, Kaufmann and Schaub (2012) proved that the answer sets are exactly the solutions of the two sets of nogoods.

## In plain words

The solver turns the program into a list of forbidden combinations. "This rule's conditions hold but its conclusion is false" is forbidden. "This fact is true but none of its rules has true conditions" is forbidden too. Then it searches the way a modern SAT solver does: guess, follow the forbidden combinations to forced values, and when a combination is hit, find the reason and remember it so the same mistake is not made again. One thing remains. A group of facts can be true only because each of them proves another in a circle. After each round of forced values, the solver looks for such a group. When it finds one, it writes down a new forbidden combination that says the group cannot be true without help from outside, and goes on.

## The problem

The input is a finite ground normal program $P$ over a set $A$ of $n$ atoms, with rules $h \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_k$ and constraints $\leftarrow b_1, \ldots, \mathit{not}\ c_k$. The output is an answer set of $P$, or the answer that there is none; repeated calls with blocking nogoods list all of them. Deciding whether an answer set exists is NP-complete in this propositional case, by the [NP-completeness theorem](/stable-model-np-completeness/). Programs with variables are first [ground](/answer-set-grounding/).

## The algorithm

The solver has a Boolean variable for each atom $p$ and for each distinct body $\beta$, with positive atoms $\beta^+$ and negative atoms $\beta^-$. A nogood is a set of literals $\mathbf{T}v$ or $\mathbf{F}v$ that must not all hold. The completion nogoods $\Delta_P$ are:

- for each body $\beta$: $\{\mathbf{F}\beta\} \cup \{\mathbf{T}a : a \in \beta^+\} \cup \{\mathbf{F}a : a \in \beta^-\}$, and $\{\mathbf{T}\beta, \mathbf{F}a\}$ for $a \in \beta^+$, and $\{\mathbf{T}\beta, \mathbf{T}a\}$ for $a \in \beta^-$, so that $\beta$ is true exactly when its literals hold;
- for each atom $p$ with bodies $\beta_1, \ldots, \beta_k$: $\{\mathbf{F}p, \mathbf{T}\beta_i\}$ for each $i$, and $\{\mathbf{T}p, \mathbf{F}\beta_1, \ldots, \mathbf{F}\beta_k\}$, so that $p$ is true exactly when one of its bodies is;
- for each constraint with body $\beta$: $\{\mathbf{T}\beta\}$.

For a set $U$ of atoms, the *external bodies* $EB(U)$ are the bodies of rules with head in $U$ whose positive part does not meet $U$. The loop nogood of $p \in U$ is $\lambda(p, U) = \{\mathbf{T}p\} \cup \{\mathbf{F}\beta : \beta \in EB(U)\}$: $p$ cannot be true when no rule from outside $U$ supports $U$.

```pseudo id=main
CDNL-ASP(P)
L1  Γ ← Δ_P; A ← an empty assignment; dl ← 0
L2  loop
L3      (A, ε) ← PROPAGATE(P, Γ, A)              ▷ ε is a violated nogood, or none
L4      if ε ≠ none then
L5          if every literal of ε has level 0 then return "no answer set"
L6          (δ, j) ← ANALYZE(ε, A)
L7          Γ ← Γ ∪ {δ}; undo the literals of level above j; dl ← j
L8      else if A assigns every variable then return {p : Tp ∈ A}
L9      else dl ← dl + 1; add a decision literal on an open variable, at level dl

PROPAGATE(P, Γ, A)
L10 loop
L11     while some δ ∈ Γ has all its literals in A but one, σ, which is open: add the complement of σ, with reason δ
L12     if some δ ∈ Γ has all its literals in A then return (A, δ)
L13     if P is tight then return (A, none)
L14     U ← the atoms not false in A that no body which is not false can derive
L15     if U = ∅ then return (A, none)
L16     Γ ← Γ ∪ {λ(p, U) : p ∈ U}

ANALYZE(ε, A)
L17 k ← the largest level of a literal of ε
L18 while ε has two or more literals of level k do
L19     σ ← the literal of ε at level k assigned last; δ ← the reason of σ
L20     ε ← (ε ∖ {σ}) ∪ (δ ∖ {complement of σ})
L21 return (ε, the largest level of the other literals of ε, or 0 if there is none)
```

Line L14 computes the greatest unfounded set: start from the bodies that are not false and whose positive atoms are already derived, add their heads that are not false, and repeat. The atoms that are not false and never derived form $U$. After unit propagation every body in $EB(U)$ is false, so each new loop nogood at line L16 is violated or unit, and the next pass of line L11 makes progress. Lines L17 to L21 are the first-UIP scheme of CDCL. The Python code decides the first open variable false at line L9.

## Example

Take the program of the [smodels example](/smodels-algorithm/):

$$p \leftarrow \mathit{not}\ q. \quad q \leftarrow \mathit{not}\ p. \quad r \leftarrow p. \quad r \leftarrow s. \quad s \leftarrow r. \quad \leftarrow \mathit{not}\ r.$$

The variables are $p, q, r, s$ and the bodies $\beta_1 = \{\mathit{not}\ q\}$, $\beta_2 = \{\mathit{not}\ p\}$, $\beta_3 = \{p\}$, $\beta_4 = \{s\}$, $\beta_5 = \{r\}$ and $\beta_6 = \{\mathit{not}\ r\}$ of the constraint. $\Delta_P$ has 22 nogoods. The program is not tight, because of the cycle $r \to s \to r$.

| level | step | new literals | why |
|---|---|---|---|
| 0 | L11 | $\mathbf{F}\beta_6$, $\mathbf{T}r$ | $\{\mathbf{T}\beta_6\}$; then $\{\mathbf{F}\beta_6, \mathbf{F}r\}$ |
| 0 | L11 | $\mathbf{T}\beta_5$, $\mathbf{T}s$, $\mathbf{T}\beta_4$ | the body and support nogoods of $r$ and $s$ |
| 0 | L14 | $U = \emptyset$ | $p$, $q$ can be derived from $\beta_1$, $\beta_2$, then $r$ from $\beta_3$, then $s$ |
| 1 | L9 | $\mathbf{F}p$ | decision |
| 1 | L11 | $\mathbf{F}\beta_3$, $\mathbf{T}\beta_2$, $\mathbf{T}q$, $\mathbf{F}\beta_1$ | the body nogoods of $\beta_3$, $\beta_2$, then $q$, then $\beta_1$ |
| 1 | L14 | $U = \{r, s\}$, $EB(U) = \{\beta_3\}$ | the only bodies that are not false and could derive $r$ or $s$ are $\beta_4$ and $\beta_5$, which need $s$ and $r$ |
| 1 | L16, L12 | conflict on $\lambda(r, U) = \{\mathbf{T}r, \mathbf{F}\beta_3\}$ | $\mathbf{T}r$ is at level 0 and $\mathbf{F}\beta_3$ at level 1 |
| 0 | L6, L7 | learn $\{\mathbf{T}r, \mathbf{F}\beta_3\}$, back to level 0 | only one literal of level 1, so it is already the first UIP |
| 0 | L11 | $\mathbf{T}\beta_3$, $\mathbf{T}p$, $\mathbf{F}\beta_2$, $\mathbf{F}q$, $\mathbf{T}\beta_1$ | the learned nogood is unit |
| 0 | L8 | answer set $\{p, r, s\}$ | every variable is assigned and $U = \emptyset$ |

The run makes one decision, meets one conflict and adds two loop nogoods, $\lambda(r, U)$ and $\lambda(s, U)$. The assignment at level 1 before the conflict, with $q, r, s$ true, satisfies every nogood of the completion: only the unfounded set check rejects it.

## Correctness

The [correctness proof](proofs/correctness.md) has the details. Soundness: the search returns only a total assignment that violates no nogood of $\Delta_P$ and has an empty unfounded set. Then the true atoms $X$ form a model of the reduct $P^X$, because each true body forces its head, and every true atom is derived in the least model of $P^X$, because the unfounded set is empty. So $X$ is an answer set. Completeness: every nogood in the database is in $\Delta_P$, in the set $\Lambda_P$ of all loop nogoods, or is a resolvent of nogoods already in the database. So the database is implied by $\Delta_P \cup \Lambda_P$, and by the theorem of Gebser, Kaufmann and Schaub every answer set violates none of it. A conflict at level 0 therefore proves that there is no answer set. Termination is the CDCL argument, plus the fact that each pass of lines L14 to L16 adds a new loop nogood, of which there are finitely many.

## Complexity

Let $s$ be the number of rules plus the number of body literals. There are at most $n + s$ variables, and $\Delta_P$ has $O(s)$ nogoods of total size $O(s)$. The full set $\Lambda_P$ of loop nogoods can have $n \cdot 2^n$ members, which is why it is built on demand. The unfounded set check at line L14 takes $O(s)$ time with counters. The number of conflicts is not bounded by a polynomial, as for CDCL, and the NP-completeness of the problem makes a polynomial bound unlikely. The termination argument bounds the number of conflicts by the number of distinct level vectors, which gives the bound $2^{O((n + s) \log(n + s))}$ on time and on the size of the learned database. The Python code scans every nogood in each pass of unit propagation; solvers such as clasp use [watched literals](/two-watched-literals/) instead.

## Properties

- **Sound and complete.** It returns an answer set if and only if one exists, and enumeration with blocking nogoods lists each answer set once.
- **No extra work on tight programs.** If the positive dependency graph has no cycle, the completion nogoods are enough, by [Fages' theorem](/fages-theorem/), and the unfounded set check is skipped.
- **Learned nogoods are consequences.** Each learned nogood is a resolvent of completion nogoods, loop nogoods and earlier learned nogoods, so it holds in every answer set.
- **Loop nogoods on demand.** Only the loop nogoods of unfounded sets that the search actually meets are ever built.

## Variants and improvements

- **Bodies as variables.** Keeping a variable for each body, and not only for each atom, lets the solver branch and learn on bodies. Gebser, Kaufmann and Schaub (2012) discuss this choice.
- **Source pointers.** The unfounded set check can keep, for each atom, one body that still supports it, and recompute only the atoms that lose their support.
- **Optimization and enumeration.** clasp extends the search with minimize statements and with enumeration that does not need a blocking nogood per answer set.
- **Disjunctive programs.** For [disjunctive programs](/disjunctive-logic-program/), each candidate also needs a minimality check, which a second solver does; that problem is coNP-complete.
- **SAT with loop formulas.** ASSAT (Lin and Zhao 2004) gives the completion to a SAT solver and adds [loop formulas](/loop-formulas/) only when a model is not stable; CDNL-ASP adds them inside the search.

## When to use it

Use conflict-driven solving for real ASP workloads: planning, scheduling, configuration, and other combinatorial search problems written as [answer set programs](/answer-set-programming/). It is the method inside clasp and the clingo system. For a small program, or to teach the semantics, the simpler [smodels search](/smodels-algorithm/) shows the propagators more clearly.

## Pitfalls

- **Completion is not enough.** Without the unfounded set check the solver returns models of the completion, such as $\{q, r, s\}$ in the example, which are not answer sets.
- **External bodies.** A body that contains an atom of $U$ positively is not external, even if it is true. Treating it as external makes loop nogoods too weak, and the self-supporting loop is accepted.
- **Constraints have no head.** A constraint gives only the nogood $\{\mathbf{T}\beta\}$; it must not add a support nogood for any atom.
- **Blocking nogoods are not consequences.** When answer sets are enumerated with blocking nogoods, the nogoods learned from them hold only for the rest of the enumeration, not for the program.
- **Speed claims.** The speed of clasp and similar solvers is a measured property of their implementations and benchmarks, not a consequence of the algorithm; the worst case is exponential.

## Implementations

## History

Lin and Zhao (2004) showed that the completion with loop formulas characterizes answer sets and used a SAT solver with loop formulas added on demand. The clasp solver of Gebser, Kaufmann, Neumann and Schaub, first presented in 2007, put the completion and loop conditions inside a conflict-driven search with nogoods, in the style of CDCL. Gebser, Kaufmann and Schaub (2012) gave the full theory: the nogood characterization of answer sets, the algorithm CDNL-ASP and its proofs. The method is the basis of the clingo system.

## References
