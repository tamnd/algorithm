---
tag: JVHRRT
kind: technique
slug: event-driven-simulation
name: Event-driven simulation
area: techniques/sweep-line
level: core
summary: Simulation method that keeps events in a priority queue and jumps directly from one event time to the next.
prereqs: [priority-queue, binary-heap]
see_also: [collision-prediction-and-resolution, time-driven-simulation, hard-disk-model, event-queue, sweep-line-technique, kinetic-heap, lazy-deletion, calendar-queue]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 6.1, Event-driven simulation
  - paper: "B. J. Alder and T. E. Wainwright, Studies in molecular dynamics. I. General method, The Journal of Chemical Physics 31(2) (1959), doi:10.1063/1.1730376"
    locator: pages 459 to 466
  - paper: "B. D. Lubachevsky, How to simulate billiards and similar systems, Journal of Computational Physics 94(2) (1991), doi:10.1016/0021-9991(91)90222-7"
    locator: pages 255 to 283
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 4, Section 4.4 (Dijkstra's algorithm as a simulation with alarm clocks)
---

Event-driven simulation is a method that keeps the future events of a system in a [priority queue](/priority-queue/) keyed by time, takes the earliest one, moves the clock straight to its time, updates the state, and schedules the new events that the update causes. Nothing is computed between two events, so the cost depends on the number of events and not on the length of the simulated time. Events that an update makes wrong are invalidated, most often lazily, by checking them when they reach the front of the queue. The method is exact when the state between events has a closed form, as for hard disks ([collision prediction and resolution](/collision-prediction-and-resolution/)) and for queues of customers.

## In plain words

Think of a desk diary with alarms. You do not check the world every minute. You write down each thing that you know will happen, with its time. Then you jump to the earliest entry, do what it says, and cross it out. Doing it may cause new things to happen later, so you write those down too. Some old entries may now be wrong, for example a meeting that was moved. You do not search for them at once. When a wrong entry comes up, you see that it is out of date and skip it.

A simulation works this way when nothing interesting happens between the entries. A ball moves in a straight line until it hits something, and a bank clerk serves one customer until the service ends. So the program can jump from one entry to the next.

## When it applies

- The state changes only at discrete moments, or it changes between them in a way that has a closed form, such as motion in a straight line.
- From the current state you can compute the time of each next event, exactly or with a known bound.
- An event changes only a small part of the state, so it makes only a few new predictions and invalidates only a few old ones.
- Events are rare compared with the resolution in time that a fixed step would need. A [time-driven simulation](/time-driven-simulation/) would spend most of its steps on moments when nothing happens.

## The template

```pseudo id=main
EVENT-DRIVEN-SIMULATION(state, limit)
L1  Q ← an empty min-priority queue keyed by time, t ← 0
L2  for each e in INITIAL-EVENTS(state) do INSERT(Q, e)       ▷ hole
L3  while Q is not empty and MIN(Q).time ≤ limit do
L4      e ← EXTRACT-MIN(Q)
L5      if not VALID(state, e) then continue                  ▷ hole: lazy invalidation
L6      ADVANCE(state, e.time − t)                            ▷ hole: closed-form motion
L7      t ← e.time
L8      HANDLE(state, e)                                       ▷ hole: change the state
L9      for each e′ in PREDICT(state, e) do INSERT(Q, e′)      ▷ hole: new events, time ≥ t
L10 ADVANCE(state, limit − t)
```

The holes are:

- **INITIAL-EVENTS** gives the events known at the start: all first arrivals of customers, or the first contact of each pair of disks and each disk with each wall.
- **VALID** tells whether an event still describes the future. Sedgewick and Wayne store in each event the collision counts of its particles at the time of the prediction; the event is valid when the counts have not changed since. A version number or a time stamp of the last update does the same job.
- **ADVANCE** moves the state from the old time to the new one. For free motion this is $r \leftarrow r + \Delta t\, v$. For a queue it does nothing, or it adds the elapsed time to running totals such as the area under the queue length.
- **HANDLE** applies the event: a bounce, the start or the end of a service.
- **PREDICT** returns the events caused by the change. It looks only at the objects that HANDLE changed.

The loop keeps the invariant of each event-driven method: *every valid event in $Q$ is a true future event on the current state, and the next true event of the system is among the valid events in $Q$*. Then the first valid event that EXTRACT-MIN returns is the next event, and the jump of line L6 skips no event. The proof for hard disks is on the page of [collision prediction and resolution](/collision-prediction-and-resolution/).

**Cost.** Let $k$ be the number of events taken from the queue, and $q$ the largest size of the queue. With a [binary heap](/binary-heap/), each INSERT and EXTRACT-MIN costs $O(\log q)$. The total cost is the cost of the initial events, plus the cost of HANDLE and PREDICT summed over the valid events, plus $O(\log q)$ for each insertion and each extraction. For $n$ hard disks, Sedgewick and Wayne's version makes about $n^2/2$ distinct pair predictions at the start (each pair is predicted from both sides, so $n(n-1)$ entries, plus $2n$ wall events), and each collision makes $O(n)$ new predictions, so $O(n \log n)$ time for each event.

## Classic examples

### A bank with one teller

Customers arrive at known times and wait in one line for one teller. The events are *arrival* and *departure*. An arrival starts the service at once when the teller is free, else it joins the line. A departure starts the service of the next customer in line, if any, and schedules that customer's departure. No event is ever invalidated. Take arrivals at times 0, 1, 2, 6 and 7, with service times 3, 2, 1, 2 and 2, and process a departure before an arrival at the same time.

| time | event | action | line after |
|---|---|---|---|
| 0 | arrival 0 | serve 0 until 3 | empty |
| 1 | arrival 1 | wait | 1 |
| 2 | arrival 2 | wait | 1, 2 |
| 3 | departure 0 | serve 1 until 5 (waited 2) | 2 |
| 5 | departure 1 | serve 2 until 6 (waited 3) | empty |
| 6 | departure 2 | teller idle | empty |
| 6 | arrival 3 | serve 3 until 8 | empty |
| 7 | arrival 4 | wait | 4 |
| 8 | departure 3 | serve 4 until 10 (waited 1) | empty |
| 10 | departure 4 | teller idle | empty |

Ten events cover ten units of time, and the mean wait is $(0 + 2 + 3 + 0 + 1)/5 = 1.2$. With random exponential gaps between arrivals and exponential service times, this is the M/M/1 queue of queueing theory, and the same program estimates its mean wait. Here a departure can only be scheduled by the event that starts the service, so the queue never holds more than one departure.

### Hard disks

The [hard-disk model](/hard-disk-model/) is the example of Sedgewick and Wayne. The events are disk-disk and disk-wall contacts, computed by [collision prediction](/collision-prediction-and-resolution/). A collision changes the velocities of one or two disks, so every prediction about them becomes stale. This is one of the first uses of the method in science: Alder and Wainwright simulated hard spheres this way in 1959, and Lubachevsky in 1991 gave a scheme for billiards with many particles. Sedgewick and Wayne also put *redraw* events in the queue at regular times, so that a display gets frames at a fixed rate without changing the physics.

### A sweep is a simulation in time

A [sweep line](/sweep-line-technique/) is an event-driven simulation in which the $x$ coordinate plays the part of time. The [event queue](/event-queue/) holds the $x$ coordinates where the status changes, and the status is the state. In the [Bentley-Ottmann algorithm](/bentley-ottmann-algorithm/), handling an event can predict a new one, the intersection point of two segments that become neighbours, exactly as a collision predicts the next collision.

### Dijkstra's algorithm with alarm clocks

Dasgupta, Papadimitriou and Vazirani explain [Dijkstra's algorithm](/dijkstra/) as a simulation. Think of each edge as a pipe that takes its length in time to cross. Set an alarm for each vertex at the time a signal from the source can first reach it. When an alarm rings, the vertex is reached, and the alarms of its neighbours move earlier if the signal through it is faster. The priority queue of the algorithm is the set of alarms, and decrease-key replaces an alarm by an earlier one.

### Kinetic data structures

A [kinetic heap](/kinetic-heap/) keeps the maximum of points that move. Each parent-child pair has a *certificate*, "the parent is larger", that holds until a time that can be computed. The certificate failures are events in a queue; at each one the structure swaps two items and recomputes a few certificates, which is the PREDICT step.

## Variations

- **Lazy or eager invalidation.** The lazy form leaves stale events in the queue and tests them when they come out; the queue can then grow with the number of events. The eager form deletes or updates them at once, which needs an [indexed priority queue](/indexed-priority-queue/) with delete or decrease-key. A common eager scheme keeps only the earliest event of each object, so the queue has one entry per object.
- **The queue.** A [binary heap](/binary-heap/) is the default. A [calendar queue](/calendar-queue/), a bucket array over time, gives $O(1)$ average time per operation for many common distributions of the event times, but not in the worst case.
- **Locality.** Divide space into cells and add *cell-crossing* events, so that PREDICT looks only at nearby objects.
- **Parallel and distributed simulation.** Split the system into parts with their own queues and clocks. Conservative methods wait until no earlier message can arrive; optimistic methods run ahead and roll back. See [parallel discrete-event simulation](/parallel-discrete-event-simulation/).
- **Hybrid stepping.** Insert regular *sampling* events (the redraw events above) to measure or show the state at fixed times.

## Pitfalls

- **Stale events.** Without a validity test (line L5), an event computed from an old state is handled as if it were true, for example a collision between two disks that one of them has already left. Every change to an object must make its old events fail the test.
- **Events at equal times.** Two events can have the same time: a departure and an arrival at time 6 above, or three disks that touch at once. Fix a rule for ties, such as "departures first", and make it part of the key, or the result depends on the heap. A truly simultaneous contact of three disks has no unique physical outcome.
- **The cost of the start.** For $n$ interacting objects, INITIAL-EVENTS makes $\Theta(n^2)$ predictions and the queue holds $\Theta(n^2)$ entries, before a single event. With $n = 10{,}000$ disks there are $49{,}995{,}000$ pairs, and Sedgewick and Wayne's form predicts each pair from both sides. Cells cut it to $O(n)$ at a bounded density.
- **Growth of the queue.** Each collision inserts $O(n)$ events and lazy deletion removes none of the stale ones before they come out. Over a long run the queue holds far more stale events than valid ones. Rebuild it from scratch from time to time, or use eager invalidation.
- **Floating time.** Store absolute event times, not delays. A prediction computed by rounding can be a tiny bit earlier than the current time $t$; clamp it to $t$, or the clock runs backwards. Do not compare times for exact equality to detect simultaneous events.
- **Infinitely many events.** A model can produce infinitely many events in a finite time, as a ball under gravity that bounces on a floor with a coefficient of restitution below 1 does: the times between bounces form a geometric series with a finite sum. The loop of line L3 then never passes that time. Add a rule, such as "a bounce slower than a threshold makes the ball rest".

## Exercises

1. Modify the bank example for two tellers and one line. Process the same arrivals and service times, and give the waits.
2. For the bank, prove that the queue never holds more than one departure event for each teller, so no event is ever stale.
3. Show that in the hard-disk simulation with lazy deletion, the queue can hold $\Theta(n^2 + kn)$ entries after $k$ collisions, and give a scheme with $O(n)$ entries.
4. Write the kinetic heap of four points with linear motion $x_i(t) = a_i + b_i t$ as an event-driven simulation: what are the events, and how many certificates does one swap change?
5. In Dijkstra's algorithm as an alarm-clock simulation, which step corresponds to the validity test of line L5 when the heap has no decrease-key and you insert a new alarm instead?

## References
