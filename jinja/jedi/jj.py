# Your Jedi name is the first three letters of your last name, followed by the first two letters of your first name. So visiting /jedi/beyonce/knowles should tell you that your Jedi #name is "knobe".

# from flask import Flask, render_template


# app = Flask(__name__)

first_name = "bob" # ASK Sam why these don't come through main
last_name = "braico"

#@app.route("/<first_name>/<last_name>")
def nameEngine(first_name,last_name):
    jedi_name = first_name[:3] + last_name[:2]
    return jedi_name

jedi_name = nameEngine(first_name,last_name)

print "First Name: {} Last Name {} Jedi Name: {}".format(first_name, last_name, jedi_name)

# @app.route("/")
# def template_test():
#     return render_template('template.html', first_name, last_name, jedi_name,
#                            my_list=[0,1,2,3,4,5])  #TRIED PASSING HERE

if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=8080)
    first_name = "bob"
    last_name = "braico"
#     print first_name
    
    