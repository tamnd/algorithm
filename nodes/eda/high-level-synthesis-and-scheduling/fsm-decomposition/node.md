---
tag: 93E5AP
kind: technique
slug: fsm-decomposition
name: FSM decomposition
aliases:
- finite state machine decomposition
- general decomposition of FSMs
area: eda/high-level-synthesis-and-scheduling
level: advanced
summary: Splits a finite state machine into interacting smaller machines, by Hartmanis-Stearns partitions or by Devadas and Newton's factorization, to cut logic and delay.
prereqs: [partition-pair, mealy-machine, dfa-minimization]
see_also: [state-assignment, krohn-rhodes-theorem, ashenhurst-curtis-decomposition, incompletely-specified-fsm-minimization, chinese-remainder-theorem, finite-state-machine-with-datapath, kiss-symbolic-minimization, mustang-state-assignment]
sources:
  - book: "Juris Hartmanis and Richard E. Stearns, Algebraic Structure Theory of Sequential Machines, Prentice-Hall, 1966"
    title: Juris Hartmanis and Richard E. Stearns, Algebraic Structure Theory of Sequential Machines, Prentice-Hall, 1966
    locator: serial and parallel decomposition of sequential machines by partitions with the substitution property and partition pairs
  - paper: doi:10.1109/43.41505
    title: Srinivas Devadas and A. Richard Newton, Decomposition and factorization of sequential finite state machines, IEEE Transactions on Computer-Aided Design 8(11), 1206 to 1217, 1989
    locator: general decomposition of a state graph and factorization by repeated subgraphs
  - paper: "Pranav Ashar, Srinivas Devadas and A. Richard Newton, Optimum and heuristic algorithms for an approach to finite state machine decomposition, IEEE Transactions on Computer-Aided Design 10(3), 296 to 310, 1991"
    title: Pranav Ashar, Srinivas Devadas and A. Richard Newton, Optimum and heuristic algorithms for an approach to finite state machine decomposition, IEEE Transactions on Computer-Aided Design 10(3), 296 to 310, 1991
    locator: exact and heuristic algorithms for general decomposition with a two-level logic cost
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 9 (finite state machine decomposition as part of sequential logic optimization)
---

FSM decomposition builds one finite state machine from two or more smaller machines that run together and read each other's state. The pieces are easier to encode and to optimize, each piece has fewer inputs to its next-state logic, and a piece that is idle can be stopped. The classic theory of Hartmanis and Stearns (1966) says exactly when a machine splits without any loss: a serial decomposition, in which the second machine reads the state of the first, exists when the machine has a nontrivial partition of its states with the substitution property, and a parallel decomposition, in which neither reads the other, exists when it has two such partitions that together tell every state apart. Logic synthesis in the late 1980s added looser forms: general decomposition, in which each piece may read the other, and factorization, in which a pattern of states that occurs several times in the state graph is built once (Devadas and Newton 1989).

## In plain words

A clock that shows hours and minutes is one machine with 1440 states, but nobody builds it that way. It is a minutes counter that ticks every minute and an hours counter that ticks only when the minutes wrap around. The hours counter needs to see one thing from the minutes counter, whether it is about to wrap; the minutes counter needs nothing from the hours counter. This is a serial decomposition. Decomposition looks for such splits in any machine: groups of states such that the group of the next state can be known from the group of the present state and the input alone.

## When it applies

- The machine is deterministic and completely specified, with states $S$, inputs $I$ and next-state function $\delta$, as on the [partition pair](/partition-pair/) page, whose notation this page uses. It should first be minimized by [DFA minimization](/dfa-minimization/), or by [incompletely specified FSM minimization](/incompletely-specified-fsm-minimization/) when it has unspecified entries, since redundant states create splits that only reflect the redundancy.
- For an exact serial split, the machine has an SP partition $\pi$ other than $0$ and $1$. For an exact parallel split, it has two SP partitions $\pi_1, \pi_2$, both other than $0$ and $1$, with $\pi_1 \wedge \pi_2 = 0$.
- The aim is smaller or faster logic, or lower power, at the price of more interacting pieces; the number of flip-flops can grow, as the pitfalls show.

## The template

```pseudo id=main
DECOMPOSE(M, π, τ)
L1  if π is not SP, or π ∧ τ ≠ 0 then fail
L2  M1.states ← blocks of π
L3  for each block B of π and input x do M1.δ(B, x) ← the block of π that holds δ(s, x), for any s in B
L4  M2.states ← blocks of τ
L5  for each block C of τ, block B of π and input x do
L6      if B ∩ C = {s} then
L7          M2.δ(C, (x, B)) ← the block of τ that holds δ(s, x)
L8          λ(B, C, x) ← λ(s, x)
L9      else leave M2.δ(C, (x, B)) and λ(B, C, x) unspecified
L10 return (M1, M2, λ)
```

The holes are the choice of $\pi$ among the SP partitions, the choice of $\tau$, the codes of the blocks of each piece, and the cost that judges the result. If $\tau$ is SP too, then $M_2.\delta(C, (x, B))$ does not depend on $B$ and the decomposition is parallel. The SP partitions are listed from the generators $\rho_{st}$ of the [partition pair](/partition-pair/) page, and $\tau$ is chosen with as few blocks as possible; it needs at least as many blocks as the largest block of $\pi$, since the states of one block of $\pi$ must lie in different blocks of $\tau$.

**Theorem (serial decomposition).** If $\pi$ is SP and $\pi \wedge \tau = 0$, then $M_1$ and $M_2$ run side by side, with $M_2$ reading the input and the state of $M_1$, start from $B_\pi(s_0)$ and $B_\tau(s_0)$, and produce the outputs of $M$ on every input word.

*Proof.* $M_1$ is well defined on line L3 because $\pi$ is SP: all states of $B$ go to one block of $\pi$ on input $x$. We show by induction on the number of steps that if $M$ is in state $s$, then $M_1$ is in $B_\pi(s)$ and $M_2$ is in $B_\tau(s)$. This holds at the start. If it holds before input $x$, then $B_\pi(s) \cap B_\tau(s)$ contains $s$, and since $\pi \wedge \tau = 0$ it is exactly $\{s\}$. So line L8 gives the output $\lambda(s, x)$, line L7 moves $M_2$ to $B_\tau(\delta(s, x))$, and line L3 moves $M_1$ to $B_\pi(\delta(s, x))$. The entries left unspecified on line L9 are never used. $\blacksquare$

**Theorem (parallel decomposition).** If $\pi_1$ and $\pi_2$ are both SP and $\pi_1 \wedge \pi_2 = 0$, then $M/\pi_1$ and $M/\pi_2$, each driven by the input alone, together track the state of $M$: it is the single state in the meet of their two blocks. The proof is the same, with $M_2 = M/\pi_2$ well defined because $\pi_2$ is SP.

Conversely, a serial decomposition in which the second machine reads only the state of the first gives an SP partition: group the states of $M$ by the state of the first machine. So a reduced machine has a nontrivial serial decomposition exactly when it has an SP partition other than $0$ and $1$. This is the result of Hartmanis and Stearns; their book states it with a precise notion of one machine realizing another, which this sketch of the converse takes for granted.

## Classic examples

**The counter modulo 4 with enable.** Let $\delta(s, e) = s + e \bmod 4$. Its SP partitions come from the subgroups of $\mathbb{Z}_4$, as the [partition pair](/partition-pair/) page shows: $0$, the parity partition $\pi = \{0, 2\}\{1, 3\}$, and $1$. Take $\pi$ and $\tau = \{0, 1\}\{2, 3\}$, with $\pi \wedge \tau = 0$. Write $s = 2h + p$. Then $M_1$ holds the parity $p$ with $p' = p \oplus e$, and $M_2$ holds $h$ with $h' = h \oplus (p \wedge e)$: it reads the state $p$ of $M_1$ to know whether a carry comes in. This is the usual synchronous binary counter, with the carry from the low bit as the link between the two pieces. The counter has no parallel decomposition, since it has only one nontrivial SP partition.

**The counter modulo 6.** The subgroups $\{0, 2, 4\}$ and $\{0, 3\}$ of $\mathbb{Z}_6$ give the SP partitions $\pi_2 = \{0, 2, 4\}\{1, 3, 5\}$ (the value modulo 2) and $\pi_3 = \{0, 3\}\{1, 4\}\{2, 5\}$ (the value modulo 3). Their meet is $0$ by the [Chinese remainder theorem](/chinese-remainder-theorem/), so the counter is a counter modulo 2 and a counter modulo 3 that run in parallel on the same enable, with 1 + 2 = 3 flip-flops, the same as a plain encoding of 6 states.

**A controller with a repeated pattern.** In the controller of a [finite state machine with datapath](/finite-state-machine-with-datapath/), the same sequence of states, such as a handshake or a memory access, often occurs at several places in the state graph. Factorization (Devadas and Newton 1989) builds that sequence once as a separate machine, which the main machine starts and waits for, so its states and transitions are not repeated. The main machine keeps one state per occurrence, in which it waits.

**State assignment by partitions.** A code in which a group of state bits encodes the blocks of an SP partition $\pi$ gives those bits next-state functions that depend only on themselves and the inputs; this is the serial decomposition hidden in a single encoding. Hartmanis used SP partitions and partition pairs this way for [state assignment](/state-assignment/), before the symbolic methods such as [KISS](/kiss-symbolic-minimization/) and [MUSTANG](/mustang-state-assignment/).

## Variations

- **Partition pairs instead of SP partitions.** If $(\pi, \tau)$ and $(\tau, \pi)$ are partition pairs with $\pi \wedge \tau = 0$, each piece computes its next block from the state of the other and the input, so the pieces read each other. Hartmanis and Stearns treat such loops of partition pairs as well.
- **General decomposition.** Devadas and Newton (1989) split a state graph into two interacting machines that may each read the other's state, without asking for SP partitions, and judge the split by the size of the encoded logic. Ashar, Devadas and Newton (1991) give an exact algorithm and heuristics for this problem with a two-level logic cost.
- **Factorization.** Devadas and Newton (1989) find factors, sets of states and transitions that occur more than once with the same shape, and implement each factor once. An exact factor gives an exact decomposition; looser factors trade some extra logic for wider use.
- **Krohn-Rhodes cascades.** Repeated serial decomposition, with covers whose blocks may overlap in place of partitions, reaches components that are simple groups or reset machines. This is the [Krohn-Rhodes theorem](/krohn-rhodes-theorem/), a theoretical result rather than a synthesis tool.
- **Functional decomposition.** The same idea for combinational logic is [Ashenhurst-Curtis decomposition](/ashenhurst-curtis-decomposition/), which splits a Boolean function by a partition of its inputs rather than of states.

## Pitfalls

- **More flip-flops.** A decomposition into pieces with $|\pi|$ and $|\tau|$ states needs $\lceil \log_2 |\pi| \rceil + \lceil \log_2 |\tau| \rceil$ flip-flops, which can be more than $\lceil \log_2 |S| \rceil$. The counter modulo 15 splits into counters modulo 3 and modulo 5, with $2 + 3 = 5$ flip-flops, while a plain encoding needs 4. Whether the smaller logic pays for the extra flip-flop must be checked.
- **A machine that is not minimized.** Equivalent states can create SP partitions that a reduced machine does not have, and can hide the ones it does have. Minimize first.
- **Choosing $\tau$ too fine.** Any $\tau$ with $\pi \wedge \tau = 0$ works, and $\tau = 0$ always does, but then $M_2$ is as large as $M$. The best $\tau$ has as many blocks as the largest block of $\pi$, and finding one that also keeps $M_2$ simple is itself a search problem.
- **No SP partition at all.** Many machines, including every counter modulo a prime, have only the SP partitions $0$ and $1$, so they have no exact serial decomposition. Then general decomposition or factorization, which do not need SP partitions, are the only choices.
- **Unspecified entries.** Line L9 leaves entries of $M_2$ free. They are don't cares for the logic of $M_2$, and forgetting them gives larger logic than needed.

## Exercises

1. List the SP partitions of the counter modulo 8 with enable, and decompose it serially into three machines with one flip-flop each.
2. Show that if $\pi$ is SP and $\pi \wedge \tau = 0$, then the number of blocks of $\tau$ is at least the size of the largest block of $\pi$, and find a $\tau$ that reaches this bound for the counter modulo 6 and $\pi = \pi_2$.
3. Prove the converse stated after the theorems: if a reduced machine is the serial connection of $M_1$ and $M_2$, and $M_2$ never influences $M_1$, then grouping the states by the state of $M_1$ gives an SP partition.
4. A machine has the SP partitions $0$, $\pi_1$, $\pi_2$ and $1$ only, with $\pi_1 \vee \pi_2 = 1$ and $\pi_1 \wedge \pi_2 \neq 0$. Which decompositions does it have?

## References
