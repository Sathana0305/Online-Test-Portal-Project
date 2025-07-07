import Test_functions as tf
def main():
    tf.load()
    
    while True:
        print("=== MAIN MENU ===")
        print("1. Create a new test")
        print("2. Take an existing test")
        print("3. Modify a test")
        print("4. Quit")
        choice = input("> ")
        
        if choice == "1":
            tf.new_test()
        elif choice == "2":
            tf.take_test()
        elif choice == "3":
            tf.modify_test()
        elif choice == "4":
            print("Good-bye!")
            break
        else:
            print("Please type 1, 2, 3 or 4.\n")
            
if __name__ == "__main__":
    main()
