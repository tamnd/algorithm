---
tag: 9B9H5V
kind: algorithm
slug: shavit-touitou-stm
name: Shavit-Touitou STM
aliases:
- first software transactional memory
- static software transactional memory
area: concurrency/transactional-memory
level: research
summary: The first software transactional memory (Shavit and Touitou 1995). Lock-free with LL/SC, by ownership in address order and helping, but only for static transactions with a known data set.
complexity:
  vars: {k: the number of words in the data set of one transaction, m: the number of data words, n: the number of processes}
  steps: {attempt: Θ(k), help: Θ(k)}
  space: {shared: Θ(m + n·k), extra: Θ(k)}
properties: {deterministic: true, opaque: true, blocking: false, lock_free: true, static_transactions_only: true}
history:
  year: 1995
  people: [Nir Shavit, Dan Touitou]
  note: Shavit and Touitou presented software transactional memory at PODC 1995 and published the journal version in Distributed Computing in 1997.
prereqs: [software-transactional-memory, load-linked-store-conditional, helping, lock-freedom]
see_also: [dstm, multi-word-cas, opacity, transaction, lock-ordering, disjoint-access-parallel-stm-lower-bound, herlihy-moss-htm, universal-construction]
sources:
  - paper: doi:10.1145/224964.224987
    title: Nir Shavit and Dan Touitou, Software transactional memory, PODC 1995
    locator: the definition of static transactions, the ownership and helping scheme, and the simulated benchmarks
  - paper: doi:10.1007/s004460050028
    title: Nir Shavit and Dan Touitou, Software transactional memory, Distributed Computing 10(2), 1997
    locator: the journal version, with the code of the transaction, the acquisition of ownerships in address order, the agreement on old values, the memory update and the correctness argument
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 4 (Software transactional memory), the part on nonblocking STM systems and the early history of STM
  - paper: doi:10.1145/165123.165164
    title: Maurice Herlihy and J. Eliot B. Moss, Transactional memory, architectural support for lock-free data structures, ISCA 1993
    locator: the hardware transactional memory that the STM of Shavit and Touitou implements in software
---

The STM of Nir Shavit and Dan Touitou (PODC 1995) is the first [software transactional memory](/software-transactional-memory/), and the paper gave the field its name. It runs **static** [transactions](/transaction/): each transaction names, before it starts, the words it will read and write (its data set), and a function that maps their old values to new values. A transaction takes *ownership* of each word of its data set in increasing address order, with [load-linked/store-conditional](/load-linked-store-conditional/). When it finds a word owned by another transaction, it fails, gives back what it owns, and [helps](/helping/) the owner to finish. Ordered acquisition and helping make the STM [lock-free](/lock-freedom/): some transaction always completes, even when processes stop for ever. The price is the static data set. A transaction cannot decide what to read next from a value it has read, so a search in a [linked list](/linked-list/) does not fit this STM. [DSTM](/dstm/) (2003) removed that limit.

## In plain words

Each memory word has an owner field. A transaction lists all its words at the start, sorted by address. It then claims them one by one, from the lowest address up. If all claims succeed, the transaction is a success: it records the old values of its words, computes the new values, writes them, and frees the words. If a word is already claimed by another transaction, the transaction fails. It frees its words and then does the work of the transaction that blocked it, from that transaction's own record, so that a stopped process cannot block the others. Then it tries again. All shared writes use LL/SC, so a helper that wakes up late cannot undo work that is already done.

## The problem

Give $n$ processes static transactions on $m$ shared words. A static transaction is a pair $(D, f)$: a data set $D$ of $k$ words, and a function $f$ that maps the old values of $D$ to new values for some words of $D$ and to a result. The system must run each transaction atomically, as one $k$-word read-modify-write: the transactions are [linearizable](/linearizability/), and $f$ must run only on a consistent set of old values. The progress condition is lock-freedom: in every infinite run, transactions keep completing, whatever the schedule and even if some processes crash.

### Model and notation

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ | process names |
| $m$ | the number of data words |
| $k$ | the size of the data set $D(r)$ of a transaction record $r$ |
| own$(a)$ | the owner field of word $a$: a record, or NONE |
| status$(r)$ | NONE (undecided), SUCCESS, or (FAILURE, $a$) when the claim of word $a$ failed |
| old$(r)$ | the old values of $D(r)$ that the helpers of $r$ agree on |

The processes are asynchronous and may crash between any two steps. The primitives are atomic read and LL/SC. LL/SC can solve consensus for any number of processes (consensus number $\infty$). The paper assumes an ideal LL/SC: a store-conditional fails only if the word was written since the load-linked of the same process, and reads of other words in between do not cancel the link. Real LL/SC on ARM or POWER can fail for other reasons and allows only a few instructions between the two; a CAS with a version counter can stand in for it. The memory is sequentially consistent.

## The algorithm

Each attempt of a transaction has its own record $r$ with $D(r)$ (sorted), $f_r$, status$(r)$ and old$(r)$. The record does not change after it is made, so a helper reads $D(r)$ and $f_r$ with no shared step. The process that makes the record is its *initiator*; any process that runs TRANSACTION$(r, \cdot)$ is a helper of $r$.

```pseudo id=main
TRANSACTION(r, initiator)
L1  for each a ∈ D(r) in increasing address order: if not ACQUIRE(r, a) then exit loop
L2  if every a ∈ D(r) is owned by r and LL(status(r)) = NONE then SC(status(r), SUCCESS)
L3  if status(r) = SUCCESS then old ← AGREE(r); new ← f_r(old); UPDATE(r, new); RELEASE(r); return SUCCESS
L4  RELEASE(r); if initiator then (o ← own(a) for the a in status(r); if o ≠ NONE then TRANSACTION(o, false)); return FAILURE

ACQUIRE(r, a)
L5  loop: o ← LL(own(a)); if o = r then return true
L6        if status(r) ≠ NONE then return false          ▷ r is decided: stop claiming
L7        if o = NONE then (if SC(own(a), r) then return true else continue)
L8        if LL(status(r)) = NONE then SC(status(r), (FAILURE, a)); return false

AGREE(r)
L9  for each a ∈ D(r): loop: t ← LL(old(r)); if a ∈ t then exit loop; v ← read(a); if SC(old(r), t ∪ {(a, v)}) then exit loop
    return old(r)

UPDATE(r, new)
L10 for each a ∈ D(r) that new writes: v ← LL(a); if v ≠ new[a] and own(a) = r then SC(a, new[a])

RELEASE(r)
L11 for each a ∈ D(r): if LL(own(a)) = r then SC(own(a), NONE)

RUN(p, D, f)                                            ▷ the initiator
L12 loop: make a new record r with D(r) = sorted D, f_r = f, status(r) = NONE, old(r) = ∅
          if TRANSACTION(r, true) = SUCCESS then return the result of f(old(r))
```

The parts:

- **Claims in address order (L1, L5 to L8).** A record claims its words from the lowest address up and keeps each one until it is decided. A claim of a free word is an SC from NONE to $r$ (L7). If the word belongs to another record, $r$ is decided FAILURE at L8. The check at L6 stops a slow helper from claiming more words for a record that is already decided.
- **One decision (L2, L8).** status$(r)$ is set once, by the first SC that wins: SUCCESS when all words are owned, FAILURE when a claim failed. Every helper then follows the same path.
- **Agreement on old values (L9).** The helpers of a SUCCESS record build old$(r)$ one entry at a time with LL/SC, so they all see the same old values, even if some helpers read a word after another helper wrote the new value.
- **Update (L10).** Each helper writes each new value with LL/SC, and only if the word does not hold the new value yet and $r$ still owns it. The value test matters: a helper whose LL comes after another helper's write sees the new value and does not write. Without the test, its SC could succeed after the release and wipe out a write of the next owner. The tests show this lost update.
- **Release and help (L4, L11).** A failed record frees its words. Its initiator then reads the current owner of the word that blocked it and runs that record to the end, once and not recursively (a helper does not help further). Then it makes a new record and tries again (L12).

This page uses a new record for each attempt. The paper reuses one record per process and adds a version number to each record, so that a late helper can see that the record has moved on. The effect is the same.

## Example

Three words $a_0 = a_1 = a_2 = 10$. Process $p$ moves 3 from $a_0$ to $a_1$ ($D = \{a_0, a_1\}$), and $q$ moves 5 from $a_1$ to $a_2$ ($D = \{a_1, a_2\}$). The run is the one in `test_worked_example_helping`.

| Step | Process | Lines | Action | Owners after it | Words $(a_0, a_1, a_2)$ |
|---|---|---|---|---|---|
| 1 | $p$ | L1, L5 to L7 | claims $a_0$ and $a_1$ for $r_p$ in 6 steps, then stops | $a_0, a_1$: $r_p$ | $(10, 10, 10)$ |
| 2 | $q$ | L5, L8 | finds own$(a_1) = r_p$; sets status$(r_q)$ = (FAILURE, $a_1$) | same | same |
| 3 | $q$ | L4, L11 | releases (owns nothing); reads own$(a_1) = r_p$ and helps $r_p$ | same | same |
| 4 | $q$ for $r_p$ | L1, L2 | finds $a_0$ and $a_1$ owned by $r_p$; sets status$(r_p)$ = SUCCESS | same | same |
| 5 | $q$ for $r_p$ | L9, L10 | old$(r_p) = \{a_0: 10, a_1: 10\}$; writes $a_0 = 7$, $a_1 = 13$ | same | $(7, 13, 10)$ |
| 6 | $q$ for $r_p$ | L11 | releases $a_0$ and $a_1$ | none | $(7, 13, 10)$ |
| 7 | $q$ | L12, L1 to L11 | new record $r'_q$: claims $a_1, a_2$, SUCCESS, old $\{a_1: 13, a_2: 10\}$, writes, releases | none | $(7, 8, 15)$ |
| 8 | $p$ | L2 to L11 | wakes up: sees SUCCESS, finds old$(r_p)$ complete, skips $a_0$ (holds 7 already) and $a_1$ (no longer owned by $r_p$) | none | $(7, 8, 15)$ |

$p$ returns success with the old values 10 and 10, although $q$ did all of its work. The history has two commits and one failed attempt, and the opacity checker accepts it in the order $r_p, r'_q$. The money is all there: $7 + 8 + 15 = 30$. At step 8, the LL of $a_1$ by $p$ returns 8, which is not the new value 13, but own$(a_1)$ is NONE, so $p$ does not write. If $p$ had stopped between its LL and its SC of $a_1$, a write to $a_1$ in the meantime would make the SC fail.

## Correctness

The full proof of atomicity is in [the correctness proof](proofs/correctness). It shows that each record that becomes SUCCESS takes effect at the SC that sets its status, in a state that the earlier SUCCESS records produced, and that a record that fails writes nothing. The key steps are: a record keeps all its words from its SUCCESS until its first release; every successful write to a data word is a write of the new value of its current SUCCESS owner (the value test at L10 is needed here); and all helpers agree on one set of old values. The function $f$ runs only on those agreed values, so no attempt ever sees an inconsistent state: this STM has no [zombie transactions](/zombie-transactions/), and it is [opaque](/opacity/) in the sense that matters for a static transaction. Opacity is the condition that every transaction, also one that fails, sees values that agree with one serial order that respects real time.

Lock-freedom is proved there only as a sketch. Records claim words in increasing order and keep them while undecided, so a chain of failures (record $r$ fails on a word of $o$, $o$ fails on a word of $o'$, and so on) has strictly increasing addresses and cannot be a cycle. The record at the top of such a chain meets no undecided owner above it, so it, or a helper of it, reaches SUCCESS. Helping is what keeps a crashed initiator from blocking its words for ever.

The tests check these claims on runs:

- all interleavings of two increments of one word, each with up to two attempts, with failures and helping: opaque, and no update is lost
- 300 seeded random schedules of two transfers, and 150 of three processes that each run three transfers and an audit: every run ends, the history is opaque, each audit sees the total 30, and every owner field is free at the end
- for each $k$, process $p$ stops for ever after its $k$-th step, and the two other processes still finish with the total intact (lock-freedom on these runs)
- with helping turned off, a process that stops while it owns $a_1$ makes the other process fail five times and never commit
- with the value test at L10 removed, the exhaustive search finds a run with two committed increments that leaves $x = 1$

The exhaustive search covers only one-word transactions: two transfers with helping give more than a million states, so two-word transactions are tested with random schedules.

## Complexity

Count shared memory steps of the code on this page. A claim takes 3 steps (LL, status read, SC), the agreement 3 steps per word, an update 3 steps per written word, and a release 2 steps per word, plus 4 steps for the decision and the reads of the status and of old$(r)$. So an attempt with no conflict on a data set of $k$ words, of which $w$ are written, takes $8k + 3w + 4$ steps: 12 steps for a one-word read, 20 for a two-word read, and 26 for a two-word transfer. A failed attempt costs $O(k)$ steps for itself and $O(k')$ for the help of one record with $k'$ words, since helping is not recursive. Each failed SC in a loop at L5 or L9 is caused by a successful SC of another process, so the total work is lock-free but not wait-free: one process can fail again and again.

Space: one owner field per data word, so $\Theta(m)$ extra shared words, and one record of $\Theta(k)$ words per process (the paper reuses it), so $\Theta(m + nk)$ in all.

## Properties

- **Lock-free**, with LL/SC as the only strong primitive. A crashed process never blocks the others.
- **Static transactions only.** The data set must be known before the transaction starts.
- **Atomic and opaque for static transactions**: $f$ runs only on agreed old values.
- **Not strictly disjoint-access parallel**: two transactions with disjoint data sets touch disjoint owner fields, except through help. If $r_1$ helps $r_2$ because they share a word, $r_1$ then touches the other words of $r_2$, which a third transaction may share.
- **Not wait-free**: one transaction can fail for ever while others succeed.
- **Redundant work**: several helpers can run the same record at once; all but one of their writes fail or are skipped.

## Variants and improvements

- **Dynamic transactions.** [DSTM](/dstm/) of Herlihy, Luchangco, Moir and Scherer (2003) lets a transaction open objects as it goes. It gives up lock-freedom for [obstruction-freedom](/obstruction-freedom/) and moves progress to a contention manager.
- **Multi-word CAS.** A static transaction that compares $k$ words and writes them is a [multi-word CAS](/multi-word-cas/). The CAS-based $k$-word CAS of Harris, Fraser and Pratt (2002) uses the same ideas: a descriptor, ownership in address order, and helping.
- **Lock-based STM.** Later STMs such as [TL2](/tl2/) and [TinySTM](/tinystm/) give up non-blocking progress for speed. They use versioned locks and a [global version clock](/global-version-clock/), and they accept that a stopped lock holder blocks others.
- **Recursive helping.** Helping the owner, and the owner of the owner, and so on, is the method of earlier universal constructions. Shavit and Touitou help only once and rely on the address order to avoid chains.

## When to use it

Use it when the set of words is known in advance and lock-freedom is required: a $k$-word read-modify-write on fixed addresses, such as a transfer between two accounts, a swap of two slots of an array, or a multi-word counter update. Do not use it for transactions that follow pointers, such as a search in a list or a tree, because the data set is not known until the search is done. For those, use a dynamic STM ([DSTM](/dstm/), [TL2](/tl2/)) or a lock-free data structure designed for the purpose. Today it is mostly of historical and teaching value: it shows the ownership, ordering and helping ideas in their simplest form.

## Pitfalls

- **A plain SC at the update.** A helper must not write a data word just because $r$ owns it at its read. If its LL came after another helper's write, the SC can succeed later, after the word has a new owner, and it wipes out that owner's write. The value test at L10 prevents this; the test `test_without_the_value_test_an_update_is_lost` shows the lost update without it.
- **Claims in random order.** If two records claim the same two words in opposite orders, each can fail on the other again and again. The address order breaks the cycle.
- **Recursive helping without order.** Helping the record that blocked the helped record can lead to long chains or cycles. One level of help, with ordered claims, is enough.
- **Late helpers.** Every write that a helper might make late must be an SC that follows an LL and a check of the state: status, owner or old values. A plain write at any of these points lets a late helper undo work.
- **Records that change.** A helper reads $D(r)$ and $f_r$ with no synchronization. This is safe only because a record does not change once it is published. When records are reused, as in the paper, a version number must tell a late helper that its record is gone.
- **Expecting dynamic transactions.** The STM cannot run code like "read $x$; if $x > 0$ then write $y$" unless $y$ is put in the data set in advance. Putting every word that might be touched in the data set makes the transaction conflict with more of the others.

## Implementations

## History

Herlihy and Moss proposed [transactional memory](/herlihy-moss-htm/) as a hardware feature in 1993. Shavit and Touitou showed at PODC 1995 that the idea can be implemented in software, on any machine with LL/SC, and named it software transactional memory. Their aim was a method to build lock-free data structures that was simpler than the universal constructions of the time, and they compared it with other non-blocking methods on simulated benchmarks. The journal version appeared in Distributed Computing in 1997. The restriction to static transactions was lifted by DSTM in 2003, which started the line of practical, dynamic STMs.

## References
