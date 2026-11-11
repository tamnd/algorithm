---
tag: 44E0B1
kind: theorem
slug: mutual-exclusion-lower-bounds
name: Mutual exclusion lower bounds
aliases:
- Burns-Lynch lower bound
- covering argument for mutual exclusion
area: concurrency/mutual-exclusion
level: advanced
summary: A deadlock free mutual exclusion algorithm for n processes from read/write registers needs n registers. Other bounds limit its RMR cost and its steps under contention.
prereqs: [mutual-exclusion-problem, burns-lamport-algorithm]
see_also: [lamport-fast-mutex, fischer-algorithm, peterson-algorithm, rmr-complexity, test-and-set, mcs-lock, deadlock-freedom, adversary-argument]
sources:
  - paper: doi:10.1006/inco.1993.1065
    title: James E. Burns and Nancy A. Lynch, Bounds on shared memory for mutual exclusion, Information and Computation 107(2), 1993, pages 171-184
    locator: the lower bound of n shared read/write variables for deadlock free mutual exclusion of n processes, and its covering proof
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 4 (mutual exclusion in shared memory), the section on the lower bound on the number of read/write registers
  - paper: doi:10.1145/1374376.1374410
    title: Hagit Attiya, Danny Hendler and Philipp Woelfel, Tight RMR lower bounds for mutual exclusion and other problems, Proceedings of the 40th ACM Symposium on Theory of Computing (STOC), 2008, pages 217-226
    locator: Section 5.1, the bound of Ω(n log n) RMRs for deadlock free mutual exclusion from reads, writes and conditional operations
  - paper: doi:10.1145/383962.383996
    title: James H. Anderson and Yong-Jik Kim, An improved lower bound for the time complexity of mutual exclusion, Proceedings of the 20th ACM Symposium on Principles of Distributed Computing (PODC), 2001, pages 90-99
    locator: the main theorem, a bound of Ω(log n / log log n) RMRs per passage
  - paper: doi:10.1109/REAL.1992.242680
    title: Rajeev Alur and Gadi Taubenfeld, Results about fast mutual exclusion, Proceedings of the 13th IEEE Real-Time Systems Symposium, 1992, pages 12-21
    locator: the result that with atomic reads and writes no algorithm bounds the number of steps of the process that enters under contention
---

The Burns-Lynch lower bound says that a deadlock free solution of the [mutual exclusion problem](/mutual-exclusion-problem/) for $n$ processes that uses only atomic read/write registers needs at least $n$ distinct registers, whatever the size of each register. The bound is tight: the [Burns-Lamport algorithm](/burns-lamport-algorithm/) uses exactly $n$ registers of one bit each. The proof is a *covering argument*: a process that is about to write a register can later overwrite, and so hide, everything that other processes wrote there. This page proves the bound for $n = 2$ in full, gives a marked sketch for general $n$, and states three related bounds without proof: the RMR bounds of Anderson and Kim (2001) and of Attiya, Hendler and Woelfel (2008), and the result of Alur and Taubenfeld (1992) on fast paths under contention.

## Statement

**Model.** There are $n \ge 2$ processes. Each one is deterministic and repeats a remainder section, an entry section, a critical section and an exit section. The processes communicate only through shared registers. Each register is atomic, any process can read or write it, and it can hold any number of values. A step is one read or one write of one register by one process, plus a change of the local state of that process. The system is asynchronous: any interleaving of the steps is a possible run. A process in its remainder section can stay there forever. A run is *fair* if each process that is not in its remainder section takes infinitely many steps, and each process leaves its critical section after a finite time.

The algorithm must give:

- **mutual exclusion:** in each run, at most one process is in the critical section at a time;
- **deadlock freedom:** in each fair run, if some process is in its entry section, then later some process enters the critical section.

**Theorem (Burns and Lynch).** *Every algorithm in this model with mutual exclusion and deadlock freedom uses at least $n$ distinct shared registers.*

**Related bounds, cited and not proved here.**

- **RMR cost (Attiya, Hendler and Woelfel 2008).** Each deterministic deadlock free mutual exclusion algorithm for $n$ processes from reads, writes and conditional operations such as compare-and-swap has a run in which the processes together make $\Omega(n \log n)$ remote memory references, in both the CC and the DSM model of [RMR complexity](/rmr-complexity/). This is usually stated as $\Omega(\log n)$ RMRs per passage, which matches the $O(\log n)$ upper bound of Yang and Anderson (1995).
- **An earlier RMR bound (Anderson and Kim 2001).** For the same kind of primitives, a passage can cost $\Omega(\log n / \log \log n)$ RMRs.
- **Fast paths under contention (Alur and Taubenfeld 1992).** With atomic reads and writes only, no mutual exclusion algorithm for two or more processes has a bound on the number of steps that the entering process makes when there is contention. A constant cost under contention needs a read-modify-write instruction such as [test-and-set](/test-and-set/), or a timing assumption as in [Fischer's algorithm](/fischer-algorithm/).

## In plain words

A register is like a whiteboard that holds one message. A process that is about to write a whiteboard can wipe out, in one step, everything that was written there before. Suppose a process $p$ stops just before such a write. Another process $q$ now runs alone and enters the critical section. If all the writes of $q$ went to whiteboards that $p$ and its friends are about to overwrite, then $p$ makes its write, and all traces of $q$ are gone. Then $p$ cannot know that $q$ is inside, so it goes in too.

So each new process must leave a trace on a register that nobody is about to overwrite. With $n$ processes, the proof keeps adding one more such register, until there are $n$ of them.

## Proof

**Covering.** In a configuration $C$, a process $p$ *covers* a register $R$ if $p$ is in its entry section and its next step is a write to $R$. For a set $P$ of processes that each cover a register, a *block write* by $P$ is a sequence of steps in which each process of $P$ makes its pending write, once. Two configurations are *indistinguishable* to a process if the process has the same local state in both and every register has the same value in both. A deterministic process that runs alone from two configurations that are indistinguishable to it makes the same steps from both.

### Lemma 1 (the covering lemma)

*Let $C$ be a reachable configuration, let $P$ be a nonempty set of processes that each cover a register in $C$, and let $W$ be the set of the covered registers. Let $z \notin P$ be in its remainder section in $C$. If $z$ runs alone from $C$, enters the critical section by the steps $\sigma$, and writes only registers in $W$, then the algorithm does not have both mutual exclusion and deadlock freedom.*

*Proof.* Let $\beta$ be a block write by $P$, and compare $C\beta$ with $C\sigma\beta$. The steps of $\sigma$ are steps of $z$ only, so each other process has the same state in $C$ and in $C\sigma$, and it makes the same write in $\beta$. So each process other than $z$ has the same state in $C\beta$ and in $C\sigma\beta$. A register in $W$ holds the value of its last write in $\beta$ in both. A register outside $W$ is not written by $\sigma$ or by $\beta$, so it holds its value of $C$ in both. So the two configurations differ only in the state of $z$, which is in the remainder section in $C\beta$ and in the critical section in $C\sigma\beta$. If some process $y \ne z$ is in the critical section in $C\beta$, it is there in $C\sigma\beta$ too, together with $z$. If not, the processes of $P$ are still in their entry sections in $C\beta$. Take a fair run from $C\beta$ in which $z$ stays in its remainder section. By deadlock freedom, some process $y \ne z$ enters the critical section after a finite part $\rho$ of it. No step of $\rho$ is a step of $z$, and no process other than $z$ can tell $C\beta$ from $C\sigma\beta$, so $\rho$ can also run from $C\sigma\beta$, with the same steps. In $C\sigma\beta\rho$, both $y$ and $z$ are in the critical section. $\square$

### Theorem for $n = 2$

*A deadlock free mutual exclusion algorithm for two processes $p$ and $q$ from read/write registers uses at least two registers. More exactly, in the configuration $C$ below, $q$ alone writes a register that $p$ does not cover.*

*Proof.* Let $C_0$ be the initial configuration, with $p$ at the start of its entry section and $q$ in its remainder section. Let $p$ run alone from $C_0$. This run is fair, since $q$ stays in its remainder section, so by deadlock freedom $p$ enters the critical section after a finite part $\alpha$ of it.

*Case 1: $p$ makes no write in $\alpha$.* Then $C_0\alpha$ has the same register values as $C_0$, and $q$ has the same state, so $C_0\alpha$ and $C_0$ are indistinguishable to $q$. Run $q$ alone from $C_0$; by deadlock freedom it enters the critical section by some steps $\sigma$. The same steps run from $C_0\alpha$, and then $p$ and $q$ are both in the critical section. This is against mutual exclusion.

*Case 2: $p$ writes in $\alpha$.* Let $\alpha'$ be the part of $\alpha$ before the first write of $p$, and let $C = C_0\alpha'$. In $C$, $p$ covers some register $R$, every register has its initial value, and $q$ is in its remainder section. So $C$ and $C_0$ are indistinguishable to $q$, and $q$ alone from $C$ makes the same steps $\sigma$ as alone from $C_0$, and enters the critical section. By Lemma 1 with $P = \{p\}$ and $W = \{R\}$, $\sigma$ writes some register other than $R$. So the algorithm has at least two registers. $\square$

### The covering run on an example

Take one register $x$, which is 0 at the start, and the algorithm "await $x = 0$; $x \leftarrow i$; if $x = i$ then enter, else start again". This is [Fischer's algorithm](/fischer-algorithm/) without its delay. The proof for $n = 2$ builds this run:

| step | process | action | $x$ | note |
|---|---|---|---|---|
| 1 | $p = 1$ | reads $x = 0$ | 0 | now $p$ covers $x$: configuration $C$ |
| 2 | $q = 2$ | reads $x = 0$ | 0 | $q$ runs alone from $C$ |
| 3 | $q$ | $x \leftarrow 2$ | 2 | |
| 4 | $q$ | reads $x = 2$ and enters | 2 | all writes of $q$ went to $x$ |
| 5 | $p$ | $x \leftarrow 1$ | 1 | the block write hides the write of $q$ |
| 6 | $p$ | reads $x = 1$ and enters | 1 | $p$ goes on as if it were alone |

The test file builds this run with the function `covering_run` and replays it. It also builds the run for two other algorithms with one register, which both fail in the same way. For 600 random algorithms with one register and two processes, it checks that each one either has a process that cannot enter alone, so it is not deadlock free, or fails mutual exclusion on the covering run; an independent search of all interleavings confirms each failure. For the two register Burns-Lamport algorithm, the run stops because $q$ writes its own flag $b_2$ while $p$ covers $b_1$, and for Peterson's algorithm $q$ writes its flag and the turn register while $p$ covers its own flag.

### General $n$ (sketch)

*This part is a sketch.* Burns and Lynch (1993) give the full proof, and Attiya and Welch give a textbook proof in their Chapter 4. Call a configuration $D$ *quiet* for a set $Z$ of processes if each process in $Z$ is in its remainder section and $D$ is indistinguishable to each process in $Z$ from some configuration in which all processes are in their remainder sections. A process $z$ of $Z$ that runs alone from such a $D$ makes the steps it would make from that idle configuration, so by deadlock freedom it enters the critical section.

The claim is: for each $k$ from 1 to $n$, from each reachable configuration in which all processes are in their remainder sections, steps of $p_1, \ldots, p_k$ only lead to a configuration $D$ in which $p_1, \ldots, p_k$ cover $k$ distinct registers and $D$ is quiet for $p_{k+1}, \ldots, p_n$. The case $k = n$ gives $n$ distinct registers.

- **$k = 1$.** As in Case 1 above, $p_1$ alone must write before it enters. Stop it just before its first write. No register has changed, so the configuration is quiet for the others.
- **From $k$ to $k + 1$.** Use the claim for $k$ to get $D^1$. Then do the block write, let $p_1, \ldots, p_k$ finish their passages until all are in the remainder section again, which deadlock freedom allows, and use the claim again to get $D^2$, and so on. If the number of registers is finite, two of these configurations, $D^a$ and $D^b$ with $a < b$, cover the same set $W$ of $k$ registers. In $D^a$, $z = p_{k+1}$ runs alone and enters, so by Lemma 1 it writes a register outside $W$. Stop $z$ just before its first write outside $W$. Then run the steps that led from $D^a$ to $D^b$. They start with the block write over $W$, which hides all earlier writes of $z$, so $p_1, \ldots, p_k$ make the same steps and again cover $W$. Now $z$ covers a register outside $W$, and the memory is the same as in $D^b$, so the new configuration is quiet for $p_{k+2}, \ldots, p_n$.

The sketch leaves out the details of the model, for example that each exit section ends after a finite number of steps of its process, which is needed to bring $p_1, \ldots, p_k$ back to their remainder sections. $\blacksquare$

## Consequences

- **Optimal register count.** The [Burns-Lamport algorithm](/burns-lamport-algorithm/) uses $n$ boolean registers, so it is optimal in the number of registers. The [bakery algorithm](/lamport-bakery-algorithm/) and [Peterson's algorithm](/peterson-algorithm/) for two processes use more.
- **Fast paths.** [Lamport's fast algorithm](/lamport-fast-mutex/) makes a constant number of steps without contention, but it still needs $n + 2$ registers, as the bound says it must. By Alur and Taubenfeld, it cannot also be fast under contention.
- **Why hardware has atomic instructions.** With one [test-and-set](/test-and-set/) register, a lock needs one shared location, not $n$. The bound is for reads and writes only, so it says nothing against read-modify-write locks such as the [MCS lock](/mcs-lock/).
- **Timing.** [Fischer's algorithm](/fischer-algorithm/) uses one register. The bound does not apply, since that algorithm is not asynchronous: it is only correct if each step is fast enough.
- **Local spinning.** The RMR bounds show that no deterministic lock from reads, writes and conditional operations such as compare-and-swap can have a constant RMR cost per passage for all $n$, so tree locks with $O(\log n)$ RMRs per passage are optimal for these primitives. Locks such as the MCS lock reach $O(1)$ RMRs per passage because they use fetch-and-store, which is not a conditional operation, so the bound does not apply to them.

## Tightness

The register bound is exact. The Burns-Lamport algorithm uses one boolean register per process and has mutual exclusion and deadlock freedom, so $n$ registers are enough, even when each register has only two values. The test file checks this for $n = 2$ on all interleavings of one entry of each process, and the page of the algorithm checks it for 2 and 3 processes on all runs.

The bound counts registers, not values. A single register with many values does not help, because the covering argument does not depend on what a register holds.

The bound needs both of its hypotheses. Without deadlock freedom, strict alternation on one register is a correct but useless solution: in the test file, the covering run stops because the second process cannot enter alone. Without the restriction to reads and writes, one test-and-set register is enough.

For the RMR bounds, the algorithm of Yang and Anderson (1995) has $O(\log n)$ RMRs per passage from reads and writes, so the bound of Attiya, Hendler and Woelfel is tight.

## History

Burns and Lynch first gave the bound of $n$ registers in 1980, in a paper at the Allerton Conference, and the journal version appeared in Information and Computation in 1993. Their covering argument became a standard tool for space lower bounds in shared memory. Alur and Taubenfeld (1992) showed that with reads and writes the cost of the entering process under contention cannot be bounded. For RMRs, Anderson and Kim (2001) proved $\Omega(\log n / \log \log n)$, which improved an earlier bound of Cypher, and Attiya, Hendler and Woelfel (2008) closed the gap with $\Omega(n \log n)$ for a run of $n$ processes, which proved a conjecture of Anderson and Kim.

## References
