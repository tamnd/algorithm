---
tag: F0PB77
kind: algorithm
slug: cristian-algorithm
name: Cristian's algorithm
aliases:
- Cristian's clock synchronization
area: distributed/clocks-and-ordering
level: intro
summary: A client asks a time server for the time and sets its clock to the reply plus half the round trip time. The error is at most half the round trip minus the minimum one-way delay.
solves: [clock-synchronization]
model: asynchronous-model
complexity:
  vars: {k: the number of attempts}
  time: {worst: O(k), best: O(1)}
  space: {extra: O(1)}
  messages: {worst: 2k, best: "2"}
properties: {deterministic: true, recursive: false}
history:
  year: 1989
  people: [Flaviu Cristian]
  note: Cristian published probabilistic clock synchronization, with the round trip bound and the retry rule, in Distributed Computing in 1989.
prereqs: [clock-synchronization]
see_also: [ntp, berkeley-algorithm, clock-skew, clock-drift, monotonic-clock, clock-synchronization-lower-bound]
sources:
  - paper: doi:10.1007/BF01784024
    title: Flaviu Cristian, Probabilistic clock synchronization, Distributed Computing 3(3), 1989
    locator: pages 146 to 158
  - book: isbn:9780132143011
    title: George Coulouris, Jean Dollimore, Tim Kindberg and Gordon Blair, Distributed Systems, Concepts and Design, fifth edition, Addison-Wesley, 2012
    locator: Chapter 14, Section 14.3 (Cristian's method and its accuracy)
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 3 (physical clock synchronization)
---

*Cristian's algorithm* sets the clock of a client from a time server. The client sends a request, the server replies with its clock reading $T$, and the client sets its clock to $T$ plus half the measured round trip time. If each one-way delay is at least $d_{\min}$, the error is at most half the round trip minus $d_{\min}$, so a short round trip gives a small error. The client retries until a round trip is short enough, which is why Cristian (1989) called the method *probabilistic* [clock synchronization](/clock-synchronization/).

## In plain words

You phone a friend who has an exact watch and ask for the time. Your friend says "ten o'clock". By the time you hear it, some time has passed, but you do not know how much. You know how long the whole call took, from your question to the answer. The answer was given somewhere in the middle of the call, so you add half of the call time to what your friend said.

How wrong can you be? At most half of the call time, and less if you know that a message always takes some minimum time. A short call means a small error. So if a call is slow, you hang up and call again, until you get a fast one.

## The problem

**Model.** A time server S has a correct clock. A client P has a clock $C$ with drift bound $\rho$ (see [clock drift](/clock-drift/)). Messages between P and S have no upper bound on their delay, but each one-way delay is at least a known $d_{\min} \ge 0$. The server may wait before and after it reads its clock; both waits fall inside the round trip. There are no faults: the server tells the truth and messages arrive. So the timing model is the [asynchronous model](/asynchronous-model/) for messages, with the extra assumptions of a minimum delay and of clocks with bounded drift.

**Goal.** P must compute an estimate $E$ of the server clock at the moment it receives the reply, together with a bound $e$ such that $|E - S(t)| \le e$. P wants $e \le U - d_{\min}$ for a target $U$ that it chooses. This is external synchronization of one client; see [clock synchronization](/clock-synchronization/).

## The algorithm

```pseudo id=main
CRISTIAN-READ(S, ρ, dmin)                  ▷ one attempt
L1  T0 ← C(), send REQUEST to S
L2  wait for ⟨T⟩ from S, T1 ← C()           ▷ S put its clock reading T in the reply
L3  h ← (T1 − T0) / (2(1 − ρ))
L4  return (T + h, h − dmin)               ▷ the estimate and its error bound

CRISTIAN(S, ρ, dmin, U, k)
L5  for attempt ← 1 to k do
        (E, e) ← CRISTIAN-READ(S, ρ, dmin)
L6      if T1 − T0 ≤ 2U(1 − ρ) then set C to E, return e
    return FAIL
```

The value $T_1 - T_0$ is the round trip time (RTT) on the client clock. When $\rho = 0$, line L3 gives $h = \mathrm{RTT}/2$ and the estimate is the classic $T + \mathrm{RTT}/2$. The factor $1/(1-\rho)$ turns a round trip measured on a slow clock into an upper bound on the real round trip. The test of line L6 accepts a reading with $h \le U$, so its error bound is at most $U - d_{\min}$. The code uses the simpler test $\mathrm{RTT} \le 2U$, which is the same when $\rho = 0$.

The client should read $C$ from a [monotonic clock](/monotonic-clock/) for $T_0$ and $T_1$. To set its clock it can step it, or slew it so that it never runs back.

## Example

The client is 2.5 s behind. At real time 100 it sends a request; its clock reads $T_0 = 97.5$. The request takes 3 ms. The server replies at once with $T = 100.003$. The reply takes 9 ms, so it arrives at real time 100.012, when the client clock reads $T_1 = 97.512$. Take $\rho = 0$ and $d_{\min} = 2$ ms.

| quantity | value |
|---|---|
| RTT $= T_1 - T_0$ | 0.012 s |
| $h$ (line L3) | 0.006 s |
| estimate $T + h$ (line L4) | 100.009 |
| real time at the receipt | 100.012 |
| actual error | $-0.003$ s |
| error bound $h - d_{\min}$ | 0.004 s |

The client moves its clock from 97.512 to 100.009. The actual error, $-3$ ms, is half the difference of the two delays: $(3 - 9)/2 = -3$ ms. The client does not know it, but it knows that the error is within 4 ms.

**Retries.** Let each one-way delay be $d_{\min} = 1$ plus an exponential random time with mean 1, and let $U = 1.5$. An attempt is accepted when the two random parts add up to at most 1, which has probability $1 - 2/e \approx 0.264$. So the client needs about $3.78$ attempts on average, and each accepted reading has an error of at most $1.5 - 1 = 0.5$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Let $\tau$ be the real round trip time. Since the client clock is $\rho$-bounded, $\tau \le \mathrm{RTT}/(1-\rho) = 2h$. The server read $T$ at least $d_{\min}$ after the request left and at least $d_{\min}$ before the reply arrived. So the time between the server reading and the receipt lies in $[d_{\min}, \tau - d_{\min}]$, and the error of the estimate lies in $[h - \tau + d_{\min},\, h - d_{\min}] \subseteq [-(h - d_{\min}),\, h - d_{\min}]$. The bound is tight: when the request takes exactly $d_{\min}$ and the server replies at once, the error is $-(h - d_{\min})$ with $\rho = 0$.

## Complexity

Each attempt sends 2 messages and takes $O(1)$ local work, so $k$ attempts send $2k$ messages. The real time of an attempt is its round trip. If each attempt is accepted with probability $p$, independently of the others, the number of attempts is geometric with mean $1/p$, and the probability that $k$ attempts all fail is $(1-p)^k$. The client stores $O(1)$ values.

## Properties

- **External, one client.** It synchronizes one client with one server. Many clients each run it on their own.
- **Error known to the client.** The client learns a bound for each reading, not only an estimate.
- **No upper bound on delay needed.** Only the minimum delay $d_{\min}$ enters the bound. A slow reading is not wrong; it is only less precise, and the retry rule discards it.
- **No fault tolerance.** One faulty server gives a wrong time to every client.

## Variants and improvements

- **Keep the best of several readings.** Take several readings and keep the one with the smallest RTT. [NTP](/ntp/) keeps the last 8 samples of each server and uses the one with the least delay.
- **Subtract the server time.** If the server reports when it received the request and when it sent the reply, the client can remove the server's time from the RTT. This gives the four timestamps of [NTP](/ntp/).
- **Many servers.** Read several servers, turn each reading into an interval $[E - e, E + e]$, and intersect the intervals with [Marzullo's algorithm](/marzullo-algorithm/) to tolerate faulty servers.
- **Master side.** The [Berkeley algorithm](/berkeley-algorithm/) uses the same round trip estimate, but from a master that reads the clocks of the other machines.

## When to use it

Use it when one client needs the time of one trusted server and must know the error. It fits a local network with short and steady round trips. Over the Internet, with many servers and asymmetric paths, use [NTP](/ntp/). On a local network with hardware timestamps, use [PTP](/precision-time-protocol/).

## Pitfalls

- **Asymmetric delays.** The estimate assumes that the server read its clock in the middle of the round trip. If the request is fast and the reply slow, the error is up to $h - d_{\min}$, and the client cannot detect it.
- **The wall clock for the RTT.** If the client measures $T_0$ and $T_1$ with a clock that a correction can step, the RTT can be wrong or even negative. Use a [monotonic clock](/monotonic-clock/).
- **Dropping the drift term.** Over a long round trip, a client clock with drift $\rho$ undercounts the RTT by up to $\rho\tau$. The factor $1/(1-\rho)$ covers this.
- **Stepping the clock back.** Setting the clock to $E$ can move it back. Programs that use it for durations break. Slew the clock instead.
- **Trusting one server.** A faulty or malicious server can set every client to any time.

## Implementations

## History

Flaviu Cristian published the method in 1989 in the journal Distributed Computing, under the title Probabilistic clock synchronization. He gave the bound in terms of the round trip and the minimum delay, and the rule to retry until a round trip is short enough, so that the client reaches a chosen precision with a probability that grows with the number of attempts.

## References
