---
title: KERNELS lists each kernel pair once, and each extraction keeps the functions and saves its value
proves: [correctness]
status: full
---

Cubes are sets of literals with at most one literal of each variable, and an SOP is a set of cubes. Fix an SOP $F$ with at least two cubes and the order $l_0 < l_1 < \cdots$ of its literals. For a cube $c$ let $S(c) = \{x \in F : c \subseteq x\}$, and when $S(c) \neq \emptyset$ let $\mathrm{cl}(c) = \bigcap S(c)$. Then $c \subseteq \mathrm{cl}(c)$, $\mathrm{cl}$ is monotone, $S(\mathrm{cl}(c)) = S(c)$, so $\mathrm{cl}(\mathrm{cl}(c)) = \mathrm{cl}(c)$, and $\mathrm{cl}(a \cup b) = \mathrm{cl}(\mathrm{cl}(a) \cup b)$, because $S(a \cup b) = S(a) \cap S(b) = S(\mathrm{cl}(a)) \cap S(b)$. Call $c$ *closed* if $\mathrm{cl}(c) = c$. Write $P_i(c) = c \cap \{l_0, \ldots, l_i\}$, with $P_{-1}(c) = \emptyset$, and $c_0 = \mathrm{cl}(\emptyset)$, the common cube of $F$.

**Lemma 1 (cokernels are closed cubes).** $F / c$ is a kernel exactly when $|S(c)| \ge 2$ and $c$ is closed.

*Proof.* $F / c = \{x \setminus c : x \in S(c)\}$, and $x \mapsto x \setminus c$ is one to one on $S(c)$, so $|F / c| = |S(c)|$. The common cube of $F / c$ is $\mathrm{cl}(c) \setminus c$. So $F / c$ is cube-free, with two or more cubes and no common literal, exactly when $|S(c)| \ge 2$ and $\mathrm{cl}(c) = c$. $\square$

**Lemma 2 (what a call holds).** Each call KERNELS$(g, p, j)$ has $g = F / p$, $p$ closed, $|S(p)| \ge 2$, and $\mathrm{cl}(c_0 \cup P_{j-1}(p)) = p$.

*Proof.* The first call has $p = c_0$, $g = F / c_0$ and $j = 0$, and $c_0$ is closed with $S(c_0) = F$. Suppose the claim holds for a call $(g, p, j)$, and line L5 runs at $i \ge j$. The cubes of $g$ that contain $l_i$ are $x \setminus p$ for $x \in S(p \cup \{l_i\})$, at least two of them by line L2, and their intersection is $C = \mathrm{cl}(p \cup \{l_i\}) \setminus p$. So the child has $c = p \cup C = \mathrm{cl}(p \cup \{l_i\})$, which is closed, $|S(c)| \ge 2$, and $g / C = F / c$. By line L4, $C$ has no literal of index below $i$, so $P_i(c) = P_i(p) \cup \{l_i\}$. Then $\mathrm{cl}(c_0 \cup P_i(c)) \supseteq \mathrm{cl}(c_0 \cup P_{j-1}(p) \cup \{l_i\}) = \mathrm{cl}(p \cup \{l_i\}) = c$, and it is at most $\mathrm{cl}(c) = c$. So the child call $(F / c, c, i + 1)$ satisfies the claim. $\square$

For a closed cube $c \neq c_0$, every closed cube contains $c_0$, and we let $i(c)$ be the least index $i$ with $\mathrm{cl}(c_0 \cup P_i(c)) = c$, which exists because $\mathrm{cl}(c) = c$, and $p(c) = \mathrm{cl}(c_0 \cup P_{i(c)-1}(c))$. Then $p(c) \subseteq c$ and $p(c) \neq c$. Also $l_{i(c)} \in c$ and $l_{i(c)} \notin p(c)$, since otherwise $p(c) \supseteq c_0 \cup P_{i(c)}(c)$ and $p(c) = c$. Since $P_{i(c)-1}(c) \subseteq p(c) \subseteq c$, we get $P_{i(c)-1}(p(c)) = P_{i(c)-1}(c)$ and $\mathrm{cl}(p(c) \cup \{l_{i(c)}\}) = c$.

**Lemma 3 (parent and index).** If a call with cokernel $q$ makes a call with cokernel $c$ at index $i^*$, then $i^* = i(c)$ and $q = p(c)$.

*Proof.* Let the call be $(F / q, q, j)$ with $j \le i^*$. Then $c = \mathrm{cl}(q \cup \{l_{i^*}\})$, and $c \setminus q$ has no literal of index below $i^*$. By Lemma 2, $\mathrm{cl}(c_0 \cup P_{j-1}(q)) = q$. For $k < i^*$, $P_k(c) = P_k(q)$, so $\mathrm{cl}(c_0 \cup P_k(c)) \subseteq q \neq c$. The proof of Lemma 2 gives $\mathrm{cl}(c_0 \cup P_{i^*}(c)) = c$. So $i^* = i(c)$. Further $q = \mathrm{cl}(c_0 \cup P_{j-1}(q)) \subseteq \mathrm{cl}(c_0 \cup P_{i^*-1}(q)) \subseteq \mathrm{cl}(q) = q$, so $q = \mathrm{cl}(c_0 \cup P_{i^*-1}(c)) = p(c)$. $\square$

**Lemma 4 (every cokernel once).** For each closed $c$ with $|S(c)| \ge 2$, exactly one call has cokernel $c$.

*Proof.* For $c = c_0$ it is the first call, and no other call has cokernel $c_0$, since a child cokernel contains a literal $l_i$ that is not in its parent and so is larger than $c_0$. Let $c \neq c_0$, $i = i(c)$ and $p = p(c)$, and use induction on $|c|$.

*Existence.* The cube $p$ is closed with $S(p) \supseteq S(c)$ and $|p| < |c|$, so some call $(F / p, p, j)$ exists. If $p = c_0$, then $j = 0 \le i$. Otherwise this call was made at index $i(p)$ by Lemma 3, so $j = i(p) + 1$, and $i(p) \le i - 1$ because $\mathrm{cl}(c_0 \cup P_{i-1}(p)) = \mathrm{cl}(c_0 \cup P_{i-1}(c)) = p$. So $j \le i$. At index $i$, line L2 passes since $|S(p \cup \{l_i\})| = |S(c)| \ge 2$, and $C = c \setminus p$ has no literal $l_k$ with $k < i$, since such a literal is in $P_{i-1}(c) \subseteq p$. So line L5 makes a call with cokernel $c$.

*Uniqueness.* By Lemma 3, every call with cokernel $c$ is made by a call with cokernel $p$ at index $i$. By induction there is one call with cokernel $p$, and it makes at most one call at index $i$. $\square$

**Theorem 1.** KERNELS$(F / c_0, c_0, 0)$ outputs each pair $(c, F / c)$ with $F / c$ a kernel exactly once.

*Proof.* Line L6 outputs one pair for each call, and by Lemma 2 its quotient is a kernel by Lemma 1. By Lemmas 1 and 4, each kernel pair has exactly one call. $\square$

**Theorem 2.** Each step of lines L10 to L12 keeps the function of every old node, makes no cycle, and lowers the total number of literals by exactly value$(R, C)$. EXTRACT ends.

*Proof.* Every column $k \in C$ lies in the kernel $F_v / c$ of each row $(v, c) \in R$, so $c \cup k \in F_v$ and $c$ shares no variable with $k$. For a node $v$, let $U_v = \{c \cup k : (v, c) \in R, k \in C\}$, the cubes that line L12 removes from $F_v$, all of them in $F_v$. The new $F_v$ is $(F_v \setminus U_v) \cup \{c \cup \{x\} : (v, c) \in R\}$. Substituting $F_x = \bigvee_{k \in C} k$ for $x$ turns $c \wedge x$ into $\bigvee_{k \in C} (c \wedge k)$, so the new $F_v$ has the function $\bigvee (F_v \setminus U_v) \vee \bigvee U_v = F_v$, and every node keeps its function by induction along the network. The variables of $F_x$ occur in cubes of every rewritten node, so they are fanins of each of these nodes, and none of them depends on a node that it feeds, so adding the edges from $x$ makes no cycle. The literals removed are $\sum_v \sum_{q \in U_v} |q|$, the cubes added have $\sum_{(v, c) \in R} (|c| + 1)$ literals, since $x$ is a new variable and the new cubes differ for different rows of one node, and $F_x$ has $\sum_{k \in C} |k|$ literals. The change is $-\mathrm{value}(R, C)$. Line L9 accepts only a positive value, so each step lowers the nonnegative integer literal count by at least 1, and the loop ends. $\blacksquare$
