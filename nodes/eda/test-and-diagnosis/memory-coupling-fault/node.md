---
tag: 939TQZ
kind: model
slug: memory-coupling-fault
name: Memory coupling fault model
aliases:
- coupling fault
- idempotent coupling fault
- inversion coupling fault
area: eda/test-and-diagnosis
level: advanced
summary: Van de Goor's fault models in which a transition or value in one memory cell changes another cell, the targets of march tests.
prereqs: [stuck-at-fault-model]
see_also: [march-test, built-in-self-test, fault-coverage, transition-fault-model, bridging-fault-model, cell-aware-test]
sources:
  - paper: "D. S. Suk and S. M. Reddy, A march test for functional faults in semiconductor random access memories, IEEE Transactions on Computers C-30(12), 982 to 985, 1981"
    title: D. S. Suk and S. M. Reddy, A march test for functional faults in semiconductor random access memories, IEEE Transactions on Computers C-30(12), 982 to 985, December 1981
    locator: faults in which a write to one cell changes another cell, and a march test of linear length that detects them
  - book: isbn:9780471925866
    title: A. J. van de Goor, Testing Semiconductor Memories, Theory and Practice, Wiley, 1991
    locator: the chapters on functional fault models (stuck-at, transition, inversion, idempotent and state couplings, address decoder faults) and on march tests
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Memory Test (memory fault models and march tests)
---

The memory coupling model describes a defect of a random access memory as an unwanted interaction between two cells: an operation on one cell, the aggressor, or its value, changes the content of another cell, the victim. Three kinds are standard. In an inversion coupling, a transition in the aggressor inverts the victim. In an idempotent coupling, a transition in the aggressor forces the victim to a fixed value. In a state coupling, the victim is forced to a fixed value while the aggressor holds a given value. A memory of $N$ cells has a number of such faults that grows with $N^2$, yet some [march tests](/march-test/), of length $O(N)$, detect all of them.

## The machine

The memory is an array of $N$ one-bit cells with addresses $0, \ldots, N - 1$. A test is a sequence of operations: $w0$ or $w1$ writes a value to one cell, and $r0$ or $r1$ reads one cell and compares it with the expected value. A fault is detected when a read returns a value other than the one the fault-free memory would return.

A coupling is given by an ordered pair of distinct cells, the aggressor $i$ and the victim $j$, and a rule. A transition of a cell is a write that changes its value, written $\uparrow$ for 0 to 1 and $\downarrow$ for 1 to 0.

- **Inversion**, written $\langle t; \updownarrow \rangle$ with $t \in \{\uparrow, \downarrow\}$: each transition $t$ of $i$ inverts $j$. There are 2 rules.
- **Idempotent**, written $\langle t; v \rangle$ with $v \in \{0, 1\}$: each transition $t$ of $i$ sets $j$ to $v$. There are 4 rules.
- **State**, written $\langle x; v \rangle$ with $x, v \in \{0, 1\}$: whenever $i$ holds $x$, $j$ holds $v$, whatever is written to $j$. There are 4 rules.

The model assumes one fault in the memory, a fault-free address decoder and read logic, and bit-oriented cells. Other functional faults of the same family are a cell stuck at 0 or 1, a cell that cannot make a transition (a memory transition fault), and address decoder faults, where an address reaches no cell, several cells, or the wrong cell.

## What it counts

The model predicts which tests detect which faults, and so the coverage of a memory test over the list of faults. For $N$ cells there are $N(N - 1)$ ordered pairs and 10 rules per pair, so $10 N(N - 1)$ faults of these three kinds, against $2N$ stuck-at cells. A memory of $2^{20}$ cells has about $10^{13}$ of them. A test that treats each pair on its own, such as the galloping pattern, needs time quadratic in $N$, which is too long. The model is used to show that a march test of linear length detects every fault of the list.

A **march test** is a sequence of march elements. Each element applies the same short sequence of operations to every cell, cell by cell, in increasing address order ($\Uparrow$), decreasing order ($\Downarrow$), or either order ($\Updownarrow$). March C−, in the form given by van de Goor, is
$$\Updownarrow(w0);\ \Uparrow(r0, w1);\ \Uparrow(r1, w0);\ \Downarrow(r0, w1);\ \Downarrow(r1, w0);\ \Updownarrow(r0),$$
with $10N$ operations. Call its elements $M_0, \ldots, M_5$.

## Relation to other models

- **Bridging faults.** A short between the storage nodes of two cells, or between their bit lines, behaves like a state coupling. This is the memory form of the [bridging fault model](/bridging-fault-model/).
- **Transition faults.** A memory cell that cannot make a transition is a single-cell analogue of the [transition fault model](/transition-fault-model/) of logic. In memory test it is a functional fault, not a timing fault.
- **Neighbourhood pattern sensitive faults.** A victim whose content depends on the pattern in several physical neighbours generalizes state coupling to more than one aggressor. Tests for it need the physical layout of the array.
- **Linked faults.** Two couplings with the same victim can hide each other, for example when one sets the victim to 1 and another sets it back to 0 before a read. The results below assume unlinked faults. Tests for linked faults are longer.
- **Built-in self-test.** Memory [BIST](/built-in-self-test/) controllers on chips run march tests, since their address counters and simple data patterns are cheap in hardware.

## Known results in the model

- **Linear lower bound.** Every test that detects all stuck-at cells reads every cell at least once and writes every cell at least once, so it has at least $2N$ operations. A march test meets the linear order.
- **March C− detects all inversion, idempotent and state couplings.** We show it for idempotent couplings; the other two kinds follow in the same way. Take the rule $\langle t; v \rangle$ with aggressor $i$ and victim $j$. In an ascending element, when cell $i$ is written, the cells below $i$ already hold the value that the element leaves, and the cells above $i$ still hold the value the element found, and they are read later in this element. A descending element is the mirror image. The fault is detected if, at the transition $t$ of $i$, the victim holds $\lnot v$ and is read before it is written again.

| rule | aggressor below victim, $i < j$ | aggressor above victim, $i > j$ |
|---|---|---|
| $\langle \uparrow; 1 \rangle$ | $M_1$: $j$ holds 0, read by $r0$ in $M_1$ | $M_3$: $j$ holds 0, read by $r0$ in $M_3$ |
| $\langle \uparrow; 0 \rangle$ | $M_3$: $j$ holds 1, read by $r1$ in $M_4$ | $M_1$: $j$ holds 1, read by $r1$ in $M_2$ |
| $\langle \downarrow; 0 \rangle$ | $M_2$: $j$ holds 1, read by $r1$ in $M_2$ | $M_4$: $j$ holds 1, read by $r1$ in $M_4$ |
| $\langle \downarrow; 1 \rangle$ | $M_4$: $j$ holds 0, read by $r0$ in $M_5$ | $M_2$: $j$ holds 0, read by $r0$ in $M_3$ |

  Each entry names the element where $i$ makes the transition while $j$ holds $\lnot v$, and the read that first sees $j$. For example, for $\langle \uparrow; 0 \rangle$ with $i > j$, element $M_1$ visits $j$ first and writes 1 there, then writes 1 to $i$, which forces $j$ to 0, and the first operation of $M_2$ at $j$ is $r1$. An inversion coupling changes the victim in every case where an idempotent one with the same trigger does, so the same table covers it. For a state coupling $\langle x; v \rangle$, the test must read $j$ expecting $\lnot v$ while $i$ holds $x$. With $i < j$, the reads of $j$ in $M_1$, $M_2$, $M_3$ and $M_4$ happen while $i$ holds 1, 0, 0 and 1. With $i > j$, they happen while $i$ holds 0, 1, 1 and 0. The expected values are 0, 1, 0, 1, so all four pairs $(x, \lnot v)$ occur for both orders. $\square$ A simulation of all 300 such faults of a memory with $N = 6$ cells agrees with the table; this is a check of the argument on a toy size, not a measurement.
- **Not every march test does.** MATS+, $\Updownarrow(w0);\ \Uparrow(r0, w1);\ \Downarrow(r1, w0)$, with $5N$ operations, detects every stuck-at cell, but misses $\langle \uparrow; 1 \rangle$ with $i > j$: when $i$ rises in the ascending element, $j$ already holds 1, and no later transition of $i$ meets $j$ at 0.
- **Suk and Reddy.** In 1981, Suk and Reddy gave a march test of linear length for faults in which a write to one cell changes another, which made coupling tests practical for large memories.

## References
