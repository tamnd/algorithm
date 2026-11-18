---
tag: GRVJKV
kind: problem
slug: data-allocation-problem
name: Data allocation problem
aliases:
- file allocation problem
- fragment allocation
area: databases/distributed-databases
level: advanced
summary: "Place fragments and their copies on sites to minimize storage, query and update cost under capacity limits. The decision version is NP-complete."
prereqs: [horizontal-fragmentation, facility-location-problem]
see_also: [vertical-fragmentation, schism-partitioning, quadratic-assignment-problem, binary-integer-programming, eager-and-lazy-replication, partition-problem, set-cover, local-search]
sources:
  - paper: doi:10.1109/T-C.1969.222542
    title: Wesley W. Chu, Optimal file allocation in a multiple computer system, IEEE Transactions on Computers C-18(10), 1969, pages 885 to 889
    locator: the zero-one programming model of the allocation of files and their copies to the computers of a network, with storage and transmission costs and capacity limits
  - paper: "Kapali P. Eswaran, Placement of records in a network file system, Proceedings of the IFIP Congress 1974"
    title: Placement of records in a network file system
    locator: the result, usually credited to this paper, that the file allocation problem is NP-complete
  - paper: doi:10.1145/356876.356883
    title: Lawrence W. Dowdy and Derrell V. Foster, Comparative models of the file assignment problem, ACM Computing Surveys 14(2), 1982, pages 287 to 313
    locator: the survey and comparison of the cost models, constraints and solution methods for file assignment
  - book: isbn:9783030262525
    title: M. Tamer Özsu and Patrick Valduriez, Principles of Distributed Database Systems, fourth edition, Springer, 2020
    locator: Chapter 2, Distributed and Parallel Database Design, the section on allocation (the information that allocation needs and the allocation model)
---

The data allocation problem asks where to store the fragments of a distributed database. Each fragment, for example a [horizontal fragment](/horizontal-fragmentation/) of a relation, can be stored at one site or copied to several sites. A copy near the users makes their reads cheap, but each copy costs storage and must receive every update. The problem is to choose the set of sites for each fragment so that the total cost of storage, reads and updates is least, within the storage capacity of each site. Chu (1969) gave a zero-one programming model of this problem for files in a computer network. Without capacities, the problem for one fragment is the [uncapacitated facility location problem](/facility-location-problem/); with capacities, even finding a feasible placement is NP-complete.

## In plain words

A company keeps its data in several cities. Each piece of data must live somewhere, and it can live in more than one place. If a city reads a piece of data often, a local copy saves the cost of asking another city. But every copy uses disk space, and every change to the data must be sent to every copy. So a piece that many cities read and few change should have many copies, and a piece that changes often should have few. The cities also have limited disk space. The task is to pick, for each piece, the cities that store it, so that the total cost of disks, reads and changes is as small as possible. Finding the best choice is hard in general, so systems use fast rules of thumb and improve the result step by step.

## Definition

**Input.**

- Sites $1, \dots, n$, with a storage capacity $C_k$ and a storage cost $s_k$ per unit at site $k$.
- A communication cost $c_{jk} \ge 0$ per unit sent from site $j$ to site $k$, with $c_{kk} = 0$.
- Fragments $1, \dots, m$, with a size $a_i$.
- For each fragment $i$ and site $j$, a read rate $r_{ij}$ and an update rate $u_{ij}$, the number of reads and updates of fragment $i$ that queries at site $j$ make per period.

**Output.** A set $S_i \subseteq \{1, \dots, n\}$ of sites for each fragment, with $S_i \neq \emptyset$. In zero-one form, $x_{ik} = 1$ if and only if $k \in S_i$.

**Cost.** A read goes to the nearest copy, and an update goes to every copy:

$$\text{cost} = \sum_{i} \Bigl( \sum_{k \in S_i} a_i s_k \;+\; \sum_j r_{ij}\, a_i \min_{k \in S_i} c_{jk} \;+\; \sum_j u_{ij}\, a_i \sum_{k \in S_i} c_{jk} \Bigr).$$

**Constraints.** Each site holds at most its capacity, $\sum_{i : k \in S_i} a_i \le C_k$ for every $k$. The goal is a feasible allocation of least cost.

The model charges a read and an update by the volume of data it moves. Other models charge the response time, add a limit on the number of copies, or add an availability constraint, such as at least two copies of each fragment.

## Variants

- **Non-redundant allocation.** Each fragment has exactly one copy, $|S_i| = 1$. Without capacities and with fragments that queries use independently, each fragment goes to the site that minimizes its own cost.
- **Redundant allocation.** Copies are allowed, as in the definition. The update term grows with the number of copies and the read term shrinks, so the best number of copies is a balance of the two.
- **Uncapacitated allocation.** No capacity limits. Then the fragments are independent, and the problem splits into one problem for each fragment.
- **Allocation with query costs.** A query that joins two fragments costs less when they are at the same site. The cost then depends on pairs of fragments, and the problem becomes a [quadratic assignment problem](/quadratic-assignment-problem/) in the non-redundant case.
- **Joint fragmentation and allocation.** [Schism](/schism-partitioning/) chooses both from a trace of transactions, by a [graph partitioning](/graph-partitioning-problem/) of the rows.
- **Dynamic allocation.** The rates change over time, and copies are moved or dropped as the workload changes. How the copies are kept up to date is the topic of [eager and lazy replication](/eager-and-lazy-replication/).

## Examples

**One fragment on three sites.** A fragment of size 1 can be stored at sites 1, 2 and 3. Every message between two different sites costs 1, and each copy costs 3. The read rates are $r = (10, 9, 1)$ and the update rates are $u = (1, 1, 4)$ for the three sites.

A copy at site $k$ costs its storage plus the updates that other sites send to it: $3 + 1 + 4 = 8$ at site 1, 8 at site 2, and $3 + 1 + 1 = 5$ at site 3. A read at a site without a copy costs its read rate.

| sites with a copy | copies | reads | total |
|---|---|---|---|
| $\{1\}$ | 8 | 9 + 1 | 18 |
| $\{2\}$ | 8 | 10 + 1 | 19 |
| $\{3\}$ | 5 | 10 + 9 | 24 |
| $\{1, 2\}$ | 16 | 1 | **17** |
| $\{1, 3\}$ | 13 | 9 | 22 |
| $\{2, 3\}$ | 13 | 10 | 23 |
| $\{1, 2, 3\}$ | 21 | 0 | 21 |

Two copies, at sites 1 and 2, are best. If the update rate of site 3 rises from 4 to 6, a copy at site 1 or 2 costs 10, and one copy at site 1 is best, with cost $10 + 9 + 1 = 20$ against 21 for $\{1, 2\}$. More updates mean fewer copies.

**Capacity makes it hard.** Two sites, each of capacity 5, and fragments of sizes 3, 3, 2 and 2 have a feasible placement, $\{3, 2\}$ and $\{3, 2\}$. Sizes 3, 3 and 4 with the same capacities have no feasible placement, though the total size 10 fits the total capacity. Deciding which case holds is the [partition problem](/partition-problem/).

## Known algorithms

- **Exact methods.** The zero-one model of Chu (1969) is a [binary integer program](/binary-integer-programming/): linearize the nearest-copy term with variables $y_{ijk}$ that say which copy serves the reads of site $j$, as in the facility location formulation. Branch and bound solves small and medium instances.
- **Facility location algorithms.** In the uncapacitated case, the problem for each fragment is uncapacitated facility location, so the algorithms of the [facility location problem](/facility-location-problem/) apply. When the costs $c_{jk}$ form a metric, these include constant-factor approximation algorithms. With capacities, the fragments share the space of each site, so the problem no longer splits into one problem for each fragment. Each site then adds a constraint of the [knapsack](/knapsack-problem/) form, and the usual method is the integer program below or a heuristic.
- **The all beneficial sites method.** A [greedy](/greedy-algorithm/) heuristic: first store each fragment at the site that reads it most. Then add a copy at each site where the read cost that the copy saves is larger than the update and storage cost that it adds, while the capacity allows. This is a heuristic with no bound on its error.
- **Local search.** Start from a feasible allocation and move, add or drop one copy while the cost goes down, as in [local search](/local-search/) and [hill climbing](/hill-climbing/). Moves that swap two fragments between sites help when the capacities are tight. Simulated annealing and genetic search are also used. These are heuristics; their quality is a measurement on test workloads.

## Bounds

**Theorem (capacities).** With capacities, deciding whether a feasible allocation exists is NP-complete, even with two sites and no copies. *Proof.* A placement can be checked in polynomial time. For a reduction from the partition problem, take numbers $a_1, \dots, a_m$ with sum $2B$, two sites of capacity $B$, and one fragment of size $a_i$ for each number. Each fragment needs a copy, and the two sites hold $2B$ in total, so a feasible allocation stores each fragment exactly once and fills both sites exactly. That is a partition into two halves of sum $B$. $\square$ So, unless P = NP, no polynomial algorithm finds an allocation within any factor of the optimum, since it would have to find a feasible one first.

**Theorem (no capacities).** Without capacities, the problem is NP-hard even for one fragment that is only read. *Proof.* Reduce from [set cover](/set-cover/). For a universe $U$ and sets $T_1, \dots, T_q$, make one site for each set, with storage cost 1 and read rate 0, and one site for each element, with storage cost $q + 1$ and read rate 1. Let the cost from an element site to a set site be 0 if the element is in the set and $q + 1$ if it is not. A solution that stores no copy at an element site and reads every element at cost 0 costs exactly the number of copies, which form a set cover. Any other solution costs at least $q + 1$, while the cover by all the sets costs $q$. So a cover of size $t$ exists if and only if an allocation of cost $t$ exists. $\square$ The decision version, "is there an allocation of cost at most $B$", is in NP, so it is NP-complete. The result is usually credited to Eswaran (1974).

**Polynomial cases.** Non-redundant allocation without capacities and without query costs between fragments takes $O(m n^2)$ time: for each fragment, try each site and add up the costs. The redundant case of one fragment with $n$ sites can be solved by trying all $2^n - 1$ sets of sites, which is the method of the example.

## Reductions

**To facility location.** Fix a fragment $i$ and drop the capacities. The update term $\sum_j u_{ij} a_i \sum_{k \in S_i} c_{jk}$ is a sum over the copies, so it can be moved into the cost of opening site $k$:
$$f_k = a_i s_k + a_i \sum_j u_{ij} c_{jk}.$$
The read term is the demand $r_{ij} a_i$ of client $j$ times the distance $c_{jk}$ to the nearest open site. So the problem for one fragment is uncapacitated facility location with the sites as both the facilities and the clients, and the opening costs $f_k$. The example above computes these $f_k$. The reduction runs both ways: the set cover proof above builds an instance of this form.

**From partition.** The capacity proof above shows that the capacitated case contains the partition problem, and so also [bin packing](/bin-packing/) when the number of sites is part of the input.

**To integer programming.** With $x_{ik}$ for the copies and $y_{ijk}$ for "site $j$ reads fragment $i$ from site $k$", the problem is a [binary integer program](/binary-integer-programming/) with the constraints $\sum_k y_{ijk} = 1$, $y_{ijk} \le x_{ik}$, and the capacity rows $\sum_i a_i x_{ik} \le C_k$.

## Applications

- **Distributed database design.** After the [vertical](/vertical-fragmentation/) or horizontal fragmentation, the designer allocates the fragments to the sites. The allocation fixes the costs that [distributed query processing](/distributed-query-processing/) can then reach.
- **Replica placement.** Geo-distributed stores and content delivery networks decide how many copies of each item to keep and where, with the same trade-off between read latency and update cost.
- **File assignment.** The early form of the problem, which Chu (1969) and the survey of Dowdy and Foster (1982) study, places files on the computers of a network.
- **Shard placement.** A system that uses [sharding](/sharding/) places and moves shards so that the servers have balanced load and enough free space.

## References
