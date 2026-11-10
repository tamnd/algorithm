---
tag: RCAZGT
kind: problem
slug: clock-synchronization
name: Clock synchronization
aliases:
- time synchronization
- clock sync
area: distributed/clocks-and-ordering
level: core
summary: Keep the clocks of n processes close to each other (internal) or to a time standard (external), in spite of drift and of message delays that are known only within bounds.
prereqs: [clock-skew, clock-drift]
see_also: [cristian-algorithm, berkeley-algorithm, ntp, precision-time-protocol, marzullo-algorithm, clock-synchronization-lower-bound, truetime, synchronizer]
sources:
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 6 (clock synchronization without faults and the lower bound) and Chapter 13 (fault-tolerant clock synchronization)
  - book: isbn:9780132143011
    title: George Coulouris, Jean Dollimore, Tim Kindberg and Gordon Blair, Distributed Systems, Concepts and Design, fifth edition, Addison-Wesley, 2012
    locator: Chapter 14, Section 14.3 (Cristian's method, the Berkeley algorithm and NTP)
  - paper: doi:10.1016/S0019-9958(84)80033-9
    title: Jennifer Lundelius and Nancy Lynch, An upper and lower bound for clock synchronization, Information and Control 62(2-3), 1984
    locator: pages 190 to 204
  - paper: doi:10.1145/28869.28876
    title: T. K. Srikanth and Sam Toueg, Optimal clock synchronization, Journal of the ACM 34(3), 1987
    locator: the whole paper (DOI to be checked)
  - paper: doi:10.1016/0022-0000(86)90028-0
    title: Danny Dolev, Joseph Y. Halpern and H. Raymond Strong, On the possibility and impossibility of achieving clock synchronization, Journal of Computer and System Sciences 32(2), 1986
    locator: the whole paper (DOI to be checked)
---

*Clock synchronization* is the problem of keeping the clocks of $n$ processes close to each other (*internal* synchronization) or close to a time standard such as UTC (*external* synchronization). Two things make it hard: each hardware clock has [drift](/clock-drift/), and a message delay is known only within bounds, so a process can never learn another clock value exactly. The goal is a bound on the [skew](/clock-skew/) that holds at all times, with resynchronization at regular intervals.

## In plain words

Each computer has a clock that runs a little fast or a little slow. Left alone, the clocks of a network move apart. The computers can send each other their clock readings, but a message takes some time to arrive, and the receiver does not know exactly how long. So when a reading arrives, it is already old, and the receiver can only guess by how much.

Clock synchronization asks the computers to correct their clocks so that any two of them stay within a small bound of each other, or within a small bound of an exact time source. They must do it again and again, because the clocks keep moving apart. Some versions also ask that it work when some computers crash or lie.

## Definition

**Model.** There are $n$ processes. Real time $t$ is not visible to them. Process $i$ has a hardware clock $H_i$ with drift bound $\rho$ (see [clock drift](/clock-drift/)). It computes an adjusted clock $C_i(t) = H_i(t) + \mathrm{adj}_i(t)$, where the algorithm sets $\mathrm{adj}_i$. Processes talk by messages over reliable channels. The delay of each message lies in a known interval $[d - u, d]$; in some variants only a lower bound $d_{\min}$ is known and the delay has no upper bound. Up to $f$ processes may be faulty; the variant says crash or Byzantine.

**Internal synchronization with precision $\pi$.** From some time $t_0$ on, for all nonfaulty $i, j$:
$$|C_i(t) - C_j(t)| \le \pi.$$

**External synchronization with accuracy $\alpha$.** One process (or a set of time servers) can read a reference time $S(t)$. From some time $t_0$ on, for every nonfaulty $i$:
$$|C_i(t) - S(t)| \le \alpha.$$

**A rate condition.** Internal synchronization alone has a trivial solution: every process sets $C_i(t) = 0$ forever. So the problem also asks that the adjusted clocks keep a rate close to real time. A common form is that there are constants $a > 0$ and $b$ with $a(t-s) - b \le C_i(t) - C_i(s)$ for all $s \le t$. Srikanth and Toueg (1987) call the best possible form of this condition *optimal accuracy*. Some systems also ask that $C_i$ never decreases (see [monotonic clock](/monotonic-clock/)).

**The one-shot version.** Lundelius and Lynch study one round: drift-free clocks ($\rho = 0$), no faults, and the goal is the smallest skew $\varepsilon$ of the adjusted clocks after the round, for every admissible execution.

The symbols follow the notation of this area: $n$ processes, $f$ faulty ones, $\rho$ the drift bound, $d$ and $u$ the delay bound and its uncertainty.

## Variants

- **Internal or external.** Internal synchronization needs no reference. External synchronization implies internal synchronization with $\pi = 2\alpha$ (proved on [clock skew](/clock-skew/)).
- **Deterministic or probabilistic.** With a known delay interval, an algorithm can guarantee a bound. With only a lower bound on the delay, [Cristian's algorithm](/cristian-algorithm/) gives a bound for each reading that it accepts, and retries until a reading is good enough, so the bound holds only with some probability within a given number of tries.
- **Fault-tolerant.** With Byzantine processes and no authentication, clock synchronization needs $n > 3f$ (Dolev, Halpern and Strong 1986). Srikanth and Toueg (1987) give algorithms with optimal accuracy for $n > 3f$, and with authentication for $n > 2f$. These results are cited here and not proved.
- **Hierarchical.** [NTP](/ntp/) arranges servers in strata below reference clocks, and each client picks among several servers with an interval intersection in the style of [Marzullo's algorithm](/marzullo-algorithm/).
- **With hardware support.** [PTP](/precision-time-protocol/) takes timestamps in the network hardware and corrects for the time a packet spends in each switch, which removes most of the delay uncertainty on a local network.
- **Exposing the uncertainty.** [TrueTime](/truetime/) does not claim a single time. It returns an interval that holds the real time, and the program waits out the uncertainty when it needs a real-time order.

## Examples

- **One round of averaging.** Let $n = 3$, $d = 10$, $u = 4$, with drift-free clocks offset from real time by $0$, $2$ and $-1$. Each process sends its reading to the others; the delays (rows are senders) are $[\cdot, 8, 9]$, $[10, \cdot, 6]$, $[7, 10, \cdot]$. Each process estimates each other clock with the midpoint delay $d - u/2 = 8$ and moves to the average of the estimates and its own clock. The adjusted offsets are $0$, $-1/3$ and $2/3$, so the skew is 1, below the bound $(1 - 1/3) \cdot 4 = 8/3$ of the [lower bound page](/clock-synchronization-lower-bound/).
- **External synchronization from a server.** A client with [Cristian's algorithm](/cristian-algorithm/) measures a round trip of 12 ms to a server with a known minimum one-way delay of 2 ms. It sets its clock to the server time plus 6 ms and knows that its error is at most $6 - 2 = 4$ ms.
- **Precision from a period.** With an error of 1 ms after each round, $\rho = 15$ ppm and rounds every 64 s, the precision is $1 + 1.92 = 2.92$ ms (see [clock skew](/clock-skew/)).

## Known algorithms

| Algorithm | Kind | Model | Guarantee |
|---|---|---|---|
| [Cristian's algorithm](/cristian-algorithm/) (1989) | external, client and server | lower bound on delay only | error at most RTT/2 minus the minimum delay, per accepted reading |
| [Berkeley algorithm](/berkeley-algorithm/) (Gusella and Zatti 1989) | internal, master polls | delays measured by round trip | fault-tolerant average, outliers excluded |
| Averaging of Lundelius and Lynch (1984) | internal, one round | drift-free, delays in $[d-u, d]$, no faults | skew at most $(1 - 1/n)u$, which is optimal |
| Srikanth and Toueg (1987) | internal, continuous | Byzantine, $n > 3f$ (or $n > 2f$ signed) | optimal accuracy (cited) |
| [Marzullo's algorithm](/marzullo-algorithm/) (1984) | a subroutine | intervals from sources | the region that the most sources agree on |
| [NTP](/ntp/) (Mills; RFC 5905) | external, hierarchical | Internet, asymmetric paths | offset error at most half the round trip delay per sample |
| [PTP](/precision-time-protocol/) (IEEE 1588) | external, master and slaves | local network with hardware timestamps | offset exact when paths are symmetric |
| [TrueTime](/truetime/) (Corbett et al. 2012) | external, with an interval | GPS and atomic clock masters | real time lies in the returned interval |

## Bounds

- **Lower bound.** With $n$ drift-free clocks, delays in $[d - u, d]$ and no faults, no algorithm can guarantee a skew below $(1 - 1/n)u$, and the averaging algorithm reaches this bound (Lundelius and Lynch 1984). Both halves are proved on the [lower bound page](/clock-synchronization-lower-bound/).
- **Error of one reading.** With a round trip time $T$ and a minimum one-way delay $d_{\min}$, a client can know a server clock only within $T/2 - d_{\min}$ (proved on [Cristian's algorithm](/cristian-algorithm/)). NTP's $\delta/2$ bound is the case $d_{\min} = 0$ (proved on [NTP](/ntp/)).
- **Drift between rounds.** Skew grows by at most $2\rho$ per second between rounds (proved on [clock drift](/clock-drift/)).
- **Faults.** $n > 3f$ is necessary without authentication (Dolev, Halpern and Strong 1986); cited only.

## Reductions

- **External to internal.** Any algorithm with accuracy $\alpha$ gives precision $2\alpha$.
- **Synchronized clocks give lock-step rounds.** Assume drift-free adjusted clocks with precision $\pi$ and message delays at most $d$. Let each process start round $r$ when its clock reads $rP$, with $P \ge d + \pi$. The real times at which two processes start round $r$ differ by at most $\pi$. A message sent at the start of round $r$ arrives at most $d$ later, so before the receiver starts round $r+1$. This simulates the [synchronous model](/synchronous-model/). With drift, $P$ must grow by a term of order $\rho P$. A [synchronizer](/synchronizer/) gives rounds without clocks, at the cost of extra messages.

## Applications

- Ordering of log records from many machines, and timeouts across machines.
- Leases and leader leases, where a lease holder and the other processes must agree on when the lease ends.
- Spanner and other databases that use real time to order transactions ([external consistency](/external-consistency/)).
- Measurement and control systems, telecom and power grid equipment, where [PTP](/precision-time-protocol/) gives sub-microsecond agreement on a local network.

## References
