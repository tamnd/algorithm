---
title: The affinity propagation messages are the max-sum messages of the exemplar factor graph
proves: [correctness]
status: full
---

We use the pseudocode of the page. We show three things: the messages of lines L3 and L5 are the max-sum messages on a factor graph whose best assignment is the best valid clustering (Theorem 1), a damped fixed point solves the undamped equations (Lemma 3), and the output of line L10 is always a valid clustering (Lemma 4). We do not claim convergence or optimality; the page gives a converged run that is not optimal. The factor graph follows Givoni and Frey (2009).

**The factor graph.** For each ordered pair $(i, k)$, including $i = k$, there is a binary variable $c_{ik}$, meaning "$i$ chooses $k$ as its exemplar". The factors are:

- $S_{ik}(c_{ik}) = s(i, k)\, c_{ik}$ for each pair;
- $I_i(c_{i1}, \ldots, c_{in}) = 0$ if $\sum_k c_{ik} = 1$, else $-\infty$ (each point chooses exactly one exemplar);
- $E_k(c_{1k}, \ldots, c_{nk}) = -\infty$ if $c_{kk} = 0$ and $c_{ik} = 1$ for some $i \ne k$, else 0 (a point chosen by others chooses itself).

Let $F(c)$ be the sum of all factors.

**Lemma 1.** $F(c) > -\infty$ if and only if $c$ encodes a valid clustering, that is, a map $i \mapsto c(i)$ with $c(c(i)) = c(i)$. Then $F(c) = \sum_i s(i, c(i))$, the net similarity.

*Proof.* The factors $I_i$ are finite exactly when each $i$ has one chosen $k$; call it $c(i)$. The factors $E_k$ are finite exactly when each $k$ chosen by some $i \ne k$ has $c(k) = k$, which is validity. The factors $S_{ik}$ then add $s(i, c(i))$ for each $i$. $\square$

So the best valid clustering is the maximizer of $F$, a MAP problem for the max-sum algorithm.

**Max-sum.** A message from a variable $x$ to a factor $f$ is the sum of the messages that $x$ gets from its other factors. A message from a factor $f$ to a variable $x$ is, for each value of $x$, the maximum over the other variables of $f$ of $f$ plus their messages to $f$. Adding a constant to a message does not change any maximizer, so for a binary variable only the difference "value at 1 minus value at 0" matters. We write each message as this difference and fix the value at 0 to 0. The messages that we need are:

- $\rho_{ik}$: from $c_{ik}$ to $E_k$;
- $\alpha_{ik}$: from $E_k$ to $c_{ik}$;
- $\beta_{ik}$: from $c_{ik}$ to $I_i$;
- $\eta_{ik}$: from $I_i$ to $c_{ik}$.

The variable $c_{ik}$ has three factors, $S_{ik}$, $I_i$ and $E_k$, and $S_{ik}$ sends the difference $s(i, k)$. So $\beta_{ik} = s(i, k) + \alpha_{ik}$ and $\rho_{ik} = s(i, k) + \eta_{ik}$.

**Lemma 2 (the factor messages).** For all $i, k$,

$$\eta_{ik} = -\max_{k' \ne k} \beta_{ik'}, \qquad \alpha_{ik} = \min\Bigl(0,\; \rho_{kk} + \sum_{i' \notin \{i, k\}} \max(0, \rho_{i'k})\Bigr) \ (i \ne k), \qquad \alpha_{kk} = \sum_{i' \ne k} \max(0, \rho_{i'k}).$$

*Proof.* *The message $\eta_{ik}$.* The incoming messages to $I_i$ from $c_{ik'}$ have the value 0 at 0 and $\beta_{ik'}$ at 1. If $c_{ik} = 1$, the constraint forces $c_{ik'} = 0$ for all $k' \ne k$, and the maximum is 0. If $c_{ik} = 0$, exactly one $k' \ne k$ has $c_{ik'} = 1$, and the maximum is $\max_{k' \ne k} \beta_{ik'}$. The difference is $\eta_{ik} = -\max_{k' \ne k} \beta_{ik'}$.

*The message $\alpha_{ik}$ for $i \ne k$.* The incoming messages to $E_k$ from $c_{i'k}$ have the value $\rho_{i'k}$ at 1. If $c_{ik} = 1$, the constraint forces $c_{kk} = 1$, and the other $c_{i'k}$ ($i' \notin \{i, k\}$) are free; each is set to 1 if and only if $\rho_{i'k} > 0$. The maximum is $v = \rho_{kk} + \sum_{i' \notin \{i, k\}} \max(0, \rho_{i'k})$. If $c_{ik} = 0$, either $c_{kk} = 1$, with the same best value $v$, or $c_{kk} = 0$, which forces all $c_{i'k} = 0$ and gives 0. The maximum is $\max(0, v)$. The difference is $v - \max(0, v) = \min(0, v)$.

*The message $\alpha_{kk}$.* If $c_{kk} = 1$, all other $c_{i'k}$ are free, and the maximum is $\sum_{i' \ne k} \max(0, \rho_{i'k})$. If $c_{kk} = 0$, all other $c_{i'k}$ must be 0, and the maximum is 0. $\square$

**Theorem 1.** Put $r(i, k) = \rho_{ik}$ and $a(i, k) = \alpha_{ik}$. Then the max-sum updates, in the schedule "all $\rho$ from the current $\alpha$, then all $\alpha$ from the new $\rho$", are lines L3 and L5 of the page without damping. The max-sum belief of $c_{ik}$ (the difference of its max-marginal between 1 and 0) is $a(i, k) + r(i, k)$, and line L7 takes as exemplars the $k$ whose belief for $c_{kk} = 1$ is positive.

*Proof.* By Lemma 2 and $\beta_{ik'} = s(i, k') + \alpha_{ik'}$,

$$\rho_{ik} = s(i, k) + \eta_{ik} = s(i, k) - \max_{k' \ne k} \bigl( s(i, k') + \alpha_{ik'} \bigr),$$

which is line L3 with $a = \alpha$. The formulas for $\alpha$ in Lemma 2 are line L5 with $r = \rho$. The belief of $c_{ik}$ is the sum of the three factor messages into it: $s(i, k) + \eta_{ik} + \alpha_{ik} = \rho_{ik} + \alpha_{ik} = r(i, k) + a(i, k)$. $\square$

On a factor graph that is a tree, max-sum gives the exact max-marginals, and the MAP assignment follows. This graph has cycles (for example $c_{ik}$, $I_i$, $c_{ii}$, $E_i$, $c_{ki}$, $I_k$, $c_{kk}$, $E_k$, back to $c_{ik}$), so these guarantees do not hold: the messages may not converge, and a fixed point may decode to a clustering that is not optimal. This is the [loopy belief propagation](/loopy-belief-propagation/) setting.

**Lemma 3 (damped fixed points).** Let line L4 be $r \leftarrow \lambda r + (1 - \lambda) R(a)$ and line L6 be $a \leftarrow \lambda a + (1 - \lambda) A(r)$, with $0 \le \lambda < 1$, where $R$ and $A$ are the maps of lines L3 and L5. If one full round leaves $(r, a)$ unchanged, then $r = R(a)$ and $a = A(r)$.

*Proof.* The round leaves $r$ unchanged, so $r = \lambda r + (1 - \lambda) R(a)$, that is, $(1 - \lambda)(r - R(a)) = 0$, and $1 - \lambda > 0$ gives $r = R(a)$. Line L5 then uses this same $r$, and the same argument gives $a = A(r)$. $\square$

So damping changes the path of the messages, not the set of fixed points. The implementation tests that the converged messages satisfy $r = R(a)$ and $a = A(r)$ up to rounding.

**Lemma 4 (valid output).** If $E \ne \emptyset$, the map $c$ of line L10 is a valid clustering, and each cluster contains its exemplar.

*Proof.* For $k \in E$, $c(k) = k$. For $i \notin E$, $c(i) \in E$, so $c(c(i)) = c(i)$. Each $k \in E$ is in its own cluster. $\square$

**Signs.** By Lemma 2, $a(i, k) \le 0$ for $i \ne k$ and $a(k, k) \ge 0$. Damping keeps these signs, since a convex combination of numbers of one sign has that sign. So $a(k, k) + r(k, k) > 0$ in line L7 needs $r(k, k) > -a(k, k)$: the self-responsibility must beat the support from the other points.
