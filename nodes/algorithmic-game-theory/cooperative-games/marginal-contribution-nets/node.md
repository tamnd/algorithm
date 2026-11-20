---
tag: J0TAYV
kind: data-structure
slug: marginal-contribution-nets
name: Marginal contribution nets
aliases:
- MC-nets
area: algorithmic-game-theory/cooperative-games
level: advanced
summary: Represents a TU game by rules of the form pattern of players gives value, with Shapley values computable in time linear in the rules.
model: word-ram
complexity:
  vars: {z: the total number of literals in all rules, n: the number of players}
  time: {value: O(z), shapley: O(z + n), banzhaf: O(z + n)}
  space: {rules: O(z)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2005
  people: [Samuel Ieong, Yoav Shoham]
  note: Ieong and Shoham introduced marginal contribution nets at the ACM Conference on Electronic Commerce in 2005, with the linear-time Shapley value and algorithms for the core.
prereqs: [transferable-utility-game, shapley-value]
see_also: [shapley-uniqueness-theorem, banzhaf-index, core-of-a-cooperative-game, weighted-voting-game, mobius-inversion, treewidth, boolean-function, shapley-value-sampling]
sources:
  - paper: doi:10.1145/1064009.1064030
    title: "Samuel Ieong and Yoav Shoham, Marginal contribution nets: a compact representation scheme for coalitional games, Proceedings of the 6th ACM Conference on Electronic Commerce (EC 2005), 193-202"
    locator: the rules with conjunctions of literals, the Shapley value in time linear in the size of the net, and the core algorithms by tree decomposition
  - paper: doi:10.1287/moor.19.2.257
    title: "Xiaotie Deng and Christos H. Papadimitriou, On the complexity of cooperative solution concepts, Mathematics of Operations Research 19(2) (1994), 257-266"
    locator: the games on weighted graphs, whose Shapley value is half the weight of the edges at each node
  - book: isbn:9781608456529
    title: Georgios Chalkiadakis, Edith Elkind and Michael Wooldridge, Computational Aspects of Cooperative Game Theory, Morgan and Claypool, 2011
    locator: Chapter 3, Representations and algorithms (induced subgraph games and marginal contribution nets)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Section 12.3.5, Marginal contribution nets
---

A marginal contribution net (MC-net) stores a TU game as a list of rules. Each rule names some players that must be in a coalition, some players that must be out of it, and a value. The worth of a coalition is the sum of the values of the rules that it meets. A game in which the players interact in small groups gets a short net, where the table of $v$ has $2^n$ entries. The main point of the structure is that the [Shapley value](/shapley-value/) of a net takes time linear in its size, because each rule is a small game with a closed-form value and the value is additive ([Shapley's uniqueness theorem](/shapley-uniqueness-theorem/)). An MC-net is a representation of one game; the solution concepts on top of it, such as the [core](/core-of-a-cooperative-game/), have their own pages.

## In plain words

Think of a list of bonus rules for a team. "If Ann and Bob both join, add 4." "If Ann and Cid both join, add 2." "If Dan joins and Eve does not, add 1." To find what a team is worth, check every rule and add up the bonuses that apply. To split the worth fairly with the Shapley value, you do not need to look at all the teams. Each rule hands out its own bonus: a rule with only people who must be present splits its bonus equally among them, and a rule that also names people who must be absent gives a share to the first kind and takes a share from the second kind. Add up the shares from all the rules, and you have each person's value.

## The abstract type

The structure holds a TU game $(N, v)$ with $N = \{1, \ldots, n\}$ and $v(\emptyset) = 0$, and supports these operations:

- VALUE$(S)$: return $v(S)$ for a coalition $S \subseteq N$.
- SHAPLEY: return the Shapley value $\varphi(v) \in \mathbb{R}^n$.
- BANZHAF: return the Banzhaf value $\beta(v)$, where $\beta_i(v) = 2^{-(n-1)} \sum_{S \subseteq N \setminus \{i\}} (v(S \cup \{i\}) - v(S))$.
- Build the net from a table of $v$ (FROM-GAME), and add or remove a rule.

## Representation

A *rule* is a triple $r = (P, Q, x)$: a nonempty set $P$ of positive literals, a set $Q$ of negative literals with $P \cap Q = \emptyset$, and a number $x$. Ieong and Shoham write it as a pattern of literals, for example $\{1, 3, \neg 2\} \to 1$. The rule *applies* to $S$ if $P \subseteq S$ and $Q \cap S = \emptyset$. The net is a list $R$ of rules, and its game is

$$v_R(S) = \sum_{(P, Q, x) \in R,\ P \subseteq S,\ Q \cap S = \emptyset} x.$$

Since $P \ne \emptyset$, no rule applies to $\emptyset$, so $v_R(\emptyset) = 0$. The size of the net is $z = \sum_{r} (|P| + |Q|)$, the number of literals. In memory, each rule is two short lists or two bit masks of players and one number. With bit masks and $n$ at most the word size, a test "$P \subseteq S$ and $Q \cap S = \emptyset$" is two word operations.

Every game has a net with positive literals only. Write $v = \sum_{T \ne \emptyset} d_T\, u_T$, where $u_T$ is the unanimity game of $T$ and $d_T = \sum_{S \subseteq T} (-1)^{|T| - |S|} v(S)$ is the Harsanyi dividend ([Möbius inversion](/mobius-inversion/)). The rules $(T, \emptyset, d_T)$ for the $T$ with $d_T \ne 0$ form a net for $v$. With negative literals the net can be much shorter, as the example below shows.

## Operations

Write $a = |P|$ and $b = |Q|$ for a rule.

```pseudo id=main
VALUE(R, S)
L1  total ← 0
L2  for each rule (P, Q, x) in R do
L3      if P ⊆ S and Q ∩ S = ∅ then total ← total + x
L4  return total

SHAPLEY(R, n)
L5  phi[i] ← 0 for each player i
L6  for each rule (P, Q, x) in R do          ▷ a = |P|, b = |Q|
L7      for each i in P do
L8          phi[i] ← phi[i] + x (a-1)! b! / (a+b)!
L9      for each j in Q do
L10         phi[j] ← phi[j] - x a! (b-1)! / (a+b)!
L11 return phi

BANZHAF(R, n)
L12 beta[i] ← 0 for each player i
L13 for each rule (P, Q, x) in R do
L14     share ← x / 2^(a+b-1)
L15     for each i in P do beta[i] ← beta[i] + share
L16     for each j in Q do beta[j] ← beta[j] - share
L17 return beta
```

Players that occur in no rule are null players and keep the value 0. A rule with $b = 0$ splits $x$ equally among the players of $P$, which is the value of the game $x\, u_P$. To add a rule, append it; to remove one, delete it. Both change $v$ by the game of that one rule.

FROM-GAME computes the dividends of all $2^n - 1$ nonempty coalitions from a table of $v$ and keeps the nonzero ones. The direct sum over subsets takes $O(3^n)$ time. The fast Möbius transform over the subset lattice takes $O(n\, 2^n)$.

## Example

**Positive rules only.** The game with $v(\{1, 2\}) = 4$, $v(\{1, 3\}) = 2$, $v(N) = 6$ and $v(S) = 0$ otherwise is the net

$$\{1, 2\} \to 4, \qquad \{1, 3\} \to 2.$$

VALUE$(\{1, 2, 3\}) = 4 + 2 = 6$, and VALUE$(\{2, 3\}) = 0$ since no rule applies. SHAPLEY gives player 1 the share $4 \cdot 1!\, 0!/2! = 2$ from the first rule and $1$ from the second, player 2 gets $2$ and player 3 gets $1$: $\varphi = (3, 2, 1)$. BANZHAF gives the shares $4/2^{1} = 2$ and $2/2^1 = 1$ in the same way, so $\beta = (3, 2, 1)$ as well.

**A rule with a negative literal.** The weighted voting game $[51; 50, 49, 1]$ wins exactly on $\{1, 2\}$, $\{1, 3\}$ and $\{1, 2, 3\}$. Two rules describe it:

$$\{1, 2\} \to 1, \qquad \{1, 3, \neg 2\} \to 1.$$

The first rule applies to $\{1, 2\}$ and $\{1, 2, 3\}$, and the second only to $\{1, 3\}$, so each winning coalition gets exactly 1. For SHAPLEY, the first rule ($a = 2$, $b = 0$) gives $1/2$ to players 1 and 2. The second rule ($a = 2$, $b = 1$) gives $1 \cdot 1!\, 1!/3! = 1/6$ to players 1 and 3 and $-1 \cdot 2!\, 0!/3! = -1/3$ to player 2. The sums are

$$\varphi = \left(\tfrac{1}{2} + \tfrac{1}{6},\ \tfrac{1}{2} - \tfrac{1}{3},\ \tfrac{1}{6}\right) = \left(\tfrac{2}{3}, \tfrac{1}{6}, \tfrac{1}{6}\right),$$

the Shapley-Shubik index of the game. For BANZHAF the shares are $1/2$ from the first rule and $\pm 1/4$ from the second, so $\beta = (3/4, 1/4, 1/4)$, the raw Banzhaf index. A single rule can give a negative share, but the sum is right. The net from the dividends has three rules instead: $\{1, 2\} \to 1$, $\{1, 3\} \to 1$ and $\{1, 2, 3\} \to -1$.

**Negative literals save space.** Let $v(S) = 1$ if $S$ meets a set $A = \{a_1, \ldots, a_k\}$ and $v(S) = 0$ if not. Its dividends are $d_T = (-1)^{|T|+1}$ for every nonempty $T \subseteq A$, so the net with positive literals only has $2^k - 1$ rules. With negative literals, $k$ rules are enough: $\{a_1\} \to 1$, $\{a_2, \neg a_1\} \to 1$, and in general $\{a_j, \neg a_1, \ldots, \neg a_{j-1}\} \to 1$. For each $S$ that meets $A$, exactly the rule of the smallest $j$ with $a_j \in S$ applies. SHAPLEY gives each player of $A$ the value $1/k$.

**Graph games.** For a weighted graph on the players, let $v(S)$ be the total weight of the edges with both ends in $S$ (Deng and Papadimitriou 1994). The net has one rule $\{i, j\} \to w_{ij}$ per edge, and SHAPLEY gives each player half the weight of its edges.

## Correctness

VALUE adds exactly the values of the rules that apply, which is the definition of $v_R$. For SHAPLEY, take one rule $(P, Q, x)$ and a uniform random order. A player $i \in P$ adds $x$ exactly when all of $P \setminus \{i\}$ comes before it and all of $Q$ comes after it. Among the $(a+b)!$ relative orders of $P \cup Q$, there are $(a-1)!\, b!$ such orders. A player $j \in Q$ adds $-x$ exactly when all of $P$ comes before it and all of $Q \setminus \{j\}$ after it, in $a!\, (b-1)!$ orders. The other players never change whether the rule applies. The Shapley value is additive, so the values of the rules add up. For BANZHAF, the marginal contribution of $i \in P$ to $S$ is $x$ for the $2^{n-a-b}$ sets $S \subseteq N \setminus \{i\}$ that contain $P \setminus \{i\}$ and avoid $Q$, which gives $x / 2^{a+b-1}$, and the same count holds for $j \in Q$. The full proofs are in [the proof file](proofs/correctness.md).

## Complexity

Let $z$ be the number of literals in the net and $n$ the number of players.

- **VALUE** takes $O(z)$ time with $S$ in a hash set or a Boolean array. With bit masks and $n$ at most the word size, it takes $O(k)$ time for $k$ rules.
- **SHAPLEY** and **BANZHAF** take $O(z + n)$ arithmetic operations: $O(n)$ to clear the output, and $O(1)$ per literal with a table of the factorials $0!, \ldots, n!$ or of the powers of 2. With integer rule values the results are rationals whose denominators divide $n!$ (for SHAPLEY) or $2^{n-1}$ (for BANZHAF), so exact arithmetic adds $O(n \log n)$ bits to the numbers.
- **Space** is $O(z)$ words for the rules.
- **FROM-GAME** takes $O(n\, 2^n)$ time from a table of $v$, and can return $2^n - 1$ rules.

The size of the net is the right measure: the Shapley value is linear in it, but a net can itself be large. The OR game above needs $2^k - 1$ positive rules, and other games, such as a majority game on many players, have dense dividends and need long nets.

Other questions are harder on nets. Ieong and Shoham (2005) show that questions about the core are intractable on general nets. They give algorithms for core membership and core emptiness whose time is exponential only in the [treewidth](/treewidth/) of the graph that links two players when they share a rule, using a [tree decomposition](/tree-decomposition/).

## Variants

- **Positive literals only.** The net is the list of the nonzero Harsanyi dividends. It is unique for each game and has the dividend formula $\varphi_i = \sum_{T \ni i} d_T / |T|$ directly.
- **Graph games** (induced subgraph games): rules with two positive literals. The Shapley value is half the weighted degree. Deng and Papadimitriou (1994) study their core.
- **Patterns other than conjunctions.** A rule can use a Boolean formula as the pattern. A conjunction of literals keeps the closed form of SHAPLEY; for other formulas the value of a rule is no longer a single formula in $a$ and $b$.
- **Banzhaf and other semivalues.** Any value that is linear in $v$ can be computed rule by rule in the same way, with the value of one rule in closed form, as BANZHAF does.

## When to use it

Use an MC-net when the worth of a coalition comes from many small interactions: pairs or small groups of players that create a bonus together, with some exceptions when a certain player is present. It is the natural format when you need Shapley or Banzhaf values exactly for many players and the game is sparse in this sense. If the game is a [weighted voting game](/weighted-voting-game/), use its weights and [dynamic programming](/power-index-dynamic-programming/) instead, since threshold games rarely have short nets. If the game is only an oracle, use [sampling](/shapley-value-sampling/).

## Pitfalls

- **An empty positive part.** A rule with $P = \emptyset$ applies to the empty coalition and breaks $v(\emptyset) = 0$. A rule with $P \cap Q \ne \emptyset$ never applies. Reject both when the net is built.
- **Signs of the negative literals.** The share of $j \in Q$ is $-x\, a!\, (b-1)!/(a+b)!$, with $a!$ and $(b-1)!$, not the mirror of the share of $P$. With $a = 2$, $b = 1$ and $x = 1$, the players of $P$ get $1/6$ each and the player of $Q$ gets $-1/3$.
- **Negative shares are normal.** A single rule can give a negative share even when the game is monotone. Check only the total.
- **The net is not unique.** With negative literals, many nets describe the same game. Two nets are equal as games only if their dividends are equal, and computing the dividends can take exponential time.
- **Converting into a net can be expensive.** The Shapley value is linear in the size of the net, not in the size of some other description of the game.

## Implementations

The Python version stores a rule as two frozensets and a value, and returns exact Fractions for the Shapley and Banzhaf values. FROM-GAME uses the direct dividend sum, which is fine for the small $n$ where a full table of $v$ exists.

## History

Ieong and Shoham (2005) introduced marginal contribution nets at the ACM Conference on Electronic Commerce, as a representation that is both expressive and fast for the Shapley value. They proved that the Shapley value takes linear time in the size of the net and studied the core through the treewidth of the interaction graph. Their work built on the graph games of Deng and Papadimitriou (1994), which are nets whose rules have two players. The textbooks of Shoham and Leyton-Brown (2009) and of Chalkiadakis, Elkind and Wooldridge (2011) cover MC-nets among the compact representations of coalitional games.

## References
