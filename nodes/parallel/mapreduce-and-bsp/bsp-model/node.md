---
tag: C7AB2T
kind: model
slug: bsp-model
name: Bulk synchronous parallel model
aliases:
- BSP
- Valiant BSP
area: parallel/mapreduce-and-bsp
level: core
summary: A cost model for distributed-memory parallel computers. A program is a sequence of supersteps, and a superstep with local work w and an h-relation costs w + g·h + L.
history:
  year: 1990
  people: [Leslie G. Valiant]
  note: Valiant proposed BSP as a bridging model between parallel software and hardware in Communications of the ACM in 1990.
prereqs: [pram-model, barrier-synchronization]
see_also: [superstep, h-relation, pregel-model, mrc-model, mapreduce-model, work-span-model, parallel-sorting-by-regular-sampling, all-prefix-sums]
sources:
  - paper: doi:10.1145/79173.79181
    title: "Leslie G. Valiant, A bridging model for parallel computation, Communications of the ACM 33(8), 1990"
    locator: pp. 103-111, the BSP computer (components, router, synchronization with periodicity L) and the simulation of PRAMs with parallel slack
  - book: isbn:9780198529392
    title: "Rob H. Bisseling, Parallel Scientific Computation: A Structured Approach using BSP and MPI, Oxford University Press, 2004"
    locator: Chapter 1, the BSP model, the superstep cost w + hg + l, and the BSP parameters of real machines
  - paper: "Hanmao Shi and Jonathan Schaeffer, Parallel sorting by regular sampling, Journal of Parallel and Distributed Computing 14(4), 1992"
    locator: the algorithm and the bound of fewer than 2n/p items per processor after the exchange
  - paper: "David Culler, Richard Karp, David Patterson, Abhijit Sahay, Klaus Erik Schauser, Eunice Santos, Ramesh Subramonian and Thorsten von Eicken, LogP: towards a realistic model of parallel computation, PPoPP 1993"
    locator: the LogP parameters L, o, g and P
---

The bulk synchronous parallel (BSP) model is a cost model for parallel computers in which each processor has its own memory and the processors talk by messages. A program runs as a sequence of [supersteps](/superstep/): the processors compute on local data, send messages, and then wait at a [barrier](/barrier-synchronization/). Valiant proposed it in 1990 as a "bridging model", a simple contract between the people who write parallel programs and the people who build parallel machines. A superstep costs $w + g \cdot h + L$, where $w$ is the local work, $h$ is the size of the [h-relation](/h-relation/) and $g$ and $L$ describe the machine.

## The machine

The notation follows the parallel pages of this site. On BSP pages, $S$ counts supersteps: it plays the part that the span plays in the [work-span model](/work-span-model/).

| Symbol | Meaning |
|---|---|
| $n$ | the input size |
| $p$ | the number of processors |
| $w_s$, $h_s$ | the local work and the h-relation of superstep $s$ |
| $W = \sum_s w_s$ | the BSP work: the sum over supersteps of the largest local work |
| $H = \sum_s h_s$ | the total communication volume, in the h-relation sense |
| $S$ | the number of supersteps |
| $g$ | the time to route one word of an h-relation, in units of one local operation |
| $L$ | the time of one barrier, and the least time of a superstep |

A BSP computer has three parts.

1. $p$ processors, each with its own local memory. A processor reads and writes only its own memory.
2. A router that delivers point-to-point messages between processors. The model does not look at the network topology: it only charges for the number of words that each processor sends and receives.
3. A facility for [barrier synchronization](/barrier-synchronization/) of all processors.

A superstep has three phases. First, each processor computes on the data in its own memory. Second, each processor sends messages; a message sent in superstep $s$ is available to its receiver only at the start of superstep $s + 1$. Third, all processors take part in a barrier. No processor starts superstep $s + 1$ before all processors have finished superstep $s$. In a superstep, processor $i$ does $w_s^{(i)}$ local operations, sends $\mathrm{out}_s^{(i)}$ words and receives $\mathrm{in}_s^{(i)}$ words. Then

$$
w_s = \max_i w_s^{(i)}, \qquad h_s = \max_i \max\left(\mathrm{out}_s^{(i)}, \mathrm{in}_s^{(i)}\right).
$$

## What it counts

The cost of superstep $s$ and of a whole program are

$$
T_s = w_s + g\,h_s + L, \qquad T = \sum_{s=1}^{S} T_s = W + g\,H + S\,L.
$$

The three terms keep three costs apart. $W$ is the computation, as in a sequential analysis but taken on the busiest processor. $gH$ is the bandwidth cost: if the network can move about $p/g$ words per unit of time in total, then a balanced h-relation in which every processor sends and receives $h$ words takes about $gh$ time. $SL$ is the latency and synchronization cost, paid once per superstep however little is sent. An algorithm designer therefore wants $W$ close to $T_{seq}/p$, $H$ small, and $S$ small, and the three goals often pull in different directions.

The parameters $g$ and $L$ are measured for each machine, in units of one local operation (Bisseling, Chapter 1, gives such measurements and the benchmark that makes them). A large $L$ favours algorithms with few supersteps. A large $g$ favours algorithms that send few words.

Valiant's paper describes the synchronization in a different way: the machine checks every $L$ time units whether the current superstep is complete, so a superstep takes a whole number of periods of length $L$. Later texts, Bisseling's among them, charge $w + gh + L$. Since

$$
\max(w, gh, L) \le w + gh + L \le 3 \max(w, gh, L),
$$

the max form and the sum form agree within a factor of 3, and all asymptotic bounds are the same in both.

A message to oneself does not use the router, so it does not count in $h$. In the simulator of this page, a superstep is a function that sees only its own processor's state and inbox; the simulator delivers all messages at once at the end, which is the barrier.

## Relation to other models

- [PRAM](/pram-model/). A PRAM has free and synchronous access to a shared memory. BSP drops shared memory and charges for communication and synchronization. Valiant showed that, when each real processor runs about $\log p$ or more virtual PRAM processors (parallel slack) and the shared memory is spread over the processors by a random hash function, a BSP computer with $g = O(1)$ and $L = O(\log p)$ can simulate an EREW PRAM with only a constant factor of extra work, with high probability.
- [Work-span model](/work-span-model/). The work-span model counts operations and the critical path, and it has no notion of where data lives. BSP adds the data placement: the same algorithm can have the same work in both models and very different $H$.
- LogP (Culler et al. 1993) has no barriers. It charges each single message for latency $L$, a send and receive overhead $o$ and a gap $g$ between messages of one processor. BSP charges whole supersteps, which is coarser but makes the analysis of a program much shorter.
- [MapReduce](/mapreduce-model/) and the [MRC model](/mrc-model/). A MapReduce round is a superstep: the map and reduce functions are the local work, and the [shuffle](/shuffle-phase/) is the h-relation. MRC and the massively parallel computation (MPC) model keep the superstep structure but count only the number of rounds and the memory of each machine; they do not charge $g$ and $L$.
- [Pregel](/pregel-model/) is BSP with one thread of control for each vertex of a graph.

## Known results in the model

The results below are proved on this page and checked by the Python simulator for many $p$ and $n$. Write $\lg p = \log_2 p$.

### Broadcast

One processor, the root, has one word $x$ and all processors must get it.

- Direct: the root sends $x$ to the $p - 1$ others in one superstep. The root sends $p - 1$ words, so $h = p - 1$, and the cost is $(p - 1)g + L$.
- Tree: in superstep $t = 0, 1, \ldots$ each processor of rank $r < 2^t$ (rank measured from the root) sends $x$ to rank $r + 2^t$. After superstep $t$ the ranks $0$ to $2^{t+1} - 1$ hold $x$, so $\lceil \lg p \rceil$ supersteps suffice. Each processor sends and receives at most one word in a superstep, so the cost is $\lceil \lg p \rceil (g + L)$.

The tree is cheaper when $L$ is small and $p$ is large; the direct method is cheaper when $L$ is large. For $p = 16$, $g = 4$ and $L = 50$, the direct broadcast costs $60 + 50 = 110$ and the tree costs $4 \cdot 54 = 216$.

For a broadcast of $n$ words, the direct method costs $n(p-1)g + L$. The two-phase broadcast does better. In superstep 1 the root splits the data into $p$ pieces of at most $\lceil n/p \rceil$ words and sends piece $j$ to processor $j$. In superstep 2 every processor sends its piece to all others. In each superstep a processor sends or receives at most $p - 1$ pieces, so

$$
T_{\text{two-phase}} \le 2(p - 1)\left\lceil \frac{n}{p} \right\rceil g + 2L,
$$

about $2ng + 2L$ for $n \ge p$, against $n(p - 1)g + L$. When $p$ divides $n$ the bound on $h$ is met exactly in both supersteps.

### Prefix sums

Processor $i$ holds block $i$ of an array of $n$ numbers, with at most $\lceil n/p \rceil$ numbers in a block, and must end with the inclusive [prefix sums](/all-prefix-sums/) of its block in the whole array.

1. Superstep 1: each processor computes the prefix sums of its own block, and sends its block total to every processor $j > i$. Processor $0$ sends $p - 1$ words and processor $p - 1$ receives $p - 1$ words, so $h_1 = p - 1$.
2. Superstep 2: processor $i$ adds the $i$ totals it received and adds that offset to each of its values.

So $S = 2$, $H = p - 1$, and $W \le 2\lceil n/p \rceil + p - 1$:

$$
T \le 2\left\lceil \frac{n}{p} \right\rceil + p - 1 + (p - 1)g + 2L.
$$

Example: $p = 4$ and the blocks $[3,1,4]$, $[1,5,9]$, $[2,6,5]$, $[3,5,8]$. After superstep 1 the blocks are $[3,4,8]$, $[1,6,15]$, $[2,8,13]$, $[3,8,16]$ and the totals are $8, 15, 13, 16$. The offsets are $0, 8, 23, 36$, and the result is $[3,4,8]$, $[9,14,23]$, $[25,31,36]$, $[39,44,52]$. The simulator charges $(w, h) = (3, 3)$ and $(6, 0)$ for the two supersteps.

For $n \gg p^2$ this is work-efficient: $W = O(n/p)$, and the communication does not grow with $n$.

### Sorting by regular sampling

[Sorting by regular sampling](/parallel-sorting-by-regular-sampling/) (Shi and Schaeffer 1992) is a form of [sample sort](/sample-sort/) with a deterministic bucket bound. Each processor holds $m = n/p$ keys, with $m \ge p$, and we make the keys distinct by tagging each with its processor and position.

1. Superstep 1: each processor sorts its keys and sends $p$ regular samples, the keys of rank $m/p, 2m/p, \ldots, m$ (rounded up), to processor $0$. $h_1 = p(p - 1)$, received by processor $0$.
2. Superstep 2: processor $0$ sorts the $p^2$ samples and sends the samples of rank $p, 2p, \ldots, (p-1)p$ to all processors as splitters $\sigma_1 < \cdots < \sigma_{p-1}$. $h_2 = (p - 1)^2$.
3. Superstep 3: each processor splits its sorted keys at the splitters and sends the part in $(\sigma_{j-1}, \sigma_j]$ to processor $j$ (with $\sigma_0 = -\infty$, $\sigma_p = +\infty$).
4. Superstep 4: each processor merges the $p$ sorted runs it received.

**Bucket bound.** If $p$ divides $m$, each processor receives at most $2m - m/p - p + 1 < 2m$ keys in superstep 3.

*Proof.* The samples of processor $i$ are its keys of rank $m/p, 2m/p, \ldots, m$. Fix $j$ with $1 \le j \le p - 1$, and let $c_i$ be the number of samples of processor $i$ that are at most $\sigma_j$. Since $\sigma_j$ is the sample of rank $jp$, $\sum_i c_i = jp$. Let $N_i$ be the number of keys of processor $i$ that are at most $\sigma_j$. The key of rank $c_i m/p$ is at most $\sigma_j$, and if $c_i < p$ the key of rank $(c_i + 1)m/p$ is greater than $\sigma_j$. So $c_i m/p \le N_i \le c_i m/p + m/p - 1$; this also holds when $c_i = p$, because then $N_i = m$ and $m/p \ge 1$. For the processor that owns the sample $\sigma_j$, that sample is its sample number $c_i$, so $N_i = c_i m/p$ exactly. Summing over $i$, the number $N(\sigma_j)$ of keys at most $\sigma_j$ satisfies

$$
jm \le N(\sigma_j) \le jm + (p - 1)\left(\frac{m}{p} - 1\right).
$$

With $N(\sigma_0) = 0$ and $N(\sigma_p) = pm$, both bounds also hold for $j = 0$ and $j = p$. Bucket $j$ has $N(\sigma_j) - N(\sigma_{j-1}) \le jm + (p-1)(m/p - 1) - (j - 1)m = 2m - m/p - p + 1$ keys. $\square$

The bound is tight. For $p = 2$ and the blocks $[0, 1, 2, 6]$ and $[3, 4, 5, 7]$, the samples are $1, 6$ and $4, 7$, the splitter is $4$, and processor $0$ receives the $5 = 2 \cdot 4 - 2 - 2 + 1$ keys $0, 1, 2, 3, 4$.

**Cost.** $S = 4$. With $n = pm$ and merges done pairwise,

$$
W = O\!\left(\frac{n}{p}\log\frac{n}{p} + p^2 \log p + \frac{n}{p} \log p\right), \qquad H \le p(p-1) + (p-1)^2 + 2\frac{n}{p}.
$$

For $n \ge p^3$ we have $p^2 \le n/p$, and the cost is $O\!\left(\frac{n}{p}\log n\right) + O\!\left(\frac{n}{p}\right)g + 4L$: the work is optimal for a comparison sort, the communication is a constant number of words per key, and the number of supersteps is a constant.

## References
