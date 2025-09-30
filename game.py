import random

print("=== Rock Paper Scissors ===")
print("Rules: Rock beats Scissors, Scissors beats Paper, Paper beats Rock")
print("First to win 3 rounds is the Champion!")

user_score = 0
computer_score = 0
round_number = 1

while user_score < 3 and computer_score < 3:
    print("\nRound", round_number)
    print("Score -> You:", user_score, " Computer:", computer_score)

    print("\nChoose one:")
    print("1. Rock")
    print("2. Paper")
    print("3. Scissors")

    try:
        my_choice = int(input("Enter your choice (1-3): "))
        if my_choice not in [1, 2, 3]:
            print("Invalid choice. Please enter 1, 2 or 3.")
            continue
    except ValueError:
        print("Please enter a number only.")
        continue

    computer_choice = random.randint(1, 3)

    # Convert numbers to text
    choices = {1: "Rock", 2: "Paper", 3: "Scissors"}
    print("You chose:", choices[my_choice])
    print("Computer chose:", choices[computer_choice])

    # Decide winner
    if my_choice == computer_choice:
        print("It's a Tie!")
    elif (my_choice == 1 and computer_choice == 3) or \
         (my_choice == 2 and computer_choice == 1) or \
         (my_choice == 3 and computer_choice == 2):
        print("You win this round!")
        user_score += 1
    else:
        print("Computer wins this round!")
        computer_score += 1

    round_number += 1

# Final result
print("\n=== GAME OVER ===")
print("Final Score: You", user_score, "-", computer_score, "Computer")

if user_score > computer_score:
    print("🎉 You are the Champion!")
else:
    print("💻 Computer Wins!")
