---
tag: KP38B4
kind: theorem
slug: dsst-persistence-theorem
name: Driscoll-Sarnak-Sleator-Tarjan persistence theorem
aliases:
- DSST theorem
- node-copying theorem
- full persistence theorem
area: data-structures/persistent-structures
level: advanced
summary: A linked structure of bounded in-degree can be made partially or fully persistent with O(1) amortized time and space per update step and O(1) time per access step.
model: pointer-machine
prereqs: [partial-persistence, full-persistence, pointer-machine, amortized-cost]
see_also: [node-copying, fat-node, path-copying, persistent-red-black-tree, sarnak-tarjan-point-location, confluent-persistence, fully-persistent-array, persistent-binary-search-tree]
sources:
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: pages 86 to 124, the section on partial persistence (fat nodes and node copying, with the amortized analysis) and the section on full persistence (the version list and node splitting)
  - paper: doi:10.1145/6138.6151
    title: Neil Sarnak and Robert E. Tarjan, Planar point location using persistent search trees, Communications of the ACM 29(7), 1986
    locator: pages 669 to 679 (node copying for a search tree, with O(1) amortized space per update)
  - paper: doi:10.1145/28395.28434
    title: Paul F. Dietz and Daniel D. Sleator, Two algorithms for maintaining order in a list, Proceedings of the 19th ACM Symposium on Theory of Computing (STOC 1987)
    locator: pages 365 to 372 (order maintenance with O(1) time per comparison, used for the version list)
  - paper: doi:10.7146/brics.v1i35.21608
    title: Gerth Stølting Brodal, Partially persistent data structures of bounded degree with constant update time, BRICS Report Series RS-94-35, 1994
    locator: the main theorem (worst-case O(1) time and space per update step for partial persistence)
---

The persistence theorem of Driscoll, Sarnak, Sleator and Tarjan says that any linked data structure whose nodes have a constant number of fields and a constant in-degree can be made [partially persistent](/partial-persistence/), and also [fully persistent](/full-persistence/), at a constant cost: each access step takes $O(1)$ time in the worst case, and each update step takes $O(1)$ amortized time and space. The partial case uses [node copying](/node-copying/): each node gets a few spare fields for changes, and is copied only when they are full. The full case uses node splitting over a list of versions kept in preorder. The theorem turns the [red-black tree](/red-black-tree/) into a persistent search tree with $O(1)$ amortized space per update, which gives [planar point location](/sarnak-tarjan-point-location/) in linear space.

## Statement

The model is the [pointer machine](/pointer-machine/). A **linked data structure** is a set of nodes, each with at most $d$ fields, and a constant number of entry pointers. A field holds a datum, a pointer to a node, or nil. An **access operation** starts at an entry pointer and does access steps, each of which reads one field of a node that it has reached. An **update operation** may also do update steps, each of which creates a node or changes one field of a node. The **in-degree** of a node is the number of fields and entry pointers that point to it. We assume that every state of the structure, including the states inside an update operation, has in-degree at most $p$. Both $d$ and $p$ are constants.

**Theorem.** Let a linked data structure with constants $d$ and $p$ start from a version $D_0$ of $O(1)$ nodes.

1. **(Partial persistence.)** There is a partially persistent representation in which an access step in any version takes $O(1)$ time in the worst case, and any sequence of update operations with $U$ update steps in total takes $O(U)$ time and $O(U)$ space. So each update step costs $O(1)$ amortized time and space.
2. **(Full persistence.)** There is a fully persistent representation with the same bounds: $O(1)$ worst-case time per access step, and $O(1)$ amortized time and space per update step.

The constants in the bounds depend on $d$ and $p$. The time of an operation is the time of the ephemeral operation, step for step, times a constant, plus $O(1)$ to find the entry pointers of the version.

## In plain words

Take any structure of boxes and arrows in which few arrows point to each box. Give every box a few empty slots. When the structure changes, write the change in a slot of the box, stamped with the version number, instead of erasing the old value. To read a box as it was at some time, look at the slots with stamps up to that time. When a box has no free slot, make a fresh copy with the newest values and tell the few boxes that point to it to point to the copy, which again uses their slots. Copies are rare, because a box is copied only after its slots are full. So every change costs a constant amount of work on average, and reads stay as fast as before.

## Proof

We prove part 1 in full. For part 2 we describe the construction of the paper and the place of the proof.

**The representation for part 1.** Let $k \ge p$ be a constant. A *persistent node* $x$ has $d$ original fields, $k$ modification slots, and a set $\text{back}(x)$. A filled slot holds a triple $(f, s, v)$: field $f$ has the value $v$ from version $s$ on. Slots are filled in order. For a version $i$, the value of field $f$ of $x$ in version $i$, written $\text{val}_i(x, f)$, is the value $v$ of the last filled slot $(f, s, v)$ with $s \le i$, or the original field $f$ if there is none. An array $E$ holds, for each version $i$, its entry pointers $E[i]$. Let $t$ be the number of the version under construction. A persistent node is *live* if it was made by the current version or if no copy of it has been made. The set $\text{back}(x)$ of a live node $x$ lists the pairs $(z, g)$ with $z$ live and $\text{val}_t(z, g) = x$; it is changed in place and is not versioned.

**Access.** An access in version $i$ starts at $E[i]$ and reads a field $f$ of a node $x$ as $\text{val}_i(x, f)$. This scans at most $k$ slots, so an access step costs $O(k) = O(1)$.

**Update.** An update operation that makes version $t$ first sets $E[t] \leftarrow E[t - 1]$. It then runs the ephemeral update on version $t$, reading with $\text{val}_t$. A node creation makes a live node whose original fields hold the initial values, with empty slots. The change of field $f$ of node $y$ to the value $v$ calls CHANGE$(y, f, v)$:

- If $y$ has a free slot, write $(f, t, v)$ into it. This is a *write*.
- Otherwise make a *copy*: a new live node $y'$ whose original fields hold $\text{val}_t(y, g)$ for each $g \ne f$ and $v$ for $f$, with each pointer to $y$ in these fields replaced by $y'$, and with empty slots. For each node $z$ that a field of $y'$ points to, replace the pairs $(y, g)$ in $\text{back}(z)$ by $(y', g)$. Replace $y$ by $y'$ in $E[t]$. Then, for each pair $(z, g) \in \text{back}(y)$ with $z \ne y$, call CHANGE$(z, g, y')$. The node $y$ is no longer live.

Each change of a pointer field also updates the two back sets concerned, in $O(p)$ time.

**Old versions do not change.** Let $i < t$. An update of version $t$ writes slots stamped $t > i$, which $\text{val}_i$ ignores, and fills original fields only in new nodes. A new node is reached in version $i$ only through a field or an entry pointer, but the pointers to it are written in new nodes, in slots stamped $t$, or in $E[t]$. So no value $\text{val}_i(x, f)$ and no $E[i]$ changes, and every version made before $t$ reads as it did when it was made.

**The new version is correct.** We show the invariant: there is a map $\phi$ from the nodes of the ephemeral state $D$ of version $t$ onto the live nodes, such that $E[t]$ is $\phi$ of the ephemeral entry pointers, and for every node $a$ of $D$ and field $f$, $\text{val}_t(\phi(a), f)$ is the datum $a.f$, or $\phi(b)$ when $a.f$ points to $b$. Also, $\text{back}$ is as defined above. At the start of the update operation, $\phi$ is the map of version $t - 1$, because no slot has the stamp $t$ yet. A node creation extends $\phi$. A write $(f, t, v)$ into $y = \phi(a)$ is the last slot with a stamp at most $t$, so it sets $\text{val}_t(y, f) = v$ and leaves the other fields alone. A copy of $y = \phi(a)$ sets $\phi(a) = y'$. The node $y'$ has the values $\text{val}_t(y, \cdot)$ with $f$ changed, and its pointers to $y$ point to $y'$. Every other pointer to $y$ in version $t$ is either in $E[t]$, which is fixed, or a field $g$ of a live node $z \ne y$ with $\text{val}_t(z, g) = y$, which is in $\text{back}(y)$ and is fixed by the recursive call. So after all the calls of one change return, the invariant holds with the change applied.

**Cost.** Count the calls of CHANGE during a sequence of update operations with $U$ update steps. Let $u \le U$ be the number of field changes of the ephemeral updates, $C$ the number of copies and $W$ the number of writes so far. Each call does one write or one copy when it starts, and each call is either one of the $u$ changes or one of the at most $p$ calls made by a copy, because $|\text{back}(y)| \le p$. So at every moment
$$W + C \le u + pC.$$
A node is copied only when its $k$ slots are full, it is copied at most once, since it is not live afterwards, and its slots were filled by writes. So $W \ge kC$. Together, $kC + C \le u + pC$, so $(k - p + 1) C \le u$, and since $k \ge p$,
$$C \le u, \qquad W + C \le u + pC \le (p + 1) u.$$
In particular each update operation makes a finite number of calls and stops. A write costs $O(p)$ time, a copy $O(d + k + dp)$ time and $O(d + k + p)$ space, and a node creation $O(d + k + p)$ time and space. So the total time and space of all update steps is $O((p + 1)(d + k + dp) U) = O(U)$, and the array $E$ adds $O(1)$ per version. This proves part 1.

**Part 2.** For full persistence, the versions are kept in a *version list*, a preorder of the [version tree](/version-tree/), in an order-maintenance structure of Dietz and Sleator that inserts a version and compares two versions in $O(1)$ time. A slot stamped with a version applies to that version and to the versions after it in the list that are its descendants. An update of version $i$ that makes $t$ writes two slots: one stamped $t$ with the new value, and one stamped with the version after the subtree of $t$ in the list, which restores the old value for the versions that follow. When a node is full, it is not copied but split into two nodes, each with half of the slots, which cover two consecutive ranges of the version list; the pointers to the node from the versions of the second range are then fixed by recursive changes. A potential argument on the number of free slots, with $\Theta(d + p)$ slots per node, bounds the work of the splits by $O(1)$ amortized per update step. The details are in the section on full persistence of Driscoll, Sarnak, Sleator and Tarjan (1989). $\blacksquare$

## Consequences

- **Persistent search trees.** An insertion or deletion in a [red-black tree](/red-black-tree/) changes $O(1)$ fields amortized, without parent pointers. By part 1, a partially persistent red-black tree uses $O(1)$ amortized space per update and $O(\log n)$ time per search in any version. This is the structure of Sarnak and Tarjan; see [persistent red-black tree](/persistent-red-black-tree/).
- **Planar point location.** With the persistent tree over a plane sweep, [Sarnak-Tarjan point location](/sarnak-tarjan-point-location/) uses $O(n)$ space and answers a query in $O(\log n)$ time.
- **A general compiler for persistence.** Many linked structures, such as lists, [binary search trees](/binary-search-tree/) and [heaps](/heap/) with bounded in-degree, become persistent with no change to their code other than the reads and writes, and with a constant factor of slowdown.
- **Comparison with other methods.** [Path copying](/path-copying/) costs $O(\log n)$ space per update in a balanced tree, and the [fat node](/fat-node/) method costs $O(\log m)$ time per access step. The theorem gets $O(1)$ for both, for structures of bounded in-degree.

## Tightness

- **The constants.** $O(1)$ per step cannot be improved beyond the constant factor, since the ephemeral step itself costs a constant.
- **Amortized versus worst case.** The bound on update steps in part 1 is amortized: a single change can start a cascade of copies. Brodal (1994) showed that for partial persistence the update steps can be made $O(1)$ in the worst case.
- **Bounded in-degree.** The proof uses $|\text{back}(y)| \le p$. A node with in-degree $\Theta(n)$ makes a copy cost $\Theta(n)$, and node copying is not efficient for such structures. The fat node method has no such condition but pays $O(\log m)$ per access.
- **Arrays.** An array allows access by index, which the pointer machine with constant in-degree does not model. For a [fully persistent array](/fully-persistent-array/) of Dietz, an access costs $O(\log \log m)$, and a matching lower bound holds in the [cell-probe model](/cell-probe-model/), so the constant-overhead result does not extend to arrays.
- **Melds.** The theorem does not cover operations that combine two versions; see [confluent persistence](/confluent-persistence/).

## History

Sarnak and Tarjan (1986) used node copying for search trees to get linear-space planar point location. Driscoll, Sarnak, Sleator and Tarjan presented the general theorem, with the fat node method, node copying and node splitting, at STOC 1986, and the journal version appeared in 1989. The order-maintenance structure of Dietz and Sleator (1987) gives the $O(1)$ version comparisons that part 2 needs. Brodal (1994) removed the amortization for partial persistence.

## References
