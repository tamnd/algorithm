---
tag: 7A48EK
kind: concept
slug: retroactive-data-structure
name: Retroactive data structure
aliases:
- retroactivity
area: data-structures/persistent-structures
level: research
summary: A structure that supports inserting or deleting an operation in the past and recomputing later answers.
prereqs: [persistent-data-structure, priority-queue, queue]
see_also: [partial-persistence, full-persistence, version-tree, offline-dynamic-connectivity, segment-tree, undo-log, kinetic-heap, horner-rule]
sources:
  - paper: doi:10.1145/1240233.1240236
    title: Erik D. Demaine, John Iacono and Stefan Langerman, Retroactive data structures, ACM Transactions on Algorithms 3(2), 2007
    locator: the definitions of partial and full retroactivity, the rollback method and its lower bound, and the retroactive queue, deque, union-find and priority queue
  - url: https://ocw.mit.edu/courses/6-851-advanced-data-structures-spring-2012/
    title: Erik Demaine, MIT 6.851 Advanced Data Structures, Spring 2012
    locator: Lecture 2, Retroactive data structures
---

A retroactive data structure keeps a timeline of the operations done on it, and lets a program insert an operation at a past time or delete a past operation. The structure then behaves as if the timeline had always been the new one: every later state, and every later answer, follows from the changed past. This is different from a [persistent data structure](/persistent-data-structure/), in which a change to an old version makes a new branch and leaves the later versions as they were. Erik Demaine, John Iacono and Stefan Langerman defined retroactivity and studied it in 2004, in a paper that appeared in a journal in 2007. They showed that there is no efficient general method, and gave efficient retroactive versions of queues, deques, union-find and priority queues.

## In plain words

Think of a bank account as a list of deposits and withdrawals in time order. Someone finds that a deposit from last week was never entered. With an ordinary structure, you can only add it today. With a retroactive structure, you add it at last week's date, and every balance after that date is now correct.

The hard part is that one change in the past can change many later results. For some structures, only a few things change, and a clever design can fix them fast. For other structures, one change in the past can force you to redo everything after it.

## The idea

**The timeline.** A retroactive structure keeps a sequence of update operations $u_{t_1}, u_{t_2}, \ldots$ at times $t_1 < t_2 < \cdots$. The state at time $t$ is the result of doing, in order, the updates before $t$ on the empty structure. The operations are:

- $\text{Insert}(t, u)$: add the update $u$ at time $t$;
- $\text{Delete}(t)$: remove the update at time $t$;
- $\text{Query}(t, q)$: answer the query $q$ on the state at time $t$.

A structure is *partially retroactive* if it supports Insert and Delete at any time, but Query only on the present state, after all updates. It is *fully retroactive* if Query works at any time. Let $m$ be the number of updates in the timeline, and $r$ the number of updates after the time of a retroactive change.

**Retroactivity versus persistence.** In both, the past can be reached. Under [full persistence](/full-persistence/), an update to an old version adds a new branch to the [version tree](/version-tree/), and the old future stays as it was. Under retroactivity, there is only one timeline, and a change in the past changes the one future. A fully retroactive structure can answer queries at any time, which also gives the reads of [partial persistence](/partial-persistence/).

**The rollback method.** Any structure can be made retroactive by keeping an [undo log](/undo-log/): to change the past at time $t$, undo the $r$ updates after $t$, apply the change, and redo the $r$ updates. This costs a factor of $O(r)$ over the cost of an update. Demaine, Iacono and Langerman showed that, in general, nothing can do much better. Their example keeps a value $x$ with updates such as $x \gets a x + b$ and the query "return $x$". A change at the start of the timeline changes the final answer into a polynomial of degree $r$ whose coefficients come from the later updates. In the algebraic model, evaluating a general polynomial of degree $r$ needs $\Omega(r)$ arithmetic steps, so [Horner's rule](/horner-rule/), which is the rollback method here, cannot be beaten by much. So efficient retroactivity needs structure-specific ideas.

**Easy cases.** Some kinds of updates make retroactivity simple.

- If the updates commute, the order does not matter for the present state, so a retroactive insert can be done at the present time. If each update also has an inverse, a retroactive delete is the inverse done at the present time. Such a structure is partially retroactive at no extra cost; a dictionary of counts with add and remove is an example.
- If the queries are *decomposable*, so that the answer on a union of sets of updates comes from the answers on the parts, a [segment tree](/segment-tree/) over time makes the structure fully retroactive with an $O(\log m)$ factor overhead. Each update is stored at the $O(\log m)$ nodes that cover the time interval in which it is alive.
- A general result turns any partially retroactive structure into a fully retroactive one, with a factor of $O(\sqrt{m})$ more time, by keeping about $\sqrt{m}$ checkpoint copies along the timeline.

## Examples

**Queue.** The timeline is: at time 1 enqueue $a$, at time 2 enqueue $b$, at time 3 dequeue. The dequeue returns $a$, and the present queue is $[b]$. Now insert "enqueue $c$" at time 0.5. The dequeue at time 3 now returns $c$, and the present queue is $[a, b]$. In a queue, the $k$-th dequeue always returns the $k$-th enqueued item, so it is enough to keep the enqueues in time order and the number of dequeues. Two pointers into the enqueues give the front and back of the present queue, and each retroactive change moves each pointer by at most one step. This gives a partially retroactive queue with $O(1)$ time per operation, and with a balanced search tree over time, a fully retroactive queue with $O(\log m)$ time per operation.

**Priority queue.** The timeline is: at time 1 insert 5, at time 2 insert 3, at time 3 delete-min, at time 4 insert 7. The delete-min removes 3, so the present set is $\{5, 7\}$. Now insert "insert 1" at time 2.5. The delete-min at time 3 removes 1 instead, and 3 stays, so the present set is $\{3, 5, 7\}$. A single retroactive change can alter the item that many later delete-mins remove, in a chain, but the present set changes by exactly one item. Demaine, Iacono and Langerman used this fact, and a characterization of that one item by *bridges*, the times $t$ at which every item in the queue at time $t$ is still in the present queue, to build a partially retroactive priority queue with $O(\log m)$ time per operation, using [balanced binary search trees](/balanced-binary-search-tree/) over time.

**Union-find.** Unions commute, and a query "are $x$ and $y$ connected at time $t$" asks for connectivity in the forest of the unions before $t$. Storing each union as an edge labeled with its time, in a dynamic forest that keeps for each path the latest edge time, gives a fully retroactive union-find with $O(\log m)$ time per operation.

**A hard case.** For the value $x$ with updates $x \gets a x + b$, every update after the changed time takes part in the new answer, which is the $\Omega(r)$ lower bound above. No design can avoid it in the algebraic model.

## Where it is used

- **Fixing errors in logs.** Systems that record events in time order, such as accounting systems, sensor logs and temporal databases, need to insert a late event or remove a wrong one, and keep the derived state right.
- **Offline algorithms.** Many [offline algorithms](/offline-algorithm/) treat the time of each operation as one more coordinate. The segment tree over time used for [offline dynamic connectivity](/offline-dynamic-connectivity/) is a form of full retroactivity for a structure with deletions.
- **Simulation and sweep-line methods.** A sweep over time with a priority queue of events can be fixed in place when an event is added or removed before the sweep position. Kinetic structures such as the [kinetic heap](/kinetic-heap/) face a related problem of changes in the future of a timeline.
- **Research on new bounds.** Later work gave fully retroactive priority queues with polylogarithmic time, and studied *nonoblivious* retroactivity, in which the structure also reports which past queries changed their answers.

## References
