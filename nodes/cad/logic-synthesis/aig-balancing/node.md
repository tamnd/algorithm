---
tag: AX6R7V
kind: algorithm
slug: aig-balancing
name: AIG balancing
aliases:
- tree height reduction of AND trees
area: cad/logic-synthesis
level: core
summary: Collects the maximal multi-input AND trees of an AIG and rebuilds each one over its distinct leaves, pairing the two lowest leaves first, so no node gets deeper or more numerous.
solves: [multi-level-logic-synthesis]
model: word-ram
complexity:
  vars: {N: the number of AND nodes of the input AIG, k: the largest number of leaves of one supergate}
  time: {worst: O(N log k) expected}
  space: {extra: O(N)}
properties: {deterministic: true, exact: false, online: false, recursive: true}
history:
  year: 2006
  people: [Alan Mishchenko, Satrajit Chatterjee, Robert Brayton]
  note: Tree height reduction is old in compilers and in SIS. Mishchenko, Chatterjee and Brayton paired AIG balancing, which lowers depth with no gain in area, with DAG-aware rewriting in ABC.
prereqs: [and-inverter-graph, huffman-coding, dag-longest-path]
see_also: [aig-rewriting, majority-inverter-graph, multi-level-logic-synthesis, parallel-prefix, greedy-algorithm, technology-mapping, hash-consing, boolean-network]
sources:
  - paper: doi:10.1145/1146909.1147048
    title: Alan Mishchenko, Satrajit Chatterjee and Robert Brayton, DAG-aware AIG rewriting, a fresh look at combinational logic synthesis, Proceedings of the 43rd Design Automation Conference, 2006, pages 532 to 535
    locator: the abstract and the experiments, where AIG balancing for delay is used together with rewriting for area
  - paper: "Martin Charles Golumbic, Combinatorial merging, IEEE Transactions on Computers C-25(11), 1976, pages 1164 to 1167"
    locator: the merge of the two smallest values with cost max plus one, and its optimality for the least height of a tree with given leaf values
  - paper: doi:10.1007/978-3-642-14295-6_5
    title: Robert Brayton and Alan Mishchenko, ABC, an academic industrial-strength verification tool, Computer Aided Verification (CAV 2010), Lecture Notes in Computer Science 6174, Springer, 2010, pages 24 to 40
    locator: the synthesis commands of ABC on AIGs, among them balance
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 8, Multiple-Level Combinational Logic Optimization (the sections on delay and on restructuring for timing)
---

AIG balancing is a fast pass of [multi-level logic synthesis](/multi-level-logic-synthesis/) that lowers the depth of an [and-inverter graph](/and-inverter-graph/). It cuts the AIG into *supergates*, maximal trees of AND nodes joined by plain edges, where every inner node has one fanout. Each supergate computes the AND of its leaves, and the order in which the two-input ANDs join the leaves does not change the function. So the algorithm rebuilds each supergate from the bottom up, always joining the two leaves of lowest level first, as Huffman's algorithm joins the two smallest weights. No node of the result is deeper than the node it replaces, and the number of AND nodes does not grow.

## In plain words

A long chain of AND gates computes the same thing as a short, bushy tree of AND gates over the same inputs. The chain is slow, because a signal at the bottom goes through every gate. The tree is fast.

So find every place in the circuit where AND gates feed only each other with no inverter between them, and treat the whole group as one big AND gate with many inputs. Throw out repeated inputs. Then build it again from two-input gates, as a tree. Signals that come late should go through few gates, so join the two signals that are ready first, then the next two, and so on. Do this from the inputs up to the outputs, so each group sees the new, earlier times of the groups below it.

## The problem

The input is an AIG with outputs $o_1, \ldots, o_k$. The output is an AIG with the same output functions. The level of an input is 0 and the level of an AND node is one more than the larger level of its two fanins, and the depth is the largest level of an output. The aim is a small depth, with no more AND nodes than before. Balancing only regroups AND trees. It does not use the distributive law or any Boolean identity other than $x \wedge x = x$, $x \wedge \neg x = 0$ and the order of the fanins, so it is a heuristic for the depth of the whole circuit.

## The algorithm

```pseudo id=main
BALANCE(G, o_1, ..., o_k)
L1  H ← an empty AIG on the inputs of G; memo ← empty
L2  for each output o: the new output is BAL(node(o)), complemented if o is

BAL(v)                         ▷ returns a literal of H with the function of v
L3  if v is an input or the constant then return the literal of v
L4  if memo holds v then return memo[v]
L5  leaves ← the leaf literals of the supergate of v
L6  S ← the set { BAL(node(ℓ)), complemented as ℓ is : ℓ in leaves }, without the constant 1
L7  if S holds 0, or some x and ¬x, then r ← 0
    else
L8      Q ← a priority queue of S keyed by the level in H
L9      while |Q| > 1: take the two lowest x and y out of Q; put AND_H(x, y) into Q
L10     r ← the one literal left in Q, or 1 if Q is empty
L11 memo[v] ← r; return r
```

The supergate of an AND node $v$ is found by a walk from $v$ down its fanins. The walk goes down a fanin edge when the edge has no inverter and leads to an AND node with exactly one fanout. Every other fanin is a leaf. The fanout counts are taken over the nodes that the outputs reach, and an output counts as a fanout. A node with two fanouts is never inside a supergate, so its logic is built once and shared.

Line L6 balances each leaf first, so the queue of line L8 knows the new levels of the leaves. As a set, $S$ drops leaves that appear twice. Line L7 finds a supergate that is 0 because it holds a literal and its complement. AND_H is the AND of the [AIG](/and-inverter-graph/) page, with the trivial rules and [structural hashing](/hash-consing/), so equal pairs in different supergates become one node.

## Example

Take the chain $o = a \wedge (b \wedge (c \wedge (d \wedge e)))$, with the literals 2, 4, 6, 8 and 10 for $a$ to $e$. It has 4 AND nodes and depth 4. The supergate of the top node has the five leaves $a$ to $e$, all at level 0.

| step | queue before (level, literal) | pair taken | new node | level |
|---|---|---|---|---|
| 1 | (0, 2), (0, 4), (0, 6), (0, 8), (0, 10) | $a$, $b$ | 12 | 1 |
| 2 | (0, 6), (0, 8), (0, 10), (1, 12) | $c$, $d$ | 14 | 1 |
| 3 | (0, 10), (1, 12), (1, 14) | $e$, $ab$ | 16 | 2 |
| 4 | (1, 14), (2, 16) | $cd$, $abe$ | 18 | 3 |

The result $(c \wedge d) \wedge (e \wedge (a \wedge b))$ has 4 AND nodes and depth 3, which is $\lceil \log_2 5 \rceil$.

Levels of leaves matter when a leaf is shared. Let $s = (a \wedge b) \wedge (c \wedge d)$ be an output and also a fanin of the second output $o_2 = e \wedge (f \wedge s)$. The node $s$ has two fanouts, so it is a leaf of the supergate of $o_2$, at level 2. The supergate of $o_2$ has the leaves $e$, $f$ at level 0 and $s$ at level 2. The queue joins $e$ and $f$ first, at level 1, and then joins that node with $s$, at level 3. The depth falls from 4 to 3, and both graphs have 5 AND nodes.

## Correctness

The [full proof](proofs/correctness.md) shows three facts. First, BAL(v) has the function of $v$: the AND of a set of literals does not depend on the order or the grouping of the two-input ANDs, a repeated literal changes nothing, and a literal with its complement gives 0. Second, the level of BAL(v) in $H$ is at most the level of $v$ in $G$. Write $T(a_1, \ldots, a_m) = \lceil \log_2 \sum_i 2^{a_i} \rceil$. Every binary tree over leaves of levels $a_i$ has a root of level at least $T$, since a node of level $\ell$ over subtrees with sums $S_1$ and $S_2$ has $2^\ell \ge 2 \max(S_1, S_2) \ge S_1 + S_2$. The greedy pairing of line L9 never raises $T$ of the queue, which gives a root of level exactly $T$, the [greedy](/greedy-algorithm/) argument of Golumbic (1976). The new leaves are fewer and, by induction, not higher than the old ones, so their $T$ is not larger, and the old supergate was a tree over the old leaves. Third, each supergate with $p$ leaf edges has $p - 1$ AND nodes in $G$ and gets at most $p - 1$ new ones in $H$, and every AND node of $G$ that the outputs reach lies in exactly one supergate.

## Complexity

The walks of line L5 touch each AND node of $G$ once in all, since an inner node of a supergate has one fanout and so belongs to one supergate, and the memo of line L4 runs each supergate once. A supergate with $p$ leaves costs $O(p \log p)$ for the queue and $O(p)$ expected time for the hash lookups of AND_H. The sum of $p$ over all supergates is at most the number of edges, $2N$, so the time is $O(N \log k)$ expected, where $k$ is the largest supergate. The extra space is the memo, the fanout counts and the queue, $O(N)$. The recursion of line L6 can be as deep as the AIG, and a long AIG needs an explicit stack.

## Properties

**What is proved.** The functions of the outputs do not change. Every node of $H$ that replaces a node $v$ of $G$ has a level at most the level of $v$, so the depth does not grow. The number of AND nodes that the outputs reach does not grow. For each supergate, the tree that line L9 builds has the least level of any tree of two-input ANDs over the same distinct leaves at the same levels.

**What is not proved.** The depth of $H$ is not the least depth of an AIG for the same functions. Balancing keeps the supergates of $G$, so it cannot move logic across a node with two fanouts or across an inverter, and it never uses the distributive law. A chain of alternating AND and OR gates, $a \wedge (b \vee (c \wedge (d \vee e)))$, has an inverter on every edge of the AIG, so every supergate has two leaves, and balancing does not change it.

**What is measured.** On 1000 random AIGs with 8 inputs and 60 calls of AND each (seed 1, with each new node taking the last node as a fanin with probability 0.6 and each fanin complemented with probability 0.2), the code of this page lowered the mean depth from 14.7 to 7.2 and the mean number of reached AND nodes from 26.5 to 16.8, and it lowered the depth of 989 of them. Random AIGs have many repeated leaves and long chains, so these numbers show only that the code works. They are not benchmark results.

## Variants and improvements

- **Arrival times.** In timing-driven balancing the leaves of line L8 are keyed by arrival times from a delay model in place of AIG levels. The same greedy is optimal for any leaf times when each AND adds the same delay.
- **Balancing for area.** Some versions keep the shape of a supergate when the depth would not fall, which avoids changing nodes that other passes have tuned.
- **SOP balancing.** A later form of balancing in ABC takes a cut of several AND and OR levels, finds a [sum of products](/sum-of-products/) for it, and builds a balanced AND-OR tree, which can cross the inverters that stop plain balancing.
- **Other operators.** The same algorithm balances any associative and commutative operator. For XOR the rules of line L7 change to $x \oplus x = 0$, so a leaf that appears twice is dropped in pairs. For the [majority-inverter graph](/majority-inverter-graph/) the associativity axiom plays the role of line L9.
- **Compilers.** Tree height reduction of sums and products in expression trees is the same idea, and [parallel prefix](/parallel-prefix/) circuits solve the harder case where every prefix of a chain is needed.

## When to use it

Use balancing as a cheap first pass that removes the depth left by the source of an AIG, such as long chains from the [bit-blasting](/bit-blasting/) of wide gates, and between passes of [AIG rewriting](/aig-rewriting/) in scripts such as the resyn scripts of ABC. It is fast enough to run many times. When the depth comes from the logic and not from the grouping of AND gates, use restructuring that changes the function of nodes, such as rewriting with a delay cost or SOP balancing.

## Pitfalls

- **Going through shared nodes.** A node with two fanouts must be a leaf. If the walk of line L5 goes into it, its logic is copied into each supergate that uses it, and the node count grows.
- **Going through inverters.** The AND of $\neg(x \wedge y)$ with $z$ is not $x \wedge y \wedge z$. The walk must stop at a complemented edge.
- **Old levels for the leaves.** Line L8 must use the levels of the leaves in $H$, after line L6. With the levels of $G$, the queue joins the wrong pairs above leaves that balancing has already made shallower.
- **Joining in input order.** Joining the leaves in a fixed order, such as the order of the walk, gives a tree that is balanced only when all leaves arrive together. The two lowest leaves must be joined first.
- **Expecting a fixed point.** A second pass can still lower the depth, since hashing in the first pass can make nodes that a second pass sees as constant or shared.

## Implementations

## History

The reduction of tree height for associative operators comes from parallel compilation in the 1960s and 1970s, and Golumbic (1976) proved that joining the two smallest values first gives the least height for a tree with given leaf values, a minimax analogue of [Huffman coding](/huffman-coding/). Logic synthesis systems such as SIS used tree height reduction for timing. Mishchenko, Chatterjee and Brayton (2006) paired AIG balancing, which lowers delay with no gain in area, with [DAG-aware AIG rewriting](/aig-rewriting/), which lowers area with no gain in delay, and the balance command of ABC became a standard step of synthesis scripts.

## References
