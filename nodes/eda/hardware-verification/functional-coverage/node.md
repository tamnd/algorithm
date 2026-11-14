---
tag: VT7FQR
kind: concept
slug: functional-coverage
name: Functional coverage
aliases:
- covergroups
- coverage model
area: eda/hardware-verification
level: core
summary: User-written coverage points and crosses over design and test values that record which features of the specification have been exercised.
prereqs: [code-coverage-metrics]
see_also: [fsm-coverage, assertion-based-verification, constrained-random-stimulus-generation, coverage-directed-test-generation, observability-based-coverage, fault-coverage, greedy-set-cover, coupon-collector-problem]
sources:
  - paper: "IEEE Std 1800-2017, IEEE Standard for SystemVerilog, Unified Hardware Design, Specification, and Verification Language, IEEE, 2018"
    title: IEEE Standard for SystemVerilog, Unified Hardware Design, Specification, and Verification Language, IEEE Std 1800-2017
    locator: Clause 19 (Functional coverage, with coverage groups, coverage points, bins, transition bins, cross coverage, options and the computation of coverage)
  - book: isbn:9781402080258
    title: Andrew Piziali, Functional Verification Coverage Measurement and Analysis, Kluwer, 2004
    locator: the chapters on the verification plan, on the design of a coverage model from the specification, and on coverage analysis and closure (general locator)
  - paper: doi:10.1109/54.936247
    title: Serdar Tasiran and Kurt Keutzer, Coverage metrics for functional validation of hardware designs, IEEE Design and Test of Computers 18(4), 36 to 45, 2001
    locator: the comparison of specification-based metrics with code and state-machine metrics
---

Functional coverage measures which features of a specification the simulation runs of a design have exercised, by counting hits on *coverage items* that the verification engineer writes: points that sample a value and sort it into bins, crosses of several points, sequences of values, and temporal cover goals. The set of items is the *coverage model*. Its score is the share of bins hit, under a stated rule for combining items. Unlike [code coverage](/code-coverage-metrics/) and [FSM coverage](/fsm-coverage/), whose items come from the source text, functional coverage items come from the specification, so a feature that the code forgets can still have an item. The price is that the model is only as complete as its author made it.

## In plain words

Before testing, the team lists the situations that matter: every instruction type, every packet length class, every instruction type with and without a carry, a full buffer followed by a read. Each situation becomes a box with a name. During simulation, a monitor looks at the design at chosen moments and puts a tick in each box whose situation it sees. At the end, the boxes with no tick show what the tests never tried.

Because the boxes come from the specification and not from the code, a box can exist for behavior that the code is missing. A ticked box says only that the situation happened, not that the design handled it right; a checker must say that. And a situation that nobody wrote a box for is never reported as missing.

## The idea

**Coverage items and bins.** A *coverage point* is an expression $e$ sampled at an event, for example the operation code of an ALU at each clock edge where a transaction is valid. Its *bins* are sets of values; a bin is hit when a sample of $e$ falls in it. Bins can be single values, ranges, or automatic bins (one per value, or ranges when the value set is large). *Illegal bins* report an error when hit, and *ignore bins* remove values from the count. In SystemVerilog these are written inside a `covergroup` with `coverpoint` and `bins` (IEEE Std 1800-2017, Clause 19).

**Crosses.** A *cross* of points $e_1, \ldots, e_k$ has one bin per tuple of bins $(b_1, \ldots, b_k)$, and that bin is hit when one sample hits $b_1, \ldots, b_k$ at the same time. With $m_i$ bins on point $i$, the cross has $\prod_i m_i$ bins before ignored tuples are removed. The product grows fast, so a cross of a few points can hold more bins than a regression ever hits, and many of its tuples may be impossible by the specification.

**Transitions and sequences.** A *transition bin* such as `(IDLE => BUSY => DONE)` is hit when consecutive samples of a point take those values. Temporal cover goals, `cover property` in SVA and `cover` in PSL, are hit when a sequence over clock cycles matches; they come from [assertion-based verification](/assertion-based-verification/).

**The score.** Let the model have items $C_1, \ldots, C_r$, and let item $C_j$ have the set $B_j$ of bins, of which the runs hit $H_j$. Two ways to combine them are common:

$$ \text{flat} = \frac{\sum_j |H_j|}{\sum_j |B_j|}, \qquad \text{weighted} = \frac{\sum_j w_j \, |H_j| / |B_j|}{\sum_j w_j}. $$

SystemVerilog computes the coverage of a coverage group as the weighted average of the coverage of its points and crosses, with the weights given by an option (default 1). The two rules give different numbers for the same hits, so a report must name its rule. A bin can also require a minimum number of hits (`at_least`) before it counts.

**What a full score guarantees.** Every bin of the model was hit at least the required number of times, at the sampling events of the model. That is all.

**What it does not guarantee.**

- *That the design was right.* A hit records a stimulus or a state, not a correct response. Checkers, assertions or a scoreboard must judge the response, and the check must be active when the bin is hit.
- *That the model is complete.* A situation with no bin is never reported. This is the main weakness and the reason why the model is reviewed against the specification.
- *That the right moment was sampled.* A point sampled at the wrong event, or without the condition that a transaction is valid, records values that never mattered.
- *That combinations were hit.* Full coverage of two points does not cover their cross. Two points with $m_1$ and $m_2$ bins can be fully hit with $\max(m_1, m_2)$ samples, while their cross needs $m_1 m_2$.

**The cost of random hits.** Under purely random stimulus, if each sample hits one of $m$ equally likely bins, the expected number of samples to hit all of them is $m H_m \approx m \ln m$, the [coupon collector](/coupon-collector-problem/) bound. Rare bins take much longer. This is one reason for [constrained random](/constrained-random-stimulus-generation/) stimulus with biases and for [coverage-directed generation](/coverage-directed-test-generation/).

## Examples

**A model with a hole.** An 8-bit ALU takes `op` in {ADD, SUB, AND, OR}, two operands `a` and `b`, and a carry in `cin`, and returns a result and a carry out `cout`. The model is

```
covergroup alu_cg @(posedge clk iff valid);
  cp_op    : coverpoint op;          // 4 bins
  cp_cin   : coverpoint cin;         // 2 bins
  op_x_cin : cross cp_op, cp_cin;    // 8 bins
endgroup
```

Eight transactions, one per (op, cin) pair, with operands below 16, hit all 14 bins: the score is 100 percent by both rules. Suppose the design computes `cout` wrong whenever $a + b + \mathit{cin} \ge 256$. With operands below 16 the sum is at most 31, so no transaction triggers the bug, and the model has no bin that asks for it. Add `cp_cout : coverpoint cout;` with 2 bins. The bin `cout = 1` stays empty. Now 15 of 16 bins are hit, a flat score of $15/16 = 93.75$ percent, and the weighted score with unit weights is $(1 + 1 + 1 + 1/2)/4 = 87.5$ percent. Both show the hole, and filling it means generating sums of 256 or more, which exposes the bug.

**Bins from the specification.** A packet length from 1 to 64 bytes, where the specification treats 1 to 4, 5 to 63 and 64 differently and forbids 0:

```
coverpoint len { bins small = {[1:4]}; bins mid = {[5:63]}; bins max = {64}; illegal_bins zero = {0}; }
```

Three bins, plus an error if a length 0 is ever seen. Automatic bins would have made 64 bins and given no extra weight to the boundary 64.

**A cross that cannot be closed.** A cross of `op` (4 bins) with a 3-bin `mode` point has 12 bins. If the specification forbids SUB in one mode, one tuple is impossible, and the score is capped at 11 of 12 until that tuple is declared as an ignore bin. Deciding that a tuple is impossible in the design, rather than only in the specification, is a [reachability](/reachability-problem/) question that a formal tool can answer through a cover goal.

**Coverage versus fault coverage.** A [fault coverage](/fault-coverage/) of 98 percent for a set of manufacturing test patterns and a functional coverage of 98 percent for a regression measure different things on different objects: detected stuck-at faults in a netlist, and bins of a model of the specification.

## Where it is used

- **Verification plans and sign-off.** A plan lists the features of the specification and maps each one to items. Closure means that every bin is hit or justified as impossible, together with clean checker results and the agreed code coverage.
- **Steering random stimulus.** The empty bins tell the engineer which constraints and biases to change, or which directed tests to write. Automating that loop is [coverage-directed test generation](/coverage-directed-test-generation/).
- **Regression ranking.** Choosing a small set of runs that hits the same bins is a [set cover](/set-cover/) problem, and tools rank runs with the [greedy method](/greedy-set-cover/).
- **Formal tools.** A cover goal given to a model checker either gets a witness trace or is proved unreachable, which justifies removing its bin from the denominator.

## References
