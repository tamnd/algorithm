---
tag: 1TFQQ5
kind: technique
slug: dns-load-balancing
name: DNS load balancing
aliases:
- DNS round robin
area: systems/load-balancing-and-hashing
level: intro
summary: "Spread clients over servers by giving one name several address records and changing their order, or by SRV records with priorities and weights; caches and clients limit the effect."
prereqs: [load-balancer, ttl-expiration]
see_also: [round-robin-load-balancing, weighted-random-load-balancing, service-discovery, failover, health-checking, layer-4-load-balancing, cache]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc1794
    title: "RFC 1794, T. Brisco, DNS Support for Load Balancing, April 1995"
    locator: Section 5, Implementation (a zone transfer program runs every 300 seconds and rotates the address records a random number of times; BIND replaced TTLs under 300 seconds with 300)
  - url: https://www.rfc-editor.org/rfc/rfc2782
    title: "RFC 2782, A. Gulbrandsen, P. Vixie and L. Esibov, A DNS RR for specifying the location of services (DNS SRV), February 2000"
    locator: the description of the Priority and Weight fields (the weighted selection with running sums and a uniform number from 0 to the sum, inclusive; weight 0 records first)
  - url: https://www.rfc-editor.org/rfc/rfc6724
    title: "RFC 6724, D. Thaler, R. Draves, A. Matsumoto and T. Chown, Default Address Selection for Internet Protocol Version 6 (IPv6), September 2012"
    locator: Section 6, Rule 9 (longest matching prefix, may be superseded), and Appendix B (the change to CommonPrefixLen lets DNS load balancing continue as a tie breaker)
  - url: https://www.rfc-editor.org/rfc/rfc1035
    title: "RFC 1035, P. Mockapetris, Domain Names, Implementation and Specification, November 1987"
    locator: Section 3.2.1 (the TTL field of a resource record, the time it may be cached)
---

*DNS load balancing* spreads clients over several servers through the name system. The name of the service has several address records, one per server, and the authoritative DNS server changes their order from one answer to the next, so that different clients try different servers first. This is *DNS round robin*. A second form uses SRV records, which carry a priority and a weight for each server, and the client picks among them at random in proportion to the weights. The technique needs no box in the data path and works across the internet, but the DNS server does not see the clients' requests: resolvers cache an answer for its TTL, many clients share one resolver, and the client library can reorder the addresses. So the result is coarse, and it is often used in front of [layer 4](/layer-4-load-balancing/) balancers rather than in place of them.

## In plain words

A town has three post offices, and the phone book lists all three under one name. Each time someone asks the operator, the operator reads the list starting one place further down, so the first office named changes. Most people go to the first one they hear, so visitors spread over the three.

But some people ask once for their whole street and pass the answer on to everyone there. If one street is big, its office gets crowded. And if an office closes, people who already wrote down its address still go there until they ask again.

## When it applies

- The servers have their own public addresses, or each address is itself a balancer, and an even spread over time is enough.
- A coarse split is acceptable: the unit of balance is a resolver's cached answer, which can hold many clients for a whole TTL.
- Failover may take a TTL or longer, since clients and resolvers keep old answers; clients that try the next address when one fails make this shorter.
- For SRV records: the client protocol looks them up, as for SIP, XMPP, LDAP and many service discovery systems.
- Clients are far apart and need a server near them: an answer that depends on the location of the resolver or the client is the same mechanism with a different choice rule.

## The template

The authoritative server answers with a rotated list; a client that uses SRV records orders them as in RFC 2782.

```pseudo id=main
ANSWER()                                        ▷ authoritative server; R = the address records, q = queries so far
L1  out ← R rotated left by q mod |R|; q ← q + 1
L2  return out with the TTL of R

SRV-ORDER(records)                               ▷ client; each record has a priority and a weight
L3  for each priority p, smallest first do
L4      C ← the records of priority p, those with weight 0 first
L5      while C is not empty do
L6          S ← the sum of the weights in C; r ← a uniform integer in [0, S]
L7          i ← the first record of C whose running sum of weights is ≥ r
L8          append i to the order; remove i from C
L9  return the order
```

**What the rotation guarantees.** In any $n$ consecutive answers for $n$ records, each address is first exactly once. This is a statement about answers, not about requests: it says nothing about how many clients use each answer. With the arrival model of real clients, many clients behind each resolver and a cache per resolver, DNS round robin is a heuristic with no bound on the load of a server.

**What SRV selection guarantees.** Within one priority, with weights $w_1, \dots, w_k$ in the order of line L4 and $S = \sum w_i$, line L7 picks record $i$ for the values of $r$ in $(s_{i-1}, s_i]$, where $s_i$ is the running sum, and the first record also for $r = 0$. So the first record is drawn with probability $(w_1 + 1)/(S + 1)$ and each other record with probability $w_i/(S + 1)$. A record of weight 0 is drawn first only when $r = 0$, with probability $1/(S + 1)$, which is the small chance that RFC 2782 asks for. A record of a higher priority value is used only when all records of lower values have been tried.

**TTL.** Each answer carries a TTL, the number of seconds a resolver may keep it. A short TTL lets a change of the records reach clients sooner, at the cost of more queries.

## Classic examples

**Rotation.** Three records A, B and C. The first four answers are (A, B, C), (B, C, A), (C, A, B) and (A, B, C).

**SRV weights.** Four records of priority 10 with weights 0, 60, 30 and 10, in that order after line L4, so $S = 100$ and $r$ takes 101 values. The weight-0 record is drawn first with probability $1/101$, and the others with $60/101$, $30/101$ and $10/101$. Without the weight-0 record the first one, of weight 60, also takes $r = 0$ and is drawn with probability $61/101$. A fifth record of priority 20 is never drawn first while any record of priority 10 exists.

**Skew from resolvers.** Two servers S1 and S2, a TTL of 60 s, and two resolvers: one serves 900 clients, the other 100, and each client sends one request per second to the first address of its resolver's answer. Each minute the big resolver asks first and gets (S1, S2), and the small one asks next and gets (S2, S1). Over 10 minutes S1 gets 540,000 requests and S2 gets 60,000, a 90 to 10 split, and the rotation never corrects it because the queries keep the same order. The same 1000 clients behind 10 resolvers of 100 clients each give exactly 300,000 requests to each server.

**Failure.** With the same TTL and two resolvers of 100 clients each, S1 fails 30 s after both resolvers fetched their answers. The resolver whose answer starts with S1 keeps it for 30 s more, so 3000 requests fail unless the clients try the second address.

**The first published setup.** RFC 1794 does not rotate per query. It describes a modified BIND in which a program transfers a special zone every 300 seconds and rotates its address records a random number of times, so the order changes every five minutes. The RFC also notes that BIND then replaced any TTL under 300 seconds with 300 and treated a zone refresh under 15 minutes as wrong as well, and that the modified code sets these values to 60 seconds.

## Variations

- **Random order.** The server shuffles the records for each answer instead of rotating them. BIND can do cyclic or random order with its `rrset-order` option.
- **Weighted answers.** Some DNS services return a record with a probability set per record, which is [weighted random load balancing](/weighted-random-load-balancing/) at the level of resolvers.
- **Health-checked answers.** The DNS server removes the address of a server that fails its [health checks](/health-checking/), so new answers skip it. Old answers stay in caches for the TTL.
- **Geographic or latency-based answers.** The answer depends on the location of the resolver, or of the client when the resolver sends part of the client's address (the EDNS client subnet option). This is the usual first step of a content delivery network.
- **SRV and service discovery.** [Service discovery](/service-discovery/) systems often publish the healthy instances of a service as DNS records with short TTLs.
- **One answer, many machines.** A single address announced from many places by BGP (anycast), or a [layer 4 balancer](/layer-4-load-balancing/) behind one address, does the fine balancing; DNS then only picks a region.

## Pitfalls

- **Caching hides the rotation.** One resolver serves many clients with one answer for a whole TTL, so the load follows the size of the resolver populations, not the number of records.
- **Old answers after a change.** Some resolvers and clients keep answers longer than the TTL, or cache them in the application, so a removed server still gets traffic.
- **Client reordering.** The client library can sort the addresses. RFC 3484 sorted by longest matching prefix in its rule 9, which could override the DNS order; RFC 6724 changed the prefix comparison so that the DNS order survives as a tie breaker, and lets rules 9 and 10 be superseded.
- **Clients that use only the first address.** If a client does not try the next address when one fails, one dead server breaks a share of the clients for up to a TTL.
- **No view of load.** The DNS server does not see requests, connections or response times, so it cannot follow the load the way [least connections](/least-connections/) does.
- **A low TTL is not free.** It raises the query rate to the authoritative servers and adds lookup latency for clients.

## Exercises

1. Show that in any $n$ consecutive answers of ANSWER, each of the $n$ records is first exactly once. Does this hold if two resolvers ask at the same time?
2. Three SRV records of one priority have weights 0, 0 and 10. What is the chance that each is drawn first?
3. Change the order of the resolvers' queries in the skew example so that the split becomes even over time.
4. With a TTL of 300 s and clients that do not retry, what fraction of requests fails in the first five minutes after one of four servers fails, if the answers were fetched at uniform random times?
5. Why does a service with a few very large resolvers in front of most of its clients get little benefit from DNS round robin?

## References
