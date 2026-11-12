---
tag: FXQQ1P
kind: algorithm
slug: weighted-least-connections
name: Weighted least connections
aliases:
- WLC
- weighted least-connection scheduling
area: systems/load-balancing-and-hashing
level: intro
summary: "Send each new connection to the backend with the smallest active connections divided by weight, compared by cross-multiplication. With no departures, no backend gets more than its rounded-up share."
solves: [load-balancing-problem]
model: word-ram
complexity:
  vars: {n: the number of backends}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [least-connections, weighted-round-robin]
see_also: [least-connections, weighted-round-robin, weighted-random-load-balancing, least-response-time, peak-ewma, power-of-two-choices, load-balancer, health-checking]
sources:
  - url: https://raw.githubusercontent.com/torvalds/linux/master/net/netfilter/ipvs/ip_vs_wlc.c
    title: Wensong Zhang and Peter Kese, IPVS Weighted Least-Connection Scheduling module, Linux kernel, net/netfilter/ipvs/ip_vs_wlc.c
    locator: ip_vs_wlc_schedule (load is overhead divided by weight, compared as loh * weight(dest) > doh * weight(least) in 64-bit integers; weight 0 quiesces a server)
  - url: https://raw.githubusercontent.com/torvalds/linux/master/include/net/ip_vs.h
    title: Linux kernel, include/net/ip_vs.h
    locator: ip_vs_dest_conn_overhead (256 times the active connections plus the inactive ones in older kernels; plus totalconns since the commit "ipvs, add totalconns for dest" of July 2026)
  - url: https://raw.githubusercontent.com/torvalds/linux/master/net/netfilter/ipvs/ip_vs_sed.c
    title: Wensong Zhang, IPVS Shortest Expected Delay scheduling module, Linux kernel, net/netfilter/ipvs/ip_vs_sed.c
    locator: the header comment ((C_i + 1) / U_i, the difference from WLC, and the reference to Weinrib and Shenker, INFOCOM 1988)
  - url: https://raw.githubusercontent.com/nginx/nginx/master/src/http/modules/ngx_http_upstream_least_conn_module.c
    title: nginx source, src/http/modules/ngx_http_upstream_least_conn_module.c
    locator: ngx_http_upstream_get_least_conn_peer (peer->conns * best->weight < best->conns * peer->weight; tied peers are then chosen by smooth weighted round robin)
  - url: http://nginx.org/en/docs/http/ngx_http_upstream_module.html
    title: nginx documentation, Module ngx_http_upstream_module
    locator: the least_conn directive (least active connections, taking into account the server weights; ties in weighted round robin)
  - url: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/load_balancing/load_balancers
    title: Envoy documentation, Supported load balancers
    locator: Weighted least request (power of two choices with equal weights; weight / (active_requests + 1)^active_request_bias with bias 1.0 by default otherwise)
---

Weighted least connections (WLC) is a [load balancer](/load-balancer/) policy that sends each new connection to the backend with the smallest ratio $a_j / w_j$, where $a_j$ is the number of active connections of backend $j$ and $w_j > 0$ its capacity weight. It is [least connections](/least-connections/) for backends of different size: a backend with weight 3 is treated as idle until it has three times the connections of a backend with weight 1. Real balancers compare two ratios by cross-multiplication, $a_i w_j < a_j w_i$, so the test needs no division. The Linux Virtual Server scheduler `wlc` and the nginx directive `least_conn` work this way.

## In plain words

A help desk has three agents. One is new and slow, one is average, and one is an expert who can handle three calls in the time the new agent handles one. A plain "fewest open calls" rule would treat them the same. The weighted rule divides the number of open calls of each agent by the agent's speed, and gives the next call to the agent with the smallest result. The expert can then hold three calls and still look as free as the new agent with one.

As in plain least connections, the balancer counts a connection up when it starts and down when it ends. The counts react to slow requests on their own. The weights only add what the counts cannot see: how much each server can handle at once.

## The problem

The model has $n$ backends with integer weights $w_0, \ldots, w_{n-1} \ge 0$ that the operator sets, often from the number of cores or a benchmark. Connections arrive online in any order (the arrival model can be adversarial), and each one stays open for a time that the balancer does not know. The balancer sees each open and each close. The goal is that each backend carries load in proportion to its weight, and that a backend that is slow at the moment receives less. A backend with weight 0 is *quiesced*: it keeps its open connections but gets no new ones, which is how [connection draining](/connection-draining/) is often done. This is one policy for the [load balancing problem](/load-balancing-problem/).

## The algorithm

The state is the counter $a[j]$ and the flag $up[j]$ of each backend, the flag from [health checking](/health-checking/).

```pseudo id=main
WLC-PICK(a, w, up)                     ▷ counters a[0..n−1], weights w[0..n−1] ≥ 0
L1  best ← none
L2  for j ← 0 to n − 1 do
L3      if not up[j] or w[j] = 0 then continue
L4      if best = none or a[j] · w[best] < a[best] · w[j] then
L5          best ← j                     ▷ a[j] / w[j] < a[best] / w[best]
L6  if best ≠ none then a[best] ← a[best] + 1
L7  return best

WLC-DONE(j)                             ▷ a connection to backend j has closed
L8  a[j] ← a[j] − 1
```

Line L4 is the ratio test without division. Both weights are positive there, so multiplying by $w[j] \cdot w[best]$ keeps the direction of the inequality. Integers make the test exact: a float division can round two equal ratios to different values and break ties at random. Ties keep the lowest index. nginx instead collects all tied backends and picks among them by [smooth weighted round robin](/weighted-round-robin/). Line L6 counts the new connection at once, so that the next pick sees it.

LVS uses a different load. Its `wlc` scheduler ranks the *overhead* $h_j$ instead of $a_j$, with $h_j = 256 \cdot \text{active}_j + \text{inactive}_j$, where an inactive connection is one that is not in the established state, for example one in TIME_WAIT. An active connection thus counts 256 times an inactive one. A kernel change of July 2026 replaced the inactive count by the total count, which gives $257 \cdot \text{active}_j + \text{inactive}_j$. The comparison is the same as line L4, in 64-bit integers.

## Example

Three backends have weights $w = (3, 2, 1)$, so $W = 6$. Six connections open and none closes.

| pick | counts before | ratios $a_j / w_j$ | backend |
|---|---|---|---|
| 1 | 0, 0, 0 | 0, 0, 0 | 0 |
| 2 | 1, 0, 0 | 1/3, 0, 0 | 1 |
| 3 | 1, 1, 0 | 1/3, 1/2, 0 | 2 |
| 4 | 1, 1, 1 | 1/3, 1/2, 1 | 0 |
| 5 | 2, 1, 1 | 2/3, 1/2, 1 | 1 |
| 6 | 2, 2, 1 | 2/3, 1, 1 | 0 |

After six picks the counts are $(3, 2, 1)$, exactly the weights. Pick 3 shows a property of the rule: a backend with 0 connections has ratio 0 and wins over every busy backend, whatever its weight. So backend 2, with the smallest weight, gets its first connection before backend 0 gets its second.

Now two connections to backend 0 close, and the counts are $(1, 2, 1)$ with ratios $1/3, 1, 1$. The next two picks both go to backend 0, and the counts are again $(3, 2, 1)$. The rule refills the backend that freed capacity.

Two more cases show the other load measures:

- **LVS overhead.** Backend A has 2 active and 100 inactive connections, backend B has 3 active and none inactive, both with weight 1. The overheads are $256 \cdot 2 + 100 = 612$ and $256 \cdot 3 = 768$, so A wins. The 100 closing connections weigh less than one active connection.
- **WLC against shortest expected delay.** Backend 0 has weight 10 and 5 connections; backend 1 has weight 1 and none. WLC compares $5/10$ with $0/1$ and picks backend 1. The shortest expected delay rule of LVS (`sed`) compares $(5+1)/10 = 0.6$ with $(0+1)/1 = 1$ and picks backend 0, where the new request would wait less.

## Correctness

The counters are exact by the same argument as for [least connections](/least-connections/): line L6 adds one per open and line L8 subtracts one per close. The loop of line L2 keeps the first eligible backend (up, with positive weight) with the smallest ratio, and line L4 is equivalent to the ratio test because both weights are positive.

**Theorem (upper quota).** Suppose the weights and flags stay fixed, all counters start at 0 and no connection closes. Let $W$ be the sum of the weights of the eligible backends. After $k$ picks, every eligible backend $j$ has

$$a_j \le \left\lceil \frac{k\, w_j}{W} \right\rceil \quad\text{and}\quad a_j \ge \frac{k\, w_j}{W} - (e - 1),$$

where $e$ is the number of eligible backends. When $W$ divides $k$, $a_j = k\, w_j / W$ exactly.

The key step: the backend picked has the smallest ratio $m$, so every eligible $i$ has $a_i \ge m\, w_i$, and summing gives $k \ge m W$. So the picked backend has $a_j \le k w_j / W$ before the pick, and one more connection keeps it within the rounded-up quota. In the language of seat apportionment, WLC with no departures is the divisor method of Adams, which never exceeds the upper quota. The lower bound is tight up to a constant: with one backend of weight $M$ and $e - 1$ backends of weight 1, the first $e$ picks go one to each backend, so the heavy backend has 1 connection against a quota near $e$. The full proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

- **Time per pick.** $\Theta(n)$ for the scan of line L2. Each step is two multiplications and one comparison.
- **Time per close.** $\Theta(1)$.
- **Faster picks.** A min-[heap](/binary-heap/) ordered by the ratio gives $O(\log n)$ per pick and per close, because only one key changes each time. The [bucket queue](/bucket-queue/) trick of least connections does not apply, because the ratios are not small integers.
- **Space.** $\Theta(n)$ for the counters and weights.
- **Overflow.** The products $a_j w_i$ need room for the largest count times the largest weight. LVS casts to 64-bit integers before it multiplies.

## Properties

- **Proportional when connections are equal.** With no departures, the Theorem gives an exact share in each block of $W$ picks. With departures, a backend's share also depends on how fast it closes connections, which is the point of the policy.
- **Zero beats everything.** A backend with no connections wins over any busy backend, whatever the weights. This is fair in steady state but floods a new or restarted backend.
- **Counts, not work.** As in least connections, two connections look the same whatever their cost.
- **Weights are static.** If a backend slows down, for example from garbage collection or a noisy neighbor, its weight stays the same. Only its count reacts. [Least response time](/least-response-time/) and [peak EWMA](/peak-ewma/) measure the slowdown directly.
- **Local view.** Each balancer counts only its own connections.

## Variants and improvements

- **Shortest expected delay (SED).** Rank $(a_j + 1) / w_j$, the expected delay of the new request if each backend serves at a rate proportional to its weight. The extra 1 stops a lightly weighted idle backend from winning over a heavy, nearly idle one. The LVS `sed` comment cites Weinrib and Shenker (INFOCOM 1988) for the rule. LVS `nq` (never queue) sends to an idle backend if there is one, and else uses SED.
- **Ties by weighted round robin.** nginx breaks ties among backends with equal ratio by [weighted round robin](/weighted-round-robin/), so an idle pool still spreads by weight instead of sending everything to the first backend.
- **Sampled weighted least request.** Envoy, with unequal weights, runs a weighted round robin whose weight is $w_j / (a_j + 1)^b$, with bias $b = 1$ by default. With equal weights it uses [power of two choices](/power-of-two-choices/) on the request counts.
- **Slow start.** Raise the weight of a new backend from a small value to its target over a set time, to avoid the flood of the zero-count rule.

## When to use it

Use WLC when one balancer sees all connections, request costs vary, and backends differ in capacity by known factors, for example a pool with machines of two sizes. Set the weights from capacity, not from a wish to steer traffic: a weight that is too high on a slow machine overloads it, and its count rises only after its queue grows. When all backends are the same, plain [least connections](/least-connections/) is enough. When the slowdowns change over time, use a latency-aware rule such as [peak EWMA](/peak-ewma/).

## Pitfalls

- **Dividing in floating point.** $a_j / w_j$ in floats can make two equal ratios differ in the last place, and the tie then goes to whichever has the smaller rounding error. Use the integer cross-multiplication of line L4.
- **Overflow of the product.** With 32-bit counters and large weights, $a_j w_i$ can wrap around and invert the comparison. Use 64-bit products.
- **Weight 0 in the ratio.** Dividing by a weight of 0 fails, and the cross-multiplied test gives answers that have nothing to do with load when one of the two weights is 0. Skip weight 0 before the test, as line L3 does.
- **Flooding a new backend.** A backend that joins with 0 connections wins every pick until its ratio catches up. With a pool of 20 busy backends with 50 connections each and weight 1, a new backend gets the next 50 connections in a row if no connection closes in the meantime. Use slow start.
- **Sinkholing.** A backend that fails fast closes its connections at once, keeps a count near 0, and draws most new traffic, as on the [least connections](/least-connections/) page. A high weight makes this worse. Count recent errors as load or remove the backend after a run of errors.
- **A missed close.** If line L8 does not run on an error path, the count stays high and the backend slowly gets no traffic.

## Implementations

## History

The Linux Virtual Server project of Wensong Zhang has `wlc` as one of its schedulers, with the overhead that counts an active connection 256 times an inactive one. Its `sed` and `nq` schedulers rank the expected delay instead. nginx has the `least_conn` directive, which takes the server weights into account and breaks ties by weighted round robin. Envoy's least request balancer adapts the idea to request counts and to a sampled choice.

## References
