---
tag: YCTSW0
kind: algorithm
slug: berkeley-algorithm
name: Berkeley algorithm
aliases:
- Berkeley clock synchronization
area: distributed/clocks-and-ordering
level: core
summary: A master polls the clocks of all machines, estimates each difference from the round trip, averages the differences that agree within a bound, and sends each machine its own adjustment.
solves: [clock-synchronization]
model: asynchronous-model
complexity:
  vars: {n: the number of machines}
  time: {worst: O(n log n)}
  space: {extra: O(n)}
  messages: {worst: 3(n − 1)}
properties: {deterministic: true, recursive: false}
history:
  year: 1989
  people: [Riccardo Gusella, Stefano Zatti]
  note: Gusella and Zatti described TEMPO, the time service of Berkeley UNIX 4.3BSD, and its accuracy in IEEE Transactions on Software Engineering in 1989.
prereqs: [cristian-algorithm]
see_also: [cristian-algorithm, clock-synchronization, clock-skew, ntp, marzullo-algorithm, approximate-agreement, median]
sources:
  - paper: doi:10.1109/32.29484
    title: Riccardo Gusella and Stefano Zatti, The accuracy of the clock synchronization achieved by TEMPO in Berkeley UNIX 4.3BSD, IEEE Transactions on Software Engineering 15(7), 1989
    locator: pages 847 to 853
  - book: isbn:9780132143011
    title: George Coulouris, Jean Dollimore, Tim Kindberg and Gordon Blair, Distributed Systems, Concepts and Design, fifth edition, Addison-Wesley, 2012
    locator: Chapter 14, Section 14.3 (the Berkeley algorithm and the fault-tolerant average)
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 3 (physical clock synchronization)
---

The *Berkeley algorithm* is an internal [clock synchronization](/clock-synchronization/) method in which one master machine polls the clocks of all the others. It estimates the difference of each clock from its own with the round trip rule of [Cristian's algorithm](/cristian-algorithm/), averages the differences that agree with each other within a bound $\gamma$, and sends each machine the adjustment that moves it to the average. Gusella and Zatti built it as TEMPO, the time service of Berkeley UNIX 4.3BSD. It makes the clocks agree with each other, not with an external standard.

## In plain words

One computer acts as the master. It asks every other computer what time its clock shows, and it uses the time of each round trip to correct for the delay, as in Cristian's method. Now it knows roughly how far each clock is ahead of or behind its own.

The master then throws away clocks that are far away from the rest, because they are probably broken. It takes the average of the remaining ones, its own clock included. Then it tells each computer by how much to move its clock, for example "go forward 15 milliseconds". It sends a change, not a time, so the delay of this last message does not matter.

## The problem

**Model.** There are $n$ machines, numbered $0$ to $n-1$; machine 0 is the master. Machine $i$ has a clock $H_i(t) = t + c_i$ with an unknown offset $c_i$. The round is short, so drift is left out here (see [clock drift](/clock-drift/) for its effect between rounds). Messages are reliable, and each one-way delay is at least $d_{\min}$; there is no upper bound. Some clocks may be faulty, which here means that they show a value far away from the others.

**Goal.** After the round, the [skew](/clock-skew/) $|C_i - C_j|$ of any two adjusted clocks should be small, and a few faulty clocks should not move the common time much. This is internal synchronization: no machine knows the real time.

## The algorithm

```pseudo id=main
BERKELEY-ROUND(γ)                             ▷ run by the master, machine 0
L1  for each slave i: S_i ← C_0(), send REQUEST to i
L2  on reply ⟨T_i⟩ from i: RTT_i ← C_0() − S_i
        Δ_i ← T_i + RTT_i / 2 − C_0()          ▷ estimate of C_i − C_0
L3  Δ_0 ← 0
L4  G ← a largest set of machines with max_{i∈G} Δ_i − min_{i∈G} Δ_i ≤ γ
L5  a ← (1 / |G|) · Σ_{i∈G} Δ_i                ▷ the fault-tolerant average
L6  for each machine i: send ADJUST(a − Δ_i) to i  ▷ also to the machines outside G
```

A slave answers a REQUEST with its clock reading. On ADJUST$(x)$ a machine moves its clock by $x$, by slewing when $x < 0$ so that the clock never runs back. Line L4 sorts the $n$ values $\Delta_i$ and slides a window over them: for each right end it keeps the leftmost left end with a spread of at most $\gamma$. Ties go to the smaller spread, then to the leftmost window.

## Example

Five machines have offsets $0, 25, -10, 5, 600$ ms from the master; machine 4 is broken. All delays are equal in both directions, so every estimate is exact: $\Delta = (0, 25, -10, 5, 600)$. Let $\gamma = 60$ ms.

| step | result |
|---|---|
| sorted values | $-10, 0, 5, 25, 600$ |
| largest window with spread $\le 60$ | $\{-10, 0, 5, 25\}$, machines 2, 0, 3, 1 |
| average $a$ (line L5) | $(0 + 25 - 10 + 5)/4 = 5$ |
| adjustments $a - \Delta_i$ (line L6) | $5, -20, 15, 0, -595$ |
| new offsets | $5, 5, 5, 5, 5$ |

After the round every clock shows the same time, 5 ms ahead of the old master clock. Machine 4 did not move the average, but it still receives an adjustment and joins the others. A plain average of all five values would be $124$ ms: one bad clock would move every good clock by more than 100 ms.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Let $e_i = \Delta_i - (c_i - c_0)$ be the error of the estimate of machine $i$, with $e_0 = 0$. By the bound of [Cristian's algorithm](/cristian-algorithm/), $|e_i| \le \mathrm{RTT}_i/2 - d_{\min}$. After the adjustment, machine $i$ has offset $c_i + a - \Delta_i = c_0 + a - e_i$. So for any two machines,
$$|C_i - C_j| = |e_i - e_j| \le |e_i| + |e_j|,$$
for every machine, also for the ones outside $G$. The value of $a$ does not enter the skew at all; it only sets the common time. The fault-tolerant average keeps that common time near the good clocks: if more than half of the machines are good and the estimates of the good ones lie in an interval of length $\gamma$, then $a$ lies within $\gamma$ of that interval.

## Complexity

One round sends $n - 1$ requests, $n - 1$ replies and $n - 1$ adjustments, so $3(n-1)$ messages. The master does $O(n \log n)$ work for the sort in line L4 and $O(n)$ for the rest, and stores $O(n)$ values. The real time of a round is the longest round trip plus the delivery of the adjustments.

## Properties

- **Internal only.** The common time is the average of the machines, not UTC. Gusella and Zatti suggest that the master may itself follow an external source, but the algorithm does not need one.
- **Adjustments, not times.** A relative change stays correct however long the ADJUST message takes, as long as the clocks do not drift much in that time.
- **Tolerant of a minority of wild clocks.** A clock far from the others is left out of the average. It still gets corrected.
- **A single master.** If the master fails, the machines must elect a new one. TEMPO includes an election for this.

## Variants and improvements

- **Rejecting large round trips.** The master can discard replies with a large RTT, since their estimates are less precise, and repeat the request.
- **Median instead of average.** The [median](/median/) of the values is another robust choice; it ignores up to half of the values minus one without any $\gamma$.
- **Fault-tolerant averaging in general.** Dropping the $f$ largest and the $f$ smallest values and averaging the rest is the rule of many Byzantine clock synchronization algorithms and of [approximate agreement](/approximate-agreement/).
- **Interval intersection.** [Marzullo's algorithm](/marzullo-algorithm/) uses error bounds instead of a fixed $\gamma$, and [NTP](/ntp/) builds on it.

## When to use it

Use it on a local network of machines that must agree with each other when no machine has a good time source, or when one machine acts as the reference for the rest. When an accurate external time matters, use [NTP](/ntp/) or [PTP](/precision-time-protocol/).

## Pitfalls

- **Choosing $\gamma$.** If $\gamma$ is smaller than the normal spread of good clocks plus the estimate errors, the largest set may be small, and the average is noisy. If it is too large, broken clocks enter the average.
- **Many broken clocks that agree.** If more than half of the machines are broken in the same way, the largest set is the broken one, and every clock follows them.
- **Stepping back.** A negative adjustment applied as a step can make a clock run back. Slew it.
- **Including the outliers in the average.** The plain average of all clocks lets one bad clock move all the others.

## Implementations

## History

Riccardo Gusella and Stefano Zatti designed TEMPO for Berkeley UNIX 4.3BSD, where it runs as the daemon timed. An earlier version of their analysis appeared as a Berkeley technical report. Their 1989 paper in IEEE Transactions on Software Engineering shows that the accuracy depends on the network latency and grows linearly with the drift rate of the clocks and with the time between synchronizations.

## References
