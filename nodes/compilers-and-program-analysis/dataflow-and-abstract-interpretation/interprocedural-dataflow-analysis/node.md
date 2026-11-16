---
tag: D27P42
kind: concept
slug: interprocedural-dataflow-analysis
name: Interprocedural dataflow analysis
aliases:
- interprocedural analysis
- whole-program analysis
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: Dataflow analysis across procedure calls, which must match each return with its call to avoid facts from paths that cannot occur.
prereqs: [dataflow-analysis, monotone-dataflow-framework, call-graph]
see_also: [context-sensitivity, functional-approach-interprocedural, ifds-framework, ide-framework, cfl-reachability, pushdown-reachability, call-graph-construction, interprocedural-constant-propagation]
sources:
  - paper: "Micha Sharir and Amir Pnueli, Two approaches to interprocedural data flow analysis, in Steven S. Muchnick and Neil D. Jones (eds.), Program Flow Analysis: Theory and Applications, Prentice-Hall, 1981"
    locator: the interprocedurally valid paths, the meet over valid paths as the goal, and the call-string and functional approaches
  - paper: doi:10.1145/199448.199462
    title: "Thomas Reps, Susan Horwitz and Mooly Sagiv, Precise interprocedural dataflow analysis via graph reachability, Proceedings of the 22nd ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL '95), 49 to 61, 1995"
    locator: the supergraph, realizable paths and the meet over all valid paths
  - paper: doi:10.1007/3-540-55984-1_13
    title: "Jens Knoop and Bernhard Steffen, The interprocedural coincidence theorem, Compiler Construction (CC '92), Lecture Notes in Computer Science, 125 to 140, 1992"
    locator: the equality of the interprocedural fixed point and the meet over valid paths for distributive frameworks
  - paper: doi:10.1016/s0950-5849(98)00093-7
    title: "Thomas Reps, Program analysis via graph reachability, Information and Software Technology 40(11-12), 701 to 726, 1998"
    locator: valid paths as a context-free language and interprocedural analysis as CFL-reachability
  - paper: doi:10.1016/j.scico.2005.02.009
    title: "Thomas Reps, Stefan Schwoon, Somesh Jha and David Melski, Weighted pushdown systems and their application to interprocedural dataflow analysis, Science of Computer Programming 58(1-2), 206 to 263, 2005"
    locator: interprocedural dataflow analysis as reachability in a weighted pushdown system
  - paper: doi:10.1145/12276.13327
    title: "David Callahan, Keith D. Cooper, Ken Kennedy and Linda Torczon, Interprocedural constant propagation, Proceedings of the 1986 SIGPLAN Symposium on Compiler Construction, 152 to 161, 1986"
    locator: jump functions and the propagation of constants over the call graph
---

An *interprocedural* dataflow analysis follows facts across procedure calls: into a callee with the arguments, and back to the caller with the results and the side effects. An *intraprocedural* analysis stops at each call and must assume the worst about it. The central difficulty is that a procedure has many callers. A run that enters a procedure from one call site always returns to that call site, and the analysis should consider only paths with this property, the *valid paths*. If it lets facts enter from one caller and leave to another, it adds facts from paths that no run can follow. The goal of an exact interprocedural analysis is the meet over all valid paths (MVP). [Context sensitivity](/context-sensitivity/) is the name for how well an analysis keeps to that goal.

## In plain words

Real programs are made of many functions that call each other. To learn what a variable can hold, an analysis must look inside the functions it calls. A simple way is to join all the flow charts into one big chart, with an arrow from each call into the function and an arrow from the end of the function back to each place that called it. But that big chart has paths that cannot happen: go into a function from one caller and come out at a different caller. A program never does that, because it always returns to where it was called from. If the analysis follows such false paths, it reports facts that are never true. A good interprocedural analysis follows only the paths where each return goes back to its own call.

## The idea

**Supergraph.** Each procedure $p$ has a control flow graph with an entry point $\mathit{entry}_p$ and an exit point $\mathit{exit}_p$. Each call site $s$ in $p$ is split into a call point $c_s$ and a return point $r_s$. The *supergraph* (Reps, Horwitz and Sagiv 1995) is the union of these graphs plus three kinds of edges for each call site $s$ that calls $q$:

| edge | from | to | carries |
|---|---|---|---|
| call edge, label $(_s$ | $c_s$ | $\mathit{entry}_q$ | the arguments and global facts into the callee |
| return edge, label $)_s$ | $\mathit{exit}_q$ | $r_s$ | the result and global facts back to the caller |
| call-to-return edge | $c_s$ | $r_s$ | the facts about the caller's locals, which the callee cannot touch |

With indirect calls, the call graph itself is the result of an analysis ([call graph construction](/call-graph-construction/)).

**Valid paths.** Read the labels of the call and return edges along a path as a string of brackets. A path is *same-level valid* if its brackets are balanced and each $)_s$ closes a $(_s$ with the same $s$. A path from $\mathit{entry}_{main}$ is *valid* if it may leave some calls open but never closes a bracket that it did not open:

$$\mathit{matched} \to \epsilon \mid \mathit{matched}\ \mathit{matched} \mid (_s\ \mathit{matched}\ )_s \mid e, \qquad \mathit{valid} \to \mathit{matched} \mid \mathit{valid}\ (_s\ \mathit{matched},$$

where $e$ is any edge that is not a call or return edge. These are the languages of a [Dyck language](/dyck-language/) with one bracket pair per call site, so a question about valid paths is a [CFL-reachability](/cfl-reachability/) question (Reps 1998). A run of the program follows a valid path, because its call stack sends each return to its own call site.

**Three solutions.** Use the meet convention of Kildall for a [monotone framework](/monotone-dataflow-framework/): $\top$ is the start value, lower is less precise, and $f_\pi$ is the composition of the edge functions along a path $\pi$. (The join convention of Cousot flips the order.) For a point $n$:

- $\mathrm{MVP}(n) = \mathop{\large\sqcap} \{ f_\pi(\iota) : \pi \text{ a valid path from } \mathit{entry}_{main} \text{ to } n \}$, the goal.
- $\mathrm{MOP}_{SG}(n)$, the same meet over *all* paths of the supergraph.
- $\mathrm{MFP}_{SG}$, the greatest fixed point of the equations of the supergraph, as for one big procedure.

**Proposition.** $\mathrm{MFP}_{SG}(n) \sqsubseteq \mathrm{MOP}_{SG}(n) \sqsubseteq \mathrm{MVP}(n)$ for every point $n$, and all three are sound.

*Proof.* The first step is the [coincidence theorem](/mop-mfp-coincidence-theorem/) for monotone frameworks, applied to the supergraph as one graph. The second holds because every valid path is a path of the supergraph, and a meet over more values is lower. Every run follows a valid path, so MVP is below the value of every run's path, and the two lower solutions are below MVP. $\square$

The first step can be strict for monotone functions that are not distributive, and the second can be strict even for distributive ones (the example below). Removing the second gap is what interprocedural analysis is about. The [interprocedural coincidence theorem](/functional-approach-interprocedural/) of Knoop and Steffen (1992) says that the functional approach, which works with procedure summaries, computes exactly MVP when every function is distributive.

**Analysis items** for the instance used in the example, "which variables may depend on the secret input", a forward may problem in the style of [taint analysis](/taint-analysis/):

| item | value |
|---|---|
| direction | forward |
| may or must | may |
| domain | subsets of $D$, the variables of each procedure plus a slot `RET` for the return value |
| order | $X \sqsubseteq Y$ when $X \supseteq Y$ (Kildall convention; in the Cousot convention, $\subseteq$ with $\cup$ as the join) |
| meet | union |
| top and bottom | $\top = \emptyset$, $\bot = D$ |
| boundary | at $\mathit{entry}_{main}$: the secret parameter |
| initial value | $\top = \emptyset$ everywhere else |
| transfer, inside a procedure | `x = e`: $x$ is in the result if some operand of `e` is in the input; other variables keep their status; distributive |
| transfer, call edge | the parameter is in the result if its argument is in the input |
| transfer, return edge | the target of the call is in the result if `RET` is in the input |
| transfer, call-to-return edge | the caller's facts, minus the target of the call |
| height | $\lvert D \rvert$ per point |
| fixed point | the greatest, which is the least set of tainted variables |
| soundness | below the value of every valid path, so below every run |
| cost | $\mathrm{MFP}_{SG}$: $O(E \lvert D \rvert)$ set operations; MVP by [IFDS](/ifds-framework/): $O(E \lvert D \rvert^3)$ |

**Ways to get close to MVP.**

| approach | idea | equals MVP for |
|---|---|---|
| context-insensitive | $\mathrm{MFP}_{SG}$ on the supergraph | distributive problems on programs where each procedure has one call site |
| [inlining](/function-inlining/) | copy each callee into its caller | distributive problems without recursion |
| call strings | tag facts with the last $k$ call sites ([context sensitivity](/context-sensitivity/)) | large enough $k$, no recursion, distributive problems |
| [functional approach](/functional-approach-interprocedural/) | compute a summary function for each procedure and apply it at each call | distributive problems, with recursion |
| [IFDS](/ifds-framework/) | summaries as edges of a graph of single facts | finite distributive subset problems |
| [IDE](/ide-framework/) | IFDS with value functions on the edges | distributive environment problems |
| pushdown systems | the program as a [pushdown system](/pushdown-reachability/), facts as weights | distributive problems in a bounded idempotent semiring (Reps, Schwoon, Jha and Melski 2005) |

**Whole-program analysis.** An interprocedural analysis needs the code of the procedures it enters. A whole-program analysis assumes that it sees all of them, as a linker or a link-time optimizer does. For code it cannot see, such as a library, it needs a summary, written by hand or computed earlier, or it must assume the worst at the call. Separate compilation makes the same trade inside a compiler: [interprocedural constant propagation](/interprocedural-constant-propagation/) by Callahan, Cooper, Kennedy and Torczon (1986) uses jump functions, which are cheap summaries of how a procedure passes values on to its callees.

## Examples

Take the taint instance and the program below. `secret` is the input whose influence we track.

```text
id(a):         RET = a
main(secret):  s1: x = id(secret)
               s2: y = id(0)
               print(y)
```

| point | $\mathrm{MFP}_{SG}$ (tainted) | MVP (tainted) |
|---|---|---|
| $\mathit{entry}_{id}$ | {a} | {a}: the union of {a} from s1 and {} from s2 |
| $\mathit{exit}_{id}$ | {a, RET} | {a, RET} |
| $r_{s1}$ | {secret, x} | {secret, x} |
| $r_{s2}$ | {secret, x, y} | {secret, x} |

Both solutions agree inside `id`, where the facts of the two calls are merged anyway. They differ after the second call. The supergraph has the path $\mathit{entry}_{main} \to c_{s1} \xrightarrow{(_{s1}} \mathit{entry}_{id} \to \mathit{exit}_{id} \xrightarrow{)_{s2}} r_{s2}$. It enters `id` from `s1` and leaves to `s2`. Along it, `RET` is tainted, so `y` gets tainted, and `print(y)` looks like a leak. The brackets $(_{s1}\ )_{s2}$ do not match, so the path is not valid. On every valid path to $r_{s2}$, `id` was entered from `s2` with an untainted argument, so MVP finds that `y` is clean. The same leak of facts between callers makes context-insensitive constant propagation lose constants; the [context sensitivity](/context-sensitivity/) page shows that case and the limits of call strings.

**Locals across a call.** In the same program, `x` is tainted after `s1`. During the call at `s2`, `x` is a local of `main`, so `id` cannot change it. The call-to-return edge of `s2` carries `x` around the call, and the call edge does not pass it into `id`. Without this edge, an analysis would have to send every local of the caller through every callee.

## Where it is used

- **Security and bug finding.** Taint analysis and many checkers for null pointers and resource leaks run interprocedurally, often with the [IFDS framework](/ifds-framework/), since a source and its sink are rarely in the same procedure.
- **Compilers.** Interprocedural constant propagation, mod-ref analysis of side effects ([mod-ref analysis](/mod-ref-analysis/)) and inlining decisions use summaries of procedures. A link-time optimizer runs them on the whole program.
- **Pointer analysis.** Points-to sets cross procedures through parameters, returns and the heap. The call graph and the points-to sets often depend on each other and are computed together ([call graph construction](/call-graph-construction/)).
- **Slicing.** Interprocedural slicing on the [system dependence graph](/system-dependence-graph-slicing/) uses the same idea of matching calls and returns, with summary edges for the procedures.
- **Model checking.** Programs with recursion are [pushdown systems](/pushdown-reachability/), and interprocedural analyses can be phrased as reachability in them.

## References
