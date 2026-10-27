import io, json, csv
from pathlib import Path
import pandas as pd
import streamlit as st
from backend import process_document, save_record, list_records, get_record, delete_all_records

st.set_page_config(page_title="Intelligent Document Processing", page_icon="📄", layout="wide")
st.title("📄 Intelligent Document Processing System")
st.caption("Upload an invoice or business document, extract key fields, review the results, and export structured data.")

with st.sidebar:
    st.header("About")
    st.write("Supports PDF, PNG, JPG, and JPEG files.")
    st.write("OCR: EasyOCR (when installed); PDF text extraction and regex-based field extraction.")
    st.info("Please review extracted fields before using them in business workflows.")

tab_process, tab_history = st.tabs(["Process document", "Saved history"])

with tab_process:
    uploaded = st.file_uploader("Choose a document", type=["pdf", "png", "jpg", "jpeg"])
    if uploaded:
        raw = uploaded.getvalue()
        if len(raw) > 10 * 1024 * 1024:
            st.error("File is larger than the 10 MB limit.")
        else:
            st.write(f"**File:** {uploaded.name} · **Size:** {len(raw):,} bytes")
            if st.button("Extract information", type="primary"):
                with st.spinner("Reading document and extracting fields..."):
                    try:
                        result = process_document(raw, uploaded.name)
                        st.session_state["last_result"] = result
                        st.session_state["last_filename"] = uploaded.name
                    except Exception as exc:
                        st.error(f"Could not process this file: {exc}")

    result = st.session_state.get("last_result")
    if result:
        st.subheader("Extracted fields — review and edit")
        fields = result.get("fields", {})
        editable = {}
        columns = st.columns(2)
        for i, (key, value) in enumerate(fields.items()):
            with columns[i % 2]:
                editable[key] = st.text_input(key.replace("_", " ").title(), value="" if value is None else str(value), key=f"field_{key}")
        st.subheader("Validation")
        issues = result.get("validation", {}).get("issues", [])
        if issues:
            for issue in issues:
                st.warning(issue)
        else:
            st.success("No validation issues detected. Please still verify the values.")
        with st.expander("Extracted text preview"):
            st.text_area("Text", result.get("text", ""), height=240)
        final = dict(result)
        final["fields"] = editable
        c1, c2, c3 = st.columns(3)
        with c1:
            json_bytes = json.dumps(final, ensure_ascii=False, indent=2).encode("utf-8")
            st.download_button("Download JSON", json_bytes, file_name="extraction_result.json", mime="application/json")
        with c2:
            df = pd.DataFrame([editable])
            st.download_button("Download CSV", df.to_csv(index=False).encode("utf-8-sig"), file_name="extraction_result.csv", mime="text/csv")
        with c3:
            if st.button("Save reviewed result"):
                saved_id = save_record(st.session_state.get("last_filename", "document"), final)
                st.success(f"Saved to local SQLite history (record #{saved_id}).")

with tab_history:
    st.subheader("Previously saved results")
    records = list_records()
    if not records:
        st.info("No saved records yet. Process a document and choose 'Save reviewed result'.")
    else:
        st.dataframe(pd.DataFrame(records), use_container_width=True, hide_index=True)
        selected = st.selectbox("Choose record ID", [r["id"] for r in records])
        if st.button("Show selected record"):
            record = get_record(int(selected))
            if record:
                st.json(record)
        if st.button("Clear all history", type="secondary"):
            delete_all_records()
            st.rerun()
