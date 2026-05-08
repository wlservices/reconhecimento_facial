from flask import redirect, url_for

def redirect_currect_dashboard(user):
    if user.role == 'Administrador':
        return redirect(url_for("admin.dashboard"))
    elif user.role == 'Supervisor':
        return redirect(url_for("supervisor.dashboard"))
    else:
        return redirect(url_for("employee.dashboard"))