import json
import sys
from tm import OneTapeTuringMachine, TwoTapeTuringMachine
from transitions import transitions_identical01s, transitions_identical_strings_twoTapeTM
import numpy as np
import matplotlib.pyplot as plt

"""
run deciders for equality on increasingly long strings
for each string, record the time for each of (one_tape_tm, two_tape_tm)
"""

test_strings = [
        ("1", "1"),
        ("10", "10"),
        ("101", "101"),
        ("1010", "1010"),
        ("10101","10101"),
        ("110110", "110110"),
        ("1101101", "1101101"),
        ("11001101", "11001101"),
        ("111110000", "111110000"),
        ("0011111110", "0011111110"),
        ("00111111101", "00111111101"),
        ("001111111010", "001111111010"),
        ]

def run_one_tape(test_string, test_str_idx):
    transitions = transitions_identical01s
    TM = OneTapeTuringMachine(test_string, transitions)

    # run the Turing Machine
    num_transitions = 0
    while (TM.state not in ('q_accept', 'q_reject')):
        current_symbol = TM.read_tape()
        if TM.state in TM.transitions and current_symbol in TM.transitions[TM.state]:
            (next_state, new_tape_symbol, direction) = TM.transitions[TM.state][current_symbol]
            TM.write_tape(new_tape_symbol)
            TM.state = next_state
            TM.move_head(direction)

        else: # all undefined transitions go to q_reject
            TM.state = 'q_reject'

        num_transitions += 1

    print(f"Finished test {test_str_idx}. Final state: {TM.state}. Steps = {num_transitions}")
    return num_transitions

def run_two_tape(input_string1, input_string2, test_str_idx):
    transitions = transitions_identical_strings_twoTapeTM

    TM = TwoTapeTuringMachine(input_string1, input_string2, transitions)

    # run the turing machine
    num_transitions = 0
    while TM.state not in ('q_accept', 'q_reject'):
        num_transitions += 1
        TM.step()

    print(f"Finished test {test_str_idx}. Final state: {TM.state}. Steps = {num_transitions}")
    return num_transitions


steps_OneTape = []
steps_TwoTape = []
for i, (test_string1, test_string2) in enumerate(test_strings):

    # preprocessing for the one tape machine's string
    test_string_oneTape = ['$'] + list('#'.join([test_string1, test_string2])) + ['_']
    print(test_string_oneTape)

    # preprocessing for the two tape machine's strings
    test_string1 = list(test_string1) + ['_']
    test_string2 = list(test_string2) + ['_']

    # run and record the steps for the one-tape machine
    steps_OneTape.append(run_one_tape(test_string_oneTape, i))
    steps_TwoTape.append(run_two_tape(test_string1, test_string2, i))


x_axis = [len(ts1) for ts1, ts2 in test_strings]
plt.scatter(x_axis, steps_OneTape, label="One-Tape Turing Machine")
plt.scatter(x_axis, steps_TwoTape, label="Two-Tape Turing Machine")
plt.legend()
plt.xlabel("Length of input string")
plt.ylabel("Steps of computation to decide")
plt.title("OneTapeTM vs TwoTapeTM time complexity")
plt.savefig("oneTape_vs_twoTape_timeComplexity")
