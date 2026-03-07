import os
from utils.analyzefile import  analyze_images, paths_to_images
from utils.wordoutput import text_to_word
from utils.pdftopicture import PDFtoPicture
from getprompt import get_main_prompt, get_support_prompt

def processfile(payload):
    """
    payload = {
        "api_key": api_key,
        "model": model,
        "selected_features": selected_features,
        "pdf_list": pdf_list,
        "image_list": image_list,
        "output_folder": output_folder,
        "extra_prompt": self.prompt_input.toPlainText()
    }
    """

    api_key = payload.get("api_key")
    model = payload.get("model")
    selected_features = payload.get("selected_features")
    pdf_list = payload.get("pdf_list")
    image_list = payload.get("image_list")
    output_folder = payload.get("output_folder")
    extra_prompt = payload.get("extra_prompt")
    UNITE_PROMPT = get_main_prompt()

    for feature in selected_features:
        UNITE_PROMPT = UNITE_PROMPT + "\n" + get_support_prompt(feature) + "\n" + extra_prompt
    
    print("📌開始進行轉換📌")
    print(f"🤖使用模型:{model}")
    for PDF in pdf_list:
        basename = os.path.splitext(os.path.basename(PDF))[0]
        print("--------------------------")
        print(f"🔴目前檔案:{basename}.pdf")
        #saving pictures
        print(f"🟠轉換中...")
        imageList =  PDFtoPicture(PDF)
        #Gemini_analyzing
        print(f"🟡分析中...")
        res = analyze_images(api_key, imageList, UNITE_PROMPT, model, basename+".pdf")
        filename = basename + ".docx"
        #write_to_word
        print("🟢正在寫入Word...")
        text_to_word(res,output_folder+"/"+filename)
        print(f"✅成功寫入{filename}")
    if image_list:
        imageList = paths_to_images(image_list)
        res = analyze_images(api_key, imageList, UNITE_PROMPT, model, "images")
        text_to_word(res,output_folder+"/picture.docx")
    return