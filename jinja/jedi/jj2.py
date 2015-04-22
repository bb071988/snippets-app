# Your Jedi name is the first three letters of your last name, followed by the first two letters of your first name. So visiting /jedi/beyonce/knowles should tell you that your Jedi #name is "knobe".

from flask import Flask, render_template


app = Flask(__name__)

def nameEngine(first_name,last_name):
    jedi_name = first_name[:3] + last_name[:2]
    return jedi_name

@app.route("/<first_name>/<last_name>/<int:age>")
def template_test(first_name, last_name,age):
    jedi_name = nameEngine(first_name,last_name)
    print jedi_name

    return render_template('template.html', first_name=first_name, last_name=last_name, 
                          jedi_name=jedi_name,future_age = age+10)

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=8080,debug=True)

    
    