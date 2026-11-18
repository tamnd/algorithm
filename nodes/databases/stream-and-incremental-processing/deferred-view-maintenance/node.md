---
tag: XHDB2T
kind: technique
slug: deferred-view-maintenance
name: Deferred view maintenance
aliases:
- lazy view maintenance
- deferred refresh
area: databases/stream-and-incremental-processing
level: advanced
summary: "Record base changes in logs and bring a materialized view up to date later, at query time or on a schedule, not in each update."
prereqs: [incremental-view-maintenance, delta-rules]
see_also: [incremental-view-maintenance, delta-rules, self-maintainable-view, materialized-view, differential-file, snapshot-isolation, write-ahead-logging, group-commit]
sources:
  - paper: "Latha S. Colby, Timothy Griffin, Leonid Libkin, Inderpal Singh Mumick and Howard Trickey, Algorithms for deferred view maintenance, Proceedings of ACM SIGMOD 1996, 469 to 480"
    title: Algorithms for deferred view maintenance
    locator: "Examples 1.2 and 1.3 (the state bug), Section 2.3 (logs and the old state as a query on the new state), Section 2.5, Definition 1 (past queries), Section 3.1 (the invariants, makesafe and refresh) and Section 5 (the algorithms for three scenarios)"
  - paper: "Timothy Griffin and Leonid Libkin, Incremental maintenance of views with duplicates, Proceedings of ACM SIGMOD 1995, 328 to 339"
    title: Incremental maintenance of views with duplicates
    locator: "the delta rules for the bag algebra, written for the state before the update, which the deferred algorithms reuse"
  - paper: "Dennis G. Severance and Guy M. Lohman, Differential files, their application to the maintenance of large databases, ACM Transactions on Database Systems, 1976"
    title: "Differential files, their application to the maintenance of large databases"
    locator: the differential file that holds the changes apart from the main file (general locator)
  - paper: "Ashish Gupta and Inderpal Singh Mumick, Maintenance of materialized views, problems, techniques, and applications, IEEE Data Engineering Bulletin 18(2) (1995), 3 to 18"
    title: "Maintenance of materialized views, problems, techniques, and applications"
    locator: immediate and deferred maintenance as a choice of when the view is brought up to date
---

Deferred view maintenance is the technique of recording the changes to the base tables in logs and bringing a [materialized view](/materialized-view/) up to date later, at query time or on a schedule, in place of maintaining it inside each updating transaction. The refresh applies [delta rules](/delta-rules/) to the logged changes, as [incremental view maintenance](/incremental-view-maintenance/) does, but at refresh time the base tables already hold their new values. So the rules, which are written for the state before the update, must read that old state as a query over the new state and the logs. Colby, Griffin, Libkin, Mumick and Trickey (1996) showed the errors that come from skipping this step and gave correct algorithms.

## In plain words

Keeping a summary table exact after every change makes every change slower. Instead, you can write each change in a side list and fix the summary only when someone reads it, or once an hour.

The catch is that the fix uses rules that ask "what did the tables look like before these changes?" When you finally do the fix, the tables already show the after picture. If you run the rules on the after picture, you get wrong answers.

So you rebuild the before picture from the after picture and the side list: take the after picture, remove what the list says was added, and put back what the list says was removed. Run the rules on that, apply the result to the summary, and empty the list.

## When it applies

- Updates are frequent and reads of the view are rare, or the readers accept a view that is a little out of date. Deferred maintenance moves the work out of the updating transactions.
- Many changes cancel or merge between refreshes, for example a tuple that is inserted and then deleted. A log of net changes makes the refresh do no work for it.
- The view is not [self-maintainable](/self-maintainable-view/), so the refresh needs the base tables. The base tables hold the new state, and the logs give the way back to the old state.
- A change is a signed bag: each tuple has an integer weight, positive for insertions and negative for deletions. A set is a Z-set with weights 0 and 1, and distinct maps a Z-set to a set.
- Late data is not a special case. A base change that commits after a refresh goes into the log and reaches the view at the next refresh. The view is stale by at most the time between two refreshes, and every committed change reaches it.

## The template

The view is $V$ over base tables $R_1, \ldots, R_m$, and $MV$ is its stored copy. Each base table $R_i$ has a log $L_i$, a signed bag of the net change since the last refresh. The *past query* for $R_i$ is $R_i - L_i$: the current table minus its log, which is the table at the last refresh. DELTA is the procedure of the [delta rules](/delta-rules/) page, which reads the old value of each base table and its change.

```pseudo id=main
UPDATE(T)                                         ▷ an ordinary transaction
L1  apply the changes of T to the base tables
L2  for each changed table R_i: L_i ← L_i + (the change of T to R_i)    ▷ in the same transaction

REFRESH()                                         ▷ on a schedule, or before a read
L3  for each i: P_i ← R_i - L_i                    ▷ the past query: the state at the last refresh
L4  ΔV ← DELTA(V), with old values P_i and changes L_i
L5  MV ← MV + ΔV
L6  for each i: L_i ← ∅

READ()                                            ▷ lazy maintenance
L7  if some L_i is not empty then REFRESH()
L8  return MV
```

Lines L3 to L6 run as one transaction, or under [snapshot isolation](/snapshot-isolation/), so that the base tables and the logs that they read belong to the same state. Line L3 does not have to be materialized: each occurrence of $R_i$ in the expression of line L4 can be replaced by the expression $R_i - L_i$. With separate logs of insertions and deletions, as in Colby et al., the past query is $(R_i \mathbin{\dot{-}} \mathit{ins}_i) \uplus \mathit{del}_i$, where $\dot{-}$ is the bag monus and $\uplus$ the bag union.

**Why it works.** The invariant is $MV = V(R_1 - L_1, \ldots, R_m - L_m)$: the stored view is the view of the state at the last refresh. It holds at the start, with empty logs. Line L2 adds the same change to $R_i$ and to $L_i$, so $R_i - L_i$ does not change, and neither does the right side. After line L4, by the correctness of the delta rules, $MV + \Delta V = V(P + L) = V(R)$, since $P_i + L_i = R_i$. After lines L5 and L6, $MV = V(R)$ and the logs are empty, so the invariant holds again, and READ returns $V$ of the current state. The reasoning needs line L2 to be atomic with line L1, and lines L3 to L6 to be atomic with respect to updates.

**Cost.** Line L2 costs $O(1)$ expected time per changed tuple with a hash map from tuples to weights, and the logs take memory for each tuple with a nonzero net weight, at most the number of distinct changed tuples. A refresh costs the evaluation of DELTA over logs of size $\ell$, which grows with the number of changes since the last refresh, not with the size of the tables. Compared with maintenance in each transaction, the total work is at most the same, because changes that cancel are never processed, and each read may wait for one refresh.

**Example.** This is Example 1.3 of Colby et al. The view is $U = R - S$ under set semantics, with $R = \{a, b, c\}$ and $S = \{c, d\}$, so $MV = \{a, b\}$. A transaction moves $b$ from $R$ to $S$, so the logs are $L_R = \{b{:}\,{-1}\}$ and $L_S = \{b{:}\,{+1}\}$, and now $R = \{a, c\}$ and $S = \{b, c, d\}$. The correct view is $\{a\}$.

| step | what it reads | deletions from $U$ | $MV$ after |
|---|---|---|---|
| the delete rule $(\nabla R - S) \cup (R \cap \Delta S)$ on the state before | $R = \{a, b, c\}$, $S = \{c, d\}$ | $\{b\}$ | $\{a\}$ |
| the same rule on the current state | $R = \{a, c\}$, $S = \{b, c, d\}$ | $\emptyset$ | $\{a, b\}$, wrong |
| line L3, then lines L4 and L5 | $P_R = \{a, b, c\}$, $P_S = \{c, d\}$ | $\{b\}$ | $\{a\}$ |

The past query rebuilds the old state exactly, so the delta rules give $\Delta U = \{b{:}\,{-1}\}$.

## Classic examples

- **Refresh on demand or on a schedule.** Database systems that offer materialized views often keep a change log per base table and refresh the view when asked or at fixed times. This is lines L1 to L6.
- **Data warehouses.** The sources send their changes in batches, and the warehouse views are refreshed at night. The views are often made [self-maintainable](/self-maintainable-view/) so that the refresh reads only the batches.
- **The [differential file](/differential-file/).** Severance and Lohman keep the changes to a file apart from the file and merge them later. A base log of this page is a differential file of the base table, and Colby et al. note that the two give different equations for the old state.
- **Batching in streams.** A stream system that updates its results once per micro-batch, not per event, is doing deferred maintenance with a fixed schedule.

## Variations

- **Three scenarios.** Colby et al. study three scenarios that differ in the auxiliary tables that the transactions keep, such as logs of the base changes and tables of changes to the view. In each scenario a procedure makesafe, run in each transaction, keeps an invariant, and refresh brings the view up to date from the auxiliary tables. The more the transactions keep, the less a refresh has to do. The choice trades the cost of each update against the time of a refresh.
- **Partial refresh.** Apply only the part of the logs up to a given time, so that the view shows a consistent earlier state. The logs then need timestamps, and lines L3 and L6 act on a prefix.
- **Lazy refresh of one group.** For a grouped view, a read that asks for one group can apply only the log entries of that group.
- **Shared logs.** Several views over the same base tables read the same logs. Each view keeps a position in the log in place of line L6, and the log is truncated after all views have passed.

## Pitfalls

- **Evaluating old-state rules on the new state.** This is the state bug of the example. In Example 1.2 of Colby et al., a projection of a join counts some view tuples twice for the same reason.
- **Reading logs and tables from different states.** If an update commits between the read of $R_i$ and the read of $L_i$ at line L3, the past query is wrong. Use one transaction or one snapshot.
- **Logging the change outside the update.** If line L2 runs after the commit of line L1 and the system crashes in between, the change is lost from the log and the view drifts forever. Keep the log in the same transaction, protected by the same [write-ahead log](/write-ahead-logging/).
- **Gross logs in place of net logs.** A log that records each insertion and each deletion apart gives a correct past query only if it is read with the matching equation. Merging into net weights is simpler and smaller.
- **Unbounded logs.** With no refresh, the logs grow without bound. A schedule, or a refresh when the logs reach a size, keeps them small.

## Exercises

1. Prove that $(R \mathbin{\dot{-}} \mathit{ins}) \uplus \mathit{del}$ equals the old $R$ when $\mathit{ins}$ and $\mathit{del}$ are the net insertions and deletions, and give a log of gross changes for which it fails.
2. Write the past query for $V = \pi_A(R \bowtie S)$ and expand the delta rules with it. Which terms read only the current tables?
3. A view is refreshed every $k$ updates. Each update changes one tuple, and half of the updates undo an earlier one. Give the best and the worst number of log entries at a refresh.
4. Show that the invariant fails if line L6 runs before line L5, and give a crash point that makes it visible.

## References
