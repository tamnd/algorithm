---
tag: JTQXV5
kind: concept
slug: h-relation
name: h-relation
aliases:
- BSP h-relation
- routing relation
area: parallel/mapreduce-and-bsp
level: advanced
summary: A communication pattern in which each processor sends at most h words and receives at most h words. BSP charges g·h for it, so only the busiest processor counts.
prereqs: [bsp-model, superstep]
see_also: [barrier-synchronization, shuffle-phase, data-skew, edge-coloring, scatter-and-gather, mapreduce-communication-lower-bounds]
sources:
  - paper: doi:10.1145/79173.79181
    title: "Leslie G. Valiant, A bridging model for parallel computation, Communications of the ACM 33(8), 1990"
    locator: pp. 103-111, h-relations and the router that realizes them
  - book: isbn:9780198529392
    title: "Rob H. Bisseling, Parallel Scientific Computation: A Structured Approach using BSP and MPI, Oxford University Press, 2004"
    locator: Chapter 1, the definition of an h-relation, its cost hg + l, and the benchmark that measures g and l
---

An h-relation is a pattern of communication among $p$ processors in which every processor sends at most $h$ words and receives at most $h$ words. In the [BSP model](/bsp-model/) the communication of a [superstep](/superstep/) is an h-relation, and it costs $g \cdot h$, where $g$ is a property of the machine. The cost depends only on the busiest processor, not on the total number of words, so balance is what counts.

## In plain words

Imagine a post office where each person can carry only one letter at a time, both when sending and when receiving. If every person sends and receives at most a few letters, all the mail is done after that many trips, whatever the total amount of mail. But if everybody writes to the same person, that one person must receive every letter, one after another, and the whole town waits for that person. So the time to deliver mail is set by the busiest person. This is the idea of an h-relation: count the largest number of letters that one person must send or receive, and charge for that number only.

## The idea

Number the processors $0$ to $p - 1$. Let $c_{ij}$ be the number of words that processor $i$ sends to processor $j \ne i$ in one superstep. Messages from a processor to itself do not use the network and do not count. The pattern is an $h$-relation when

$$
\sum_{j \ne i} c_{ij} \le h \quad \text{and} \quad \sum_{j \ne i} c_{ji} \le h \qquad \text{for every processor } i.
$$

The h of the superstep is the least such $h$, that is, $h = \max_i \max\left(\mathrm{out}_i, \mathrm{in}_i\right)$. The BSP model charges $g\,h$ for it, plus the barrier cost $L$ of the superstep.

Why the maximum? A processor that must send or receive $h$ words needs at least $h$ word-times at its own network port, so no router can finish faster than the busiest processor. The BSP contract is that the router meets this bound up to the constant $g$: any $h$-relation, however its words are spread, takes about $g\,h$ time. On a real machine $g$ is measured by timing h-relations of many sizes and fitting a line, time $\approx g\,h + L$; for small $h$ the constant term dominates, which is why $L$ is part of every superstep.

Two facts follow from the definition.

- **Total volume.** An $h$-relation moves at most $p\,h$ words. A pattern that moves $V$ words in total has $h \ge V/p$, with equality only when every processor sends and receives the same amount.
- **Decomposition into permutations.** Let each word be a single message. Draw a bipartite multigraph with the senders on one side, the receivers on the other, and one edge per word. Every vertex has degree at most $h$. By Kőnig's theorem on [edge coloring](/edge-coloring/) of bipartite multigraphs, the edges can be colored with $h$ colors so that no two edges of one color share a vertex. Each color class is a partial permutation (a 1-relation). So every $h$-relation of single words is the union of $h$ 1-relations, and a router that can do one permutation per $g$ time units can do any $h$-relation in $g\,h$ time.

## Examples

All examples use $p$ processors and count words.

| Pattern | Words moved | $h$ |
|---|---|---|
| a permutation (each sends one word to a distinct processor) | $p$ | $1$ |
| gather: each processor sends one word to processor $0$ | $p - 1$ | $p - 1$ |
| direct broadcast of one word from processor $0$ | $p - 1$ | $p - 1$ |
| total exchange: each sends one word to every other | $p(p - 1)$ | $p - 1$ |
| transpose of an $n \times n$ matrix stored by blocks of $n/p$ rows | $n^2 (1 - 1/p)$ | $(n^2/p)(1 - 1/p)$ |

The gather and the total exchange have the same $h$, and therefore the same BSP cost, although the total exchange moves $p$ times more data. For $p = 8$ both are 7-relations; one moves 7 words and the other 56. For the transpose with $n = 8$ and $p = 4$, each processor holds 2 rows, that is 16 words, and keeps the $16/4 = 4$ words of its own diagonal block, so $h = 12$.

**Balancing an unbalanced pattern.** A direct broadcast of $n$ words from one processor is an $n(p - 1)$-relation. The two-phase broadcast of the [BSP model](/bsp-model/) page first scatters $n/p$ words to each processor and then lets each processor send its piece to all others. Each of the two supersteps is an h-relation with $h \le (p - 1)\lceil n/p \rceil$, so the cost drops from about $n p g$ to about $2 n g$, at the price of one more barrier.

**Skew in a shuffle.** In a [MapReduce](/mapreduce-model/) [shuffle](/shuffle-phase/), the reducer machine that receives the most data sets $h$. If one key has a third of all values, its machine receives at least a third of the data, so $h \ge V/3$ instead of $V/p$, whatever the number of machines. This is the problem of [data skew](/data-skew/).

## Where it is used

- The BSP cost $W + gH + SL$ of every BSP algorithm, where $H$ is the sum of the h of the supersteps. The [BSP model](/bsp-model/) page derives $h$ for broadcast, prefix sums and sorting by regular sampling.
- Algorithm design for distributed memory. Many algorithms add a randomization or a two-phase step to turn a skewed pattern into a balanced one, because a balanced pattern with more total words can be cheaper than a skewed one with fewer.
- The analysis of MapReduce and of the massively parallel computation model, where the largest reducer input plays the part of $h$ and the [communication lower bounds](/mapreduce-communication-lower-bounds/) bound the total volume.

## References
