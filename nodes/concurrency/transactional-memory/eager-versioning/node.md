---
tag: ZAQJVK
kind: concept
slug: eager-versioning
name: Eager versioning
aliases:
- direct update
- in-place update
- eager version management
area: concurrency/transactional-memory
level: advanced
summary: Writes go to memory in place, and an undo log keeps the old values for an abort. Commit is cheap and abort is dear; the writer must keep other transactions away from the words it wrote.
prereqs: [undo-log, software-transactional-memory]
see_also: [lazy-versioning, encounter-time-locking, eager-conflict-detection, tinystm, transaction-abort, privatization-safety, zombie-transactions, herlihy-moss-htm]
sources:
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 2 (version management, eager and lazy) and Chapter 4 (Software transactional memory)
  - paper: doi:10.1145/1345206.1345241
    title: "Pascal Felber, Christof Fetzer and Torvald Riegel, Dynamic performance tuning of word-based software transactional memory, PPoPP 2008, pages 237-246"
    locator: the write-through design of TinySTM, next to its write-back design
  - paper: "Ali-Reza Adl-Tabatabai, Brian T. Lewis, Vijay Menon, Brian R. Murphy, Bratin Saha and Tatiana Shpeisman, Compiler and runtime support for efficient software transactional memory, PLDI 2006"
    locator: an STM that updates memory in place and keeps an undo log
  - paper: "Kevin E. Moore, Jayaram Bobba, Michelle J. Moravan, Mark D. Hill and David A. Wood, LogTM, log-based transactional memory, HPCA 2006"
    locator: a hardware TM with eager version management, where new values go to memory and old values to a log in virtual memory
---

**Eager versioning** is the version management policy in which a transaction writes its new values straight into shared memory, at the time of each write, and keeps the old values in a private [undo log](/undo-log/). If the transaction commits, memory already holds the right values and the log is dropped. If it aborts, the old values are copied back. It is one of the three design axes of [software transactional memory](/software-transactional-memory/); its counterpart is [lazy versioning](/lazy-versioning/), which buffers the new values and writes them at commit. Eager versioning makes commit fast and reads simple, and makes abort slow. It also has a strong requirement: from its first write to a word until it ends, the transaction must keep every other transaction from reading or writing that word. In practice this means a write lock taken at the first write, that is, [encounter-time locking](/encounter-time-locking/). This page gives the policy; the undo log page gives the data structure.

## In plain words

The transaction changes the real data as it goes, and writes down on the side what each word held before. When it is done, it just throws the notes away. If it has to give up, it uses the notes to put everything back. While it runs, the real data holds values that may still be taken back, so nobody else may look at those words. The transaction locks each word before it changes it.

## The idea

**Notation and model.** $n$ is the number of processes, $r$ and $w$ the numbers of words a transaction reads and writes. The STM uses versioned write locks with atomic read, write and [compare-and-swap](/compare-and-swap/) (consensus number $\infty$), on a [sequentially consistent](/sequential-consistency/) memory.

A write by transaction $T$ to word $a$ does three things, in this order:

1. take the write lock of $a$, or abort (or wait) if another transaction holds it;
2. if this is $T$'s first write to $a$, append $(a, M[a])$ to $T$'s undo log;
3. write the new value into $M[a]$.

A read of $a$ by $T$ is a plain read of memory. If $T$ holds the lock of $a$, memory has $T$'s own value; there is no lookup in a log. If another transaction holds the lock, $T$ must not use the value: it waits or aborts.

At commit, $T$ validates its reads, releases its locks with a new version, and drops the log. At abort, it writes the old values back in reverse order and then releases its locks. A released lock must get a new version (not the old one), because a reader may have seen the value that was just undone; the [TinySTM](/tinystm/) test `test_write_through_abort_must_release_with_a_new_version` shows a reader that commits an inconsistent snapshot when the old version is restored.

### What it costs

| Event | Eager versioning | [Lazy versioning](/lazy-versioning/) |
|---|---|---|
| write | lock, log the old value, write memory | append to the redo log |
| read of a word the transaction wrote | plain read | look up the redo log |
| read of another word | plain read and lock check | look up the redo log, then read and check |
| commit | release $w$ locks | lock $w$ words (or hold them), write back $w$ values, release |
| abort | write back $w$ old values, release | drop the log, release |
| lock hold time | from the first write to the end | from the commit start to the end (with commit-time locking) |

The trade is clear. Eager versioning is faster when most transactions commit and when they often read what they wrote. Lazy versioning is faster when aborts are common, and it holds locks for a shorter time.

### Why eager versioning needs early locks

With eager versioning, memory holds uncommitted values. If another transaction could read them, it could see a value that is later undone (a dirty read), and an opaque STM must prevent that. If another transaction could write the word, then a rollback would wipe out its write. The undo log tests `test_without_a_write_lock_another_reader_sees_a_value_that_is_undone` and `test_without_a_write_lock_a_rollback_wipes_out_another_write` show both runs. So eager versioning implies that write-write conflicts and write-read conflicts are found at the access: it forces [eager conflict detection](/eager-conflict-detection/) for writes. Read-write conflicts (a writer that comes after an invisible reader) can still be found late, by validation.

## Examples

**A transfer in TinySTM's write-through mode.** Two accounts hold $a_0 = a_1 = 10$, and $T$ moves 3 from $a_0$ to $a_1$. $T$ reads both (two lock checks and two reads), then writes $a_0$: it locks $a_0$, logs $(a_0, 10)$ and writes 7. Then it writes $a_1$: it locks, logs $(a_1, 10)$ and writes 13. At commit it takes a new version from the clock and releases both locks with it. Run alone, this costs 18 shared steps in the simulation, against 16 for the write-back mode, which writes memory only at commit. If $T$ aborts after its second write, it writes 10 back into $a_1$ and then into $a_0$: two more shared writes that the write-back mode would not need.

**A reader meets a writer.** $T$ has written $a_0 \leftarrow 7$ in place and holds the lock. An audit $U$ reads $a_0$. It sees the lock is held by another transaction, so it does not use the 7: it aborts, or in some STMs waits for $T$ to end. If $U$ ignored the lock and $T$ then aborted, $U$ would have read a value that was never committed.

**Hardware.** LogTM (Moore et al., HPCA 2006) is a hardware TM with eager versioning: new values go to the cache and memory, and old values go to a log in virtual memory that the hardware fills. Commits are fast; aborts run a handler that walks the log. [Herlihy and Moss](/herlihy-moss-htm/) used the other choice, keeping new values in a transactional cache.

## Where it is used

- The write-through mode of [TinySTM](/tinystm/) (2008).
- The McRT-STM of Saha et al. (2006) and the STM with compiler support of Adl-Tabatabai et al. (PLDI 2006), which were designed for fast commits in managed languages.
- GCC's libitm, whose software methods `ml_wt` and `gl_wt` write through to memory and keep an undo log.
- Hardware TMs in the LogTM family.
- Databases, where in-place update with an undo log is the usual design ([write-ahead logging](/write-ahead-logging/)).

Eager versioning is less common in STMs that must be [privatization safe](/privatization-safety/): a doomed transaction that writes in place can change data that another thread has just made private, and the later rollback writes old values into it. Its in-place writes also make [zombie transactions](/zombie-transactions/) more dangerous, since a zombie can write to memory that others read without the STM.

## References
