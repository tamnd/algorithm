---
title: Proof of Kleene's theorem
proves: [statement]
status: full
---

We prove $1 \Rightarrow 2 \Rightarrow 3 \Rightarrow 1$ for a fixed finite alphabet $\Sigma$.

**Paths in an epsilon-NFA.** Let $N = (Q, \Sigma, \delta, q_0, F)$ with $\delta : Q \times (\Sigma \cup \{\varepsilon\}) \to 2^Q$. A path from $p$ to $r$ is a sequence $p = p_0, p_1, \ldots, p_m = r$ with labels $x_1, \ldots, x_m \in \Sigma \cup \{\varepsilon\}$ such that $p_t \in \delta(p_{t-1}, x_t)$ for each $t$. Its label is the string $x_1 x_2 \cdots x_m$, in which each $\varepsilon$ adds nothing. We write $p \overset{w}{\leadsto} r$ when some path from $p$ to $r$ has the label $w$; the path with $m = 0$ gives $p \overset{\varepsilon}{\leadsto} p$. The language is $L(N) = \{ w : q_0 \overset{w}{\leadsto} f \text{ for some } f \in F \}$. The [epsilon-NFA](/epsilon-nfa/) page shows that this is the same as the definition by the extended transition function.

## Step 1: from expressions to epsilon-NFAs

The size $|E|$ of an expression is its number of occurrences of $\emptyset$, $\varepsilon$, symbols and operators.

**Lemma 1.** For each regular expression $E$ there is an epsilon-NFA $N_E$ with $L(N_E) = L(E)$ and at most $2|E|$ states, which has the *shape*: (a) one accepting state $f$, different from the start state $s$; (b) no transition enters $s$; (c) no transition leaves $f$.

*Proof.* By structural induction on $E$. In each case the automata of the subexpressions have disjoint sets of states, and we keep all their transitions.

*Base cases.* For $\emptyset$: states $s, f$ and no transition. For $\varepsilon$: the one transition $f \in \delta(s, \varepsilon)$. For $a \in \Sigma$: the one transition $f \in \delta(s, a)$. In each case the only paths from $s$ to $f$ are the ones with zero transitions (none, since $s \ne f$) or the one transition, so the languages are $\emptyset$, $\{\varepsilon\}$ and $\{a\}$. Each has 2 states and the shape.

*Union $E = E_1 + E_2$.* Let $N_1$ and $N_2$ have the start states $s_1, s_2$ and the accepting states $f_1, f_2$. Add new states $s, f$ and the $\varepsilon$-transitions $s \to s_1$, $s \to s_2$, $f_1 \to f$, $f_2 \to f$. A path from $s$ to $f$ starts with $s \to s_1$ or $s \to s_2$; say $s \to s_1$. After it, the path uses transitions of $N_1$ until it takes a transition that is not in $N_1$. The only such transition from a state of $N_1$ is $f_1 \to f$, because no transition leads from $N_1$ to $N_2$ and none enters $s$. So the path is $s \to s_1$, then a path of $N_1$ from $s_1$ to $f_1$, then $f_1 \to f$, and its label is in $L(N_1) = L(E_1)$. In the same way a path through $s_2$ has its label in $L(E_2)$. Conversely each such combination is a path. So $L(N_E) = L(E_1) \cup L(E_2)$. The new transitions leave $s$ and enter $f$, so the shape holds. The number of states is $n_1 + n_2 + 2 \le 2|E_1| + 2|E_2| + 2 = 2|E|$.

*Concatenation $E = E_1 E_2$.* Add the $\varepsilon$-transition $f_1 \to s_2$; the start state is $s_1$ and the accepting state is $f_2$. A path from $s_1$ to $f_2$ must reach a state of $N_2$, and the only transition from a state of $N_1$ to a state of $N_2$ is $f_1 \to s_2$. No transition leads back from $N_2$ to $N_1$. So the path is a path of $N_1$ from $s_1$ to $f_1$, then $f_1 \to s_2$, then a path of $N_2$ from $s_2$ to $f_2$, and its label is $xy$ with $x \in L(E_1)$ and $y \in L(E_2)$. Conversely each such $x$ and $y$ give a path. So $L(N_E) = L(E_1)L(E_2)$. No transition enters $s_1$ (the new one enters $s_2$) and none leaves $f_2$. The number of states is $n_1 + n_2 \le 2|E|$.

*Star $E = E_1^*$.* Add new states $s, f$ and the $\varepsilon$-transitions $s \to s_1$, $s \to f$, $f_1 \to s_1$, $f_1 \to f$. A path from $s$ to $f$ is either $s \to f$, with label $\varepsilon$, or starts with $s \to s_1$. In the second case, cut the path at each use of a new transition. Between two cuts the path uses only transitions of $N_1$, starts at $s_1$ (each new transition that the path takes before the end enters $s_1$), and ends at a state that has a new outgoing transition, which is $f_1$. So the path is $s \to s_1$, then $k \ge 1$ paths of $N_1$ from $s_1$ to $f_1$ joined by $f_1 \to s_1$, then $f_1 \to f$. Its label is $x_1 \cdots x_k$ with each $x_i \in L(E_1)$. Conversely $\varepsilon$ and each such product are labels of paths. So $L(N_E) = \{\varepsilon\} \cup \bigcup_{k \ge 1} L(E_1)^k = L(E_1)^*$. The new transitions enter $s_1$ and $f$ and leave $s$ and $f_1$, so the shape holds. The number of states is $n_1 + 2 \le 2|E|$. $\square$

The expression $(E)$ with redundant brackets needs no case. This proves $1 \Rightarrow 2$.

## Step 2: from epsilon-NFAs to DFAs

For $S \subseteq Q$ let $\mathrm{Cl}(S) = \{ r : p \overset{\varepsilon}{\leadsto} r \text{ for some } p \in S \}$, the [epsilon-closure](/epsilon-closure/) of $S$. Define the DFA $D = (2^Q, \Sigma, \Delta, S_0, F_D)$ with $S_0 = \mathrm{Cl}(\{q_0\})$, $\Delta(S, a) = \mathrm{Cl}\big(\bigcup_{p \in S} \delta(p, a)\big)$ and $F_D = \{ S : S \cap F \neq \emptyset \}$. It is complete, since $\Delta$ is defined for each $S$ and $a$, including $S = \emptyset$.

**Lemma 2.** For each $w \in \Sigma^*$, $\Delta^*(S_0, w) = R(w)$, where $R(w) = \{ r : q_0 \overset{w}{\leadsto} r \}$.

*Proof.* By induction on $|w|$. For $w = \varepsilon$, $R(\varepsilon) = \mathrm{Cl}(\{q_0\}) = S_0 = \Delta^*(S_0, \varepsilon)$. For $w = va$ with $a \in \Sigma$, take a path from $q_0$ to $r$ with the label $va$. Exactly $|va|$ of its transitions carry a symbol, and the last of them carries $a$. Cut the path before and after this transition. The first part is a path from $q_0$ to some $p$ with label $v$, the transition goes from $p$ to some $p' \in \delta(p, a)$, and the last part is a path from $p'$ to $r$ with label $\varepsilon$. So $r \in R(va)$ if and only if there are $p \in R(v)$ and $p' \in \delta(p, a)$ with $p' \overset{\varepsilon}{\leadsto} r$, that is, if and only if $r \in \Delta(R(v), a)$. By the induction hypothesis $R(v) = \Delta^*(S_0, v)$, so $R(va) = \Delta(\Delta^*(S_0, v), a) = \Delta^*(S_0, va)$. $\square$

So $w \in L(D)$ if and only if $R(w) \cap F \neq \emptyset$, if and only if $w \in L(N)$. The DFA has $2^{|Q|}$ states; keeping only the subsets reachable from $S_0$ does not change the language. This proves $2 \Rightarrow 3$.

## Step 3: from DFAs to expressions

Let $M = (Q, \Sigma, \delta, q_0, F)$ be a complete DFA with $Q = \{1, \ldots, n\}$. For a string $w = a_1 \cdots a_m$ and a state $i$, the run from $i$ is $r_0 = i$, $r_t = \delta(r_{t-1}, a_t)$. Its *inner* states are $r_1, \ldots, r_{m-1}$; the first and the last state do not count. For $0 \le k \le n$ define

$$R^{(k)}_{ij} = \{ w \in \Sigma^* : \delta^*(i, w) = j \text{ and every inner state of the run of } w \text{ from } i \text{ is at most } k \}.$$

**Lemma 3.** For all $i, j$ and $k$, the set $R^{(k)}_{ij}$ is the language of a regular expression $E^{(k)}_{ij}$.

*Proof.* By induction on $k$.

*Base $k = 0$.* No state is at most 0, so the run has no inner state, and $m \le 1$. With $m = 0$ the string is $\varepsilon$, and it lies in the set exactly when $i = j$. With $m = 1$ the string is a symbol $a$ with $\delta(i, a) = j$. So $R^{(0)}_{ij}$ is the finite set $\{ a \in \Sigma : \delta(i, a) = j \}$, plus $\varepsilon$ when $i = j$. Its expression is the sum of these symbols (and $\varepsilon$), or $\emptyset$ when the set is empty.

*Step $k \ge 1$.* We show

$$R^{(k)}_{ij} = R^{(k-1)}_{ij} \cup R^{(k-1)}_{ik} \big(R^{(k-1)}_{kk}\big)^* R^{(k-1)}_{kj}.$$

Let $w \in R^{(k)}_{ij}$. If no inner state of its run equals $k$, then each inner state is at most $k - 1$, and $w \in R^{(k-1)}_{ij}$. Otherwise let $t_1 < t_2 < \cdots < t_p$ be the inner positions with $r_t = k$, where $p \ge 1$. Cut $w$ at these positions: $w = x y_1 \cdots y_{p-1} z$, where $x = a_1 \cdots a_{t_1}$, $y_l = a_{t_l + 1} \cdots a_{t_{l+1}}$ and $z = a_{t_p + 1} \cdots a_m$. The piece $x$ leads from $i$ to $k$, and its inner states are inner states of $w$ before $t_1$, so they are at most $k$ and not equal to $k$: $x \in R^{(k-1)}_{ik}$. In the same way each $y_l \in R^{(k-1)}_{kk}$ and $z \in R^{(k-1)}_{kj}$. So $w$ is in the right side.

Conversely, the set $R^{(k-1)}_{ij}$ is a subset of $R^{(k)}_{ij}$. Let $w = x y_1 \cdots y_q z$ with $x \in R^{(k-1)}_{ik}$, each $y_l \in R^{(k-1)}_{kk}$ and $z \in R^{(k-1)}_{kj}$, where $q \ge 0$. By the lemma $\delta^*(i, uv) = \delta^*(\delta^*(i, u), v)$ of the [DFA](/deterministic-finite-automaton/) page, the run of $w$ from $i$ is the run of $x$, which ends in $k$, followed by the runs of the $y_l$ from $k$ to $k$ and the run of $z$ from $k$ to $j$. So $\delta^*(i, w) = j$. Each inner state of $w$ is an inner state of a piece, which is at most $k - 1$, or a joint between two pieces, which is $k$. So $w \in R^{(k)}_{ij}$.

By the induction hypothesis the four sets on the right have expressions, so $E^{(k)}_{ij} = E^{(k-1)}_{ij} + E^{(k-1)}_{ik} \big(E^{(k-1)}_{kk}\big)^* E^{(k-1)}_{kj}$ is an expression for $R^{(k)}_{ij}$. $\square$

Each inner state is at most $n$, so $R^{(n)}_{ij} = \{ w : \delta^*(i, w) = j \}$. Hence

$$L(M) = \bigcup_{j \in F} R^{(n)}_{q_0 j},$$

and the sum of the expressions $E^{(n)}_{q_0 j}$ over $j \in F$, or $\emptyset$ if $F = \emptyset$, is an expression for $L(M)$. This proves $3 \Rightarrow 1$ and the theorem. $\blacksquare$
