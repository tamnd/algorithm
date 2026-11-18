---
tag: 0ABZ30
kind: algorithm
slug: higher-order-ivm
name: Higher-order incremental view maintenance
aliases:
- DBToaster
- recursive IVM
area: databases/stream-and-incremental-processing
level: research
summary: "Materialize the deltas of a view, the deltas of those deltas and so on, so each update is applied by simple arithmetic on maps."
solves: [view-maintenance]
model: word-ram
complexity:
  vars: {k: the number of atoms of the query, m: the largest number of entries in one map}
  time: {worst: "O(2^k m)", average: "O(2^k m)", best: "O(2^k)"}
  space: {extra: "O(2^k m)"}
properties: {deterministic: true, exact: true, online: true, external: false, in_place: false, recursive: false}
history:
  year: 2010
  people: [Christoph Koch]
  note: "Koch showed at PODS 2010 that the delta of a query over a ring of databases is a simpler query with its own delta, and that materializing the whole hierarchy of deltas makes each update cheap."
prereqs: [incremental-view-maintenance, delta-rules]
see_also: [delta-rules, dbsp, incremental-view-maintenance, differential-dataflow, self-maintainable-view, materialized-view, provenance-semirings, finite-differences]
sources:
  - paper: doi:10.1145/1807085.1807100
    title: "Christoph Koch, Incremental query evaluation in a ring of databases, Proceedings of ACM PODS 2010, pages 87 to 98"
    locator: "the ring of databases with integer multiplicities, the aggregation calculus and its delta queries, the drop in degree with each delta, and the result that maintaining all higher-order deltas puts each update in NC0 for this calculus (the theorem number is not checked)"
  - paper: doi:10.14778/2336664.2336670
    title: "Yanif Ahmad, Oliver Kennedy, Christoph Koch and Milos Nikolic, DBToaster, higher-order delta processing for dynamic, frequently fresh views, PVLDB 5(10), 2012, pages 968 to 979"
    locator: "the viewlet transform, which compiles a query into a hierarchy of maps and one trigger program per relation and kind of update"
  - paper: doi:10.1007/s00778-013-0348-4
    title: "Christoph Koch, Yanif Ahmad, Oliver Kennedy, Milos Nikolic, Andres Nötzli, Daniel Lupei and Amir Shaikhha, DBToaster, higher-order delta processing for dynamic, frequently fresh views, The VLDB Journal 23(2), 2014, pages 253 to 278"
    locator: "the full compiler, with the choice and factorization of the maps, nested aggregates, and the experiments (general locator)"
---

Higher-order incremental view maintenance keeps a query result up to date by storing not only the result but also its delta with respect to each base relation, the deltas of those deltas, and so on, as a hierarchy of maps. Classic [incremental view maintenance](/incremental-view-maintenance/) applies [delta rules](/delta-rules/) once and evaluates the delta query, often a join, on every update. Here the delta query is itself maintained, so an update only looks up stored values, multiplies and adds. Koch (2010) gave the idea for queries over a ring of databases, and Ahmad, Kennedy, Koch and Nikolic (2012) call the transformation the *viewlet transform*, while [DBSP](/dbsp/) and [differential dataflow](/differential-dataflow/) keep the first-order delta and maintain the state of each operator instead.

## In plain words

Suppose you keep the total of a sum over a join of three tables. A new row arrives in one table. The change of the total is that row's value times a number that depends on the other two tables. Ordinary maintenance computes that number by a join every time. This algorithm keeps the number in a stored table, ready to read.

That stored table must also change when the other tables change. Its change again has the same form: a value times a number that depends on fewer tables. So you store those numbers too, and so on, until a number depends on no table at all.

After that, a new row only causes reads, products and sums in the stored tables. No join runs.

## The problem

The input is a query and a sequence of updates. The query is a sum over a natural join of base relations $R_1, \ldots, R_k$ with distinct names (no self-join), of the product of some attribute values $\mathit{VALS}$, grouped by attributes $F$:

$$Q[F] = \sum_{x \in R_1 \bowtie \cdots \bowtie R_k} \prod_{v \in \mathit{VALS}} x_v.$$

With $\mathit{VALS}$ empty, $Q$ is COUNT(\*). Each relation gives each tuple an integer weight. An update adds a weight $w$ to one tuple $t$ of one relation $R_j$: $w = 1$ is an insertion and $w = -1$ a deletion. A set is a Z-set with weights 0 and 1, and distinct maps a Z-set to a set, so sets and bags are special cases. After each update, the current value of $Q$ must be available.

## The algorithm

For a set $S$ of atoms, let $\mathrm{rem}$ be the other atoms and $\mathrm{Vars}(X)$ the attributes of the atoms in $X$. The map $M_S$ is the delta of $Q$ with respect to the atoms of $S$, with the attributes that connect $S$ to the rest as its key:

$$K_S = \mathrm{Vars}(\mathrm{rem}) \cap (\mathrm{Vars}(S) \cup F), \qquad M_S(y) = \sum_{z} \prod_{i \in \mathrm{rem}} R_i(y, z) \prod_{v \in \mathit{VALS},\ v \text{ summed}} z_v,$$

where $z$ ranges over the other attributes of $\mathrm{rem}$. Then $M_\emptyset$ is $Q$, and $M_S() = 1$ when $S$ holds all atoms. An update to $R_j$ changes $M_S$ only for $j \notin S$, and by the delta rule for a product its change is a lookup in $M_{S \cup \{j\}}$, which the update does not change.

```pseudo id=main
INIT()
L1  for each set S of atoms: M_S ← an empty map; M_all() ← 1

UPDATE(j, t, w)                                   ▷ add weight w to tuple t of R_j
L2  for each set S of atoms with j ∉ S do          ▷ any order: M_{S ∪ {j}} does not change
L3      S' ← S ∪ {j}
L4      for each entry (y', c) of M_{S'} that agrees with t on the attributes of R_j do
L5          y ← y' together with t, cut to the key K_S
L6          M_S[y] ← M_S[y] + w · c · (the product of the values of t in VALS that M_S sums)
L7          if M_S[y] = 0 then remove the entry y

RESULT(f)
L8  return M_∅[f] times the product of the values of f in VALS
```

The compiler of Ahmad et al. writes the loop of line L2 for each relation, at compile time, as a *trigger program*: a short list of statements of the form "map $\mathrel{+}=$ value times lookup". Line L4 with a hash index on the attributes of $K_{S'}$ that $t$ fixes reads only the matching entries.

## Example

The query is $Q = \sum A \cdot D$ over $R(A, B) \bowtie S(B, C) \bowtie T(C, D)$. The six maps below $Q$ are:

| map | key | definition |
|---|---|---|
| $M_R$ | $B$ | $\sum_{C, D} S(b, C)\, T(C, D)\, D$ |
| $M_S$ | $B, C$ | $\big(\sum_A R(A, b)\, A\big)\big(\sum_D T(c, D)\, D\big)$ |
| $M_T$ | $C$ | $\sum_{A, B} R(A, B)\, S(B, c)\, A$ |
| $M_{RS}$ | $C$ | $\sum_D T(c, D)\, D$ |
| $M_{RT}$ | $B, C$ | $S(b, c)$ |
| $M_{ST}$ | $B$ | $\sum_A R(A, b)\, A$ |

The trigger for an insertion of $(a, b)$ into $R$ is: $Q \mathrel{+}= a \cdot M_R(b)$; $M_S(b, c) \mathrel{+}= a \cdot M_{RS}(c)$ for each $c$; $M_T(c) \mathrel{+}= a \cdot M_{RT}(b, c)$ for each $c$; $M_{ST}(b) \mathrel{+}= a$. Five insertions give:

| update | change of $Q$ | other changes | $Q$ |
|---|---|---|---|
| $R(1, 10)$ | $1 \cdot M_R(10) = 0$ | $M_{ST}(10) = 1$ | 0 |
| $S(10, 20)$ | $M_S(10, 20) = 0$ | $M_T(20) = 1$, $M_{RT}(10, 20) = 1$ | 0 |
| $T(20, 5)$ | $5 \cdot M_T(20) = 5$ | $M_R(10) = 5$, $M_S(10, 20) = 5$, $M_{RS}(20) = 5$ | 5 |
| $R(2, 10)$ | $2 \cdot M_R(10) = 10$ | $M_S(10, 20) = 15$, $M_T(20) = 3$, $M_{ST}(10) = 3$ | 15 |
| $T(20, 7)$ | $7 \cdot M_T(20) = 21$ | $M_R(10) = 12$, $M_S(10, 20) = 36$, $M_{RS}(20) = 12$ | 36 |

The last update would cost first-order IVM a join of $R$ and $S$. Here it reads one entry, $M_T(20) = 3$. The check: the join has $(1 + 2) \cdot (5 + 7) = 36$ as its sum of $A \cdot D$. A later deletion of $R(1, 10)$ gives $Q = 36 - 1 \cdot M_R(10) = 24$.

## Correctness

The claim is that after every update each map equals its definition over the current relations. Since no relation name occurs twice, every map is linear in each relation. So adding $w$ to the weight of $t$ in $R_j$ changes $M_S$, for $j \notin S$, by $w$ times the sum with $R_j$ fixed to $t$. With the attributes of $t$ fixed, that sum is $M_{S \cup \{j\}}$ at the matching key, times the values of $t$ that $M_S$ sums over. $M_{S \cup \{j\}}$ does not contain $R_j$ and does not change, so the order of the maps in line L2 does not matter. Induction on the number of updates finishes the proof. The proof never uses positive weights, so the maps are exact for any order of signed updates. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

The costs are per update, in the [word RAM](/word-ram/) model with hash maps, so lookups take expected $O(1)$ time.

- **Time.** An update to $R_j$ touches the $2^{k-1}$ maps $M_S$ with $j \notin S$, and for each it visits the matching entries of one child map. When the update fixes the whole key of each child, as for the update of $T$ in the example, each map costs one lookup and the total is $O(2^k)$ expected time. In the worst case a child has $m$ matching entries, which gives $O(2^k m)$. These are bounds for each single update, in expectation over the hash function, not amortized.
- **Memory.** The maps hold at most $2^k m$ entries. A map can be much larger than the relations: $M_S$ in the example has an entry for each pair of a $B$ value and a $C$ value.
- **Reading.** RESULT costs $O(1)$ expected time per group. The query is never evaluated.

In Koch's calculus each delta lowers the degree of the query in the relations by one, so the hierarchy ends after $k$ levels with constants. He shows that for this calculus each update can be done with the full hierarchy in NC0, constant parallel time.

## Properties

- **Exact.** The maps are equal to their definitions after every update, not approximate.
- **Online, with constant work for many updates.** The work of an update does not depend on the size of the relations when each lookup has one match.
- **Order independent and safe for late data.** The maps depend only on the current weights. A late update, or a deletion that arrives before its insertion and leaves a weight of -1 for a while, is applied when it arrives, and the maps are exact for the weights at that moment.
- **No base relations.** The maps include the needed parts of the relations, so the view and its maps together are [self-maintainable](/self-maintainable-view/).

## Variants and improvements

- **Factorized maps.** $M_S$ in the example is the product of $M_{ST}$ and $M_{RS}$. A compiler can store such a map as the product of two smaller maps, which saves space and work.
- **Self-joins.** With a relation that occurs twice, the delta of a product has the extra term $\Delta R \cdot \Delta R$, and the child map changes during the update. The full viewlet transform handles this with the rules of the ring.
- **Choosing maps.** Not every map needs to be stored. A map can be computed from the relations at update time when that is cheaper, which mixes first-order and higher-order maintenance.
- **Nested aggregates and inequality joins.** The full compiler accepts a larger calculus, with nested aggregates and inequality joins, in which some deltas are not simpler than the query. For those parts a map is not always the cheapest choice.
- **Batches.** An update can carry many tuples. The same triggers apply, with a loop over the batch or with a join of the batch and the child map.
- **Other rings.** The construction needs only addition, multiplication and inverses for deletions, so it works for any ring of values, as in [provenance semirings](/provenance-semirings/) with negatives.

## When to use it

Use it for SUM and COUNT queries over joins that must be fresh after every update, with many small updates and a fixed query, such as live dashboards and order books. Prefer first-order [incremental view maintenance](/incremental-view-maintenance/) when the maps would be much larger than the relations, when updates come in large batches, or when the query uses MIN, MAX or distinct, which have no inverse.

## Pitfalls

- **Map blowup.** There are $2^k$ maps, and a map keyed by several attributes of different relations can hold a product of their domains. Check the key of each map before storing it.
- **Self-joins treated as distinct relations.** Renaming one copy of $R$ and updating only it gives a wrong result. Both copies change at once, and the $\Delta R \cdot \Delta R$ term is needed.
- **MIN and MAX.** They are not ring operations: a deletion of the current minimum cannot be undone by subtraction. These need the base data or a sorted structure per group.
- **Updates inside the loop.** Line L2 is correct in any order only because the child $M_{S \cup \{j\}}$ does not change. Code that also updates the children in the same pass must read the old values.
- **Floating-point values.** With floats, the sum of many additions and subtractions drifts, and an entry that should be 0 is not removed at line L7. Use exact numbers or remove entries below a tolerance.

## Implementations

## History

Koch (2010) set incremental view maintenance in a ring of databases, where tuples have integer multiplicities and deletions are insertions with negative weight. In that ring the delta of a query is again a query, of lower degree, so it can be maintained in the same way, and so on. Ahmad, Kennedy, Koch and Nikolic (2012) built a compiler that turns a SQL query into trigger programs over the maps by the viewlet transform, and showed large speedups over first-order maintenance in their experiments. Koch, Ahmad, Kennedy, Nikolic, Nötzli, Lupei and Shaikhha (2014) gave the full description of the compiler. Budiu, Chajed, McSherry, Ryzhyk and Tannen later gave [DBSP](/dbsp/), which keeps the first-order delta rules and adds streams and recursion.

## References
