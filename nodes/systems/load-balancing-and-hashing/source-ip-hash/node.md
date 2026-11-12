---
tag: 39Q693
kind: algorithm
slug: source-ip-hash
name: Source IP hash
aliases:
- IP hash
- client IP hashing
area: systems/load-balancing-and-hashing
level: intro
summary: A load balancer hashes the client's IP address and takes it modulo the total server weight, so each client keeps reaching the same server while the server list stays the same.
solves: [load-balancing-problem]
model: word-ram
complexity:
  vars: {n: the number of servers}
  time: {worst: O(n)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [hash-function, load-balancer]
see_also: [sticky-sessions, consistent-hashing, rendezvous-hashing, ecmp-hashing, layer-4-load-balancing, round-robin-load-balancing, load-skew, monotonicity-property]
sources:
  - url: https://nginx.org/en/docs/http/ngx_http_upstream_module.html#ip_hash
    title: nginx documentation, Module ngx_http_upstream_module, directive ip_hash
    locator: "the key is the first three octets of an IPv4 address or the whole IPv6 address; a server that must be removed for a while should be marked down to keep the hashing of the other clients"
  - url: https://github.com/nginx/nginx/blob/master/src/http/modules/ngx_http_upstream_ip_hash_module.c
    title: nginx source code, src/http/modules/ngx_http_upstream_ip_hash_module.c
    locator: "ngx_http_upstream_init_ip_hash_peer (address length 3 or 16, start value 89) and ngx_http_upstream_get_ip_hash_peer (hash = (hash * 113 + byte) % 6271, the weighted pick, the skip of down peers, the fallback to round robin after 20 tries)"
  - url: https://docs.haproxy.org/3.2/configuration.html
    title: HAProxy Configuration Manual, version 3.2
    locator: the balance keyword, algorithm source (the source address is hashed and divided by the total weight of the running servers; many clients move when the number of running servers changes; hash-type consistent changes this)
  - paper: doi:10.1145/258533.258660
    title: David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine and Daniel Lewin, Consistent hashing and random trees, Proceedings of the 29th ACM Symposium on Theory of Computing (STOC), 1997
    locator: the motivation that a hash modulo the number of caches remaps almost every item when a cache is added
---

Source IP hash is a [load balancer](/load-balancer/) rule that picks a server from a [hash](/hash-function/) of the client's IP address, usually modulo the total weight of the servers. A client then reaches the same server on every request, with no cookie and no table, as long as the server list does not change. This gives a weak form of [sticky sessions](/sticky-sessions/) that works for any protocol. The cost is that the spread of load follows the spread of client addresses, and a change of the server count moves most clients, unless the hash is replaced by [consistent hashing](/consistent-hashing/).

## In plain words

Each client comes from an address. The balancer turns the address into a number and uses the number to pick a server, so the same address always gets the same server. A server that keeps some state for a client, such as a login or a cache of its data, sees all of that client's requests.

Two things can go wrong. If many people share one address, as in an office behind one router, they all land on one server. And if the number of servers changes, the picks change for most addresses, so most clients lose the server that knew them. A server that is only marked as unavailable, but kept in the list, does better: only its own clients move.

## The problem

There are $n$ servers $S_1, \ldots, S_n$ with positive integer weights $w_1, \ldots, w_n$, $W = \sum_i w_i$, and a set $D$ of servers that are down. Requests arrive in any order, adversarial or not, and each carries a client address. The rule must:

- send all requests of one address to one server while the server list is fixed (affinity);
- give server $S_i$ about the share $w_i / W$ of the client addresses;
- keep no state per client.

This is the keyed form of the [load balancing problem](/load-balancing-problem/), with the client address as the key. The guarantees below count addresses, not requests or bytes; they hold if the hash of the addresses in use is close to uniform.

## The algorithm

The pseudocode is the form of the nginx `ip_hash` module. Other balancers use another hash, but the same steps.

```pseudo id=main
IP-HASH(ip, S, w, D)       ▷ S[1..n] servers, w weights, W = Σ w, D servers down
L1  a ← the first 3 bytes of ip if it is IPv4, else all 16 bytes
L2  h ← 89, tries ← 0
L3  loop
L4      for each byte b of a do h ← (113 · h + b) mod 6271
L5      r ← h mod W
L6      i ← 1
L7      while r ≥ w[i] do r ← r − w[i], i ← i + 1
L8      if S[i] ∉ D then return S[i]
L9      tries ← tries + 1
L10     if tries > 20 then return FALLBACK()      ▷ nginx falls back to round robin
```

Lines L5 to L7 give server $S_i$ a block of $w_i$ residues modulo $W$. If the chosen server is down, line L4 hashes the same key again, starting from the current $h$, so each address has its own fixed sequence of probes.

The plainest form, as in HAProxy's `balance source`, is $S[\text{hash}(ip) \bmod W']$ over the servers that are running, where $W'$ is their total weight. It has no probe sequence: a server that goes down changes $W'$ and so moves most clients.

## Example

Three servers A, B and C of weight 1. The client 192.168.1.10 has the key bytes 192, 168 and 1.

| byte | $h$ before | $113 h + b$ | $h$ after (mod 6271) |
|---|---|---|---|
| 192 | 89 | 10,249 | 3,978 |
| 168 | 3,978 | 449,682 | 4,441 |
| 1 | 4,441 | 501,834 | 154 |

Then $154 \bmod 3 = 1$, so line L7 stops at the second server, B. If B is down, the next pass of line L4 gives $h = 5654$, and $5654 \bmod 3 = 2$ picks C.

| client | first $h$ | server | server with B down |
|---|---|---|---|
| 192.168.1.10 | 154 | B | C |
| 192.168.1.77 | 154 | B | C |
| 192.168.2.10 | 155 | C | C |
| 10.0.0.5 | 2,565 | A | A |
| 203.0.113.9 | 2,592 | A | A |
| 2001:db8::1 | 2,600 | C | C |

The first two clients share a /24 prefix, so they share a server. The others keep their servers when B goes down.

**Many clients.** Take 100,000 random IPv4 addresses (seed 5) and five servers s0 to s4 of weight 1. The servers get between 19,803 and 20,182 clients.

- Mark s2 down: exactly its 19,976 clients move, and they spread over the other four, which then have between 24,798 and 25,086.
- Remove s2 from the list: 80,190 clients move, close to the $4/5$ of Theorem 4.
- Add a sixth server s5 at the end: 83,333 clients move, while only 16,803 of them go to s5.
- Add one NAT address that sends 25,000 requests. Its server s0 now has 44,803 of the 125,000 requests, 1.79 times the mean.

## Correctness

The loop returns the first server of the address's probe sequence that is up, and gives up after 21 probes. The sequence depends only on the key bytes, so the choice is a function of the address prefix, the server list and the set of servers that are down. If more servers are marked down, a client whose server is still up keeps it, because the earlier probes were already down; so marking one server down moves exactly its clients, and they come back when it returns. Removing a server from the list instead changes the modulus, and a client keeps its server with probability about $1/n$. With uniform hash values, server $S_i$ gets a share within $w_i/6271$ of $w_i / W$. The proofs are below.

## Complexity

- **Time.** Each probe hashes 3 or 16 bytes and scans at most $n$ weights, so $O(n)$ per probe and at most 21 probes: $O(n)$ in the worst case. With a prefix sum of the weights and a binary search, the scan is $O(\log n)$.
- **Space.** $\Theta(1)$ extra space, and no state per client.
- **Balance.** In the model where each address hashes to a uniform value, the number of addresses on a server is binomial, as in [balls into bins](/balls-into-bins/). In practice the request load per address is far from equal, and that dominates.

## Properties

- **Stateless affinity.** No cookie, no table: the balancer, or several balancers with the same list, compute the same server.
- **Protocol independent.** It needs only the source address, so it works at layer 4 for any TCP or UDP service, and for TLS without decryption.
- **Not monotone.** A change of the server list moves most clients, not only those of the changed server. See the [monotonicity property](/monotonicity-property/).
- **Coarse keys.** In nginx, every client of a /24 IPv4 prefix is one key.

## Variants and improvements

- **Consistent source hashing.** Use the address as the key of a [hash ring](/hash-ring/), [rendezvous hashing](/rendezvous-hashing/) or [Maglev hashing](/maglev-hashing/). A change of one server then moves about $1/n$ of the clients. HAProxy does this with `hash-type consistent`.
- **Generic hash keys.** nginx's `hash` directive takes any key, such as `$remote_addr` for the whole address or a header, with an optional `consistent` flag.
- **Flow hashing.** Routers and layer 4 balancers hash the whole flow, both addresses and ports; see [ECMP hashing](/ecmp-hashing/). That spreads one client's connections, so it gives no client affinity.
- **Cookies.** A cookie that names the server gives exact [sticky sessions](/sticky-sessions/) for HTTP, also for clients that change address.

## When to use it

Use source IP hash when a server keeps per-client state that is costly to lose, the protocol has no cookie or the balancer cannot read it, and the client addresses are many and stable. Typical cases are TCP services at layer 4 and simple web farms with local session storage. Do not use it when many clients come through a few proxies or NAT addresses, or when the server set changes often; then use cookies, a shared session store, or a consistent hash.

## Pitfalls

- **NAT and proxies.** One address can stand for thousands of users. In the run above, one busy address puts 1.79 times the mean load on its server. See [load skew](/load-skew/).
- **The /24 key.** nginx hashes only three bytes of an IPv4 address, so a whole office or campus subnet is one key.
- **Removing a server from the list.** This moves most clients and breaks their sessions. Mark the server down instead, as the nginx documentation advises, or use a consistent hash.
- **Changing addresses.** Mobile clients and IPv6 privacy addresses change their source address, and then their server.
- **The address of a proxy.** Behind another proxy or a CDN, the source address is the proxy's address. Hashing it sends everything to one server. Use the forwarded client address only if the proxy in front is trusted to set it.
- **A small hash range.** The nginx hash has only 6,271 values, so a total weight above 6,271 leaves some weight units with no hash value.

## Implementations

## History

Hashing the source address to pick a server is an old practice in proxies, routers and layer 4 switches, and its first use is hard to date. The weakness of the plain modulo rule, that adding a server remaps almost every key, is the motivation of the consistent hashing paper of Karger et al. (1997). nginx's `ip_hash` and HAProxy's `balance source` are widely used forms of the rule today.

## References
