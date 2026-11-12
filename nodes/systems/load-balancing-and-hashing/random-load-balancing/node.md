---
tag: FXC04X
kind: algorithm
slug: random-load-balancing
name: Random load balancing
aliases:
- uniform random dispatch
area: systems/load-balancing-and-hashing
level: intro
summary: "Send each request to a server drawn uniformly at random. It needs no state, but n requests on n servers give a busiest server near ln n / ln ln n."
solves: [load-balancing-problem]
model: word-ram
complexity:
  vars: {n: the number of servers, m: the number of requests}
  time: {worst: O(1)}
  space: {extra: O(1)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1986
  people: [Derek L. Eager, Edward D. Lazowska, John Zahorjan]
  note: Random placement is folklore. Eager, Lazowska and Zahorjan used it in 1986 as the baseline for adaptive load sharing, and the balls into bins analysis gives its maximum load.
prereqs: [load-balancing-problem, balls-into-bins]
see_also: [weighted-random-load-balancing, round-robin-load-balancing, power-of-two-choices, least-connections, load-balancer, balls-into-bins-max-load, consistent-hashing, source-ip-hash]
sources:
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 5, Sections 5.2 and 5.4 (balls into bins, the maximum load ln n / ln ln n and the Poisson approximation)
  - paper: doi:10.1109/71.963420
    title: Michael Mitzenmacher, The power of two choices in randomized load balancing, IEEE Transactions on Parallel and Distributed Systems 12(10), 2001
    locator: pp. 1094 to 1104, the supermarket model; with one choice each queue is M/M/1 and the tail is lambda^i
  - paper: "Derek L. Eager, Edward D. Lazowska and John Zahorjan, Adaptive load sharing in homogeneous distributed systems, IEEE Transactions on Software Engineering 12(5), 1986"
    locator: pp. 662 to 675, the Random policy as the baseline against threshold and shortest queue policies
---

Random load balancing sends each request to a server drawn uniformly at random, independently of all other requests. It is the simplest dispatch rule for the [load balancing problem](/load-balancing-problem/): it keeps no state, needs no load reports, and many dispatchers can use it at once without coordination. Each server gets $m/n$ requests on average, but the luck of the draw makes some servers much busier: with $n$ requests on $n$ servers the busiest server holds about $\ln n/\ln\ln n$ requests ([maximum load of balls into bins](/balls-into-bins-max-load/)). A weighted form draws server $i$ with probability proportional to its capacity. [Round robin](/round-robin-load-balancing/) gives exact balance but needs a counter, and [two choices](/power-of-two-choices/) cut the maximum to about $\ln\ln n/\ln 2$.

## In plain words

Each request rolls a die with one face per server and goes to the server that comes up. Nobody needs to remember anything or ask any server how busy it is. On average every server gets the same number of requests.

The average hides bad luck. Some faces come up more often than others in any run, so a few servers get more than their share while others sit idle. With many servers, the busiest one gets a few times the average. If servers are of different size, use a die whose faces have sizes in proportion to the server capacity.

## The problem

There are $n$ servers and a stream of requests. Each request must go to one server when it arrives. In the simplest model all requests are equal, the dispatcher knows nothing about the current loads, and the goal is a small maximum load, or a small waiting time when requests also finish. Servers may have known capacities $w_0, \ldots, w_{n-1}$, and then the goal is a load in proportion to capacity.

## The algorithm

```pseudo id=main
RANDOM-DISPATCH(load)                       ▷ load[0 .. n − 1] holds the request counts
L1  s ← RANDOM(0, n − 1)                     ▷ uniform and independent
L2  load[s] ← load[s] + 1; return s
WEIGHTED-PICK(prefix)                       ▷ prefix[i] = w[0] + ... + w[i], W = prefix[n − 1]
L3  u ← W · RANDOM-REAL()                    ▷ uniform in [0, W)
L4  return the least i with prefix[i] > u   ▷ binary search
```

RANDOM-DISPATCH is the uniform rule. WEIGHTED-PICK is the form for servers of different capacity: it builds the prefix sums of the weights once, in $O(n)$ time, and then each pick is one random number and one [binary search](/binary-search/). Server $i$ owns the interval $[prefix[i-1], prefix[i])$ of length $w_i$, so a uniform point falls in it with probability $w_i/W$. The page on [weighted random load balancing](/weighted-random-load-balancing/) treats the weighted policy in a load balancer.

## Example

**Uniform.** Four servers, twelve equal requests. A seeded run (Python `random.Random(3)`) sends them to the servers with counts $2, 4, 2, 4$. The mean is 3 per server, and the busiest server has 4. [Round robin](/round-robin-load-balancing/) would give $3, 3, 3, 3$.

**Weighted pick.** Weights $w = (1, 2, 3, 4)$, so $prefix = (1, 3, 6, 10)$ and $W = 10$. The intervals of the servers are $[0, 1)$, $[1, 3)$, $[3, 6)$ and $[6, 10)$.

| RANDOM-REAL() | $u$ | least $i$ with $prefix[i] > u$ | server |
| --- | --- | --- | --- |
| 0.47 | 4.7 | $prefix[2] = 6 > 4.7$ | 2 |
| 0.05 | 0.5 | $prefix[0] = 1 > 0.5$ | 0 |
| 0.10 | 1.0 | $prefix[1] = 3 > 1.0$ | 1 |
| 0.99 | 9.9 | $prefix[3] = 10 > 9.9$ | 3 |

With 100000 requests (seed 4) the counts are 9941, 20145, 29951 and 39963, close to the shares 10, 20, 30 and 40 percent.

**The busiest server.** With $n$ requests on $n$ servers, 200 seeded runs each (seed 5):

| $n$ | mean of the maximum load | range | $\ln n/\ln\ln n$ |
| --- | --- | --- | --- |
| 100 | 4.22 | 3 to 7 | 3.03 |
| 1000 | 5.52 | 4 to 8 | 3.57 |

The average load is 1 in both cases. The maximum is several times larger and grows with $n$, slowly.

**Queues.** With Poisson arrivals at 90 percent of capacity and exponential service, each server is an M/M/1 queue with mean $0.9/(1 - 0.9) = 9$ requests. A simulation of 50 servers (seed 6, 300000 events after 30000 events of warm-up) gives a mean of 8.73 per server.

## Correctness

Each call of RANDOM-DISPATCH sends the request to server $j$ with probability exactly $1/n$, and the $m$ calls are independent, so the loads have the multinomial law with mean $m/n$ each (Lemma 1 of the proof). WEIGHTED-PICK returns $i$ exactly when $u$ falls in $[prefix[i-1], prefix[i])$, an interval of length $w_i$, so it returns $i$ with probability $w_i/W$ and never returns a server of weight 0 (Lemma 2). The quality of the rule is the law of the maximum load, which is the [balls into bins](/balls-into-bins/) law (Lemma 3). The proof file also shows that round robin is exact and that each queue under random dispatch is M/M/1.

## Complexity

- **Time per request.** $O(1)$ for the uniform rule in the [word RAM](/word-ram/). $O(\log n)$ for the weighted pick, after $O(n)$ time to build the prefix sums.
- **Space.** No state for the uniform rule beyond $n$. $O(n)$ for the prefix sums of the weighted rule.
- **Maximum load, $m = n$.** $(1 + o(1))\ln n/\ln\ln n$ with high probability.
- **Maximum load, $m \ge n\ln n$.** $m/n + \Theta(\sqrt{m\ln n/n})$ with high probability. The gap to the mean grows with $m$, while its ratio to the mean tends to 0.
- **Queues.** At load $\lambda < 1$ each server is an M/M/1 queue: mean $\lambda/(1-\lambda)$ requests, and a fraction $\lambda^i$ of servers hold at least $i$ requests. With two choices the fraction is $\lambda^{2^i - 1}$.

## Properties

- **Online and stateless.** A request is placed when it arrives, from a random number alone. Many dispatchers can share the servers without talking to each other.
- **Fair in expectation.** Each server has the same expected load, or a load in proportion to its weight.
- **Not sticky.** Two requests of the same client go to unrelated servers. Use a hash, such as [source IP hash](/source-ip-hash/) or [consistent hashing](/consistent-hashing/), when a key must stay on one server.
- **Oblivious to the loads.** The rule never reads a load, so it cannot correct bad luck. A server that falls behind stays behind until its queue drains.

## Variants and improvements

- **Weighted random.** Draw server $i$ with probability $w_i/W$, as above. Walker's alias method gives $O(1)$ time per pick after $O(n)$ preparation.
- **Power of two choices.** Draw two servers and send the request to the less loaded one. The maximum load falls to $\ln\ln n/\ln 2 + O(1)$ ([power of two choices](/power-of-two-choices/)).
- **Round robin.** Send request $t$ to server $t \bmod n$. Each server gets $\lfloor m/n \rfloor$ or $\lceil m/n \rceil$ requests, which is exact balance for equal requests, but the dispatcher keeps a counter and several dispatchers must share it or accept some imbalance ([round robin load balancing](/round-robin-load-balancing/), [weighted round robin](/weighted-round-robin/)).
- **Least connections.** Read every load and pick the least ([least connections](/least-connections/)). This is the best balance but needs a full view of the loads.

## When to use it

Use random dispatch when many independent dispatchers share a pool and cannot share a counter or load reports, when requests are short and many, so the averages settle quickly, or as the baseline to compare other policies with. For equal requests through one dispatcher, round robin is better at the same cost. When the loads can be probed, two choices is much better for a small extra cost. Do not use it when a session or a cache key must stay on one server.

## Pitfalls

- **A poor random source.** A generator shared by threads without care, or one seeded with the same value in every dispatcher, makes all dispatchers pick the same servers. Seed each dispatcher on its own.
- **Modulo bias.** Taking a 32-bit random number mod $n$ favors the low indices slightly when $n$ does not divide $2^{32}$. Use a library call that draws a uniform index, such as `randrange`.
- **Expecting exact balance.** The loads differ by about $\sqrt{m/n}$ even when every request is equal. Small pools and short runs show this most.
- **Unequal requests.** Random dispatch balances the count of requests, not the work. A few heavy requests can overload one server.
- **Zero weights and rounding.** In the weighted form a server with weight 0 must never be picked, and $u$ can round up to $W$. Search with "greater than", not "at least", and clamp the result to the last server.

## Implementations

The Python file has the uniform rule, the weighted pick by binary search on prefix sums, round robin as the baseline, and a simulation of random dispatch into queues. The tests check the weighted trace above, the frequencies, the exact balance of round robin and the maximum load of the uniform rule against $\ln n/\ln\ln n$.

## History

Random placement is folklore and appears in early studies of distributed systems as the baseline policy. Eager, Lazowska and Zahorjan in 1986 compared it with policies that use load information and found that a little information gives most of the gain. The law of its maximum load is the balls into bins law, with Gonnet's analysis of hash tables in 1981 and the sharp bounds of Raab and Steger in 1998. Mitzenmacher's analysis of two choices in 1996 used random dispatch, with its M/M/1 queues, as the point of comparison.

## References
