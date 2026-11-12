---
tag: EZ722J
kind: concept
slug: load-balancer
name: Load balancer
aliases:
- load balancing server
- request distributor
area: systems/load-balancing-and-hashing
level: intro
summary: "A component that takes requests or connections for one service address and sends each to one backend of a pool, by a policy, while it keeps track of which backends are up."
prereqs: [load-balancing-problem]
see_also: [layer-4-load-balancing, layer-7-load-balancing, dns-load-balancing, round-robin-load-balancing, least-connections, power-of-two-choices, consistent-hashing, health-checking]
sources:
  - book: isbn:9781491929124
    title: Betsy Beyer, Chris Jones, Jennifer Petoff and Niall Richard Murphy (editors), Site Reliability Engineering, O'Reilly, 2016
    locator: Chapter 19, Load Balancing at the Frontend (DNS and virtual IP addresses), and Chapter 20, Load Balancing in the Datacenter (subsetting and request-level policies), chapter level only
  - url: http://www.linuxvirtualserver.org/VS-NAT.html
    title: The Linux Virtual Server project, Virtual Server via NAT
    locator: the whole page (a balancer with a virtual service address, a scheduling algorithm and a connection hash table)
  - url: https://nginx.org/en/docs/http/ngx_http_upstream_module.html
    title: nginx documentation, Module ngx_http_upstream_module
    locator: the directives upstream and server (weight, max_fails, fail_timeout, backup, down) and the balancing methods
  - url: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/load_balancing/load_balancers
    title: Envoy documentation, Supported load balancers
    locator: the list of balancer types (weighted round robin, weighted least request, ring hash, Maglev, random)
  - paper: doi:10.1109/71.963420
    title: "Michael Mitzenmacher, The power of two choices in randomized load balancing, IEEE Transactions on Parallel and Distributed Systems 12(10), 2001"
    locator: the supermarket model and its fixed point, for the effect of sampling two queues
---

A load balancer is the part of a system that stands for a service at one address and sends each request or connection that arrives there to one of several servers, the *backends* of a pool. It has four parts: a front end that clients reach (a virtual IP address, a host name or a client library), a list of backends with their weights, a *policy* that picks the backend for each request, and a view of which backends are healthy. Its goals are to use all backends, to keep any one from overload, and to hide the failure of one. The problem it solves, assigning arriving work to servers so that the largest load stays small, is the [load balancing problem](/load-balancing-problem/); this page is about the component and its parts, and the policy pages below are about the choice rules.

## In plain words

Think of the host at a busy restaurant. Guests come in through one door, and the host sends each party to a table with a free waiter. The guests do not need to know the waiters. If a waiter goes home sick, the host stops sending guests to that waiter's tables.

A load balancer does this for computer requests. Clients send to one address. The balancer picks a server for each request, by a fixed turn, by chance, by who is least busy, or by a key that keeps a client on the same server. It also checks the servers now and then and skips the ones that do not answer.

## The idea

**Where it sits.** The same job is done at several levels, often stacked:

- **In DNS.** The name of the service resolves to several addresses ([DNS load balancing](/dns-load-balancing/)). Coarse and cached, but it needs nothing in the data path.
- **At layer 4.** A balancer picks a backend once per TCP or UDP flow from the addresses and ports ([layer 4 load balancing](/layer-4-load-balancing/)). With [direct server return](/direct-server-return/), the replies bypass it.
- **At layer 7.** A proxy ends the client's connection, reads each HTTP or RPC request, routes it by content and picks a backend per request ([layer 7 load balancing](/layer-7-load-balancing/)).
- **In the client.** A library in each client keeps the list of backends and picks one per request, with no proxy in between. Finagle and gRPC can work this way.
- **In routers.** [ECMP hashing](/ecmp-hashing/) spreads flows over equal-cost paths, often to a set of layer 4 balancer machines.

**The policy.** The policies on these pages fall into three groups.

| group | policies | state per backend | what it uses |
|---|---|---|---|
| static | [round robin](/round-robin-load-balancing/), [weighted round robin](/weighted-round-robin/), [random](/random-load-balancing/), [weighted random](/weighted-random-load-balancing/) | none or a counter | weights only |
| keyed | [source IP hash](/source-ip-hash/), [consistent hashing](/consistent-hashing/), [rendezvous hashing](/rendezvous-hashing/), [Maglev hashing](/maglev-hashing/), [bounded-load consistent hashing](/bounded-load-consistent-hashing/) | the backend list | a key of the request, so the same key reaches the same backend |
| dynamic | [least connections](/least-connections/), [weighted least connections](/weighted-least-connections/), [least response time](/least-response-time/), [power of two choices](/power-of-two-choices/), [peak EWMA](/peak-ewma/) | counts of open work, latency estimates | the current load |

Static policies are cheap and need no feedback, but they are blind to request size and server speed. Keyed policies give affinity, which caches and [sticky sessions](/sticky-sessions/) need, at the cost of balance when some keys are hot. Dynamic policies follow the load, but they need fresh data, and stale data can make many balancers herd onto the same backend.

**Guarantees.** Each guarantee holds only under its own arrival model:

- Round robin, for any sequence of requests: the request counts of any two backends differ by at most 1. Nothing is said about the work.
- Uniform random, $n$ requests on $n$ backends in the balls-into-bins model: the largest count is about $\ln n / \ln \ln n$ with high probability.
- [Two choices](/power-of-two-choices/), in the same model: about $\ln \ln n / \ln 2 + O(1)$ with high probability.
- Consistent hashing, with random hash values: a backend that joins takes about a $1/(n+1)$ share of the keys, and only those keys move.
- [Least connections](/least-connections/) as join the shortest queue: optimal for identical servers with exponential service times (Winston, 1977) and with service times of non-decreasing hazard rate (Weber, 1978), each in the sense its paper proves, but not for every service time distribution (Whitt, 1986).
- [Least response time](/least-response-time/) and [peak EWMA](/peak-ewma/): heuristics with no worst-case or queueing optimality bound.

**Operations around the policy.** A balancer also needs [health checking](/health-checking/) to find dead backends, [failover](/failover/) to a standby pool or a standby balancer, [connection draining](/connection-draining/) to take a backend out without breaking open work, [service discovery](/service-discovery/) to learn the backend list, and [load shedding](/load-shedding/) to refuse work when the whole pool is full. The balancer itself must not be a single point of failure: large systems run many balancer instances behind ECMP or DNS.

## Examples

**Blind turns against open work.** Two backends. Requests arrive at times 0, 1, 2, 3, 4 and 5, and take 10, 1, 10, 1, 10 and 1 time units. A request leaves at its end time, before a request that arrives at the same time is placed.

| request | arrives | takes | round robin | least connections |
|---|---|---|---|---|
| 1 | 0 | 10 | B0 | B0 |
| 2 | 1 | 1 | B1 | B1 |
| 3 | 2 | 10 | B0 | B1 |
| 4 | 3 | 1 | B1 | B0 |
| 5 | 4 | 10 | B0 | B0 |
| 6 | 5 | 1 | B1 | B1 |

Least connections breaks ties to B0. Round robin sends all three long requests to B0, which then has 3 open requests from time 4 to 10 while B1 has at most 1. Least connections sees at time 2 that B1 is free and gives it the second long request; neither backend ever has more than 2 open requests.

**Affinity against balance.** A cache tier of 4 backends holds user sessions. With round robin, each user's requests reach all 4 backends, so each backend must load each session. With a consistent hash on the user ID, each user reaches one backend, and when a fifth backend joins, only about 1/5 of the users move. But a single very active user now loads one backend alone; [bounded-load consistent hashing](/bounded-load-consistent-hashing/) caps each backend's share for this reason.

**Stacked balancers.** A request to a large web service resolves a name to a regional address by DNS, reaches one of many layer 4 balancer machines by ECMP, is sent by a consistent hash of its 5-tuple to a layer 7 proxy, and is routed by its path to a pool where the proxy picks a backend by least requests. Each level works at its own granularity: a resolver, a flow, a connection, a request.

## Where it is used

- **Web and API front ends.** Hardware appliances, cloud balancers, and software such as LVS (IPVS) in the Linux kernel, HAProxy, nginx and Envoy.
- **Inside data centers.** Client libraries and service mesh proxies balance each RPC; Google's SRE book describes request-level balancing with subsets of backends per client.
- **Large layer 4 tiers.** Maglev at Google, Ananta at Microsoft and Katran at Facebook, in software on ordinary servers behind ECMP.
- **Databases and caches.** Proxies spread reads over replicas, and keyed policies route each key to the shard or cache node that holds it.

A load balancer differs from a CPU scheduler's balancing of threads over cores, which moves work that is already running, and from [sharding](/sharding/), which places data, not requests, although a keyed policy often does both.

## References
