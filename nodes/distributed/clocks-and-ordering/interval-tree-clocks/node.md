---
tag: MXR7AF
kind: data-structure
slug: interval-tree-clocks
name: Interval tree clocks
aliases:
- ITC
area: distributed/clocks-and-ordering
level: research
summary: A causality clock for a changing set of replicas. Ids and counters are binary trees over an interval, so replicas fork and join with no global names and stamps shrink after joins.
model: asynchronous-model
complexity:
  vars: {t: the number of nodes in the id and event trees of the operands, d: the depth of these trees}
  time: {worst: O(t)}
  space: {extra: O(d)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2008
  people: [Paulo Sérgio Almeida, Carlos Baquero, Victor Fonte]
  note: Almeida, Baquero and Fonte presented interval tree clocks at OPODIS 2008.
prereqs: [vector-clocks, version-vectors]
see_also: [version-vectors, dotted-version-vectors, vector-clocks, happened-before, causal-ordering, join-semilattice, crdt]
sources:
  - paper: doi:10.1007/978-3-540-92221-6_18
    title: Paulo Sérgio Almeida, Carlos Baquero and Victor Fonte, Interval tree clocks, a logical clock for dynamic systems, OPODIS 2008, LNCS 5401
    locator: pages 259 to 274; the fork-event-join model, the id and event trees, normalization, and the definitions of leq, fork, join, fill and grow
---

An interval tree clock (ITC) is a logical clock for a system in which replicas are created and retired all the time. A [version vector](/version-vectors/) needs one global name per replica and keeps an entry for every replica that ever existed. An ITC stamp instead holds an *id*, a part of the unit interval, and an *event* tree, a function on that interval. A replica forks by splitting its id, and two replicas join by uniting their ids, so no global names are needed and stamps shrink again after joins. Paulo Sérgio Almeida, Carlos Baquero and Victor Fonte described ITC in 2008.

## In plain words

Think of a ruler. At the start, one replica owns the whole ruler, and its counter is a flat line at height zero. When a replica wants to make a copy of itself, it cuts its part of the ruler in two and gives one piece away. When two replicas meet and merge, they glue their pieces back together.

To record a new event, a replica raises the line somewhere above its own piece. No one else raises the line there, so the raised spot proves that this event happened. To compare two clocks, put one line over the other: the first one is older if it is never higher.

The pieces and the lines are stored as small binary trees. After a merge, the trees simplify, so a clock stays small even when many replicas come and go.

## The abstract type

The model is the fork-event-join model over the [asynchronous model](/asynchronous-model/). A stamp is a pair $(i, e)$ of an id and an event tree. The operations are:

- FORK$(s)$: two stamps that both have the history of $s$ and disjoint ids.
- EVENT$(s)$: a stamp that records one new event.
- JOIN$(s_1, s_2)$: one stamp with both histories and the union of the ids.
- PEEK$(s)$: the anonymous stamp $(0, e)$. It carries the history in a message, and it cannot record events.
- LEQ$(s_1, s_2)$: true if and only if the causal history of $s_1$ is contained in that of $s_2$.

Sending a message is EVENT then PEEK, and receiving is JOIN with the peek then EVENT. A sync between two replicas is JOIN then FORK. The specification is the last operation: LEQ must agree with inclusion of causal histories, which gives the [happened-before](/happened-before/) order on stamps.

## Representation

An **id** is $0$, $1$, or a pair $(l, r)$ of ids. It denotes a subset of $[0, 1)$: $1$ is all of it, $0$ is none of it, and $(l, r)$ puts $l$ on the left half and $r$ on the right half. An **event tree** is an integer $n$, or a triple $(n, l, r)$ that denotes $n$ plus $l$ on the left half and $n$ plus $r$ on the right half.

Trees are kept in normal form:

- For ids: $(0, 0) \to 0$ and $(1, 1) \to 1$.
- For events: $(n, m, m) \to n + m$, and otherwise $(n, l, r) \to (n + m, l \downarrow m, r \downarrow m)$ with $m = \min(\min l, \min r)$.

Here $\min n = n$, $\min (n, l, r) = n + \min(\min l, \min r)$, and $\downarrow m$ subtracts $m$ from the root of a tree. The max function is defined in the same way, and $\uparrow m$ adds $m$ to the root. In normal form the minimum of $(n, l, r)$ is $n$.

## Operations

```pseudo id=main
FORK((i, e))
L1  (i1, i2) ← SPLIT(i);  return (i1, e) and (i2, e)

JOIN((i1, e1), (i2, e2))
L2  return (SUM(i1, i2), JOIN(e1, e2))      ▷ union of ids, pointwise max of events

EVENT((i, e))                                ▷ precondition: i ≠ 0
L3  e' ← FILL(i, e)
L4  if e' ≠ e then return (i, e')
L5  else return (i, the result of GROW(i, e) with the smallest cost)

LEQ(e1, e2)
L6  if e1 = n1 then return n1 ≤ root(e2)
L7  if e2 = n2 then return n1 ≤ n2 and LEQ(l1 ↑ n1, n2) and LEQ(r1 ↑ n1, n2)
L8  return n1 ≤ n2 and LEQ(l1 ↑ n1, l2 ↑ n2) and LEQ(r1 ↑ n1, r2 ↑ n2)
```

The helper functions are short recursions:

- **SPLIT.** $\mathrm{split}(0) = (0, 0)$ and $\mathrm{split}(1) = ((1, 0), (0, 1))$. If one half is $0$, split the other half. If both halves are nonzero, give the left half to one stamp and the right half to the other.
- **SUM.** $0$ is the identity, and two pairs are summed half by half and normalized.
- **JOIN of events.** Two integers give their maximum. Otherwise, promote an integer $n$ to $(n, 0, 0)$, keep the tree with the smaller root $n_1$, lift the children of the other tree by $n_2 - n_1$, join the children and normalize.
- **FILL.** Raise the tree inside the id as far as possible without using a value that is not already in the tree. Under a leaf $1$ of the id, a subtree becomes its maximum. If the left half of the id is $1$, the left child becomes the larger of its own maximum and the minimum of the filled right child. The right side is symmetric.
- **GROW.** Add $1$ at one place inside the id. Walk down into halves that the id covers. At a leaf $1$ over an integer, add $1$. At an integer over a mixed id, expand $n$ to $(n, 0, 0)$, which costs a large penalty. When both halves are possible, take the one with the smaller cost, so that the tree grows as little as possible.

FILL first tries to make the tree simpler: raising a part of the own region to the level of its neighbor lets normalization merge nodes. Only if FILL changes nothing does GROW add a new node.

## Example

| step | stamp $a$ | stamp $b$ | stamp $c$ |
|---|---|---|---|
| seed, then FORK | $((1,0), 0)$ | $((0,1), 0)$ | |
| EVENT on $a$ | $((1,0), (0,1,0))$ | $((0,1), 0)$ | |
| two EVENTs on $b$ | $((1,0), (0,1,0))$ | $((0,1), (0,0,2))$ | |
| FORK of $b$ | | $((0,(1,0)), (0,0,2))$ | $((0,(0,1)), (0,0,2))$ |
| JOIN of $a$ and $b$ | $((1,(1,0)), (1,0,1))$ | | $((0,(0,1)), (0,0,2))$ |
| EVENT on $a$ | $((1,(1,0)), 2)$ | | $((0,(0,1)), (0,0,2))$ |

After the first events, $a$ has $1$ on the left half and $b$ has $2$ on the right half. Neither tree is below the other, so $a$ and $b$ are [concurrent](/concurrent-events/). The join takes the maximum $(0, 1, 2)$, and normalization moves the common $1$ to the root, which gives $(1, 0, 1)$. The last event on $a$ does not grow the tree. FILL raises the left half, which $a$ owns, from $1$ to $2$, the level of the right half. Then both halves are equal, and the tree becomes the integer $2$. Now $c \le a$, since $a$ has seen everything that $c$ has.

## Correctness

Read every tree as a function on $[0, 1)$. LEQ is the pointwise order, JOIN of events is the pointwise maximum, SPLIT and SUM partition and unite sets, and EVENT raises the function only inside the own id and strictly somewhere. The ids of the live stamps always partition the interval, so each point has one owner. Only the owner raises the function at its points, and anyone who later owns a point has seen every event recorded there. So each event leaves a value at some point that no stamp without that event can reach. The tree of a stamp is the maximum of the trees of the events in its history. Together, these facts give: LEQ$(s_1, s_2)$ holds if and only if the history of $s_1$ is contained in that of $s_2$. The full proof is below.

## Complexity

Let $t$ be the number of nodes in the trees of the operands and $d$ their depth. Each of SPLIT, SUM, JOIN, FILL, GROW and LEQ visits each node a constant number of times, so each takes $O(t)$ time and $O(d)$ stack space. The size of a stamp depends on how ids were split and on how events are spread, not on the number of replicas that ever existed. When replicas retire by joining, their ids merge, and normalization removes the nodes that described them.

## Variants

- **[Version vectors](/version-vectors/) and [vector clocks](/vector-clocks/).** They use one counter per global replica name. They are simpler and faster when the set of replicas is fixed and known.
- **[Dotted version vectors](/dotted-version-vectors/).** They solve a different problem: a fixed set of servers act for many clients. ITC solve the problem of a changing set of replicas.
- **Version stamps.** An earlier design by Almeida, Baquero and Fonte for the same fork-join setting. ITC add counters, so they can also order events, not only replicas.

## When to use it

Use ITC when replicas are created and retired often and there is no cheap way to give them unique names: for example, mobile or peer-to-peer replicas that fork new copies, or short-lived workers. Each fork and join is local, so no coordination service is needed. If the set of replicas is fixed, a [version vector](/version-vectors/) is simpler. If only a total order that respects causality is needed, a [Lamport clock](/lamport-clocks/) is enough.

## Pitfalls

- **Events on an anonymous stamp.** A peek has the id $0$ and cannot record events. A receiver must join the peek into its own stamp first.
- **Losing an id.** If a replica crashes and its id is lost, that part of the interval can never be used again, and the trees keep the nodes for it. The ids of retired replicas must be joined back into a live stamp.
- **Joining overlapping ids.** SUM assumes disjoint ids. Joining a stamp with a copy of itself, for example a stamp that was duplicated instead of forked, breaks the uniqueness of event values.
- **Skipping normalization.** The LEQ rule of line L6 relies on normal form. On trees that are not normal, it can give a wrong answer.

## Implementations

## History

Paulo Sérgio Almeida, Carlos Baquero and Victor Fonte presented interval tree clocks at OPODIS 2008. They described the fork-event-join model, in which operations are local and identities are created by splitting, and they built the clock from two trees over the unit interval. Their earlier version stamps used the same model to track the identity of replicas without counters.

## References
