import time
import requests
import streamlit as st

FASTAPI_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered",
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume PDF and paste the job description.")

resume_pdf = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"],
)

job_description_text = st.text_area(
    "Paste Job Description",
    height=250,
    placeholder="Paste the job description here...",
)

if st.button("Analyze Resume"):
    if resume_pdf is None:
        st.error("Please upload your resume PDF.")
    elif not job_description_text.strip():
        st.error("Please paste the job description.")
    else:
        with st.spinner("Uploading resume..."):
            files = {
                "resume_pdf": (
                    resume_pdf.name,
                    resume_pdf.getvalue(),
                    "application/pdf",
                )
            }

            data = {
                "job_description_text": job_description_text
            }

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
