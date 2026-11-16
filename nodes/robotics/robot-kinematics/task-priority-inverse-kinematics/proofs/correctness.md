---
title: The priority step solves the lexicographic least squares problem with the least norm, and its fixed points meet the first task
proves: [correctness]
status: full
---

We use the notation of the page, in exact arithmetic.
For a matrix $A$, $A^{+}$ is the Moore-Penrose pseudoinverse.
We use three standard facts about it: $A^{+}A$ is the orthogonal projector onto $\operatorname{range}(A^{\mathsf T})$, the range of $A^{+}$ is $\operatorname{range}(A^{\mathsf T})$, and the minimizers of $|Az - r|$ are exactly $z = A^{+}r + w$ with $w \in \operatorname{null}(A)$, among which $A^{+}r$ has the least norm.

Define the sets of kept steps by $S_0 = \mathbb R^n$ and $S_i = \arg\min_{x \in S_{i-1}}|J_ix - e_i|$.
Let $N_i = \bigcap_{j \le i}\operatorname{null}(J_j)$, with $N_0 = \mathbb R^n$.
Write $\Delta\theta_i$ and $P_i$ for the values of $\Delta\theta$ and $P$ after level $i$ of the loop, with $\Delta\theta_0 = 0$ and $P_0 = I$.

**Claim.** For every $i = 0, \ldots, p$:

1. $P_i$ is the orthogonal projector onto $N_i$;
2. $S_i = \Delta\theta_i + N_i$;
3. $\Delta\theta_i$ is orthogonal to $N_i$, so it is the element of least norm of $S_i$.

*Proof.*
By induction on $i$.
For $i = 0$ all three hold, since $P_0 = I$, $S_0 = \mathbb R^n = 0 + N_0$ and $\Delta\theta_0 = 0$.

Assume the claim for $i - 1$, and write $P = P_{i-1}$, $A = J_iP$ and $r = e_i - J_i\Delta\theta_{i-1}$, as in lines L3 to L5.
Since $P$ is the orthogonal projector onto $N_{i-1}$, every $x \in S_{i-1}$ is $x = \Delta\theta_{i-1} + Pz$ for some $z \in \mathbb R^n$, and then $J_ix - e_i = Az - r$.
So $S_i = \{\Delta\theta_{i-1} + Pz : z \text{ minimizes } |Az - r|\} = \{\Delta\theta_{i-1} + PA^{+}r + Pw : w \in \operatorname{null}(A)\}$.

*The range of $A^{+}$ is in the range of $P$.*
$\operatorname{range}(A^{+}) = \operatorname{range}(A^{\mathsf T}) = \operatorname{range}(PJ_i^{\mathsf T}) \subseteq \operatorname{range}(P)$, using $P^{\mathsf T} = P$.
So $PA^{+} = A^{+}$, and the first part of the set is $\Delta\theta_{i-1} + A^{+}r = \Delta\theta_i$, the value of line L6.

*The free part.*
$\{Pw : w \in \operatorname{null}(A)\}$ is the set $N_{i-1} \cap \operatorname{null}(J_i) = N_i$.
Indeed, if $Aw = 0$, then $v = Pw \in N_{i-1}$ and $J_iv = J_iPw = Aw = 0$; conversely, if $v \in N_i$, then $Pv = v$ and $Av = J_iv = 0$, so $v = Pv$ with $v \in \operatorname{null}(A)$.
This proves part 2.

*The projector.*
$Q = A^{+}A$ is the orthogonal projector onto $\operatorname{range}(A^{\mathsf T}) \subseteq \operatorname{range}(P)$, so $PQ = Q$, and taking transposes, $QP = Q$.
Then $P - Q$ is symmetric and $(P - Q)^2 = P - PQ - QP + Q = P - Q$, so $P - Q$ is an orthogonal projector.
Its range is $\operatorname{range}(P) \cap \operatorname{range}(Q)^{\perp} = N_{i-1} \cap \operatorname{null}(A)$, and the last paragraph shows that this is $N_i$.
So $P_i = P - Q$, the value of line L7, is the orthogonal projector onto $N_i$, which is part 1.

*Least norm.*
$\Delta\theta_{i-1}$ is orthogonal to $N_{i-1} \supseteq N_i$ by the induction hypothesis.
$A^{+}r$ is in $\operatorname{range}(A^{\mathsf T})$, which is orthogonal to $\operatorname{null}(A) \supseteq N_i$.
So $\Delta\theta_i$ is orthogonal to $N_i$, and for every $v \in N_i$, $|\Delta\theta_i + v|^2 = |\Delta\theta_i|^2 + |v|^2$.
This is part 3.
$\square$

So the output $\Delta\theta_p$ is the step of least norm that solves the lexicographic least squares problem of the page.

## Consequences

**Strict priority.** $S_p \subseteq S_j$ for every $j$, and two elements of $S_j$ differ by an element of $N_j$, which no task $1, \ldots, j$ sees.
So $J_l\Delta\theta_p = J_l\Delta\theta_j$ for all $l \le j$: the levels below $j$ do not change what the levels up to $j$ achieve.

**The first task.** If $J_1$ has full row rank, the minimum of $|J_1x - e_1|$ is 0, so $J_1\Delta\theta_p = e_1$.

**Two levels.** With $P_1 = I - J_1^{+}J_1$, the loop gives $\Delta\theta_2 = J_1^{+}e_1 + (J_2P_1)^{+}(e_2 - J_2J_1^{+}e_1)$, the formula of Nakamura, Hanafusa and Yoshikawa.

## Fixed points of the iteration

Let the iteration stop with $\Delta\theta_p = 0$ at a configuration $\bar\theta$ with $J_1(\bar\theta)$ of full row rank.

- By part 3, $\Delta\theta_1 = J_1^{+}e_1$ is orthogonal to $N_1$, and every later increment $A^{+}r$ lies in $N_1$ (its range is in the range of $P_{i-1} \subseteq$ the range of $P_1$).
So $\Delta\theta_p = 0$ forces $J_1^{+}e_1 = 0$.
Since $J_1$ has full row rank, $J_1^{+}$ is injective, and $e_1 = 0$.
- Then $\Delta\theta_1 = 0$, $r = e_2$ at level 2, and the increment of level 2 is $(J_2P_1)^{+}e_2$.
It is orthogonal to $N_2$ while the later increments lie in $N_2$, so it is zero too.
Since $\operatorname{null}(A^{+}) = \operatorname{null}(A^{\mathsf T})$, this means $P_1J_2^{\mathsf T}e_2 = 0$.
As $-J_2^{\mathsf T}e_2$ is the gradient of $\tfrac12|e_2|^2$, its projection onto the motions that keep the first task to first order is zero.

So a fixed point meets the first task exactly and is a stationary point of the second task error on the set where the first task holds.
Nothing more is claimed: the iteration need not converge, and a stationary point need not be the best one.
