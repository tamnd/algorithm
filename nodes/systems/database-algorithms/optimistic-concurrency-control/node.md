---
tag: 8MJ6N3
kind: algorithm
slug: optimistic-concurrency-control
name: Optimistic concurrency control
aliases:
- OCC
- Kung-Robinson validation
- backward validation with transaction numbers
area: systems/database-algorithms
level: core
summary: "Transactions run without locks on private copies, then a validation step checks their read sets against the write sets of transactions that committed meanwhile, and aborts on overlap."
solves: [concurrency-control]
model: word-ram
complexity:
  vars: {r: the size of the read set, w: the size of the write set, k: the transactions that commit or validate during the life of the transaction}
  time: {worst: O(r + w + k w)}
  space: {extra: O(r + w)}
properties: {deterministic: true}
history:
  year: 1981
  people: [H. T. Kung, John T. Robinson]
  note: ACM TODS 6(2); a technical report of Carnegie Mellon University came first in 1979.
prereqs: [conflict-serializability, concurrency-control]
see_also: [two-phase-locking, timestamp-ordering, multiversion-concurrency-control, serializable-snapshot-isolation, tl2, norec, transaction-validation, read-set-and-write-set]
sources:
  - paper: doi:10.1145/319566.319567
    title: H. T. Kung and John T. Robinson, On optimistic methods for concurrency control, ACM Transactions on Database Systems 6(2), 1981, pages 213 to 226
    locator: Section 2 (the read, validation and write phases), Section 3 (transaction numbers and the three validation conditions), Section 4 (serial validation) and Section 5 (parallel validation)
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 4, the section on certifiers (optimistic schedulers that check at commit), chapter level only
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: Chapter 4, the section on optimistic protocols (backward-oriented and forward-oriented validation), chapter level only
---

*Optimistic concurrency control* (OCC) is the method of Kung and Robinson (1981) that solves the [concurrency control](/concurrency-control/) problem without locks. Each transaction runs in three phases. In the *read phase* it reads from the database and writes only to private copies. In the *validation phase* it checks that no transaction that committed while it ran wrote an item it read. If the check passes, the *write phase* copies its writes into the database, and the transaction gets a *transaction number*; if not, it aborts and restarts. The method bets that conflicts are rare: when they are, transactions never wait, and the price is the work lost by a restart. The result is [conflict serializable](/conflict-serializability/), with the order of the transaction numbers as the serial order in the serial form of validation.

## In plain words

Each person who wants to change a shared document makes a private copy, writes notes on it, and keeps a list of the parts of the original that they looked at.

When they are done, they go to a desk where only one person is served at a time. The clerk checks: since you started, did anyone change a part you looked at? If no, your changes go into the document, and you get the next number in line. If yes, your work was based on old facts, so you throw your copy away and start again.

Nobody waits for anyone while working. Work is lost only when two people really touched the same part at the same time.

## The problem

The input is a stream of transactions, each a program of reads $r_i(x)$ and writes $w_i(x)$ that ends with a commit request. The output is a schedule of the operations on the shared database, plus a decision to commit or abort for each transaction, such that the committed transactions are conflict serializable. Aborted transactions may be restarted as new transactions. There is no durability in this problem; recovery is a separate concern.

## The algorithm

Each transaction $T$ has a *read set* $RS(T)$ and a *write set* $WS(T)$ with the private new values. A global counter $tnc$ holds the last transaction number given out, and for each number $n$ the system keeps $WS(n)$, the write set of the transaction with that number. $T.start$ is the value of $tnc$ when $T$ began.

```pseudo id=main
BEGIN(T)                                                 ▷ read phase
L1  T.start ← tnc; RS(T) ← ∅; WS(T) ← ∅
READ(T, x)
L2  add x to RS(T); return WS(T)[x] if x ∈ WS(T), else the value of x in the database
WRITE(T, x, v)
L3  WS(T)[x] ← v                                         ▷ a private copy
SERIAL-VALIDATE(T)                                       ▷ the whole body is one critical section
L4  finish ← tnc
L5  for n ← T.start + 1 to finish do if WS(n) ∩ RS(T) ≠ ∅ then abort T
L6  copy WS(T) into the database                         ▷ write phase
L7  tnc ← tnc + 1; tn(T) ← tnc; WS(tn(T)) ← the items of WS(T)
PARALLEL-VALIDATE(T)                                     ▷ ⟨ ⟩ marks a short critical section
L8  ⟨finish ← tnc; A ← a copy of active; add T to active⟩
L9  for n ← T.start + 1 to finish do if WS(n) ∩ RS(T) ≠ ∅ then invalid
L10 for each U in A do if WS(U) ∩ (RS(T) ∪ WS(T)) ≠ ∅ then invalid
L11 if invalid then ⟨remove T from active⟩; abort T
L12 copy WS(T) into the database                         ▷ write phase, concurrent with others
L13 ⟨tnc ← tnc + 1; tn(T) ← tnc; WS(tn(T)) ← the items of WS(T); remove T from active⟩
```

**The three conditions.** Kung and Robinson state when a transaction $T_j$ may be ordered after a transaction $T_i$ with $tn(T_i) < tn(T_j)$. One of these must hold:

1. $T_i$ completes its write phase before $T_j$ starts its read phase.
2. $WS(T_i) \cap RS(T_j) = \emptyset$, and $T_i$ completes its write phase before $T_j$ starts its write phase.
3. $WS(T_i) \cap RS(T_j) = \emptyset$, $WS(T_i) \cap WS(T_j) = \emptyset$, and $T_i$ completes its read phase before $T_j$ completes its read phase.

**Serial validation** (lines L4 to L7) runs validation and the write phase of one transaction at a time. Write phases do not overlap, so condition 2 holds whenever the sets are disjoint, and line L5 checks exactly those transactions that are not covered by condition 1: the ones numbered after $T$ started. This is *backward* validation: $T$ is checked against transactions that have already committed.

**Parallel validation** (lines L8 to L13) lets write phases overlap. The transactions in $A$ were in validation or in their write phase when $T$ entered; they completed their read phases first, so line L10 checks the sets of condition 3. Kung and Robinson take the check of lines L9 and L10 out of the critical section; only lines L8, L11 and L13 must be atomic.

## Example

Items $x$ and $y$ start at 0, and $tnc = 0$.

| step | $T_1$ | $T_2$ | effect |
|---|---|---|---|
| 1 | begin, start $= 0$ | begin, start $= 0$ | |
| 2 | $r_1(x) = 0$ | | $RS(T_1) = \{x\}$ |
| 3 | | $w_2(x, 5)$ | private |
| 4 | | serial validation | finish $= 0$, nothing to check; write $x = 5$; $tn(T_2) = 1$, $WS(1) = \{x\}$ |
| 5 | serial validation | | finish $= 1$; $WS(1) \cap RS(T_1) = \{x\}$: abort |
| 6 | restart as $T_3$, start $= 1$ | | |
| 7 | $r_3(x) = 5$ | | |
| 8 | serial validation | | finish $= 1$, the range $2..1$ is empty: commit, $tn(T_3) = 2$ |

$T_1$ read $x$ before $T_2$ wrote it, but $T_2$ got the smaller number, so $T_1$ would have to come after $T_2$ while it saw the old $x$; validation catches this. The restarted $T_3$ starts after number 1, so condition 1 covers $T_2$.

A case that passes: $T_4$ reads $y$, $T_5$ writes $x$ and commits first with number 3. When $T_4$ validates, $WS(3) = \{x\}$ and $RS(T_4) = \{y\}$ are disjoint, so $T_4$ commits with number 4. The serial order is $T_5, T_4$, and it is conflict equivalent because $T_4$ never touched $x$.

## Correctness

**Theorem.** With serial validation, the committed transactions are conflict equivalent to the serial schedule in the order of their transaction numbers.

*Sketch.* Take committed $T_i$ and $T_j$ with $tn(T_i) < tn(T_j)$ and a conflict on $x$. All writes to the database happen in write phases, which are serial and in number order, so a write-write conflict is ordered $T_i$ first. If $T_j$ reads $x$ and $T_i$ writes $x$: if $tn(T_i) \le T_j.start$, $T_i$ wrote before $T_j$ began, so the read follows the write; otherwise line L5 checked $WS(T_i) \cap RS(T_j)$ and found it empty, so there is no such conflict. If $T_i$ reads $x$ and $T_j$ writes $x$: $T_i$ read in its read phase, before its write phase, which precedes the write phase of $T_j$. So every conflict goes from the smaller number to the larger, and the [conflict graph](/conflict-graph/) is acyclic. The full proof, also for parallel validation, is in the correctness proof below.

**Parallel validation and the numbers.** With parallel validation the committed transactions are conflict serializable in the order in which they *entered validation* (line L8), and this order can differ from the order of the numbers. Example: $U$ reads $x$ and enters validation; $T$ writes $x$ only, enters validation, checks $WS(U) \cap (RS(T) \cup WS(T)) = \emptyset$, writes $x$ and finishes first, so $tn(T) < tn(U)$. $U$ then validates against numbers up to its own finish value, which does not include $T$, and commits. $U$ read $x$ before $T$ wrote it, so the only equivalent serial order is $U, T$. The implementation's tests find such runs at random and confirm that the order of entry is always a serial order.

## Complexity

For one transaction with read set size $r$, write set size $w$, and $k$ transactions that receive numbers or validate during its life:

- **Read phase.** $O(1)$ per operation with hash sets, the same as running without control.
- **Validation.** Line L5 tests $k$ write sets against $RS(T)$: with a hash set for $RS(T)$, $O(\sum |WS(n)|)$, at most $O(k w_{\max})$. Line L10 adds the same for the active set. Building the sets is $O(r + w)$.
- **Write phase.** $O(w)$.
- **Space.** $O(r + w)$ per transaction, plus the write sets of recent numbers. A write set can be dropped once no active transaction started before its number.

The critical section of serial validation is the whole of lines L4 to L7, which limits throughput to one write phase at a time. A restarted transaction repeats all its work, so under high contention the useful throughput can fall far below that of locking.

## Properties

- **No waiting and no deadlock.** No transaction ever waits for a lock, so there is no [deadlock](/deadlock/); the price is restarts.
- **Readers see committed data only.** Writes reach the database only in a write phase, after validation, so no transaction reads uncommitted data and no abort cascades.
- **Starvation is possible.** A long transaction can fail validation again and again. Kung and Robinson suggest running it in the critical section the next time.
- **Read-only transactions** need no write phase but must still validate their reads, unless they read a snapshot.
- **Backward validation** checks against committed transactions; the transaction that fails is always the one validating.

## Variants and improvements

- **Forward validation.** The validating transaction checks its write set against the read sets of transactions still in their read phase, and can choose which one to abort. Härder (1984) compared the two.
- **Timestamp-based validation in memory.** Silo and other in-memory databases keep a version number in each record, record the version read, and at commit lock the write set and check that each read version is unchanged. This is the same backward validation with per-record versions instead of transaction number ranges.
- **Software transactional memory.** [TL2](/tl2/) validates with a [global version clock](/global-version-clock/) and versioned locks, and [NoREC](/norec/) validates by comparing values. They are optimistic in the same way, but they run in memory with a [redo log](/redo-log/) and no durability, and they must also keep a running transaction from seeing an inconsistent state (opacity), which database OCC does not need because a read-phase transaction cannot harm anything before validation. [Transaction validation](/transaction-validation/) covers the cost of these checks.
- **Optimistic multiversion.** Hekaton combines validation with [multiversion concurrency control](/multiversion-concurrency-control/), so readers see a stable snapshot during the read phase.
- **Serializable snapshot isolation.** [SSI](/serializable-snapshot-isolation/) also validates at commit, but it checks for patterns of rw dependencies, not for every overlap of sets.

## When to use it

Use OCC when conflicts are rare, transactions are short, and waiting is expensive: read-mostly workloads, in-memory databases where a lock costs as much as the access, and systems where a client edits data for a long time between reads and writes (a web form with a version check at save is OCC). Prefer [two-phase locking](/two-phase-locking/) when many transactions update the same hot items, because restarts then waste more work than waits. Prefer [multiversion concurrency control](/multiversion-concurrency-control/) when long read-only transactions must not abort.

## Pitfalls

- **Assigning numbers at the start.** If the number is given when the transaction begins, line L5 cannot cover transactions that finish later. Kung and Robinson give the number after the write phase.
- **Validating outside the critical section in serial mode.** If two transactions validate at the same time and then both write, neither saw the other's write set. Serial validation must cover lines L4 to L7, or use the parallel form with the active set.
- **Forgetting the write-write test in parallel mode.** Line L10 must test $WS(T)$ against $WS(U)$ as well: overlapping write phases on the same item can leave the value of either one.
- **Reading the numbers as the serial order in parallel mode.** The equivalent order is the order of entry into validation, as the example in the correctness section shows.
- **Phantoms.** The read set holds the items read, not the predicate. A transaction that scanned a range must also detect inserts into the range, for example by validating the scan or a version of the index node.
- **Starvation.** Without a limit on restarts, a long transaction under load may never commit.

## Implementations

## History

H. T. Kung and John T. Robinson described optimistic methods at Carnegie Mellon University in a technical report of 1979 and in ACM Transactions on Database Systems in 1981. They argued that locking costs too much when conflicts are rare, gave the three conditions for serial equivalence with transaction numbers, and the serial and parallel validation algorithms. Analyses of the 1980s showed that OCC suffers under high contention, and locking stayed the norm in disk-based systems. Optimistic validation returned with main-memory databases (Hekaton, 2011; Silo, 2013) and with transactional memory, where waiting for locks costs more than an occasional restart.

## References
