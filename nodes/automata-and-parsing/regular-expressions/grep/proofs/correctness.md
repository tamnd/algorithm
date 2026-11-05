---
title: GREP prints exactly the lines that contain a substring in the language of the expression
proves: [correctness, termination]
status: full
---

Let $N$ be the NFA built at line L1, with start state $s$ and accepting state $f$, and assume $L(N) = L(r)$, which is the correctness of the [Thompson construction](/thompson-construction/). Fix a line $x = x_1 \cdots x_\ell$ and write $x[j:i] = x_{j+1} \cdots x_i$ for $0 \le j \le i \le \ell$.

A *run* of $N$ on a string $v$ is a path of moves that starts in $s$ and whose symbol labels, in order, spell $v$, with any number of $\varepsilon$-moves before, between and after them. Let $R(v)$ be the set of the last states of the runs on $v$. Then $v \in L(N)$ if and only if $f \in R(v)$. For a set $X$ of states, $\mathrm{CLOSE}(X)$ is the set of states that a path of zero or more $\varepsilon$-moves reaches from $X$; the procedure with an explicit stack computes exactly this set, as proved for [NFA simulation](/nfa-simulation/).

**Lemma 1.** For every string $v$ and symbol $a$, $R(va) = \mathrm{CLOSE}(\{q' : q \in R(v) \text{ has a move on } a \text{ to } q'\})$.

*Proof.* A run on $va$ reads $a$ in exactly one symbol move, from some $q$ to some $q'$, after the part that reads $v$. That part is a run on $v$ ending in $q$, so $q \in R(v)$, and the rest is a path of $\varepsilon$-moves from $q'$. Conversely, a run on $v$ ending in $q$, a move on $a$ from $q$ to $q'$ and a path of $\varepsilon$-moves from $q'$ form a run on $va$. $\square$

**Lemma 2 (invariant).** When the test of line L6 is evaluated after $i$ passes of the loop, $S = S_i$ with
$$S_i = \bigcup_{j=0}^{i} R(x[j:i]).$$

*Proof.* By induction on $i$. Before the loop, line L3 sets $S = \mathrm{CLOSE}(\{s\}) = R(\varepsilon) = R(x[0:0]) = S_0$. Assume $S = S_{i-1}$ before pass $i$. Line L8 sets $T = M \cup \{s\}$, where $M$ is the set of states $q'$ such that some $q \in S_{i-1}$ has a move on $x_i$ to $q'$. CLOSE distributes over union, so line L9 gives
$$S = \mathrm{CLOSE}(M) \cup \mathrm{CLOSE}(\{s\}) = \bigcup_{j=0}^{i-1} \mathrm{CLOSE}(\{q' : q \in R(x[j:i-1]) \text{ has a move on } x_i \text{ to } q'\}) \cup R(\varepsilon),$$
and by Lemma 1 the union over $j$ is $\bigcup_{j=0}^{i-1} R(x[j:i])$, while $R(\varepsilon) = R(x[i:i])$. So $S = S_i$. $\square$

**Lemma 3.** After line L4 or line L10 in pass $i$ (with $i = 0$ for line L4), `matched` is true if and only if some substring $x[j:i]$ with $j \le i$ is in $L(r)$.

*Proof.* By Lemma 2, $f \in S_i$ if and only if $f \in R(x[j:i])$ for some $j \le i$, that is, if and only if $x[j:i] \in L(N) = L(r)$ for some $j \le i$. $\square$

**Theorem.** For each line, the loop of lines L6 to L10 stops, and line L11 prints the line if and only if some substring of it is in $L(r)$.

*Proof.* Each pass increases $i$ by 1, and the loop stops when $i = \ell$ at the latest, so it makes at most $\ell$ passes. Each CLOSE stops because each state is pushed at most once.

If the loop stops with `matched` true after pass $i$, then by Lemma 3 some substring $x[j:i]$ is in $L(r)$, and the line is printed.

If it stops with `matched` false, then $i = \ell$ and `matched` was false after every pass $0, 1, \ldots, \ell$. By Lemma 3, no substring $x[j:i]$ with $0 \le j \le i \le \ell$ is in $L(r)$. These are all the substrings of $x$, so the line is correctly not printed. The lines are handled one after another in order, so the output is the selected lines in order. $\blacksquare$

**Cost.** The NFA has at most $2m$ states and each state has at most two moves. Each pass of the loop handles each state of $S$ once at line L8 and pushes each state at most once in CLOSE, so a pass costs $O(m)$, and a line of length $\ell$ costs $O(m(\ell + 1))$.
