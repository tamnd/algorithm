---
tag: NZDW12
kind: concept
slug: syn-flooding
name: SYN flooding
aliases:
- SYN flood
area: security-and-privacy/network-and-web-security
level: intro
summary: A denial of service on TCP servers. Connection requests that never complete fill the table of half-open connections, so the server turns away real clients.
history:
  year: 1996
  people: [William R. Cheswick, Steven M. Bellovin]
  note: Cheswick and Bellovin found the weakness in 1994. It became public in 1996, and attacks that year led to a CERT advisory and to the defenses that RFC 4987 lists.
see_also: [syn-cookies, ingress-filtering, ip-traceback-problem, probabilistic-packet-marking, algorithmic-complexity-attack, token-bucket, intrusion-detection-problem]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc4987"
    title: Wesley M. Eddy, TCP SYN flooding attacks and common mitigations, RFC 4987, August 2007
    locator: Section 2.1 (history), Section 2.2 (theory of operation), Sections 3.1 to 3.8 (filtering, larger backlog, shorter timer, recycling the oldest half-open TCB, SYN cache, SYN cookies, hybrids, firewalls and proxies) and Section 4 (analysis)
  - url: "https://www.rfc-editor.org/rfc/rfc9293"
    title: Wesley M. Eddy (editor), Transmission Control Protocol (TCP), RFC 9293, August 2022
    locator: Section 3.5 (the three-way handshake and the SYN-RECEIVED state) and Section 3.4.1 (initial sequence number selection)
  - url: "https://www.rfc-editor.org/rfc/rfc2827"
    title: Paul Ferguson and Daniel Senie, Network ingress filtering, RFC 2827 (BCP 38), May 2000
    locator: Sections 2 and 3 (forged source addresses in SYN floods, and the filter that stops them at the edge)
---

SYN flooding is a denial of service attack on a TCP server that fills the server's table of half-open connections. Each request starts a TCP handshake that never finishes, and the server keeps state for it until a timer ends. When the table is full, the server drops new requests, so real clients cannot connect. The attack needs little bandwidth, and its packets usually carry forged source addresses, which links it to [ingress filtering](/ingress-filtering/) and the [IP traceback problem](/ip-traceback-problem/).

## In plain words

A restaurant takes table bookings by phone. When a caller asks for a table, the restaurant writes the name in a book with a few lines and waits for the caller to confirm. If nobody confirms, the line is wiped after half an hour. A prankster calls again and again with false names and never confirms. Soon every line in the book is taken by a booking that will never happen, and real guests hear "we are full".

The server does the same thing with connection requests. It writes each request in a small table and waits for the last message of the handshake. The attacker sends many first messages and never sends the last one. The fix is to keep less memory per request, or none at all, or to throw out the oldest unfinished entries first.

## The idea

**The handshake.** A TCP connection opens with three messages ([RFC 9293](https://www.rfc-editor.org/rfc/rfc9293), Section 3.5). The client sends a SYN segment with its initial sequence number $x$. The server answers with a SYN-ACK segment that carries its own initial sequence number $y$ and the acknowledgment $x + 1$. The client finishes with an ACK of $y + 1$. Between its SYN-ACK and the final ACK, the server holds the connection in the SYN-RECEIVED state. It stores a transmission control block (TCB) with the addresses, the ports, $x$, $y$ and the options the client asked for. RFC 4987 calls such an entry half-open.

**The resource.** A listening socket keeps at most $B$ half-open entries, the backlog. Each entry stays until the final ACK arrives, a reset arrives, or a timer of length $T$ ends after the SYN-ACK retransmissions. The backlog is a fixed resource, and the attack spends it.

**The condition.** Suppose that SYNs that never complete arrive at a rate of $r$ per second. Each one holds a slot for the full time $T$. By Little's law, the mean number of slots they hold is $\min(B, rT)$ once the table reaches a steady state. So the table stays full when

$$
r \, T \ge B ,
$$

and then a real SYN gets a slot only when it arrives in the short gap after an old entry ends and before the next forged SYN. The required rate $B/T$ is small: it does not depend on the server's link speed or its processor, so more bandwidth does not help the server. RFC 4987, Section 2.2, states the same condition in words: the attack works as long as new SYNs arrive faster than the server reaps old entries.

**Forged sources.** The attacker does not need to see the SYN-ACK, so the SYN can carry a source address that is not its own. The SYN-ACK goes to that address. If a host there answers with a reset, the entry ends early (RFC 4987, Section 2.2). Forged sources hide the attacker and make filtering by source useless. Two network defenses follow: [ingress filtering](/ingress-filtering/) stops forged sources at the edge, and IP traceback finds the path of the packets after the fact.

**The threat model.** The adversary can send SYN segments at a rate $r$ with any source address it chooses. It cannot see traffic to the forged addresses and cannot guess the server's secrets. A flood that fills the server's link with traffic is a different attack: no change on the host stops it, and it needs help from the network.

**The defenses** (RFC 4987, Section 3). They divide into those that make the table harder to fill and those that remove the table.

| defense | RFC 4987 | what changes | cost or limit |
|---|---|---|---|
| filtering | 3.1 | forged sources are dropped at the edge | needs deployment in other networks |
| larger backlog | 3.2 | $B$ grows | memory and search time grow with $B$ |
| shorter timer | 3.3 | $T$ shrinks | slow real clients fail |
| recycle the oldest | 3.4 | a new SYN replaces the oldest entry | fails when $r$ is so high that a real entry is replaced before its ACK |
| SYN cache | 3.5 | a small entry in a hash table instead of a full TCB | still a table, only a larger effective $B$ |
| [SYN cookies](/syn-cookies/) | 3.6 | the state goes into $y$, the server keeps none | most TCP options are lost when the table is full |
| hybrid | 3.7 | cache first, cookies when the cache is full | more code |
| firewalls and proxies | 3.8 | a middlebox ends the handshake first | the middlebox is now the target |

Of these, only SYN cookies make the server's memory independent of $r$. The cache-based methods trade memory for a larger effective $B$, so the condition $rT \ge B$ still holds at a higher rate. Section 4 of RFC 4987 concludes that the SYN cache and SYN cookies are the only viable end-host techniques found so far. It advises that SYN cookies stay off by default because of the lost options, while a SYN cache can be on by default.

## Examples

**A table that fills.** Take a toy server at the documentation address 192.0.2.10 with $B = 4$ slots and $T = 3$ ticks. Two SYNs with forged sources from 198.51.100.0/24 arrive at the start of each tick, and none completes. A real client from 203.0.113.7 sends a SYN at tick 2. An entry made at tick $t$ ends at tick $t + 3$.

| tick | entries that end | forged SYNs stored | forged SYNs dropped | entries after the tick | real SYN |
|---|---|---|---|---|---|
| 0 | 0 | 2 | 0 | 2 | |
| 1 | 0 | 2 | 0 | 4 | |
| 2 | 0 | 0 | 2 | 4 | dropped |
| 3 | 2 (from tick 0) | 2 | 0 | 4 | |
| 4 | 2 (from tick 1) | 2 | 0 | 4 | |

From tick 1 on, the table is full at the end of every tick. Here $rT = 2 \cdot 3 = 6 \ge 4 = B$, so the condition holds. With one forged SYN per tick, $rT = 3 < 4$, and one slot stays free for real clients.

**The rate that is needed.** For a backlog of $B = 256$ and a timeout of $T = 30$ seconds, the condition needs only $r = 256/30 = 8.53$ SYNs per second that never complete. Doubling $B$ doubles that rate. Halving $T$ also doubles it, but then a real client on a slow path that needs more than 15 seconds for its ACK fails. This is the trade-off of Sections 3.2 and 3.3 of RFC 4987.

**The same server with SYN cookies.** When the table is full, the server answers each SYN with a SYN-ACK whose $y$ is a keyed hash of the connection and a time counter, and it stores nothing. The real client's ACK carries $y + 1$, and the server checks it and builds the TCB then. The forged SYNs cost the server one hash and one SYN-ACK each, and no memory. The [SYN cookies](/syn-cookies/) page gives the algorithm, its proof and its code.

## Where it is used

- [SYN cookies](/syn-cookies/) are the standard end-host defense. They remove the per-request state.
- [Ingress filtering](/ingress-filtering/) (BCP 38) stops floods with forged sources at the network where they start.
- The [IP traceback problem](/ip-traceback-problem/), [probabilistic packet marking](/probabilistic-packet-marking/) and [hash-based IP traceback](/hash-based-ip-traceback/) find where forged floods come from.
- [Algorithmic complexity attacks](/algorithmic-complexity-attack/) are the same pattern on a different resource: a small input that makes the victim spend a large part of a fixed budget.
- Rate limits such as a [token bucket](/token-bucket/) and alarms from an [intrusion detection](/intrusion-detection-problem/) system can cap the rate of SYNs from one network, but forged sources weaken both.

## References
