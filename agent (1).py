import os
import streamlit as st
from pydantic import BaseModel, Field
from typing import Optional
import langroid as lr
from langroid.agent.chat_agent import ChatAgent, ChatAgentConfig
from langroid.agent.task import Task
from langroid.language_models import OpenAIGPTConfig
from langroid.agent.tools.duckduckgo_search_tool import DuckduckgoSearchTool

# Configure app
st.set_page_config(page_title="AI Outreach Personalizer", page_icon="✉️")

# Hide warnings
st.set_option('deprecation.showPyplotGlobalUse', False)

class ProspectData(BaseModel):
    name: str = Field(..., description="Prospect's full name")
    company: str = Field(..., description="Company name")
    role: str = Field(..., description="Job title/role")
    website: Optional[str] = Field(None, description="Company website URL")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")

def generate_outreach(prospect: ProspectData) -> str:
    """Core email generation function"""
    llm_config = OpenAIGPTConfig(
        chat_model=st.session_state.get("model", "groq/llama3-70b-8192"),
        temperature=0.3,
        max_output_tokens=500,
    )

    # Research Agent
    researcher = ChatAgent(
        ChatAgentConfig(
            name="Researcher",
            system_message="""
            Find company info and prospect's public content using search tools.
            Return raw facts only.
            """,
            llm=llm_config,
        )
    )
    researcher.enable_message(DuckduckgoSearchTool)

    # Personalizer Agent
    personalizer = ChatAgent(
        ChatAgentConfig(
            name="Personalizer",
            system_message=f"""
            Create a 3-4 line email with:
            1. Personal hook about {prospect.company}
            2. Value proposition
            3. Clear CTA
            
            Format:
            Subject: [Hook]
            Body:
            Hi [Name], [hook]...
            We help [value prop].
            [Call-to-action?]
            Best, [Your Name]
            """,
            llm=llm_config,
        )
    )

    # Setup tasks
    research_task = Task(researcher, single_round=True)
    personalize_task = Task(personalizer, llm_delegate=True)
    personalize_task.add_sub_task(research_task)

    query = f"""
    Find info about:
    1. {prospect.company} {f'website:{prospect.website}' if prospect.website else ''}
    2. {prospect.name} {prospect.role} site:linkedin.com/in
    """
    
    result = personalize_task.run(query)
    return result.content if result else "Error generating email"

# Streamlit UI
st.title("✉️ AI Outreach Personalizer")
st.markdown("Create hyper-personalized cold emails in seconds")

with st.sidebar:
    st.header("Settings")
    model = st.selectbox(
        "AI Model",
        ["groq/llama3-70b-8192", "openai/gpt-4-turbo"],
        index=0,
        key="model"
    )
    st.markdown("---")
    st.markdown("💡 Tip: For best results, include the company website")

# Main form
with st.form("prospect_form"):
    cols = st.columns(2)
    with cols[0]:
        name = st.text_input("Prospect Name", placeholder="Jane Doe")
    with cols[1]:
        company = st.text_input("Company", placeholder="Acme Inc")
    
    role = st.text_input("Role", placeholder="CEO")
    website = st.text_input("Company Website (optional)", placeholder="https://acme.com")
    
    submitted = st.form_submit_button("Generate Email")
    
    if submitted:
        if not name or not company or not role:
            st.error("Please fill in required fields")
        else:
            with st.spinner("Researching and crafting perfect email..."):
                prospect = ProspectData(
                    name=name,
                    company=company,
                    role=role,
                    website=website if website.startswith("http") else None
                )
                email = generate_outreach(prospect)
                
                if "Subject:" in email:
                    st.success("Email generated!")
                    st.markdown("---")
                    st.subheader("Your Personalized Email")
                    
                    # Format with HTML for better display
                    subject = email.split("Subject:")[1].split("\n")[0].strip()
                    body = "\n".join(email.split("\n")[1:]).strip()
                    
                    st.markdown(f"""
                    <div style='background:#f9f9f9;padding:20px;border-radius:10px'>
                        <h4>Subject: {subject}</h4>
                        <pre style='white-space:pre-wrap;font-family:sans-serif'>{body}</pre>
                    </div>
                    """, unsafe_allow_html=True)
                    
# Add copy button
st.code(email, language="text")

# Show cost stats if available
try:
    cost = lr.language_models.base.LLM.cost_summary()
    st.caption(f"Cost: ${cost.total:.4f} (in: {cost.input_tokens} tokens, out: {cost.output_tokens} tokens)")
except AttributeError:
    pass

# How to run:
# streamlit run outreach_app.py
