---
tag: FWT8FT
kind: algorithm
slug: blum-mansour-reduction
name: Blum-Mansour swap regret reduction
aliases:
- external to swap regret reduction
area: algorithmic-game-theory/computing-equilibria
level: advanced
summary: Builds a no-swap-regret algorithm from k copies of a no-external-regret algorithm by playing the stationary distribution of their advice.
model: real-ram
complexity:
  vars: {k: the number of actions, T: the number of rounds}
  time: {worst: "O(T k^3)"}
  space: {extra: "O(k^2)"}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2007
  people: [Avrim Blum, Yishay Mansour]
  note: "Blum and Mansour gave the general reduction from swap regret to external regret, with swap regret O(sqrt(T k log k)) when the copies run multiplicative weights; earlier no-internal-regret methods were those of Foster and Vohra (1997) and Hart and Mas-Colell (2000)."
prereqs: [regret, multiplicative-weights-update, stationary-distribution, correlated-equilibrium]
see_also: [regret-matching, no-regret-dynamics, correlated-equilibrium-linear-program, expert-problem, coarse-correlated-equilibrium, no-regret-coarse-correlated-theorem, optimistic-hedge, markov-chain]
sources:
  - paper: "Avrim Blum and Yishay Mansour, From external to internal regret, Journal of Machine Learning Research 8 (2007), 1307-1324"
    title: From external to internal regret
    locator: "the generic reduction from swap regret to external regret, and its bound O(sqrt(T k log k)) with multiplicative weights"
  - book: isbn:9781316624791
    title: "Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016"
    locator: "Lecture 18 (swap regret, the reduction, and no-swap-regret dynamics converging to correlated equilibria)"
  - paper: doi:10.1111/1468-0262.00153
    title: "Sergiu Hart and Andreu Mas-Colell, A simple adaptive procedure leading to correlated equilibrium, Econometrica 68(5) (2000), 1127-1150"
    locator: Section 3 (regrets and correlated epsilon-equilibria)
  - book: isbn:9780521841085
    title: "Nicolo Cesa-Bianchi and Gabor Lugosi, Prediction, Learning, and Games, Cambridge University Press, 2006"
    locator: the treatment of internal and swap regret
---

The Blum-Mansour reduction turns any algorithm with small external [regret](/regret/) into one with small *swap regret*. External regret compares the learner with the best fixed action. Swap regret compares it with every rule $\delta$ that replaces each action $j$ by an action $\delta(j)$, applied to all the rounds at once. The reduction runs $k$ copies of the external regret algorithm, one for each action, and in each round plays the stationary distribution of the Markov chain whose rows are the copies' proposals. With [multiplicative weights](/multiplicative-weights-update/) as the copy, the swap regret after $T$ rounds is $O(\sqrt{T k \log k})$. In a game, if every player uses it, the empirical distribution of play is an approximate [correlated equilibrium](/correlated-equilibrium/), while external regret alone only gives a coarse correlated equilibrium ([no-regret convergence to coarse correlated equilibria](/no-regret-coarse-correlated-theorem/)). [Regret matching](/regret-matching/) reaches the same set by a simpler rule with a slower rate; the general scheme is [no-regret dynamics](/no-regret-dynamics/). This site has no separate page on swap regret, so it is defined below.

## In plain words

A learner chooses among $k$ actions each day and then sees what each action would have cost. It wants a strong guarantee: for every way of renaming its choices, such as "each time I chose A, I should have chosen B", the renamed history must not be much cheaper. The trick is to hire $k$ advisers, one for each action. Adviser $j$ is only responsible for the days on which the learner picks $j$, and is charged only for that share of the cost. Each adviser proposes a mix of actions. The learner then picks a mix that agrees with the advice: the chance of each action equals the total chance that the advisers, weighted by the mix itself, send it there. Each adviser only has to beat the best single action, which simple methods can do, and together they beat every renaming.

## The problem

There are $k$ actions and $T$ rounds. In round $t$ the learner chooses a distribution $p_t$ on the actions, then an adversary, who may know $p_t$, reveals a loss vector $\ell_t \in [0, 1]^k$, and the learner pays $p_t \cdot \ell_t$. For a map $\delta : \{1, \ldots, k\} \to \{1, \ldots, k\}$, the regret against $\delta$ is

$$R_T(\delta) = \sum_{t=1}^{T} \sum_{j=1}^{k} p_t(j)\,\big[\ell_t(j) - \ell_t(\delta(j))\big].$$

The *external regret* is the maximum over constant maps $\delta$, the *internal regret* is the maximum over maps that change one action $j$ into one other action $l$, and the *swap regret* is the maximum over all $k^k$ maps. The maximum over all maps splits into one choice for each $j$, so

$$\text{swap regret} = \sum_{j=1}^{k} \max_{l} \sum_{t=1}^{T} p_t(j)\,\big[\ell_t(j) - \ell_t(l)\big],$$

and it is at most $k$ times the internal regret. The goal is an online algorithm with swap regret $o(T)$ against every adversary.

## The algorithm

```pseudo id=main
BLUM-MANSOUR(A, k, T)           ▷ A is an algorithm with small external regret
L1  create k copies A_1, ..., A_k of A, each on the k actions
L2  for t ← 1 to T
L3      q_j ← the distribution that A_j proposes, for each j
L4      Q ← the k by k matrix whose row j is q_j
L5      p ← a distribution with p = p Q
L6      play p and observe the loss vector l^t
L7      give A_j the loss vector p(j) l^t, for each j
```

Line L1 creates one copy of the base algorithm for each action $j$; copy $j$ advises the learner what to play instead of $j$. Lines L3 and L4 collect the advice into a row-stochastic matrix $Q$, the transition matrix of a [Markov chain](/markov-chain/) on the actions. Line L5 picks a [stationary distribution](/stationary-distribution/) of that chain; it exists for every stochastic matrix, and it can be computed by [Gaussian elimination](/gaussian-elimination/) on the system $p(Q - I) = 0$, $\sum_j p(j) = 1$. When every entry of $Q$ is positive, as with multiplicative weights, it is unique. Line L7 charges copy $j$ only for its share $p(j)$ of the round, so copy $j$ sees losses in $[0, p(j)]$.

The stationary condition gives two views of the same round. On one side, $p \cdot \ell = \sum_i p(i) \ell(i)$. On the other side, $p(i) = \sum_j p(j) q_j(i)$, so $p \cdot \ell = \sum_j q_j \cdot (p(j)\,\ell)$, which is the sum of the losses that the copies are charged. This identity is the whole reduction.

## Example

Take $k = 2$ actions and multiplicative weights with $\eta = 1$ in each copy: copy $j$ proposes $q_j(a) \propto e^{-L_j(a)}$, where $L_j(a)$ is the total scaled loss of action $a$ given to copy $j$. For two actions the stationary distribution of line L5 is $p(1) = q_2(1) / (q_1(2) + q_2(1))$. The losses are $(1, 0)$, $(1, 0)$ and then $(0, 1)$. The numbers are rounded to four places.

| round | $q_1$ | $q_2$ | $p$ (line L5) | loss | copy 1 gets | copy 2 gets |
|---|---|---|---|---|---|---|
| 1 | (0.5, 0.5) | (0.5, 0.5) | (0.5, 0.5) | (1, 0) | (0.5, 0) | (0.5, 0) |
| 2 | (0.3775, 0.6225) | (0.3775, 0.6225) | (0.3775, 0.6225) | (1, 0) | (0.3775, 0) | (0.6225, 0) |
| 3 | (0.2937, 0.7063) | (0.2456, 0.7544) | (0.258, 0.742) | (0, 1) | (0, 0.258) | (0, 0.742) |
| 4 | (0.3499, 0.6501) | (0.406, 0.594) | (0.3844, 0.6156) | | | |

In the first two rounds both copies see the same losses up to a factor, but copy 2 is charged more in round 2 because $p(2) > p(1)$, so after round 2 the copies differ. In round 3, $p(1) = 0.2456 / (0.7063 + 0.2456) = 0.258$, and one checks $p Q = p$: $0.258 \cdot 0.2937 + 0.742 \cdot 0.2456 = 0.258$.

## Correctness

**Theorem.** Let $R^j$ be the external regret of copy $j$ on the losses $p_t(j)\ell_t$ that it receives. Then for every map $\delta$, $R_T(\delta) \le \sum_j R^j$. If each copy is multiplicative weights with rate $\eta$, the swap regret is at most $k \ln k / \eta + \eta T / 2$, which is $\sqrt{2 T k \ln k}$ for $\eta = \sqrt{2 k \ln k / T}$.

*Proof sketch.* By the identity above, the learner's total loss is $\sum_j \sum_t q_{t,j} \cdot (p_t(j)\ell_t)$, the sum of the copies' losses. The total loss under $\delta$ is $\sum_j \sum_t p_t(j)\ell_t(\delta(j))$, and for each $j$ this is the loss of the fixed action $\delta(j)$ on the losses of copy $j$. Subtract: the difference for each $j$ is at most the external regret of copy $j$. For multiplicative weights on losses in $[0, c_t]$, the regret is at most $\ln k / \eta + (\eta / 2) \sum_t c_t^2$; with $c_t = p_t(j)$ and $\sum_j p_t(j)^2 \le 1$ the sum over the copies gives the bound. The full proof is in the proof file.

In a game, let every player $i$ run the reduction on the losses $\ell_t(a) = (\max u_i - u_i(a, \sigma_{t,-i})) / \Delta_i$, where $\sigma_t$ is the profile of the distributions in round $t$ and $\Delta_i$ is the range of $u_i$. Let $z = \frac{1}{T}\sum_t \sigma_{t,1} \times \cdots \times \sigma_{t,n}$. Then, for each player, the largest gain from a swap under $z$ is exactly $\Delta_i$ times the swap regret divided by $T$, so $z$ is a correlated $\varepsilon$-equilibrium as soon as every player has swap regret at most $\varepsilon T / \Delta_i$. With multiplicative weights this takes $T = O(k \log k / \varepsilon^2)$ rounds for payoffs in $[0, 1]$.

## Complexity

Each round computes $k$ distributions of the copies, which takes $O(k^2)$ time for multiplicative weights, solves a $k$ by $k$ linear system in $O(k^3)$ time, and updates $k$ copies in $O(k^2)$ time. The total is $O(T k^3)$ time, or $O(T k^2)$ per round plus the cost of the stationary distribution if an iterative method such as [power iteration](/power-iteration/) is accurate enough. The memory is $O(k^2)$: $k$ copies of $k$ weights and the matrix $Q$. For an $\varepsilon$-correlated equilibrium of a game with payoffs in $[0, 1]$, the number of rounds is $O(k \log k / \varepsilon^2)$, and each round also needs the expected losses of each player, which costs $O(n k^n)$ for a game in normal form.

## Properties

- **Generic.** Any external regret algorithm can be plugged in. The swap regret bound is the sum of the copies' bounds, on scaled losses.
- **Deterministic distributions.** Given the losses, the distributions $p_t$ are fixed; a learner that must play pure actions samples from $p_t$, and the regret bounds then hold in expectation.
- **Full information.** Each copy needs the whole loss vector. Without it, the copies must be bandit algorithms such as [Exp3](/exp3/), with a worse dependence on $k$.
- **Stronger than external regret.** Small swap regret implies small external regret, since constant maps are swaps. The converse fails: if the learner plays action 1 against the losses $(1, 0)$ and then action 2 against $(0, 1)$, each fixed action loses 1 and the learner loses 2, but the swap of the two actions loses 0.

## Variants and improvements

- **Other base algorithms.** With [weighted majority](/weighted-majority/), [follow the leader](/follow-the-leader/) with perturbations, or any algorithm for the [expert problem](/expert-problem/), the bound changes accordingly. With regret matching as the base, the whole method uses no exponentials.
- **Internal regret.** Foster and Vohra and Hart and Mas-Colell (2000) gave earlier procedures with no internal regret. Since swap regret is at most $k$ times internal regret, these also give no swap regret, with a worse dependence on $k$.
- **Many actions.** For swap regret $\varepsilon T$, the bound of this reduction needs $T$ of order $k \log k / \varepsilon^2$ rounds, linear in $k$. In 2024, Dagan, Daskalakis, Fishelson and Golowich, and independently Peng and Rubinstein, gave a different reduction whose number of rounds for swap regret $\varepsilon T$ is polylogarithmic in $k$ but exponential in $1/\varepsilon$.
- **Faster rates in games.** Anagnostides, Daskalakis, Farina, Fishelson, Golowich and Sandholm (2022) ran [optimistic Hedge](/optimistic-hedge/) inside the copies and showed that, when all players learn this way, the swap regret of each player grows only polylogarithmically in $T$.

## When to use it

Use it when a learner must have no swap regret, for example to reach correlated rather than coarse correlated equilibria by repeated play, or when a forecast must be calibrated against each recommendation. If the game is small and given as a table, the [correlated equilibrium LP](/correlated-equilibrium-linear-program/) gives an exact answer instead. If only external regret matters, a single copy is enough and is $k$ times cheaper.

## Pitfalls

- **Unscaled losses in line L7.** If every copy gets the full loss vector $\ell_t$, all copies see the same inputs, propose the same distribution, and the method is the base algorithm with only external regret. Copy $j$ must get $p_t(j)\ell_t$.
- **The wrong distribution in line L5.** Playing the average of the rows of $Q$, or the row of the last action, breaks the identity $p \cdot \ell = \sum_j q_j \cdot (p(j)\ell)$, and the bound fails. Only a fixed point $p = pQ$ works.
- **Power iteration in line L5.** If a copy can propose distributions with zeros, such as follow the leader, the chain may be periodic and power iteration may not converge. Solve the linear system instead, or mix $Q$ with a small amount of the uniform matrix and account for the extra regret.
- **Comparing the wrong regrets.** Swap regret is a sum over $j$ of separate maxima. Taking a single maximum over pairs $(j, l)$ gives the internal regret, which can be smaller by a factor up to $k$.

## Implementations

The Python code implements multiplicative weights (Hedge), the stationary distribution by Gaussian elimination with partial pivoting, and the reduction of lines L1 to L7, in floating point. The tests check the stationary step on random positive stochastic matrices, the identity that splits the learner's loss among the copies, the swap regret bound $k \ln k / \eta + \eta t / 2$ after every round against random, adaptive and periodic adversaries, and, in self-play in chicken, rock-paper-scissors and a random three-player game, that the correlated equilibrium gap of the empirical distribution equals the scaled swap regret.

## History

Foster and Vohra (1997) showed that players who best respond to calibrated forecasts reach correlated equilibria, and procedures with no internal regret followed. Hart and Mas-Colell (2000) gave regret matching. Blum and Mansour gave the general reduction from external to swap regret; the conference version appeared at COLT in 2005 and the journal version in 2007. Roughgarden's lecture notes made it the standard proof that no-swap-regret dynamics converge to correlated equilibria.

## References
