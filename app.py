from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
from boto3.dynamodb.conditions import Key, Attr

app = Flask(__name__)
CORS(app)

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

login_table = dynamodb.Table("login")
music_table = dynamodb.Table("music")
subscriptions_table = dynamodb.Table("subscriptions")


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    result = login_table.get_item(Key={"email": email})
    user = result.get("Item")

    if not user or user.get("password") != password:
        return jsonify({"message": "email or password is invalid"}), 401

    return jsonify({
        "message": "Login successful",
        "email": user["email"],
        "user_name": user["user_name"]
    })


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    user_name = data.get("user_name")
    password = data.get("password")

    existing_user = login_table.get_item(Key={"email": email})

    if "Item" in existing_user:
        return jsonify({"message": "The email already exists"}), 409

    login_table.put_item(Item={
        "email": email,
        "user_name": user_name,
        "password": password
    })

    return jsonify({"message": "Registration successful"})


@app.route("/music", methods=["GET"])
def query_music():
    title = request.args.get("title")
    artist = request.args.get("artist")
    year = request.args.get("year")
    album = request.args.get("album")

    if not title and not artist and not year and not album:
        return jsonify({"message": "At least one field is required", "items": []}), 400

    items = []

    if artist:
        query_args = {
            "KeyConditionExpression": Key("artist").eq(artist)
        }

        filter_exp = None

        if title:
            filter_exp = Attr("title").eq(title)
        if year:
            filter_exp = filter_exp & Attr("year").eq(year) if filter_exp else Attr("year").eq(year)
        if album:
            filter_exp = filter_exp & Attr("album").eq(album) if filter_exp else Attr("album").eq(album)

        if filter_exp:
            query_args["FilterExpression"] = filter_exp

        result = music_table.query(**query_args)
        items = result.get("Items", [])

    elif title:
        result = music_table.query(
            IndexName="title-index",
            KeyConditionExpression=Key("title").eq(title)
        )
        items = result.get("Items", [])

        if year:
            items = [song for song in items if song.get("year") == year]
        if album:
            items = [song for song in items if song.get("album") == album]

    else:
        filter_exp = None

        if year:
            filter_exp = Attr("year").eq(year)
        if album:
            filter_exp = filter_exp & Attr("album").eq(album) if filter_exp else Attr("album").eq(album)

        result = music_table.scan(FilterExpression=filter_exp)
        items = result.get("Items", [])

    if not items:
        return jsonify({
            "message": "No result is retrieved. Please query again",
            "items": []
        })

    return jsonify({
        "message": "Results retrieved",
        "items": items
    })


@app.route("/subscriptions", methods=["GET"])
def get_subscriptions():
    email = request.args.get("email")

    result = subscriptions_table.query(
        KeyConditionExpression=Key("email").eq(email)
    )

    return jsonify({
        "message": "Subscriptions retrieved",
        "items": result.get("Items", [])
    })


@app.route("/subscriptions", methods=["POST"])
def add_subscription():
    data = request.get_json()

    item = {
        "email": data.get("email"),
        "song_key": data.get("song_key"),
        "title": data.get("title"),
        "artist": data.get("artist"),
        "year": data.get("year"),
        "album": data.get("album"),
        "image_url": data.get("image_url")
    }

    subscriptions_table.put_item(Item=item)

    return jsonify({"message": "Subscription added successfully"})


@app.route("/subscriptions", methods=["DELETE"])
def remove_subscription():
    email = request.args.get("email")
    song_key = request.args.get("song_key")

    subscriptions_table.delete_item(
        Key={
            "email": email,
            "song_key": song_key
        }
    )

    return jsonify({"message": "Subscription removed successfully"})


@app.route("/")
def home():
    return "EC2 backend is running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)