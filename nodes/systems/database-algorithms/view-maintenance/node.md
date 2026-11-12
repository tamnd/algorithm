---
tag: DJ1QCJ
kind: problem
slug: view-maintenance
name: View maintenance problem
aliases:
- materialized view maintenance
- materialized view refresh
area: systems/database-algorithms
level: advanced
summary: "Keep a materialized view equal to its defining query as the base tables change: by recomputation or by incremental deltas, at once or deferred."
prereqs: [materialized-view]
see_also: [incremental-view-maintenance, dred-algorithm, materialized-view, view-selection, semi-naive-evaluation, datalog, group-by-aggregation, relational-algebra]
sources:
  - paper: "Ashish Gupta and Inderpal Singh Mumick, Maintenance of materialized views, problems, techniques, and applications, IEEE Data Engineering Bulletin 18(2) (1995), 3 to 18"
    title: Maintenance of materialized views, problems, techniques, and applications
    locator: the dimensions of the problem (information available, modifications allowed, view language, database instance) and the survey of techniques
  - paper: "Ashish Gupta, Inderpal Singh Mumick and V. S. Subrahmanian, Maintaining views incrementally, Proceedings of ACM SIGMOD 1993, 157 to 166"
    title: Maintaining views incrementally
    locator: the counting algorithm for nonrecursive views and the DRed algorithm for recursive views
  - paper: "Latha S. Colby, Timothy Griffin, Leonid Libkin, Inderpal Singh Mumick and Howard Trickey, Algorithms for deferred view maintenance, Proceedings of ACM SIGMOD 1996, 469 to 480"
    title: Algorithms for deferred view maintenance
    locator: immediate against deferred maintenance, and the computation of deltas from logs against the state after the updates
  - paper: "Dallan Quass, Ashish Gupta, Inderpal Singh Mumick and Jennifer Widom, Making views self-maintainable for data warehousing, Proceedings of PDIS 1996, 158 to 169"
    title: Making views self-maintainable for data warehousing
    locator: the auxiliary views that make a view maintainable without access to the base relations
  - paper: "Christoph Berkholz, Jens Keppeler and Nicole Schweikardt, Answering conjunctive queries under updates, Proceedings of ACM PODS 2017, 303 to 318"
    title: Answering conjunctive queries under updates
    locator: the dichotomy for conjunctive queries with constant update time (q-hierarchical queries) under the OMv conjecture
---

The view maintenance problem asks how to keep a [materialized view](/materialized-view/) $V = Q(D)$ equal to its query $Q$ when the database $D$ changes. The two basic answers are *full recomputation*, which evaluates $Q$ again, and *incremental maintenance*, which computes the change of $V$ from the change of $D$ ([incremental view maintenance](/incremental-view-maintenance/)). A second choice is *when*: *immediate* maintenance updates the view in the same transaction as the base tables, so the view is never stale; *deferred* maintenance updates it later, on demand or on a schedule, so updates are fast and reads can see stale data. Which method works depends on the view language: delta rules with counts handle select-project-join views, aggregates need extra state, and recursive views need algorithms such as [DRed](/dred-algorithm/).

## In plain words

A stored answer becomes wrong when the data behind it changes. The database must fix it. It can throw the answer away and compute it again, which is simple but slow for big tables. Or it can work out only what changed in the answer, which is fast when the change is small.

It must also decide when to fix the answer. It can fix it at once, as part of each change, so that the answer is always right but every change costs more. Or it can wait and fix it later, for many changes at a time, so that changes stay fast but the stored answer is out of date for a while.

## Definition

**Input.** A view definition $Q$, the stored result $V = Q(D)$, and an update $\Delta D$: a set of insertions, deletions and modifications of base tuples, giving the new state $D' = D + \Delta D$. Some variants restrict what the algorithm may read: the view only, the view and the update, or also the base relations.

**Output.** The new view $Q(D')$, usually as a change $\Delta V$ applied to the stored $V$.

**Goal.** Minimize the cost of producing $Q(D')$, and so the cost of updates (for immediate maintenance) or of refreshes (for deferred maintenance), while keeping the view consistent with the definition at the times the system promises.

## Variants

Gupta and Mumick (1995) classify the problem along four dimensions.

- **Information available.** A view is *self-maintainable* for a kind of update if the view and the update alone determine the new view. A selection view is self-maintainable for insertions and deletions; a join view is not, because a new tuple of $R$ must be joined with $S$. Auxiliary views can make a view self-maintainable, which matters in data warehouses that cannot query their sources.
- **Modifications.** Insertions, deletions, updates of tuples (as a deletion plus an insertion, or directly), and changes of the view definition itself.
- **View language.** Select-project-join views, unions and differences, aggregates, outer joins, subqueries, and recursive views (Datalog).
- **Instance.** Algorithms that work for every database, or that use the current contents to decide that an update cannot affect the view (an *irrelevant update*).

**Timing.**

- **Immediate.** The view changes in the same transaction as the base tables. Reads are always fresh, but each update pays the maintenance cost and may lock view rows, which can make the view a point of contention.
- **Deferred.** Changes are logged and applied later: *on demand* (when a query reads the view, called lazy), *periodic* (on a schedule), or *forced* after a number of changes. Batches are cheaper per change, but the view is stale between refreshes, and the delta must be computed against the right state of the base tables.

## Examples

**Recompute or update.** Let `Sales` have $10^6$ rows, and let the view hold `SUM(amount)` and `COUNT(*)` per store, 100 rows. A batch of 1000 new sales arrives.

| method | reads | writes |
|---|---|---|
| full recomputation | $10^6$ sales rows | 100 view rows |
| incremental | 1000 new rows, grouped into at most 100 deltas | at most 100 view rows, each $+$ the group's delta sum and count |

Incremental maintenance is about 1000 times less work here. If the batch deletes half of all sales instead, the delta has $5 \cdot 10^5$ rows and recomputation is as good.

**An aggregate that is hard to maintain.** If the view also holds `MAX(amount)` per store, insertions are easy: the new maximum is the larger of the old one and the new values. But deleting the sale that holds a store's maximum leaves the view unable to know the second largest value, so the group must be recomputed from the base table: about $10^4$ rows for one store, still far less than $10^6$.

**Counts for deletions.** In a set view $\pi_a(R \bowtie S)$, a tuple $a = 1$ derived twice must survive the deletion of one derivation. The counting algorithm keeps the number of derivations; see the worked example of [incremental view maintenance](/incremental-view-maintenance/).

## Known algorithms

- **Full recomputation.** Evaluate $Q(D')$ and replace $V$. Simple, always correct, and best for large changes or small views. PostgreSQL's `REFRESH MATERIALIZED VIEW` does this.
- **Delta rules and the counting algorithm.** For select-project-join views and unions, apply the delta rules of [incremental view maintenance](/incremental-view-maintenance/); keep counts of derivations to handle deletions under set semantics (Gupta, Mumick and Subrahmanian 1993).
- **Aggregate maintenance.** Keep SUM and COUNT per group and add deltas; recompute groups for MIN and MAX after the deletion of an extreme value. Summary-delta methods first aggregate the changes, then merge them into the view.
- **Recursive views.** [DRed](/dred-algorithm/) (delete and rederive) handles deletions in recursive Datalog views; insertions use [semi-naive evaluation](/semi-naive-evaluation/) seeded with the new facts.
- **Deferred maintenance.** Compute the delta from the log of changes against the state of the base tables after the updates, with compensation for the changes that are already applied (Colby et al. 1996), or keep the base state of the last refresh.
- **Self-maintenance with auxiliary views.** Store small extra views, such as the relevant part of each base relation, so that the view can be maintained without the sources (Quass et al. 1996).

## Bounds

- **Recomputation is always an upper bound** on the cost of maintenance: it costs the evaluation of $Q$ on $D'$. A delta can be as large as the view, so incremental methods do not beat recomputation in the worst case.
- **Constant update time is rare.** Berkholz, Keppeler and Schweikardt (2017) showed that a conjunctive query (without self-joins) can be maintained with constant time per single-tuple update, while still allowing its result to be enumerated with constant delay and its size counted, exactly when it is *q-hierarchical*; for other conjunctive queries this is impossible under the OMv conjecture. So for many join views, every update must cost more than constant time, whatever the algorithm.
- **Recursion.** For recursive views, the effect of one deleted fact can reach facts far away in the derivation graph, and the counting method fails because derivations can form cycles; DRed may do work proportional to the overestimated deletions.

## Reductions

- Incremental maintenance of $Q$ reduces to evaluating the *delta query* $\Delta Q$ on the old database and the update, which is itself a query that the optimizer can plan.
- Maintenance of a recursive view under insertions is semi-naive evaluation started from the new facts; under deletions, DRed reduces it to a deletion phase and a rederivation phase that are both semi-naive evaluations.
- Deciding whether an update is irrelevant to a view (cannot change it) is a satisfiability question about the view's predicates and the updated tuple, which is easy for conjunctions of comparisons.

## Applications

Data warehouses refresh summary tables after each load, usually deferred and incremental. Transactional systems maintain indexed views immediately (SQL Server) or offer both on-commit and on-demand refresh (Oracle). Streaming databases and dataflow systems maintain query results continuously as events arrive. Deductive databases and program analysis tools maintain recursive Datalog results under program edits with DRed and its successors.

## References
