---
title: The value of a coalition and the Shapley and Banzhaf values of an MC-net
proves: [correctness]
status: full
---

An MC-net on the players $N = \{1, \ldots, n\}$ is a list $R$ of rules $r = (P, Q, x)$, where $P \subseteq N$ is nonempty, $Q \subseteq N$ is disjoint from $P$ and $x$ is a number. The rule applies to $S$ if $P \subseteq S$ and $Q \cap S = \emptyset$. The game of the net is $v_R(S) = \sum_{r \in R} v_r(S)$, where $v_r(S) = x$ if $r$ applies to $S$ and $v_r(S) = 0$ if not. Since $P \neq \emptyset$, no rule applies to $\emptyset$, so $v_R(\emptyset) = 0$ and $v_R$ is a TU game.

**Lemma (VALUE).** VALUE$(R, S)$ returns $v_R(S)$.

*Proof.* Line L1 sets $total = 0$. The loop of line L2 visits each rule once, and line L3 adds $x$ exactly when the rule applies to $S$. So after the loop, $total = \sum_r v_r(S) = v_R(S)$, which line L4 returns. $\square$

**Lemma (one rule).** Let $r = (P, Q, x)$ with $a = |P|$ and $b = |Q|$. The Shapley value of the game $v_r$ is
$$\varphi_i(v_r) = x \frac{(a-1)!\, b!}{(a+b)!} \text{ for } i \in P, \qquad \varphi_j(v_r) = -x \frac{a!\, (b-1)!}{(a+b)!} \text{ for } j \in Q,$$
and $\varphi_k(v_r) = 0$ for $k \notin P \cup Q$. The raw Banzhaf value is $\beta_i(v_r) = x / 2^{a+b-1}$ for $i \in P$, $\beta_j(v_r) = -x / 2^{a+b-1}$ for $j \in Q$, and 0 for the other players.

*Proof.* We use the order form of the Shapley value: $\varphi_i(v)$ is the mean over the $n!$ orders $\pi$ of $v(P_i^\pi \cup \{i\}) - v(P_i^\pi)$, where $P_i^\pi$ is the set of the players before $i$ in $\pi$.

A player $k \notin P \cup Q$ does not change whether the rule applies, so $v_r(S \cup \{k\}) = v_r(S)$ for every $S$. Every marginal contribution of $k$ is 0.

Let $i \in P$ and let $B = P_i^\pi$. Since $i \in P$ and $i \notin B$, the rule does not apply to $B$, so $v_r(B) = 0$. The rule applies to $B \cup \{i\}$ if and only if $P \setminus \{i\} \subseteq B$ and $Q \cap B = \emptyset$. So the marginal contribution is $x$ if, in $\pi$, all the other players of $P$ come before $i$ and all the players of $Q$ come after $i$, and 0 if not. This event depends only on the relative order of the $a + b$ players of $P \cup Q$, which is uniform over the $(a+b)!$ orders of these players when $\pi$ is uniform. The orders in the event put $P \setminus \{i\}$ in the first $a - 1$ places in any order, $i$ in place $a$, and $Q$ in the last $b$ places in any order. There are $(a-1)!\, b!$ of them, which gives the first formula.

Let $j \in Q$ and $B = P_j^\pi$. The rule does not apply to $B \cup \{j\}$, because $j \in Q$. It applies to $B$ if and only if $P \subseteq B$ and $(Q \setminus \{j\}) \cap B = \emptyset$. So the marginal contribution is $-x$ if all of $P$ comes before $j$ and all of $Q \setminus \{j\}$ comes after $j$, and 0 if not. The same count gives $a!\, (b-1)!$ orders out of $(a+b)!$.

For the Banzhaf value of $i \in P$, the marginal contribution to $S \subseteq N \setminus \{i\}$ is $x$ if $P \setminus \{i\} \subseteq S$ and $Q \cap S = \emptyset$, and 0 if not. Such a set $S$ contains the $a - 1$ fixed players, avoids the $b$ fixed players and is free on the other $n - a - b$ players, so there are $2^{n-a-b}$ of them. Divided by $2^{n-1}$, this gives $x / 2^{a+b-1}$. For $j \in Q$, the sets $S$ with marginal $-x$ contain $P$ and avoid $Q \setminus \{j\}$, which again fixes $a + b - 1$ players and leaves $2^{n-a-b}$ sets. $\square$

**Theorem (SHAPLEY and BANZHAF).** SHAPLEY$(R, n)$ returns $\varphi(v_R)$, and BANZHAF$(R, n)$ returns the raw Banzhaf values $\beta(v_R)$.

*Proof.* Both values are linear in the game: the order form and the subset form are sums of terms $v(T)$ with coefficients that do not depend on $v$. So $\varphi(v_R) = \sum_{r \in R} \varphi(v_r)$ and $\beta(v_R) = \sum_{r \in R} \beta(v_r)$. Line L5 sets each $\varphi_i$ to 0. The loop of line L6 visits each rule once, and lines L7 to L10 add the terms of the one-rule lemma for the players in $P$ and in $Q$. Players outside $P \cup Q$ get 0 from the rule, so they need no update. After the loop, $\varphi_i$ is the sum of the contributions of all rules, which line L11 returns. Lines L12 to L17 do the same for the Banzhaf value with the term $x / 2^{a+b-1}$ of line L14. $\blacksquare$

**Check of efficiency.** For one rule with $b \ge 1$, the Shapley values sum to $a \cdot x \frac{(a-1)!\,b!}{(a+b)!} - b \cdot x \frac{a!\,(b-1)!}{(a+b)!} = 0 = v_r(N)$, since $Q \cap N \ne \emptyset$. For $b = 0$, they sum to $a \cdot x/a = x = v_r(N)$.

**Lemma (from a table).** For every TU game $v$ on $N$, the rules $(T, \emptyset, d_T)$ with $d_T = \sum_{S \subseteq T} (-1)^{|T| - |S|} v(S)$, over the nonempty $T$ with $d_T \ne 0$, form an MC-net with $v_R = v$.

*Proof.* The rule $(T, \emptyset, d_T)$ applies to $S$ if and only if $T \subseteq S$, so $v_R(S) = \sum_{\emptyset \ne T \subseteq S} d_T$. By Möbius inversion on the lattice of subsets, $\sum_{T \subseteq S} d_T = v(S)$ for every $S$, and $d_\emptyset = v(\emptyset) = 0$. So $v_R(S) = v(S)$. $\square$
