---
tag: CCRPNN
kind: concept
slug: backpressure
name: Backpressure
aliases:
- back pressure
area: systems/rate-limiting
level: advanced
summary: "A slow consumer makes its producer slow down: the buffer between them is bounded, and the producer may send only when the consumer has room, signaled by a blocked write, credits or demand."
prereqs: [queue, bounded-buffer-problem]
see_also: [flow-control, sliding-window-protocol, bounded-buffer-problem, admission-control, load-shedding, throttling, congestion-control, backpressure-routing]
sources:
  - url: https://github.com/reactive-streams/reactive-streams-jvm/blob/v1.0.4/README.md
    title: "Reactive Streams for the JVM, Specification version 1.0.4"
    locator: "Goals, Design and Scope; Specification rules 1.1 (onNext count at most the requested count), 2.1 (signal demand with request(n)), 3.9 (request(n) with n at most 0 is an error) and 3.17 (demand up to 2^63 - 1, effectively unbounded); section Subscriber controlled queue bounds"
  - paper: doi:10.1145/190314.190324
    title: "H. T. Kung, Trevor Blackwell and Alan Chapman, Credit-Based Flow Control for ATM Networks, Proceedings of ACM SIGCOMM 1994, pages 101 to 114"
    locator: Hop-by-hop credit-based flow control per virtual circuit, and the buffer needed for full link speed
  - paper: doi:10.1109/65.372658
    title: "H. T. Kung and Robert Morris, Credit-Based Flow Control for ATM Networks, IEEE Network 9(2), pages 40 to 48, 1995"
    locator: The credit protocol and the comparison with rate-based flow control
  - book: isbn:9780122007514
    title: William James Dally and Brian Towles, Principles and Practices of Interconnection Networks, Morgan Kaufmann, 2004
    locator: "Section 13.3 (buffer management and backpressure: 13.3.1 credit-based flow control and its credit round-trip time, 13.3.2 on/off flow control) and Chapter 14 (deadlock and livelock)"
  - url: https://www.rfc-editor.org/rfc/rfc9293
    title: "Wesley Eddy (editor), RFC 9293, Transmission Control Protocol (TCP), August 2022"
    locator: "Section 3.8.6 (managing the window: the receive window tells the sender how much data the receiver can accept)"
  - url: https://www.rfc-editor.org/rfc/rfc7323
    title: "David Borman, Bob Braden, Van Jacobson and Richard Scheffenegger, RFC 7323, TCP Extensions for High Performance, September 2014"
    locator: "Section 2 (the window scale option for windows above 65,535 bytes)"
  - url: https://man7.org/linux/man-pages/man7/pipe.7.html
    title: "Linux man-pages, pipe(7)"
    locator: "Section Pipe capacity (a write to a full pipe blocks; the default capacity is 16 pages, 65,536 bytes with 4096-byte pages)"
---

Backpressure is the signal by which a slow consumer makes its producer slow down, so that the data between them never needs more than a bounded buffer. The consumer has room for $B$ items, and the producer may send an item only when the consumer has said that there is room: by a write that blocks on a full buffer, by credits, by a window, or by a demand count such as `request(n)` in Reactive Streams. No work is lost, and the producer runs at the speed of the slowest stage after it. It is different from [backpressure routing](/backpressure-routing/), the max-weight routing and scheduling algorithm of Tassiulas and Ephremides, which uses queue differences to choose routes; here the word means only the slow-down signal.

## In plain words

A cook puts plates on a shelf, and a waiter takes them to the tables. The shelf holds ten plates. When the waiter is slow, the shelf fills up, and the cook must stop and wait until there is space. The cook slows down to the waiter's speed, and no plate falls on the floor.

That is backpressure. The slow end of a chain pushes back on the fast end, through a buffer of fixed size. The signal can be a full shelf, or the waiter can give the cook a ticket for each free space, and the cook may put down a plate only with a ticket.

Without backpressure, the cook keeps cooking. Either the plates pile up without end and get cold, or someone throws plates away. Backpressure keeps the pile small and loses nothing, but it makes the cook wait.

## The idea

**The rule.** Between a producer and a consumer there is a buffer of $B$ items. The producer sends an item only if the consumer will have a place for it. The consumer gives places back as it takes items out. The mechanisms differ only in how the producer learns of free places:

- **Blocking writes.** A bounded queue or a pipe in one address space. A write to a full buffer waits, as in the [bounded buffer problem](/bounded-buffer-problem/) and in Linux pipes, whose default capacity is 65,536 bytes.
- **Credits.** The consumer sends one credit for each place that becomes free, and the producer spends one credit for each item. Kung, Blackwell and Chapman use credits per virtual circuit on each ATM link, and on-chip and cluster networks use them per buffer, as in Dally and Towles, Section 13.3.1.
- **Windows.** The receiver advertises how many bytes it can still accept, and the sender keeps the unacknowledged data within that number. This is TCP [flow control](/flow-control/) (RFC 9293, Section 3.8.6), a [sliding window protocol](/sliding-window-protocol/).
- **Demand.** In Reactive Streams the subscriber calls `request(n)` to ask for $n$ more items. Rule 1.1 says that the total number of `onNext` calls must never exceed the total requested. A request of $n \le 0$ is an error (rule 3.9), and a demand of $2^{63} - 1$ may be read as "effectively unbounded" (rule 3.17), which turns backpressure off.
- **On and off.** The consumer sends "stop" when its buffer passes a high mark and "go" when it falls below a low mark (Dally and Towles, Section 13.3.2). The buffer above the high mark must absorb what is already in flight when "stop" arrives.

**Theorem 1 (no overflow).** In credit-based flow control, let $c$ be the credits at the producer, $f$ the items in flight to the consumer, $q$ the items in the consumer's buffer and $g$ the credits in flight back. If the producer starts with $B$ credits and an empty system, then $c + f + q + g = B$ at all times, so $q \le B$ and the buffer never overflows.

*Proof.* The four events keep the sum: a send moves one unit from $c$ to $f$, an arrival from $f$ to $q$, a consumption from $q$ to $g$, and a credit arrival from $g$ to $c$. The producer sends only when $c \ge 1$, so $c \ge 0$, and with $f, g \ge 0$ we get $q \le B$. The same argument with $f = g = 0$ covers a blocking queue, and with bytes in place of items it covers a window. $\square$

**Theorem 2 (the buffer limits the rate).** Let $T$ be the credit round trip: the least time from sending an item until the credit for its place is back at the producer. Then the producer sends at most $B \lceil \tau / T \rceil$ items in any interval of length $\tau$, so its long-term rate is at most $B / T$. To run a link of rate $\lambda$ at full speed, the buffer must hold at least $\lambda T$ items, the bandwidth-delay product.

*Proof.* Each send uses one credit. A credit used at time $s$ comes back no earlier than $s + T$, so in an interval of length $\tau$ each of the $B$ credits is used at most $\lceil \tau/T \rceil$ times. Divide by $\tau$ and let $\tau$ grow. $\square$

**Theorem 3 (the chain runs at the slowest stage).** Take a chain of stages with service rates $\mu_1, \ldots, \mu_k$, items per unit time, joined by buffers of sizes $B_1, \ldots, B_{k-1}$ with backpressure. Then the long-term rate of every stage is the same, and it is at most $\min_i \mu_i$.

*Proof.* Let $D_i(t)$ be the number of items that stage $i$ has finished by time $t$. Each item that stage $i+1$ finishes came from stage $i$, and the items that stage $i$ has finished and stage $i+1$ has not are in the buffer, in service at stage $i+1$, or held by stage $i$ while it is blocked, so $0 \le D_i(t) - D_{i+1}(t) \le B_i + 2$. Divided by $t$, the difference tends to 0, so all stages have the same long-term rate, and this rate is at most each $\mu_i$. $\square$

When the first stage always has work and the rates are constant, the rate is exactly $\min_i \mu_i$: the buffers in front of the slowest stage fill, and the stages before it block for the rest of the time. The slowdown moves up the chain one stage at a time, each time a buffer fills.

**What backpressure costs.** The producer must be able to wait. A source that cannot wait, such as a clock, a sensor or users who send requests, must still drop, sample or reject at some point; the Reactive Streams text says so for sources "whose production rate cannot be influenced". Backpressure moves the queue upstream, toward the place where the work enters, and that place then needs [admission control](/admission-control/), [load shedding](/load-shedding/) or [throttling](/throttling/).

**What backpressure is not.**

- **[Backpressure routing](/backpressure-routing/)** sends packets from long queues to short queues to maximize the throughput of a network. It does not stop anyone from sending.
- **[Congestion control](/congestion-control/)** protects the network between the two ends, and it learns about congestion from loss or delay. Flow control and backpressure protect the receiver, and the receiver tells the sender its free space.
- **[Load shedding](/load-shedding/)** and **[admission control](/admission-control/)** refuse work. Backpressure delays work and refuses nothing.
- **[Rate limiting](/rate-limiter/)** holds a client to a fixed rate even when the consumer is idle. Backpressure lets the producer run as fast as the consumer can take.

## Examples

**A fast producer.** A producer makes 100 items per second, a consumer takes 60, and the buffer holds 50. The buffer gains 40 items per second and is full after $50/40 = 1.25$ s. From then on the producer is blocked 40 percent of the time and runs at 60 items per second. An item waits in the buffer for at most $50/60 \approx 0.83$ s. With an unbounded buffer instead, the queue after 10 s has 400 items, a new item waits $400/60 \approx 6.7$ s, and both grow without bound.

**Credits on a link.** A link sends one item per time slot, and the credit round trip is $T = 4$ slots. With $B = 2$ credits the link runs at half speed, $2/4$ items per slot; with $B = 4$ or more it runs at full speed. With $T = 8$ and $B = 3$ the rate is $3/8$. A slot-by-slot simulation gives the same rates as Theorem 2.

**The TCP window.** Without window scaling the advertised window is at most 65,535 bytes. On a path with a round-trip time of 100 ms, the sender can then send at most $65{,}535/0.1 = 655{,}350$ bytes per second, about 5.24 Mbit/s, whatever the link speed. To fill 1 Gbit/s at 100 ms the window must be 12.5 MB, which needs the window scale option of RFC 7323.

**Demand in Reactive Streams.** A subscriber with room for 4 items calls `request(4)` at the start and `request(1)` after it processes each item. With $P$ the total requested and $N$ the number processed, $P - N = 4$ at all times, so at most 4 items can be on their way or waiting. A subscriber that calls `request(1)` only after each item gets stop-and-wait behavior, one item per round trip, as the specification notes.

**A pipeline.** Three stages with rates 100, 30 and 80 items per second, with bounded buffers between them, run at 30 items per second. The buffer in front of the second stage fills, and the first stage is blocked 70 percent of the time. The buffer after the second stage stays nearly empty.

## Where it is used

- **Operating systems.** Pipes, sockets and bounded queues block a writer when the buffer is full.
- **Transport protocols.** TCP flow control with the receive window, and the credits of the flow control of other transports.
- **Networks.** Credit-based flow control on ATM links and in on-chip and cluster interconnects. With hop-by-hop backpressure, a cycle of full buffers can deadlock, so these networks also need the deadlock avoidance of Dally and Towles, Chapter 14.
- **Stream processing and reactive libraries.** Reactive Streams, and the `java.util.concurrent.Flow` interfaces that follow it, carry demand from subscriber to publisher. Stream processors stop reading from their sources when downstream operators fall behind.
- **Services.** A service with bounded queues of work, a bounded pool of connections, or a limit on requests in progress pushes back on its callers. At the edge, where the callers are users who cannot wait, the push becomes a rejection, as in [admission control](/admission-control/).

## References
