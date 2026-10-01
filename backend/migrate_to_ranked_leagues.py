import sqlite3

DATABASE = "instance/counting_stars.db"

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

print("Starting Ranked League migration...")

# Existing application data is preserved.
# Old trophies are NOT deleted. New applications will use league.
columns = [
    row[1]
    for row in cursor.execute(
        "PRAGMA table_info(recruitment_applications)"
    ).fetchall()
]

if "league" not in columns:
    cursor.execute("""
        ALTER TABLE recruitment_applications
        ADD COLUMN league VARCHAR(50)
    """)
    print("Added league to recruitment_applications.")
else:
    print("league already exists in recruitment_applications.")

# Clan settings: add the new minimum league setting.
columns = [
    row[1]
    for row in cursor.execute(
        "PRAGMA table_info(clan_settings)"
    ).fetchall()
]

if "min_league" not in columns:
    cursor.execute("""
        ALTER TABLE clan_settings
        ADD COLUMN min_league VARCHAR(50)
        NOT NULL DEFAULT 'Titan III'
    """)
    print("Added min_league to clan_settings.")
else:
    print("min_league already exists in clan_settings.")

connection.commit()
connection.close()

print()
print("Migration completed successfully.")
print("Old trophy data remains intact for existing applications.")
print("New recruitment workflow uses Ranked League.")
