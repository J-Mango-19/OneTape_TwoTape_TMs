from tm import OneTapeTuringMachine

transitions = {
        'q_1' : {
            '0' : ('q_2', 'x', 'R'),
            '1' : ('q_1', '1', 'R'),
            'x' : ('q_1', 'x', 'R'),
            '$' : ('q_1', '$', 'R'),
            '_' : ('q_5', '_', 'L')
                   },
        'q_2' : {
            '0' : ('q_2', '0', 'L'),
            '1' : ('q_2', '1', 'L'),
            'x' : ('q_2', 'x', 'L'),
            '$' : ('q_3', '$', 'R')
            },
        'q_3' : {
            '0' : ('q_3', '0', 'R'),
            '1' : ('q_4', 'x', 'L'),
            'x' : ('q_3', 'x', 'R'),
            },
        'q_4' : {
            '0' : ('q_4', '0', 'L'),
            '1' : ('q_4', '1', 'L'),
            'x' : ('q_4', 'x', 'L'),
            '$' : ('q_1', '$', 'R')
            },
        'q_5' : {
            '0' : ('q_5', '0', 'L'),
            '1' : ('q_5', '1', 'L'),
            'x' : ('q_5', 'x', 'L'),
            '$' : ('q_6', '$', 'R'),
        },
        'q_6' : {
            '0' : ('q_6', '0', 'R'),
            '1' : ('q_reject', '1', 'R'),
            'x' : ('q_6', 'x', 'R'),
            '_' : ('q_accept', '_', 'R')
            }
        }

input_string = "010100011101"
# process input string by prepending '$' and appending '_' (blank symbol)
TM = OneTapeTuringMachine(['$'] + list(input_string) + ['_'], transitions)
TM.display()

num_transitions = 0
while(TM.state != 'q_accept' and TM.state != 'q_reject'):
    current_symbol = TM.read_tape()
    if TM.state in TM.transitions and current_symbol in TM.transitions[TM.state]:
        (next_state, new_tape_symbol, direction) = TM.transitions[TM.state][current_symbol]
        TM.write_tape(new_tape_symbol)
        TM.state = next_state
        TM.move_head(direction)

    else: # all undefined transitions go to qreject
        TM.state = 'q_reject'

    num_transitions += 1
    print(f'Transition number: {num_transitions}')
    TM.print_configuration()
    print('----------------------------------------')
