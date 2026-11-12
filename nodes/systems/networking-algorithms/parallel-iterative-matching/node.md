---
tag: V6ZQKP
kind: algorithm
slug: parallel-iterative-matching
name: Parallel iterative matching
aliases:
- PIM
- PIM switch scheduler
area: systems/networking-algorithms
level: advanced
summary: "Randomized crossbar scheduler: inputs request, outputs grant at random, inputs accept at random. Each round resolves 3/4 of open requests on average, so O(log N) rounds give a maximal matching."
solves: [switch-scheduling]
model: word-ram
complexity:
  vars: {n: the number of ports}
  time: {worst: O(n^3), expected: O(n^2 log n)}
  space: {extra: Θ(n^2)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1993
  people: [Thomas E. Anderson, Susan S. Owicki, James B. Saxe, Charles P. Thacker]
  note: Anderson, Owicki, Saxe and Thacker designed PIM for the AN2 switch of the DEC Systems Research Center and analyzed it in ACM TOCS in 1993.
prereqs: [switch-scheduling, maximal-matching, markov-inequality]
see_also: [islip, birkhoff-von-neumann-decomposition, bipartite-matching, hopcroft-karp, maximum-weight-matching, randomized-algorithm]
sources:
  - paper: doi:10.1145/161541.161736
    title: "Thomas E. Anderson, Susan S. Owicki, James B. Saxe and Charles P. Thacker, High-speed switch scheduling for local-area networks, ACM Transactions on Computer Systems 11(4) (1993), 319-352"
    locator: the request, grant and accept phases, the lemma that each iteration resolves on average at least 3/4 of the remaining unresolved requests, the O(log N) bound on the expected number of iterations, and simulations of the AN2 switch
  - paper: doi:10.1109/90.769767
    title: "Nick McKeown, The iSLIP scheduling algorithm for input-queued switches, IEEE/ACM Transactions on Networking 7(2) (1999), 188-201"
    locator: the description of PIM as the starting point of iSLIP, its throughput of about 63% with one iteration under uniform traffic, and the cost of random choice in hardware
  - book: isbn:9780120884773
    title: George Varghese, Network Algorithmics, Morgan Kaufmann, 2005
    locator: Chapter 13, the section on parallel iterative matching
  - book: isbn:9780122007514
    title: William J. Dally and Brian Towles, Principles and Practices of Interconnection Networks, Morgan Kaufmann, 2004
    locator: Chapter 19, allocation (separable allocators, PIM and iSLIP)
---

Parallel iterative matching (PIM) finds a [maximal matching](/maximal-matching/) between the inputs and the outputs of a crossbar switch, for one time slot of [switch scheduling](/switch-scheduling/). Each iteration has three parallel steps: every unmatched input requests all unmatched outputs that it has cells for, every requested output grants one request at random, and every input that got grants accepts one at random. Anderson, Owicki, Saxe and Thacker (1993) proved that one iteration resolves, in expectation, at least 3/4 of the requests that are still open, so about $\log_2 N$ iterations give a maximal matching on average. It is a fast hardware replacement for a [maximum-size](/hopcroft-karp/) or [maximum-weight](/maximum-weight-matching/) matching, which are too slow to compute in one slot.

## In plain words

Think of a dance with the same number of leaders and followers. Each leader who has no partner yet calls out to every free follower that leader likes. Each free follower who hears calls picks one caller at random and says yes to that caller. A leader who gets several yes answers picks one of them at random, and the two become a pair. The others try again in the next round.

Each round removes many of the open calls: either the follower gets a partner, or the leader who got the yes already had another yes. After a few rounds, no free leader likes a free follower. The pairs are then a matching that cannot grow by adding a pair, although a different choice might have made more pairs.

## The problem

The input is one slot of an $N \times N$ input-queued switch with virtual output queues: a request matrix $req \in \{0,1\}^{N \times N}$, where $req[i][j] = 1$ when input $i$ has a cell for output $j$. The output is a matching $M$: a set of pairs $(i, j)$ with $req[i][j] = 1$ and no port in two pairs. PIM aims for a maximal $M$, so that no request joins an unmatched input to an unmatched output. The goal of the switch, throughput over many slots, is the [switch scheduling](/switch-scheduling/) problem.

## The algorithm

```pseudo id=main
PIM(req, N)                                   ▷ req[i][j] = 1: input i has a cell for output j
L1  mark all inputs and all outputs unmatched
L2  while some req[i][j] = 1 has i and j unmatched do
L3      each unmatched input i sends a request to each unmatched output j with req[i][j] = 1
L4      for each unmatched output j that got requests, in parallel do
L5          grant one requesting input, chosen uniformly at random
L6      for each input i that got grants, in parallel do
L7          accept one grant, from output j chosen uniformly at random
L8          match i to j
L9  return the matched pairs
```

In hardware, the loop of line L2 runs a fixed number of iterations, for example 3 or 4, and the slot uses the pairs found so far. Each phase is one parallel step: the $N$ output arbiters of lines L4 and L5 work at the same time, and so do the $N$ input arbiters of lines L6 to L8. An input that got no grant and an output whose grant was not accepted stay unmatched and try again. Pairs never break up in later iterations.

## Example

Take $N = 4$ with these requests (inputs are rows, outputs are columns, numbered from 0):

| | out 0 | out 1 | out 2 | out 3 |
| --- | --- | --- | --- | --- |
| in 0 | 1 | 1 | 0 | 0 |
| in 1 | 1 | 0 | 1 | 0 |
| in 2 | 0 | 1 | 1 | 1 |
| in 3 | 0 | 0 | 0 | 1 |

There are 8 requests. One run (seed 0 of the implementation) goes as follows.

| iteration | requests received (by output) | grants received (by input) | accepted | unresolved after |
| --- | --- | --- | --- | --- |
| 1 | out 0: in 0, in 1; out 1: in 0, in 2; out 2: in 1, in 2; out 3: in 2, in 3 | in 1: out 0, out 2; in 2: out 1; in 3: out 3 | (1, 2), (2, 1), (3, 3) | 1 |
| 2 | out 0: in 0 | in 0: out 0 | (0, 0) | 0 |

In iteration 1, outputs 0 and 2 both grant input 1, and input 0 gets no grant. Input 1 accepts output 2, so output 0 stays unmatched. One request, (0, 0), is still open, and iteration 2 matches it. The result $\{(0,0), (1,2), (2,1), (3,3)\}$ is a perfect matching. Other runs stop with three pairs. Seed 3 finds $\{(0,0), (2,2), (3,3)\}$ in one iteration; it is maximal, because input 1 wants only outputs 0 and 2, and both are taken. Seed 5 finds $\{(1,0), (2,1), (3,3)\}$, and input 0 is left out in the same way.

## Correctness

The pairs always form a matching, because each output grants at most once and each input accepts at most once, and matched ports drop out. While a request joins two unmatched ports, the output of that request grants someone, and that input accepts some grant. So each iteration adds a pair, the loop stops after at most $N$ iterations, and at the stop the matching is maximal by the loop test of line L2.

The speed comes from the key lemma. Fix an output $j$ with $k$ open requests, and fix the grants of the other outputs. Let $q$ of the $k$ requesters get no other grant. If $j$ grants one of these $q$, the grant is accepted and all $k$ requests to $j$ close. Otherwise at most $q$ requests to $j$ stay open, since every other requester got a grant and is matched. So the expected number left open is at most $\frac{k-q}{k}q \le k/4$. The full proofs are in the correctness proof below.

## Complexity

Let $R_t$ be the number of open requests after $t$ iterations, with $R_0 \le N^2$.

- **Iterations, expected.** By the lemma, $\mathbb{E}[R_t] \le N^2/4^t$. With the Markov inequality, the expected number of iterations is at most $\lceil \log_2 N \rceil + 4/3$. For $N = 16$ that is 5.33. In seeded runs with all requests present (seed 7), the mean is 3.38 iterations for $N = 16$ and 4.73 for $N = 64$, with a maximum of 5 and 6.
- **Iterations, worst case.** Each iteration adds at least one pair, so there are at most $N$ iterations.
- **Work.** One iteration looks at each request once, $O(N^2)$ work on a sequential machine. So the time is $O(N^3)$ in the worst case and $O(N^2 \log N)$ in expectation over the random choices, on the word RAM. The request lists take $\Theta(N^2)$ space.
- **Hardware time.** In a switch, each phase is $N$ arbiters working in parallel. Each arbiter picks one of up to $N$ requests, which a tree circuit does in $O(\log N)$ gate delays. So an iteration takes $O(\log N)$ gate delays, and the slot needs $O(\log^2 N)$ in expectation.

The 3/4 bound is a bound on the expectation, not on each run. In seeded runs with $N = 4$ and all requests present, the first iteration resolved as little as 44% of the requests in a bad run, while the mean over all iterations of 2000 runs was 88%.

## Properties

- **Randomized.** The grant and accept choices are random. The random choice is what gives the 3/4 bound without any memory between slots.
- **Maximal, not maximum.** A maximal matching has at least half the edges of a maximum matching, and PIM may stop at a smaller one than the maximum.
- **One iteration is weak.** With all $N^2$ requests present, each output grants a uniform input, and an input is matched when at least one output grants it, which has probability $1 - (1 - 1/N)^N$, which tends to $1 - 1/e \approx 0.632$. So PIM with a single iteration caps the throughput near 63% under uniform load (McKeown 1999).
- **Stateless.** Nothing is kept from one slot to the next. This makes PIM robust to errors but unable to remember fairness.

## Variants and improvements

- **[iSLIP](/islip/).** Replace the random choices by round-robin pointers that move only when a first-iteration grant is accepted. The pointers then spread out, and one iteration gives 100% throughput under uniform Bernoulli traffic. It needs no random number generators.
- **Weighted PIM.** Grant with probability proportional to a weight, such as a reserved rate, so that the switch can give bandwidth guarantees. Anderson et al. describe statistical matching for reserved traffic in the AN2 paper.
- **Fixed iteration count.** Real switches stop after a small fixed number of iterations, which costs a little matching size in exchange for a fixed slot time.
- **Separable allocators.** In on-chip routers, the same input-first or output-first allocation with random or round-robin arbiters assigns virtual channels and switch ports.

## When to use it

Use PIM when the scheduler must finish in a few gate delays and a maximal matching is good enough. Under uniform traffic it gets close to the throughput of a maximum matching with 3 or 4 iterations. Use [iSLIP](/islip/) instead when random number generation in each arbiter is costly, or when one iteration must already give high throughput. Use a [maximum-weight matching](/maximum-weight-matching/) in analysis or in slow switches, when 100% throughput for all admissible loads is needed. Use a [Birkhoff-von Neumann](/birkhoff-von-neumann-decomposition/) schedule when the rates are known in advance.

## Pitfalls

- **Breaking pairs.** Line L8 makes a pair final. An implementation that lets a matched input request again in line L3 can undo pairs and lose the progress bound.
- **Requests to matched outputs.** Line L3 must skip matched outputs. If matched outputs keep granting, they waste grants, and the 3/4 lemma no longer holds.
- **Reading 3/4 as a per-run bound.** The lemma is about the expectation. A single iteration can resolve less than half of the requests.
- **Running one iteration and expecting maximality.** With one iteration, the matching is often not maximal and the throughput is near 63%.
- **Unfair choices with weak random sources.** A biased random number generator in the arbiters gives a biased schedule and can starve a queue.

## Implementations

## History

Anderson, Owicki, Saxe and Thacker developed PIM for AN2, an ATM-style local-area network switch built at the DEC Systems Research Center, and published the algorithm and its analysis in ACM Transactions on Computer Systems in 1993. McKeown's iSLIP (1999) kept the structure of request, grant and accept and replaced the random choices by round-robin pointers.

## References
