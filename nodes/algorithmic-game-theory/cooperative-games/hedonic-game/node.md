---
tag: 2RD8PD
kind: model
slug: hedonic-game
name: Hedonic game
aliases:
- coalition formation game
area: algorithmic-game-theory/cooperative-games
level: advanced
summary: A coalition formation game in which each player cares only about the members of its own coalition. The questions are which stable partitions exist and how hard they are to find.
prereqs: [core-of-a-cooperative-game, nash-equilibrium, set-partitions]
see_also: [stable-roommates-problem, stable-matching, coalition-structure-generation, potential-game, pls, np-complete, transferable-utility-game, pareto-optimality]
sources:
  - paper: "Jacques H. Dreze and Joseph Greenberg, Hedonic coalitions: optimality and stability, Econometrica 48(4) (1980), 987-1003"
    title: "Hedonic coalitions: optimality and stability"
    locator: the hedonic aspect of coalition formation, where a player's payoff depends only on the members of its coalition
  - paper: "Anna Bogomolnaia and Matthew O. Jackson, The stability of hedonic coalition structures, Games and Economic Behavior 38(2) (2002), 201-230"
    title: The stability of hedonic coalition structures
    locator: the stability notions (core, Nash, individual and contractual individual stability) and the existence of a Nash stable partition for symmetric additively separable preferences
  - paper: "Coralio Ballester, NP-completeness in hedonic games, Games and Economic Behavior 49(1) (2004), 1-30"
    title: NP-completeness in hedonic games
    locator: deciding whether a core stable, Nash stable or individually stable partition exists is NP-complete when preferences are given as lists of individually rational coalitions
  - paper: doi:10.1287/moor.2018.0960
    title: "Martin Gairing and Rahul Savani, Computing stable outcomes in symmetric additively separable hedonic games, Mathematics of Operations Research 44(3) (2019), 1101-1121"
    locator: computing a Nash stable or an individually stable partition of a symmetric additively separable hedonic game is PLS-complete
  - book: isbn:9781107060432
    title: "Haris Aziz and Rahul Savani, Hedonic games, Chapter 15 of Felix Brandt, Vincent Conitzer, Ulle Endriss, Jerome Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016, 356-376"
    locator: the survey of representations, stability notions, existence results and complexity results
---

A hedonic game is a model of coalition formation in which each player's satisfaction depends only on who else is in its coalition. There is no payoff to divide: a research group, a club or a team is good or bad for a member because of the other members. Each player ranks the coalitions that contain it, and the outcome is a partition of the players. The questions are whether the partition is stable, in one of several senses, whether a stable partition exists, and how hard it is to find. Dreze and Greenberg (1980) named the hedonic aspect, and Bogomolnaia and Jackson (2002) set out the stability notions that are now standard.

## The machine

There is a finite set $N$ of $n$ players. For each player $i$, let $\mathcal{N}_i = \{S \subseteq N : i \in S\}$ be the coalitions that contain $i$. Player $i$ has a complete and transitive preference $\succeq_i$ over $\mathcal{N}_i$. The outcome is a partition $\pi$ of $N$, and $\pi(i)$ is the coalition of $\pi$ that contains $i$. Player $i$ compares two partitions only through $\pi(i)$.

A general preference has $2^{n-1}$ coalitions to rank, so the model is studied with compact representations.

- **Additively separable.** Player $i$ gives a value $v_i(j)$ to each other player $j$, and $u_i(S) = \sum_{j \in S \setminus \{i\}} v_i(j)$. The game is symmetric if $v_i(j) = v_j(i)$ for all $i, j$.
- **Lists of coalitions.** Each player lists the coalitions it prefers to being alone, in order. Ballester (2004) calls these individually rational lists of coalitions.
- **Anonymous.** A player cares only about the size of its coalition.
- **Fractional, dichotomous, friends and enemies.** Other representations from the literature, surveyed by Aziz and Savani (2016).

A partition $\pi$ can be stable in the following senses. Each condition says that some deviation is not possible.

- **Individually rational (IR):** $\pi(i) \succeq_i \{i\}$ for every $i$.
- **Nash stable (NS):** no player wants to move alone to another coalition of $\pi$ or to the empty set: $\pi(i) \succeq_i S \cup \{i\}$ for every $S \in \pi \cup \{\emptyset\}$.
- **Individually stable (IS):** no player can move to a coalition $S \in \pi \cup \{\emptyset\}$ that it strictly prefers, when every member of $S$ weakly prefers $S \cup \{i\}$ to $S$. So the new coalition must accept the move.
- **Contractually individually stable (CIS):** as IS, but the move is also blocked if a member of the old coalition $\pi(i)$ is worse off after $i$ leaves.
- **Core stable:** no nonempty coalition $S$ blocks $\pi$, that is, no $S$ with $S \succ_i \pi(i)$ for every $i \in S$.
- **Strictly core stable:** no $S$ with $S \succeq_i \pi(i)$ for every $i \in S$ and $S \succ_i \pi(i)$ for some $i \in S$.

Nash stability implies individual stability, which implies contractual individual stability. Strict core stability implies core stability. Core stability and Nash stability do not imply each other.

## What it counts

The model counts which partitions are stable. For a given partition and a given notion, checking stability is easy for Nash and individual stability: try every player and every coalition of $\pi$, which is $O(n^2)$ comparisons. For core stability the check ranges over all coalitions, and it is hard for some representations. The main questions are existence (does every game in a class have a stable partition), the complexity of deciding existence, and the complexity of finding a stable partition when one is known to exist. A second set of questions is about welfare: a partition that maximizes the sum of utilities is an instance of [coalition structure generation](/coalition-structure-generation/), and [Pareto optimal](/pareto-optimality/) partitions can be studied too.

**No Nash stable partition.** Two players have additively separable values $v_1(2) = 1$ and $v_2(1) = -1$. In $\{\{1\}, \{2\}\}$, player 1 wants to join player 2. In $\{\{1, 2\}\}$, player 2 wants to leave. So no partition is Nash stable. But $\{\{1\}, \{2\}\}$ is individually stable, because player 2 does not accept player 1, and it is core stable.

**Empty core.** Three players have the preferences

- player 1: $\{1, 2\} \succ \{1, 3\} \succ \{1\} \succ \{1, 2, 3\}$,
- player 2: $\{2, 3\} \succ \{1, 2\} \succ \{2\} \succ \{1, 2, 3\}$,
- player 3: $\{1, 3\} \succ \{2, 3\} \succ \{3\} \succ \{1, 2, 3\}$.

The singletons are blocked by $\{1, 2\}$. The partition with $\{1, 2\}$ is blocked by $\{2, 3\}$, the one with $\{2, 3\}$ by $\{1, 3\}$, the one with $\{1, 3\}$ by $\{1, 2\}$, and the grand coalition by any player alone. So all five partitions are blocked, and the core is empty. This is the cycle of a [stable roommates](/stable-roommates-problem/) instance with three people.

## Relation to other models

- **Matching.** If only coalitions of size at most 2 are acceptable, a hedonic game is a [stable roommates](/stable-roommates-problem/) instance, and with two sides it is a [stable matching](/stable-matching/) instance. Core stability is then the usual stability of a matching, up to weak blocking.
- **TU games.** In a [TU game](/transferable-utility-game/) the players form coalitions and divide their values. If a fixed rule divides each value, such as equal split or the Shapley value of the coalition, each player gets a fixed payoff in each coalition, and the game becomes hedonic.
- **Potential games.** A symmetric additively separable game has a potential: with Nash stability as the solution, each improving move raises a common function. So it behaves like a [potential game](/potential-game/), and improvement dynamics end at a Nash stable partition, though maybe after many steps.
- **Coalition structure generation.** The welfare question for a hedonic game is a [coalition structure generation](/coalition-structure-generation/) problem with $v(C) = \sum_{i \in C} u_i(C)$.

## Known results in the model

- **Nash stable partitions in symmetric additively separable games (Bogomolnaia and Jackson 2002).** Let $\Phi(\pi) = \sum_{C \in \pi} \sum_{\{i, j\} \subseteq C} v_i(j)$. If player $i$ moves from $A$ to $B$, then $\Phi$ changes by $\sum_{j \in B} v_i(j) - \sum_{j \in A \setminus \{i\}} v_i(j) = u_i(B \cup \{i\}) - u_i(A)$, by symmetry. An improving move raises $\Phi$, and there are finitely many partitions, so a partition that maximizes $\Phi$ is Nash stable.
- **Finding one is PLS-complete (Gairing and Savani).** Computing a Nash stable partition of a symmetric additively separable game is [PLS](/pls/)-complete, and so is computing an individually stable one. So a polynomial algorithm for either task would give one for every problem in PLS, and none is known.
- **Contractually individually stable partitions always exist.** In a CIS move the mover gains, the members of the new coalition do not lose, and the members of the old coalition do not lose. So every move gives a strict Pareto improvement, no sequence of moves can repeat a partition, and the moves must stop at a CIS partition.
- **Deciding existence is NP-complete (Ballester 2004).** With preferences given as lists of individually rational coalitions, deciding whether a core stable, Nash stable or individually stable partition exists is [NP-complete](/np-complete/).
- **Surveys.** Aziz and Savani (2016) collect existence and complexity results for core and strict core stability, Pareto optimality and the other notions, for many representations.

## References
