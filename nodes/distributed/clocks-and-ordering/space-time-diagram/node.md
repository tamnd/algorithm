---
tag: MAPPCM
kind: concept
slug: space-time-diagram
name: Space-time diagram
aliases:
- Lamport diagram
- process-time diagram
area: distributed/clocks-and-ordering
level: intro
summary: A drawing of a distributed run with one time line per process, a dot per event and an arrow per message. Happened-before is a path in it, and concurrent events have no path between them.
prereqs: [asynchronous-model]
see_also: [happened-before, concurrent-events, consistent-cut, lamport-clocks, vector-clocks, causal-ordering, directed-acyclic-graph, global-snapshot]
sources:
  - paper: doi:10.1145/359545.359563
    title: Leslie Lamport, Time, clocks, and the ordering of events in a distributed system, Communications of the ACM 21(7), 1978
    locator: pages 558 to 565, section The Partial Ordering (the space-time diagram of Figure 1)
  - paper: "Friedemann Mattern, Virtual time and global states of distributed systems, in M. Cosnard et al. (eds.), Parallel and Distributed Algorithms, North-Holland, 1989"
    title: Friedemann Mattern, Virtual time and global states of distributed systems, Parallel and Distributed Algorithms, North-Holland, 1989
    locator: pages 215 to 226 (time diagrams, cuts and the rubber band transformation)
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 2 (a model of distributed executions and the space-time diagram)
---

A space-time diagram draws one run of a distributed system. Each process gets a time line, each event is a dot on the line of its process, and each message is an arrow from its send event to its receive event. Lamport used such diagrams in 1978 to define [happened-before](/happened-before/): one event happened before another exactly when a path in the diagram leads from the first to the second, along time lines and message arrows. The diagram shows only the order of events, not the real times at which they happened.

## In plain words

Draw a line for each computer, with time going from left to right. Put a dot on a computer's line each time it does something. When a computer sends a message, draw an arrow from the dot of the send to the dot where the other computer receives it.

Now you can see cause and effect with your finger. If you can walk from one dot to another, moving right along lines and following arrows, the first dot could have influenced the second. If you cannot walk either way, the two dots could not have influenced each other, and they are called concurrent.

The lengths in the picture mean nothing. You can stretch the lines like rubber, and as long as no arrow turns backwards, the picture describes the same run.

## The idea

A run in the [asynchronous model](/asynchronous-model/) is a set of events at $n$ processes. The events of one process are totally ordered by its local history, and each receive event matches one send event. The space-time diagram draws exactly this data:

- a horizontal line for each process $P_i$, with time growing to the right;
- a dot on line $P_i$ for each event of $P_i$, in the order of its local history;
- an arrow from each send event to the matching receive event.

The diagram is a [directed acyclic graph](/directed-acyclic-graph/) once the segments of each time line are read as edges that point to the right. Its reachability relation is the happened-before relation $\to$: $e \to f$ if and only if there is a directed path from $e$ to $f$. Two distinct events with no path in either direction are [concurrent](/concurrent-events/).

Only the order matters. Mattern calls this the *rubber band transformation*: moving dots along their lines, while every arrow still points forward in time, gives a diagram of the same run, with the same happened-before relation. In particular, the run can always be drawn so that two chosen concurrent events appear at the same vertical position, or in either order. So a diagram shows what *could* have influenced what, and nothing about simultaneity.

A *cut* is a line that crosses each process line once and splits the events into a past and a future. The cut is a [consistent cut](/consistent-cut/) if no arrow goes from the future to the past. Once the diagram is stretched, every consistent cut can be drawn as a vertical line. [Global snapshot](/global-snapshot/) algorithms record the state at such a cut.

## Examples

**The running example.** This run has three processes and seven events. It is used on several pages of this area.

```
P1   a-----------b------------>
      \
       \
P2   c--d--------e------------>
                  \
                   \
P3   f--------------g--------->
```

- $P_1$: $a$ sends a message to $P_2$, then $b$ is a local event.
- $P_2$: $c$ is local, $d$ receives the message of $a$, $e$ sends a message to $P_3$.
- $P_3$: $f$ is local, $g$ receives the message of $e$.

Paths give 11 ordered pairs: $a \to b$, $a \to d$, $a \to e$, $a \to g$, $c \to d$, $c \to e$, $c \to g$, $d \to e$, $d \to g$, $e \to g$ and $f \to g$. The other 10 of the 21 pairs are concurrent, for example $b \parallel e$: nothing leaves $P_1$ after $b$, and no path reaches $b$ from $P_2$. A script that enumerates all orders confirms that 52 total orders of the seven events agree with all 11 pairs, and that 22 of the $3 \cdot 4 \cdot 3 = 36$ cuts (one prefix of each time line, the empty prefix included) are consistent.

**Clock values on the diagram.** Writing [Lamport clock](/lamport-clocks/) values next to the dots gives $a = 1$, $b = 2$, $c = 1$, $d = 2$, $e = 3$, $f = 1$, $g = 4$. Writing [vector clock](/vector-clocks/) values gives $a = (1,0,0)$, $b = (2,0,0)$, $c = (0,1,0)$, $d = (1,2,0)$, $e = (1,3,0)$, $f = (0,0,1)$ and $g = (1,3,2)$. The vector of an event counts, per process, the dots that can reach it.

**A non-example.** A drawing in which arrows and time lines form a directed cycle is not the diagram of any run, because it would make an event happen before itself. Each receive must come after its send in some stretching of the lines, and a cycle makes that impossible.

**An inconsistent cut.** A cut that contains $d$ but not $a$ is inconsistent: the arrow from $a$ to $d$ crosses it from the future into the past, so the cut records a message as received but never sent.

## Where it is used

- **Defining causality.** Lamport introduced happened-before with space-time diagrams, and textbooks use them to explain [Lamport clocks](/lamport-clocks/), [vector clocks](/vector-clocks/) and [causal ordering](/causal-ordering/).
- **Cuts and snapshots.** Consistent cuts, global states and snapshot algorithms such as the [Chandy-Lamport algorithm](/chandy-lamport-snapshot/) are explained by drawing cuts on these diagrams.
- **Message ordering.** Violations of FIFO or causal order appear as crossing arrows: two arrows from one sender that cross at the receiver break [FIFO ordering](/fifo-ordering/).
- **Debugging.** Tools that collect logs with vector timestamps can draw the run as a space-time diagram, so a developer can see which events could have influenced a failure.

## References
