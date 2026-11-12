---
tag: JZRZJJ
kind: algorithm
slug: round-robin-load-balancing
name: Round-robin load balancing
aliases:
- RR balancing
- static round-robin balancing
area: systems/load-balancing-and-hashing
level: intro
summary: "Send request k to backend k mod n, skipping backends that are down. O(1) state and exact balance by request count, but blind to request cost and server speed."
solves: [load-balancing-problem]
model: word-ram
complexity:
  vars: {n: the number of backends}
  time: {worst: O(n), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [load-balancer]
see_also: [weighted-round-robin, least-connections, random-load-balancing, power-of-two-choices, round-robin, dns-load-balancing, health-checking, deficit-round-robin]
sources:
  - book: isbn:9781107027503
    title: Mor Harchol-Balter, Performance Modeling and Design of Computer Systems, Queueing Theory in Action, Cambridge University Press, 2013
    locator: Chapter 24, Task Assignment Policies for Server Farms (Random, Round-Robin, Join-the-Shortest-Queue and Least-Work-Left for FCFS server farms, Section 24.1)
  - book: isbn:9781491929124
    title: Betsy Beyer, Chris Jones, Jennifer Petoff and Niall Richard Murphy (eds.), Site Reliability Engineering, How Google Runs Production Systems, O'Reilly, 2016
    locator: Chapter 20, Load Balancing in the Datacenter, the part on simple round robin and why it fails (varying query costs, machine diversity, unpredictable performance factors)
  - url: http://nginx.org/en/docs/http/ngx_http_upstream_module.html
    title: nginx documentation, Module ngx_http_upstream_module
    locator: the upstream directive (weighted round robin is the default method) and the server parameters weight, max_fails and down
  - url: https://docs.haproxy.org/2.8/configuration.html
    title: HAProxy 2.8 Configuration Manual
    locator: Section 4.2, the balance keyword, algorithms roundrobin and static-rr
  - paper: "Wensong Zhang, Linux Virtual Server for Scalable Network Services, Proceedings of the Ottawa Linux Symposium, 2000"
    locator: the section on the scheduling algorithms of IPVS (round robin, weighted round robin, least connection, weighted least connection)
---

Round-robin load balancing is the simplest [load balancer](/load-balancer/) policy: it sends request $k$ to backend $k \bmod n$, and it skips backends that [health checks](/health-checking/) mark as down. It keeps one index of state, it costs $O(1)$ per request, and it balances the *number* of requests exactly: over any window of $m$ requests each backend gets $\lfloor m/n \rfloor$ or $\lceil m/n \rceil$ of them. It does not look at the cost of a request or the speed of a backend, so with request sizes that vary a lot it can put long queues on one backend while the others are idle.

## In plain words

A teacher hands out exam papers to three graders. The first paper goes to the first grader, the second to the second, the third to the third, and the fourth again to the first. Each grader gets the same number of papers, and the teacher needs to remember only who is next.

The method is fair in the number of papers, but not in the work. If one paper is a thick thesis and the next ones are single pages, the grader who got the thesis is busy for a long time, and the rotation keeps sending that grader new papers on schedule. A grader who is sick is skipped until the teacher hears that the grader is back.

## The problem

The model has $n$ backends $B[0], \ldots, B[n-1]$ and a stream of requests that arrive one at a time. The balancer must choose a backend for each request when it arrives, without knowing the future (an online choice). Round robin uses no information about the requests or the backends, except a flag $up[j]$ for each backend from [health checking](/health-checking/). This is one policy for the [load balancing problem](/load-balancing-problem/).

There are two different measures of success. Balance by count: the number of requests per backend. Balance by work or by delay: the total service time per backend, or the response time of each request. Round robin gives an exact guarantee for the first one in any arrival model, including an adversarial one. For the second one there is no worst-case guarantee, and it depends on the arrival process and the distribution of request sizes.

## The algorithm

The state is the index $i$ of the next backend to try. A call returns one backend, or none when all are down.

```pseudo id=main
RR-PICK(B, up)                  ▷ backends B[0..n−1], flags up[0..n−1], state i
L1  repeat n times
L2      j ← i
L3      i ← (i + 1) mod n
L4      if up[j] then return B[j]
L5  return none                ▷ every backend is down
```

When all backends are up, the loop of line L1 runs once: line L2 takes the current index, line L3 moves it on, and line L4 returns the backend. When some backends are down, the loop skips them in order, and the next call starts just after the backend that was returned. If no backend is up, the loop makes one full turn, leaves $i$ where it was, and line L5 returns none, so the caller can fail the request or try a [failover](/failover/) pool.

In a multi-threaded proxy, line L3 is an atomic fetch-and-add on a shared counter, and the index is the counter modulo $n$. Each worker thread may also keep its own counter, which gives exact balance per thread and almost exact balance overall.

## Example

Three backends, all up. Eight requests arrive at times 0 to 7. Their sizes, in seconds of work, are 9, 1, 1, 9, 1, 1, 9, 1. Each backend is one FCFS server. Round robin sends request $k$ to backend $k \bmod 3$.

| request | arrival | size | backend | start | finish | response time |
|---|---|---|---|---|---|---|
| 0 | 0 | 9 | 0 | 0 | 9 | 9 |
| 1 | 1 | 1 | 1 | 1 | 2 | 1 |
| 2 | 2 | 1 | 2 | 2 | 3 | 1 |
| 3 | 3 | 9 | 0 | 9 | 18 | 15 |
| 4 | 4 | 1 | 1 | 4 | 5 | 1 |
| 5 | 5 | 1 | 2 | 5 | 6 | 1 |
| 6 | 6 | 9 | 0 | 18 | 27 | 21 |
| 7 | 7 | 1 | 1 | 7 | 8 | 1 |

The counts are 3, 3 and 2, as balanced as 8 requests on 3 backends can be. But the long requests come every third arrival, and the rotation also has period 3, so all three long requests land on backend 0 and wait behind each other. The total response time is 50, a mean of 6.25. [Least connections](/least-connections/) on the same input sends requests 3 and 6 to idle backends, and its total is 34, a mean of 4.25.

## Correctness

Each call returns the first backend that is up at or after the index $i$, in cyclic order, and moves $i$ to just after it; if no backend is up, it returns none and leaves $i$ unchanged. The invariant of line L1 is: at the start of pass $t$, $i = (i_0 + t - 1) \bmod n$ and the $t - 1$ backends before it in cyclic order are down. From this, when all backends stay up, call $k$ returns $B[(i_0 + k) \bmod n]$, so each window of $m$ calls gives each backend $\lfloor m/n \rfloor$ or $\lceil m/n \rceil$ requests. The same holds with $u$ in place of $n$ while the set of $u$ up backends does not change. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Time per request.** When the backend at index $i$ is up, line L1 makes one pass, so the cost is $\Theta(1)$. In the worst case the loop scans all $n$ flags, which is $O(n)$; this happens only when many backends are down. A balancer that keeps a separate array of the up backends, rebuilt when a health check changes a flag, makes every pick $\Theta(1)$.
- **Space.** One index, $\Theta(1)$ beyond the pool and its flags.
- **Coordination.** In a shared-memory proxy the only shared write is the increment of line L3. Several balancer instances that do not share state each rotate on their own, and the total stays balanced only on average.

## Properties

- **Exact count balance in any arrival order.** Claim 2 of the proof holds for every request sequence. Random choice ([random load balancing](/random-load-balancing/)) gives only expected balance: with $n$ requests on $n$ backends the busiest one gets about $\ln n / \ln \ln n$ of them (see [balls into bins](/balls-into-bins-max-load/)).
- **Smoother arrivals than random under Poisson traffic.** If requests arrive as a Poisson process of rate $\lambda$, each backend gets every $n$-th request, so its gaps between arrivals are Erlang with $n$ phases and mean $n/\lambda$. These gaps are less variable than the exponential gaps that random splitting gives. With requests of similar size, round robin then has shorter queues than random choice (Harchol-Balter, Chapter 24).
- **Blind to cost and speed.** The policy does not read queue lengths, latencies or request sizes. It sends the same number of requests to a backend that is twice as slow, or that is stuck in a long garbage collection pause.
- **Deterministic and stateless across requests.** It needs no feedback from the backends, so it works for one-way traffic and for a balancer that cannot see responses.

## Variants and improvements

- **[Weighted round robin](/weighted-round-robin/).** Backend $j$ gets $w_j$ turns in each cycle of $\sum_j w_j$ requests, for backends of different capacity.
- **Random start.** Each balancer instance starts at a random index. Without this, many proxies that restart at the same time all send their first requests to backend 0.
- **Per-thread counters.** Each worker thread of a proxy keeps its own index. This avoids a shared atomic counter at the cost of slightly less exact balance.
- **Dynamic and static rotation.** HAProxy has both: `static-rr` is plain rotation over the server list, and `roundrobin` is a weighted rotation whose weights can change while it runs.
- **[DNS round robin](/dns-load-balancing/).** The same rotation of the address list in DNS answers. Caching resolvers weaken it a lot.

Round robin here is a different algorithm from [round-robin CPU scheduling](/round-robin/). The CPU scheduler gives one processor to many processes in time slices of length $q$ and preempts them. The load balancer gives each whole request to one of many servers and never preempts. [Deficit round robin](/deficit-round-robin/) is a third use of the name, for packets on one link, and it counts bytes, not requests.

## When to use it

Use round robin when the requests have similar cost, the backends are alike, and the balancer cannot see backend load, for example a simple TCP proxy or a client library with no feedback. It is also a good default for a short list of backends that each have a deep internal queue. When the request costs vary a lot, use [least connections](/least-connections/) or [power of two choices](/power-of-two-choices/); with heavy-tailed sizes the difference is large. In an event simulation of 4 FCFS backends at load 0.8, with Poisson arrivals and Pareto request sizes of shape 1.5 and mean 1 (20000 requests, seeds 1 to 5), round robin had a mean response time of 9.5 to 23.8 and a 99th percentile of 84 to 711, while least connections had a mean of 2.4 to 5.3 and a 99th percentile of 24 to 48. When the backends differ in speed, use [weighted round robin](/weighted-round-robin/) or [weighted least connections](/weighted-least-connections/).

## Pitfalls

- **A request pattern with the same period as the rotation.** In the example, every third request is long and there are three backends, so every long request goes to the same backend. Batch jobs and clients that send requests in fixed groups can do this. A random start per balancer, or a policy that reads load, breaks the alignment.
- **Counting on the wrong side of the skip.** If line L3 runs only when line L4 fails, the index stays on the returned backend, and every call returns the same backend. Line L3 must advance the index for every backend tried.
- **One rotation per client.** If each client creates a new balancer object for each request, every request starts at index 0 and goes to backend 0. Keep the balancer, or its counter, for the life of the process.
- **Removing a backend from the list.** If the code deletes backend $j$ from the list and keeps $i$, the indices after $j$ shift, and one backend gets two turns in a row. Use the up flags of line L4, or reset $i$ modulo the new length.
- **Long-lived connections.** A balancer that applies round robin per TCP connection balances connections, not requests. With HTTP/2 or gRPC, one connection can carry most of the traffic. See [layer 7 load balancing](/layer-7-load-balancing/).

## Implementations

## History

Rotation over a list of servers is old and has no single inventor that we can source. The Linux Virtual Server project of Wensong Zhang, started in 1998, has round robin and weighted round robin among its first scheduling methods, and nginx and HAProxy use weighted round robin as their default. The queueing comparison of round robin with random assignment and with join-the-shortest-queue for server farms is in Harchol-Balter, Chapter 24.

## References
