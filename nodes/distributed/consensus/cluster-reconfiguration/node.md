---
tag: 3KQHHP
kind: concept
slug: cluster-reconfiguration
name: Cluster membership change
aliases:
- reconfiguration
- joint consensus
area: distributed/consensus
level: advanced
summary: Safely changing the set of nodes participating in a consensus group.
prereqs: [quorum, raft, multi-paxos]
see_also: [vertical-paxos, cheap-paxos, quorum-intersection, replicated-state-machine, viewstamped-replication, split-brain, flexible-paxos, zab]
sources:
  - paper: "Diego Ongaro and John Ousterhout, In search of an understandable consensus algorithm, USENIX Annual Technical Conference (ATC), 2014"
    locator: Section 6 (cluster membership changes, the joint configuration C_old,new, and the two-phase change)
  - url: https://web.stanford.edu/~ouster/cgi-bin/papers/OngaroPhD.pdf
    title: Diego Ongaro, Consensus, bridging theory and practice, PhD thesis, Stanford University, 2014
    locator: Chapter 4 (cluster membership changes), Section 4.1 (safety of single-server changes), Section 4.2 (availability, catching up new servers and removing the leader) and Section 4.3 (arbitrary changes with joint consensus)
  - url: https://groups.google.com/g/raft-dev/c/t4xj6dJTP6E
    title: Diego Ongaro, bug in single-server membership changes, raft-dev mailing list, 10 July 2015
    locator: the counterexample with one addition and one removal in a 4-server cluster, and the fix (a leader appends no configuration entry until it has committed an entry of its current term)
  - paper: "Leslie Lamport, Paxos made simple, ACM SIGACT News 32(4), 51-58, December 2001"
    locator: Section 3 (state machines, and changing the set of servers with a command that takes effect α instances later)
  - paper: doi:10.1145/1753171.1753191
    title: Leslie Lamport, Dahlia Malkhi and Lidong Zhou, Reconfiguring a state machine, ACM SIGACT News 41(1), 63-73, 2010
    locator: the methods of reconfiguration, among them the α window and stopping the old state machine before the new one starts
  - paper: doi:10.1145/1582716.1582783
    title: Leslie Lamport, Dahlia Malkhi and Lidong Zhou, Vertical Paxos and primary-backup replication, PODC 2009, 312-313
    locator: the configuration master, and the new configuration that reads the old state before it is activated
---

A cluster membership change, or reconfiguration, replaces the set of nodes that runs a consensus protocol, while the protocol keeps running. The danger is that, for some time, some nodes use the old configuration and some use the new one, and a [quorum](/quorum/) of the old one and a quorum of the new one may not share a node. Then two leaders can commit different values. Every correct method keeps one of two rules: during the change, every quorum that can decide meets every other such quorum, or the old configuration stops deciding before the new one starts. The known methods are Lamport's α window, joint consensus and single-server changes in [Raft](/raft/), and an external configuration master as in [Vertical Paxos](/vertical-paxos/).

## In plain words

A club decides things by a majority vote of its members. Now it wants to change who the members are.

If everyone switched to the new list at the same moment, there would be no problem. But members hear about the change at different times. For a while, some count votes with the old list and some with the new list. Then a majority of the old list and a majority of the new list can be two separate groups, and each can pass its own decision.

The fix is to make sure that the two groups always share at least one person. One way is to need a majority of both lists during the change. Another way is to change one member at a time. Another way is to close the old club first and then open the new one.

## The idea

### The safety condition

A configuration $C$ is a set of nodes with a set of quorums, usually the majorities of $C$. A consensus protocol such as [Paxos](/paxos/) or Raft is safe because every two quorums it uses share a node: that node carries the knowledge of an earlier decision to every later leader. A change from $C_{old}$ to $C_{new}$ is safe if, at every moment, the set of quorums that can decide still has this property. The direct switch breaks it. Let $C_{old} = \{1, 2, 3\}$ and $C_{new} = \{1, 2, 3, 4, 5\}$. A majority of $C_{old}$ needs 2 nodes and a majority of $C_{new}$ needs 3, and $2 + 3 = 5$ is not more than the 5 nodes in total, so $\{1, 2\}$ and $\{3, 4, 5\}$ are disjoint majorities. If nodes 1 and 2 still use $C_{old}$ while nodes 3, 4 and 5 use $C_{new}$, each group can elect a leader and commit a different entry at the same index.

There are two ways to keep the condition.

1. **Overlap.** Arrange that a quorum of every configuration that can be in use meets a quorum of every other one. Joint consensus and single-server changes do this.
2. **Hand-off.** Stop the old configuration, so that it can decide nothing more, and start the new one from its final state. The α window, the stop command of Lamport, Malkhi and Zhou (2010) and Vertical Paxos do this.

### The α window of Paxos

In Paxos Made Simple (Section 3), the set of servers is part of the state of the [replicated state machine](/replicated-state-machine/). The configuration that runs instance $i + \alpha$ of [Multi-Paxos](/multi-paxos/) is the one given by the state after the command of instance $i$ is executed. A change is an ordinary command, and it takes effect $\alpha$ instances later.

This works because the configuration of each instance is fixed by an earlier decision, which all nodes learn in the same way. So there is never a doubt about which quorums decide instance $j$. The cost is that a leader can run instances only up to $\alpha$ ahead of the last one it knows is chosen, because it cannot know the configuration of instance $j$ before instance $j - \alpha$ is chosen. A small $\alpha$ limits pipelining. A large $\alpha$ makes a change take effect late, though the leader can fill the window quickly with no-op commands.

### Joint consensus

Raft (Ongaro and Ousterhout, Section 6) changes the configuration in two steps through a joint configuration $C_{old,new}$. A set $Q$ is a quorum of $C_{old,new}$ if it holds a majority of $C_{old}$ and a majority of $C_{new}$. The leader appends $C_{old,new}$ to the log as an entry. Each server uses the latest configuration in its log, whether it is committed or not. When $C_{old,new}$ is committed, the leader appends $C_{new}$. When $C_{new}$ is committed, the change is over, and the servers that are not in $C_{new}$ can be shut down. A leader that is not in $C_{new}$ steps down then.

**Claim.** A quorum of $C_{old,new}$ meets every majority of $C_{old}$ and every majority of $C_{new}$.

*Proof.* A quorum $Q$ of $C_{old,new}$ holds a majority $M$ of $C_{old}$. Two majorities of the same set share a node, so $M$, and with it $Q$, meets every majority of $C_{old}$. The same holds for $C_{new}$. $\square$

There is never a time at which $C_{old}$ and $C_{new}$ can both decide on their own. Before $C_{old,new}$ is committed, a leader uses $C_{old}$ or $C_{old,new}$. After it is committed, a leader must have it in its log, by the election rule, so it uses $C_{old,new}$ or, later, $C_{new}$. Before $C_{new}$ can be appended, $C_{old,new}$ must be committed, so no leader uses $C_{new}$ while another can still use $C_{old}$. In every pair of configurations that can be in use at the same time, at least one is $C_{old,new}$, and by the claim their quorums meet. Joint consensus allows any change, for example from $\{1, 2, 3\}$ to $\{3, 4, 5\}$ in one go.

### Single-server changes

The Raft thesis (Section 4.1) gives a simpler method: add or remove one server at a time.

**Claim.** Let $C$ be a set of $n$ servers and $C' = C \cup \{x\}$ with $x \notin C$. Every majority of $C$ meets every majority of $C'$.

*Proof.* A majority $Q$ of $C$ has at least $\lfloor n/2 \rfloor + 1$ members. A majority $Q'$ of $C'$ has at least $\lfloor (n+1)/2 \rfloor + 1$ members, and at most one of them is $x$, so $|Q' \cap C| \ge \lfloor (n+1)/2 \rfloor$. Both $Q$ and $Q' \cap C$ are subsets of $C$, and $|Q| + |Q' \cap C| \ge \lfloor n/2 \rfloor + \lfloor (n+1)/2 \rfloor + 1 = n + 1 > n$, so they share a server. A removal is the same claim with the roles of $C$ and $C'$ swapped. $\square$

So a single change needs no joint configuration: the leader appends $C'$, each server uses it as soon as it is in its log, and the next change waits until $C'$ is committed. The claim does not hold for two servers at a time: from 3 to 5 servers is exactly the direct switch above.

### The 2015 bug in single-server changes

In July 2015, Ongaro posted on the raft-dev list a counterexample, found by Huanchen Zhang and Brandon Amos, to the single-server method of his thesis. The rule "wait until the previous change is committed" was not enough, because two changes made by leaders of different terms can both start from the same committed configuration, and the two new configurations then differ by two servers.

The fix that he gave is: **a leader may not append a configuration entry until it has committed an entry of its own term.** In practice, a new leader first commits its no-op entry. The post gives no proof; this is a sketch of why it works. When the leader of term $t$ has committed an entry of term $t$ with a majority of the configuration $C$ in its log, those servers have logs that end in term $t$ or later. A configuration entry $D$ from an older term that is not in this leader's log differs from $C$ by one server. So every majority of $D$ meets that majority of $C$, and the server in the intersection has a more up-to-date log than any log that ends in $D$, and refuses to vote. A server that holds $D$ can never again become leader, so $D$ can never be committed. The example below goes through the counterexample step by step.

### An external master

[Vertical Paxos](/vertical-paxos/) and many primary-backup systems take the decision about membership out of the group. A configuration master, which is itself replicated, gives each new ballot its own set of acceptors and its quorums. A leader of a new configuration first reads the state from a read quorum of the old configuration, and only then does the master activate the new one. After that, the old configuration is no longer needed, which is the hand-off rule. Because the master decides membership, the group itself can use smaller quorums, for example $f + 1$ replicas to survive $f$ crashes.

### Practical points

- **Catching up.** A new server with an empty log cannot help commit until it has the log. Raft adds it first as a non-voting member (Ongaro, Section 4.2). Otherwise adding a server to a 3-server cluster where one server is down can stop progress, because 3 of the new 4 are needed and only 2 have the log.
- **Removing the leader.** A leader that is removed must keep managing the cluster until the new configuration is committed, but must not count itself in the quorums of $C_{new}$.
- **Removed servers.** A server that is removed but still running does not hear heartbeats and starts elections with higher terms. Raft servers ignore vote requests while they hear from a current leader.

## Examples

**Joint quorums, with numbers.** Let $C_{old} = \{1, 2, 3\}$ and $C_{new} = \{3, 4, 5\}$. Their majorities can be disjoint: $\{1, 2\}$ and $\{4, 5\}$. The minimal quorums of $C_{old,new}$ are five sets: $\{1, 3, 4\}$, $\{1, 3, 5\}$, $\{2, 3, 4\}$, $\{2, 3, 5\}$ and $\{1, 2, 4, 5\}$. Each holds 2 of $\{1, 2, 3\}$ and 2 of $\{3, 4, 5\}$, so each meets every majority of either side. For $C_{old} = \{1, 2, 3\}$ and $C_{new} = \{1, 2, 3, 4, 5\}$ the minimal joint quorums are the seven sets of size 3 that hold at least 2 of $\{1, 2, 3\}$.

**Single-server overlap, with numbers.** From 3 to 4 servers: a majority of 3 has 2 servers, a majority of 4 has 3 servers, and at most one of those 3 is the new server, so at least 2 are old. Since $2 + 2 > 3$, the two groups of old servers share one. From 4 to 5: $3 + 2 > 4$. The test `test_single_server_changes_keep_majorities_overlapping` checks every subset $C$ of $\{1, \ldots, 5\}$ and every one-server change of it.

**The counterexample of 2015.** The start is $C = \{1, 2, 3, 4\}$, and entry 1 is committed on all servers. This is the trace of `ongaro_scenario` in `impl/python/reconfiguration.py`.

| step | event | index 2 on each server |
|---|---|---|
| 1 | Leader 1 (term 1) appends $D = C \cup \{5\}$ at index 2 and sends it only to server 5. Then it stops. | 1: $D$, 5: $D$ |
| 2 | Server 2 wins term 2 with votes of 2, 3 and 4, a majority of $C$. | |
| 3 | Leader 2 appends $E = C \setminus \{1\} = \{2, 3, 4\}$ at index 2 and sends it to 3. Now $\{2, 3\}$ is a majority of $E$, so $E$ is committed. | 2: $E$, 3: $E$ |
| 4 | Server 1 tries term 2 and fails (server 4 voted for 2), then wins term 3 with votes of 1, 4 and 5, a majority of $D$. The logs of 4 and 5 are not more up to date than its own. | |
| 5 | Leader 1 appends a no-op at index 3, sends its log to 4 and 5, and commits index 3 with $\{1, 4, 5\}$. | 1, 4, 5: $D$ |

Index 2 is now committed as $E$ by leader 2 and as $D$ by leader 1, so two committed logs disagree. With the fix, leader 2 in step 3 must first commit its no-op of term 2 with 3 of the 4 servers of $C$, for example $\{2, 3, 4\}$. Then in step 4, server 4 has a log that ends in term 2 and refuses server 1, every majority of $D$ holds one of 2, 3 or 4, and server 1 cannot win. The model reports a violation without the fix and none with it.

**Random runs.** The model in `impl/python/reconfiguration.py` starts with $\{1, 2, 3\}$ out of 5 servers. It runs random elections, appends, partial replication and commits, and a leader counts acknowledgements it got earlier. A change is allowed only after the last configuration in the leader's log is committed. In 500 runs of 150 steps each:

| method | changes made | runs where two leaders committed different entries at one index |
|---|---|---|
| joint consensus | 1173 | 0 |
| joint consensus, with the no-op rule | 340 | 0 |
| single-server, with the no-op rule | 332 | 0 |
| single-server, without the no-op rule | 1167 | 0 |
| direct switch to a random set | 1218 | 11 |

The random runs did not find the single-server bug, because it needs a precise order of events, so the test checks it with the fixed trace above.

## Where it is used

- Raft implementations change membership with single-server changes and the no-op rule, or with joint consensus. etcd supports both.
- Multi-Paxos systems that put the configuration in the replicated log use the α method; Lamport, Malkhi and Zhou (2010) compare it with methods that stop the old state machine.
- [Viewstamped Replication](/viewstamped-replication/) Revisited changes the group with a reconfiguration request that ends the current epoch, a hand-off: the old group stops and the new group starts from its state.
- [Zab](/zab/) in ZooKeeper 3.5 and later supports dynamic reconfiguration.
- Primary-backup systems with an external master, such as chain replication, are instances of [Vertical Paxos](/vertical-paxos/). [Cheap Paxos](/cheap-paxos/) uses reconfiguration to remove failed main processors, so that auxiliary processors rarely have to act.

## References
