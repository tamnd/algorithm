---
tag: 6H7AM2
kind: algorithm
slug: parallel-sorting-by-regular-sampling
name: Parallel sorting by regular sampling
aliases:
- PSRS
- regular sampling sort
area: sorting/parallel-sorting
level: advanced
summary: Each processor sorts its block, takes regularly spaced samples to choose splitters, then merges the pieces.
solves: [parallel-sorting-problem]
model: bsp-model
complexity:
  vars: {n: the number of keys, p: the number of processors}
  time: {worst: Θ(n log n + p² log p)}
  space: {extra: Θ(n + p²)}
  depth: {worst: O((n/p) log n + p² log p)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [sample-sort, merge-sort, binary-search, bsp-model]
see_also: [sample-sort, distributed-sorting, bsp-model, h-relation, parallel-merging-problem, merge-path, hyperquicksort, columnsort]
sources:
  - paper: "Hanmao Shi and Jonathan Schaeffer, Parallel sorting by regular sampling, Journal of Parallel and Distributed Computing 14(4), 1992"
    locator: the algorithm and the bound of at most 2n/p keys on any processor for distinct keys
  - paper: "Xiaobo Li, Paul Lu, Jonathan Schaeffer, John Shillington, Pok Sze Wong and Hanmao Shi, On the versatility of parallel sorting by regular sampling, Parallel Computing 19(10), 1993"
    locator: implementations of PSRS on several machines and the treatment of duplicate keys
  - book: isbn:9780072822564
    title: Michael J. Quinn, Parallel Programming in C with MPI and OpenMP, McGraw-Hill, 2004
    locator: Chapter 14, Sorting (parallel sorting by regular sampling)
  - book: isbn:9780201648652
    title: Ananth Grama, Anshul Gupta, George Karypis and Vipin Kumar, Introduction to Parallel Computing, second edition, Addison-Wesley, 2003
    locator: Chapter 9, Sorting, the section on bucket and sample sort
---

Parallel sorting by regular sampling, or PSRS, is a deterministic [sample sort](/sample-sort/) for $p$ processors. Each processor first sorts its own $n/p$ keys and takes $p$ samples at evenly spaced positions. One processor sorts the $p^2$ samples and picks every $p$-th one as a splitter. Each processor then sends the keys between two splitters to one processor, which merges the $p$ sorted pieces it receives. For distinct keys, no processor gets more than $2n/p - p$ keys, so the sort is balanced without randomness. In the [BSP model](/bsp-model/) it takes a constant number of supersteps and local time $O((n/p) \log n)$ when $n \ge p^3$.

## In plain words

A group of helpers must sort a big pile of cards. Each takes an equal share and sorts it. Then each helper picks a few cards from their sorted share at equal distances, like every tenth card, and passes them to a leader.

The leader sorts these sample cards and chooses cut values at equal distances among them. Every helper cuts their sorted share at these values and hands the first part to the first helper, the second part to the second helper, and so on. Each helper now holds a few sorted parts and merges them into one.

Because the samples were taken at equal distances from sorted shares, no helper can get much more than twice a fair share.

## The problem

The input is $n$ keys from a total order, spread over $p$ processors with $n/p$ keys each. The output is the keys sorted, with processor $j$ holding the $j$-th part of the sorted sequence and the parts in order. This is the [parallel sorting problem](/parallel-sorting-problem/) on a distributed-memory machine, analysed in the [BSP model](/bsp-model/). In the analysis $p^2$ divides $n$, $w = n/p^2$, and the keys are distinct. Equal keys are made distinct by pairing each key with its input index.

## The algorithm

Bucket $j$ holds the keys $x$ with $y_j < x \le y_{j+1}$, where $y_0 = -\infty$ and $y_p = +\infty$.

```pseudo id=main
PSRS(n keys, block b on processor b, for b = 0, …, p − 1)
L1  parallel for b: sort block b
L2  parallel for b: send the keys at positions 0, w, 2w, …, (p − 1)w of block b to processor 0
L3  on processor 0: sort the p² samples into S; y_j ← S[jp − 1] for j = 1, …, p − 1; broadcast the y_j
L4  parallel for b: cut block b into pieces P[b][0], …, P[b][p − 1], with P[b][j] the keys of bucket j    ▷ binary search
L5  parallel for b: send P[b][j] to processor j, for each j
L6  parallel for j: merge the p sorted pieces P[0][j], …, P[p − 1][j]
```

## Example

Sort 27 keys on $p = 3$ processors, so $w = 3$. After line L1 the blocks are:

| processor | sorted block | samples at positions 0, 3, 6 |
| --- | --- | --- |
| 0 | $6, 14, 15, 39, 46, 48, 72, 91, 93$ | $6, 39, 72$ |
| 1 | $12, 21, 36, 40, 54, 61, 69, 89, 97$ | $12, 40, 69$ |
| 2 | $20, 27, 32, 33, 53, 58, 72, 84, 97$ | $20, 33, 72$ |

The sorted sample is $S = [6, 12, 20, 33, 39, 40, 69, 72, 72]$, so the splitters are $y_1 = S[2] = 20$ and $y_2 = S[5] = 40$. Processor 0 cuts its block into $6, 14, 15$, then $39$, then $46, \ldots, 93$, and the others cut theirs in the same way.

| processor | bucket | pieces received | keys |
| --- | --- | --- | --- |
| 0 | $x \le 20$ | $[6, 14, 15]$, $[12]$, $[20]$ | 5 |
| 1 | $20 < x \le 40$ | $[39]$, $[21, 36, 40]$, $[27, 32, 33]$ | 7 |
| 2 | $x > 40$ | $[46, 48, 72, 91, 93]$, $[54, 61, 69, 89, 97]$, $[53, 58, 72, 84, 97]$ | 15 |

Each processor merges its pieces, and the three buckets in order are the sorted output. Processor 2 gets $15 = 2n/p - p$ keys, so the bound below is reached by this input.

## Correctness

Every key of bucket $j$ is at most $y_{j+1}$, and every key of bucket $j + 1$ is greater than $y_{j+1}$, so the buckets are in order. Each bucket is the merge of sorted pieces, so it is sorted. Each key lies in exactly one bucket. So the output is sorted for every input. The bound on the bucket sizes is the main claim, proved in [the proof of correctness](proofs/correctness.md): each bucket contains exactly $p$ of the samples, and within one sorted block, a stretch of keys that contains $c$ samples has at most $(c + 1)w - 1$ keys. Summing over the $p$ blocks gives at most $2pw - p = 2n/p - p$ keys.

## Complexity

Each processor holds $n/p$ keys, and $p^2 \mid n$.

**Local work.** Line L1 takes time $O((n/p) \log(n/p))$. Line L3 sorts $p^2$ samples on one processor in time $O(p^2 \log p)$. Line L4 makes $p - 1$ binary searches in time $O(p \log(n/p))$. Line L6 merges $p$ pieces of at most $2n/p$ keys in total with a heap, in time $O((n/p) \log p)$. So the local time is $O((n/p) \log n + p^2 \log p)$, which is $O((n/p) \log n)$ when $n \ge p^3$.

**Communication.** Line L2 is a gather of $p^2$ keys, line L3 a broadcast of $p - 1$ keys, and line L5 a total exchange in which each processor sends $n/p$ keys and receives at most $2n/p - p$. In the [BSP model](/bsp-model/), PSRS uses four [supersteps](/superstep/), and the largest exchange is an [h-relation](/h-relation/) with $h \le 2n/p$.

**Work.** The total work is $O(n \log n + p^2 \log p)$, which is $O(n \log n)$ for $n \ge p^3$.

## Properties

- **Deterministic balance.** For distinct keys, every processor ends with at most $2n/p - p$ keys, for every input, without random sampling.
- **One move per key.** Each key moves once, on line L5, apart from the $p^2$ samples.
- **Stable with index tags.** With keys paired with their input indices, and blocks taken in input order, equal keys keep their input order.
- **Not in place.** The pieces and the merged buckets need new memory.

## Variants and improvements

- **Other offsets.** The original paper takes the samples and the splitters at slightly different positions in each group of $p$, and proves the bound $2n/p$. The choice on this page gives the bound $2n/p - p$ with a short proof.
- **Random sampling.** [Sample sort](/sample-sort/) draws a random sample instead. It does not need the first local sort, but its bound on the load holds only with high probability.
- **More samples.** Take $ps$ samples per processor at evenly spaced positions, and every $ps$-th sorted sample as a splitter. The same proof then bounds the load by $(1 + 1/s) n/p - p$ keys per processor. The cost is a larger sample sort on line L3.
- **Parallel sample sort.** For large $p$, the $p^2$ samples are sorted in parallel, for example by [bitonic sort](/bitonic-sort/), so that line L3 does not take time $\Theta(p^2 \log p)$ on one processor.
- **Merge path for the last merge.** Line L6 can use a multiway form of [merge path](/merge-path/) to split the merge among the cores of one processor.

## When to use it

Use PSRS on clusters and distributed-memory machines with moderate $p$, when the keys are general and a deterministic bound on the load per processor is wanted. It works well when $n \ge p^3$. With very many processors, the $p^2$ samples become a bottleneck, and randomized [sample sort](/sample-sort/) with a smaller sample, or a recursive scheme, is better.

## Pitfalls

- **Duplicate keys.** If many keys are equal, they all fall into one bucket, and one processor can get almost all of the keys. Tag the keys with their index or processor and position before sampling.
- **Too many processors.** For $n < p^3$, the sample sort on line L3 takes longer than the local sorts.
- **Off-by-one splitters.** The bound depends on taking the splitters at the right positions of $S$. With $y_j = S[jp]$ instead, the first bucket gets $p + 1$ samples and the last $p - 1$, and the bound becomes weaker.
- **Uneven blocks.** If $p^2$ does not divide $n$, the samples are not evenly spaced in all blocks. The output is still sorted, but the proof of the bound needs adjusting.

## Implementations

## History

Shi and Schaeffer published PSRS in 1992, with the bound of $2n/p$ keys per processor. Li, Lu, Schaeffer and others reported in 1993 that it ran well on a range of parallel machines and discussed duplicate keys. The method is a deterministic form of the sample sorts of the 1980s, with the local sort done first so that the samples can be taken at regular positions.

## References
