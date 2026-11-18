---
tag: Q5KMJR
kind: theorem
slug: snapshot-isolation-dangerous-structure
name: Dangerous structure theorem
aliases:
- Fekete snapshot isolation theorem
- consecutive rw-antidependencies theorem
- dangerous structure
area: databases/transactions-and-concurrency
level: advanced
summary: "Every cycle in the dependency graph of a snapshot isolation history has two rw-antidependency arcs in a row between concurrent transactions, and the last of the three commits first."
prereqs: [snapshot-isolation, adya-isolation-levels, multiversion-serializability]
see_also: [serializable-snapshot-isolation, write-skew, transaction-anomalies, robustness-against-weak-isolation, isolation-levels, multiversion-concurrency-control, conflict-graph, serializability]
sources:
  - paper: doi:10.1145/1071610.1071615
    title: "Alan Fekete, Dimitrios Liarokapis, Elizabeth O'Neil, Patrick O'Neil and Dennis Shasha, Making snapshot isolation serializable, ACM Transactions on Database Systems 30(2), 2005"
    locator: "the theorem on two consecutive vulnerable anti-dependency edges in every cycle of an SI history, the static dependency graph, and the analysis of TPC-C; chapter level only"
  - paper: doi:10.1145/1065167.1065193
    title: "Alan Fekete, Allocating isolation levels to transactions, Proceedings of ACM PODS 2005, pages 206 to 215"
    locator: "the use of the theorem to decide which programs must run with two-phase locking so that a mix of SI and locking is serializable, chapter level only"
  - paper: doi:10.1145/1376616.1376690
    title: "Michael J. Cahill, Uwe Röhm and Alan Fekete, Serializable isolation for snapshot databases, Proceedings of ACM SIGMOD 2008"
    locator: "the run-time use of the theorem (abort a transaction with an rw arc in and an rw arc out) and the discussion of false positives, chapter level only"
  - paper: "Alan Fekete, Elizabeth O'Neil and Patrick O'Neil, A read-only transaction anomaly under snapshot isolation, ACM SIGMOD Record 33(3), 2004, pages 12 to 14"
    locator: "the three-transaction anomaly with a read-only transaction"
  - paper: doi:10.1145/223784.223785
    title: "Hal Berenson, Phil Bernstein, Jim Gray, Jim Melton, Elizabeth O'Neil and Patrick O'Neil, A critique of ANSI SQL isolation levels, Proceedings of ACM SIGMOD 1995"
    locator: "Section 4.2, the definition of snapshot isolation with first-committer-wins"
---

## Statement

Let $H$ be a history of committed transactions under [snapshot isolation](/snapshot-isolation/): each $T_i$ has a start time $s_i$ and a commit time $c_i$, all distinct, reads the last version of each item committed before $s_i$ (or its own write), and no two concurrent transactions write the same item (first-committer-wins). Two transactions are *concurrent* if $s_i < c_j$ and $s_j < c_i$. Let $DSG(H)$ be the dependency graph of committed transactions with ww, wr and rw arcs, with the versions of each item ordered by commit time.

**Theorem** (Fekete, Liarokapis, O'Neil, O'Neil and Shasha, 2005). Every cycle of $DSG(H)$ contains two consecutive arcs $T_1 \xrightarrow{rw} T_2 \xrightarrow{rw} T_3$ such that $T_1$ and $T_2$ are concurrent, $T_2$ and $T_3$ are concurrent, and $T_3$ commits first among the transactions of the cycle. $T_1$ and $T_3$ may be the same transaction.

## In plain words

Under snapshot isolation, a transaction that reads an item can miss a change that a concurrent transaction makes to it. That missed change is an "anti-dependency": the reader seems to come before the writer. A cycle of such orders means that no serial order exists. The theorem says that a bad cycle cannot be made of ordinary dependencies and a single missed change. It always needs two missed changes in a row, through a middle transaction (the pivot) that runs at the same time as both its neighbors. So a system can watch for a transaction that both misses a change and has its own change missed by another. Aborting such a transaction is enough to keep every result serializable.

## Proof

All arcs join distinct committed transactions. Versions of an item are ordered by the commit times of their writers.

**Lemma A.** If $T_i \xrightarrow{ww} T_j$ or $T_i \xrightarrow{wr} T_j$, then $c_i < s_j$.

*Proof.* For ww, $T_i$ and $T_j$ both write the same item, so by first-committer-wins they are not concurrent. The version of $T_j$ follows that of $T_i$, so $c_i < c_j$. Not concurrent means $c_i < s_j$ or $c_j < s_i$; the second gives $c_j < s_i < c_i$, which contradicts $c_i < c_j$. For wr, $T_j$ reads the version of $T_i$ from its snapshot, which contains only versions committed before $s_j$. $\square$

**Lemma B.** If $T_i \xrightarrow{rw} T_j$, then $s_i < c_j$.

*Proof.* $T_i$ reads a version $x_k$ from its snapshot, and $T_j$ installs the next version of $x$ after $x_k$. If $c_j < s_i$, the version of $T_j$ is in the snapshot of $T_i$, and it is later than $x_k$; then $T_i$ reads it or a later one, not $x_k$. $\square$

**The theorem.** Take a cycle, and let $T_3$ be the transaction in it with the smallest commit time. Let $T_2 \to T_3$ be the arc of the cycle that enters $T_3$.

*The arc into $T_3$ is rw.* If it were ww or wr, Lemma A would give $c_2 < s_3 < c_3$, against the choice of $T_3$. So $T_2 \xrightarrow{rw} T_3$, and by Lemma B, $s_2 < c_3$. Also $c_3 < c_2$ by the choice of $T_3$, so $s_2 < c_3 < c_2$, and with $s_3 < c_3 < c_2$ the two are concurrent.

*The arc into $T_2$ is rw.* Let $T_1 \to T_2$ be the arc of the cycle that enters $T_2$; $T_1 = T_3$ is possible if the cycle has length 2. If the arc were ww or wr, Lemma A would give $c_1 < s_2 < c_3$; if $T_1 \ne T_3$ this contradicts the choice of $T_3$, and if $T_1 = T_3$ it contradicts $s_2 < c_3$. So $T_1 \xrightarrow{rw} T_2$, and by Lemma B, $s_1 < c_2$. Also $s_2 < c_3 \le c_1$, since $c_3$ is the smallest commit time in the cycle. So $T_1$ and $T_2$ are concurrent. $\square$

A history whose DSG has no cycle is serializable, in the order of a topological sort, by the [MVSG theorem](/multiversion-serializability/). So every history under snapshot isolation that is not serializable contains the structure of the theorem.

## Consequences

**No cycle with a single anti-dependency.** Every cycle has at least two rw arcs. So snapshot isolation forbids the phenomenon G-single of [Adya's isolation levels](/adya-isolation-levels/), and with it the lost update, the non-repeatable read and read skew of the [transaction anomalies](/transaction-anomalies/). The anomalies it allows are those with two rw arcs: the [write skew](/write-skew/) when the cycle has length 2, and longer cycles such as the read-only anomaly.

**Read-only transactions.** If $T_1$ in the theorem is read-only, then $T_3$ commits before $T_1$ starts. *Proof.* $T_1$ installs no versions, so no ww or rw arc enters it; the arc of the cycle that enters $T_1$ is $T_0 \xrightarrow{wr} T_1$, and Lemma A gives $c_0 < s_1$. Since $c_3 \le c_0$, $c_3 < s_1$. $\square$ In the read-only anomaly of Fekete, O'Neil and O'Neil (2004), the report $T_1$ starts after the deposit $T_3$ commits and misses the withdrawal $T_2$, which is the pivot. A read-only transaction whose snapshot was taken before any such $T_3$ could commit is safe; PostgreSQL uses this rule for safe snapshots.

**Run-time prevention.** If the system aborts any transaction that has an rw arc in from a concurrent transaction and an rw arc out to a concurrent transaction, no committed history has the structure, so every committed history is serializable. This is [serializable snapshot isolation](/serializable-snapshot-isolation/) (Cahill, Röhm and Fekete, 2008). The commit-order clause lets the system wait: a pivot $T_2$ is dangerous only if $T_3$ commits first.

**Static analysis.** For a fixed set of transaction programs, Fekete et al. build a *static dependency graph* with an arc between two programs when some executions of them conflict, and mark an rw arc *vulnerable* when the two can run concurrently without a ww conflict. If no program has a vulnerable arc in and a vulnerable arc out on a cycle, every execution under snapshot isolation is serializable. They showed in this way that TPC-C is serializable under snapshot isolation. This is one method for [robustness against weak isolation](/robustness-against-weak-isolation/). Fekete (PODS 2005) used the same graph to choose which programs must run under two-phase locking when the others run under snapshot isolation.

**Removing a structure.** A dangerous structure in the static graph is removed by adding a write that both programs on a vulnerable arc perform (materializing the conflict), or by turning the read of the arc into a write (promotion). Either way the arc gets a ww conflict and stops being vulnerable.

## Tightness

**The converse fails.** A dangerous structure need not lie on a cycle. With $T_1 = r(x)\, w(z)$, $T_2 = r(y)\, w(x)$ and $T_3 = w(y)$, the history $r_1(x)\, r_2(y)\, w_2(x)\, w_3(y)\, w_1(z)\, c_3\, c_2\, c_1$ has $T_1 \xrightarrow{rw} T_2 \xrightarrow{rw} T_3$ between concurrent transactions with $T_3$ first to commit, yet it is serializable as $T_1, T_2, T_3$. So the theorem gives a sufficient test for serializability, not a characterization, and methods built on it abort some serializable histories; the [serializable snapshot isolation](/serializable-snapshot-isolation/) page discusses these false positives.

**Two is the right number.** A cycle can have exactly two rw arcs and no other arcs: the write skew $r_1(x)\, r_1(y)\, r_2(x)\, r_2(y)\, w_1(x)\, w_2(y)\, c_1\, c_2$ has the cycle $T_1 \xrightarrow{rw} T_2 \xrightarrow{rw} T_1$. So "two consecutive rw arcs" cannot be raised to three, and cannot be lowered to one by the first consequence.

**Concurrency matters.** An rw arc between transactions that are not concurrent is harmless: if $c_i < s_j$, then $T_i$ is before $T_j$ in every order consistent with real time, and the arc agrees with that. A cycle can contain such arcs, but the theorem finds a pair of consecutive arcs where both are between concurrent transactions; a test that ignored concurrency would abort far more.

**First-committer-wins is needed.** Without it, two concurrent transactions may write the same item, Lemma A fails for ww arcs, and the lost update $r_1(x_0)\, r_2(x_0)\, w_2(x_2)\, c_2\, w_1(x_1)\, c_1$ is a cycle $T_1 \xrightarrow{rw} T_2 \xrightarrow{ww} T_1$ with a single rw arc.

## History

Berenson et al. defined snapshot isolation in 1995 and noted the write skew. Adya's thesis (1999) defined snapshot isolation by graph phenomena, which already exclude cycles with one anti-dependency. Fekete, O'Neil and O'Neil found the read-only anomaly in 2004. The theorem with two consecutive vulnerable edges was published by Fekete, Liarokapis, O'Neil, O'Neil and Shasha in ACM TODS in 2005, together with the static dependency graph and the TPC-C analysis; Fekete's PODS 2005 paper applied it to mixed isolation levels. Cahill, Röhm and Fekete built serializable snapshot isolation on it in 2008, and Ports and Grittner implemented it in PostgreSQL 9.1 in 2011, with the read-only rules above.

## References
