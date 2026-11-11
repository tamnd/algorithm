---
tag: X31NPD
kind: concept
slug: linearization-point
name: Linearization point
aliases: [commit point]
area: concurrency/lock-free-structures
level: core
summary: A proof method for linearizability. Pick one step inside each operation where it takes effect, and show that the order of these steps is a legal sequential run.
prereqs: [linearizability]
see_also: [linearizability, treiber-stack, michael-scott-queue, herlihy-wing-queue, harris-linked-list, helping, afek-atomic-snapshot, universal-construction]
sources:
  - paper: doi:10.1145/78969.78972
    title: Maurice P. Herlihy and Jeannette M. Wing, Linearizability, A correctness condition for concurrent objects, ACM Transactions on Programming Languages and Systems 12(3), 1990
    locator: pages 463 to 492; the queue that uses fetch-and-increment and swap, whose operations have no fixed linearization point, and its proof with sets of possible values
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 3 (linearization points), Chapter 9 (the lazy list and its linearization points), Chapter 10 (the lock-free queue), Chapter 11 (the lock-free stack)
  - paper: doi:10.1145/248052.248106
    title: Maged M. Michael and Michael L. Scott, Simple, fast, and practical non-blocking and blocking concurrent queue algorithms, PODC 1996
    locator: pages 267 to 275 (the linearization points of the lock-free queue)
  - paper: doi:10.1007/11795490_3
    title: Steve Heller, Maurice Herlihy, Victor Luchangco, Mark Moir, William N. Scherer III and Nir Shavit, A lazy concurrent list-based set algorithm, OPODIS 2005, LNCS 3974, 2006
    locator: pages 3 to 16 (an unsuccessful contains whose point can lie in a step of another process)
  - paper: doi:10.1016/0304-3975(91)90224-P
    title: Martin Abadi and Leslie Lamport, The existence of refinement mappings, Theoretical Computer Science 82(2), 1991
    locator: pages 253 to 284 (prophecy variables, the general tool when a point depends on the future)
---

A linearization point of an operation is one atomic step, inside the interval between its invocation and its response, at which the operation seems to take effect. The method of linearization points proves that an object is [linearizable](/linearizability/): name a point for each operation, and show that applying the operations in the order of their points to the sequential object gives the results that the real operations returned. For simple objects, such as the [Treiber stack](/treiber-stack/), the point is a fixed instruction of the operation itself. For harder ones it depends on what other processes do, and for some, such as the [Herlihy and Wing queue](/herlihy-wing-queue/), no fixed instruction works.

## In plain words

A shared stack can be in use by many threads, and their calls overlap in time. To say that it behaves like a normal stack, you pick, for each call, one moment between its start and its end. You say: "this is when the call really happened". Then you list the calls in the order of these moments, run them one at a time on a normal stack, and check that each call would return what it really returned.

If you can always pick such moments, the shared stack is correct. Usually the moment is one special instruction, such as the successful compare-and-swap that changes the top of the stack. If you pick the wrong instruction, the check fails, even when the stack is correct.

## The idea

**Notation and model.** $n$ is the number of processes, $p$ and $q$ are processes, $i$ and $j$ are indices, $k$ is the contention and $m$ is the number of shared words. Processes are asynchronous and can crash between steps. Memory is sequentially consistent, and each read, write and compare-and-swap is one atomic step. The method shows a safety property ([linearizability](/linearizability/)); progress, such as [lock-freedom](/lock-freedom/), needs a separate proof.

**The method.** Fix an *abstraction function* $A$ that maps the shared memory to a state of the sequential object. For a stack it maps the list from top to the sequence of its values. Then, for each operation $e$, name a step $\ell(e)$, its *linearization point*, and show three facts.

1. $\ell(e)$ lies inside the interval of $e$: after its invocation and before its response. It may be a step of another process, but it must happen in that interval.
2. Each step that is not a linearization point leaves $A(\text{memory})$ the same.
3. At $\ell(e)$, $A$ changes exactly as the sequential operation would change it, and the result that the sequential operation would return in that state is the result that $e$ returns.

A pending operation gets a point only if it has taken effect.

**Why the method works.** Let $S$ be the sequence of operations in the order of their points. By facts 2 and 3, $S$ is a legal sequential history with the same results as $H$, so it meets rule (L1) of the definition. For rule (L2), take $e <_H f$, so $e$ responds before $f$ is invoked. By fact 1, $\ell(e)$ comes before the response of $e$, which comes before the invocation of $f$, which comes before $\ell(f)$. So $e$ is before $f$ in $S$. $\square$

The converse also holds in a weak sense: if a history is linearizable, you can pick one instant in each interval in the order of a linearization. But that instant need not be a step of the code that you can name in advance.

**Fixed and non-fixed points.** A point is *fixed* if it is a fixed instruction of the operation itself, for example "the successful CAS at line L2". Many proofs need more:

- The point depends on the run. The pop of a Treiber stack has its point at the successful CAS if it finds an item, and at the read of `top` that returned null if the stack is empty. The dequeue of the [Michael and Scott queue](/michael-scott-queue/) is similar.
- The point is a step of another process. In the lazy list of Heller et al. (2005), an unsuccessful `contains(x)` may be linearized just before another process adds `x`. In algorithms with [helping](/helping/), such as the [Kogan and Petrank queue](/kogan-petrank-queue/) or the [universal construction](/universal-construction/), a helper's CAS is often the point of the operation it helps.
- The point depends on the future. In the [Herlihy and Wing queue](/herlihy-wing-queue/), an enqueue takes a slot with fetch-and-increment and then stores its item. Neither step can serve as the point: two enqueues can take slots in one order and become visible to dequeuers in the other, and which order is right depends on later dequeues. Herlihy and Wing proved this queue correct with sets of possible abstract values instead of points. The general tool for such cases is a prophecy variable (Abadi and Lamport 1991).

## Examples

All numbers below come from the explorer and the tests in the implementation folder. The stack is the Treiber stack: one shared word `top`, nodes that are never reused (so there is no [ABA problem](/aba-problem/)), and these operations.

```text
push(v):  loop:  t := read(top)                           ▷ L1
                 if CAS(top, t, new node(v, next = t)): return       ▷ L2, the point
pop():    loop:  t := read(top)                           ▷ L3
                 if t = null: return empty                ▷ the point is the read at L3
                 if CAS(top, t, t.next): return t.value   ▷ L4, the point
```

**A worked run.** The stack is empty. $p_0$ calls push(1) and $p_1$ calls push(2). The schedule is $p_0, p_1, p_1, p_0, p_0, p_0$.

| Step | Process | Action | Result | Abstract stack |
|---|---|---|---|---|
| 1 | $p_0$ | L1 read top | null | empty |
| 2 | $p_1$ | L1 read top | null | empty |
| 3 | $p_1$ | L2 CAS(top, null, node 2) | true: point of push(2) | 2 |
| 4 | $p_0$ | L2 CAS(top, null, node 1) | false | 2 |
| 5 | $p_0$ | L1 read top | node 2 | 2 |
| 6 | $p_0$ | L2 CAS(top, node 2, node 1) | true: point of push(1) | 2, 1 (1 on top) |

The order of the points is push(2), push(1). Only steps 3 and 6 change the abstract stack, as fact 2 needs. The two calls overlap, so either order is allowed by real time, and this one is legal.

**Every run of a small case.** Process $p_0$ runs push(1) then pop(), and $p_1$ runs push(2) then pop(), on an empty stack. The explorer visits 419 states (counting the history in the state) and finds 70 different complete histories. In each of them the order of the points is a legal stack run with the real results. With three processes that run push(1), push(2) and pop() on the stack [0], there are 703 states and 90 histories, and again all pass.

**A wrong choice of points.** Put the point of push at its first read of `top` (L1) instead. In the same two-process case, 24 of the 70 histories fail the check. One of them:

1. $p_1$ runs push(2) to the end. The stack is [2].
2. $p_0$ calls push(1) and reads `top`. With the wrong choice, this is the point of push(1).
3. $p_1$ calls pop(), and its CAS removes 2. It returns 2.
4. $p_0$'s CAS fails, because `top` changed. $p_0$ reads again and pushes 1. Then $p_0$ pops and gets 1.

The order of the wrong points is push(2), push(1), pop by $p_1$. A sequential stack would return 1 to that pop, but $p_1$ got 2. The stack is still linearizable (the right order is push(2), pop returns 2, push(1), pop returns 1), and the checker confirms this. Only the choice of points was wrong. A failed CAS does not take effect, so its read cannot be the point.

**A wrong algorithm.** Replace the CAS in pop with a read of `top` followed by a plain write of `top.next`. Two processes pop from the stack [1, 2]. Of the 6 possible histories, 4 are not linearizable. In one, both processes read node 2 before either writes, and both return 2. No choice of points can fix this, and the brute force checker rejects the history.

## Where it is used

- Proofs of nearly every lock-free object: the [Treiber stack](/treiber-stack/), the [Michael and Scott queue](/michael-scott-queue/), the [Harris linked list](/harris-linked-list/) (where the point of a delete is the CAS that marks the node, see [logical deletion](/logical-deletion/)), and [split-ordered lists](/split-ordered-list/).
- In the [universal construction](/universal-construction/), the point of an operation is the consensus decision that puts it in the log.
- In the [Afek et al. snapshot](/afek-atomic-snapshot/), a scan that sees two equal collects is linearized between them, and a scan that borrows another scan's view is linearized inside the borrowed scan. That second case is a point in a step of another process.
- Testing tools record the point that the code claims (here, an `("lp",)` event after the step) and check the order of points, which is much cheaper than the full linearizability search. A failed check shows a wrong proof or a wrong algorithm, and the full search tells which.

## References
