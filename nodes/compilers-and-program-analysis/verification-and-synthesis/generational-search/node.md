---
tag: WF74QR
kind: algorithm
slug: generational-search
name: Generational search
aliases:
- whitebox fuzzing
- SAGE search
area: compilers-and-program-analysis/verification-and-synthesis
level: advanced
summary: Expands each concolic run by negating every branch condition on its path at once, producing a generation of new inputs to test.
model: word-ram
complexity:
  vars: {R: the number of runs, m: the largest number of recorded conditions on one run, T: the largest number of steps of one run, C: the cost of one solver call}
  time: {worst: O(R (T + m C + log R))}
  space: {extra: O(R T)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2008
  people: [Patrice Godefroid, Michael Y. Levin, David Molnar]
  note: Introduced with the SAGE whitebox fuzzer at NDSS 2008 and used at Microsoft to test file parsers in Windows and Office.
prereqs: [concolic-testing]
see_also: [path-condition, symbolic-execution-tree, path-explosion-problem, coverage-guided-fuzzing, grammar-based-fuzzing, symbolic-execution, breadth-first-search, smt-problem]
sources:
  - url: "https://www.ndss-symposium.org/ndss2008/automated-whitebox-fuzz-testing/"
    title: Patrice Godefroid, Michael Y. Levin and David Molnar, Automated whitebox fuzz testing, Proceedings of NDSS 2008, Internet Society
    locator: the section on generational search (the algorithms Search and ExpandExecution, the bound of each input and the score by incremental block coverage)
  - paper: doi:10.1145/2093548.2093564
    title: Patrice Godefroid, Michael Y. Levin and David Molnar, SAGE, whitebox fuzzing for security testing, Communications of the ACM 55(3), 2012
    locator: pp. 40 to 44, the description of generational search and the results on Windows 7
  - paper: doi:10.1145/1065010.1065036
    title: Patrice Godefroid, Nils Klarlund and Koushik Sen, DART, directed automated random testing, Proceedings of PLDI 2005
    locator: pp. 213 to 223, the depth-first search that generational search replaces
  - paper: doi:10.1145/2408776.2408795
    title: Cristian Cadar and Koushik Sen, Symbolic execution for software testing, three decades later, Communications of the ACM 56(2), 2013
    locator: pp. 82 to 90, the sections on concolic testing and on search heuristics
---

Generational search is the search order of SAGE, the whitebox fuzzer of Godefroid, Levin and Molnar. Like [concolic testing](/concolic-testing/), it runs the program on concrete inputs and records the [path condition](/path-condition/) of each run. Unlike the depth-first search of DART, it negates every condition of a run, not only the deepest open one, and so turns one run into a whole *generation* of new inputs. A *bound* stored with each input stops the search from producing the same path twice, and a score by new code coverage picks the run to expand next. The design fits long runs on large input files, where one symbolic run is expensive and should pay for many new tests.

## In plain words

Run the program on a seed input and write down every test it passes on the way, in terms of the input. A depth-first tool would now flip only the last test. Generational search flips each test in turn: for the first test, find an input that goes the other way there; for the second test, find an input that goes the same way at the first test and the other way at the second; and so on to the end. Each answer is a new input, a child of the seed. Then run all the children, see which ones reach code not seen before, and expand the best one next in the same way. A child does not flip the tests that its parent already handled, so the search never makes the same input path twice.

## The problem

The problem is the one of [concolic testing](/concolic-testing/). The input is a program $P$ of the toy IR with $k$ integer parameters, a set $D \subseteq \mathbb{Z}^k$ of allowed inputs, a seed in $D$ and a solver. The output is a list of tests, one for each path that some input of $D$ follows, or as many as a budget allows.

What is decidable is also the same. A path can have an undecidable condition over unbounded integers with products, and a program can have infinitely many paths (see [path explosion](/path-explosion-problem/)). The algorithm is complete relative to its solver: with a solver that is exact over a finite $D$, it finds every path of $D$ once and stops. On this page $D$ is the box $[-8, 8]^k$ and the solver tries the points of the box. SAGE uses an SMT solver on bit vectors, and in a real use the search stops at a time budget, with no claim about the paths that it did not reach.

## The algorithm

RUN is the concolic run of [concolic testing](/concolic-testing/): it returns the outcome, the blocks visited and the conditions $c_0, \dots, c_{m-1}$, numbered from 0, with the implicit conditions of divisions and shifts. Each run $r$ carries a bound $b(r)$: the search negates only the conditions at positions $b(r)$ and later. SOLVE takes a hint, the input of the parent run, and changes only the inputs that occur in the query, as SAGE does: its new input is the old one with the solved bytes replaced.

```pseudo id=main
GENERATIONAL-SEARCH(P, v0, SOLVE)
L1  r0 <- RUN(P, v0); output r0; covered <- the blocks of r0
L2  W <- {r0}, with b(r0) = 0
L3  while W is not empty do
L4      remove from W the run r with the highest score (the oldest on ties)
L5      let c_0 ... c_(m-1) be the conditions of r
L6      for j <- b(r) to m - 1 do
L7          v' <- SOLVE(c_0 and ... and c_(j-1) and not c_j), with the input of r as the hint
L8          if there is no v' then continue
L9          r' <- RUN(P, v'); output r'
L10         score(r') <- the number of blocks of r' not in covered; add them to covered
L11         b(r') <- j + 1; add r' to W
```

The bound on line L11 is the key. The child $r'$ agrees with $r$ on the positions before $j$ and is opposite at $j$. Flipping $r'$ at a position before $j$ would ask for an input that agrees with $r$ before that position and differs there, which $r$ itself, or one of its other children, already covers. Flipping $r'$ at $j$ would give back the side of $r$. So $r'$ is expanded only at positions $j + 1$ and later.

The score is the number of new blocks that a run covers when it is made, SAGE's measure of incremental coverage. Ties go to the older run. The score changes only the order of the runs; without a budget, the set of runs is the same for every order.

## Example

The parameters are $a$, $b$ and $c$, with the symbols $\alpha$, $\beta$ and $\gamma$. The bug is reached when at least two of the three tests hold. It is a smaller form of the four-byte example of the SAGE paper, in which a counter grows for each byte that has a given value.

```
entry:
  n = 0
  t = a == 7
  br t i1 j1
i1:
  n = n + 1
  jump j1
j1:
  t = b == 5
  br t i2 j2
i2:
  n = n + 1
  jump j2
j2:
  t = c == 3
  br t i3 j3
i3:
  n = n + 1
  jump j3
j3:
  u = 2 <= n
  br u bad ok
bad:
  ret 1
ok:
  ret 0
```

On every path, $n$ is a constant, so the last branch has a constant condition and RUN does not record it. Each run records three conditions, $\alpha = 7$, $\beta = 5$ and $\gamma = 3$, each true or false.

| run | input | parent, flipped position | bound | outcome | score |
|---|---|---|---|---|---|
| 1 | (0, 0, 0) | seed | 0 | ret 0 | 5 |
| 2 | (7, 0, 0) | run 1, position 0 | 1 | ret 0 | 1 (`i1`) |
| 3 | (0, 5, 0) | run 1, position 1 | 2 | ret 0 | 1 (`i2`) |
| 4 | (0, 0, 3) | run 1, position 2 | 3 | ret 0 | 1 (`i3`) |
| 5 | (7, 5, 0) | run 2, position 1 | 2 | ret 1 | 1 (`bad`) |
| 6 | (7, 0, 3) | run 2, position 2 | 3 | ret 1 | 0 |
| 7 | (0, 5, 3) | run 3, position 2 | 3 | ret 1 | 0 |
| 8 | (7, 5, 3) | run 5, position 2 | 3 | ret 1 | 0 |

The seed gives the first generation, runs 2 to 4, from three queries. Run 2 is expanded next, at positions 1 and 2 only, and its first child reaches the bug. Run 4 has bound 3 and three conditions, so it has no children. The search makes 8 runs for the 8 paths, with 7 solver calls that all succeed, and no path appears twice. Each child keeps the inputs of its parent that its query does not mention: run 5 keeps $a = 7$ from run 2.

## Correctness

The full proof is in the proof file. Assume that SOLVE is exact over a finite $D$, the seed is in $D$, and RUN tracks every operation exactly. Let $T_D$ be the tree of the decision sequences of the inputs of $D$, as in the proof for [concolic testing](/concolic-testing/); its leaves are the paths of $D$.

1. **A child follows its query.** The input from line L7 satisfies $c_0, \dots, c_{j-1}, \neg c_j$, so its run records the same first $j$ conditions and then $\neg c_j$.
2. **Descendants keep the prefix.** A run made by flipping position $j$ has bound $j + 1$, and its own children flip at positions $j + 1$ or later. By induction, every descendant of $r'$ agrees with $r'$ at the positions $0$ to $j$.
3. **No path twice.** Take two different runs and their lowest common ancestor $z$ in the tree of parents. If $z$ is one of them, the other one is opposite to $z$ at the position where its chain leaves $z$. Otherwise the two chains leave $z$ by flips at two different positions $j_1 < j_2$; the first run is opposite to $z$ at $j_1$ and the second agrees with $z$ there. In both cases the paths differ.
4. **Every path.** Take a leaf $\ell$ and follow a chain of runs that agree with $\ell$ at all positions below their bound, starting at the seed, whose bound is 0. If the current run $r$ is not $\ell$, let $j$ be the first position where they differ; then $j \ge b(r)$. An input that follows $\ell$ satisfies the query at position $j$, so the exact solver returns a model, and $r$ gets a child that agrees with $\ell$ at the positions 0 to $j$, below its bound $j + 1$. The first difference grows at each step, so after at most $|\ell|$ steps the run is $\ell$.
5. **The end.** Each run is a new leaf and $T_D$ has at most $|D|$ leaves, and each run is expanded once.

Exactly $R - 1$ solver calls succeed, and the total number of calls is $\sum_r (m(r) - b(r))$, where $m(r)$ is the number of conditions of $r$.

## Complexity

Let $R$ be the number of runs, $m$ the largest number of conditions on a run, $T$ the largest number of steps of a run and $C$ the cost of a solver call. Each run is made once at cost $O(T)$ and expanded once with at most $m$ calls. The priority queue costs $O(\log R)$ per run. The total is $O(R (T + m C + \log R))$, the same order as depth-first concolic testing; the difference is the order of the runs, not their number.

The space is larger. The worklist can hold every run made so far, and this implementation keeps the conditions of each, $O(R T)$ in total. SAGE keeps only the input of each run in the worklist, $O(R k)$, and runs the program again symbolically when it expands a run. Depth-first search needs only one stack of $O(m)$ entries.

In SAGE, $m$ is large: a run on a file of thousands of bytes can record many thousands of conditions, and the symbolic run takes much longer than a concrete one. Generational search turns that one symbolic run into up to $m$ new tests.

## Properties

- **Complete relative to the solver, with no repeats.** With exact tracking and an exact solver over a finite $D$, every path of $D$ is found exactly once.
- **The order does not change the result without a budget.** Any choice on line L4 explores the same set of runs. With a budget, the order decides which paths are found, which is why SAGE scores by new coverage.
- **Each symbolic run pays for many tests.** Depth-first search gets one new input per run. Generational search gets up to $m - b(r)$.
- **Children of one run are independent.** The queries of one expansion share nothing but the parent's path condition, so a tool can solve them in parallel and run the children in parallel.
- **No false alarms.** Every test is a real run, so a crash that the search finds is a real crash, as in all concolic methods.

## Variants and improvements

- **Depth-first and breadth-first orders.** The depth-first search of [concolic testing](/concolic-testing/) expands only the deepest open condition and keeps one stack. Generational search with a first-in, first-out worklist instead of the score is a [breadth-first search](/breadth-first-search/) over the generations of the search tree.
- **Query optimizations in SAGE.** The SAGE paper drops the conditions that share no input with the negated one, skips a condition that is already in the path condition, limits how often the conditions of one branch are flipped, and drops a condition of a loop that a later condition of the same branch implies. The solver of this page does the first in a weak form: it changes only the inputs that occur in the query.
- **Grammar-based whitebox fuzzing.** Godefroid, Kiezun and Levin (2008) replace the bytes of the input by the tokens of a grammar, so that the generated inputs pass the parser of the program. See [grammar-based fuzzing](/grammar-based-fuzzing/).
- **Hybrid fuzzing.** A [coverage-guided fuzzer](/coverage-guided-fuzzing/) does the cheap exploration, and a generational expansion of selected inputs gets past the narrow checks such as magic numbers and checksums.

## When to use it

Use generational search for concolic testing of programs whose runs are long and whose inputs are large, such as parsers of file formats, media decoders and network protocol handlers. It suits a fixed time budget, because it spreads the search over the whole tree instead of the deepest corner. For short runs, depth-first concolic testing is simpler and needs less memory. For a proof that a program has no bug, use a verifier instead: whitebox fuzzing proves nothing about the paths that it does not reach.

## Pitfalls

- **The wrong bound.** If a child gets the bound $j$ instead of $j + 1$, it flips position $j$ again, and the solver returns an input of its parent's path. If the bound is too large, paths are lost. With the bound $j + 1$ each path appears once, under the conditions of the proof.
- **Divergence.** A child whose run does not follow its query, because of concretization or calls to code that is not instrumented, can repeat a path or leave a subtree out. The implementation stops with an error; SAGE detects divergences and counts them.
- **Memory.** A worklist of complete runs grows with the number of tests. Store inputs and recompute the conditions.
- **A greedy score.** Scoring by new blocks favors runs that found new code early. A deep bug behind code that is already covered gets a low score and waits. The score helps under a budget; it is not a guarantee.
- **Overflow and the solver.** As in all concolic methods, the solver must use the arithmetic of the machine, or its inputs follow other paths than predicted.

## Implementations

## History

Godefroid, Levin and Molnar presented SAGE and generational search at NDSS 2008. SAGE worked on x86 binaries: it recorded a trace of a run on an input file, executed the trace symbolically to get the path condition, and expanded it with generational search. They designed the search for long runs with thousands of conditions, where the depth-first search of DART spends a whole budget in one small subtree. In their 2012 article in Communications of the ACM they report that SAGE found about one third of the bugs that file fuzzing found during the development of Windows 7. The NDSS paper calls this approach whitebox fuzzing: fuzzing guided by the path condition of each run, in contrast to blackbox fuzzing, which mutates inputs at random.

## References
