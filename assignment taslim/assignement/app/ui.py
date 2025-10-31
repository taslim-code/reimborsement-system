import streamlit as st
import requests
from zipfile import ZipFile
import io

st.title("Invoice Reimbursement System UI")

st.header("1. Analyze Invoices")
policy_pdf = st.file_uploader("Upload HR Policy PDF", type=["pdf"], key="policy")
invoices_zip = st.file_uploader("Upload Invoices ZIP", type=["zip"], key="invoices")
employee_name = st.text_input("Employee Name")

if st.button("Analyze Invoices"):
    if not policy_pdf or not invoices_zip or not employee_name:
        st.warning("Please provide all inputs.")
    else:
        files = {
            "policy_pdf": (policy_pdf.name, policy_pdf, "application/pdf"),
            "invoices_zip": (invoices_zip.name, invoices_zip, "application/zip")
        }
        data = {"employee_name": employee_name}
        with st.spinner("Analyzing invoices..."):
            response = requests.post(
                "http://localhost:8000/analyze/",
                files=files,
                data=data
            )
        if response.ok:
            st.success("Analysis complete!")
            st.json(response.json())
        else:
            st.error(f"Error: {response.text}")

st.header("2. Query Chatbot")
query = st.text_input("Ask a question about invoices (e.g., 'Show declined invoices for John Doe'):")
if st.button("Ask Chatbot"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Querying chatbot..."):
            response = requests.post(
                "http://localhost:8000/chatbot/",
                json={"query": query}
            )
        if response.ok:
            result = response.json()
            st.markdown(result.get("response", "No response."))
        else:
            st.error(f"Error: {response.text}")
