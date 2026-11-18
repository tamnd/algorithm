---
title: Barrier snapshots record a consistent global state, and recovery from them is a run of the job
proves: [correctness, termination]
status: full
---

We use the line numbers of the pseudocode on the page. The job is a directed graph of tasks with FIFO channels that lose no message. Sources read records from replayable inputs at an offset. Every other task applies a deterministic operator to each record that it takes, which changes its state and sends records on its outputs. Barriers change no state. The back edges are the channels that close a cycle in a depth-first search from the sources; all other channels are *regular*. The regular channels form an acyclic graph, because every cycle of a graph contains a back edge of any depth-first search.

Fix one snapshot $n$. The *cut point* of a source is its step L10. The cut point of any other task $t$ is its step L4. The *pre-cut events* of a task are the records that it took and sent before its cut point.

**Lemma 1 (order of cut points).** If $(u, t)$ is a regular channel, the cut point of $t$ is after the cut point of $u$. If $(u, t)$ is a back edge, the cut point of $u$ is after the cut point of $t$.

*Proof.* Barrier $n$ is sent on $(u, t)$ only at the cut point of $u$ (lines L3 and L10), and $t$ passes L2 only after it has taken barrier $n$ from every regular input. This gives the first claim. For a back edge $(u, t)$, the search reached $u$ from $t$ along a path of tree edges, which are regular. By the first claim, the cut points increase along that path. $\square$

**Lemma 2 (no orphan records).** Every record that a task takes before its cut point was sent before the cut point of its sender.

*Proof.* Let $t$ take $x$ from channel $c = (u, t)$ before its cut point. If $c$ is regular, $t$ blocks $c$ when it takes barrier $n$ from it (line L1) and unblocks it only at line L5, after its cut point. So $x$ came before the barrier on $c$, and, the channel being FIFO, $u$ sent $x$ before it sent the barrier, which is at its cut point. If $c$ is a back edge, $u$ sent $x$ before $t$ took it, which is before the cut point of $t$, which is before the cut point of $u$ by Lemma 1. $\square$

So the pre-cut events form a consistent cut: no record is received in the cut and sent outside it.

**Lemma 3 (channel states).** The records sent in the cut and not received in it are none on a regular channel, and, on a back edge $c$ into $t$, exactly the records that $t$ logs from $c$ at line L8.

*Proof.* On a regular channel $(u, t)$, all records sent before the cut point of $u$ come before barrier $n$, and $t$ takes the barrier before its cut point, so it takes all of them before its cut point. On a back edge $c = (u, t)$, the records sent before the cut point of $u$ are those before barrier $n$ on $c$. The task $t$ logs the records that it takes from $c$ after its cut point (line L4 starts the log) and stops when it takes the barrier from $c$ (lines L6 and L7). Since $c$ is FIFO and never blocked, these are exactly the records before the barrier that $t$ takes after its cut point. $\square$

**Theorem 1 (consistency).** The snapshot, made of the copied states, the source offsets and the logs, is a global state of the job that some run of the job, without barriers, reaches from the start.

*Proof.* Order all pre-cut events by the real order in which they happened. This order lists each send of a record before its receipt, and on each channel the receipts are in the order of the sends, because the real run did so. Removing the post-cut events keeps these properties, since by Lemma 2 no pre-cut receipt depends on a post-cut send, and removing the barrier steps changes no state. Each task is deterministic, so in this run every task ends in the state that it had at its cut point, which is the copy of line L4, and every source has read its stored offset. The channel contents are given by Lemma 3. $\blacksquare$

**Theorem 2 (recovery).** Restore the copied states, reset each source to its offset, leave the regular channels empty, and put each log at the front of its back edge. Every run from this state is the continuation of a run of the job from the start on the same inputs. So each input record changes the state of each task in the same way as in some run without failure, once.

*Proof.* By Theorem 1, the restored state is the state after a run prefix $P$ of the job. The records of $P$ are exactly the input records before the offsets, together with the records that they cause. The sources continue from their offsets, so each later input record is read once, after $P$. A continuation from the restored state is therefore a continuation of $P$. $\blacksquare$

For a job whose final states do not depend on the order in which the scheduler runs the tasks, such as the jobs in the tests, the state after recovery and a run to the end is the state of the run without failure.

**Termination.** Assume a fair scheduler, which takes from every unblocked nonempty channel eventually. We show that every task reachable from the sources stores its part of snapshot $n$. Order the tasks topologically along the regular channels, which is possible because they form an acyclic graph. Sources pass L10 when they take the trigger. Suppose every regular predecessor of $t$ has passed its cut point. Then barrier $n$ is on every regular input of $t$. An input of $t$ is blocked only after the barrier has been taken from it, so the barriers on the others are taken, and $t$ passes L2 to L5. By induction, every task passes its cut point, and so it sends barrier $n$ on every output, back edges included. No back edge is ever blocked, so every task takes barrier $n$ from each of its back edges, line L6 holds, and line L7 stores its part. A blocked channel is unblocked at L5, so no record waits forever.

Without alignment the proof of Lemma 2 fails: a task that copies its state at the first barrier and keeps taking records from an input whose barrier has not yet come takes records that are in neither the copy nor the replay, and a task that copies at the last barrier without blocking holds records in its copy that the replay sends again. The test of the page example shows the first case.
