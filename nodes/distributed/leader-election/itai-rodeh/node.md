---
tag: Y6D4ZP
kind: algorithm
slug: itai-rodeh
name: Itai-Rodeh algorithm
aliases:
- Itai-Rodeh randomized ring election
- Itai-Rodeh leader election
area: distributed/leader-election
level: advanced
summary: Randomized election on an anonymous ring of known size n. Processes draw random ids from {1..n} and repeat the round when the largest is not unique. Las Vegas, with O(n log n) expected messages.
solves: [anonymous-leader-election]
model: asynchronous-model
complexity:
  vars: {n: the number of processes}
  time: {average: O(n)}
  messages: {average: O(n log n)}
  space: {extra: O(log n)}
properties: {deterministic: false, recursive: false}
history:
  year: 1981
  people: [Alon Itai, Michael Rodeh]
  note: Showed that coin flips break the symmetry of anonymous rings when n is known, and that with n unknown no always-correct algorithm can terminate.
prereqs: [anonymous-network, anonymous-ring-impossibility, chang-roberts, las-vegas-algorithm]
see_also: [anonymous-leader-election, chang-roberts, dolev-klawe-rodeh, ring-leader-election, las-vegas-algorithm, fair-coin-flipping, ring-network, message-complexity]
sources:
  - paper: doi:10.1109/SFCS.1981.41
    title: Alon Itai and Michael Rodeh, Symmetry breaking in distributive networks, Proceedings of the 22nd IEEE Symposium on Foundations of Computer Science, 1981
    locator: pages 150 to 158 (the first version of the randomized election algorithms)
  - paper: doi:10.1016/0890-5401(90)90004-2
    title: Alon Itai and Michael Rodeh, Symmetry breaking in distributed networks, Information and Computation 88(1), 1990
    locator: pages 60 to 87 (Section 3, election on asynchronous rings with O(n log n) expected bits; Section 4, Theorem 4.1, no processor terminating algorithm is correct for both N and 2N)
  - paper: doi:10.1016/j.entcs.2005.04.004
    title: Wan Fokkink and Jun Pang, Simplifying Itai-Rodeh leader election for anonymous rings, Electronic Notes in Theoretical Computer Science 128(6), 2005
    locator: pages 53 to 68 (the form with random identifiers, round numbers, hop counters and a dirty bit, on rings with FIFO channels)
---

The Itai-Rodeh algorithm elects a leader on an [anonymous](/anonymous-network/) unidirectional [ring](/ring-network/) whose size $n$ is known to all processes. Since identical processes cannot break symmetry by a deterministic rule, each process draws a random identifier from $\{1, \ldots, n\}$, and the processes run [Chang-Roberts](/chang-roberts/) on these values. A hop counter tells a process when its own message has come back, and a bit records whether the message met another process with the same value. If the largest value was not unique, the processes that hold it draw again in a new round. The algorithm is a [Las Vegas algorithm](/las-vegas-algorithm/): it is always correct, it ends with probability 1, and the expected number of messages is $O(n \log n)$.

## In plain words

People sit in a circle and look exactly alike. They all know how many people are in the circle. Notes go only to the right.

Each person rolls a die with as many sides as there are people and passes the result on. A note that meets a bigger number is thrown away, and a person who sees a bigger number than their own drops out. Each note carries a step counter, so when a note has made a full circle, its writer knows it is their own.

If a note meets an equal number on the way, it gets a mark. A note that comes back without a mark means its writer has the only biggest number, and that person is the leader. A note that comes back marked means there was a tie, so the people still in roll again.

## The problem

The ring has $n \ge 1$ identical processes and is unidirectional: $p_i$ sends to $p_{i+1}$, indices modulo $n$. The model is [asynchronous](/asynchronous-model/), with reliable FIFO channels. Every process knows $n$ and can draw random numbers that are independent of those of the other processes. All processes start. The goal is that, with probability 1, exactly one process becomes the leader, and in every run no two processes become leaders. This is [leader election in anonymous networks](/anonymous-leader-election/) in its Las Vegas form.

## The algorithm

Each process is *active* or *passive*. An active process holds a round number $r$ and a value $v$. A message $\langle i, r, h, b \rangle$ holds a value, a round, a hop count and a bit; $b = \text{true}$ means *dirty*.

```pseudo id=main
ITAI-RODEH(n)                         ▷ the same code at every process
L1  active ← true, r ← 0, NEW-ROUND
L2  NEW-ROUND: r ← r + 1; v ← a uniform random value in {1, ..., n}; send ⟨v, r, 1, false⟩
L3  on receiving ⟨i, s, h, b⟩: if not active then send ⟨i, s, h + 1, b⟩
L4  else if (s, i) > (r, v) then active ← false; send ⟨i, s, h + 1, b⟩
L5  else if (s, i) < (r, v) then drop the message
L6  else if h < n then send ⟨i, s, h + 1, true⟩       ▷ same round and value: mark it dirty
L7  else if b = false then status ← leader             ▷ own message, no tie seen
L8  else NEW-ROUND                                     ▷ own message, there was a tie
```

The pairs $(s, i)$ and $(r, v)$ compare round first and value second. A message from a later round therefore always wins, so a process that is still in an old round drops out. A message whose round and value equal those of the receiver has either come back to its sender, when $h = n$, or met another process with the same draw, when $h < n$; the hop count tells the two cases apart. This is where knowledge of $n$ is used.

To make every process learn that the election is over, the leader sends one more message round the ring, at a cost of $n$ messages.

## Example

Take $n = 4$. In round 1 the processes $p_0, \ldots, p_3$ draw $3, 1, 3, 2$. Suppose every message takes one time unit.

| time | events |
|---|---|
| 1 | $p_1$ gets $3$ from $p_0$ and becomes passive. $p_2$ drops $1$. $p_3$ gets $3$ from $p_2$ and becomes passive. $p_0$ drops $2$. |
| 2 | $p_2$ gets $p_0$'s $3$ and marks it dirty; $p_0$ gets $p_2$'s $3$ and marks it dirty. |
| 4 | Both $3$ messages come back dirty with $h = 4$. $p_0$ and $p_2$ start round 2 and draw $2$ and $4$. |
| 6 | $p_2$ drops $\langle 2, 2 \rangle$. $p_0$ gets $\langle 4, 2 \rangle$ and becomes passive. |
| 8 | $p_2$ gets its own message back, clean, and becomes the leader. |

Round 1 sends $4 + 1 + 4 + 1 = 10$ messages and round 2 sends $2 + 4 = 6$, so $16$ in all. With another schedule the count can change. For example, if $p_0$ gets its own message back before $p_2$'s message reaches it, $p_0$ is in round 2 and drops $p_2$'s message, so $p_2$ never starts round 2.

## Correctness

- **At most one leader.** Suppose $p$ becomes the leader in round $r$ with value $v$. Its message passed every other process. A process that was active in round $r$ with a larger value would have dropped it, and one with the same value would have marked it dirty, so every other process that was active in round $r$ had a smaller value or an older round and became passive. No process can be in a later round: a process enters round $r + 1$ only when its own round $r$ message comes back dirty, which needs a tie at the largest value of round $r$, and then $p$'s message would be dirty too. A passive process never becomes active again. So no second leader can appear.
- **Progress.** In every round at least one active process gets its own message back: the message of a process with the largest value of the round is never dropped. So each round either elects a leader or starts a new round with at least one process.
- **The round ends the election with probability at least $(1 - 1/n)^n$.** If the largest value of a round is held by one process, that process becomes the leader in that round. For $k \ge 2$ independent uniform values in $\{1, \ldots, n\}$ the largest one is unique with probability at least $(1 - 1/n)^k \ge (1 - 1/n)^n \ge 1/4$.

So the number of rounds is at most a geometric random variable, and the algorithm ends with probability 1. The [proof of correctness](proofs/correctness/) gives the details.

## Complexity

**Rounds.** The expected number of rounds is at most $(1 - 1/n)^{-n} \le e \cdot \frac{n}{n-1}$, which is at most 4 and tends to $e$. In the tests the mean is about 1.45 for $n = 64$.

**Messages.** Fix a round with $k$ active processes. The round's message of an active process crosses a link only if no active process between them on the ring has a larger value. For independent uniform values, the chance that a value is at least the $j$ values before it is at most $1/(j + 1) + 1/n$, so each link carries at most $H_k + 1$ messages of the round on average, where $H_k$ is the $k$-th harmonic number. With the bound on the number of rounds:

$$\mathbb{E}[M] \le \left(1 - \tfrac{1}{n}\right)^{-n} n \,(H_n + 1) = O(n \log n).$$

Fokkink and Pang also give $O(n \log n)$ expected messages for this form. Over 1000 seeded runs, the tests measure means of about $18.5$ messages for $n = 5$, $74$ for $n = 16$ and $385$ for $n = 64$, which is about $1.27 \, n H_n$ for $n = 64$. There is no worst case bound: with probability $0$ the ties go on for ever.

**Time.** If each message takes at most one time unit, each round ends within $n$ time units after its last process starts it, so the expected time is $O(n)$.

**Space and message size.** A process stores its value, its round and two flags. A message holds a value and a hop count of $O(\log n)$ bits, a bit, and the round. The round number is not bounded, which is why Fokkink and Pang give versions with a finite state space.

## Properties

- **Las Vegas.** Always correct when it ends, ends with probability 1.
- **Needs $n$.** The hop counter must be compared with $n$. Without it no algorithm of this kind can be correct and end for sure.
- **Needs FIFO channels**, so that the messages of a round stay in order with those of later rounds.
- **Uniform randomness at each process**, independent of the others.
- **The leader is a random process.** Every process has the same chance to win, by symmetry.

## Variants and improvements

- **The 1990 algorithm.** In the journal version Itai and Rodeh give an asynchronous algorithm in two phases. In the selection phase each active process flips a coin about $c \log n$ times and drops out when it flips 0 and its active predecessor flips 1. In the verification phase each remaining process sends a counter round the ring; if more than one is left, the algorithm starts again. They show $O(n \log n)$ expected bits.
- **Synchronous rings.** For synchronous rings of known size Itai and Rodeh give an algorithm with on average at most $2.442\,n$ bits and $O(n)$ time.
- **Finite state.** Fokkink and Pang give versions with bounded round numbers that a probabilistic model checker can verify for small rings.
- **Franklin with coins.** Bakhshi, Fokkink, Pang and van de Pol made a randomized version of [Franklin's algorithm](/franklin/) for anonymous bidirectional rings.
- **Unknown $n$.** If processes only know a bound $N \ge n$, the verification message can travel $2N - 1$ hops. Itai and Rodeh show that with $n$ unknown, no algorithm in which processes stop is always correct; the best one can do is correct with high probability, or correct without explicit termination.

## When to use it

Use it on a ring of identical processes whose size is known, where no identifiers are available or trusted, and where a random leader is fine. If processes have distinct identifiers, a deterministic algorithm such as [Chang-Roberts](/chang-roberts/) or [Dolev-Klawe-Rodeh](/dolev-klawe-rodeh/) is simpler. If $n$ is not known, use a Monte Carlo version and accept a small chance of error.

## Pitfalls

- **Forgetting the hop count.** Without it a process cannot tell its own message from a message of another process with the same value, and two processes can both claim to lead.
- **Comparing values only.** The round must be compared first. Otherwise a process that drew a high value in an old round can stop the messages of the current round.
- **Non-FIFO channels.** A message of a later round can overtake one of an earlier round, and the dirty bit can be set or missed on the wrong message.
- **Assuming the count is fixed.** The number of messages depends on the schedule and on the coins. Only its expected value is bounded.

## Implementations

## History

Itai and Rodeh presented randomized election on anonymous rings at FOCS in 1981, and the journal version appeared in Information and Computation in 1990. They showed that randomization overcomes [Angluin's impossibility result](/anonymous-ring-impossibility/) when $n$ is known, and that it cannot fully do so when $n$ is unknown. The form with random identifiers, round numbers, hop counters and a dirty bit is the one used in textbooks and in the analysis by Fokkink and Pang.

## References
