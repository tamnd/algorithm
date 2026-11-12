---
tag: K5FA12
kind: technique
slug: health-checking
name: Health checking
aliases:
- active health checks
- passive health checks
- rise and fall thresholds
- outlier ejection
area: systems/load-balancing-and-hashing
level: intro
summary: "A load balancer probes each backend on a timer, or watches its real responses, and takes it out of the pool after a run of failures. Rise and fall counts stop flapping."
prereqs: [load-balancer, failure-detection]
see_also: [failure-detector, phi-accrual-failure-detector, swim, failover, connection-draining, load-shedding, service-discovery, peak-ewma]
sources:
  - url: https://docs.haproxy.org/3.2/configuration.html
    title: HAProxy Configuration Manual, version 3.2
    locator: "Section 5.2, server options check, inter, rise and fall (defaults inter 2000 ms, rise 2, fall 3)"
  - url: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/health_checking
    title: Envoy Proxy documentation, architecture overview, Health checking
    locator: active health checks, unhealthy_threshold and healthy_threshold, and the interaction with outlier detection
  - url: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/outlier
    title: Envoy Proxy documentation, architecture overview, Outlier detection
    locator: "consecutive 5xx, the ejection algorithm, ejection time = base_ejection_time times the number of ejections, the decrement of the multiplier, max_ejection_percent"
  - url: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/load_balancing/panic_threshold
    title: Envoy Proxy documentation, architecture overview, Panic threshold
    locator: the default panic threshold of 50 percent and the routing to all hosts below it
  - book: isbn:9781491929124
    title: Betsy Beyer, Chris Jones, Jennifer Petoff and Niall Richard Murphy (editors), Site Reliability Engineering, O'Reilly, 2016
    locator: Chapter 20, Load Balancing in the Datacenter (identifying bad tasks, lame duck state)
  - paper: doi:10.1145/226643.226647
    title: Tushar Deepak Chandra and Sam Toueg, Unreliable failure detectors for reliable distributed systems, Journal of the ACM 43(2), 1996, pages 225 to 267
    locator: Section 2, the completeness and accuracy properties of failure detectors
---

Health checking is the technique by which a [load balancer](/load-balancer/) decides which backends may receive traffic. *Active* checks send a probe to each backend on a timer and count the answers; *passive* checks, also called outlier detection, watch the status of real responses and eject a backend after a run of errors. A backend leaves the pool after `fall` failures in a row and comes back after `rise` successes in a row, and this hysteresis keeps a flaky backend from flapping in and out. It is a practical [failure detector](/failure-detector/): it can be wrong about a slow backend, and it trades the time to detect a failure against the rate of false removals.

## In plain words

A head waiter sends guests to tables in many rooms. Every few seconds, a helper looks into each room and asks the cook there "are you working?". If the cook does not answer three times in a row, the waiter stops sending guests to that room. If the cook then answers twice in a row, the room is open again. One missed answer does not close a room, because a cook can be busy for a moment.

The waiter also listens to the guests. If five guests in a row come back from a room and say "the food was bad", the waiter closes that room for half a minute, then a full minute the next time, and so on.

If every room fails the check at once, the problem is probably with the check, not with every cook. So the waiter keeps sending guests to all rooms.

## When it applies

- A balancer spreads requests over a pool of backends that can fail, hang, or be restarted, and it must route around them without a person in the loop.
- The balancer cannot read the state of a backend directly. It sees only answers to probes and to real requests, over a network that can delay or lose them. This is the model of the [failure detection](/failure-detection/) problem with one observer per backend.
- The model here: an integer clock; one probe to each backend every $I$ ticks, at times $0, I, 2I, \ldots$; a probe sent at time $s$ sees the state of the backend at $s$; a passing probe reports at $s$, and a failing probe reports at $s + T$, where $T$ is the probe timeout. The thresholds are $r$ (rise) and $f$ (fall), both at least 1.

## The template

The template has three parts: a state machine per backend for active probes, a counter per backend for passive checks, and a rule that decides which backends the balancer may use.

```pseudo id=main
OBSERVE(b, ok)                           ▷ one probe result for backend b
L1  if ok = b.healthy then b.streak ← 0; return
L2  b.streak ← b.streak + 1
L3  if b.streak ≥ (f if b.healthy else r) then
L4      b.healthy ← ok; b.streak ← 0

ON-RESPONSE(h, status, now)              ▷ passive check on a real response
L5  if status < 500 then h.c ← 0; return
L6  h.c ← h.c + 1
L7  if h.c ≥ N and h is not ejected and (ejected + 1) · 100 ≤ P · |hosts| then
L8      h.k ← h.k + 1; h.until ← now + min(h.k · B, M)      ▷ eject h

SWEEP(now)                               ▷ every sweep interval
L9  for each host h do
L10     if h is ejected and now ≥ h.until then return h to service; h.c ← 0
L11     else if h is not ejected and h.k > 0 then h.k ← h.k − 1

ROUTABLE()
L12 G ← the backends that are healthy and not ejected
L13 if |G| · 100 < Q · |backends| then return all backends      ▷ panic mode
L14 return G
```

**The rise and fall machine (lines L1 to L4).** The field *streak* counts consecutive results that disagree with the current state. A result that agrees resets it (line L1). A healthy backend goes down after $f$ failures in a row, and an unhealthy one comes up after $r$ passes in a row. Inside one run of equal results the streak only grows, so the state flips exactly when a run opposes the state and is at least as long as the threshold of the current state. The implementation tests this run rule against the machine on every result sequence up to length 10.

**The outlier ejector (lines L5 to L11).** A host is ejected after $N$ server errors in a row (status 500 to 599) if the share of ejected hosts after the ejection is at most $P$ percent. The $k$-th ejection in a row lasts $\min(kB, M)$, where $B$ is the base ejection time and $M$ the maximum. Each sweep in which the host is in service lowers $k$ by one, so a host that stays good is forgiven step by step. The parameters follow Envoy, whose documented defaults are $N = 5$, a sweep interval of 10 s, $B = 30$ s, $P = 10$ percent, and $M = 300$ s or $B$, whichever is larger. Envoy's docs do not state how the percentage is rounded; the rule of line L7 is this page's choice, and with it a pool of fewer than 10 hosts at $P = 10$ ejects nothing. Envoy has an option, always_eject_one_host, for that case.

**The panic rule (lines L12 to L14).** If fewer than $Q$ percent of the backends are usable, the balancer uses all of them. Envoy calls $Q$ the panic threshold, with a default of 50 percent.

**Detection delay.** Let a backend be up before time $t > 0$ and down from time $t$ on, and let the machine start healthy. Then it marks the backend down exactly at

$$D(t) = \left\lceil t / I \right\rceil I - t + (f - 1) I + T$$

ticks after the failure, so $(f-1)I + T \le D < fI + T$.

*Proof.* Every probe sent before $t$ passes, so the streak is 0 when the first probe after the failure is sent, at $s_1 = \lceil t/I \rceil I$. The probes at $s_1, s_1 + I, \ldots$ all fail, and none of them resets the streak, so the streak reaches $f$ with the probe sent at $s_1 + (f-1)I$, which reports at $s_1 + (f-1)I + T$. Subtract $t$. Since $0 \le \lceil t/I \rceil I - t < I$, the bounds follow, and both are reached: the lower one when $t$ is a probe time, the upper one in the limit just after a probe time. $\square$

On an integer clock the maximum is $fI + T - 1$; the tests check the formula for every failure time in four intervals and for many values of $I$, $T$ and $f$. In the same way, a backend that recovers at time $t$ comes back after $\lceil t/I \rceil I - t + (r - 1)I$ ticks, since passing probes report at once.

**Cost.** OBSERVE and ON-RESPONSE take $O(1)$ time; SWEEP and ROUTABLE take $O(n)$ for $n$ backends. Active checks cost $n/I$ probes per tick for each balancer, so $m$ balancers send $mn/I$ probes per tick in total. In a fleet with many client-side proxies this product is large, which is one reason to rely on passive checks or on a shared health service.

**Example.** HAProxy's defaults are $I = 2000$ ms, $r = 2$ and $f = 3$. With a timeout of 0 (the connection is refused at once), a crash is detected after 4000 to 5999 ms; a probe timeout $T$ adds $T$ to both ends. Here is a backend that starts healthy, with $r = 2$ and $f = 3$:

| probe | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| result | pass | fail | fail | pass | fail | fail | fail | pass | fail | pass | pass |
| streak after | 0 | 1 | 2 | 0 | 1 | 2 | 0 | 1 | 0 | 1 | 0 |
| state after | up | up | up | up | up | up | down | down | down | down | up |

Probes 2 and 3 are two failures, then a pass resets the count, so the backend stays up. Probes 5 to 7 are three failures in a row, so it goes down. Probe 9 resets the rise count, and probes 10 and 11 bring it back.

**Flapping.** A backend that fails each probe with probability 0.3, independently, over 10,000 probes (seed 7): with $r = f = 1$ the state changes 4207 times; with $r = 2$ and $f = 3$ it changes 401 times, and the backend is out of the pool for 677 of the probes. A backend that fails in the pattern fail, fail, pass, repeated, changes state 100 times in 150 probes with $r = f = 1$ and never with $f = 3$.

**Passive trace.** With $N = 5$ and $B = 30$: four 503 answers, one 200, then five 503 answers eject the host at the fifth one, for 30 s. If it fails again at once after it returns, the next ejection is 60 s, then 90 s, up to the cap $M$. With $M = 100$ the sequence is 30, 60, 90, 100, 100.

## Classic examples

- **HAProxy.** The server option `check` turns on active checks, with `inter`, `rise` and `fall` as above. Checks can be a TCP connect, an HTTP request with an expected status, or an agent on the backend that reports a weight.
- **Envoy.** Active checks with an interval, a timeout, `unhealthy_threshold` and `healthy_threshold`; outlier detection with consecutive 5xx, consecutive gateway failures and success-rate statistics; and the panic threshold. A successful active check returns an ejected host and clears its outlier counters.
- **Cloud load balancers.** AWS Application Load Balancers use healthy and unhealthy threshold counts on HTTP checks, and send traffic to all targets when too few are healthy, which AWS calls failing open.
- **Kubernetes probes.** A readiness probe decides whether a pod is in the endpoint list of a service, and a liveness probe decides whether the kubelet restarts the container. Both use a period and failure and success thresholds. Readiness is health checking for the balancer; liveness is a restart policy.
- **Lame duck state.** Google's internal balancing lets a backend tell its clients that it is healthy but going away, so that they stop sending it new work. This is the client side of [connection draining](/connection-draining/).

## Variations

- **Shallow and deep checks.** A shallow check asks whether the process answers (a TCP connect, or a `/ping` that returns 200). A deep check also tests the dependencies of the backend, such as its database. A deep check finds more faults, but a fault in a shared dependency makes every backend fail at once, and the panic rule is then the only thing that keeps traffic flowing.
- **One saturating counter.** Another design keeps one counter between 0 and $r + f - 1$, which a pass raises and a fail lowers, and calls the backend healthy while the counter is at least $r$. It does not need a true run. With $r = 2$ and $f = 3$ and a full counter of 4, the sequence fail, fail, pass, fail, fail ends at 1 and marks the backend down, while the rise and fall machine keeps it up.
- **Faster probes near a change.** HAProxy's `fastinter` and `downinter` change the interval while a backend is in transition or down, to shorten the detection delay without probing healthy backends more often.
- **Success rate outliers.** Instead of a run of errors, eject the hosts whose success rate is far below the mean of the pool. This catches a host that fails one request in five, which never makes five errors in a row.
- **Accrual detectors.** The [phi accrual failure detector](/phi-accrual-failure-detector/) outputs a level of suspicion from the history of heartbeat gaps instead of a count. [SWIM](/swim/) probes a member through other members before it suspects it, and spreads the result by gossip. Both are failure detection among peers of a group; health checking is one-way, from each balancer to each backend.
- **Health from load.** [Least connections](/least-connections/) and [peak EWMA](/peak-ewma/) send less traffic to a slow backend without a binary verdict, which handles the gray zone between up and down.

## Pitfalls

- **Correlated removal.** A deep check that depends on a shared database fails on every backend when the database is slow. Without a panic threshold the balancer removes every backend, and a partial outage becomes a full one.
- **Check passes, traffic fails.** A `/health` handler that returns 200 from a thread that is not blocked, while the worker pool is full, keeps a broken backend in the pool. Passive checks on real traffic close this gap.
- **No hysteresis.** With $r = f = 1$ a backend near its limit flaps in and out, and each return brings a burst of traffic that pushes it over again.
- **Thresholds that are too high.** The detection delay grows as $fI + T$. With $I = 10$ s and $f = 5$, a dead backend receives traffic for up to a minute.
- **A timeout longer than the interval.** Then probes overlap, and an implementation that waits for each probe before it sends the next one stretches the real interval to $T$.
- **Ejection without a cap.** If outlier detection could eject any share of the pool, a bad deploy that makes every host return errors would empty it. The ejection cap and the panic threshold both guard against this.
- **Mixing up detection and accuracy.** A check cannot tell a dead backend from a slow one or from a lost probe. A faster detector makes more false removals; see [failure detector](/failure-detector/) for why no timeout is both complete and accurate in an asynchronous network.

## Exercises

1. With $I = 5$ s, $T = 2$ s and $f = 3$, give the smallest and the largest time from a crash to the removal of the backend.
2. A backend fails each probe with probability $p$, independently. With $f = 3$, what is the expected number of probes until it is first marked down, starting healthy? (Hint: the expected waiting time for three failures in a row.)
3. Take the single saturating counter of the Variations section with $r = 2$, $f = 3$ and a full counter. Show that no sequence of 4 or fewer results marks the backend down without 3 failures in a row, and that fail, fail, pass, fail, fail is the only such sequence of length 5.
4. A pool has 8 hosts, a panic threshold of 50 percent, and a deep check. The database fails and 6 hosts fail the check. What does ROUTABLE return, and what does it return if only 4 hosts fail?

## References
