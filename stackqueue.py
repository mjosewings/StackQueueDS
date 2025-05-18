#Project 1 - Stacks & Queues

#Part 1 - Implement three classes named Stack, Queue, and Deque
class Stack:
    def __init__(self):
        self.stack = []
    
    def push(self, item):
        self.stack.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        return None
    
    def is_empty(self):
        return len(self.stack) == 0
    
    def size(self):
        return len(self.stack)
    
    def get_stack(self):
        return self.stack


class Queue:
    def __init__(self):
        self.queue = []
    
    def enqueue(self, item):
        self.queue.append(item)
    
    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        return None
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def size(self):
        return len(self.queue)
    
    def get_queue(self):
        return self.queue
        
class Deque:
    def __init__(self):
        self.deque = []
        
    def is_empty(self):
        return self.deque == []
    
    def add_front(self, item):
        self.deque.insert(item)

    def add_rear(self, item):
        self.deque.append(0, item)

    def remove_front(self):
        return self.deque.pop()

    def remove_rear(self):
        return self.deque.pop(0)

    def size(self):
        return len(self.deque)

    
#Part 2 - Applications

#Part 2a: Tower of Hanoi
def tower_of_hanoi(n, source, destination, auxiliary, disks):

    #If there is only one disk, move it from source to destination
    if n == 1:
        print(f"Move {disks[n-1]} disk from {source} to {destination}")
        return
    tower_of_hanoi(n-1, source, auxiliary, destination, disks)

    #Move the nth disk from source to destination
    print(f"Move {disks[n-1]} disk from {source} to {destination}")
    tower_of_hanoi(n-1, auxiliary, destination, source, disks)

def main():
    n = int(input("Enter the number of disks: ")) #Asks user for the number of disks
    disks = []
    for i in range(n):
        #Asks user for the color of each disk
        color = input(f"Enter the color of disk {i+1} (from top to bottom): ")
        disks.append(color) #Adds the color to the list of disks
    
    #Prints the steps to solve the Tower of Hanoi
    print("\nSteps to solve the Tower of Hanoi:")
    tower_of_hanoi(n, 'A', 'C', 'B', disks)

if __name__ == "__main__":
    main()



#Part 2b: DNA Sequence Alignment Tool

#Imports necessary libraries
from collections import deque

#Reads and validates DNA sequences from the user and stores them in a list
def get_valid_dna_sequence(prompt):
    while True:

        #Converts the input to uppercase to ensure that the user can enter the sequence in any case
        sequence = input(prompt).upper()

        #Checks if the sequence contains only A, T, C, and G
        if all(nucleotide in 'ATCG' for nucleotide in sequence):
            return sequence
        
 #If the sequence is not valid, prompt the user to enter a valid sequence
        else:
            print("Invalid input. Please enter a sequence containing only A, T, C, and G.")

'''Gets the number of sequences from the user by 
asking them to enter the amount of sequences they want to input.'''
def get_number_of_sequences():
    while True:
        try:
            num = int(input("How many DNA sequences do you want to input? "))
            if num > 0:
                return num
            
            #The user is prompted to enter a positive integer.
            else:
                print("Please enter a positive integer.") 
            
        #Catches the exception if the user enters a non-integer value
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

# Queue for input sequences
input_sequences = deque()

#Obtains the number of sequences from the user
num_sequences = get_number_of_sequences()

#Retrieves sequence from the user by asking them to enter a sequence
for i in range(num_sequences):
    input_sequences.append(get_valid_dna_sequence(f"Enter DNA sequence {i+1}: "))

#Reads sequences from the queue
def read_sequences(queue):
    while queue:
        yield queue.popleft()

sequences = list(read_sequences(input_sequences))

#Stores the sequences in a list by reading them from the queue provided in a sequence
def initialize_matrix(seq1, seq2):
    rows = len(seq1) + 1
    cols = len(seq2) + 1
    score_matrix = [[0] * cols for _ in range(rows)]
    traceback_matrix = [[None] * cols for _ in range(rows)]
    return score_matrix, traceback_matrix

#Each pair of sequences are being processed in a loop
for i in range(0, len(sequences), 2):
    if i + 1 < len(sequences):
        seq1, seq2 = sequences[i], sequences[i+1]
        score_matrix, traceback_matrix = initialize_matrix(seq1, seq2)

#Function to fill the score matrix and traceback matrix
        def fill_matrix(seq1, seq2, score_matrix, traceback_matrix):
            match_score = 1
            mismatch_penalty = -1
            gap_penalty = -2

            for i in range(1, len(seq1) + 1):
                for j in range(1, len(seq2) + 1):
                    match = score_matrix[i-1][j-1] + (match_score if seq1[i-1] == seq2[j-1] else mismatch_penalty)
                    delete = score_matrix[i-1][j] + gap_penalty
                    insert = score_matrix[i][j-1] + gap_penalty
                    score_matrix[i][j] = max(match, delete, insert)

                    if score_matrix[i][j] == match:
                        traceback_matrix[i][j] = (i-1, j-1)
                    elif score_matrix[i][j] == delete:
                        traceback_matrix[i][j] = (i-1, j)
                    else:
                        traceback_matrix[i][j] = (i, j-1)

        fill_matrix(seq1, seq2, score_matrix, traceback_matrix)

        def traceback(seq1, seq2, traceback_matrix):
            aligned_seq1 = []
            aligned_seq2 = []
            stack = [(len(seq1), len(seq2))]

            while stack:
                i, j = stack.pop()
                if i > 0 and j > 0 and traceback_matrix[i][j] == (i-1, j-1):
                    aligned_seq1.append(seq1[i-1])
                    aligned_seq2.append(seq2[j-1])
                elif i > 0 and (j == 0 or traceback_matrix[i][j] == (i-1, j)):

                    #Appends the first aligned sequence in the first sequence
                    aligned_seq1.append(seq1[i-1]) 
                    aligned_seq2.append('-') #Separates the second aligned sequences with a dash
                else:
                    aligned_seq1.append('-') #Separates the first aligned sequences with a dash
                    #Appends the second aligned sequence in the second sequence
                    aligned_seq2.append(seq2[j-1])

                if traceback_matrix[i][j]:
                    stack.append(traceback_matrix[i][j])

#Returns the joined strings of the aligned sequences and reverses them
            return ''.join(reversed(aligned_seq1)), ''.join(reversed(aligned_seq2))

        aligned_seq1, aligned_seq2 = traceback(seq1, seq2, traceback_matrix)

        #Prints the aligned sequences for each pair
        print(f"Aligned Sequences for pair {i//2 + 1}:") 
        print(aligned_seq1) #prints the first aligned sequence
        print(aligned_seq2) #prints the second aligned sequence

    #Prints a message if there is no pair for alignment
    else:
        print(f"Sequence {i+1} does not have a pair for alignment.")
