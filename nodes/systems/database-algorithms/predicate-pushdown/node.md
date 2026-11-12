---
tag: 75V2SP
kind: technique
slug: predicate-pushdown
name: Predicate pushdown
aliases:
- selection pushdown
- filter pushdown
- pushing selections down
area: systems/database-algorithms
level: intro
summary: "Rewrite a query plan so that each selection runs as early as the algebraic laws allow: below joins, projections and outer joins on the preserved side."
prereqs: [relational-algebra, query-plan]
see_also: [query-optimization, selectivity, relational-join, semijoin, zone-map, magic-sets, iterator-model, cost-model]
sources:
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2008)
    locator: Chapter 16, the algebraic laws for improving query plans (laws for selection, pushing selections, laws for joins and products)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: Chapter 15 (relational algebra equivalences and their use in a query optimizer)
  - paper: doi:10.1145/170035.170078
    title: Joseph M. Hellerstein and Michael Stonebraker, Predicate migration, optimizing queries with expensive predicates, Proceedings of ACM SIGMOD 1993, 267 to 276
    locator: the rank of a predicate, (selectivity minus 1) divided by cost per tuple, and the predicate migration algorithm
  - paper: "César A. Galindo-Legaria and Arnon Rosenthal, Outerjoin simplification and reordering for query optimization, ACM Transactions on Database Systems 22(1) (1997)"
    title: Outerjoin simplification and reordering for query optimization
    locator: the rule that a null-rejecting predicate turns an outer join into an inner join, and the valid reorderings of outer joins
---

Predicate pushdown rewrites a [query plan](/query-plan/) so that each selection is applied as early as possible: below the joins, below the projections, and into the scans. The rewrite is correct because of a few laws of the [relational algebra](/relational-algebra/), and it is the first rule of almost every [query optimizer](/query-optimization/), because a filter applied early shrinks every result above it. The laws have exact conditions: a filter may not cross to the null-supplying side of an outer join, and an expensive or nondeterministic filter should not always move down.

## In plain words

Suppose you want the names of the employees in Paris. One way is to pair every employee with every department and then throw away the pairs that do not fit. A better way is to keep only the Paris departments first, and only then match the employees to them. The answer is the same, and the work is much smaller.

Predicate pushdown does this to a whole plan. Each filter moves down the tree, past the steps that do not change what the filter sees, until it reaches the table it reads, or a step that it must not pass. A filter that reads columns of two tables stops at the join of those tables and becomes the join condition.

## When it applies

- The plan has a selection above a join, a product or a projection, and the selection reads columns of only one input. The usual source is the SQL `WHERE` clause, which the parser puts above the product of all tables in `FROM`.
- A conjunction mixes conditions on one table with join conditions. Each conjunct moves on its own.
- The scan can evaluate a filter more cheaply than the operators above it: an index or a [zone map](/zone-map/) skips whole blocks, a columnar file format skips row groups, or a remote source filters before it sends the data.
- The predicate is cheap and deterministic. For costly ones, the rank rule below decides the place.

## The template

`PUSH(t, P)` returns a plan equivalent to $\sigma_P(t)$, where $P$ is a set of conjuncts that come from above $t$ and $\mathrm{attrs}(p)$ is the set of attributes that $p$ reads. Call `PUSH(root, ∅)`.

```pseudo id=main
PUSH(t, P)
L1  if t is a stored relation then
L2      return σ_P(t)                         ▷ the identity when P = ∅
L3  if t = σ_Q(c) then
L4      return PUSH(c, P ∪ Q)                 ▷ split the cascade of selections
L5  if t = π_A(c) then
L6      return π_A(PUSH(c, P))               ▷ each p ∈ P reads only A
L7  if t = L ⋈_Q S then                      ▷ inner join; Q = ∅ is a product
L8      P_L ← {p ∈ P ∪ Q : attrs(p) ⊆ sch(L)};  P_S ← {p ∈ P ∪ Q : attrs(p) ⊆ sch(S)} − P_L
L9      K ← (P ∪ Q) − P_L − P_S              ▷ conjuncts that read both sides
L10     return PUSH(L, P_L) ⋈_K PUSH(S, P_S)
    ▷ otherwise t = L ⟕_Q S, a left outer join with S null-supplying
L11 A ← {p ∈ P : attrs(p) ⊄ sch(L)};  Q_S ← {q ∈ Q : attrs(q) ⊆ sch(S), attrs(q) ⊄ sch(L)}
L12 return σ_A( PUSH(L, P − A) ⟕_{Q − Q_S} PUSH(S, Q_S) )
```

**The laws.** Bag semantics: a relation is a multiset, $\sigma$ keeps the multiplicity of each tuple it keeps, and $\pi$ keeps duplicates. $\mathrm{sch}(E)$ is the set of attributes of $E$. For all $E, E_1, E_2$:

1. $\sigma_{p \wedge q}(E) = \sigma_p(\sigma_q(E))$.
2. $\sigma_p(E_1 \bowtie_\theta E_2) = \sigma_p(E_1) \bowtie_\theta E_2$ if $\mathrm{attrs}(p) \subseteq \mathrm{sch}(E_1)$, and the mirror law for $E_2$.
3. $\sigma_\theta(E_1 \times E_2) = E_1 \bowtie_\theta E_2$, and $\sigma_p(E_1 \bowtie_\theta E_2) = E_1 \bowtie_{\theta \wedge p} E_2$.
4. $\sigma_p(\pi_A(E)) = \pi_A(\sigma_p(E))$ if $\mathrm{attrs}(p) \subseteq A$.
5. $\sigma_p(E_1 ⟕_\theta E_2) = \sigma_p(E_1) ⟕_\theta E_2$ if $\mathrm{attrs}(p) \subseteq \mathrm{sch}(E_1)$.
6. $E_1 ⟕_{\theta \wedge q} E_2 = E_1 ⟕_\theta \sigma_q(E_2)$ if $\mathrm{attrs}(q) \subseteq \mathrm{sch}(E_2)$.

*Proofs.* (1) A tuple passes both filters if and only if it passes the conjunction, with the same multiplicity. (2) A pair $(t_1, t_2)$ occurs in $E_1 \bowtie_\theta E_2$ with multiplicity $m_1(t_1) \, m_2(t_2)$ when $\theta(t_1, t_2)$ holds. Since $p$ reads only attributes of $E_1$, $p(t_1 t_2) = p(t_1)$, so the pair survives on the left side exactly when $t_1$ survives $\sigma_p$ on the right side, with the same multiplicity. (3) is the definition of the join. (4) Each tuple $t$ of $E$ gives the tuple $t[A]$, and $p(t) = p(t[A])$ because $p$ reads only $A$. (5) Each output tuple of a left outer join comes from one tuple $t_1$ of $E_1$: either $t_1$ with a match, or $t_1$ padded with nulls. Whether $t_1$ has a match does not depend on $p$, and $p$ reads only the part $t_1$, so $\sigma_p$ keeps the tuples from $t_1$ if and only if $p(t_1)$ holds. (6) The matches of $t_1$ on both sides are the tuples $t_2$ with $\theta(t_1, t_2) \wedge q(t_2)$, so $t_1$ is padded on both sides exactly when this set is empty. $\square$

**Walk-through and correctness.** By induction on the tree, `PUSH(t, P)` is equivalent to $\sigma_P(t)$. Line L2 is the claim itself. L4 uses law 1. L6 uses law 4; its condition holds because a predicate above $\pi_A$ can read only $A$. L8 to L10 use laws 1, 2 and 3: each conjunct that reads one side moves into that side, and the rest become the join condition. L11 and L12 use law 5 for the conjuncts of $P$ that read only the preserved side $L$, and law 6 for the conjuncts of the `ON` condition that read only $S$; all other conjuncts stay where they were. Each predicate moves at most once per tree node, so the time is $O(|t| \cdot |P|)$ for a tree of $|t|$ nodes.

**Where pushdown is not valid.**

- **A `WHERE` predicate on the null-supplying side.** Take $R = \{(a{=}1), (a{=}2)\}$, $S = \{(c{=}1, d{=}1), (c{=}2, d{=}5)\}$ and `R LEFT JOIN S ON a = c WHERE d = 1`. The answer is the single tuple $(1, 1, 1)$. If $d = 1$ moves into $S$, then $a = 2$ has no match and comes back as $(2, \text{null}, \text{null})$. The fix is outer join simplification (Galindo-Legaria and Rosenthal, 1997): a predicate that is false on nulls, such as $d = 1$, removes every padded tuple, so the outer join can become an inner join, and then law 2 applies.
- **An `ON` predicate on the preserved side.** `R LEFT JOIN S ON a = c AND a > 1` keeps the tuple $a = 1$, padded. Moving $a > 1$ into $R$ removes it.
- **Aggregation.** A predicate on grouping columns may move below a grouping; a predicate on an aggregate (`HAVING SUM(x) > 10`) may not.
- **Nondeterministic predicates.** `random() < 0.5` above a join of $R$ and $S$ flips one coin per output pair. Below the join it flips one coin per tuple of $R$, and all pairs of one tuple share the coin. The expected size is the same but the distribution differs, so the rewrite changes the meaning of the query.
- **Expensive predicates.** A user-defined function that costs a second per call should not run on every tuple of a large table if a selective join above it would leave only a few tuples. Hellerstein and Stonebraker (1993) define the *rank* of a filter with selectivity $s$ and cost $c$ per tuple as $(s - 1)/c$ and place filters by rank (predicate migration).

**The rank rule.** For a stream of $n$ tuples and two independent filters $f$ and $g$, running $f$ first costs $n c_f + n s_f c_g$, and $g$ first costs $n c_g + n s_g c_f$. So $f$ first is at least as cheap if and only if $c_f (1 - s_g) \le c_g (1 - s_f)$, that is, after division by $c_f c_g > 0$, if and only if $(s_f - 1)/c_f \le (s_g - 1)/c_g$. By exchanges of adjacent filters, a sequence of filters on one stream has minimum expected cost when it is sorted by increasing rank. Cheap filters have a rank near $-\infty$ and go first, which is plain pushdown.

## Classic examples

- **Products into joins.** $\sigma_{a<10 \wedge c<5 \wedge b=c}(R \times S)$ becomes $\sigma_{a<10}(R) \bowtie_{b=c} \sigma_{c<5}(S)$. With 200 tuples in each relation ($a$ uniform in 0 to 99, $b$ and $c$ uniform in 0 to 19, seed 5), the product has 40000 tuples, the join $R \bowtie_{b=c} S$ without the filters has 2069, and the pushed plan joins 13 tuples with 67 tuples and produces only the 24 result tuples. This turns a [product](/relational-algebra/) into a [join](/relational-join/) that a [hash join](/hash-join/) can run.
- **Filters into the scan.** A pushed filter on an indexed column becomes an index lookup, and a filter on a column with a [zone map](/zone-map/) skips each block whose minimum and maximum exclude the constant.
- **Implied predicates.** From $R.b = S.c$ and $R.b < 5$ the optimizer can derive $S.c < 5$ and push it into $S$ as well. This moves a filter across a join, which the laws alone do not do.
- **Semijoin reduction.** A [semijoin](/semijoin/) or a Bloom filter built on one input of a join is a predicate pushed into the other input: "keep the tuples whose key occurs on the other side".
- **Magic sets.** In recursive Datalog, [magic sets](/magic-sets/) push the constants of a query into the recursive rules, which is pushdown through recursion.

## Variations

- **Projection pushdown.** Drop each column as soon as no operator above needs it. This shrinks the tuples, not their number, and in a column store it decides which columns are read at all.
- **Pushdown into sources.** A federated or distributed engine sends the filter to the remote database or to the storage layer, so that less data crosses the network.
- **Predicate migration.** For expensive predicates, choose the place of each filter in the plan by rank and by the cost of the joins around it, instead of always the lowest place.
- **Pulling up.** The inverse rewrite moves a predicate up, for example to share it between two subqueries or to make a [materialized view](/materialized-view/) match a query.

## Pitfalls

- **Outer joins.** Do not push a `WHERE` conjunct on the null-supplying side, nor an `ON` conjunct on the preserved side (line L11 keeps both in place). Check for null-rejection first, and turn the outer join into an inner join when the check passes.
- **Nulls and NOT.** In SQL a comparison with null is unknown, and `WHERE` drops unknown. A rewrite that turns $\neg(a = 1)$ into "everything except $a = 1$" adds the null rows by mistake.
- **Costly user-defined functions.** Pushing them below a selective join can multiply their calls. Use the rank.
- **Side effects and errors.** A predicate that can raise an error, such as a division by a column that is zero only in rows that a join removes, can fail after pushdown on a query that ran before. Some systems guard such predicates.
- **Correlation between filters.** Rules about order use selectivities; if these come from wrong independence assumptions ([selectivity](/selectivity/)), the chosen order of filters may be poor, but the result stays correct.

## Exercises

1. Prove that $\sigma_p(E_1 \cup E_2) = \sigma_p(E_1) \cup \sigma_p(E_2)$ and $\sigma_p(E_1 - E_2) = \sigma_p(E_1) - E_2$ for bags, where $-$ subtracts multiplicities down to 0.
2. Give a relation $R(g, x)$ and the query $\sigma_{s > 10}(\gamma_{g, \, s = \mathrm{SUM}(x)}(R))$ for which moving the filter as $x > 10$ below the grouping changes the answer. Then show that a filter on $g$ may move.
3. For a full outer join $E_1 ⟗_\theta E_2$, which conjuncts of a `WHERE` clause may move into either input? Prove your answer or give counterexamples.
4. Three filters on one stream have $(s, c) = (0.5, 1)$, $(0.1, 10)$ and $(0.9, 0.1)$. Find the order of minimum expected cost by the rank rule, and check it against all six orders.

## References
