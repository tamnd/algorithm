---
tag: PA8RXC
kind: technique
slug: pure-literal-elimination
name: Pure literal elimination
aliases:
- pure literal rule
- affirmative-negative rule
- monotone literal fixing
area: logic-and-constraints/sat-solving
level: intro
summary: Set each pure literal (one whose complement never occurs) to true and delete the clauses it satisfies. It keeps satisfiability, but not every model.
prereqs: [literal, conjunctive-normal-form]
see_also: [dpll, davis-putnam-elimination, unit-propagation, autarky, blocked-clause-elimination, bounded-variable-elimination, qbf, model-counting]
sources:
  - paper: doi:10.1145/321033.321034
    title: Martin Davis and Hilary Putnam, A computing procedure for quantification theory, Journal of the ACM 7(3), 1960
    locator: pages 201 to 215 (rule II, the affirmative-negative rule)
  - paper: doi:10.1145/368273.368557
    title: Martin Davis, George Logemann and Donald Loveland, A machine program for theorem-proving, Communications of the ACM 5(7), 1962
    locator: pages 394 to 397 (the affirmative-negative rule in the search procedure)
  - paper: "Burkhard Monien and Ewald Speckenmeyer, Solving satisfiability in less than 2^n steps, Discrete Applied Mathematics 10(3), 1985, pages 287 to 295"
    locator: autark assignments, of which a pure literal is the simplest case
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 3, Complete Algorithms, by Darwiche and Pipatsrisawat (the pure literal rule in DPLL), and the chapter on minimal unsatisfiability and autarkies by Kleine Büning and Kullmann
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability (pure literals and autarkies)
---

Pure literal elimination is the simplification rule that sets a [literal](/literal/) to true when its complement occurs in no clause of the formula, and deletes the clauses that contain it. Setting such a pure literal true satisfies its clauses and falsifies no literal anywhere else, so the formula keeps its satisfiability: the new formula is satisfiable exactly when the old one is. The rule is rule II of Davis and Putnam (1960) and part of [DPLL](/dpll/), but it does not keep all models, so it is wrong for [model counting](/model-counting/), and [CDCL](/cdcl/) solvers leave it out of the search.

## In plain words

Suppose some value appears in the rules only one way: some rules say "this switch on would be fine", and no rule ever wants it off. Then put the switch on. Every rule that mentions it is now obeyed, and no rule gets worse, because no rule wanted it off. Strike those rules out.

Striking rules out can make more switches appear only one way, so repeat the step. If the rules could be obeyed before, they still can. But some settings that obeyed all rules are now lost, because the switch is no longer free to be off. So use the step to answer "is there a solution?", not "how many solutions are there?".

## When it applies

- The formula is in [CNF](/conjunctive-normal-form/), and the task is to decide satisfiability or to find one model. The rule also keeps the optimum of [MaxSAT](/max-sat/), since making a pure literal true can falsify no clause.
- The formula is fixed. If clauses can be added later, as in [incremental SAT](/incremental-sat/) or in CDCL with learned clauses, a literal that is pure now may not stay pure.
- All models are not needed. For counting or enumeration, the rule loses models.

## The template

The pure literals are found with occurrence counts. $\mathrm{occ}[u]$ is the number of live clauses that hold the literal $u$.

```pseudo id=main
PURE-LITERALS(F)                              ▷ returns the fixed literals and the rest of F
L1  compute occ[u] for every literal u; P ← empty list
L2  S ← stack of every literal u with occ[u] > 0 and occ[¬u] = 0
L3  while S is not empty do
L4      u ← POP(S)
L5      if the variable of u is fixed or occ[u] = 0 or occ[¬u] > 0 then continue
L6      append u to P                           ▷ hole CHOICE: fix u, or only record it
L7      for each live clause C with u ∈ C do
L8          delete C
L9          for each q ∈ C do
L10             occ[q] ← occ[q] − 1
L11             if occ[q] = 0 and occ[¬q] > 0 then PUSH(S, ¬q)
L12 return P and the live clauses
```

**Why it is safe.** Let $u$ be pure in $F$, let $F_u$ be the clauses that contain $u$, and let $F' = F \setminus F_u$.

*Lemma.* $F$ is satisfiable if and only if $F'$ is. Every model $\beta$ of $F'$, changed to make $u$ true, is a model of $F$.

*Proof.* $F' \subseteq F$, so a model of $F$ is a model of $F'$. Let $\beta$ satisfy $F'$, and let $\beta'$ be $\beta$ with $u$ true. The clauses of $F_u$ hold $u$, so $\beta'$ satisfies them. A clause of $F'$ does not hold $u$ (else it is in $F_u$) and does not hold $\neg u$ (since $u$ is pure), so its value does not depend on the variable of $u$, and $\beta'$ satisfies it as $\beta$ does. $\blacksquare$

By induction over the literals of $P$, in the order of line L6, $F$ is satisfiable exactly when the returned clauses are, and a model of them with the literals of $P$ made true is a model of $F$. Each literal of $P$ is pure in the formula that is live when it is fixed, because line L5 checks the counts at that moment. In terms of [autarkies](/autarky/): the set of literals $P$ is an autark assignment, one that satisfies every clause it touches.

**Cost.** Line L1 takes $O(|F|)$. Each clause is deleted at most once, and each deletion costs its length at lines L9 to L11, so the loop costs $O(|F|)$ in total, and a literal is pushed at most twice. So the whole rule, iterated until no pure literal is left, runs in $O(|F| + n)$ time.

**Example.** Let $F$ be $C_1 = \{x_4, \neg x_1\}$, $C_2 = \{x_4, x_2\}$, $C_3 = \{x_1, x_3\}$, $C_4 = \{x_1, \neg x_2\}$, $C_5 = \{\neg x_3, x_2\}$. Take the pure literal with the smallest variable first.

| step | pure literals now | fixed | clauses deleted | live clauses |
|---|---|---|---|---|
| 1 | $x_4$ | $x_4$ | $C_1, C_2$ | $C_3, C_4, C_5$ |
| 2 | $x_1$ | $x_1$ | $C_3, C_4$ | $C_5$ |
| 3 | $x_2$, $\neg x_3$ | $x_2$ | $C_5$ | none |

The formula is satisfiable, and every assignment with $x_1 = x_2 = x_4 = 1$ is a model; $x_3$ is free. Brute force over the 16 assignments shows that $F$ has 3 models: these two and $x_1 = 1, x_2 = 0, x_3 = 0, x_4 = 1$, which the rule lost at step 3. Step 2 shows the iteration: $x_1$ became pure only after $C_1$ was deleted.

## Classic examples

- **[DPLL](/dpll/).** Davis, Logemann and Loveland apply the rule at each node of the search, after [unit propagation](/unit-propagation/). It never causes a backtrack, because the branch with the pure literal false is never needed.
- **[Davis-Putnam elimination](/davis-putnam-elimination/).** Eliminating a variable that has only positive occurrences produces no resolvent, so the pure literal rule is the special case of resolution elimination with an empty side.
- **[Bounded variable elimination](/bounded-variable-elimination/) and [blocked clause elimination](/blocked-clause-elimination/).** In preprocessors, every clause with a pure literal is blocked on it, and its variable is eliminated at no cost. Preprocessors remove such clauses as part of these more general rules.
- **[QBF](/qbf/) solvers.** In a quantified formula, an existential pure literal is set true and a universal pure literal is set false; both keep the truth value of the formula.

## Variations

- **Autarky reduction.** A pure literal is an autarky of size one. In general, a partial assignment that satisfies every clause it touches can be applied without changing satisfiability. Monien and Speckenmeyer used autarkies to get a $k$-SAT algorithm faster than $2^n$.
- **Pure literals in the current subformula.** Inside a search, purity is checked against the clauses not yet satisfied by the partial assignment, so more literals are pure deeper in the tree. DPLL implementations do this with counters of unsatisfied clauses per literal.
- **Static preprocessing only.** CDCL solvers run the rule, if at all, as a preprocessing step on the input, with a list of frozen variables that the user may still mention later.

## Pitfalls

- **Counting or enumerating models.** The rule keeps satisfiability but loses models, as the example shows. A [model counter](/model-counting/) must not use it.
- **Learned clauses.** A learned clause can hold $\neg u$ for a literal $u$ that is pure in the input. Treating $u$ as pure in the current clause database is sound, since learned clauses are implied, but solvers would need to track occurrences in all clauses, which costs more than the rule saves.
- **Incremental use.** If the user may add clauses later, a literal fixed as pure may become impure, and the fixed value can make a satisfiable extension look unsatisfiable. Freeze the variables that may appear again.
- **Stale counts.** Purity must be checked when the literal is taken from the stack (line L5): a literal pushed as pure can lose its last occurrence or its variable can be fixed meanwhile.
- **Purity in the satisfied clauses.** In a search, a clause already satisfied does not count. Counting it makes the rule find fewer pure literals; ignoring satisfied clauses is correct because they stay satisfied below the node.

## Exercises

1. Prove that if $F$ is unsatisfiable, then no clause that contains a pure literal of $F$ is in a [minimal unsatisfiable subset](/minimal-unsatisfiable-subset/) of $F$.
2. Show that for each $n$ there is a formula on $n$ variables where the iterated rule fixes all $n$ variables one at a time, each new pure literal appearing only after the previous deletions.
3. Show that the pure literal rule keeps the optimum of MaxSAT, and give an example where it does not keep the set of optimal assignments.
4. Prove that a set of literals $P$, built by iterating the rule, satisfies every clause of $F$ that contains a variable of $P$.

## References
