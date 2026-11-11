---
tag: B5EAJ4
kind: data-structure
slug: causal-tree
name: Causal tree
aliases:
- causal tree CRDT
area: distributed/replication-and-crdts
level: advanced
summary: A sequence CRDT that stores each edit as an atom pointing to its cause. The text is a depth-first walk of the atom tree with newer siblings first, the same order as RGA.
implements: [crdt]
model: word-ram
complexity:
  vars: {N: "the number of atoms, deletions included"}
  time: {worst: Θ(N)}
  space: {extra: Θ(N)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [rga, op-based-crdt, lamport-clocks, depth-first-search]
see_also: [rga, yata, woot, logoot, treedoc, collaborative-text-editing, tombstone, causal-broadcast]
sources:
  - paper: doi:10.1145/1832772.1832777
    title: Victor Grishchenko, Deep hypertext with embedded revision control implemented in regular expressions, WikiSym 2010
    locator: pages 1 to 10, atoms with ids and causes, the weave as a depth-first order, deletions as atoms, and the weave kept as a string
  - paper: doi:10.1145/2596631.2596641
    title: Victor Grishchenko, Citrea and Swarm, partially ordered op logs in the browser, PaPEC 2014
    locator: pages 1 to 3, the causal tree data structure in the Citrea editor
  - paper: doi:10.1145/3301419.3323972
    title: Martin Kleppmann, Victor B. F. Gomes, Dominic P. Mulligan and Alastair R. Beresford, Interleaving anomalies in collaborative text editors, PaPoC 2019
    locator: the remark that Attiya et al. call this structure a timestamped insertion tree, while Grishchenko calls it a causal tree
  - paper: doi:10.1145/2933057.2933090
    title: Hagit Attiya, Sebastian Burckhardt, Alexey Gotsman, Adam Morrison, Hongseok Yang and Marek Zawirski, Specification and complexity of collaborative text editing, PODC 2016
    locator: pages 259 to 268, the timestamped insertion tree behind RGA
---

A Causal tree is a [CRDT](/crdt/) for a sequence in which every edit is an atom with a unique id and a cause, the atom it was typed after. The atoms form a tree under the cause relation, rooted at a start atom. The text, called the weave, is the [depth-first](/depth-first-search/) walk of this tree with the children of each atom visited in decreasing id order. A deletion is an atom too, whose cause is the deleted atom, and an atom with a deletion child is hidden. Victor Grishchenko described the structure in 2010. With Lamport ids it is the same tree that orders [RGA](/rga/), and it gives the same order: Kleppmann et al. (2019) note that Attiya et al. call this structure a timestamped insertion tree, while Grishchenko calls it a causal tree.

## In plain words

Every letter remembers which letter it was typed after. Draw an arrow from each letter to that letter. The arrows make a family tree with a start mark at the top.

To read the text, walk the tree: write a letter, then visit its children, the newest child first, and finish each child's whole family before the next child. A letter typed right after another, later than everything else there, comes straight after it, which is what the typist saw.

To delete a letter, add a small "delete" mark as its child. The letter stays in the tree, hidden. Since the text comes from the tree alone, two servers with the same letters and marks show the same text, in any order of arrival.

## The abstract type

The causal tree implements a replicated list with updates INSERT$(i, x)$ and DELETE$(i)$ and the query READ. It is an [op-based CRDT](/op-based-crdt/) whose operations are atoms. Its state is a grow-only set of atoms, so it is also a [state-based](/state-based-crdt/) one under union, provided that every atom's cause is present.

**Model.** There are $n$ sites with distinct ids. Atoms are sent by [causal broadcast](/causal-broadcast/), or by any channel together with a rule that holds an atom back until its cause has arrived. Duplicates are ignored.

**Specification.** Replicas with the same set of atoms return the same text. A local INSERT$(i, x)$ makes $x$ the $i$-th visible element at its source, and DELETE$(i)$ hides the $i$-th one. As for RGA, one order on all atoms explains the text of every replica at every time.

## Representation

An atom is a tuple $(\mathit{id}, \mathit{cause}, \mathit{kind}, \mathit{value})$. The id is a Lamport pair (time, site): a site makes an id one larger in time than every id it has seen, so a cause is always smaller than its effect. The kind is "char" or "del". A replica stores a map from ids to atoms and, for each atom, its list of children sorted by decreasing id. The root atom has the id $(0, \bot)$.

Grishchenko keeps the weave itself as a flat string of atoms and updates it in place, so a read is a scan and an insert puts the atom right after its cause and its newer siblings. The version on this page stores the tree and computes the weave by a walk, which is easier to check and gives the same order.

## Operations

```pseudo id=main
CREATE()
L1  atoms ← {root};  children[root] ← empty list

ADD(a)                                                ▷ a remote or local atom; its cause is present
L2  atoms[a.id] ← a;  children[a.id] ← empty list
L3  put a.id into children[a.cause]
L4  keep children[a.cause] sorted by decreasing id   ▷ newer siblings first

WEAVE()
L5  stack ← [root];  out ← empty list
L6  while stack is not empty do
L7      x ← pop(stack);  append x to out
L8      push children[x] onto stack, smallest id first   ▷ so the largest id is popped next

READ()
L9  return the values of the char atoms in WEAVE() that have no del child
```

**Local insert.** To insert $x$ as visible element $i$, the source makes an atom whose cause is visible element $i - 1$ (or the root) and whose id is larger than every id it has seen, then runs ADD and broadcasts the atom. **Local delete.** To delete visible element $i$, the source makes a del atom whose cause is that element.

## Example

Two sites, $a$ (site 0) and $b$ (site 1). $a$ types H with id $(1, 0)$ after the root and i with id $(2, 0)$ after H, and $b$ receives both. Then $a$ types e after H with id $(3, 0)$, and $b$ types o after H with id $(3, 1)$, at the same time.

| step | event | children of H | weave at $a$ | weave at $b$ |
| --- | --- | --- | --- | --- |
| 1 | H and i at both | $(2,0)$ | H i | H i |
| 2 | $a$ adds e $(3,0)$; $b$ adds o $(3,1)$ | $a$: $(3,0), (2,0)$; $b$: $(3,1), (2,0)$ | H e i | H o i |
| 3 | they exchange atoms | $(3,1), (3,0), (2,0)$ | H o e i | H o e i |
| 4 | $b$ deletes o: del atom $(4,1)$ with cause $(3,1)$ | same | H e i, with o hidden | H e i, with o hidden |

The walk visits H, then its children in the order o, e, i, because $(3,1) > (3,0) > (2,0)$. RGA with the same ids gives H o e i as well.

## Correctness

The weave is computed from the set of atoms alone, so two replicas with the same atoms have the same weave and the same text. For a local insert, the new atom has the largest id at its source, so it is the first child of its cause and the walk visits it right after the cause, at visible index $i$. Ids grow along causality, so every atom in a subtree has a larger id than the subtree's root. Under that condition, the pre-order with newer siblings first is exactly the list that RGA builds by "skip larger timestamps after the reference", as the RGA proof shows, and it is the restriction of one global order to each replica's atoms. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $N$ be the number of atoms, deletions included, and $k$ the number of children of the cause.

| operation | time | messages |
| --- | --- | --- |
| ADD | $O(k)$ to place the id among its siblings | one atom |
| WEAVE and READ | $\Theta(N)$ | none |
| local insert or delete at index $i$ | $\Theta(N)$ with a walk; less with a cached weave and an index | one atom |

The state is $\Theta(N)$: nothing is ever removed. Each atom carries two ids of $O(\log N + \log n)$ bits. Grishchenko's string form makes reads a linear scan of a flat buffer, which is fast in practice.

## Variants

- **The weave as a string.** Grishchenko (2010) stores the weave as a string with atoms and ids, and implements the operations with regular expressions over it.
- **Version control.** Because the atom set only grows, any earlier version is the set of atoms below some causal cut, so the structure doubles as a revision history. Grishchenko presents this as embedded revision control.
- **[RGA](/rga/).** Builds the same order incrementally in a linked list with tombstone flags instead of delete atoms.
- **How it differs from the other sequence CRDTs.** Like RGA it records one neighbour, unlike [WOOT](/woot/) and [YATA](/yata/), which record two. Unlike [Logoot](/logoot/) and [LSEQ](/lseq/), it has no dense position identifiers and keeps deleted atoms.

## When to use it

Use a causal tree when the full edit history is useful, for example for undo, blame or time travel, and when a single append-only log of atoms is a natural storage format. It is a good fit for systems that already ship operation logs with Lamport ids. Where only the current text matters, RGA or YATA keep less per deletion.

## Pitfalls

- **Ids that do not respect causality.** The weave order relies on causes having smaller ids. A site that makes an id without first raising its clock above every id it has seen breaks it.
- **Atoms before their causes.** An atom whose cause is missing has no place in the tree. Hold it until the cause arrives.
- **Visiting siblings oldest first.** That puts a newly typed character after the older text that follows its cause, so the local insert lands in the wrong place.
- **Counting deletion atoms as text.** Deletion atoms are children in the tree but are not characters, and they must be filtered out when reading.

## Implementations

The Python class follows the main block with `# @line` markers for L1 to L9. It computes the weave by an iterative walk on each read. The tests run the example and seeded runs with 2 to 5 sites and up to 300 operations under causal delivery. They check that sites converge, that local edits land at their index, that one order explains every site's text, and that the weave order equals the order that the RGA rule gives with the same ids.

## History

Victor Grishchenko described the causal tree and its weave in 2010, in a paper on hypertext with embedded revision control implemented with regular expressions, and later used it in the Citrea editor and the Swarm library (2014). Attiya et al. (2016) described the same tree for RGA as a timestamped insertion tree, and Kleppmann et al. (2019) pointed out that the two names refer to the same structure.

## References
