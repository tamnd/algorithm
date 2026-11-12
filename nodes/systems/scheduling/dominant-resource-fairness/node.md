---
tag: DB84HW
kind: algorithm
slug: dominant-resource-fairness
name: Dominant resource fairness
aliases:
- DRF
area: systems/scheduling
level: research
summary: Max-min fairness for several resource types. A user's dominant share is its largest share of any resource; progressive filling equalizes these shares until each user's bottleneck is used up.
solves: [cluster-scheduling]
model: real-ram
complexity:
  vars: {n: the number of users, m: the number of resource types}
  time: {worst: O(n^2 m)}
  space: {extra: O(n + m)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 2011
  people: [Ali Ghodsi, Matei Zaharia, Benjamin Hindman, Andy Konwinski, Scott Shenker, Ion Stoica]
  note: Ghodsi, Zaharia, Hindman, Konwinski, Shenker and Stoica defined dominant resource fairness and proved its fairness properties at NSDI 2011, and implemented it in the Mesos cluster manager.
prereqs: [max-min-fairness, pareto-optimality]
see_also: [cluster-scheduling, proportional-fairness, weighted-fair-queueing, linear-programming-problem, lottery-scheduling, completely-fair-scheduler, backfilling, nash-equilibrium]
sources:
  - paper: "Ali Ghodsi, Matei Zaharia, Benjamin Hindman, Andy Konwinski, Scott Shenker and Ion Stoica, Dominant Resource Fairness: Fair Allocation of Multiple Resource Types, Proceedings of the 8th USENIX Symposium on Networked Systems Design and Implementation (NSDI), 2011"
    title: "Dominant Resource Fairness: Fair Allocation of Multiple Resource Types"
    locator: pages 323 to 336 (the definition, the example with 9 CPUs and 18 GB, Algorithm 1, progressive filling, the properties and their proofs, and the comparison with asset fairness and CEEI)
---

Dominant resource fairness (DRF) is a rule for dividing several resource types, such as CPUs and memory, among users whose tasks need them in fixed proportions. The *dominant share* of a user is the largest of its shares of the resources: a user that holds 3 of 9 CPUs and 1 of 18 GB has a dominant share of $1/3$. DRF applies [max-min fairness](/max-min-fairness/) to the dominant shares: it makes the smallest dominant share as large as possible, then the next smallest, and so on. It is computed by *progressive filling*: all users raise their dominant shares at the same rate, and a user stops when a resource that it needs runs out. With one resource type, DRF is max-min fairness. Ghodsi and others proved that DRF gives each user at least as much as an equal split, that no user envies another, that no user can gain by lying about its demand, and that the result is [Pareto efficient](/pareto-optimality/).

## In plain words

A shared cluster has CPUs and memory. One team runs tasks that need much memory and little CPU; another team runs tasks that need much CPU and little memory. How should the cluster be split fairly?

For each team, look at the resource that it uses the most of, compared with the size of the cluster. That fraction is the team's main share. DRF tries to make the main shares of all teams equal, and as large as possible.

Imagine all teams growing at the same pace. When a resource runs out, every team that needs it must stop. The other teams keep growing until they too hit a resource that is used up.

## The problem

There are $m$ resource types with capacities $C_1, \ldots, C_m > 0$, and $n$ users. Each task of user $i$ needs the demand vector $D_i = (D_{i1}, \ldots, D_{im})$, with $D_{ir} \ge 0$ and at least one positive entry. A user gets $x_i \ge 0$ tasks (fractional tasks are allowed in the model), so it holds $x_i D_{ir}$ of resource $r$. An allocation is feasible if $\sum_i x_i D_{ir} \le C_r$ for every $r$. User $i$ values an allocation only by the number of tasks it can run; extra resources outside the proportions of $D_i$ are of no use to it.

Let $d_i = \max_r D_{ir} / C_r$ be the dominant share of one task of user $i$. Then the dominant share of user $i$ is $s_i = x_i d_i$, and the resource that attains the maximum is its *dominant resource*. DRF chooses the feasible allocation whose sorted vector of dominant shares is the largest in lexicographic order (the leximin optimum).

## The algorithm

```pseudo id=main
DRF-PROGRESSIVE-FILLING(C, D)
L1  for each user i do d_i ← max_r D_ir / C_r; x_i ← 0; mark i active
L2  while some user is active do
L3      for each resource r needed by an active user do s_r ← (C_r − Σ_{frozen i} x_i D_ir) / Σ_{active i} D_ir / d_i
L4      s ← the smallest s_r; R* ← the resources with s_r = s
L5      for each active user i do x_i ← s / d_i              ▷ every active user has dominant share s
L6      freeze every active user i that needs a resource in R*  (D_ir > 0)
```

At level $s$, an active user holds $s / d_i$ tasks, so resource $r$ is in use by $\sum_{\text{frozen}} x_i D_{ir} + s \sum_{\text{active}} D_{ir} / d_i$, which grows linearly in $s$. Line L3 finds the level at which each resource runs out, and line L4 takes the first one. In each pass at least one user is frozen, because every resource with a positive rate is needed by some active user.

**Whole tasks.** The paper's Algorithm 1 works with whole tasks. It repeatedly picks the user with the lowest dominant share and launches one more of its tasks, and it stops when that task does not fit. The implementation includes it as `drf_discrete`.

## Example

This is the example of the paper. The cluster has 9 CPUs and 18 GB of memory. Each task of user A needs $\langle 1\ \text{CPU}, 4\ \text{GB} \rangle$, and each task of user B needs $\langle 3\ \text{CPU}, 1\ \text{GB} \rangle$.

- For A, one task is $1/9$ of the CPUs and $4/18 = 2/9$ of the memory, so $d_A = 2/9$ and memory is A's dominant resource.
- For B, one task is $3/9 = 1/3$ of the CPUs and $1/18$ of the memory, so $d_B = 1/3$ and CPU is B's dominant resource.

At level $s$, A runs $s / (2/9) = 9s/2$ tasks and B runs $s / (1/3) = 3s$ tasks. The CPUs in use are $9s/2 + 9s = 27s/2$, which reaches 9 at $s = 2/3$. The memory in use is $18s + 3s = 21s$, which reaches 18 only at $s = 6/7$. So the CPUs run out first, at $s = 2/3$, and both users need CPUs, so both are frozen.

| user | tasks | CPUs | memory | dominant share |
|---|---|---|---|---|
| A | 3 | 3 | 12 GB | $12/18 = 2/3$ |
| B | 2 | 6 | 2 GB | $6/9 = 2/3$ |
| total | | 9 of 9 | 14 of 18 GB | |

Both users have the dominant share $2/3$, and 4 GB stay free, because no user can use memory without more CPUs. The tests check these numbers with exact fractions, and Algorithm 1 gives the same 3 and 2 tasks.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md). They are for the divisible model, as in the paper.

1. **Feasibility and termination.** No resource is used beyond its capacity, and each pass freezes at least one user, so there are at most $n$ passes.
2. **Sharing incentive.** Every user gets a dominant share of at least $1/n$, which is what an equal split of every resource gives it.
3. **Pareto efficiency.** Each user needs a resource that is used up, so no user can get more tasks unless another gets fewer.
4. **Envy-freeness.** No user can run more tasks with another user's resources than with its own.
5. **Max-min property.** If another feasible allocation gives user $i$ a larger dominant share, it gives a smaller one to some user $j$ whose DRF share is at most that of $i$. So DRF maximizes the smallest dominant share, and it is the leximin optimum.

The paper proves these four properties: sharing incentive, strategy-proofness, envy-freeness and Pareto efficiency. Strategy-proofness, that no user can get more tasks by reporting a false demand vector, is proved in the paper and is not repeated here. The tests check claims 1 to 5 on random instances, and compare DRF with a brute force over a grid of allocations in the leximin order.

## Complexity

Each pass of lines L3 to L6 takes $O(nm)$ time: line L3 sums over the users for each resource. There are at most $n$ passes, so the total is $O(n^2 m)$ arithmetic operations, in exact rational arithmetic. The space is $O(n + m)$. Algorithm 1 for whole tasks keeps the users in a [priority queue](/priority-queue/) by dominant share, so each task costs $O(m + \log n)$.

## Properties

- **Reduces to max-min fairness.** With one resource, the dominant share is the share of that resource, and DRF is max-min fairness.
- **Bottleneck fairness.** If one resource is the dominant resource of every user, DRF is max-min fairness on that resource.
- **Population monotonicity.** When a user leaves and gives back its resources, no other user gets fewer tasks.
- **Not resource monotone.** Adding more of a resource can lower the allocation of some user. The paper shows that no rule can have resource monotonicity together with sharing incentive and Pareto efficiency.
- **Unused resources.** Resources that no unfrozen user can use stay idle, as the 4 GB of memory in the example.
- **Leontief preferences.** The properties rely on users whose tasks need fixed proportions of the resources.

## Variants and improvements

- **Weighted DRF.** Give user $i$ a weight $w_i$, and equalize $s_i / w_i$ instead of $s_i$.
- **Asset fairness.** Equalize the sum of a user's shares over all resources. The paper shows that it fails the sharing incentive.
- **Competitive equilibrium from equal incomes (CEEI).** Give each user the same budget and find market prices. It is Pareto efficient and envy-free, but not strategy-proof.
- **Finite demands and many machines.** Real clusters have users that want a limited number of tasks and resources split across machines. DRF is then applied per offer or per machine, and the guarantees hold only approximately; see [cluster scheduling](/cluster-scheduling/).

## When to use it

Use DRF to share a cluster of several resource types between users or groups whose tasks need fixed amounts of each resource, as in Mesos and in the DRF policy of the Hadoop YARN fair scheduler. It is a good default when users may try to game the allocator, because it is strategy-proof. For one resource, plain max-min fairness or a weighted [proportional share](/lottery-scheduling/) is simpler. When the goal is throughput rather than fairness, use a packing heuristic instead.

## Pitfalls

- **Comparing raw amounts.** Comparing 3 CPUs with 12 GB has no meaning. Divide each amount by the capacity of its resource before taking the maximum.
- **Freezing too few users.** When a resource runs out, every active user that needs any of it must stop, not only the users for which it is the dominant resource (line L6).
- **Ties between resources.** Two resources can run out at the same level. Collect all of them in $R^*$ at line L4, or a user that needs only the second one keeps growing past its capacity.
- **Floating point.** The levels $s_r$ are ratios, and with floating point a resource can appear to have a tiny amount left, which leads to an extra pass that overfills it. Use exact fractions, or a tolerance.

## Implementations

## History

Ghodsi, Zaharia, Hindman, Konwinski, Shenker and Stoica introduced dominant resource fairness at NSDI 2011, motivated by data-center clusters in which tasks have very different needs for CPU and memory. They showed that DRF has sharing incentive, strategy-proofness, envy-freeness and Pareto efficiency, compared it with asset fairness and with CEEI from economics, and implemented it in the Mesos cluster manager. Work in economics and computation later extended DRF to weighted users, to indivisible tasks and to several machines.

## References
