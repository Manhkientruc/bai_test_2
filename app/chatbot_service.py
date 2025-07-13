import re

def chatbot_response(transcript: str) -> str:
    rules = [
        # English rules
        (r"\bhi\b|\bhello\b|\bhey\b", "Hi there! How can I assist you today? 😊"),
        (r"\bproblem\b|\bissue\b|\btrouble\b", "I'm here to help. Can you describe the problem in more detail?"),
        (r"\baccount\b", "Sure, I can help you with your account. What seems to be the issue?"),
        (r"\bpassword\b", "Need to reset your password? I can walk you through the steps."),
        (r"\bforgot\b.*\bpassword\b", "No worries! Let's reset your password together."),
        (r"\blogin\b|\bsign in\b", "Are you having trouble logging in? I can assist you with that."),
        (r"\bpayment\b|\bbill\b|\bpay\b", "You can check your billing details in your account settings."),
        (r"\bcancel\b.*\baccount\b", "I'm sorry to hear that. I can help you cancel your account if you’d like."),
        (r"\bupdate\b.*\binfo\b|\bemail\b", "Want to update your information? I can guide you through."),
        (r"\bthanks\b|\bthank you\b", "You're welcome! Let me know if there's anything else. 🙌"),
        (r"\bbye\b|\bgoodbye\b", "Goodbye! Have a great day ahead! 👋")

        #Vietnamese rules
        (r"\bxin chào\b|\bchào\b", "Chào bạn! Mình có thể giúp gì cho bạn nè? 👋"),
        (r"\btài khoản\b", "Bạn gặp vấn đề tài khoản à? Để mình hỗ trợ nha."),
        (r"\bđăng nhập\b|\bkhông vào được\b", "Bạn đang gặp lỗi khi đăng nhập đúng không? Mình giúp liền."),
        (r"\bmật khẩu\b|\bquên mật khẩu\b", "Không sao, mình sẽ giúp bạn đặt lại mật khẩu nè."),
        (r"\bhủy tài khoản\b|\bxóa tài khoản\b", "Nếu bạn cần hủy tài khoản, mình có thể hỗ trợ."),
        (r"\bcảm ơn\b|\bthanks\b", "Rất vui được giúp bạn! Có gì cứ hỏi tiếp nha 😊"),
        (r"\btạm biệt\b|\bhẹn gặp lại\b", "Tạm biệt bạn nhé, chúc một ngày vui vẻ 🧡"),
        (r"\bthanh toán\b|\bhóa đơn\b", "Bạn có thể kiểm tra hóa đơn trong phần tài khoản."),
        (r"\bgiao hàng\b|\bvận chuyển\b", "Thời gian giao hàng dự kiến là 3–5 ngày."),
        (r"\bđơn hàng\b|\btrạng thái\b", "Bạn muốn kiểm tra đơn hàng à? Để mình kiểm tra giúp.")

        #Chinese rules
        (r"你好|您好", "你好～ 我可以幫你什麼呢？😄"),
        (r"帳號|账号", "我可以協助你處理帳號問題。"),
        (r"登入|登錄", "你遇到登入的問題嗎？我可以幫你看看。"),
        (r"密碼|密码", "需要重設密碼嗎？我來幫你。"),
        (r"忘記密碼", "沒關係，我們可以一起重設喔！"),
        (r"付款|支付|賬單|账单", "你可以在設定裡查詢付款資訊。"),
        (r"取消|刪除帳號", "你想取消帳號嗎？我可以協助。"),
        (r"謝謝|谢谢", "不客氣喔～ 祝你有美好的一天 🙌"),
        (r"再見|拜拜", "再見啦！有需要再找我 👋")

        #Japanese rules
        (r"こんにちは|こんばんは", "こんにちは！どのようにお手伝いできますか？😊"),
        (r"アカウント|アカ", "アカウントに関する問題ですね。お手伝いします！"),
        (r"ログイン|サインイン", "ログインに問題がありますか？確認してみましょう。"),
        (r"パスワード|パス忘れ", "パスワードをリセットしましょうか？"),
        (r"支払い|請求", "お支払い情報はアカウント設定で確認できます。"),
        (r"注文|ステータス", "ご注文の状況を確認しましょう。"),
        (r"キャンセル|削除", "アカウントをキャンセルしたい場合は、お手伝いします。"),
        (r"ありがとう|感謝", "どういたしまして！また何かあれば言ってくださいね 🙏"),
        (r"さようなら|バイバイ", "さようなら！良い一日を 👋"),
        (r"メール|情報変更", "メールアドレスや情報の更新をご希望ですか？")

        #Spanish rules
        (r"hola|buenas", "¡Hola! ¿En qué puedo ayudarte hoy? 😊"),
        (r"cuenta", "Puedo ayudarte con tu cuenta. ¿Qué pasa exactamente?"),
        (r"iniciar sesión|login", "¿Tienes problemas para iniciar sesión? Te puedo ayudar."),
        (r"contraseña|clave", "¿Quieres restablecer tu contraseña? Te muestro cómo."),
        (r"correo electrónico|email", "¿Necesitas cambiar tu correo? ¡Claro que sí!"),
        (r"pago|factura|cobro", "Puedes ver tus pagos en la configuración de la cuenta."),
        (r"cancelar|eliminar cuenta", "¿Deseas cancelar tu cuenta? Te puedo guiar."),
        (r"gracias|muchas gracias", "¡De nada! Estoy para ayudarte 🙌"),
        (r"adiós|hasta luego", "¡Hasta luego! Que tengas un buen día 👋"),
        (r"pedido|estado", "¿Quieres revisar el estado de tu pedido? Te ayudo.")
    ]

    transcript_lower = transcript.lower()

    for pattern, reply in rules:
        if re.search(pattern, transcript_lower):
            return reply

    return "I'm not sure I understand. Could you rephrase that or give me more info? 🤔"
