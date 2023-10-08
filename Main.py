import json
from ics import Calendar, Event
from datetime import datetime, timedelta
import streamlit as st
    
# dictionary to specify whether a particular day is a holiday or not
chutti_h_kya = {}
chutti_h_kya[datetime.strptime("24/10/2023", "%d/%m/%Y")] = "Dussehra"
chutti_h_kya[datetime.strptime("27/11/2023", "%d/%m/%Y")] = "Guru Nanak Jayanti"

# dictionary to specify whether a particular day has a different timetable or not. if yes, then specify a date of the day of which the timetable is followed.
# (has not yet been integrated in the code)
diff_tt = {}
diff_tt[datetime.strptime("20/11/2023", "%d/%m/%Y")] = datetime.strptime("13/10/2023", "%d/%m/%Y")
diff_tt[datetime.strptime("29/11/2023", "%d/%m/%Y")] = datetime.strptime("12/10/2023", "%d/%m/%Y")

# date till which you want to add timetable to your google calendar. (keep it in the future and preferably before 29/11/2023(that's when the semester ends ))
tt_till_date = datetime.strptime("29/11/2023", "%d/%m/%Y")

# compare datetime objects
def cmp_date(date1, date2):
    if date1.year != date2.year:
        return date1.year - date2.year
    elif date1.month != date2.month:
        return date1.month - date2.month
    else:
        return date1.day - date2.day

def add_weekly_to_calendar(gc, subject, popup, popup_time):
    arr = subject["start_time"]
    for current_date in arr:
        current_date = datetime.strptime(current_date, "%d/%m/%Y[%H:%M]")
        while cmp_date(current_date, tt_till_date) <= 0 :
            try :
                if chutti_h_kya[datetime.strptime(current_date.strftime("%d/%m/%Y"), "%d/%m/%Y")]:
                    current_date += timedelta(days=7)
            except:
                try :
                    if diff_tt[datetime.strptime(current_date.strftime("%d/%m/%Y"), "%d/%m/%Y")]:
                        current_date += timedelta(days=7)
                except:
                    event = Event()
                    event.name = subject["name"]
                    event.begin =  current_date
                    event.duration = {
                        "hours": subject["duration_hours"],
                        "minutes": subject["duration_minutes"]
                    }
                    event.location = subject["location"]
                    event.description = subject["description"]
                    event.begin = event.begin - timedelta(hours=5, minutes=30)
                    if (popup):
                        event.alarms = [{
                            "action": "DISPLAY",
                            "trigger": f"-PT{popup_time.hour}H{popup_time.minute}M{popup_time.second}S"
                        }]
                    gc.events.add(event)
                    current_date += timedelta(days=7)

def main():
    st.title("IIITD Timetable on Google Calendar")
    st.header("Please select your subjects:")

    with open("Schedules/first_year_lectures.json", "r") as f:
        data = json.load(f)

    with open("Schedules/second_year_lectures.json", "r") as f:
        data.update(json.load(f))

    courseNames = data.keys()
    selected_courses = st.multiselect("Select your courses", courseNames)

    popup = st.checkbox('Do you want a popup before the class?')
    if (popup):
        popup_time = st.time_input('How much time before the class should the popup be?', value=None)
        
    proceed = st.button("Proceed")
    
    if (proceed):
        if not popup:
            popup_time = None
        cal = Calendar()
        st.write("Adding courses to calendar...")
        for x in selected_courses:
            add_weekly_to_calendar(cal, data[x], popup, popup_time)
            st.write(f"Added {x} to calendar")
        st.write("Successfully added all courses to calendar")

        temp_filename = "lectures.ics"
        with open(temp_filename, "w") as f:
            f.write("\n".join(cal))

        st.write("Conversion completed. The .ics file has been generated.")

        with open(temp_filename,"r") as f:
            st.download_button("Download .ics File", f, file_name="lectures.ics")
            
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.write("Error:", e)
