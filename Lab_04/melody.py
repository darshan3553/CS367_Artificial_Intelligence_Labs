import random
import math

def optimize_melody(quality_evaluator, note_pool, init_temp, cool_rate, stop_temp):
    # Initialize a random melody from the available pool of notes
    current_sequence = random.sample(note_pool, len(note_pool))
    optimal_sequence = current_sequence[:]
    temperature = init_temp

    while temperature > stop_temp:
        # Generate a neighboring melody by swapping two random notes
        new_sequence = current_sequence[:]
        idx1, idx2 = random.sample(range(len(note_pool)), 2)
        new_sequence[idx1], new_sequence[idx2] = new_sequence[idx2], new_sequence[idx1]

        # Determine the change in melody quality
        quality_change = quality_evaluator(new_sequence) - quality_evaluator(current_sequence)

        if quality_change < 0 or random.random() < math.exp(-quality_change / temperature):
            current_sequence = new_sequence[:]
            if quality_evaluator(current_sequence) < quality_evaluator(optimal_sequence):
                optimal_sequence = current_sequence[:]

        # Cool down the temperature gradually
        temperature *= cool_rate

    return optimal_sequence

def evaluate_quality(sequence):
    total_score = 0

    for index in range(len(sequence) - 1):
        if sequence[index] == 'Sa' and sequence[index + 1] != 'Re':
            total_score += 10
    return total_score

# User input for note sequences
user_notes = input("Provide the notes for the melody (comma-separated): ")
note_pool = [n.strip() for n in user_notes.split(',')]

best_sequence = optimize_melody(evaluate_quality, note_pool, init_temp=1000, cool_rate=0.95, stop_temp=0.01)
print("Optimal Melody:", best_sequence)