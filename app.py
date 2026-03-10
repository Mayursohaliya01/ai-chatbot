import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import base64


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("🚀 Mayur AI chatbot")
st.caption("Powered by Groq AI")

st.caption("Chat + Vision + Function Calling")

# -------- Chat Memory --------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# -------- Function Example --------

def book_flight(city1, city2):
    return f"✈️ Flight booked from {city1} to {city2}"

# -------- Chat Input --------

prompt = st.chat_input("Ask something...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # simple function trigger
    if "book flight" in prompt.lower():
        result = book_flight("Ahmedabad","Delhi")
        st.chat_message("assistant").write(result)
        st.session_state.messages.append({"role":"assistant","content":result})

    else:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages
        )

        msg = response.choices[0].message.content

        st.chat_message("assistant").write(msg)
        st.session_state.messages.append({"role":"assistant","content":msg})


# -------- Image Upload (Vision) --------

st.subheader("🖼️ Upload Image")

image = st.file_uploader("Upload an image", type=["png","jpg","jpeg"])

if image:

    bytes_data = image.read()
    base64_image = base64.b64encode(bytes_data).decode("utf-8")

    response = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role":"user",
                "content":[
                    {"type":"text","text":"Describe this image"},
                    {
                        "type":"image_url",
                        "image_url":{
                            "url":f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )

    st.write(response.choices[0].message.content)


# -------- Structured Output Example --------

st.subheader("📊 Structured Output")

city = st.text_input("Enter city name")

if city:

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role":"system","content":"Return JSON only"},
            {"role":"user","content":f"Give weather info for {city} in JSON"}
        ]
    )

    st.code(response.choices[0].message.content)
    st.caption("© 2026 Mayur AI Lab")
