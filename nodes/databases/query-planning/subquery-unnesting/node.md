---
tag: 0C9G7B
kind: technique
slug: subquery-unnesting
name: Subquery unnesting
aliases:
- subquery decorrelation
- query unnesting
area: databases/query-planning
level: core
summary: "Rewrite a correlated nested subquery as a join or an outer join with grouping, so that it is evaluated once instead of once per row."
prereqs: [relational-algebra, sql-null-semantics, semijoin, group-by-aggregation]
see_also: [eager-aggregation, relational-algebra-equivalences, predicate-pushdown, magic-sets, certain-answers, cascades-framework, query-optimization, hash-aggregation]
sources:
  - paper: "Won Kim, On optimizing an SQL-like nested query, ACM Transactions on Database Systems 7(3) (1982), 443 to 469"
    title: On optimizing an SQL-like nested query
    locator: "the types of nesting (A, N, J, JA and D) and the algorithms that transform each type into a query without nesting"
  - paper: "Richard A. Ganski and Harry K. T. Wong, Optimization of nested SQL queries revisited, Proceedings of ACM SIGMOD 1987, 23 to 33"
    title: Optimization of nested SQL queries revisited
    locator: "the COUNT bug of the transformation of type JA queries, and the repair that computes the aggregate for every outer value with an outer join"
  - paper: "Umeshwar Dayal, Of nests and trees: a unified approach to processing queries that contain nested subqueries, aggregates, and quantifiers, Proceedings of VLDB 1987, 197 to 208"
    title: "Of nests and trees: a unified approach to processing queries that contain nested subqueries, aggregates, and quantifiers"
    locator: "general locator: one method for nested subqueries, aggregates and quantifiers"
  - paper: "Thomas Neumann and Alfons Kemper, Unnesting arbitrary queries, BTW 2015, Lecture Notes in Informatics P-241, 383 to 402"
    title: Unnesting arbitrary queries
    locator: "general locator: the dependent join, the set of distinct outer values and the rules that push the dependent join down until no correlation is left"
  - paper: "doi:10.1145/2877206"
    title: "Leonid Libkin, SQL's three-valued logic and certain answers, ACM Transactions on Database Systems 41(1), 2016, article 1"
    locator: "general locator: the difference between SQL answers on databases with nulls and certain answers"
---

Subquery unnesting is the technique that rewrites a query with a subquery in its WHERE clause into a query of joins, [semijoins](/semijoin/), antijoins and groupings. A subquery is *correlated* when it reads a column of the outer row, as in `S.k = R.k`. Evaluated as written, it runs once for each row of $R$. After the rewrite, the optimizer can choose the join order and the join algorithms, and the subquery work is done once for the whole table. The rewrite must give the same bag of rows as the original query under the SQL rules for NULL, and that is the hard part: the COUNT bug and the NOT IN case are both errors of rewrites that ignore empty groups or nulls.

## In plain words

A query asks, for each order, whether the customer has any complaint, or whether the number of complaints equals a stored value. Done literally, the database looks through all complaints once for each order. That is slow.

It is better to count the complaints of all customers in one pass, and then match each order with its customer's count. A question about "any complaint" becomes a check that the customer appears in the complaints.

Two details make this harder than it looks. A customer with no complaints has no line in the counts, but the real count is zero, so the rewrite must keep the orders that find no match and give them a zero. A missing value in the data also changes the answer of a "not in this list" question, so the rewrite must treat missing values exactly as the original does.

## When it applies

- The query is SQL, so tables and results are bags. Each row of $R$ that passes the WHERE condition appears in the result as many times as it appears in $R$, whatever the subquery returns.
- The condition has a subquery that is a function of the outer row. The code of this page uses the outer table $R(k, x)$ and the inner table $S(k, v)$ with these conditions: `EXISTS (SELECT * FROM S WHERE S.k = R.k)`, its negation, `R.k IN (SELECT S.k FROM S)`, `R.k NOT IN (SELECT S.k FROM S)`, and `R.x op (SELECT agg(S.v) FROM S WHERE S.k = R.k)` with op one of =, <>, <, <=, >, >= and agg one of COUNT(\*), COUNT, SUM, MIN and MAX.
- The correlation is an equality on columns. Then the inner rows can be grouped once by the correlated column. Other correlations, such as `S.k < R.k`, need the general method with the set of distinct outer values in the Variations section.
- A scalar subquery without an aggregate must return at most one row, or SQL raises an error at run time. A rewrite with a join silently returns several rows instead, so it applies only when a key of $S$ proves that the subquery returns at most one row.
- The WHERE test keeps a row only if the condition is TRUE. FALSE and UNKNOWN both drop the row, and the rewrite uses this fact at line L6.

## The template

Write $\gamma_{k;\,\mathrm{agg}(v) \to a}(S)$ for the grouping of $S$ by $k$, $\mathrm{agg}(\emptyset)$ for the value of the aggregate on no rows (0 for COUNT(\*) and COUNT, NULL for SUM, MIN and MAX), and $R \ltimes S$ for the semijoin. A join test with NULL on either side is UNKNOWN, so no row with a NULL join value has a match.

```pseudo id=main
UNNEST(R, S, condition)                       ▷ the rows of R whose condition is TRUE, as a bag
L1  if condition is EXISTS with S.k = R.k, or R.k IN S.k then return R ⋉ π_k(S)
L2  if condition is NOT EXISTS with S.k = R.k then return ANTIJOIN(R, π_k(S))
L3  if condition is R.k NOT IN S.k then return NULL-AWARE-ANTIJOIN(R, π_k(S))
L4  G ← γ_{k; agg(v) → a}(S)                   ▷ condition is R.x op (agg(S.v) where S.k = R.k)
L5  if agg(∅) is not NULL then T ← LEFT-OUTER-JOIN(R, G, R.k = G.k), with a ← agg(∅) in each row of R with no match
L6  else T ← R ⋈_{R.k = G.k} G                 ▷ a row with no group compares with NULL and fails
L7  return π_{k, x}(σ_{x op a}(T))
```

NULL-AWARE-ANTIJOIN$(R, K)$ returns $R$ if $K$ is empty. If $K$ holds a NULL, it returns the empty bag. Otherwise it returns the antijoin of the rows of $R$ whose $k$ is not NULL with $K$.

**Why it works.** For a row $r$, the inner rows that the subquery sees are the rows $s$ of $S$ with $s.k = r.k$ TRUE, which is the empty bag when $r.k$ is NULL. Line L1: EXISTS is TRUE exactly when this bag is not empty, which is the definition of the semijoin with the SQL join test. IN with an uncorrelated list is TRUE exactly when some $s.k$ equals $r.k$, and it is never TRUE when $r.k$ is NULL, so it is the same semijoin. The semijoin keeps each row of $R$ with its count and never repeats it. Line L2 is the complement of line L1 within $R$, as NOT EXISTS is never UNKNOWN. Line L3: `r.k NOT IN K` is the negation of a disjunction of the tests $r.k = s.k$. It is TRUE for every row when $K$ is empty. If $K$ holds a NULL, one term of the disjunction is UNKNOWN, so the negation is FALSE or UNKNOWN and never TRUE. If $K$ has no NULL, the negation is TRUE exactly when $r.k$ is not NULL and equals no value of $K$. Lines L4 to L6: the bag that the subquery sees is the group of $r.k$ in $G$ if there is one, and the empty bag otherwise. $G$ has at most one row for each value of $k$, so the join gives each row of $R$ at most one partner and keeps its count. When $\mathrm{agg}(\emptyset)$ is NULL, the original comparison for a row with no group is UNKNOWN, so the row is dropped, as the inner join of line L6 drops it. When $\mathrm{agg}(\emptyset)$ is 0, the outer join of line L5 keeps the row and gives it 0. The group of $G$ with key NULL never joins, which is correct, because no outer row sees it.

**Cost.** The nested query evaluates the subquery once for each row of $R$, which costs $O(|R| \cdot |S|)$ with scans. After the rewrite, a hash grouping and a hash join cost $O(|R| + |S|)$ expected time, and the optimizer can also use a sort-based plan or an index. The code of this page builds the operators of the dbrel helper by their definitions, with nested loops, so it shows that the results are the same, not that the rewrite is faster.

**Example.** Take $R = \{(1, 0), (2, 0), (3, 2), (\mathrm{NULL}, 0)\}$ as $(k, x)$ and $S = \{(1, 5), (1, 7), (3, \mathrm{NULL}), (\mathrm{NULL}, 4)\}$ as $(k, v)$.

| condition | original query | rewrite of this page | naive rewrite |
|---|---|---|---|
| `x = (SELECT COUNT(*) ... S.k = R.k)` | $(2, 0)$, $(\mathrm{NULL}, 0)$ | lines L4, L5 and L7: the same | inner join with $G$: empty |
| `k NOT IN (SELECT k FROM S)` | empty | line L3: empty | antijoin: $(2, 0)$, $(\mathrm{NULL}, 0)$ |
| `EXISTS (... S.k = R.k)` | $(1, 0)$, $(3, 2)$ | line L1: the same | join, then projection: $(1, 0)$ twice, $(3, 2)$ |

For the first row of the table, the counts that the subquery returns are 2 for $k = 1$, 0 for $k = 2$, 1 for $k = 3$ and 0 for the row with a NULL key, which sees no inner row. The grouping $G$ is $\{(1, 2), (3, 1), (\mathrm{NULL}, 1)\}$. It has no group for $k = 2$, so the inner join loses $(2, 0)$, and it cannot match the NULL key, so it loses $(\mathrm{NULL}, 0)$ too. If the row $(\mathrm{NULL}, 4)$ is removed from $S$, the original NOT IN query returns $(2, 0)$ only: the row with a NULL key gets UNKNOWN, as it is compared with a list that is not empty. With an empty $S$, NOT IN returns all four rows of $R$. The tests check these cases and random tables with NULL values against the original query, for every condition.

## Classic examples

- **Kim's types.** Kim classified a nested block by whether it is correlated (type J) or not, and whether it has an aggregate (type A). An uncorrelated aggregate is a constant and runs once. Types N and J become semijoins, as at line L1. Type JA becomes a grouping and a join, as at lines L4 and L6.
- **The COUNT bug.** Ganski and Wong showed that Kim's transformation of type JA queries gives wrong answers for COUNT, because the inner join drops the outer rows with no inner rows. Their repair computes the aggregate for every outer value with an outer join, as at line L5.
- **NOT IN as a null-aware antijoin.** An optimizer can use a special antijoin for NOT IN that checks for NULL in the inner input, as at line L3, because the plain antijoin is the rewrite of NOT EXISTS only. The NOT IN case is also an example of how SQL answers on tables with nulls can differ from the [certain answers](/certain-answers/), as Libkin discusses.
- **Rewrites before the search.** Optimizers often unnest in a rewrite phase, and then the [Cascades](/cascades-framework/) or [Selinger](/selinger-join-enumeration/) search orders the joins that the rewrite made.

## Variations

- **General unnesting.** For any correlation, first compute $D = \mathrm{DISTINCT}(\pi_k(R))$, the outer values. Then evaluate the subquery once for each value of $D$ with a left outer join of $D$ with $S$ and a grouping by $D$, and join the result back to $R$. Neumann and Kemper describe this with a *dependent join* that is pushed down until no correlation is left. The join back must treat two NULL values as equal (`IS NOT DISTINCT FROM`). The code has this variant as general_unnest. With a plain equality it loses $(\mathrm{NULL}, 0)$ in the example.
- **COUNT(\*) after an outer join.** In the general variant, the padded row of a value of $D$ with no inner row must not be counted. COUNT(\*) over the outer join gives 1 for it. The code counts a column of $S$ that is never NULL in a real match, here $S.k$, which gives 0.
- **Magic sets.** Computing $D$ first and passing it into the subquery is the idea of the [magic sets](/magic-sets/) rewriting of Datalog: compute the bindings that the caller needs, then only the answers for those bindings.
- **Groupjoin.** Lines L4 and L5 group $S$ and then join it with $R$. An operator that does both in one hash table on $k$ saves one pass and one table.
- **Aggregation below or above the join.** When the rewrite gives a join with a grouping on top, [eager aggregation](/eager-aggregation/) decides whether to group before the join.

## Pitfalls

- **The COUNT bug.** An inner join with the grouped subquery drops the outer rows with no inner row. This is wrong exactly when $\mathrm{agg}(\emptyset)$ is not NULL. For COUNT(\*) and COUNT, use an outer join and replace the padding with 0. For SUM, MIN and MAX, the inner join is right, as the tests check on random tables.
- **NOT IN as a plain antijoin.** The antijoin keeps the rows of $R$ whose key matches nothing, and it keeps a row with a NULL key. NOT IN keeps neither when the list holds a NULL, and it drops a NULL key when the list is not empty. In the example, the antijoin returns two rows and NOT IN returns none.
- **EXISTS as a join.** A join of $R$ with $S$ repeats each row of $R$ once for each match. In the example, $(1, 0)$ appears twice. Use a semijoin. A DISTINCT after the join does not repair it when $R$ itself has duplicate rows, as their copies are then lost.
- **The join back with plain equality.** In general unnesting, the rows of $R$ whose correlated column is NULL do not match their own value of $D$. Use a null-safe equality.
- **Scalar subqueries with more than one row.** The join hides the run-time error of the original query and returns extra rows.
- **Other aggregates.** AVG of no rows is NULL, so it follows the rule of SUM. A user aggregate with another value on no rows needs line L5 with that value.

## Exercises

1. Rewrite `R.x > (SELECT MAX(S.v) FROM S WHERE S.k = R.k)` and explain why the inner join gives the right answer when some groups are empty.
2. Give tables for which `R.k NOT IN (SELECT S.k FROM S)` and `NOT EXISTS (SELECT * FROM S WHERE S.k = R.k)` differ, with no NULL in $R$.
3. Rewrite `R.x = (SELECT COUNT(*) FROM S WHERE S.k = R.k)` with general unnesting. What must be counted after the outer join of $D$ with $S$, and why is COUNT(\*) wrong there?
4. Rewrite `EXISTS (SELECT * FROM S WHERE S.k = R.k AND S.v > R.x)`. Why can $S$ not be grouped by $k$ alone, and what does the set $D$ hold?

## References
