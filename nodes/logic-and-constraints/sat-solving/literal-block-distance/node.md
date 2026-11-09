---
tag: DRJEJQ
kind: concept
slug: literal-block-distance
name: Literal block distance
aliases:
- LBD
- glue
- glue level
area: logic-and-constraints/sat-solving
level: research
summary: "The number of distinct decision levels among the literals of a learned clause. CDCL solvers use it to rank learned clauses for deletion and to time restarts."
prereqs: [cdcl, clause-learning]
see_also: [clause-database-reduction, clause-database, restarts, first-uip, implication-graph, vsids, phase-saving]
sources:
  - paper: "Gilles Audemard and Laurent Simon, Predicting learnt clauses quality in modern SAT solvers, Proceedings of the 21st International Joint Conference on Artificial Intelligence (IJCAI 2009), 2009"
    locator: pages 399 to 404 (the definition of LBD, glue clauses, the deletion schedule, and the comparison on the SAT 2007 industrial instances)
  - paper: doi:10.1007/978-3-642-33558-7_11
    title: Gilles Audemard and Laurent Simon, Refining restarts strategies for SAT and UNSAT, Principles and Practice of Constraint Programming (CP 2012), Lecture Notes in Computer Science 7514, 2012
    locator: pages 118 to 126 (restarts driven by the recent and the global average LBD)
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 4, Conflict-Driven Clause Learning SAT Solvers, by Marques-Silva, Lynce and Malik (clause deletion policies)
---

The literal block distance (LBD) of a clause, under the current assignment of a [CDCL](/cdcl/) solver, is the number of distinct decision levels among its literals. Audemard and Simon defined it in 2009 to measure how useful a [learned clause](/clause-learning/) is likely to be, and called a clause with LBD 2 a glue clause. LBD is the main score that modern solvers use to choose which learned clauses to delete and when to restart. Its value as a predictor is an empirical finding; the exact facts are about what it counts.

## In plain words

When a solver makes a guess, a chain of forced values follows from it. Call the guess and its chain one block. A learned clause mentions some variables, and each of them belongs to some block. The LBD is how many different blocks the clause touches.

A clause that touches only a few blocks links a few guesses together. Such a clause tends to become forced again soon, because the solver only needs to repeat a few guesses for it to act. A clause that touches many blocks needs many guesses at once before it can do anything. Solvers keep the clauses with few blocks and throw away many of the others.

## The idea

Fix a clause $C$ whose literals are all assigned, none at level 0, and write $\mathrm{level}(x)$ for the [decision level](/cdcl/) of the variable of literal $x$. Then

$$\mathrm{LBD}(C) = \left|\{\mathrm{level}(x) : x \in C\}\right|.$$

The literals of $C$ fall into blocks, one block per level, and the LBD is the number of blocks. Solvers compute it when they learn the clause, and solvers of the glucose line recompute it when the clause takes part in a later conflict analysis, keeping the new value if it is smaller.

The following facts hold exactly.

1. **Bounds.** $1 \le \mathrm{LBD}(C) \le |C|$, and $\mathrm{LBD}(C)$ is at most the current decision level. Each block is nonempty and holds at least one literal, and there is at most one block per level from 1 to the current level.

2. **Learned clauses.** Let $C$ be an [asserting clause](/first-uip/) learned at a conflict at level $d$, with backjump level $b$. Exactly one literal of $C$ is at level $d$, so $\mathrm{LBD}(C) = 1 + k$, where $k$ is the number of distinct levels among the other literals. So $\mathrm{LBD}(C) = 1$ exactly when $C$ is a unit clause. And $\mathrm{LBD}(C) = 2$ exactly when $C$ has at least two literals and all literals other than the asserting one are at level $b$.

3. **Glue.** If $\mathrm{LBD}(C) = 2$ at learning time, then after the backjump to level $b$ the asserting literal is assigned at level $b$, so all literals of $C$ are at level $b$. The clause joins, or glues, the new literal to one existing block. This is the case that gave glue clauses their name.

4. **Dependence on the trail.** LBD is not a property of the clause alone. The same clause under another trail can have another LBD. For example, the clause $(u \vee v_1 \vee v_2)$ has LBD 3 if $u$, $v_1$, $v_2$ are false at levels 5, 2 and 3, and LBD 2 if they are false at levels 5, 2 and 2. This is why the stored value is an estimate that is updated over time.

5. **Cost.** With an array of stamps indexed by level, one pass over the clause computes the LBD in $O(|C|)$ time: for each literal, mark its level with a fresh stamp and count the levels not yet marked.

Why a small LBD should predict usefulness is not proved. Audemard and Simon argue as follows: literals of one level are linked by propagation from one decision, so a clause with small LBD needs few decisions to become unit or false again. They support the claim with measurements, given below.

**The measured result.** In the 2009 paper, the solver glucose ranked learned clauses by LBD and deleted half of them every $20000 + 500x$ conflicts, where $x$ is the number of deletions done so far, keeping the clauses with the smallest LBD. It used Luby restarts with a unit of 32 conflicts. On the 234 industrial instances of the SAT 2007 competition, it solved 176, compared with about 140 for RSat and for MiniSat and 153 for PicoSAT.

## Examples

**The running example of CDCL.** Take the clauses $C_1 = (x_1 \vee x_2)$, $C_2 = (x_1 \vee x_3 \vee x_7)$, $C_3 = (\neg x_2 \vee \neg x_3 \vee x_4)$, $C_4 = (\neg x_4 \vee x_5 \vee x_8)$, $C_5 = (\neg x_4 \vee x_6 \vee x_9)$ and $C_6 = (\neg x_5 \vee \neg x_6)$, and the decisions $\neg x_7$, $\neg x_8$, $\neg x_9$, $\neg x_1$ at levels 1 to 4.

| learned clause | levels of its literals | LBD | backjump level |
|---|---|---|---|
| $(\neg x_4 \vee x_8 \vee x_9)$ | $x_4$: 4, $x_8$: 2, $x_9$: 3 | 3 | 3 |
| $(x_1 \vee x_4 \vee x_7)$ | $x_1$: 4, $x_4$: 3, $x_7$: 1 | 3 | 3 |

The first clause comes from the conflict at level 4. After the backjump, $\neg x_4$ is assigned at level 3, the decision $\neg x_1$ is made again at level 4, and the second conflict learns the second clause.

**A glue clause.** Suppose a conflict at level 7 learns the clause $(u \vee v_1 \vee v_2 \vee v_3 \vee v_4)$, where $u$ is false at level 7 and all four $v_i$ are false at level 3. The clause has five literals but LBD 2. After the backjump to level 3, $u$ becomes true at level 3, and all five literals are now at level 3.

**Not the same as length.** A clause $(x \vee y)$ whose two literals are false at levels 2 and 9 has length 2 and LBD 2, and a clause of length 10 with all literals except one at level 4 also has LBD 2. Ranking by LBD and ranking by length can disagree in both directions.

## Where it is used

- **Clause deletion.** [Clause database reduction](/clause-database-reduction/) sorts learned clauses by LBD and deletes the worst part. Many solvers keep clauses with very small LBD, such as LBD at most 2, for ever, and keep clauses with LBD below a second bound for longer than the rest.
- **Restarts.** The glucose [restart](/restarts/) rule compares the mean LBD of the recent learned clauses with the mean of all of them, and restarts when the recent clauses are worse.
- **Sharing in parallel solvers.** Solvers that run several searches at once often share only learned clauses with small LBD, to limit traffic. See [parallel portfolio SAT](/parallel-portfolio-sat/).
- **Combined scores.** Some solvers combine LBD with clause activity or with length. Recursive [clause minimization](/clause-minimization/) keeps a literal of every level of the clause, so it shortens the clause but leaves its LBD as it was.

## References
