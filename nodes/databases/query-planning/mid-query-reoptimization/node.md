---
tag: ZYAS1Y
kind: technique
slug: mid-query-reoptimization
name: Mid-query re-optimization
aliases:
- Kabra-DeWitt re-optimization
- progressive optimization
area: databases/query-planning
level: advanced
summary: "Count the rows at checkpoints while a plan runs, and optimize the rest of the query again when a count is far from its estimate, reusing the results already computed."
prereqs: [query-optimization, cardinality-estimation, pipelining-and-materialization]
see_also: [eddies, parametric-query-optimization, estimation-error-propagation, learned-query-optimization, materialized-view, selinger-join-enumeration, hash-join, index-nested-loop-join]
sources:
  - paper: doi:10.1145/276304.276315
    title: Navin Kabra and David J. DeWitt, Efficient mid-query re-optimization of sub-optimal query execution plans, Proceedings of ACM SIGMOD 1998, 106 to 117
    locator: statistics collectors in the plan, the decision to re-optimize at a materialization point, and the re-optimization of the rest of the plan with the intermediate result as a new input
  - paper: "Volker Markl, Vijayshankar Raman, David Simmen, Guy Lohman and Hamid Pirahesh, Robust query processing through progressive optimization, Proceedings of ACM SIGMOD 2004, 659 to 670"
    title: Robust query processing through progressive optimization
    locator: CHECK operators, validity ranges computed by sensitivity analysis during optimization, and re-optimization that reuses intermediate results, in a DB2 prototype measured on TPC-H
  - paper: doi:10.14778/2850583.2850594
    title: Viktor Leis, Andrey Gubichev, Atanas Mirchev, Peter Boncz, Alfons Kemper and Thomas Neumann, How good are query optimizers, really?, Proceedings of the VLDB Endowment 9(3) (2015), 204 to 215
    locator: Section 3 (the size of cardinality errors in real systems, the reason to check estimates at run time)
---

Mid-query re-optimization checks the estimates of a plan while the plan runs, and if they are badly wrong, optimizes the rest of the query again. A classic optimizer picks a plan once, from [cardinality estimates](/cardinality-estimation/) whose errors can grow fast with the number of joins (see [estimation error propagation](/estimation-error-propagation/)). Navin Kabra and David J. DeWitt (1998) added statistics collectors to the plan: at a point where an intermediate result is fully materialized, the system compares the observed size with the estimate, and if a new plan for the rest is expected to be much faster, it re-optimizes, using the materialized result as a new input with exact statistics. Markl et al. (2004) called their form progressive optimization (POP): the optimizer computes, for each checkpoint, a validity range of sizes for which the plan stays the best, and a CHECK operator triggers re-optimization when the observed size leaves the range. The decisions of both are heuristics. [Eddies](/eddies/) go further and change the order for each tuple.

## In plain words

Before a query runs, the database guesses how many rows each step will make, and picks a plan for those numbers. If a guess is very wrong, the plan can be very slow.

Mid-query re-optimization puts check points into the plan. At a check point, the database counts the rows that were really produced. If the count is close to the guess, the plan goes on. If it is far off, the database stops, plans the rest of the query again with the true count, and goes on with the new plan. The work done before the check point is kept and used by the new plan.

The best place for a check point is where a step has finished all its rows anyway, such as after a sort. There, stopping and changing the plan costs little.

## When it applies

- **Long queries with uncertain estimates.** Many joins, correlated predicates, parameter values unknown at compile time, or missing statistics. A query that runs for minutes can afford a second optimization.
- **Plans with materialization points.** A sort, the build side of a [hash join](/hash-join/), or a temporary table finishes its input before the next step uses it. There, the exact size is known and no output has been sent yet. See [pipelining and materialization](/pipelining-and-materialization/).
- **An optimizer that can take a partial result as input.** The new plan must use the materialized result as a table, with its exact size and maybe a histogram.
- **It does not apply** to short queries, where re-optimization costs more than it saves, or to fully pipelined plans that have already sent rows to the user, unless the system can avoid sending duplicates.

## The template

1. **Optimize and annotate.** Choose a plan as usual. For each candidate checkpoint, record the estimated size $\hat c$ and, for POP, a validity range $[l, h]$ of sizes for which the plan is still the best among the alternatives the optimizer compared there.
2. **Place checkpoints.** Put a statistics collector or a CHECK operator above the subplans whose estimates are uncertain, preferably at materialization points.
3. **Observe.** At run time, count the rows $c$ that reach the checkpoint, and collect other statistics if they are cheap, such as the number of distinct values or a histogram.
4. **Decide.** POP re-optimizes when $c \notin [l, h]$. Kabra and DeWitt re-optimize when the estimated gain of a new plan for the rest is large compared with the remaining cost and with the time to optimize again. Both tests use thresholds, which are heuristics.
5. **Re-optimize the rest.** Treat each materialized intermediate result as a base table with known statistics, like a [materialized view](/materialized-view/), and optimize the remaining query. The optimizer can still choose plans that do not use these results.
6. **Bound the loop.** Limit the number of re-optimizations per query, so that a query does not keep changing its plan.

**Validity ranges are intervals (proved, for linear costs).** At a checkpoint with size $c$, let $P$ be the chosen subplan above it and $P_1, \ldots, P_m$ the alternatives the optimizer compared with it. If each cost is an affine function of $c$, $\mathrm{cost}_X(c) = \alpha_X + \beta_X c$, then the set of $c \ge 0$ where $P$ is at least as cheap as every alternative is an interval.

*Proof.* For each $j$, the set $\{c \ge 0 : \mathrm{cost}_P(c) \le \mathrm{cost}_{P_j}(c)\}$ is $\{c \ge 0 : (\beta_P - \beta_{P_j}) c \le \alpha_{P_j} - \alpha_P\}$. A linear inequality in one variable defines a half-line, the whole line or the empty set, and each of these meets $[0, \infty)$ in an interval. The set where $P$ is best is the intersection of these $m$ intervals, which is an interval. $\square$

With costs that are not affine in $c$, for example $c \log c$ for a sort, the set can still be an interval when the differences of the costs are monotone in $c$, but this is not true in general. Also, the range says only that $P$ beats the alternatives that were compared at that point; it does not say that the whole plan is optimal, so it is a heuristic test.

## Classic examples

**A validity range.** A plan joins the result of a filter on Orders with Customers. The optimizer estimates $\hat c = 1000$ rows and picks an [index nested loop join](/index-nested-loop-join/) with a cost of $3c$ page reads (three reads per index probe). The alternative is a hash join with a cost of $20{,}000 + 0.01c$ (a scan of Customers plus a small cost per row). The nested loop join is cheaper when $3c \le 20{,}000 + 0.01c$, that is when $c \le 20{,}000 / 2.99 \approx 6689$, so the validity range is $[0, 6688]$. At $c = 1000$, the costs are 3000 and 20,010. If the filter really returns 50,000 rows, the CHECK operator above it sees that $c$ is out of range. The nested loop join would cost 150,000 reads, and the hash join 20,500, so re-optimization saves about 129,500 reads, minus the cost of optimizing again and of writing the filter result to a temporary table.

**Kabra and DeWitt.** In their system, statistics collectors were placed where the optimizer expected the largest errors and where collecting was cheap, and a re-optimization was done only if it was expected to improve the rest of the query by a large factor. They also used the new statistics to give the remaining operators better memory budgets. Their measurements showed large gains for queries with bad initial estimates and small overhead otherwise; these are measurements of their prototype.

**POP in DB2.** Markl et al. placed CHECK operators of several kinds: lazy checks at existing materialization points, and eager checks that materialize or buffer rows only to be able to check. They measured POP on TPC-H queries in a DB2 prototype, with large gains for queries whose estimates were wrong and a small overhead for the others.

## Variations

- **Lazy and eager checks.** A lazy check waits for a natural materialization point. An eager check is placed earlier, for example below a pipelined join, and buffers rows until it can decide; if the plan has already sent rows to the user, the new plan must remove the rows already sent.
- **Choice among precomputed plans.** Instead of optimizing again, prepare several plans at compile time and pick one at run time, as in the choose-plan operator of dynamic plans and in [parametric query optimization](/parametric-query-optimization/).
- **Robust plans.** Choose at compile time a plan whose cost grows slowly when the estimates are wrong, so that fewer checks fail. Later work computed bounding boxes around estimates for this.
- **Per-tuple adaptivity.** [Eddies](/eddies/) remove the fixed plan altogether and route each tuple, which needs no checkpoints but costs a decision per tuple.
- **Learning across queries.** The observed sizes can be fed back to the statistics, so the next query starts with better estimates, and [learned optimizers](/learned-query-optimization/) use them as training data.

## Pitfalls

- **Thrashing.** If the new estimates are also wrong, the query can re-optimize many times. Limit the number of rounds, and widen the thresholds after each one.
- **Duplicate rows.** A pipelined plan may have sent some result rows before a check fails. The new plan must not send them again.
- **Losing the work done.** A re-optimization that ignores the materialized results wastes the work before the checkpoint. Make the intermediate results available to the new plan.
- **Checking only one number.** The row count can be right while the distribution is wrong, for example when a join value is skewed. Collect distinct counts or histograms where they matter.
- **Too many checkpoints.** Each check costs time and some prevent pipelining. Place them where the estimates are most uncertain.

## Exercises

1. In the validity range example, find the range if the hash join cost is $40{,}000 + 0.5c$. (Answer: $3c \le 40{,}000 + 0.5c$ gives $c \le 16{,}000$.)
2. Give three cost functions of $c$, for one chosen plan and two alternatives, for which the set of $c$ where the chosen plan is best is not an interval. (Hint: costs that are not affine.)
3. A query has re-optimized once at a hash join build and the new plan has a sort. Where can the next check go, and what does it cost?
4. Explain why an eager check below a pipelined join must either buffer its input or track which result rows were sent, and compare the costs of the two.

## References
