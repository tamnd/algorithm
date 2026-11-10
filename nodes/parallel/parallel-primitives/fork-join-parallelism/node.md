---
tag: VQN3KY
kind: concept
slug: fork-join-parallelism
name: Fork-join parallelism
aliases:
- spawn and sync
area: parallel/parallel-primitives
level: intro
summary: Split a job into parts, spawn the parts to run in parallel, wait for them at a sync, and combine their results. The pattern behind Cilk, Java ForkJoin and rayon, with its common errors.
prereqs: [divide-and-conquer-paradigm, computation-dag]
see_also: [fork-join-model, work-span-model, work-stealing, task-parallelism, parallel-for, parallel-reduce, determinacy-race, parallel-fibonacci]
sources:
  - paper: "Melvin E. Conway, A multiprocessor system design, AFIPS Fall Joint Computer Conference, 1963"
    locator: the fork and join operations for starting and joining parallel paths of control
  - paper: doi:10.1145/277650.277725
    title: Matteo Frigo, Charles E. Leiserson and Keith H. Randall, The implementation of the Cilk-5 multithreaded language, ACM PLDI, 1998
    locator: Section 2 (spawn and sync in Cilk-5) and Section 3 (the work-first principle)
  - paper: doi:10.1145/337449.337465
    title: Doug Lea, A Java fork/join framework, ACM Java Grande Conference, 2000
    locator: the design of the framework, the task queues and the grain size of tasks
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, 3rd edition, MIT Press, 2009
    locator: Chapter 27, Section 27.1 (spawn, sync, P-FIB, the computation dag and races)
  - book: isbn:9780124159938
    title: Michael McCool, Arch D. Robison and James Reinders, Structured Parallel Programming, Morgan Kaufmann, 2012
    locator: Chapter 8, fork-join (the pattern, recursive splitting and cut-offs)
---

Fork-join parallelism is the most common way to write a parallel divide and conquer. A function splits its job into parts, *spawns* some of the parts so that they may run in parallel with the rest of the function, waits for all of them at a *sync*, and then combines their results. Each spawned part may do the same, so the parallelism nests to any depth. The program says only what *may* run in parallel; a scheduler, usually [work stealing](/work-stealing/), decides what runs where. This page is about the pattern in practice: how to write it, how to choose the size of the parts, and the errors that are easy to make. The cost model, with work, span and the bound for a greedy scheduler, is on the [fork-join model](/fork-join-model/) and [work-span model](/work-span-model/) pages.

Notation on this page: $W$ is the work and $S$ the span. $P$ is the number of processors. The grain size $g$ is the size of a part below which the code runs in sequence.

## In plain words

A teacher has a big pile of tests to mark. She splits the pile in two, gives one half to a helper, and marks the other half herself. Each of them can split their half again and find more helpers.

When she has finished her half, she waits until her helper is done too. Then she puts the two marked halves together.

This works well when the piles are big. If she splits down to single tests, she spends more time giving out work than marking.

It also needs care with shared things. If two people write on one score sheet at the same time, a score can get lost. It is better that each person keeps their own sheet and the sheets are added at the end.

## The idea

**The template.** Each fork-join function has the same four parts.

```pseudo
SOLVE(problem)
    if problem is small then return SOLVE-SEQUENTIALLY(problem)   ▷ the grain size
    split problem into parts p₁, ..., pₘ                           ▷ divide
    for i ← 1 to m - 1 do rᵢ ← spawn SOLVE(pᵢ)                     ▷ fork
    rₘ ← SOLVE(pₘ)                                                 ▷ the parent does the last part itself
    sync                                                           ▷ join: wait for all children of this call
    return COMBINE(r₁, ..., rₘ)                                    ▷ combine
```

**The rules.** A spawned call may run at the same time as the code that follows it in the parent, up to the next sync. A sync waits only for the children that this call has spawned, not for other tasks. Each function ends with an implied sync, so no call returns while its children still run. These rules make each run a series-parallel [computation dag](/computation-dag/): the run splits at each spawn and comes together at each sync. The work is the sum of the costs of all parts, and the span is the length of the [critical path](/critical-path/), so a spawn adds the work of the two branches and takes the larger of their spans.

**Why it is easy to reason about.** Without races, the result of a fork-join program is the same as the result of the program with each spawn and sync deleted. This sequential program is called the *serial elision*, and it can be tested and debugged in the plain way. A greedy scheduler runs the program on $P$ processors in time at most $W/P + S$, so the program is fast when the parallelism $W/S$ is much larger than $P$.

**Grain size.** A spawn costs some tens to some thousands of machine steps, much more than an addition. So the recursion must stop at a part that is large enough to pay for its spawn, and run the base case in sequence. The cut-off changes the work only a little but cuts the number of tasks by a large factor. A good cut-off still leaves a parallelism much larger than $P$, the [parallel slackness](/parallel-slackness/) that the scheduler needs to balance the load.

**The common errors.**

- *Too fine a grain.* Spawning down to single items makes the cost of the spawns the main cost. The fix is a cut-off at the grain size.
- *A race on a shared accumulator.* If both branches do `total ← total + x` on one variable, the two reads can happen before the two writes, and one update is lost. With `total = 0` and the two values 3 and 5, both branches can read 0, and the result is 5 or 3, not 8. This is a [determinacy race](/determinacy-race/). The fix is to have each branch return its own sum and add the sums after the sync, or to use a reducer that the runtime merges.
- *Reading a result before the sync.* The value of a spawned call is not ready until the sync. Code that uses it earlier reads an old value, and it may even pass the tests, because on one processor the child often finishes first.
- *Spawning in a long loop.* A loop that spawns one task per item runs its spawns one after the other, so its span is $\Theta(n)$ even when the tasks are small. A [parallel for](/parallel-for/) splits the range in halves, which gives a span of $\Theta(\log n)$ for the loop control.
- *An unbalanced split.* If one part is much larger than the other, the span stays close to the sequential time. Split into parts of about equal cost, not equal count, when the costs differ.
- *Blocking inside a task.* A task that waits for a lock or for input holds its worker, and the scheduler bound no longer holds. Keep tasks free of waits, other than sync.

## Examples

- **Parallel sum.** Split the array in halves, spawn the sum of the left half, compute the sum of the right half, sync, and add. The work is $\Theta(n)$ and the span $\Theta(\log n)$. This is [parallel reduce](/parallel-reduce/), and it is the safe form of the shared accumulator above.
- **Fibonacci numbers.** The function P-FIB of CLRS spawns $F(n-1)$ and computes $F(n-2)$ in the parent; see [parallel Fibonacci](/parallel-fibonacci/). For $n = 30$ it makes 2692537 calls, about half of them spawns of tiny tasks, and its span is 30 calls. With a cut-off at $n \le 20$, below which the code runs the plain recursion, there are only 287 calls of the parallel function. The span is then 10 spawn levels plus the 21891 calls of one sequential $F(20)$, and the parallelism is still about 123, which is enough for a machine with some tens of cores.
- **Merge sort.** Sort the two halves in parallel, sync, and merge. With a sequential merge the span is $\Theta(n)$, so the merge must be parallel too; [parallel merge](/parallel-merge/) gives [parallel merge sort](/parallel-merge-sort/) a span of $\Theta(\log^3 n)$.
- **Matrix product.** Split each matrix into four blocks and compute the eight block products in parallel; see [parallel matrix multiplication](/parallel-matrix-multiplication/), and [parallel Strassen](/parallel-strassen/) for seven products.
- **Parallel loops.** A [parallel for](/parallel-for/) over $n$ items is itself a fork-join recursion over the index range, with the loop body as the base case.

## Where it is used

- **Cilk and OpenCilk** have the keywords `spawn` and `sync` (`cilk_spawn` and `cilk_sync` in Cilk Plus), and a work stealing runtime (Frigo, Leiserson and Randall 1998).
- **Java** has `ForkJoinPool` and `RecursiveTask`, with `fork` and `join`, after the framework of Lea (2000); parallel streams run on it.
- **Rust** has `rayon::join(a, b)`, which runs two closures and returns both results, and parallel iterators built on it.
- **C++** has `task_group` and `parallel_invoke` in Intel TBB, and **OpenMP** has `#pragma omp task` and `taskwait`.
- **.NET** has the Task Parallel Library, with `Parallel.Invoke` and tasks that are waited for.

The words *fork* and *join* for starting parallel paths of control and waiting for them go back to Conway (1963). The pattern with low cost spawns and provable time bounds came with Cilk in the 1990s.

## References
