---
tag: 69ZADN
kind: concept
slug: traffic-policing
name: Traffic policing
aliases:
- rate policing
area: systems/rate-limiting
level: intro
summary: Measure each packet against a traffic profile and act at once. Packets out of profile are dropped or marked. No queue and no delay, but bursts above the profile are lost.
prereqs: [token-bucket]
see_also: [traffic-shaping, token-bucket, gcra, single-rate-three-color-marker, two-rate-three-color-marker, burst-tolerance, active-queue-management, congestion-control]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc2475"
    title: Steven Blake, David L. Black, Mark A. Carlson, Elwyn Davies, Zheng Wang and Walter Weiss, RFC 2475, An Architecture for Differentiated Services, 1998
    locator: Section 1.2 (the terms policing, shaping, traffic profile and traffic conditioner) and Section 2.3.3 (traffic conditioners, meters, markers, shapers and droppers)
  - paper: doi:10.1145/2934872.2934873
    title: Tobias Flach, Pavlos Papageorge, Andreas Terzis, Luis Pedrosa, Yuchung Cheng, Tayeb Karim, Ethan Katz-Bassett and Ramesh Govindan, An Internet-wide analysis of traffic policing, ACM SIGCOMM 2016, pages 468 to 482
    locator: the measurement of policing on 270 billion packets to 28,400 client autonomous systems, the share of policed lossy transfers, the loss rates of policed flows, and pacing and shaping as alternatives
  - url: "https://www.rfc-editor.org/rfc/rfc2212"
    title: Scott Shenker, Craig Partridge and Roch Guerin, RFC 2212, Specification of Guaranteed Quality of Service, 1997
    locator: the section on policing (the bound M+min[pT, rT+b-M], and non-conforming datagrams treated as best effort)
  - book: isbn:9783540421849
    title: Jean-Yves Le Boudec and Patrick Thiran, Network Calculus, A Theory of Deterministic Queuing Systems for the Internet, Springer LNCS 2050, 2001
    locator: Section 1.2.2 (the leaky bucket controller and Proposition 1.2.3) and Section 1.5.1 (policers and shapers)
---

Traffic policing checks each packet or request against a traffic profile, such as a [token bucket](/token-bucket/) with rate $r$ and depth $b$, and acts on it at once. A packet in profile goes on. A packet out of profile is dropped, or marked so that a later stage can drop it first. A policer never holds a packet, so it adds no delay and needs no buffer. The price is that a burst above the profile is lost, not smoothed. The other way to enforce a profile is [traffic shaping](/traffic-shaping/), which delays packets until they fit.

## In plain words

A policer is a guard at a door with a counter. Each person who comes either fits the rule and goes in, or does not fit and is sent away at once. Nobody waits in a line. This is fast and needs no waiting room, but a group that arrives all together loses the people at the back.

The same idea is used for web servers. A server that answers "429 Too Many Requests" to a client over its limit is policing: it refuses the extra requests at once instead of queueing them.

## The idea

**Definitions.** RFC 2475, the Differentiated Services architecture, defines policing as "the process of discarding packets (by a dropper) within a traffic stream in accordance with the state of a corresponding meter enforcing a traffic profile". A traffic profile is "a description of the temporal properties of a traffic stream such as rate and burst size". The traffic conditioner at the edge of a network can contain meters, markers, shapers and droppers. A *meter* measures the stream against the profile, a *marker* sets a code in the packet, a *shaper* delays packets, and a *dropper* discards them. A policer is a meter followed by a dropper or a marker.

**The meter.** The usual meter is a [token bucket](/token-bucket/), or one of its equal forms, the [leaky bucket meter](/leaky-bucket-meter/) and [GCRA](/gcra/). A packet of size $L$ conforms if the bucket holds at least $L$ tokens. This meter is the exact policer for the arrival curve $r\tau + b$: the packets it passes fit the curve, and if the input already fits the curve it passes every packet. Le Boudec and Thiran prove this for the leaky bucket controller (Proposition 1.2.3). So a policer never drops a packet that a conforming source sends; it drops only what is out of profile.

**The action.** The out-of-profile packets can be:

- **Dropped.** The common action at a network edge and in API gateways.
- **Re-marked.** The packet goes on with a lower priority, for example a different DiffServ code point, or in ATM with its cell loss priority bit set. RFC 2212 says "Non-conforming datagrams SHOULD be treated as best-effort datagrams."
- **Colored.** Two buckets give three levels, green, yellow and red, as in the [single-rate three-color marker](/single-rate-three-color-marker/) and the [two-rate three-color marker](/two-rate-three-color-marker/).

**Policing compared with shaping.**

| | policing | [shaping](/traffic-shaping/) |
|---|---|---|
| out-of-profile packets | dropped or marked at once | held in a queue until they fit |
| added delay | none | up to the queue size divided by the rate |
| buffer | none | needed |
| bursts above the profile | lost | smoothed, if the queue has room |
| output | the passed packets fit the profile | all packets that are not dropped fit the profile |
| effect on TCP | runs of losses, then retransmissions | higher round-trip time, few losses |

**Effect on TCP.** A TCP sender increases its rate until it sees loss. Against a policer it first sends a burst at the line rate, the bucket empties, and then many packets in a row are dropped. Flach and others measured traffic policing on 270 billion packets sent to 28,400 client networks in 2016. Depending on the region, up to 7% of the lossy transfers were policed, and policed transfers had loss rates about 6 times higher on average than transfers that were not policed. They proposed pacing at the sender and shaping as ways to get the same rate with fewer losses.

## Examples

**A burst at a policer.** A sender at 100 Mbit/s sends 20 packets of 1500 bytes back to back, one each 0.12 ms, into a policer of 10 Mbit/s (1250 bytes per ms) with a depth of $b = 15{,}000$ bytes, full at the start. In 0.12 ms the bucket gains 150 bytes. Packet $k$ (from 0) finds $15{,}000 + 150k - 1500k$ bytes of tokens, so packets 0 to 10 pass, and at 1.2 ms the bucket is empty. Packets 11 to 19 each find at most $9 \times 150 = 1350$ bytes and are dropped. So 11 packets pass and 9 in a row are lost, 45% of the burst. The same burst through a [shaper](/traffic-shaping/) with the same bucket loses nothing but delays the last packet by 9.72 ms.

**An API limit.** A token bucket with 10 requests per second and depth 20 polices one API key. A client that sends 30 requests at once gets 20 answers and 10 answers with status 429. A client that sends 10 per second gets all its answers.

**ATM usage parameter control.** At the user network interface, each cell is tested with GCRA on the peak cell rate and on the sustainable cell rate. A cell that fails is dropped, or tagged as low priority.

**A three-color policer.** With a committed rate and two bucket depths, a burst is green while the first bucket has tokens, yellow while only the second has, and red after. A router can forward green, forward yellow at low priority, and drop red.

## Where it is used

- **Network edges.** Internet service providers police customer links to the contracted rate. DiffServ boundary nodes police and mark traffic into classes.
- **Web APIs.** Per-key and per-IP request limits with status 429, using the [token bucket](/token-bucket/), [GCRA](/gcra/) or the window counters as the meter.
- **Protection of control planes.** Routers police traffic to their own processors, so that a flood of control packets cannot starve the routing process.
- **Guaranteed services.** RFC 2212 polices each flow at the edge against its token bucket specification, and treats the excess as best effort.

## References
