import psycopg2
import streamlit as st

print("DATABASE LOADED: SUPABASE")


def get_connection():
    return psycopg2.connect(
        st.secrets["SUPABASE_DB_URL"]
    )


def insert_claims(df):

    connection = get_connection()
    cursor = connection.cursor()

    inserted = 0
    skipped = 0

    for index, row in df.iterrows():

        cursor.execute("""
            INSERT INTO claims (
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
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
            ON CONFLICT (docket_number) DO NOTHING
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
    cursor.close()
    connection.close()

    print("RETURN IS EXECUTING")
    return {
        "total": len(df),
        "inserted": inserted,
        "skipped": skipped
      }


def search_claim(docket_number):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM claims
        WHERE docket_number = %s
    """, (docket_number,))

    claim = cursor.fetchone()

    cursor.close()
    connection.close()

    return claim


def search_customer(customer_name):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM claims
        WHERE customer_name ILIKE %s
    """, ('%' + customer_name + '%',))

    claims = cursor.fetchall()

    cursor.close()
    connection.close()

    return claims


def total_claims(month="All"):

    connection = get_connection()
    cursor = connection.cursor()

    if month == "All":

        cursor.execute("""
            SELECT COUNT(*)
            FROM claims
        """)

    else:

        cursor.execute("""
            SELECT COUNT(*)
            FROM claims
            WHERE SUBSTRING(claim_date, 1, 7) = %s
        """, (month,))

    total = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return total


def approved_claims(month="All"):

    connection = get_connection()
    cursor = connection.cursor()

    if month == "All":

        cursor.execute("""
            SELECT COUNT(*)
            FROM claims
            WHERE UPPER(disposition) LIKE '%ACCEPT%'
        """)

    else:

        cursor.execute("""
            SELECT COUNT(*)
            FROM claims
            WHERE UPPER(disposition) LIKE '%ACCEPT%'
            AND SUBSTRING(claim_date, 1, 7) = %s
        """, (month,))

    total = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return total


def rejected_claims(month="All"):

    connection = get_connection()
    cursor = connection.cursor()

    if month == "All":

        cursor.execute("""
            SELECT COUNT(*)
            FROM claims
            WHERE UPPER(disposition) LIKE '%REJECT%'
        """)

    else:

        cursor.execute("""
            SELECT COUNT(*)
            FROM claims
            WHERE UPPER(disposition) LIKE '%REJECT%'
            AND SUBSTRING(claim_date, 1, 7) = %s
        """, (month,))

    total = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return total


def total_claim_loss(month="All"):

    connection = get_connection()
    cursor = connection.cursor()

    if month == "All":

        cursor.execute("""
            SELECT SUM(claim_loss)
            FROM claims
        """)

    else:

        cursor.execute("""
            SELECT SUM(claim_loss)
            FROM claims
            WHERE SUBSTRING(claim_date, 1, 7) = %s
        """, (month,))

    total = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return total if total else 0


def approval_rate(month="All"):

    total = total_claims(month)
    approved = approved_claims(month)

    if total == 0:
        return 0

    return round((approved / total) * 100, 2)


def monthly_claims():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            SUBSTRING(claim_date, 1, 7) AS month,
            COUNT(*)
        FROM claims
        GROUP BY month
        ORDER BY month
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data


def top_customers(month="All"):

    connection = get_connection()
    cursor = connection.cursor()

    if month == "All":

        cursor.execute("""
            SELECT
                customer_name,
                COUNT(*) AS total_claims
            FROM claims
            GROUP BY customer_name
            ORDER BY total_claims DESC
            LIMIT 10
        """)

    else:

        cursor.execute("""
            SELECT
                customer_name,
                COUNT(*) AS total_claims
            FROM claims
            WHERE SUBSTRING(claim_date, 1, 7) = %s
            GROUP BY customer_name
            ORDER BY total_claims DESC
            LIMIT 10
        """, (month,))

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data


def get_months():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT DISTINCT SUBSTRING(claim_date, 1, 7)
        FROM claims
        ORDER BY 1
    """)

    months = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return months


def top_defects(month="All"):

    connection = get_connection()
    cursor = connection.cursor()

    if month == "All":

        cursor.execute("""
            SELECT
                defect_description,
                COUNT(*) AS total_claims
            FROM claims
            GROUP BY defect_description
            ORDER BY total_claims DESC
            LIMIT 10
        """)

    else:

        cursor.execute("""
            SELECT
                defect_description,
                COUNT(*) AS total_claims
            FROM claims
            WHERE SUBSTRING(claim_date, 1, 7) = %s
            GROUP BY defect_description
            ORDER BY total_claims DESC
            LIMIT 10
        """, (month,))

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data
    