---
tag: QV4H8D
kind: algorithm
slug: precision-time-protocol
name: Precision Time Protocol
aliases:
- PTP
- IEEE 1588
area: distributed/clocks-and-ordering
level: advanced
summary: IEEE 1588. A master sends Sync and Follow_Up, a slave answers with Delay_Req, and four hardware timestamps give the offset and mean path delay. Switches correct for their own delay.
solves: [clock-synchronization]
model: asynchronous-model
complexity:
  vars: {n: the number of slaves of one master}
  time: {worst: O(1)}
  space: {extra: O(1)}
  messages: {worst: 2 + 2n}
properties: {deterministic: true, recursive: false}
history:
  year: 2002
  people: [John C. Eidson]
  note: IEEE 1588 first appeared in 2002, from work led by John Eidson at Agilent. Version 2 (2008) added transparent clocks; the 2019 edition (version 2.1) added optional features.
prereqs: [ntp]
see_also: [ntp, cristian-algorithm, clock-skew, clock-drift, clock-synchronization, truetime, berkeley-algorithm]
sources:
  - paper: doi:10.1109/IEEESTD.2008.4579760
    title: IEEE Std 1588-2008, IEEE Standard for a Precision Clock Synchronization Protocol for Networked Measurement and Control Systems, 2008
    locator: Clause 9.3 (best master clock algorithm), Clause 11.3 (delay request-response mechanism), Clause 11.5 and Clause 6.5 (transparent and boundary clocks)
  - paper: doi:10.1109/IEEESTD.2020.9120376
    title: IEEE Std 1588-2019, IEEE Standard for a Precision Clock Synchronization Protocol for Networked Measurement and Control Systems, 2020
    locator: the revision of 2008 (version 2.1), with the same delay request-response mechanism
  - book: isbn:9780132143011
    title: George Coulouris, Jean Dollimore, Tim Kindberg and Gordon Blair, Distributed Systems, Concepts and Design, fifth edition, Addison-Wesley, 2012
    locator: Chapter 14, Section 14.3 (clock synchronization in a local network)
---

The *Precision Time Protocol* (PTP), standard IEEE 1588, synchronizes the clocks of a local network to within a microsecond or much less. A master sends Sync and Follow_Up messages, a slave sends Delay_Req and gets Delay_Resp, and the four timestamps $t_1, \dots, t_4$ give the offset of the slave from the master and the mean path delay. Its accuracy comes from hardware that takes the timestamps when a packet crosses the wire, and from switches that report how long they held each packet. The arithmetic is the same as in [NTP](/ntp/); the difference is where the timestamps come from and who removes the delays.

## In plain words

A master clock sends a message that says "I sent this at time $t_1$". The slave notes when it got it. Then the slave sends a message back and notes when it left, and the master tells the slave when it arrived. With these four times the slave can compute how far its clock is from the master clock and how long a message takes.

This is the same idea as in NTP. The difference is precision. The network card takes each time at the moment the packet passes, so software delays do not count. Each switch on the way measures how long it held the packet and writes this into the packet, so the slave can take it away. Then only the wire delay is left, which is usually the same in both directions.

## The problem

**Model.** A master and its slaves are on a local network of links and switches. Each node has a clock with [drift](/clock-drift/), and the slave can adjust its clock's phase and rate. The one-way delay of a message is the sum of the link delays and of the time it spends in each switch (its *residence time*). The link delays are steady and often equal in both directions, but the residence times vary with the traffic. Delays have no fixed upper bound, as in the [asynchronous model](/asynchronous-model/).

**Goal.** External synchronization of each slave to the grandmaster, the best clock of the network, with a precision of well below a microsecond, and an automatic choice of that grandmaster.

## The algorithm

```pseudo id=main
PTP-DELAY-REQUEST-RESPONSE                     ▷ slave clock = master clock + o
    master: send Sync; t1 ← the hardware time when it left
    master: send Follow_Up(t1)                  ▷ a two-step clock sends t1 here
    slave: t2 ← the hardware time when Sync arrived
    slave: send Delay_Req; t3 ← the hardware time when it left
    master: t4 ← the hardware time when Delay_Req arrived; send Delay_Resp(t4)
L1  ms ← t2 − t1 − correctionField(Sync)        ▷ master to slave, residence removed
L2  sm ← t4 − t3 − correctionField(Delay_Req)   ▷ slave to master, residence removed
L3  offsetFromMaster ← (ms − sm) / 2;  meanPathDelay ← (ms + sm) / 2
    the slave servo moves its clock by −offsetFromMaster
```

**Two-step and one-step clocks.** A two-step master sends the precise $t_1$ in Follow_Up, because the hardware learns it only when the Sync leaves. A one-step master writes $t_1$ into the Sync message on the fly and sends no Follow_Up.

**Transparent clocks.** A transparent clock is a switch that measures the residence time of each Sync and Delay_Req and adds it to the message's *correctionField*. Lines L1 and L2 subtract these fields, so the queues in the switches do not enter the result. A peer-to-peer transparent clock also adds the delay of the link it received the message on, which it measures with Pdelay_Req and Pdelay_Resp messages to its neighbour.

**Boundary clocks.** A boundary clock is a switch with its own clock. It is a slave on one port, toward the grandmaster, and a master on its other ports. The network is then a tree of master and slave pairs, and each pair runs the exchange above on one hop only.

**The best master clock algorithm (BMCA).** Each master port sends Announce messages with the data set of its grandmaster. Each node compares these data sets field by field, in the order priority1, clockClass, clockAccuracy, offsetScaledLogVariance, priority2 and clockIdentity, where a smaller value wins. The winner becomes the grandmaster, and each port takes the state master, slave or passive. Further ties between paths to the same grandmaster go by the number of hops and the port identities. Because every node uses the same order, all nodes choose the same grandmaster.

## Example

The slave clock is $o = 40$ µs ahead of the master. The Sync takes $a = 3$ µs and the Delay_Req takes $b = 5$ µs; there are no switches.

| quantity | value (µs) | how |
|---|---|---|
| $t_1$ | 1000 | master clock |
| $t_2$ | 1043 | $t_1 + a + o$ on the slave clock |
| $t_3$ | 1100 | slave clock |
| $t_4$ | 1065 | $t_3 + b - o$ on the master clock |
| $ms = t_2 - t_1$ (line L1) | 43 | $a + o$ |
| $sm = t_4 - t_3$ (line L2) | $-35$ | $b - o$ |
| offsetFromMaster (line L3) | 39 | true value 40 |
| meanPathDelay (line L3) | 4 | true value $(3 + 5)/2$ |

The error of the offset is $-1$ µs, which is $(a - b)/2$. With $a = b = 4$ µs the result would be exactly 40.

**BMCA.** A free-running clock with priority1 = 128, clockClass 248 and a GPS-locked clock with priority1 = 128, clockClass 6 meet. The first field is equal, so clockClass decides, and the GPS clock becomes the grandmaster. An operator can force a choice with a smaller priority1, since that field comes first.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Let the slave clock be $o$ ahead of the master clock, let the Sync spend $a$ on links and $r_a$ in switches, and the Delay_Req $b$ and $r_b$. Then $t_2 = t_1 + a + r_a + o$ and $t_4 = t_3 + b + r_b - o$. Transparent clocks report $r_a$ and $r_b$ in the correctionFields, so line L1 gives $ms = a + o$ and line L2 gives $sm = b - o$. Line L3 gives
$$\text{offsetFromMaster} = o + \frac{a - b}{2}, \qquad \text{meanPathDelay} = \frac{a + b}{2}.$$
So the offset is exact when the link delays are equal in the two directions, whatever the queues, and in all cases its error is at most the mean path delay. This is the $\delta/2$ bound of [NTP](/ntp/), with $\delta = a + b$. As in NTP, no rule on these timestamps can do better, because shifting $o$ by $s$ and the delays by $\mp s$ leaves every timestamp the same.

## Complexity

One exchange uses four messages: Sync, Follow_Up, Delay_Req and Delay_Resp. The master sends Sync and Follow_Up once by multicast for all $n$ slaves, and each slave sends its own Delay_Req and gets its own Delay_Resp, so one round costs $2 + 2n$ messages. Each slave does $O(1)$ work and keeps $O(1)$ state per exchange. A boundary clock limits the Delay_Req load on a master to the slaves on its own ports.

## Properties

- **Hardware timestamps.** The time is taken at the physical layer, so the operating system and the protocol stack add no error.
- **Queues removed.** Transparent clocks remove residence times; boundary clocks split the path into single hops.
- **Only link asymmetry is left.** The remaining error is $(a - b)/2$ per hop, which comes from different cable lengths or different transmit and receive delays in the hardware. It can be measured and configured.
- **Self-organizing.** The BMCA picks the grandmaster and the tree without an operator, and picks again when the grandmaster fails.

## Variants and improvements

- **Profiles.** A profile fixes the options of 1588 for one field: the default profiles of the standard, IEEE 802.1AS (gPTP) for audio, video and vehicle networks, ITU-T G.8275.1 for telecom networks, and IEEE C37.238 for power systems.
- **IEEE 1588-2019.** Version 2.1 is compatible with version 2 and adds options, among them a high accuracy profile that comes from the White Rabbit project at CERN and reaches sub-nanosecond accuracy with phase measurement on the link.
- **Peer delay mechanism.** Instead of Delay_Req from each slave to the master, each node measures the delay to its neighbours, which also helps when the topology changes.
- **Software PTP.** Without hardware timestamps PTP still works, but its precision is then close to that of [NTP](/ntp/) on the same network.

## When to use it

Use PTP when the clocks of a local network must agree to within a microsecond or less, as in telecom base stations, power grid measurement, industrial control, audio and video production and financial trading. It needs network cards with timestamping, and switches that are transparent or boundary clocks for the best results. Over the Internet, or when milliseconds are enough, use [NTP](/ntp/).

## Pitfalls

- **Ordinary switches.** A switch that is neither transparent nor boundary adds queueing delays that differ in the two directions, and the error grows with the traffic.
- **Link asymmetry.** Fibres of different length or different transceiver delays give a constant error of $(a-b)/2$ that the protocol cannot see. Calibrate it.
- **Sign conventions.** offsetFromMaster is slave minus master. Applying it with the wrong sign doubles the error instead of removing it.
- **Errors add up along boundary clocks.** In a chain of $k$ boundary clocks, the asymmetry errors of the $k$ hops add up.
- **A bad grandmaster wins.** The BMCA trusts the Announce data. A misconfigured clock with a small priority1 becomes the grandmaster of the whole network.

## Implementations

## History

John C. Eidson of Agilent Technologies led the work that became IEEE 1588-2002, for test and measurement systems. IEEE 1588-2008, known as PTP version 2, was not compatible with version 1; among other changes it added transparent clocks and profiles. IEEE 1588-2019, version 2.1, kept compatibility with version 2 and added optional features, among them the high accuracy profile and security mechanisms.

## References
