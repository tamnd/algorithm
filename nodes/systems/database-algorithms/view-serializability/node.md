---
tag: S03CR7
kind: definition
slug: view-serializability
name: View serializability
aliases:
- view-serializable schedule
- view equivalence of schedules
area: systems/database-algorithms
level: advanced
summary: "A schedule is view serializable if some serial schedule has the same reads-from relation and the same final writes. It is strictly larger than conflict serializability and NP-complete to test."
prereqs: [conflict-serializability]
see_also: [serializability, conflict-graph, thomas-write-rule, timestamp-ordering, concurrency-control, multiversion-concurrency-control]
sources:
  - paper: doi:10.1145/322154.322158
    title: Christos H. Papadimitriou, The serializability of concurrent database updates, Journal of the ACM 26(4), 1979, pages 631 to 653
    locator: the polygraph of a schedule and the proof that testing serializability is NP-complete
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 2 (view equivalence and view serializability) and Chapter 4 (the Thomas write rule)
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: Chapter 3 (final-state, view and conflict serializability, and the NP-completeness of the view test)
  - paper: doi:10.1145/320071.320076
    title: Robert H. Thomas, A majority consensus approach to concurrency control for multiple copy databases, ACM Transactions on Database Systems 4(2), 1979, pages 180 to 209
    locator: the rule that an obsolete update is ignored, the source of view serializable schedules that are not conflict serializable
---

A schedule is *view serializable* if it is view equivalent to a serial schedule: each read sees the value of the same write, and each item gets its final value from the same write. It is the most permissive common form of [serializability](/serializability/) that still looks only at which value each read sees. Every [conflict serializable](/conflict-serializability/) schedule is view serializable, but not the reverse, and Papadimitriou (1979) showed that deciding view serializability is NP-complete. For this reason schedulers enforce conflict serializability, and view serializability is the yardstick that explains rules such as the [Thomas write rule](/thomas-write-rule/).

## Definition

**Model.** A transaction $T_i$ is a sequence of actions $r_i(x)$ and $w_i(x)$. A schedule $S$ interleaves the actions of a set of committed transactions and keeps the order inside each transaction. Name each action by its transaction and its position in that transaction, so that two equal actions such as two copies of $w_1(x)$ differ.

**Reads-from.** A read $r_j(x)$ *reads from* a write $w_i(x)$ in $S$ if $w_i(x) <_S r_j(x)$ and no other write of $x$ lies between them. If no write of $x$ comes before $r_j(x)$, the read reads the initial value; we say it reads from a virtual transaction $T_0$ that writes every item before the schedule starts.

**Final write.** The *final write* of $x$ in $S$ is the last write of $x$ in $S$. One can think of a virtual transaction $T_f$ that reads every item after the schedule ends.

**View equivalence.** Two schedules $S$ and $S'$ over the same transactions are *view equivalent* if

1. each read reads from the same write in $S$ and in $S'$ (or from $T_0$ in both), and
2. each item has the same final write in $S$ and in $S'$.

**View serializability.** $S$ is view serializable if it is view equivalent to some serial schedule. For a schedule with aborts, apply the definition to the committed projection.

**Why this is the right equivalence.** Assume nothing about what a transaction computes: each write $w_i(x)$ may store any function of all values that $T_i$ has read before it. Then two view equivalent schedules give every read the same value and leave the same final state, by induction along the schedule. Each read sees the same write, and that write computed its value from reads that by induction saw the same values.

**Theorem 1.** Every conflict serializable schedule is view serializable, and the inclusion is strict.

*Proof.* Let $S \approx_c S'$. Let $r_j(x)$ read from $w_i(x)$ in $S$. If $i \ne j$, these two actions conflict, so $w_i(x) <_{S'} r_j(x)$; if $i = j$, the order inside $T_i$ gives the same. Let $w_k(x)$ be any other write of $x$. Its order relative to $r_j(x)$ is the same in both schedules: they conflict if $k \ne j$, and they are in one transaction if $k = j$. In the same way its order relative to $w_i(x)$ is the same. In $S$ it is not between them, so it is not between them in $S'$. Hence $r_j(x)$ reads from $w_i(x)$ in $S'$. Reads from $T_0$ are handled by the same argument with no $w_i(x)$. The final write of $x$ is the write that comes after every other write of $x$, and the order of any two writes of $x$ is the same in both schedules. So $S$ and $S'$ are view equivalent. The schedule $S_1$ below shows that the inclusion is strict. $\square$

**Theorem 2 (blind writes).** A write $w_i(x)$ is *blind* if $T_i$ does not read $x$ before it. If a view serializable schedule has no blind writes, it is conflict serializable.

*Proof.* Let $S$ be view equivalent to the serial schedule $S'$, with no blind writes. Fix an item $x$. Let $W_1, \ldots, W_k$ be the transactions that write $x$, in their order in $S'$, and let $L_t$ be the last write of $x$ by $W_t$. Since no write is blind, the first action of $W_t$ on $x$ is a read; call it $f_t$. In $S'$, $f_t$ reads from $L_{t-1}$ (from $T_0$ when $t = 1$), so it does the same in $S$. Hence $L_{t-1} <_S f_t$, and $f_t$ comes before every write of $W_t$. So in $S$ all writes of $W_{t-1}$ come before all writes of $W_t$: the writes of $x$ form the blocks $W_1, \ldots, W_k$ in the same order as in $S'$. Now take any read $r$ of $x$. In $S'$ it reads from $L_s$ for the last writer $W_s$ before its transaction, or from its own transaction's latest write, or from $T_0$. It reads from the same write $w$ in $S$, so in $S$ it lies after $w$ and before the next write of $x$ after $w$. Because the writes are in the same blocks, $r$ is after exactly the same writes of other transactions in $S$ as in $S'$. So every pair of conflicting actions on $x$ has the same order in both schedules. This holds for every $x$, so $S \approx_c S'$. $\square$

**Theorem 3 (Papadimitriou 1979).** Deciding whether a schedule is view serializable is NP-complete.

Membership in NP is easy: guess a serial order and compare the reads-from relations and final writes in polynomial time. For the hardness, Papadimitriou expresses the question with a *polygraph*. It has a node for each transaction plus $T_0$ and $T_f$, an arc $T_i \to T_j$ whenever $T_j$ reads some $x$ from $T_i$, and, for each such pair and each other transaction $T_k$ that writes $x$, a choice: $T_k$ must come before $T_i$ or after $T_j$. The schedule is view serializable exactly when one side of each choice can be picked so that the resulting graph is acyclic. He then shows that acyclicity of polygraphs is NP-complete. A brute-force test tries all $m!$ serial orders of the $m$ transactions in $O(m! \cdot n)$ time for $n$ actions.

## Examples and non-examples

**View serializable, not conflict serializable.** Take

$$S_1 = r_1(x)\ w_2(x)\ w_1(x)\ w_3(x).$$

| relation | in $S_1$ | in $T_1 T_2 T_3$ |
|---|---|---|
| $r_1(x)$ reads from | $T_0$ | $T_0$ |
| final write of $x$ | $w_3(x)$ | $w_3(x)$ |

The schedules agree, so $S_1$ is view serializable. The first serial order in lexicographic order that works is $T_1 T_2 T_3$; the orders $T_1 T_3 T_2$ and $T_2 T_1 T_3$ fail on the final write and on the read. The conflict graph has the cycle $T_1 \to T_2 \to T_1$ from $r_1(x) < w_2(x)$ and $w_2(x) < w_1(x)$, so $S_1$ is not conflict serializable. The writes $w_2(x)$ and $w_3(x)$ are blind, as Theorem 2 requires.

**A prefix that is not view serializable.** The prefix $r_1(x)\ w_2(x)\ w_1(x)$ of $S_1$ is not view serializable. In $T_1 T_2$ the final write is $w_2(x)$, not $w_1(x)$, and in $T_2 T_1$ the read $r_1(x)$ reads from $T_2$, not from $T_0$. So the class is not closed under prefixes: the last write $w_3(x)$ repairs the schedule after the fact. An online scheduler that must decide on each action when it arrives cannot use this freedom without knowing the future, which is a second reason, next to NP-completeness, why schedulers use conflict serializability.

**Blind writes on two items.** In $w_1(x)\ w_2(x)\ w_2(y)\ w_1(y)$ the final writes are $w_2(x)$ and $w_1(y)$, from different transactions, and each serial order makes one transaction last on both items. It is not view serializable. Adding $w_3(x)\ w_3(y)$ at the end gives $w_1(x)\, w_2(x)\, w_2(y)\, w_1(y)\, w_3(x)\, w_3(y)$, which is view equivalent to $T_1 T_2 T_3$, while its conflict graph still has the cycle $T_1 \to T_2 \to T_1$.

**Non-example: the lost update.** $r_1(x)\ r_2(x)\ w_1(x)\ w_2(x)$ has no blind writes and is not conflict serializable, so by Theorem 2 it is not view serializable. Directly: in $T_1 T_2$ the read $r_2(x)$ reads from $T_1$, and in $T_2 T_1$ the final write is $w_1(x)$.

**How often the gap appears.** In 1500 random schedules of 2 to 4 transactions, each with 1 to 3 random actions on the items $x$ and $y$ (seed 99), 915 schedules are conflict serializable and 972 are view serializable. Each of the 57 schedules in the gap has a blind write.

## Related definitions

- **[Serializability](/serializability/)** is the general idea of equivalence to a serial schedule. Final-state serializability asks only for the same final state under all interpretations; it ignores reads whose values never reach the final state, and it is larger again than view serializability (Weikum and Vossen, Chapter 3).
- **[Conflict serializability](/conflict-serializability/)** is the subclass with a polynomial test by the [conflict graph](/conflict-graph/). Theorems 1 and 2 place view serializability between it and the classes with blind writes.
- **[Thomas write rule](/thomas-write-rule/).** [Timestamp ordering](/timestamp-ordering/) with the Thomas write rule ignores an obsolete write instead of aborting its transaction. The accepted schedules can contain patterns such as $S_1$, which are view serializable but not conflict serializable.
- **Multiversion view serializability.** With several versions per item, a read may see an older version. The equivalence is then defined against a serial single-version schedule, and the test is again NP-complete in general; see [multiversion concurrency control](/multiversion-concurrency-control/).
- **[Opacity](/opacity/)** in transactional memory is closer to view serializability than to conflict serializability, because it speaks about the values that each transaction reads, but it also covers transactions that abort and requires the real-time order.

## References
