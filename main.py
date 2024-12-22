import json
import sys
from tm import OneTapeTuringMachine
from transitions import transitions_equal01s, transitions_identical01s

machine_type = 'test_identical'

if machine_type == 'test_identical':
    input_string = '1000001#1000001'
    transitions = transitions_identical01s

elif machine_type == 'test_equal_amount':
    input_string = '010100011101'
    transitions = transitions_equal01s
else:
    print("invalid machine type selected. Options are:")
    print("test_identical: tests if two strings comprised of 0s and 1s are identical")
    print("test_equal_amount: tests if a string has the same amount of 0s as 1s")
    sys.exit(1)

# process input string by prepending '$' and appending '_' (blank symbol)
input_string = ['$'] + list(input_string) + ['_'] 

# construct the turing machine
TM = OneTapeTuringMachine(input_string, transitions)
TM.display()


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
        print(TM.state in TM.transitions)
        print(current_symbol in TM.transitions[TM.state])
        TM.state = 'q_reject'

    num_transitions += 1
    print(f'Transition number: {num_transitions}')
    TM.print_configuration()
    print('----------------------------------------')
