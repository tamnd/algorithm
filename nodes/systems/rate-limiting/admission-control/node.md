---
tag: W9QGBX
kind: concept
slug: admission-control
name: Admission control
aliases:
- call admission control
- connection admission control
area: systems/rate-limiting
level: intro
summary: "Decide at entry whether to accept a new flow, call or request, so that all the work already accepted, and the new work, still meets its target for delay, loss or response time."
prereqs: [queue]
see_also: [load-shedding, rate-limiter, throttling, backpressure, token-bucket, cache-admission-policy, distributed-rate-limiting, codel]
sources:
  - paper: doi:10.1109/90.554722
    title: "Sugih Jamin, Peter B. Danzig, Scott J. Shenker and Lixia Zhang, A Measurement-Based Admission Control Algorithm for Integrated Service Packet Networks, IEEE/ACM Transactions on Networking 5(1), pages 56 to 70, 1997"
    locator: "Section II-D (the two admission tests: requested rate plus measured usage against the utilization target, and the delay bound), Section III-A (the measurement process) and Section III-B (the utilization target, 90 percent in the paper)"
  - paper: doi:10.1109/INFCOM.2000.832506
    title: "Lee Breslau, Sugih Jamin and Scott Shenker, Comments on the Performance of Measurement-Based Admission Control Algorithms, Proceedings of IEEE INFOCOM 2000, pages 1233 to 1242"
    locator: "The simulation comparison of several measurement-based admission control algorithms"
  - book: isbn:9780132009164
    title: Dimitri Bertsekas and Robert Gallager, Data Networks, second edition, Prentice Hall, 1992
    locator: "Section 3.3 (the M/M/1 system and its mean delay) and Section 3.4.3 (the m-server loss system M/M/m/m and the Erlang B formula)"
  - paper: doi:10.1287/opre.9.3.383
    title: "John D. C. Little, A Proof for the Queuing Formula L = λW, Operations Research 9(3), pages 383 to 387, 1961"
    locator: The theorem L = λW for a stationary queueing system
  - book: isbn:9783540421849
    title: Jean-Yves Le Boudec and Patrick Thiran, Network Calculus, A Theory of Deterministic Queuing Systems for the Internet, Springer LNCS 2050, 2001
    locator: "Chapter 1 (arrival curves, service curves, and the backlog and delay bounds)"
  - paper: doi:10.1145/502034.502057
    title: "Matt Welsh, David Culler and Eric Brewer, SEDA, An Architecture for Well-Conditioned, Scalable Internet Services, Proceedings of the 18th ACM Symposium on Operating Systems Principles (SOSP 2001), pages 230 to 243"
    locator: "Section 3 (stages with event queues, and admission control on the queue of each stage)"
---

Admission control is the decision, made when new work arrives, to accept or reject it so that the work already accepted, and the new work if it is accepted, still meets a target such as a delay bound, a loss rate or a response time. The work can be a network flow, a telephone call, a connection, or a request to a server. The test uses a model of the system's capacity, declared traffic parameters, measurements of the current load, or a combination of them. It is different from [load shedding](/load-shedding/), which an overloaded server uses to drop or refuse part of its work, often work that is already in its queues, from a [rate limiter](/rate-limiter/), which caps each client at a fixed rate whatever the state of the system, and from a [cache admission policy](/cache-admission-policy/), which decides what to store in a cache.

## In plain words

A restaurant has twenty tables. When all the tables are full, the host tells new guests at the door that there is no table. The guests who are already eating get their food on time, because the kitchen does not take more orders than it can cook.

Admission control is that host. It stands at the entry of a system, looks at how busy the system is, and says yes or no to each new arrival. A no at the door is cheap and clear: the guest can go somewhere else or come back later. A yes that the kitchen cannot keep is worse for everyone, because all the meals get late.

The hard part is to know how much the kitchen can take. Some hosts count the tables. Others watch how long the meals take now and stop the line when the times get too long.

## The idea

**Where the decision is made.** At the entry, before the system spends resources on the new work. The new work is rejected whole, so no work is half done. A rejected client gets an explicit answer and can retry later, go elsewhere, or degrade.

**What the test protects.** The target applies to the admitted work: a delay bound for each packet of a flow, a probability of loss, a mean or percentile response time for requests. Admission control trades the fraction of arrivals that is accepted against the quality that the accepted work gets.

**Parameter-based tests.** Each new flow declares its traffic, for example with a [token bucket](/token-bucket/) of rate $r$ and depth $b$, and the test checks a worst-case bound. For flows into one FIFO link of rate $C$:

- **Theorem.** If flow $i$ conforms to a token bucket $(r_i, b_i)$ and $\sum_i r_i \le C$, the backlog never exceeds $\sum_i b_i$ and the delay of each bit never exceeds $\sum_i b_i / C$.
- **Proof.** Fix a time $t$ and let $s$ be the start of the busy period that contains $t$. The flows send at most $\sum_i (b_i + r_i (t - s))$ in $(s, t]$, and the link serves exactly $C(t - s)$, so the backlog at $t$ is at most $\sum_i b_i + (\sum_i r_i - C)(t - s) \le \sum_i b_i$. In FIFO order a bit that arrives at $t$ leaves when the backlog in front of it is served, after at most $\sum_i b_i / C$. $\square$
- **The test.** Admit a new flow $(r, b)$ if $\sum_i r_i + r \le C$ and $(\sum_i b_i + b)/C \le D$. The guarantee holds for every arrival pattern that conforms to the declared buckets. The cost is low utilization: declared parameters are worst cases, and most flows use much less.

**Measurement-based tests.** The test uses the measured load in place of the declared worst case. In the algorithm of Jamin, Danzig, Shenker and Zhang (1997), a link of bandwidth $\mu$ keeps the largest utilization $\hat\nu$ sampled over a window and the largest measured queueing delay. It denies a new flow with requested rate $r$ if $\hat\nu + r$ would exceed $v\mu$, where $v$ is a utilization target (90 percent in the paper), or if the flow could break the delay bound of its class. After it admits a flow, it adds the flow's worst case to the measured values and restarts the window. The paper says that such algorithms can be checked only by experiment, not by proof: they give higher utilization and an occasional violation of the target. Breslau, Jamin and Shenker (2000) compare several measurement-based algorithms in simulation.

**Loss systems.** With $c$ circuits, Poisson arrivals of rate $\lambda$ and exponential holding times of mean $1/\mu$, a call is admitted when a circuit is free and blocked otherwise. The offered load is $a = \lambda/\mu$ Erlangs. The number of busy circuits is a birth-death chain with $p_k \propto a^k/k!$ for $k = 0, \ldots, c$, and Poisson arrivals see the time averages, so the blocking probability is the Erlang B formula

$$B(c, a) = \frac{a^c / c!}{\sum_{k=0}^{c} a^k / k!}.$$

Here the admission rule is trivial, and the question is how many circuits make the blocking small enough.

**Servers and queues.** A server can admit a request only while fewer than $K$ requests are in it, or only while the measured latency is below a target. Two facts size such limits:

- **Little's law.** In a stable system, the mean number in the system $L$, the throughput $\lambda$ and the mean time in the system $W$ satisfy $L = \lambda W$ (Little, 1961). A limit of $K$ requests in the system therefore gives a throughput of at most $K/W$.
- **A bounded FIFO queue.** With one server, FIFO order and at most $K$ requests in the system, an admitted request finds at most $K - 1$ requests in front of it. If service times are exponential with mean $1/\mu$, the remaining service of the request in service is again exponential with mean $1/\mu$, so the expected wait of an admitted request is at most $(K-1)/\mu$. Under overload, without the limit, the queue and the wait grow without bound.

**What admission control is not.**

- **[Load shedding](/load-shedding/)** is the reaction of a server that is already overloaded: it drops or refuses part of its work, by priority or by time in queue, and can drop requests that it has already queued. Admission control is the test at the door that keeps the admitted work within a target, so that it rejects only new work, and it rejects it whole.
- **[Rate limiting](/rate-limiter/)** caps a client at an agreed rate even when the system is idle. Admission control looks at the state of the system, and in its simplest form it does not look at the client at all.
- **[Backpressure](/backpressure/)** makes the producer wait, through bounded buffers or credits, and loses no work. Admission control rejects work, and the client decides what to do next.
- **[Throttling](/throttling/)** slows a client down on purpose. A client-side throttle can be a local admission controller for the requests that the client sends.
- **[Cache admission](/cache-admission-policy/)** decides whether an item enters a cache. It does not reject the request.

## Examples

**A delay-bounded link.** A link of $C = 100$ Mbit/s with a delay target of $D = 10$ ms has a burst budget of $C D = 1$ Mbit, or 125,000 bytes. Flows with buckets of rate 10 Mbit/s and depth 12,500 bytes each: the rate test admits 10 flows and the delay test also admits 10, since $10 \cdot 12{,}500 = 125{,}000$. If each flow sends 3 Mbit/s on average, the link is only 30 percent busy. A measurement-based test with target $v = 0.9$ sees about 30 Mbit/s and admits more flows, about 20 more of rate 3 Mbit/s each before $\hat\nu + r$ reaches 90 Mbit/s, at the risk of a missed bound when many flows burst at once.

**A measurement-based decision.** With $\mu = 100$ Mbit/s and $v = 0.9$, the threshold is 90 Mbit/s. If the measured utilization is 72 Mbit/s, a flow asking for 15 Mbit/s is admitted, since $87 \le 90$. The test then counts the new flow at its full rate, so the measured value becomes 87, and a second flow asking for 5 Mbit/s is denied, since $92 > 90$.

**Telephone trunks.** Ten circuits with an offered load of 7 Erlangs block $B(10, 7) \approx 7.87$ percent of calls and carry $7 (1 - 0.0787) \approx 6.45$ Erlangs. At 5 Erlangs the blocking is about 1.84 percent, and at 10 Erlangs it is about 21.5 percent. For a load of 7 Erlangs, 14 circuits are the fewest with blocking below 1 percent ($B(14, 7) \approx 0.71$ percent). The numbers come from the formula above with exact fractions.

**A server with a response-time target.** A server that behaves as an M/M/1 queue with service rate $\mu = 100$ requests per second has mean response time $1/(\mu - \lambda)$ at arrival rate $\lambda < \mu$. For a target of 50 ms, the admitted rate must satisfy $1/(100 - \lambda) \le 0.05$, so $\lambda \le 80$. If 120 requests per second arrive, the server admits 80 of them, two thirds, and rejects 40. Without admission control the arrival rate exceeds the service rate and the queue grows without bound.

**A concurrency limit.** A service whose requests spend $W = 0.1$ s inside it and which admits at most $K = 50$ requests at a time serves at most $K / W = 500$ requests per second, by Little's law. With one FIFO worker of mean service time 10 ms and at most $K = 20$ requests in the system, an admitted request waits on average at most $19 \times 10 = 190$ ms.

## Where it is used

- **Telephone networks.** Calls are blocked when no circuit is free. Trunk groups are sized with the Erlang B formula.
- **ATM and integrated services.** Connection admission control and the admission control of RSVP-style reservations check declared traffic parameters against the resources of each link on the path, with parameter-based or measurement-based tests.
- **Differentiated services.** Edge meters such as the [single rate](/single-rate-three-color-marker/) and [two rate](/two-rate-three-color-marker/) three color markers police traffic per customer, and admission control decides which customers and contracts a network can accept.
- **Internet services.** Servers bound the number of requests in progress, the length of their queues, or the measured latency, and return an overload error when the bound is reached. SEDA (Welsh, Culler and Brewer, 2001) puts an admission controller on the queue of each stage.
- **Clusters and schedulers.** A cluster scheduler admits a job only if its requested resources fit, and a database admits a query only while the number of active queries is below a limit.
- **Clients.** A client that rejects some of its own requests when the backend rejects many of them, as in the adaptive [throttling](/throttling/) of the Google SRE book, is a form of admission control at the source.

## References
