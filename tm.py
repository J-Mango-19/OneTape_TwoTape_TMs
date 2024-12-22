from graphviz import Digraph

class OneTapeTuringMachine():
    def __init__(self, tape, transitions):
        self.tape = tape
        self.transitions = transitions
        self.head_position = 0
        self.state = 'q_1'

    def write_tape(self, symbol):
        self.tape[self.head_position] = symbol

    def read_tape(self):
        return self.tape[self.head_position]

    def move_head(self, direction):
        if direction.lower() == "r":
            if self.head_position + 1 < len(self.tape): # prevent head from going off end of tape
                self.head_position += 1

        elif direction.lower() == "l":
            if self.head_position > 0: # prevent from going off end of tape
                self.head_position -= 1

    def print_configuration(self):
        print(f'Configuration: {''.join(self.tape[: self.head_position])}{self.state}{''.join(self.tape[self.head_position :])}')

    def display(self):
        dot = Digraph()
        for node in self.transitions:
            dot.node(node)
            for tape_symbol, (next_state, new_symbol, direction) in self.transitions[node].items():
                dot.edge(node, next_state, label=f"{node} -> {new_symbol}, {direction}", labeldistance='5')

        dot.render('Turing Machine', format='png', cleanup=True)



"""
transitions = {
        cur_state : {
                     tape_symbol : (next_state, new_symbol, direction),
                      tape_symbol : (next_state, new_symbol, direction)
                      }}
"""

transitions = {
        'q_1' : {
            '0' : ('q_2', 'x', 'R'),
            '1' : ('q_1', '1', 'R'),
            'x' : ('q_1', 'x', 'R'),
            '$' : ('q_1', '$', 'R')
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
            '1' : ('q_5', '0', 'L'),
            'x' : ('q_5', 'x', 'L'),
            '$' : ('q_6', '$', 'R'),
        },
        'q_6' : {
            '0' : ('q_6', '0', 'R'),
            '1' : ('q_reject' 'q', 'L'),
            'x' : ('q_6', 'x', 'R'),
            '_' : ('q_accept', '_', 'L')
            }
        }

