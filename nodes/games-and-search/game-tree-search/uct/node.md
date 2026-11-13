---
tag: TGTRKB
kind: algorithm
slug: uct
name: Upper confidence bounds applied to trees
aliases:
- UCT
- UCB for trees
area: games-and-search/game-tree-search
level: advanced
summary: Tree policy in MCTS that picks children by UCB1 value plus an exploration bonus.
model: real-ram
complexity:
  vars: {n: the number of iterations, b: the largest number of actions at a node, d: the depth of the tree}
  time: {worst: O(n b d), best: O(n b d)}
  space: {extra: O(n d b)}
properties: {randomized: true, anytime: true, iterative: true, approximate: true}
prereqs: [monte-carlo-tree-search, ucb1, multi-armed-bandit]
see_also: [rapid-action-value-estimation, rollout-algorithm, markov-decision-process, hoeffding-inequality, regret, minimax, exp3, alpha-beta-pruning]
sources:
  - paper: doi:10.1007/11871842_29
    title: "Levente Kocsis and Csaba Szepesvári, Bandit based Monte-Carlo planning, Machine Learning (ECML 2006), LNCS 4212, Springer, 2006, 282-293"
    locator: Section 2.1 (rollout-based planning, Figure 1), Section 2.3 (the UCT rule with bias 2 Cp sqrt(ln t / s)), Section 2.4 and Theorems 1 to 6 (the analysis; Theorem 6 is the main result), Section 3 (experiments on P-games)
  - paper: doi:10.1023/A:1013689704352
    title: "Peter Auer, Nicolò Cesa-Bianchi and Paul Fischer, Finite-time analysis of the multiarmed bandit problem, Machine Learning 47(2-3) (2002), 235-256"
    locator: the UCB1 policy and Theorem 1, the bound 8 ln n / Δ² + 1 + π²/3 on the expected number of plays of a worse arm
  - paper: arXiv:cs/0703062
    title: "Pierre-Arnaud Coquelin and Rémi Munos, Bandit algorithms for tree search, UAI 2007, 67-74"
    locator: trees on which UCT is too optimistic and has regret of order exp(exp(D)), and a modified rule with regret O(2^D sqrt(n))
  - paper: arXiv:1902.05213
    title: "Devavrat Shah, Qiaomin Xie and Zhi Xu, Non-asymptotic analysis of Monte Carlo tree search, 2019"
    locator: the abstract and the main result, convergence of MCTS with a polynomial instead of a logarithmic bonus
  - book: isbn:9781108486828
    title: Tor Lattimore and Csaba Szepesvári, Bandit Algorithms, Cambridge University Press, 2020
    locator: Chapter 7 (the upper confidence bound algorithm and its analysis)
  - paper: doi:10.1109/TCIAIG.2012.2186810
    title: "Cameron B. Browne et al., A survey of Monte Carlo tree search methods, IEEE Transactions on Computational Intelligence and AI in Games 4(1) (2012), 1-43"
    locator: the section on UCT, the choice of the constant, and the variants of the tree policy
---

UCT, short for upper confidence bounds applied to trees, is the rule that most [Monte Carlo tree search](/monte-carlo-tree-search/) programs use to walk down their tree. At each node it treats the choice of a child as a multi-armed bandit and picks the child with the largest mean reward plus a bonus that grows when the child has been tried rarely, as in [UCB1](/ucb1/). Kocsis and Szepesvári (2006) proposed it for planning in Markov decision processes and games and gave a proof that the probability of choosing a wrong action at the root goes to zero, an analysis that Shah, Xie and Xu (2019) later questioned (see Correctness). The name UCT is also the slug of this page.

## In plain words

At each position in the search tree you have a few moves to choose from, and you have tried each a few times. You could always take the move with the best average so far, but a move tried only twice may just have been unlucky. So you give every move an extra bonus that is large when the move has been tried few times compared with its siblings, and you pick the move with the best average plus bonus. A good move is chosen again and again. A bad move is still tried now and then, but less and less often. You use the same rule at every level of the tree.

## The problem

The input is a finite tree in which each internal node is a decision of one of two players (or of a single agent), and each leaf gives a reward in $[0, 1]$. The reward may be random, as in a Markov decision process with a horizon. The input also includes a budget of $n$ iterations. The output is an action at the root. The goal is the optimal action: the [minimax](/minimax/) move of a game, or the action of largest expected return in an MDP.

## The algorithm

```pseudo id=main
UCT(root, n)
L1  repeat n times: SEARCH(root)
L2  return the action a at the root with the largest mean Q(root, a)

SEARCH(s)
L3  if s is a leaf then return a reward r drawn at s
L4  if some action of s has N(s, a) = 0 then a ← the first such action
L5  else a ← the action with the largest Q(s, a) + 2 C_p √(ln N(s) / N(s, a)), with Q seen by the player at s
L6  r ← SEARCH(the child of s by a)
L7  N(s) ← N(s) + 1; N(s, a) ← N(s, a) + 1
L8  add r to the total reward of (s, a), so Q(s, a) = total / N(s, a)
L9  return r
```

The bias term $c_{t,s} = 2C_p\sqrt{\ln t/s}$ is the one of Kocsis and Szepesvári (Section 2.3). With $C_p = 1/\sqrt2$ it equals the UCB1 bonus $\sqrt{2\ln t/s}$ for rewards in $[0, 1]$. At a node of the minimizing player, $Q$ is the reward of that player, $1 - Q$ for rewards to MAX. Line L4 tries every action once before line L5 applies. The implementation stores a node for every position on the path, as in the original paper, and keeps the total reward rather than a running mean, so that equal statistics give exactly equal scores. In a program with a large tree, line L3 is replaced by the expansion of one node and a random playout, as on the page [MCTS](/monte-carlo-tree-search/).

## Example

**A bandit.** With one level and two Bernoulli leaves of means 0.9 and 0.6, UCT is UCB1. Averaged over 50 seeds, the worse arm was tried 22.9 times in 100 iterations, 81.2 times in 1000 and 127.5 times in 4000. The bound of Auer, Cesa-Bianchi and Fischer, $8\ln n/\Delta^2 + 1 + \pi^2/3$ with $\Delta = 0.3$, gives 414, 618 and 742. The counts grow like $\ln n$, and the bound is valid but loose.

**A small game.** MAX chooses A or B, and then MIN chooses a leaf. Below A the leaves are $1, 1, 1, 0$, and below B they are $1/2, 1/2$. The minimax value of A is 0 and that of B is 1/2, although the average of the leaves under A is 3/4. With fixed leaf values and seed 0:

| iterations | tries of A | Q(A) | tries of B | tries of MIN's replies under A | choice |
|---|---|---|---|---|---|
| 10 | 5 | 0.6 | 5 | 1, 1, 1, 2 | A |
| 100 | 30 | 0.3 | 70 | 3, 3, 3, 21 | B |
| 1000 | 77 | 0.195 | 923 | 5, 5, 5, 62 | B |
| 10000 | 120 | 0.15 | 9880 | 6, 6, 6, 102 | B |

MIN finds its reply 0 under A, and the bad replies are still tried, but only about $\ln n$ times each. So $Q(A)$ falls toward 0 slowly, with a bias of order $\log n/n$ times the number of bad replies, and $A$ itself gets $O(\log n)$ tries. With random leaves that pay 1 with the given probability, UCT chose A in 46 of 100 runs after 20 iterations and in none after 100 or 300.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows that at one level UCT is UCB1, so a worse action is tried at most $8\ln n/\Delta^2 + 1 + \pi^2/3$ times in expectation (Theorem 1 of Auer et al., with a full proof by Hoeffding's inequality), and the mean at the root converges to the best value. For deeper trees, the rewards that reach a node drift as the search below it improves. Kocsis and Szepesvári first analyze UCB1 with such drifting rewards (their Theorems 1 to 5). Their Theorem 6 then states, for a finite-horizon MDP with rewards in $[0, 1]$, horizon $D$ and $K$ actions, with the bias multiplied by $D$, that the bias of the estimated value at the root is $O(\log n/n)$ and that the probability of choosing a wrong action at the root goes to 0 at a polynomial rate. Shah, Xie and Xu (2019) argued that this kind of analysis with a logarithmic bonus assumes a concentration of the regret that is unlikely to hold, and they proved the guarantee for a variant with a polynomial bonus. For a finite tree with fixed payoffs, the consistency proof on the page [MCTS](/monte-carlo-tree-search/) applies to UCT as well.

## Complexity

**Time.** An iteration goes down at most $d$ levels and compares up to $b$ scores at each level, so $n$ iterations cost $O(nbd)$, plus the cost of the leaf rewards or playouts.

**Space.** This version stores every node on the path, $O(d)$ new nodes per iteration with $b$ counters each, so $O(ndb)$ in the worst case. With one new node per iteration, as in MCTS, it is $O(nb)$.

**Iterations needed.** The theory gives rates, not a practical budget. Kocsis and Szepesvári observed on random P-games that UCT needs about as many iterations as alpha-beta needs leaf evaluations, about $B^{D/2}$ for branching $B$ and depth $D$. Coquelin and Munos (2007) built trees of depth $D$ on which the regret of UCT is of order $\exp(\exp(D))$.

## Properties

- **Bandit at every node.** Each node runs its own UCB1 on rewards that change as the search below it learns.
- **Consistent.** With enough iterations it picks the optimal action, with fixed or random rewards.
- **No pruning.** A clearly bad action is still tried $O(\log n)$ times, so UCT never proves that a move is bad.
- **Scale dependent.** The bonus assumes rewards in $[0, 1]$. Other ranges need a rescaled $C_p$.
- **Deterministic given the rewards.** With fixed leaves and the first-untried rule, UCT uses no random numbers at all; the randomness is in the rewards or the playouts.

## Variants and improvements

- **Tuning $C_p$.** In games, values well below $1/\sqrt2$ often play better, because they exploit more. [RAVE](/rapid-action-value-estimation/) adds a second estimate to $Q$ that learns quickly in the first iterations.
- **UCB1-tuned and other bandit rules.** The bonus can use the observed variance of the rewards. [EXP3](/exp3/) is used at nodes where players move at the same time, because it handles adversarial rewards.
- **PUCT.** AlphaGo and AlphaZero use a bonus of the form $c\,P(s, a)\sqrt{N(s)}/(1 + N(s, a))$, with a prior $P$ from a policy network. It grows like $\sqrt{N}$, not $\sqrt{\ln N}$.
- **Polynomial bonus.** Shah, Xie and Xu replace $\sqrt{\ln t}$ by a power of $t$ and give a non-asymptotic proof.
- **Modified UCT.** Coquelin and Munos add a bonus that depends on the depth and obtain regret $O(2^D\sqrt n)$.

## When to use it

Use UCT as the tree policy of an MCTS program, and as a planner for an MDP when you have a simulator but cannot enumerate the states. It needs rewards on a known scale and works best when the number of actions per node is moderate, so that each can be tried once. With very many actions, use progressive widening or a learned prior (PUCT). When a good evaluation function exists and the game has sharp tactics, [alpha-beta pruning](/alpha-beta-pruning/) can be better, and a [rollout algorithm](/rollout-algorithm/) is simpler when one step of lookahead with a good base policy is enough.

## Pitfalls

- **Rewards outside $[0, 1]$.** Rewards of $-1$ and $1$ double the range, and with the same constant UCT explores too little.
- **Sign at MIN nodes.** Each player must maximize its own reward. Taking the MAX reward at every node makes MIN choose its worst moves.
- **Taking a log of 0.** The bonus is not defined until every action has been tried once; line L4 handles this.
- **Expecting the bound to set the budget.** The guarantees are asymptotic or loose. Measure how often the chosen move changes as $n$ grows.
- **Confusing the alias.** UCT is the selection rule plus the search loop. The MCTS page covers the full four-phase method and its other tree policies.

## Implementations

## History

Auer, Cesa-Bianchi and Fischer (2002) gave UCB1 and its finite-time bound for bandits. Kocsis and Szepesvári presented UCT at ECML 2006 as bandit-based Monte Carlo planning, with experiments on P-games and on a sailing problem. In the same year Gelly, Wang, Munos and Teytaud used UCT in the Go program MoGo, which soon became one of the strongest programs at 9x9 Go, and UCT became the standard tree policy of MCTS. Coquelin and Munos (2007) showed its worst case, and later work, such as that of Shah, Xie and Xu (2019), revisited its analysis. AlphaGo (2016) replaced the logarithmic bonus by the PUCT rule with learned priors.

## References
