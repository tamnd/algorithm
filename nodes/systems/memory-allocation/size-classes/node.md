---
tag: 3FJ7YX
kind: concept
slug: size-classes
name: Size classes
aliases:
- segregated size classes
- allocation size classes
area: systems/memory-allocation
level: intro
summary: "A fixed list of block sizes. Each request is rounded up to the next class, and with classes a factor r apart, the waste is less than (r-1)/r of the block."
prereqs: [internal-fragmentation]
see_also: [segregated-free-lists, buddy-system, fibonacci-buddy-system, slab-allocator, tlsf, external-fragmentation, floor-log2, jemalloc]
sources:
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: Section 3.6, Segregated free lists (size classes, simple segregated storage and segregated fits) and Section 3.7, Buddy systems (powers of two and Fibonacci sizes)
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, CRC Press, 2011
    locator: Chapter 7, Allocation (segregated fits and size classes)
  - paper: "Miguel Masmano, Ismael Ripoll, Alfons Crespo and Jorge Real, TLSF, a new dynamic memory allocator for real-time systems, 16th Euromicro Conference on Real-Time Systems (ECRTS), 2004"
    locator: the first-level classes by powers of two, split into 2^SLI linear second-level classes
---

*Size classes* are a fixed, sorted list of block sizes $c_0 < c_1 < \cdots < c_K$ that an allocator uses for all its blocks. A request of $n$ words gets a block of the least class $c_i \ge n$. The rounding wastes $c_i - n$ words, the [internal fragmentation](/internal-fragmentation/) of the request. In exchange, all blocks of a class are interchangeable, so the allocator can keep one free list or one set of pages per class and find a block without a search. The spacing of the classes sets the worst waste: if each class is at most $r$ times the one before, a request wastes less than $(r - 1)/r$ of its block.

## In plain words

A shoe shop does not stock every foot length. It stocks a fixed list of sizes, and you take the smallest size that fits. The extra room in the shoe is lost.

An allocator does the same with memory. It keeps blocks only in a fixed list of sizes, and it gives each request the smallest block that is big enough. Because all blocks of one size are the same, the allocator can keep them on one list and take the first one, with no search.

Few sizes far apart are cheap to manage, but they waste much room. Many sizes close together waste little room, but each size needs its own list, and memory kept for one size cannot easily serve another. Good allocators pick sizes that grow by a fixed factor, so that the lost room is always a small share of the block.

## The idea

**Rounding.** Let $\text{class}(n)$ be the least $c_i \ge n$. A request with $n > c_K$ is outside the classes; allocators serve such large requests in another way, for example with whole pages.

**Theorem (the geometric bound).** Let the classes satisfy $c_{i+1} \le r\, c_i$ for each $i$, with $r > 1$. Then for every request with $c_0 < n \le c_K$,

$$\text{class}(n) - n < \frac{r - 1}{r} \cdot \text{class}(n).$$

*Proof.* Let $c_i < n \le c_{i+1}$, so $\text{class}(n) = c_{i+1}$. Then $c_{i+1} - n < c_{i+1} - c_i$, and $c_i \ge c_{i+1}/r$, so $c_{i+1} - c_i \le c_{i+1} - c_{i+1}/r = \frac{r-1}{r} c_{i+1}$. $\square$

The bound is tight in the limit. The request $n = c_i + 1$ wastes $c_{i+1} - c_i - 1$ words, and if $c_{i+1} = r c_i$ the share of waste is $\frac{r-1}{r} - \frac{1}{c_{i+1}}$, which tends to $\frac{r-1}{r}$ as the sizes grow. The bound is on the share of the *block*. As a share of the request, the waste is less than $r - 1$.

**Two families.**

- *Powers of two*, $1, 2, 4, 8, \ldots$. Here $r = 2$, so the waste is less than half of the block. The [buddy system](/buddy-system/) uses these classes.
- *Geometric classes with $g$ classes per doubling*, for $g$ a power of two. Take every size from 1 to $2g$, and then, for each power of two $2^e \ge 2g$, the sizes $2^e + j \cdot 2^e/g$ for $j = 1, \ldots, g$. Two consecutive classes from $g$ on differ by a step $s$ and the smaller one is at least $g s$, so the ratio is at most $1 + 1/g$. With $r = 1 + 1/g$ the bound gives a waste of less than $\frac{1}{g+1}$ of the block. For example, with $g = 4$ the ratio is $1.25$ and the waste is less than 20 percent.

**The cost of many classes.** Up to $2^{20}$ words, there are 21 power-of-two classes, 40 classes with $g = 2$, 76 with $g = 4$ and 144 with $g = 8$. Each class needs its own list or its own pages. Memory that is free in one class does not serve a request of another class until it is merged or given back, so more classes can turn the saved internal fragmentation into [external fragmentation](/external-fragmentation/). Most designs pick a few classes per doubling.

**Finding the class in constant time.** For geometric classes, the class of $n > 2g$ follows from a few word operations, as in [TLSF](/tlsf/): let $e = \lfloor \lg(n - 1) \rfloor$, found with a [floor log2](/floor-log2/) instruction, so that $2^e < n \le 2^{e+1}$. The step is $s = 2^e / g$, and the class is $2^e + j s$ with $j = \lceil (n - 2^e)/s \rceil$, which is a shift. The class index is $2g - 1 + (e - \lg 2g)\, g + j$. The page's code checks this formula against a binary search for every $n$ up to $2^{14}$.

## Examples

**Classes with $g = 4$.** The classes up to 128 words are

$$1, 2, \ldots, 8,\ 10, 12, 14, 16,\ 20, 24, 28, 32,\ 40, 48, 56, 64,\ 80, 96, 112, 128.$$

| request $n$ | power-of-two class | waste | class with $g = 4$ | waste |
|---|---|---|---|---|
| 5 | 8 | 37.5% | 5 | 0% |
| 9 | 16 | 43.8% | 10 | 10% |
| 33 | 64 | 48.4% | 40 | 17.5% |
| 65 | 128 | 49.2% | 80 | 18.8% |
| 100 | 128 | 21.9% | 112 | 10.7% |
| 129 | 256 | 49.6% | 160 | 19.4% |

The rows with $n = 2^e + 1$ are the worst case of power-of-two classes, and they move toward 50 percent. The requests $9 = 8 + 1$, $33 = 32 + 1$, $65 = 64 + 1$ and $129 = 128 + 1$ are also just above a class with $g = 4$, and their waste moves toward 20 percent but stays below it.

**Exhaustive check.** For powers of two and for $g = 1, 2, 4, 8, 16$, the page's code tests the theorem for every $n$ up to $2^{14}$ with exact fractions, and finds the largest waste close to $1/(g + 1)$ for each $g$.

**Fibonacci classes.** The sizes $1, 2, 3, 5, 8, 13, \ldots$ of the [Fibonacci buddy system](/fibonacci-buddy-system/) are not exactly geometric, but the ratio of consecutive sizes is at most $5/3$ from size 3 on and tends to about $1.618$. The bound gives a waste of less than $2/5$ of the block.

## Where it is used

- **Buddy systems.** The [buddy system](/buddy-system/) uses powers of two, and its variants use Fibonacci or other sizes so that blocks can split into blocks of other classes.
- **Segregated storage.** [Segregated free lists](/segregated-free-lists/) keep one free list per class. In the terms of Wilson et al., *simple segregated storage* never splits or merges blocks, and *segregated fits* allow both.
- **Slab and object caches.** The [slab allocator](/slab-allocator/) keeps one cache per object type, and general caches for a set of size classes.
- **Real-time allocators.** [TLSF](/tlsf/) splits each power-of-two range into $2^{SLI}$ equal parts, which is the geometric family with $g = 2^{SLI}$.
- **General-purpose allocators.** Allocators such as [jemalloc](/jemalloc/), [tcmalloc](/tcmalloc/) and [mimalloc](/mimalloc/) use a small number of classes per doubling for small objects and serve large requests by pages. Their exact tables differ between versions, so this page does not list them.

## References
