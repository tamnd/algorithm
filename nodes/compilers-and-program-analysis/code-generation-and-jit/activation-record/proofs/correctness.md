---
title: Static links and displays find the right frame for each variable
proves: [correctness]
status: full
---

We use the language, the frame layout and the pseudocode of the page. The *depth* of main is 0, and a function declared inside a function of depth $d$ has depth $d + 1$. The *lexical chain* of a function $g$ is the list $g_0, g_1, \ldots, g_d = g$, where $g_0$ is main and each $g_{j+1}$ is declared inside $g_j$.

## The reference semantics

The direct evaluator gives the meaning. An environment is a record $(g, V, P)$: the function $g$, a map $V$ from the parameters and locals of $g$ to values, and the environment $P$ of the enclosing function. A variable $x$ is looked up by following $P$ from the current record to the first record whose $V$ has $x$. A call to $f$ follows $P$ to the first record $(g_i, \cdot, \cdot)$ such that $f$ is declared in $g_i$, and the new record is $(f, V', \text{that record})$. So the $P$ chain of an environment of $g$ has one record for each function of the lexical chain of $g$, in order, and the record of $g_j$ is $d - j$ steps away.

The compiler resolves names in the same way at compile time. For $x$ in the body of $g$, it takes the largest $j$ such that $g_j$ declares $x$, and emits LOAD with $h = d - j$ hops and the offset of $x$ in the frame of $g_j$. Since the $P$ chain of $g$ follows the lexical chain, this $g_j$ is the record where the evaluator finds $x$. The same holds for STORE, and for CALL, where the compiler takes the largest $i$ such that $g_i$ declares $f$ and emits $d - i$ hops.

## The invariant

Map each environment record $E$ to a frame $\phi(E)$ on the stack: the frame of the activation that created $E$. We say that the machine *simulates* the evaluator when:

1. each active frame $\phi(E)$ holds, at the offset of each variable of $E$, the value that $E$ maps it to;
2. for each active frame $\phi(E)$ with $E = (g, V, P)$ and $g \ne$ main, the static link slot of $\phi(E)$ holds the address of $\phi(P)$;
3. the frames of the records on the current $P$ chain are active.

**Lemma 1.** If the machine simulates the evaluator and the current function is $g$ of depth $d$, then following $h \le d$ static links from FP reaches $\phi$ of the record of $g_{d-h}$.

*Proof.* By induction on $h$. For $h = 0$ it is the current frame. Each step goes from $\phi(E)$ to $\phi(P)$ by part 2, which is one step along the $P$ chain, and by part 3 the frame is still there. $\square$

**Theorem 1.** For each program and each limit on the number of calls, the machine with static links returns the same value as the evaluator, or both run out of calls.

*Proof.* We show that each step of the machine keeps the invariant, and that each expression leaves on the stack the value that the evaluator computes. The proof is by induction on the steps of the evaluator.

- LOAD and STORE: by Lemma 1 and the compile-time resolution, the frame reached is $\phi$ of the record where the evaluator finds $x$, and by part 1 the slot holds its value. STORE changes the slot and the record in the same way.
- CALL to $f$ (lines L1 to L3): MARK reserves the header and the arguments are evaluated on top of it, so the new frame starts at $\mathrm{SP} - n - 3$, with the arguments at offsets $3, \ldots, n + 2$. The static link is found with $d - i$ hops, which by Lemma 1 reaches $\phi$ of the record of $g_i$, the record that the evaluator takes as $P$ for the new record. So part 2 holds for the new frame. ENTER (line L4) puts the locals, set to 0, after the arguments, as the evaluator does. The new frame is on top of the old ones, so the frames of the $P$ chain stay active, and part 3 holds.
- RET (lines L5 and L6) reads the return address and the dynamic link before it pops the frame, pushes the result, and gives the caller back its FP. The frames below are unchanged, so the invariant holds for the caller.

The machine counts a call at CALL, after the arguments, and the evaluator counts it after it evaluates the arguments, in the same left-to-right order. So both stop at the same call when the limit is reached. $\blacksquare$

## The display

**Theorem 2.** The display variant returns the same value as the static link variant.

*Proof.* Let $D[0..63]$ be the display. We show that, while the current function is $g$ of depth $d$, $D[j]$ is $\phi$ of the record of $g_j$ for each $j \le d$. Then LOADD with the depth $j$ of the declaring function reaches the same frame as LOAD with $d - j$ hops, by Lemma 1.

When $g$ calls $f$, declared in $g_i$, the depth of $f$ is $i + 1 \le d + 1$. The entries $D[0..i]$ are $\phi$ of the records of $g_0, \ldots, g_i$, which are also the first $i + 1$ functions of the lexical chain of $f$, with the same records, since the evaluator takes the record of $g_i$ as $P$. ENTER saves $D[i+1]$ in the frame and sets $D[i+1]$ to the new frame. So the claim holds for $f$. RET restores the saved $D[i+1]$, and the entries $D[0..i]$ were not changed by $f$ when it returns, because every call inside $f$ restores the entry it changed. So the claim holds again for $g$. The entries above the depth of the current function are never read. $\blacksquare$

## The dynamic link is not the static link

The dynamic link of a frame points to the frame of the caller. It equals the static link only when the caller is the enclosing function. In the program of the page, $g$ calls $f$, and both are declared in main. In the frame of $f$, the static link points to main and the dynamic link points to $g$. LOAD of $x$ with 1 hop along the dynamic link reads the slot at offset 3 of the frame of $g$, which holds $y = 2$, not $x = 1$. This is the rule of dynamic scoping, not of lexical scoping.
