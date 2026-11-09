---
tag: FBB94E
kind: problem
slug: parity-game-solving
name: Parity game solving
aliases:
- Solving parity games
- Parity game problem
area: logic-and-constraints/model-checking
level: research
summary: Compute the winning regions of a parity game and positional winning strategies. In NP ∩ co-NP and quasi-polynomial time; no polynomial algorithm is known.
prereqs: [parity-game]
see_also: [zielonka-algorithm, mu-calculus-model-checking, modal-mu-calculus, quasi-polynomial-time, unambiguous-polynomial-time, stochastic-game]
sources:
  - paper: doi:10.1016/S0304-3975(98)00009-7
    title: Wiesław Zielonka, Infinite games on finitely coloured graphs with applications to automata on infinite trees, Theoretical Computer Science 200(1-2), 1998, pages 135 to 183
    locator: the recursive algorithm
  - paper: "Marcin Jurdziński, Small progress measures for solving parity games, STACS 2000, Lecture Notes in Computer Science 1770, Springer, 2000, pages 290 to 301"
    title: Small progress measures for solving parity games
    locator: the definition of small progress measures, the lifting algorithm and its time and space bounds
  - paper: "Jens Vöge and Marcin Jurdziński, A discrete strategy improvement algorithm for solving parity games, CAV 2000, Lecture Notes in Computer Science 1855, Springer, 2000, pages 202 to 215"
    title: A discrete strategy improvement algorithm for solving parity games
    locator: the valuation of a strategy and the improvement step
  - paper: "Oliver Friedmann, An exponential lower bound for the parity game strategy improvement algorithm as we know it, 24th IEEE Symposium on Logic in Computer Science (LICS 2009), pages 145 to 156"
    title: An exponential lower bound for the parity game strategy improvement algorithm as we know it
    locator: the family of games on which discrete strategy improvement takes exponentially many iterations
  - paper: "Cristian S. Calude, Sanjay Jain, Bakhadyr Khoussainov, Wei Li and Frank Stephan, Deciding parity games in quasipolynomial time, 49th ACM Symposium on Theory of Computing (STOC 2017), pages 252 to 263"
    title: Deciding parity games in quasipolynomial time
    locator: the play summaries of logarithmic size, the reduction to a reachability game, and the main theorem
  - paper: "Marcin Jurdziński and Ranko Lazić, Succinct progress measures for solving parity games, 32nd IEEE Symposium on Logic in Computer Science (LICS 2017)"
    title: Succinct progress measures for solving parity games
    locator: the succinct encoding of progress measures that gives quasi-polynomial time with small space
  - paper: "Marcin Jurdziński, Mike Paterson and Uri Zwick, A deterministic subexponential algorithm for solving parity games, SIAM Journal on Computing 38(4), 2008, pages 1519 to 1532"
    title: A deterministic subexponential algorithm for solving parity games
    locator: the dominion search that gives time n^O(√n)
  - paper: "Wojciech Czerwiński, Laure Daviaud, Nathanaël Fijalkow, Marcin Jurdziński, Ranko Lazić and Paweł Parys, Universal trees grow inside separating automata: quasi-polynomial lower bounds for parity games, SODA 2019"
    title: "Universal trees grow inside separating automata: quasi-polynomial lower bounds for parity games"
    locator: the quasi-polynomial lower bound for all algorithms based on separating automata
---

*Parity game solving* is the problem of computing, for a [parity game](/parity-game/), the set of vertices from which each player wins, and a positional winning strategy for each player on its set. It is the core of [mu-calculus model checking](/mu-calculus-model-checking/), of the emptiness test for automata on infinite trees, and of synthesis from LTL specifications. The problem is in NP ∩ co-NP and in UP ∩ co-UP, and since 2017 it is known to be solvable in quasi-polynomial time $n^{O(\log d)}$. Whether it is in polynomial time is open. This page compares the algorithms; the game itself and the proof of positional determinacy are on the [parity game](/parity-game/) page, and the most used algorithm is on the [Zielonka's algorithm](/zielonka-algorithm/) page.

## In plain words

Two players push a token around a graph forever. Each vertex has a number. The first player wins when the largest number that keeps coming back is even. The question is: from which start vertices can the first player win, however the second player plays, and how? For each vertex the answer is one of the two players, and the winner can always use a fixed rule: "at this vertex, take this edge". So a solver must find a split of the vertices into two parts and one rule for each part. Many algorithms do this. Some go down from the largest number, some grow a numeric score at each vertex until it settles, and some improve a rule step by step. All known ones take more than polynomial time on some games.

## Definition

The input is a parity game $G = (V, V_0, V_1, E, \Omega)$: a finite set of vertices $V = V_0 \sqcup V_1$, a set of edges $E \subseteq V \times V$ in which each vertex has a successor, and priorities $\Omega : V \to \{0, \ldots, d\}$. We write $n = |V|$ and $m = |E|$. Player 0 wins a play when the largest priority that occurs infinitely often is even.

The output is a pair $(W_0, W_1)$ and positional strategies $\sigma_0 : W_0 \cap V_0 \to V$ and $\sigma_1 : W_1 \cap V_1 \to V$ such that

- $W_0 \sqcup W_1 = V$;
- for $j \in \{0, 1\}$, each play that starts in $W_j$ and follows $\sigma_j$ is won by player $j$, whatever the opponent does.

Such an output exists for every input by positional determinacy, and $W_0$ and $W_1$ are then unique: they are the winning regions.

## Variants

- **Decision.** Given $G$ and a vertex $v$, is $v \in W_0$? The complexity results below are stated for this version. The search version (the regions and the strategies) has the same bounds for all algorithms below, which output strategies too.
- **Few priorities.** For a fixed number of priorities $d$ the problem is in polynomial time. Two special cases are linear: in a *reachability game* player 0 wants to visit a target set, and in a *safety game* she wants to avoid it. Both are solved by one attractor in $O(n + m)$ time. *Büchi games* (priorities $\{1, 2\}$) are solved in $O(n m)$ time by a loop of attractors.
- **Min-parity.** The least priority seen infinitely often decides. It is the same problem after the map $q \mapsto d' - q$ for an even $d' \ge d$.
- **Partial solving.** Only the region that contains a given start vertex is asked for. Local algorithms explore only the part of the game that the start vertex can reach.

## Examples

**A small game.** In the game below, player 0 owns $u$ and player 1 owns $v$, $w$ and $x$.

| vertex | owner | priority | successors |
|---|---|---|---|
| u | 0 | 2 | v, w |
| v | 1 | 1 | u, x |
| w | 1 | 0 | u |
| x | 1 | 3 | x, w |

The answer is $W_0 = \{u, w\}$ with $\sigma_0(u) = w$, and $W_1 = \{v, x\}$ with $\sigma_1(v) = x$ and $\sigma_1(x) = x$. Small progress measures find it as follows. The odd priorities are 3 and 1, and each is used by one vertex, so a measure is a pair $(m_3, m_1)$ with $0 \le m_3, m_1 \le 1$, or the top value $\top$. All measures start at $(0, 0)$. The vertex $x$ has priority 3 and a self-loop, so each lift raises its $m_3$: first to $(1, 0)$, then past the bound to $\top$. Then $v$, owned by player 1, takes the larger option, $\top$ through $x$. The vertex $u$, owned by player 0, takes the smaller option: through $w$ it keeps $(0, 0)$. The measures stop changing with $\top$ exactly at $v$ and $x$, so $W_1 = \{v, x\}$.

**A game that needs two rounds.** On the six-vertex game of the [Zielonka's algorithm](/zielonka-algorithm/) page, the first attractor of the top priority does not settle the game. The recursion first finds that player 0 wins $\{c, d, e\}$, cuts it off, and then gives the rest to player 1.

## Known algorithms

| algorithm | worst-case time | notes |
|---|---|---|
| [Zielonka's algorithm](/zielonka-algorithm/) (1998) | $O(m (n+1)^d)$ | recursive, with attractors; exponential on some games (Friedmann 2011); fast in practice |
| Small progress measures (Jurdziński 2000) | $O\big(d m (n / \lfloor d/2 \rfloor)^{\lfloor d/2 \rfloor}\big)$ | a lifting fixed point over tuples of counters |
| Discrete strategy improvement (Vöge and Jurdziński 2000) | at most the number of positional strategies of one player, times a polynomial | exponential on some games (Friedmann 2009) |
| Dominion search (Jurdziński, Paterson and Zwick 2006) | $n^{O(\sqrt{n})}$ | the first deterministic subexponential bound |
| Play summaries (Calude, Jain, Khoussainov, Li and Stephan 2017) | $O(n^{\lceil \lg d \rceil + 6})$ | quasi-polynomial; polynomial when $d \le \lg n$ |
| Succinct progress measures (Jurdziński and Lazić 2017) | quasi-polynomial | the same order of time as Calude et al., with nearly linear space |

**Small progress measures.** Let $n_q$ be the number of vertices of priority $q$. A *measure* is a tuple $(m_q)$ indexed by the odd priorities $q$, with $0 \le m_q \le n_q$, or the top value $\top$. Tuples are compared lexicographically, the largest priority first, and $\top$ is above all tuples. For a priority $p$, write $x \ge_p y$ when the tuples, cut to the entries with $q \ge p$, compare in this way. Let $\mathrm{prog}(\rho, v, w)$ be the least measure $x$ with $x \ge_{\Omega(v)} \rho(w)$ if $\Omega(v)$ is even, and with $x >_{\Omega(v)} \rho(w)$ if $\Omega(v)$ is odd ($\top$ if there is none, or if $\rho(w) = \top$). The algorithm starts with $\rho = 0$ everywhere and repeats the *lift*: $\rho(v) \leftarrow \max(\rho(v), \min_w \mathrm{prog}(\rho, v, w))$ for $v \in V_0$ and with $\max_w$ for $v \in V_1$, over the successors $w$. The lifts are monotone on a finite lattice, so they reach the least simultaneous fixed point, and Jurdziński proved that $W_0 = \{v : \rho(v) \neq \top\}$ there. Each odd entry counts how many visits to vertices of that priority player 1 can force without a larger even priority in between; a count above $n_q$ means a cycle that player 1 wins.

**Strategy improvement.** Fix a positional strategy $\sigma$ of player 0, compute a valuation of each vertex for the best answer of player 1 to it, and switch $\sigma$ at each vertex where a successor has a better valuation. The valuations improve strictly, so the loop ends, at an optimal strategy. Friedmann (2009) built games on which the standard switching rules need exponentially many iterations. Friedmann, Hansen and Zwick (2011) gave subexponential lower bounds for randomized rules.

**Quasi-polynomial algorithms.** Calude et al. store, for the play so far, a summary of $O(\log n)$ priorities that tells whether player 0 has already seen a winning pattern. This turns the parity game into a reachability game on (vertex, summary) pairs, of quasi-polynomial size, solved by one attractor. Later algorithms use universal trees or register games. Czerwiński, Daviaud, Fijalkow, Jurdziński, Lazić and Parys (2019) proved that every algorithm based on a separating automaton, which includes these, needs quasi-polynomial time. So a polynomial algorithm needs a new idea.

## Bounds

- **Upper bound.** Time $n^{O(\log d)}$, and so $n^{O(\log n)}$ (Calude et al. 2017). Membership in NP ∩ co-NP comes from positional strategies as certificates, and in [UP](/unambiguous-polynomial-time/) ∩ co-UP from Jurdziński (1998). The proof of the NP bound is on the [parity game](/parity-game/) page.
- **Lower bound.** The problem is P-hard under logspace reductions, because reachability games, the special case with one attractor, are P-complete. No better lower bound is known. Because the problem is in NP ∩ co-NP, it is not NP-hard unless NP = co-NP.
- **Lower bounds for algorithm families.** Exponential for Zielonka's algorithm (Friedmann 2011) and for discrete strategy improvement (Friedmann 2009). Quasi-polynomial for algorithms based on separating automata (Czerwiński et al. 2019).

## Reductions

- **From mu-calculus model checking.** Checking a [modal mu-calculus](/modal-mu-calculus/) formula $\varphi$ on a Kripke structure $M$ reduces to a parity game with $O(|M| \cdot |\varphi|)$ vertices and with $d$ about the alternation depth of $\varphi$. The reduction also goes back: the winning region of a parity game is defined by a mu-calculus formula of alternation depth $d$ on the game graph. So the two problems have the same complexity up to a polynomial.
- **To mean payoff, discounted payoff and simple stochastic games.** A parity game becomes a mean payoff game when each edge out of $v$ gets a weight whose sign is the parity of $\Omega(v)$ and whose size grows by a factor of about $n$ for each step up in priority, so that one visit to a larger priority outweighs a whole cycle of smaller ones (Puri 1995; Jurdziński 1998). Mean payoff games reduce to discounted payoff games and these to simple [stochastic games](/stochastic-game/) (Zwick and Paterson 1996). None of the reverse reductions is known to be polynomial.
- **From LTL synthesis and tree automata.** Emptiness of a nondeterministic parity tree automaton, and realizability of an LTL formula through a deterministic parity automaton, reduce to solving a parity game whose size is that of the automaton times the system.

## Applications

- [Mu-calculus model checking](/mu-calculus-model-checking/), and through it model checking of [CTL](/computation-tree-logic/) with [fairness](/fairness/) and other fixed-point logics.
- Synthesis of reactive controllers from LTL specifications: the specification becomes a deterministic parity automaton, and the product with the interface of the system is a parity game.
- Checking emptiness and complementation of automata on infinite trees, and deciding satisfiability of the mu-calculus.
- Equivalence and preorder checking with games, such as the game view of [bisimulation](/bisimulation/).

## References
