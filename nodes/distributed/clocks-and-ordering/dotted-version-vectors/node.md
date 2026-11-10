---
tag: Q366JY
kind: data-structure
slug: dotted-version-vectors
name: Dotted version vectors
aliases:
- DVV
area: distributed/clocks-and-ordering
level: advanced
summary: A version vector over server ids plus one dot that names the write itself, so a key-value store keeps exactly the concurrent writes, with no lost update and no sibling explosion.
model: asynchronous-model
complexity:
  vars: {s: the number of server identifiers, k: the number of siblings}
  time: {worst: Θ(s k^2)}
  space: {extra: Θ(s k)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2010
  people: [Nuno Preguiça, Carlos Baquero, Paulo Sérgio Almeida, Victor Fonte, Ricardo Gonçalves]
  note: The authors described dotted version vectors in an arXiv report in 2010, and Riak 2.0 adopted them.
prereqs: [version-vectors, vector-clocks]
see_also: [version-vectors, mv-register, dynamo-style-replication, interval-tree-clocks, leaderless-replication, anti-entropy, eventual-consistency]
sources:
  - url: "https://arxiv.org/abs/1011.5808"
    title: Nuno Preguiça, Carlos Baquero, Paulo Sérgio Almeida, Victor Fonte and Ricardo Gonçalves, Dotted version vectors, logical clocks for optimistic replication, arXiv 1011.5808, 2010
    locator: Section 3.2 (lost update with per-server vectors), Section 3.3 (per-client vectors), Section 4 (sync and update), Section 5 (definition, order, update and correctness)
  - paper: doi:10.1145/2332432.2332497
    title: Nuno Preguiça, Carlos Baquero, Paulo Sérgio Almeida, Victor Fonte and Ricardo Gonçalves, Brief announcement, efficient causality tracking in distributed storage systems with dotted version vectors, PODC 2012
    locator: pages 335 to 336
  - paper: doi:10.1007/978-3-662-43352-2_6
    title: Paulo Sérgio Almeida, Carlos Baquero, Ricardo Gonçalves, Nuno Preguiça and Victor Fonte, Scalable and accurate causality tracking for eventually consistent stores, DAIS 2014, LNCS 8460
    locator: pages 67 to 81
  - url: "https://docs.riak.com/riak/kv/latest/learn/concepts/causal-context/index.html"
    title: Riak KV documentation, Causal Context
    locator: sections on dotted version vectors and sibling explosion
---

A dotted version vector (DVV) is a logical clock for a replicated key-value store. It is a [version vector](/version-vectors/) with one entry per server, plus one *dot* $(r, n)$ that names the write itself: the $n$-th write coordinated by server $r$. The dot need not be contiguous with the vector, so a clock can say "everything up to 3 from $r$, and also write 5 of $r$". With this one extra pair, a server keeps exactly the writes that are truly concurrent, with only one entry per server. Preguiça, Baquero, Almeida, Fonte and Gonçalves described DVV in 2010, and Riak 2.0 uses them.

## In plain words

In a store such as Riak, clients write through a few servers. A plain version vector with one counter per server gets confused when two clients write through the same server without reading each other's writes. The second write gets a bigger counter, so it looks newer, and the first write is thrown away.

A dotted version vector fixes this with one small addition. Each write carries the usual row of counters, which says what the client had read, and also a separate label for the write itself. The label is not merged into the row unless it is the next number. So the store can see that the second write did not know about the first one, and it keeps both as siblings. A later client that reads both and writes once replaces both.

## The abstract type

The setting is the [asynchronous model](/asynchronous-model/) with a set of servers that have unique identifiers and any number of clients. Clients talk to servers, and servers exchange data with [anti-entropy](/anti-entropy/). For one key, each server keeps a set of *siblings*, pairs of a clock and a value. The operations are:

- GET at server $r$: return the values of the siblings and a *context*.
- PUT$(ctx, v)$ at server $r$: store $v$ as a write that has seen the context $ctx$ of an earlier GET.
- SYNC of two servers: both end with the same siblings.

The specification uses causal histories. Each write $u$ has the history $H(u) = \{u\} \cup$ (the histories of the siblings that the client read). A server must keep exactly the writes whose history no other known write strictly contains. A write must never be dropped unless a kept write has it in its history (no lost update), and two kept writes must never be ordered (no false conflict).

## Representation

A clock is a map $vv$ from server identifiers to counters and an optional dot $(r, n)$. The paper writes an entry with a dot as a triple $(r, m, n)$ with $n > m$. The causal history of a clock is

$$C[(vv, (r, n))] = \{(i, k) : 1 \le k \le vv[i]\} \cup \{(r, n)\}.$$

So $C[(r, m)] = \{r_1, \ldots, r_m\}$ and $C[(r, m, n)] = \{r_1, \ldots, r_m\} \cup \{r_n\}$. A clock is in normal form if its dot is not the next counter of the vector: a dot $(r, vv[r] + 1)$ is folded into $vv$. The order is inclusion of histories.

## Operations

```pseudo id=main
LEQ(X, Y)                                  ▷ C[X] ⊆ C[Y], both in normal form
L1  for each (i, m) in vv_X do if m > vv_Y[i] then return false
L2  if X has a dot d and d ∉ C[Y] then return false     ▷ d = (i, n) ∈ C[Y] iff n ≤ vv_Y[i] or d is the dot of Y
L3  return true

SYNC(S1, S2)                               ▷ two sets of siblings
L4  return {x ∈ S1 : no y ∈ S2 with x < y} ∪ {y ∈ S2 : no x ∈ S1 with y < x}

CEILING(S)                                 ▷ the context of a set of clocks
L5  for each id i: ctx[i] ← the largest counter of i in a vector entry or a dot of S

UPDATE(ctx, S_r, r)                        ▷ the clock of a new write at server r
L6  n ← CEILING(S_r)[r] + 1
L7  return the clock with vector ctx and dot (r, n), in normal form

PUT(ctx, v) at server r
L8  u ← UPDATE(ctx, S_r, r)
L9  S_r ← SYNC({(u, v)}, S_r)

GET() at server r
L10 return the values of S_r, and CEILING(S_r) as the context
```

The new write gets the client's context as its vector and a fresh dot from the server. Line L9 then removes exactly the siblings that the client had read, and keeps the ones that it had not.

## Example

**The lost update of plain version vectors.** Two clients write $v_1$ and then $v_2$ through server $b$, each with an empty context. With one plain version vector per sibling, $v_1$ gets $\{(b,1)\}$ and $v_2$ gets $\{(b,2)\}$. Since $\{(b,1)\} \le \{(b,2)\}$, the store drops $v_1$, although no client read it. With DVV, $v_1$ gets $(b,0,1)$, which has normal form $\{(b,1)\}$, and $v_2$ gets $(b,0,2)$, whose history is $\{b_2\}$. Neither history contains the other, so both stay. A client that reads both gets the context $\{(b,2)\}$, and its next write replaces both.

**Sibling explosion.** Two clients $c_1$ and $c_2$ write in turn through server $r$. After each write, the writer does a GET. So each write has seen all writes except the last one of the other client. Write $k$ is $x_k$.

| write | context | DVV of the write | siblings with DVV | siblings with one vector per object |
|---|---|---|---|---|
| $x_1$ by $c_2$ | $\{\}$ | $(r, 0, 1) = \{(r,1)\}$ | $x_1$ | $x_1$ |
| $x_2$ by $c_1$ | $\{\}$ | $(r, 0, 2)$ | $x_1, x_2$ | $x_1, x_2$ |
| $x_3$ by $c_2$ | $\{(r,1)\}$ | $(r, 1, 3)$ | $x_2, x_3$ | $x_1, x_2, x_3$ |
| $x_4$ by $c_1$ | $\{(r,2)\}$ | $(r, 2, 4)$ | $x_3, x_4$ | $x_1, \ldots, x_4$ |
| $x_5$ by $c_2$ | $\{(r,3)\}$ | $(r, 3, 5)$ | $x_4, x_5$ | $x_1, \ldots, x_5$ |

With DVV the store keeps two siblings, which is the true number of concurrent writes. The write $x_3$ has history $\{r_1, r_3\}$, so it replaces $x_1$ and is concurrent with $x_2$, whose history is $\{r_2\}$. A store with one version vector per object and a list of sibling values knows only that the context $\{(r,1)\}$ is older than the object vector $\{(r,2)\}$. It cannot tell which siblings the client saw, so it keeps them all, and the list grows by one per write. The Riak documentation calls this sibling explosion.

The pair $\{(r,4)\}$ and $\{(r,3,5)\}$ is concurrent: the first has $r_4$, and the second has $r_5$.

## Correctness

The order test is exact on clocks in normal form. A prefix $r_1, \ldots, r_m$ fits inside another clock only if its vector reaches $m$, because a dot never fills the next gap. The store keeps three invariants. Each sibling's clock has exactly the true causal history of its write. The union of the histories of a server's siblings is a downset, a prefix for each server identifier. And this union holds every write that the server coordinated. The downset makes the context of a GET cover exactly what the client read. The third invariant makes the new dot fresh. Then the new clock has the true history, and SYNC keeps exactly the maximal writes. The full proof is below.

## Complexity

Let $s$ be the number of server identifiers and $k$ the number of siblings.

| operation | time |
|---|---|
| LEQ | $\Theta(s)$ |
| CEILING | $\Theta(s k)$ |
| PUT | $\Theta(s k)$ |
| SYNC of two sets of $k$ siblings | $\Theta(s k^2)$ |

Each clock has at most $s$ entries and one dot, so a key with $k$ siblings stores $O(s k)$ integers. The size depends on the servers, not on the clients. A per-client version vector is also exact, but it has one entry per client that ever wrote the key.

## Variants

- **Per-client version vectors.** Exact, but the vectors grow with the number of clients, and pruning them can cause the errors that it was meant to avoid.
- **Dotted version vector sets.** The DAIS 2014 paper stores all siblings of a key under one shared vector, with one dot per sibling, which is more compact than one full clock per sibling.
- **Multi-value registers.** A [multi-value register](/mv-register/) has the same semantics, all concurrent writes are kept, and DVV are one way to build it.
- **[Interval tree clocks](/interval-tree-clocks/).** They solve a different problem with similar tools: the set of identifiers itself changes, and identifiers are split and joined.

## When to use it

Use DVV in a [leaderless](/leaderless-replication/) or [Dynamo-style](/dynamo-style-replication/) store in which servers coordinate writes for many clients and concurrent writes must be kept as siblings. Clients should send the context of their last GET with each PUT. If the store resolves conflicts by [last-writer-wins](/last-writer-wins/), it does not need DVV. If each writer is itself a replica, plain [version vectors](/version-vectors/) are enough.

## Pitfalls

- **Writing without a context.** A PUT with an empty context is concurrent with everything stored, so each blind write adds a sibling. DVV keeps these writes correctly, but the application must still read and merge the siblings.
- **Merging the dot.** A dot $(r, n)$ with $n > vv[r] + 1$ must stay separate. Folding it into the vector claims the writes between $vv[r]$ and $n$, which the writer never saw, and later writes can then be lost.
- **A fresh dot needs the server's own writes.** The counter of line L6 must come from the coordinating server's own data. A server that loses its data and restarts with the same identifier can reuse dots.
- **Contexts from another key.** A context describes one key. Using it for a different key gives meaningless comparisons.

## Implementations

## History

Nuno Preguiça, Carlos Baquero, Paulo Sérgio Almeida, Victor Fonte and Ricardo Gonçalves described dotted version vectors in an arXiv report in 2010. They showed that version vectors with one entry per server lose updates when servers act for clients, and that one entry per client does not scale. A brief announcement appeared at PODC 2012, and a paper on a more compact form appeared at DAIS 2014. Riak adopted dotted version vectors in version 2.0, with the bucket property `dvv_enabled`.

## References
