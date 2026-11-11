---
tag: ZX6H95
kind: problem
slug: collaborative-text-editing
name: Collaborative text editing
aliases:
- real-time collaborative editing
- concurrent text editing
area: distributed/replication-and-crdts
level: intro
summary: Let several users edit copies of one text at the same time, each seeing their own edits at once, so that all copies end the same and every edit keeps its meaning.
prereqs: [eventual-consistency, happened-before]
see_also: [operational-transformation, crdt, rga, yata, woot, logoot, tp1-tp2-conditions, strong-eventual-consistency]
sources:
  - paper: doi:10.1145/274444.274447
    title: Chengzheng Sun, Xiaohua Jia, Yanchun Zhang, Yun Yang and David Chen, Achieving convergence, causality preservation, and intention preservation in real-time cooperative editing systems, ACM TOCHI 5(1), 1998
    locator: pages 63 to 108, the consistency model with convergence, causality preservation and intention preservation, and the GOT algorithm
  - paper: doi:10.1145/67544.66963
    title: Clarence A. Ellis and Simon J. Gibbs, Concurrency control in groupware systems, SIGMOD 1989
    locator: pages 399 to 407, the groupware editing problem, the precedence and convergence properties, and the dOPT algorithm
  - paper: doi:10.1145/2933057.2933090
    title: Hagit Attiya, Sebastian Burckhardt, Alexey Gotsman, Adam Morrison, Hongseok Yang and Marek Zawirski, Specification and complexity of collaborative text editing, PODC 2016
    locator: pages 259 to 268, Definition 7 (strong list specification), Definition 8 (weak list specification), Theorems 1 and 2 (RGA meets the strong one, and its metadata), Theorem 4 (the lower bound on metadata)
  - paper: doi:10.1145/3301419.3323972
    title: Martin Kleppmann, Victor B. F. Gomes, Dominic P. Mulligan and Alastair R. Beresford, Interleaving anomalies in collaborative text editors, PaPoC 2019
    locator: the interleaving anomaly and which sequence CRDTs show it
  - paper: doi:10.4204/EPTCS.107.5
    title: Aurel Randolph, Hanifa Boucheneb, Abdessamad Imine and Alejandro Quintero, On consistency of operational transformation approach, EPTCS 107, 2013
    locator: pages 45 to 59, the result that no transformation function with the classical parameters meets both TP1 and TP2
---

Collaborative text editing is the problem of letting several people edit one text at the same time from different machines. Each person works on a local copy and sees their own edits at once, without waiting for the network. Edits travel to the other copies later and in different orders. The problem asks for a way to apply remote edits so that all copies end with the same text (convergence), edits are applied after the edits they depend on (causality preservation), and each edit keeps the effect its author meant, even when other edits happened at the same time (intention preservation). These three goals are the CCI model of Sun et al. (1998). There are two families of solutions: [operational transformation](/operational-transformation/), which changes the positions of incoming edits, and sequence [CRDTs](/crdt/), which give every character a unique identity so that positions never need to change.

## In plain words

Two people edit "Hi" together. At the same moment one types "e" after "H" and the other types "o" after "H". Each sees their own letter at once.

Now each screen gets the other person's edit: "put a letter at position 1". If each screen does just that, one ends with "Hoei" and the other with "Heoi". The copies differ, and they will stay different.

The goal is a rule that makes both screens show the same text, with both letters after "H" and before "i", without making anyone wait or ask a central lock for permission.

## Definition

There are $n$ sites. Each holds a copy of a string over some alphabet; all start from the same string. A user at a site can run INSERT$(i, c)$, which puts character $c$ at index $i$, and DELETE$(i)$, which removes the character at index $i$, and the site applies the edit to its copy at once. The site then sends the edit, in some form, to the other sites, which apply it when it arrives. The network delivers every message eventually, but with delays and in different orders at different sites.

A solution must meet these requirements, stated by Sun et al. (1998) as the CCI model:

- **Convergence.** When all sites have applied the same set of edits, their copies are equal.
- **Causality preservation.** If edit $a$ [happened before](/happened-before/) edit $b$, every site applies $a$ before $b$.
- **Intention preservation.** The effect of each edit at every site is the effect it had at its own site, and it does not change the effect of edits that were concurrent with it. An insert that went between two characters stays between them; a delete removes the character its author saw, and only that one.

Intention preservation is informal in the CCI model. Attiya et al. (2016) give a precise form for lists. The **strong list specification** (their Definition 7) asks for one total order on all inserted elements such that, at every site and every time, the copy is the elements the site has seen and not deleted, in that order. The **weak list specification** (their Definition 8) asks only that two elements appear in the same relative order in every copy that holds both. Together with convergence, these are the specifications that the sequence CRDTs on this site prove or test.

## Variants

- **Real time or asynchronous.** In real-time editing, edits travel within seconds. In asynchronous editing, a site can stay offline for days and then merge, which makes metadata size and merge cost matter more.
- **With or without a server.** A central server can fix one order of all edits, which makes the problem easier. Peer-to-peer settings have no such site.
- **Plain text or rich text.** Rich text adds formatting spans, and structured documents add trees. Many systems build these on top of a replicated list.
- **Preserving runs.** A further goal is that two runs of text typed at the same place at the same time end next to each other, not mixed letter by letter. Kleppmann et al. (2019) call the mixing the interleaving anomaly.

## Examples

**Two inserts at one place.** "Hi"; site 1 runs INSERT$(1, \mathrm{e})$ and site 2 runs INSERT$(1, \mathrm{o})$ at the same time. Applying the remote edit as it is gives "Hoei" at site 1 and "Heoi" at site 2. Both are acceptable final texts, but the sites must pick the same one; a tie rule, such as the smaller site id goes first, fixes this.

**A delete moves the place of an insert.** "abc"; site 1 runs DELETE$(0)$, removing "a", and site 2 runs INSERT$(2, \mathrm{x})$, putting "x" between "b" and "c". Applied as they are, site 1 gets "bc" and then "bcx", with "x" in the wrong place, and site 2 gets "abxc" and then "bxc". The copies differ, and at site 1 the intention of the insert is lost. Transforming the insert to INSERT$(1, \mathrm{x})$ at site 1 gives "bxc" at both.

**Interleaving.** Site 1 types "abcd" and site 2 types "wxyz", both at the end of an empty text, at the same time. All copies converge in every algorithm below, but with [Logoot](/logoot/) the result can be "awbxcdyz", which mixes the two words.

## Known algorithms

The two families differ in what an edit carries. In operational transformation, an edit carries an index, and each site transforms incoming edits against the concurrent edits it has already applied. In a sequence CRDT, an edit carries the identity of a character, or of its neighbours, and applying it needs no transformation.

| design | year | family | an insert carries | delivery | deleted characters | interleaving (Kleppmann et al. 2019) |
| --- | --- | --- | --- | --- | --- | --- |
| dOPT | 1989 | OT, peer to peer | an index and a state vector | causal | not stored | not studied there; dOPT fails to converge in some cases |
| Jupiter | 1995 | OT, central server | an index and two counters | FIFO to and from the server | not stored | not studied there |
| adOPTed, GOT, GOTO | 1996 to 1998 | OT, peer to peer | an index and a state vector | causal | not stored | not studied there |
| [WOOT](/woot/) | 2006 | CRDT | its id and both neighbours' ids | any order, with a waiting pool | hidden | conjectured not to interleave |
| [Treedoc](/treedoc/) | 2009 | CRDT | a path in a binary tree | causal | hidden until a flatten | conjectured not to interleave |
| [Logoot](/logoot/) | 2009 | CRDT | a position from a dense order | causal | removed | interleaves |
| [Causal tree](/causal-tree/) | 2010 | CRDT | its id and its left neighbour's id | causal | hidden | the same order as RGA |
| [RGA](/rga/) | 2011 | CRDT | its timestamp and its left neighbour's id | causal | hidden | no interleaving of forward runs, a lesser anomaly remains |
| [LSEQ](/lseq/) | 2013 | CRDT | a position from a dense order | causal | removed | interleaves |
| [YATA](/yata/) | 2016 | CRDT | its id and both neighbours' ids | after its neighbours | hidden | not stated there |

The OT designs are on the [operational transformation](/operational-transformation/) page; the conditions they need are on the [TP1 and TP2](/tp1-tp2-conditions/) page. A CRDT for a list meets [strong eventual consistency](/strong-eventual-consistency/): sites that have delivered the same edits have equal copies, with no further messages.

## Bounds

- **Metadata.** Attiya et al. (2016) give a lower bound on the metadata that an algorithm meeting the list specifications must keep in the worst case (their Theorem 4), and show that RGA stays close to it (their Theorem 2). This is why sequence CRDTs keep tombstones or long identifiers: some record of past edits cannot be avoided.
- **Transformation functions.** Randolph et al. (2013) show, by controller synthesis, that no inclusion transformation function built on the classical parameters (the kind of edit, the index and the character, with a site id for ties) meets both TP1 and TP2. Peer-to-peer OT that needs TP2 must therefore add information to the edits, as tombstone-based transforms do, or restrict the order in which edits are transformed.
- **Messages.** Every algorithm above sends each edit once to each other site. Server-based designs send it to the server and from the server to the others.

## Reductions

- **To a replicated list.** Text is a list of characters, so any replicated list that meets the strong or weak list specification, such as a sequence CRDT, solves the problem.
- **To state machine replication, with a server.** If one server orders all edits, as in [total order broadcast](/total-order-broadcast/), every site could apply the edits in that order. To keep local edits instant, a site must still transform the server's edits against its own unconfirmed ones, which is what Jupiter does.
- **To the TP conditions.** A peer-to-peer OT algorithm that transforms along any path, such as adOPTed, converges if its transform meets TP1 and TP2.

## Applications

Real-time editors for documents, slides and code in the browser use server-based OT or sequence CRDTs. Local-first software, where each device keeps a full copy and syncs later, mostly uses CRDTs, through libraries such as Yjs, which implements YATA. Peer-to-peer wikis such as Wooki built on WOOT. The same problem appears for any replicated ordered collection, such as to-do lists and the children of a node in a document tree.

## References
