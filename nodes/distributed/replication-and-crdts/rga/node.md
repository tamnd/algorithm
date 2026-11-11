---
tag: WZ1GQT
kind: data-structure
slug: rga
name: Replicated Growable Array (RGA)
aliases:
- replicated growable array
- RGA
area: distributed/replication-and-crdts
level: advanced
summary: An op-based sequence CRDT. Each element has a unique timestamp, an insert names the element to its left, and a replica skips larger timestamps after it. Deletes leave tombstones.
implements: [crdt]
model: word-ram
complexity:
  vars: {N: "the number of elements ever inserted, tombstones included"}
  time: {worst: O(N)}
  space: {extra: Θ(N)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [op-based-crdt, causal-broadcast, lamport-clocks, linked-list, tombstone]
see_also: [causal-tree, yata, woot, logoot, lseq, treedoc, collaborative-text-editing, operational-transformation]
sources:
  - paper: doi:10.1016/j.jpdc.2010.12.006
    title: Hyun-Gul Roh, Myeongjae Jeon, Jin-Soo Kim and Joonwon Lee, Replicated abstract data types, building blocks for collaborative applications, Journal of Parallel and Distributed Computing 71(3), 2011
    locator: pages 354 to 368, the RGA with S4Vector timestamps, insert after a reference and tombstones
  - url: https://inria.hal.science/inria-00555588
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, A comprehensive study of convergent and commutative replicated data types, INRIA RR-7506, 2011
    locator: Section 3.5 and Specification 19 (op-based RGA)
  - paper: doi:10.1145/2933057.2933090
    title: Hagit Attiya, Sebastian Burckhardt, Alexey Gotsman, Adam Morrison, Hongseok Yang and Marek Zawirski, Specification and complexity of collaborative text editing, PODC 2016
    locator: pages 259 to 268, Definition 7 (strong list specification), Theorem 1 (RGA meets it) and Theorem 2 (metadata bound)
  - paper: doi:10.1145/3301419.3323972
    title: Martin Kleppmann, Victor B. F. Gomes, Dominic P. Mulligan and Alastair R. Beresford, Interleaving anomalies in collaborative text editors, PaPoC 2019
    locator: the analysis of RGA, which does not interleave forward-typed runs but has a lesser anomaly, and the name timestamped insertion tree
  - paper: doi:10.1145/3133933
    title: Victor B. F. Gomes, Martin Kleppmann, Dominic P. Mulligan and Alastair R. Beresford, Verifying strong eventual consistency in distributed systems, OOPSLA 2017
    locator: the mechanized convergence proof of RGA in Isabelle/HOL
---

The Replicated Growable Array (RGA) is an op-based [CRDT](/crdt/) for a sequence, such as the characters of a shared text. Every inserted element gets a unique timestamp that grows along causality, like a [Lamport clock](/lamport-clocks/). An insert names the element it goes after, its reference. To apply an insert, a replica goes to the position right after the reference, skips every element whose timestamp is larger than the new one, and puts the new element there. A delete marks the element as a [tombstone](/tombstone/) and keeps it, so later inserts can still use it as a reference. With causal delivery, all replicas that have applied the same operations hold the same list.

## In plain words

Think of a shared line of text. Each letter gets a unique stamp, and a letter typed later gets a larger stamp than every letter its author had seen. To insert a letter, a writer says "put it right after that letter".

Two writers may put letters after the same letter at the same time. To agree on an order, each server walks forward from the named letter and passes every letter with a larger stamp, then stops. So letters after the same spot end up ordered by stamp, largest first, and a letter that someone typed after one of them stays next to it. Deleted letters stay in the list, hidden, so that a later "after that letter" still makes sense.

## The abstract type

RGA implements a replicated list with updates INSERT$(i, x)$, which makes $x$ the $i$-th visible element, and DELETE$(i)$, and the query READ, which returns the visible elements. It is an [op-based CRDT](/op-based-crdt/).

**Model.** There are $n$ replicas with distinct ids. Operations are sent by [causal broadcast](/causal-broadcast/): each operation is delivered exactly once at every replica, after every operation in its causal past. A replica runs an operation at its source at once.

**Specification.** Replicas that have delivered the same set of operations return the same list (strong eventual consistency). A local INSERT$(i, x)$ makes $x$ the $i$-th visible element at its source, and DELETE$(i)$ hides the $i$-th one. There is one total order on all inserted elements such that every replica's list, at every time, is the elements it has seen and not deleted, in that order; Attiya et al. call this the strong list specification (their Definition 7), and they prove that RGA meets it (their Theorem 1).

## Representation

A replica stores a [linked list](/linked-list/) of nodes, starting with a head sentinel. A node holds a timestamp, a value and a tombstone flag. A [hash table](/hash-table/) maps each timestamp to its node, so a remote operation finds its reference in $O(1)$ expected time.

Roh et al. use an S4Vector $(\mathit{ssn}, \mathit{sum}, \mathit{sid}, \mathit{seq})$ as the timestamp: a session number, the sum of the replica's vector clock, the replica id and the replica's own count of operations. Timestamps are compared by $(\mathit{ssn}, \mathit{sum}, \mathit{sid})$. Under causal delivery, $\mathit{sum}$ is larger at an operation than at every operation in its causal past, and $\mathit{sid}$ breaks ties, so any unique Lamport timestamp (counter, replica id) works the same way.

The list is the depth-first pre-order of a tree: the parent of each element is its reference, the head is the root, and the children of a node are visited in decreasing timestamp order. This is the timestamped insertion tree of Attiya et al. and the [causal tree](/causal-tree/) of Grishchenko.

## Operations

```pseudo id=main
CREATE()
L1  list ← [head];  index ← empty map                 ▷ head is a sentinel before the first element

INSERT-REMOTE(ref, t, x)                              ▷ also used at the source
L2  p ← the position right after the node of ref
L3  while p is not the end and timestamp(p) > t do
L4      p ← next(p)                                   ▷ skip larger timestamps
L5  node ← a new node (t, x, alive)
L6  put node before p
L7  index[t] ← node

DELETE-REMOTE(t)
L8  mark index[t] as a tombstone                      ▷ it stays in the list
```

**Local insert.** To insert $x$ as visible element $i$, the source takes as $\mathit{ref}$ the timestamp of visible element $i - 1$ (or the head), makes a timestamp $t$ larger than every timestamp it has seen, runs lines L2 to L7, and broadcasts $(\mathit{ref}, t, x)$. Since $t$ is the largest timestamp at the source, the loop of line L3 stops at once and $x$ lands right after its reference, at visible position $i$.

**Remote insert.** Lines L3 and L4 skip the elements that were inserted after the same reference with a larger timestamp, together with everything inserted after those. The new element goes before the first element with a smaller timestamp.

**Delete.** Line L8 only sets a flag. The node stays, because a concurrent or later insert may name it as a reference.

## Example

Two replicas $a$ (id 0) and $b$ (id 1) hold "H i", typed by $a$ with timestamps $(0, 1, 0)$ and $(0, 2, 0)$, written as $(\mathit{ssn}, \mathit{sum}, \mathit{sid})$. Now both type between H and i at the same time.

| step | event | $a$ | $b$ |
| --- | --- | --- | --- |
| 1 | $a$ inserts e after H with $t_e = (0, 3, 0)$ | H e i | H i |
| 2 | $b$ inserts o after H with $t_o = (0, 3, 1)$ | H e i | H o i |
| 3 | $a$ applies o: start after H, $t_e < t_o$, stop | H o e i | H o i |
| 4 | $b$ applies e: start after H, skip o since $t_o > t_e$, stop at i since $(0, 2, 0) < t_e$ | H o e i | H o e i |
| 5 | $a$ deletes e; $b$ applies it | H o i, with e a tombstone | H o i, with e a tombstone |

Both replicas agree. The tree view: H has the children o and e, visited in decreasing timestamp order, and e has the child i.

**Interleaving.** If $a$ types "abc" and $b$ types "xyz" forward at the same place, each letter's reference is the letter before it, so each word hangs as one chain in the tree and the result is abcxyz or xyzabc. If each replica types its word from back to front, always at the head (c, then b before it, then a), every letter is a child of the head, and the timestamps alone decide the order: the result is xaybzc. Kleppmann et al. (2019) show that RGA does not interleave text typed forward and describe this kind of lesser anomaly.

## Correctness

Two facts carry the proof. First, timestamps are unique and grow along causality, so every element in the subtree of a node has a larger timestamp than the node. Second, a new element has no children yet, because anything inserted after it is causally later and is delivered later. Now take the list to be the pre-order of the tree. Starting right after the reference, lines L3 and L4 pass the subtrees of the reference's children with larger timestamps, since every node in those subtrees has a timestamp above the new one, and stop at the first node with a smaller timestamp, which is either the next child of the reference or a node after the reference's whole subtree. Both are exactly where pre-order puts the new element. So the list is always the pre-order of the tree of delivered inserts, which does not depend on delivery order. The full proof is in [the correctness proof](proofs/correctness.md). Attiya et al. (2016) prove that RGA meets the strong list specification, and Gomes et al. (2017) check its convergence in Isabelle/HOL.

## Complexity

Let $N$ be the number of elements ever inserted, tombstones included.

| operation | time | messages |
| --- | --- | --- |
| remote insert | $O(1)$ expected to find the reference, plus the skipped nodes, $O(N)$ worst | none |
| remote delete | $O(1)$ expected | none |
| local insert or delete at visible index $i$ | $O(N)$ to find the node by walking; $O(\log N)$ with an [order-statistic tree](/order-statistic-tree/) over visible counts | one operation with two timestamps |
| READ | $\Theta(N)$ | none |

The state is $\Theta(N)$, since tombstones stay. Each timestamp takes $O(\log N + \log n)$ bits. Attiya et al. show that RGA keeps metadata of $O(D \lg k)$ bits for a document of $D$ elements, over its history in their model (their Theorem 2), and that any algorithm meeting the strong specification needs $\Omega(D)$ in the worst case for three or more replicas (their Theorem 4).

## Variants

- **[Causal tree](/causal-tree/).** Stores the same tree as a weave of atoms and computes the same order.
- **Block-wise RGA.** Stores runs of consecutive characters typed by one author as one node and splits a node when an insert lands inside it, which cuts the per-character overhead.
- **Garbage collection of tombstones.** A tombstone can be dropped once every replica has delivered its delete and every insert that names it. That needs a stable cut of the causal history, which costs coordination.
- **How RGA differs from the other sequence CRDTs.** [WOOT](/woot/) records both neighbours and integrates with a recursive scan. [YATA](/yata/) records both origins and a different conflict rule. [Logoot](/logoot/) and [LSEQ](/lseq/) give each element a dense position identifier and keep no tombstones, but can interleave. [Treedoc](/treedoc/) uses paths in a binary tree.

## When to use it

Use RGA for collaborative text or list editing when operations can be sent by causal broadcast: it is simple, its metadata per element is one timestamp and one reference, and it does not interleave forward-typed text. It underlies the list types of Automerge. If causal delivery is not available, an insert must wait until its reference has arrived, which is a form of causal delivery anyway.

## Pitfalls

- **Timestamps that do not grow along causality.** If a replica makes a timestamp smaller than one it has seen, a subtree can contain a smaller timestamp than its root, and the skip loop stops in the wrong place, so replicas diverge.
- **Removing tombstones too early.** A node removed while a concurrent insert still names it leaves that insert without a reference.
- **Skipping until "smaller or equal".** Timestamps must be unique. With equal timestamps, the loop's stop rule is not a total order.
- **Inserting at the wrong side.** The rule is "skip larger, stop at smaller". Reversing it on some replicas only makes them diverge.

## Implementations

The Python class follows the main block with `# @line` markers for L1 to L8, with S4Vector timestamps compared on $(\mathit{ssn}, \mathit{sum}, \mathit{sid})$. It keeps the nodes in a Python list, so a lookup of a position is linear. The tests run the example, the forward and back-to-front typing cases, and seeded runs with 2 to 5 replicas and up to 300 operations under causal delivery. They check that replicas converge, that a local insert lands at its index, and that one order on all elements explains every replica's list at every step, the strong list specification.

## History

Roh, Jeon, Kim and Lee gave the RGA in their work on replicated abstract data types, published in 2011, with S4Vector timestamps and a hash table for remote operations. Shapiro et al. included it as Specification 19 of their 2011 report. Attiya et al. (2016) proved that it meets the strong list specification and noted its tree structure, Gomes et al. (2017) verified it in Isabelle/HOL, and Kleppmann et al. (2019) studied its interleaving behaviour.

## References
