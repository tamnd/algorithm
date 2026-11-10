---
tag: 8VM9DJ
kind: definition
slug: anonymous-network
name: Anonymous network
aliases:
- Anonymous processes
- Anonymous distributed system
area: distributed/leader-election
level: core
summary: A network whose processes have no identifiers and all run the same program. Symmetry of the network then limits what can be computed, for example leader election.
prereqs: [port-numbering, ring-network, synchronous-model, asynchronous-model]
see_also: [anonymous-ring-impossibility, anonymous-leader-election, itai-rodeh, ring-leader-election, las-vegas-algorithm, fair-coin-flipping]
sources:
  - paper: doi:10.1145/800141.804655
    title: Dana Angluin, Local and global properties in networks of processors, Proceedings of the 12th ACM Symposium on Theory of Computing, 1980
    locator: pages 82 to 93 (identical processes, coverings of networks, and the impossibility of election in symmetric networks)
  - paper: doi:10.1109/71.481599
    title: Masafumi Yamashita and Tsunehiko Kameda, Computing on anonymous networks, part I, characterizing the solvable cases, IEEE Transactions on Parallel and Distributed Systems 7(1), 1996
    locator: pages 69 to 89 (views of processes, and which problems, among them leader election, are solvable)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 3, Section 3.2 (anonymous rings)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 3, Section 3.2 (impossibility for identical processes)
---

An anonymous network is a message-passing network in which the processes have no identifiers: all processes run the same program and start in the same state, except perhaps for an input. A process can tell its own links apart by local port numbers, but it has no name that other processes could use. In such a network, symmetry limits what can be computed. If the network looks the same from two processes, a deterministic algorithm cannot make them behave differently, so tasks like [leader election](/anonymous-leader-election/) can become impossible. Angluin studied these limits in 1980, and Yamashita and Kameda gave an exact description of the solvable cases in 1996 using *views*.

## Definition

An **anonymous network** is a connected graph $G = (V, E)$ together with a [port numbering](/port-numbering/): each process $v$ numbers its incident links $1, \ldots, \deg(v)$. An **algorithm** for the network is one state machine $A$, the same for all processes. The initial state of $v$ depends only on $\deg(v)$, on the input of $v$ if there is one, and on global knowledge given to all processes, such as $n$ or a bound on it. When $v$ sends, it names a port; when it receives, it learns the port the message came on. Nothing else distinguishes processes.

The **symmetry** of the network is given by its port-preserving automorphisms: bijections $\phi : V \to V$ such that if port $a$ of $v$ leads to port $b$ of $w$, then port $a$ of $\phi(v)$ leads to port $b$ of $\phi(w)$, and $v$ and $\phi(v)$ have the same input.

The **view** of $v$, in the sense of Yamashita and Kameda, is the infinite rooted tree $T(v)$ of all walks that start at $v$. The root is labelled with the input and degree of $v$, and each edge of a walk is labelled with the port numbers at both of its ends. Two processes with the same view cannot be told apart by any deterministic algorithm, in either timing model: an induction on rounds shows that in the synchronous run they are in the same state after every round.

## Examples and non-examples

- **An oriented anonymous ring.** On a [ring](/ring-network/) where every process calls the link to its successor port 1, the map $p_i \mapsto p_{i+1}$ preserves ports. All processes have the same view, and every deterministic algorithm keeps them in the same state, so no deterministic algorithm can elect a leader. This is [Angluin's theorem](/anonymous-ring-impossibility/).
- **A path of three processes.** The middle process has degree 2 and the ends have degree 1, so the middle process has its own view. The algorithm "a process of degree 2 is the leader" elects it without any identifiers.
- **A path of two processes.** Both have degree 1 and port 1, so the swap is a port-preserving automorphism. No deterministic algorithm elects one of them.
- **A ring with distinct inputs.** If the inputs are all different, every view is different, and the network is not anonymous in the sense that matters: inputs act as identifiers.
- **Non-example: a ring with identifiers.** In the usual [ring election problem](/ring-leader-election/) each process has a distinct identifier, so the processes do not run the same initial state. This is not an anonymous network.
- **Randomized processes.** If each process can flip its own coins, as in the [Itai-Rodeh algorithm](/itai-rodeh/), the processes start the same but can draw different values. The network is still anonymous; randomness breaks the symmetry with probability 1, not with certainty.

## Related definitions

- **Symmetry and covering.** Angluin's argument uses coverings: if a network $H$ covers $G$, that is, there is a map from $H$ onto $G$ that preserves ports and is a bijection on the links of each process, then a run on $G$ can be lifted to a run on $H$ in which the processes over the same process of $G$ behave alike. A problem that has a solution on $G$ but would force two such processes to differ on $H$ cannot be solved on both by the same algorithm.
- **Views and solvability.** Two views are equal if they are equal to a finite depth that depends on $n$; Norris later showed that depth $n - 1$ is enough. Yamashita and Kameda characterize, for each kind of knowledge of the network, the graphs and port numberings on which leader election and other tasks have deterministic solutions. For election when $n$ or the graph is known, the condition is that no two processes have the same view.
- **Uniform and non-uniform algorithms.** As for rings with identifiers, an algorithm is uniform if it does not depend on $n$. In anonymous networks, knowledge of $n$ changes what randomized algorithms can do: see [leader election in anonymous networks](/anonymous-leader-election/).
- **Las Vegas and Monte Carlo.** A randomized algorithm in an anonymous network can be a [Las Vegas algorithm](/las-vegas-algorithm/) (always correct, ends with probability 1) only under some conditions, such as known $n$; otherwise it may only be correct with some probability.

## References
