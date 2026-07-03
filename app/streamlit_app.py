import os
import time
import requests
import streamlit as st

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered",
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume PDF and provide the job description.")

resume_pdf = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"],
)

st.subheader("Job Description")

jd_input_mode = st.radio(
    "Choose JD input method",
    ["Paste JD Text", "Upload JD PDF"],
)

job_description_text = None
jd_pdf = None

if jd_input_mode == "Paste JD Text":
    job_description_text = st.text_area(
        "Paste Job Description",
        height=250,
        placeholder="Paste the job description here...",
    )
else:
    jd_pdf = st.file_uploader(
        "Upload JD PDF",
        type=["pdf"],
    )

if st.button("Analyze Resume"):
    if resume_pdf is None:
        st.error("Please upload your resume PDF.")
    elif jd_input_mode == "Paste JD Text" and not job_description_text.strip():
        st.error("Please paste the job description.")
    elif jd_input_mode == "Upload JD PDF" and jd_pdf is None:
        st.error("Please upload JD PDF.")
    else:
        with st.spinner("Uploading resume..."):
            files = {
                "resume_pdf": (
                    resume_pdf.name,
                    resume_pdf.getvalue(),
                    "application/pdf",
                )
            }

            data = {}

            if jd_input_mode == "Paste JD Text":
                data["job_description_text"] = job_description_text
            else:
                files["jd_pdf"] = (
                    jd_pdf.name,
                    jd_pdf.getvalue(),
                    "application/pdf",
                )

            response = requests.post(
                f"{FASTAPI_URL}/resume/analyze",
                files=files,
                data=data,
            )

        if response.status_code != 200:
            st.error("Failed to upload resume.")
            st.write(response.text)
        else:
            file_id = response.json()["file_id"]

            st.success("Resume uploaded successfully.")
            st.caption(f"File ID: {file_id}")

            status_placeholder = st.empty()
            result_placeholder = st.empty()

            while True:
                result_response = requests.get(
                    f"{FASTAPI_URL}/resume/{file_id}"
                )

                result_data = result_response.json()
                status = result_data.get("status")

                status_placeholder.info(f"Status: {status}")

                if status == "processed":
                    result_placeholder.markdown(result_data.get("result"))
                    break

                if status == "failed":
                    st.error(result_data.get("result"))
                    break

                time.sleep(3)