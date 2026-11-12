---
tag: BY0B33
kind: problem
slug: load-balancing-problem
name: Load balancing problem
aliases:
- job assignment to servers
- request dispatching problem
area: systems/load-balancing-and-hashing
level: intro
summary: "Assign arriving jobs or requests to servers so that the maximum load stays small. Forms differ in what is known in advance, what state the dispatcher keeps, and whether a key must stick to a server."
prereqs: [makespan, balls-into-bins]
see_also: [makespan-minimization, online-makespan-minimization, online-restricted-assignment-load-balancing, least-connections, round-robin-load-balancing, peak-ewma, power-of-two-choices, consistent-hashing]
sources:
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 5 (balls into bins, the model of random assignment) and Chapter 17 (balanced allocations)
  - paper: "Yossi Azar, On-line load balancing, in Online Algorithms, The State of the Art, LNCS 1442, Springer, 1998"
    locator: pp. 178 to 195, the online models (identical, related, restricted and unrelated machines; permanent and temporary jobs) and their competitive ratios
  - paper: doi:10.1145/258533.258660
    title: David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine and Daniel Lewin, Consistent hashing and random trees, STOC 1997
    locator: pp. 654 to 663, the assignment of items to caches when the set of caches changes and each client sees only part of it
---

The load balancing problem asks how to assign a stream of jobs or requests to a set of servers so that no server is much busier than the others. The load of a server is the total size of the jobs it holds, and the usual goal is to keep the maximum load close to the average. The problem has many forms: the jobs may be known in advance or arrive one by one, the dispatcher may keep state and read the loads or know nothing, jobs may stay forever or finish, and a job with a key may have to go to the same server every time. Each form has its own algorithms, from [round robin](/round-robin-load-balancing/) and [least connections](/least-connections/) to [the power of two choices](/power-of-two-choices/) and [consistent hashing](/consistent-hashing/). The offline form with known sizes is [makespan minimization](/makespan-minimization/).

## In plain words

Work arrives and several workers can do it. You must decide who does each piece, so that nobody is buried while others are idle. If you know all the work in advance, you can plan. Usually you do not: pieces arrive one at a time, you must decide at once, and you cannot take the decision back.

How well you can do depends on what you know. If you can see how busy every worker is, give the piece to the least busy one. If you cannot look, pick at random or take turns. If the same customer must always go to the same worker, you need a fixed rule that maps the customer to a worker, and the rule should change little when a worker joins or leaves.

## Definition

**Input.** A set of $n$ servers, with capacities $c_1, \ldots, c_n > 0$ (all 1 when the servers are equal), and a sequence of jobs $j = 1, 2, \ldots$. Job $j$ has a size $p_j > 0$ and, in some forms, a key $k_j$ and a set of servers that may run it.

**Output.** An assignment $a(j) \in \{1, \ldots, n\}$ for each job.

**Load.** The load of server $i$ at time $t$ is $L_i(t) = \frac{1}{c_i}\sum p_j$, summed over the jobs $j$ with $a(j) = i$ that are present at time $t$. When jobs never leave, this is the total size assigned to $i$, and its maximum over $i$ is the [makespan](/makespan/).

**Goal.** Make $\max_i L_i$ small, at all times or at the end. Common yardsticks are the average load $\sum_j p_j/\sum_i c_i$, the optimal offline value, and for random rules the maximum load with high probability. When jobs are requests that wait in queues, the goal is often the mean or a high percentile of the response time instead.

**Constraints of the dispatcher.** An *online* dispatcher assigns job $j$ when it arrives, without knowledge of later jobs, and never moves it. A *stateless* dispatcher keeps no record of past assignments and reads no loads. A *keyed* dispatcher must send equal keys to the same server, so its rule is a function of the key and the current set of servers.

## Variants

- **Offline, known sizes.** All jobs are known in advance. This is [makespan minimization](/makespan-minimization/) on identical machines, NP-hard, with good approximation algorithms such as [list scheduling](/list-scheduling/) and [longest processing time first](/longest-processing-time-first/). Machines of different speed give [uniform machine scheduling](/uniform-machine-scheduling/).
- **Online, permanent jobs.** Jobs arrive one by one and stay. This is [online makespan minimization](/online-makespan-minimization/), measured by the competitive ratio against the offline optimum. If each job may run only on some servers, it is [online restricted assignment](/online-restricted-assignment-load-balancing/).
- **Online, temporary jobs.** Jobs arrive and later finish, as requests do in a server pool. The load is the number of open requests, or the remaining work. Policies read the current loads ([least connections](/least-connections/), [weighted least connections](/weighted-least-connections/)) or latency estimates ([least response time](/least-response-time/), [peak EWMA](/peak-ewma/)). With Poisson arrivals and exponential service the problem becomes a queueing system.
- **Random equal jobs.** All jobs have size 1, and the dispatcher uses random choices. This is the [balls into bins](/balls-into-bins/) model, where the questions are the law of the maximum load and the effect of more choices.
- **Stateless dispatch.** The dispatcher keeps nothing: [random load balancing](/random-load-balancing/) and [weighted random load balancing](/weighted-random-load-balancing/). With a single counter of state it can do [round robin](/round-robin-load-balancing/) and [weighted round robin](/weighted-round-robin/).
- **Keyed (sticky) assignment.** Each job carries a key, such as a client address, a cache object or a database row, and equal keys must go to the same server. The rule is a hash of the key. The dynamic form, where servers join and leave and few keys may move, is solved by [consistent hashing](/consistent-hashing/), [rendezvous hashing](/rendezvous-hashing/) and their relatives, and is close to [sharding](/sharding/) and [hash partitioning](/hash-partitioning/).
- **Many dispatchers.** Several dispatchers share the servers and cannot see each other's decisions, so their information about the loads is partial or old. Random and sampling rules work well here, and rules that all pick the single least loaded server work badly.

## Examples

Three equal servers. Six jobs arrive in this order, with sizes $3, 1, 2, 2, 1, 3$. The total is 12, so the average load is 4.

| rule | server 1 | server 2 | server 3 | maximum load |
| --- | --- | --- | --- | --- |
| offline optimum: $\{3, 1\}, \{2, 2\}, \{1, 3\}$ | 4 | 4 | 4 | 4 |
| round robin: job $j$ to server $((j - 1) \bmod 3) + 1$ | $3 + 2 = 5$ | $1 + 1 = 2$ | $2 + 3 = 5$ | 5 |
| least loaded first, ties to the lowest index | $3 + 3 = 6$ | $1 + 2 = 3$ | $2 + 1 = 3$ | 6 |

The least loaded rule puts each job on a server of least load: after five jobs all loads are 3, and the last job of size 3 makes one load 6. Round robin is better on this input by luck. Neither rule can know that a large job comes last. This is why online rules are measured against the optimum by a competitive ratio, see [online makespan minimization](/online-makespan-minimization/) and the [list scheduling bound](/list-scheduling-bound/).

With equal jobs the picture changes. For $n$ jobs of size 1 on $n$ servers, round robin and least loaded give maximum load 1, while one uniform random choice per job gives about $\ln n/\ln\ln n$, and two random choices give about $\ln\ln n/\ln 2$.

## Known algorithms

| algorithm | state and information | keyed | maximum load, $n$ equal jobs on $n$ servers |
| --- | --- | --- | --- |
| [random load balancing](/random-load-balancing/) | none | no | $(1 + o(1))\ln n/\ln\ln n$ w.h.p. |
| [round robin](/round-robin-load-balancing/) | one counter | no | 1 |
| [power of two choices](/power-of-two-choices/) | $d$ probes per job | no | $\ln\ln n/\ln d + O(1)$ w.h.p. |
| [least connections](/least-connections/) | all loads | no | 1 |
| [peak EWMA](/peak-ewma/), [least response time](/least-response-time/) | latency estimates | no | aims at response time, not count |
| [source IP hash](/source-ip-hash/) | none, fixed $n$ | yes | as random, per key |
| [consistent hashing](/consistent-hashing/) | the ring of servers | yes | $\Theta(\log n)$ times the mean with one point per server, $1 + \epsilon$ times with [virtual nodes](/virtual-nodes/) |
| [bounded-load consistent hashing](/bounded-load-consistent-hashing/) | the ring and all loads | mostly | at most $1 + \epsilon$ times the mean |
| [list scheduling](/list-scheduling/), [LPT](/longest-processing-time-first/) | all loads, sizes | no | 1 |

The bounds for random keyed rules hold when the keys are distinct and the hash behaves like a random function. A [load balancer](/load-balancer/) in practice combines one of these rules with health checks and weights.

## Bounds

- **Offline.** The optimum is at least the average load and at least the largest job. Finding it is NP-hard, see [makespan minimization](/makespan-minimization/).
- **Online.** No deterministic online rule matches the offline optimum on every input. The guarantees of list scheduling and the best known ratios are on [online makespan minimization](/online-makespan-minimization/) and the [list scheduling bound](/list-scheduling-bound/). With restricted assignment the best ratio is $\Theta(\log n)$.
- **Random rules, equal jobs.** One uniform choice gives a maximum load of $(1 + o(1))\ln n/\ln\ln n$ for $n$ jobs ([maximum load of balls into bins](/balls-into-bins-max-load/)). The least loaded of $d \ge 2$ uniform choices gives $\ln\ln n/\ln d + \Theta(1)$ ([power of d choices theorem](/power-of-d-choices-theorem/)).
- **Keyed rules.** A key must go where the hash sends it, so the load of a server is the number of keys in its share. With consistent hashing and one point per server the largest share is $\Theta(\log n/n)$ ([consistent hashing load bound](/consistent-hashing-max-load-bound/)). A rule that sends keys to the least loaded server cannot also be a fixed function of the key.

## Reductions

- **Equal jobs and random choices** reduce to [balls into bins](/balls-into-bins/): jobs are balls, servers are bins.
- **The offline problem with known sizes** is [makespan minimization](/makespan-minimization/), with $n$ servers as the machines.
- **Keyed assignment** reduces to choosing a hash function from keys to servers. The mod-$n$ hash is balanced but moves almost every key when $n$ changes. Consistent hashing keeps balance and moves only a $1/n$ share, see the [monotonicity property](/monotonicity-property/).
- **Servers of different capacity** reduce to equal servers by giving server $i$ a share in proportion to $c_i$: weights in random and round robin rules, or more virtual nodes on a hash ring.

## Applications

- **Web and service traffic.** A [load balancer](/load-balancer/) spreads requests across the replicas of a service.
- **Caches and storage.** Distributed caches and key value stores assign keys to nodes with consistent hashing, so that a node can join or leave without a full reshuffle.
- **Parallel computing.** A scheduler assigns tasks to processors or threads; work stealing and task queues are load balancing at run time.
- **Networks.** Routers split flows over equal paths with [ECMP hashing](/ecmp-hashing/), which keeps the packets of a flow on one path.
- **Databases.** [Sharding](/sharding/) splits a table over machines by a hash or a range of the key, and then has to deal with [load skew](/load-skew/).

## References
