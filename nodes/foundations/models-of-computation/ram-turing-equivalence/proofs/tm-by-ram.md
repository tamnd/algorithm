---
title: A RAM simulates a multitape Turing machine in logarithmic-cost time O(T log T)
proves: [tm-by-ram]
status: full
---

**Statement.** Let $M$ be a deterministic $k$-tape Turing machine, with the tape alphabet $\Gamma$ of $g$ symbols and the input alphabet $\{0,1\}$, that decides $L \subseteq \{0,1\}^*$ and halts within $T(n)$ steps on every input of length $n$, where $T(n) \ge \max(n, 2)$. Then there is a RAM program $P_M$ (with the instructions of the [random-access machine](/random-access-machine/) page, no multiplication) that decides $L$ in unit-cost time $O(T(n))$ and in logarithmic-cost time $O(T(n) \log T(n))$. The constants depend on $M$ only.

**Setup.** Write $\Gamma = \{\gamma_0, \ldots, \gamma_{g-1}\}$ with $\gamma_0 = \sqcup$, $\gamma_1 = 0$ and $\gamma_2 = 1$, and use the index $j$ as the code of $\gamma_j$. A blank cell has code $0$, which is the value of a register that was never written. Let $B = k + 2$. The registers are used like this.

- $R_i$ for $1 \le i \le k$ holds the address of the register that stores the cell scanned by head $i$.
- $R_{k+1}$ is a pointer $p$ for the copy of the input.
- The cell $c \ge 0$ of tape $i$ is stored in the register with the address $B + kc + (i-1)$. These addresses are at least $B > k + 1$ and are all different, for different pairs $(i, c)$, since $(i - 1)$ is the remainder of the offset modulo $k$ and $c$ is the quotient.
- $R_0$ is the accumulator.

The program has two parts. **Part I** copies the input into the cells of tape 1.

```text
      LOAD =B
      STORE k+1               ; p = B
loop  JEOF done
      READ                    ; acc = w_c, 0 or 1
      ADD =1                  ; code of the bit: 1 for 0, 2 for 1
      STORE *(k+1)            ; the cell gets the code
      LOAD k+1
      ADD =k
      STORE k+1               ; p = p + k
      JUMP loop
done  LOAD =B+i-1             ; for each i = 1..k
      STORE i                 ; head i on cell 0
      JUMP S(q0)
```

**Part II** has a block $S(q)$ for each non-halting state $q$ of $M$ and a block for each of accept and reject. The block $S(\text{accept})$ is `LOAD =1`, `HALT`. The block $S(\text{reject})$ is `LOAD =0`, `HALT`. The block $S(q)$ is a decision tree of depth $k$ that finds the scanned symbols. At a node for tape $i$, with the symbols of the tapes $1, \ldots, i-1$ already fixed by the path, it runs the tests for $a = 0, 1, \ldots, g-2$ in this order. The test for $a$ is

```text
      LOAD *i
      SUB =a
      JZERO (the node for tape i+1 in which the symbol of tape i is a)
```

and if all $g - 1$ tests fail, the code goes on to the node in which the symbol of tape $i$ is $g - 1$. The tree has $g^k$ leaves, one for each tuple $(a_1, \ldots, a_k)$ of codes, and each leaf is a separate piece of code. In the leaf $(q; a_1, \ldots, a_k)$, let $\delta(q, \gamma_{a_1}, \ldots, \gamma_{a_k}) = (q', \gamma_{b_1}, \ldots, \gamma_{b_k}, D_1, \ldots, D_k)$. The leaf has these instructions, for $i = 1, \ldots, k$ in turn.

- `LOAD =b_i`, then `STORE *i`: write the symbol.
- If $D_i = R$: `LOAD i`, `ADD =k`, `STORE i`.
- If $D_i = L$: `LOAD i`, `SUB =B+i-1`, `JZERO skip_i`, `LOAD i`, `SUB =k`, `STORE i`, and then the label `skip_i`.
- If $D_i = S$: nothing.

The leaf ends with `JUMP S(q')`. The program has $O(g^k)$ instructions, which is a constant.

**Step 1: the test finds the symbol.** Let $x = R_{R_i}$, the code of the scanned symbol, with $0 \le x \le g-1$. The test for $a$ computes $\max(x - a, 0)$, and the jump is taken if and only if $x \le a$. The tests run for $a = 0, 1, \ldots$ in this order. If $x = a_0$, then the tests for $a < a_0$ fail, since $x > a$. The test for $a = a_0$ jumps. So the first jump is at $a = x$. If no test jumps, then $x > g - 2$, so $x = g - 1$. Hence the leaf that the block reaches is the leaf of the true symbols. (After each test the accumulator is overwritten by the next `LOAD *i`, so the tests do not interact.)

**Step 2: the left move.** The cell $0$ of tape $i$ has the address $B + i - 1$, and every cell has an address of at least this value. So `SUB =B+i-1` gives $0$ if and only if $R_i \le B + i - 1$, that is, if and only if head $i$ is on cell $0$. In that case the move $L$ keeps the head in place, as in the machine, since `JZERO` skips the subtraction. Else `SUB =k` moves the address of head $i$ one cell to the left (the address of cell $c-1$ is that of cell $c$ minus $k$).

**Invariant $I_j$.** After $j$ steps of $M$ (and after Part I for $j = 0$), the control is at the beginning of $S(q_j)$, where $q_j$ is the state of $M$ after $j$ steps. For each $i$ the register $R_i$ holds the address of the cell scanned by head $i$. For each $i$ and $c$ the register with the address $B + kc + (i-1)$ holds the code of the symbol in cell $c$ of tape $i$.

*Proof of $I_0$.* The registers other than those of tape 1 are $0$, which is the code of the blank, and tape $i \ge 2$ is blank at the start. Part I stores the codes of the input symbols at the addresses $B + kc$ for $c = 0, 1, \ldots, n-1$, since $p$ starts at $B$ and grows by $k$ at each pass, and `JEOF done` ends the loop after $n$ passes. The cells $c \ge n$ of tape 1 are blank and the registers are $0$. The heads start on cell $0$, whose address is $B + i - 1$.

*Proof of $I_{j} \Rightarrow I_{j+1}$.* Assume $I_j$ and $q_j$ non-halting. By Step 1 the block reaches the leaf of the true tuple of symbols. In the leaf, for each $i$ the instruction pair `LOAD =b_i`, `STORE *i` writes the symbol $b_i$ into the register of the scanned cell, and then the move updates $R_i$ as in Step 2. Different tapes use different registers, so the order in which the tapes are handled does not matter. The leaf jumps to $S(q_{j+1})$. This is the configuration of $M$ after step $j+1$. If $q_j$ is accept, $S(q_j)$ halts with $R_0 = 1$, and if reject with $R_0 = 0$. $\blacksquare$ (of the invariant)

**Step 3: the cost.** Let $M$ halt after $T' \le T(n)$ steps on the input. A head moves at most one cell in a step, so during the run, every scanned cell has an index of at most $\max(n, T')\le T(n)$ (the input has length $n \le T(n)$). So every address and every register value that occurs is at most $B + k(T(n)+1) + k$, and every constant in the program is bounded by a constant. An instruction costs at most four lengths (by the cost table), each at most $\lg(B + k(T(n) + 2)) + 1 = O(\log T(n))$, since $T(n) \ge 2$. The number of instructions executed is as follows.

- Part I executes $8n + O(1)$ instructions with $n$ the length of the input, since each pass of the loop executes 8 instructions and the end has $2k + 1$.
- Each step of $M$ executes at most $3k(g-1) + 8k + 1$ instructions: at most $3(g-1)$ for each tape in the tests, at most $8$ for each tape in the leaf (the longest case is the move $L$ with 6 instructions plus 2 for the write), and 1 for the jump at the end of the leaf.
- The last block has 2 instructions.

So the number of instructions is at most $8n + K_1 T' + K_2 \le K T(n)$, using $n \le T(n)$. This is the unit-cost time $O(T(n))$. Multiplying by the cost per instruction, the logarithmic-cost time is $O(T(n) \log T(n))$. By the invariant, $P_M$ halts with $R_0 = 1$ exactly when $M$ accepts. $\blacksquare$
