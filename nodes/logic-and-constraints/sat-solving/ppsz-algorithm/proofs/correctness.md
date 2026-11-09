---
title: PPSZ returns only models, its forced values are sound, and one try finds a unique model with probability at least 2^(-(1-1/k)n)
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $F$ is a CNF formula over $x_1, \ldots, x_n$ with clauses of at most $k$ literals. $G$ is the formula of line L1: $F$ together with all resolvents of at most $s$ literals that bounded resolution derives. One *try* is lines L3 to L8.

**Termination.** Line L1 adds only clauses of at most $s$ literals over $n$ variables, and never the same clause twice, so it adds at most $\sum_{i \le s} \binom{n}{i} 2^i$ clauses and stops. Each try sets each variable once. The loop of line L2 runs at most $T$ times.

**One-sided correctness.** A try returns $x$ at line L8 only after the check that $x$ satisfies $F$. So each returned assignment is a model, and if $F$ has no model the algorithm reaches line L9. (The implementation also stops at once with "no model" when line L1 derives the empty clause. This answer is right, because a resolvent is implied by its two parents, so a formula that implies the empty clause has no model.)

**Lemma 1 (forced values are sound).** Let $a$ be a model of $F$. If, in a try, all variables set before $v$ have their values in $a$, and $v$ is forced at line L6, then $v$ gets its value in $a$.

*Proof.* Each clause of $G$ is implied by $F$: the clauses of $F$ trivially, and a resolvent $(C \setminus \{x\}) \cup (D \setminus \{\neg x\})$ because a model of $C$ and $D$ makes $x$ true or false, so it makes $D \setminus \{\neg x\}$ or $C \setminus \{x\}$ true. Induction on the order of derivation gives the claim for all of $G$. So $a$ satisfies each clause of $G$. Suppose $v$ is forced by the clause $E \in G$ with the literal $\ell$ of $v$: every other literal of $E$ is on a variable set before $v$, and is false under the current values, which are the values of $a$. Since $a$ satisfies $E$, it must satisfy $\ell$, and line L6 makes $\ell$ true. $\square$

**Theorem 2 (Paturi, Pudlák and Zane 1997).** Suppose $F$ has exactly one model $a$. Then one try, even with $G = F$ (no resolution), returns $a$ with probability at least $2^{-(1 - 1/k) n}$.

*Proof.* *Critical clauses.* For each variable $v$, let $a^{(v)}$ be $a$ with $v$ flipped. It is not a model, so some clause $C_v$ of $F$ is false under $a^{(v)}$. Since $a$ satisfies $C_v$ and differs from $a^{(v)}$ only at $v$, the clause $C_v$ contains a literal $\ell_v$ of $v$ that is true under $a$, and all its other literals are false under $a$. We call $C_v$ a critical clause for $v$.

*Following $a$.* Fix the order $\pi$ of line L3, and consider the run in which each guess at line L7 equals the value in $a$. By Lemma 1 and induction along $\pi$, each variable gets its value in $a$ in this run. Let $\Phi(\pi)$ be the number of variables that are forced in this run. The real try with order $\pi$ returns $a$ if and only if each of the $n - \Phi(\pi)$ guesses is right: a wrong guess sets a variable to the value that is not in $a$, and the only model is $a$, so line L8 fails. The guesses are independent and uniform, so

$$\Pr[\text{the try returns } a \mid \pi] = 2^{-(n - \Phi(\pi))}.$$

*Many forced variables.* If $v$ comes after all other variables of $C_v$ in $\pi$, then $v$ is forced in the run that follows $a$: when line L5 reaches $v$, every other literal of $C_v$ is set and false under $a$, so $C_v$ is a unit clause $(\ell_v)$. The clause $C_v$ has at most $k$ variables, and $\pi$ is uniform, so $v$ is last among them with probability at least $1/k$. By linearity of expectation, $\mathbb{E}[\Phi(\pi)] \ge n/k$.

*Jensen.* The function $t \mapsto 2^{t}$ is convex, so

$$\Pr[\text{the try returns } a] = \mathbb{E}\left[2^{-(n - \Phi(\pi))}\right] \ \ge\ 2^{-(n - \mathbb{E}[\Phi(\pi)])} \ \ge\ 2^{-(1 - 1/k) n}. \qquad \blacksquare$$

Adding the clauses of $G$ can only force more variables in the run that follows $a$, since each clause of $F$ is still in $G$. So the bound also holds for PPSZ with any $s$.

**What bounded resolution adds (cited, not proved here).** Paturi, Pudlák, Saks and Zane (2005) show that with $s = s(n)$ growing slowly to infinity, a variable $v$ is forced in the run that follows a unique model with probability at least $\mu_k / (k - 1) - o(1)$, where $\mu_k = \sum_{j \ge 1} \frac{1}{j (j + 1/(k-1))}$. The proof builds a tree of critical clauses below $v$ and shows that, with $s$ large, the clauses that bounded resolution derives force $v$ whenever the variables of some cut of this tree come before $v$ in $\pi$. The same Jensen step then gives success probability $2^{-(1 - \mu_k/(k-1)) n - o(n)}$, which is $2^{-(2 \ln 2 - 1) n - o(n)} \approx 1.3071^{-n}$ for $k = 3$. Hertli (2014) shows that the same bound holds when $F$ has many models.
