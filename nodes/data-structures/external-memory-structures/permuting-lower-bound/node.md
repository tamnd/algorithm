---
tag: 9JY1JB
kind: theorem
slug: permuting-lower-bound
name: Permuting lower bound
aliases:
- Aggarwal-Vitter permuting bound
area: data-structures/external-memory-structures
level: advanced
summary: Permuting N items in the external memory model needs Θ(min{N, (N/B) log_{M/B}(N/B)}) I/Os.
prereqs: [external-memory-model, counting-argument]
see_also: [permuting-problem, external-permuting, external-sorting-lower-bound, external-merge-sort, comparison-sort-lower-bound, list-ranking, time-forward-processing]
sources:
  - paper: doi:10.1145/48529.48535
    title: "Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9) (1988), 1116-1127"
    locator: Theorem 3.2 (permuting) and the lower bound proofs of Section 4
  - book: isbn:9781601981066
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4) (2008)
    locator: Chapter 6, lower bounds on I/O, Section 6.1 (permuting) and the table of bounds in Chapter 3
  - paper: doi:10.1007/978-1-4684-2001-2_10
    title: "Robert W. Floyd, Permuting information in idealized two-level storage, in Complexity of Computer Computations (1972), 105-109"
    locator: pp. 105 to 109, the first bounds for special values of the parameters
---

The permuting lower bound says that in the [external memory model](/external-memory-model/), moving $N$ indivisible items into an order given in advance needs $\Omega\big(\min\big\{N, \frac{N}{B}\log_{M/B}\frac{N}{B}\big\}\big)$ block transfers for some permutation, even for an algorithm that knows the permutation and never compares keys. Two simple methods meet it: moving one item per I/O costs $O(N)$, and sorting the items by their target positions costs $O\big(\frac{N}{B}\log_{M/B}\frac{N}{B}\big)$. So permuting costs $\Theta(\min\{N, \mathrm{Sort}(N)\})$ I/Os. Aggarwal and Vitter proved it in 1988. In internal memory, permuting takes $N$ steps and sorting $\Theta(N \log N)$; in external memory the two cost the same for all practical values of $M$ and $B$.

## Statement

**Model.** The machine is that of the [external memory model](/external-memory-model/): an internal memory of $M$ cells, and a disk of blocks of $B$ cells, with $1 \le B \le M/2$. A read copies one block into $B$ cells of the memory, a write copies $B$ cells of the memory into one block, and work in memory is free. Each cell holds at most one item. Items are *indivisible*: the algorithm can copy, move and delete whole items, but cannot build an item from parts of others. The input is $N$ items $x_1, \ldots, x_N$ in the blocks $0, \ldots, n - 1$, where $n = N/B$ is an integer, and the other blocks are empty.

**The problem.** A permutation $\pi$ of $\{1, \ldots, N\}$ is given, and the algorithm must put the item $x_i$ into the cell $\pi(i)$ of the disk, for each $i$. The algorithm may depend on $\pi$ in any way, so it knows the target of every item from the start.

**Theorem (exact form).** Let $t$ be the largest number of I/Os that the algorithm makes over all $N!$ permutations $\pi$. Then

$$2\,\Big(2(n + t)\,S\Big)^{t} \;\ge\; \frac{N!}{(B!)^{n}}, \qquad\text{where } S = \sum_{k=0}^{B}\binom{M}{k}.$$

**Corollary (asymptotic form).** Let $N \ge 4096$, $N \ge e^2 B$ and $M \ge 3B$. Then

$$t \;\ge\; \frac{1}{16}\,\min\Big\{N,\ \frac{N}{B}\log_{M/B}\frac{N}{B}\Big\}.$$

With the upper bounds of the Tightness section, the I/O complexity of permuting is $\Theta\big(\min\big\{N, \frac{N}{B}\log_{M/B}\frac{N}{B}\big\}\big)$. Aggarwal and Vitter (Theorem 3.2) state it as $\Theta\big(\min\big\{N, \frac{N}{B}\frac{\log(1 + N/B)}{\log(1 + M/B)}\big\}\big)$, and prove it for the average over all $\pi$ as well.

## In plain words

You must rearrange a huge file into a fixed new order, and you know where each record must go. You never need to compare records. It still costs as much as sorting.

The reason is counting. There are very many possible new orders. Each disk transfer can change the layout of the data in only so many ways: it picks a block, and for a write it picks which records in memory go into that block. The order of records inside one block does not matter much, because memory can arrange it for free. So the number of different results that a short sequence of transfers can reach is too small to cover all the orders, and some order needs many transfers.

When blocks are tiny, a different simple method wins: move the records one at a time.

## Proof

**Step 1: one copy of each item.** Fix $\pi$ and the run of the algorithm on it. Each item $x_i$ ends in the cell $\pi(i)$. Trace this final copy back in time: it was made by a write from a memory cell, that memory copy was made by a move in memory or by a read from a disk cell, and so on, back to the input cell of $x_i$. At each moment, exactly one cell is on this chain; call it the *place* of $x_i$. The place of $x_i$ is not overwritten while it is the place, because the chain goes on from it. Two items never have the same place, since a cell holds one item.

Define the *state* at a moment as the place of each item reduced to its *location*: either "memory" or the number of a block. So a state assigns each item to memory or to a block, with at most $M$ items in memory and at most $B$ in each block. The state changes only at I/Os, because moves inside memory keep the location "memory".

- At a read of block $j$, some items of block $j$ have their place moved into memory, and the others stay in block $j$. The new state is fixed by $j$ and by a subset of the at most $B$ items located in block $j$: at most $2^B$ choices for a given $j$.
- At a write of block $j$, every cell of block $j$ is overwritten, so no item is located in block $j$ just before it. Some items located in memory get their place in block $j$, at most $B$ of them. The new state is fixed by $j$ and by a subset of at most $B$ of the at most $M$ items in memory: at most $S = \sum_{k \le B}\binom{M}{k}$ choices for a given $j$. Since $B \le M/2$, $S \ge \sum_{k \le B}\binom{B}{k} = 2^B$.

**Step 2: few choices of block.** The blocks $0, \ldots, n - 1$ are the *output blocks*, the others are *scratch blocks*. Rename the scratch blocks in the order in which the run first touches them, as $n, n + 1, \ldots$. All scratch blocks are empty at the start and are not part of the output, so this renaming does not change the final state on the output blocks. At the I/O number $s \le t$, the block is an output block, one of the at most $s - 1$ scratch blocks touched before, or the next new one: at most $n + t$ choices.

So the *trace* of a run, the sequence of states after each I/O, is fixed by a sequence of at most $t$ choices, each of a kind (read or write), a block, and a subset. With $X = 2(n + t)S$, the number of possible traces with exactly $s$ I/Os is at most $X^s$, and the number with at most $t$ I/Os is at most $\sum_{s=0}^{t}X^s \le 2X^t$, since $X \ge 2$.

**Step 3: many final states are needed.** At the end, the place of $x_i$ is the cell $\pi(i)$, so the final state puts $x_i$ into the block $\lfloor (\pi(i) - 1)/B \rfloor$. This is the partition of the items into the $n$ output blocks by their target blocks. Two permutations give the same partition exactly when they differ only inside the target blocks, so there are $N!/(B!)^n$ different partitions. Each needs a trace that ends in it, so

$$2X^t \;\ge\; \frac{N!}{(B!)^n},$$

which is the exact form. $\square$

**Proof of the corollary.** If $t \ge N$, the claim holds. So let $t < N$. Then $n + t \le 2N$. Three standard estimates are used: $N! \ge (N/e)^N$, $B! \le B^B$, and $S \le (eM/B)^B$. The last holds because, for $k \le B$, $\binom{M}{k} \le \binom{M}{k}(B/M)^{k-B}$, so

$$S\Big(\frac{B}{M}\Big)^{B} \le \sum_{k=0}^{M}\binom{M}{k}\Big(\frac{B}{M}\Big)^{k} = \Big(1 + \frac{B}{M}\Big)^{M} \le e^{B}.$$

Hence $\ln X \le \ln(4N) + B\ln\frac{eM}{B} \le 2D$ with $D = \max\big\{\ln(4N),\ B\ln\frac{eM}{B}\big\}$, and taking logarithms of the exact form,

$$t \;\ge\; \frac{N\ln\frac{N}{eB} - \ln 2}{2D} \;\ge\; \frac{N \ln\frac{N}{eB}}{4D}.$$

The second step uses $N\ln\frac{N}{eB} \ge N \ge 2\ln 2$, which holds because $N \ge e^2 B$ gives $\ln\frac{N}{eB} \ge 1$.

*Case 1: $D = B\ln\frac{eM}{B}$.* From $N \ge e^2B$, $\ln\frac{N}{eB} = \ln\frac{N}{B} - 1 \ge \frac12\ln\frac{N}{B}$. From $M \ge 3B$, $\ln\frac{M}{B} \ge \ln 3 > 1$, so $\ln\frac{eM}{B} = 1 + \ln\frac{M}{B} \le 2\ln\frac{M}{B}$. So

$$t \;\ge\; \frac{N \cdot \frac12\ln\frac{N}{B}}{4B \cdot 2\ln\frac{M}{B}} \;=\; \frac{1}{16}\cdot\frac{N}{B}\log_{M/B}\frac{N}{B}.$$

*Case 2: $D = \ln(4N) > B\ln\frac{eM}{B}$.* Then $B < \ln(4N)$, because $\ln\frac{eM}{B} \ge 1$. So $\frac{N}{eB} > \frac{N}{e\ln(4N)} \ge \sqrt{4N}$, where the last step is $\sqrt{N} \ge 2e\ln(4N)$. This holds at $N = 4096$, where $64 > 2e \cdot 9.71 \approx 52.8$, and for all larger $N$, because the derivative of $\sqrt N - 2e\ln(4N)$ is $\frac{1}{2\sqrt N} - \frac{2e}{N} > 0$ when $\sqrt N > 4e$. So $\ln\frac{N}{eB} \ge \frac12\ln(4N)$ and

$$t \;\ge\; \frac{N \cdot \frac12\ln(4N)}{4\ln(4N)} \;=\; \frac{N}{8}.$$

In both cases $t \ge \frac{1}{16}\min\big\{N, \frac{N}{B}\log_{M/B}\frac{N}{B}\big\}$. $\blacksquare$

## Consequences

- **Sorting without comparisons.** Any algorithm that sorts indivisible items must, on the input whose sorted order is $\pi^{-1}$, move each item to its place, so it solves permuting. So sorting needs $\Omega(\min\{N, \mathrm{Sort}(N)\})$ I/Os even for algorithms that are not comparison-based, such as radix sorts that move whole items. In the usual range, where the sort term is the smaller one, this is the full sorting bound. The comparison argument of the [external sorting lower bound](/external-sorting-lower-bound/) also covers the range of tiny blocks.
- **Problems as hard as permuting.** Matrix transposition, [list ranking](/list-ranking/), the Euler tour of a tree and many graph problems contain a permutation of the input as a special case, so they inherit the bound. This is why [time-forward processing](/time-forward-processing/) and sorting are the basic tools of external graph algorithms: they meet it.
- **Average case.** The count of Step 2 does not depend on $\pi$, so at most $2X^t$ of the $N!/(B!)^n$ partitions can be reached with $t$ I/Os. For $t$ a small constant times the bound, this is a tiny fraction, so almost all permutations need $\Omega(\min\{N, \mathrm{Sort}(N)\})$ I/Os.
- **Knowing the permutation does not help.** The algorithm in the theorem may be designed for $\pi$ in advance, with any amount of free computation. The bound comes from the movement of data alone.
- **Parallel disks.** With $D$ disks and one block per disk in each parallel I/O, the bound divided by $D$ holds, as in the [external memory model](/external-memory-model/).

### Worked example

These are the smallest $t$ that satisfy the exact form, found by a binary search on $t$, against the two terms of the minimum.

| $N$ | $B$ | $M$ | exact bound on $t$ | $N$ | $\frac{N}{B}\log_{M/B}\frac{N}{B}$ |
|---|---|---|---|---|---|
| $10^{10}$ | $10^4$ | $8 \cdot 10^7$ | about $1.383 \times 10^6$ | $10^{10}$ | about $1.537 \times 10^6$ |
| $2^{20}$ | 16 | 4096 | about $99\,700$ | $1\,048\,576$ | $131\,072$ |
| $10^8$ | 1 | $10^6$ | about $5.22 \times 10^7$ | $10^8$ | about $1.33 \times 10^8$ |

In the first two rows the sort term is the minimum, and the bound is close to it. In the first row it equals the bound for sorting on the [external sorting lower bound](/external-sorting-lower-bound/) page, because the factor $2(n + t)$ for the choice of block is tiny next to $S$. In the last row the blocks hold one item, the minimum is $N$, and the bound is about $N/2$: there, permuting one item per I/O is optimal up to a factor of 2.

## Tightness

**The naive method, $O(N)$ I/Os.** For each output block in turn, read for each of its $B$ target cells the block that holds the item for it, then write the output block. This makes $N$ reads and $n$ writes, $N + N/B$ I/Os in all, with $2B$ cells of memory. See the [external memory model](/external-memory-model/) page.

**Sorting by target, $O\big(\frac{N}{B}\log_{M/B}\frac{N}{B}\big)$ I/Os.** The algorithm knows $\pi$, so it can sort the items by the key $\pi(i)$ with [external merge sort](/external-merge-sort/), which compares only these targets. The result is the permuted order. For $N > M$ this costs $O\big(\frac{N}{B}\log_{M/B}\frac{N}{B}\big)$ I/Os.

The better of the two is $O(\min\{N, \mathrm{Sort}(N)\})$, so the theorem is tight up to a constant factor. The naive method is the better one exactly when $N < \frac{N}{B}\log_{M/B}\frac{N}{B}$, that is, when $B\log(M/B) < \log(N/B)$, which needs blocks of only a few items.

**Constants.** The constant $1/16$ of the corollary comes from rough estimates. Aggarwal and Vitter give finer forms, and the table shows that the exact form is within a factor of 1.4 of the sort term for realistic parameters.

## History

Floyd (1972) studied permuting in a two-level storage, where a fast memory exchanges pages with a slow one, and proved the first bounds, for special values of the parameters. Aggarwal and Vitter (1988) defined the external memory model with general $M$ and $B$ and proved the bound $\Theta(\min\{N, \mathrm{Sort}(N)\})$ for permuting, with matching bounds for sorting, the FFT, permutation networks and matrix transposition. Their counting argument for permuting is also the main part of their sorting lower bound. Vitter's survey of 2008 gives the argument in its chapter on lower bounds, as a count of the ways in which one I/O can change the set of items in each block.

## References
