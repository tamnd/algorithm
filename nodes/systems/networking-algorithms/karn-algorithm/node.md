---
tag: ZDWFE6
kind: algorithm
slug: karn-algorithm
name: Karn's algorithm
aliases:
- Karn-Partridge algorithm
area: systems/networking-algorithms
level: advanced
summary: Take no RTT sample from a segment that was sent more than once, and keep the doubled timeout until a segment sent once is acknowledged.
solves: [round-trip-time-estimation]
model: asynchronous-model
complexity:
  vars: {n: the number of segments, w: the number of segments in flight}
  time: {best: Θ(n), worst: Θ(n)}
  space: {extra: Θ(w)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1987
  people: [Phil Karn, Craig Partridge]
  note: Karn found the problem in his TCP/IP code for amateur packet radio. Karn and Partridge published the two rules at SIGCOMM 1987.
prereqs: [round-trip-time-estimation, exponential-backoff]
see_also: [jacobson-rto-estimation, stop-and-wait, go-back-n, selective-repeat, reliable-data-transfer]
sources:
  - paper: doi:10.1145/55483.55484
    title: Phil Karn and Craig Partridge, Improving round-trip time estimates in reliable transport protocols, Proceedings of SIGCOMM 1987, 2-7
    locator: the retransmission ambiguity, the sampling rule and the timer backoff rule
  - paper: doi:10.1145/118544.118549
    title: Phil Karn and Craig Partridge, Improving round-trip time estimates in reliable transport protocols, ACM Transactions on Computer Systems 9(4), 1991, 364-373
    locator: the journal version of the same paper
  - url: https://www.rfc-editor.org/rfc/rfc6298
    title: RFC 6298, Computing TCP's Retransmission Timer, 2011
    locator: Section 3, Taking RTT Samples, and Section 5, rule 5.5
  - url: https://www.rfc-editor.org/rfc/rfc1122
    title: RFC 1122, Requirements for Internet Hosts, Communication Layers, 1989
    locator: Section 4.2.3.1, Retransmission Timeout Calculation
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition
    locator: Section 3.5.3, Round-Trip Time Estimation and Timeout, and Section 3.5.4 (doubling the timeout interval)
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition
    locator: Section 5.2.6, Adaptive Retransmission (the Karn/Partridge algorithm)
---

Karn's algorithm, by Phil Karn and Craig Partridge (1987), fixes two errors in [round-trip time estimation](/round-trip-time-estimation/) for a sender that retransmits. First, it takes no round-trip time (RTT) sample from a segment that was sent more than once, because the sender cannot tell which copy an ACK answers. Second, when the timer expires it doubles the retransmission timeout (RTO), and it keeps the doubled value until a segment that was sent once is acknowledged. TCP uses it together with [Jacobson's RTO estimation](/jacobson-rto-estimation/).

## In plain words

You send a letter, wait, and send it again because no reply came. Then a reply comes. You do not know if it answers the first letter or the second, so you cannot tell how long the post takes. Karn's rule says: do not learn from that reply at all.

But if you never learn, a post that has become slow traps you: each letter times out, each is sent twice, and you never get a clean time. So the second rule says: each time the clock runs out, wait twice as long, and keep that longer wait for the next letters. Soon one letter gets its reply before the clock runs out, and you get a clean time again.

## The problem

A reliable sender measures RTT samples to set its timeout. When a segment is resent and an ACK arrives, the ACK may answer the first copy, which was slow, or a later copy. Measuring from the first copy adds the timeout to the sample when the first copy was lost. Measuring from the last copy gives a much too short sample when the first copy was only slow. Both errors feed on themselves.

## The algorithm

The sender keeps the time when each segment was first sent, a mark for segments that were sent again, and the estimator of [Jacobson's RTO estimation](/jacobson-rto-estimation/).

```pseudo id=main
KARN
L1  on sending segment s for the first time: sent[s] ← now
L2  on sending s again: mark s as retransmitted
L3  on a timeout: RTO ← 2·RTO; resend   ▷ no sample changes this value
L4  on the ACK of segment s:
L5      if s was sent only once then
L6          update SRTT, RTTVAR and RTO with R = now − sent[s]
L7      else take no sample, and keep the backed-off RTO
```

TCP times one segment at a time, and with cumulative ACKs an ACK may cover several segments. RFC 6298, Section 3, states the rule: RTT samples MUST NOT be taken from segments that were retransmitted, unless the TCP timestamps option removes the ambiguity.

## Example

The sender sends one segment at a time. For the first 5 segments the RTT is 0.5 s, and then it jumps to 3.5 s. With the lower bound of 1 s, the RTO after the first 5 segments is 1 s.

| segment | Karn: copies | Karn: sample | Karn: RTO after | last copy: copies | last copy: sample |
|---|---|---|---|---|---|
| 0 to 4 | 1 | 0.5 | 1.5, 1.25, 1.06, 1, 1 | 1 | 0.5 |
| 5 | 3 | none | 4 | 3 | 0.5 |
| 6 | 1 | 3.5 | 4.11 | 3 | 0.5 |
| 7 | 1 | 3.5 | 6.26 | 3 | 0.5 |
| 8 | 1 | 3.5 | 7.58 | 3 | 0.5 |

Segment 5 times out at 1 s and at 3 s, and the RTO becomes 2 and then 4. Its ACK comes at 3.5 s and gives no sample, but the RTO stays 4, so segment 6 is sent once and gives the true sample 3.5. The rule "measure from the last copy" computes $3.5 - 3 = 0.5$ for every segment: its RTO stays 1, and all 15 slow segments are sent three times, 30 retransmissions in total.

The rule "measure from the first copy" works in this trace but fails in another. With a constant RTT of 0.5 s and lost first copies of segments 3 to 8, it takes the samples 1.5625, 2.6172 and 4.4785 s, and so on, and ten segments after the losses its RTO is still 18.8 s. Karn's algorithm takes no sample from these segments, doubles the RTO to 2.125, 4.25, 8.5, 17, 34 and 60 s, and returns to 1 s with the first segment that is sent once.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). A segment that was sent once has one copy, so the first ACK answers that copy, and the sample is exact. The second rule is necessary: if the RTO went back to the value from SRTT for each new segment, a path with an RTT above that value would make every segment time out, so no sample would ever be taken, and the sender would be stuck. With the doubled value kept, after at most $\lceil \log_2 (D/L) \rceil + 1$ timeouts the RTO is above the new RTT $D$, where $L$ is the lower bound; the next segment is sent once and gives the sample $D$. From then on the RTO from [Jacobson's rule](/jacobson-rto-estimation/) is at least $D$, and SRTT converges to $D$.

## Complexity

Each send, ACK and timeout costs $O(1)$ time. The sender keeps the first send time and one bit for each segment in flight. A TCP sender that times one segment at a time needs only one time stamp and one bit.

## Properties

- **Exact samples.** Every sample belongs to a known copy.
- **Fewer samples.** On a lossy path, each retransmitted segment gives no sample. With loss probability $p$ per segment, about a fraction $p$ of the samples is lost.
- **Conservative.** During a run of losses the RTO keeps doubling up to its upper bound, even if the RTT is unchanged.
- **Self-correcting.** One segment that is sent once restores the estimate.

## Variants and improvements

- **Timestamps.** With the TCP timestamps option (RFC 7323), the ACK echoes the time stamp of the copy that it answers, so a sample can be taken also from a retransmitted segment. RFC 6298 allows this.
- **Distinct sequence numbers.** QUIC gives each transmission a new packet number, so an ACK always names one copy and the ambiguity does not arise.
- **Clearing the estimate.** After several backoffs in a row, RFC 6298 allows the sender to clear SRTT and RTTVAR, because they are probably wrong, and to start again with the next sample as a first sample.

## When to use it

Use it in every sender that retransmits on a timeout and estimates the RTT from the ACKs, unless each ACK can name the copy that it answers. It is required for TCP hosts by RFC 1122.

## Pitfalls

- **Rule 1 without rule 2.** Ignoring retransmitted samples but resetting the RTO for each segment stops all sampling after a delay jump.
- **Forgetting the mark on a go-back.** In [Go-Back-N](/go-back-n/), a timeout resends a whole window; each of these segments is then retransmitted.

## Implementations

## History

Phil Karn found the problem in 1987 while he ran his KA9Q TCP/IP code over amateur packet radio, where losses and long delays are common. With Craig Partridge he published the two rules at SIGCOMM 1987, and the paper appeared again in ACM Transactions on Computer Systems in 1991. RFC 1122 (1989) requires Karn's algorithm for TCP hosts, and RFC 2988 and RFC 6298 state it in Section 3 next to Jacobson's estimator.

## References
