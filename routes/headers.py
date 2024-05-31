from flask import Blueprint, request, jsonify
from utils.auth import get_auth_and_cookie, fetch_drn_list, fetch_pallet_summary, check_headers_validity, fetch_upc_data
import requests
from cache import cache

headers_bp = Blueprint('headers_bp', __name__)

@headers_bp.route('/fetch_drn_list', methods=['POST'])
@cache.cached(query_string=True)
def fetch_drn():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    store_number = data.get('store_number')
    store_code = data.get('storeCode')

    if not store_code:
        return jsonify({"error": "storeCode parameter is required"}), 400

    try:
        if not check_headers_validity():
            get_auth_and_cookie(username, password, store_number)
        drn_list = fetch_drn_list(store_code)
        return jsonify(drn_list)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except requests.HTTPError as e:
        return jsonify({"error": f"HTTP error occurred: {e}"}), e.response.status_code
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@headers_bp.route('/fetch_pallet_summary', methods=['POST'])
@cache.cached(query_string=True)
def fetch_pallet():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    store_number = data.get('store_number')
    store_code = data.get('storeCode')
    drn = data.get('drn')

    if not store_code or not drn:
        return jsonify({"error": "storeCode and drn parameters are required"}), 400

    try:
        if not check_headers_validity():
            get_auth_and_cookie(username, password, store_number)
        pallet_summary = fetch_pallet_summary(drn, store_code)
        return jsonify(pallet_summary)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except requests.HTTPError as e:
        return jsonify({"error": f"HTTP error occurred: {e}"}), e.response.status_code
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@headers_bp.route('/fetch_upc_data', methods=['POST'])
@cache.cached(query_string=True)
def fetch_upc_data_route():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    store_number = data.get('store_number')
    upc = data.get('upc')

    if not store_number or not upc:
        return jsonify({"error": "Missing store_number or upc"}), 400

    try:
        if not check_headers_validity():
            get_auth_and_cookie(username, password, store_number)
        upc_data = fetch_upc_data(store_number, upc)
        return jsonify(upc_data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except requests.HTTPError as e:
        return jsonify({"error": f"HTTP error occurred: {e}"}), e.response.status_code
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
