---
tag: XS6G6S
kind: algorithm
slug: sdf-static-scheduling
name: Static scheduling of synchronous dataflow
aliases:
- periodic admissible sequential schedule
- PASS construction
- SDF balance equations
area: eda/high-level-synthesis-and-scheduling
level: core
summary: Solves the balance equations of an SDF graph for the repetition vector and simulates one period to build a periodic admissible schedule or prove deadlock.
solves: [high-level-synthesis]
model: word-ram
complexity:
  vars: {n: the number of actors, E: the number of edges, Q: the number of firings in one period (the sum of the repetition vector), D: the largest number of edges at one actor}
  time: {worst: O(n + E + (n + Q D) D)}
  space: {extra: O(n + E)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1987
  people: [Edward A. Lee, David G. Messerschmitt]
  note: Lee and Messerschmitt gave the balance equations, the rank test and the class-S algorithm that builds a periodic admissible sequential schedule, in IEEE Transactions on Computers in 1987.
prereqs: [synchronous-dataflow, queue]
see_also: [kahn-process-network, iteration-bound, nullspace-computation, gaussian-elimination, lcm-of-integers, topological-sort, dsp-unfolding, deadlock]
sources:
  - paper: doi:10.1109/TC.1987.5009446
    title: Edward A. Lee and David G. Messerschmitt, Static scheduling of synchronous data flow programs for digital signal processing, IEEE Transactions on Computers C-36(1), 24 to 35, 1987
    locator: the rank test, the class-S algorithm for a periodic admissible sequential schedule and its proof, and the expansion for parallel schedules
  - paper: doi:10.1109/PROC.1987.13876
    title: Edward A. Lee and David G. Messerschmitt, Synchronous data flow, Proceedings of the IEEE 75(9), 1235 to 1245, 1987
    locator: the SDF model and an overview of its static scheduling
  - book: isbn:0792397223
    title: Shuvra S. Bhattacharyya, Praveen K. Murthy and Edward A. Lee, Software Synthesis from Dataflow Graphs, Kluwer, 1996
    locator: the chapters on consistency, looped schedules, single appearance schedules and buffer memory
---

Static scheduling of synchronous dataflow turns an SDF graph into a fixed firing order that a compiler can emit as straight-line code or as nested loops. It has two steps. The first solves the balance equations $\Gamma q = 0$ of the [synchronous dataflow](/synchronous-dataflow/) graph for the repetition vector $q$, the number of times each actor fires in one period; if they have no positive solution, the graph cannot run forever in bounded memory. The second simulates one period: it fires any actor that has enough tokens on its inputs and has not yet reached its count, until every actor has fired $q_a$ times or no actor can fire. Lee and Messerschmitt (1987) proved that this greedy simulation never fails when some schedule exists, so it decides deadlock exactly. The schedule that it finds is valid, but its buffer memory can be larger than needed.

## In plain words

A factory line has machines that take parts from bins and put parts into other bins, always in the same numbers: this machine takes 3 bolts and makes 2 brackets. Before the line runs, a planner can work out how many times each machine must run so that every bin ends a shift with as many parts as it started with; that is a small system of equations. Then the planner walks through the shift on paper, running any machine that has its parts. If that walk gets stuck, no other plan works either, because running a machine early never takes parts away from another machine. If it gets through, the walk itself is the plan, repeated shift after shift.

## The problem

The input is a connected SDF graph, as on the [synchronous dataflow](/synchronous-dataflow/) page: actors $1, \ldots, n$, and edges $e = (a, b)$ with a production rate $p_e \ge 1$, a consumption rate $c_e \ge 1$ and $d_e \ge 0$ initial tokens. The topology matrix $\Gamma$ has one row per edge, with $p_e$ in column $a$ and $-c_e$ in column $b$. The output is either a periodic admissible sequential schedule (PASS), a firing sequence in which every actor is enabled when it fires, every actor fires at least once, and the token counts end where they started; or a proof that no PASS exists, because the graph is inconsistent or because it deadlocks.

## The algorithm

```pseudo id=main
SDF-SCHEDULE(n, E)
L1  q_1 ← 1; walk a spanning tree of the undirected graph and set q_b ← q_a · p_e / c_e along each tree edge e = (a, b), or q_a ← q_b · c_e / p_e when the walk enters a from b
L2  if p_e · q_a ≠ c_e · q_b for some edge e = (a, b) then return "inconsistent"
L3  scale q by the least common multiple of its denominators, then divide by the gcd of its entries
L4  tokens ← d; count ← 0; seq ← empty; W ← a FIFO queue holding every actor
L5  while W is not empty do
L6      a ← pop W
L7      if count_a < q_a and tokens_e ≥ c_e for every input edge e of a then
L8          take c_e tokens from each input edge e of a, add p_e tokens to each output edge e of a
L9          count_a ← count_a + 1; append a to seq
L10         push a and every actor that reads an output edge of a onto W, unless already there
L11 if count = q then return (q, seq) else return (q, "deadlock")
```

Lines L1 to L3 compute the repetition vector by the spanning tree walk of Theorem 1 on the [synchronous dataflow](/synchronous-dataflow/) page, with exact rational arithmetic; [Gaussian elimination](/gaussian-elimination/) of $\Gamma$ gives the same vector more slowly. A self loop has the row $p_e - c_e$, so line L2 rejects it unless $p_e = c_e$. Lines L4 to L10 are the simulation. The queue $W$ only saves work: an actor needs another look only after it fires, or after a firing adds tokens to one of its inputs, so line L10 pushes exactly those actors.

## Example

Take the ring of the [synchronous dataflow](/synchronous-dataflow/) page: $A \to B$ with rates $(2, 3)$, $B \to C$ with rates $(1, 2)$, and $C \to A$ with rates $(3, 1)$ and $d$ initial tokens. Line L1 sets $q_A = 1$, $q_B = 2/3$ and $q_C = 1/3$, line L2 checks the edge $C \to A$, $3 \cdot 1/3 = 1 \cdot 1$, and line L3 scales to $q = (3, 2, 1)$.

With $d = 3$, the queue starts as $A, B, C$.

| step | pop | fires? | tokens on $A{\to}B$, $B{\to}C$, $C{\to}A$ | counts $A, B, C$ | queue after |
| --- | --- | --- | --- | --- | --- |
| start | | | 0, 0, 3 | 0, 0, 0 | $A, B, C$ |
| 1 | $A$ | yes | 2, 0, 2 | 1, 0, 0 | $B, C, A$ |
| 2 | $B$ | no, needs 3 | 2, 0, 2 | 1, 0, 0 | $C, A$ |
| 3 | $C$ | no, needs 2 | 2, 0, 2 | 1, 0, 0 | $A$ |
| 4 | $A$ | yes | 4, 0, 1 | 2, 0, 0 | $A, B$ |
| 5 | $A$ | yes | 6, 0, 0 | 3, 0, 0 | $B, A$ |
| 6 | $B$ | yes | 3, 1, 0 | 3, 1, 0 | $A, B, C$ |
| 7 | $A$ | no, count reached | 3, 1, 0 | 3, 1, 0 | $B, C$ |
| 8 | $B$ | yes | 0, 2, 0 | 3, 2, 0 | $C, B$ |
| 9 | $C$ | yes | 0, 0, 3 | 3, 2, 1 | $B, C, A$ |

The last three pops find every actor at its count, so the queue empties and the algorithm returns $q = (3, 2, 1)$ and the sequence $AAABBC$, with the tokens back at $(0, 0, 3)$. The order $AABABC$ is also a PASS. Its largest token counts are $(4, 2, 3)$, while those of $AAABBC$ are $(6, 2, 3)$, so the order changes the buffer memory.

With $d = 2$, $A$ fires twice and $B$ once, which leaves 1 token on $A \to B$, 1 token on $B \to C$ and none on $C \to A$. No actor is enabled, the counts are $(2, 1, 0) \ne q$, and the algorithm reports a deadlock. By the theorem below, no other order does better.

## Correctness

The [full proof](proofs/correctness.md) shows:

- **The repetition vector.** If line L2 passes, $q$ is the least positive integer solution of $\Gamma q = 0$; if it fails, $\operatorname{rank} \Gamma = n$ and no PASS exists. This is Theorem 1 of the [synchronous dataflow](/synchronous-dataflow/) page applied to the walk.
- **Valid output.** Every firing in seq is enabled when it happens, every actor fires $q_a \ge 1$ times, and the final token counts are $d + \Gamma q = d$, so seq is a PASS.
- **Deadlock is real.** If the simulation stops with $\mathrm{count} \ne q$, then no PASS exists. The proof first cuts any PASS down to an admissible sequence with counts exactly $q$, and then shows that the first firing of that sequence that the simulation did not make would have been enabled at the end of the simulation.

So the algorithm is exact for the question "does a PASS exist", in the order of firings that it chooses. It is not exact for any measure of the schedule: the proof says nothing about buffer memory or code size, and the example shows a schedule whose buffer on $A \to B$ is 6 where 4 is enough.

## Complexity

Lines L1 to L3 make $O(n + E)$ rational operations. The numbers can be long: a chain of $n$ actors in which each produces 2 tokens and the next consumes 1 has $q = (1, 2, 4, \ldots, 2^{n-1})$, so $Q$ can be exponential in $n$, and the simulation is linear in $Q$, not in the size of the graph. Each firing costs $O(D)$ on line L8 and pushes at most $D + 1$ actors on line L10, and each pop costs $O(D)$ on line L7. There are at most $n + Q(D + 1)$ pops, so the simulation takes $O((n + Q D) D)$ time. The extra space is $O(n + E)$ for the counts, the tokens and the queue, plus the output of length $Q$.

## Properties

- **Exact for deadlock.** It finds a PASS whenever one exists.
- **Any order works.** The proof holds for any rule that picks an enabled actor below its count, so the queue on line L6 can be replaced by any rule that suits the code generator.
- **Deterministic.** With the FIFO queue the output is fixed.
- **Sequential.** It gives one firing order for one processor. Parallel schedules need the precedence expansion described on the [synchronous dataflow](/synchronous-dataflow/) page.
- **Not memory optimal.** Different valid orders need different buffer sizes.

## Variants and improvements

- **Looped and single appearance schedules.** Code size grows with $Q$ if every firing is a line of code. Bhattacharyya, Murthy and Lee (1996) write schedules as nested loops, such as $(3A)(2B)C$ for the ring, and study single appearance schedules, in which each actor appears once. These exist only under conditions on the cycles of the graph, and choosing the loop nest trades code size against buffer memory; the book gives heuristics for this trade.
- **Buffer minimization.** Among all PASSes, choose one with the least total buffer. The greedy order is not chosen for this; the book treats the problem and its heuristics.
- **Parallel schedules.** Expand the graph into its precedence graph, with $q_a$ copies of actor $a$, and schedule that graph on several processors with a list scheduler. With execution times, the best period on unlimited processors is the [iteration bound](/iteration-bound/) of the expansion, and [unfolding](/dsp-unfolding/) several periods can help to reach it.
- **The requirement graph.** The proof of Theorem 3 on the [synchronous dataflow](/synchronous-dataflow/) page gives another exact test: build the graph of firings and their requirements, and look for a cycle with a [topological sort](/topological-sort/). The simulation is simpler and does the same work in the same order of time.

## When to use it

Use it in any compiler or synthesis tool for SDF graphs, as the first check that a program can run forever in bounded memory and as the source of a valid schedule. When code size or buffer memory matters, use its answer as a starting point for a looped or memory-aware scheduler, never as the final schedule. When some rates depend on the data, SDF does not apply; the program is a general [Kahn process network](/kahn-process-network/), and these questions become undecidable.

## Pitfalls

- **Floating point rates.** Lines L1 to L3 need exact rationals or integers. With floating point, a consistent graph can fail line L2 by rounding, or an inconsistent one can pass.
- **Overflow.** Entries of $q$ grow as products of rates along paths, as in the chain above. Fixed-width integers can overflow on large graphs.
- **Firing up to $J q$.** A loop that fires until no actor is enabled, without the bound count$_a < q_a$, runs forever on a graph that has a PASS. The bound is what ends the period.
- **Stopping on the first blocked actor.** A blocked actor may become enabled later. Only an empty queue, with every actor blocked or at its count, proves a deadlock.
- **Self loops and disconnected graphs.** A self loop with $p_e \ne c_e$ makes the graph inconsistent. A graph with several components must be split first, since its null space has one dimension per component.

## Implementations

## History

Lee and Messerschmitt (1987) introduced synchronous dataflow for signal processing and gave the rank test, the repetition vector and the class-S algorithm, the simulation of this page, with the proof that it finds a PASS whenever one exists. The Ptolemy project at Berkeley built code generators on these schedules. Bhattacharyya, Murthy and Lee (1996) turned the flat schedules into looped schedules with small code and buffer memory.

## References
