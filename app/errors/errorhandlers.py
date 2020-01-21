from flask import jsonify

def page_not_found(e):
    return jsonify({'status':404, 'error_message':'The resorse wasn\'t found'}), 404

def page_is_forbidden(e):
    return jsonify({'status':403, 'error_message':'unauthorised to access the resource'}), 403

def httpmethod_not_allowed(e):
    return jsonify({'status':405, 'error_message':'The http method is not allowed'}), 405

def page_was_deleted(e):
    return jsonify({'status':410, 'error_message':'The resource was deleted'}), 410

def server_error(e):
    return jsonify({'status':500, 'error_message':'The server has some issues'}), 500
