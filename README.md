🐾 AniAid – Real-Time Animal & Bird First Aid Assistant

AniAid is an AI-powered assistant designed to provide real-time first-aid guidance for animals and birds. It combines Generative AI + Computer Vision (image input) with regional rescue helpline support to help users take immediate action in emergency situations.

🚀 Features
📸 Image-based Analysis
Upload an image of an injured or sick animal/bird for AI-assisted guidance.
💬 Text-based Queries
Ask questions like:
“Injured dog bleeding”
“Bird not flying”
“Cow not eating”
🧠 AI First-Aid Suggestions
Provides safe, humane, and practical advice
📍 Location-based Emergency Contacts
Suggests animal rescue helplines based on user location
⛔ Stop Generation Feature
Allows users to stop response generation anytime
🌐 Real-time Streaming Output
Response is generated live (token-by-token)
🛠️ Tech Stack
Frontend/UI: Gradio
Backend: Python
AI Model API: Local LLM via Ollama (localhost:11434)
Libraries Used:
requests
gradio
json
base64
📂 Project Structure
AniAid/
│── app.py                # Main application file
│── README.md             # Project documentation
⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/aniaid.git
cd aniaid
2️⃣ Install dependencies
pip install gradio requests
3️⃣ Run Ollama Model (Important)

Make sure your local model is running:

ollama run AniAid

Or ensure API is available at:

http://localhost:11434/api/generate
4️⃣ Run the application
python app.py
🧪 How to Use
Upload an animal/bird image (optional)
Enter your location (e.g., Pune, Maharashtra)
Describe the issue in the question box
Click 🚑 Get Aid
Get:
AI-generated first-aid advice
Emergency rescue contact
📍 Supported Regions (Sample)
Maharashtra (Pandharpur, Sangli, Satara, Solapur)
Uttar Pradesh
Delhi
Assam
Udaipur

(Can be extended easily in REGIONAL_CONTACTS dictionary)

⚠️ Disclaimer
This tool provides first-aid guidance only
It is NOT a replacement for a veterinarian
Always contact a professional vet or rescue service in serious cases
💡 Future Improvements
🔍 Advanced image classification (disease detection)
🌎 More region-wise rescue databases
📱 Mobile app version
🧠 Fine-tuned veterinary AI model
🗣️ Voice input support
🤝 Contribution

Contributions are welcome!

# Fork the repo
# Create a new branch
git checkout -b feature-name

# Commit changes
git commit -m "Added feature"

# Push
git push origin feature-name
📬 Contact

Ashutosh Sahu
📧 ashutoshsahu375@gmail.com

🔗 GitHub: https://github.com/ashutoshsahuuu09

⭐ Support

If you found this useful:

⭐ Star the repo
🐾 Share with others
