---
tag: W7GF0B
kind: definition
slug: quorum
name: Quorum
aliases:
- quorum system
- majority quorum
area: distributed/consensus
level: intro
summary: Subsets of nodes whose pairwise intersection ensures that decisions are consistent.
prereqs: [crash-failure]
see_also: [quorum-intersection, quorum-replication, byzantine-quorum-system, flexible-paxos, paxos, split-brain, sloppy-quorum, cluster-reconfiguration]
sources:
  - paper: doi:10.1145/320071.320076
    title: Robert H. Thomas, A majority consensus approach to concurrency control for multiple copy databases, ACM Transactions on Database Systems 4(2), 180-209, 1979
    locator: the majority consensus rule, by which an update is applied only when a majority of the database sites vote for it
  - paper: doi:10.1145/800215.806583
    title: David K. Gifford, Weighted voting for replicated data, Proceedings of the 7th ACM Symposium on Operating Systems Principles (SOSP), 150-162, 1979
    locator: the votes of each copy, the read quorum r and the write quorum w, and the condition r + w greater than the total number of votes
  - paper: doi:10.1145/4221.4223
    title: Hector Garcia-Molina and Daniel Barbara, How to assign votes in a distributed system, Journal of the ACM 32(4), 841-860, 1985
    locator: the definition of a coterie (pairwise intersecting groups, none of which contains another) and its comparison with vote assignments
  - paper: doi:10.1145/214438.214445
    title: Mamoru Maekawa, A √N algorithm for mutual exclusion in decentralized systems, ACM Transactions on Computer Systems 3(2), 145-159, 1985
    locator: the request sets of size about √N, built from finite projective planes, with a grid as a simpler construction
  - paper: doi:10.1137/S0097539795281232
    title: Moni Naor and Avishai Wool, The load, capacity, and availability of quorum systems, SIAM Journal on Computing 27(2), 423-447, 1998
    locator: the definitions of load and availability, and the lower bound on the load in terms of the size of the smallest quorum
---

A quorum system over a set of nodes is a family of subsets, the quorums, such that every two quorums share at least one node. A protocol that does each decision with a quorum can then rely on one fact: any later quorum holds a node that took part in the earlier decision. This is the reason why [Paxos](/paxos/), [Raft](/raft/) and quorum-replicated storage stay consistent when some nodes fail. The most common quorums are the majorities. Weighted votes and grids give other quorum systems with other costs.

## Definition

Let $U$ be a finite set of $n$ nodes.

**Quorum system.** A quorum system over $U$ is a nonempty family $\mathcal{Q}$ of nonempty subsets of $U$ such that
$$Q_1 \cap Q_2 \ne \emptyset \qquad \text{for all } Q_1, Q_2 \in \mathcal{Q}.$$
Its members are the **quorums**. A quorum system in which no quorum contains another is a **coterie** (Garcia-Molina and Barbara, 1985). Any superset of a quorum also meets every quorum, so a protocol usually accepts any set that contains a quorum.

**Majority quorums.** $\mathcal{M}_n = \{Q \subseteq U : |Q| > n/2\}$. The smallest quorums have $\lfloor n/2 \rfloor + 1$ nodes. Two such sets have together more than $n$ members, so they share a node. The system remains usable while a quorum is alive, so it tolerates $\lfloor (n - 1)/2 \rfloor$ crashed nodes, and $n = 2f + 1$ nodes tolerate $f$. This is the rule of Thomas (1979).

**Weighted voting.** Give each node $i$ a number of votes $v_i \ge 0$, with $V = \sum_i v_i$. A set is a quorum if it holds more than $V/2$ votes. Gifford (1979) separates reads and writes: a read needs $r$ votes and a write needs $w$ votes, with
$$r + w > V \quad \text{and} \quad 2w > V.$$
The first condition makes every read quorum meet every write quorum, and the second makes two write quorums meet. Such a pair of families, where only some pairs must meet, is a **read-write quorum system** (also bicoterie). The plain definition above is the case where the two families are the same.

**Grid quorums.** Put $n = k^2$ nodes in a $k \times k$ grid. A quorum is one full row together with one full column. Its size is $2k - 1 = 2\sqrt{n} - 1$. Two quorums meet, because the row of the first and the column of the second share a cell. Maekawa (1985) used sets of size about $\sqrt{n}$ for mutual exclusion, built from finite projective planes, with grids as an easy approximation.

**Load and availability.** Naor and Wool (1998) measure a quorum system by its **load**, the smallest possible largest fraction of requests that one node must serve when the quorum for each request is chosen by the best strategy, and by its **availability**, the probability that some quorum has no failed node. They show that the load is at least the larger of $1/c$ and $c/n$, where $c$ is the size of the smallest quorum, so it is at least $1/\sqrt{n}$. Majorities have load about $1/2$ and the best availability for independent failures with probability below $1/2$. Grids have load about $2/\sqrt{n}$ but lower availability.

## Examples and non-examples

**Majorities for small $n$.**

| $n$ | smallest quorum | minimal quorums | crashes tolerated |
|---|---|---|---|
| 3 | 2 | 3 | 1 |
| 4 | 3 | 4 | 1 |
| 5 | 3 | 10 | 2 |
| 6 | 4 | 15 | 2 |
| 7 | 4 | 35 | 3 |

The number of minimal quorums is $\binom{n}{\lfloor n/2 \rfloor + 1}$. An even $n$ tolerates no more crashes than $n - 1$ and needs larger quorums, which is why clusters usually have an odd size.

**Weighted votes.** Let A have 2 votes and B, C, D 1 vote each, so $V = 5$ and a quorum needs at least 3 votes. The minimal quorums are $\{A, B\}$, $\{A, C\}$, $\{A, D\}$ and $\{B, C, D\}$, and every two of them meet. A can be a fast or reliable node: with it, two nodes are enough. With $V = 5$, Gifford's rule allows $r = 2$ and $w = 4$: reads are cheap, and since $2 + 4 > 5$, every read meets the last write.

**A $3 \times 3$ grid.** The 9 quorums, one for each choice of row and column, each have 5 nodes, and all pairs meet. Any 2 failures leave a row and a column with no failure, so the grid tolerates 2 failures. But 3 failures, one in each column, leave no full column, and then no quorum is alive. Majorities of 9 nodes also have 5 nodes, but they tolerate 4 failures. For $n = 100$, a grid quorum has 19 nodes and a majority 51.

**Non-example: half of an even set.** With $n = 4$, the sets $\{1, 2\}$ and $\{3, 4\}$ each hold half of the nodes and are disjoint. "At least half" is not a quorum rule. A network partition into two halves of this kind is how [split brain](/split-brain/) happens.

**Non-example: $r + w = n$.** With $n = 4$ replicas, $r = 2$ and $w = 2$, a write to $\{1, 2\}$ and a read from $\{3, 4\}$ do not meet, and the read misses the write. Leaderless stores that allow this, or that use a [sloppy quorum](/sloppy-quorum/), give up the guarantee on purpose.

**Non-example: rows alone.** In a grid, the family of full rows has no intersecting pairs at all. Both a row and a column are needed.

**Non-example: quorums of two different configurations.** A majority of $\{1, 2, 3\}$ and a majority of $\{1, 2, 3, 4, 5\}$ can be $\{1, 2\}$ and $\{3, 4, 5\}$, which are disjoint. This is the problem that [cluster membership change](/cluster-reconfiguration/) must solve.

## Related definitions

- [Quorum intersection](/quorum-intersection/): the counting argument behind $r + w > n$ and $2w > n$, used by every protocol on this list.
- [Quorum replication](/quorum-replication/): reads and writes to replicated data with read and write quorums.
- [Flexible Paxos](/flexible-paxos/): Paxos needs only that every phase-1 quorum meets every phase-2 quorum, so the two can have different sizes, a read-write quorum system.
- [Byzantine quorum system](/byzantine-quorum-system/): with $f$ Byzantine nodes, two quorums must share at least $f + 1$ nodes (or $2f + 1$ for masking), so that a correct node is in the intersection.
- [Sloppy quorum](/sloppy-quorum/): a set of $w$ reachable nodes that need not be the designated replicas, which keeps availability but loses the intersection.
- [Ballot number](/ballot-number/) and [view change](/view-change/): the quorum intersection is what lets a new leader learn every earlier decision.

## References
