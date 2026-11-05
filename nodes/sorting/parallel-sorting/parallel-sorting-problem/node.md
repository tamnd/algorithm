---
tag: 7MNFD9
kind: problem
slug: parallel-sorting-problem
name: Parallel sorting problem
aliases:
- parallel sort
area: sorting/parallel-sorting
level: intro
summary: Sort n keys using many processors, minimizing parallel time and total work.
prereqs: [sorting-problem, pram-model, work-span-model]
see_also: [parallel-merging-problem, parallel-merge-sort, sample-sort, cole-merge-sort, parallel-sorting-depth-lower-bound, mesh-sorting-problem, sorting-network, distributed-sorting]
sources:
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 4, Searching, merging and sorting (PRAM algorithms and the lower bounds for comparison problems)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 26, Parallel Algorithms (the work-span model, the work law, the span law, greedy scheduling, and Section 26.3, parallel merge sort)
  - book: isbn:9780201648652
    title: Ananth Grama, Anshul Gupta, George Karypis and Vipin Kumar, Introduction to Parallel Computing, second edition, Addison-Wesley, 2003
    locator: Chapter 9, Sorting (sorting networks, odd-even transposition, parallel quicksort, bucket and sample sort, radix sort)
  - paper: doi:10.1137/0217049
    title: Richard Cole, Parallel merge sort, SIAM Journal on Computing 17(4), 1988
    locator: the main theorem, sorting n keys in O(log n) time with n processors on the CREW and the EREW PRAM
  - paper: doi:10.1137/0204030
    title: Leslie G. Valiant, Parallelism in comparison problems, SIAM Journal on Computing 4(3), 1975
    locator: the parallel comparison model, in which only the comparisons are counted
  - paper: doi:10.1137/0215006
    title: Stephen Cook, Cynthia Dwork and Ruediger Reischuk, Upper and lower time bounds for parallel random access machines without simultaneous writes, SIAM Journal on Computing 15(1), 1986
    locator: pp. 87 to 97, the lower bound of Omega(log n) steps for the OR of n bits on a CREW PRAM
  - paper: doi:10.1145/65950.65958
    title: Paul Beame and Johan Hastad, Optimal bounds for decision problems on the CRCW PRAM, Journal of the ACM 36(3), 1989
    locator: pp. 643 to 670, the lower bound of Omega(log n / log log n) steps for parity with a polynomial number of processors
---

The parallel sorting problem asks to put $n$ keys in non-decreasing order with many processors that work at the same time. It is the [sorting problem](/sorting-problem/) with a second cost: besides the total work, the algorithm must make the parallel time short. The answer depends on the machine, so each bound names a model: a [PRAM](/pram-model/) variant, the [work-span model](/work-span-model/), the [BSP model](/bsp-model/), a [sorting network](/sorting-network/) or a fixed processor network such as a mesh.

## In plain words

You have a big pile of exam papers to put in order by student number, and ten friends to help. One person alone needs a long time. If each friend sorts a part of the pile, the parts must still be combined, and the combining is the hard part. Friends who wait for each other do no useful work.

So a parallel sort is judged by two numbers. The first is how long you wait until the pile is in order. The second is how much effort all the helpers spend in total. A good method makes the wait short and does not waste much more effort than one careful person would spend. How well this works depends on how the helpers can talk: all at one table, by passing papers to a neighbour, or by sending parcels in rounds.

## Definition

**Input.** A sequence $x_0, \ldots, x_{n-1}$ of keys from a total order, placed in the shared memory of a PRAM, or spread over the $p$ processors of a distributed machine with about $n/p$ keys on each.

**Output.** The same keys in non-decreasing order. On a shared-memory machine the output is an array. On a distributed machine the output is a sorted sequence cut into consecutive pieces, with piece $i$ on processor $i$ (or on the processor that has index $i$ in a fixed order, such as the snake order of a mesh).

**Costs.** Each model has its own measures.

- **PRAM with $p$ processors** ([EREW](/erew-pram/), [CREW](/crew-pram/) or [CRCW](/crcw-pram/)): the number of synchronous steps $T_p(n)$, and the work $p \cdot T_p(n)$ or the number of operations done.
- **Work-span model**: the work $T_1(n)$, the number of operations of the computation, and the span $T_\infty(n)$, the length of a longest chain of operations that must run one after another. By [Brent's theorem](/brent-theorem/) a greedy scheduler on $p$ processors then needs at most $T_1/p + T_\infty$ steps.
- **Parallel comparison model**: the number of rounds, where each of $p$ processors makes one comparison per round and all other computation is free.
- **Comparator network**: the [depth](/network-depth/), the number of layers of [comparators](/comparator/), and the [size](/network-size/), the number of comparators.
- **BSP model**: the number of supersteps, the local work per superstep, and the largest number of words that one processor sends or receives in one superstep.
- **Fixed network** (linear array, mesh, hypercube): the number of steps, when in each step each link carries one key.

A parallel algorithm is **work-efficient** when its work is within a constant factor of the best sequential time, which is $\Theta(n \log n)$ for a comparison sort. See [work efficiency](/work-efficiency/).

## Variants

- **Comparison sorting.** Only comparisons of keys are allowed. This is the usual case, and the case of all the lower bounds below.
- **Integer sorting.** The keys are integers of $b$ bits, and the algorithm may use them as addresses. [Parallel radix sort](/parallel-radix-sort/) is in this class.
- **Oblivious sorting.** The sequence of compare-exchange operations is fixed in advance and does not depend on the keys. These are the [sorting networks](/sorting-network/), [odd-even transposition sort](/odd-even-transposition-sort/), [shearsort](/shearsort/) and [columnsort](/columnsort/).
- **Sorting on a processor network.** Each processor holds one key, or a block of keys, and only neighbours can exchange keys. The [mesh sorting problem](/mesh-sorting-problem/) is the main case.
- **Distributed and external sorting.** The keys do not fit in one memory. See [distributed sorting](/distributed-sorting/) and [external merge sort](/external-merge-sort/).
- **Stable parallel sorting.** Equal keys must keep their input order. Many fast parallel sorts are not stable, so the key is often extended with its input index.

## Examples

**One input on three machines.** Take the 8 keys $[6, 3, 8, 1, 7, 2, 5, 4]$.

- On a linear array of 8 processors, odd-even transposition sort finishes in 8 rounds of neighbour compare-exchange. It makes $8 \cdot 7/2 = 28$ comparisons.
- Batcher's [bitonic sort](/bitonic-sort/) is a network of 24 comparators in 6 layers. Any network for 8 keys needs at least $\lceil \lg 8 \rceil = 3$ layers, because each output depends on all 8 inputs, and at least $\lceil 16/4 \rceil = 4$ layers, because a layer has at most 4 comparators and the network needs at least $\lceil \lg 8! \rceil = 16$ comparators.
- With 4 processors on a PRAM, each processor can sort 2 keys, and two rounds of parallel merging combine the 4 sorted pairs.

**Lower bounds in numbers.** The table gives $\lg n!$, the least number of comparisons of a comparison sort in the worst case, and two lower bounds on the parallel time.

| $n$ | $\lceil \lg n! \rceil$ | rounds with $n$ comparisons each, $\lceil \lg n! / n \rceil$ | network depth, $\lceil \lg n \rceil$ | network depth, $\lceil \lg n! / \lfloor n/2 \rfloor \rceil$ |
| --- | --- | --- | --- | --- |
| 8 | 16 | 2 | 3 | 4 |
| 1024 | 8770 | 9 | 10 | 18 |
| $2^{20}$ | 19458756 | 19 | 20 | 38 |

So even with a million processors, a comparison sort of a million keys needs about 20 parallel steps.

## Known algorithms

The table names the model of each bound. Here $n$ is the number of keys and $p$ the number of processors.

| algorithm | model | time or span | work |
| --- | --- | --- | --- |
| [Odd-even transposition sort](/odd-even-transposition-sort/) | linear array, $n$ processors | $n$ rounds | $\Theta(n^2)$ comparisons |
| [Bitonic sort](/bitonic-sort/), [odd-even merge sort](/odd-even-merge-sort/) | comparator network | depth $\Theta(\log^2 n)$ | size $\Theta(n \log^2 n)$ |
| [AKS network](/aks-sorting-network/) | comparator network | depth $O(\log n)$ | size $O(n \log n)$ |
| [Parallel merge sort](/parallel-merge-sort/) | work-span | span $\Theta(\log^3 n)$, or $\Theta(\log^2 n)$ with a faster merge | $\Theta(n \log n)$ |
| [Parallel quicksort](/parallel-quicksort/) | work-span, randomized | span $O(\log^2 n)$ w.h.p. | $O(n \log n)$ expected |
| [Cole's merge sort](/cole-merge-sort/) | EREW PRAM, $n$ processors | $O(\log n)$ | $O(n \log n)$ |
| [Sample sort](/sample-sort/), [regular sampling](/parallel-sorting-by-regular-sampling/) | BSP or message passing, $p$ processors | $O(1)$ supersteps | $O(n \log n)$ |
| [Parallel radix sort](/parallel-radix-sort/) | work-span, $b$-bit integer keys | $O(b \log n)$ with 1-bit digits | $O(bn)$ |
| [Shearsort](/shearsort/) | $\sqrt n \times \sqrt n$ mesh | $\sqrt n (\lg n + 1)$ steps | |

## Bounds

**Work.** A parallel comparison sort makes at least $\lceil \lg n! \rceil = n \lg n - \Theta(n)$ comparisons in the worst case, because it is also a sequential comparison sort, and the [comparison sort lower bound](/comparison-sort-lower-bound/) applies. So the work is $\Omega(n \log n)$ in each model that counts comparisons.

**Time.** The [parallel sorting depth lower bound](/parallel-sorting-depth-lower-bound/) collects the lower bounds on the time.

- In a network of gates of fan-in 2, each output depends on all $n$ inputs, so the depth is at least $\lceil \lg n \rceil$.
- In the parallel comparison model with $p$ comparisons per round, $r$ rounds have at most $2^{pr}$ outcomes, so $r \ge \lg n! / p$. With $p = O(n)$ this is $\Omega(\log n)$.
- On a CREW PRAM, sorting needs $\Omega(\log n)$ steps with any number of processors, by the bound of Cook, Dwork and Reischuk for the OR of $n$ bits.
- On a CRCW PRAM with a polynomial number of processors, sorting needs $\Omega(\log n / \log \log n)$ steps, by the bound of Beame and Hastad for parity.
- On a $\sqrt n \times \sqrt n$ mesh, a key may have to move from one corner to the other, so sorting needs at least $2\sqrt n - 2$ steps. See the [mesh sorting problem](/mesh-sorting-problem/).

**Matching upper bounds.** The AKS network and Cole's merge sort reach $O(\log n)$ time with $O(n \log n)$ work, so on the EREW PRAM with $n$ processors sorting takes $\Theta(\log n)$ time. Both have large constant factors, and in practice sorts with span $O(\log^2 n)$ or with a constant number of BSP supersteps are used.

## Reductions

- **Sorting to merging.** A merge sort does $\lceil \lg n \rceil$ levels of merges, so a merge with span $S(n)$ and linear work gives a sort with span $O(S(n) \log n)$ and work $O(n \log n)$. See the [parallel merging problem](/parallel-merging-problem/).
- **Sorting to prefix sums.** Counting and placing keys by digit, as in [parallel radix sort](/parallel-radix-sort/), uses the [all-prefix-sums](/all-prefix-sums/) operation.
- **OR and parity to sorting.** The largest output of a sort of $n$ bits is their OR, and on a CRCW PRAM the number of ones of a sorted bit array can be read in $O(1)$ steps with $n$ processors. These reductions carry the lower bounds for OR and parity to sorting.
- **Sorting to selection of splitters.** [Sample sort](/sample-sort/) reduces one large sort to many small independent sorts, with a few splitters chosen from a sample.

## Applications

- **Building blocks of parallel algorithms.** Parallel graph algorithms, computational geometry and database joins use a parallel sort to group items by a key.
- **Data processing systems.** The shuffle phase of a MapReduce job and distributed database sorts are sample sorts across machines.
- **GPU computing.** Radix sort and merge sort with [merge path](/merge-path/) partitioning are the standard sorts on graphics processors.
- **Hardware.** Fixed comparator networks such as bitonic sort are built in hardware and used in switching networks.

## References
