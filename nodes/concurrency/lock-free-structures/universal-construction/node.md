---
tag: TT2P8N
kind: technique
slug: universal-construction
name: Universal construction
aliases:
- Herlihy universal construction
- wait-free universal construction
- universality of consensus
area: concurrency/lock-free-structures
level: advanced
summary: Turn any sequential object into a linearizable wait-free one for n processes, from n-process consensus objects and registers, with a log of operations and an announce array.
prereqs: [cas-has-infinite-consensus-number, helping, linearizability]
see_also: [consensus-number, cas-has-infinite-consensus-number, helping, wait-freedom, lock-freedom, consensus-problem, atomic-snapshot, linearization-point]
sources:
  - paper: doi:10.1145/114005.102808
    title: Maurice Herlihy, Wait-free synchronization, ACM Transactions on Programming Languages and Systems 13(1), 1991
    locator: pages 124 to 149, the section on universality (the wait-free construction from consensus objects, with an announce array)
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 6, Universality of consensus (the lock-free and the wait-free universal constructions and their proofs)
  - paper: doi:10.1145/161468.161469
    title: Maurice Herlihy, A methodology for implementing highly concurrent data objects, ACM Transactions on Programming Languages and Systems 15(5), 1993
    locator: pages 745 to 770 (copy the object, change the copy, and swing a root pointer with load-linked/store-conditional)
  - paper: doi:10.1145/78969.78972
    title: Maurice Herlihy and Jeannette M. Wing, Linearizability, a correctness condition for concurrent objects, ACM Transactions on Programming Languages and Systems 12(3), 1990
    locator: the definition of linearizability that the construction satisfies
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations, and Advanced Topics, second edition, Wiley, 2004
    locator: the chapter on wait-free simulations of arbitrary objects (the universal construction and its proof)
---

## In plain words

You have a sequential object, for example a queue, and you want a [linearizable](/linearizability/), [wait-free](/wait-freedom/) version that $n$ processes can share. The universal construction does this for every object at once. Its one tool is a consensus object: each process proposes a value, and all get the same proposed value back.

The idea is a log. Every operation is a node. At each log position, one consensus object decides which node comes next. A process whose node is in the log runs the log from the start on a private copy of the object, and so gets its answer. All processes see the same log, so the answers agree. To stop one process from losing every consensus for ever, each process first announces its operation, and at each position all propose the announced operation of a process chosen in turn. This is [helping](/helping/).

## When it applies

- You have a sequential specification of the object: a start state and a function from (state, operation) to (new state, result). The object must be deterministic, or the processes would not agree on the results.
- You have consensus objects for $n$ processes, or something that implements them wait-free: [compare-and-swap](/compare-and-swap/), [load-linked/store-conditional](/load-linked-store-conditional/), or any object with [consensus number](/consensus-number/) at least $n$. Since [CAS has infinite consensus number](/cas-has-infinite-consensus-number/), any machine with CAS can build every object wait-free.
- You want a proof that an object can be built, or a correct but slow baseline. It is not a fast design: see Pitfalls.

It does not apply with only read/write registers, fetch-and-add, or other objects of consensus number lower than $n$: those cannot implement consensus for $n$ processes, so this construction has nothing to start from. That is the other half of Herlihy's result: an object is universal for $n$ processes exactly when its consensus number is at least $n$.

## The template

**Shared data.** A node holds an operation, a sequence number $seq$ (0 while the node is not in the log), a pointer $next$, and a one-shot consensus object $decideNext$. A sentinel node $tail$ starts the log with $seq = 1$. The array $head[0 .. n-1]$ holds, for each process, the last node of the log that it knows. The array $announce[0 .. n-1]$ holds the current operation of each process. Initially every $head[j]$ and $announce[j]$ is $tail$.

```text
max_head():                                   -- the node with the largest seq among the heads
  read head[0], ..., head[n-1] and their seq fields; return the one with the largest seq

append(before, after, i):                     -- any process may do it; all write the same values
  before.next := after
  after.seq := before.seq + 1
  head[i] := after

LOCK-FREE apply(op) by process i:
  node := new node(op)
  while node.seq = 0:
    before := max_head()
    after := before.decideNext.decide(node)   -- propose my own node
    append(before, after, i)
  return replay(node)

WAIT-FREE apply(op) by process i:
  node := new node(op); announce[i] := node
  before := max_head(); head[i] := before
  while node.seq = 0:
    other := announce[(before.seq + 1) mod n] -- whose turn is this position?
    prefer := other if other.seq = 0 else node
    after := before.decideNext.decide(prefer)
    append(before, after, i)
    before := after
  head[i] := node
  return replay(node)

replay(node):                                 -- the answer of node
  s := the start state of the sequential object
  for each node x of the log, from tail.next to node, in order:
    (s, r) := apply x.op to s
  return r
```

This is the form of Herlihy and Shavit (Chapter 6), with one change in the wait-free loop: after an append the process goes on from the node it just appended, instead of reading all heads again. The implementation folder has both forms, run on a simulated one-shot consensus object: the first value proposed to it is decided, and every later proposal returns that value.

**Why the log is well formed.** Two facts carry the proofs.

1. *The seq fields are set in order.* A process sets $after.seq$ only when it holds $before$ with $before.seq$ already set: it got $before$ from a head (and a head is written only after its seq) or it set $before.seq$ itself in its previous append. By induction on the position, when the node at position $p$ gets its seq, all nodes at positions below $p$ already have theirs, and their $next$ fields are set. So $replay$ never meets a missing $next$.
2. *No node is in the log twice.* A process proposes a node $x$ at position $p$ only after it holds the node at $p - 1$ and has read $x.seq = 0$. By fact 1, $x$ is then not at any position up to $p - 1$. If $x$ were already at a position above $p$, position $p$ would already be decided, and the decide returns that other node, not $x$. So each node gets exactly one position.

**Linearizability.** Linearize each operation at the moment its node is decided, that is, the first decide on the position that it gets. The order of these moments is the order of the log, because position $p + 1$ can be decided only by a process that holds the decided node at $p$. The moment is inside the operation: the node exists only after the call starts (in the wait-free form, others learn it only from $announce[i]$, which is written after the call starts), and the call returns only after it reads $node.seq \ne 0$, which is after the decision. The result is the result of the operation in the sequential run of the log, which is what replay computes. So every history is linearizable, with the log as the witness order.

**Lock-freedom of the first form.** Every round of the loop decides a position (or finds one decided). Each decided position holds a different node, by fact 2. If a process loops for ever, infinitely many positions are decided, so infinitely many different operations are put in the log. With $n$ processes, each with one pending operation at a time, infinitely many operations must have finished. So some operation always finishes. A single process can still lose every consensus: it is not wait-free.

**Wait-freedom of the second form.** Let process $A$ write $announce[A]$ at time $t_0$, and let $L_0$ be the largest decided position at time $t_0$.

- *Every position $p \ge L_0 + 2$ with $p \bmod n = A$ is safe for $A$.* Position $p$ is decided by the first process $Q$ that calls decide on it. $Q$ read $announce[A]$ after it held the node at $p - 1$, so after position $p - 1$ was decided, so after $t_0$. So $Q$ read $A$'s node. If $A$'s node had seq 0, $Q$ proposed it, and $Q$'s proposal wins position $p$. Otherwise $A$'s node was already in the log. In both cases $A$'s node is at a position of at most $p$.
- *There is such a $p$ in $L_0 + 2, \ldots, L_0 + n + 1$*, because these are $n$ consecutive numbers. So $A$'s node lands at a position of at most $L_0 + n + 1$.
- *$A$ starts at position $L_0 - 1$ or higher.* The first process that called decide on position $L_0$ had set its own head to the node at $L_0 - 1$ before that call, and a process never moves its head back below the last position it has decided on. $A$ reads all heads after $t_0$, so $max\_head$ gives $A$ a node at position $m \ge L_0 - 1$.
- *So $A$ loops at most $n + 2$ times.* Each round moves $before$ up by one position. When $before$ is at position $L_0 + n + 1$ or higher, $A$'s node has its seq by fact 1, and the loop ends. That takes at most $(L_0 + n + 1) - (L_0 - 1) = n + 2$ rounds.

**Cost per operation.** Count the shared steps. The threading phase has one write to $announce$, $2n$ reads in $max\_head$, two writes to $head$, and at most $n + 2$ rounds of seven steps each (three reads, one decide, three writes), plus one last read of $node.seq$. That is at most $9n + 18$ steps, which is $O(n)$, whatever the schedule. The replay then reads one $next$ field per earlier operation, so it costs $O(k)$ steps for the $k$-th operation in the log, plus the local work of the sequential object. In this form, the total is wait-free (it is bounded for each operation) but it grows with the length of the history. The $O(n)$ bound is for agreeing on the order; computing the answer costs extra unless the nodes keep states, as in the variations below.

## Classic examples

**A queue from consensus.** The tests in the implementation folder build a FIFO queue from the sequential queue specification, in both forms, and check them with the interleaving explorer and the linearizability checker from [linearizability](/linearizability/).

| check | wait-free form | lock-free form |
|---|---|---|
| enq ‖ enq, every schedule | 933 states, 6 histories, all linearizable | 372 states, 6 histories, all linearizable |
| enq ‖ deq, every schedule | 933 states, 8 histories, all linearizable | 372 states, 10 histories, all linearizable |
| rounds of the loop, every schedule above | at most 2 (bound $n + 2 = 4$) | at most 2 |
| $n = 3$ and $n = 4$, each process enq then deq, 2000 random schedules | all linearizable, rounds at most $n + 2$ | all linearizable |
| one process alone | one round per operation | one round per operation |
| adversary, $n = 2, \ldots, 5$, head starts of 0 to 100 steps | process 0 ends after at most $n + 2$ rounds (worst seen: 2, 4, 4, 5) | process 0 has not ended after 2000 steps; the others have put 125 to 207 nodes in the log |

In the adversary run, process 0 does one dequeue and the others enqueue for ever. Each time process 0 is about to propose on an open position, the others run until that position is decided. In the lock-free form, process 0 never wins. In the wait-free form, the others reach the position whose turn belongs to process 0, read its announced node, and propose it for it.

**Herlihy's copy method.** Herlihy (1993) gave a practical form for small objects: a root pointer points to the current version of the object. An operation reads the root, copies the object, applies the operation to the copy, and swings the root to the copy with [LL/SC](/load-linked-store-conditional/) or [CAS](/compare-and-swap/). This is lock-free. For wait-freedom, the paper adds operation combining: each process applies the announced operations of the others to its copy too.

**Consensus number as the right measure.** With this construction, an object $X$ with consensus number $n$ plus registers implements every object for $n$ processes. With an object of consensus number $k < n$ it can fail: see [consensus number](/consensus-number/) and [registers have consensus number one](/registers-have-consensus-number-one/).

## Variations

- **Store states in the nodes.** In Herlihy's 1991 paper each cell of the log also records the state after its operation and the result, so a process computes its result from the previous cell instead of replaying the whole log. The paper also reuses cells, so that the memory is bounded. This removes the $O(k)$ replay but copies the object state at each operation.
- **Lock-free only.** Drop the announce array. Each process proposes its own node. Fewer steps, but a process can starve.
- **Copy and swing.** Herlihy's 1993 method above, with a single CAS or SC on a root pointer instead of a log.
- **Faster wait-free constructions.** Later work cuts the cost: combining many announced operations into one step (for example the P-Sim construction of Fatourou and Kallimanis, 2011), and constructions for objects with large state that copy only the parts that change. The fast-path-slow-path method of Kogan and Petrank (2012) uses an announce-and-help slow path only when the fast lock-free path fails.
- **Consensus from other objects.** The consensus objects can be one CAS word each ([CAS has infinite consensus number](/cas-has-infinite-consensus-number/)), or built from any object with a high enough consensus number.

## Pitfalls

- **It is slow.** Every operation reads all $n$ heads, and in the simple form it replays the whole log. Even with stored states, it copies the object state on every operation. It shows what is possible; specific algorithms such as the [Michael and Scott queue](/michael-scott-queue/) are much faster.
- **Consensus objects are one-shot.** Each node needs its own consensus object, so the construction uses unboundedly many of them unless nodes are reused. Reusing them safely needs care with the [ABA problem](/aba-problem/) and with memory reclamation, for example [hazard pointers](/hazard-pointers/).
- **Helping in turn is what gives wait-freedom.** If processes always propose their own node, the construction is only lock-free. If they help but not in a fixed turn order, a process can still be skipped for ever.
- **The help check must read the seq of the announced node.** Proposing an announced node that is already in the log would put it in twice. The check $other.seq = 0$ prevents this, and the proof needs fact 1 to show that the check is not too late.
- **Nondeterministic objects.** If the sequential specification allows several results, the processes must agree on the result too. Put the chosen result in the node with the consensus, or the replays can disagree.

## Exercises

1. In the wait-free form, take $n = 3$ and let process 2 announce its operation and then stop for a long time. Show that processes 0 and 1 put process 2's node in the log, and bound the number of positions that they can decide before they do it.
2. Give a schedule of the lock-free form with $n = 2$ in which process 0 loops for ever. Why does this schedule not stop process 1?
3. Change the wait-free form so that the help check is removed (the process always proposes $announce[(before.seq + 1) \bmod n]$). Show a run in which a node is put in the log twice.
4. Modify the construction so that each node also stores the object state after its operation. What is the cost per operation now, and what must be atomic?
5. Use the construction with a consensus object for 2 processes and $n = 3$ processes. Where does the proof break?

## References
