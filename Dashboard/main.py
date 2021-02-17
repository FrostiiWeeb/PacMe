from flask import Flask, render_template, request, session
from oauth import Oauth
from discord.ext import commands
import discord

app = Flask(__name__)
app.config["SECRET_KEY"] = "test123"


@app.route("/")
@app.route("/home")
def home():
	return render_template("index.html",discord_url= Oauth.discord_login_url)
	
@app.route("/about")
def about():
	return render_template("test.html")
	
@app.route("/dashboard")
def dashboard():
	f = open('guild.txt', 'r')
	
	g = f.read()
	
	f.close()
	return render_template("dashboard.html", guild_count = g)

@app.route("/login")
def login():
	code = request.args.get("code")

	at = Oauth.get_access_token(code)
	session["token"] = at

	user = Oauth.get_user_json(at)
	user_name, user_id = user.get("username"), user.get("discriminator")

	return f"Success {user_name}#{user_id}"


if __name__ == "__main__":
	app.run(host='pacme.ddns.net',debug=True)
