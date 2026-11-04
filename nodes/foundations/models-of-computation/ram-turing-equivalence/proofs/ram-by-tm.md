---
title: A multitape Turing machine simulates a logarithmic-cost RAM in time O(t^2)
proves: [ram-by-tm]
status: full
---

**Statement.** Let $P$ be a RAM program with the instructions `LOAD`, `STORE`, `ADD`, `SUB`, `READ`, `JUMP`, `JZERO`, `JEOF`, `HALT`, as on the [random-access machine](/random-access-machine/) page. Let $P$ decide $L \subseteq \{0,1\}^*$ in logarithmic-cost time $t(n)$: on every input word $w$ of length $n$, given as $n$ integers in $\{0,1\}$, $P$ halts with logarithmic cost at most $t(n)$, and with $R_0 = 1$ if $w \in L$ and $R_0 = 0$ if $w \notin L$. Then there is a deterministic 5-tape Turing machine $M_P$ that decides $L$ in $O(t(n)^2)$ steps. The constant depends on $P$ only.

**Setup.** Fix an input $w$ of length $n$ and the run of $P$ on $w$. Let the run execute $N$ instructions, numbered $1, \ldots, N$, and let $c_s$ be the logarithmic cost of instruction $s$. Then $C = \sum_s c_s \le t(n)$. Every cost $c_s$ is at least 1, so $N \le C$. We write $\ell(x)$ for the bit length, with $\ell(0) = 1$. Let $K_P$ be the largest length of a number that occurs in the text of $P$ (a constant, a register number or a jump target). Every constant $K$ below depends on $P$ only.

*Encoding.* Numbers are written in binary on the tapes with the least significant bit first and with no leading zeros, and $0$ is the string `0`. A number on a tape is followed by a blank or by a separator.

*Tapes of $M_P$.*

- Tape 1 holds the input $w$. Its head moves only to the right, and it is on the next unread symbol.
- Tape 2, the *memory tape*, holds a list of records `#a:v`, where $a$ and $v$ are numbers. The list stands in the first cells, and the cells after it are blank. The addresses of different records are different. A register $R_a$ with $a \ge 1$ that has no record has the value $0$. We write $m$ for the length of the list.
- Tape 3 holds the accumulator $R_0$.
- Tapes 4 and 5 are work tapes. Tape 4 holds an address, and tape 5 holds a value or a copy.

The program counter is in the finite control. Because $P$ has finitely many instructions, the control has finitely many states.

**Invariant $J_s$.** Before instruction $s$ of the run, the control is at the instruction that $P$ executes as instruction $s$. Tape 3 holds the value of $R_0$. Tape 2 holds exactly one record `#a:v` for each register $R_a$ with $a \ge 1$ that a `STORE` has written in the instructions $1, \ldots, s-1$, with its current value $v$. Tapes 4 and 5 are blank. Tape 1 has read exactly as many symbols as the instructions `READ` before $s$. All heads except head 1 are on cell 0.

**Step 1: the length of the memory tape.** Let $m_s$ be the length of the list before instruction $s$. We show $m_s \le 2 \sum_{r<s} c_r$. A record `#a:v` has length $\ell(a) + \ell(v) + 2$. It is in the list because of the last `STORE` $r < s$ that wrote the register $R_a$, and at that time $R_a$ received the value $v$ from $R_0$. By the cost table, the cost of `STORE i` is $\ell(c(0)) + \ell(i)$, and the cost of `STORE *i` is $\ell(c(0)) + \ell(i) + \ell(c(i))$. In both cases $c_r \ge \ell(v) + \ell(a)$, and also $c_r \ge 2$. So the record has length at most $c_r + 2 \le 2 c_r$. Different records belong to different instructions `STORE`, since one `STORE` writes one register. So the lengths add up to at most $2 \sum_{r<s} c_r \le 2t(n)$.

**Step 2: the subroutines.** All subroutines start and end with the heads of tapes 2, 4 and 5 on cell 0.

- *FIND.* Tape 4 holds a number $a$. The machine moves head 2 over the list. For each record it compares $a$ with the address, symbol by symbol, with head 4 and head 2 moving together, until the symbols differ or one string ends. If both strings end together, the record matches. Then it moves head 4 back to cell 0 and head 2 to the end of the record. For one record this takes $O(\text{the length of the record}+1)$ steps, since the comparison makes at most as many steps as the shorter address has symbols plus one, and the rewind of head 4 takes as many. So FIND takes $O(m + 1)$ steps. It stops at the first match. It ends in one of two states: found, with head 2 on the `:` of the record, or not found, with head 2 on the first blank after the list.
- *LOOKUP.* FIND, then copy the value after the `:` to tape 5 if found, or write `0` on tape 5 if not found. The result on tape 5 is the value of $R_a$. LOOKUP takes $O(m + \ell(v))$ steps where $v$ is the value, and $\ell(v) \le m$ if found. So it takes $O(m+1)$ steps. If $a = 0$, the address names the accumulator (a program can reach $R_0$ only through an indirect operand whose register holds $0$): LOOKUP copies tape 3 to tape 5 and does not use the list.
- *UPDATE.* Tape 4 holds $a$ and tape 3 holds $v$. If $a = 0$, do nothing, since `STORE` then copies $R_0$ to $R_0$. Else FIND. If found, copy the part of the list after the old value to tape 5 and blank it on tape 2, write $v$ after the `:`, copy the part back from tape 5 after $v$, and blank tape 5. This takes $O(m + \ell(v))$ steps. If not found, write `#`, $a$, `:` and $v$ at the end of the list, which takes $O(\ell(a) + \ell(v))$ steps. Then rewind. The total is $O(m + \ell(a) + \ell(v) + 1)$ steps.
- *ARITH.* Tapes 3 and 5 hold $x$ and $v$. Add: scan both from the left with a carry, and write the sum on tape 3. Subtract: scan with a borrow; if a borrow remains at the end, write `0`, else erase the leading zeros of the result. Each takes $O(\ell(x) + \ell(v) + 1)$ steps.

**Step 3: one instruction.** Assume $J_s$. Let $\lambda_s$ be the length of $R_0$ before instruction $s$. We show that the machine executes instruction $s$ in at most $K(m_s + c_s + \lambda_s)$ steps if $s$ is a `LOAD` or a `READ`, in at most $K(m_s + c_s)$ steps if $s$ is a `STORE`, `ADD`, `SUB` or `JZERO`, and in $O(1)$ steps if $s$ is a `JUMP`, `JEOF` or `HALT`, and that $J_{s+1}$ holds after it. Only `LOAD` and `READ` pay $\lambda_s$ outside $c_s$. In the other instructions that read $R_0$, $\lambda_s \le c_s$ by the cost table. Operands: for the operand $=c$ the machine writes $c$ on tape 5 in $O(K_P)$ steps. For the operand $i$ it writes $i$ on tape 4, which takes $O(K_P)$ steps, and it does LOOKUP, which leaves $c(i)$ on tape 5. For the operand $*i$ it writes $i$ on tape 4 and does LOOKUP, so tape 5 holds $c(i)$. It then copies this number to tape 4, which takes $O(\ell(c(i)))$ steps, blanks tape 5 in $O(\ell(c(i)))$ steps, and does LOOKUP again, so tape 5 holds $c(c(i))$. Each of these takes $O(m_s + K_P + \ell(c(i)))$ steps, and each of the lengths that occur is part of the cost $c_s$ of the instruction.

- `LOAD X`: get the operand on tape 5 as above, and copy tape 5 to tape 3, after erasing the old content. This takes $O(\lambda_s + \ell(v))$ more steps, and $\ell(v) \le c_s$.
- `STORE i`, `STORE *i`: put the address on tape 4 (for `*i`, by LOOKUP of $i$, a copy to tape 4 and the blanking of tape 5, which cost $O(\ell(a))$ steps), so that tape 5 is blank, and do UPDATE with $v$ on tape 3. The register $R_a$ gets $R_0$. The records of the other registers do not change. The cost is $O(m_s + \ell(a) + \ell(v) + K_P)$, and $\ell(v) + \ell(a) \le c_s$.
- `ADD X`, `SUB X`: get the operand on tape 5, and do ARITH. The cost is $O(m_s + \ell(R_0) + \ell(v))$, and $c_s \ge \ell(R_0) + \ell(v)$. The result is $R_0 + v$ or $\max(R_0 - v, 0)$, as ARITH computes.
- `READ`: erase tape 3, and write the symbol of tape 1 under head 1 on tape 3 (the number is 0 or 1), and move head 1 right. If head 1 reads a blank, no input is left, and the machine writes `0` and does not move head 1. This takes $O(\lambda_s + 1)$ steps.
- `JUMP k`: set the control to $k$. `JZERO k`: read tape 3 and jump if it is `0`. `JEOF k`: jump if head 1 reads a blank. `HALT`: accept if tape 3 holds `1`, else reject. Each takes $O(1)$ steps.

After each instruction, the machine rewinds the heads to cell 0 (not head 1). This costs at most the lengths already counted. The effects are those of the RAM instruction, so $J_{s+1}$ holds. For `HALT` the answer is the value of $R_0$, so $M_P$ accepts if and only if $P$ halts with $R_0 = 1$.

**Step 4: the length of the accumulator.** In the list of Step 3, only `LOAD` and `READ` pay for the old length $\lambda_s$ outside $c_s$. In `ADD` and `SUB` the length $\lambda_s = \ell(R_0)$ is a part of $c_s$. Let $r$ be the last instruction before $s$ that set $R_0$ (`LOAD`, `ADD`, `SUB` or `READ`). Then $\lambda_s \le c_r$: for `LOAD X` the new value is the value of $X$, and its length is a part of $c_r$; for `ADD` the new length is at most $\max(\ell(R_0), \ell(v)) + 1 \le \ell(R_0) + \ell(v) \le c_r$, where $R_0$ is the old value; for `SUB` it is at most the length of the old $R_0$, which is a part of $c_r$; for `READ` it is $1 \le c_r$. If no instruction has set $R_0$, then $\lambda_s = 1$. A setter $r$ is the last setter before at most one later instruction $s$, namely the next setter. So $\sum_s \lambda_s \le 1 + \sum_r c_r \le t(n) + 1$, where the sum is over the instructions `LOAD` and `READ`.

**Step 5: the total.** The first step of $M_P$ writes `0` on tape 3, and this makes $J_1$ true. By Step 3, Step 1 and Step 4, the total time of the simulation is at most

$$
K \sum_{s=1}^{N} (m_s + c_s + \lambda_s) + K' \le K\bigl( N \cdot 2t(n) + t(n) + t(n) + 1 \bigr) + K'.
$$

Here the sum of the $\lambda_s$ is over the instructions `LOAD` and `READ`, and the other terms are bounded by Step 1 (so $m_s \le 2t(n)$) and by $\sum_s c_s \le t(n)$. Since $N \le t(n)$ and $t(n) \ge 1$, this is $O(t(n)^2)$. By the invariant at the halting instruction, $M_P$ decides $L$. $\blacksquare$

**Remark.** The bound uses that every instruction costs at least 1, so that the number of instructions is at most the time. It also uses that a `STORE` costs at least the length of its record, so that the list is as short as the time. These two facts are the reason for the logarithmic cost rule. With the unit rule and an instruction `MULT`, repeated squaring and a `STORE` make a record of length $2^{\Omega(t)}$, and the proof fails.
