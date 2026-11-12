---
tag: MD9K0X
kind: algorithm
slug: peak-ewma
name: Peak EWMA
aliases:
- peak exponentially weighted moving average
area: systems/load-balancing-and-hashing
level: advanced
summary: "Latency cost per backend that jumps up at once to a slower response and decays with time constant tau; load is cost times (pending + 1), and the balancer takes the lower of two random backends."
solves: [load-balancing-problem]
model: word-ram
complexity:
  vars: {n: the number of backends}
  time: {worst: O(1)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: false, recursive: false}
prereqs: [least-response-time, power-of-two-choices, exponential-decay]
see_also: [least-response-time, least-connections, power-of-two-choices, exponential-moving-average, round-trip-time-estimation, load-balancer, health-checking]
sources:
  - url: https://github.com/twitter/finagle/blob/develop/finagle-core/src/main/scala/com/twitter/finagle/loadbalancer/PeakEwma.scala
    title: Finagle source, finagle-core, com/twitter/finagle/loadbalancer/PeakEwma.scala
    locator: the class Metric (Penalty = Long.MaxValue >> 16, observe with the peak rule, get with observe(0.0) and cost * (pending + 1)) and PeakEwmaNode (start and end of each request)
  - url: https://github.com/twitter/finagle/blob/develop/finagle-core/src/main/scala/com/twitter/finagle/util/Ema.scala
    title: Finagle source, finagle-core, com/twitter/finagle/util/Ema.scala
    locator: the class Ema (update with w = exp(-td / window) and x * (1 - w) + ema * w; reset)
  - url: https://twitter.github.io/finagle/guide/Clients.html
    title: Finagle documentation, Clients
    locator: the section on load balancing, Balancers.p2cPeakEwma (decayTime, default 10 seconds)
  - url: https://docs.rs/tower/latest/tower/load/peak_ewma/struct.PeakEwma.html
    title: tower crate documentation, tower::load::peak_ewma::PeakEwma
    locator: the struct documentation (EWMA of latencies times pending requests, derived from Finagle, a default RTT of 1 second before the first measurement)
  - paper: doi:10.1109/71.963420
    title: "Michael Mitzenmacher, The power of two choices in randomized load balancing, IEEE Transactions on Parallel and Distributed Systems 12(10), 2001, pages 1094 to 1104"
    locator: the supermarket model (each arrival joins the shorter of d random queues), for the sampled choice
---

Peak EWMA is a latency-aware [load balancer](/load-balancer/) policy from the Finagle RPC library. Each backend has a *cost*, an estimate of its response time that jumps up at once when a response is slower than the estimate and otherwise moves toward new responses with a weight that depends on the elapsed time. Reading the cost also lets it [decay](/exponential-decay/) toward 0 with a time constant $\tau$ (10 seconds by default in Finagle). The load of a backend is its cost times (requests pending + 1), and each request goes to the less loaded of two backends drawn at random, as in [power of two choices](/power-of-two-choices/). The rule reacts to a slow backend after one slow response and gives it traffic again only slowly.

## In plain words

Imagine you pick between two delivery firms for each parcel. You remember how slow each one was. If one firm is ever slower than you thought, you believe the bad news at once. If it is faster, you only trust it a little, and your memory of the bad times fades over the next few seconds. Your guess for a firm is that memory times the number of parcels it already has from you, plus one.

The balancer works the same way. It does not compare all servers: it picks two at random and sends the request to the one with the better guess. One bad response is enough to steer traffic away from a server that has a pause, and the server gets traffic back as the memory fades.

## The problem

The model has $n$ backends and requests that arrive online in any order, often from many independent clients, each with its own balancer. The balancer measures the time from sending each request to its end, on a monotonic clock. The speed of each backend changes over time, for example during garbage collection pauses. The goal is low response time, and in particular to keep requests away from a backend that is slow now. There is no worst-case or queueing optimality result for the policy; it is a heuristic. What holds is the envelope of the Theorem below, and the $O(1)$ cost of each pick. This is one policy for the [load balancing problem](/load-balancing-problem/).

## The algorithm

Backend $j$ has the cost $c[j]$ (0 at the start), the time $s[j]$ of its last update and the number $p[j]$ of pending requests. PENALTY is a number larger than any real cost.

```pseudo id=main
OBSERVE(j, x, t)                   ▷ a sample x at time t, or x = 0 to decay only
L1  Δ ← max(t − s[j], 0); s[j] ← max(s[j], t)
L2  if x > c[j] then
L3      c[j] ← x                     ▷ the peak rule
L4  else w ← e^(−Δ/τ)
L5      c[j] ← c[j] · w + x · (1 − w)

LOAD(j, t)
L6  OBSERVE(j, 0, t)
L7  if c[j] = 0 and p[j] > 0 then return PENALTY + p[j]
L8  return c[j] · (p[j] + 1)

PICK(t)                             ▷ among the backends that are up
L9  draw two different backends i and k uniformly at random
L10 if LOAD(k, t) < LOAD(i, t) then i ← k
L11 p[i] ← p[i] + 1; return i       ▷ the caller keeps t0 = t for the request

DONE(j, t0, t)                      ▷ the request to j sent at t0 ends at t
L12 p[j] ← p[j] − 1
L13 OBSERVE(j, t − t0, t)
```

Line L3 is the peak rule: in Finagle it resets the moving average, and the next update sets it to the sample. Line L5 is an exponential moving average for samples that arrive at irregular times: the old value keeps the weight $e^{-\Delta/\tau}$, where $\Delta$ is the time since the last update, so a sample after a long silence counts almost fully. Line L6 runs the same update with the value 0, so the cost decays toward 0 between samples. Line L7 handles a backend that has requests out but no sample yet: it loses against any backend with a sample, so it gets one probe at a time until its first response. A backend with no sample and nothing pending has load 0 and wins, which is how a new backend gets its first request.

In Finagle, PENALTY is `Long.MaxValue >> 16` nanoseconds, $2^{47} - 1$, about 39.1 hours. The Rust crate tower, used by the Linkerd proxy, implements the same cost and states that it is derived from Finagle; before the first measurement it uses a default round trip time of 1 second instead of a penalty.

## Example

**A trace of one cost.** Take $\tau = 10$ s. The calls below are on one backend, with times in seconds and costs in milliseconds.

| call | time | value | cost after |
|---|---|---|---|
| sample | 0 | 10 ms | 10.0 |
| sample | 1 | 500 ms | 500.0 |
| read | 2 | | 452.4 |
| sample | 2 | 10 ms | 452.4 |
| sample | 3 | 10 ms | 410.3 |
| read | 8 | | 248.9 |
| sample | 30 | 10 ms | 36.5 |

The 500 ms response raises the cost at once. The read at time 2 decays it by $e^{-0.1}$. The sample at time 2 comes 0 s after the read, so $w = 1$ and it has no effect. The sample at time 3 has $w = e^{-0.1} = 0.905$ and moves the cost only from 452.4 to 410.3. The read at time 8 decays it by $e^{-0.5}$. The last sample comes 22 s later, with $w = e^{-2.2} = 0.111$, and counts for 89 percent. Without samples, a peak halves every $\tau \ln 2 = 6.93$ s.

**A choice.** Backend A has cost 452.4 ms and no pending request, so its load is 452.4. Backend B has cost 20 ms and 3 pending requests, so its load is $20 \cdot 4 = 80$. B wins although it is busier. If A gets no more samples after its 500 ms peak, its cost falls below the load 20 of an idle backend B only $10 \ln (500/20) = 32.2$ s after the peak.

**A slow backend in a pool.** In a simulation of five backends, one with a fixed response time of 100 ms and four with 10 ms, each able to serve any number of requests at once, a request arrives every 2 ms for 8 s, 4000 requests in all. Over the seeds 1 to 5, the slow backend received 1 or 2 requests, and each fast backend between 967 and 1027. A uniform random choice would send it about 800.

## Correctness

The pending counts are exact, because line L11 adds one per request and line L12 subtracts one per end. PICK returns the backend with the smaller load of a uniform random ordered pair of different backends.

**Theorem (envelope of the cost).** Suppose the calls on backend $j$ come with non-decreasing times, and let $t$ be the time of the last one. Let the samples be $x_i$ at times $t_i \le t$. Then

$$\max_i x_i\, e^{-(t - t_i)/\tau} \;\le\; c[j] \;\le\; \max_i x_i .$$

Also, if only reads happen between $t_a$ and $t_b$, the cost at $t_b$ is the cost at $t_a$ times $e^{-(t_b - t_a)/\tau}$, however many reads there are.

The key step is that each call, with $w = e^{-\Delta/\tau}$, gives a new cost that is at least $c\,w$, at least the new sample, and at most the larger of the old cost and the sample. The lower bound is the precise meaning of "sensitive to peaks": one response of $x$ keeps the cost at least $x\,e^{-\Delta/\tau}$ for each $\Delta$ after it, whatever faster responses follow. The full proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

- **Time per pick.** $O(1)$: two random draws and two calls of LOAD, each with one exponential.
- **Time per response.** $O(1)$.
- **Space.** $\Theta(n)$: a cost, a time and a count per backend.
- **No global state.** Each client keeps its own costs, and the random pair needs no scan of the pool. This suits client-side balancing with many clients and many backends.

## Properties

- **Fast up, slow down.** One slow response sets the cost to that response time. A faster response lowers it only by the weight of the time since the last update, and reads decay it toward 0.
- **Decay by time, not by count.** The weight of the past depends on seconds elapsed, not on the number of samples. A busy client and a quiet client forget a peak at the same speed.
- **Reads change the state.** A read is an update with the value 0. The decay alone does not depend on the reads, but the weight of the next smaller sample does, because it uses the time since the last update of either kind.
- **Load includes the queue.** The factor $p_j + 1$ plays the role it has in [least response time](/least-response-time/): pending requests make a backend look busier at once, before their responses return.
- **Random pair.** As in [power of two choices](/power-of-two-choices/), a client never herds on one backend that looks best, and two clients that see the same costs still spread their requests.

## Variants and improvements

- **Full scan.** Compare all backends instead of two. This is [least response time](/least-response-time/) with the peak rule and costs $\Theta(n)$ per pick.
- **A default instead of a penalty.** tower starts each backend at a round trip time of 1 second, so a new backend is neither flooded nor shut out.
- **Other decay times.** Finagle lets the user set `decayTime`; a short value forgets a pause quickly but makes the cost noisy, a long value keeps a backend out for longer after one slow response.
- **Least loaded with two choices.** Rank by $p_j$ only, without latency. Finagle's `p2c` balancer and Envoy's least request balancer do this.

## When to use it

Use peak EWMA in RPC clients that talk to many backends with short requests, where some backends stall now and then, for example during garbage collection, and where each client balances on its own. It needs a steady stream of responses to keep the costs fresh. For long-lived connections with few requests, [least connections](/least-connections/) is simpler. For a single central balancer that can see every backend, a full scan by [least response time](/least-response-time/) is also possible.

## Pitfalls

- **Fast errors.** Finagle also measures the time of a failed request. A backend that fails in 1 ms gets a low cost and draws traffic, the sinkholing effect of [least connections](/least-connections/). Pair the policy with [health checking](/health-checking/) or with a failure accrual that removes such a backend.
- **A long tail after one spike.** With $\tau = 10$ s, one 500 ms response keeps a backend more expensive than an idle 20 ms backend for about 32 s, if it gets no new samples. For a backend that has few requests, that can be most of its traffic.
- **A clock that goes back.** The update needs a monotonic clock. Line L1 treats a time in the past as $\Delta = 0$; with a wall clock that jumps, the decay can stop or jump.
- **Units.** Costs, $\tau$ and the penalty must use the same unit. Finagle works in nanoseconds; a penalty meant for nanoseconds is far too small if the costs are in seconds.
- **Too few backends.** With $n = 2$ every pick compares both backends, and the random pair adds nothing; with $n = 1$ there is no choice at all.

## Implementations

## History

Peak EWMA comes from Finagle, the RPC library of Twitter, where the balancer `Balancers.p2cPeakEwma` combines it with power of two choices. The tower crate for Rust, used by the Linkerd 2 proxy, carries a version that states it is derived from Finagle. The sampled choice goes back to the power of two choices of Azar, Broder, Karlin and Upfal and to the supermarket model of Mitzenmacher.

## References
