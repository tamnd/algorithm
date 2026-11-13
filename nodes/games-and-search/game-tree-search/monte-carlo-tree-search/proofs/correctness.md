---
title: On a finite game tree, MCTS with UCB1 selection returns a minimax move once the number of playouts is large enough
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page with a constant $C > 0$ and any fixed rule to break ties. The game tree is finite, the players alternate, and each final position has a fixed payoff in $[0, 1]$ to player 0. For a position $u$ let $p(u)$ be the player to move at $u$ and, if $u$ is not the root, $m(u)$ the player who moved into $u$, so $m(c) = p(u)$ for a child $c$ of $u$ and $p(u) = 1 - m(u)$. Write $\mathrm{val}_i(u)$ for the minimax value of $u$ to player $i$, so $\mathrm{val}_1 = 1 - \mathrm{val}_0$. A stored node $u$ keeps $N(u)$ and the total reward $W(u)$ of $m(u)$, and $Q(u) = W(u)/N(u)$.

**Termination.** In each iteration, line L4 moves down the stored tree, which is finite, and line L6 plays moves in a finite game tree, where every move goes one level deeper. So each iteration stops, and the search stops after $n$ iterations.

**Counts.** A node is created in line L5 during one iteration, and that iteration counts as its first visit. Every later visit of $u$ continues to exactly one child: in line L5 if $u$ still has an untried move, and in line L4 otherwise. Line L8 counts the visit at that child too. Hence

$$N(u) = 1 + \sum_c N(c), \qquad W(u) = r_0(u) + \sum_c \big(N(c) - W(c)\big), \tag{1}$$

where $r_0(u) \in [0, 1]$ is the reward of $m(u)$ in the creation visit, and the second sum uses that $c$ stores the reward of $p(u) = 1 - m(u)$.

**Lemma 1. If $u$ is visited infinitely often and is not final, then every child of $u$ is created and visited infinitely often.** The first visits of $u$ after its creation expand its moves one by one, so after finitely many visits all children exist and every visit selects a child by line L4. Suppose the set $B$ of children with a bounded count is not empty, and let $M$ bound their counts. After some time no child in $B$ is selected. Suppose a child $c' \notin B$ is selected when the count of $u$ is $t$. Its score is at least the score of any $c \in B$, and $0 \le Q \le 1$, so

$$1 + C\sqrt{\ln t / N(c')} \;\ge\; Q(c') + C\sqrt{\ln t / N(c')} \;\ge\; Q(c) + C\sqrt{\ln t / N(c)} \;\ge\; C\sqrt{\ln t / M}.$$

Once $C\sqrt{\ln t/M} \ge 2$, this gives $C\sqrt{\ln t/N(c')} \ge \tfrac12 C\sqrt{\ln t/M}$, so $N(c') \le 4M$. Then every child has a bounded count, and by (1) so has $u$, which is a contradiction. $\square$

The root is visited in every iteration. By Lemma 1 and induction on the depth, every position of the game tree is created after finitely many iterations and is visited infinitely often. From the iteration $T_1$ on in which the last node is created, every non-final node has all its children, so line L4 goes down to a final position, lines L5 and L6 do nothing, and the search uses no more random numbers.

**Lemma 2. For every node $u$ other than the root, $Q(u) \to \mathrm{val}_{m(u)}(u)$ as the number of iterations grows. For every non-final node $u$ and every child $c$ with $\mathrm{val}_{p(u)}(c) < \max_{c'} \mathrm{val}_{p(u)}(c')$, $N(c) = O(\log N(u))$.** We use induction on the height of $u$.

*A final position.* Every visit reads the same payoff, so $Q(u)$ equals the payoff to $m(u)$, which is $\mathrm{val}_{m(u)}(u)$.

*A non-final position.* Let $w^* = \max_c \mathrm{val}_{p(u)}(c)$, the value of $u$ to $p(u)$. By the induction hypothesis, $Q(c) \to \mathrm{val}_{m(c)}(c) = \mathrm{val}_{p(u)}(c)$ for every child $c$. If some child is not optimal, let $\delta > 0$ be the gap between $w^*$ and the best value of a non-optimal child, and take an iteration $T \ge T_1$ after which $|Q(c) - \mathrm{val}_{p(u)}(c)| < \delta/4$ for every child. Fix an optimal child $c^*$. If a non-optimal child $c$ is selected after $T$, when the count of $u$ is $t$, then

$$Q(c) + C\sqrt{\ln t / N(c)} \;\ge\; Q(c^*) + C\sqrt{\ln t / N(c^*)} \;\ge\; Q(c^*), \quad\text{so}\quad C\sqrt{\ln t / N(c)} > \delta/2 \text{ and } N(c) < 4C^2 \ln t / \delta^2.$$

So $N(c)$ is at most its count at $T$ plus $4C^2\ln N(u)/\delta^2 + 1$, which is $O(\log N(u))$. By (1),

$$Q(u) = \frac{r_0(u)}{N(u)} + \sum_c \frac{N(c)}{N(u)} \big(1 - Q(c)\big).$$

The first term goes to 0. The weights $N(c)/N(u)$ of the non-optimal children go to 0, the weights of the optimal children add up to a number that goes to 1, and $1 - Q(c) \to 1 - w^*$ for the optimal children. Hence $Q(u) \to 1 - w^* = \mathrm{val}_{1 - p(u)}(u) = \mathrm{val}_{m(u)}(u)$. $\square$

**The returned move.** Apply the second part of Lemma 2 at the root, with $N(\text{root}) = n$. Each non-optimal child has $O(\log n)$ visits. By (1) the optimal children together have $n - 1 - O(\log n)$ visits, so one of them has at least $(n - 1 - O(\log n))/b$, where $b$ is the number of moves at the root. For $n$ large enough this is more than the count of any non-optimal child, so the most visited child, which line L9 returns, is a minimax move. $\blacksquare$

The proof gives no bound on how large $n$ must be. That depends on the gaps $\delta$ at all nodes and on the time $T_1$ to store the whole tree, and it can be very large; see the page on [UCT](/uct/) for rates.
