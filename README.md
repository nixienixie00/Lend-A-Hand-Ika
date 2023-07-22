# Lend A Hand - Micro-Volunteering Platform

Lend A Hand is an easy-to-use micro-volunteering platform developed for the TechXelerate Hackathon. Our project aims to connect volunteers with meaningful opportunities to contribute to various causes and organizations.

## Project Description

Lend A Hand provides a user-friendly web interface built using Flask, HTML, CSS, JavaScript, and SQLAlchemy. The platform allows users to browse and apply for micro-volunteering tasks through task cards, each providing essential details about the task, such as the title, deadline, required skills, and the cause it supports.

## How to Install and Run the Project

1. Clone the repository to your local machine:
 ```
git clone https://github.com/your-username/lend-a-hand.git
cd lend-a-hand
 ```

2. Set up a virtual environment (optional but recommended)
```
python -m venv venv
```

3. Activate the virtual environment:

- On Windows:
```
venv\Scripts\activate
```

- On macOS and Linux:
```
source venv/bin/activate

```

4. Install the required dependencies:
```
pip install -r requirements.txt
```

5. Run the development server:
```
python app.py
```


The application will be accessible at `http://localhost:5000`.

## How to Use the Project

1. **Sign Up:** When you first load the Lend A Hand website, click the "Sign Up" button to create a new account. Provide your first name, email, password, and address. Click "Sign Up" to proceed.

2. **Login:** If you already have an account, click the "Login" button and enter your registered email and password.

3. **Home Page:** After signing up or logging in, you'll be directed to the Home Page. Here, you'll find a list of Task Cards representing different volunteering opportunities. Each card contains essential details about the task.

4. **More Info:** Click the "More info" button on a Task Card to view an automated email draft expressing your interest in the volunteering opportunity. You can customize the message before sending it.

5. **Filter Your Search:** Use the "Filter your Search" button to narrow down Task Cards based on specific preferences.

6. **Ask For A Hand:** To create your own volunteering opportunity, click the "Need A Hand?" button. Fill out the "Ask for A Hand" form with the title, deadline, required skills, causes, time required, minimum age, and a brief description of the task. Click "Submit" to post your task on the Home Page.

## Future Improvements

As this project was developed during the TechXelerate Hackathon, there are opportunities for improvement and expansion in the future. Some potential enhancements include:

- Adding a personal page to streamline task creation and automatically input relevant skills in the email draft.
- Expanding the range of causes and skills to diversify the opportunities on the platform.
- Making the application responsive
- Improving the Design of the User interface

## Credits

Lend A Hand was developed as a collaborative effort by our team members for the TechXelerate Hackathon:

- Anika Dzulkiflee
- Rishika Das
- Inika Agarwal


Special thanks to the organizers of the TechXelerate Hackathon for providing this learning and innovation platform.

## License

Lend A Hand is open-source and distributed under the [MIT License](LICENSE). Feel free to use, modify, and share the project as per the terms of the license.

We hope Lend A Hand inspires more people to engage in micro-volunteering and contributes to making the world a better place. Happy hacking at TechXelerate!











