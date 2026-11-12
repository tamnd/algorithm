---
tag: 48CY61
kind: concept
slug: time-triggered-scheduling
name: Time-triggered scheduling
area: systems/scheduling
level: advanced
summary: "Every task and every message of a distributed system starts at a fixed instant of a synchronized global clock, from a table built offline. Events do not trigger work; time does."
prereqs: [cyclic-executive, clock-synchronization]
see_also: [cyclic-executive, clock-synchronization, hyperperiod, fixed-priority-scheduling, real-time-scheduling, pinwheel-scheduling, periodic-task-model, schedulability-analysis]
sources:
  - book: isbn:9781441982377
    title: "Hermann Kopetz, Real-Time Systems: Design Principles for Distributed Embedded Applications, second edition, Springer, 2011"
    locator: Chapter 10 (real-time scheduling), Section 10.3 (static scheduling); the chapters on global time and on time-triggered communication
  - paper: doi:10.1109/JPROC.2002.805821
    title: "Hermann Kopetz and Günther Bauer, The time-triggered architecture, Proceedings of the IEEE 91(1) (2003), 112-126"
    locator: the global time base, the TDMA communication, the temporal firewalls and composability
  - paper: doi:10.1007/BF02341919
    title: "Theodore P. Baker and Alan Shaw, The cyclic executive model and Ada, Real-Time Systems 1(1) (1989), 7-25"
    locator: the single-processor static table that time-triggered systems extend
---

Time-triggered scheduling runs every task and sends every message of a distributed real-time system at a fixed instant of a global time base. The instants come from a table that is built and checked before the system runs, and the table repeats in a cycle; at run time a node only reads its clock and its table. It is the [cyclic executive](/cyclic-executive/) carried over to many nodes and a shared network, held together by [clock synchronization](/clock-synchronization/). Its opposite is event-triggered scheduling, in which the arrival of an event starts the work.

## In plain words

A train timetable says that the 8:15 train leaves platform 2 at 8:15, every day, whether five people are waiting or five hundred. The connecting bus leaves at 8:40, because the timetable knows that the train arrives at 8:32. Nobody phones the bus driver. All clocks show the same time, and each person follows the timetable.

A time-triggered system works like this. Each computer in a car or an aircraft has a copy of its timetable. At 3 milliseconds into each cycle it reads a sensor, and at 5 milliseconds it sends the value on the network. The network knows which computer may talk at each moment. Nobody asks for a turn, so nobody can talk over another, and every delay is known before the system is switched on.

## The idea

**The model.** The system has several nodes connected by a bus or a switched network. The work is a set of periodic tasks and periodic messages with fixed periods, worst-case execution and transmission times, and precedence: a sensor task produces a message that a control task needs. The schedule is a table of start instants for all tasks and all message slots, over a cluster cycle that is a common multiple of the periods, usually their [hyperperiod](/hyperperiod/). The schedulability test is the construction and offline check of the table: for that table, it is exact, as every instant is known.

**Global time.** All nodes keep clocks that a fault-tolerant [clock synchronization](/clock-synchronization/) algorithm holds within a precision $\Pi$ of each other. An action that the table puts at time $t$ starts on each node at a local time within $\Pi$ of $t$. Two actions that must not overlap therefore need a gap of at least $\Pi$, and the table adds this guard time around each slot. Kopetz uses a sparse time base: events of interest happen only at the ticks of a coarse grid, so all nodes agree on the order of any two events.

**Communication by time slots.** Access to the bus is time-division multiple access: each node owns fixed slots in a round, and only that node may send in them. No arbitration happens at run time, so a message has a fixed delay. A bus guardian closes the access of a node outside its own slots, so a faulty node that sends at random cannot block the others.

**Building the table.** The table must place each task inside its period and after the messages it needs, and each message in a slot after its producer and before its consumer, on every node at once. This is a search over start times with precedence and resource constraints. It contains the single-processor table of the cyclic executive, so it is NP-hard in general, and tools solve it with heuristics, constraint solvers or integer programming.

**Time-triggered compared with event-triggered.**

| question | time-triggered | event-triggered |
|---|---|---|
| what starts an action | a tick of the global clock | the arrival of an event or a message |
| load on the network | constant, the same in each cycle | depends on the events, can peak |
| delay and jitter | fixed, near zero jitter | vary with the load |
| analysis | read from the table | a [schedulability analysis](/schedulability-analysis/) of worst cases |
| change | a new table for the cluster | often local |
| rare events | must be polled in each cycle | handled when they come |

**Composability.** The interfaces between subsystems are fixed in time, not only in value. A subsystem that meets its slots behaves the same when other subsystems are added, so subsystems can be built and tested apart and then put together. Kopetz calls these fixed interfaces temporal firewalls.

## Examples

**A control loop over two nodes.** The cluster cycle is 10 ms, and the precision of the clocks is $\Pi = 0.2$ ms, so each guard gap is 0.5 ms. Node A reads a sensor and drives an actuator. Node B computes the control law.

| time in the cycle (ms) | node A | bus | node B |
|---|---|---|---|
| 0.0 to 2.0 | read the sensor | | |
| 2.5 to 3.0 | | slot of A: sensor value | |
| 3.5 to 6.0 | | | compute the control |
| 6.5 to 7.0 | | slot of B: actuator command | |
| 7.5 to 8.5 | drive the actuator | | |

The delay from the sensor to the actuator is 8.5 ms in each cycle, with no jitter beyond the precision of the clocks. A failure is also easy to see: if the slot of B is empty at 6.5 ms, node A knows at once that something is wrong, with no timeout to choose.

**Single processor.** With one node and no network, the table is a cyclic executive, and the frame constraints of that page apply.

## Where it is used

- **Fieldbuses and networks.** The time-triggered protocol TTP, the static segment of FlexRay in cars, TTEthernet, and the time-aware shaper of the IEEE time-sensitive networking standards all send frames in slots of a global schedule.
- **Avionics.** Integrated modular avionics after ARINC 653 gives each partition fixed time windows in a major frame, which is a time-triggered schedule at the level of partitions.
- **Safety-critical control.** Brake-by-wire, steer-by-wire and engine control use time-triggered designs where a fixed delay and a certified table matter more than flexibility.

## References
