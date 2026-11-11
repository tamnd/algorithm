---
tag: MGMTMQ
kind: theorem
slug: cas-has-infinite-consensus-number
name: CAS has infinite consensus number
aliases:
- CAS universality
- universality of compare-and-swap
area: concurrency/lock-free-structures
level: advanced
summary: One compare-and-swap word solves wait-free consensus for any number of processes, in one step each. With the universal construction, CAS and registers implement every object wait-free.
prereqs: [consensus-number, compare-and-swap]
see_also: [consensus-number, universal-construction, compare-and-swap, load-linked-store-conditional, registers-have-consensus-number-one, read-modify-write, wait-freedom, multi-word-cas]
sources:
  - paper: doi:10.1145/114005.102808
    title: Maurice Herlihy, Wait-free synchronization, ACM Transactions on Programming Languages and Systems 13(1), 1991
    locator: pages 124 to 149 (compare-and-swap has infinite consensus number; the universal construction)
  - paper: doi:10.1145/62546.62593
    title: Maurice Herlihy, Impossibility and universality results for wait-free synchronization, PODC 1988
    locator: pages 276 to 290 (the conference version)
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 5, the section on the compareAndSet operation; Chapter 6 (universality of consensus)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations, and Advanced Topics, second edition, Wiley, 2004
    locator: the chapter on wait-free simulations of arbitrary objects
---

## Statement

**Model.** Any number $n$ of asynchronous processes, any of which may crash, share one compare-and-swap object $x$. The object holds a value. CAS($x$, $e$, $v$) atomically compares the value with $e$, writes $v$ if they are equal, and returns the old value. The value $\bot$ is not an input, and $x$ starts as $\bot$.

**Theorem (Herlihy 1991).** For every $n \ge 1$, the following protocol is a wait-free consensus protocol for $n$ processes. Process $i$ with input $v_i$ runs:

```text
decide(v_i):
  old := CAS(x, ⊥, v_i)
  if old = ⊥ then return v_i
  else return old
```

Each process takes exactly one step. So the [consensus number](/consensus-number/) of compare-and-swap is $\infty$.

If the CAS returns only a success bit, the same holds with one more step: on failure, read $x$ and return the value read.

## In plain words

All processes race to put their own value into one empty memory word, and they all use compare-and-swap with "empty" as the expected value. Only the first one can succeed, because after it the word is no longer empty. Every later CAS fails and hands back the value that is already there, which is the winner's value. So every process learns the same value, it is one of the inputs, and nobody ever waits: one instruction and the process is done. The number of processes does not matter, so compare-and-swap is as strong as a primitive can be in this ranking.

## Proof

Fix $n$ and any run of the protocol. The object $x$ is linearizable, so its CAS steps happen one at a time in a total order. Only processes that take their step are in this order; a process that crashes before it takes no part.

**The first CAS wins.** Let $w$ be the process whose CAS is first in the order, if any. When $w$ runs, $x = \bot$, since nothing has written $x$ before. So the compare succeeds, $x$ becomes $v_w$, and $w$ receives $\bot$ and returns $v_w$.

**Every later CAS loses and learns $v_w$.** By induction on the order: after the first CAS, $x = v_w \ne \bot$, because $v_w$ is an input and $\bot$ is not. A later CAS compares $v_w$ with $\bot$, fails, writes nothing, and returns $v_w$. So $x$ stays $v_w$, and the process returns $v_w$.

**Agreement.** Every process that decides returns $v_w$.

**Validity.** $v_w$ is the input of $w$.

**Wait-freedom.** Each process decides after its single step, whatever the other processes do, crash included. Nothing in the argument depends on $n$; it even works when the set of processes is not known in advance. $\blacksquare$

For the form with a boolean CAS: the first CAS succeeds as above; every later CAS fails, and the following read returns $v_w$, because $x$ never changes again. Two steps per process.

**Checked on small cases.** The tests in the implementation folder run the interleaving explorer over every interleaving and check agreement and validity in every state, so every crash point is covered:

| processes | states (one step) | states (boolean CAS and read) | final states | most steps per process |
|---|---|---|---|---|
| 1 | 2 | 2 | 1 | 1 |
| 2 | 5 | 7 | 2 | 1 and 2 |
| 3 | 13 | 28 | 3 | 1 and 2 |
| 4 | 33 | 109 | 4 | 1 and 2 |

They also check all 8 binary input vectors for 3 processes, and 50 random runs of 8 processes in which about a third of them crash.

## Consequences

**Universality.** Herlihy's [universal construction](/universal-construction/) builds a wait-free linearizable implementation of any object with a sequential specification for $n$ processes from $n$-process consensus objects and registers. With this theorem, consensus objects come from CAS. So:

> With CAS and registers, every sequential object has a wait-free linearizable implementation, for any number of processes.

The construction is general, not fast: it takes $O(n)$ consensus steps per operation, plus the cost of applying the operations. Practical data structures use CAS more directly, but the theorem is the reason why it is enough to put CAS (or LL/SC) in hardware.

**Separations.** No object of consensus number $k$ can implement CAS, wait-free, for more than $k$ processes. In particular, there is no wait-free implementation of CAS from registers (consensus number 1) for 2 processes, or from [test-and-set](/test-and-set/), swap, [fetch-and-add](/fetch-and-add/), queues or stacks (consensus number 2) for 3 processes.

**LL/SC.** [Load-linked/store-conditional](/load-linked-store-conditional/) also has infinite consensus number: each process runs LL($x$); if the value is $\bot$, it tries SC($x$, $v_i$); then it reads $x$ and decides that value. A failed SC means that some other write happened, and the only writes write inputs over $\bot$. So both main hardware primitives are universal.

**Other universal objects.** The same one-step idea works for any object where the first operation leaves a mark that later operations can see and cannot remove: a queue with a peek operation, a sticky bit, memory-to-memory move or swap.

## Tightness

- **One step is the least possible.** A process that takes no step on shared memory cannot know the other inputs, so it can only decide its own input, and two such processes would disagree.
- **The value $\bot$ is needed.** The protocol needs an initial value that is not an input. If the word must start with an input value, use one more bit that says "empty".
- **The result needs an atomic compare.** A CAS whose compare and write are separate steps (a read, then a write) is just two register operations, and registers have [consensus number 1](/registers-have-consensus-number-one/).
- **Consensus, not every task.** The theorem says nothing about cost. For example, a wait-free queue from CAS exists, but known general methods pay $O(n)$ per operation or more, and Censor-Hillel, Petrank and Timnat showed that such queues need [helping](/helping/).

## History

Compare-and-swap was introduced on the IBM System/370 in the 1970s for multiprocessor synchronization. Herlihy (1988, journal version 1991) placed it at the top of the consensus hierarchy, together with LL/SC and memory-to-memory move and swap, and showed with the universal construction that any object with infinite consensus number is universal. Plotkin had shown in 1989 that sticky bits are universal in the same sense.

## References
