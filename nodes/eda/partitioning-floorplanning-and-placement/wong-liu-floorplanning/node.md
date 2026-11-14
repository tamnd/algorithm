---
tag: 0Y56MN
kind: algorithm
slug: wong-liu-floorplanning
name: Wong-Liu floorplanning
aliases:
- simulated annealing floorplanning
area: eda/partitioning-floorplanning-and-placement
level: core
summary: Simulated annealing over normalized Polish expressions with three moves, swap operands, complement a chain and swap an operand with an operator.
solves: [floorplanning]
model: word-ram
complexity:
  vars: {n: the number of blocks, d: the depth of the slicing tree, k: the moves per block at one temperature, s: the number of temperatures}
  time: {worst: O(s k n^2 d), average: O(s k n^2 d), best: O(s k n^2)}
  space: {extra: O(n d)}
properties: {deterministic: false, exact: false, recursive: false}
history:
  year: 1986
  people: [D. F. Wong, C. L. Liu]
  note: Wong and Liu presented the method at the 23rd Design Automation Conference in 1986, and the journal version with L-shaped blocks in Algorithmica in 1989.
prereqs: [normalized-polish-expression, simulated-annealing, stockmeyer-floorplan-sizing, floorplanning]
see_also: [slicing-floorplan, shape-function, cooling-schedule, metropolis-criterion, neighborhood-structure, sequence-pair, b-star-tree-floorplan, simulated-annealing-placement]
sources:
  - paper: "D. F. Wong and C. L. Liu, A new algorithm for floorplan design, Proceedings of the 23rd ACM/IEEE Design Automation Conference, 101 to 107, 1986"
    locator: the moves M1, M2 and M3, the proof that they connect all normalized Polish expressions, the cost of area plus weighted wire length, and the cooling schedule
  - paper: doi:10.1007/BF01553890
    title: D. F. Wong and C. L. Liu, Floorplan design of VLSI circuits, Algorithmica 4, 263 to 291, 1989
    locator: the journal version, with L-shaped blocks
  - paper: doi:10.1126/science.220.4598.671
    title: S. Kirkpatrick, C. D. Gelatt Jr. and M. P. Vecchi, Optimization by simulated annealing, Science 220(4598), 671 to 680, 1983
    locator: simulated annealing with the Metropolis rule and a geometric schedule
  - paper: doi:10.1016/S0019-9958(83)80038-2
    title: Larry Stockmeyer, Optimal orientations of cells in slicing floorplan designs, Information and Control 57(2-3), 91 to 101, 1983
    locator: the shape list merge that gives the cost of a slicing tree
  - paper: "Bruce Hajek, Cooling schedules for optimal annealing, Mathematics of Operations Research 13(2), 311 to 329, 1988"
    locator: the logarithmic schedule under which annealing converges to an optimum
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 3, Chip Planning (floorplanning by simulated annealing over Polish expressions; general locator)
---

Wong-Liu floorplanning searches for a good [slicing floorplan](/slicing-floorplan/) with [simulated annealing](/simulated-annealing/). A state is a [normalized Polish expression](/normalized-polish-expression/), so every state is one slicing floorplan and no floorplan has two states. Three small moves change the word: swap two neighbouring blocks, change the direction of a run of cuts, and swap a block with a cut next to it. The cost of a word is the least area over the shapes of the blocks, found by [Stockmeyer's floorplan sizing](/stockmeyer-floorplan-sizing/), plus a weight times the wire length. Wong and Liu published it in 1986, and it became the model for many later annealing floorplanners. It is a heuristic: what is proved is that every state is a valid floorplan and that the moves reach every slicing floorplan, not how close the result is to the optimum.

## In plain words

You arrange furniture in a room by trying small changes. Swap two pieces next to each other. Turn a row of pieces into a column. Move a piece across a wall. After each change you measure the room you need. If the change helps, you keep it. If it makes things worse, you sometimes still keep it, more often at the start and less often later. This lets you leave a bad arrangement that no single small change can improve.

The arrangement is written as a word of blocks and cuts. The rules of the word make sure that every word is a real arrangement and that no arrangement has two words, so no time is lost on copies.

## The problem

The input is a set of $n$ blocks, each with a list of allowed shapes $(w, h)$ (for example a rectangle and its rotation, or a staircase approximation of a soft block), a list of nets on the blocks, and a weight $\lambda \ge 0$. The output is a slicing floorplan with a shape for each block. The goal is a small cost $A + \lambda L$, where $A$ is the area of the floorplan and $L$ is the [half-perimeter wire length](/half-perimeter-wirelength/) of the nets over the centres of the blocks. This is the slicing case of [floorplanning](/floorplanning/). The method looks for a good floorplan, and it does not prove that the one it finds is optimal.

## The algorithm

The tokens are blocks and the operators $V$ ($E_1 E_2 V$ puts $E_1$ to the left of $E_2$) and $H$ ($E_1$ below $E_2$). A *chain* is a maximal run of operators in the word. The three moves are:

- **M1.** Swap two operands that are next to each other in the order of the operands. Operators between them stay in place.
- **M2.** Complement a chain: each $H$ in it becomes $V$, and each $V$ becomes $H$.
- **M3.** Swap an operand and an operator that are next to each other, only if the result is still normalized.

```pseudo id=main
WONG-LIU(blocks, S, nets, λ, r, k, ε)       ▷ cost(E) = least area of E over S, plus λ · HPWL
L1  E ← 1 2 V 3 V ... n V; best ← E
L2  T ← T_0, so that an average uphill move is accepted with probability P_0
L3  repeat
L4      tries ← 0; uphill ← 0; rejects ← 0
L5      repeat
L6          E' ← M1, M2 or M3, chosen at random, applied to E
L7          tries ← tries + 1; Δ ← cost(E') − cost(E)
L8          if Δ ≤ 0 or random() < e^(−Δ / T) then
L9              if Δ > 0 then uphill ← uphill + 1
L10             E ← E'; if cost(E) < cost(best) then best ← E
L11         else rejects ← rejects + 1
L12     until uphill > N or tries > 2N              ▷ N = k · n
L13     T ← r · T
L14 until rejects / tries > 0.95 or T < ε
L15 return best
```

Line L8 is the [Metropolis rule](/metropolis-criterion/), and lines L13 and L14 are a geometric [cooling schedule](/cooling-schedule/). One temperature ends when the search has made $N$ uphill moves or tried $2N$ moves. The search stops when almost every move is rejected or the temperature is very low. The code uses $r = 0.85$ by default, and it also has a limit on the number of temperatures.

M3 is the only move that can break the normal form. If the operand $e_i$ moves right past the operator $e_{i+1}$, the prefix of length $i$ gets one more operator, and the balloting property needs $2 (N_{i-1} + 1) < i$, where $N_k$ is the number of operators in $e_1 \cdots e_k$. The operator also gets a new left neighbour $e_{i-1}$, which must not be the same operator. If the operator moves right past an operand, only its new right neighbour must differ from it. With the prefix counts both tests take $O(1)$ time.

## Example

Take five blocks, each of which may turn: $1: 2 \times 3$, $2: 3 \times 2$, $3: 4 \times 1$, $4: 2 \times 2$ and $5: 1 \times 3$ (width by height). The block area is $6 + 6 + 4 + 4 + 3 = 23$. Some moves from the start word, each with the least area of the new word:

| step | word | move | least area |
|---|---|---|---|
| 0 | $1\,2\,V\,3\,V\,4\,V\,5\,V$ | the start: a row | 30, a $15 \times 2$ row |
| 1 | $1\,3\,V\,2\,V\,4\,V\,5\,V$ | M1 on blocks 2 and 3 | 30 |
| 2 | $1\,2\,V\,3\,V\,4\,H\,5\,V$ | M2 on the chain after block 4 | 36 |
| 3 | $1\,2\,V\,3\,4\,V\,H\,5\,V$ | M3 on the operator before block 4 | 28 |
| 4 | $1\,2\,V\,3\,4\,H\,V\,5\,V$ | M2 on the chain $V\,H$ | 27 |

Step 2 to step 3 swaps the operator $V$ at position 5 with the operand 4 after it. Its new right neighbour is $H$, so the word stays normalized. The same swap on the start word would give $1\,2\,V\,3\,4\,V\,V\,5\,V$ with two $V$ in a row, so M3 refuses it there. Step 1 to step 2 is an uphill move by 6, which the search accepts with probability $e^{-6/T}$.

Five runs of the annealing with $k = 10$ and the seeds 0 to 4 all end at area 24. One of the results is $5\,3\,H\,1\,V\,4\,V\,2\,V$: block 5 as $3 \times 1$ under block 3 as $4 \times 1$, and then blocks 1, 4 and 2 in a row, in a $12 \times 2$ rectangle with one empty unit. A full search over all $5! \cdot 90 = 10800$ normalized words with Stockmeyer's sizing confirms that 24 is the least area of a slicing floorplan of these blocks.

## Correctness

Each move keeps the word normalized. M1 does not change the positions and the values of the operators. M2 changes a run of operators that alternate into a run that still alternates, with operands on both sides. M3 is applied only after the balloting test and the neighbour test above. So every state is a normalized Polish expression, which is one slicing floorplan, and its cost is computed exactly by Stockmeyer's sizing. The returned word is the best state visited. So its area is at least the least area of a slicing floorplan, which is at least the total block area. The inner loop stops after at most $2N + 1$ tries, and the temperature falls by the factor $r$, so the search stops. Wong and Liu also prove that the three moves connect all normalized words, so every slicing floorplan can be reached. The full proof is in [the correctness proof](proofs/correctness.md).

What is not proved is the quality of the result. The geometric schedule gives no bound on the gap to the optimum. In the measurement above, on 20 random instances of 5 blocks with rotation, 19 runs with $k = 10$ reached the least area of an exhaustive search. That is a measurement on toy instances, not a guarantee.

## Complexity

A move copies the word in $O(n)$ time. The cost of the new word takes $O(n d)$ time for blocks with two shapes, where $d$ is the depth of its slicing tree, because Stockmeyer's merge is linear in the lengths of the fronts. The wire length takes $O(P)$ time for $P$ pins. One temperature makes at most $2N + 1 = O(k n)$ moves. So the time is $O(s \cdot k n \cdot (n d + P))$ for $s$ temperatures. With $T_0$, $r$ and $\varepsilon$ fixed, $s = O(\log(T_0 / \varepsilon))$. The space is $O(n d)$ for the fronts of one evaluation.

The evaluation can be incremental: a move changes a few nodes of the tree, and only their fronts and the fronts of their ancestors need new merges. The implementation evaluates each word from scratch.

## Properties

- **No duplicate states.** Each slicing floorplan has exactly one normalized word, so the search does not count a floorplan twice. This is the main reason for the normal form.
- **Every state is legal.** There is no penalty for overlap, because no state has overlap.
- **Randomized.** The result depends on the seed. With a fixed seed it is the same each run.
- **Slicing only.** The search cannot reach a non-slicing floorplan such as a pinwheel of five blocks.

## Variants and improvements

- **L-shaped blocks.** The journal version adds operators for L-shaped blocks and a modified sizing.
- **Fixed outline.** For a fixed chip outline, the cost adds a penalty for the part of the floorplan outside the outline, as in the work of Adya and Markov on [sequence pairs](/sequence-pair/).
- **Other representations.** The same annealing runs over [sequence pairs](/sequence-pair/), [B*-trees](/b-star-tree-floorplan/) and [O-trees](/o-tree-floorplan/), which also reach non-slicing packings.
- **Other moves.** Later floorplanners rotate single blocks as a move, or change the aspect ratio of a soft block, instead of a full sizing for each word.
- **Placement.** The same annealing scheme for cells is [simulated annealing placement](/simulated-annealing-placement/).

## When to use it

Use the method for a slicing floorplan of tens to a few hundred blocks, when the design flow prefers slicing structures (for example for routing channels or for hierarchical design), and when blocks have rotations or soft shapes, because the sizing then finds the best shapes for each tree. For packings that need not be slicing, an annealing over a [B*-tree](/b-star-tree-floorplan/) or a [sequence pair](/sequence-pair/) can reach smaller areas.

## Pitfalls

- **M3 without the balloting test.** Swapping an operand to the right of an operator can leave a prefix with as many operators as operands. The word is then not a Polish expression, and the stack evaluation fails.
- **M3 without the neighbour test.** The swap can put two equal operators side by side. The word is then a valid Polish expression, but not a normalized one, and the search has two words for one floorplan.
- **A wrong start temperature.** With $T_0$ too low the search is only a [local search](/local-search/). With $T_0$ too high it wastes time. Estimate it from a short random walk, as in line L2.
- **The cost of one part only.** Choosing the best shape of each subtree for its own area is wrong; use the whole front at each node, as Stockmeyer's sizing does.
- **Comparing floats for equality.** The code keeps areas and wire lengths as exact fractions, and uses floats only for the acceptance probability.

## Implementations

The Python module implements the three moves with the $O(1)$ test for M3, the cost with Stockmeyer's merge and an exact wire length, and the annealing loop of the pseudocode. A random generator with a fixed seed is passed in. The tests check that the M3 test agrees with a full check of the normal form at every position, that the moves reach all normalized words for $n \le 5$ by breadth-first search, that 600 random walks of moves keep the normal form, that the realized blocks never overlap, and that the annealing returns a normalized word whose area is at least the exhaustive optimum and at least the block area, the same for the same seed.

## History

Kirkpatrick, Gelatt and Vecchi proposed simulated annealing for placement and other problems in 1983. Otten had described slicing structures in 1982, and Stockmeyer had given the exact sizing of a slicing tree in 1983. Wong and Liu combined these in 1986: annealing over normalized Polish expressions, three moves, and a cost of area plus wire length. The journal version of 1989 added L-shaped blocks. Later floorplanners replaced the word by representations of non-slicing packings, the [sequence pair](/sequence-pair/) in 1995 and the [B*-tree](/b-star-tree-floorplan/) in 2000, but kept the annealing scheme.

## References
