---
tag: KGRQ21
kind: model
slug: timed-event-graph
name: Timed event graph
aliases:
- timed marked graph
area: control/discrete-event-and-hybrid-systems
level: advanced
summary: "A Petri net where each place has one input and one output transition and a holding time. With earliest firing, the firing times obey x(k) = A x(k-1) in max-plus algebra."
prereqs: [petri-net, max-plus-algebra]
see_also: [max-plus-eigenvalue-theorem, discrete-event-system, karp-minimum-mean-cycle, synchronous-dataflow, latency-insensitive-design, critical-path-method, job-shop-scheduling, timed-automata]
sources:
  - book: isbn:9780471936091
    title: François Baccelli, Guy Cohen, Geert Jan Olsder and Jean-Pierre Quadrat, Synchronization and Linearity, An Algebra for Discrete Event Systems, Wiley, 1992
    locator: the chapter on graph theory and Petri nets, and the chapters on the max-plus model of event graphs and its periodic regime
  - book: isbn:9780691117638
    title: Bernd Heidergott, Geert Jan Olsder and Jacob van der Woude, Max Plus at Work, Princeton University Press, 2006
    locator: Chapter 7, Petri Nets (timed event graphs and their max-plus equations); Chapter 3, the cycle-time vector
  - paper: "Guy Cohen, Didier Dubois, Jean-Pierre Quadrat and Michel Viot, A linear-system-theoretic view of discrete-event processes and its use for performance evaluation in manufacturing, IEEE Transactions on Automatic Control AC-30(3), 210-220, 1985"
    locator: the max-plus linear model of a manufacturing system and its cycle time
  - paper: doi:10.1109/5.24143
    title: Tadao Murata, Petri nets, properties, analysis and applications, Proceedings of the IEEE 77(4), 541-580, 1989
    locator: the section on marked graphs (liveness and the token count of circuits) and the section on timed nets
---

A timed event graph is a model of a system of repeated events that wait for each other, such as machines in a production line, stages of a pipeline, or actors in a dataflow program. It is a [Petri net](/petri-net/) in which every place has exactly one transition that puts tokens into it and exactly one transition that takes tokens out, and in which each token must stay a fixed holding time in its place before it can be used. So there are no choices, only synchronization: each event happens as soon as all of its input conditions are ready. Under this earliest firing rule, the time of the $k$-th occurrence of each event is the maximum, over its inputs, of an earlier time plus a delay. In [max-plus algebra](/max-plus-algebra/) this is a linear recurrence $x(k) = A \otimes x(k-1)$, and the long-run period of the system is the eigenvalue of $A$ given by the [max-plus eigenvalue theorem](/max-plus-eigenvalue-theorem/). The untimed version is called a marked graph; homogeneous [synchronous dataflow](/synchronous-dataflow/) graphs and the pipelines of [latency-insensitive design](/latency-insensitive-design/) are marked graphs.

## The machine

**Structure.** There are $n$ transitions $t_1, \dots, t_n$ (the events) and a set of places (the conditions). Each place $p$ has one input transition $t_{j(p)}$, one output transition $t_{i(p)}$, a number $m_p \ge 0$ of initial tokens and a holding time $\tau_p \ge 0$. A token that enters $p$ can be used by $t_{i(p)}$ only $\tau_p$ time units later. Tokens leave a place in the order they entered. Some authors put the delays on the transitions (firing times) instead of on the places; a transition delay can be moved to its output places, so the two forms are equivalent.

**Time axis.** Event driven. The state is the vector of daters $x(k) \in \mathbb{R}^n$, where $x_i(k)$ is the time of the $k$-th firing of $t_i$. Firing itself takes no time.

**Dynamics.** Under the earliest firing rule, each transition fires as soon as every input place holds a token that has stayed its holding time. Then

$$x_i(k) = \max_{p:\ i(p) = i} \left(\tau_p + x_{j(p)}(k - m_p)\right).$$

A place with $m_p \ge 2$ can be split into a chain of places with one token each, so assume $m_p \in \{0, 1\}$. Let $A_0$ collect the zero-token places and $A_1$ the one-token places: $(A_m)_{ij}$ is the largest $\tau_p$ over the places from $t_j$ to $t_i$ with $m_p = m$, and $\varepsilon = -\infty$ if there is none. Then

$$x(k) = A_0 \otimes x(k) \oplus A_1 \otimes x(k-1).$$

**Standing assumption.** Every circuit of places carries at least one token. Then the graph of $A_0$ has no circuit, its star $A_0^* = E \oplus A_0 \oplus \cdots \oplus A_0^{\otimes(n-1)}$ is finite, and

$$x(k) = A \otimes x(k-1), \qquad A = A_0^* \otimes A_1.$$

The initial condition $x(0)$ fixes when the initial tokens become available: the token of a one-token place from $t_j$ is available at $x_j(0) + \tau_p$. The proof is in proofs/correctness.md of this page. The computation of $A$ and of the daters is:

```pseudo id=main
TEG-MATRIX(n, places)                  ▷ place = (j, i, m, tau) with m ∈ {0, 1}
L1  A0 ← n by n matrix of ε; A1 ← n by n matrix of ε
L2  for each place (j, i, m, tau) do
L3      if m = 0 then A0[i][j] ← max(A0[i][j], tau) else A1[i][j] ← max(A1[i][j], tau)
L4  S ← A0* = E ⊕ A0 ⊕ ... ⊕ A0^(n-1)    ▷ error if A0^n ≠ ε: a circuit without tokens
L5  A ← S ⊗ A1
L6  for k ← 1 to K do x(k) ← A ⊗ x(k-1)
```

**Example 1.** Two transitions. Place $t_1 \to t_1$ holds 3, place $t_2 \to t_2$ holds 4, place $t_2 \to t_1$ holds 7 and place $t_1 \to t_2$ holds 2; every place has one token. The self-loops say that a transition cannot fire again before its own processing time has passed. All places have one token, so $A_0 = \mathcal{E}$, $A_0^* = E$ and

$$A = A_1 = \begin{bmatrix} 3 & 7 \\ 2 & 4 \end{bmatrix}.$$

From $x(0) = (0, 0)$ the daters are:

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $x_1(k)$ | 0 | 7 | 11 | 16 | 20 | 25 |
| $x_2(k)$ | 0 | 4 | 9 | 13 | 18 | 22 |

For example, $x_1(2) = \max(3 + 7, 7 + 4) = 11$: the second firing of $t_1$ waits for the token from the first firing of $t_2$. After the first step, each transition fires 9 time units every 2 firings, so the cycle time is 4.5, the mean of the circuit $t_1 \to t_2 \to t_1$ (holding times $2 + 7$ over 2 tokens).

**Example 2.** A production line with one pallet. $t_1$ starts a part on machine 1, $t_2$ starts it on machine 2, $t_3$ releases it. The places are: $t_1 \to t_1$ (machine 1 busy, 1 token, 3), $t_1 \to t_2$ (the part moves on, 0 tokens, 3), $t_2 \to t_2$ (machine 2 busy, 1 token, 4), $t_2 \to t_3$ (0 tokens, 4) and $t_3 \to t_1$ (the pallet returns, 1 token, 0). Here $A_0$ has the arcs $t_1 \to t_2$ (3) and $t_2 \to t_3$ (4), so $A_0^*$ adds the path $t_1 \to t_3$ of weight 7, and

$$A = A_0^* \otimes A_1 = \begin{bmatrix} 3 & \varepsilon & 0 \\ 6 & 4 & 3 \\ 10 & 8 & 7 \end{bmatrix}.$$

With $x(0) = (-3, -4, 0)$, all initial tokens are available at time 0, and the daters are $x(1) = (0, 3, 7)$, $x(2) = (7, 10, 14)$, $x(3) = (14, 17, 21)$. The single pallet makes the line sequential, and the cycle time is $3 + 4 + 0 = 7$.

## What it counts

The model predicts the time of every event under the earliest firing rule, from the holding times and the initial condition alone. The main derived quantities are:

- The cycle time $\lambda = \lim_k x_i(k)/k$, the mean time between two firings of a transition in the long run, and the throughput $1/\lambda$.
- The critical circuits, the ones that reach the maximum in $\lambda$. They are the bottleneck: shortening a holding time off the critical circuits does not change $\lambda$.
- Sojourn times of tokens in places and the transient before the periodic regime.

The model does not count resource use, costs or probabilities, and it does not decide between alternatives: a system with routing choices or with competition for a resource needs a general Petri net or another [discrete event system](/discrete-event-system/) model.

## Relation to other models

- A timed event graph is a [Petri net](/petri-net/) without conflicts: since each place has one output transition, two transitions never compete for a token. The other special class, the state machine, has one input and one output arc per transition and models choice without synchronization.
- [Max-plus algebra](/max-plus-algebra/) is its algebra: the firing equations are linear there, as above. Counting the firings up to a time $t$ instead of timing the $k$-th firing gives the dual, min-plus linear form (the counter description of Baccelli et al. 1992).
- A homogeneous [synchronous dataflow](/synchronous-dataflow/) graph, where each actor consumes and produces one token per firing on each arc, is a marked graph; with execution times it is a timed event graph. Its throughput analysis is the cycle time analysis here.
- The [critical path method](/critical-path-method/) is the one-shot, acyclic case: each activity happens once, and the start times are the longest paths, given by the max-plus star.
- Cyclic [job shop scheduling](/job-shop-scheduling/) with a fixed order of operations on each machine is a timed event graph. Choosing that order is the hard part, and it is outside the model.
- [Timed automata](/timed-automata/) model time with clocks and allow choice; they are more expressive, and their questions are decided by state-space exploration rather than by linear algebra.

## Known results in the model

- **Max-plus linearity.** If every circuit has a token, $x(k) = A_0^* \otimes A_1 \otimes x(k-1)$ (Baccelli et al. 1992; proof on this page).
- **Liveness and token invariance.** The number of tokens on each circuit never changes, since each transition on the circuit takes one token from the circuit and puts one back. A marked graph is live if and only if every circuit holds at least one token (Murata 1989, section on marked graphs).
- **Cycle time.** If the graph of $A$ is strongly connected, every transition has the same cycle time $\lambda$. It is the maximum cycle mean of $A$, and it equals the maximum over the circuits of the net of the sum of the holding times divided by the number of tokens on the circuit. This is the [max-plus eigenvalue theorem](/max-plus-eigenvalue-theorem/), and [Karp's algorithm](/karp-minimum-mean-cycle/) computes $\lambda$ in polynomial time.
- **Periodic regime.** After a finite transient, $x(k + c) = c\lambda + x(k)$ for a cyclicity $c \ge 1$ (Cohen, Dubois, Quadrat and Viot 1985). In Example 1, $c = 2$ and the transient is one step.
- **Reducible nets.** If the graph is not strongly connected, the transitions can have different cycle times, given by the cycle time vector (Heidergott, Olsder and van der Woude 2006, Chapter 3).

## References
