---
tag: 858QA0
kind: problem
slug: swap-two-values
name: Swapping two values
aliases:
- swap variables
area: techniques/bit-tricks
level: intro
summary: Exchanging the contents of two variables, with or without a temporary.
prereqs: [bitwise-operations]
see_also: [xor-swap, in-place-algorithm, selection-sort, fisher-yates-shuffle, sorting-network, compare-and-swap, xor-linked-list, in-place-permutation]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley (2013)
    locator: Chapter 2, Section 2-20 (Exchanging Registers) and Section 2-21 (Alternating among Two or More Values)
  - book: isbn:9780131103627
    title: Brian W. Kernighan and Dennis M. Ritchie, The C Programming Language, second edition, Prentice Hall (1988)
    locator: Section 5.2 (Pointers and Function Arguments, the function swap)
  - url: https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf
    title: ISO/IEC 9899:2011 committee draft N1570 (the C11 standard)
    locator: Section 6.5, paragraphs 2 and 5 (unsequenced side effects and signed overflow are undefined)
---

Swapping two values means to exchange the contents of two variables or memory cells, so that each one ends with the old value of the other. The usual solution copies one value to a temporary; the [XOR swap](/xor-swap/) and the add-and-subtract swap do it with no third cell. Swapping is the basic step of many [in-place algorithms](/in-place-algorithm/), such as [selection sort](/selection-sort/), [heapsort](/heapsort/) and the [Fisher-Yates shuffle](/fisher-yates-shuffle/). The problem is easy, but each solution has its own trap: aliasing, overflow or undefined behaviour in C.

## In plain words

You have a cup of tea and a cup of coffee, and you want the tea in the other cup. With an empty third cup this is easy: pour the tea into the empty cup, the coffee into the tea cup, and the tea into the coffee cup. That is three moves and one extra cup.

Computers usually do the same, with a third variable. With numbers you can also do it without the third cup, because you can mix two values into one and later separate them again. Exclusive-or and addition both allow this. These tricks save one cell, but they break when both names refer to the same place in memory.

## Definition

**State.** Two cells $a$ and $b$ that each hold a value of a set $V$. For the bit tricks, $V = \{0,1\}^w$, the $w$-bit words.

**Task.** Change the state $(a, b) = (x, y)$ to $(a, b) = (y, x)$ for all $x, y \in V$, and change nothing else that the program can observe.

**Cost model.** One step is an assignment $c \gets f(\ldots)$ that reads some cells, applies an operation, and writes one cell. The measures are the number of assignments and the number of extra cells.

**Aliasing.** When $a$ and $b$ are names for the same cell (for example `swap(&v[i], &v[j])` with $i = j$), the required result is that the cell does not change.

## Variants

- **Swap with a temporary.** One extra cell is allowed. This is the general solution and works for any $V$.
- **Swap without a temporary.** Only the two cells may be written. This needs an operation that can mix two values and later separate them, such as $\oplus$ on words or $+$ and $-$ modulo $2^w$.
- **Conditional swap.** Swap only when a condition holds, for example $a > b$. This is the compare-exchange of a [sorting network](/sorting-network/). A branch-free form uses a mask.
- **Atomic swap.** Exchange a register and a shared memory cell as one indivisible step, so that no other thread sees a middle state. Hardware gives instructions for this, and it is the basis of locks such as [test-and-set](/test-and-set/) and of [compare-and-swap](/compare-and-swap/).
- **Swap of large objects.** For records or arrays, swap pointers or handles instead of the contents, or swap word by word.
- **Rotation of more than two values.** $(a, b, c) \gets (b, c, a)$ with one temporary and $k + 1$ moves for $k$ values. A permutation in place is a product of such cycles; see [in-place permutation](/in-place-permutation/).

## Examples

**With a temporary.** For $(a, b) = (7, 3)$: $t \gets a$ gives $t = 7$; $a \gets b$ gives $a = 3$; $b \gets t$ gives $b = 7$.

**XOR, 8-bit words.** For $(a, b) = (180, 105) = (10110100_2, 01101001_2)$: $a \gets a \oplus b = 221$, $b \gets a \oplus b = 180$, $a \gets a \oplus b = 105$.

**Add and subtract, unsigned 8-bit words.** For $(a, b) = (200, 100)$: $a \gets (a + b) \bmod 256 = 44$, $b \gets (a - b) \bmod 256 = 200$, $a \gets (a - b) \bmod 256 = 100$. The middle value 44 is a wrapped sum, and the result is still right because all three steps use arithmetic modulo $256$.

**A non-example: multiply and divide.** $a \gets ab$, $b \gets a / b$, $a \gets a / b$ swaps nonzero reals in exact arithmetic, but it fails when $b = 0$ (the division is undefined), it overflows for large words, and it loses precision in floating point.

**Aliasing.** With one cell $a = 180$, the XOR method computes $180 \oplus 180 = 0$ in its first step and ends with $a = 0$. The add-and-subtract method computes $a = 360 \bmod 256 = 104$, then $a = 104 - 104 = 0$, then $a = 0 - 0 = 0$. Both end with 0. The temporary method ends with 180, which is right.

## Known algorithms

| method | assignments | extra cells | works for | trap |
|---|---|---|---|---|
| temporary | 3 | 1 | any type | none |
| [XOR swap](/xor-swap/) | 3 | 0 | integer words of any width, signed or unsigned | aliasing |
| add and subtract | 3 | 0 | unsigned words (arithmetic modulo $2^w$) | aliasing; signed overflow in C |
| hardware exchange | 1 instruction | 0 | a register and a cell, or two registers | none (x86 `XCHG` with a memory operand also locks the bus, so it is slow) |
| tuple assignment | 1 statement | a slot of the interpreter stack | Python `a, b = b, a` | none; the language uses a temporary inside |

Each method takes $\Theta(1)$ time on the [word RAM](/word-ram/).

## Bounds

**Three assignments are needed without a temporary.** Assume $|V| \ge 2$ and that only the cells $a$ and $b$ may be written.

*Proof.* Zero assignments leave $(x, y)$, which differs from $(y, x)$ when $x \ne y$. One assignment changes only one cell, so the other cell keeps its old value, and the result is wrong for $x \ne y$. Now consider two assignments, and say the first writes $a$; the case for $b$ is symmetric. After it the state is $(f(x, y), y)$. If the second also writes $a$, then $b = y$ at the end, which is wrong for $x \ne y$. So the second writes $b$, and the final state is $(f(x, y), g(f(x, y), y))$. The first part must be $y$ for all $x, y$, so $f(x, y) = y$. Then the second part is $g(y, y)$, which does not depend on $x$, but it must equal $x$ for all $x$. With $|V| \ge 2$ this is impossible. So at least three assignments are needed, and the XOR swap shows that three are enough. $\square$

**Three moves are needed with a temporary.** Consider plain copies $c \gets d$ only, with no operations that mix values. At the start, $x$ is only in $a$ and $y$ is only in $b$. A first useful copy into $a$ or $b$ would destroy the only copy of $x$ or of $y$, and no later copy can bring it back. So the first useful copy writes the temporary, and after it both $a$ and $b$ must still be written at least once, because each must change when $x \ne y$. So three copies are needed, and the temporary method uses three.

## Reductions

- **Permutations from swaps.** Each permutation of $n$ cells is a product of at most $n - 1$ swaps (transpositions), since each cycle of length $k$ needs $k - 1$. So an in-place permutation of an array reduces to swaps; see [permutation cycle decomposition](/permutation-cycle-decomposition/).
- **Sorting.** [Selection sort](/selection-sort/) does at most $n - 1$ swaps, and [cycle sort](/cycle-sort/) writes each item at most once.

## Applications

- Sorting in place: [selection sort](/selection-sort/), [heapsort](/heapsort/), [quicksort](/quicksort/) with [Lomuto](/lomuto-partition/) or [Hoare](/hoare-partition/) partition, [bubble sort](/bubble-sort/).
- Random permutations: the [Fisher-Yates shuffle](/fisher-yates-shuffle/) swaps a random item into each position.
- Double buffering: swap the pointers of the front and the back buffer instead of copying the buffers.
- Constant-time code: the masked conditional swap $t \gets (a \oplus b) \wedge m$, $a \gets a \oplus t$, $b \gets b \oplus t$, with $m$ all zeros or all ones, swaps without a branch that depends on secret data.

## References
