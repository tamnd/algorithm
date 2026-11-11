---
tag: 6YJE35
kind: concept
slug: quorum-intersection
name: Quorum intersection
aliases:
- R + W > N
- quorum overlap
area: distributed/replication-and-crdts
level: core
summary: With N replicas, R + W > N makes every read quorum meet every write quorum, and 2W > N makes two write quorums meet; both follow by counting.
prereqs: [quorum]
see_also: [quorum-replication, byzantine-quorum-system, leaderless-replication, sloppy-quorum, flexible-paxos, dynamo-style-replication]
sources:
  - paper: doi:10.1145/800215.806583
    title: David K. Gifford, Weighted voting for replicated data, Proceedings of the 7th ACM Symposium on Operating Systems Principles (SOSP), 150-162, 1979
    locator: the condition that the read quorum plus the write quorum exceed the total number of votes
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 8 (quorum consensus, with the conditions 2w > v for write-write conflicts and r + w > v for read-write conflicts)
  - paper: doi:10.1007/s004460050050
    title: Dahlia Malkhi and Michael Reiter, Byzantine quorum systems, Distributed Computing 11(4), 203-213, 1998
    locator: the definitions of dissemination quorum systems (intersection of at least f + 1) and masking quorum systems (intersection of at least 2f + 1), and the bound n > 4f for threshold masking quorums
  - paper: doi:10.1137/S0097539795281232
    title: Moni Naor and Avishai Wool, The load, capacity, and availability of quorum systems, SIAM Journal on Computing 27(2), 423-447, 1998
    locator: the definitions of load and capacity, the lower bound on load in terms of the smallest quorum size, the trade off between load and availability, and the Paths system
  - paper: "Mamoru Maekawa, A square root N algorithm for mutual exclusion in decentralized systems, ACM Transactions on Computer Systems 3(2), 145-159, 1985"
    locator: quorums of size about the square root of n, built so that every two of them meet
  - paper: "Divyakant Agrawal and Amr El Abbadi, An efficient and fault-tolerant solution for distributed mutual exclusion, ACM Transactions on Computer Systems 9(1), 1-20, 1991"
    locator: the tree quorum protocol, with paths from the root to a leaf as quorums
---

Quorum intersection is the property that makes quorum-based replication correct: any two quorums that must agree share at least one server. With $N$ replicas, a read quorum of $R$ servers and a write quorum of $W$ servers, the condition $R + W > N$ makes every read quorum meet every write quorum, so a read sees at least one copy of the last completed write. The condition $2W > N$ makes every two write quorums meet, which orders the writes. Both follow from a counting argument. More general quorum systems drop the threshold form, use grids or trees, ask for larger overlaps to mask Byzantine servers, and trade the load on each server against the chance that no quorum is alive.

## In plain words

Picture ten seats in a row. One person sits in six of them, and another person sits in five. There are only ten seats, so at least one seat is used by both. That shared seat is the point of a quorum.

When a write goes to some copies and a later read asks some copies, at least one asked copy must have the write. Then the read can find the newest value. If the two groups are too small, they can miss each other, and the read sees old data.

The same idea applies to two writes. If every two write groups share a copy, the two writes meet somewhere, and that copy decides which one came first.

## The idea

### The two counting conditions

Let $U$ be the set of $N$ replicas, let $Q_r \subseteq U$ with $|Q_r| = R$ and $Q_w \subseteq U$ with $|Q_w| = W$. Since $Q_r \cup Q_w \subseteq U$,

$$|Q_r \cap Q_w| = |Q_r| + |Q_w| - |Q_r \cup Q_w| \ge R + W - N.$$

So **$R + W > N$ implies $|Q_r \cap Q_w| \ge 1$** for every choice of the two sets. The bound is tight: if $R + W \le N$, put $Q_w$ on the first $W$ replicas and $Q_r$ on the last $R$, and they are disjoint. So for size-based quorums, $R + W > N$ is exactly the condition for read and write quorums to meet. The same argument with two write quorums gives: **$2W > N$ if and only if every two write quorums meet**.

**Why $R + W > N$ is needed.** A write is complete when $W$ replicas hold it. A read that starts later asks $R$ replicas and takes the value with the newest version. If the two sets meet, the read gets at least one copy of the write, and the version tells it which value is newest. If they can miss each other, the read can return an older value although the write completed before it began.

**Why $2W > N$ is needed for write ordering.** In Gifford's weighted voting a write gets the current version number from a read quorum, adds one, and installs the new value with that number at a write quorum. Two writes that run at the same time can read the same version number and pick the same new number. If their write quorums are disjoint, both succeed, and two replicas hold different values under the same version. Later reads can then return either value, in any order, so the writes have no single order. If $2W > N$, the two write quorums share a replica, and in Gifford's scheme each write locks its quorum, so the two writes conflict at that replica and run one after the other (Bernstein, Hadzilacos and Goodman 1987, Chapter 8, state the conditions as $2w > v$ and $r + w > v$). Protocols that put the writer id into the version, as the ABD register does, order concurrent writes by the id and need only $R + W > N$; see [quorum replication](/quorum-replication/).

### Quorum systems in general

A **quorum system** over a set $U$ of $n$ servers is a family of subsets, the quorums, such that every two of them meet. A read/write quorum system has two families, with every read quorum meeting every write quorum. The threshold systems above are one case. Weighted voting gives each server $v_i$ votes and counts votes in place of servers: $r + w > V$ and $2w > V$ with $V = \sum_i v_i$. Other systems:

- **Grid.** Arrange $n = k^2$ servers in a $k \times k$ grid. A quorum is one full row and one full column, so it has $2k - 1$ servers, about $2\sqrt{n}$. Any two such quorums meet: the row of one crosses the column of the other. Maekawa (1985) gave quorums of size about $\sqrt{n}$ for mutual exclusion.
- **Tree.** Arrange the servers in a tree. A quorum is a path from the root to a leaf; if a server on the path is down, it is replaced by paths through all of its children (Agrawal and El Abbadi 1991). With all servers up a quorum has about $\log_2 n$ servers.
- **Byzantine quorums.** If up to $f$ servers can lie, one common server is not enough. Malkhi and Reiter (1998) define *dissemination* quorum systems, where every two quorums meet in at least $f + 1$ servers, for data that clients can verify, such as signed data; and *masking* quorum systems, where they meet in at least $2f + 1$ servers, so that the correct servers in the overlap outvote the liars. For threshold masking quorums of size $q$, the overlap is at least $2q - n \ge 2f + 1$, and a quorum of correct servers must exist, $q \le n - f$. Both hold only if $n > 4f$. See [Byzantine quorum system](/byzantine-quorum-system/).
- **Two kinds of quorums in consensus.** [Flexible Paxos](/flexible-paxos/) observes that Paxos needs only every phase 1 quorum to meet every phase 2 quorum, not majorities for both.

### Load and availability

Naor and Wool (1998) measure a quorum system by two numbers. The **load** of a strategy, a probability distribution over the quorums, is the largest probability that a given server is in the chosen quorum; the load $L$ of the system is the smallest load over all strategies. The **capacity** is $1/L$. They prove that if the smallest quorum has $c$ servers, then $L \ge \max(1/c, c/n)$, so $L \ge 1/\sqrt{n}$ for every quorum system. Majority quorums have load about $1/2$. The grid has load $(2k - 1)/k^2$, about $2/\sqrt{n}$, which is within a constant of the bound.

The **failure probability** $F_p$ is the chance that every quorum holds a failed server when each server fails on its own with probability $p$. Majorities are the best here for $p < 1/2$: their failure probability goes to 0 as $n$ grows. The grid goes the wrong way: when every row has a failed server, no quorum is alive, and for fixed $p$ this becomes likely as the rows grow. Naor and Wool show that low load and high availability pull against each other, and they give a system, Paths, with load $O(1/\sqrt{n})$ and a failure probability that drops exponentially in $\sqrt{n}$ for $p < 1/2$.

### The model

Intersection is a property of sets; it holds in any timing model. What it buys depends on the failure model: with crash failures one common server is enough, with Byzantine failures the overlap must be larger. The [asynchronous model](/asynchronous-model/) is the usual setting, because a client that waits for a quorum never waits for a particular server.

## Examples

**$N = 5$, $R = 2$, $W = 4$.** Every read quorum meets every write quorum in at least $2 + 4 - 5 = 1$ replica, and $2W = 8 > 5$. Reads are cheap; a write fails if two replicas are down.

**$N = 4$, $R = 3$, $W = 2$.** Reads meet writes ($3 + 2 > 4$), but $2W = 4$ is not greater than 4. The write quorums $\{S_0, S_1\}$ and $\{S_2, S_3\}$ are disjoint. Two concurrent writes with plain version numbers can both read version 0 and both install version 1, one with value $a$ and one with value $b$. A read that asks $\{S_0, S_1, S_2\}$ sees version 1 twice with $a$ and once with $b$, and nothing tells it which is right.

**$N = 3$, $R = W = 1$.** A write to $S_0$ and a later read from $S_2$ miss each other, and the read returns the old value. Stores in the style of [Dynamo](/dynamo-style-replication/) allow such settings on purpose, for speed, and accept stale reads.

**A grid of 9.** With $k = 3$, a quorum has 5 servers, the load is $5/9$ and the bound of Naor and Wool is $\max(1/5, 5/9) = 5/9$. Majority quorums of 9 have 5 servers too, and the same load. With each server down with probability $0.1$, no majority is alive with probability about $0.00089$, and no grid quorum is alive with probability about $0.0333$. The grid pays off only for large $n$, where its load goes down like $2/\sqrt{n}$ and the load of majorities stays at about $1/2$.

**Sloppy quorums break it.** A [sloppy quorum](/sloppy-quorum/) counts any $W$ healthy servers, not $W$ of the $N$ home replicas. Then $R + W > N$ no longer forces an overlap, because the two sets are drawn from more than $N$ servers.

## Where it is used

- **Replicated registers and key-value stores.** [Quorum replication](/quorum-replication/) and the ABD register rely on read and write quorums that meet; [leaderless replication](/leaderless-replication/) exposes $N$, $R$ and $W$ to the user.
- **Consensus.** [Paxos](/paxos/) and [Raft](/raft/) use majorities so that every two quorums meet, which keeps a chosen value or a committed entry from being lost.
- **Byzantine replication.** [PBFT](/pbft/) uses quorums of $2f + 1$ among $3f + 1$ replicas, which meet in $f + 1$ replicas, so at least one correct replica is in both.
- **Mutual exclusion.** Maekawa's algorithm and the tree protocol grant a lock when a quorum agrees; two holders would need two quorums that do not meet.

## References
