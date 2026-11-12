---
tag: V6R8C9
kind: problem
slug: round-trip-time-estimation
name: Round-trip time estimation
aliases:
- RTO estimation
area: systems/networking-algorithms
level: core
summary: From measured round-trip times, choose a retransmission timeout that is rarely shorter than the next round trip and not much longer, as the delay changes.
prereqs: [exponential-moving-average, reliable-data-transfer]
see_also: [stop-and-wait, go-back-n, selective-repeat, exponential-backoff, failure-detector, phi-accrual-failure-detector, peak-ewma, congestion-control]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc793
    title: RFC 793, Transmission Control Protocol, 1981
    locator: Section 3.7, Data Communication, Retransmission Timeout (SRTT, ALPHA, BETA, UBOUND and LBOUND)
  - url: https://www.rfc-editor.org/rfc/rfc6298
    title: RFC 6298, Computing TCP's Retransmission Timer, 2011
    locator: Sections 2, 3 and 5
  - url: https://www.rfc-editor.org/rfc/rfc7323
    title: RFC 7323, TCP Extensions for High Performance, 2014
    locator: Section 4, The RTTM Mechanism, and Appendix G (RTO calculation with many samples per round trip)
  - paper: doi:10.1145/52324.52356
    title: Van Jacobson, Congestion avoidance and control, Proceedings of SIGCOMM 1988, 314-329
    locator: Section 2, Round-trip timing
  - paper: doi:10.1145/55483.55484
    title: Phil Karn and Craig Partridge, Improving round-trip time estimates in reliable transport protocols, Proceedings of SIGCOMM 1987, 2-7
    locator: the retransmission ambiguity problem
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition
    locator: Section 3.5.3, Round-Trip Time Estimation and Timeout
  - book: isbn:9780132126953
    title: Andrew S. Tanenbaum and David J. Wetherall, Computer Networks, fifth edition
    locator: Section 6.5.9, TCP Timer Management
---

Round-trip time estimation is the problem of setting the retransmission timeout (RTO) of a [reliable data transfer](/reliable-data-transfer/) protocol from measured round-trip times (RTTs). A timeout that is too short sends packets again that were not lost, which wastes the link and, in TCP, also cuts the sending rate. A timeout that is too long leaves a lost packet unrepaired for a long time. The delay of a path changes with the load, so the estimate must follow it online. The standard solution in TCP is [Jacobson's RTO estimation](/jacobson-rto-estimation/) with [Karn's algorithm](/karn-algorithm/).

## In plain words

You send a packet and wait for its confirmation. How long should you wait before you decide that it was lost? You can measure how long the earlier confirmations took. But the times change: a busy network is slower, and some confirmations come late for no clear reason.

So you keep a running average of the measured times and some measure of how much they vary. You wait for a bit more than the usual time, and much more when the times vary a lot. You also take care to measure only clean cases, where you know which packet the confirmation answers.

## Definition

A sender gets RTT samples $R_1, R_2, \ldots$ over time; sample $R_i$ is the time from sending a segment to receiving its acknowledgement. Before each transmission, it must choose a timeout $\mathrm{RTO}$, using only the samples so far. Let $D$ be the round trip of the segment that is sent. The outcomes are:

- **spurious timeout**: $\mathrm{RTO} < D$; the segment is sent again for nothing;
- **slow recovery**: the segment is lost, and the sender waits $\mathrm{RTO}$ before it resends; it would like $\mathrm{RTO}$ to be close to $D$.

An estimator is good if spurious timeouts are rare, and $\mathrm{RTO} - D$ is small. It must use $O(1)$ time and memory per sample, and it must handle samples that are ambiguous: after a retransmission, the sender does not know which copy an ACK answers.

## Variants

- **One sample per round trip or per segment.** Classic TCP times one segment at a time. With the timestamps option (RFC 7323), every ACK gives a sample.
- **Coarse clocks.** Old BSD stacks used a tick of 500 ms, so the estimator must keep a margin of one tick.
- **Timeouts for requests.** RPC systems and service clients set request timeouts from measured latencies, often from a high percentile.
- **Failure detection.** A [failure detector](/failure-detector/) suspects a process when a heartbeat is late; the [phi accrual failure detector](/phi-accrual-failure-detector/) fits a distribution to the gaps between heartbeats.

## Examples

**The earlier TCP rule.** RFC 793 (Section 3.7) uses

$$\mathrm{SRTT} \leftarrow \alpha\,\mathrm{SRTT} + (1 - \alpha) R, \qquad \mathrm{RTO} = \min(\mathrm{UBOUND}, \max(\mathrm{LBOUND}, \beta\,\mathrm{SRTT})),$$

with $\alpha$ from 0.8 to 0.9, $\beta$ from 1.3 to 2.0, and bounds such as LBOUND = 1 s and UBOUND = 1 min.

**A trace with spikes.** Take the RTT samples 0.1, 0.1, 0.1, 0.1, 0.4 s, repeated 20 times, and call a sample *late* if it is larger than the RTO that was in force before it. The RFC 793 rule with $\alpha = 0.9$, $\beta = 2$ and no lower bound keeps SRTT below 0.174 s, so its RTO stays below 0.35 s, and all 20 spikes are late. [Jacobson's rule](/jacobson-rto-estimation/), $\mathrm{RTO} = \mathrm{SRTT} + 4\,\mathrm{RTTVAR}$, also without a lower bound, is late only for the spikes at the positions 4, 9 and 14: the deviation term learns that the path has spikes.

**An ambiguous sample.** A segment is sent at time 0, times out at 1 s, and is sent again. An ACK comes at 1.2 s. If it answers the first copy, the RTT is 1.2 s; if it answers the second, it is 0.2 s. [Karn's algorithm](/karn-algorithm/) takes no sample from this segment.

## Known algorithms

| algorithm | estimate | handles |
|---|---|---|
| RFC 793 rule | $\beta\,\mathrm{SRTT}$ within LBOUND and UBOUND | a stable mean |
| [Jacobson's RTO estimation](/jacobson-rto-estimation/) | $\mathrm{SRTT} + \max(G, 4\,\mathrm{RTTVAR})$, doubled on a timeout | changing mean and spread |
| [Karn's algorithm](/karn-algorithm/) | no samples from retransmitted segments; keep the backed-off RTO | ambiguous samples |
| TCP timestamps (RFC 7323) | the ACK echoes the send time of the copy | ambiguity, more samples |
| QUIC (RFC 9002) | smoothed RTT and RTT variation as in TCP, plus the minimum RTT and the peer's ACK delay | distinct packet numbers for each copy |

The averages are [exponential moving averages](/exponential-moving-average/). After a timeout, [exponential backoff](/exponential-backoff/) doubles the RTO until a valid sample arrives.

## Bounds

- **No timeout is always safe.** In the [asynchronous model](/asynchronous-model/), delays have no bound, so every finite timeout can be shorter than some round trip. A timeout trades spurious retransmissions against slow recovery.
- **Quantiles.** If the round trips were independent with a known distribution, the best fixed timeout for a target rate $q$ of spurious timeouts would be the $(1-q)$ quantile. Mean plus a multiple of the deviation is a cheap stand-in for a high quantile.
- **Convergence speed.** With the weight $1/8$, the influence of an old sample falls by the factor $7/8$ per new sample, so the estimate needs about $\ln 2 / \ln(8/7) \approx 5.2$ samples to move halfway to a new steady value.

## Reductions

- Timeout setting reduces to online estimation of a high quantile of the RTT.
- Failure detection in distributed systems reduces to the same problem: a process is suspected when its heartbeat is later than the estimated timeout.

## Applications

TCP and SCTP retransmission timers, QUIC loss detection and probe timeouts, request timeouts and hedged requests in RPC frameworks, heartbeat timeouts in cluster managers, and load balancers that pick backends by measured latency, as with [peak EWMA](/peak-ewma/).

## References
