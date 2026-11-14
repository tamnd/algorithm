---
title: Correctness of the Braun SSA construction
proves: [correctness]
status: full
---

We prove that the construction in `impl/python/braun_ssa_construction.py` terminates, that its output is in strict SSA form, and that the output computes the same values as the input on every run. We also prove that every phi-function it keeps lies at a block where its variable is live, and that no trivial phi-function is left. Minimality on reducible graphs is the theorem of Braun et al. (CC 2013, Section 4); we give their argument in outline at the end.

## Setting

The input $P$ is a program without phi-functions. Its control flow graph has entry $r$, $r$ has no predecessors, and every block is reachable from $r$. A *point* is a position between two instructions of a block, or the top or the end of a block. For a run of $P$ and a variable $v$, $\mathrm{val}(v)$ is the value of $v$ at the current step. If $v$ has no value yet, any value counts as correct for it.

The builder fills the blocks in reverse postorder. It seals a block when all its predecessors are filled, and at the end it seals the rest. Every block is then filled and sealed.

The output names are of three kinds: the fresh name of each instruction, the name of each phi-function the builder creates, and the entry names (the parameters and the names $v.0$, which `v.0 = 0` defines at the top of $r$). A removed phi-function forwards to the value that replaced it. Write $\rho(x)$ for the end of the forwarding chain of $x$ after the builder stops. The output writes $\rho(x)$ wherever the builder recorded $x$.

## Facts that hold during the run of the builder

**Fact 1.** Every call `read_variable(v, p)` made from inside `read_variable_recursive` or `add_phi_operands` has $p$ filled.

*Proof.* Such a call is either the single-predecessor case or the operand read of a phi-function. In both cases $p$ is a predecessor of a block $b$ that is sealed at that moment: the single-predecessor case is only taken for a sealed $b$, `add_phi_operands` runs either from `seal_block` or for a sealed $b$ in `read_variable_recursive`. A block is sealed only when all its predecessors are filled. $\square$

So a recursive lookup never enters the block that is being filled, because that block is not yet filled. The first call of a lookup is either at the block being filled, at the current point, or (Fact 1) at the end of a filled block.

**Fact 2.** At most one phi-function for $v$ is ever created in a block $b$.

*Proof.* A phi-function for $v$ at $b$ is created only in `read_variable_recursive(v, b)`, which runs only when `current_def` has no entry for $(v, b)$, and which sets that entry before it returns (line L8) and, in the sealed case, before it recurses (line L6). The entry is never deleted. $\square$

**Fact 3 (termination).** Every lookup ends.

*Proof.* A call `read_variable_recursive(v, b)` either creates a phi-function and records it in `current_def[(v, b)]` before it reads any predecessor, or follows the single predecessor. After the first case, a lookup of $v$ at $b$ stops at once. By Fact 2 this case happens at most once per pair $(v, b)$. A chain of single-predecessor steps cannot run forever: it would follow a cycle in which every block has one predecessor, and no block of such a cycle is reachable from $r$. Each removal of a phi-function deletes one of finitely many phi-functions, so the recursive rechecks also end. $\square$

## Names attached to points

The builder attaches names to points. We call a triple $(x, v, q)$ a *claim*: "$x$ is the name of $v$ at point $q$". The claims are these.

- **(C1) Definitions.** When block $b$ is filled and the instruction at point $q$ assigns $v$ with the fresh name $x$, the claim $(x, v, q')$ holds for each point $q'$ after $q$ in $b$ up to the next assignment of $v$ in $b$, or up to the end of $b$.
- **(C2) Values on entry.** When `read_variable_recursive(v, b)` records the value $x$ (lines L4 to L8), the claim $(x, v, q)$ holds for the top of $b$ and for each point of $b$ before the first assignment of $v$ in $b$. For $b = r$ the builder also records each parameter $p$ as the name of $p$ at the top of $r$.
- **(C3) Phi operands.** When a phi-function $\varphi$ for $v$ at $b$ gets the operand $x$ for the edge $(p, b)$, the claim $(x, v, \mathrm{end}(p))$ holds.

A use of $v$ at point $q$ of block $b$ reads `read_variable(v, b)`. By Fact 1 and the order of filling, this returns either the name of the last assignment of $v$ before $q$ in $b$ (a claim C1 at $q$) or the value recorded for $(v, b)$ (a claim C2 at $q$). A phi operand for the edge $(p, b)$ is the value of `read_variable(v, p)` for a filled $p$, which is a claim C1 or C2 at the end of $p$; C3 records it. So **every name the output reads is the first part of a claim at the point where it is read.**

In the output, every claim $(x, v, q)$ becomes $(\rho(x), v, q)$. We call these the *output claims*.

**Lemma 1 (entry claims).** Let $(x, v, \mathrm{top}(b))$ be an output claim made by C2. Then exactly one of these holds:

1. $x$ is the name of a phi-function for $v$ at $b$ that the output keeps;
2. $b \neq r$, and $(x, v, \mathrm{end}(p))$ is an output claim for every predecessor $p$ of $b$;
3. $b = r$, and $x$ is a parameter or $v.0$.

*Proof.* Look at the case of `read_variable_recursive(v, b)` that recorded the value.

- *Single predecessor $p$.* The recorded value is `read_variable(v, p)`, a claim at the end of $p$. Its image under $\rho$ is $x$. This is case 2.
- *A phi-function $\varphi$ was created* (unsealed block, or sealed block with several predecessors, or $b = r$ with none). Every phi-function becomes complete: an incomplete one gets its operands when $b$ is sealed, and every block is sealed. If the output keeps $\varphi$, then $\rho(\varphi) = \varphi$ and we are in case 1. Otherwise $\varphi$ was replaced. A replacement by `try_remove_trivial_phi` happens when every operand of $\varphi$ is $\varphi$ itself or one value $s$, and then $\varphi$ forwards to $s$. A replacement by the SCC pass happens when $\varphi$ lies in a set of phi-functions whose operands lie in the set or equal one value $w$, and then every member forwards to $w$. In both cases every operand of $\varphi$ has the same image under $\rho$ as $\varphi$, which is $x$. If $b \ne r$, the operand claims C3 give case 2. If $b = r$, $\varphi$ has no operands and is replaced by $v.0$: case 3.
- *The parameter claims at $r$* are case 3. $\square$

Since the output keeps at most one phi-function for $v$ at $b$ (Fact 2), case 1 says that $x$ is that phi-function.

## Single assignment and strictness

Every output name has exactly one definition: fresh names and phi names are new each time, and the entry names are defined once at the top of $r$.

**Theorem 1 (strict).** If the output reads $x$ at point $q$, the definition of $x$ dominates $q$.

*Proof.* There is an output claim $(x, v, q)$. Suppose a path $\pi$ from the top of $r$ to $q$ avoids the definition of $x$. Walk $\pi$ backward from $q$ and carry the claim.

- Inside a block, a claim C1 at $q'$ comes from an assignment of $v$ with name $x$ earlier in the same block, and $\pi$ passes it before $q'$ unless $\pi$ starts later than it, which it does not, because $\pi$ starts at $r$ and enters the block at its top. So every claim we meet inside a block on $\pi$ is a claim C2, which holds from the top of the block.
- At the top of a block $b$, Lemma 1 applies. Case 1 puts the definition of $x$ at the top of $b$, on $\pi$, which is excluded. Case 2 gives the claim at the end of the predecessor that $\pi$ came from, so we can go on. For a claim at the end of a block that is a claim C1, the assignment is in that block and $\pi$, which passed the whole block, passed it; so it is a claim C2 again.
- At the top of $r$, case 3 applies, and $x$ is defined at the top of $r$, on $\pi$.

Each case either contradicts the choice of $\pi$ or moves the claim to an earlier point of $\pi$. Since $\pi$ is finite, we reach a contradiction. $\square$

The same walk shows that every phi-function has one operand per predecessor in the output: the builder gives it one per predecessor when it is completed.

## Same values on every run

**Theorem 2.** Run $P$ and the output on the same arguments. They follow the same path through the blocks, and at every step, for every output claim $(x, v, q)$ with $q$ the current point, the output holds $\mathrm{val}(v)$ in $x$.

*Proof.* By induction on the number of steps. Assume the statement at a step, and look at the next one.

- **Top of $r$.** The claims there are case 3 of Lemma 1. A parameter holds its argument. $v.0$ is a claim only for a $v$ that has no value yet in $P$, and any value is correct for it.
- **An instruction at $q$ in block $b$.** Its operands are names with claims at $q$, so by the hypothesis they hold the values that $P$ reads. The instruction computes the same value, and, for a branch, takes the same edge. If it assigns $v$ with fresh name $x$, the claims at the next point $q'$ for $v$ are claims C1 with name $x$, and $x$ now holds the new value of $v$. For any other variable $u$, a claim at $q'$ is the same claim as at $q$ (C1 and C2 run over a range of points), and its name is a name of $u$, which this step does not write.
- **An edge from $p$ to $b$.** Take a claim $(x, v, \mathrm{top}(b))$. If $x$ comes from a C1 claim, it is not at the top of a block. So Lemma 1 applies. In case 1, $x$ is the phi-function for $v$ at $b$. It receives the value of its operand for $(p, b)$, which has a claim at the end of $p$. All phi-functions of $b$ read their operands before any of them is written, so that value is $\mathrm{val}(v)$ at the end of $p$, which is $\mathrm{val}(v)$ at the top of $b$. In case 2, $(x, v, \mathrm{end}(p))$ is a claim, so $x$ held $\mathrm{val}(v)$ at the end of $p$, and the edge writes only the phi-functions of $b$. A phi-function of $b$ for another variable has a different name, and $x$ is not the phi-function of $b$ for $v$ because case 1 and case 2 exclude each other. So $x$ still holds $\mathrm{val}(v)$.

Every name the output reads has a claim at that point, so every read in the output gets the value that the matching read in $P$ gets, and both programs make the same steps. $\square$

The output has no copies in place of the input's copies (the builder keeps each copy as an instruction), so two names of the same variable are never live at once, and dropping the version numbers gives back a program equivalent to $P$. This is the function `strip_versions`.

## Every phi-function is at a live block

**Theorem 3.** If the builder creates a phi-function for $v$ at $b$, then $v$ is live on entry to $b$ in $P$.

*Proof.* Call a lookup `read_variable(v, c)` *justified* if some path from the point where it asks for $v$ (the current point of $c$ during filling, or the end of $c$ otherwise) reaches a use of $v$ with no assignment of $v$ in between. A lookup made for an operand of an instruction or a terminator is justified by that use. A recursive lookup at a predecessor $p$ of $c$ comes from `read_variable_recursive(v, c)`, which runs only when $c$ has no assignment of $v$ before the point asked for. If the lookup at $c$ was justified, the path from the end of $p$ into $c$ and then on to the use is free of assignments of $v$, so the lookup at $p$ is justified. An operand lookup for an incomplete phi-function at $c$, made when $c$ is sealed, is justified in the same way, because the lookup that created the incomplete phi-function was. By induction every lookup is justified. A phi-function for $v$ at $b$ is created by `read_variable_recursive(v, b)`, for a point of $b$ with no assignment of $v$ before it, so the justifying path starts at the top of $b$. $\square$

## No trivial phi-function is left

**Theorem 4.** In the output, every phi-function has at least two different operands other than itself.

*Proof.* A phi-function is tested by `try_remove_trivial_phi` when its last operand is in (line L10). Its operands can change later only when one of them is replaced. The builder keeps, for every value, the set of phi-functions that use it, and when a phi-function is replaced, its users move to the new value and are tested again (line L14). The SCC pass replaces through the same routine. So every phi-function that is left was tested with its final operands, and the test keeps exactly those with two different operands other than itself. $\square$

## Minimality on reducible graphs (outline)

Braun et al. (CC 2013, Section 4, Theorem 1) prove: *an SSA program with a reducible control flow graph and no trivial phi-function is in minimal SSA form*, that is, every phi-function for $v$ sits at a block where two paths from two different assignments of $v$ first meet. Their argument, in outline:

1. (Lemma 2 of the paper.) If a phi-function $p$ at block $P$ has two distinct operands $q$ and $r$, other than $p$, defined in blocks $Q$ and $R$, then $Q$ and $R$ do not both dominate $P$. Otherwise one of them, say $Q$, dominates the other, and the path from $Q$ through $R$ to the predecessor where $p$ reads $q$ has another definition of $v$ between a definition and its use.
2. (Lemma 3 of the paper.) If $p$ is unnecessary but not trivial, then it has an operand that is itself an unnecessary phi-function whose block does not dominate the block of $p$.
3. (Theorem 1.) Follow such operands from an unnecessary phi-function. The chain must repeat, so the phi-functions form a cycle, which lies on a cycle of the control flow graph. In a reducible graph, that cycle has an entry block that dominates all its blocks, and the phi-function in that block dominates the one before it in the chain, against step 2.

By Theorem 4, the builder's output has no trivial phi-function, so on a reducible graph it is minimal. With Theorem 3, every phi-function it keeps for $v$ lies in $J^+(S_v)$, the iterated join set of the assignments of $v$, at a block where $v$ is live. On irreducible graphs, a cycle of phi-functions can pass a single value around without being trivial, and the SCC pass of Section 3.2 of the paper (`minimize_sccs=True`) removes such cycles.

## Running time

Filling the blocks touches each instruction once. Each pair $(v, b)$ is looked up recursively at most once, so there are $O(V B)$ phi-functions and $O(V E)$ operand reads, where $B$ and $E$ are the numbers of blocks and edges. This gives $O(I + V(B + E))$ before the removal of trivial phi-functions. Each removal retests the users of the removed phi-function; Braun et al. bound these tests by $O(B^2 V^2)$ in total, and the SCC pass by $O(I + B (B + E) V^2)$.
