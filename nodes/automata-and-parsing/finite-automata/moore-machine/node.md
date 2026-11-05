---
tag: DKZHB2
kind: model
slug: moore-machine
name: Moore machine
aliases:
- Moore automaton
area: automata-and-parsing/finite-automata
level: core
summary: Finite-state transducer whose output depends only on the current state.
prereqs: [deterministic-finite-automaton, alphabet]
see_also:
- mealy-machine
- finite-state-transducer
- moore-minimization
- hopcroft-minimization
- myhill-nerode-relation
- dfa-equivalence
- hidden-markov-model
- boolean-circuit
sources:
  - paper: "Edward F. Moore, Gedanken-experiments on sequential machines, in C. E. Shannon and J. McCarthy (eds.), Automata Studies, Annals of Mathematics Studies 34, Princeton University Press, 1956"
    locator: pp. 129 to 153 (machines with an output for each state, equivalent states, experiments and the reduced machine)
  - book: isbn:9780201029888
    title: John E. Hopcroft and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, first edition, 1979
    locator: Section 2.7, Finite Automata with Output (Moore and Mealy machines and their equivalence)
  - paper: doi:10.1002/j.1538-7305.1955.tb03788.x
    title: George H. Mealy, A method for synthesizing sequential circuits, The Bell System Technical Journal 34(5) (1955)
    locator: pp. 1045 to 1079 (the comparison with machines whose output depends only on the state)
  - paper: doi:10.1109/5.533956
    title: David Lee and Mihalis Yannakakis, Principles and methods of testing finite state machines, a survey, Proceedings of the IEEE 84(8) (1996)
    locator: pp. 1090 to 1123 (state identification and checking experiments)
---

A Moore machine is a [deterministic finite automaton](/deterministic-finite-automaton/) that has an output symbol for each state. Each time it enters a state, it writes the output of that state. So the output at each moment depends only on the current state, and it reports a property of the input read so far. A DFA is the special case with the outputs "accept" and "reject". Moore machines and [Mealy machines](/mealy-machine/) compute the same functions, but a Moore machine may need more states, and its output reacts to an input symbol one step later.

## The machine

A Moore machine is a tuple $M = (Q, \Sigma, \Delta, \delta, \lambda, q_0)$, where

- $Q$ is a finite, non-empty set of states,
- $\Sigma$ is a finite input [alphabet](/alphabet/) and $\Delta$ is a finite output alphabet,
- $\delta : Q \times \Sigma \to Q$ is the transition function,
- $\lambda : Q \to \Delta$ is the output function, and
- $q_0 \in Q$ is the start state.

The notation is that of the DFA pages, with $\lambda$ in place of $F$. The machine is *complete*, since $\delta$ and $\lambda$ are total, and it has no $\varepsilon$-moves.

**Runs and the output.** On an input $w = a_1 \cdots a_n$, the run is $r_0, \ldots, r_n$ with $r_0 = q_0$ and $r_i = \delta(r_{i-1}, a_i)$, and the output is

$$T_M(w) = \lambda(r_0)\, \lambda(r_1) \cdots \lambda(r_n) \in \Delta^{n+1}.$$

This is the convention of Moore (1956) and of Hopcroft and Ullman (1979): the first symbol $\lambda(q_0)$ is written before any input. When a Moore machine is compared with a Mealy machine, this first symbol is dropped. The *last output* is the function $g_M(w) = \lambda(\delta^*(q_0, w))$, and $T_M(w)$ lists $g_M$ on the prefixes of $w$. So a Moore machine is the same thing as a DFA that classifies each input into one of $|\Delta|$ classes.

**DFAs as Moore machines.** A DFA $(Q, \Sigma, \delta, q_0, F)$ is the Moore machine with $\Delta = \{0, 1\}$ and $\lambda(q) = 1$ if and only if $q \in F$. Then $g_M(w) = 1$ if and only if the DFA accepts $w$.

**Example 1: the residue modulo 3.** Let $\Sigma = \{0, 1\}$, $\Delta = Q = \{0, 1, 2\}$, $q_0 = 0$, $\delta(r, b) = (2r + b) \bmod 3$ and $\lambda(r) = r$. The machine reads a binary number from the most significant digit and always shows the value of the prefix modulo 3. On $10010$, the number 18, the run is $0, 1, 2, 1, 0, 0$, and so is the output: the prefixes $\varepsilon, 1, 10, 100, 1001, 10010$ have the values $0, 1, 2, 4, 9, 18$, with the residues $0, 1, 2, 1, 0, 0$. A script checked this run.

**Example 2: the last symbol.** Let $\Sigma = \Delta = \{a, b\}$, $Q = \{A, B\}$, $q_0 = A$, $\lambda(A) = a$, $\lambda(B) = b$, and $\delta(q, a) = A$, $\delta(q, b) = B$ for both states. After a non-empty input the output is its last symbol. On $abba$ the output is $a\,a\,b\,b\,a$, where the first $a$ is the output of the start state.

## What it counts

The cost of a run is the number of steps. A step reads one input symbol, looks up one entry of $\delta$, and writes the output of the new state. On an input of length $n$ the machine makes $n$ steps and writes $n + 1$ symbols. The only memory is the current state, so the output after a prefix $x$ depends only on $\delta^*(q_0, x)$.

The size of a machine is its number of states. The tables have $|Q| \cdot |\Sigma|$ entries for $\delta$ and $|Q|$ for $\lambda$.

**Which functions a Moore machine computes.** For a function $g : \Sigma^* \to \Delta$, let $x \equiv_g y$ if $g(xz) = g(yz)$ for all $z \in \Sigma^*$. Then $g = g_M$ for some Moore machine $M$ if and only if $\equiv_g$ has finitely many classes, and the least number of states is the number of classes.

*Proof.* If $g = g_M$ and $\delta^*(q_0, x) = \delta^*(q_0, y)$, then $\delta^*(q_0, xz) = \delta^*(q_0, yz)$ for each $z$ by the DFA lemma, so $x \equiv_g y$. Hence each class of $\equiv_g$ is a union of the sets $\{ x : \delta^*(q_0, x) = q \}$ over some reachable states $q$, and there are at most $|Q|$ classes. Conversely, if there are finitely many classes, take them as the states, with start $[\varepsilon]$, $\delta([x], a) = [xa]$ and $\lambda([x]) = g(x)$. These are well defined: if $x \equiv_g y$ then $xa \equiv_g ya$ (take $z = a z'$), and $g(x) = g(y)$ (take $z = \varepsilon$). By induction on $|w|$, $\delta^*([\varepsilon], w) = [w]$, so the machine computes $g$. $\square$

This is the [Myhill-Nerode](/myhill-nerode-relation/) theorem with $\Delta$ in place of $\{0, 1\}$. The class machine is the *minimal* Moore machine of $g$, and it is unique up to a renaming of the states.

## Relation to other models

- **Mealy machines.** A [Mealy machine](/mealy-machine/) writes a symbol on each move, $\lambda : Q \times \Sigma \to \Delta$. A Moore machine with $n$ states becomes a Mealy machine with the same states and $\lambda'(q, a) = \lambda(\delta(q, a))$; the outputs agree except for the first Moore symbol. A Mealy machine with $n$ states becomes a Moore machine on the pairs (state, last output), with at most $n |\Delta|$ states, and this factor is needed in the worst case (see the Mealy page). The gap can also be large in the other direction: Example 2 has $|\Sigma|$ states as a Moore machine, one per possible last symbol, but one state as a Mealy machine, which writes the symbol it reads.
- **DFAs.** A DFA is a Moore machine with two outputs, as above. A Moore machine with output alphabet $\Delta$ is the same as $|\Delta|$ DFAs that share their states and have disjoint accepting sets, one for each $g^{-1}(b)$.
- **Finite-state transducers.** A Moore machine is a deterministic [finite-state transducer](/finite-state-transducer/) in which every move writes one symbol, the symbol of its target state, plus an initial output.
- **Circuits.** In a Moore circuit, the output is a [Boolean circuit](/boolean-circuit/) applied to the state register alone. So the output is stable during a clock cycle and does not depend on the input of that cycle. This is why hardware designers often prefer Moore machines for control units.
- **Hidden Markov models.** A [hidden Markov model](/hidden-markov-model/) is a Moore machine in which the transitions and the outputs are random, with no input.

## Known results in the model

Below, $n = |Q|$ and $\sigma = |\Sigma|$.

### Equivalence and minimization

Two states $p$ and $q$ are *equivalent* if $\lambda(\delta^*(p, z)) = \lambda(\delta^*(q, z))$ for every $z$.

- **Short separating inputs.** Let $c$ be the number of distinct values of $\lambda$ on the reachable states. If $c = 1$, all reachable states are equivalent. Otherwise, two states that are not equivalent write different outputs on some input of length at most $n - c \le n - 2$. The proof is the round count of [Moore's algorithm](/moore-minimization/), which starts with $c$ classes and adds at least one class in each round that splits. This is Moore's result that experiments of bounded length suffice to tell states apart.
- **Minimization.** Moore's algorithm and [Hopcroft's algorithm](/hopcroft-minimization/) minimize a Moore machine when they start from the partition by the value of $\lambda$. This takes $O(\sigma n^2)$ and $O(\sigma n \log n)$ time. The result is the minimal machine of the theorem above.
- **Equivalence of two machines.** The search of [DFA equivalence](/dfa-equivalence/) applies, with a pair of states *bad* when their outputs differ. It takes $O(\sigma n_1 n_2)$ time on the product, or $O(\sigma n \alpha(n))$ with the union-find method of Hopcroft and Karp.

### Experiments

Moore (1956) asked what an observer learns about a machine in an unknown state by feeding inputs and reading outputs. He gave a machine in which every two states can be told apart by some input, but no single experiment on one copy finds the start state, because an input that separates one pair of states sends another pair to the same state. Homing sequences, distinguishing sequences and checking experiments grew from these questions; the [Mealy machine](/mealy-machine/) page gives the main complexity results, which hold for Moore machines through the translation above (Lee and Yannakakis, 1996).

### Pitfalls

- **The first output.** The output $\lambda(q_0)$ comes before any input. Code that writes one symbol per input symbol drops it, and tests that compare against a Mealy machine must drop it too.
- **Delay.** A Moore machine reacts to an input symbol only in the output of the next state, so its output for the input read so far is always visible, but it cannot react within the step. A specification such as "write 1 in the same step in which the input is $a$" needs a Mealy machine. A Moore machine meets it only with the output one step later, as in Example 2.
- **Minimizing with two blocks.** Minimization must start from one block per output value. Starting from "output 0" and "any other output" merges states with different outputs.
- **The size of the conversion.** Converting a Mealy machine to a Moore machine can multiply the number of states by $|\Delta|$. The usual construction makes all pairs (state, output), many of them unreachable, so it should be followed by a reachability pass.

## References
