---
tag: RWPEJQ
kind: concept
slug: materialized-view
name: Materialized view
aliases:
- materialised view
- indexed view
- materialized query table
area: systems/database-algorithms
level: core
summary: "A view whose result is computed and stored. Queries can read it in place of the base tables, but it must be kept up to date when the base tables change."
prereqs: [relational-algebra]
see_also: [view-maintenance, incremental-view-maintenance, view-selection, query-containment-problem, query-optimization, index-selection, group-by-aggregation, dred-algorithm]
sources:
  - paper: doi:10.1007/s007780100054
    title: Alon Y. Halevy, Answering queries using views, a survey, The VLDB Journal 10(4) (2001), 270 to 294
    locator: Section 1 and Section 3 (query optimization with materialized views), Section 2 (the definitions of equivalent and maximally contained rewritings)
  - paper: "Alon Y. Levy, Alberto O. Mendelzon, Yehoshua Sagiv and Divesh Srivastava, Answering queries using views, Proceedings of ACM PODS 1995, 95 to 104"
    title: Answering queries using views
    locator: the NP-completeness of finding an equivalent rewriting of a conjunctive query using conjunctive views, and the bound on the number of view atoms in a rewriting
  - paper: "Jonathan Goldstein and Per-Ake Larson, Optimizing queries using materialized views, a practical, scalable solution, Proceedings of ACM SIGMOD 2001, 331 to 342"
    title: Optimizing queries using materialized views, a practical, scalable solution
    locator: the view matching tests for select-project-join views with aggregation in SQL Server
  - paper: "Ashish Gupta and Inderpal Singh Mumick, Maintenance of materialized views, problems, techniques, and applications, IEEE Data Engineering Bulletin 18(2) (1995), 3 to 18"
    title: Maintenance of materialized views, problems, techniques, and applications
    locator: the applications of materialized views and the classes of maintenance problems
  - url: https://www.postgresql.org/docs/current/rules-materializedviews.html
    title: PostgreSQL documentation, Materialized Views
    locator: CREATE MATERIALIZED VIEW and REFRESH MATERIALIZED VIEW (the view is refreshed in full on demand)
---

A materialized view is a named query whose result is stored as a table. An ordinary view is only a definition: each query that uses it runs the definition again. A materialized view runs the definition once and keeps the answer, so a query that needs it, or that can be rewritten to use it, reads the small stored result in place of large joins and aggregations. The price is space and the cost of keeping the stored result consistent with the base tables when they change, which is the [view maintenance](/view-maintenance/) problem. Which views to store is the [view selection](/view-selection/) problem, and how to use them in a query is the problem of *answering queries using views*.

## In plain words

Some questions are asked again and again, such as the total sales of each store. To answer one, the database must read millions of sale records and add them up. If the answer is stored in a small table, the next question can read that table in a moment.

That small stored table is a materialized view. It is like a cached answer. It has two costs. It takes space. And when a new sale is recorded, the stored totals become wrong unless the database changes them too. So the database must decide which answers to keep, how to use them in other questions, and how to keep them correct.

## The idea

**Definition.** A view is a pair (name $V$, query $Q_V$) over base relations. A *virtual* view stores only $Q_V$; a query that names $V$ is expanded by putting $Q_V$ in its place. A *materialized* view also stores the relation $V = Q_V(D)$ for the current database $D$. After the base relations change from $D$ to $D'$, the stored $V$ is *stale* until it is maintained, so that $V = Q_V(D')$ again.

**Three questions.** Systems with materialized views must answer:

1. **Maintenance.** How to bring $V$ up to date: recompute $Q_V(D')$, or compute only the change from the change of the base relations ([incremental view maintenance](/incremental-view-maintenance/)). When: in the same transaction as the update (immediate) or later (deferred). For recursive views the [DRed algorithm](/dred-algorithm/) applies.
2. **Use.** Given a query $Q$ and views $V_1, \ldots, V_m$, find a query $Q'$ over the views (and perhaps base relations) that is equivalent to $Q$: a *rewriting*. The optimizer then compares the cost of $Q'$ with that of $Q$. For conjunctive queries, deciding whether a rewriting exists is a question of [query containment](/query-containment-problem/), and Levy, Mendelzon, Sagiv and Srivastava (1995) proved that finding an equivalent rewriting with conjunctive views is NP-complete. Practical optimizers use fast sufficient tests (*view matching*): the view must contain all rows the query needs, must keep the columns the query uses, and must group at least as finely as the query.
3. **Selection.** Which views to materialize under a space or maintenance budget, for a workload: the [view selection](/view-selection/) problem, a sister of [index selection](/index-selection/).

**Equivalent and contained rewritings.** In query optimization, the rewriting must be equivalent, so the answer does not change. In data integration, where the views describe what each source holds, a *maximally contained* rewriting is enough: it returns the most answers that the sources can give. Halevy's survey (2001) covers both settings.

**Aggregates.** Views with GROUP BY are the most useful, because they are much smaller than their input. A query can use an aggregate view grouped by $G$ if it groups by a coarser set of columns that is a function of $G$ and if its aggregates can be rolled up: SUM, COUNT, MIN and MAX roll up (a SUM of sums), but AVG does not; AVG must be computed from a stored SUM and COUNT.

## Examples

**Rolling up a sum.** Let `Sales(item, store, amount)` have $10^6$ rows and `Store(store, region)` 100 rows. The view

```
CREATE MATERIALIZED VIEW StoreTotal AS
  SELECT store, SUM(amount) AS total, COUNT(*) AS n FROM Sales GROUP BY store
```

has 100 rows. The query `SELECT region, SUM(amount) FROM Sales JOIN Store USING (store) GROUP BY region` can be rewritten as

```
SELECT region, SUM(total) FROM StoreTotal JOIN Store USING (store) GROUP BY region
```

which reads 200 rows in place of $10^6$. The rewriting is equivalent because each region's sum is the sum of the sums of its stores. The query `SELECT region, AVG(amount) ...` can also use the view, as `SUM(total) / SUM(n)`; the average of the store averages would be wrong when stores have different numbers of sales.

**A view that cannot be used.** The view `SELECT store, SUM(amount) FROM Sales WHERE amount > 100 GROUP BY store` cannot answer a query about all sales, because the rows it filtered out are lost. It can answer `... WHERE amount > 500 ...` only if it groups by `amount` too, because the filter on `amount` must be applied before the sum.

**Join views.** A view `V = Emp ⋈ Dept` can replace the join in a query `σ_{city = 'Oslo'}(Emp ⋈ Dept)`, as `σ_{city = 'Oslo'}(V)`, if `V` keeps the column `city`. If an index on `V.city` exists, the query becomes an index lookup.

## Where it is used

- **Commercial systems.** Oracle has materialized views with complete and fast (incremental) refresh, on commit or on demand, and automatic query rewrite. SQL Server has indexed views, which it maintains immediately with each update and can match in queries. DB2 has materialized query tables. PostgreSQL has `CREATE MATERIALIZED VIEW`, which is refreshed in full by `REFRESH MATERIALIZED VIEW` and is not used for automatic rewrites.
- **Data warehouses and OLAP.** Precomputed aggregates of a data cube, chosen by [view selection](/view-selection/), answer roll-up queries fast. They are refreshed after each batch load.
- **Streaming and incremental systems.** Systems that keep query results up to date as data arrives, such as those based on DBToaster-style incremental view maintenance or differential dataflow, are materialized views with continuous maintenance.
- **Data integration.** When sources are described as views over a global schema, answering a query means rewriting it with the views.
- **Caching.** Result caches in application layers are materialized views without automatic maintenance; they become stale.

## References
