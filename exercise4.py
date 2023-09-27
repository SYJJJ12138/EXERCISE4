import sqlite3

def create_tables():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE Books
                 (BookID text, Title text, Author text, ISBN text, Status text)''')

    c.execute('''CREATE TABLE Users
                 (UserID text, Name text, Email text)''')

    c.execute('''CREATE TABLE Reservations
                 (ReservationID text, BookID text, UserID text, ReservationDate text)''')

    conn.commit()
    conn.close()

def add_book():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    book_id = input("Enter BookID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = input("Enter Status: ")

    c.execute("INSERT INTO Books VALUES (?, ?, ?, ?, ?)",
              (book_id, title, author, isbn, status))

    conn.commit()
    conn.close()

def find_book():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    book_id = input("Enter BookID: ")

    c.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status, Users.UserID, Users.Name, Users.Email, Reservations.ReservationID, Reservations.ReservationDate
                 FROM Books
                 INNER JOIN Reservations ON Books.BookID = Reservations.BookID
                 INNER JOIN Users ON Reservations.UserID = Users.UserID
                 WHERE Books.BookID = ?''', (book_id,))

    print(c.fetchall())

    conn.close()

def find_reservation_status():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    identifier = input("Enter Identifier: ")

    if identifier.startswith("LB"):
        c.execute("SELECT Status FROM Books WHERE BookID = ?", (identifier,))
    elif identifier.startswith("LU"):
        c.execute('''SELECT Books.Status
                     FROM Books
                     INNER JOIN Reservations ON Books.BookID = Reservations.BookID
                     WHERE Reservations.UserID = ?''', (identifier,))
    elif identifier.startswith("LR"):
        c.execute('''SELECT Books.Status
                     FROM Books
                     INNER JOIN Reservations ON Books.BookID = Reservations.BookID
                     WHERE Reservations.ReservationID = ?''', (identifier,))
    else:
        c.execute("SELECT Status FROM Books WHERE Title = ?", (identifier,))

    print(c.fetchall())

    conn.close()

def find_all_books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status, Users.UserID, Users.Name, Users.Email, Reservations.ReservationID, Reservations.ReservationDate
                 FROM Books
                 INNER JOIN Reservations ON Books.BookID = Reservations.BookID
                 INNER JOIN Users ON Reservations.UserID = Users.UserID''')

    print(c.fetchall())

    conn.close()

def modify_book():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    book_id = input("Enter BookID: ")
    title = input("Enter new Title: ")
    author = input("Enter new Author: ")
    isbn = input("Enter new ISBN: ")
    status = input("Enter new Status: ")

    c.execute("UPDATE Books SET Title = ?, Author = ?, ISBN = ?, Status = ? WHERE BookID = ?",
              (title, author, isbn, status, book_id))

    conn.commit()
    conn.close()

def delete_book():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    book_id = input("Enter BookID: ")

    c.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
    c.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))

    conn.commit()
    conn.close()

def main():
    create_tables()

    while True:
        print("\n1. Add a new book")
        print("2. Find a book's detail")
        print("3. Find a book's reservation status")
        print("4. Find all the books")
        print("5. Modify / update book details")
        print("6. Delete a book")
        print("7. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            add_book()
        elif choice == 2:
            find_book()
        elif choice == 3:
            find_reservation_status()
        elif choice == 4:
            find_all_books()
        elif choice == 5:
            modify_book()
        elif choice == 6:
            delete_book()
        elif choice == 7:
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()