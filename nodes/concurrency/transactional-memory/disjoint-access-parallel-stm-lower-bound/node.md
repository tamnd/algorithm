---
tag: KV109F
kind: theorem
slug: disjoint-access-parallel-stm-lower-bound
name: Disjoint-access-parallel STM lower bound
aliases:
- Attiya-Hillel-Milani bound
area: concurrency/transactional-memory
level: research
summary: A strictly serializable TM cannot be disjoint-access parallel and also have invisible read-only transactions that always commit (Attiya, Hillel and Milani, 2009).
prereqs: [software-transactional-memory, wait-freedom, serializability]
see_also: [opacity, tl2, norec, multi-version-stm, global-version-clock, obstruction-freedom, dstm, transaction-validation]
sources:
  - paper: doi:10.1007/s00224-010-9304-5
    title: "Hagit Attiya, Eshcar Hillel and Alessia Milani, Inherent limitations on disjoint-access parallel implementations of transactional memory, SPAA 2009, pp. 69 to 78; journal version in Theory of Computing Systems 49(4), 2011, pp. 698 to 719"
    locator: the abstract (the impossibility for invisible read-only transactions that always commit, and the Ω(t) bound on writes), and the definition of weak disjoint-access parallelism
  - paper: doi:10.1145/1378533.1378587
    title: "Rachid Guerraoui and Michal Kapalka, On obstruction-free transactions, SPAA 2008, pp. 304 to 313"
    locator: the definition of strict disjoint-access parallelism and the proof that obstruction-free TMs cannot satisfy it
  - paper: "Amos Israeli and Lihu Rappoport, Disjoint-access-parallel implementations of strong shared memory primitives, PODC 1994"
    locator: the original definition of disjoint-access parallelism, for implementations of multi-word primitives
  - url: https://arxiv.org/abs/1407.6876
    title: "Petr Kuznetsov and Srivatsan Ravi, On partial wait-freedom in transactional memory, arXiv 1407.6876 (ICDCN 2015)"
    locator: Section 2 (the model, weak DAP and invisible reads), Lemma 1 (disjoint-access transactions do not contend), Theorem 4 (Ω(m) expensive patterns in a read-only transaction) and Section 7 (how the results relate to AHM and GK)
  - url: https://www.cse.lehigh.edu/~palmieri/files/pubs/CR-podc2015.pdf
    title: "Sebastiano Peluso, Roberto Palmieri, Paolo Romano, Binoy Ravindran and Francesco Quaglia, Disjoint-access parallelism: impossibility, possibility, and cost of transactional memory implementations, PODC 2015"
    locator: Section 4 (a strictly DAP TM with wait-free invisible read-only transactions once the real-time order is weakened)
---

The **disjoint-access-parallel STM lower bound** of Attiya, Hillel and Milani (SPAA 2009) says that a transactional memory cannot have all of four good properties at once: strict serializability, disjoint-access parallelism (transactions on unrelated data do not touch the same memory), read-only transactions that write nothing to shared memory, and read-only transactions that always commit. In the words of their abstract, TM implementations "cannot be both disjoint-access parallel and have read-only transactions that are invisible and always terminate successfully". They also prove that in a disjoint-access-parallel TM, a read-only transaction of $t$ items that always commits needs $\Omega(t)$ writes. The result explains why practical STMs such as [TL2](/tl2/) and [NOrec](/norec/) use a [global version clock](/global-version-clock/) or let readers abort.

## Statement

**Model.** There are $n$ deterministic processes. They communicate by applying primitives to shared *base objects*; one primitive on one base object is an *event*. A primitive is *trivial* if it never changes the base object (a read) and *nontrivial* otherwise. A TM implementation gives each process the operations $\mathit{read}_k(X)$, $\mathit{write}_k(X, v)$ and $\mathit{tryC}_k$ of transactions $T_k$ on *items* $X$ (t-objects); each returns a value, or ok, or commit, or abort. The *data set* $\mathit{Dset}(T)$ is the set of items that $T$ accesses. A transaction is *read-only* if it has no write.

- Two events *contend* on a base object $b$ if both access $b$ and at least one is nontrivial. Two transactions *concurrently contend* on $b$ after an execution $E$ if each has an enabled event on $b$ in the configuration after $E$ and these two events contend.
- For transactions $T_1$ and $T_2$ in $E$, let $\tau$ be the set of transactions that are concurrent in $E$ with $T_1$ or with $T_2$, together with $T_1$ and $T_2$. The *conflict graph* has the items of the data sets of $\tau$ as vertices and an edge $\{X, Y\}$ whenever some $T \in \tau$ accesses both $X$ and $Y$. $T_1$ and $T_2$ are *disjoint-access* in $E$ if no path joins an item of $T_1$ to an item of $T_2$.
- A TM is **weak disjoint-access parallel** (weak DAP) if, in every execution $E$, two transactions concurrently contend on a base object after $E$ only if they are not disjoint-access in $E$.
- A TM has **invisible reads** if no read-only transaction ever applies a nontrivial primitive.
- **Wait-free read-only transactions**: every read-only transaction of a process that keeps taking steps commits within a finite number of its own steps.
- **Sequential progress for updating transactions**: a transaction that runs alone (step contention-free) from a configuration with no live transaction commits.
- The TM is **strictly serializable**: for each execution there is a serial order of the committed transactions, consistent with the real-time order of transactions, in which every read returns the last value written before it.

**Theorem 1 (Attiya, Hillel and Milani, 2009).** No TM implementation is strictly serializable, weak DAP, has invisible reads, and gives wait-free read-only transactions and sequential progress for updating transactions. The impossibility holds already for two items and three static transactions.

**Theorem 2 (Attiya, Hillel and Milani, 2009; cited, not proved here).** In a strictly serializable TM that is disjoint-access parallel in the stronger sense of their paper, and in which read-only transactions always commit, there is an execution in which a read-only transaction that reads $t$ items applies $\Omega(t)$ nontrivial primitives (writes).

Theorem 1 is stated here with the progress conditions that Kuznetsov and Ravi use; it is the first result of the abstract of AHM, and the proof below follows the published argument of Kuznetsov and Ravi, which they say is inspired by AHM.

## In plain words

Take an STM where readers leave no trace in memory, never give up, and where transactions on unrelated data never touch the same memory. Reader R reads x, then y. Between the two reads, writer A writes x and commits, and then writer B writes y and commits.

R saw the old x, so R comes before A. B started after A ended, so B comes after A. If R now sees the new y, R comes after B: a cycle. So R must see the old y. But if B had run before R started, R must see the new y. Some memory must record which case happened. R wrote nothing, and B cannot touch memory that A or R uses, because their data are unrelated. So nothing records it.

## Proof

The proof needs two facts about executions. Throughout, a *fragment* of a transaction is a sequence of its events with no events of other processes in between.

**Lemma A (swapping).** Let $C$ be a configuration, $\rho$ a sequence of events of process $p$ and $\sigma$ a sequence of events of process $q \ne p$, such that $C \cdot \rho \cdot \sigma$ is an execution and no event of $\rho$ contends with an event of $\sigma$. Then $C \cdot \sigma \cdot \rho$ is an execution, each event gets the same response in both, and both end in the same configuration.

*Proof.* The response of an event depends only on the state of its base object, and the next event of a process depends only on the responses it got. Each base object that $\sigma$ accesses is either not accessed by $\rho$ or only read by both, so $\rho$ does not change it, and $\sigma$ run from $C$ sees the same states as after $\rho$; so $q$ takes the same events and gets the same responses. Each base object that $\rho$ accesses is not changed by $\sigma$ in the same way, so $\rho$ run after $\sigma$ is also unchanged. Each base object is changed by at most one of the two sequences, so the final states agree, and so do the local states of $p$ and $q$. $\square$

**Lemma B (disjoint-access transactions do not contend; Kuznetsov and Ravi, Lemma 1).** Let $M$ be weak DAP. Let $\alpha \cdot \rho_1 \cdot \rho_2$ be an execution, where $\rho_1$ is a fragment of $T_1$, $\rho_2$ is a fragment of $T_2$, neither transaction takes a step in $\alpha$, and $T_1$, $T_2$ are disjoint-access in $\alpha \cdot \rho_1 \cdot \rho_2$. Then no event of $\rho_1$ contends with an event of $\rho_2$.

*Proof.* Suppose that some do. Call a base object *shared* if an event of $\rho_1$ and an event of $\rho_2$ contend on it. There are two cases.

1. Some event of $\rho_1$ is nontrivial on a shared object. Let $e_1$ be the last such event of $\rho_1$, on object $b$, and let $e_2$ be the first event of $\rho_2$ that accesses $b$.
2. Every event of $\rho_1$ on a shared object is trivial. Then $\rho_2$ has a nontrivial event on a shared object; let $e_2$ be the first one, on object $b$, and let $e_1$ be the last event of $\rho_1$ that accesses $b$.

Let $\rho_1'$ and $\rho_2'$ be the prefixes of $\rho_1$ and $\rho_2$ before $e_1$ and $e_2$. The part of $\rho_1$ from $e_1$ on changes no object that $\rho_2'$ accesses: in case 1, after $e_1$ it changes only objects that $\rho_2$ never accesses, and $e_1$ itself changes $b$, which $\rho_2'$ does not access; in case 2, it changes only objects that $\rho_2$ never accesses. So $\rho_2'$ run after $\alpha \cdot \rho_1'$ sees the same object states as after $\alpha \cdot \rho_1$, and $\alpha \cdot \rho_1' \cdot \rho_2'$ is an execution. After it, $T_1$ is about to apply $e_1$ and $T_2$ is about to apply $e_2$, both on $b$, and one of them is nontrivial, so $T_1$ and $T_2$ concurrently contend on $b$. In a prefix, the data sets and the set of concurrent transactions can only be smaller, so the conflict graph has no more edges, and $T_1$, $T_2$ are still disjoint-access. This contradicts weak DAP. $\square$

**Proof of Theorem 1.** Suppose that $M$ has all the properties. Let $X_1, X_2$ be items with initial value 0. Consider three transactions, run by three processes:

- $T_0$ is read-only: $\mathit{read}_0(X_1)$, $\mathit{read}_0(X_2)$, $\mathit{tryC}_0$;
- $T_1$ is $\mathit{write}_1(X_1, 1)$, $\mathit{tryC}_1$;
- $T_2$ is $\mathit{write}_2(X_2, 1)$, $\mathit{tryC}_2$.

*Step 1: the execution $E$.* From the initial configuration, which has no live transaction, let $T_2$ run alone; by sequential progress it commits, in a fragment $\delta_2$. Then let $T_0$ run alone until $\mathit{read}_0(X_1)$ returns; by wait-freedom this is a finite fragment $\alpha_1$. Its response is 0: in the execution $\delta_2 \cdot \alpha_1$ followed by $T_0$ alone until it commits, no transaction writes $X_1$, so strict serializability forces 0, and $\alpha_1$ is the same in both executions. Now let $T_1$ run alone; call its fragment $\delta_1$. Reads are invisible, so $\alpha_1$ changed no base object, and $\delta_1$ sees the same object states as in the execution $\delta_2 \cdot \delta_1$, where $T_1$ runs alone from a configuration with no live transaction and so commits by sequential progress. So $T_1$ commits in $\delta_2 \cdot \alpha_1 \cdot \delta_1$ too. Finally let $T_0$ run alone until it commits, by wait-freedom, in a fragment $\alpha_2$. Call the whole execution $E = \delta_2 \cdot \alpha_1 \cdot \delta_1 \cdot \alpha_2$. $T_2$ committed before $T_0$ started, so strict serializability puts $T_2$ before $T_0$, and $\mathit{read}_0(X_2)$ returns 1 in $E$.

*Step 2: move $T_2$ to after $T_1$.* In $\delta_2 \cdot \alpha_1$, the transactions $T_2$ and $T_0$ have data sets $\{X_2\}$ and $\{X_1\}$ so far, and no transaction accesses both items, so they are disjoint-access. By Lemma B with an empty $\alpha$, $\delta_2$ and $\alpha_1$ do not contend, and by Lemma A, $\alpha_1 \cdot \delta_2$ ends in the same configuration as $\delta_2 \cdot \alpha_1$. So $\alpha_1 \cdot \delta_2 \cdot \delta_1$ is an execution with the same events. In it, the transactions concurrent with $T_2$ or $T_1$ are $T_0$, $T_1$, $T_2$, with data sets $\{X_1\}$, $\{X_1\}$, $\{X_2\}$; again no transaction accesses both items, so $T_2$ and $T_1$ are disjoint-access. By Lemma B with $\alpha = \alpha_1$, the fragments $\delta_2$ and $\delta_1$ do not contend, and by Lemma A, $\alpha_1 \cdot \delta_1 \cdot \delta_2$ ends in the same configuration as $\delta_2 \cdot \alpha_1 \cdot \delta_1$.

*Step 3: the contradiction.* From that configuration, $T_0$ takes the same events as in $\alpha_2$ and gets the same responses. So $E' = \alpha_1 \cdot \delta_1 \cdot \delta_2 \cdot \alpha_2$ is an execution in which $T_0$, $T_1$ and $T_2$ all commit, $\mathit{read}_0(X_1)$ returns 0 and $\mathit{read}_0(X_2)$ returns 1. Take a serial order of $E'$ that strict serializability gives. $T_1$ is the only writer of $X_1$ and $T_0$ read 0, so $T_0$ is before $T_1$. $T_1$ committed before $T_2$ started, so $T_1$ is before $T_2$. $T_2$ is the only writer of $X_2$ and $T_0$ read 1, so $T_2$ is before $T_0$. These three relations form a cycle, so no such order exists, a contradiction. $\blacksquare$

Each hypothesis is used once. Invisibility makes $T_1$ commit, because $T_0$ left no trace. Weak DAP lets us move $T_2$ without anyone noticing. Wait-freedom makes $T_0$ commit instead of aborting, and strict serializability supplies the real-time edge from $T_1$ to $T_2$.

## Consequences

- **Practical STMs give up DAP or wait-free readers.** In TL2 and NOrec, every updating transaction writes one global clock or sequence lock, so two transactions on unrelated data contend on it, and the TM is not DAP; and a read-only transaction may still abort. STMs that keep per-object metadata and no global clock keep reads invisible but let a reader abort when validation fails; Kuznetsov and Ravi note that several popular TMs satisfy weak DAP.
- **Multi-version STMs.** A [multi-version STM](/multi-version-stm/) can let a read-only transaction read an old snapshot and always commit. By Theorem 1, if its reads are invisible and it is strictly serializable, it cannot be weak DAP; designs of this kind typically use a global clock to pick the snapshot.
- **The cost of visible reads.** Theorem 2 says that a DAP TM with read-only transactions that always commit must pay writes in proportion to the read set. Kuznetsov and Ravi strengthen this for weak DAP: a read-only transaction that reads $m$ items performs $\Omega(m)$ expensive patterns (a read after a write to another location, which needs a memory fence, or an atomic read-modify-write), even when updating transactions have only sequential progress (their Theorem 4).
- **Obstruction freedom.** Guerraoui and Kapalka (SPAA 2008) defined **strict DAP**: two transactions contend on a base object only if their data sets intersect, whether or not they are concurrent. They proved that no [obstruction-free](/obstruction-freedom/) TM is strictly DAP. Their scenario uses one transaction that accesses two items $x$ and $y$ and two transactions that access only $x$ and only $y$; strict DAP forbids the last two to contend, so they cannot exchange what they learned about the first, while obstruction freedom forces each of them to make progress alone. Every strictly DAP TM is weak DAP, but not the other way round, so this result says nothing about weak DAP; the proof of Theorem 1 needs wait-free readers instead, and obstruction-free STMs such as [DSTM](/dstm/) let readers abort.

## Tightness

Each hypothesis of Theorem 1 is needed.

- **Without strict serializability.** Peluso, Palmieri, Romano, Ravindran and Quaglia (PODC 2015) build a TM that is DAP in the strongest sense, with wait-free invisible read-only transactions, by weakening the real-time order between transactions and the consistency condition (Extended Update Serializability). The proof above breaks exactly there: it needs the real-time edge from $T_1$ to $T_2$.
- **Without DAP.** With a global clock, $T_2$ changes a base object that $T_0$ reads, so $T_0$ can tell the two orders apart. A multi-version STM with a global clock can then let $T_0$ read the old $X_2$ and commit.
- **Without wait-free readers.** $T_0$ may abort in $E'$, as in an STM that validates the read set.
- **Without invisible reads.** $T_0$ can write a mark that $T_1$ sees; then $T_1$ is no longer alone, and it may wait or abort. Theorem 2 measures how much writing this needs.
- **Without progress for updating transactions.** A TM in which updating transactions never commit has all the other properties, trivially.

## History

Israeli and Rappoport defined disjoint-access parallelism in 1994 for implementations of multi-word primitives. Guerraoui and Kapalka defined strict DAP for TMs and proved at SPAA 2008 that obstruction-free TMs cannot satisfy it. Attiya, Hillel and Milani defined weak DAP and proved Theorems 1 and 2 at SPAA 2009, with a journal version in 2011. Kuznetsov and Ravi gave a single proof that strengthens both of their lower bounds, and Peluso et al. showed in 2015 which weaker consistency conditions make DAP with invisible, always-committing readers possible.

## References
