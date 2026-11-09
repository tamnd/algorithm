---
tag: AM6WAY
kind: technique
slug: lookahead-sat
name: Lookahead
aliases:
- lookahead solving
- look-ahead SAT solver
- lookahead DPLL
area: logic-and-constraints/sat-solving
level: advanced
summary: At each DPLL node, try every free variable both ways with unit propagation; fix failed literals and autarkies, and branch on the variable that reduces the formula most on both sides.
prereqs: [dpll, unit-propagation]
see_also: [failed-literal-probing, autarky, cube-and-conquer, cdcl, k-sat, stalmarck-algorithm, branching-rule]
sources:
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 5 (Heule and van Maaren, Look-Ahead Based SAT Solvers), the lookahead procedure, the difference and mixing heuristics, preselection, and the additional reasoning
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms, Part 2, Addison-Wesley, 2022
    locator: Section 7.2.2.2, Algorithm L (satisfiability by lookahead) and its discussion
  - paper: "Jon W. Freeman, Improvements to propositional satisfiability search algorithms, PhD thesis, University of Pennsylvania, 1995"
    title: Improvements to propositional satisfiability search algorithms
    locator: the POSIT solver and its branching heuristics
  - paper: "Chu Min Li and Anbulagan, Heuristics based on unit propagation for satisfiability problems, IJCAI 1997"
    title: Heuristics based on unit propagation for satisfiability problems
    locator: the satz solver, lookahead on a preselected set of variables
  - paper: "Marijn Heule, Mark Dufour, Joris van Zwieten and Hans van Maaren, March_eq: implementing additional reasoning into an efficient look-ahead SAT solver, SAT 2004, LNCS 3542"
    title: "March_eq: implementing additional reasoning into an efficient look-ahead SAT solver"
    locator: tree-based lookahead, equivalence reasoning and preselection in march_eq
---

A lookahead SAT solver is a [DPLL](/dpll/) solver that works hard at every node of the search tree to choose the branching variable. For each free variable $x$ it sets $x$ to true, runs [unit propagation](/unit-propagation/), measures how much the formula shrank, and does the same for $x$ false. Three things can come out of one such test. If one side gives a conflict, that literal is *failed* and its negation is fixed. If one side shortens no open clause, its assignment is an [autarky](/autarky/) and is fixed. Otherwise the two reductions $d(x)$ and $d(\neg x)$ give the variable a score, and the solver branches on the best variable, so that both subtrees are small. POSIT, satz, kcnfs, OKsolver and the march solvers follow this design, and Knuth presents it as Algorithm L. Lookahead solvers are strong on small hard random [k-SAT](/k-sat/) formulas and give balanced splits, which makes them the cube phase of [cube-and-conquer](/cube-and-conquer/). On large structured formulas, [CDCL](/cdcl/) is usually faster.

## In plain words

Before you choose which question to ask next, try every possible question in your head. For each yes-or-no question, follow the easy consequences of "yes" and of "no". If one answer leads straight to a contradiction, you do not need to ask: the other answer must hold. If one answer touches only rules that it already meets, take it for free.

Otherwise, pick the question where both answers simplify the problem a lot. Then each branch of the search starts from a much smaller problem, and the search tree stays small.

## When it applies

- A backtracking search where each node is cheap to examine many times over, compared with the cost of a bad branch.
- Formulas without much structure for clause learning to use, such as random 3-SAT near the [threshold](/satisfiability-threshold/), where the search tree is the main cost.
- A need for a balanced split of the search space, as in cube-and-conquer and parallel search.

Lookahead is a poor fit for formulas with millions of clauses: every node costs about $2n$ propagations.

## The template

Notation: $F$ is a CNF formula with $n$ variables, $m$ clauses and size $|F|$, the total number of literal occurrences. $\alpha$ is the current partial assignment. UP$(F, \alpha)$ is the closure of $\alpha$ under unit propagation, or *fail* if a clause becomes false. For a literal $l$, $\alpha_l = $ UP$(F, \alpha \cup \{l\})$.

The *reduction* $d(l)$ is the number of clauses that $\alpha_l$ shortens but does not satisfy: clauses not satisfied by $\alpha_l$ that contain a variable set by $\alpha_l$ but not by $\alpha$.

```pseudo id=main
LOOKAHEAD-DPLL(F, α)
L1  α ← UP(F, α); if it fails, return UNSAT
L2  if α satisfies F, return SAT with α
L3  for each free variable x of the clauses that α does not satisfy
L4      α_x ← UP(F, α ∪ {x}); α_¬x ← UP(F, α ∪ {¬x})
L5      if both fail, return UNSAT
L6      if α_l fails for one literal l, set α ← α_¬l and go to L2
L7      compute d(x) and d(¬x)
L8      if d(l) = 0 for a literal l, set α ← α_l and go to L2
L9  x ← a variable with the largest H(x) = 1024·d(x)·d(¬x) + d(x) + d(¬x)
L10 for l in (the side of x with the smaller d, then the other side)
        if LOOKAHEAD-DPLL(F, α ∪ {l}) is SAT, return SAT
L11 return UNSAT
```

The holes are the measure $d$, the mixing function $H$, the set of variables tried at L3, and the order of the branches at L10. The rest is fixed.

**Walk-through.** L1 and L2 are the plain DPLL steps. L3 to L8 form the *lookahead phase*. Each failed literal or autarky fixes a variable, and the phase starts again, because the old scores are out of date. When the phase ends without a fixed variable, every free variable has two positive reductions, and L9 picks the best. L10 is the *direction heuristic*: it tries first the side that changes the formula less, which is more often satisfiable.

### Why it is correct

**Lemma 1 (failed literal).** If UP$(F, \alpha \cup \{l\})$ fails, then every model of $F$ that extends $\alpha$ sets $l$ false.

*Proof.* Every literal that unit propagation adds is implied by $F$, $\alpha$ and $l$. A false clause means $F \wedge \alpha \wedge l$ has no model. $\square$

So L5 is right to return UNSAT, and L6 does not lose a model.

**Lemma 2 (autarky).** If $\alpha_l$ does not fail and $d(l) = 0$, then $F$ has a model extending $\alpha$ if and only if it has one extending $\alpha_l$.

*Proof.* One direction is clear. For the other, let $\tau$ be the part of $\alpha_l$ that is new. Since $d(l) = 0$, every clause that contains a variable of $\tau$ is satisfied by $\alpha$ or by $\tau$. Take a model $\sigma \supseteq \alpha$ of $F$ and change it to agree with $\tau$. A clause without a variable of $\tau$ keeps its value. A clause with a variable of $\tau$ is satisfied by $\alpha$, which did not change, or by $\tau$. So the new assignment is a model that extends $\alpha_l$. $\square$

**Theorem.** LOOKAHEAD-DPLL$(F, \emptyset)$ returns SAT with a model of $F$ if $F$ is satisfiable, and UNSAT otherwise. It terminates.

*Proof.* By Lemmas 1 and 2, the steps L1, L5, L6 and L8 keep the set of models that extend $\alpha$ nonempty exactly when it was nonempty before. The branch at L10 covers both values of $x$. A SAT answer at L2 is a model. Each step at L6 or L8 sets at least one more variable, and each branch sets one, so the recursion is finite. $\blacksquare$

### Cost

One lookahead on a literal is one unit propagation, $O(|F|)$ with counters. A lookahead phase does at most $2n$ of them between two fixed variables, and at most $n$ variables are fixed, so a node costs $O(n^2 |F|)$ in the worst case and usually $O(n |F|)$. The point is the trade: a node costs far more than in CDCL, and in return the tree has far fewer nodes. Solvers bring the cost down by *preselection*: they look ahead only on a subset of the variables chosen by a cheaper estimate.

### A worked example

Take 11 clauses over $x_1, \ldots, x_5$:
$$\begin{aligned}
&(x_1 \vee \neg x_3 \vee \neg x_4),\ (x_1 \vee x_2 \vee x_5),\ (x_2 \vee \neg x_5),\ (\neg x_1 \vee x_2 \vee x_5),\ (x_1 \vee \neg x_4 \vee \neg x_5),\ (x_2 \vee \neg x_3),\\
&(x_2 \vee x_3 \vee x_5),\ (\neg x_1 \vee x_3 \vee x_4),\ (x_2 \vee \neg x_4 \vee \neg x_5),\ (x_1 \vee x_4 \vee x_5),\ (\neg x_1 \vee x_3 \vee \neg x_5).
\end{aligned}$$

- The lookahead on $x_1$ gives no result. On $x_2$, the side $\neg x_2$ forces $\neg x_5$ and $\neg x_3$, and then $(x_2 \vee x_3 \vee x_5)$ is false. So $\neg x_2$ is a failed literal and $x_2$ is fixed at L6. This satisfies six clauses.
- The phase starts again on the other five clauses. The reductions and scores are below.

| $x$ | $d(x)$ | $d(\neg x)$ | $H(x)$ |
|---|---|---|---|
| $x_1$ | 2 | 3 | 6149 |
| $x_3$ | 1 | 2 | 2051 |
| $x_4$ | 2 | 2 | 4100 |
| $x_5$ | 2 | 1 | 2051 |

- L9 picks $x_1$, and L10 tries $x_1$ true first, since $d(x_1) = 2 < 3$. In the child, two clauses are left: $(x_3 \vee x_4)$ and $(x_3 \vee \neg x_5)$. The lookahead on $x_3$ shortens nothing, so $x_3$ is fixed as an autarky at L8, and L2 returns the model $x_1 = x_2 = x_3 = 1$, $x_4 = x_5 = 0$.

The whole search uses 2 nodes, 7 lookaheads, 1 failed literal and 1 autarky. The tests check these numbers, check the solver against brute force on 300 random formulas with up to 12 variables, and check that the variables fixed by each lookahead phase keep satisfiability.

## Classic examples

- **Failed-literal probing as preprocessing.** One lookahead phase at the root, with no branching, is [failed-literal probing](/failed-literal-probing/). CDCL solvers run it as a preprocessing or inprocessing step.
- **Random 3-SAT.** On random formulas near the threshold there is little structure to learn, and the size of the search tree decides the run time. Here the product rule pays off, and lookahead solvers such as kcnfs and march were built for this case. The Handbook chapter by Heule and van Maaren reports their results.
- **Cube-and-conquer.** A lookahead solver splits the formula into many cubes, and a CDCL solver solves each one; see [cube-and-conquer](/cube-and-conquer/). The balanced splits of the product rule are what makes the cubes of similar difficulty.
- **Stålmarck's method.** The dilemma rule of [Stålmarck's algorithm](/stalmarck-algorithm/) tries both values of a variable and keeps what both branches agree on. This is a lookahead that keeps the common consequences instead of choosing a branch.

## Variations

- **Reduction measures.** The simplest $d(l)$ counts variables set by propagation. The march solvers count new binary clauses, weighted by the occurrences of their literals, and kcnfs uses a measure called the backbone search heuristic. All of them estimate how much easier the formula becomes.
- **Mixing functions.** The product $d(x) \cdot d(\neg x)$ favors balanced reductions: with a fixed total, the smallest product comes from the most uneven split. The term $d(x) + d(\neg x)$ breaks ties, and the factor 1024 lets the product dominate. This form appears in the Handbook chapter on lookahead solvers. For $k$-way branching, products of more factors are used.
- **Preselection.** satz looks ahead only on variables that pass a cheap test; march ranks variables by an estimate of their reduction and looks ahead on a fraction of them.
- **Necessary assignments.** If both $\alpha_x$ and $\alpha_{\neg x}$ set a literal $y$, then $y$ holds in every model that extends $\alpha$. Stålmarck's dilemma rule is built on this.
- **Local learning.** If $\alpha_l$ sets $y$, the binary clause $(\neg l \vee y)$ is implied by $F$ and $\alpha$. Adding such clauses speeds up later lookaheads.
- **Double lookahead.** When a lookahead reduces a lot, run a second level of lookahead under it to find more failed literals.
- **Tree-based lookahead.** Order the literals along the binary implication graph, so that the propagation of an implied literal is shared by the literals that imply it.

## Pitfalls

- **Stale scores.** After a failed literal or an autarky fixes a variable at L6 or L8, the old reductions are wrong. Go back to L2, not on to L9.
- **Autarky without the conflict check.** A side with $d(l) = 0$ can be taken only if its propagation did not fail. Check L5 and L6 before L8.
- **The sum alone.** Branching on the largest $d(x) + d(\neg x)$ can pick a variable with a large reduction on one side and almost none on the other. One subtree is then nearly as hard as the whole formula. The product avoids this.
- **Cost on large formulas.** Without preselection, each node costs about $2n$ propagations, which is too much for formulas with millions of variables.
- **The direction heuristic and UNSAT formulas.** On an unsatisfiable subtree, both branches must be searched, so the order at L10 does not change the work there. It matters only for satisfiable formulas.

## Exercises

1. Prove that if both $\alpha_x$ and $\alpha_{\neg x}$ set $y$ to true, then $F \wedge \alpha$ implies $y$.
2. Show that a pure literal $l$ (one whose negation does not occur in the open clauses) has $d(l) = 0$, so L8 subsumes the pure literal rule.
3. For fixed $d(x) + d(\neg x) = s$, show that $d(x) \cdot d(\neg x)$ is largest when the two are equal. Why is this good for the size of the search tree?
4. Give a formula where a lookahead phase finds a failed literal only after another failed literal was fixed, so the restart at L6 matters.
5. Estimate the size of the search tree when every branch reduces the number of free variables by $a$ on one side and $b$ on the other, and compare $(a, b) = (1, 9)$ with $(5, 5)$.

## References
