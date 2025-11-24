import streamlit as st
import pandas as pd
global df_books

# --- Data Simulation (In a real app, this would come from a database) ---
@st.cache_data
def load_data():
    data = pd.read_csv('library_books.csv')
    return data

df_books = load_data()

# --- Streamlit App Structure ---
st.set_page_config(layout="wide")
st.sidebar.title("Library App Navigation")

selection = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Issue Book", "Return Book", "Donate Book"]
)

# --- Dashboard Page ---
if selection == "Dashboard":
    st.title("📚 Library Dashboard")
    st.write("Welcome to the library management system!")
    

# --- Issue Book Page ---
elif selection == "Issue Book":
    st.title("📖 Issue a Book")
    st.write("Select a book to issue to a member.")

    issue_book_title = st.text_input("Enter the name of the book you want to search: ")
    issue_book_title = issue_book_title.strip()
    issue_book_title = issue_book_title.title()

    if st.button("Return Book"):
        if issue_book_title:
            if issue_book_title in df_books['Book Name'].tolist():
                book_index = df_books[df_books['Book Name'] == issue_book_title].index[0]
                if df_books.loc[book_index, 'Copies Available'] == 0:
                    st.warning(f"'{issue_book_title}' is currently not available for issue.")
                else:
                    df_books.loc[book_index, 'Copies Available'] -= 1
                    st.success(f"'{issue_book_title}' has been returned successfully!")
                    st.rerun()
            else:
                st.error(f"Book with title '{issue_book_title}' not found in our records.")
        else:
            st.warning("Please enter a book title to issue")
    

# --- Return Book Page ---
elif selection == "Return Book":
    st.title("↩️ Return a Book")
    st.write("Enter the book title to mark it as returned.")

    return_book_title = st.text_input("Enter the name of the book you want to search: ")
    return_book_title = return_book_title.strip()
    return_book_title = return_book_title.title()

    if st.button("Return Book"):
        if return_book_title:
            if return_book_title in df_books['Book Name'].tolist():
                book_index = df_books[df_books['Book Name'] == return_book_title].index[0]
                if df_books.loc[book_index, 'Copies Available'] < df_books.loc[book_index, 'Total Copies']:
                    df_books.loc[book_index, 'Copies Available'] += 1
                    st.success(f"'{return_book_title}' has been returned successfully!")
                    st.rerun()
                else:
                    st.warning(f"'{return_book_title}' was not recorded as issued or already has all copies available.")
            else:
                st.error(f"Book with title '{return_book_title}' not found in our records.")
        else:
            st.warning("Please enter a book title to return.")
    

# --- Donate Book Page ---
elif selection == "Donate Book":
    
    st.title("🎁 Donate a New Book")
    st.write("Help expand our collection by donating new books!")

    with st.form("new_book_form"):
        new_title = st.text_input("Book Title:")
        new_author = st.text_input("Author:")
        new_genre = st.selectbox("Genre:", df_books['Genre'].unique().tolist() + ["New Genre"])
        if new_genre == "New Genre":
            new_genre = st.text_input("Enter new genre:")
        num_copies = st.number_input("Number of Copies to Donate:", min_value=1, value=1)
        submitted = st.form_submit_button("Add Book to Library")

        if submitted:
            if new_title and new_author and new_genre and num_copies > 0:
                new_book_id = df_books['Book ID'].max() + 1 if not df_books.empty else 1
                new_book_data = {
                    'Book ID': new_book_id,
                    'Book Name  ': new_title,
                    'Author': new_author,
                    'Genre': new_genre,
                    'Copies Available': num_copies,
                    'Total Copies': num_copies,
                    'Popularity': 0
                }
                df_books = pd.concat([df_books, pd.DataFrame([new_book_data])], ignore_index=True)
                st.success(f"'{new_title}' ({num_copies} copies) added to the library! Thank you for your donation.")
                st.rerun()
            else:
                st.error("Please fill in all book details and specify at least one copy.")