---
tag: RQ5WRV
kind: definition
slug: multi-valued-logic-simulation
name: Multi-valued logic for simulation
aliases:
- four-valued logic
- IEEE 1164 nine-valued logic
- 01XZ logic
area: eda/logic-and-circuit-simulation
level: intro
summary: Value systems beyond 0 and 1, such as X for unknown and Z for high impedance and IEEE 1164's nine values, used to model initialization, buses and conflicts.
prereqs: [boolean-circuit, logic-simulation]
see_also: [ternary-simulation, switch-level-simulation, delta-cycle, event-driven-logic-simulation, compiled-code-logic-simulation, symbolic-trajectory-evaluation, fault-simulation, knaster-tarski-theorem]
sources:
  - paper: "IEEE Std 1164-1993, IEEE Standard Multivalue Logic System for VHDL Model Interoperability (Std_logic_1164), IEEE, 1993"
    title: IEEE Standard Multivalue Logic System for VHDL Model Interoperability (Std_logic_1164), IEEE Std 1164-1993
    locator: the type std_ulogic with its nine values, the resolution function resolved and its table, the logic tables for and, or, xor and not, and the conversion To_X01, in the package and its body
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter Logic Simulation, the parts on three-valued logic, the unknown value and its pessimism, and on tristate buses and wired logic (general locator)
  - book: doi:10.1007/978-1-4612-4210-9
    title: Janusz A. Brzozowski and Carl-Johan H. Seger, Asynchronous Circuits, Springer, New York, 1995
    locator: Chapter 7, Ternary Simulation (the ternary extension of a Boolean function and its monotonicity)
---

A logic simulator that knows only 0 and 1 cannot say that a flip-flop has not been reset yet, that a bus has no driver, or that two drivers fight. Multi-valued logic adds values for these cases: X for an unknown value, Z for a node that no driver holds, and, in the IEEE 1164 standard of VHDL, nine values that also give the strength of a driver. This page is in the logic simulation half of the sub-area. The value systems do not depend on the delay model, and the examples use zero delay. Two kinds of operation act on the values. A gate function, such as AND, computes an output from its inputs. A resolution function combines the values of several drivers of one wire. The first is monotone in an order by information, which makes X results safe but sometimes too pessimistic. The second is the join in an order by strength.

## Definition

**Three values.** The values are 0, 1 and X. The information order puts X above both binary values: $0 \sqsubseteq X$, $1 \sqsubseteq X$, and 0 and 1 are not comparable. A binary vector $c$ is a *completion* of a vector $a$ over $\{0, 1, X\}$ if $c_i = a_i$ wherever $a_i \ne X$. The *ternary extension* of a Boolean function $f$ is
$$\hat f(a) = \begin{cases} b & \text{if } f(c) = b \text{ for every completion } c \text{ of } a, \\ X & \text{otherwise.} \end{cases}$$
For the basic gates this gives Kleene's strong tables: $\lnot X = X$; $0 \land v = 0$ and $1 \land v = v$ for every $v$; $1 \lor v = 1$ and $0 \lor v = v$. So $X \land X = X$ and $X \lor X = X$.

**Soundness and monotonicity (exact).** Each $\hat f$ is monotone: if $a \sqsubseteq a'$ then $\hat f(a) \sqsubseteq \hat f(a')$, because the completions of $a$ are among those of $a'$. A circuit evaluated gate by gate with these tables computes a composition of monotone functions, which is monotone. And it is sound: a net that gets 0 or 1 for an input vector $a$ has that value for every completion of $a$. The proof by induction over the gates, and the use of monotonicity in Eichelberger's hazard detection, are on the [ternary simulation](/ternary-simulation/) page. The converse fails: a net can get X although all completions agree, as the examples show.

**Four values.** Add Z, the value of a wire with no active driver. A gate reads a Z input as X, since a floating input can settle at either level. A wire with drivers $v_1, \ldots, v_r$ takes the resolved value
$$v_1 \sqcup \cdots \sqcup v_r, \qquad Z \sqcup v = v, \quad v \sqcup v = v, \quad 0 \sqcup 1 = X, \quad X \sqcup v = X,$$
which is the join in the order $Z < 0, 1 < X$. A wire with no driver, or only Z drivers, is Z. Verilog uses these four values for its `wire` type.

**Nine values (IEEE Std 1164).** The type `std_ulogic` has the values

| value | meaning | value | meaning |
|---|---|---|---|
| U | uninitialized | W | weak unknown |
| X | forcing unknown | L | weak 0 |
| 0 | forcing 0 | H | weak 1 |
| 1 | forcing 1 | - | don't care |
| Z | high impedance | | |

A forcing value comes from a driver that holds the wire hard, such as a transistor to a supply. A weak value comes from a resistor or a weak device, such as a pull-up. The resolved subtype `std_logic` combines drivers with this table, as given in the package body:

| | U | X | 0 | 1 | Z | W | L | H | - |
|---|---|---|---|---|---|---|---|---|---|
| **U** | U | U | U | U | U | U | U | U | U |
| **X** | U | X | X | X | X | X | X | X | X |
| **0** | U | X | 0 | X | 0 | 0 | 0 | 0 | X |
| **1** | U | X | X | 1 | 1 | 1 | 1 | 1 | X |
| **Z** | U | X | 0 | 1 | Z | W | L | H | X |
| **W** | U | X | 0 | 1 | W | W | W | W | X |
| **L** | U | X | 0 | 1 | L | W | L | W | X |
| **H** | U | X | 0 | 1 | H | W | W | H | X |
| **-** | U | X | X | X | X | X | X | X | X |

The function `resolved` returns a single driver unchanged. For two or more drivers it starts from Z and folds the table over the drivers.

**The table is a join (exact).** Order the eight values other than '-' by
$$Z < L, H < W < 0, 1 < X < U,$$
where L and H are not comparable and 0 and 1 are not comparable. This order is a lattice, and the table restricted to these eight values is its join $\sqcup$: the result is the least value above both arguments. For example $L \sqcup H = W$, $H \sqcup 0 = 0$ and $0 \sqcup 1 = X$. The value '-' resolves to U with U and to X with everything else, including itself. A script compared all 81 entries with this rule and found no difference. A join is commutative, associative and idempotent, so for drivers without '-' the resolved value does not depend on the order of the drivers. With '-' the table is still commutative and associative, which the script also checked over all 729 triples, but not idempotent, since '-' with '-' gives X. That is why `resolved` treats one driver apart: folding from Z would turn a lone '-' into X.

**Logic on nine values.** The tables for `and`, `or`, `xor` and `not` first read L as 0 and H as 1, and Z, W and '-' as X, which is the conversion `To_X01`. Then they apply the Kleene tables, with one change: U takes the place of X in the result when an input is U. So `and` gives 0 if either input is 0 or L, whatever the other input is, and `'0' and 'U'` is 0; otherwise it gives U if either input is U; otherwise it gives the Kleene AND of the converted values. A script checked this rule against all 81 entries of the `and` table. The gates thus keep the soundness of the three-valued case, and strength only matters on wires with several drivers.

## Examples and non-examples

**Example: a tristate bus.** Two tristate buffers drive one wire. When one is enabled with 1 and the other is off, the drivers are 1 and Z, and the wire is 1. When both are enabled with different values, it is X, which marks a bus fight. When both are off, it is Z, and any gate that reads it sees X.

**Example: an open-drain line with a pull-up.** A resistor to the supply drives H. Each open-drain output drives 0 or Z. The resolved value is H if all outputs are Z and 0 if any output is 0, so the line computes the AND of the outputs. Two pull-ups give $H \sqcup H = H$, and a pull-up and a pull-down give $H \sqcup L = W$, a weak conflict that a forcing driver can still override.

**Example: U and X.** A signal of type `std_logic` starts at U, the leftmost value of the type. If a flip-flop is never reset, its output stays U, and a wire that it drives together with other drivers resolves to U, whatever the others drive. So U tracks "never set", and X tracks "set, but to an unknown or conflicting value". After `To_X01`, both are X.

**Non-example: X pessimism.** Let $y = x \land \lnot x$ with $x = X$. The tables give $\lnot x = X$ and $y = X \land X = X$, but $y = 0$ for both completions. The value system does not remember that the two inputs of the AND gate come from the same signal. The same happens on every reconvergent fanout, such as the multiplexer $s a + \bar s b$ with $a = b = 1$ and $s = X$, which gives X in place of 1. The gate-by-gate result is sound but not exact; the exact value $\hat f$ of the whole circuit needs all completions, which is exponential in the number of X inputs.

**Non-example: X optimism in HDL code.** The tables are pessimistic, but the statements of a hardware description language can be optimistic. In Verilog, `if (s) y = a; else y = b;` takes the else branch when `s` is X, so `y = b` although the hardware could give `a`. A `case` statement with no matching item behaves in a similar way. These results are not sound, and they can hide a reset bug that gate-level simulation shows.

**Non-example: '-' in a comparison.** The value '-' marks a don't care for synthesis, but the operator `=` on `std_logic` treats it as one more value, so `"1-" = "10"` is false. The function `std_match` of the numeric packages reads '-' as matching any value. The resolution table does not give '-' this meaning either.

**Non-example: Z is not a gate output.** A gate that computes a function never drives Z. Only a tristate driver, a transmission gate or a switch drives Z. A switch-level simulator, which models charge on a node with no driver, needs more than Z: see [switch-level simulation](/switch-level-simulation/), where an undriven node keeps its last value.

## Related definitions

- **[Ternary simulation](/ternary-simulation/).** Uses 0, 1 and X with the information order to find hazards and races, with the full proof of monotonicity and soundness.
- **[Switch-level simulation](/switch-level-simulation/).** Replaces the fixed strengths of IEEE 1164 by a scale of transistor strengths and node sizes.
- **[Delta cycle](/delta-cycle/).** The determinism of the VHDL cycle needs a resolution function that does not depend on the order of the drivers, which the join gives.
- **[Event-driven logic simulation](/event-driven-logic-simulation/) and [compiled-code logic simulation](/compiled-code-logic-simulation/).** Both work with these values; compiled code with X needs two words per net.
- **[Symbolic trajectory evaluation](/symbolic-trajectory-evaluation/).** Uses 0, 1 and X with a fourth value for a conflict, and runs ternary simulation with symbolic values.
- **[Fault simulation](/fault-simulation/).** Uses X for flip-flops with an unknown initial state, so a fault is detected only where the good and faulty values are both binary and differ.
- **[Knaster-Tarski theorem](/knaster-tarski-theorem/).** Monotone functions on a lattice have least fixed points, the base of the ternary fixed point computations.

## References
