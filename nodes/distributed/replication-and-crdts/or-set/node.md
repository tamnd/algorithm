---
tag: DDH0TH
kind: data-structure
slug: or-set
name: OR-Set
aliases:
- observed-remove set
- add-wins set
area: distributed/replication-and-crdts
level: core
summary: A replicated set where each add makes a unique tag and a remove deletes only the tags it has seen. A concurrent add wins, and elements can be added again after a remove.
implements: [crdt]
model: word-ram
complexity:
  vars: {k: the number of tags of the element at the source}
  time: {worst: Θ(k)}
  space: {extra: Θ(k)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [g-set, op-based-crdt, causal-broadcast, version-vectors]
see_also: [two-phase-set, lww-element-set, g-set, tombstone, dotted-version-vectors, delta-state-crdt, crdt, causal-broadcast]
sources:
  - paper: doi:10.1007/978-3-642-24550-3_29
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, Conflict-free replicated data types, SSS 2011, LNCS 6976
    locator: pages 386 to 400, the observed-remove set
  - url: https://inria.hal.science/inria-00555588
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, A comprehensive study of convergent and commutative replicated data types, INRIA RR-7506, 2011
    locator: Section 3.3.5 and Specification 15 (op-based OR-Set with unique tags and causal delivery)
  - url: https://arxiv.org/abs/1210.3368
    title: Annette Bieniusa, Marek Zawirski, Nuno Preguiça, Marc Shapiro, Carlos Baquero, Valter Balegas and Sérgio Duarte, An optimized conflict-free replicated set, arXiv 1210.3368 and INRIA RR-8083, 2012
    locator: the add-wins specification and the optimized state-based OR-Set with a version vector and no tombstones
  - paper: doi:10.1016/j.jpdc.2017.08.003
    title: Paulo Sérgio Almeida, Ali Shoker and Carlos Baquero, Delta state replicated data types, Journal of Parallel and Distributed Computing 111, 2018
    locator: pages 162 to 173, the add-wins set over a causal context of dots
---

An OR-Set (observed-remove set) is a replicated set with add, remove and lookup, in which an add and a concurrent remove of the same element leave the element in the set. Each add makes a fresh unique tag and stores the pair (element, tag). A remove collects the tags of the element that its source can see and deletes only those pairs at every replica. An add that the remove did not see has a tag outside that collection, so it survives: add wins. Unlike the [2P-Set](/two-phase-set/), an element can be added again after a remove, and unlike the [LWW-Element-Set](/lww-element-set/), no clock decides. This page gives the op-based form of Shapiro et al. (2011) and the optimized state-based form of Bieniusa et al. (2012), which needs no [tombstones](/tombstone/).

## In plain words

Each time a server puts an item in, it attaches a new, unique sticker to that copy of the item. When a server takes an item out, it removes only the stickers that it can see at that moment.

Suppose one server takes out "milk" while another, at the same time, puts "milk" in again. The second "milk" has a sticker that the first server never saw, so the remove does not touch it, and after the servers talk, "milk" is still there. An item is in the set while at least one of its stickers is left. Putting an item back in after a remove simply adds a new sticker.

## The abstract type

The OR-Set implements a replicated set with updates ADD and REMOVE and the query LOOKUP, with the add-wins rule for conflicts.

**Model.** There are $n$ replicas with ids $1, \ldots, n$. The system is asynchronous. For the op-based form, operations are sent by [causal broadcast](/causal-broadcast/): each operation is delivered exactly once at every replica, after every operation that was delivered at its source before it was made. For the state-based form, channels may lose, duplicate and reorder states.

**Specification (add-wins).** Let $C_i$ be the causal history of replica $i$, ordered by [happened-before](/happened-before/). REMOVE$(e)$ has the precondition LOOKUP$(e)$ at its source. LOOKUP$(e)$ at $i$ returns true exactly when $C_i$ holds an ADD$(e)$ that is not in the causal past of any REMOVE$(e)$ in $C_i$. So a remove cancels the adds it has seen, and an add concurrent with every remove of $e$ keeps $e$ in the set.

## Representation

**Op-based form.** A replica stores a set $S$ of pairs (element, tag), where a tag is a pair (replica id, counter) and so is unique. The invariant is that $S$ holds the pairs of the adds in $C_i$ whose tags no remove in $C_i$ has collected.

**Optimized state-based form.** A replica stores a set $E$ of triples $(e, c, j)$ and a [version vector](/version-vectors/) $V$. The triple means "the $c$-th add of replica $j$ added $e$", and $(j, c)$ is called a dot. $V[j]$ is the number of adds of replica $j$ that the replica has seen. A dot $(j, c)$ with $c \le V[j]$ that is not in $E$ has been removed, so no tombstone is needed. $E$ keeps at most one dot per element and replica: the latest.

## Operations

The op-based OR-Set, as in Specification 15 of the INRIA report. PREPARE runs at the source and makes the message; EFFECT runs at every replica on delivery, the source included.

```pseudo id=main
CREATE(i)
L1  S ← ∅;  counter ← 0

LOOKUP(e)
L2  return some (e, t) ∈ S

ADD(e)  at the source:
L3      counter ← counter + 1;  t ← (i, counter);  broadcast add(e, {t})
REMOVE(e)  at the source, with precondition LOOKUP(e):
L4      R ← {t : (e, t) ∈ S};  broadcast remove(e, R)   ▷ the observed tags

on delivery of add(e, {t}):
L5      S ← S ∪ {(e, t)}
on delivery of remove(e, R):
L6      S ← S ∖ {(e, t) : t ∈ R}
```

Line L3 makes a tag that no other add has. Line L4 is the heart of the design: the remove names exactly the tags its source has observed. Causal delivery puts every add whose tag is in $R$ before the remove, so line L6 never deletes a pair that has not arrived yet.

The optimized state-based OR-Set of Bieniusa et al.:

```pseudo
ADD(e)  at replica i
1  V[i] ← V[i] + 1;  c ← V[i]
2  E ← (E ∖ {(e, c', i) ∈ E}) ∪ {(e, c, i)}            ▷ the new dot replaces the older own dot of e
REMOVE(e)
3  E ← E ∖ {(e, c, j) ∈ E}                              ▷ the removed dots stay covered by V
MERGE(E', V')
4  M  ← E ∩ E'
5  M₁ ← {(e, c, j) ∈ E ∖ E' : c > V'[j]}               ▷ the other side has not seen the dot yet
6  M₂ ← {(e, c, j) ∈ E' ∖ E : c > V[j]}                ▷ this side has not seen the dot yet
7  U ← M ∪ M₁ ∪ M₂
8  E ← U without each (e, c, j) for which U has (e, c', j) with c' > c
9  V ← max(V, V')                                        ▷ entrywise
```

A dot that is on one side only was removed on the other side if that side's vector covers it (lines 5 and 6), and was not yet seen there otherwise.

## Example

**Op-based.** Two replicas $a$ (id 0) and $b$ (id 1).

| step | event | $S$ at $a$ | $S$ at $b$ |
| --- | --- | --- | --- |
| 1 | $a$ adds $x$ with tag $(0,1)$; both deliver it | $\{(x, (0,1))\}$ | $\{(x, (0,1))\}$ |
| 2 | $b$ removes $x$ with $R = \{(0,1)\}$ | same | $\varnothing$ |
| 3 | $a$ adds $x$ with tag $(0,2)$, concurrently | $\{(x,(0,1)), (x,(0,2))\}$ | $\varnothing$ |
| 4 | $a$ delivers the remove; $b$ delivers the add | $\{(x, (0,2))\}$ | $\{(x, (0,2))\}$ |
| 5 | $a$ removes $x$ with $R = \{(0,2)\}$; both deliver | $\varnothing$ | $\varnothing$ |
| 6 | $a$ adds $x$ with tag $(0,3)$ | $\{(x, (0,3))\}$ | $\varnothing$ until delivery |

In step 4 both replicas have $x$: the remove did not see tag $(0,2)$. In step 6, $x$ is back, which a 2P-Set does not allow.

**Optimized.** The same story with states written as $E \mid V$. $a$ adds $x$: $\{(x,1,0)\} \mid (1,0)$. $b$ merges it and removes $x$: $\varnothing \mid (1,0)$. $a$ adds $x$ again: the new dot replaces the old one, giving $\{(x,2,0)\} \mid (2,0)$. When $a$ merges $b$, the dot $(x,2,0)$ is on $a$'s side only and $2 > V_b[0] = 1$, so $b$ has not seen it, and it stays. Both end at $\{(x,2,0)\} \mid (2,0)$. If $b$ now removes $x$ and $a$ merges, the dot is on $a$'s side only and $2 \le V_b[0] = 2$, so $b$ has seen and removed it, and $a$ drops it.

## Correctness

For the op-based form, the invariant is that $S_i$ holds $(e, t)$ exactly when the add with tag $t$ is in $C_i$ and no remove in $C_i$ collected $t$. A remove collects the tag of an add exactly when the add is in its causal past and still visible at its source, and an add hidden at the source was collected by an earlier remove, which is also in $C_i$. So "some tag of $e$ is not collected" is the add-wins specification. Concurrent operations commute: a concurrent add and remove touch different pairs, because a remove only names tags of adds it has seen. For the optimized form, the invariant is that $E_i$ holds the latest dot of each element and replica among the adds in $C_i$ that no remove in $C_i$ has seen, and $V_i$ counts the adds per replica; a case split on where a dot occurs shows that MERGE computes the state of the union of the histories. The full proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | op-based | optimized state-based |
| --- | --- | --- |
| ADD | $O(1)$ | $O(1)$ expected with an index by element |
| REMOVE of an element with $k$ tags | $O(k)$, message of $k$ tags | $O(k)$, $k \le n$ |
| LOOKUP | $O(1)$ expected with an index | $O(1)$ expected |
| MERGE | none | $O(\lvert E \rvert + \lvert E' \rvert + n)$ expected |

The op-based form keeps no tombstones, because causal delivery makes a remove arrive after its adds, but it needs exactly-once causal broadcast, and its state holds one tag per add that is still visible. The first state-based OR-Set kept every removed tag as a tombstone. The optimized form stores at most $n$ dots per element plus one vector of $n$ counters, and removed elements cost nothing.

## Variants

- **Remove-wins set.** The dual rule: a remove beats every concurrent add. It needs the remove to be recorded, for example as tombstones or as a dot of its own.
- **Delta-state add-wins set.** Almeida, Shoker and Baquero write the optimized OR-Set as a dot store with a causal context, and ship deltas of it. Their causal context is a set of dots, compressed to a version vector plus a few extra dots.
- **OR-Map.** A map whose keys behave like an OR-Set and whose values are CRDTs, as in Riak and Automerge.
- **[2P-Set](/two-phase-set/) and [LWW-Element-Set](/lww-element-set/).** Simpler sets with remove-wins and timestamp rules.

## When to use it

Use an OR-Set when a set must allow add, remove and re-add, and a concurrent add should not be lost: shopping carts, tag sets, group membership, the keys of a map. Use the optimized state-based form when the network does not give causal delivery or when tombstones are too costly.

## Pitfalls

- **Op-based without causal delivery.** If a remove arrives before the add whose tag it names, line L6 deletes nothing, and the late add then puts the pair back for good. If an add arrives twice, the pair comes back after it was removed. Use causal broadcast with deduplication.
- **Reusing tags.** A tag must name one add. A replica that restarts with a fresh counter and an old id makes tags that collide with old ones.
- **Expecting remove to win.** A user who removes an item while another user adds it sees it come back. That is the specified behaviour.
- **Optimized merge with stale vectors.** The vector must count exactly the adds whose dots the replica has processed. A replica that advances $V$ without merging the matching $E$ makes later merges drop live dots.

## Implementations

The Python module has both forms. The op-based class follows the main block with `# @line` markers for L1 to L6; the optimized class follows the second block. The tests run the example, check the add-wins specification against an oracle that computes the causal past of each operation, run seeded runs with causal delivery and deduplication for the op-based form and with duplicated and reordered states for the optimized form, and check the semilattice laws of the optimized merge on reachable states.

## History

Shapiro, Preguiça, Baquero and Zawirski gave the OR-Set in 2011, in the SSS paper and as Specification 15 of the INRIA report, with unique tags and causal delivery. Bieniusa, Zawirski, Preguiça, Shapiro, Baquero, Balegas and Duarte (2012) stated the add-wins specification precisely and gave the optimized form with a version vector and no tombstones. Almeida, Shoker and Baquero (2018) recast it as a delta-state CRDT over dots.

## References
