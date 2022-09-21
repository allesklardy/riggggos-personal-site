from multiprocessing.forkserver import connect_to_new_process
import os
from sqlite3 import connect
from flask import *
import datetime as dt
from dateutil import relativedelta
import smtplib
# using jinja
app = Flask(__name__)  # name of the current directory
MY_MAIL = "finkbeinerrico.service@yahoo.com"
MY_MAIL_PASSWORD = os.environ.get("MY_MAIL_PASSWORD")
SEND_TO_MAIL = "finkbeinerrico@gmail.com"
MY_BIRTHDAY = dt.datetime(2003, 9, 2)


@app.route("/website1")
def home():
    current_date = dt.datetime.now()
    current_year = current_date.year
    my_age = relativedelta.relativedelta(current_date, MY_BIRTHDAY).years

    return render_template("index.html", current_year=current_year, my_age=my_age)


@app.route("/website1/skills")
def skill_overview_render_method():
    return render_template("skill.html", skill="all", current_year=dt.datetime.now().year)


@app.route("/website1/contact", methods=["POST", "GET"])
def contact_render_method():
    if request.method == "GET":
        mode = "get"
        # show the contact form
        return render_template("contact.html", mode=mode, current_year=dt.datetime.now().year)
    else:
        # submit data and show a success/ status message
        if request.form.get("phone_number") == "":
            success = send_email(request.form["name"], request.form["email"], request.form["message"])
        else:
            success = send_email(request.form["name"], request.form["email"], request.form["message"],
                                 phone_number=request.form["phone_number"])
        if success:
            mode = "send"
            return render_template("contact.html", mode=mode, current_year=dt.datetime.now().year)
        else:
            mode = "error"
            return render_template("contact.html", mode=mode, current_year=dt.datetime.now().year)

port = 587
def send_email(name, email, message, **kwargs):
    try:
        with smtplib.SMTP("smtp.mail.yahoo.com", port) as connection:  # yahoo: smtp.mail.yahoo.com
            # secure communication
            connection.set_debuglevel(1)
            connection.starttls()
            connection.login(user=MY_MAIL, password=MY_MAIL_PASSWORD)
            phone_number = kwargs.get("phone_number", "-")
            current_date = dt.datetime.now()
            body = f"Message from: \"{name}\" (email: {email}, phone: {phone_number})\n\n" \
                   f"Message: \n\n{message}\n\n" \
                   f"{ current_date.strftime('%d.%m.%Y %H:%M')}"
            subject = "New Message from your website"
            connection.sendmail(from_addr=MY_MAIL,
                                to_addrs=SEND_TO_MAIL,
                                msg=f"Subject:{subject}\n\n{body}")
        # connection.close() no need when using with block
    except Exception as ex:
        print(ex)
        return False
    else:
        return True


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=4000)  # Debug mode