---
tag: R9GFHC
kind: technique
slug: lock-coupling
name: Lock coupling
aliases: [hand-over-hand locking, crabbing]
area: concurrency/mutual-exclusion
level: core
summary: Walk a linked structure with one lock per node, and take the lock of the next node before you release the lock of the current one. Locks are taken in path order.
history:
  year: 1977
  people: [Rudolf Bayer, Mario Schkolnick]
  note: Bayer and Schkolnick (1977) used lock coupling to let many processes search and update a B-tree at once, and released the locks above a node once it could not split.
prereqs: [mutex, linked-list]
see_also: [b-tree, b-plus-tree, linked-list, ordered-set, two-phase-locking, lock-ordering, harris-linked-list, linearizability]
sources:
  - paper: doi:10.1007/BF00263762
    title: Rudolf Bayer and Mario Schkolnick, Concurrency of operations on B-trees, Acta Informatica 9(1), 1977, pages 1-21
    locator: the lock coupling protocol for readers, the safe node rule for updaters, and the three solutions for updaters
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 9, Linked Lists, the Role of Locking, Section 9.5, Fine-Grained Synchronization (hand-over-hand locking of a sorted list)
  - paper: doi:10.1145/319628.319663
    title: Philip L. Lehman and S. Bing Yao, Efficient locking for concurrent operations on B-trees, ACM Transactions on Database Systems 6(4), 1981, pages 650-670
    locator: the B-link tree, where a link to the right sibling lets a search hold no lock and an insert hold few
  - paper: "Abraham Silberschatz and Zvi Kedem, Consistency in hierarchical database systems, Journal of the ACM 27(1), 1980"
    locator: the tree locking protocol, a locking rule for trees that is not two-phase and still gives serializable transactions
  - paper: "Galen C. Hunt, Maged M. Michael, Srinivasan Parthasarathy and Michael L. Scott, An efficient algorithm for concurrent priority queue heaps, Information Processing Letters 60(3), 1996"
    locator: a heap with one lock per node, where insertions climb and deletions descend with locks taken in a fixed order
  - paper: "Steve Heller, Maurice Herlihy, Victor Luchangco, Mark Moir, William N. Scherer III and Nir Shavit, A lazy concurrent list-based set algorithm, OPODIS 2005"
    locator: the lazy list, which traverses with no locks and locks only the two nodes it changes
---

Lock coupling, also called hand-over-hand locking or crabbing, is a way to let many processes work on a linked structure at once. Each node has its own lock. A process that walks down the structure takes the lock of the next node *before* it releases the lock of the node it holds, so at every moment it holds at least one lock on its path. Two processes can then work in different parts of a list or a tree at the same time, and no process ever follows a link that another process is changing. Bayer and Schkolnick (1977) introduced it for B-trees.

## In plain words

Think of a person who crosses a river on stepping stones while others cross too, and a stone may be moved. The rule is: do not lift your back foot until your front foot stands firmly on the next stone. Then you never stand on nothing, and nobody can pull away the stone in front of you while you step onto it.

In a list, each item has a lock. You hold the lock of the item where you are, take the lock of the next item, and only then let go of the first one. A process that changes the list holds the locks of the items around the change, so the walkers behind it wait, and the walkers ahead of it are not disturbed.

## When it applies

- The data is a linked structure, a list or a tree, that every operation enters at the same place (the head or the root) and walks in one direction.
- Each operation changes only a small part of the structure, near the end of its path: the links next to one node in a list, or one leaf and maybe a few of its ancestors in a tree.
- Each node can carry a lock, and the order in which the paths visit the nodes is the same for all processes, so that locks are always taken in one global order.
- A single lock for the whole structure would be a bottleneck, but the cost of one lock operation per visited node is acceptable.

## The template

**Model.** A sorted singly linked list stores a set of keys. It has two sentinel nodes $H$ with key $-\infty$ and $T$ with key $+\infty$. Each node $x$ has an immutable key $key(x)$, a pointer $next(x)$ and a lock. `LOCATE(k)` returns two adjacent nodes $pred$ and $curr$ with $key(pred) < k \le key(curr)$, both locked by the caller:

```pseudo id=main
LOCATE(k)
L1  lock(H)
L2  pred ← H; curr ← next(H)
L3  lock(curr)
L4  while key(curr) < k do
L5      unlock(pred)
L6      pred ← curr; curr ← next(pred)
L7      lock(curr)
    return (pred, curr)
```

The operations of the set use `LOCATE` and then change the links next to $pred$ while they hold both locks:

```pseudo
CONTAINS(k)
    (pred, curr) ← LOCATE(k)
    r ← (key(curr) = k)
    unlock(curr); unlock(pred); return r

ADD(k)
    (pred, curr) ← LOCATE(k)
    if key(curr) = k then r ← false
    else
        x ← a new node with key k and next(x) = curr
        next(pred) ← x
        r ← true
    unlock(curr); unlock(pred); return r

REMOVE(k)
    (pred, curr) ← LOCATE(k)
    if key(curr) ≠ k then r ← false
    else
        next(pred) ← next(curr)
        r ← true
    unlock(curr); unlock(pred); return r
```

The abstract set is the set of keys of the nodes that can be reached from $H$, without the two sentinels. A node is never put back into the list after it has been removed; a new node is made for each add.

**Lemma 1 (a held lock pins a node).** The pointer $next(x)$ is written only by a process that holds the lock of $x$. A node $x$ becomes unreachable only by a remove that holds the locks of $x$ and of its predecessor. So if process $p$ holds the lock of a reachable node $x$, then until $p$ releases it, no other process changes $next(x)$, and $x$ stays reachable.

*Proof.* The writes of $next$ are the write of $next(pred)$ in `ADD` and `REMOVE`, both made while the caller holds $pred$, and the write of $next(x)$ for a new node $x$ that no other process can see yet. A remove makes only $curr$ unreachable, and it holds the lock of $curr$. An add makes no node unreachable. So while $p$ holds the lock of $x$, $next(x)$ is fixed and $x$ is not removed; a change before $x$ either inserts a node or bypasses a node other than $x$, and keeps a path from $H$ to $x$. $\square$

**Lemma 2 (the list stays sorted).** At every time, the reachable nodes form a chain $H = x_0, x_1, \ldots, x_m = T$ with $next(x_i) = x_{i + 1}$ and $key(x_0) < key(x_1) < \cdots < key(x_m)$.

**Lemma 3 (the locate invariant).** Each time process $p$ finishes L3 or L7, it holds the locks of $pred$ and $curr$, $pred$ is reachable, $next(pred) = curr$, and $key(pred) < k$. When `LOCATE(k)` returns, also $k \le key(curr)$.

*Proof of Lemmas 2 and 3, by induction on the steps.* At the start the list is $H, T$, sorted. *Lemma 3 at L3.* $p$ took the lock of $H$ at L1, and $H$ is always reachable, since it is never removed: a remove of $H$ would need $key(curr) = k$ with $curr = H$, but $curr$ is never $H$. $p$ read $curr = next(H)$ at L2 while it held $H$, so by Lemma 1 $next(H) = curr$ still holds when L3 succeeds, and $key(H) = -\infty < k$. *Lemma 3 at L7.* Before L5, $p$ held $pred$ and $curr$ with $next(pred) = curr$, and $key(curr) < k$ by the test at L4. At L5 it keeps the lock of $curr$, which is reachable because $pred$ is reachable and points to it. So by Lemma 1, the node $curr$, now called $pred$, stays reachable and its $next$ field stays fixed while $p$ reads it at L6 and waits at L7. *Return.* The loop stops when $key(curr) \ge k$. *Lemma 2.* An add writes $next(pred) \leftarrow x$ with $next(x) = curr$, while it holds $pred$ and $curr$, so by Lemma 3 these are adjacent in the chain, and $key(pred) < k < key(curr)$ because $key(curr) \ne k$. The chain stays sorted. A remove writes $next(pred) \leftarrow next(curr)$ while it holds both locks, so $next(curr)$ is the node after $curr$ in the chain (Lemma 1), and dropping $curr$ keeps the chain sorted. $\square$

**Theorem (safety).** Every execution of `CONTAINS`, `ADD` and `REMOVE` is linearizable with respect to a sequential set.

*Proof.* Choose the linearization point of a successful add at its write $next(pred) \leftarrow x$, of a successful remove at its write $next(pred) \leftarrow next(curr)$, and of every other call at the moment that its `LOCATE` returns. At each of these points the caller holds $pred$ and $curr$, which are adjacent in the sorted chain with $key(pred) < k \le key(curr)$ (Lemmas 2 and 3). By sortedness, $k$ is in the set exactly when $key(curr) = k$. So a contains returns the right answer, a failed add sees $k$ in the set, and a failed remove sees $k$ not in the set. A successful add changes the set from $S$ to $S \cup \{k\}$ with $k \notin S$, and a successful remove changes it from $S$ to $S \setminus \{k\}$ with $k \in S$, in one step. No other step changes the set of reachable keys. $\square$

**A removed node is never seen again.** A process can reach the node $curr$ only by reading $next(pred)$ while it holds the lock of $pred$, and a remover holds that lock until after $next(pred)$ no longer points to $curr$. A process that is ahead of the remover has already released $curr$. So after the remove, no other process has a pointer to $curr$, and it may be freed at once. Lists that traverse without locks, such as the lazy list and the [Harris list](/harris-linked-list/), cannot do this and need a reclamation scheme such as [hazard pointers](/hazard-pointers/).

**Theorem (deadlock freedom by ordered acquisition).** If every node lock is deadlock free, then some call always finishes: no set of processes waits forever.

*Proof.* A process waits only at L1, L3 and L7, and at L3 and L7 it waits for the lock of $curr$ while it holds only the lock of $pred$, with $key(pred) < key(curr)$. At L1 it holds no lock. The unlock steps after `LOCATE` do not wait. So each waiting process holds only locks on keys smaller than the key of the lock it waits for. If $p_1$ waits for a lock held by $p_2$, then the key that $p_2$ waits for, if it waits, is larger than every key that $p_2$ holds, which includes the key that $p_1$ waits for. Following the chain of waits, the keys grow strictly, so the chain cannot return to $p_1$: the waits-for relation has no cycle. A chain of waits ends at a process that does not wait, which runs and releases its locks after a finite number of its own steps. Hence some waiting process gets its lock. This is the [lock ordering](/lock-ordering/) rule for the order of the keys. $\square$

**No overtaking.** A process $q$ behind $p$ on the list must take the lock of a node that $p$ holds before it can pass $p$, so it cannot pass. So at most $n - 1$ processes can add nodes ahead of $p$ during one call, each at most once before it has to start again at $H$, and every traversal takes a finite number of steps. With starvation-free node locks, every call finishes.

The test file checks all this with the explorer of this area: six scenarios with two or three processes, each mixing `ADD`, `REMOVE` and `CONTAINS`, all have only linearizable histories against the sequential set and no state that waits forever. With the coupling turned off (release $pred$ before taking $curr$), two adds at the same place lose one of the nodes, and two removes of neighboring keys put a removed node back into the list.

## Classic examples

**Sorted list set.** The template above is the fine-grained list of Herlihy and Shavit, an [ordered set](/ordered-set/) on a [linked list](/linked-list/). Its throughput beats a list with one lock when the operations spread over the list, but every call locks every node on its path, so it is slow for long lists.

**B-trees and B+ trees.** Bayer and Schkolnick (1977) apply coupling to [B-trees](/b-tree/) and [B+ trees](/b-plus-tree/). A search couples shared locks from the root to a leaf. An insert couples exclusive locks, and when it reaches a node that is *safe*, one that will not split because it has room for one more key, it releases all the locks above it, since a split cannot climb past a safe node. A delete does the same with nodes that will not underflow. Their second solution descends optimistically with shared locks, takes an exclusive lock on the leaf, and starts again with exclusive coupling only if the leaf is not safe. This is still the base of the locking in many database index implementations.

**B-link trees.** Lehman and Yao (1981) add to each node of a B+ tree a link to its right sibling. A search then needs no lock at all, and an insert holds at most a few locks at a time, because a process that reaches a node after a split can follow the link to the right. See [B-link tree](/blink-tree/), which builds on the ideas of this page.

**Concurrent heaps.** In the heap of Hunt, Michael, Parthasarathy and Scott (1996), each node of an array heap has a lock. A deletion moves down from the root and takes locks in the same top-down order. An insertion bubbles up from a leaf, against that order, so it locks a parent and a child with care to avoid deadlock. See [fine-grained concurrent heap](/fine-grained-concurrent-heap/).

**Tree locking in databases.** Silberschatz and Kedem (1980) showed that transactions on data arranged in a tree may follow the *tree protocol*: lock the first node anywhere, then lock a node only while holding its parent, and never lock a node again after releasing it. This is not [two-phase locking](/two-phase-locking/), because a transaction releases locks before it takes all of them, yet every schedule is serializable and free of deadlock.

## Variations

- **Shared and exclusive modes.** Readers couple shared locks of a [readers-writer lock](/readers-writer-lock/), and writers couple exclusive locks, so that searches can pass each other.
- **Early release in trees.** Release all locks above a safe node, as in B-trees, so that a long path holds few locks.
- **Optimistic traversal.** Walk with no locks, lock $pred$ and $curr$, and then check that $pred$ is still reachable and still points to $curr$; if not, start again (the optimistic list of Herlihy and Shavit). The lazy list adds a *marked* bit so that the check needs no second traversal.
- **Links to the right.** B-link trees let a process that was passed by a split recover by moving right, instead of holding the parent.
- **Ordered locking of a bounded window.** Hold $w \ge 2$ locks along the path, for operations that change more than two adjacent nodes.

## Pitfalls

- **Releasing too early.** If a process releases $pred$ before it takes $curr$, another process can change $next(pred)$ or remove $curr$ in the gap. The test file shows both failures: a lost add and a remove that is undone.
- **Two directions.** If some operations walk the structure in the opposite direction, such as along the $prev$ links of a doubly linked list or up a tree, the locks are no longer taken in one order, and two processes can deadlock. Such operations must take the locks in the global order, for example by releasing and taking the locks again from the top, or by using try-lock and backing off.
- **A hot head.** Every operation locks $H$ (or the root) first, and no process can pass the one in front of it. A slow process near the head, for example one that is preempted, holds up every process behind it.
- **Cost per node.** Each visited node costs a lock and an unlock, and in a cache-coherent machine each of them writes the lock word and moves its cache line. For read-mostly workloads, the optimistic and lazy lists, or a lock-free list, are much faster.
- **Not two-phase.** A process releases locks before it has taken all of them, so a sequence of calls is not atomic as a whole. Coupling makes each call linearizable, but a transaction that combines several calls needs another mechanism.

## Exercises

1. Show that the list stays correct if `ADD` and `REMOVE` release $pred$ before $curr$. Which order lets other processes in sooner?
2. Change `LOCATE` so that it releases $pred$ before it takes $curr$, and find a schedule with two removes of neighboring keys after which a removed key is back in the set.
3. Prove that `CONTAINS` needs no lock at all if keys are never removed and each write of a pointer is atomic.
4. A doubly linked list with $prev$ pointers must support `REMOVE` with coupling from the head. Which locks must the remover hold, and in which order, to keep both directions consistent without deadlock?

## References
