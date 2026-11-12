---
tag: WV4M3X
kind: problem
slug: congestion-control
name: Congestion control
aliases:
- network congestion control
area: systems/networking-algorithms
level: intro
summary: Adapt the sending rates of the flows so that they share the link capacity fairly and use it well, without overloading the network.
prereqs: [sliding-window-protocol, reliable-data-transfer]
see_also: [aimd, tcp-reno, tcp-cubic, tcp-vegas, bbr-congestion-control, ecn, flow-control, network-utility-maximization]
sources:
  - paper: doi:10.1145/52324.52356
    title: Van Jacobson, Congestion avoidance and control, ACM SIGCOMM 1988
    locator: pages 314 to 329 (the October 1986 collapse in the introduction, the conservation of packets, slow start and congestion avoidance)
  - url: "https://www.rfc-editor.org/rfc/rfc896"
    title: John Nagle, RFC 896, Congestion Control in IP/TCP Internetworks, 1984
    locator: the section on congestion collapse
  - paper: doi:10.1016/0169-7552(89)90019-6
    title: Dah-Ming Chiu and Raj Jain, Analysis of the increase and decrease algorithms for congestion avoidance in computer networks, Computer Networks and ISDN Systems 17(1), 1989
    locator: pages 1 to 14 (the goals of efficiency, fairness and convergence, and the binary feedback model)
  - url: "https://www.rfc-editor.org/rfc/rfc5681"
    title: Mark Allman, Vern Paxson and Ethan Blanton, RFC 5681, TCP Congestion Control, 2009
    locator: Sections 3.1 and 3.2
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition
    locator: Section 3.6 (principles of congestion control) and Section 3.7 (TCP congestion control)
  - book: isbn:9781107036055
    title: R. Srikant and Lei Ying, Communication Networks, An Optimization, Control and Stochastic Networks Perspective, 2014
    locator: Chapter 2 (network utility maximization and congestion control)
---

Congestion control is the problem of how each sender in a packet network chooses its sending rate, so that the flows use the link capacity well, share it fairly and do not overload a router. It differs from [flow control](/flow-control/), which protects a slow receiver. A sender only sees signals at the edge: lost packets, a longer round-trip time, or marks set by a router. From these signals each sender must find its share. [AIMD](/aimd/), [TCP Reno](/tcp-reno/), [TCP CUBIC](/tcp-cubic/), [TCP Vegas](/tcp-vegas/) and [BBR](/bbr-congestion-control/) are solutions with different signals.

## In plain words

Many cars use one road. If too many drivers enter at the same time, the road jams and fewer cars per hour get through than on a free road. Nobody can see the full road. Each driver only sees what happens to their own trip: a trip takes longer, or a car does not arrive.

A network has the same problem. Each computer sends data through routers that have small waiting rooms. When too much data arrives, the waiting rooms fill, the packets wait longer, and then the routers throw packets away. The senders must slow down when they see these signs, and speed up again when the network is free. The goal is that the network stays busy, the waiting rooms stay small, and each sender gets a fair part.

## Definition

**The model.** A network has a set $L$ of links. Link $l$ has a capacity $c_l$ in packets per second and a buffer of $B_l$ packets. A set $S$ of flows uses it. Flow $s$ follows a fixed route $R_s \subseteq L$, and its round trip without queues takes $d_s$ seconds, the propagation delay. At time $t$, flow $s$ has a window of $w_s(t)$ segments: the number of segments that it may have sent and not yet seen acknowledged. Its rate is about $x_s \approx w_s / T_s$, where $T_s$ is the measured round-trip time. When the total arrival rate at link $l$ is above $c_l$, a queue builds, and $T_s$ grows. When the queue reaches $B_l$, the link drops packets.

**The control.** Each sender changes $w_s$ (or a pacing rate) from the signals it gets on its acknowledgments: a loss, a delay $T_s$ above $d_s$, or an explicit mark ([ECN](/ecn/)). It gets no direct view of the other flows or of the link loads.

**The goals.** Chiu and Jain name four goals for such a control:

- **Efficiency.** The load $\sum_{s : l \in R_s} x_s$ on each bottleneck link is close to $c_l$, so the link does not stay idle.
- **No overload.** The queues stay short, so the delay is close to $d_s$ and the loss rate is low.
- **Fairness.** Flows that share a bottleneck get comparable rates. The exact meaning is a fairness criterion such as [max-min fairness](/max-min-fairness/) or [proportional fairness](/proportional-fairness/).
- **Convergence.** From any start, the rates go to the fair and efficient point, and they stay near it with small oscillations.

The static form of the goal, with a utility for each flow, is [network utility maximization](/network-utility-maximization/). Congestion control is the dynamic, distributed problem: the senders must reach that point with only local signals, and they must follow it when flows arrive and leave.

**Congestion collapse.** Without control, the useful throughput can fall as the offered load grows. Nagle described this in RFC 896 in 1984. When the queues grow, the round trips get longer than the senders' retransmission timers. The senders then resend packets that are not lost, and the copies use more of the capacity. The network can reach a stable state in which most packets on a link are copies. Jacobson reports that in October 1986 the throughput from LBL to UC Berkeley fell from 32 Kbps to 40 bps, a factor of about 800.

## Variants

- **By the signal.** *Loss-based* controls react to lost packets: [TCP Tahoe](/tcp-tahoe/), [TCP Reno](/tcp-reno/) and [TCP CUBIC](/tcp-cubic/). They fill the buffer until it overflows. *Delay-based* controls react to a growing round-trip time: [TCP Vegas](/tcp-vegas/). They keep a small queue but lose against loss-based flows on the same link. *Model-based* controls estimate the bottleneck rate and the propagation delay, and pace at that rate: [BBR](/bbr-congestion-control/).
- **By who decides.** In *end-to-end* control the network only drops or delays packets, and the senders infer the state. In *network-assisted* control the routers send an explicit signal: a mark in the packet header ([ECN](/ecn/)), set by an [active queue management](/active-queue-management/) scheme such as [RED](/red-random-early-detection/), [CoDel](/codel/) or [PIE](/pie-aqm/), or an explicit rate.
- **Window or rate.** A window control limits the data in flight and is self-clocked by the acknowledgments. A rate control paces the packets at a set rate.
- **Hop by hop.** Link-level flow control, such as credits or pause frames between two neighbors, stops a sender on one link. It is a different mechanism with its own problem of [backpressure](/backpressure/) and is not end-to-end congestion control.

## Examples

**One link and one flow.** A link of 100 Mbit/s carries packets of 1500 bytes, so $c = 8333.3$ packets per second. The propagation delay is $d = 40$ ms, so the bandwidth-delay product is $c\,d = 333.3$ packets. In a fluid model with a large buffer, a window of $w$ packets gives the rate $\min(w/d, c)$ and the round trip $\max(d, w/c)$:

| window $w$ (packets) | rate (Mbit/s) | round trip (ms) | queue (packets) |
|---|---|---|---|
| 100 | 30.0 | 40.0 | 0 |
| 200 | 60.0 | 40.0 | 0 |
| 333 | 99.9 | 40.0 | 0 |
| 400 | 100.0 | 48.0 | 66.7 |
| 500 | 100.0 | 60.0 | 166.7 |
| 1000 | 100.0 | 120.0 | 666.7 |

Below the bandwidth-delay product, a larger window gives more rate at the same delay. Above it, the extra data only waits in the queue. Kleinrock's operating point is $w = c\,d$: the rate is the largest and the delay the smallest. A loss-based control drives the window up to $c\,d + B$, the point where the buffer overflows. A delay-based or model-based control tries to stay near $c\,d$.

**Rate against loss.** For Reno, the throughput formula of Mathis et al. gives about $\sqrt{3/2} / \sqrt{p}$ segments per round trip at loss rate $p$. With segments of 1460 bytes and a round trip of 40 ms, $p = 10^{-2}$ gives 12.2 segments per round trip, or 3.6 Mbit/s, and $p = 10^{-6}$ gives 1224.7 segments per round trip, or 357.6 Mbit/s. A loss-based control needs a very low loss rate to fill a fast link.

**Two flows.** Two flows share one link. [AIMD](/aimd/) moves the rates $(1, 7)$ on a link of capacity 10 toward the equal share: each cut by one half also halves the difference of the two rates. The [AIMD](/aimd/) page has the full trace.

## Known algorithms

| algorithm | signal | increase | decrease |
|---|---|---|---|
| [AIMD](/aimd/) (Chiu and Jain 1989) | binary feedback | $+a$ per step | $\times b$ |
| [slow start](/slow-start/) (Jacobson 1988) | loss | double per round trip | to the threshold |
| [TCP Tahoe](/tcp-tahoe/) (1988) | loss, three duplicate ACKs | slow start, then $+1$ per round trip | window to 1 segment |
| [TCP Reno](/tcp-reno/) (1990) | loss, with [fast recovery](/fast-retransmit-fast-recovery/) | $+1$ per round trip | window to one half |
| [TCP Vegas](/tcp-vegas/) (1994) | delay | $+1$ if the queue is short | $-1$ if the queue is long |
| [TCP CUBIC](/tcp-cubic/) (2008) | loss | a cubic function of time | $\times 0.7$ |
| [BBR](/bbr-congestion-control/) (2016) | delivery rate and minimum RTT | pacing at the estimated rate | no reaction to a single loss |
| [ECN](/ecn/) with [AQM](/active-queue-management/) | router marks | as the sender's control | as on a loss, without the loss |

## Bounds

- **Convergence of AIMD.** In the synchronous binary feedback model of Chiu and Jain, additive increase with multiplicative decrease converges to the fair and efficient point, and it is the only linear control that does. The [AIMD](/aimd/) page has the theorem and its conditions.
- **Throughput of Reno.** With random losses at rate $p$ and a round trip $T$, the rate of Reno is about $\frac{\text{MSS}}{T} \sqrt{3/(2p)}$ (Mathis, Semke, Mahdavi and Ott 1997). The rate falls as $1/T$, so flows with a long round trip get less on a shared link. This is the RTT unfairness of Reno.
- **Stability.** In the fluid models of Kelly, Maulloo and Tan, a primal or a dual congestion controller converges to the optimum of a [network utility maximization](/network-utility-maximization/) problem when the delays are ignored. With delays, stability needs conditions on the gains.
- **No guarantee for the heuristics.** CUBIC and BBR have no proved worst-case bound on fairness or delay in a general network. Their properties come from models and from measurements.

## Reductions

- **To network utility maximization.** A congestion controller is a distributed algorithm for a [network utility maximization](/network-utility-maximization/) problem. The link signal (loss, delay or marks) acts as a price. Low, Peterson and Wang show that Vegas solves a weighted [proportional fairness](/proportional-fairness/) problem, with the queueing delay as the price.
- **From reliable transfer.** Congestion control runs inside a [sliding window protocol](/sliding-window-protocol/) for [reliable data transfer](/reliable-data-transfer/). The sender may have at most $\min(\text{cwnd}, \text{rwnd})$ unacknowledged data, where the congestion window cwnd comes from congestion control and the receiver window rwnd from flow control. The retransmission timer comes from [round-trip time estimation](/round-trip-time-estimation/).

## Applications

- TCP in every operating system. Linux uses CUBIC by default and also has BBR. RFC 5681 is the standard for the base TCP algorithms.
- QUIC, whose loss detection and congestion control in RFC 9002 follow NewReno.
- Data center transports, such as DCTCP, that use ECN marks to keep the queues very short.
- Video streaming and real-time media, which need a low delay more than a high rate.

## References
