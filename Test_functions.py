import json, os
FILE = "tests.json"
tests = {}
def load():
    if os.path.exists(FILE):
        txt = open(FILE).read().strip()
        if txt:                       
            tests.update(json.loads(txt))
def save():
    json.dump(tests, open(FILE, "w"), indent=2)
def new_test():
    name = input("\nName of the test: ")
    num  = int(input("How many questions? "))
    questions = []
    for i in range(num):
        print(f"\nQuestion {i + 1}")
        q_text = input("  Enter the question: ")
        opts = [input(f"  Option {ltr}: ") for ltr in "ABCD"]
        ans  = input("  Which option is correct? (A/B/C/D): ").upper()
        questions.append({"text": q_text, "opts": opts, "ans": ans})
    tests[name] = questions
    save()
    print("\n Test saved!\n")
def take_test():
    if not tests:
        print("\nNo tests available yet.\n")
        return
    print("\nAvailable tests:")
    for idx, test_name in enumerate(tests, 1):
        print(f"  {idx}. {test_name}")
    choice = int(input("Choose a test number: ")) - 1
    test_name = list(tests)[choice]
    score = 0
    for q in tests[test_name]:
        print("\n" + q["text"])
        for ltr, text in zip("ABCD", q["opts"]):
            print(f"  {ltr}. {text}")
        user_ans = input("Your answer: ").upper()
        if user_ans == q["ans"]:
            print(" Correct! ")
            score += 1
        else:
            print(f" Wrong. Correct answer is {q['ans']}. ")
    total = len(tests[test_name])
    print(f"\n You scored {score}/{total}\n")
def modify_test():
    if not tests:
        print("\nNo tests to modify.\n")
        return
    for i, name in enumerate(tests, 1):
        print(f"{i}. {name}")
    test_name = list(tests)[int(input("Pick test number: ")) - 1]
    for i, q in enumerate(tests[test_name], 1):
        print(f"{i}. {q['text']}")
    q_idx = int(input("Pick question to edit: ")) - 1
    q = tests[test_name][q_idx]
    print("\n(Press Enter to keep current value)")
    new_text = input("New question text: ")
    if new_text:
        q["text"] = new_text
    for j, ltr in enumerate("ABCD"):
        new_opt = input(f"Option {ltr} [{q['opts'][j]}]: ")
        if new_opt:
            q["opts"][j] = new_opt
    new_ans = input(f"Correct letter [{q['ans']}]: ").upper()
    if new_ans in "ABCD":
        q["ans"] = new_ans
    save()
    print("\n Question updated!\n")
