---
title: The verification conditions are sound, exact on loop-free code, and the compact form has the same meaning
proves: [correctness]
status: full
---

**Setting.** States map variable names to integers. Expressions and statements are those of the page: skip, $x := e$, assert $p$, assume $p$, sequence, if, and while $b$ invariant $I$ do $B$. A run of a statement from a state either fails at an assert, is blocked at an assume, ends in a final state, or does not stop. A run is *correct for $Q$* when no assert fails and the run is blocked or ends in a state of $Q$. $\mathrm{WP}(S, Q)$ is the formula that the function WP of the page returns, and $\mathrm{side}(S, Q)$ is the list of formulas that it appends. Write $\sigma \models F$ when the formula $F$ is true in the state $\sigma$. For a formula $R$, $R[e/x]$ is true in $\sigma$ exactly when $R$ is true in $\sigma[x \mapsto e(\sigma)]$; this is the substitution lemma of first-order logic, and it holds here because expressions have no side effects and no bound names clash.

## Lemma 1: exactness for loop-free statements

**Claim.** Let $S$ be loop-free. For every formula $Q$ and state $\sigma$: $\sigma \models \mathrm{WP}(S, Q)$ if and only if the run of $S$ from $\sigma$ is correct for $Q$.

**Proof.** Induction on $S$.

- skip: the run ends in $\sigma$, and WP returns $Q$.
- $x := e$: the run ends in $\sigma[x \mapsto e(\sigma)]$, and $\sigma \models Q[e/x]$ exactly when that state satisfies $Q$.
- assert $p$: the run fails when $\sigma \not\models p$ and ends in $\sigma$ otherwise. So it is correct exactly when $\sigma \models p \wedge Q$.
- assume $p$: the run is blocked when $\sigma \not\models p$ and ends in $\sigma$ otherwise. So it is correct exactly when $\sigma \models p \Rightarrow Q$.
- $S_1; S_2$: the run of the sequence is correct for $Q$ exactly when the run of $S_1$ is correct for the set of states from which $S_2$ runs correctly for $Q$. A run of $S_1$ that fails or is blocked is a run of the sequence that fails or is blocked. By induction on $S_2$, that set is $\mathrm{WP}(S_2, Q)$, and by induction on $S_1$, the condition is $\sigma \models \mathrm{WP}(S_1, \mathrm{WP}(S_2, Q))$.
- if $b$ then $S_1$ else $S_2$: if $\sigma \models b$, the run is the run of $S_1$, and WP reduces to $\mathrm{WP}(S_1, Q)$ in $\sigma$. The other case is symmetric. $\square$

**Consequence.** For loop-free $S$ the list of VCs is the single formula $P \Rightarrow \mathrm{WP}(S, Q)$. For any set of states $B$, this formula holds in every state of $B$ if and only if every run of $S$ from a state of $B \cap P$ is correct for $Q$. With $B$ the box of the tests, this is the exact statement that the random test checks; with $B$ all states, it says that the VC is valid exactly when the program is correct.

## Lemma 2: soundness with loops, relative to a set of states

**Claim.** Let $B$ be a set of states, $S$ a statement and $Q$ a formula. Suppose that every formula of $\mathrm{side}(S, Q)$ holds in every state of $B$. Let $\sigma \models \mathrm{WP}(S, Q)$, and suppose the run of $S$ from $\sigma$ stops (it fails, is blocked or ends) and every state of that run at the head of a loop is in $B$. Then the run is correct for $Q$.

**Proof.** Induction on $S$. The cases skip, assignment, assert and assume are as in Lemma 1. For $S_1; S_2$: $\mathrm{side}(S, Q)$ contains $\mathrm{side}(S_2, Q)$ and $\mathrm{side}(S_1, \mathrm{WP}(S_2, Q))$. The run of $S_1$ from $\sigma$ stops and its loop heads are among those of the whole run, so by induction it is correct for $\mathrm{WP}(S_2, Q)$. If it fails or is blocked, so is the whole run. Otherwise it ends in $\tau \models \mathrm{WP}(S_2, Q)$, and the induction on $S_2$ applies to the rest of the run. The if case is the same, with the branch that the run takes.

For while $b$ invariant $I$ do $B'$, WP returns $I$, and the side list contains $C_1 = (I \wedge b) \Rightarrow \mathrm{WP}(B', I)$, $C_2 = (I \wedge \neg b) \Rightarrow Q$ and the side list of $\mathrm{WP}(B', I)$. Let $\tau_0 = \sigma, \tau_1, \tau_2, \dots$ be the states of the run at the loop head. They are in $B$. We show by induction on $k$ that every $\tau_k$ that the run reaches satisfies $I$ and that the run up to $\tau_k$ has failed no assert. For $k = 0$, $\sigma \models I$ by hypothesis. Let $\tau_k \models I$. If $\tau_k \not\models b$, the loop ends in $\tau_k$, and $C_2$ in $\tau_k \in B$ gives $\tau_k \models Q$: the run is correct. If $\tau_k \models b$, then $C_1$ in $\tau_k$ gives $\tau_k \models \mathrm{WP}(B', I)$. The run of $B'$ from $\tau_k$ stops, because the whole run stops, and its loop heads are among those of the whole run, so by induction on $B'$ it is correct for $I$: it fails no assert, and it is blocked or ends in $\tau_{k+1} \models I$. Since the whole run stops, it passes the loop head only finitely often, so one of the ending cases occurs. $\square$

**Theorem (soundness).** If every formula of $\mathrm{VCGEN}(P, S, Q)$ holds in every state of $B$, then every run of $S$ from a state $\sigma \in B \cap P$ that stops, and whose loop-head states are in $B$, is correct for $Q$. When $B$ is the set of all states, this is the usual soundness of VC generation for partial correctness: valid VCs imply $\{P\}\ S\ \{Q\}$.

**Proof.** The main VC in $\sigma$ gives $\sigma \models \mathrm{WP}(S, Q)$, and the side VCs hold in $B$. Apply Lemma 2. $\square$

The converse fails as soon as there is a loop, because the side VCs ask for more than correctness: they ask that $I$ is inductive in every state, also in states that no run reaches. The page shows this with the invariant $x = qy + r$ of the division program.

## Lemma 3: the compact VC means the same

**Claim.** Let $S$ be loop-free. For every state $\rho$, the formula $\mathrm{COMPACT}(P, S, Q)$ is true in $\rho$ exactly when $P \Rightarrow \mathrm{WP}(S, Q)$ is.

**Proof.** The compact formula is $\mathbf{let}\ D\ \mathbf{in}\ (P \Rightarrow \mathrm{pwp}(S', Q[\sigma_f]))$, where $D$ is the list of definitions $v = e_v$ in the order in which pass 1 made them, $S'$ is the passive statement, $\sigma_f$ maps each variable to its last version, and $Q[\sigma_f]$ is $Q$ with each variable renamed by $\sigma_f$. Each $e_v$ uses only the original variables and versions defined before $v$, so evaluating the lets in $\rho$ gives one extension $\rho_D$ of $\rho$. The let that pass 2 puts at a join only gives a name to a formula, so $\mathrm{pwp}(T, R)$ has the same truth value as the plain weakest precondition $\mathrm{wp}(T, R)$ of the passive statement, with $\mathrm{wp}(T_1 \sqcap T_2, R) = \mathrm{wp}(T_1, R) \wedge \mathrm{wp}(T_2, R)$.

For a substitution $\sigma$ from variables to versions, write $F[\sigma]$ for the renamed formula. We show: if pass 1 maps the statement $T$ with the input map $\sigma$ to the passive statement $T'$ and the output map $\sigma_T$, then for every formula $R$,

$$\rho_D \models \mathrm{wp}(T', R[\sigma_T]) \iff \rho_D \models \mathrm{WP}(T, R)[\sigma].$$

Induction on $T$.

- skip: $T' = \mathbf{skip}$ and $\sigma_T = \sigma$.
- $x := e$: $T' = \mathbf{skip}$, and $\sigma_T = \sigma[x \mapsto v]$, where $D$ defines $v = e[\sigma]$. In $\rho_D$ the version $v$ has the value of $e[\sigma]$. So $R[\sigma_T]$ and $R[e/x][\sigma]$ both read every variable $y \ne x$ from $\sigma(y)$ and read $x$ as the value of $e[\sigma]$; they have the same truth value.
- assert $p$ and assume $p$: $T'$ is assert $p[\sigma]$ or assume $p[\sigma]$, and the rules of wp and WP agree after renaming.
- $T_1; T_2$: with $\sigma \to \sigma_1 \to \sigma_2$, $\mathrm{wp}(T_1'; T_2', R[\sigma_2]) = \mathrm{wp}(T_1', \mathrm{wp}(T_2', R[\sigma_2]))$. By induction on $T_2$, the inner formula is equivalent in $\rho_D$ to $\mathrm{WP}(T_2, R)[\sigma_1]$. A passive statement does not change the state, so wp of $T_1'$ is monotone in the truth value of its postcondition at the single state $\rho_D$, and we can replace the inner formula by an equivalent one. Then induction on $T_1$ with $R_1 = \mathrm{WP}(T_2, R)$ gives $\mathrm{WP}(T_1, \mathrm{WP}(T_2, R))[\sigma]$.
- if $b$ then $T_1$ else $T_2$: pass 1 defines $g = b[\sigma]$, passifies $T_1$ to $(T_1', \sigma_1)$ and $T_2$ to $(T_2', \sigma_2)$, and for each $x$ with $\sigma_1(x) \ne \sigma_2(x)$ defines $x_m = \mathrm{ite}(g, \sigma_1(x), \sigma_2(x))$; $\sigma_T$ maps such $x$ to $x_m$ and the other variables to $\sigma_1(x) = \sigma_2(x)$. Suppose $\rho_D \models g$. Then $\rho_D$ gives each $x_m$ the value of $\sigma_1(x)$, so $R[\sigma_T]$ and $R[\sigma_1]$ have the same truth value. The passive statement is $(\mathbf{assume}\ g; T_1') \sqcap (\mathbf{assume}\ \neg g; T_2')$, and its wp in $\rho_D$ reduces to $\mathrm{wp}(T_1', R[\sigma_T])$, which is equivalent to $\mathrm{wp}(T_1', R[\sigma_1])$ by the same monotonicity, and by induction to $\mathrm{WP}(T_1, R)[\sigma]$. On the other side, $\mathrm{WP}(T, R)[\sigma]$ reduces to $\mathrm{WP}(T_1, R)[\sigma]$ because $b[\sigma] = g$ holds. The case $\rho_D \not\models g$ is symmetric.

At the top, $\sigma$ is the identity, so the right side is $\mathrm{WP}(S, Q)$. $P$ mentions only original variables, which $\rho_D$ reads from $\rho$. So the compact formula is true in $\rho$ exactly when $P \Rightarrow \mathrm{WP}(S, Q)$ is. $\square$

## Lemma 4: sizes

Size is the number of nodes of a formula as a tree; a let counts one node plus its two parts.

**Naive wp can be exponential.** Let $S_n$ be $n$ copies of "if $0 < x$ then $x := x - 1$ else $x := x + 1$". Then $\mathrm{WP}(S_n, Q) = (0 < x \Rightarrow W[x - 1/x]) \wedge (\neg(0 < x) \Rightarrow W[x + 1/x])$ with $W = \mathrm{WP}(S_{n-1}, Q)$, so the size at least doubles at each step and is at least $2^n$. The formula has a copy of $Q$ for each of the $2^n$ choices of signs, with $x$ replaced by a term that records the choices in order, such as $((x - 1) + 1) - 1$. These $2^n$ terms are different, so even a DAG that shares equal subterms has at least $2^n$ nodes.

**The compact VC is polynomial.** Let $|T|$ be the number of nodes of a passive statement, each assert or assume counted with the size of its formula. We show $\mathrm{size}(\mathrm{pwp}(T, R)) \le 4|T| + \mathrm{size}(R)$ by induction. skip: $\mathrm{size}(R)$. assert or assume $e$: $1 + \mathrm{size}(e) + \mathrm{size}(R)$. Sequence: $\mathrm{pwp}(T_1, \mathrm{pwp}(T_2, R))$ has size at most $4|T_1| + 4|T_2| + \mathrm{size}(R)$. Choice with $R$ a single name: $1 + (4|T_1| + 1) + (4|T_2| + 1) \le 4(|T_1| + |T_2| + 1) + 1$. Choice with a larger $R$: the let has $R$ once and two references to its name, $1 + \mathrm{size}(R) + 1 + (4|T_1| + 1) + (4|T_2| + 1) \le 4(|T_1| + |T_2| + 1) + \mathrm{size}(R)$.

Pass 1 makes a passive statement with $O(1)$ nodes per statement plus the formulas of the asserts, assumes and conditions, renamed name for name, so $|S'| = O(|S|)$. The definitions cost $\mathrm{size}(e) + O(1)$ per assignment, $\mathrm{size}(b) + O(1)$ per if, and $O(1)$ per merged version. There are at most $V$ merged versions per if, where $V$ is the number of variables, so the compact VC has size $O(|S| + |P| + |Q| + V \cdot k)$, where $k$ is the number of ifs. This is $O(|S|^2)$ in the worst case and linear when the number of variables is bounded, the same bounds that Flanagan and Saxe give. $\blacksquare$
