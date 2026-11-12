---
tag: XW2KX8
kind: concept
slug: service-discovery
name: Service discovery
aliases:
- dynamic service registry
- service registry
- client-side discovery
- server-side discovery
area: systems/load-balancing-and-hashing
level: intro
summary: "How clients and balancers find the live instances of a service by name: instances register and renew a lease, and clients read the registry directly, through a router, or by DNS SRV."
prereqs: [load-balancer, health-checking]
see_also: [dns-load-balancing, swim, membership-management, failure-detection, leader-lease, connection-draining, failover, zab]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc2782
    title: "A. Gulbrandsen, P. Vixie and L. Esibov, RFC 2782, A DNS RR for specifying the location of services (DNS SRV), 2000"
    locator: "the format of the SRV RR (the owner name _Service._Proto.Name, and the fields Priority, Weight, Port and Target), the meaning of the target \".\", and the weighted selection algorithm with running sums"
  - paper: "Patrick Hunt, Mahadev Konar, Flavio P. Junqueira and Benjamin Reed, ZooKeeper: wait-free coordination for Internet-scale systems, USENIX Annual Technical Conference (USENIX ATC), 2010"
    locator: "Section 2.1 (regular and ephemeral znodes, sessions and the session timeout) and Section 2.4 (the group membership primitive with ephemeral child znodes and watches)"
  - paper: doi:10.1145/74850.74870
    title: Cary G. Gray and David R. Cheriton, Leases, an efficient fault-tolerant mechanism for distributed file cache consistency, Proceedings of the 12th ACM Symposium on Operating Systems Principles (SOSP), 1989
    locator: the definition of a lease as a grant for a fixed term, after which the grantor may act without hearing from the holder
  - url: https://etcd.io/docs/v3.5/learning/api/
    title: etcd documentation, version 3.5, etcd3 API
    locator: "the section Lease API (LeaseGrant with a TTL, LeaseKeepAlive, and the deletion of all keys attached to a lease when it expires or is revoked)"
  - url: https://github.com/Netflix/eureka/wiki/Understanding-eureka-client-server-communication
    title: Netflix Eureka wiki, Understanding Eureka client-server communication
    locator: "the sections on Renew (a heartbeat every 30 seconds, and removal after 90 seconds without one) and Fetch Registry (the client refreshes its cached copy every 30 seconds)"
  - url: https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/
    title: Kubernetes documentation, DNS for Services and Pods
    locator: "the section Services (A and AAAA records for normal and headless Services, and SRV records for named ports)"
  - url: https://microservices.io/patterns/client-side-discovery.html
    title: Chris Richardson, Microservices.io, Pattern, Client-side service discovery
    locator: the pattern, its benefits and drawbacks, and the related pattern Server-side service discovery
  - url: https://developer.hashicorp.com/consul/docs/services/usage/checks
    title: HashiCorp Consul documentation, Define health checks
    locator: "the TTL check, which an outside process must update through the pass, warn, fail or update endpoints, and which becomes critical when its ttl runs out"
---

Service discovery is the way a client or a [load balancer](/load-balancer/) finds the current network addresses of the live instances of a service from the name of the service. Instances record themselves in a *service registry* and keep their entry alive with heartbeats or a lease that has a time to live; the entry goes away when the instance deregisters or stops renewing. Clients then read the registry themselves (*client-side discovery*) or send their requests to a router that reads it for them (*server-side discovery*). DNS is the oldest registry: an SRV record, defined in RFC 2782, maps a service name to hosts, ports, priorities and weights. Every registry can be stale in two directions, listing a dead instance or missing a live one, and its timers set how long each error lasts.

## In plain words

In a large office, teams move between rooms all the time. A visitor knows only the name of the team, not the room. So there is a board at the entrance. Each team writes its room on the board, and a team must come back every ten minutes to tick its line, or the line is wiped.

A visitor can read the board and walk to a room. Or the visitor can ask the receptionist, who reads the board and walks the visitor there. The first way is quicker, but every visitor must learn to read the board. The second way is simpler for visitors, but the receptionist is one more step.

The board is never quite right. A team that has gone home can stay on the board until its tick runs out. A visitor who read the board an hour ago may still go to an old room.

## The idea

### The model

A service has a set of instances, each with an address and a port. A *registry* stores, for each service name, the entries of its instances. It is usually a small replicated store, built on [Raft](/raft/) as in etcd or on [Zab](/zab/) as in ZooKeeper, so that it survives the loss of a minority of its own nodes. An instance renews its entry every $R$ ticks; each renewal reaches the registry within $\delta$ ticks or is lost; the registry deletes an entry $L$ ticks after the last renewal it received, unless the instance deregisters first. A client keeps a copy of the list for service name lookups and refreshes it every $C$ ticks, or, with DNS, keeps an answer for its TTL of $C$ seconds. These are the [lease](/leader-lease/) parameters of Gray and Cheriton: the registry may act on its own once the term $L$ has passed.

### Client-side and server-side discovery

In *client-side discovery*, the client reads the registry, keeps the list, and picks an instance with its own balancing policy. Netflix used this with the Eureka registry and the Ribbon client library. There is no extra network hop, and each client can use a smart policy, but every language needs its own discovery library, and every client depends on the registry's API.

In *server-side discovery*, the client sends each request to one fixed address, and a router or balancer at that address reads the registry and forwards the request. A Kubernetes Service with a cluster IP works this way: its DNS name resolves to the cluster IP, and the nodes forward traffic for that IP to the pods of the Service. The client stays simple, at the price of one more hop and one more component that must be highly available.

DNS sits between the two. The client asks by name, but it gets the addresses and picks one itself. For a headless Kubernetes Service, the DNS name resolves to the addresses of all the selected pods, and the client is expected to use the set or to pick from it round robin. This is [DNS load balancing](/dns-load-balancing/) with a registry behind it.

### Registration and liveness

An instance can register itself (*self-registration*), or an outside component can register it (*third-party registration*), such as an orchestrator that starts the instance and knows its address. The registry learns that an instance is gone in one of four ways:

- **Deregistration.** A clean shutdown removes the entry first and then [drains](/connection-draining/) the requests in flight. This is the only fast way, and it does not help after a crash.
- **Heartbeats with a TTL.** The instance renews its entry, and the registry deletes the entry when the TTL runs out. In Eureka, a client renews every 30 seconds and the server removes it after 90 seconds without a renewal. In etcd, an instance attaches its key to a lease granted with a TTL and keeps it alive with LeaseKeepAlive; when the lease expires, every key attached to it is deleted. A Consul TTL check goes critical when no update comes within its ttl.
- **Sessions.** In ZooKeeper, an instance creates an *ephemeral* znode under the node of its group. ZooKeeper deletes the znode when the session that created it ends, and it ends the session when it hears nothing from the client for the session timeout. Clients list the children of the group node and set a watch to learn of changes.
- **Health checks by the registry.** The registry, or an agent next to each instance, probes the instance, as in [health checking](/health-checking/), and hides entries that fail. Consul agents also find failed nodes with a gossip protocol based on [SWIM](/swim/).

The first three ways need nothing from outside the instance's own process, so they cannot tell a live process that is stuck from a healthy one. This is why registries often combine a lease with a real health check.

### How stale the list can be

**Claim 1 (no false expiry).** If each renewal reaches the registry within $\delta$ ticks and $R + \delta < L$, the registry never deletes a live instance. More generally, the entry survives $k$ lost renewals in a row whenever $(k + 1)R + \delta < L$.

*Proof.* Let renewal $i$ be sent at $t_0 + iR$ and received at $r_i$, with $t_0 + iR \le r_i \le t_0 + iR + \delta$. If renewals $i + 1, \ldots, i + k$ are lost, the next one is received at $r_{i+k+1} \le t_0 + (i + k + 1)R + \delta \le r_i + (k + 1)R + \delta < r_i + L$. So it arrives before the entry expires at $r_i + L$. With $k = 0$ this is the first statement. $\square$

**Claim 2 (bounded traffic to a dead instance).** If an instance crashes at time $c$ and does not deregister, the registry deletes its entry by $c + \delta + L$, and no client whose copy is refreshed every $C$ ticks sends to it after $c + \delta + L + C$, plus the delay of the refresh itself.

*Proof.* The last renewal was sent at or before $c$, so it was received at some $r \le c + \delta$, and no renewal is received after it. The registry deletes the entry at $r + L \le c + \delta + L$. A client copy that was fetched before the deletion is replaced by a fresh copy within $C$ ticks of its fetch, so the dead entry is gone from every copy by $c + \delta + L + C$ plus the delay of a fetch. $\square$

The two claims pull against each other. A short lease $L$ shortens the window of Claim 2 but needs $L > R + \delta$ for Claim 1, so a short lease needs frequent renewals, and $n$ instances that renew every $R$ seconds send $n/R$ renewals per second to the registry. This is the trade-off of the [failure detection](/failure-detection/) problem between detection time, false suspicions and message cost. Since the window of Claim 2 is never zero, clients must still retry on another instance when a request fails.

A registry lease differs from a [leader lease](/leader-lease/) in what it promises. A leader lease promises that no one else holds the role, so a clock error breaks safety. A registry lease only claims that the instance is probably alive, so an error costs only a few failed requests.

### DNS SRV records

An SRV record has the owner name `_Service._Proto.Name`, for example `_ldap._tcp.example.com`, and four fields: Priority, Weight, Port and Target. A client must try the targets with the lowest priority it can reach first. Within one priority, it orders the targets by weight with this algorithm, repeated until no record is left: put the records of weight 0 first and the others in any order, compute the running sums of the weights, choose a random number uniformly from 0 to the total $S$ inclusive, and take the first record whose running sum is at least that number. A single record with the target `.` says that the service is not available at this name. Kubernetes publishes SRV records for the named ports of a Service, under `_port-name._port-protocol.my-svc.my-namespace.svc.cluster-domain.example`.

### Pitfalls

- **Caches longer than the TTL.** Some resolvers, libraries and runtimes keep DNS answers longer than the TTL, or for the life of a connection pool, so the $C$ of Claim 2 is longer than the TTL says.
- **A registry that is down.** If clients cannot reach the registry, they should keep using their last copy rather than drop to an empty list. An empty list turns a registry outage into a full outage.
- **Registering before ready.** An instance that registers before it can serve gets traffic it fails. Register after warm-up, or let a readiness check gate the entry.
- **Exiting before deregistration has spread.** Deregister, wait for at least $C$ so that every client copy has dropped the entry, and only then stop accepting new work.
- **Liveness is not health.** A lease shows that the process can still send a renewal, not that it can serve. Combine it with a health check that tests the service path.
- **Herds at startup.** If all clients refresh at the same moment, or all instances renew in step after a restart, the registry gets bursts. Add random jitter to $R$ and $C$.

## Examples

**A lease timeline.** Take $R = 10$, $L = 30$, $\delta \le 2$ and a client refresh every $C = 15$ seconds, at 10, 25, 40, 55, 70 and so on. Since $R + \delta = 12 < 30$, Claim 1 says that a live instance is never deleted, and it survives one lost renewal since $2R + \delta = 22 < 30$. Renewals sent at 0, 10, 20, 30 and 40 arrive at 1, 12, 21, 32 and 41. The instance crashes at 47. The registry deletes it at $41 + 30 = 71$. The client's copy of time 70 still lists it, so the client can send to the dead instance until its next refresh at 85, which is 38 seconds after the crash. The bound of Claim 2 is $\delta + L + C = 47$ seconds plus the fetch delay.

**Eureka.** With renewals every 30 seconds, removal after 90 seconds without one, and a client refresh every 30 seconds, the model gives up to $90 + 30 = 120$ seconds, plus network delays, in which a client may still send to a crashed instance. By Claim 1, one lost heartbeat never removes a live instance when each heartbeat arrives within 30 seconds, since $2 \cdot 30 + \delta < 90$; two lost in a row can remove it.

**SRV selection.** Records at priority 10 with weights 60, 30 and 10, listed in that order, have running sums 60, 90 and 100. The random number is one of the 101 integers 0 to 100, so the first pick is the weight-60 record with probability $61/101$, the weight-30 record with $30/101$ and the weight-10 record with $10/101$. The record listed first gets the extra value 0. If a record of weight 0 is added, it goes first with running sum 0, and it is the first pick only when the number is 0, with probability $1/101$: this is the "very small chance" that the RFC asks for. A record at priority 20 is used only when no target at priority 10 can be reached.

**ZooKeeper group membership.** A group is a znode $z_g$. Each instance creates an ephemeral child of $z_g$, named by its identifier or with the sequential flag, and stores its address and port in the child's data. A client lists the children of $z_g$ with a watch, and gets a notification when one is added or removed. When an instance fails, its session times out, its child disappears, and the watch fires.

**Non-example.** A fixed list of addresses in a configuration file is not service discovery: it does not change when instances come and go, so a failed instance stays in it until a person edits it. A [gossip membership](/membership-management/) protocol is close but different: it gives each member of a group a view of the other members, while discovery serves clients that are outside the group.

## Where it is used

- **Microservices.** Each service finds its dependencies by name through a registry such as Consul, etcd, ZooKeeper or Eureka, or through the Services of an orchestrator such as Kubernetes.
- **Load balancers.** A balancer takes its pool from the registry, adds its own [health checking](/health-checking/), and routes around the gaps. Discovery tells it who exists; health checking tells it who works.
- **Internet protocols.** SRV records let a client find the server for a protocol in a domain, such as LDAP over TCP in the RFC's own example, with priorities for backup servers and weights for capacity.
- **Failover.** After a [failover](/failover/), the registry is how clients learn the address of the new primary, and its staleness adds to the time to fail over.

## References
