---
title: Proof of the edit distance hardness theorem
proves: [statement]
status: full
---

Positions in strings are numbered from 1 in this proof, and coordinates of vectors also from 1. For a symbol $\gamma$ and an integer $h \ge 0$, $\gamma^h$ is the string of $h$ copies of $\gamma$. The distance $\mathrm{ed}$ is the Levenshtein distance with unit costs.

## Alignments and gain

An **alignment** of strings $x$ and $y$ is a set of pairs $(i, j)$ with $1 \le i \le |x|$ and $1 \le j \le |y|$, such that no two pairs share an $i$ or a $j$, and for any two pairs $(i, j)$ and $(i', j')$, $i < i'$ holds if and only if $j < j'$. A pair is **equal** when $x[i] = y[j]$ and **unequal** otherwise. A symbol in no pair is **unpaired**. The **cost** of the alignment is the number of unpaired symbols of $x$ and $y$ plus the number of unequal pairs. Each unpaired symbol and each unequal pair is one **unit** of cost.

**Lemma 1.** $\mathrm{ed}(x, y)$ is the least cost of an alignment of $x$ and $y$. If an alignment has $\pi$ pairs, of which $\mu$ are equal, its cost is $|x| + |y| - (\pi + \mu)$.

*Proof.* Given an alignment, delete the unpaired symbols of $x$, substitute $y[j]$ for $x[i]$ in each unequal pair, and insert the unpaired symbols of $y$. Because the pairs are in the same order in both strings, this turns $x$ into $y$ with as many operations as the cost. Conversely, take a sequence of $c$ operations that turns $x$ into $y$, and follow each symbol of $x$ through it. Pair $x[i]$ with $y[j]$ when the symbol at position $i$ of $x$ is never deleted and ends at position $j$ of $y$. Insertions, deletions and substitutions keep the order of the symbols that they do not remove, so this is an alignment. Each unpaired symbol of $x$ was deleted, each unpaired symbol of $y$ comes from an insertion, and the symbol of each unequal pair was substituted at least once. These are distinct operations, so the cost of the alignment is at most $c$. For the formula: there are $|x| - \pi$ unpaired symbols in $x$, $|y| - \pi$ in $y$ and $\pi - \mu$ unequal pairs, and the sum is $|x| + |y| - \pi - \mu$. $\square$

Call $\pi + \mu$ the **gain** of the alignment: each pair gains 1, and 2 when it is equal. Let $g(x, y) = |x| + |y| - \mathrm{ed}(x, y)$, the largest gain of an alignment of $x$ and $y$. Lemma 1 turns each lower bound on $\mathrm{ed}$ into an upper bound on the gain. Reversing both strings maps alignments to alignments with the same pairs read backwards, so $\mathrm{ed}$ and $g$ do not change under the reversal of both arguments.

The next fact is used many times. Let $(i_1, j_1)$ and $(i_2, j_2)$ be pairs of an alignment with $i_1 < i_2$, so $j_1 < j_2$.

**(B)** A symbol of $y$ at a position strictly between $j_1$ and $j_2$ is unpaired or paired with a position of $x$ strictly between $i_1$ and $i_2$. The same holds with the roles of $x$ and $y$ exchanged.

This follows from the definition: a pair $(i, j)$ with $j_1 < j < j_2$ needs $i_1 < i < i_2$.

## From SETH to orthogonal vectors

**Lemma 2.** If there are constants $\delta > 0$ and $c$ and an algorithm that solves OV with $n$ vectors of dimension $d$ on each side in time $O(n^{2-\delta} d^c)$, then SETH is false.

*Proof.* A smaller $\delta$ gives a weaker assumption, so we may assume $\delta \le 1$. Let $\varepsilon = \delta / 4$ and let $k$ be any integer. Take a $k$-CNF formula $\varphi$ with $\nu$ variables. Add one unused variable if $\nu$ is odd, and remove repeated clauses. A clause is a set of at most $k$ literals out of $2\nu$, so there are $\kappa \le (2\nu + 1)^k$ clauses. Split the variables into two halves $V_1$ and $V_2$ of size $\nu / 2$. For each assignment $\alpha$ of $V_1$, let $u_\alpha \in \{0, 1\}^\kappa$ have coordinate $r$ equal to 0 when some literal of clause $r$ on a variable of $V_1$ is true under $\alpha$, and 1 otherwise. Define $w_\beta$ in the same way for each assignment $\beta$ of $V_2$. Then $u_\alpha \cdot w_\beta = 0$ if and only if each clause has a literal that is true under $\alpha$ or under $\beta$, that is, if and only if the joint assignment satisfies $\varphi$. So $\varphi$ is satisfiable if and only if the OV instance with the $n = 2^{\nu/2}$ vectors $u_\alpha$ and the $n$ vectors $w_\beta$ has an orthogonal pair. Building the instance takes $O(n \kappa k)$ time, and the algorithm takes $O(n^{2-\delta} \kappa^c) = O(2^{(1 - \delta/2)\nu} (2\nu + 1)^{kc})$. For fixed $k$, $(2\nu + 1)^{kc} \le 2^{\delta \nu / 4}$ for all large $\nu$, so the total time is $O(2^{(1 - \varepsilon)\nu})$. This holds for every $k$, which contradicts SETH for this $\varepsilon$. $\square$

## Coordinate gadgets

Fix $t \ge 1$. The alphabet has distinct symbols $\sigma_{\ell, 0}$, $\sigma_{\ell, 1}$ and $\tau_\ell$ for $1 \le \ell \le t$. For $u, w \in \{0, 1\}^t$ let

$$ L(u) = \sigma_{1, u_1} \sigma_{2, u_2} \cdots \sigma_{t, u_t}, \qquad Q(w) = \beta_1(w_1) \beta_2(w_2) \cdots \beta_t(w_t), $$

where the block $\beta_\ell(0) = \sigma_{\ell, 0} \sigma_{\ell, 1}$ and $\beta_\ell(1) = \sigma_{\ell, 0} \tau_\ell$. So $|L(u)| = t$ and $|Q(w)| = 2t$.

**Lemma 3.** $\mathrm{ed}(L(u), Q(w)) = t + u \cdot w$.

*Proof.* The symbol $\sigma_{\ell, u_\ell}$ at position $\ell$ of $L(u)$ occurs in $Q(w)$ only in block $\ell$, and it occurs there exactly when $u_\ell = 0$ or $w_\ell = 0$, that is, when $u_\ell w_\ell = 0$. So an alignment has at most $t - u \cdot w$ equal pairs, and at most $t$ pairs, because $|L(u)| = t$. Its gain is at most $2t - u \cdot w$, and by Lemma 1 its cost is at least $3t - (2t - u \cdot w) = t + u \cdot w$. For the upper bound, pair position $\ell$ of $L(u)$ with the copy of $\sigma_{\ell, u_\ell}$ in block $\ell$ when there is one, and with the first symbol of block $\ell$ otherwise. The pairs are in increasing order in both strings, there are $t$ of them, and $t - u \cdot w$ are equal, so the gain is $2t - u \cdot w$ and the cost is $t + u \cdot w$. $\square$

## A gadget with two options

**Lemma 4.** Let $\alpha$ and $\beta$ be two symbols, and let $L$, $R$ and $D$ be strings that contain neither of them, with $|L| = |R| = p$ and $|D| = q$. Let $h \ge 2q$, and

$$ X = \alpha^h L \beta^h R \alpha^h, \qquad Y = \beta^h D \beta^h. $$

Then $\mathrm{ed}(X, Y) = 2h + p + \min(\mathrm{ed}(L, D), \mathrm{ed}(R, D))$.

*Proof.* Name the parts $X = Z_1 L V_0 R Z_2$ and $Y = V_1 D V_2$, with $Z_1 = Z_2 = \alpha^h$ and $V_0 = V_1 = V_2 = \beta^h$. Then $|X| = 3h + 2p$ and $|Y| = 2h + q$.

*Upper bound.* Pair $Z_1$ with $V_1$ symbol by symbol ($h$ unequal pairs), align $L$ with $D$ at cost $\mathrm{ed}(L, D)$, pair $V_0$ with $V_2$ ($h$ equal pairs), and leave $R$ and $Z_2$ unpaired ($p + h$ units). The cost is $2h + p + \mathrm{ed}(L, D)$. In the same way, leaving $Z_1$ and $L$ unpaired, pairing $V_0$ with $V_1$, $R$ with $D$ and $Z_2$ with $V_2$ costs $2h + p + \mathrm{ed}(R, D)$.

*Lower bound.* By Lemma 1 it suffices to show that each alignment has gain at most $3h + \max(g(L, D), g(R, D))$, since then the cost is at least $(5h + 2p + q) - 3h - (p + q) + \min(\mathrm{ed}(L, D), \mathrm{ed}(R, D))$. Fix an alignment. Each pair has its $Y$ end in $V_1 \cup V_2$ or in $D$. Let $\Gamma_V$ be the gain of the pairs with their $Y$ end in $V_1 \cup V_2$, and $\Gamma_D$ the gain of the pairs with their $Y$ end in $D$. The only symbols $\beta$ of $X$ are in $V_0$, so an equal pair with its $Y$ end in $V_1 \cup V_2$ has its $X$ end in $V_0$. There are three cases.

*Case 1: $D$ has a partner in $Z_1 L$ and a partner in $R Z_2$.* All of $V_0$ lies strictly between these two partners, so by (B) each symbol of $V_0$ is unpaired or paired with a symbol of $D$. So no pair with its $Y$ end in $V_1 \cup V_2$ is equal, and $\Gamma_V \le 2h$. Each symbol of $D$ gains at most 2, so $\Gamma_D \le 2q \le h$. The gain is at most $3h$.

*Case 2: $D$ has no partner in $R Z_2$.* The partners of $D$ lie in $Z_1$, $L$ and $V_0$. Let $k_Z$ and $k_V$ be the numbers of pairs between $D$ and $Z_1$, and between $D$ and $V_0$. Each of these pairs is unequal and gains 1. The pairs between $L$ and $D$ form an alignment of $L$ and $D$, so they gain at most $g(L, D)$. So $\Gamma_D \le g(L, D) + k_Z + k_V$. Now bound $\Gamma_V$. The number of equal pairs that it counts is at most $h - k_V$, because only symbols of $V_0$ can be their $X$ ends and $k_V$ symbols of $V_0$ are paired with $D$. The number of pairs that it counts is $2h - e$, where $e$ is the number of unpaired symbols of $V_1 V_2$. If $k_Z > 0$, let $s$ be the smallest position in $Z_1$ of a symbol paired with $D$. All of $V_1$ comes before $D$ in $Y$, so a symbol of $V_1$ can only be paired with one of the $s - 1$ symbols of $Z_1$ before position $s$. So at least $h - s + 1$ symbols of $V_1$ are unpaired, while $k_Z \le h - s + 1$. So $e \ge k_Z$, which also holds when $k_Z = 0$. Hence $\Gamma_V \le (2h - k_Z) + (h - k_V)$, and the gain is $\Gamma_V + \Gamma_D \le 3h + g(L, D)$.

*Case 3: $D$ has no partner in $Z_1 L$.* Reverse both strings. The reversed $X$ is $\alpha^h R' \beta^h L' \alpha^h$ and the reversed $Y$ is $\beta^h D' \beta^h$, where $'$ denotes reversal. The reversed alignment is in Case 2 for these strings, with $R'$ in the place of $L$. So its gain, which is the same as before, is at most $3h + g(R', D') = 3h + g(R, D)$.

Each alignment is in at least one of the three cases, because an alignment that is not in Case 1 has no partner of $D$ in $Z_1 L$ or none in $R Z_2$. Since $g \ge 0$, each case gives a gain of at most $3h + \max(g(L, D), g(R, D))$. $\square$

## Vector gadgets

Let $d \ge 1$, $t = d + 1$ and $h = 4t$. For $a \in \{0, 1\}^d$ let $\hat a = (0, a_1, \ldots, a_d)$, for $b \in \{0, 1\}^d$ let $\hat b = (1, b_1, \ldots, b_d)$, and let $e_1 = (1, 0, \ldots, 0) \in \{0, 1\}^t$ and $1^t = (1, \ldots, 1)$. Define

$$ G_1(a) = \alpha^h L(\hat a) \beta^h L(e_1) \alpha^h, \qquad G_2(w) = \beta^h Q(w) \beta^h \quad (w \in \{0, 1\}^t). $$

So $|G_1(a)| = 3h + 2t = 14t$ and $|G_2(w)| = 2h + 2t = 10t$. Let $E_s = 10t$ and $E_u = 10t + 1$.

**Lemma 5.** For all $a, b \in \{0, 1\}^d$: $\mathrm{ed}(G_1(a), G_2(\hat b)) = E_s$ if $a \cdot b = 0$ and $E_u$ otherwise, and $\mathrm{ed}(G_1(a), G_2(1^t)) = E_s$ if $a$ is the zero vector and $E_u$ otherwise.

*Proof.* Apply Lemma 4 with $L = L(\hat a)$, $R = L(e_1)$, $D = Q(w)$, $p = t$ and $q = 2t$. These strings contain no $\alpha$ or $\beta$, and $h = 4t = 2q$. With Lemma 3, $\mathrm{ed}(G_1(a), G_2(w)) = 2h + t + \min(t + \hat a \cdot w, t + e_1 \cdot w) = 10t + \min(\hat a \cdot w, w_1)$. For $w = \hat b$: $\hat a \cdot \hat b = a \cdot b$ and $w_1 = 1$. For $w = 1^t$: $\hat a \cdot 1^t$ is the number of ones of $a$, and $w_1 = 1$. $\square$

## The pattern distance

For strings $P$ and $T$, let $\mathrm{pd}(P, T)$ be the least value of $\mathrm{ed}(P, T')$ over all substrings $T'$ of $T$, the empty one included.

Let $A = (a_1, \ldots, a_n)$ and $B = (b_1, \ldots, b_n)$ be an OV instance in dimension $d$. Let $\#$ be a new symbol and $H = E_u$. Let $K_i = G_1(a_i)$ for $1 \le i \le n$. Let $c_1, \ldots, c_{3n-2}$ be the vectors $1^t$ ($n - 1$ times), $\hat b_1, \ldots, \hat b_n$, then $1^t$ ($n - 1$ times), so $c_{n - 1 + j} = \hat b_j$, and let $L_j = G_2(c_j)$. Define

$$ P = \#^H K_1 \#^{2H} K_2 \#^{2H} \cdots \#^{2H} K_n \#^H, \qquad T = \prod_{j=1}^{3n-2} \#^H L_j \#^H. $$

The strings $K_i$ and $L_j$ are the **cores**. The runs of $\#$ in $P$ are $\rho_0$ (before $K_1$), $\rho_i$ between $K_i$ and $K_{i+1}$, and $\rho_n$ (after $K_n$). Each has at least $H$ symbols, and $\rho_1, \ldots, \rho_{n-1}$ have $2H$. Between $L_j$ and $L_{j+1}$ the text has a run of $2H$ symbols $\#$. No core contains $\#$.

**Lemma 6.** If $a_i \cdot b_j = 0$ for some $i$ and $j$, then $\mathrm{pd}(P, T) \le n E_u - 1$. If $a_i \cdot b_j \ge 1$ for all $i$ and $j$, then $\mathrm{pd}(P, T) \ge n E_u$.

*Proof of the first claim.* Let $s = n - 1 + j - i$. Then $0 \le s$ and $s + n \le 3n - 2$, because $1 \le i, j \le n$. Let $T'$ be the substring $\prod_{r=1}^{n} \#^H L_{s+r} \#^H$ of $T$. It has the same runs of $\#$ as $P$, with $L_{s+r}$ in the place of $K_r$. Pair the runs of $\#$ symbol by symbol, at no cost, and align each $K_r$ with $L_{s+r}$ optimally. The cost is $\sum_{r=1}^n \mathrm{ed}(K_r, L_{s+r})$. By Lemma 5 each term is at most $E_u$, and the term for $r = i$ is $\mathrm{ed}(G_1(a_i), G_2(\hat b_j)) = E_s = E_u - 1$, since $s + i = n - 1 + j$. $\square$

*Proof of the second claim.* No $a_i$ is the zero vector, since otherwise $a_i \cdot b_1 = 0$. So by Lemma 5, $\mathrm{ed}(K_i, L_j) = E_u$ for all $i$ and $j$. Fix a substring $T'$ of $T$ and an alignment of $P$ with $T'$. A core $K_i$ **touches** $L_j$ when a symbol of $K_i$ is paired with a symbol of $L_j$. For each $j$, let $I_j$ be the set of $i$ such that $K_i$ touches $L_j$.

*Order.* If $i < i'$, $K_i$ touches $L_j$ and $K_{i'}$ touches $L_{j'}$, then $j \le j'$, because the pairs are in the same order in both strings. Hence, if $I_j$ and $I_{j'}$ are nonempty and $j < j'$, then $\max I_j \le \min I_{j'}$.

Sort each core $K_i$ into one class:

- **(C0)** $K_i$ touches no core.
- **(C2)** $K_i$ touches at least two cores.
- **(C1)** $K_i$ touches exactly one core $L_j$. It is **clean** if $I_j = \{i\}$ and all of $L_j$ lies inside $T'$, **cut** if $I_j = \{i\}$ and some symbol of $L_j$ is outside $T'$, and **shared** if $|I_j| \ge 2$.

We now give sets of units, pairwise disjoint, that together contain at least $n E_u$ units.

*(C0).* Let $U_i$ hold the unpaired symbols of $K_i$ and the pairs with an end in $K_i$. Such a pair has its other end in a $\#$ of $T'$, because $K_i$ touches no core, so it is unequal. So $|U_i| = |K_i| = 14t \ge E_u$.

*(C2).* Let $K_i$ touch $L_j$ and $L_{j'}$ with $j < j'$. The run of $2H$ symbols $\#$ between $L_j$ and $L_{j+1}$ lies strictly between a partner of $K_i$ in $L_j$ and a partner of $K_i$ in $L_{j'}$, so it lies inside $T'$. By (B), each of its symbols is unpaired or paired with a symbol of $K_i$, which is not $\#$. Let $U_i$ hold these $2H$ units. So $|U_i| = 2H \ge E_u$.

*Clean (C1).* Let $U_i$ hold the unpaired symbols of $K_i$ and of $L_j$, and the unequal pairs with an end in $K_i$ or in $L_j$. A pair with an end in $K_i$ has its other end in $L_j$ or in a $\#$, since $K_i$ touches only $L_j$. A pair with an end in $L_j$ has its other end in $K_i$ or in a $\#$ of $P$, since $I_j = \{i\}$. Drop the pairs with an end in a $\#$. The pairs between $K_i$ and $L_j$ that remain form an alignment of $K_i$ with $L_j$, which is whole inside $T'$. Its cost counts the unpaired symbols of $K_i$ and $L_j$, the symbols of $K_i$ and $L_j$ that were paired with a $\#$, and the unequal pairs between $K_i$ and $L_j$. Each of these is one unit of $U_i$, counted once. So $|U_i| \ge \mathrm{ed}(K_i, L_j) = E_u$.

*Shared (C1).* For each $j$ with $|I_j| \ge 2$, let $p = \min I_j < q = \max I_j$. The runs $\rho_p, \ldots, \rho_{q-1}$ lie strictly between a symbol of $K_p$ and a symbol of $K_q$ whose partners are in $L_j$. By (B), each of their $2H(q - p)$ symbols is unpaired or paired with a symbol of $L_j$, which is not $\#$. Let $U^{(j)}$ hold these units. Each shared core whose touched core is $L_j$ has its index in $I_j \subseteq \{p, \ldots, q\}$, so there are at most $q - p + 1 \le 2(q - p)$ of them. So $|U^{(j)}| = 2H(q - p) \ge E_u$ times the number of these cores.

*Cut (C1).* Here $I_j = \{i\}$, $T'$ contains a symbol of $L_j$ and misses another one, so $T'$ starts or ends strictly inside $L_j$. Suppose that it starts inside $L_j$. Let $x_0$ be the first symbol of $K_i$ that has a partner, and $y_0$ its partner. Some symbol of $K_i$ has a partner in $L_j$, and that partner is at or after $y_0$, so $y_0$ lies in the part of $T'$ up to that partner, which is inside $L_j$. Each symbol of $\rho_{i-1}$ comes before $x_0$ in $P$, so its partner, if any, comes before $y_0$ in $T'$ and is a symbol of $L_j$. Let $U_i$ hold the $|\rho_{i-1}| \ge H = E_u$ units of the symbols of $\rho_{i-1}$. If $T'$ does not start inside $L_j$, it ends inside $L_j$, and the same argument with the last symbol of $K_i$ that has a partner gives $|\rho_i| \ge E_u$ units from $\rho_i$; let $U_i$ hold those.

*Disjointness.* Unpaired core symbols appear only in the sets of (C0) and clean cores, each for its own core, and the core $L_j$ of a clean $K_i$ is touched by no other core, so no other set holds it. Unpaired symbols $\#$ of $T$ appear only in (C2) sets. A run of $T$ in the set of $K_i$ lies strictly between two partners of $K_i$. If it also lay strictly between two partners of $K_{i'}$ with $i < i'$, then a partner of $K_i$ after the run would come before a partner of $K_{i'}$ before the run, against the order of the pairs. So two (C2) sets use different runs. Unpaired symbols $\#$ of $P$ appear only in shared and cut sets. By the order property, the index ranges $\{p, \ldots, q - 1\}$ of two shared sets are disjoint. A cut core $K_i$ with $I_j = \{i\}$ uses $\rho_{i-1}$ or $\rho_i$. If one of these were in the range of a shared set for $j'$, then $p \le i \le q$ for $p = \min I_{j'}$ and $q = \max I_{j'}$. If $i = p$ or $i = q$, then $K_i$ touches $L_{j'}$. If $p < i < q$, then by (B) every partner of $K_i$ lies strictly between two symbols of $L_{j'}$, so it is in $L_{j'}$ and again $K_i$ touches $L_{j'}$. Either way $j' = j$, which is impossible because $|I_j| = 1 < 2 \le |I_{j'}|$. At most one cut core uses the run before it, since $T'$ starts inside only one core, and at most one uses the run after it. If the first one is $K_i$ and the second is $K_{i-1}$, they would use the same run $\rho_{i-1}$. But $T'$ starts inside the core $L_j$ touched by $K_i$ and ends inside the core $L_{j'}$ touched by $K_{i-1}$, so $j \le j'$, and the order property gives $j' \le j$. Then $L_j$ is touched by both cores, against $|I_j| = 1$. Now the unequal pairs. A pair between a core $K_i$ and a $\#$ of $T$ appears only in the set of $K_i$. A pair between a core $L_j$ and a $\#$ of $P$ appears only in a clean set with this $L_j$, in $U^{(j)}$, or in a cut set with this $L_j$, and exactly one of these kinds can exist for a given $j$. A pair between two cores appears only in a clean set. So the sets are pairwise disjoint.

Every core is in one class, and each class gives at least $E_u$ units for each of its cores, so the cost of the alignment is at least $n E_u$. This holds for every $T'$ and every alignment, so $\mathrm{pd}(P, T) \ge n E_u$. $\square$

## Padding

**Lemma 7.** Let $P$ and $T$ be strings, let $\&$ be a symbol that occurs in neither, and let $m_0 \ge |T|$. Then $\mathrm{ed}(\&^{m_0} P \&^{m_0}, T) = 2 m_0 + \mathrm{pd}(P, T)$.

*Proof.* *Upper bound.* Let $T = y T' z$ with $\mathrm{ed}(P, T') = \mathrm{pd}(P, T)$. Pair the last $|y|$ symbols of the first run of $\&$ with $y$ and the first $|z|$ symbols of the second run with $z$, align $P$ with $T'$ optimally, and leave the other symbols $\&$ unpaired. Each of the $2 m_0$ symbols $\&$ is one unit, and nothing else costs more than the alignment of $P$ with $T'$.

*Lower bound.* Fix an alignment. Each symbol $\&$ is unpaired or in an unequal pair, so the symbols $\&$ give $2 m_0$ units. If no symbol of $P$ is paired, the $|P|$ symbols of $P$ give $|P| = \mathrm{ed}(P, \varepsilon) \ge \mathrm{pd}(P, T)$ more units. Otherwise, let $T'$ be the substring of $T$ from the first to the last partner of a symbol of $P$. By (B), the symbols of $T'$ are unpaired or paired with symbols of $P$, and the symbols of $P$ are unpaired or paired with symbols of $T'$. So the pairs between $P$ and $T'$ form an alignment of $P$ with $T'$, and its units are units of the whole alignment that do not involve $\&$. Its cost is at least $\mathrm{ed}(P, T') \ge \mathrm{pd}(P, T)$. $\square$

## Proof of the theorem

*Part 1.* Given the OV instance, build $P$ and $T$ as in Lemma 6, and let $X = \&^{|T|} P \&^{|T|}$, $Y = T$ and $\theta = 2|T| + n E_u$. By Lemmas 6 and 7, $\mathrm{ed}(X, Y) \le \theta - 1$ when there is an orthogonal pair, and $\mathrm{ed}(X, Y) \ge \theta$ otherwise. The lengths are $|T| = (3n - 2)(2H + 10t)$ and $|P| = n \cdot 14t + 2nH$ with $H = 10t + 1$ and $t = d + 1$, so $|X| = 2|T| + |P|$ and $|Y|$ are $O(nd)$, and the strings are written in $O(nd)$ time. The symbols are $\sigma_{\ell,0}, \sigma_{\ell,1}, \tau_\ell$ for $1 \le \ell \le t$, and $\alpha$, $\beta$, $\#$ and $\&$: $3t + 4 = 3d + 7$ in all.

*Part 2.* Suppose that an algorithm computes the edit distance of two strings of length at most $N$ over at most $N$ symbols in time $O(N^{2-\delta})$. Given an OV instance, build $X$, $Y$ and $\theta$ by part 1 and compare $\mathrm{ed}(X, Y)$ with $\theta$. Here $N = \max(|X|, |Y|) = O(nd)$ and $3d + 7 \le N$, so for $\delta \le 1$, which we may assume, the time is $O(nd + (nd)^{2-\delta}) = O(n^{2-\delta} d^2)$. By Lemma 2 with $c = 2$, SETH is false. $\blacksquare$
