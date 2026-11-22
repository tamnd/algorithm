---
title: A verified module stores only inside its fault domain, whatever its data and its jumps
proves: [correctness, invariant, termination]
status: full
---

**The model.** Words have $w$ bits. The fault domain of a module is the set of addresses $a$ with $\lfloor a / 2^m \rfloor = g$, for a segment identifier $g$ with $0 \le g < 2^{w - m}$; write $\mathrm{dom}(a)$ for this condition. A module is a finite list of instructions on registers, with the instruction set of the code file: constant loads, additions, loads, stores, the two sandboxing steps SANDBOX$(d, a)$ (line L3) and CHECK$(d, a)$ (line L4), conditional direct jumps, indirect jumps and halt. The register $d$ is the dedicated register. A run starts with any values in the registers other than $d$ and any memory contents, which models an attacker who controls every value the module computes, and with $d$ set to some address in the domain by the trusted loader.

**Lemma 1 (the sandboxing steps).** For every word $a$, $\mathrm{dom}\big((a \wedge (2^m - 1)) \vee g \cdot 2^m\big)$ holds. CHECK$(d, a)$ either faults or sets $d$ to a value $a$ with $\mathrm{dom}(a)$.

*Proof.* The value $a \wedge (2^m - 1)$ is below $2^m$ and has no bits at positions $m$ and above, and $g \cdot 2^m$ has no bits below position $m$. So their OR equals $g \cdot 2^m + (a \wedge (2^m - 1))$, which lies in $[g \cdot 2^m, (g + 1) \cdot 2^m)$, and it is below $2^w$ because $g < 2^{w - m}$. CHECK writes $d$ only after it has tested $\lfloor a / 2^m \rfloor = g$. $\square$

**Invariant (D).** Let $P$ be a module that the verifier accepts (lines L6 to L8). At every step of every run of $P$, the register $d$ holds an address in the domain.

*Proof, by induction on the number of steps.* At the start, the loader set $d$ to a domain address. Assume (D) before a step. If the step runs SANDBOX or CHECK with destination $d$, then by Lemma 1 the new value of $d$ is in the domain, or the run faults and stops. If the step runs any other instruction that writes a register, then its destination is not $d$, because line L6 rejects every module with such an instruction; so $d$ does not change. Stores, jumps and halt write no register. A jump changes only the position in the module, and (D) is a statement about $d$ alone, so it holds at every position, including a position that a run reaches by an indirect jump to the middle of a sandboxed pair. $\square$

**Theorem (confinement).** If the verifier accepts $P$, then every store that a run of $P$ executes writes an address in the domain, for every initial value of the other registers and of memory, and for every sequence of jumps.

*Proof.* By line L7, every store of $P$ has the form STORE$(d, v)$, so it writes the address held in $d$. By (D) that address is in the domain. $\square$

The theorem is the point of the design of Wahbe et al.: the check is on the dedicated register, not on the path that led to the store. So an attacker who controls the values of the module, or who jumps over a sandboxing step, still cannot store outside the domain. The only thing that must be true at every moment is (D), and the verifier makes sure that only the sandboxing steps can change $d$.

**Lemma 2 (the rewriter's output passes the verifier).** If a module $Q$ does not mention $d$, then REWRITE$(Q, d)$ is accepted by the verifier, in both modes.

*Proof.* REWRITE refuses a module that mentions $d$ (line L1). It replaces each store STORE$(a, v)$ by a sandboxing step with destination $d$ followed by STORE$(d, v)$ (lines L2 to L5), and copies every other instruction, with direct jump targets renumbered to the new position of their old target, or to the end of the new module if the old target was the end. The copied instructions do not mention $d$, so line L6 finds no instruction that writes $d$ other than a sandboxing step. Every store of the output goes through $d$, and every direct jump target is in range, so line L7 does not reject. Line L8 accepts. $\square$

**Theorem (transparency).** Let $Q$ be a module without indirect jumps that does not mention $d$. Take a run of $Q$ that halts and in which every store address is in the domain. Then the run of REWRITE$(Q, d)$ from the same initial state, in either mode, halts with the same sequence of stores.

*Proof.* Match each step of the run of $Q$ at position $i$ with the step of the rewritten module at the new position of $i$. Instructions other than stores and jumps are copied, so they compute the same values. A direct jump goes to the renumbered target, which is the new position of the old target. A store STORE$(a, v)$ at position $i$ becomes a sandboxing step and STORE$(d, v)$. By assumption the address in $a$ is in the domain, so the masking step leaves it unchanged (Lemma 1 with $\lfloor a / 2^m \rfloor = g$ gives back $a$), and the checking step passes and copies it. So the store writes the same address and the same value. The register $d$ is not read by any other instruction of $Q$, so its new value changes nothing else. By induction on the steps, the two runs make the same stores and halt together. $\square$

**What the theorems do not say.** They are about stores. In this model loads are not confined, which matches the cheaper variant that protects only writes and jumps; confining reads needs a sandboxing step before each load as well. They say nothing about indirect jumps leaving the module, which a real system confines in the same way with a code segment and a second dedicated register. They need the loader to set $d$ at entry and the verifier to run on the exact code that will run, and they assume that the code cannot be changed after verification, as [data execution prevention](/data-execution-prevention/) provides.

**Termination and cost.** REWRITE and the verifier each make a fixed number of passes over the $n$ instructions, so they take $O(n)$ steps. The interpreter stops after at most its step budget. Each sandboxing step adds one instruction per store in this model and two machine instructions on a RISC processor in the paper of Wahbe et al. $\blacksquare$
