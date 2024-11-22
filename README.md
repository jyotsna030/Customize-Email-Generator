
# Custom Email Sending Application

This is a fully functional application that allows users to send customized emails from a CSV file. The application provides a front-end dashboard built using Streamlit, and the back-end is powered by FastAPI. It supports email scheduling, throttling, and real-time email status tracking using WebSockets. The emails can be personalized using a template-based approach with dynamic fields such as name and other custom data.

## Features

- **CSV Upload:** Upload a CSV file containing email details for personalized email sending.
- **Email Personalization:** Customize emails with a personal touch using dynamic placeholders like `name`.
- **SMTP Configuration:** Connect your email account with SMTP server settings (e.g., Gmail, custom SMTP).
- **Rate Limiting:** Limit the number of email requests per minute to avoid spam issues.
- **WebSocket Tracking:** Real-time status updates of sent emails.
- **Email Scheduling:** Send emails immediately or schedule them for later using Celery tasks.
- **Email Delivery:** Supports sending emails via SMTP with a user-friendly interface for configuring the subject, body, and recipients.

## Prerequisites

- Python 3.x
- `pip` package manager
- A working SMTP server (e.g., Gmail or custom SMTP)
- Celery and Redis for scheduling emails (optional for scheduling functionality)

## Setup Instructions

Follow these steps to set up and run the project:

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/custom-email-sender.git
cd custom-email-sender
2. Install dependencies
Ensure you have Python 3.x installed, then install the required Python packages:

bash
Copy code
pip install -r requirements.txt
3. Setup and Configure the SMTP Server
To send emails, you'll need to configure the SMTP server. If you are using Gmail, you'll need to enable "Less secure apps" or use OAuth2. For custom SMTP, use the details provided by your email provider.

4. Start the FastAPI Server
Run the FastAPI backend server using uvicorn. This will start the API that the frontend communicates with:

bash
Copy code
uvicorn app.api:app --reload
This will start the server at http://127.0.0.1:8000.

5. Start the Celery Worker (For Scheduling Emails)
If you want to schedule emails, you need to have Celery and Redis installed. Run the Celery worker using the following command:

bash
Copy code
celery -A tasks.celery_tasks worker --loglevel=info
6. Run the Streamlit Dashboard
To run the front-end dashboard, which is built with Streamlit, use the following command:

bash
Copy code
streamlit run frontend/dashboard.py
This will start the dashboard at http://localhost:8501.

Usage
Upload CSV File
Prepare CSV: The CSV file must have at least two columns: email and name. You can include additional columns to further personalize emails.

Example CSV format:

graphql
Copy code
email,name
user1@example.com,John
user2@example.com,Mary
Upload CSV: In the front-end dashboard, go to the Step 1: Upload CSV File section and upload the prepared CSV file.

Customize and Send Emails
Enter Email Details: Provide your email account details, email subject, and a personalization prompt. The prompt should include placeholders like {name} that will be replaced by actual data from the CSV.

Example of personalization prompt:

rust
Copy code
Hi {name},

We have an exciting offer just for you!
Send Emails: Click Send Emails to immediately send the customized emails to the recipients listed in the CSV.

Email Scheduling
Schedule Emails: You can choose to schedule emails by filling out the necessary details and clicking Schedule Emails. This will add the emails to a queue that will be processed asynchronously.
View Email Status
Track Status: Go to the Step 3: Email Status section to view the current status of sent emails. This provides real-time tracking via WebSocket.
API Endpoints
1. POST /upload/
Purpose: Upload a CSV file containing email details.
Request: Multipart form-data with a file input.
Response: Returns the columns of the CSV file.
2. POST /send/
Purpose: Send customized emails based on the uploaded CSV file.
Request: Form data containing the SMTP server settings, email subject, body, and CSV file.
Response: Returns a status and details of the sent emails.
3. POST /schedule/
Purpose: Schedule emails to be sent later using Celery.
Request: Form data containing the SMTP server settings, email subject, body, and CSV file.
Response: Returns a success message if emails are successfully scheduled.
4. GET /status/
Purpose: Fetch the current status of the sent emails.
Response: Returns a list of email statuses, including success or failure.
5. WebSocket /ws/
Purpose: Receive real-time updates on email statuses via WebSocket.
Troubleshooting
SMTP Errors: Ensure your SMTP settings (server, port, username, password) are correct.
Rate Limiting: If you hit the rate limit, wait for the next minute before retrying.
WebSocket Connection Issues: If you’re having trouble with WebSockets, ensure that your client is correctly handling the connection.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contributing
We welcome contributions to improve this project! Please fork the repository, make your changes, and submit a pull request.

Contact
For any questions or feedback, feel free to open an issue or contact us at your-email@example.com.

markdown
Copy code

---

### Key Sections Breakdown:

1. **Features**: Lists all the key features that the application provides, such as CSV upload, email scheduling, and WebSocket integration.
2. **Setup Instructions**: Provides a step-by-step guide to setting up the application, including installation and configuration steps.
3. **Usage**: Describes how users can interact with the app, upload files, customize and send emails, and view statuses.
4. **API Endpoints**: Explains the available backend API endpoints and how to use them.
5. **Troubleshooting**: Provides help on common issues such as SMTP errors or WebSocket issues.
6. **Contributing**: Encourages open-source contributions to improve the app.
7. **License & Contact**: Basic licensing and contact information.

This README provides a full overview of the project, usage instructions, and technical details for anyone wishing to understand or contribute to the project. Feel free to adjust the sections to better fit your exact needs!





