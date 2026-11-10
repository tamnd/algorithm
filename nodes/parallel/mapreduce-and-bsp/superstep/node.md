---
tag: 1C796A
kind: concept
slug: superstep
name: Superstep
aliases:
- BSP superstep
- computation superstep
area: parallel/mapreduce-and-bsp
level: core
summary: 'The unit of a BSP program: local computation, then communication, then a barrier. Messages sent in one superstep are read in the next.'
prereqs: [bsp-model, barrier-synchronization]
see_also: [h-relation, pregel-model, mapreduce-model, synchronizer, all-prefix-sums]
sources:
  - paper: doi:10.1145/79173.79181
    title: "Leslie G. Valiant, A bridging model for parallel computation, Communications of the ACM 33(8), 1990"
    locator: pp. 103-111, the computation as a sequence of supersteps
  - book: isbn:9780198529392
    title: "Rob H. Bisseling, Parallel Scientific Computation: A Structured Approach using BSP and MPI, Oxford University Press, 2004"
    locator: Chapter 1, computation and communication supersteps and their cost
  - paper: doi:10.1145/1807167.1807184
    title: "Grzegorz Malewicz, Matthew H. Austern, Aart J. C. Bik, James C. Dehnert, Ilan Horn, Naty Leiser and Grzegorz Czajkowski, Pregel: a system for large-scale graph processing, SIGMOD 2010"
    locator: pp. 135-146, Section 2 (supersteps, and messages sent in superstep S that arrive in superstep S + 1)
---

A superstep is the unit of execution of a [bulk synchronous parallel](/bsp-model/) program. In a superstep every processor computes on its own data and sends messages, and then all processors meet at a [barrier](/barrier-synchronization/). A message sent in one superstep can be read only in the next one. A superstep with local work $w$ and an [h-relation](/h-relation/) of size $h$ costs $w + g\,h + L$.

## In plain words

Think of a class that works in rounds. In each round every student works alone with the papers on their own desk, and puts notes into the mailboxes of other students. Nobody reads a note during the round. When everybody has finished, the teacher rings a bell, all notes are delivered at once, and the next round starts. A student never waits for one particular note, only for the bell. So the students cannot get stuck waiting for each other, and the order in which they work during a round does not matter. The price is the bell: each round costs a fixed amount of time, even when there was little to do. Good programs use few rounds and send few notes.

## The idea

A superstep $s$ of a program on $p$ processors has three phases.

1. **Local computation.** Processor $i$ runs code that reads and writes only its local memory, including the messages that it received at the end of superstep $s - 1$. It does $w_s^{(i)}$ operations.
2. **Communication.** Processor $i$ sends messages. They are buffered, and no receiver sees them in superstep $s$.
3. **Barrier.** No processor starts superstep $s + 1$ before all have finished superstep $s$. After the barrier all messages of superstep $s$ are in the receivers' memories.

In the BSP cost model the superstep costs

$$
T_s = w_s + g\,h_s + L, \qquad w_s = \max_i w_s^{(i)},
$$

where $h_s$ is the largest number of words that one processor sends or receives (the [h-relation](/h-relation/)), $g$ is the cost of routing one word and $L$ is the cost of the barrier. A program of $S$ supersteps costs $W + gH + SL$, with $W$ and $H$ the sums of $w_s$ and $h_s$.

The superstep gives three properties that make parallel programs easier to reason about.

- **No races on messages.** A processor reads only messages from the previous superstep, which are complete and cannot change. Within a superstep, the processors do not share any data that one of them writes.
- **No communication deadlock.** A processor never waits for a particular message, only for the barrier. If every processor reaches the end of each superstep, the program makes progress.
- **Timing does not change the result.** Assume that the local computation of each processor is deterministic and does not depend on the order in which its messages arrived (for example, the code sorts its inbox by sender first). Then the state after each superstep is a function of the state before it, whatever the speeds of the processors and of the network.

Because the barrier cost $L$ is paid once per superstep, the main design rule is to put independent communication into one superstep. A message that waits until the next superstep costs nothing extra; a superstep with nothing to send still costs $L$.

## Examples

**Delivery at the barrier.** Three processors each send their own number to the next processor in a ring, in superstep 1. During superstep 1 all inboxes are empty. In superstep 2 processor $0$ reads the word of processor $2$, processor $1$ reads the word of processor $0$, and processor $2$ reads the word of processor $1$. Each superstep has $w = 1$ and $h = 1$; with $g = 3$ and $L = 10$ the two supersteps cost $2(1 + 3 + 10) = 28$.

**Two supersteps for prefix sums.** In the [BSP prefix sums](/bsp-model/) algorithm, superstep 1 computes local [prefix sums](/all-prefix-sums/) and sends each block total to the later processors ($h = p - 1$); superstep 2 adds the received totals. The second step needs data from the first, so it cannot share its superstep.

**Packing independent reductions.** Each of $p$ processors holds $k$ numbers $a_{i,1}, \ldots, a_{i,k}$, and every processor needs the $k$ sums $\sum_i a_{i,t}$. A reduction by total exchange sends each value to all other processors and adds locally: $h = p - 1$ for one sum. Doing the $k$ sums one after another costs $k\left((p - 1)g + L\right)$ plus the additions. Sending all $k$ values in one superstep gives $h = k(p - 1)$ and costs $k(p - 1)g + L$. For $p = 8$, $k = 10$, $g = 4$ and $L = 100$ the communication cost drops from $1280$ to $380$.

**A non-example.** A program in which processor $0$ sends a request, processor $1$ answers it, and processor $0$ uses the answer, all inside one superstep, is not a BSP program: the answer would only arrive in the next superstep. In BSP this exchange takes two supersteps, and the cost $2L$ shows the round trip in the analysis.

## Where it is used

- BSP algorithms and libraries. The BSP model of Valiant and the textbook of Bisseling structure every algorithm as a sequence of supersteps and analyse each one by its $w$, $h$ and $L$.
- Graph processing. A [Pregel](/pregel-model/) program is a sequence of supersteps in which each vertex runs a function, and messages sent in superstep $S$ arrive in superstep $S + 1$. The [GAS model](/gas-model/) in its synchronous mode works the same way.
- [MapReduce](/mapreduce-model/). Each round is a superstep in which the map and reduce functions are the local work and the [shuffle](/shuffle-phase/) is the communication. The [MRC model](/mrc-model/) counts these rounds.
- Distributed algorithms. A [synchronizer](/synchronizer/) builds the round structure of a synchronous network on top of an asynchronous one, which is the superstep idea in the message-passing setting.

## References
