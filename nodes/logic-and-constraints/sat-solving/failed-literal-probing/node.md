---
tag: SWRBBT
kind: technique
slug: failed-literal-probing
name: Failed-literal probing
aliases:
- failed literal detection
- probing
- lifting
- necessary assignments
area: logic-and-constraints/sat-solving
level: advanced
summary: Set a literal, run unit propagation, and if this gives a conflict add the opposite literal as a unit; literals implied by both values of a variable are units too.
prereqs: [unit-propagation, conjunctive-normal-form]
see_also: [lookahead-sat, equivalent-literal-substitution, backbone, clause-subsumption, bounded-variable-elimination, dpll]
sources:
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 9 (Biere, Järvisalo and Kiesl, Preprocessing in SAT Solving), the section on failed literals, probing and hyper-binary resolution; Chapter 5 (Heule and van Maaren, Look-Ahead Based SAT Solvers), failed literals inside look-ahead
  - paper: "Jon W. Freeman, Improvements to propositional satisfiability search algorithms, PhD thesis, University of Pennsylvania, 1995"
    title: Improvements to propositional satisfiability search algorithms (POSIT)
    locator: the detection of failed literals by unit propagation inside a DPLL solver
  - paper: "Inês Lynce and João Marques-Silva, Probing-based preprocessing techniques for propositional satisfiability, ICTAI 2003, pages 105 to 110"
    title: Probing-based preprocessing techniques for propositional satisfiability
    locator: probing as preprocessing, with failed literals, necessary assignments from both values of a variable, and equivalences
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability, the look-ahead algorithm and its use of failed literals
---

Failed-literal probing finds unit clauses that are implied by a [CNF](/conjunctive-normal-form/) formula but not found by [unit propagation](/unit-propagation/) alone. Set a literal $l$ true and run unit propagation. If this gives a conflict, $l$ is a **failed literal**, so $\neg l$ holds in every model and can be added as a unit clause. If both $x$ and $\neg x$ fail, the formula is unsatisfiable. If neither fails, every literal that both runs set the same way is also implied; adding these is called **lifting** or finding necessary assignments. Each step keeps the set of models. Freeman's POSIT solver used failed literals inside DPLL in 1995; today probing runs as preprocessing, as inprocessing, and inside [look-ahead solvers](/lookahead-sat/).

## In plain words

Try a guess and see what follows from it by simple forced steps. If the forced steps lead to a contradiction, the guess was wrong, so the opposite is certain. Write the opposite down as a fact.

If neither guess for a variable leads to a contradiction, compare what each guess forced. Anything that both guesses force is certain too, because one of the two guesses must be right. Repeat this for all variables until nothing new appears. It costs one round of forced steps per guess, but it can fix many variables before the real search starts.

## When it applies

Use it as preprocessing or inprocessing on formulas where unit propagation is strong but not complete. Signals:

- the formula comes from circuits, planning or bounded model checking, where one wrong guess quickly forces a contradiction through long chains of implications;
- many variables are probably fixed in all models (a large [backbone](/backbone/)), and you want to find some of them cheaply;
- a look-ahead solver already runs unit propagation for both values of many variables, so the failed literals come for free.

## The template

Notation: $F$ has $n$ variables, $m$ clauses and $|F|$ literal occurrences. $\mathrm{UP}(F, \rho)$ is the closure of the partial assignment $\rho$ under unit propagation on $F$, or $\bot$ if a clause becomes false. $\rho_0 = \mathrm{UP}(F, \emptyset)$ holds the literals fixed so far.

```pseudo id=main
PROBE(F)
L1  repeat
L2      for each variable x not set in ρ_0 do
L3          A ← UP(F, ρ_0 ∪ {x});  B ← UP(F, ρ_0 ∪ {¬x})
L4          if A = ⊥ and B = ⊥ then return UNSAT
L5          else if A = ⊥ then add ¬x to ρ_0 and propagate      ▷ x is a failed literal
L6          else if B = ⊥ then add x to ρ_0 and propagate
L7          else add to ρ_0 each literal set in both A and B, and propagate   ▷ lifting
L8  until a full pass adds nothing   (return UNSAT if a propagation gives ⊥)
L9  return ρ_0
```

The output is a set of units. Adding them to $F$, removing satisfied clauses and deleting false literals gives a formula with the same models.

### Example

Let $F$ have the seven clauses
$$(\neg x_1 \vee x_2),\ (\neg x_1 \vee x_3),\ (\neg x_2 \vee \neg x_3 \vee x_4),\ (\neg x_1 \vee \neg x_4),\ (x_1 \vee x_5 \vee x_6),\ (\neg x_5 \vee x_7),\ (\neg x_6 \vee x_7).$$

Unit propagation alone sets nothing. Probe $x_1$: it sets $x_2$ and $x_3$, then $x_4$ by the third clause, and the fourth clause $(\neg x_1 \vee \neg x_4)$ is false. So $x_1$ fails and $\neg x_1$ is a unit. Now the fifth clause is $(x_5 \vee x_6)$. Probe $x_5$: it sets $x_7$. Probe $\neg x_5$: it sets $x_6$ by $(x_5 \vee x_6)$, then $x_7$. Both sides set $x_7$, so lifting adds $x_7$. No more literal fails, and PROBE returns $\{\neg x_1, x_7\}$.

### Why it is correct

**Lemma 1.** If $\mathrm{UP}(F, \rho) = \bot$, then no model of $F$ extends $\rho$. If $\mathrm{UP}(F, \rho) = \rho'$, every model of $F$ that extends $\rho$ extends $\rho'$.

*Proof.* Each step of unit propagation sets the last free literal of a clause whose other literals are false; every model that agrees with the current assignment must make that literal true. A clause with all literals false has no model that extends the assignment. $\square$

**Theorem.** Every literal that PROBE adds to $\rho_0$ is true in every model of $F$. If PROBE returns UNSAT, $F$ has no model.

*Proof.* By induction on the additions, assume every literal of $\rho_0$ is implied by $F$. Then every model of $F$ extends $\rho_0$, and so it extends $\rho_0 \cup \{x\}$ or $\rho_0 \cup \{\neg x\}$. Line L5: no model extends $\rho_0 \cup \{x\}$ by Lemma 1, so every model sets $x$ false. Line L6 is symmetric. Line L4: no model at all. Line L7: a model extends one of the two, so by Lemma 1 it extends $A$ or $B$, and a literal set the same way in both is true in it. The propagations after each addition are sound by Lemma 1. $\blacksquare$

The units are implied, so $F \wedge \rho_0$ has exactly the models of $F$. No reconstruction step is needed.

**Cost.** One call of UP costs $O(|F|)$ with watched literals. A pass makes $2n$ calls, and each pass except the last fixes a variable, so PROBE takes $O(n^2 |F|)$ time in the worst case. Practical tools probe only some literals (for example the roots of the binary implication graph) and stop after a time limit.

**Probing is incomplete.** The formula with all 8 clauses over $x_1, x_2, x_3$ is unsatisfiable, but no literal fails: setting $x_1$ leaves four binary clauses over $x_2, x_3$, none of which is unit.

## Classic examples

- **DPLL with failed literals.** POSIT and later look-ahead solvers probe the literals of the current node before they branch. A failed literal is set at once, which is cheaper than finding the conflict by search.
- **Preprocessing structured formulas.** On bounded model checking and planning formulas, probing often fixes many variables before the search.
- **Look-ahead solvers.** [Look-ahead solvers](/lookahead-sat/) such as march and kcnfs propagate both values of many variables to score them, and they get failed literals from the same work.
- **Backbone approximation.** Every unit found by probing is in the [backbone](/backbone/). Probing gives a cheap partial backbone before exact methods run.

## Variations

- **Equivalences from probing.** If $\mathrm{UP}(F, \rho_0 \cup \{x\})$ sets $y$ and $\mathrm{UP}(F, \rho_0 \cup \{\neg x\})$ sets $\neg y$, then $x \leftrightarrow y$ holds in every model. [Equivalent literal substitution](/equivalent-literal-substitution/) can then remove $y$.
- **Hyper-binary resolution.** If probing $l$ sets $y$ by a clause with more than two literals, the binary clause $(\neg l \vee y)$ is implied. Adding it makes later probes cheaper and can create cycles for equivalent literal substitution.
- **Double look-ahead.** Probe pairs of literals: if $\mathrm{UP}(F, \{l, l'\}) = \bot$, the binary clause $(\neg l \vee \neg l')$ is implied. This is stronger and costs more.
- **Tree-based probing.** Probe the literals along a spanning forest of the binary implication graph, so that the propagation from a parent can be reused for its children.
- **Vivification.** Probe the negations of the literals of a clause to find a shorter implied clause.

## Pitfalls

- **Cost.** A full pass is $2n$ propagations. Without a time limit, probing can take longer than solving.
- **Lifting needs care with the trail.** Compare only the literals set by the two runs that were not already in $\rho_0$, and undo each run fully before the next.
- **Added clauses that are not implied.** Learned clauses are implied by $F$, so units found with their help are implied too. Clauses added by steps that only keep satisfiability, such as blocked clause addition (the reverse of [blocked clause elimination](/blocked-clause-elimination/)), are not implied. A unit found with their help can remove models of the original $F$, so treat it as a satisfiability-preserving step, not as an implied fact.
- **Proof output.** A failed literal $\neg l$ is a RUP clause, so in a [DRAT](/drat-proof/) proof it can be added directly. A lifted literal is not RUP in general; add the two clauses $(\neg x \vee y)$ and $(x \vee y)$ first, which are RUP, then $y$.

## Exercises

1. Show that a lifted literal $y$ (set by both $x$ and $\neg x$) need not be found by unit propagation on $F \wedge \neg y$, and give the two RUP clauses that justify it in a DRAT proof.
2. Prove that if $F$ is a 2-CNF, probing all literals decides satisfiability, and give its running time.
3. Find a formula with $n$ variables on which PROBE needs $\Omega(n)$ passes of line L1.

## References
