---
tag: R0C39B
kind: algorithm
slug: binary-exponential-backoff
name: Binary exponential backoff
aliases:
- truncated binary exponential backoff
area: systems/networking-algorithms
level: intro
summary: After the n-th collision of a frame, wait a random number of slots from 0 to 2^min(n,10) - 1; drop the frame after 16 attempts. Ethernet uses it.
model: synchronous-model
complexity:
  vars: {n: the number of collisions of the frame}
  time: {best: Θ(1), worst: Θ(2^n)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1976
  people: [Robert M. Metcalfe, David R. Boggs]
  note: The Ethernet paper let each station back off after collisions with a random interval whose mean grows with the load. IEEE 802.3 fixed the truncated binary form.
prereqs: [exponential-backoff]
see_also: [csma-cd, medium-access-control, slotted-aloha, csma-ca, geometric-distribution, markov-chain]
sources:
  - paper: doi:10.1145/360248.360253
    title: Robert M. Metcalfe and David R. Boggs, Ethernet, Distributed packet switching for local computer networks, Communications of the ACM 19(7), 1976, 395-404
    locator: the section on collision control (the retransmission interval and its adjustment to the load)
  - paper: "David J. Aldous, Ultimate instability of exponential back-off protocol for acknowledgment-based transmission control of random access communication channels, IEEE Transactions on Information Theory IT-33(2), 1987, 219-223"
    title: Ultimate instability of exponential back-off protocol
    locator: the main theorem (instability for every positive arrival rate in the model with infinitely many users)
  - paper: doi:10.1145/28395.28422
    title: Johan Håstad, Tom Leighton and Brian Rogoff, Analysis of backoff protocols for multiple access channels, Proceedings of STOC 1987, 241-253; also SIAM Journal on Computing 25(4), 1996, 740-774
    locator: the results on binary exponential backoff and on polynomial backoff with a finite number of users
  - paper: doi:10.1145/44483.44488
    title: Jonathan Goodman, Albert G. Greenberg, Neal Madras and Peter March, Stability of binary exponential backoff, Journal of the ACM 35(3), 1988, 579-602
    locator: the stability result for a finite number of stations and a small arrival rate
  - book: isbn:9780132126953
    title: Andrew S. Tanenbaum and David J. Wetherall, Computer Networks, fifth edition
    locator: Section 4.3.2, Classic Ethernet MAC Sublayer Protocol (binary exponential backoff)
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition
    locator: Section 6.3.2, Random Access Protocols (CSMA/CD and the binary backoff algorithm)
---

Binary exponential backoff (BEB) is the collision rule of classic Ethernet. After the $n$-th collision of a frame, the station waits $k$ slot times, with $k$ drawn uniformly from $0, 1, \ldots, 2^{\min(n,10)} - 1$, and then tries again. After 16 attempts that all collide, it drops the frame. The window doubles while collisions repeat, so the stations spread out as fast as the number of contending stations requires. It is the random, slotted case of [exponential backoff](/exponential-backoff/), and the retransmission rule of [CSMA/CD](/csma-cd/).

## In plain words

Several stations share one cable. When two talk at the same time, both messages are lost, and both stations notice it.

Each station then picks a random number of short waiting periods: after the first collision, 0 or 1; after the second, 0 to 3; after the third, 0 to 7; and so on, doubling each time. If two stations pick different numbers, the one with the smaller number goes first and the other hears it and waits. If many stations are in the crowd, the range soon grows large enough to separate them.

The range stops growing at 0 to 1023. After 16 failures in a row, the station gives up on that message and reports an error.

## The problem

Stations share a broadcast channel with no central control and no knowledge of how many other stations want to send. Two transmissions that overlap destroy each other. Each station must choose when to retry so that, with high probability, the stations soon transmit one at a time, without wasting the channel when few stations contend.

## The algorithm

In 10 Mbit/s Ethernet, a slot time is 512 bit times, 51.2 µs. The rule is for one frame of one station.

```pseudo id=main
BEB-SEND(frame)
L1  n ← 0
L2  transmit the frame when the channel is free
L3  if there is no collision then return success
L4  n ← n + 1
L5  if n = 16 then drop the frame; return failure
L6  k ← a uniform random integer in {0, 1, ..., 2^min(n,10) − 1}
L7  wait k slot times; go to L2
```

IEEE 802.3 calls the limits attemptLimit (16) and backoffLimit (10). The station starts again at $n = 0$ for its next frame.

## Example

Two stations collide in slot 0. After the first collision each picks $k \in \{0, 1\}$. With probability $1/2$ the picks differ, and the station with $k = 0$ sends in slot 1 while the other one waits. With probability $1/2$ they collide again and pick from $\{0, 1, 2, 3\}$, where they collide with probability $1/4$, and so on. The expected number of collisions is

$$1 + \tfrac12 + \tfrac12 \cdot \tfrac14 + \tfrac12 \cdot \tfrac14 \cdot \tfrac18 + \cdots \approx 1.6416,$$

and a simulation of 20000 runs gives the same mean to within 0.03. If the random number generator always returned 0, both stations would collide 16 times and drop their frames.

In a slotted simulation with $s$ stations that each have 5 frames, all frames are sent with 22 collisions in total for $s = 4$, 71 for $s = 10$, and 195 for $s = 20$.

The *capture effect* shows in the same simulation: with two stations that each have 100 frames, in each of five seeds one station sends all its 100 frames before the other sends any. The winner of a contention starts its next frame at $n = 0$, while the loser keeps its large window, so the winner keeps winning.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). A frame has at most 16 attempts, with at most $2^{\min(n,10)} - 1$ slots of wait after collision $n$, so every frame is sent or dropped within $16 + 7151$ slots of its first attempt, whatever the other stations do. After their $c$-th collision, two stations collide again with probability exactly $2^{-\min(c,10)}$, which gives the mean of 1.6416 collisions. With $s$ stations and a window of $W$ values, a shared smallest pick has probability at most $\binom{s}{2}/W$, so about $2\log_2 s$ doublings make the window large enough.

The long-run behaviour is harder. In the model with infinitely many users, where each new frame comes from a new station with Poisson arrivals, Aldous (1987) proved that BEB without truncation is unstable for every positive arrival rate: the throughput tends to 0 and the backlog grows without bound. For a finite number of stations, Goodman, Greenberg, Madras and March (1988) proved stability for small enough arrival rates. Håstad, Leighton and Rogoff (STOC 1987, SIAM Journal on Computing 1996) proved that BEB is unstable for large enough arrival rates below 1, while polynomial backoff, with a window that grows like a power of $n$, is stable for every arrival rate below 1 when the number of users is finite.

## Complexity

Drawing $k$ costs $O(1)$. A frame waits $O(2^n)$ slots after $n$ collisions, and at most 7151 slots in total. The state is the collision count.

## Properties

- **Distributed.** Each station needs only its own collision count.
- **Adaptive.** The window doubles until it is about as large as the number of contending stations.
- **Truncated.** The window stops at 1024 slots, and the frame is dropped after 16 attempts.
- **Unfair in the short run.** The capture effect lets a station that has just won keep the channel.
- **Randomized.** Without independent random picks, stations that collide stay in step.

## Variants and improvements

- **Polynomial backoff.** A window that grows like $n^\alpha$ for some $\alpha > 1$ is stable with a finite number of users (Håstad, Leighton and Rogoff).
- **Wi-Fi.** IEEE 802.11 doubles a contention window from $CW_{\min}$ to $CW_{\max}$ after each failed transmission, and counts down only while the channel is idle: see [CSMA/CA](/csma-ca/).
- **Capture fixes.** Proposals such as the binary logarithmic arbitration method (BLAM) change the counter rules to reduce the capture effect.
- **General retry policies.** Services use the same idea with continuous random waits and a cap: see [exponential backoff](/exponential-backoff/).

## When to use it

Use it on a shared channel where stations detect collisions and do not know how many others contend: classic half-duplex Ethernet, and, in a changed form, wireless LANs. Switched full-duplex Ethernet has no collisions, so it does not use BEB.

## Pitfalls

- **Correlated random numbers.** Stations that seed their generators the same way, for example from the same clock at power-on, pick the same $k$ and collide again.
- **Treating 16 failures as rare.** On a very busy shared segment, frames are dropped, and the upper layer must retransmit them.
- **Expecting fairness.** The capture effect can starve a station for a long time.
- **Confusing it with a retry policy.** BEB counts whole slot times and resets the count for each frame; a service retry policy waits a continuous time and keeps the count for one request.

## Implementations

## History

The ALOHA network (around 1970) retransmitted after a random delay. Metcalfe and Boggs's Ethernet paper (1976) let each station adjust its retransmission interval to the load, doubling it after each collision. The DIX Ethernet specification and IEEE 802.3 (1983) fixed the truncated binary form, with a window of at most 1024 slots and 16 attempts. The theory followed: Aldous (1987) proved instability in the model with infinitely many users, Goodman, Greenberg, Madras and March (1988) proved stability for small loads with finitely many stations, and Håstad, Leighton and Rogoff (1987) compared it with polynomial backoff.

## References
