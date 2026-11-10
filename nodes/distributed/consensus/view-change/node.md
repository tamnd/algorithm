---
tag: S57AM3
kind: concept
slug: view-change
name: View change
area: distributed/consensus
level: advanced
summary: Protocol step that replaces a failed primary and installs a new view.
prereqs: [quorum, ballot-number, replicated-state-machine]
see_also: [viewstamped-replication, pbft, raft, multi-paxos, leader-lease, failure-detector, primary-backup-replication, cluster-reconfiguration]
sources:
  - url: https://pmg.csail.mit.edu/papers/vr-revisited.pdf
    title: Barbara Liskov and James Cowling, Viewstamped Replication Revisited, MIT technical report MIT-CSAIL-TR-2012-021, 2012
    locator: Section 4.2 (the view change protocol with StartViewChange, DoViewChange and StartView, and the choice of the log with the largest last normal view and then the largest op-number) and Section 8 (correctness)
  - paper: doi:10.1145/62546.62549
    title: Brian M. Oki and Barbara H. Liskov, Viewstamped replication, a new primary copy method to support highly-available distributed systems, 7th ACM Symposium on Principles of Distributed Computing (PODC), 1988
    locator: the view change algorithm and viewstamps
  - paper: "Miguel Castro and Barbara Liskov, Practical Byzantine fault tolerance, 3rd USENIX Symposium on Operating Systems Design and Implementation (OSDI), 1999"
    locator: Section 4.4 (view changes, with VIEW-CHANGE messages that carry prepared certificates and the NEW-VIEW message)
  - paper: "Diego Ongaro and John Ousterhout, In search of an understandable consensus algorithm, USENIX Annual Technical Conference (ATC), 2014"
    locator: Section 5.2 (leader election) and Section 5.4.1 (the election restriction, which makes a new leader hold every committed entry)
---

A view change is the step of a primary-based replication protocol that replaces the current primary, or leader, with a new one. A view is a numbered period with a fixed primary. When the replicas suspect that the primary of view $v$ has failed, they move to view $v + 1$ with another primary. The new primary first learns the state from a [quorum](/quorum/) of replicas and builds a log that holds every operation that may have been committed, and only then starts to accept new requests. The name comes from [Viewstamped Replication](/viewstamped-replication/), where it is a protocol of its own; [PBFT](/pbft/) has the same step for Byzantine faults, and leader election in [Raft](/raft/) and phase 1 of [Multi-Paxos](/multi-paxos/) do the same job.

## In plain words

A team works through a list of tasks that its leader hands out. The leader stops answering. The team must pick a new leader and go on, without doing any finished task twice and without losing one.

So the team members first agree to stop working for the old leader. Then the new leader asks enough of them what they have on their lists. Because any task that was finished was written down by more than half of the team, and the new leader asks more than half, at least one person it asks knows about each finished task.

The new leader then takes the most recent list, sends it to everyone, and work goes on.

## The idea

### The steps

The view numbers are [ballot numbers](/ballot-number/): totally ordered, and each view has one primary, for example replica $v \bmod n$ in view $v$. With $n = 2f + 1$ replicas that may crash, a view change has four parts.

1. **Detect.** A backup that has not heard from the primary for a timeout suspects it. The protocol is safe even if the suspicion is wrong, so a timeout, or any [failure detector](/failure-detector/), is enough.
2. **Stop the old view.** The replicas that move to view $v + 1$ stop taking part in view $v$. In Viewstamped Replication, a replica in view-change status sends no PrepareOK. Once $f + 1$ replicas have moved, the old primary can never again collect a quorum, so it cannot commit anything more, even if it is alive and does not know that it was replaced.
3. **Learn from a quorum.** Each replica sends its state to the new primary: in Viewstamped Replication, a DoViewChange message with its log, the last view $v'$ in which it was in normal status, its op-number and its commit-number. The new primary waits for $f + 1$ of them, counting its own.
4. **Carry the values over and install the view.** The new primary chooses the log with the largest $v'$, and among those the one with the largest op-number. It sets its commit-number to the largest one it received, and sends StartView with the log to all replicas. The others take the log and return to normal status.

### Why no committed operation is lost

An operation $x$ is committed at position $j$ when the primary has it at $j$ and $f$ backups have acknowledged it, so $f + 1$ replicas held $x$ at $j$ in the same view. The new primary hears from $f + 1$ replicas. Since $(f + 1) + (f + 1) > 2f + 1$, at least one replica $r$ is in both sets, so the new primary sees a log with $x$ at $j$.

That is not yet enough, because the new primary keeps only one of the logs it receives. The rule "largest $v'$ first" makes the choice right. The log of $r$ was last updated in some view $v' \ge v$, where $v$ is the view in which $x$ was committed. A log with a larger $v'$ was installed by the primary of that later view, which by induction over the views already carried $x$ at $j$. A log with the same $v'$ was a prefix of the log of the same primary, and the longest such prefix is at least as long as that of $r$. In both cases the chosen log holds $x$ at $j$. The full proof is on the [Viewstamped Replication](/viewstamped-replication/) page.

The rule "longest log" alone is wrong. A long log can come from an old view, and it can hold operations that were never committed in place of ones that were. The example below shows this.

### The same step in other protocols

- **Multi-Paxos.** A new leader runs phase 1 with a higher ballot for all open instances at once. For each instance, it takes the value accepted with the highest ballot among a majority of acceptors, and fills the gaps with no-ops. This is the view change, done per instance.
- **Raft.** Raft moves the work into the election. A server votes only for a candidate whose log is at least as up to date as its own, comparing the term of the last entry and then the length. A leader is elected by a majority, so it already holds every committed entry (Ongaro and Ousterhout, Section 5.4.1), and it does not collect logs from others. It then makes the followers' logs match its own.
- **PBFT.** With $n = 3f + 1$ replicas and Byzantine faults, replicas cannot simply send their logs, because a faulty one could lie. Each VIEW-CHANGE message carries prepared certificates, each signed by $2f + 1$ replicas. The new primary collects $2f + 1$ VIEW-CHANGE messages and sends a NEW-VIEW message that includes them as proof, and every replica checks that the new primary chose the right requests and put null requests in the gaps (Castro and Liskov, Section 4.4).

### Pitfalls

- **Choosing the wrong log.** As above, the chosen log must be the one from the latest view, not simply the longest one.
- **Too few replies.** The new primary must wait for a full quorum. If it starts with fewer, it may miss the only replica that saw a committed operation.
- **Forgotten state.** A replica that crashes and returns with an empty log must not take part as if nothing had happened, or a committed operation can be at fewer than $f + 1$ replicas. Viewstamped Replication Revisited adds a recovery protocol for this.
- **Reads by the old primary.** Stopping the old view stops it from committing writes, but a primary that serves reads from its own state can still return stale data after it was replaced. It needs a [leader lease](/leader-lease/), or must check with a quorum before each read.
- **Repeated view changes.** If timeouts are too short, the replicas can keep changing views and never make progress. Protocols back off, for example by doubling the timeout after each view change.

## Examples

**Why the latest view wins over the longest log.** Three replicas $r_0, r_1, r_2$, so $f = 1$, and the primary of view $v$ is $r_{v \bmod 3}$.

1. In view 0, primary $r_0$ appends a and b to its log, but its Prepare messages are lost. Nothing is committed. Log of $r_0$: [a, b], with $v' = 0$.
2. The backups move to view 1. Primary $r_1$ gets DoViewChange messages from $r_1$ and $r_2$, both with empty logs, and starts view 1 with an empty log.
3. In view 1, $r_1$ appends c, $r_2$ acknowledges it, and c is committed at position 1 and executed. Logs of $r_1$ and $r_2$: [c], with $v' = 1$.
4. $r_1$ fails. View 2 has primary $r_2$, which gets DoViewChange messages from $r_0$ (log [a, b], $v' = 0$) and from itself (log [c], $v' = 1$). That is $f + 1 = 2$ messages.

With the right rule, $r_2$ takes [c], because $v' = 1 > 0$, and c survives. With "longest log", $r_2$ would take [a, b], and the committed c would be gone, replaced by a at position 1.

**In simulation.** The tests on the [Viewstamped Replication](/viewstamped-replication/) page run the protocol with random message delays, duplicates and view changes. With the rule from the paper, 60 runs for each of $f = 1$ and $f = 2$ keep every committed operation. With the new primary choosing the longest log, 6 of 60 runs with $f = 1$ lose a committed operation.

**The cost.** A view change in Viewstamped Replication takes three message delays after the timeout: StartViewChange to all, DoViewChange to the new primary, and StartView to all. With $n$ replicas it sends about $n^2$ StartViewChange messages and $2n$ others. The DoViewChange and StartView messages carry whole logs, which is why practical systems send only the suffix the receiver lacks, or a state snapshot.

## Where it is used

- [Viewstamped Replication](/viewstamped-replication/), in the original form of Oki and Liskov (1988) and in the revised form of Liskov and Cowling (2012).
- [PBFT](/pbft/) and the protocols built on it, where the view change is the most complex part.
- [Raft](/raft/), [Zab](/zab/) and [Multi-Paxos](/multi-paxos/), where leader election plays the same role.
- [Primary-backup replication](/primary-backup-replication/) systems, where an external service may run the view change, as in [Vertical Paxos](/vertical-paxos/).
- A view change also ends one configuration in some systems, and the next view can have a different set of replicas: see [cluster membership change](/cluster-reconfiguration/).

## References
