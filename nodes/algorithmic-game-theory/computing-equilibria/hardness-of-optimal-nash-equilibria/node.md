---
tag: 4GH3YV
kind: theorem
slug: hardness-of-optimal-nash-equilibria
name: NP-hardness of optimal Nash equilibria
aliases:
- Gilboa-Zemel theorem
- Conitzer-Sandholm hardness
area: algorithmic-game-theory/computing-equilibria
level: advanced
summary: Deciding whether a bimatrix game has a Nash equilibrium with a given property, such as welfare above a bound, is NP-complete.
prereqs: [bimatrix-game, nash-equilibrium, best-response, np-complete, sat]
see_also: [ppad-completeness-of-nash, correlated-equilibrium-linear-program, support-enumeration, lipton-markakis-mehta-algorithm, planted-clique, cook-levin-theorem, nash-equilibrium-computation, epsilon-nash-equilibrium]
sources:
  - paper: doi:10.1016/0899-8256(89)90006-7
    title: "Itzhak Gilboa and Eitan Zemel, Nash and correlated equilibria: some complexity considerations, Games and Economic Behavior 1(1) (1989), 80-93"
    locator: the NP-hardness of deciding properties of Nash equilibria of bimatrix games, and the polynomial algorithms for the same questions about correlated equilibria
  - paper: doi:10.1016/j.geb.2008.02.015
    title: "Vincent Conitzer and Tuomas Sandholm, New complexity results about Nash equilibria, Games and Economic Behavior 63(2) (2008), 621-641"
    locator: "the game G(phi) built from a formula, its equilibria and the list of NP-hard and #P-hard questions; conference version: Complexity results about Nash equilibria, IJCAI 2003, 765-771, Section 2, Definition 4, Theorem 1 and Corollaries 1 to 9"
  - paper: doi:10.1137/070699652
    title: "Constantinos Daskalakis, Paul W. Goldberg and Christos H. Papadimitriou, The complexity of computing a Nash equilibrium, SIAM Journal on Computing 39(1) (2009), 195-259"
    locator: the contrast between finding some equilibrium, which is PPAD-complete, and finding one with a property
---

Finding some [Nash equilibrium](/nash-equilibrium/) of a two-player game is [PPAD-complete](/ppad-completeness-of-nash/), and an equilibrium always exists. Asking for an equilibrium with an extra property changes the picture: the question may have the answer no, and then it is [NP-complete](/np-complete/). Gilboa and Zemel (1989) proved that it is NP-hard to decide whether a [bimatrix game](/bimatrix-game/) has a Nash equilibrium in which a player gets at least a given payoff, and several similar questions. Conitzer and Sandholm (2003, 2008) gave one simple reduction from [SAT](/sat/) that proves many of these results at once, already for symmetric games. The same questions about correlated equilibria are linear programs and are easy ([correlated equilibrium LP](/correlated-equilibrium-linear-program/)).

## Statement

Let $(A, B)$ be an $m \times n$ bimatrix game with rational payoffs, where $m$ and $n$ are the numbers of pure strategies. A pair of [mixed strategies](/mixed-strategy/) $(x, y)$ is a Nash equilibrium if each is a [best response](/best-response/) to the other. A mixed strategy is a best response if and only if its support is inside the set of pure best responses, so it is enough to test pure deviations.

**Theorem (Gilboa and Zemel 1989; Conitzer and Sandholm 2008).** Each of the following questions is NP-complete for bimatrix games, and stays NP-hard for symmetric bimatrix games:

1. Is there a Nash equilibrium in which the sum of the expected payoffs is at least $k$?
2. Is there a Nash equilibrium in which each player gets at least $k$?
3. Is there a Nash equilibrium in which player 1 gets at least $k$?
4. Is there a Nash equilibrium that is Pareto optimal among all profiles?
5. Is there more than one Nash equilibrium?
6. Is there a Nash equilibrium in which a given pure strategy is played with positive probability?
7. Is there a Nash equilibrium in which a given pure strategy is never played?

Counting the Nash equilibria is #P-hard (Conitzer and Sandholm). The questions are in NP for two players: a certificate is a pair of supports, and a linear program checks whether some equilibrium has these supports and the property. For question 5 the certificate is two such pairs of supports, or one pair whose linear program has two different solutions.

The proof for all seven questions rests on one game.

**The game $G(\varphi)$.** Let $\varphi$ be a formula in conjunctive normal form with the set $V$ of $n$ variables, the set $L$ of $2n$ literals and the set $C$ of clauses. For a literal $l$, write $-l$ for its negation and $v(l)$ for its variable. The game is symmetric, each player has the pure strategies $L \cup V \cup C \cup \{f\}$, and $u(a, b)$ is the payoff of a player who plays $a$ against $b$:

| own strategy $a$ | against a literal $l'$ | against $b \in V \cup C$ | against $f$ |
|---|---|---|---|
| literal $l$ | $1$ if $l' \ne -l$, $-2$ if $l' = -l$ | $-2$ | $-2$ |
| variable $v$ | $2$ if $v(l') \ne v$, $2 - n$ if $v(l') = v$ | $-2$ | $-2$ |
| clause $c$ | $2$ if $l' \notin c$, $2 - n$ if $l' \in c$ | $-2$ | $-2$ |
| $f$ | $1$ | $1$ | $0$ |

**Theorem 1 (Conitzer and Sandholm).** The pair $(f, f)$ is a Nash equilibrium with payoff 0 to each player. For each satisfying assignment of $\varphi$, the pair in which both players play uniformly over the $n$ true literals is a Nash equilibrium with payoff 1 to each player. There are no other Nash equilibria.

## In plain words

A game can be built from a logic puzzle. Each player may name a fact about the puzzle, name a variable or a clause to challenge the other, or take a safe option. If the puzzle has no solution, the only stable outcome is that both take the safe option and get nothing. If the puzzle has solutions, each solution gives a better stable outcome, in which both players name the true facts of that solution at random. So a question like "is there a stable outcome that pays well?" is the same as "does the puzzle have a solution?", and that question is hard. Finding some stable outcome is easy in this game, because the safe option always works.

## Proof

**The listed profiles are equilibria.** Against $f$, every strategy other than $f$ gets $-2 < 0$, so $(f, f)$ is an equilibrium. Now let $T$ be the set of true literals of a satisfying assignment, with one literal for each variable, and let both players play uniformly on $T$. A literal $l \in T$ gets 1, because $-l \notin T$. This is the equilibrium payoff. A literal $l \notin T$ gets $1 - 3/n$, because $-l \in T$. A variable $v$ gets $\frac{n - 1}{n} \cdot 2 + \frac{1}{n}(2 - n) = 1$, because exactly one literal of $T$ has variable $v$. A clause $c$ contains at least one literal of $T$, so it gets at most $\frac{n-1}{n} \cdot 2 + \frac1n (2 - n) = 1$. The strategy $f$ gets 1. No deviation gets more than 1, so the profile is an equilibrium.

**There are no other equilibria.** Let $(\sigma_1, \sigma_2)$ be a Nash equilibrium other than $(f, f)$.

(a) If one player plays $f$ with probability 1, the only best response of the other player is $f$, because everything else gets $-2$. So neither player plays $f$ with probability 1.

(b) Let $q$ be the probability that the other player plays $f$. Playing $f$ gives $1 - q$. Playing $a \ne f$ gives $(1 - q) w_a - 2q$, where $w_a$ is the expected payoff of $a$ given that the other player does not play $f$. If $w_a < 1$, then $f$ is strictly better than $a$. So every strategy $a \ne f$ in the support of a player has $w_a \ge 1$.

(c) For two strategies $a, b \ne f$, the sum $u(a, b) + u(b, a)$ is at most 2, and it is less than 2 if $a$ or $b$ is in $V \cup C$: a variable or clause gets at most 2 and the other side gets $-2$. Condition on the event that neither player plays $f$. By (b) each player's conditional expected payoff is at least 1, so the conditional expected sum is at least 2. Since the sum is at most 2 for every pair, it is exactly 2 with probability 1 on this event, and no player plays a strategy in $V \cup C$. Also no pair $(l, -l)$ is played, because its sum is $-4$. Each played literal then has $w_a = 1$.

(d) Now the supports are inside $L \cup \{f\}$. If the other player plays $f$ with probability $q > 0$, then a literal gets at most $(1 - q) - 2q < 1 - q$, which is the payoff of $f$. So the player plays only $f$, which (a) excludes. So $q = 0$ for both players, and both play only literals, with payoff 1.

(e) Let $p_v$ be the probability that player 2 plays a literal of variable $v$. The deviation of player 1 to $v$ gets $2(1 - p_v) + (2 - n) p_v = 2 - n p_v$. This must be at most 1, so $p_v \ge 1/n$. The $n$ numbers $p_v$ sum to 1, so $p_v = 1/n$ for every $v$. The same holds for player 1.

(f) A literal $l$ played by player 1 gets $1 - 3\sigma_2(-l)$, which must equal 1, so player 2 never plays $-l$. If player 2 played both literals of a variable $v$, player 1 could play neither of them, which contradicts (e) for player 1. So player 2 plays exactly one literal of each variable, each with probability $1/n$. These literals form an assignment $T$. Player 1 also gives probability $1/n$ to each variable and cannot play the negation of a literal in $T$, so it plays uniformly on $T$ too.

(g) The deviation to a clause $c$ gets $\frac1n \sum_{l \in T} u(c, l)$. If no literal of $T$ is in $c$, this is 2, which is more than 1. So every clause contains a literal of $T$, and $T$ satisfies $\varphi$. $\square$

**The questions.** The size of $G(\varphi)$ is polynomial in the size of $\varphi$. If $\varphi$ is satisfiable, there is an equilibrium with payoffs $(1, 1)$; otherwise $(f, f)$ with $(0, 0)$ is the only one. So questions 1 ($k = 2$), 2 ($k = 1$) and 3 ($k = 1$) have the answer yes exactly when $\varphi$ is satisfiable. For question 4: every profile has sum at most 2 (pairs with $f$ have sum $-1$ or 0), so $(1, 1)$ is Pareto optimal, while $(0, 0)$ is not, because a pair of literals that are not negations of each other gives $(1, 1)$. For question 5, there is a second equilibrium exactly when $\varphi$ is satisfiable. For question 6, add a new variable $z$ that is in no clause: the literal $z$ is played in some equilibrium exactly when $\varphi$ is satisfiable. For question 7, the strategy $f$ is never played in some equilibrium exactly when $\varphi$ is satisfiable. Since SAT is NP-complete ([Cook-Levin theorem](/cook-levin-theorem/)), all questions are NP-hard. The number of equilibria is the number of satisfying assignments plus 1, which gives the #P-hardness of counting.

## Consequences

- **Optimal equilibria are hard, existence is not.** Every game has an equilibrium, so the plain search problem is in TFNP and is not NP-hard unless NP equals coNP. The hardness here comes only from the extra property. So a rule that selects the equilibrium with the largest welfare is hard to compute.
- **Algorithms must enumerate.** To find a welfare-maximizing equilibrium exactly, methods such as [support enumeration](/support-enumeration/) or enumeration of the vertices of the best-response polytopes look at all equilibria, which takes exponential time in the worst case.
- **Correlated equilibria are easy.** The set of correlated equilibria is a polytope given by linear inequalities, so a linear program finds the one with the largest welfare in polynomial time (Gilboa and Zemel 1989).
- **Approximation.** Approximate versions are also hard. With $\varepsilon$-Nash equilibria and payoffs in $[0, 1]$, the [Lipton-Markakis-Mehta](/lipton-markakis-mehta-algorithm/) argument gives an $\varepsilon$-Nash equilibrium whose payoffs are within $\varepsilon$ of those of any given Nash equilibrium, in time $n^{O(\log n / \varepsilon^2)}$. Hazan and Krauthgamer (2011) showed that finding an $\varepsilon$-Nash equilibrium with near-optimal welfare in polynomial time, for a small constant $\varepsilon$, would solve the [planted clique](/planted-clique/) problem. Braverman, Ko and Weinstein (2015) showed that time $n^{o(\log n)}$ is not enough for this under the exponential time hypothesis (ETH).

## Tightness

The reduction gives hardness already for symmetric two-player games, the smallest interesting class. It does not give hardness for zero-sum games: there all equilibria have the same payoffs, and the set of equilibrium strategies is a polytope that a linear program describes, so questions 1 to 3 are easy. For games with 3 or more players, membership in NP fails in general, because equilibria can be irrational, and questions of this kind are harder: deciding whether a 3-player game has an equilibrium with a given property is complete for the existential theory of the reals for several properties (Schaefer and Stefankovic, and Garg, Mehta, Vazirani and Yazdanbod). The reduction does not say anything about finding some equilibrium, which stays PPAD-complete.

## History

Gilboa and Zemel (1989) gave the first NP-hardness results for properties of Nash equilibria, with a reduction from CLIQUE, and contrasted them with polynomial algorithms for correlated equilibria. Conitzer and Sandholm presented the SAT-based game at IJCAI 2003, with a list of NP-hard and #P-hard questions, and published the journal version with approximation results in Games and Economic Behavior in 2008. After 2006, the PPAD-completeness of finding any equilibrium made the difference between the two kinds of question clear.

## References
