---
tag: D5ET3Q
kind: model
slug: kahn-process-network
name: Kahn process network
aliases:
- KPN
- Kahn network
area: eda/high-level-synthesis-and-scheduling
level: core
summary: Kahn's model of deterministic processes that talk through unbounded FIFO channels with blocking reads, so the output depends only on the input, not the schedule.
prereqs: [queue, kleene-fixed-point-theorem]
see_also: [synchronous-dataflow, sdf-static-scheduling, fixed-point, knaster-tarski-theorem, halting-problem, undecidability, latency-insensitive-design, deadlock]
sources:
  - paper: "Gilles Kahn, The semantics of a simple language for parallel programming, Information Processing 74, Proceedings of the IFIP Congress 74, North-Holland, 471 to 475, 1974"
    title: Gilles Kahn, The semantics of a simple language for parallel programming, Information Processing 74, Proceedings of the IFIP Congress 74, North-Holland, 471 to 475, 1974
    locator: the language of processes and channels, streams ordered by prefix, processes as continuous functions, and the network as the least fixed point of its equations
  - paper: "Gilles Kahn and David B. MacQueen, Coroutines and networks of parallel processes, Information Processing 77, Proceedings of the IFIP Congress 77, North-Holland, 993 to 998, 1977"
    title: Gilles Kahn and David B. MacQueen, Coroutines and networks of parallel processes, Information Processing 77, North-Holland, 993 to 998, 1977
    locator: an operational implementation of the networks with coroutines and demand-driven scheduling
  - paper: "Thomas M. Parks, Bounded Scheduling of Process Networks, PhD thesis, University of California, Berkeley, Technical Report UCB/ERL M95/105, 1995"
    title: Thomas M. Parks, Bounded Scheduling of Process Networks, PhD thesis, University of California, Berkeley, 1995
    locator: the undecidability of termination and of bounded buffering for Kahn networks, and a scheduling policy that runs in bounded memory whenever that is possible
  - paper: "Edward A. Lee and Thomas M. Parks, Dataflow process networks, Proceedings of the IEEE 83(5), 773 to 801, 1995"
    title: Edward A. Lee and Thomas M. Parks, Dataflow process networks, Proceedings of the IEEE 83(5), 773 to 801, 1995
    locator: the place of Kahn networks among the dataflow models, and dataflow actors with firing rules as Kahn processes
---

A Kahn process network is a set of sequential processes that communicate only through FIFO channels. Each channel has one writer and one reader, holds any number of values, and is read with a blocking read: a process that wants a value from an empty channel waits until one arrives. A process may not test whether a channel is empty, and it may not wait on two channels at once. Gilles Kahn defined the model in 1974 and proved that it is determinate: for a given input, the sequence of values that passes through every channel is the same in every run, whatever order the processes run in. This page defines the model and proves determinacy and the undecidability of termination and of bounded memory. [Synchronous dataflow](/synchronous-dataflow/) is the special case with fixed rates, in which those questions become decidable.

## The machine

A network has processes $P_1, \ldots, P_m$ and channels. Each channel is a [queue](/queue/) of values from a set $A$ with exactly one writer and exactly one reader. A channel whose writer is the environment is an input of the network, and a channel whose reader is the environment is an output.

Each process is a deterministic sequential program with local memory. One step of a process is one of three actions:

- **Write** a value to one of its output channels. Channels have no bound, so a write never waits.
- **Read** from one of its input channels. Which channel is read next is fixed by the local state, not by the contents of the channels. If that channel is empty, the process is blocked and takes no step until a value arrives.
- **Compute** on the local memory.

A run is a sequence of steps, each by some process that is not blocked. A run is fair when no process stays able to move forever without moving, and the environment supplies all of its input. The scheduler is free; a single processor that runs the processes as coroutines and a network of processors are both runs of the model.

The history of a channel in a run is the sequence of all values written to it. Histories are finite or infinite sequences in $S = A^* \cup A^\omega$, ordered by prefix: $x \sqsubseteq y$ when $x$ is a prefix of $y$. The empty sequence is the least element, and every increasing chain $x_0 \sqsubseteq x_1 \sqsubseteq \cdots$ has a least upper bound, its limit. Vectors of histories are ordered entry by entry.

## What it counts

- **Histories.** The values that pass through each channel. Determinacy says that they depend only on the input.
- **Memory.** The largest number of values that a channel holds at one time in a run. Unlike the histories, this depends on the schedule.
- **Termination.** Whether all processes eventually halt or block forever.

Time and the cost of a step play no part in the theorems. A process network is a model of what a parallel program computes; the cost model comes from the scheduler that runs it.

## Relation to other models

- **Dataflow.** An actor with a fixed rate, as in [synchronous dataflow](/synchronous-dataflow/), is a Kahn process that reads a fixed number of values from each input and then writes a fixed number to each output. Lee and Parks (1995) describe dataflow actors with firing rules as Kahn processes, so all of these models inherit determinacy.
- **Turing machines.** One process is any program, so a network can compute any computable function, and a process with a channel from itself to itself is a queue machine. This is the reason for Theorem 3.
- **Models with choice.** Petri nets, and process models in which a process may wait on whichever of two channels has data first, are not determinate. The determinacy of Kahn networks is bought by giving up such a choice.
- **Hardware.** A [latency-insensitive design](/latency-insensitive-design/) is a network of synchronous blocks that talk through bounded queues with back pressure. With unbounded queues it would be a Kahn network.

## Known results in the model

For a process $P$, let $F_P$ map the vector $x$ of histories of its input channels to the vector of histories it writes when it runs alone and is fed $x$. The run is unique, since $P$ is deterministic and decides by itself which channel to read next. The run on $x$ stops when $P$ halts, or when it asks for a value that $x$ does not have, or never.

**Lemma 1.** $F_P$ is monotone and continuous: $x \sqsubseteq y$ implies $F_P(x) \sqsubseteq F_P(y)$, and $F_P$ of the limit of a chain is the limit of the images.

*Proof.* If $x \sqsubseteq y$, the run on $y$ does the same steps as the run on $x$ until the run on $x$ stops. If it stops by halting, the two runs are equal. If it stops because $x$ ran out on some channel, the run on $y$ continues from there. In both cases the run on $x$ is a prefix of the run on $y$, and so are its writes. For continuity, each value written by the run on the limit is written after a finite number of reads, which all lie in some $x_i$ of the chain, so the run on $x_i$ writes it too. $\square$

Collect the channels into one vector $X$. Fix the input channels to the given input $I$, and for a channel $c$ written by $P$ let $F(X)_c = F_P(X_{\mathrm{in}(P)})_c$. By Lemma 1, $F$ is monotone and continuous on a set in which every increasing chain has a limit, so by the [Kleene fixed-point theorem](/kleene-fixed-point-theorem/) it has a least fixed point
$$\mu F = \lim_{k \to \infty} F^k(\bot),$$
where $\bot$ gives the empty history to every channel that is not an input. Every vector $H$ with $F(H) \sqsubseteq H$ satisfies $\mu F \sqsubseteq H$, since by induction $F^k(\bot) \sqsubseteq H$ for every $k$.

**Theorem 1 (determinacy, Kahn 1974).** In every fair run of the network on the input $I$, the history of every channel is the entry of $\mu F$ for that channel.

*Proof.* First, at every moment of every run, finite or not, the histories so far are below $\mu F$. By induction on the steps: when $P$ writes, it has read some values $u$, and by induction $u$ is below the entries of $\mu F$ on its inputs. The run of $P$ so far is a prefix of its run on $u$, which by Lemma 1 is a prefix of its run on $\mu F_{\mathrm{in}(P)}$, so what $P$ has written is a prefix of $F_P(\mu F_{\mathrm{in}(P)}) = \mu F_{\mathrm{out}(P)}$. Taking limits, the final histories $H$ of the run satisfy $H \sqsubseteq \mu F$.

Next, $H$ is a fixed point of $F$. Fix a process $P$ and let $u$ be all that it reads in the whole run. Its run is the complete run of $P$ on $u$: otherwise $P$ would be able to move from some moment on and never move, which fairness forbids. So $P$ writes $F_P(u)$. If $u = H_{\mathrm{in}(P)}$, this is $F_P(H_{\mathrm{in}(P)})$. Otherwise some value is written on an input channel $c$ of $P$ and never read. Then the run of $P$ on $u$ does not stop by asking for that value, since $P$ would then be able to read it forever and never do so. So it stops by halting, or by asking for a value on a channel on which $u$ already equals $H$, or never; in each case the run on $H_{\mathrm{in}(P)}$ is the same run, and $F_P(u) = F_P(H_{\mathrm{in}(P)})$. So $H_{\mathrm{out}(P)} = F_P(H_{\mathrm{in}(P)})$ for every $P$, that is $F(H) = H$. Then $\mu F \sqsubseteq H$, and with the first part, $H = \mu F$. $\square$

Kahn stated the result in the language of fixed points; the match between the runs of the processes and the fixed point was later treated in detail for more general settings (Kahn and MacQueen 1977, and later work cited by Lee and Parks 1995). The proof above assumes the simple process language of this page: deterministic programs, one writer and one reader per channel, and reads whose channel the process picks by itself.

**Theorem 2 (no determinacy without blocking reads).** If a process may test a channel for emptiness, the histories can depend on the schedule. A merge process that loops "if channel $a$ is not empty, copy one value from $a$ to $c$; else if $b$ is not empty, copy one value from $b$ to $c$" with inputs $a = (1)$ and $b = (2)$ writes $(1, 2)$ on $c$ if the value on $a$ arrives first and $(2, 1)$ if the value on $b$ arrives first. Its input-output relation is not a function, so it has no $F_P$, and Lemma 1 fails.

**Theorem 3 (undecidability).** Whether a Kahn network terminates, and whether it has a fair run in which every channel holds at most $B$ values for some $B$, are both undecidable.

*Proof.* Termination: one process with no channels is any program, so this is the [halting problem](/halting-problem/). Bounded memory: given a program $M$, build a network with two processes. Process $P$ runs $M$; if $M$ halts, $P$ then writes a value to channel $c$ again and again forever. Process $Q$ first reads from a channel $c'$ that nobody writes, so it blocks forever, and it is the reader of $c$. In every fair run, $P$ is never blocked, so it keeps moving, and channel $c$ grows without bound exactly when $M$ halts. So a decision procedure for bounded memory would decide the halting problem. $\square$

Parks (1995) states both results and gives a policy for bounded channels: run with small capacities, make a write wait while its channel is full, and when every process waits and at least one of them waits to write, raise the capacity of the full channel with the least capacity among those that block a write. A write that waits changes only the timing, so by the first part of the proof of Theorem 1 the histories of such a run are always prefixes of $\mu F$. Parks shows that the policy produces the complete histories, and that it stays in bounded memory whenever some fair run does. Such questions are decidable in [synchronous dataflow](/synchronous-dataflow/), whose fixed rates make the memory of a periodic schedule computable.

### Example

A network computes the running sums of its input. Process Add reads one value from channel $X$, the input, and one from channel $Z$, and writes their sum to $Y$, again and again. Process Delay writes 0 to $Z$ and then copies every value it reads from $Y$ to $Z$. The output is $Y$. For the input $X = (1, 2, 3)$ the Kleene iterates of $F$, with $X$ held fixed, are:

| iterate | $Y$ | $Z$ |
| --- | --- | --- |
| $F^0(\bot)$ | () | () |
| $F^1(\bot)$ | () | (0) |
| $F^2(\bot)$ | (1) | (0) |
| $F^3(\bot)$ | (1) | (0, 1) |
| $F^4(\bot)$ | (1, 3) | (0, 1) |
| $F^5(\bot)$ | (1, 3) | (0, 1, 3) |
| $F^6(\bot)$ | (1, 3, 6) | (0, 1, 3) |
| $F^7(\bot)$ | (1, 3, 6) | (0, 1, 3, 6) |

From $F^7$ on, nothing changes, so $\mu F$ gives $Y = (1, 3, 6)$. A schedule that runs Delay as far as it can before Add, and one that alternates the two, both write exactly these histories. At the end, the value 6 stays on $Z$, since Add blocks on $X$ before it reads it; the run ends with Add blocked on the input and Delay blocked on $Y$.

## References
