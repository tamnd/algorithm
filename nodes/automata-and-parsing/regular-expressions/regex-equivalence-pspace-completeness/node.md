---
tag: C3A5C0
kind: theorem
slug: regex-equivalence-pspace-completeness
name: PSPACE-completeness of regex equivalence
aliases:
- Meyer-Stockmeyer theorem for regex equivalence
area: automata-and-parsing/regular-expressions
level: advanced
summary: Regex equivalence is PSPACE-complete, even for restricted regex syntaxes.
prereqs: [regex-equivalence, regex-universality, pspace, turing-machine]
see_also: [regex-inclusion, nfa-universality, nfa-equivalence, savitch-theorem, cook-levin-theorem, expspace, co-np, extended-regular-expressions]
sources:
  - paper: "Albert R. Meyer and Larry J. Stockmeyer, The equivalence problem for regular expressions with squaring requires exponential space, 13th Annual Symposium on Switching and Automata Theory (1972)"
    locator: pp. 125 to 129 (the encoding of space-bounded computations by regular expressions; equivalence is PSPACE-complete without squaring and EXPSPACE-complete with it)
  - paper: "Larry J. Stockmeyer and Albert R. Meyer, Word problems requiring exponential time, Fifth Annual ACM Symposium on Theory of Computing (STOC 1973)"
    locator: pp. 1 to 9 (the table of complexities for the operator sets with union, concatenation, star, squaring and complement, and for a one-letter alphabet)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Chapter 8, Example 8.4 (the nondeterministic linear-space algorithm for the complement of NFA universality) and Section 8.1 (Savitch's theorem); Section 9.1 (the EXPSPACE-completeness of equivalence with exponentiation, by the same encoding of computation histories)
  - paper: "Richard E. Stearns and Harry B. Hunt III, On the equivalence and containment problems for unambiguous regular expressions, regular grammars and finite automata, SIAM Journal on Computing 14(3) (1985)"
    locator: pp. 598 to 611 (polynomial time for unambiguous expressions)
---

## Statement

The expressions use the syntax of the [regular expression](/regular-expression/) page: symbols of the alphabet, $\varepsilon$, $\emptyset$, union $\mid$, concatenation and star $^*$. No other operator is allowed. The size of an expression is the number of nodes of its syntax tree.

**Theorem** (Meyer and Stockmeyer, 1972). Let $\Sigma$ be a fixed alphabet with at least two symbols. Each of the following problems is PSPACE-complete:

1. **Universality.** Given $r$ over $\Sigma$, is $L(r) = \Sigma^*$?
2. **Equivalence.** Given $r$ and $s$ over $\Sigma$, is $L(r) = L(s)$?
3. **Inclusion.** Given $r$ and $s$ over $\Sigma$, is $L(r) \subseteq L(s)$?

The hardness holds under polynomial-time many-one reductions, and already for expressions of star height 1, that is, expressions in which no star is applied to an expression that contains a star.

## In plain words

Two patterns are equivalent if they describe the same strings. You cannot check this by trying strings one at a time, since there are infinitely many, but you can turn both patterns into machines and run them side by side, keeping track of the set of places each machine could be in. That needs only a modest amount of memory, though it may take a very long time.

The theorem says that no shortcut avoids this in general. Any problem that a computer can solve with a modest amount of memory can be rewritten as a question of the form "does this pattern describe every string?". The pattern describes all the ways in which a long string can fail to be a correct record of the computation. So a fast method for patterns would give a fast method for every such problem, which is believed to be impossible.

## Proof

**Inclusion and universality reduce to each other's special cases.** Write $\Sigma = \{a_1, \ldots, a_k\}$ and $U = (a_1 \mid \cdots \mid a_k)^*$. Then $L(r) = \Sigma^*$ if and only if $r \equiv U$, if and only if $L(U) \subseteq L(r)$. So universality reduces to equivalence and to inclusion in linear time, and it suffices to show (a) that equivalence and inclusion are in PSPACE and (b) that universality is PSPACE-hard. Equivalence is then in PSPACE and PSPACE-hard, and so is inclusion, and universality is in PSPACE as a special case.

**(a) Membership.** Convert $r$ and $s$ to NFAs $N_r$ and $N_s$ with $\varepsilon$-moves and $O(\lvert r \rvert)$ and $O(\lvert s \rvert)$ states, by [Thompson's construction](/thompson-construction/). For a set $S$ of states of an NFA and a symbol $a$, let $\delta(S, a)$ be the $\varepsilon$-closure of the states reached from $S$ by $a$-moves; it is computed in polynomial time. Consider the following nondeterministic procedure for non-inclusion, $L(r) \not\subseteq L(s)$:

- Let $S$ and $T$ be the $\varepsilon$-closures of the start states of $N_r$ and $N_s$, and let $c = 0$.
- Repeat: if $S$ contains an accepting state and $T$ does not, accept. If $c = 2^{\lvert N_r \rvert + \lvert N_s \rvert}$, reject. Otherwise guess a symbol $a$ and set $S \leftarrow \delta(S, a)$, $T \leftarrow \delta(T, a)$ and $c \leftarrow c + 1$.

After a guessed prefix $w$, $S$ and $T$ are the sets of states that $N_r$ and $N_s$ can reach on $w$, so a branch accepts exactly when it has guessed a $w$ with $w \in L(r) \setminus L(s)$. If such a $w$ exists, a shortest one has length less than $2^{\lvert N_r \rvert + \lvert N_s \rvert}$: the pairs $(S, T)$ along a shortest one are pairwise distinct, since a repeated pair would let us cut out the part between the two repetitions. So the procedure accepts if and only if $L(r) \not\subseteq L(s)$. It stores two sets of states and a counter of $\lvert N_r \rvert + \lvert N_s \rvert + 1$ binary digits, which is space polynomial in the input. Hence non-inclusion is in NPSPACE, which equals PSPACE by [Savitch's theorem](/savitch-theorem/). Since PSPACE is closed under complement, inclusion is in PSPACE, and equivalence, which is two inclusions, is too.

**(b) Hardness: the machine and its histories.** Let $A \in$ [PSPACE](/pspace/). Its complement $\overline{A}$ is also in PSPACE, so it is decided by a deterministic single-tape [Turing machine](/turing-machine/) $M$ with states $Q$, accepting state $q_{\mathrm{acc}}$, tape alphabet $\Gamma$ containing the blank $\sqcup$, and a polynomial $p$ with $p(n) \ge n + 1$, such that on inputs of length $n$:

- $M$ uses only the first $p(n)$ cells, never moves left from the first cell or right from cell $p(n)$, and halts;
- each move writes a symbol, changes the state, and moves the head left, right, or not at all; once $M$ halts, we let it stay in its halting state forever without changing the tape.

These are standard normalizations. Fix an input $x = x_1 \cdots x_n$ and write $p = p(n)$. Let $\Delta_0 = \Gamma \cup (Q \times \Gamma)$ and $\Delta = \Delta_0 \cup \{\#\}$. A *configuration* is a string of $p$ symbols of $\Delta_0$, exactly one of which is in $Q \times \Gamma$; the pair $(q, a)$ marks the cell under the head, the symbol $a$ in it, and the state $q$. The start configuration is $C_0 = (q_0, x_1)\, x_2 \cdots x_n \sqcup^{p - n}$.

Because the head moves at most one cell per step, the symbol in cell $j$ of the next configuration is determined by the symbols in cells $j - 1$, $j$ and $j + 1$ of the current one, where cell 0 and cell $p + 1$ are read as $\#$. So there is a function $F : \Delta^3 \to \Delta_0$, defined from the transition function of $M$ alone, such that the successor $C'$ of a configuration $C$ satisfies $C'_j = F(C_{j-1}, C_j, C_{j+1})$ for $1 \le j \le p$. For instance, if $\delta(q, a) = (q', b, \text{right})$ then $F(d, (q, a), e) = b$ and $F((q, a), c, e) = (q', c)$ for every $c \in \Gamma$; and if no symbol of the window is in $Q \times \Gamma$, then $F(d, c, e) = c$. The values of $F$ on windows with two or more head symbols are never used and can be set arbitrarily.

Call a string $w \in \Delta^*$ *good* if:

- **(format)** $w \in \#(\Delta_0^p \#)^*\Delta_0^p\#$, that is, $w = \# B_0 \# B_1 \# \cdots \# B_t \#$ with $t \ge 0$ and blocks $B_i$ of exactly $p$ symbols of $\Delta_0$;
- **(start)** $B_0 = C_0$;
- **(moves)** for every $i < t$ and every $j$, the $j$-th symbol of $B_{i+1}$ is $F$ of the symbols at positions $j - 1$, $j$, $j + 1$ of $\# B_i \#$;
- **(accept)** some symbol of $w$ is of the form $(q_{\mathrm{acc}}, a)$.

By induction on $i$, (format), (start) and (moves) hold exactly when $B_0, B_1, \ldots, B_t$ are the first $t + 1$ configurations of the run of $M$ on $x$. With (accept), a good string exists if and only if the run reaches $q_{\mathrm{acc}}$, that is, if and only if $M$ accepts $x$, that is, if and only if $x \notin A$.

**The expression.** We build an expression $R_x$ with $L(R_x) = \Delta^* \setminus \{\text{good strings}\}$, as a union of four parts, one for each way to fail. Write $\Delta$ also for the union of all symbols of $\Delta$, $\Delta_0$ for the union of those of $\Delta_0$, $\Delta \setminus X$ for the union of the symbols not in $X$, and $e^k$ for $k$ copies of $e$ concatenated.

- **Not in format:** $\varepsilon \mid \# \mid \Delta_0\Delta^* \mid \Delta^*\Delta_0 \mid \Delta^* \# (\varepsilon \mid \Delta_0)^{p-1} \# \Delta^* \mid \Delta^* \Delta_0^{p+1} \Delta^*$. A string escapes all six terms exactly when it has length at least 2, starts and ends with $\#$, and has exactly $p$ symbols between any two consecutive $\#$s.
- **Wrong start:** with $c_0 c_1 \cdots c_{p+1} = \# C_0 \#$, the union of $(\varepsilon \mid \Delta)^{p+1}$, for strings that are too short, and of $\Delta^i (\Delta \setminus \{c_i\}) \Delta^*$ for $0 \le i \le p + 1$.
- **A wrong move:** $\Delta^* \big(\bigcup_{(d, c, e)} d\, c\, e\, \Delta^{p-1} (\Delta_0 \setminus \{F(d, c, e)\})\big) \Delta^*$, where the union is over the windows $(d, c, e)$ with $c \in \Delta_0$, $d, e \in \Delta$ and at most one symbol from $Q \times \Gamma$. The symbol after $\Delta^{p-1}$ is $p + 1$ positions after $c$, which in a string in format is the same cell of the next block.
- **No acceptance:** $(\Delta \setminus \{(q_{\mathrm{acc}}, a) : a \in \Gamma\})^*$.

A good string matches none of the terms: it is in format, starts with $\# C_0 \#$, contains an accepting symbol, and every window that has a symbol $p + 1$ positions later satisfies $F$. Conversely, let $w$ be a string that is not good. If it fails (format), (start) or (accept), it matches the corresponding part. Otherwise it fails (moves); take the least $i$ such that $B_{i+1}$ is not computed from $B_i$ by $F$. By the induction above, $B_i$ is a configuration, so all its windows have at most one head symbol, and the window where $F$ fails matches a term of the third part. So $L(R_x) = \Delta^* \setminus \{\text{good strings}\}$, and
$$x \in A \iff \text{no good string exists} \iff L(R_x) = \Delta^*.$$

The alphabet $\Delta$ and the function $F$ depend only on $M$, so they are constants. The first part has size $O(p)$, the second $O(p^2)$, the third has a constant number of terms of size $O(p)$, and the fourth has constant size. So $R_x$ has size $O(p(n)^2)$ and is computed in polynomial time. Every star in $R_x$ is applied to a union of symbols, so $R_x$ has star height 1.

**(b) Hardness over two letters.** The alphabet $\Delta$ depends on $M$. To get a fixed alphabet $\{0, 1\}$, fix an injective code $h : \Delta \to \{0, 1\}^\ell$ with $\ell = \lceil \log_2 \lvert \Delta \rvert \rceil$, extended to strings. Let $h(R_x)$ be $R_x$ with each symbol $d$ replaced by the string $h(d)$, so $L(h(R_x)) = h(L(R_x))$, and let
$$B = \big((0 \mid 1)^\ell\big)^* \big((0 \mid 1)(\varepsilon \mid 0 \mid 1)^{\ell - 2} \mid N\, (0 \mid 1)^*\big),$$
where $N$ is the union of the strings of length $\ell$ that are not codes. Then $L(B)$ is the set of binary strings that are not in $h(\Delta)^*$: either their length is not a multiple of $\ell$, or some block at a position divisible by $\ell$ is not a code. Every other binary string is $h(u)$ for exactly one $u \in \Delta^*$, since $h$ has fixed length and is injective. So $h(R_x) \mid B$ is universal over $\{0, 1\}$ if and only if every $u \in \Delta^*$ is in $L(R_x)$. The expression $B$ has constant size and star height 1, and $h(R_x)$ is larger than $R_x$ by a constant factor. This gives a polynomial-time reduction from $A$ to universality over $\{0, 1\}$; over a larger alphabet the same expression works after adding the other symbols as further non-codes. $\square$

**Check by script.** For a machine that accepts when its input contains a 1, with $\Gamma = \{0, 1, \sqcup\}$, three states and inputs of length 1 to 3, a script built $R_x$ and compared it against a direct test for good strings: on all strings of length at most 4 over $\Delta$ (13 symbols), on 20000 random edits of the true history for each input, and on every string in format with at most three blocks for inputs of length 1. The two agreed in every case, the only good strings found were the accepting histories, and for the inputs $0$, $00$ and $000$ no good string exists.

## Consequences

- **Equivalence of NFAs.** The same statements hold for NFAs ([NFA universality](/nfa-universality/), [NFA equivalence](/nfa-equivalence/)). The membership proof works on NFAs directly, and hardness follows by converting $R_x$ to an NFA of linear size.
- **No polynomial algorithm unless P = PSPACE.** In particular, minimizing a regular expression, or testing whether a rewriting of an expression preserves its language, cannot be done in polynomial time in general unless P = PSPACE ([regex equivalence](/regex-equivalence/), [regex inclusion](/regex-inclusion/), [regex minimization](/regex-minimization/)).
- **Exponential-time algorithms are the norm.** The procedures that are used in practice, by the [subset construction](/subset-construction/), by [Brzozowski derivatives](/brzozowski-derivatives/), or by antichains, take time $2^{O(m)}$ for expressions of size $m$ in the worst case.
- **Long counterexamples.** When two expressions differ, the shortest string in their symmetric difference can be exponentially long in their size, so a short certificate of inequivalence may not exist. Over one letter, a certificate written in binary does exist, which is why that case is easier.
- **A template for hardness.** The encoding of computation histories as strings, with an expression for the strings that are not correct histories, is the same as in the [Cook-Levin theorem](/cook-levin-theorem/), and it is reused for many problems about automata, grammars and logics.

## Tightness

- **One letter.** Over a one-letter alphabet, equivalence and inclusion are coNP-complete (Stockmeyer and Meyer, 1973), so the condition $\lvert\Sigma\rvert \ge 2$ cannot be dropped unless NP = PSPACE.
- **No star.** Without star, expressions denote finite sets of strings, and inequivalence is NP-complete (Stockmeyer and Meyer, 1973). The proof above uses stars only around unions of symbols, so star height 1 is already enough for PSPACE-hardness, and star height 0 is not, unless NP = PSPACE.
- **More operators.** With a squaring operator $r^2$, or with exponents written in binary, equivalence becomes EXPSPACE-complete ([EXPSPACE](/expspace/); Meyer and Stockmeyer, 1972), because an expression of polynomial size then describes configurations of exponential length. With complement, as in [extended regular expressions](/extended-regular-expressions/), it is non-elementary (Stockmeyer and Meyer, 1973).
- **Restricted expressions in polynomial time.** For unambiguous expressions, equivalence and inclusion are polynomial (Stearns and Hunt, 1985). For deterministic expressions, whose Glushkov automaton is a DFA, they are polynomial because DFA equivalence is.
- **Space.** The membership proof uses space $O(m^2)$ after Savitch's theorem; the nondeterministic procedure itself uses only $O(m)$ space for expressions of size $m$, so non-universality is in NSPACE($m$).

## History

Meyer and Stockmeyer (1972) introduced the method in their paper on regular expressions with squaring. They showed that equivalence with squaring needs exponential space and that, without squaring, the same construction shows that equivalence is complete for polynomial space. Stockmeyer and Meyer (1973) completed the picture for the operator sets with union, concatenation, star, squaring and complement, and for one-letter alphabets. Sipser's textbook presents the EXPSPACE version with the same encoding of histories, and the PSPACE membership by a nondeterministic search over sets of states.

## References
