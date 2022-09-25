from flask import Flask, render_template, request
import requests
import smtplib
email = ""
passw = ""
connection = smtplib.SMTP("smtp.gmail.com")
connection.starttls()
connection.login(user=email, password=passw)
reponse = requests.get("https://api.npoint.io/fb2cf9a4606601ff3016")
all_posts = reponse.json()

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def get_blog():
    return render_template("index.html", posts=all_posts)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        name = data['name']
        email = data['email']
        phone = data['phone']
        message = data['message']
        connection.sendmail(from_addr=email,
                            to_addrs=email,
                            msg=f"subject:Contact details\n\nname:{name}\nemail:{email}\nphone:{phone}\nmessage:{message}")
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

@app.route('/post/<int:index>')
def show_post(index):
    requested_post = None
    for blog_post in all_posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
