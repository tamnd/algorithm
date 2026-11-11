---
tag: M2X7MT
kind: algorithm
slug: drop-the-anchor
name: Drop the anchor
aliases: [DTA, anchor-based reclamation]
area: concurrency/memory-reclamation
level: research
summary: A traversal publishes an anchor once every K nodes instead of a hazard pointer per node. An anchor guards the next K nodes, so reclamation stays bounded with few shared writes.
solves: [safe-memory-reclamation]
complexity:
  vars: {n: the number of processes, K: the number of nodes between two anchors, R: the retired list length that starts a scan, L: the number of nodes that a traversal visits}
  space: {anchors: Θ(n), unfreed_garbage: O(n R)}
  steps: {anchor_writes: O(1 + L / K), scan: O(n + R)}
properties: {robust: true, bounded_garbage: true, per_read_cost: false, needs_double_width_cas: true}
history:
  year: 2013
  people: [Anastasia Braginsky, Alex Kogan, Erez Petrank]
  note: Braginsky, Kogan and Petrank presented drop the anchor at SPAA 2013, for the lock-free linked list, with a recovery that freezes and replaces the nodes near the anchor of a stuck thread.
prereqs: [safe-memory-reclamation, hazard-pointers]
see_also: [harris-linked-list, michael-scott-queue, treiber-stack, epoch-based-reclamation, hazard-eras, interval-based-reclamation]
sources:
  - paper: doi:10.1145/2486159.2486184
    title: Anastasia Braginsky, Alex Kogan and Erez Petrank, Drop the anchor, lightweight memory management for non-blocking data structures, SPAA 2013, pages 33-42
    locator: the description of anchors placed every K hops in the linked list, the reclamation rule for nodes near an anchor, and the freezing and recovery of the nodes near the anchor of a stuck thread
  - paper: doi:10.1109/TPDS.2004.8
    title: Maged M. Michael, Hazard pointers, safe memory reclamation for lock-free objects, IEEE Transactions on Parallel and Distributed Systems 15(6), 2004, pages 491-504
    locator: the publish and check protocol and the scan that the anchors make cheaper
---

Drop the anchor is a [safe memory reclamation](/safe-memory-reclamation/) method by Anastasia Braginsky, Alex Kogan and Erez Petrank. With [hazard pointers](/hazard-pointers/), a traversal writes a shared pointer and makes a check for every node it visits. With drop the anchor, a traversal publishes an **anchor** only once every $K$ nodes, and an anchor guards the node it names and the $K$ nodes after it. A reclaimer frees a retired node only if no anchor guards it. So a long traversal makes few shared writes, and a stuck thread still guards only about $K$ nodes, which keeps the garbage bounded.

This page implements a simplified version on the [Michael and Scott queue](/michael-scott-queue/) and the [Treiber stack](/treiber-stack/). The paper works on the [Harris linked list](/harris-linked-list/) and adds a recovery for stuck threads; that part is not implemented here.

## In plain words

A group of climbers walk along a rope that others are cutting from the back.

A climber does not hold the rope at every step. Every few steps, the climber drops an anchor, and the anchor holds that point and the next few steps of rope.

Before going on, the climber checks that the anchor point is still part of the rope. If it was already cut off, the climber goes back to the start.

The people who cut rope may throw away a piece only if no anchor holds it. A climber who falls asleep holds only a short piece, so most of the old rope can still go.

## The problem

[Safe memory reclamation](/safe-memory-reclamation/) for lock-free structures, with a lower cost per node read than hazard pointers and with a bound on the garbage that a stuck thread can cause, which [epoch-based reclamation](/epoch-based-reclamation/) does not give.

The model: $n$ asynchronous processes on a sequentially consistent shared memory with reads, writes, [compare-and-swap](/compare-and-swap/) and a compare-and-swap on two adjacent words. The version here runs on a queue whose nodes carry a sequence number, one more than the node before them. The head and the tail are each kept in one double-width word with the number of their node, so $hseq$ is the number of the head node. An anchor is a sequence number $a$, and it guards the numbers $a$ to $a + K$. Nodes leave the queue only at the head, in order, so a reclaimer never has to follow pointers from an anchor. On the stack, a pop reads only the top node, so there the anchor names the top node by address, as a hazard pointer does.

## The algorithm

```pseudo id=main
TRAVERSE(t)                          ▷ walk the queue from the head
L1  (x, s) ← (head, hseq); ANCHOR[t] ← s; if (head, hseq) ≠ (x, s) then repeat L1
    hops ← 0; repeat: use x
L2      y ← x.next; if y = nil then stop
L3      hops ← hops + 1
L4      if hops = K then
L5          ANCHOR[t] ← y.seq; hops ← 0
L6          if hseq > y.seq then go to L1     ▷ y has already left the queue
L7      x ← y
SCAN(t)                              ▷ when the retired list of t holds R nodes
L8  A ← the set of all ANCHOR[q] that are not nil
L9  for each retired (x, s): if some a ∈ A has a ≤ s ≤ a + K then keep x
L10     else free x
```

L1 anchors the head as hazard pointers do: publish, then check that the head did not move. From there the traversal reads up to $K$ nodes after its anchor with no shared writes. At the $K$-th node $y$, it moves the anchor to $y$ and checks at L6 that $y$ has not left the queue. If $hseq \le y.seq$ at that time, then $y$ and every node after it were retired after the new anchor was written, so any scan that could free them sees the anchor. A dequeue and an enqueue use L1 on the head or the tail and read only the anchored node and its successor, which the anchor also guards.

## Example

A queue $D \to A \to B \to C$ with numbers 0 to 3, where $D$ is the dummy head, $K = 2$ and $R = 1$, so every retire scans at once. Process $p$ traverses, and process $q$ dequeues.

| step | process | line | action | state after |
|---|---|---|---|---|
| 1 | $p$ | L1 | reads $(D, 0)$, writes $ANCHOR[p] = 0$, the head did not move | guards 0 to 2 |
| 2 | $p$ | L2, L3 | reads $D.next = A$, one hop; $x = A$ | |
| 3 | $q$ | dequeue | moves the head to $(A, 1)$, retires $D$ with number 0 | $hseq = 1$ |
| 4 | $q$ | L8 to L10 | anchors $\{0\}$: 0 is in 0 to 2, so keeps $D$ | $D$ kept |
| 5 | $p$ | L2 to L5 | reads $A.next = B$, two hops, writes $ANCHOR[p] = 2$ | guards 2 to 4 |
| 6 | $p$ | L6 | $hseq = 1 \le 2$, so $B$ is in the queue; $x = B$ | |
| 7 | $q$ | dequeue | moves the head to $(B, 2)$, retires $A$ with number 1 | $hseq = 2$ |
| 8 | $q$ | L8 to L10 | anchors $\{2\}$: frees $D$ (0) and $A$ (1), keeps nothing else | |
| 9 | $p$ | L2 | reads $B.next = C$ safely | |

If $q$ had dequeued $A$ and $B$ before step 6, then $hseq = 3 > 2$ and $p$ starts again at L1. Without that check, $p$ would go on from $B$, which a scan may already have freed. The test finds this run.

## Correctness

The full proof is in proofs/correctness.md. It assumes that a process reads a node only under an anchor that guards it and that it checked after the write, that each node is retired once by the process that removed it, and that nodes are freed only at L10.

- **Removal in order.** The head CAS moves $hseq$ from $s$ to $s + 1$ and removes the node with number $s$. So the removed nodes are exactly those with numbers below $hseq$, and unfreed retired nodes have different numbers.
- **Key fact.** If a process reads node $x$ with number $s_x$ under anchor $a$, then after the write of $a$ it saw $hseq \le a \le s_x$, so $x$ was retired after the anchor was written. Any scan that could free $x$ starts later, reads the anchor, and keeps $x$.
- **Bound.** An anchor guards at most $K + 1$ unfreed nodes, so a scan keeps at most $n (K + 1) < R$ nodes and each list holds at most $R$. At most $n R$ retired nodes are unfreed.

The test file checks every interleaving of small stack runs, queue runs and traversals with $K = 1$ and $K = 2$, seeded random runs, two broken versions (an anchor without the check, and an anchor that guards only its own node), an immediate free, and the garbage under a stall.

## Complexity

| measure | value |
|---|---|
| shared space | one anchor word per process, and a sequence number per node |
| traversal of $L$ nodes | $\lceil L / K \rceil$ anchor writes and checks, against $L$ for hazard pointers |
| scan | $n$ anchor reads; frees at least $R - n (K + 1)$ nodes |
| unfreed garbage | at most $n R$, even with stopped threads |

**Garbage under a stall.** The test runs three processes with $K = 2$ and $R = 2 n (K + 1) = 18$. Process 0 stops for good inside its first pop, dequeue or traversal, and the two others do 50 or 400 operations each. The peak of unfreed retired nodes is between 32 and 37 in all runs, under the proved bound $n R = 54$, and it does not grow with the run length.

## Properties

- Robust: a stopped thread guards at most $K + 1$ nodes, so the garbage stays bounded.
- A traversal writes to shared memory once every $K$ nodes, not once per node.
- Reads between two anchors need no fence and no check.
- The version here needs double-width words for the pointer and its sequence number.
- Larger $K$ means fewer writes but more nodes kept by each anchor.

## Variants and improvements

- **The original method.** In the [Harris linked list](/harris-linked-list/), nodes leave from the middle and $next$ pointers change, so a range of numbers does not describe what an anchor guards. The paper keeps anchors as node pointers with timestamps and lets the reclaimer reason about the $K$ nodes after each anchor. When a thread is stuck, other threads freeze the nodes near its anchor, copy them and replace them in the list, so the stuck thread no longer holds the rest of the list; on waking up it sees the change and starts again.
- **[Hazard pointers](/hazard-pointers/).** The case $K = 1$ in spirit: one protected node per publish and check, at the cost of a write and a fence per node.
- **[Hazard eras](/hazard-eras/) and [interval-based reclamation](/interval-based-reclamation/).** They reduce the writes by publishing eras instead of pointers, and need no help from the data structure, but they bound the garbage less tightly when a thread is stuck.

## When to use it

Use the anchor idea for long traversals over structures where hazard pointers cost too much and epoch methods are not robust enough. It needs the help of the data structure: a cheap way to tell from an anchor which nodes it guards, such as sequence numbers in a queue, or the freezing and recovery of the paper for a list. For short operations such as stack pops, it gives the same result as hazard pointers.

## Pitfalls

**Anchoring without the check.** The wrong code writes the new anchor at L5 and goes on at L7. The node $y$ may already have left the queue and been freed before the anchor was written. The right code checks $hseq \le y.seq$ at L6 and starts again if the check fails. The test finds this.

**An anchor that guards only its node.** The wrong scan keeps a node only if an anchor names it exactly. The traversal still reads the next $K$ nodes, which the scan then frees. The right L9 keeps every node with a number from $a$ to $a + K$. The test finds this.

**Reading past $K$ hops.** The traversal must move its anchor at the $K$-th node. A read of the node $K + 1$ after the anchor is not guarded.

**Numbers that wrap around.** If the sequence numbers wrap, two unfreed nodes can share a number and an old anchor can guard the wrong range. Use 64-bit numbers.

## Implementations

## History

Anastasia Braginsky, Alex Kogan and Erez Petrank presented drop the anchor at SPAA 2013, as a lighter form of hazard pointers for lock-free linked lists. The goal was the low cost per read of epoch-based reclamation together with the robustness of hazard pointers, which they kept with the freezing and recovery of the nodes near the anchor of a stuck thread.

## References
