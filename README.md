# MediReminder

MediReminder is a comprehensive medication management system built with Django that helps users track their medications, set reminders, and manage their healthcare providers.

## Features

- **User Management**
  - Custom user authentication
  - Profile management with profile pictures
  - Secure password handling

- **Medicine Management**
  - Add and manage medications
  - Upload medicine images
  - Track dosage and manufacturer information
  - Detailed medicine information storage

- **Reminder System**
  - Set medication reminders
  - Flexible scheduling options
  - Email/notification alerts
  - Track medication adherence

- **Doctor Management**
  - Store doctor information
  - Track appointments
  - Manage prescriptions

- **Medicine Scanner**
  - Scan medicine labels
  - OCR for medicine information
  - Scan history tracking

## Technology Stack

- **Backend**: Django
- **Database**: SQLite (development) / MySQL (production)
- **Frontend**: 
  - HTML/CSS/JavaScript
  - Tailwind CSS
  - Font Awesome icons
  - Google Fonts

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/medireminder.git
   cd medireminder
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
medireminder/
├── medireminder/          # Project configuration
├── users/                 # User management app
├── medicines/            # Medicine management app
├── static/               # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── media/                # User uploaded files
│   ├── profile_images/
│   ├── medicine_images/
│   └── scan_images/
├── templates/            # HTML templates
│   ├── base.html
│   ├── users/
│   └── medicines/
└── requirements.txt      # Project dependencies
```

## Configuration

1. Environment Variables:
   Create a `.env` file in the project root:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key
   DATABASE_URL=your-database-url
   EMAIL_HOST=your-email-host
   EMAIL_PORT=your-email-port
   EMAIL_HOST_USER=your-email
   EMAIL_HOST_PASSWORD=your-email-password
   ```

2. Database Configuration:
   - Development: SQLite (default)
   - Production: Configure your production database in settings.py

## Usage

1. Register a new account or login with existing credentials
2. Add your medications and doctors
3. Set up reminders for your medications
4. Use the scanner feature to quickly add new medications
5. Track your medication history and adherence

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django documentation
- Tailwind CSS
- Font Awesome
- Google Fonts

## Contact

Your Name - your.email@example.com
Project Link: https://github.com/yourusername/medireminder
