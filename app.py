import os
from flask import Flask, render_template_string, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="UTF-8">
  <title>直播AI助手</title>
</head>
<body>
  <h1>直播 AI 助手</h1>

  <form method="POST">
    <select name="mode">
      <option value="product">商品介紹</option>
      <option value="customer_service">客服回覆</option>
    </select>

    <br><br>

    <textarea name="user_input" rows="6" cols="60" placeholder="輸入商品或客人問題"></textarea>

    <br><br>

    <button type="submit">產生</button>
  </form>

  <hr>

  <div style="white-space: pre-wrap;">{{ result }}</div>

</body>
</html>
"""

def load_prompt(mode):
    path = "prompts/product_prompt.txt" if mode == "product" else "prompts/customer_service_prompt.txt"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
        try:
            mode = request.form.get("mode", "product")
            user_input = request.form.get("user_input", "").strip()

            if not user_input:
                result = "請先輸入內容。"
                return render_template_string(HTML, result=result)

            system_prompt = load_prompt(mode)

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=f"{system_prompt}\n\n使用者輸入：{user_input}"
            )

            result = response.output_text if hasattr(response, "output_text") else str(response)

        except Exception as e:
            result = f"系統發生錯誤：{str(e)}"

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
