---
tag: Y6F20Y
kind: data-structure
slug: yata
name: YATA
aliases:
- Yet Another Transformation Approach
- Yjs algorithm
area: distributed/replication-and-crdts
level: advanced
summary: The sequence CRDT behind Yjs. Each item records its left and right origin, a remote item goes between them, and a conflict rule orders items in the same gap by client id.
implements: [crdt]
model: word-ram
complexity:
  vars: {N: "the number of items ever inserted, tombstones included"}
  time: {worst: O(N)}
  space: {extra: Θ(N)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [op-based-crdt, causal-broadcast, linked-list, tombstone]
see_also: [rga, woot, causal-tree, logoot, lseq, treedoc, collaborative-text-editing, operational-transformation]
sources:
  - paper: doi:10.1145/2957276.2957310
    title: Petru Nicolaescu, Kevin Jahns, Michael Derntl and Ralf Klamma, Near real-time peer-to-peer shared editing on extensible data types, GROUP 2016
    locator: pages 39 to 49, the YATA model with origin and right origin, the rules that order conflicting insertions, and the integration
  - url: https://github.com/yjs/yjs
    title: Kevin Jahns and contributors, Yjs, a CRDT framework for shared editing
    locator: the integrate method of the Item class in src/structs/Item.js
  - paper: doi:10.1145/3301419.3323972
    title: Martin Kleppmann, Victor B. F. Gomes, Dominic P. Mulligan and Alastair R. Beresford, Interleaving anomalies in collaborative text editors, PaPoC 2019
    locator: the interleaving anomaly for sequence CRDTs and the test of typing at the same place
---

YATA (Yet Another Transformation Approach) is the sequence [CRDT](/crdt/) of the Yjs library, given by Nicolaescu, Jahns, Derntl and Klamma in 2016. Each inserted item has a unique id (client, clock) and records two neighbours from the moment it was made: its origin, the item to its left, and its right origin, the item to its right. A remote item is placed somewhere between its two origins. When concurrent items already sit in that gap, a conflict rule decides the place: items with the same origin are ordered by client id, and an item whose origin lies inside a run of scanned items stays with that run. Deleted items stay as [tombstones](/tombstone/).

## In plain words

When you type a letter, the editor writes down the letter on your left and the letter on your right. On every other screen, the new letter must land somewhere between those two.

Often another person typed into the same gap at the same time. Then the letters in the gap must be sorted the same way everywhere. The rule is: letters that were typed right after the same left neighbour are sorted by the typist's number, smaller first. A letter that was typed after one of those letters travels with it, so a word typed by one person stays together.

Knowing both neighbours helps against mixing two people's words, also when someone types backwards.

## The abstract type

YATA implements a replicated list with updates INSERT$(i, x)$ and DELETE$(i)$ and the query READ. It is an [op-based CRDT](/op-based-crdt/).

**Model.** There are clients with distinct numeric ids. An item is delivered at every replica after its origin and its right origin; Yjs holds back items whose origins are missing. Deletes are delivered after the item they delete. Duplicates are ignored.

**Specification.** Replicas that have integrated the same items and deletes show the same list. A local INSERT$(i, x)$ makes $x$ the $i$-th visible element at its source, and DELETE$(i)$ hides the $i$-th one. Every item sits after its origin and before its right origin at every replica.

## Representation

A replica stores the items in one list, deleted items included. Each item has an id (client, clock), where clock counts the client's own inserts, an origin id, a right origin id, a value and a deleted flag. Yjs stores the list as a doubly [linked list](/linked-list/) of items, with an index from ids to items, and merges consecutive items of one client into one struct.

The YATA paper defines the order by rules on conflicting insertions: origin connections must not cross, the order is transitive, and among insertions with the same origin the one whose creator has the smaller id goes to the left. The loop below is the integrate function of Yjs, which implements these rules in one left-to-right scan.

## Operations

```pseudo id=main
INTEGRATE(x)                                          ▷ x has id, origin, right origin
L1  left ← the position of x.origin (or −1 for none)
L2  right ← the position of x.rightOrigin (or the end)
    beforeOrigin ← ∅;  conflicting ← ∅;  k ← left + 1
L3  while k < right do
        o ← list[k];  add o to beforeOrigin and to conflicting
L4      if o.origin = x.origin then
L5          if o.client < x.client then left ← k;  conflicting ← ∅
L6          else if o.rightOrigin = x.rightOrigin then break
        else if o.origin ∈ beforeOrigin then
L7          if o.origin ∉ conflicting then
L8              left ← k;  conflicting ← ∅
        else
L9          break
        k ← k + 1
L10 put x at position left + 1
```

**The scan.** The loop walks the gap between the two origins. An item with the same origin and a smaller client id (line L5) must stay to the left of $x$, and so must everything scanned so far: $\mathit{left}$ moves past it. An item with the same origin, a larger client id and the same right origin (line L6) must go to the right of $x$, and the scan stops. An item whose origin was scanned (lines L7 and L8) was typed after something in the gap. If its origin is not among the items still in conflict, it belongs to a run that is already settled to the left, so $\mathit{left}$ moves past it. An item whose origin lies outside the gap (line L9) ends the scan.

**Local insert.** The source takes as origin the visible element $i - 1$ and as right origin the item right after it in the list, live or deleted. The gap is empty, so the item goes right after its origin, at visible index $i$. **Delete.** Mark the item as deleted and broadcast its id.

## Example

Three clients 1, 2 and 3 share "H i", typed by client 1 with ids $(1,1)$ and $(1,2)$. At the same time each types a letter between H and i: client 1 types e with id $(1,3)$, client 2 types o with id $(2,1)$, client 3 types u with id $(3,1)$. All three have origin H and right origin i.

| replica | delivery order | after the first remote item | after the second |
| --- | --- | --- | --- |
| client 1 | o, then u | H e o i: e has client 1 < 2, so left moves past e | H e o u i: e and o have smaller client ids |
| client 2 | u, then e | H o u i | H e o u i: at o, client 2 > 1 and the right origins match, so stop |
| client 3 | e, then o | H e u i | H e o u i: past e, stop at u |

All replicas show H e o u i: the items of one gap are in client id order.

**Typing at the same place.** Client 1 types "abc" and client 2 types "xyz" at the start of an empty list, both forward. All replicas show abcxyz. If each types its word from back to front (c, then b before it, then a), the result is again abcxyz. The right origin keeps each backwards-typed word together, which is the case where [RGA](/rga/) gives xaybzc.

## Correctness

Three properties are proved in [the correctness proof](proofs/correctness.md). First, every item sits after its origin and before its right origin at every replica, because the insert position stays inside the gap. Second, a local insert lands at its visible index, because its gap is empty at the source. Third, items that were inserted concurrently into the same gap, with the same origin and right origin, end in client id order at every replica, whatever the delivery order; this is the conflict rule. Convergence in general, with runs typed after items in the gap, rests on the ordering rules of the YATA paper and on the integrate loop of Yjs; the proof file does not give a general argument for it. The tests check it on seeded runs with 2 to 5 replicas and up to 300 operations.

## Complexity

Let $N$ be the number of items, tombstones included.

| operation | time | messages |
| --- | --- | --- |
| integrate a remote item | $O(1)$ expected to find the origins with an index, plus the scanned gap, $O(N)$ worst | none |
| local insert or delete at index $i$ | $O(N)$ by walking; Yjs caches recent positions | one item with three ids |
| delete | $O(1)$ expected | one id |
| READ | $\Theta(N)$ | none |

Each item carries three ids. Yjs packs consecutive items of one client into one struct and encodes deletes as ranges, so typical documents need far less than three ids per character.

## Variants

- **Yjs.** The production form. It adds types for maps, XML and rich text, merges runs of items, keeps deletes in a compact delete set, and can garbage-collect the content of deleted items while keeping their ids.
- **Fugue and its tree form.** Later work by Weidner, Gentle and Kleppmann relates this family of algorithms to a tree with left and right children and studies the cases where interleaving remains.
- **How YATA differs from the other sequence CRDTs.** Like [WOOT](/woot/), it records both neighbours, but it integrates with one forward scan and a simple rule instead of WOOT's recursion. [RGA](/rga/) and the [causal tree](/causal-tree/) record only the left neighbour and order siblings by timestamp. [Logoot](/logoot/) and [LSEQ](/lseq/) use dense identifiers and no tombstones.

## When to use it

Use YATA, in practice through Yjs, for real-time collaborative editing of text and rich documents in browsers and peer-to-peer settings. It has low overhead per character after run merging and keeps words typed concurrently at one place apart in the common cases.

## Pitfalls

- **Taking the next visible item as the right origin.** The right origin must be the next item in the list, deleted or not. Skipping a tombstone gives a gap that other replicas do not share.
- **Integrating before the origins arrive.** An item whose origin or right origin is missing has no gap. Hold it back.
- **Changing the tie rule.** All replicas must compare client ids the same way. A client that reuses another client's id produces equal ids and breaks the scan.
- **Assuming no interleaving at all.** The rule keeps runs typed forward or backward together, but sequence CRDTs in general can still mix concurrent edits in some patterns.

## Implementations

The Python class follows the main block with `# @line` markers for L1 to L10, after the integrate method of Yjs. It keeps items in a Python list, so positions cost linear time. The tests run the example in all delivery orders shown, the forward and backward typing cases, and seeded runs with 2 to 5 replicas and up to 300 operations, where items arrive after their origins. They check that replicas converge, that local edits land at their index, that each item sits between its origins, and that one order explains every replica's list.

## History

Nicolaescu, Jahns, Derntl and Klamma presented YATA at GROUP 2016 as the model behind Yjs, a framework that Kevin Jahns had started for shared editing on extensible data types. Yjs became a widely used CRDT library for collaborative editors.

## References
