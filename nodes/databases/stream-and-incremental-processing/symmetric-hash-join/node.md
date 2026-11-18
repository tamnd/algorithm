---
tag: 2VN9MN
kind: algorithm
slug: symmetric-hash-join
name: Symmetric hash join
aliases:
- pipelined hash join
- double pipelined hash join
area: databases/stream-and-incremental-processing
level: core
summary: "Keep a hash table for each input; each arriving tuple is inserted in its own table and probes the other, producing results at once."
solves: [relational-join]
model: word-ram
complexity:
  vars: {n: the number of tuples that have arrived from both inputs, T: the number of output tuples so far}
  time: {worst: "O(n^2)", average: "O(n + T)", best: "O(n + T)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: true, online: true, external: false, in_place: false, recursive: false}
history:
  year: 1991
  people: [Annita N. Wilschut, Peter M. G. Apers]
  note: "Wilschut and Apers described the join for dataflow query execution in a parallel main-memory system, so that both inputs of a join can be pipelined."
prereqs: [hash-join, hash-table]
see_also: [xjoin, sliding-window-join, hash-join, ripple-join, eddies, pipelining-and-materialization, iterator-model, grace-hash-join]
sources:
  - paper: "Annita N. Wilschut and Peter M. G. Apers, Dataflow query execution in a parallel main-memory environment, Proceedings of the First International Conference on Parallel and Distributed Information Systems (PDIS), 1991"
    title: Dataflow query execution in a parallel main-memory environment
    locator: the pipelining hash-join and its comparison with the simple hash-join (the page numbers are not confirmed here)
  - paper: "Zachary G. Ives, Daniela Florescu, Marc Friedman, Alon Levy and Daniel S. Weld, An adaptive query execution system for data integration, Proceedings of ACM SIGMOD 1999"
    title: An adaptive query execution system for data integration
    locator: the pipelined hash join of the Tukwila system and its strategies for memory overflow (the page numbers are not confirmed here)
  - paper: "Tolga Urhan and Michael J. Franklin, XJoin, a reactively-scheduled pipelined join operator, IEEE Data Engineering Bulletin 23(2), 2000, 27 to 33"
    title: "XJoin: a reactively-scheduled pipelined join operator"
    locator: "the description of the symmetric hash join as the starting point of XJoin, and its memory problem"
---

The symmetric hash join computes the equi-join of two inputs $R$ and $S$ while both inputs are still arriving. It keeps one [hash table](/hash-table/) on the join key for each input: an arriving tuple goes into the table of its own input and then probes the table of the other input, so each result is emitted as soon as its second tuple arrives. The classic [hash join](/hash-join/) is different: it must read all of its build input before it can emit the first result, but it keeps only one table. The [sliding window join](/sliding-window-join/) is the same scheme with tuples that expire, and [XJoin](/xjoin/) extends it to inputs that do not fit in memory.

## In plain words

Two people read out names from two lists, one name at a time, in any order and at any speed. You keep two card boxes, one for each list. When you hear a name from the first list, you file a card for it in the first box, and then you look in the second box for cards with the same name. Each card that you find there is a match, and you call it out at once.

You never wait for a list to end. A match is called out at the moment that its second name is read. The cost is that you keep a card for every name you have heard, from both lists, because a name that comes later can match any of them.

## The problem

The input is two relations $R$ and $S$ with the set $J$ of common attributes, delivered as one sequence of arrivals. Each arrival is a tuple of $R$ or a tuple of $S$, and the order and timing of the arrivals are not under the control of the join. The output is the natural join $R \bowtie S$ on $J$, as on the page [relational join problem](/relational-join/), under bag semantics: each pair of matching occurrences gives one output tuple. A NULL in a join attribute never matches, as in SQL.

The join must be *pipelined*: after each arrival, the output so far must be the join of the inputs seen so far. This matters when the inputs come over a slow network, when another pipelined operator produces them, or when a user wants the first answers early. A blocking join cannot do this, and the [iterator model](/iterator-model/) page and the page on [pipelining and materialization](/pipelining-and-materialization/) explain why a hash join blocks on its build input.

## The algorithm

```pseudo id=main
SYMMETRIC-HASH-JOIN(arrivals)          ▷ each arrival is (side, t) with side R or S
L1  H_R ← an empty hash table; H_S ← an empty hash table
L2  for each arrival (side, t), in arrival order do
L3      (own, other) ← (H_R, H_S) if side = R, else (H_S, H_R)
L4      k ← t[J]                       ▷ the values of the join attributes
L5      if some value of k is NULL then go to the next arrival      ▷ it can never match
L6      insert t into own under the key k
L7      for each tuple u in the bucket of k in other with u[J] = k do
L8          emit the combination of t and u
```

Line L6 inserts before line L7 probes, but the order of the two lines does not matter: the probe looks at the other table, and the tuple is put in its own table. Line L5 drops a tuple with a NULL key at once. An outer join could not do this, because it must still output such a tuple padded with NULLs.

The two inputs play the same role, which gives the join its name. There is no build phase and no probe phase. Every tuple is first a build tuple, for the tuples that come later from the other side, and then a probe tuple, for the tuples that came earlier.

## Example

$R(A, B)$ and $S(B, C)$ join on $B$. The arrivals come in this order.

| step | arrival | stored in | probes | output of the step |
|---|---|---|---|---|
| 1 | $R$: (1, 10) | $H_R$ | $H_S$, empty | none |
| 2 | $S$: (10, p) | $H_S$ | $H_R$, bucket 10 | (1, 10, p) |
| 3 | $R$: (2, 20) | $H_R$ | $H_S$, bucket 20 empty | none |
| 4 | $S$: (10, q) | $H_S$ | $H_R$, bucket 10 | (1, 10, q) |
| 5 | $R$: (3, 10) | $H_R$ | $H_S$, bucket 10 | (3, 10, p), (3, 10, q) |
| 6 | $S$: (20, r) | $H_S$ | $H_R$, bucket 20 | (2, 20, r) |

The steps emit 0, 1, 0, 1, 2 and 1 tuples, 5 in total, which is $R \bowtie S$. After step 6 the tables hold all 6 tuples. A classic hash join with $R$ as the build input must read all of $R$ first, so it can emit nothing before step 5, when the last tuple of $R$ arrives.

## Correctness

The claim is that after each arrival, the bag of emitted tuples equals $R_j \bowtie S_j$, the join of the first $j$ arrivals. Lines L6 and L1 keep the invariant that each table holds exactly the tuples of its input seen so far with a key free of NULL. When a tuple $t$ of $R$ arrives, the join grows by exactly $\{t\} \bowtie S_{j-1}$, because the bag join distributes over the union of bags, and this is what lines L7 and L8 emit. So every pair is emitted exactly once, at the arrival of the later of its two tuples, which is the earliest possible moment. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

The costs are per arriving tuple, in the [word RAM](/word-ram/) model, with $n$ the number of tuples that have arrived from both inputs.

- **Time.** With a hash table of expected $O(1)$ time per insertion and per bucket lookup, an arrival costs expected $O(1 + m)$, where $m$ is the number of results it emits. Over $n$ arrivals the expected total is $O(n + T)$ for $T$ results, which is optimal because each result must be written. This bound is in expectation over the hash function, not amortized. In the worst case, when all keys collide in one bucket, a probe compares with all stored tuples of the other side, and the total is $O(n^2)$ comparisons.
- **Memory.** All $n$ tuples, minus those with NULL keys. A classic hash join keeps only the smaller input. An unbounded join cannot keep less in general, because a stored tuple can match any later tuple (see the end of the proof page).
- **With a window.** If each input keeps only its last $W$ tuples, the memory is at most $2W$ tuples, and each arrival also removes the tuple that leaves its window in expected $O(1)$ time. This is the [sliding window join](/sliding-window-join/).

## Properties

- **Pipelined and non-blocking.** The first result comes out with the first matching pair. The join never waits for the end of an input.
- **Order independent.** The final output does not depend on the order of the arrivals. Only the time at which each result appears does.
- **Exact under bag semantics.** Duplicates multiply as in SQL, and NULL keys never match.
- **Symmetric.** Neither input must be the smaller one, and the join does not need to know the sizes in advance.

## Variants and improvements

- **Memory overflow.** When the two tables do not fit in memory, a part of them must go to disk. [XJoin](/xjoin/) partitions both tables by a hash of the key, moves whole partitions to disk, joins the disk parts while the inputs are blocked, and uses timestamps so that no pair is emitted twice. Ives et al. (1999) used the same join in the Tukwila data integration system and gave other strategies for overflow.
- **Windows and expiration.** For unbounded streams, each tuple is kept only while it is inside a window, which gives the [sliding window join](/sliding-window-join/).
- **Many inputs.** The [ripple join](/ripple-join/) of online aggregation reads samples of both inputs in turn and joins each new sample with all earlier samples of the other input. Its hash form is a symmetric hash join. The [eddies](/eddies/) of adaptive query processing keep one hash index per input and route tuples between them, which generalizes the same idea to more than two inputs.
- **Outside streams.** The join is also used in ordinary query plans: in parallel and distributed engines, where the inputs come from other nodes at different speeds, and in any plan where the user wants early results. It is not only a stream operator.

## When to use it

Use it when both inputs arrive slowly or in bursts, when the first results matter more than the total time, or when neither input is known to be small. Use it on streams only with a window or another bound, because the memory grows without limit. Prefer a classic [hash join](/hash-join/) when one input is small and fully available, since it keeps one table instead of two, and a [Grace hash join](/grace-hash-join/) when the inputs are large and on disk.

## Pitfalls

- **Unbounded memory.** On streams the tables grow forever unless tuples expire. Without a window or a punctuation that closes a key, the join will run out of memory.
- **Late data in windowed joins.** In a window join, a tuple that arrives after the tuples it should match have expired misses those matches. A system must either keep tuples until a watermark says that no earlier data can come, or accept that late data loses results. Heuristic watermarks can be wrong, so this is a choice of the system and not a property of the join.
- **Outer joins.** Line L5 drops a tuple with a NULL key. An outer join must keep and pad it, and it can emit an unmatched tuple only when it knows that no match will come, which needs the end of the other input or a punctuation.
- **Double counting in variants.** Any variant that moves tuples to disk and joins them later can emit a pair twice, once from memory and once from disk. [XJoin](/xjoin/) solves this with timestamps.

## Implementations

## History

Wilschut and Apers (1991) described this join for dataflow query execution in a parallel main-memory database system. A hash join with one table pipelines only its probe input, and they wanted both inputs of a join to be pipelined so that a whole tree of joins could run at once. Ives, Florescu, Friedman, Levy and Weld (1999) used it in the Tukwila system for data integration over the network, where remote sources are slow and unpredictable, and added ways to handle memory overflow. Urhan and Franklin (2000) took it as the base of [XJoin](/xjoin/), which spills partitions to disk and uses the time that the inputs are blocked.

## References
