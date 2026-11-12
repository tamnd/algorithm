---
tag: XY2H5A
kind: problem
slug: dynamic-partitioning-problem
name: Dynamic partitioning problem
aliases:
- key-to-server mapping under churn
- distributed key assignment
area: systems/load-balancing-and-hashing
level: core
summary: Map keys to a set of servers that changes over time, so that every client computes the same server, loads stay close to even, and each change of the server set moves few keys.
prereqs: [load-balancing-problem, hash-function]
see_also: [consistent-hashing, monotonicity-property, balance-property, spread-and-load, hash-partitioning, sharding, virtual-nodes, balls-into-bins-max-load]
sources:
  - paper: doi:10.1145/258533.258660
    title: David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine and Daniel Lewin, Consistent hashing and random trees, distributed caching protocols for relieving hot spots on the World Wide Web, STOC 1997
    locator: pages 654 to 663, the section on consistent hashing (ranged hash functions, views, and the balance, monotonicity, spread and load properties)
  - paper: doi:10.1109/90.663936
    title: David G. Thaler and Chinya V. Ravishankar, Using name-based mappings to increase hit rates, IEEE/ACM Transactions on Networking 6(1), 1998, pages 1 to 14
    locator: the highest random weight (HRW) mapping and its minimal disruption when a server fails (section level not checked)
  - url: https://arxiv.org/abs/1406.2294
    title: John Lamping and Eric Veach, A fast, minimal memory, consistent hash algorithm, arXiv:1406.2294, 2014
    locator: the requirements of balance and monotonicity, and the restriction of jump consistent hash to buckets numbered 0 to n - 1
  - paper: doi:10.1137/1.9781611975031.39
    title: Vahab Mirrokni, Mikkel Thorup and Morteza Zadimoghaddam, Consistent hashing with bounded loads, SODA 2018, pages 587 to 604
    locator: the introduction (the capacity of (1 + eps) times the mean load, and the expected moves per update)
---

The dynamic partitioning problem asks for a rule that maps each key to one server of a set that changes over time. Every client that knows the set must compute the same server without asking anyone, every server must receive about its share of the keys, and when a server joins or leaves, only a small part of the keys may change servers, ideally only the keys that must. It is the keyed and changing form of the [load balancing problem](/load-balancing-problem/), and the problem that [consistent hashing](/consistent-hashing/) was made to solve. The plain rule $h(k) \bmod n$ solves the first two goals and fails the third: a change of $n$ moves almost every key.

## In plain words

Many machines share a large set of items, such as the entries of a cache or the rows of a database. Anyone who wants an item must know which machine has it, and must find out alone, by a fixed rule. The rule must give each machine about the same number of items.

Machines come and go. When one is added, it must take over some items from the others, and when one leaves, its items must go somewhere. Each moved item costs something: a copy over the network, or a miss in a cache. So the rule must change as little as it can: when a machine joins, only the items it takes should move, and when a machine leaves, only its own items should move.

## Definition

**Input.** A universe $U$ of keys and a universe of server names. At each time $t$ there is a set $S_t$ of $n_t$ servers (the view), possibly with weights $w_s > 0$, and a set $K_t \subseteq U$ of $m_t$ keys in use. Between steps, one server joins or leaves, or keys are added or removed.

**Output.** An assignment $f_t : K_t \to S_t$ for each $t$. In the basic form $f_t(k) = f(k, S_t)$ is a function of the key and the view only, so all clients with the same view agree with no communication.

**Measures.**

- **Balance.** The peak-to-mean ratio $\max_{s} |f_t^{-1}(s)| \,/\, (m_t / n_t)$, or the share of server $s$ against $w_s / \sum_r w_r$ in the weighted form. Bounds on the key counts hold with high probability over a random hash; only a rule with a capacity cap has a worst-case bound.
- **Movement.** The number of keys $k$ with $f_t(k) \ne f_{t+1}(k)$ for one change of the view. A rule is *monotone* if adding a server moves keys only to the new server, and removing a server moves only the keys that it held; see the [monotonicity property](/monotonicity-property/).
- **Cost.** The lookup time and the memory per client.

The arrival model is that of [balls into bins](/balls-into-bins-max-load/) with a random hash: the keys are fixed in advance by an adversary that does not see the hash, and the view changes by any sequence of joins and leaves.

## Variants

- **Inconsistent views.** Clients may know different subsets of the servers. Karger et al. then ask for low *spread*, the number of servers one key is sent to over all views, and low *load*, the number of keys one server gets over all views; see [spread and load](/spread-and-load/).
- **Weighted servers.** Server $s$ should get the share $w_s / W$.
- **Replication.** Map each key to an ordered list of $r$ distinct servers, so that the loss of a server moves only one entry of each list.
- **Hard capacity.** No server may hold more than $\lceil (1 + \varepsilon) m / n \rceil$ keys, also under adversarial or hot keys. Then the assignment depends on the set of keys, not only on the key.
- **Numbered buckets.** The servers are $0, \ldots, n - 1$ and change only at the end, as with shards that are renumbered by the application.
- **Ordered keys.** Keys that are close in order should stay together, so that range queries touch few servers; see [range partitioning](/range-partitioning/).
- **Decentralized lookup.** No client knows the whole view. A distributed hash table such as [Chord](/chord/) finds the server of a key in $O(\log n)$ hops.

## Examples

Take $m = 100{,}000$ keys, 10 servers, 64-bit BLAKE2b hashes, and count the moves when an 11th server is added and when one server is removed. Adding a server must move at least $100{,}000/11 \approx 9{,}091$ keys if all 11 servers end up equal. Removing a server must move the keys it held.

| rule | peak-to-mean with 10 servers | keys moved on adding one | keys moved on removing one |
|---|---|---|---|
| $h(k) \bmod n$ | 1.014 | 90,840 | 89,881 (it held 9,884) |
| ring, 1 point per server | 2.494 | 1,357 | 16,315 (it held 16,315) |
| ring, 100 points per server | 1.092 | 8,772 | 10,625 (it held 10,625) |
| rendezvous hashing | 1.019 | 9,061 | 9,990 (it held 9,990) |
| jump consistent hash | 1.018 | 8,989 | 9,933 (the last server) |

The modulo rule balances well and moves about $10/11$ of the keys on any change. The ring with one point per server is monotone but unbalanced, so the new server takes only 1,357 keys and one old server holds 2.5 times the mean. With 100 points per server the ring is close to the ideal. Rendezvous hashing and jump hash meet the lower bound up to random noise; jump hash can only remove the last server.

## Known algorithms

| algorithm | lookup time | client state | balance | movement | notes |
|---|---|---|---|---|---|
| [hash mod n](/hash-partitioning/) | $O(1)$ | $O(1)$ | binomial | about $n/(n+1)$ of the keys | not monotone |
| fixed partitions and a map | $O(1)$ | $O(P)$ | within one partition | whole partitions, near minimal | the map must be kept and shared |
| [consistent hashing](/consistent-hashing/), 1 point | $O(\log n)$ | $O(n)$ | largest share $\Theta(\log n / n)$ | monotone | |
| ring with [virtual nodes](/virtual-nodes/) | $O(\log (n v))$ | $O(n v)$ | constant factor for $v = \Omega(\log n)$ | monotone | weights by point counts |
| [rendezvous hashing](/rendezvous-hashing/) | $\Theta(n)$ | $O(n)$ | as balls into bins | monotone, minimal | weights and top $r$ |
| [CARP](/carp/) | $\Theta(n)$ | $O(n)$ | weighted shares | minimal on removal | HRW with load factors |
| [jump consistent hash](/jump-consistent-hash/) | $O(\log n)$ expected | $O(1)$ | as balls into bins | monotone, minimal | numbered buckets only |
| [multi-probe consistent hashing](/multi-probe-consistent-hashing/) | $O(k \log n)$ | $O(n)$ | peak about 1.05 of the mean for $k = 21$ | monotone | $k$ probes per key |
| [Maglev hashing](/maglev-hashing/) | $O(1)$ | $O(M)$ table | each server gets $\lfloor M/n \rfloor$ or $\lceil M/n \rceil$ slots | a few extra slots | not exactly monotone |
| [bounded-load consistent hashing](/bounded-load-consistent-hashing/) | walk on a ring | $O(n + m)$ | hard cap $1 + \varepsilon$ | $O(1/\varepsilon^2)$ times the minimum, in expectation | depends on the key set |

## Bounds

- **Movement lower bound for joins.** If all $n + 1$ servers must be exactly balanced after a join, the new server holds $\lfloor m/(n+1) \rfloor$ or more keys, and each of them moved. So at least about $m/(n+1)$ keys move. The same count shows that a monotone rule with exact balance is optimal.
- **Movement lower bound for leaves.** All keys of the server that leaves must move, about $m/n$ of them under balance.
- **Modulo rule.** For a hash uniform over a multiple of $n(n+1)$, a key keeps its server from $n$ to $n + 1$ servers with probability $1/(n+1)$, by the Chinese remainder theorem; so the fraction $n/(n+1)$ moves.
- **Ring balance.** With one random point per server, the largest arc is $\Theta(\log n / n)$ with high probability; with $\Theta(\log n)$ points per server, every share is within a constant factor of $1/n$ ([max-load bound](/consistent-hashing-max-load-bound/)).
- **Balls into bins.** Any rule that sends each key to a uniform random server, independently, has the balance of $m$ balls in $n$ bins: the largest load is $m/n + O(\sqrt{(m/n) \log n})$ with high probability for $m \ge n \log n$. A rule in which each key's server depends only on the key and the view keeps this random noise, whatever the shares are; only a rule that also looks at the set of keys, such as bounded loads, can remove it.

## Reductions

- **Weighted to unweighted.** A server of integer weight $w$ becomes $w$ virtual servers. Rendezvous hashing avoids the copies with a weighted score, and CARP with load factor multipliers.
- **Keys to partitions.** Hash keys into $P$ fixed partitions, and solve the problem for the $P$ partitions with a small map; then the map is the only state, and moves are of whole partitions. This is [hash partitioning](/hash-partitioning/) with a partition map, and [sharding](/sharding/) in most databases.
- **Replication.** A rule for one server gives a rule for $r$ servers: the top $r$ scores in rendezvous hashing, or the next $r$ distinct servers clockwise on a ring.
- **Static case.** For a fixed view, the problem is the keyed form of the [load balancing problem](/load-balancing-problem/), and its balance with a random hash is a [balls into bins](/balls-into-bins-max-load/) question.

## Applications

- Distributed caches, where a moved key is a cache miss: web proxy arrays (CARP), memcached clients (ring with virtual nodes), content delivery networks.
- Key-value and wide-column stores such as Dynamo and Cassandra, where a moved key is a copy over the network.
- Load balancers and routers that must keep a flow on one backend or next hop when the set changes: [Maglev hashing](/maglev-hashing/), [ECMP hashing](/ecmp-hashing/) with HRW.
- Peer-to-peer systems and distributed hash tables, where no node knows the whole view.
- Services with many clients and a hard per-server limit, for which Mirrokni, Thorup and Zadimoghaddam report the use of bounded loads.

## References
