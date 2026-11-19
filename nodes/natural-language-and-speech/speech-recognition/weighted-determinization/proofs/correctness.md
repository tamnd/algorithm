---
title: Weighted determinization gives an equivalent deterministic acceptor
proves: [correctness]
status: full
---

We use the notation of the page. Weights are costs, the semiring is the tropical semiring $(\mathbb{R} \cup \{+\infty\}, \min, +, +\infty, 0)$ or the log semiring on costs, with $a \oplus b = -\log(e^{-a} + e^{-b})$. In both, $\otimes$ is $+$, and for a finite $w$ the division $w^{-1} \otimes v$ is $v - w$. The input $A$ is an $\varepsilon$-free acceptor with finite arc weights, start state $i$, initial weight $\lambda$ and final weights $\rho$. We assume exact arithmetic, and that two weighted subsets are the same state of the result only when they are equal. The code rounds the residuals to a multiple of $\delta$ before it compares subsets; the remark at the end discusses this.

For a string $u$ and a state $q$, let $\delta(u, q)$ be the $\oplus$-sum of the weights of all paths of $A$ from $i$ to $q$ that read $u$, with $\delta(u, q) = \bar 0 = +\infty$ if there is none. The weight of $u$ in $A$ is

$$A(u) = \bigoplus_q \lambda \otimes \delta(u, q) \otimes \rho(q),$$

with $\rho(q) = \bar 0$ for a state that is not final.

**Lemma 1 (determinism).** The result $D$ is deterministic.

*Proof.* Line L5 handles each label once per state of $D$, and line L9 adds one arc for it. The start state is unique (line L1). $\square$

So every string $u$ has at most one path in $D$ from the start. If it exists, write $p'(u)$ for its last state and $W(u) = \lambda' \otimes w'_1 \otimes \cdots \otimes w'_k$ for the product of $\lambda' = \lambda$ and the weights of its arcs.

**Lemma 2 (the invariant).** For every string $u$, the path of $u$ in $D$ exists if and only if some path of $A$ reads $u$. If it exists, the weighted subset $p'(u)$ holds exactly the states $q$ with $\delta(u, q) \ne \bar 0$, and for each pair $(q, r_q)$ in it,

$$\lambda \otimes \delta(u, q) = W(u) \otimes r_q .$$

*Proof.* Induction on the length of $u$. For the empty string, the path of $A$ is empty, $\delta(\epsilon, i) = \bar 1$ and $\delta(\epsilon, q) = \bar 0$ for $q \ne i$, and $D$ starts in $\{(i, \bar 1)\}$ with $W = \lambda$ (line L1), so the claim holds.

Now let $u$ satisfy the claim and let $a$ be a label. Some path of $A$ reads $ua$ if and only if some state $q$ with $\delta(u, q) \ne \bar 0$ has an arc labelled $a$, that is, if and only if line L5 handles $a$ at $p'(u)$. Then line L9 adds an arc with label $a$, so the path of $ua$ in $D$ exists, and otherwise it does not. Assume it exists. Lines L6 and L7 compute

$$w' = \bigoplus_{(q, r_q) \in p'(u)} \ \bigoplus_{(q, a, w, n)} r_q \otimes w, \qquad v(n) = \bigoplus_{(q, r_q) \in p'(u)} \ \bigoplus_{(q, a, w, n)} r_q \otimes w,$$

where the second sum runs only over the arcs into $n$. A path of $A$ that reads $ua$ and ends in $n$ is a path that reads $u$ and ends in some $q$, followed by an arc $(q, a, w, n)$. By distributivity and the induction hypothesis,

$$\lambda \otimes \delta(ua, n) = \bigoplus_q \bigoplus_{(q, a, w, n)} \lambda \otimes \delta(u, q) \otimes w = \bigoplus_q \bigoplus_{(q, a, w, n)} W(u) \otimes r_q \otimes w = W(u) \otimes v(n).$$

The new subset holds the states $n$ with an arc into them, which are exactly those with $\delta(ua, n) \ne \bar 0$, since all weights are finite. Line L8 sets $r_n = v(n) - w'$, so $W(ua) \otimes r_n = W(u) + w' + v(n) - w' = W(u) \otimes v(n) = \lambda \otimes \delta(ua, n)$. $\square$

**Theorem (equivalence).** If the algorithm stops, $D(u) = A(u)$ for every string $u$.

*Proof.* If no path of $A$ reads $u$, then $A(u) = \bar 0$, and by Lemma 2 no path of $D$ reads $u$, so $D(u) = \bar 0$. Otherwise, by line L4 and Lemma 2,

$$D(u) = W(u) \otimes \rho'(p'(u)) = \bigoplus_{(q, r_q)} W(u) \otimes r_q \otimes \rho(q) = \bigoplus_q \lambda \otimes \delta(u, q) \otimes \rho(q) = A(u). \qquad \square$$

**Termination.** Each state of $D$ is a weighted subset $p'(u)$ for some string $u$ that $A$ can read, and line L10 creates a state only once.

- If $A$ is acyclic, it reads only finitely many strings, so $D$ has finitely many states and the loop stops. The number of states can still be exponential in the number of states of $A$, as for $(a \mid b)^* a (a \mid b)^{n-1}$, where $D$ has $2^n$ states.
- If $A$ has the twins property over the tropical semiring, Mohri 1997 proves that only finitely many weighted subsets occur, so the loop stops (Mohri 2009, Theorem 5, states the same result). For trim unambiguous acceptors over the tropical semiring, the twins property is also necessary (Mohri 2009, Theorem 6).
- Without the twins property the loop can run forever. In the acceptor with the arcs $0 \xrightarrow{a/0} 1$, $0 \xrightarrow{a/0} 2$, $1 \xrightarrow{a/3} 1$, $2 \xrightarrow{a/4} 2$, $1 \xrightarrow{b/0} 3$, $2 \xrightarrow{c/0} 3$ and final state 3, Lemma 2 and the tropical semiring give $p'(a^k) = \{(1, 0), (2, k - 1)\}$ for every $k \ge 1$: the best path to 1 costs $3(k-1)$ and the best path to 2 costs $4(k-1)$, and $W(a^k) = 3(k-1)$. These subsets are all different, so $D$ would need infinitely many states.

**Remark (rounding).** The code identifies two subsets when their residuals round to the same multiple of $\delta$, and it keeps the residuals of the first one. Each such merge can change the weight of a later path by less than $\delta$ per merged state on the path. The opposite error, two equal subsets whose residuals round apart, only adds a state and does not change any weight. In the tropical tests all weights are multiples of $0.25$, so the residuals are exact and the proof above applies as stated.
