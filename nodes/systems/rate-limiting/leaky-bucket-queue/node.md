---
tag: QSRTMA
kind: algorithm
slug: leaky-bucket-queue
name: Leaky bucket (queue)
aliases:
- leaky bucket as a queue
- leaky bucket shaper
area: systems/rate-limiting
level: intro
summary: Requests enter a bounded FIFO queue drained at a constant rate; overflow is dropped.
solves: [rate-limiting-problem]
model: word-ram
complexity:
  vars: {n: the number of packets that arrive, k: the capacity of the queue in packets}
  time: {worst: Θ(n)}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1986
  people: [Jonathan S. Turner]
  note: Turner described the leaky bucket for packet networks in 1986.
prereqs: [leaky-bucket-meter, queue]
see_also: [leaky-bucket-meter, token-bucket, traffic-shaping, traffic-policing, gcra, burst-tolerance, circular-buffer, packet-scheduling]
sources:
  - paper: doi:10.1109/MCOM.1986.1092946
    title: Jonathan S. Turner, New directions in communications (or which way to the information age?), IEEE Communications Magazine 24(10), 1986
    locator: the leaky bucket as a way to control the rate and the burstiness of a virtual circuit
  - book: isbn:9780132126953
    title: Andrew S. Tanenbaum and David J. Wetherall, Computer Networks, fifth edition
    locator: Chapter 5, Section 5.4.2 (traffic shaping, leaky and token buckets)
  - book: isbn:9783540421849
    title: Jean-Yves Le Boudec and Patrick Thiran, Network Calculus, A Theory of Deterministic Queuing Systems for the Internet, Springer LNCS 2050, 2001
    locator: Section 1.2.2, Lemma 1.2.2 (content of a buffer served at constant rate r) and Section 1.5 (greedy shapers)
  - url: "https://www.rfc-editor.org/rfc/rfc2212"
    title: Scott Shenker, Craig Partridge and Roch Guerin, RFC 2212, Specification of Guaranteed Quality of Service, 1997
    locator: the section on policing (reshaping with a buffer, a token bucket and a peak rate regulator)
---

A leaky bucket queue is a [traffic shaper](/traffic-shaping/): it holds the arriving packets in a FIFO [queue](/queue/) of at most $K$ packets and sends them out at a constant rate $r$, one after the other. A packet that finds the queue full is dropped. The output has no bursts at all: the packets leave at most $r$ per second, whatever the input does, at the cost of a delay of up to $K/r$. For packets of one size it accepts exactly the packets that a [leaky bucket meter](/leaky-bucket-meter/) of size $K$ would pass, but the meter forwards them at once, in bursts, while the queue spaces them out.

## In plain words

Think of a bucket with a hole in the bottom, but now the requests themselves go into the bucket and drip out of the hole one at a time, at a fixed pace. If many requests come at once, they wait in the bucket. If the bucket is full, a new request spills over the edge and is lost.

So the output is always smooth: one request each tick, never faster. A burst of input becomes a train of evenly spaced requests, and the price is the time that each request spends in the bucket. A bucket that holds more requests loses fewer of them, but makes them wait longer.

## The problem

The input is a sequence of packets at times $t_1 \le t_2 \le \cdots$ with sizes $L_k$. The queue must send every packet that it accepts, in the order of arrival, so that the output never exceeds the rate $r$: a packet of size $L$ takes $L/r$ seconds on the output link. The buffer holds at most $K$ packets, counted with the one being sent. This is the shaping form of the [rate limiting problem](/rate-limiting-problem/), with the output curve $r\tau + L_{\max}$, a peak rate and no burst. The arrival model is adversarial.

## The algorithm

The queue $Q$ keeps a FIFO of packets and the departure time $Q.next$ of the head of the FIFO. The head is the packet on the link. DRAIN runs at each arrival; a real device runs it from a timer at each $Q.next$.

```pseudo id=main
LEAKY-BUCKET-QUEUE-ARRIVE(Q, t, p)     ▷ packet p of size L arrives at time t
L1  DRAIN(Q, t)
L2  if |Q.fifo| ≥ K then return DROP
L3  if Q.fifo is empty then Q.next ← t + L / r      ▷ the link is idle: start at once
L4  append p to the tail of Q.fifo
L5  return ACCEPT

DRAIN(Q, t)                              ▷ send each packet whose time has come
L6  while Q.fifo is not empty and Q.next ≤ t do
L7      remove the head of Q.fifo; it leaves at time Q.next
L8      if Q.fifo is not empty then Q.next ← Q.next + (size of the new head) / r
```

Line L3 starts the link when it is idle. Line L8 starts the next packet at the moment the one before it ends, so the link never idles while a packet waits. The capacity test of line L2 counts the packet on the link.

## Example

Let $r = 1$ packet per second and $K = 3$, with packets of one size. The column "in system" is the size of the FIFO after line L1.

| arrival | in system | decision | departure | delay |
|---|---|---|---|---|
| 0 | 0 | accept | 1 | 1 |
| 0 | 1 | accept | 2 | 2 |
| 0 | 2 | accept | 3 | 3 |
| 0 | 3 | drop | | |
| 0.5 | 3 | drop | | |
| 1.5 | 2 | accept | 4 | 2.5 |
| 2 | 2 | accept | 5 | 3 |
| 2 | 3 | drop | | |
| 2.5 | 3 | drop | | |
| 6 | 0 | accept | 7 | 1 |

Four packets come at time 0, and the fourth one is dropped. The output is one packet per second from time 1 to time 5, then one at time 7: never two in the same second. The largest delay is $3 = K/r$. A leaky bucket meter with $r = 1$ and $b = 3$ passes the same six packets (it gives the same pass and drop column), but it sends the first three at time 0 and the next two at times 1.5 and 2.

## Correctness

The full proof is below. For packets of any size, the departure of an accepted packet $k$ is

$$d_k = \max(t_k, d_{\text{prev}}) + L_k / r,$$

where $d_{\text{prev}}$ is the departure of the accepted packet before it. This is the recursion of a single server at a fixed rate. From it:

- **Smooth output.** Consecutive departures are at least $L_k/r$ apart, so any interval of length $\tau$ sees at most $r\tau + L_{\max}$ units leave; for packets of one size, at most $r\tau + 1$ packets.
- **Same acceptance as the meter (packets of one size).** At an arrival the FIFO holds $\lceil X \rceil$ packets, where $X = r \max(0, d_{\text{prev}} - t)$ is also the level of a leaky bucket meter with rate $r$ and size $K$. The test "fewer than $K$ packets" is $\lceil X \rceil \le K - 1$, which is $X + 1 \le K$, the meter test.
- **Delay.** Each accepted packet leaves $(X + 1)/r \le K/r$ seconds after it arrives.

## Complexity

In the [word RAM](/word-ram/):

- **Time.** An arrival does $\Theta(1)$ work plus one step of DRAIN per packet that leaves. Each packet leaves at most once, so $n$ arrivals cost $\Theta(n)$ in total, and $O(K)$ for one arrival in the worst case. With a timer that sends each packet at its time, each event is $\Theta(1)$.
- **Space.** $\Theta(K)$ for the FIFO, for example a [circular buffer](/circular-buffer/) of $K$ slots, plus the packets themselves.

## Properties

- **A shaper, not a policer.** It delays packets; it drops only when the buffer is full.
- **No output burst.** The output rate never exceeds $r$, even right after a quiet period. This is the main difference from the [token bucket](/token-bucket/) shaper, which sends a burst of up to $b$ at once.
- **Work conserving at rate $r$.** The link sends at rate $r$ whenever a packet waits, and idles otherwise. It never uses spare capacity above $r$.
- **FIFO.** Packets leave in the order they arrived.

## Variants and improvements

**Meter and queue.** The two leaky buckets share a name and a test, and differ in what passes through the hole.

| | [leaky bucket meter](/leaky-bucket-meter/) | leaky bucket queue |
|---|---|---|
| what is in the bucket | a counter (fluid), no packets | the packets |
| a conforming packet | is forwarded at once | waits, and leaves at rate $r$ |
| output curve | $r\tau + b$: bursts of $b$ | $r\tau + L_{\max}$: no bursts |
| delay | none | up to $K/r$ for one-size packets |
| state per flow | two numbers | a buffer of $K$ packets |
| decisions on one-size packets | pass iff level $+ 1 \le b$ | accept iff the same test with $b = K$ |

- **Byte capacity.** Count the buffer in bytes instead of packets. Then a large packet can be dropped where a small one fits. If the count holds only the unsent bytes, including the unsent part of the packet on the link, the queue accepts a packet of size $L$ exactly when that count plus $L$ is at most $K$, which is the meter test with $b = K$ for packets of any size.
- **Token bucket shaper.** Put a [token bucket](/token-bucket/) after the queue, so that the head leaves when it has tokens. The output then fits $r\tau + b$: bursts are allowed up to $b$. With $b$ equal to one packet it is the leaky bucket queue.
- **Peak rate plus token bucket.** RFC 2212 reshapes a flow with a buffer, a token bucket and a peak rate regulator; see [traffic shaping](/traffic-shaping/) and [burst tolerance](/burst-tolerance/).
- **Head drop.** Drop from the head instead of the tail when the buffer is full, so that the packets sent are the newest.

## When to use it

Use a leaky bucket queue when the receiver or the next link cannot take bursts at all: a link of fixed rate, a device with a tiny buffer, or a service that must see a steady request rate. If a short burst is fine, a token bucket shaper gives less delay. If you must not delay at all, use a policer such as the [leaky bucket meter](/leaky-bucket-meter/) and accept the losses.

## Pitfalls

- **Calling the meter a queue.** The two have the same name in many texts. A "leaky bucket" limiter that answers at once with yes or no is a meter, and its output has bursts of $b$.
- **Large buffers.** A buffer of $K$ packets adds up to $K/r$ of delay. A buffer sized for the worst burst can hold packets for seconds, which hurts interactive traffic and the round-trip estimates of TCP. See [active queue management](/active-queue-management/).
- **Wasted capacity.** The queue sends at rate $r$ even when the link is idle. A flow that could go faster for a moment cannot.
- **Timer granularity.** A software shaper that wakes up each millisecond cannot space packets by less than a millisecond. It must send a few packets per wake-up and keep the average at $r$.

## Implementations

The Python version is a discrete-event model with an explicit clock: the FIFO holds packet ids, and DRAIN records each departure time. The tests reproduce the table above, check that unit packets are accepted exactly when a leaky bucket meter with $b = K$ passes them, check the departure recursion and the delay $(X + 1)/r \le K/r$, and check, for packets of sizes 1 to 3, the FIFO order, the absence of idle time and the bound $r\tau + L_{\max}$ on the output.

## History

Turner described the leaky bucket in 1986 as a way to bound the rate and the bursts of the traffic that a user sends into a packet network. Textbooks such as Tanenbaum and Wetherall present the queue form as a traffic shaper and the token bucket as the shaper that allows bursts. Le Boudec and Thiran show that the content of a buffer served at constant rate $r$ is $\sup_{s \le t}(R(t) - R(s) - r(t - s))$, which is the level of the meter.

## References
