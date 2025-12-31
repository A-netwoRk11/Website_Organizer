# Website Organizer

A comprehensive web application to organize multiple email IDs, associated websites, and track important submission deadlines.

## 📋 Features

- **Email Management**: Store and organize multiple email IDs with their purposes
- **Website Organization**: Link websites to specific email IDs for easy access
- **Submission Tracking**: Never miss important deadlines with submission date tracking
- **Dashboard**: Get an overview of all your email IDs, websites, and upcoming submissions
- **Search Functionality**: Quickly find email IDs, websites, or submissions
- **Overdue Alerts**: Automatic detection of overdue submissions
- **Status Management**: Mark submissions as pending or completed

## 🚀 Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Open in Browser**:
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
website organizer/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── organizer.db          # SQLite database (auto-created)
│
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Dashboard
│   ├── emails.html      # Email management
│   ├── websites.html    # Website management
│   ├── submissions.html # Submission tracking
│   └── search.html      # Search results
│
└── static/              # Static files
    ├── style.css       # Stylesheet
    └── script.js       # JavaScript functions
```

## 💡 Usage

### Adding Email IDs
1. Go to "Email IDs" page
2. Click "+ Add Email ID"
3. Enter email address and purpose
4. Click "Add Email"

### Adding Websites
1. Click on an email ID to view its websites
2. Click "+ Add Website"
3. Enter website name, URL, and optional username
4. Click "Add Website"

### Tracking Submissions
1. Go to "Submissions" page
2. Click "+ Add Submission"
3. Select website, enter title, description, and due date
4. Click "Add Submission"

### Managing Deadlines
- View upcoming submissions on the dashboard
- Overdue submissions are highlighted in red
- Update submission status to "Completed" when done

## 🎨 Features Explained

### Dashboard
- Shows statistics: total emails, websites, pending and overdue submissions
- Displays upcoming submissions in a table
- Quick access cards for all email IDs

### Email Organization
- Add multiple email IDs with purposes (Work, Personal, Freelance, etc.)
- View all websites associated with each email
- Delete email IDs (cascades to websites and submissions)

### Website Management
- Link websites to specific email IDs
- Store website URLs and usernames
- Track how many submissions are pending for each website

### Submission Tracking
- Add submission deadlines with date and time
- Automatic overdue detection
- Status management (Pending/Completed)
- Search and filter submissions

## 🔧 Customization

### Change Port
Edit `app.py` line:
```python
app.run(debug=True, port=5000)  # Change 5000 to your preferred port
```

### Modify Colors
Edit `static/style.css` to change the color scheme:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## 📊 Database Schema

### EmailAccount
- id (Primary Key)
- email
- purpose
- created_at

### Website
- id (Primary Key)
- name
- url
- username
- email_id (Foreign Key)
- created_at

### Submission
- id (Primary Key)
- title
- description
- due_date
- website_id (Foreign Key)
- status
- created_at

## 🛡️ Security Note

For production use:
1. Change the `SECRET_KEY` in app.py
2. Use environment variables for sensitive data
3. Enable HTTPS
4. Add user authentication

## 📝 Future Enhancements

- Email notifications for upcoming deadlines
- Calendar view for submissions
- Export data to CSV/PDF
- Multi-user support with authentication
- Password storage for websites (encrypted)
- Browser extension for quick access

## 🤝 Contributing

Feel free to fork this project and add your own features!

## 📄 License

This project is open source and available under the MIT License.
