---
title: Quine-McCluskey lists all primes and returns a minimum cover
proves: [correctness]
status: full
---

We write $A = F \cup D$, and for a cube $c$ we write $\mathrm{dash}(c)$ for the number of its dashes. An implicant is a cube $c \subseteq A$. For a cube $c$ and a position $i$ with $c[i] = -$, the two halves of $c$ at $i$ are $c$ with $c[i]$ set to 0 and $c$ with $c[i]$ set to 1. Their union is $c$.

**Lemma 1 (levels).** At the start of round $k$ of the loop of line L2 (rounds count from 0), the set level is exactly $L_k = \{c : c \subseteq A,\ \mathrm{dash}(c) = k\}$.

*Proof.* By induction on $k$. For $k = 0$, line L1 sets level to the minterms of $A$, which are the implicants with no dash. Assume the claim for $k$. Line L6 adds a cube $e$ to next only when its two halves at some position $i$ are both in level, so both are implicants by the hypothesis, and $e$, their union, is an implicant with $k + 1$ dashes. Conversely, let $e$ be an implicant with $k + 1$ dashes, and let $i$ be any dash of $e$. Its two halves $c$ (with 0 at $i$) and $d$ (with 1 at $i$) are subcubes of $e$, so they are implicants with $k$ dashes, and they are in level. Line L4 reaches $c$ and $i$, line L5 builds exactly $d$, and line L6 adds $e$. So next $= L_{k+1}$ after the round, and line L9 makes it the new level. $\square$

**Lemma 2 (primes).** In round $k$, a cube $c \in L_k$ is put in merged by line L7 exactly when $c$ is not prime.

*Proof.* By the literal form of primality (see the prime implicant page), an implicant $c$ is not prime exactly when, for some literal position $i$ of $c$, the cube $e$ equal to $c$ with $c[i]$ set to $-$ is an implicant. Such an $e$ has $k + 1$ dashes, and $c$ is one of its halves at $i$. The other half $c'$ is a subcube of $e$, so it is in $L_k$. If $c[i] = 0$, then line L4 reaches $c$ and $i$, line L5 builds $c'$, and line L7 marks $c$. If $c[i] = 1$, then line L4 reaches $c'$ and $i$, line L5 builds $c$, and line L7 marks $c$ as the cube $d$. Conversely, line L7 marks a cube only when it is a half of a cube that line L6 adds, and that cube is an implicant by Lemma 1, so the marked cube is not prime. $\square$

**Theorem 1.** PRIMES returns every prime implicant of $f$ once, and nothing else.

*Proof.* Every implicant $c$ is in exactly one level, $L_{\mathrm{dash}(c)}$, by Lemma 1. Line L8 adds $c$ in that round exactly when $c$ is not in merged, that is, by Lemma 2, when $c$ is prime. A level $L_k$ with $k > n$ is empty, so the loop of line L2 stops after at most $n + 1$ rounds. $\square$

For phase 2, let $P$ be the list of primes and $w(p) = (1, |p|)$, where $|p|$ is the number of literals. Weights add coordinatewise and compare lexicographically. For a set $\mathrm{left} \subseteq F$ and a set $\mathrm{cols} \subseteq P$, let $\mathrm{OPT}(\mathrm{left}, \mathrm{cols})$ be the least weight of a set $S \subseteq \mathrm{cols}$ whose union contains $\mathrm{left}$, or $\infty$ if there is none.

**Lemma 3 (reductions).** Each change that lines L13, L14 and L15 make to (left, cols, chosen, spent) keeps the value $\mathrm{spent} + \mathrm{OPT}(\mathrm{left}, \mathrm{cols})$.

*Proof.* Line L13: let row $m$ have the single prime $p$ in cols. Every feasible $S$ for (left, cols) holds $p$, since nothing else covers $m$. So $\mathrm{OPT}(\mathrm{left}, \mathrm{cols}) = w(p) + \mathrm{OPT}(\mathrm{left} \setminus p, \mathrm{cols} \setminus \{p\})$, and moving $p$ to chosen adds $w(p)$ to spent. When several rows force primes at once, apply this to each forced prime in turn.

Line L14: let $j \ne k$ be in cols, with $j \cap \mathrm{left} \subseteq k$ and $w(k) \le w(j)$. Take an optimal $S$ for (left, cols). If $j \in S$, then $S' = (S \setminus \{j\}) \cup \{k\}$ still covers left and has weight at most $w(S)$, because weights are nonnegative. So some optimal set avoids $j$, and dropping $j$ keeps OPT. Line L14 drops one column per pass and then recomputes, so the dominating column $k$ is in cols when $j$ is dropped. Two equal columns cannot both go in one pass.

Line L15: let $m \ne m_2$ be rows of left with $\mathrm{rows}(m_2) \subseteq \mathrm{rows}(m)$, where $\mathrm{rows}(x)$ is the set of primes of cols that contain $x$. Every set that covers $m_2$ holds a prime of $\mathrm{rows}(m_2)$, which also covers $m$. So the feasible sets for left and for $\mathrm{left} \setminus \{m\}$ are the same, and OPT does not change. Again one row goes per pass, so two equal rows cannot both go. $\square$

**Lemma 4 (search).** A call SOLVE(left, cols, chosen, spent) records, among other sets, a set of weight $\mathrm{spent} + \mathrm{OPT}(\mathrm{left}, \mathrm{cols})$ unless the best recorded weight is already at most that value. Every recorded set covers $F$ when the root call starts with $\mathrm{left} = F$.

*Proof.* By induction on $|\mathrm{cols}|$. By Lemma 3, the reductions keep $\mathrm{spent} + \mathrm{OPT}$. Each pass that changes something removes a row or a column, so the repeat loop stops. If some row has no prime in cols, OPT is $\infty$ and the return loses nothing. If left is empty, OPT is $(0, 0)$ and line L11 records chosen when it is better. If spent is at least the best weight, line L12 returns, and the claim holds since $\mathrm{OPT} \ge (0, 0)$. Otherwise let $m$ be the row of line L16. Every feasible set for (left, cols) holds some prime $p$ of row $m$, so $\mathrm{OPT}(\mathrm{left}, \mathrm{cols}) = \min_p \big(w(p) + \mathrm{OPT}(\mathrm{left} \setminus p, \mathrm{cols} \setminus \{p\})\big)$, and the loop calls SOLVE on each term, with one column fewer. The claim follows from the induction hypothesis. A set is recorded only at line L11, when left is empty, and the rows removed on the way were covered by chosen primes or were dominated rows, which a chosen prime of the dominating row covers. $\square$

**Theorem 2.** COVER returns a set of primes of least weight whose union contains $F$, and it is a minimum cover of $f$.

*Proof.* The set of all primes covers $F$, since each minterm of $F$ is an implicant and lies in some prime. It has at most $|P|$ cubes, so the initial bound $(|P| + 1, 0)$ is larger than its weight, and Lemma 4 applied to the root call shows that the returned set has weight $\mathrm{OPT}(F, P)$. Each prime lies in $A$, so the union of the returned set lies between $F$ and $A$, and it is a cover. By Quine's theorem (see the prime implicant page), every minimum cover for this cost consists of primes, so no cover has a smaller weight. $\blacksquare$

**Termination.** Phase 1 stops after at most $n + 1$ rounds. In phase 2 each recursive call has one column fewer, so the depth is at most $|P|$, and each repeat loop stops as shown in Lemma 4.
