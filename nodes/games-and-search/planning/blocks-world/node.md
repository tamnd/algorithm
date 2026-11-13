---
tag: KD4S9R
kind: problem
slug: blocks-world
name: Blocks world
aliases:
- blocks problem
- blocksworld
area: games-and-search/planning
level: intro
summary: Rearrange stacks of labelled blocks on a table into a goal arrangement, moving one clear block at a time; optimal plans are NP-hard to find.
prereqs: [strips]
see_also: [sussman-anomaly, classical-planning, pddl, state-space-planning, np-complete, international-planning-competition, sas-plus, tower-of-hanoi]
sources:
  - paper: doi:10.1016/0004-3702(92)90028-V
    title: "Naresh Gupta and Dana S. Nau, On the complexity of blocks-world planning, Artificial Intelligence 56(2-3) (1992)"
    locator: Section 3.2 and Appendix B (NP-completeness of optimal blocks world planning by reduction from feedback arc set; deadlocks)
  - paper: doi:10.1016/S0004-3702(00)00079-5
    title: "John Slaney and Sylvie Thiébaux, Blocks World revisited, Artificial Intelligence 125(1-2) (2001)"
    locator: pp. 119 to 153 (near-optimal algorithms, random instances, and the blocks world as a benchmark)
  - paper: doi:10.1016/0010-0285(72)90002-3
    title: "Terry Winograd, Understanding natural language, Cognitive Psychology 3(1) (1972)"
    locator: pp. 1 to 191 (SHRDLU, a dialogue system for a simulated world of blocks)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 4, Section 4.5 (the container stacking domain and its near-optimal algorithm)
  - paper: "N. J. A. Sloane (editor), The On-Line Encyclopedia of Integer Sequences, sequence A000262"
    title: OEIS A000262
    locator: "sequence A000262 (number of sets of lists: 1, 1, 3, 13, 73, 501, 4051, ...)"
---

The blocks world is a planning domain of labelled blocks on a table: a block can sit on the table or on one other block, a clear block can be moved onto the table or onto another clear block, and the task is to reach a goal arrangement. It is the oldest benchmark of [classical planning](/classical-planning/), from Winograd's SHRDLU (1972) and the [Sussman anomaly](/sussman-anomaly/) to the planning competitions. Some plan is always easy to find, but a shortest plan is NP-hard to find (Gupta and Nau 1992), and a simple algorithm is within a factor 2 of optimal.

## In plain words

Some toy blocks, each with a letter, stand in towers on a big table. You may lift only a block with nothing on top of it, and put it on the table or on top of another tower. You are told how the towers should look at the end, and you want to get there with as few moves as possible. Getting there at all is easy: put every block on the table, then build the towers. Getting there in the fewest moves is hard, because some blocks are in each other's way and you must choose which ones to put down on the table first.

## Definition

### States and moves

Fix a set $B$ of $n$ blocks. A state is an arrangement of $B$ into towers: each block is on the table or on exactly one other block, at most one block is on each block, and there are no cycles. A block is clear when no block is on it. As a [STRIPS](/strips/) task in the move encoding, the facts are $\mathit{on}(x, y)$ for $x \ne y$, $\mathit{ontable}(x)$ and $\mathit{clear}(x)$, and there are three move schemas:

- $\mathit{move}(b, x, y)$: from block $x$ to block $y$, with precondition $\mathit{on}(b, x)$, $\mathit{clear}(b)$, $\mathit{clear}(y)$;
- $\mathit{move}(b, x, \mathit{table})$: precondition $\mathit{on}(b, x)$, $\mathit{clear}(b)$;
- $\mathit{move}(b, \mathit{table}, y)$: precondition $\mathit{ontable}(b)$, $\mathit{clear}(b)$, $\mathit{clear}(y)$;

each with the obvious add and delete lists, and all parameters distinct. That gives $n(n-1)(n-2) + 2n(n-1) = n^2(n-1)$ ground actions. The four-operator encoding of the competitions has a robot hand, the facts $\mathit{holding}(x)$ and $\mathit{handempty}$, and the actions $\mathit{pickup}$, $\mathit{putdown}$, $\mathit{stack}$ and $\mathit{unstack}$: $2n^2$ ground actions, and each move becomes two actions.

### The problems

The input is an initial arrangement and a goal, a set of $\mathit{on}$ and $\mathit{ontable}$ facts. A full goal fixes the support of every block; a partial goal fixes only some.

- BW-PLAN: find a plan. A plan always exists for a goal that some arrangement satisfies.
- BW-OPT: find a shortest plan (unit costs; moves are sequential).
- The decision version: given $k$, is there a plan with at most $k$ moves?

### State counts

The states of the move encoding are the ways to split $n$ labelled blocks into a set of ordered towers, that is, sets of lists. Their number $a(n)$ is OEIS A000262:

$$a(n) = \sum_{k=1}^{n} \binom{n-1}{k-1} \frac{n!}{k!}, \qquad a(n) = (2n - 1)\, a(n-1) - (n-1)(n-2)\, a(n-2),$$

where the term for $k$ counts the arrangements with exactly $k$ towers (the Lah numbers). For $n = 0, 1, \ldots, 8$: 1, 1, 3, 13, 73, 501, 4051, 37633, 394353. All of them are reachable from any one of them. With a hand, a state is an arrangement or a held block plus an arrangement of the rest, so there are $a(n) + n\, a(n-1)$ states: 2, 5, 22, 125 and 866 for $n = 1$ to 5. The number of STRIPS fact sets is much larger: $2^{16} = 65536$ for 3 blocks with a hand.

## Variants

- Move encoding against hand encoding. On full goals the shortest plan in the hand encoding is exactly twice the shortest move plan, since each move is one $\mathit{pickup}$ or $\mathit{unstack}$ followed by one $\mathit{putdown}$ or $\mathit{stack}$.
- Partial goals: a goal that leaves some blocks free. Choosing where the free blocks go adds to the difficulty.
- Container stacking (Ghallab, Nau and Traverso): containers in piles moved by cranes, a blocks world with locations.
- Generalized planning: find one program that solves every blocks world instance, for any $n$.

## Examples

### The Sussman anomaly

Initial: $C$ on $A$, and $A$, $B$ on the table. Goal: $\mathit{on}(A, B)$ and $\mathit{on}(B, C)$. The shortest plan has 3 moves: $C$ to the table, $B$ onto $C$, $A$ onto $B$; with a hand it has 6 actions. A planner that achieves one goal and then the other needs 5 moves; see [Sussman anomaly](/sussman-anomaly/).

### A deadlock

Initial: $A$ on $B$ and $C$ on $D$, as two towers. Goal: $A$ on $D$ and $C$ on $B$. Each top block wants to go onto the other tower, but each target is covered by the other top block. Neither can go directly, so one of them must stop on the table first: move $A$ to the table, $C$ onto $B$, $A$ onto $D$, 3 moves for 2 misplaced blocks. Gupta and Nau call such a cycle of blocks waiting on each other a deadlock; in a large instance the deadlocks overlap, and choosing a smallest set of blocks that break all of them is the source of NP-hardness.

### Counting the work

In the 4-operator encoding with 3 blocks, the 18 ground actions and 22 reachable states make a breadth-first search trivial. With 10 blocks the move encoding has $a(10) = 58941091$ states, and with 20 blocks $a(20) \approx 3.3 \cdot 10^{20}$, so optimal search needs the domain-specific results below.

## Known algorithms

- Search: [breadth-first search](/breadth-first-search/) or [A*](/a-star-search/) over the state space is optimal, and is practical only for small $n$. Domain-independent planners treat the blocks world as a standard benchmark.
- Table then build: move every block that is not in position to the table, top block first, then build the goal towers from the bottom up. A block is in position when it is on its goal support and every block below it is in position; blocks in position never move. Each other block moves at most twice, so the plan has at most $2m$ moves, where $m$ is the number of blocks not in position. Every block not in position must move at least once in every plan, so $m \le \mathrm{OPT}$, and the plan is at most twice optimal. It runs in linear time after the in-position test.
- Better approximations: Gupta and Nau, and Slaney and Thiébaux, move a block directly to its final place whenever that place is ready, and send a block to the table only when no such move exists. This keeps the ratio 2 in the worst case and does better on typical instances.
- The deadlock view: every plan moves each block not in position at least once, and plans differ in which blocks move more than once. Deadlocks force such extra moves, and the choice of the blocks that make them is the hard part of optimal planning.

## Bounds

- Lower bound: every block not in position moves at least once, so $\mathrm{OPT} \ge m$.
- Upper bound: $\mathrm{OPT} \le 2m \le 2n$, from table then build.
- Complexity: BW-PLAN is in linear time; the decision version of BW-OPT is NP-complete (Gupta and Nau 1992, by reduction from feedback arc set), so BW-OPT is NP-hard, while a 2-approximation takes linear time.

## Reductions

- From feedback arc set: Gupta and Nau encode a directed graph as a blocks world instance whose deadlocks correspond to the cycles of the graph, so that a short plan exists if and only if a small set of arcs meets every cycle. This shows NP-hardness of optimal planning.
- To STRIPS and PDDL: the domain is a set of [action schemas](/action-schema/); grounding gives $n^2(n-1)$ moves or $2n^2$ hand actions.
- To SAS+: the position of each block is a variable with $n + 1$ values, which gives $(n+1)^n 2^{n+1}$ assignments for the hand encoding; see [SAS+](/sas-plus/).

## Applications

- Language and vision: SHRDLU (Winograd 1972) held dialogues about a simulated world of blocks, and blocks worlds remain a test bed for grounded language understanding.
- Planning research: the domain shows goal interaction (the Sussman anomaly), the gap between satisficing and optimal planning, and the effect of the encoding, and it was a domain of the early planning competitions.
- Robotics and logistics: stacking containers in a yard or crates in a warehouse is a blocks world with locations and cranes.

## References
