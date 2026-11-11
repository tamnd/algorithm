---
tag: QFVDF2
kind: technique
slug: lock-ordering
name: Lock ordering
aliases:
- resource ordering
- lock hierarchy
- lock levels
- ordered locking
area: concurrency/mutual-exclusion
level: core
summary: Give every lock a rank and take locks only in increasing rank. Then no cycle of waits can form, so locks alone can never deadlock.
history:
  year: 1968
  people: [J. W. Havender]
  note: Havender proposed ordered classes of resources for OS/360 in 1968. Lock levels, address order and run-time order validators are later practice.
prereqs: [deadlock-prevention, mutex]
see_also: [deadlock-prevention, mutual-exclusion-deadlock-handling, dining-philosophers-problem, lock-coupling, wait-for-graph, coffman-conditions, reentrant-lock, deadlock]
sources:
  - paper: "J. W. Havender, Avoiding deadlock in multitasking systems, IBM Systems Journal 7(2), 1968, pages 74 to 84"
    locator: the rule that resources are grouped in ordered classes and requested in the order of the classes
  - url: "https://docs.kernel.org/locking/lockdep-design.html"
    title: The Linux kernel documentation, Runtime locking correctness validator
    locator: lock classes, the dependency rules between classes, and the report of a possible circular locking dependency
  - book: isbn:9780321349606
    title: Brian Goetz and others, Java Concurrency in Practice (2006)
    locator: Chapter 10, Avoiding Liveness Hazards, the sections on lock-ordering deadlocks and dynamic lock order deadlocks
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition (2015)
    locator: Chapter 6, Deadlocks, the section on attacking the circular wait condition, with numbered resources
---

Lock ordering is the rule that every lock has a rank and that a process takes a lock only when its rank is above the rank of every lock it already holds. It denies the circular wait condition of [Coffman](/coffman-conditions/), so a set of processes that wait only for locks can never [deadlock](/deadlock/). It is the most used form of [deadlock prevention](/deadlock-prevention/): Havender (1968) proposed ordered classes of resources, kernels write their lock hierarchies down and check them at run time, and library code orders locks on objects by address.

## In plain words

Put a number on every lock. Make a rule for everybody: you may take a lock only if its number is higher than the number of every lock you already hold.

Now think of a group of programs that wait for each other in a circle. Each program in the circle holds a lock and waits for a lock that the next program holds. That next program holds that lock and waits for one with a higher number still. As you go round the circle, the numbers only go up. But a circle comes back to where it started, and a number cannot be higher than itself. So the circle cannot exist.

The rule is simple, but every piece of code in the program must keep it.

## When it applies

The model has asynchronous processes and [mutexes](/mutex/) (or other exclusive locks) in a sequentially consistent memory, with lock and unlock, and perhaps trylock. A process blocks only in a lock operation. Locks are not reentrant unless said otherwise; a [reentrant lock](/reentrant-lock/) that is taken again by its holder does not block and needs no rank check.

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ | process names; $i, j$ are indices |
| $m$ | the number of locks (the shared objects) |
| $\mathit{rank}(\ell)$ | the rank of lock $\ell$, an element of a partial order $\prec$ |

Use it when the set of locks a piece of code may hold together is known when the code is written, or can be computed at run time before the first lock is taken. It gives [deadlock freedom](/deadlock-freedom/) among the locks. It says nothing about [starvation](/starvation/), which depends on the locks themselves, and nothing about waits for other things, such as messages or condition variables.

## The template

```pseudo id=template
ORDERED-ACQUIRE(S)                ▷ S is a set of locks
1  for each ℓ in S, in increasing rank, ties broken by a unique key do
2      lock ℓ

ACQUIRE-LATE(ℓ, H)                ▷ the process holds H and finds that it needs ℓ
3  if rank(ℓ) is above the rank of every lock in H then lock ℓ; return
4  if trylock ℓ succeeds then return
5  release the locks of H whose rank is not below rank(ℓ)
6  take ℓ and those locks again, in increasing rank
7  check again every fact read under the released locks
```

**Why it works.** Let $\prec$ be a strict partial order on the locks, and suppose every process, whenever it waits for a lock $\ell$, holds only locks $h$ with $h \prec \ell$. Then the [wait-for graph](/wait-for-graph/) has no cycle, at any time.

*Proof.* Suppose the graph has a cycle $p_0 \to p_1 \to \cdots \to p_{k-1} \to p_0$. An edge $p_i \to p_{i+1}$ means that $p_i$ waits for a lock $\ell_i$ held by $p_{i+1}$. The process $p_{i+1}$ is itself waiting, for $\ell_{i+1}$, and it holds $\ell_i$, so by the rule $\ell_i \prec \ell_{i+1}$. Going round the cycle gives $\ell_0 \prec \ell_1 \prec \cdots \prec \ell_{k-1} \prec \ell_0$, and by transitivity $\ell_0 \prec \ell_0$, which a strict order forbids. $\square$

Since every deadlock among locks contains a cycle of the wait-for graph, there is no deadlock. Only pairs of locks that some process holds together need to be comparable, which is why a partial order, or a few levels, is enough.

**Late locks** (lines 3 to 7). Sometimes a process learns that it needs a lock only after it has taken others, and the new lock ranks lower. Lines 4 to 6 are the two phase form: try the lock without waiting, which cannot close a cycle since the process does not wait; if that fails, release the higher ranked locks and take everything again in order. The process never waits while holding a lock of higher rank than the one it waits for, so the proof above still applies. Line 7 is needed because other processes may have changed the data between the release and the new acquisition.

## Classic examples

**Two locks in opposite orders.** Process $p$ takes $A$ then $B$, and $q$ takes $B$ then $A$. If each takes its first lock, each waits for the other. With the rank $A \prec B$, $q$ must take $A$ first, and the simulator of the implementation finds no deadlock in any interleaving.

**Address order.** A transfer between two accounts locks both. If one thread transfers from account 0 to account 1 while another transfers from 1 to 0, locking "source, then destination" deadlocks. Locking "lower account number, then higher" does not, whatever the direction. In languages without stable addresses one orders by a unique identifier; Goetz and others describe ordering by an identity hash code, with an extra tie-breaking lock for the rare case of equal hashes. The implementation checks three transfers over all interleavings: the source-first version deadlocks, and the ordered one never does and keeps the total balance.

| version | deadlocks over all interleavings | wait-for graph |
|---|---|---|
| source, then destination | yes | can have a cycle |
| lower number, then higher | none | acyclic in every state |

**A parent and a child.** In a tree, the natural order is parent before child, as in [lock coupling](/lock-coupling/). A process that starts at a child and must then lock the parent goes against the order. The naive version deadlocks with a process going down. With ACQUIRE-LATE, it tries the parent, and on failure releases the child, takes the parent and the child in order, and checks that the child still hangs from that parent. The implementation finds no deadlock in any interleaving.

**Lock levels.** Large programs give each kind of lock a level: for example, a hash table bucket lock at level 1, an entry lock at level 2, a statistics lock at level 3. Code may take a lock only at a level above every lock it holds. A debug build checks the rule at each lock operation, which is a constant time test against the most recent lock held.

**The dining philosophers.** Numbering the forks and having each philosopher pick up the lower numbered fork first is lock ordering; see the [dining philosophers problem](/dining-philosophers-problem/).

**Run-time validation.** The Linux kernel's lock validator (lockdep) records, for each pair of lock *classes*, whether one has been taken while the other was held, and builds a graph of these dependencies. When a new acquisition would add a dependency that closes a cycle, it prints a report of a possible circular locking dependency, even if the run itself did not deadlock. The implementation has a small validator of the same kind on lock instances: in a trace where $p$ takes $A$ then $B$ and, later, $q$ takes $B$ then $A$, it reports the second acquisition, although no deadlock happened. The kernel documentation describes many more details, such as the states in which locks are taken and annotations for nesting locks of the same class.

## Variations

- **A total order.** The simplest rule: one rank for each lock. Easy to state, hard to keep in a large program.
- **A partial order or levels.** Only locks that are held together need an order. A hierarchy of modules gives a natural one: a module may call down into lower modules while it holds its own lock, but not up.
- **Order by a run-time key.** For dynamic sets of locks, sort by address or identifier before locking. Equal keys need a tie-break.
- **Order plus trylock.** For late or unordered locks, try and back off, as in lines 4 to 6. Without care, this can become a [livelock](/livelock/).
- **Checked order.** A validator, such as lockdep, learns the order from runs and reports any cycle. A static checker can do the same from the code.

## Pitfalls

- One exception breaks the proof. A callback that takes a lock while the caller holds another, or a library that takes its own locks, can close a cycle that no single piece of code shows.
- Locks of the same rank need a tie-break. Two objects of one class, locked in different orders by different threads, deadlock as easily as two classes.
- Taking a lower ranked lock after releasing a higher one is fine; taking it while still holding the higher one is not. Release order does not matter for deadlock.
- Ordering covers only waits for locks. A process that holds a lock and waits on a condition variable, a message, or a join can still deadlock; see [monitors](/monitor/) for the nested monitor problem.
- A reader-writer lock taken in shared mode still counts. A reader that holds $A$ in shared mode and waits for $B$ can be part of a cycle with a writer that holds $B$ and waits for $A$.
- After a release-and-retry, the data that was checked under the released locks may have changed; check it again.

## Exercises

1. Prove that it is enough for every process to request locks in increasing order of a strict partial order, as long as each pair of locks held together at some time is comparable.
2. A doubly linked list has one lock per node. One thread walks forward, another walks backward, each using lock coupling. Give a deadlock, and an order that removes it.
3. Write a transfer between accounts that orders the locks by account number and handles a transfer from an account to itself.
4. Show a trace that a lock order validator reports and that can never deadlock, because a third lock, always held around both, serializes the two orders. (Such a lock is sometimes called a gate lock.)

## References
