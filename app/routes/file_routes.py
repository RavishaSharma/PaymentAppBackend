from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import gridfs
from datetime import datetime

# MongoDB connection
connection_string = "mongodb+srv://ravisha23sharma:xWjmqRy8ymJNzyuu@cluster0.xe6ha.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_string)
db = client["payment_app"]
payments_collection = db["payments"]
fs = gridfs.GridFS(db)

file_routes = Blueprint("file_routes", __name__)

from bson import ObjectId  # Import ObjectId for MongoDB ID conversion

@file_routes.route("/upload_evidence", methods=["POST"])
def upload_evidence():
    try:
        # Debugging: Log received data
        print("Form data:", request.form)
        print("Files:", request.files)

        payment_id = request.form.get("payment_id")
        file = request.files.get("file")

        if not payment_id or not file:
            return jsonify({"error": "Payment ID and file are required"}), 400

        # Convert payment_id to ObjectId
        try:
            payment_id = ObjectId(payment_id)
        except Exception:
            return jsonify({"error": "Invalid payment ID format"}), 400

        # Check if the payment exists
        payment = payments_collection.find_one({"_id": payment_id})
        if not payment:
            return jsonify({"error": "Payment not found"}), 404

        # Save the file to GridFS
        file_id = fs.put(file.read(), filename=file.filename, payment_id=str(payment_id))

        # Update payment status to 'completed' and link the file
        payments_collection.update_one(
            {"_id": payment_id},
            {"$set": {"status": "completed", "evidence_file_id": str(file_id)}}
        )

        return jsonify({"message": "File uploaded successfully", "file_id": str(file_id)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@file_routes.route("/download_evidence/<file_id>", methods=["GET"])
def download_evidence(file_id):
    try:
        # Convert file_id to ObjectId and retrieve the file
        file = fs.get(ObjectId(file_id))

        # Return the file content as a downloadable attachment
        return file.read(), 200, {
            "Content-Disposition": f"attachment; filename={file.filename}"
        }
    except Exception as e:
        print("Error:", e)  # Log the error
        return jsonify({"error": "File not found"}), 404
