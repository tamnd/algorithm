---
tag: J50NFB
kind: concept
slug: data-parallelism
name: Data parallelism
aliases:
- SIMD-style parallelism
- data-parallel programming
- nested data parallelism
area: parallel/parallel-primitives
level: intro
summary: The same operation is applied to many elements at once.
prereqs: [work-span-model]
see_also: [task-parallelism, parallel-map, all-prefix-sums, segmented-scan, parallel-pack, simt-model, simd-within-a-register, mapreduce-model]
sources:
  - paper: doi:10.1145/7902.7903
    title: W. Daniel Hillis and Guy L. Steele Jr., Data parallel algorithms, Communications of the ACM 29(12), 1170 to 1183, 1986
    locator: the opening sections on the data-parallel style of programming, with one processor for each data element, and the algorithms that follow
  - book: isbn:9780262023139
    title: Guy E. Blelloch, Vector Models for Data-Parallel Computing, MIT Press, 1990
    locator: the parallel vector models and their complexity measures, the scan vector model with its primitives, and the flattening of nested parallelism
  - paper: doi:10.1145/227234.227246
    title: Guy E. Blelloch, Programming parallel algorithms, Communications of the ACM 39(3), 85 to 97, 1996
    locator: NESL, nested data parallelism with the apply-to-each construct, its work and depth, and the quicksort example
  - paper: doi:10.1016/0743-7315(90)90087-6
    title: Guy E. Blelloch and Gary W. Sabot, Compiling collection-oriented languages onto massively parallel computers, Journal of Parallel and Distributed Computing 8(2), 119 to 134, 1990
    locator: the flattening transformation, which turns nested parallel operations into flat operations on segmented vectors
  - paper: doi:10.1006/jpdc.1994.1038
    title: Guy E. Blelloch, Jonathan C. Hardwick, Jay Sipelstein, Marco Zagha and Siddhartha Chatterjee, Implementation of a portable nested data-parallel language, Journal of Parallel and Distributed Computing 21(1), 4 to 14, 1994
    locator: the implementation of NESL by flattening to a vector code that runs on several parallel machines
  - paper: doi:10.1109/TC.1972.5009071
    title: Michael J. Flynn, Some computer organizations and their effectiveness, IEEE Transactions on Computers C-21(9), 948 to 960, 1972
    locator: the classes of machines by instruction and data streams, including SIMD
  - paper: doi:10.1145/1248648.1248652
    title: Manuel M. T. Chakravarty, Roman Leshchinskiy, Simon Peyton Jones, Gabriele Keller and Simon Marlow, Data Parallel Haskell, a status report, Proceedings of the 2007 Workshop on Declarative Aspects of Multicore Programming, 10 to 18
    locator: nested data parallelism in Haskell and its flattening
---

Data parallelism is a way to write parallel programs in which the parallelism comes from the data: one operation is applied to all the items of a collection at the same time. The program has one thread of control, and its steps are operations on whole arrays, such as a [map](/parallel-map/), a reduce, a [scan](/all-prefix-sums/), a [pack](/parallel-pack/) or a [permute](/scatter-and-gather/). The amount of parallelism grows with the size of the data, not with the number of tasks in the program. In **nested** data parallelism, the operation applied to each item may itself be data-parallel, which lets the style express divide and conquer and irregular data. NESL (Blelloch) is the main language of this kind, and its cost model of work and depth is the [work-span model](/work-span-model/). Data parallelism is the opposite style to [task parallelism](/task-parallelism/), in which the program names different tasks that run at the same time.

## In plain words

A teacher has to mark 300 tests with the same answer key. She can give each helper some tests, and all helpers do the same job on different papers. That is data parallelism: one job, many pieces of data. The more tests there are, the more helpers can be busy.

Task parallelism is different. In a kitchen, one cook makes the soup, one cuts the bread and one makes the dessert, all at the same time. The jobs are different, and the number of cooks that can be busy depends on the menu, not on the number of guests.

Nested data parallelism lets each helper also split their own job. For example, a helper who marks a long test can give its pages to more helpers.

## The idea

**The model.** A data-parallel program is a sequence of operations on collections, usually arrays. Each operation is defined on the whole collection, and its result does not depend on the order in which the items are processed. The basic operations are:

- elementwise operations: a [map](/parallel-map/), or an "apply-to-each", that applies a function to every item;
- reductions and [scans](/all-prefix-sums/) with an [associative operator](/associative-operator/);
- data movement: [scatter, gather and permute](/scatter-and-gather/), and [pack](/parallel-pack/);
- operations on [segmented](/segmented-scan/) arrays, which hold many sequences in one flat array.

Between two operations there is an implicit barrier, so a program has no races as long as each operation is deterministic. Hillis and Steele (1986) described the style for the Connection Machine, with one virtual processor for each data item. Blelloch (1990) made it a family of machine models, the vector models, in which a program is charged for the number of vector steps and for the total number of element operations. These are the depth and the work of the [work-span model](/work-span-model/).

**Scan as a primitive.** Blelloch's scan vector model adds the scan to the elementwise operations and the permute, at unit cost for each step. He argued that a scan is about as cheap as a memory access on real hardware, and he showed that many algorithms (sorting, graph algorithms, computational geometry) become simple and fast in this model. With a scan, a pack and a split are a constant number of steps.

**Nested data parallelism.** In flat data parallelism, the function in a map must be sequential. In nested data parallelism, it may itself call parallel operations, so the program can apply a parallel function to each item of a sequence of sequences. NESL, designed by Blelloch and colleagues at Carnegie Mellon University in the early 1990s, is built on this idea. Its main construct, the apply-to-each, is written `{f(x) : x in a}`, and it can have a filter, as in `{x in a | x > 0}`. The cost of an apply-to-each is the sum of the work of the calls, and the maximum of their depths plus a constant.

**Flattening.** Hardware runs flat operations, so a nested program must be changed into a flat one. The flattening transformation (Blelloch and Sabot 1990) stores a nested sequence as one flat array of values and a segment descriptor, and it replaces each operation inside an apply-to-each by a segmented operation on the flat array. For example, the sums of all rows of a matrix with rows of different lengths become one segmented reduce. The work and the depth stay within constant factors for most programs, and the load is balanced automatically, because every flat operation works on all the items at once, whatever the lengths of the inner sequences.

**Data parallelism compared with task parallelism.**

| | Data parallelism | [Task parallelism](/task-parallelism/) |
|---|---|---|
| Source of parallelism | the items of a collection | the tasks named in the program |
| Control | one thread of control, collective steps | many threads, or a [fork-join](/fork-join-parallelism/) tree of tasks |
| Parallelism grows with | the size of the data | the structure of the program |
| Synchronization | implicit, between operations | explicit, with sync, join or locks |
| Load balance | by the size of the data; by flattening when nested | at run time, for example by work stealing |
| Typical hardware | SIMD units, GPUs, vector machines | multicore CPUs |

The two styles meet in the middle. A parallel map in a fork-join language is data parallelism built from tasks, and a nested data-parallel program can express divide and conquer, such as quicksort, which is the classic task-parallel pattern.

**Data parallelism and SIMD.** SIMD is a class of hardware, in Flynn's (1972) classes of machines: one instruction stream acts on many data streams. Data parallelism is a programming style. A data-parallel program can run on SIMD units, on the [SIMT](/simt-model/) model of GPUs, on multicore CPUs by cutting the arrays into blocks, or on a cluster. The alias "SIMD-style parallelism" refers to the style, not to the hardware.

## Examples

**Vector addition.** $C = A + B$ for arrays of length $n$ is one elementwise operation: $\Theta(n)$ work and $O(1)$ depth in the vector model.

**Sum of squares.** $\sum_i A[i]^2$ is a map followed by a reduce: $\Theta(n)$ work and $\Theta(\log n)$ depth.

**Sparse matrix-vector product.** In NESL style, with each row a sequence of (column, value) pairs,

```
{ sum({ v * x[j] : (j, v) in row }) : row in A }
```

This is nested: the outer apply-to-each runs over the rows, and the inner one over the nonzeros of a row. Flattening turns it into a gather of the $x_j$, a map that multiplies, and a segmented reduce over the rows, as in [segmented prefix sums](/segmented-prefix-sums/). The work is $\Theta(\text{nonzeros} + \text{rows})$ and the depth is $O(\log n)$, even when the row lengths are very uneven.

**Quicksort.** Blelloch (1996) gives a NESL quicksort of this form:

```
function quicksort(a) =
  if (#a < 2) then a
  else
    let pivot   = a[#a/2];
        lesser  = {e in a | e < pivot};
        equal   = {e in a | e == pivot};
        greater = {e in a | e > pivot};
        result  = {quicksort(v) : v in [lesser, greater]}
    in result[0] ++ equal ++ result[1];
```

The filters are data parallel, and the two recursive calls run in parallel inside one apply-to-each. With a random pivot, the expected work is $O(n \log n)$, and the recursion depth is $O(\log n)$ with high probability. If each filter is a [pack](/parallel-pack/) with depth $O(\log n)$, the depth is $O(\log^2 n)$ with high probability. After flattening, all the calls at one level of the recursion are segments of one array, which is the segmented quicksort of Blelloch (1990).

## Where it is used

- **SIMD instructions.** Compilers turn loops into vector instructions, such as SSE and AVX on x86 or NEON on ARM, when the iterations are independent. See [SIMD within a register](/simd-within-a-register/) for the same idea inside one machine word.
- **GPUs.** A CUDA or OpenCL kernel is one function applied to every index of a grid of threads, which is a data-parallel map; libraries such as Thrust and CUB add reduce, scan, sort and select. See the [SIMT model](/simt-model/).
- **Array languages.** APL, Fortran 90 array statements, High Performance Fortran, and NumPy express programs as whole-array operations.
- **Nested data-parallel languages.** NESL, Data Parallel Haskell (Chakravarty and colleagues, 2007), and the work on flattening in later functional languages.
- **Clusters.** [MapReduce](/mapreduce-model/) and Spark apply the same function to every record of a distributed data set, which is data parallelism at the scale of many machines.
- **Machine learning.** "Data-parallel training" copies a model to every device, gives each device a part of each batch, and combines the gradients with a reduction. The name comes from the same idea: the data is split, and the operation is the same.

## References
