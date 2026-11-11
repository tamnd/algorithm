---
tag: HJDC4M
kind: algorithm
slug: pass-the-buck
name: Pass the buck
aliases: [PTB, Herlihy-Luchangco-Moir pass the buck]
area: concurrency/memory-reclamation
level: research
summary: Threads post guards on the pointers they use. A wait-free Liberate returns the retired values that no guard traps, and hands each trapped value to its guard for a later Liberate.
solves: [safe-memory-reclamation]
complexity:
  vars: {n: the number of processes, K: the number of guards per process, G: the number of guards, R: the number of values passed to one Liberate}
  space: {guards: Θ(G), unfreed_garbage: O(n R + n G)}
  steps: {post_guard: O(1), liberate: O(G + R)}
properties: {robust: true, bounded_garbage: true, wait_free_liberate: true, per_read_cost: true, needs_double_width_cas: true}
history:
  year: 2002
  people: [Maurice Herlihy, Victor Luchangco, Paul Martin, Mark Moir]
  note: Herlihy, Luchangco and Moir posed the repeat offender problem at DISC 2002, and with Martin published the full pass the buck algorithm and its proof in ACM TOCS in 2005.
prereqs: [safe-memory-reclamation, hazard-pointers]
see_also: [treiber-stack, michael-scott-queue, lock-free-reference-counting, wait-freedom, hazard-eras]
sources:
  - paper: doi:10.1145/1062247.1062249
    title: Maurice Herlihy, Victor Luchangco, Paul Martin and Mark Moir, Nonblocking memory management support for dynamic-sized data structures, ACM Transactions on Computer Systems 23(2), 2005, pages 146-196
    locator: Section 2.3 (PostGuard and Liberate), Section 2.5 (the guarantees of Liberate), Figure 9 and Section 6.1 (the Pass The Buck code and the handoff), Figure 10 (why three failed CAS steps are enough), Section 6.2 (wait freedom and the bound after failures), Figure 11 (the lock-free variant)
  - paper: "Maurice Herlihy, Victor Luchangco and Mark Moir, The repeat offender problem, a mechanism for supporting dynamic-sized lock-free data structures, DISC 2002, LNCS 2508, pages 339-353"
---

Pass the buck, or PTB, is a [safe memory reclamation](/safe-memory-reclamation/) method by Maurice Herlihy, Victor Luchangco, Paul Martin and Mark Moir. A thread that is about to use a pointer posts it in a guard, and then checks that the pointer is still in the structure, as with [hazard pointers](/hazard-pointers/). A thread that wants to free some retired nodes calls Liberate with their set. Liberate looks at every guard once. If a guard holds a value of the set, Liberate does not wait for it: it moves the value into a handoff word of that guard, and takes out the value that was there before, which is no longer guarded. Liberate then returns the rest, and the caller frees them. So Liberate is wait free, and the responsibility for a guarded value passes to the next Liberate that finds the guard free of it.

## In plain words

A library lends books, and readers put a card with the book title in their own card slot while they read it.

When the library wants to throw away old books, a clerk takes the pile and walks past all the card slots once.

If a slot shows a book from the pile, the clerk does not wait for the reader. The clerk puts that book in a box under the slot and takes out the book that was in the box before, which that reader no longer has, and adds it to the pile.

At the end of the walk, the clerk throws away the pile. A book in a box waits there until the next clerk sees that the reader has put it down.

## The problem

[Safe memory reclamation](/safe-memory-reclamation/) for lock-free structures such as the [Treiber stack](/treiber-stack/) and the [Michael and Scott queue](/michael-scott-queue/). The paper calls it the repeat offender problem: a value is **trapped** by a guard if the guard has held it since before the value was passed to Liberate, and Liberate must never return a trapped value. Hazard pointers solve this with a scan that may keep the guarded nodes in the caller's own list. Pass the buck asks for more: Liberate must be wait free, and a value that stays guarded must not stay with the thread that tried to free it.

The model: $n$ asynchronous processes on a sequentially consistent shared memory with reads, writes and a [compare-and-swap](/compare-and-swap/) on a pair of a value and a version number. There are $G = n K$ guards. Guard $g$ has a word $POST[g]$ and a word $HNDOFF[g] = (val, ver)$. Here each process owns $K$ guards; the paper also lets threads hire and fire guards at run time.

## The algorithm

```pseudo id=main
POST_GUARD(g, p)                     ▷ the client then reads the source again
L1  POST[g] ← p
LIBERATE(S)                          ▷ S is a set of retired values
L2  for each guard g:
L3      h ← HNDOFF[g]; attempts ← 0
L4      v ← POST[g]
L5      if v ≠ nil and v ∈ S then repeat:
L6          if CAS(HNDOFF[g], h, (v, h.ver + 1)) then
L7              S ← S − {v}; if h.val ≠ nil then S ← S ∪ {h.val}; leave the loop
            attempts ← attempts + 1; if attempts = 3 then leave the loop
            h ← HNDOFF[g]; if attempts = 2 and h.val ≠ nil then leave the loop
L8          if POST[g] ≠ v then leave the loop
L9      else if h.val ≠ nil and h.val ≠ v then
L10         if CAS(HNDOFF[g], h, (nil, h.ver + 1)) then S ← S ∪ {h.val}
L11 return S                         ▷ the caller frees every value in S
```

A guard holds one value at a time, so it can trap at most one value, and one handoff word per guard is enough. When Liberate puts $v$ into $HNDOFF[g]$, the value $w$ that it takes out is safe to carry on: Liberate read $POST[g] = v$ after it read $w$ in the word, and the version number shows that $w$ was still there at that time, so $g$ did not guard $w$. An escaping value cannot become trapped again, because a trap needs a post from before the value was retired.

If the CAS at L6 fails again and again, other Liberate calls are working on the same guard. The paper shows that after two failures followed by a non-nil handoff word, or after three failures, some other Liberate saw the guard holding a different value after $v$ was retired, so $g$ does not trap $v$ and Liberate can move on with $v$ still in $S$. L9 and L10 make sure that a value left in a handoff word is picked up by the next Liberate that finds the guard free of it.

## Example

A stack $top \to A \to B \to C$, two processes $p$ and $q$ with guards $p_0, p_1, q_0, q_1$, and $R = 1$: each retire calls Liberate at once.

| step | process | line | action | state after |
|---|---|---|---|---|
| 1 | $p$ | L1 | posts $A$ in $p_0$; reads $top = A$ again | $POST[p_0] = A$ |
| 2 | $q$ | pop | posts $A$ in $q_0$, CAS $top$ from $A$ to $B$, retires $A$ | $top = B$ |
| 3 | $q$ | L2 to L7 | Liberate($\{A\}$): $p_0$ guards $A$, so CAS moves $A$ into the handoff word | $HNDOFF[p_0] = (A, 1)$, $S = \{\}$ |
| 4 | $q$ | L2 to L11 | $q_0$ shows $A$, but $A$ is no longer in $S$; returns the empty set | nothing freed |
| 5 | $p$ | pop | reads $A.next$ safely; its CAS fails; posts $B$ in $p_0$, pops $B$, retires $B$ | $top = C$ |
| 6 | $p$ | L2 to L7 | Liberate($\{B\}$): $p_0$ guards $B$, so CAS puts $B$ in and takes $A$ out | $HNDOFF[p_0] = (B, 2)$, $S = \{A\}$ |
| 7 | $p$ | L11 | returns $\{A\}$; $p$ frees $A$ | $B$ waits in the handoff word |

$B$ waits until a later Liberate finds $p_0$ holding a different value and takes it out at L10. With an immediate free, $A$ is freed at step 2 and the read at step 5 is a use after free. The test finds this run.

## Correctness

The full proof is in proofs/correctness.md. It assumes that a process posts a pointer, reads the source again, and uses the node only if it saw the same pointer and the node was reachable at that read (the stack reads from the root, and the dequeue checks the head again). It also assumes that each node is retired once after its unlink, not linked again, and freed only when Liberate returns it.

- **Single location.** A retired value that Liberate has not returned is in exactly one place: the set of one running Liberate, or one handoff word.
- **Key fact.** When Liberate has passed guards $0$ to $i - 1$, none of these guards traps a value in its set, and a value in $HNDOFF[g]$ is not trapped by a guard below $g$. The failed CAS steps are handled by the argument of Figure 10 in the paper.
- **Safety.** A node that a process uses was posted before it was retired, so its guard traps it, and Liberate does not return it.
- **Bound.** Each set holds at most $R + G$ values and there are $G$ handoff words, so at most $n (R + G) + G$ retired nodes are unfreed.

The test file checks every interleaving of two stack runs and a queue run, seeded random runs, that values are handed off and later freed, two broken versions (a guard posted without the check read, and an L9 that takes a value out of the handoff word while the guard still holds it), an immediate free, and the garbage under a stall.

## Complexity

| measure | value |
|---|---|
| shared space | $2 G$ words; the handoff word holds a value and a version |
| PostGuard | 1 write, plus the check read of the client |
| Liberate | at most 3 CAS steps and $O(1)$ reads per guard: $O(G)$ shared steps, wait free |
| values kept per Liberate | at most one per guard, so at least $R - G$ are returned |
| unfreed garbage | at most $n (R + G) + G$, even with stopped threads |

**Garbage under a stall.** The test runs three processes on a structure with four nodes, with $K = 2$, $G = 6$ and $R = 2 G = 12$. Process 0 stops inside its first pop or dequeue with a guard posted, and the others do 50 or 400 operations. The peak of unfreed retired nodes stays between 23 and 27 in all runs, under the proved bound $n (R + G) + G = 60$.

## Properties

- Liberate is wait free, even when other Liberate calls work on the same guards at the same time.
- A stopped thread traps at most one value per guard, so the garbage stays bounded.
- A value that stays guarded does not stay with the thread that retired it; it moves to the guard and then to whoever finds it free.
- The handoff word needs a CAS on a value and a version number, which is a double-width CAS on 64-bit machines.
- Each protected read costs a write and a check read, as with hazard pointers.

## Variants and improvements

- **Lock-free Liberate with single-width CAS.** Figure 11 of the paper drops the version numbers. Without them, Liberate must retry the handoff and check again after a success, so it is only lock free.
- **Dynamic guards.** The paper hires and fires guards at run time with a long-lived renaming algorithm, and Liberate reads a counter of the highest guard ever hired. This page gives each process a fixed set of guards.
- **[Hazard pointers](/hazard-pointers/).** Michael published the same post-and-check protocol in the same year. Its scan keeps guarded nodes in the caller's list instead of handing them off, and needs only single-width atomics.
- **[Lock-free reference counting](/lock-free-reference-counting/).** The paper uses PTB to make the single-word reference counting of Detlefs and others work without double compare-and-swap.

## When to use it

Use pass the buck when the reclamation itself must be wait free, or when a thread that retires a node must not be stuck holding it because some other thread guards it. It fits structures with short traversals, such as stacks and queues, as hazard pointers do. Where a double-width CAS is missing or slow, use the lock-free variant or plain hazard pointers. For long traversals, the write per node is costly; consider [hazard eras](/hazard-eras/) or an epoch-based method.

## Pitfalls

**Posting without the check.** The wrong client writes the pointer to its guard at L1 and uses it at once. A Liberate may already have passed the guard, so it does not see the post and frees the node. The right client reads the source again after L1 and retries if it changed. The test finds this.

**Taking a trapped value out of the handoff word.** The wrong L9 takes $h.val$ out whenever it is not nil. If the guard still holds that value, it may be trapped, and the Liberate returns it. The right L9 also requires $h.val \ne v$. The test finds this with two pops.

**Dropping the version number.** Without it, the CAS at L6 can succeed on a word that changed and changed back, and the argument that the value taken out was unguarded at the read of $POST[g]$ fails. The three-try rule depends on it too. Use the lock-free variant if you cannot have it.

**Freeing what was passed in.** The caller must free the set that Liberate returns, not the set it passed in. The returned set can lack trapped values and contain values that other threads retired.

## Implementations

## History

Maurice Herlihy, Victor Luchangco and Mark Moir posed the repeat offender problem and gave pass the buck at DISC 2002, and a brief announcement with Paul Martin on dynamic-sized lock-free data structures appeared at PODC 2002, the same meeting where Maged Michael presented [hazard pointers](/hazard-pointers/). The full paper, with the wait-free Liberate, the proof as I/O automata and experiments on the Michael and Scott queue, appeared in ACM Transactions on Computer Systems in 2005.

## References
