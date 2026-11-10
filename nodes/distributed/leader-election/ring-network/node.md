---
tag: 2Q85J6
kind: definition
slug: ring-network
name: Ring network
aliases:
- Ring topology
- Cycle network
area: distributed/leader-election
level: intro
summary: A message-passing network whose graph is a cycle. It is unidirectional or bidirectional, oriented or not, and n is known or unknown. It is the standard model for election bounds.
prereqs: [graph, port-numbering, asynchronous-model, synchronous-model]
see_also: [ring-leader-election, chang-roberts, ring-election-lower-bound, anonymous-ring-impossibility, anonymous-network, complete-network-leader-election, message-complexity, round-complexity]
sources:
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 3, Section 3.1 (the synchronous ring and its variants) and Chapter 15, Section 15.1 (the asynchronous ring)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 3 (leader election in rings, the formal ring model, uniform and nonuniform algorithms, anonymous rings)
  - book: isbn:9780521794831
    title: Gerard Tel, Introduction to Distributed Algorithms, second edition, Cambridge University Press, 2000
    locator: Chapter 7 (election algorithms, Section 7.2 on rings)
---

A ring network is a message-passing system whose communication [graph](/graph/) is a cycle: each of the $n$ processes has exactly two neighbours, and the links close into one loop. The model has several versions: links can carry messages in one direction or in both, the processes can share a sense of direction or not, and they can know $n$ or not. The ring is the standard topology for the bounds of [leader election](/ring-leader-election/), because it is the simplest network in which no process is special by its position.

## Definition

Let $n \ge 1$. A **ring of size $n$** has processes $p_0, p_1, \ldots, p_{n-1}$. Indices are taken modulo $n$. For each $i$ there is a link between $p_i$ and $p_{i+1}$. For $n \ge 3$ the graph is the cycle $C_n$. For $n = 2$ there are two parallel links between $p_0$ and $p_1$, and for $n = 1$ the link is a loop. Each link is a reliable channel: each message that is sent is delivered once, without change.

A process does not know the indices. It sees only its two **ports**, which it calls *left* and *right* (a [port numbering](/port-numbering/) with two ports). The versions of the model differ in four choices.

- **Direction of the links.** In a *unidirectional* ring, $p_i$ can send only on its link to $p_{i+1}$ and can receive only from $p_{i-1}$. In a *bidirectional* ring each link carries messages both ways.
- **Orientation.** A bidirectional ring is *oriented* if for each $i$ the right port of $p_i$ leads to $p_{i+1}$ and the left port leads to $p_{i-1}$. Then all processes agree on what "clockwise" means. In a *non-oriented* ring, each process labels its two ports in an arbitrary way. A unidirectional ring is oriented by definition.
- **Knowledge of $n$.** An algorithm is *uniform* if the same code works for each $n$, so the processes do not know $n$. It is *non-uniform* if the code of the processes can depend on $n$.
- **Identifiers.** Each process has a distinct identifier $\mathrm{id}_i$ from a totally ordered set, or the processes are identical. A ring of identical processes is an [anonymous network](/anonymous-network/).

The timing model is the [synchronous model](/synchronous-model/) (lock-step rounds) or the [asynchronous model](/asynchronous-model/) (each message arrives after a finite but unbounded delay). In the asynchronous case the channels are FIFO or not, and the page of each algorithm says which it needs.

Basic measures follow from the cycle. A ring has $n$ links. In a bidirectional ring the distance between $p_i$ and $p_j$ is $\min(d, n - d)$ with $d = (j - i) \bmod n$, so the diameter is $\lfloor n/2 \rfloor$. In a unidirectional ring a message from $p_i$ to $p_j$ needs $(j - i) \bmod n$ hops, and a message that goes all the way round needs $n$ hops.

## Examples and non-examples

- **A unidirectional ring of size 5** with identifiers 3, 7, 1, 5, 2 in the order of the links. Each process can send only to the next one, so a message from the process with identifier 7 reaches the process with identifier 3 after 4 hops. This is the setting of the [Chang-Roberts algorithm](/chang-roberts/).
- **An oriented bidirectional ring.** The same 5 processes, with links that carry messages both ways and with "right" meaning "next" at each process. The [Hirschberg-Sinclair algorithm](/hirschberg-sinclair/) and [Franklin's algorithm](/franklin/) run here.
- **A non-oriented ring.** The same graph, but $p_2$ calls its link to $p_3$ "left". An algorithm that sends "to the right" at each process now sends in both directions round the ring. Algorithms that only compare what arrives on the two ports, such as Hirschberg-Sinclair, still work.
- **A ring of size 3** is also the [complete graph](/complete-graph/) $K_3$. For $n \ge 4$ the two classes are different.
- **Non-example: a path.** The processes $p_0, \ldots, p_{n-1}$ with links only between $p_i$ and $p_{i+1}$ for $i < n - 1$. The two end processes have one neighbour, so the network is a [tree](/tree/), and election there is the [tree election problem](/tree-leader-election/).
- **Non-example: a ring with a chord.** A cycle plus one more link has two processes with three neighbours. It is a general network, and the ring bounds do not apply to it as stated.

## Related definitions

- **Ring election.** The [leader election problem on a ring](/ring-leader-election/) asks that exactly one process becomes the leader. Its message cost is $\Theta(n \log n)$ for comparison-based algorithms by the [ring election lower bound](/ring-election-lower-bound/).
- **Anonymous ring.** A ring of identical processes. No deterministic algorithm elects a leader in it, by [Angluin's theorem](/anonymous-ring-impossibility/).
- **Complete network.** Each process has a link to each other process. [Election in complete networks](/complete-network-leader-election/) also costs $\Theta(n \log n)$ messages, but the reasons are different.
- **Message and time cost.** Algorithms on rings are measured by their [message complexity](/message-complexity/) and by their time, in rounds or in units of the largest message delay ([round complexity](/round-complexity/)).

## References
