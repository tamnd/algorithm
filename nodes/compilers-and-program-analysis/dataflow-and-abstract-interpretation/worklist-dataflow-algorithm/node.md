---
tag: 5353DC
kind: algorithm
slug: worklist-dataflow-algorithm
name: Worklist dataflow algorithm
aliases:
- Kildall's algorithm
- iterative dataflow algorithm
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: Solves dataflow equations by keeping a worklist of nodes whose input changed and applying their transfer functions until nothing changes.
solves: [reaching-definitions, live-variable-analysis, available-expressions, very-busy-expressions, constant-propagation-problem]
model: word-ram
complexity:
  vars: {n: the number of blocks, m: the number of edges, h: the height of the lattice}
  time: {worst: O((n + m)(h + 1)), average: O((n + m)(h + 1)), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [monotone-dataflow-framework, maximal-fixed-point-solution]
see_also: [dataflow-analysis, meet-over-all-paths-solution, distributive-dataflow-framework, kam-ullman-iteration-bound, elimination-dataflow-methods, sparse-conditional-constant-propagation, semi-naive-evaluation, widening-operator]
sources:
  - paper: doi:10.1145/512927.512945
    title: "Gary A. Kildall, A unified approach to global program optimization, Proceedings of the 1st ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL 1973), 194-206"
    locator: the whole paper (the iterative algorithm from the top element, and its result for distributive functions)
  - paper: doi:10.1007/BF00290339
    title: "John B. Kam and Jeffrey D. Ullman, Monotone data flow analysis frameworks, Acta Informatica 7(3), 1977, 305-317"
    locator: the whole paper (the maximal fixed point of a monotone framework, the proof that Kildall's algorithm computes it, and the proof that it is below the meet over all paths)
  - paper: doi:10.1145/321921.321938
    title: "John B. Kam and Jeffrey D. Ullman, Global data flow analysis and iterative algorithms, Journal of the ACM 23(1), 1976, 158-171"
    locator: the whole paper (the analysis of round-robin iteration in depth-first order, which covers the bit-vector problems)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Pearson Addison-Wesley, 2007
    locator: Section 9.3.3 (The Iterative Algorithm for General Frameworks), Section 9.3.4 (Meaning of a Data-Flow Solution) and Section 9.6.7 (Speed of Convergence of Iterative Data-Flow Algorithms)
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 9 (Data-Flow Analysis), Section 9.2 (Iterative Data-Flow Analysis)
  - book: isbn:9783540654100
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999
    locator: Section 2.4 (Equation Solving, the worklist algorithm for the MFP solution), in the join convention where the same solution is the least one
---

The worklist dataflow algorithm solves the equations of a [monotone dataflow framework](/monotone-dataflow-framework/). Every node of the graph gets the value $\top$, the start nodes get the boundary value $\iota$, and a queue holds the nodes whose output may still change. The algorithm takes a node from the queue, applies its transfer function, meets the result into the input of each successor, and puts back every successor whose input went down. When the queue is empty, the values are the [maximal fixed-point solution](/maximal-fixed-point-solution/) (MFP), the greatest solution of the equations. It is safe, because MFP is below the [meet-over-all-paths solution](/meet-over-all-paths-solution/), and it equals that solution in a [distributive dataflow framework](/distributive-dataflow-framework/) where every node is reachable. With $n$ nodes, $m$ edges and a lattice of height $h$, it applies at most $n(h + 1)$ transfer functions and $m(h + 1)$ meets. The same code solves [reaching definitions](/reaching-definitions/), [live variables](/live-variable-analysis/), [available expressions](/available-expressions/), [very busy expressions](/very-busy-expressions/) and [constant propagation](/constant-propagation-problem/); only the lattice, the functions and the direction change.

## In plain words

Picture the blocks of a program, each with a note that says what is known there. At first every note holds the most hopeful claim, except at the place where the analysis starts, which gets the honest starting fact. Every block goes on a to-do list. Take a block off the list, work out what holds when control leaves it, and hand that to the blocks that come next. Each of them combines the new fact with its note. If its note gets weaker, it goes back on the list, because what it hands on may change too. A note can only get weaker, and only a few times, so the list runs empty. Then every note agrees with its neighbors, and the notes are the most precise answer that such local agreement allows.

## The problem

The input is an instance of a monotone framework, in the meet convention used by Kildall, Kam and Ullman, and the dragon book:

- a directed graph $G = (V, E)$ with $n$ nodes and $m$ edges, and a set $S$ of start nodes;
- a meet semilattice $(L, \sqcap)$ with top element $\top$, where $x \sqsubseteq y$ means $x \sqcap y = x$, and of finite height $h$: no strictly descending chain has more than $h$ steps;
- a boundary value $\iota \in L$;
- a monotone transfer function $f_v : L \to L$ for each node $v$.

Let $init(s) = \iota$ if $s \in S$ and $init(s) = \top$ otherwise. The output is the greatest assignment $IN$ with

$$IN[s] = init(s) \sqcap \bigsqcap_{(v, s) \in E} f_v(IN[v]) \quad \text{for every node } s,$$

the [maximal fixed-point solution](/maximal-fixed-point-solution/). For a forward problem, $G$ is the [control flow graph](/control-flow-graph/), $S$ holds the entry block, and $IN[s]$ is the fact at the start of block $s$. For a backward problem, $G$ is the reverse CFG, $S$ holds the blocks that end in `ret`, and $IN[s]$ is the fact at the end of block $s$. The facts on the other side of each block are $f_s(IN[s])$.

| problem | graph | start nodes | meet | $\top$ | $\iota$ |
|---|---|---|---|---|---|
| reaching definitions | CFG | entry | $\cup$ | $\emptyset$ | $\emptyset$ |
| live variables | reverse CFG | `ret` blocks | $\cup$ | $\emptyset$ | $\emptyset$ |
| available expressions | CFG | entry | $\cap$ | all expressions | $\emptyset$ |
| very busy expressions | reverse CFG | `ret` blocks | $\cap$ | all expressions | $\emptyset$ |
| constant propagation | CFG | entry | per variable, in a flat lattice | no value yet, for every variable | parameters not constant |

May problems use union and must problems use intersection. In a must problem $\top$ is the set of all items, so the boundary value $\emptyset$ is the bottom element and not $\top$.

## The algorithm

$IN$ only goes down during the run, so line L8 can meet the new output into the old value instead of recomputing the meet over all predecessors. A flag per node records whether it is in the queue, so the test of line L11 costs $O(1)$. The queue starts with every node, in reverse postorder from the start nodes (see [depth-first orders](/depth-first-orders/)), so on the acyclic parts of the graph a node usually runs after all its predecessors.

```pseudo id=main
WORKLIST(V, succ, S, ι, ⊤, ⊓, f)
L1  for each node v in V do IN[v] ← ⊤
L2  for each start node s in S do IN[s] ← ι
L3  W ← a queue that holds every node of V once, in reverse postorder
L4  while W is not empty do
L5      v ← remove the first node of W
L6      out ← f_v(IN[v])
L7      for each successor s of v do
L8          new ← IN[s] ⊓ out
L9          if new ≠ IN[s] then
L10             IN[s] ← new
L11             if s is not in W then append s to W
    return IN
```

A backward problem calls the same procedure with the predecessor lists as $succ$ and the `ret` blocks as $S$. Nothing else changes.

## Example

The running example of [dataflow analysis](/dataflow-analysis/) has the parameters `n` and `x`:

```
entry:
  i = 0
  s = 0
  jump head
head:
  t = i < n
  br t body done
body:
  a = x * 2
  u = i & 1
  br u odd next
odd:
  s = s + a
  jump next
next:
  i = i + 1
  jump head
done:
  ret s
```

Take live variables, a backward problem. The reverse CFG has `done` as its only start node, and the queue starts with its reverse postorder `done`, `head`, `next`, `odd`, `body`, `entry`. $IN[v]$ is the set live at the end of $v$, and line L6 gives the set live at its start, which goes to the predecessors of $v$ in the CFG.

| step | node | out (live at its start) | IN changed at | queue after the step |
|---|---|---|---|---|
| 1 | done | s | head | head, next, odd, body, entry |
| 2 | head | i, n, s | entry, next | next, odd, body, entry |
| 3 | next | i, n, s | body, odd | odd, body, entry |
| 4 | odd | a, i, n, s | body | body, entry |
| 5 | body | i, n, s, x | head | entry, head |
| 6 | entry | n | none | head |
| 7 | head | i, n, s, x | entry, next | entry, next |
| 8 | entry | n, x | none | next |
| 9 | next | i, n, s, x | body, odd | body, odd |
| 10 | body | i, n, s, x | none | odd |
| 11 | odd | a, i, n, s, x | none | empty |

The first pass misses `x` in most blocks, because `x` is read only in `body` and that read reaches `head`, `next` and `odd` only around the loop. Step 5 lowers $IN[\text{head}]$ when `head` has already left the queue, so `head` goes back in, and its new output then reaches `entry` and `next` again. The run applies 11 transfer functions, does 13 unions and changes an $IN$ value 11 times; no value changes more than 3 times. With $n = 6$ blocks, $m = 7$ edges and $h = 7$ variables, the bounds are 48 transfer functions and 56 meets. On the same program, reaching definitions also takes 11 transfer functions and 13 meets, available expressions and very busy expressions take 6 and 7 (each block runs once), and constant propagation takes 14 and 17, with $h = 14$.

## Correctness

The full proof is in the proof file. Its steps:

1. **Values only go down.** Line L8 gives $new = IN[s] \sqcap out \sqsubseteq IN[s]$, so every change at line L10 is a strict step down.
2. **Termination and counts.** By step 1 each $IN[s]$ changes at most $h$ times. A node enters the queue once at line L3 and once more at most after each change, so it is removed at most $h + 1$ times.
3. **Nothing safe is lost.** For every assignment $X$ with $X \sqsubseteq F(X)$, where $F$ is the right side of the equations, $X \sqsubseteq IN$ holds at all times. It holds after line L2, and line L10 keeps it because $X[s] \sqsubseteq f_v(X[v]) \sqsubseteq f_v(IN[v])$ by monotonicity.
4. **The end is a fixed point.** A node that is not in the queue has sent its current output to all its successors, and a change of its own value puts it back. So at the end $IN[s] \sqsubseteq f_v(IN[v])$ for every edge, and $IN \sqsubseteq F(IN)$. Every node runs at least once, and every value at the end is the meet of $init(s)$ and of outputs computed from higher values, so also $F(IN) \sqsubseteq IN$.
5. **It is the MFP.** By steps 3 and 4 the result is a fixed point above every fixed point. The order of the queue does not matter for the result.
6. **Safety and precision.** Induction on path length gives $\mathrm{MFP} \sqsubseteq \mathrm{MOP}$ for every monotone framework. If every function is distributive and every node is reachable from $S$, then $\mathrm{MOP} \sqsubseteq F(\mathrm{MOP})$, so step 3 gives $\mathrm{MOP} \sqsubseteq \mathrm{MFP}$ and the two are equal. Gen-kill functions $x \mapsto g \cup (x - k)$ are distributive over $\cup$ and over $\cap$, so this covers the four bit-vector problems.

## Complexity

A transfer function or a meet counts as one lattice operation. The proved bounds:

- **Transfer functions.** Each removal of a node from the queue applies one function. A node is removed at most once more than its value changes, so there are at most $n + C \le n(h + 1)$ of them, where $C \le n h$ is the total number of changes.
- **Meets.** Each removal of $v$ does one meet per outgoing edge, so there are at most $\sum_v (h + 1)\, outdeg(v) = m(h + 1)$ meets.
- **Total.** $O((n + m)(h + 1))$ lattice operations, plus $O(1)$ queue work per operation. The extra space is one value per node, the queue and the flags, $\Theta(n)$ values.
- **Best case.** If the graph is acyclic and the queue starts in a topological order, such as reverse postorder from the start nodes when every node is reachable, no node is ever appended again: exactly $n$ transfer functions and $m$ meets.
- **Bit vectors.** For a gen-kill problem over $U$ items, $h = |U|$ and one operation costs $O(|U| / w)$ word operations on a $w$-bit word RAM, so the worst case is $O((n + m)|U|^2 / w)$. For constant propagation over $v$ variables, $h = 2v$.

The bound is a worst case allowed by the height, and it is rarely reached. The table below is *measured*, not proved: it comes from 300 random looping programs of the toy IR (seed 31337), with 3 to 8 blocks and 25.6 instructions on average (at most 43), solved with a queue in reverse postorder.

| analysis | transfer functions per block, average | per block, worst | most changes of one value | largest $h$ | meets per edge, worst |
|---|---|---|---|---|---|
| reaching definitions | 1.36 | 2.12 | 6 | 35 | 2.33 |
| live variables | 1.32 | 2.25 | 4 | 14 | 2.11 |
| available expressions | 1.11 | 1.67 | 4 | 24 | 1.78 |
| very busy expressions | 1.16 | 1.71 | 3 | 24 | 1.67 |
| constant propagation | 2.04 | 3.50 | 7 | 28 | 3.67 |

The bound allows $h + 1$ transfer functions per block, up to 36 here, and the worst run used 3.5. For rapid frameworks such as the bit-vector problems, the [Kam-Ullman iteration bound](/kam-ullman-iteration-bound/) shows that the number of round-robin sweeps depends on the loops of the graph and not on $h$.

## Properties

- **Order-free result.** Any initial order of the queue, and a stack or a priority queue in place of the FIFO queue, gives the same MFP. Only the amount of work depends on the order.
- **Deterministic.** For a fixed order the run, its counts and its result are fixed.
- **Non-recursive.** One loop and a queue; no recursion.
- **Generic.** The algorithm needs only $\top$, $\iota$, the meet, an equality test and the transfer functions. The lattice can be sets, bit vectors, maps from variables to constants, or any other domain of finite height.
- **No safe partial answer.** Values move down only, so a run stopped early can leave values that are too high, which is unsafe.

## Variants and improvements

- **Round-robin iteration.** Sweep over all nodes in reverse postorder until a whole sweep changes nothing. For rapid frameworks, which include the four bit-vector problems, $d + 2$ sweeps suffice, where $d$ is the largest number of back edges on an acyclic path ([Kam-Ullman iteration bound](/kam-ullman-iteration-bound/)). It is simpler, but it revisits nodes whose inputs did not change.
- **Priority by order.** Keep the worklist sorted by reverse postorder number and always take the earliest node. This follows the flow of the program more closely than a FIFO queue, and the result is the same.
- **Recompute the input.** Store $OUT[v] = f_v(IN[v])$ and recompute $IN[s]$ as the meet over all predecessors when $s$ is taken from the queue, as in the dragon book. This gives the same result, but a node with $k$ predecessors costs $k$ meets per visit.
- **Bit-vector parallelism.** For gen-kill problems, store each set as a bit vector, so one machine word handles $w$ items at once.
- **Elimination methods.** [Elimination dataflow methods](/elimination-dataflow-methods/) solve the equations by the loop structure of a [reducible flow graph](/reducible-flow-graph/), instead of by iteration.
- **Sparse analysis.** On [static single assignment form](/static-single-assignment-form/), facts about a variable can travel along def-use edges instead of through every block. [Sparse conditional constant propagation](/sparse-conditional-constant-propagation/) runs one worklist of CFG edges and one of SSA edges.
- **Deltas.** For a union meet, send only the items that are new since the last visit, as in [semi-naive evaluation](/semi-naive-evaluation/) of Datalog.
- **Infinite height.** For lattices such as intervals, the run may not end. [Abstract interpretation](/abstract-interpretation/) adds a [widening operator](/widening-operator/) at loop heads to force termination, in the join convention where values go up from $\bot$.
- **Interprocedural problems.** The [IFDS framework](/ifds-framework/) runs a worklist over path edges of an exploded supergraph.

## When to use it

Use it for any intraprocedural dataflow problem with monotone transfer functions and a lattice of finite height. It is the standard solver in compilers and static analyzers: it needs no structure of the graph, works for irreducible control flow, and does little work on typical programs. If the lattice has infinite height, add widening. If the program is in SSA form and the facts are per variable, a sparse solver is often faster.

## Pitfalls

- **Setting the boundary to $\top$.** The boundary value $\iota$ describes the start of the program (or the point after `ret`) and is usually not $\top$. In available expressions, $\iota = \emptyset$ but $\top$ is the set of all expressions; starting the entry at $\top$ claims that every expression is available on entry. In the may problems $\top = \iota = \emptyset$, which hides the difference.
- **Running a backward problem on the CFG.** A backward problem needs the reverse CFG, with the `ret` blocks as start nodes and the queue order taken from the reverse CFG. Its $IN$ values are the facts at the ends of the blocks.
- **Starting a must problem at the empty set.** The other nodes must start at $\top$, the set of all items. Starting at $\emptyset$ still ends at a fixed point, but often a smaller one: an expression computed before a loop is lost at the loop head, because the back edge brings $\emptyset$.
- **A queue that does not hold every node at the start.** If line L3 puts only the start nodes in the queue, a node whose input never changes is never processed, so its own facts, such as its definitions in reaching definitions, never reach its successors. Line L3 must queue every node once.
- **Unreachable nodes.** Nodes that the start nodes do not reach get values from the equations alone, which can differ from MOP. For example, an unreachable block that loops to itself keeps its own definitions in reaching definitions. MFP = MOP needs every node to be reachable.
- **Non-monotone functions.** If a transfer function is not monotone, the equations may have no solution. This algorithm still stops, because line L8 only lowers values, but its result is then not a solution, and a solver that recomputes inputs can loop forever. With one item $d$, union as the meet and a self-loop with the function $X \mapsto \{d\} - X$, this algorithm returns $\{d\}$, which does not satisfy $X = \{d\} - X$.
- **Self-loops.** Line L5 must clear the queue flag of $v$ before the loop of line L7, so that a self-loop that lowers $IN[v]$ puts $v$ back.

## Implementations

## History

Kildall (1973) described one iterative algorithm for a whole family of global optimization problems, parameterized by a lattice and the functions of the nodes. It starts from the top element and lowers values until they are stable, and Kildall showed that it gives the meet over all paths when the functions are distributive. Kam and Ullman (1976) studied round-robin iteration in depth-first order and bounded the number of sweeps for the bit-vector problems. Kam and Ullman (1977) defined monotone frameworks, proved that Kildall's algorithm computes the maximal fixed point, which is below the meet over all paths and can differ from it, and showed that no algorithm computes the meet over all paths for every monotone framework. Textbooks give both the round-robin and the worklist forms (Aho, Lam, Sethi and Ullman; Cooper and Torczon; Nielson, Nielson and Hankin, who use the join convention and least fixed points).

## References
