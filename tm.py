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

    def display(self):
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
        dot.render('Turing Machine', format='png', cleanup=True)


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

    def print_configuration(self):
        print(f"Configuration: {''.join(self.tape[: self.head_position])} {self.state} {''.join(self.tape[self.head_position:])}")

class TwoTapeTuringMachine(TuringMachine):
    """
    Implementation of a two-tape Turing machine. This machine operates on two separate
    tapes simultaneously, with independent head positions for each tape. The transition
    function takes into account symbols from both tapes when determining the next state
    and actions.
    """
    def __init__(self, tape1, tape2, transitions):
        """
        Initialize the two-tape Turing machine with its tapes and transition function.

        Args:
            tape1 (list): The initial contents of the first tape
            tape2 (list): The initial contents of the second tape
            transitions (dict): A dictionary mapping (state, (symbol1, symbol2)) to
                              (next_state, (new_symbol1, new_symbol2), (direction1, direction2))
        """
        super().__init__(transitions)
        self.tape1 = tape1
        self.tape2 = tape2
        self.head_position1 = 0
        self.head_position2 = 0

    def write_symbol(self, symbols, positions):
        """
        Write symbols at the specified positions on both tapes.

        Args:
            symbols (tuple): A pair of symbols (symbol1, symbol2) to write
            positions (tuple): The positions (pos1, pos2) to write at
        """
        symbol1, symbol2 = symbols
        pos1, pos2 = positions
        self.tape1[pos1] = symbol1
        self.tape2[pos2] = symbol2

    def read_symbol(self, positions):
        """
        Read symbols from the specified positions on both tapes.

        Args:
            positions (tuple): The positions (pos1, pos2) to read from

        Returns:
            tuple: The symbols (symbol1, symbol2) at the specified positions
        """
        pos1, pos2 = positions
        return (self.tape1[pos1], self.tape2[pos2])

    def move(self, directions, positions):
        """
        Move the heads in the specified directions from the given positions.

        Args:
            directions (tuple): ('L'/'R', 'L'/'R') for left/right on each tape
            positions (tuple): Current positions (pos1, pos2)

        Returns:
            tuple: The new positions (new_pos1, new_pos2) after moving
        """
        pos1, pos2 = positions
        dir1, dir2 = directions

        # Move head on first tape
        new_pos1 = pos1
        if dir1.lower() == "r":
            if pos1 + 1 < len(self.tape1):
                new_pos1 = pos1 + 1
        elif dir1.lower() == "l":
            if pos1 > 0:
                new_pos1 = pos1 - 1

        # Move head on second tape
        new_pos2 = pos2
        if dir2.lower() == "r":
            if pos2 + 1 < len(self.tape2):
                new_pos2 = pos2 + 1
        elif dir2.lower() == "l":
            if pos2 > 0:
                new_pos2 = pos2 - 1

        return (new_pos1, new_pos2)

    def step(self):
        """
        Perform one step of the Turing machine computation.

        Returns:
            bool: True if a valid transition was found and executed, False otherwise
        """
        # Read current symbols from both tapes
        current_symbols = self.read_symbol((self.head_position1, self.head_position2))

        # Look up transition
        if self.state in self.transitions and current_symbols in self.transitions[self.state]:
            next_state, new_symbols, directions = self.transitions[self.state][current_symbols]

            # Write new symbols
            self.write_symbol(new_symbols, (self.head_position1, self.head_position2))

            # Move heads
            self.head_position1, self.head_position2 = self.move(
                directions,
                (self.head_position1, self.head_position2)
            )

            # Update state
            self.state = next_state
            return True

        return False

    def print_configuration(self):
        """
        Print the current configuration showing both tapes and machine state.
        """
        print("Configuration:")
        print(f"Tape 1: {''.join(self.tape1[: self.head_position1])} {self.state} {''.join(self.tape1[self.head_position1:])}")
        print(f"Tape 2: {''.join(self.tape2[: self.head_position2])} {self.state} {''.join(self.tape2[self.head_position2:])}")

    def run_until_halt(self, max_steps=1000):
        """
        Run the Turing machine until it halts or reaches the maximum number of steps.

        Args:
            max_steps (int): Maximum number of steps to execute before stopping

        Returns:
            tuple: (halted, steps) where halted is True if the machine halted normally
                  and steps is the number of steps executed
        """
        steps = 0
        while steps < max_steps:
            self.print_configuration()
            if not self.step():
                return True, steps
            steps += 1
        return False, steps
