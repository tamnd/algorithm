---
tag: BFAFX0
kind: technique
slug: transactional-boosting
name: Transactional boosting
aliases:
- semantic conflict detection
area: concurrency/transactional-memory
level: research
summary: Use a linearizable concurrent object inside transactions by taking an abstract lock before each call and logging the inverse call, so conflicts are found by meaning, not by memory words.
prereqs: [linearizability, transaction, two-phase-locking]
see_also: [open-nested-transactions, lock-free-skip-list, harris-linked-list, fetch-and-add, readers-writer-lock, serializability, transaction-conflict, contention-management]
sources:
  - paper: doi:10.1145/1345206.1345237
    title: "Maurice Herlihy and Eric Koskinen, Transactional boosting: a methodology for highly-concurrent transactional objects, PPoPP 2008, pp. 207 to 216"
    locator: the boosting methodology (abstract locks, inverses, the commutativity condition), the correctness argument, and the boosted set, priority queue and pipeline examples
  - book: "Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020"
    locator: the chapter on transactional programming
  - paper: doi:10.1016/j.scico.2006.05.010
    title: "J. Eliot B. Moss and Antony L. Hosking, Nested transactional memory: model and architecture sketches, Science of Computer Programming 63(2), 2006, pp. 186 to 201"
    locator: open nesting with abstract locks and compensation, the related mechanism inside a TM
---

**Transactional boosting** is a way to use an existing linearizable concurrent object, such as a lock-free skip list set, inside transactions. Each call of the object is guarded by an **abstract lock** chosen so that calls that do not commute always conflict, and each call that changes the object logs its **inverse**. On commit the transaction releases its abstract locks; on abort it runs the inverses, newest first, and then releases them. Herlihy and Koskinen introduced boosting in 2008, so that two transactions that add different keys to a set no longer conflict just because they touch the same memory words.

## In plain words

A software TM finds conflicts by watching memory words. For a shared set, that is too strict: two transactions that add different keys may both write the same tree node or the same size counter, and the TM aborts one of them, though the order of the two additions does not matter.

Boosting finds conflicts by meaning. Before each call, the transaction locks the key it uses; calls on different keys never wait for each other. The call itself runs at once on a good concurrent set, which handles the memory details. If the transaction later fails, it cannot roll back memory words, so it undoes its calls instead: it removes what it added and adds back what it removed.

## When it applies

Boosting needs three things, and gives serializable transactions when all three hold.

- **A linearizable base object.** Each call takes effect at one point in time ([linearizability](/linearizability/)), so the calls of all threads form one sequence.
- **Abstract locks that cover non-commutation.** Two calls *commute* if, from every state, running them in either order gives the same results for both and the same final state. The lock rule must make any two calls that do not commute take conflicting locks. For a set, one exclusive lock per key works: `add(k)`, `remove(k)` and `contains(k)` commute with every call on a different key.
- **Inverses.** For each call $c$ that returned $r$, there is a call $c^{-1}$ that, run right after $c$, restores the state before $c$. The inverse may depend on the result: the inverse of `add(k)` that returned true is `remove(k)`, and an `add(k)` that returned false needs no inverse. The inverse must commute with every call that commutes with $c$; this holds when it takes the same abstract lock.

Boosting does not apply well when every pair of calls conflicts (for example, a stack where every push and pop changes the top), or when an operation has no inverse (output, or freeing memory that others may still read).

## The template

```pseudo id=main
BOOSTED-CALL(T, c)                         ▷ transaction T calls c on the base object
L1  k ← the abstract lock of c
L2  if T does not hold k then
L3      acquire k, or abort T if it stays busy (a timeout)
L4      add k to the locks of T
L5  r ← run c on the linearizable base object
L6  if c with result r changed the abstract state then
L7      push the inverse of c for result r onto the undo log of T
L8  return r

COMMIT(T)
L9  release every lock of T

ABORT(T)
L10 for each call d in the undo log of T, newest first do
L11     run d on the base object
L12 release every lock of T
```

Abstract locks are held from the first call that needs them to the end of the transaction, as in [two-phase locking](/two-phase-locking/). Herlihy and Koskinen use timeouts on lock acquisition to break deadlocks: a transaction that cannot get a lock in time aborts and releases its own. The calls on the base object run at once and are not part of the read or write set of any underlying STM, so a boosted object can be combined with ordinary transactional memory or used alone.

*Example.* The set holds $\{2\}$. $T_0$ runs `add(1); remove(2)` and then aborts; $T_1$ runs `contains(1); add(2)`.

| step | $T_0$ | $T_1$ | set | locks |
|---|---|---|---|---|
| 1 | lock 1; `add(1)` = true; log `remove(1)` | | $\{1, 2\}$ | 1: $T_0$ |
| 2 | | lock 1 is busy: abort, wait | $\{1, 2\}$ | 1: $T_0$ |
| 3 | lock 2; `remove(2)` = true; log `add(2)` | | $\{1\}$ | 1, 2: $T_0$ |
| 4 | abort: `add(2)`, then `remove(1)`; release | | $\{2\}$ | none |
| 5 | | lock 1; `contains(1)` = false; lock 2; `add(2)` = false; commit | $\{2\}$ | none |

$T_1$ never sees key 1, which $T_0$ added but never committed. Without the abstract locks, step 2 could run `contains(1)` and return true; without the undo log, the set would end as $\{1\}$.

### Why it is correct

**Claim.** Under the three conditions, every execution of boosted transactions on one object is equivalent to a serial execution of its committed transactions, in the order in which they finish, with the same results for every call and the same final state.

*Proof.* By linearizability, treat each call, including each inverse, as one atomic step, so the execution is a sequence of calls. Let $T$ be the transaction that finishes first (commits, or ends its abort). Take any call $c$ of $T$ and any call $d$ of another transaction $U$ that comes before $c$ in the sequence. $U$ took the lock of $d$ before $d$ and still holds it when $c$ runs, because $U$ finishes after $T$. $T$ took the lock of $c$ before $c$. The two locks are held at the same time, so they do not conflict, and by the lock rule $c$ and $d$ commute. Swapping two adjacent commuting calls keeps every result and the final state. So we can move all calls of $T$, keeping their order, to the front of the sequence.

If $T$ committed, it now runs alone first, and the rest is an execution of the other transactions from the state that $T$ left; the claim follows by induction on the number of transactions. If $T$ aborted, its block is $c_1 c_2 \cdots c_m$ followed by the inverses of the calls that changed the state, newest first. Calls that changed nothing can be dropped. Then $c_m$ is directly followed by $c_m^{-1}$, which restores the state before $c_m$; remove both and repeat. The block vanishes, and the rest of the execution is unchanged, so again the claim follows by induction. $\blacksquare$

The same argument shows that an aborted transaction saw a consistent state up to its abort (its calls ran first, from a state that the committed transactions explain), which is the abstract form of [opacity](/opacity/).

## Classic examples

- **Sets and maps.** Boost a [lock-free skip list](/lock-free-skip-list/) or a list based on the [Harris linked list](/harris-linked-list/) with one lock per key. Transactions that touch different keys run in parallel, while an STM would make them conflict on shared nodes. This is the main example of Herlihy and Koskinen.
- **Priority queue.** Calls of `add` commute with each other (in terms of the set of elements), but not with `removeMin`. Herlihy and Koskinen use a [readers-writer lock](/readers-writer-lock/) as the abstract lock: `add` takes it in shared mode and `removeMin` in exclusive mode. The inverse of `add(x)` must remove that particular element.
- **Unique identifiers.** A counter that hands out unique IDs with [fetch-and-add](/fetch-and-add/) needs no abstract lock at all if callers only need the IDs to be distinct: all calls commute in that weaker sense, and the inverse is empty (an unused ID is harmless).
- **Open nesting.** An [open nested transaction](/open-nested-transactions/) with abstract locks and a compensating action is the same pattern, built into a TM: the child is the call, and the compensation is the inverse.

## Variations

- **Lock modes.** Use readers-writer abstract locks when read-only calls commute with each other, or locks on ranges for range queries.
- **Disposable calls.** Some calls, such as freeing a node, need not happen at once; they can be delayed to commit, which avoids the need for an inverse. Herlihy and Koskinen discuss calls of this kind.
- **Optimistic variants.** Later work replaces the pessimistic abstract locks with validation at commit, or stores per-key metadata in the map itself (transactional predication, Bronson et al., 2010), to cut the cost of the lock table.
- **Mixed with an STM.** A transaction can use boosted objects and plain transactional memory together; the STM handles words, and boosting handles the objects. The abort of the STM must call the boosting undo log.

## Pitfalls

- **Locks that miss a non-commuting pair.** If two calls that do not commute can hold their locks at the same time, the proof fails, and the implementation for this page finds a non-serializable run when the locks are dropped. Check commutativity for all states, including the results of the calls.
- **Inverses that ignore the result.** The inverse of `add(k)` is `remove(k)` only if the `add` returned true. A blind inverse removes a key that another committed transaction had added.
- **Deadlock between abstract locks.** Two transactions that lock keys in opposite orders wait for each other. Use timeouts and abort, or order the keys.
- **Mixing levels.** If a transaction also reads the internal memory of the base object through the STM, the conflicts at the word level come back, and the inverses may undo changes that other transactions depend on.
- **Side effects of aborted transactions.** Between a call and its inverse, the effect of the call is in the base object. Code that reads the object without boosting (outside transactions) can see it; boosting gives isolation only to transactions that use the abstract locks.

## Exercises

1. Show that `add(k)` and `contains(j)` commute for $j \ne k$, and that `add(k)` and `contains(k)` do not, by giving a state where the two orders give different results.
2. For a FIFO queue with `enqueue` and `dequeue`, find which pairs of calls commute. Design abstract locks that allow an enqueue and a dequeue to run in parallel when the queue is long enough. *Hint.* The answer depends on the state; consider locks on the head and the tail.
3. Prove that if $c^{-1}$ takes the same abstract lock as $c$, then $c^{-1}$ commutes with every call that commutes with $c$, for the set with one lock per key.
4. Give an execution of three transactions on a boosted set without abstract locks in which every transaction commits but no serial order explains the results.
5. A counter has `increment()` and `read()`. Which pairs commute? Give an abstract lock rule and the inverse of `increment`.

## References
