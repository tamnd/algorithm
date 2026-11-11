---
tag: H6Z98Q
kind: concept
slug: lazy-conflict-detection
name: Lazy conflict detection
aliases:
- commit-time conflict detection
- late conflict detection
- optimistic conflict detection
area: concurrency/transactional-memory
level: advanced
summary: Deferring conflict detection to commit time. More transactions can finish, since a conflict may resolve itself, but a doomed transaction runs to its end before it aborts.
prereqs: [transaction-conflict, software-transactional-memory]
see_also: [eager-conflict-detection, commit-time-locking, lazy-versioning, transaction-validation, tl2, norec, zombie-transactions, optimistic-concurrency-control]
sources:
  - paper: doi:10.1007/11864219_13
    title: "Michael F. Spear, Virendra J. Marathe, William N. Scherer III and Michael L. Scott, Conflict detection and validation strategies for software transactional memory, DISC 2006, LNCS 4167, pages 179-193"
    locator: the comparison of eager, lazy and mixed acquisition, and of visible and invisible reads
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 2 (conflict detection, eager and lazy) and Chapter 4 (Software transactional memory)
  - paper: doi:10.1007/11864219_14
    title: "Dave Dice, Ori Shalev and Nir Shavit, Transactional Locking II, DISC 2006, LNCS 4167, pages 194-208"
    locator: Section 2.1 (write locks taken at commit, then validation of the read set)
  - paper: doi:10.1145/319566.319567
    title: H. T. Kung and John T. Robinson, On optimistic methods for concurrency control, ACM Transactions on Database Systems 6(2), 1981
    locator: the read, validation and write phases of an optimistic transaction
---

**Lazy conflict detection** looks for [transaction conflicts](/transaction-conflict/) only when a transaction tries to commit. Until then the transaction runs on, even if another transaction has written a word it read or is about to write a word it wrote. At commit, the transaction locks its write set and [validates](/transaction-validation/) its read set; if a conflict has made its reads stale, it [aborts](/transaction-abort/). It is one end of the conflict detection axis of [software transactional memory](/software-transactional-memory/), opposite to [eager conflict detection](/eager-conflict-detection/). Lazy detection lets more transactions commit, because many conflicts resolve themselves before commit: the other transaction aborts, or commits in an order that does no harm. Its costs are that a doomed transaction runs to its end before it learns its fate, and that a transaction that is not checked before commit can run on an inconsistent state, a [zombie](/zombie-transactions/). Pure lazy detection therefore needs extra checks during the run to be [opaque](/opacity/). Spear, Marathe, Scherer and Scott (DISC 2006) compared lazy, eager and mixed detection and found that no single choice is best on all workloads.

## In plain words

Each transaction works on its own and does not look at what the others do. Only at the end, before it makes its changes public, does it check whether anything it read has changed in the meantime. If so, it starts over; if not, it commits. This lets transactions that touch the same data still both finish, as long as their order works out. The downside is that a transaction whose data changed early keeps working until the end, and all that work is lost.

## The idea

**Notation and model.** $n$ is the number of processes, $r$ and $w$ the numbers of words a transaction reads and writes. The STM uses versioned locks or a global sequence lock, with atomic read, write and [compare-and-swap](/compare-and-swap/), on a [sequentially consistent](/sequential-consistency/) memory.

A lazy transaction runs in three phases, the same as an optimistic database transaction ([optimistic concurrency control](/optimistic-concurrency-control/), Kung and Robinson 1981):

1. **Read phase.** Reads go to memory (after a look in the private log); writes go to a [redo log](/redo-log/). No lock is taken, so no other transaction can see this one.
2. **Validation.** At commit, take the write locks of the write set ([commit-time locking](/commit-time-locking/)) or one global lock, then check that each word in the read set still has the value or version seen.
3. **Write phase.** Write back the redo log and release the locks.

Lazy detection needs [lazy versioning](/lazy-versioning/): with in-place writes, memory would hold uncommitted values, and WR and WW conflicts would have to be caught at the access.

### Why many conflicts resolve themselves

Two transactions $T$ and $U$ conflict, but only the conflicts in which the loser has to see the winner's commit force an abort:

- If $T$ read $x$ and $U$ writes $x$, and $T$ commits before $U$ does, then the order "$T$ then $U$" works and both commit. An eager STM with visible reads would have stopped one of them.
- If $T$ and $U$ both write $x$ without reading it (blind writes), whichever commits second simply wins.
- If $U$ aborts for another reason, $T$ never needed to react.

### The costs

- **Waste.** A transaction whose read became stale early runs to its commit before it aborts. The longer the transaction, the more work is lost.
- **Zombies.** Between the conflict and its commit, the transaction may read a mix of old and new values. Code that relies on an invariant can then loop, divide by zero or follow a bad pointer. To be opaque, a lazy STM must check its reads during the run as well: [TL2](/tl2/) checks each read against a [global version clock](/global-version-clock/), and [NOrec](/norec/) validates by value whenever the global sequence number has changed. So in practice "lazy" refers to when the conflict is *resolved*, while reads are still checked as they happen.
- **Starvation of long transactions.** A long transaction can be invalidated again and again by short ones that commit first. Lazy STMs have no point before commit at which a contention manager could protect it.
- **Commit work.** The commit takes the locks and checks the whole read set, so it is longer than in an eager STM.

## Examples

The runs come from the simulations of the [TL2](/tl2/), [TinySTM](/tinystm/) and [SwissTM](/swisstm/) pages, with one attempt per transaction.

**Both commit.** $T_1$ writes $x \leftarrow 1$, then reads $a_0, \dots, a_4$. Right after $T_1$'s write, $T_2$ reads $x$, writes $x \leftarrow x + 10$ and commits. In TL2, which detects WW conflicts lazily, $T_2$ commits with $x = 10$ and then $T_1$ commits with $x = 1$; the order "$T_2$ then $T_1$" explains the run, and the checker confirms that it is opaque. In TinySTM and SwissTM, which take write locks at the write, $T_2$ aborts.

**A doomed transaction runs on.** $T_1$ reads $x$, then reads $a_0, \dots, a_4$, then writes $y$. After its read of $x$, $T_2$ writes $x \leftarrow 7$ and commits. $T_1$'s read of $x$ is now stale, but $T_1$ does not know: it spends 20 more steps in TL2 before its commit validation fails and it aborts. Since the reads of $a_i$ find versions older than $T_1$'s start, TL2's per-read check passes them, and the conflict is found only at commit.

**A zombie without per-read checks.** $T_1$ keeps $x = y$ and changes both from 0 to 1. $T_2$ reads $x = 0$, then $T_1$ commits, then $T_2$ reads $y = 1$. With checks only at commit, $T_2$ now runs with $x \neq y$. The [DSTM](/dstm/) test `test_without_validation_at_each_open_a_zombie_sees_x_ne_y` and the TL2 test `test_without_post_validation_a_read_only_transaction_commits_an_inconsistent_snapshot` show such runs; see [zombie transactions](/zombie-transactions/).

## Where it is used

- [TL2](/tl2/) (2006): commit-time locks and commit-time validation, plus a version check at each read for opacity.
- [NOrec](/norec/) (2010): no locks until commit; one global sequence lock serializes the commits.
- [SwissTM](/swisstm/) (2009): lazy for read-write conflicts, eager for write-write conflicts.
- Haskell's STM, which validates at commit and, in the GHC runtime, also from time to time while a transaction runs.
- Some hardware proposals, such as TCC (Hammond et al., 2004), detect conflicts at commit by broadcasting the write set.
- [Optimistic concurrency control](/optimistic-concurrency-control/) in databases is the same idea for disk-based transactions.

## References
