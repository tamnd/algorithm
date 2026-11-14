---
title: Event-driven simulation computes the transport-delay waveforms, and with zero or unit delays it settles to the levelized values
proves: [correctness]
status: full
---

Let $C$ be a gate-level circuit. Each gate $g$ has a function $f_g$, an output net $\mathrm{out}(g)$ and an integer delay $d(g) \ge 0$. Every net has an initial value $v_0$ in $\{0, 1\}$, and the inputs change only by the given input events. For a time $t$ let $\mathrm{ref}(t)$ be the values of all nets at time $t$ in the model, and let $z_g(t) = f_g(\mathrm{ref}(t) \text{ on the inputs of } g)$. Lines L1 to L11 refer to the pseudocode of the page.

**Transport model.** For integer delays $d(g) \ge 1$, $\mathrm{ref}$ is defined by induction on $t = 0, 1, 2, \ldots$: an input net has the value of its last input event at a time $\le t$ (or $v_0$), and $\mathrm{out}(g)(t) = z_g(t - d(g))$ if $t \ge d(g)$ and $v_0(\mathrm{out}(g))$ otherwise. This is well defined, because $z_g(t - d(g))$ depends only on values at earlier times. To make the statements uniform, put $z_g(s) = v_0(\mathrm{out}(g))$ for $s < 0$.

For a gate output $n$ and a time $u$ after the present time, let $\mathrm{pend}_n(u)$ be the value of the last pending event on $n$ at a time $\le u$, or $\mathrm{val}[n]$ if there is none. Events on one net and one time are ordered by the order in which L10 scheduled them, and L4 keeps the last one.

**Theorem 1 (transport delay, delays at least 1).** Let every $d(g) \ge 1$. For every integer $t \ge 0$, after the algorithm has handled time $t$ (or has skipped it because $W$ had no event at $t$), $\mathrm{val} = \mathrm{ref}(t)$. This holds on any circuit, with or without loops.

*Proof.* We prove by induction on $t \ge -1$ the invariant $I(t)$: after time $t$ is handled,

1. $\mathrm{val} = \mathrm{ref}(t)$ (for $t = -1$, read this as $\mathrm{val} = v_0$);
2. for every gate $g$ with $n = \mathrm{out}(g)$ and $d = d(g)$: $\mathrm{proj}[n] = z_g(t)$, and $\mathrm{pend}_n(u) = z_g(u - d)$ for all $u$ with $t < u \le t + d$;
3. no pending event has a time $\le t$.

*Base, $t = -1$.* L1 sets $\mathrm{val} = \mathrm{proj} = v_0$, and only input events are pending. For $u \le d - 1$ we have $z_g(u - d) = v_0(n) = \mathrm{val}[n] = \mathrm{pend}_n(u)$, and $\mathrm{proj}[n] = v_0(n) = z_g(-1)$.

*Step from $t - 1$ to $t$.* By part 3 of $I(t-1)$, the events taken at L4 are exactly the pending events of time $t$. For an input net, they are the input events of time $t$, and the last one wins, as in $\mathrm{ref}$. For a gate output $n$, the last event at time $t$, or no event, gives the new value $\mathrm{pend}_n(t) = z_g(t - d) = \mathrm{ref}(t)(n)$ by part 2. So after L5, $\mathrm{val} = \mathrm{ref}(t)$, which is part 1. Since all delays are at least 1, the events scheduled at time $t$ have times $> t$, so there is one pass at time $t$ and part 3 holds.

Now take a gate $g$ with $n = \mathrm{out}(g)$. If no input of $g$ is in the set $A$ of L5, then the inputs of $g$ have the same values at $t - 1$ and $t$ (at $t = 0$ every gate is evaluated, so this case does not occur there). So $z_g(t) = z_g(t - 1) = \mathrm{proj}[n]$, and nothing is scheduled. The window $t < u \le t + d$ gains the point $u = t + d$, and $\mathrm{pend}_n(t + d) = \mathrm{pend}_n(t + d - 1) = z_g(t - 1) = z_g(t)$, because no event on $n$ lies at time $t + d$: an event at $t + d$ would have been scheduled at time $t$. If $g$ is evaluated, L8 computes $v = z_g(t)$, because $\mathrm{val} = \mathrm{ref}(t)$. Two cases.

- $v = \mathrm{proj}[n] = z_g(t - 1)$. Nothing is scheduled, and the same argument as above gives part 2.
- $v \ne \mathrm{proj}[n]$. L10 sets $\mathrm{proj}[n] = v = z_g(t)$ and schedules $v$ at $t + d$. All other pending events on $n$ lie at times $\le t - 1 + d$, so this event is the last one at or before $t + d$, and $\mathrm{pend}_n(t + d) = v = z_g(t)$. For $t < u < t + d$, nothing changed, and $\mathrm{pend}_n(u) = z_g(u - d)$ by $I(t - 1)$.

If the algorithm skips time $t$ because no event is pending at $t$, then no net changes at $t$, so $\mathrm{ref}(t) = \mathrm{ref}(t - 1)$ (by part 2, every gate output keeps $\mathrm{pend}_n(t) = \mathrm{val}[n]$), every $z_g(t) = z_g(t - 1)$, and the argument of the unselected case gives $I(t)$. $\square$

**Inertial model.** Here $\mathrm{out}(g)(t) = z_g(t - d)$ if $z_g$ has the same value at all integer times $t - d, \ldots, t - 1$, and $\mathrm{out}(g)(t) = \mathrm{out}(g)(t - 1)$ otherwise (with the initial value for $t < d$). In the algorithm, L10 cancels all pending events of $n$ and schedules $v$ at $t + d$ only if $v \ne \mathrm{val}[n]$.

**Theorem 2 (inertial delay, delays at least 1).** With the inertial rule, $\mathrm{val} = \mathrm{ref}(t)$ after time $t$, for every $t \ge 0$ and every circuit.

*Proof.* Replace part 2 of the invariant by: $\mathrm{proj}[n] = z_g(t)$, and $n$ has at most one live pending event. It exists exactly when $z_g(t) \ne \mathrm{val}[n]$, and then it has the value $z_g(t)$ and the time $s + d$, where $s \le t$ is the last time at which $z_g$ changed (that is, $z_g(s) \ne z_g(s - 1)$). The step is as before. A gate whose $z_g$ does not change at $t$ gives $v = \mathrm{proj}[n]$, so nothing happens. A gate whose $z_g$ changes at $t$ gives $v \ne \mathrm{proj}[n]$, so the old event is cancelled, and a new one at $t + d$ is made exactly when $v \ne \mathrm{val}[n]$. So $\mathrm{val}[n]$ changes at time $T$ exactly when $z_g$ changed at $T - d$ to a value $v \ne \mathrm{val}[n]$ and did not change at $T - d + 1, \ldots, T - 1$. This is the rule of the model: if $z_g$ is constant on $T - d, \ldots, T - 1$ and changed at $T - d$, then $\mathrm{out}(T) = z_g(T - d)$, and if it is constant there but did not change at $T - d$, then it was constant on $T - d - 1, \ldots, T - 2$, so $\mathrm{out}(T - 1)$ already has that value. $\square$

**Theorem 3 (zero delay, acyclic circuit).** Let every $d(g) = 0$ and let $C$ have no loops, with depth $D$ (the largest number of gates on a path). At each time $t$ that has events, the delta passes stop after at most $D + 1$ passes, and then $\mathrm{val}$ equals the direct evaluation of $C$ on the inputs of time $t$.

*Proof.* Let the level of a primary input be 0 and the level of a gate output be one more than the largest level of its inputs. The changes in pass 1 are input events, on nets of level 0, and at time 0 the first pass evaluates all gates, which have level $\ge 1$. A gate evaluated in pass $k$ has an input that changed in pass $k$; if all changes in pass $k$ are on nets of level $\ge k - 1$, then each evaluated gate has level $\ge k$, and its event, applied in pass $k + 1$, is on a net of level $\ge k$. By induction, the changes in pass $k$ are on nets of level $\ge k - 1$. No net has a level above $D$, so pass $D + 2$ has no events, and there are at most $D + 1$ passes.

When the passes stop, no event is pending at time $t$, and with zero delays no event is pending at any later time either. For each gate output $n$, $\mathrm{proj}[n]$ is the value of the last event scheduled on $n$, and that event has been applied, so $\mathrm{val}[n] = \mathrm{proj}[n]$. After each pass, $\mathrm{proj}[\mathrm{out}(g)] = f_g(\mathrm{val} \text{ on the inputs of } g)$ for every gate: it held after $g$ was last evaluated, and the inputs of $g$ have not changed since, because every change of an input puts $g$ into the set of L6. So $\mathrm{val}[\mathrm{out}(g)] = f_g(\mathrm{val}[\text{inputs}])$ for every gate. The values are a solution of the circuit equations with the given inputs. In an acyclic circuit, induction on the level shows that this solution is unique, and the direct evaluation is a solution. $\square$

**Corollary (unit delay, acyclic circuit).** With every $d(g) = 1$, if the last input event is at time $t_0$, then $\mathrm{val}$ does not change after $t_0 + D$, and it then equals the direct evaluation of $C$ on the final inputs.

*Proof.* By Theorem 1, $\mathrm{ref}$ is the unit-delay model. A net of level $\ell$ has a value at time $t \ge t_0 + \ell$ that depends only on the inputs at times $\ge t_0$, which are the final inputs: by induction on $\ell$, $\mathrm{out}(g)(t) = f_g(\mathrm{ref}(t - 1))$, and the inputs of $g$ have level $< \ell$, so their values at $t - 1 \ge t_0 + \ell - 1$ are already the direct values. $\square$

So with zero or unit delays, the settled values of event-driven simulation equal the values of levelized evaluation on an acyclic circuit. The waveforms before settling can differ: they can contain glitches and zero-width delta pulses that levelized evaluation never shows.
