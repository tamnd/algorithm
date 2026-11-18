---
tag: E9MBSZ
kind: problem
slug: robustness-against-weak-isolation
name: Robustness against weak isolation
aliases:
- robustness checking for isolation levels
- isolation robustness
area: databases/transactions-and-concurrency
level: research
summary: "Decide whether every execution of a given set of transactions or programs that a weak isolation level allows is serializable, so the weak level is safe for that workload."
prereqs: [isolation-levels, conflict-serializability, snapshot-isolation]
see_also: [snapshot-isolation-dangerous-structure, transaction-chopping, write-skew, transaction-anomalies, adya-isolation-levels, serializable-snapshot-isolation, co-np-complete, logspace]
sources:
  - paper: doi:10.1145/3561049
    title: "Bas Ketsman, Christoph Koch, Frank Neven and Brecht Vandevoort, Deciding robustness for lower SQL isolation levels, ACM Transactions on Database Systems 47(4), 2022, article 13; first in PODS 2020, pages 315 to 330"
    locator: "the definitions of robustness for concrete transactions, the coNP-completeness for read committed, the result for read uncommitted, and the relation to transaction chopping; chapter level only"
  - paper: "Brecht Vandevoort, Bas Ketsman, Christoph Koch and Frank Neven, Robustness against read committed for transaction templates, Proceedings of the VLDB Endowment 14(11), 2021, pages 2141 to 2153"
    locator: "the polynomial-time decision procedure for transaction templates under read committed, chapter level only"
  - paper: doi:10.4230/LIPIcs.ICDT.2022.16
    title: "Brecht Vandevoort, Bas Ketsman, Christoph Koch and Frank Neven, Robustness against read committed for transaction templates with functional constraints, ICDT 2022"
    locator: "the extension of the template analysis with functional constraints such as foreign keys, chapter level only"
  - paper: doi:10.1145/1071610.1071615
    title: "Alan Fekete, Dimitrios Liarokapis, Elizabeth O'Neil, Patrick O'Neil and Dennis Shasha, Making snapshot isolation serializable, ACM Transactions on Database Systems 30(2), 2005"
    locator: "the static dependency graph, the sufficient condition for serializability under snapshot isolation, and the analysis of TPC-C; chapter level only"
  - paper: doi:10.1145/1065167.1065193
    title: "Alan Fekete, Allocating isolation levels to transactions, Proceedings of ACM PODS 2005, pages 206 to 215"
    locator: "the choice of snapshot isolation or two-phase locking per program so that every execution is serializable, chapter level only"
  - paper: "Sidi Mohamed Beillahi, Ahmed Bouajjani and Constantin Enea, Checking robustness against snapshot isolation, Proceedings of CAV 2019"
    locator: "the reduction of robustness against snapshot isolation to reachability under serializability, and its complexity for finite-state programs, chapter level only"
  - paper: doi:10.1007/978-3-662-48653-5_26
    title: "Andrea Cerone, Alexey Gotsman and Hongseok Yang, Transaction chopping for parallel snapshot isolation, DISC 2015, LNCS 9363, pages 388 to 404"
    locator: "criteria for chopping and for robustness under snapshot isolation and parallel snapshot isolation by cycles in dependency graphs, chapter level only"
---

*Robustness* asks whether a weak [isolation level](/isolation-levels/) is safe for a particular application. A set of transactions, or of transaction programs, is *robust against* a level $I$ if every execution of it that $I$ allows is [conflict serializable](/conflict-serializability/). A robust workload gets the speed of the weak level with the correctness of serializability, and the [transaction anomalies](/transaction-anomalies/) of the level never show up for it. For [snapshot isolation](/snapshot-isolation/) the main tool is the [dangerous structure theorem](/snapshot-isolation-dangerous-structure/): if the programs cannot form two consecutive rw-antidependencies between concurrent transactions, they are robust. For read committed, Ketsman, Koch, Neven and Vandevoort (2020) showed that the problem is coNP-complete for concrete transactions, and later work found polynomial algorithms for transaction templates. [Transaction chopping](/transaction-chopping/) is a close relative: it asks whether pieces of transactions can run as separate transactions with no isolation between the pieces and still give serializable results.

## In plain words

A database can run transactions with strong isolation, which is always correct but slower, or with a weaker level, which is faster but allows some wrong results. For many applications the wrong results cannot actually happen, because of what the transactions do. If no two transactions ever read and write the same data in the dangerous way, the weak level gives the same results as the strong one. The robustness problem is to decide this for a given application, ahead of time, by looking at its transactions. If the answer is yes, the application can run at the weak level safely. If the answer is no, the checker can show a bad interleaving and point to the transactions that need a stronger level or a change.

## Definition

**Transactions and levels.** A *transaction* is a finite sequence of reads $r(x)$ and writes $w(x)$ on objects, ending in a commit. For a finite set $\mathcal{T}$ of transactions, a level $I$ defines the set $A_I(\mathcal{T})$ of schedules of $\mathcal{T}$ that it allows, given as interleavings with the version each read returns. In one common formalization, read uncommitted allows every schedule with no dirty write; read committed also requires each read to return the last committed version at the time of the read; snapshot isolation requires each read to return the last version committed before the transaction started, and forbids concurrent writers of the same object.

**Problem.** Given $\mathcal{T}$ and $I$, decide whether every schedule in $A_I(\mathcal{T})$ is conflict serializable, with conflicts taken over the versions read, as in the dependency graph of [Adya's isolation levels](/adya-isolation-levels/). If not, a witness is an allowed schedule whose dependency graph has a cycle.

**Templates.** A *transaction template* is a program with parameters, such as "read the balance of account $a$, then write it", that the application may run any number of times with any arguments. A set of templates is robust if every finite set of instances is robust. This is the form that matches real applications, and the set of instances is infinite.

## Variants

- **Concrete transactions** against read uncommitted, read committed or snapshot isolation, as in the definition.
- **Templates or programs**, with parameters, loops or several client processes, where the instances are unbounded.
- **Mixed levels.** Each program gets its own level, and the question is whether the mix is serializable, or which programs need the strong level (Fekete, PODS 2005).
- **Other levels**: parallel snapshot isolation, causal consistency and the levels of [highly available transactions](/highly-available-transactions/), studied by Cerone, Gotsman and Yang and others.
- **Robustness against no isolation.** Pieces of transactions run as separate transactions, which is the correctness question of [transaction chopping](/transaction-chopping/).

## Examples

| transactions | read committed | snapshot isolation |
|---|---|---|
| $T_1 = r(x)\, w(x)$, $T_2 = r(x)\, w(x)$ | not robust: the lost update $r_1(x)\, r_2(x)\, w_2(x)\, c_2\, w_1(x)\, c_1$ | robust: first-committer-wins aborts one writer |
| $T_1 = r(x)\, r(y)$, $T_2 = w(x)\, w(y)$ | not robust: the read skew $r_1(x)\, w_2(x)\, w_2(y)\, c_2\, r_1(y)\, c_1$ | robust: $T_1$ reads one snapshot |
| $T_1 = r(x)\, w(y)$, $T_2 = r(y)\, w(x)$ | not robust | not robust: the [write skew](/write-skew/) |
| $T_1 = r(x)\, w(x)\, w(y)$, $T_2 = r(y)\, w(x)$ | not robust | robust: both write $x$ |

**Why the second row is robust against SI.** A cycle needs two consecutive rw arcs, and an rw arc leaves a transaction only when it reads an item that another writes. $T_2$ reads nothing, so no rw arc leaves $T_2$, and $T_1$ is read-only, so no arc of any kind enters $T_1$ except wr arcs. No cycle has two rw arcs in a row, so by the dangerous structure theorem every schedule is serializable.

**Why the last row is robust against SI.** The two transactions both write $x$, so under first-committer-wins they are never concurrent, and the theorem needs concurrent pairs. Adding the write $w(x)$ to $T_1$ is how one fixes the third row: it *materializes* the conflict.

## Known algorithms

- **Static dependency graph (snapshot isolation).** Fekete et al. (2005) build a graph on the programs with an arc for each possible conflict, mark an rw arc *vulnerable* when the two programs can run concurrently without a write conflict, and test whether some program has a vulnerable arc in and a vulnerable arc out on a cycle. If not, the programs are robust. The test is sufficient but not necessary, and it is a reachability check on a small graph.
- **Concrete transactions under read committed.** Ketsman et al. show that a non-robust set has a counterexample schedule of a restricted form, and search for it. The search is exponential in the worst case, which is unavoidable unless P = NP.
- **Templates under read committed.** Vandevoort et al. (PVLDB 2021) decide robustness for a class of templates in polynomial time, by reasoning on the templates and not on their instances. The ICDT 2022 paper adds functional constraints such as foreign keys, which rule out some conflicts and make more workloads robust.
- **Programs with processes.** Beillahi, Bouajjani and Enea (CAV 2019) reduce robustness against snapshot isolation to a reachability problem for an instrumented program, which tools for program verification can solve.
- **Chopping.** For pieces with no isolation between them, the SC-cycle test of [transaction chopping](/transaction-chopping/) is a sufficient condition that runs in polynomial time.

## Bounds

- **Read committed, concrete transactions:** coNP-complete (Ketsman et al.). The upper bound is direct: to show non-robustness, guess an allowed schedule and check that its dependency graph has a cycle. The lower bound is a reduction in the same paper.
- **Read uncommitted, concrete transactions:** LOGSPACE-complete in the formalization of Ketsman et al., so much easier than read committed.
- **Snapshot isolation, programs with processes:** EXPSPACE-complete in general and PSPACE-complete for a fixed number of processes, for the finite-state programs of Beillahi, Bouajjani and Enea.
- **Templates:** polynomial time for the classes of Vandevoort et al., even though each template has infinitely many instances.

## Reductions

- **To cycle search.** All methods look for a cycle in a dependency graph that an allowed schedule can produce. The level decides which cycles are possible: under snapshot isolation only those with two consecutive vulnerable rw arcs, under read committed also those with one.
- **To a certificate check.** Non-robustness has a short certificate, an allowed schedule with a cycle, whenever checking that a schedule is allowed takes polynomial time. This puts non-robustness for concrete transactions in NP for each of the levels above, and robustness in coNP.
- **To and from chopping.** Robustness against no isolation between pieces is the correctness of a chopping. Cerone, Gotsman and Yang give chopping criteria for snapshot isolation and parallel snapshot isolation in the same graph terms.

## Applications

- **TPC-C under snapshot isolation.** Fekete et al. showed by the static dependency graph that the TPC-C programs are robust against snapshot isolation, so a database that runs TPC-C at snapshot isolation gives serializable results.
- **Choosing a level per program.** A database that offers both snapshot isolation and a serializable level can run each program at the weakest safe level; Fekete (2005) gives a method to choose.
- **Program repair.** When a workload is not robust, the counterexample points to the transactions on the cycle; adding a write that materializes the conflict, or running those transactions at a stronger level, makes it robust.

## References
