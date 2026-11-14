---
tag: C4VGK0
kind: model
slug: path-delay-fault-model
name: Path delay fault model
aliases:
- path delay fault
area: eda/test-and-diagnosis
level: core
summary: A fault model in which the total delay of one path exceeds the clock period, tested by a two-pattern test that launches a transition down the path.
prereqs: [transition-fault-model, static-timing-analysis]
see_also: [robust-path-delay-test, false-path, dag-longest-path, timing-graph, setup-and-hold-constraints, launch-on-capture-and-launch-on-shift, fault-coverage, topological-sort]
sources:
  - paper: "G. L. Smith, Model for delay faults based upon paths, Proceedings of the International Test Conference, 342 to 349, 1985"
    title: G. L. Smith, Model for delay faults based upon paths, Proceedings of the International Test Conference, 342 to 349, 1985
    locator: the path delay fault, with a rising or falling transition at the start of a path, and its two-pattern tests
  - paper: "C. J. Lin and S. M. Reddy, On delay fault testing in logic circuits, IEEE Transactions on Computer-Aided Design CAD-6(5), 694 to 703, 1987"
    title: C. J. Lin and S. M. Reddy, On delay fault testing in logic circuits, IEEE Transactions on Computer-Aided Design CAD-6(5), 694 to 703, September 1987
    locator: robust and non-robust tests of path delay faults and their generation
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Delay Test (path delay faults, path counts, robust and non-robust tests)
---

The path delay fault model describes a timing defect as a path of a circuit whose total delay is too large. A fault is a path from an input to an output together with the direction of the transition at its start, rising or falling. The fault is present when a transition launched at the start of the path reaches the end later than the clock period allows. Unlike the [transition fault model](/transition-fault-model/), it catches a sum of small extra delays spread along a path, but a circuit can have a number of paths that is exponential in its size, so only a selected list of paths is tested.

## The machine

The circuit is a combinational gate circuit $C$ between launch points (primary inputs or flip-flops) and capture points (primary outputs or flip-flops), clocked with period $\tau$. A **path** is a sequence of lines $P = (x_0, x_1, \ldots, x_k)$ where $x_0$ is a launch point, $x_k$ is a capture point, and each $x_{i+1}$ is a gate (or fanout branch) with $x_i$ as one of its inputs, called the **on-path input**. The other inputs of $x_{i+1}$ are its **off-path inputs**. A **path delay fault** is a pair $(P, \uparrow)$ or $(P, \downarrow)$: a rising or falling transition at $x_0$. The direction at each later line follows from the inversions along the path.

The assumptions are:

- **Delay of a path.** Each gate has a delay for a rising and for a falling output, and the delay of $P$ for the transition is the sum along the path. The fault is present when this sum exceeds $\tau$ minus the setup time of the capture point (see [setup and hold constraints](/setup-and-hold-constraints/)).
- **One faulty path.** The test is judged for one path at a time. Whether other paths are also slow is left open, and the robust and non-robust classes below differ in how they treat it.

A test is a pair of vectors $(v_1, v_2)$. It must launch the transition at $x_0$, so $x_0(v_1) \ne x_0(v_2)$ in the right direction, and it must sensitize the path, so that a late arrival along $P$ makes the value captured at $x_k$ wrong. The conditions on the off-path inputs that make this sure define the [robust and non-robust tests](/robust-path-delay-test/).

## What it counts

The model predicts which paths a test set has checked for timing, and so the path delay fault coverage: the fraction of the faults of a path list that the tests detect, often split into robustly and non-robustly detected. The list is chosen first. All paths are too many in most circuits, so tools take the paths that [static timing analysis](/static-timing-analysis/) reports as longest, or the longest path through each line. The coverage is a fraction of that list, and a report should give the list.

Take $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$, with the stem $b$ and its branches $b_g$ and $b_h$. It has four paths from an input to $z$: $a\,g\,z$, $b\,b_g\,g\,z$, $b\,b_h\,h\,z$ and $c\,h\,z$, so 8 path delay faults. For $(a\,g\,z, \uparrow)$, the second vector must set $a = 1$, the off-path input $b_g$ to 1 so that $g$ follows $a$, and the off-path input $h$ to 1 so that $z$ follows $g$, which gives $v_2 = 110$. With $v_1 = 010$, $a$ rises, $g$ falls, $z$ rises, and $b$ and $h$ stay at 1 throughout. If the path is slow, $z$ still holds 0 at the capture, and the fault is detected whatever the delays of the other lines, since no line off the path changes.

## Relation to other models

- **Transition faults.** A transition fault puts a gross delay on one line, and a transition test may propagate it along any path. A path delay test fixes the path, so it can detect small delays on long paths. The two models count differently: $2L$ transition faults against two faults per path.
- **Static timing analysis.** [Static timing analysis](/static-timing-analysis/) bounds the delay of every path without vectors, on the [timing graph](/timing-graph/). The path delay model checks the paths on silicon. A path that no vector pair can sensitize is a [false path](/false-path/) for timing, and its path delay faults are untestable.
- **Scan launch.** In a scan design, the pair comes from [launch on shift or launch on capture](/launch-on-capture-and-launch-on-shift/), which restricts which pairs can be applied.
- **Segment and gate delay faults.** Intermediate models put the extra delay on a segment of a path of bounded length, between the path and the single line.

## Known results in the model

- **The number of paths can be exponential.** Take $k$ stages. Stage $i$ has the line $s_i$, two new inputs $x_i$ and $y_i$, two gates $p_i = \mathrm{AND}(s_i, x_i)$ and $q_i = \mathrm{AND}(s_i, y_i)$, and the output $s_{i+1} = \mathrm{OR}(p_i, q_i)$, with $s_0$ an input. The circuit has $3k$ gates and $O(k)$ lines, counting the two branches of each $s_i$. *Claim:* the number of paths from $s_0$ to $s_k$ is $2^k$. *Proof.* By induction on $k$. For $k = 0$ there is one path. A path from $s_0$ to $s_{i+1}$ ends with $s_{i+1}$, and its line before $s_{i+1}$ is $p_i$ or $q_i$. Each of these is reached from $s_i$ only, through its own branch, since $x_i$ and $y_i$ are inputs. So the paths to $s_{i+1}$ are the paths to $s_i$ extended in two ways, and their number doubles. $\square$ So the circuit has $2^{k+1}$ path delay faults on these paths. Each of them has a test: for each stage, set the side input of the on-path AND to 1 and the side input of the other AND to 0, in both vectors, and launch the transition at $s_0$. Then every off-path input of the path is constant and non-controlling, and the transition runs along the path alone.
- **Counting paths is linear.** The number of paths into each line is the sum of the numbers of paths into its inputs, with 1 at each launch point. In [topological order](/topological-sort/) this takes $O(L + P)$ time for $L$ lines and $P$ gate input pins, so the number of faults can be found without listing them. In the same way, the longest path through each line is a [longest path in a DAG](/dag-longest-path/), which gives the path list that test tools target.
- **Untestable paths.** Replace the stage of the example by $p_i = \mathrm{BUF}(s_i)$, $q_i = \mathrm{NOT}(s_i)$ and $s_{i+1} = \mathrm{OR}(p_i, q_i)$. The path count is still $2^k$, but the side input of each OR is now the complement of the on-path input, so the OR is constant 1, no path propagates a transition, and all path delay faults are untestable. In real circuits a large share of paths is untestable or has no robust test, which is why coverage is reported over a list or over the testable paths.
- **Hardness.** Deciding whether a path delay fault has a test, robust or not, is NP-complete. It is in NP, since a vector pair is a certificate that can be checked in polynomial time. For hardness, take a circuit $F$ for a [SAT](/sat/) instance, a new input $x_0$, and the output $z = \mathrm{AND}(x_0, F)$. The path $(x_0, z)$ with a rising transition has a test exactly when $F$ can be 1: a test needs the off-path input $F$ at 1 in $v_2$, and any satisfying assignment, held in both vectors, keeps $F$ at a steady 1, which meets the robust conditions too.

## References
