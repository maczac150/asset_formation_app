from fastapi import FastAPI, Request, Form
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import openai
import os
from openai import OpenAI
from openai.types import Completion
from dotenv import load_dotenv
from typing import List, Optional
import markdown
from fastapi.responses import FileResponse
from xhtml2pdf import pisa
import io
from starlette.responses import RedirectResponse
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from reportlab.pdfgen import canvas
from pathlib import Path
from datetime import datetime
import uvicorn




# .env をロード(APIキーの取得)
load_dotenv()


# 環境変数からAPIキーを取得
openai.api_key = os.getenv("OPENAI_API_KEY")

# メモリ内に gpt_response を一時保存する（セッション管理を使う方が適切）
cache = {}

app = FastAPI(
    title='FastAPIでつくるtoDoアプリケーション',
    description='FastAPIチュートリアル：FastAPI(とstarlette)でシンプルなtoDoアプリを作りましょう．',
    version='0.9 beta'
)

# new テンプレート関連の設定 (jinja2)
templates = Jinja2Templates(directory="app/templates")
jinja_env = templates.env  # Jinja2.Environment : filterやglobalの設定用


def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})



def entry(request: Request):
     return templates.TemplateResponse('entry.html', {'request': request})


@app.api_route("/chat", methods=["GET", "POST"], response_class=HTMLResponse)
async def chat(
    request: Request,
    interest: Optional[List[str]] = Form(None),
    skills: Optional[List[str]] = Form(None),
    working_style: Optional[str] = Form(None),
    future_life: Optional[str] = Form(None),
    target_income: Optional[str] = Form(None),
    family_plan: Optional[str] = Form(None),
    saving_plan: Optional[str] = Form(None),
    side_job_interest: Optional[str] = Form(None),
    side_job: Optional[List[str]] = Form(None),
    investment_mindset: Optional[str] = Form(None),
    work_values: Optional[str] = Form(None),
    money_priority: Optional[str] = Form(None),
):

    if request.method == "GET":
        return templates.TemplateResponse("chat.html", {"request": request, "gpt_response": None})

    # GPT に送信する内容を作成
    user_input = (
        f"以下はユーザーが回答したアンケートの内容です:\n"
        f"- 興味のある分野や業界: {', '.join(interest) if interest else '未選択'}\n"
        f"- 得意なこと・スキル: {', '.join(skills) if skills else '未選択'}\n"
        f"- 働き方: {working_style if working_style else '未選択'}\n"
        f"- 将来したい生活: {future_life if future_life else '未選択'}\n"
        f"- 目標年収: {target_income if target_income else '未選択'}\n"
        f"- 将来の家族構成: {family_plan if family_plan else '未選択'}\n"
        f"- 貯蓄計画: {saving_plan if saving_plan else '未選択'}\n"
        f"- 副業への興味: {side_job_interest if side_job_interest else '未選択'}\n"
        f"- 興味がある副業: {', '.join(side_job) if side_job else '未選択'}\n"
        f"- 投資に対する考え方: {investment_mindset if investment_mindset else '未選択'}\n"
        f"- 働く上で大切にしたい価値観: {work_values if work_values else '未選択'}\n"
        f"- お金の使い方の優先事項: {money_priority if money_priority else '未選択'}\n"
    )

    #print(user_input)

    prompt_input = """
あなたはキャリアアドバイザーと資産形成のプロフェッショナルです。ユーザの回答内容を分析し、以下のマークダウン形式の例に従って提案を行ってください．

## ライフプランに基づいた資産計画

## あなたが適している職業
### 職業１
* 業界
* 想定年収
* 昇給ペース
* 理由
### 職業２
* 業界
* 想定年収
* 昇給ペース
* 理由
### 職業３
* 業界
* 想定年収
* 昇給ペース
* 理由

## 貯蓄計画
貯蓄計画の詳細をここに入力してください。
## ライフスタイルと支出
アンケート結果に基づいたライフスタイルと支出の詳細をここに記載してください。

## 資産形成のための具体的な提案
### 副業について
* 副業：質問9の回答に基づいて、ここに具体的な副業の提案内容を記載してください
* 副業の詳細：質問9の回答に基づいて、ここに具体的な副業の詳細を記載してください
### 投資について
* 投資：質問10の回答に基づいて、ここに具体的な投資の提案内容を記載してください。
* 投資の詳細：質問10の回答に基づいて、ここに具体的な投資の詳細を記載してください。

### 各質問に対するあなたの回答
* 質問1の内容：質問1の回答
* 質問2の内容：質問2の回答
* 質問3の内容：質問3の回答
* 質問4の内容：質問4の回答
* 質問5の内容：質問5の回答
* 質問6の内容：質問6の回答
* 質問7の内容：質問7の回答
* 質問8の内容：質問8の回答
* 質問9の内容：質問9の回答
* 質問10の内容：質問10の回答
* 質問11の内容：質問11の回答
* 質問12の内容：質問12の回答
"""

    try:
        response = openai.chat.completions.create(
            #model="gpt-3.5-turbo",
            model = "gpt-4o",
            messages=[
                {"role": "system", "content": prompt_input},
                {"role": "user", "content": user_input},
            ]
        )

        #gpt_response = response['choices'][0]['message']['content']
        gpt_response=response.choices[0].message.content
        gpt_response_html = markdown.markdown(gpt_response)
        #print(gpt_response_html)
    except openai.AuthenticationError as e:
        gpt_response = f"APIキーが正しく設定されていません: {str(e)}"
    except openai.RateLimitError as e:
        gpt_response = f"リクエストの上限に達しました。しばらくしてから再試行してください: {str(e)}"
    except openai.OpenAIError as e:
        gpt_response = f"OpenAIのエラーが発生しました: {str(e)}"
    except Exception as e:
        gpt_response = f"不明なエラーが発生しました: {str(e)}"

    # gpt_response_html をキャッシュに保存
    cache["last_gpt_response"] = gpt_response
    return templates.TemplateResponse("chat.html", {"request": request, "gpt_response": gpt_response_html})

@app.get("/download_pdf", response_class=HTMLResponse)
async def download_pdf():
    # gpt_response_html をキャッシュから取得
    gpt_response_html = cache.get("last_gpt_response", None)

    if not gpt_response_html:
        return JSONResponse({"error": "No GPT response available for download"}, status_code=400)

    # メモリ内で PDF を生成
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)

    # ページ設定
    c.setFont("Helvetica", 12)
    text = c.beginText(50, 800)  # 開始位置 (x, y)

    # HTML をテキストに変換して PDF に挿入
    lines = gpt_response_html.split("\n")
    for line in lines:
        text.textLine(line)  # 各行を PDF に追加

    c.drawText(text)
    c.showPage()
    c.save()

    buffer.seek(0)  # バッファを先頭に戻す

    # PDF をレスポンスとして返す
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=asset_result.pdf"}
    )




