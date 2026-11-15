---
title: Local value numbering keeps the outcome of every run
proves: [correctness]
status: full
---

**Setting.** The proof is about one basic block $B$ with instructions $I_1, \ldots, I_n$, and the block $B'$ with instructions $I'_1, \ldots, I'_n$ that LVN returns. The algorithm keeps instruction $i$ at position $i$: $I'_i$ is $I_i$, or it is a `const` or a copy with the same destination as $I_i$, and only an `op` instruction is ever replaced. The terminator does not change. We assume, as the toy IR does for its test programs, that no run reads a name before it is defined. A *state* is the environment of names, the memory, and the input of the calls; in the toy IR a run of a block is a function of its state on entry.

Fix any state $\sigma_0$ on entry to $B$, and run $B$ from $\sigma_0$. Let $\sigma_i$ be the state after $I_1, \ldots, I_i$, if none of them traps. We show:

**Theorem.** Run $B$ and $B'$ from the same entry state $\sigma_0$. For each $i$, $I_i$ traps if and only if $I'_i$ traps, and if neither traps, both programs are in the same state $\sigma_i$ after position $i$. Hence $B$ and $B'$ trap at the same position or reach the terminator in the same state. Because each block maps every entry state to the same result, the programs before and after LVN make the same sequence of blocks and have the same outcome on every input: the same return value, the same trap, or no end.

**The meaning of a value number.** The algorithm creates each value number $v$ at most once, at one position of $B$. Give it a value $\mathrm{val}(v)$ in the run from $\sigma_0$, by the way it was created:

- a number created by NUMBER for a name $a$ that the block has not defined before: $\mathrm{val}(v) = \sigma_0(a)$;
- a number created for an integer $k$: $\mathrm{val}(v) = k$, and CONST maps $v$ to $k$;
- a number created at line L15 for the key $(op, v_a, v_b)$: $\mathrm{val}(v) = \mathrm{val}(v_a) \mathbin{op} \mathrm{val}(v_b)$, the value that the instruction at that position computes in the run, if it does not trap;
- a number created for a phi, load, call, alloc or addr at position $i$: the value that $I_i$ writes in the run.

Each $\mathrm{val}(v)$ is fixed for the run, because a block is straight-line code and each position runs once.

**Invariant.** After the algorithm has handled position $i$, and in a run that reaches position $i + 1$ (no trap so far):

(I1) for every name $n$ in VN, $\sigma_i(n) = \mathrm{val}(\mathrm{VN}[n])$;

(I2) for every key $(op, v_a, v_b)$ in KEY, the instruction that created it ran without a trap, so $\mathrm{val}(v_a) \mathbin{op} \mathrm{val}(v_b)$ is defined and equals $\mathrm{val}(\mathrm{KEY}[op, v_a, v_b])$.

Both hold before position 1, where the maps are empty. NUMBER keeps (I1) when it adds a name $a$ that the block has not defined: $a$ still holds $\sigma_0(a)$, which is $\mathrm{val}$ of its new number. A name that the block has defined is in VN already, because line L18 binds every destination.

**Step.** Assume the invariant and the theorem up to position $i - 1$, so both programs are in state $\sigma_{i-1}$. Look at $I_i$.

1. *Not an op.* Then $I'_i = I_i$. Both programs run the same instruction from the same state, so they trap together or reach the same $\sigma_i$. For a phi, load, call, alloc or addr, $x$ gets a fresh number whose value is, by definition, what $I_i$ wrote. For `x = k` the number is the one of $k$, and $x$ holds $k$. For `x = a` the number is the one of $a$, and by (I1) $x$ now holds $\sigma_{i-1}(a) = \mathrm{val}(\mathrm{VN}[a])$. A store defines no name. Every other name keeps its value and its number, so (I1) holds after line L18. KEY does not change, so (I2) holds.

2. *An op `x = a op b`, with $v_a = \mathrm{VN}[a]$ and $v_b = \mathrm{VN}[b]$ after line L7.* By (I1), $\sigma_{i-1}(a) = \mathrm{val}(v_a)$ and $\sigma_{i-1}(b) = \mathrm{val}(v_b)$.

   a. *Folding (L8, L9).* CONST gives $\mathrm{val}(v_a) = c_1$ and $\mathrm{val}(v_b) = c_2$, and the operation does not trap on $(c_1, c_2)$ under the semantics of the toy IR, which is the target. So $I_i$ does not trap and writes $r = c_1 \mathbin{op} c_2$. $I'_i$ is `x = r`, which does not trap and writes the same value. The number of $x$ is the number of $r$, whose value is $r$.

   b. *An identity (L10, L11).* Each identity in the list is an equation that holds for all integers on which its left side is defined, and none of them has an operation that can trap on the left side and not on the right side, except where the divisor or the shift count is the constant that the identity requires ($x / 1$, $x \% 1$, $x \% {-1}$, $x \ll 0$, $x \gg 0$), and those never trap. So $I_i$ does not trap and writes the value that $I'_i$ writes: the constant of the identity or the current value of the operand it copies. The number of $x$ is the number of that constant or operand, and by (I1) its value is the value written.

   c. *A key that is in KEY (L13, L14).* Let $v = \mathrm{KEY}[key]$. The key is $(op, v_a, v_b)$, with the operands swapped only for a commutative operator, for which $\mathrm{val}(v_a) \mathbin{op} \mathrm{val}(v_b) = \mathrm{val}(v_b) \mathbin{op} \mathrm{val}(v_a)$ for all integers. By (I2) the value $\mathrm{val}(v_a) \mathbin{op} \mathrm{val}(v_b)$ is defined, so $I_i$, whose operands hold exactly these values, does not trap, and it writes $\mathrm{val}(v)$. If a holder $n$ with $\mathrm{VN}[n] = v$ exists, $I'_i$ is `x = n`; it reads a defined name, does not trap, and by (I1) writes $\sigma_{i-1}(n) = \mathrm{val}(v)$. Otherwise $I'_i = I_i$. In both cases $x$ gets the number $v$ and holds $\mathrm{val}(v)$.

   d. *A new key (L15, L16).* $I'_i = I_i$. If it traps, both programs trap here. Otherwise it writes $\mathrm{val}(v_a) \mathbin{op} \mathrm{val}(v_b)$, which is by definition $\mathrm{val}$ of the fresh number $v$, and the new entry of KEY was created by an instruction that ran without a trap, so (I2) holds.

   In each case the two programs trap together or write the same value to $x$ and nothing else, so both are in the same state $\sigma_i$. Only $x$ changed its number, and it holds the value of its new number, so (I1) holds. A holder list may still contain $x$ under its old number; line L14 checks $\mathrm{VN}[n] = v$, so a stale holder is never used. $\square$

**Undefined names.** $I'_i$ reads only names that $I_i$ reads or that are in VN. A name enters VN when the block defines it or when an earlier instruction reads it, so by the assumption it is defined in the run. So $B'$ reads no undefined name.

**The number of operations.** An op instruction at position $i$ of $B'$ is the op instruction $I_i$ of $B$, so every run of the program after LVN executes at most as many op instructions as the same run before it. This bound is about the count of operations; the total number of instructions is the same, because LVN replaces and never deletes.

**Cost.** Each instruction does a constant number of map lookups and inserts, plus the search for a holder at line L14. A name enters a holder list once per definition, at most $n$ entries in all for a block of $n$ instructions. The search drops stale names from the front of the list until it finds a current one, so each entry is dropped at most once, and each search costs $O(1)$ plus the entries it drops. The whole block takes $O(n)$ map operations, which is $O(n)$ expected time with hash maps.
