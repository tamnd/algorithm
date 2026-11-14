---
title: Under the stated model, the precedence relations select exactly the feasible assembly orders
proves: [correctness, termination]
status: full
---

We use the pseudocode and the model of the page. The product has parts $P$, $|P| = n \ge 2$, and a connected liaison graph $L$ with liaison set $E$. For a set $Q$ of parts, $E(Q)$ is the set of liaisons with both ends in $Q$. The motion set is $M$. For a part $v$ and a direction $d \in M$, $B(v, d)$ is the set of parts that block $v$ when $v$ translates to infinity along $d$. The test for one step is

$$f(Q, p) \iff \text{there is } d \in M \text{ with } Q \cap B(v, d) = \emptyset \text{ for } v = p,$$

that is, part $p$ can come into the placed set $Q$ by one translation along $-d$, since the motion that takes it out along $d$ meets nothing. A *feasible order* is an order $p_1, \ldots, p_n$ of $P$ such that for each $k \ge 2$, part $p_k$ shares a liaison with one of $p_1, \ldots, p_{k-1}$ and $f(\{p_1, \ldots, p_{k-1}\}, p_k)$ holds. Its *image* is the sequence of states $E(Q_2), E(Q_3), \ldots, E(Q_n)$ with $Q_k = \{p_1, \ldots, p_k\}$.

The answers are the formulas of lines L1 to L3. For a part $w$, $\mathrm{present}(w)$ is the disjunction of the liaisons at $w$. For a part $v$, $\mathrm{stuck}(v) = \bigwedge_{d \in M} \bigvee_{w \in B(v, d)} \mathrm{present}(w)$, where an empty disjunction is false. For a liaison $i = \{u, v\}$:

- $\mathrm{pre}_i$ is false if $f(\{u\}, v)$ and $f(\{v\}, u)$ are both false, and true otherwise;
- $\mathrm{post}_i = (\mathrm{present}(u) \wedge \mathrm{stuck}(v)) \vee (\mathrm{present}(v) \wedge \mathrm{stuck}(u))$.

A step from a state $X$ that makes the set of liaisons $\Delta$ *passes* when $\mathrm{pre}_i(X)$ is true and $\mathrm{post}_i(X)$ is false for every $i \in \Delta$.

**Lemma 1 (monotone blocking).** If $Q' \subseteq Q$ and $f(Q, p)$, then $f(Q', p)$.

*Proof.* If $Q \cap B(p, d) = \emptyset$ then $Q' \cap B(p, d) = \emptyset$. $\square$

**Lemma 2 (a state names its parts).** Let $Q$ be connected in $L$ with $|Q| \ge 2$, and let $X = E(Q)$. For every part $w$, $\mathrm{present}(w)$ is true on $X$ exactly when $w \in Q$. So $Q$ is the set of ends of the liaisons in $X$, and $\mathrm{stuck}(v)$ is true on $X$ exactly when $f(Q, v)$ is false. On the empty state, every $\mathrm{present}(w)$ is false.

*Proof.* If $w \in Q$, then $w$ has a neighbour in $Q$ because $Q$ is connected and has a second part, so a liaison at $w$ lies in $X$. If $w \notin Q$, no liaison at $w$ lies in $E(Q)$. Then $\mathrm{stuck}(v)$ on $X$ says that for each $d \in M$ some $w \in B(v, d)$ lies in $Q$, which is the negation of $f(Q, v)$. $\square$

**Lemma 3 (a later step passes exactly when it is feasible).** Let $Q$ be connected with $|Q| \ge 2$, let $p \notin Q$ share a liaison with $Q$, and let $X = E(Q)$ and $\Delta = E(Q \cup \{p\}) \setminus X$, the liaisons between $p$ and $Q$. The step from $X$ that makes $\Delta$ passes if and only if $f(Q, p)$.

*Proof.* $\Delta$ is not empty. Take $i = \{p, u\} \in \Delta$, so $u \in Q$. By Lemma 2, $\mathrm{present}(u)$ is true and $\mathrm{present}(p)$ is false on $X$, so $\mathrm{post}_i(X) = \mathrm{stuck}(p)(X) = \neg f(Q, p)$. If $f(Q, p)$ holds, then $f(\{u\}, p)$ holds by Lemma 1, so $\mathrm{pre}_i$ is true, and $\mathrm{post}_i(X)$ is false: every liaison of $\Delta$ passes. If $f(Q, p)$ fails, then $\mathrm{post}_i(X)$ is true for any $i \in \Delta$, and the step does not pass. $\square$

**Lemma 4 (the first step).** The start state $\{i\}$ for $i = \{u, v\}$ is made on line L4 if and only if $f(\{u\}, v)$ or $f(\{v\}, u)$.

*Proof.* The step from the empty state makes $\Delta = E(\{u, v\}) = \{i\}$. On the empty state $\mathrm{post}_i$ is false by Lemma 2, so the step passes exactly when $\mathrm{pre}_i$ is true. $\square$

**Lemma 5 (prefixes are connected).** In an order where each new part shares a liaison with an earlier part, every prefix $Q_k$ is connected. Conversely, in the diagram every state is $E(Q)$ for a connected $Q$ with $|Q| \ge 2$, and the full state $E$ is $E(Q)$ only for $Q = P$.

*Proof.* The first claim is by induction on $k$. For the second, the start states are $E(\{u, v\})$ for a liaison $\{u, v\}$, and line L6 adds only a part with a liaison to $Q$. If $Q \ne P$, some liaison of the connected graph $L$ leaves $Q$ and is not in $E(Q)$, so $E(Q) \ne E$. $\square$

**Theorem 1 (exact selection).** The paths of the diagram from a start state to the full state are exactly the images of the feasible orders.

*Proof.* Take a feasible order. Its first two parts share a liaison $i$, and $f(\{p_1\}, p_2)$ holds, so $\{i\}$ is a start state by Lemma 4. For $k \ge 2$, $Q_k$ is connected by Lemma 5, $p_{k+1}$ shares a liaison with it, and $f(Q_k, p_{k+1})$ holds, so line L6 tries $p = p_{k+1}$ and by Lemma 3 line L9 adds the arc from $E(Q_k)$ to $E(Q_{k+1})$. The last state is $E(P) = E$. So the image is a path.

Conversely, take a path $X_2, \ldots, X_m$ from a start state $X_2 = \{i\}$, $i = \{u, v\}$, to $E$. By Lemma 5, $X_k = E(Q_k)$ with $Q_2 = \{u, v\}$, each arc adds one part, and $Q_m = P$, so $m = n$. By Lemma 4 one of $f(\{u\}, v)$ and $f(\{v\}, u)$ holds: let $p_1, p_2$ be $u, v$ in an order for which it holds. For $k \ge 3$ let $p_k$ be the part of $Q_k \setminus Q_{k-1}$. It shares a liaison with $Q_{k-1}$, because line L6 chose it so, and $f(Q_{k-1}, p_k)$ holds by Lemma 3, because the arc passed. So $p_1, \ldots, p_n$ is a feasible order with this image. $\square$

**Corollary 1 (counting).** Two feasible orders have the same image exactly when they differ only in the order of their first two parts. So the number of feasible orders is the sum over the sequences of the number (1 or 2) of feasible orders of their first two parts. When $M$ is closed under $d \mapsto -d$ and the parts are boxes, both orders of the first two parts are feasible, and the number of feasible orders is twice the number of sequences.

*Proof.* By Lemma 2 the image fixes $Q_2, \ldots, Q_n$, hence $p_3, \ldots, p_n$ and the set $\{p_1, p_2\}$. For the last claim: if $f(\{u\}, v)$ fails, then $u \in B(v, d)$ for every $d \in M$, so $u \in B(v, d)$ and $u \in B(v, -d)$ for one $d$, which would put $u$ on both sides of $v$ along the axis of $d$. $\square$

**Termination.** The states are sets $E(Q)$ for distinct connected sets $Q$, so there are at most $N$ of them, $N$ the number of connected sets, and each is expanded once. The path count of line L10 recurses only to larger states, so it stops, and with memoization it visits each state and arc once.

**Scope.** The proof uses one property of the answers: on the states that can occur, $\mathrm{pre}_i \wedge \neg \mathrm{post}_i$ for the liaisons of a step says exactly whether the new part can come in. Lemma 1, which says that blocking only gets worse when parts are added, is what makes the answer to Q1 trivial in this model. A condition that gets easier as parts are added, such as a part that needs another part below it as a support, goes into Q1 instead. It can be written in the same way, but on the empty state it cannot tell which of the first two parts came first, so the first step must then be checked on the parts.
