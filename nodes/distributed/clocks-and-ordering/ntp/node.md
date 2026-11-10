---
tag: PXEY9N
kind: algorithm
slug: ntp
name: Network Time Protocol
aliases:
- NTP
- NTPv4
area: distributed/clocks-and-ordering
level: core
summary: Servers in strata below reference clocks. A client takes four timestamps per exchange, computes offset and delay, filters samples, rejects falsetickers, combines the rest and disciplines its clock.
solves: [clock-synchronization]
model: asynchronous-model
complexity:
  vars: {m: the number of servers that the client polls}
  time: {worst: O(m^3)}
  space: {extra: O(m)}
  messages: {worst: 2m}
properties: {deterministic: true, recursive: false}
history:
  year: 1985
  people: [David L. Mills]
  note: Mills specified NTP in RFC 958 (1985), described it in IEEE Transactions on Communications in 1991, and led its design up to version 4, RFC 5905 (2010).
prereqs: [cristian-algorithm, marzullo-algorithm]
see_also: [precision-time-protocol, cristian-algorithm, marzullo-algorithm, berkeley-algorithm, clock-skew, clock-drift, monotonic-clock, truetime]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc5905
    title: David Mills, Jim Martin, Jack Burbank and William Kasch, RFC 5905, Network Time Protocol Version 4, Protocol and Algorithms Specification, 2010
    locator: Section 3 (strata), Section 6 (timestamps), Section 8 (on-wire protocol, offset and delay), Section 10 (clock filter), Section 11.2 (selection, cluster and combine), Section 11.3 (clock discipline)
  - paper: doi:10.1109/26.103043
    title: David L. Mills, Internet time synchronization, the Network Time Protocol, IEEE Transactions on Communications 39(10), 1991
    locator: pages 1482 to 1493
  - book: isbn:9780132143011
    title: George Coulouris, Jean Dollimore, Tim Kindberg and Gordon Blair, Distributed Systems, Concepts and Design, fifth edition, Addison-Wesley, 2012
    locator: Chapter 14, Section 14.3 (the Network Time Protocol)
---

The *Network Time Protocol* (NTP) keeps the clocks of computers on the Internet close to UTC. Servers form a hierarchy of *strata* below reference clocks. A client exchanges packets with several servers, and from the four timestamps of each exchange it computes the offset $\theta$ and the round trip delay $\delta$ of that server, with $|\theta - \theta_0| \le \delta/2$ for the true offset $\theta_0$. It then filters the samples, rejects wrong servers with a variant of [Marzullo's algorithm](/marzullo-algorithm/), combines the rest, and steers its clock with a feedback loop.

## In plain words

Your computer asks a time server for the time, like in [Cristian's algorithm](/cristian-algorithm/), but it notes four moments: when the question leaves, when the server gets it, when the server answers, and when the answer comes back. From these four it can remove the time that the server spent, and it gets two numbers: how far its clock is from the server clock, and how long the messages travelled.

If the trip out and the trip back take the same time, the first number is exact. If not, the error is at most half the travel time. So your computer asks many times, trusts the fastest answers, asks several servers, ignores servers that disagree with most others, and then turns its clock slowly toward the result.

## The problem

**Model.** A client A reads a set of servers over a network with no upper bound on delay, in the [asynchronous model](/asynchronous-model/) for messages. Each server has a clock, a *stratum*, and an error estimate for its own time (the root delay and root dispersion). The client clock drifts at up to PHI = 15 ppm by the assumption of RFC 5905 (see [clock drift](/clock-drift/)). Some servers may be *falsetickers*: their time is wrong, by fault or by attack. The ones that are right are *truechimers*.

**Goal.** External synchronization: keep the client clock within a small, known distance of UTC, with no steps back in normal operation, and with few messages.

**Strata.** Stratum 1 servers, the *primary* servers, read a reference clock such as a GPS receiver or an atomic clock. A server that synchronizes to a stratum $s$ server has stratum $s + 1$, up to 15. Stratum 16 means unsynchronized, and stratum 0 in a packet means unspecified or invalid. A client picks servers of low stratum and short distance, so that errors do not add up along a long chain.

**Timestamps.** An NTP timestamp has 64 bits: 32 bits of seconds since 1 January 1900 and 32 bits of fraction, so the resolution is about 233 ps and the seconds field wraps in 2036. The protocol works with differences, so it handles the wrap by era arithmetic.

## The algorithm

```pseudo id=main
NTP-EXCHANGE(server)                           ▷ client A, server B
    T1 ← A's clock when the request leaves
    T2 ← B's clock when the request arrives;  T3 ← B's clock when the reply leaves
    T4 ← A's clock when the reply arrives
L1  θ ← ((T2 − T1) + (T3 − T4)) / 2             ▷ offset of B's clock from A's
L2  δ ← (T4 − T1) − (T3 − T2)                    ▷ round trip delay without the server time
L3  push (θ, δ) into the shift register of B; keep the last 8 samples
L4  B's offset and delay ← the sample with the least δ  ▷ the clock filter

NTP-MITIGATE(servers)
L5  [l, u] ← SELECT({(θ_B, λ_B)})                ▷ Marzullo variant, λ_B = root distance of B
        truechimers ← the servers with θ_B in [l, u]
L6  while more than NMIN = 3 survivors and the largest selection jitter
          is not below the smallest peer jitter do
        drop the survivor with the largest selection jitter      ▷ cluster
L7  Θ ← Σ θ_B / λ_B  ÷  Σ 1 / λ_B over the survivors           ▷ combine
    pass Θ to the clock discipline
```

The four timestamps come from the packets: B copies $T_1$ from the request into the reply, together with $T_2$ and $T_3$, and A reads $T_4$ on arrival. SELECT is the selection algorithm of RFC 5905, Section 11.2.1, which the page on [Marzullo's algorithm](/marzullo-algorithm/) describes. The *root distance* $\lambda$ bounds the error of a server's time with respect to the primary reference: it is half the total round trip delay to the reference, plus the dispersion (the error that grows at PHI per second since the last update) and the jitter. The selection jitter of a survivor is the RMS difference between its offset and the offsets of the others; the peer jitter is the RMS difference between the samples in its own register.

**Clock discipline (Section 11.3).** The combined offset $\Theta$ drives a hybrid phase-locked and frequency-locked loop that adjusts both the phase and the rate of the clock. If $|\Theta|$ exceeds STEPT = 0.125 s for a while, the client steps the clock; below that it slews it (see [monotonic clock](/monotonic-clock/)). Above PANICT = 1000 s it stops and asks for an operator. The poll interval $2^\tau$ seconds grows from 16 s up to about 36 hours when the clock is stable.

## Example

The server clock is $\theta_0 = 0.25$ s ahead of the client clock. The request takes $a = 10$ ms, the server holds it for 1 ms, and the reply takes $b = 30$ ms.

| timestamp | value | how |
|---|---|---|
| $T_1$ | 100.000 | client clock at send |
| $T_2$ | 100.260 | $T_1 + a + \theta_0$ on the server clock |
| $T_3$ | 100.261 | 1 ms later |
| $T_4$ | 100.041 | $T_3 - \theta_0 + b$ on the client clock |

Line L1 gives $\theta = ((100.260 - 100.000) + (100.261 - 100.041))/2 = (0.260 + 0.220)/2 = 0.240$ s. Line L2 gives $\delta = 0.041 - 0.001 = 0.040$ s. The error is $0.240 - 0.250 = -0.010 = (a - b)/2$, and it is within the bound $\delta/2 = 0.020$ s. If the two delays had been 20 ms each, $\theta$ would be exactly 0.250.

**Selection.** Four servers give $(\theta, \lambda) = (10, 4)$, $(12, 3)$, $(11, 5)$ and $(50, 2)$ in ms. The selection finds no region where all four meet, and with $f = 1$ it returns $[9, 14]$. The server at 50 ms is a falseticker and is dropped.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Let B's clock be $\theta_0$ ahead of A's, and let the one-way delays be $a$ out and $b$ back, both at least 0. Then $T_2 = T_1 + a + \theta_0$ and $T_4 = T_3 - \theta_0 + b$, so
$$T_2 - T_1 = \theta_0 + a, \qquad T_3 - T_4 = \theta_0 - b.$$
Adding gives $\theta = \theta_0 + (a - b)/2$, and line L2 gives $\delta = a + b$. Since $|a - b| \le a + b$,
$$|\theta - \theta_0| \le \delta / 2.$$
The bound is reached when one delay is 0. No rule can do better from the four timestamps alone: the runs $(\theta_0, a, b)$ and $(\theta_0 + s, a - s, b + s)$ give the same timestamps for every $s$ with $-b \le s \le a$, so the true offset can be anywhere in $[\theta - \delta/2, \theta + \delta/2]$. This is why the clock filter keeps the sample with the least delay: it has the smallest error bound.

If at most $f$ servers are falsetickers with $2f$ less than the number of servers, the selection returns an interval $[l, u]$ that holds the true offset (proved on [Marzullo's algorithm](/marzullo-algorithm/)). Every survivor has $\theta_B \in [l, u]$, and line L7 takes a weighted average with positive weights, so $\Theta \in [l, u]$ and $|\Theta - \theta_0| \le u - l$.

## Complexity

One exchange sends 2 messages, so polling $m$ servers once sends $2m$ messages. Lines L1 to L4 take $O(1)$ time per sample, since the register has 8 stages. Selection sorts $3m$ entries and scans them at most $m/2$ times, so it takes $O(m^2)$ time. The cluster step of line L6 recomputes the selection jitter of each survivor, $O(m^2)$, at most $m$ times, so $O(m^3)$ in the simple form of the code. A client has few servers, often 4 to 10, so this is small. The client stores $O(m)$ registers of 8 samples each.

## Properties

- **Exact for symmetric paths.** If $a = b$, $\theta = \theta_0$, whatever the delays and the server time.
- **A known error bound.** Each sample comes with $\delta/2$, and each server with its root distance.
- **Tolerant of falsetickers.** Up to fewer than half of the servers can be wrong.
- **Hierarchical.** Errors and distances add up along the strata, and the root distance tells the client how much.
- **Slewing.** In normal operation the clock never steps; it is slewed, so it stays monotonic.

## Variants and improvements

- **Modes.** Besides client and server, NTP has symmetric mode between peers of the same stratum, and broadcast mode, where a server sends the time without requests and clients use a delay that they measured once.
- **SNTP.** The Simple Network Time Protocol uses the same packets and the formulas of lines L1 and L2, but leaves out the filter, the selection and the discipline. It suits clients that need less precision.
- **Hardware timestamps.** Taking $T_1$ to $T_4$ in the network card removes the time spent in the operating system. [PTP](/precision-time-protocol/) goes further and corrects for the time in each switch.
- **Interleaved mode and Chrony.** Later implementations send the exact transmit time of the previous packet in the next one, and Chrony replaces the filter and the discipline with its own estimators. These are outside RFC 5905.
- **Security.** Network Time Security (RFC 8915) adds authentication of the packets, so an attacker in the path cannot forge a time.

## When to use it

Use NTP on any computer that needs UTC within milliseconds over the Internet, or within less than a millisecond on a good local network. When sub-microsecond accuracy on a local network is needed, use [PTP](/precision-time-protocol/). When a program needs a guaranteed bound for ordering, wrap the time in an interval, as [TrueTime](/truetime/) does.

## Pitfalls

- **Asymmetric paths.** A path that is slower in one direction gives an error of $(a-b)/2$ that the client cannot see. Only the bound $\delta/2$ is known.
- **Few servers.** With one server there is no selection; with two, a disagreement has no majority. Use at least four.
- **Steps at start.** A client that starts far from UTC steps its clock. Programs that measure durations with the wall clock see a jump. Use a [monotonic clock](/monotonic-clock/) for durations.
- **Leap seconds.** NTP announces leap seconds in the packet header. Systems handle them by a repeated second or by smearing them over hours, and two systems that use different methods disagree by up to a second during the event.
- **Trusting the root distance.** The bound holds only if every server on the path reports honest delays and dispersions.

## Implementations

## History

David L. Mills of the University of Delaware specified the first version of NTP in RFC 958 in 1985, building on earlier time protocols of the ARPANET. Version 1 followed in RFC 1059 (1988), version 2 in RFC 1119 (1989) and version 3 in RFC 1305 (1992). Mills described the design and its measurements in IEEE Transactions on Communications in 1991. Version 4, with the algorithms on this page, is RFC 5905 (2010) by Mills, Martin, Burbank and Kasch. Mills wrote the reference implementation, ntpd, and kept it for decades.

## References
