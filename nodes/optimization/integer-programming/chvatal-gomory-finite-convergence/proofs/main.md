---
title: Repeated Chvátal closures of a rational polytope reach the integer hull
proves: [statement]
status: full
---

We prove the theorem for a rational polytope $P \subseteq \mathbb{R}^n$, which is Chvátal's theorem. The extension to unbounded rational polyhedra is due to Schrijver (1980) and is not proved here. We write $P'$ for the Chvátal closure, $P^{(0)} = P$, $P^{(k+1)} = (P^{(k)})'$ and $P_I = \operatorname{conv}(P \cap \mathbb{Z}^n)$. A *cut* of a polyhedron $Q$ is an inequality $c^T x \le \lfloor \delta \rfloor$ with $c \in \mathbb{Z}^n$ and $c^T x \le \delta$ valid for $Q$. For $Q = \{x : Ax \le b\}$ nonempty and bounded, LP duality shows that these are exactly the inequalities $(u^T A) x \le \lfloor u^T b \rfloor$ with $u \ge 0$ and $u^T A$ integral, up to weakening the right side. Each cut of $Q$ is valid for $Q \cap \mathbb{Z}^n$, so $P_I \subseteq P^{(k)} \subseteq P$ for all $k$.

**Lemma 1 (the closure of a rational polytope is a rational polytope).** If $P$ is a rational polytope, so is $P'$, and $P'$ is given by $P$ and finitely many cuts with integral right sides.

*Proof.* If $P = \emptyset$ then $P' = \emptyset$. Otherwise write $P = \{x : Ax \le b\}$ with $A$ and $b$ integral, which is possible by scaling each row by a positive integer. Take a cut $c^T x \le \lfloor u^T b \rfloor$ with $u \ge 0$ and $c = A^T u$ integral. Let $f = u - \lfloor u \rfloor \in [0, 1)^m$, componentwise. Then $A^T f = c - A^T \lfloor u \rfloor$ is integral, and since $\lfloor u \rfloor^T b$ is an integer,

$$\lfloor u^T b \rfloor = \lfloor u \rfloor^T b + \lfloor f^T b \rfloor.$$

So the cut is the sum of the inequality $\lfloor u \rfloor^T A x \le \lfloor u \rfloor^T b$, which holds on $P$, and the cut $(A^T f)^T x \le \lfloor f^T b \rfloor$. Hence $P'$ is the intersection of $P$ with the cuts that come from $f \in [0,1)^m$. For these, $A^T f$ lies in a bounded set, so it takes finitely many integral values $c$. For each such $c$, the numbers $\lfloor f^T b \rfloor$ are integers in a bounded set, and only the least one matters. So $P'$ is $P$ intersected with finitely many half spaces $c^T x \le \gamma$ with $c$ and $\gamma$ integral. $\square$

**Lemma 2 (faces).** Let $P$ be a rational polytope and $F = \{x \in P : a^T x = \beta\}$ a face, where $a^T x \le \beta$ is valid for $P$. Then $F' = P' \cap F$.

*Proof.* Scaling, we may assume $a$ integral and $\beta$ an integer. If $F = \emptyset$, both sides are empty. Let $F \ne \emptyset$.

$F' \subseteq P' \cap F$: $F' \subseteq F$ by definition. A cut $c^T x \le \lfloor \delta \rfloor$ of $P$ comes from an inequality $c^T x \le \delta$ valid for $P$, hence for $F$, so it is also a cut of $F$. So $F' \subseteq P'$.

$P' \cap F \subseteq F'$: let $c^T x \le \lfloor \delta \rfloor$ be a cut of $F$, and let $\delta_0 = \max\{c^T x : x \in F\} \le \delta$. Write $P = \{x : Ax \le b\}$. By LP duality for $\max\{c^T x : Ax \le b,\ a^T x = \beta\}$, there are $y \ge 0$ and $\lambda \in \mathbb{R}$ with

$$A^T y + \lambda a = c, \qquad y^T b + \lambda \beta = \delta_0.$$

Since $a^T x \le \beta$ is valid for $P$ and attained on $F$, LP duality also gives $z \ge 0$ with $A^T z = a$ and $z^T b = \beta$. Let $\mu = \lambda - \lfloor \lambda \rfloor \in [0, 1)$ and

$$c' = c - \lfloor \lambda \rfloor a = A^T (y + \mu z), \qquad \delta' = (y + \mu z)^T b = \delta_0 - \lfloor \lambda \rfloor \beta.$$

Then $c'$ is integral, the multipliers $y + \mu z$ are nonnegative, and $c'^T x \le \lfloor \delta' \rfloor$ is a cut of $P$. For $x \in P' \cap F$ we have $a^T x = \beta$ and $c'^T x \le \lfloor \delta' \rfloor$, so, since $\lfloor \lambda \rfloor \beta$ is an integer,

$$c^T x = c'^T x + \lfloor \lambda \rfloor \beta \le \lfloor \delta' \rfloor + \lfloor \lambda \rfloor \beta = \lfloor \delta_0 \rfloor \le \lfloor \delta \rfloor. \qquad \square$$

**Corollary 3.** With $P$ and $F$ as in Lemma 2, $P^{(k)} \cap F = F^{(k)}$ for all $k \ge 0$.

*Proof.* By induction on $k$. Each $P^{(k)}$ is a rational polytope by Lemma 1, and $a^T x \le \beta$ is valid for $P^{(k)} \subseteq P$, so $P^{(k)} \cap F = \{x \in P^{(k)} : a^T x = \beta\}$ is a face of $P^{(k)}$. Lemma 2 for $P^{(k)}$ gives $P^{(k+1)} \cap F = (P^{(k)} \cap F)' = (F^{(k)})' = F^{(k+1)}$. $\square$

We now prove the theorem by induction on $d = \dim P$, with $\dim \emptyset = -1$. Assume that it holds for all rational polytopes of dimension less than $d$.

**Lemma 4 (the descent step).** Let $P$ be a rational polytope of dimension $d$, let $c \in \mathbb{Z}^n$, let $Q = P^{(k)}$ for some $k$, and let $\gamma$ be an integer with $Q \subseteq \{x : c^T x \le \gamma\}$. Assume that no integer point of $P$ has $c^T x = \gamma$, and that $c^T x$ is not constant on $Q$ or $\dim Q < d$. Then $P^{(k + r)} \subseteq \{x : c^T x \le \gamma - 1\}$ for some $r$.

*Proof.* If $\dim Q < d$, then $Q_I \subseteq P_I$, and the theorem for $Q$ gives $r_0$ with $Q^{(r_0)} = Q_I$. Then $P^{(k + r_0)} = Q_I$, a polytope whose vertices are integer points of $P$. They satisfy $c^T x \le \gamma$ and not $c^T x = \gamma$, so $c^T x \le \gamma - 1$ on $Q_I$, and $r = r_0$ works.

Otherwise $c^T x$ is not constant on $Q$, so $F = \{x \in Q : c^T x = \gamma\}$ is empty or a proper face of $Q$, and $\dim F < \dim Q \le d$. $F$ contains no integer point, so $F_I = \emptyset$, and the induction hypothesis gives $r_0$ with $F^{(r_0)} = \emptyset$. By Corollary 3 applied to $Q$, $Q^{(r_0)} \cap F = \emptyset$, so $c^T x < \gamma$ on the polytope $Q^{(r_0)}$, and its maximum is below $\gamma$. The next closure contains the cut $c^T x \le \lceil \gamma \rceil - 1 = \gamma - 1$, so $r = r_0 + 1$ works. $\square$

**Theorem.** For each rational polytope $P$ there is a $k$ with $P^{(k)} = P_I$.

*Proof.* If $P = \emptyset$, take $k = 0$. If $d = 0$, then $P = \{p\}$. If $p$ is integral, $P = P_I$. Otherwise some $p_j$ is fractional, and the cuts $x_j \le \lfloor p_j \rfloor$ and $-x_j \le \lfloor -p_j \rfloor$ give $P' = \emptyset = P_I$. Let $d \ge 1$.

*Case 1: $P_I = \emptyset$.* Since $d \ge 1$, some coordinate $x_j$ is not constant on $P$. Let $\gamma_0 = \lfloor \max_P x_j \rfloor$, so $P' \subseteq \{x_j \le \gamma_0\}$. Apply Lemma 4 repeatedly with $c = e_j$. At each step the current $Q = P^{(k)}$ satisfies $x_j \le \gamma$. Either $\dim Q < d$, or $\dim Q = d$, in which case $Q$ and $P$ have the same affine hull, so $x_j$ is not constant on $Q$. There are no integer points in $P$ at all. So each application lowers $\gamma$ by 1, and after finitely many steps $\gamma < \min_P x_j$, which gives $P^{(k)} = \emptyset = P_I$.

*Case 2: $P_I \ne \emptyset$.* $P_I$ is a polytope with integer vertices, so $P_I = \{x : c_i^T x \le \delta_i,\ i = 1, \ldots, t\}$ with each $c_i$ integral and each $\delta_i$ an integer: scale a rational normal vector to an integer one, and take $\delta_i$ as the maximum of $c_i^T x$ over the integer vertices. Fix $i$, and write $c = c_i$, $\delta = \delta_i$. Let $\gamma_0 = \lfloor \max_P c^T x \rfloor$, so $P' \subseteq \{c^T x \le \gamma_0\}$. While the current bound $\gamma$ is greater than $\delta$, look at $Q = P^{(k)}$. Integer points $x$ of $P$ lie in $P_I$, so $c^T x \le \delta < \gamma$. If $c^T x$ is constant on $Q$, it is constant on the nonempty set $P_I \subseteq Q$, with a value at most $\delta$, so $Q \subseteq \{x : c^T x \le \delta\}$ and we stop. Otherwise the conditions of Lemma 4 hold, and it lowers $\gamma$ by 1. After at most $\gamma_0 - \delta$ steps, some $P^{(k_i)}$ satisfies $c_i^T x \le \delta_i$.

Let $k = \max_i k_i$. Since the closures decrease, $P^{(k)}$ satisfies every inequality of $P_I$, so $P^{(k)} \subseteq P_I$. With $P_I \subseteq P^{(k)}$, this gives $P^{(k)} = P_I$. $\blacksquare$
