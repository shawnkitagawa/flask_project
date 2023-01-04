# from flask import Flask, render_template, Blueprint, session, request, redirect, url_for



# login= Blueprint("login", __name__, static_folder= "static", template_folder="templates")

# @login.route("/home")
# @login.route("/" ,methods =["POST", "GET"])
# def login():
#     if request.method == "POST":
#         user = request.form["nm"]
#         session["user"] = user
#         return redirect(url_for("user"))
#     else:
#         if "user" in session:
#             return redirect(url_for("user"))
#     return render_template("login.html")


# @login.route("/user")
# def user():
#     if "user" in session:
#         user = session["user"]
#         return f"<h1>{user}</h1>"
#     else:
#         redirect(url_for("login"))


# @login.route("/logout")
# def logout():
#     session.pop("user",None)
#     return redirect(url_for("login"))
