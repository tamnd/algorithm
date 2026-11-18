---
tag: SJBPXM
kind: algorithm
slug: cascades-framework
name: Cascades optimization framework
aliases:
- Cascades optimizer
- memo-based top-down optimization
- Cascades search
area: databases/query-planning
level: advanced
summary: "A rule-driven top-down optimizer that explores groups of equivalent expressions in a memo with tasks, promises and branch-and-bound pruning."
solves: [query-optimization]
model: word-ram
complexity:
  vars: {n: the number of relations in the join model of this page}
  time: {exploration: "O(4^n)", search without pruning: "O(3^n)"}
  space: {memo: "O(3^n)"}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 1995
  people: [Goetz Graefe]
  note: Described in the IEEE Data Engineering Bulletin as the successor of the Volcano optimizer generator.
prereqs: [volcano-optimizer-generator, depth-first-branch-and-bound]
see_also: [volcano-optimizer-generator, dphyp, dpccp, interesting-orders, relational-algebra-equivalences, subquery-unnesting, eager-aggregation, query-optimization]
sources:
  - paper: "Goetz Graefe, The Cascades framework for query optimization, IEEE Data Engineering Bulletin 18(3) (1995), 19 to 29"
    title: The Cascades framework for query optimization
    locator: "the memo of groups, the rules with patterns and promises, the search by tasks, and the comparison with the Volcano search"
  - paper: "Goetz Graefe and William J. McKenna, The Volcano optimizer generator: extensibility and efficient search, Proceedings of ICDE 1993, 209 to 218"
    title: "The Volcano optimizer generator: extensibility and efficient search"
    locator: "the earlier search with a look-up table, physical properties, enforcers and a cost limit, which Cascades refines"
---

Cascades is a framework for query optimizers that Goetz Graefe described in 1995 as the successor of the [Volcano optimizer generator](/volcano-optimizer-generator/). Like Volcano, it keeps equivalent logical expressions in groups of a memo and searches top down for the cheapest plan of a group with a required physical property, with memoization and a cost limit. The difference is the control of the search. Volcano applies all transformation rules first and only then searches for plans. Cascades works with a stack of small tasks: it explores a group only when a goal needs it, applies the rules of each expression in the order of their *promise*, and optimizes an input group only with an upper bound that comes from the best plan so far. Rules, enforcers and promises are objects that the builder of an optimizer supplies. Many industrial optimizers follow this design.

## In plain words

An optimizer must pick a cheap way to run a query among many equivalent ones. Cascades keeps a notebook: on each page it writes a group of query parts that give the same result, and the best known way to compute that group with the needed sort order.

The work is a to-do list. A typical item says: find the best way to compute this group, sorted, for less than this cost. To do it, the optimizer first writes all equivalent forms of the group into the notebook, then tries each method, starting with the one that looks most promising, and adds new items for the inputs. If the inputs already cost more than the best answer so far, it drops the method. When all items for the group are done, it writes the winner, or notes that nothing was cheap enough.

## The problem

The input is a logical query and a required physical property; the output is a physical plan of least cost that gives the property. A *goal* is a pair of a group and a required property, with an upper bound on the cost. A *winner* of a goal is its best plan; a *failure* records that no plan is below a bound.

The code of this page uses the join model of the Volcano page. Relations $R_0, \ldots, R_{n-1}$ share one join attribute $k$, a group is a set of relations, and the rules are join commutativity and associativity. The property is the sort order on $k$. The algorithms are TableScan, IndexScan (sorted, if $R$ has an index on $k$), HashJoin, MergeJoin (both inputs sorted, output sorted) and NestedLoop (keeps the order of the outer input), and the enforcer is Sort. Their local costs are in the code.

## The algorithm

```pseudo id=main
CASCADES(query, required property p)
L1  put the query in the memo and push O_GROUP(the group of the query, p, ∞)
L2  while the stack is not empty, pop the top task and run it
L3  return the plan of the winner of (the group of the query, p)
```

```pseudo id=tasks
O_GROUP(S, p, limit)
L4  if (S, p) has a winner, or a failure with a bound of at least limit, return
L5  if S is not explored, push O_GROUP(S, p, limit) again and E_GROUP(S) on top of it, and return
L6  make a context (S, p, limit); push FINISH(context), then O_EXPR(context, e) for each expression e of S, and the enforcer move for p

E_GROUP(S)
L7  if S is explored or being explored, return; else push MARK_EXPLORED(S), then E_EXPR(S, e) for each expression e of S

E_EXPR(S, e)
L8  for each rule not yet applied to e: mark it, push APPLY_RULE(S, e, rule), and on top push E_GROUP of each input group that the pattern of the rule looks into

APPLY_RULE(S, e, rule)
L9  add the new expressions to their groups, and push E_EXPR(S, f) for each new expression f of S

O_EXPR(context, e)
L10 push O_INPUTS(context, move) for each algorithm that implements e and gives p, so that the most promising move runs first

O_INPUTS(context, move), which can stop and resume
L11 while the move has an input goal (G, q) left do
L12     if total ≥ context.limit, or (G, q) failed with a bound of at least context.limit - total, drop the move and return
L13     if (G, q) has a winner, add its cost to total and go to the next input
L14     push this task again, push O_GROUP(G, q, context.limit - total) on top of it, and return
L15 if total < context.limit, make the move the best of the context and set context.limit ← total

FINISH(context)
L16 store the best move as the winner of (S, p), or store a failure with the first limit of the context

MARK_EXPLORED(S)
L17 mark S as explored
```

Line L5 is exploration on demand: a group is explored only when a goal needs it. Line L8 pushes E_GROUP above APPLY_RULE, so the input group of a pattern is explored before the rule binds it, as associativity needs all expressions of its left input. Line L14 shows the branch and bound: an input goal gets only the part of the limit that is left. The promise in this code is the local cost of a move, so cheap moves run first and set a low limit early. In this toy model the transformation rules are applied during exploration and the algorithms during optimization; in the framework both kinds of rule are objects with a pattern, a promise and a condition.

## Example

Take the data of the Volcano page: $|R_0| = 200$, $|R_1| = 100$, $|R_2| = 50$, with 100, 50 and 10 distinct values of $k$, and an index on $R_0.k$ only, so $|R_1 \bowtie R_2| = 100$ and the result has 200 rows. Ask for any order. These are the first steps for the goal of the whole query.

| step | move | input goals and their limits | result | limit after |
|---|---|---|---|---|
| 1 | MergeJoin($R_0 R_1$, $R_2$), local 250 | sorted $R_0 R_1$ and sorted $R_2$, limit $\infty$ | 1400 | 1400 |
| 2 | HashJoin($R_0 R_1$, $R_2$), local 300 | winners exist: 700 and 50 | 1050 | 1050 |
| 3 | MergeJoin($R_0$, $R_1 R_2$), local 300 | sorted $R_0$ costs 400; sorted $R_1 R_2$ gets the limit 350 | fails | 1050 |
| 4 | HashJoin($R_0$, $R_1 R_2$), local 400 | $R_0$ costs 200; $R_1 R_2$ (any order) gets the limit 450 and wins with 350 | 950 | 950 |

Inside step 3, the goal "sorted $R_1 R_2$ below 350" tries its Sort move, whose local cost is 200, so it asks for "$R_1 R_2$ in any order below 150". That goal fails, and its failure is stored with the bound 150. In step 4 the same group is asked again with the higher limit 450, so the search runs again and finds the hash join at 350. No later move beats 950. Later, the merge join of $R_0 R_2$ and $R_1$, with local cost 200, asks for "sorted $R_0 R_2$ below 750"; its optimum is exactly 750, so it fails, and that failure stays in the memo at the end. The plan is HashJoin($R_0$, HashJoin($R_1$, $R_2$)) at 950, as with Volcano. For sorted output the result is MergeJoin(IndexScan $R_0$, Sort(HashJoin($R_1$, $R_2$))) at 1250.

In this model, pruning does not reduce the number of tasks: the example runs 231 tasks, against 178 without pruning, because goals that fail are optimized again with higher limits.

## Correctness

The tasks run in last-in, first-out order, so a goal that a task asks for, with all its own tasks, ends before the asking task resumes, and a task only asks for smaller groups, or for the same group with a weaker property. Exploration is complete: every expression of a group gets each rule once, after the input group of the pattern is explored, so the expressions of an explored group are closed under the rules, which in this model gives every ordered split. The search is then correct by induction over the goals, as for Volcano: a move reaches line L15 with its true cost exactly when that cost is below the current limit, a failure is a lower bound, and a winner is the optimum. The proof file has the details, with the termination.

## Complexity

In the join model the memo has $2^n - 1$ groups and $3^n - 2^{n+1} + 1$ join expressions, and each expression gets each of the two rules exactly once, which the tests count. Associativity reads the expressions of the left input, so exploration costs $O(4^n)$ set operations. Without pruning each goal is optimized once, with $O(3^n)$ tasks in all. With pruning a goal can be optimized again with a higher limit, so the work depends on the costs. The memo takes $O(3^n)$ space. The stack of tasks replaces the recursion of Volcano, so its depth does not limit the size of the query.

## Properties

- **Exact.** With rules that reach every equivalent expression, the winner of the query goal is a cheapest plan.
- **Explores on demand.** A group is explored when a goal or a rule pattern needs it, not all at the start.
- **Ordered by promise.** The order of the moves is free, so good moves can run first and give low limits early.
- **Memoized goals.** Winners and failures are stored per group and property; a failure is a lower bound for its limit.
- **Extensible.** Operators, rules, enforcers and promises are objects that the builder of the optimizer adds.
- **Explicit tasks.** The search can stop after a time budget, because its state is the stack and the memo.

## Variants and improvements

- **Lower bounds.** Later work computes a lower bound on the cost of a group from its cardinality, so a move can stop before its inputs are optimized.
- **Join enumeration inside the memo.** For large join queries a rule set that generates every split by commutativity and associativity makes many duplicates; an optimizer can instead fill a group with the splits from a [DPccp](/dpccp/) or [DPhyp](/dphyp/) style enumerator.
- **Rewrites before the search.** Many systems apply heuristic rewrites, such as [subquery unnesting](/subquery-unnesting/), before the cost-based search.
- **Parallel search.** Independent goals can be optimized in parallel, since the tasks share only the memo.
- **Search stages and timeouts.** A system can run the search in stages with larger rule sets, and stop when a stage gives a good enough plan.

## When to use it

Use Cascades when an optimizer must handle many operators, rules and physical properties, and the search should be easy to extend and to control. For join order alone, a bottom-up enumerator such as [DPccp](/dpccp/) is simpler and faster. For a very large query, use a heuristic such as [greedy operator ordering](/greedy-operator-ordering/) to fix the join order first, or limit the rule set.

## Pitfalls

- **Optimizing a group before it is explored.** If a goal starts before its group holds all expressions, moves of the expressions that come later are never tried for that goal.
- **Stale failures.** A failure holds only for its limit. A request with a higher limit must search again.
- **Rule duplicates.** Commutativity applied twice gives the old expression back; the memo must detect duplicates and the rules need marks, or exploration does not end.
- **Enforcer cycles.** An enforcer must ask for a weaker property, or a goal depends on itself.
- **Pruning is not free.** Low limits cause failures and new searches; with a poor order of moves, pruning can cost more tasks than it saves.

## Implementations

## History

Goetz Graefe built the EXODUS optimizer generator with David DeWitt in 1987 and the Volcano optimizer generator with William McKenna in 1993. In 1995 he described the Cascades framework, which kept the memo and the goal-driven search of Volcano but replaced its fixed two-phase search with tasks, explored on demand, and made rules and promises into objects. The Columbia optimizer at Portland State University later reimplemented the framework for research.

## References
