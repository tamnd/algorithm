---
tag: FAZZ48
kind: concept
slug: fetch-and-add
name: Fetch-and-add
aliases:
- FAA
- fetch-and-increment
- atomic add
area: concurrency/lock-free-structures
level: intro
summary: An atomic instruction that adds a number to a memory word and returns the old value. It solves consensus for two processes but not three, so its consensus number is 2.
prereqs: [race-condition]
see_also: [compare-and-swap, read-modify-write, consensus-number, ticket-lock, combining-tree, herlihy-wing-queue, test-and-set, prefix-sums]
sources:
  - paper: doi:10.1109/TC.1983.1676201
    title: Allan Gottlieb, Ralph Grishman, Clyde P. Kruskal, Kevin P. McAuliffe, Larry Rudolph and Marc Snir, The NYU Ultracomputer, Designing an MIMD shared memory parallel computer, IEEE Transactions on Computers C-32(2), 1983
    locator: pages 175 to 189 (the fetch-and-add operation, and combining of concurrent fetch-and-adds in the network)
  - paper: doi:10.1145/114005.102808
    title: Maurice Herlihy, Wait-free synchronization, ACM Transactions on Programming Languages and Systems 13(1), 1991
    locator: pages 124 to 149 (read-modify-write operations; fetch-and-add solves two-process consensus, and read-modify-write operations whose functions commute cannot solve three-process consensus)
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 5 (the read-modify-write operations, the common2 class, and the proof that it cannot solve three-process consensus)
  - paper: doi:10.1109/TC.1987.1676921
    title: Pen-Chung Yew, Nian-Feng Tzeng and Duncan H. Lawrie, Distributing hot-spot addressing in large-scale multiprocessors, IEEE Transactions on Computers C-36(4), 1987
    locator: pages 388 to 395 (the software combining tree that spreads the accesses to one hot counter)
  - url: "https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html"
    title: Intel 64 and IA-32 Architectures Software Developer's Manual
    locator: Volume 2 (instruction set reference), the instruction XADD with the LOCK prefix
---

Fetch-and-add is an atomic instruction. FAA$(a, d)$ adds $d$ to the word at address $a$ and returns the value that the word had before, in one indivisible step. With $d = 1$ it is fetch-and-increment, which hands out distinct numbers: tickets, slots in an array, or positions in a queue. Gottlieb et al. (1983) made it the central operation of the NYU Ultracomputer. In the [consensus hierarchy](/consensus-number/) it has consensus number 2: it solves consensus for two processes, as this page proves, but not for three (Herlihy 1991).

## In plain words

Think of the ticket machine at a bakery. Each customer pulls a ticket and gets the next number. Two customers never get the same number, even if they pull at the same moment, because the machine gives out one ticket at a time.

Fetch-and-add is that machine in memory. A thread asks the memory to add one to a counter and to tell it the value from before the addition. Each thread gets a different value, and no update is lost. A plain read followed by a write cannot do this: two threads can read the same value and both write the same result.

## The idea

**Notation and model.** $n$ is the number of processes, $p$ and $q$ are processes, and $i, j$ are indices. Processes are asynchronous and can crash between steps. Memory is sequentially consistent, and each read, write and FAA is one atomic step.

**Semantics.**

```text
FAA(a, d):          ▷ one atomic step
    old := M[a]
    M[a] := old + d
    return old
```

It is a [read-modify-write](/read-modify-write/) operation with the function $f(x) = x + d$. Related forms are atomic increment without a result, fetch-and-or, fetch-and-and and fetch-and-xor. In hardware: `LOCK XADD` on x86, `LDADD` in the Armv8.1 Large System Extensions (and an `LDXR`/`STXR` loop before them), and `fetch_add` on `std::atomic` in C++. A [CAS loop](/compare-and-swap/) can also compute FAA, but it is only lock-free, while the instruction is one step and so wait-free.

**Two-process consensus.** Two processes, 0 and 1, each start with a value and must decide on one of the two values, with the same decision for both, in a bounded number of their own steps (wait-free). Shared: a word $x = 0$ and two registers $\mathit{prop}[0]$ and $\mathit{prop}[1]$.

```text
DECIDE(p, v):                      ▷ p is 0 or 1
F1  prop[p] := v
F2  r := FAA(x, 1)
F3  if r = 0: return v
F4  return prop[1 − p]
```

*Proof.* Each process takes at most 3 steps, so the protocol is wait-free. Exactly one FAA returns 0, the first one to run, because the value of $x$ only grows. Call that process the winner $w$; it returns its own value $v_w$ at F3. The other process $\ell$ gets $r = 1$ and returns $\mathit{prop}[w]$. The winner wrote $\mathit{prop}[w]$ at F1 before its FAA at F2, and its FAA came before the FAA of $\ell$, which comes before the read at F4. So the read returns $v_w$. Both processes that decide return $v_w$ (agreement), and $v_w$ is an input (validity). A crash only removes decisions, so the argument holds when a process stops at any point. $\square$

**Not three processes.** Herlihy (1991) proved that no wait-free protocol solves consensus for three processes with any number of FAA words and registers. The proof is cited here and only sketched. Suppose a protocol exists. A valence argument, as on the [registers page](/registers-have-consensus-number-one/), gives a *critical* state $s$: the decision is still open, but the next step of $p$ fixes it to one value and the next step of $q$ fixes it to the other. If the two steps are on different words, or one is a read, a third process can not tell the two orders apart, as in the register proof. If both are FAA on the same word, then $s \cdot p \cdot q$ and $s \cdot q \cdot p$ leave the same memory, because addition commutes. Only $p$ and $q$ know the order. The third process $r$, run alone from either state, sees the same thing and decides the same value, although one state is fixed to each value. This is a contradiction. The step that needs a third process is the last one: with only two processes, nobody is left who can not tell.

So FAA sits at level 2 with [test-and-set](/test-and-set/), swap, queues and stacks. The general result for any read-modify-write whose functions commute or overwrite each other is on the [read-modify-write](/read-modify-write/) page.

**Contention.** All FAA calls on one word go through one cache line, so they run one at a time. Under heavy contention the counter is a hot spot. The Ultracomputer combined concurrent FAAs to the same address inside the network: two requests FAA$(a, d_1)$ and FAA$(a, d_2)$ that meet at a switch go on as one FAA$(a, d_1 + d_2)$, and the reply $v$ is split into $v$ and $v + d_1$. Yew, Tzeng and Lawrie (1987) did the same in software with a [combining tree](/combining-tree/). The results are a [prefix sum](/prefix-sums/) of the increments.

## Examples

All numbers come from the tests in the implementation folder, which run the interleaving explorer over every schedule.

**Two-process consensus.** With inputs a and b, the explorer finds 12 reachable states, 2 of them final. In every state, the processes that have decided agree on an input value, and no process takes more than 3 steps. The same holds for the inputs (a, a), (b, a) and (b, b).

**A three-process attempt.** The natural extension lets the FAA that returns 0 win, and lets a later process guess the winner as the lowest id that has proposed. The explorer finds a bad run at once: process 0 writes a, process 1 writes b, process 1 does FAA and gets 0 (so it decides b), process 0 does FAA and gets 1, reads $\mathit{prop}[0] = $ a and decides a. A process that gets 1 or 2 knows that it lost, but not to whom. The theorem says that no cleverer rule helps. A program can find a bad run of one protocol, but it cannot prove that every protocol fails.

**Tickets.** Four processes each take one ticket with FAA on a shared counter. In every interleaving they get the numbers 0, 1, 2 and 3, each exactly once. The 24 final states are the 24 ways to hand out the tickets.

## Where it is used

- The [ticket lock](/ticket-lock/): FAA on `next` gives a ticket, and a process waits until `serving` equals its ticket. The lock is first come first served. All waiters read the same word `serving`, so each release makes every waiter miss in its cache; in the cache-coherent model, one passage can cost $\Theta(n)$ remote memory references in total (see [RMR complexity](/rmr-complexity/)).
- Counters and statistics, reference counts that only need to go up and down, and the counter of a [barrier](/barrier-synchronization/).
- Array-based queues: the [Herlihy and Wing queue](/herlihy-wing-queue/) takes a slot index with fetch-and-increment, and many fast queues take head and tail positions with FAA instead of a CAS loop, so that each process gets a slot in one step.
- Parallel loops: a shared index handed out with FAA gives each thread the next chunk of work (self-scheduling).
- [Combining trees](/combining-tree/) and [counting networks](/counting-network/) spread the load of one shared counter.

## References
