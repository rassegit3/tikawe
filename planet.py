import db







def get_stars():
    sql = """SELECT name FROM star """
    return db.query(sql)[0]

def get_all_planets():
    sql = """SELECT name from planet"""
    return db.query(sql)[0]

def get_star(star_id):
    sql = """SELECT id, name FROM star WHERE id = ?"""
    return db.query(sql, [star_id])[0]

def get_planets(star_id):
    sql = """SELECT id, name, content, discovery, user_id, method FROM planet WHERE id in (select planet_id from planet_star WHERE star_id =  ?)"""
    return db.query(sql, [star_id])

def get_planet(planet_id):
    sql = """SELECT id, name, discovery, method, user_id FROM planet WHERE id = ?"""
    return db.query(sql, [planet_id])[0]

def getstarforplanet_id(planet_id):
    sql = """SELECT star_id FROM planet_star WHERE planet_id = ?"""
    return db.query(sql, [planet_id])[0]

def getstarnamefromid(star_id):
    sql = """SELECT name FROM star WHERE id = ?"""
    return db.query(sql, [star_id])[0]

def getmethodforplanet(planet_id):
    sql = """SELECT method FROM planet WHERE id = ?"""
    result =  db.query(sql, [planet_id])[0]
    return result

def getmethodname(method_id):
    sql = """SELECT name from method WHERE id = ?"""
    return db.query(sql,[method_id])[0]

def get_comments(planet_id):
    sql = "SELECT comment.id, comment.content, comment.user_id, users.username FROM comment, users WHERE comment.user_id = users.id AND " \
          "comment.id in (select comment_id from planet_comment WHERE planet_id =  ?)"
    return db.query(sql, [planet_id])

def get_types(planet_id):
    sql = "SeLECT type.name FROM type LEFT JOIN planet_type ON type.id = planet_type.type_id LEFT JOIN planet ON planet.id = planet_type.planet_id WHERE planet.id = ?"
    return db.query(sql, [planet_id])

def add_planet(name, content, discovery, user_id, star_id, method ):
    sql = "INSERT INTO planet (name, content, discovery, user_id, method) VALUES (?,?, ?, ?, ?)"
    db.execute(sql, [name,content, discovery, user_id, method])
    sql = "SELECT id FROM planet WHERE id = (SELECT max(id) FROM planet)"
    planet_id = db.query(sql)[0]
    sql =  "INSERT INTO planet_star VALUES (?,?)"
    db.execute(sql, [planet_id, star_id])



def update_planet(planet_id, content):
    sql = "UPDATE planet SET content = ? WHERE id = ?"
    db.execute(sql, [content, planet_id])

def remove_planet(planet_id):
    sql = "DELETE from planet WHERE id = ?"
    db.execute(sql, [planet_id])

def add_star(name, content,  user_id):
    sql = "INSERT INTO star (name, user_id, content) VALUES (?,?, ?)"
    db.execute(sql, [name, user_id, content])

def update_star(star_id, content):
    sql = "UPDATE star SET content = ? WHERE id = ?"
    db.execute(sql, [content, star_id])

def remove_star(star_id):
    sql = "SELECT planet_id FROM planet_star WHERE star_id = ?"
    planet_ids = db.query(sql, [star_id])
    for id in planet_ids:
        remove_planet(id[0])
    sql = "DELETE from star WHERE id = ?"
    db.execute(sql, [star_id])


def add_comment(content, user_id, planet_id):
    sql = "INSERT INTO comment (content, user_id) VALUES (?,?)"
    db.execute(sql, [content, user_id])
    sql = "SELECT id FROM comment WHERE id = (SELECT max(id) FROM comment)"
    comment_id = db.query(sql)[0]
    sql = "INSERT INTO planet_comment () VALUES (?,?)"
    db.execute(sql, [planet_id, comment_id])

def remove_comment(comment_id):
    sql = " DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])

def update_comment(comment_id, content):
    sql = "UPDATE comment SET content = ? WHERE id = ?"
    db.execute(sql, [content, comment_id])

def getusername(user_id):
    sql = "SELECT username FROM users WHERE users.id = ?"
    return db.query(sql, [user_id])

def findplanets_byname(query):
    sql = "SELECT id from planet WHERE name LIKE ?"
    return db.query(sql, ["%" + query + "%"])

def findstars_byname(query):
    sql = "SELECT id from star WHERE name LIKE ?"
    return db.query(sql, ["%" + query + "%"])

def findplanetsname_withname(query):
    sql = "SELECT name from planet WHERE name LIKE ?"
    return db.query(sql, ["%" + query + "%"])

def findstarsname_withname(query):
    sql = "SELECT name from star WHERE name LIKE ?"
    return db.query(sql, ["%" + query + "%"])
