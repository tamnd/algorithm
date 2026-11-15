---
tag: S2FQ4Y
kind: algorithm
slug: weiser-slicing
name: Weiser's slicing algorithm
aliases:
- dataflow-based slicing
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: Computes a backward slice by iterating relevant-variable sets over the flow graph and adding the branches that control included statements.
solves: [program-slicing]
model: word-ram
complexity:
  vars: {n: the number of statements, m: the number of control flow edges between statements, v: the number of variables, c: the number of branches}
  time: {worst: O((c + 1) (n + m) v^2)}
  space: {extra: O(n v + c n)}
properties: {deterministic: true, recursive: false, online: false, executable_result: true}
history:
  year: 1981
  people: [Mark Weiser]
  note: Weiser defined slices and gave this algorithm in his 1979 thesis at the University of Michigan, at ICSE 1981, and in IEEE TSE in 1984.
prereqs: [program-slicing, control-flow-graph, post-dominance, live-variable-analysis]
see_also: [pdg-slicing, control-dependence, worklist-dataflow-algorithm, distributive-dataflow-framework, system-dependence-graph-slicing, dynamic-slicing, aggressive-dead-code-elimination, cooper-harvey-kennedy-dominance]
sources:
  - paper: "Mark Weiser, Program slicing, Proceedings of the 5th International Conference on Software Engineering, San Diego, March 1981, pages 439-449"
    locator: the relevant variables, the sets of included statements and branches, the INFL sets and the iteration
  - paper: doi:10.1109/TSE.1984.5010248
    title: Mark Weiser, Program slicing, IEEE Transactions on Software Engineering SE-10(4), 1984, pages 352-357
    locator: the equations for the directly relevant variables and statements, the influence sets of branches through the nearest inverse dominator, the iteration to a fixed point, and slices across procedures
  - paper: "Mark Weiser, Program slices: formal, psychological, and practical investigations of an automatic program abstraction method, PhD thesis, University of Michigan, Ann Arbor, 1979"
    locator: the first statement of slices and of the dataflow method
  - paper: "Frank Tip, A survey of program slicing techniques, Journal of Programming Languages 3(3), 1995, pages 121-189"
    locator: the section on static slicing with dataflow equations, the cost of Weiser's algorithm, and the problems with unstructured control flow
  - paper: doi:10.1145/24039.24041
    title: Jeanne Ferrante, Karl J. Ottenstein and Joe D. Warren, The program dependence graph and its use in optimization, ACM Transactions on Programming Languages and Systems 9(3), 1987, pages 319-349
    locator: control dependence defined by post-dominance, which matches the influence sets of the algorithm
---

Weiser's algorithm solves the [program slicing](/program-slicing/) problem with backward dataflow equations. For a criterion $\langle p, V \rangle$ it computes, at each statement, the set of *relevant* variables: the variables whose values at that statement can flow into $V$ at $p$. A statement that writes a relevant variable joins the slice. A branch joins the slice when one of the statements it controls is in the slice, and then the variables that the branch reads become relevant too. The algorithm repeats this until no new branch joins. The result is the dependence slice of the problem page, and deleting the other statements gives a program that runs and gives the same values at $p$. Mark Weiser gave the algorithm in his thesis (1979), at ICSE 1981 and in IEEE TSE (1984).

## In plain words

Pick a line and a few variables. Walk backward through the program and keep a list, at each line, of the variables that still matter. At the chosen line, the list holds the chosen variables. Going back over a line that writes a variable on the list, keep that line, take the variable off the list and put on the variables the line reads. Other lines are dropped, and the list passes through them. A loop brings the walk back to lines already seen, so it goes on until no list grows. Then look at the tests. A test that decides whether a kept line runs must be kept too, and the variables it reads start new lists. Repeat the whole walk with these extra starting points until no new test is added. The kept lines form a smaller program that still computes the chosen variables.

## The problem

Programs are in the toy IR of the [control flow graph](/control-flow-graph/) pages, with the conventions of the [program slicing](/program-slicing/) page. A statement $n = (\ell, i)$ is instruction $i$ of block $\ell$, or its terminator when $i$ equals the number of instructions. The statements form a graph: an instruction has the next statement of its block as its only successor, and a terminator has the first statements of its target blocks. $DEF(n)$ is the variable that $n$ writes ($\emptyset$ for terminators) and $REF(n)$ is the set of variables it reads. Every block reaches a `ret`. There are $n$ statements, $m$ edges between them, $v$ variables and $c$ branches.

The input is a program $P$ and a criterion $C = \langle p, V \rangle$, where $p$ is a statement (the point just before it) and $V$ is a set of variables. The output is the set $S$ of instructions and branches in the slice, and the executable slice: the projection of $P$ on $S$ as defined on the problem page. Branches outside $S$ become jumps to the immediate [post-dominator](/post-dominance/) of their block, all jumps stay, and a `ret a` keeps $a$ only when $p$ is that return and $a \in V$.

## The algorithm

For a branch $b$ at the end of block $\ell$, let $d$ be the immediate post-dominator of $\ell$, computed with a virtual EXIT after every `ret`. The *influence set* $INFL(b)$ is the set of blocks that can be reached from a successor of $\ell$ by a path that does not enter $d$. These are the blocks whose execution $b$ decides.

For a seed map $\sigma$ that gives a set of variables to some statements, the relevant sets are the least solution of

$$R(n) = \sigma(n) \cup \bigcup_{n \to m} \Bigl( (R(m) \setminus DEF(n)) \cup \bigl( REF(n) \text{ if } DEF(n) \cap R(m) \ne \emptyset \bigr) \Bigr).$$

A variable relevant after $n$ stays relevant before $n$ unless $n$ writes it, and if $n$ writes a relevant variable, the variables $n$ reads become relevant.

```pseudo id=main
WEISER-SLICE(P, p, V)
L1  compute ipdom(l) for every block l, with a virtual EXIT after every ret
L2  for each branch b at the end of a block l do
L3      INFL(b) <- the blocks reachable from the successors of l without entering ipdom(l)
L4  B <- empty
L5  repeat
L6      seeds(p) <- V; seeds(b) <- REF(b) for every b in B; seeds(n) <- empty for all other n
L7      R <- RELEVANT-SETS(P, seeds)
L8      S <- B union { instructions n : DEF(n) meets R(m) for the successor m of n }
L9      newB <- { branches b : INFL(b) holds the block of p or the block of a statement of S }
L10     done <- (newB = B); B <- newB
L11 until done
L12 return S, R

RELEVANT-SETS(P, seeds)
L13 R(n) <- seeds(n) for every statement n
L14 W <- the set of all statements
L15 while W is not empty do
L16     remove a statement m from W
L17     for each predecessor n of m do
L18         X <- R(m) minus DEF(n)
L19         if DEF(n) meets R(m) then X <- X union REF(n)
L20         if X is not a subset of R(n) then R(n) <- R(n) union X; add n to W
L21 return R
```

Round $k$ of lines L5 to L11 is Weiser's step from $R^{k-1}$ to $R^k$. By distributivity, solving once with all the seeds gives the same sets as Weiser's union of one solution for $C$ and one for each branch criterion $\langle b, REF(b) \rangle$. A branch is in $S$ exactly when it is in $B$, because a branch writes nothing. Line L9 also tests the block of $p$, so that a test which decides whether $p$ is reached joins the slice even when no statement of $S$ lies under it. The executable slice is then built from $S$ as in the problem section.

In the implementation, `weiser_slice` returns $S$, $R$, $B$ and the number of rounds, `executable_slice` builds the projection, `slice_point` maps $p$ to its place in the projection, and `observe` runs a program like `toyir.run` and records the values of $V$ at each visit of a point. Post-dominators come from the plain iteration over sets.

### Analysis summary

The relevant sets are a backward dataflow problem, in the Kildall convention of the dataflow pages, like [live variable analysis](/live-variable-analysis/).

| item | value |
|---|---|
| direction | backward |
| may or must | may (a variable is relevant if it is relevant along some path) |
| domain | sets of variables at each statement; height $h = v$ at each statement |
| order and meet | $X \sqsubseteq Y$ when $X \supseteq Y$; meet is union |
| $\top$ and $\bot$ | $\top = \emptyset$, $\bot$ = all variables |
| boundary | the seeds: $V$ at $p$, $REF(b)$ at each branch of $B$; $\emptyset$ after every `ret` |
| initial value elsewhere | $\top = \emptyset$ |
| transfer of $n$ | $f_n(X) = (X \setminus DEF(n)) \cup (REF(n)$ if $DEF(n) \cap X \ne \emptyset)$, applied to the facts of the successors; at a seeded statement, $\sigma(n)$ is added |
| monotone | yes |
| distributive | yes: $f_n(X \cup Y) = f_n(X) \cup f_n(Y)$ |

The transfer is not of gen-kill form, because the variables that $n$ reads are added only when $DEF(n)$ is relevant. This is the transfer of *strong liveness* (faint variables), seeded at the criterion instead of at the exit. Since the framework is distributive, the maximal fixed point equals the meet over all paths ([MOP and MFP coincidence](/mop-mfp-coincidence-theorem/)): $x \in R(n)$ exactly when some path from $n$ carries $x$ to a seed through a chain of writes to relevant variables. With the order turned upside down, this is the least solution under $\subseteq$ reached by iterating up from $\emptyset$, which is how the code and the proof describe it.

**Soundness** is against the runs of the program: the theorem in the proof file says that the projection gives the same values at $p$ as $P$ for every input on which $P$ returns. Every real run follows a path of the control flow graph, so every path counts. **Precision** is lost because every path counts, even paths that no input can take. In the program

```
B1:
  y = 1
  t = a * a
  c = t < 0
  br c B2 B3
B2:
  y = 2
  jump B3
B3:
  ret y
```

with $C = \langle (B3, 0), \{y\} \rangle$, the path through B2 makes `y = 2` relevant, the branch on $c$ joins through $INFL$, and the slice keeps all 5 instructions and branches. No input reaches B2, so `y = 1` alone is a slice.

## Example

Take the program of the problem page, which sums the odd numbers up to $n$ in $s$ and computes $p = n!$, with the criterion $\langle (B6, 0), \{p\} \rangle$.

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

The immediate post-dominators are B1 to B2, B2 to B6, B3 to B5, B4 to B5, B5 to B2 and B6 to EXIT. So $INFL(\texttt{br t}) = \{B2, B3, B4, B5\}$ (the loop, entered from B3 and left only through B6) and $INFL(\texttt{br u}) = \{B4\}$.

| round | seeds | relevant sets (some points) | $S$ | new $B$ |
|---|---|---|---|---|
| 1 | $p$ at (B6, 0) | $\{p\}$ at (B6, 0); $\{i, p\}$ from (B1, 3) to (B5, 1); $\{i\}$ at (B1, 1) and (B1, 2); $\emptyset$ at (B1, 0) | `i = 1`, `p = 1`, `p = p * i`, `i = i + 1` | `br t`, since $INFL$ of it holds B3 and B5 |
| 2 | also $t$ at (B2, 1) | $t$ added at (B2, 1); $n$ added at every point from (B1, 0) to (B5, 1); $R(B2, 1) = \{i, n, p, t\}$ | also `t = i <= n` and `br t` | `br t` only, since $INFL(\texttt{br u}) = \{B4\}$ holds no statement of $S$ |

Round 2 changes nothing in $B$, so the algorithm stops after 2 rounds, with $c = 2$ branches. In round 1, `p = p * i` writes $p$, which is relevant after it, so $i$ and $p$ become relevant before it, and around the loop $i$ stays relevant up to `i = 1`. The statements `s = 0`, `u = i % 2` and `s = s + i` write variables that are never relevant, so they stay out. The executable slice is

```
B1:
  i = 1
  p = 1
  jump B2
B2:
  t = i <= n
  br t B3 B6
B3:
  p = p * i
  jump B5
B4:
  jump B5
B5:
  i = i + 1
  jump B2
B6:
  ret 0
```

The branch on $u$ became `jump B5`, its immediate post-dominator, and `ret s` became `ret 0`, because $s$ is not relevant at the return. On the inputs $n = 0$ to $6$, both programs have $p = 1, 1, 2, 6, 24, 120, 720$ at B6. For the criterion $\langle (B6, 0), \{s\} \rangle$ the algorithm keeps 8 statements, all but `p = 1` and `p = p * i`, also in 2 rounds, and `ret s` keeps its operand.

## Correctness

The full proof is in the proof file. Its steps:

1. **Least solution.** Each transfer is monotone and distributive. The worklist only adds variables that the equations force, and it stops with all equations true, so it returns the least solution. A larger seed map gives larger sets.
2. **Termination.** $B$ only grows from round to round, by step 1, so the loop stops after at most $c + 1$ rounds. At the end: a kept instruction has $REF(n) \subseteq R(n)$; a dropped instruction writes no variable of $R$ at its successor; a kept branch has $REF(b) \subseteq R(b)$; and no $INFL$ of a dropped branch holds a kept statement or $p$.
3. **INFL is control dependence.** For every branch, $INFL(b)$ equals the transitive closure of [control dependence](/control-dependence/) in the sense of Ferrante, Ottenstein and Warren. The proof uses two facts about post-dominance: it is antisymmetric, and the strict post-dominators of a block form a chain.
4. **Dependence slice.** $S$ is exactly the dependence slice of the problem page. $S$ satisfies its three rules, so it contains the least such set. Conversely, the sets $R^\ast$ defined by def-clear paths to the dependence slice are a solution of each round's equations, so by step 1 each round stays inside the dependence slice.
5. **The projection is a slice.** Relate a state of $P$ at statement $n$ to a state of the projection at the image of $n$ when the two environments agree on $R(n)$. A dropped instruction keeps the relation without a step of the projection. A kept instruction or branch runs on equal operands. At a dropped branch, $P$ stays inside $INFL$ until it reaches the post-dominator, makes no observation there and writes no relevant variable, while the projection jumps there in one step. So the observations at $p$ are the same, and if $P$ returns, so does the projection.

## Complexity

**Proved.** Each round runs RELEVANT-SETS once. A statement is added to the worklist only when its set grows, and a set grows at most $v$ times, so each statement is removed at most $v + 1$ times and each edge is handled at most $v + 1$ times, with $O(1)$ set operations each. A round costs $O(v (n + m))$ set operations, and line L8 adds $O(n + m)$ more. There are at most $c + 1$ rounds. The $INFL$ sets cost one search each, $O(c (n + m))$ in total, and line L9 tests them once per round. With sets of $v$ variables as arrays of flags, a set operation costs $O(v)$ word operations, or $O(\lceil v / w \rceil)$ with words of $w$ flags each. The total is $O((c + 1)(n + m) v^2)$ time, plus the post-dominators, which take $O((n + m)\, \alpha(n + m))$ time with [Lengauer and Tarjan](/lengauer-tarjan-algorithm/) on the reverse graph. The space is $O(n v)$ for the relevant sets and $O(c n)$ for the influence sets.

**Reached.** The bound of $c + 1$ rounds is reached when each test reads a variable that is written only under the next test, so that each round adds one more test. In a seeded run over 300 random programs, some programs needed exactly $c + 1$ rounds and none needed more.

**Compared.** To slice for many criteria, building the [program dependence graph](/program-dependence-graph/) once and using [slicing by dependence graph reachability](/pdg-slicing/) costs $O(n + e)$ per criterion, where $e$ is the number of dependence edges. Weiser's algorithm needs no dependence graph, but it runs the whole iteration again for each criterion.

## Properties

- **Executable result.** The output is a program in the same language that runs and keeps the criterion values. A dependence graph slice is a set of nodes and needs this rebuilding step.
- **Same set as the dependence graph.** $S$ is the dependence slice, so for one criterion Weiser's algorithm and backward reachability in the program dependence graph keep the same statements.
- **Distributive equations.** The solution for a set of seeds is the union of the solutions for each seed, so slices for a union of criteria are unions of slices.
- **Static.** The slice works for every input on which $P$ returns. It may hold statements that no input needs, as in the precision example.
- **Deterministic.** The order of the worklist changes the work, not the result.

## Variants and improvements

- **Dependence graphs.** Ottenstein and Ottenstein (1984) replaced the iteration by one backward search in the program dependence graph; see [slicing by dependence graph reachability](/pdg-slicing/). For one procedure it gives the same statements.
- **Procedures.** Weiser sliced across calls by mapping the criterion into the called procedure and out to the callers. This mixes calling contexts and can give large slices. [System dependence graph slicing](/system-dependence-graph-slicing/) of Horwitz, Reps and Binkley keeps the contexts apart.
- **Unstructured jumps.** Weiser's programs had structured statements. With `goto`, `break` and `continue`, deleting statements can change where control goes. Ball and Horwitz (1993) and Agrawal (1994) add the needed jumps to the slice. In the toy IR every jump stays and dropped branches jump to their post-dominator, so the problem does not arise.
- **Dynamic slices.** The same idea on one recorded run gives [dynamic slicing](/dynamic-slicing/), with much smaller slices that hold for one input only.
- **Dead code.** With the outputs of the program as the criterion, the dropped statements are the dead code that [aggressive dead code elimination](/aggressive-dead-code-elimination/) removes.

## When to use it

Use it when one or a few slices are needed and an executable program is wanted, for example to cut a program down for debugging or to extract one computation. It reuses the machinery of a dataflow framework and needs only post-dominators besides. For many slices of the same program, or for forward slices and chops, build the program dependence graph once and use graph reachability.

## Pitfalls

- **Deleting without rerouting.** If a dropped branch is simply removed, control falls into one of its targets, and the slice can run statements the original skipped. The branch must become a jump to its immediate post-dominator, or `ret 0` when that is the exit.
- **Dropping jumps.** A jump writes nothing, so the equations never keep it. Dropping it would join blocks that are not adjacent. Keep every jump, or rebuild control flow as in the variants above.
- **Forgetting the block of $p$.** If line L9 tests only $S$, a criterion inside one arm of a test whose relevant variables are all written before the test loses that test. Then the projection never reaches $p$ and records nothing, while $P$ does. Some statements of the algorithm test $S$ alone; the test of rule 2 of the problem page is needed.
- **Stopping after one round.** One round finds only the data dependences of $V$. The branches that control those statements, and the data that those branches read, come in later rounds.
- **Reading a slice as minimal.** The slice can hold statements that no run needs, because the equations count every path. A smaller slice may exist, and finding the smallest is not computable.
- **Trusting a dependence graph slice to run.** A slice from dependence graph reachability is a set of nodes. It runs only after jumps and block structure are rebuilt as in this algorithm.

## Implementations

## History

Mark Weiser defined program slices in his 1979 PhD thesis at the University of Michigan. His motivation was the way programmers debug: they read backward from a wrong value and keep in mind only the code that can affect it. He presented slices and this algorithm at ICSE 1981 and in IEEE Transactions on Software Engineering in 1984, where he also showed that minimal slices cannot be computed in general. His definitions used the nearest inverse dominator of a branch, which is the immediate post-dominator. In 1984 Ottenstein and Ottenstein showed that the same slices are reachability in the program dependence graph, and the graph method became the common one. Tip's survey of 1995 compares the two methods.

## References
