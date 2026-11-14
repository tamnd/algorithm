---
title: The polynomial mode is exact, the numeric mode is exact without reconvergence, and exact signal probability is #P-hard
proves: [correctness]
status: full
---

The inputs $X_1, \ldots, X_n$ are independent with $P(X_i = 1) = p_i$. For a function $f : \{0,1\}^n \to \{0,1\}$ write

$$ \Pr\nolimits_p(f) \;=\; \sum_{x \in \{0,1\}^n} f(x) \prod_{i=1}^n p_i^{x_i} (1 - p_i)^{1 - x_i}, $$

which is $P(f(X) = 1)$. A polynomial in $x_1, \ldots, x_n$ is *multilinear* when no variable has an exponent above 1. The *suppression* $\sigma(q)$ of a polynomial $q$ replaces each monomial $c \prod_i x_i^{e_i}$ by $c \prod_{i : e_i \ge 1} x_i$ and collects terms.

**Lemma 1 (gate identities).** For each gate kind, the formula $r(q_1, \ldots, q_k)$ of lines L5 to L9 satisfies $r(b_1, \ldots, b_k) = \mathrm{kind}(b_1, \ldots, b_k)$ for all $b \in \{0,1\}^k$.

*Proof.* AND: the product of 0-1 values is 1 exactly when all are 1. OR: $1 - \prod_j (1 - b_j)$ is 0 exactly when all $b_j$ are 0. XOR: for $r, b \in \{0,1\}$, $r + b - 2 r b$ is 1 exactly when one of them is 1, so the fold of line L7 computes the parity. BUF returns $b_1$. Line L9 complements the value for NAND, NOR, XNOR and NOT, since $1 - b$ is the complement of a 0-1 value. $\square$

**Lemma 2 (uniqueness).** If two multilinear polynomials $q$ and $q'$ agree on $\{0,1\}^n$, then $q = q'$.

*Proof.* Let $d = q - q'$, a multilinear polynomial that is 0 on $\{0,1\}^n$, and suppose $d \ne 0$. Take a monomial $c \prod_{i \in S} x_i$ of $d$ with $c \ne 0$ and $|S|$ smallest. Evaluate $d$ at the corner $x$ with $x_i = 1$ for $i \in S$ and $x_i = 0$ otherwise. A monomial with set $T$ is 1 at this corner if $T \subseteq S$ and 0 otherwise. By the choice of $S$, no monomial of $d$ has a set strictly inside $S$, so $d(x) = c \ne 0$. This contradicts $d(x) = 0$. $\square$

**Lemma 3 (suppression keeps corner values).** For every polynomial $q$ and every $b \in \{0,1\}^n$, $\sigma(q)(b) = q(b)$. Also $\sigma(q q') = \sigma(\sigma(q) \sigma(q'))$ and $\sigma(q + q') = \sigma(q) + \sigma(q')$.

*Proof.* For $b_i \in \{0,1\}$ and $e \ge 1$, $b_i^e = b_i$. So each monomial has the same value before and after suppression. The two identities hold because suppression only lowers exponents $e \ge 1$ to 1, and the exponent of $x_i$ in a product is the sum of the exponents in the factors, which is at least 1 exactly when one of them is. $\square$

**Lemma 4 (the probability is the multilinear extension).** $\Pr_p(f)$ is a multilinear polynomial in $p_1, \ldots, p_n$, and $\Pr_b(f) = f(b)$ for every $b \in \{0,1\}^n$.

*Proof.* Each term $f(x) \prod_i p_i^{x_i} (1 - p_i)^{1 - x_i}$ is a product of one factor $p_i$ or $(1 - p_i)$ for each $i$, which is multilinear, and a sum of multilinear polynomials is multilinear. At a corner $p = b$, the factor $b_i^{x_i} (1 - b_i)^{1 - x_i}$ is 1 if $x_i = b_i$ and 0 otherwise. So only the term $x = b$ is not zero, and it equals $f(b)$. $\square$

**Theorem 1 (the polynomial mode is exact).** In the polynomial mode, for every node $y$, line L12 sets $P[y] = \Pr_p(f_y)$.

*Proof.* We show by induction in topological order that before line L12 the value $Q_y$ of $P[y]$ is a multilinear polynomial with $Q_y(b) = f_y(b)$ for all $b \in \{0,1\}^n$. For a primary input, $Q_{x_i} = x_i$, which is multilinear and equals the projection $f_{x_i}$ on the corners. For a gate $y = \mathrm{kind}(z_1, \ldots, z_k)$, lines L5 to L9 combine $Q_{z_1}, \ldots, Q_{z_k}$ with the formula $r$ and suppress after each product, so by Lemma 3 the result is $\sigma(r(Q_{z_1}, \ldots, Q_{z_k}))$, which is multilinear. At a corner $b$, Lemma 3, the induction hypothesis and Lemma 1 give

$$ Q_y(b) = r\big(Q_{z_1}(b), \ldots, Q_{z_k}(b)\big) = r\big(f_{z_1}(b), \ldots, f_{z_k}(b)\big) = \mathrm{kind}\big(f_{z_1}(b), \ldots, f_{z_k}(b)\big) = f_y(b). $$

So $Q_y$ and $\Pr_p(f_y)$ are multilinear and agree on all corners by Lemma 4. By Lemma 2 they are the same polynomial, and line L12 evaluates it at $p$. $\square$

**Theorem 2 (the numeric mode without reconvergence).** Suppose that for every gate the supports of its input pins are pairwise disjoint. Then the numeric mode returns $P[y] = \Pr_p(f_y)$ for every node $y$.

*Proof.* By induction in topological order we show two facts: $f_y$ depends only on the inputs in $S(y)$, and $P[y] = P(f_y(X) = 1)$. For a primary input both are clear. For a gate $y = \mathrm{kind}(z_1, \ldots, z_k)$, $f_y = \mathrm{kind}(f_{z_1}, \ldots, f_{z_k})$ depends only on $S(z_1) \cup \cdots \cup S(z_k) = S(y)$. The random variables $f_{z_j}(X)$ are functions of the disjoint groups of variables $(X_i)_{i \in S(z_j)}$, and the $X_i$ are mutually independent, so $f_{z_1}(X), \ldots, f_{z_k}(X)$ are mutually independent. For independent 0-1 variables $B_j$ with $P(B_j = 1) = q_j$:

- AND: $P(\text{all } B_j = 1) = \prod_j q_j$;
- OR: $P(\text{some } B_j = 1) = 1 - \prod_j (1 - q_j)$;
- XOR: if $R$ is the parity of $B_1, \ldots, B_{j-1}$ with $P(R = 1) = r$, and $B_j$ is independent of $R$, then $P(R \oplus B_j = 1) = r (1 - q_j) + (1 - r) q_j = r + q_j - 2 r q_j$;
- BUF and the complements of line L9 are clear.

With $q_j = P[z_j] = P(f_{z_j}(X) = 1)$ by the induction hypothesis, line L10 sets $P[y] = P(f_y(X) = 1)$. $\square$

A fanout-free circuit satisfies the hypothesis: if two input pins of a gate had a common input $x_i$ in their supports, there would be two paths from $x_i$ to the gate that end at different pins, and the node where these paths split would drive two gate pins.

**Counterexample under reconvergence.** For $u = \mathrm{AND}(a, b)$, $v = \mathrm{AND}(a, c)$, $y = \mathrm{OR}(u, v)$ and all $p = 1/2$, the numeric mode returns $1 - (1 - 1/4)^2 = 7/16$, while $P(y = 1) = P(a = 1) P(b \lor c = 1) = 3/8$. The supports $\{a, b\}$ and $\{a, c\}$ of the pins of $y$ meet, and the step that fails is the independence of $u$ and $v$: $P(u = v = 1) = 1/8 \ne 1/16$.

**Theorem 3 (hardness).** Computing $\Pr_p(f_y)$ for a circuit and rational input probabilities is #P-hard under polynomial-time reductions that make one query. It stays #P-hard with every $p_i = 1/2$ and gates AND, OR and NOT only.

*Proof.* Counting the satisfying assignments of a CNF formula is #P-complete (Valiant 1979). Let $F = C_1 \land \cdots \land C_m$ be a CNF formula over $x_1, \ldots, x_n$. Build a circuit with inputs $x_1, \ldots, x_n$, one NOT gate per variable that appears negated, one OR gate per clause over its literals, and one AND gate over the clause outputs. Its size is linear in the size of $F$, and its output $y$ computes $F$. With $p_i = 1/2$ for all $i$, every vector has probability $2^{-n}$, so $\Pr_p(f_y) = \#F / 2^{n}$. One query of the signal probability, and a multiplication by $2^n$, give $\#F$. $\square$

Since the number $2^n \Pr_{1/2}(f_y)$ counts the inputs that set $y$ to 1, it is itself a #P function, so for $p_i = 1/2$ the problem is #P-complete. The decision version, whether $\Pr_p(f_y) > 0$ for probabilities in $(0, 1)$, is satisfiability of the circuit and is NP-complete.
