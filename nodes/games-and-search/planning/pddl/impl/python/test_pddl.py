# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pddl/. The authors are listed in prov/DM6GS3.jsonl.

import pytest

from pddl import bfs_plan, ground, is_plan, objects_by_type, parse_sexpr, read_domain, read_problem, reachable

BLOCKS = """
; the four operator blocks world, in the style of the 2000 competition
(define (domain blocksworld)
  (:requirements :strips)
  (:predicates (clear ?x) (ontable ?x) (handempty) (holding ?x) (on ?x ?y))
  (:action pick-up
    :parameters (?x)
    :precondition (and (clear ?x) (ontable ?x) (handempty))
    :effect (and (holding ?x) (not (clear ?x)) (not (ontable ?x)) (not (handempty))))
  (:action put-down
    :parameters (?x)
    :precondition (holding ?x)
    :effect (and (clear ?x) (handempty) (ontable ?x) (not (holding ?x))))
  (:action stack
    :parameters (?x ?y)
    :precondition (and (holding ?x) (clear ?y))
    :effect (and (not (holding ?x)) (not (clear ?y)) (clear ?x) (handempty) (on ?x ?y)))
  (:action unstack
    :parameters (?x ?y)
    :precondition (and (on ?x ?y) (clear ?x) (handempty))
    :effect (and (holding ?x) (clear ?y) (not (clear ?x)) (not (handempty)) (not (on ?x ?y)))))
"""

SUSSMAN = """
(define (problem sussman)
  (:domain blocksworld)
  (:objects A B C)
  (:init (clear c) (on c a) (ontable a) (clear b) (ontable b) (handempty))
  (:goal (and (on a b) (on b c))))
"""

LOGISTICS = """
(define (domain tiny-logistics)
  (:requirements :strips :typing)
  (:types truck package - locatable location)
  (:predicates (at ?x - locatable ?l - location) (in ?p - package ?t - truck) (road ?a ?b - location))
  (:action drive :parameters (?t - truck ?from ?to - location)
    :precondition (and (at ?t ?from) (road ?from ?to))
    :effect (and (at ?t ?to) (not (at ?t ?from))))
  (:action load :parameters (?p - package ?t - truck ?l - location)
    :precondition (and (at ?p ?l) (at ?t ?l))
    :effect (and (in ?p ?t) (not (at ?p ?l))))
  (:action unload :parameters (?p - package ?t - truck ?l - location)
    :precondition (and (in ?p ?t) (at ?t ?l))
    :effect (and (at ?p ?l) (not (in ?p ?t)))))
"""

DELIVERY = """
(define (problem deliver)
  (:domain tiny-logistics)
  (:objects t1 - truck p1 p2 - package l1 l2 - location)
  (:init (road l1 l2) (road l2 l1) (at t1 l1) (at p1 l1) (at p2 l2))
  (:goal (and (at p1 l2) (at p2 l1))))
"""


def test_parse_sexpr():
    assert parse_sexpr("(a (B c) ; comment\n d)") == ["a", ["b", "c"], "d"]
    with pytest.raises(ValueError):
        parse_sexpr("(a (b)")
    with pytest.raises(ValueError):
        parse_sexpr("(a)) (")


def test_blocks_world_from_text():
    dom, prob = read_domain(BLOCKS), read_problem(SUSSMAN)
    acts = ground(dom, prob)
    assert len(acts) == 3 + 3 + 9 + 9  # stack(a, a) and unstack(a, a) are grounded too
    plan = bfs_plan(prob.init, prob.goal, acts)
    assert [a.name for a in plan] == ["(unstack c a)", "(put-down c)", "(pick-up b)", "(stack b c)", "(pick-up a)", "(stack a b)"]
    assert is_plan(prob.init, prob.goal, plan)
    assert len(reachable(prob.init, acts)) == 22


def test_equality_removes_self_stacking():
    text = BLOCKS.replace("(:requirements :strips)", "(:requirements :strips :equality)")
    text = text.replace(":precondition (and (holding ?x) (clear ?y))", ":precondition (and (holding ?x) (clear ?y) (not (= ?x ?y)))")
    text = text.replace(":precondition (and (on ?x ?y) (clear ?x) (handempty))", ":precondition (and (on ?x ?y) (clear ?x) (handempty) (not (= ?x ?y)))")
    acts = ground(read_domain(text), read_problem(SUSSMAN))
    assert len(acts) == 3 + 3 + 6 + 6


def test_types_and_hierarchy():
    dom, prob = read_domain(LOGISTICS), read_problem(DELIVERY)
    objs = objects_by_type(dom, prob)
    assert objs["locatable"] == ["t1", "p1", "p2"]
    assert objs["object"] == ["t1", "p1", "p2", "l1", "l2"]
    acts = ground(dom, prob)
    assert len(acts) == 1 * 2 * 2 + 2 * (2 * 1 * 2)
    plan = bfs_plan(prob.init, prob.goal, acts)
    # load p1, drive to l2, unload p1, load p2, drive back, unload p2
    assert len(plan) == 6


def test_unsupported_features_are_rejected():
    with pytest.raises(ValueError):
        read_domain(BLOCKS.replace("(:requirements :strips)", "(:requirements :strips :conditional-effects)"))
    when = BLOCKS.replace(":effect (and (clear ?x) (handempty) (ontable ?x) (not (holding ?x))))", ":effect (and (when (clear ?x) (handempty)) (not (holding ?x))))")
    with pytest.raises(ValueError):
        read_domain(when)
