---
tag: 1V18D7
kind: algorithm
slug: dynamic-slicing
name: Dynamic slicing
aliases:
- Korel-Laski dynamic slice
- Agrawal-Horgan dynamic slicing
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: advanced
summary: Finds the statements that affected a value in one execution, from a trace of the dependences that actually occurred.
solves: [program-slicing]
model: word-ram
complexity:
  vars: {T: the number of statement instances the run executes, n: the number of statements, v: the number of names, b: the number of blocks}
  time: {worst: O(T n)}
  space: {extra: O((v + b) n)}
properties: {deterministic: true, recursive: false, online: true, executable_result: false}
history:
  year: 1988
  people: [Bogdan Korel, Janusz Laski]
  note: Korel and Laski defined the slice of one run, for debugging, and asked that it run on the same input along the same path; Agrawal and Horgan (1990) computed it from dependence graphs of the run.
prereqs: [program-slicing, pdg-slicing, control-dependence]
see_also: [weiser-slicing, system-dependence-graph-slicing, post-dominance, reaching-definitions, taint-analysis, delta-debugging, concolic-testing, binary-decision-diagram]
sources:
  - paper: doi:10.1016/0020-0190(88)90054-3
    title: Bogdan Korel and Janusz Laski, Dynamic program slicing, Information Processing Letters 29(3), 1988, pages 155-163
    locator: the dynamic slicing criterion (input, statement occurrence, variables) and slices that must run along the projected path
  - paper: doi:10.1145/93542.93576
    title: Hiralal Agrawal and Joseph R. Horgan, Dynamic program slicing, Proceedings of the ACM SIGPLAN 1990 Conference on Programming Language Design and Implementation, ACM SIGPLAN Notices 25(6), 1990, pages 246-256
    locator: four methods, from marking the static graph to the dynamic dependence graph and its reduced form
  - paper: doi:10.1145/186258.186514
    title: Bogdan Korel and Satish Yalamanchili, Forward computation of dynamic program slices, Proceedings of the 1994 ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA '94), 1994, pages 66-79
    locator: computing executable dynamic slices during the run, without keeping the trace
  - paper: doi:10.1109/ICSE.2004.1317472
    title: Xiangyu Zhang, Rajiv Gupta and Youtao Zhang, Efficient forward computation of dynamic slices using reduced ordered binary decision diagrams, Proceedings of the 26th International Conference on Software Engineering (ICSE 2004), pages 502-511
    locator: one slice set per name kept during the run, stored as shared BDDs
  - paper: doi:10.1145/1273463.1273489
    title: Bin Xin and Xiangyu Zhang, Efficient online detection of dynamic control dependence, Proceedings of the 2007 International Symposium on Software Testing and Analysis (ISSTA '07), pages 185-195
    locator: dynamic control dependence found online with a stack keyed by immediate post-dominators
  - paper: "Frank Tip, A survey of program slicing techniques, Journal of Programming Languages 3(3), 1995, pages 121-189"
    locator: the section on dynamic slicing, which compares the executable slices of Korel and Laski with the graph methods of Agrawal and Horgan
---

Dynamic slicing solves the [program slicing](/program-slicing/) problem for one run instead of all runs. The criterion names an input, a statement, which visit of that statement, and some variables. The answer is the set of statements whose executions in that run affected those values, through the data and control dependences that the run really had. Korel and Laski (1988) defined it for debugging. A static slice must cover every input and every path, so it keeps statements that this run never used; a dynamic slice drops them and is often much smaller. The price is that **a dynamic slice holds for its one input only.**

## In plain words

Run the program once and watch. Each time a statement runs, write down which earlier steps it used: the step that last set each variable it reads, and the test that decided it would run at all. Each variable keeps a list of the statements its current value came from. When a statement runs, its list is the union of the lists of what it read, plus itself. When the run reaches the place you care about, the lists of the variables you care about are the answer. A statement that ran a thousand times but never fed those values is not in the answer. A statement that did not run at all is never in it.

## The problem

Programs are in the toy IR, with `x = k`, `x = y`, `x = a op b`, `jump`, `br` and `ret`, and every block reaches a `ret`. A statement is an instruction or a block terminator. A *dynamic criterion* is $\langle I, p, q, V \rangle$: an input $I$, a statement $p$, a count $q$, and names $V$. It asks for the values of $V$ just before the $q$-th time the run on $I$ reaches $p$.

The run is a sequence of *instances*: executions of statements. Instance $k$ has two kinds of parents.

- **Dynamic data dependence.** For each name $y$ that $k$ reads, the last earlier instance that wrote $y$.
- **Dynamic control dependence.** The most recent earlier branch instance $j$, in a block $X$, such that the run has not entered the block $\mathrm{ipdom}(X)$ since $j$. The [immediate post-dominator](/post-dominance/) of $X$ is where the two arms of the branch join, so $k$ is still inside the region that $j$ decided.

The *dynamic slice* is the set of statements of all instances that reach the criterion by parent links. This is the slice of Agrawal and Horgan (1990), a set of statements. Korel and Laski (1988) also asked the slice to be a program that runs on $I$ along the same path, which can force more statements in.

## The algorithm

The method runs forward and keeps no trace. $DS[x]$ is the set of statements that the current value of $x$ depends on, the statement that wrote it included. $O$ is a list of the open branch instances, at most one per block, each with its own set.

```pseudo id=main
DYNAMIC-SLICE(P, I, p, q, V)
L1  DS[x] <- empty for every name x; O <- empty list; start the run of P on I
L2  for each statement instance s, in the order of the run do
L3      C <- the set of the last entry of O, or empty if O is empty
L4      if s is at p and the run reaches p for the q-th time then
L5          return C ∪ (the union of DS[x] over x in V)
L6      T <- {s} ∪ C ∪ (the union of DS[y] over the names y that s reads)
L7      if s writes x then DS[x] <- T
L8      if s is the branch of block X then remove the entry of X from O; append (X, ipdom(X), T) to O
L9      if s ends a block and the run goes to block Y then remove from O each entry whose ipdom is Y
    return none, because the run stopped before the q-th visit to p
```

Line L3 finds the dynamic control parent: the last open entry. Lines L8 and L9 keep the list right. An entry closes when the run enters its ipdom block. An older instance of the same block closes together with the newer one, so it can never again be the latest open entry, and line L8 drops it. This is the stack of Xin and Zhang (2007), and it keeps $O$ no longer than the number of blocks.

In the implementation, `dynamic_slice` is lines L1 to L9 and runs the program itself. The parameters start with an empty set, since no statement wrote them.

## Example

The program counts $i$ from 0 to $n - 1$ and adds $i$ to $s$ only when $i = k$. The variable $p$ is never used for $s$.

```
# params: n, k
B0:
  i = 0
  s = 0
  p = 1
  jump B1
B1:
  c = i < n
  br c B2 B5
B2:
  d = i == k
  br d B3 B4
B3:
  s = s + i
  jump B4
B4:
  p = p * 2
  i = i + 1
  jump B1
B5:
  ret s
```

The criterion is $s$ just before `ret s`, at its first visit.

**Static slice.** Every definition of $s$ can reach `ret s`, so the static slice is the 8 statements `i = 0`, `s = 0`, `c = i < n`, `br c`, `d = i == k`, `br d`, `s = s + i` and `i = i + 1`.

**Input $n = 3$, $k = 5$.** The loop runs 3 times and `s = s + i` never runs. The sets as the run goes:

| instance | what happens |
|---|---|
| `i = 0` | $DS[i] = \{$`i = 0`$\}$ |
| `s = 0` | $DS[s] = \{$`s = 0`$\}$ |
| `c = i < n` | $DS[c] = \{$`c = i < n`, `i = 0`$\}$ |
| `br c` to B2 | open entry (B1, ipdom B5) with the set $DS[c] \cup \{$`br c`$\}$ |
| `d = i == k` | gets the open set, $DS[i]$ and itself |
| `br d` to B4 | its entry (B2, ipdom B4) closes at once, because the run enters B4 |
| `i = i + 1` | $DS[i]$ now also holds `br c` and `c = i < n` |
| two more trips, then `br c` to B5 | entering B5 closes the B1 entry |

At `ret s` the open list is empty and $DS[s]$ is still $\{$`s = 0`$\}$. **The dynamic slice is the single statement `s = 0`**, against 8 in the static slice. The loop ran, but nothing in it reached $s$.

**Input $n = 3$, $k = 1$.** Now `s = s + i` runs once, at $i = 1$. Its set holds `s = 0`, the set of $i$ (written by `i = i + 1` in the first trip, which holds `i = 0`), and the set of the open `br d`, which holds `d = i == k`, the open `br c` and `c = i < n`. The dynamic slice is all 8 statements of the static slice.

**For one input only.** The slice $\{$`s = 0`$\}$ of the first input is wrong for the second: on $n = 3$, $k = 1$ the value of $s$ comes from `s = s + i`, which is not in it.

## Correctness

The full proof is in the proof file. Its steps:

1. **The open list.** Before each instance, the list holds the open branch instances that are the latest of their block, in time order. An older instance of a block is open only while the newer one is, so the last entry is the dynamic control parent.
2. **The sets.** Before each instance, $DS[x]$ is the set of statements reachable by parent links from the last writer of $x$. The step for line L6 is the recursion: the closure of an instance is the instance plus the closures of its parents.
3. **The answer.** Line L5 returns the union of the closures of the parents of the criterion instance, which is the dynamic slice by definition.
4. **The slice holds for its input.** Run again on the same input, force every branch the way it went, and let every statement outside the slice write any value at all. The values of $V$ at the criterion do not change. The proof is induction over the instances in the closure: each one is a statement of the slice, and it reads values written by instances in the closure.

## Complexity

**Proved, for the method here.** The loop runs once per instance, $T$ times. Each set holds at most $n$ statements and a statement reads at most two names, so line L6 costs $O(n)$. The open list has at most one entry per block, so lines L8 and L9 cost $O(b)$ with $b \le n$. The time is $O(T n)$. The space is one set per name and one per open entry, $O((v + b) n)$, independent of the length of the run.

**Compared.** The dynamic dependence graph of Agrawal and Horgan has one node per instance, so it takes $O(T)$ space, and a slice is a backward search in it, linear in its size; once built, it answers any criterion of the run. The forward method answers one criterion, or all names at once, without storing the run. Zhang, Gupta and Zhang (2004) keep the sets as shared binary decision diagrams to cut the cost of the unions.

## Properties

- **Holds for one input only.** The guarantee is for the input of the criterion and its path. For another input the dependences are different instances, and the slice can miss statements.
- **Inside the static slice.** Each dynamic dependence is also a static one, so the dynamic slice is a subset of the [PDG slice](/pdg-slicing/) for the same point and names. It is often much smaller, as in the example.
- **Exact dependences.** The run knows which branch went which way and which definition was the last one. With pointers and arrays, it also knows the exact address read, which static analysis can only approximate.
- **Not a program.** The result is a set of statements. If a statement of the slice runs several times, other instances of it may read values from statements outside the slice and change the path. Korel and Laski add statements to make the slice run; their slices can be larger.
- **Not minimal.** A dependence counts even when it does not change the value, for example `x = y - y` depends on `y`.

## Variants and improvements

- **Korel and Laski (1988).** The slice must be a program that, run on the same input, follows the projection of the original path. If one instance of a statement is needed, all are, and more statements join to keep the path.
- **Agrawal and Horgan (1990).** Four methods: mark the nodes of the static graph that ran; mark the edges that ran (both give slices that can be too large); build the full dynamic dependence graph, one node per instance; and the reduced dynamic dependence graph, which adds a node only when a new slice set appears.
- **Forward methods.** Korel and Yalamanchili (1994) compute executable slices during the run. Zhang, Gupta and Zhang (2004) keep one set per name, as here, stored in [binary decision diagrams](/binary-decision-diagram/).
- **Relevant slicing.** Adds statements that did not run but could have changed the value had a branch gone the other way. This catches bugs of omission, such as a missing assignment in the arm that was skipped.
- **Interprocedural runs.** Calls and returns need one control stack per frame. Xin and Zhang (2007) handle this online, and irregular control flow too.
- **Between static and dynamic.** Conditioned slicing fixes a predicate on the inputs instead of one input.

## When to use it

Use it to debug one failing run: start from the wrong value and read only the statements that produced it. It also serves fault localization over test suites, explaining a value seen in a log, and cutting down a run before [delta debugging](/delta-debugging/). When the slice must hold for all inputs, as for program understanding or refactoring, use a static slice. To follow untrusted data forward through runs, use [taint analysis](/taint-analysis/) instead. When the cost of tracing is too high, a static slice of the failing path is a cheaper middle ground.

## Pitfalls

- **Reusing a slice for another input.** The slice of one input says nothing about other inputs. In the example, the slice of $n = 3$, $k = 5$ is one statement, and it is wrong for $k = 1$.
- **Taking the most recent branch as the control parent.** A branch whose arms have joined no longer controls anything. Without the ipdom check, every statement after an `if` depends on it.
- **Keeping old instances of a loop test on the control stack.** Without line L8, every trip of a loop pushes one more entry and the stack grows with the run.
- **Expecting the set to run.** A statement in the slice can run again with inputs that the slice does not compute and take another path. For a runnable slice, use the method of Korel and Laski.
- **Missing omission bugs.** A statement that did not run is never in the slice, even when the bug is that it did not run. Relevant slicing addresses this.
- **Storing the whole trace.** It grows with the run. Forward methods or compact graphs keep memory bounded by the program instead.

## Implementations

## History

Weiser's slices (1979 to 1984) were static. Korel and Laski (1988) defined the dynamic slice in Information Processing Letters, for debugging, as a program that keeps the behavior of one run. Agrawal and Horgan (PLDI 1990) recast it as the statements reached in dependence graphs of the run, compared four ways to compute it, and introduced the reduced dynamic dependence graph. Korel and Yalamanchili (1994) computed slices forward during the run. Tip's survey (1995) compared the definitions. Zhang, Gupta and Zhang made forward slicing practical on large runs in 2004, with binary decision diagrams, and Xin and Zhang (2007) gave an online method for dynamic control dependence that also covers calls and irregular control flow.

## References
