from app.controllers import app, index, chat, entry, download_pdf

# ルートエンドポイント
app.add_api_route("/", index, methods=["GET"])
# chat
app.add_api_route("/chat", chat, methods=["GET", "POST"])
#entry
app.add_api_route("/entry" , entry, methods=["GET"])
# PDFダウンロード機能
app.add_api_route("/download-pdf", download_pdf, methods=["GET"], name="download_pdf")