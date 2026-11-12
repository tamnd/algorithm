---
tag: BGFEMR
kind: concept
slug: layer-7-load-balancing
name: Layer 7 load balancing
aliases:
- application-layer load balancing
area: systems/load-balancing-and-hashing
level: intro
summary: "Balancing by request: the balancer ends the client's connection, parses each HTTP or gRPC request, routes it by host, path or header and picks a backend for each request."
prereqs: [load-balancer, layer-4-load-balancing]
see_also: [sticky-sessions, least-response-time, peak-ewma, least-connections, power-of-two-choices, health-checking, load-shedding, connection-draining]
sources:
  - url: https://grpc.io/blog/grpc-load-balancing/
    title: gRPC blog, gRPC Load Balancing, June 15, 2017
    locator: the sections on proxy load balancing at L3/L4 and at L7 (an L7 balancer ends and parses HTTP/2 and can spread the streams of one client over several backends)
  - url: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/load_balancing/load_balancers
    title: Envoy documentation, Supported load balancers
    locator: the list of balancer types and the section Weighted least request (two choices by active requests; weight / (active_requests + 1)^bias with bias 1.0 when weights differ)
  - url: https://nginx.org/en/docs/http/ngx_http_upstream_module.html
    title: nginx documentation, Module ngx_http_upstream_module
    locator: the directives upstream, server, least_conn, hash, ip_hash, random and least_time
  - book: isbn:9781491929124
    title: Betsy Beyer, Chris Jones, Jennifer Petoff and Niall Richard Murphy (editors), Site Reliability Engineering, O'Reilly, 2016
    locator: Chapter 20, Load Balancing in the Datacenter (request-level policies, subsetting, the sinkholing of errors), chapter level only
---

A layer 7 [load balancer](/load-balancer/) works at the application layer, layer 7 of the OSI model. It ends the client's TCP connection, and usually its TLS session, reads each request of the application protocol, most often HTTP or gRPC, and then makes two choices for each request: which pool of backends serves it, from the host name, the path, a header or a cookie, and which backend in that pool, by a balancing policy. It sends the request over its own connection to that backend and sends the response back. So it balances requests, not connections, and it can measure each response. The price is the work of parsing and of TLS, a second connection, and a balancer that sees the content. Balancing by flow without reading the content is [layer 4 load balancing](/layer-4-load-balancing/).

## In plain words

A layer 7 balancer is like a mail room that opens each letter. It reads what the letter asks for, sends questions about bills to the billing team and questions about orders to the order team, and inside each team gives the letter to the person with the least work. The answer comes back through the mail room.

Because it opens every letter, it can split one customer's many letters over many people, retry a letter that got no answer, and note who answers slowly. Opening letters takes time, and the mail room must be trusted with what is inside.

## The idea

**Two connections.** The client connects to the balancer, and the balancer keeps its own connections to the backends, often a pool of open connections that it reuses. Requests from many clients share these backend connections. The client never talks to a backend directly.

**Routing.** A list of rules maps each request to a pool, by host name, path prefix, method, header or cookie. Systems differ in how they pick among rules: Envoy takes the first route that matches, in order, and nginx takes the longest matching prefix location unless a regular expression matches. A rule with a plain string prefix /api also matches /apiary; rules that should match whole path segments must say so.

**Balancing.** Inside the pool, the balancer picks a backend for each request, so it can use policies that need per-request data: requests in flight, as in [least connections](/least-connections/) counted by request, response time, as in [least response time](/least-response-time/) and [peak EWMA](/peak-ewma/), or a sampled choice as in [power of two choices](/power-of-two-choices/). Envoy's least request balancer, for example, compares the active requests of two random backends when all weights are equal.

**What else it can do.** Because it sees requests and responses, it can retry a failed idempotent request on another backend, keep a client on one backend with a cookie ([sticky sessions](/sticky-sessions/)), drop or delay requests under overload ([load shedding](/load-shedding/)), mark a backend bad from its status codes as well as from [health checks](/health-checking/), and move the next request of a connection away from a backend that is [draining](/connection-draining/).

**What is guaranteed.** Requests arrive online in any order. The routing rules are deterministic: the same request goes to the same pool. The balance of load depends on the policy and its model; a request-level policy cannot overload a backend through one long connection, which a connection-level policy can. Most request-level policies on these pages are heuristics, and the policy pages say which ones have a proved bound.

## Examples

**Routing rules.** The rules are, in order: path prefix /api/v2 to pool v2, path prefix /api to pool v1, host static.example.com to pool static, and all else to pool web. With first match:

| request | pool |
|---|---|
| GET www.example.com/api/v2/users | v2 |
| GET www.example.com/api/users | v1 |
| GET www.example.com/apiary | v1 (a plain string prefix matches) |
| GET static.example.com/logo.png | static |
| GET www.example.com/ | web |

If the rule for /api came first, /api/v2/users would go to v1: with first match, the more specific rule must come first.

**Splitting a long connection.** Three clients each open one HTTP/2 connection and send 100, 10 and 10 requests per second. A [layer 4](/layer-4-load-balancing/) balancer gives each of three backends one connection, so the backends see 100, 10 and 10 requests per second. A layer 7 balancer with per-request round robin sends the 120 requests per second as 40, 40 and 40, because it picks a backend for each HTTP/2 stream.

**A retry.** A request to backend A times out after 1 s. The balancer sends it again to backend B, which answers in 20 ms; the client sees about 1.02 s instead of an error. This is safe only for requests that can run twice, such as a GET, and retries must be limited, or a slow pool gets twice the load when it can least take it.

## Where it is used

- **Reverse proxies.** nginx, HAProxy in `mode http`, Envoy and Traefik, in front of web and API servers. They often also end TLS, compress and cache.
- **Service meshes and RPC clients.** A sidecar proxy such as Envoy, or the Linkerd proxy with its [peak EWMA](/peak-ewma/) balancer, balances each RPC. gRPC clients can also balance by request themselves, without a proxy.
- **Cloud application balancers.** Managed HTTP balancers route by host and path to groups of backends. They usually run behind a [layer 4](/layer-4-load-balancing/) tier that spreads the client connections over the layer 7 machines.
- **Large services.** Google's SRE book describes request-level balancing in the data center with least-loaded choices among a subset of backends per client.

## References
