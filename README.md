# IIITD TimeTable on GoogleCalendar

## Overview

The IIITD TimeTable on GoogleCalendar is a Python script and Streamlit web application designed to help IIITD students organize their academic schedules efficiently. The tool generates an iCalendar (.ics) file that can be easily imported into Google Calendar, providing a convenient way for students to keep track of their class timings. The interface is user-friendly and interactive, making it accessible for users with varying technical backgrounds.

## Features

- **Dynamic Scheduling:** Select your academic year and choose specific courses to include in your calendar.
  
- **Popup Reminders:** Opt for popup reminders before each class for better organization.

- **Customizable Timetables:** Add custom timetables for holidays, mid-semester breaks, and special events.

- **Google Calendar Integration:** Import the generated .ics file into Google Calendar with ease.

## How to Use

1. **Access the Tool:**
   - Visit the [IIITD TimeTable on GoogleCalendar](https://iiitd-tt-on-gcal.streamlit.app/) web application.

2. **On the Landing Page:**
   - Welcome to the tool! Follow the provided instructions to generate your class schedule.

3. **Select Academic Year:**
   - Choose your academic year (First Year, Second Year, Third Year, Fourth Year).

4. **Choose Courses:**
   - Pick specific courses from the selected academic year.

5. **Set Preferences:**
   - Opt for popup reminders and set the time if desired.

6. **Generate Calendar:**
   - Click the "Submit" button to generate the `lectures.ics` file.

7. **Download and Import to Google Calendar:**
   - Download the generated file and follow [these instructions](https://support.google.com/calendar/answer/37118?hl=en&co=GENIE.Platform%3DDesktop) to import it into your Google Calendar.

## Landing Page

The landing page provides a quick overview and instructions on how to use the tool effectively. It introduces users to the purpose of the College Calendar Generator and guides them through the process.

## Detailed Instructions

For more detailed instructions, click the link provided on the landing page or visit [Detailed Instructions](#).

#  Timetable JSON Format

- **Course Name (e.g., "DBMS (Sec A)"):**
  - Each course has a unique identifier which corresponds to the subject name and section (if valid).

- **Attributes:**
  - **name:** Name of the lecture or course.
  - **description:** Instructor or lecturer's name.
  - **start_time:** List of start times for the lecture in the format "DD/MM/YYYY[HH:MM]". Keep the times as dates from maybe first week or current week.
  - **location:** Classroom or location of the lecture.
  - **duration_hours:** Duration of the lecture in hours.
  - **duration_minutes:** Duration of the lecture in minutes.

- **Adding More Courses:**
  - Simply add more entries for each course following the same structure.
 
- **Updating:**
  - Timetable updates can be done manually by modifying the existing JSON file with new details.
  - Consider creating a PDF to JSON converter tool for more automated updates.

## Important Notes

- Ensure that the `tt_till_date` variable is set to a future date.
- The `SEM` variable defines the ongoing semester type (odd/even).
- Customize holiday and event timetables in the `chutti_h_kya` dictionary.
- The script currently supports up to the Second Years' timetable and only contains lectures.

## Troubleshooting

In case of errors, check the provided inputs and configurations. Feel free to customize the script or provide suggestions for improvements.
Feel free to contribute.

Happy scheduling!
