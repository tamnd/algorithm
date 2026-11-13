---
title: Expectiminimax returns the value of a finite stochastic game tree, and pure strategies reach it
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The tree is finite. A pure strategy $\sigma$ of MAX picks one child at every MAX node, and a pure strategy $\tau$ of MIN picks one child at every MIN node. For a node $n$, let $E_n(\sigma, \tau)$ be the expected payoff of the play that starts at $n$, follows $\sigma$ and $\tau$ at decision nodes, and draws the children of chance nodes with their probabilities. Only the choices of $\sigma$ and $\tau$ inside the subtree of $n$ matter, so we may view $\sigma$ and $\tau$ as strategies of that subtree.

**Termination.** Each call on a node calls itself only on the children of that node. The tree is finite, so the recursion visits each node once and stops.

**Claim.** For every node $n$,

$$\text{EXPECTIMINIMAX}(n) \;=\; \max_\sigma \min_\tau E_n(\sigma, \tau) \;=\; \min_\tau \max_\sigma E_n(\sigma, \tau).$$

We prove it by induction on the height of $n$. Write $v(n)$ for the returned value.

**Leaf (line L1).** There is nothing to choose, $E_n = \mathrm{UTILITY}(n)$, and all three numbers are equal.

**Independence of subtrees.** Let $n$ be an internal node with children $c_1, \ldots, c_k$. The subtrees of the children are disjoint, so a strategy $\sigma$ in the subtree of $n$ is the choice at $n$ (if $n$ is a MAX node) together with independent strategies $\sigma_1, \ldots, \sigma_k$ in the subtrees of the children, and the same holds for $\tau$. By the induction hypothesis, $\max_{\sigma_c}\min_{\tau_c} E_c = \min_{\tau_c}\max_{\sigma_c} E_c = v(c)$ for each child $c$.

**Chance node (line L4).** Here $E_n(\sigma, \tau) = \sum_c p_c E_c(\sigma_c, \tau_c)$ with $p_c \ge 0$. The term of child $c$ depends only on $(\sigma_c, \tau_c)$, so for fixed $\sigma$ the minimum over the independent $\tau_c$ splits into a sum: $\min_\tau E_n = \sum_c p_c \min_{\tau_c} E_c(\sigma_c, \tau_c)$, because $p_c \ge 0$. The maximum over the independent $\sigma_c$ splits in the same way, so $\max_\sigma\min_\tau E_n = \sum_c p_c v(c)$. The same argument in the other order gives $\min_\tau\max_\sigma E_n = \sum_c p_c v(c)$, which is the value of line L4.

**MAX node (line L2).** MAX picks a child $c$ and then plays $\sigma_c$, so $E_n(\sigma, \tau) = E_c(\sigma_c, \tau_c)$ for the chosen $c$. For fixed $\sigma$, only $\tau_c$ matters, so

$$\max_\sigma \min_\tau E_n = \max_c \max_{\sigma_c} \min_{\tau_c} E_c = \max_c v(c).$$

For the other order, fix $\tau = (\tau_1, \ldots, \tau_k)$. Then $\max_\sigma E_n = \max_c f_c(\tau_c)$ with $f_c(\tau_c) = \max_{\sigma_c} E_c(\sigma_c, \tau_c)$. Each $f_c$ depends on its own coordinate only, so MIN can minimize all of them at once: with $\tau_c^*$ a minimizer of $f_c$, $\max_c f_c(\tau_c^*) = \max_c \min_{\tau_c} f_c = \max_c v(c)$, and no $\tau$ does better, since $\max_c f_c(\tau_c) \ge f_{c'}(\tau_{c'}) \ge v(c')$ for every $c'$. So $\min_\tau \max_\sigma E_n = \max_c v(c)$, the value of line L2.

**MIN node (line L3).** This is the MAX case with the roles of the players and of max and min exchanged, and both orders give $\min_c v(c)$.

This proves the claim. $\blacksquare$

**Consequences.**

1. The value is the same whichever player commits first, so it is the value of the game in pure strategies. Mixed strategies cannot do better, since the expected payoff of a mixed strategy is an average of the expected payoffs of pure ones.
2. The strategy $\sigma^*$ that picks at each MAX node a child of largest value $v(c)$ reaches $\min_\tau E_n(\sigma^*, \tau) = v(n)$, by the same induction. In particular the move returned by BEST-MOVE at the root is optimal.
3. If every leaf value $u$ is replaced by $\alpha u + \beta$ with $\alpha > 0$, every value $v(n)$ becomes $\alpha v(n) + \beta$, by induction on the lines L1 to L4, so the decisions do not change. For other increasing changes line L4 does not commute with the change, and the decisions can change, as the example on the page shows.
