import requests
import json
import gradio as gr
import fitz  # PyMuPDF

url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}
session = requests.Session()

stop_flag = {"stop": False}
pdf_text_store = {"text": ""}

# Preload known regional animal aid contacts
REGIONAL_CONTACTS = {
    "maharashtra": {
        "pandharpur": "9552552049",
        "sangli": "9850958484",
        "satara": "9552553980",
        "solapur": "9552552048",
        "after_hours": "9820122602"
    },
    "uttar pradesh": {
        "siyana": "9552554411",
        "after_hours": "9820122602"
    },
    "uttarakhand": {},
    "uttar pradesh": {},
    "delhi": {
        "any": ["011-23890485", "011-20833238"]
    },
    "assam": {
        "any": "18003453570"
    },
    "bihar": {},
    "udaipur": {
        "any": ["9829843726", "9602325253", "9784005989"]
    },
    # Add more regions as needed...
}

def extract_pdf(file_obj):
    try:
        pdf_text = ""
        with fitz.open(file_obj.name) as pdf_doc:
            for page in pdf_doc:
                pdf_text += page.get_text()
        pdf_text_store["text"] = pdf_text.strip()
        return "✅ PDF uploaded & processed for animal case!"
    except Exception as e:
        return f"❌ PDF processing failed: {e}"

def stop_generation():
    stop_flag["stop"] = True
    return "⛔ Generation stopped."

def lookup_contact(user_loc):
    loc = user_loc.strip().lower()
    for region, data in REGIONAL_CONTACTS.items():
        if region in loc:
            # Exact city match?
            for city, num in data.items():
                if city in loc and city != "any" and city != "after_hours":
                    return num, region
            # Else fallback to "any"
            if "any" in data:
                return data["any"], region
            # Else fallback to first number
            for city_key in data:
                return data[city_key], region
    return None, None

def generate_response(prompt, user_loc):
    stop_flag["stop"] = False
    contact, region_found = lookup_contact(user_loc or "")
    contact_msg = (f"⚠ Emergency Animal Aid Helpline for your region ({region_found.title()}): {contact}"
                   if contact else "⚠ No specific regional helpline found for your location.")

    base_instruction = (
        "You are an Animal First Aid Assistant. Provide safe, humane, "
        "practical advice for injured or suffering animals. Always encourage consulting a veterinarian."
    )

    if not prompt.strip() and pdf_text_store["text"]:
        full_prompt = f"{base_instruction}\n\nAnalyze this animal case:\n{pdf_text_store['text']}"
    elif prompt.strip() and pdf_text_store["text"]:
        full_prompt = f"{base_instruction}\n\nUser Question: {prompt}\n\nCase details from PDF:\n{pdf_text_store['text']}"
    elif prompt.strip():
        full_prompt = f"{base_instruction}\n\nUser Question: {prompt}"
    else:
        yield "⚠ Please provide a PDF or a question."
        return

    data = {"model": "AniAid", "prompt": full_prompt, "stream": True}

    try:
        with session.post(url, headers=headers, json=data, stream=True) as r:
            output = ""
            for line in r.iter_lines():
                if stop_flag["stop"]:
                    break
                if line:
                    try:
                        json_data = json.loads(line.decode())
                        if "response" in json_data:
                            output += json_data["response"]
                            yield contact_msg + "\n\n" + output
                    except json.JSONDecodeError:
                        continue
    except requests.RequestException as e:
        yield f"❌ API connection error: {e}"

with gr.Blocks(css=".gradio-container {background-color: #1e1e1e; color: white;}") as demo:
    gr.Markdown("<h1 style='text-align:center; color:#ff914d;'>🐾 Animal Aid Real-Time Helper</h1>"
                "<p style='text-align:center;'>Upload case details, ask for help — plus get local rescue contacts!</p>")
    with gr.Row():
        with gr.Column():
            pdf_upload = gr.File(label="📄 Upload Animal Case Report (PDF)", file_types=[".pdf"])
            upload_status = gr.Textbox(label="📢 Status", interactive=False)
            user_loc = gr.Textbox(label="📍 Your Location (district/state)", placeholder="Eg: Pune, Maharashtra or Udaipur, Rajasthan")
            user_input = gr.Textbox(label="💬 Your Question", lines=4,
                                    placeholder="Describe the situation or ask for treatment advice…")
            output_box = gr.Textbox(label="🐶 AI Response + Emergency Contact", lines=10)
            with gr.Row():
                submit_btn = gr.Button("🚑 Get Aid", variant="primary")
                stop_btn = gr.Button("⛔ Stop", variant="secondary")

    pdf_upload.change(extract_pdf, inputs=pdf_upload, outputs=upload_status)
    submit_btn.click(generate_response, inputs=[user_input, user_loc], outputs=output_box, queue=True)
    stop_btn.click(stop_generation, outputs=output_box)

demo.queue()
demo.launch()
