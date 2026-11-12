---
tag: MKYZP0
kind: algorithm
slug: least-connections
name: Least connections
aliases:
- least connections balancing
- leastconn
- least_conn
area: systems/load-balancing-and-hashing
level: intro
summary: "Send each new request to the backend with the fewest active connections. In queueing terms this is join the shortest queue, optimal for identical exponential servers."
solves: [load-balancing-problem]
model: word-ram
complexity:
  vars: {n: the number of backends}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [round-robin-load-balancing, queue]
see_also: [weighted-least-connections, power-of-two-choices, least-response-time, peak-ewma, random-load-balancing, bucket-queue, fcfs-scheduling, health-checking]
sources:
  - paper: doi:10.2307/3213271
    title: "Wayne Winston, Optimality of the shortest line discipline, Journal of Applied Probability 14(1), 1977, pages 181 to 189"
    locator: the main result (identical exponential servers, Poisson arrivals, assignment on arrival; joining the shortest queue maximizes the discounted number of service completions)
  - paper: doi:10.2307/3213411
    title: "Richard R. Weber, On the optimal assignment of customers to parallel servers, Journal of Applied Probability 15(2), 1978, pages 406 to 413"
    locator: the main result (general arrivals, service times with a non-decreasing hazard rate; joining the shortest queue maximizes in stochastic order the number served by time t)
  - paper: doi:10.1287/opre.34.1.55
    title: "Ward Whitt, Deciding which queue to join, some counterexamples, Operations Research 34(1), 1986, pages 55 to 62"
    locator: the counterexamples (service time distributions for which joining the shortest queue is not optimal, even when only the queue lengths are known)
  - book: isbn:9781107027503
    title: Mor Harchol-Balter, Performance Modeling and Design of Computer Systems, Queueing Theory in Action, Cambridge University Press, 2013
    locator: Chapter 24, Task Assignment Policies for Server Farms (Random, Round-Robin, JSQ and Least-Work-Left for FCFS and PS server farms)
  - url: https://docs.haproxy.org/2.8/configuration.html
    title: HAProxy 2.8 Configuration Manual
    locator: Section 4.2, the balance keyword, algorithm leastconn (round robin among servers of equal load, advice for long sessions)
  - url: http://nginx.org/en/docs/http/ngx_http_upstream_module.html
    title: nginx documentation, Module ngx_http_upstream_module
    locator: the least_conn directive (added in nginx 1.3.1 by the change log)
---

Least connections is a [load balancer](/load-balancer/) policy that sends each new request or connection to the backend with the fewest active connections. It needs one counter per backend, raised when a connection opens and lowered when it closes. In a queueing model where each backend is a server with its own [queue](/queue/), the active count is the queue length, and least connections is *join the shortest queue* (JSQ). For identical servers with exponential service times, JSQ is optimal among the policies that assign each job on arrival with knowledge of the queue lengths (Winston, 1977; Weber, 1978), but not for every service time distribution (Whitt, 1986). It adapts to requests of different cost without knowing their cost, because a backend that is busy with a long request keeps a high count.

## In plain words

At a supermarket with several checkout lanes, you look at the lanes and join the one with the fewest people. You do not know how full their carts are, but a lane with a slow customer stays long, so new shoppers avoid it.

The balancer does the same. It keeps a count of open requests for each server. A new request goes to the server with the lowest count, and the count goes up. When a request finishes, the count goes down. A server that is stuck on a big request keeps a high count and gets nothing new until it catches up.

## The problem

The model has $n$ backends and a stream of requests that arrive online. Each request occupies a connection on its backend from its start to its end. The balancer sees when each connection opens and closes, but not how long a request will take. The goal is low response time: a request should not wait behind a long request when another backend is idle. For a queueing analysis the arrivals are a Poisson process of rate $\lambda$, each backend is a FCFS server of rate $\mu$, and the load is $\rho = \lambda / (n\mu) < 1$. This is one policy for the [load balancing problem](/load-balancing-problem/).

## The algorithm

The state is the counter $a[j]$ of active connections of each backend, and the flags $up[j]$ from [health checking](/health-checking/).

```pseudo id=main
LC-PICK(B, a, up)                 ▷ counters a[0..n−1], flags up[0..n−1]
L1  best ← none
L2  for j ← 0 to n − 1 do
L3      if up[j] and (best = none or a[j] < a[best]) then best ← j
L4  if best ≠ none then a[best] ← a[best] + 1
L5  return best

LC-DONE(j)                         ▷ a connection to backend j has closed
L6  a[j] ← a[j] − 1
```

Line L3 keeps the first up backend with the smallest count, so ties go to the lowest index. Line L4 counts the new connection at once, before it does any work, so that the next request sees it. Line L6 runs when the response ends or the connection closes. A proxy that pools connections to its backends counts requests in flight instead of TCP connections; the rule is the same.

Real balancers break ties differently. HAProxy's `leastconn` rotates in round robin among the servers with the same load, so that an idle pool still uses all servers. A random choice among the tied backends has the same effect.

## Example

Three backends, each a FCFS server. Eight requests arrive at times 0 to 7 with sizes 9, 1, 1, 9, 1, 1, 9, 1. The column "counts" shows $a[0], a[1], a[2]$ just before the pick, after the requests that ended by then were closed.

| request | arrival | size | counts | backend | start | finish | response time |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 9 | 0, 0, 0 | 0 | 0 | 9 | 9 |
| 1 | 1 | 1 | 1, 0, 0 | 1 | 1 | 2 | 1 |
| 2 | 2 | 1 | 1, 0, 0 | 1 | 2 | 3 | 1 |
| 3 | 3 | 9 | 1, 0, 0 | 1 | 3 | 12 | 9 |
| 4 | 4 | 1 | 1, 1, 0 | 2 | 4 | 5 | 1 |
| 5 | 5 | 1 | 1, 1, 0 | 2 | 5 | 6 | 1 |
| 6 | 6 | 9 | 1, 1, 0 | 2 | 6 | 15 | 9 |
| 7 | 7 | 1 | 1, 1, 1 | 0 | 9 | 10 | 3 |

Each long request goes to an idle backend, and the total response time is 34. [Round robin](/round-robin-load-balancing/) on the same input sends all three long requests to backend 0, and its total is 50. Request 7 shows the limit of the rule: all counts are 1, the tie goes to backend 0, and backend 0 still has 2 seconds of work left, while backends 1 and 2 have more. The count does not see remaining work.

## Correctness

Two invariants make the policy correct. First, $a[j]$ is always the number of open connections to backend $j$, because line L4 adds one for each connection that LC-PICK opens and line L6 subtracts one for each that closes. Second, the loop of line L2 keeps in $best$ the first up backend with the smallest count among those scanned so far. So each pick goes to an up backend with the fewest open connections. With no departures, the counts of any start state become equal within 1 after enough picks, and stay so. The full proof is in [the correctness proof](proofs/correctness.md).

**Optimality in a queueing model.** Winston (1977) studied $n$ identical servers, each with its own queue, Poisson arrivals and exponential service times, where each customer joins a queue on arrival and does not move later. Among all policies that know the current queue lengths, joining the shortest queue maximizes the expected discounted number of service completions. Weber (1978) allowed a general arrival process and independent service times with a non-decreasing hazard rate, which includes the exponential case. He proved that joining the shortest queue maximizes, in stochastic order, the number of customers served by time $t$, for every $t$. All policies see the same arrivals, so the number in the system at each time is then stochastically smallest, and by Little's law the long-run mean response time is smallest too. The result does not hold for every service distribution: Whitt (1986) gives service time distributions for which joining the shortest queue is not optimal, even among the policies that know only the queue lengths.

## Complexity

- **Time per pick.** The loop of line L2 visits all $n$ backends, so $\Theta(n)$. A min-[heap](/binary-heap/) keyed by the count gives $O(\log n)$ for each pick and each close. Because counts change by exactly 1, a [bucket queue](/bucket-queue/) with one list per count value gives $O(1)$ per operation.
- **Time per close.** $\Theta(1)$ for line L6, plus the heap or bucket update.
- **Space.** One counter per backend, $\Theta(n)$.
- **Feedback.** The balancer must see the end of each request. A [layer 4](/layer-4-load-balancing/) balancer in a direct server return setup does not see the response, and it must guess the end from TCP flags or timeouts.

## Properties

- **Load-aware without request sizes.** A backend that is busy with a long request keeps a high count, so new requests avoid it. In an event simulation of 4 FCFS servers with exponential service of mean 1, Poisson arrivals at load 0.9 and 100000 requests (seeds 1 to 5), the mean response time was 3.1 to 3.7 for least connections, 5.9 to 7.2 for [round robin](/round-robin-load-balancing/) and 9.6 to 11.1 for [random choice](/random-load-balancing/). The model values are 10 for random (each server is an M/M/1 queue at load 0.9) and 6.38 for round robin (each server is an $E_4/M/1$ queue), and the simulation matches both.
- **Counts, not work.** Two backends with one connection each look the same, even if one connection is a long upload and the other a short read. Least work left, which needs the request sizes, does better when the sizes are known.
- **Equal speeds assumed.** A backend that is twice as fast clears its queue twice as fast, and least connections sends it more requests only because its count falls sooner. For known capacity differences use [weighted least connections](/weighted-least-connections/).
- **Global state.** The counts are exact only for one balancer. Several balancers that each count their own connections see only their part of the load.
- **Stale counts are dangerous.** If the counts come from periodic reports instead of the balancer's own bookkeeping, all requests between two reports go to the same backend. See [least response time](/least-response-time/) for this herding effect.

## Variants and improvements

- **[Power of two choices](/power-of-two-choices/).** Look at only two random backends and take the one with fewer connections. This costs $O(1)$, needs no global scan, and, in the supermarket model, keeps the queues almost as short as full JSQ when $n$ is large. Envoy's least request balancer works this way when all weights are equal.
- **[Weighted least connections](/weighted-least-connections/).** Pick the smallest $a[j] / w_j$, for backends of different capacity.
- **[Least response time](/least-response-time/) and [peak EWMA](/peak-ewma/).** Multiply the count by a measured latency, so that a slow backend with few connections is also avoided.
- **Slow start.** A new or restarted backend has 0 connections and gets every new request until it catches up. HAProxy's `slowstart` server option and similar features raise its weight over a set time.
- **Least work left.** If request sizes are known, send each request to the backend with the least remaining work. Harchol-Balter, Chapter 24, compares it with JSQ.

## When to use it

Use least connections when request costs vary and one balancer sees all requests and their ends, for example a reverse proxy in front of application servers, or long-lived connections such as database sessions. HAProxy recommends `leastconn` for long sessions and notes that it suits short HTTP requests less well. With many independent balancers, use [power of two choices](/power-of-two-choices/), because each balancer's own counts are only a part of the load. When backends differ in capacity, use [weighted least connections](/weighted-least-connections/). When request costs are all alike, [round robin](/round-robin-load-balancing/) is just as good and needs no feedback.

## Pitfalls

- **Counting at the end instead of the start.** If line L4 runs only when the backend accepts the request, a burst of requests that arrive together all see the same counts and go to the same backend. Count the connection at once, in line L4.
- **A missed close.** If line L6 does not run for a request that times out or fails, the count of that backend stays too high forever, and the backend slowly gets no traffic. Run line L6 on every exit path, including errors.
- **Ties to the lowest index.** With line L3 as written, an idle pool sends every request to backend 0 until its count rises. With short requests that finish before the next one arrives, backend 0 gets all the traffic. Break ties at random or in round robin, as HAProxy does.
- **Sinkholing.** A backend that fails fast, for example one that returns an error at once because a dependency is down, closes each connection almost at once. Its count stays near 0, so least connections sends it most of the new traffic, and most requests fail. A health check that only opens a TCP port does not see this. Watch the error rate of each backend and take a backend out after a run of errors, or add a penalty to the count of a backend that returns errors.
- **A new backend gets a flood.** A backend that joins with 0 connections receives all new requests at once. Use slow start.
- **One long connection per client.** With HTTP/2 or gRPC, one connection carries many requests. Counting connections then says little about load; count requests in flight at [layer 7](/layer-7-load-balancing/).

## Implementations

## History

Assignment to the shortest queue was studied in queueing theory before load balancers existed: Winston (1977) and Weber (1978) proved its optimality for identical servers under their assumptions, and Whitt (1986) gave the limits. The Linux Virtual Server project of Wensong Zhang has least-connection and weighted least-connection schedulers, and nginx added the `least_conn` directive in version 1.3.1 (June 2012).

## References
