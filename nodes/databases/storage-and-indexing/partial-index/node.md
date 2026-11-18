---
tag: 5RMQCY
kind: technique
slug: partial-index
name: Partial index
aliases:
- filtered index
area: databases/storage-and-indexing
level: advanced
summary: "An index over only the rows that satisfy a predicate, which saves space and update cost when queries target that subset."
prereqs: [b-plus-tree, selectivity, access-path-selection]
see_also: [covering-index, clustered-index, index-selection, materialized-view, bitmap-index, zone-map, predicate-pushdown, autoadmin-index-selection]
sources:
  - paper: doi:10.1145/74120.74121
    title: "Michael Stonebraker, The case for partial indexes, ACM SIGMOD Record 18(4) (1989)"
    locator: pp. 4 to 11, the proposal of indexes over a subset of the rows given by a predicate, and their use by the optimizer
  - paper: doi:10.1109/ICDE.1995.380355
    title: "Praveen Seshadri and Arun Swami, Generalized partial indexes, Proceedings of the 11th International Conference on Data Engineering (ICDE 1995)"
    locator: pp. 420 to 427, partial indexes whose predicate is chosen from the data and the query workload
---

A partial index is an ordinary index, such as a [B+ tree](/b-plus-tree/), that holds entries only for the rows of a table that satisfy a fixed predicate $P$, for example `status = 'open'`. If most queries look only at those rows, and the rows are a small part of the table, the index is much smaller than a full index and most updates do not touch it. The optimizer may use the index for a query only if the query's predicate *implies* $P$, so that no row the query needs can be missing from the index. PostgreSQL calls these partial indexes and SQL Server calls them filtered indexes. A partial unique index makes a key unique only among the rows that satisfy $P$.

## In plain words

A shop keeps a card for every order it has ever had, sorted by customer. Almost all orders are done, and people only ever ask about the open ones. So the shop keeps a second, small box with a card only for each open order, sorted by customer. When an order is closed, its card leaves the small box; when an old done order is changed, nothing in the small box changes.

To answer "the open orders of customer 120" you look in the small box. To answer "all orders of customer 120" you cannot, because done orders are not in it. You must check first that the question only asks about open orders.

## When it applies

- Queries filter on a condition that holds for a small, stable fraction of the rows: open orders, unprocessed jobs, rows that are not deleted, rows where a column is not null.
- A full index on the same key would be large, and most writes go to rows outside the subset, so a full index would pay maintenance for rows that queries never ask for.
- The query predicates are written so that the optimizer can prove that they imply $P$. In practice this means that the query repeats the condition of the index, or a narrower one, in the same form.
- A uniqueness rule holds only for a subset, such as "one active subscription per user".

## The template

The index stores (key, row id) pairs for the rows that satisfy $P$, in key order. Predicates are conjunctions of comparisons of integer columns with constants. A conjunction allows one closed interval per column, a *box*. A query on $lo \le key \le hi$ with the extra predicate $Q$ may use the index if the box of $Q \wedge lo \le key \le hi$ lies inside the box of $P$.

```pseudo id=main
BUILD(T, key, P)
L1  I ← the sorted pairs (r.key, r.id) for the rows r of T with P(r)

ON-CHANGE(old row o, new row n)                 ▷ o or n is missing for an insert or a delete
L2  if o exists and P(o) then remove (o.key, o.id) from I
L3  if n exists and P(n) then insert (n.key, n.id) into I

QUERY(lo ≤ key ≤ hi, Q)
L4  if IMPLIES(Q ∧ lo ≤ key ≤ hi, P) then
L5      for each (k, id) in I with lo ≤ k ≤ hi do: output id if Q holds for row id
L6  else scan T and output the rows with lo ≤ key ≤ hi and Q

IMPLIES(Q, P)
L7  for each column c that P restricts do: if the interval of c in Q is not inside the interval of c in P then return false
L8  return true                                 ▷ also true if Q allows no row at all
```

**Correctness.** L1 to L3 keep the invariant "the index holds exactly the rows that satisfy $P$": a change removes the old entry if the old row was in the subset and adds the new entry if the new row is. If the test at L4 succeeds, every row that satisfies the query satisfies $P$ and so is in the index, and L5 checks $Q$ on each candidate, so the answer equals that of a full scan. For conjunctions of comparisons on integer columns, the box test of L7 is exact: if the interval of some column in $Q$ is not inside that of $P$, a row with a value in the difference, and any allowed values in the other columns, satisfies $Q$ but not $P$. Real optimizers use a sound but incomplete test on richer predicates, so they sometimes miss a valid use.

**Cost.** A full index of $N$ rows costs $\Theta(N)$ entries and an update of every row; a partial index costs $\Theta(sN)$ entries for a selectivity $s$ of $P$, and only updates of rows that enter, leave or move inside the subset touch it. A query that uses it reads $O(\log(sN) + t)$ entries for $t$ matches, as a full index would, plus one check of $Q$ per candidate.

## Classic examples

**Open orders.** A table of 10,000 orders (seed 2 in the tests) has 514 open ones, with `status = 0`, and an index on the customer `WHERE status = 0` has 514 entries, about 5% of a full index (a measurement).

| query, for customers 100 to 199 | plan | entries or rows read | answer |
|---|---|---|---|
| `status = 0` | partial index | 44 | 44 rows |
| `status = 0 AND amount > 100` | partial index, then the check of `amount` | 44 | 38 rows |
| no condition on `status` | full scan | 10,000 | 993 rows |
| `status <= 0` | full scan | 10,000 | |

The last query shows the strictness of the test: as far as the predicate says, `status` could be negative, so `status <= 0` does not imply `status = 0`. With the condition `status >= 0` added to the query, the test succeeds and the index is used. After the index is built, 500 updates of the amount of shipped orders cause no index writes. Closing one open order and reopening one shipped order cause two.

**Not null.** An index `WHERE email IS NOT NULL` on a column that is mostly null holds only the rows that have a value, and serves every lookup by email, since `email = ?` implies `email IS NOT NULL`.

**Partial uniqueness.** A unique index on the user `WHERE active` allows many old subscriptions per user but only one active one. The rule cannot be written as a unique index on the whole table.

**Soft deletes.** An index `WHERE deleted_at IS NULL` keeps lookups of live rows fast while the deleted rows pile up in the table.

## Variations

- **Generalized partial indexes.** Seshadri and Swami (1995) let the system choose the indexed subset from the data and the workload, for example to leave out the most frequent values, whose lookups are better done by a scan.
- **Filtered statistics.** SQL Server keeps statistics over the same subset, which helps the optimizer estimate the [selectivity](/selectivity/) of queries on it.
- **Index on an expression.** A related tool indexes $f(row)$ instead of a subset; the two can be combined, as in an index on `lower(email)` where `active`.
- **[Materialized views](/materialized-view/)** with a selection predicate generalize the idea to stored query results, with the same need to prove that a query is contained in the view.
- **[Zone maps](/zone-map/)** and [bitmap indexes](/bitmap-index/) are other ways to skip most of a table for a selective predicate, without a fixed subset.

## Pitfalls

- **The optimizer cannot prove the implication.** A query with a parameter, `status = $1`, cannot use an index `WHERE status = 0`, since the plan must work for every value. A condition written differently, such as `status < 1` for `status = 0`, may also fail, as in the example. Write queries with the same condition as the index.
- **A subset that grows.** If the fraction of rows that satisfy $P$ grows, the index loses its advantage, and if $P$ is a moving condition such as "created in the last week", it cannot be written with a constant and the index must be rebuilt.
- **Too many partial indexes.** One partial index per value of a column (one per status, per tenant) is a full index in pieces, with more overhead and more planning work.
- **Uniqueness only on the subset.** A partial unique index does not prevent duplicates outside $P$, and a row that changes so that it enters $P$ can fail on a conflict.
- **Updates that move rows in and out.** If rows often enter and leave the subset, every such change is an index insert or delete, and the saving in update cost disappears.

## Exercises

1. For an index `WHERE a >= 5 AND b < 3`, decide which of these queries may use it: `a = 7 AND b = 1`, `a > 4 AND b <= 2`, `a >= 5`, `a = 9 AND b < 3 AND c = 0`, `a > 10 AND a < 8`.
2. Show that the box test of L7 is exact for conjunctions of comparisons on integer columns, and give a predicate with `OR` for which the test of each disjunct alone is not enough.
3. A table has $N$ rows, a fraction $s$ of which satisfy $P$, and each row is updated once to a new key, with no change to the columns of $P$. How many index writes does a full index on the key cost, and how many does a partial index cost?

## References
