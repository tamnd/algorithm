---
tag: 3VECZJ
kind: concept
slug: compare-and-swap
name: Compare-and-swap (CAS)
aliases:
- CAS
- compare-and-set
- compare-and-exchange
area: concurrency/lock-free-structures
level: intro
summary: An atomic instruction. It writes a new value to a memory word only if the word still holds an expected value, and it reports whether it did.
prereqs: [race-condition]
see_also: [load-linked-store-conditional, aba-problem, cas-has-infinite-consensus-number, double-compare-and-swap, multi-word-cas, fetch-and-add, read-modify-write, lock-freedom]
sources:
  - paper: doi:10.1145/114005.102808
    title: Maurice Herlihy, Wait-free synchronization, ACM Transactions on Programming Languages and Systems 13(1), 1991
    locator: pages 124 to 149 (compare-and-swap solves consensus for any number of processes)
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 5 (the compareAndSet operation and its consensus number), Chapter 10 (the ABA problem), Chapter 11 (the lock-free stack)
  - url: "https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html"
    title: Intel 64 and IA-32 Architectures Software Developer's Manual
    locator: Volume 2A, the instructions CMPXCHG and CMPXCHG8B/CMPXCHG16B, and the LOCK prefix
  - url: "https://developer.arm.com/documentation/ddi0487/latest"
    title: Arm Architecture Reference Manual for A-profile architecture
    locator: the exclusive instructions LDXR and STXR, and the CAS instructions of the Large System Extensions (Armv8.1)
  - url: "https://eel.is/c++draft/atomics.types.operations"
    title: Working Draft, Programming Languages, C++, [atomics.types.operations]
    locator: compare_exchange_weak and compare_exchange_strong (spurious failure of the weak form, and the update of the expected value)
---

Compare-and-swap (CAS) is an atomic instruction on one memory word. CAS$(a, e, v)$ checks whether the word at address $a$ holds the expected value $e$; if so, it writes $v$ and succeeds, and if not, it changes nothing and fails. The check and the write are one indivisible step. CAS is the basic tool of [lock-free](/lock-freedom/) programming: read a word, compute a new value, and install it with CAS only if nobody changed the word in between. Herlihy (1991) showed that CAS has [infinite consensus number](/cas-has-infinite-consensus-number/), so it can build a wait-free version of any shared object for any number of processes.

## In plain words

You want to change a shared number, but other threads may change it at the same time. You read the number, say 5, and you compute the new value, 6. Then you tell the memory: "put 6 here, but only if it still says 5". If another thread wrote 7 in the meantime, the memory refuses, and you start again with 7.

The memory does the check and the write in one go, so no other thread can slip in between them. This is compare-and-swap. A loop of read, compute and compare-and-swap is the most common pattern in programs that do not use locks.

## The idea

**Notation and model.** $n$ is the number of processes and $p, q$ are processes. Processes are asynchronous and can crash between steps. Memory is sequentially consistent unless this page says otherwise, and CAS is one atomic step.

**Semantics.** There are two common forms. Both are one atomic step.

```text
CAS(a, e, v):             ▷ compare-and-set: returns a boolean
    if M[a] = e: M[a] := v; return true
    else: return false

CMPXCHG(a, e, v):         ▷ compare-and-exchange: returns the old value
    old := M[a]
    if old = e: M[a] := v
    return old
```

The forms are equivalent: CAS succeeded exactly when CMPXCHG returned $e$, and a failed CAS can be followed by a read when the caller needs the value (the read then may see a newer value, which is fine for a retry loop). CMPXCHG is more convenient, because the loop gets the current value for free.

**The CAS loop.** Any update $x \mapsto f(x)$ of one word becomes atomic with this loop:

```text
UPDATE(a, f):
    loop:
        old := read(a)
        if CAS(a, old, f(old)): return old
```

The successful CAS is the [linearization point](/linearization-point/). A CAS fails only if another process changed the word after the read, and that change came from a successful CAS of another update. So each failure of one process goes with a success of another, and the loop is [lock-free](/lock-freedom/): in any infinite run, infinitely many updates finish. It is not wait-free: one process can fail for ever while the others keep succeeding. With $n$ processes that each run one update, a process needs at most $n$ attempts, since each of the other $n-1$ processes can make it fail at most once.

**Why it is strong.** A write, a swap or a [fetch-and-add](/fetch-and-add/) makes the same change whatever the word holds, so a later process can always overwrite or shift what an earlier one did. CAS changes the word only if it holds the expected value, so the first process can install a value that no later CAS on the empty value can replace. With it, $n$ processes reach consensus: each proposes with CAS(decision, empty, my value), and the first CAS wins. Registers have [consensus number 1](/registers-have-consensus-number-one/), fetch-and-add has 2, and CAS has infinity. See [consensus number](/consensus-number/).

**The ABA problem.** CAS compares values, not histories. If the word went from A to B and back to A between the read and the CAS, the CAS succeeds, although the state that the process saw is gone. In a [Treiber stack](/treiber-stack/) that reuses nodes, this corrupts the list. This is the [ABA problem](/aba-problem/). The usual fixes are a version counter next to the pointer ([tagged pointers](/tagged-pointers/), which need a double-width CAS), safe memory reclamation such as [hazard pointers](/hazard-pointers/), or [load-linked/store-conditional](/load-linked-store-conditional/), which fails after any write.

**Hardware.**

- x86: `LOCK CMPXCHG` compares the accumulator (EAX or RAX) with the destination. If they are equal, it stores the source and sets the zero flag; if not, it loads the destination into the accumulator and clears the flag. So it is the CMPXCHG form. `CMPXCHG8B` and `CMPXCHG16B` do the same on two adjacent words (8 or 16 bytes). That is a *double-width* CAS on one wide word, not the [double-compare-and-swap](/double-compare-and-swap/) of two separate words. A locked instruction is also a full memory fence on x86.
- Arm: Armv8.0 has no CAS instruction. A CAS is a loop of `LDXR` (load exclusive) and `STXR` (store exclusive), which is [load-linked/store-conditional](/load-linked-store-conditional/). Armv8.1 added the Large System Extensions with `CAS`, `CASA`, `CASL` and `CASAL` (the letters add acquire and release ordering), and `CASP` for a pair of registers.
- POWER and RISC-V use LL/SC pairs (`lwarx`/`stwcx.` and `lr`/`sc`), and a compiler turns a CAS into a short loop around them.

**C and C++.** `std::atomic<T>` has two forms. `compare_exchange_strong(expected, desired)` fails only if the value differs from `expected`. `compare_exchange_weak` may also fail *spuriously*, when the values are equal, because on an LL/SC machine it is a single LL/SC attempt that can lose its reservation. Both forms write the current value into `expected` when they fail, so a loop needs no extra read. Use the weak form inside a retry loop, and the strong form when a failure is acted on directly (for example, in a one-shot consensus). Both take a memory order for success and one for failure; the default is `seq_cst`. The failure order cannot be `release` or `acq_rel`, because a failed CAS does not write. The comparison is on the object representation (its bytes), so padding bytes in a struct can make a CAS fail although the fields are equal.

## Examples

All numbers come from a small script that runs the interleaving explorer of the [linearization point](/linearization-point/) page over every schedule.

**Lost updates without CAS.** Two processes each increment a shared counter once by a read and then a write. Of the 6 possible interleavings, 4 end with the counter at 1, not 2: both read 0, and both write 1. With three processes, only 6 of the 90 interleavings end at 3, 36 end at 2, and 48 end at 1.

**The CAS loop is correct.** With the CAS loop instead, all 6 interleavings of two processes end at 2, and all 498 complete schedules of three processes end at 3. With two processes that each increment twice, all 226 complete schedules end at 4.

**Retries.** In those runs the largest number of attempts (one read and one CAS each) that one process needs for one increment is 2 with two processes and 3 with three processes, which matches the bound of $n$ attempts for one update each. With repeated updates there is no bound: a process can fail for ever while the others keep succeeding. The [lock-freedom](/lock-freedom/) page runs such a schedule.

**A one-shot decision.** Process $p$ runs CMPXCHG(d, empty, $v_p$). The first process to run it writes its value; each later process gets that value back. All processes return the same value, and it is a proposed value. This is the whole consensus protocol of the [CAS consensus page](/cas-has-infinite-consensus-number/).

## Where it is used

- Lock-free data structures: the [Treiber stack](/treiber-stack/), the [Michael and Scott queue](/michael-scott-queue/), the [Harris linked list](/harris-linked-list/), [split-ordered lists](/split-ordered-list/) and [lock-free skip lists](/lock-free-skip-list/).
- Spin locks: a lock is acquired by CAS(lock, free, mine). A [test-and-set](/test-and-set/) lock is the special case with a fixed new value.
- Reference counts, statistics counters and state machines of one word, through the CAS loop.
- Building larger atomic steps: [multi-word CAS](/multi-word-cas/) is built from single-word CAS with descriptors, and [load-linked/store-conditional](/load-linked-store-conditional/) can be built from CAS.
- The [universal construction](/universal-construction/) uses CAS-based consensus to make any sequential object wait-free.

## References
