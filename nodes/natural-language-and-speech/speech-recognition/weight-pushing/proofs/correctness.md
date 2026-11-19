---
title: Weight pushing keeps every weight and makes each state stochastic
proves: [correctness]
status: full
---

We use the notation of the page. Weights are costs. The semiring is the tropical semiring $(\mathbb{R} \cup \{+\infty\}, \min, +, +\infty, 0)$ or the log semiring on costs, with $a \oplus b = -\log(e^{-a} + e^{-b})$. In both, $\otimes$ is $+$. The machine $T$ has states $Q$, a start state $i$ with initial weight $\lambda$, final weights $\rho(q)$ (with $\rho(q) = +\infty$ when $q$ is not final) and arcs $e = (p, a, b, w, n)$ with finite $w$. The labels play no part, so everything below holds for acceptors and transducers alike.

For a path $\pi = e_1 \cdots e_k$ from $p$ to $q$, write $w(\pi) = w(e_1) + \cdots + w(e_k)$. The distance to the final states is

$$D(p) = \bigoplus_{\pi \text{ from } p \text{ to } q} w(\pi) \otimes \rho(q),$$

the $\oplus$-sum over all paths from $p$ and all their end states. In the tropical semiring it is the cost of the best path to a final state. In the log semiring it is $-\log$ of the total probability of the paths to a final state, and we assume it is finite where a final state can be reached, which holds when the sum converges.

**Lemma 1 (any potential keeps the weights).** Let $d$ be any function from the trim states (those with $D(q) \ne +\infty$) to $\mathbb{R}$. Give the machine the new weights $\lambda' = \lambda + d(i)$, $w'(e) = w(e) + d(n) - d(p)$ for an arc $e$ from $p$ to $n$, and $\rho'(q) = \rho(q) - d(q)$, and drop the states with $D(q) = +\infty$ with their arcs. Then every successful path keeps its weight, and so every string or string pair keeps its weight.

*Proof.* A successful path $i = q_0, q_1, \ldots, q_k$ visits only trim states, since each of them reaches the final state $q_k$. So the dropped states lie on no successful path and their removal changes no weight. On the path, the new weight telescopes:

$$\lambda' + \sum_{j=1}^{k} \big(w(e_j) + d(q_j) - d(q_{j-1})\big) + \rho'(q_k) = \lambda + d(q_0) + \sum_j w(e_j) + d(q_k) - d(q_0) + \rho(q_k) - d(q_k),$$

which is $\lambda + \sum_j w(e_j) + \rho(q_k)$, the old weight. The weight of a string is the $\oplus$-sum of the weights of its successful paths, which are the same paths with the same weights. $\square$

So the correctness of the weights does not depend on the values of $d$. The distances matter only for the second claim, the normal form.

**Lemma 2 (the distance equation).** $D$ satisfies, for every state $p$,

$$D(p) = \rho(p) \oplus \bigoplus_{e = (p, \cdot, \cdot, w, n)} w \otimes D(n).$$

*Proof.* A path from $p$ is either empty, which gives the term $\rho(p)$, or starts with an arc $e$ to $n$ and goes on with a path from $n$. Group the paths by their first arc and use distributivity of $\otimes$ over the (possibly infinite, convergent) sum. $\square$

**Lemma 3 (the shortest distance, tropical).** In the tropical semiring with no cycle of negative cost, lines L1 to L7 stop and return $d = D$.

*Proof.* We show three facts.

1. *Every value is a path weight.* At line L1, $d(q) = \rho(q)$ is the weight of the empty path at $q$. At line L6, the new value of $d(p)$ is $w + r_q$ for an arc from $p$ to $q$, and we show below that $r_q = d(q)$, so it is the weight of that arc followed by a path from $q$. Hence $d(p) \ge D(p)$ at all times.
2. *At a pop, $r_q = d(q)$.* $r_q$ starts at $\rho(q) = d(q)$. After a pop it is reset to $+\infty$, and each later change of $d(q)$ sets $d(q)$ to a value $x$ below the old one and sets $r_q$ to $\min(r_q, x) = x$, since the values $x$ decrease. A state is queued only after such a change, so at its next pop $r_q = d(q)$.
3. *At the end, the distance equation holds as an inequality.* Consider any arc from $p$ to $q$. After the last change of $d(q)$, the state $q$ is in the queue (line L7), and it is popped later, at which point line L6 makes $d(p) \le w + d(q)$. Values only decrease, so this stays true. Also $d(q) \le \rho(q)$ from line L1.

By fact 3 and induction on the length of a path, $d(p)$ is at most the weight of every path from $p$ to a final state, plus its final weight. So $d(p) \le D(p)$, and with fact 1, $d = D$.

Termination is the argument for the queue form of [Bellman-Ford](/bellman-ford/). Split the run into rounds: round 0 pops the final states queued at line L1, and round $k + 1$ pops the states queued during round $k$. By induction, after round $k$ every $d(p)$ is at most the best weight of a path from $p$ with at most $k$ arcs, plus its final weight. With no negative cycle, a best path is simple and has at most $|Q| - 1$ arcs, so after round $|Q| - 1$ every value is final, no value changes in the next round, and the queue becomes empty. Each round pops each state at most once and looks at each arc at most once, so the time is $O(|Q| \cdot |E|)$. $\square$

In the log semiring the values $d(p)$ grow toward $D(p)$ from below in probability, and the loop stops when no value changes by more than $\delta$. Mohri 2002 shows that the generic algorithm computes $D$ in a $k$-closed semiring. The log semiring is not $k$-closed, and in it the result is an approximation; the tests compare it with the exact solution of the linear system for the probabilities.

**Theorem (pushing).** Let $T'$ be the result of lines L8 to L12 with $d = D$.

1. $T'$ gives every string, or string pair, the same weight as $T$.
2. Tropical semiring: at every state $p$ of $T'$, the minimum of $\rho'(p)$ and the weights of the arcs that leave $p$ is $0$, and every arc weight and final weight is $\ge 0$. The initial weight $\lambda'$ is the cost of the best successful path of $T$.
3. Log semiring: at every state $p$ of $T'$, $e^{-\rho'(p)} + \sum_{e \text{ leaves } p} e^{-w'(e)} = 1$, so $T'$ is stochastic. The initial weight $\lambda'$ is $-\log$ of the total probability of $T$.

*Proof.* Claim 1 is Lemma 1. For claims 2 and 3, subtract $D(p)$ from both sides of the distance equation of Lemma 2. Since $\otimes$ is $+$ and $\oplus$ commutes with adding a constant to all its arguments,

$$\bar 1 = 0 = \big(\rho(p) - D(p)\big) \oplus \bigoplus_{e} \big(w(e) + D(n) - D(p)\big) = \rho'(p) \oplus \bigoplus_e w'(e).$$

Arcs into dropped states have $D(n) = +\infty$ and contribute $+\infty = \bar 0$ to the sum, so dropping them changes nothing. In the tropical semiring this says the minimum is $0$, so each term is $\ge 0$. In the log semiring it says that the probabilities $e^{-\rho'(p)}$ and $e^{-w'(e)}$ add up to $e^{0} = 1$. Finally $\lambda' = \lambda + D(i)$ is the $\oplus$-sum of the weights of all successful paths, by the definition of $D$. $\square$

**Remark (why this helps pruning).** In the tropical case, let a path prefix go from $i$ to $q$. In $T'$ its cost, including $\lambda'$, is $\lambda + w(\text{prefix}) + D(q)$ by the telescoping sum of Lemma 1, which is the cost of the best complete path that starts with this prefix. Before pushing, the cost of a prefix says nothing about its endings, and a prefix can look cheap and lead only to costly endings.
