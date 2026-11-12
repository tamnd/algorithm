---
tag: DAQ627
kind: algorithm
slug: consistent-hashing
name: Consistent hashing
aliases:
- Karger consistent hashing
area: systems/load-balancing-and-hashing
level: core
summary: "Hash servers and keys onto one ring and give each key to the next server point clockwise. When a server joins or leaves, only about 1/n of the keys move, against almost all with hash mod n."
solves: [load-balancing-problem]
model: word-ram
complexity:
  vars: {n: the number of servers, v: the number of points per server}
  time: {worst: O(log(n v))}
  space: {extra: O(n v)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1997
  people: [David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine, Daniel Lewin]
  note: Karger, Lehman, Leighton, Panigrahy, Levine and Lewin defined consistent hashing at STOC 1997 to spread web caches; it became the basis of Akamai, of Chord and of Dynamo.
prereqs: [hash-function, load-balancing-problem]
see_also: [hash-ring, virtual-nodes, consistent-hashing-max-load-bound, rendezvous-hashing, jump-consistent-hash, maglev-hashing, bounded-load-consistent-hashing, chord]
sources:
  - paper: doi:10.1145/258533.258660
    title: David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine and Daniel Lewin, Consistent hashing and random trees, distributed caching protocols for relieving hot spots on the World Wide Web, STOC 1997
    locator: pp. 654 to 663, Section 4 (ranged hash functions; the properties balance, monotonicity, spread and load; the construction with kappa log C points per bucket on the unit interval, Theorem 4.1)
  - paper: doi:10.1145/383059.383071
    title: Ion Stoica, Robert Morris, David Karger, M. Frans Kaashoek and Hari Balakrishnan, Chord, a scalable peer-to-peer lookup service for Internet applications, SIGCOMM 2001
    locator: Section 4.2 (consistent hashing on an identifier circle, a key goes to its successor node, and a join moves O(K/N) keys)
  - paper: doi:10.1145/1294261.1294281
    title: Giuseppe DeCandia and others, Dynamo, Amazon's highly available key-value store, SOSP 2007
    locator: Section 4.2 (partitioning by consistent hashing with virtual nodes) and Section 6.2 (the partitioning strategies compared)
---

Consistent hashing assigns keys to servers so that a change in the set of servers moves only a few keys. Each server is hashed to one or more points on a circle, each key is hashed to a point on the same circle, and the key goes to the server that owns the first point clockwise from it. When a server joins, it takes only the keys that fall just before its points; when a server leaves, only its own keys move, to the next points. With $n$ servers the expected share that moves is $1/(n+1)$ of the keys, while the plain rule "server number $h(k) \bmod n$" moves $n/(n+1)$ of them. Karger, Lehman, Leighton, Panigrahy, Levine and Lewin introduced it in 1997 for web caches, and it is now the standard way to place keys in distributed caches, [distributed hash tables such as Chord](/chord/) and key value stores. The data structure behind it is the [hash ring](/hash-ring/), and its balance comes from [virtual nodes](/virtual-nodes/).

## In plain words

Draw a clock face. Put each server at a few places on the clock, chosen by a hash of its name. Put each key at one place on the clock, chosen by a hash of the key. Walk clockwise from the key and stop at the first server you meet: that server stores the key.

When a new server arrives, it takes a place on the clock. Only the keys between it and the server before it change hands, and they all go to the new server. Every other key stays where it was. When a server leaves, its keys go to the next server clockwise, and nothing else moves. With the usual rule "hash the key and take the remainder by the number of servers", nearly every key changes server when that number changes.

## The problem

A system has a changing set of servers, such as caches or storage nodes, and a large set of keys. Each key must go to one server, every client must find that server from the key alone, the servers should get about equal shares, and when a server joins or leaves, few keys should move, because each moved key is a cache miss or a copy over the network. This is the keyed and dynamic form of the [load balancing problem](/load-balancing-problem/). Karger et al. also allowed each client to know only part of the servers (a *view*) and asked that the views still agree on most keys.

## The algorithm

```pseudo id=main
CH-LOOKUP(pos, owner, key)       ▷ pos[0 .. N − 1] sorted point positions, owner[i] the server of pos[i]
L1  x ← h(key)
L2  i ← least index with pos[i] ≥ x, or N if there is none     ▷ binary search
L3  if i = N then i ← 0                                         ▷ wrap around the ring
L4  return owner[i]
CH-JOIN(pos, owner, s)           ▷ server s gets v points
L5  for r ← 0 to v − 1 do
L6      insert the position h(s, r) with owner s into pos and owner, in sorted order
CH-LEAVE(pos, owner, s)
L7  for r ← 0 to v − 1 do
L8      delete the position h(s, r) and its owner from pos and owner
```

Positions are 64-bit numbers, and the ring is $\{0, \ldots, 2^{64} - 1\}$ with wrap-around. The code hashes a key with BLAKE2b and a server point with the string `"server#r"`. The sorted arrays are the simplest [hash ring](/hash-ring/); a [balanced search tree](/balanced-binary-search-tree/) gives faster joins. Karger et al. described the same scheme on the unit interval with each item sent to the closest bucket point; the circle with the next point clockwise is the form that Chord and later systems use, and it has the same properties.

## Example

**A small ring.** Positions run from 0 to 99. Servers A, B and C have one point each, at 12, 47 and 80. Four keys hash to 5, 30, 50 and 90.

| key position | first point at or after it | owner |
| --- | --- | --- |
| 5 | 12 | A |
| 30 | 47 | B |
| 50 | 80 | C |
| 90 | none, wrap to 12 | A |

Server D joins with a point at 40. The key at 30 now meets 40 before 47 and moves from B to D. The keys at 5, 50 and 90 stay. If C leaves instead, the key at 50 goes on to the next point, 12, and moves to A; no other key moves.

**Moved keys with real hashes.** 100000 keys on 10 servers, then an 11th server joins (BLAKE2b positions as in the code):

| scheme | share of keys moved | expected |
| --- | --- | --- |
| $h(k) \bmod n$ | 0.908 | $10/11 = 0.909$ |
| ring, 1 point per server | 0.014 | $1/11 = 0.091$ in mean, with a wide spread |
| ring, 100 points per server | 0.088 | $1/11 = 0.091$ |

With one point per server the new server took only 1.4 percent of the keys, because its single point landed close behind another point. On the same ring the largest share of the 10 servers is 2.50 times the fair share $1/10$ and the smallest is 0.03 times. With 100 points per server the shares range from 0.88 to 1.11 times the fair share. This is why real systems use [virtual nodes](/virtual-nodes/).

## Correctness

Line L2 finds the point of least clockwise distance at or after $x$, and line L3 handles the keys past the last point, so CH-LOOKUP returns the owner of the first point clockwise from $h(key)$ (Lemma 1 of the proof). The key property is that a join only adds points: for each key, the first point clockwise in the larger set is either the old one or a new one, so a key either stays or moves to the new server ([monotonicity](/monotonicity-property/), Lemma 2). A leave moves only the keys of the server that leaves (Lemma 3). If the hash positions behave like independent uniform points, every server is the owner of a key with the same probability, so a join moves $1/(n+1)$ of the keys in expectation (Lemma 4). For $h(k) \bmod n$, a key keeps its server from $n$ to $n + 1$ servers only when $h(k) \bmod n(n+1) < n$, which has probability $1/(n+1)$ (Lemma 5).

## Complexity

- **Lookup.** One hash and one binary search over $N = nv$ points: $O(\log(nv))$ time in the [word RAM](/word-ram/).
- **Join or leave.** $v$ inserts or deletes. With a sorted array each costs $O(nv)$ for the shift, so $O(nv^2)$ in all; with a balanced tree it is $O(v\log(nv))$.
- **Space.** $O(nv)$ for the points.
- **Keys moved.** $1/(n+1)$ of the keys in expectation on a join, and exactly the keys of the server on a leave.
- **Balance.** Each server gets $1/n$ of the keys in expectation. With one point per server the largest share is $\Theta(\log n/n)$ with high probability, and with $v = \Theta(\log n)$ points it is at most $(1 + \epsilon)/n$ ([consistent hashing load bound](/consistent-hashing-max-load-bound/)).

## Properties

Karger et al. defined four properties for a hash function whose set of buckets changes and which each client sees only in part, and their construction has all four:

- **[Balance](/balance-property/).** In each view, each bucket gets $O(1/|V|)$ of the items with high probability.
- **[Monotonicity](/monotonicity-property/).** When buckets are added to a view, items move only to the new buckets.
- **[Spread and load](/spread-and-load/).** Over many views, an item is put in few different buckets (spread), and a bucket gets few different items (load), both $O(t\log C)$ when each view holds at least a $1/t$ fraction of the $C$ buckets.

The scheme is deterministic once the hash function is fixed, so every client computes the same answer from the same set of servers, with no table to share.

## Variants and improvements

- **Virtual nodes.** Give each server $v$ points, or a number of points in proportion to its capacity ([virtual nodes](/virtual-nodes/)). This is what makes the shares even, and Karger et al. already used $\kappa\log C$ points per bucket.
- **Rendezvous hashing.** Give the key to the server with the highest hash of the pair (key, server) ([rendezvous hashing](/rendezvous-hashing/)). It has the same monotonicity, needs no ring, and costs $O(n)$ per lookup.
- **Jump consistent hash.** Maps a key to one of $n$ numbered buckets in $O(\log n)$ time with no memory, but only lets buckets join or leave at the end ([jump consistent hash](/jump-consistent-hash/)).
- **Maglev hashing.** Fills a lookup table of fixed size from per-server preference lists, for $O(1)$ lookups and near equal shares, at the cost of a few extra moves ([Maglev hashing](/maglev-hashing/)).
- **Multi-probe consistent hashing.** One point per server, but each key looks up several positions and takes the closest point ([multi-probe consistent hashing](/multi-probe-consistent-hashing/)).
- **Bounded loads.** Cap each server at $(1 + \epsilon)$ times the average and send overflow keys further clockwise ([bounded-load consistent hashing](/bounded-load-consistent-hashing/)).
- **CARP.** The Cache Array Routing Protocol uses a highest-hash rule for web proxies ([CARP](/carp/)).

## When to use it

Use consistent hashing when keys must stick to servers and the set of servers changes: distributed caches, where a moved key is a miss; storage and [sharding](/sharding/) by key, where a moved key is a copy; and peer-to-peer lookup, as in [Chord](/chord/). Use more than a few points per server, or one of the variants above. If the set of servers never changes, a plain hash mod $n$ is simpler and balanced. If keys need not stick, a dynamic rule such as [the power of two choices](/power-of-two-choices/) balances better. If the servers are numbered and only grow or shrink at the end, [jump consistent hash](/jump-consistent-hash/) is smaller and faster.

## Pitfalls

- **One point per server.** The largest arc is about $\ln n$ times the average, so one server can get several times its share, and a joining server may take almost nothing. Use virtual nodes.
- **Different hash functions on different clients.** Every client must compute the same positions: the same hash function, the same encoding of server names, and the same point labels. A change of any of them moves all keys.
- **Server names that change.** If a server's point depends on its address and the address changes, its keys move. Hash a stable name.
- **Hot keys.** The scheme balances the number of keys, not the traffic. One very popular key overloads its server whatever the ring looks like ([load skew](/load-skew/)); use replication or bounded loads.
- **Collisions of points.** Two points at the same position make the owner depend on the order of inserts. Use 64-bit positions, or break ties by server name.
- **Cascading failure.** When a server leaves, all of its keys go to the next point. With one point per server that single neighbor gets the whole extra load, which can overload it too. Virtual nodes spread the keys of a failed server over many servers.

## Implementations

The Python file keeps the points in two sorted lists and uses `bisect` for the binary search. It also has the mod-$n$ scheme and a function that measures the share of keys that move. The tests compare the lookup with a linear scan of the ring, check that a join moves keys only to the new server, that a leave moves only the keys of the server that leaves, and that the share that moves is near $1/(n+1)$ for the ring and near $n/(n+1)$ for mod $n$.

## History

Karger, Lehman, Leighton, Panigrahy, Levine and Lewin presented consistent hashing and random trees at STOC 1997, as a way to spread web pages over a changing set of caches without hot spots. Their construction maps buckets and items to the unit interval and gives each bucket $\kappa\log C$ points. Leighton and Lewin founded Akamai in 1998 on these ideas. Chord (Stoica, Morris, Karger, Kaashoek and Balakrishnan, 2001) used consistent hashing on an identifier circle with the successor rule, and Dynamo (DeCandia et al., 2007) used it with virtual nodes for a key value store, followed by Cassandra and Riak. The ketama library from Last.fm (2007) made the ring with many points per server the common form for memcached clients.

## References
