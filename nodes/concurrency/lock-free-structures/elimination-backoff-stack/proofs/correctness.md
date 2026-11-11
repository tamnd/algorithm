---
title: The elimination back-off stack is linearizable and lock-free
proves: [correctness, linearizability, progress]
status: full
---

We use the pseudocode of the page, with the model of the page: asynchronous processes that may crash, atomic read, write and CAS, sequential consistency, and nodes that are not reused while a process holds them. TRYPUSH and TRYPOP are single passes of the Treiber loops, so the facts proved for the [Treiber stack](/treiber-stack/) hold for the central stack: each successful CAS on `top` changes the list of `top` exactly as one push or one pop, a TRYPOP that returns EMPTY read NULL in a state where the list was empty, and no other step changes that list.

**Lemma 1 (the cell protocol).** Consider one cell. (a) The cell goes from FREE to WAITING only by a CAS at X3, whose process we call the owner of this phase. (b) While the phase lasts, only the owner writes FREE into the cell, and at most one CAS at X9 changes it from WAITING to BUSY. (c) The phase ends when the owner writes FREE at X6 or X8, or its CAS at X7 succeeds; in the first two cases exactly one CAS at X9 succeeded during the phase, and in the third case none did.

*Proof.* The steps that write a cell are the CASes at X3, X7 and X9 and the writes at X6 and X8. The CAS at X3 expects FREE, the CAS at X9 expects WAITING, and the CAS at X7 expects (mine, WAITING), where mine is the owner's item. The writes at X6 and X8 are done only by the process that succeeded at X3, so only by the owner. During a phase the cell is not FREE until the owner frees it, so no CAS at X3 succeeds, and there is no second owner. After one CAS at X9 succeeds, the state is BUSY and stays BUSY until the owner writes FREE; so a second CAS at X9 in the same phase fails. The owner leaves its wait loop at X6 only after it reads BUSY, which needs a successful X9. If the owner's CAS at X7 succeeds, the cell was still WAITING with its item, so no X9 succeeded. If it fails, the cell was not (mine, WAITING), and as only X9 can change it in the phase, X9 succeeded; the owner then reads the partner's item at X8 and frees the cell. ∎

So each successful CAS at X9 pairs two operations, the owner $o$ and the partner $a$, and each one gets the item of the other: $a$ returns the owner's item at X10, and $o$ reads the partner's item at X6 or X8, because nothing but the owner's write changes the cell after X9. We call the pair an *elimination* when one of them is a push and the other is a pop. When both are pushes or both are pops, neither one returns at L6 or L13 (a push returns only if it got POP, and a pop returns only if it did not get POP), so both go on to the next loop iteration with no effect on any shared object except the cell, which is free again.

**Theorem (linearizability).** Each history of the elimination back-off stack is linearizable.

*Proof.* Choose a linearization point for each operation that returns, and for each pending operation that has already had its effect:

- a push or pop that returns after a successful CAS on `top` in TRYPUSH or TRYPOP: that CAS;
- a pop that returns EMPTY: the read of `top` in TRYPOP that returned NULL;
- a push and a pop that are eliminated by one successful CAS at X9: that CAS, with the push placed just before the pop.

Each operation that returns uses exactly one of these: it returns at L3, L6, L10 or L13, and each case names one step. A pending operation is given its point if it has made a successful CAS on `top`, or if it took part in an elimination; otherwise it is dropped. Each point lies between the invocation and the response of its operation. For the eliminated pair this holds because the CAS at X9 is a step of the partner, which is in progress, and the owner returns only after it reads BUSY (at X6) or fails at X7, both after the CAS at X9; so the owner is in progress too. So the order of these points respects real time.

Now apply the operations to a sequential stack in this order. Between two consecutive points on the central stack the list of `top` does not change, so the Treiber argument gives the right results for these operations. An eliminated pair push$(v)$, pop is placed with nothing between them: push$(v)$ puts $v$ on top, and the pop then removes $v$ and returns it, which is the value the pop actually returns (Lemma 1). The state after the pair equals the state before it, and the list of `top` did not change at the step X9. So, by induction on the points, the sequential stack has, after each point, the same content as the list of `top`, and each operation returns the same value as in the run. ∎

**Theorem (lock-freedom).** In each infinite run in which some process takes infinitely many steps, infinitely many operations complete.

*Proof.* One loop iteration of PUSH or POP takes at most $4 + 2T + 4$ steps: one TRYPUSH or TRYPOP, and at most $T$ outer and $T$ inner iterations of EXCHANGE plus the steps of X7 and X8. Assume that after some time no operation completes, while a process $p$ takes infinitely many steps. Then $p$ runs infinitely many iterations, and in each one its CAS on `top` fails, so some other process did a successful CAS on `top` after $p$ read it. Each successful CAS on `top` completes the try of an operation, which then returns within one more step if its process keeps running. A process starts a new operation only after the current one returns, so after the given time each process makes at most one successful CAS on `top`. That is at most $n$ successful CASes, but $p$ needs infinitely many. Contradiction. ∎
