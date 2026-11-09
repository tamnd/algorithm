---
title: Heap's algorithm visits every permutation once, with one exchange per step
proves: [correctness]
status: full
---

We describe a rearrangement of the prefix $A[0 \ldots k-1]$ by a permutation $f$ of the positions $\{0, \ldots, k-1\}$: the item at position $p$ moves to position $f(p)$. We write $(p\ q)$ for the exchange of positions $p$ and $q$, and $(p_1\ p_2\ \cdots\ p_m)$ for the cycle that moves the item at $p_1$ to $p_2$, the item at $p_2$ to $p_3$, and so on, and the item at $p_m$ to $p_1$. For two rearrangements, $g \circ f$ means "first $f$, then $g$". Let $E_k$ be the net rearrangement of the prefix made by one call HEAP$(A, k)$.

**Theorem.** For each $k \ge 1$:

1. HEAP$(A, k)$ changes only $A[0 \ldots k-1]$. It makes $k!$ visits, and the arrangements of the prefix at these visits are the $k!$ arrangements of its starting items by position, each once.
2. Between two consecutive visits of the call it makes exactly one exchange of two distinct positions. It makes no change before its first visit and none after its last visit.
3. If $k$ is odd, $E_k = (0\ \ k-1)$, which is the identity for $k = 1$. If $k$ is even, $E_k$ is a cycle of length $k$ on $\{0, \ldots, k-1\}$; for $k \ge 4$ it is $E_k = (0\ \ k-1\ \ k-2\ \ 1\ \ 2\ \cdots\ k-3)$, and $E_2 = (0\ 1)$.

*Proof.* By induction on $k$. For $k = 1$, lines L1 to L3 make one visit and no change, so all three parts hold.

Let $k \ge 2$ and assume the theorem for $k - 1$. The call makes $k$ *rounds*: round 0 is the call of line L4, and round $r$ for $1 \le r \le k-1$ is the call of line L8 in the pass $i = r - 1$ of the loop, just after the exchange of line L6 or L7. Let $S_r$ be the prefix at the start of round $r$. A round changes only $A[0 \ldots k-2]$, by part 1 for $k - 1$, so the item at position $k - 1$ is fixed during the round. Let $z_r$ be this item.

*Claim.* The items $z_0, \ldots, z_{k-1}$ are the $k$ items of the starting prefix, each once.

Given the claim, part 1 follows. In round $r$, part 1 for $k - 1$ gives the $(k-1)!$ arrangements of the other $k - 1$ items at positions $0, \ldots, k-2$, each once, with $z_r$ at position $k - 1$. Each arrangement of the prefix has one item at position $k - 1$, which is some $z_r$, and so it occurs in round $r$ and in no other round. The total is $k \cdot (k-1)! = k!$ visits. Part 2 follows from part 2 for $k - 1$: inside a round there is one exchange between consecutive visits. Between the last visit of round $r$ and the first visit of round $r + 1$, the only change is the exchange of line L6 or L7. Its two positions are distinct, since $i \le k-2 < k-1$ and $0 < k-1$. The call begins with round 0 and ends with round $k - 1$, so it makes no change before its first visit or after its last one.

It remains to prove the claim and part 3. Let $x_0, \ldots, x_{k-1}$ be the starting prefix.

**Case $k$ even.** Then $k - 1$ is odd, so by part 3 for $k - 1$ each round makes the exchange $(0\ \ k-2)$. Line L6 in the pass $i = r - 1$ makes the exchange $(r-1\ \ k-1)$. So $S_{r+1} = (r\ \ k-1) \circ (0\ \ k-2)\, (S_r)$ for $0 \le r \le k-2$, and the final prefix is $(0\ \ k-2)\,(S_{k-1})$.

For $k = 2$: $S_0 = x_0 x_1$ and $(0\ 0)$ does nothing, so $S_1 = x_1 x_0$. Then $z_0 = x_1$ and $z_1 = x_0$, and $E_2 = (0\ 1)$.

For $k \ge 4$ we track the prefix. $S_0 = x_0 x_1 \cdots x_{k-1}$, so $z_0 = x_{k-1}$. Round 0 exchanges positions 0 and $k - 2$, and line L6 with $i = 0$ exchanges positions 0 and $k - 1$, so

$$S_1 = x_{k-1}\ x_1\ x_2 \cdots x_{k-3}\ x_0\ x_{k-2}, \qquad z_1 = x_{k-2}.$$

Round 1 exchanges positions 0 and $k - 2$, and $i = 1$ exchanges positions 1 and $k - 1$, so

$$S_2 = x_0\ x_{k-2}\ x_2\ x_3 \cdots x_{k-3}\ x_{k-1}\ x_1, \qquad z_2 = x_1.$$

We show by induction on $r$, for $2 \le r \le k-2$, that $S_r$ is as follows: position 1 holds $x_{k-2}$; positions $2, \ldots, r-1$ hold $x_1, \ldots, x_{r-2}$; positions $r, \ldots, k-3$ hold $x_r, \ldots, x_{k-3}$; position $k - 1$ holds $x_{r-1}$; and positions 0 and $k - 2$ hold $x_0$ and $x_{k-1}$, with $x_0$ at position 0 when $r$ is even and $x_{k-1}$ at position 0 when $r$ is odd. For $r = 2$ this is the line above. For a step from $r$ to $r + 1$ with $r \le k - 3$: the round exchanges positions 0 and $k - 2$, which swaps $x_0$ and $x_{k-1}$ and so flips the rule for position 0. Then line L6 with $i = r$ exchanges positions $r$ and $k - 1$. Position $r$ holds $x_r$, because $r \le k-3$, and position $k - 1$ holds $x_{r-1}$. After the exchange, positions $2, \ldots, r$ hold $x_1, \ldots, x_{r-1}$, positions $r + 1, \ldots, k-3$ hold $x_{r+1}, \ldots, x_{k-3}$, and position $k - 1$ holds $x_r$. This is the statement for $r + 1$.

So $z_r = x_{r-1}$ for $2 \le r \le k-2$. In $S_{k-2}$, the index $k - 2$ is even, so position 0 holds $x_0$ and position $k - 2$ holds $x_{k-1}$, and position $k-1$ holds $x_{k-3}$. Round $k - 2$ swaps positions 0 and $k - 2$, and line L6 with $i = k - 2$ exchanges positions $k - 2$ and $k - 1$. This gives

$$S_{k-1} = x_{k-1}\ x_{k-2}\ x_1\ x_2 \cdots x_{k-4}\ x_{k-3}\ x_0, \qquad z_{k-1} = x_0.$$

In these displays a run such as $x_1\ x_2 \cdots x_{k-4}$ is empty when its last index is below its first, as for $k = 4$, where $S_{k-1} = x_3\ x_2\ x_1\ x_0$. The items at the end are $z_0, \ldots, z_{k-1} = x_{k-1}, x_{k-2}, x_1, x_2, \ldots, x_{k-3}, x_0$. These are all $k$ items, each once, which proves the claim. The last round swaps positions 0 and $k - 2$ of $S_{k-1}$, so the final prefix is

$$x_{k-3}\ x_{k-2}\ x_1\ x_2 \cdots x_{k-4}\ x_{k-1}\ x_0.$$

Read by positions: the item from position 0 is now at $k - 1$, the item from $k - 1$ is at $k - 2$, the item from $k - 2$ is at 1, the item from $p$ is at $p + 1$ for $1 \le p \le k-4$, and the item from $k - 3$ is at 0. So $E_k = (0\ \ k-1\ \ k-2\ \ 1\ \ 2\ \cdots\ k-3)$, one cycle through all $k$ positions. For $k = 4$ this is $(0\ 3\ 2\ 1)$.

**Case $k$ odd, $k \ge 3$.** Then $k - 1$ is even, and by part 3 for $k - 1$, $E_{k-1} = (c_0\ c_1\ \cdots\ c_{k-2})$ is a cycle through all of $\{0, \ldots, k-2\}$. Write it with $c_0 = 0$. Each pass of the loop exchanges positions 0 and $k - 1$, by line L7. Let $T = (0\ \ k-1) \circ E_{k-1}$, a rearrangement of $\{0, \ldots, k-1\}$, so that $S_{r+1} = T(S_r)$ for $0 \le r \le k - 2$.

We compute $T$. For $p = c_t$ with $0 \le t \le k-3$, $E_{k-1}$ sends $p$ to $c_{t+1} \ne 0$, and the exchange does not move it, so $T(c_t) = c_{t+1}$. $E_{k-1}$ sends $c_{k-2}$ to $c_0 = 0$, and the exchange sends 0 to $k - 1$, so $T(c_{k-2}) = k - 1$. $E_{k-1}$ fixes $k - 1$, and the exchange sends it to 0, so $T(k-1) = 0 = c_0$. Hence

$$T = (c_0\ c_1\ \cdots\ c_{k-2}\ \ k-1),$$

a single cycle of length $k$. The item at position $k - 1$ in $S_r = T^r(S_0)$ is the item that started at position $T^{-r}(k-1)$. For $r = 0, 1, \ldots, k-1$ the positions $T^{-r}(k-1)$ walk once around the cycle of $T$ backwards, so they are the $k$ distinct positions. This proves the claim.

The net effect of the call is the round 0, then $k - 1$ times the exchange and a round. As a rearrangement,

$$E_k = E_{k-1} \circ \big( (0\ \ k-1) \circ E_{k-1} \big)^{k-1} = E_{k-1} \circ T^{k-1}.$$

$T$ is a cycle of length $k$, so $T^k$ is the identity and $T^{k-1} = T^{-1} = E_{k-1}^{-1} \circ (0\ \ k-1)$. So $E_k = E_{k-1} \circ E_{k-1}^{-1} \circ (0\ \ k-1) = (0\ \ k-1)$. This proves part 3 for odd $k$, and completes the induction. $\blacksquare$

**Corollary.** HEAP$(A, n)$ visits each of the $n!$ arrangements of $A[0 \ldots n-1]$ once, with $n! - 1$ exchanges, one between each two consecutive visits. For odd $n$ and for $n = 2$, the last arrangement is the first one with positions 0 and $n - 1$ exchanged.

*Proof.* Parts 1 and 2 with $k = n$ give the first sentence. The last visit happens after all changes, so the last arrangement is $E_n$ applied to the first one, and part 3 gives the second sentence. $\blacksquare$

**The iterative form.** HEAP-ITERATIVE simulates the recursion. The counter $c[k]$ is the number of passes that the loop of line L5 at level $k + 1$ has done, and the index $k$ of the while loop is the lowest level whose loop is not finished. When $c[k] < k$, lines I6 to I9 make the next exchange of level $k + 1$, then descend to level 2 by setting $k$ to 1; the descent visits at once, because the inner calls of levels $k$ down to 2 start with their round 0, which reaches a visit without any exchange. When $c[k] = k$, the loop of level $k + 1$ is done, line I11 resets its counter for its next call and moves up one level. So both forms make the same exchanges in the same order and visit at the same moments.
