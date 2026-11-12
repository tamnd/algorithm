---
title: AIMD reaches the band of efficient loads and converges to the equal share
proves: [correctness]
status: full
---

**The model.** There are $n \ge 1$ users and one resource of capacity $c > 0$. The rates at step $t$ are $x_1(t), \ldots, x_n(t) \ge 0$, and $S(t) = \sum_i x_i(t)$ is the total load. Line L2 computes the feedback $y(t) = 1$ if $S(t) > c$, else $y(t) = 0$. All users get the same $y(t)$. Line L4 runs when $y(t) = 0$ and sets $x_i(t+1) = x_i(t) + a$. Line L5 runs when $y(t) = 1$ and sets $x_i(t+1) = b\,x_i(t)$. The parameters are $a > 0$ and $0 < b < 1$. We call a step with $y(t) = 1$ a *decrease step*, and we write $D(t)$ for the number of decrease steps among the steps $0, 1, \ldots, t-1$.

The rates stay non-negative: line L4 adds a positive number, and line L5 multiplies by a positive number.

**Lemma 1 (differences).** For all users $i$, $j$ and all $t \ge 0$, $x_i(t) - x_j(t) = (x_i(0) - x_j(0))\, b^{D(t)}$.

*Proof.* By induction on $t$. For $t = 0$, $D(0) = 0$ and the claim is trivial. Assume it for $t$. If step $t$ is an increase, both rates grow by $a$, so the difference does not change, and $D(t+1) = D(t)$. If step $t$ is a decrease, both rates are multiplied by $b$, so the difference is multiplied by $b$, and $D(t+1) = D(t) + 1$. $\square$

**Lemma 2 (the band is closed).** Let $I = (bc, c + na]$. If $S(t) \in I$, then $S(t+1) \in I$.

*Proof.* If $S(t) \le c$, step $t$ is an increase, so $S(t+1) = S(t) + na$. Then $S(t+1) > bc + na > bc$ and $S(t+1) \le c + na$. If $S(t) > c$, step $t$ is a decrease, so $S(t+1) = b\,S(t)$. Then $S(t+1) > bc$, and $S(t+1) \le b(c + na) < c + na$. $\square$

**Lemma 3 (the band is reached).** For every start $x(0) \ge 0$ there is a step $t_0$ with $S(t_0) \in I$. One can take $t_0 \le \lfloor (bc - S(0))/(na) \rfloor + 1$ if $S(0) \le bc$, and $t_0 \le \lceil \ln(S(0)/(c + na)) / \ln(1/b) \rceil$ if $S(0) > c + na$.

*Proof.* If $S(0) \in I$, take $t_0 = 0$.

Assume $S(0) \le bc$. As long as $S(t) \le bc < c$, step $t$ is an increase and $S(t+1) = S(t) + na$. So $S(t) = S(0) + t\,na$ while all values stay at most $bc$. Let $t_0$ be the first step with $S(t_0) > bc$. It exists, with the bound in the statement, because the sum grows by the fixed amount $na > 0$ per step. Then $S(t_0 - 1) \le bc$, so $S(t_0) = S(t_0 - 1) + na \le bc + na < c + na$. So $S(t_0) \in I$.

Assume $S(0) > c + na$. As long as $S(t) > c + na > c$, step $t$ is a decrease and $S(t+1) = b\,S(t)$. So $S(t) = b^t S(0)$ while all values stay above $c + na$. Since $0 < b < 1$, $b^t S(0) \le c + na$ as soon as $t \ge \ln(S(0)/(c+na)) / \ln(1/b)$. Let $t_0$ be the first step with $S(t_0) \le c + na$. Then $S(t_0 - 1) > c + na > c$, so $S(t_0) = b\,S(t_0 - 1) > bc$. So $S(t_0) \in I$. $\square$

**Lemma 4 (decreases recur).** Let $m = \lceil (1-b)c / (na) \rceil$. If $S(t) \in I$, then at least one of the steps $t, t+1, \ldots, t+m$ is a decrease step.

*Proof.* Assume that the steps $t, \ldots, t+m$ are all increases. Then $S(t+k) \le c$ for $k = 0, \ldots, m$, and $S(t+m) = S(t) + m\,na$. But $S(t) > bc$ and $m\,na \ge (1-b)c$, so $S(t+m) > bc + (1-b)c = c$. This is a contradiction. $\square$

**Theorem.** Let $x(0) \ge 0$, and let $t_0$ and $m$ be as in Lemmas 3 and 4. Then for all $t \ge t_0$:

1. $bc < S(t) \le c + na$.
2. $|x_i(t) - x_j(t)| \le |x_i(0) - x_j(0)|\, b^{\lfloor (t - t_0)/(m+1) \rfloor}$ for all $i$ and $j$.
3. $|x_i(t) - S(t)/n| \to 0$ for each $i$, and Jain's index $J(t) = S(t)^2 / (n \sum_i x_i(t)^2)$ goes to 1.

*Proof.* Part 1 follows from Lemma 3 and from Lemma 2 by induction on $t$. For part 2, cut the steps $t_0, \ldots, t-1$ into $\lfloor (t - t_0)/(m+1) \rfloor$ disjoint blocks of $m+1$ consecutive steps. By part 1 the load is in $I$ at the start of each block, so by Lemma 4 each block holds a decrease step. Then $D(t) \ge \lfloor (t - t_0)/(m+1) \rfloor$, and Lemma 1 with $0 < b < 1$ gives part 2. For part 3, $x_i - S/n = \frac{1}{n} \sum_j (x_i - x_j)$, so $|x_i - S/n| \le \max_j |x_i - x_j|$, which goes to 0 by part 2. Write $\bar x = S/n$. Then $\sum_i x_i^2 = n \bar x^2 + \sum_i (x_i - \bar x)^2$, so

$$J = \frac{n^2 \bar x^2}{n \left(n \bar x^2 + \sum_i (x_i - \bar x)^2\right)} = \frac{1}{1 + \sum_i (x_i - \bar x)^2 / (n \bar x^2)}.$$

By part 1, $\bar x > bc/n > 0$, and the sum of squares goes to 0, so $J(t) \to 1$. $\blacksquare$

**The other linear controls.** The same induction shows what goes wrong without both parts. With additive decrease, $x_i \leftarrow x_i - a_D$, a decrease step keeps the difference $x_i - x_j$ as long as no rate reaches 0, so additive increase with additive decrease keeps the difference of the rates fixed while all rates stay positive. With multiplicative increase, $x_i \leftarrow b_I x_i$ with $b_I > 1$, an increase step multiplies the difference by $b_I$, so multiplicative increase with multiplicative decrease keeps the ratio $x_i / x_j$ fixed. Chiu and Jain prove the general statement: among the linear controls $x_i \leftarrow a_I + b_I x_i$ on increase and $x_i \leftarrow a_D + b_D x_i$ on decrease, convergence to efficiency and fairness needs $a_I > 0$, $b_I \ge 1$, $a_D = 0$ and $0 \le b_D < 1$.
