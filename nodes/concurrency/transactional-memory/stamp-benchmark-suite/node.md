---
tag: A9KZDJ
kind: concept
slug: stamp-benchmark-suite
name: STAMP benchmark suite
aliases:
- STAMP
- Stanford Transactional Applications for Multi-Processing
area: concurrency/transactional-memory
level: research
summary: Eight C applications from Stanford (2008), with 30 configurations, that use transactions in different ways. For years the standard workload to compare TM systems.
prereqs: [software-transactional-memory, hardware-transactional-memory]
see_also: [tl2, hybrid-transactional-memory, best-effort-htm, transactional-lock-elision, intel-tsx, contention-management, opacity, k-means]
sources:
  - paper: doi:10.1109/IISWC.2008.4636089
    title: "Chi Cao Minh, JaeWoong Chung, Christos Kozyrakis and Kunle Olukotun, STAMP: Stanford transactional applications for multi-processing, IISWC 2008, pp. 35 to 46"
    locator: Section III with the eight applications, Table III with their transactional characteristics, Table IV with the recommended inputs, and Section V with results on six TM systems
  - url: https://transact2014.cse.lehigh.edu/ruan.pdf
    title: "Wenjia Ruan, Yujie Liu and Michael Spear, STAMP need not be considered harmful, TRANSACT 2014"
    locator: the known problems of the suite (nondeterminism in bayes, the crash of yada with lazy STM, the use of restart, the 32-bit and 64-bit types) and a version for the draft C++ TM specification
  - paper: doi:10.1145/2503210.2503232
    title: "Richard M. Yoo, Christopher J. Hughes, Konrad Lai and Ravi Rajwar, Performance evaluation of Intel transactional synchronization extensions for high-performance computing, SC 2013"
    locator: STAMP run on the RTM of Intel Haswell with lock elision, and the effect of capacity and conflict aborts per application
---

**STAMP** (Stanford Transactional Applications for Multi-Processing) is a set of eight multithreaded C programs that use [transactions](/transaction/) for their synchronization: bayes, genome, intruder, kmeans, labyrinth, ssca2, vacation and yada. Chi Cao Minh, JaeWoong Chung, Christos Kozyrakis and Kunle Olukotun published it at IISWC 2008. The programs come from different fields, and their transactions differ in length, in the size of their read and write sets, and in how often they conflict, so one suite tests a [transactional memory](/software-transactional-memory/) system in many ways. With 30 recommended configurations and inputs, and versions that run on software, [hardware](/hardware-transactional-memory/) and [hybrid](/hybrid-transactional-memory/) TM, STAMP became the standard workload of TM research for about ten years. It also has known faults, and a result on STAMP says only as much as the program and the TM system that produced it.

## In plain words

A new idea for transactional memory must be tested on real programs, not only on a shared counter or a small tree. Before STAMP, every research group used its own small tests, so the numbers of two groups could not be compared.

STAMP gave everyone the same eight programs. Some do short transactions that seldom collide. Some do long transactions that touch much data and collide often. Some spend almost all their time in transactions, and some spend little.

So a TM system that is good only for short, quiet transactions shows this on STAMP. A hardware TM that cannot hold large transactions shows this too.

The programs are old research code, and some of them behave in ways that are not typical for programs of today. A careful reader checks which version of STAMP a paper used, and how.

## The idea

**What the suite holds.** Each application is a C program with threads. The parts that need synchronization are marked as transactions with macros such as `TM_BEGIN` and `TM_END`, and in the original release each shared load and store inside a transaction is also marked by hand (`TM_SHARED_READ`, `TM_SHARED_WRITE`), so that a software TM can put a barrier on it and a hardware TM can ignore the marks. The suite has 30 variants: kmeans and vacation have six each (`-low` and `-high` for the level of contention, each with a plain, a `+` and a `++` input size), and the other six applications have three each. The variants without `++` are small enough for a simulator; the `++` inputs are for real machines.

**The eight applications.** The descriptions follow Section III of the paper.

- **bayes** learns the structure of a [Bayesian network](/bayesian-network/) from data by [hill climbing](/hill-climbing/), with an adtree to estimate probabilities. A transaction computes and adds one new dependency, so the transactions are long and read much of the graph.
- **genome** puts a gene back together from many short overlapping segments (see [genome assembly](/genome-assembly-problem/)). A [hash](/hash-table/) set first removes duplicate segments, and then threads match segments by their overlaps. Transactions are of medium size and seldom conflict.
- **intruder** is a network intrusion detector, after design 5 of Haagdorens and colleagues. Packets go through capture (a FIFO queue), reassembly (a dictionary kept as a tree) and detection. The first two phases are transactions; they are short but conflict often.
- **kmeans** clusters points with [k-means](/k-means/), using code from MineBench. A transaction updates one cluster center, so it is short and small. The number of clusters $K$ sets the contention: with more clusters, two threads are less likely to update the same one.
- **labyrinth** routes paths in a three-dimensional grid with a variant of Lee's maze-routing algorithm. One transaction copies the grid, finds a path in the private copy, and then writes the path into the shared grid after it reads every cell of the path again. The copy is done with early release where the TM system has it, but the transactions are still very long, with very large read and write sets.
- **ssca2** is kernel 1 of the SSCA2 graph benchmark: it builds a large directed graph in adjacency arrays. Threads add nodes in parallel, and transactions guard the adjacency arrays; they are tiny and seldom conflict, because there are many nodes.
- **vacation** is a travel booking system, in the style of the SPECjbb2000 benchmark, with its tables kept as trees. Each client session (a booking, a cancellation or an update) is one coarse transaction of medium length.
- **yada** refines a [Delaunay mesh](/delaunay-refinement/) with Ruppert's algorithm. A transaction takes a skinny triangle from a work queue and rebuilds the mesh around it, so transactions are long and large.

**Table III of the paper** puts the eight on a few rough scales:

| application | transaction length | read and write set | time in transactions | contention |
|---|---|---|---|---|
| bayes | long | large | high | high |
| genome | medium | medium | high | low |
| intruder | short | medium | medium | high |
| kmeans | short | small | low | low |
| labyrinth | long | large | high | high |
| ssca2 | short | small | low | low |
| vacation | medium | medium | high | low or medium |
| yada | long | large | high | medium |

**Six TM systems in the paper.** The authors ran the suite on a simulated lazy HTM (in the style of TCC), an eager HTM (in the style of LogTM), a lazy STM (an x86 port of [TL2](/tl2/)), an eager STM (TL2 with an undo log), and a lazy and an eager hybrid in the style of SigTM. They set out to test two common views, that HTMs are the fastest and that eager systems beat lazy ones, and they found cases against both. On yada, the large transactions made the HTMs overflow their transactional buffers; the largest sets were in labyrinth+, with 783 lines read and 779 written. On vacation, the cost of undo logs made the eager HTM and hybrid much slower than the lazy ones. The general lesson was that the eight applications stress different parts of a TM design, so no single application stands for the suite.

**Known problems.** Ruan, Liu and Spear (TRANSACT 2014, "STAMP need not be considered harmful") list problems that had been found in the five years since the last release, and they made a repaired version. The main points, in their words or close to them:

- bayes is not deterministic: the order of the first commits can change the run time of the whole program very much. So one run of bayes is not a good measurement.
- yada crashes with lazy software TMs. The cause they give is a write inside a transaction that is instrumented, followed by a read of the same location that is not, so the read misses the buffered value.
- labyrinth behaves differently on hardware and software TM. Its transaction copies the grid with a plain `memcpy` that is not instrumented and then calls `TM_RESTART` to retry on its own; with an HTM the copy is part of the hardware transaction, with an STM it is not.
- The manual macros encode the sizes of types, and some of them are wrong when the code is built for 64 bits instead of 32.
- In vacation, the calls to `TM_RESTART` are on paths that an [opaque](/opacity/) TM can never reach; they exist only for TMs that let a transaction see inconsistent state.
- Some transactions call library functions, such as `qsort` in bayes, that a compiler-based TM must treat as unsafe or as pure.
- On a hardware TM (through the GCC TM support), vacation, intruder and genome lost much of their speed with more threads. As far as the authors could tell, transactions kept aborting each other until the runtime fell back to serial mode.

Their conclusion is in the title: with repairs, STAMP is still useful. Other groups have made their own changes, so the name "STAMP" in a paper can mean different code.

**Why STAMP is hard for a best-effort HTM.** A [best-effort HTM](/best-effort-htm/) such as [Intel TSX](/intel-tsx/) gives up on a transaction that does not fit in the cache. So Table III also predicts how STAMP runs on such hardware: applications with short, small transactions can gain, and those with long, large transactions (labyrinth, yada, bayes) are likely to abort for capacity and run under the fallback lock. Yoo and colleagues (SC 2013) measured STAMP with [lock elision](/transactional-lock-elision/) on the RTM of Haswell and report the gains and the abort causes per application.

## Examples

**A small workload model. This is not STAMP.** The code of this page, `impl/python/workload_model.py`, has three toy workloads that copy only the shape of the transactions of three STAMP applications. There are no real data structures and no real inputs. Each thread is a generator that runs on `htmsim.py`, the small best-effort HTM model of the [best-effort HTM](/best-effort-htm/) page (bounded read and write sets, conflicts found by coherence requests, the requester wins), and every transaction runs with [lock elision](/transactional-lock-elision/): up to three hardware tries that read the lock, then the lock.

- `kmeans_like`: each thread adds its points to cluster $x \bmod K$, one transaction of two reads and two writes per point.
- `vacation_like`: a session books one to three items, all or none, and adds the count to a record of the thread.
- `labyrinth_like`: a transaction reads every cell of a path and writes all of them if all are free.

In 100 random schedules of 4 threads with 6 points each (2400 transactions), the model gives these counts. The scheduler switches threads at every step, which is far more often than real threads switch, so the numbers show the direction of the effect, not its real size.

| workload | committed in hardware | ran under the lock | conflict aborts | capacity aborts |
|---|---|---|---|---|
| kmeans, $K = 1$ | 817 | 1583 | 5555 | 0 |
| kmeans, $K = 2$ | 1558 | 842 | 3636 | 0 |
| kmeans, $K = 8$ | 2314 | 86 | 797 | 0 |

With one cluster, every pair of transactions conflicts, and most of them use up their tries and take the lock. With eight clusters the hardware does almost all the work. This is the effect of $K$ that the paper describes for kmeans.

For labyrinth, the write buffer of the model holds 4 lines. In 100 schedules of 4 threads that each claim 2 paths (800 claims), paths of 2 cells committed in hardware 797 times and took the lock 3 times. Paths of 6 cells can never be written in hardware: 169 claims won, and every one of them ran under the lock; only the claims that found a taken cell, and so wrote nothing, committed in hardware. This is the capacity problem of long STAMP transactions in a few lines.

The tests in `test_workload_model.py` check, over 552 seeded random schedules, that the result is always right (the cluster sums are exact, no item is sold more times than it has places, no grid cell belongs to two paths), that the contention falls as $K$ grows, that bookings and paths that do not fit the write buffer finish only under the lock, and that a seed gives the same run each time.

## Where it is used

- **Evaluation of TM systems.** From 2008 on, most papers on software, hardware and hybrid TM report results on some or all of STAMP, often with the TL2 port of the suite as the baseline.
- **Hardware TM studies.** Simulator studies of HTM designs and measurements of commercial HTM, such as Intel TSX and IBM POWER8, use STAMP to show the effect of capacity and conflicts.
- **Compiler TM.** Versions of STAMP for the draft C++ TM specification and for GCC TM support test compilers that place the barriers themselves.
- **Contention management and scheduling.** STAMP applications with high contention, such as intruder and labyrinth, are a common test for [contention managers](/contention-management/) and transaction schedulers.

## References
