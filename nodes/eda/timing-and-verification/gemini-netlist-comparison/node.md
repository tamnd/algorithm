---
tag: N08Y88
kind: algorithm
slug: gemini-netlist-comparison
name: Gemini netlist comparison
aliases:
- Ebeling netlist comparison
- Gemini LVS
- GeminiII
area: eda/timing-and-verification
level: advanced
summary: Ebeling and Zajicek's LVS algorithm that labels devices and nets by local invariants and refines the labels iteratively, then breaks ties by guessing.
model: word-ram
complexity:
  vars: {n: the number of devices, m: the number of nets, P: the number of pins}
  time: {one_refinement: O((n + m) (P + n + m) log(n + m)), with_guesses_no_backtracking: O((n + m)^2 (P + n + m) log(n + m)), with_backtracking_worst: 2^O((n + m) log(n + m))}
  space: {extra: O(n + m + P)}
properties: {deterministic: true, recursive: true, exact: true}
history:
  year: 1983
  people: [Carl Ebeling, Ofer Zajicek]
  note: Ebeling and Zajicek described Gemini at ICCAD 1983. Ebeling's GeminiII (ICCAD 1988) used the bipartite structure of the device and net graph to relabel faster, and SubGemini (DAC 1993) applied the method to finding subcircuits.
prereqs: [layout-versus-schematic, graph-isomorphism-problem, weisfeiler-leman]
see_also: [individualization-refinement, canonical-labeling, nauty, vf2-algorithm, subgraph-isomorphism, circuit-extraction, bipartite-graph, partition-refinement]
sources:
  - paper: "Carl Ebeling and Ofer Zajicek, Validating VLSI circuit layout by wirelist comparison, Proceedings of the IEEE International Conference on Computer-Aided Design (ICCAD) 1983, 172 to 173"
    locator: the reduction of layout validation to graph isomorphism of the device and net graphs, the iterative relabeling from neighbour labels, and the guess when labels stop splitting
  - paper: doi:10.1109/ICCAD.1988.122520
    title: Carl Ebeling, GeminiII, a second generation layout validation program, IEEE International Conference on Computer-Aided Design (ICCAD) 1988, Digest of Technical Papers, 322 to 325
    locator: the improved relabeling on the bipartite graph of devices and nets, and the reporting of differences
  - paper: doi:10.1145/157485.164556
    title: Miles Ohlrich, Carl Ebeling, Eka Ginting and Lisa Sather, SubGemini, identifying subcircuits using a fast subgraph isomorphism algorithm, Proceedings of the 30th Design Automation Conference, 1993
    locator: the use of the Gemini labels to find all instances of a small circuit in a large netlist
  - paper: "Daniel Neuen and Pascal Schweitzer, An exponential lower bound for individualization-refinement algorithms for graph isomorphism, Proceedings of the 50th ACM Symposium on Theory of Computing (STOC), 2018"
    locator: the graphs on which every individualization and refinement search visits exponentially many nodes
---

Gemini is an algorithm that decides whether two transistor netlists are the same circuit, and if they are, gives the matching of their devices and nets. It is the classic method for [layout versus schematic](/layout-versus-schematic/) checking: it gives each device and each net a label from local facts, refines the labels again and again from the labels of the neighbours, and when the labels stop splitting it pairs two vertices with the same label by a guess and goes on. Carl Ebeling and Ofer Zajicek published it in 1983, and Ebeling's GeminiII followed in 1988. The refinement step is [color refinement](/weisfeiler-leman/) run on the two netlists at the same time.

## In plain words

Two people draw the same circuit, but they name the wires differently and list the parts in another order. To check that the drawings agree, give every part and every wire a short description: "a transistor", "a wire that touches three parts". Then improve each description with the descriptions of its neighbours: "a transistor whose gate wire touches two parts". Do the same in both drawings at once, with the same rules.

If one drawing has more things with some description than the other, the drawings differ, and that description points to the place. If every description is unique, each thing matches the one thing with the same description in the other drawing. If some things still look alike, they are often copies of the same cell: pair one from each side by a guess, mark them, and go on.

## The problem

A netlist has devices and nets. Each device has a type, and each pin of a device has a *pin class* and a net. Pins of one class are interchangeable, like the source and the drain of a MOS transistor or the two ends of a resistor. Some nets carry names that must match, such as the supplies and the ports. Two netlists are *isomorphic* when there are bijections $\pi$ on the devices and $\varphi$ on the nets that keep the types, keep the names, and map the multiset of nets on the pins of class $c$ of each device $u$ to the multiset on the pins of class $c$ of $\pi(u)$.

This is [graph isomorphism](/graph-isomorphism-problem/) of two [bipartite graphs](/bipartite-graph/), one vertex per device and per net and one edge per pin, with the pin class as the colour of the edge. The output is the pair $(\pi, \varphi)$, or a report of a difference. Costs are counted in the number of devices $n$, of nets $m$ and of pins $P$.

## The algorithm

```pseudo id=main
GEMINI(G, G′)
L1  give each device the label of its type, and each net the label (name or none, number of pins)
L2  return SEARCH(λ)

SEARCH(λ)                                   ▷ λ labels the vertices of G and G′ together
L3  repeat
L4      for each net v of G and G′: key(v) ← (λ(v), multiset of (pin class, λ(u)) over the pins on v)
L5      for each device u: key(u) ← (λ(u), multiset of (pin class, λ(v)) over the pins of u)   ▷ with the new net labels
L6          (after L4 and after L5) renumber the keys of both netlists with one table
L7      if some label has more vertices in G than in G′, or fewer, then return MISMATCH(that label)
L8  until the number of labels did not grow
L9  if every label has one vertex in G and one in G′ then return the map from G to G′ by equal labels
L10 choose a smallest label class K with two or more vertices on each side, and a vertex x of K in G
L11 for each vertex y of K in G′ do
L12     give x and y one new label;  r ← SEARCH(λ);  if r is a map then return r
L13 return the last MISMATCH
```

Line L1 uses only facts that every isomorphism keeps. Lines L4 to L6 are one round of colour refinement, done on the union of the two netlists, so that a label means the same thing on both sides. Line L7 compares the sizes of the classes, which is where a difference shows. Line L12 is the guess, which Ebeling and Zajicek describe as a heuristic step for the symmetric parts of a circuit. The version above tries the other candidates of line L11 when a guess leads to a mismatch, which makes it exact; with only the first candidate it is the plain guessing comparator.

## Example

The schematic is a CMOS NAND gate with inputs A and B and output Y. P1 is a p-transistor with gate A between Y and VDD, P2 a p-transistor with gate B between VDD and Y, N1 an n-transistor with gate A between Y and X, and N2 an n-transistor with gate B between X and GND. The extracted layout has the nets n1 to n6, with n4 named VDD and n6 named GND, and the devices in this order: 0 is an n-transistor with gate n2 between n6 and n5, 1 a p-transistor with gate n1 between n4 and n3, 2 an n-transistor with gate n1 between n3 and n5, and 3 a p-transistor with gate n2 between n3 and n4. Each transistor has the pin classes gate, and source or drain twice.

| step | classes of the schematic | classes of the layout |
| --- | --- | --- |
| L1, devices | {N1, N2}, {P1, P2} | {0, 2}, {1, 3} |
| L1, nets | {A, B, X} (2 pins), {Y} (3 pins), {GND}, {VDD} | {n1, n2, n5}, {n3}, {n6}, {n4} |
| round 1, nets | {A, B}, {X}, {Y}, {GND}, {VDD} | {n1, n2}, {n5}, {n3}, {n6}, {n4} |
| round 1, devices | {N1}, {N2}, {P1, P2} | {2}, {0}, {1, 3} |
| round 2, nets | {A}, {B}, {X}, {Y}, {GND}, {VDD} | {n1}, {n2}, {n5}, {n3}, {n6}, {n4} |
| round 2, devices | {N1}, {N2}, {P1}, {P2} | {2}, {0}, {1}, {3} |

In round 1 the nets A and B (one p gate and one n gate each) part from X (two n sources or drains), and the device N1 (on Y and X) parts from N2 (on X and GND). In round 2 the net A, the gate of N1, parts from B, the gate of N2, and then P1 parts from P2. Round 3 splits nothing. Every class has one member on each side, so line L9 returns A to n1, B to n2, X to n5, Y to n3, VDD to n4, GND to n6, and P1, P2, N1, N2 to devices 1, 3, 2, 0. No guess was needed.

If the layout had A at the bottom of the n stack and B at the top, the two netlists would still be isomorphic, with A and B exchanged: without names the comparator cannot tell which input drives the transistor at the bottom of the stack, although that changes the delay. Naming the ports A and B makes this a mismatch at round 1. A ring of six equal resistors against two rings of three is the opposite case: every net has two pins and every resistor two neighbours, the refinement never splits a class, and only a guess shows the difference.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The labels are *sound*: every isomorphism that agrees with the guesses made so far maps each vertex to a vertex with the same label. Line L1 is sound because types, names and pin counts are kept by an isomorphism, a round of lines L4 to L6 keeps soundness because the key of a vertex is built from its neighbours with their pin classes, and a guess keeps soundness for the isomorphisms that agree with it. So a class with different sizes on the two sides proves that no such isomorphism exists. When every class has one member on each side and the labels are stable, the map by equal labels is an isomorphism, because each device has the same multiset of (pin class, net label) as its image, and each net label names one net on each side. With backtracking, the candidate $y = f(x)$ of some isomorphism $f$ is always among those tried, so a match is found whenever one exists.

## Complexity

One round builds $n + m$ keys of total size $O(P)$ and sorts them, which costs $O(P \log P + (n + m) \log(n + m))$ time. The number of labels grows in every round but the last and cannot pass the number of vertices, so one refinement takes at most $2(n + m)$ rounds. A guess makes a new class, so a run without backtracking makes at most $n + m$ guesses and costs $O((n + m)^2 (P + n + m) \log(n + m))$ in the worst case. With backtracking the search tree has depth at most $n + m$ and at most $n + m$ branches at each node, so it has $2^{O((n + m) \log(n + m))}$ nodes, and Neuen and Schweitzer showed that every individualization and refinement search needs exponentially many nodes on some graphs. These are bounds on the worst case. On real layouts the refinement splits almost every class in a few rounds, because supply nets, ports and the mix of device types break the symmetry early. That is an observation from practice, not a theorem.

## Properties

- Every reported mismatch at the top level is real (Theorem 4 of the proof). A mismatch after a guess is real only when the guess cannot be wrong, for example when the tied vertices are copies of one cell.
- Every returned map is an isomorphism.
- The labels are exact signatures here. Gemini computes numeric labels from the neighbour labels, which can collide. A collision merges two classes that should differ, which can force an extra guess, but it cannot make a wrong map pass the final check.
- Unlike [Weisfeiler-Leman](/weisfeiler-leman/) as a test of non-isomorphism, Gemini runs the refinement on both netlists with one label table, uses the pin classes and the names, returns a matching, and points to the place of a difference.

## Variants and improvements

- **GeminiII.** Ebeling's second version uses the bipartite structure of the device and net graph, with nets and devices relabeled in turn, to make the relabeling faster.
- **SubGemini.** The labels of a small pattern circuit find all its copies in a large netlist, a [subgraph isomorphism](/subgraph-isomorphism/) problem: candidates in the large netlist are filtered by labels that only depend on a bounded neighbourhood.
- **Series and parallel reduction.** LVS tools often merge parallel transistors and series stacks before the comparison, and permute the inputs of a stack of equivalent transistors, so that netlists that differ only in these ways compare equal.
- **Canonical forms.** [Canonical labeling](/canonical-labeling/) tools such as [nauty](/nauty/) solve the same problem for general graphs with a full individualization and refinement search and automorphism pruning.

## When to use it

Use it to compare an extracted netlist with a schematic netlist at the transistor or the cell level, and to find a known circuit inside a larger one. For general graphs with large symmetric parts use nauty or a similar [individualization and refinement](/individualization-refinement/) tool, which prunes the search with automorphisms. For pattern search with a small pattern and a large target, [VF2](/vf2-algorithm/) and similar backtracking matchers are simpler.

## Pitfalls

- Pin classes matter. If the source and the drain are two different classes, a layout with them exchanged is reported as a mismatch.
- Unnamed supply nets make the problem much more symmetric. Give the supplies and the ports names before the comparison.
- A guess that leads to a mismatch is not a proof of a difference. Report it as a difference only if the tied vertices are known to be interchangeable, or else backtrack.
- A class that differs by one vertex says where a difference is, not what it is. A short or an open in the layout changes the labels of all vertices near it, so the first reported class is often a neighbour of the real error.
- The refinement compares structure only. Device sizes and parameter values need a separate check after the matching.

## Implementations

## History

Ebeling and Zajicek presented Gemini at ICCAD 1983 as a way to validate a VLSI layout by comparing wirelists with a graph isomorphism method. Ebeling's GeminiII at ICCAD 1988 used the bipartite structure of the device and net graph for a faster relabeling, and Ohlrich, Ebeling, Ginting and Sather used the same labels to find subcircuits in SubGemini at DAC 1993.

## References
