---
title: The Fisher-Yates shuffle gives each order with probability 1/n!
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The calls of RANDOM are independent, and the call RANDOM$(0, i)$ is uniform on $\{0, \ldots, i\}$. The items may be equal, so we follow positions: let $A_0$ be the input array, and say that the output is the arrangement $\sigma$ when the output holds $A_0[\sigma(0)], A_0[\sigma(1)], \ldots, A_0[\sigma(n-1)]$, that is, the item that started at position $\sigma(p)$ ends at position $p$. Each swap moves items, so $\sigma$ is a well-defined permutation of $\{0, \ldots, n-1\}$ after each step.

**Termination.** The loop of line L1 runs for $i = n-1, n-2, \ldots, 1$, so it makes exactly $\max(n-1, 0)$ iterations. Each iteration makes one call of RANDOM and one swap. So the algorithm stops after exactly $\max(n-1, 0)$ calls, whatever the random values are.

**Theorem.** For each permutation $\tau$ of $\{0, \ldots, n-1\}$, $\Pr[\sigma = \tau] = 1/n!$.

## Proof 1: by a loop invariant

For a step with value $i$, call the positions $i+1, \ldots, n-1$ the done part. We prove this invariant.

> **(I)** Before the iteration for $i$, with $0 \le i \le n - 1$: for each sequence $(x_{i+1}, \ldots, x_{n-1})$ of distinct elements of $\{0, \ldots, n-1\}$, the probability that for each $p$ in $i+1, \ldots, n-1$ the position $p$ holds the item that started at position $x_p$ is $(i+1)!/n!$.

When $i = n - 1$ the done part is empty, the sequence is empty, and the probability is $1 = n!/n!$. So (I) is true before the first iteration. (When $n \le 1$ the loop does not run. Then $1/n! = 1$ and the one arrangement is the identity, so the theorem holds.)

*Maintenance.* Assume (I) before the iteration for $i \ge 1$. Fix distinct $x_i, x_{i+1}, \ldots, x_{n-1}$. Let $E$ be the event that the done part holds the items from $x_{i+1}, \ldots, x_{n-1}$ in order. By (I), $\Pr[E] = (i+1)!/n!$. On $E$, positions $0, \ldots, i$ hold the $i+1$ items from the other $i+1$ starting positions, one at each position, and $x_i$ is one of these starting positions. So exactly one index $j^* \in \{0, \ldots, i\}$ holds the item from $x_i$. Line L3 puts that item at position $i$ if and only if $j = j^*$. The call of line L2 is independent of the earlier calls, and $E$ and $j^*$ depend only on the earlier calls. So
$$\Pr[E \text{ and } j = j^*] = \frac{(i+1)!}{n!} \cdot \frac{1}{i+1} = \frac{i!}{n!}.$$
Line L3 does not change the done part, which is above $i$. So after the iteration, the probability that positions $i, \ldots, n-1$ hold the items from $x_i, \ldots, x_{n-1}$ is $i!/n!$. This is (I) for the next value $i - 1$.

*End.* After the iteration for $i = 1$, (I) holds with $i = 0$: for each sequence $(x_1, \ldots, x_{n-1})$ of distinct positions, the probability is $1!/n! = 1/n!$. Position 0 then holds the item from the one starting position that is not in the sequence. So each arrangement $\tau$ is fixed by $(\tau(1), \ldots, \tau(n-1))$, and $\Pr[\sigma = \tau] = 1/n!$. $\square$

## Proof 2: by a bijection with the choice sequences

Let $j_i$ be the value that line L2 returns in the iteration for $i$. The run is fixed by the choice sequence $c = (j_{n-1}, j_{n-2}, \ldots, j_1)$ with $0 \le j_i \le i$. There are $n \cdot (n-1) \cdots 2 = n!$ choice sequences, and each has probability $\prod_{i=1}^{n-1} \frac{1}{i+1} = 1/n!$, by independence.

Let $t_i$ be the transposition of positions $i$ and $j_i$ (the identity if $j_i = i$). If an array $C$ becomes $C'$ by the swap of positions $i$ and $j$, then $C'[p] = C[t(p)]$ with $t = (i\ j)$. So by induction on the number of swaps, the output is $A_0 \circ \sigma$ with
$$\sigma = t_{n-1} \circ t_{n-2} \circ \cdots \circ t_1 .$$

*The map from $c$ to $\sigma$ is one to one.* We use induction on $n$. For $n \le 1$ there is one sequence and one permutation. Let $n \ge 2$. Each $t_i$ with $i \le n-2$ moves only positions in $\{0, \ldots, n-2\}$, so it fixes $n-1$. Hence
$$\sigma(n-1) = t_{n-1}(n-1) = j_{n-1}.$$
So $\sigma$ determines $j_{n-1}$. Then $t_{n-1}$ is known, and $t_{n-1} \circ \sigma = t_{n-2} \circ \cdots \circ t_1$, because a transposition is its own inverse. This product fixes $n-1$, and on $\{0, \ldots, n-2\}$ it is the permutation of the same algorithm run on $n-1$ positions with the choices $(j_{n-2}, \ldots, j_1)$. By the induction hypothesis these choices are determined. So two different choice sequences give two different permutations.

*Conclusion.* The map is one to one from a set of $n!$ choice sequences to the set of $n!$ permutations. So it is a bijection. Each permutation $\tau$ comes from exactly one choice sequence, and that sequence has probability $1/n!$. So $\Pr[\sigma = \tau] = 1/n!$. $\blacksquare$

**The inside-out form.** In INSIDE-OUT, the step for $i$ takes a uniform order of $S[0 \ldots i-1]$ in $B[0 \ldots i-1]$ and a value $j$ uniform on $\{0, \ldots, i\}$. It puts $S[i]$ at position $j$ and moves the old $B[j]$ to position $i$. Each order of $S[0 \ldots i]$ comes from exactly one pair (order of $S[0 \ldots i-1]$, $j$): $j$ is the position of $S[i]$, and the shorter order is found by moving the item at position $i$ back to position $j$. So each of the $(i+1)!$ orders has probability $\frac{1}{i!} \cdot \frac{1}{i+1} = \frac{1}{(i+1)!}$, and induction on $i$ gives a uniform output.
