---
title: Interprocedural constant propagation with jump functions is sound
proves: [correctness]
status: full
---

**Setting.** A whole program is a set of procedures with a distinguished procedure $\mathit{main}$. Each procedure has formals and uses only `const`, `copy`, `op` and `call` instructions, so a callee cannot read or write a variable of its caller. A run starts with one activation of $\mathit{main}$ on any arguments. A call creates a new activation of the callee whose formals hold the argument values, and the caller waits until the callee returns. For an activation $A$ of a procedure $f$, write $\sigma_A(q)$ for the value of formal $q$ when $A$ starts.

**Lattices.** The local analysis uses the values $\mathrm{Const}(k)$, $\mathrm{Formal}(q)$ and $\bot$. Within one activation $A$, a value describes a set of integers: $\gamma_A(\mathrm{Const}(k)) = \{k\}$, $\gamma_A(\mathrm{Formal}(q)) = \{\sigma_A(q)\}$, and $\gamma_A(\bot)$ is every value, together with "not defined yet". The interprocedural values are $\top$, $\mathrm{Const}(k)$ and $\bot$, with $\gamma(\top) = \emptyset$, $\gamma(\mathrm{Const}(k)) = \{k\}$ and $\gamma(\bot)$ every integer. In both lattices, $u \sqsubseteq v$ means $u = v$, or $u = \bot$, or $v = \top$. Then $u \sqcap v \sqsubseteq u$ and $u \sqcap v \sqsubseteq v$, and $u \sqsubseteq v$ implies $\gamma(v) \subseteq \gamma(u)$.

**What we prove.** Let VAL be the result of lines L2 to L11.

- **Theorem 1 (soundness).** If $\mathrm{VAL}[f, p] = \mathrm{Const}(c)$, then in every run, every activation of $f$ starts with $p = c$.
- **Theorem 2 (same behavior).** The program of line L12 has the same outcome as the old one on every input: the same returned value, a trap, or no end.
- **Theorem 3 (termination).** The worklist loop stops.

## 1. The local analysis

Fix a procedure $f$. The analysis of line L1 assigns a state $S_B$, a map from names to local values, to each block $B$ that it reaches. The entry state maps each formal $q$ to $\mathrm{Formal}(q)$ and every other name to $\bot$. The transfer of an instruction is: `x = k` gives $\mathrm{Const}(k)$, `x = y` copies the value of $y$, `x = a op b` gives $\mathrm{Const}(a \mathbin{op} b)$ if both operands are constants and the operation does not trap, and $\bot$ otherwise, and `x = call g(...)` gives $\bot$. Write $T_B$ for the transfer of the whole block $B$.

**Lemma 1 (local fixed point).** When the local worklist is empty, every successor $t$ of a reached block $B$ is reached and $S_t \sqsubseteq T_B(S_B)$ for every name.

*Proof.* A block's state only goes down: the first time it is set, and later only by a meet with a new value. Every time $S_B$ changes, $B$ goes into the worklist, if it is not already there. So after the last change of $S_B$, the block $B$ is taken out and processed with its final state. That step sets $S_t$ for an unreached $t$, or replaces $S_t$ by $S_t \sqcap T_B(S_B)$, which is $\sqsubseteq T_B(S_B)$. Later changes only lower $S_t$. Each name can lower at most once below its first value, since $\bot$ is the only value below a constant or a symbol, so the number of changes is finite and the worklist empties. $\square$

**Lemma 2 (local soundness).** Let $A$ be an activation of $f$. Each time $A$ is at the start of a block $B$, the block is reached by the analysis, and for every name $x$ the current value of $x$ in $A$ lies in $\gamma_A(S_B(x))$. The same holds at every instruction of $B$ for the state that the analysis computes at that instruction.

*Proof.* Induction on the steps of $A$. At the start, $A$ is at the entry. A formal $q$ holds $\sigma_A(q) \in \gamma_A(\mathrm{Formal}(q))$, and any other name is in $\gamma_A(\bot)$. Inside a block, each kind of instruction keeps the property. For a constant, a copy or a folded operation this is direct: if both operands hold $a$ and $b$, then $x$ gets $a \mathbin{op} b$, the value that the analysis computed. If the operation traps, $A$ ends and nothing more is claimed. A call writes only its target $x$, whose value is $\bot$, because the callee works on its own variables and cannot change those of $A$. No instruction changes $\sigma_A$. At the end of $B$, control moves to a successor $t$. The values satisfy $T_B(S_B)$, and by Lemma 1 the block $t$ is reached and $S_t \sqsubseteq T_B(S_B)$, so $\gamma_A(T_B(S_B)(x)) \subseteq \gamma_A(S_t(x))$. $\square$

**Corollary 3 (jump functions).** Let $s$ be a call site in $f$ and $J_{s,i}$ the value of its $i$-th argument in the state at $s$. If an activation $A$ of $f$ executes $s$, then $s$ is in a reached block, so line L1 records it, and the $i$-th argument value $a_i$ lies in $\gamma_A(J_{s,i})$. That is, $a_i = k$ if $J_{s,i} = \mathrm{Const}(k)$, and $a_i = \sigma_A(q)$ if $J_{s,i} = \mathrm{Formal}(q)$.

## 2. The propagation

For a jump function $J$ and a map $V$ from the formals of $f$ to interprocedural values, let $\mathrm{ev}(J, V)$ be $\mathrm{Const}(k)$ for $J = \mathrm{Const}(k)$, $V(q)$ for $J = \mathrm{Formal}(q)$, and $\bot$ for $J = \bot$. This is line L10. It is monotone in $V$.

**Lemma 4 (global fixed point).** When the loop of line L5 stops, for every procedure $f$ in REACHED and every recorded call site $s$ in $f$ with callee $g$: $g$ is in REACHED, and $\mathrm{VAL}[g, p_i] \sqsubseteq \mathrm{ev}(J_{s,i}, \mathrm{VAL}[f, \cdot])$ for every argument position $i$, where $p_i$ is the $i$-th formal of $g$.

*Proof.* Every value of VAL only goes down, since line L11 replaces a value by its meet with another. A procedure goes into $W$ when it enters REACHED (lines L4 and L8) and every time one of its values changes (line L11). Let $t$ be the last moment at which $f$ entered REACHED or a value $\mathrm{VAL}[f, \cdot]$ changed. At $t$, $f$ is in $W$, so it is taken out later, at line L6, with its final values. Lines L7 to L11 then put $g$ into REACHED and make $\mathrm{VAL}[g, p_i] \sqsubseteq \mathrm{ev}(J_{s,i}, \mathrm{VAL}[f, \cdot])$. After that, the right side does not change and the left side only goes down, so the relation still holds at the end. $\square$

**Lemma 5 (no $\top$ in a reached procedure).** At the end, $\mathrm{VAL}[f, p] \ne \top$ for every $f$ in REACHED and every formal $p$ of $f$.

*Proof.* Induction on the order in which procedures enter REACHED. The formals of $\mathit{main}$ are $\bot$. A procedure $g$ enters REACHED at line L8 for a call site $s$ in a procedure $f$ that is already in REACHED. In the same step, line L11 lowers each $\mathrm{VAL}[g, p_i]$ to at most $\mathrm{ev}(J_{s,i}, \mathrm{VAL}[f, \cdot])$, which is a constant, $\bot$, or a value $\mathrm{VAL}[f, q]$ that is not $\top$ by the induction hypothesis, since values only go down. $\square$

## 3. Soundness

**Theorem 1.** In every run, every activation $A$ of a procedure $f$ has $f \in \mathrm{REACHED}$, and $\sigma_A(p) \in \gamma(\mathrm{VAL}[f, p])$ for every formal $p$ of $f$. In particular, $\mathrm{VAL}[f, p] = \mathrm{Const}(c)$ implies $\sigma_A(p) = c$.

*Proof.* Induction on the order in which the activations start. The first activation is of $\mathit{main}$, which is in REACHED with all formals $\bot$, and $\gamma(\bot)$ contains every integer.

Let an activation $B$ of $g$ start from a call site $s$ executed by an earlier activation $A$ of $f$. By the induction hypothesis, $f \in \mathrm{REACHED}$ and $\sigma_A(q) \in \gamma(\mathrm{VAL}[f, q])$ for every formal $q$ of $f$. By Corollary 3, $s$ is recorded, and the argument $a_i$ is in $\gamma_A(J_{s,i})$. We show $a_i \in \gamma(\mathrm{ev}(J_{s,i}, \mathrm{VAL}[f, \cdot]))$:

- if $J_{s,i} = \mathrm{Const}(k)$, then $a_i = k$ and $\mathrm{ev} = \mathrm{Const}(k)$;
- if $J_{s,i} = \mathrm{Formal}(q)$, then $a_i = \sigma_A(q) \in \gamma(\mathrm{VAL}[f, q]) = \gamma(\mathrm{ev})$;
- if $J_{s,i} = \bot$, then $\mathrm{ev} = \bot$, which contains every integer.

By Lemma 4, $g \in \mathrm{REACHED}$ and $\mathrm{VAL}[g, p_i] \sqsubseteq \mathrm{ev}(J_{s,i}, \mathrm{VAL}[f, \cdot])$, so $\gamma(\mathrm{ev}) \subseteq \gamma(\mathrm{VAL}[g, p_i])$. Since $\sigma_B(p_i) = a_i$, the claim holds for $B$. $\square$

The proof never uses that the call graph is acyclic, so recursion is covered. A procedure that no activation ever reaches may keep $\top$, and $\gamma(\top) = \emptyset$ says correctly that no activation of it exists.

## 4. The transformation

**Theorem 2.** The program of line L12 has the same outcome as the old one on every input.

*Proof.* Line L12 changes a procedure $f$ only by a new entry block that runs `p = c` for each formal with $\mathrm{VAL}[f, p] = \mathrm{Const}(c)$, and then jumps to the old entry. Run both programs side by side on the same input, and match each activation of the new program with the activation of the old one that the same call creates. By Theorem 1, in the old program every activation of $f$ starts with $p = c$, so the new entry block writes to each such $p$ the value that it already holds. After the jump, the matched activations have equal variables and are at the same block, and they run the same instructions on the same values. A call in one is a call in the other, with the same arguments, so by induction on the order of the activations, the theorem applies to the callee too. So the two runs make the same calls, take the same branches, return the same values and trap at the same instruction. The only difference is the extra steps of the new entry blocks. $\square$

Theorem 1 holds for the old program, and the matching shows that both programs create the same activations, so the claim also holds in the new program. A later pass may therefore replace uses of $p$ in $f$ by $c$ or fold them.

## 5. Termination

**Theorem 3.** The worklist loop stops after at most $\sum_f (1 + 2 k_f)$ iterations, where $k_f$ is the number of formals of $f$.

*Proof.* Each iteration takes one procedure out of $W$. A procedure goes into $W$ once when it enters REACHED, and once each time one of its values goes down. A value goes down at most twice, from $\top$ to a constant and from a constant to $\bot$, because a meet of two different constants is $\bot$. $\square$
