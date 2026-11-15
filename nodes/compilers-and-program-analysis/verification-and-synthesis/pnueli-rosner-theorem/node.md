---
tag: R8YAMJ
kind: theorem
slug: pnueli-rosner-theorem
name: Pnueli-Rosner theorem
aliases:
- 2EXPTIME-completeness of LTL synthesis
area: compilers-and-program-analysis/verification-and-synthesis
level: research
summary: Synthesis of a reactive system from an LTL specification is complete for doubly exponential time.
prereqs: [reactive-synthesis, ltl-to-buchi-translation, zielonka-algorithm]
see_also: [parity-game-solving, ltl-satisfiability, ltl-model-checking-pspace-completeness, alternating-turing-machine, time-hierarchy-theorem, determinization-blowup-lower-bound, buchi-automaton, automata-theoretic-approach]
sources:
  - paper: doi:10.1145/75277.75293
    title: Amir Pnueli and Roni Rosner, On the synthesis of a reactive module, Principles of Programming Languages (POPL 1989)
    locator: pp. 179-190, realizability of LTL by a reactive module, decided in doubly exponential time through the emptiness of a deterministic tree automaton, with a finite-state module when one exists
  - paper: "Roni Rosner, Modular Synthesis of Reactive Systems, PhD thesis, Weizmann Institute of Science, Rehovot, 1992"
    locator: the proof that LTL realizability is 2EXPTIME-hard, which makes the upper bound of 1989 tight
  - paper: doi:10.2307/1994916
    title: J. Richard Büchi and Lawrence H. Landweber, Solving sequential conditions by finite-state strategies, Transactions of the American Mathematical Society 138, 1969
    locator: pp. 295-311, Church's problem for S1S is decidable, and finite-state strategies suffice
  - paper: doi:10.1006/inco.1994.1092
    title: Moshe Y. Vardi and Pierre Wolper, Reasoning about infinite computations, Information and Computation 115(1), 1994
    locator: pp. 1-37, the translation of an LTL formula of length n into a Büchi automaton with 2^O(n) states
  - paper: doi:10.1109/SFCS.1988.21948
    title: Shmuel Safra, On the complexity of omega-automata, Foundations of Computer Science (FOCS 1988)
    locator: pp. 319-327, determinization of Büchi automata with 2^O(m log m) states
  - paper: doi:10.1109/LICS.2006.28
    title: Nir Piterman, From nondeterministic Büchi and Streett automata to deterministic parity automata, Logic in Computer Science (LICS 2006)
    locator: pp. 255-264, a deterministic parity automaton with at most 2 m^m m! states and 2m priorities for a Büchi automaton with m states
  - paper: doi:10.1109/SFCS.1991.185392
    title: E. Allen Emerson and Charanjit S. Jutla, Tree automata, mu-calculus and determinacy, Foundations of Computer Science (FOCS 1991)
    locator: pp. 368-377, positional determinacy of parity games
  - paper: doi:10.1016/S0304-3975(98)00009-7
    title: Wiesław Zielonka, Infinite games on finitely coloured graphs with applications to automata on infinite trees, Theoretical Computer Science 200(1-2), 1998
    locator: pp. 135-183, the recursive algorithm for parity games
  - paper: doi:10.1145/3055399.3055409
    title: Cristian S. Calude, Sanjay Jain, Bakhadyr Khoussainov, Wei Li and Frank Stephan, Deciding parity games in quasipolynomial time, Symposium on Theory of Computing (STOC 2017)
    locator: pp. 252-263, parity games in time polynomial in the number of positions when the number of priorities is logarithmic, and quasi-polynomial in general
  - paper: doi:10.1145/322234.322243
    title: Ashok K. Chandra, Dexter C. Kozen and Larry J. Stockmeyer, Alternation, Journal of the ACM 28(1), 1981
    locator: pp. 114-133, alternating exponential space equals doubly exponential time
  - paper: doi:10.1109/SFCS.1977.32
    title: Amir Pnueli, The temporal logic of programs, Foundations of Computer Science (FOCS 1977)
    locator: pp. 46-57, linear temporal logic as a specification language for reactive programs
---

The Pnueli-Rosner theorem gives the exact complexity of [reactive synthesis](/reactive-synthesis/) from [linear temporal logic](/linear-temporal-logic/). Deciding whether an LTL formula over inputs and outputs is realizable is complete for 2EXPTIME, the class of problems solvable in time $2^{2^{p(n)}}$ for a polynomial $p$. Pnueli and Rosner gave the upper bound in 1989, and Rosner proved the lower bound in his thesis of 1992. The theorem explains a gap that surprises many readers: [LTL satisfiability](/ltl-satisfiability/) and [LTL model checking](/ltl-model-checking-pspace-completeness/) are PSPACE-complete, but realizability costs one more exponential, because the environment chooses the inputs as an adversary.

## Statement

Let $I$ and $O$ be disjoint sets of input and output propositions, and let $\varphi$ be an LTL formula over $I \cup O$ of length $n$. Realizability is defined on the [reactive synthesis](/reactive-synthesis/) page: some strategy $\sigma : (2^I)^{+} \to 2^O$ makes every outcome satisfy $\varphi$.

**Theorem (Pnueli and Rosner 1989, Rosner 1992).**

1. **Upper bound.** Realizability of $\varphi$ can be decided in time $2^{2^{O(n)}}$. If $\varphi$ is realizable, a Mealy machine with $2^{2^{O(n)}}$ states that realizes it can be built in the same time.
2. **Lower bound.** Realizability of LTL formulas is 2EXPTIME-hard.

So LTL realizability is 2EXPTIME-complete. The same holds for Moore strategies, where the output at a step does not depend on the input of that step.

## In plain words

A specification over inputs and outputs is given. The question is whether some controller keeps it against every possible input. The theorem says how much time this question needs in the worst case.

The answer is "doubly exponential": the time grows like two raised to two raised to the length of the specification. An algorithm reaches this bound, and no algorithm can do much better in general.

This is one level higher than the cost of asking whether some single run meets the specification. The extra level comes from the opponent. The controller must decide now, without knowing what the inputs will do later, so it must be ready for all futures at once.

## Proof

### Upper bound

The algorithm is the reduction to a parity game on the [reactive synthesis](/reactive-synthesis/) page. Its correctness is the Büchi-Landweber argument proved there. Here we count its cost. Let $k = |I| + |O| \le n$, so the alphabet $2^{I \cup O}$ has $2^k \le 2^n$ letters.

**Step 1: a Büchi automaton.** Build a nondeterministic [Büchi automaton](/buchi-automaton/) $A$ that accepts exactly the words that satisfy $\varphi$ ([LTL to Büchi translation](/ltl-to-buchi-translation/), Vardi and Wolper 1994). It has $m \le 2^{c n}$ states for a constant $c$, and it is built in time $2^{O(n)}$.

**Step 2: a deterministic parity automaton.** Determinize $A$ into a deterministic parity automaton $D$ with the same language (Piterman 2006). It has $N \le 2 m^m m!$ states and $d \le 2m$ priorities. Since $m! \le m^m$,

$$ N \le 2 m^{2m} = 2^{1 + 2m \log_2 m} \le 2^{1 + 2 c n 2^{c n}} = 2^{2^{O(n)}}, \qquad d \le 2^{c n + 1} = 2^{O(n)}. $$

The construction takes time polynomial in $N$ and $2^k$, so $2^{2^{O(n)}}$.

**Step 3: the game.** The [parity game](/parity-game/) $G$ has an environment position $q$ for each state of $D$ and a system position $(q, x)$ for each state and input letter. The environment moves from $q$ to $(q, x)$, and the system moves from $(q, x)$ to $\delta_D(q, x \cup y)$ for an output letter $y$. Both positions carry the priority of $q$. The game has

$$ P = N + N 2^{|I|} \le N 2^{n+1} \text{ positions}, \qquad E = N 2^{|I|} + N 2^{|I|} 2^{|O|} \le N 2^{n+1} \text{ moves}, $$

so $P$ and $E$ are $2^{2^{O(n)}}$, and the game has $d$ priorities.

**Step 4: solving the game.** [Zielonka's algorithm](/zielonka-algorithm/) solves a parity game with $P$ positions, $E$ moves and $d$ priorities in time $O(E (P + 1)^d)$ and returns positional winning strategies. With the bounds above,

$$ E (P + 1)^d \le \left(2^{2^{a n}}\right)^{d + 1} \le 2^{2^{a n} \cdot (2^{c n + 1} + 1)} = 2^{2^{O(n)}} $$

for a constant $a$. Here the exponent $d$ is exponential in $n$, but it multiplies an exponent that is already exponential, so the result stays doubly exponential.

**Step 5: the answer.** By the Büchi-Landweber argument, $\varphi$ is realizable exactly when the system wins $G$ from the initial state of $D$. In that case a positional strategy $s(q, x) = y$ of the system is a Mealy machine with the $N = 2^{2^{O(n)}}$ states of $D$. The total time of the four steps is $2^{2^{O(n)}}$, which proves part 1.

For Moore strategies, swap the order of the moves: the system picks $y$ in $q$, and then the environment picks $x$. The counts do not change.

**Why the automaton must be deterministic.** If the game were played on the states of $A$, with the system choosing the next state of $A$, a win of the system would still give a correct strategy. But a loss would not prove that $\varphi$ is unrealizable, because the system would have to resolve the choices of $A$ before it sees the future inputs. Take $I = \{a\}$, $O = \emptyset$ and the valid formula $\varphi = \mathbf{F}\mathbf{G}\, a \vee \mathbf{G}\mathbf{F}\, \neg a$, with $A$ the union of the usual two-state automaton for $\mathbf{F}\mathbf{G}\, a$, which guesses when $a$ stays true forever, and a deterministic automaton for $\mathbf{G}\mathbf{F}\, \neg a$. If the system picks the second part, the environment plays $a$ forever. If it picks the first part, the environment plays $\neg a$ right after the guess, or the system never guesses. In each case $A$ rejects the play, so the system loses the game on $A$, yet $\varphi$ is realizable, since it holds on every word. Determinization removes the choice.

### Lower bound

Rosner (1992, PhD thesis) proved that LTL realizability is 2EXPTIME-hard: there is a polynomial-time reduction from every problem in 2EXPTIME to the realizability of LTL formulas. The proof is not repeated here.

As context for the bound: by the theorem of Chandra, Kozen and Stockmeyer (1981), 2EXPTIME equals the class of problems decided by [alternating Turing machines](/alternating-turing-machine/) in exponential space. Realizability has the same shape: two players with opposite goals, and a winning condition that needs an exponentially large automaton to check.

Two easier lower bounds follow at once from the special cases on the [reactive synthesis](/reactive-synthesis/) page. With $O = \emptyset$, realizability is validity, and with $I = \emptyset$, it is satisfiability. Both are PSPACE-complete for LTL, so realizability is at least PSPACE-hard by these reductions alone. The thesis lifts this to 2EXPTIME. $\square$

## Consequences

- **Realizability is not satisfiability.** By the time hierarchy theorem, EXPTIME is a proper subclass of 2EXPTIME. So LTL realizability is not in EXPTIME, while satisfiability is in PSPACE, which is inside EXPTIME. The adversarial environment adds at least one exponential that cannot be removed.
- **Finite-state controllers suffice.** A realizable LTL formula is realized by a Mealy machine with $2^{2^{O(n)}}$ states. No controller with infinite memory is ever needed.
- **Parity game solving is not the bottleneck.** Even Zielonka's algorithm, which is exponential in the number of priorities, stays inside the doubly exponential bound, as step 4 shows. A faster solver from [parity game solving](/parity-game-solving/), such as the quasi-polynomial algorithm of Calude and others (2017), makes the solving step cheaper but does not change the bound. The blowup comes from the determinization in step 2.
- **Fragments.** Practical tools work in fragments of LTL with cheaper determinization, such as GR(1), or search for small implementations directly, as in bounded synthesis on the [reactive synthesis](/reactive-synthesis/) page.

## Tightness

- **Both exponentials are needed.** The lower bound shows that no algorithm runs in time $2^{p(n)}$ for a polynomial $p$, by the time hierarchy theorem. The upper bound shows that time $2^{2^{O(n)}}$ is enough.
- **Determinization is the source of the second exponential.** The Büchi automaton of step 1 is exponential in $n$, and some Büchi automata need deterministic automata that are exponentially larger again, even on finite words ([determinization blowup lower bound](/determinization-blowup-lower-bound/)). A deterministic automaton is needed, as the example in the proof shows.
- **Satisfiability and model checking stay in PSPACE.** With no adversary, the same formula needs only a search for one lasso-shaped run, and the nondeterministic automaton of step 1 is enough.
- **Richer logics cost more.** For S1S the problem is still decidable (Büchi and Landweber 1969), but not elementary, because already its satisfiability is not elementary.

## History

Church posed the synthesis problem for circuits in 1957. Büchi and Landweber (1969) solved it for S1S with finite-state strategies. Pnueli (1977) proposed LTL for reasoning about reactive programs. Pnueli and Rosner (1989) defined the realizability of LTL by a reactive module, pointed out that it differs from satisfiability, and gave an algorithm through deterministic tree automata. Its time is doubly exponential, with Safra's determinization of 1988 as the key step. Rosner's thesis (1992) proved the matching lower bound. Piterman (2006) gave a direct determinization into parity automata, which is the form used in the proof above.

## References
