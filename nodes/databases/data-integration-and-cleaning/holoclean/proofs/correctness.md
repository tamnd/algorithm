---
title: What the toy HoloClean pipeline computes, and why its Gibbs sampler targets the joint model
proves: [correctness, termination, time.worst]
status: full
---

**Scope.** HoloClean is a heuristic: nothing proves that its repairs are the true values. This file proves what the toy pipeline of the page does compute. The detection step finds exactly the cells of the violating pairs. The probabilities of line L8 are the exact distribution of the learned model in which each noisy cell is inferred with the other cells fixed. Line L6 follows the gradient of a concave objective. The sampler of lines L11 to L16 has the joint model as its stationary distribution, and its frequencies converge to the marginals of that model. Set semantics is not needed here: the table is a list of rows, and two equal rows are two rows.

**Setting.** A table has $n$ rows and $a$ attributes. A cell is a pair $(i, b)$ of a row and an attribute. A denial constraint $\delta$ is a list of at most $p$ predicates $t_1[b] \;\theta\; t_2[b']$, and an ordered pair of different rows $(r, s)$ *violates* $\delta$ if all its predicates hold with $t_1 = r$ and $t_2 = s$. There are $q$ constraints. For each cell $c$ with observed value $o_c$, line L3 gives a finite domain $\text{dom}(c)$, line L5 gives a feature vector $f(c, d)$ for each $d \in \text{dom}(c)$, and the score is $s_w(c, d) = w \cdot f(c, d) + \lambda [d = o_c]$, where $\lambda$ is the prior.

**Lemma 1 (detection).** Line L1 returns the set of cells $(i, b)$ such that, for some constraint $\delta$ that mentions attribute $b$, row $i$ is in some ordered pair of different rows that violates $\delta$.

*Proof.* The loop visits every constraint and every ordered pair $(i, j)$ with $i \ne j$, tests every predicate, and on a violation adds the cells of both rows for every attribute of the constraint. It adds nothing else. $\square$

**Lemma 2 (domains).** For each cell $c$, $o_c \in \text{dom}(c)$, and $\text{dom}(c)$ is a subset of the values that occur in the attribute of $c$. A value $v \ne o_c$ is in $\text{dom}(c)$ exactly when some other cell $(i, b')$ of the row has $\#\{v, u\} \ge \tau \cdot \#\{u\}$, where $u$ is its value, $\#\{u\}$ counts the rows with $u$ in attribute $b'$, and $\#\{v, u\}$ counts those that also have $v$ in the attribute of $c$.

*Proof.* Line L3 starts the domain with $o_c$, ranges $v$ over the values of the attribute, and adds $v$ under the stated test. $\square$

**Lemma 3 (the probabilities of line L8).** Consider the model in which the noisy cells are independent and cell $c$ takes the value $d \in \text{dom}(c)$ with probability proportional to $\exp(s_w(c, d))$. The features $f(c, d)$ depend only on $d$ and on the observed values of the other cells, so this is a well defined product distribution. Line L8 returns, for each noisy cell, its exact marginal in this model, and line L9 returns its most likely value, with ties broken in favour of $o_c$.

*Proof.* In a product distribution, the marginal of $c$ is its own factor, normalized: $P(d) = \exp(s_w(c, d)) / \sum_{d'} \exp(s_w(c, d'))$. This is the softmax of line L8. Subtracting the largest score before taking exponentials multiplies numerator and denominator by one number, so it does not change the result. Line L9 takes the largest probability, and the key $(P(d), [d = o_c])$ prefers $o_c$ among equal ones. The most likely joint assignment of a product distribution is the assignment of the most likely value to each cell. $\square$

**Lemma 4 (learning).** Let $E$ be the set of clean cells with more than one candidate, and $L(w) = \frac{1}{|E|} \sum_{c \in E} \log P_w(o_c \mid c) - \frac{\mu}{2} \|w\|^2$, with $P_w$ the softmax of Lemma 3 and $\mu$ the parameter l2. Each epoch of line L6 adds $\eta \nabla L(w)$ to $w$, and $L$ is strictly concave.

*Proof.* For one cell, $\log P_w(o_c \mid c) = s_w(c, o_c) - \log \sum_d \exp(s_w(c, d))$. Its gradient is $f(c, o_c) - \sum_d P_w(d \mid c) f(c, d) = \sum_d ([d = o_c] - P_w(d \mid c)) f(c, d)$, which is the sum that the code builds, with the label $[d = o_c]$. The gradient of the penalty is $-\mu w$. The function $\log \sum_d \exp(\cdot)$ of an affine map of $w$ is convex, so each log-likelihood term is concave, and the penalty with $\mu > 0$ makes $L$ strictly concave. $\square$

A fixed number of steps with a fixed rate need not reach the maximum of $L$. The proof claims only the direction of each step.

**The joint model.** For a set $N$ of noisy cells with domains and scores $\phi(c, d)$, and pair factors $(\delta, i, j, \beta)$ with $\beta \ge 0$, let

$$\pi(x) \propto \exp\Big(\sum_{c \in N} \phi(c, x_c) - \sum_{(\delta, i, j, \beta)} \beta \cdot [\text{rows } i, j \text{ of } x \text{ violate } \delta \text{ in some order}]\Big)$$

over the assignments $x$ of the noisy cells, where the other cells keep their observed values. The function log_weight computes the exponent.

**Lemma 5 (one Gibbs step).** For a cell $c = (i, b)$, line L14 draws $x_c$ from $\pi(x_c \mid x_{-c})$, the conditional of $\pi$ given the current values of the other noisy cells.

*Proof.* As a function of $x_c$ alone, the exponent of $\pi$ changes only in $\phi(c, x_c)$ and in the factors whose rows include $i$, since a factor on rows $j, j'$ with $i \notin \{j, j'\}$ reads no value of row $i$. The code scores each $d$ by $\phi(c, d)$ minus the weights of exactly these factors that are violated with $x_c = d$, and samples from the softmax of the scores by inverting the cumulative sum with a uniform number. The terms it leaves out are the same for every $d$, so they cancel in the normalization. $\square$

**Theorem.** The pipeline of lines L1 to L10 stops, and it returns the noisy cells of Lemma 1, the exact marginals of Lemma 3 for the learned weights, and the most likely value of each noisy cell in that model. The sampler of lines L11 to L16 stops after the given number of sweeps. If all factor weights are finite, then as the number of sweeps grows, the frequency of each value $d$ of each cell $c$ converges with probability 1 to the marginal $\pi(x_c = d)$.

*Proof.* Every loop of the pipeline is over finite sets, and line L6 runs a fixed number of epochs. The returned values are those of Lemmas 1 and 3.

For the sampler, let $K_c$ be the kernel of the step at cell $c$. By Lemma 5, $K_c$ resamples $x_c$ from $\pi(x_c \mid x_{-c})$, so $\sum_x \pi(x) K_c(x, y) = \pi(y)$: the step keeps $\pi$. A sweep applies the kernels in a fixed order, so the sweep kernel $K$ also keeps $\pi$. With finite weights, every assignment has $\pi(x) > 0$, so every conditional is positive on the whole domain. Then $K(x, y) > 0$ for all $x, y$, since one sweep can set each cell to its value in $y$. So the chain on the finite state space is irreducible and aperiodic, and by the ergodic theorem for finite Markov chains, the fraction of sweeps after which $x_c = d$ converges to $\pi(x_c = d)$ with probability 1. Counting cell $c$ right after its own update, rather than at the end of the sweep, looks at the same chain shifted within the sweep, whose kernel is a cyclic reordering of the same steps and also keeps $\pi$ with positive entries. The burn-in removes finitely many terms, which does not change the limit. $\blacksquare$

The theorem gives no rate. When some $\beta$ is large, $K(x, y)$ is positive but tiny for $y$ far from $x$, and the chain can stay near one mode for longer than any practical run. The test of the page shows this with $\beta = 20$.

**Running time.** Let $n$ be the number of rows, $a$ the number of attributes, $v$ the largest number of distinct values in an attribute, $q$ the number of constraints, $p$ the largest number of predicates in one, and $e$ the number of epochs. Line L1 costs $O(q n^2 p)$. The counts cost $O(n a^2)$. Line L3 costs $O(a v)$ dictionary lookups per cell, so $O(n a^2 v)$. Line L5 builds $O(a)$ statistics and at most $q$ relaxed counts of $O(n p)$ each, for at most $n a v$ pairs of a cell and a value, so $O(n a v (a + q n p))$. One epoch of line L6 touches each feature of each candidate of each example, so $O(n a v (a + q))$, and line L8 costs the same once. The total is $O(n^2 a v q p + e\, n a v (a + q))$ time and $O(n a (a + v (a + q)))$ space. One sweep of the sampler costs $O(|N| v F p)$, where $F$ is the largest number of factors that touch one row.
