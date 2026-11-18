---
tag: KJT4MR
kind: algorithm
slug: volcano-optimizer-generator
name: Volcano optimizer generator
aliases:
- Volcano optimizer
- Volcano search strategy
area: databases/query-planning
level: advanced
summary: Generate an optimizer from algebraic rules and physical properties that searches plans top down by dynamic programming with memoization.
solves: [query-optimization]
model: word-ram
complexity:
  vars: {n: the number of relations in the join model of this page}
  time: {exploration: "O(4^n)", search without pruning: "O(3^n)"}
  space: {memo: "O(3^n)"}
properties: {deterministic: true, exact: true, recursive: true}
history:
  year: 1993
  people: [Goetz Graefe, William J. McKenna]
  note: Presented at ICDE 1993 as the successor of the EXODUS optimizer generator.
prereqs: [query-plan, cost-model, relational-algebra-equivalences, interesting-orders, memoization]
see_also: [cascades-framework, selinger-join-enumeration, dpccp, depth-first-branch-and-bound, iterator-model, exchange-operator, left-deep-and-bushy-join-trees, query-optimization]
sources:
  - paper: "Goetz Graefe and William J. McKenna, The Volcano optimizer generator: extensibility and efficient search, Proceedings of ICDE 1993, 209 to 218"
    title: "The Volcano optimizer generator: extensibility and efficient search"
    locator: "the model specification with operators, algorithms, enforcers, rules and properties, and the search procedure FindBestPlan with its look-up table and cost limit"
  - paper: "Goetz Graefe, The Cascades framework for query optimization, IEEE Data Engineering Bulletin 18(3) (1995), 19 to 29"
    title: The Cascades framework for query optimization
    locator: "the description of the Volcano search strategy and its two phases, compared with the search of Cascades"
---

The Volcano optimizer generator takes a description of a data model and produces a query optimizer for it. The description gives the logical operators, the algorithms that implement them, the transformation rules between logical expressions, the physical properties such as sort order, the *enforcers* that create a property, such as a Sort, and the cost functions. The generated optimizer keeps equivalent expressions in groups of a memo and searches top down. For a group and a required physical property it tries every algorithm that gives the property and every enforcer, asks for the best plans of the inputs with the properties they need, stores the best plan in a table, and prunes moves that cost more than a limit. Goetz Graefe and William McKenna presented it in 1993. Its search is a form of dynamic programming with memoization, driven by the goal instead of built bottom up.

## In plain words

An optimizer must find, among many equivalent ways to run a query, a cheap one. Volcano does not write this search by hand for each system. The builder of a database describes the operators, the rules that turn one form of a query into another, and the costs. Volcano makes the search code from this description.

The search first applies the rules until no new form appears, and it puts forms that give the same result in one group. Then it asks one question: what is the cheapest way to compute this group so that the result has the needed sort order? It answers by trying each method, asking the same question for the inputs, and adding up the costs. It writes each answer down, so it never computes the same answer twice. It also stops a try as soon as it costs more than the best answer so far.

## The problem

The input is a logical query and a required physical property, for example "no order needed" or "sorted on the join key". A *logical expression* is an operator with groups as inputs; a *group* is a set of logical expressions that give the same result. A *physical plan* is a tree of algorithms. Each algorithm implements one logical expression of a group, needs some properties of its inputs, gives some property of its output, and has a local cost. An enforcer, such as Sort, changes only the property. The task is to find a physical plan of least total cost for the query that gives the required property.

The code of this page uses a small model of joins. Relations $R_0, \ldots, R_{n-1}$ share one join attribute $k$, a group is a set of relations, and the rules are join commutativity and associativity. The property is the sort order on $k$. The algorithms are TableScan, IndexScan (sorted, if $R$ has an index on $k$), HashJoin, MergeJoin (both inputs sorted, output sorted) and NestedLoop (keeps the order of the outer input), and the enforcer is Sort. Their local costs are in the code.

## The algorithm

```pseudo id=main
VOLCANO(query, required property p)
L1  put the query in the memo, and EXPLORE each group until no rule adds an expression
L2  return FIND-BEST-PLAN(the group of the query, p, ∞)
```

```pseudo id=explore
EXPLORE(group S)
L3  repeat until a pass adds no expression to S
L4      for each expression (L, R) of S do
L5          add (R, L) to S, by commutativity
L6          EXPLORE(L); for each expression (A, B) of L, add (B, R) to the group B ∪ R and (A, B ∪ R) to S, by associativity
L7  mark S as explored
```

```pseudo id=search
FIND-BEST-PLAN(group S, property p, limit)
L8  if (S, p) is in the table, return its plan if it costs less than limit, or failure if it failed with a limit of at least limit
L9  best ← none
L10 for each move for (S, p): an algorithm that gives p on an expression of S, or the enforcer of p on (S, any) do
L11     total ← the local cost of the move
L12     for each input (G, q) of the move, while total < limit do
L13         r ← FIND-BEST-PLAN(G, q, limit - total)
L14         if r is failure, reject the move; else total ← total + the cost of r
L15     if every input has a plan and total < limit, then best ← this move with its input plans, and limit ← total
L16 store best for (S, p) in the table, or store a failure with the first limit if best is none
L17 return best
```

Line L8 is the memoization. Lines L12 and L15 are the branch and bound: a move stops as soon as its partial cost reaches the limit, and each input gets only the part of the limit that is left. The enforcer move asks for the same group with a weaker property, so a plan that needs sorted output can use an unsorted plan and a Sort on top. In the code a failure also stores its limit, so a later call with a lower or equal limit fails at once, and a call with a higher limit searches again.

The 1993 paper lists the transformations among the moves of FindBestPlan. Graefe described the Volcano search in 1995 as two phases, all transformations first and then the search for plans, and this page uses that form, with lines L1 to L7 as the first phase.

## Example

Take $|R_0| = 200$, $|R_1| = 100$ and $|R_2| = 50$, with 100, 50 and 10 distinct values of $k$, and an index on $R_0.k$ only. The size estimates are $|R_1 \bowtie R_2| = 100$ and $|R_0 \bowtie R_1 \bowtie R_2| = 200$. Exploration makes all 7 groups and the 12 ordered splits. The best plans per group and property are these.

| group | any order | cost | sorted | cost |
|---|---|---|---|---|
| $R_0$ | TableScan | 200 | IndexScan | 400 |
| $R_1$ | TableScan | 100 | Sort(TableScan) | 300 |
| $R_2$ | TableScan | 50 | Sort(TableScan) | 150 |
| $R_1 R_2$ | HashJoin | 350 | Sort(HashJoin) | 550 |
| $R_0 R_1 R_2$ | HashJoin($R_0$, $R_1 R_2$) | 950 | MergeJoin(IndexScan $R_0$, Sort(HashJoin($R_1$, $R_2$))) | 1250 |

For no order, the best plan costs 950. For sorted output, the obvious plan is a Sort on top of that plan, at $950 + 2 \cdot 200 = 1350$. Volcano finds a cheaper plan at 1250: it reads $R_0$ in order through the index, sorts the small join $R_1 \bowtie R_2$, and merges. The pruning shows in the same search. After the merge join at 1250 is found, the Sort move asks for the unsorted plan of the whole query with the limit $1250 - 400 = 850$. The best unsorted plan costs 950, so the call fails and the table stores that failure with the limit 850. With pruning, this search makes 79 calls of FIND-BEST-PLAN; without it, 128.

## Correctness

The rules are sound because the join is commutative and associative on bags. They are complete in this model: in each group, a short chain of the two rules reaches every ordered split, so the memo holds all bushy join trees. The search is correct by induction over the groups, smaller groups first, and for one group with the property "any" before "sorted". If the best plan for $(S, p)$ costs less than the limit, every input of that plan costs less than the part of the limit that it gets, so the induction returns it exactly; otherwise the call fails, and the stored failure limit is a lower bound on the optimum. The proof file has the details.

## Complexity

In the join model with $n$ relations, the memo has $2^n - 1$ groups and $3^n - 2^{n+1} + 1$ join expressions. Exploration of a group with $k$ relations takes a constant number of passes, each over its $O(2^k)$ expressions and the $O(2^k)$ expressions of their left inputs, so the exploration costs $O(4^n)$ set operations. Without pruning, each pair of a group and a property is searched once, with $O(2^{|S|})$ moves, so the search costs $O(3^n)$ moves. With pruning, a pair that failed can be searched again with a higher limit, so the number of searches depends on the costs; in return many moves stop early. The memo and the table take $O(3^n)$ space. In general models the size of the memo depends on the rules, and it can be exponential in the size of the query.

## Properties

- **Exact.** If the rules reach every equivalent expression, the result is a cheapest plan for the required property.
- **Top down and goal driven.** Only pairs of a group and a property that some move needs are optimized, unlike a bottom-up dynamic program that computes all of them.
- **Physical properties and enforcers.** Sort order, and in a parallel system the partitioning of data, are properties that an algorithm can give or that an enforcer can create.
- **Extensible.** New operators, algorithms and rules change the description, not the search.
- **Memoized.** Each result and each failure is stored for the pair of a group and a property.

## Variants and improvements

- **[Cascades](/cascades-framework/).** Graefe's successor explores groups on demand with a stack of tasks, orders rules by promise, and merges transformation and implementation into one search.
- **Better bounds.** Later work uses lower bounds on the cost of a group, so a move can stop before its inputs are optimized.
- **Bottom-up search.** A [Selinger-style](/selinger-join-enumeration/) dynamic program or [DPccp](/dpccp/) builds the same table of best plans bottom up for join order, keeping [interesting orders](/interesting-orders/) instead of required properties.
- **Heuristic limits.** A generated optimizer can stop exploration early, or skip rules, to bound the time for large queries.

## When to use it

Use the Volcano search when an optimizer must support many operators and rules, and the rules should be separate from the search code. For join ordering alone, a bottom-up enumerator such as [DPccp](/dpccp/) is simpler and faster, because it does not generate the expressions by rules. Many newer optimizers follow the [Cascades framework](/cascades-framework/) instead, because it does not need to explore everything before the search.

## Pitfalls

- **Cost of full exploration.** Applying every rule to every group before the search can generate a very large memo, also for expressions that no good plan uses.
- **Rule duplicates.** Commutativity applied twice gives the old expression back; the memo must detect duplicate expressions, or the rules never stop.
- **Stored failures.** A failure is only a lower bound for the limit that caused it. Returning it for a call with a higher limit loses plans.
- **Enforcer loops.** An enforcer must ask for a weaker property; if Sort asks for sorted input, the search calls itself without end.
- **The name.** The Volcano iterator model of query execution comes from the same research project; it is a different topic, the [iterator model](/iterator-model/).

## Implementations

## History

Goetz Graefe and David DeWitt presented the EXODUS optimizer generator in 1987, which already generated an optimizer from rules. Graefe and William McKenna presented the Volcano optimizer generator at ICDE 1993. Its aims were extensibility and an efficient search, and it brought physical properties and enforcers, a top-down search with memoization and a cost limit, and a split between the logical and the physical part of the model. In 1995 Graefe described its successor, the Cascades framework, which kept the memo and the goal-driven search but explored on demand.

## References
