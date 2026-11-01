# app.py
import gradio as gr
from main import app

# Create a dummy Gradio UI so Hugging Face's health checks pass
demo = gr.Blocks()
with demo:
    gr.Markdown("# TripSmith API is Running Globally!")

# Mount the dummy UI at /ui so it doesn't interfere with your /api/plan-trip endpoint
app = gr.mount_gradio_app(app, demo, path="/ui")