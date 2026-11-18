---
title: Clock-SI gives snapshot isolation for any clock skew
proves: [correctness, messages]
status: full
---

We use the line numbers of the pseudocode on the page. The model is the model of the page and of the toy code. Each partition has a clock that never goes back, and two readings of the clock at one partition differ; readings at different partitions differ in the partition number (the paper breaks ties by partition id). Nothing is assumed about the skew between clocks. Each step of a partition (serving a read, a certification with its prepare or local commit, an install, an abort) is atomic. Messages to a partition are not lost. A coordinator may crash, but it comes back and reads its log.

For a transaction $T$, $s(T)$ is its snapshot timestamp (line L1). For a committed writer $W$, $c(W)$ is its commit timestamp: the clock reading at line L6 for a local commit, and the largest prepare timestamp at line L9 for a distributed commit. A *version* of $k$ is a pair (timestamp, value) that line L10 installs. While $W$ is certified at a partition and not yet installed or aborted there, $W$ is *pending* on its keys at that partition with a timestamp $p$: its prepare timestamp, or its commit timestamp for a local commit. In both cases $p \le c(W)$ if $W$ commits.

**Lemma 1 (versions).** Line L10 installs a version of $k$ only for a committed writer $W$ of $k$, with timestamp $c(W)$. A pending entry of $W$ is removed only by its install (if $W$ commits) or by an abort (if $W$ aborts).

*Proof.* Line L10 runs for a local commit after the commit record is on disk, and for a distributed commit when the commit message arrives, which the coordinator sends only after it has logged the decision at line L9. The rest is read from the code. $\square$

**Lemma 2 (clocks after a wait).** If partition $q$ serves a request of $T$ at time $\tau$, then every clock reading at $q$ after $\tau$ is larger than $s(T)$.

*Proof.* If $q$ is not the origin of $T$, line L2 serves the request only when the clock of $q$ is above $s(T)$, and later readings are larger still. If $q$ is the origin, $s(T)$ is a reading at $q$ minus $\Delta \ge 0$, taken before $\tau$, and later readings are larger. $\square$

**Lemma 3 (commit after snapshot).** Every committed writer $W$ has $c(W) > s(W)$.

*Proof.* Each prepare timestamp and each local commit timestamp is a reading at a partition that has served a request of $W$ (line L2 applies to prepare and to a remote local commit), so by Lemma 2 it is above $s(W)$. The commit timestamp is one of these readings or their maximum. $\square$

**Theorem 1 (consistent snapshot).** When partition $q$ serves a read of $k$ by $T$ at line L4, it returns the value written by the committed writer $W$ of $k$ with the largest $c(W) < s(T)$ (the initial value if there is none).

*Proof.* Let $W$ be any committed writer of $k$ with $c(W) < s(T)$, and let $\tau$ be the time of the read. If $W$ was certified at $q$ before $\tau$, then at $\tau$ it is installed or still pending with timestamp $p \le c(W) < s(T)$. A pending entry like this makes line L3 wait, so at $\tau$ it is installed. If $W$ was certified at $q$ after $\tau$, its timestamp at $q$ is a reading after $\tau$, so it is above $s(T)$ by Lemma 2. Then $c(W) \ge p > s(T)$, which is false. So every committed writer of $k$ with commit timestamp below $s(T)$ has its version on $q$ at time $\tau$, and by Lemma 1 no other transaction has a version there. Line L4 takes the version with the largest timestamp below $s(T)$, which is the version of the writer with the largest $c(W) < s(T)$. $\blacksquare$

The proof uses line L3 only for writers that were already certified and line L2 only for writers that come later. These are the two delays of the paper: a pending commit and a clock that is behind.

**Theorem 2 (first committer wins).** If committed writers $A$ and $B$ both write $k$, then $c(A) < s(B)$ or $c(B) < s(A)$.

*Proof.* Both are certified at the partition $q$ of $k$ (line L8), in atomic steps. Say $A$ is certified first. When $B$ is certified, $A$ is pending at $q$ or installed (Lemma 1, since $A$ commits). If $A$ is pending, line L8 rejects $B$. So $A$ is installed with timestamp $c(A)$, and line L8 accepts $B$ only if $c(A) < s(B)$. $\blacksquare$

**Theorem 3 (snapshot isolation).** The commit timestamps order the committed writers in a total order. Each transaction reads the state made by the writers with commit timestamps below its snapshot timestamp (Theorem 1), each writer commits after its snapshot (Lemma 3), and two committed writers of one item do not overlap (Theorem 2). These are the three rules of snapshot isolation in Section II-B of the paper. The proofs never use a bound on the clock skew, so the skew changes only how long the reads wait. $\blacksquare$

**All or nothing.** A distributed writer is committed when its coordinator logs the decision. By Lemma 1 no version is installed before that. If the coordinator crashes before it logs a decision, it aborts when it comes back, and sends the abort to every participant. If it crashes after it logged the commit, it sends the commit messages when it comes back. Messages to partitions are not lost, so in the end every participant installs the writes or drops them, and no pending entry is left.

**Progress.** A read waits at line L2 until a clock moves past a value, which happens in finite time, or at line L3 until a pending writer is decided. A certification never waits, so a coordinator gets all its votes and decides, unless it is down. A prepared participant whose coordinator is down waits until the coordinator comes back, and so do the reads that need its keys; this is the blocking of [two-phase commit](/two-phase-commit/), and Clock-SI does not remove it. Waits never form a cycle, because nothing that a read waits for waits for a read.

**A counterexample for the smallest prepare timestamp.** If line L9 took the smallest prepare timestamp, the argument of Theorem 1 would fail. Let $W$ prepare $x$ on $P_1$ at timestamp 10 and $y$ on $P_2$ at timestamp 30, and commit with timestamp 10. A reader with snapshot 20 reads $y$ on $P_2$: the pending entry there has timestamp $30 > 20$, so the read does not wait and returns the old $y$. It reads $x$ on $P_1$ after the install and gets the new $x$, since $10 < 20$. The snapshot has half of $W$. The tests find such runs when the maximum is replaced by the minimum.

**Theorem 4 (messages).** A transaction that reads $r$ items on partitions other than its origin sends $2r$ messages for the reads. A writer that writes on one partition other than its origin sends 2 more messages, and a writer that writes on $p$ partitions sends 3 messages for each participant other than its origin. No message goes to a timestamp server.

*Proof.* Each remote read is one request and one reply. A local commit at another partition is one request and one reply. Two-phase commit sends a prepare, a vote and a commit message to each participant; messages to the origin itself are not network messages. The timestamps come from line L1 and from the clocks of the participants. $\blacksquare$
