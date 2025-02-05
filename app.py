# import os

# import streamlit as st

# from dotenv import load_dotenv
# from src.agents import AgentManager
# from src.utils.logger import logger

# load_dotenv()

# def main():
#     st.set_page_config(
#         page_title = "Multi AI-Agentic System", layout="wide"
#     )
#     st.title("Multi AI-Agentic System with Collaboration and Validation")

#     st.sidebar.title("Select Task")

#     # 🔹 User selects LLM provider
#     llm_provider = st.sidebar.radio("Choose LLM Provider:", ["OpenAI", "Groq"]).lower()


#     task = st.sidebar.selectbox("Choose a task: ", [
#             "Summarize Medical Text",
#             "Write and Refine Research Articles",
#             "Sanitize Medical Data (PHI Removal)"
#         ]
#     )

#     agent_manager = AgentManager(max_retries=3, verbose=True)

#     if task == "Summarize Medical Text":
#         summarize_section(agent_manager, llm_provider)
    
#     elif task == "Write and Refine Research Articles":
#         write_and_refine_article_section(agent_manager, llm_provider)

#     elif task == "Sanitize Medical Data (PHI Removal)":
#         sanitize_data_section(agent_manager, llm_provider)

# def summarize_section(agent_manager, llm_provider):
#     st.header("Summarize Medical Text")
#     text = st.text_area("Enter medical text to summarize:", height=200)
#     if st.button("Summarize"):
#         if text:
#             main_agent = agent_manager.get_agent("summarize")
#             validator_agent = agent_manager.get_agent("summarize_validator")
            
#             main_agent.llm_provider = llm_provider
#             validator_agent.llm_provider = llm_provider

#             with st.spinner("Summarizing..."):
#                 try:
#                     summary = main_agent.execute(text)
#                     st.subheader("Summary:")
#                     st.write(summary)
#                 except Exception as e:
#                     st.error(f"Error: {e}")
#                     logger.error(f"SummarizeAgent Error: {e}")
#                     return

#             with st.spinner("Validating summary..."):
#                 try:
#                     validation = validator_agent.execute(original_text=text, summary=summary)
#                     st.subheader("Validation:")
#                     st.write(validation)
#                 except Exception as e:
#                     st.error(f"Validation Error: {e}")
#                     logger.error(f"SummarizeValidatorAgent Error: {e}")
#         else:
#             st.warning("Please enter some text to summarize.")

# def write_and_refine_article_section(agent_manager, llm_provider):
#     st.header("Write and Refine Research Article")
#     topic = st.text_input("Enter the topic for the research article:")
#     outline = st.text_area("Enter an outline (optional):", height=150)
#     if st.button("Write and Refine Article"):
#         if topic:
#             writer_agent = agent_manager.get_agent("write_article")
#             refiner_agent = agent_manager.get_agent("refiner")
#             validator_agent = agent_manager.get_agent("validator")
            
#             writer_agent.llm_provider = llm_provider
#             refiner_agent.llm_provider = llm_provider
#             validator_agent.llm_provider = llm_provider

#             with st.spinner("Writing article..."):
#                 try:
#                     draft = writer_agent.execute(topic, outline)
#                     st.subheader("Draft Article:")
#                     st.write(draft)
#                 except Exception as e:
#                     st.error(f"Error: {e}")
#                     logger.error(f"WriteArticleAgent Error: {e}")
#                     return

#             with st.spinner("Refining article..."):
#                 try:
#                     refined_article = refiner_agent.execute(draft)
#                     st.subheader("Refined Article:")
#                     st.write(refined_article)
#                 except Exception as e:
#                     st.error(f"Refinement Error: {e}")
#                     logger.error(f"RefinerAgent Error: {e}")
#                     return

#             with st.spinner("Validating article..."):
#                 try:
#                     validation = validator_agent.execute(topic=topic, article=refined_article)
#                     st.subheader("Validation:")
#                     st.write(validation)
#                 except Exception as e:
#                     st.error(f"Validation Error: {e}")
#                     logger.error(f"ValidatorAgent Error: {e}")
#         else:
#             st.warning("Please enter a topic for the research article.")

# def sanitize_data_section(agent_manager, llm_provider):
#     st.header("Sanitize Medical Data (PHI)")
#     medical_data = st.text_area("Enter medical data to sanitize:", height=200)
#     if st.button("Sanitize Data"):
#         if medical_data:
#             main_agent = agent_manager.get_agent("sanitize_data")
#             validator_agent = agent_manager.get_agent("sanitize_data_validator")

#             main_agent.llm_provider = llm_provider
#             validator_agent.llm_provider = llm_provider

#             with st.spinner("Sanitizing data..."):
#                 try:
#                     sanitized_data = main_agent.execute(medical_data)
#                     st.subheader("Sanitized Data:")
#                     st.write(sanitized_data)
#                 except Exception as e:
#                     st.error(f"Error: {e}")
#                     logger.error(f"SanitizeDataAgent Error: {e}")
#                     return

#             with st.spinner("Validating sanitized data..."):
#                 try:
#                     validation = validator_agent.execute(original_data=medical_data, sanitized_data=sanitized_data)
#                     st.subheader("Validation:")
#                     st.write(validation)
#                 except Exception as e:
#                     st.error(f"Validation Error: {e}")
#                     logger.error(f"SanitizeDataValidatorAgent Error: {e}")
#         else:
#             st.warning("Please enter medical data to sanitize.")

# if __name__ == "__main__":
#     main()

import os
import streamlit as st
from dotenv import load_dotenv
from src.agents import AgentManager
from src.utils.logger import logger

load_dotenv()

def main():
    # Set Streamlit Page Config
    st.set_page_config(
        page_title="Multi AI-Agentic System",
        layout="wide"
    )

    st.title("Multi AI-Agentic System with Collaboration and Validation")

    # Initialize session state for API keys if not set
    if "api_keys_set" not in st.session_state:
        st.session_state.api_keys_set = False

    # API Key Input Section
    if not st.session_state.api_keys_set:
        st.sidebar.header("🔑 Enter API Keys")

        openai_api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
        groq_api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

        if st.sidebar.button("Submit API Keys"):
            if not openai_api_key or not groq_api_key:
                st.sidebar.error("❌ Please enter both API keys!")
            else:
                # Store keys in session state
                st.session_state.openai_api_key = openai_api_key
                st.session_state.groq_api_key = groq_api_key
                st.session_state.api_keys_set = True

                # Mask keys for display (only show first 3 characters)
                masked_openai_key = openai_api_key[:3] + "*" * (len(openai_api_key) - 3)
                masked_groq_key = groq_api_key[:3] + "*" * (len(groq_api_key) - 3)

                st.sidebar.success(f"✅ OpenAI Key: {masked_openai_key}")
                st.sidebar.success(f"✅ Groq Key: {masked_groq_key}")

    # Proceed only if API keys are set
    if st.session_state.api_keys_set:
        st.sidebar.success("✅ API Keys Verified!")
        st.sidebar.title("Select Task")

        # User selects LLM provider
        llm_provider = st.sidebar.radio("Choose LLM Provider:", ["OpenAI", "Groq"]).lower()

        task = st.sidebar.selectbox("Choose a task:", [
            "Summarize Medical Text",
            "Write and Refine Research Articles",
            "Sanitize Medical Data (PHI Removal)"
        ])

        agent_manager = AgentManager(max_retries=3, verbose=True)

        if task == "Summarize Medical Text":
            summarize_section(agent_manager, llm_provider)
        
        elif task == "Write and Refine Research Articles":
            write_and_refine_article_section(agent_manager, llm_provider)

        elif task == "Sanitize Medical Data (PHI Removal)":
            sanitize_data_section(agent_manager, llm_provider)

# ------------------- Summarization Section -------------------

def summarize_section(agent_manager, llm_provider):
    st.header("Summarize Medical Text")
    text = st.text_area("Enter medical text to summarize:", height=200)
    
    if st.button("Summarize"):
        if text:
            main_agent = agent_manager.get_agent("summarize")
            validator_agent = agent_manager.get_agent("summarize_validator")
            
            main_agent.llm_provider = llm_provider
            validator_agent.llm_provider = llm_provider

            with st.spinner("Summarizing..."):
                try:
                    summary = main_agent.execute(text)
                    st.subheader("Summary:")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Error: {e}")
                    logger.error(f"SummarizeAgent Error: {e}")
                    return

            with st.spinner("Validating summary..."):
                try:
                    validation = validator_agent.execute(original_text=text, summary=summary)
                    st.subheader("Validation:")
                    st.write(validation)
                except Exception as e:
                    st.error(f"Validation Error: {e}")
                    logger.error(f"SummarizeValidatorAgent Error: {e}")
        else:
            st.warning("Please enter some text to summarize.")

# ------------------- Write & Refine Article Section -------------------

def write_and_refine_article_section(agent_manager, llm_provider):
    st.header("Write and Refine Research Article")
    topic = st.text_input("Enter the topic for the research article:")
    outline = st.text_area("Enter an outline (optional):", height=150)
    
    if st.button("Write and Refine Article"):
        if topic:
            writer_agent = agent_manager.get_agent("write_article")
            refiner_agent = agent_manager.get_agent("refiner")
            validator_agent = agent_manager.get_agent("validator")
            
            writer_agent.llm_provider = llm_provider
            refiner_agent.llm_provider = llm_provider
            validator_agent.llm_provider = llm_provider

            with st.spinner("Writing article..."):
                try:
                    draft = writer_agent.execute(topic, outline)
                    st.subheader("Draft Article:")
                    st.write(draft)
                except Exception as e:
                    st.error(f"Error: {e}")
                    logger.error(f"WriteArticleAgent Error: {e}")
                    return

            with st.spinner("Refining article..."):
                try:
                    refined_article = refiner_agent.execute(draft)
                    st.subheader("Refined Article:")
                    st.write(refined_article)
                except Exception as e:
                    st.error(f"Refinement Error: {e}")
                    logger.error(f"RefinerAgent Error: {e}")
                    return

            with st.spinner("Validating article..."):
                try:
                    validation = validator_agent.execute(topic=topic, article=refined_article)
                    st.subheader("Validation:")
                    st.write(validation)
                except Exception as e:
                    st.error(f"Validation Error: {e}")
                    logger.error(f"ValidatorAgent Error: {e}")
        else:
            st.warning("Please enter a topic for the research article.")

# ------------------- Sanitize Data Section -------------------

def sanitize_data_section(agent_manager, llm_provider):
    st.header("Sanitize Medical Data (PHI)")
    medical_data = st.text_area("Enter medical data to sanitize:", height=200)
    
    if st.button("Sanitize Data"):
        if medical_data:
            main_agent = agent_manager.get_agent("sanitize_data")
            validator_agent = agent_manager.get_agent("sanitize_data_validator")

            main_agent.llm_provider = llm_provider
            validator_agent.llm_provider = llm_provider

            with st.spinner("Sanitizing data..."):
                try:
                    sanitized_data = main_agent.execute(medical_data)
                    st.subheader("Sanitized Data:")
                    st.write(sanitized_data)
                except Exception as e:
                    st.error(f"Error: {e}")
                    logger.error(f"SanitizeDataAgent Error: {e}")
                    return

            with st.spinner("Validating sanitized data..."):
                try:
                    validation = validator_agent.execute(original_data=medical_data, sanitized_data=sanitized_data)
                    st.subheader("Validation:")
                    st.write(validation)
                except Exception as e:
                    st.error(f"Validation Error: {e}")
                    logger.error(f"SanitizeDataValidatorAgent Error: {e}")
        else:
            st.warning("Please enter medical data to sanitize.")

if __name__ == "__main__":
    main()