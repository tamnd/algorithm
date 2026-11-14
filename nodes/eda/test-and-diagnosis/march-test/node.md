---
tag: G5W6E7
kind: algorithm
slug: march-test
name: March test
aliases:
- March C-
- memory march algorithm
area: eda/test-and-diagnosis
level: core
summary: A memory test that walks through all addresses in up or down order applying read and write elements, such as March C- with 10n operations for stuck-at and coupling faults.
model: word-ram
complexity:
  vars: {N: the number of memory cells, m: the total number of operations in all elements of the test}
  time: {worst: O(m N)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1978
  people: [Ravindra Nair, Satish M. Thatte, Jacob A. Abraham, Marian Marinescu, Ad J. van de Goor]
  note: Nair, Thatte and Abraham gave the linear MATS test in 1978. Suk and Reddy, Marinescu and van de Goor built the march tests for coupling faults from 1981 to 1993.
prereqs: [memory-coupling-fault]
see_also: [stuck-at-fault-model, transition-fault-model, built-in-self-test, fault-coverage, bridging-fault-model, fault-simulation]
sources:
  - paper: doi:10.1109/TC.1978.1675150
    title: R. Nair, S. M. Thatte and J. A. Abraham, Efficient algorithms for testing semiconductor random-access memories, IEEE Transactions on Computers C-27(6), 572 to 576, 1978
    locator: the functional fault model and the linear test MATS
  - paper: "D. S. Suk and S. M. Reddy, A march test for functional faults in semiconductor random access memories, IEEE Transactions on Computers C-30(12), 982 to 985, 1981"
    title: D. S. Suk and S. M. Reddy, A march test for functional faults in semiconductor random access memories, IEEE Transactions on Computers C-30(12), 982 to 985, December 1981
    locator: the march test of linear length for faults in which a write to one cell changes another
  - paper: "Marian Marinescu, Simple and efficient algorithms for functional RAM testing, Proceedings of the IEEE International Test Conference, 236 to 239, 1982"
    title: M. Marinescu, Simple and efficient algorithms for functional RAM testing, Proc. International Test Conference 1982, 236 to 239
    locator: the march notation and the 11N test March C
  - paper: doi:10.1145/356914.356916
    title: M. S. Abadir and H. K. Reghbati, Functional testing of semiconductor random access memories, ACM Computing Surveys 15(3), 175 to 198, 1983
    locator: the survey of RAM fault models and tests, including MATS+
  - paper: doi:10.1109/54.199799
    title: A. J. van de Goor, Using march tests to test SRAMs, IEEE Design and Test of Computers 10(1), 8 to 14, 1993
    locator: the families of march tests, the reduced March C with 10N operations, and the fault classes each test detects
  - book: isbn:9780471925866
    title: A. J. van de Goor, Testing Semiconductor Memories, Theory and Practice, Wiley, 1991
    locator: the chapters on functional fault models, address decoder faults and march tests
---

A march test is a test for a random access memory of $N$ cells. It is a short list of march elements. Each element visits every address once, in increasing or in decreasing order, and at each address it runs the same few reads and writes before it moves on. A read expects a known value, and the test fails at the first read that gets another value. A march test takes time linear in $N$, and the right choice of elements detects every cell stuck at 0 or 1, every cell that cannot change its value, every fault of the address decoder and every coupling of the [memory coupling fault model](/memory-coupling-fault/). The best known example, March C− of van de Goor, has 6 elements and $10N$ operations. Memory testers and on-chip memory [built-in self-test](/built-in-self-test/) controllers run march tests on almost every memory that is made.

## In plain words

A memory chip has millions of one-bit cells. A defect can make a cell stuck, make it unable to flip, or make a write to one cell disturb another cell. Trying every pair of cells would take far too long.

A march test sweeps the whole memory a few times. On each sweep it goes up or down the addresses and does the same small job at each cell, for example "read it and expect 0, then write 1". Because the sweep moves in one direction, every cell below the current one already has its new value and every cell above it still has its old one. Going up once and down once makes every pair of cells meet in both orders, so a disturbance between any two cells shows up as a wrong read later in the sweep.

## The problem

The input is a memory of $N$ one-bit cells with addresses $0, \ldots, N - 1$, and a march test. A march test is a list of elements $M_0, \ldots, M_{e-1}$. Each element has an order, $\Uparrow$ for increasing addresses, $\Downarrow$ for decreasing addresses or $\Updownarrow$ when either order works, and a list of operations. An operation is $w0$ or $w1$, a write, or $r0$ or $r1$, a read that expects the given value. The output is "pass", or the first failing read with its element, address and the value it got.

The faults are those of van de Goor's functional model, one fault at a time: a cell stuck at 0 or 1, a cell with a transition fault that cannot go up ($\uparrow$) or down ($\downarrow$), the inversion, idempotent and state couplings $\langle t; \updownarrow \rangle$, $\langle t; v \rangle$ and $\langle x; v \rangle$ of the [coupling page](/memory-coupling-fault/), and address decoder faults, where an address reaches no cell, the wrong cell or two cells. These are the memory counterparts of the [stuck-at](/stuck-at-fault-model/) and [transition fault](/transition-fault-model/) models of logic. A fault is detected when the test fails from every initial content of the memory.

## The algorithm

```pseudo id=main
MARCH(memory, M_0, …, M_{e−1}, N)
L1  for each element M_k = (order, operations) of the test
L2      for each address a from 0 to N − 1 if order is ⇑ or ⇕, from N − 1 to 0 if order is ⇓
L3          for each operation of M_k, in order
L4              if the operation is w v then write v to address a
L5              else the operation is r v: read address a
L6                  if the value read is not v then return FAIL(k, a, the operation, the value)
L7  return PASS
```

The test is fixed before the run, so the same loop serves every march test. The code of this page gives March C− as

$$\Updownarrow(w0);\ \Uparrow(r0, w1);\ \Uparrow(r1, w0);\ \Downarrow(r0, w1);\ \Downarrow(r1, w0);\ \Updownarrow(r0),$$

MATS+ as $\Updownarrow(w0);\ \Uparrow(r0, w1);\ \Downarrow(r1, w0)$, and runs an element marked $\Updownarrow$ upward.

## Example

**A transition fault.** Take $N = 4$ cells, all 0 at the start, and let cell 2 be unable to go from 1 to 0. MATS+ writes 0 everywhere, then on the upward sweep reads 0 and writes 1 at each cell, then on the downward sweep reads 1 and writes 0. The last write fails at cell 2, but no read follows, so MATS+ passes this memory.

March C− runs as follows.

| element | operations at cell 2 | cell 2 after | operations so far |
|---|---|---|---|
| $M_0$ $\Updownarrow(w0)$ | $w0$ | 0 | 4 |
| $M_1$ $\Uparrow(r0, w1)$ | $r0$ gets 0, $w1$ | 1 | 12 |
| $M_2$ $\Uparrow(r1, w0)$ | $r1$ gets 1, $w0$ fails | 1 | 20 |
| $M_3$ $\Downarrow(r0, w1)$ | after cell 3, $r0$ gets 1: FAIL | 1 | 23 |

The test stops after 23 of its 40 operations and reports element $M_3$, address 2, and the value 1.

**Coverage on four cells.** The tests of this page inject every fault of each class into a memory of 4 cells and run each test from all 16 initial contents. The table gives the number of faults detected from every initial content.

| test | operations | stuck-at (8) | transition (8) | inversion (24) | idempotent (48) | state (48) | address decoder (44) |
|---|---|---|---|---|---|---|---|
| MATS, $\Updownarrow(w0); \Updownarrow(r0, w1); \Updownarrow(r1)$ | $4N$ | 8 | 4 | 12 | 12 | 36 | 38 |
| MATS+ | $5N$ | 8 | 4 | 18 | 18 | 36 | 44 |
| MATS++, $\Updownarrow(w0); \Uparrow(r0, w1); \Downarrow(r1, w0, r0)$ | $6N$ | 8 | 8 | 18 | 18 | 36 | 44 |
| March C− | $10N$ | 8 | 8 | 24 | 48 | 48 | 44 |

The address decoder faults here are an address that reaches no cell (a read returns a fixed 0 or 1), an address that reaches the wrong cell, and an address that reaches two cells (a read returns their AND or their OR). The numbers come from this small model and this small $N$. They show which tests miss faults, not the coverage on a real chip.

## Correctness

The [full proof](proofs/correctness.md) shows four things. First, a run that does not fail performs exactly $N \sum_k m_k$ operations, where $m_k$ is the number of operations of $M_k$, because every element visits each address once. The six elements of March C− have 1, 2, 2, 2, 2 and 1 operations, which gives $10N$, and MATS+ gives $5N$. Second, a test passes on a fault-free memory from every initial content exactly when every read follows a write of the value it expects, since the operations that reach one cell are the operations of the test in order. Third, March C− detects every stuck-at cell and every transition fault, by following the faulty cell through the elements as in the example. Fourth, MATS+ misses every transition fault $\downarrow$.

That March C− detects all inversion, idempotent and state couplings is proved on the [memory coupling fault](/memory-coupling-fault/) page. The detection of the address decoder faults is shown in van de Goor's book and not proved here. The tests check both claims by exhaustive injection for memories of 2 to 5 cells, which confirms them for those sizes only.

## Complexity

The run takes $O(m N)$ time, where $m$ is the number of operations per address over all elements, and $O(1)$ extra space for the loop counters. For a fixed test, $m$ is a constant, so the time is linear in $N$. Any test that detects every stuck-at cell must read and write every cell, so linear time is the best possible order.

The constant matters on real memories. With $N = 2^{20}$ cells and 10 ns per operation, March C− takes about 0.1 s. A test with $N^2$ operations, which is what a test that handles each pair of cells on its own needs, would take about 3 hours.

## Properties

- **Linear time.** Every march test of $e$ elements with $m$ operations in total runs in $mN$ operations.
- **Deterministic and data-independent.** The sequence of addresses and values is fixed, so a simple address counter and a few data bits generate it in hardware.
- **No false alarms.** A test in which every read follows a write of the expected value passes on every fault-free memory. All standard tests have this form.
- **Order matters.** The element orders $\Uparrow$ and $\Downarrow$ decide which couplings meet a victim at the right value. MATS+ detects every stuck-at cell and every address decoder fault in the model of this page, but misses some couplings and every transition fault $\downarrow$.
- **Unlinked faults only.** The coverage results assume one fault at a time. Two couplings on the same victim can mask each other.

## Variants and improvements

- **MATS** (Nair, Thatte and Abraham, 1978) has $4N$ operations and detects every stuck-at cell.
- **MATS+** adds order to MATS, and **MATS++** adds a final read to the last element, which catches the transition faults $\downarrow$ that MATS+ misses.
- **March C** (Marinescu, 1982) has $11N$ operations with an extra $\Updownarrow(r0)$ element in the middle. Van de Goor showed that this element is redundant for the target faults, which gives March C−.
- **Longer tests** such as March A and March B, from the work of Suk and Reddy, target linked couplings. Many later tests target faults found in real SRAMs, such as read disturb and faults that depend on the timing of the operations.
- **Word-oriented memories.** A memory with $B$-bit words runs each march test with several data backgrounds, so that the bits inside one word also couple in both directions.
- **Built-in self-test.** On-chip memory [BIST](/built-in-self-test/) runs a march test with an address counter that counts both ways and a comparator. Some controllers can be programmed with the elements.

## When to use it

Use a march test for every embedded or stand-alone RAM in production test and in memory BIST. March C− is a common default for bit-oriented SRAM. Pick a longer test when the fault list of the memory technology needs it, and add a retention test with a pause when the cells can leak. For the random logic around the memory, use logic test methods such as [scan design](/scan-design/) instead.

## Pitfalls

- **Assuming the initial content.** A cell can hold anything at power-up. The first element must write every cell before any read.
- **Ignoring the order of $\Updownarrow$.** An element marked $\Updownarrow$ may run in either order only if the coverage proof does not depend on it. Running a $\Uparrow$ element downward breaks the coupling coverage.
- **Logical and physical addresses.** Coupling between neighbours depends on the physical layout. Address scrambling in the decoder can put logically far cells side by side, which matters for tests that target neighbourhoods.
- **One fault at a time.** A memory with several faults can pass a test that detects each fault alone.
- **Stopping at the first failure.** For repair with spare rows and columns, the tester must log every failing address, not only the first.

## Implementations

## History

Early RAM tests such as walking and galloping patterns took time quadratic in the number of cells. In 1978 Nair, Thatte and Abraham gave a functional fault model and the linear test MATS. Suk and Reddy published a march test of linear length for coupling faults in 1981, and Marinescu introduced the march notation and March C in 1982. Abadir and Reghbati surveyed the field in 1983. Van de Goor collected the fault models in his 1991 book and, in 1993, showed which classes each march test detects, including the 10N test March C−. March tests then became the standard algorithms of memory BIST controllers.

## References
