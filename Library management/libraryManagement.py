import os
import datetime
from colorama import init, Fore, Style
init(autoreset=True)

#Global Variables
bookListPath = "D:/learning python/Projects/Library management/books.txt"
issueBookLP = "D:/learning python/Projects/Library management/issued.txt"
masterListPath = "D:/learning python/Projects/Library management/master.txt"

def addBooks():
  
    try:
        title = input(Fore.CYAN+"Enter the book title: ")
        author = input(Fore.CYAN+"Enter the author name: ")
        isbn = input(Fore.CYAN+"Enter the ISBN number: ")
        with open(bookListPath, "a+") as f:
            f.seek(0)
            existingBooks = [line.strip().split(",") for line in f.readlines()]

        # Safe way to get existing ISBNs
        existingISBN = [book[2].strip() for book in existingBooks if len(book) >= 3]

        if isbn in existingISBN: #Checks if entered isbn exists in the list of existing isbn(s)
            print(Fore.RED + "Book can not be added since the same ISBN exists!")
            return
   
        with open(bookListPath, "a") as f:
            f.write(f"{title}, {author}, {isbn}\n")
            print(Fore.GREEN + f"Book: {title}, By: {author}, ISBN: {isbn} added successfully!")

    except FileNotFoundError:
        print(Fore.RED + "File not found!")

def viewBooks():
    try:
        
        with open(bookListPath, "r") as f:
            f.seek(0)
            books = [line.strip().split(",") for line in f.readlines()] #Gets book list
        for book in books:
            print(book)
    except FileNotFoundError:
        return(Fore.RED + "File not found!")
    

def issueBook():
    try: 
        #Taking the information
        isbn = input(Fore.CYAN+"Enter the ISBN number for the book you wanna issue: ")
        student = input(Fore.CYAN+"Please enter your name: ")

        #Checking the availability in the library
        with open(bookListPath, 'r') as f:
            libraryBooks = [line.strip().split(",") for line in f.readlines()]

        existingISBN = [book[2].strip() for book in libraryBooks]
        if isbn not in existingISBN:
            print(Fore.RED + "Sorry, the following book is out!")
            return

        #Checking if the book is already issued
        try:
            with open(issueBookLP, "r") as f:
                issuedBooks = [line.strip().split(",") for line in f.readlines()]
        except FileNotFoundError:
            issuedBooks = []
        
        #Issuing the book
        issuedISBN = [book[2].strip() for book in issuedBooks]
        if isbn in issuedISBN:
            print(Fore.RED+"The book is already issued!")
            return
        issueDate = datetime.date.today().strftime("%Y-%m-%d")
        with open(issueBookLP, "a") as f:
            f.write(f"{isbn}, {student}, {issueDate}\n")
        print(Fore.GREEN+"Book issued successfully!")

        # Updating the library
        with open(bookListPath, 'r') as f:
            books = [line.strip().split(",") for line in f.readlines()]
            updatedBooks = [left for left in books if left[2].strip() != isbn]
            with open(bookListPath, "w") as f:
                for left in updatedBooks:
                    f.write(",".join([a.strip() for a in left]) + "\n")


    except FileNotFoundError:
        return
    
def returnBook():
    isbn = input(Fore.CYAN+"Enter the ISBN number of the book: ")

    #Checking if issued
    try: 
        with open(issueBookLP, 'r') as f:
            issuedBooks = [line.strip().split(",") for line in f.readlines()]
    except FileNotFoundError:
        issuedBooks = []
    issuedISBN = [book[0].strip() for book in issuedBooks]
    if isbn not in issuedISBN:
        print(Fore.RED+"The book was not issued!")
        return
    try:
        returnedBook = [book for book in issuedBooks if book[0].strip() == isbn][0] #Returned book index
    except IndexError:
        print(Fore.RED+"The book was not issued")
        return


    #Updating the issued file
    with open(issueBookLP, 'r') as f:
        books = [line.strip().split(",") for line in f.readlines()]
        updatedBooks = [issued for issued in books if issued[0] != isbn]
        with open(issueBookLP, "w") as f:
            for issued in updatedBooks:
                f.write(",".join(issued) + "\n")

    #Adding to library
    with open(masterListPath, 'r') as f:
        masterBooks = [line.strip().split(",") for line in f.readlines()]
    
    originalBook = [book for book in masterBooks if book[2].strip() == isbn][0]

    # Add back to books.txt
    with open(bookListPath, 'a') as f:
        f.write(",".join(originalBook) + "\n")
        print(Fore.GREEN + "Library updated successfully!")

def searchBook():
    isbn = input(Fore.CYAN + "Enter the book ISBN you want to search: ")
    with open(bookListPath, 'r') as f:
        libraryBooks = [line.strip().split(",") for line in f.readlines()]
    
    libraryISBN = [book[2].strip() for book in libraryBooks]

    with open(issueBookLP, 'r') as f:
        issueBook = [line.strip().split(",") for line in f.readlines()]

    issueISBN = [book[0].strip() for book in issueBook]

    if isbn in libraryISBN:
        print(Fore.GREEN+"The book is currently available")

    elif isbn in issueISBN: 
        print(Fore.RED+"The book is currently issued")

    else:
        print(Fore.RED+"Please recheck the ISBN number!")



def menu():
    while True:
        
        print(Fore.CYAN + "\n===== Library Menu =====")
        print(Fore.YELLOW + "1. Add Book")
        print(Fore.YELLOW + "2. View Books")
        print(Fore.YELLOW + "3. Issue Book")
        print(Fore.YELLOW + "4. Return Book")
        print(Fore.YELLOW + "5. Check Availability")
        print(Fore.YELLOW + "6. Clear log")
        print(Fore.YELLOW + "7. Exit")

        choice = input(Fore.YELLOW + "Enter your choice: ")

        if choice == "1":
            addBooks()
        elif choice == "2":
            viewBooks()
        elif choice == "3":
            issueBook()
        elif choice == "4":
            returnBook()
        elif choice == '5':
            searchBook()
        elif choice == '6':
            os.system('cls' if os.name == 'nt' else 'clear')
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Try again.")

menu()