---
tag: D7SVKR
kind: algorithm
slug: sat-sweeping
name: SAT sweeping
aliases:
- FRAIG construction
- functional reduction
area: cad/logic-synthesis
level: advanced
summary: Finds internal nodes that are equal or complementary by random simulation, proves each candidate pair with SAT, and merges proven pairs, for equivalence checking.
solves: [boolean-equivalence-checking]
model: word-ram
complexity:
  vars: {N: the number of AND nodes, W: the number of simulation patterns at the end, T: the cost of one SAT call on a miter}
  time: {worst: O(N^2 (N W + T))}
  space: {extra: O(N W)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2004
  people: [Andreas Kuehlmann, Alan Mishchenko, Satrajit Chatterjee, Roland Jiang, Robert Brayton]
  note: Kuehlmann named SAT sweeping in 2004, for simplifying the transition relation in bounded property checking. Mishchenko, Chatterjee, Jiang and Brayton built functionally reduced AIGs (FRAIGs) with it in 2005.
prereqs: [and-inverter-graph, sat, tseitin-transformation]
see_also: [boolean-equivalence-checking, equivalence-checking, cdcl, incremental-sat, bounded-model-checking, aig-rewriting, priority-cuts, bit-parallelism]
sources:
  - paper: doi:10.1109/ICCAD.2004.1382542
    title: Dynamic transition relation simplification for bounded property checking
    locator: Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD 2004), pages 50 to 57; SAT sweeping of the AIG of the unrolled transition relation
  - paper: "Alan Mishchenko, Satrajit Chatterjee, Roland Jiang and Robert Brayton, FRAIGs: a unifying representation for logic synthesis and verification, ERL technical report, EECS Department, University of California, Berkeley, March 2005"
    title: "FRAIGs: a unifying representation for logic synthesis and verification"
    locator: the definition of a functionally reduced AIG and its construction by simulation and SAT (general locator)
  - paper: "Alan Mishchenko, Satrajit Chatterjee, Robert Brayton and Niklas Een, Improvements to combinational equivalence checking, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD 2006)"
    title: Improvements to combinational equivalence checking
    locator: SAT sweeping of a miter for combinational equivalence checking, with counterexample simulation and resource limits (general locator, not checked)
---

SAT sweeping finds and merges the nodes of an [and-inverter graph](/and-inverter-graph/) that compute the same function, or the complement of the same function. It simulates the graph on random input patterns to give each node a signature, and nodes whose signatures agree, after complement, are candidates. Each candidate pair is checked by a [SAT](/sat/) solver on the miter of the two nodes, the [Tseitin](/tseitin-transformation/) clauses of their cones plus the condition that they differ. If the miter is unsatisfiable, the two nodes are equal and one replaces the other. If it is satisfiable, the model is an input pattern that tells them apart, and it is added to the simulation patterns, which can also split other false candidates. Kuehlmann named the method in 2004, and Mishchenko, Chatterjee, Jiang and Brayton called its result a functionally reduced AIG, or FRAIG, in 2005: no two nodes of a FRAIG compute the same function or complementary functions. Applied to the miter of two circuits, it is the core of combinational [equivalence checking](/boolean-equivalence-checking/) in tools such as ABC.

## In plain words

A large circuit often computes the same signal in two places. Finding these places makes the circuit smaller, and if two circuits are compared, it splits one hard question into many easy ones.

First, feed the circuit some random inputs and record what each wire does. Two wires that do different things on some input are surely different. Two wires that always did the same thing, or always the opposite, might be equal.

For each such pair, ask a SAT solver for an input that makes them differ. If there is none, they are equal, so keep one and drop the other. If there is one, use it as a new random input, which may also show other pairs to be different.

## The problem

The input is an AIG with $n$ inputs, $N$ AND nodes in topological order and a list of output literals, in the notation of the [AIG page](/and-inverter-graph/): node 0 is the constant 0, a literal is $2v + c$, and $c = 1$ complements node $v$. The output is an AIG that computes the same output functions and is *functionally reduced*: no two of its nodes, the constant and the inputs included, compute functions $f$ and $g$ with $f = g$ or $f = \neg g$. As a problem this is [Boolean equivalence checking](/boolean-equivalence-checking/) for every pair of nodes at once. It is co-NP-hard: a circuit is unsatisfiable exactly when its output node is equal to the constant 0, and a functionally reduced result shows this at once, because the output then is the constant node.

## The algorithm

```pseudo id=main
SAT-SWEEP(G, W0)
L1  P ← W0 random input patterns; H ← an empty AIG with the inputs of G
L2  for each AND node v of G in topological order do
L3      w ← the AND in H of the images of the fanins of v, with constant rules and structural hashing
L4      if w is an old node of H then image(v) ← w; continue
L5      loop
L6          s ← the signature of w under P; r ← a node of H other than w with signature s or ¬s
L7          if there is no r then image(v) ← w; break
L8          if the miter of w and r, or of w and ¬r, is unsatisfiable then
L9              image(v) ← r with the phase; point the hash entry of w at it; drop w; break
L10         else add the model of the miter to P and simulate H again
L11 return the cones in H of the images of the outputs of G
```

The signature of a node at line L6 is its value on each pattern of $P$, a word of bits computed by bit-parallel simulation, as on the page on [bit parallelism](/bit-parallelism/). To compare up to complement, the signature is complemented when its bit for pattern 0 is 1, so that equal and complementary nodes get the same key. A hash table from keys to nodes finds $r$. The phase is the bit of pattern 0 in $s \oplus \mathrm{sig}(r)$. At line L8, the miter is the CNF of the cones of $w$ and $r$ by the Tseitin transformation, plus the two clauses $(w \lor r') \land (\neg w \lor \neg r')$, where $r'$ is $r$ with the phase, which say that the two differ. Line L9 points the hash entry of the dropped AND at $r$, so that a later AND with the same fanins also gets $r$. Line L10 adds one bit to every signature, and the new bit differs between $w$ and $r$, so the loop tries $r$ at most once.

## Example

Take inputs $x$ and $y$ and the AIG with
$t_3 = x \land \neg y$, $t_4 = \neg x \land y$, $t_5 = \neg t_3 \land \neg t_4$ (XNOR), $t_6 = x \land y$, $t_7 = \neg x \land \neg y$, $t_8 = \neg t_6 \land \neg t_7$ (XOR) and $o = t_9 = \neg t_5 \land t_8$, whose function is XOR. The code of this page with 4 patterns and seed 3 gets the patterns $(x, y) = (1, 1), (1, 0), (0, 0), (0, 1)$ for $p_0, p_1, p_2, p_3$.

| node | function | signature $p_0 p_1 p_2 p_3$ | result |
|---|---|---|---|
| $x$ | $x$ | 1100 | input |
| $y$ | $y$ | 1001 | input |
| $t_3$ | $x \land \neg y$ | 0100 | new class |
| $t_4$ | $\neg x \land y$ | 0001 | new class |
| $t_5$ | XNOR | 1010 | new class |
| $t_6$ | $x \land y$ | 1000 | new class |
| $t_7$ | $\neg x \land \neg y$ | 0010 | new class |
| $t_8$ | XOR | 0101 | candidate $\neg t_5$; SAT says UNSAT; $t_8 \to \neg t_5$ |
| $t_9$ | $\neg t_5 \land \neg t_5$ | | the rule $a \land a = a$ gives $\neg t_5$ |

The signature of $t_8$ is the complement of that of $t_5$, so the pair is a candidate, and the miter is unsatisfiable. The image of $t_8$ is $\neg t_5$. At $t_9$, both fanins become $\neg t_5$, so the AND is not even built. The output is $\neg t_5$, and the cone of the output has the three ANDs $t_3$, $t_4$ and $t_5$. The nodes $t_6$ and $t_7$ stay in $H$ but leave the result at line L11. One SAT call was made.

With one pattern only, the same run makes 3 SAT calls that find counterexamples before the one UNSAT call, since a single pattern gives many nodes the same key.

## Correctness

The [full proof](proofs/correctness.md) shows that the image of every node of $G$ computes the same function as the node, so the outputs are kept, and that the nodes of $H$ that stay are pairwise not equal and not complementary. The second fact holds because a node joins $H$ only when no node has its key, and a node with a different signature is surely different. A dropped node is used by no other node, because it is dropped at once. The loop of lines L5 to L10 ends, because each counterexample separates $w$ from one more node for good.

## Complexity

One simulation of $H$ costs $O(N W)$ bit operations, or $O(N W / w)$ word operations with machine words of $w$ bits. For a new node, each SAT call at line L8 either merges it or separates it from one node, so there are at most $N + n + 1$ calls for that node and $O(N^2)$ calls in all, in the worst case. Each call costs $T$, the cost of the SAT solver on a miter of at most $N$ AND nodes, which is exponential in the number of inputs of the cones in the worst case, since the problem is co-NP-hard. This gives $O(N^2 (N W + T))$. In practice most candidates are true, few calls return SAT, and the simulation is redone only for the new bit. The signatures take $O(N W)$ bits.

## Properties

**What is proved.** The result computes the same output functions as $G$. It is functionally reduced: no two of its nodes are equal or complementary, and no node is equal to a constant or to an input or its complement. Each merge is backed by an UNSAT answer of the solver, and each split by a counterexample that can be checked by simulation. Each AND node of the result was built for a different AND node of $G$, so the result has at most $N$ AND nodes.

**What is not proved.** A FRAIG is not a smallest AIG for its functions, and it depends on the order of the nodes. The number of SAT calls depends on the patterns, and with too few patterns it can be large. When a solver has a limit on its effort, as real tools set, an undecided pair is left unmerged, and the result is then not functionally reduced.

**What is measured.** On the test set of this page, 150 random AIGs with at most 8 inputs and 25 ANDs (seed 2) and 1, 4 or 16 starting patterns, the sweep made 389 SAT calls that found a counterexample and 207 that proved a merge. This is a small test run, not a benchmark result.

## Variants and improvements

- **Incremental SAT.** Real implementations keep one solver for the whole sweep, add the clauses of each node once, and ask each miter under assumptions, as in [incremental SAT](/incremental-sat/) with a [CDCL](/cdcl/) solver.
- **Effort limits.** A limit on the number of conflicts per call stops hard pairs from blocking the sweep. The pairs that fail are left alone or tried again later with a larger limit.
- **Better patterns.** Tools simulate many words of patterns at once, and they also add patterns near each counterexample, so that one model splits more classes.
- **Equivalence checking.** For two circuits, sweep the miter of their outputs. If the circuits are equal, the sweep reduces every output of the miter to the constant 0. Mishchenko, Chatterjee, Brayton and Eén (2006) improved this flow.
- **Choices instead of merges.** Keep the proved equal nodes as a class of choices instead of dropping them. A mapper such as [priority cuts](/priority-cuts/) can then pick the best structure.
- **Sequential sweeping.** Signal correspondence finds nodes equal in all reachable states with simulation and induction, the sequential form of the same idea.

## When to use it

Use SAT sweeping to check two combinational circuits for equality after synthesis, to shrink an AIG before [bounded model checking](/bounded-model-checking/) or other SAT queries, and to find structural choices for mapping. For a single pair of small functions, a [BDD](/reduced-ordered-bdd/) or one SAT call on the outputs may be simpler. Note that [equivalence checking](/equivalence-checking/) of transition systems up to bisimulation is a different problem.

## Pitfalls

- **Comparing only equal signatures.** Normalize the phase, for example by pattern 0, or complementary nodes are never found.
- **Keeping the dropped node in the hash table.** A later AND with the same fanins must get the kept node, not a new copy of the dropped one.
- **Merging on simulation alone.** Equal signatures are only a hint. Without the SAT proof, a merge can change the function.
- **Dropping a node that is used.** Decide on a node as soon as it is built, before any other node reads it. A node that is merged later must have its fanouts moved first.
- **Missing the constants.** Put the constant node and the inputs in the table of keys, so that a node that is always 0 or equal to an input is found.

## Implementations

## History

Brand (1993) used internal equivalences found by test generation to check large synthesized designs. Kuehlmann and Krohm (1997) combined structural hashing with BDD and SAT checks of internal points for equivalence checking, which led to the AIG based checkers. In 2004 Kuehlmann named SAT sweeping and used it to simplify the transition relation of bounded property checking. In 2005 Mishchenko, Chatterjee, Jiang and Brayton defined functionally reduced AIGs and built them by simulation and SAT, and the ABC system uses them for equivalence checking, for choices in mapping and as a basic step of synthesis.

## References
