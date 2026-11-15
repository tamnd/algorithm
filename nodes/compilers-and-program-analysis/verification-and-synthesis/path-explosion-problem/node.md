---
tag: ECXME8
kind: concept
slug: path-explosion-problem
name: Path explosion
aliases:
- path explosion problem
area: compilers-and-program-analysis/verification-and-synthesis
level: core
summary: The number of paths of a program grows exponentially with its branches and is unbounded with loops, which limits symbolic execution.
prereqs: [symbolic-execution-tree, path-condition]
see_also: [symbolic-execution, concolic-testing, generational-search, bounded-model-checking, meet-over-all-paths-solution, model-counting, ball-larus-path-profiling, coverage-guided-fuzzing]
sources:
  - paper: doi:10.1145/2254064.2254088
    title: Volodymyr Kuznetsov, Johannes Kinder, Stefan Bucur and George Candea, Efficient state merging in symbolic execution, Proceedings of PLDI 2012
    locator: pp. 193 to 204, the sections on query count estimation and on dynamic state merging
  - paper: doi:10.1145/2568225.2568293
    title: Thanassis Avgerinos, Alexandre Rebert, Sang Kil Cha and David Brumley, Enhancing symbolic execution with veritesting, Proceedings of ICSE 2014
    locator: pp. 1083 to 1094, the sections on veritesting (static symbolic execution of acyclic regions and transition points)
  - paper: doi:10.1145/2408776.2408795
    title: Cristian Cadar and Koushik Sen, Symbolic execution for software testing, three decades later, Communications of the ACM 56(2), 2013
    locator: pp. 82 to 90, the section on the key challenges (path explosion)
  - paper: doi:10.1145/3182657
    title: Roberto Baldoni, Emilio Coppa, Daniele Cono D'Elia, Camil Demetrescu and Irene Finocchi, A survey of symbolic execution techniques, ACM Computing Surveys 51(3), 2018
    locator: Article 50, the sections on path explosion (pruning unrealizable paths, function and loop summarization, path subsumption, state merging and under-constrained execution)
  - url: "https://www.usenix.org/legacy/event/osdi08/tech/full_papers/cadar/cadar.pdf"
    title: Cristian Cadar, Daniel Dunbar and Dawson Engler, KLEE, unassisted and automatic generation of high-coverage tests for complex systems programs, Proceedings of OSDI 2008, USENIX
    locator: pp. 209 to 224, the section on state scheduling (random path selection and coverage-optimized search)
---

Path explosion is the fact that the number of paths of a program grows exponentially with the number of branches in sequence and without bound when a loop depends on the input. Every method that handles one path at a time, such as [symbolic execution](/symbolic-execution/), [concolic testing](/concolic-testing/) and [generational search](/generational-search/), must explore one [path condition](/path-condition/) per leaf of the [symbolic execution tree](/symbolic-execution-tree/), so path explosion is the main limit on their scale. The remedies trade paths for something else: a budget and a search order, larger formulas (state merging and veritesting), or a loss of precision.

## In plain words

Each "if" in a program can send a run one of two ways. Ten tests in a row give up to 1024 different ways through the code, and forty tests give more than a million million. A loop that runs as many times as the input says gives a new way through for each count. A tool that checks the ways through one at a time cannot finish. Most of the ways through do the same thing in the end, so the work is often wasted. Tools cope in three ways. They stop after a budget and pick the most promising ways first. They join two ways that meet again into one, with a more complex description. Or they describe a whole piece of code at once, so that the ways through it are never split.

## The idea

**The count.** Let a loop-free program have $k$ branches in sequence, each on its own input, with the two arms joining before the next branch. Its [control flow graph](/control-flow-graph/) has $3k + 1$ blocks, and all $2^k$ paths are feasible. A loop whose trip count is an input has one path per trip count, so infinitely many. A loop with a fixed trip count $m$ and one input-dependent branch in its body has $2^m$ paths. The number of syntactic paths of a [directed acyclic graph](/directed-acyclic-graph/) can be computed in linear time by dynamic programming over a topological order, even when it is exponential; the [Ball-Larus](/ball-larus-path-profiling/) path numbering uses this. Counting the feasible paths is harder: if each branch tests one Boolean input and the last block checks a CNF formula, the feasible paths that reach the check block are the satisfying assignments, so counting them is [model counting](/model-counting/).

**Why it is not only a weakness of the tools.** A per-path method pays at least one solver query per fork, so its cost is at least the number of leaves of the tree. Some exponential cost is unavoidable in the worst case for any method: reachability of a block in a loop-free program over Boolean inputs is NP-complete, because a program can test a [SAT](/sat/) formula. With loops over unbounded integers, reachability is undecidable (see [path condition](/path-condition/)). So remedies move the cost; they do not remove it.

**Paths are not behaviors.** Many paths compute the same result. Take 8 inputs $x_0, \dots, x_7$ and the code "for each $i$, if $x_i = 120$ then $c \leftarrow c + 1$", followed by "if $c = 5$ then error". The loop has $2^8 = 256$ paths, but $c$ takes only 9 values, 0 to 8. On each path $c$ is a constant, so the last test does not fork. Of the 256 leaves, $\binom{8}{5} = 56$ reach the error. A per-path tool explores 256 states. A tool that merges the two arms of each test keeps one state with the store $c = \sum_i \mathrm{ite}(x_i = 120, 1, 0)$, and asks one query: is $c = 5$ satisfiable? The single query is larger, and a solver must do the case analysis that the tool skipped.

**State merging.** At a join point, two states $(B, \sigma_1, \pi_1)$ and $(B, \sigma_2, \pi_2)$ become $(B, \sigma, \pi_1 \vee \pi_2)$, where $\sigma(x) = \mathrm{ite}(\pi_1, \sigma_1(x), \sigma_2(x))$ for each name on which the stores differ. Merging every join turns symbolic execution of loop-free code into the one-formula encoding of [bounded model checking](/bounded-model-checking/). Merging nothing is plain symbolic execution. Kuznetsov, Kinder, Bucur and Candea (2012) choose in between. *Query count estimation* is a static analysis that estimates, for each variable, how many later solver queries depend on it. Two states are merged only when the variables on which their stores differ are not expected to appear in many later queries, so that the ite terms do not make those queries much harder. *Dynamic state merging* keeps a short history of the recent program points of each state. When a state reaches a point that another state passed a few steps ago, the search gives priority to the state that is behind, so that the two meet at the same point and merge. They built it in KLEE and report large speedups in path coverage on the GNU Coreutils.

**Veritesting.** Avgerinos, Rebert, Cha and Brumley (2014) start in dynamic symbolic execution, one state per path. When a state reaches a branch, they recover the control flow graph of the code that follows, take its acyclic part, and run static symbolic execution on that region: the region becomes one formula with ite terms, as in bounded model checking. At the *transition points* of the region (back edges, calls to code that the static step does not model, system calls, the end of the region) the tool goes back to dynamic symbolic execution, with one state per transition point. Their tool, MergePoint, works on binary programs.

**Other remedies.**

- *A search order and a budget.* KLEE picks the next state by random path selection or by an estimate of new coverage. The order does not change the number of paths; it changes which ones are found before the budget ends.
- *Generational search.* SAGE negates every condition of one long run, so that each expensive run gives many new tests. See [generational search](/generational-search/).
- *Loop bounds.* Unroll each loop a fixed number of times and drop deeper paths. The result is not a proof for the dropped part.
- *Summaries.* Compute pairs of a path condition and a result for a function once, and reuse them at each call.
- *Concretization and fuzzing.* Replace a symbolic value by a concrete one, or let a [fuzzer](/coverage-guided-fuzzing/) cover the easy paths and call the solver only for the hard branches.

## Examples

**Counting paths of the merge example.** The table gives, for the program with $k$ inputs above and the error test $c = 5$, the number of leaves of the tree and the number of leaves that reach the error.

| $k$ | paths | paths to the error | states with merging at each join |
|---|---|---|---|
| 5 | 32 | 1 | 1 |
| 8 | 256 | 56 | 1 |
| 16 | 65536 | 4368 | 1 |
| 32 | 4294967296 | 201376 | 1 |

The second column is $2^k$ and the third is $\binom{k}{5}$. With merging, the price is a formula with $k$ ite terms, and the solver decides it in one call.

**The same problem in a dataflow analysis.** The [meet over all paths](/meet-over-all-paths-solution/) solution of a dataflow problem combines the facts of every path. On a program with loops the paths are infinite in number, and for general monotone frameworks the MOP solution is not computable (Kam and Ullman 1977). Iterative dataflow analysis merges at every join, which is the full state merging of the analysis world; it pays with a loss of precision in place of harder solver calls.

**A loop with an input bound.** In `i = 0; while i < n: i = i + 1`, every value $n = j \ge 1$ is one path, and the tree is infinite (see [symbolic execution tree](/symbolic-execution-tree/)). Each path is cheap; the explosion is in the number of paths. A loop summary that says "at the exit, $i = \max(n, 0)$" replaces the whole family by one formula.

## Where it is used

- **Test generation tools.** KLEE, SAGE and their successors are designed around path explosion: search heuristics, budgets, generational search and state merging all exist because of it.
- **Hybrid fuzzing.** Tools combine a greybox fuzzer with a concolic engine, and call the engine only when the fuzzer stops finding new coverage.
- **Verification by symbolic execution.** A proof by exhaustive symbolic execution is possible only for a finite tree. Path explosion decides whether such a proof is practical. Bounded model checkers and verifiers with invariants avoid the per-path view.
- **Measurement of coverage.** Path coverage is not a practical goal for real code because of path explosion, so tools measure branch or edge coverage instead.

## References
