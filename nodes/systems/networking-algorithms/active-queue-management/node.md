---
tag: CHK0BQ
kind: concept
slug: active-queue-management
name: Active queue management
aliases:
- AQM
- router queue management
area: systems/networking-algorithms
level: intro
summary: "A router drops or marks packets before its buffer is full, based on the state of the queue, so that senders slow down early and the queueing delay stays small."
prereqs: [congestion-control, queue]
see_also: [red-random-early-detection, codel, pie-aqm, ecn, fair-queueing, packet-scheduling, tcp-reno, aimd]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc7567
    title: Fred Baker and Godred Fairhurst, IETF Recommendations Regarding Active Queue Management, RFC 7567 (BCP 197), 2015
    locator: Section 1 (lock-out, full queues and bufferbloat), Section 2 (the reasons to manage queues) and Section 4 (the recommendations)
  - url: https://www.rfc-editor.org/rfc/rfc2309
    title: Bob Braden et al., Recommendations on Queue Management and Congestion Avoidance in the Internet, RFC 2309, 1998
    locator: Section 2 (the problems of tail drop, lock-out and full queues) and Section 3 (the advantages of active queue management)
  - paper: doi:10.1145/2063166.2071893
    title: Jim Gettys and Kathleen Nichols, Bufferbloat, dark buffers in the Internet, ACM Queue 9(11) (2011)
    locator: pp. 40 to 54 (also Communications of the ACM 55(1), 2012, pp. 57 to 65)
  - paper: doi:10.1109/90.251892
    title: Sally Floyd and Van Jacobson, Random early detection gateways for congestion avoidance, IEEE/ACM Transactions on Networking 1(4) (1993)
    locator: Section 1 and Section 3 (global synchronization and the bias against bursty traffic under drop tail)
  - paper: doi:10.1145/2208917.2209336
    title: Kathleen Nichols and Van Jacobson, Controlling queue delay, ACM Queue 10(5) (2012)
    locator: pp. 20 to 34 (good queue and bad queue, and the standing queue)
  - paper: doi:10.1145/1030194.1015499
    title: Guido Appenzeller, Isaac Keslassy and Nick McKeown, Sizing router buffers, ACM SIGCOMM Computer Communication Review 34(4) (2004)
    locator: pp. 281 to 292 (the rule of a buffer of RTT times C over the square root of n for n long flows)
  - paper: doi:10.1145/205511.205520
    title: Curtis Villamizar and Cheng Song, High performance TCP in ANSNET, ACM SIGCOMM Computer Communication Review 24(5) (1994)
    locator: pp. 45 to 60 (a buffer of one bandwidth-delay product for one TCP flow)
  - url: https://www.rfc-editor.org/rfc/rfc8290
    title: Toke Høiland-Jørgensen, Paul McKenney, Dave Taht, Jim Gettys and Eric Dumazet, The Flow Queue CoDel Packet Scheduler and Active Queue Management Algorithm, RFC 8290, 2018
    locator: Section 1 and Section 4 (a per-flow queue with CoDel on each queue)
  - url: https://www.rfc-editor.org/rfc/rfc8034
    title: Greg White and Rong Pan, Active Queue Management (AQM) Based on Proportional Integral Controller Enhanced (PIE) for Data-Over-Cable Service Interface Specifications (DOCSIS) Cable Modems, RFC 8034, 2017
    locator: Section 1 (PIE in DOCSIS 3.1 cable modems)
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition, Pearson, 2020
    locator: Chapter 4, Section 4.2 (queueing in routers, buffer sizing and buffer management)
---

Active queue management (AQM) is the practice of a router that drops or marks packets before its buffer is full, based on the state of the queue. The plain alternative, drop tail, drops a packet only when there is no room for it. AQM sends an early signal of [congestion](/congestion-control/) to the senders, by a drop or by an [ECN](/ecn/) mark, so that they slow down while the queue is still short. The aim is a small queueing delay and full use of the link at the same time. [RED](/red-random-early-detection/), [CoDel](/codel/) and [PIE](/pie-aqm/) are the main AQM algorithms.

## In plain words

A router keeps a waiting line of packets for each outgoing link. A short line is good: it absorbs a burst and keeps the link busy. A line that stays long is bad: every packet waits in it, and the extra wait does nothing useful.

Senders on the Internet speed up until they lose a packet, and then they slow down. With a plain router, a packet is lost only when the line is completely full. So the senders keep the line nearly full all the time, and every packet waits long.

Active queue management means that the router does not wait for a full line. It watches the line, and when the line stays long, it throws away or flags a few packets on purpose. The senders see the signal and slow down early. The line stays short, the wait stays small, and the link still stays busy.

## The idea

### The model

A router port is a FIFO [queue](/queue/) in front of a link of rate $C$ (bits per second), with a buffer of $B$ bytes. Flows send packets through it. Most flows use a window-based [congestion control](/congestion-control/) such as [TCP Reno](/tcp-reno/), which grows its window until it sees a loss or a mark, and then cuts it ([AIMD](/aimd/)). A packet that finds $b$ bytes in the queue waits $b / C$ seconds. The queue management policy decides, for each packet, whether to enqueue it, drop it or mark it. A [packet scheduler](/packet-scheduling/) is a different policy: it decides which queued packet to send next. The two are often combined, as in FQ-CoDel.

### What goes wrong with drop tail

- **Full queues and bufferbloat.** A loss-based sender fills the buffer before it backs off. So with drop tail, the queue stays near $B$ whenever the link is the bottleneck, and each packet waits about $B/C$. Gettys and Nichols named the large, always-full buffers of home routers and modems *bufferbloat*. Memory is cheap, so buffers grew much faster than the needed size.
- **Lock-out.** With drop tail, one flow or a few flows can take almost all of the buffer space, and other flows lose most of their packets. This often comes from timing effects of the window dynamics, not from the demand of the flows.
- **Global synchronization.** When the buffer overflows, many flows lose a packet in the same short time and all cut their windows at once. The link then goes idle until they grow again, and the cycle repeats.
- **Bias against bursts.** A full queue has no room for a burst, so a bursty flow loses more packets than a smooth flow of the same rate.

### Good queue and bad queue

Nichols and Jacobson separate two kinds of queue. A *good queue* forms when a burst arrives, and drains within about one round-trip time. It is needed to keep the link busy. A *bad queue* is a standing queue: it does not drain, and it only adds delay. A standing queue forms when the sum of the windows is larger than the bandwidth-delay product $C \cdot RTT$. The excess stays in the buffer. An AQM aims to remove the bad queue and keep the good queue.

### The design choices

- **What to measure.** [RED](/red-random-early-detection/) uses an average of the queue length. [CoDel](/codel/) uses the sojourn time of each packet, the time from its arrival to its departure. [PIE](/pie-aqm/) uses an estimate of the queueing delay.
- **How to signal.** A drop works with every sender. An [ECN](/ecn/) mark sets a bit in the IP header and does not lose the packet, but it needs support from both ends. RFC 7567 recommends that an AQM mark the ECN-capable packets in place of a drop.
- **When to signal.** RED signals with a probability that rises with the average queue. CoDel drops at times set by a control law when the delay stays above a target for an interval. PIE drops each packet with a probability that a proportional-integral controller updates.
- **Where the queue is.** One FIFO per port, or one queue per flow behind a [fair queueing](/fair-queueing/) scheduler, where each queue has its own AQM.

The AQM controls the queue, not the rate of the senders. It works only because the senders respond to its signals. A flow that does not respond can still fill the queue; flow isolation by a scheduler handles that case.

## Examples

**The delay of a full buffer.** A home router has a buffer of 1 MB in front of an uplink of 10 Mbit/s. When drop tail keeps the buffer full, each packet waits $8 \cdot 10^6 / 10^7 = 0.8$ s. A buffer of 256 KB on a 1 Mbit/s link gives about 2.05 s. These delays are added to every packet of every flow on the link, including the packets of a voice call.

**A standing queue.** A link of 10 Mbit/s has a base RTT of 50 ms, so the bandwidth-delay product is $62{,}500$ bytes, about 41.7 packets of 1500 bytes. A single flow with a window of 100 packets keeps the link busy and also keeps $100 - 41.7 \approx 58.3$ packets in the queue all the time. That queue adds $58.3 \cdot 1500 \cdot 8 / 10^7 \approx 70$ ms to each packet and gives no extra throughput. An AQM that keeps the sojourn time near 5 ms makes the sender use a window of about 46 packets.

**Buffer sizing.** The classic rule sizes a buffer as $C \cdot RTT$, enough for one TCP flow to keep the link busy after it halves its window (Villamizar and Song, 1994). Appenzeller, Keslassy and McKeown (2004) showed that with $n$ long-lived flows whose windows are not synchronized, a buffer of $C \cdot RTT / \sqrt{n}$ is enough. A buffer of the right size limits the worst delay, but it does not remove a standing queue; that is the work of an AQM.

**A non-example.** A token bucket policer at the edge of a network drops packets that exceed a contracted rate. It looks at the rate of a flow, not at the state of a queue, so it is [traffic policing](/traffic-policing/), not AQM.

## Where it is used

- **Routers and switches.** RED and its weighted forms have been in router software since the 1990s, but operators often left it switched off, because its parameters were hard to set. RFC 7567 (2015) asks that an AQM work well with default parameters.
- **Home gateways and cable modems.** A form of PIE is part of the DOCSIS 3.1 standard for cable modems (RFC 8034). CoDel and FQ-CoDel (RFC 8290) are in Linux and in many home routers.
- **Operating systems.** Linux has the queue disciplines red, codel, fq_codel and pie.
- **Data centers.** Switches mark packets with ECN when the queue passes a threshold, and DCTCP-style senders react to the fraction of marks.
- **Theory.** The pair of a congestion control and an AQM is a feedback system. Fluid models of TCP with RED, and [network utility maximization](/network-utility-maximization/), treat the drop or mark probability as a price that the link sets.

## References
