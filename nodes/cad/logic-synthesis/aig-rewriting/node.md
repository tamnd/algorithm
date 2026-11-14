---
tag: CJJRNE
kind: algorithm
slug: aig-rewriting
name: DAG-aware AIG rewriting
aliases:
- AIG rewriting
area: cad/logic-synthesis
level: advanced
summary: Mishchenko, Chatterjee and Brayton's rewriting that replaces the logic of small cuts of an AIG by precomputed AIGs of the same NPN class when this saves nodes in the shared graph.
solves: [multi-level-logic-synthesis]
model: word-ram
complexity:
  vars: {N: the number of AND nodes, C: the largest number of cuts of at most K leaves of one node, K: the largest number of leaves of a cut}
  time: {worst: O(N^2 C^2)}
  space: {extra: O(N C)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2006
  people: [Alan Mishchenko, Satrajit Chatterjee, Robert Brayton]
  note: Mishchenko, Chatterjee and Brayton rewrote 4-input cuts of an AIG with precomputed subgraphs of the NPN classes of 4-input functions, counting the gain over the shared graph, and built it into ABC.
prereqs: [and-inverter-graph, k-feasible-cut, cut-enumeration, boolean-matching]
see_also: [aig-balancing, exact-synthesis, sat-sweeping, majority-inverter-graph, technology-mapping, multi-level-logic-synthesis, local-search, hash-consing]
sources:
  - paper: doi:10.1145/1146909.1147048
    title: Alan Mishchenko, Satrajit Chatterjee and Robert Brayton, DAG-aware AIG rewriting, a fresh look at combinational logic synthesis, Proceedings of the 43rd Design Automation Conference, 2006, pages 532 to 535
    locator: the 4-input cuts, the 222 NPN classes of 4-input functions, the precomputed non-redundant subgraphs of the useful classes, the count of gain over the shared graph, and the experiments with balancing
  - paper: doi:10.1007/978-3-642-14295-6_5
    title: Robert Brayton and Alan Mishchenko, ABC, an academic industrial-strength verification tool, Computer Aided Verification (CAV 2010), Lecture Notes in Computer Science 6174, Springer, 2010, pages 24 to 40
    locator: the synthesis commands of ABC on AIGs, among them rewrite, refactor and balance
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.2, Boolean evaluation (the least cost of the functions of 3 and 4 variables, and their classes under permutation and complementation)
---

DAG-aware AIG rewriting is a local search for [multi-level logic synthesis](/multi-level-logic-synthesis/) that makes an [and-inverter graph](/and-inverter-graph/) smaller without changing its functions. For each node it looks at the small [cuts](/k-feasible-cut/) of the node, computes the function of the node in terms of the leaves of the cut, and looks up a precomputed AIG for that function, up to a permutation and complement of inputs and output, its NPN class. The new AIG replaces the old logic when this saves nodes. The gain counts the nodes that the change frees and the nodes that it adds, both in the shared graph: a node that other logic still uses is not freed, and a node that the hash table already holds is not added. Mishchenko, Chatterjee and Brayton (2006) used cuts of 4 leaves and the 222 NPN classes of 4-input functions, and the rewrite command of ABC is built on their method.

## In plain words

Take a gate and a few wires below it, at most three or four, from which the gate's value can be computed. Work out what the gate computes from those wires. That is a small truth table.

Long ago, someone found good small circuits for every such table and stored them. Look up the stored circuit for this table. Count what you would save if you threw out the old logic between the wires and the gate, and built the stored circuit in its place. Old gates that other parts of the circuit still need cannot be thrown out, so do not count them. Gates of the stored circuit that already exist somewhere cost nothing.

If the count says you save at least one gate, make the change. Go through all gates this way, from the inputs to the outputs.

## The problem

The input is an AIG with outputs $o_1, \ldots, o_k$. The output is an AIG with the same output functions and fewer AND nodes. Finding the smallest AIG of a function is a hard problem, so rewriting only makes local changes that never add nodes, and it stops after one pass over the graph. See [multi-level logic synthesis](/multi-level-logic-synthesis/) for the problem and its hardness.

A cut of a node $v$ is a set $C$ of nodes such that every path from an input to $v$ passes through $C$, and the cut is $K$-feasible when $|C| \le K$. The *maximum fanout-free cone* $M(v, C)$ is the set of nodes that become unused if $v$ is deleted: $v$ itself, and every node between $C$ and $v$ all of whose fanouts are in the set. Two functions are NPN-equivalent if one becomes the other by a permutation of the inputs, a negation of some inputs and a negation of the output. A permutation and negations cost nothing in an AIG, so two NPN-equivalent functions have smallest AIGs of the same size.

## The algorithm

```pseudo id=main
REWRITE(G)
L1  for each AND node v of G in topological order, if v is still in use do
L2      best ← none
L3      for each cut C of v with 2 to K leaves do
L4          t ← the truth table of v over C; (c, π) ← the NPN class of t and the transform to it
L5          M ← the maximum fanout-free cone of v over C
L6          for each structure S of the library for c do
L7              a ← the nodes that S over C, under π, would add, with a reused node of M counted as added
L8              if |M| − a > the gain of best then best ← (S, C, π)
L9      if best has gain > 0 then
L10         r ← build S over C under π, with the AND of the AIG page
L11         replace v by r: move each fanout of v to r, and hash it again; a fanout that now equals another node or a trivial case is replaced in turn
L12         delete the nodes that no output reaches
```

Line L3 takes the cuts from [cut enumeration](/cut-enumeration/), which merges the cuts of the two fanins. Line L4 computes the truth table by simulating the cone of $v$ above $C$, and finds the class and the transform in a table of all $2^{2^K}$ functions. Line L7 is a dry run of the AND of the AIG page that looks up each node of $S$ in the hash table and creates nothing. A node of $S$ that the table holds and that is outside $M$ costs nothing. A node that the table holds and that is in $M$ costs one, because it would be freed otherwise. A node that the table does not hold costs one. Line L8 keeps the best gain. Line L11 can trigger more merges above $v$, since a fanout of $v$ may now have the same fanins as another node.

The code of this page uses $K = 3$ and stores one smallest AIG for each of the 14 NPN classes of 3-input functions, found by an exhaustive search. The paper uses $K = 4$. It precomputes, for the classes that occur often, a set of AIG subgraphs that have no redundant nodes, shared in one graph of about a thousand nodes, and tries all of them for each cut.

## Example

Take $o = ab + ac$, built as written: node 4 is $a \wedge b$, node 5 is $a \wedge c$, and node 6 is $\neg 4 \wedge \neg 5$, with $o = \neg 6$. So the AIG has 3 AND nodes. Node 6 has four cuts with 2 or 3 leaves.

| cut of node 6 | function of node 6 | freed nodes M | added a | gain |
|---|---|---|---|---|
| {4, 5} | $\neg x \wedge \neg y$ | {6} | 1 | 0 |
| {a, c, 4} | $\neg(x_3 \vee x_1 x_2)$ | {5, 6} | the structure is node 6 again | skipped |
| {a, b, 5} | $\neg(x_3 \vee x_1 x_2)$ | {4, 6} | the structure is node 6 again | skipped |
| {a, b, c} | $\neg(a(b + c))$ | {4, 5, 6} | 2 | 1 |

The cut $\{a, b, c\}$ has the class of the function $\bar{x}_1 \vee \bar{x}_2 \bar{x}_3$ (table 00011111), whose smallest AIG has 2 nodes: the complement of $a \wedge \neg(\neg b \wedge \neg c)$. Neither node is in the table, so $a = 2$, and the gain is $3 - 2 = 1$. Line L10 makes node 7 $= \neg b \wedge \neg c$ and node 8 $= a \wedge \neg 7$, line L11 moves the output to node 8, and line L12 deletes nodes 4, 5 and 6. The AIG now has 2 nodes for $a(b + c)$, and its truth table is still 11100000.

Now let $a \wedge b$ be a second output. Node 4 is no longer freed when node 6 goes, so the cut $\{a, b, c\}$ has $M = \{5, 6\}$, $a = 2$ and gain 0, and the cut $\{a, b, 5\}$ has $M = \{6\}$ and gain 0. Nothing changes, and the AIG keeps 3 nodes. A rewriter that counted the whole tree of node 6 as freed would predict a gain of 1 and make the change, but node 4 must stay, so the AIG would still have 3 nodes, nodes 4, 7 and 8. With a structure of 3 nodes such a rewriter would even make the AIG larger. This is the sense in which the method is DAG-aware.

## Correctness

The [full proof](proofs/correctness.md) shows three facts. First, the functions do not change: the structure $S$ computes the class representative $c$, the transform $\pi$ maps it to the table $t$ of $v$ over $C$, and the new literal $r$ is built over the same leaves, so $r$ and $v$ have the same function, and line L11 only replaces nodes by literals with equal functions. Second, no cycle appears: a node built at line L10 depends only on the leaves of $C$ and on nodes found in the table, and a found node depends on $v$ only if it is $v$ or above it. If the dry run uses $v$, it has rebuilt the whole cone of $v$ above $C$, so it counts every node of $M$ and the gain is at most 0. Third, the number of nodes that the outputs reach falls by at least the gain at each change: the nodes of $M$ that the new logic does not use are deleted, each node of $S$ adds at most one node, a reused node of $M$ is counted as added, and the merges of line L11 only remove nodes.

## Complexity

With $K$ fixed, a cut has a truth table of $2^K$ bits and a constant number of library structures, so lines L4 to L8 cost $O(|M|)$ per cut, at most $O(N)$. The code of this page enumerates the cuts of each node again by merging the cuts of its fanins, $O(N C^2)$ per node in the worst case, and an accepted change costs $O(N)$ for line L11 and the sweep of line L12. Over $N$ nodes this gives the $O(N^2 C^2)$ of the front matter. ABC computes the cuts of all nodes once, bottom up, in $O(N C^2)$, keeps only a bounded number of cuts per node, and updates the graph locally, so a pass is close to linear in $N$ on circuits. The NPN table for $K = 4$ has $2^{16}$ entries, made once.

## Properties

**What is proved.** One pass keeps every output function, never makes a cycle, and lowers the number of AND nodes by at least the gain of each change, so the size never grows. The 14 structures of the code of this page are smallest AIGs of their classes: an exhaustive search over all AIGs of at most 5 nodes, run by the test file, finds each of their sizes, and it finds no AIG of 5 or fewer nodes for the two classes of size 6.

**What is not proved.** The result is not a smallest AIG. A pass only sees cuts of at most $K$ leaves, accepts a change only when it saves nodes now, and visits the nodes once, so it stops at a local optimum. The 4-input subgraphs of the paper are not all smallest AIGs of their functions. They are the subgraphs with no redundant nodes that the precomputation found, and some classes are left out. The depth can grow when a change makes a longer path.

**What is measured.** On 300 random AIGs with 6 inputs, 50 calls of AND and 3 outputs each (seed 3), the code of this page lowered the mean number of AND nodes that the outputs reach from 23.3 to 10.3 in one pass, and a second pass lowered it to 10.0. Random AIGs have much redundant logic, so this shows only that the code works. It is not a benchmark result. The paper reports its own results on benchmark circuits.

## Variants and improvements

- **Zero-gain changes.** Accepting changes with gain 0 does not shrink the graph, but it changes its shape, and a later pass can then find gains. ABC offers this as an option of rewrite.
- **Keeping the depth.** The rewrite command of ABC can reject a change that raises the level of the node, so that rewriting for area and [AIG balancing](/aig-balancing/) for depth work together in scripts such as resyn2.
- **Refactoring and resubstitution.** Refactoring takes a larger cut of a node, often 10 or more leaves, computes a factored form of its function, and keeps it when it saves nodes. Resubstitution tries to express a node with nodes that already exist, sometimes with don't-cares.
- **Exact libraries.** With [exact synthesis](/exact-synthesis/) by SAT, the library can hold proved smallest AIGs for every NPN class of 4 inputs, and for many classes of 5 or 6 inputs. Exact synthesis on the fly for larger cuts is slower but finds more.
- **Choices.** Instead of replacing the old logic, a pass can keep both versions as structural choices, and let [technology mapping](/technology-mapping/) pick between them.
- **Other graphs.** The same scheme works on the [majority-inverter graph](/majority-inverter-graph/) with a library of majority structures, and on XOR-AND graphs.

## When to use it

Use rewriting as the main area pass on AIGs, alternating with [balancing](/aig-balancing/), before [technology mapping](/technology-mapping/) or before a SAT based check, where fewer nodes mean a smaller CNF. It is fast, and many passes are cheap. It finds local redundancy well. It does not find logic sharing across distant parts of a circuit, which [SAT sweeping](/sat-sweeping/) finds, and it does not use the don't-cares of the network unless a variant with don't-cares is used.

## Pitfalls

- **Counting the tree, not the DAG.** The gain must subtract only the nodes of the fanout-free cone. A node that has other fanouts stays, and the example above shows how counting it predicts a saving that does not happen.
- **Counting a reused cone node as free.** If the new structure reuses a node of $M$ through the hash table, that node is no longer freed, and it must count as added. Without this rule the predicted gain is too high, and the change can even rebuild $v$ over itself and make a cycle.
- **Stale fanouts after a merge.** When a fanout of $v$ becomes equal to another node, its own fanouts must move too, and a node that was already replaced must be followed to its replacement. A chain of merges is common after a change.
- **Wrong transform direction.** The transform maps the table of the cut to the class representative. Building the representative's structure needs the inverse map on the leaves, and the output phase must be put back. A test that compares the tables before and after a change catches this at once.
- **Calling the subgraphs optimal.** The library of the paper holds non-redundant subgraphs, not proved smallest ones, and the rewriting is a local search, so neither the structures nor the result are optimal.

## Implementations

## History

Rewriting circuits with local rules goes back to the transformation systems of the 1980s, such as the rule based LSS system of IBM. Bjesse and Borälv (2004) compressed AIGs for formal verification by replacing small cuts with precomputed structures while counting the shared nodes, and the 2006 paper builds on their work. Mishchenko, Chatterjee and Brayton (2006) made the method fast enough for synthesis, with the NPN classes of 4-input functions, a shared library of non-redundant subgraphs, and the gain over the maximum fanout-free cone. They reported that scripts of rewriting and balancing on AIGs give results close to those of the older SOP based scripts in much less run time. Their method became the rewrite command of ABC, which Brayton and Mishchenko (2010) describe as the base of its synthesis.

## References
