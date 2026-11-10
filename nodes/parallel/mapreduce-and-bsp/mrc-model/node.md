---
tag: 1TX2QG
kind: model
slug: mrc-model
name: MapReduce class (MRC) model
aliases:
- MRC
- MapReduce complexity model
area: parallel/mapreduce-and-bsp
level: research
summary: A model of MapReduce in which each machine has memory sublinear in the input and the cost is the number of rounds. MRC^i is the class of problems solved in O(log^i n) rounds.
history:
  year: 2010
  people: [Howard Karloff, Siddharth Suri, Sergei Vassilvitskii]
  note: Karloff, Suri and Vassilvitskii defined MRC and DMRC at SODA 2010 and related them to NC and PRAM.
prereqs: [mapreduce-model, nc]
see_also: [bsp-model, pram-model, crew-pram, minimum-spanning-tree, iterative-mapreduce, mapreduce-communication-lower-bounds, round-complexity, congested-clique-model]
sources:
  - paper: doi:10.1137/1.9781611973075.76
    title: "Howard Karloff, Siddharth Suri and Sergei Vassilvitskii, A model of computation for MapReduce, SODA 2010"
    locator: pp. 938-948; Definition 3.1 (MRC^i and DMRC^i), Section 3.1.1 (the number of machines), Theorem 4.1 (DMRC and NC), Section 5 (minimum spanning tree, Lemma 5.1 and Theorem 5.1), Section 6.2 (s-t connectivity), Theorem 7.1 (PRAM simulation)
  - paper: "Michael T. Goodrich, Nodari Sitchinava and Qin Zhang, Sorting, searching, and simulation in the MapReduce framework, ISAAC 2011 (arXiv 1101.1902)"
    locator: the simulation of CRCW PRAM algorithms and sorting in O(log_M N) rounds, with M the memory of a reducer
  - paper: doi:10.1145/2463664.2465224
    title: "Paul Beame, Paraschos Koutris and Dan Suciu, Communication steps for parallel query processing, PODS 2013"
    locator: the massively parallel communication model, with load and rounds as its costs
---

The MapReduce class (MRC) model is a theoretical model of [MapReduce](/mapreduce-model/), defined by Karloff, Suri and Vassilvitskii in 2010. A computation is a sequence of map and reduce rounds. Each mapper and reducer has memory $O(n^{1-\epsilon})$ for an input of size $n$, so no single machine can hold the input, and the cost of an algorithm is its number of rounds. The class $\mathrm{MRC}^i$ contains the problems that can be solved in $O(\log^i n)$ rounds under these limits.

## The machine

The input is a set of key-value pairs of total size $n$ words. Fix a constant $\epsilon$ with $0 < \epsilon < 1$.

| Symbol | Meaning |
|---|---|
| $n$ | the size of the input, in words |
| $s$ | the memory of one mapper or reducer, $s = O(n^{1-\epsilon})$ |
| $R$ | the number of rounds |
| $\mu_r$, $\rho_r$ | the map and reduce functions of round $r$ |

**Rounds.** Round $r$ applies the mapper $\mu_r$ to each key-value pair separately, and each call outputs a multiset of key-value pairs. The system groups all output pairs by key (the [shuffle](/shuffle-phase/)). Then the reducer $\rho_r$ runs once per key on the list of values of that key and outputs a multiset of key-value pairs, which is the input of round $r + 1$.

**Limits (Definition 3.1 of the paper).** An algorithm is in $\mathrm{MRC}^i$ if, for some $\epsilon > 0$:

1. each $\mu_r$ and each $\rho_r$ is a RAM program that uses $O(n^{1-\epsilon})$ space and time polynomial in $n$, on every call;
2. the total size of the output of all mappers in one round is $O(n^{2-2\epsilon})$;
3. the number of rounds is $O(\log^i n)$;
4. the output is correct with probability at least $3/4$.

$\mathrm{DMRC}^i$ is the same class for deterministic algorithms. A reducer that holds all values of one key needs that list to fit in $O(n^{1-\epsilon})$ space, so no key may receive more.

**Machines.** The paper takes $\Theta(n^{1-\epsilon})$ machines, each with $O(n^{1-\epsilon})$ memory (Section 3.1.1). Many mapper and reducer calls share a machine, and the total memory is $O(n^{2-2\epsilon})$, which is the reason for limit 2. Both limits are sublinear in $n$ on purpose: if one machine could hold the input, every problem in P would take one round, and if there were $\Omega(n)$ machines with $O(1)$ memory, the model would be a PRAM with expensive steps.

## What it counts

The main cost is the number of rounds $R$. Within a round, the work of a single reducer is free as long as it is polynomial, and the shuffle is free as long as the limits hold. The reasons are practical: in a real cluster, a round means starting a job, writing the map output to disk and moving it over the network, so a few rounds of heavy work are faster than many light ones.

The space limits are hard constraints, not costs. So an MRC analysis has two parts: show that every reducer input fits in $O(n^{1-\epsilon})$ and that the round output fits in $O(n^{2-2\epsilon})$, then count the rounds. Later models, such as the massively parallel communication (MPC) model of Beame, Koutris and Suciu, keep the round count but also charge the load, the largest number of words that one machine receives in a round. The page on [communication lower bounds](/mapreduce-communication-lower-bounds/) shows the trade between the reducer size and the total communication in a single round.

**Example: the sum of $n$ numbers.** Let $s = n^{1-\epsilon}$. Round 1 sends number $x_j$ to the key $\lfloor j/s \rfloor$, so each of the $n^{\epsilon}$ reducers adds $s$ numbers. Round 2 sends the $n^{\epsilon}$ partial sums to one key. That reducer fits when $n^{\epsilon} \le n^{1-\epsilon}$, that is, $\epsilon \le 1/2$. For larger $\epsilon$, a tree with fan-in $s$ needs $\lceil 1/(1-\epsilon) \rceil$ rounds, a constant, so the sum is in $\mathrm{DMRC}^0$. For $n = 10^6$ and $s = 10^4$ this is two rounds: 100 reducers of $10^4$ numbers each, then one reducer of 100 numbers.

**A matching lower bound.** Say that an output word depends on an input word if changing the input word can change the output word. A mapper call reads one pair, so each word it outputs depends only on that pair. A reducer call reads at most $s$ words, so each word it outputs depends on at most $s$ words of the previous round's output. By induction on $r$, a word output in round $r$ depends on at most $s^r$ input words. The sum depends on all $n$ inputs, so $s^R \ge n$ and $R \ge \log_s n = 1/(1-\epsilon)$. The tree above meets this bound, up to rounding.

## Relation to other models

- [MapReduce](/mapreduce-model/). MRC is the system with its limits written down. It ignores the cost of a round and the [combiner](/combiner/), which in a real system makes a key with a very long value list possible.
- [BSP](/bsp-model/). A round is a [superstep](/superstep/) in which the shuffle is the communication. MRC fixes the memory per machine and counts only the supersteps; BSP also charges $g$ per word and $L$ per superstep.
- [PRAM](/pram-model/) and [NC](/nc/). Theorem 7.1 of the paper: a [CREW PRAM](/crew-pram/) algorithm with $O(n^{2-2\epsilon})$ processors and total memory that runs in $t$ steps can be run in $O(t)$ rounds of DMRC. Each round sends each memory read and write as a key-value pair keyed by the address. So such an algorithm in $\mathrm{NC}^i$ gives a $\mathrm{DMRC}^i$ algorithm. Goodrich, Sitchinava and Zhang noted that a concurrent read of one cell by many processors sends many pairs to one key, which can break the space limit, and they gave a simulation of CRCW PRAM algorithms in $O(t \log_s P)$ rounds by building trees of fan-in $s$ for such reads and writes, with $P$ processors.
- The other direction (Theorem 4.1 of the paper): if $\mathrm{P} \ne \mathrm{NC}$, then DMRC is not contained in NC. A reducer may run any polynomial-time program on its $O(n^{1-\epsilon})$ words, so a P-complete problem whose input is padded to a polynomially larger size is solved in one round, but it cannot be in NC unless the original problem is.
- MPC and the [congested clique](/congested-clique-model/). The MPC model is the usual modern form of MRC: $p$ machines, each with $s$ words of memory, and rounds as the cost. With $s = n$ and $p = n$, for a graph with $n$ vertices, MPC is close to the congested clique of distributed computing, and [round complexity](/round-complexity/) results move between the two.

## Known results in the model

**Minimum spanning tree of a dense graph (Section 5).** Let the graph have $N$ vertices and $m = N^{1+c}$ edges with distinct weights, for a constant $c > 0$. Split the vertices into $k = N^{c/2}$ parts $V_1, \ldots, V_k$ at random.

1. Round 1: for each pair $i < j$, one reducer gets the edges with both ends in $V_i \cup V_j$, computes their minimum spanning forest, and outputs its edges.
2. Round 2: one reducer gets all output edges and computes their [minimum spanning tree](/minimum-spanning-tree/).

*Correctness.* Each edge $(u, v)$ lies in at least one pair subgraph. If round 1 drops it, then $(u, v)$ is the heaviest edge on a cycle of that subgraph, so it is the heaviest edge on a cycle of the whole graph and, by the cycle property, it is not in the minimum spanning tree. So every edge of the tree survives round 1, and round 2 finds it. $\square$

*Space.* A pair subgraph has about $2N/k$ vertices and, for random parts, about $(2/k)^2 m = 4N$ edges with high probability. Its forest has fewer than $2N/k$ edges, so round 2 gets fewer than $\binom{k}{2} \cdot 2N/k < kN = N^{1+c/2}$ edges. This is $m^{(1+c/2)/(1+c)}$, which is sublinear in the input size $m$. So the minimum spanning tree of a dense graph is in $\mathrm{MRC}^0$ with two rounds.

**Other results.**

- Undirected s-t connectivity in $O(\log n)$ rounds, so in $\mathrm{MRC}^1$ (Section 6.2 of the paper), from a PRAM-style algorithm that merges components.
- Any function that is a sum, minimum or count over all input words in $\lceil 1/(1-\epsilon) \rceil$ rounds, by the tree above, and not fewer.
- Sorting in $O(\log_s n)$ rounds, which is $O(1)$ for $s = n^{1-\epsilon}$ (Goodrich, Sitchinava and Zhang).
- No problem in P is known to need $\omega(\log n)$ rounds in this setting. For graph connectivity, a well-known conjecture states that telling one cycle on $n$ vertices from two cycles on $n/2$ vertices each needs $\Omega(\log n)$ rounds when $s = n^{1-\epsilon}$; it is open.

## References
