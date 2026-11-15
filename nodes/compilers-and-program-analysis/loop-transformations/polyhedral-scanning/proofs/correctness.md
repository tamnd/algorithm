---
title: The scanning code visits each integer point of each statement exactly once, in lexicographic order
proves: [correctness]
status: full
---

**Setting.** We use the notation of the page. All constraints have integer coefficients and are written $g(x, N) \ge 0$ with $g$ affine. For a set $R$ of constraints, a *point of* $R$ means an integer point that satisfies them, and $R$ is *rationally empty* if no rational point does. We treat a polyhedron as its set of constraints, so for two of them $R \cup Q$ is the set of constraints of their intersection. Statement $S$ has the polyhedron $Q_S$ in $(x, N) \in \mathbb{Z}^n \times \mathbb{Z}^p$, made of its domain, the equalities $x_j = \theta_{S,j}(\vec{i})$, the zero padding and the context $K$. For each $N \in K$ the points of $Q_S$ are exactly the vectors $(\theta_S(\vec{i}), \vec{i}, 0, \dots, 0)$ with $\vec{i} \in D_S$, and this map is one to one, because $\vec{i}$ is part of the vector. So it is enough to prove the claim below for the points of the $Q_S$.

**Claim.** For every integer $N \in K$, the generated code runs the pairs $(x, S)$ with $x$ a point of $Q_S$, each exactly once, and no other pair, in the lexicographic order of $(x_1, \dots, x_n, S)$, where $S$ is compared by its text position.

### Step 1: operations that keep the integer points

**Lemma 1.** Let $R$ be a set of constraints.

1. Replacing $a \cdot x + c \ge 0$ by $(a / d) \cdot x + \lfloor c / d \rfloor \ge 0$, where $d$ is the gcd of the entries of $a$, keeps the points of $R$ and does not enlarge its rational set.
2. Removing a constraint that the others imply on all rational points keeps the rational set, so it keeps the points.
3. Every point of $R$ satisfies every constraint that Fourier-Motzkin elimination derives from $R$, before or after step 1.

*Proof.* (1) At an integer $x$, $(a / d) \cdot x$ is an integer, and it is at least $-c / d$, so it is at least $\lceil -c / d \rceil = -\lfloor c / d \rfloor$. Conversely $\lfloor c / d \rfloor \le c / d$, so the new constraint implies the old one at every rational point. (2) is clear. (3) A derived constraint is $b r + a q$ with $a, b > 0$, where $r \ge 0$ and $q \ge 0$ are constraints of $R$, or $a s - s_j r$ where $r = 0$ is an equality of $R$. Both are nonnegative wherever the constraints of $R$ hold. $\square$

Let $Q'$ be the shadow of $Q$ on $(x_1, \dots, x_k, N)$ computed at line L1. By Lemma 1, if $x$ is a point of $Q$, then $(x_1, \dots, x_k)$ with the same $N$ is a point of $Q'$. Also $Q'$ is contained in the rational projection of $Q$, because each derived constraint holds on that projection and step 1 only shrinks it.

### Step 2: separation

Let $Q'_1, \dots, Q'_r$ be the shadows at one call, each with the statement it stands for. Line L2 returns pieces $R$ with labels $L_R$.

**Lemma 2.** The pieces satisfy:

1. *Cover and disjointness.* Every point of $Q'_1 \cup \dots \cup Q'_r$ is a point of exactly one piece, and pieces have no other points.
2. *Labels.* A point $y$ of the piece $R$ is a point of $Q'_i$ if and only if $i \in L_R$.
3. *Separation.* For two different pieces $A$ and $B$, there is a constraint $g$ such that all rational points of one satisfy $g \ge 0$ and all rational points of the other satisfy $g \le -1$.

*Proof.* First, the difference. For constraint sets $P$ and $Q = \{q_1, \dots, q_t\}$, the pieces of $P \setminus Q$ are $P_j = P \cup \{q_1 \ge 0, \dots, q_{j-1} \ge 0, q_j \le -1\}$, with the rationally empty ones dropped; the loop also stops early when $P \cup \{q_1, \dots, q_j \ge 0\}$ is rationally empty, and then no later $P_j$ has a point. A point of $P$ that is not a point of $Q$ breaks some $q_j \ge 0$; let $j$ be the first. Since $q_j$ is an integer there, $q_j \le -1$, so the point lies in $P_j$ and in no other $P_{j'}$: for $j' < j$ it has $q_{j'} \ge 0$, and for $j' > j$ it breaks $q_j \ge 0$. Points of $Q$ lie in no $P_j$. Any $P_j$ and $P_{j'}$ with $j < j'$ are separated by $g = q_j$. Step 1 of Lemma 1, applied by the cleaning, keeps all of this, since it keeps points and only shrinks rational sets.

Now induct on the number of shadows inserted. With one shadow there is one piece. Suppose the claims hold for the pieces of $Q'_1, \dots, Q'_{i-1}$ and insert $Q = Q'_i$. Each old piece $R$ gives $R \cup Q$ with label $L_R \cup \{i\}$ (if not rationally empty) and the pieces of $R \setminus Q$ with label $L_R$. What is left of $Q$, the pieces of $(\dots(Q \setminus R_1) \setminus R_2 \dots)$, gets the label $\{i\}$.

(1) A point in some old piece $R$, unique by induction, lies in $R \cup Q$ if it is a point of $Q$, and else in exactly one piece of $R \setminus Q$. It lies in no piece of what is left of $Q$, since those avoid every old piece. A point of $Q$ in no old piece lies in exactly one piece of what is left of $Q$, by the property of the difference applied at each step.

(2) For a point of $R \cup Q$ or of a piece of $R \setminus Q$, the old labels are right by induction, and membership in $Q$ is right by construction. A point in what is left of $Q$ lies in no old piece, so by (1) for the old pieces it lies in no $Q'_{i'}$ with $i' < i$.

(3) Two new pieces that come from different old pieces inherit their separating constraint. $R \cup Q$ and a piece $R_j$ of $R \setminus Q$ are separated by $q_j$. Two pieces of $R \setminus Q$ are separated as shown above. A piece of what is left of $Q$ lies inside a piece of a difference by some old $R$, so it satisfies $r_j \le -1$ for a constraint $r_j$ of $R$, while every new piece inside $R$ satisfies $r_j \ge 0$. Two pieces of what is left of $Q$ were split at some difference step by a constraint of the piece subtracted there. $\square$

### Step 3: the order of the pieces

For pieces $A$ and $B$ at level $k$, let $W$ be the rational set of pairs $(a, b)$ with $a \in A$, $b \in B$, the same $N$ and $a_j = b_j$ for $j < k$.

**Lemma 3.** Either $W$ is empty, or $a_k < b_k$ on all of $W$, or $a_k > b_k$ on all of $W$. The test of line L3 finds which.

*Proof.* Take the constraint $g = \alpha x_k + h(x_1, \dots, x_{k-1}, N)$ of Lemma 2(3), and say $A$ satisfies $g \ge 0$ and $B$ satisfies $g \le -1$. On $W$, both points have the same $h$. If $\alpha = 0$, then $h \ge 0$ and $h \le -1$, so $W$ is empty. If $\alpha > 0$, then $\alpha a_k \ge -h > -h - 1 \ge \alpha b_k$, so $a_k > b_k$. If $\alpha < 0$, the same steps give $a_k < b_k$. Line L3 tests the emptiness of $W$, of $W \cap \{a_k \ge b_k\}$ and of $W \cap \{b_k \ge a_k\}$ with the simplex method, which is exact. $\square$

So line L3 builds a relation $A \to B$ ("$A$ comes first") between every two pieces with $W \ne \emptyset$. If it has no cycle, a topological sort gives an order. In that order, if two pieces $A$ before $B$ both have points over the same outer values $(x_1, \dots, x_{k-1}, N)$, then $W \ne \emptyset$, the relation holds as $A \to B$, and every point of $A$ there has a smaller $x_k$ than every point of $B$ there.

### Step 4: one loop

**Lemma 4.** Let $R$ be a piece at level $k$ with the guards and bounds of lines L6 and L7, and let $(y, N)$, $y = (x_1, \dots, x_{k-1})$, be an integer point that satisfies the context $C$ of the call. The loop of line L10 runs $x_k$ over exactly the integers $z$ such that $(y, z)$ is a point of $R$, in increasing order.

*Proof.* The constraints of $R$ without $x_k$ are the guards, except those implied by $C$, which hold at $(y, N)$. Line L7 removes from the constraints with $x_k$, together with $C$, those implied by the others. By Lemma 1(2) the remaining set has the same rational points as all of them together with $C$. Since $(y, N)$ satisfies all of $C$, the kept bounds hold at $(y, z)$ exactly when all constraints of $R$ with $x_k$ hold. For an integer $z$, $a z + r \ge 0$ with $a > 0$ means $z \ge \lceil -r / a \rceil$, and with $a < 0$ it means $z \le \lfloor r / (-a) \rfloor$. So the integers $z$ with $(y, z) \in R$ are those from the largest lower bound to the smallest upper bound. Both kinds of bounds exist: $R$ lies in a shadow, which lies in the rational projection of some $Q_S$, and that projection is bounded for each $N \in K$, because $D_S$ is. $\square$

### Step 5: the induction

**Invariant.** A call $\mathrm{SCAN}(\Lambda, C, k)$ gets a list $\Lambda$ of pairs $(Q, S)$, at most one per statement, such that every $Q$ contains the constraints of $C$. We prove, by induction on $n - k$, that for every integer point $(y, N)$ of $C$ with $y \in \mathbb{Z}^{k-1}$ the code of the call runs exactly the pairs $(x, S)$ with $(Q, S) \in \Lambda$, $x$ a point of $Q$ and $(x_1, \dots, x_{k-1}) = y$, each once, in the lexicographic order of $(x_k, \dots, x_n, S)$.

*The pairs run.* Take such a pair $(x, S)$. By Step 1, $(y, x_k)$ is a point of the shadow $Q'$, so by Lemma 2(1) it is a point of exactly one piece $R$, and by Lemma 2(2) $S \in L_R$. By Lemma 4, the loop of $R$ runs $z = x_k$ exactly once, and the loops of the other pieces never reach $(y, x_k)$, because they run only over their own points.

- If $k = n$, the body runs the statements of $L_R$, so $(x, S)$ runs once. Conversely, a statement $S \in L_R$ runs at $x = (y, z)$ only when $x$ is a point of $R$, so of $Q'$ by Lemma 2(2). At level $n$ there is nothing to eliminate, and by Lemma 1 the points of $Q'$ are the points of $Q$.
- If $k < n$, the body is $\mathrm{SCAN}(\Lambda_R, C \cup R, k + 1)$ with $\Lambda_R = \{(Q \cup R, S) : S \in L_R\}$. Every new $Q \cup R$ contains $C \cup R$, and $(y, z, N)$ satisfies $C \cup R$; the pruning of the new context keeps its rational set. By induction the body runs exactly the pairs $(x, S)$ with $S \in L_R$, $x$ a point of $Q$ and of $R$, and prefix $(y, z)$. Every point with prefix $(y, z)$ is a point of $R$, because $R$ only has constraints in $x_1, \dots, x_k$. So these are all the pairs with prefix $(y, z)$ and $S \in L_R$. For $S \notin L_R$, no point of $Q$ has the prefix $(y, z)$, because its shadow would contain $(y, z)$, and Lemma 2(2) would put $S$ in $L_R$.

So the call runs every pair once and no other pair.

*The order.* Inside one loop, $z = x_k$ grows, and for each $z$ the body runs its pairs in the order of $(x_{k+1}, \dots, x_n, S)$ by induction, or in text order at $k = n$. Between two pieces $A$ before $B$ in the sorted order, Step 3 shows that every point of $A$ over $y$ has a smaller $x_k$ than every point of $B$ over $y$. So the whole sequence is ordered by $(x_k, \dots, x_n, S)$.

*The fallback.* If line L4 runs, the code runs $z$ in increasing order over a range that contains the ranges of all pieces, and for each $z$ runs the body of every piece whose range contains $z$. By Lemma 4, that range is exactly the set of $z$ with $(y, z)$ a point of the piece, and by Lemma 2(1) at most one piece has this point. So the same argument applies, with the order coming from the single loop over $z$.

### Step 6: conclusion

The first call is $\mathrm{SCAN}(\{(Q_S, S)\}, K, 1)$, with $K$ pruned, which keeps its rational set. Every $Q_S$ contains $K$, and for $k = 1$ the prefix $y$ is empty. The invariant gives the claim for every integer $N \in K$. The generator itself stops: the recursion has depth $n$, each call makes finitely many pieces, and each linear program ends, because the simplex method uses a ratio test that cannot cycle. $\blacksquare$
