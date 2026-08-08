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
st.markdown("""
<style>

/* Move entire page content upward */
.block-container{
    padding-top: 1rem;
    padding-bottom: 2rem;
}

/* Reduce gap below page title */
h1{
    margin-bottom:0.2rem !important;
}

/* Reduce paragraph spacing */
p{
    margin-bottom:0.5rem !important;
}

</style>
""", unsafe_allow_html=True)



if "page" not in st.session_state:
    st.session_state.page = "Home"
with st.sidebar:

    st.sidebar.image("assets/ceat_logo.png", width=200)
    st.sidebar.markdown(
      """
      <p style="
       text-align:center;
       color:#0B5CAD;
      font-size:19px;
      font-weight:bold;
      margin-top:-12px;
      margin-bottom:20px;">
      It helps. It lasts.
     </p>
       """,
       unsafe_allow_html=True
        )

    st.sidebar.markdown("""
    <h2 style="
    color:#0B5CAD;
    text-align:left;
    margin-bottom:0;">
    Navigation
     </h2>
       """, unsafe_allow_html=True)
    
    st.sidebar.markdown("""
     <div style="
     height:3px;
      width:70px;
      background:#0B5CAD;
      margin-bottom:18px;
      border-radius:3px;">
     </div>
     """, unsafe_allow_html=True)

    
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"
    

    if st.button("📤 Upload Claim Report", use_container_width=True):
        st.session_state.page = "Upload Claim Report"

    if st.button("🔍 Search Claim", use_container_width=True):
        st.session_state.page = "Search Claim"

    if st.button("📋 Customer Claim History", use_container_width=True):
        st.session_state.page = "Customer Claim History"

    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"

    if st.button("ℹ About", use_container_width=True):
        st.session_state.page = "About"

page = st.session_state.page



st.markdown("""
<style>

/* Sidebar width */
section[data-testid="stSidebar"]{
    width: 260px !important;
}

/* Sidebar background */
section[data-testid="stSidebar"]{
    background-color:#F8F9FA;
}

/* Remove top spacing */
section[data-testid="stSidebar"] > div{
    padding-top:2px;
}

</style>
""", unsafe_allow_html=True)





# -----------------------------
# Sidebar
# -----------------------------
st.markdown("""
<style>

/* Menu Buttons */
.stButton > button{
    width:100%;
    background:white;
    color:#0B5CAD;
    font-size:17px;
    font-weight:600;
    text-align:left;
    border:none;
    border-radius:10px;
    padding:12px 16px;
    transition:0.3s;
}

/* Hover */
.stButton > button:hover{
    background:#EEF4FF;
    color:#0B5CAD;
}

/* Click */
.stButton > button:focus{
    background:#EEF4FF !important;
    color:#0B5CAD !important;
    border-left:5px solid #0B5CAD !important;
    outline:none;
}

</style>
""", unsafe_allow_html=True)
# -----------------------------
# Home Page
# -----------------------------
if page == "Home":
    st.markdown(
        """
        <h1 style='margin-bottom: 0px;'>
            🛞 
            <span style='color: #0053AE;'>C</span><span style='color: #F5822D;'>E</span><span style='color: #0053AE;'>A</span><span style='color: #0053AE;'>T</span> 
            Claim Management System
        </h1>
        """, 
        unsafe_allow_html=True
          )
    st.markdown("""
    <div style="
    display:flex;
     width:100%;
    height:2px;
    margin-top:0px;
    margin-bottom:5px;
     ">
    <div style="width:55%;background:#0053AE;"></div>
    <div style="width:45%;background:#F58220;"></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(
          """
          <div style="font-size:18px;">
         Welcome to the Tyre Claim Management System.
         </div>

         <div style="font-size:18px; color:#444;">
          Automating tyre claim processing with analytics and PDF reporting.
        </div>
        """,unsafe_allow_html=True )
    st.markdown("""
         <h2 style="
          margin-bottom:0px;
          font-size:20px;
          font-weight:650;
           color:#111;">
          Features
              </h2>

         <div style="
          width:80px;
          height:2px;
          background:#F58220;
          border-radius:5px;
         margin-bottom:10px;">
         </div>
            """, unsafe_allow_html=True)
    st.markdown("✅ Upload Weekly Claim Reports")
    st.markdown("🔍 Search Claim by Docket Number")
    st.markdown("📋 Customer Claim History")
    st.markdown("📊 Interactive Analytics Dashboard")
    st.markdown("📄 Professional PDF Reports")
    
 # ---------------- FOOTER ---------------- 
    
#     st.markdown("""
#      <div style="margin-top:58px;">
#         <div style="
#             width:320px;
#             height:2px;
#             background:#F58220;
#             margin-left:auto;
#             border-radius:2px;">
#         </div>
#         <div style="text-align:right; margin-top:1px;">
#             <div style="font-size:12px; font-weight:700;">
#                 Version 1.0
#             </div>
#             <div style="font-size:12px;">
#                 Developed by <b>Mohammad Shahbaz Shaikh</b>
#             </div>
#         </div>
#      </div> """, unsafe_allow_html=True)

# -----------------------------
# Upload Page
# -----------------------------
elif page == "Upload Claim Report":
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
elif page == "Search Claim":
    st.header(" Search Claim")
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
elif page == "Customer Claim History":

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
    
elif page == "Dashboard":

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
    title=None,
    color_discrete_sequence=["#0053AE"]
   )


    fig.update_traces(textposition="outside")

    fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Number of Claims",
    height=320,
    plot_bgcolor="white",
    paper_bgcolor="white"
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
    title=None,
    color_discrete_sequence=["#F58220"]
   )

    fig.update_traces(textposition="outside")

    fig.update_layout(
    yaxis=dict(categoryorder="total ascending"),
    height=450,
    xaxis_title="Number of Claims",
    yaxis_title="",
    plot_bgcolor="white",
    paper_bgcolor="white"
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
    title=None,
    color_discrete_sequence=["#0053AE"]
   )

    fig.update_traces(textposition="outside")

    fig.update_layout(
    yaxis=dict(categoryorder="total ascending"),
    height=450,
    xaxis_title="Number of Claims",
    yaxis_title="",
    plot_bgcolor="white",
    paper_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

   
# -----------------------------
# About
# -----------------------------
elif page == "About":

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
# -----------------------------
# Global Footer
# -----------------------------

st.markdown("""
<div style="
    position: fixed;
    bottom: 20px;
    right: 35px;
    width: 320px;
    text-align: right;
    z-index: 999;">

<div style="
        height:2px;
        background:#F58220;
        margin-bottom:5px;
        border-radius:2px;">
</div>

<div style="
        font-size:12px;
        font-weight:700;">
        Version 1.0
</div>

<div style="font-size:12px;">
        Developed by <b>Mohammad Shahbaz Shaikh</b>
</div>

</div>
""", unsafe_allow_html=True)

