---
tag: 05N9RH
kind: technique
slug: commitment-ordering
name: Commitment ordering
aliases:
- commit ordering
- commitment order
- CO
area: databases/transactions-and-concurrency
level: advanced
summary: "Commit transactions in the order of their conflicts. Each local schedule is then serializable, and with atomic commitment the global schedule across databases is too."
prereqs: [conflict-serializability, conflict-graph, atomic-commit]
see_also: [two-phase-commit, strict-two-phase-locking, serializability, recoverable-schedule, strict-schedule, external-consistency, optimistic-concurrency-control, timestamp-ordering]
sources:
  - paper: "Yoav Raz, The principle of commitment ordering, or guaranteeing serializability in a heterogeneous environment of multiple autonomous resource managers using atomic commitment, Proceedings of the 18th VLDB Conference, 1992, pages 292 to 312"
    locator: "the definition of commitment ordering, the proof that CO implies serializability, the commitment ordering algorithm with its abort set, and global serializability under atomic commitment"
  - book: isbn:9781558605084
    title: "Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001"
    locator: "Chapter 3, the classes of order-preserving and commit order-preserving conflict serializable schedules, chapter level only"
  - book: isbn:9780201107159
    title: "Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987"
    locator: "Chapter 2 (the serializability theorem and the conflict graph) and Chapter 7 (atomic commitment), chapter level only"
---

*Commitment ordering* (CO), named by Raz in 1992, is the rule that a scheduler commits transactions in the same order as their conflicts: if an operation of $T_i$ comes before a conflicting operation of $T_j$ and both commit, then $T_i$ commits first. The commit order is then a topological order of the [conflict graph](/conflict-graph/), so the schedule is [conflict serializable](/conflict-serializability/), with the commit order as a serial order. The rule needs no information from other sites. If every database of a distributed system enforces it locally and the sites decide commits with [atomic commitment](/atomic-commit/), such as [two-phase commit](/two-phase-commit/), then the global schedule is serializable too. That is the use Raz had in mind: global serializability over autonomous databases that may use different concurrency control methods. [Strict two-phase locking](/strict-two-phase-locking/) in its strong form, where all locks are held to the end, always gives CO schedules.

## In plain words

When two transactions touch the same data, one of them goes first. Commitment ordering asks that the one that went first also commits first. If every pair follows this rule, the order of commits is an order in which the transactions could have run one at a time, so the result is correct. The rule is cheap to enforce, because a database only has to look at its own conflicts and at the order in which it commits. When a transaction is ready to commit, the database aborts the transactions that touched the same data before it and are still undecided, or makes it wait for them. Because the rule uses only the commit order, many databases can each follow it on their own and the whole system stays correct, as long as they agree on which transactions commit.

## When it applies

- A scheduler that already produces conflict serializable schedules, and that can delay or abort a commit. CO adds a check at commit time.
- Several resource managers that take part in one atomic commitment protocol, and that must give a globally serializable result without exchanging conflict information or a global timestamp.
- Systems that want the commit order to be a serial order, so that clients that see commits in real time see a serial order. Every schedule that is CO is order-preserving: a transaction that commits before another starts comes first in the serial order.

## The template

The scheduler keeps the conflict graph of the transactions that are not yet decided, together with the committed ones that still have undecided successors. The holes are the local concurrency control ⟨LOCAL-CC⟩ and the choice ⟨POLICY⟩ between aborting and waiting.

```pseudo id=main
ON-OPERATION(T, op)
L1  run op under ⟨LOCAL-CC⟩                                  ▷ any method, or none
L2  for each earlier operation op' of an undecided or committed T' ≠ T that conflicts with op do add T' → T to G
READY-TO-COMMIT(T)                                           ▷ T has finished and votes, or asks to commit
L3  A ← the undecided transactions with a path to T in G   ▷ the abort set of T
L4  if ⟨POLICY⟩ = abort then abort every transaction in A
L5  else wait until every transaction in A has committed or aborted
L6  commit T (or vote yes on T in atomic commitment)
L7  remove T and the aborted transactions from G when they have no undecided predecessor
```

**Why a schedule of this template is serializable.** A committed transaction never has an undecided predecessor at its commit: line L4 or L5 removed it. So for each arc $T_i \to T_j$ between committed transactions, $T_i$ committed before $T_j$. All arcs go forward in the commit order, the graph of committed transactions is acyclic, and the commit order is a serial order by the [serializability theorem](/serializability-theorem/).

**Why the global schedule is serializable.** Let each site run the template and vote yes on $T$ only at line L6. Suppose the global conflict graph has a cycle $T_1 \to T_2 \to \cdots \to T_k \to T_1$ of committed transactions, where the arc $T_l \to T_{l+1}$ comes from a conflict at some site $S_l$. At $S_l$, $T_{l+1}$ got its yes vote only after $T_l$ was decided there, and $T_l$ is decided at a site only after the global decision on $T_l$. So the global decision on $T_l$ comes before the global decision on $T_{l+1}$, for every $l$, which around the cycle is impossible. The atomic commitment protocol does the work of a global coordinator, and no site needs to know the conflicts of another.

**Classes.** CO schedules are conflict serializable; they are a strict subclass of the order-preserving conflict serializable schedules. $r_1(x)\, w_2(x)\, c_2\, c_1$ is serializable as $T_1 T_2$ and order-preserving, but not CO, because $T_2$ commits first. Rigorous schedules, in which no item that $T_i$ has read or written is written or read in conflict by another transaction until $T_i$ ends, are CO: a conflict $p_i < q_j$ gives $c_i < q_j < c_j$.

## Classic examples

- **Strong strict two-phase locking.** Under [strict two-phase locking](/strict-two-phase-locking/) with read locks also held to the end, a conflicting operation of $T_j$ waits until $T_i$ has ended. The schedule is rigorous, so it is CO, and its commits need no extra check. This is why distributed databases built on locks and [two-phase commit](/two-phase-commit/) are globally serializable.
- **Optimistic and timestamp schedulers.** A method that does not hold locks, such as [optimistic concurrency control](/optimistic-concurrency-control/) or [timestamp ordering](/timestamp-ordering/), can be made CO by the check of lines L3 to L5 at commit. Raz proposed CO for such resource managers in a mixed system.
- **Multidatabases.** In a federation of autonomous databases, each with its own concurrency control and with no global timestamp, CO at each database and a common atomic commitment protocol give global serializability. The participants exchange only commit votes.
- **A small run.** $w_1(x)\, r_2(x)\, w_2(y)$, and $T_2$ is ready first. Its abort set is $\{T_1\}$. With the abort policy, $T_1$ is aborted and $T_2$ commits; but $T_2$ read the value of $T_1$, so the schedule is not [recoverable](/recoverable-schedule/), and a scheduler that must also be recoverable has to abort $T_2$ as well. With the wait policy, $T_2$ waits for $T_1$, which commits; then $T_2$ commits after it.

## Variations

- **Abort or wait.** The abort policy never blocks a commit but may abort much work; the wait policy aborts nothing that would have committed but makes a ready transaction wait for slower ones, and in atomic commitment it delays the vote.
- **Extended CO.** In later work Raz gave a weaker rule that orders only conflicts between global transactions, for systems with local transactions that do not take part in atomic commitment. Local transactions still follow the local concurrency control.
- **Commit order and real time.** Since the commit order is a serial order, a system that also reports commits in that order gives a form of [external consistency](/external-consistency/) for its clients.
- **Strict CO.** Combining CO with a [strict schedule](/strict-schedule/) makes recovery by before-images correct as well.

## Pitfalls

- **CO is not recoverability.** CO speaks only about pairs of transactions that both commit. If $T_2$ reads from $T_1$, $T_2$ commits and $T_1$ then aborts, the schedule is CO but not recoverable. The abort policy of line L4 produces exactly this case, so recoverability must be enforced as well.
- **Abort sets can cascade.** Under the abort policy, aborting the predecessors of a ready transaction can abort a transaction that others have read from, and their aborts follow.
- **Local CO without atomic commitment is not enough.** The global argument uses the fact that a site votes yes only after the predecessors are decided globally. If sites commit on their own, each local schedule is serializable but the serial orders of two sites can disagree.
- **Voting yes too early.** A site that votes yes on $T$ while a local predecessor of $T$ is still undecided breaks the proof, even if it later commits in the right order.

## Exercises

1. Show that a CO schedule is order-preserving: if $T_i$ commits before $T_j$ starts, then $T_i$ is before $T_j$ in some serial order of the schedule.
2. Give a conflict serializable schedule of three transactions that is not CO, and give the commit order that would make it CO.
3. Two sites run strong strict two-phase locking and decide commits by two-phase commit. Show directly, without CO, that the global schedule is serializable.
4. In the template, why must line L3 use paths in $G$ and not only direct predecessors? Give a schedule where only a path reaches $T$.
5. Site 1 runs CO and site 2 runs ordinary strict two-phase locking with read locks released at the end of the transaction's work, before commit. Give a global schedule that is not serializable.

## References
