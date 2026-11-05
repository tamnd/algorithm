---
title: The lazy DFA accepts exactly the words that the NFA accepts
proves: [correctness, termination]
status: full
---

Let $N$ have the finite set of states $Q$, start state $q_0$ and accepting states $F$. For $S \subseteq Q$ and a symbol $c$, $\mathrm{MOVE}(S, c)$ is the set of targets of the moves on $c$ that leave $S$, and $\mathrm{CLOSURE}(S)$ is the set of states reachable from $S$ by zero or more $\varepsilon$-moves. Define $\hat\delta(\varepsilon) = \mathrm{CLOSURE}(\{q_0\})$ and $\hat\delta(ua) = \mathrm{CLOSURE}(\mathrm{MOVE}(\hat\delta(u), a))$.

**Lemma 1.** For every word $u$, $\hat\delta(u)$ is the set of states $q$ such that some path from $q_0$ to $q$ reads $u$, where a path may use $\varepsilon$-moves anywhere.

*Proof.* By induction on $u$. For $u = \varepsilon$, a path that reads $\varepsilon$ uses only $\varepsilon$-moves, so its end is in $\mathrm{CLOSURE}(\{q_0\})$, and every state of the closure is the end of such a path. For $ua$, a path that reads $ua$ splits at its last move on a symbol, which reads $a$: before it, a path that reads $u$, ending in some $p \in \hat\delta(u)$ by induction; then a move on $a$ from $p$ to some $p'$, so $p' \in \mathrm{MOVE}(\hat\delta(u), a)$; then only $\varepsilon$-moves, so the end is in the closure. Conversely, each state of $\mathrm{CLOSURE}(\mathrm{MOVE}(\hat\delta(u), a))$ is the end of a path built from these three parts. $\square$

So $N$ accepts $u$ if and only if $\hat\delta(u) \cap F \ne \emptyset$.

**Lemma 2 (stored moves).** At all times, every DFA state object $X$ satisfies: $X.\mathrm{accepting} = (X.\mathrm{set} \cap F \ne \emptyset)$, and for every symbol $c$ with $X.\mathrm{next}[c] = Y$ defined, $Y.\mathrm{set} = \mathrm{CLOSURE}(\mathrm{MOVE}(X.\mathrm{set}, c))$.

*Proof.* Objects are made only at line L12, with the right accepting bit and an empty table. The fields `set` and `accepting` of an object never change afterwards. A table entry is written only at line L9, as $S.\mathrm{next}[c] \gets T$, where $T$ was returned by STATE$(U)$ at line L8 with $U = \mathrm{CLOSURE}(\mathrm{MOVE}(S.\mathrm{set}, c))$ from line L6, and STATE$(U)$ returns an object whose set is $U$: either the one already stored under the key $U$, or a new one with set $U$. Clearing the map at line L7 removes keys but changes no object. So the property holds after every line. $\square$

**Lemma 3 (loop invariant).** After $i$ rounds of the loop at lines L3 to L10, $S.\mathrm{set} = \hat\delta(a_1 \cdots a_i)$.

*Proof.* Before the loop, line L2 sets $S$ to an object with set $\mathrm{CLOSURE}(\{q_0\}) = \hat\delta(\varepsilon)$. In round $i$, with $c = a_i$ and $S.\mathrm{set} = \hat\delta(a_1 \cdots a_{i-1})$: if $S.\mathrm{next}[c]$ is defined, line L4 reads $T$, and by Lemma 2 $T.\mathrm{set} = \mathrm{CLOSURE}(\mathrm{MOVE}(S.\mathrm{set}, c))$. Otherwise lines L6 to L8 make $T$ with the same set. Either way, after line L10, $S.\mathrm{set} = \mathrm{CLOSURE}(\mathrm{MOVE}(\hat\delta(a_1 \cdots a_{i-1}), a_i)) = \hat\delta(a_1 \cdots a_i)$. $\square$

**Termination.** The loop runs once for each of the $n$ symbols of $w$. In each round, MOVE scans the finitely many moves that leave $S.\mathrm{set}$, and CLOSURE is a graph search that adds each state of $Q$ at most once. Lines L7 to L9, L12 and L13 do finitely many map operations. So the algorithm stops.

**Theorem.** LAZY-DFA-MATCH$(N, w, k)$ returns true if and only if $N$ accepts $w$, for every capacity $k \ge 1$.

*Proof.* By Lemma 3, after the loop $S.\mathrm{set} = \hat\delta(w)$. By Lemma 2, line L11 returns $\hat\delta(w) \cap F \ne \emptyset$, which by Lemma 1 holds exactly when $N$ accepts $w$. The capacity enters only through line L7, which by Lemma 2 never makes a stored set or move wrong. $\blacksquare$

**Search.** With $q_0$ added to the result of MOVE before the closure, the same argument with $\hat\delta'(ua) = \mathrm{CLOSURE}(\mathrm{MOVE}(\hat\delta'(u), a) \cup \{q_0\})$ shows, by the induction of Lemma 1, that $\hat\delta'(u)$ is the set of states reachable from $q_0$ by a path that reads some suffix of $u$. So the state after $a_1 \cdots a_i$ is accepting if and only if some substring of $w$ that ends at position $i$ is accepted.
