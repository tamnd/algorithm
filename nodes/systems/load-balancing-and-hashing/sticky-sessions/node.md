---
tag: GNHJ0X
kind: technique
slug: sticky-sessions
name: Sticky sessions
aliases:
- session affinity
- session persistence
area: systems/load-balancing-and-hashing
level: intro
summary: "A load balancer sends every request of one session to the same server, with a cookie that names the server or a hash of the client address. It costs balance and failover."
prereqs: [load-balancer, consistent-hashing]
see_also: [source-ip-hash, bounded-load-consistent-hashing, rendezvous-hashing, connection-draining, failover, health-checking, layer-7-load-balancing, layer-4-load-balancing]
sources:
  - url: https://docs.haproxy.org/3.2/configuration.html
    title: HAProxy Configuration Manual, version 3.2
    locator: "Section 4.2, the keywords balance (the source algorithm), hash-type (map-based against consistent), cookie (the insert, rewrite and prefix modes, nocache, maxidle and maxlife) and option redispatch"
  - url: https://nginx.org/en/docs/http/ngx_http_upstream_module.html
    title: nginx documentation, Module ngx_http_upstream_module
    locator: "the directives ip_hash (the first three octets of an IPv4 address as the key, and the down parameter that keeps the hashing) and hash with the consistent parameter (ketama)"
  - url: https://www.rfc-editor.org/rfc/rfc6265
    title: "A. Barth, RFC 6265, HTTP State Management Mechanism, 2011"
    locator: "Section 4.1 (the Set-Cookie header and its attributes) and Section 4.2 (the Cookie header that the client sends back)"
  - paper: doi:10.1145/258533.258660
    title: David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine and Daniel Lewin, Consistent hashing and random trees, distributed caching protocols for relieving hot spots on the World Wide Web, STOC 1997
    locator: Section 4 (ranged hash functions, and the monotonicity property that a change of the set of buckets moves only the items that must move)
---

Sticky sessions, also called session affinity, is the technique by which a [load balancer](/load-balancer/) sends every request of one client session to the same backend server. A layer 7 balancer usually does it with a *cookie* that names the server; a layer 4 balancer, which cannot read cookies, hashes the *client address*, as in [source IP hash](/source-ip-hash/). Affinity lets a server keep session state in memory and keeps its caches warm. It costs balance, because the balancer can no longer move a busy session, and it costs [failover](/failover/), because the state of a session dies with its server. With a plain hash modulo the number of servers, a change in the pool moves most clients, so address affinity uses [consistent hashing](/consistent-hashing/), which moves only the clients of the changed server.

## In plain words

A bank has several clerks. A customer who opens an account talks to one clerk, and that clerk keeps the papers on the desk. If the customer comes back and meets another clerk, the papers are not there, and the customer must start again.

So the bank gives the customer a card with the name of the clerk. Each time the customer comes back, the guard reads the card and sends the customer to that clerk. If that clerk has gone home, the guard picks another clerk and writes a new card, and only that customer starts again.

The bank could also send customers by the first letter of their surname. That needs no card. But when one clerk goes home and the bank shares the letters out again from the start, most customers get a new clerk, not only those of the clerk who left.

## When it applies

- A server keeps per-session state that is costly to move or to rebuild: a login session in memory, a shopping cart, a server-side cache of the user's data, a long protocol exchange such as a TLS session or a multi-step upload.
- The balancer can identify the session: by a cookie at layer 7, or only by the source address and port at [layer 4](/layer-4-load-balancing/).
- The model of this page: a pool of servers that changes only when a server leaves (a failure or a drain) or joins; each request carries a session identifier, a client address, and perhaps an affinity cookie from an earlier response; the balancer has a fallback policy, for example the server with the fewest sessions, to place a session that has no valid cookie. For address hashing, keys are hash values of addresses, and we count the fraction of keys whose server changes when the pool changes.

## The template

```pseudo id=main
ROUTE(r)                                              ▷ cookie affinity, layer 7
L1  c ← the affinity cookie of r, or NONE
L2  if c names a server s in the pool then send r to s; return
L3  s ← CHOOSE(pool)                                  ▷ fallback policy, for example the fewest sessions
L4  add the session of r to the sessions of s
L5  send r to s, and set the cookie c ← s on the response

ROUTE_IP(r)                                           ▷ address affinity, layer 4
L6  k ← HASH(the source address of r)
L7  s ← the server of the first point at or after k on the consistent-hash ring of the pool
L8  (map-based variant) s ← pool[k mod |pool|]
    send r to s
```

Lines L1 and L2 are the whole of cookie affinity: the balancer keeps no table, because the client carries the binding. A cookie that names a server that has left falls through to line L3, and the response sets a new cookie. Line L7 needs no state either, but it binds a client address, not a session, and line L8 shows the static map that HAProxy calls map-based and that the next claim warns against.

**Claim 1 (cookie affinity).** In the model above:

1. every request of a session goes to the server named by its cookie as long as that server is in the pool;
2. when server $s$ leaves, exactly the sessions bound to $s$ are moved, each once, at its next request, and from then on each stays on its new server;
3. when a server joins, no existing session moves, so the new server gets only new sessions and sessions moved off a server that left.

*Proof.* (1) Line L2 sends the request to the named server whenever that server is in the pool. (2) A session bound to another server $s' \ne s$ still has a valid cookie, so by (1) it does not move. A session bound to $s$ has a cookie that names no server in the pool, so its next request falls to line L3, gets a server and a new cookie on line L5, and from then on (1) applies. (3) A join changes no cookie and leaves every named server in the pool, so (1) holds for every existing session. $\square$

**Claim 2 (map-based hashing moves almost every client).** Let the pool be a list of $n \ge 2$ servers, and let key $k$ go to position $k \bmod n$ (line L8). Remove any one server, so that the list closes up to $n - 1$ servers. Then among any $n(n - 1)$ consecutive keys, exactly $n - 1$ keep their server. If instead a server joins at the end, then among any $n(n + 1)$ consecutive keys, exactly $n$ keep their server.

*Proof.* Let the removed server be at position $j$. Write $a = k \bmod n$ and $b = k \bmod (n - 1)$. Since $\gcd(n, n - 1) = 1$, the Chinese remainder theorem makes $k \mapsto (a, b)$ a bijection from any $n(n - 1)$ consecutive integers onto $\{0, \ldots, n - 1\} \times \{0, \ldots, n - 2\}$. Before the removal, key $k$ goes to the server at old position $a$. After it, the server at new position $b$ is the one at old position $b$ if $b < j$, and at old position $b + 1$ if $b \ge j$. So $k$ keeps its server exactly when $a = b < j$, which gives $j$ pairs, or when $a = b + 1$ with $j \le b \le n - 2$, which gives $n - 1 - j$ pairs. That is $n - 1$ pairs, so $n - 1$ keys. For a join at the end, the bijection is onto $\{0, \ldots, n - 1\} \times \{0, \ldots, n\}$, and $k$ keeps its server exactly when $k \bmod n = k \bmod (n + 1)$, which gives the $n$ pairs $(a, a)$ with $a \le n - 1$. $\square$

So for keys spread evenly, a removal moves a fraction $1 - 1/n$ of the clients, although only $1/n$ of them were on the removed server, and a join moves a fraction $n/(n + 1)$. With consistent hashing (line L7), a removal moves only the keys whose first point belonged to the removed server, because every other point stays where it was; this is the monotonicity property of Karger et al.

**Cost.** Cookie affinity costs $O(1)$ per request and no table at the balancer, since the client carries the binding. Address affinity costs one hash and, with a ring of $V$ points, a binary search, $O(\log V)$. The real cost is in balance and in failover, as the example shows.

**Example: four servers, twelve keys.** Keys $0$ to $11$ on servers $s_0$ to $s_3$ by $k \bmod 4$. Server $s_3$ fails, and the list becomes $s_0, s_1, s_2$, so keys go by $k \bmod 3$.

| key | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| before, $k \bmod 4$ | 0 | 1 | 2 | 3 | 0 | 1 | 2 | 3 | 0 | 1 | 2 | 3 |
| after, $k \bmod 3$ | 0 | 1 | 2 | 0 | 1 | 2 | 0 | 1 | 2 | 0 | 1 | 2 |

Only keys 0, 1 and 2 keep their server, which is $n - 1 = 3$ of $n(n - 1) = 12$. Three keys (3, 7 and 11) had to move, and six more move with no need. With 10,000 random IPv4 addresses hashed with SHA-256 (seed 1 in the tests), the same change moves 7,514 clients by $k \bmod n$ and 2,366 on a ring with 100 points per server, and the 2,366 are exactly the clients that were on $s_3$.

**Example: what affinity does to balance.** Sessions arrive at servers A and B, and the fallback policy picks the server with the fewest sessions, with ties to the first name. Sessions 1 to 6 go to A, B, A, B, A, B. Then A fails: sessions 1, 3 and 5 move to B at their next request (Claim 1, part 2), and B now has all 6. A new server C joins. No old session moves (part 3), so B keeps 6 sessions while C has none, and the next 6 new sessions all go to C before a 7th goes to B. The load evens out only as the old sessions end. Balance is also per session, not per request: if session 1 sends 50 requests and every other session sends 1, A carries 52 requests while B carries 3, and the balancer cannot help.

**Example: shared addresses.** Address affinity sees one client where a NAT gateway or a proxy hides many users. With 8,000 random addresses plus 2,000 users behind one address, on a ring of 4 servers with 100 points each (seed 2 in the tests), the server that owns that address gets 4,319 of the 10,000 users, while the others get 1,801 to 1,962. The nginx ip_hash method makes this coarser on purpose: it hashes only the first three octets of an IPv4 address, so all 256 addresses of a /24 network share one server.

## Classic examples

- **HAProxy cookies.** The `cookie` keyword enables cookie persistence in three modes. In `insert` mode, HAProxy adds a cookie with the server's identifier to the response when the client does not already have a valid one. In `rewrite` mode, the server sets the cookie and HAProxy rewrites its value to the server's identifier. In `prefix` mode, HAProxy prefixes an existing application cookie with the server's identifier and strips the prefix on the way in. The `maxidle` and `maxlife` options make an inserted cookie expire, so that clients do not stay on one server forever after the pool changes.
- **HAProxy source hashing.** `balance source` hashes the client address and divides by the total weight of the running servers. The manual says that it is generally used in TCP mode, where no cookie can be inserted, and that many clients move when the number of running servers changes. `hash-type consistent` replaces the static map by a tree with many points per server, so that only the associations of a server that goes up or down move.
- **nginx.** `ip_hash` keeps a client on one server except when that server is unavailable. To take a server out for a while without rehashing the others, the manual says to mark it `down` instead of deleting it from the list. The `hash` directive with the `consistent` parameter uses ketama consistent hashing.

## Variations

- **Cookie set by the balancer, or by the application.** A balancer cookie works with any application. An application cookie lets the application decide when a session starts and ends, for example to drop the affinity at logout.
- **Encoded cookie.** The cookie holds an opaque or encrypted server identifier, so that it does not reveal internal names and a client cannot pick a server by hand.
- **Bounded loads.** Address affinity on a plain ring can overload a server. [Consistent hashing with bounded loads](/bounded-load-consistent-hashing/) caps each server at $(1 + \varepsilon)$ times the average and sends the overflow to the next server, which trades a little affinity for balance. [Rendezvous hashing](/rendezvous-hashing/) gives the same monotonicity as a ring with no ring.
- **Drain with affinity.** A [draining](/connection-draining/) server can keep its existing sessions and refuse only new ones. The drain then lasts as long as the sessions, so it needs a short timeout or a shared session store.
- **Stateless servers.** Keep the session in a shared store or in a signed cookie at the client. Then any server can serve any request, and affinity becomes only a way to keep caches warm: it can break at any time without a user-visible error.

## Pitfalls

- **Affinity as a substitute for shared state.** If session state lives only on one server, every server failure, deploy or scale-in logs users out. Claim 1 bounds the damage to the sessions of that server, but it does not remove it.
- **Map-based hashing.** By Claim 2, a hash modulo the number of live servers moves about $1 - 1/n$ of all clients on every failure, every recovery and every scale event. Use consistent hashing, or follow the nginx advice and mark a server down instead of removing it.
- **Cached cookies.** If an inserting balancer puts the cookie on a cacheable page, a shared cache can serve that page with the same cookie to many users, and one server gets much more traffic than the others. HAProxy offers `nocache` and `postonly` for this.
- **A cookie for a dead server.** If the balancer forces persistence even when the named server is down, the client cannot reach the service until the cookie expires. Fall through to line L3, as in HAProxy's `option redispatch`.
- **Changing client addresses.** A mobile client can change its address in the middle of a session, and address affinity then moves it. Clients behind a NAT or a large proxy all share one address and one server.
- **Hidden imbalance.** Average load can look fine while one server carries a few heavy sessions. Watch the most loaded server, not only the mean, and prefer a fallback policy such as [least connections](/least-connections/) for new sessions.
- **Health checks and stickiness.** A server that fails its [health check](/health-checking/) must lose its sessions, or the clients pinned to it see errors. A server that only becomes slow keeps its sessions, so stickiness slows the move of load away from a slow server.

## Exercises

1. In the four-server example, which keys keep their server if $s_1$ fails instead of $s_3$? Check that there are again 3.
2. Show that with $n$ servers and a join at the end, map-based hashing moves a fraction $n/(n + 1)$ of evenly spread keys, while a ring moves on average $1/(n + 1)$.
3. A pool of 10 servers with cookie affinity has 1,000 sessions, 100 on each. One server fails and is replaced by a new one. How many sessions does the new server have right after the failure? If sessions end at random with a mean life of 30 minutes and new sessions arrive at the same rate, how long until the new server has about its share?
4. Why can a layer 4 balancer not use cookie affinity for HTTPS traffic that it does not decrypt? What can it use instead?
5. Give a sequence of session arrivals and request counts for which the fewest-sessions fallback leaves one server with 10 times the requests of another.

## References
