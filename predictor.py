from random import randint


def count_triads(string):
    global count_of_triads, triads

    while len(string) > 3:
        for triad in triads:
            if triad + "0" in string[0:4]:
                count_of_triads[triad][0] += 1
                count_of_triads[triad][2] += 1  # total counted
            elif triad + "1" in string[0:4]:
                count_of_triads[triad][1] += 1
                count_of_triads[triad][2] += 1
        string = string[1:]


def filter_data(raw_data):
    filtered = ""
    if raw_data == "enough":
        return raw_data
    for i in raw_data:
        if i in "01":
            filtered += i
    return filtered


def collect_and_filter(length_required=3, feeding_info=False):
    data = ""

    while len(data) < length_required:
        if feeding_info:
            print(
                "Current data length is " + str(len(data)) + ", " + str(length_required - len(data)) + " symbols left")
        print("Print a random string containing 0 or 1" + "\n")
        data += filter_data(input())

        # displaying information if it is not done yet
        if len(data) >= length_required:
            break

    return data


print("Please give AI some data to learn...")
data_string = collect_and_filter(length_required=100, feeding_info=True)
print("\nFinal data string:")
print(data_string)

# generating predictions
triads = ["000", "001", "010", "011", "100", "101", "110", "111"]
count_of_triads = {triad: [0, 0, 0] for triad in triads}  # [0's, 1's, total]
count_triads(data_string)

print()

# game
print("You have $1000. Every time the system successfully predicts your next press, you lose $1.")
print('Otherwise, you earn $1. Print "enough" to leave the game. Let\'s go!\n')
money = 1000
while True:
    test_string = collect_and_filter()
    if test_string == "enough":
        break
    count_triads(test_string)

    # finding the highest probable triad for the first three numbers
    most_used_triad = "000"
    for i in count_of_triads:
        if count_of_triads[i][2] > count_of_triads[most_used_triad][2]:
            most_used_triad = i

    prediction = most_used_triad

    # finding rest of numbers
    for i in range(len(test_string) - 3):
        if count_of_triads[test_string[i:i+3]][0] > count_of_triads[test_string[i:i+3]][1]:
            prediction += "0"
        elif count_of_triads[test_string[i:i+3]][0] < count_of_triads[test_string[i:i+3]][1]:
            prediction += "1"
        else:  # if they are equal
            prediction += str(randint(0, 1))

    print("prediction:\n" + prediction)

    prediction = prediction[3:]
    test_string = test_string[3:]  # excluding first three letters for calculation
    N = 0  # number correct
    M = len(prediction)  # total numbers

    for i in range(len(prediction)):
        if prediction[i] == test_string[i]:
            N += 1

    ACC = round(N / M * 100, 2)

    print("\nComputer guessed right", N, "out of", M, "symbols (" + str(ACC), "%)")
    money += M - N * 2  # total numbers minus numbers correct will give number incorrect,
    # do it again to get difference between correct and incorrect

    print("Your balance is now $" + str(money))

print("Game Over!")
