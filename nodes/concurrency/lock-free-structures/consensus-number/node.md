---
tag: FQYCHK
kind: concept
slug: consensus-number
name: Consensus number (Herlihy hierarchy)
aliases:
- Herlihy hierarchy
- consensus hierarchy
- wait-free hierarchy
area: concurrency/lock-free-structures
level: advanced
summary: The largest number of processes for which objects of a type, with registers, solve wait-free consensus. It ranks primitives by power. Registers have 1, test-and-set 2, CAS infinity.
prereqs: [consensus-problem, wait-freedom, linearizability]
see_also: [registers-have-consensus-number-one, cas-has-infinite-consensus-number, universal-construction, read-modify-write, compare-and-swap, fetch-and-add, test-and-set, flp-impossibility]
sources:
  - paper: doi:10.1145/114005.102808
    title: Maurice Herlihy, Wait-free synchronization, ACM Transactions on Programming Languages and Systems 13(1), 1991
    locator: pages 124 to 149 (the definition, the hierarchy, the proofs for registers, read-modify-write, queues, m-register assignment, compare-and-swap and memory-to-memory move and swap, and the universal construction)
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 5 (the relative power of primitive synchronization operations)
  - paper: doi:10.1145/263867.263888
    title: Prasad Jayanti, Robust wait-free hierarchies, Journal of the ACM 44(4), 1997
    locator: pages 592 to 614 (the variants of the hierarchy and the question of robustness)
  - paper: doi:10.1145/258533.258651
    title: Wai-Kau Lo and Vassos Hadzilacos, All of us are smarter than any of us, wait-free hierarchies are not robust, STOC 1997
    locator: nondeterministic types for which the hierarchy is not robust
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations, and Advanced Topics, second edition, Wiley, 2004
    locator: the chapter on wait-free simulations of arbitrary objects (consensus numbers and the universal construction)
---

## In plain words

Different atomic instructions have different power. A read and a write of one memory word are weak; a compare-and-swap is strong. The consensus number makes this exact. Take a type of shared object, add as many plain read/write registers as you like, and ask: for how many processes can these objects solve consensus, so that all processes decide the same input value and no process ever waits for another? The largest such number is the consensus number of the type.

Registers get 1: they cannot solve consensus even for two processes. Test-and-set, swap, fetch-and-add, queues and stacks get 2. Compare-and-swap and load-linked/store-conditional work for any number of processes. The ranking matters because consensus is universal: an object that solves consensus for a number of processes can build every other object for that many processes, without waits.

## The idea

**Notation and model.** $n$ is the number of processes, $p$ and $q$ are processes, $i$ and $j$ are indices, and $m$ is a number of shared words. Processes are asynchronous and can crash between steps. Memory is sequentially consistent, and every object is linearizable.

**Consensus.** Each process has an input and must output (decide) a value, with three conditions: *agreement*, all decided values are equal; *validity*, the decided value is the input of some process; *wait-free termination*, each process that does not crash decides after a finite number of its own steps. This is the [consensus problem](/consensus-problem/) in shared memory, with wait-freedom in place of a bound on failures: any number of processes can crash.

**Definition (Herlihy 1991).** A type $X$ *solves $n$-process consensus* if there is a wait-free consensus protocol for $n$ processes that uses any number of objects of type $X$, in any initial states, and any number of atomic read/write registers. The **consensus number** of $X$ is the largest $n$ for which $X$ solves $n$-process consensus, or $\infty$ if it solves it for every $n$.

Because a lock-free implementation of a one-shot object is wait-free (each process calls only one operation), the same numbers bound lock-free consensus. They do not bound [obstruction-free](/obstruction-freedom/) consensus, which registers alone can solve.

**The hierarchy.**

| type | consensus number | why |
|---|---|---|
| atomic read/write registers | 1 | [registers have consensus number one](/registers-have-consensus-number-one/) |
| atomic snapshot | 1 | it has a wait-free implementation from registers ([atomic snapshot](/atomic-snapshot/)) |
| [test-and-set](/test-and-set/), swap, [fetch-and-add](/fetch-and-add/) | 2 | the 2-process protocol below; they are [read-modify-write](/read-modify-write/) operations whose functions commute or overwrite |
| queue, stack | 2 | the queue starts with "win" then "lose"; 3 processes fail by a valence argument |
| $m$-register assignment ($m > 1$) | $2m - 2$ | Herlihy 1991: writing $m$ registers in one atomic step |
| [compare-and-swap](/compare-and-swap/), [LL/SC](/load-linked-store-conditional/) | $\infty$ | [CAS has infinite consensus number](/cas-has-infinite-consensus-number/) |
| memory-to-memory move, memory-to-memory swap | $\infty$ | Herlihy 1991 |
| queue with peek, sticky bit | $\infty$ | the first value stays visible to every process |

**Lower bounds are protocols.** For test-and-set, swap, fetch-and-add, queue and stack, two processes use the same pattern: process $i$ writes its input to prop[$i$], then takes one step on the shared object, whose answer tells it whether it was first. The first process decides its own input. The second one knows that the other was first, and the first one wrote its input before its step, so the second reads prop[$1 - i$] and decides it. For CAS, each process runs CAS($x$, $\bot$, input), which returns the old value: $\bot$ for the first process, and the winner's input for every other one.

**Upper bounds are valence arguments.** To show that a type cannot solve consensus for $n + 1$ processes, assume a protocol and find a *critical* state: one from which the decision is not yet fixed, but any next step fixes it. All processes must be about to access the same object, and the next steps must be distinguishable by someone. For registers, a read or a write by one process can be hidden from the other; for test-and-set, swap and fetch-and-add with 3 processes, the two first steps commute or overwrite each other, so a third process cannot tell which was first. The full proof for registers is on [registers have consensus number one](/registers-have-consensus-number-one/); the one for read-modify-write operations is on [read-modify-write](/read-modify-write/). The argument is in the style of [FLP](/flp-impossibility/), but for shared memory and wait-free protocols.

**Universality.** Herlihy also proved the other direction. A type with consensus number $n$, together with registers, can implement *any* object with a sequential specification, wait-free, for $n$ processes. The method is the [universal construction](/universal-construction/). So the consensus number answers one question with two faces:

- if $X$ has consensus number $k < n$ and $Y$ solves $n$-process consensus, then no wait-free implementation of $Y$ from $X$ and registers exists for $n$ processes;
- if $X$ has consensus number at least $n$, then every $Y$ has a wait-free implementation from $X$ and registers for $n$ processes.

**Robustness.** The hierarchy is *robust* if objects of several types, each with consensus number at most $k$, cannot together solve consensus for more than $k$ processes. Jayanti (1997) showed that the answer depends on the exact form of the definition: whether registers are free, and whether one object or many objects of the type may be used. Some of these forms give different numbers and are not robust. Lo and Hadzilacos (1997) showed that for nondeterministic types the hierarchy is not robust: some types solve consensus together for more processes than any one of them can alone. For deterministic types, robustness is known for some classes of types, and the general case has been studied since then.

**What the number does not say.** It is a coarse measure. Two types with the same consensus number need not be able to implement each other for more processes than that number, and the number says nothing about speed or space.

## Examples

The numbers come from the tests in the implementation folder, which run the interleaving explorer over every interleaving and check agreement and validity at every state (any state can be the last one for a process that crashes there) and that every run ends.

| protocol | processes | states | final states | most steps per process |
|---|---|---|---|---|
| test-and-set | 2 | 12 | 2 | 3 |
| fetch-and-add | 2 | 12 | 2 | 3 |
| swap | 2 | 12 | 2 | 3 |
| queue ("win", "lose") | 2 | 12 | 2 | 3 |
| stack ("win" on top) | 2 | 12 | 2 | 3 |
| CAS | 1, 2, 3, 4 | 2, 5, 13, 33 | 1, 2, 3, 4 | 1 |

The two final states of each 2-process protocol are "p0 won" and "p1 won". The CAS protocol has one final state per possible winner.

**A failed attempt: test-and-set with 3 processes.** A loser knows it lost, but not who won. A natural guess is "decide the input of the lowest process that has written a proposal". The explorer finds the schedule $[0, 1, 1, 0, 0]$: $p_0$ writes $a$, $p_1$ writes $b$, $p_1$ wins the test-and-set and decides $b$, $p_0$ loses, reads prop[0] $= a$ and decides $a$. Agreement fails. The valence argument shows that every attempt fails in some run.

**Fetch-and-add for 3 processes.** The [fetch-and-add](/fetch-and-add/) page shows the same failure for the natural 3-process attempt with fetch-and-add.

## Where it is used

- **Choosing hardware primitives.** Every common multiprocessor instruction set has CAS or LL/SC, because with only consensus number 2 operations, some objects (such as a wait-free queue for 3 processes) cannot be built at all.
- **Proving that an implementation cannot exist.** For example, no wait-free queue from registers; no wait-free implementation of CAS from test-and-set and registers for 3 processes; no wait-free snapshot can implement a queue.
- **Universal constructions.** The [universal construction](/universal-construction/) turns any consensus object into any object.
- **Beyond consensus.** The same method ranks objects by $k$-set agreement, and it leads to the study of objects below consensus number 2.

## References
