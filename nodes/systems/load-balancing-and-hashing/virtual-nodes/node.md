---
tag: CK7ZZ4
kind: technique
slug: virtual-nodes
name: Virtual nodes
aliases:
- virtual servers
- vnodes
area: systems/load-balancing-and-hashing
level: core
summary: "Give each server v points on the hash ring instead of one. Its share becomes a sum of v arcs, so the shares even out (spread about 1/sqrt(v)), and weights become point counts."
prereqs: [hash-ring]
see_also: [consistent-hashing, consistent-hashing-max-load-bound, hash-ring, multi-probe-consistent-hashing, bounded-load-consistent-hashing, maglev-hashing, rendezvous-hashing, chord]
sources:
  - paper: doi:10.1145/258533.258660
    title: David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine and Daniel Lewin, Consistent hashing and random trees, STOC 1997
    locator: Section 4.2 (each bucket is mapped to kappa log C points of the unit interval) and Theorem 4.1 (balance)
  - paper: doi:10.1145/383059.383071
    title: Ion Stoica, Robert Morris, David Karger, M. Frans Kaashoek and Hari Balakrishnan, Chord, a scalable peer-to-peer lookup service for Internet applications, SIGCOMM 2001
    locator: the load balance experiments, where each real node runs r virtual nodes and r = O(log N) evens out the keys per node
  - paper: doi:10.1145/1294261.1294281
    title: Giuseppe DeCandia and others, Dynamo, Amazon's highly available key-value store, SOSP 2007
    locator: Section 4.2 (virtual nodes, and their use for heterogeneous capacity and for spreading the load of a failed node) and Section 6.2 (three partitioning strategies compared)
---

Virtual nodes is the technique of giving each server many points on a [hash ring](/hash-ring/) instead of one. Each point is a *virtual node*: it owns the arc before it, like a server would, and all the virtual nodes of a server send their keys to that server. With one point per server the arcs are very uneven: the largest is about $\ln n$ times the average and the smallest is close to zero. With $v$ points per server, a server's share is the sum of $v$ random arcs, so its relative spread falls like $1/\sqrt v$, and with $v = \Theta(\log n)$ every server gets $(1 \pm \epsilon)/n$ of the ring with high probability ([consistent hashing load bound](/consistent-hashing-max-load-bound/)). Virtual nodes also give servers of different size different shares, by giving them different numbers of points, and they spread the keys of a failed server over many servers instead of one. Karger et al. used $\kappa\log C$ points per bucket in the first paper on [consistent hashing](/consistent-hashing/), and Chord, Dynamo and Cassandra use the technique under this name.

## In plain words

If each server throws one dart at a wheel, some darts land close together and some far apart, so some servers get huge slices and others tiny ones. If each server throws a hundred darts and gets all the slices that its darts end, the luck evens out: every server gets many slices of all sizes, and the totals are close to equal.

A bigger server can throw more darts and get a bigger share. And when a server leaves, its many slices go to many different neighbors, so no single neighbor gets all of the extra work.

## When it applies

- A set of servers or buckets is placed on a ring, or on any line or space, by hashing, and each owns the region nearest to its point. The shares of single points are uneven, because the gaps between random points are uneven.
- The share of a server can be the sum of several regions, and the cost of a server is the sum of the costs of its regions.
- The number of points is small enough to store and search: $nv$ points in all, with $O(\log(nv))$ time per lookup.

## The template

1. **Choose $v$.** Pick the number of points per server: about $c\log n$ for a guarantee with high probability, or a fixed number such as 100 to 256 in practice. The relative spread of the shares is about $1/\sqrt v$.
2. **Name the points.** Give point $r$ of server $s$ the position $h(s, r)$, for $r = 0, \ldots, v - 1$, with a fixed encoding such as the string `"s#r"`. Every client must use the same names and the same hash.
3. **Insert all points.** Put the $nv$ points in the ring, each with its server as owner.
4. **Look up as usual.** A key goes to the owner of the first point clockwise from $h(key)$. Nothing else changes.
5. **Weights.** A server of capacity $c_s$ gets $v_s \propto c_s$ points, so its expected share is $v_s/\sum_t v_t$.
6. **Join and leave.** Insert or remove all $v_s$ points of the server. Each point takes or gives back one arc, so the keys that move come from, or go to, up to $v_s$ different servers.

## Classic examples

**The balance of the shares.** Points placed uniformly at random (Python `random.Random(21)`), averaged over 20 rings (5 rings for $n = 100$, $v = 1000$). A share of 1 is the fair share $1/n$.

| servers $n$ | points per server $v$ | largest share | smallest share | standard deviation | $1/\sqrt v$ |
| --- | --- | --- | --- | --- | --- |
| 10 | 1 | 3.04 | 0.11 | 0.90 | 1 |
| 10 | 10 | 1.50 | 0.53 | 0.29 | 0.32 |
| 10 | 100 | 1.15 | 0.85 | 0.09 | 0.10 |
| 10 | 1000 | 1.05 | 0.95 | 0.03 | 0.03 |
| 100 | 1 | 5.61 | 0.01 | 1.01 | 1 |
| 100 | 10 | 2.02 | 0.38 | 0.32 | 0.32 |
| 100 | 100 | 1.27 | 0.76 | 0.10 | 0.10 |
| 100 | 1000 | 1.09 | 0.91 | 0.03 | 0.03 |

With one point per server the largest share is close to $H_n$ times the fair share ($H_{10} = 2.93$, $H_{100} = 5.19$), as the [load bound](/consistent-hashing-max-load-bound/) predicts. The share of one server is a sum of $v$ of the $nv$ gaps, with relative standard deviation $\sqrt{(n-1)/(nv+1)} \approx 1/\sqrt v$, which the table matches.

**A failed server.** On 10 servers, when one server leaves, its keys go to the servers of the next points clockwise. Over 50 rings (seed 22), the keys of the failed server went to 1 server with $v = 1$, to 5.9 servers on average with $v = 10$, and to all 9 remaining servers with $v = 100$. With one point, the single successor gets twice its load at once.

**Weighted servers.** Two servers of capacity 1 and one of capacity 2 get 100, 100 and 200 points. Their expected shares are $1/4$, $1/4$ and $1/2$.

**Systems.** Karger et al. map each cache to $\kappa\log C$ points. Chord runs $O(\log N)$ virtual nodes per real node to even out the keys. Dynamo calls them virtual nodes or tokens, uses them for capacity and for spreading the load of a failed node, and later moved to a fixed number of equal partitions assigned to nodes. Cassandra assigned 256 tokens per node by default for many years. The ketama library for memcached hashes each server name with an index to many points.

## Variations

- **Fixed partitions.** Cut the ring into $Q$ equal arcs, with $Q$ much larger than $n$, and assign whole arcs to servers by a table. The shares are exactly controlled and moving data is per partition, at the cost of a table that all clients must share. Dynamo's third strategy is of this kind.
- **Multi-probe.** Keep one point per server and hash each key $k$ times, taking the closest point. The balance improves with $k$ in the same way, without the memory of $nv$ points ([multi-probe consistent hashing](/multi-probe-consistent-hashing/)).
- **Bounded loads.** Cap each server at $(1 + \epsilon)$ times the average and pass the extra keys on clockwise ([bounded-load consistent hashing](/bounded-load-consistent-hashing/)). This bounds the load of keys, not only the share of the ring.
- **Rendezvous and Maglev.** [Rendezvous hashing](/rendezvous-hashing/) gives each key the server with the highest hash of the pair and is balanced without extra points. [Maglev hashing](/maglev-hashing/) fills a fixed table and gets near equal shares by construction.
- **Moving virtual servers.** In peer-to-peer systems a heavy node can hand one of its virtual servers to a light node, which balances the real load, not only the expected share.

## Pitfalls

- **Too few points.** With $v = 10$ the largest share is still about 1.5 to 2 times fair. The spread falls only like $1/\sqrt v$, so going from 1.15 to 1.05 needs ten times more points.
- **Too many points.** Each point costs memory in every client, and a join inserts $v$ points. Rings of $10^6$ points or more make joins and the publication of the ring slow.
- **Correlated point names.** If $h(s, r)$ is weak, the points of one server can cluster, and the shares stay uneven. Use a good [hash function](/hash-function/) on a clear encoding of $(s, r)$.
- **Replicas on the same server.** When a key is stored on the next $r$ points clockwise, two of those points can belong to the same server. Skip points of servers already chosen.
- **Balance of the ring is not balance of the load.** Virtual nodes even out the number of keys, not the traffic. A hot key still lands on one server ([load skew](/load-skew/)).
- **Changing $v$ later.** A change of $v$ or of the naming scheme moves most keys, like a new hash function. Choose it once.

## Exercises

1. Two servers have one point each on a circle of length 1. Show that the smaller share is uniform on $[0, 1/2]$, so its mean is $1/4$.
2. With $n$ servers and $v$ uniform points each, the share of a server is a sum of $v$ of the $nv$ arcs. Show that its mean is $1/n$ and its variance is $(n-1)/(n^2(nv+1))$, using that the share has the Beta$(v, (n-1)v)$ law.
3. A server leaves a ring of $n$ servers with $v$ points each. Its points form maximal runs of consecutive points, and each run hands its keys to the owner of the next point, which is uniform among the other servers. Show that the expected number of runs is about $v(n-1)/n$, and conclude that about $(n-1)\bigl(1 - (1 - \frac{1}{n-1})^{v(n-1)/n}\bigr)$ servers receive keys. Compare with the 5.9 servers of the example for $n = v = 10$.
4. Servers of capacity $c_1, \ldots, c_n$ get $v_i = \lceil c_i\,k \rceil$ points. Bound the error of the expected shares against $c_i/\sum_j c_j$ in terms of $k$.
5. Give a sequence of joins in which every server has the same number of points but one server's share is much larger than $1/n$ for a bad but valid hash function, and explain why the analysis needs random positions.

## References
