---
tag: PT7YP8
kind: definition
slug: sequence-form
name: Sequence form
aliases:
- Koller-Megiddo-von Stengel sequence form
- realization plan
area: algorithmic-game-theory/computing-equilibria
level: advanced
summary: Represents a strategy in an extensive-form game with perfect recall by the probabilities of its action sequences, with linear constraints.
prereqs: [game-tree, imperfect-information-game, mixed-strategy, linear-programming-problem]
see_also: [sequence-form-linear-program, extensive-form-game, perfect-recall, information-set, kuhn-theorem-behavioral-strategies, counterfactual-regret-minimization, linear-complementarity-problem, normal-form-game]
sources:
  - paper: doi:10.1006/game.1996.0051
    title: "Daphne Koller, Nimrod Megiddo and Bernhard von Stengel, Efficient computation of equilibria for extensive two-person games, Games and Economic Behavior 14(2) (1996), 247-259"
    locator: sequences, realization plans as the solutions of linear constraints, the sequence payoff matrices, and the LP and LCP built on them
  - paper: "Bernhard von Stengel, Efficient computation of behavior strategies, Games and Economic Behavior 14(2) (1996), 220-246"
    title: Efficient computation of behavior strategies
    locator: the sequence form in detail, realization plans and their relation to behavior strategies
  - paper: "I. V. Romanovskii, Reduction of a game with complete memory to a matrix game, Soviet Mathematics 3 (1962), 678-681"
    title: Reduction of a game with complete memory to a matrix game
    locator: an earlier form of the same idea for zero-sum games with perfect recall
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Éva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 3 (Bernhard von Stengel, Equilibrium computation for two-player games in strategic and extensive form), the sections on extensive games and the sequence form
---

The sequence form is a way to write the strategies of a player in a [game tree](/game-tree/) with imperfect information and [perfect recall](/perfect-recall/) as vectors that satisfy a small system of linear equations. Instead of a probability for each pure strategy, of which there can be exponentially many, a player has one variable for each sequence of own moves on a path of the tree, and the expected payoff is bilinear in the two players' vectors. This page is the representation. The [sequence-form linear program](/sequence-form-linear-program/) is the algorithm that uses it to solve two-player zero-sum games, and the same vectors give a [linear complementarity problem](/linear-complementarity-problem/) for games that are not zero-sum.

## Definition

Take a finite two-player [extensive-form game](/extensive-form-game/) with chance moves. Player $i$ has a set $H_i$ of [information sets](/information-set/), and $A(h)$ is the set of actions at $h \in H_i$. A **sequence** of player $i$ is the list of the (information set, action) pairs of player $i$ on the path from the root to some node, in order. The empty sequence $\emptyset$ belongs to every player. The sequence $\sigma_h a$ is the sequence $\sigma_h$ that leads to $h$, followed by action $a$ at $h$.

Perfect recall means that all nodes of an information set $h$ of player $i$ have the same sequence of player $i$, which is then written $\sigma_h$. Then the set of sequences of player $i$ is

$$S_i = \{\emptyset\} \cup \{\sigma_h a : h \in H_i,\ a \in A(h)\}, \qquad |S_i| = 1 + \sum_{h \in H_i} |A(h)|,$$

which is at most one more than the number of edges out of the nodes of player $i$.

A **realization plan** of player 1 is a vector $x \in \mathbb{R}^{S_1}$ with

$$x(\emptyset) = 1, \qquad x(\sigma_h) = \sum_{a \in A(h)} x(\sigma_h a) \ \text{ for every } h \in H_1, \qquad x \ge 0 .$$

In matrix form this is $E x = e$, $x \ge 0$, where $E$ has one row for $\emptyset$ and one row for each information set, and $e = (1, 0, \ldots, 0)$. Realization plans $y$ of player 2 are $F y = f$, $y \ge 0$ in the same way. The number $x(\sigma)$ is the probability that player 1 plays all the moves of $\sigma$, when the other player and chance let the play get there.

**Payoffs.** For a leaf $\ell$ with payoffs $u_1(\ell)$, $u_2(\ell)$ and chance probability $c(\ell)$, the product of the chance probabilities on its path, let $\sigma_1(\ell)$ and $\sigma_2(\ell)$ be the sequences of the two players that lead to it. The **sequence payoff matrices** are

$$A(\sigma_1, \sigma_2) = \sum_{\ell : \sigma_1(\ell) = \sigma_1,\ \sigma_2(\ell) = \sigma_2} c(\ell)\, u_1(\ell),$$

and $B$ the same with $u_2$. Most entries are 0, and the number of nonzero entries is at most the number of leaves. The expected payoffs are $x^{\mathsf T} A y$ and $x^{\mathsf T} B y$.

**Relation to the other strategy forms.** A behavior strategy $\beta$, which gives a distribution $\beta(h, \cdot)$ at each information set, has the realization plan $x(\sigma) = \prod_{(h, a) \in \sigma} \beta(h, a)$. A mixed strategy $\mu$ over pure strategies has the realization plan $x(\sigma) = \sum \mu(\pi)$ over the pure strategies $\pi$ that choose every move of $\sigma$. Under perfect recall:

- every vector that satisfies the constraints is the realization plan of some behavior strategy, given by $\beta(h, a) = x(\sigma_h a) / x(\sigma_h)$ when $x(\sigma_h) > 0$, and by any distribution when $x(\sigma_h) = 0$;
- two strategies with the same realization plan give the same expected payoffs against every strategy of the other player (they are realization equivalent).

These two facts are the sequence-form version of [Kuhn's theorem on behavioral strategies](/kuhn-theorem-behavioral-strategies/).

## Examples and non-examples

- **A small game.** Player 1 plays $L$, which ends the game with payoff 1, or $R$. After $R$, player 2 picks $a$ or $b$, and then player 1 picks $c$ or $d$ without seeing that choice. Payoffs to player 1 (the game is zero-sum) are 3 after $R a c$, 0 after $R a d$ and $R b c$, and 2 after $R b d$. The sequences are $S_1 = \{\emptyset, L, R, Rc, Rd\}$ and $S_2 = \{\emptyset, a, b\}$, and the constraints of player 1 are

$$x(\emptyset) = 1, \qquad x(\emptyset) = x(L) + x(R), \qquad x(R) = x(Rc) + x(Rd).$$

The nonzero entries of $A$ are $A(L, \emptyset) = 1$, $A(Rc, a) = 3$ and $A(Rd, b) = 2$. The behavior strategy "play $R$, then $c$ with probability $2/5$" has the realization plan $x = (1, 0, 1, 2/5, 3/5)$. Player 1 has 4 pure strategies ($Lc$, $Ld$, $Rc$, $Rd$), 3 in the reduced normal form, where $Lc$ and $Ld$ are the same, and 5 sequences.

- **Exponentially many pure strategies.** If chance first picks one of $k$ cases and player 1 then chooses between two actions in a separate information set for each case, player 1 has $2^k$ pure strategies and only $1 + 2k$ sequences.
- **Kuhn poker.** Each player has 6 information sets with 2 actions each, so 13 sequences and $2^6 = 64$ pure strategies.
- **Not a realization plan.** In the small game, $x = (1, 0, 1, 1/2, 1/4)$ violates $x(R) = x(Rc) + x(Rd)$. So does any vector that puts weight on $Rc$ while $x(R) = 0$.
- **No perfect recall.** If player 1 moves $L$ or $R$ and then reaches one information set $h$ after both, the nodes of $h$ have the sequences $(L)$ and $(R)$, so $\sigma_h$ is not defined. The sequence form does not apply, and mixed and behavior strategies are no longer equivalent.

## Related definitions

- **Reduced normal form.** Pure strategies that differ only at information sets that they themselves make unreachable are merged. The sequence form is often exponentially smaller even than the reduced normal form.
- **Polytope of realization plans.** The set $\{x : E x = e, x \ge 0\}$ is a polytope, sometimes called a treeplex. Its vertices are the realization plans of the pure strategies of the reduced normal form.
- **Sequence-form LP and LCP.** For a zero-sum game, $\max_x \min_y x^{\mathsf T} A y$ over the two polytopes is one LP, by LP duality on the inner problem ([sequence-form linear program](/sequence-form-linear-program/)). For a general two-player game, the equilibrium conditions are an LCP of size linear in the tree, solved by a variant of [Lemke's algorithm](/lemke-algorithm/).
- **Counterfactual regret minimization.** [CFR](/counterfactual-regret-minimization/) works with behavior strategies at the information sets and updates them locally. Its average strategy has to be taken in the sequence form, weighted by the realization probabilities.

## References
