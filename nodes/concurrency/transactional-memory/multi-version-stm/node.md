---
tag: 0DZJAM
kind: concept
slug: multi-version-stm
name: Multi-version STM
aliases:
- multiversion STM
- MVSTM
- multi-versioned STM
- versioned boxes
area: concurrency/transactional-memory
level: research
summary: An STM that keeps old versions of each word, so a read-only transaction reads a consistent snapshot and never aborts. The price is the space of the versions that live readers still need.
prereqs: [global-version-clock, multiversion-concurrency-control]
see_also: [tl2, opacity, snapshot-isolation, transaction-validation, disjoint-access-parallel-stm-lower-bound, epoch-based-reclamation, transaction-abort, software-transactional-memory]
sources:
  - paper: doi:10.1016/j.scico.2006.05.009
    title: "João Cachopo and António Rito-Silva, Versioned boxes as the basis for memory transactions, Science of Computer Programming 63(2), 2006, pages 172-185"
    locator: versioned boxes, the read-only transactions of JVSTM that never abort, and the commit of write transactions
  - paper: doi:10.1007/11864219_20
    title: "Torvald Riegel, Pascal Felber and Christof Fetzer, A lazy snapshot algorithm with eager validation, DISC 2006, LNCS 4167, pages 284-298"
    locator: the validity range of a snapshot, and the use of older versions of an object to keep a snapshot valid
  - paper: "Dmitri Perelman, Rui Fan and Idit Keidar, On maintaining multiple versions in STM, PODC 2010, pages 16-25"
    locator: how many versions an STM must keep so that read-only transactions do not abort, and selective multi-versioning (SMV)
  - paper: "Sérgio Miguel Fernandes and João Cachopo, Lock-free and scalable multi-version software transactional memory, PPoPP 2011"
    locator: a JVSTM whose commit takes no global lock
  - paper: doi:10.1145/1345206.1345233
    title: "Rachid Guerraoui and Michał Kapałka, On the correctness of transactional memory, PPoPP 2008, pages 175-184"
    locator: Section 6 (the lower bound for single-version opaque TMs with invisible reads, which multi-version STMs do not meet the conditions of)
  - url: https://clojure.org/reference/refs
    title: Clojure reference, Refs and Transactions
    locator: refs, implemented with multiversion concurrency control and history queues for snapshot isolation
---

A **multi-version STM** is a [software transactional memory](/software-transactional-memory/) that keeps, for each word or object, a list of its recent committed values, each labelled with the time of the commit that wrote it. A transaction takes a start time $rv$ from a [global version clock](/global-version-clock/) and reads, in each list, the newest value labelled at most $rv$. All its reads then come from the state of memory at time $rv$, a consistent snapshot, whatever other transactions commit meanwhile. So a transaction that only reads never has to abort and never has to [validate](/transaction-validation/): its snapshot stays valid forever. A single-version STM such as [TL2](/tl2/) has only the newest value, and must abort a reader that meets a value written after it began. The idea is the [multiversion concurrency control](/multiversion-concurrency-control/) of databases, brought to memory transactions; JVSTM (Cachopo and Rito-Silva, 2006) and the multi-version form of LSA (Riegel, Felber and Fetzer, 2006) are early examples. The cost is space: an old version must stay as long as some running transaction may read it, so one long reader can hold a version of every word that changes during its run.

## In plain words

Imagine a notice board where nobody ever erases a notice. When a notice changes, the new text is pinned on top with the date, and the old one stays underneath. A reader who came in on Monday reads, for each topic, the newest notice dated Monday or earlier, and ignores anything pinned later. What the reader sees is exactly the board as it was on Monday, so it all fits together, even if people are pinning new notices while the reader reads. The reader never has to start again. A writer still has to check, at the end, that nothing they read has been replaced since, because what they write must fit the board as it is now. The board fills up, so someone must take down old notices, but only those that no reader still in the room could want.

## The idea

**Versioned boxes.** Each word $a$ holds a list of pairs (version, value), newest first. A global clock $G$ holds the version of the last committed update. In JVSTM the list is called a *versioned box*.

**Reading.** A transaction $T$ reads $rv \leftarrow G$ once, at begin. To read $a$ it walks the list of $a$ and returns the first value with version $\le rv$. It records $a$ in its read set only if it may write later.

**Committing an update.** In the simplest design, which is the design of the first JVSTM and of the code on this page, a writer takes one global commit lock. It validates: every word it read must still have its newest version $\le rv$, or it aborts. It sets $wv = G + 1$, pushes (wv, new value) onto the list of each word it wrote, then publishes $G \leftarrow wv$, and releases the lock. Publishing $G$ last is what makes every version $\le rv$ complete: a reader can see a label $\le rv$ only after the whole commit that wrote it is in place.

**Committing a read-only transaction.** Nothing to do. There is no validation, no shared write, and no abort.

**Why the reads are consistent.** Every version a reader returns was published by a commit with $wv \le rv$, so before the reader read $G$. Every version it skips has $wv > rv$, so it was published after. Hence the reader sees exactly the commits with $wv \le rv$: the state at time $rv$. The serial order that explains it puts the reader just after the commit $wv = rv$. A read-only transaction may thus be ordered before update transactions that ended earlier in real time than it did. This is allowed by [opacity](/opacity/), because the reader began before they committed (see Example 2 of the opacity page). Update transactions are ordered at their commit, and their validation makes that order legal.

**The two lower bounds it avoids.** Guerraoui and Kapałka (PPoPP 2008) proved that a single-version, opaque, progressive STM with invisible reads needs $\Omega(k)$ steps for some read of a transaction that reads $k$ objects. A multi-version STM is outside the single-version condition: a read is one look at a list, with no validation. The [disjoint-access-parallel lower bound](/disjoint-access-parallel-stm-lower-bound/) still applies; a global clock, as here, is not disjoint-access parallel.

**How many versions to keep.** The code on this page has three policies, and the tests measure them:

- **Keep all.** Space grows with every committed write and never shrinks.
- **Keep the newest $k$.** Space is at most $k$ per word. With $k = 1$ the STM is single-version. A reader that needs a version that has been dropped aborts, so the promise of no aborts is lost.
- **Keep what live transactions need.** Each process announces its $rv$ in a shared slot. A writer keeps every version newer than the oldest announced $rv$ (or than $G$, whichever is smaller), plus the newest version at or below it. Readers never abort, and space follows the oldest live snapshot. A reader announces $rv$ and then reads $G$ again; if $G$ moved, it takes the new value and announces again. This closes the window in which a writer could miss a reader that has read $G$ but not yet announced it. The same pattern of announce, then check, appears in [hazard pointers](/hazard-pointers/), and the policy is a form of [epoch-based reclamation](/epoch-based-reclamation/) for versions.

Perelman, Fan and Keidar (PODC 2010) studied this question formally. They showed that keeping a fixed number of versions per object cannot ensure that read-only transactions never abort, and gave selective multi-versioning (SMV), which keeps an old version only while some running transaction may still read it, the same goal as the third policy.

### Measurements

All counts come from the simulation on this page, with shared memory steps counted as atomic.

**A long reader.** A read-only transaction reads $a_0$ of two accounts. Then five transfers commit one after another, each writing $a_0$ and $a_1$. Then the reader reads $a_1$, and a sixth transfer commits.

| Policy | Result of the reader | Versions of $a_1$ when the reader reads it | Versions of $a_1$ at the end | Largest total |
|---|---|---|---|---|
| Keep all | 20 (commits) | 6 | 7 | 14 |
| Keep what live readers need | 20 (commits) | 6 | 2 | 12 |
| Keep the newest 1 | aborts | 1 | 1 | 2 |

The reader pins versions 0 to 5 of $a_1$ while it runs: one per commit during its life. When it ends, the next writer trims the list to two.

**Random runs.** 80 seeded runs of five processes on three accounts: three transfers, retried until they commit, and two audits that read all three accounts.

| Policy | Aborts of the audits | Largest total of versions | Longest list |
|---|---|---|---|
| Keep all | 0 | 9 | 3 |
| Keep what live readers need | 0 | 7 | 3 |
| Keep the newest 2 | 0 | 6 | 2 |
| Keep the newest 1 | 19 | 3 | 1 |

Every audit returned 30, the bank invariant. With one version, the audits aborted 19 times. With two versions, no audit aborted in these runs, but a bound of $k$ versions fails as soon as $k$ commits to one word fall inside the life of one reader; the long-reader table shows it for $k = 1$, and the exhaustive search finds such a schedule.

**Cost of a read.** A read-only transaction of $r$ reads takes $1 + r$ shared steps (one read of $G$, one read per list), plus 3 steps for the announce, the check and the final retire under the third policy. It does no validation. The walk down a list is local work on the list that one read returned.

## Examples

**1. The old version saves the reader.** Two accounts hold 10 each. An audit reads $G = 0$ and $a_0 = 10$. A transfer of 3 commits with version 1: $a_0 = 7$, $a_1 = 13$. The audit reads the list of $a_1$, which is ((1, 13), (0, 10)). It skips version 1 because $1 > rv = 0$ and returns 10. The sum is 20, the correct total at time 0, and the audit commits. In a single-version STM, the list is only ((1, 13)); there is no version $\le 0$, and the audit must abort. Both runs are opaque; only the first commits.

**2. A writer still validates.** Two transactions with $rv = 0$ run `y ← x + 1` and `x ← y + 1`. Each reads 0 from its snapshot. The first commits $y = 1$ with version 1. The second takes the lock and finds that the newest version of $y$ is $1 > rv$, so it aborts and retries with $rv = 1$, reading $y = 1$ and writing $x = 2$. Without the validation, both would commit with $x = y = 1$, which is write skew: that is [snapshot isolation](/snapshot-isolation/), not serializability.

**3. A non-example.** A multi-version STM in which update transactions do not validate their reads gives snapshot isolation. It is useful, and some systems choose it, but it is not opaque and not serializable, as Example 2 shows.

## Where it is used

- **JVSTM** (Cachopo and Rito-Silva, 2006), a Java library built on versioned boxes. Read-only transactions never abort. Later versions commit without a global lock (Fernandes and Cachopo, PPoPP 2011).
- **LSA** (Riegel, Felber and Fetzer, 2006) can keep several versions of an object, so that a transaction can find a version inside the validity range of its snapshot instead of aborting.
- **Clojure refs** use multiversion concurrency control with history queues and give snapshot isolation. The `ensure` operation is there to prevent write skew when it matters.
- **Databases**, where [multiversion concurrency control](/multiversion-concurrency-control/) is the common design, and where the same space problem appears as long-running queries that hold back the clean-up of old row versions.
- **Read-mostly workloads** in general, such as long traversals and queries of a shared structure while a few short writers update it: these are the cases where single-version STMs abort the long readers again and again.

## References
