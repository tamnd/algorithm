---
tag: CC55PY
kind: problem
slug: termination-detection
name: Termination detection
aliases:
- distributed termination detection
- diffusing computation termination
- quiescence detection
area: distributed/distributed-graph-algorithms
level: core
summary: Detect that every process is passive and no message is in transit. Methods use trees, waves, weights or snapshots; in the worst case they need one control message per basic message.
prereqs: [asynchronous-model, consistent-cut, global-snapshot, echo-algorithm]
see_also: [dijkstra-scholten, chandy-lamport-snapshot, global-snapshot, consistent-cut, lai-yang-snapshot, distributed-predicate-detection, echo-algorithm, global-virtual-time]
sources:
  - paper: doi:10.1016/0020-0190(80)90021-6
    title: Edsger W. Dijkstra and Carel S. Scholten, Termination detection for diffusing computations, Information Processing Letters 11(1), 1-4, 1980
    locator: diffusing computations and their termination detection with deficit counters
  - paper: doi:10.1007/BF01782776
    title: Friedemann Mattern, Algorithms for distributed termination detection, Distributed Computing 2(3), 161-175, 1987
    locator: the four-counter method, the channel counting and vector counting methods, and the role of consistent time cuts
  - paper: doi:10.1016/0020-0190(89)90212-3
    title: Friedemann Mattern, Global quiescence detection based on credit distribution and recovery, Information Processing Letters 30(4), 195-200, 1989
    locator: the credit (weight) method
  - paper: doi:10.1109/ICDCS.1989.37933
    title: Shing-Tsaan Huang, Detecting termination of distributed computations by external agents, Proceedings of the 9th International Conference on Distributed Computing Systems, 79-84, 1989
    locator: the weight throwing method with a controlling agent
  - paper: doi:10.1007/BF01843569
    title: K. Mani Chandy and Jayadev Misra, How processes learn, Distributed Computing 1(1), 40-52, 1986
    locator: the lower bound on the number of control messages for termination detection
  - book: isbn:9780521794831
    title: Gerard Tel, Introduction to Distributed Algorithms, second edition, Cambridge University Press, 2000
    locator: Chapter 8 (termination detection, the computation model, lower bounds, tree, wave and credit based solutions)
---

Termination detection asks a distributed system to find out that a computation has ended. A process can see that it is itself idle, but not that the others are, and not that a message is on its way that will wake one of them up. The computation has *terminated* when every process is passive and no message of the computation is in transit; once that holds, it holds for ever, so it is a *stable property*. A detection algorithm runs beside the computation, sends its own *control* messages, and must announce termination only after it has happened (safety) and some time after it has happened (liveness). The classic solutions build a tree of active processes ([Dijkstra-Scholten](/dijkstra-scholten/)), count messages in waves (the four-counter method), return weights to a controller (weight throwing), or take [snapshots](/global-snapshot/). In the worst case each of them needs as many control messages as the computation sends. This page is about the problem and compares the methods; the page on [Dijkstra-Scholten](/dijkstra-scholten/) gives one method in full, with its proof.

## In plain words

A group of people pass work items to each other by post. Each person works on an item, may post new items to others, and then waits. The job is done only when nobody is working and no item is still in the post.

The hard part is the post. You can phone everyone and hear "I am idle" from all, but a letter may still be on its way that will start someone again.

So the group needs extra notes, such as "I got your item", or counts of items sent and received, to be sure the job is really over. In the worst case, they need one extra note for each work item.

## Definition

**Model.** An [asynchronous](/asynchronous-model/) network of $n$ processes on a connected graph with $m$ channels and diameter $D$. Channels are reliable and need not be FIFO, unless a method says so. There are no failures. Processes may have identifiers; one process, or an outside observer, makes the announcement.

**Basic computation.** Each process is *active* or *passive*. An active process can send *basic messages* and can become passive at any time. A passive process becomes active only when it receives a basic message, and sends nothing while passive.

**Termination.** The computation has terminated at time $t$ if at $t$ every process is passive and no basic message is in transit. This predicate is stable: no event of the computation can make it false once it is true.

**Task.** Add control messages and local steps, without changing the basic computation, so that some process eventually announces termination (liveness), and no process announces it before the computation has terminated (safety).

**Costs.** The number of control messages, often compared with the number $B$ of basic messages; the *detection delay* from termination to announcement; and the memory per process.

## Variants

- **Diffusing computations.** One process starts active and all others passive. This allows the tree method of [Dijkstra-Scholten](/dijkstra-scholten/).
- **General computations.** Any set of processes is active at the start. Methods must cover the whole network, for example with waves.
- **Synchronous or atomic models.** If messages take no time, or delivery is atomic, termination means "all passive", which a single wave can check. Real networks need the message accounting.
- **Topology.** Rings, trees and general graphs give different wave costs; the token ring method of Dijkstra, Feijen and van Gasteren (1983) works on a ring.
- **Faulty networks.** With crash failures, termination of the surviving processes is defined and detected with failure detectors; this needs other methods.
- **Quiescence and deadlock.** Related stable properties, detected by the same means; see [predicate detection](/distributed-predicate-detection/).

## Examples

**Why "all passive" is not enough.** Process $p$ sends a basic message to $q$ and becomes passive. A controller asks $q$, which is passive, and then $p$, which is passive too. Both answer "passive", but the message is still in transit and will wake $q$. A detector that only asks for states announces too early.

**Why one wave of counts is not enough.** Each process also reports how many basic messages it has sent and received so far. Take three processes $p$, $q$, $r$, a wave that visits them in that order, and a start with $r$ active and $p$, $q$ passive.

1. The wave visits $p$: passive, sent 0, received 0.
2. $r$ sends $m_1$ to $p$ and becomes passive.
3. $p$ receives $m_1$, sends $m_2$ to $q$ and $m_3$ to $r$, and becomes passive.
4. $q$ receives $m_2$ and becomes passive.
5. The wave visits $q$: passive, sent 0, received 1.
6. The wave visits $r$: passive, sent 1, received 0.

The wave sums to 1 sent and 1 received, and every process was passive when visited, but $m_3$ is still in transit and will wake $r$. The send of $m_1$ is counted without its receipt and the receipt of $m_2$ without its send, so the two errors cancel. The counts were read at different times and do not describe a [consistent cut](/consistent-cut/). A second wave sees $p$ with 2 sent and 1 received, so the four-counter test below does not announce.

**Dijkstra-Scholten on three nodes.** The [Dijkstra-Scholten page](/dijkstra-scholten/) traces a run with three basic messages and three signals.

## Known algorithms

| method | setting | control messages | delay after termination |
|---|---|---|---|
| [Dijkstra-Scholten](/dijkstra-scholten/) (1980) | diffusing, any graph | exactly $B$ | $O(h)$, $h$ the height of the engagement tree |
| Shavit-Francez (1986) | several initiators | $B$ plus waves | $O(n)$ per wave |
| token ring of Dijkstra, Feijen, van Gasteren (1983) | ring, atomic or counted messages | $O(n)$ per round of the token | $O(n)$ |
| four-counter method (Mattern 1987) | any graph, waves | $O(n)$ or $O(m)$ per wave, unbounded number of waves while the computation runs | two waves |
| channel or vector counting (Mattern 1987) | any graph | counters carried by a circulating token | one round of the token |
| weight throwing (Mattern 1989, Huang 1989) | a controller, any graph | at most one return message per activation | one message delay |
| snapshots ([Chandy-Lamport](/chandy-lamport-snapshot/), [Lai-Yang](/lai-yang-snapshot/)) | any computation | $O(m)$ per snapshot | one snapshot |

**The four-counter method.** The detector runs a wave, for example a [convergecast](/convergecast/) on a tree, that sums the counts of basic messages sent ($S$) and received ($R$) as each process reports them, and checks that every process is passive when visited. When the first wave ends, at time $t_1$, it runs a second wave, which gets the sums $S'$ and $R'$. It announces if every process was passive in the first wave and $R = S'$ (Mattern 1987). Proof of safety: write $S(t_1)$ and $R(t_1)$ for the true totals at $t_1$. Counts only grow, the first wave reads each process before $t_1$ and the second after $t_1$, and a message is received only after it is sent, so $R \le R(t_1) \le S(t_1) \le S'$. If $R = S'$, all are equal: no message is in transit at $t_1$, and no process received a message between its first visit and $t_1$, so each process is still passive at $t_1$. The computation has terminated at $t_1$. The example above fails the test, since $R = 1$ and $S' = 3$.

**Weight throwing (sketch).** The controller starts with weight 1. A message carries part of its sender's weight, and a process that becomes passive returns all its weight to the controller. Weight is never created or lost, so the controller holds weight 1 exactly when no process and no message holds any, which is termination. With exact arithmetic on powers of 2 there is no rounding; with finite precision, the weights must be split carefully or borrowed from the controller.

**Snapshots.** A [global snapshot](/global-snapshot/) records process states and channel contents on a consistent cut. Termination is stable, so if the snapshot shows all processes passive and all channels empty, the computation has terminated. Repeated snapshots detect it after it happens.

## Bounds

**Control messages (cited).** Chandy and Misra (1986) prove that every termination detection algorithm, in the worst case, sends at least as many control messages as the computation sends basic messages: for every algorithm there is a computation with $B$ basic messages on which it sends at least $B$ control messages. Dijkstra-Scholten meets this bound exactly, with one signal per basic message. The bound concerns the worst case; methods such as weight throwing pay per activation and not per message, and can do better on computations that send many messages per activation.

**Delay (sketch).** With delays of at most one unit, the last process to become passive may be any process, and the fact reaches the announcing process only through a chain of messages. So in the worst case the delay is at least the distance between them, up to $D$. Dijkstra-Scholten announces within $h + 1$ units, where $h$ is the height of its tree; wave methods need one or two full waves.

## Reductions

- **Termination detection and snapshots.** A [snapshot](/global-snapshot/) algorithm with a check of "all passive and all channels empty" detects termination; conversely, termination detection is the detection of one stable predicate, the general task solved by snapshots.
- **Acknowledged broadcast.** The [echo algorithm](/echo-algorithm/) is Dijkstra-Scholten applied to the diffusing computation "flood a message".
- **Garbage collection.** Detecting that an object is unreachable is a termination detection problem for the computation that holds references, and many collectors reuse the same algorithms.
- **Global virtual time.** In optimistic simulation, [GVT](/global-virtual-time/) computation needs the minimum time stamp of messages in transit, which uses the same message accounting.

## Applications

- **Ending phases of distributed algorithms.** An asynchronous algorithm, such as the Bellman-Ford form of [distributed BFS](/breadth-first-search-distributed/), runs until quiet; a termination detector tells the root that the phase is over.
- **Parallel search and graph processing.** Work stealing and asynchronous graph systems must know when no work remains anywhere.
- **Distributed garbage collection** and the release of resources after a distributed job.
- **Simulation.** Detecting the end of a distributed discrete event simulation.

## References
