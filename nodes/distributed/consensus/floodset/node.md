---
tag: MBNRW2
kind: algorithm
slug: floodset
name: FloodSet algorithm
area: distributed/consensus
level: advanced
summary: Synchronous crash-tolerant consensus where processes flood known values for f+1 rounds.
solves: [consensus-problem]
model: synchronous-model
complexity:
  vars: {n: the number of processes, f: the largest number of crashes}
  time: {worst: Θ(f), best: Θ(f)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
prereqs: [consensus-problem, synchronous-model, crash-failure]
see_also: [consensus-round-lower-bound, consensus-properties, flooding, interactive-consistency, dolev-strong-algorithm, oral-messages-algorithm, flp-impossibility, chandra-toueg-consensus]
sources:
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 6, Section 6.1 (the agreement problem for stopping failures) and Section 6.2 (FloodSet, its correctness by the clean round argument, and the variant OptFloodSet)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 5, Section 5.1 (consensus in synchronous systems with crash failures, the f + 1 round algorithm that decides the minimum)
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luís Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 5, Section 5.1 (Flooding Consensus, a round-based version that uses a perfect failure detector)
  - paper: doi:10.1016/0020-0190(82)90033-3
    title: Michael J. Fischer and Nancy A. Lynch, A lower bound for the time to assure interactive consistency, Information Processing Letters 14(4), 1982
    locator: pages 183 to 186 (f + 1 rounds are necessary)
  - paper: doi:10.1137/0212045
    title: Danny Dolev and H. Raymond Strong, Authenticated algorithms for Byzantine agreement, SIAM Journal on Computing 12(4), 1983
    locator: pages 656 to 666 (the f + 1 round lower bound and the authenticated algorithm)
---

FloodSet is the basic [consensus](/consensus-problem/) algorithm for the [synchronous model](/synchronous-model/) with [crash failures](/crash-failure/). Each process keeps the set of input values it has heard of, and sends the whole set to every other process in each of $f + 1$ rounds, where $f$ is the largest number of crashes. After the last round it decides by a fixed rule on the set. It tolerates any $f < n$ crashes, and its $f + 1$ rounds are optimal by the [round lower bound](/consensus-round-lower-bound/) when $f \le n - 2$.

## In plain words

A group of computers must agree on one value. Each starts with its own value. Some computers can stop at any moment, even halfway through sending a message to the others. Time moves in rounds, and a message sent in a round arrives in the same round.

Each computer keeps a set of all the values it has heard of. In each round, it sends its set to everyone and adds the sets it gets. After enough rounds, it picks a value from its set, for example the smallest.

Why does this work? A value can travel only through computers that crash, and each crash can pass it on to just a few others. If there are more rounds than crashes, then in some round nobody crashes. In that round everyone gets everything, and from then on all the sets are the same.

## The problem

There are $n$ processes $p_1, \ldots, p_n$ on a complete network of reliable links. Process $p_i$ has an input $v_i$ from a value set $V$. At most $f$ processes can crash, where $0 \le f < n$. The model is the [synchronous model](/synchronous-model/): in each round, each process that has not crashed sends its messages, then receives all messages sent to it in the round, then changes its state. A process that crashes in round $r$ sends its round $r$ message to any subset of the others, chosen by the adversary, and does nothing after that.

The algorithm must give the properties of the [consensus problem](/consensus-problem/), in the form that Lynch uses:

- **Agreement.** No two processes decide different values.
- **Validity.** If all inputs are equal to $v$, then $v$ is the only possible decision.
- **Termination.** Each process that does not crash decides.

Agreement here covers every process that decides, also one that crashes later. It is [uniform agreement](/consensus-properties/). With the minimum rule below, FloodSet also gives the stronger validity that the decision is one of the inputs.

## The algorithm

The code of process $p_i$ is below. The default $v_0 \in V$ is fixed and known to all processes.

```pseudo id=main
FLOODSET(i, v_i)                            ▷ the code of p_i; f is the largest number of crashes
L1  W ← {v_i}
L2  for r ← 1 to f + 1 do                   ▷ lock-step rounds
L3      send W to each other process
L4      for each set X received in round r do
L5          W ← W ∪ X
L6  if |W| = 1 then decide the element of W
L7  else decide v_0                         ▷ the variant decides min W
```

Line L3 sends the whole set in each round. Lines L4 and L5 run after all the messages of the round have arrived, which the synchronous model guarantees. The decision of lines L6 and L7 is a function of $W$ only. Any function works for agreement, because the proof shows that all deciding processes end with the same set. The function must map $\{v\}$ to $v$ for validity. Lynch uses the rule of lines L6 and L7. Attiya and Welch decide $\min W$, which also makes the decision one of the inputs.

## Example

Take $n = 4$ and $f = 2$, so there are 3 rounds. The inputs are $v_1 = 3$, $v_2 = 1$, $v_3 = 4$, $v_4 = 5$, and the rule is $\min W$. The adversary crashes $p_2$ in round 1, and its message reaches only $p_3$. It crashes $p_3$ in round 2, and its message reaches only $p_4$. The value 1 is known only to $p_2$ at the start, so it can only travel along this chain of crashing processes.

| after round | $W_1$ | $W_2$ | $W_3$ | $W_4$ | crash in the round |
|---|---|---|---|---|---|
| 0 | {3} | {1} | {4} | {5} | |
| 1 | {3, 4, 5} | crashed | {1, 3, 4, 5} | {3, 4, 5} | $p_2$, heard by $p_3$ only |
| 2 | {3, 4, 5} | crashed | crashed | {1, 3, 4, 5} | $p_3$, heard by $p_4$ only |
| 3 | {1, 3, 4, 5} | crashed | crashed | {1, 3, 4, 5} | none |

Round 3 is a clean round: no process crashes in it, so $p_4$ gives the value 1 to $p_1$. Both $p_1$ and $p_4$ decide 1. If the algorithm stopped after 2 rounds, $p_1$ would decide 3 and $p_4$ would decide 1, so agreement would break. The run sends 10 messages in round 1, 7 in round 2 and 6 in round 3, 23 in total.

## Correctness

The proof rests on two facts about the sets $W$. A *clean round* is a round in which no process crashes.

- After a clean round, all processes that have not crashed have the same set $W$. Each of them gets the set of each process that was alive at the start of the round, so each ends with the union of these sets.
- Once all live processes have the same set, no set changes again. Each set that arrives later is that same set.

At most $f$ processes crash, and each crashes in one round, so at least one of the $f + 1$ rounds is clean. So all processes that decide have the same $W$, and they decide the same value. $W$ only ever holds inputs, so if all inputs are $v$, then $W = \{v\}$ and the decision is $v$. Each process that does not crash finishes the $f + 1$ rounds and decides. The full proof is below.

## Complexity

The costs are in the synchronous model, counted in rounds and messages.

- **Rounds.** Exactly $f + 1$ rounds, in every run. This is $\Theta(f)$ in the best and the worst case. FloodSet never stops early, even when no process crashes.
- **Messages.** Each live process sends $n - 1$ messages in each round, so at most $n(n-1)(f+1)$ messages in total. A run with no crash sends exactly this number.
- **Message size.** A message is a set of at most $\min(n, |V|)$ values, so $O(n \log |V|)$ bits when $|V| \ge 2$, and $O(n^3 f \log |V|)$ bits in total.
- **Local space.** The set $W$ has at most $n$ values, so the extra space is $O(n)$ values.

The [round lower bound](/consensus-round-lower-bound/) of Fischer and Lynch, and of Dolev and Strong, says that each consensus algorithm in this model needs $f + 1$ rounds in some run when $f \le n - 2$. So FloodSet is optimal in its worst case. When $f = n - 1$, $f$ rounds are enough for FloodSet: a run with $f$ crashes in the first $f$ rounds leaves at most one process, which cannot disagree with anyone.

## Properties

- **Deterministic.** No coins and no timeouts. The only nondeterminism is the adversary's choice of crashes.
- **Resilience.** It tolerates any $f < n$ crashes. No majority of correct processes is needed, unlike the asynchronous algorithms with failure detectors.
- **Uniform.** Agreement holds also for a process that decides and then crashes, because all processes decide at the same time.
- **Not early stopping.** It always takes $f + 1$ rounds, also when no crash happens.
- **Only for crashes.** A Byzantine process can send different sets to different processes, and then the clean round argument fails.

## Variants and improvements

- **Minimum rule.** Decide $\min W$, as Attiya and Welch do. This gives the strong form of validity: the decision is the input of some process.
- **OptFloodSet.** Lynch gives a variant in which each process sends its own value and, later, at most one other value. The rule of lines L6 and L7 only needs to know whether $|W| = 1$, so two values are enough. Each process then broadcasts at most twice, so there are at most $2n(n-1)$ messages, each with one value.
- **Send only new values.** In the version of Attiya and Welch, each process sends each value at most once to each other process. At most $n$ different values exist, so at most $n^2(n-1)$ values cross the network in total, in place of up to $n^2(n-1)(f+1)$.
- **Exponential information gathering.** The EIG algorithms of Lynch, Section 6.2, also tolerate crashes in $f + 1$ rounds, and their Byzantine form is the basis of the [oral messages algorithm](/oral-messages-algorithm/).

## When to use it

Use FloodSet to teach or to reason about consensus in the synchronous crash model, where it is the simplest correct algorithm. In a real system the synchronous model only holds when the network and the clocks give hard bounds, for example in some embedded and real-time systems. Most systems are closer to the [asynchronous model](/asynchronous-model/) or to [partial synchrony](/partial-synchrony/). There, use an algorithm with a [failure detector](/failure-detector/) such as [Chandra-Toueg](/chandra-toueg-consensus/), or [Paxos](/paxos/) or [Raft](/raft/). For Byzantine faults use the [Dolev-Strong algorithm](/dolev-strong-algorithm/) with signatures or an oral messages algorithm with $n > 3f$.

## Pitfalls

- **Only $f$ rounds.** With $f$ in place of $f + 1$ in line L2, a chain of crashes can carry a value to a single process in the last round. The example above shows this for $f = 2$. For $n = 3$ and $f = 1$, 6 of the runs with one round and binary inputs break agreement.
- **Deciding as soon as $W$ looks stable.** A process cannot stop early because its own $W$ did not change in a round. Another process may still hold a value that a crashing process passed to it alone.
- **Counting a partial broadcast as a full one.** A process that crashes in round $r$ may reach any subset of the others in that round. A proof or a simulator that crashes a process only between rounds misses the hard runs.
- **Using it without lock-step rounds.** Line L4 needs all round $r$ messages from live processes. In an asynchronous network a slow message looks like a crash, and the algorithm breaks.

## Implementations

## History

Fischer and Lynch proved in 1982 that $f + 1$ rounds are necessary for interactive consistency with $f$ faults, and Dolev and Strong showed the same for authenticated Byzantine agreement in 1983. Lynch's textbook of 1996 names the simple flooding algorithm FloodSet and proves it with the clean round argument, in Section 6.2. Attiya and Welch give the same algorithm with the minimum rule.

## References
