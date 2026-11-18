---
tag: C7AQN1
kind: definition
slug: adya-isolation-levels
name: "Adya's generalized isolation levels"
aliases:
- direct serialization graph
- DSG isolation levels
- portable isolation levels
- PL-1 to PL-3
area: databases/transactions-and-concurrency
level: advanced
summary: "Isolation levels defined by the cycles they forbid in a graph of dependencies between committed transactions, so that locking, optimistic and multiversion systems can all meet them."
prereqs: [isolation-levels, multiversion-serializability, conflict-graph]
see_also: [transaction-anomalies, write-skew, snapshot-isolation, snapshot-isolation-dangerous-structure, phantom-problem, serializability, highly-available-transactions, consistency-models]
sources:
  - url: https://pmg.csail.mit.edu/papers/adya-phd.pdf
    title: "Atul Adya, Weak consistency, a generalized theory and optimistic implementations for distributed transactions, PhD thesis, MIT, 1999"
    locator: "the chapters on histories with version orders, the direct serialization graph, the phenomena G0 to G2 and G-single, the levels PL-1 to PL-3 with PL-2+ and PL-2.99, and the start-ordered serialization graph with PL-SI; chapter level only"
  - paper: "Atul Adya, Barbara Liskov and Patrick O'Neil, Generalized isolation level definitions, Proceedings of the 16th IEEE International Conference on Data Engineering (ICDE), 2000"
    locator: "the conference version of the definitions of the DSG, G0, G1a, G1b, G1c, G2-item and G2, and of the portable levels, chapter level only"
  - paper: doi:10.1145/223784.223785
    title: "Hal Berenson, Phil Bernstein, Jim Gray, Jim Melton, Elizabeth O'Neil and Patrick O'Neil, A critique of ANSI SQL isolation levels, Proceedings of ACM SIGMOD 1995"
    locator: "the phenomena P0 to P3 in their broad form, which the generalized definitions replace"
  - url: https://arxiv.org/abs/1609.06670
    title: "Natacha Crooks, Youer Pu, Lorenzo Alvisi and Allen Clement, Seeing is believing, a client-centric specification of database isolation, arXiv 1609.06670"
    locator: "the restatement of Adya's definitions, used to compare them with state-based definitions, chapter level only"
---

Atul Adya's thesis (1999), and the paper of Adya, Liskov and O'Neil (2000), define [isolation levels](/isolation-levels/) by the shapes of cycles in the *direct serialization graph* (DSG) of a history, a graph on the committed transactions with an arc for each write dependency, read dependency and anti-dependency. The levels of Berenson et al. (1995) forbid patterns of operations such as "a read of data that has not committed yet", and in effect assume a locking implementation; optimistic and multiversion systems that produce correct histories by other means fail those definitions. Adya's levels speak only about committed transactions and the versions they read and install, so any implementation can meet them. The graph is the [multiversion serialization graph](/multiversion-serializability/) with the version order given in the history, and its cycles are the [transaction anomalies](/transaction-anomalies/). The four *portable levels* PL-1, PL-2, PL-2.99 and PL-3 match read uncommitted, read committed, repeatable read and serializable; the thesis adds PL-2+, the weakest level with consistent reads, and PL-SI, a definition of [snapshot isolation](/snapshot-isolation/) without timestamps.

## Definition

**Histories.** A *history* $H$ consists of the reads, writes, commits and aborts of the transactions, and a *version order* $\ll$: for each object, a total order on the versions installed by committed transactions. Each write $w_i(x_i)$ makes a version $x_i$; a read $r_j(x_i)$ names the version it returns; a *predicate read* $r_j(P : V)$ names the predicate $P$ and the set $V$ of versions, one per object, from which its matches were computed. A version of $x$ *changes the matches* of $P$ if $x$ matches $P$ in that version and not in the version before it in $\ll$, or the other way round.

**Dependencies.** For committed $T_i \ne T_j$:

- $T_i \xrightarrow{ww} T_j$ (directly write-depends) if $T_i$ installs $x_i$ and $T_j$ installs the next version of $x$ after $x_i$ in $\ll$.
- $T_i \xrightarrow{wr} T_j$ (directly read-depends) if $T_j$ reads $x_i$ (an *item* read dependency), or if a predicate read of $T_j$ uses a version of $x$ equal to or later than a version $x_i$ that changes the matches of $P$ (a *predicate* read dependency).
- $T_i \xrightarrow{rw} T_j$ (directly anti-depends) if $T_i$ reads a version $x_k$ and $T_j$ installs the next version of $x$ after $x_k$ (an *item* anti-dependency), or if $T_j$ installs a version that changes the matches of a predicate read of $T_i$ and comes after the version that read used (a *predicate* anti-dependency).

**DSG.** $DSG(H)$ has a node for each committed transaction and an arc for each of these dependencies.

**Phenomena.**

- **G0** (write cycles): $DSG(H)$ has a cycle of ww arcs only.
- **G1a** (aborted reads): a committed transaction reads a version written by a transaction that aborts.
- **G1b** (intermediate reads): a committed transaction reads a version of $x$ written by $T_i$ that is not the last version of $x$ that $T_i$ writes.
- **G1c** (circular information flow): $DSG(H)$ has a cycle of ww and wr arcs only.
- **G1** is G1a, G1b or G1c.
- **G-single** (single anti-dependency cycles): $DSG(H)$ has a cycle with exactly one rw arc.
- **G2-item** (item anti-dependency cycles): $DSG(H)$ has a cycle with at least one item rw arc.
- **G2** (anti-dependency cycles): $DSG(H)$ has a cycle with at least one rw arc.

**Levels.** A history is at the level if it shows none of the listed phenomena.

| level | forbids | corresponds to |
|---|---|---|
| PL-1 | G0 | read uncommitted |
| PL-2 | G1 | read committed |
| PL-2+ | G1, G-single | consistent reads, no lost updates |
| PL-2.99 | G1, G2-item | repeatable read |
| PL-3 | G1, G2 | serializable |
| PL-SI | G1, G-SI | snapshot isolation |

A history without G1 and G2 has an acyclic DSG, and is then serializable: any topological sort is a serial order, as in the [MVSG theorem](/multiversion-serializability/).

**PL-SI.** For snapshot isolation each committed transaction also has a start point and a commit point in one time order. The *start-ordered serialization graph* $SSG(H)$ is $DSG(H)$ plus a *start-dependency* arc $T_i \xrightarrow{s} T_j$ whenever $T_i$ commits before $T_j$ starts. **G-SIa** (interference) holds if $SSG(H)$ has a ww or wr arc from $T_i$ to $T_j$ but no start-dependency arc from $T_i$ to $T_j$: $T_j$ saw or overwrote the effect of a transaction that had not committed when $T_j$ started. **G-SIb** (missed effects) holds if $SSG(H)$ has a cycle with exactly one rw arc. G-SI is G-SIa or G-SIb.

## Examples and non-examples

**A serializable history that the broad P1 forbids.** $w_1(x_1)\, r_2(x_1)\, c_1\, c_2$. $T_2$ reads data before $T_1$ commits, so the broad dirty read P1 of Berenson et al. rejects it at read committed. Here $T_1$ commits and the DSG has the single arc $T_1 \xrightarrow{wr} T_2$, so the history is PL-3. An optimistic system that lets $T_2$ read early and makes it wait for $T_1$ at commit produces exactly this.

**A serializable history that the broad P2 forbids.** $r_1(x_0)\, w_2(x_2)\, c_2\, c_1$. $T_2$ writes an item that $T_1$ read before $T_1$ ends, which is the broad fuzzy read P2. The DSG has one arc $T_1 \xrightarrow{rw} T_2$ and no cycle, so the history is PL-3, with the serial order $T_1\, T_2$. A multiversion system can give it at serializable without making $T_2$ wait.

**The lost update is PL-2 but not PL-2+.** $r_1(x_0)\, r_2(x_0)\, w_2(x_2)\, c_2\, w_1(x_1)\, c_1$ with $x_0 \ll x_2 \ll x_1$. The arcs are $T_1 \xrightarrow{rw} T_2$ ($T_1$ read $x_0$, and $T_2$ installs the next version) and $T_2 \xrightarrow{ww} T_1$. The cycle has one rw arc: G-single and G2-item, but no G1.

**Write skew is PL-2+ and PL-SI but not PL-2.99.** $r_1(x_0)\, r_1(y_0)\, r_2(x_0)\, r_2(y_0)\, w_1(x_1)\, w_2(y_2)\, c_1\, c_2$. The cycle $T_1 \xrightarrow{rw} T_2 \xrightarrow{rw} T_1$ has two item rw arcs. So it is G2-item but not G-single. With both transactions concurrent, the SSG has no start arcs and no ww or wr arcs between them, and no cycle with one rw arc, so it is PL-SI: this is the [write skew](/write-skew/) of snapshot isolation.

**A phantom that PL-2.99 allows.** $T_1$ reads the employees of a department by a predicate $P$, and then the stored count $z$. $T_2$ inserts a new employee $y$ in that department, updates $z$ and commits before $T_1$ reads $z$. The predicate read of $T_1$ used the version of $y$ before the insert, so $T_1 \xrightarrow{rw} T_2$ is a predicate anti-dependency, and $T_2 \xrightarrow{wr} T_1$ on $z$. The cycle has one rw arc, which is a predicate arc: the history is not G2-item, so PL-2.99 allows it, but it is G2 and G-single, so PL-3 and PL-2+ forbid it. This is H3 of Berenson et al.

**A serializable history that is not PL-SI.** $T_2$ starts, $T_1$ writes $x_1$ and commits, then $T_2$ reads $x_1$ and commits. The serial order $T_1\, T_2$ explains it, so it is PL-3. But $T_1 \xrightarrow{wr} T_2$ has no start-dependency arc, since $T_1$ committed after $T_2$ started: G-SIa. A snapshot taken at the start of $T_2$ could not contain $x_1$.

## Related definitions

- **How the levels relate.** PL-1 is weaker than PL-2, and PL-3 is stronger than all others except PL-SI. PL-2+ and PL-2.99 are incomparable: write skew separates them one way and the predicate phantom above the other. PL-SI is stronger than PL-2+, since every DSG cycle with one rw arc is an SSG cycle with one rw arc, and it is incomparable with PL-3 and with PL-2.99, as write skew and the last example show.
- [Isolation levels](/isolation-levels/) gives the levels of SQL and of Berenson et al., and the correspondence with locking.
- [Multiversion serializability](/multiversion-serializability/) is the setting: the DSG is the multiversion serialization graph for the version order of the history, with its arcs split by kind.
- The [dangerous structure theorem](/snapshot-isolation-dangerous-structure/) is a statement about DSG cycles under snapshot isolation: every cycle has two rw arcs in a row between concurrent transactions.
- [Highly available transactions](/highly-available-transactions/) and [consistency models](/consistency-models/) use these phenomena to classify which levels a system can give while it stays available during network partitions.

## References
