---
tag: T25KTC
kind: theorem
slug: knuth-fifty-percent-rule
name: Knuth's fifty-percent rule
aliases:
- Knuth's 50% rule
- fifty-percent rule of dynamic storage allocation
area: systems/memory-allocation
level: advanced
summary: "In a steady state with N blocks in use, random frees, immediate coalescing and splits with chance p, the heap has about pN/2 free blocks."
prereqs: [first-fit-allocation, coalescing]
see_also: [external-fragmentation, sequential-fit, best-fit-allocation, free-list, boundary-tags, online-memory-allocation, robson-bound, next-fit-allocation]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.5, Dynamic storage allocation, the fifty-percent rule and its derivation from the three types of reserved blocks
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: the discussion of Knuth's fifty-percent rule and of the random trace models on which such results rest
---

Knuth's *fifty-percent rule* says how many free blocks a heap has in a steady state. If $N$ blocks are in use, each of them is equally likely to be the next one freed, free merges each freed block with its free neighbours, and an allocation leaves a remainder with probability $p$, then the average number of free blocks is about $pN/2$. When almost every allocation splits a block, $p$ is close to 1 and there is about one free block for every two used blocks, so about a third of all blocks are free. Knuth stated the rule for first fit in *The Art of Computer Programming*, but the counting argument does not depend on the placement policy. It counts free blocks, not free words, and its assumption of random frees does not hold for many real programs.

## Statement

Use the heap model of [first-fit allocation](/first-fit-allocation/), with immediate [coalescing](/coalescing/). Let the heap run in *cycles*: each cycle frees one used block and then allocates one new block. Assume that

1. the number of used blocks is $N$ at the start of every cycle, so no allocation fails;
2. the freed block is chosen uniformly at random among the $N$ used blocks, independently of the past;
3. an allocation either splits a free block and leaves a free remainder, or uses a whole free block, and over the long run a fraction $p$ of the allocations split;
4. the process is in a steady state: the mean number of free blocks at the start of a cycle does not change from cycle to cycle.

Let $M$ be the number of free blocks at the start of a cycle, and $e \in \{0, 1, 2\}$ the number of ends of the heap where a free block lies.

**Theorem (Knuth's rule in exact form).** Under these assumptions,

$$E[M] = \frac{pN + E[e]}{2}, \qquad\text{so}\qquad \frac{pN}{2} \le E[M] \le \frac{pN}{2} + 1.$$

## In plain words

Look at a busy heap after a long time. Each free block sits between two used blocks, because two free blocks side by side would have been merged. A free makes the number of free blocks go up, stay the same or go down, depending on how many free neighbours the freed block has. An allocation that takes a whole block makes the number go down. In a steady state the ups and the downs cancel out.

When you work this out, the number of free blocks is half the number of used blocks, times the chance that an allocation leaves a piece behind. If almost every allocation leaves a piece, a heap with a thousand used blocks has about five hundred free blocks.

## Proof

Classify the used blocks at the start of a cycle by their free neighbours in memory: $A$ blocks have two free neighbours, $B$ blocks have one and $C$ blocks have none. So $A + B + C = N$.

**Step 1: a counting identity.** Count the pairs (free block, used block) that touch. Because of coalescing, no two free blocks touch, so every side of a free block touches either a used block or an end of the heap. The free blocks have $2M$ sides in all, and $e$ of them touch an end, so there are $2M - e$ pairs. Counted from the used blocks, there are $2A + B$ pairs. So

$$2M = 2A + B + e = N + A - C + e.$$

This holds at every moment, with no assumption on the trace.

**Step 2: the change in one cycle.** Freeing a block with $k$ free neighbours makes one new free block and merges it with $k$ free blocks into one, so $M$ changes by $1 - k$: by $+1$ for a type-$C$ block, by $0$ for type $B$ and by $-1$ for type $A$. By assumption 2, the freed block is of type $C$ with probability $C/N$ and of type $A$ with probability $A/N$. The allocation that follows changes $M$ by $0$ if it splits, because the remainder takes the place of the block, and by $-1$ if it uses a whole block. So, given the state at the start of a cycle,

$$E[\Delta M \mid \text{state}] = \frac{C - A}{N} - \Pr[\text{whole block}].$$

**Step 3: the steady state.** By assumption 4, $E[\Delta M] = 0$. Taking the mean over the states and using assumption 3 for the allocations,

$$\frac{E[C - A]}{N} = 1 - p.$$

**Step 4.** Take the mean of the identity of Step 1: $2E[M] = N - E[C - A] + E[e] = N - (1 - p)N + E[e] = pN + E[e]$. Since $0 \le e \le 2$, the bounds follow. $\blacksquare$

Steps 1 and 2 hold for any placement policy, so the theorem holds for first fit, [best fit](/best-fit-allocation/) and the other [sequential fits](/sequential-fit/); only $p$ depends on the policy. Knuth's own argument counts the same three types of used blocks and ignores the ends of the heap.

## Consequences

- **The free list is long.** A first-fit search may have to look at $\Theta(M) = \Theta(pN)$ free blocks, so the time of a [sequential fit](/sequential-fit/) grows with the number of live blocks. This is one reason for indexed fits and [segregated free lists](/segregated-free-lists/).
- **One third of the blocks.** With $p$ close to 1, the free blocks are about $M/(M + N) \approx 1/3$ of all blocks.
- **The free memory.** If the average free block has $k$ times the size of the average used block, the fraction of memory that is free is about $pk/(pk + 2)$. The rule alone does not give $k$, so it says nothing direct about [external fragmentation](/external-fragmentation/) in words.
- **Exact fits help.** A policy that finds exact fits more often has a smaller $p$ and so fewer free blocks. Best fit had a smaller $p$ than first fit in the simulation below.

**A seeded simulation.** The simulation keeps $N = 200$ blocks in use in a heap of $2^{15}$ words. Each cycle frees a random live block and allocates a block of 1 to 64 words, chosen uniformly. It runs 2000 cycles to reach the steady state and then measures $M/N$ and $p$ over 8000 more cycles.

| run | measured $M/N$ | measured $p$ | $p/2$ |
|---|---|---|---|
| first fit, seed 0 | 0.320 | 0.625 | 0.313 |
| first fit, seed 1 | 0.324 | 0.637 | 0.319 |
| first fit, seed 2 | 0.317 | 0.637 | 0.318 |
| best fit, seed 0 | 0.208 | 0.404 | 0.202 |
| first fit, sizes 1 to 2000, heap of $2^{18}$ words | 0.498 | 0.981 | 0.490 |

The measured ratio stays within about 0.01 of $p/2$, and slightly above it on average, as the term $E[e]/2N$ predicts. With requests of 1 to 2000 words almost every allocation splits, and the ratio is close to one half.

## Tightness

The identity of Step 1 is exact, and the bounds $pN/2 \le E[M] \le pN/2 + 1$ cannot be improved in general, since $e$ can be 0 or 2. The assumptions, however, matter.

- **Frees that are not random.** If the program always frees the block that it allocated last, as a stack does, the freed block always touches the free space after it, so it is never of type $C$. In the simulation with such frees and first fit, every allocation split a block ($p = 1$), yet there was only one free block at the start of each cycle, so $M/N = 0.005$ and not $0.5$. Step 3 fails because the freed block is not uniform over the used blocks.
- **One request size.** If all requests have the same size, a freed block is reused whole, $p$ is close to 0 and so is $M$. The rule holds, but it says little.
- **No steady state.** A program that grows its heap, or changes its sizes in phases, never reaches the steady state of assumption 4. Wilson, Johnstone, Neely and Boles argue that real programs are of this kind, so results from random traces must be used with care.
- **Small $N$.** The term $E[e]/2$ is up to 1 block, which matters when $N$ is small.

## History

Knuth gave the rule in Section 2.5 of the first volume of *The Art of Computer Programming*, first published in 1968, in the study of the storage allocation algorithms of that section, and named it the fifty-percent rule. Later work, summed up in the survey of Wilson, Johnstone, Neely and Boles, criticised the random-trace model on which this and similar results rest, and moved the study of allocators to traces of real programs.

## References
