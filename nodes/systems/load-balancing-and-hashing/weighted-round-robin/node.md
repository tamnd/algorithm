---
tag: CCH3Y5
kind: algorithm
slug: weighted-round-robin
name: Weighted round-robin
aliases:
- smooth weighted round robin
- WRR
- weighted round robin load balancing
area: systems/load-balancing-and-hashing
level: intro
summary: "Give backend j exactly w_j of every W = sum of weights requests. The smooth nginx form adds w_j to a counter, picks the largest and subtracts W, so picks are spread out."
solves: [load-balancing-problem]
model: word-ram
complexity:
  vars: {n: the number of backends}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2012
  people: [Maxim Dounin, Wensong Zhang]
  note: Dounin's 2012 change to nginx gave the smooth form; the gcd-based form is in the IPVS scheduler of Linux Virtual Server by Zhang.
prereqs: [round-robin-load-balancing]
see_also: [weighted-random-load-balancing, weighted-least-connections, stride-scheduling, lottery-scheduling, deficit-round-robin, weighted-fair-queueing, load-balancer, euclidean-algorithm]
sources:
  - url: https://github.com/phusion/nginx/commit/27e94984486058d73157038f7950a0a36ecc6e35
    title: "Maxim Dounin, Upstream: smooth weighted round-robin balancing, nginx commit (svn trunk r4622), files src/http/ngx_http_upstream_round_robin.c and .h"
    locator: the commit message (the rule, the example weights 5, 1, 1 with the sequence a a b a c a a and its counters, and effective_weight); shipped in nginx 1.3.0 of 15 May 2012 by the change log; this mirror hash is not the hash in the official nginx repository
  - url: https://raw.githubusercontent.com/torvalds/linux/master/net/netfilter/ipvs/ip_vs_wrr.c
    title: Wensong Zhang, IPVS weighted round-robin scheduling module, Linux kernel, net/netfilter/ipvs/ip_vs_wrr.c
    locator: the comment on mw, di and cw, and ip_vs_wrr_schedule (cw steps down by the gcd di and wraps to mw)
  - url: http://www.linuxvirtualserver.org/docs/scheduling.html
    title: Linux Virtual Server project, Job Scheduling Algorithms in Linux Virtual Server
    locator: the section on weighted round-robin scheduling (weights 4, 3 and 2 give the sequence AABABCABC)
  - paper: "Carl A. Waldspurger and William E. Weihl, Stride Scheduling: Deterministic Proportional-Share Resource Management, technical memorandum MIT/LCS/TM-528, MIT, 1995"
    locator: the basic stride algorithm, for the comparison with a deterministic proportional-share CPU scheduler
---

Weighted round robin (WRR) is a [load balancer](/load-balancer/) policy that gives backend $j$ a share $w_j / W$ of the requests, where $w_j \ge 0$ is an integer weight and $W = \sum_j w_j$. Every version sends exactly $w_j$ of each cycle of $W$ requests to backend $j$; the versions differ in the order of the picks inside the cycle. The *smooth* form of nginx keeps a counter per backend: at each pick it adds $w_j$ to every counter, takes the backend with the largest counter and subtracts $W$ from it. Its picks are spread out, so a heavy backend never gets a whole pick ahead of its fair share.

## In plain words

Three cashiers work at different speeds: the first can serve five customers in the time the other two serve one each. A greeter sends customers to them. The simple way is to send five customers in a row to the first cashier, then one to each of the others. That keeps the right proportion, but the fast cashier gets a burst of five at once while the other two wait.

The smooth way works like a savings account for each cashier. Before each customer, every cashier's account grows by that cashier's weight. The cashier with the most money gets the customer and pays back the total of all weights. The fast cashier saves quickly, so it is chosen often, but never many times in a row, and after one full cycle every account is back at zero.

## The problem

The model has $n$ backends with integer weights $w_0, \ldots, w_{n-1} \ge 0$, $W = \sum_j w_j > 0$, and a stream of requests in any order (the arrival model can be adversarial). The balancer must choose a backend for each request online and deterministically. The goal is proportional share by count: after $t$ picks, backend $j$ should have about $t\,w_j / W$ requests, exactly $w_j$ in each cycle of $W$ picks, and its picks should be spread out instead of sent in a block. The weights usually stand for capacity: a backend with twice the CPU gets twice the weight. As in [round robin](/round-robin-load-balancing/), the policy does not see request costs or backend load.

## The algorithm

The state is one integer counter $c_j$ per backend, all 0 at the start.

```pseudo id=main
SWRR-PICK(B, w, c)             ▷ weights w[0..n−1] ≥ 0 with a positive sum; counters c[0..n−1]
L1  W ← 0; best ← none
L2  for j ← 0 to n − 1 do
L3      c[j] ← c[j] + w[j]
L4      W ← W + w[j]
L5      if best = none or c[j] > c[best] then best ← j
L6  c[best] ← c[best] − W
L7  return B[best]
```

Line L3 raises every counter by the weight of its backend, and line L4 sums the weights. Line L5 keeps the first backend with the largest counter. Line L6 charges the chosen backend the total weight. Lines L3 and L6 together keep the sum of the counters at 0: one pick adds $W$ in total and removes $W$.

The counter has a direct meaning. After $t$ picks, $c_j = t\,w_j - W k_j$, where $k_j$ is the number of picks of $j$ so far, so $c_j / W = t\,w_j/W - k_j$ is how far backend $j$ is behind its fair share. Line L5 picks the backend that is furthest behind once the current pick is counted.

nginx runs this loop over the backends that are up and not over their failure limit. It uses a second weight, `effective_weight`, in line L3: it starts equal to the configured weight, drops when the backend fails, and grows back by one per pick until it reaches the configured weight again. This slowly returns traffic to a backend that recovers.

## Example

Weights $5, 1, 1$ for backends $a, b, c$, so $W = 7$. The table shows the counters after line L3 and after line L6 of each pick. These are the values in the message of the nginx change.

| pick | counters after L3 | chosen | counters after L6 |
|---|---|---|---|
| 1 | 5, 1, 1 | a | −2, 1, 1 |
| 2 | 3, 2, 2 | a | −4, 2, 2 |
| 3 | 1, 3, 3 | b | 1, −4, 3 |
| 4 | 6, −3, 4 | a | −1, −3, 4 |
| 5 | 4, −2, 5 | c | 4, −2, −2 |
| 6 | 9, −1, −1 | a | 2, −1, −1 |
| 7 | 7, 0, 0 | a | 0, 0, 0 |

After 7 picks, $a$ has 5, $b$ has 1 and $c$ has 1, and all counters are 0 again, so pick 8 starts the same cycle. The old nginx code gave the order c b a a a a a for these weights.

The order inside a cycle is what the versions change. The longest run counts consecutive picks of one backend, with the cycle read in a loop. The largest gaps are the largest distances between two picks of the same backend, for $a$, $b$ and $c$.

| weights | version | one cycle | longest run | largest gaps |
|---|---|---|---|---|
| 5, 1, 1 | classic (blocks) | a a a a a b c | 5 | 3, 7, 7 |
| 5, 1, 1 | LVS (gcd steps) | a a a a a b c | 5 | 3, 7, 7 |
| 5, 1, 1 | smooth | a a b a c a a | 4 | 2, 7, 7 |
| 4, 3, 2 | classic (blocks) | a a a a b b b c c | 4 | 6, 7, 8 |
| 4, 3, 2 | LVS (gcd steps) | a a b a b c a b c | 2 | 3, 4, 6 |
| 4, 3, 2 | smooth | a b c a b a c b a | 2 | 3, 3, 5 |

The ideal gaps for $4, 3, 2$ are $9/4$, $3$ and $9/2$. The smooth order is closest to them.

## Correctness

The proof rests on two facts. First, $c_j(t) = t\,w_j - W k_j(t)$ and the counters sum to 0. Second, $c_j(t) > -W$ always: the counters after line L3 sum to $W$, so the largest one is positive, and the chosen backend keeps more than $-W$ after line L6. If backend $j$ were picked $w_j + 1$ times within the first $W$ picks, its counter would be at most $W w_j - W(w_j + 1) = -W$, which is impossible. So each backend gets at most $w_j$ of the first $W$ picks, and since the counts sum to $W$, exactly $w_j$. Then all counters are 0 again, the sequence has period $W$, and every window of $W$ consecutive picks, at any start, gives backend $j$ exactly $w_j$ picks. The same facts give the burst bound $k_j(t) < t\,w_j/W + 1$ at every $t$, and for $n \ge 2$ the lag bound $k_j(t) > t\,w_j/W - (n - 1)$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Time per pick.** The loop of line L2 visits all $n$ backends, so a pick costs $\Theta(n)$ in every case. For tens of backends this is a few hundred instructions.
- **Space.** One counter per backend, $\Theta(n)$. The counters stay in the range $(-W, (n - 1)W)$ by the proof, so they fit in a machine word whenever $n W$ does.
- **Faster picks.** With fixed weights the sequence has period $W$, so a table of one cycle gives $O(1)$ per pick with $\Theta(W)$ memory. A [priority queue](/priority-queue/) keyed by the lag does not help directly, because line L3 changes every key at each pick.
- **LVS.** The gcd-based version scans the list once for each value of its threshold, $\max_j w_j / g$ scans per cycle of $W / g$ picks, where $g$ is the gcd of the weights. That is $n \max_j w_j / W \le n$ steps per pick on average, and up to $n$ steps for one pick.

## Properties

- **Exact share per cycle.** Every window of $W$ consecutive picks gives backend $j$ exactly $w_j$ picks, in any arrival order, because the sequence does not depend on the requests at all.
- **Bounded lead.** No backend is ever a whole pick ahead of its fair share $t\,w_j/W$ (Theorem 2 of the proof). The lag bound that the proof gives is $n - 1$. In an exhaustive check of all weight vectors with $n \le 4$ and weights 0 to 6, the largest lag was $11/12$; over 3000 random weight vectors with $n \le 8$ and weights up to 100, it was about 1.30.
- **Zero weights.** A backend with weight 0 is never picked: its counter never rises above 0, and the chosen counter is positive.
- **Deterministic.** Two balancers with the same weights and start state make the same picks. Many proxies that start at the same moment therefore send their first requests to the same backend; a random start state per proxy avoids this.
- **Blind to load.** Like [round robin](/round-robin-load-balancing/), it balances counts, not work. With weights that match capacity and requests of similar cost, the expected utilization of the backends is equal.

## Variants and improvements

- **Classic WRR.** Send $w_0$ requests in a row to backend 0, then $w_1$ to backend 1, and so on. It is exact per cycle but bursty: a backend with a large weight gets all its requests back to back.
- **Interleaved WRR.** Make rounds $r = 1, \ldots, \max_j w_j$, and in round $r$ visit, in list order, the backends with $w_j \ge r$. The LVS scheduler of Wensong Zhang does this in reverse with a threshold: it keeps a current weight $cw$, starts it at $\max_j w_j$, lowers it by $g = \gcd(w_0, \ldots, w_{n-1})$ after each scan of the list (the gcd comes from the [Euclidean algorithm](/euclidean-algorithm/)), and returns each backend whose weight is at least $cw$. The step $g$ removes rounds in which the same backends would repeat. For weights 4, 3, 2 it gives a a b a b c a b c, as in the LVS documentation. Its bursts are shorter than those of the classic form, but for one dominant weight, such as 5, 1, 1, it still sends the whole surplus of the heavy backend in a row.
- **Smooth WRR.** The algorithm of this page. It is in nginx since 1.3.0 (May 2012).
- **[Weighted random](/weighted-random-load-balancing/).** Pick backend $j$ with probability $w_j / W$. No shared counter is needed, so many balancers can run without coordination, but the share is exact only in expectation.
- **Earliest deadline order.** Give each backend a virtual finish time that grows by $1/w_j$ per pick and pick the smallest, with a heap. This is [stride scheduling](/stride-scheduling/) applied to requests, and it costs $O(\log n)$ per pick.

**Relation to proportional-share CPU scheduling.** Weighted round robin is the request-routing analogue of [stride scheduling](/stride-scheduling/): both are deterministic and give each client a share in proportion to its weight. Stride scheduling gives time quanta of one CPU to processes and picks the smallest pass value, which grows by $1/t_j$ per quantum; smooth WRR gives whole requests to servers and picks the largest lag. [Weighted random](/weighted-random-load-balancing/) choice is in the same way the analogue of [lottery scheduling](/lottery-scheduling/). Packet schedulers such as [deficit round robin](/deficit-round-robin/) and [weighted fair queueing](/weighted-fair-queueing/) also use weights, but they share the bytes of one link among flows; weighted round robin for servers spreads requests, and it does not look at their size.

## When to use it

Use weighted round robin when the backends differ in capacity, the requests have similar cost, and the weights are known, for example a pool of machines of two hardware generations. Prefer the smooth form to the classic one, since it costs the same and avoids bursts. When request costs vary, or when the real capacity of a backend changes at run time, a load-aware policy such as [weighted least connections](/weighted-least-connections/) or [peak EWMA](/peak-ewma/) adapts, and weighted round robin does not. When many independent balancers share the same backends, [weighted random](/weighted-random-load-balancing/) choice needs no shared state.

## Pitfalls

- **Picking the minimum instead of the maximum.** If line L5 keeps the smallest counter, the same backend is picked again and again, because its counter only falls. Line L5 must keep the largest counter.
- **Subtracting the wrong total.** Line L6 must subtract the sum of the weights of the backends that took part in line L3. If it subtracts the sum over all configured backends while some are down, the counters drift down and the shares are wrong until a reset.
- **Changing the weights without a reset.** The exact-share proof needs counters that sum to 0. After a weight change or a change of the up set, reset all counters to 0, or accept a short period of error.
- **Weights as relative speed only.** A weight of 2 means twice the requests, not twice the work. A backend that is twice as fast but gets requests that are twice as expensive is overloaded with weight 2.
- **One cycle per connection.** A balancer that runs WRR per TCP connection can still put most requests on one backend when one connection carries most of the traffic.

## Implementations

## History

The gcd-based weighted round robin is in the IPVS scheduler of the Linux Virtual Server project by Wensong Zhang; the kernel file `net/netfilter/ipvs/ip_vs_wrr.c` names him as the author. Maxim Dounin changed the upstream balancer of nginx to the smooth form in 2012, in the commit "Upstream: smooth weighted round-robin balancing" (nginx svn trunk r4622), which also added `effective_weight`. The change log lists the bug fixes of that commit under nginx 1.3.0 of 15 May 2012.

## References
