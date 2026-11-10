---
tag: 46VA12
kind: definition
slug: crash-failure
name: Crash-failure model
aliases:
- crash-stop
- fail-stop
area: distributed/consensus
level: intro
summary: Faulty processes stop and never send further messages.
prereqs: [asynchronous-model]
see_also: [byzantine-failure-model, failure-detector, floodset, flp-impossibility, consensus-properties, synchronous-model, wait-freedom, failure-detection]
sources:
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 2 (stopping failures in the synchronous model, where a process may stop in the middle of sending its messages of a round), Chapter 6 (agreement with stopping failures) and Chapter 21 (stopping failures in asynchronous networks)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 5, Section 5.1 (the crash failure model in synchronous systems)
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luis Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 2 (process failures, crash, omission, crash with recovery and arbitrary faults)
  - paper: doi:10.1145/357369.357371
    title: Richard D. Schlichting and Fred B. Schneider, Fail-stop processors, an approach to designing fault-tolerant computing systems, ACM Transactions on Computer Systems 1(3), 1983
    locator: pages 222 to 238 (fail-stop processors, whose failures the other processors can detect)
---

In the crash-failure model, a faulty process behaves correctly until some moment, and then stops for ever: it takes no more steps and sends no more messages. It is the mildest failure model for processes, and the standard one for [consensus](/consensus-problem/), [Paxos](/paxos/) and [Raft](/raft/). A crash can still fall in the middle of a broadcast, so that some processes get a message and others do not, and in the [asynchronous model](/asynchronous-model/) nobody can tell a crashed process from a slow one.

## Definition

There are $n$ processes. A *failure pattern* assigns to each process $p$ either no crash time, or a crash time $t_p$. A process with no crash time is *correct*. A process with a crash time is *faulty*, and

- before $t_p$, $p$ follows its algorithm exactly;
- after $t_p$, $p$ takes no step and sends no message;
- messages that $p$ sent before $t_p$ are delivered as usual, if the links are reliable.

The model allows at most $f$ faulty processes in an execution, for a known $f$. An algorithm that is correct with up to $f$ crashes is *$f$-resilient*. The case $f = n - 1$ is called *wait-free*, see [wait-freedom](/wait-freedom/).

**A crash in the middle of a broadcast.** A broadcast is a sequence of single sends. A process that crashes during a broadcast has sent the message to some of the processes and not to the others, and the adversary chooses which. In the round model of the [synchronous model](/synchronous-model/), Lynch states this directly: in the round of its crash, a process sends its messages of that round to an arbitrary subset of its neighbours.

**Why a crash cannot be detected in the asynchronous model.** Let $q$ crash at time 0 in execution $\alpha$. Let $\beta$ be an execution with the same inputs in which $q$ is correct, but every step of $q$ and every message from $q$ is delayed until after time $T$. Up to $T$, every other process receives the same messages in $\alpha$ and in $\beta$, so it is in the same state. The asynchronous model allows $\beta$ for every $T$. So no process can ever know that $q$ has crashed, and a rule such as "wait for $q$" can block for ever, while a rule such as "decide without $q$" must also be safe when $q$ is only slow. This is the source of the [FLP impossibility](/flp-impossibility/). In the synchronous model the two executions differ after one round, because a correct $q$ must send in every round.

**Names.** *Crash-stop* stresses that a crashed process never recovers. *Fail-stop* is used in two ways: often as a synonym of crash-stop, and in Schlichting and Schneider (1983) for a process whose crash the others are able to detect, which is a stronger model. The two should not be confused when results are compared.

## Examples and non-examples

- **Example: a broadcast cut short.** With $n = 4$, process $p_1$ sends $v$ to $p_2$, then to $p_3$, and crashes before it sends to $p_4$. Now $p_2$ and $p_3$ know $v$ and $p_4$ does not. This is why [FloodSet](/floodset/) needs $f + 1$ rounds: each crash can hide a value from some processes for one more round. It is also why a reliable broadcast relays every new message before it delivers it.
- **Example: a process that halts after a power loss.** A server loses power and never comes back, or comes back with a new identity and empty state. As far as the algorithm is concerned, the old process crashed.
- **Non-example: a long pause.** A process that pauses for ten seconds for garbage collection and then goes on has not crashed. In the asynchronous model this is just a slow process. Treating it as crashed, and acting as if it will never send again, is a common source of bugs such as [split brain](/split-brain/).
- **Non-example: a restart with stable storage.** A process that crashes and later recovers its state from disk follows the *crash-recovery* model, not crash-stop. Algorithms for it must write some state to stable storage before they send messages that depend on it.
- **Non-example: a lost message.** A process that keeps running but fails to send some of its messages has an *omission* failure. A crash is the special case in which it omits all messages from some time on.
- **Non-example: a wrong value.** A process that sends a value its algorithm would not send, because of a bug or an attack, has a [Byzantine failure](/byzantine-failure-model/).

## Related definitions

- **Failure models by strength.** Crash, then send omission, then general omission (send and receive), then Byzantine with signatures, then Byzantine. Each allows all the behaviours of the one before it, so an algorithm for a stronger model works in a weaker one, and impossibility results carry over in the other direction.
- **Crash-recovery.** Processes may crash and recover any number of times. A process is *good* if it eventually stays up for ever, and *bad* otherwise. Aguilera, Chen and Toueg (2000) show that consensus without stable storage needs more processes that never crash than bad processes; with stable storage, a majority of good processes is enough.
- **Correct and faulty.** These are properties of a whole execution, not of a moment: a process that will crash later is faulty even before its crash.
- **Uniform agreement.** Agreement that also binds processes that decide and then crash, see [consensus properties](/consensus-properties/). In the crash model, many algorithms give it at no extra cost.
- **[Failure detector](/failure-detector/).** An oracle that gives the processes hints about the failure pattern. It adds to the asynchronous crash model just the information that the indistinguishability argument above denies.
- **Resilience bounds.** With crash failures, consensus is solvable for any $f < n$ in the synchronous model, needs $n > 2f$ in the [partial synchrony](/partial-synchrony/) model, and is impossible for $f \ge 1$ in the asynchronous model without randomization or a detector.

## References
