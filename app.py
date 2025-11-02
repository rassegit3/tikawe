import sqlite3
from flask import Flask, redirect, url_for
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import planet, users

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/star/<int:star_id>")
def show_star(star_id):
    star = planet.get_star(star_id)
    planets = planet.get_planets(star_id)


    return render_template("star.html", star=star, planets=planets)

@app.route("/planet/<int:planet_id>")
def show_planet(planet_id):
    planet1  = planet.get_planet(planet_id)
    star_id = planet.getstarforplanet_id(planet_id)["star_id"]
    star_id = int(star_id)
    star  = planet.getstarnamefromid(star_id)
    method_id = planet.getmethodforplanet(planet_id)["method"]
    """ method_id = int(method_id) """
    """ method = planet.getmethodname(method_id)["name"] """
    method = method_id
    types = planet.get_types(planet_id)


    return render_template("planet.html", planet=planet1, star =star, types=types, method = method)


@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/search", methods = ["POST","GET"])
def search():
    starname = request.args.get("starname")
    planetname = request.args.get("planetname")
    planet_id = 0
    star_id = 0

    if request.method == "POST":


        starname = request.form["starname"]
        planetname = request.form["planetname"]

        planets = planet.get_all_planets()
        stars = planet.get_stars()

        if planetname in planets:
            planet_id = planet.findplanets_byname(planetname)[0]
        else:
            planetname = "NoPlanet"

        if starname in stars:
            star_id = planet.findstars_byname(starname)[0]
        else:
            starname = "NoStar"


        if starname == "":
            starname = "NoStar"
        if planetname == "":
            planetname = "NoPlanet"
        return redirect(url_for("results", starname=starname, planetname=planetname, planet_id = planet_id, star_id = star_id))

    else:
        return render_template("search.html", planetname = planetname, starname = starname)


@app.route("/results/<starname>/<planetname>")
def results(starname, planetname):

    if starname != "NoStar":
        stars = planet.findstars_byname(starname)[0]
    else:
        stars = []

    if planetname != "NoPlanet":
        planets = planet.findplanets_byname(planetname)[0]
    else:
        planets = []



    return render_template("results.html",planets=planets,stars=stars)


"""
@app.route("/search_star")
def search_star():
    query = request.args.get("query")
    if query:
        results = items
    return render_template("stars.html", query= query, results=results)


@app.route("/search_planet")
def search_planet():
    query = request.args.get("query")
    if query:
        results = items
    return render_template("planets.html", query= query, results=results)
"""

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    db.execute("INSERT INTO messages (content) VALUES (?)", [content])
    return redirect("/")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return "VIRHE: salasanat eivät täsmää"

        try:
            users.create_user(username, password1)
            return redirect("/")
        except sqlite3.IntegrityError:
            return "VIRHE: tunnus on jo käytössä"





@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"


@app.route("/logout")
def logout():
    # del session["user_id"]
    del session["username"]
    return redirect("/")

@app.route("/modify_star")
def modify_star():
    return render_template("create_star.html")

@app.route("/create_star", methods=["GET", "POST"])
def create_star():
    star_name = request.form["starname"]
    star_content = request.form["starcontent"]
    user_id = session["user_id"]
    planet.add_star(star_name, star_content, user_id)
    return redirect("/")


@app.route("/modify", methods=["GET","POST"])
def modify():
    types = db.query("SELECT name FROM type")
    stars = db.query("SELECT name FROM star")
    methods = db.query("SELECT name FROM method")

    return render_template("/create_planet.html", types=types, stars=stars, methods=methods)


@app.route("/create_planet", methods=["GET", "POST"])
def create_planet():
    planet_name = request.form["planetname"]
    planet_content = request.form["planetcontent"]
    planet_types = request.form.getlist("planettypes")
    print(planet_types)
    planet_star = request.form["planetstar"]
    planet_date = request.form["planetdate"]
    planet_method = request.form["planetmethod"]
    user_id = session["user_id"]

    planet_content = "'" + planet_content + "'"
    sql = "INSERT INTO planet (name, content, discovery, user_id, method) VALUES (?,?,?,?,?)"
    db.execute(sql, [planet_name, planet_content, planet_date, user_id, planet_method])

    sql = ("""SELECT id FROM planet WHERE name = ?""")
    result = db.query(sql, [planet_name])[0]
    planet_id = int(result[0])

    for item in planet_types:
        sql = ("""SELECT id FROM type WHERE name = ?""")
        result = db.query(sql, [item])
        planet_type_id = int(result[0])
        sql = ("INSERT INTO planet_type (planet_id, star_id) VALUES (?,?)")
        db.execute(sql, [planet_type_id, planet_id])


    sql = ("""SELECT id FROM star WHERE name = ?""")
    result = db.query(sql, [planet_star])[0]
    star_id = int(result[0])
    sql = ("INSERT INTO planet_star (planet_id, star_id) VALUES (?,?)")
    db.execute(sql, [planet_id, star_id])

    sql = ("""SELECT id FROM method WHERE name = ?""")
    result = db.query(sql, [planet_method])[0]
    method_id = int(result[0])
    sql = ("INSERT INTO planet_method (planet_id, method_id) VALUES (?,?)")
    db.execute(sql, [planet_id, method_id])







    return redirect("/")


'''

'@app.route("/remove/star")
def remove_star():


@app.route("/remove/planet")
def remove_planet():

'''
@app.route("/ownpage")
def ownpage():

    planets = db.query("SELECT * FROM planet")
    stars = db.query("SELECT * FROM star")
    return render_template("ownpage.html", stars=stars, planets=planets)

@app.route("/planets")
def planets():

    planets = db.query("SELECT * FROM planet")
    stars = db.query("SELECT * FROM star")
    return render_template("planets.html", stars=stars, planets=planets)


@app.route("/removeplanet/<planet_id>", methods = ["GET"])
def removeplanet(planet_id):
    planet.remove_planet(planet_id)
    planets = db.query("SELECT * FROM planet")
    stars = db.query("SELECT * FROM star")
    return render_template("ownpage.html", stars = stars, planets=planets)

@app.route("/removestar/<star_id>", methods = ["GET"])
def removestar(star_id):
    planet.remove_star(star_id)
    planets = db.query("SELECT * FROM planet")
    stars = db.query("SELECT * FROM star")
    return render_template("ownpage.html", stars=stars, planets=planets)



