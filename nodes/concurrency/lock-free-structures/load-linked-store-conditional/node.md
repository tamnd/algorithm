---
tag: 5J33C1
kind: concept
slug: load-linked-store-conditional
name: Load-linked/store-conditional (LL/SC)
aliases:
- LL/SC
- load-reserved/store-conditional
- load-exclusive/store-exclusive
area: concurrency/lock-free-structures
level: intro
summary: A pair of instructions. LL reads a word and links to it; SC writes the word only if nobody wrote it since the LL. It avoids ABA in theory, but hardware LL/SC is weaker.
prereqs: [compare-and-swap]
see_also: [compare-and-swap, aba-problem, tagged-pointers, read-modify-write, consensus-number, double-compare-and-swap, multi-word-cas, treiber-stack]
sources:
  - paper: doi:10.1145/259380.259442
    title: Mark Moir, Practical implementations of non-blocking synchronization primitives, PODC 1997
    locator: pages 219 to 228 (LL/SC and VL built from CAS with tags, in constant time)
  - paper: doi:10.1145/872035.872078
    title: Prasad Jayanti and Srdjan Petrovic, Efficient and practical constructions of LL/SC variables, PODC 2003
    locator: pages 285 to 294 (wait-free LL/SC from single-word CAS with bounded tags)
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 5 (synchronization operations and consensus numbers), Chapter 10 (the ABA problem, and load-linked/store-conditional as a way to avoid it)
  - url: "https://developer.arm.com/documentation/ddi0487/latest"
    title: Arm Architecture Reference Manual for A-profile architecture
    locator: the synchronization and semaphores chapter (LDXR, STXR, CLREX, the exclusive monitors and the Exclusives Reservation Granule)
  - url: "https://riscv.org/specifications/ratified/"
    title: The RISC-V Instruction Set Manual, Volume I, Unprivileged Architecture
    locator: the A extension, load-reserved/store-conditional (LR and SC), and the constrained LR/SC loops that are guaranteed to make progress
---

Load-linked/store-conditional (LL/SC) is a pair of atomic instructions on one memory word. LL$(a)$ reads the word and sets a *link* (a reservation) of the process on it. SC$(a, v)$ writes $v$ and succeeds only if no other write to the word happened since the last LL of this process; otherwise it fails and writes nothing. Because SC fails after any write, even one that put back the same value, ideal LL/SC does not have the [ABA problem](/aba-problem/) of [compare-and-swap](/compare-and-swap/). Real processors (Arm, POWER, RISC-V, and earlier MIPS and Alpha) give a weaker LL/SC: an SC can fail for no visible reason, a process holds only one link, and the link covers a whole block of memory.

## In plain words

You read a shared value and get a ticket with it. Later you try to write a new value, and you show your ticket. The memory accepts the write only if nobody wrote to that spot since you got your ticket. If somebody did, your ticket is no longer valid, the write fails, and you read again.

Compare-and-swap checks the value. This pair checks whether there was any write at all. So it notices a change even if the value was changed and then changed back. On real chips the ticket is fragile: it can be lost because of an interrupt or a write nearby, so the code must always be ready to try again.

## The idea

**Notation and model.** $n$ is the number of processes; $p$ and $q$ are processes. Processes are asynchronous and can crash between steps. Memory is sequentially consistent. Each operation below is one atomic step.

**Ideal semantics.** Each word has a set of linked processes.

```text
LL(p, a):      links[a] := links[a] ∪ {p};  return M[a]
SC(p, a, v):   if p ∈ links[a]: M[a] := v; links[a] := ∅; return true
               else: return false
VL(p, a):      return p ∈ links[a]          ▷ validate: is my link still good?
```

Any successful write to $a$ (an SC, or a plain write) clears all links on $a$. This ideal form is what theory papers mean by LL/SC. Like CAS, it has infinite [consensus number](/consensus-number/): each process does LL on a decision word, and if it is empty, an SC of its own value; then all processes read the word, and the first successful SC fixes the value for all.

**Why ideal LL/SC avoids ABA.** Suppose $p$ does LL and reads A, then $q$ changes the word to B and back to A, then $p$ does SC. A CAS of $p$ with expected value A would succeed, because it only compares values. The SC of $p$ fails, because $q$'s writes cleared $p$'s link. In a [Treiber stack](/treiber-stack/), a pop with LL on `top` and SC of the next node is safe against ABA for this reason, as long as each link lasts from the read of `top` to the SC.

**LL/SC in hardware.** Processors give LL/SC with these limits.

- *Spurious failure.* SC may fail although no other process wrote the word: after an interrupt or a context switch, when the cache line is evicted, or after some other memory access by the same processor. The code must retry, and in theory a spurious failure can repeat for ever, so lock-freedom needs a hardware guarantee of progress.
- *One link per processor, no nesting.* A processor has one reservation. An LL on a second address drops the first link. So you cannot LL two words and then SC both: LL/SC does not give a [double-compare-and-swap](/double-compare-and-swap/).
- *Reservation granule.* The hardware tracks a block, not a word. On Arm it is the Exclusives Reservation Granule, whose size depends on the implementation and is often one cache line. A write by another processor to any address in the block breaks the link. So false sharing can make SC fail.
- *Short code only.* Between LL and SC, the code must be short and simple. RISC-V promises eventual success only for *constrained* LR/SC loops: a short loop of base integer instructions with no other loads, stores or system instructions inside. The Arm manual also limits what may come between `LDXR` and `STXR`. A Treiber pop must load `top.next` between its LL and its SC. That load is outside the constrained form, so the hardware may fail the SC every time, and progress is no longer promised. A link that must last across arbitrary code is exactly what hardware does not give.

Names: `LDXR`/`STXR` on Arm (with `CLREX` to drop a link), `lwarx`/`stwcx.` on POWER, `lr`/`sc` on RISC-V, `ll`/`sc` on MIPS, and `ldl_l`/`stl_c` on Alpha.

**CAS from LL/SC.** A compiler builds CAS from LL/SC with a short loop: LL the word; if it differs from the expected value, return false; otherwise SC the new value, and if the SC failed, start again. C++ `compare_exchange_weak` is a single try of this loop and may fail spuriously; `compare_exchange_strong` is the full loop. The result is plain CAS: it has the ABA problem again.

**LL/SC from CAS.** In the other direction, put a tag next to the value. The word $X$ holds a pair (value, tag).

```text
LL(p):      link[p] := read(X);  return link[p].value
SC(p, v):   return CAS(X, link[p], (v, link[p].tag + 1))
VL(p):      return read(X) = link[p]
```

*Why it is correct.* Take the read in LL and VL, and the CAS in SC, as [linearization points](/linearization-point/). A successful SC finds the tag of $X$ equal to the tag of its link and writes that tag plus one. So the tags of the successive values of $X$ go 0, 1, 2, and so on, and $X$ never holds a pair twice. Hence, at the time of an SC or VL of $p$, $X = \mathit{link}[p]$ exactly when no SC has succeeded since the LL of $p$, which is the ideal rule with links. (A plain write to $X$ must also raise the tag.)

This simple version needs a tag that never wraps around. Moir (1997) gave constant-time LL/SC and VL from CAS in this style, with a tag of fixed size in the same word; a fixed-size tag is safe only if it cannot wrap around while a process is between its LL and its SC. Jayanti and Petrovic (2003) gave wait-free constant-time constructions that need no such assumption, at the cost of extra space for each process. The implementation of this page uses the simple version with Python integers as tags, and says so.

## Examples

All numbers come from the tests in the implementation folder, which check each history with the brute force linearizability checker against the ideal LL/SC specification.

**Every run of LL/SC from CAS.** Two processes each run LL, SC and VL (with values B and C) on a word that starts at A. The explorer finds 20 complete histories, and all are linearizable. With three processes (LL then SC for two of them; VL, LL and SC for the third) it finds 210 histories, all linearizable.

**ABA, caught.** $p$ runs LL and then SC(C). $q$ runs LL, SC(B), LL, SC(A). The schedule is: $p$ does LL and reads A; $q$ runs its four operations, so the value goes A, B, A; then $p$ does SC.

| Step | Process | Operation | $X$ with tags | $X$ without tags |
|---|---|---|---|---|
| 1 | $p$ | LL returns A | (A, 0) | A |
| 2 | $q$ | LL returns A | (A, 0) | A |
| 3 | $q$ | SC(B) succeeds | (B, 1) | B |
| 4 | $q$ | LL returns B | (B, 1) | B |
| 5 | $q$ | SC(A) succeeds | (A, 2) | A |
| 6 | $p$ | SC(C) | fails: (A, 2) is not (A, 0) | succeeds: C |

With the tag, $p$'s SC fails, as ideal LL/SC requires, and the history is linearizable. Without the tag, the SC is a plain CAS on the value, it succeeds, and the checker finds that the history is not linearizable for LL/SC. Over all 15 histories of these two programs, the version without tags gives 2 that are not linearizable.

## Where it is used

- On Arm (before Armv8.1), POWER and RISC-V, every atomic read-modify-write, including CAS and [fetch-and-add](/fetch-and-add/), is an LL/SC loop that the compiler or the C library emits.
- Algorithms from the theory literature are often written with LL/SC, because it avoids ABA. To run them on hardware, you build ideal LL/SC from CAS as above.
- Wait-free and lock-free constructions, such as the [universal construction](/universal-construction/) in some textbook forms, and [multi-word CAS](/multi-word-cas/) variants, use LL/SC or VL as a building block.
- The ABA fixes for plain CAS, such as [tagged pointers](/tagged-pointers/), are the same idea as the tag above: make each write unique.

## References
