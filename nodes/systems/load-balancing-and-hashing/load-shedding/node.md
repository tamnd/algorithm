---
tag: Q0Y7AN
kind: technique
slug: load-shedding
name: Load shedding
aliases:
- request shedding
area: systems/load-balancing-and-hashing
level: intro
summary: "An overloaded server refuses or drops part of its work so that the rest still finishes before clients give up. It sheds by priority, by time in queue, or above a concurrency limit."
prereqs: [load-balancer, queue]
see_also: [admission-control, backpressure, throttling, rate-limiter, codel, health-checking, least-connections, peak-ewma]
sources:
  - book: isbn:9781491929124
    title: Betsy Beyer, Chris Jones, Jennifer Petoff and Niall Richard Murphy (editors), Site Reliability Engineering, O'Reilly, 2016
    locator: "Chapter 21, Handling Overload, by Alejandro Forero Cuervo (criticality classes CRITICAL_PLUS to SHEDDABLE, client-side adaptive throttling with the multiplier K = 2, retry budgets); Chapter 22, Addressing Cascading Failures, by Mike Ulrich (the sections Queue Management, Load Shedding and Graceful Degradation, and Latency and Deadlines)"
  - paper: doi:10.1145/2838344.2839461
    title: Ben Maurer, Fail at scale, reliability in the face of rapid change, ACM Queue 13(8), 2015, pages 30 to 46
    locator: the part on queues (controlled delay with the parameters M and N, adaptive LIFO, and concurrency control at the client)
  - paper: doi:10.1145/2208917.2209336
    title: Kathleen Nichols and Van Jacobson, Controlling queue delay, ACM Queue 10(5), 2012
    locator: good queue and bad queue, and the use of the minimum sojourn time over an interval as the signal
  - url: https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/adaptive_concurrency_filter
    title: Envoy Proxy documentation, Adaptive Concurrency filter
    locator: "the sections Gradient Controller, Calculating the minRTT, The Gradient (gradient = (minRTT + B) / sampleRTT) and Concurrency Limit Headroom (new limit = gradient times limit plus the square root of the limit)"
  - url: https://github.com/Netflix/concurrency-limits
    title: Netflix, concurrency-limits library, README
    locator: "the limit as average rate times average latency (Little's law), and the Vegas and Gradient2 limit algorithms"
---

Load shedding is the technique by which an overloaded server refuses or drops part of the work it is offered, so that the work it keeps still finishes in time to be useful. The goal is *goodput*, the rate of responses that reach a client before the client gives up, not throughput: a server that answers every request late does full work for no result. The three common forms shed the least important requests first (*priority shedding*), drop requests that have waited too long in the queue (*queue-time shedding*, in the style of [CoDel](/codel/)), or cap the number of requests in progress and adapt the cap to the measured latency (*adaptive concurrency limits*). It acts on the server's own measured overload, and that is how it differs from a [rate limiter](/rate-limiter/), which enforces a fixed rate per client, and from [backpressure](/backpressure/), which asks the sender to slow down instead of dropping work.

## In plain words

A small café has one cook. At lunch, twice as many orders come in as the cook can make. If the cook makes every order in turn, the queue grows, and soon each meal is ready only after its customer has left. The cook works hard all day and nobody eats.

So the café throws away tickets. One rule: if a ticket has waited longer than a customer will wait, throw it away before cooking. Another rule: when the rail is full, throw away the ticket for a coffee before the ticket for a lunch that was paid in advance. A third rule: never let more than five tickets wait at once, and turn new customers away at the door.

Each rule makes some customers unhappy at once. In exchange, every meal the cook makes is eaten.

## When it applies

- Demand can exceed capacity for a while: a traffic spike, a [failover](/failover/) that moves the load of a lost server onto the others, or a retry storm. Adding servers takes minutes, and the overload lasts seconds to minutes.
- Clients have deadlines. A client waits for some time, then gives up, and often retries. Work on a request whose client has gone is wasted.
- The server can tell that it is overloaded: its queue is long, requests wait long in it, its CPU is saturated, or its latency rises above the latency it has with no queue.
- The model of this page: an integer clock; one server that serves one request at a time and does not preempt; each request needs $s$ ticks of service; request $j$ arrives at $a_j$, has a priority class, and is *on time* if it completes by $a_j + T$, where $T$ is the client timeout; the server may refuse a request at arrival or drop it from the queue, and this costs no server time. Goodput is the number of on-time completions per tick. The arrival sequence is arbitrary unless a claim says otherwise. With $c$ servers or a variable $s$ the same rules apply, but the theorems below need the model as stated.

## The template

The three forms act at two points: at arrival (lines L1 to L5) and when the server takes the next request (lines L6 to L10).

```pseudo id=main
ARRIVE(r, now)
L1  if OUTSTANDING() ≥ ⌊L⌋ then reject r; return       ▷ concurrency limit
L2  append r to Q
L3  if |Q| > C then                                     ▷ priority shedding
L4      v ← the request in Q of the lowest class, the newest among equals
L5      remove v from Q; reject v

NEXT(now)                                               ▷ when the server is free
L6  while Q is not empty
L7      r ← the oldest request in Q (the newest in LIFO mode)
L8      remove r from Q
L9      if now − r.arrival > D(now) then drop r; continue     ▷ queue-time shedding
L10     serve r; return
```

$\text{OUTSTANDING}()$ counts the requests that wait or are in service. The cap $C$ on the queue and the limit $L$ can be infinite, and the queue timeout $D$ can be infinite, so each form can be used alone. $D$ is either a constant, usually $T - s$, or the *controlled delay* rule of Maurer: $D(now) = M$ if the queue has not been empty at any time in the last $N$ ticks, and $D(now) = N$ otherwise. With an adaptive limit, the server changes $L$ after each window of completions; the gradient rule of Envoy sets

$$ L \leftarrow \frac{\text{minRTT}\,(1 + b)}{\text{sampleRTT}} \, L + \sqrt{L}, $$

where minRTT is the response time with no queue, sampleRTT is the response time in the last window, and $b$ is a slack fraction. When the queue grows, sampleRTT rises and $L$ falls; when there is no queue, the $\sqrt{L}$ term lets $L$ grow.

**Theorem 1 (collapse without shedding).** One request arrives every $p$ ticks, at times $0, p, 2p, \ldots$, with $p < s$, and the server is FIFO with no shedding. Then request $k$ (from 0) completes at $(k + 1)s$, its response time is $s + k(s - p)$, and the number of on-time responses over the whole run is $\lfloor (T - s)/(s - p) \rfloor + 1$ if $T \ge s$, and 0 if $T < s$.

*Proof.* Request 0 starts at 0. If request $k - 1$ completes at $ks$, then request $k$ has arrived, because $kp < ks$, and it is the oldest request in the queue, so it starts at $ks$ and completes at $(k + 1)s$. Its response time is $(k + 1)s - kp = s + k(s - p)$. This grows with $k$, so the on-time requests are those with $s + k(s - p) \le T$, which are $k = 0, \ldots, \lfloor (T - s)/(s - p) \rfloor$ when $T \ge s$. $\square$

So the throughput stays at its maximum, one response every $s$ ticks, while the goodput falls to 0 after a finite time. A bigger queue only delays the collapse.

**Theorem 2 (queue-time shedding is optimal).** Let $D = T - s$ and let the queue be FIFO. For every arrival sequence, lines L6 to L10 give the largest number of on-time responses of any schedule on one non-preemptive server, even a schedule that knows all future arrivals and may idle on purpose. Every response it sends is on time.

The proof is in [the correctness proof](proofs/correctness.md). It first puts an optimal schedule in arrival order by exchanges, which works because all service times and all timeouts are equal, and then shows that the $k$-th request of the greedy rule starts no later than the $k$-th request of the optimal schedule.

**Corollary (full goodput under steady overload).** With one arrival every $p \le s$ ticks from time 0 and $T - s \ge p - 1$, the FIFO server with $D = T - s$ and no other shedding is never idle from time 0, so it completes one on-time response every $s$ ticks, which is the most any policy can do.

*Proof.* Let the server be free at time $t$, and let $a$ be the latest arrival time with $a \le t$, so $t - a \le p - 1 \le D$. That request has not been served: a request served earlier would have started at some $t' \le t - s$, so it arrived at most at $t - s \le t - p$, and then another request arrived in $(a, t]$, against the choice of $a$. It has not been dropped either, since its wait has never been above $p - 1 \le D$. So line L9 keeps at least one request, and the server starts a request at $t$. Each started request is on time by line L9. $\square$

**Theorem 3 (a concurrency limit bounds the response time).** With FIFO, no queue timeout, and the limit $L$ of line L1 held fixed, every admitted request completes within $\lfloor L \rfloor \cdot s$ ticks of its arrival. So with $L = \lfloor T/s \rfloor$ no admitted request is late.

*Proof.* Let $\ell = \lfloor L \rfloor$. At admission, at most $\ell - 1$ requests are outstanding, and with FIFO all of them are served first. If one of them is in service, it completes within $s$ ticks; each of the others then takes $s$ ticks; the server is never idle while a request waits, since only line L9 can skip a request. So the new request starts within $(\ell - 1)s$ ticks and completes within $\ell s$. $\square$

**Priority shedding.** Lines L3 to L5 keep this invariant: a request is never shed while a request of a strictly lower class waits in the queue. So in a long overload the lowest classes absorb all the loss first.

**Cost.** Each form adds $O(1)$ work per request, plus $O(\log C)$ for priority shedding with a heap per queue, or $O(1)$ with one FIFO list per class. The gradient update is $O(1)$ per window. The price is tuning: each form needs a parameter ($D$, $M$ and $N$, $C$, or the start and range of $L$), and none of the adaptive forms has a worst-case guarantee.

**Example.** $s = 4$, $T = 20$, one arrival every $p = 2$ ticks from time 0 to 100, so 51 arrivals and twice the load the server can carry. The server can complete at most 25 requests by time 100.

| policy | completed | on time | shed | largest response time |
|---|---|---|---|---|
| FIFO, no shedding | 25 | 9 | 0 | 52 |
| FIFO, drop at wait above 16 | 25 | 25 | 17 | 20 |
| LIFO, drop at wait above 16 | 25 | 25 | 0 | 4 |
| FIFO, limit $L = 5$ | 25 | 25 | 21 | 20 |

Without shedding, Theorem 1 gives $\lfloor 16/2 \rfloor + 1 = 9$ on-time responses: the response times are $4, 6, 8, \ldots$, and from request 9 on, which completes at time 40 with a response time of 22, every response is late. With the queue timeout of 16, the first requests behave the same, and then the server starts to drop: request 9, which arrived at 18, has waited 18 ticks at time 36, so line L9 drops it, and so on for every second request. From then on each response time is exactly 20, the most that is still on time. LIFO serves the newest request, so each response takes 4 ticks; the old requests stay at the bottom of the stack until line L9 drops them, so LIFO has shed none of them by time 100, and 25 of them still wait there. With the limit $L = 5 = T/s$, 21 requests are refused at arrival and each response takes at most $5 \cdot 4 = 20$ ticks, as Theorem 3 says.

**A random overload.** With the same $s$ and $T$, arrivals are random: at each tick, four independent trials each add a request with probability $1/8$, so on average 0.5 requests arrive per tick and the load is about twice the capacity. Each request gets one of three classes at random. With seed 1 and ticks 0 to 2000, there are 982 requests, and the server can complete at most 500. Response times are given as the 50th and 99th percentiles by nearest rank.

| policy | completed | on time | shed | median | 99th percentile |
|---|---|---|---|---|---|
| FIFO, no shedding | 499 | 9 | 0 | 491 | 995 |
| FIFO, drop at wait above 16 | 499 | 499 | 474 | 19 | 20 |
| controlled delay, $M = 4$, $N = 20$ | 482 | 482 | 495 | 8 | 19 |
| adaptive LIFO after 20 ticks, drop above 16 | 497 | 497 | 247 | 5 | 18 |
| fixed limit $L = 5$ | 499 | 499 | 478 | 19 | 20 |
| gradient limit, $b = 0.25$, window 5, start 10 | 496 | 488 | 483 | 11 | 28 |
| priority, queue cap $C = 4$ | 499 | 499 | 479 | 16 | 19 |

With priority shedding, the on-time responses by class are 37 of 320 requests of the lowest class, 151 of 329 of the middle class, and 311 of 333 of the highest. Every other policy treats the classes about the same. Controlled delay serves fewer requests than the fixed timeout, because its short timeout $M$ sometimes drops the whole queue, and then the server is idle until the next arrival. The gradient limit starts at 10, which is too high: all 8 of its late responses complete in the first 70 ticks, while the limit falls. From tick 100 on, its limit stays between 2.5 and 4.8.

## Classic examples

- **Criticality at Google.** Each request carries one of four classes, CRITICAL_PLUS, CRITICAL, SHEDDABLE_PLUS and SHEDDABLE, and the class propagates to the requests it causes downstream. An overloaded backend rejects the lower classes sooner. Rejected requests are not free, so clients also throttle themselves: each client keeps, for the last two minutes, its number of requests and the number the backend accepted, and rejects a new request locally with probability $\max(0, (\text{requests} - K \cdot \text{accepts})/(\text{requests} + 1))$, with $K = 2$ in the usual setting. Retries are capped at three attempts per request and at 10 percent of requests per client.
- **Controlled delay at Facebook.** Maurer describes servers whose queue timeout is a short $M$ while the queue has stayed non-empty for $N$ milliseconds, and $N$ otherwise. A burst that the server clears within $N$ is absorbed; a standing queue is cut to $M$. The idea comes from [CoDel](/codel/), which drops packets by sojourn time in a router.
- **Adaptive LIFO.** In the same servers, the queue is FIFO in normal operation and turns LIFO when a queue forms, so the newest requests, whose clients are still waiting, are served first. HHVM, Facebook's PHP runtime, implements it.
- **Adaptive concurrency in Envoy.** The adaptive concurrency filter measures minRTT by pinning the limit to a small value for a short time, then updates the limit with the gradient rule above. The filter blocks the requests over the limit instead of queueing them.
- **Netflix concurrency-limits.** The library sets the limit with Little's law, limit equals average rate times average latency, and adapts it with Vegas, which estimates the queue as $L(1 - \text{minRTT}/\text{sampleRTT})$ and adds 1 to $L$ when that is below $\alpha$ or subtracts 1 when it is above $\beta$, or with Gradient2.

## Variations

- **Where to shed.** At the server, after the request has used the network and some CPU to parse; at the [load balancer](/load-balancer/), which can see queue lengths through [least connections](/least-connections/) or [peak EWMA](/peak-ewma/) and refuse before forwarding; or at the client, which saves the most work.
- **Signals.** Queue length, time in queue, CPU or memory use, latency above minRTT, or the fraction of requests that miss their deadline. Time in queue is robust because it does not depend on the request size or the number of workers. CPU use alone reacts late when the bottleneck is a lock or a downstream service.
- **Deadline propagation.** Each request carries its absolute deadline. A server drops a request whose deadline has passed or is too close to finish, and it gives its own calls to other services the remaining time. This is line L9 with a per-request $T$.
- **Graceful degradation.** Instead of rejecting, serve a cheaper answer: a cached result, fewer search results, no personalization. It sheds work, not requests.
- **Shedding and admission control.** [Admission control](/admission-control/) is the general decision to accept or refuse work at entry. Load shedding is the form that reacts to the server's measured overload, and it also drops work already admitted (line L9).
- **Shedding and rate limiting.** A [rate limiter](/rate-limiter/), built for example on a [token bucket](/token-bucket/), and [throttling](/throttling/) enforce a contract per client at a fixed rate, even when the server is idle. Load shedding has no per-client contract and acts only when the server is overloaded. The two combine well: the limiter stops one client from taking all the capacity, and shedding protects the server from the total.
- **Shedding and backpressure.** [Backpressure](/backpressure/) slows the producer and loses nothing, but it needs a producer that can wait, such as a stage in a pipeline. Open-loop clients on the Internet do not wait, so the server must shed.
- **Shedding and CoDel in a router.** CoDel drops packets so that TCP senders slow down; the drop is the signal. A server that sheds a request saves the work of serving it; a client does not slow down unless it throttles itself.

## Pitfalls

- **Shedding is not free.** Parsing a request, logging and sending an error costs CPU. If the overload is high enough, the server spends all its time rejecting. The fix is to reject as early and as cheaply as possible, and to throttle at the client.
- **Retries multiply load.** A shed request that the client retries at once comes back, and three levels of services that each make up to three attempts turn one request into up to 27. Use retry budgets and [exponential backoff](/exponential-backoff/) with jitter.
- **A queue timeout longer than the client timeout.** If $D > T - s$, the server still serves requests whose clients have gone. Theorem 2 needs $D = T - s$, so the server must know $T$, ideally from a propagated deadline.
- **FIFO under a standing queue.** With FIFO and $D = T - s$, every served request waits almost $D$, so the latency of every success is close to the timeout. LIFO, or a shorter $D$ in a standing queue, gives successes a low latency at the same goodput.
- **LIFO without a timeout.** Pure LIFO starves the oldest requests forever. Pair it with line L9.
- **Health checks that fail under load.** If a shedding server also fails its [health checks](/health-checking/), the balancer removes it, and the other servers get its load and fail in turn. Health checks should test that the server is alive, not that it is idle, and they should not be shed.
- **A limit tuned on one machine.** A fixed $L$ is right only for one service time and one hardware type. When a dependency slows down, the right limit falls. This is why adaptive limits exist, but they have no worst-case guarantee and can oscillate.
- **Shedding the wrong class.** Without priorities, a flood of cheap background requests causes user requests to be shed. Batch work should be the first class to go.

## Exercises

1. In the first example, with no shedding, what is the largest client timeout for which only 9 responses are on time? What is the response time of request 24?
2. With $D = T$ instead of $T - s$, give an arrival sequence for which the server completes a request late. Does it still complete as many on-time requests as with $D = T - s$?
3. Give an instance with two service times, 1 and 10, where FIFO with drop of late requests completes far fewer on-time requests than the best schedule. Which assumption of Theorem 2 does it break?
4. A server has capacity 1000 requests per second and receives 3000. Rejecting a request costs one tenth of serving it. What goodput is left if the server rejects at the last moment, and what if clients throttle with $K = 2$?
5. Prove the priority invariant of lines L3 to L5 by induction over the arrivals.

## References
