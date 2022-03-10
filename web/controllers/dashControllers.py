from flask import (render_template,
                    request as req)

def sendDash():
    return render_template('dashboard.html')