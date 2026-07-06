import gradio as gr
from src.ai_engine.vlm_parser import parse_material_image
from src.quantum_engine.circuit_factory import generate_barrier_circuit

def run_ai_to_quantum(vlm_text):
    # 1. AI Engine parses the text
    result = parse_material_image(vlm_text)
    if result["status"] == "error":
        return "AI Parsing Error", None
    
    # 2. Quantum Engine generates the visualization
    coords = result["coords"]
    qc = generate_barrier_circuit(coords)
    
    return f"Detected {result['defect_type']} at {coords}", qc.draw(output='text')

with gr.Blocks() as app:
    gr.Markdown("# 👁️ AI-to-Quantum Discovery Pipeline")
    vlm_input = gr.Textbox(label="VLM Inference (JSON Output)", value='{"coordinates": [5, 10, 2], "defect_type": "vacancy"}')
    btn = gr.Button("Analyze and Generate Circuit")
    out_txt = gr.Textbox(label="Detection Results")
    out_qc = gr.Textbox(label="Quantum Circuit")
    
    btn.click(run_ai_to_quantum, inputs=vlm_input, outputs=[out_txt, out_qc])

app.launch(server_name="0.0.0.0", server_port=8080)