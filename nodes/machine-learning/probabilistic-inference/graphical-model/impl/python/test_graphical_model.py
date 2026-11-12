# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/graphical-model/. The authors are listed in prov/QJW75C.jsonl.

from fractions import Fraction as F

from graphical_model import (
    all_dags,
    all_undirected_graphs,
    dag_independences,
    independences,
    joint_from_factors,
    undirected_independences,
)

A, B, C, D = 0, 1, 2, 3


def v_structure():
    # A -> C <- B with independent causes and a noisy effect
    pa = lambda a: F(3, 10) if a else F(7, 10)
    pb = lambda b: F(2, 5) if b else F(3, 5)
    on = {(0, 0): F(1, 10), (1, 0): F(6, 10), (0, 1): F(7, 10), (1, 1): F(9, 10)}
    pc = lambda a, b, c: on[(a, b)] if c else 1 - on[(a, b)]
    return joint_from_factors(3, [((A,), pa), ((B,), pb), ((A, B, C), pc)])


def four_cycle():
    # pairwise potentials on A - B - C - D - A, all different
    tables = [((A, B), (5, 1, 2, 3)), ((B, C), (4, 1, 1, 6)), ((C, D), (2, 7, 1, 3)), ((D, A), (3, 2, 5, 1))]
    factors = [(scope, lambda x, y, t=t: F(t[2 * x + y])) for scope, t in tables]
    return joint_from_factors(4, factors)


def test_counts_of_graphs() -> None:
    assert len(all_undirected_graphs(3)) == 8
    assert len(all_dags(3)) == 25
    assert len(all_dags(4)) == 543


def test_v_structure_has_no_undirected_perfect_map() -> None:
    p = v_structure()
    assert sum(p.values()) == 1
    ci = independences(p, 3)
    assert ci == {(A, B, frozenset())}  # A _||_ B, but not given C
    dag = {A: set(), B: set(), C: {A, B}}
    assert dag_independences(dag, 3) == ci
    assert all(undirected_independences(g, 3) != ci for g in all_undirected_graphs(3))
    # the moral graph is complete, so the best undirected I-map loses A _||_ B
    full = {A: {B, C}, B: {A, C}, C: {A, B}}
    assert undirected_independences(full, 3) == set()


def test_four_cycle_has_no_directed_perfect_map() -> None:
    p = four_cycle()
    ci = independences(p, 4)
    assert ci == {(A, C, frozenset({B, D})), (B, D, frozenset({A, C}))}
    cycle = {A: {B, D}, B: {A, C}, C: {B, D}, D: {A, C}}
    assert undirected_independences(cycle, 4) == ci
    assert all(dag_independences(g, 4) != ci for g in all_dags(4))
    # some DAG is an I-map (implies only true statements), but every such DAG misses one
    imaps = [g for g in all_dags(4) if dag_independences(g, 4) <= ci]
    assert imaps and all(len(dag_independences(g, 4)) <= 1 for g in imaps)
