---
tag: X40DBH
kind: algorithm
slug: sample-sort
name: Sample sort
aliases:
- Parallel sample sort
- samplesort
area: sorting/parallel-sorting
level: core
summary: Pick splitters from a random sample, bucket the keys by them, then sort each bucket independently.
solves: [parallel-sorting-problem]
model: crew-pram
complexity:
  vars: {n: the number of keys, p: the number of processors, s: the oversampling factor}
  time: {worst: Θ(n²), average: Θ(n log n)}
  space: {extra: Θ(n + p s)}
  depth: {average: O((n/p) log n + p s log(p s))}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: false, comparison: true, recursive: false}
prereqs: [quicksort, bucket-sort, binary-search, all-prefix-sums, chernoff-bound, crew-pram]
see_also: [parallel-sorting-by-regular-sampling, parallel-quicksort, bucket-sort, external-samplesort, distributed-sorting, bsp-model, parallel-radix-sort, hyperquicksort]
sources:
  - paper: "W. D. Frazer and A. C. McKellar, Samplesort: a sampling approach to minimal storage tree sorting, Journal of the ACM 17(3), 1970"
    locator: the sequential samplesort, which picks splitters from a sorted random sample
  - paper: "Guy E. Blelloch, Charles E. Leiserson, Bruce M. Maggs, C. Greg Plaxton, Stephen J. Smith and Marco Zagha, A comparison of sorting algorithms for the Connection Machine CM-2, Proceedings of the 3rd ACM Symposium on Parallel Algorithms and Architectures (SPAA), 1991"
    locator: parallel sample sort with oversampling, its analysis of the largest bucket, and its comparison with bitonic sort and radix sort
  - paper: "John H. Reif and Leslie G. Valiant, A logarithmic time sort for linear size networks, Journal of the ACM 34(1), 1987"
    locator: flashsort, a sample sort with time O(log n) with high probability on networks of bounded degree
  - book: isbn:9780201648652
    title: Ananth Grama, Anshul Gupta, George Karypis and Vipin Kumar, Introduction to Parallel Computing, second edition, Addison-Wesley, 2003
    locator: Chapter 9, Sorting, the section on bucket and sample sort
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 4, Chernoff and Hoeffding bounds
---

Sample sort sorts $n$ keys on $p$ processors by cutting the key range into $p$ buckets of about equal size and letting each processor sort one bucket. It finds the $p - 1$ cut points, the splitters, by sorting a random sample of $ps$ keys and taking every $s$-th one. With an oversampling factor $s = \Theta(\log n)$, every bucket has at most about $2n/p$ keys with high probability, and on the [CREW PRAM](/crew-pram/) with $p$ processors the sort takes time $O((n/p) \log n)$ when $p^2 \log n = O(n)$. It is [quicksort](/quicksort/) with $p - 1$ pivots at once, and the basis of most sorts on distributed-memory machines.

## In plain words

A class must sort a huge pile of exam papers by score. The teacher picks a few papers at random and sorts only those. From this small sorted set she picks some cut scores, so that the set is cut into equal parts.

Each helper then takes a share of the pile and throws every paper into the box for its score range. Each box goes to one helper, who sorts it alone. Finally the boxes are put in a row.

The papers picked at random look like a small copy of the whole pile, so the boxes come out of about equal size. If the teacher picks more papers, the boxes are more even, but the first sort takes longer.

## The problem

The input is an array $A[0 \ldots n-1]$ of keys from a total order, spread over $p$ processors, $\lceil n/p \rceil$ keys each. The output is the keys in non-decreasing order, as $p$ buckets in a row, with bucket $j$ held by processor $j$. This is the [parallel sorting problem](/parallel-sorting-problem/) on the [CREW PRAM](/crew-pram/) or on a [BSP](/bsp-model/) machine with $p$ processors. In the analysis the keys are distinct. Equal keys are made distinct by pairing each key with its input index.

## The algorithm

Here $s \ge 1$ is the oversampling factor. Bucket $0$ holds the keys at most $y_1$, bucket $j$ the keys in $(y_j, y_{j+1}]$, and bucket $p - 1$ the keys greater than $y_{p-1}$.

```pseudo id=main
SAMPLE-SORT(A[0 .. n − 1], p, s)
L1  draw ps keys of A uniformly at random, with replacement, into S
L2  sort S                                     ▷ ps keys, any sort
L3  y_j ← S[js] for j = 1, …, p − 1           ▷ the splitters
L4  parallel for each key x: b(x) ← number of splitters less than x   ▷ binary search
L5  count the keys of each bucket, take prefix sums of the counts, and move each key to its bucket
L6  parallel for j ← 0 to p − 1 do sort bucket j sequentially
L7  return bucket 0 ∥ bucket 1 ∥ … ∥ bucket p − 1
```

Line L5 is one pass of [parallel radix sort](/parallel-radix-sort/) with the bucket number $b(x)$ as the digit, so it keeps the input order within each bucket.

## Example

Sort $A = [41, 7, 93, 25, 60, 12, 88, 3, 54, 31, 76, 19]$ with $p = 3$ and $s = 2$. Suppose the $ps = 6$ draws are $60, 12, 31, 88, 25, 54$. Sorted, the sample is $S = [12, 25, 31, 54, 60, 88]$, so the splitters are $y_1 = S[2] = 31$ and $y_2 = S[4] = 60$.

| bucket | key range | keys | sorted |
| --- | --- | --- | --- |
| 0 | $x \le 31$ | $7, 25, 12, 3, 31, 19$ | $3, 7, 12, 19, 25, 31$ |
| 1 | $31 < x \le 60$ | $41, 60, 54$ | $41, 54, 60$ |
| 2 | $x > 60$ | $93, 88, 76$ | $76, 88, 93$ |

The three processors sort their buckets at the same time, and the output is the three buckets in a row. Bucket 0 has 6 keys, which is within the bound $\lceil 2n/p \rceil = 8$. With so small a sample the bound is not guaranteed. The point of the analysis is that $s = \Theta(\log n)$ makes it hold with high probability.

## Correctness

Every key of bucket $j$ is less than every key of bucket $j + 1$, because the first is at most $y_{j+1}$ and the second is greater than $y_{j+1}$. Each bucket is sorted on line L6, so the concatenation is sorted. This holds for every sample, so the output is always correct, and only the running time depends on the random draws. With keys paired with their input indices, the sort is also stable. The proof of the bucket bound is in [the proof of correctness](proofs/correctness.md).

## Complexity

**Bucket sizes.** Let the keys be distinct, $p \ge 2$ and $g = \lceil 2n/p \rceil$. Every bucket has at most $g$ keys with probability at least $1 - n e^{-s/4}$. With $s = \lceil 12 \ln n \rceil$ this is at least $1 - n^{-2}$. The proof: if a bucket has more than $g$ keys, then some run of $g$ consecutive keys in sorted order gets at most $s$ of the $ps$ draws, while each run expects at least $2s$. A [Chernoff bound](/chernoff-bound/) and a union bound over the $n$ runs give the result.

**Time on the CREW PRAM with $p$ processors.** Lines L1 and L3 take time $O(s)$. Sorting the sample on one processor takes time $O(ps \log(ps))$. On line L4 each key does a [binary search](/binary-search/) over the $p - 1$ splitters, and all processors read the splitters at the same time, which needs concurrent reads. This takes time $O((n/p) \log p)$. Line L5 takes time $O(n/p + p + \log p)$, as one pass of parallel radix sort. Line L6 takes time $O((n/p) \log(n/p))$ when every bucket has at most $2n/p + 1$ keys. So with high probability the time is

$$O\left(\frac{n}{p} \log n + ps \log(ps)\right),$$

which is $O((n/p) \log n)$ when $p^2 \log n = O(n)$ and $s = \Theta(\log n)$. The work is then $O(n \log n)$, which matches the [comparison lower bound](/comparison-sort-lower-bound/).

**BSP cost.** On a [BSP](/bsp-model/) machine, the sample is gathered on one processor and the splitters are broadcast, and line L5 is one total exchange, an [h-relation](/h-relation/) with $h \le 2n/p + 1$ with high probability. So the sort uses a constant number of [supersteps](/superstep/), and local work $O((n/p) \log n)$.

**Worst case.** If the sample is very unlucky, one bucket can get almost all the keys, and the work of line L6 is then that of the sequential sort used. With quicksort there, the worst case is $\Theta(n^2)$.

## Properties

- **Las Vegas.** The output is always sorted. Only the bucket sizes, and so the time, depend on the random sample.
- **One round of communication.** Each key moves once, from its first processor to its bucket. This is the main reason sample sort is fast on machines where moving data is costly.
- **Stable with index pairs.** With each key paired with its input index, and the move on line L5 order-preserving, equal keys keep their input order.
- **Not in place.** The buckets go to new memory.

## Variants and improvements

- **Regular sampling.** [Parallel sorting by regular sampling](/parallel-sorting-by-regular-sampling/) sorts each processor's keys first and takes $p$ evenly spaced samples from each. This gives a deterministic bound of $2n/p$ keys per bucket for distinct keys.
- **Recursive sample sort.** If a bucket is still large, sort it by sample sort again. Flashsort of Reif and Valiant does this on networks of bounded degree and sorts in time $O(\log n)$ with high probability.
- **Splitter selection by a parallel sort.** For large $p$, the sample of $ps$ keys is sorted in parallel, for example by [bitonic sort](/bitonic-sort/), so that line L2 does not take time $\Theta(ps \log(ps))$ on one processor.
- **External memory.** [External samplesort](/external-samplesort/) uses the same splitters to cut a large file into buckets that fit in memory.
- **Integer keys.** If the keys are small integers, [parallel radix sort](/parallel-radix-sort/) avoids the binary searches and the bucket sorts.

## When to use it

Use sample sort on distributed-memory machines, clusters and GPUs for general comparison keys, when moving data between processors is the main cost. It is also a good shared-memory sort for many cores, since it reads and writes each key only a few times. For small $p$, or when a deterministic bound is needed, use [regular sampling](/parallel-sorting-by-regular-sampling/). For integer keys, compare with [parallel radix sort](/parallel-radix-sort/).

## Pitfalls

- **Too small a sample.** With $s = 1$, the largest bucket is about $\ln p$ times the mean, which wastes most of the processors on line L6. The bound needs $s = \Theta(\log n)$.
- **Equal keys.** If many keys are equal, they all fall into one bucket, whatever the sample. Pairing each key with its index, or sending the keys equal to a splitter to more than one bucket, fixes this.
- **Sequential splitter sort.** Sorting the sample on one processor costs $\Theta(ps \log(ps))$, which is larger than the rest of the sort when $p^2$ is close to $n$.
- **Wrong bucket rule at the splitters.** The rule for a key equal to a splitter must be the same on every processor, or keys equal to a splitter end up in two buckets in an unsorted order.

## Implementations

## History

Frazer and McKellar described samplesort in 1970 as a sequential sort that improves quicksort by choosing many pivots from a sample. The parallel form with oversampling was analysed by several groups in the 1980s, among them Reif and Valiant with flashsort in 1987. Blelloch and others found in 1991 that sample sort was the fastest of the sorts they implemented on the Connection Machine CM-2 for large inputs.

## References
