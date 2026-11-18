---
tag: MFH0BC
kind: technique
slug: escrow-transactional-method
name: Escrow transactional method
aliases:
- escrow locking
- escrow concurrency control
area: databases/transactions-and-concurrency
level: advanced
summary: "Let concurrent transactions update a numeric quantity by reserving amounts in escrow, as long as all outcomes respect its bounds."
prereqs: [two-phase-locking, serializability]
see_also: [invariant-confluence, highly-available-transactions, sagas, open-nested-transactions, multiple-granularity-locking, transaction-chopping, write-ahead-logging, strict-two-phase-locking]
sources:
  - paper: doi:10.1145/7239.7265
    title: "Patrick E. O'Neil, The escrow transactional method, ACM Transactions on Database Systems 11(4), 1986, pages 405 to 430"
    locator: "the escrow operation with its infimum and supremum over pending transactions, the bounds test, the treatment of reads of escrow quantities, and recovery by logged increments; chapter level only"
  - book: isbn:9781558601901
    title: "Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993"
    locator: "the discussion of hot spots, field calls and escrow in the chapters on locking, chapter level only"
  - book: isbn:9781558605084
    title: "Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2002"
    locator: "the chapters on semantic and multilevel concurrency control, where increments and escrow are operations that commute under conditions, chapter level only"
---

The *escrow transactional method* of Patrick O'Neil (1986) is a form of concurrency control for numeric fields with bounds, such as an account balance that must stay at least 0 or a stock count that must stay between 0 and the size of a warehouse. Under [two-phase locking](/two-phase-locking/) every transaction that changes such a field locks it until commit, so a popular field becomes a hot spot that serializes all its updaters. Escrow lets many transactions hold uncommitted changes to the same field at once. Each request to add or take an amount $\delta$ is granted only if the field stays within its bounds *for every subset* of the pending transactions that may still commit or abort; the amount is then said to be held in escrow. Because increments commute, the final value does not depend on the order of the commits, and the schedule is [serializable](/serializability/) with respect to the operations on the field. The same idea, a share of a bounded quantity reserved ahead of time, is how [invariant confluence](/invariant-confluence/) handles constraints such as "stock at least 0" without coordination, and how [sagas](/sagas/) reserve resources before a long process finishes.

## In plain words

A shop has 10 tickets left. Many customers try to buy at the same time. Locking the counter would make them buy one at a time, even though most of them will succeed. Escrow does something smarter. When a customer asks for 2 tickets, the system checks that, even in the worst case, the counter cannot go below zero, and then sets the 2 tickets aside for that customer. Other customers can take from the tickets that are left without waiting. If a customer finally buys, the tickets leave the counter; if the customer gives up, they go back. The system always knows the smallest and the largest value the counter could end up with, and it refuses a request that could push either one outside the allowed range.

## When it applies

- The data item is a number, and the updates are increments and decrements by known amounts, which commute.
- The constraint on the item is a range $[low, high]$, often only a lower bound such as 0.
- Transactions mostly need to know that the value is large enough, not its exact value.
- The item is a hot spot: many transactions change it, and each holds its change for a while before it commits.

## The template

For an item $x$ the system stores the committed value $val(x)$, the bounds, and the pending changes $P(x)$, one entry $\delta_T$ for each transaction $T$ that holds an escrow on $x$. Let $inf(x) = val(x) + \sum_{\delta_T < 0} \delta_T$ and $sup(x) = val(x) + \sum_{\delta_T > 0} \delta_T$, the smallest and largest values that any set of commits can give. The holes are ⟨BOUNDS⟩, ⟨ON-FAIL⟩, ⟨EXACT-READ⟩ and ⟨LOG⟩.

```pseudo id=main
ESCROW(T, x, δ)                                              ▷ ask to add δ, which may be negative
L1  inf' ← inf(x) + min(δ, 0); sup' ← sup(x) + max(δ, 0)
L2  if ⟨BOUNDS⟩ low(x) ≤ inf' and sup' ≤ high(x) then
L3      δ_T ← δ_T + δ in P(x); ⟨LOG⟩ append (T, x, δ); grant
L4  else ⟨ON-FAIL⟩ wait until inf or sup moves, or abort T
COMMIT(T)
L5  for each x with an entry for T: val(x) ← val(x) + δ_T; remove δ_T from P(x)
ABORT(T)
L6  for each x with an entry for T: remove δ_T from P(x)                ▷ val(x) is unchanged
READ-BOUNDS(x)
L7  return [inf(x), sup(x)]                                    ▷ needs no lock
READ-EXACT(x)
L8  ⟨EXACT-READ⟩ wait until P(x) is empty and block new escrows on x, then return val(x)
```

**Why the bounds always hold.** Let $S$ be any subset of the pending transactions. The value after exactly those commit is $val(x) + \sum_{T \in S} \delta_T$, which lies between $inf(x)$ and $sup(x)$, since $inf$ adds every negative change and $sup$ every positive one. Line L2 grants a request only when the new $inf$ and $sup$ are inside $[low, high]$, and lines L5 and L6 only remove terms from the sums. So whatever happens to the pending transactions, the committed value stays in bounds.

**Why it is serializable.** Escrow operations on one item commute with each other, so any order of commits gives the same value. A read of the bounds by line L7 is true in every serial order of the pending transactions. An exact read by line L8 sees no pending change, which is the same as a lock that conflicts with escrow. With [strict two-phase locking](/strict-two-phase-locking/) on the other data, the schedule is serializable at the level of these operations, as in the semantic concurrency control of Weikum and Vossen.

## Classic examples

- **Bank withdrawals.** A balance must stay at least 0. A withdrawal of 100 is granted if $inf - 100 \ge 0$; deposits raise $sup$ and do not help a withdrawal until they commit. Many withdrawals and deposits of one account run at once, instead of one at a time under [two-phase locking](/two-phase-locking/).
- **Stock and seats.** A count of items or seats, with bounds 0 and the capacity. An order reserves its quantity by escrow and releases it on abort. This is also the reservation step of a [saga](/sagas/): the compensation of a reservation is the release, which always succeeds.
- **Replicated quotas.** A bound such as "at most 1000 tickets in total" can be split into quotas, one per replica, each enforced locally by escrow. A replica that runs out asks another to give up some of its quota. Work on [invariant confluence](/invariant-confluence/) points to this method for a lower bound on a counter, a constraint that decrements on different replicas can break, and the demarcation protocol of Barbará and Garcia-Molina is a version of it for distributed databases.
- **Field calls.** The field calls of IBM's IMS Fast Path, an earlier method for hot fields, let a transaction state a test and an update on a hot field, checked at the call and applied at commit, without holding a lock in between.

## Variations

- **No bounds.** If there are no bounds, every increment is granted and the method is an increment lock that is compatible with itself and conflicts with reads and writes.
- **Conditional tests.** A transaction can ask "is $x \ge 500$?" and get "yes" if $inf(x) \ge 500$, "no" if $sup(x) < 500$, and must wait or lock otherwise.
- **Multilevel and open nesting.** Escrow is an operation at a higher level than page reads and writes. In [open nested transactions](/open-nested-transactions/) the page latches are released at the end of the operation and the escrow entry plays the part of the higher-level lock; undo is a compensating increment.
- **Granularity.** The escrow entry can be kept with the item, with the lock table, or with the transaction, as with other lock modes in [multiple granularity locking](/multiple-granularity-locking/).

## Pitfalls

- **Operations that do not commute.** "Set $x$ to 5" or "double $x$" cannot be held in escrow alongside increments. They need an exclusive lock that waits for $P(x)$ to empty.
- **Exact reads destroy the benefit.** If many transactions read the exact value, line L8 blocks escrow as often as a lock would. Applications that print a balance should read the bounds or a committed snapshot.
- **Undo by before-image is wrong.** Other transactions may have committed changes to $x$ while $T$ was pending, so an abort must not restore an old value. Recovery logs increments, and undo applies $-\delta_T$, as with logical logging under [write-ahead logging](/write-ahead-logging/).
- **Starvation of large requests.** A large withdrawal can wait forever while small ones keep $inf$ low. A queue in arrival order, or a limit on how much may be in escrow, fixes it.
- **Hidden reads.** A transaction that reads $val(x)$ directly and then calls escrow with a computed amount has made a read that escrow does not protect. The amount must depend only on the bounds test, or the read must be locked.

## Exercises

1. A balance is 100 with bound $\ge 0$. Pending: $-60$ from $T_1$ and $+50$ from $T_2$. Is a request of $-50$ from $T_3$ granted? What if $T_2$ commits first?
2. Show that if line L2 used $val(x) + \sum \delta_T + \delta$ in place of the new $inf$ and $sup$, a sequence of aborts could leave the committed value out of bounds. Give the sequence.
3. A replica holds a quota of 300 of a bound of 1000 tickets. Write the escrow state of the replica and the message it sends when it runs out.
4. Show how an exact read can be served without blocking by a snapshot, and say what isolation the reader then gets.
5. In a saga for a trip, the hotel step uses escrow on the room count. Write the step and its compensation, and explain why the compensation cannot fail.

## References
