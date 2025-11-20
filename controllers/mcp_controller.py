from flask import Blueprint, jsonify

# Define el Blueprint
mcp_bp = Blueprint('mcp_bp', __name__)

@mcp_bp.route('/mcp', methods=['GET'])
def mcp_endpoint():
    return jsonify({
        "status": "success",
        "message": "MCP endpoint funcionando"
    })