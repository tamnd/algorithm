---
tag: BKRT7Y
kind: algorithm
slug: selinger-join-enumeration
name: System R join enumeration
aliases:
- Selinger optimizer
- System R optimizer
- Selinger join order algorithm
- System R dynamic programming
area: systems/database-algorithms
level: core
summary: "Find the cheapest left-deep join plan by dynamic programming over subsets of relations, keeping one plan per interesting order. The optimizer of System R (1979)."
solves: [join-ordering]
model: word-ram
complexity:
  vars: {n: the number of relations, k: the number of interesting orders plus 1}
  time: {worst: "O(k^2 n 2^n)"}
  space: {extra: "O(k 2^n)"}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 1979
  people: [Patricia Selinger, Morton Astrahan, Donald Chamberlin, Raymond Lorie, Thomas Price]
  note: The access path selection of System R at IBM San Jose, published at SIGMOD 1979.
prereqs: [join-ordering, cost-model]
see_also: [query-optimization, matrix-chain-multiplication, query-plan, cardinality-estimation, sort-merge-join, index-nested-loop-join, selectivity, iterator-model]
sources:
  - paper: doi:10.1145/582095.582099
    title: P. Griffiths Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie and T. G. Price, Access path selection in a relational database management system, Proceedings of ACM SIGMOD 1979, 23 to 34
    locator: Section 5, Access path selection for joins, from p. 27 (the search over successively larger subsets, the interesting orders defined by join and ORDER BY columns, and the deferral of cross products)
  - paper: "Guido Moerkotte and Thomas Neumann, Analysis of two existing and one new dynamic programming algorithm for the generation of optimal bushy join trees without cross products, Proceedings of VLDB 2006, 930 to 941"
    title: Analysis of two existing and one new dynamic programming algorithm for the generation of optimal bushy join trees without cross products
    locator: the algorithms DPsize, DPsub and DPccp, and the counts of csg-cmp pairs
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: Chapter 15, the System R style enumeration of left-deep plans with interesting orders
  - paper: doi:10.1145/275487.275492
    title: Surajit Chaudhuri, An overview of query optimization in relational systems, Proceedings of ACM PODS 1998, 34 to 43
    locator: Section 3, the System R optimizer (dynamic programming, interesting orders, left-deep trees)
---

The System R join enumeration, from Selinger et al. (1979), finds the cheapest left-deep plan for a query that joins $n$ relations. It builds the best plans for all sets of relations in order of size: the best plans for a set $S$ come from the best plans for $S - \{R_j\}$, joined with $R_j$ by each available method. This is dynamic programming over the $2^n$ subsets, in place of a search over the $n!$ join orders. Because a plan whose output is sorted can save a sort later, the algorithm keeps, for each set, the cheapest plan for each *interesting order* as well as the cheapest plan overall. It avoids cross products when it can. Most relational optimizers still use this design or a direct extension of it.

## In plain words

To join ten tables, there are millions of orders to try. But many orders share a beginning. Every order that starts with tables A, B and C must first make the join of A, B and C, and only the cheapest way to make it matters for the rest. So the algorithm finds the cheapest way to join each group of two tables, then each group of three, and so on. Each larger group is built from a smaller group plus one more table.

There is one exception. A plan that is a little more expensive but gives its rows in sorted order can save a costly sort later. So for each group, the algorithm keeps the cheapest plan for each useful sort order too, not only the cheapest plan.

## The problem

The input is a set of relations $R_1, \ldots, R_n$ with estimated sizes, the join predicates between them, the access paths of each relation (a scan, and index scans that return tuples in index order), the join methods (nested loops, merge join, and others), a [cost model](/cost-model/), and an optional required output order (ORDER BY). The output is a left-deep join tree with an access path for each relation and a join method for each join, with the least estimated cost. This is the [join ordering](/join-ordering/) problem restricted to left-deep trees, with physical properties.

An order $o$ is *interesting* for a set $S$ if it can still help: it is the order of a join column that connects $S$ to a relation outside $S$ (a later merge join can use it), or it is the order of the ORDER BY or GROUP BY columns. Join columns that are made equal by predicates form one equivalence class and count as one order.

## The algorithm

$\mathrm{best}[S, o]$ holds the cheapest known plan for the join of the set $S$ whose output is in the interesting order $o$, or in no useful order if $o$ = none.

```pseudo id=main
SELINGER(R[1..n], required order r)
L1  for each relation R[j] and each access path a of R[j] do ADD({R[j]}, a)
L2  for k ← 2 to n do
L3      for each set S of k relations do
L4          for each R[j] in S do                           ▷ R[j] is joined last
L5              L ← S − {R[j]}
L6              if no predicate joins L and R[j] and cross products are off then skip this R[j]
L7              for each order o with a stored plan P = best[L, o] do
L8                  for each join method m that can join P with R[j] do
L9                      ADD(S, P ⋈m R[j])
L10 return the cheapest best[{R[1..n]}, o], adding the cost of a final sort when o ≠ r
```

```pseudo id=add
ADD(S, P)
A1  o ← the output order of P;  if o is not interesting for S then o ← none
A2  if best[S, o] is empty or cost(P) < cost(best[S, o]) then best[S, o] ← P
```

Line L1 fills the sets of one relation with every access path, so an index scan that costs more than a full scan survives when its order is interesting. Lines L3 to L9 try every way to get $S$ as a left-deep tree: some relation $R_j$ is joined last, on top of a plan for the other relations. For a merge join on the class $k$, the method adds a sort of $P$ unless $o = k$, and a sort or an ordered access path for $R_j$. A nested loop or index nested loop join keeps the order of its outer input; a hash join destroys it. Line A1 maps orders that can no longer help to none, so that only useful orders are kept apart.

## Example

Three relations: Emp with 1000 tuples, Dept with 10 and Job with 50. The predicates are Emp.dno = Dept.dno (selectivity 1/10) and Emp.job = Job.job (1/50), and the query asks for ORDER BY job. Emp and Job have sorted indexes on job. The page's implementation uses this cost model, in abstract units: a scan costs the size $N_j$ of the relation, an index scan $2N_j$; a nested loop join costs $N_j + |P| N_j / 10$ more than its outer input $P$; a hash join $3N_j + |P|$; an index nested loop join $2|P| + |P \bowtie R_j|$; a merge join adds a sort of $2|P|$ when $P$ is not in the right order; the final sort costs 2000. Every join here has 1000 tuples.

| set | interesting orders | best plan for order none | best plan for order job |
|---|---|---|---|
| {Emp} | dno, job | scan, 1000 | index scan, 2000 |
| {Dept} | dno, job | scan, 10 | |
| {Job} | job | scan, 50 | index scan, 100 |
| {Emp, Dept} | job | Dept, nested loop Emp: 2010 | Emp index scan, nested loop Dept: 3010 |
| {Emp, Job} | dno, job | Job scan, index nested loop Emp: 1150 | Job index scan, index nested loop Emp: 1200 |
| {Emp, Dept, Job} | job | {Emp, Job} none, nested loop Dept: 2160 | {Emp, Job} job, nested loop Dept: 2210 |

The set {Dept, Job} has no predicate, so line L6 skips it. Line L10 compares $2160 + 2000 = 4160$ (the unordered plan plus the final sort) with 2210, and returns the second plan: Job by its index in job order, an index nested loop join into Emp, which keeps the job order, and a nested loop join with Dept. If the algorithm kept only the cheapest plan per set, it would keep the plan of cost 1150 for {Emp, Job}, lose the ordered one, and return 4160. With cross products on, the plan (Job by its index $\times$ Dept) then Emp by its index costs 2160 and wins.

## Correctness

The proof rests on two facts. First, the cost of a left-deep plan is the cost of its left input plus a term that depends only on the set of relations of that input, its output order, the relation joined last and the method; the size of each result depends only on its set of relations. Second, an order that is not interesting for a set $L$ cannot become useful later: a merge join needs an order on a class that links $L$ to the new relation, and ORDER BY is always interesting. So two plans of $L$ with the same label (interesting order, or none) can replace each other in any larger plan, and the cheapest one per label is enough. By induction on the size of $S$, $\mathrm{best}[S, o]$ is a cheapest left-deep plan of $S$ with label $o$, and line L10 returns a cheapest complete plan. The proof file has the details.

## Complexity

With cross products allowed, there are $2^n$ sets, each with at most $n$ choices of the last relation, at most $k$ stored orders, and $O(k)$ join methods and classes per step, so the time is $O(k^2 n 2^n)$ steps, and the table has $O(k 2^n)$ entries. Without cross products, only connected sets of relations have plans, which is far fewer for chain and star queries: a chain has $n(n+1)/2$ connected sets. The exponential growth is unavoidable in the worst case, because the problem is NP-hard (see [join ordering](/join-ordering/)). Compared with the $n!$ orders of an exhaustive search, the DP for 10 relations considers at most $10 \cdot 2^{9} = 5120$ (set, last relation) pairs, against 3 628 800 orders.

## Properties

- **Exact for its space.** It finds the cheapest left-deep plan under the cost model, not the cheapest bushy plan.
- **Needs an additive, monotone cost.** The cost of a plan must be its input's cost plus a term that does not depend on how the input was computed beyond its set and order. Costs that depend on the whole plan, such as the memory shared by concurrent operators, break this.
- **Plans are only as good as the estimates.** The DP is exact for the estimated cardinalities, which can be far off; see [cardinality estimation](/cardinality-estimation/).

## Variants and improvements

- **Bushy trees.** Let both inputs of a join be any stored plan: for each set $S$, try each split into $S_1$ and $S - S_1$. Enumerating by subsets (DPsub) takes $O(3^n)$ pairs with cross products. DPsize enumerates by size, as System R does.
- **DPccp.** Moerkotte and Neumann (2006) enumerate only pairs of connected subgraphs that are joined by an edge (csg-cmp pairs). The work then equals the number of such pairs, which is $O(n^3)$ for chain queries; DPsize and DPsub can do much more work on sparse query graphs.
- **Matrix chain.** For a chain query with bushy trees and no cross products, the connected sets are intervals and the DP is the interval DP of [matrix chain multiplication](/matrix-chain-multiplication/), with the subsets replaced by intervals.
- **Top-down enumeration with memoization**, as in the Volcano and Cascades optimizers, explores the same space from the full set downward and can prune with cost bounds.
- **Heuristic limits.** Systems switch to greedy or randomized search when $n$ is large; PostgreSQL uses its genetic optimizer from 12 relations by default.

## When to use it

Use it for queries with up to about 10 to 15 relations, where the exponential table is still small, and when the plans must be exact for the cost model. It is the standard choice in relational optimizers. For bushy plans on sparse query graphs prefer DPccp; for very large queries use the heuristics of [join ordering](/join-ordering/), such as greedy or randomized search, or IKKBZ for tree queries.

## Pitfalls

- **Forgetting interesting orders.** Keeping one plan per set loses ordered plans and can miss the optimum, as the example shows (4160 against 2210).
- **Too many orders.** Treating every column as an interesting order multiplies the table size. Only orders that a later join, GROUP BY or ORDER BY can use should be kept apart (line A1).
- **Equivalence classes.** The predicates $A = B$ and $B = C$ make $A$ and $C$ equal too. Without this closure, a set of relations may look disconnected and need a cross product, and an order on $A$ is not seen to serve a merge join on $C$.
- **Cross products.** Forbidding them always is a heuristic, not a rule. For star queries a cross product of small dimension tables can be the best plan, and the DP without them can miss it.
- **Estimated costs.** The DP picks the cheapest plan for the estimates, not for the data; errors in the estimates of large joins grow quickly.

## Implementations

## History

Selinger, Astrahan, Chamberlin, Lorie and Price described the access path selection of System R at SIGMOD 1979. The paper introduced the cost formulas with page fetches and a CPU weight, the selectivity defaults, the dynamic program over subsets for left-deep trees, interesting orders, and the deferral of cross products. It became the model for the optimizers of most commercial systems. Later work extended the search to bushy trees and improved the enumeration: Ono and Lohman (1990) counted the search spaces, and Moerkotte and Neumann (2006) gave DPccp, which is optimal for the number of pairs it considers.

## References
