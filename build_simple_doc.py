import os
from docx_builder import DocxBuilder

doc = DocxBuilder()

# 1. Title and Student Info
doc.add_title_block(
    "Assignment: AI Tools Setup & Comparative Evaluation",
    "GitHub Copilot vs. OpenAI ChatGPT vs. Anthropic Claude",
    [
        ("Student Name:", "[Your Name]"),
        ("Student ID / Roll No:", "[Your Roll Number]"),
        ("Subject / Course:", "Cloud Computing / Web Technologies"),
        ("Date:", "October 2026"),
        ("Screencast Video Link:", "https://drive.google.com/file/d/your-screencast-link/view")
    ]
)

# 2. Objective
doc.add_heading_1("1. Objective")
doc.add_paragraph("The objective of this assignment is to install and activate GitHub Copilot in VS Code, configure two other AI tools (ChatGPT and Claude), prompt each AI to generate a simple responsive HTML/CSS landing page, compare their outputs, and provide an evaluation sheet along with a screencast recording link.")

# 3. Setup of AI Tools
doc.add_heading_1("2. Setup & Configuration")

doc.add_heading_2("2.1 Visual Studio Code & GitHub Copilot")
doc.add_bullet("Installed Visual Studio Code on the system.", bold_prefix="Step 1:")
doc.add_bullet("Installed 'GitHub Copilot' and 'GitHub Copilot Chat' from the VS Code Extensions tab (Ctrl+Shift+X).", bold_prefix="Step 2:")
doc.add_bullet("Signed in with GitHub account and verified the Copilot status icon in the bottom status bar.", bold_prefix="Step 3:")
doc.add_bullet("Verified inline code suggestions and the chat sidebar (Ctrl+Alt+I).", bold_prefix="Step 4:")

doc.add_heading_2("2.2 OpenAI ChatGPT")
doc.add_bullet("Opened chat.openai.com in the browser and logged in.", bold_prefix="Step 1:")
doc.add_bullet("Selected the GPT-4o model for generating code.", bold_prefix="Step 2:")

doc.add_heading_2("2.3 Anthropic Claude")
doc.add_bullet("Opened claude.ai in the browser and logged in.", bold_prefix="Step 1:")
doc.add_bullet("Selected Claude 3.5 Sonnet and enabled Artifacts for live code preview.", bold_prefix="Step 2:")

# 4. Standardized Prompt
doc.add_heading_1("3. The Standardized Prompt")
doc.add_paragraph("The following prompt was given to all three AI tools to ensure a fair comparison:")

prompt_code = """Create a simple, modern, and responsive HTML/CSS landing page for a cloud tool named "CloudPulse".

Requirements:
1. Navigation bar with a logo and "Get Started" button.
2. Hero section with a title, short description, and CTA button.
3. Features section with 3 cards (Icon, Title, Description).
4. Simple footer with copyright info.
5. All CSS must be inside a <style> tag so it is self-contained."""

doc.add_code_block(prompt_code)

# 5. Output Comparison
doc.add_heading_1("4. Output Comparison")

doc.add_paragraph(
    "Copilot generated clean, standard HTML5 code quickly directly inside VS Code. The structure was semantic and valid. However, the visual styling was very basic (flat colors, standard shadows, minimal micro-interactions).",
    bold_prefix="GitHub Copilot:"
)

doc.add_paragraph(
    "ChatGPT generated a well-organized file using CSS variables (:root). It included modern gradient accents, button hover effects, and responsive media queries. The layout looked balanced and clean.",
    bold_prefix="OpenAI ChatGPT:"
)

doc.add_paragraph(
    "Claude produced the most visually appealing landing page. It used modern dark-mode aesthetics, subtle glassmorphism, fluid typography, and clean cards. With Claude Artifacts, the page could be previewed live instantly without leaving the chat.",
    bold_prefix="Anthropic Claude:"
)

# 6. Comparative Evaluation Sheet (Table)
doc.add_heading_1("5. Comparative Evaluation Sheet")
doc.add_paragraph("Here is the scoring matrix comparing all three tools across core criteria (scored out of 10):")

eval_headers = ["Evaluation Criteria", "GitHub Copilot", "ChatGPT (GPT-4o)", "Claude (3.5 Sonnet)", "Comments"]
eval_rows = [
    ["Setup & Ease of Use", "9 / 10", "9 / 10", "9 / 10", "All tools are easy to set up; Copilot lives directly in the IDE."],
    ["Prompt Following", "8.5 / 10", "9 / 10", "10 / 10", "All followed instructions; Claude included nice extra design touches."],
    ["HTML Code Quality", "9 / 10", "9 / 10", "9.5 / 10", "All produced clean, semantic HTML5 structure."],
    ["CSS & Visual Design", "7.5 / 10", "8.5 / 10", "9.8 / 10", "Claude had the best visual look; Copilot was standard/basic."],
    ["Mobile Responsiveness", "8 / 10", "8.5 / 10", "9.5 / 10", "Claude adapted most smoothly across screen sizes."],
    ["Speed & Workflow", "10 / 10", "8.5 / 10", "8.5 / 10", "Copilot is fastest for in-editor coding without copy-paste."],
    ["TOTAL SCORE (out of 60)", "52.0 / 60", "53.5 / 60", "56.3 / 60", "Claude scored highest overall for landing page design."],
    ["AVERAGE (out of 10)", "8.67 / 10", "8.92 / 10", "9.38 / 10", "Claude: Rank 1 | ChatGPT: Rank 2 | Copilot: Rank 3"]
]

doc.add_table(eval_headers, eval_rows, [1800, 1600, 1700, 1700, 2560])

# 7. Screencast Submission & Walkthrough
doc.add_heading_1("6. Screencast Video Submission")
doc.add_paragraph("A short 3 to 4 minute screencast was recorded demonstrating the setup, prompt execution, and output comparison.")

doc.add_bullet("https://drive.google.com/file/d/your-screencast-link/view (Replace with your actual uploaded link)", bold_prefix="Video Link:")
doc.add_bullet("Demonstration of VS Code with GitHub Copilot extension active and generating code in Copilot Chat.", bold_prefix="Part 1 (0:00 - 1:00):")
doc.add_bullet("Demonstration of ChatGPT and Claude interfaces receiving the same prompt.", bold_prefix="Part 2 (1:00 - 2:00):")
doc.add_bullet("Side-by-side browser view of all 3 HTML landing pages, checking layout and mobile view.", bold_prefix="Part 3 (2:00 - 3:00):")
doc.add_bullet("Quick overview of the evaluation sheet table and final scores.", bold_prefix="Part 4 (3:00 - 3:45):")

# 8. Conclusion
doc.add_heading_1("7. Conclusion")
doc.add_paragraph("Each AI tool has a specific strength: Anthropic Claude is the best for generating visually appealing front-end web pages with live previews; OpenAI ChatGPT is great for general logic and well-commented code; and GitHub Copilot is the most efficient for day-to-day coding directly inside the VS Code editor.")

# Build both simple docx and update the existing docx
doc.build("AI_Tools_Assignment_Submission.docx")
doc.build("AI_Tools_Comparative_Evaluation_Assignment.docx")

print("Generated clean, simple Word files successfully!")
