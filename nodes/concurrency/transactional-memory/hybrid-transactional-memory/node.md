---
tag: 932XZC
kind: concept
slug: hybrid-transactional-memory
name: Hybrid transactional memory
aliases:
- HyTM
- hybrid TM
area: concurrency/transactional-memory
level: research
summary: Run each transaction in hardware when it can and in a software TM when it cannot, with both kinds running at the same time. The hard part is to make each kind see the conflicts of the other cheaply.
prereqs: [best-effort-htm, norec, software-transactional-memory]
see_also: [transactional-lock-elision, intel-tsx, hardware-transactional-memory, dstm, tl2, transaction-validation, privatization-safety, opacity]
sources:
  - paper: doi:10.1145/1168857.1168900
    title: "Peter Damron, Alexandra Fedorova, Yossi Lev, Victor Luchangco, Mark Moir and Daniel Nussbaum, Hybrid transactional memory, ASPLOS 2006, pp. 336 to 346"
    locator: the HyTM design, in which hardware transactions check the ownership records of a software TM, and the claim that the system works without any HTM and uses one only to go faster
  - paper: doi:10.1145/1122971.1123003
    title: "Sanjeev Kumar, Michael Chu, Christopher J. Hughes, Partha Kundu and Anthony Nguyen, Hybrid transactional memory, PPoPP 2006, pp. 209 to 220"
    locator: proposed hardware support combined with an object-based STM, with transactions that start in hardware and move to software
  - paper: doi:10.1145/1950365.1950373
    title: "Luke Dalessandro, Francois Carouge, Sean White, Yossi Lev, Mark Moir, Michael L. Scott and Michael F. Spear, Hybrid NOrec: a case study in the effectiveness of best effort hardware transactional memory, ASPLOS 2011, pp. 39 to 52"
    locator: hardware transactions that read the NOrec sequence lock and increment a separate counter at commit, and software transactions that watch both words
  - book: "Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Synthesis Lectures on Computer Architecture, Morgan and Claypool, 2010, doi:10.1007/978-3-031-01728-5"
    locator: the section on hybrid TM in the chapter on hardware-supported transactional memory
---

A **hybrid transactional memory** runs each transaction as a hardware transaction when it can, and as a [software transaction](/software-transactional-memory/) when the hardware fails, for example because the transaction is too large or makes a system call. Unlike a single fallback lock, the software path lets many failed transactions run in parallel, and hardware transactions keep running next to them. The two kinds must still detect conflicts with each other, and the cost of that check on the hardware path decides whether the design is fast. Damron and colleagues and Kumar and colleagues proposed the first hybrid designs in 2006; Hybrid NOrec (2011) is a simple and well-studied one.

## In plain words

A [best-effort HTM](/best-effort-htm/) is fast but may fail. The simplest backup is one lock, but then every failed transaction runs alone and stops all others.

A hybrid TM uses a software TM as the backup. Failed transactions run in software, and many of them can run together. Hardware transactions run at the same time.

Now there are two kinds of transaction on the same data, and each must notice when the other changes something it uses. The hardware notices only memory accesses, and software notices only what its own bookkeeping tells it. So both sides must touch some shared words. If the hardware side touches too much, it becomes slow and it conflicts too often, and the hybrid loses its point.

## The idea

**Two paths, one memory.** A transaction first tries in hardware a few times and then switches to software. Each path is correct alone: the hardware path by the HTM, and the software path by its STM algorithm. The design must add a way for each path to see the other.

- *Software sees hardware.* A software transaction must learn that a hardware transaction wrote data that it read. A hardware commit makes all its writes visible at once, but it does not update the metadata of the STM unless the hardware code does so itself.
- *Hardware sees software.* A hardware transaction must not read data that a software transaction is in the middle of changing, and must not commit over a software transaction that will then write stale values. The HTM finds conflicts on any line that the hardware transaction has read, so the usual way is to make the hardware transaction read some word that a software writer always writes. This is the same trick as reading the lock in [lock elision](/transactional-lock-elision/).

**Ownership records (HyTM, 2006).** In the HyTM of Damron, Fedorova, Lev, Luchangco, Moir and Nussbaum, the software path is an STM with an ownership record for each location. The hardware code, made by the compiler, reads the ownership record of every location that it accesses and aborts if a software transaction owns it. A software transaction that later acquires that record writes it, which aborts the hardware transaction. This is precise but costly: every hardware access becomes two accesses, and the read set grows. The paper stresses that the system is correct and complete without any HTM, and uses the HTM only to go faster. Kumar, Chu, Hughes, Kundu and Nguyen proposed in the same year hardware support together with an object-based STM, in which a transaction starts in hardware and moves to software, and the two modes share the metadata of each object.

**A global clock (Hybrid NOrec, 2011).** [NOrec](/norec/) has no ownership records at all, only one global sequence lock SEQ, which is odd while a software writer writes back. Dalessandro and colleagues built a hybrid on it.

1. *Hardware path.* The transaction reads SEQ at the start, and aborts if it is odd. SEQ is now in its read set, so a software writer that takes SEQ aborts it. If the transaction wrote anything, it adds 1 to a second word HWC just before it commits.
2. *Software path.* The transaction is NOrec: it buffers writes, keeps the values it read, and after each read checks that SEQ did not change. In the hybrid it checks HWC too, because a hardware commit changes memory without changing SEQ. If either changed, it validates by value: it rereads every value it read and restarts only if one differs.
3. *Software commit.* The writer takes SEQ with compare-and-swap (even to odd). This aborts every hardware transaction. It then checks HWC once more, and validates if a hardware commit came in between. Then it writes back and releases SEQ.

Hardware transactions touch only two shared words, SEQ and HWC, so their overhead is small. The cost is that every writing hardware transaction writes HWC, so two hardware writers always conflict near their ends, and every software writer aborts every hardware transaction in the system. Hybrid NOrec discusses these costs and ways to reduce them.

**Phases instead of mixing.** Another way avoids the coordination: run all transactions in hardware, and when one cannot, switch the whole system into a software phase, and back later. Phased TM (Lev, Moir and Nussbaum, 2007) works in this way. It is simpler, but one long software transaction slows all others.

**Correctness.** The implementation for this page, `impl/python/hybrid_norec.py`, is a simplified Hybrid NOrec on the best-effort HTM model of `impl/python/htmsim.py`. It omits the refinements of the paper; it keeps SEQ, HWC and the checks above. Each of the checks is needed:

| removed check | what goes wrong | run found by the tests |
|---|---|---|
| the hardware path reads SEQ | a hardware audit reads the accounts in the middle of a software write back | the software transfer from $a$ to $b$ has stored $a = 9$ but not yet $b$; the hardware audit reads $a = 9, b = 10$ and commits the sum 19 |
| the software path watches HWC | a software transaction reads one account before and one after a hardware commit | the software audit reads $a = 10$; a hardware transfer commits $a = 9, b = 11$ without changing SEQ; the audit reads $b = 11$ and returns 21 |

With both checks, the tests run every schedule with up to 4 preemptions of five small two-thread cases (more than 10,000 schedules), every schedule with up to 2 preemptions of a three-thread case, and 600 random runs of four threads on hardware and software paths with small and large capacities. Every audit sees the right sum, and no update is lost.

## Examples

**One schedule, step by step.** The table shows the second row above, but with the check of HWC in place. Memory starts with $a = b = 10$ and SEQ $=$ HWC $= 0$.

| step | $P_0$, hardware transfer | $P_1$, software audit | memory |
|---|---|---|---|
| 1 | | read SEQ $= 0$, HWC $= 0$ | |
| 2 | | read $a = 10$; SEQ and HWC unchanged | |
| 3 | begin; read SEQ $= 0$; read $a$, $b$; write $a = 9$, $b = 11$ | | |
| 4 | read HWC $= 0$, write HWC $= 1$; commit | | $a = 9, b = 11$, HWC $= 1$ |
| 5 | | read $b = 11$; HWC changed | |
| 6 | | validate: $a$ is now 9, not 10; restart | |
| 7 | | read $a = 9$, $b = 11$; return 20 | |

Without the check in step 5, the audit returns 21.

**A capacity failure.** A transaction that writes more lines than the write buffer holds aborts with the capacity code on every hardware try. In a TLE system it would take the global lock and stop everyone. In a hybrid it runs as a software transaction, and other transactions, in hardware or software, continue as long as they do not conflict with it.

## Where it is used

- **Research.** Hybrid designs were studied on simulators, on Sun's Rock, and later on Intel TSX. Later work, such as Reduced Hardware NOrec (Matveev and Shavit, 2015), uses small hardware transactions inside the software path to cut the overhead further.
- **TM runtimes.** A runtime for language-level transactions can choose between hardware and software implementations. On real machines a common choice is hardware with a single lock as the fallback, as in [lock elision](/transactional-lock-elision/), because it is simpler; a hybrid pays off when many transactions fail in hardware for reasons other than conflicts.
- **Teaching.** Hybrid NOrec is a small, complete example of how two synchronization methods on the same data must each make their changes visible to the other.

## References
