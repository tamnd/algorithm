---
tag: PGBE80
kind: data-structure
slug: and-inverter-graph
name: And-inverter graph
aliases:
- AIG
area: eda/logic-synthesis
level: core
summary: A Boolean network of two-input AND nodes with optional inverted edges, kept free of duplicate nodes by structural hashing, the main form of modern logic synthesis.
model: word-ram
complexity:
  vars: {N: the number of AND nodes, n: the number of primary inputs, w: the number of bits in a machine word}
  time: {and: O(1) expected, simulate: O(N 2^n / w), levels: O(N)}
  space: {nodes: O(N)}
properties: {persistent: true, concurrent: false, external: false}
history:
  year: 2002
  people: [Andreas Kuehlmann, Viresh Paruthi, Florian Krohm, Malay K. Ganai]
  note: Kuehlmann, Paruthi, Krohm and Ganai described the structurally hashed AND graph with complemented edges as the core of a combined SAT, BDD and simulation engine for equivalence checking. The ABC system of Brayton and Mishchenko made it the main form of logic synthesis.
prereqs: [boolean-network, hash-consing, directed-acyclic-graph]
see_also: [binary-decision-diagram, aig-balancing, aig-rewriting, majority-inverter-graph, sat-sweeping, tseitin-transformation, bit-blasting, boolean-equivalence-checking]
sources:
  - paper: doi:10.1109/TCAD.2002.804386
    title: Andreas Kuehlmann, Viresh Paruthi, Florian Krohm and Malay K. Ganai, Robust Boolean reasoning for equivalence checking and functional property verification, IEEE Transactions on Computer-Aided Design 21(12), 2002, pages 1377 to 1394
    locator: the AND graph with complemented edges, structural hashing of the two fanins, and its use with SAT, BDDs and random simulation
  - paper: doi:10.1007/978-3-642-14295-6_5
    title: Robert Brayton and Alan Mishchenko, ABC, an academic industrial-strength verification tool, Computer Aided Verification (CAV 2010), Lecture Notes in Computer Science 6174, Springer, 2010, pages 24 to 40
    locator: the AIG as the common form of the synthesis and verification engines of ABC
  - paper: doi:10.1145/1146909.1147048
    title: Alan Mishchenko, Satrajit Chatterjee and Robert Brayton, DAG-aware AIG rewriting, a fresh look at combinational logic synthesis, Proceedings of the 43rd Design Automation Conference, 2006, pages 532 to 535
    locator: the AIG of the paper, its structural hashing and its node count as the cost of synthesis
---

An and-inverter graph, or AIG, is a [Boolean network](/boolean-network/) in which every inner node is an AND of two inputs and every edge may carry an inverter. It is a [directed acyclic graph](/directed-acyclic-graph/) whose sources are the primary inputs and the constant 0, and each primary output is an edge, possibly inverted, to one node. A hash table on the pair of fanins makes sure that no two nodes have the same two fanins, which is [hash consing](/hash-consing/) applied to circuits and is called structural hashing. AND and NOT can express every Boolean function, so an AIG can hold any circuit, at the cost of a few nodes for each XOR or multiplexer.

## In plain words

Draw a circuit with only one kind of gate, a two-input AND. To get NOT, put a small dot on a wire. OR is an AND with dots on its two inputs and on its output. With these two parts you can build every circuit.

Keep a dictionary of every gate you have built, keyed by its two input wires. Before you build a new gate, look it up. If the same gate is already there, use the old one. So the graph never holds two copies of the same gate, and shared logic is shared by itself.

The graph is small and simple to walk, and every program in a tool chain can read it. It does not decide by itself if two gates compute the same thing, because two different shapes can give the same function.

## The abstract type

An AIG over the inputs $x_1, \ldots, x_n$ stores a set of nodes, each one a Boolean function of the inputs. A *literal* names a node and a phase: the node itself or its complement. The operations are:

- INPUT(i): the literal of $x_i$.
- AND(a, b): a literal whose function is $f_a \wedge f_b$. NOT(a) is free: it flips the phase of $a$. OR, XOR and MUX are made from AND and NOT.
- SIMULATE(o_1, ..., o_k): the truth tables of the given literals.
- LEVELS: the depth of each node, the number of AND nodes on the longest path from an input.

The contract of AND is that the function is right and that no node is ever added twice for the same pair of fanins. Two literals with the same function may still differ, so the type gives no constant-time equality test of functions. That is the main difference from the [ROBDD](/reduced-ordered-bdd/), where equal functions have equal nodes.

## Representation

A literal is the integer $2v + c$, where $v$ is the node number and $c = 1$ means a complemented edge. Node 0 is the constant 0, so the literal 0 is false and the literal 1 is true. Nodes 1 to $n$ are the inputs. Every later node $v$ holds two fanin literals $a < b$ of older nodes, in two arrays fanin0 and fanin1. A hash table maps the pair $(a, b)$ to $v$. The node numbers are a topological order, since a node is made after its fanins. This is also the literal code of the AIGER file format, which most tools use to exchange AIGs.

## Operations

```pseudo id=main
AND(a, b)
L1  if a > b then swap a and b                       ▷ one order for each pair
L2  if a = 0 then return 0                           ▷ x ∧ 0 = 0
L3  if a = 1 then return b                           ▷ x ∧ 1 = x
L4  if a = b then return a                           ▷ x ∧ x = x
L5  if a = b xor 1 then return 0                     ▷ x ∧ ¬x = 0
L6  if T holds the key (a, b) then return 2·T[a, b]  ▷ structural hashing
L7  v ← a new node with fanins (a, b); T[a, b] ← v; return 2v

SIMULATE(o_1, ..., o_k)                ▷ truth tables as integers of 2^n bits
L8  val[0] ← 0; val[i] ← the table of x_i for i = 1 to n
L9  for v ← n + 1 to the last node: val[v] ← lit(fanin0[v]) ∧ lit(fanin1[v])
L10 return lit(o_1), ..., lit(o_k)     ▷ lit(2u + c) = val[u], complemented if c = 1
```

Line L1 fixes one order for the two fanins, so that $a \wedge b$ and $b \wedge a$ find the same key. Lines L2 to L5 remove the cases where the result is a constant or an old literal, so no node has a constant fanin, two equal fanins or two opposite fanins. Line L6 is the hash lookup. NOT(a) returns $a \oplus 1$ and adds nothing. OR(a, b) is $\neg(\neg a \wedge \neg b)$, one node. XOR(a, b) is $\neg(a \wedge b) \wedge \neg(\neg a \wedge \neg b)$, three nodes, and MUX(s, t, e) is $\neg(\neg(s \wedge t) \wedge \neg(\neg s \wedge e))$, also three nodes.

SIMULATE keeps one integer of $2^n$ bits for each node, bit $m$ being the value at input point $m$, with $x_1$ the high bit as in [sum of products](/sum-of-products/). Line L9 does one machine AND per word, so all points are simulated at once. With random words in place of full tables, the same loop is the random simulation that equivalence checkers run first to split nodes into candidate classes.

## Example

Build a full adder with sum $s = a \oplus b \oplus c$ and carry $= ab + c(a \oplus b)$, over the inputs $a, b, c$ with literals 2, 4 and 6.

| step | call | key | result | nodes |
|---|---|---|---|---|
| 1 | AND(2, 4), the $a b$ of $t = a \oplus b$ | (2, 4) | new node 4, literal 8 | 1 |
| 2 | AND(3, 5), the $\bar{a}\bar{b}$ of $t$ | (3, 5) | new node 5, literal 10 | 2 |
| 3 | AND(9, 11), so $t = 12$ | (9, 11) | new node 6, literal 12 | 3 |
| 4 | AND(12, 6), the $t c$ of $s$ | (6, 12) | new node 7, literal 14 | 4 |
| 5 | AND(13, 7), the $\bar{t}\bar{c}$ of $s$ | (7, 13) | new node 8, literal 16 | 5 |
| 6 | AND(15, 17), so $s = 18$ | (15, 17) | new node 9, literal 18 | 6 |
| 7 | AND(2, 4), the $a b$ of the carry | (2, 4) | found node 4, literal 8 | 6 |
| 8 | AND(12, 6), the $t c$ of the carry | (6, 12) | found node 7, literal 14 | 6 |
| 9 | AND(9, 15), carry $= 21$ | (9, 15) | new node 10, literal 20, then NOT | 7 |

Steps 7 and 8 find the nodes of steps 1 and 4 in the table, so the carry costs one new node, and the adder has 7 AND nodes in all. SIMULATE gives the tables 240, 204 and 170 for $a$, $b$ and $c$, 150 (the bits 10010110) for the sum and 232 (the bits 11101000) for the carry. The deepest node is node 9 at level 4, and the carry is at level 4 too. In step 4, line L1 swaps the call AND(12, 6) to the key (6, 12).

Structural hashing does not find every equal pair. In a new AIG, AND(AND(a, b), c) and AND(a, AND(b, c)) give two different literals, 10 and 14, with the same table 128. Finding that two such literals are equal needs a [SAT](/sat/) call or a BDD, which is what [SAT sweeping](/sat-sweeping/) does.

## Correctness

The [full proof](proofs/correctness.md) shows two invariants. First, every AND node $v$ has fanins $2 \le a < b$ with $a \ne b \oplus 1$ and both from nodes older than $v$, and the table maps each node's pair to that node and holds no other key. Second, AND(a, b) returns a literal whose function is $f_a \wedge f_b$: lines L2 to L5 are the identities $x \wedge 0 = 0$, $x \wedge 1 = x$, $x \wedge x = x$ and $x \wedge \neg x = 0$, line L6 returns a node whose fanins are exactly $a$ and $b$, and line L7 makes one. From the first invariant, no two AND nodes share a pair of fanins, and the graph has no cycle. SIMULATE is right by induction on the node number, since the fanins of a node come before it.

## Complexity

AND does a constant number of steps and one hash lookup, so it takes $O(1)$ expected time. SIMULATE takes $O(N 2^n / w)$ word operations for $N$ nodes and $n$ inputs, or $O(N r / w)$ for $r$ random patterns. LEVELS is one pass in $O(N)$. The space is two integers for each node and one table entry, $O(N)$.

The size of an AIG is close to the size of the circuit it comes from. A circuit of $s$ two-input AND, OR and NOT gates gives at most $s$ AND nodes. A circuit with XOR gates gives at most three nodes for each. The parity of $n$ inputs needs $3(n - 1)$ AND nodes, while its smallest sum of products has $2^{n-1}$ cubes, and an ROBDD of parity has $2n - 1$ inner nodes in any order. The ROBDD of a multiplier is exponential in every order (Bryant 1991), while its AIG has $O(n^2)$ nodes. This size bound is why tools keep the AIG as the main form and build BDDs only for small parts.

## Variants

- **Complemented edges on BDDs.** The same trick of a bit on the edge is used by [complemented edges](/complemented-edges/) in BDD packages, where it also keeps the diagram canonical.
- **Functionally reduced AIGs.** A FRAIG merges every two nodes with the same function, found by simulation and SAT, so that equal functions get equal literals. See [SAT sweeping](/sat-sweeping/).
- **Hashing two levels.** Some packages also look up small patterns of two levels, so that, for example, $(a \wedge b) \wedge (a \wedge c)$ and $a \wedge (b \wedge c)$ meet. This finds more sharing, but the result still depends on the order of construction.
- **Sequential AIGs.** Latches are kept as extra inputs and outputs, and the AIGER format lists them with their next-state literals.
- **Other node types.** The [majority-inverter graph](/majority-inverter-graph/) uses three-input majority nodes, and XOR-AND graphs add an XOR node, which suits arithmetic and cryptographic circuits.

## When to use it

Use an AIG as the main form of a combinational or sequential circuit in a synthesis or verification tool. It is small, its size grows like the circuit, it turns into CNF with three clauses per node by the [Tseitin transformation](/tseitin-transformation/), and the [bit-blasting](/bit-blasting/) of word-level formulas gives one directly. Most of the work on it is local: [AIG balancing](/aig-balancing/) for depth, [AIG rewriting](/aig-rewriting/) for size, and [technology mapping](/technology-mapping/) over [cuts](/k-feasible-cut/). Use a [binary decision diagram](/binary-decision-diagram/) when you need equality of functions in constant time or counts of solutions, and the function is small enough for one.

## Pitfalls

- **No order on the key.** Without line L1, AND(a, b) and AND(b, a) make two nodes for one gate.
- **Hashing before the trivial rules.** Lines L2 to L5 must come before the lookup. Otherwise the graph gets nodes such as $x \wedge \neg x$, which are constant but look like gates.
- **Treating hashing as a canonical form.** Two literals with the same function can differ, as the example shows. A tool that tests equality of literals as equality of functions misses most equivalences.
- **Forgetting the output phase.** An output is a literal, and its complement bit is part of the function. A simulator that reads only the node number gives the wrong table for half of the outputs.
- **Counting inverters as nodes.** Inverters are bits on edges and cost nothing. The size of an AIG is the number of AND nodes, and its depth counts only AND nodes.

## Implementations

## History

Graphs of AND gates and inverters are as old as switching theory, but their use as a shared, hashed data structure came from equivalence checking in the 1990s. Kuehlmann, Paruthi, Krohm and Ganai (2002) gave the form used today: an AND graph with complemented edges, structural hashing of the fanins, and SAT, BDD and simulation engines that work on it together. Mishchenko, Chatterjee and Brayton (2006) showed that synthesis can work on the AIG directly with local rewriting, and the ABC system of Brayton and Mishchenko (2010) made the AIG the common form of its synthesis, mapping and verification commands. Biere's AIGER format with the literal code $2v + c$ became the standard file format, and the hardware model checking competitions use it.

## References
