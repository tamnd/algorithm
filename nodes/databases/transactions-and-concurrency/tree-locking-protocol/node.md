---
tag: AV253P
kind: algorithm
slug: tree-locking-protocol
name: Tree locking protocol
aliases:
- Silberschatz-Kedem tree protocol
area: databases/transactions-and-concurrency
level: advanced
summary: A protocol for items arranged in a tree that locks a node only while holding its parent and allows early release, yet stays serializable.
solves: [concurrency-control]
model: word-ram
complexity:
  vars: {m: the number of accesses of one transaction, h: the height of the tree, k: the number of active transactions}
  time: {per-request: "O(1) expected", per-transaction: "O(m h) expected"}
  space: {extra: "O(k m h)"}
properties: {deterministic: true, online: true}
prereqs: [two-phase-locking, conflict-serializability, rooted-tree]
see_also: [two-phase-locking-theorem, lock-coupling, blink-tree, b-tree, multiple-granularity-locking, deadlock-prevention, wait-for-graph, recoverable-schedule]
sources:
  - paper: doi:10.1145/322169.322176
    title: Abraham Silberschatz and Zvi Kedem, Consistency in hierarchical database systems, Journal of the ACM 27(1), 1980, pages 72 to 80
    locator: the tree protocol with exclusive locks, and the proof that its schedules are serializable and free of deadlocks
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 3 (tree locking, as a locking protocol that is not two-phase)
---

The tree locking protocol, due to Silberschatz and Kedem (1980), is a locking protocol for data items that form a rooted tree, such as the nodes of an index. A transaction may put its first lock on any node. After that, it may lock a node only while it holds the lock on the parent of that node, and it may never lock a node again after it unlocked it. It may unlock any node at any time. These rules alone make every schedule [conflict serializable](/conflict-serializability/) and free of deadlocks, although a transaction can unlock a node and lock another one later, which [two-phase locking](/two-phase-locking/) forbids. The price is that a transaction must lock every node on the path to the items that it wants, and that the schedules need not be recoverable.

## In plain words

Think of a cave system where the tunnels branch like a tree, and only one person fits in a section at a time. You may start in any section. To go deeper, you must still stand in the section you came from while you step into the next one; then you may leave the one behind you. You may not go back to a section you left.

Two people who meet in the tunnels always meet in the same order: whoever went first through the highest shared section is first everywhere below it. Nobody can pass, so the visits are as if one person went through after the other. And nobody gets stuck in a circle of people who each wait for the next one.

## The problem

The input is a set of transactions that read and write the nodes of a rooted tree, given by the parent of each node. The actions of the transactions arrive interleaved, and a scheduler with locks must make the output schedule conflict serializable. With [two-phase locking](/two-phase-locking/), a transaction that walks down the tree must keep every lock until it has all of them, so it keeps the root locked for its whole growing phase, and nobody else can enter the tree. Two-phase locking can also deadlock. The goal is a protocol that uses the shape of the tree to release locks early, without losing serializability.

In the model here, every lock is exclusive: a transaction locks a node before it reads or writes it, whatever the action. A transaction that waits keeps its locks and takes no other step.

## The algorithm

```pseudo id=main
LOCK(T, x)
L1  if T has locked x before then reject                ▷ no lock again
L2  if T holds some lock and does not hold parent(x) then reject
L3  if another transaction holds x then T waits; try again later
L4  grant the lock on x to T; record x as locked by T

UNLOCK(T, x)
L5  T must hold x; release it                            ▷ at any time

PLAN(T, accesses)                ▷ one way to follow the rules
L6  t ← the lowest common ancestor of the accessed nodes; lock t first
L7  before each access to v, lock the nodes on the path from t to v that are not locked yet, from the top down
L8  after each lock and each access, unlock each held node that has no later access
       and no child on a planned path that is still to be locked
```

Lines L1 to L5 are the protocol. A transaction reads or writes a node only while it holds the lock on it. Lines L6 to L8 are a planner of this page that turns a list of accesses into lock and unlock steps that follow the rules and release each lock as early as possible. Other plans are legal too, for example one that keeps every lock until the commit.

## Example

The tree has the root $a$ with children $b$ and $c$; $b$ has the children $d$ and $e$, and $c$ has $f$ and $g$. Let $T_1 = w_1(d)\, w_1(e)\, c_1$ and $T_2 = r_2(b)\, r_2(d)\, c_2$. Both start at $b$, the lowest common ancestor of the nodes they use.

| step | event | locks held after the step |
|---|---|---|
| 1 | $T_1$ locks $b$, then $d$ | 1: $b$, $d$ |
| 2 | $w_1(d)$; $T_1$ unlocks $d$, which it needs no more | 1: $b$ |
| 3 | $T_2$ asks for $b$ and waits | 1: $b$ |
| 4 | $T_1$ locks $e$, then unlocks $b$: it has no access to $b$, and both its children on the paths are locked | 1: $e$ |
| 5 | $T_2$ locks $b$; $r_2(b)$; it locks $d$ and unlocks $b$ | 1: $e$; 2: $d$ |
| 6 | $r_2(d)$; $T_2$ unlocks $d$; $c_2$ | 1: $e$ |
| 7 | $w_1(e)$; $T_1$ unlocks $e$; $c_1$ | |

The output is $w_1(d)\, r_2(b)\, r_2(d)\, c_2\, w_1(e)\, c_1$. It is conflict equivalent to $T_1\, T_2$. $T_1$ is not two-phase, since it unlocked $d$ before it locked $e$. The schedule is also not [recoverable](/recoverable-schedule/): $T_2$ read $d$ from $T_1$ and committed first.

A transaction $T_3 = r_3(f)\, c_3$ would lock only $f$, its first lock, and run at any moment, since no other transaction uses $c$, $f$ or $g$. If $T_2$ were $w_2(e)\, w_2(d)\, c_2$ instead, the opposite order of $T_1$, then two-phase locking could deadlock on $d$ and $e$. Here both transactions must lock $b$ first, and the second one waits there without any lock.

## Correctness

The proofs are on [the proof page](proofs/correctness.md). Let $T \mathrel{\rho} U$ mean that $T$ and $U$ lock a common node and $T$ locks it first.

- **The lock order has no cycle.** The proof is by induction on the size of the tree. The transactions that lock the root take it one after the other, and each of them reaches the subtree of a child $c$ through $c$, while it holds the root. So their order on $c$, and on all of the subtree of $c$, is their order on the root. A transaction that does not lock the root stays inside one subtree, where the induction applies.
- **Serializability.** Every access is made under an exclusive lock, so every edge of the conflict graph is an edge of $\rho$. The conflict graph has no cycle, and by the [serializability theorem](/serializability-theorem/) the schedule is conflict serializable.
- **No deadlock.** If $T_1, \dots, T_k$ waited in a cycle, each $T_i$ for a node $x_i$ that $T_{i+1}$ holds, then the history can be extended legally so that each $T_i$ gets $x_i$ after $T_{i+1}$. This gives a cycle of $\rho$, which cannot be.

## Complexity

- **Per request.** A lock or unlock is $O(1)$ expected time with hash tables: the test for the parent, the test for the holder, and the set of nodes that the transaction has locked.
- **Per transaction.** A transaction with $m$ accesses in a tree of height $h$ locks at most the nodes of $m$ paths, so $O(m h)$ locks, each $O(1)$ expected. The planner of the code is simple and takes more time than this, up to quadratic in the number of locks.
- **Space.** The lock table has one holder per node, and each transaction records the nodes it locked, so $O(k m h)$ for $k$ active transactions.
- **Concurrency.** A transaction holds each node only while it needs it or while it still has to pass through it. The top of the tree is free again as soon as the transaction has gone below it, so many transactions can work in the tree at once, one behind the other.

## Properties

- **Output class.** Conflict serializable, but not always recoverable, since locks can be released before the commit.
- **Deadlock free.** No wait-for graph and no deadlock victims are needed.
- **Not comparable with two-phase locking.** A transaction can lock after it unlocked. On the tree of the example, $w_1(d)\, w_2(d)\, w_3(e)\, w_1(e)$ comes from the tree protocol ($T_1$ holds $b$, and $T_2$ and $T_3$ start at $d$ and $e$), but not from two-phase locking, since $T_1$ would have to hold $e$ from before $w_2(d)$ until $w_1(e)$. In the other direction, $w_1(d)\, w_2(b)\, w_1(b)$ comes from two-phase locking, but not from the tree protocol, since $T_1$ must lock $b$ first and cannot lock it again.
- **Needs the tree.** It works only when every transaction reaches the items through the tree, along parent links.

## Variants and improvements

- **Locks to the commit.** A transaction may keep all its locks until it commits. This is still legal, and the schedules become [strict](/strict-schedule/), but the early release, the main gain of the protocol, is lost.
- **Lock coupling in B-trees.** [Lock coupling](/lock-coupling/), or crabbing, walks from the root of a [B-tree](/b-tree/) to a leaf, and locks a child before it releases the parent. It uses the same rule for short page latches, not for transaction locks. The [B-link tree](/blink-tree/) adds right links so that a reader can hold one latch at a time.
- **Shared locks and graphs.** Kedem and Silberschatz extended the protocol to directed acyclic graphs and to shared locks; these versions need more rules than the parent rule, as the pitfall below shows.
- **Locks of several sizes.** [Multiple granularity locking](/multiple-granularity-locking/) also uses a tree, but there a lock on a node covers the subtree, and it is used together with two-phase locking.

## When to use it

Use it when the data is reached through a tree and transactions use small parts of it, so that early release of the upper nodes gives real concurrency: index structures, hierarchies of objects, and file systems. It also fits systems that cannot afford deadlock detection. Do not use it when transactions reach items directly, without the path from a common ancestor, or when they must abort often, since dirty reads then cause cascading aborts.

## Pitfalls

- **Shared locks break the plain rules.** If two transactions may hold a node at the same time in a shared mode and both go down from it, the order on the node no longer fixes the order below it. With $a$ above $b$ and $c$: $T_1$ and $T_2$ both hold $a$ shared, $T_1$ writes $b$ before $T_2$ does, and $T_2$ writes $c$ before $T_1$ does. Both follow the parent rule, and the schedule is not serializable.
- **Recoverability.** A transaction that reads a node after an early unlock reads uncommitted data. Hold the locks on written nodes until the commit, or delay the commit of the reader until the writer commits.
- **Choosing the first node.** A transaction must start at a node above all the items that it will use. A transaction that discovers later that it needs an item outside the subtree of its first lock cannot get it, and must restart.
- **No lock again.** A transaction that unlocks a node too early cannot come back to it, so the plan must know which nodes it will use again.

## Implementations

## History

Bayer and Schkolnick (1977) studied lock coupling for concurrent operations on B-trees, where a process keeps the lock on a node until it holds the lock on the child. Silberschatz and Kedem (1980) stated the tree protocol for transactions on hierarchical databases and proved that it gives serializable schedules without deadlocks, although it is not two-phase. Kedem and Silberschatz then extended it to directed acyclic graphs and to shared locks, and Bernstein, Hadzilacos and Goodman (1987) present tree locking as the standard example of a protocol that is correct without the two-phase rule.

## References
