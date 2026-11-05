---
tag: YPD26X
kind: model
slug: mealy-machine
name: Mealy machine
aliases:
- Mealy automaton
area: automata-and-parsing/finite-automata
level: core
summary: Finite-state transducer whose output depends on the current state and input symbol.
prereqs: [deterministic-finite-automaton, alphabet]
see_also:
- moore-machine
- finite-state-transducer
- moore-minimization
- hopcroft-minimization
- dfa-equivalence
- krohn-rhodes-theorem
- boolean-circuit
- lstar-algorithm
sources:
  - paper: doi:10.1002/j.1538-7305.1955.tb03788.x
    title: George H. Mealy, A method for synthesizing sequential circuits, The Bell System Technical Journal 34(5) (1955)
    locator: pp. 1045 to 1079 (the machine whose output is a function of the present state and the present input)
  - paper: "Edward F. Moore, Gedanken-experiments on sequential machines, in C. E. Shannon and J. McCarthy (eds.), Automata Studies, Annals of Mathematics Studies 34, Princeton University Press, 1956"
    locator: pp. 129 to 153 (equivalent states, distinguishing experiments and the reduced machine)
  - book: isbn:9780201029888
    title: John E. Hopcroft and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, first edition, 1979
    locator: Section 2.7, Finite Automata with Output (Moore and Mealy machines and their equivalence)
  - paper: doi:10.1145/320924.320930
    title: George N. Raney, Sequential functions, Journal of the ACM 5(2) (1958)
    locator: pp. 177 to 180 (the functions computed by finite sequential machines)
  - paper: doi:10.1109/12.272431
    title: David Lee and Mihalis Yannakakis, Testing finite-state machines, state identification and verification, IEEE Transactions on Computers 43(3) (1994)
    locator: pp. 306 to 320 (preset and adaptive distinguishing sequences)
  - paper: doi:10.1109/5.533956
    title: David Lee and Mihalis Yannakakis, Principles and methods of testing finite state machines, a survey, Proceedings of the IEEE 84(8) (1996)
    locator: pp. 1090 to 1123 (homing, synchronizing and distinguishing sequences, and checking experiments)
---

A Mealy machine is a [deterministic finite automaton](/deterministic-finite-automaton/) that writes one output symbol on each transition. The output symbol depends on the current state and on the input symbol that the machine reads. So the machine turns each input string into an output string of the same length, in one left-to-right pass with constant memory. Mealy machines model synchronous digital circuits, protocol controllers and other reactive systems. They have the same power as [Moore machines](/moore-machine/), whose output depends only on the state, but they can need fewer states.

## The machine

A Mealy machine is a tuple $M = (Q, \Sigma, \Delta, \delta, \lambda, q_0)$, where

- $Q$ is a finite, non-empty set of states,
- $\Sigma$ is a finite input [alphabet](/alphabet/) and $\Delta$ is a finite output alphabet,
- $\delta : Q \times \Sigma \to Q$ is the transition function,
- $\lambda : Q \times \Sigma \to \Delta$ is the output function, and
- $q_0 \in Q$ is the start state.

This is the notation $(Q, \Sigma, \delta, q_0)$ of the DFA pages, with an output function in place of the set $F$. The machine is *complete*: $\delta$ and $\lambda$ are total functions. It has no $\varepsilon$-moves, and it writes exactly one symbol of $\Delta$ on each move. A machine with partial functions can be completed with a dead state, as for a DFA, if the output on the missing moves does not matter.

**Runs and the output.** On an input $w = a_1 a_2 \cdots a_n$, the run is $r_0, r_1, \ldots, r_n$ with $r_0 = q_0$ and $r_i = \delta(r_{i-1}, a_i)$, and the output is

$$T_M(w) = \lambda(r_0, a_1)\, \lambda(r_1, a_2) \cdots \lambda(r_{n-1}, a_n) \in \Delta^n.$$

In terms of the extended functions, $\delta^*$ is as for a DFA, and $\lambda^* : Q \times \Sigma^* \to \Delta^*$ is defined by $\lambda^*(q, \varepsilon) = \varepsilon$ and $\lambda^*(q, wa) = \lambda^*(q, w)\, \lambda(\delta^*(q, w), a)$. Then $T_M(w) = \lambda^*(q_0, w)$. More generally, $T_q(w) = \lambda^*(q, w)$ is the function computed from the state $q$.

**Lemma.** For each state $q$ and all $x, y \in \Sigma^*$, $\lambda^*(q, xy) = \lambda^*(q, x)\, \lambda^*(\delta^*(q, x), y)$.

*Proof.* By induction on $|y|$. For $y = \varepsilon$ both sides are $\lambda^*(q, x)$. For $y = y'a$, the definition gives $\lambda^*(q, xy'a) = \lambda^*(q, xy')\, \lambda(\delta^*(q, xy'), a)$. By the induction hypothesis and the DFA lemma $\delta^*(q, xy') = \delta^*(\delta^*(q, x), y')$, this is $\lambda^*(q, x)\, \lambda^*(\delta^*(q, x), y')\, \lambda(\delta^*(\delta^*(q, x), y'), a)$, which is $\lambda^*(q, x)\, \lambda^*(\delta^*(q, x), y'a)$ by the definition. $\square$

**Example: the serial adder.** Two binary numbers are read together, least significant digit first, one pair of digits per step. So $\Sigma = \{0, 1\}^2$ and $\Delta = \{0, 1\}$. The state is the carry, $Q = \{0, 1\}$ and $q_0 = 0$. On the pair $(x, y)$ in state $c$, the machine writes $(x + y + c) \bmod 2$ and moves to the carry $\lfloor (x + y + c)/2 \rfloor$.

| state | $(0,0)$ | $(0,1)$ | $(1,0)$ | $(1,1)$ |
|---|---|---|---|---|
| 0 | 0, out 0 | 0, out 1 | 0, out 1 | 1, out 0 |
| 1 | 0, out 1 | 1, out 0 | 1, out 0 | 1, out 1 |

Each entry gives the next state and the output. To add $6 = 110_2$ and $3 = 011_2$, the input is $(0,1), (1,1), (1,0), (0,0)$, with a final pair $(0,0)$ that flushes the carry. The run is $0, 0, 1, 1, 0$ and the output is $1, 0, 0, 1$, which is $1001_2 = 9$ read from the most significant digit. A script checked this run.

## What it counts

The cost of a run is the number of steps. A step reads one input symbol, looks up one entry of $\delta$ and one of $\lambda$, and writes one output symbol. On an input of length $n$ the machine makes $n$ steps and writes $n$ symbols, and it writes the $i$-th output symbol before it reads the $(i+1)$-th input symbol. So $|T_M(w)| = |w|$, and $T_M(x)$ is a prefix of $T_M(xy)$ by the lemma. The only memory is the current state.

The size of a machine is its number of states. The size of the tables is $|Q| \cdot |\Sigma|$ entries for $\delta$ and as many for $\lambda$.

**Which functions a Mealy machine computes.** For a function $f : \Sigma^* \to \Delta^*$ that preserves lengths and prefixes, the *residual* of $f$ at $x$ is the function $f_x$ with $f(xy) = f(x)\, f_x(y)$ for all $y$. Raney (1958) characterized these functions: $f = T_M$ for some Mealy machine $M$ if and only if

1. $|f(w)| = |w|$ for every $w$,
2. $f(x)$ is a prefix of $f(xy)$ for all $x, y$, and
3. $f$ has only finitely many distinct residuals.

Moreover, the least number of states of a Mealy machine for $f$ is the number of distinct residuals.

*Proof.* If $f = T_M$, then (1) and (2) hold as shown above, and by the lemma $f_x = T_{\delta^*(q_0, x)}$, so there are at most $|Q|$ residuals, and at least as many states as residuals. Conversely, suppose (1), (2) and (3) hold. Take the residuals as states, with start $f_\varepsilon = f$, $\delta(f_x, a) = f_{xa}$ and $\lambda(f_x, a) = f_x(a)$, a single symbol by (1). These are well defined: $f(xay) = f(x)\, f_x(ay)$ and also $f(xay) = f(xa)\, f_{xa}(y) = f(x)\, f_x(a)\, f_{xa}(y)$, so $f_{xa}(y)$ is $f_x(ay)$ without its first symbol, and it depends only on $f_x$. By induction on $|y|$, the machine writes $f_x(y)$ from the state $f_x$ on input $y$, so it computes $f$. $\square$

This is the [Myhill-Nerode](/myhill-nerode-relation/) theorem for Mealy machines. The residual machine is the *minimal* Mealy machine of $f$, and it is unique up to a renaming of the states.

## Relation to other models

- **DFAs.** A Mealy machine without its output function is a DFA without accepting states. A DFA $(Q, \Sigma, \delta, q_0, F)$ becomes a Mealy machine with $\Delta = \{0, 1\}$ and $\lambda(q, a) = 1$ if and only if $\delta(q, a) \in F$. The last output symbol on a non-empty input then says whether the DFA accepts it.
- **Moore machines.** A [Moore machine](/moore-machine/) writes a symbol that depends only on the state it enters. Each Moore machine with $n$ states has an equivalent Mealy machine with the same $n$ states, with $\lambda(q, a)$ the output of $\delta(q, a)$. A Mealy machine with $n$ states has an equivalent Moore machine with at most $n |\Delta|$ states, the pairs (state, last output). Both translations ignore the first output of the Moore machine, which comes before any input. The factor $|\Delta|$ is needed in the worst case; see the known results.
- **Finite-state transducers.** A Mealy machine is a deterministic [finite-state transducer](/finite-state-transducer/) in which every move reads one symbol and writes one symbol, and every state is final. Sequential transducers relax the second rule and write a string on each move.
- **Boolean circuits.** A synchronous sequential circuit is a Mealy machine: a register holds the state in $\lceil \lg |Q| \rceil$ binary digits, and a [Boolean circuit](/boolean-circuit/) computes the next state and the output from the state and the input. Mealy (1955) introduced the model to synthesize such circuits.
- **Cascades.** Feeding the output of one Mealy machine into another gives a Mealy machine on the product of the state sets. The [Krohn-Rhodes theorem](/krohn-rhodes-theorem/) says that every Mealy machine can be simulated by a cascade of machines whose transformations are simple groups or two-state resets.
- **Weighted and probabilistic models.** A [weighted automaton](/weighted-automaton/) gives weights instead of symbols, and a [hidden Markov model](/hidden-markov-model/) is a Moore or Mealy machine with random transitions and outputs.

## Known results in the model

Below, $n = |Q|$, $\sigma = |\Sigma|$ and $k = |\Delta|$.

### Equivalence and minimization

Two states $p$ and $q$ are *equivalent* if $T_p = T_q$, that is, $\lambda^*(p, w) = \lambda^*(q, w)$ for every $w$.

- **Short separating inputs.** If $p$ and $q$ are not equivalent, they write different outputs on some input of length at most $n - 1$. Let $p \sim_i q$ mean that the outputs agree on all inputs of length at most $i$. As in [Moore's algorithm](/moore-minimization/), $p \sim_{i+1} q$ if and only if $\lambda(p, a) = \lambda(q, a)$ and $\delta(p, a) \sim_i \delta(q, a)$ for each $a$, so once $\sim_{i+1} = \sim_i$ the relations stay fixed. If $\sim_1$ has one class, all states write the same symbol for each input symbol, so $\sim_2 = \sim_1$ and all states are equivalent. Otherwise $\sim_1$ has at least two classes, each strict refinement adds a class, and there are at most $n$ classes, so $\sim_{n-1}$ is the final relation. The bound is reached: on the chain $0 \to 1 \to \cdots \to n - 1$ over one input symbol, with a loop at $n - 1$ and the output 1 only on the move out of $n - 1$, the states 0 and 1 first differ at step $n - 1$. A script checked this chain for $n = 2, \ldots, 8$, and checked the bound on 20000 random machines.
- **Minimization.** The minimal machine is the quotient of the reachable part by equivalence. [Moore's algorithm](/moore-minimization/) and [Hopcroft's algorithm](/hopcroft-minimization/) compute it when they start from the partition by the row $(\lambda(q, a))_{a \in \Sigma}$ instead of $F$ and $Q \setminus F$. Hopcroft's algorithm takes $O(\sigma n \log n)$ time for any initial partition.
- **Equivalence of two machines.** Run the search of [DFA equivalence](/dfa-equivalence/) on the product, with a pair *bad* when the two states write different symbols on some input symbol. The union-find method of Hopcroft and Karp also applies and takes $O(\sigma n \alpha(n))$ time with $n$ the total number of states.

### Mealy and Moore sizes

The Moore machine built from a Mealy machine has the states $(q, b)$ with $b \in \Delta$, the output $b$ in the state $(q, b)$, and the moves $(q, b) \xrightarrow{a} (\delta(q, a), \lambda(q, a))$. Two of its states reached by non-empty inputs are equivalent if and only if they have the same $b$ and equivalent $q$, so the minimal Moore machine has one state per such reachable pair, plus one start state if no pair has a $q$ equivalent to $q_0$.

- The serial adder has 2 states as a Mealy machine and 4 as a Moore machine: the pairs (carry, last sum digit).
- The factor $k$ is needed for every $n \ge 1$ and $k \ge 2$. Take $Q = \{0, \ldots, n-1\}$, $\Delta = \{0, \ldots, k-1\}$ and $\Sigma = \Delta \cup \{t\}$. A symbol $b \in \Delta$ writes $b$ and moves from $q$ to $q + 1 \bmod n$. The symbol $t$ writes 1 in state 0 and 0 in the other states, and does not move. The $n$ states are pairwise inequivalent, since $b^j t$ for a suitable $j$ separates them, and every pair $(q, b)$ is reached, so the minimal Moore machine has $nk$ states. A script checked this for $n \le 6$ and $k \le 4$.

### Testing and identification

These problems ask what an experimenter learns about an unknown state by applying inputs and watching the outputs. They come from Moore (1956).

- A *distinguishing sequence* is an input on which all states write different outputs, so it reveals the start state. Lee and Yannakakis (1994) showed that deciding whether a machine has a *preset* distinguishing sequence is PSPACE-complete, while the existence of an *adaptive* one, where the next input may depend on the outputs seen, can be decided in polynomial time.
- A *homing sequence* is an input after which the output determines the current state. Every minimal machine has one, and one can be found in polynomial time.
- *Checking experiments* test whether a black-box machine with at most a given number of states is equivalent to a specification. They are the basis of conformance testing of protocols (Lee and Yannakakis, 1996).

### Learning

The [L* algorithm](/lstar-algorithm/) learns a DFA from membership and equivalence queries. Its variants for Mealy machines ask for the output on an input instead of a membership bit, and they learn the minimal machine with a number of queries polynomial in $n$, $\sigma$ and the length of the counterexamples. Active learning of models of network protocols and embedded software uses these variants.

### Pitfalls

- **Output length conventions.** A Mealy machine writes $|w|$ symbols and a Moore machine, in the convention of Moore and of Hopcroft and Ullman, writes $|w| + 1$. Translations between them drop the first Moore output. Comparing the two without this care gives off-by-one errors.
- **Timing in circuits.** In a Mealy circuit the output depends on the current input directly, so a change of the input can change the output within the same clock cycle. Two Mealy circuits in a loop can form a combinational cycle. A Moore circuit avoids this at the cost of one step of delay.
- **Minimizing with $F$.** Minimization must start from the partition by output rows. Starting from a single block, or from a partition by one input symbol only, merges states with different outputs.
- **Unreachable states.** As for DFAs, remove them before minimization, or the result is not minimal.

## References
