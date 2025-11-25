import streamlit as st
import pandas as pd
import plotly.express as px
global book_data

st.cache_data.clear()
st.cache_resource.clear()

# --- Data Simulation (In a real app, this would come from a database) ---
@st.cache_data
def load_data():
    book_data = pd.read_csv('library_books.csv')
    donated_data = pd.read_csv('donated_books.csv')
    issue_data = pd.read_csv('issue_books.csv')
    return book_data, donated_data, issue_data

book_data, donated_data, issue_data = load_data()

# --- Streamlit App Structure ---
st.set_page_config(layout="wide")
st.sidebar.title("Library App Navigation")

selection = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Issue Book", "Return Book", "Donate Book"]
)

# Dashboard Page
if selection == "Dashboard":
    st.title("📚 Library Dashboard")
    st.write("Welcome to the library management system!")

    max_book=book_data['Popularity'].max()
    st.write("Most popular book(s):")
    st.write(book_data[book_data['Popularity'] == max_book])

    c1, c2 = st.columns(2)

    with c1:
        genre_counts = book_data['Genre'].value_counts().reset_index()
        genre_counts.columns = ['Genre', 'Count']
        
        fig_genre = px.bar(
            genre_counts, 
            x='Genre', 
            y='Count', 
            color='Genre',
            title="Books by Genre",
            text_auto=True
        )
        st.plotly_chart(fig_genre, use_container_width=True)

    with c2:
        status_data = book_data['Issued'].map({True: 'Issued', False: 'Available'}).value_counts().reset_index()
        status_data.columns = ['Status', 'Count']
        
        fig_status = px.pie(
            status_data, 
            values='Count', 
            names='Status', 
            title="Current Library Status",
            hole=0.4,
            color='Status',
            color_discrete_map={'Issued':'#FF6F61', 'Available':'#6B5B95'}
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
# Issue Book Page
elif selection == "Issue Book":
    st.title("📖 Issue a Book")
    st.write("Select a book to issue to a member.")

    issue_book = st.text_input("Enter the name of the book you want to search").strip()
    issue_book = issue_book.title()

    if issue_book:
        if issue_book in book_data['Book Name'].tolist():
            st.write(book_data.loc[issue_book == book_data['Book Name']])
            
            ques = st.radio("Enter whether you want to issue this book or not:", ("No", "Yes"))
            
            if st.button("Submit"):
                if ques == "Yes":   
                    member_ID = st.text_input('Member ID')
                    member_name = st.text_input('Member Name')
                    book_ID = st.text_input('Book ID')
                    book_name = st.text_input('Book Name')
                    issue_date = st.date_input('Issue Date')
                    duration_days = st.number_input('Duration (in days)', min_value=1, value=14)
                    due_date = issue_date + pd.Timedelta(days=duration_days)

                    if st.button("Confirm Issue"):
                        new_issue = {
                            'Member ID': member_ID,
                            'Member Name': member_name,
                            'Book ID': book_ID,
                            'Book Name': book_name,
                            'Issue Date': issue_date,
                            'Due Date': due_date,
                            'Returned': False
                        }

                        st.write("Book issued successfully!")
                        st.write(new_issue)

                        issue_data = pd.concat([issue_data, pd.DataFrame([new_issue])], ignore_index=True)

                        book_data.at[issue_book, 'Issued'] = "Yes"
                        book_data.at[issue_book, 'Popularity'] += 1
                    
                        st.success(f"'{issue_book}' issued successfully!")  
                        st.rerun()

                else:
                    st.info("Book was not issued.")
                    st.rerun()

        else:
            st.error("This book is not present in the library as of now.")
            st.rerun()
    

# Return Book Page
elif selection == "Return Book":
    st.title("↩️ Return a Book")
    st.write("Enter the book title to mark it as returned.")

    return_book = st.text_input("Enter Member ID").strip()

    if return_book:
        if return_book in issue_data['Member ID'].tolist():
            st.write('Book details:')
            st.write("Review the details before processing return")
            st.write(issue_data.loc[return_book == issue_data['Memeber ID']])

            if st.button("Process Return"):
                issue_data.at[return_book, 'Returned'] = True
                st.write("Book returned successfully!")
                st.rerun()

        else:
            st.error("This book is not present in the library as of now.")
            st.rerun()
    
# Donate Book Page
elif selection == "Donate Book":
    
    st.title("🎁 Donate Books")
    st.write("Share the joy of reading by donating books to our library!")

    with st.form("new_book_form"):
        new_name = st.text_input("Your Name")
        new_email = st.text_input("Email Address")
        new_phone = st.text_input("Phone Number")
        new_title = st.text_input("Book Title")
        new_author = st.text_input("Author")
        new_genre = st.selectbox("Genre:", book_data['Genre'].unique().tolist() + ["New Genre"])
        if new_genre == "New Genre":
            new_genre = st.text_input("Enter new genre:")
        num_copies = st.number_input("Number of Copies to Donate:", min_value=1, value=1)
        new_notes = st.text_input("Additional Notes (Optional)")
        submitted = st.form_submit_button("Submit Donation")

        if submitted:
            if new_title and new_author and new_genre and num_copies > 0:
                new_book_id = book_data['Book ID'].max() + 1 if not book_data.empty else 1
                new_book_data = {
                    'Book ID': new_book_id,
                    'Book Name  ': new_title,
                    'Author': new_author,
                    'Genre': new_genre,
                    'Shelf Location': 'To Be Assigned',
                    'Issued': False,
                    'Popularity': 0,
                    'Copies Available': num_copies,
                }
                new_donated_data = {
                    'Name': new_name,
                    'Email': new_email, 
                    'Phone': new_phone,
                    'Book ID': new_book_id,
                    'Book Title': new_title,
                    'Author': new_author,
                    'Genre': new_genre,
                    'Number of Copies': num_copies,
                    'Notes': new_notes
                }
                book_data = pd.concat([book_data, pd.DataFrame([new_book_data])], ignore_index=True)
                donated_data = pd.concat([donated_data, pd.DataFrame([new_donated_data])], ignore_index=True)
                st.success(f"'{new_title}' ({num_copies} copies) added to the library! Thank you for your donation.")
                st.rerun()
            else:
                st.error("Please fill in all book details and specify at least one copy.")