import streamlit as st
import pandas as pd
import plotly.express as px
from db_manager import (
    insert_claims,
    search_claim,
    search_customer,
    total_claims,
    approved_claims,
    rejected_claims,
    total_claim_loss,
    approval_rate,
    monthly_claims,
    top_customers,
    get_months,
    top_defects
)
from pdf_generator import generate_pdf
from claim_pdf import generate_claim_pdf
# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Tyre Claim Management System",
    page_icon="🚗",
    layout="wide"
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a Page",
    [
        "🏠 Home",
        "📤 Upload Claim Report",
        "🔍 Search Claim",
        "📋 Customer Claim History",
        "📊 Dashboard",
        "ℹ About"
    ]
)

# -----------------------------
# Home Page
# -----------------------------
if page == "🏠 Home":
    st.title("🛞 Tyre Claim Management System")
    st.write(
        """
        Welcome to the Tyre Claim Management System.

        This application helps automate the weekly tyre claim process.

        Features:
        - Upload weekly claim reports
        - Search claims using Docket Number
        - View customer claim details
        - Analytics Dashboard (Coming Soon)
        """
    )

# -----------------------------
# Upload Page
# -----------------------------
elif page == "📤 Upload Claim Report":
    st.header("📤 Upload Weekly Claim Report")
    uploaded_file = st.file_uploader(
        "Choose Claim Report",
        type=["xlsx"]
    )
    if uploaded_file is not None:
        st.success("File uploaded successfully.")
        df = pd.read_excel(uploaded_file)
        df = df.rename(columns={
    "Plant": "plant",
    "Docket Number": "docket_number",
    "Docket Date": "docket_date",
    "Notification Number": "notification_number",
    "Date": "claim_date",
    "Sold-To-Party": "sold_to_party",
    "Sold-To-Party Name": "sold_to_party_name",
    "Customer Name": "customer_name",
    "Material Code": "material_code",
    "Material Description": "material_description",
    "Serial Number": "serial_number",
    "Disposition": "disposition",
    "Re.Insp Disposition": "re_insp_disposition",
    "Re.Insp Defect Code Desc": "defect_description",
    "NBP": "nbp",
    "Repl-Offer": "repl_offer",
    "Claim Loss": "claim_loss",
    "Wear%": "wear_percent",
    "Invoice / CL10": "invoice_number",
    "Invoice/CL10 Date": "invoice_date"
})
        df["docket_date"] = df["docket_date"].astype(str)
        df["claim_date"] = df["claim_date"].astype(str)
        df["invoice_date"] = df["invoice_date"].astype(str)
        df = df.drop_duplicates(subset=["docket_number"])
 
        result = insert_claims(df)
        # st.write(result)
        st.success("Upload Completed Successfully!")
        st.write(f"📄 Total Records : {result['total']}")
        st.write(f"✅ New Records : {result['inserted']}")
        st.write(f"⏭️ Skipped Records : {result['skipped']}")
        st.subheader("📄 File Information")
        col1, col2 = st.columns(2)
        # col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Total Columns", len(df.columns))
            st.subheader("👀 Data Preview")
            st.dataframe(df.head(10))


# -----------------------------
# Search Page
# -----------------------------
elif page == "🔍 Search Claim":
    st.header("🔍 Search Claim")
    docket_number = st.text_input("Enter Docket Number")
    if st.button("Search"):
        claim = search_claim(docket_number)
        if claim:
            st.success("Claim Found!")
            st.subheader("📄 Claim Details")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Docket Number:** {claim[2]}")
                st.write(f"**Customer Name:** {claim[8]}")
                st.write(f"**Material:** {claim[10]}")
                st.write(f"**Defect Description:** {claim[14]}")
                st.write(f"**Serial Number:** {claim[11]}")
            with col2:
                    claim_loss = claim[17]
                    gst = claim_loss * 0.18
                    total_payable = claim_loss + gst

                    st.write(f"**Claim Loss:** ₹{claim_loss:,.2f}")
                    st.write(f"**GST (18%):** ₹{gst:,.2f}")
                    st.write(f"**Total Payable:** ₹{total_payable:,.2f}")
                    st.write(f"**Wear %:** {claim[18]}%")
                    #st.write(f"**Invoice No:** {claim[20]}")
            # Claim Status
            status = claim[12].strip().upper()
            if "ACCEPT" in status:
                st.success("🟢 CLAIM APPROVED")
            elif "REJECT" in status:
                st.error("🔴 CLAIM REJECTED")
            else:
                st.warning(f"Status : {status}")
        else:
            st.error("No Claim Found")
        pdf_file = generate_claim_pdf(claim)

        with open(pdf_file, "rb") as file:
              st.download_button(
               label="📄 Download Claim PDF",
               data=file,
               file_name=pdf_file,
               mime="application/pdf"
               )

# -----------------------------
# Customer Claim History
# -----------------------------
elif page == "📋 Customer Claim History":

    st.header("📋 Customer Claim History")

    customer_name = st.text_input("Enter Customer Name")

    if st.button("Search Customer"):

        claims = search_customer(customer_name)

        if claims:

            st.success(f"{len(claims)} Claim(s) Found")

            columns = [
                "ID",
                "Plant",
                "Docket Number",
                "Docket Date",
                "Notification Number",
                "Claim Date",
                "Sold To Party",
                "Sold To Party Name",
                "Customer Name",
                "Material Code",
                "Material Description",
                "Serial Number",
                "Disposition",
                "Re Insp Disposition",
                "Defect Description",
                "NBP",
               "Replacement Offer",
               "Claim Loss",
               "Wear %",
               "Invoice Number",
                "Invoice Date"
            ]
              
            history_df = pd.DataFrame(claims, columns=columns)

# Calculate Total Payable first
            history_df["Claim Amount"] = (history_df["Claim Loss"] * 1.18).round(2)

# Now select only the required columns
            history_df = history_df[
         [
         "Docket Number",
         "Docket Date",
         "Customer Name",
         "Material Description",
         "Serial Number",
         "Disposition",
         "Defect Description",
         "Wear %",
         "Claim Amount"
          ]
     ]

            st.dataframe(history_df, use_container_width=True)
            data = [history_df.columns.tolist()] + history_df.values.tolist()
            pdf_file = generate_pdf(data, customer_name)
            with open(pdf_file, "rb") as file:
                st.download_button(
                    label="📥 Download PDF",
                    data=file,
                    file_name="Claim_History.pdf",
                    mime="application/pdf"
                  )
            #st.dataframe(history_df, use_container_width=True) (showing two tmes the data)

        else:

            st.error("No Claims Found")
# -----------------------------
# Dashboard
# -----------------------------
    
elif page == "📊 Dashboard":

    st.header("📊 Dashboard")
    months = ["All"] + get_months()
    
    selected_month = st.selectbox(
        "📅 Select Month",
        months
         )
    

    # First Row
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Claims", total_claims(selected_month))

    with col2:
        st.metric("Approved Claims", approved_claims(selected_month))

    with col3:
        st.metric("Rejected Claims", rejected_claims(selected_month))
    
        

# Second Row
    col4, col5 = st.columns(2)

    with col4:
        st.metric(
        "Total Claim Loss",
        f"₹{total_claim_loss(selected_month):,.2f}"
    )

    with col5:
        st.metric(
        "Approval Rate",
        f"{approval_rate(selected_month)}%"
    )

    st.subheader("📈 Monthly Claims Trend")

    chart_data = monthly_claims()

    chart_df = pd.DataFrame(
    chart_data,
    columns=["Month", "Claims"]
      )

    fig = px.bar(
    chart_df,
    x="Month",
    y="Claims",
    text="Claims",
    title=None
      )

    fig.update_traces(textposition="outside")

    fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Number of Claims",
    height=320
      )

    st.plotly_chart(fig, use_container_width=True)
    st.subheader("🏆 Top 10 Customers by Claims")

    customer_data = top_customers(selected_month)
    # st.write(customer_data)
    customer_df = pd.DataFrame(
    customer_data,
    columns=["Customer", "Claims"]
    )

    fig = px.bar(
    customer_df,
    x="Claims",
    y="Customer",
    orientation="h",
    text="Claims",
    title=None
     )

    fig.update_traces(textposition="outside")

    fig.update_layout(
    yaxis=dict(categoryorder="total ascending"),
    height=450,
    xaxis_title="Number of Claims",
    yaxis_title=""
   )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔧 Top 10 Defect Types")

    defect_data = top_defects(selected_month)

    defect_df = pd.DataFrame(
    defect_data,
    columns=["Defect", "Claims"]
    )

    fig = px.bar(
    defect_df,
    x="Claims",
    y="Defect",
    orientation="h",
    text="Claims",
    title=None
     )

    fig.update_traces(textposition="outside")

    fig.update_layout(
    yaxis=dict(categoryorder="total ascending"),
    height=450,
    xaxis_title="Number of Claims",
    yaxis_title=""
      )

    st.plotly_chart(fig, use_container_width=True)

   
# -----------------------------
# About
# -----------------------------
elif page == "ℹ About":

    st.header("About Project")

    st.write(
        """
        Developed using:

        - Python
        - Streamlit
        - Pandas
        - SQLite
        """
    )
    

