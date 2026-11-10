---
tag: J3RKBA
kind: data-structure
slug: matrix-clocks
name: Matrix clocks
aliases:
- Wuu-Bernstein matrix clock
area: distributed/clocks-and-ordering
level: advanced
summary: Each process keeps an n by n matrix whose row j is its latest knowledge of the vector clock of process j, so it can tell which events every process has already seen.
model: asynchronous-model
complexity:
  vars: {n: the number of processes}
  time: {worst: Θ(n^2)}
  space: {extra: Θ(n^2)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1984
  people: [Gene T. J. Wuu, Arthur J. Bernstein]
  note: Wuu and Bernstein used a matrix of counters per site to discard log entries in a replicated log and dictionary.
prereqs: [vector-clocks, happened-before]
see_also: [vector-clocks, lamport-clocks, replicated-log, causal-order-delivery, version-vectors, anti-entropy]
sources:
  - paper: doi:10.1145/800222.806750
    title: Gene T. J. Wuu and Arthur J. Bernstein, Efficient solutions to the replicated log and dictionary problems, PODC 1984
    locator: pages 233 to 242
  - paper: doi:10.1109/TSE.1987.232564
    title: Sunil K. Sarin and Nancy A. Lynch, Discarding obsolete information in a replicated database system, IEEE Transactions on Software Engineering SE-13(1), 1987
    locator: pages 39 to 47
  - paper: doi:10.1109/2.485846
    title: Michel Raynal and Mukesh Singhal, Logical time, capturing causality in distributed systems, IEEE Computer 29(2), 1996
    locator: pages 49 to 56 (scalar, vector and matrix time)
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 3, Section 3.7 (matrix time)
---

A matrix clock is an $n \times n$ array of counters that each of $n$ processes keeps. Row $i$ of the matrix of process $p_i$ is its own [vector clock](/vector-clocks/). Row $j$ is the newest vector clock of $p_j$ that $p_i$ knows of through the chain of messages that reached it. The minimum of a column then tells $p_i$ how many events of a process every process has already seen, which lets it discard old log entries and old messages. Wuu and Bernstein used the matrix in 1984 for a [replicated log](/replicated-log/).

## In plain words

A vector clock tells a computer what it knows. A matrix clock also tells it what the others know.

Each computer keeps a table with one row for each computer in the group. Its own row is its ordinary vector clock. Every other row is the newest copy of that computer's vector clock that has reached it, perhaps through other computers. Each message carries the whole table. On a receive, the computer keeps the larger value of each pair of entries, and it also updates its own row with the row of the sender.

Now look down one column of the table. The smallest number in the column says how many events of that computer every computer has surely heard of. Any record that only exists to tell others about those events can be thrown away.

## The abstract type

The setting is the [asynchronous model](/asynchronous-model/) with $n$ processes $p_1, \ldots, p_n$, known in advance, and point-to-point channels that need not be FIFO. No failure assumption is needed for the safety claims below. A matrix clock is a [logical clock](/lamport-clocks/) whose timestamp of an event $e$ of $p_i$ is a matrix $M(e)$. It must satisfy:

- **Own row.** Row $i$ of $M(e)$ is the vector clock $V(e)$.
- **Other rows.** For $j \ne i$, row $j$ of $M(e)$ is $V(g)$, where $g$ is the last event of $p_j$ that [happened before](/happened-before/) $e$, or the zero vector if there is none.
- **Knowledge query.** $\min_k M(e)[k][l]$ is a number $t$ such that, for each process $p_k$, the first $t$ events of $p_l$ are in the causal past of an event of $p_k$ that happened before $e$ or is $e$.

## Representation

Process $p_i$ stores an array $M_i[1 \ldots n][1 \ldots n]$ of non-negative integers. Entry $M_i[k][l]$ means: as far as $p_i$ knows, $p_k$ has heard of the first $M_i[k][l]$ events of $p_l$. Each message carries a copy of the matrix and the identity of the sender.

## Operations

```pseudo id=main
MATRIX-CLOCK at process p_i
L1  M_i ← the n × n zero matrix

TICK()                                         ▷ a local event
L2  M_i[i][i] ← M_i[i][i] + 1
L3  return a copy of M_i

SEND(m)
L4  attach t ← TICK() to m, and send m

RECEIVE(m)                                     ▷ m carries W and its sender p_j
L5  for k ← 1 to n do
L6      for l ← 1 to n do M_i[k][l] ← max(M_i[k][l], W[k][l])
L7  for l ← 1 to n do M_i[i][l] ← max(M_i[i][l], W[j][l])
L8  return TICK()

KNOWN-BY-ALL(l)                                ▷ events of p_l seen by every process
L9  return min over k of M_i[k][l]
```

Line L6 merges what both processes know about everyone. Line L7 is the step of a vector clock: $p_i$ now knows everything that $p_j$ knew when it sent the message. Without line L7, row $i$ would miss the events that $p_j$ itself had heard of.

## Example

Three processes run seven events. $P_1$ sends a message to $P_2$ (event $a$) and then does a local event $b$. $P_2$ does a local event $c$, receives the message of $a$ (event $d$) and sends a message to $P_3$ (event $e$). $P_3$ does a local event $f$ and receives the message of $e$ (event $g$). The rows of each matrix are listed in the order $P_1, P_2, P_3$.

| event | process | $M$ |
|---|---|---|
| $a$ | $P_1$ | $(1,0,0), (0,0,0), (0,0,0)$ |
| $b$ | $P_1$ | $(2,0,0), (0,0,0), (0,0,0)$ |
| $c$ | $P_2$ | $(0,0,0), (0,1,0), (0,0,0)$ |
| $d$ | $P_2$ | $(1,0,0), (1,2,0), (0,0,0)$ |
| $e$ | $P_2$ | $(1,0,0), (1,3,0), (0,0,0)$ |
| $f$ | $P_3$ | $(0,0,0), (0,0,0), (0,0,1)$ |
| $g$ | $P_3$ | $(1,0,0), (1,3,0), (1,3,2)$ |

At $g$, row 1 is $V(a) = (1,0,0)$, because $a$ is the last event of $P_1$ in the past of $g$. Event $b$ is not in that past, so $P_3$ does not know about it. Row 2 is $V(e)$, and row 3 is $V(g)$. The minimum of column 1 is 1: $P_3$ knows that all three processes have seen the first event of $P_1$. At $d$, the minimum of each column is 0, because $P_2$ knows nothing about $P_3$ yet.

## Correctness

The proof is an induction along the run. A row $j \ne i$ only changes by the entrywise maximum of line L6. The two rows that meet there are vector clocks of two events of $p_j$, and vector clocks grow along one process, so the maximum is the vector clock of the later of the two events. This is the last event of $p_j$ in the new causal past. For row $i$, line L7 adds the vector clock of the send, and the row of $p_i$ in the message can only be older than the present row of $p_i$. So row $i$ follows the vector clock rule exactly. The knowledge query follows from the rows, because entry $l$ of a vector clock counts a prefix of the events of $p_l$. The full proof is below.

## Complexity

| operation | time | message overhead |
|---|---|---|
| TICK | $\Theta(1)$, plus $\Theta(n^2)$ for the copy | none |
| SEND | $\Theta(n^2)$ | $n^2$ integers and a process identifier |
| RECEIVE | $\Theta(n^2)$ | none |
| KNOWN-BY-ALL | $\Theta(n)$ | none |

Each process stores $n^2$ integers. With $k$ events in the run, a message has $O(n^2 \log k)$ bits. This cost is the main reason to use a matrix clock only when its extra knowledge pays for itself.

## Variants

- **Send only what the receiver lacks.** In Wuu and Bernstein's log protocol, a site sends to $p_j$ only the log records that, by the matrix, $p_j$ may not have yet. An event of $p_l$ with index $t$ is known to $p_j$ when $M_i[j][l] \ge t$.
- **Causal delivery with a matrix.** The algorithm of Raynal, Schiper and Toueg keeps an $n \times n$ matrix of counts of messages sent between each pair of processes. A message carries the matrix, and the receiver waits until it has delivered every message that the matrix says was sent to it before. See [causal order delivery](/causal-order-delivery/).

## When to use it

Use a matrix clock when a process must know what the other processes know, not only what it knows itself. The main case is garbage collection in a replicated system: a log entry, a buffered message or a tombstone can be deleted once every replica has seen it. Sarin and Lynch used the same idea to discard obsolete information in a replicated database. For pure causality tests, a [vector clock](/vector-clocks/) is enough and costs $n$ times less.

## Pitfalls

- **Forgetting line L7.** Line L6 alone gives row $i$ only the old view of $p_i$ held by $p_j$. The row of the sender must also be merged into the own row.
- **Reading the column minimum as exact.** The minimum is a lower bound. Other processes can know more than $p_i$ knows that they know. Deleting on the lower bound is safe, but it can be late.
- **A silent process blocks collection.** If one process never sends, its row in all other matrices stays old, and no entry can be deleted. Periodic empty messages from each process avoid this.
- **Crashes.** A crashed process stops all garbage collection in the basic scheme, since its row never grows. The group must remove it from the matrix first, which needs a membership protocol.

## Implementations

## History

Gene Wuu and Arthur Bernstein introduced the matrix in 1984, in a PODC paper on the replicated log and the replicated dictionary. Each site keeps a table of what it knows each other site knows, and uses it to delete log records that all sites have received. Sarin and Lynch used a related matrix in 1987 to discard obsolete information in a replicated database. Raynal and Singhal presented scalar, vector and matrix time side by side in 1996.

## References
