---
tag: C0A2V1
kind: definition
slug: byzantine-failure-model
name: Byzantine failure model
aliases:
- arbitrary failure model
- Byzantine fault
- malicious failure model
area: distributed/byzantine-agreement
level: intro
summary: A faulty process may deviate from its algorithm in any way, send conflicting messages to different processes, and act together with the other faulty processes.
prereqs: [crash-failure, synchronous-model]
see_also: [byzantine-broadcast, byzantine-fault-tolerance, oral-messages-model, signed-messages-model, byzantine-resilience-bound, byzantine-quorum-system, consensus-properties, digital-signature]
sources:
  - paper: doi:10.1145/357172.357176
    title: Leslie Lamport, Robert Shostak and Marshall Pease, The Byzantine Generals Problem, ACM Transactions on Programming Languages and Systems 4(3), 1982
    locator: Section 1 (traitors that may do anything, and the generals story that gave the model its name)
  - paper: doi:10.1145/42282.42283
    title: Cynthia Dwork, Nancy Lynch and Larry Stockmeyer, Consensus in the presence of partial synchrony, Journal of the ACM 35(2), 1988
    locator: Section 1 (the fault classes fail-stop, omission, authenticated Byzantine and Byzantine, and their bounds)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 2 (Byzantine failures in the synchronous model) and Chapter 6, Section 6.3 (agreement with Byzantine failures)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 5, Section 5.2 (the Byzantine failure model in synchronous systems)
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luís Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 2 (process abstractions, from crashes and omissions to arbitrary faults)
  - paper: doi:10.1145/3293611.3331629
    title: Ittai Abraham, T.-H. Hubert Chan, Danny Dolev, Kartik Nayak, Rafael Pass, Ling Ren and Elaine Shi, Communication complexity of Byzantine agreement, revisited, PODC 2019
    locator: Section 2 (static, adaptive and strongly adaptive adversaries)
---

In the Byzantine failure model, a faulty process may do anything: send wrong values, send different values to different processes, stay silent, or follow the algorithm for a while and then stop. The faulty processes may also act together, as if one adversary controls them all. It is the most general model of process failure, and an algorithm that works in it works for every other kind of process failure, from bugs and hardware faults to attacks. The name comes from the 1982 paper of Lamport, Shostak and Pease, in which traitor generals of the Byzantine army try to stop the loyal ones from agreeing on a plan.

## Definition

A system has $n$ processes that each run an algorithm, and a parameter $t$, the largest number of faulty processes. A process is **Byzantine** (or **faulty**) in a run if it does not follow the algorithm in that run. A process that follows it to the end is **correct**. In the Byzantine failure model:

1. **Any behavior.** A faulty process may send any messages, with any contents, to any processes, or send nothing. In the [synchronous model](/synchronous-model/), it sends at most one message per link per round, but its contents are free. It may send different messages to different processes in the same round. This is called *equivocation*.
2. **Collusion.** All faulty processes are controlled by one adversary. The adversary knows their states and inputs and can coordinate what they send.
3. **At most $t$ faults.** In each run, at most $t$ processes are faulty. The correctness conditions of a problem, such as agreement and validity, are only required for the correct processes.
4. **Limits on the adversary.** The adversary cannot change, add or drop messages on a link between two correct processes, and a receiver knows which process sent each message. In the [signed messages model](/signed-messages-model/) the adversary also cannot produce a signature of a correct process on a message that the correct process did not sign. In the [oral messages model](/oral-messages-model/) there are no signatures.

**When the faulty processes are chosen.**

- A **static** adversary fixes the set of faulty processes before the run starts.
- An **adaptive** adversary chooses which processes to corrupt during the run, based on what it has seen so far, up to $t$ in total. From then on it controls them.
- A **strongly adaptive** adversary can also corrupt a process in a round after the process has sent its messages for the round, and remove those messages before they are delivered.

**Rushing.** In a round of the synchronous model, a **rushing** adversary sees the messages that correct processes send in the round before it chooses the messages of the faulty processes for the same round. Lower bounds usually allow rushing, and good algorithms should tolerate it.

**The hierarchy of process failures.** Each class below allows all the behaviors of the classes before it:

$$\text{crash} \subset \text{omission} \subset \text{authenticated Byzantine} \subset \text{Byzantine}.$$

A [crashed](/crash-failure/) process follows the algorithm and then stops. An *omission* fault follows the algorithm but may fail to send or to receive some messages. An *authenticated Byzantine* fault may do anything except forge the signatures of correct processes. A *Byzantine* fault has no limit. An algorithm that tolerates $t$ faults of one class tolerates $t$ faults of every smaller class, and a lower bound for a smaller class holds for every larger class.

## Examples and non-examples

- **Example: equivocation.** A faulty commander tells one general "attack" and another "retreat". This is the basic Byzantine behavior, and the reason why simple voting fails. With $n = 3$ and one fault, no algorithm without signatures can defeat it, by the [Byzantine resilience bound](/byzantine-resilience-bound/).
- **Example: a lying relay.** A faulty process reports "the sender told me 0" when the sender said 1. With signatures this lie is impossible, because the relay would have to show the sender's signature on 0.
- **Example: hardware and software faults.** A processor with a stuck bit, a corrupted memory word or a bug that sends a wrong value is Byzantine. The model was first made for such faults in the SIFT aircraft computer.
- **Example: attacks.** A replica taken over by an attacker in a [BFT system](/byzantine-fault-tolerance/), or a malicious validator in a blockchain, is Byzantine. In these settings collusion is a real threat.
- **Example: a crash.** A process that stops is a Byzantine process with a very simple behavior. So the [round lower bound for crashes](/consensus-round-lower-bound/) is also a bound for Byzantine faults.
- **Non-example: a lossy link.** If messages between two correct processes are lost, that is a link failure, not a process failure. The standard Byzantine model assumes reliable links, and models with faulty links need other algorithms.
- **Non-example: unlimited identities.** If an attacker can add as many processes as it wants, the bound of $t$ faults does not hold. This *Sybil attack* is outside the model. Permissionless blockchains limit it with [proof of work](/proof-of-work/) or [proof of stake](/proof-of-stake/) instead of counting processes.
- **Non-example: a process that is slow.** In the [asynchronous model](/asynchronous-model/), a slow correct process is not faulty. It still counts as correct, although others cannot tell it from a silent faulty one.

## Related definitions

- **[Crash failure](/crash-failure/).** The smallest class of the hierarchy. Synchronous crash consensus works for any $t < n$, and Byzantine consensus without signatures needs $n > 3t$.
- **Oral and signed messages.** The [oral messages model](/oral-messages-model/) and the [signed messages model](/signed-messages-model/) are the two standard ways to fix what a Byzantine process can claim about messages from others.
- **[Byzantine broadcast](/byzantine-broadcast/) and consensus.** The basic problems of the model. Their [consensus properties](/consensus-properties/) are restated for correct processes only, and validity splits into [strong validity](/strong-validity/) and [weak validity](/weak-validity/).
- **[Byzantine quorum system](/byzantine-quorum-system/).** Sets of processes that intersect in at least $t + 1$ processes, so in at least one correct process.
- **Bounds that depend on the class.** In the synchronous model, consensus needs $n > t$ for crash faults, $n > 3t$ for Byzantine faults, and $n > 2t$ for authenticated Byzantine faults. In [partial synchrony](/partial-synchrony/), Dwork, Lynch and Stockmeyer show $n > 2t$ for crash faults and $n > 3t$ for both Byzantine classes.

## References
