---
tag: Q8ZX00
kind: technique
slug: delta-rules
name: Delta rules
aliases:
- delta queries
- derivative of a query
area: databases/stream-and-incremental-processing
level: core
summary: "Rules that give the change of a query result from the changes of its inputs, for each operator of relational algebra."
prereqs: [incremental-view-maintenance, relational-algebra]
see_also: [incremental-view-maintenance, higher-order-ivm, dbsp, self-maintainable-view, deferred-view-maintenance, dred-algorithm, semi-naive-evaluation, finite-differences]
sources:
  - paper: "José A. Blakeley, Per-Åke Larson and Frank Wm. Tompa, Efficiently updating materialized views, Proceedings of ACM SIGMOD 1986, 61 to 71"
    title: Efficiently updating materialized views
    locator: "the differential expressions for select-project-join views, with the three terms of the join, and the multiplicity counters for projections"
  - paper: "Xiaolei Qian and Gio Wiederhold, Incremental recomputation of active relational expressions, IEEE Transactions on Knowledge and Data Engineering, 1991"
    title: Incremental recomputation of active relational expressions
    locator: "the change rules for each operator of the set relational algebra (general locator, volume and pages not checked)"
  - paper: "Ashish Gupta, Inderpal Singh Mumick and V. S. Subrahmanian, Maintaining views incrementally, Proceedings of ACM SIGMOD 1993, 157 to 166"
    title: Maintaining views incrementally
    locator: "the counting algorithm, which applies delta rules to tuples with counts of derivations"
  - paper: "Timothy Griffin and Leonid Libkin, Incremental maintenance of views with duplicates, Proceedings of ACM SIGMOD 1995, 328 to 339"
    title: Incremental maintenance of views with duplicates
    locator: "delta rules for the bag algebra, with monus and duplicate elimination, and their correctness"
  - paper: "Latha S. Colby, Timothy Griffin, Leonid Libkin, Inderpal Singh Mumick and Howard Trickey, Algorithms for deferred view maintenance, Proceedings of ACM SIGMOD 1996, 469 to 480"
    title: Algorithms for deferred view maintenance
    locator: "Examples 1.2 and 1.3, which show that a rule written for the state before the update gives wrong results when it is evaluated in the state after the update"
  - paper: "Ashish Gupta and Inderpal Singh Mumick, Maintenance of materialized views, problems, techniques, and applications, IEEE Data Engineering Bulletin 18(2) (1995), 3 to 18"
    title: "Maintenance of materialized views, problems, techniques, and applications"
    locator: the survey of maintenance methods by view language and kind of change
  - paper: doi:10.14778/3587136.3587137
    title: "Mihai Budiu, Tej Chajed, Frank McSherry, Leonid Ryzhyk and Val Tannen, DBSP: automatic incremental view maintenance for rich query languages, PVLDB 16(7), 2023, pages 1601 to 1614"
    locator: Theorem 3.3 (a linear operator is its own delta) and Theorem 3.4 (the delta of a bilinear operator such as the join)
---

Delta rules are the technique that gives, for each operator of [relational algebra](/relational-algebra/), an expression for the change of its result in terms of the changes of its inputs and the old values of its inputs. Applied by structural recursion to a query $E$, they give a query $\Delta E$ with $E(D + \Delta D) = E(D) + \Delta E$. [Incremental view maintenance](/incremental-view-maintenance/) is the algorithm that evaluates $\Delta E$ after each update and adds it to a [materialized view](/materialized-view/). [Higher-order IVM](/higher-order-ivm/) applies the rules again to $\Delta E$ itself, and [DBSP](/dbsp/) restates them as one theorem about linear and bilinear operators on streams of changes.

## In plain words

A view is a stored query answer. When a few rows of the tables change, you do not want to run the query again. Delta rules tell you, one operator at a time, how a change at the input of the operator becomes a change at its output.

For a filter, you filter the changed rows. For a projection, you project the changed rows. For a union, you put the two changes together. A join is harder: new rows on the left meet the old right side, new rows on the right meet the old left side, and new rows on the two sides also meet each other. Difference, duplicate removal and grouping look at the old count of each changed row or group and give the new count.

You then add the change to the stored answer.

## When it applies

- The query is an expression of the bag relational algebra: selection, projection, renaming, union, difference, intersection, product, join, duplicate elimination and grouping with COUNT and SUM. The rules here are for this algebra. Recursive queries need a fixed point; see [semi-naive evaluation](/semi-naive-evaluation/) and the [DRed algorithm](/dred-algorithm/).
- A change is a signed bag: each tuple has an integer weight, positive for insertions and negative for deletions. A bag is a change with weights at least 0. A set is a Z-set with weights 0 and 1, and distinct maps a Z-set to a set. So one set of rules covers bags, sets and changes.
- The old values of the inputs of each operator are available, stored or computable. A view that needs no such values is [self-maintainable](/self-maintainable-view/).
- The rule is evaluated in the state that it was written for. The rules below read the state before the update. If the base tables are already changed, use the variant for the state after the update, or the logs of [deferred view maintenance](/deferred-view-maintenance/).
- Delta rules have no notion of time, so late data needs no special case. A change that arrives late is one more delta, computed against the state at the moment it is applied. Because the weights add up, the view after all changes equals $E$ on the final tables, in any order of application.

## The template

Write $E[t]$ for the weight of tuple $t$ in $E$, $\mathrm{supp}(X)$ for the tuples with nonzero weight in $X$, and $+$ for the sum of weights, tuple by tuple. A join of two signed bags multiplies weights. $E_1$ and $E_2$ are the subexpressions at their old values, and $\Delta E_1$ and $\Delta E_2$ are their changes, found by the same procedure.

```pseudo id=main
DELTA(E)                                         ▷ returns ΔE with E(D + ΔD) = E(D) + ΔE
L1  if E = R then return ΔR                       ▷ a base table: its change is given
L2  if E = σ_p(E1) then return σ_p(ΔE1)
L3  if E = π_A(E1) then return π_A(ΔE1)           ▷ weights of equal tuples add up
L4  if E = E1 ⊎ E2 then return ΔE1 + ΔE2
L5  if E = E1 ⋈ E2 then return ΔE1 ⋈ E2 + E1 ⋈ ΔE2 + ΔE1 ⋈ ΔE2
L6  if E = f(E1, E2) for f in {monus, min} then return, for each t in supp(ΔE1) ∪ supp(ΔE2),
        f(E1[t] + ΔE1[t], E2[t] + ΔE2[t]) - f(E1[t], E2[t])
L7  if E = δ(E1) then return, for each t in supp(ΔE1), [E1[t] + ΔE1[t] > 0] - [E1[t] > 0]
L8  if E = γ_{G; aggs}(E1) then keep, per group g, the count n, the non-null count k and the sum s
L9      for each group g of a tuple in supp(ΔE1): add -1 to the old row of g and +1 to the new row of g
```

Renaming passes the change through with new attribute names, and a product is a join with no common attribute. At line L6, monus is the bag difference, $\max(0, m - n)$, and min is the bag intersection. At line L7, $[x]$ is 1 if $x$ holds and 0 if not. At line L9, a group with no rows before the update has no old row to remove, and a group with no rows after it has no new row to add. With no grouping attributes the single result row always exists, as in SQL.

**Why it works.** The proof is by induction on $E$. Lines L2 to L4 hold because selection, projection and union are linear: they act on each tuple's weight on its own, so $f(X + \Delta X) = f(X) + f(\Delta X)$. Line L5 holds because the join is bilinear, so $(E_1 + \Delta E_1) \bowtie (E_2 + \Delta E_2)$ expands into $E_1 \bowtie E_2$ and the three terms of the rule. This is the product rule of [finite differences](/finite-differences/), $\Delta(fg) = \Delta f \cdot g + f \cdot \Delta g + \Delta f \cdot \Delta g$. Lines L6 and L7 are not linear, so they use the definition: the new weight minus the old weight, and only tuples whose input weight changes can change. Line L9 removes the old row of each changed group and adds its new one, and the summary $(n, k, s)$ of a group after the update is its old summary plus the summary of the change, because counts and sums are linear.

**Cost.** Lines L1 to L4 cost $O(1)$ per changed tuple in the worst case and keep no memory. Line L5 must store both old inputs, and with a hash index on the join attributes each changed tuple costs $O(1)$ expected time plus its number of matches, which can be the size of the other input. Lines L6, L7 and L9 keep one counter per distinct tuple or one summary per group, in a hash map, and cost $O(1)$ expected time per changed tuple. The reference code on this page computes the old values of the subexpressions from scratch, which is simpler to check and much slower. Real systems store them.

**Example.** Take $R(A, B) = \{(1, 10), (2, 10), (3, 20)\}$ and $S(B, C) = \{(10, x), (20, y)\}$, so $R \bowtie S = \{(1, 10, x), (2, 10, x), (3, 20, y)\}$. The update inserts $(4, 20)$ into $R$, deletes $(1, 10)$ from $R$, and inserts $(20, z)$ into $S$. Line L5 gives three terms.

| term | tuples and weights |
|---|---|
| $\Delta R \bowtie S$ | $(4, 20, y)$ +1, $(1, 10, x)$ -1 |
| $R \bowtie \Delta S$ | $(3, 20, z)$ +1 |
| $\Delta R \bowtie \Delta S$ | $(4, 20, z)$ +1 |

Their sum, added to the old view, gives $\{(2, 10, x), (3, 20, y), (3, 20, z), (4, 20, y), (4, 20, z)\}$, which is $R \bowtie S$ on the new tables. Now group the join by $B$ with $n = $ COUNT(\*) and $s = $ SUM($A$). The old view is $\{(10, 2, 3), (20, 1, 3)\}$. Lines L8 and L9 touch groups 10 and 20 and give the change $-(10, 2, 3) + (10, 1, 2) - (20, 1, 3) + (20, 4, 14)$.

## Classic examples

- [Incremental view maintenance](/incremental-view-maintenance/) evaluates DELTA after each transaction. Its counting algorithm is the set case: it keeps the weight of each tuple as a count of derivations and applies line L7 at the end.
- [Semi-naive evaluation](/semi-naive-evaluation/) of [Datalog](/datalog/) applies line L5 to each rule in each round: only joins with at least one new fact can make new facts.
- The [DRed algorithm](/dred-algorithm/) applies the rules to recursive views, where deletions need a step that derives tuples again.
- [Higher-order IVM](/higher-order-ivm/) notes that $\Delta E$ is itself a query, with a delta of its own, and stores the deltas of deltas so that each update costs only lookups and additions.
- [DBSP](/dbsp/) states lines L2 to L5 as two theorems: the delta of a linear operator is the operator itself, and the delta of a bilinear operator has the three terms of line L5.

## Variations

- **Two terms for the join.** Since $\Delta E_1 \bowtie E_2 + \Delta E_1 \bowtie \Delta E_2 = \Delta E_1 \bowtie (E_2 + \Delta E_2)$, line L5 can read the new value of $E_2$ and drop the third term. In the example, $\Delta R \bowtie S_{\mathrm{new}} + R \bowtie \Delta S$ gives the same four weights.
- **Separate insertions and deletions.** The older rules for sets and bags give two expressions per operator, one for the inserted tuples and one for the deleted tuples, in place of one signed change.
- **Rules for the state after the update.** If the base tables already hold the new values, each old value is written as the new value minus the change, which is the *past query* of deferred maintenance.
- **Other aggregates.** AVG is SUM divided by COUNT, so it follows from line L8. MIN and MAX have a rule for insertions (compare with the old value) but not for deletions: deleting the current minimum needs the other rows of the group.
- **Outer joins.** A left outer join is the join plus the left rows with no match, padded with NULL. Its change has the part of line L5 and a part for the left rows whose number of matches goes from 0 to more than 0 or back, found as at line L7.

## Pitfalls

- **Dropping the term $\Delta R \bowtie \Delta S$.** It is easy to forget that new tuples on both sides meet each other. In the example, the sum of the first two terms misses $(4, 20, z)$.
- **Evaluating a rule in the wrong state.** The three terms of line L5 read the old $R$ and $S$. If the update is applied first and the same terms read the new tables, the example gives $(4, 20, z)$ weight 3 in place of 1. Colby and others show the same fault for a projection of a join and for a difference.
- **Treating difference as linear.** Monus is not linear: with $R = \{(5, 1)\}$ and $T = \{(5, 1), (5, 1)\}$, the view $R \setminus T$ is empty, and deleting one copy from $T$ leaves it empty, but $\Delta R - \Delta T$ gives $(5, 1)$ weight +1. Line L6 uses the old weights to get 0.
- **Duplicate elimination without counts.** Line L7 needs the old weight of each tuple below $\delta$. A view that stores only the set result cannot tell whether a deleted tuple had another derivation.
- **Self-joins.** In $R \bowtie R$ both inputs change together. Line L5 handles this if $\Delta E_1$ and $\Delta E_2$ are both $\Delta R$, but code that changes one copy of $R$ at a time must read the other copy at the matching state.
- **NULL keys.** Under SQL a NULL join attribute matches nothing, in the change as in the table. The rules must use the same join test as the query, or the view drifts from the query.

## Exercises

1. Give the rule for the semijoin $E_1 \ltimes E_2$ under set semantics. Which old values does it need?
2. Prove the two-term form of the join rule, and give the form that reads the new value of $E_1$ in place of $E_2$.
3. Find two tables and one deletion for which MIN of a group cannot be found from the old view and the change alone.
4. A view is $\pi_A(R \bowtie S)$ under bag semantics. Show that the rules need no count of derivations, and say what extra state the set version needs.

## References
