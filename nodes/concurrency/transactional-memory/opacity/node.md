---
tag: 7CW7RJ
kind: definition
slug: opacity
name: Opacity
aliases:
- opacity correctness condition
- final-state opacity
area: concurrency/transactional-memory
level: advanced
summary: "Safety condition for transactional memory: every transaction, even one that aborts or still runs, sees values that one real-time serial order of committed transactions explains."
prereqs: [transaction, serializability, linearizability]
see_also: [zombie-transactions, transaction-validation, tl2, norec, multi-version-stm, privatization-safety, snapshot-isolation, disjoint-access-parallel-stm-lower-bound]
sources:
  - paper: doi:10.1145/1345206.1345233
    title: "Rachid Guerraoui and Michał Kapałka, On the correctness of transactional memory, PPoPP 2008, pp. 175 to 184"
    locator: the definition of opacity and the examples of inconsistent views of aborted transactions
  - book: doi:10.1007/978-3-031-02002-5
    title: Rachid Guerraoui and Michał Kapałka, Principles of Transactional Memory, Synthesis Lectures on Distributed Computing Theory, 2010
    locator: Chapter 4 (TM correctness issues), Chapter 7 (Opacity, with final-state opacity and the prefix rule), Chapter 8 (Proving opacity)
  - paper: doi:10.1007/s00165-012-0225-8
    title: "Simon Doherty, Lindsay Groves, Victor Luchangco and Mark Moir, Towards formally specifying and verifying transactional memory, Formal Aspects of Computing 25(5), 2013, pp. 769 to 799"
    locator: the TMS1 and TMS2 specifications
  - paper: "Mohsen Lesani, Victor Luchangco and Mark Moir, Putting opacity in its place, 4th Workshop on the Theory of Transactional Memory (WTTM), 2012"
    locator: the machine-checked proofs that every TMS2 history is opaque and every opaque history is TMS1
  - paper: doi:10.1016/j.tcs.2012.04.037
    title: "Damien Imbs and Michel Raynal, Virtual world consistency: a condition for STM systems (with a versatile protocol with invisible read operations), Theoretical Computer Science 444, 2012, pp. 113 to 127"
    locator: the definition of virtual world consistency and its comparison with opacity
  - paper: "Petr Kuznetsov and Srivatsan Ravi, On the cost of concurrency in transactional memory, arXiv:1103.1302 (version 9, 2013)"
    locator: Section 8 (Related work), the statement of the linear lower bound of Guerraoui and Kapałka for progressive opaque TMs with invisible reads
---

**Opacity** is a safety condition for [transactional memory](/software-transactional-memory/), defined by Rachid Guerraoui and Michał Kapałka in 2008. It asks that every [transaction](/transaction/), including one that aborts and one that is still running, sees values that a single serial order of the committed transactions explains, and that this order respects real time. [Serializability](/serializability/) and strict serializability speak only about committed transactions, so they allow a doomed transaction to see an inconsistent state before it aborts. Opacity forbids this, and with it the harm that [zombie transactions](/zombie-transactions/) can do.

## Definition

**Model.** There are $n$ asynchronous processes; each takes steps at its own speed and can crash. The memory is sequentially consistent. The TM gives the processes t-objects; on this page each t-object $x$ is a read/write register with initial value 0. A transaction $T_k$ calls read$_k(x)$, which returns a value or $A_k$; write$_k(x, v)$, which returns ok or $A_k$; tryC$_k$, which returns $C_k$ (committed) or $A_k$ (aborted); and tryA$_k$, which returns $A_k$. A history $H$ is the sequence of the invocation and response events of these calls, and $H|T_k$ is the subsequence of the events of $T_k$.

**Status.** In $H$, $T_k$ is *committed* if $H|T_k$ ends with $C_k$, *aborted* if it ends with $A_k$, *commit-pending* if its last event is the invocation of tryC$_k$, and *live* if it is not committed and not aborted (so a commit-pending transaction is live). $T_i$ *precedes $T_j$ in real time*, written $T_i \prec_H T_j$, if $T_i$ is committed or aborted and its last event comes before the first event of $T_j$ in $H$.

**Completion.** A completion of $H$ is a history $\bar H$ that adds events at the end of $H$ so that no transaction is live: each commit-pending transaction gets the response $C_k$ or the response $A_k$, and each other live transaction is aborted (its pending call, if there is one, returns $A_k$; otherwise tryA$_k$ is added).

**Legality.** A history $S$ is sequential if no two transactions in it overlap. A sequential history is legal if each read in it returns the value of the latest earlier write to the same register, or 0 if there is none. For a transaction $T_k$ of a sequential history $S$, let $\mathrm{vis}_S(T_k)$ be the subsequence of $S$ made of the events of $T_k$ and of the committed transactions that come before $T_k$ in $S$. $T_k$ is *legal in $S$* if $\mathrm{vis}_S(T_k)$ is legal.

**Final-state opacity.** $H$ is final-state opaque if there exist a completion $\bar H$ of $H$ and a sequential history $S$ such that

1. $S$ is equivalent to $\bar H$: $S|T_k = \bar H|T_k$ for every transaction $T_k$;
2. $S$ respects real time: $T_i \prec_H T_j$ implies $T_i \prec_S T_j$;
3. every transaction of $S$, committed or aborted, is legal in $S$.

**Opacity.** $H$ is *opaque* if every prefix of $H$ is final-state opaque. A TM implementation is opaque if every history that it can produce is opaque.

Guerraoui and Kapałka's book gives the condition in these two steps because final-state opacity alone is not closed under prefixes (Example 4). Opacity is closed under prefixes by its definition, so it is a safety property: a violation shows in a finite prefix.

Clause 3 is the heart of the condition. In strict serializability the same clause applies only to committed transactions. Opacity applies it to each transaction, with $\mathrm{vis}_S(T_k)$ in place of the whole prefix, so an aborted transaction must see the committed writes before it and nothing from other aborted transactions. Taking only the committed transactions of $S$ shows that every opaque history is strictly serializable.

## Examples and non-examples

All registers start at 0, and each committed transaction keeps the invariant $x = y$.

**1. The doomed read (not opaque).**

| step | $T_1$ | $T_2$ |
|---|---|---|
| 1 | read$_1(x) \to 0$ | |
| 2 | | write$_2(x, 1)$, write$_2(y, 1)$ |
| 3 | | tryC$_2 \to C_2$ |
| 4 | read$_1(y) \to 1$ | |
| 5 | tryC$_1 \to A_1$ | |

The only committed transaction is $T_2$, so the history is strictly serializable. It is not final-state opaque. $T_1$ must appear in $S$. If $T_1$ comes before $T_2$, then $\mathrm{vis}_S(T_1)$ has no write to $y$ and read$_1(y)$ should return 0. If $T_1$ comes after $T_2$, then read$_1(x)$ should return 1. So no $S$ exists, and already the prefix that ends at step 4 is not final-state opaque. $T_1$ saw $x = 0$ and $y = 1$, a state that no serial order produces. If $T_1$ goes on to compute $1/(1 + x - y)$, it divides by zero; if it runs `while x != y`, it loops forever and never reaches the commit that would abort it. An STM that validates the read set only at commit time produces this history. [TL2](/tl2/) does not: at step 4 the version of $y$ is newer than the read version of $T_1$, so the read aborts.

**2. An old snapshot (opaque).** As in Example 1, but read$_1(y)$ returns 0 and $T_1$ commits. The order $T_1, T_2$ explains every read, and $T_1$ does not precede $T_2$ in real time because $T_1$ ends last. A [multi-version STM](/multi-version-stm/) can produce this history; a single-version STM such as TL2 aborts $T_1$ instead.

**3. Real time (not opaque).** $T_2$ writes $x = 1$ and commits; after that, $T_1$ begins, reads $x \to 0$, and aborts. The history is strictly serializable, because $T_1$ did not commit. It is not opaque: $T_2 \prec_H T_1$ forces $T_2$ before $T_1$ in $S$, and then $T_1$ must read 1.

**4. A read of an uncommitted write (final-state opaque, but not opaque).**

| step | $T_1$ | $T_2$ |
|---|---|---|
| 1 | | write$_2(x, 1)$ |
| 2 | read$_1(x) \to 1$ | |
| 3 | | tryC$_2 \to C_2$ |
| 4 | tryC$_1 \to C_1$ | |

The whole history is final-state opaque with $S = T_2, T_1$. The prefix of steps 1 and 2 is not: $T_2$ is live and not commit-pending there, so every completion aborts it, and then no committed transaction wrote the value 1 that $T_1$ read. Had $T_2$ aborted, $T_1$ would have seen a value that never existed. An STM with [eager versioning](/eager-versioning/) that lets a reader see a write in place produces this history. If $T_2$ had invoked tryC$_2$ before step 2, the prefix would be final-state opaque, since the completion may commit $T_2$; this is the case of a TL2 reader that sees a value right after the write-back.

**5. A read from an aborted transaction (not opaque, but serializable).** $T_1$ writes $x = 5$ and aborts; then $T_2$ reads $x \to 5$ and aborts. No transaction committed, so the history is serializable. It is not opaque, because $\mathrm{vis}_S(T_2)$ never contains the write of the aborted $T_1$.

## Related definitions

- **[Serializability](/serializability/).** The committed transactions are equivalent to some legal serial order. There is no condition on aborted or live transactions and no real-time condition. Example 3 shows why real time matters: without it, a transaction can read a value that was overwritten before it began.
- **Strict serializability.** Serializability with the real-time order of the committed transactions. Opacity implies it, and Examples 1, 3 and 5 show that the converse fails. For a single operation in each transaction, strict serializability is [linearizability](/linearizability/) of the memory.
- **[Zombie transactions](/zombie-transactions/) and [validation](/transaction-validation/).** A zombie is a transaction that will abort but still runs on an inconsistent view. Opacity is the condition that no zombie ever sees such a view. STMs meet it with a [global version clock](/global-version-clock/) (TL2), with value-based validation at each change of a global sequence number ([NOrec](/norec/)), or with incremental validation of the whole read set at each new read, which costs time quadratic in the size of the read set.
- **TMS1 and TMS2.** Doherty, Groves, Luchangco and Moir specify transactional memory as two automata. TMS1 asks that each transaction, including an aborted one, see a state that a serialization of committed and commit-pending transactions explains, but different transactions may use different serializations. TMS2 is more operational. Lesani, Luchangco and Moir proved with a theorem prover that, for read/write registers, every TMS2 history is opaque and every opaque history is TMS1.
- **Virtual world consistency.** Imbs and Raynal ask that the committed transactions be serializable and that each aborted transaction see a state consistent with its own causal past, its "virtual world". Two aborted transactions may then see worlds that no single order explains, so the condition is weaker than opacity, and it allows more transactions to commit.
- **[Snapshot isolation](/snapshot-isolation/).** Each transaction reads from one consistent snapshot, and only write-write conflicts abort. Every transaction sees a consistent state, but the committed transactions need not be serializable (write skew), so snapshot isolation does not imply opacity.
- **[Strong](/strong-atomicity/) and [weak atomicity](/weak-atomicity/), [privatization safety](/privatization-safety/).** Opacity speaks only about accesses inside transactions. What a non-transactional access may see is a separate question, which these pages treat.
- **The cost of opacity.** Guerraoui and Kapałka prove that in an opaque TM that is progressive, uses invisible reads and is strictly data-partitioned, a successful read can take a number of steps linear in the number of t-objects (Kuznetsov and Ravi state the result this way). The [disjoint-access-parallel lower bound](/disjoint-access-parallel-stm-lower-bound/) gives a related cost for read-only transactions.

## References
