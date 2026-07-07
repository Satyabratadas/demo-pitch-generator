import streamlit as st
import requests

# Set up the page layout
st.set_page_config(page_title="Hackathon Pitch Generator", page_icon="🎤", layout="centered")

st.title("🎤 MLH Demo Pitch Generator")
st.markdown("Did you just spend 36 hours coding? Exhausted? Drop your GitHub repo below, and AI will write your 2-minute winning presentation.")

# The input box
repo_url = st.text_input("Enter public GitHub Repository URL:", placeholder="https://github.com/psf/requests")

# The submit button
if st.button("Generate Pitch", type="primary"):
    if not repo_url:
        st.warning("Please enter a GitHub URL first.")
    else:
        # Show a loading spinner while waiting for FastAPI and Gemini
        with st.spinner("Scanning repository and writing your script..."):
            try:
                # Call your local FastAPI server
                response = requests.post(
                    "http://127.0.0.1:8000/generate-pitch", 
                    json={"repo_url": repo_url}
                )
                
                if response.status_code == 200:
                    pitch = response.json()
                    st.success(f"Pitch generated for: **{pitch['project_name']}**")
                    
                    # Display the Hook
                    st.subheader("🪝 The Hook (0:00 - 0:15)")
                    st.info(pitch["hook"])
                    
                    # Display the Problem Statement
                    st.subheader("The Problem")
                    st.write(pitch["problem_statement"])
                    
                    # Display the Wow Moment
                    st.subheader("The 'Wow' Moment")
                    st.success(pitch["wow_moment"])
                    
                    # Display the Timeline using Expanders
                    st.subheader("2-Minute Script Timeline")
                    for segment in pitch["timeline"]:
                        with st.expander(f"{segment['time_marker']} - {segment['action'][:50]}..."):
                            st.markdown(f"**Action on Screen:** {segment['action']}")
                            st.markdown(f"**What to Say:** \"*{segment['talking_points']}*\"")
                            
                    # Display Warnings
                    st.subheader("⚠️ Demo Warnings")
                    for warning in pitch["demo_warnings"]:
                        st.error(warning)
                        
                else:
                    st.error(f"Failed to generate pitch. Error: {response.json().get('detail', 'Unknown error')}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to the backend server. Is FastAPI running on port 8000?")