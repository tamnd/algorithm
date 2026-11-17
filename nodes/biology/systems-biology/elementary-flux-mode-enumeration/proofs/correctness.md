---
title: The nullspace double description method lists every elementary flux mode exactly once
proves: [correctness]
status: full
---

Fix an $n \times m$ matrix $S$ and a set of reversible reactions. The flux cone is $C = \{v : S v = 0, \; v_j \ge 0 \text{ for irreversible } j\}$, and the elementary flux modes (EFMs) are its non-zero vectors of minimal support, counted up to a positive factor (see the definition page). We show that efm_enumeration returns each EFM exactly once, as a vector of coprime integers.

Throughout, a *ray* is a non-zero vector up to a positive factor, and for a pointed polyhedral cone $P = \{t \in \mathbb{R}^d : A t \ge 0\}$ with $\operatorname{rank} A = d$ and a vector $t \in P$, the *tight set* is $Z(t) = \{i : a_i t = 0\}$, where $a_i$ is row $i$ of $A$. We write $A_Z$ for the rows of $A$ in $Z$.

## Step 1: splitting

Line L1 builds $S'$, with the columns of $S$ followed by $-S_j$ for each reversible $j$, so that column $k$ of $S'$ is $\sigma_k S_{j(k)}$ with $\sigma_k = \pm 1$. Let $C' = \{x \ge 0 : S' x = 0\}$ and $\varphi(x)_j = \sum_{k : j(k) = j} \sigma_k x_k$. A *two-cycle* is a vector of $C'$ whose support is the two copies of one reversible reaction. For an EFM $e$ of $C$, let $\psi(e)$ put $\max(e_j, 0)$ on the forward copy of $j$ and $\max(-e_j, 0)$ on the backward copy.

**Lemma 1 (the support rank test).** Let $Q$ be the support of a non-zero $v \in C$. Then $v$ is an EFM of $C$ if and only if $\dim \ker S_Q = 1$. The same holds for $C'$ and $S'$.

*Proof.* If $\dim \ker S_Q \ge 2$, take $w \in \ker S_Q$ independent of $v_Q$, with the sign chosen so that some $i$ has $v_i / w_i > 0$. Let $\tau = \min \{ v_i / w_i : v_i / w_i > 0 \}$. Then $u = v - \tau w$ (zero outside $Q$) has $S u = 0$, is not zero because $w$ is independent of $v$, has $u_i = 0$ for some $i \in Q$, and has the sign of $v_i$ or 0 on every other $i \in Q$. So $u \in C$ and $\operatorname{supp}(u) \subsetneq Q$, and $v$ is not an EFM. Conversely, if $\dim \ker S_Q = 1$ and $u \in C$ is non-zero with $\operatorname{supp}(u) \subsetneq Q$, then $u_Q \in \ker S_Q$, so $u_Q = c v_Q$ with $c \ne 0$, and then $\operatorname{supp}(u) = Q$, a contradiction. The argument for $C'$ is the same with $S'$, since $C'$ is the flux cone of $S'$ with all reactions irreversible. $\square$

**Lemma 2 (the splitting correspondence).** $\psi$ maps the EFMs of $C$ to the EFMs of $C'$ that are not two-cycles, and $\varphi$ maps these back, with $\varphi(\psi(e)) = e$ and $\psi(\varphi(x)) = x$.

*Proof.* Let $e$ be an EFM of $C$. Then $\psi(e) \ge 0$, $S' \psi(e) = S e = 0$, and $\psi(e)$ never uses both copies of a reaction. Its support columns in $S'$ are the columns $\pm S_j$ for $j \in \operatorname{supp}(e)$, so $\dim \ker S'_{\operatorname{supp}(\psi(e))} = \dim \ker S_{\operatorname{supp}(e)} = 1$, and $\psi(e)$ is an EFM of $C'$ by Lemma 1. It is not a two-cycle, since it uses one copy per reaction. Clearly $\varphi(\psi(e)) = e$.

Now let $x$ be an EFM of $C'$ that is not a two-cycle. If $x$ had both copies of some reversible $j$ in its support, the two-cycle on these copies would be a vector of $C'$ with support inside $\operatorname{supp}(x)$, so by minimality $\operatorname{supp}(x)$ would be these two copies, and $x$ would be the two-cycle. So $x$ uses at most one copy of each reaction. Then $v = \varphi(x)$ has $S v = S' x = 0$, the sign of each irreversible flux is that of $x$ (non-negative), and the support columns of $v$ in $S$ are, up to sign, the support columns of $x$ in $S'$. By Lemma 1 for $C'$ and then for $C$, $v$ is an EFM of $C$, and $\psi(v) = x$. $\square$

So it suffices to list the EFMs of $C'$, drop the two-cycles and apply $\varphi$, which is what line L10 does.

## Step 2: the cone in kernel coordinates

Let $m'$ be the number of columns of $S'$. Line L2 computes the reduced row echelon form of $S'$ with pivot columns $\Pi$ and free columns $F$, $|F| = d = \dim \ker S'$, and the kernel basis whose vector $b$ is 1 at the $b$-th free column and 0 at the other free columns. Let $K$ be the $m' \times d$ matrix with these vectors as columns. Then $t \mapsto K t$ is a bijection from $\mathbb{R}^d$ onto $\ker S'$, and the rows of $K$ in $F$ form the identity matrix. So

$$C' = \{K t : t \in P\}, \qquad P = \{t \in \mathbb{R}^d : K t \ge 0\},$$

and $P$ is pointed, since its constraints contain $t \ge 0$. The coordinate $x_i = K_i t$ is 0 exactly when constraint $i$ is tight. The code keeps every ray as the vector $x = K t \in \mathbb{R}^{m'}$, so the tight set of a ray is its zero set, and all operations below are linear, so they commute with $t \mapsto K t$.

**Lemma 3 (extreme rays by rank).** Let $P = \{t : A t \ge 0\}$ be pointed, with $\operatorname{rank} A = d$. A non-zero $t \in P$ spans an extreme ray of $P$ if and only if $\operatorname{rank} A_{Z(t)} = d - 1$. A ray is extreme in $C'$ if and only if its support is minimal, so the extreme rays of $C'$ are its EFMs.

*Proof.* The set $\{u \in P : A_{Z(t)} u = 0\}$ is the smallest face of $P$ that contains $t$, and $t$ is in its relative interior. Its linear span is $\ker A_{Z(t)}$, because near $t$ every vector of $\ker A_{Z(t)}$ satisfies the other constraints strictly. So the face is the ray of $t$ if and only if $\ker A_{Z(t)}$ has dimension 1, that is, rank $d - 1$. For $C'$, with $A = K$, the tight set of $x = K t$ is the complement of its support $Q$, and $\dim \ker K_{Z} = \dim \{x \in \ker S' : x_i = 0 \text{ off } Q\} = \dim \ker S'_Q$. So $x$ is extreme if and only if $\dim \ker S'_Q = 1$, which is the EFM test of Lemma 1. $\square$

Call two extreme rays $r, r'$ of $P$ that are not multiples of each other *adjacent* if $\operatorname{rank} A_{Z(r) \cap Z(r')} = d - 2$. This is the test of line L8, where the rows are the rows of $K$ for the processed constraints on which both rays are zero.

**Lemma 4 (the double description step).** Let $P = \{t : A t \ge 0\}$ be pointed with $\operatorname{rank} A = d$, let $R$ hold one vector for each extreme ray of $P$, and let $h$ be a row vector. Split $R$ into $R^+$, $R^0$, $R^-$ by the sign of $h r$. Then the extreme rays of $P' = P \cap \{h t \ge 0\}$ are, each exactly once,

$$R^+ \;\cup\; R^0 \;\cup\; \{ (h r)\, r' - (h r')\, r \; : \; r \in R^+, \; r' \in R^-, \; r, r' \text{ adjacent in } P \} .$$

*Proof.* $P'$ is pointed and its matrix $A' = (A; h)$ has rank $d$. Write $Z'$ for tight sets in $P'$.

(a) Each $r \in R^+ \cup R^0$ is in $P'$, and $Z'(r) \supseteq Z(r)$, so $\operatorname{rank} A'_{Z'(r)} \ge d - 1$. All these rows vanish on $r \ne 0$, so the rank is at most $d - 1$. By Lemma 3, $r$ is extreme in $P'$.

(b) For adjacent $r \in R^+$ and $r' \in R^-$, let $w = (h r) r' - (h r') r = \alpha r' + \beta r$ with $\alpha = h r > 0$ and $\beta = -h r' > 0$. Then $w \in P$, $h w = 0$, and $w \ne 0$ since $r, r'$ are independent. For a row $a_i$ of $A$, $a_i w = \alpha a_i r' + \beta a_i r$ is a sum of two non-negative terms, so it is 0 if and only if $i \in Z(r) \cap Z(r')$. So $Z'(w) = (Z(r) \cap Z(r')) \cup \{h\}$. The kernel of $A_{Z(r) \cap Z(r')}$ has dimension 2 and contains $r$ and $r'$, so it is their span, and $h r \ne 0$ shows that $h$ is not a combination of these rows. So $\operatorname{rank} A'_{Z'(w)} = d - 1$, and $w$ is extreme in $P'$ by Lemma 3.

(c) Let $w$ be extreme in $P'$. If $h w > 0$, then $Z'(w) = Z(w)$, so $w$ is extreme in $P$ by Lemma 3, and $w \in R^+$. If $h w = 0$ and $w$ is extreme in $P$, then $w \in R^0$. Otherwise $h w = 0$, and $\operatorname{rank} A_{Z(w)} = d - 2$: it is at least $d - 2$ because adding the one row $h$ gives rank $d - 1$, and at most $d - 2$ because $w$ is not extreme in $P$. The face $G = \{u \in P : A_{Z(w)} u = 0\}$ of $P$ then has a two-dimensional span and is pointed, so it is the cone over two extreme rays $r_1, r_2$ of $G$, which are extreme rays of $P$ (a face of a face is a face). Their common tight set contains $Z(w)$, so its rank is at least $d - 2$, and at most $d - 2$ because both lie in its kernel; so they are adjacent. As $w$ is in the relative interior of $G$, $w = a r_1 + b r_2$ with $a, b > 0$. From $h w = 0$, either $h r_1 = h r_2 = 0$, but then $h$ vanishes on the span of $G$, so $h$ is a combination of the rows $A_{Z(w)}$ and $\operatorname{rank} A'_{Z'(w)} = d - 2$, a contradiction; or one of $h r_1, h r_2$ is positive and the other negative, say $h r_1 > 0 > h r_2$. In the plane spanned by $r_1, r_2$, the vectors of $G$ with $h u = 0$ form one ray, which contains both $w$ and $(h r_1) r_2 - (h r_2) r_1$. So $w$ is in the third set.

(d) No ray appears twice. The rays of $R^+ \cup R^0$ are distinct extreme rays of $P$, and the new rays are not extreme in $P$ (each is a positive combination of two independent rays). Two different adjacent pairs span two different two-dimensional faces of $P$, and each new ray lies in the relative interior of its face, so different pairs give different rays. $\square$

## Step 3: the loop

**Lemma 5 (the invariant).** Let $D_0 = F$ and let $D_s$ be $F$ plus the first $s$ pivot columns processed by line L4. After $s$ rounds of the loop, the list rays holds exactly one vector $K t$ for each extreme ray of $P_s = \{t : K_i t \ge 0 \text{ for } i \in D_s\}$.

*Proof.* By induction on $s$. For $s = 0$, $P_0 = \{t \ge 0\}$, the orthant, whose extreme rays are the unit vectors $e_b$, and $K e_b$ is the kernel basis vector $b$ of line L3. Each $P_s$ is pointed and its matrix has rank $d$, because it contains the identity rows of $F$. For the step from $s$ to $s + 1$ with pivot $p$, the new constraint is $h = K_p$, and $h t = x_p$ for the stored vector $x = K t$. Line L5 splits the rays by the sign of $x_p$. Lines L7 and L8 test each pair of a positive and a negative ray for adjacency in $P_s$: the rows $K_i$ for $i \in D_s$ with $x_i = 0$ and $y_i = 0$ are $A_{Z(r) \cap Z(r')}$, and the code compares their rank with $d - 2$. (The test that skips pairs with fewer than $d - 2$ common zeros only saves time, since fewer rows cannot have rank $d - 2$.) For an adjacent pair, line L7 forms $a_p\, y - b_p\, x$ with $a_p > 0 > b_p$, which is the vector $(h r) r' - (h r') r$ of Lemma 4. Line L9 keeps $R^+ \cup R^0$ and the new vectors. By Lemma 4 this is exactly one vector for each extreme ray of $P_{s+1}$. $\square$

**Theorem.** efm_enumeration returns the sorted list of the EFMs of $C$, each exactly once, as the primitive integer vector of its ray.

*Proof.* If $d = 0$, then $\ker S' = \{0\}$, so $C' = \{0\}$, $C = \varphi(C') = \{0\}$ has no EFMs, and the code returns the empty list. Otherwise, after the last pivot, $D = F \cup \Pi$ is all coordinates, so $P = \{t : K t \ge 0\}$ and $K P = C'$. By Lemma 5 the list holds one vector for each extreme ray of $C'$, and by Lemma 3 these are the EFMs of $C'$. Line L10 drops the two-cycles and maps the others by $\varphi$; by Lemma 2 this gives each EFM of $C$ exactly once, up to a positive factor. The function primitive divides by the positive gcd after clearing denominators, so it keeps the sign and maps each ray to one integer vector, and the set removes nothing that is not a repeat. $\square$

**Remark (signs and reversible modes).** A mode $e$ whose support has only reversible reactions gives two EFMs, $e$ and $-e$, which are different rays of $C$. They come from two different extreme rays of $C'$, one on the forward copies and one on the backward copies, so both are returned.
