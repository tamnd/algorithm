---
tag: 8G5PTB
kind: data-structure
slug: diffracting-tree
name: Diffracting tree
area: data-structures/concurrent-structures
level: advanced
summary: Binary tree of balancers with prism elimination that spreads tokens to counter leaves with low contention.
prereqs: [counting-network, compare-and-swap, quiescent-consistency]
see_also: [combining-tree, combining-funnel, bitonic-counting-network, elimination-backoff-stack, sloppy-counter, lock-freedom, linearizability]
sources:
  - paper: doi:10.1145/235543.235546
    title: Nir Shavit and Asaph Zemach, Diffracting trees, ACM Transactions on Computer Systems 14(4), 1996
    locator: pages 385 to 428, the counting tree, the prism, and the proof of the step property
  - book: isbn:9780123973375
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, revised reprint
    locator: Chapter 12, Section 12.6 (Diffracting Trees), pages 303 onward; Chapter 11, Section 11.4.1 (A Lock-Free Exchanger)
  - paper: doi:10.1145/185675.185815
    title: James Aspnes, Maurice Herlihy and Nir Shavit, Counting networks, Journal of the ACM 41(5), 1994
    locator: pages 1020 to 1048, balancers, the step property and quiescent consistency of counters
---

A diffracting tree is a shared counter built from a binary tree of *balancers*. Each call is a token that enters at the root and at each balancer goes left or right, until it reaches one of $w$ output wires; wire $i$ hands out the values $i, i + w, i + 2w, \ldots$. A balancer is a toggle bit that sends tokens left and right in turn, and in front of it sits a *prism*, an array of exchangers where two tokens that meet are sent one left and one right without touching the toggle. Shavit and Zemach introduced the structure in 1996. Its counter is [quiescently consistent](/quiescent-consistency/), not [linearizable](/linearizability/), and with lock-free toggles it is [lock-free](/lock-freedom/). Under high load the prisms take most of the traffic away from the toggles, so the root stops being a hot spot.

## In plain words

Picture a river that splits in two, and each branch splits again, until there are eight streams. At each split a gate sends boats to the left and right in turn, so the streams get equal numbers of boats. Each stream has its own ticket booth: the first stream gives tickets 0, 8, 16, the second 1, 9, 17, and so on. Together the booths hand out every number once.

One gate for each split is still a crowded place. So in front of each gate there is a wide pool. Two boats that meet in the pool agree that one goes left and one goes right, and they skip the gate. The balance is the same, because one boat went each way. Only a boat that finds no partner in the pool uses the gate.

## The abstract type

The tree implements a shared counter: getAndIncrement() returns a value and each value is returned once. The guarantee is quiescent consistency: in every quiescent state, a moment when no call is in progress, the calls so far have returned exactly $0, 1, \ldots, n - 1$. While calls are in progress, a call may return a larger value than a later call, so the counter is not linearizable. For uses that only need distinct values that fill a range, such as handing out slots or building a pool, this is enough.

## Representation

- Width $w = 2^k$, and $w - 1$ balancers in a complete binary tree of depth $k$, stored in heap order: the children of balancer $j$ are $2j + 1$ and $2j + 2$.
- Each balancer $b$ has a toggle $b.toggle \in \{0, 1\}$, initially 0, read and changed by [compare-and-swap](/compare-and-swap/), and a prism $b.prism$ of exchanger slots. Prisms are often smaller deeper in the tree, where fewer tokens pass.
- Each exchanger slot holds a pair (item, state) with state EMPTY, WAITING or BUSY, changed by compare-and-swap.
- $T.count[0..w-1]$: one counter per output wire, changed by [fetch-and-add](/fetch-and-add/).

The root decides bit 0 of the wire, its children bit 1, and so on. Every caller has a distinct id, which decides who goes which way after a meeting in a prism.

## Operations

```pseudo id=main
GET-AND-INCREMENT(T, me)
L1  j ← 0; wire ← 0; bit ← 1
L2  while j < w − 1 do                         ▷ balancer j of the tree
L3      d ← BALANCE(T.b[j], me)
L4      wire ← wire + d·bit; bit ← 2·bit; j ← 2j + 1 + d
L5  k ← FETCH-AND-ADD(T.count[wire], 1)
L6  return wire + w·k

BALANCE(b, me)
L7  i ← a random index of b.prism
L8  partner ← EXCHANGE(b.prism[i], me, patience)
L9  if partner ≠ TIMEOUT then return 0 if me < partner else 1     ▷ diffracted
L10 repeat t ← b.toggle until CAS(b.toggle, t, 1 − t)
L11 return t

EXCHANGE(slot, me, patience)
L12 repeat at most patience times
L13     (x, state) ← slot
L14     if state = EMPTY and CAS(slot, (x, EMPTY), (me, WAITING)) then
L15         wait up to patience steps for state = BUSY; if it comes, take the item, set slot to (nil, EMPTY), return it
L16         if CAS(slot, (me, WAITING), (nil, EMPTY)) then return TIMEOUT
L17         take the item, set slot to (nil, EMPTY), return it            ▷ a partner came at the last moment
L18     if state = WAITING and CAS(slot, (x, WAITING), (me, BUSY)) then return x
L19 return TIMEOUT
```

**The exchanger.** It is the lock-free exchanger of Herlihy and Shavit. A token that finds the slot EMPTY installs its id and waits. A token that finds it WAITING swaps in its own id with state BUSY and leaves with the waiting id. The waiting token sees BUSY, takes the partner id and frees the slot. If no partner comes, the waiting token takes itself out with a CAS (line L16); if that CAS fails, a partner came just in time (line L17). Both tokens of a pair get each other's id, so exactly one of them, the smaller id, goes left.

**The toggle.** A token that finds no partner flips the toggle and goes the way the toggle pointed before the flip (lines L10 and L11).

**The counter.** At the wire, the token takes the next index $k$ of that wire and returns $wire + w \cdot k$.

## Example

Width 2: one balancer with a prism of one slot, and wires 0 and 1 that give even and odd values. Thread $B$ (id 1) starts first, finds no partner in the prism, flips the toggle from 0 to 1, and is delayed before it reaches wire 0. Then thread $A$ (id 0) calls twice.

| step | thread | what it does | toggle | count[0] | count[1] |
|---|---|---|---|---|---|
| 1 | $B$ | L7 to L9: prism times out | 0 | 0 | 0 |
| 2 | $B$ | L10, L11: flips the toggle, side 0; then stalls | 1 | 0 | 0 |
| 3 | $A$ | prism times out; flips the toggle, side 1 | 0 | 0 | 0 |
| 4 | $A$ | L5, L6: wire 1, $k = 0$, returns 1 | 0 | 0 | 1 |
| 5 | $A$ | second call: flips the toggle, side 0 | 1 | 0 | 1 |
| 6 | $A$ | L5, L6: wire 0, $k = 0$, returns 0 | 1 | 1 | 1 |
| 7 | $B$ | L5, L6: wire 0, $k = 1$, returns 2 | 1 | 2 | 1 |

$A$ got 1 and then 0, in this order, so the history is not linearizable. But $B$ was in progress the whole time, so there is no quiescent point between the two calls of $A$, and at the end the values are exactly 0, 1, 2: the history is quiescently consistent.

Now diffraction. Two threads with ids 5 and 9 enter the same balancer at the same time. Thread 5 installs itself in the slot (WAITING), and thread 9 swaps in (BUSY) and leaves with partner 5, so it goes right, to wire 1, and gets 1. Thread 5 sees BUSY, takes 9, goes left, to wire 0, and gets 0. The toggle stayed 0, and each side got one token, exactly as if both had used the toggle.

## Correctness

The proof has three parts. First, the exchanger pairs tokens symmetrically: if a token returns partner $y$, then token $y$ returns this token's id, so a diffracted pair sends one token to each side. Second, each balancer has the *step property* in every quiescent state: the toggle sends tokens to side 0 and side 1 in turn, starting with 0, and diffracted pairs add one to each side, so the number that left on side 0 minus the number on side 1 is 0 or 1. By induction on the depth, the whole tree has the step property: in a quiescent state with $n$ tokens out, wire $i$ has received $\lceil (n - i)/w \rceil$ tokens. Third, so the wire counters have handed out exactly $\{i + w k\}$ for these counts, which is $\{0, \ldots, n - 1\}$, and that is quiescent consistency. Each call ends within a bounded number of its own steps except for retries of the toggle CAS, and a failed CAS means another token's CAS succeeded, so the tree is lock-free. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| quantity | value |
|---|---|
| balancers passed per call | $\log_2 w$ |
| steps per call without contention | $O(\log w)$, plus the patience spent in each prism |
| toggle accesses | only by tokens without a prism partner |
| space | $w - 1$ balancers, their prisms, $w$ counters |

If all calls used the toggles, the root toggle would see every token, which is the contention of a single counter. Shavit and Zemach measured that under high load the prisms take most tokens away from the toggles, so that a tree with prisms of the right size keeps its throughput as the number of processors grows. The patience and the prism sizes must be tuned: a large prism spreads the tokens so far that they rarely meet, and a small one is itself a hot spot. At low load every token waits in vain in each prism, so the tree is slower than a plain counter there.

## Variants

- **[Counting networks](/counting-network/).** A [bitonic counting network](/bitonic-counting-network/) of width $w$ has depth $O(\log^2 w)$ but lets tokens pass many balancers in parallel; a diffracting tree has depth $\log w$ but all tokens pass its root.
- **Elimination trees.** Shavit and Touitou let a token for an insert and a token for a delete that meet in a prism cancel each other, which gives pools and stacks. The [elimination backoff stack](/elimination-backoff-stack/) uses the same exchanger.
- **Reactive trees.** Della-Libera and Shavit grow and shrink the tree with the load, so that it acts as a single counter when contention is low.
- **[Combining trees](/combining-tree/) and [combining funnels](/combining-funnel/).** Combine increments instead of spreading them, and so are linearizable, but threads wait for each other.

## When to use it

Use a diffracting tree when many threads need distinct values or slots at a high rate, and the order between calls that overlap does not matter: index allocation in a pool, load distribution, producer-consumer pools. Do not use it when a call must see the effect of all earlier calls, such as a sequence number that must grow with real time, or at low contention, where an atomic fetch-and-add is faster and linearizable.

## Pitfalls

- **Expecting linearizability.** A thread can get a smaller value in its second call than in its first, as in the example. Quiescent consistency promises nothing about calls in progress.
- **Equal ids.** Two tokens with the same id in one prism both go the same way, and the balance breaks. Ids must be distinct.
- **A one-sided exchange.** If the waiting token gives up (line L16) with a plain write instead of a CAS, a partner can leave with its id while it also uses the toggle, and one side gets two tokens.
- **Prisms without timeouts.** A token that waits for a partner without a bound blocks for ever when the load drops.
- **Tuning for one load.** Prism sizes and patience that are good at high load waste time at low load. Measure at the loads that matter.

## Implementations

The Python module simulates each atomic word, the toggles, the exchanger slots and the wire counters, by a word with a lock around get, set, compare-and-swap and fetch-and-add. Each access is one step of a generator, so the tests replay the example and a diffraction step by step, check that every random interleaving is quiescently consistent, and confirm that some interleavings are not linearizable. The plain method also runs under real threads.

## History

Aspnes, Herlihy and Shavit introduced counting networks and their step property in 1991, with the journal version in 1994. Shavit and Zemach added prisms to a tree of balancers in 1996, and called the splitting of a pair in a prism diffraction. Shavit and Touitou used the same idea for elimination trees. Herlihy and Shavit's textbook presents the tree with their lock-free exchanger.

## References
