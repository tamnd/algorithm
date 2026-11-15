---
tag: 8QKCJ8
kind: algorithm
slug: pdg-slicing
name: Slicing by dependence graph reachability
aliases:
- Ottenstein PDG slicing
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: Computes a backward slice as the set of nodes that reach the criterion in the program dependence graph, in linear time in its size.
solves: [program-slicing]
model: word-ram
complexity:
  vars: {n: the number of statements, e: the number of control and data edges of the program dependence graph}
  time: {worst: O(n + e)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: false, executable_result: false}
history:
  year: 1984
  people: [Karl J. Ottenstein, Linda M. Ottenstein]
  note: The Ottensteins proposed the program dependence graph as the internal form of a software development environment, so that slices become a linear-time graph search.
prereqs: [program-slicing, program-dependence-graph, graph-reachability]
see_also: [weiser-slicing, system-dependence-graph-slicing, dynamic-slicing, control-dependence, data-dependence, aggressive-dead-code-elimination, depth-first-search, reaching-definitions]
sources:
  - paper: doi:10.1145/390011.808263
    title: Karl J. Ottenstein and Linda M. Ottenstein, The program dependence graph in a software development environment, ACM SIGPLAN Notices 19(5) (Proceedings of the ACM SIGSOFT/SIGPLAN Software Engineering Symposium on Practical Software Development Environments), 1984, pages 177-184
    locator: the dependence graph as the internal form of the environment, and slices found by a linear-time walk over its edges
  - paper: doi:10.1145/24039.24041
    title: Jeanne Ferrante, Karl J. Ottenstein and Joe D. Warren, The program dependence graph and its use in optimization, ACM Transactions on Programming Languages and Systems 9(3), 1987, pages 319-349
    locator: control dependence from the post-dominator tree, the definition of the graph used here
  - paper: doi:10.1007/3-540-50940-2_47
    title: Thomas Reps and Wuu Yang, The semantics of program slicing and program integration, TAPSOFT '89, Lecture Notes in Computer Science 352, Springer, 1989, pages 360-374
    locator: the Slicing Theorem (on every initial state on which the program halts, the slice computes the same sequence of values at each of its points) and the Termination Theorem
  - paper: doi:10.1145/77606.77608
    title: Susan Horwitz, Thomas Reps and David Binkley, Interprocedural slicing using dependence graphs, ACM Transactions on Programming Languages and Systems 12(1), 1990, pages 26-60
    locator: slicing within one procedure as reachability in the dependence graph, the base case of the interprocedural method
  - paper: "Frank Tip, A survey of program slicing techniques, Journal of Programming Languages 3(3), 1995, pages 121-189"
    locator: the section on static slicing with dependence graphs, and the comparison with the dataflow method of Weiser
---

Slicing by dependence graph reachability solves the [program slicing](/program-slicing/) problem with one backward search. Build the [program dependence graph](/program-dependence-graph/) (PDG), whose edges go from each statement to the statements that use its values or that it decides to run. The slice for a criterion is the set of nodes from which the criterion can be reached along these edges. Karl and Linda Ottenstein proposed this in 1984. Once the graph is built, each slice costs time linear in the size of the graph, and slices for other criteria, forward slices and chops come from the same graph. The result is a set of statements, not a program: to run it, the jumps and the block structure must be put back.

## In plain words

First draw a map of the program. Each line is a dot. Draw an arrow from one line to another when the second line uses a value that the first line wrote, or when the first line is a test that decides whether the second line runs. To slice, start at the chosen line and walk the arrows backward. Every dot you can reach is in the slice. Each arrow is walked at most once, so the walk is fast, even if the map took some time to draw. One map serves every slice of the same program. The dots you reach tell you which lines matter, but they do not say how to jump between them. To run the slice, you still have to put the jumps back.

## The problem

Programs are in the toy IR, with the conventions of the [program slicing](/program-slicing/) page: a statement $(\ell, i)$ is instruction $i$ of block $\ell$, or its terminator; $DEF$ and $REF$ are the variables written and read; every block reaches a `ret`. The input is a program $P$ and a criterion $\langle p, V \rangle$, the values of the variables of $V$ just before statement $p$. The output is the dependence slice: the least set of instructions and branches that contains the definitions of $V$ that reach $p$ and the branches that $p$ is control dependent on, and that is closed under data and control dependence.

The graph is the PDG of the [program dependence graph](/program-dependence-graph/) page. Its nodes are the statements and a node ENTRY, which stands for the start of the run and the values of the parameters. A *data edge* $s \to t$ labeled $x$ means that $s$ defines $x$, $t$ reads $x$, and some path in the control flow graph goes from just after $s$ to $t$ with no other definition of $x$ ([data dependence](/data-dependence/), from [reaching definitions](/reaching-definitions/)). A *control edge* $b \to t$ means that the block of $t$ is [control dependent](/control-dependence/) on the branch $b$ in the sense of Ferrante, Ottenstein and Warren; the blocks that run on every run get a control edge from ENTRY.

## The algorithm

The criterion is not a node, so the search starts from its parents: the definitions of the variables of $V$ that reach $p$, and the control parents of $p$. This is the same as adding a node at $p$ that reads $V$.

```pseudo id=main
PDG-SLICE(P, p, V)
L1  G <- the PDG of P, unless it is already built
L2  W <- the statements s such that a definition of some x in V by s reaches p
L3  W <- W union the control parents of p; remove ENTRY from W
L4  S <- W
L5  while W is not empty do
L6      remove a node z from W
L7      for each control or data edge x -> z of G do
L8          if x is not ENTRY and x is not in S then add x to S and to W
L9  return S
```

Lines L5 to L8 are a [graph search](/graph-reachability/) over the reversed edges; any order of the work list gives the same set. ENTRY is left out of the result because it is not a statement.

To get a program that runs, build the projection of the problem page: keep the statements of $S$, keep every jump, turn each branch outside $S$ into a jump to the immediate [post-dominator](/post-dominance/) of its block (or `ret 0` when that is the exit), and let a `ret a` keep $a$ only when it is the statement $p$ and $a \in V$. In the implementation, `build_pdg` builds the graph with the walk of Ferrante, Ottenstein and Warren up the post-dominator tree and with reaching definitions, `pdg_slice` is the search, `executable_slice` builds the projection, and `observe` runs a program and records the values of $V$ at a point.

## Example

Take the program of the problem page, which sums the odd numbers up to $n$ in $s$ and computes $p = n!$.

```
B1:
  i = 1
  s = 0
  p = 1
  jump B2
B2:
  t = i <= n
  br t B3 B6
B3:
  p = p * i
  u = i % 2
  br u B4 B5
B4:
  s = s + i
  jump B5
B5:
  i = i + 1
  jump B2
B6:
  ret s
```

The control edges: ENTRY controls B1, B2 and B6, which run on every run; `br t B3 B6` controls B2, B3 and B5 (B2 because the test runs again after each trip); `br u B4 B5` controls B4. The data edges into the statements that matter here:

| statement | data parents | control parents |
|---|---|---|
| `t = i <= n` | `i = 1`, `i = i + 1`, ENTRY for $n$ | ENTRY, `br t` |
| `br t B3 B6` | `t = i <= n` | ENTRY, `br t` |
| `p = p * i` | `i = 1`, `i = i + 1`, `p = 1`, `p = p * i` | `br t` |
| `i = i + 1` | `i = 1`, `i = i + 1` | `br t` |
| `p = 1`, `i = 1` | none | ENTRY |

For the criterion $\langle (B6, 0), \{p\} \rangle$, the definitions of $p$ that reach B6 are `p = 1` and `p = p * i`, and B6 has only ENTRY as control parent. So the search starts from these two. One order of the search:

| removed | added to $S$ |
|---|---|
| start | `p = 1`, `p = p * i` |
| `p = p * i` | `i = 1`, `i = i + 1`, `br t B3 B6` |
| `br t B3 B6` | `t = i <= n` |
| `t = i <= n`, `i = i + 1`, `i = 1`, `p = 1` | nothing new |

The slice has 6 statements, the same as [Weiser's algorithm](/weiser-slicing/) finds: `i = 1`, `p = 1`, `t = i <= n`, `br t B3 B6`, `p = p * i` and `i = i + 1`. None of the jumps is in it, because a jump writes nothing and decides nothing. For $\langle (B6, 0), \{s\} \rangle$ the same graph gives 8 statements, and for the value of $i$ just before `i = i + 1` it gives `i = 1`, `t = i <= n`, `br t B3 B6` and `i = i + 1`.

**Where the jumps matter.** The next program counts the numbers from 1 to $n$ that are not multiples of 3. Block B4 is a `continue`: it jumps back to the loop test.

```
B1:
  i = 0
  c = 0
  jump B2
B2:
  t = i < n
  br t B3 B6
B3:
  i = i + 1
  r = i % 3
  br r B5 B4
B4:
  jump B2
B5:
  c = c + 1
  jump B2
B6:
  ret c
```

For $\langle (B6, 0), \{c\} \rangle$ the slice is every statement except the jumps and the `ret`. The projection keeps `jump B2` in B4 and gives $c = 4$ for $n = 6$, like the program. If the slice is turned back into source code by deleting the statements outside it, the `continue` disappears, control falls into `c = c + 1`, and the result is 6.

## Correctness

The full proof is in the proof file. Its steps:

1. **The search finds the dependence slice.** The start set holds exactly the statements of the first two rules of the problem page, the search adds only parents, and it stops with a set closed under all parents. So it returns the least closed set.
2. **Relevant names.** For a set $S$ closed in this way, call a variable relevant at a statement if some path from there carries it, with no new definition, to a use in $S$ or to $V$ at $p$. A dropped instruction never writes a relevant variable, because the reader would make it a data parent of a statement of $S$.
3. **Dropped branches.** The blocks that a dropped branch decides, up to its immediate post-dominator, are in the transitive closure of its control dependences, so none of them holds a statement of $S$ or $p$.
4. **The projection keeps the values.** A simulation relates the two runs when their environments agree on the relevant variables. It gives the slicing theorem of Reps and Yang (1989): on every input on which the program returns, the projection returns, and the values of $V$ at $p$ form the same sequence. More generally, each statement of the slice runs as many times with the same operand values.

## Complexity

**Proved.** Each node enters the work list at most once, and each edge is read once when its target is removed. So the search takes $O(n + e)$ time, where $n$ is the number of statements and $e$ the number of control and data edges. It needs $O(n)$ extra space for $S$ and the work list.

**Building the graph.** The graph itself costs more, and it can have $\Theta(n^2)$ edges, for example $k$ definitions of one variable that all reach $k$ uses. The [program dependence graph](/program-dependence-graph/) page gives the cost: control edges in $O(m + c)$ after post-dominators, and data edges from reaching definitions. The graph is built once and serves every slice of the program, so the cost of building it is shared among all the slices.

**Compared.** [Weiser's algorithm](/weiser-slicing/) needs no graph but solves dataflow equations again for each criterion, up to $c + 1$ times for $c$ branches. Both give the same set of statements.

## Properties

- **Same set as Weiser.** For one procedure, the reachable set is exactly the dependence slice, which is also the set of Weiser's algorithm.
- **Not a program.** The result is a set of nodes. Jumps never appear in it, and a branch outside it must be rerouted to its post-dominator before the slice runs.
- **Many slices from one graph.** After the graph is built, each backward slice, each forward slice (the same search over the edges in their own direction) and each chop costs linear time.
- **Static.** The slice holds for every input. It can contain statements that no run needs.
- **Deterministic.** The order of the work list changes the order of the visits, not the set.

## Variants and improvements

- **Forward slices and chops.** Search along the edges instead of against them to find what a statement can affect. Intersect a forward and a backward slice to get the chop between two statements.
- **Across procedures.** Joining the PDGs of the procedures with call and parameter edges and searching naively mixes calling contexts. [System dependence graph slicing](/system-dependence-graph-slicing/) of Horwitz, Reps and Binkley adds summary edges and searches in two phases.
- **Unstructured jumps.** Ball and Horwitz (1993) and Agrawal (1994) give methods that add to the slice the `goto`, `break` and `continue` statements that a source-level slice needs.
- **Dynamic dependence graphs.** Built from one run instead of from the program text, the same search gives [dynamic slices](/dynamic-slicing/).
- **Dead code.** With all outputs as the criterion, the statements outside the slice are dead; [aggressive dead code elimination](/aggressive-dead-code-elimination/) works this way.

## When to use it

Use it when many slices of the same program are needed: in a debugger or an editor that shows slices on demand, in tools for program understanding, in change impact analysis with forward slices, and in program integration. Build the graph once and answer each query with one search. For a single slice where an executable program is wanted and no graph is at hand, [Weiser's algorithm](/weiser-slicing/) is simpler.

## Pitfalls

- **Expecting a runnable program.** The slice is a set of nodes. It runs only after the jumps are kept and the branches outside it are rerouted to their immediate post-dominators. Deleting statements from source code with `goto`, `break` or `continue` can change where control goes, as the `continue` example shows.
- **Starting at the criterion node.** The node of $p$ itself and its own data parents are the slice of the statement $p$ with $V = REF(p)$. For another set $V$, start from the definitions of $V$ that reach $p$ and the control parents of $p$.
- **Missing the edge from ENTRY.** Without the control edges from ENTRY, the statements that run on every run have no control parent. This does not change the slice of a single procedure, but across procedures it loses the dependence of a callee on its call sites.
- **Using a weak control dependence.** Some tools make the code after a loop depend on the loop test. That keeps non-termination, but it gives larger slices than the dependence slice of the problem page.
- **Reading a slice as minimal.** Every path counts, including paths that no input takes, so the slice can be larger than needed. The smallest slice is not computable.

## Implementations

## History

Karl and Linda Ottenstein proposed in 1984 that a software development environment keep programs as program dependence graphs, so that slices for debugging become linear-time searches. Ferrante, Ottenstein and Warren gave the general definition of the graph, with control dependence from post-dominators, in 1987. Reps and Yang (1989) proved that a dependence graph slice computes the same values as the program on every run that halts, and Horwitz, Reps and Binkley (1990) extended the method across procedures. Tip's survey of 1995 compares the graph method with Weiser's dataflow method.

## References
