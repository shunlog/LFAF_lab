#!/usr/bin/env python3
from src.grammar import *
from src.automata import *

def test_regular_grammar():
    '''
    A -> aA
    A -> aB
    A -> ε
    B -> b
    '''
    VN = {"A", "B"}
    VT = {"a", "b"}
    S = "A"
    P = {("A"): {("a", "B"), ("a", "A"), ()},
         ("B"): {("b",)}}
    g = Grammar(VN, VT, P, S)

    assert g.type() == 3

def test_context_sensitive_grammar():
    VN = {"A", "B"}
    VT = {"a", "b"}
    S = "A"
    P = {("abAbC"): {("abAbC")}}
    g = Grammar(VN, VT, P, S)
    assert g.type() == 1

    P = {("abAbC"): {("abxxxbC")}}
    g = Grammar(VN, VT, P, S)
    assert g.type() == 1

    P = {("AbC"): {("xxxbC")}}
    g = Grammar(VN, VT, P, S)
    assert g.type() == 1

    P = {("bCA"): {("bCB")}}
    g = Grammar(VN, VT, P, S)
    assert g.type() == 1

def test_type0_grammar():
    VN = {"A", "B"}
    VT = {"a", "b"}
    S = "A"
    P = {("abbC"): {("abAbC")}}
    g = Grammar(VN, VT, P, S)
    assert g.type() == 0

    P = {("abAbC"): {("abbC")}}
    g = Grammar(VN, VT, P, S)
    assert g.type() == 0

def test_grammar_to_NFA():
    VN = {"A", "B"}
    VT = {"a", "b"}
    P = {("A"): {("a", "B"), ("a", "A"), ()},
        ("B"): {("b",)}}
    S = "A"
    g = Grammar(VN, VT, P, S)
    nfa = NFA.from_grammar(g)

    S = {'B', 'ε', 'A'}
    A = {'a', 'b'}
    s0 = 'A'
    d = {('A', 'a'): {'A', 'B'}, ('B', 'b'): {'ε'}}
    F = {'ε', 'A'}

    assert nfa.S == S
    assert nfa.A == A
    assert nfa.s0 == s0
    assert nfa.d == d
    assert nfa.F == F

def test_is_deterministic():
    VN = {"A", "B"}
    VT = {"a", "b"}
    P = {("A"): {("a", "B"), ("a", "A"), ()},
        ("B"): {("b",)}}
    S = "A"
    g = Grammar(VN, VT, P, S)
    nfa = NFA.from_grammar(g)
    assert not nfa.is_deterministic()

    P = {("A"): {("b", "B"), ("a", "A"), ()},
        ("B"): {("b",)}}
    g = Grammar(VN, VT, P, S)
    nfa = NFA.from_grammar(g)
    assert nfa.is_deterministic()

def test_NFA_to_DFA():
    VN = {"q0", "q1"}
    VT = {"a", "b"}
    P = {("q0"): {("a", "q1"), ("a", "q0"), ()},
        ("q1"): {("b",)}}
    S = "q0"
    g = Grammar(VN, VT, P, S)
    nfa = NFA.from_grammar(g)

    dfa = nfa.to_DFA()

    S = {frozenset({"q0"}), frozenset({"q0", "q1"}), frozenset({'ε'})}
    A = {'a', 'b'}
    s0 = {"q0"}
    d = {(frozenset({"q0"}), "a"): {"q0", "q1"},
         (frozenset({"q0", "q1"}), "a"): {"q0", "q1"},
         (frozenset({"q0", "q1"}), "b"): {"ε"}}
    F = {frozenset({"q0"}),
         frozenset({"q0", "q1"}),
         frozenset({'ε'})}

    assert dfa.S == S
    assert dfa.A == A
    assert dfa.s0 == s0
    assert dfa.d == d
    assert dfa.F == F
