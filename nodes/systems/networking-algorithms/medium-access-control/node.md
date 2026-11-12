---
tag: 3BBJ7Z
kind: problem
slug: medium-access-control
name: Medium access control
aliases:
- multiple access problem
area: systems/networking-algorithms
level: intro
summary: "Many stations share one broadcast channel, and a frame gets through only if no other frame overlaps it. Decide who sends when, with no or little coordination, so that throughput is high and delay low."
prereqs: [bernoulli-trials]
see_also: [slotted-aloha, csma-cd, csma-ca, binary-exponential-backoff, wireless-link-scheduling, graph-coloring, independent-set, balls-into-bins]
sources:
  - book: isbn:9780132009164
    title: Dimitri Bertsekas and Robert Gallager, Data Networks, second edition, Prentice Hall, 1992
    locator: Chapter 4, Multiaccess Communication (Section 4.2 slotted multiaccess and ALOHA, Section 4.3 splitting algorithms, Section 4.4 carrier sensing, Section 4.5 reservations and polling)
  - book: isbn:9780135928615
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition, Pearson, 2021
    locator: Chapter 6, Section 6.3 (multiple access links and protocols, channel partitioning, random access and taking-turns protocols)
  - book: isbn:9780132126953
    title: Andrew S. Tanenbaum and David J. Wetherall, Computer Networks, fifth edition, Pearson, 2011
    locator: Chapter 4, The Medium Access Control Sublayer (the channel allocation problem, multiple access protocols, Ethernet and wireless LANs)
  - paper: doi:10.1145/1478462.1478502
    title: "Norman Abramson, THE ALOHA SYSTEM: another alternative for computer communications, AFIPS Fall Joint Computer Conference, 1970"
    locator: pages 281 to 285 (the first random access radio channel)
---

Medium access control is the problem of sharing one broadcast channel among many stations. When two stations send at overlapping times, the frames collide and are usually lost, so the stations need a rule that decides who sends when. The rule should keep the channel busy with useful frames, keep delays short and treat stations fairly, and it must work with the little that each station knows: often only its own queue and what it hears on the channel. Solutions fall into three families: *channel partitioning* (time, frequency or code division), *taking turns* (polling, tokens, reservations) and *random access* ([slotted ALOHA](/slotted-aloha/), [CSMA/CD](/csma-cd/), [CSMA/CA](/csma-ca/) and splitting algorithms).

## In plain words

Think of a classroom with one microphone. Anyone can talk into it, but if two people talk at once, nobody understands either. You could give each person a fixed turn, which is fair but slow when only one person has something to say. You could let a teacher call on people, which works well until the teacher is busy. Or you could let people just try, listen, and wait a random time after a clash. That is fast when few people talk and messy when many do. Medium access control is the study of these rules for computers and radios on a shared wire or radio channel.

## Definition

**Collision channel.** There are $n$ stations and one channel. A station sends a frame by occupying the channel for one frame time. A receiver gets the frame if and only if no other frame overlaps it in time at the receiver. In the *slotted* version, time is cut into slots of one frame time, frames start only at slot starts, and each slot is idle, a success or a collision.

**Feedback.** What a station learns is part of the problem:

- *ternary feedback*: after each slot, every station learns whether it was idle, a success or a collision;
- *acknowledgement only*: a sender learns whether its own frame got through;
- *carrier sense*: a station can tell, before it sends, whether the channel is busy at its own position;
- *collision detection*: a sender can tell, while it sends, that another signal is present.

**Traffic.** Frames arrive at the stations over time, often modeled as independent Poisson or Bernoulli arrivals with total rate $\lambda$ frames per frame time. In the *infinite-population* model each new frame comes from a new station.

**Goal.** A protocol is a rule, run at each station, that decides from the station's history whether to send in each slot or at each moment. The main measures are:

- the *throughput*, the long-run fraction of time carrying successful frames, and the largest arrival rate for which the queues stay stable;
- the *delay* of a frame from arrival to delivery;
- *fairness* among stations;
- the amount of coordination needed: a shared clock, the number of stations, a central controller.

## Variants

- **Channel partitioning.** Time division (TDMA) gives each station every $n$-th slot; frequency division (FDMA) gives each a band; code division (CDMA) gives each a code, so that several frames can be decoded at once; OFDMA assigns subcarriers. There are no collisions, but a station with nothing to send leaves its share idle.
- **Taking turns.** A master polls the stations in order, or a token passes from station to station and only its holder sends, or stations reserve future slots in a short contention phase. These reach a throughput near one under heavy load, at the cost of a coordinator, a token that can be lost or a reservation overhead.
- **Random access.** Stations send when they have frames and repeat after collisions with random delays: ALOHA, slotted ALOHA, CSMA with or without collision detection or avoidance, and splitting (tree) algorithms. They need no coordination and are fast under light load.
- **Spatial reuse.** On radio channels a frame collides only at receivers that hear two senders. The channel is then a graph of interference, and several links can be active at once if they do not conflict. Choosing sets of links that may send together is [wireless link scheduling](/wireless-link-scheduling/).
- **Known or unknown number of stations.** Many analyses assume $n$ known; a protocol for unknown $n$ must estimate it, for example by [binary exponential backoff](/binary-exponential-backoff/) or a backlog estimate.

## Examples

- **Three stations, slotted, ternary feedback, each always has a frame.** TDMA delivers one frame per slot. Slotted ALOHA with send probability $1/3$ delivers a frame in a slot with probability $3 \cdot \frac13 \cdot (\frac23)^2 = 4/9$.
- **One station with traffic, nine silent.** TDMA with $n = 10$ makes the busy station wait for its turn, so it can use only one slot in ten. Random access lets it send at once and use every slot.
- **Shared Ethernet.** Stations on a cable sense the carrier and detect collisions within a round trip; CSMA/CD stops colliding frames early and wastes little time.
- **Wi-Fi with a hidden station.** Stations $A$ and $C$ both send to $B$ but cannot hear each other, so carrier sense does not prevent their collisions at $B$. CSMA/CA adds acknowledgements and an RTS/CTS handshake.

## Known algorithms

| protocol | family | needs | best throughput |
|---|---|---|---|
| TDMA, FDMA | partitioning | a schedule or band plan | 1 under full load |
| polling, token passing | taking turns | a master or a token | near 1 under load |
| pure ALOHA | random access | acknowledgements | $1/(2e) \approx 0.184$ |
| [slotted ALOHA](/slotted-aloha/) | random access | slot clock, feedback | $1/e \approx 0.368$ |
| splitting (FCFS) algorithms | random access | slot clock, ternary feedback | about $0.487$, stable |
| [CSMA/CD](/csma-cd/) | random access | carrier sense, collision detection | near 1 when the bus is short compared with a frame |
| [CSMA/CA](/csma-ca/) | random access | carrier sense, ACKs | about $0.6$ to $0.85$ in the saturation model of Bianchi |

The throughputs of the random access rows are for the model each protocol is analyzed in, and they are not directly comparable: carrier sense helps only when the propagation delay is small compared with a frame.

## Bounds

- **Partitioning reaches throughput 1** but has delay about $n/2$ slots even under light load, because a station waits for its turn.
- **Slotted ALOHA with a common send probability** has a throughput of at most $(1 - 1/n)^{n-1}$, which tends to $1/e$; with Poisson traffic the maximum is $1/e$ at an offered load of one frame per slot.
- **Stable throughput with ternary feedback.** In the infinite-population Poisson model, splitting algorithms are stable for arrival rates up to about $0.487$ frames per slot, and it is known that no protocol is stable above about $0.568$ (Bertsekas and Gallager, Section 4.3). The exact capacity of this channel is open.
- **Instability.** Slotted ALOHA with a fixed repeat probability is unstable in the infinite-population model for any positive arrival rate: the backlog drifts to infinity. Adapting the probability to an estimate of the backlog restores stability for rates below $1/e$.
- **Carrier sense.** With end-to-end delay $\tau$ and frame time $T$, collisions cost time of order $\tau$, so CSMA protocols approach throughput 1 as $a = \tau / T \to 0$; the textbook approximation for CSMA/CD is $1/(1 + 5a)$.

## Reductions

- **Collision-free schedules are independent sets.** If two links conflict when they share a receiver or one sender reaches the other's receiver, the sets of links that may send in the same slot are the [independent sets](/independent-set/) of the conflict graph, and a schedule that gives every link one slot in each frame is a [coloring](/graph-coloring/) of that graph.
- **One slot of random access is balls into bins.** If $k$ stations each pick one of $s$ slots at random, a station succeeds when its bin holds one ball, so framed slotted ALOHA (used to read RFID tags) is a [balls into bins](/balls-into-bins/) process.
- **Contention resolution.** Resolving a collision of $k$ stations is a group testing problem: each slot is a test that answers whether zero, one or several of the remaining stations are in a chosen subset. Splitting algorithms are adaptive group tests.

## Applications

Every shared link layer solves this problem: Ethernet in its half duplex form, Wi-Fi, Bluetooth, the random access channels by which phones join a cellular cell, satellite return links, IEEE 802.15.4 sensor networks, cable modems, which reserve upstream slots by contention, and RFID readers, which use framed slotted ALOHA to count tags.

## References
