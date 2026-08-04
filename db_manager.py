import sqlite3
print("DATABASE FILE LOADED")

connection = sqlite3.connect("claims.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS claims (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plant TEXT,
    docket_number TEXT UNIQUE,
    docket_date TEXT,
    notification_number TEXT,
    claim_date TEXT,
    sold_to_party TEXT,
    sold_to_party_name TEXT,
    customer_name TEXT,
    material_code TEXT,
    material_description TEXT,
    serial_number TEXT,
    disposition TEXT,
    re_insp_disposition TEXT,
    defect_description TEXT,
    nbp REAL,
    repl_offer REAL,
    claim_loss REAL,
    wear_percent REAL,
    invoice_number TEXT,
    invoice_date TEXT
)
""")
def insert_claims(df):

    connection = sqlite3.connect("claims.db")
    cursor = connection.cursor()

    inserted = 0
    skipped = 0

    for index, row in df.iterrows():

        cursor.execute("""
        INSERT OR IGNORE INTO claims (
            plant,
            docket_number,
            docket_date,
            notification_number,
            claim_date,
            sold_to_party,
            sold_to_party_name,
            customer_name,
            material_code,
            material_description,
            serial_number,
            disposition,
            re_insp_disposition,
            defect_description,
            nbp,
            repl_offer,
            claim_loss,
            wear_percent,
            invoice_number,
            invoice_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["plant"],
            row["docket_number"],
            row["docket_date"],
            row["notification_number"],
            row["claim_date"],
            row["sold_to_party"],
            row["sold_to_party_name"],
            row["customer_name"],
            row["material_code"],
            row["material_description"],
            row["serial_number"],
            row["disposition"],
            row["re_insp_disposition"],
            row["defect_description"],
            row["nbp"],
            row["repl_offer"],
            row["claim_loss"],
            row["wear_percent"],
            row["invoice_number"],
            row["invoice_date"]
        ))

        if cursor.rowcount == 1:
            inserted += 1
        else:
            skipped += 1

    connection.commit()
    connection.close()

    print("RETURN IS EXECUTING")
    return {
    "total": len(df),
    "inserted": inserted,
    "skipped": skipped
    }
def search_claim(docket_number):

    connection = sqlite3.connect("claims.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM claims
        WHERE docket_number = ?
    """, (docket_number,))

    claim = cursor.fetchone()

    connection.close()

    return claim

def search_customer(customer_name):

    connection = sqlite3.connect("claims.db")
    cursor = connection.cursor()

    cursor.execute("""
      SELECT *
      FROM claims
      WHERE customer_name LIKE ?
      """, ('%' + customer_name + '%',))

    claims = cursor.fetchall()

    connection.close()

    return claims