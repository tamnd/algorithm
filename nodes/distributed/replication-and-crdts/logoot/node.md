---
tag: AHQMT3
kind: data-structure
slug: logoot
name: Logoot
aliases:
- Logoot sequence CRDT
area: distributed/replication-and-crdts
level: advanced
summary: A sequence CRDT that gives each element a unique position from a dense order, a list of (digit, site, clock) triples. The document is the elements sorted by position, with no tombstones.
implements: [crdt]
model: word-ram
complexity:
  vars: {N: "the number of elements in the document", L: "the length of the longest position"}
  time: {worst: O(L log N)}
  space: {extra: Θ(N L)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [op-based-crdt, causal-broadcast, lexicographic-order]
see_also: [lseq, treedoc, rga, woot, yata, causal-tree, collaborative-text-editing, operational-transformation]
sources:
  - paper: doi:10.1109/ICDCS.2009.75
    title: Stéphane Weiss, Pascal Urso and Pascal Molli, Logoot, a scalable optimistic replication algorithm for collaborative editing on P2P networks, ICDCS 2009
    locator: pages 404 to 412, line identifiers as lists of identifiers, the dense total order, and the generation of positions between two lines
  - paper: doi:10.1109/TPDS.2009.173
    title: Stéphane Weiss, Pascal Urso and Pascal Molli, Logoot-Undo, distributed collaborative editing system on P2P networks, IEEE Transactions on Parallel and Distributed Systems 21(8), 2010
    locator: pages 1162 to 1174, identifiers as triples of digit, site and clock, the base, and the boundary strategy for allocation
  - paper: doi:10.1145/2494266.2494278
    title: Brice Nédelec, Pascal Molli, Achour Mostefaoui and Emmanuel Desmontils, LSEQ, an adaptive structure for sequences in distributed collaborative editing, DocEng 2013
    locator: pages 37 to 46, the growth of Logoot identifiers when editing is not random, and the comparison with LSEQ
  - paper: doi:10.1145/3301419.3323972
    title: Martin Kleppmann, Victor B. F. Gomes, Dominic P. Mulligan and Alastair R. Beresford, Interleaving anomalies in collaborative text editors, PaPoC 2019
    locator: the example showing that Logoot and LSEQ can interleave text typed concurrently at one place
---

Logoot is a sequence [CRDT](/crdt/) for collaborative text, given by Weiss, Urso and Molli in 2009. Each element gets a position: a list of triples (digit, site, clock), compared in [lexicographic order](/lexicographic-order/). These lists form a dense [total order](/total-order/): between any two positions there is room for a new one, at the price of a longer list. The document is the set of elements sorted by position. To insert, a replica makes a new position between the positions of the two neighbours, and other replicas only have to put it in sorted order. A delete removes the element, so Logoot needs no [tombstones](/tombstone/). The price is that positions can grow long, linearly in the number of inserts for some editing patterns.

## In plain words

Think of the page numbers in a book where you can always add a page between two others. Between page 7 and page 13 you can add page 11. Between page 7 and page 8 there is no whole number free, so you add page 7.5, which is "7, then 5" one level down.

Logoot gives every letter such a number, written as a list. To insert a letter, you pick a number between the numbers of its two neighbours. Each number also holds the typist's id and a counter, so two typists never pick the same one. Every screen sorts the letters by number, so all screens agree.

A deleted letter is simply removed, because no one needs its number any more.

## The abstract type

Logoot implements a replicated list with updates INSERT$(i, x)$ and DELETE$(i)$ and the query READ. It is an [op-based CRDT](/op-based-crdt/).

**Model.** There are sites with distinct numeric ids. Each operation is delivered once at every replica, in an order consistent with [causal broadcast](/causal-broadcast/); in particular a delete arrives after the insert of its element.

**Specification.** Replicas that have run the same operations show the same list. A local INSERT$(i, x)$ makes $x$ the $i$-th element at its source, and DELETE$(i)$ removes the $i$-th element. The relative order of two elements never changes.

## Representation

A position is a list of triples $(d, s, c)$ with a digit $0 \le d < \mathit{base}$, a site id $s$ and a clock value $c$. Triples are compared as tuples, and positions as lists of triples, so a proper prefix comes first. The start of the document is the empty list, and the end is a mark $\top$ above all positions. Each replica keeps a site id, a clock, and the pairs (position, value) in a sorted structure, such as a [balanced binary search tree](/balanced-binary-search-tree/), with a map from positions to values. Two parameters shape allocation: the $\mathit{base}$, the number of digits per level, and the $\mathit{boundary}$, the largest step from the left neighbour.

Every position ends with a triple whose digit is at least 1. This invariant makes sure that there is room to the left of every position.

## Operations

```pseudo id=main
ALLOC(p, q)                                           ▷ a position strictly between p and q
    out ← [];  bound ← (q ≠ ⊤);  i ← 0                ▷ bound: out is a prefix of q
    loop
L1      pd ← the digit of p[i], or 0 if p has run out
L2      qd ← the digit of q[i] if bound, else base
L3      if qd − pd ≥ 2 then                           ▷ a free digit at this level
L4          step ← min(boundary, qd − pd − 1)
L5          return out + [(pd + RANDOM(1, step), site, clock)]
L6      if i < |p| then append p[i] to out;  bound ← bound and p[i] = q[i]
L7      else if qd = 0 then append q[i] to out
L8      else append (0, site, clock) to out;  bound ← false
L9      i ← i + 1
```

Line L5 is the boundary strategy: the new digit is at most $\mathit{boundary}$ above the digit of $p$, which leaves room for later inserts to the right of the new element. Line L6 copies the triple of $p$ when this level has no room. Lines L7 and L8 handle a $p$ that is a prefix of $q$: they follow $q$ while its digit is 0 and step one level down below a digit 1.

**Local insert.** Let $p$ be the position of element $i - 1$, or the empty list, and $q$ the position of element $i$, or $\top$. Increase the clock, set $x \leftarrow \mathrm{ALLOC}(p, q)$, add $(x, v)$, and broadcast it. **Local delete.** Remove element $i$ and broadcast its position. **Remote operations.** Add the pair, or remove the position, in sorted order.

## Example

Base 100, boundary 10, two sites 1 and 2. Site 1 types "Hi"; the positions are made by ALLOC and sent to site 2.

| step | site | operation | ALLOC | position |
| --- | --- | --- | --- | --- |
| 1 | 1 | insert H at 0 | between the start and $\top$: $pd = 0$, $qd = 100$, step 10 | $\langle(7,1,1)\rangle$ |
| 2 | 1 | insert i at 1 | between $\langle(7,1,1)\rangle$ and $\top$ | $\langle(13,1,2)\rangle$ |
| 3 | 1 | insert e at 1 | between 7 and 13: step $\min(10, 5) = 5$ | $\langle(11,1,3)\rangle$ |
| 3 | 2 | insert o at 1, at the same time | between 7 and 13 | $\langle(12,2,1)\rangle$ |
| 4 | both | apply the other's insert | sort | H e o i at both sites |

**Going one level down.** Between $\langle(5,1,1)\rangle$ and $\langle(6,2,1)\rangle$ no digit is free. Line L6 copies $(5,1,1)$, and since the triples differ, $\mathit{bound}$ becomes false. At level 2, $pd = 0$ and $qd = 100$, so line L5 gives for example $\langle(5,1,1),(4,3,7)\rangle$, which lies between the two.

**Interleaving.** If site 1 types "abcd" and site 2 types "wxyz" at the same place at the same time, each new letter goes at a random digit near the left neighbour, so the merged text can mix the two words, for example "awbxcdyz". Kleppmann et al. (2019) showed this anomaly for Logoot and LSEQ.

## Correctness

[The correctness proof](proofs/correctness.md) shows four things. ALLOC stops and returns a position strictly between $p$ and $q$ that again ends with a digit of at least 1, and it is at most one level longer than the longer of $p$ and $q$. Positions are unique, because the last triple always holds the site and the fresh clock value of the insert that made it. The state of a replica is the set of pairs whose insert it has run and whose delete it has not, which does not depend on the delivery order, so replicas with the same operations show the same list. A local insert lands at its index, because its position is between the positions of its neighbours.

## Complexity

Let $N$ be the number of elements and $L$ the length of the longest position.

| operation | time | messages |
| --- | --- | --- |
| ALLOC | $O(L)$ | none |
| insert or delete, local or remote, in a balanced tree | $O(L \log N)$, since a comparison costs $O(L)$ | one position of $O(L)$ triples |
| READ | $\Theta(N)$ | none |

Space is $\Theta(N L)$ in the worst case, with no tombstones. The length $L$ depends on the editing pattern. With random inserts it stays small, but repeated inserts at one place make it grow linearly. In one seeded run of the code on this page, with base $2^{10}$ and boundary 10:

| inserts | pattern | average levels | largest |
| --- | --- | --- | --- |
| 1000 | always at the end | 3.25 | 6 |
| 1000 | always at the start | 168.9 | 329 |
| 1000 | at random places | 3.83 | |
| 10000 | always at the end | 27.4 | 54 |
| 10000 | always at the start | 1688 | 3395 |
| 10000 | at random places | 4.89 | |

At the start, every insert lies between the empty list and a position with small digits, so most allocations go one level down. At the end, each level allows about $\mathit{base} / (\mathit{boundary}/2)$ inserts before it is full, so the length still grows linearly, with a small slope. [LSEQ](/lseq/) changes the allocation to fix this.

## Variants

- **Logoot-Undo.** Weiss, Urso and Molli (2010) add undo of any operation, by keeping a visibility degree for each element. It uses the triple form shown on this page.
- **LSEQ.** [LSEQ](/lseq/) doubles the base at each level and picks per level, at random, whether to allocate near the left or near the right neighbour, which keeps positions short for editing at the end or at the start.
- **How Logoot differs from the other sequence CRDTs.** [Treedoc](/treedoc/) also uses dense positions, but as paths in a binary tree, and keeps deleted nodes that still have children. [WOOT](/woot/), [RGA](/rga/), the [causal tree](/causal-tree/) and [YATA](/yata/) store neighbour ids instead of positions and keep tombstones. Logoot needs causal delivery for deletes, and it can interleave concurrent text, which RGA, YATA and WOOT avoid in most cases.

## When to use it

Use Logoot when you want a sequence CRDT without tombstones, where a remote insert is only a sorted insert, and where the editing pattern is not dominated by long runs at one place. Its simple state, a sorted map from positions to values, fits storage in key-value stores. For text typed mostly at the end or in long bursts, prefer LSEQ or a design based on neighbour ids.

## Pitfalls

- **A position that ends with digit 0.** Then no position fits to its left at that level and a later ALLOC between it and its left neighbour may fail. Line L5 never makes such a position.
- **Dropping the site and the clock.** Two sites that pick the same digits at the same time then get the same position, and one element overwrites the other.
- **Allocating in the middle of the gap.** Picking the midpoint uses up the gap in $\log_2(\mathit{base})$ steps for typing at the end. The boundary strategy keeps the step small and near the left neighbour.
- **Delivering a delete before its insert.** Without causal delivery the delete finds nothing to remove and the later insert brings the element back.
- **Interleaving.** Concurrent words typed at one place can mix letter by letter.

## Implementations

The Python module follows the main block with `# @line` markers for L1 to L9 and keeps the positions in a sorted Python list. The tests check ALLOC on hand-made and random pairs, run the example, find interleaving of two concurrent words over 20 seeds, check growth (short positions for typing at the end, long ones for typing at the start), and run seeded runs with 2 to 5 sites, causal delivery and up to 300 operations, with a small base to force deep positions. They check that all replicas converge, that local edits land at their index, that no position ends with digit 0, and that one order explains every replica's list.

## History

Weiss, Urso and Molli presented Logoot at ICDCS 2009, the same conference where Preguiça, Marques, Shapiro and Letia presented [Treedoc](/treedoc/), as a scalable alternative to [WOOT](/woot/) for peer-to-peer editing. Logoot-Undo followed in 2010. Nédelec, Molli, Mostefaoui and Desmontils showed in 2013 that Logoot positions grow linearly under common editing patterns and proposed LSEQ. Kleppmann, Gomes, Mulligan and Beresford showed in 2019 that Logoot and LSEQ can interleave concurrent insertions.

## References
