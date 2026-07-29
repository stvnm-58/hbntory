# CRUD des succursales (branches) - pas encore relié à une route dans app.py
from flask import request, jsonify

from database.db import db
from models.branch import Branch


def get_branches():
    # Liste toutes les succursales
    branches = Branch.query.all()

    return jsonify([
        {"id": branch.id, "name": branch.name, "location": branch.location}
        for branch in branches
    ]), 200

def get_branch(branch_id):
    # Récupère une succursale par id
    branch = Branch.query.get(branch_id)

    if not branch:
        return jsonify({"error": "Branch not found"}), 404

    return jsonify({
        "id": branch_id, "name": branch.name, "location": branch.location
    }), 200

def create_branch():
    # Crée une succursale (name obligatoire, location optionnelle)
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing data"}), 400

    name = data.get("name")
    location = data.get("location")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    branch = Branch(name=name, location=location)

    db.session.add(branch)
    db.session.commit()

    return jsonify({
        "message": "Branch created",
        "branch": {"id": branch.id, "name": branch.name, "location": branch.location}
    }), 201

def update_branch(branch_id):
    # Met à jour une succursale (uniquement les champs fournis)
    branch = Branch.query.get(branch_id)

    if not branch:
        return jsonify({"error": "Branch not found"}), 404

    data = request.get_json()

    if "name" in data:
        branch.name = data["name"]

    if "location" in data:
        branch.location = data["location"]

    db.session.commit()

    return jsonify({"message": "Branch updated"}), 200

def delete_branch(branch_id):
    # Supprime définitivement une succursale
    branch = Branch.query.get(branch_id)

    if not branch:
        return jsonify({"error": "Branch not found"}), 404

    db.session.delete(branch)
    db.session.commit()

    return jsonify({"message": "Branch deleted"}), 200
