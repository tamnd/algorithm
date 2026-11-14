---
title: Path-count sampling on a BDD is exactly uniform, its weighted form is exact, and rejection sampling is exact with 2^n/#models expected tries
proves: [correctness]
status: full
---

**Setting.** $B$ is a reduced ordered BDD over the variables $x_0, \ldots, x_{n-1}$ in this order. Each nonterminal node $u$ has a level $\ell(u) \in \{0, \ldots, n-1\}$, the index of its variable, and children $\mathrm{lo}(u)$ and $\mathrm{hi}(u)$ with $\ell(\mathrm{lo}(u)) > \ell(u)$ and $\ell(\mathrm{hi}(u)) > \ell(u)$. The terminals $0$ and $1$ have level $n$. Node $u$ represents a function $f_u$ that depends only on the variables at levels $\ell(u), \ldots, n-1$, with $f_u = \bar x_{\ell(u)} f_{\mathrm{lo}(u)} + x_{\ell(u)} f_{\mathrm{hi}(u)}$. The constraint is $C = f_{\mathrm{root}}$ and $\#C$ is its number of models among the $2^n$ assignments. The *gap* of an edge from $u$ to a child $v$ is $g(u, v) = \ell(v) - \ell(u) - 1$, the number of variables that the edge skips. We assume that each call `randrange(m)` returns each of $0, \ldots, m-1$ with probability exactly $1/m$, independently of all other calls; for a pseudo-random generator this is a modeling assumption.

$N$ is computed at line L1 by $N(0) = 0$, $N(1) = 1$ and

$$ N(u) = 2^{g(u, \mathrm{lo})} N(\mathrm{lo}(u)) + 2^{g(u, \mathrm{hi})} N(\mathrm{hi}(u)). $$

**Lemma 1 (counts).** For every node $u$, $N(u)$ is the number of assignments of $x_{\ell(u)}, \ldots, x_{n-1}$ that satisfy $f_u$. Hence $\#C = 2^{\ell(\mathrm{root})} N(\mathrm{root})$.

*Proof.* Induction on $n - \ell(u)$. For the terminals the set of variables is empty and the count is 0 for the constant 0 and 1 for the constant 1. For a nonterminal $u$ at level $i$, split the satisfying assignments by the value of $x_i$. Those with $x_i = 1$ satisfy $f_{\mathrm{hi}(u)}$, which does not depend on the $g(u, \mathrm{hi})$ variables at levels $i+1, \ldots, \ell(\mathrm{hi}(u)) - 1$; these are free, and the remaining variables give $N(\mathrm{hi}(u))$ choices by the induction hypothesis. So there are $2^{g(u, \mathrm{hi})} N(\mathrm{hi}(u))$ of them. The case $x_i = 0$ is the same with $\mathrm{lo}$. For the root, the $\ell(\mathrm{root})$ variables above it are free. $\square$

The [counting page](/bdd-satisfy-count/) states the same recurrence. In particular $N(u) > 0$ for every nonterminal $u$ of a reduced BDD with $f_u \ne 0$, and $N(u) = 0$ only for the terminal 0.

**Lemma 2 (the walk ends at 1).** If $N(\mathrm{root}) > 0$, every run of lines L3 to L10 ends at the terminal 1, and the returned $x$ satisfies $C$.

*Proof.* At a node $u$ with $N(u) > 0$, line L7 moves to $\mathrm{hi}(u)$ with probability $c_1 / N(u)$ and to $\mathrm{lo}(u)$ with probability $c_0 / N(u)$, where $c_1 = 2^{g(u, \mathrm{hi})} N(\mathrm{hi}(u))$ and $c_0 = N(u) - c_1 = 2^{g(u, \mathrm{lo})} N(\mathrm{lo}(u))$ by the recurrence. A child $v$ with $N(v) = 0$ has branch probability 0, so the walk only visits nodes with $N > 0$, and it never reaches the terminal 0. The level grows at each step, so the walk stops after at most $n$ steps, at the terminal 1. The values of $x$ at the levels of the visited nodes are the branches taken, so evaluating $C$ at $x$ follows the same path and gives 1. $\square$

**Theorem 1 (exact uniformity).** If $\#C > 0$, the sampler returns every model $s$ of $C$ with probability exactly $1/\#C$ and returns no other assignment. If $\#C = 0$, it returns "no solution".

*Proof.* The last sentence is line L2. Let $s$ be a model, and let $\mathrm{root} = u_0, u_1, \ldots, u_k = 1$ be the path that $s$ selects in $B$: $u_{j+1} = \mathrm{hi}(u_j)$ if $s_{\ell(u_j)} = 1$ and $\mathrm{lo}(u_j)$ otherwise. It ends at 1 because $s$ is a model, so each $N(u_j) > 0$ by Lemma 1. The sampler returns $s$ exactly when the following independent events all happen.

- Line L3 draws $s_i$ for each $i < \ell(\mathrm{root})$: probability $2^{-\ell(\mathrm{root})}$.
- For each $j < k$, line L7 takes the branch to $u_{j+1}$: probability $2^{g(u_j, u_{j+1})} N(u_{j+1}) / N(u_j)$, because $r$ is uniform on $\{0, \ldots, N(u_j) - 1\}$ and the branch is decided by $r < c_1$.
- For each $j < k$, line L8 draws $s_i$ at the $g(u_j, u_{j+1})$ skipped levels: probability $2^{-g(u_j, u_{j+1})}$.

Different runs that return $s$ must take this path, since the path is fixed by the values at the visited levels. Multiplying, the powers of 2 of the last two items cancel, and the product telescopes:

$$ \Pr[\text{output} = s] = 2^{-\ell(\mathrm{root})} \prod_{j=0}^{k-1} \frac{N(u_{j+1})}{N(u_j)} = \frac{2^{-\ell(\mathrm{root})} N(1)}{N(\mathrm{root})} = \frac{1}{2^{\ell(\mathrm{root})} N(\mathrm{root})} = \frac{1}{\#C}, $$

by Lemma 1. Every output is a model by Lemma 2, and the $\#C$ models have total probability 1, so no other assignment has positive probability. $\blacksquare$

The don't-care variables enter in two places, both handled: the variables above the root (line L3), and the variables skipped by an edge (line L8). Each is filled by a fair bit, and the factor $2^{g}$ in the recurrence weighs the branch by the number of completions of the skipped variables. Without that factor, a branch that skips many variables would be chosen too rarely.

**Theorem 2 (weighted generation).** Let $p_0, \ldots, p_{n-1} \in (0, 1)$ be biases, let $b_i(1) = p_i$ and $b_i(0) = 1 - p_i$, and let $w(s) = \prod_i b_i(s_i)$. Define $W(0) = 0$, $W(1) = 1$ and $W(u) = (1 - p_{\ell(u)}) W(\mathrm{lo}(u)) + p_{\ell(u)} W(\mathrm{hi}(u))$. Draw the variables above the root and the skipped variables with their own biases, and at node $u$ go to $\mathrm{hi}(u)$ with probability $p_{\ell(u)} W(\mathrm{hi}(u)) / W(u)$. Then each model $s$ is returned with probability $w(s) / Z$, where $Z = \sum_{t \models C} w(t) = W(\mathrm{root})$.

*Proof.* As in Lemma 1, $W(u)$ is the sum of $\prod_{i \ge \ell(u)} b_i(t_i)$ over the assignments $t$ of the variables at levels $\ell(u), \ldots, n-1$ that satisfy $f_u$: a skipped variable $x_i$ is free, and summing over its two values multiplies by $b_i(0) + b_i(1) = 1$. The variables above the root contribute the factor 1 in the same way, so $Z = W(\mathrm{root})$. All biases are positive, so $W(u) > 0$ whenever $f_u \ne 0$, and the walk stays on nodes with $W > 0$ as in Lemma 2. For a model $s$ with path $u_0, \ldots, u_k$, the probability of returning $s$ is the product of $b_i(s_i)$ over the variables above the root and over the skipped variables, times, for each $j$, $b_{\ell(u_j)}(s_{\ell(u_j)}) W(u_{j+1}) / W(u_j)$. The factors $b_i(s_i)$ together cover every variable once and give $w(s)$, and the ratios telescope to $W(1) / W(\mathrm{root}) = 1/Z$. $\blacksquare$

With every $p_i = 1/2$, $w(s) = 2^{-n}$, $W(u) = 2^{-(n - \ell(u))} N(u)$, and Theorem 2 gives Theorem 1.

**Theorem 3 (rejection sampling).** Let $\#C > 0$ and $q = \#C / 2^n$. Draw $x$ uniformly from $\{0, 1\}^n$ until $C(x) = 1$, and return the last $x$ and the number $T$ of draws. Then the returned $x$ is each model with probability exactly $1/\#C$, independently of $T$, and $T$ has the [geometric distribution](/geometric-distribution/) $\Pr[T = k] = (1 - q)^{k-1} q$, with mean $\mathrm{E}[T] = 1/q = 2^n / \#C$.

*Proof.* The draws are independent, and each is a model with probability $q$. The process returns $s$ at draw $k$ exactly when the first $k - 1$ draws are not models and draw $k$ equals $s$, which has probability $(1 - q)^{k-1} 2^{-n}$. Summing over $k$ gives $\Pr[x = s, T = k] = (1 - q)^{k-1} q \cdot \frac{1}{\#C}$, a product of a function of $k$ and the constant $1/\#C$. So $x$ and $T$ are independent, $x$ is uniform on the models, and $T$ is geometric with success probability $q$. Its mean is $\sum_{k \ge 1} k (1 - q)^{k-1} q = 1/q$. $\blacksquare$

If $\#C = 0$, rejection sampling never stops, which is why the implementation takes a bound on the tries. The bound changes the law only by the event that the bound is reached, which has probability $(1 - q)^{\text{bound}}$.

**What is measured.** The tests check Theorems 1 and 2 exactly, by running the sampler on every outcome of its calls to `randrange` and summing the probabilities in Fractions, and compare with the models found by evaluating each constraint on all $2^n$ assignments. For the pseudo-random generator of Python, the chi-square and total variation tests on a fixed-seed sample, and the mean number of rejection tries, are measurements, not proofs.
