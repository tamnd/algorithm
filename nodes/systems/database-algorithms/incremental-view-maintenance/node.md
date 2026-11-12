---
tag: V5APR5
kind: algorithm
slug: incremental-view-maintenance
name: Incremental view maintenance
aliases:
- IVM
- delta view maintenance
- counting algorithm for view maintenance
area: systems/database-algorithms
level: advanced
summary: "Update a materialized view from the changes to its base tables by delta rules, such as dR join S + R join dS + dR join dS, in place of a full recomputation."
solves: [view-maintenance]
properties: {deterministic: true, exact: true, recursive: true}
history:
  year: 1986
  people: [José A. Blakeley, Per-Åke Larson, Frank Wm. Tompa]
  note: Blakeley, Larson and Tompa gave differential update rules for select-project-join views at SIGMOD 1986; Gupta, Mumick and Subrahmanian gave the counting algorithm in 1993.
prereqs: [view-maintenance]
see_also: [dred-algorithm, materialized-view, view-maintenance, relational-algebra, semi-naive-evaluation, datalog, hash-join, group-by-aggregation]
sources:
  - paper: "José A. Blakeley, Per-Åke Larson and Frank Wm. Tompa, Efficiently updating materialized views, Proceedings of ACM SIGMOD 1986, 61 to 71"
    title: Efficiently updating materialized views
    locator: the differential update of select-project-join views, the detection of updates that cannot affect the view, and the multiplicity counters for projections
  - paper: "Ashish Gupta, Inderpal Singh Mumick and V. S. Subrahmanian, Maintaining views incrementally, Proceedings of ACM SIGMOD 1993, 157 to 166"
    title: Maintaining views incrementally
    locator: the counting algorithm for nonrecursive views (counts of derivations) and the DRed algorithm for recursive views
  - paper: "Timothy Griffin and Leonid Libkin, Incremental maintenance of views with duplicates, Proceedings of ACM SIGMOD 1995, 328 to 339"
    title: Incremental maintenance of views with duplicates
    locator: delta rules for the bag algebra and their correctness
  - paper: "Christoph Koch, Incremental query evaluation in a ring of databases, Proceedings of ACM PODS 2010, 87 to 98"
    title: Incremental query evaluation in a ring of databases
    locator: databases with signed multiplicities as a ring, and recursive (higher-order) delta queries, the basis of DBToaster
  - paper: "Ashish Gupta and Inderpal Singh Mumick, Maintenance of materialized views, problems, techniques, and applications, IEEE Data Engineering Bulletin 18(2) (1995), 3 to 18"
    title: Maintenance of materialized views, problems, techniques, and applications
    locator: the survey of maintenance algorithms by view language, information available and kind of modification
---

Incremental view maintenance (IVM) keeps a [materialized view](/materialized-view/) up to date by computing only the change to the view from the change to the base tables. For a view defined by a relational algebra expression $E$, a *delta rule* gives an expression $\Delta E$ such that $E(D + \Delta D) = E(D) + \Delta E$. For a join the rule is

$$\Delta(R \bowtie S) = \Delta R \bowtie S \;+\; R \bowtie \Delta S \;+\; \Delta R \bowtie \Delta S,$$

with $R$ and $S$ at their old values. When the update is small, $\Delta E$ is much cheaper than a new evaluation of $E$. Deletions need care under set semantics: a tuple of the view may have several derivations, and the *counting algorithm* of Gupta, Mumick and Subrahmanian (1993) keeps, for each tuple, the number of its derivations, and removes the tuple only when the count reaches 0. Counting works for nonrecursive views; for recursive views, such as those of [Datalog](/datalog/), the [DRed algorithm](/dred-algorithm/) is used instead.

## In plain words

A stored view is like a stored answer to a question. When one row of a big table changes, the answer often changes only a little. It is a waste to compute the whole answer again.

So each kind of step has a rule that turns a change in its input into a change in its output. A filter passes the changed rows that meet its condition. A join matches the new rows of one table with the old and the new rows of the other. The output change is added to the stored answer.

Deleting is harder than adding. A row of the answer can come from several rows of the input. So the view stores a count for each row: how many ways there are to make it. A delete lowers the count, and the row leaves the answer only when its count reaches zero.

## The problem

Given a view definition $E$, the stored result $V = E(D)$ and an update $\Delta D$ to the base relations (insertions and deletions), compute $E(D + \Delta D)$, preferably as $V$ plus a small change, without evaluating $E$ from scratch. This is the [view maintenance](/view-maintenance/) problem; this page treats select, project, join and union views (nonrecursive) under bag semantics and under set semantics with counts.

## The algorithm

Relations and changes are *signed bags*: each tuple has an integer multiplicity, negative for deletions. A sum of signed bags adds multiplicities, and a join multiplies them. The view stores $\mathrm{count}[t]$, the multiplicity of $t$ in $E(D)$.

```pseudo id=main
DELTA(E, D, ΔD)                      ▷ returns ΔE with E(D + ΔD) = E(D) + ΔE
L1  if E is a base relation R then return ΔR
L2  if E = σp(E1) then return σp(DELTA(E1))
L3  if E = πA(E1) then return πA(DELTA(E1))
L4  if E = E1 ⊎ E2 then return DELTA(E1) ⊎ DELTA(E2)
L5  E = E1 ⋈ E2:  Δ1 ← DELTA(E1);  Δ2 ← DELTA(E2)
L6  return Δ1 ⋈ E2(D)  ⊎  E1(D) ⋈ Δ2  ⊎  Δ1 ⋈ Δ2

MAINTAIN(V, E, D, ΔD)                ▷ count[t] = multiplicity of t in E(D)
L7  ΔV ← DELTA(E, D, ΔD)
L8  for each tuple t with ΔV[t] ≠ 0 do
L9      c ← count[t] + ΔV[t]
L10     if count[t] = 0 and c > 0 then report t inserted; if count[t] > 0 and c = 0 then report t deleted
L11     count[t] ← c;  drop t when c = 0
L12 D ← D ⊎ ΔD
```

Selection and projection are linear, so their delta is the operator applied to the delta (lines L2 and L3). Join is bilinear, which gives the three terms of line L6. The term $\Delta_1 \bowtie \Delta_2$ is needed when both inputs change in the same update: it joins a new tuple of $R$ with a new tuple of $S$, and it corrects the double counting when an old pair loses a tuple on both sides. A term with an empty delta is empty and is skipped, so a join whose right input did not change costs only $\Delta_1 \bowtie E_2(D)$, which an index on $E_2$ makes a few lookups per changed tuple. An update to a relation that does not occur in $E$ costs nothing.

Under set semantics, $\mathrm{count}[t]$ is the number of *derivations* of $t$: the number of combinations of base tuples that produce it. Projection is where counts matter, because it can map several tuples to one.

## Example

Let $R(a, b) = \{(1,1), (1,2), (2,3)\}$, $S(b, c) = \{(1,0), (2,0), (3,0)\}$ and $V = \pi_a(R \bowtie S)$. Then $R \bowtie S = \{(1,1,0), (1,2,0), (2,3,0)\}$, so $\mathrm{count}[a{=}1] = 2$ and $\mathrm{count}[a{=}2] = 1$.

**Update 1: delete $S(1,0)$.** $\Delta S = \{(1,0) \mapsto -1\}$. Only the term $R \bowtie \Delta S$ is nonempty: it is $\{(1,1,0) \mapsto -1\}$, and its projection is $\{a{=}1 \mapsto -1\}$. The count of $a = 1$ drops from 2 to 1, so the tuple stays: it still has the derivation through $(1,2)$. A set view without counts could not tell this without looking for other derivations.

**Update 2: delete $S(2,0)$, insert $S(4,0)$ and $R(3,4)$ together.** Now $\Delta R = \{(3,4) \mapsto +1\}$ and $\Delta S = \{(2,0) \mapsto -1, (4,0) \mapsto +1\}$, with the old $R$ and $S = \{(2,0), (3,0)\}$.

| term | tuples | after $\pi_a$ |
|---|---|---|
| $\Delta R \bowtie S$ | none (no old $S$ tuple has $b = 4$) | |
| $R \bowtie \Delta S$ | $(1,2,0) \mapsto -1$ | $a{=}1 \mapsto -1$ |
| $\Delta R \bowtie \Delta S$ | $(3,4,0) \mapsto +1$ | $a{=}3 \mapsto +1$ |

The count of $a = 1$ goes from 1 to 0, so $a = 1$ is deleted; $a = 3$ goes from 0 to 1 and is inserted. The new view is $\{a{=}2, a{=}3\}$, the same as a recomputation. Without the third term, $a = 3$ would be missing.

## Correctness

The delta rules are exact for signed bags because selection and projection are linear and join is bilinear: $(R + \Delta R) \bowtie (S + \Delta S)$ expands into $R \bowtie S$ plus the three terms of line L6. By induction on the expression, $E(D + \Delta D) = E(D) + \mathrm{DELTA}(E)$ for every database and update. MAINTAIN adds $\Delta V$ to the counts, so the counts stay equal to the multiplicities of $E$ on the current database. When the base relations are sets, or bags with nonnegative multiplicities, the result has nonnegative multiplicities, so the tuples with a positive count are exactly the tuples of the view. The proof file has the details.

## Complexity

The cost of maintenance is the cost of evaluating the delta expression, not the view. For a view $R \bowtie S$ and an update of $d$ tuples to $R$, with a hash index on the join column of $S$, the cost is $O(d + |\Delta V|)$ expected lookups and output tuples, against $O(|R| + |S| + |V|)$ for a recomputation. For a view with $k$ joins, the delta of one changed relation is a query with $k$ joins in which one input is small, which optimizers evaluate well; in the worst case, the delta can be as large as the view, and then recomputation is as good. Space: the counts add one integer per view tuple. The old values of subexpressions such as $E_2(D)$ must be readable: they are base tables, or stored intermediate views, or they are recomputed.

## Properties

- **Exact.** The result equals a recomputation, multiplicities included.
- **Self-maintainable cases.** Some views can be maintained from the view and the update alone, without reading the base relations. Selection views are self-maintainable for insertions and deletions; join views are not, because $\Delta R \bowtie S$ reads $S$.
- **Order of updates.** The rules use the old state of all relations. Applying the changes of $R$ and $S$ as two separate updates, each with its own old state, also works and needs no $\Delta R \bowtie \Delta S$ term.
- **Nonrecursive views only.** For a recursive view, a tuple can have infinitely many derivations, or derivations in a cycle that keep a count positive after the tuple loses its last real support, so counting fails.

## Variants and improvements

- **Aggregates.** For a view with GROUP BY and SUM or COUNT, the delta of each group's sum is the sum over the delta tuples of the group. Store COUNT(*) per group to know when a group becomes empty, and compute AVG from SUM and COUNT. MIN and MAX are maintained cheaply under insertions, but deleting the current minimum requires reading the group again.
- **Higher-order IVM.** DBToaster (Koch 2010) treats databases with signed multiplicities as a ring. The delta of a delta query is simpler again, so it materializes the deltas too, recursively, and updates each of them by adding small terms. For some query classes each single-tuple update then costs constant time per changed view entry.
- **Recursive views.** For Datalog views, the [DRed algorithm](/dred-algorithm/) (delete and rederive) deletes an overestimate of the affected facts and then rederives those that still have a derivation; insertions use [semi-naive evaluation](/semi-naive-evaluation/), which is the same delta idea applied to the iterations of a fixpoint.
- **Deferred maintenance.** Collect the changes in a log and apply the delta rules later, in one batch. The rules must then use the state of the base tables at the time of the last refresh, or compensate for later changes.
- **Dataflow systems.** Differential dataflow and streaming databases keep many views up to date with deltas, and handle iteration by indexing deltas by both input time and loop round.

## When to use it

Use IVM when the views are read often and the updates are small compared with the base tables: dashboards over growing data, caches of query results, and views over streams. Use recomputation when an update changes a large part of a base table, when the view is cheap to compute, or when the view uses operators without good delta rules (some outer joins, nested subqueries, or MIN and MAX under many deletions). Systems such as Oracle choose between the two per refresh.

## Pitfalls

- **Forgetting the $\Delta R \bowtie \Delta S$ term** when both inputs of a join change in one update. New pairs of new tuples are then lost, and a deleted pair is subtracted twice.
- **Using the new state on both sides.** $\Delta R \bowtie S_{\text{new}} + R_{\text{new}} \bowtie \Delta S$ counts the pairs of changed tuples twice. Use old states as in line L6, or new on one side and old on the other (the form $\Delta R \bowtie S_{\text{new}} + R_{\text{old}} \bowtie \Delta S$ is also exact).
- **Deleting by value under set semantics.** Deleting every view tuple that the delta touches is wrong when the tuple has another derivation; keep counts, or recheck.
- **Projections and DISTINCT without counts.** A view with DISTINCT is a set view; it needs the counts even if the user never sees them.
- **Nondeterministic functions.** A view that uses the current time or random numbers has no delta rule; it must be recomputed.

## Implementations

## History

Blakeley, Larson and Tompa (1986) gave differential rules for select-project-join views, including counters of duplicate derivations for projections and tests that skip updates that cannot affect a view. Gupta, Mumick and Subrahmanian (1993) gave the counting algorithm for nonrecursive views and the DRed algorithm for recursive views. Griffin and Libkin (1995) proved delta rules for the bag algebra. Koch (2010) introduced higher-order delta processing, which the DBToaster system implements, and later work extended incremental maintenance to dataflow and streaming systems.

## References
