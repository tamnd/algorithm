---
title: L* learns the minimal DFA with at most n equivalence queries
proves: [correctness, termination, complexity]
status: full
---

Let $L \subseteq \Sigma^*$ be the target, and let $n$ be the number of states of its minimal complete DFA, which is also the number of classes of the Myhill-Nerode relation $\equiv_L$ ($x \equiv_L y$ when $xz \in L \Leftrightarrow yz \in L$ for all $z$). DFAs are complete and have no $\varepsilon$-moves. For a DFA $M$ with transition function $\delta$ we use $\delta^*(q, xy) = \delta^*(\delta^*(q, x), y)$. A DFA $M$ *agrees with* the table $(S, E, T)$ if for all $s \in S \cup S\Sigma$ and $e \in E$, $M$ accepts $se$ if and only if $T(se) = 1$. The target's minimal DFA agrees with every table that L* builds, since $T$ holds true membership answers.

Throughout, $S$ is prefix-closed and $E$ is suffix-closed, and $\varepsilon \in S$, $\varepsilon \in E$. This holds after line L1, and lines L4, L6 and L10 keep it: line L4 adds $ae$ with $e \in E$, whose proper suffixes are suffixes of $e$ and so in $E$; line L6 adds $sa$ with $s \in S$; line L10 adds all prefixes of $c$. Let $k(S, E)$ be the number of distinct rows $\mathrm{row}(s)$ with $s \in S$.

## Part 1: the hypothesis agrees with the table

Let the table be closed and consistent, and let $H = H(S, E, T)$ with transition function $\delta$, start $q_0 = \mathrm{row}(\varepsilon)$ and accepting set $F$. As noted on the page, $\delta$ and $F$ are well defined.

**Lemma 1.** For every $s \in S \cup S\Sigma$, $\delta^*(q_0, s) = \mathrm{row}(s)$.

*Proof.* By induction on $|s|$. For $s = \varepsilon$ it is the definition of $q_0$. Let $s = s'a$ with $a \in \Sigma$. If $s \in S$, then $s' \in S$ since $S$ is prefix-closed. If $s \in S\Sigma$, then $s'$ is the element of $S$ that was extended. In both cases $s' \in S$, so by the induction hypothesis $\delta^*(q_0, s'a) = \delta(\mathrm{row}(s'), a) = \mathrm{row}(s'a)$ by the definition of $\delta$. $\square$

**Lemma 2.** For every $s \in S \cup S\Sigma$ and $e \in E$, $\delta^*(q_0, se) \in F$ if and only if $T(se) = 1$.

*Proof.* By induction on $|e|$. If $e = \varepsilon$: by Lemma 1, $\delta^*(q_0, s) = \mathrm{row}(s)$. By closedness (or trivially if $s \in S$) there is $s' \in S$ with $\mathrm{row}(s') = \mathrm{row}(s)$, so $\mathrm{row}(s) \in F$ if and only if $T(s') = 1$, and $T(s') = T(s)$ because the two rows agree on the column $\varepsilon$.

If $e = ae'$ with $a \in \Sigma$: then $e' \in E$ since $E$ is suffix-closed. Pick $s' \in S$ with $\mathrm{row}(s') = \mathrm{row}(s)$. Then

$$\delta^*(q_0, s a e') = \delta^*(\delta(\mathrm{row}(s'), a), e') = \delta^*(\mathrm{row}(s'a), e') = \delta^*(q_0, s'ae'),$$

using Lemma 1 for $s$ and for $s'a \in S\Sigma$. By the induction hypothesis for $s'a$ and $e'$, this state is in $F$ if and only if $T(s'ae') = 1$. Finally $T(s'ae') = T(sae')$, because $\mathrm{row}(s') = \mathrm{row}(s)$ and $ae' = e \in E$. $\square$

So $H$ agrees with the table.

## Part 2: uniqueness of the hypothesis

**Lemma 3.** Let the table be closed and consistent, let $k = k(S, E)$, and let $M = (Q', \Sigma, \delta', q_0', F')$ be a DFA that agrees with the table and has at most $k$ states. Then $M$ is isomorphic to $H(S, E, T)$.

*Proof.* For $q \in Q'$ let $\rho(q) : E \to \{0, 1\}$ map $e$ to 1 if and only if $\delta'^*(q, e) \in F'$. Because $M$ agrees with the table, $\rho(\delta'^*(q_0', s)) = \mathrm{row}(s)$ for all $s \in S \cup S\Sigma$. The strings of $S$ have $k$ distinct rows, so the states $\delta'^*(q_0', s)$ with $s \in S$ have at least $k$ distinct images under $\rho$, and so are at least $k$ distinct states. As $|Q'| \le k$, these are all the states of $M$, $|Q'| = k$, and $\rho$ maps $Q'$ bijectively onto the set of rows of $S$. Hence a state of $M$ is determined by its $\rho$ value.

Define $\varphi(\mathrm{row}(s)) = \delta'^*(q_0', s)$ for $s \in S$. It is well defined: if $\mathrm{row}(s_1) = \mathrm{row}(s_2)$, the two states have the same $\rho$ value and so are equal. It is a bijection from the states of $H$ onto $Q'$ by the previous paragraph. It maps start to start, since $\varphi(\mathrm{row}(\varepsilon)) = q_0'$. It preserves transitions: for $s \in S$ and $a \in \Sigma$, closedness gives $s'' \in S$ with $\mathrm{row}(s'') = \mathrm{row}(sa)$, and the states $\delta'(\varphi(\mathrm{row}(s)), a) = \delta'^*(q_0', sa)$ and $\varphi(\mathrm{row}(sa)) = \delta'^*(q_0', s'')$ have the same $\rho$ value $\mathrm{row}(sa)$, so they are equal. It preserves acceptance: $\varphi(\mathrm{row}(s)) \in F'$ if and only if $T(s) = 1$ (agreement with $e = \varepsilon$), if and only if $\mathrm{row}(s) \in F$. $\square$

## Part 3: the number of rows

**Lemma 4.** $k(S, E) \le n$ at all times, and $k$ never decreases.

*Proof.* If $\mathrm{row}(s_1) \neq \mathrm{row}(s_2)$, some $e \in E$ has $T(s_1 e) \neq T(s_2 e)$, so $s_1 \not\equiv_L s_2$. So the access strings with distinct rows lie in distinct classes of $\equiv_L$, of which there are $n$. Adding a string to $S$ adds a row and changes no other row. Adding a column to $E$ extends every row by one entry, so rows that differed still differ. Hence $k$ never decreases. $\square$

**Lemma 5.** Each execution of line L4 or line L6 increases $k$ by at least one.

*Proof.* Line L4 adds $ae$ where $\mathrm{row}(s_1) = \mathrm{row}(s_2)$ and $T(s_1 ae) \neq T(s_2 ae)$; after the addition the rows of $s_1$ and $s_2$ differ in the new column, and by Lemma 4 no other pair of distinct rows merges, so $k$ grows. Line L6 adds $sa$, whose row differs from every row of $S$; the new column set is the same, so $k$ grows by one. $\square$

## Part 4: counterexamples and termination

**Lemma 6.** Let $H$ be a hypothesis with $k$ states that receives the counterexample $c$, and let $H'$ be the next hypothesis. Then $H'$ has more than $k$ states.

*Proof.* Let $(S, E, T)$ be the table that gave $H$ and $(S', E', T')$ the table that gives $H'$. Then $S \subseteq S'$, $E \subseteq E'$, and $T'$ extends $T$. $H'$ agrees with $(S', E', T')$ by Part 1, and so it also agrees with $(S, E, T)$, whose strings are among those of the new table. The number of states of $H'$ is $k(S', E') \ge k(S, E) = k$ by Lemma 4. Suppose that it is exactly $k$. Then $H'$ agrees with $(S, E, T)$ and has at most $k$ states, so it is isomorphic to $H$ by Lemma 3, and $L(H') = L(H)$. But $c \in S'$ after line L10 and $\varepsilon \in E'$, so $H'$ accepts $c$ if and only if $T'(c) = 1$, that is, if and only if $c \in L$; and $H$ accepts $c$ if and only if $c \notin L$. This contradicts $L(H') = L(H)$. $\square$

**Theorem.** L* stops after at most $n$ equivalence queries and at most $n - 1$ executions of lines L4 and L6 in all, and returns the minimal DFA of $L$.

*Proof.* By Lemmas 4 and 5, $k$ starts at 1 and is at most $n$, and each execution of L4 or L6 increases it, so there are at most $n - 1$ such executions in the whole run. Between two consecutive equivalence queries, the loop therefore makes finitely many passes, each of which either adds a column, adds a row, or reaches line L7 with a closed and consistent table. The hypotheses have $k \le n$ states by Lemma 4, and by Lemma 6 their sizes strictly increase. Since the first has at least one state, there are at most $n$ hypotheses, so at most $n$ equivalence queries, and the last one is answered "yes" (the loop cannot run forever without asking another one, by the bound on L4 and L6). The returned $H$ satisfies $L(H) = L$ and has at most $n$ states, so it has exactly $n$ states and, by the uniqueness of the minimal DFA up to isomorphism, it is the minimal DFA. $\square$

## Part 5: cost

Let $m$ be the length of the longest counterexample. By Lemma 4 and Lemma 5, $|E| \le 1 + (n - 1) = n$. $S$ gains at most $n - 1$ strings at line L6 and at most $m$ new strings at each of at most $n - 1$ executions of line L10 (the prefix $\varepsilon$ is already present), so $|S| \le n + m(n - 1)$. The table has $|S \cup S\Sigma| \cdot |E| \le (\sigma + 1)(n + m(n - 1)) n$ entries, and each membership query fills one new entry, so this bounds the number of membership queries.

The loop runs at most $(n - 1) + (n - 1) + n \le 3n$ times. In each pass, the consistency check, the closedness check, the construction of the hypothesis and the filling of new entries read each entry of the table a constant number of times, which is $O(\sigma m n^2)$ entries, and each read hashes a string of length at most $m + 2n$. So a pass takes $O(\sigma m n^2 (m + n))$ time, and the whole run $O(\sigma m n^3 (m + n))$ time besides the teacher's work. The table stores $O(\sigma m n^2)$ strings of length $O(m + n)$, which is $O(\sigma m n^2 (m + n))$ space. $\blacksquare$
