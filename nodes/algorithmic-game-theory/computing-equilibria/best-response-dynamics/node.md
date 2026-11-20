---
tag: 0D2G4K
kind: algorithm
slug: best-response-dynamics
name: Best-response dynamics
aliases:
- better-response dynamics
- myopic best response
area: algorithmic-game-theory/computing-equilibria
level: intro
summary: "Lets players in turn switch to a best response to the current pure profile. When it stops, the profile is a pure Nash equilibrium; in finite potential games it always stops."
model: word-ram
complexity:
  vars: {n: the number of players, k: the largest number of pure strategies of a player}
  time: {worst: "O(n k^(n+1))"}
  space: {extra: "O(n k^n)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1838
  people: [Antoine Augustin Cournot, Robert W. Rosenthal, Dov Monderer, Lloyd S. Shapley]
  note: "Cournot let two producers adjust their quantities in turn, each to the best reply to the other. Rosenthal (1973) and Monderer and Shapley (1996) showed that the process stops in congestion games and in finite potential games."
prereqs: [normal-form-game, best-response, pure-nash-equilibrium]
see_also: [potential-game, finite-improvement-property, rosenthal-potential-theorem, atomic-congestion-game, pls-completeness-of-congestion-games, no-regret-dynamics, robinson-fictitious-play-theorem, replicator-dynamics]
sources:
  - book: "Antoine Augustin Cournot, Recherches sur les principes mathématiques de la théorie des richesses, Hachette, Paris, 1838"
    title: Recherches sur les principes mathématiques de la théorie des richesses
    locator: the chapter on competition between producers (two producers who adjust their quantities in turn)
  - paper: doi:10.1007/BF01737559
    title: "Robert W. Rosenthal, A class of games possessing pure-strategy Nash equilibria, International Journal of Game Theory 2(1) (1973), 65-67"
    locator: "the potential function of a congestion game, which every improving move decreases"
  - paper: doi:10.1006/game.1996.0044
    title: "Dov Monderer and Lloyd S. Shapley, Potential games, Games and Economic Behavior 14(1) (1996), 124-143"
    locator: "the finite improvement property, and its equivalence with a generalized ordinal potential"
  - paper: "Alex Fabrikant, Christos Papadimitriou and Kunal Talwar, The complexity of pure Nash equilibria, Proceedings of the 36th ACM Symposium on Theory of Computing (STOC 2004), 604-612"
    title: The complexity of pure Nash equilibria
    locator: "the PLS-completeness of a pure Nash equilibrium in congestion games, and congestion games with exponentially long improvement paths"
  - book: isbn:9781316624791
    title: "Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016"
    locator: Lecture 16 (best-response dynamics in potential games and their speed)
---

Best-response dynamics is the simplest way for players to look for a pure [Nash equilibrium](/pure-nash-equilibrium/): while some player can gain by a change of strategy, one such player switches to a [best response](/best-response/) to what the others play now. If the process stops, nobody can gain and the profile is a pure Nash equilibrium. In a finite [potential game](/potential-game/), such as an [atomic congestion game](/atomic-congestion-game/), every switch raises the potential, so the process always stops. In a game without a pure equilibrium, such as matching pennies, it cycles. The better-response version lets a player move to any strictly better strategy, not only a best one; the [finite improvement property](/finite-improvement-property/) is the statement that all such paths are finite. Unlike [no-regret dynamics](/no-regret-dynamics/) and fictitious play, the players here use only the current profile and play pure strategies.

## In plain words

Several people each choose one option, and each person's reward depends on all the choices. Look at the current choices. If someone could do better by changing only their own choice, let one such person change to their best option. Then look again. Stop when nobody wants to change. At that point the choices are stable: every person already has the best option against the others. The process need not stop. In a game of guessing heads or tails, one player wants to match and the other wants to differ, and they chase each other for ever. In games where a single number goes up with every selfish change, the number cannot go up for ever, so the process stops.

## The problem

The input is a finite game in normal form with players $N = \{1, \ldots, n\}$, pure strategy sets $S_1, \ldots, S_n$ with $|S_i| \le k$, and utilities $u_i : S \to \mathbb{Q}$ on $S = S_1 \times \cdots \times S_n$, which each player maximizes. A cost game uses $u_i = -c_i$. A start profile $s \in S$ is also given. The set of pure best responses of player $i$ to $s_{-i}$ is

$$BR_i(s_{-i}) = \arg\max_{b \in S_i} u_i(b, s_{-i}).$$

A profile $s$ is a pure Nash equilibrium if $s_i \in BR_i(s_{-i})$ for every $i$. (For mixed strategies the same test reads: a mixed strategy is a best response if and only if its support lies in $BR_i$. This page needs only pure strategies.) The output is a pure Nash equilibrium reached from $s$, or the report that the dynamics cycle from $s$.

The strategies of each player are numbered, and ties go to the smallest number. This makes the process deterministic, so that "it cycles" is a fact about the start profile.

## The algorithm

```pseudo id=main
BEST-RESPONSE-DYNAMICS(G, s)        ▷ G is a finite game, s a pure profile
L1  seen ← empty set
L2  repeat
L3      U ← the players i with s_i not in BR_i(s_-i)
L4      if U is empty then return (s, "equilibrium")
L5      if s is in seen then return (s, "cycle")
L6      add s to seen
L7      i ← the smallest player in U
L8      s_i ← the smallest strategy in BR_i(s_-i)
```

Line L3 finds the players who can gain by a change. A player whose current strategy is one of several best responses stays put; only a strict gain makes a player move. Line L4 stops at a pure Nash equilibrium. Lines L7 and L8 make one move. The next profile depends only on the current one, so if a profile comes back (line L5), the same sequence of moves repeats for ever and no equilibrium is reached from the start. The set `seen` of line L1 holds the profiles already left.

Other orders are common. In round-robin order the players take turns, and a player who cannot gain passes. In simultaneous best response all players switch at once, which can cycle even in a potential game: in a two-player coordination game started at a miscoordinated profile, both players switch at the same time and stay miscoordinated.

## Example

Four players each choose one of two links, $A$ (strategy 0) or $B$ (strategy 1). A link used by $x$ players costs each of them $x$. This is an atomic congestion game, and [Rosenthal's potential](/rosenthal-potential-theorem/) is $\Phi(s) = \sum_{e} (1 + 2 + \cdots + x_e)$, where $x_e$ is the load of link $e$. The run starts with all four players on $A$.

| step | profile | loads (A, B) | costs | $\Phi$ | U (line L3) | move (lines L7, L8) |
|---|---|---|---|---|---|---|
| 0 | (A, A, A, A) | (4, 0) | (4, 4, 4, 4) | 10 | {1, 2, 3, 4} | player 1 to B |
| 1 | (B, A, A, A) | (3, 1) | (1, 3, 3, 3) | 7 | {2, 3, 4} | player 2 to B |
| 2 | (B, B, A, A) | (2, 2) | (2, 2, 2, 2) | 6 | empty | return at line L4 |

Each move lowers the cost of the mover by the same amount as it lowers $\Phi$: by 3 in step 1 and by 1 in step 2. In matching pennies, where the row player gets 1 on a match and the column player gets 1 on a mismatch, the run from (H, H) visits (H, T), (T, T), (T, H) and then (H, H) again, and line L5 reports a cycle. That game has no pure Nash equilibrium, so every start cycles.

## Correctness

If the algorithm returns at line L4, no player can gain by a unilateral change, which is the definition of a pure Nash equilibrium. If it returns at line L5, the current profile was left before, and since the next profile is a function of the current one, the run from the start profile is periodic from that point and never meets a profile where line L4 returns. Each pass that does not return adds a new profile to `seen`, so there are at most $|S|$ passes. In a finite game with a generalized ordinal potential $P$, each move of line L8 strictly increases $P$, so no profile repeats and the algorithm always returns an equilibrium. Congestion games have such a potential. The full proof is in the proof file.

## Complexity

Line L3 checks each player against each of its strategies, so one pass costs $O(n k)$ payoff lookups plus $O(n)$ for the set operations on a profile, if `seen` is a hash set of profiles. There are at most $|S| \le k^n$ passes, so the worst case is $O(n k^{n+1})$ lookups, and `seen` holds at most $k^n$ profiles of length $n$, which is $O(n k^n)$ space. In the word RAM model each payoff is a rational number of bounded size, and a comparison costs $O(1)$.

The bound is linear in the size of the normal form, which already lists $n k^n$ numbers. The interesting case is a succinct game, such as a congestion game given by its resources and cost functions. There the number of moves is at most the number of distinct values of the potential, which is polynomial when the costs are small integers but can be exponential in general. Finding a pure Nash equilibrium of a congestion game is [PLS-complete](/pls-completeness-of-congestion-games/) (Fabrikant, Papadimitriou and Talwar, 2004), and there are congestion games with start profiles from which every improvement path to an equilibrium is exponentially long. PLS-complete does not mean NP-hard: a pure equilibrium always exists in these games.

## Properties

- **Deterministic and exact.** With the tie rule of lines L7 and L8 and exact payoffs, the run is a function of the start profile.
- **Uncoupled.** A player needs only its own utility and the current profile, not the others' utilities.
- **Pure.** It works with pure strategies only, so it cannot find a mixed equilibrium. A game with no pure equilibrium always cycles.
- **Monotone in potential games.** In an exact potential game, the potential rises by exactly the gain of the mover at each step.
- **No welfare guarantee.** The equilibrium it reaches depends on the start and the order, and it may be a bad one.

## Variants and improvements

- **Better-response dynamics.** A player may move to any strictly better strategy. In a game with the finite improvement property all such paths are finite, and Monderer and Shapley (1996) showed that a finite game has this property if and only if it has a generalized ordinal potential.
- **Epsilon-best responses.** Move only when the gain is more than an $\varepsilon$ fraction of the current cost. Roughgarden (Lecture 16) proves that in symmetric congestion games whose cost functions have bounded jumps, and with the player of largest gain moving first, this reaches an approximate equilibrium in a number of moves polynomial in $n$, $1/\varepsilon$ and the bit length of the costs, while exact dynamics may take exponentially many.
- **Weakly acyclic games.** In a game that is weakly acyclic under best responses, there is a path of best responses from every profile to an equilibrium, but not every path ends. If the mover is drawn at random at each step, the run reaches an equilibrium with probability 1.
- **Mixed-strategy learning.** Fictitious play best-responds to the empirical mix of the past play of the others and can approach mixed equilibria ([Robinson's theorem](/robinson-fictitious-play-theorem/)). [No-regret dynamics](/no-regret-dynamics/) and [replicator dynamics](/replicator-dynamics/) are smoother forms of adaptation.

## When to use it

Use it to find a pure Nash equilibrium of a potential game, in particular a congestion game, where it is simple, needs only local information and always stops. It is also a model of how myopic players adapt. In a general game, use it only with the cycle check, and expect cycles; a pure equilibrium may not exist at all, and brute force over the normal form is then as cheap. For mixed equilibria use [Nash equilibrium computation](/nash-equilibrium-computation/) methods, and for coarse correlated equilibria use no-regret dynamics.

## Pitfalls

- **Moving on a tie.** If line L3 also lets a player move between two equal best responses, the run can cycle in a potential game, because the potential does not rise on a tie. Move only on a strict gain, as line L3 does.
- **All players at once.** Updating every player in line L8 at the same time breaks the potential argument, because the potential rises only for one mover at a time. The two-player coordination game cycles under simultaneous updates.
- **No cycle check.** Without lines L1, L5 and L6 the loop never ends on matching pennies. Keep the check, or cap the number of steps.
- **Reading a stop as a good outcome.** Line L4 certifies a pure Nash equilibrium, not an efficient one; the [price of anarchy](/price-of-anarchy/) measures how bad it can be.

## Implementations

The Python code follows the pseudocode with the profile as a tuple and `seen` as a set, and returns the path of visited profiles. The tests use the example above, matching pennies from every start, random congestion games with up to 4 players and 4 resources (each move must raise the mover's utility and lower Rosenthal's potential by the same amount, and the result must be a pure Nash equilibrium found by brute force), random exact potential games, and 500 random games compared with a direct simulation of the step rule.

## History

Cournot (1838) described two producers who in turn set their quantity to the best reply to the other's quantity, and studied when this process settles. Rosenthal (1973) introduced congestion games and their potential, which shows that improving moves stop. Monderer and Shapley (1996) defined potential games and the finite improvement property. Fabrikant, Papadimitriou and Talwar (2004) proved that a pure Nash equilibrium of a congestion game is PLS-complete to find.

## References
