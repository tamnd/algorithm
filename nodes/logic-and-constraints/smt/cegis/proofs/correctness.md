---
title: CEGIS returns only correct programs, and it stops when the candidate space or the input space is finite
proves: [correctness, termination]
status: full
---

**Setting.** A synthesis problem has a set $C$ of candidates, a set $X$ of inputs, and a specification $\mathrm{ok}(c, x)$ that says whether candidate $c$ behaves correctly on input $x$. (In the implementation, $\mathrm{ok}(c, x)$ is $\mathrm{spec}(x, \mathrm{run}(c, x))$.) A candidate is *correct* if $\mathrm{ok}(c, x)$ holds for all $x \in X$. For a set $E \subseteq X$ of examples, write $C_E = \{ c \in C : \mathrm{ok}(c, x) \text{ for all } x \in E \}$ for the candidates *consistent* with $E$.

The two oracles have these contracts.

- **Synthesizer** (line L3). On input $E$, it returns an element of $C_E$, or "none" only if $C_E = \emptyset$.
- **Verifier** (line L5). On input $c$, it returns an $x \in X$ with $\neg \mathrm{ok}(c, x)$, or "none" only if $c$ is correct.

The loop starts with a set $E_0$ of examples (line L1; empty in the plain form). Round $k \ge 1$ calls the synthesizer on $E_{k-1}$ and gets $c_k$; if $c_k$ is not "none", it calls the verifier on $c_k$ and gets $x_k$, and line L7 sets $E_k = E_{k-1} \cup \{x_k\}$.

**Lemma 1 (soundness).** If the loop returns a candidate $c$ at line L6, then $c$ is correct. If it returns "none" at line L4, then no candidate is correct.

*Proof.* Line L6 returns $c_k$ only when the verifier answered "none" on $c_k$, and by its contract this happens only if $c_k$ is correct. Line L4 returns only when the synthesizer answered "none" on $E_{k-1}$, so $C_{E_{k-1}} = \emptyset$. Each correct candidate is consistent with every set of examples, so it would lie in $C_{E_{k-1}}$. Hence no correct candidate exists. $\square$

**Lemma 2 (progress).** Suppose round $k$ reaches line L7. Then:

(a) $x_k \notin E_{k-1}$, so $|E_k| = |E_{k-1}| + 1$;

(b) $c_k \in C_{E_{k-1}}$ and $c_k \notin C_{E_k}$, so $C_{E_k} \subsetneq C_{E_{k-1}}$.

*Proof.* The synthesizer returned $c_k \in C_{E_{k-1}}$, so $\mathrm{ok}(c_k, x)$ holds for all $x \in E_{k-1}$. The verifier returned $x_k$ with $\neg \mathrm{ok}(c_k, x_k)$. So $x_k \notin E_{k-1}$, which is (a). Since $x_k \in E_k$, the candidate $c_k$ is not consistent with $E_k$, and $E_{k-1} \subseteq E_k$ gives $C_{E_k} \subseteq C_{E_{k-1}}$, which is (b). $\square$

**Lemma 3 (termination).** If $C$ is finite, the loop stops after at most $|C| + 1$ rounds. If $X$ is finite, it stops after at most $|X \setminus E_0| + 1$ rounds.

*Proof.* Suppose rounds $1, \ldots, r$ all reach line L7. By Lemma 2(b), the sets $C_{E_0} \supsetneq C_{E_1} \supsetneq \cdots \supsetneq C_{E_r}$ strictly decrease, so $|C_{E_r}| \le |C_{E_0}| - r \le |C| - r$, and $r \le |C|$. By Lemma 2(a), the sets $E_k$ gain one new input of $X \setminus E_0$ in each round, so $r \le |X \setminus E_0|$. Round $r + 1$ then ends at line L4 or line L6, since a round that does not reach line L7 returns. $\square$

**Theorem.** Let $C$ or $X$ be finite, and let the oracles satisfy their contracts. Then CEGIS stops after at most $\min(|C|, |X|) + 1$ rounds. It returns a correct candidate if one exists, and "none" otherwise.

*Proof.* Termination and the bound are Lemma 3. When the loop stops, it stops at line L4 or line L6. If a correct candidate exists, line L4 cannot return, because by Lemma 1 a return at line L4 means that none exists; so the loop returns at line L6, and the candidate is correct by Lemma 1. If no correct candidate exists, line L6 cannot return, by Lemma 1; so the loop returns "none" at line L4. $\square$

**Remark (the implementation).** The default synthesizer scans the list of candidates and returns the first one that is consistent with the examples, and the default verifier scans the list of inputs and returns the first input that fails. Both meet their contracts. The list of candidates is fixed, and by Lemma 2(b) the first consistent candidate moves strictly forward in the list. So the returned program is the first correct candidate in the list, which the tests compare with brute force.

**Remark (infinite spaces).** If both $C$ and $X$ are infinite, the loop may run forever. Take $X = \mathbb{N}$, the specification "the output is 0", and candidates $c_n$ that output 0 on the inputs below $n$ and 1 on the others. A synthesizer that returns $c_{n}$ with $n$ larger than all examples meets its contract, and the verifier then returns the input $n$. This loop never ends, whether or not the constant program 0 is also a candidate. Lemma 1 still holds, so each answer that the loop gives is right. $\blacksquare$
