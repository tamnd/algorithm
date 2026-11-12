---
tag: 4ZQE1H
kind: algorithm
slug: least-response-time
name: Least response time
aliases:
- least latency balancing
- least_time
area: systems/load-balancing-and-hashing
level: intro
summary: "Keep a moving average L of each backend's response time and send each request to the smallest L times (requests in flight + 1). The factor stops a burst from herding to one backend."
solves: [load-balancing-problem]
model: word-ram
complexity:
  vars: {n: the number of backends}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [least-connections, exponential-moving-average]
see_also: [peak-ewma, least-connections, weighted-least-connections, power-of-two-choices, round-trip-time-estimation, health-checking, load-balancer]
sources:
  - url: http://nginx.org/en/docs/http/ngx_http_upstream_module.html
    title: nginx documentation, Module ngx_http_upstream_module
    locator: the least_time directive (least average response time and least number of active connections with weights; the header, last_byte and inflight parameters; in version 1.7.10, commercial only before 1.31.0)
  - url: https://raw.githubusercontent.com/nginx/nginx/master/src/http/modules/ngx_http_upstream_least_time_module.c
    title: nginx source, src/http/modules/ngx_http_upstream_least_time_module.c
    locator: ngx_http_upstream_least_time_eta (20 ms clusters, the 5000 ms cap, halving per fail_timeout, rt * (1 + conns)) and the peer choice by eta * weight
  - url: https://raw.githubusercontent.com/nginx/nginx/master/src/http/ngx_http_upstream_round_robin.h
    title: nginx source, src/http/ngx_http_upstream_round_robin.h
    locator: the macro ngx_http_upstream_response_time_avg (exponential moving average with weights 0.05 and 0.95, rounded; the first sample is taken as it is)
  - paper: doi:10.1109/71.824633
    title: "Michael Mitzenmacher, How useful is old information?, IEEE Transactions on Parallel and Distributed Systems 11(1), 2000, pages 6 to 20"
    locator: the bulletin board model (load information updated only periodically; joining the apparently shortest queue herds, a choice among a few random servers stays good)
  - paper: doi:10.1109/71.888643
    title: "Michael Dahlin, Interpreting stale load information, IEEE Transactions on Parallel and Distributed Systems 11, 2000"
    locator: the analysis of how the age of load information should change the choice of server, chapter level only
---

Least response time is a [load balancer](/load-balancer/) policy that keeps, for each backend, a moving average $L_j$ of its recent response times, and sends each new request to the backend with the smallest estimated time to finish, $L_j \cdot (a_j + 1)$, where $a_j$ is the number of its requests in flight. The average is an [exponential moving average](/exponential-moving-average/) that the balancer updates each time a response ends. Unlike [least connections](/least-connections/), it sees a backend that is slow for a reason the counts do not show, such as a slow disk or a far network path. The factor $a_j + 1$ is what keeps it stable: a rule that ranks by $L_j$ alone sends every request of a burst to the same backend. The nginx directive `least_time` uses this score.

## In plain words

You choose a checkout lane at a store. Counting people is good, but some cashiers are slower than others. If you remember how long each cashier took for recent customers, you can estimate your own wait: the time per customer times the number of people in front of you, plus you.

The balancer does this for each server. When a response comes back, it updates that server's typical time, giving recent responses more weight. For a new request, it picks the server where the typical time times (requests already there plus one) is smallest. If it ignored the count and only looked for the fastest server, every request that arrives before the next response would rush to that one server.

## The problem

The model has $n$ backends with integer weights $w_j \ge 0$, and requests that arrive online in any order. Each request ends after a time that the balancer measures but cannot predict: time to the first byte of the response header, or to its last byte. The service speed of each backend can change over time. The goal is low response time, which needs the balancer to send less work to the backends that are slow now. The policy is a heuristic. There is no worst-case or queueing optimality result for it, and the guarantees below are about what it does with its estimates. This is one policy for the [load balancing problem](/load-balancing-problem/).

## The algorithm

The state of backend $j$ is the count $a[j]$, the estimate $L[j]$ (empty until the first sample), the weight $w[j]$ and the flag $up[j]$ from [health checking](/health-checking/). The smoothing factor is $0 < \alpha \le 1$.

```pseudo id=main
LRT-PICK(a, L, w, up)
L1  best ← none
L2  for j ← 0 to n − 1 do
L3      if not up[j] or w[j] = 0 then continue
L4      e[j] ← L[j] · (a[j] + 1)              ▷ L[j] counts as 0 before its first sample
L5      if best = none or e[j] · w[best] < e[best] · w[j] then
L6          best ← j
L7  if best ≠ none then a[best] ← a[best] + 1
L8  return best

LRT-DONE(j, x)                               ▷ a request to j ended after time x
L9  a[j] ← a[j] − 1
L10 if L[j] is empty then L[j] ← x
L11 else L[j] ← L[j] + α · (x − L[j])
```

Line L4 estimates how long the backend needs to finish its current requests and the new one, if it serves them one after another at its recent speed. Line L5 divides by the weight, by cross-multiplication. Line L11 is the moving average: the new sample gets weight $\alpha$ and the old estimate $1 - \alpha$. A backend without a sample scores 0, so it gets the next request, which gives it its first sample.

**The nginx version.** nginx `least_time header` or `least_time last_byte` keeps $L$ in milliseconds with $\alpha = 0.05$, and rounds after each update. Before line L4 it changes the estimate in three ways: it rounds it up to the next multiple of 20 ms (so that backends with close times tie and share the load by weighted round robin), it caps it at 5000 ms (above that all backends look equally bad and the rule becomes least connections), and it halves it once for each `fail_timeout` period since the last check, so that a slow backend gets a new chance. With the `inflight` parameter, it also uses the average age of the requests still in flight when that is larger.

## Example

**A burst.** Three backends have estimates $L = (10, 12, 15)$ ms and weight 1, and six requests arrive before any response.

| request | in flight before | scores $L_j (a_j + 1)$ | backend |
|---|---|---|---|
| 1 | 0, 0, 0 | 10, 12, 15 | 0 |
| 2 | 1, 0, 0 | 20, 12, 15 | 1 |
| 3 | 1, 1, 0 | 20, 24, 15 | 2 |
| 4 | 1, 1, 1 | 20, 24, 30 | 0 |
| 5 | 2, 1, 1 | 30, 24, 30 | 1 |
| 6 | 2, 2, 1 | 30, 36, 30 | 0 |

The split is $3, 2, 1$. The speeds $1/L_j$ give the shares $2.4$, $2$ and $1.6$ of six requests, and the split is within one request of each share. The rule that ranks by $L_j$ alone sends all six requests to backend 0, because no estimate changes until a response ends.

**A slowdown.** With $\alpha = 0.05$, a backend at $L = 10$ ms slows down so that every response now takes 50 ms. After $k$ responses the estimate is $50 - 40 \cdot 0.95^k$: 12 ms after one response, 19.0 after five, 30.5 after fourteen and 46.0 after forty-five. The gap to the new value halves about every 13.5 responses.

**The nginx average.** Starting empty, the samples 100, 100, 300, 300, 300 ms give the averages 100, 100, 110, 120, 129. An average of 39 ms with 2 connections rounds up to the cluster 40 and scores $40 \cdot 3 = 120$. An average of exactly 20 ms rounds up to 40 as well, because the code adds $20 - (rt \bmod 20)$.

## Correctness

The counts are exact by the argument of [least connections](/least-connections/). The loop of line L2 returns the first eligible backend with the smallest $e_j / w_j$; line L5 is equivalent to that ratio test because both weights are positive. After the samples $x_1, \ldots, x_k$, the estimate is

$$L = (1 - \alpha)^k L_0 + \sum_{i=1}^{k} \alpha (1 - \alpha)^{k-i} x_i ,$$

a weighted average with weights that add up to 1, so it always lies between the smallest and the largest value seen. If all new samples equal $y$, the gap $L - y$ shrinks by the factor $1 - \alpha$ per sample.

**Theorem (a burst is split by speed).** Suppose $k$ requests arrive before any of them ends, every eligible backend has $L_j > 0$, and let $u_j = w_j / L_j$ and $U = \sum_j u_j$ over the $e$ eligible backends. Then backend $j$ receives $c_j$ requests with

$$\frac{k\, u_j}{U} - 1 \le c_j \le \frac{k\, u_j}{U} + (e - 1).$$

The key step: the rule picks the backend with the largest $u_j / (c_j + 1)$, and this largest value never grows during the burst. So at its last pick each backend had $u_j / c_j$ at least the final largest value $m$, which gives $c_j \le u_j / m$, and summing gives $m \le U/k$. In the language of seat apportionment, this is the method of D'Hondt with the speeds as votes. The full proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

- **Time per pick.** $\Theta(n)$ for the scan of line L2.
- **Time per response.** $\Theta(1)$ for lines L9 to L11.
- **Space.** $\Theta(n)$: one count, one estimate and one weight per backend.
- **Sampled form.** Score only two random backends, as in [power of two choices](/power-of-two-choices/), for $O(1)$ per pick. [Peak EWMA](/peak-ewma/) is such a sampled form.

## Properties

- **Sees slowness that counts miss.** A backend whose requests take longer for a reason outside the balancer gets a higher $L_j$ and so less work, even when its count is low.
- **Stable under bursts.** The theorem bounds the split of a burst within about one request of the speed shares, while a latency-only rule herds.
- **Lags behind changes.** The estimate moves by a fixed fraction per response. With $\alpha = 0.05$ it needs about 14 responses to cover half of a jump. A backend that suddenly becomes slow keeps receiving work in the meantime; [peak EWMA](/peak-ewma/) reacts to a rise at once.
- **Needs responses to learn.** A backend that gets no requests gets no new samples, and its old estimate stays. nginx halves the estimate over time for this reason.
- **Local view.** Each balancer sees only its own requests and their times.

## Variants and improvements

- **Latency only.** Rank by $L_j$ without the count. This herds and should not be used when many requests arrive within one response time.
- **Time to first byte or last byte.** Time to the header measures the server's work; time to the last byte also includes the response size and the client's download speed.
- **[Peak EWMA](/peak-ewma/).** Jump the estimate up at once to any larger sample, decay it with time instead of per sample, and choose between two random backends.
- **Weighted round robin among near ties.** nginx clusters estimates in 20 ms steps so that backends with close times share the load by [weighted round robin](/weighted-round-robin/).
- **Server-reported load.** Backends can report their own utilization or queue length, and the balancer can rank by that. Response time measured at the balancer needs no help from the backend but includes the network.

## When to use it

Use least response time when backends differ in speed in ways that change over time, for example a mixed fleet, shared machines with noisy neighbors, or backends in different zones, and when one balancer sees enough responses per backend to keep the estimates fresh. Keep the factor $a_j + 1$. With very few requests per backend the estimates are noise, and [least connections](/least-connections/) or [round robin](/round-robin-load-balancing/) is a better choice.

## Pitfalls

- **Herding.** Ranking by the estimate alone, or using estimates that a central service publishes every few seconds, sends all requests between two updates to the backend that looks best. Mitzenmacher (2000) shows in a bulletin board model that the policy of joining the apparently shortest queue does badly when the information is old, while a choice among a few random servers keeps working. Keep the local count in the score or sample two backends.
- **Fast failures look fast.** A backend that returns errors in 1 ms gets a very low $L_j$ and draws traffic, the sinkholing effect of [least connections](/least-connections/). Do not feed the times of failed requests into $L_j$, or feed a penalty time instead.
- **Response size in the time.** With time to the last byte, a backend that serves the large downloads looks slow. Use time to the header when response sizes vary a lot.
- **A frozen estimate.** A backend that was slow once and then gets no traffic keeps its bad estimate forever. Decay the estimate with time, or send it an occasional request.
- **Unmeasured backends.** A backend with no sample scores 0 and wins the next pick. With a burst, many requests can reach it before its first response returns, because $L_j = 0$ keeps its score at 0 however many requests it has. Start new backends with a default estimate, or with a large penalty as Finagle does.

## Implementations

## History

The papers of Mitzenmacher and Dahlin of 2000 study what goes wrong when a balancer acts on load information that is old, which is the main risk of ranking by a measured time. nginx added the `least_time` method in version 1.7.10 as part of its commercial version, and it became part of the open source nginx in version 1.31.0.

## References
