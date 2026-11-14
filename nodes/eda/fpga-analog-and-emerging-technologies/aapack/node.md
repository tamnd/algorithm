---
tag: 11GQMP
kind: algorithm
slug: aapack
name: AAPack
aliases:
- architecture-aware packing
area: eda/fpga-analog-and-emerging-technologies
level: advanced
summary: Luu, Anderson and Rose's packer for logic blocks with hierarchy, modes and complex local interconnect, which checks each candidate by placing it and routing inside the block.
solves: [fpga-packing]
model: word-ram
complexity:
  vars: {n: the number of BLEs, N: the number of slots of a block, K: the LUT size, I: the number of input pins, R: the time of one route inside a block}
  time: {packing: O(n^2 N R)}
  space: {total: O(n K + N K (I + N))}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2011
  people: [Jason Luu, Jason H. Anderson, Jonathan Rose]
  note: AAPack replaced the counting checks of T-VPack by a placement and a route inside the block, read from an architecture description with hierarchy and modes. In 2014 Luu, Rose and Anderson added speculative packing, which routes a block once when it is full and repacks it only if that route fails.
prereqs: [t-vpack, fpga-packing, routing-resource-graph]
see_also: [negotiated-congestion-routing, fpga-logic-cluster, maximum-matching, augmenting-path, berge-lemma, greedy-algorithm, island-style-fpga, generic-backtracking-algorithm]
sources:
  - paper: doi:10.1145/1950413.1950457
    title: Jason Luu, Jason H. Anderson and Jonathan Rose, Architecture description and packing for logic blocks with hierarchy, modes and complex interconnect, Proceedings of the ACM/SIGDA International Symposium on Field Programmable Gate Arrays (FPGA '11), 227 to 236, 2011
    locator: the architecture description language and the packing algorithm (seed choice, candidate choice by attraction, placement of a candidate in a primitive and the intra-block route with a PathFinder-based router)
  - paper: doi:10.1145/2554688.2554783
    title: Jason Luu, Jonathan Rose and Jason Anderson, Towards interconnect-adaptive packing for FPGAs, Proceedings of the ACM/SIGDA International Symposium on Field-Programmable Gate Arrays (FPGA '14), 2014
    locator: speculative packing, with a single route at the end of a block and a detailed repack on failure (general locator)
  - paper: doi:10.1145/2617593
    title: Jason Luu and others, VTR 7.0, next generation architecture and CAD system for FPGAs, ACM Transactions on Reconfigurable Technology and Systems 7(2), 2014
    locator: the packer of the VTR flow (general locator)
---

AAPack is a greedy algorithm for [FPGA packing](/fpga-packing/) into logic blocks whose local routing is not a full crossbar, whose parts have modes, or that hold memories and multipliers. Like [T-VPack](/t-vpack/), it fills one block at a time from a seed and adds the most attracted BLE that fits, but it decides that a BLE fits by placing it in a free slot of the block and routing all nets inside the block. The algorithm belongs to the FPGA CAD topic of this sub-area and is the packer of the VTR flow.

## In plain words

T-VPack decides that a group of logic pieces fits in a block by counting: enough seats, and few enough input wires. That is right only when every input wire of the block can reach every seat.

Real blocks are not built that way. Each seat can only be reached from some of the input wires, some seats have a flip-flop and some do not, and some parts of a block can be set up in more than one way. Counting is then too optimistic: a group can pass the count and still not be wired up.

AAPack therefore tries for real. To add a piece, it picks a free seat that suits the piece and then searches for a wiring of the whole block. If the wiring works, the piece stays; if not, it tries another seat or another piece.

## The problem

**Input.** A netlist of $n$ BLEs, each with at most $K$ input nets, one output net and a flag for its flip-flop. A logic block with $N$ slots, $I$ input pins, a flag per slot for a flip-flop, and a local routing $\mathrm{conn}(s, j)$: the set of sources (input pins and slot outputs) that can drive LUT input $j$ of slot $s$.

**Output.** A partition of the BLEs into blocks, and for each block a slot for each member, a pin for each external net and a LUT input for each input net of each member, such that every LUT input is driven by a source that carries its net. This is a legal configuration; the [proof page](proofs/correctness.md) states it in full.

**Goal.** Few blocks and, with a timing weight, few critical connections between blocks. AAPack minimizes neither exactly.

In the model of this page, each external net enters the block on one pin, and the LUT inputs of one LUT can be permuted, since a LUT can compute any function of its inputs in any order. The real tool reads a hierarchical description with modes, and its slots are the primitives of that description.

## The algorithm

The attraction of a BLE $b$ to the open block $C$ is the one of T-VPack: $\lambda \, \mathrm{Crit}(b, C) + (1 - \lambda) \, |\mathrm{Nets}(b) \cap \mathrm{Nets}(C)| / (K + 1)$. LEGAL checks the slot limit, the flip-flops and the count of external nets, and then, in detailed mode, routes the block. In speculative mode, LEGAL is the counting part only.

```pseudo id=main
AAPACK(B, block, λ, speculative)
L1  while some BLE is unclustered:
L2      seed ← the unclustered BLE of highest criticality (ties: more inputs, then lower index)
L3      place seed in the first slot s for which LEGAL({seed ↦ s}) holds
L4      while the block has a free slot:
L5          order the unclustered BLEs by attraction to the block, highest first
L6          for each BLE b in that order, and each free slot s:
L7              if LEGAL(block + {b ↦ s}) then place b at s and go back to line L4
L8          no BLE fits in any free slot: leave the loop
L9      route the block
L10     if the route fails (speculative mode only): redo lines L3 to L8 from the same seed in detailed mode
L11     output the block with its slots and its route
```

AAPack routes inside the block with a [negotiated congestion](/negotiated-congestion-routing/) router on a graph of the block's pins, multiplexers and LUT inputs, which is a [routing resource graph](/routing-resource-graph/) of the block. That router is a heuristic: it can fail on a block that could be routed. The implementation instead routes exactly, which suits the tiny blocks of the tests. It tries every injective map from the external nets to the pins by [backtracking](/generic-backtracking-algorithm/), and for each map it gives the input nets of each member distinct LUT inputs by a [bipartite matching](/bipartite-matching/), one per slot. The members of different slots never compete for a LUT input, so the matchings are independent.

## Example

The block has $N = 2$ slots, $K = 2$, $I = 3$ pins, and a flip-flop only in slot 0. Each LUT input has a multiplexer with two sources:

| LUT input | sources |
| --- | --- |
| slot 0, input 0 | pin 0, output of slot 1 |
| slot 0, input 1 | pin 1, output of slot 0 |
| slot 1, input 0 | pin 2, output of slot 0 |
| slot 1, input 1 | pin 1, output of slot 1 |

**Counting is not enough.** Two BLEs both read $x$ and $y$. Together they have 2 external nets, fewer than 3, and 2 BLEs, so the counting checks pass. But slot 0 can read external nets only from pins 0 and 1, and slot 1 only from pins 2 and 1. So $x$ and $y$ would have to be on pins 0 and 1 for slot 0 and on pins 2 and 1 for slot 1, which needs both nets on pin 1. No configuration exists. AAPack in detailed mode puts the two BLEs in two blocks. In speculative mode it first puts both in one block by counting, then line L9 fails, and line L10 repacks the block, again with one BLE.

**The slot choice matters.** BLE $a$ reads $x, y$; BLE $b$ reads $w, x$ and is registered. The seed is $a$, since both have two inputs and $a$ comes first, and line L3 puts it in slot 0, which routes. Then $b$ needs the flip-flop of slot 0, which is taken, so the block closes with $a$ alone and $b$ gets a second block. Yet one block suffices: $b$ in slot 0 and $a$ in slot 1, with $w$ on pin 0, $x$ on pin 1 and $y$ on pin 2. Slot 0 reads $w$ on input 0 and $x$ on input 1; slot 1 reads $y$ on input 0 and $x$ on input 1, both from pin 1. AAPack never moves a member that it has placed, so it does not find this.

## Correctness

The [full proof](proofs/correctness.md) shows the following, assuming that every BLE fits alone in some slot of an empty block.

- **The route is exact.** With the slots fixed, the route of the implementation finds a legal configuration if and only if one exists. The proof combines the search over all pin maps with Kuhn's algorithm, which finds a covering matching whenever one exists by [Berge's lemma](/berge-lemma/).
- **Legality.** Every block that AAPack outputs comes with a configuration, in both modes, and so has at most $N$ BLEs and at most $I$ external nets. In speculative mode this rests on the final route of line L9 and the repack of line L10.
- **Partition and termination.** Every BLE is in exactly one block, and the loops end.
- **Maximality for fixed slots.** In detailed mode, a closed block admits no remaining BLE in any free slot, as long as its members keep their slots.

With PathFinder in place of the exact route, a block that AAPack outputs is still legal, because PathFinder's success is a real routing; only its failures can be wrong, and they cost blocks, not legality. Nothing here bounds the number of blocks, and the second example shows a loss.

## Complexity

Let $R$ be the time of one route inside a block. Each addition at line L7 tries at most $n$ BLEs in at most $N$ slots, so it makes $O(n N)$ calls of LEGAL, and so does each closing at line L8. There are at most $n$ additions and $n$ blocks, so packing makes $O(n^2 N)$ calls and takes $O(n^2 N R)$ time. Speculative mode makes at most one route per block in the good case and repeats a block in detailed mode only when its final route fails.

The exact route of the implementation takes $O(I! / (I - e)! \cdot N K^3)$ time for $e$ external nets, which is exponential and fine only for the small blocks of the tests. A PathFinder route takes time polynomial in the size of the block's graph per iteration, with a cap on the iterations. The space holds the netlist and the local routing of one block.

## Properties

- **Legal by construction.** A block is accepted only with a route, so placement and routing never meet a block that cannot be wired inside.
- **Not optimal.** The second example uses 2 blocks where 1 suffices. On seeded random tests with blocks of at most 3 slots, AAPack used more blocks than the exhaustive optimum on some instances; these are toy instances, not benchmark results.
- **Members stay put.** A placed member is never moved to another slot, which keeps the method simple and greedy.
- **Architecture-independent.** The same code packs any block that the description language can express, since all of its structure is in the routing graph and the slot types.

## Variants and improvements

- **Speculative packing.** Luu, Rose and Anderson (2014) count pins while they add BLEs and route a block only once, when it is full; if that route fails, they repack the block with a route after each addition. When most blocks route at the first try, this saves most of the routes.
- **Interconnect-adaptive packing.** The same 2014 work aims to adapt the packer to how sparse the interconnect of the block is.
- **Timing.** With $\lambda > 0$ and criticalities from a [static timing analysis](/static-timing-analysis/), the packer keeps critical connections inside blocks, as in T-VPack.
- **Moving members.** A packer can try to move placed members when a candidate does not fit, at the cost of more routes. The second example shows what this can gain.

## When to use it

Use AAPack, or the VTR packer that grew from it, when the logic block has sparse local routing, modes, carry chains, memories or multipliers, so that counting cannot decide legality. For a homogeneous block with a full crossbar, the counting checks are already exact, and [T-VPack](/t-vpack/) gives the same blocks with no routes. When packing time matters, turn on speculative mode.

## Pitfalls

- **Trusting the count.** Passing $|C| \le N$ and $|\mathrm{ext}(C)| \le I$ does not mean a block can be routed when the crossbar is sparse; the first example fails with two nets on three pins.
- **Forgetting slot types.** A registered BLE needs a slot with a flip-flop. A packer that places unregistered BLEs into those slots first can run out of them, as in the second example.
- **A heuristic failure is not a proof.** When PathFinder fails inside a block, the block may still be routable. Treat the failure as a cost, not as a fact about the block.
- **Routing one net at a time.** Nets inside a block compete for pins and multiplexer inputs, so they must be routed together, as a matching or with negotiation, not one by one.

## Implementations

## History

Luu, Anderson and Rose (2011) introduced AAPack with an architecture description language for logic blocks with hierarchy, modes and complex interconnect. They kept the greedy growth of T-VPack and checked each candidate by placing it in a primitive of the block and routing the block with a PathFinder-based router, which made the packer work for any block that the language describes. Luu, Rose and Anderson (2014) added speculative packing, which routes a block once instead of after every addition. The packer is part of VPR in the VTR flow.

## References
