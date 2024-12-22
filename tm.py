from graphviz import Digraph
from collections import defaultdict

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
        print(f'Configuration: {''.join(self.tape[: self.head_position])} {self.state} {''.join(self.tape[self.head_position :])}')

    def display(self):
        dot = Digraph()
        for node in self.transitions:
            dot.node(node)

            # Group transitions that connect to the same nodes
            next_state_description_dict = defaultdict(list)
            for tape_symbol, (next_state, new_symbol, direction) in self.transitions[node].items():
                next_state_description_dict[next_state].append(f"{tape_symbol} -> {new_symbol}, {direction}")

            for next_state, description in next_state_description_dict.items():
                dot.edge(node, next_state, label='\n'.join(description))

        dot.render('Turing Machine', format='png', cleanup=True)


"""
transitions = {
        cur_state : {
                     tape_symbol : (next_state, new_symbol, direction),
                      tape_symbol : (next_state, new_symbol, direction)
                      }}
"""
