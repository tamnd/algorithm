---
tag: 135CB9
kind: algorithm
slug: rendezvous-hashing
name: Rendezvous hashing
aliases:
- highest random weight hashing
- HRW hashing
- HRW mapping
area: systems/load-balancing-and-hashing
level: core
summary: Give each key to the server with the highest hash score h(key, server). Removing a server moves only its keys, and a weighted score gives shares in proportion to weights.
solves: [dynamic-partitioning-problem]
model: word-ram
complexity:
  vars: {n: the number of servers, r: the number of replicas}
  time: {worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1996
  people: [David G. Thaler, Chinya V. Ravishankar]
  note: Thaler and Ravishankar described the highest random weight mapping in a 1996 technical report at the University of Michigan and in IEEE/ACM Transactions on Networking in 1998.
prereqs: [hash-function, dynamic-partitioning-problem]
see_also: [consistent-hashing, monotonicity-property, carp, ecmp-hashing, jump-consistent-hash, maglev-hashing, weighted-reservoir-sampling, gumbel-max-trick]
sources:
  - paper: doi:10.1109/90.663936
    title: David G. Thaler and Chinya V. Ravishankar, Using name-based mappings to increase hit rates, IEEE/ACM Transactions on Networking 6(1), 1998, pages 1 to 14
    locator: the definition of the highest random weight (HRW) mapping, its load balance and its minimal disruption when a server fails (section level not checked)
  - paper: doi:10.1145/1073970.1074008
    title: Christian Schindelhauer and Gunnar Schomaker, Weighted distributed hash tables, Proceedings of the 17th ACM Symposium on Parallelism in Algorithms and Architectures (SPAA), 2005, pages 218 to 227
    locator: the logarithmic method, a score of the form -w / ln(u) that gives each server a share in proportion to its weight
  - url: https://www.rfc-editor.org/rfc/rfc2991
    title: D. Thaler and C. Hopps, Multipath issues in unicast and multicast next-hop selection, RFC 2991, 2000
    locator: Section 4 (HRW as a next-hop selection method, with a disruption of about 1/N of the flows)
  - url: https://www.rfc-editor.org/rfc/rfc2992
    title: C. Hopps, Analysis of an equal-cost multi-path algorithm, RFC 2992, 2000
    locator: Section 3 (comparison of modulo-N, hash-threshold and HRW; HRW disruption is always 1/N)
---

Rendezvous hashing, or highest random weight (HRW) hashing, sends each key to the server with the highest score $h(\text{key}, \text{server})$, where $h$ is a [hash function](/hash-function/) of the pair. It solves the [dynamic partitioning problem](/dynamic-partitioning-problem/) with no shared state: each client that knows the server set computes the same answer. When a server leaves, only its own keys move, and when a server joins, it takes about $1/(n+1)$ of the keys from the others. A lookup costs $\Theta(n)$ hash evaluations for $n$ servers.

## In plain words

Each key holds a lottery among the servers. The ticket of a server is a hash of the key name and the server name together, so the tickets look random but every client draws the same tickets. The server with the highest ticket wins the key.

If a server goes away, the keys that it did not win keep their winners, because the winning tickets did not change. Only the keys of the lost server go to their second best server. If a new server comes, it wins a key only when its ticket beats the old winner, and that happens for about one key in the new number of servers. No server list must be sorted, and no ring is necessary. The price is that each lookup computes one ticket for each server.

## The problem

There is a set $S$ of $n$ servers with stable names and a stream of keys (object names, user IDs, flow identifiers). Each client must map each key to one server so that:

- all clients that know the same $S$ give the same answer, with no communication;
- each server gets about $1/n$ of the keys (or a share in proportion to a weight);
- when $S$ changes by one server, few keys move.

The guarantees below are in the random oracle model: the scores of different pairs behave as independent uniform random numbers. The arrival model is a fixed set of $m$ keys, as in balls into bins.

## The algorithm

```pseudo id=main
HRW(key, S)                                ▷ S is a nonempty set of server names
L1  best ← none, bestScore ← −∞
L2  for each server s in S do
L3      v ← h(key, s)
L4      if v > bestScore then              ▷ ties go to the larger name
L5          best ← s, bestScore ← v
L6  return best
```

**Replicas.** To place $r$ copies, take the $r$ servers with the highest scores. The first one is the HRW server. When one of them fails, the next server in the order takes its place, and the other copies stay.

**Weights.** Give server $s$ a weight $w_s > 0$. Map the hash to a number $u = u(\text{key}, s)$ strictly between 0 and 1, and use the score

$$\text{score}(\text{key}, s) = \frac{-w_s}{\ln u}.$$

Then server $s$ gets the share $w_s / \sum_t w_t$ of the keys. This is the logarithmic method of Schindelhauer and Schomaker.

## Example

Three servers A, B and C, and six keys. The table gives $u = h(\text{key}, s)$ scaled to $(0, 1)$, from the 64-bit BLAKE2b score of the implementation below.

| key | A | B | C | owner | owner without B | D | owner with D added |
|---|---|---|---|---|---|---|---|
| apple | 0.838 | **0.886** | 0.583 | B | A | 0.003 | B |
| banana | **0.590** | 0.187 | 0.574 | A | A | 0.775 | D |
| cherry | **0.632** | 0.136 | 0.058 | A | A | 0.871 | D |
| date | 0.602 | **0.697** | 0.364 | B | A | 0.763 | D |
| elder | 0.113 | **0.817** | 0.208 | B | C | 0.302 | B |
| fig | 0.409 | **0.791** | 0.285 | B | A | 0.444 | B |

When B leaves, banana and cherry stay on A. Each key of B goes to its second highest score: apple, date and fig to A, elder to C. When a fourth server D joins, it wins exactly the keys where its score beats the old winner: banana, cherry and date. No key moves between A, B and C. With six keys the loads are uneven (B has four); the balance is a statement about many keys.

**A larger run.** Hash the keys key0 to key99999 onto ten servers s0 to s9. The loads lie between 9,930 and 10,078, against a mean of 10,000. Removing s9 moves exactly its 9,941 keys. Adding s10 moves 9,072 keys, all to s10; the expected number is $100{,}000 / 11 \approx 9{,}091$. With the weighted score and weights 1, 2, 3 and 4 on four servers, the loads are 10,008, 19,833, 30,021 and 40,138, against 10,000, 20,000, 30,000 and 40,000. Removing the server of weight 4 moves exactly its 40,138 keys, and the other three then have 16,668, 33,140 and 50,192.

## Correctness

The procedure returns the argmax of the scores, which depends only on the key and the set $S$, so all clients agree. If a server $r$ is removed, the winner $s^* \ne r$ of a key is still the largest score in the smaller set, so it keeps the key. Adding a server $t$ is the same statement read backwards: the winner over $S \cup \{t\}$ is $t$ or the old winner. This is the [monotonicity property](/monotonicity-property/). In the random oracle model each server wins a key with probability $1/n$, so it has the [balance property](/balance-property/), and an added server takes each key with probability $1/(n+1)$, the smallest expected share that keeps the expected loads equal.

For the weighted score, $E = -\ln u$ is exponential with rate 1, so the score $w_s / E$ is largest when $E / w_s$ is smallest. The variable $E / w_s$ is exponential with rate $w_s$, and the smallest of independent exponentials has index $s$ with probability $w_s / \sum_t w_t$. The full proofs are below.

## Complexity

- **Lookup.** $\Theta(n)$ score evaluations and comparisons in each case. This is the main cost of the method. A ring with [virtual nodes](/virtual-nodes/) answers in $O(\log n)$ time with a binary search.
- **Replicas.** The top $r$ servers take $\Theta(n)$ score evaluations and $O(n \log r)$ comparisons with a heap of size $r$.
- **Space.** Only the list of server names, $\Theta(n)$, and $\Theta(1)$ extra space for a lookup. There is no table and no ring to rebuild.
- **Change of the server set.** No work at all: the next lookup sees the new list.
- **Load.** The load of one server is binomial with $m$ trials and success probability $1/n$. Its expected value is $m/n$ and its standard deviation is $\sqrt{m (1/n)(1 - 1/n)}$. The maximum over the servers follows the [balls into bins](/balls-into-bins-max-load/) bounds; for $m \ge n \ln n$ it is $m/n + O(\sqrt{(m/n) \ln n})$ with high probability. A plain [consistent hashing](/consistent-hashing/) ring with one point per server has a maximum share of order $(\ln n)/n$ (see the [max load bound](/consistent-hashing-max-load-bound/)), so HRW needs no virtual nodes for balance.

## Properties

- **Deterministic and stateless.** The answer is a function of the key and the server set.
- **Monotone.** A key moves only to an added server, or away from a removed one. This holds for each key, not only on average.
- **Balanced** in expectation, in the random oracle model, with the binomial spread of balls into bins.
- **Exact weights.** The logarithmic score gives each server the share $w_s / W$, and a weight change on one server moves keys only to it or only from it.
- **Low spread.** Clients that see different server sets still agree on a key whenever the winner over the union of their sets is in both sets.

## Variants and improvements

- **Skeleton or hierarchical HRW.** Put the servers at the leaves of a tree with fan-out $f$. At each inner node, pick the child with the highest score, and go down. A lookup costs $O(f \log_f n)$ instead of $\Theta(n)$. The keys of a removed server stay in its subtree, but the tree must be kept balanced by hand, and the shares are equal only when the subtrees are equal.
- **Cache Array Routing Protocol.** [CARP](/carp/) is HRW for proxy cache arrays, with load factor multipliers on the scores.
- **Next-hop selection.** RFC 2991 and RFC 2992 list HRW as one method for [ECMP hashing](/ecmp-hashing/), with a disruption of $1/N$ of the flows.
- **Weighted sampling without replacement.** The weighted score is an increasing function of $u^{1/w}$, the key of [weighted reservoir sampling](/weighted-reservoir-sampling/), and its logarithm is $\ln w$ plus a Gumbel variable, as in the [Gumbel-max trick](/gumbel-max-trick/). So the top $r$ servers of weighted HRW are a weighted sample of $r$ servers without replacement.
- **Not MinHash.** [MinHash](/minhash/) also takes an extreme of hash values, but over the elements of a set with one hash function, to estimate the Jaccard similarity of sets. HRW takes the maximum over servers for one key, to place the key.

## When to use it

Use HRW when the number of servers is small to moderate (tens to a few hundred), when the server set changes often, and when you want exact monotonicity, good balance and weights without a table to rebuild. Typical uses are client-side selection of a cache or a shard, replica placement (top $r$), and next-hop choice with per-flow state. For thousands of servers and a lookup on every packet, the $\Theta(n)$ cost is too high; use a table such as [Maglev hashing](/maglev-hashing/), a ring, or [jump consistent hash](/jump-consistent-hash/) when the servers are numbered.

## Pitfalls

- **A weak combination of hashes.** The score must be a good hash of the pair. With $h(k) + h(s)$ (without wraparound), the server with the largest $h(s)$ wins every key. With $h(k) \oplus h(s)$, the winner depends on the first bit where the server hashes differ, and the shares are unequal.
- **Weights as a plain factor.** The score $w_s \cdot u$ does not give shares in proportion to $w_s$. With weights 1 and 2, the first server wins when $u_1 > 2 u_2$, which has probability $1/4$, not $1/3$. Use $-w_s / \ln u$, or the multipliers of CARP.
- **A score of 0 or 1.** $\ln u$ must be finite and nonzero. Map the hash to the open interval, for example $u = (\lfloor x / 2^{12} \rfloor + 1/2) / 2^{52}$ for a 64-bit $x$, so that the value fits a double exactly.
- **Unstable names.** The scores use the server name. If a server comes back with a new address used as its name, all its keys are new random draws. Use a stable identifier.
- **The lookup cost in the fast path.** $\Theta(n)$ hashes per request is fine for 10 servers and slow for 1,000. Cache the result per key, or use the skeleton variant.

## Implementations

## History

David Thaler and Chinya Ravishankar described the highest random weight mapping in a 1996 technical report at the University of Michigan, and published it in IEEE/ACM Transactions on Networking in 1998. Their goal was to raise the hit rate of a group of web proxy caches: if all clients send the same URL to the same cache, each object is stored once. The method appeared in the same years as the ring of Karger et al. (1997). CARP, an Internet draft of 1998 for proxy arrays, uses the same highest score rule. Thaler later wrote it into RFC 2991 as a next-hop selection method. Schindelhauer and Schomaker gave the logarithmic method for weights in 2005.

## References
