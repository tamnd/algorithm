---
tag: NHXTYV
kind: concept
slug: determinacy-race
name: Determinacy race
aliases:
- determinacy race condition
area: parallel/work-span-models
level: core
summary: Two logically parallel accesses to one memory location, at least one a write, so the result can depend on the schedule. SP-bags finds them in one serial run with union-find.
prereqs: [fork-join-model, computation-dag]
see_also: [race-condition, fork-join-model, computation-dag, disjoint-set, tarjan-offline-lca, happened-before, mutex, work-span-model]
sources:
  - paper: doi:10.1145/258492.258493
    title: "Mingdong Feng and Charles E. Leiserson, Efficient detection of determinacy races in Cilk programs, SPAA 1997"
    locator: pp. 1-11, the Nondeterminator, the SP-bags rules (Figure 8), Lemma 4, Corollary 9, Theorem 1 and Theorem 10
  - paper: "Mingdong Feng and Charles E. Leiserson, Efficient detection of determinacy races in Cilk programs, Theory of Computing Systems 32(3), 1999"
    locator: pp. 301-326, the journal version of the SPAA 1997 paper
  - paper: doi:10.1145/277651.277696
    title: "Guang-Ien Cheng, Mingdong Feng, Charles E. Leiserson, Keith H. Randall and Andrew F. Stark, Detecting data races in Cilk programs that use locks, SPAA 1998"
    locator: the data race with locks, and the All-Sets and Brelly algorithms
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, third edition, MIT Press, 2009
    locator: Chapter 27, Section 27.1, the subsection on race conditions (two parallel increments of one variable)
  - paper: "Robert H. B. Netzer and Barton P. Miller, What are race conditions? Some issues and formalizations, ACM Letters on Programming Languages and Systems 1(1), 1992"
    locator: the general race (determinacy race) and the data race (atomicity race)
  - paper: doi:10.1145/277650.277725
    title: "Matteo Frigo, Charles E. Leiserson and Keith H. Randall, The implementation of the Cilk-5 multithreaded language, PLDI 1998"
    locator: the spawn and sync model of the programs that the Nondeterminator checks
---

A determinacy race is a pair of accesses to the same memory location, at least one of them a write, that are logically parallel: in the [computation DAG](/computation-dag/) of the run, neither access comes before the other. Such a pair can run in either order, so the result of the program can depend on the schedule. A fork-join run with no determinacy race gives the same result under every schedule as the serial run. Feng and Leiserson (1997) gave the SP-bags algorithm, which finds every determinacy race of a run on a given input in one serial run, with a [disjoint-set](/disjoint-set/) structure.

## In plain words

A parallel program says which pieces of work may run at the same time. Such pieces are in parallel. If one piece must finish before another starts, they are in series.

Suppose two parallel pieces use one variable, and at least one of them changes it. Then the scheduler picks the order, and two runs can give two answers. This is a determinacy race. Tests can miss it, because many runs happen to use the same order.

A lock does not cure it. A lock stops the two pieces from using the variable at the same instant, but either piece can still go first.

The SP-bags detector runs the program once, on one processor, in the normal serial order. It sorts the pieces that ran so far into groups: those in series with the current piece and those in parallel. It checks each memory access against these groups.

## The idea

The notation follows the parallel pages of this site.

| Symbol | Meaning |
|---|---|
| $n$ | the input size |
| $p$ | the number of processors |
| $W = T_1$ | the work: the serial running time |
| $S = T_\infty$ | the span: the length of a longest path in the DAG |
| $T_p$ | the time on $p$ processors |
| $W/S$ | the parallelism |
| $v$ | the number of shared memory locations that the run accesses |

**The definition.** Take a fork-join program with spawn and sync, as in the [fork-join model](/fork-join-model/), and fix its input. The run is a DAG $G$ whose nodes are instructions. Write $u \prec v$ if $G$ has a path from $u$ to $v$, and $u \parallel v$ if neither $u \prec v$ nor $v \prec u$. A *determinacy race* is a pair of accesses $u, v$ to one location $\ell$ with $u \parallel v$ and at least one of them a write. A program has a determinacy race on an input if the DAG of its run on that input has one.

The order of two reads of $\ell$ does not matter, so read and read is not a race. Two writes that are in parallel are a race, because the final value of $\ell$ depends on which one comes last.

**Why a race-free run is deterministic.** Suppose the run has no determinacy race. Then every two accesses to $\ell$ with at least one write are ordered by $\prec$, so all writes to $\ell$ form a chain, and each read of $\ell$ is ordered with every write of $\ell$. A schedule runs the nodes in an order consistent with $\prec$. So in every schedule, a read of $\ell$ sees the value of the last write of $\ell$ that precedes it in $G$, which is the same write in every schedule. By induction over the nodes in the order of $G$, every schedule computes the same values as the serial run. Feng and Leiserson call such a program *internally deterministic*. A program can also be *externally deterministic*: it has races, but the racing operations commute and associate, as two additions to one counter do, so the output is still fixed.

**Determinacy races and data races.** Netzer and Miller (1992) call the determinacy race a *general race*. A *data race* (Netzer and Miller say *atomicity race*) is a pair of parallel accesses to one location, at least one a write, that do not hold a common lock (Cheng et al., 1998). In a program without locks the two notions agree. With locks, every data race is a determinacy race, but not the converse. Two parallel critical sections on $x$, one doing $x \leftarrow x + 1$ and one doing $x \leftarrow 2x$ under the same [mutex](/mutex/), have no data race. They still have a determinacy race: from $x = 1$, the result is $4$ or $3$, depending on which runs first. A data race detector finds bugs in the use of locks. A determinacy race detector finds every place where the schedule can change the result. The general view of races in concurrent programs is on [race condition](/race-condition/).

**Series-parallel structure.** The DAG of a spawn and sync run is series-parallel (Feng and Leiserson, Theorem 3). It has a parse tree whose leaves are threads (maximal runs of instructions with no spawn or sync) and whose internal nodes are S-nodes (run the left part, then the right part) and P-nodes (run the two parts in parallel). Two threads are in parallel exactly when their lowest common ancestor in the parse tree is a P-node (Lemma 4). SP-bags finds this ancestor on the fly, in the way of [Tarjan's offline LCA algorithm](/tarjan-offline-lca/).

**The SP-bags algorithm.** Run the program serially, depth first, as a C program would run. Each procedure instance $F$ has an ID and two bags of procedure IDs, kept in a disjoint-set forest with union by rank and path compression. Each set is tagged S or P.

- The S-bag $S_F$ holds $F$ and the descendants of the completed children of $F$ that precede the current thread.
- The P-bag $P_F$ holds the descendants of the completed children of $F$ that are in parallel with the current thread.

The bags change at these events (Figure 8 of the paper):

| Event | Action |
|---|---|
| $F$ is spawned | $S_F \leftarrow \mathrm{MakeSet}(F)$, $P_F \leftarrow \emptyset$ |
| child $F'$ returns to $F$ | $P_F \leftarrow \mathrm{Union}(P_F, S_{F'})$ |
| $F$ runs a sync | $S_F \leftarrow \mathrm{Union}(S_F, P_F)$, $P_F \leftarrow \emptyset$ |

For each location $\ell$, a shadow memory keeps one procedure $\mathrm{reader}(\ell)$ and one procedure $\mathrm{writer}(\ell)$. When procedure $F$ accesses $\ell$:

- **Write.** If $\mathrm{Find}(\mathrm{reader}(\ell))$ or $\mathrm{Find}(\mathrm{writer}(\ell))$ is a P-bag, report a race on $\ell$. Then set $\mathrm{writer}(\ell) \leftarrow F$.
- **Read.** If $\mathrm{Find}(\mathrm{writer}(\ell))$ is a P-bag, report a race on $\ell$. If $\mathrm{Find}(\mathrm{reader}(\ell))$ is an S-bag, set $\mathrm{reader}(\ell) \leftarrow F$.

The key fact is that the bags give the relation $\prec$ exactly. When a thread $e_2$ runs, a thread $e_1$ of procedure $F_1$ that ran earlier satisfies $e_1 \prec e_2$ if $F_1$ is in an S-bag, and $e_1 \parallel e_2$ if $F_1$ is in a P-bag (Corollary 9).

**Why one reader and one writer suffice.** Let $a$ run before $e$ in the serial order with $a \prec e$, and let $w$ run after $e$ with $w \parallel a$. Then $w \parallel e$. *Proof.* The lowest common ancestor $x$ of $a$ and $w$ in the parse tree is a P-node, with $a$ on its left side and $w$ on its right side. The serial order visits $e$ between $a$ and $w$. If $e$ were under the right side of $x$, then the ancestor of $a$ and $e$ would be $x$, and $a \parallel e$, which is false. So $e$ is under the left side of $x$, and the ancestor of $e$ and $w$ is the P-node $x$, so $e \parallel w$. $\blacksquare$ So when the stored access precedes the new one, the new one can replace it: any later access that races with the old one also races with the new one. Feng and Leiserson use this to prove the main result.

**Theorem 10 (Feng and Leiserson).** "The SP-bags algorithm detects a determinacy race in a Cilk program if and only if a determinacy race exists." More exactly, the proof shows that SP-bags reports a race on $\ell$ whenever the run has a determinacy race on $\ell$. It need not report every racing pair.

**Theorem 1 (Feng and Leiserson).** On a run with serial time $W$ that accesses $v$ shared locations, SP-bags takes $O(W\,\alpha(v, v))$ time and $O(v)$ space, where $\alpha$ is the inverse of Ackermann's function. The run does at most $W$ disjoint-set operations. If it spawns $n$ procedures, Tarjan's bound for the disjoint-set forest gives $O(W\,\alpha(W, n))$ time and $O(v + n)$ space. A garbage collection every $v$ steps, which removes the IDs that the shadow memory no longer uses, keeps the forest at $O(v)$ nodes and gives the bound of the theorem. Feng and Leiserson note that the Nondeterminator does not do this garbage collection.

## Examples

**Two parallel increments.** This is the example of CLRS (third edition, Section 27.1). The main procedure $F_0$ spawns $F_1$ and $F_2$, and each runs $x \leftarrow x + 1$, a read of $x$ followed by a write of $x$, then $F_0$ syncs. If the two reads both run before the two writes, $x$ grows by 1 and not by 2. SP-bags runs as follows.

1. $F_1$ is spawned: $S_1 = \{F_1\}$. It reads $x$, so $\mathrm{reader}(x) = F_1$. It writes $x$: $F_1$ is in an S-bag, so there is no race, and $\mathrm{writer}(x) = F_1$.
2. $F_1$ returns: $P_0 = \{F_1\}$.
3. $F_2$ is spawned: $S_2 = \{F_2\}$. It reads $x$: $\mathrm{Find}(\mathrm{writer}(x)) = \mathrm{Find}(F_1)$ is the P-bag $P_0$, so SP-bags reports a race on $x$.

**A sync removes the race.** If $F_0$ runs a sync between the two spawns, then at the sync $S_0 \leftarrow \mathrm{Union}(S_0, P_0)$ moves $F_1$ into an S-bag. When $F_2$ reads $x$, $\mathrm{Find}(F_1)$ is an S-bag, and no race is reported. This matches the DAG: the sync node is on every path from $F_1$ to $F_2$.

**Locks.** In the mutex example above, both critical sections run in parallel children of $F_0$. The brute-force check with locks finds no data race, and SP-bags, which ignores locks, reports the determinacy race on $x$. Section 5 of Feng and Leiserson extends SP-bags to programs with locks and to the atomic updates of Cilk inlets. The Nondeterminator-2 of Cheng et al. (1998) detects data races with locks, by the All-Sets and Brelly algorithms.

**The tests.** The file `determinacy_race.py` has SP-bags and a brute-force check. A program is a nested list of reads, writes, spawns and syncs, and each procedure ends with an implicit sync. The brute force builds the DAG with one node per access and edges for spawn, continuation and sync, computes reachability with bit masks, and checks every pair of accesses. The tests check:

- the examples above, the read-only case, and nested spawns where the child's implicit sync orders a grandchild;
- that SP-bags and the brute force give the same set of racy locations on 3000 random programs with up to four levels of spawn;
- that the bags give the relation $\parallel$ exactly: for every pair of accesses on 1500 random programs, the earlier procedure is in a P-bag when the later access runs if and only if the DAG has no path between them;
- that two parallel locked updates have no data race but do have a determinacy race.

## Where it is used

- **The Nondeterminator.** Feng and Leiserson built SP-bags into the Nondeterminator, a debugging tool for Cilk. It runs the program serially on one input, so it is a test tool and not a proof of correctness for all inputs. If the run on that input has a determinacy race, it reports one, and if it reports none, every schedule of that run gives the same result. In their tests the slowdown was less than a factor of 12 over the serial run.
- **Race detectors for locks.** The Nondeterminator-2 adds lock sets to the shadow memory, to detect data races instead of determinacy races (Cheng et al., 1998).
- **Parallel race detection.** SP-bags must run serially, because it depends on the depth-first order. Later work by Bender, Fineman, Gilbert and Leiserson (2004) keeps the series-parallel relation with order-maintenance structures, so that the check can run in parallel with the program.
- **Teaching and program design.** CLRS (Section 27.1) uses the determinacy race to explain why the strands of a parallel loop must be independent. A parallel program that is free of determinacy races can be tested and debugged as a serial program, which is one reason for the spawn and sync style of the [fork-join model](/fork-join-model/) and the [work-span model](/work-span-model/). The [happened-before](/happened-before/) relation of message-passing systems plays the role of $\prec$ in race detectors for threads and messages.

## References
