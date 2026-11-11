---
tag: VVC9F1
kind: technique
slug: global-version-clock
name: Global version clock
aliases:
- GV clock
- global version-clock
area: concurrency/transactional-memory
level: advanced
summary: A shared counter that stamps each committed write, so a transaction checks each read once against its start time. TL2 and LSA use it; the one hot word limits how far it scales.
prereqs: [transaction-validation, fetch-and-add]
see_also: [tl2, tinystm, swisstm, norec, multi-version-stm, opacity, timestamp-ordering, lamport-clocks]
sources:
  - paper: doi:10.1007/11864219_14
    title: "Dave Dice, Ori Shalev and Nir Shavit, Transactional Locking II, DISC 2006, LNCS 4167, pages 194-208"
    locator: Section 2.1 (the global version-clock, the read version rv, the write version wv, and the skip of validation when rv + 1 = wv)
  - paper: doi:10.1007/11864219_20
    title: "Torvald Riegel, Pascal Felber and Christof Fetzer, A lazy snapshot algorithm with eager validation, DISC 2006, LNCS 4167, pages 284-298"
    locator: the global time base, the validity range of a snapshot, and its extension by validation
  - url: https://github.com/ccaominh/tl2-x86/blob/master/RELEASENOTES
    title: Dave Dice, Ori Shalev and Nir Shavit, release notes of the TL2 code, 2006
    locator: the clock schemes GV4, GV5 and GV6, and the invariant that a computed WV must be greater than any RV read before
  - paper: "Yossi Lev, Victor Luchangco, Virendra J. Marathe, Mark Moir, Dan Nussbaum and Marek Olszewski, Anatomy of a scalable software transactional memory, TRANSACT 2009"
    locator: the discussion of the global clock schemes of the TL2 code release
  - paper: "Hillel Avni and Nir Shavit, Maintaining consistent transactional states without a global clock, SIROCCO 2008"
    locator: thread-local clocks (TLC) as a replacement for the global clock
  - paper: "Torvald Riegel, Christof Fetzer and Pascal Felber, Time-based transactional memory with scalable time bases, SPAA 2007"
    locator: time bases built from synchronized hardware clocks instead of one shared counter
  - paper: doi:10.1007/11864219_13
    title: "Michael F. Spear, Virendra J. Marathe, William N. Scherer III and Michael L. Scott, Conflict detection and validation strategies for software transactional memory, DISC 2006, LNCS 4167, pages 179-193"
    locator: the global commit counter, a clock that only says whether some transaction has committed
---

A **global version clock** is one shared integer $G$ that a [software transactional memory](/software-transactional-memory/) uses as a time base. A transaction reads $G$ when it begins and keeps the value as its *read version* $rv$. A writing transaction takes a *write version* $wv$ from $G$ at commit and stamps every word it writes with $wv$. A reader then needs only one look at each word: a stamp no larger than $rv$ means the value was there before the reader began, and a larger stamp means it was written later, so the reader aborts. This replaces the repeated scans of the read set that incremental [validation](/transaction-validation/) needs, and it gives [opacity](/opacity/) (every transaction, also one that aborts, sees values from one serial order that respects real time) at a cost of $O(1)$ per read. The idea appeared twice at DISC 2006: in [TL2](/tl2/) by Dice, Shalev and Shavit, and in the lazy snapshot algorithm (LSA) by Riegel, Felber and Fetzer. Its price is that every writing transaction touches the same word, so the clock becomes a point of contention on many cores. The TL2 code release has three schemes, GV4, GV5 and GV6, that write the clock less often.

## In plain words

Think of a ticket counter at a shop. Each customer who changes something takes the next ticket number and writes it on what they changed. A customer who only looks around notes the number on the display when they walk in. Anything they find with a higher ticket number was changed after they came in, so what they have seen may no longer fit together, and they start again. Anything with a lower or equal number was changed before they came in and fits with everything else they saw. Nobody has to walk back and recheck old items. The trouble is that every writer must use the same ticket machine, and on a large machine with many cores that one machine becomes a queue.

## When it applies

- The STM has **invisible reads** and keeps **one version** per word, so readers must validate. With visible reads, writers find their readers and no clock is needed for safety.
- Each word, or each stripe of words, has a **versioned lock**: a version number and an owner, in one word that can be read atomically.
- Writers take their locks **before** they take $wv$. This is what makes a stamp $\le rv$ trustworthy; see the lemma below. TL2 takes them at commit ([commit-time locking](/commit-time-locking/)); [TinySTM](/tinystm/) takes them at the first write ([encounter-time locking](/encounter-time-locking/)). Both take $wv$ only at commit.
- The clock must be **monotone**: it never goes back, and the versions written must stay below the range of the counter. A 64 bit counter at $10^9$ commits per second lasts about 584 years.
- The cost of one shared read-modify-write per update commit is acceptable, or one of the schemes below is used to cut it.

## The template

**Notation and model.** $n$ processes share data words $M[a]$, a clock word $G$ (initially 0) and one versioned lock $\ell(a) = (\text{version}, \text{owner})$ per word, with owner free or a transaction. The steps are atomic read, write, [compare-and-swap](/compare-and-swap/) (consensus number $\infty$) and [fetch-and-add](/fetch-and-add/) (consensus number 2), on a [sequentially consistent](/sequential-consistency/) memory. A transaction $T$ keeps a read set $RS(T)$ and a write set $WS(T)$ ([read and write sets](/read-set-and-write-set/)); writes go to a private [redo log](/redo-log/) and reach memory only at commit. The template is TL2 with four ways to produce $wv$:

- **GV1**, the clock of the DISC paper: $wv = \text{FAA}(G, 1) + 1$ at each update commit.
- **GV4**: one CAS from $g$ to $g + 1$. If it fails, some other committer has just moved $G$, and this committer uses the value now in $G$. Two committers may then share one $wv$; this is safe because both hold their locks at the same time, so their write sets do not meet.
- **GV5**: no write to $G$ at commit; $wv = G + 1$. Versions can run one ahead of $G$. A reader that meets a version above its $rv$ aborts, and raises $G$ before it retries, so that the retry can read the word.
- **GV6**: GV4 at some commits and GV5 at the others. The release notes describe a random choice of about one commit in $N$; the code on this page uses every $N$-th commit, which is deterministic.

```pseudo id=main
BEGIN(T)
L1  rv ← G                                                  ▷ the start time of T
READ(T, a)                                                  ▷ after the look-up in WS(T)
L2  (v1, o1) ← ℓ(a); x ← M[a]; (v2, o2) ← ℓ(a); if o1 ≠ free or (v1, o1) ≠ (v2, o2) then ABORT
L3  if v1 > rv then                                         ▷ written after T began
L4      if clock is GV5 or GV6 then g ← G; if g < v1 then CAS(G, g, v1)   ▷ the abort-time increment
        ABORT
    add a to RS(T); return x
COMMIT(T)                                                   ▷ a read-only T returns at once
L5  lock each word of WS(T) with CAS, or ABORT
L6  GV1: wv ← FAA(G, 1) + 1; own ← true
L7  GV4: g ← G; if CAS(G, g, g + 1) then wv ← g + 1; own ← (clock is GV4) else wv ← G; own ← false
L8  GV5: wv ← G + 1; own ← false                            ▷ GV6 runs L7 at one commit in N, L8 at the others
L9  if own and wv = rv + 1 then go to L11                   ▷ nobody committed since T began
L10 for each a in RS(T): if ℓ(a) is owned by another, or its version > rv, then ABORT
L11 write back WS(T); release each lock of WS(T) with version wv
```

**Read (L1 to L4).** The two samples of the lock around the load (L2) give a value and a version that belong together, as in a sequence lock. The test at L3 is the whole point of the clock: one comparison per read, with no scan of earlier reads.

**Commit (L5 to L11).** The locks come first (L5), then the clock (L6 to L8), then validation (L10), then write-back and release (L11). The order of L5 before L6 to L8 is what the safety lemma needs.

### Why a stamp no larger than rv can be trusted

**Lemma.** Let $T$ read $G = rv$ at L1, and let $W$ be a writer that takes its first lock after that step. Then $W$ commits, if it does, with $wv > rv$.

*Proof.* $W$ reads or changes $G$ at L6 to L8, after its locks, so after the L1 step of $T$. $G$ never decreases, so $W$ sees a value $g \ge rv$. Under GV1 and under a GV4 CAS that succeeds, $wv = g + 1 > rv$. Under a GV4 CAS that fails, $G$ has moved away from $g$, and since it only grows, $wv = G > g \ge rv$. Under GV5, $wv = G + 1 > G \ge rv$. $\square$

The TL2 release notes state this as the safety invariant of all the schemes: any computed $wv$ must be greater than any $rv$ read before. The rest of the argument goes like this. A value that $T$ accepts has a stamp $\le rv$, so by the lemma its writer $W$ took all its locks before $T$ began. $W$ keeps those locks until its release at L11, so each read by $T$ of a word of $W$ finds either the lock (and $T$ aborts at L2) or the final value of $W$. Writers that locked after $T$ began have stamps $> rv$, and $T$ rejects all their values at L3. So the reads of $T$ all come from one state: the one in which the early writers have finished and the late ones have not started. This holds at each read, not only at commit, which is why the template is opaque.

### When the commit may skip validation

TL2 skips the validation at L10 when $wv = rv + 1$. Under GV1 this is sound: every commit does an FAA, so $wv = rv + 1$ means that no other transaction drew a version between the L1 of $T$ and its own FAA. A writer that changed a word in $RS(T)$ after $T$ read it locked that word after $T$ began, so it drew its version after $T$ began; it drew it after $T$ did, and it is ordered after $T$. Under pure GV4 a CAS winner can skip for the same reason, because every commit moves $G$ (a loser borrows only after some winner moved it); the exhaustive tests on this page support this, but the argument there is longer. Under GV5 and GV6 the rule fails, because a GV5 commit leaves $G$ unchanged, so $wv = rv + 1$ says nothing about the commits in between. The release notes state the invariant above but do not discuss this shortcut; the bad runs in the pitfalls were found by the exhaustive search of the implementation.

### Cost

A read takes 3 shared steps and one comparison. A read-only transaction takes $1 + 3r$ steps and never validates. An update commit takes 2 steps per lock, 1 or 2 clock steps (FAA; or read and CAS; or one read), at most $r$ lock reads for validation, and $2w$ writes. In a solo run of a bank transfer ($r = w = 2$) the implementation takes 16 shared steps under GV1 and GV5 and 17 under GV4, where the extra step is the read before the CAS.

The step count hides the real cost. Under GV1 every update commit does a read-modify-write on the same word. On a machine with cache coherence, that moves the cache line of $G$ to the core of the committer, so all commits on all cores pass, one at a time, through one line, even when their data are disjoint. Every transaction also reads $G$ at begin, and that read misses in the cache after each commit. This is the contention that GV4 to GV6 attack: GV4 keeps the read-modify-write but lets a failed CAS end the commit at once instead of retrying; GV5 removes the write at commit and pays with extra aborts; GV6 mixes the two.

The simulation cannot show cache traffic, but it shows the other side of the trade. Over 80 seeded random runs of five processes on three accounts (three transfers and two audits, 400 commits, 240 of them updates):

| Scheme | CAS or FAA on $G$ at commit | Raises of $G$ by aborting readers | Aborts | Commits that skipped L10 |
|---|---|---|---|---|
| GV1 | 255 | 0 | 731 | 238 |
| GV4 | 249 | 0 | 797 | 236 |
| GV5 | 0 | 179 | 1112 | 0 |
| GV6 ($N = 4$) | 22 | 171 | 1111 | 0 |

GV1 does 255 clock writes for 240 update commits: 15 commits drew a version and then failed validation. GV5 writes the clock only when a reader aborts, but it aborts about 1.5 times as often, because a fresh transaction starts with $rv = G$ while recent stamps are $G + 1$, so it rejects values that GV1 would accept.

## Classic examples

- **TL2** (Dice, Shalev and Shavit, DISC 2006) introduced the clock with commit-time locking, the check at L3 and the skip when $rv + 1 = wv$. Read-only transactions keep no read set at all.
- **LSA** (Riegel, Felber and Fetzer, DISC 2006) uses the same kind of time base to give each snapshot a validity range. When a read meets a newer version, LSA tries to *extend* the snapshot: it reads $G$ again, validates the read set, and on success moves $rv$ forward instead of aborting.
- **[TinySTM](/tinystm/)** and **[SwissTM](/swisstm/)** use a global clock with encounter-time locks and LSA-style snapshot extension.
- **[Multi-version STMs](/multi-version-stm/)** such as LSA-STM and JVSTM label each kept version with a clock value, so a read-only transaction can always find the version that was current at its $rv$ and never aborts.
- **[NOrec](/norec/)** keeps one global sequence lock that is both the clock and the commit lock. A change of it tells readers only that some transaction committed; they then validate by value. The global commit counter of Spear et al. (DISC 2006) is the same idea used only as a hint.
- In databases, [timestamp ordering](/timestamp-ordering/) and [multiversion concurrency control](/multiversion-concurrency-control/) draw transaction timestamps from one counter for the same reason. [Lamport clocks](/lamport-clocks/) solve a different problem: they order events across processes that share no counter.

## Variations

- **GV4, GV5 and GV6.** These are the schemes of the TL2 release notes, described above. GV4 reduces retries on the clock, GV5 removes the clock write from commit, and GV6 trades between them. Lev et al. (TRANSACT 2009) discuss them in their account of a scalable STM.
- **Snapshot extension.** With LSA, a reader that meets a version above $rv$ validates and moves $rv$ up instead of aborting. It turns many aborts at L3 into one scan.
- **Thread-local clocks.** Avni and Shavit (SIROCCO 2008) proposed thread-local clocks (TLC), which keep transactional states consistent with no shared counter.
- **Hardware time bases.** Riegel, Fetzer and Felber (SPAA 2007) built time bases from synchronized hardware clocks, which every core can read without a shared write.
- **Scalable counters.** A [combining tree](/combining-tree/) or a [sloppy counter](/sloppy-counter/) spreads the increments, but the clock needs every reader to see a value at least as large as every stamp already written, which these structures do not give directly.

## Pitfalls

- **Taking $wv$ before the locks.** If a writer draws $wv$ and then locks, a reader can begin between the two, get $rv \ge wv$, read the old value, and later accept new values of the same writer with stamp $wv \le rv$. The lemma needs L5 before L6 to L8.
- **The skip with a shared or computed $wv$.** Under GV5, two transactions with $rv = 0$ run `y ← x + 1` and `x ← y + 1`. Both read 0, both compute $wv = G + 1 = 1 = rv + 1$, both skip L10, and both commit with $x = y = 1$. No serial order gives that (it gives 1 and 2): this is write skew. With the rule of L9 the second commit validates, finds $\ell(x)$ at version $1 > rv$, and aborts. The same run with GV4 needs one lost CAS: the loser borrows $wv = 1$ and skips. Under GV6 even a CAS winner must not skip; the exhaustive search finds a run where a GV5 commit of $y$ sits between $rv$ and the winning CAS.
- **GV5 with no abort-time increment.** If an aborting reader does not raise $G$ (L4), a stamp of $G + 1$ stays above every new $rv$, and every retry that reads that word aborts again until some other event moves $G$.
- **Assuming the stamp changes on every write.** Under GV5 and GV6 a word can be rewritten with the stamp it already had. The template is still safe, by the lemma: a reader whose $rv$ admits that stamp began after the writer locked the word, so it sees the lock or the new value. Code that uses the stamp alone to detect a change, with no lock bit, must not rely on it.
- **Placing $G$ next to other hot data.** The clock is written by every committer; if it shares a cache line with other words, those words pay the same traffic (false sharing).

## Exercises

1. Prove that under GV1, a transaction whose commit finds $wv = rv + 1$ and skips L10 is serializable, using only the lemma and the fact that each commit does exactly one FAA.
2. Give a schedule of three transactions under GV4 in which two commits share one $wv$, and check that the reader of the third transaction still sees a consistent state.
3. Under GV5, find the largest number of aborts a single read-only transaction can suffer from one writer that commits once, with and without L4.

## References
