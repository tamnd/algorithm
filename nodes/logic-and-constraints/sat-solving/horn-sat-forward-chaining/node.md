---
tag: JGNV5C
kind: algorithm
slug: horn-sat-forward-chaining
name: Horn-SAT forward chaining
aliases:
- Dowling-Gallier algorithm
- linear-time unit resolution for Horn formulas
area: logic-and-constraints/sat-solving
level: core
summary: Decide a Horn formula in linear time. Start with all variables false, and set a head true each time all the variables of its body are true; a goal clause with a true body means UNSAT.
solves: [horn-sat]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of clauses, s: the number of literal occurrences in the formula}
  time: {worst: Θ(n + m + s), best: Θ(n + m + s)}
  space: {extra: Θ(n + m + s)}
properties: {deterministic: true}
history:
  year: 1984
  people: [William F. Dowling, Jean H. Gallier]
  note: Published linear-time algorithms for the satisfiability of propositional Horn formulas, based on passing truth values forward from the facts.
prereqs: [horn-sat, horn-clause, unit-propagation]
see_also: [two-sat-algorithm, xor-gaussian-elimination, unit-resolution, datalog, logic-programming, sld-resolution, dpll]
sources:
  - paper: doi:10.1016/0743-1066(84)90014-1
    title: William F. Dowling and Jean H. Gallier, Linear-time algorithms for testing the satisfiability of propositional Horn formulae, Journal of Logic Programming 1(3), 267 to 284 (1984)
    locator: the whole paper (the counter-based algorithm and its linear bound)
  - paper: "Michel Minoux, LTUR: a simplified linear-time unit resolution algorithm for Horn formulae and computer implementation, Information Processing Letters 29(1), 1 to 12 (1988)"
    locator: the whole paper
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity (1994)
    locator: Chapter 4, Section 4.2 (Horn clauses and the polynomial-time algorithm for HORNSAT)
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2 (2022)
    locator: Section 7.2.2.2, Satisfiability (Horn clauses and their least models)
  - paper: "Alfred Horn, On sentences which are true of direct unions of algebras, Journal of Symbolic Logic 16(1), 14 to 21 (1951)"
    locator: the whole paper (the sentences now called Horn sentences)
---

Forward chaining decides [Horn-SAT](/horn-sat/) in time linear in the size of the formula. It starts with all variables false and keeps, for each clause, a count of the variables of its body that are still false. When a count reaches 0, the head of the clause must be true, so the algorithm sets it true and updates the counts. If a clause with no head gets a count of 0, the formula is unsatisfiable. Dowling and Gallier published this method in 1984. The [Horn-SAT](/horn-sat/) page covers the problem; this page covers the algorithm, which is [unit propagation](/unit-propagation/) made linear for [Horn clauses](/horn-clause/).

## In plain words

A Horn rule says "if these facts are all true, then this fact is true", or "these facts are never all true together". Some rules have no "if" part: they are plain facts.

Start with nothing known. Each time all the "if" parts of a rule are known, add its "then" part to what you know. Keep a counter on each rule with the number of its "if" parts that you do not know yet, so that you do not check the same rule again and again. When a counter reaches zero, the rule fires. If a rule of the second kind fires, the rules contradict each other. If no more rules fire, make the facts you know true and all other facts false. This makes every rule true, and it makes as few facts true as possible.

## The problem

The input is a CNF formula $F$ over $x_1, \ldots, x_n$ with $m$ clauses and $s = |F|$ literal occurrences, where each clause has at most one positive literal. Such a clause is a [Horn clause](/horn-clause/). We write it as an implication: the clause $(\neg x_1 \vee \neg x_2 \vee x_3)$ is the rule $x_1 \wedge x_2 \Rightarrow x_3$, with *body* $\{x_1, x_2\}$ and *head* $x_3$. A clause with no positive literal is a *goal clause*, $x_1 \wedge x_2 \Rightarrow \bot$, and a clause with an empty body is a *fact*. The output is UNSAT when $F$ has no model, and else a model. The algorithm returns the least model, the one with the fewest true variables.

## The algorithm

For each variable $v$, $occ[v]$ lists the clauses that hold $\neg x_v$, with one entry for each occurrence.

```pseudo id=main
FORWARD-CHAIN(F, n)
L1  for v ← 1 to n do val[v] ← false
L2  for each clause C do count[C] ← the number of negative literals of C
L3  Q ← a queue of the clauses C with count[C] = 0
L4  while Q is not empty do
L5      C ← take the first clause out of Q
L6      if C has no positive literal then return UNSAT
L7      h ← the variable of the positive literal of C
L8      if val[h] = false then
L9          val[h] ← true
L10         for each clause D in occ[h] do
L11             count[D] ← count[D] − 1
L12             if count[D] = 0 then put D in Q
L13 return val
```

Line L3 starts with the facts. A clause leaves the queue only when all the variables of its body are true. Line L6 then finds a goal clause whose body is all true, which no model can satisfy. Line L9 sets a head true at most once for each variable, and lines L10 to L12 update the counts of exactly the clauses that hold $\neg x_h$. The queue can be a stack: the order does not change the answer.

## Example

Take $n = 6$ and the seven clauses

| clause | as a rule | count at the start |
|---|---|---|
| $C_1 = (x_1)$ | $\Rightarrow x_1$ | 0 |
| $C_2 = (\neg x_1 \vee x_2)$ | $x_1 \Rightarrow x_2$ | 1 |
| $C_3 = (\neg x_1 \vee \neg x_2 \vee x_3)$ | $x_1 \wedge x_2 \Rightarrow x_3$ | 2 |
| $C_4 = (\neg x_3 \vee \neg x_4 \vee x_5)$ | $x_3 \wedge x_4 \Rightarrow x_5$ | 2 |
| $C_5 = (\neg x_2 \vee \neg x_5)$ | $x_2 \wedge x_5 \Rightarrow \bot$ | 2 |
| $C_6 = (\neg x_4 \vee x_1)$ | $x_4 \Rightarrow x_1$ | 1 |
| $C_7 = (\neg x_3 \vee x_6)$ | $x_3 \Rightarrow x_6$ | 1 |

The run, with the counts of $C_1, \ldots, C_7$ after each step:

| step | clause taken | action | counts | queue |
|---|---|---|---|---|
| start | | | 0 1 2 2 2 1 1 | $C_1$ |
| 1 | $C_1$ | $x_1 \gets$ true | 0 0 1 2 2 1 1 | $C_2$ |
| 2 | $C_2$ | $x_2 \gets$ true | 0 0 0 2 1 1 1 | $C_3$ |
| 3 | $C_3$ | $x_3 \gets$ true | 0 0 0 1 1 1 0 | $C_7$ |
| 4 | $C_7$ | $x_6 \gets$ true | 0 0 0 1 1 1 0 | empty |

The result is $x_1 = x_2 = x_3 = x_6 = 1$ and $x_4 = x_5 = 0$. Each clause is true: $C_4$, $C_5$ and $C_6$ are true because $x_4$ or $x_5$ is false. Each of the four true variables is true in each model, so this is the least model.

Now add the fact $C_8 = (x_4)$. The queue starts as $C_1, C_8$. The run sets $x_1$, then $x_4$, which brings $C_6$ to count 0. $C_2$ sets $x_2$. $C_6$ finds $x_1$ already true and changes nothing. $C_3$ sets $x_3$, which brings $C_4$ and $C_7$ to count 0. $C_4$ sets $x_5$, which brings the goal clause $C_5$ to count 0. $C_7$ sets $x_6$. Then $C_5$ leaves the queue, it has no positive literal, and line L6 returns UNSAT. The chain $x_1 \Rightarrow x_2 \Rightarrow x_3$, with $x_4$, gives $x_5$, and $x_2 \wedge x_5$ is forbidden.

## Correctness

Three invariants hold at line L4. Each count is the number of body variables of its clause that are still false. Each true variable is true in every model of $F$. Each clause enters the queue at most once, when its count reaches 0. The second invariant shows that UNSAT is right: a goal clause leaves the queue only when its whole body is true in every model. At line L13, a clause with a positive count has a false body variable, and a clause with count 0 has a true head. So the result is a model, and by the second invariant it lies below every model. The full proof is in the proof file below.

## Complexity

Lines L1 to L3 take $\Theta(n + m + s)$ time. Each clause enters the queue at most once, so line L5 runs at most $m$ times. Line L9 runs at most once for each variable, and then lines L10 to L12 run once for each occurrence of $\neg x_h$. Over the whole run this is at most $s$ steps. So the time is $\Theta(n + m + s)$ in the worst case on the [word RAM](/word-ram/), which is linear in the size of the input. The best case is the same, because lines L1 to L3 read the whole formula. The extra space is $\Theta(n + m + s)$ for the counts and the occurrence lists.

## Properties

- **Exact and deterministic.** The answer is always right, and the model is always the least model.
- **The least model.** The result is the smallest model in the order $\alpha \le \beta$ (each variable true under $\alpha$ is true under $\beta$). In [logic programming](/logic-programming/) and [Datalog](/datalog/) it is the meaning of a program without negation.
- **Incremental.** New facts or clauses can be added after a run: put the new clauses with count 0 in the queue and continue. The variables never change from true to false.
- **Unit resolution.** Each step is a step of [unit resolution](/unit-resolution/). The algorithm shows that unit resolution is complete for Horn formulas: a Horn formula is unsatisfiable exactly when unit resolution derives the empty clause.

## Variants and improvements

- **Other versions in the 1984 paper.** Dowling and Gallier give more than one linear-time algorithm. They describe the formula as a graph with a node for each variable, and pass truth values along the arcs.
- **LTUR.** Minoux's linear-time unit resolution of 1988 is the same idea with a simple implementation, and works on Horn formulas given as rules.
- **Dual Horn.** If each clause has at most one negative literal, flip the sign of each variable. The result is a Horn formula, and its least model gives the greatest model of the original formula.
- **Renamable Horn.** A formula is renamable Horn when flipping the signs of some variables makes it Horn. After the flips, each clause may have at most one positive literal, and this condition is a set of 2-clauses over one flip variable for each variable. So the flips can be found with the [2-SAT algorithm](/two-sat-algorithm/) in polynomial time.
- **Inside CDCL solvers.** [Unit propagation](/unit-propagation/) with [two watched literals](/two-watched-literals/) does a similar job on general clauses without counts. On a Horn formula, unit propagation from the empty assignment finds a conflict exactly when forward chaining returns UNSAT. Otherwise each clause that is not yet true has two or more open literals, so it has an open negative literal, and setting all open variables false gives a model.

## When to use it

Use it for any Horn formula: rule bases, Datalog programs without negation, type inference and dependency rules that only derive facts, and the Horn steps inside larger solvers. It is optimal up to a constant factor, because it reads the input once. For general CNF formulas it does not apply, because [SAT](/sat/) is NP-complete. For 2-CNF use the [2-SAT algorithm](/two-sat-algorithm/), and for parity constraints use [Gaussian elimination](/xor-gaussian-elimination/).

## Pitfalls

- **Scanning all clauses after each change.** A loop that rescans every clause until nothing changes is correct but takes $O(n \cdot s)$ time. Lines L10 to L12 touch only the clauses that hold $\neg x_h$.
- **Repeated literals.** If a clause holds $\neg x_v$ twice, line L2 counts 2, so $occ[v]$ must list the clause twice. With one entry the count never reaches 0, and the algorithm misses a forced head.
- **Testing the goal clauses only at the end.** Line L6 must test each clause that leaves the queue. A program that sets heads only and forgets goal clauses with count 0 returns a "model" that makes a goal clause false.
- **A clause with two positive literals.** The algorithm is only correct for Horn clauses. On $(x_1 \vee x_2)$ it would never fire the clause and would return all false, which is not a model. The Python version rejects such input.

## Implementations

## History

Horn clauses are named after Alfred Horn, who studied sentences of this form in 1951. Dowling and Gallier published the linear-time algorithms in 1984, and Minoux published the LTUR version in 1988. The same counting idea is used in the bottom-up evaluation of Datalog programs.

## References
