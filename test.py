import google.generativeai as genai

client = genai.configure("AIzaSyDzNB1pysn52yqpZdWHE67jHM8NTNW8-vY")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How does AI work?"
)
print(response.text)