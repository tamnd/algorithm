---
title: FIFO with drop of late requests serves the most requests on time
proves: [correctness]
status: full
---

**Model.** One server serves one request at a time and does not preempt. Request $j$, for $j = 1, \ldots, n$, arrives at time $a_j$, needs $s$ ticks of service, and is *on time* if it completes by $a_j + T$, where $T \ge s$ is the same client timeout for all requests. Number the requests so that $a_1 \le a_2 \le \cdots \le a_n$. Shedding a request costs no server time. A *schedule* picks a set of requests and a start time $\sigma_j \ge a_j$ for each picked request, with no two service intervals $[\sigma_j, \sigma_j + s)$ overlapping. It is *feasible* if each picked request is on time: $\sigma_j + s \le a_j + T$. A schedule may know all arrivals in advance and may leave the server idle on purpose.

**The greedy rule G.** This is lines L6 to L10 of the page with $D = T - s$ and FIFO order. Whenever the server is free at time $t$, G removes from the queue each request $j$ with $t - a_j > T - s$, which is the same as $t + s > a_j + T$, and starts the oldest request that is left. If none is left, G waits for the next arrival. A request removed at time $t$ can never be on time later, because $t + s > a_j + T$ stays true as $t$ grows. So G never drops a request that could still be served on time at that moment, and every request that G starts is on time.

**Theorem.** For every arrival sequence, the number of on-time requests of G is at least that of every feasible schedule.

*Step 1: an optimal schedule in arrival order.* Take a feasible schedule $O$ with the most on-time requests. Suppose $O$ serves $j$ at $\sigma$ and $i$ at $\sigma' > \sigma$ with $i < j$. Swap them: serve $i$ at $\sigma$ and $j$ at $\sigma'$. The busy intervals do not change, so there is still no overlap. Request $i$ may start at $\sigma$, since $a_i \le a_j \le \sigma$, and it ends at $\sigma + s < \sigma' + s \le a_i + T$. Request $j$ may start at $\sigma'$, since $a_j \le \sigma < \sigma'$, and it ends at $\sigma' + s \le a_i + T \le a_j + T$. The swap removes one inversion and keeps the count, so after a finite number of swaps $O$ serves its requests $j_1 < j_2 < \cdots < j_m$ at times $\sigma_1 < \sigma_2 < \cdots < \sigma_m$, with $\sigma_{k+1} \ge \sigma_k + s$.

*Step 2: G serves in arrival order.* Suppose G starts request $h$ at time $t$ and request $x < h$ has not been served. Then $a_x \le a_h \le t$, so $x$ was in the queue at time $t$, and G passed over it only because it was too late at $t$. Then $x$ is too late at every later time, and G never serves it. So the requests that G serves have increasing indices.

*Step 3: G stays ahead.* Let G serve $h_1 < h_2 < \cdots$ at times $\gamma_1 < \gamma_2 < \cdots$. We show by induction on $k = 1, \ldots, m$ that G serves at least $k$ requests, with $\gamma_k \le \sigma_k$ and $h_k \le j_k$.

Fix $k$, and assume the claim for $k - 1$. Let $f = \gamma_{k-1} + s$ be the time at which G is free after its $(k-1)$-th request, with $f = 0$ and $h_0 = 0$ when $k = 1$. By the induction hypothesis, $f \le \sigma_{k-1} + s \le \sigma_k$; for $k = 1$ this is $0 \le \sigma_1$.

Request $j_k$ has not been served by G before $f$: G has served only $h_1, \ldots, h_{k-1}$, and $h_{k-1} \le j_{k-1} < j_k$. Request $j_k$ has not been dropped by G before $\sigma_k$ either: at each time $t \le \sigma_k$ we have $t + s \le \sigma_k + s \le a_{j_k} + T$, so $j_k$ is not too late at $t$.

Let $t^* = \max(f, a_{j_k})$. Then $t^* \le \sigma_k$, because $f \le \sigma_k$ and $a_{j_k} \le \sigma_k$. G is free from time $f$ on until it starts its next request. At time $t^*$, request $j_k$ has arrived, is not served, and is not too late. So if G has not started a request in $[f, t^*)$, it starts one at $t^*$. In both cases $\gamma_k \le t^* \le \sigma_k$. The request $h_k$ that G starts is the oldest request in the queue that is not too late. If G starts it at a time $t < a_{j_k}$, then $a_{h_k} \le t < a_{j_k}$, so $h_k < j_k$. If G starts it at $t^* = a_{j_k}$ or at $t^* = f \ge a_{j_k}$, then $j_k$ is a candidate, and the oldest candidate has $h_k \le j_k$. This proves the claim for $k$.

With $k = m$, G serves at least $m$ requests, and all of them are on time. $\square$

**Remarks.** The proof uses two facts that the general problem lacks. All service times are equal, so a swap in Step 1 does not change the busy intervals. All timeouts are equal, so arrival order is also deadline order. With unequal service times, maximizing the number of on-time jobs on one machine with release dates is NP-hard, and the greedy rule can be far from optimal. With unequal timeouts, the greedy rule must use the earliest deadline instead of the earliest arrival, and the proof above does not cover it.
