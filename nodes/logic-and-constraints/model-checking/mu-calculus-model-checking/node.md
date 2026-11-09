---
tag: NNPB2C
kind: problem
slug: mu-calculus-model-checking
name: Modal mu-calculus model checking
aliases:
- Mu-calculus model checking
- L-mu model checking
area: logic-and-constraints/model-checking
level: advanced
summary: Decide whether a state of a Kripke structure satisfies a modal mu-calculus formula. It is in NP ∩ co-NP and quasi-polynomial time, it is P-hard, and it is equivalent to solving parity games.
prereqs: [modal-mu-calculus, kripke-structure, fixed-point]
see_also: [modal-mu-calculus, emerson-lei-algorithm, parity-game, parity-game-solving, zielonka-algorithm, ctl-model-checking, local-model-checking, symbolic-model-checking]
sources:
  - paper: "E. Allen Emerson and Chin-Laung Lei, Efficient model checking in fragments of the propositional mu-calculus, Proceedings of the First IEEE Symposium on Logic in Computer Science (LICS 1986), pages 267 to 278"
    locator: the evaluation of nested fixed points with reuse of inner values, polynomial for each fixed alternation depth
  - paper: "E. Allen Emerson, Charanjit S. Jutla and A. Prasad Sistla, On model-checking for fragments of mu-calculus, CAV 1993, Lecture Notes in Computer Science 697, Springer"
    locator: the polynomial-time equivalence of mu-calculus model checking and parity games, and membership in NP ∩ co-NP
  - paper: doi:10.1016/S0020-0190(98)00150-1
    title: Marcin Jurdziński, Deciding the winner in parity games is in UP ∩ co-UP, Information Processing Letters 68(3), 1998, pages 119 to 124
    locator: the main theorem, which with the equivalence above places mu-calculus model checking in UP ∩ co-UP
  - paper: doi:10.1145/3055399.3055409
    title: Cristian S. Calude, Sanjay Jain, Bakhadyr Khoussainov, Wei Li and Frank Stephan, Deciding parity games in quasipolynomial time, STOC 2017, pages 252 to 263
    locator: the main theorem, a quasi-polynomial bound for parity games, and a polynomial bound when the number of priorities is at most logarithmic in the number of vertices
  - paper: "Rance Cleaveland and Bernhard Steffen, A linear-time model-checking algorithm for the alternation-free modal mu-calculus, Formal Methods in System Design 2(2), 1993, pages 121 to 147"
    locator: the main algorithm and its linear bound for alternation-free formulas
  - paper: "David E. Long, Anca Browne, Edmund M. Clarke, Somesh Jha and Wilfredo R. Marrero, An improved algorithm for the evaluation of fixpoint expressions, CAV 1994, Lecture Notes in Computer Science 818, Springer, pages 338 to 350"
    locator: the evaluation of nested fixed points with about half as many nested iterations as alternations
  - book: "Julian Bradfield and Igor Walukiewicz, The mu-calculus and model checking, in Edmund M. Clarke, Thomas A. Henzinger, Helmut Veith and Roderick Bloem (eds.), Handbook of Model Checking, Springer, 2018"
    locator: Chapter 26 (the model checking game, the reduction to and from parity games, and the survey of algorithms and their complexity)
  - paper: "Igor Walukiewicz, Pushdown processes: games and model checking, CAV 1996, Lecture Notes in Computer Science 1102, Springer"
    locator: the EXPTIME-completeness of mu-calculus model checking for pushdown systems
---

Mu-calculus model checking is the problem of deciding whether a state of a finite [Kripke structure](/kripke-structure/) satisfies a formula of the [modal mu-calculus](/modal-mu-calculus/). Since the mu-calculus contains CTL, LTL and CTL*, an algorithm for this problem checks all of them. The problem has a strange status. It is in NP ∩ co-NP, in UP ∩ co-UP and in quasi-polynomial time, it is P-hard, and nobody knows whether it is in P. The reason is that it is polynomial-time equivalent to solving [parity games](/parity-game/), whose status is the same open question. For each fixed alternation depth it is polynomial, and for alternation-free formulas, which include all of CTL, it is linear. This page is about the problem; the [Emerson-Lei algorithm](/emerson-lei-algorithm/) is the classic fixed-point algorithm for it, and [Zielonka's algorithm](/zielonka-algorithm/) solves it through games.

## In plain words

A mu-calculus formula describes behaviour by "do this step, then repeat". Some repeats must stop after finitely many rounds, as in "eventually". Others may go on forever, as in "always". The task is to find out which states of a system have the described behaviour.

When the two kinds of repeat are not mixed, one pass over the system per piece of the formula is enough. When they are nested inside each other, an inner repeat must be redone each time the outer one changes, and the work grows with the depth of the nesting.

The same task is a game. One player claims that the behaviour holds and the other denies it. They move through the system and through the formula, and the kind of repeat that is visited forever decides the winner. Nobody knows a fast method for all such games.

## Definition

**Input.** A finite Kripke structure $M = (S, I, R, L)$ given by [adjacency lists](/adjacency-list/), of size $|M| = |S| + |R|$, a closed mu-calculus formula $\varphi$ in positive normal form with each variable bound once, and a state $s \in S$.

**Question.** Is $s \in [\![\varphi]\!]$, where $[\![\cdot]\!]$ is the fixed-point semantics of the [modal mu-calculus](/modal-mu-calculus/) page?

The *global* version asks for the whole set $[\![\varphi]\!]$, and $M \models \varphi$ means $I \subseteq [\![\varphi]\!]$. The parameters that matter are $n = |S|$, $|M|$, $|\varphi|$, the number $k$ of fixed-point operators, and the alternation depth $d = \mathit{ad}(\varphi)$.

## Variants

- **Global and local.** Global model checking computes $[\![\varphi]\!]$ for all states, as fixed-point iteration does. [Local model checking](/local-model-checking/) explores only the pairs (state, subformula) needed to answer for one state, and works on the fly on structures that are generated on demand.
- **Bounded alternation.** For each fixed $d$ the problem is polynomial, and for $d \le 1$ (alternation-free formulas) it is linear. Most specifications in practice have $d \le 2$.
- **Fixed formula.** With $\varphi$ fixed and $M$ the input (data complexity), it is polynomial, and still P-complete.
- **Symbolic and succinct structures.** With $M$ given by [BDDs](/binary-decision-diagram/), the [symbolic](/symbolic-model-checking/) form of the fixed-point iteration is used. When $M$ is a parallel composition of processes, the problem is EXPTIME-complete in the size of the processes (Kupferman, Vardi and Wolper 2000).
- **Infinite-state systems.** For [pushdown systems](/pushdown-system/) the problem is EXPTIME-complete (Walukiewicz 1996). For [Petri nets](/petri-net/) the branching-time mu-calculus is undecidable (Esparza 1994).
- **Equational form.** Boolean equation systems and the vectorial mu-calculus write the fixed points as a list of equations $X_i =_{\sigma_i} f_i(X_1, \ldots, X_m)$; tools such as mCRL2 and CADP solve these.

## Examples

**Infinitely often.** Take $\mathsf{E}\,\mathsf{G}\mathsf{F}\,p = \nu X.\, \mu Y.\, ((p \wedge \Diamond X) \vee \Diamond Y)$ on the structure with edges $0 \to 1$, $0 \to 2$, $1 \to 0$, $2 \to 3$, $3 \to 3$ and $p$ in $1$ and $2$. Nested iteration gives:

| outer $X$ | iterates of the inner $Y$ | inner result |
|---|---|---|
| $\{0, 1, 2, 3\}$ | $\{1, 2\}$, $\{0, 1, 2\}$, $\{0, 1, 2\}$ | $\{0, 1, 2\}$ |
| $\{0, 1, 2\}$ | $\{1\}$, $\{0, 1\}$, $\{0, 1\}$ | $\{0, 1\}$ |
| $\{0, 1\}$ | $\{1\}$, $\{0, 1\}$, $\{0, 1\}$ | $\{0, 1\}$, equal to $X$ |

So $[\![\varphi]\!] = \{0, 1\}$, after $9$ evaluations of the inner body and $3$ of the outer one. In the second row, state $2$ drops out because its only successor $3$ is no longer in $X$.

**Reuse.** Take $\mu X.\, \big(\mu Y.\, r \vee (q \wedge \Diamond Y)\big) \vee (p \wedge \Diamond X)$, that is $\mathsf{E}[p\,\mathsf{U}\,\mathsf{E}[q\,\mathsf{U}\,r]]$ in a form where both fixed points are least, on the path $0 \to 1 \to \cdots \to 5 \to 5$ with $p$ in $0, 1, 2$, $q$ in $3, 4$ and $r$ in $5$. All six states satisfy it. Restarting the inner fixed point at each of the $5$ outer rounds costs $25$ body evaluations. Keeping its value between rounds, as the [Emerson-Lei algorithm](/emerson-lei-algorithm/) does when the signs agree, costs $13$, since after the first round the inner value is already a fixed point.

**Hardness pattern.** On a structure whose states are labelled $\mathit{own}$ or not, $\mu Z.\, \mathit{goal} \vee (\mathit{own} \wedge \Diamond Z) \vee (\neg \mathit{own} \wedge \Box Z)$ holds exactly where the owner of the $\mathit{own}$ states can force a visit to $\mathit{goal}$. This alternation-free formula decides alternating reachability, which is P-complete.

## Known algorithms

| method | cost | notes |
|---|---|---|
| Nested iteration | $k\,(n + 1)^q$ body evaluations | $q$ is the nesting depth |
| [Emerson-Lei](/emerson-lei-algorithm/) (1986) | $k\,(1 + kn)^d$ body evaluations, time $O(|M|\,|\varphi|\,(1 + kn)^d)$ | reuses inner values of the same sign |
| Cleaveland and Steffen (1993) | $O(\lvert M\rvert\,\lvert\varphi\rvert)$ | alternation-free formulas only |
| Long, Browne, Clarke, Jha and Marrero (1994) | about $n^{\lceil d/2 \rceil + 1}$ iterations | stores many intermediate values |
| Local tableau and game search | exponential in $d$ | on the fly, for one state |
| Reduction to parity games, then [Zielonka](/zielonka-algorithm/), progress measures or strategy improvement | about $N^{d}$ for Zielonka, about $N^{d/2}$ for small progress measures, exponential in the worst case for strategy improvement | $N = O(\lvert M\rvert\,\lvert\varphi\rvert)$ |
| Reduction to parity games, then the quasi-polynomial methods (2017) | $N^{O(\log d)}$ | polynomial when $d = O(\log N)$ |

The fixed-point methods are the natural choice for symbolic model checking, where each body evaluation is a few BDD operations. The game methods are the fastest in theory and in parity game solvers.

## Bounds

- **Upper bounds.** The problem is in NP ∩ co-NP (Emerson, Jutla and Sistla 1993): a positional winning strategy in the model checking game is a polynomial certificate for $s \models \varphi$, and one for the opponent certifies $s \not\models \varphi$. Jurdziński (1998) improved this to UP ∩ co-UP, with unique certificates. Calude, Jain, Khoussainov, Li and Stephan (2017) solved parity games in quasi-polynomial time, so the problem takes time $(|M|\,|\varphi|)^{O(\log d)}$.
- **Fixed alternation depth.** The Emerson-Lei bound $O(|M|\,|\varphi|\,(1 + kn)^d)$ is polynomial for each fixed $d$, and linear for $d \le 1$.
- **Lower bound.** The problem is P-hard, already for the fixed alternation-free formula of the hardness pattern above, by a reduction from alternating reachability. It is also P-hard through the CTL fragment, see [CTL model checking](/ctl-model-checking/).
- **Open.** Membership in P is open, and it holds if and only if parity games can be solved in polynomial time. A polynomial algorithm cannot come from the known separating-automaton approach: Czerwiński, Daviaud, Fijalkow, Jurdziński, Lazić and Parys (2019) proved quasi-polynomial lower bounds for it.

## Reductions

**Model checking to parity games.** The game has a position $(t, \psi)$ for each state $t$ and each subformula $\psi$ of $\varphi$. The verifier moves at $\vee$ (choose a side) and $\Diamond$ (choose a successor), and the refuter moves at $\wedge$ and $\Box$. At $\sigma Z.\, \psi$ and at $Z$ the play goes on to $\psi$ or to the body of $Z$. At an atomic position the verifier wins if it is true in $t$. Each fixed point gets a priority that is even for $\nu$ and odd for $\mu$, and larger than the priorities of the fixed points inside it; other positions get priority $0$. On an infinite play the outermost variable that is unfolded infinitely often decides: the verifier wins when it is a $\nu$. Then $s \models \varphi$ if and only if the verifier wins from $(s, \varphi)$. The game has $|S|\,|\varphi|$ positions, $O(|M|\,|\varphi|)$ edges, and about $d + 1$ priorities with a careful assignment (Emerson, Jutla and Sistla 1993; Bradfield and Walukiewicz 2018).

**Parity games to model checking.** Let a parity game have priorities $0, \ldots, d - 1$, every position with a successor, and propositions $P_i$ (priority $i$) and $\mathit{own}$ (positions of player 0). Read the game graph as a Kripke structure. Then player 0 wins from exactly the states of

$$\sigma_{d-1} Z_{d-1}.\, \cdots\, \sigma_0 Z_0.\; \bigvee_{i < d} \Big(P_i \wedge \big((\mathit{own} \wedge \Diamond Z_i) \vee (\neg \mathit{own} \wedge \Box Z_i)\big)\Big),$$

where $\sigma_i = \nu$ for even $i$ and $\mu$ for odd $i$, and the largest priority is the outermost. The formula has alternation depth $d$ and size $O(d)$. So the two problems are polynomial-time equivalent, with the alternation depth matching the number of priorities, and any algorithm for one solves the other.

**From other logics.** [CTL model checking](/ctl-model-checking/) is the alternation-free case. [LTL model checking](/ltl-model-checking/) reduces to fair $\mathsf{EG}$ on the product with a [Büchi automaton](/buchi-automaton/), which is a formula of alternation depth $2$. CTL* reduces with an exponential translation.

## Applications

- **Model checkers.** The Concurrency Workbench, CADP (through its Evaluator tool) and mCRL2 accept mu-calculus properties, the last two through Boolean equation systems or parameterized versions with data.
- **A common back end.** Fixed points in the mu-calculus implement CTL, fair CTL, and the emptiness checks for LTL; symbolic model checkers compute them with [BDDs](/binary-decision-diagram/) by the fixed-point iteration of the [Emerson-Lei algorithm](/emerson-lei-algorithm/).
- **Games and synthesis.** Winning regions of reachability, Büchi and parity games are mu-calculus formulas, so controller synthesis and the emptiness of tree automata use the same algorithms.
- **Equivalence checking.** [Bisimulation](/bisimulation/) is a greatest fixed point, and characteristic formulas reduce equivalence checking to mu-calculus model checking.

## References
