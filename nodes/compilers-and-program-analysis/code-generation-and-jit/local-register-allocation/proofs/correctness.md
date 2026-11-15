---
title: Belady's rule is optimal for local allocation with clean values, and only then
proves: [correctness]
status: full
---

We use the model and the pseudocode of the page. A block is turned into a list of *steps*. A value is a definition of a name, or a parameter. For each instruction, there is a step USE $u$ for each distinct operand $u$, in order, where the earlier operands of the same instruction are *pinned*. Then there is a step DROP $u$ for each operand with no later use, and then a step DEF $x$ for the result. The ret is an instruction with one operand and no result. There are $k \ge 2$ registers.

An *allocation* answers each step. At USE $u$ with $u$ not in a register, it loads $u$ into a free register, or, if there is none, it frees the register of some value that is not pinned, and then loads $u$. At DEF $x$, it puts $x$ into a free register, or frees the register of some value first. A value that is freed while it is dirty costs a store. A load costs 1. The *clean model* is the model in which stores cost 0, which is the same as saying that each value always has a copy in memory.

## Validity

**Lemma 1.** The code that ALLOCATE emits computes the same result as the block, and it never uses more than $k$ registers.

*Proof.* The allocator keeps the map from registers to values exact: a register holds a value only after the load or the instruction that writes it, and the map drops a value when its register is freed or reused. Only registers $r_0, \ldots, r_{k-1}$ exist. A load reads the memory slot of a value. That slot holds the value: a parameter starts there, and a computed value is loaded only after the store that line L9 emits when it frees the register of the dirty value. The slot of a name is not written again while the value is live, because a later definition of the same name comes after the last use of the old value. An instruction reads its operands from the registers that the USE steps recorded. A pinned operand is never freed before the instruction runs, so these registers still hold the operands. Freeing the register of an operand at DEF is safe, because the instruction reads its operands before it writes its result. By induction over the steps, each instruction computes the value of the original one, so the ret returns the same value. $\square$

## The clean model

**Theorem 1.** In the clean model, ALLOCATE with Belady's rule (lines L7 and L8) has the least cost of all allocations of the block.

*Proof.* We map the block to a request sequence $\sigma$ for [demand paging](/demand-paging/) with a cache of size $k$ and an empty initial cache. The pages are the values. Each USE $u$ gives a request for $u$. If the USE step of $u$ has pinned values, it is followed by one more request for each pinned value. Each DEF $x$ gives a request for $x$. DROP steps give no request.

*From allocations to paging.* Take any allocation $A$. It gives a paging schedule $P_A$: keep the same values in the cache as $A$ keeps in registers, except that a dropped value stays in the cache until $A$ reuses its register. The repeated requests of pinned values are hits, since $A$ never frees a pinned value. The request for a defined value $x$ is a fault in every schedule, because $x$ was never requested before. So $P_A$ loads exactly $\mathrm{cost}(A) + D$ pages, where $D$ is the number of DEF steps.

*From LFD to Belady.* By [the optimality of Belady's rule](/belady-optimality/), the schedule LFD, which evicts the page whose next request is furthest away, loads at most as many pages on $\sigma$ as any paging algorithm. We show that LFD on $\sigma$ makes the same choices as ALLOCATE.

- A dropped value has no later request, so LFD evicts it before any live value. This is the same as using the free register at line L7.
- At a fault on the USE of $u$, each pinned value $p$ has its next request just after the request for $u$. The cache is full and has $k \ge 2$ pages, so it holds a page other than $p$ whose next request is later. So LFD never evicts a pinned value, and the repeated requests are hits.
- The repeated requests only add requests for a pinned value right after the USE step. So among values that are not pinned, the order of the next requests in $\sigma$ is the order of the next USE steps, which is the order that line L8 uses.

So LFD on $\sigma$ is $P_B$ for the allocation $B$ that ALLOCATE makes, and it loads $\mathrm{cost}(B) + D$ pages. For each allocation $A$,
$$\mathrm{cost}(B) + D = \mathrm{LFD}(\sigma) \le P_A(\sigma) = \mathrm{cost}(A) + D.$$
So $\mathrm{cost}(B) \le \mathrm{cost}(A)$. $\blacksquare$

Two values never have the same next request in $\sigma$, unless they have none, so the ties of line L8 do not matter for the cost.

## Dirty values

**Claim 2.** When a store costs 1, Belady's rule is not always optimal.

*Proof.* Take $k = 3$ and the block

```
t = b + 1
u = b + t
u = u * a
t = b * t
v = t * u
ret v
```

with the parameters $a$ and $b$ in memory. ALLOCATE loads $b$, computes $t$ and $u$, and then needs a register for $a$ at the third instruction, where $u$ is pinned. The next uses of $b$ and $t$ are the first and the second operand of the fourth instruction, so line L8 frees the register of $t$. The value $t$ is dirty, so this costs a store, and $t$ is loaded again at the fourth instruction. The total is three loads ($b$, $a$, $t$) and one store: 4. The allocation that frees $b$ instead pays no store, and it loads $b$ again at the fourth instruction: three loads ($b$, $a$, $b$), a total of 3. $\square$

In this case, the value with the furthest next use is only one step further than a clean value, but it costs twice as much to free. Belady's rule does not see the difference. The test file checks Theorem 1 and Claim 2 by brute force over all choices of the register to free.
