from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId  # Import ObjectId from bson

# MongoDB connection
connection_string = "mongodb+srv://ravisha23sharma:xWjmqRy8ymJNzyuu@cluster0.xe6ha.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_string)
db = client["payment_app"]
payments_collection = db["payments"]

payment_routes = Blueprint("payment_routes", __name__)

@payment_routes.route("/get_payments", methods=["GET"])
def get_payments():
    try:
        # Fetch and process payments
        filters = request.args.to_dict()
        payments = payments_collection.find(filters)
        
        # Update statuses and calculate total_due
        updated_payments = []
        for payment in payments:
            # Convert ObjectId to string
            payment["_id"] = str(payment["_id"])

            # Process payment status
            due_date = datetime.strptime(payment["payee_due_date"], "%Y-%m-%d")
            today = datetime.now()
            if due_date.date() == today.date():
                payment["payee_payment_status"] = "due_now"
            elif due_date.date() < today.date():
                payment["payee_payment_status"] = "overdue"

            # Calculate total_due
            discount = payment.get("discount_percent", 0)
            tax = payment.get("tax_percent", 0)
            due_amount = payment.get("due_amount", 0)
            payment["total_due"] = due_amount * (1 - discount / 100) * (1 + tax / 100)

            updated_payments.append(payment)

        return jsonify(updated_payments), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@payment_routes.route("/create_payment", methods=["POST"])
def create_payment():
    try:
        data = request.json
        result = payments_collection.insert_one(data)
        return jsonify({"message": "Payment created successfully", "id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@payment_routes.route("/update_payment", methods=["PUT"])
def update_payment():
    try:
        # Get the `_id` and convert it to ObjectId
        payment_id = request.json.get("_id")
        if not payment_id:
            return jsonify({"error": "_id is required"}), 400

        # Convert `_id` string to ObjectId
        try:
            payment_id = ObjectId(payment_id)
        except Exception:
            return jsonify({"error": "Invalid _id format"}), 400

        # Get the fields to update
        updates = request.json
        del updates["_id"]  # Remove `_id` from the update payload if it exists

        # Perform the update
        result = payments_collection.update_one({"_id": payment_id}, {"$set": updates})
        if result.matched_count == 0:
            return jsonify({"error": "Payment not found"}), 404

        return jsonify({"message": "Payment updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@payment_routes.route("/delete_payment/<payment_id>", methods=["DELETE"])
def delete_payment(payment_id):
    try:
        # Convert string `payment_id` to ObjectId
        try:
            payment_id = ObjectId(payment_id)
        except Exception:
            return jsonify({"error": "Invalid payment_id format"}), 400

        # Perform the delete operation
        result = payments_collection.delete_one({"_id": payment_id})
        if result.deleted_count == 0:
            return jsonify({"error": "Payment not found"}), 404

        return jsonify({"message": "Payment deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
