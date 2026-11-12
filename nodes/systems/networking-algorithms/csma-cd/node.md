---
tag: 296FV6
kind: algorithm
slug: csma-cd
name: CSMA/CD
aliases:
- carrier sense multiple access with collision detection
- Ethernet MAC
area: systems/networking-algorithms
level: intro
summary: "Listen before sending, stop at once when a collision is heard, and retry after a random backoff. Classic shared Ethernet uses it with a 512-bit slot and a 64-byte minimum frame."
solves: [medium-access-control]
model: asynchronous-model
complexity:
  vars: {n: the number of stations, k: the number of collisions of one frame}
  time: {worst: O(k), expected: O(k)}
  space: {extra: O(1)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1976
  people: [Robert M. Metcalfe, David R. Boggs]
  note: Metcalfe and Boggs built Ethernet at Xerox PARC in 1973 and described it in 1976. The 10 Mb/s form was standardized as IEEE 802.3 in 1983.
prereqs: [medium-access-control, slotted-aloha]
see_also: [binary-exponential-backoff, exponential-backoff, csma-ca, wireless-link-scheduling]
sources:
  - paper: doi:10.1145/360248.360253
    title: "Robert M. Metcalfe and David R. Boggs, Ethernet: distributed packet switching for local computer networks, Communications of the ACM 19(7), 1976"
    locator: pages 395 to 404 (carrier sense, collision detection, the jam, backoff and the efficiency estimate)
  - url: "https://standards.ieee.org/ieee/802.3/7071/"
    title: IEEE Standard for Ethernet, IEEE 802.3
    locator: Clause 4, the media access control (slotTime 512 bit times, jamSize 32 bits, attemptLimit 16, backoffLimit 10, minFrameSize 512 bits)
  - book: isbn:9780135928615
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition, Pearson, 2021
    locator: Chapter 6, Section 6.3 (CSMA, CSMA/CD and the efficiency 1/(1 + 5a))
  - book: isbn:9780132126953
    title: Andrew S. Tanenbaum and David J. Wetherall, Computer Networks, fifth edition, Pearson, 2011
    locator: Chapter 4 (persistent and nonpersistent CSMA, CSMA/CD, classic Ethernet)
  - book: isbn:9780132009164
    title: Dimitri Bertsekas and Robert Gallager, Data Networks, second edition, Prentice Hall, 1992
    locator: Chapter 4, Section 4.4 (carrier sensing and collision detection)
---

CSMA/CD (carrier sense multiple access with collision detection) is the [medium access control](/medium-access-control/) protocol of classic shared Ethernet. A station listens to the cable before it sends and waits while another station is sending. Two stations can still start at almost the same time, because a signal takes time to cross the cable. A sending station keeps listening, and when it hears another signal it stops its frame, sends a short jam signal and tries again after a random wait chosen by [binary exponential backoff](/binary-exponential-backoff/). Every frame must last at least one round trip of the cable, so that the sender is still sending when news of a collision gets back to it.

## In plain words

Think of people at a dinner table. Nobody starts to talk while someone else talks. Sometimes two people start at the same moment. Each one hears the other, both stop at once, and each waits a random short time before trying again. If they clash again, they wait longer on average. CSMA/CD is this rule for computers on one cable. The only trick is about time. A signal needs time to reach the far end of the cable, so a station must keep talking long enough to hear a clash from the far end. That is why Ethernet has a smallest frame size.

## The problem

Stations sit along one cable, a bus. A signal that one station puts on the bus reaches a station at distance $d$ after a propagation delay of $d$ bit times, and the largest such delay is $\tau$, the end-to-end delay. Every station can sense whether a signal of another station is present at its own point (carrier sense), and it can detect that a second signal is present while it sends (collision detection). There is no shared clock and no central control. The task is to deliver frames with few collisions, to waste little time on the collisions that happen, and to make sure that a sender knows whether its frame got through intact. This is the carrier sense form of [medium access control](/medium-access-control/).

## The algorithm

The pseudocode is the transmit side of 1-persistent CSMA/CD at one station, with the constants of 10 Mb/s Ethernet. One bit time is $0.1\,\mu s$ at 10 Mb/s.

```pseudo id=main
CSMA-CD(F)                                    ▷ times in bit times; 10 Mb/s values
L1  attempts ← 0                              ▷ the frame F is ready
L2  wait until the channel is idle
L3  wait 96 more bit times of idle channel (the interframe gap); if it turns busy go to L2
L4  start to send F
L5  listen while sending
L6  if another signal is heard before F ends then
L7      stop F, send a 32-bit jam, attempts ← attempts + 1
L8  else return "sent"
L9  if attempts = 16 then return "dropped"
L10 wait K · 512 bit times, K uniform in {0, …, 2^min(attempts, 10) − 1}; go to L2
```

Lines L2 and L3 are carrier sense, and they are *1-persistent*: a station that finds the channel busy sends as soon as the channel turns idle and the gap has passed. Lines L5 to L7 are collision detection. The jam of line L7 makes sure that every station involved hears the collision, even one whose own signal was very short. Line L10 is truncated binary exponential backoff: the window doubles after each collision of the same frame, up to $1024$ slots. The *slot time* of 512 bit times is the unit of backoff and also the minimum frame length of 64 bytes, and it must be at least the round trip $2\tau$ plus the jam and some margin.

| constant | 10 Mb/s value |
|---|---|
| slot time and minimum frame | 512 bit times, 64 bytes, $51.2\,\mu s$ |
| interframe gap | 96 bit times, $9.6\,\mu s$ |
| jam | 32 bits |
| attempt limit | 16 |
| backoff limit | window $2^{10}$ slots |

## Example

Three stations: $A$ at position $0$, $C$ at $290$ and $B$ at $300$, in bit times of propagation, so $\tau = 300$ and the round trip is $600$. The cable is longer than the standard allows, which is the point of the example. Station $C$ is the receiver.

**A frame that is too short.** $A$ has a 100-bit frame at time 0, and $B$ has one at time 380.

1. $A$ waits the gap and sends during $[96, 196)$. Its signal reaches $C$ at $386$ and $B$ at $396$.
2. At time $380$ the frame of $A$ has not yet reached $B$, so $B$ senses an idle channel and starts its frame.
3. At $396$ the signal of $A$ reaches $B$. $B$ detects the collision, stops and sends its jam.
4. The signal of $B$ reaches $A$ at $380 + 300 = 680$. $A$ finished at $196$, so $A$ hears nothing and reports its frame as sent.
5. At $C$ the frame of $A$ is present during $[386, 486)$ and the signal of $B$ from $390$: the frame of $A$ is garbled at $C$. The collision went *undetected* by its sender. $B$ backs off and later delivers its frame intact.

**The same scene with 600-bit frames.** Now $A$ sends from $96$, and at time $680$ it is still sending when the signal of $B$ arrives. It stops the frame at $680$, sends the jam, and both stations back off. In the run of the implementation both frames then go through intact on later attempts. A frame of $600 \ge 2\tau$ bit times is long enough, which is what the theorem below says.

**Efficiency.** Ten stations evenly spaced over a bus with $\tau = 256$, each with 30 frames of 512 bits ready at time 0 (seed 9), finished all 300 frames by time $191902$, an efficiency of $153600 / 191902 \approx 0.80$, with 54 jam bursts in total. The approximation $1/(1 + 5a)$ with $a = \tau / 512$ gives $0.29$. The run also showed the *capture effect*: each station sent all its 30 frames in a row before the next station got one through, because the winner of a collision resets its attempt count and backs off over the smallest window, while the losers keep their larger windows.

## Correctness

The safety property is that a sender that finishes a frame (line L8) may trust that the frame is intact. Let $L$ be the length of a frame of station $A$ that starts at $s_a$, and let $b$ be a signal of station $B$ at distance $d \le \tau$ that overlaps it somewhere on the bus.

- If $b$ starts after $s_a$, carrier sense at $B$ means it started before the frame of $A$ reached $B$, so before $s_a + d$. Then $b$ reaches $A$ before $s_a + 2d \le s_a + 2\tau$.
- If $b$ starts before $s_a$, carrier sense at $A$ means $b$ had not yet reached $A$ at $s_a$. Then $b$ reaches $A$ within $d$ bit times after $s_a$.

Either way $A$ hears $b$ before $s_a + 2\tau$. So if $L \ge 2\tau$, $A$ is still sending, detects the collision and stops. The minimum frame of 512 bits is what makes this hold on a standard bus. The example above shows that the bound is needed. Each frame also leaves the station after at most 16 attempts, sent or dropped, because every pass that does not end at line L8 adds one to the attempt count. The proof file below gives the details.

## Complexity

- **Work per frame.** A station does $O(1)$ work per attempt: a sense, a send and one random draw. A frame that collides $k$ times costs $O(k)$ work, and $k \le 16$. The state is $O(1)$: the attempt count and the backoff timer.
- **Time lost to a collision.** A collision wastes at most the round trip $2\tau$ plus the jam, because every involved station stops within that time. In unslotted ALOHA a collision wastes up to two whole frame times.
- **Efficiency.** With $a = \tau / T$ for frame time $T$, the textbook approximation of Kurose and Ross is $1 / (1 + 5a)$, close to $1$ when frames are long compared with the bus. It comes from a model with many stations, each sending in each contention slot with the best probability, and it is an approximation, not a bound. A bus with few busy stations, as in the run of the example, can do much better because of capture.
- **Delay.** Under light load a frame waits only the gap of $96$ bit times. The backoff window after $k$ collisions has $2^{\min(k, 10)}$ slots, so delays grow fast under heavy load.

## Properties

- **Decentralized and asynchronous.** There is no clock and no master; each station uses only what it senses at its own point of the cable.
- **Fast abort.** Collisions cost a round trip, not a whole frame, which is the gain over [slotted ALOHA](/slotted-aloha/).
- **Needs a short bus or long frames.** The guarantee holds only if a frame lasts at least the round trip. For a fixed minimum frame, a faster bit rate means a shorter allowed cable; this limited the diameter of shared 10 Mb/s Ethernet to about 2500 meters and of shared 100 Mb/s Ethernet to about 200 meters.
- **Unfair in the short run.** The capture effect lets one station send many frames in a row under load.
- **Not suited to radio.** A radio cannot hear well while it sends, and not every station hears every other one, so wireless LANs use [CSMA/CA](/csma-ca/) instead.

## Variants and improvements

- **Nonpersistent and p-persistent CSMA.** A nonpersistent station that senses a busy channel waits a random time before it senses again, instead of watching for the end of the busy period. A p-persistent station sends with probability $p$ when the channel turns idle. Both lower the chance of a collision at the end of a busy period at the cost of more idle time.
- **CSMA without collision detection.** The sender only learns of a collision from a missing acknowledgement, so each collision costs a whole frame. Tanenbaum compares the throughput of these variants.
- **Backoff rules.** The binary exponential rule of line L10 is the standard; the [exponential backoff](/exponential-backoff/) page treats the general family.
- **Full duplex Ethernet.** Switched Ethernet with one station per link and separate wires in each direction has no collisions, and CSMA/CD is turned off. Modern Ethernet is of this kind.
- **Gigabit carrier extension.** Half duplex Gigabit Ethernet kept the minimum frame of 64 bytes but extended the slot to 4096 bit times by padding short frames with a carrier extension, and added frame bursting.

## When to use it

Use CSMA/CD on a shared wired medium where every station hears every other one and can detect a collision while it sends, and where the round trip is short compared with a frame. That was the case for coaxial and hub-based Ethernet. Today almost all Ethernet is switched and full duplex, so CSMA/CD survives mainly in half duplex links, some industrial and automotive buses and as the textbook model of carrier sense. On radio channels use [CSMA/CA](/csma-ca/); when there is no carrier sense at all, use [slotted ALOHA](/slotted-aloha/) or a schedule.

## Pitfalls

- **Frames shorter than the round trip.** A short frame, or a cable longer than the standard allows, makes a collision invisible to its sender. The frame is lost and the loss is found only by a higher layer. Pad short frames to 64 bytes.
- **Skipping the jam.** Without the jam a station whose signal collided only briefly might not register the collision, and the stations may disagree about whether a collision happened.
- **Forgetting the interframe gap after one's own frame.** A station must also wait the gap after its own frame. Otherwise a station with a long queue sends frame after frame with no idle time, and the other stations never sense an idle channel.
- **Resetting the backoff count in the wrong place.** The count belongs to one frame. Reset it after a success or a drop, not after each attempt; but the reset after success is what causes capture.
- **Reading the efficiency formula as exact.** $1/(1+5a)$ is a model value; measured efficiency depends on the number of active stations, frame sizes and the backoff rule.

## Implementations

## History

Robert Metcalfe and David Boggs built the first Ethernet at Xerox PARC in 1973, inspired by the ALOHA network of Hawaii, and published it in 1976. Their paper added carrier sense and collision detection to random access and introduced the backoff rule. Digital, Intel and Xerox published the 10 Mb/s DIX Ethernet specification in 1980, and the IEEE standardized it as 802.3 in 1983. Hubs, then switches, replaced the coaxial bus, and full duplex switched Ethernet made CSMA/CD rarely active, though it is still in the standard for half duplex operation.

## References
