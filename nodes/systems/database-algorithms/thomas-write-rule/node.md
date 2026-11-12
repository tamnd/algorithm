---
tag: NVC9CE
kind: technique
slug: thomas-write-rule
name: Thomas write rule
aliases:
- Thomas's write rule
- ignore obsolete writes rule
area: systems/database-algorithms
level: advanced
summary: "In timestamp ordering, skip a write that a younger write has already made obsolete instead of aborting. It admits some schedules that are view but not conflict serializable."
prereqs: [timestamp-ordering, view-serializability]
see_also: [timestamp-ordering, view-serializability, conflict-serializability, multiversion-concurrency-control, lww-register, two-phase-locking, quorum, concurrency-control]
sources:
  - paper: doi:10.1145/320071.320076
    title: Robert H. Thomas, A majority consensus approach to concurrency control for multiple copy databases, ACM Transactions on Database Systems 4(2), 1979, pages 180 to 209
    locator: the update rule for copies, under which an update with an older timestamp than the stored value is not applied
  - paper: doi:10.1145/356842.356846
    title: Philip A. Bernstein and Nathan Goodman, Concurrency control in distributed database systems, ACM Computing Surveys 13(2), 1981, pages 185 to 221
    locator: the section on timestamp ordering, where the Thomas write rule is the T/O method for write-write synchronization
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 4 (timestamp ordering and the Thomas write rule)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Chapter 17 (timestamp concurrency control; the Thomas write rule and the schedules it allows that are not conflict serializable)
---

The Thomas write rule is a change to the write rule of [timestamp ordering](/timestamp-ordering/). Basic timestamp ordering rejects a write $w_i(x)$ when a younger transaction has already read or written $x$. The Thomas write rule splits this case. If a younger transaction has *read* $x$, the write is still rejected. If a younger transaction has only *written* $x$, the write is obsolete: in timestamp order it would be overwritten at once by the younger write, and no transaction in between reads it. So the scheduler skips the write and lets $T_i$ go on. The rule comes from Thomas's 1979 protocol for replicated databases. It saves aborts, and the schedules it accepts are equivalent to the timestamp order in the sense of [view serializability](/view-serializability/), though not always in the sense of [conflict serializability](/conflict-serializability/).

## In plain words

Every transaction has a ticket number, and the result must look like running them one at a time in ticket order. Suppose ticket 5 wants to write a value, but ticket 7 has already written a newer value to the same place, and nobody with a ticket between 5 and 7 has looked at it.

In ticket order, the value of ticket 5 would be written and then replaced by the value of ticket 7 at once, before anyone could see it. So writing it now would only do harm, and cancelling ticket 5 would waste its work. The rule says: just drop that one write, and let ticket 5 continue. If someone younger has already read the place, though, ticket 5 really is too late, and it must start again.

## When it applies

- The scheduler is [timestamp ordering](/timestamp-ordering/), so the serial order is the timestamp order, and each item has a read timestamp $\mathrm{rts}(x)$ and a write timestamp $\mathrm{wts}(x)$.
- A write replaces the whole value of the item (a *blind* overwrite in effect). It must not be an increment or another update that combines with the old value at the storage level.
- Only the final effect of the writes matters, not each intermediate write: there are no triggers or logs that must see every write.
- Recovery can deal with a transaction whose write was skipped: if the younger writer later aborts, the value of the skipped write may be needed again (see the pitfalls).

## The template

The read rule is that of basic timestamp ordering. The write rule has three cases.

```pseudo id=main
TWR-WRITE(T_i, x)
L1  if ts(T_i) < rts(x) then reject: abort T_i and restart it with a new timestamp
L2  else if ts(T_i) < wts(x) then skip the write; T_i continues        ▷ obsolete
L3  else run w_i(x); wts(x) ← ts(T_i)

TO-READ(T_i, x)
L4  if ts(T_i) < wts(x) then reject: abort T_i and restart it with a new timestamp
L5  else run r_i(x); rts(x) ← max(rts(x), ts(T_i))
```

Line L2 is the whole technique. Compared with basic TO, it turns a reject into a skip when the conflict is a write-write conflict with a younger transaction.

**What the result is equivalent to.** Take a run with no rejections, and call the skipped writes *dead*. Then:

1. *The executed actions are in timestamp order.* The stamps never decrease and bound the timestamps of the accepted actions on each item, so, exactly as for basic TO, every pair of conflicting executed actions is in timestamp order. Executed actions alone form a conflict serializable schedule.
2. *The views match the timestamp order.* Let $S$ be the input schedule and $\sigma$ the serial schedule in timestamp order, both with the dead writes removed. Then each read reads from the same write in both, and each item has the same final write. Moreover, the dead writes would not change the final writes of $\sigma$: a write is skipped only when a younger write of the item exists, so it is never the last write in timestamp order.
3. *Why no read is lost.* A read $r_k(x)$ that, in timestamp order, comes between a dead write $w_i(x)$ and the younger write $w_j(x)$ that made it obsolete would have $\mathrm{ts}(T_i) < \mathrm{ts}(T_k) < \mathrm{ts}(T_j)$. If it came before $w_i(x)$ in $S$, then $\mathrm{rts}(x) \ge \mathrm{ts}(T_k)$ and $w_i(x)$ would be rejected at line L1, not skipped. If it came after $w_j(x)$, it would be rejected at line L4. Either way the run has a rejection, which we excluded.

So the execution is view equivalent to the timestamp order, once the dead writes are seen as never done. For the plain input schedule, with the dead writes kept in place, the same holds when each dead write $w_i(x)$ is followed by a live write of $x$ before any read of $x$: then nobody reads the dead value, and it is not final. In that case the plain schedule is view serializable, and it is often not conflict serializable, as the first example shows.

## Classic examples

**View but not conflict serializable.** Let $T_1, T_2, T_3$ start in this order, and take $S = r_1(x)\ w_2(x)\ w_1(x)\ w_3(x)$.

| action | basic TO | Thomas write rule |
|---|---|---|
| $r_1(x)$ | accept, $\mathrm{rts}(x) = 1$ | accept, $\mathrm{rts}(x) = 1$ |
| $w_2(x)$ | accept, $\mathrm{wts}(x) = 2$ | accept, $\mathrm{wts}(x) = 2$ |
| $w_1(x)$ | $1 < \mathrm{wts}(x)$: reject $T_1$ | $1 \ge \mathrm{rts}(x)$ but $1 < \mathrm{wts}(x)$: skip |
| $w_3(x)$ | accept | accept, $\mathrm{wts}(x) = 3$ |

The conflicts $r_1(x) < w_2(x)$ and $w_2(x) < w_1(x)$ form the cycle $T_1 \to T_2 \to T_1$, so $S$ is not conflict serializable. But it is view equivalent to $T_1 T_2 T_3$: $T_1$ reads the initial value in both, and $T_3$ writes the final value in both. Basic TO aborts $T_1$; the Thomas write rule commits all three.

**An accepted schedule whose plain form is not view serializable.** Take $S = r_1(x)\ w_2(x)\ w_1(x)$, with $T_1$ older. The rule skips $w_1(x)$, and the database ends with the value of $T_2$, which is what $T_1 T_2$ gives. But the plain schedule, read literally, ends with the value of $T_1$, and it is not view serializable: in $T_1 T_2$ the last write is by $T_2$, and in $T_2 T_1$ the read of $T_1$ would see $T_2$'s value. The rule is correct because the skipped write never happens; the equivalence is about the execution, not about the input schedule. In a test of 3000 random small schedules (seed 11, two items, up to four transactions) run to a state with no rejections, 619 runs skipped a write. In 133 of them every skipped write is overwritten before the next read of its item, and in those the plain schedule was always view equivalent to the timestamp order; 123 of these 133 were not conflict serializable. In 246 of the 619 runs the plain schedule was not view serializable, which is the case of this second example.

**Replicated data.** In Thomas's majority consensus protocol, each copy of an item stores the timestamp of its value. An update that arrives at a copy with an older timestamp than the stored one is not applied. Copies that receive the same updates in different orders still end in the same state. The same rule appears today as the [last-writer-wins register](/lww-register/) of replicated stores, where it gives convergence of copies but no serializability of transactions.

## Variations

- **Multiversion timestamp ordering.** Instead of dropping an obsolete write, keep it as an old version. A late reader with a timestamp between the two writes can then read it. [Multiversion concurrency control](/multiversion-concurrency-control/) generalizes the Thomas write rule in this way.
- **Combined with locking.** Bernstein and Goodman describe hybrid methods that use [two-phase locking](/two-phase-locking/) for read-write conflicts and the Thomas write rule for write-write conflicts; then writes never wait for or abort each other.
- **Strict TO with the rule.** The recoverability fix of strict TO (delay access to items written by uncommitted transactions) can be combined with the rule, but the skipped write needs care when the younger writer aborts.

## Pitfalls

- **The younger writer aborts.** If $T_j$, whose write made $w_i(x)$ obsolete, aborts later, its write is undone, and $x$ goes back to a value older than $T_i$'s. The skipped write of $T_i$ is then lost, and a committed $T_i$ has no effect on $x$. A system that uses the rule must either keep the skipped value until $T_j$ commits, or make $T_i$ wait for the outcome of $T_j$ (a strict variant). The tests on this page avoid the case by removing rejected transactions and rerunning until no transaction is rejected.
- **Read-modify-write is not blind.** If $T_i$ read $x$ before writing it, the rule is still correct as long as the read was accepted, but if the write is an increment applied by the storage layer, skipping it loses an update. The rule assumes a write that sets the whole value.
- **Do not compare the input schedule.** Correctness is about the execution with the skipped writes removed. The plain input schedule may be neither conflict nor view serializable (second example).
- **Read rule unchanged.** A read with a timestamp older than $\mathrm{wts}(x)$ must still be rejected. Only writes can be skipped, because a skipped read would return a wrong value.
- **Not a general concurrency control rule.** The Thomas write rule only refines timestamp ordering. It has no meaning in a locking scheduler, where the order of conflicting writes is set by the locks.

## Exercises

1. Run TO with the Thomas write rule on $r_1(y)\ w_2(x)\ w_1(x)\ r_3(x)$, with timestamps in start order. Which actions are skipped, and which are rejected? Is the result view equivalent to the timestamp order?
2. Prove that a skipped write is never the last write of its item in timestamp order.
3. Let $T_1$ be older than $T_2$ and take $w_1(x)\ w_2(x)\ w_2(y)\ w_1(y)$. Show that basic TO rejects $T_1$, that the Thomas write rule accepts all, that the execution leaves the state of $T_1 T_2$, and that the plain schedule is not view serializable.
4. Show that, without reads, the rule makes the final value of each item the value of the youngest writer, whatever the arrival order of the writes. Relate this to a last-writer-wins register.
5. The younger writer $T_j$ aborts after $w_i(x)$ was skipped. Design a fix that keeps the result correct, and say what it costs.

## References
