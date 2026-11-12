---
tag: T00ABF
kind: technique
slug: connection-draining
name: Connection draining
aliases:
- graceful shutdown of servers
- deregistration delay
- lame duck mode
area: systems/load-balancing-and-hashing
level: intro
summary: "Before a backend leaves the pool, the balancer stops sending it new work and lets the requests in flight finish, up to a timeout that cuts the rest."
prereqs: [load-balancer, health-checking]
see_also: [failover, layer-4-load-balancing, layer-7-load-balancing, service-discovery, sticky-sessions, least-connections, load-shedding]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc9113
    title: "M. Thomson and C. Benfield (editors), RFC 9113, HTTP/2, 2022"
    locator: "Section 6.8 (GOAWAY, and the graceful shutdown with a first GOAWAY of last stream identifier 2^31 - 1) and Section 8.7 (requests above the last stream identifier are safe to retry)"
  - url: https://www.rfc-editor.org/rfc/rfc9112
    title: "R. Fielding, M. Nottingham and J. Reschke (editors), RFC 9112, HTTP/1.1, 2022"
    locator: "Section 9.6, Tear-down (the close connection option, and closing in stages with a half-close)"
  - url: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/edit-target-group-attributes.html
    title: Amazon Web Services, Elastic Load Balancing, Application Load Balancers, Edit target group attributes
    locator: "the section Deregistration delay (default 300 seconds, the draining state, early completion when no requests are in flight)"
  - url: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
    title: Kubernetes documentation, Pod Lifecycle
    locator: the section on the termination of pods (the grace period, the preStop hook, and the removal of the pod from the endpoints)
  - book: isbn:9781491929124
    title: Betsy Beyer, Chris Jones, Jennifer Petoff and Niall Richard Murphy (editors), Site Reliability Engineering, O'Reilly, 2016
    locator: "Chapter 20, Load Balancing in the Datacenter (the healthy, refusing connections and lame duck states of a backend task)"
---

Connection draining is the technique of taking a backend out of a [load balancer](/load-balancer/) pool without failing the work it already has. The balancer marks the backend *draining*: it sends it no new requests or connections, it lets the requests in flight finish, and after a timeout it cuts whatever is left and removes the backend. It is how rolling deploys, scale-in and maintenance avoid errors, and it is the planned twin of [failover](/failover/), where the backend leaves without warning. HTTP gives the backend the means to tell clients to go elsewhere: `Connection: close` in HTTP/1.1 and the GOAWAY frame in HTTP/2.

## In plain words

A cashier wants to close her till at the end of a shift. If she just walks away, the people in her line lose their place and must start again. So she puts up a "closed" sign. New customers go to the other tills. She serves the people already in her line, and when the line is empty she leaves.

One customer may have a cart so full that it takes an hour. So the manager gives her a limit: after fifteen minutes, she leaves anyway, and the people still in line are sent to another till.

There is one more trap. If the sign goes up after she has already stopped serving, the people who join in between are turned away. So she must keep serving until everyone has seen the sign.

## When it applies

- A backend leaves the pool on purpose: a new version replaces it, the pool scales in, or the host needs maintenance. A crash gives no time to drain; [health checking](/health-checking/) and failover handle it.
- Requests take time, so at any moment some are in flight. If the backend stopped at once, each of them would fail, and only some clients can retry safely.
- The model of this page: an integer clock; a request that starts at time $a$ with duration $d$ ends at $a + d$; at each tick the balancer finishes the requests that end then, applies the drain deadlines, and routes the new arrivals with [least connections](/least-connections/); a drain of backend $b$ starts at time $s$ with timeout $\tau$, so the deadline is $s + \tau$; the balancer learns of the drain $\ell$ ticks late (the lag until a deregistration reaches every balancer).

## The template

```pseudo id=main
DRAIN(b, now, τ)
L1  b.state ← DRAINING; b.start ← now; b.deadline ← now + τ

ROUTE(r, now)
L2  C ← the backends in state ACTIVE        ▷ a balancer that has not seen a drain still counts b
L3  b ← the member of C with the fewest requests in flight
L4  send r to b; add r to b.inflight

TICK(now), for each backend b
L5  finish each request of b that ends at or before now
L6  if b is DRAINING and now ≥ b.deadline then
L7      cut the requests still in b.inflight; b.state ← REMOVED
L8  else if b is DRAINING, b.inflight is empty and every balancer has seen the drain then b.state ← REMOVED
```

Line L2 is the whole effect of the draining state on new work. Lines L5 to L8 decide when the backend may stop: as soon as it is empty and no balancer can still send to it, or at the deadline, whichever comes first.

**Claim.** In this model, for a drain of backend $b$ that starts at $s$ with deadline $s + \tau$ and lag $\ell$:

1. no request that arrives at time $s + \ell$ or later is sent to $b$;
2. a request on $b$ that ends at or before $s + \tau$ finishes, and a request on $b$ that ends later is cut at $s + \tau$; no request on another backend is cut;
3. $b$ is removed at time $\min(s + \tau,\ \max(s + \ell,\ e))$, where $e$ is the latest end time of a request ever sent to $b$.

*Proof.* (1) From time $s + \ell$ every balancer sees $b$ as draining, and line L2 leaves it out of $C$. (2) A request on $b$ with end $e_r \le s + \tau$ is still in flight at tick $e_r$, since by line L7 the backend has not been cleared before the deadline, and lines L6 to L8 run only after line L5 in the same tick. So line L5 finishes it at tick $e_r$. A request with $e_r > s + \tau$ is still in flight at tick $s + \tau$, and line L7 cuts it. Lines L6 to L8 touch only draining backends. (3) By (1), the requests on $b$ arrive before $s + \ell$, and all have ended by tick $e$. If $\max(s + \ell, e) < s + \tau$, the first tick at which $b$ is empty and every balancer has seen the drain is $\max(s + \ell, e)$, and line L8 fires there. Otherwise line L6 fires at $s + \tau$. $\square$

The implementation checks the three parts on 200 seeded runs with timeouts from 0 to 40 and lags from 0 to 5.

**Cost.** One state field and one deadline per backend; the balancer does no extra work per request. The price is time: a backend that serves long requests can take up to $\tau$ to leave, and a rolling deploy of $k$ batches can take up to $k\tau$ longer than one without draining.

**Example.** Two backends, timeout 6. At time 0, request 1 (length 4) goes to backend 0, request 2 (length 12) to backend 1, and request 3 (length 9) to backend 0. At time 1 backend 0 starts to drain, so its deadline is 7.

| time | event | backend 0 | backend 1 |
|---|---|---|---|
| 0 | requests 1, 2, 3 arrive | 1 (to 4), 3 (to 9) | 2 (to 12) |
| 1 | DRAIN(0, 1, 6) | draining, deadline 7 | |
| 2 | request 4 (length 3) arrives: only backend 1 is in $C$ | | 2, 4 (to 5) |
| 4 | request 1 ends | 3 | |
| 5 | request 4 ends | | 2 |
| 7 | deadline: request 3 is cut (it would end at 9) | removed | |
| 12 | request 2 ends | | empty |

With a timeout of 8 or more, request 3 would finish at 9 and backend 0 would leave at 9 with nothing cut. With a timeout of 0, the drain is an abrupt removal, and every request in flight at time 1 is cut.

**The lag race.** If the backend refuses new work as soon as the drain starts, but a balancer learns of it $\ell$ ticks later, the requests that balancer sends during those $\ell$ ticks fail. In the seeded run of the tests, with $\ell = 5$ and four backends, 2 requests fail this way; when the backend keeps accepting for $\ell$ ticks after the drain starts, none fail. Kubernetes has this race: removing a pod from the endpoints and sending it the termination signal happen in parallel, and a common fix is a preStop hook that waits a few seconds before the server stops accepting.

## Classic examples

- **HTTP/2 GOAWAY.** A server that wants to close a connection sends GOAWAY with the largest stream identifier it will process; the client opens no new streams on the connection, and streams with larger identifiers were never processed, so the client may retry them on a new connection, even when they are not idempotent (RFC 9113, Section 8.7). A one-step GOAWAY races with streams that the client opened while the frame was in flight. RFC 9113, Section 6.8, therefore advises a first GOAWAY with the identifier $2^{31} - 1$, a wait of at least one round trip, and then a second GOAWAY with the real last identifier. Example: one-way delay 3, GOAWAY at 10, streams 1, 3, 5, 7 sent at times 0, 4, 9, 11. One step: the server has received only 1 and 3, so 5 and 7 are refused and must be retried. Two steps: by time 16 all four have arrived, so the last identifier is 7 and nothing is refused.
- **HTTP/1.1 Connection: close.** A draining server adds `Connection: close` to the next response on each persistent connection, closes the connection after that response, and processes no further request on it (RFC 9112, Section 9.6). It closes in stages, with a half-close first, so that a request already on the wire does not cause a TCP reset that destroys the response.
- **Cloud balancers.** AWS calls draining the deregistration delay, with a default of 300 seconds. The target stays in the draining state, gets no new requests, and leaves early if it has no requests in flight and no open connections.
- **Kubernetes.** A terminating pod leaves the endpoints of its service and gets SIGTERM; it then has a grace period, by default 30 seconds, before SIGKILL.
- **Lame duck state.** In Google's datacenter balancing, a backend task can be in a lame duck state: it still serves, but it tells its clients to stop sending it new requests. The clients do the draining.

## Variations

- **Layer 4 and layer 7.** A [layer 7](/layer-7-load-balancing/) balancer sees each request and can move the next request of a connection to another backend. A [layer 4](/layer-4-load-balancing/) balancer sees only connections: draining stops new connections, but a long-lived keep-alive connection keeps sending requests to the draining backend until the backend closes it. So at layer 4 the backend must close its idle connections itself.
- **Draining sessions.** With [sticky sessions](/sticky-sessions/), the balancer can keep sending requests of existing sessions to a draining backend and send it only no new sessions. The drain then lasts as long as the sessions, which is why it needs a short timeout or a session store.
- **Long-lived streams.** WebSockets and server streams do not end by themselves. The timeout cuts them, and the protocol must make the client reconnect.
- **Drain by weight.** Lower the weight of the backend step by step instead of to zero at once. This spreads the move of load over the other backends.
- **Slow start.** The reverse of draining: a new backend gets a small share of traffic first, which grows over a warm-up time.

## Pitfalls

- **Stopping before the balancers know.** The backend stops accepting at the start of the drain, but some balancer still sends to it. Keep accepting for at least the time it takes the deregistration to reach every balancer, or every client cache of [service discovery](/service-discovery/).
- **A timeout shorter than the requests.** If $\tau$ is below the length of normal requests, draining cuts them all the same, and only the deploy is slower.
- **A timeout that is too long.** A deploy waits $\tau$ for each batch. A default of 300 seconds with requests of 100 ms wastes almost all of it, unless the balancer ends the drain early when the backend is empty.
- **Health check versus drain.** A backend that starts to fail its health check on purpose to drain itself is removed only after the fall count, and it gets traffic until then. An explicit drain state is faster and exact.
- **One-step GOAWAY.** Sending one GOAWAY with the current last stream identifier refuses the streams that are in flight. The client can retry them, but a client that does not retry shows an error.

## Exercises

1. In the example, what is the smallest timeout for which no request is cut? What if request 4 were sent to backend 0?
2. Prove that with a lag $\ell$ and a backend that refuses new work from time $s + g$, the number of refused requests is the number of requests that the balancers send to $b$ in the interval $[s + g, s + \ell)$, and that it is 0 when $g \ge \ell$.
3. With a one-way delay $\delta$ and a one-step GOAWAY at time $g$, show that the refused streams are exactly those that the client sends in the open interval $(g - \delta, g + \delta)$.
4. A layer 4 balancer drains a backend whose clients use keep-alive connections with an idle timeout of 60 seconds and send a request every 10 seconds. How long does the drain take if the backend never closes a connection, and what should the backend do instead?

## References
