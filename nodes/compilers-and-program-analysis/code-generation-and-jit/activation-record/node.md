---
tag: 4XG2M7
kind: data-structure
slug: activation-record
name: Activation record
aliases:
- stack frame
- call frame
area: compilers-and-program-analysis/code-generation-and-jit
level: intro
summary: The block of stack memory for one call of a procedure, with its arguments, return address, saved registers and local variables.
model: word-ram
complexity:
  vars: {h: the difference between the nesting depth of a use and that of its declaration, s: the number of parameters and locals of the callee}
  time: {worst: O(h + s)}
  space: {extra: Θ(s)}
prereqs: [stack, recursion]
see_also: [tail-call-optimization, closure-conversion, lambda-lifting, continuation-passing-style, stack-allocation, escape-analysis, gc-roots, region-based-memory-management]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Chapter 7 (Run-Time Environments), activation records, calling sequences, access links and displays
  - book: isbn:9780521820608
    title: Andrew W. Appel, Modern Compiler Implementation in ML, Cambridge University Press, 1998
    locator: Chapter 6 (Activation Records), stack frames, frame pointers, static links and escaping variables
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 6 (The Procedure Abstraction), activation records, access links and global displays
  - paper: "E. W. Dijkstra, Recursive programming, Numerische Mathematik 2, 1960, 312-318"
    locator: the run-time stack for the recursive procedures of ALGOL 60
---

An activation record, or stack frame, is the block of memory that holds the state of one call of a procedure: its arguments, its local variables, the address to return to, and links to other frames. A call pushes a new record on the run-time [stack](/stack/), and the return pops it. So the records of the active calls form a stack, which is what makes [recursion](/recursion/) work. In a language with nested procedures, each record also has a *static link* to the record of the enclosing procedure, and the code reaches a variable of an outer procedure by following these links.

## In plain words

Each time a function is called, it needs its own place to keep its arguments and its local variables. If a function calls itself, each call needs a separate place, or the calls would overwrite each other.

So the program keeps a stack. A call puts a new block, the frame, on top. The frame holds the arguments, the locals, and the place in the caller where the program continues after the return. When the call ends, its frame is taken off, and the caller's frame is on top again.

Some languages let you write a function inside another function. The inner function can use the variables of the outer one. To find them, each frame keeps a pointer to the frame of the function that it is written inside. This pointer is not always the caller. Mixing up the two gives wrong values.

## The abstract type

The run-time stack is a stack of frames, with these operations:

- **call** $f$ with arguments $a_1, \ldots, a_n$: push a frame for $f$ that holds the arguments, fresh locals, the return address, and the links;
- **return** $v$: pop the top frame and continue in the caller with the value $v$;
- **load** and **store** of a variable $x$: read or write the slot of $x$ in the frame where $x$ lives.

The last operation is the hard one. A function $g$ at nesting depth $d$ can use a variable that is declared in an enclosing function at depth $j \le d$. The compiler knows $d$ and $j$, so it names each variable by a pair $(h, o)$: go $h = d - j$ frames out along the lexical nesting, then take offset $o$. The data structure must find the frame that is $h$ levels out quickly. That frame is the one of the *most recent active call* of the enclosing function that $g$ was created in, and with recursion this can be far down the stack.

## Representation

The frame is a contiguous block, and a frame pointer FP holds the address of the current one. In the reference code, a frame on the toy stack machine has this layout:

| Offset from FP | Slot |
|---|---|
| 0 | return address RA |
| 1 | dynamic link DL: the FP of the caller |
| 2 | static link SL: the FP of the frame of the enclosing function |
| 3, 4, ... | the parameters, then the locals |
| above | temporaries of the expression in progress |

The dynamic link restores the FP of the caller on return. The static link, also called the access link, points to the frame of the function that lexically encloses the callee. Real machines add slots for saved registers and outgoing arguments, and they keep the first arguments in registers. The layout above shows only the parts that the access to variables needs.

## Operations

The caller runs MARK, pushes the arguments, and runs CALL. The callee begins with ENTER. CALL has three operands: the address of the callee, the number $h$ of static links to follow, and the number $n$ of arguments.

```pseudo id=main
CALL(target, h, n)
L1  MARK: push three empty header slots, then push the n arguments
L2  base ← SP - n - 3
L3  stack[base + RA], stack[base + DL], stack[base + SL] ← pc, FP, FRAME(h); FP ← base; pc ← target
L4  ENTER: push the locals of the callee, each set to 0

RETURN
L5  v ← pop; ra ← stack[FP + RA]; dl ← stack[FP + DL]
L6  pop the frame; push v; pc ← ra; FP ← dl

FRAME(h)
L7  a ← FP; repeat h times: a ← stack[a + SL]

LOAD(h, o)
L8  push stack[FRAME(h) + o]
```

STORE is LOAD with a write. The static link of the callee comes from line L3. If $f$ is declared in the function that is $h$ hops out from the caller, then the frame of that function is FRAME($h$) of the caller, and this is the frame that $f$ must see as its parent. For a function declared in the caller itself, $h = 0$ and the static link is the FP of the caller.

A *display* replaces the chain by an array $D$, where $D[j]$ is the frame of the current function at depth $j$ of the lexical chain. A use at depth $j$ reads $D[j]$, in one step. ENTER of a function at depth $j$ saves $D[j]$ in the frame and sets $D[j]$ to the new frame, and RETURN puts the saved value back.

## Example

Take this program, where $f$ and $g$ are declared inside main:

```
main() { var x; x = 1; g() }
  f() { x }
  g() { var y; y = 2; f() }
```

The compiler emits this code. The first three instructions are the startup code, which calls main.

```
 0 MARK            7 MARK           14 PUSH 2
 1 CALL 3 0 0      8 CALL 13 0 0    15 STORE 0 3
 2 HALT            9 RET 0          16 POP
 3 ENTER 1 0      10 ENTER 0 1      17 MARK
 4 PUSH 1         11 LOAD 1 3       18 CALL 10 1 0
 5 STORE 0 3      12 RET 1          19 RET 1
 6 POP            13 ENTER 1 1
```

Instruction 11 is the use of $x$ in $f$: $f$ has depth 1 and $x$ belongs to main at depth 0, so it follows 1 static link and reads offset 3. Instruction 18 is the call of $f$ from $g$: $f$ is declared in main, which is 1 hop out from $g$, so the static link of $f$ is the static link of $g$. When instruction 11 runs, the stack is:

| Address | Value | Meaning |
|---|---|---|
| 0, 1, 2 | 0, 0, 0 | the frame of the startup code |
| 3, 4, 5 | 2, 0, 0 | main: RA, DL, SL |
| 6 | 1 | main: $x$ |
| 7, 8, 9 | 9, 3, 3 | $g$: RA, DL, SL |
| 10 | 2 | $g$: $y$ |
| 11, 12, 13 | 19, 7, 3 | $f$: RA, DL, SL |

With FP = 11, one static link gives the frame at 3, and the slot $3 + 3 = 6$ holds $x = 1$, which is right. If the code followed the dynamic link instead, it would reach the frame of $g$ at 7 and read $y = 2$ from slot 10. That is the answer of dynamic scope, not of lexical scope. The display version emits LOADD 0 3 at instruction 11, with the same result.

A second test computes $6! = 720$ with a recursive fact$(n)$ that declares an inner times$(k) = k \cdot n$. Each call of times must see the $n$ of the call of fact that created it, not of a deeper one. The static link gives exactly that.

## Correctness

The proof file shows that the machine simulates a direct evaluator with environments. Each environment record maps to one frame, the slots of the frame hold the values of the record, and the static link of a frame points to the frame of the parent record. By induction on $h$, FRAME($h$) reaches the record of the function that is $h$ levels out in the lexical chain, which is where the compiler resolved the name. The call keeps the invariant, because line L3 computes the static link with the same rule that the evaluator uses to find the parent. The return keeps it, because it reads RA and DL before it pops the frame. A second theorem shows that the display holds the same frames as the chain. The tests compare the machine, with static links and with a display, against the evaluator on 1,500 random programs with nesting up to depth 3. They also check that following the dynamic links gives a different result on many of them.

## Complexity

A call costs $O(h + s)$: $O(h)$ to follow the static links at line L3, and $O(s)$ to push the header, the arguments and the locals. A return costs $O(1)$ beyond the pop of the frame. A variable access costs $O(h)$ with static links and $O(1)$ with a display. In real programs $h$ is almost always 0 or 1, so the chain is cheap. A frame takes $\Theta(s)$ words, and the stack holds one frame for each active call, so its size is the depth of the recursion times the size of the largest frame.

## Variants

- **Display.** As above, with $O(1)$ access to every level. It costs a save and a restore on each call, and it is harder to make right with procedures passed as values, which must carry their own display or static link.
- **No static link.** In C, functions are not nested, so a frame has only the dynamic link, and many compilers omit even that and address the frame from the stack pointer.
- **[Lambda lifting](/lambda-lifting/).** The compiler passes the free variables of an inner function as extra parameters, and the static link is no longer needed.
- **[Closure conversion](/closure-conversion/) and heap frames.** When an inner function can outlive the call that created it, its free variables cannot stay in a frame on the stack. They move to a heap record, and the closure holds a pointer to it. [Escape analysis](/escape-analysis/) finds which frames can stay on the [stack](/stack-allocation/).
- **[Tail calls](/tail-call-optimization/).** A call in tail position reuses the frame of the caller, so a loop written as recursion runs in constant stack space.
- **Register windows.** Some machines, such as SPARC, give each call a fresh set of registers that overlap with those of the caller, so small frames need no memory at all.

## When to use it

Every compiler for a language with recursion uses activation records on a stack. Static links are the usual choice for nested functions, because the nesting is shallow and the cost of a call stays small. A display pays off when the code often reads variables several levels out. When functions are first-class values that can escape, the frames, or at least the escaping variables, must live on the heap, or in [regions](/region-based-memory-management/) whose lifetime the compiler can prove. A garbage collector must find the pointers in the frames, because the slots of the active frames are part of its [roots](/gc-roots/). So the compiler records, for each call site, which slots of the frame hold pointers.

## Pitfalls

- **Dynamic link for static link.** Following the caller instead of the enclosing function gives dynamic scope. The two links agree only when the caller is the enclosing function, so simple tests may not catch the error.
- **Returning the address of a local.** The frame is gone after the return, and a later call writes over it.
- **Escaping closures.** An inner function that is returned or stored keeps a static link to a frame that has been popped. This is the upward funarg problem. Such variables must go to the heap.
- **Popping too early.** The return must read the return address and the dynamic link before it frees the frame, or it reads slots that are no longer there.
- **Hops counted from the wrong frame.** The number of hops for a call is the distance from the caller to the function that declares the callee, not to the callee.

## Implementations

## History

Dijkstra described in 1960 how a run-time stack handles the recursive procedures of ALGOL 60, with a record for each call. The ALGOL 60 compilers of the early 1960s used static and dynamic chains, and some used a display, for access to the variables of enclosing blocks. Later textbooks, such as the dragon book and Appel's book, made the frame layout with access links the standard way to teach run-time environments.

## References
