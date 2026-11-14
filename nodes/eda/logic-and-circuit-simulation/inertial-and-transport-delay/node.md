---
tag: NCPZRX
kind: definition
slug: inertial-and-transport-delay
name: Inertial and transport delay
aliases:
- inertial delay
- transport delay
area: eda/logic-and-circuit-simulation
level: intro
summary: Two delay models of logic simulation, where transport delay passes every pulse after a delay, inertial delay also swallows pulses shorter than the gate delay.
prereqs: [logic-simulation]
see_also: [event-driven-logic-simulation, delta-cycle, glitch-power, ternary-simulation, timing-simulation, event-driven-simulation]
sources:
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter Logic Simulation, the part on delay models (transport delay, inertial delay, rise and fall delays) and their handling in event-driven simulation (general locator)
  - paper: "IEEE Std 1076-2008, IEEE Standard VHDL Language Reference Manual, IEEE, 2009"
    title: IEEE Standard VHDL Language Reference Manual, IEEE Std 1076-2008
    locator: the section on signal assignment statements, the delay mechanism (transport, inertial, and reject with a pulse rejection limit) and the updating of a projected output waveform (general locator)
  - paper: "IEEE Std 1364-2005, IEEE Standard for Verilog Hardware Description Language, IEEE, 2006"
    title: IEEE Standard for Verilog Hardware Description Language, IEEE Std 1364-2005
    locator: the clauses on continuous assignments, gate delays and nonblocking procedural assignments (general locator)
---

A delay model of [logic simulation](/logic-simulation/) says how the output of a gate follows the value that its Boolean function asks for. This page is in the logic simulation half of the sub-area, and the delay models it defines are the nominal fixed delay $d$ per gate in two forms. **Transport delay** copies the asked-for value to the output after $d$, so every pulse goes through, however short. **Inertial delay** also copies it after $d$, but it removes every pulse that is shorter than $d$: a gate must see a new value for at least its delay before its output follows. Transport delay models an ideal wire or delay line. Inertial delay models a gate that has to charge a load and cannot follow a fast input. Neither is the behavior of a real gate, whose delay depends on the load, the input slope and the process, but they are the two rules that [event-driven logic simulation](/event-driven-logic-simulation/) and the hardware description languages use.

## Definition

**Signals.** Let $z(t)$ be the value that the gate function asks for, computed from the present values of the gate inputs. It is piecewise constant: it starts at $z_0$ at time 0 and changes at the times $s_1 < s_2 < \cdots$ to the values $v_1, v_2, \ldots$, with $v_k \ne v_{k-1}$ and $v_0 = z_0$. Call the interval $[s_k, s_{k+1})$ the $k$-th piece of $z$, with $s_0 = 0$ and $s_{k+1} = \infty$ for the last piece. Its width is $w_k = s_{k+1} - s_k$. A pulse of width $w$ is a piece of width $w$ between two pieces of the other value. Let $d > 0$ be the gate delay, and let the output $y$ start at $y(0) = z_0$.

**Transport delay.** $y(t) = z(t - d)$ for $t \ge d$, and $y(t) = z_0$ for $t < d$. As an event rule: when $z$ changes to $v$ at time $s$, schedule the output event "$y = v$ at $s + d$", and keep all earlier pending events.

**Inertial delay.** As an event rule: when $z$ changes to $v$ at time $s$, first apply any output event that is due at $s$, then cancel every pending output event, and schedule "$y = v$ at $s + d$" if $v$ differs from the present output value. This is the rule of line L10 on the [event-driven logic simulation](/event-driven-logic-simulation/) page.

**Characterization of inertial delay (exact).** Call the $k$-th piece of $z$ *long* if $k = 0$ or $w_k \ge d$. Let $F(t)$ be the value of the last long piece $j$ with $s_j + d \le t$, where the piece 0 counts with $s_0 + d \le t$ for all $t \ge 0$. Then the inertial rule gives $y = F$. In words: the output is $z$ delayed by $d$ with every piece shorter than $d$ removed, and the value before a removed piece held through it.

*Proof.* The claim is that the following holds just after the rule acts at each change time $s_k$, for $k \ge 1$:

1. $y(t) = F(t)$ for $0 \le t \le s_k$;
2. the only pending event is "$y = v_k$ at $s_k + d$" if $v_k \ne F(s_k)$, and there is none otherwise.

Before $s_1$, $z = z_0$, nothing is pending, $y = z_0$, and $F = z_0$ since only piece 0 qualifies. At $s_1$ nothing is due, and the rule cancels nothing and schedules $v_1$ at $s_1 + d$ exactly when $v_1 \ne y(s_1) = z_0 = F(s_1)$. So both parts hold for $k = 1$.

Suppose both hold for $k$, and look at the interval $(s_k, s_{k+1}]$. No long piece $j < k$ changes $F$ in this interval, since $s_j + d \le s_{j+1} \le s_k$. A piece $j > k$ has $s_j + d > s_{k+1}$. So $F$ can change in the interval only at $s_k + d$, to $v_k$, and only if piece $k$ is long. There are two cases.

- *Piece $k$ is long*, $s_{k+1} \ge s_k + d$. The pending event, if any, falls in the interval. It sets $y = v_k$ at $s_k + d$, which is where $F$ becomes $v_k$. If there was no event, $v_k = F(s_k)$ and neither $y$ nor $F$ changes. At $s_{k+1}$ an event due at that time is applied first, so the present output is $F(s_{k+1})$.
- *Piece $k$ is short*, $s_{k+1} < s_k + d$. The pending event lies after $s_{k+1}$, so nothing changes $y$ in the interval, and $F$ does not change either. At $s_{k+1}$ the rule cancels the event before it is due.

In both cases $y = F$ on $(s_k, s_{k+1}]$, nothing is pending after the cancel step, and the rule then schedules $v_{k+1}$ at $s_{k+1} + d$ exactly when $v_{k+1} \ne y(s_{k+1}) = F(s_{k+1})$. So both parts hold for $k + 1$. If there is no next change, the same case analysis on $(s_k, \infty)$ ends the proof. $\square$

**Pulses (exact).** Take a pulse of width $w$ between two long pieces of the other value $a$, so $z$ is $a$, then $b$ on $[s, s + w)$, then $a$.

- Transport delay gives the output pulse $b$ on $[s + d, s + w + d)$, of the same width $w$, for every $w > 0$.
- Inertial delay gives the same output pulse if $w \ge d$, and no pulse if $w < d$. This follows from the characterization: piece $b$ is long exactly when $w \ge d$, and the value before it is $a$. A pulse of width exactly $d$ passes, because at $s + d$ the rule applies the due event $y = b$ before it reacts to the change back to $a$.

So inertial delay filters pulses shorter than the delay, and transport delay keeps them.

**In the languages.** In VHDL, `y <= x after 5 ns;` is inertial, `y <= transport x after 5 ns;` is transport, and `y <= reject 2 ns inertial x after 5 ns;` keeps the delay at 5 ns but uses a pulse rejection limit of 2 ns in place of the delay. In Verilog, a delay on a continuous assignment or a gate instance, such as `assign #5 y = x;`, acts as an inertial delay, and a nonblocking assignment with an intra-assignment delay in an `always` block, `y <= #5 x;`, schedules every change and acts as a transport delay. The exact rules, for example for a signal with pending events of several values, are in the standards cited below.

## Examples and non-examples

**Example: one buffer.** A buffer with $d = 3$ gets $z = 0$, with changes to 1 at 2, to 0 at 4, to 1 at 10 and to 0 at 15. The first pulse has width 2 and the second width 5.

| model | output events | output pulses |
|---|---|---|
| transport | 1 at 5, 0 at 7, 1 at 13, 0 at 18 | $[5, 7)$ and $[13, 18)$ |
| inertial | 1 at 13, 0 at 18 | $[13, 18)$ |

Under the inertial rule, the change at 2 schedules 1 at 5, and the change at 4 cancels it, since $4 < 5$, and schedules nothing, since the output is still 0. A script ran the event rule and the formula $F$ on 20000 random waveforms with integer change times and delays from 1 to 5, and they agreed on all of them. With $d = 3$ and a pulse from 10 to 13, of width exactly $d$, the rule gives the output pulse $[13, 16)$.

**Example: a hazard pulse.** On the [event-driven logic simulation](/event-driven-logic-simulation/) page, a static hazard makes a gate function go to 0 for a short time. With transport delay the pulse appears at the output and travels on. With an inertial delay longer than the pulse, the output stays at 1. For power estimation this pulse is real switching; see [glitch power](/glitch-power/).

**Non-example: two inertial buffers in series.** Two inertial buffers with $d = 2$ each do not act like one inertial buffer with $d = 4$. A pulse of width 3 at the input passes the first buffer, since $3 \ge 2$, and the second for the same reason, so the output has a pulse $[14, 17)$ for an input pulse $[10, 13)$. One buffer with $d = 4$ removes it. Inertial delay is not additive, so moving delay from one gate to the next changes which pulses survive. Transport delay is additive: two buffers with $d_1$ and $d_2$ give $y(t) = z(t - d_1 - d_2)$.

**Non-example: unequal rise and fall delays.** Let a buffer have rise delay $d_r = 4$ and fall delay $d_f = 1$, with transport delay. A 1 pulse of width 2 at the input asks for 1 at $s + 4$ and for 0 at $s + 3$, which comes first. The output events are out of time order, and the pulse has width $w + d_f - d_r = -1$. So with unequal rise and fall delays even the transport model loses pulses, here every 1 pulse of width at most 3, and a simulator must either use the inertial rule or keep the events sorted and drop the pulse. The event-driven page lists the same pitfall.

**Non-example: zero delay.** With $d = 0$ the two models agree, because no pending event can be cancelled before it is due. The order of the changes at one time is then given by [delta cycles](/delta-cycle/), not by these rules.

## Related definitions

- **[Event-driven logic simulation](/event-driven-logic-simulation/).** The algorithm that applies both rules, and its proof that transport delay matches a step-by-step simulation.
- **[Delta cycle](/delta-cycle/).** The order of zero-delay changes at one time.
- **[Ternary simulation](/ternary-simulation/).** Finds hazards for every choice of gate delays at once, in place of fixing one delay model.
- **[Glitch power](/glitch-power/).** The power used by short pulses, which an inertial model can hide.
- **[Timing simulation](/timing-simulation/).** Follows node voltages, so a short input pulse gives a partial swing at the output instead of all or nothing.
- **[Event-driven simulation](/event-driven-simulation/).** The generic event loop that holds the pending events.

## References
