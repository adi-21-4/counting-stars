import os
from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required
)
from dotenv import load_dotenv

from models import (
    db,
    AdminUser,
    AdminRequest,
    RecruitmentApplication,
    Announcement,
    ClanSettings
)

from services.clash_api import (
    get_clan,
    get_current_war,
    get_war_log
)


load_dotenv()


# --------------------------------------------------
# APP
# --------------------------------------------------

app = Flask(__name__)

CORS(app)


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///counting_stars.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# --------------------------------------------------
# JWT
# --------------------------------------------------

app.config["JWT_SECRET_KEY"] = os.getenv(
    "JWT_SECRET_KEY"
)

if not app.config["JWT_SECRET_KEY"]:
    raise RuntimeError(
        "JWT_SECRET_KEY is not configured in .env"
    )


db.init_app(app)
jwt = JWTManager(app)


# --------------------------------------------------
# CLAN
# --------------------------------------------------

CLAN_TAG = "#29QCLVURL"


# --------------------------------------------------
# ADMIN HELPER
# --------------------------------------------------

def admin_required():
    """
    Returns True when the current JWT belongs to either
    a Leader or Co-Leader.
    """

    claims = get_jwt()

    role = claims.get("role")

    return role in ["leader", "co_leader"]

def get_or_create_clan_settings():
    settings = ClanSettings.query.first()

    if not settings:
        settings = ClanSettings(
            min_town_hall=15,
            min_league="PEKKA I",
            war_participation_required=True,
            minimum_donations=1000,
            recruitment_open=True,
            rules=(
                "Respect all clan members.\n"
                "Use attacks during war.\n"
                "Follow clan leadership instructions."
            ),
            recruitment_requirements=(
                "Minimum Town Hall: 15\n"
                "Minimum Ranked League: PEKKA I\n"
                "Regular war participation required."
            )
        )

        db.session.add(settings)
        db.session.commit()

    return settings

# --------------------------------------------------
# DATABASE INITIALIZATION
# --------------------------------------------------

with app.app_context():
    db.create_all()


# --------------------------------------------------
# HEALTH
# --------------------------------------------------

@app.route("/api/health")
def health():

    return jsonify({
        "status": "online",
        "service": "Counting Stars API"
    }), 200


# --------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------

@app.route("/api/auth/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:

        return jsonify({
            "success": False,
            "error": "Username and password are required"
        }), 400


    user = AdminUser.query.filter_by(
        username=username
    ).first()


    if not user or not user.check_password(password):

        return jsonify({
            "success": False,
            "error": "Invalid username or password"
        }), 401


    # Both Leader and Co-Leader are full admins.
    if user.role not in ["leader", "co_leader"]:

        return jsonify({
            "success": False,
            "error": "Admin access denied"
        }), 403


    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "username": user.username,
            "role": user.role
        }
    )


    return jsonify({
        "success": True,
        "token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    }), 200


@app.route("/api/auth/me")
@jwt_required()
def current_user():

    if not admin_required():

        return jsonify({
            "success": False,
            "error": "Admin access required"
        }), 403


    user_id = get_jwt_identity()


    user = db.session.get(
        AdminUser,
        int(user_id)
    )


    if not user:

        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404


    return jsonify({
        "success": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    }), 200


# --------------------------------------------------
# CREATE FIRST ADMIN
# --------------------------------------------------

@app.route("/api/auth/setup", methods=["POST"])
def setup_admin():

    # Don't allow setup after an admin already exists.
    existing_admin = AdminUser.query.first()


    if existing_admin:

        return jsonify({
            "success": False,
            "error": "Admin setup has already been completed"
        }), 403


    data = request.get_json(silent=True) or {}

    username = data.get("username", "").strip()
    password = data.get("password", "")
    role = data.get("role", "leader")


    if not username or not password:

        return jsonify({
            "success": False,
            "error": "Username and password are required"
        }), 400


    if role not in ["leader", "co_leader"]:

        return jsonify({
            "success": False,
            "error": "Role must be leader or co_leader"
        }), 400


    if len(password) < 8:

        return jsonify({
            "success": False,
            "error": "Password must contain at least 8 characters"
        }), 400


    user = AdminUser(
        username=username,
        role=role
    )


    user.set_password(password)

    db.session.add(user)
    db.session.commit()


    return jsonify({
        "success": True,
        "message": "Admin account created successfully"
    }), 201


# --------------------------------------------------
# ADMIN REGISTRATION REQUEST
# --------------------------------------------------

@app.route("/api/auth/register", methods=["POST"])
def register_admin_request():

    data = request.get_json(silent=True) or {}

    username = str(
        data.get("username", "")
    ).strip()

    password = data.get(
        "password",
        ""
    )

    reason = str(
        data.get("reason", "")
    ).strip()

    # Public registration can only request Co-Leader.
    requested_role = "co_leader"

    if not username or not password or not reason:

        return jsonify({
            "success": False,
            "error": "Username, password and reason are required"
        }), 400

    if len(username) < 3 or len(username) > 50:

        return jsonify({
            "success": False,
            "error": "Username must be between 3 and 50 characters"
        }), 400

    if len(password) < 8:

        return jsonify({
            "success": False,
            "error": "Password must contain at least 8 characters"
        }), 400

    existing_admin = AdminUser.query.filter_by(
        username=username
    ).first()

    if existing_admin:

        return jsonify({
            "success": False,
            "error": "An admin account with this username already exists"
        }), 409

    existing_request = AdminRequest.query.filter_by(
        username=username
    ).first()

    if existing_request:

        if existing_request.status == "pending":

            return jsonify({
                "success": False,
                "error": "A registration request for this username is already pending"
            }), 409

        if existing_request.status == "rejected":

            db.session.delete(existing_request)
            db.session.flush()

    admin_request = AdminRequest(
        username=username,
        requested_role=requested_role,
        reason=reason,
        status="pending"
    )

    admin_request.set_password(password)

    db.session.add(admin_request)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Admin registration request submitted successfully"
    }), 201


# --------------------------------------------------
# CLAN API
# --------------------------------------------------

@app.route("/api/clan")
def clan():

    status_code, data = get_clan(CLAN_TAG)


    if status_code != 200:

        return jsonify({
            "success": False,
            "error": data
        }), status_code


    return jsonify({
        "success": True,
        "data": data
    }), 200

@app.route("/api/clan-settings")
def clan_settings():
    settings = get_or_create_clan_settings()

    return jsonify({
        "success": True,
        "settings": {
            "minTownHall": settings.min_town_hall,
            "minLeague": settings.min_league,
            "warParticipationRequired": settings.war_participation_required,
            "minimumDonations": settings.minimum_donations,
            "recruitmentOpen": settings.recruitment_open,
            "rules": settings.rules,
            "recruitmentRequirements": settings.recruitment_requirements,
            "updatedAt": (
                settings.updated_at.isoformat()
                if settings.updated_at
                else None
            ),
            "updatedBy": settings.updated_by
        }
    }), 200

@app.route("/api/admin/clan-settings")
@jwt_required()
def get_admin_clan_settings():
    if not admin_required():
        return jsonify({
            "success": False,
            "error": "Admin access required"
        }), 403

    settings = get_or_create_clan_settings()

    return jsonify({
        "success": True,
        "settings": {
            "id": settings.id,
            "minTownHall": settings.min_town_hall,
            "minLeague": settings.min_league,
            "warParticipationRequired": settings.war_participation_required,
            "minimumDonations": settings.minimum_donations,
            "recruitmentOpen": settings.recruitment_open,
            "rules": settings.rules,
            "recruitmentRequirements": settings.recruitment_requirements,
            "updatedAt": (
                settings.updated_at.isoformat()
                if settings.updated_at
                else None
            ),
            "updatedBy": settings.updated_by
        }
    }), 200

@app.route(
    "/api/admin/clan-settings",
    methods=["PATCH"]
)
@jwt_required()
def update_clan_settings():
    if not admin_required():
        return jsonify({
            "success": False,
            "error": "Admin access required"
        }), 403

    settings = get_or_create_clan_settings()
    data = request.get_json(silent=True) or {}

    if "minTownHall" in data:
        try:
            min_town_hall = int(data["minTownHall"])
        except (TypeError, ValueError):
            return jsonify({
                "success": False,
                "error": "Minimum Town Hall must be a number"
            }), 400

        if min_town_hall < 1 or min_town_hall > 18:
            return jsonify({
                "success": False,
                "error": "Invalid minimum Town Hall"
            }), 400

        settings.min_town_hall = min_town_hall

    if "minLeague" in data:
        min_league = str(data["minLeague"]).strip()

        allowed_leagues = [
            "Skeleton 1", "Skeleton 2", "Skeleton 3",
            "Barbarian 4", "Barbarian 5", "Barbarian 6",
            "Archer 7", "Archer 8", "Archer 9",
            "Wizard 10", "Wizard 11", "Wizard 12",
            "Valkyrie 13", "Valkyrie 14", "Valkyrie 15",
            "Witch 16", "Witch 17", "Witch 18",
            "Golem 19", "Golem 20", "Golem 21",
            "P.E.K.K.A 22", "P.E.K.K.A 23", "P.E.K.K.A 24",
            "Titan 25", "Titan 26", "Titan 27",
            "Dragon 28", "Dragon 29", "Dragon 30",
            "Electro 31", "Electro 32", "Electro 33",
            "Legend 3", "Legend 2", "Legend 1"
        ]

        legacy_to_canonical = {
            "Skeleton I": "Skeleton 1", "Skeleton II": "Skeleton 2", "Skeleton III": "Skeleton 3",
            "Barbarian I": "Barbarian 4", "Barbarian II": "Barbarian 5", "Barbarian III": "Barbarian 6",
            "Archer I": "Archer 7", "Archer II": "Archer 8", "Archer III": "Archer 9",
            "Wizard I": "Wizard 10", "Wizard II": "Wizard 11", "Wizard III": "Wizard 12",
            "Valkyrie I": "Valkyrie 13", "Valkyrie II": "Valkyrie 14", "Valkyrie III": "Valkyrie 15",
            "Witch I": "Witch 16", "Witch II": "Witch 17", "Witch III": "Witch 18",
            "Golem I": "Golem 19", "Golem II": "Golem 20", "Golem III": "Golem 21",
            "P.E.K.K.A I": "P.E.K.K.A 22", "P.E.K.K.A II": "P.E.K.K.A 23", "P.E.K.K.A III": "P.E.K.K.A 24",
            "Titan I": "Titan 25", "Titan II": "Titan 26", "Titan III": "Titan 27",
            "Dragon I": "Dragon 28", "Dragon II": "Dragon 29", "Dragon III": "Dragon 30",
            "Electro I": "Electro 31", "Electro II": "Electro 32", "Electro III": "Electro 33",
            "Legend III": "Legend 3", "Legend II": "Legend 2", "Legend I": "Legend 1"
        }

        min_league = legacy_to_canonical.get(min_league, min_league)

        if min_league not in allowed_leagues:
            return jsonify({
                "success": False,
                "error": "Invalid minimum Ranked League"
            }), 400

        settings.min_league = min_league

    if "warParticipationRequired" in data:
        settings.war_participation_required = bool(
            data["warParticipationRequired"]
        )

    if "minimumDonations" in data:
        try:
            minimum_donations = int(data["minimumDonations"])
        except (TypeError, ValueError):
            return jsonify({
                "success": False,
                "error": "Minimum donations must be a number"
            }), 400

        if minimum_donations < 0:
            return jsonify({
                "success": False,
                "error": "Minimum donations cannot be negative"
            }), 400

        settings.minimum_donations = minimum_donations

    if "recruitmentOpen" in data:
        settings.recruitment_open = bool(
            data["recruitmentOpen"]
        )

    if "rules" in data:
        settings.rules = str(
            data["rules"]
        ).strip()

    if "recruitmentRequirements" in data:
        settings.recruitment_requirements = str(
            data["recruitmentRequirements"]
        ).strip()

    claims = get_jwt()

    settings.updated_by = claims.get("username")
    settings.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Clan settings updated successfully",
        "settings": {
            "minTownHall": settings.min_town_hall,
            "minLeague": settings.min_league,
            "warParticipationRequired": settings.war_participation_required,
            "minimumDonations": settings.minimum_donations,
            "recruitmentOpen": settings.recruitment_open,
            "rules": settings.rules,
            "recruitmentRequirements": settings.recruitment_requirements,
            "updatedAt": (
                settings.updated_at.isoformat()
                if settings.updated_at
                else None
            ),
            "updatedBy": settings.updated_by
        }
    }), 200

@app.route("/api/members")
def members():

    status_code, data = get_clan(CLAN_TAG)


    if status_code != 200:

        return jsonify({
            "success": False,
            "error": data
        }), status_code


    return jsonify({
        "success": True,
        "data": data.get("memberList", [])
    }), 200


@app.route("/api/current-war")
def current_war():

    status_code, data = get_current_war(CLAN_TAG)


    if status_code != 200:

        return jsonify({
            "success": False,
            "error": data
        }), status_code


    return jsonify({
        "success": True,
        "data": data
    }), 200


@app.route("/api/war-log")
def war_log():

    status_code, data = get_war_log(CLAN_TAG)


    if status_code != 200:

        return jsonify({
            "success": False,
            "error": data
        }), status_code


    return jsonify({
        "success": True,
        "data": data
    }), 200


# --------------------------------------------------
# PUBLIC ANNOUNCEMENTS
# --------------------------------------------------

@app.route("/api/announcements")
def get_announcements():

    announcements = Announcement.query.filter_by(
        is_published=True
    ).order_by(
        Announcement.created_at.desc()
    ).all()


    return jsonify({
        "success": True,
        "announcements": [
            {
                "id": announcement.id,
                "title": announcement.title,
                "content": announcement.content,
                "category": announcement.category,
                "createdAt": (
                    announcement.created_at.isoformat()
                    if announcement.created_at
                    else None
                ),
                "updatedAt": (
                    announcement.updated_at.isoformat()
                    if announcement.updated_at
                    else None
                )
            }

            for announcement in announcements
        ]
    }), 200


# --------------------------------------------------
# RECRUITMENT
# --------------------------------------------------

@app.route("/api/applications", methods=["POST"])
def create_application():

    data = request.get_json(silent=True) or {}


    required_fields = [
        "playerName",
        "playerTag",
        "townHallLevel",
        "league",
        "age",
        "reason"
    ]


    for field in required_fields:

        if data.get(field) in [None, ""]:

            return jsonify({
                "success": False,
                "error": f"{field} is required"
            }), 400


    try:

        town_hall_level = int(
            data["townHallLevel"]
        )

        age = int(
            data["age"]
        )

    except (TypeError, ValueError):

        return jsonify({
            "success": False,
            "error": "Town Hall and age must be numbers"
        }), 400


    if town_hall_level < 1 or town_hall_level > 18:

        return jsonify({
            "success": False,
            "error": "Invalid Town Hall level"
        }), 400


    if age < 13:

        return jsonify({
            "success": False,
            "error": "Applicant must be at least 13 years old"
        }), 400


    application = RecruitmentApplication(

        player_name=str(
            data["playerName"]
        ).strip(),

        player_tag=str(
            data["playerTag"]
        ).strip(),

        town_hall_level=town_hall_level,

        league=str(
            data["league"]
        ).strip(),

        age=age,

        discord=str(
            data.get("discord", "")
        ).strip(),

        reason=str(
            data["reason"]
        ).strip(),

        status="pending"
    )


    db.session.add(application)
    db.session.commit()


    return jsonify({
        "success": True,
        "message": "Application submitted successfully",
        "application": {
            "id": application.id,
            "status": application.status
        }
    }), 201


# --------------------------------------------------
# ADMIN APPLICATIONS
# --------------------------------------------------

@app.route("/api/admin/applications")
@jwt_required()
def get_applications():

    if not admin_required():

        return jsonify({
            "success": False,
            "error": "Admin access required"
        }), 403


    applications = RecruitmentApplication.query.order_by(
        RecruitmentApplication.created_at.desc()
    ).all()


    return jsonify({
        "success": True,
        "applications": [

            {
                "id": application.id,

                "playerName": application.player_name,

                "playerTag": application.player_tag,

                "townHallLevel": application.town_hall_level,

                "league": application.league,

                "age": application.age,

                "discord": application.discord,

                "reason": application.reason,

                "status": application.status,

                "createdAt": (
                    application.created_at.isoformat()
                    if application.created_at
                    else None
                ),

                "reviewedAt": (
                    application.reviewed_at.isoformat()
                    if application.reviewed_at
                    else None
                ),

                "reviewedBy": application.reviewed_by
            }

            for application in applications
        ]
    }), 200


# --------------------------------------------------
# UPDATE APPLICATION STATUS
# --------------------------------------------------

@app.route(
    "/api/admin/applications/<int:application_id>",
    methods=["PATCH"]
)
@jwt_required()
def update_application(application_id):

    if not admin_required():

        return jsonify({
            "success": False,
            "error": "Admin access required"
        }), 403


    application = db.session.get(
        RecruitmentApplication,
        application_id
    )


    if not application:

        return jsonify({
            "success": False,
            "error": "Application not found"
        }), 404


    data = request.get_json(silent=True) or {}

    status = data.get("status")


    if status not in [
        "pending",
        "approved",
        "rejected"
    ]:

        return jsonify({
            "success": False,
            "error": "Invalid application status"
        }), 400


    claims = get_jwt()


    application.status = status

    application.reviewed_at = datetime.utcnow()

    application.reviewed_by = claims.get(
        "username"
    )


    db.session.commit()


    return jsonify({
        "success": True,
        "message": "Application updated successfully",
        "application": {
            "id": application.id,
            "status": application.status,
            "reviewedBy": application.reviewed_by
        }
    }), 200


# --------------------------------------------------
# ADMIN REQUESTS
# --------------------------------------------------

@app.route("/api/admin/requests")
@jwt_required()
def get_admin_requests():

    if not admin_required():

        return jsonify({
            "success": False,
            "error": "Admin access required"
        }), 403

    requests = AdminRequest.query.order_by(
        AdminRequest.created_at.desc()
    ).all()

    return jsonify({
        "success": True,
        "requests": [
            {
                "id": item.id,
                "username": item.username,
                "requestedRole": item.requested_role,
                "reason": item.reason,
                "status": item.status,
                "createdAt": (
                    item.created_at.isoformat()
                    if item.created_at
                    else None
                ),
                "reviewedAt": (
                    item.reviewed_at.isoformat()
                    if item.reviewed_at
                    else None
                ),
                "reviewedBy": item.reviewed_by
            }
            for item in requests
        ]
    }), 200


@app.route(
    "/api/admin/requests/<int:request_id>",
    methods=["PATCH"]
)
@jwt_required()
def review_admin_request(request_id):

    if not admin_required():

        return jsonify({
            "success": False,
            "error": "Admin access required"
        }), 403

    admin_request = db.session.get(
        AdminRequest,
        request_id
    )

    if not admin_request:

        return jsonify({
            "success": False,
            "error": "Admin request not found"
        }), 404

    if admin_request.status != "pending":

        return jsonify({
            "success": False,
            "error": "This request has already been reviewed"
        }), 400

    data = request.get_json(silent=True) or {}

    status = data.get("status")

    if status not in ["approved", "rejected"]:

        return jsonify({
            "success": False,
            "error": "Status must be approved or rejected"
        }), 400

    claims = get_jwt()

    if status == "approved":

        existing_admin = AdminUser.query.filter_by(
            username=admin_request.username
        ).first()

        if existing_admin:

            return jsonify({
                "success": False,
                "error": "An admin with this username already exists"
            }), 409

        new_admin = AdminUser(
            username=admin_request.username,
            role=admin_request.requested_role
        )

        new_admin.password_hash = admin_request.password_hash

        db.session.add(new_admin)

    admin_request.status = status
    admin_request.reviewed_at = datetime.utcnow()
    admin_request.reviewed_by = claims.get("username")

    db.session.commit()

    return jsonify({
        "success": True,
        "message": (
            "Admin request approved"
            if status == "approved"
            else "Admin request rejected"
        )
    }), 200


# --------------------------------------------------
# ADMIN ANNOUNCEMENTS
# --------------------------------------------------

@app.route("/api/admin/announcements")
@jwt_required()
def get_admin_announcements():

    if not admin_required():

        return jsonify({
            "success": False,
            "error": "Admin access required"
        }), 403


    announcements = Announcement.query.order_by(
        Announcement.created_at.desc()
    ).all()


    return jsonify({
        "success": True,
        "announcements": [

            {
                "id": announcement.id,

                "title": announcement.title,

                "content": announcement.content,

                "category": announcement.category,

                "isPublished": announcement.is_published,

                "createdAt": (
                    announcement.created_at.isoformat()
                    if announcement.created_at
                    else None
                ),

                "updatedAt": (
                    announcement.updated_at.isoformat()
                    if announcement.updated_at
                    else None
                ),

                "createdBy": announcement.created_by
            }

            for announcement in announcements
        ]
    }), 200


@app.route(
    "/api/admin/announcements",
    methods=["POST"]
)
@jwt_required()
def create_announcement():

    if not admin_required():

        return jsonify({
            "success": False,
            "error": "Admin access required"
        }), 403


    data = request.get_json(silent=True) or {}


    title = str(
        data.get("title", "")
    ).strip()


    content = str(
        data.get("content", "")
    ).strip()


    category = str(
        data.get("category", "general")
    ).strip().lower()


    is_published = data.get(
        "isPublished",
        True
    )


    if not title:

        return jsonify({
            "success": False,
            "error": "Title is required"
        }), 400


    if not content:

        return jsonify({
            "success": False,
            "error": "Content is required"
        }), 400


    allowed_categories = [
        "general",
        "war",
        "cwl",
        "recruitment",
        "event",
        "important"
    ]


    if category not in allowed_categories:

        return jsonify({
            "success": False,
            "error": "Invalid announcement category"
        }), 400


    claims = get_jwt()


    announcement = Announcement(

        title=title,

        content=content,

        category=category,

        is_published=bool(
            is_published
        ),

        created_by=claims.get(
            "username"
        )
    )


    db.session.add(announcement)

    db.session.commit()


    return jsonify({
        "success": True,
        "message": "Announcement created successfully",

        "announcement": {

            "id": announcement.id,

            "title": announcement.title,

            "content": announcement.content,

            "category": announcement.category,

            "isPublished": announcement.is_published
        }

    }), 201


@app.route(
    "/api/admin/announcements/<int:announcement_id>",
    methods=["PATCH"]
)
@jwt_required()
def update_announcement(announcement_id):

    if not admin_required():

        return jsonify({
            "success": False,
            "error": "Admin access required"
        }), 403


    announcement = db.session.get(
        Announcement,
        announcement_id
    )


    if not announcement:

        return jsonify({
            "success": False,
            "error": "Announcement not found"
        }), 404


    data = request.get_json(silent=True) or {}


    if "title" in data:

        title = str(
            data["title"]
        ).strip()


        if not title:

            return jsonify({
                "success": False,
                "error": "Title cannot be empty"
            }), 400


        announcement.title = title


    if "content" in data:

        content = str(
            data["content"]
        ).strip()


        if not content:

            return jsonify({
                "success": False,
                "error": "Content cannot be empty"
            }), 400


        announcement.content = content


    if "category" in data:

        category = str(
            data["category"]
        ).strip().lower()


        allowed_categories = [
            "general",
            "war",
            "cwl",
            "recruitment",
            "event",
            "important"
        ]


        if category not in allowed_categories:

            return jsonify({
                "success": False,
                "error": "Invalid announcement category"
            }), 400


        announcement.category = category


    if "isPublished" in data:

        announcement.is_published = bool(
            data["isPublished"]
        )


    db.session.commit()


    return jsonify({
        "success": True,
        "message": "Announcement updated successfully"
    }), 200


@app.route(
    "/api/admin/announcements/<int:announcement_id>",
    methods=["DELETE"]
)
@jwt_required()
def delete_announcement(announcement_id):

    if not admin_required():

        return jsonify({
            "success": False,
            "error": "Admin access required"
        }), 403


    announcement = db.session.get(
        Announcement,
        announcement_id
    )


    if not announcement:

        return jsonify({
            "success": False,
            "error": "Announcement not found"
        }), 404


    db.session.delete(announcement)

    db.session.commit()


    return jsonify({
        "success": True,
        "message": "Announcement deleted successfully"
    }), 200


# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )