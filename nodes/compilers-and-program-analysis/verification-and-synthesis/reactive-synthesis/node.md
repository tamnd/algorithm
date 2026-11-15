---
tag: R9BHD9
kind: problem
slug: reactive-synthesis
name: Reactive synthesis
aliases:
- LTL synthesis
- Church's synthesis problem
area: compilers-and-program-analysis/verification-and-synthesis
level: advanced
summary: Given a temporal logic specification over inputs and outputs, build a finite-state system whose outputs meet it for all input sequences.
prereqs: [program-synthesis, linear-temporal-logic, parity-game]
see_also: [pnueli-rosner-theorem, ltl-to-buchi-translation, zielonka-algorithm, parity-game-solving, ltl-satisfiability, mealy-machine, automata-theoretic-approach, supervisory-control-theory]
sources:
  - paper: "Alonzo Church, Applications of recursive arithmetic to the problem of circuit synthesis, Summaries of the Summer Institute of Symbolic Logic, vol. I, Cornell University, Ithaca, 1957, pp. 3-50"
    locator: the first statement of the problem, for circuits that map input streams to output streams under a specification in a logic of sequences
  - paper: doi:10.2307/1994916
    title: J. Richard Büchi and Lawrence H. Landweber, Solving sequential conditions by finite-state strategies, Transactions of the American Mathematical Society 138, 1969
    locator: pp. 295-311, Church's problem for S1S is decidable, the game is determined, and the winner has a finite-state strategy
  - paper: doi:10.1145/75277.75293
    title: Amir Pnueli and Roni Rosner, On the synthesis of a reactive module, Principles of Programming Languages (POPL 1989)
    locator: pp. 179-190, the definition of realizability of LTL by a reactive module, its difference from satisfiability, and the doubly exponential algorithm through tree automata
  - paper: "Roni Rosner, Modular Synthesis of Reactive Systems, PhD thesis, Weizmann Institute of Science, Rehovot, 1992"
    locator: the matching 2EXPTIME lower bound for LTL realizability
  - paper: doi:10.1016/S0019-9958(66)80013-X
    title: Robert McNaughton, Testing and generating infinite sequences by a finite automaton, Information and Control 9(5), 1966
    locator: pp. 521-530, every Büchi automaton has an equivalent deterministic Muller automaton
  - paper: doi:10.1109/SFCS.1988.21948
    title: Shmuel Safra, On the complexity of omega-automata, Foundations of Computer Science (FOCS 1988)
    locator: pp. 319-327, determinization of a Büchi automaton with n states into a Rabin automaton with 2^O(n log n) states
  - paper: doi:10.1109/LICS.2006.28
    title: Nir Piterman, From nondeterministic Büchi and Streett automata to deterministic parity automata, Logic in Computer Science (LICS 2006)
    locator: pp. 255-264, a deterministic parity automaton with at most 2 n^n n! states and 2n priorities for a Büchi automaton with n states
  - paper: doi:10.1109/SFCS.1991.185392
    title: E. Allen Emerson and Charanjit S. Jutla, Tree automata, mu-calculus and determinacy, Foundations of Computer Science (FOCS 1991)
    locator: pp. 368-377, parity games are determined with positional (memoryless) winning strategies
  - paper: doi:10.1016/S0304-3975(98)00009-7
    title: Wiesław Zielonka, Infinite games on finitely coloured graphs with applications to automata on infinite trees, Theoretical Computer Science 200(1-2), 1998
    locator: pp. 135-183, the recursive algorithm for parity games and positional determinacy
  - paper: doi:10.1109/FSCS.1990.89597
    title: Amir Pnueli and Roni Rosner, Distributed reactive systems are hard to synthesize, Foundations of Computer Science (FOCS 1990)
    locator: pp. 746-757, synthesis for an architecture of several processes with partial information is undecidable in general
  - paper: doi:10.1016/j.jcss.2011.08.007
    title: Roderick Bloem, Barbara Jobstmann, Nir Piterman, Amir Pnueli and Yaniv Sa'ar, Synthesis of Reactive(1) designs, Journal of Computer and System Sciences 78(3), 2012
    locator: pp. 911-938, the GR(1) fragment and its symbolic algorithm by a nested fixpoint, polynomial in the size of the game graph (first version by Piterman, Pnueli and Sa'ar at VMCAI 2006, doi:10.1007/11609773_24)
  - paper: doi:10.1109/SFCS.2005.66
    title: Orna Kupferman and Moshe Y. Vardi, Safraless decision procedures, Foundations of Computer Science (FOCS 2005)
    locator: pp. 531-542, synthesis through universal co-Büchi automata, with no determinization
  - paper: doi:10.1007/978-3-540-75596-8_33
    title: Sven Schewe and Bernd Finkbeiner, Bounded synthesis, Automated Technology for Verification and Analysis (ATVA 2007)
    locator: pp. 474-488, a search for implementations of bounded size by constraint solving
  - paper: doi:10.1007/BFb0064872
    title: Albert R. Meyer, Weak monadic second order theory of successor is not elementary-recursive, Logic Colloquium, Lecture Notes in Mathematics 453, 1975
    locator: pp. 132-154, the non-elementary lower bound for the weak monadic theory of one successor
---

Reactive synthesis asks for a system that runs forever against an environment. At each step the environment sets the input signals, and the system then sets the output signals. The specification is a formula of [linear temporal logic](/linear-temporal-logic/) (LTL), or of another logic of infinite words, over both kinds of signals. The system must make the formula true for *every* sequence of inputs, so the problem is a game between the system and an adversarial environment, not a search for one good run. Church posed the problem in 1957. Büchi and Landweber (1969) solved it for the monadic logic S1S, and Pnueli and Rosner (1989) gave the doubly exponential algorithm for LTL, which the [Pnueli-Rosner theorem](/pnueli-rosner-theorem/) shows to be optimal.

## In plain words

Think of a controller for traffic lights. Cars arrive when they want, and the controller turns lights green and red. A rule might say: "two crossing roads are never green at the same time, and every waiting car gets a green light at some time". The task is to build a controller that keeps the rule, however the cars arrive.

The hard part is that the controller does not know the future. A rule can be easy to meet for one known arrival pattern and still impossible to keep for all of them. So the question is not "is there a good run?" but "is there a way to react that always wins?"

The usual solution turns the rule into a finite game board. A winning way to play on this board is a finite machine, and that machine is the controller.

## Definition

**Signals.** $I$ and $O$ are disjoint finite sets of atomic propositions, the inputs and the outputs. A letter is a set of true propositions, so the input letters are $\Sigma_I = 2^I$ and the output letters are $\Sigma_O = 2^O$.

**Strategy.** A strategy for the system is a function $\sigma : \Sigma_I^{+} \to \Sigma_O$. It maps the inputs seen so far, including the current one, to the current output. On an input word $x = x_0 x_1 x_2 \cdots$ it gives the *outcome*

$$ \mathrm{out}(\sigma, x) = (x_0 \cup \sigma(x_0))\,(x_1 \cup \sigma(x_0 x_1))\,(x_2 \cup \sigma(x_0 x_1 x_2)) \cdots, $$

an infinite word over $2^{I \cup O}$. The output at step $t$ depends only on the inputs up to step $t$: the strategy cannot see the future.

**Realizability.** A formula $\varphi$ over $I \cup O$ is *realizable* if some strategy $\sigma$ has $\mathrm{out}(\sigma, x) \models \varphi$ for every input word $x \in \Sigma_I^{\omega}$.

**Input.** The sets $I$ and $O$ and a formula $\varphi$.

**Output.** "Unrealizable", or a *finite-state* strategy that realizes $\varphi$: a [Mealy machine](/mealy-machine/) $M = (Q, q_0, \delta, \lambda)$ with a finite set of states $Q$, a transition function $\delta : Q \times \Sigma_I \to Q$ and an output function $\lambda : Q \times \Sigma_I \to \Sigma_O$. It reads $x_t$, writes $\lambda(q_t, x_t)$ and moves to $q_{t+1} = \delta(q_t, x_t)$.

**Realizability is not satisfiability.** $\varphi$ is satisfiable if *some* word over $2^{I \cup O}$ satisfies it. Realizability needs a good output for *every* input word, chosen step by step with no knowledge of later inputs. Two edge cases show the gap. If $O = \emptyset$, the system has no choice, and $\varphi$ is realizable exactly when it is valid over $2^I$. If $I = \emptyset$, the environment has no choice, and $\varphi$ is realizable exactly when it is satisfiable; a satisfiable LTL formula has an ultimately periodic model ([LTL satisfiability](/ltl-satisfiability/)), which a finite machine can produce.

## Variants

- **Moore strategies.** The system writes its output before it reads the input, so $\sigma : \Sigma_I^{\ast} \to \Sigma_O$. Some formulas, such as $\mathbf{G}(g \leftrightarrow r)$, are realizable as a Mealy machine and not as a Moore machine.
- **Church's problem.** The specification is a formula of S1S, the monadic second-order logic of one successor, or an automaton on infinite words. This is the first form of the problem.
- **GR(1) synthesis.** The specification has the form "safety and fairness assumptions on the environment imply safety and fairness guarantees of the system", with formulas $\mathbf{G}\mathbf{F}\, a$ as fairness. This fragment is solved in time polynomial in the size of the game graph (Piterman, Pnueli and Sa'ar 2006).
- **Bounded synthesis.** Look for an implementation with at most $k$ states, for $k = 1, 2, \ldots$, by a constraint problem for a SAT or [SMT](/smt-problem/) solver (Schewe and Finkbeiner 2007).
- **Distributed synthesis.** Several processes, each with its own partial view of the inputs, must together realize $\varphi$. This is undecidable in general (Pnueli and Rosner 1990).
- **Branching time.** The specification is a formula of [CTL](/computation-tree-logic/) or of the [modal mu-calculus](/modal-mu-calculus/) over the tree of all behaviours.

## Examples

Let $I = \{r\}$ and $O = \{g\}$.

- $\varphi_1 = \mathbf{G}(g \leftrightarrow r)$ is realizable by the Mealy machine with one state and $\lambda(q, x) = x$: the grant copies the request.
- $\varphi_2 = \mathbf{G}(g \leftrightarrow \mathbf{X}\, r)$ is satisfiable, for example by the word where $r$ and $g$ are always false. It is not realizable. Take any strategy $\sigma$ and let the environment play $x_0 = \emptyset$ and then $x_{t+1} = \{r\}$ exactly when $g \notin \sigma(x_0 \cdots x_t)$. Then $g$ at step 0 differs from $r$ at step 1, so $\varphi_2$ fails at step 0. The system would have to predict the next input.

**An arbiter.** Let $I = \{r_1, r_2\}$ and $O = \{g_1, g_2\}$, and

$$ \varphi_3 = \mathbf{G}\,\neg(g_1 \wedge g_2) \wedge \mathbf{G}(r_1 \rightarrow \mathbf{F}\, g_1) \wedge \mathbf{G}(r_2 \rightarrow \mathbf{F}\, g_2). $$

A Mealy machine with two states $A$ and $B$ realizes it: in $A$ it writes $g_1$ and moves to $B$, and in $B$ it writes $g_2$ and moves to $A$, whatever the input. The grants never overlap, and each grant comes back every second step, so every request is served. No machine with one state works: its output on the input $\{r_1, r_2\}$ is one fixed letter, and if the environment sends this input forever, one of the two grants never comes.

Now add "no grant without a current request", $\mathbf{G}(g_1 \rightarrow r_1) \wedge \mathbf{G}(g_2 \rightarrow r_2)$. The result $\varphi_4$ is satisfiable, for example by a word with no requests and no grants, but it is not realizable. The environment sends $\{r_1, r_2\}$ at step 0 and then $\emptyset$ forever. At step 0 the system can grant at most one request, and later it may grant nothing, so the other request is never served.

## Known algorithms

**Reduction to a parity game (the automata-theoretic method).** Let $n = |\varphi|$.

1. Translate $\varphi$ into a nondeterministic [Büchi automaton](/buchi-automaton/) $A$ with $2^{O(n)}$ states over the alphabet $2^{I \cup O}$ ([LTL to Büchi translation](/ltl-to-buchi-translation/)).
2. Determinize $A$ into a deterministic parity automaton $D$ (Safra 1988, Piterman 2006). For $m$ states in $A$, $D$ has at most $2 m^m m!$ states and $2m$ priorities. With $m = 2^{O(n)}$, this is $2^{2^{O(n)}}$ states and $2^{O(n)}$ priorities. A nondeterministic automaton is not enough, because the system would have to guess a run that must work for future inputs it has not seen.
3. Build the [parity game](/parity-game/): in a state $q$ of $D$ the environment picks $x \in \Sigma_I$, then the system picks $y \in \Sigma_O$, and the play moves to $\delta_D(q, x \cup y)$. The priority of a position is the priority of its state of $D$. The system wins a play if $D$ accepts the word of the play.
4. Solve the game, for example by [Zielonka's algorithm](/zielonka-algorithm/), or by a quasi-polynomial algorithm ([parity game solving](/parity-game-solving/)). If the system wins from the start, a positional winning strategy $s(q, x) = y$ is a Mealy machine with the states of $D$ as its states.

The [Pnueli-Rosner theorem](/pnueli-rosner-theorem/) page counts the cost: doubly exponential in $n$, and polynomial in the number of states of $D$ for a fixed number of priorities.

**Safraless methods.** Kupferman and Vardi (2005) avoid determinization. They dualize a Büchi automaton for $\neg\varphi$ into a universal co-Büchi automaton for $\varphi$, and reduce realizability to the emptiness of a nondeterministic Büchi tree automaton. Bounded synthesis encodes "an implementation with $k$ states whose runs the universal automaton accepts" as constraints, which is often small for real specifications.

**GR(1).** For specifications in the GR(1) form, a nested fixpoint over sets of states, in the style of the modal mu-calculus, computes the winning region and a strategy directly with binary decision diagrams (Piterman, Pnueli and Sa'ar 2006; Bloem and others 2012).

## Bounds

**Theorem (Büchi and Landweber 1969).** Church's problem for a formula of S1S is decidable. If the formula is realizable, it is realizable by a finite-state strategy, and if it is not, the environment has a finite-state strategy that defeats every strategy of the system.

*Proof.* Let $\varphi$ be the formula. By McNaughton's theorem (1966) there is a deterministic automaton $D$ with a Muller condition that accepts exactly the words that satisfy $\varphi$. A Muller condition can be turned into a parity condition by a finite memory of the order of last visits, so let $D$ be a deterministic parity automaton. Build the finite parity game $G$ of step 3 above.

Parity games on finite graphs are determined, and the winner has a positional winning strategy (Emerson and Jutla 1991; Zielonka 1998). The winner is also computable, because the game is finite: for example, Zielonka's algorithm decides it. So it is enough to show that the system wins $G$ from the start exactly when $\varphi$ is realizable.

Suppose the system wins with the positional strategy $s$. The Mealy machine $(Q_D, q_0, \delta, s)$ with $\delta(q, x) = \delta_D(q, x \cup s(q, x))$ is finite. On an input word $x$, the states of this machine are the run of $D$ on the outcome, and this run is a play of $G$ in which the system follows $s$. The play is won by the system, so $D$ accepts the outcome, and the outcome satisfies $\varphi$.

Suppose the environment wins with the positional strategy $e$. Take any strategy $\sigma$ of the system in the synthesis problem, with any memory. Because $D$ is deterministic, every history of inputs and outputs fixes one state of $D$, so $\sigma$ is also a strategy of the system in $G$. The play where the environment follows $e$ and the system follows $\sigma$ is won by the environment, so $D$ rejects this outcome, and $\sigma$ does not realize $\varphi$. So $\varphi$ is unrealizable, and $e$ is a finite-state strategy that defeats every $\sigma$. $\square$

The same proof works for LTL, through the translation into a Büchi automaton.

**Further bounds.**

- **LTL.** Realizability is 2EXPTIME-complete ([Pnueli-Rosner theorem](/pnueli-rosner-theorem/)). LTL satisfiability and validity, the cases $I = \emptyset$ and $O = \emptyset$, are only PSPACE-complete. The extra exponential comes from the adversarial environment.
- **S1S.** The cost is not elementary. The case $I = \emptyset$ is satisfiability of S1S, and Meyer (1975) proved that already the weak monadic theory of one successor, which S1S contains, is not elementary.
- **GR(1).** Polynomial in the size of the game graph. The graph itself can be exponential in the number of propositions.
- **Distributed architectures.** Undecidable in general (Pnueli and Rosner 1990).

## Reductions

- **To parity games.** The method above reduces LTL realizability to a parity game with doubly exponentially many positions and exponentially many priorities.
- **From satisfiability and validity.** With $I = \emptyset$ realizability is satisfiability, and with $O = \emptyset$ it is validity. So reactive synthesis is at least as hard as both.
- **Duality.** By the theorem above, $\varphi$ is unrealizable by a Mealy system exactly when $\neg\varphi$ is realizable by the environment as a Moore machine, which writes the next input before it sees the next output.
- **Supervisory control.** [Supervisory control theory](/supervisory-control-theory/) restricts a given plant by disabling some of its controllable events. This is a game of the same kind, with the uncontrollable events as the environment.

## Applications

- **Hardware controllers.** Arbiters, bus controllers and other small circuits whose behaviour has a clear temporal specification.
- **Robot controllers.** High-level plans for robots, written as GR(1) specifications over sensor inputs and actions.
- **Interfaces and protocols.** Components that must react correctly to any behaviour of their neighbours.
- **Checking specifications.** An unrealizable specification is a bug in the specification, and the environment strategy from the proof above shows how it fails.

## References
