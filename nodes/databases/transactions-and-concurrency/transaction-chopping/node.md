---
tag: G7FCSD
kind: algorithm
slug: transaction-chopping
name: Transaction chopping
aliases:
- SC-graph chopping
- finest chopping
area: databases/transactions-and-concurrency
level: advanced
summary: "Split known transaction programs into pieces that commit one by one, and keep every execution serializable: a chopping is safe when its graph of sibling and conflict edges has no SC-cycle."
solves: [concurrency-control]
model: word-ram
complexity:
  vars: {n: the number of transactions, m: the number of statements in all transactions}
  time: {worst: "O((m^2 + n^3) α(m))"}
  space: {extra: O(m n)}
properties: {deterministic: true}
history:
  year: 1992
  people: [Dennis Shasha, Eric Simon, Patrick Valduriez]
  note: "SIGMOD 1992. The journal version of 1995 in ACM TODS adds François Llirbat."
prereqs: [conflict-serializability, two-phase-locking, connected-components]
see_also: [conflict-graph, weighted-union-find, robustness-against-weak-isolation, sagas, nested-transactions, open-nested-transactions, serializability, escrow-transactional-method]
sources:
  - paper: doi:10.1145/211414.211427
    title: "Dennis Shasha, François Llirbat, Eric Simon and Patrick Valduriez, Transaction chopping, algorithms and performance studies, ACM Transactions on Database Systems 20(3), 1995, pages 325 to 363"
    locator: "the definitions of a chopping, of rollback-safe choppings and of the chopping graph with S and C edges, the theorem that a rollback-safe chopping with no SC-cycle is correct, and the algorithm for the finest chopping by private choppings"
  - paper: doi:10.1145/130283.130328
    title: "Dennis Shasha, Eric Simon and Patrick Valduriez, Simple rational guidance for chopping up transactions, Proceedings of ACM SIGMOD 1992, pages 298 to 307"
    locator: "the first version of the SC-cycle test and of the finest chopping, chapter level only"
  - paper: doi:10.1145/3561049
    title: "Bas Ketsman, Christoph Koch, Frank Neven and Brecht Vandevoort, Deciding robustness for lower SQL isolation levels, ACM Transactions on Database Systems 47(4), 2022, article 13"
    locator: "the related work, which places chopping as robustness against no isolation and notes that the SC-cycle test runs in polynomial time"
  - paper: "Yang Zhang, Russell Power, Siyuan Zhou, Yair Sovran, Marcos K. Aguilera and Jinyang Li, Transaction chains, achieving serializability with low latency in geo-distributed storage systems, Proceedings of the 24th ACM SOSP, 2013"
    locator: "the static analysis of chains with an SC-graph (Figure 2), chapter level only"
  - paper: doi:10.1007/978-3-662-48653-5_26
    title: "Andrea Cerone, Alexey Gotsman and Hongseok Yang, Transaction chopping for parallel snapshot isolation, Proceedings of DISC 2015, LNCS 9363, pages 388 to 404"
    locator: "the chopping test for parallel snapshot isolation, chapter level only"
---

*Transaction chopping* is a method of Shasha, Simon and Valduriez (1992), developed with Llirbat in a journal paper of 1995, to get more [concurrency](/concurrency-control/) from a workload whose transaction programs are all known in advance. It splits each transaction into *pieces*, and each piece runs and commits as a transaction of its own, so locks are held for a shorter time. A chopping is *correct* if every execution of the pieces is equivalent to a serial execution of the original, whole transactions. The test is on an undirected graph of the pieces with *S* (sibling) edges between pieces of one transaction and *C* (conflict) edges between conflicting pieces of different transactions: if no simple cycle has both kinds of edge (an *SC-cycle*), and every rollback statement is in the first piece, the chopping is correct. The finest correct chopping is unique, and a union-find pass per transaction computes it. The test reasons about [conflict serializability](/conflict-serializability/) at the level of whole transactions; it does not change the concurrency control, which can be [two-phase locking](/two-phase-locking/) or any other serializable method for the pieces.

## In plain words

A long transaction holds its locks until it ends, and the other transactions wait. If we knew that no other transaction can see the difference, we could commit the transaction in several steps and release the locks after each step. Chopping finds where this is safe. It looks at all the programs that can run. Two steps of one transaction may be split apart only if no chain of conflicting transactions joins them: if one step touches data that some group of transactions uses, and another step touches data of the same group, then a member of the group can run between the two steps, see half of the work, and break serializability. The method also keeps every possible rollback in the first step, because a later step cannot undo the steps that already committed.

## The problem

**Input.** A set of transaction programs $T_1, \ldots, T_n$, the complete workload. Each program is a sequence of *statements*: reads $r(x)$, writes $w(x)$ and *rollback statements*, the places where the program may decide to abort. Two accesses *conflict* if they touch the same item and at least one is a write.

**Chopping.** A chopping of $T_i$ cuts its sequence into pieces $p_{i,1}, \ldots, p_{i,k}$. On this page each piece is a run of consecutive statements, and the pieces of $T_i$ run in program order. A chopping of the workload is a chopping of each $T_i$.

**Execution model.** Each piece runs as a transaction under a concurrency control that makes the execution of the pieces serializable. A piece that the system aborts (for example as the victim of a deadlock) is restarted until it commits. Only a rollback statement can make the whole $T_i$ give up.

**Correctness.** A chopping is correct if every execution of the pieces allowed by the model is [conflict equivalent](/conflict-serializability/) to a serial execution of the whole transactions $T_1, \ldots, T_n$.

**The test of Shasha et al.**

- A chopping is *rollback-safe* if, for every $T_i$ with rollback statements, all of them are in its first piece.
- The *chopping graph* has a node for each piece. An *S edge* joins two pieces of the same transaction. A *C edge* joins two pieces of different transactions that contain conflicting accesses.
- An *SC-cycle* is a simple cycle of the chopping graph with at least one S edge and at least one C edge.

**Theorem (Shasha et al.).** A rollback-safe chopping with no SC-cycle is correct.

The goal is the *finest* such chopping: the one with the most pieces.

## The algorithm

The S edges of one transaction form a clique, so the other transactions join their own pieces anyway. For this reason the finest chopping of $T_i$ depends only on the other transactions as wholes, not on how they are chopped. FINEST-CHOPPING computes this *private chopping* of each $T_i$ and returns the union. The positions of $T_i$ are $1, \ldots, |T_i|$.

```pseudo id=main
FINEST-CHOPPING(T_1, ..., T_n)
L1  for i ← 1 to n do
L2      U ← a union-find over the transactions T_j with j ≠ i
L3      for each pair j, k ≠ i such that T_j and T_k have conflicting accesses do UNION(U, j, k)
L4      P ← a union-find over the positions of T_i; owner ← an empty map
L5      for p ← 1 to |T_i| do
L6          for each j ≠ i such that T_j has an access in conflict with statement p of T_i do
L7              r ← FIND(U, j); if r ∈ owner then UNION(P, owner[r], p) else owner[r] ← p
L8      end ← the position of the last rollback statement of T_i, or 1 if there is none
L9      for p ← 1 to |T_i| do end ← max(end, the last position in the class of p in P)
L10         if end = p then cut T_i after position p
L11 return the cuts of T_1, ..., T_n
```

Lines L2 and L3 find the connected components of the conflict graph of the other transactions: two transactions are in one component if a chain of conflicts joins them. Lines L4 to L7 put two statements of $T_i$ into one class when they conflict with the same component; `owner` remembers the first statement that touched each component. Lines L8 to L10 turn the classes into contiguous pieces. A piece must contain every class that it touches from its first to its last position, and the first piece must reach the last rollback statement. The sweep keeps in `end` the furthest position that the current piece must reach, and cuts as soon as the sweep arrives there.

Each component of the other transactions ends up inside one piece of $T_i$. This is exactly the condition for no SC-cycle through $T_i$: an SC-cycle that uses an S edge of $T_i$ must leave $T_i$ through a C edge, walk inside one component of the others, and come back through a C edge into a different piece of $T_i$. The same observation gives the test HAS-SC-CYCLE of the implementation, which runs in the same time and needs no cycle search.

## Example

Accounts $a$ and $b$. The workload has a transfer $T_1 = r(a)\, w(a)\, r(b)\, w(b)$, a deposit $T_2 = r(b)\, w(b)$ on $b$, and a deposit $T_3 = r(a)\, w(a)$ on $a$. For $T_1$, the others are $T_2$ and $T_3$. They do not conflict, so lines L2 and L3 leave two components, $\{T_2\}$ and $\{T_3\}$.

| step | statement $p$ of $T_1$ | conflicts with | owner | classes of $P$ | end | cut |
|---|---|---|---|---|---|---|
| L5 to L7 | 1: $r(a)$ | $T_3$ | $\{T_3\} \mapsto 1$ | $\{1\}, \{2\}, \{3\}, \{4\}$ | | |
| L5 to L7 | 2: $w(a)$ | $T_3$ | | $\{1, 2\}, \{3\}, \{4\}$ | | |
| L5 to L7 | 3: $r(b)$ | $T_2$ | $\{T_2\} \mapsto 3$ | $\{1, 2\}, \{3\}, \{4\}$ | | |
| L5 to L7 | 4: $w(b)$ | $T_2$ | | $\{1, 2\}, \{3, 4\}$ | | |
| L8 | | | | | 1 | |
| L9, L10 | $p = 1$ | | | | 2 | |
| L9, L10 | $p = 2$ | | | | 2 | after 2 |
| L9, L10 | $p = 3$ | | | | 4 | |
| L9, L10 | $p = 4$ | | | | 4 | after 4 |

The transfer becomes two pieces, $r(a)\, w(a)$ and $r(b)\, w(b)$. A deposit on $a$ can run between them and sees the debit, which is fine: in the equivalent serial order it runs after $T_1$. Both deposits stay whole, because each of their two statements conflicts with the transfer, which is one component for them.

Now add an audit $T_4 = r(a)\, r(b)$. It conflicts with $T_2$ and with $T_3$, so for $T_1$ the others form one component $\{T_2, T_3, T_4\}$, and every statement of $T_1$ lands in one class: the transfer cannot be chopped. The old chopping now has the SC-cycle $p_{1,1} \xrightarrow{C} T_4 \xrightarrow{C} p_{1,2} \xrightarrow{S} p_{1,1}$, and the execution $r_1(a)\, w_1(a)\, r_4(a)\, r_4(b)\, c_4\, r_1(b)\, w_1(b)\, c_1$ shows why: the audit sees $a$ debited and $b$ not yet credited, and its conflict graph has the cycle $T_1 \to T_4 \to T_1$.

Rollbacks change the picture too. If the transfer checks the balance after $r(a)$ and may roll back there, the first piece is $r(a)$, rollback, $w(a)$, which is the same cut. If it checks at the very end, line L8 sets the end of the first piece to the last position, and the transfer is one piece.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It has three parts. First, the theorem of Shasha et al.: suppose an execution of a rollback-safe chopping with no SC-cycle had a cycle among the whole transactions; contract each transaction to its pieces and follow the cycle in the chopping graph; either the walk gives an SC-cycle, or it stays on C edges between single pieces, which is a cycle in the conflict graph of the pieces and contradicts that the pieces ran serializably. Second, the component lemma: there is an SC-cycle if and only if two different pieces of one transaction conflict with the same component of the other transactions. Third, the output of FINEST-CHOPPING passes the test, and a contiguous chopping of $T_i$ passes it if and only if every one of its cuts is a cut of the output. So the output is the unique finest correct chopping in the sense of the test.

## Complexity

Let $n$ be the number of transactions and $m$ the number of statements. A first pass compares every pair of statements and records, for each statement, the set of transactions it conflicts with, and for each transaction the transactions it conflicts with: $O(m^2)$ time and $O(m n)$ space. For each $i$, lines L2 and L3 make at most $n^2$ calls to UNION, and lines L5 to L7 make at most $|T_i| \cdot n$ calls, so the whole loop makes $O(n^3 + m n)$ union-find calls. With union by size and path compression, each call costs $O(\alpha(m))$ amortized, where $\alpha$ is the inverse Ackermann function. The sweep of lines L8 to L10 is linear. The total is $O((m^2 + n^3)\, \alpha(m))$ time. With an index from items to accesses, the first pass costs time proportional to the number of conflicting pairs.

## Properties

- **Unique result.** The finest correct chopping is unique, so the output does not depend on the order in which the loops visit transactions and statements.
- **Compositional.** The union of the private choppings, each computed against the other transactions whole, is correct. A transaction can be chopped without knowing how the others are chopped.
- **Monotone.** Merging two adjacent pieces of a correct chopping keeps it correct. Cutting a piece of an incorrect chopping keeps it incorrect, since the SC-cycle stays.
- **Static.** The test needs the whole workload. A new program that conflicts with two components joins them and can forbid cuts that were safe before.
- **The simplest SC-cycle always hurts.** If two pieces $p$ and $p'$ of $T_i$ both conflict with an unchopped $T_j$, the execution $p, T_j, p'$ gives the conflict cycle $T_i \to T_j \to T_i$.

## Variants and improvements

- **Robustness.** [Robustness against weak isolation](/robustness-against-weak-isolation/) asks the general question: do all executions of a fixed set of programs at a weak level stay serializable? Ketsman et al. place chopping as the case of no isolation at all between the pieces of one transaction.
- **Chains in geo-replicated stores.** Lynx (Zhang et al., 2013) chops transactions into *chains* of hops, one per server, and runs the SC-cycle test on the static set of chains, so that the first hop can return to the client early.
- **Other consistency models.** Cerone, Gotsman and Yang (2015) give a chopping test for parallel snapshot isolation, where the pieces run at that level instead of serializable.
- **Semantic methods.** [Sagas](/sagas/) split a transaction with no test at all and give up isolation; [escrow](/escrow-transactional-method/) and [open nested transactions](/open-nested-transactions/) use the meaning of the operations to allow more interleavings than conflicts permit.

## When to use it

Use chopping when the workload is fixed and known, for example a set of stored procedures in an OLTP system, when long transactions hold hot locks, and when the system can retry a piece until it commits. It does not help a workload with ad hoc queries, because a single new program can join the components. It is also not a fit when the application needs a rollback late in the transaction, because rollback safety then forces the whole transaction into one piece.

## Pitfalls

- **Single transactions in place of components.** Line L7 looks up the component of $T_j$. A version that keys `owner` by $j$ itself merges two statements only when they conflict with the same transaction, and misses longer SC-cycles such as $p \xrightarrow{C} T_2 \xrightarrow{C} T_3 \xrightarrow{C} p' \xrightarrow{S} p$. Lines L2 and L3 must run first.
- **Forgetting the rollback statements.** A cut before a rollback statement lets a later piece abort after the earlier pieces have committed and released their locks. Line L8 must start the sweep at the last rollback position, not at 1.
- **Pieces that are not contiguous.** The classes of $P$ after line L7 may interleave, as in classes $\{1, 3\}$ and $\{2\}$. If pieces must be runs of consecutive statements, cutting at class boundaries alone is wrong; lines L9 and L10 must extend the piece to the last position of every class that it touches.
- **Treating the test as dynamic.** The test assumes every program in the workload. Adding a report query later without running the test again can make a correct chopping incorrect, as the audit of the example shows.

## Implementations

## History

Dennis Shasha, Eric Simon and Patrick Valduriez presented the SC-cycle test and the finest chopping at SIGMOD 1992 as "simple rational guidance for chopping up transactions". The journal version with François Llirbat in ACM TODS 1995 extends the theory and reports performance studies. Lynx at SOSP 2013 brought the SC-graph analysis to geo-distributed storage, and later work by Cerone, Gotsman and Yang carried the test to weaker consistency models.

## References
