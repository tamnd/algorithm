---
tag: HMFCEA
kind: algorithm
slug: csma-ca
name: CSMA/CA
aliases:
- 802.11 DCF
- carrier sense multiple access with collision avoidance
area: systems/networking-algorithms
level: intro
summary: "Wireless stations cannot hear a collision, so they wait for an idle medium, count down a random backoff, and rely on ACKs. RTS/CTS and the NAV soften the hidden terminal problem."
solves: [medium-access-control]
model: asynchronous-model
complexity:
  vars: {n: the number of stations, k: the number of attempts of one frame}
  time: {worst: O(k), expected: O(k)}
  space: {extra: O(1)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1997
  people: [Phil Karn, Vaduvur Bharghavan, Giuseppe Bianchi]
  note: Karn proposed the RTS/CTS handshake of MACA in 1990 and Bharghavan and others refined it as MACAW in 1994. The IEEE 802.11 standard of 1997 made CSMA/CA with ACKs, optional RTS/CTS and the NAV its distributed coordination function. Bianchi modeled its saturation throughput in 2000.
prereqs: [medium-access-control, csma-cd]
see_also: [slotted-aloha, binary-exponential-backoff, exponential-backoff, wireless-link-scheduling, bisection-method]
sources:
  - url: "https://standards.ieee.org/ieee/802.11/7028/"
    title: IEEE Standard for Information Technology, Part 11, Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications, IEEE 802.11
    locator: the distributed coordination function (DCF), interframe spaces, the backoff procedure, RTS/CTS and the NAV
  - paper: doi:10.1109/49.840210
    title: "Giuseppe Bianchi, Performance analysis of the IEEE 802.11 distributed coordination function, IEEE Journal on Selected Areas in Communications 18(3), 2000"
    locator: pages 535 to 547 (the Markov chain of the backoff, the fixed point for tau and p, the saturation throughput)
  - paper: "Phil Karn, MACA: a new channel access method for packet radio, ARRL/CRRL Amateur Radio 9th Computer Networking Conference, 1990"
    locator: pages 134 to 140 (RTS and CTS, hidden and exposed terminals)
  - paper: doi:10.1145/190314.190334
    title: "Vaduvur Bharghavan, Alan Demers, Scott Shenker and Lixia Zhang, MACAW: a media access protocol for wireless LANs, ACM SIGCOMM 1994"
    locator: pages 212 to 225 (link-layer ACKs, the RTS-CTS-DS-DATA-ACK exchange, backoff copying and fairness)
  - paper: "Fouad A. Tobagi and Leonard Kleinrock, Packet switching in radio channels: Part II, the hidden terminal problem in carrier sense multiple-access and the busy-tone solution, IEEE Transactions on Communications 23(12), 1975"
    locator: the hidden terminal problem and the busy tone
  - book: isbn:9780135928615
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition, Pearson, 2021
    locator: Chapter 7, Section 7.3 (the 802.11 MAC protocol, hidden terminals, RTS and CTS)
---

CSMA/CA (carrier sense multiple access with collision avoidance) is the [medium access control](/medium-access-control/) protocol of Wi-Fi, the distributed coordination function (DCF) of IEEE 802.11. A radio cannot hear a collision while it sends, so unlike [CSMA/CD](/csma-cd/) it cannot stop a doomed frame. Instead it tries to avoid collisions before they happen: a station waits until the medium has been idle for a fixed time, then counts down a random backoff in idle slots, freezing the count while the medium is busy, and sends only when the count reaches zero. The receiver confirms each frame with an ACK, and a missing ACK counts as a collision and doubles the backoff window. An optional RTS/CTS handshake reserves the medium for stations that cannot hear the sender.

## In plain words

Radios on one channel take turns without a referee. A radio that wants to talk first listens. If the channel is busy, it waits. When the channel has been quiet for a short while, the radio picks a random number and counts it down, one tick for each quiet moment; if someone else starts talking, it pauses the count. When the count hits zero, it talks. Because a radio cannot hear others while it talks, the listener answers with a short "got it". No answer means something went wrong, so the radio tries again with a larger range of random numbers. For long messages, the radio can first ask "may I?" and wait for "go ahead", so that radios near the listener also know to stay quiet.

## The problem

Stations share one radio channel. A station hears only the stations within its range, and while it sends it cannot hear anything, so a collision is invisible to its senders. Two stations that cannot hear each other may both reach a third one: a *hidden terminal* pair. Two stations that hear each other may send to receivers that would not be disturbed, but carrier sense still keeps them from sending at the same time: an *exposed terminal* pair. The task is to share the channel with few collisions and no central control, and to let a sender learn whether its frame arrived.

## The algorithm

The pseudocode is the sending side for one frame. CW is the contention window, DIFS and SIFS are the two interframe spaces with SIFS shorter than DIFS, and the retry limit is a constant of the standard.

```pseudo id=main
DCF-SEND(F)                                    ▷ one frame at one station
L1  stage ← 0
L2  wait until the medium has been idle for DIFS
L3  b ← uniform integer in {0, …, CW}, CW = min(2^stage (CWmin + 1), CWmax + 1) − 1
L4  while b > 0: after each idle slot b ← b − 1; if the medium turns busy, freeze b and wait for DIFS of idle medium again
L5  send F (with RTS/CTS: send an RTS, and send F SIFS after the CTS)
L6  wait SIFS plus the ACK time for an ACK
L7  if the ACK came then return "sent"
L8  stage ← stage + 1                          ▷ no CTS or no ACK: treat it as a collision
L9  if stage > the retry limit then return "dropped" else go to L2
```

The receiving side answers without carrier sense: SIFS after a correct data frame addressed to it, it sends an ACK, and SIFS after an RTS it sends a CTS unless its NAV says the medium is reserved. Because SIFS is shorter than DIFS, these answers always win over new frames.

*Virtual carrier sense.* Every RTS, CTS and data frame carries the time until the end of its exchange. A station that receives a frame addressed to another station sets its *network allocation vector* (NAV) to that end time and treats the medium as busy until then, even if it hears nothing. A station that hears the CTS of a receiver, but not the RTS of a hidden sender, still learns to keep quiet.

Typical values: in 802.11b a slot is $20\,\mu s$, SIFS $10\,\mu s$, DIFS $50\,\mu s$ and the window grows from $31$ to $1023$; in 802.11a and g a slot is $9\,\mu s$, SIFS $16\,\mu s$, DIFS $34\,\mu s$ and CWmin is $15$. Every station also runs a fresh backoff after each success (the post-backoff), so a station with a queue cannot keep the channel.

## Example

**Saturation.** Take $n$ stations that all hear each other and always have a frame, with $W = \text{CWmin} + 1 = 32$ and $m = 5$ doublings, so the window grows to $1024$. Bianchi models each station as sending in a backoff slot with probability $\tau$ and colliding with constant probability $p$, and solves

$$\tau = \frac{2}{1 + W + p W \sum_{k=0}^{m-1} (2p)^k}, \qquad p = 1 - (1 - \tau)^{n-1}.$$

The throughput $S$ below is the fraction of time spent on payload, with the timing of Bianchi's 1 Mb/s example (slot $50\,\mu s$, SIFS $28\,\mu s$, DIFS $128\,\mu s$, payload 8184 bits, basic access). The simulation runs the backoff of the stations slot by slot for $200000$ backoff slots with the seed $n$ and makes no independence assumption.

| $n$ | model $\tau$ | sim $\tau$ | model $p$ | sim $p$ | model $S$ | sim $S$ |
|---|---|---|---|---|---|---|
| 5 | 0.04785 | 0.04744 | 0.17808 | 0.17940 | 0.8102 | 0.8093 |
| 10 | 0.03731 | 0.03723 | 0.28977 | 0.29049 | 0.7579 | 0.7576 |
| 20 | 0.02642 | 0.02659 | 0.39878 | 0.39631 | 0.6975 | 0.6990 |
| 50 | 0.01539 | 0.01535 | 0.53236 | 0.53020 | 0.6109 | 0.6130 |

More stations make each station more careful, but not enough: the collision probability rises and the throughput falls.

**Hidden terminals.** Three stations in a line, $A - B - C$, where $A$ and $C$ both send to $B$ but cannot hear each other. In the slot-level network simulation (data frame 20 slots, RTS, CTS and ACK 2 slots, SIFS 1, DIFS 3; $30000$ slots, seed 3), $231$ of $961$ data frames, $24$ percent, were garbled at $B$ without RTS/CTS. With RTS/CTS, $C$ hears the CTS of $B$ and sets its NAV, and only $25$ of $744$ data frames, $3.4$ percent, were lost. The rest of the losses come from a station that was sending its own RTS while the CTS went by and so missed it.

**Exposed terminals.** Four stations in a line, $A - B - C - D$, where $B$ sends to $A$ and $C$ sends to $D$. The two transfers would not disturb each other's receivers, but $B$ and $C$ hear each other and take turns. In the same simulation the two links delivered $537 + 544 = 1081$ frames, against $894$ frames for one link alone and $1788$ for two independent links. The surplus over one link comes only from the slots in which both counters reached zero together.

**One collision domain.** With three senders and one receiver that all hear each other, $195$ of $1144$ data frames were lost without RTS/CTS and none with it: once an RTS gets through, every other station sets its NAV for the whole exchange.

## Correctness

A sender reports a frame as sent only when the ACK comes, and the receiver sends the ACK only after it received the frame intact. So a reported success is a real one. The converse fails: if the ACK is lost, the sender repeats a frame that already arrived, and the receiver drops the copy by its sequence number. Every frame leaves the sender after at most the retry limit plus one attempts, because each failure increases the stage at line L8.

In a single collision domain, RTS/CTS protects the data frame completely: an RTS that gets through is heard by every other station, which sets its NAV to the end of the exchange, and SIFS answers cannot interfere because DIFS is longer than SIFS. With hidden terminals the protection is only partial, as the example shows.

The model of Bianchi follows from a renewal argument: a frame needs $1/(1-p)$ attempts on average, and the attempt at stage $i$ takes on average $(W_i + 1)/2$ backoff slots, where $W_i$ is the window. The fixed point has exactly one solution: $\tau(p)$ decreases in $p$, so $1 - (1 - \tau(p))^{n-1} - p$ decreases strictly and changes sign once on $[0, 1]$, and [bisection](/bisection-method/) finds the root. The proofs are in the proof file below.

## Complexity

- **Work per frame.** Each station does $O(1)$ work per slot and per attempt; a frame that needs $k$ attempts costs $O(k)$ draws, with $k$ at most the retry limit plus one. The state is the stage, the counter and the NAV.
- **Time.** An attempt at stage $i$ waits DIFS plus on average $\text{CW}_i / 2$ idle slots, plus the slots frozen during other transmissions. The window doubles with each failure, so the delay grows fast when the collision probability is high.
- **Throughput.** In saturation, about $0.81$ of the time carries payload for $5$ stations and $0.61$ for $50$ in the example. The cost per collision is a whole frame plus the ACK timeout, unlike [CSMA/CD](/csma-cd/), which stops a frame within a round trip.
- **RTS/CTS overhead.** The handshake adds two short frames and two SIFS to every exchange; for one link alone the delivered frames dropped from $894$ to $759$ in the example. It pays off only for long frames or many hidden stations, so real devices use it above a length threshold.

## Properties

- **Decentralized.** Each station uses only what it senses, the ACKs and the NAV.
- **Collision avoidance, not collision detection.** Losses are found by a missing ACK, after a whole frame time.
- **Fair in the long run among stations that hear each other.** In the saturation runs above with $5$, $10$ and $20$ stations, every station got at least $0.85$ times the successes of the busiest one. Short-term unfairness remains, because the station that just succeeded restarts from the smallest window.
- **Sensitive to the topology.** Hidden terminals cause collisions that carrier sense cannot prevent; exposed terminals waste chances to send in parallel.
- **No hard delay guarantee.** The backoff is random, and a frame can be dropped after the retry limit.

## Variants and improvements

- **MACA and MACAW.** Karn's MACA used only RTS and CTS with no carrier sense. MACAW added link-layer ACKs, a DS frame and fairer backoff rules, and DCF took over much of this design.
- **EDCA.** The 802.11e enhanced distributed channel access gives each traffic class its own AIFS (in place of DIFS) and window sizes, so voice frames wait less than bulk data.
- **Point and hybrid coordination.** The PCF and HCF let an access point poll stations, a controlled access scheme on top of DCF.
- **Other backoff rules.** Lowering the window gently after a success, or tuning CWmin to the number of stations, raises saturation throughput. The [exponential backoff](/exponential-backoff/) page covers the general family; DCF uses the [binary](/binary-exponential-backoff/) form.
- **OFDMA in 802.11ax.** The access point schedules several stations at once on separate subcarriers, which moves Wi-Fi toward [scheduled access](/wireless-link-scheduling/).
- **Busy tones.** Tobagi and Kleinrock proposed a separate tone that a busy receiver sends, which tells hidden stations to keep quiet.

## When to use it

Use CSMA/CA on radio channels, where a station cannot detect collisions while it sends and the stations may not all hear each other. It suits bursty traffic from many stations with no central schedule, as in Wi-Fi and in IEEE 802.15.4 sensor networks, which use a slotted or unslotted CSMA/CA without RTS/CTS. Turn on RTS/CTS when frames are long and hidden stations are likely. When the load is high and steady, or delays must be bounded, a scheduled scheme such as TDMA, polling or OFDMA is better. On a wire with collision detection, [CSMA/CD](/csma-cd/) wastes less per collision.

## Pitfalls

- **Expecting RTS/CTS to solve hidden terminals.** It helps a lot, but a station that misses the CTS can still collide with the data, and the handshake costs time on every frame.
- **Confusing carrier sense with interference range.** A station may be too far to sense a sender but close enough to garble frames at the receiver; hidden terminals are about the receiver's neighborhood.
- **Not freezing the counter.** Counting down during busy periods makes all waiting stations reach zero together right after a transmission.
- **Reading a missing ACK as a collision only.** Fading and noise also lose frames, and doubling the window for them lowers throughput for no gain. Rate adaptation and error recovery need to tell them apart.
- **Taking Bianchi's model as exact.** It assumes saturation, a constant collision probability and an ideal channel. It matches simulations well in that setting, not under light load or with hidden terminals.

## Implementations

## History

Tobagi and Kleinrock described the hidden terminal problem of carrier sense on radio channels in 1975. Phil Karn proposed MACA in 1990 for amateur packet radio, replacing carrier sense with an RTS and CTS exchange. Bharghavan, Demers, Shenker and Zhang refined it at Xerox PARC as MACAW in 1994, adding link-layer acknowledgements. The IEEE 802.11 standard of 1997 combined physical carrier sense, random backoff, ACKs, optional RTS/CTS and the NAV in its distributed coordination function, and Giuseppe Bianchi's 2000 model of its saturation throughput became the standard analysis.

## References
