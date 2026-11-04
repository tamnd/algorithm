---
tag: EATF60
kind: concept
slug: trivial-lower-bound
name: Trivial lower bound
aliases:
- input-reading bound
- obvious lower bound
area: foundations/lower-bounds
level: intro
summary: A bound that follows because every input item must be read, such as Omega(n) for most problems.
prereqs: [lower-bound, decision-tree-model]
see_also: [adversary-argument, sensitivity, max-finding-lower-bound, matrix-multiplication-quadratic-lower-bound, sublinear-time, linear-search, query-complexity, optimality]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 9.1, Minimum and maximum (each element except the winner must lose a comparison, so n - 1 comparisons are necessary)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Chapter 12, Decision trees (decision tree complexity and certificate complexity)
  - paper: doi:10.1016/S0304-3975(01)00144-X
    title: Harry Buhrman and Ronald de Wolf, Complexity measures and decision tree complexity, a survey, Theoretical Computer Science 288(1) (2002)
    locator: pp. 21 to 43 (sensitivity and its relation to the deterministic decision tree complexity)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 2.4, A Survey of Common Running Times (linear time)
---

The trivial lower bound says that an algorithm must at least read the parts of its input that can change the answer, and write each part of its output. For most problems on $n$ items it gives $\Omega(n)$, and for a problem with an output of size $k$ it gives $\Omega(k)$. The bound needs a short proof, an [adversary argument](/adversary-argument/) on one input, and it is valid only when that proof works. It is the first [lower bound](/lower-bound/) to try, and for many linear-time algorithms it is the one that shows they are [optimal](/optimality/).

## In plain words

To answer a question about some data, a program must look at the data. If one item can change the answer and the program never looks at it, the program cannot know the answer. So a program that adds a list of numbers must read every number, and a program that finds the largest item must look at every item. A program that writes a large result must spend at least one step on each part of the result.

This sounds too obvious to need a proof, but it can be false. A program that searches a sorted list does not read most of the list, because the order tells it where to look. So the bound holds only when each item can matter on a single hard input, and that must be shown.

## The idea

**The query model.** Take inputs $x = (x_1, \dots, x_n) \in \Sigma^n$ and a function $f : \Sigma^n \to Y$. An algorithm reads one position $x_i$ per step, chooses the next position from what it has read, and stops with an output. This is a [decision tree](/decision-tree-model/) whose queries read one position. A word RAM algorithm that reads one input word per step fits this model: count only its reads.

For an input $x$, a position $i$ is **sensitive** at $x$ when some $y$ that differs from $x$ only in position $i$ has $f(y) \ne f(x)$. Let $s(f, x)$ be the number of sensitive positions at $x$. The largest value over all $x$ is the [sensitivity](/sensitivity/) $s(f)$.

**Claim.** Each algorithm that computes $f$ reads at least $s(f, x)$ positions on the input $x$. So its worst-case number of reads is at least $s(f)$.

*Proof.* Let $i$ be sensitive at $x$, and let $y$ differ from $x$ only in position $i$ with $f(y) \ne f(x)$. Suppose that the algorithm does not read position $i$ on input $x$. Run it on $y$. Each position that it reads on $x$ has the same value in $y$, so by induction on the steps it reads the same positions in the same order and gets the same values on $y$. It stops at the same point with the same output. That output is $f(x)$, which is not $f(y)$, so the algorithm is wrong on $y$. So the algorithm reads every sensitive position on $x$, and there are $s(f, x)$ of them. ∎

When some input has all $n$ positions sensitive, the bound is $n$ reads, and so $\Omega(n)$ time on the word RAM.

**The output bound.** An algorithm that writes one output item per step and must output $k$ items needs at least $k$ steps. This is the bound for problems with large outputs: the product of two $n \times n$ matrices has $n^2$ entries, and the list of all pairs of $n$ points has $n(n-1)/2$ entries.

**The condition matters.** That $f$ depends on each position is not enough. The function $f(x_1, x_2, x_3) = x_2$ if $x_1 = 1$ and $x_3$ if $x_1 = 0$ depends on all three bits, but every input has at most 2 sensitive positions, and the algorithm "read $x_1$, then read the bit it names" reads only 2. The bound needs one input on which all positions are sensitive at once.

## Examples

**Examples where the bound holds.**

- **Sum, parity, OR of $n$ bits.** For parity, every position is sensitive at every input. So each algorithm reads all $n$ bits on every input. For OR, take $x = 0^n$: each position is sensitive, so $n$ reads are needed on the all-zero input.
- **Search in an unsorted array.** Let the output be "is $t$ in $A[1..n]$?". At an input where $t$ is absent, each position is sensitive (put $t$ there). So [linear search](/linear-search/) with $n$ probes is optimal, and the absent case is the hard input.
- **The maximum.** Take distinct values and the output "the index of the maximum". Every position is sensitive: raising $x_i$ above all other values moves the maximum to $i$. So $n$ reads are needed. In the comparison model the bound is $n - 1$ comparisons, which needs a different argument because one comparison reads two items ([maximum finding lower bound](/max-finding-lower-bound/)).
- **Matrix multiplication.** The output has $n^2$ entries, so each algorithm takes $\Omega(n^2)$ steps. This is still the best known lower bound for the general problem, and the best known upper bound is near $n^{2.371}$. See the [quadratic lower bound](/matrix-multiplication-quadratic-lower-bound/) and the [matrix multiplication exponent](/matrix-multiplication-exponent/).
- **Graph search.** Breadth-first search on a graph given by adjacency lists takes $O(n + m)$ time. An algorithm that decides if vertex $t$ is reachable from $s$ must read every edge in some inputs, so $\Omega(n + m)$ is a lower bound for the problem on this input format, and breadth-first search is asymptotically optimal.

**Non-examples, where the bound is false or weak.**

- **Search in a sorted array.** [Binary search](/binary-search/) reads $\lfloor \lg n \rfloor + 1$ items, for example 20 items of an array of $10^6$. The promise that the array is sorted makes most positions not sensitive: at an input with $t$ absent, only the two neighbours of the gap where $t$ would be are sensitive under changes that keep the array sorted. See the [sorted search lower bound](/sorted-search-lower-bound/).
- **Sublinear algorithms.** A [sublinear-time](/sublinear-time/) algorithm that estimates the fraction of ones in $n$ bits to within $\pm 0.01$ with probability $0.99$ reads a number of random bits that does not depend on $n$. The bound fails because the answer is approximate and random.
- **The maximum of a heap.** In a max-[heap](/heap/) the maximum is at the root, so one read is enough. The heap order is a promise on the input.
- **Sorting.** The trivial bound gives $n - 1$ comparisons (each item must be compared at least once, and the comparisons must connect all items). The true bound is $\lceil \lg(n!) \rceil$, which is 16 for $n = 8$ against 7. The trivial bound is true but weak.
- **Connectivity with an adjacency matrix.** At a path through all $v$ vertices, only the $v - 1$ edges of the path are sensitive. So the sensitivity bound gives only $v - 1$ reads. An adversary argument gives $\Omega(v^2)$ reads, which is far stronger. See the [decision tree model](/decision-tree-model/).

### Pitfalls

- **Dependence is not sensitivity at one input.** A function can depend on every position without any input that makes all of them sensitive, as the example with three bits shows.
- **Promises on the input.** Sorted, heap ordered or bounded inputs often break the bound. State the input set over which the adversary may change an item: the changed input must still satisfy the promise.
- **Reading a word versus reading a bit.** On the word RAM one step reads $w$ bits. A bound of $n$ bits of input gives only $n/w$ reads.
- **Randomized and approximate algorithms.** The claim above is for exact deterministic algorithms. A randomized algorithm can skip positions with small error probability, and a lower bound for it needs its own argument.
- **Too weak to close a problem.** For sorting, matrix multiplication and many other problems, the trivial bound is far from the best algorithm. A matching trivial bound is a strong result. A non-matching one says little.

## Where it is used

- **Linear-time optimality.** Each algorithm that runs in $O(n)$ time on an input of $n$ words and must read all of it is asymptotically optimal: [median of medians](/median-of-medians/) for selection, [counting sort](/counting-sort/) with a key range of $O(n)$, breadth-first and depth-first search.
- **Output-sensitive bounds.** For listing problems the bound is $\Omega(n + k)$, the size of the input plus the size of the output. Algorithms that meet it are called output-sensitive optimal.
- **The starting point for stronger bounds.** The [adversary argument](/adversary-argument/) for the maximum, for connectivity and for evasive graph properties begins with the reading bound and makes it sharper.
- **Open problems.** For matrix multiplication, the claim $\omega = 2$ would mean that the trivial bound is tight up to $n^{o(1)}$ factors.

## References
