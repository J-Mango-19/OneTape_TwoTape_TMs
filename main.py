import json
import sys
from tm import OneTapeTuringMachine, TwoTapeTuringMachine
from transitions import transitions_equal01s, transitions_identical01s, transitions_identical_strings_twoTapeTM

def run_two_tape(algorithm):
    print(f"Running Two-Tape TM. {algorithm=}")
    print("Example inputs: string1: 010101  string2: 010101  return q_accept")
    input_string1 = list(input("Enter input_string1: (use only characters in {0, 1, _}: ")) + ['_']
    input_string2 = list(input("Enter input_string2: (use only characters in {0, 1, _}: ")) + ['_']

    transitions = transitions_identical_strings_twoTapeTM

    # construct (possibly display) the turing machine 
    TM = TwoTapeTuringMachine(input_string1, input_string2, transitions)
    res = input("Save a png image of the TM state diagram in this directory? Requires graphviz library. [Y/n]: ")
    if res.lower() == 'y':
        print("saving png image")
        TM.display("TwoTape_IdenticalStrings_StateDiagram")

    # run the turing machine
    num_transitions = 0
    print(f"{num_transitions=}")
    TM.print_configuration()
    while TM.state not in ('q_accept', 'q_reject'):
        num_transitions += 1
        print(f"{num_transitions=}")
        TM.step()
        TM.print_configuration()
        print("------------")

    print(f"Done. Final state: {TM.state}")

def run_one_tape(algorithm):
    print(f"Running one-tape TM. {algorithm=}")

    # get input strings and transitions based on algorithm
    if algorithm == 'test_identical':
        print("Example input: 1000001#1000001 returns q_accept")
        input_string = input("Enter input string in the format string1#string2 use only chars in {0, 1, #}: ")
        transitions = transitions_identical01s

    elif algorithm == 'test_equal_amount':
        print("Example input: 010100011101 returns q_accept")
        input_string = input("Enter input string using only chars in {0, 1}")
        transitions = transitions_equal01s
    else:
        print("invalid algorithm selected. Options are:")
        print("test_identical: tests if two strings comprised of 0s and 1s are identical")
        print("test_equal_amount: tests if a string has the same amount of 0s as 1s")
        sys.exit(1)

    # process input string by prepending '$' and appending '_' (blank symbol)
    input_string = ['$'] + list(input_string) + ['_']

    # construct (maybe display) the turing machine
    TM = OneTapeTuringMachine(input_string, transitions)
    res = input("Save a png image of the TM state diagram in this directory? Requires graphviz library. [Y/n]: ")
    if res.lower() == 'y':
        print("saving png image")
        if algorithm == 'test_identical':
            TM.display("OneTape_IdenticalStrings_StateDiagram")
        elif algorithm == 'test_equal_amount':
            TM.display("OneTape_EqualTypeStrings_StateDiagram")

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
        print(f'Transition number: {num_transitions}')
        TM.print_configuration()
        print('----------------------------------------')

    print(f"Done. Final state: {TM.state}")


machine_type = input("Which type of machine would you like to run? Options: (one_tape, two_tape): ").lower()
if machine_type not in ('one_tape', 'two_tape'):
    print("invalid machine type")
    sys.exit(1)

if machine_type == 'one_tape':
    algorithm = input("Which algorithm? Options: (test_identical, test_equal_amount): ")
    run_one_tape(algorithm)

elif machine_type == 'two_tape':
    algorithm = 'test_identical'
    run_two_tape(algorithm)
