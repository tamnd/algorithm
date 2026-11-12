---
tag: 4TQNVH
kind: technique
slug: iterator-model
name: Iterator model (Volcano)
aliases:
- Volcano model
- pull-based execution
- Volcano iterator model
- open-next-close interface
- tuple-at-a-time execution
area: systems/database-algorithms
level: intro
summary: "Run a query plan by giving each operator open, next and close. The root pulls tuples one at a time, so most operators pipeline and need no stored result."
prereqs: [query-plan]
see_also: [query-optimization, hash-join, nested-loop-join, sort-merge-join, hash-aggregation, top-k-query, external-merge-sort, predicate-pushdown]
sources:
  - paper: doi:10.1109/69.273032
    title: Goetz Graefe, Volcano, an extensible and parallel query evaluation system, IEEE Transactions on Knowledge and Data Engineering 6(1) (1994), 120 to 135
    locator: the sections on the iterator interface (open, next and close) and on the exchange operator for parallelism
  - paper: doi:10.1145/152610.152611
    title: Goetz Graefe, Query evaluation techniques for large databases, ACM Computing Surveys 25(2) (1993)
    locator: Section 1 (the architecture of query execution engines and the iterator protocol) and the later sections on sorting, hashing and parallelism
  - url: https://www.cidrdb.org/cidr2005/papers/P19.pdf
    title: Peter Boncz, Marcin Zukowski and Niels Nes, MonetDB/X100, hyper-pipelining query execution, CIDR 2005
    locator: the analysis of tuple-at-a-time interpretation overhead and the vectorized execution model of X100
  - paper: doi:10.14778/2002938.2002940
    title: Thomas Neumann, Efficiently compiling efficient query plans for modern hardware, Proceedings of the VLDB Endowment 4(9) (2011), 539 to 550
    locator: the sections on pipeline breakers, the produce and consume interface, and code generation for each pipeline
  - paper: doi:10.1145/582095.582099
    title: P. Griffiths Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie and T. G. Price, Access path selection in a relational database management system, Proceedings of ACM SIGMOD 1979, 23 to 34
    locator: Section 3, The Research Storage System (scans with OPEN, NEXT and CLOSE), p. 24
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2008)
    locator: Chapter 15 (iterators for the implementation of physical operators)
---

The iterator model runs a [query plan](/query-plan/) by giving every operator the same three calls: `open`, `next` and `close`. The root calls `next` on its children, they call `next` on theirs, and so tuples are pulled up the tree one at a time. Most operators then *pipeline*: they pass each tuple on at once and store no intermediate result. Graefe made the interface the core of the Volcano system, so it is also called the Volcano model.

## In plain words

Think of a line of workers. The last worker wants one finished item, so he asks the worker before him for one. That worker asks the worker before her, and so on, back to the first worker, who takes one raw item from the store. Each worker does her step on the item and hands it forward. No one builds a pile.

In a database, each worker is an operator of the plan: a scan, a filter, a join. Each one knows only how to start, how to give the next row, and how to stop. Because they all speak this same small language, you can plug any operator on top of any other. Some workers cannot hand anything forward until they have seen everything, for example a worker who sorts. They make a pile; the rest do not.

## When it applies

- You have a tree of operators (a physical [query plan](/query-plan/)) and you want one generic driver for every tree, with operators that combine freely.
- The input can be much larger than memory, and you want to avoid writing intermediate results to disk.
- The consumer may stop early: a LIMIT, an EXISTS test, or a cursor that the user closes. Pulling on demand then does only the work that is needed.
- Parallelism is to be added without changes to the operators: Volcano puts an *exchange* operator between two ordinary operators, and it hides the processes and the data partitioning behind the same three calls.

## The template

Each operator implements three calls. The holes are written in capitals.

```pseudo id=main
OPEN(op)
L1  call OPEN on each child of op
L2  INIT-STATE(op)                 ▷ hole: a blocking operator reads its input here
NEXT(op)                           ▷ returns one tuple, or EOF
L3  loop
L4      t ← PRODUCE(op)            ▷ hole: calls NEXT on the children
L5      if t = EOF then return EOF
L6      if ACCEPT(op, t) then return t   ▷ hole: a filter test, or true
CLOSE(op)
L7  free the state of op, then call CLOSE on each child
RUN(root)
L8  OPEN(root)
L9  while (t ← NEXT(root)) ≠ EOF do emit t
L10 CLOSE(root)
```

The state of an operator lives between the calls: a position in a file, the current outer tuple of a join, a hash table. Two instances of the holes:

- **Selection** $\sigma_p$. INIT-STATE does nothing. PRODUCE is NEXT on the child. ACCEPT is $p(t)$. The loop of L3 skips the tuples that fail $p$.
- **Hash join**, build input $B$, probe input $P$, keys $k_B$ and $k_P$. INIT-STATE reads all of $B$ with NEXT and puts each tuple in a hash table under $k_B(t)$; this makes the build side blocking. PRODUCE returns the next pair $(b, p)$ from the list of matches of the current probe tuple $p$; when that list is empty it calls NEXT on $P$ and looks up $k_P(p)$. ACCEPT is true.

**Pipelined and blocking operators.** An operator is *pipelined* if it can return its first tuple after it reads a bounded number of input tuples: selection, projection with duplicates, the probe side of a hash join, the outer side of a nested-loop join, LIMIT. An operator is *blocking* if it must read all of an input first: sort, [hash aggregation](/hash-aggregation/), the build side of a [hash join](/hash-join/), duplicate elimination by sorting. A blocking operator cuts the plan into *pipelines*; the tuples of one pipeline flow without storage, and the blocking operator holds the boundary in memory or in a temporary file.

**Cost of the interface.** Each tuple that passes through an operator costs at least one call of NEXT on that operator. If $N$ tuples flow through a pipeline of $d$ operators, the interface costs $\Theta(N d)$ calls, in addition to the work of the operators. Each call is a virtual function call or a call through a pointer, which a compiler cannot inline. On disk-bound systems this cost hides behind the I/O. On data in memory it dominates, and this is the reason for the vectorized and compiled variants below.

## Classic examples

- **Selection and projection.** The simplest pipelined operators: each NEXT pulls until a tuple passes the test, and projection maps each tuple. [Predicate pushdown](/predicate-pushdown/) moves selections down so that fewer tuples flow through the joins.
- **[Nested-loop join](/nested-loop-join/).** The outer input is pulled once. For each outer tuple, the operator calls CLOSE and then OPEN on the inner input and pulls it again from the start. The inner input must therefore support a rescan, and a costly inner subplan runs once for each outer tuple, unless it is stored first.
- **[Hash join](/hash-join/).** Blocking on the build input, pipelined on the probe input. A chain of hash joins whose build inputs are all base relations streams the probe input through every hash table.
- **[Sort-merge join](/sort-merge-join/) and [external merge sort](/external-merge-sort/).** The sort is blocking. OPEN of the sort creates the sorted runs on disk, and NEXT returns tuples from the final merge, so the last merge pass pipelines into the merge join above it.
- **[Hash aggregation](/hash-aggregation/).** Blocking: no group is complete until all input is read. Aggregation over input already sorted on the grouping columns can pipeline: a group is complete when the key changes.
- **[Top-k](/top-k-query/) and LIMIT.** LIMIT $k$ stops pulling after $k$ tuples, so a pipeline below it does only the work for those $k$ tuples. Above a sort it saves nothing in the input, because the sort has read everything.

**A trace with numbers.** Take a scan of 1000 tuples $(0), (1), \ldots, (999)$, a filter "value divisible by 10", and LIMIT 3 at the root. The root calls NEXT three times and gets $(0), (10), (20)$. The fourth call returns EOF without a call to the child. So the scan returns only 21 tuples, not 1000. Put a sort on the value, descending, in place of the filter, with LIMIT 1: the answer is $(999)$, but the scan returns all 1000 tuples, because OPEN of the sort reads its whole input. For a hash join with a build input of 50 tuples, a probe input of 500 tuples and LIMIT 2, the build scan returns all 50 tuples and the probe scan returns only 2.

## Variations

- **Vectorized execution.** NEXT returns a *batch* (a vector) of values of each column instead of one tuple, for example about a thousand at a time. The cost of the interface is paid once per batch, and the operator works in a tight loop over arrays that the compiler and the CPU handle well. Boncz, Zukowski and Nes introduced this design in MonetDB/X100 (2005), after they measured that tuple-at-a-time interpretation used the CPU poorly.
- **Compiled, push-based execution.** Neumann (2011) turns the plan inside out: each pipeline becomes one loop that reads tuples from its source and *pushes* each one through all operators of the pipeline, until a pipeline breaker (a blocking operator) stores it. The operators generate code through two calls, *produce* and *consume*, and the generated code keeps the tuple in CPU registers across operators.
- **Exchange.** Volcano adds parallelism with one more operator. Exchange runs its subtree in other processes, partitions or merges the streams, and offers OPEN, NEXT and CLOSE to its parent, so no other operator changes.
- **Materialization of a subplan.** A spool operator stores the result of its child on the first pass and replays it on rescans. This fixes the cost of a rescanned inner subplan of a nested-loop join.
- **Python generators.** In a language with generators or coroutines, each operator is a generator that pulls from the generators of its children. This is the same model with the state kept in the suspended frame.

## Pitfalls

- **Rescans of a costly inner input.** A [nested-loop join](/nested-loop-join/) re-opens its inner child for each outer tuple. If the inner child is a sort or a join, all of that work repeats. Put a materialization or an index on the inner side.
- **Hidden blocking.** A LIMIT does not make a plan cheap if a sort or an aggregation sits below it. Look for the pipeline breakers when you estimate the time to the first row.
- **Missing CLOSE.** An operator that stops early must still call CLOSE on its children, so that they free buffers, temporary files and locks. A LIMIT that returns EOF must not forget the subtree below it.
- **State that OPEN does not reset.** OPEN must reset all of the state, because a parent can open a child many times. A scan that does not rewind its position returns nothing on the second pass of a nested-loop join.
- **Too much per-tuple work.** On data in memory, the calls themselves can cost more than the work. Measure before you blame an operator, and use batches.

## Exercises

1. Write NEXT for a merge join of two inputs sorted on the join key, with duplicate keys on both sides. Which state must the operator keep between calls, and which input must it be able to reposition?
2. A plan is $\sigma_p(R) \bowtie_{NL} \text{Sort}(S)$, with the sort as the inner input. Count the number of times $S$ is sorted when $\sigma_p(R)$ has $m$ tuples, and change the plan so that it is sorted once.
3. A pipeline of $d$ pipelined operators processes $N$ tuples, and the filter at the bottom passes a fraction $f$ of them. Count the calls of NEXT, as a function of $N$, $d$ and $f$, in the tuple-at-a-time model and in a vectorized model with batches of $b$ tuples.
4. Show that HashJoin, as written in the template, returns the same multiset as a nested-loop equijoin of the same two inputs.

## References
