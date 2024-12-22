from graphviz import Digraph
from collections import defaultdict
from abc import ABC, abstractmethod

class TuringMachine(ABC):
    def __init__(self, transitions):
        self.transitions = transitions
        self.state = 'q_1'  # Initial state

    @abstractmethod
    def write_symbol(self, symbol, position):
        pass

    @abstractmethod
    def read_symbol(self, position):
        pass

    @abstractmethod
    def move_head(self, direction, position):
        pass
    @abstractmethod
    def print_configuration(self):
        pass

    @abstractmethod
    def step(self):
        pass

    def display(self, title):
        """
        Create a visual representation of the Turing machine's state diagram
        using graphviz.
        """
        dot = Digraph()
        for node in self.transitions:
            dot.node(node)
            # Group transitions that connect to the same nodes
            next_state_description_dict = defaultdict(list)
            for tape_symbol, (next_state, new_symbol, direction) in self.transitions[node].items():
                next_state_description_dict[next_state].append(f"{tape_symbol} -> {new_symbol}, {direction}")
            for next_state, description in next_state_description_dict.items():
                dot.edge(node, next_state, label='\n'.join(description))
        dot.render(f'assets/{title}', format='png', cleanup=True)


class OneTapeTuringMachine(TuringMachine):
    def __init__(self, tape, transitions):
        super().__init__(transitions)
        self.tape = tape
        self.head_position = 0

    def write_symbol(self, symbol, position):
        self.tape[position] = symbol

    def read_symbol(self, position):
        return self.tape[position]

    def move_head(self, direction):
        if direction.lower() == "r":
            if self.head_position + 1 < len(self.tape): # prevent head from going off end of tape
                self.head_position += 1

        elif direction.lower() == "l":
            if self.head_position > 0: # prevent from going off end of tape
                self.head_position -= 1

    def write_tape(self, symbol):
        self.write_symbol(symbol, self.head_position)

    def read_tape(self):
        return self.read_symbol(self.head_position)

    def step(self):
        current_symbol = self.read_tape(self)

        if self.state in self.transitions and current_symbols in self.transitions[self.state]:

            next_state, new_tape_symbol, direction = self.transitions[self.state][current_symbol]

            self.write_tape(new_tape_symbol)
            self.move_head(direction)
            self.state = next_state

        else:
            self.state = 'q_reject'

    def print_configuration(self):
        print(f"Configuration: {''.join(self.tape[: self.head_position])} {self.state} {''.join(self.tape[self.head_position:])}")

class TwoTapeTuringMachine(TuringMachine):
    def __init__(self, tape1, tape2, transitions):
        super().__init__(transitions)
        self.tape1 = tape1
        self.tape2 = tape2
        self.head_position1 = 0
        self.head_position2 = 0

    def write_symbol(self, symbols, positions):
        symbol1, symbol2 = symbols
        pos1, pos2 = positions
        self.tape1[pos1] = symbol1
        self.tape2[pos2] = symbol2

    def read_symbol(self, positions):
        pos1, pos2 = positions
        return (self.tape1[pos1], self.tape2[pos2])

    def move_head(self, directions, positions):
        pos1, pos2 = positions
        dir1, dir2 = directions

        new_pos1 = pos1
        if dir1.lower() == "r":
            if pos1 + 1 < len(self.tape1):
                new_pos1 = pos1 + 1
        elif dir1.lower() == "l":
            if pos1 > 0:
                new_pos1 = pos1 - 1

        new_pos2 = pos2
        if dir2.lower() == "r":
            if pos2 + 1 < len(self.tape2):
                new_pos2 = pos2 + 1
        elif dir2.lower() == "l":
            if pos2 > 0:
                new_pos2 = pos2 - 1

        return (new_pos1, new_pos2)

    def step(self):

        current_symbols = self.read_symbol((self.head_position1, self.head_position2))

        if self.state in self.transitions and current_symbols in self.transitions[self.state]:

            next_state, new_symbols, directions = self.transitions[self.state][current_symbols]
            self.write_symbol(new_symbols, (self.head_position1, self.head_position2))

            self.head_position1, self.head_position2 = self.move_head(
                directions,
                (self.head_position1, self.head_position2)
            )

            self.state = next_state

        else:
            self.state = 'q_reject'

    def print_configuration(self):
        """
        Print the current configuration showing both tapes and machine state.
        """
        print("Configuration:")
        print(f"Tape 1: {''.join(self.tape1[: self.head_position1])} {self.state} {''.join(self.tape1[self.head_position1:])}")
        print(f"Tape 2: {''.join(self.tape2[: self.head_position2])} {self.state} {''.join(self.tape2[self.head_position2:])}")
