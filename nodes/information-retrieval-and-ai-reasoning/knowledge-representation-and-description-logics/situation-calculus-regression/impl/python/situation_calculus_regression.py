# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/situation-calculus-regression/. The authors are listed in prov/A4NKPR.jsonl.
"""Regression for a ground, finite, propositional fragment of the situation calculus.

This module is not the first-order regression operator of Reiter. It covers
the case where every fluent is a ground atom with no situation-independent
arguments, there are finitely many ground actions, and no action senses
anything. In that case a situation is a truth assignment to the fluents,
and the successor state axiom of a fluent F for an action a reads

    F(do(a, s))  <->  gamma_plus(s)  or  (F(s) and not gamma_minus(s)),

where gamma_plus and gamma_minus are formulas over the fluents at s. The
precondition axiom of a is Poss(a, s) <-> pi_a(s). The general regression
theorem (Pirri and Reiter, JACM 46(3), 1999) is first order and needs the
foundational axioms and unique names axioms for actions; none of that
appears here.

Formulas are nodes of a hash-consed DAG (class Formulas). Node ids are
integers and equal formulas built twice get the same id, so a regression
step that replaces each fluent by its successor state formula shares every
common subformula. The size of the regressed DAG grows by at most the size
of the successor state formulas at each step.
"""

from __future__ import annotations

import itertools

FALSE, TRUE = 0, 1


class Formulas:
    """A hash-consed DAG of propositional formulas over named fluents."""

    def __init__(self) -> None:
        self.nodes: list[tuple] = [("const", False), ("const", True)]
        self.unique: dict[tuple, int] = {}

    def _make(self, key: tuple) -> int:
        u = self.unique.get(key)
        if u is None:
            u = len(self.nodes)
            self.nodes.append(key)
            self.unique[key] = u
        return u

    def fluent(self, name: str) -> int:
        return self._make(("fluent", name))

    def neg(self, a: int) -> int:
        if a in (FALSE, TRUE):
            return TRUE - a
        key = self.nodes[a]
        if key[0] == "not":
            return key[1]
        return self._make(("not", a))

    def conj(self, a: int, b: int) -> int:
        if a == FALSE or b == FALSE:
            return FALSE
        if a == TRUE:
            return b
        if b == TRUE or a == b:
            return a
        return self._make(("and", min(a, b), max(a, b)))

    def disj(self, a: int, b: int) -> int:
        if a == TRUE or b == TRUE:
            return TRUE
        if a == FALSE:
            return b
        if b == FALSE or a == b:
            return a
        return self._make(("or", min(a, b), max(a, b)))

    def evaluate(self, root: int, state: dict[str, bool]) -> bool:
        memo: dict[int, bool] = {}

        def ev(u: int) -> bool:
            if u in memo:
                return memo[u]
            key = self.nodes[u]
            if key[0] == "const":
                r = key[1]
            elif key[0] == "fluent":
                r = state[key[1]]
            elif key[0] == "not":
                r = not ev(key[1])
            elif key[0] == "and":
                r = ev(key[1]) and ev(key[2])
            else:
                r = ev(key[1]) or ev(key[2])
            memo[u] = r
            return r

        return ev(root)

    def dag_size(self, root: int) -> int:
        """The number of distinct nodes below the root."""
        seen = set()
        stack = [root]
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            key = self.nodes[u]
            if key[0] in ("not", "and", "or"):
                stack.extend(key[1:])
        return len(seen)

    def tree_size(self, root: int) -> int:
        """The number of nodes of the formula written out as a tree, with no sharing."""
        memo: dict[int, int] = {}

        def ts(u: int) -> int:
            if u in memo:
                return memo[u]
            key = self.nodes[u]
            r = 1 + sum(ts(c) for c in key[1:]) if key[0] in ("not", "and", "or") else 1
            memo[u] = r
            return r

        return ts(root)

    def show(self, root: int) -> str:
        key = self.nodes[root]
        if key[0] == "const":
            return "true" if key[1] else "false"
        if key[0] == "fluent":
            return key[1]
        if key[0] == "not":
            return "not " + self.show(key[1])
        return "(" + self.show(key[1]) + " " + key[0] + " " + self.show(key[2]) + ")"


class Action:
    """A ground action: a precondition and, per fluent, the formulas gamma_plus and gamma_minus."""

    def __init__(self, name: str, poss: int, plus: dict[str, int], minus: dict[str, int]) -> None:
        self.name = name
        self.poss = poss
        self.plus = plus
        self.minus = minus


class BasicActionTheory:
    """Fluents, actions with successor state axioms, and an initial database D_S0.

    D_S0 is a list of formulas over the fluents. It may leave some fluents
    unknown, so the initial situation can have many models.
    """

    def __init__(self, f: Formulas, fluents: list[str], actions: dict[str, Action], initial: list[int]) -> None:
        self.f = f
        self.fluents = fluents
        self.actions = actions
        self.initial = initial
        # Phi[a][F] is the right side of the successor state axiom of F for a.
        self.phi: dict[str, dict[str, int]] = {}
        for a in actions.values():
            row = {}
            for name in fluents:
                gp = a.plus.get(name, FALSE)
                gm = a.minus.get(name, FALSE)
                row[name] = f.disj(gp, f.conj(f.fluent(name), f.neg(gm)))
            self.phi[a.name] = row

    # ------------------------------------------------------------ regression

    def regress_step(self, phi: int, action: str) -> int:
        """R_a(phi): replace each fluent F of phi by Phi_{F,a}; the result is about the earlier situation."""
        f = self.f
        row = self.phi[action]
        memo: dict[int, int] = {}  # @line L2

        def r(u: int) -> int:
            if u in memo:  # @line L5
                return memo[u]
            key = f.nodes[u]
            if key[0] == "const":  # @line L6
                out = u
            elif key[0] == "fluent":  # @line L7
                out = row[key[1]]
            elif key[0] == "not":  # @line L8
                out = f.neg(r(key[1]))
            else:  # @line L9
                make = f.conj if key[0] == "and" else f.disj
                out = make(r(key[1]), r(key[2]))
            memo[u] = out  # @line L10
            return out

        return r(phi)

    def regress(self, phi: int, actions: list[str]) -> int:
        """R[phi(do([a1, ..., an], S0))]: a formula about S0 with the same truth value."""
        for a in reversed(actions):  # @line L1
            phi = self.regress_step(phi, a)  # @line L3
        return phi  # @line L4

    def executable_formula(self, actions: list[str]) -> int:
        """The regression of: each a_i is possible in the situation reached by a_1 to a_{i-1}.

        One backward pass: chi_n = true and chi_{i-1} = pi_{a_i} and R_{a_i}(chi_i), so chi_0
        is the conjunction of each precondition regressed through the actions before it.
        """
        f = self.f
        chi = TRUE  # @line L11
        for a in reversed(actions):  # @line L12
            chi = f.conj(self.actions[a].poss, self.regress_step(chi, a))  # @line L13
        return chi  # @line L14

    def entails_initially(self, phi: int) -> bool:
        """Does D_S0 entail phi? Brute force over the assignments to the fluents."""
        for state in self.initial_models():
            if not self.f.evaluate(phi, state):
                return False
        return True

    def initial_models(self):
        for bits in itertools.product([False, True], repeat=len(self.fluents)):
            state = dict(zip(self.fluents, bits))
            if all(self.f.evaluate(g, state) for g in self.initial):
                yield state

    def project_by_regression(self, phi: int, actions: list[str]) -> bool:
        """Is phi true in do(actions, S0) in every model of the theory?"""
        return self.entails_initially(self.regress(phi, actions))  # @line L15

    def executable_by_regression(self, actions: list[str]) -> bool:
        return self.entails_initially(self.executable_formula(actions))

    # ------------------------------------------------- progression (reference)

    def step(self, state: dict[str, bool], action: str) -> dict[str, bool]:
        """The successor state, by evaluating each successor state axiom at the current state."""
        row = self.phi[action]
        return {name: self.f.evaluate(row[name], state) for name in self.fluents}

    def project_by_simulation(self, phi: int, actions: list[str]) -> bool:
        for state in self.initial_models():
            for a in actions:
                state = self.step(state, a)
            if not self.f.evaluate(phi, state):
                return False
        return True

    def executable_by_simulation(self, actions: list[str]) -> bool:
        for state in self.initial_models():
            for a in actions:
                if not self.f.evaluate(self.actions[a].poss, state):
                    return False
                state = self.step(state, a)
        return True


def yale_shooting(initial_alive_only: bool = True) -> tuple[BasicActionTheory, Formulas]:
    """The Yale shooting domain: fluents loaded and alive; actions load, wait and shoot."""
    f = Formulas()
    loaded, alive = f.fluent("loaded"), f.fluent("alive")
    actions = {
        "load": Action("load", f.neg(loaded), {"loaded": TRUE}, {}),
        "wait": Action("wait", TRUE, {}, {}),
        "shoot": Action("shoot", TRUE, {}, {"alive": loaded, "loaded": TRUE}),
    }
    initial = [alive] if initial_alive_only else [alive, f.neg(loaded)]
    return BasicActionTheory(f, ["loaded", "alive"], actions, initial), f
