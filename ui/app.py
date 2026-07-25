import streamlit as st
import sys
import os

# Ensure Streamlit can find your services folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.llm_service import analyze_message

# Set up the webpage design
st.set_page_config(page_title="Triage AI", layout="centered", page_icon="🛠️")

st.title("🛠️ Customer Support Triage AI")
st.markdown("Enter a customer message below to automatically extract the category, priority, and suggested actions using a local LLM.")

# Input Box for the customer message
user_message = st.text_area(
    "Customer Message", 
    height=150, 
    placeholder="E.g., My order #1234 still hasn't arrived and it's been two weeks."
)

# Action Button
if st.button("Analyze Message", type="primary"):
    if not user_message.strip():
        st.warning("Please enter a message first.")
    else:
        # Display a spinner so users know the CPU is working
        with st.spinner("Llama 3.1 is analyzing (this may take 45-60 seconds on CPU)..."):
            try:
                # Send the message to your local LLM
                result = analyze_message(user_message)
                
                st.success("Analysis Complete!")
                
                # Display metrics side-by-side in a clean row
                col1, col2, col3 = st.columns(3)
                col1.metric("Category", result.category)
                col2.metric("Priority", result.priority)
                
                # Color code the human review flag
                human_flag = "🚨 YES" if result.needs_human else "✅ NO"
                col3.metric("Needs Human", human_flag)
                
                # Display the text summaries
                st.subheader("Summary")
                st.info(result.summary)
                
                st.subheader("Suggested Action")
                st.write(result.suggested_action)
                
                # Show warning if human escalation is triggered
                if result.needs_human:
                    st.error(f"**Escalation Reason:** {result.escalation_reason}")
                    
                # Show the raw JSON for the technical requirement
                with st.expander("View Raw JSON Output"):
                    st.json(result.model_dump())
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")