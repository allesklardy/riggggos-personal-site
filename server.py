import os

from flask import *
import datetime as dt
import smtplib
# using jinja
app = Flask(__name__)  # name of the current directory
MY_MAIL = "finkbeinerrico.service@gmail.com"
MY_MAIL_PASSWORD = os.environ.get("MY_MAIL_PASSWORD")
SEND_TO_MAIL = "finkbeinerrico@gmail.com"


@app.route("/")
def home():
    current_year = dt.datetime.now().year
    return render_template("index.html", current_year=current_year)


@app.route("/skills/<skill>")
def skill_render_method(skill):
    return render_template("skill.html", skill=skill)


@app.route("/skills")
def skill_overview_render_method():
    return render_template("skill.html", skill="all")


@app.route("/contact", methods=["POST", "GET"])
def contact_render_method():
    if request.method == "GET":
        mode = "get"
        # show the contact form
        return render_template("contact.html", mode=mode)
    else:
        # submit data and show a success/ status message
        if request.form.get("phone_number") == "":
            success = send_email(request.form["name"], request.form["email"], request.form["message"])
        else:
            success = send_email(request.form["name"], request.form["email"], request.form["message"],
                                 phone_number=request.form["phone_number"])
        if success:
            mode = "send"
            return render_template("contact.html", mode=mode)
        else:
            mode = "error"
            return render_template("contact.html", mode=mode)

port = 587
def send_email(name, email, message, **kwargs):
    try:
        with smtplib.SMTP("smtp.gmail.com", port) as connection:  # yahoo: smtp.mail.yahoo.com
            connection.starttls()  # secure communication
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
        # connection.close() no need if in with block
    except Exception as ex:
        print(ex)
        return False
    else:
        return True


if __name__ == "__main__":
    app.run(debug=False)  # Debug mode