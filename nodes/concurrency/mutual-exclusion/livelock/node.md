---
tag: 92X6MQ
kind: concept
slug: livelock
name: Livelock
area: concurrency/mutual-exclusion
level: intro
summary: Processes keep taking steps and reacting to each other, but none makes progress. Random backoff breaks the symmetry and ends it with probability 1.
history:
  year: 1976
  people: [Robert M. Metcalfe, David R. Boggs]
  note: The Ethernet of Metcalfe and Boggs (1976) used random backoff after a collision so that stations that collide do not retry in lock step forever.
prereqs: [deadlock]
see_also: [deadlock, starvation, deadlock-freedom, exponential-backoff, binary-exponential-backoff, obstruction-freedom, contention-management, dining-philosophers-problem]
sources:
  - paper: doi:10.1145/360248.360253
    title: Robert M. Metcalfe and David R. Boggs, Ethernet, distributed packet switching for local computer networks, Communications of the ACM 19(7), 1976, pages 395-404
    locator: the retransmission after a collision with a random delay that grows with the number of collisions
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 7, Section 7.4, Exponential Backoff
  - paper: "Maurice Herlihy, Victor Luchangco and Mark Moir, Obstruction-free synchronization, double-ended queues as an example, Proceedings of the 23rd International Conference on Distributed Computing Systems (ICDCS), 2003"
    locator: obstruction freedom, which allows livelock, and the use of a separate contention manager to avoid it
  - paper: "Jeffrey C. Mogul and K. K. Ramakrishnan, Eliminating receive livelock in an interrupt-driven kernel, ACM Transactions on Computer Systems 15(3), 1997"
    locator: receive livelock, where a kernel spends all its time on interrupts for new packets and delivers none
---

A livelock is a run of a concurrent system in which the processes keep taking steps, and keep changing their state in answer to each other, but none of them makes progress. It differs from a [deadlock](/deadlock/), where the processes are blocked and take no useful steps, and from [starvation](/starvation/), where some process makes progress while another does not. A livelock usually comes from symmetric, polite rules that two processes apply at the same time. Randomization breaks the symmetry.

## In plain words

Two people meet in a narrow hall. Each one steps aside to let the other pass. Both step to the same side, so they are face to face again. They both step back to the other side, and again they block each other. Both are busy and both are polite, but neither gets past.

The fix is to break the tie. If each person waits a random short time before the next move, soon one of them moves while the other stands still, and that one gets past. Computers use the same trick when two parts of a program keep giving way to each other.

## The idea

**Definition.** A run is a *livelock* if, from some time on, the processes that are involved take infinitely many steps and none of them reaches its goal (for a lock: no process enters its critical section), although none of them is blocked. The state changes all the time, so a livelock is not a deadlock state. A lock with a livelock run is not [deadlock free](/deadlock-freedom/), because deadlock freedom counts entries, not steps.

**A polite protocol.** Two processes 0 and 1 share the flags $flag[0]$ and $flag[1]$, both false at the start. Process $i$, with $j = 1 - i$, runs:

1. $flag[i] \leftarrow$ true;
2. if $flag[j]$ is false, enter the critical section;
3. else $flag[i] \leftarrow$ false, and go back to step 1.

In its exit section, process $i$ writes $flag[i] \leftarrow$ false.

**Safety.** The protocol gives mutual exclusion. If both processes are in the critical section, look at their last reads at step 2. Each one read the flag of the other as false, after it set its own flag to true. Let $i$ be the one whose write came first. Then the write of $i$ came before the write of $j$, which came before the read of $j$, and $flag[i]$ stayed true from its write until the read, so $j$ read true. This is a contradiction.

**Livelock.** Let the scheduler run the two processes in lock step: one step of process 0, then one step of process 1. Both raise their flags, both read true, both lower their flags, and both start again in the same state. The run is fair, every step is enabled, and no process ever enters. The polite rule that prevents the deadlock of the plain flag protocol (raise, then wait while the other flag is up) has turned it into a livelock.

**The randomized fix.** After it lowers its flag, process $i$ flips a fair coin and waits $c \cdot U$ local steps, where $c \in \{0, 1\}$ is the coin and $U$ is the length of one attempt. The protocol stays safe, because the argument above does not use the waits.

**Proposition (expected time with an oblivious scheduler).** Fix the lock step schedule, with $U = 3$. Let $K$ be the number of collisions (rounds in which both processes retreat) before the first entry. Then $\Pr[K > k] = 2^{-k}$ for $k \ge 0$, so $E[K] = 2$, and the first process to enter takes at most $8K + 2$ steps from its first raise to its entry, so it enters in at most 18 expected steps.

*Proof.* While the two processes have flipped the same coins so far, they are in the same state after each round: both raise, both read the other flag as true, and both retreat. In a round where the coins are equal, both wait the same time and the next round starts in step again. In a round where the coins differ, say $c_i = 0$ and $c_j = 1$, process $i$ raises its flag and reads $flag[j]$ while $j$ still waits with its flag down, so $i$ enters. The coins of a round are independent of the earlier rounds and are equal with probability $1/2$, so $K$ has the geometric distribution on $\{1, 2, \ldots\}$ with success probability $1/2$: $\Pr[K > k] = 2^{-k}$ and $E[K] = \sum_{k \ge 0} \Pr[K > k] = 2$. A collision round costs a process at most 8 steps: raise, read, lower, the retreat, the coin, and at most $U = 3$ waits. The winning attempt costs 2 steps (raise and read). So the winner makes at most $8K + 2$ steps, and by [linearity of expectation](/linearity-of-expectation/) its expected number is at most $8 \cdot 2 + 2 = 18$. $\square$

**The scheduler matters.** The proof needs a schedule that is fixed in advance and does not see the coins. An *adaptive* scheduler that sees the coins can keep the processes in step: when the coins differ, it pauses the fast process, runs the waits of the slow one and its raise, and then lets both read. Then both see the other flag up, and they collide again. So the randomized protocol is free of livelock with probability 1 against an oblivious scheduler, and not against an adaptive one. Real systems are close to the oblivious case, since the hardware timing does not depend on the coin values, but proofs must state the assumption.

**Why backoff grows.** With $m$ processes that collide, a fixed range of two delays fails often: the chance that exactly one process picks the short delay is $m \cdot 2^{-m}$, which goes to 0. [Exponential backoff](/exponential-backoff/) doubles the range after each collision, so the range catches up with the number of competitors. [Binary exponential backoff](/binary-exponential-backoff/) in Ethernet is this scheme.

## Examples

**Test runs.** The test file of this page checks four facts with the explorer of this area. The polite protocol never puts both processes in the critical section, and its state graph has a cycle in which both processes move and nobody enters. A lock step run of 3000 steps has no entry and 748 retreats. The randomized protocol stays safe, and every one of 200 lock step runs ends with both processes in the critical section once. Over 4000 lock step runs, the number of collisions is at least 1, its mean is between 1.9 and 2.1, and the fraction of runs with $K > k$ is within 0.03 of $2^{-k}$ for $k = 1, 2, 3, 4$.

**Dining philosophers.** Each philosopher picks up the left fork, sees that the right fork is taken, puts the left fork down, and tries again. If all of them do it in step, nobody eats. Lehmann and Rabin (1981) gave a randomized solution in which each philosopher picks the first fork by a coin flip. See the [dining philosophers problem](/dining-philosophers-problem/).

**Ethernet.** Stations that send at the same time detect a collision and retry. If they retried after the same delay, they would collide forever. Each station waits a random number of slot times, and the range of the random number doubles after each collision, up to a limit.

**Obstruction-free algorithms.** An [obstruction-free](/obstruction-freedom/) operation finishes if it runs alone, but two operations can keep aborting each other. Herlihy, Luchangco and Moir (2003) separate this risk from the algorithm and hand it to a [contention manager](/contention-management/), which uses backoff or priorities.

**Receive livelock.** A kernel that does all its packet work in interrupt handlers can, under a high packet rate, spend all its time on interrupts for new packets, and never run the code that delivers them. Mogul and Ramakrishnan (1997) avoid this with polling under load.

## Where it is used

- As a failure to rule out in lock and protocol design. [Deadlock freedom](/deadlock-freedom/) rules out livelock inside a lock, because it demands entries.
- In randomized symmetry breaking: backoff in networks, in [spin locks](/spin-lock/) and in transactional memory.
- In the analysis of non-blocking progress: [lock freedom](/lock-freedom/) rules out livelock, and obstruction freedom does not.
- In the design of systems that must stay useful under overload, such as network stacks.

## References
