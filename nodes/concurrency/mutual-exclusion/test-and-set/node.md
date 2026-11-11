---
tag: JZT9EK
kind: concept
slug: test-and-set
name: Test-and-set
aliases: [TAS, test-and-set instruction, test-and-set register]
area: concurrency/mutual-exclusion
level: intro
summary: An atomic instruction that sets a bit to true and returns its old value. It gives a simple spin lock, and its consensus number is exactly 2.
history:
  year: 1964
  people: [Maurice Herlihy]
  note: The IBM System/360 had a TS (test and set) instruction in 1964. Herlihy showed in 1991 that test-and-set solves wait-free consensus for two processes but not for three.
prereqs: [critical-section]
see_also: [read-modify-write, compare-and-swap, fetch-and-add, consensus-number, registers-have-consensus-number-one, cas-has-infinite-consensus-number, spin-lock, load-linked-store-conditional]
sources:
  - paper: doi:10.1145/114005.102808
    title: Maurice Herlihy, Wait-free synchronization, ACM Transactions on Programming Languages and Systems 13(1), 1991, pages 124-149
    locator: the consensus hierarchy; the theorem that test-and-set, swap, fetch-and-add, queues and stacks have consensus number 2
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 5, The Relative Power of Primitive Synchronization Operations (common2 read-modify-write operations), and Chapter 7, Spin Locks and Contention (the TAS lock)
  - paper: doi:10.1109/71.80120
    title: Thomas E. Anderson, The performance of spin lock alternatives for shared-memory multiprocessors, IEEE Transactions on Parallel and Distributed Systems 1(1), 1990, pages 6-16
    locator: the cost of spinning with test-and-set on a bus with caches
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 10, Mutual Exclusion (the test-and-set algorithm for read-modify-write shared variables)
---

Test-and-set is an atomic instruction on one shared bit $b$. In one indivisible step, $\mathrm{TAS}(b)$ writes true to $b$ and returns the value that $b$ had before. A process writes false to $b$ to reset it. It is the simplest [read-modify-write](/read-modify-write/) operation, and it is enough for a [spin lock](/spin-lock/): the process whose test-and-set returns false holds the lock. In the [consensus hierarchy](/consensus-number/) of Herlihy (1991) it has consensus number exactly 2.

## In plain words

Think of a single light switch in a dark hall. Each person who arrives flips the switch on and looks at what it was before. If it was off, that person is the first one, and wins. If it was already on, somebody else was first.

Because flipping and looking happen in one move, two people can never both see "off". This is why the switch can guard a room: the winner goes in, and turns the switch off when it leaves.

The switch can pick one winner from two people in a way that both agree on. With three or more people, a switch and plain notes on a board are not enough to make everyone agree, no matter how cleverly they use them.

## The idea

**Model.** There are $n$ asynchronous processes $p, q, \ldots$ that share memory. The memory is sequentially consistent: every run is one sequence of atomic steps. The objects are atomic read/write registers, with consensus number 1, and test-and-set bits. In the notation of the [mutex](/mutex/) page, $i$ and $j$ are process indices and $k$ is the number of processes that contend.

**The operation.** On a bit $b$:

```pseudo
TAS(b)                     ▷ one atomic step
    old ← b
    b ← true
    return old
```

Many processors had it: the IBM System/360 `TS` instruction (1964), `BSET` and `TAS` on the Motorola 68000, and `XCHG` or `LOCK BTS` on x86. C11 has `atomic_flag_test_and_set`, the only atomic type that the standard requires to be lock free. Java has `AtomicBoolean.getAndSet(true)`. A [swap](/read-modify-write/) of the value true, a [compare-and-swap](/compare-and-swap/) from false to true, and a [fetch-and-add](/fetch-and-add/) on a counter can each do the work of test-and-set.

**Consensus number 2.** In the consensus problem each process has an input and must decide a value, so that all decisions are equal (agreement), each decision is an input (validity), and each process decides in a finite number of its own steps (wait freedom). The consensus number of an object type is the largest $n$ for which objects of that type and registers solve consensus for $n$ processes.

*Claim 1.* One test-and-set bit $T$ (false at the start) and two registers $reg[0]$ and $reg[1]$ solve wait-free consensus for processes 0 and 1.

```pseudo
DECIDE(i, v)                ▷ j = 1 − i
    reg[i] ← v              ▷ announce the input
    if TAS(T) = false then return v
    return reg[j]
```

*Proof.* Each process takes at most three steps, so the protocol is wait free. Each decision is the value $v$ of the caller or the content of $reg[j]$, which only process $j$ writes, with its input; so validity holds. For agreement, note that $T$ is false only before the first TAS on it. So exactly one TAS returns false, if any TAS runs at all. Call its caller the winner $w$. The winner decides its own input $v_w$. If the other process $\ell$ decides, its TAS returned true, so its TAS came after the TAS of $w$. And $w$ wrote $reg[w] \leftarrow v_w$ before its TAS. Nobody else writes $reg[w]$. So the read of $\ell$ returns $v_w$, and $\ell$ decides $v_w$ too. $\square$

The test file runs this protocol for all four pairs of inputs over every interleaving, and checks agreement and validity in each final state. The longest run has 9 steps of the explorer: three marks or memory steps for each process, as the winner skips its read.

*Claim 2 (Herlihy 1991).* Test-and-set bits and registers do not solve wait-free consensus for three processes. We give the proof idea. Assume a protocol for processes $p$, $q$ and $r$. A state is bivalent if both decisions are still possible from it. As in the proof of the [FLP theorem](/flp-impossibility/), there is a bivalent *critical* state $s$: each next step leads to a univalent state. Say the step of $p$ leads to a 0-valent state and the step of $q$ to a 1-valent state. Both steps must be on the same object, or they commute. They cannot be register steps: [registers have consensus number one](/registers-have-consensus-number-one/) by the same case analysis. So both are TAS on the same bit, or one is TAS and the other a read or write of that bit. Look at the case of two TAS steps. After $p$ then $q$, and after $q$ then $p$, the bit is true in both states, and all other objects are the same. Only the local states of $p$ and $q$ differ. Now let $r$ run alone from each state. It cannot see the difference, so it decides the same value in both, but one state is 0-valent and the other is 1-valent. That is a contradiction. The other cases are similar: a write of the bit hides the effect of a TAS before it, and a read is not seen by $r$. So the consensus number of test-and-set is exactly 2. By the [universal construction](/universal-construction/), it follows that test-and-set and registers cannot give a wait-free implementation of compare-and-swap for three or more processes; see [CAS has infinite consensus number](/cas-has-infinite-consensus-number/).

The test file also runs a natural attempt for three processes, in which the winner decides its own value and each loser reads one other register. The explorer finds an interleaving in which two processes decide different values.

## Examples

**The test-and-set lock.**

```pseudo
LOCK()
    while TAS(L) = true do nothing
UNLOCK()
    L ← false
```

*Mutual exclusion.* A process enters only when its TAS returns false. Between two such TAS steps there must be a write of false, which only the holder does when it leaves. So at most one process is in the critical section.

*Deadlock freedom.* If the lock is free and processes keep trying, the next TAS returns false.

*No starvation freedom.* The lock does not record who came first. The test file finds this run, and replays its cycle 50 times:

| step | process | action | $L$ after |
|---|---|---|---|
| 1 | 1 | TAS returns false, enters | true |
| 2 | 0 | TAS returns true, tries again | true |
| 3 | 1 | leaves: $L \leftarrow$ false | false |
| 4 | 1 | tries again: TAS returns false, enters | true |
| 5 | 0 | TAS returns true, tries again | true |
| ... | | steps 3 to 5 repeat | |

Process 0 takes a step in every cycle, so the run is fair, but it never enters. A strong scheduler can always let the holder take the lock back first.

*Cost under contention.* Each TAS writes the bit, even when it fails. In the cache coherent (CC) model a write needs the cache line in exclusive mode, so each failed TAS of a waiter is a remote memory reference, and it also takes the line away from the other waiters. The number of RMRs in one passage of a waiter is not bounded: it grows with the time that the holder stays inside. On the [spin lock](/spin-lock/) page the test file measures 199 remote references for 200 steps of a TAS waiter while the lock is held, against 1 for a test-and-test-and-set waiter. See [RMR complexity](/rmr-complexity/).

**A one-shot flag.** "Run this initialization once": each caller does $\mathrm{TAS}(done)$, and only the caller that gets false runs the code. This is consensus on who goes first, and it is wait free.

**Two-process consensus.** The protocol of Claim 1 is the standard example that test-and-set is stronger than registers.

## Where it is used

- The [spin lock](/spin-lock/) family: the TAS lock, the test-and-test-and-set lock, and backoff locks. In Linux and many runtimes, the first try of a lock is a single atomic exchange or compare-and-swap.
- The C11 `atomic_flag` and the C++ `std::atomic_flag`, which are the portable lock-free building block.
- The theory of synchronization power. Test-and-set, swap, [fetch-and-add](/fetch-and-add/), queues and stacks all have consensus number 2. Herlihy proved this for the read-modify-write operations whose functions commute or overwrite each other, and Afek, Weisberger and Weisman (1993) called a related class Common2. [Compare-and-swap](/compare-and-swap/) and [LL/SC](/load-linked-store-conditional/) have infinite consensus number. See [consensus number](/consensus-number/).
- Renaming and leader election, where a test-and-set bit picks one winner among the processes that arrive.

## References
