---
tag: A1GTWT
kind: problem
slug: interface-synthesis
name: Interface synthesis
aliases:
- interface transducer synthesis
- protocol converter synthesis
area: eda/high-level-synthesis-and-scheduling
level: advanced
summary: Generate the logic that lets two blocks with different communication protocols exchange data correctly, from timing diagrams or protocol automata.
prereqs: [finite-state-machine-with-datapath, product-construction, games-on-graphs]
see_also: [latency-insensitive-design, reactive-synthesis, supervisory-control-theory, mealy-machine, parity-game, clock-domain-crossing-verification, memory-partitioning-for-hls, hardware-software-partitioning]
sources:
  - paper: "Roberto Passerone, Luca de Alfaro, Thomas A. Henzinger and Alberto L. Sangiovanni-Vincentelli, Convertibility verification and converter synthesis: two faces of the same coin, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design, 132 to 139, 2002"
    locator: whole paper (protocols as automata, the converter as a winning strategy of a game against the protocols, and its computation)
  - paper: "Gaetano Borriello and Randy H. Katz, Synthesis and optimization of interface transducer logic, Proceedings of the IEEE International Conference on Computer-Aided Design, 1987"
    locator: whole paper (interface logic synthesized from timing diagrams of the two sides; general locator)
  - book: isbn:9783540003885
    title: Erich Grädel, Wolfgang Thomas and Thomas Wilke (editors), Automata, Logics, and Infinite Games, Lecture Notes in Computer Science 2500, Springer (2002)
    locator: Chapter 2, Infinite Games (safety games and attractors; general locator)
---

Interface synthesis builds the glue logic between two hardware blocks that talk with different protocols, for example a sender that pushes each datum and waits for an acknowledge, and a receiver that requests each datum before it takes one. The input is a description of each protocol, as timing diagrams or as finite automata over signal events, and a requirement on the data that flows between them, such as in-order delivery with a buffer of bounded size. The output is a converter, a finite state machine with a small datapath, that sits between the blocks, never refuses an event either block may produce, and keeps the requirement in every run. Seen this way, the converter is a winning strategy in a safety game played against the two protocols.

## In plain words

Two chips want to pass numbers to each other, but they follow different etiquette. One says "here is a number, tell me when you got it". The other says "I am ready, give me a number". Neither can change. We must build a small go-between that speaks both languages. It must accept whatever either side says at any moment, it may hold a few numbers in a small store, and it decides when to answer. It must never lose a number, never make one up, never overfill its store and never leave both sides stuck. Finding such a go-between is like finding a way to win a game against two players who may act at any time.

## Definition

**Protocols.** A protocol is a deterministic finite automaton $P = (Q, q_0, \Sigma, \delta)$ whose actions are split into outputs $\Sigma^{\mathrm{out}}$, which the block produces when it chooses, and inputs $\Sigma^{\mathrm{in}}$, which it waits for. Some actions carry a datum: the sender $P_1$ has an output that hands over one datum, and the receiver $P_2$ has an input that takes one.

**Converter.** A converter $C$ is a deterministic finite automaton over $\Sigma_1 \cup \Sigma_2$, with a buffer of at most $k$ data. Its inputs are the outputs of $P_1$ and $P_2$, and its outputs are their inputs. The closed system is the product $P_1 \parallel C \parallel P_2$, built as in the [product construction](/product-construction/): an action takes place when every component whose alphabet contains it takes it together. Each datum taken from $P_1$ enters the buffer, and each datum given to $P_2$ leaves it in first-in first-out order.

**Correctness.** $C$ is correct when, in every reachable state of the closed system:

1. **Receptive.** Every output that $P_1$ or $P_2$ can produce in its current state is accepted by $C$. A block is never blocked by the converter.
2. **Buffer.** The buffer holds between $0$ and $k$ data. So no datum is lost by overflow, and none is given to $P_2$ that was not taken from $P_1$.
3. **No deadlock.** Some action is enabled.

The timing is an interleaving: the protocols may produce any enabled output at any moment, and the converter chooses when to produce its own.

**Problem.** Given $P_1$, $P_2$ and $k$, decide whether a correct converter exists, and build one. The optimization form asks for the least $k$, or for a converter with the fewest states.

## Variants

- **Timing diagrams.** Borriello and Katz (1987) take the two sides as timing diagrams, sequences of signal events with bounds on the delays between them, and produce interface logic that meets both. Delays then matter, not only the order of events.
- **Liveness.** Ask also that every datum taken from $P_1$ reaches $P_2$ eventually. This is no longer a safety requirement, and the game becomes a Büchi or [parity game](/parity-game/).
- **General specifications.** Replace the buffer rule by an automaton $S$ that accepts the correct orders of events, and take its product with the arena. Passerone, de Alfaro, Henzinger and Sangiovanni-Vincentelli (2002) treat this form, where checking that two protocols can be converted and building the converter are one computation.
- **Width and rate conversion.** The sides use different data widths, such as 32 bits against 8 bits, or different rates, and the converter splits or packs words.
- **Clock domains.** The two blocks run on different clocks. The converter then needs synchronizers and an asynchronous buffer, and its correctness depends on [clock domain crossing](/clock-domain-crossing-verification/) rules beyond the protocol automata.
- **Generated interfaces in high-level synthesis.** A C function argument becomes a port with a fixed protocol, such as a handshake, a stream or a memory bus, and the tool generates the adapter. [Latency-insensitive design](/latency-insensitive-design/) fixes one protocol for all blocks so that no converter is needed between them.

## Examples

**A push sender and a pull receiver.** The sender $P_1$ has the states $s_0, s_1$: in $s_0$ it outputs a datum $d_1$ and goes to $s_1$, where it waits for the input $\mathit{ack}$ and goes back to $s_0$. The receiver $P_2$ has the states $r_0, r_1$: in $r_0$ it outputs $\mathit{req}$ and goes to $r_1$, where it waits for a datum $d_2$ and goes back to $r_0$. The converter takes $d_1$ and $\mathit{req}$, and produces $\mathit{ack}$ and $d_2$. A state of the closed system is $(s, r, \beta)$ with $\beta$ the number of buffered data.

- **No buffer, $k = 0$.** At the start, $P_1$ may output $d_1$ before $P_2$ has asked for anything. The converter must accept it, and it cannot pass it on, since $P_2$ is in $r_0$. So the buffer would hold 1 datum, and no correct converter exists.
- **One place, $k = 1$.** Take $d_1$ into the buffer. Wait for $\mathit{req}$, then give the datum as $d_2$, and only then send $\mathit{ack}$. The reachable states are the six triples $(s_0, r_0, 0)$, $(s_0, r_1, 0)$, $(s_1, r_0, 1)$, $(s_1, r_1, 1)$, $(s_1, r_0, 0)$ and $(s_1, r_1, 0)$. The last one arises when $P_2$ asks again before the converter has acknowledged. In each of them the buffer holds at most 1 and some action is enabled. While the buffer is full, $P_1$ waits in $s_1$ for $\mathit{ack}$ and cannot send again.
- **Acknowledging at once fails for every $k$.** If the converter sends $\mathit{ack}$ as soon as it takes $d_1$, then $P_1$ may send $d_1$ again and again while $P_2$ never outputs $\mathit{req}$. After $k + 1$ data the buffer overflows. So the choice of when to acknowledge decides correctness.

The least buffer for this pair is 1.

## Known algorithms

- **Safety games.** Build the arena of the product of $P_1$, $P_2$ and the buffer, mark the states that break a rule, and compute the set of states from which the protocols can force a bad state, an attractor, in time linear in the arena. A converter exists exactly when the initial state is outside it. See [games on graphs](/games-on-graphs/).
- **Fixed points over the protocol product.** Passerone et al. (2002) compute the converter as a greatest fixed point over the product of the protocols, and the same computation decides whether the protocols can be converted at all.
- **Timing diagram synthesis.** Borriello and Katz (1987) derive the interface logic from the events and timing constraints of the two diagrams.
- **Supervisory control.** The same question, a controller that may only disable controllable events, is the subject of [supervisory control theory](/supervisory-control-theory/) for discrete event systems.
- **Reactive synthesis.** For specifications in temporal logic, see [reactive synthesis](/reactive-synthesis/).

## Bounds

**Arena size.** With the buffer rule, the arena has at most $|Q_1| \cdot |Q_2| \cdot (k + 1)$ states, and at most $|\Sigma_1| + |\Sigma_2|$ moves from each. With a specification automaton $S$, multiply by $|Q_S|$. The attractor is linear in the arena, so for two protocols the problem takes time polynomial in their sizes and in $k$.

**Monotone in the buffer.** A converter that is correct for $k$ is correct for $k + 1$, since a buffer that never holds more than $k$ data never holds more than $k + 1$. So the least $k$ is well defined when some $k$ works, and the example shows a pair where it is 1.

**Many components.** When several protocols are composed, the arena is the product of all of them, and its size is the product of their sizes, exponential in their number.

## Reductions

**To a safety game.** Build the arena whose vertices are the triples $(q_1, q_2, \beta)$ with $0 \le \beta \le k$, plus one bad vertex. The protocols play the environment: from each vertex, they may take any enabled output, and the moves that raise $\beta$ above $k$ lead to the bad vertex. The converter plays the controller: it may take one of its outputs that is enabled in the protocols, where giving a datum needs $\beta \ge 1$, or wait. A vertex with no enabled action at all also leads to the bad vertex. A correct converter is a strategy for the controller that never reaches the bad vertex. Conversely, every such strategy gives a correct converter, since the moves of the environment are exactly the outputs that the converter must accept. Safety games have winning strategies that depend only on the current vertex, so the converter needs no more states than the arena.

## Applications

- **IP integration.** Systems on chip combine blocks from many sources, and bus bridges and protocol adapters connect a handshake interface to a stream or a memory bus.
- **High-level synthesis.** Function arguments become hardware interfaces, and the tool inserts adapters between the generated datapath and the system bus.
- **Verification.** Checking that a given converter is correct is the same game with the controller fixed, a reachability check on the closed system.

## References
